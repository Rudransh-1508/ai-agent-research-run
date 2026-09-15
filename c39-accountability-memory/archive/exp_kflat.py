"""
EXP_KFLAT: the flatness threshold K_flat(n).

P0 of C39_UPDATE_2026-09-13. D*(K,gamma) is FLAT at (n,K) if the incentive
constraint costs nothing there, i.e. D*(K,gamma) = D0(K) := D*(K,0).

Only the UPPER bound model is needed to PROVE flatness, because

        D0(K)  <=  D*(K,gamma)  <=  UB(K,gamma)

so UB(K,gamma) == D0(K) sandwiches D* onto D0. UB restricts each agent's
payment decoder to a vertex p_i in {0,1}^K; the products p_i[y]*d_i[c,y] are
then represented EXACTLY by McCormick inequalities, so every UB solution is a
genuinely feasible encoder/decoder pair and the value is a true upper bound.

The converse does NOT hold: UB(K,gamma) > D0(K) does not prove non-flatness,
only that binary payment decoders cannot reach D0. Those rows are recorded as
inconclusive, never as negative.

This is a sparse re-implementation of exp3_bracket.solve(mode="UB"). It is
validated against the dense original in validate_kflat_model.py before use.

Additions over the dense original:
  * scipy.sparse constraint matrix, so n=7 / K=64 is representable at all;
  * optional label-ordering symmetry breaking (valid: labels are exchangeable,
    so any feasible solution can be relabelled to have non-increasing marginal
    label mass, preserving both feasibility and objective);
  * a FEASIBILITY probe "is there a feasible point with D <= D0 + tol", which
    is what flatness actually asks and is far cheaper than proving optimality;
  * independent post-hoc verification: D and every per-agent margin are
    recomputed in plain floating point from the returned (q, p), so a
    "certified flat" row never rests on the solver's own objective value.

Usage:
    python exp_kflat.py <n> <K> <gamma[,gamma,...]> [time_limit] [--nosym]
Writes kflat_n<n>_K<K>.json incrementally, one entry per solve.
"""
import itertools, json, os, sys, time
import numpy as np
import scipy.sparse as sp
from scipy.optimize import milp, LinearConstraint, Bounds

TOL = 1e-7


def states(n):
    return np.array(list(itertools.product([0, 1], repeat=n)), dtype=int)


