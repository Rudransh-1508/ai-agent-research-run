#!/bin/bash
Q="$1"; N="${2:-10}"
curl -s --max-time 40 "https://export.arxiv.org/api/query?search_query=${Q}&start=0&max_results=${N}&sortBy=submittedDate&sortOrder=descending" \
| python3 -c '
import sys, re, html
data = sys.stdin.read()
entries = re.findall(r"<entry>(.*?)</entry>", data, re.S)
print("### " + str(len(entries)) + " results")
for e in entries:
    idm = re.search(r"<id>http://arxiv.org/abs/([^<]+)</id>", e)
    tm = re.search(r"<title>(.*?)</title>", e, re.S)
    pm = re.search(r"<published>([^<]+)</published>", e)
    title = html.unescape(re.sub(r"\s+", " ", tm.group(1)).strip()) if tm else "?"
    aid = idm.group(1) if idm else "?"
    pub = pm.group(1)[:10] if pm else "?"
    print("- " + aid + " | " + pub + " | " + title)
'
