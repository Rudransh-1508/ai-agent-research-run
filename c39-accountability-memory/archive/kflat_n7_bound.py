"""
n=7 counting bound only (no code enumeration, no margin search).

The Lemma 3 counting corollary of kflat_structure.py gives a LOWER bound on
K_flat(n) that is a proof, not a search:

    flatness at (n,K) requires   N*D0(K) >= 2(N-K) - nK/2.

At n=7 this is exactly what separates the two surviving scaling hypotheses:
the linear family 2n predicts K_flat(7)=14, the family 2^(n+1)/(n+2) predicts
ceil(256/9)=29. If the bound excludes every K <= 28, linear scaling is FALSE
as a matter of proof, independently of any constructive result.

D0(7,K) is computed by the certified p-median reduction; every row records the
MIP gap, and a row with nonzero gap is reported as inconclusive.
"""
import json, warnings
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out
warnings.filterwarnings("ignore")
import numpy as np
from exp_kflat import solve_D0_pmedian
from kflat_structure import counting_bound

n = 7; N = 2 ** n
rows = {}
Ks = [8, 12, 14, 16, 20, 24, 26, 27, 28, 29, 30, 32]
for K in Ks:
    r = solve_D0_pmedian(n, K, time_limit=900)
    if r["value"] is None or r["gap"] is None or r["gap"] > 1e-9:
        rows[K] = dict(D0=r.get("value"), gap=r.get("gap"),
                       verdict="INCONCLUSIVE (D0 not certified)",
                       seconds=r["seconds"])
        print(f"K={K:3d}: D0 NOT CERTIFIED gap={r.get('gap')} [{r['seconds']}s]", flush=True)
    else:
        D0 = r["D_recomputed"]
        cb = counting_bound(n, K, D0)
        rows[K] = dict(D0=D0, gap=r["gap"], N_D0=cb["lhs_N_D0"], rhs=cb["rhs"],
                       flatness_excluded=cb["flatness_excluded"],
                       seconds=r["seconds"])
        tag = "FLATNESS IMPOSSIBLE" if cb["flatness_excluded"] else "not excluded"
        print(f"K={K:3d}: D0={D0:.6f} gap={r['gap']}  N*D0={cb['lhs_N_D0']:.2f} "
              f"vs rhs={cb['rhs']:.2f}  -> {tag}   [{r['seconds']}s]", flush=True)
    json.dump(rows, open(out("kflat_n7_bound.json"), "w", newline="\n"), indent=1, default=float)

excl = [K for K, v in rows.items() if v.get("flatness_excluded")]
ok = [K for K, v in rows.items() if v.get("flatness_excluded") is False]
print(f"\nexcluded (proved not flat): {sorted(excl)}")
print(f"not excluded              : {sorted(ok)}")
if ok:
    print(f"=> K_flat(7) >= {min(ok)} among the K tested "
          f"(lower bound; the constructive side is untested)")
