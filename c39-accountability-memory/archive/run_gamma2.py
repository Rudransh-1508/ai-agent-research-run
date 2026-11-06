import json, warnings, time
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out as outpath
warnings.filterwarnings("ignore")
from kflat_theory import (two_dominating_set, check_two_dominating,
                          verify_flat_construction, exclusion_scan)

out = {}
print("=== A. equivalence check: gamma_2(Q_n) vs the known K_flat(n) ===", flush=True)
for n, known in [(3, 4), (5, 10)]:
    lo_infeas = None
    for K in range(known - 2, known + 1):
        C, info = two_dominating_set(n, K, time_limit=600)
        if C is None:
            print(f"  n={n} K={K}: no 2-dominating set (status {info['status']}) "
                  f"[{info['seconds']}s]", flush=True)
            lo_infeas = K
        else:
            chk = check_two_dominating(n, C)
            v = verify_flat_construction(n, C)
            print(f"  n={n} K={K}: FOUND 2-dom set, min_deg={chk['min_deg_outside']}, "
                  f"internal_edges={chk['internal_edges']} | construction: D={v['D']:.6f} "
                  f"D0={v['D0']:.6f} flat={v['flat']} margin={v['min_margin']:.6f} "
                  f"[{info['seconds']}s]", flush=True)
            out[f"n{n}_K{K}"] = dict(info=info, check=chk, verify=v, centers=C)
            break
    out[f"n{n}_gamma2"] = K
    print(f"  => gamma_2(Q_{n}) = {K}   (known K_flat({n}) = {known})  "
          f"{'MATCH' if K == known else 'MISMATCH'}\n", flush=True)
    json.dump(out, open(outpath("gamma2_results.json"), "w", newline="\n"), indent=1, default=float)
