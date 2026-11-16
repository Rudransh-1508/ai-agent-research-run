#!/bin/bash
# Certification data for the design gate's Groq judge: score exactly what design/gate.py
# sends (hook rendering), 3 runs on main + 1 on held-out, then resume any failed rows.
cd /Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates
set -a; source ~/.env; set +a
model=openai/gpt-oss-120b; tag=gptoss120b_hook
run() {  # out corpus
  python3 analysis/model_judge.py --render hook --model $model --corpus $2 --out $1 | tail -1
  python3 analysis/model_judge.py --render hook --model $model --corpus $2 --out $1 --resume | tail -1
}
run artifact/judge_groq_${tag}.jsonl benchmark/corpus.jsonl &
run artifact/judge_groq_${tag}_r2.jsonl benchmark/corpus.jsonl &
run artifact/judge_groq_${tag}_r3.jsonl benchmark/corpus.jsonl &
run artifact/judge_groq_${tag}_heldout.jsonl benchmark/corpus_heldout.jsonl &
wait
