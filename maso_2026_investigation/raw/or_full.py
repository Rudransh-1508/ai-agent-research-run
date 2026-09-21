import json, subprocess, sys, time
def search_full(term, limit=4, retries=4):
    url=f"https://api2.openreview.net/notes/search?term={term.replace(' ','%20')}&limit={limit}"
    for i in range(retries):
        r=subprocess.run(['curl','-s','--max-time','30',url],capture_output=True,text=True)
        try:
            d=json.loads(r.stdout)
            break
        except Exception:
            time.sleep(25)
    else:
        print('FAILED', term); return
    for n in d.get('notes',[]):
        c=n.get('content',{})
        def g(k):
            v=c.get(k,{})
            return v.get('value') if isinstance(v,dict) else v
        t=g('title')
        if not t: continue
        print('TITLE:',t)
        print('AUTHORS:',str(g('authors'))[:180])
        print('VENUE:',g('venue'))
        print('ABS:',str(g('abstract'))[:1100])
        print('======')
if __name__=='__main__':
    search_full(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 4)
