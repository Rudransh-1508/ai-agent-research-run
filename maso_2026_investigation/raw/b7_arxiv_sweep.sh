#!/bin/bash
# B7 arXiv API sweep with generous spacing to dodge shared-IP 429s.
cd "$(dirname "$0")"
OUT=b7_arxiv_results.txt
: > "$OUT"

run_q () {
  local label="$1"; local query="$2"; local n="${3:-12}"
  echo "=== QUERY: $label ===" >> "$OUT"
  for attempt in 1 2 3 4 5; do
    curl -sL --max-time 50 \
      "https://export.arxiv.org/api/query?search_query=${query}&start=0&max_results=${n}&sortBy=submittedDate&sortOrder=descending" \
      -o /tmp/b7_q.xml
    if [ -s /tmp/b7_q.xml ] && grep -q "<feed" /tmp/b7_q.xml; then
      python3 - "$OUT" <<'EOF'
import sys, xml.etree.ElementTree as ET
out = sys.argv[1]
ns = {'a': 'http://www.w3.org/2005/Atom'}
try:
    root = ET.parse('/tmp/b7_q.xml').getroot()
except Exception as e:
    print(f"# parse error: {e}", file=sys.stderr); sys.exit(1)
entries = root.findall('a:entry', ns)
with open(out, 'a') as f:
    if not entries:
        f.write("# no results\n")
    for e in entries:
        title = ' '.join((e.find('a:title', ns).text or '').split())
        pub = e.find('a:published', ns).text[:10]
        aid = e.find('a:id', ns).text.replace('http://arxiv.org/abs/', '')
        auths = ', '.join(a.find('a:name', ns).text for a in e.findall('a:author', ns)[:4])
        f.write(f"{pub} | {title} | {aid} | {auths}\n")
EOF
      break
    fi
    echo "# attempt $attempt failed/429 for $label; sleeping" >> "$OUT"
    sleep $((attempt * 25))
  done
  sleep 12
}

run_q "confused deputy + agent" "all:%22confused%20deputy%22%20AND%20all:%22agent%22" 15
run_q "OAuth + AI agent" "all:%22OAuth%22%20AND%20all:%22AI%20agent%22" 15
run_q "agent identity + authorization" "all:%22agent%20identity%22%20AND%20all:%22authorization%22" 15
run_q "delegation token + LLM agent" "all:%22delegation%22%20AND%20all:%22token%22%20AND%20all:%22LLM%22" 15
run_q "blast radius + agent" "all:%22blast%20radius%22%20AND%20all:%22agent%22" 15
run_q "failure propagation + multi-agent LLM" "all:%22failure%20propagation%22%20AND%20all:%22multi-agent%22" 15
run_q "least privilege + LLM agent" "all:%22least%20privilege%22%20AND%20all:%22agent%22" 15
run_q "revocation + AI agent" "all:%22revocation%22%20AND%20all:%22AI%20agent%22" 15
run_q "capability + delegation + LLM" "all:%22capability%22%20AND%20all:%22delegation%22%20AND%20all:%22LLM%22" 15
run_q "MCP authorization security" "all:%22model%20context%20protocol%22%20AND%20all:%22authorization%22" 15
run_q "agentic authorization" "all:%22agentic%22%20AND%20all:%22authorization%22" 15
run_q "error cascade + LLM agents" "all:%22error%20cascade%22%20AND%20all:%22agent%22" 10
run_q "containment + prompt injection + agent" "all:%22containment%22%20AND%20all:%22prompt%20injection%22" 12
run_q "privilege control + LLM agent" "all:%22privilege%22%20AND%20all:%22LLM%20agent%22%20AND%20all:%22control%22" 12
echo "=== SWEEP DONE ===" >> "$OUT"
