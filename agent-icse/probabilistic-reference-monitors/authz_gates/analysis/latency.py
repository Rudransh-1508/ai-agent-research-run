#!/usr/bin/env python3
"""Per-gate decision latency, and the design's fast-path vs model-path split.

A gate sits in the critical path of every tool call, so its added latency is a deployment
property, not an afterthought. We report wall-clock seconds per decision (median, p95) from
the live runs. Deterministic gates (dcg, cc-safety-net) pay only local compute; model-backed
gates pay a model round-trip. The composed design is asymmetric by construction: most calls
are decided deterministically (read-only allow, dcg/tactic deny, scratch-write, oversize)
with no model call, and only the ambiguous minority pays the judge - this script quantifies
that split from the gate's own decision reason. Same machine; network RTT (TypeSafe) varies.
Stdlib only.
"""
import argparse
import collections
import glob
import json
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")


def pct(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    k = min(len(xs) - 1, int(round((p / 100.0) * (len(xs) - 1))))
    return xs[k]


def design_path(row):
    """Classify a design-gate row as model or deterministic from its reason."""
    tail = row.get("stdout_tail", "")
    if '\\"model\\": \\"ok\\"' in tail or '"model": "ok"' in tail:
        return "model"
    return "deterministic"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--inputs", nargs="+", default=None,
                    help="live_*.jsonl files; default = the committed scorecard mains + design-v2")
    ap.add_argument("--out", default=os.path.join(ROOT, "artifact/LATENCY.md"))
    args = ap.parse_args()

    inputs = args.inputs or ([
        os.path.join(ROOT, "faultinject/results/live_main_head.jsonl"),
        os.path.join(ROOT, "artifact/scorecard-baselines/live_main.jsonl"),
        os.path.join(ROOT, "artifact/scorecard-sdkks-cli/live_main.jsonl"),
        os.path.join(ROOT, "artifact/scorecard-agentguards/live_main.jsonl"),
    ] + glob.glob(os.path.join(ROOT, "artifact/design-v2/live_main.jsonl")))

    by_gate = collections.defaultdict(list)
    design_rows = []
    for f in inputs:
        if not os.path.exists(f):
            continue
        for row in (json.loads(l) for l in open(f)):
            w = row.get("wall_s")
            if w is None:
                continue
            by_gate[row["gate"]].append(w)
            if row["gate"] == "design":
                design_rows.append(row)

    MODEL_BACKED = {"jev-guard", "sdkks(cli)", "agentguards", "design",
                    "jev-engineering", "jev-engineering(guard)", "jev-engineering(auto)"}
    lines = ["# Gate decision latency (same machine; model-backed gates include network RTT)", "",
             "Wall-clock seconds per decision, from the live main-corpus runs. Deterministic "
             "gates pay local compute only; model-backed gates pay a model round-trip.", "",
             "| gate | kind | n | median (s) | p95 (s) |", "|---|---|---|---|---|"]
    for g in sorted(by_gate):
        xs = by_gate[g]
        kind = "model-backed" if g in MODEL_BACKED else "deterministic"
        lines.append(f"| {g} | {kind} | {len(xs)} | {statistics.median(xs):.2f} | {pct(xs,95):.2f} |")

    if design_rows:
        det = [r["wall_s"] for r in design_rows if design_path(r) == "deterministic"]
        mod = [r["wall_s"] for r in design_rows if design_path(r) == "model"]
        tot = len(det) + len(mod)
        lines += ["", "## Design: fast path vs model path", "",
                  f"Of {tot} decisions, **{len(det)} ({100*len(det)/tot:.0f}%) were decided "
                  f"deterministically with no model call**; {len(mod)} paid the judge.", "",
                  "| path | n | median (s) | p95 (s) |", "|---|---|---|---|",
                  f"| deterministic (fast) | {len(det)} | {statistics.median(det):.2f} | {pct(det,95):.2f} |"
                  if det else "| deterministic (fast) | 0 | - | - |",
                  f"| model | {len(mod)} | {statistics.median(mod):.2f} | {pct(mod,95):.2f} |"
                  if mod else "| model | 0 | - | - |"]
    open(args.out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
