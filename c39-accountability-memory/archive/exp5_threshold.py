"""
EXP5: where does the tradeoff vanish?

At n=3 the certified frontier is strictly increasing in gamma for K=2,3 but
completely FLAT for K=4 (D*(4,gamma) = D0 = 0.5 for all gamma up to 0.6).
So the reconstruction-incentive tension is a small-K phenomenon at n=3.

The decisive question is how the threshold K_flat(n) scales:
  * if K_flat ~ 2^(n-1), the tension survives any sub-exponential record and
    C39's significance claim is safe;
  * if K_flat ~ n or 2n, the tension is an artifact of extreme compression and
    the significance claim must be downgraded.

Cheap decisive test: the UPPER bound (binary payment decoders) alone.
UB(K, gamma) == D0(K) proves flatness, since UB is achieved by a genuinely
feasible construction. UB has only 2nK binaries, so it scales much better
than the LB model.
"""
import sys, json, time
from exp3_bracket import solve

n = int(sys.argv[1])
Ks = [int(x) for x in sys.argv[2].split(",")]
gamma = float(sys.argv[3])
tl = float(sys.argv[4]) if len(sys.argv) > 4 else 240
out = {}
for K in Ks:
    t0 = time.time()
    D0 = solve(n, K, 0.0, "UB", time_limit=tl)
    Dg = solve(n, K, gamma, "UB", time_limit=tl)
    d0, dg = D0["value"], Dg["value"]
    if d0 is None or dg is None:
        verdict = "inconclusive (timeout/infeasible)"
    elif abs(dg - d0) < 1e-6:
        verdict = "FLAT (no tradeoff)"
    else:
        verdict = f"tradeoff, excess = {dg - d0:.6f}"
    print(f"n={n} K={K:3d} gamma={gamma}  D0={d0}  D(gamma)={dg}  -> {verdict}"
          f"   [{time.time()-t0:.1f}s, gaps {D0.get('gap')},{Dg.get('gap')}]", flush=True)
    out[K] = dict(D0=d0, Dg=dg, verdict=verdict)
    json.dump(out, open(f"exp5_n{n}.json", "w", newline="\n"), indent=1, default=float)