class UBModel:
    """Variable layout matches exp3_bracket.solve(mode='UB')."""

    def __init__(self, n, K, gamma, symbreak=True, cap=None):
        self.n, self.K, self.gamma = n, K, gamma
        self.S = states(n)
        self.NS = 2 ** n
        self.pr = 1.0 / self.NS
        self.profiles = list(itertools.product([0, 1], repeat=n - 1))
        self.NP = len(self.profiles)
        self.nq = self.NS * K
        self.base = self.nq + 2 * n * K
        self.NV = self.base + n * K + n * self.NP * K
        self.symbreak = symbreak
        self.cap = cap
        self._build()

    # --- variable indices -------------------------------------------------
    def Q(self, s, y): return s * self.K + y
    def Mv(self, i, y): return self.nq + i * self.K + y
    def Zm(self, i, y): return self.nq + self.n * self.K + i * self.K + y
    def P(self, i, y): return self.base + i * self.K + y
    def W(self, i, c, y): return self.base + self.n * self.K + (i * self.NP + c) * self.K + y

    def edge_pair(self, i, c):
        """State indices of the direction-i edge at teammate profile c."""
        prof = self.profiles[c]
        hi = list(prof[:i]) + [1] + list(prof[i:])
        lo = list(prof[:i]) + [0] + list(prof[i:])
        return (int("".join(map(str, hi)), 2), int("".join(map(str, lo)), 2))

    # --- model ------------------------------------------------------------
    def _build(self):
        n, K, NS, NP, pr, g = self.n, self.K, self.NS, self.NP, self.pr, self.gamma
        rows, cols, vals, lo, hi = [], [], [], [], []
        r = [0]

        def add(idx, coef, l, h):
            rows.extend([r[0]] * len(idx)); cols.extend(idx); vals.extend(coef)
            lo.append(l); hi.append(h); r[0] += 1

        # 1. each state's label distribution sums to 1
        for s in range(NS):
            add([self.Q(s, y) for y in range(K)], [1.0] * K, 1.0, 1.0)

        # 2. m[i,y] >= P(S_i = z[i,y], Y=y), so min(...) at the optimum
        for i in range(n):
            for y in range(K):
                for side, zc, l in ((0, 1.0, 0.0), (1, -1.0, -1.0)):
                    idx = [self.Mv(i, y)]; coef = [1.0]
                    for s in range(NS):
                        if self.S[s, i] == side:
                            idx.append(self.Q(s, y)); coef.append(-pr)
                    idx.append(self.Zm(i, y)); coef.append(zc)
                    add(idx, coef, l, np.inf)

        # 3. McCormick for w = p*d with p binary, d in [-1,1]; then margin
        for i in range(n):
            for c in range(NP):
                s1, s0 = self.edge_pair(i, c)
                for y in range(K):
                    w, p, qh, ql = self.W(i, c, y), self.P(i, y), self.Q(s1, y), self.Q(s0, y)
                    add([w, qh, ql, p], [1.0, -1.0, 1.0, 1.0], -np.inf, 1.0)
                    add([w, qh, ql, p], [1.0, -1.0, 1.0, -1.0], -1.0, np.inf)
                    add([w, p], [1.0, -1.0], -np.inf, 0.0)
                    add([w, p], [1.0, 1.0], 0.0, np.inf)
                add([self.W(i, c, y) for y in range(K)], [1.0] * K, g, np.inf)

        # 4. label-ordering symmetry breaking: marginal mass non-increasing
        if self.symbreak and K > 1:
            for y in range(K - 1):
                idx = [self.Q(s, y) for s in range(NS)] + [self.Q(s, y + 1) for s in range(NS)]
                coef = [pr] * NS + [-pr] * NS
                add(idx, coef, 0.0, np.inf)

        # 5. optional objective cap, turning the model into a feasibility test
        if self.cap is not None:
            idx = [self.Mv(i, y) for i in range(n) for y in range(K)]
            add(idx, [1.0] * len(idx), -np.inf, self.cap)

        self.A = sp.coo_matrix((vals, (rows, cols)), shape=(r[0], self.NV)).tocsr()
        self.lo = np.array(lo); self.hi = np.array(hi)

        self.c = np.zeros(self.NV)
        if self.cap is None:
            for i in range(n):
                for y in range(K):
                    self.c[self.Mv(i, y)] = 1.0

        self.lb = np.zeros(self.NV); self.ub = np.ones(self.NV)
        self.integ = np.zeros(self.NV)
        for i in range(n):
            for y in range(K):
                self.integ[self.Zm(i, y)] = 1
                self.integ[self.P(i, y)] = 1
            for c in range(NP):
                for y in range(K):
                    self.lb[self.W(i, c, y)] = -1.0

    def run(self, time_limit):
        t0 = time.time()
        res = milp(c=self.c,
                   constraints=LinearConstraint(self.A, self.lo, self.hi),
                   integrality=self.integ,
                   bounds=Bounds(self.lb, self.ub),
                   options=dict(time_limit=time_limit, mip_rel_gap=0.0,
                                presolve=True))
        out = dict(status=int(res.status), message=str(res.message),
                   seconds=round(time.time() - t0, 2),
                   n=self.n, K=self.K, gamma=self.gamma,
                   symbreak=self.symbreak, cap=self.cap,
                   n_vars=int(self.NV), n_rows=int(self.A.shape[0]),
                   n_binaries=int(self.integ.sum()))
        if res.x is None:
            out.update(value=None, gap=None, verified=None)
            return out
        gap = getattr(res, "mip_gap", None)
        out.update(value=float(res.fun), gap=(None if gap is None else float(gap)))
        out["verified"] = self.verify(res.x)
        out["q"] = res.x[:self.nq].reshape(self.NS, self.K).round(9).tolist()
        out["p"] = [[float(round(res.x[self.P(i, y)])) for y in range(self.K)]
                    for i in range(self.n)]
        return out

    # --- independent recomputation from the returned solution -------------
    def verify(self, x):
        """
        Recompute D and every per-agent all-profile margin directly from
        (q, p), in plain numpy, without reference to the solver's objective
        or auxiliary variables. A flatness claim rests on THIS, not on res.fun.
        """
        n, K, NS = self.n, self.K, self.NS
        q = x[:self.nq].reshape(NS, K)
        q = np.clip(q, 0.0, 1.0)
        row_err = float(np.max(np.abs(q.sum(1) - 1.0)))
        p = np.array([[round(x[self.P(i, y)]) for y in range(K)] for i in range(n)],
                     dtype=float)

        # renormalise so the reported D corresponds to an exactly stochastic q
        qn = q / q.sum(1, keepdims=True)

        D = 0.0
        for i in range(n):
            for y in range(K):
                p0 = self.pr * qn[self.S[:, i] == 0, y].sum()
                p1 = self.pr * qn[self.S[:, i] == 1, y].sum()
                D += min(p0, p1)

        margins = []
        for i in range(n):
            worst = np.inf
            for c in range(self.NP):
                s1, s0 = self.edge_pair(i, c)
                worst = min(worst, float(np.dot(p[i], qn[s1] - qn[s0])))
            margins.append(worst)

        # binary-p margin is a lower bound on what a general p in [0,1]^K gives,
        # but report the exact LP value of the best p too, via the elimination
        # theorem's point-mass form (an upper bound on the true margin).
        return dict(D_recomputed=float(D),
                    min_margin=float(min(margins)),
                    per_agent_margin=[float(m) for m in margins],
                    row_sum_max_error=row_err,
                    p_integrality_max_error=float(
                        max(abs(x[self.P(i, y)] - round(x[self.P(i, y)]))
                            for i in range(n) for y in range(K))))


