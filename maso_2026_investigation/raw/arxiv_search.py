import sys, urllib.parse, urllib.request, xml.etree.ElementTree as ET, time

def search(query, max_results=15, sort='submittedDate'):
    q = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/api/query?search_query={q}&start=0&max_results={max_results}&sortBy={sort}&sortOrder=descending"
    req = urllib.request.Request(url, headers={'User-Agent':'research-bot/1.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    ns={'a':'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(data)
    out=[]
    for e in root.findall('a:entry',ns):
        title=' '.join(e.find('a:title',ns).text.split())
        pub=e.find('a:published',ns).text[:10]
        aid=e.find('a:id',ns).text.replace('http://arxiv.org/abs/','')
        out.append((pub,title,aid))
    return out

if __name__=='__main__':
    q=sys.argv[1]
    n=int(sys.argv[2]) if len(sys.argv)>2 else 15
    for pub,title,aid in search(q,n):
        print(pub,'|',title,'|',aid)
