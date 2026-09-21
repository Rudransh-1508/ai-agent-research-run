#!/usr/bin/env python3
"""Batch arXiv export-API search. Usage: python3 axq.py queries.txt
Each line of queries.txt: <tag>|<arXiv API search_query>
Saves raw XML per tag, prints parsed one-line summaries."""
import sys, time, subprocess, urllib.parse, xml.etree.ElementTree as ET, os

NS = {'a': 'http://www.w3.org/2005/Atom'}
OUT = os.path.dirname(os.path.abspath(__file__))

def run(tag, q, max_results=15):
    url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q)
           + f"&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending")
    path = os.path.join(OUT, f"q_{tag}.xml")
    try:
        r = subprocess.run(['curl', '-sL', '--max-time', '45', url], capture_output=True, timeout=60)
        data = r.stdout
        if not data:
            print(f"[{tag}] FETCH FAIL empty response")
            return
        open(path, 'wb').write(data)
    except Exception as ex:
        print(f"[{tag}] FETCH FAIL {ex}")
        return
    try:
        root = ET.fromstring(data)
        entries = root.findall('a:entry', NS)
        if not entries:
            print(f"[{tag}] (no results)")
        for e in entries:
            title = ' '.join((e.find('a:title', NS).text or '').split())
            pub = e.find('a:published', NS).text[:10]
            aid = e.find('a:id', NS).text.replace('http://arxiv.org/abs/', '')
            print(f"[{tag}] {pub} | {aid} | {title}")
    except Exception as ex:
        print(f"[{tag}] PARSE ERROR {ex}")

if __name__ == '__main__':
    for line in open(sys.argv[1]):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        tag, q = line.split('|', 1)
        run(tag.strip(), q.strip())
        time.sleep(3)