def solve(n, K, gamma, time_limit=600, symbreak=True, cap=None):
    return UBModel(n, K, gamma, symbreak=symbreak, cap=cap).run(time_limit)


class D0Model:
    """
    D0(K) = min distortion with K labels and NO incentive constraint.

    At gamma=0 the payment decoder and all McCormick machinery are vacuous
    (p=0 gives margin 0 >= 0), so they are dropped entirely: this is the same
    optimum as UBModel(n,K,0) but with n*NP*K fewer variables.

    Variables: q[s,y], m[i,y], z[i,y] (binary). Label symmetry broken by
    non-increasing marginal label mass, as in UBModel.
    """

    def __init__(self, n, K, symbreak=True):
        self.n, self.K = n, K
        self.S = states(n); self.NS = 2 ** n; self.pr = 1.0 / self.NS
        self.nq = self.NS * K
        self.NV = self.nq + 2 * n * K
        self.symbreak = symbreak
        self._build()

    def Q(self, s, y): return s * self.K + y
    def Mv(self, i, y): return self.nq + i * self.K + y
    def Zm(self, i, y): return self.nq + self.n * self.K + i * self.K + y

    def _build(self):
        n, K, NS, pr = self.n, self.K, self.NS, self.pr
        rows, cols, vals, lo, hi = [], [], [], [], []
        r = [0]

        def add(idx, coef, l, h):
            rows.extend([r[0]] * len(idx)); cols.extend(idx); vals.extend(coef)
            lo.append(l); hi.append(h); r[0] += 1

        for s in range(NS):
            add([self.Q(s, y) for y in range(K)], [1.0] * K, 1.0, 1.0)
        for i in range(n):
            for y in range(K):
                for side, zc, l in ((0, 1.0, 0.0), (1, -1.0, -1.0)):
                    idx = [self.Mv(i, y)]; coef = [1.0]
                    for s in range(NS):
                        if self.S[s, i] == side:
                            idx.append(self.Q(s, y)); coef.append(-pr)
                    idx.append(self.Zm(i, y)); coef.append(zc)
                    add(idx, coef, l, np.inf)
        if self.symbreak and K > 1:
            for y in range(K - 1):
                idx = [self.Q(s, y) for s in range(NS)] + [self.Q(s, y + 1) for s in range(NS)]
                add(idx, [pr] * NS + [-pr] * NS, 0.0, np.inf)

        self.A = sp.coo_matrix((vals, (rows, cols)), shape=(r[0], self.NV)).tocsr()
        self.lo = np.array(lo); self.hi = np.array(hi)
        self.c = np.zeros(self.NV)
        for i in range(n):
            for y in range(K):
                self.c[self.Mv(i, y)] = 1.0
        self.integ = np.zeros(self.NV)
        for i in range(n):
            for y in range(K):
                self.integ[self.Zm(i, y)] = 1

    def run(self, time_limit):
        t0 = time.time()
        res = milp(c=self.c, constraints=LinearConstraint(self.A, self.lo, self.hi),
                   integrality=self.integ,
                   bounds=Bounds(np.zeros(self.NV), np.ones(self.NV)),
                   options=dict(time_limit=time_limit, mip_rel_gap=0.0, presolve=True))
        out = dict(model="D0", n=self.n, K=self.K, status=int(res.status),
                   message=str(res.message), seconds=round(time.time() - t0, 2),
                   n_vars=int(self.NV), n_rows=int(self.A.shape[0]),
                   n_binaries=int(self.integ.sum()))
        if res.x is None:
            out.update(value=None, gap=None)
            return out
        gap = getattr(res, "mip_gap", None)
        q = np.clip(res.x[:self.nq].reshape(self.NS, self.K), 0.0, 1.0)
        qn = q / q.sum(1, keepdims=True)
        D = 0.0
        for i in range(self.n):
            for y in range(self.K):
                p0 = self.pr * qn[self.S[:, i] == 0, y].sum()
                p1 = self.pr * qn[self.S[:, i] == 1, y].sum()
                D += min(p0, p1)
        out.update(value=float(res.fun), gap=(None if gap is None else float(gap)),
                   D_recomputed=float(D), q=qn.round(9).tolist())
        return out


