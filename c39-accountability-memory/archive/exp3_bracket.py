"""
EXP3: certified two-sided bracket on D*(K, gamma).

LOWER BOUND (LB_TV): relax the payment-decoder existence condition to its
point-mass case, i.e. require only that every hypercube edge move the
retained label distribution by at least gamma in total variation:
        (1/2) * || q(1,s_-i) - q(0,s_-i) ||_1  >=  gamma.
This is implied by the true condition (take lambda = point mass), so the
resulting MILP value is a valid lower bound on D*(K,gamma).

UPPER BOUND (UB_bin): restrict each agent's payment decoder to the vertices
p_i in {0,1}^K and optimize p jointly with q. Since p is binary the products
p_i[y]*d[y] are represented EXACTLY by McCormick inequalities, so every
solution is genuinely feasible for the original problem, and the value is a
valid upper bound on D*(K,gamma).

If LB_TV == UB_bin the frontier is certified at that (n,K,gamma), and as a
by-product binary payment decoders are certified optimal there.

Distortion uses coordinate-wise MAP reconstruction, which is optimal for
Hamming loss:  D = sum_{i,y} min( P(S_i=0,Y=y), P(S_i=1,Y=y) ).
"""
import itertools, json, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def states(n):
    return np.array(list(itertools.product([0, 1], repeat=n)), dtype=int)

def solve(n, K, gamma, mode, time_limit=240):
    S = states(n); NS = 2 ** n; pr = 1.0 / NS
    profiles = list(itertools.product([0, 1], repeat=n - 1))
    NP = len(profiles)

    nq = NS * K
    Q = lambda s, y: s * K + y
    Mv = lambda i, y: nq + i * K + y
    Zm = lambda i, y: nq + n * K + i * K + y
    base = nq + 2 * n * K
    if mode == "LB":
        # u[i,c,y] = positive part of d ; zu[i,c,y] binary
        U = lambda i, c, y: base + ((i * NP + c) * K + y) * 2
        ZU = lambda i, c, y: base + ((i * NP + c) * K + y) * 2 + 1
        NV = base + n * NP * K * 2
    else:
        # p[i,y] binary ; w[i,c,y] = p[i,y]*d[i,c,y]
        P = lambda i, y: base + i * K + y
        W = lambda i, c, y: base + n * K + (i * NP + c) * K + y
        NV = base + n * K + n * NP * K

    A, lo, hi = [], [], []
    def add(row, l, h): A.append(row); lo.append(l); hi.append(h)

    for s in range(NS):
        r = np.zeros(NV)
        for y in range(K): r[Q(s, y)] = 1.0
        add(r, 1.0, 1.0)

    for i in range(n):
        for y in range(K):
            for side, zc in ((0, 1.0), (1, -1.0)):
                r = np.zeros(NV); r[Mv(i, y)] = 1.0
                for s in range(NS):
                    if S[s, i] == side: r[Q(s, y)] -= pr
                r[Zm(i, y)] = zc
                add(r, 0.0 if side == 0 else -1.0, np.inf)

    def dvec(i, c, y, r, coef):
        p1 = list(profiles[c][:i]) + [1] + list(profiles[c][i:])
        p0 = list(profiles[c][:i]) + [0] + list(profiles[c][i:])
        i1 = int("".join(map(str, p1)), 2); i0 = int("".join(map(str, p0)), 2)
        r[Q(i1, y)] += coef; r[Q(i0, y)] -= coef

    for i in range(n):
        for c in range(NP):
            if mode == "LB":
                for y in range(K):
                    # u >= d ;  u >= 0 ;  u <= d + (1-zu) ;  u <= zu
                    r = np.zeros(NV); r[U(i, c, y)] = 1.0; dvec(i, c, y, r, -1.0)
                    add(r, 0.0, np.inf)
                    r = np.zeros(NV); r[U(i, c, y)] = 1.0; dvec(i, c, y, r, -1.0)
                    r[ZU(i, c, y)] = 1.0; add(r, -np.inf, 1.0)
                    r = np.zeros(NV); r[U(i, c, y)] = 1.0; r[ZU(i, c, y)] = -1.0
                    add(r, -np.inf, 0.0)
                r = np.zeros(NV)
                for y in range(K): r[U(i, c, y)] = 1.0
                add(r, gamma, np.inf)
            else:
                for y in range(K):
                    r = np.zeros(NV); r[W(i, c, y)] = 1.0; dvec(i, c, y, r, -1.0)
                    r[P(i, y)] = 1.0; add(r, -np.inf, 1.0)
                    r = np.zeros(NV); r[W(i, c, y)] = 1.0; dvec(i, c, y, r, -1.0)
                    r[P(i, y)] = -1.0; add(r, -1.0, np.inf)
                    r = np.zeros(NV); r[W(i, c, y)] = 1.0; r[P(i, y)] = -1.0
                    add(r, -np.inf, 0.0)
                    r = np.zeros(NV); r[W(i, c, y)] = 1.0; r[P(i, y)] = 1.0
                    add(r, 0.0, np.inf)
                r = np.zeros(NV)
                for y in range(K): r[W(i, c, y)] = 1.0
                add(r, gamma, np.inf)

    c = np.zeros(NV)
    for i in range(n):
        for y in range(K): c[Mv(i, y)] = 1.0
    integ = np.zeros(NV); lb = np.zeros(NV); ub = np.ones(NV)
    for i in range(n):
        for y in range(K): integ[Zm(i, y)] = 1
    if mode == "LB":
        for i in range(n):
            for cc in range(NP):
                for y in range(K):
                    integ[ZU(i, cc, y)] = 1
    else:
        for i in range(n):
            for y in range(K): integ[P(i, y)] = 1
            for cc in range(NP):
                for y in range(K): lb[W(i, cc, y)] = -1.0

    res = milp(c=c, constraints=LinearConstraint(np.array(A), lo, hi),
               integrality=integ, bounds=Bounds(lb, ub),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0))
    if res.x is None:
        return dict(value=None, status=int(res.status), message=str(res.message))
    return dict(value=float(res.fun), gap=float(res.mip_gap), status=int(res.status),
                q=res.x[:nq].reshape(NS, K).round(9).tolist())

if __name__ == "__main__":
    n = int(sys.argv[1]); out = {}
    for K in [2, 3, 4]:
        for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
            g = frac / n
            t0 = time.time()
            L = solve(n, K, g, "LB"); U = solve(n, K, g, "UB")
            lv, uv = L["value"], U["value"]
            tag = "CERTIFIED" if (lv is not None and uv is not None and abs(uv - lv) < 1e-6) else "open"
            print(f"n={n} K={K} gamma={g:.6f}  LB={lv}  UB={uv}  [{tag}]  {time.time()-t0:.1f}s",
                  flush=True)
            out[f"K{K}_g{frac}"] = dict(gamma=g, LB=L, UB=U, certified=(tag == "CERTIFIED"))
            json.dump(out, open(f"exp3_n{n}.json", "w", newline="\n"), indent=1, default=float)
