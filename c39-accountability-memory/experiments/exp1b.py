"""
EXP1b: same exact K=2 computation as exp1, but with the decoder-pair
enumeration reduced to orbit representatives.

Justification: with all-plus orientation, the constraint polytope
{q : q in [0,1], q(s+e_i) - q(s) >= gamma} is invariant under simultaneous
permutation of the n coordinates, and Hamming distortion is too. So the LP
value for decoder pair (a,b) equals that for (pi(a), pi(b)). The orbit of a
pair under S_n is determined by the counts (n00, n01, n10, n11), i.e. by a
composition of n into 4 parts. That is C(n+3,3) representatives instead of 4^n.

This is still an EXACT enumeration, not a sample.
"""
import itertools, json, sys, time
import numpy as np
from scipy.optimize import linprog
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out as outpath

def states(n):
    return np.array(list(itertools.product([0, 1], repeat=n)), dtype=int)

def M_n(n):
    S = states(n); w = S.sum(1)
    return float(np.mean(np.minimum(w, n - w)))

def claimed(n, gamma):
    m = M_n(n)
    return m + n * gamma * ((n - 1) / 2.0 - m)

def edge_rows(n, orient):
    S = states(n)
    idx = {tuple(s): j for j, s in enumerate(S)}
    rows = []
    for i in range(n):
        for rest in itertools.product([0, 1], repeat=n - 1):
            s0 = list(rest[:i]) + [0] + list(rest[i:])
            s1 = list(rest[:i]) + [1] + list(rest[i:])
            r = np.zeros(2 ** n)
            r[idx[tuple(s1)]] = -orient[i]
            r[idx[tuple(s0)]] = orient[i]
            rows.append(r)
    return np.array(rows)

def decoder_reps(n):
    """One (a,b) representative per S_n orbit, via counts (n00,n01,n10,n11)."""
    reps = []
    for n00 in range(n + 1):
        for n01 in range(n + 1 - n00):
            for n10 in range(n + 1 - n00 - n01):
                n11 = n - n00 - n01 - n10
                a = [0]*n00 + [0]*n01 + [1]*n10 + [1]*n11
                b = [0]*n00 + [1]*n01 + [0]*n10 + [1]*n11
                reps.append((np.array(a), np.array(b)))
    return reps

def solve(n, gamma, orient=None, full=False):
    S = states(n); N = 2 ** n; p = 1.0 / N
    orient = orient or [1] * n
    A = edge_rows(n, orient); b = -gamma * np.ones(A.shape[0])
    if full or orient != [1] * n:
        idxs = [(S[i], S[j]) for i in range(N) for j in range(N)]
    else:
        idxs = decoder_reps(n)
    best = (np.inf, None, None)
    for av, bv in idxs:
        ha = (S != av).sum(1).astype(float)
        hb = (S != bv).sum(1).astype(float)
        const = p * ha.sum(); c = p * (hb - ha)
        res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, 1)] * N, method="highs")
        if res.status == 0 and const + res.fun < best[0] - 1e-12:
            best = (const + res.fun, (av.tolist(), bv.tolist()), res.x.copy())
    return best

def conj_q(n, gamma):
    w = states(n).sum(1)
    return gamma * w + (1 - n * gamma) * (w > n / 2.0)

if __name__ == "__main__":
    out = {}
    for n in [3, 5, 7, 9]:
        t0 = time.time(); rows = []
        for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
            g = frac / n
            D, dec, q = solve(n, g)
            cl = claimed(n, g)
            ok = bool(np.allclose(np.sort(q), np.sort(conj_q(n, g)), atol=1e-7))
            rows.append(dict(gamma=g, D_lp=float(D), D_claimed=cl, gap=float(D - cl),
                             q_matches_conjecture=ok, decoder=dec))
            print(f"n={n} gamma={g:.6f}  LP={D:.10f}  claimed={cl:.10f}"
                  f"  gap={D-cl:+.3e}  q=conj:{ok}", flush=True)
        out[n] = dict(M_n=M_n(n), seconds=time.time() - t0, rows=rows)
        json.dump(out, open(outpath("exp1b_results.json"), "w", newline="\n"), indent=1, default=float)
        print(f"  [n={n} done in {time.time()-t0:.1f}s]\n", flush=True)

    # cross-check: orbit reduction vs full enumeration at n=3 and n=5
    print("orbit-vs-full cross-check:")
    for n in [3, 5]:
        for frac in [0.0, 0.5, 1.0]:
            g = frac / n
            a, _, _ = solve(n, g); b2, _, _ = solve(n, g, full=True)
            print(f"  n={n} gamma={g:.4f}  orbit={a:.10f} full={b2:.10f} diff={a-b2:+.2e}", flush=True)

    # orientation invariance at n=3 (all 8 sign patterns, full enumeration)
    print("\norientation invariance n=3 gamma=1/6:")
    vals = []
    for orient in itertools.product([1, -1], repeat=3):
        D, _, _ = solve(3, 1/6, orient=list(orient))
        vals.append(float(D)); print(f"  {orient} -> {D:.10f}", flush=True)
    out["orientation_spread_n3"] = max(vals) - min(vals)
    print("  spread:", max(vals) - min(vals))
    json.dump(out, open(outpath("exp1b_results.json"), "w", newline="\n"), indent=1, default=float)
