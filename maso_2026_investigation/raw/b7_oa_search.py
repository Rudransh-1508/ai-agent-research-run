import sys, json, time, urllib.parse, subprocess

def fetch(url):
    for attempt in range(4):
        r = subprocess.run(['curl', '-s', '--max-time', '40', url], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                pass
        time.sleep(6 * (attempt + 1))
    return None

def search(query, per_page=12, from_date="2023-01-01"):
    q = urllib.parse.quote(query)
    url = (f"https://api.openalex.org/works?search={q}"
           f"&filter=from_publication_date:{from_date}"
           f"&per-page={per_page}"
           f"&select=id,title,publication_year,publication_date,doi,primary_location,authorships,cited_by_count")
    data = fetch(url)
    if not data:
        print("# FETCH FAILED")
        return
    for w in data.get('results', []):
        pl = w.get('primary_location') or {}
        src = (pl.get('source') or {}).get('display_name') or ''
        land = pl.get('landing_page_url') or ''
        auths = ', '.join(a['author']['display_name'] for a in (w.get('authorships') or [])[:4])
        print(f"{w.get('publication_date')} | {w.get('title')} | {auths} | {src} | {w.get('doi') or land} | cites={w.get('cited_by_count')}")

if __name__ == '__main__':
    q = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    fd = sys.argv[3] if len(sys.argv) > 3 else "2023-01-01"
    print(f"### QUERY: {q}")
    search(q, n, fd)
    print()
