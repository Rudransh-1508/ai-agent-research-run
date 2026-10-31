#!/usr/bin/env python3
"""Noise-floor analysis: spread of identical calls across repeats.

Reads the repeat result files (artifact/results_noise_r*.jsonl) and computes,
per item: spread (max-min of p_safe), decision-flip count (allow/ask/deny
changes across repeats), and confidence spread. This is the empirical null
distribution every other result is judged against (PREREGISTRATION.md, MR0
logic: if the model is non-deterministic, the floor is the null).

Usage: python3 analysis/noise_floor.py artifact/results_noise_r*.jsonl
       python3 analysis/noise_floor.py --self-test
"""

import json
import math
import statistics
import sys
from collections import Counter, defaultdict


def load_repeats(paths):
    per_item = defaultdict(list)
    for p in paths:
        for line in open(p):
            r = json.loads(line)
            if r.get("outcome") != "ok":
                continue
            per_item[r["item_id"]].append(
                {"p_safe": r["p_safe"], "decision": r["decision"],
                 "confidence": r.get("confidence"), "tier": r.get("tier")})
    return per_item


def analyze(per_item):
    rows = []
    for item_id, reps in sorted(per_item.items()):
        if len(reps) < 2:
            continue
        ps = [r["p_safe"] for r in reps]
        ds = [r["decision"] for r in reps]
        cs = [r["confidence"] for r in reps if r["confidence"] is not None]
        rows.append({
            "item_id": item_id,
            "tier": reps[0]["tier"],
            "n": len(reps),
            "p_safe_mean": statistics.fmean(ps),
            "p_safe_spread": max(ps) - min(ps),
            "p_safe_sd": statistics.pstdev(ps) if len(ps) > 1 else 0.0,
            "decision_flips": len(set(ds)) > 1,
            "n_distinct_decisions": len(set(ds)),
            "confidence_spread": (max(cs) - min(cs)) if cs else None,
        })
    return rows


def summarize(rows):
    spreads = [r["p_safe_spread"] for r in rows]
    flips = sum(1 for r in rows if r["decision_flips"])
    by_tier = defaultdict(list)
    for r in rows:
        by_tier[r["tier"]].append(r["p_safe_spread"])
    return {
        "n_items": len(rows),
        "spread_mean": statistics.fmean(spreads),
        "spread_median": statistics.median(spreads),
        "spread_p95": sorted(spreads)[math.ceil(0.95 * len(spreads)) - 1],
        "spread_max": max(spreads),
        "decision_flip_items": flips,
        "decision_flip_rate": flips / len(rows),
        "spread_by_tier": {t: {"mean": statistics.fmean(v), "max": max(v)}
                           for t, v in sorted(by_tier.items())},
    }


def self_test():
    # synthetic: item A stable, item B noisy with a decision flip
    reps = {
        "a": [{"p_safe": 0.90 + i * 0.001, "decision": "allow", "confidence": 0.8,
               "tier": "clearly_safe"} for i in range(10)],
        "b": [{"p_safe": 0.88 if i % 2 else 0.93,
               "decision": "ask" if i % 2 else "allow",
               "confidence": 0.7, "tier": "ambiguous"} for i in range(10)],
    }
    rows = analyze(reps)
    s = summarize(rows)
    assert s["n_items"] == 2
    assert abs(s["decision_flip_rate"] - 0.5) < 1e-9
    assert s["spread_max"] == max(r["p_safe_spread"] for r in rows)
    print("self-test OK:", json.dumps(s, indent=1))


def main():
    args = sys.argv[1:]
    if args and args[0] == "--self-test":
        self_test()
        return
    if not args:
        sys.exit("usage: noise_floor.py results_r1.jsonl results_r2.jsonl ...")
    rows = analyze(load_repeats(args))
    s = summarize(rows)
    print(json.dumps(s, indent=1))
    worst = sorted(rows, key=lambda r: -r["p_safe_spread"])[:10]
    print("\nworst 10 items by spread:")
    for r in worst:
        print(f"  {r['item_id']} ({r['tier']}): spread={r['p_safe_spread']:.3f} "
              f"flips={r['decision_flips']} mean={r['p_safe_mean']:.3f}")


if __name__ == "__main__":
    main()
