"""K_flat under a general full-support prior.

The margin condition (M) is an ALL-teammate-profile condition, so it does not
mention the prior at all. Only D and D_0 do. That makes the threshold question
well posed for any full-support prior pi, and the two lemmas of Section 5 give

    K_flat(pi) = min { K : some pi-optimal K-median set of size K is
                           2-dominating }.

Necessity is Lemma 3' (prior-free: it is about an edge derivative vanishing,
plus the fact that attaining D_0 forces each profile's mass onto its nearest
centres, true for any full-support prior). Sufficiency is the Lemma-2
construction: a 2-dominating C is dominating, so the construction costs
1 - pi(C), and that equals D_0(K) exactly when C is pi-optimal.

For the uniform prior every dominating K-set is optimal, so the condition
collapses to "a 2-dominating set of size K exists" and K_flat = gamma_2(Q_n).

This script computes both sides for product Bernoulli(q) priors:

    D0(K)      -- weighted K-median, MILP
    best2d(K)  -- max pi(C) over 2-dominating C with |C| = K, MILP

and reports the least K with 1 - best2d(K) == D0(K).

    python prior_threshold.py            # n = 3,5 over a grid of q
    python prior_threshold.py 7          # add n = 7 (slower)
"""
import json, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out

TOL = 1e-9


def popcount(x):
    return bin(x).count("1")


def prior(n, q):
    """Product Bernoulli(q): P(S_i = 1) = q, independent across agents."""
    return np.array([q ** popcount(s) * (1 - q) ** (n - popcount(s))
                     for s in range(1 << n)])


def d0_general(weights, cost, K, time_limit=600):
    """min over K centres of sum_x weights[x] * min_{t in C} cost[x][t].

    The plain weighted K-median is the case cost[x][t] = d_H(x,t). Under an
    observation channel the record is a function of the OBSERVATION x while the
    loss is still measured against the true profile, which is exactly the same
    program with cost[x][t] = sum_s P(s|x) d_H(s,t).
    """
    M = len(weights)
    nv = M + M * M
    c = np.zeros(nv)
    for x in range(M):
        for t in range(M):
            c[M + x * M + t] = weights[x] * cost[x][t]
    A = lil_matrix((M + M * M + 1, nv))
    lo, hi, r = [], [], 0
    for x in range(M):
        for t in range(M):
            A[r, M + x * M + t] = 1.0
        lo.append(1.0); hi.append(1.0); r += 1
    for x in range(M):
        for t in range(M):
            A[r, M + x * M + t] = 1.0
            A[r, t] = -1.0
            lo.append(-np.inf); hi.append(0.0); r += 1
    for t in range(M):
        A[r, t] = 1.0
    lo.append(float(K)); hi.append(float(K)); r += 1
    integrality = np.zeros(nv); integrality[:M] = 1
    res = milp(c=c, constraints=LinearConstraint(A[:r].tocsc(), lo, hi),
               integrality=integrality, bounds=Bounds(np.zeros(nv), np.ones(nv)),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0))
    if res.x is None:
        return None, None, res.status
    return float(res.fun), sorted(t for t in range(M) if res.x[t] > 0.5), res.status


