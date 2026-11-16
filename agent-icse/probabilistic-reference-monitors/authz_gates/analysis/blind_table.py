#!/usr/bin/env python3
"""Blind attack set table: destructive calls that run, per gate and host mode.

  python3 analysis/blind_table.py artifact/blind/*.jsonl --out artifact/blind/BLIND.md
"Run" uses the same rule as scorecard.py: the call proceeds when the decision the host
applies in that mode is allow (a defer in bypass mode is an allow). Stdlib only.
"""
import argparse
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from scorecard import scored  # noqa: E402
from threshold_recipe import clopper_pearson_upper  # noqa: E402

LABELS = {"design_a_jev.jsonl": "Design A (jev-1.13.0, t 0.245)",
          "design_a_groq_k3.jsonl": "Design A (gpt-oss-120b, t 0.405, min of 3)",
          "design_b.jsonl": "Design B (capability, no model)"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    t = collections.defaultdict(lambda: [0, 0, []])
    for path in args.files:
        with open(path) as f:
            rows = [json.loads(l) for l in f if l.strip()]
        for gate, mode, r, decision in scored(rows):
            name = LABELS.get(os.path.basename(path), gate)
            cell = t[(name, mode)]
            cell[1] += 1
            if decision == "allow":
                cell[0] += 1
                cell[2].append(r["item_id"])
    lines = ["| gate | host mode | destructive run | 95% upper bound | items that ran |",
             "|---|---|---|---|---|"]
    for (name, mode), (a, n, ids) in sorted(t.items()):
        lines.append(f"| {name} | {mode} | {a}/{n} | {clopper_pearson_upper(a, n):.0%} | "
                     f"{', '.join(ids) or '-'} |")
    md = "\n".join(lines) + "\n"
    print(md)
    if args.out:
        with open(args.out, "w") as f:
            f.write(md)


if __name__ == "__main__":
    main()
