import json, warnings
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out as outpath
warnings.filterwarnings("ignore")
from kflat_theory import exclusion_scan

out={}
for n, Kmax in [(3,3),(5,9),(7,15),(9,61)]:
    rows = exclusion_scan(n, Kmax)
    bad = [K for K,v in rows.items() if not v["excluded"]]
    out[n]=dict(rows=rows, not_excluded=bad)
    print(f"n={n}: scanned K=2..{Kmax} (below gamma(Q_n), where Lemma 3' is weaker "
          f"than 2-domination)", flush=True)
    print(f"   NOT excluded by the counting bound: {bad}", flush=True)
    for K in bad:
        v=rows[K]
        print(f"     K={K}: N*D0<= {v['N_D0_upper']}  rhs={v['rhs']}  "
              f"(sphere LB on N*D0 = {v['N_D0_lower']})", flush=True)
    json.dump(out, open(outpath("exclusion_scan.json"),"w", newline="\n"), indent=1, default=float)
