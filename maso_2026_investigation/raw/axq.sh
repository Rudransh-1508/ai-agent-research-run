#!/bin/bash
curl -sL --max-time 40 "https://export.arxiv.org/api/query?search_query=$1&start=0&max_results=${2:-12}&sortBy=${3:-submittedDate}&sortOrder=descending" -o ax_tmp.xml
python3 -c "
import xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
try:
    t=ET.parse('ax_tmp.xml')
    entries=t.getroot().findall('a:entry',ns)
    if not entries: print('(no results)')
    for e in entries:
        title=' '.join(e.find('a:title',ns).text.split())
        pub=e.find('a:published',ns).text[:10]
        aid=e.find('a:id',ns).text.replace('http://arxiv.org/abs/','')
        print(pub,'|',title,'|',aid)
except Exception as ex:
    print('PARSE ERROR', ex)
"
