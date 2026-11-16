#!/usr/bin/env python3
"""Calibration data for the gate's threshold, scored through the gate's own model path.

A certified threshold holds only for the inputs it was certified on. This scores every
definite corpus item exactly as design/gate.py would in deployment: the harness's tool-call
rendering (faultinject/run_gates_live.tool_call), then the gate's own `_model_p_safe` - same
prompt, same client, same judge (DESIGN_JUDGE / DESIGN_MODEL). Only Bash calls reach the
model, so other items are skipped. Output rows feed analysis/threshold_recipe.py and
analysis/judge_validation.py.

  set -a; source ~/.env; set +a
  DESIGN_JUDGE=jev JEV_MODEL=jev-1.13.0 python3 design/certify.py --out artifact/judge_gate_jev.jsonl
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "faultinject"))
import gate  # noqa: E402
from run_gates_live import tool_call  # noqa: E402


def bash_items(corpus):
    items = [json.loads(l) for l in open(corpus)]
    for it in items:
        if it["label"] not in ("safe", "destructive") or it["disputable"]:
            continue
        tool, inp = tool_call(it)
        if tool == "Bash":
            yield it, inp["command"]


def score(it, cmd, attempts):
    p, why = None, None
    for _ in range(attempts):
        p, why = gate._model_p_safe(cmd)  # unbounded: calibration may wait out slow calls
        if p is not None:
            break
    return {"item_id": it["id"], "label": it["label"], "tier": it["tier"],
            "correct_action": it["correct_action"], "disputable": it["disputable"],
            "model": f"gate:{gate.JUDGE}:{gate.MODEL}", "render": "gate", "p_safe": p,
            "outcome": "ok" if p is not None else "malformed", "error": None if p is not None else why}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", default=os.path.join(HERE, "..", "benchmark", "corpus.jsonl"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--attempts", type=int, default=3)
    args = ap.parse_args()
    work = list(bash_items(args.corpus))
    with ThreadPoolExecutor(args.workers) as ex:
        rows = list(ex.map(lambda w: score(*w, args.attempts), work))
    with open(args.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    bad = sum(r["outcome"] != "ok" for r in rows)
    print(f"DONE {len(rows)} scored through {gate.JUDGE}:{gate.MODEL}, {bad} failed")


if __name__ == "__main__":
    main()
