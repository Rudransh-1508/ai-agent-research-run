import json, warnings
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out
warnings.filterwarnings("ignore")
from kflat_theory import shell_exclusion_scan, shell_bound
out={}
print("=== sanity: the shell bound must NOT exclude the known flat points ===", flush=True)
for n,K,ND0 in [(3,4,4),(5,10,22),(7,32,96)]:
    fm=shell_bound(n,K)
    print(f"  n={n} K={K}: shell_lower={fm}  N*D0={ND0}  "
          f"-> {'WRONGLY EXCLUDED (BUG)' if fm>ND0 else 'ok, not excluded'}", flush=True)
print()
for n,Kmax in [(3,3),(5,9),(7,31),(9,96)]:
    rows=shell_exclusion_scan(n,Kmax)
    bad=[K for K,v in rows.items() if not v["excluded_shell"]]
    gained=[K for K,v in rows.items() if v["excluded_shell"] and not v["excluded_old"]]
    out[n]=dict(rows=rows,not_excluded=bad,newly_excluded_vs_session1=gained)
    print(f"n={n}: K=2..{Kmax}  not excluded by shell bound: {bad}", flush=True)
    print(f"        newly excluded vs session-1 bound: {gained}", flush=True)
    json.dump(out, open(out("shell_exclusion.json"),"w"), indent=1, default=float)
