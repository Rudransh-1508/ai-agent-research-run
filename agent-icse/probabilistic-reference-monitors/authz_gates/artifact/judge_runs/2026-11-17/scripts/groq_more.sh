#!/bin/bash
# More Groq judges, same protocol as gpt-oss-120b / qwen3: 3 main runs + held-out, then resume.
cd /Users/rudranshrathore/research-gap-agentic/agent-icse/probabilistic-reference-monitors/authz_gates
set -a; source ~/.env; set +a
LOG=/private/tmp/claude-501/-Users-rudranshrathore-research-gap-agentic/8b8960b8-47eb-48cd-82be-205cd59771ed/scratchpad/logs
run() {  # model tag suffix corpus
  out=artifact/judge_groq_$2$3.jsonl
  python3 analysis/model_judge.py --model $1 --max-tokens 1024 --corpus $4 --out $out > $LOG/$2$3.log 2>&1
  python3 analysis/model_judge.py --model $1 --max-tokens 1024 --corpus $4 --out $out --resume >> $LOG/$2$3.log 2>&1
}
for spec in "openai/gpt-oss-20b gptoss20b" "openai/gpt-oss-safeguard-20b safeguard20b" "allam-2-7b allam7b"; do
  set -- $spec
  run $1 $2 "" benchmark/corpus.jsonl &
  run $1 $2 _r2 benchmark/corpus.jsonl &
  run $1 $2 _r3 benchmark/corpus.jsonl &
  run $1 $2 _heldout benchmark/corpus_heldout.jsonl &
done
wait
python3 - <<'EOF'
import json, glob
for f in sorted(glob.glob("artifact/judge_groq_*.jsonl")):
    rows = [json.loads(l) for l in open(f)]
    print(f, len(rows), "not ok:", [r["item_id"] for r in rows if r["outcome"] != "ok"][:8])
EOF
