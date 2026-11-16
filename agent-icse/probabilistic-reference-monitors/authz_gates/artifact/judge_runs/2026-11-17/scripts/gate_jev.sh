#!/bin/bash
# Re-certify the jev design threshold through the gate's own prompt: 3 main runs + held-out.
cd /Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates
set -a; source ~/.env; set +a
export DESIGN_JUDGE=jev JEV_MODEL=jev-1.13.0
for s in "" _r2 _r3; do
  python3 design/certify.py --out artifact/judge_gate_jev113$s.jsonl
done
python3 design/certify.py --corpus benchmark/corpus_heldout.jsonl --out artifact/judge_gate_jev113_heldout.jsonl
