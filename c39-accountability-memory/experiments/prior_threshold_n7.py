"""MILP confirmation of the tilted-prior threshold at n = 7.

`prior_threshold.py` scans K upward from 2, which is fine at n = 3 and n = 5 but
not at n = 7: the weighted K-median MILP is hardest at SMALL K (128 candidate
centres, 16384 assignment variables, and a loose LP relaxation), and the scan
does not reach the interesting region in reasonable time.

It does not need to. That all K below the threshold fail is a combinatorial
fact, not a computational one -- if 2^n - K >= n then every minimum-mass
complement contains 0^n together with at least n-1 of the n weight-one vertices,
so 0^n keeps at most one neighbour in C (this is the lower-bound half of
Corollary 5, checked solver-free in verify_all.py block G). What a solver adds
at n = 7 is an independent confirmation of the TRANSITION, so that is what this
script records: the MILP verdict on a band of K around the claimed threshold.

    python prior_threshold_n7.py     # -> prior_threshold_n7.json
"""
import json, time
from prior_threshold import prior, d0_weighted, best_two_dominating, TOL
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out

N_ = 7
BAND = range(117, 126)
CLAIM = 2 ** N_ - (N_ - 1)          # 122

out = {"n": N_, "claim": CLAIM, "q": {}, "band": [BAND.start, BAND.stop - 1]}
for q in (0.6, 0.7, 0.8):
    pi = prior(N_, q)
    rows = []
    print(f"n={N_} q={q}", flush=True)
    for K in BAND:
        t0 = time.time()
        d0, _, st0 = d0_weighted(N_, pi, K)
        mass, C, st1 = best_two_dominating(N_, pi, K)
        flat = (d0 is not None and mass is not None
                and abs((1.0 - mass) - d0) < TOL)
        rows.append(dict(K=K, D0=d0, best_2dom_cost=None if mass is None else 1 - mass,
                         flat=bool(flat), d0_status=st0, dom_status=st1,
                         seconds=time.time() - t0))
        print(f"  K={K}: D0={d0:.10f}  best 2-dom cost={1-mass:.10f}"
              f"  {'FLAT' if flat else ''}  [{time.time()-t0:.1f}s]", flush=True)
    first = next((r["K"] for r in rows if r["flat"]), None)
    out["q"][str(q)] = dict(rows=rows, first_flat_in_band=first,
                            agrees_with_claim=(first == CLAIM))
    print(f"  => first flat K in band = {first}  "
          f"(claim {CLAIM}: {'AGREE' if first == CLAIM else 'DISAGREE'})\n", flush=True)

json.dump(out, open(out("prior_threshold_n7.json"), "w"), indent=1)
ok = all(v["agrees_with_claim"] for v in out["q"].values())
print("ALL TILTS AGREE WITH 2^n-(n-1) = 122" if ok else "DISAGREEMENT")
raise SystemExit(0 if ok else 1)