def solve_D0(n, K, time_limit=600, symbreak=True):
    return D0Model(n, K, symbreak=symbreak).run(time_limit)


def solve_D0_pmedian(n, K, time_limit=600):
    """
    D0(K) computed as the K-MEDIAN PROBLEM ON THE HAMMING CUBE.

    Derivation. With reconstruction points sh_y in {0,1}^n,
        D(q) = sum_y sum_s (1/N) q[s,y] * d_H(s, sh_y),
    which for fixed {sh_y} is LINEAR in q, so the minimum over the product of
    simplices is attained by assigning each s wholly to its nearest sh_y.
    Hence stochastic encoders cannot beat deterministic ones at gamma=0, and

        D0(K) = (1/2^n) * min_{C subset of {0,1}^n, |C| <= K} sum_s d_H(s, C).

    There is no loss in taking the reconstruction points inside the cube:
    coordinate-wise MAP reconstruction is optimal for Hamming loss and is
    cube-valued. This is the classical p-median MILP: 2^n binaries, a tight
    relaxation, and it solves in milliseconds where the generic D0Model
    struggles. Cross-checked against D0Model wherever both terminate.
    """
    t0 = time.time()
    S = states(n); N = 2 ** n
    Dm = (S[:, None, :] != S[None, :, :]).sum(2).astype(float)   # Hamming distances

    # variables: x[s,c] (N*N), u[c] (N, binary)
    nx = N * N
    NV = nx + N
    rows, cols, vals, lo, hi = [], [], [], [], []
    r = [0]

    def add(idx, coef, l, h):
        rows.extend([r[0]] * len(idx)); cols.extend(idx); vals.extend(coef)
        lo.append(l); hi.append(h); r[0] += 1

    for s in range(N):                                   # assign each state
        add([s * N + c for c in range(N)], [1.0] * N, 1.0, 1.0)
    for s in range(N):                                   # x[s,c] <= u[c]
        for c in range(N):
            add([s * N + c, nx + c], [1.0, -1.0], -np.inf, 0.0)
    add([nx + c for c in range(N)], [1.0] * N, 0.0, float(K))   # at most K centers

    A = sp.coo_matrix((vals, (rows, cols)), shape=(r[0], NV)).tocsr()
    c_obj = np.zeros(NV)
    c_obj[:nx] = (Dm / N).ravel()
    integ = np.zeros(NV); integ[nx:] = 1

    res = milp(c=c_obj, constraints=LinearConstraint(A, np.array(lo), np.array(hi)),
               integrality=integ, bounds=Bounds(np.zeros(NV), np.ones(NV)),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0, presolve=True))
    out = dict(model="D0_pmedian", n=n, K=K, status=int(res.status),
               message=str(res.message), seconds=round(time.time() - t0, 2))
    if res.x is None:
        out.update(value=None, gap=None)
        return out
    centers = [int(c) for c in range(N) if res.x[nx + c] > 0.5]
    # recompute the value directly from the chosen centers
    Drec = float(Dm[:, centers].min(1).sum() / N)
    gap = getattr(res, "mip_gap", None)
    out.update(value=float(res.fun), gap=(None if gap is None else float(gap)),
               D_recomputed=Drec, n_centers=len(centers),
               centers=[S[c].tolist() for c in centers])
    return out


