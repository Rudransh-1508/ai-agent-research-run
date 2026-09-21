#!/usr/bin/env python3
"""Batch OpenReview search. Usage: python3 orq.py queries.txt
Each line: <tag>|<search term>. Prints id | title | venue | first 220 chars of abstract."""
import sys, time, subprocess, json, os, urllib.parse

OUT = os.path.dirname(os.path.abspath(__file__))

def run(tag, term, limit=10):
    url = ("https://api2.openreview.net/notes/search?term=" + urllib.parse.quote(term)
           + f"&limit={limit}")
    path = os.path.join(OUT, f"or_{tag}.json")
    r = subprocess.run(['curl', '-s', '-m', '40', url], capture_output=True, timeout=50)
    data = r.stdout
    open(path, 'wb').write(data)
    try:
        d = json.loads(data)
        notes = d.get('notes', [])
        if not notes:
            print(f"[{tag}] (no results)")
        for n in notes:
            c = n.get('content', {})
            def gv(k):
                v = c.get(k)
                if isinstance(v, dict):
                    return v.get('value', '')
                return v or ''
            title = ' '.join(str(gv('title')).split())[:110]
            venue = ' '.join(str(gv('venue')).split())[:60]
            absr = ' '.join(str(gv('abstract')).split())[:200]
            print(f"[{tag}] {n.get('id')} | {title} | {venue} | {absr}")
    except Exception as ex:
        print(f"[{tag}] PARSE ERROR {ex}: {data[:200]}")

if __name__ == '__main__':
    for line in open(sys.argv[1]):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        tag, q = line.split('|', 1)
        run(tag.strip(), q.strip())
        time.sleep(2)
