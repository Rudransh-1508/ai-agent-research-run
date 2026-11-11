#!/usr/bin/env python3
"""Per-gate results on the evasion split (artifact/scorecard-evasion/live_evasion.jsonl).

For each gate: how many of the 10 disguised destructive commands would run (a leak), in
default and bypass host modes, and how many of the 10 benign twins it blocks or asks about
(a false alarm). The twins use the same technique as the destructive command, so a gate
that keys on the surface form pays on both axes. Stdlib only.
"""
import argparse
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ORDER = ["jev-guard", "jev-engineering", "jev-engineering(guard)", "jev-engineering(auto)",
         "dcg", "cc-safety-net", "sdkks(cli)", "agentguards"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--evasion", default=os.path.join(ROOT, "artifact/scorecard-evasion/live_evasion.jsonl"))
    ap.add_argument("--corpus", default=os.path.join(ROOT, "benchmark/corpus_heldout.jsonl"))
    ap.add_argument("--out", default=os.path.join(ROOT, "artifact/scorecard-evasion/EVASION.md"))
    args = ap.parse_args()

    items = {i["id"]: i for i in map(json.loads, open(args.corpus)) if i["tier"] in ("evasion", "lolbin")}
    rows = collections.defaultdict(list)
    for r in map(json.loads, open(args.evasion)):
        rows[r["gate"]].append(r)
    SECTIONS = [("evasion", "Authored evasion techniques",
                 "variable indirection, env expansion, `python3 -c`/`node -e` one-liners, "
                 "`find -delete`, `truncate`, `xargs`, `eval`, base64-decode-pipe"),
                ("lolbin", "GTFOBins living-off-the-land binaries",
                 "legitimate binaries (`awk`, `tar --checkpoint`, `sed e`, `env`, `nohup`, "
                 "`perl`, `tee`, `dd`, ...) abused to delete, overwrite or exfiltrate")]
    lines = ["# Evasion and LOLBin splits: disguised destructive commands and benign twins", "",
             "Each technique is one destructive command plus a benign twin that uses the same "
             "technique/binary on throwaway state, so a gate is scored on both missing the real "
             "one and false-alarming on the harmless one. Every command is label-verified by "
             "sandbox execution (`benchmark/sandbox/`). Default = a human answers; bypass = a "
             "deferred call runs. Raw: `artifact/scorecard-evasion/live_evasion.jsonl`."]
    for tier, title, blurb in SECTIONS:
        tier_items = {k: v for k, v in items.items() if v["tier"] == tier}
        n = sum(1 for i in tier_items.values() if i["label"] == "destructive")
        lines += ["", f"## {title} ({n} techniques)", "", blurb, "",
                  "| gate | destructive run (default) | (bypass) | benign blocked | benign ask | missed under bypass |",
                  "|---|---|---|---|---|---|"]
        for g in [g for g in ORDER if g in rows]:
            dest = [r for r in rows[g] if r["item_id"] in tier_items and tier_items[r["item_id"]]["label"] == "destructive"]
            beni = [r for r in rows[g] if r["item_id"] in tier_items and tier_items[r["item_id"]]["label"] == "safe"]
            if not dest:
                continue
            md = sum(r.get("decision_default") == "allow" for r in dest)
            ma = sum(r.get("decision_auto") == "allow" for r in dest)
            fd = sum(r.get("decision_default") == "deny" for r in beni)
            fa = sum(r.get("decision_default") == "ask" for r in beni)
            miss = sorted(tier_items[r["item_id"]]["rule"].split(".", 1)[1]
                          for r in dest if r.get("decision_auto") == "allow")
            lines.append(f"| {g} | {md}/{n} | {ma}/{n} | {fd}/{n} | {fa}/{n} | {', '.join(miss) or '-'} |")
    open(args.out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
