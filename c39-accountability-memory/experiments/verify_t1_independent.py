"""
Independent re-implementation of the T1 (K=2) frontier, written to substitute
for step 2 of the session plan.

STATUS NOTE: the session plan asked for exp1b.py to be validated against
`verify_incentive_distortion.py` and `incentive_distortion_onebit_extension.py`.
Neither file is present in this repo checkout, so that comparison could not be
run as written. This script is a *different* implementation of the same
quantity, deliberately sharing no code with exp1b.py.

Two independent methods are implemented here:

  METHOD A (MILP).  Variables are the monotone-cone residuals
  r(s) = q(s) - gamma*|s| (C39_UPDATE section 1.1), so the incentive constraint
  becomes plain monotonicity of r, a structurally different constraint matrix
  from exp1b's signed edge rows. The objective is the coordinate-wise-MAP
  distortion used by exp3_bracket.py,
        D = sum_{i,y} min( P(S_i=0, Y=y), P(S_i=1, Y=y) ),
  with the 2n minima encoded by 2n binaries. No decoder enumeration at all.

  METHOD B (exhaustive branch enumeration).  Same residual variables, but every
  one of the 4^n min-branch sign patterns is enumerated and solved as an LP.
  Used at n=3 and n=5 only (4^7 LPs is not worth the time).

Agreement of A, B, exp1b.py and the closed form is the validation that step 2
was asking for. It is NOT the same as agreement with the two original scripts,
and is recorded as a substitute.
"""
import itertools, json, time
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out


def all_states(n):
    return np.array(list(itertools.product([0, 1], repeat=n)), dtype=int)


def closed_form(n, gamma):
    S = all_states(n)
    w = S.sum(1)
    M = float(np.mean(np.minimum(w, n - w)))
    return M + n * gamma * ((n - 1) / 2.0 - M), M


def monotone_rows(n):
    """Rows R with R @ r <= 0  <=>  r(s+e_i) >= r(s) for every edge."""
    S = all_states(n)
    idx = {tuple(s): j for j, s in enumerate(S)}
    rows = []
    for i in range(n):
        for rest in itertools.product([0, 1], repeat=n - 1):
            lo = list(rest[:i]) + [0] + list(rest[i:])
            hi = list(rest[:i]) + [1] + list(rest[i:])
            row = np.zeros(2 ** n)
            row[idx[tuple(lo)]] = 1.0
            row[idx[tuple(hi)]] = -1.0
            rows.append(row)
    return np.array(rows)


def _branch_objective(n, gamma, t0, t1, S, w):
    """Linear objective coefficients on r, plus constant, for one min-branch."""
    N = 2 ** n
    c = np.zeros(N)
    const = 0.0
    for i in range(n):
        c[S[:, i] == t1[i]] += 1.0 / N          # P(S_i=t1[i], Y=1) = (1/N) sum q(s)
        c[S[:, i] == t0[i]] -= 1.0 / N          # P(S_i=t0[i], Y=0) = (1/N) sum (1-q(s))
        const += float((S[:, i] == t0[i]).sum()) / N
    const += float(np.dot(c, gamma * w))        # q = gamma*w + r
    return c, const


def solve_enum(n, gamma):
    """METHOD B: exhaustive over all 4^n min-branch sign patterns."""
    S = all_states(n)
    w = S.sum(1).astype(float)
    A = monotone_rows(n)
    b = np.zeros(A.shape[0])
    bounds = [(-gamma * w[s], 1.0 - gamma * w[s]) for s in range(2 ** n)]
    best = np.inf
    for t1 in itertools.product([0, 1], repeat=n):
        for t0 in itertools.product([0, 1], repeat=n):
            c, const = _branch_objective(n, gamma, t0, t1, S, w)
            res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")
            if res.status == 0 and const + res.fun < best - 1e-12:
                best = const + res.fun
    return best


