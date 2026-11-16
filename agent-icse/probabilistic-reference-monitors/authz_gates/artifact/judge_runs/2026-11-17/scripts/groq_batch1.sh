#!/bin/bash
# Held-out scoring + two main-corpus repeats for both Groq judges, run in parallel.
cd /Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates
set -a; source ~/.env; set +a
LOG=/private/tmp/claude-501/-Users-rudranshrathore-research-gap-agentic/8b8960b8-47eb-48cd-82be-205cd59771ed/scratchpad/logs
mkdir -p "$LOG"
for pair in "openai/gpt-oss-120b gptoss120b" "qwen/qwen3.8-27b qwen3"; do
  set -- $pair; model=$1; tag=$2
  python3 analysis/model_judge.py --model "$model" --corpus benchmark/corpus_heldout.jsonl \
    --out artifact/judge_groq_${tag}_heldout.jsonl > "$LOG/${tag}_heldout.log" 2>&1 &
  for r in 2 3; do
    python3 analysis/model_judge.py --model "$model" \
      --out artifact/judge_groq_${tag}_r$r.jsonl > "$LOG/${tag}_r$r.log" 2>&1 &
  done
done
wait
tail -n 2 "$LOG"/*.log
