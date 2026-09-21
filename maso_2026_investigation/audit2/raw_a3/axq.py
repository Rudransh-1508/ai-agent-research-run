import sys, time, urllib.request, urllib.parse, re
def q(query, n=8, fname=None):
    url = "https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(query) + f"&max_results={n}&sortBy=submittedDate&sortOrder=descending"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"research-audit/1.0 (novelty audit)"})
            x = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
            if "<entry>" in x or "<title>" in x:
                break
        except Exception as e:
            x = ""
        time.sleep(6)
    if fname: open(fname,"w").write(x)
    titles = re.findall(r"<title>(.*?)</title>", x, re.S)
    ids = re.findall(r"<id>(.*?)</id>", x)
    pubs = re.findall(r"<published>(.*?)</published>", x)
    print(f"### {query} -> {len(titles)-1} hits")
    for t,i,p in zip(titles[1:], ids[1:], pubs):
        print(p[:10], "|", i.split("/abs/")[-1], "|", " ".join(t.split())[:120])
    print()
queries = [
    ('all:"multi-agent" AND all:"fault tolerance" AND all:LLM', "ax_ft_mas_llm.xml"),
    ('all:"multi-agent" AND all:recovery AND all:"fault injection"', "ax_recovery_fi.xml"),
    ('all:agents AND all:"retry" AND all:"cascading failures"', "ax_retry_cascade.xml"),
    ('all:"self-healing" AND all:"multi-agent" AND all:LLM', "ax_selfheal_mas.xml"),
]
for qy, fn in queries:
    q(qy, fname=fn)
    time.sleep(5)
