#!/bin/bash
# OpenReview search helper
curl -s --max-time 30 "https://api2.openreview.net/notes/search?term=$1&limit=${2:-10}" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception as e:
    print("ERR", e); sys.exit()
for n in d.get("notes", []):
    c = n.get("content", {})
    def g(k):
        v = c.get(k, {})
        return v.get("value") if isinstance(v, dict) else v
    t = g("title") or "?"
    venue = g("venue") or ""
    year = ""
    import datetime
    pd = n.get("pdate")
    if pd: year = datetime.datetime.utcfromtimestamp(pd/1000).year
    inv = ",".join(n.get("invitations", []))[:60]
    print("-", n.get("id"), "|", year, "|", str(t)[:110], "|", str(venue)[:40], "|", inv)
'
