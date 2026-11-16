#!/bin/bash
# Re-ask only the failed rows of each batch-1 run.
cd /Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates
set -a; source ~/.env; set +a
for spec in "openai/gpt-oss-120b gptoss120b" "qwen/qwen3.8-27b qwen3"; do
  set -- $spec; model=$1; tag=$2
  for suffix in _r2 _r3 _heldout; do
    corpus=benchmark/corpus.jsonl
    [ "$suffix" = _heldout ] && corpus=benchmark/corpus_heldout.jsonl
    python3 analysis/model_judge.py --resume --model "$model" --corpus "$corpus" \
      --out artifact/judge_groq_${tag}${suffix}.jsonl | tail -1
  done
done
python3 - <<'EOF'
import json, glob
for f in sorted(glob.glob("artifact/judge_groq_*.jsonl")):
    rows = [json.loads(l) for l in open(f)]
    bad = [r["item_id"] for r in rows if r["outcome"] != "ok"]
    print(f, len(rows), "not ok:", bad)
EOF
