"""
Closing the small-K gap left by the counting bound.

Lemma 3' says every non-centre must have >= 2 NEAREST centres. A weaker but
solver-friendly consequence, valid for ANY C:

    every vertex adjacent to C but not in C has >= 2 neighbours in C.

(For such a vertex the nearest-centre distance is exactly 1, so "nearest
centres" and "neighbours in C" coincide.) Vertices far from C are left
unconstrained, which is what makes this usable below gamma(Q_n) where the
counting bound dies.

MILP: u[v] = v in C, z[v] = v is adjacent to C.
    z[v] >= u[w]                 for each w ~ v
    z[v] <= sum_{w~v} u[w]
    sum_{w~v} u[w] >= 2(z[v] - u[v])
Infeasible at |C| = K  =>  flatness at (n,K) is impossible.
"""
import time
import numpy as np
import scipy.sparse as sp
from scipy.optimize import milp, LinearConstraint, Bounds
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out


def local_2dom_feasible(n, K, time_limit=600):
    N = 2 ** n
    nb = [[v ^ (1 << i) for i in range(n)] for v in range(N)]
    U = lambda v: v
    Z = lambda v: N + v
    NV = 2 * N
    rows, cols, vals, lo, hi = [], [], [], [], []
    r = [0]

    def add(idx, coef, l, h):
        rows.extend([r[0]] * len(idx)); cols.extend(idx); vals.extend(coef)
        lo.append(l); hi.append(h); r[0] += 1

    for v in range(N):
        for w in nb[v]:
            add([Z(v), U(w)], [1.0, -1.0], 0.0, np.inf)        # z >= u[w]
        add([Z(v)] + [U(w) for w in nb[v]], [1.0] + [-1.0] * n, -np.inf, 0.0)
        add([U(w) for w in nb[v]] + [Z(v), U(v)],
            [1.0] * n + [-2.0, 2.0], 0.0, np.inf)              # >= 2(z-u)
    add([U(v) for v in range(N)], [1.0] * N, float(K), float(K))

    A = sp.coo_matrix((vals, (rows, cols)), shape=(r[0], NV)).tocsr()
    t0 = time.time()
    res = milp(c=np.zeros(NV),
               constraints=LinearConstraint(A, np.array(lo), np.array(hi)),
               integrality=np.ones(NV), bounds=Bounds(np.zeros(NV), np.ones(NV)),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0, presolve=True))
    secs = round(time.time() - t0, 2)
    if res.x is None:
        return None, dict(status=int(res.status), seconds=secs,
                          proved_infeasible=bool(res.status == 2))
    C = sorted(int(v) for v in range(N) if res.x[U(v)] > 0.5)
    return C, dict(status=int(res.status), seconds=secs, proved_infeasible=False)


if __name__ == "__main__":
    import json, warnings
    warnings.filterwarnings("ignore")
    out = {}
    for n, Ks in [(7, range(2, 6)), (9, range(2, 14))]:
        out[n] = {}
        for K in Ks:
            C, info = local_2dom_feasible(n, K, time_limit=600)
            if C is None and info["proved_infeasible"]:
                verdict = "EXCLUDED (no C satisfies the local condition)"
            elif C is None:
                verdict = f"UNRESOLVED (status {info['status']})"
            else:
                verdict = "not excluded (a local-condition C exists)"
            out[n][K] = dict(verdict=verdict, **info)
            print(f"n={n} K={K}: {verdict}  [{info['seconds']}s]", flush=True)
            json.dump(out, open(out("local2dom.json"), "w"), indent=1, default=float)
