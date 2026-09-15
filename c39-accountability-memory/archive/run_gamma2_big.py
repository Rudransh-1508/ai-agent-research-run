import json, warnings, time
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out
warnings.filterwarnings("ignore")
from kflat_theory import (two_dominating_set, check_two_dominating,
                          verify_flat_construction, exclusion_scan)

out = json.load(open(data("gamma2_results.json"))) if __import__("os").path.exists("gamma2_results.json") else {}

def run(n, lo, hi, tl):
    print(f"=== n={n}: searching gamma_2(Q_{n}) over K={lo}..{hi} ===", flush=True)
    res = {}
    for K in range(lo, hi + 1):
        C, info = two_dominating_set(n, K, time_limit=tl)
        if C is None:
            tag = ("INFEASIBLE (proved)" if info["status"] == 2
                   else f"unresolved (status {info['status']})")
            print(f"  K={K}: {tag}  [{info['seconds']}s]", flush=True)
            res[K] = dict(feasible=False, **info)
            if info["status"] != 2:
                break
        else:
            chk = check_two_dominating(n, C)
            v = verify_flat_construction(n, C)
            print(f"  K={K}: FOUND. min_deg={chk['min_deg_outside']} "
                  f"internal_edges={chk['internal_edges']} outside={chk['n_outside']} "
                  f"| D={v['D']:.8f} D0={v['D0']:.8f} FLAT={v['flat']} "
                  f"margin={v['min_margin']:.6f}  [{info['seconds']}s]", flush=True)
            res[K] = dict(feasible=True, check=chk, verify=v, centers=C, **info)
            out[f"n{n}_gamma2"] = K
            out[f"n{n}_detail"] = res
            json.dump(out, open(out("gamma2_results.json"), "w"), indent=1, default=float)
            return K
        out[f"n{n}_detail"] = res
        json.dump(out, open(out("gamma2_results.json"), "w"), indent=1, default=float)
    return None

for n, lo, hi, tl in [(7, 28, 34, 900), (9, 92, 100, 1800)]:
    t0 = time.time()
    g = run(n, lo, hi, tl)
    print(f"  => gamma_2(Q_{n}) = {g}   [{time.time()-t0:.1f}s total]\n", flush=True)
json.dump(out, open(out("gamma2_results.json"), "w"), indent=1, default=float)
