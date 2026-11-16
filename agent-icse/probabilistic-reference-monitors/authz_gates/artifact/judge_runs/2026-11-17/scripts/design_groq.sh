#!/bin/bash
# Design A with the judge swapped to gpt-oss-120b at its hook-rendered certified threshold.
cd /Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates
set -a; source ~/.env; set +a
export DESIGN_DCG_BIN="$PWD/baselines/dcg/dcg"
export DESIGN_JUDGE=groq DESIGN_MODEL=openai/gpt-oss-120b DESIGN_THRESHOLD=0.405
export DESIGN_CMD="python3 $PWD/design/gate.py"
OUT=artifact/design-groq
[ -e "$OUT" ] && { echo "$OUT exists; refusing to append"; exit 1; }
bash benchmark/run_scorecard.sh "$OUT" design
