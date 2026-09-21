#!/bin/bash
# OpenReview 2026 keyword sweep: ICLR 2026, ICML 2026, AAAI 2026
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
OUT=maso_2026_investigation/raw
terms=(
  "multi-agent failure"
  "failure propagation"
  "cascading failure"
  "fault injection"
  "blast radius"
  "agent recovery"
  "fault tolerance multi-agent"
  "multi-agent robustness"
  "error propagation multi-agent"
  "delegation multi-agent"
  "organizational agents"
  "multi-agent reliability"
  "agent fault"
  "failure containment"
  "multi-agent hallucination"
  "agent error recovery"
)
groups=("ICLR.cc/2026" "ICML.cc/2026" "AAAI.org/2026")
for g in "${groups[@]}"; do
  gsafe=$(echo "$g" | tr './' '__')
  for t in "${terms[@]}"; do
    tsafe=$(echo "$t" | tr ' ' '_')
    f="$OUT/search_${gsafe}_${tsafe}.json"
    if [ -s "$f" ]; then continue; fi
    enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$t")
    curl -s -A "$UA" "https://api2.openreview.net/notes/search?term=${enc}&group=${g}&limit=25" -o "$f"
    cnt=$(python3 -c "import json;d=json.load(open('$f'));print(d.get('count'))" 2>/dev/null || echo ERR)
    echo "$g | $t -> $cnt"
    sleep 5
  done
done
echo DONE
