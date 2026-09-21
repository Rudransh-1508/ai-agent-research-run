#!/bin/bash
# $1 = query (already URL-encoded with + for spaces), $2 = max results, $3 = output label
Q="$1"; N="${2:-15}"
curl -sL --max-time 30 "https://export.arxiv.org/api/query?search_query=${Q}&start=0&max_results=${N}&sortBy=submittedDate&sortOrder=descending" -o tmp_arxiv.xml
python3 -c "
import xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
try:
    t=ET.parse('tmp_arxiv.xml')
    for e in t.getroot().findall('a:entry',ns):
        title=' '.join(e.find('a:title',ns).text.split())
        pub=e.find('a:published',ns).text[:10]
        aid=e.find('a:id',ns).text.replace('http://arxiv.org/abs/','')
        print(pub,'|',title,'|',aid)
except Exception as ex:
    print('PARSE ERROR', ex)
"
