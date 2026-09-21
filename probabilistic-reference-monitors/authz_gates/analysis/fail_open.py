#!/usr/bin/env python3
"""Fail-open tabulation + P1-P4 computation over corpus/gates.json.

gates.json is produced by the corpus-extraction agent. This script codes against
the extraction fields fixed in PREREGISTRATION.md; the assumed schema (tolerant —
missing fields are classified, never dropped) is:

  gates.json: a JSON list, or {"gates": [...]}, of gate records:
    repo            str, required-ish (falls back to "unknown:<i>")
    sha             str | null          pinned commit
    in_pilot_set    bool (default false)  pilot-set membership for the split report
    primitives      [ "Choice" | "Score" | "Noul", ... ]
    questions       [ str, ... ]
    action_set      [ str, ... ]
    attacker_reachable_unsanitised  bool | null
    thresholds      [ {"value": float, "provenance": str, "evidence": str}, ... ]
                      provenance in {documented-derivation, swept-on-data,
                      copied-from-vendor-docs, undocumented}; missing -> undocumented
    error_paths     { "<mode>": "<classification>" }
                      mode in {timeout, http_429, http_5xx, malformed_response}
                      (aliases 429/5xx/malformed are normalized)
                      classification in {fail-open, fail-closed, partial,
                      undocumented, unclassifiable}
    fail_classification  str | null   overall label from the extraction agent
    cites_cross_evaluation  bool (default false)  cites a published evaluation
                      against another gate or a public benchmark with baselines
    evidence        [ "file:line ...", ... ]

Registered predictions computed:
  P1  >= 50% of gates with a determinable error path fail open on >= 1 of
      timeout / 429 / 5xx / malformed response.
  P2  >= 60% of threshold constants have no documented derivation
      (undocumented or copied-from-vendor-docs).
  P3  >= 1 gate ships the vendor docs' illustrative threshold (0.9 or 0.5)
      verbatim.
  P4  no gate cites a published cross-evaluation.

Per PREREGISTRATION.md, P1-P4 are reported for the full corpus AND separately
for the held-out remainder (gates not in the pilot set).

Output: JSON + Markdown table (the paper table is regenerable). Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re

FAILURE_MODES = ["timeout", "http_429", "http_5xx", "malformed_response"]
MODE_ALIASES = {"429": "http_429", "http429": "http_429", "rate_limit": "http_429",
                "5xx": "http_5xx", "http500": "http_5xx", "server_error": "http_5xx",
                "malformed": "malformed_response", "bad_json": "malformed_response",
                "timeout": "timeout", "http_429": "http_429", "http_5xx": "http_5xx",
                "malformed_response": "malformed_response"}
DETERMINABLE = {"fail-open", "fail-closed", "partial"}
VENDOR_CONSTANTS = (0.9, 0.5)
NO_DERIVATION = {"undocumented", "copied-from-vendor-docs"}


def normalize_gate(g, i):
    gate = dict(g)
    gate.setdefault("repo", f"unknown:{i}")
    gate["in_pilot_set"] = bool(gate.get("in_pilot_set", False))
    raw_paths = gate.get("error_paths") or {}
    paths = {}
    for k, v in raw_paths.items():
        mode = MODE_ALIASES.get(str(k).lower())
        if mode:
            paths[mode] = str(v).lower()
    for mode in FAILURE_MODES:
        paths.setdefault(mode, "undocumented")
    gate["error_paths_norm"] = paths
    thresholds = []
    for t in gate.get("thresholds") or []:
        if isinstance(t, (int, float)):
            t = {"value": float(t)}
        t = dict(t)
        try:
            t["value"] = float(t.get("value"))
        except (TypeError, ValueError):
            m = re.search(r"-?\d+(?:\.\d+)?", str(t.get("value")))
            t["value"] = float(m.group(0)) if m else None
        t["provenance"] = str(t.get("provenance") or "undocumented").lower()
        thresholds.append(t)
    gate["thresholds_norm"] = thresholds
    gate["cites_cross_evaluation"] = bool(
        gate.get("cites_cross_evaluation",
                 gate.get("cites_published_evaluation", False)))
    return gate


def wilson_ci(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (round(max(0.0, center - half), 4), round(min(1.0, center + half), 4))


def compute_predictions(gates):
    """Compute P1-P4 over one set of gates. Returns counts + verdicts."""
    # P1: fail-open on >= 1 failure mode, among gates with a determinable path.
    # A per-mode "partial" means the action sometimes proceeds under that failure
    # mode, which is security-relevant fail-open behaviour; this matches the
    # counting rule fixed in corpus/build_table.py and PREREGISTRATION.md.
    determinable, fail_open_gates = [], []
    for g in gates:
        paths = g["error_paths_norm"]
        if any(paths[m] in DETERMINABLE for m in FAILURE_MODES):
            determinable.append(g)
            if any(paths[m] in ("fail-open", "partial") for m in FAILURE_MODES):
                fail_open_gates.append(g)
    n_det = len(determinable)
    p1_frac = len(fail_open_gates) / n_det if n_det else None
    p1_ci = wilson_ci(len(fail_open_gates), n_det)

    # per-mode tabulation (paper table body)
    mode_table = {m: {"fail-open": 0, "fail-closed": 0, "partial": 0,
                      "undocumented": 0, "unclassifiable": 0}
                  for m in FAILURE_MODES}
    for g in gates:
        for m in FAILURE_MODES:
            cls = g["error_paths_norm"][m]
            mode_table[m][cls if cls in mode_table[m] else "unclassifiable"] += 1

    # P2: threshold provenance
    all_thresholds = [(g["repo"], t) for g in gates for t in g["thresholds_norm"]]
    n_thr = len(all_thresholds)
    n_no_deriv = sum(1 for _, t in all_thresholds if t["provenance"] in NO_DERIVATION)
    p2_frac = n_no_deriv / n_thr if n_thr else None
    p2_ci = wilson_ci(n_no_deriv, n_thr)

    # P3: vendor constants shipped verbatim
    p3_hits = sorted({repo for repo, t in all_thresholds
                      if t["value"] is not None
                      and any(abs(t["value"] - v) < 1e-9 for v in VENDOR_CONSTANTS)})

    # P4: cross-evaluation citations
    p4_hits = sorted({g["repo"] for g in gates if g["cites_cross_evaluation"]})

    return {
        "n_gates": len(gates),
        "fail_open_table": mode_table,
        "P1": {"n_determinable": n_det, "n_fail_open": len(fail_open_gates),
               "fraction": round(p1_frac, 4) if p1_frac is not None else None,
               "ci95": p1_ci, "threshold": 0.5,
               "supported": (p1_frac is not None and p1_frac >= 0.5),
               "gates": sorted(g["repo"] for g in fail_open_gates)},
        "P2": {"n_thresholds": n_thr, "n_no_derivation": n_no_deriv,
               "fraction": round(p2_frac, 4) if p2_frac is not None else None,
               "ci95": p2_ci, "threshold": 0.6,
               "supported": (p2_frac is not None and p2_frac >= 0.6)},
        "P3": {"vendor_constants": list(VENDOR_CONSTANTS),
               "gates": p3_hits, "supported": len(p3_hits) >= 1},
        "P4": {"gates_citing_cross_evaluation": p4_hits,
               "supported": len(p4_hits) == 0},
    }


def render_markdown(report):
    def section(name, res):
        lines = [f"## {name} (n={res['n_gates']})", ""]
        lines.append("| failure mode | fail-open | fail-closed | partial | undocumented | unclassifiable |")
        lines.append("|---|---|---|---|---|---|")
        for m in FAILURE_MODES:
            t = res["fail_open_table"][m]
            lines.append(f"| {m} | {t['fail-open']} | {t['fail-closed']} "
                         f"| {t['partial']} | {t['undocumented']} | {t['unclassifiable']} |")
        lines.append("")
        for p in ("P1", "P2", "P3", "P4"):
            r = res[p]
            lines.append(f"- **{p}**: supported={r['supported']} — "
                         + json.dumps({k: v for k, v in r.items()
                                       if k not in ("supported", "gates")}))
        lines.append("")
        return lines

    lines = ["# Fail-open tabulation and P1-P4", ""]
    lines += section("Full corpus", report["full_corpus"])
    if report.get("held_out_remainder"):
        lines += section("Held-out remainder (non-pilot gates)",
                         report["held_out_remainder"])
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gates", required=True, help="corpus/gates.json")
    ap.add_argument("--out-prefix", required=True,
                    help="writes <out-prefix>.json and <out-prefix>.md")
    args = ap.parse_args()

    with open(args.gates) as f:
        data = json.load(f)
    raw_gates = data["gates"] if isinstance(data, dict) else data
    gates = [normalize_gate(g, i) for i, g in enumerate(raw_gates)]

    report = {"source": os.path.basename(args.gates),
              "full_corpus": compute_predictions(gates)}
    remainder = [g for g in gates if not g["in_pilot_set"]]
    if remainder and len(remainder) < len(gates):
        report["held_out_remainder"] = compute_predictions(remainder)
    else:
        report["held_out_remainder"] = None

    os.makedirs(os.path.dirname(os.path.abspath(args.out_prefix)), exist_ok=True)
    with open(args.out_prefix + ".json", "w") as f:
        json.dump(report, f, indent=2, sort_keys=True)
    with open(args.out_prefix + ".md", "w") as f:
        f.write(render_markdown(report))
    print(render_markdown(report))


if __name__ == "__main__":
    main()
