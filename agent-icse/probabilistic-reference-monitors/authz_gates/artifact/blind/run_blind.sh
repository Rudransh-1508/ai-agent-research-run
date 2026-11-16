#!/bin/bash
# Score the pre-registered blind attack set (benchmark/corpus_blind.jsonl): frozen designs
# (tag design-freeze-2026-11-17) and the measured gates, each call in both host modes.
set -euo pipefail
cd "$(dirname "$0")/../.."
set -a; source ~/.env; set +a
C=benchmark/corpus_blind.jsonl; O=artifact/blind
export DESIGN_DCG_BIN="$PWD/baselines/dcg/dcg"
run() { python3 faultinject/run_gates_live.py --per-mode --corpus "$C" --out "$O/$1.jsonl" --gates "${@:2}"; }
run gates dcg cc-safety-net jev-guard "jev-engineering(guard)" "jev-engineering(auto)" agentguards
DESIGN_CMD="python3 $PWD/design/gate.py" JEV_MODEL=jev-1.13.0 run design_a_jev design
DESIGN_CMD="python3 $PWD/design/gate.py" DESIGN_JUDGE=groq DESIGN_MODEL=openai/gpt-oss-120b \
  DESIGN_THRESHOLD=0.405 DESIGN_SAMPLES=3 run design_a_groq_k3 design
DESIGN_CMD="python3 $PWD/design/gate_capability.py" run design_b design
