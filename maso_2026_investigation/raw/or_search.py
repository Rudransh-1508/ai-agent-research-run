import json, subprocess, sys, time
def search(term, limit=15):
    url=f"https://api2.openreview.net/notes/search?term={term.replace(' ','%20')}&limit={limit}"
    r=subprocess.run(['curl','-s','--max-time','30',url],capture_output=True,text=True)
    try:
        d=json.loads(r.stdout)
    except Exception:
        print('ERR', r.stdout[:200]); return
    for n in d.get('notes',[]):
        c=n.get('content',{})
        def g(k):
            v=c.get(k,{})
            return v.get('value') if isinstance(v,dict) else v
        t=g('title')
        if not t: continue
        venue=g('venue') or ''
        print(f"{t} | {venue} | forum:{n.get('forum')}")
if __name__=='__main__':
    search(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 15)