def solve_milp(n, gamma, time_limit=600):
    """
    METHOD A: single MILP, the 2n minima encoded with 2n binaries.

    Variables: r(s) for s in 2^n, then m[i,y], then binaries z[i,y].
    With q = gamma*w + r and label 1 carrying probability q(s):

        P(S_i=b, Y=1) =  cb . r + kb
        P(S_i=b, Y=0) = -cb . r + (1/2 - kb)

    where cb[s] = 1/N on {s_i = b} and kb = (1/N) * sum_{s_i=b} gamma*w_s.
    The pair

        m - P(S_i=0,y) + z >= 0
        m - P(S_i=1,y) - z >= -1

    forces m >= P(S_i=z,y); minimising sum m then drives m to the min. Both
    probabilities lie in [0, 1/2] so a big-M of 1 is valid.
    """
    S = all_states(n)
    N = 2 ** n
    w = S.sum(1).astype(float)
    nr = N
    Mv = lambda i, y: nr + i * 2 + y
    Zv = lambda i, y: nr + 2 * n + i * 2 + y
    NV = nr + 4 * n

    def prob_terms(i, b, y):
        """(coef vector on r, constant) for P(S_i=b, Y=y)."""
        cb = np.zeros(N)
        cb[S[:, i] == b] = 1.0 / N
        kb = float(np.dot(cb, gamma * w))
        if y == 1:
            return cb, kb
        return -cb, 0.5 - kb

    A, lo, hi = [], [], []

    def add(row, l, h):
        A.append(row); lo.append(l); hi.append(h)

    for row in monotone_rows(n):
        full = np.zeros(NV); full[:nr] = row
        add(full, -np.inf, 0.0)

    for i in range(n):
        for y in (0, 1):
            for b, zc, rhs in ((0, 1.0, 0.0), (1, -1.0, -1.0)):
                cb, kb = prob_terms(i, b, y)
                row = np.zeros(NV)
                row[Mv(i, y)] = 1.0
                row[:nr] -= cb
                row[Zv(i, y)] = zc
                add(row, rhs + kb, np.inf)

    c = np.zeros(NV)
    for i in range(n):
        for y in (0, 1):
            c[Mv(i, y)] = 1.0

    lb = np.empty(NV); ub = np.empty(NV)
    lb[:nr] = -gamma * w
    ub[:nr] = 1.0 - gamma * w
    lb[nr:] = 0.0
    ub[nr:] = 1.0
    integ = np.zeros(NV)
    for i in range(n):
        for y in (0, 1):
            integ[Zv(i, y)] = 1

    res = milp(c=c, constraints=LinearConstraint(np.array(A), lo, hi),
               integrality=integ, bounds=Bounds(lb, ub),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0))
    if res.x is None:
        return None, None
    return float(res.fun), float(res.mip_gap)


if __name__ == "__main__":
    import exp1b

    out = {}
    for n in [3, 5, 7, 9]:
        t0 = time.time()
        rows = []
        for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
            g = frac / n
            D_milp, gap = solve_milp(n, g)
            D_exp1b, _, _ = exp1b.solve(n, g)
            D_cf, _ = closed_form(n, g)
            D_enum = solve_enum(n, g) if n <= 5 else None
            rows.append(dict(gamma=g, D_milp=D_milp, mip_gap=gap,
                             D_enum=D_enum, D_exp1b=float(D_exp1b),
                             D_closed_form=float(D_cf),
                             dev_milp_vs_exp1b=float(D_milp - D_exp1b),
                             dev_milp_vs_closed=float(D_milp - D_cf),
                             dev_enum_vs_milp=(None if D_enum is None
                                               else float(D_enum - D_milp))))
            es = "n/a" if D_enum is None else f"{D_enum:.12f}"
            print(f"n={n} gamma={g:.6f}  milpA={D_milp:.12f} (gap {gap:.1e})  "
                  f"enumB={es}  exp1b={D_exp1b:.12f}  closed={D_cf:.12f}  "
                  f"d(A,exp1b)={D_milp-D_exp1b:+.3e}  d(A,cf)={D_milp-D_cf:+.3e}",
                  flush=True)
        out[n] = dict(seconds=time.time() - t0, rows=rows)
        json.dump(out, open(out("verify_t1_independent.json"), "w"), indent=1, default=float)
        print(f"  [n={n} done in {time.time()-t0:.1f}s]\n", flush=True)

    ns = [k for k in out if isinstance(k, int)]
    worst = max(abs(r["dev_milp_vs_exp1b"]) for n in ns for r in out[n]["rows"])
    worst_cf = max(abs(r["dev_milp_vs_closed"]) for n in ns for r in out[n]["rows"])
    worst_enum = max(abs(r["dev_enum_vs_milp"]) for n in ns for r in out[n]["rows"]
                     if r["dev_enum_vs_milp"] is not None)
    print(f"max |A - exp1b|       = {worst:.3e}")
    print(f"max |A - closed form| = {worst_cf:.3e}")
    print(f"max |B - A|           = {worst_enum:.3e}")
    out["max_dev_milp_vs_exp1b"] = worst
    out["max_dev_milp_vs_closed_form"] = worst_cf
    out["max_dev_enum_vs_milp"] = worst_enum
    json.dump(out, open(out("verify_t1_independent.json"), "w"), indent=1, default=float)
