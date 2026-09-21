#!/bin/bash
# B7 Semantic Scholar sweep with long spacing (shared IP is contended).
cd "$(dirname "$0")"
OUT=b7_s2_results.txt
: > "$OUT"

s2q () {
  local label="$1"; local query="$2"
  echo "=== QUERY: $label ===" >> "$OUT"
  for attempt in 1 2 3 4 5 6; do
    curl -s --max-time 30 \
      "https://api.semanticscholar.org/graph/v1/paper/search?query=${query}&limit=10&fields=title,year,venue,externalIds,abstract,citationCount" \
      -o /tmp/b7_s2.json
    if [ -s /tmp/b7_s2.json ] && grep -q '"data"' /tmp/b7_s2.json; then
      python3 - "$OUT" <<'EOF'
import json, sys
out = sys.argv[1]
d = json.load(open('/tmp/b7_s2.json'))
with open(out, 'a') as f:
    for p in d.get('data', []):
        ids = p.get('externalIds') or {}
        f.write(f"{p.get('year')} | {p.get('title')} | {(p.get('venue') or '')[:50]} | arXiv:{ids.get('ArXiv','-')} DOI:{ids.get('DOI','-')} | cites={p.get('citationCount')}\n")
        ab = (p.get('abstract') or '')[:600].replace('\n', ' ')
        if ab:
            f.write(f"    ABS: {ab}\n")
EOF
      break
    fi
    echo "# attempt $attempt 429/fail for $label" >> "$OUT"
    sleep $((attempt * 40))
  done
  sleep 25
}

s2q "blast radius agents" "blast+radius+agent+containment"
s2q "revocation containment agent" "revocation+containment+AI+agent+authority"
s2q "capability attenuation delegation" "capability+attenuation+delegation+token"
s2q "OAuth AI agents" "OAuth+AI+agents+authorization"
s2q "delegation multi-agent authorization LLM" "delegation+authorization+multi-agent+LLM"
s2q "agent identity authentication" "agent+identity+authentication+agentic"
s2q "failure propagation containment LLM" "failure+propagation+containment+LLM+agents"
s2q "cascade containment multi-agent" "cascade+containment+multi-agent+systems"
echo "=== S2 SWEEP DONE ===" >> "$OUT"
