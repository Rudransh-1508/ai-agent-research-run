#!/usr/bin/env python3
"""Attach a 95% confidence interval to every headline rate in the study.

Each proportion (destructive calls run, safe calls auto-approved, ...) is an estimate from a
finite corpus; we report a Wilson 95% interval and, for zero-count rates, the one-sided
Clopper-Pearson upper bound. Reads the committed live result files (the scorecard sources,
both designs) and writes artifact/CONFIDENCE.md. Stdlib only.
"""
import collections
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def cp_upper(k, n, alpha=0.05):
    if n == 0:
        return 1.0
    if k == 0:
        return 1 - alpha ** (1 / n)
    from math import comb
    lo, hi = 0.0, 1.0
    for _ in range(100):
        m = (lo + hi) / 2
        tail = sum(comb(n, i) * m ** i * (1 - m) ** (n - i) for i in range(k + 1))
        hi, lo = (m, lo) if tail <= alpha else (hi, m)
    return hi


def fmt(k, n):
    if n == 0:
        return "-"
    lo, hi = wilson(k, n)
    if k == 0:
        return f"0/{n} (<={cp_upper(k,n)*100:.1f}%)"
    return f"{k}/{n} ({100*k/n:.0f}%, 95% CI {100*lo:.1f}-{100*hi:.1f}%)"


def load(path):
    return [json.loads(l) for l in open(path)] if os.path.exists(path) else []


def destr_run(rows, gate, mode):
    sel = [r for r in rows if r["gate"] == gate and not r["disputable"]
           and r["label"] == "destructive" and (not r.get("host_mode") or r["host_mode"] == mode)]
    k = sum(1 for r in sel if r.get(f"decision_{mode}") == "allow")
    return k, len(sel)


def safe_auto(rows, gate):
    # restrict to default-mode rows (per-mode files duplicate each item per host mode),
    # dedup by item_id; auto-approved = allow with no human prompt in default mode
    seen = {}
    for r in rows:
        if r["gate"] != gate or r.get("tier") != "clearly_safe":
            continue
        if r.get("host_mode") not in (None, "default"):
            continue
        seen[r["item_id"]] = r.get("decision_default") == "allow"
    return sum(seen.values()), len(seen)


def main():
    R = os.path.join(ROOT, "faultinject/results")
    A = os.path.join(ROOT, "artifact")
    main_src = {"jev-guard,jev-engineering,jev-engineering(guard),jev-engineering(auto)": f"{R}/live_main_head.jsonl",
                "dcg,cc-safety-net": f"{A}/scorecard-baselines/live_main.jsonl",
                "sdkks(cli)": f"{A}/scorecard-sdkks-cli/live_main.jsonl",
                "agentguards": f"{A}/scorecard-agentguards/live_main.jsonl",
                "design (A)": f"{A}/design-v2/live_main.jsonl",
                "design (B, capability)": f"{A}/design-capability/live_main.jsonl"}
    hld_src = {k: v.replace("live_main", "live_heldout").replace("_main_head", "_heldout_head")
               for k, v in main_src.items()}
    ovr_src = {k: v.replace("live_main", "live_oversize").replace("_main_head", "_oversize_head")
               for k, v in main_src.items()}

    lines = ["# Confidence intervals on the headline rates", "",
             "Wilson 95% interval; zero-count rates give the one-sided Clopper-Pearson 95% "
             "upper bound. Destructive-run is under bypassPermissions.", "",
             "| gate | destructive run (main) | (held-out) | padded | safe auto-approved (default) |",
             "|---|---|---|---|---|"]
    for key, mf in main_src.items():
        gates = key.split(",") if "," in key else [key.split(" (")[0]] if key.startswith("design") else [key]
        gname = "design" if key.startswith("design") else None
        for g in ([gname] if gname else gates):
            label = key if key.startswith("design") else g
            mr, hr, orr = load(mf), load(hld_src[key]), load(ovr_src[key])
            md = fmt(*destr_run(mr, g, "auto"))
            hd = fmt(*destr_run(hr, g, "auto"))
            od = fmt(*destr_run(orr, g, "auto"))
            sa = fmt(*safe_auto(mr, g))
            lines.append(f"| {label} | {md} | {hd} | {od} | {sa} |")
    open(os.path.join(A, "CONFIDENCE.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
