"""
Destroy-and-repair search for a smaller 2-dominating set of Q_9.

The algebraic code has no internal edges, so deleting any single centre leaves
it with zero centre-neighbours and single-deletion local search cannot move.
This version removes a random BLOCK, greedily repairs 2-domination, then
shrinks. Every candidate is re-verified from scratch.
"""
import json, random, warnings, time
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out
warnings.filterwarnings("ignore")
from kflat_theory import check_two_dominating, verify_flat_construction
from linear_2dom import linear_2dom_code

n = 9; N = 2 ** n
nb = [[v ^ (1 << i) for i in range(n)] for v in range(N)]

def deficient(C):
    return [v for v in range(N) if v not in C and sum(1 for w in nb[v] if w in C) < 2]

def repair(C, rng):
    while True:
        d = deficient(C)
        if not d:
            return C
        v = rng.choice(d)
        # add the neighbour that fixes the most deficiencies
        best, bestgain = None, -1
        for w in nb[v] + [v]:
            if w in C:
                continue
            gain = 0
            for u in [w] + nb[w]:
                if u not in C and u != w and sum(1 for z in nb[u] if z in C) < 2:
                    gain += 1
            if gain > bestgain:
                best, bestgain = w, gain
        C.add(best if best is not None else v)

def shrink(C, rng):
    improved = True
    while improved:
        improved = False
        order = list(C); rng.shuffle(order)
        for c in order:
            C.discard(c)
            good = sum(1 for w in nb[c] if w in C) >= 2
            if good:
                for t in nb[c]:
                    if t not in C and sum(1 for w in nb[t] if w in C) < 2:
                        good = False; break
            if good: improved = True
            else: C.add(c)
    return C

C0, _ = linear_2dom_code(n)
best = set(C0)
rng = random.Random(7)
t0 = time.time(); trial = 0
while time.time() - t0 < 600:
    trial += 1
    C = set(best)
    k = rng.randint(5, 40)
    for _ in range(k):
        if C: C.discard(rng.choice(list(C)))
    C = repair(C, rng); C = shrink(C, rng)
    if not deficient(C) and len(C) < len(best):
        best = C
        print(f"  trial {trial}: |C|={len(best)}  [{time.time()-t0:.0f}s]", flush=True)

Cs = sorted(best)
chk = check_two_dominating(n, Cs); v = verify_flat_construction(n, Cs)
print(f"\nBEST |C|={len(Cs)} 2-dom={chk['is_2_dominating']} min_deg={chk['min_deg_outside']} "
      f"internal_edges={chk['internal_edges']} | D={v['D']:.8f} D0={v['D0']:.8f} "
      f"FLAT={v['flat']} margin={v['min_margin']:.6f}  (trials={trial})")
json.dump(dict(size=len(Cs), check=chk, verify=v, centers=Cs, trials=trial),
          open(out("n9_destroy_repair.json"),"w"), indent=1, default=float)
