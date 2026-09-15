import sys, json, warnings
warnings.filterwarnings("ignore")
from kflat_theory import two_dominating_set, check_two_dominating, verify_flat_construction
K = int(sys.argv[1]); tl = float(sys.argv[2])
C, info = two_dominating_set(9, K, time_limit=tl)
res = dict(K=K, info=info)
if C is None:
    print(f"K={K}: {'INFEASIBLE (proved)' if info['status']==2 else 'unresolved status '+str(info['status'])}  [{info['seconds']}s]", flush=True)
    res["feasible"] = False
else:
    chk = check_two_dominating(9, C)
    v = verify_flat_construction(9, C)
    print(f"K={K}: FOUND. min_deg={chk['min_deg_outside']} internal_edges={chk['internal_edges']} "
          f"| D={v['D']:.8f} D0={v['D0']:.8f} FLAT={v['flat']} margin={v['min_margin']:.6f}  [{info['seconds']}s]", flush=True)
    res.update(feasible=True, check=chk, verify=v, centers=C)
json.dump(res, open(f"n9_K{K}.json","w"), indent=1, default=float)