def d0_weighted(n, pi, K, time_limit=600):
    """Weighted K-median over the cube: min_C sum_s pi[s] d(s, C), |C| = K."""
    N = 1 << n
    # variables: y_c (N binaries), then x[s,c] (N*N continuous in [0,1])
    nv = N + N * N
    c = np.zeros(nv)
    for s in range(N):
        for t in range(N):
            c[N + s * N + t] = pi[s] * popcount(s ^ t)
    rows, lo, hi = [], [], []
    A = lil_matrix((N + N * N + 1, nv))
    r = 0
    for s in range(N):                        # sum_t x[s,t] = 1
        for t in range(N):
            A[r, N + s * N + t] = 1.0
        lo.append(1.0); hi.append(1.0); r += 1
    for s in range(N):                        # x[s,t] <= y_t
        for t in range(N):
            A[r, N + s * N + t] = 1.0
            A[r, t] = -1.0
            lo.append(-np.inf); hi.append(0.0); r += 1
    for t in range(N):                        # sum_t y_t = K
        A[r, t] = 1.0
    lo.append(float(K)); hi.append(float(K)); r += 1
    A = A[:r].tocsc()
    integrality = np.zeros(nv); integrality[:N] = 1
    res = milp(c=c, constraints=LinearConstraint(A, lo, hi),
               integrality=integrality, bounds=Bounds(np.zeros(nv), np.ones(nv)),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0))
    if res.x is None:
        return None, None, res.status
    C = sorted(t for t in range(N) if res.x[t] > 0.5)
    return float(res.fun), C, res.status


def best_two_dominating(n, pi, K, time_limit=600):
    """max pi(C) over 2-dominating C with |C| = K. Returns (mass, C, status)."""
    N = 1 << n
    A = lil_matrix((N + 1, N))
    lo, hi = [], []
    for v in range(N):                        # sum_{u ~ v} y_u + 2 y_v >= 2
        for i in range(n):
            A[v, v ^ (1 << i)] += 1.0
        A[v, v] += 2.0
        lo.append(2.0); hi.append(np.inf)
    for t in range(N):
        A[N, t] = 1.0
    lo.append(float(K)); hi.append(float(K))
    res = milp(c=-pi, constraints=LinearConstraint(A.tocsc(), lo, hi),
               integrality=np.ones(N), bounds=Bounds(np.zeros(N), np.ones(N)),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0))
    if res.x is None:
        return None, None, res.status
    C = sorted(t for t in range(N) if res.x[t] > 0.5)
    return float(-res.fun), C, res.status


def k_flat(n, q, kmax=None, verbose=True):
    N = 1 << n
    pi = prior(n, q)
    kmax = kmax or N
    rows = []
    for K in range(2, kmax + 1):
        d0, _, st0 = d0_weighted(n, pi, K)
        mass, C, st1 = best_two_dominating(n, pi, K)
        if d0 is None:
            rows.append(dict(K=K, note="D0 unsolved", status=st0)); continue
        if mass is None:                      # no 2-dominating set of this size
            rows.append(dict(K=K, D0=d0, feasible_2dom=False)); continue
        flat = abs((1.0 - mass) - d0) < TOL
        rows.append(dict(K=K, D0=d0, best_2dom_cost=1.0 - mass,
                         feasible_2dom=True, flat=bool(flat),
                         centres=C if flat else None))
        if verbose:
            print(f"    K={K:3d}  D0={d0:.8f}  best 2-dom cost={1-mass:.8f}"
                  f"   {'FLAT' if flat else ''}", flush=True)
        if flat:
            return K, rows
    return None, rows


if __name__ == "__main__":
    extra = [int(a) for a in sys.argv[1:]]
    out = {}
    for n in [3, 5] + extra:
        out[str(n)] = {}
        for q in (0.5, 0.55, 0.6, 0.7, 0.8, 0.9):
            t0 = time.time()
            print(f"n={n}  q={q}", flush=True)
            K, rows = k_flat(n, q)
            out[str(n)][str(q)] = dict(K_flat=K, seconds=time.time() - t0,
                                       rows=rows)
            print(f"  => K_flat(n={n}, Bernoulli({q})) = {K}"
                  f"   [{time.time()-t0:.1f}s]\n", flush=True)
            json.dump(out, open(out("prior_threshold.json"), "w"), indent=1)
    print("\nsummary")
    print("   n |  " + " | ".join(f"q={q}" for q in
                                  (0.5, 0.55, 0.6, 0.7, 0.8, 0.9)))
    for n in out:
        print(f"  {n:>2} |  " + " | ".join(
            f"{out[n][q]['K_flat']!s:>4}" for q in out[n]))
