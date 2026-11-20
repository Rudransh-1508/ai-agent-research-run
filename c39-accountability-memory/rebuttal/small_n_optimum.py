"""Exact optimal Nash margin of a K-label record under noisy outcomes, small n (rebuttal, VYMg 3).

mu*(n,K) = max over stochastic encoders q: {0,1}^n -> Delta([K]) of min_i mu_i^N(q), where
mu_i^N = TV(Q[1], Q[(0,1_{-i})]) (Section 4).  TV is attained by a 0/1 payment vector, so

    max t  s.t.  sum_{s,y} Delta_i(s) z_i[y] q[s,y] >= t   for every i,

with z_i in {0,1}^K and Delta_i(s) = P(s | all work) - P(s | i shirks).  The products
w = z q are linearised exactly (z binary, q in [0,1]), giving a MILP.  HiGHS returns a primal
record (lower bound, re-evaluated exactly below) and a dual bound (certified upper bound).

Compared with:
  * the Theorem 2 bound: all margins >= t  =>  t <= sqrt(C ln K / n),  C = (h-l)^2 / (2h(1-h));
  * the best threshold-block record of Proposition 3 that fits in K labels;
  * K*(n,c): least K whose optimum reaches c, against Theorem 3's two sides.

    python small_n_optimum.py [time_limit_seconds]
"""
import itertools, json, math, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from scipy.stats import binom

H_, L_ = 0.9, 0.1
C = (H_ - L_) ** 2 / (2 * H_ * (1 - H_))


def outcome_law(n, shirker=None):
    P = np.empty(1 << n)
    for s in range(1 << n):
        pr = 1.0
        for i in range(n):
            p = L_ if i == shirker else H_
            pr *= p if (s >> i) & 1 else 1 - p
        P[s] = pr
    return P


def nash_margins(q, n):
    Q1 = outcome_law(n) @ q
    return [0.5 * np.abs(Q1 - outcome_law(n, i) @ q).sum() for i in range(n)]


def solve(n, K, time_limit):
    P = 1 << n
    base = outcome_law(n)
    D = [base - outcome_law(n, i) for i in range(n)]
    nq, nz, nw = P * K, n * K, n * P * K
    iq = lambda s, y: s * K + y
    iz = lambda i, y: nq + i * K + y
    iw = lambda i, s, y: nq + nz + (i * P + s) * K + y
    it = nq + nz + nw
    nv = it + 1
    rows, lo, hi = [], [], []
    A = lil_matrix((P + n + 3 * nw + K, nv))
    r = 0
    for s in range(P):                                   # rows of q sum to 1
        for y in range(K):
            A[r, iq(s, y)] = 1
        lo.append(1); hi.append(1); r += 1
    for i in range(n):                                   # margin of agent i >= t
        for s in range(P):
            for y in range(K):
                A[r, iw(i, s, y)] = D[i][s]
        A[r, it] = -1
        lo.append(0); hi.append(np.inf); r += 1
    for i in range(n):                                   # w = z * q, exact for binary z
        for s in range(P):
            for y in range(K):
                w = iw(i, s, y)
                A[r, w] = 1; A[r, iq(s, y)] = -1; lo.append(-np.inf); hi.append(0); r += 1
                A[r, w] = 1; A[r, iz(i, y)] = -1; lo.append(-np.inf); hi.append(0); r += 1
                A[r, w] = 1; A[r, iq(s, y)] = -1; A[r, iz(i, y)] = -1; lo.append(-1); hi.append(np.inf); r += 1
    for y in range(K - 1):                               # label symmetry: agent 0's set first
        A[r, iz(0, y)] = 1; A[r, iz(0, y + 1)] = -1; lo.append(0); hi.append(np.inf); r += 1
    A = A[:r].tocsr()
    c = np.zeros(nv); c[it] = -1
    integrality = np.zeros(nv); integrality[nq:nq + nz] = 1
    lb = np.zeros(nv); ub = np.ones(nv); ub[it] = H_ - L_
    t0 = time.time()
    res = milp(c, constraints=LinearConstraint(A, lo, hi), integrality=integrality,
               bounds=Bounds(lb, ub), options={"time_limit": time_limit, "mip_rel_gap": 1e-6})
    secs = time.time() - t0
    out = {"n": n, "K": K, "seconds": round(secs, 1), "status": res.status, "message": res.message}
    if res.x is not None:
        q = np.clip(res.x[:nq].reshape(P, K), 0, 1); q /= q.sum(1, keepdims=True)
        m = nash_margins(q, n)
        out["primal"] = min(m)                           # re-evaluated exactly, no MILP tolerance
        out["deterministic"] = bool(np.all((q < 1e-6) | (q > 1 - 1e-6)))
    out["dual_bound"] = -res.mip_dual_bound if res.mip_dual_bound is not None else None
    out["optimal"] = res.status == 0
    return out


def pstar(N):                                            # max_k P[Bin(N, h) = k]
    return float(binom.pmf(np.arange(N + 1), N, H_).max())


def best_block_threshold(n, K):
    """Prop. 3(b): one threshold bit per block -> 2^{#blocks} labels; margin set by largest block."""
    b = int(math.floor(math.log2(K)))
    if b < 1:
        return 0.0
    b = min(b, n)
    m = math.ceil(n / b)
    return (H_ - L_) * pstar(m - 1)


def thm2_bound(n, K):
    return min(H_ - L_, math.sqrt(C * math.log(K) / n))


if __name__ == "__main__":
    tl = float(sys.argv[1]) if len(sys.argv) > 1 else 600
    plan = {2: range(2, 5), 3: range(2, 9), 4: range(2, 17), 5: list(range(2, 9)) + [10, 12, 16]}
    results = []
    for n, Ks in plan.items():
        for K in Ks:
            o = solve(n, K, tl)
            o["thm2_bound"] = thm2_bound(n, K)
            o["block_threshold"] = best_block_threshold(n, K)
            results.append(o)
            print(f"n={n} K={K:2d}  opt={o.get('primal', float('nan')):.4f}  "
                  f"dual<={o['dual_bound']:.4f}  {'OPT' if o['optimal'] else 'LIMIT'}  "
                  f"det={o.get('deterministic')}  thm2<={o['thm2_bound']:.4f}  "
                  f"blocks={o['block_threshold']:.4f}  {o['seconds']}s", flush=True)
            json.dump(results, open("small_n_optimum.json", "w"), indent=1)
