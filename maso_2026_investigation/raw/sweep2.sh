#!/bin/bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
OUT=maso_2026_investigation/raw
terms=(
  "trust propagation"
  "error cascade"
  "fault-tolerant LLM agents"
  "agent rollback"
  "orchestrator failure"
  "hierarchical multi-agent"
  "failure taxonomy agents"
  "resilient multi-agent LLM"
  "checkpoint recovery agent"
  "accountability multi-agent"
  "authority delegation agents"
  "Who and When attribution"
  "agentic workflow robustness"
  "memory poisoning agents"
  "human-agent teaming failure"
  "inter-agent communication failure"
)
groups=("ICLR.cc/2026" "ICML.cc/2026" "AAAI.org/2026")
for g in "${groups[@]}"; do
  gsafe=$(echo "$g" | tr './' '__')
  for t in "${terms[@]}"; do
    tsafe=$(echo "$t" | tr ' ' '_')
    f="$OUT/s2_${gsafe}_${tsafe}.json"
    if [ -s "$f" ]; then continue; fi
    enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$t")
    curl -s -A "$UA" "https://api2.openreview.net/notes/search?term=${enc}&group=${g}&limit=25" -o "$f"
    cnt=$(python3 -c "import json;d=json.load(open('$f'));print(d.get('count'))" 2>/dev/null || echo ERR)
    echo "$g | $t -> $cnt"
    sleep 5
  done
done
echo DONE2
