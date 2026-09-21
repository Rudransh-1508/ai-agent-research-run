#!/usr/bin/env python3
"""C3: Semantic Scholar bulk search for Jul-Sep 2026 papers on failure propagation in LLM MAS."""
import urllib.parse, subprocess, json, time, sys, os

OUT = os.path.dirname(os.path.abspath(__file__))
FIELDS = "title,abstract,year,venue,externalIds,publicationDate,authors,citationCount,openAccessPdf"
DATE = "2026-06-01:2026-09-21"

QUERIES = [
    "error cascade LLM multi-agent",
    "cascading failures LLM agents",
    "fault injection LLM agents",
    "failure propagation multi-agent LLM",
    "error propagation multi-agent systems",
    "blast radius agents",
    "agent containment quarantine rollback",
    "organizational multi-agent benchmark LLM",
    "hallucination propagation multi-agent",
    "multi-agent LLM reliability failure",
    "agentic system failure benchmark",
    "multi-agent resilience fault tolerance LLM",
    "error accumulation multi-agent LLM",
    "failure modes LLM multi-agent systems",
    "multi-agent error correction recovery",
]

def fetch(q, retries=3):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search/bulk?query="
           + urllib.parse.quote(q) + f"&publicationDateOrYear={urllib.parse.quote(DATE)}"
           + f"&fields={FIELDS}")
    for attempt in range(retries):
        try:
            r = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", "c3-novelty-hunter/1.0", url],
                               capture_output=True, timeout=90)
            return json.loads(r.stdout)
        except Exception as e:
            wait = 8 * (attempt + 1)
            print(f"  retry {attempt+1}: {e}; sleep {wait}s", file=sys.stderr)
            time.sleep(wait)
    return None

def main():
    all_hits = {}
    for q in QUERIES:
        print(f"[s2] {q}", file=sys.stderr)
        res = fetch(q)
        if not res:
            continue
        for p in res.get("data", []):
            pid = p.get("paperId")
            if not pid:
                continue
            if pid in all_hits:
                all_hits[pid].setdefault("matched", []).append(q)
            else:
                p["matched"] = [q]
                all_hits[pid] = p
        time.sleep(3)
    papers = sorted(all_hits.values(), key=lambda x: x.get("publicationDate") or "", reverse=True)
    with open(os.path.join(OUT, "c3_s2_hits.json"), "w") as f:
        json.dump(papers, f, indent=1)
    print(f"TOTAL UNIQUE S2: {len(papers)}")

if __name__ == "__main__":
    main()
