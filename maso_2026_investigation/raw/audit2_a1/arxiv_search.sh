#!/bin/bash
# Batch arXiv search helper. Usage: arxiv_search.sh "query" "label" [max_results]
# Appends parsed results to results.txt
Q="$1"; LABEL="$2"; MAX="${3:-15}"
OUT="maso_2026_investigation/raw/audit2_a1/results.txt"
ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$Q")
echo "=== QUERY [$LABEL]: $Q ===" >> "$OUT"
curl -sL -m 30 "https://export.arxiv.org/api/query?search_query=$ENC&max_results=$MAX&sortBy=submittedDate&sortOrder=descending" \
 | python3 -c "
import sys, re
data = sys.stdin.read()
entries = re.findall(r'<entry>(.*?)</entry>', data, re.S)
for e in entries:
    idm = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', e)
    tm = re.search(r'<title>(.*?)</title>', e, re.S)
    pm = re.search(r'<published>(.*?)</published>', e)
    if idm and tm:
        title = re.sub(r'\s+', ' ', tm.group(1)).strip()
        print(f'{idm.group(1)} | {pm.group(1)[:10] if pm else \"?\"} | {title}')
" >> "$OUT"
echo "" >> "$OUT"
sleep 45
