#!/usr/bin/env python3
"""C3 novelty hunter: arXiv 90-day sweep (Jun 21 - Sep 21 2026, with margin from Jun 1)."""
import urllib.parse, xml.etree.ElementTree as ET
import subprocess, time, json, sys, os

NS = {"a": "http://www.w3.org/2005/Atom"}
OUT = os.path.dirname(os.path.abspath(__file__))
DATE_RANGE = "submittedDate:[202606010000 TO 202609212359]"

QUERIES = [
    ("error_cascade_agent",      'all:"error cascade" AND all:"agent"'),
    ("cascading_failure_llm",    'all:"cascading failure" AND all:"LLM"'),
    ("cascading_failures_agent", 'all:"cascading failures" AND all:"agent"'),
    ("fault_injection_llm",      'all:"fault injection" AND all:"LLM"'),
    ("fault_injection_agent",    'all:"fault injection" AND all:"agent"'),
    ("failure_propagation_ma",   'all:"failure propagation" AND all:"multi-agent"'),
    ("failure_propagation_llm",  'all:"failure propagation" AND all:"LLM"'),
    ("error_propagation_ma_llm", 'all:"error propagation" AND all:"multi-agent" AND all:"LLM"'),
    ("blast_radius",             'all:"blast radius"'),
    ("containment_agent_llm",    'all:"containment" AND all:"agent" AND all:"LLM"'),
    ("quarantine_agent",         'all:"quarantine" AND all:"agent"'),
    ("rollback_agent_llm",       'all:"rollback" AND all:"agent" AND all:"LLM"'),
    ("org_benchmark_ma",         'all:"organizational" AND all:"multi-agent" AND all:"benchmark"'),
    ("hallucination_cascade",    'all:"hallucination cascade"'),
    ("hallucination_propagation",'all:"hallucination propagation"'),
    ("ma_reliability_llm",       'all:"multi-agent" AND all:"reliability" AND all:"LLM"'),
    ("agentic_failure_bench",    'all:"agentic" AND all:"failure" AND all:"benchmark"'),
    ("resilience_ma_llm",        'all:"resilience" AND all:"multi-agent" AND all:"LLM"'),
    ("fault_tolerance_llm_ag",   'all:"fault tolerance" AND all:"LLM" AND all:"agent"'),
    ("error_accumulation_ma",    'all:"error accumulation" AND all:"multi-agent"'),
    ("failure_modes_ma_llm",     'all:"failure modes" AND all:"multi-agent" AND all:"LLM"'),
    ("agent_failure_benchmark",  'all:"agent failure" AND all:"benchmark"'),
    ("systemic_failure_agents",  'all:"systemic failure" AND all:"agents"'),
    ("error_cascade_llm",        'all:"error cascades" AND all:"LLM"'),
    ("multi_agent_robustness",   'all:"multi-agent" AND all:"robustness" AND all:"LLM" AND all:"failure"'),
    ("agent_recovery_llm",       'all:"recovery" AND all:"multi-agent" AND all:"LLM" AND all:"failure"'),
    ("propagation_llm_agents",   'all:"propagation" AND all:"LLM agents" AND all:"errors"'),
    ("correction_multi_agent",   'all:"multi-agent" AND all:"LLM" AND all:"error correction"'),
]

def fetch(q, retries=4):
    full = f"{q} AND {DATE_RANGE}"
    url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(full)
           + "&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending")
    for attempt in range(retries):
        try:
            r = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", "c3-novelty-hunter/1.0", url],
                               capture_output=True, timeout=90)
            data = r.stdout
            if len(data) < 200:
                raise RuntimeError(f"suspiciously short response ({len(data)} bytes): {r.stderr.decode()[:200]}")
            return data
        except Exception as e:
            wait = 5 * (attempt + 1)
            print(f"  retry {attempt+1} after error: {e}; sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
    return None

def parse(data):
    root = ET.fromstring(data)
    out = []
    for e in root.findall("a:entry", NS):
        aid = e.find("a:id", NS).text.strip()
        arxiv_id = aid.rsplit("/abs/", 1)[-1]
        title = " ".join(e.find("a:title", NS).text.split())
        published = e.find("a:published", NS).text[:10]
        updated = e.find("a:updated", NS).text[:10]
        authors = [a.find("a:name", NS).text for a in e.findall("a:author", NS)]
        summary = " ".join(e.find("a:summary", NS).text.split())
        cats = [c.get("term") for c in e.findall("a:category", NS)]
        out.append({"arxiv_id": arxiv_id, "title": title, "published": published,
                    "updated": updated, "authors": authors, "abstract": summary, "categories": cats})
    return out

def main():
    all_hits = {}
    by_query = {}
    for name, q in QUERIES:
        print(f"[{name}] {q}", file=sys.stderr)
        data = fetch(q)
        if data is None:
            by_query[name] = "FETCH_FAILED"
            continue
        with open(os.path.join(OUT, f"c3_{name}.xml"), "wb") as f:
            f.write(data)
        try:
            hits = parse(data)
        except Exception as ex:
            by_query[name] = f"PARSE_FAILED: {ex}"
            continue
        by_query[name] = len(hits)
        for h in hits:
            h.setdefault("matched_queries", []).append(name)
            if h["arxiv_id"] in all_hits:
                all_hits[h["arxiv_id"]]["matched_queries"] += [name]
            else:
                all_hits[h["arxiv_id"]] = h
        print(f"  -> {len(hits)} hits", file=sys.stderr)
        time.sleep(4)
    with open(os.path.join(OUT, "c3_all_hits.json"), "w") as f:
        json.dump({"by_query": by_query, "papers": sorted(all_hits.values(),
                   key=lambda x: x["published"], reverse=True)}, f, indent=1)
    print(json.dumps(by_query, indent=1))
    print(f"TOTAL UNIQUE: {len(all_hits)}")

if __name__ == "__main__":
    main()
