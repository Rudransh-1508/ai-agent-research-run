"""The frontier at intermediate K, where the paper currently has only endpoints.

Theorem 5 gives D*(2,gamma) exactly; Theorem 9 gives the K at which the tradeoff
vanishes. Between them the paper says nothing numerical, and that is where most
real records live. This sweeps K = 2..K_flat at small n.

What is computed, precisely, because it is not the exact D* for K > 2:

  * For a FIXED centre set C and FIXED payment vectors p, both the objective and
    the margin constraints are linear in the encoder q, so the problem is an LP.
  * The joint problem over (q, p) is bilinear, so we alternate: solve the LP for
    q, then re-solve for the best p at that q via Theorem 3, and repeat from
    several starts.
  * That yields an ACHIEVABILITY curve -- an upper bound on D*(K,gamma) -- since
    every point corresponds to a record that actually exists.

Two anchors check it. At gamma = 0 the curve must equal D_0(K), and at K = 2 it
must equal the closed form of Theorem 5. Both are asserted, not hoped for.

    python frontier_sweep.py        # -> frontier_sweep.json
"""
import json, math, sys, time
from itertools import combinations
import numpy as np
from scipy.optimize import linprog

from experiment_agents import popcount, prior, distortion, margin
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out

RNG = np.random.default_rng(20260915)
STARTS = 6


def d0_uniform(n, K):
    """min over K centres of the uniform-prior K-median value."""
    N = 1 << n
    best = math.inf
    for C in combinations(range(N), K):
        v = sum(min(popcount(s ^ c) for c in C) for s in range(N)) / N
        best = min(best, v)
    return best


def edges(n, i):
    """(s0, s1) pairs differing only in coordinate i."""
    out = []
    for sm in range(1 << (n - 1)):
        lo = sm & ((1 << i) - 1)
        hi = (sm >> i) << (i + 1)
        s0 = lo | hi
        out.append((s0, s0 | (1 << i)))
    return out


def lp_for_q(n, K, C, P, gamma):
    """min D over q, with centres C and payment vectors P fixed. LP."""
    N = 1 << n
    nv = N * K
    c = np.array([popcount(s ^ C[y]) / N for s in range(N) for y in range(K)])
    A_eq = np.zeros((N, nv))
    for s in range(N):
        A_eq[s, s * K:(s + 1) * K] = 1.0
    rows, rhs = [], []
    for i in range(n):
        for s0, s1 in edges(n, i):
            r = np.zeros(nv)
            for y in range(K):
                r[s1 * K + y] -= P[i][y]
                r[s0 * K + y] += P[i][y]
            rows.append(r); rhs.append(-gamma)       # -<p,d> <= -gamma
    res = linprog(c, A_ub=np.array(rows) if rows else None,
                  b_ub=np.array(rhs) if rows else None,
                  A_eq=A_eq, b_eq=np.ones(N), bounds=[(0, 1)] * nv,
                  method="highs")
    if not res.success:
        return None, None
    return float(res.fun), res.x.reshape(N, K)


def best_p(n, q, gamma):
    """Given q, the payment that maximises the worst-case margin (Theorem 3)."""
    N, K = q.shape
    P = []
    for i in range(n):
        A = np.array([q[s1] - q[s0] for s0, s1 in edges(n, i)])
        T = A.shape[0]
        # max t s.t. A p >= t, 0 <= p <= 1
        c = np.zeros(K + 1); c[-1] = -1.0
        A_ub = np.hstack([-A, np.ones((T, 1))])
        res = linprog(c, A_ub=A_ub, b_ub=np.zeros(T),
                      bounds=[(0, 1)] * K + [(None, None)], method="highs")
        P.append(res.x[:K] if res.success else np.zeros(K))
    return P


def frontier_point(n, K, gamma):
    """Alternate LP(q) and best-p until it stops improving; keep the best start."""
    N = 1 << n
    best = math.inf
    for C in combinations(range(N), K):
        # Start from the paper's own construction -- pay agent i the
        # reconstructed i-th bit -- then random restarts. Purely random binary
        # starts miss the aligned-orientation case and badly overestimate.
        seeded = [np.array([float((C[y] >> i) & 1) for y in range(K)])
                  for i in range(n)]
        starts = [seeded] + [[RNG.integers(0, 2, size=K).astype(float)
                              for _ in range(n)] for _ in range(STARTS)]
        for P in starts:
            val = math.inf
            for _ in range(8):
                v, q = lp_for_q(n, K, C, P, gamma)
                if v is None:
                    break
                if v > val - 1e-12:
                    val = min(val, v)
                    break
                val = v
                P = best_p(n, q, gamma)
            best = min(best, val)
    return best


if __name__ == "__main__":
    out = {}
    for n in (3,):
        M = sum(math.comb(n, k) * min(k, n - k) for k in range(n + 1)) / 2 ** n
        kflat = {3: 4, 5: 10}[n]
        out[str(n)] = {"M_n": M, "K_flat": kflat, "curves": {}}
        for K in range(2, kflat + 1):
            d0 = d0_uniform(n, K)
            gmax = 1.0 / n if K == 2 else 1.0
            # do NOT round: rounding 2/3 up to 0.666667 makes the exact
            # margin 1 - 1/d_min infeasible by 3e-7 and looks like a cliff
            gs = [j * gmax / 6 for j in range(7)]
            row = []
            t0 = time.time()
            for g in gs:
                v = frontier_point(n, K, g)
                row.append(dict(gamma=g, D=None if v == math.inf else v,
                                feasible=v != math.inf))
            out[str(n)]["curves"][str(K)] = dict(D0=d0, points=row,
                                                 seconds=time.time() - t0)
            shown = " ".join("inf" if r["D"] is None else f"{r['D']:.4f}" for r in row)
            print(f"n={n} K={K:2d}  D0={d0:.4f}  D(gamma) = {shown}"
                  f"  [{time.time()-t0:.1f}s]", flush=True)
            # anchor 1: gamma = 0 must reproduce D_0(K)
            assert abs(row[0]["D"] - d0) < 1e-6, (K, row[0]["D"], d0)
            # anchor 2: at K = 2 the curve must reproduce Theorem 5
            if K == 2:
                for r in row:
                    closed = M + n * r["gamma"] * ((n - 1) / 2 - M)
                    assert abs(r["D"] - closed) < 1e-6, (r["gamma"], r["D"], closed)
            json.dump(out, open(out("frontier_sweep.json"), "w"), indent=1)
    print("\nanchors hold: gamma=0 reproduces D_0(K), and K=2 reproduces Theorem 5")
    print("wrote frontier_sweep.json")
