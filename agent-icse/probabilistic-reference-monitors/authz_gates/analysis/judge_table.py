#!/usr/bin/env python3
"""One table across every judge's frozen-threshold validation (judge_validation.py output).

  python3 analysis/judge_table.py artifact/validation_groq_*.json --out artifact/JUDGES.md

Columns, all at alpha/delta as certified: the single-run threshold and the worst-case-over-
runs threshold (the one to deploy), how much safe traffic the latter automates on main and
held-out, how many held-out destructive calls it lets through, and what the copied vendor
constant 0.9 does on the same data. Stdlib only.
"""
import argparse
import json
import os


def pct(a, n):
    return f"{a}/{n} ({a / n:.0%})" if n else "-"


def row(name, v):
    c = v["certified_operating_point"]
    w = v.get("worst_case_certified") or {}
    hw = v.get("heldout_at_worst_case_t") or v.get("heldout") or {}
    vm, vh = v.get("vendor_0.9", {}), v.get("heldout_vendor_0.9", {})
    st = v.get("stability", {})
    runs = len(v.get("repeats", [])) + 1
    stable = f"{st.get('identical_scores', '-')}/{st.get('n_items', '-')}" if st else "-"
    safe_main = (f"{w['safe_auto_allowed']:.0%}" if w else f"{c['safe_auto_allowed']:.0%}")
    return (f"| {name} | {runs} | {stable} | {c['t']} | {w.get('t', '-')} | {safe_main} | "
            f"**{hw.get('destr_allowed', '-')}/{hw.get('destr_n', '-')}** | "
            f"{pct(hw.get('safe_automated', 0), hw.get('safe_n', 0))} | "
            f"{vm.get('false_allows', '-')}/{vm.get('n_allowed', '-')} | "
            f"{vh.get('destr_allowed', '-')}/{vh.get('destr_n', '-')} |")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("validations", nargs="+")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    lines = ["| judge | runs | items scored identically | t (run 1) | t (worst case, deploy) | "
             "main safe automated | held-out destructive allowed | held-out safe automated | "
             "vendor 0.9 main false allows | vendor 0.9 held-out destructive allowed |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for p in args.validations:
        v = json.load(open(p))
        if not v.get("certified_operating_point"):
            vm, vh = v.get("vendor_0.9") or {}, v.get("heldout_vendor_0.9") or {}
            lines.append(f"| {v.get('name', p)} | {len(v.get('repeats', [])) + 1 if v.get('repeats') else '-'} "
                         f"| - | none | none | 0% (refuses) | 0 | 0 | "
                         f"{vm.get('false_allows', '-')}/{vm.get('n_allowed', '-')} | "
                         f"{vh.get('destr_allowed', '-')}/{vh.get('destr_n', '-')} |")
            continue
        lines.append(row(v.get("name") or os.path.basename(p), v))
    md = "\n".join(lines) + "\n"
    print(md)
    if args.out:
        with open(args.out, "w") as f:
            f.write(md)


if __name__ == "__main__":
    main()
