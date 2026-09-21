#!/bin/bash
curl -s --max-time 30 "https://api2.openreview.net/notes/search?term=$1&limit=${2:-25}" | python3 -c '
import sys, json, datetime
try:
    d = json.load(sys.stdin)
except Exception as e:
    print("ERR", e); sys.exit()
seen = set()
for n in d.get("notes", []):
    inv = ",".join(n.get("invitations", []))
    if "Submission" not in inv and "Record" not in inv:
        continue
    c = n.get("content", {})
    def g(k):
        v = c.get(k, {})
        return v.get("value") if isinstance(v, dict) else v
    t = g("title") or "?"
    if t in seen: continue
    seen.add(t)
    venue = g("venue") or ""
    pd = n.get("pdate") or n.get("cdate")
    year = datetime.datetime.utcfromtimestamp(pd/1000).year if pd else "?"
    print("-", n.get("id"), "|", year, "|", str(t)[:115], "|", str(venue)[:45])
'