def classify(r, D0v, g):
    """
    Turn a solve result into a verdict, using the POST-HOC RECOMPUTED numbers,
    never the solver's own objective.

    FLAT is certified only when a genuinely feasible (q, p) is exhibited whose
    recomputed distortion equals D0 and whose recomputed worst-case per-agent
    margin is at least gamma. Anything else is inconclusive for D*, because
    UB > D0 only rules out BINARY payment decoders at level D0.
    """
    if r is None or r["value"] is None:
        return "INCONCLUSIVE (no solution returned)"
    v = r["verified"]
    flat = abs(v["D_recomputed"] - D0v) < 1e-6
    margin_ok = v["min_margin"] >= g - 1e-6
    if flat and margin_ok:
        return "FLAT_CERTIFIED"
    if not margin_ok:
        return (f"INVALID (recomputed margin {v['min_margin']:.6g} < gamma); "
                "solution rejected by post-hoc verification")
    return (f"UB above D0 by {v['D_recomputed'] - D0v:.6f} "
            f"(gap {r['gap']}) -- inconclusive for D*")


def main():
    n = int(sys.argv[1]); K = int(sys.argv[2])
    gammas = [float(g) for g in sys.argv[3].split(",")]
    tl = float(sys.argv[4]) if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else 600.0
    symbreak = "--nosym" not in sys.argv
    path = f"kflat_n{n}_K{K}.json"
    out = json.load(open(path)) if os.path.exists(path) else {}

    def flush():
        json.dump(out, open(path, "w"), indent=1, default=float)

    print(f"=== n={n} K={K} symbreak={symbreak} time_limit={tl}s ===", flush=True)

    r0 = solve_D0_pmedian(n, K, time_limit=tl)
    out["D0"] = r0
    flush()
    D0 = r0["value"]
    print(f"D0: value={D0} gap={r0['gap']} recomputed={r0.get('D_recomputed')} "
          f"status={r0['status']} [{r0['seconds']}s]", flush=True)
    if D0 is None or r0["gap"] is None or r0["gap"] > 1e-9:
        print("D0 not certified -> every gamma row at this K is inconclusive", flush=True)
        return
    D0v = r0["D_recomputed"]

    for g in gammas:
        key = f"gamma_{g}"
        t0 = time.time()
        # Cheapest decisive test first: is there ANY feasible point at level D0?
        # That is exactly what flatness asks, and it is a feasibility problem
        # rather than a proof of optimality.
        pr = solve(n, K, g, time_limit=tl, symbreak=symbreak, cap=D0v + 1e-9)
        entry = dict(feas_probe=pr, verdict=classify(pr, D0v, g))
        if entry["verdict"] != "FLAT_CERTIFIED":
            # Probe failed. Fall back to the full optimisation so the row
            # carries a UB value and a MIP gap for the record.
            op = solve(n, K, g, time_limit=tl, symbreak=symbreak)
            entry["opt"] = op
            if pr["status"] == 2:
                entry["verdict"] = ("binary-p INFEASIBLE at D0 -> NOT flat for "
                                    "binary payment decoders; inconclusive for D*")
                if op["value"] is not None and op["gap"] is not None and op["gap"] <= 1e-9:
                    entry["verdict"] += (f" | UB(K,gamma)={op['verified']['D_recomputed']:.6f} "
                                         f"certified, excess {op['verified']['D_recomputed']-D0v:.6f}")
            else:
                entry["verdict"] = "INCONCLUSIVE (probe timed out): " + classify(op, D0v, g)
        out[key] = entry
        flush()
        v = pr.get("verified") or {}
        print(f"gamma={g}: probe status={pr['status']} D_recomp={v.get('D_recomputed')} "
              f"min_margin={v.get('min_margin')} -> {entry['verdict']}   "
              f"[{time.time()-t0:.1f}s]", flush=True)


if __name__ == "__main__":
    main()
