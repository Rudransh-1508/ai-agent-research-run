#!/bin/bash
# Crossref helper: crq.sh "query" rows [from-date]
Q="$1"; N="${2:-8}"; F="${3:-2024-01-01}"
curl -s --max-time 30 "https://api.crossref.org/works?query.bibliographic=${Q}&rows=${N}&select=title,DOI,published,container-title&filter=from-pub-date:${F}" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception as e:
    print("ERR", e); sys.exit()
for it in d["message"]["items"]:
    t = (it.get("title") or ["?"])[0]
    ct = (it.get("container-title") or ["?"])[0]
    y = it.get("published",{}).get("date-parts",[["?"]])[0][0]
    print("-", y, "|", it.get("DOI"), "|", t[:100], "|", ct[:40])
'
