#!/bin/bash
# DataCite helper: dcq.sh "query" rows
Q="$1"; N="${2:-12}"
curl -s --max-time 35 "https://api.datacite.org/dois?query=${Q}&page%5Bsize%5D=${N}" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception as e:
    print("ERR", e); sys.exit()
for it in d.get("data", []):
    a = it["attributes"]
    t = (a.get("titles") or [{}])[0].get("title", "?")
    pub = a.get("publisher", "?")
    y = a.get("publicationYear", "?")
    doi = a.get("doi", "?")
    print("-", y, "|", doi, "|", str(t)[:105], "|", str(pub)[:25])
'
