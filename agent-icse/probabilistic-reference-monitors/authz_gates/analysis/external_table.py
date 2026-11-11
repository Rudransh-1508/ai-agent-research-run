#!/usr/bin/env python3
"""Per-gate results on the external attack split: real MITRE ATT&CK commands from Atomic Red
Team (artifact/scorecard-external/live_external.jsonl), each sandbox-verified destructive.
Reports how many run unchecked (default/bypass) and a per-ATT&CK-technique coverage line."""
import argparse
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
ORDER = ["jev-guard", "jev-engineering", "jev-engineering(guard)", "jev-engineering(auto)",
         "dcg", "cc-safety-net", "sdkks(cli)", "agentguards"]
TECH = {"T1048": "Exfil over alt protocol", "T1070": "Indicator removal",
        "T1567": "Exfil over web service"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--external", default=os.path.join(ROOT, "artifact/scorecard-external/live_external.jsonl"))
    ap.add_argument("--corpus", default=os.path.join(ROOT, "benchmark/corpus_heldout.jsonl"))
    ap.add_argument("--out", default=os.path.join(ROOT, "artifact/scorecard-external/EXTERNAL.md"))
    args = ap.parse_args()

    items = {i["id"]: i for i in map(json.loads, open(args.corpus)) if i["tier"] == "attack_external"}
    n = len(items)
    rows = collections.defaultdict(list)
    for r in map(json.loads, open(args.external)):
        rows[r["gate"]].append(r)
    techs = sorted({i["attack"]["vector"].split(".")[0] for i in items.values()})

    lines = ["# External attack split: real MITRE ATT&CK commands (Atomic Red Team)", "",
             f"{n} commands drawn from Atomic Red Team (MIT; `benchmark/external/`), one per Linux "
             "`sh`/`bash` atomic in our threat-model techniques whose destructive or exfiltration "
             "effect was confirmed in the sandbox. Each is a real attacker command mapped to a "
             "MITRE ATT&CK technique. Default = a human answers; bypass = a deferred call runs. "
             "Raw: `artifact/scorecard-external/live_external.jsonl`.", "",
             "| gate | run (default) | run (bypass) | ATT&CK techniques fully blocked (bypass) |",
             "|---|---|---|---|"]
    for g in [g for g in ORDER if g in rows]:
        rs = [r for r in rows[g] if not r["disputable"]]
        md = sum(r.get("decision_default") == "allow" for r in rs)
        ma = sum(r.get("decision_auto") == "allow" for r in rs)
        blocked = []
        for t in techs:
            tr = [r for r in rs if items[r["item_id"]]["attack"]["vector"].split(".")[0] == t]
            if tr and all(r.get("decision_auto") != "allow" for r in tr):
                blocked.append(t)
        cov = ", ".join(f"{t} {TECH.get(t, '')}".strip() for t in blocked) or "none"
        lines.append(f"| {g} | {md}/{n} | {ma}/{n} | {cov} |")
    open(args.out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
