"""
Upper bound on gamma_2(Q_9) by direct local search (no MILP).

Start from the verified algebraic 2-dominating code (size 128) and shrink it:
repeatedly delete a centre whose deletion keeps the set 2-dominating, with
random tie-breaking and restarts. Every reported set is re-verified from
scratch by check_two_dominating and by the solver-free flat-construction
check, so a search bug cannot produce a false upper bound.
"""
import json, random, warnings, time
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out
warnings.filterwarnings("ignore")
import numpy as np
from kflat_theory import check_two_dominating, verify_flat_construction
from linear_2dom import linear_2dom_code

n = 9
N = 2 ** n
nb = [[v ^ (1 << i) for i in range(n)] for v in range(N)]


def ok(Cset):
    for v in range(N):
        if v not in Cset:
            if sum(1 for w in nb[v] if w in Cset) < 2:
                return False
    return True


def shrink(Cset, rng):
    C = set(Cset)
    improved = True
    while improved:
        improved = False
        order = list(C)
        rng.shuffle(order)
        for c in order:
            C.discard(c)
            # only c and its neighbours can break
            good = sum(1 for w in nb[c] if w in C) >= 2
            if good:
                for t in nb[c]:
                    if t not in C and sum(1 for w in nb[t] if w in C) < 2:
                        good = False
                        break
            if good:
                improved = True
            else:
                C.add(c)
    return C


C0, meta = linear_2dom_code(n)
best = set(C0)
print(f"start: |C|={len(best)} (verified algebraic code)", flush=True)
rng = random.Random(12345)
t0 = time.time()
trial = 0
while time.time() - t0 < 420:
    trial += 1
    C = set(best)
    # perturb: add a few random vertices then shrink
    for _ in range(rng.randint(1, 12)):
        C.add(rng.randrange(N))
    C = shrink(C, rng)
    if ok(C) and len(C) < len(best):
        best = C
        print(f"  trial {trial}: improved to |C|={len(best)}  [{time.time()-t0:.0f}s]", flush=True)

Cs = sorted(best)
chk = check_two_dominating(n, Cs)
v = verify_flat_construction(n, Cs)
print(f"\nBEST |C|={len(Cs)}  2-dominating={chk['is_2_dominating']} "
      f"min_deg={chk['min_deg_outside']} internal_edges={chk['internal_edges']}")
print(f"construction check: D={v['D']:.8f} D0={v['D0']:.8f} FLAT={v['flat']} "
      f"margin={v['min_margin']:.6f}")
json.dump(dict(size=len(Cs), check=chk, verify=v, centers=Cs, trials=trial),
          open(out("n9_localsearch.json"), "w", newline="\n"), indent=1, default=float)
