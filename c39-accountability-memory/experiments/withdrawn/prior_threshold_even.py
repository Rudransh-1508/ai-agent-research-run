"""Corollary 12 at even n, and the strict-decrease hypothesis of Lemma 7.

Two hypotheses were audited on 2026-09-15 and neither had evidence behind it:

  * Corollary 12 was stated for odd n, but its proof never uses parity. If the
    restriction is real the corollary is under-stated; if not, the hypothesis is
    spurious and should go. This settles it by MILP at n = 4 and n = 6.

  * Lemma 7 assumes D_0 is strictly decreasing at K, so that the K centres are
    distinct. Nothing in the paper checked that. This records the check.

    python prior_threshold_even.py     # -> prior_threshold_even.json
"""
import json, time
from prior_threshold import prior, d0_weighted, best_two_dominating, TOL
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out as outpath

out = {"claim": "K_flat = 2^n - (n-1) for a tilted product prior, any n >= 3",
       "even_n": {}, "strict_decrease": {}}

for n in (4, 6):
    pred = 2 ** n - (n - 1)
    pi = prior(n, 0.7)
    rows, first = [], None
    print(f"n={n}  prediction 2^n-(n-1) = {pred}", flush=True)
    for K in range(pred - 3, pred + 2):
        t0 = time.time()
        d0, _, _ = d0_weighted(n, pi, K)
        mass, _, _ = best_two_dominating(n, pi, K)
        flat = mass is not None and abs((1 - mass) - d0) < TOL
        if flat and first is None:
            first = K
        rows.append(dict(K=K, D0=d0, best_2dom_cost=None if mass is None else 1 - mass,
                         flat=bool(flat), seconds=time.time() - t0))
        print(f"   K={K}: D0={d0:.8f}  best 2-dom={1-mass:.8f}"
              f"  {'FLAT' if flat else ''}", flush=True)
    out["even_n"][str(n)] = dict(rows=rows, first_flat=first, prediction=pred,
                                 agrees=(first == pred))
    print(f"   => first flat K = {first}  ({'MATCHES' if first == pred else 'DIFFERS'})\n",
          flush=True)

# Lemma 7's hypothesis, by complete enumeration where that is possible
for n in (3, 4):
    N = 1 << n
    pi = prior(n, 0.5)
    vals = [d0_weighted(n, pi, K)[0] for K in range(1, N + 1)]
    ties = [K + 1 for K, (a, b) in enumerate(zip(vals, vals[1:]), start=1)
            if not b < a - 1e-12]
    out["strict_decrease"][str(n)] = dict(values=vals, strictly_decreasing=not ties,
                                          ties_at=ties)
    print(f"D_0 strictly decreasing at n={n} over K=1..{N}: {not ties}"
          + (f"  ties at {ties}" if ties else ""), flush=True)

json.dump(out, open(outpath("prior_threshold_even.json"), "w", newline="\n"), indent=1)
ok = all(v["agrees"] for v in out["even_n"].values()) and \
     all(v["strictly_decreasing"] for v in out["strict_decrease"].values())
print("\n" + ("BOTH HYPOTHESES SETTLED: parity is not needed, D_0 is strictly decreasing"
              if ok else "A HYPOTHESIS CHECK FAILED"))
raise SystemExit(0 if ok else 1)
