"""
EXP_KFLAT (structural): K_flat(n) by reduction to the Hamming-cube K-median
problem, instead of a monolithic MILP over (q, p).

------------------------------------------------------------------------
LEMMA 1 (support restriction).  Let q be any stochastic encoder with
D(q) = D0(K), and let sh_y be the coordinate-wise MAP reconstruction of label
y. Then

    D(q) = sum_{s,y} (1/N) q[s,y] d_H(s, sh_y)
         >= sum_s (1/N) min_y d_H(s, sh_y)
         >= sum_s (1/N) d_H(s, C)          where C = {sh_y}
         >= D0(K)          since |C| <= K.

Equality forces (a) C is an optimal K-median code, and (b) q[s,y] > 0 only
when d_H(s, sh_y) = d_H(s, C), i.e. every state may only use labels whose
reconstruction point is one of its NEAREST centers.

LEMMA 2 (distinct centers).  If D0 is strictly decreasing at K, the K centers
in Lemma 1 are pairwise distinct. Otherwise the distinct set C' has |C'| = K'
< K and D0(K') <= sum_s d(s,C')/N = D0(K) <= D0(K'), so D0(K') = D0(K),
contradicting strict decrease. (Checked numerically for every K used.)

LEMMA 3 (flatness necessary condition).  Assume Lemmas 1-2. For a center c,
d(c,C) = 0 and c is the unique nearest center, so q[c] is a POINT MASS on c's
label. If a state t adjacent to c has c as its ONLY center at distance 1, then
q[t] is a point mass on the same label, so for the edge (c,t) in direction i

    d_i = q[t] - q[c] = 0,

and <p_i, d_i> = 0 < gamma for EVERY p_i in [0,1]^K. So flatness fails.

Therefore flatness at (n,K) requires:
    every state at distance exactly 1 from C has at least TWO centers at
    distance 1.

This is a statement about arbitrary bounded payment decoders, not just binary
ones, so it yields genuine NON-flatness, not merely a failure of the UB model.

COUNTING COROLLARY.  Let e be the number of hypercube edges inside C and a the
number of non-centers at distance 1. Counting center-neighbour incidences,

    nK = 2e + sum_{t at distance 1} deg_C(t) >= 2e + 2a,    so  a <= nK/2 - e.

Every remaining state is at distance >= 2, hence

    N * D0(K) = sum_s d(s,C) >= a + 2(N - K - a) = 2(N-K) - a
                             >= 2(N-K) - nK/2.

If N*D0(K) < 2(N-K) - nK/2, flatness at (n,K) is IMPOSSIBLE.
------------------------------------------------------------------------

The remaining K are settled constructively: enumerate optimal K-median codes
that satisfy the Lemma-3 condition, and for each solve a small MIP for a
support-restricted encoder plus binary payment decoders achieving margin gamma.
A success is a certified flat point with an explicit construction.
"""
import itertools, json, sys, time
import numpy as np
import scipy.sparse as sp
from scipy.optimize import milp, linprog, LinearConstraint, Bounds

from exp_kflat import states, solve_D0_pmedian


# ----------------------------------------------------------------- counting
def counting_bound(n, K, D0):
    N = 2 ** n
    rhs = 2 * (N - K) - n * K / 2.0
    return dict(n=n, K=K, D0=D0, lhs_N_D0=N * D0, rhs=rhs,
                flatness_excluded=bool(N * D0 < rhs - 1e-9))


# ------------------------------------------------- optimal-code enumeration
def enumerate_codes(n, K, D0, limit=200, time_limit=120, require_double=True):
    """
    Enumerate K-subsets C of {0,1}^n with sum_s d_H(s,C) = N*D0 (optimal
    K-median codes) and, if require_double, every non-centre having >= 2
    neighbours in C. Uses no-good cuts to walk through distinct solutions.
    """
    S = states(n); N = 2 ** n
    Dm = (S[:, None, :] != S[None, :, :]).sum(2).astype(float)
    adj = (Dm == 1)

    nx = N * N
    NV = nx + N
    rows, cols, vals, lo, hi = [], [], [], [], []
    r = [0]

    def add(idx, coef, l, h):
        rows.extend([r[0]] * len(idx)); cols.extend(idx); vals.extend(coef)
        lo.append(l); hi.append(h); r[0] += 1

    for s in range(N):
        add([s * N + c for c in range(N)], [1.0] * N, 1.0, 1.0)
        for c in range(N):
            add([s * N + c, nx + c], [1.0, -1.0], -np.inf, 0.0)
    add([nx + c for c in range(N)], [1.0] * N, float(K), float(K))
    # total distance pinned to the optimum
    add(list(range(nx)), list(Dm.ravel()), N * D0 - 1e-6, N * D0 + 1e-6)
    if require_double:
        # v not a centre  =>  at least 2 neighbours are centres
        for v in range(N):
            nb = [nx + int(w) for w in np.where(adj[v])[0]]
            add(nb + [nx + v], [1.0] * len(nb) + [2.0], 2.0, np.inf)

    base_rows = r[0]
    A = sp.coo_matrix((vals, (rows, cols)), shape=(base_rows, NV)).tocsr()
    lo = np.array(lo); hi = np.array(hi)

    c_obj = np.zeros(NV)
    integ = np.zeros(NV); integ[nx:] = 1
    found = []
    cut_rows, cut_lo, cut_hi = [], [], []

    while len(found) < limit:
        if cut_rows:
            Af = sp.vstack([A, sp.csr_matrix(np.array(cut_rows))]).tocsr()
            lof = np.concatenate([lo, cut_lo]); hif = np.concatenate([hi, cut_hi])
        else:
            Af, lof, hif = A, lo, hi
        res = milp(c=c_obj, constraints=LinearConstraint(Af, lof, hif),
                   integrality=integ, bounds=Bounds(np.zeros(NV), np.ones(NV)),
                   options=dict(time_limit=time_limit, mip_rel_gap=0.0, presolve=True))
        if res.x is None:
            break
        C = tuple(sorted(int(v) for v in range(N) if res.x[nx + v] > 0.5))
        if len(C) != K or C in found:
            break
        found.append(C)
        row = np.zeros(NV)
        for v in C:
            row[nx + v] = 1.0
        cut_rows.append(row); cut_lo.append(-np.inf); cut_hi.append(float(K - 1))
    return found, (res.x is None)


# ------------------------------------------------- support-restricted margin
def margin_mip(n, C, gamma, time_limit=300, return_solution=False):
    """
    Given a centre set C (labels are indexed by position in C), decide whether
    there is an encoder q supported on each state's NEAREST centres together
    with binary payment decoders p_i in {0,1}^K achieving all-profile
    unilateral margin >= gamma. Feasible => flatness certified at (n,|C|).

    q is restricted by Lemma 1, so any feasible point automatically has
    D(q) = D0(K); this is verified post hoc.
    """
    S = states(n); N = 2 ** n; K = len(C)
    Cv = S[list(C)]
    dist = (S[:, None, :] != Cv[None, :, :]).sum(2)          # N x K
    near = (dist == dist.min(1, keepdims=True))              # allowed labels
    profiles = list(itertools.product([0, 1], repeat=n - 1))
    NP = len(profiles)

    nq = N * K
    Q = lambda s, y: s * K + y
    P = lambda i, y: nq + i * K + y
    W = lambda i, c, y: nq + n * K + (i * NP + c) * K + y
    NV = nq + n * K + n * NP * K

    rows, cols, vals, lo, hi = [], [], [], [], []
    r = [0]

    def add(idx, coef, l, h):
        rows.extend([r[0]] * len(idx)); cols.extend(idx); vals.extend(coef)
        lo.append(l); hi.append(h); r[0] += 1

    for s in range(N):
        add([Q(s, y) for y in range(K)], [1.0] * K, 1.0, 1.0)

    def edge(i, c):
        pr = profiles[c]
        hi_ = list(pr[:i]) + [1] + list(pr[i:])
        lo_ = list(pr[:i]) + [0] + list(pr[i:])
        return int("".join(map(str, hi_)), 2), int("".join(map(str, lo_)), 2)

    for i in range(n):
        for c in range(NP):
            s1, s0 = edge(i, c)
            for y in range(K):
                add([W(i, c, y), Q(s1, y), Q(s0, y), P(i, y)],
                    [1.0, -1.0, 1.0, 1.0], -np.inf, 1.0)
                add([W(i, c, y), Q(s1, y), Q(s0, y), P(i, y)],
                    [1.0, -1.0, 1.0, -1.0], -1.0, np.inf)
                add([W(i, c, y), P(i, y)], [1.0, -1.0], -np.inf, 0.0)
                add([W(i, c, y), P(i, y)], [1.0, 1.0], 0.0, np.inf)
            add([W(i, c, y) for y in range(K)], [1.0] * K, gamma, np.inf)

    A = sp.coo_matrix((vals, (rows, cols)), shape=(r[0], NV)).tocsr()
    ub = np.ones(NV); lb = np.zeros(NV)
    for s in range(N):                       # Lemma 1 support restriction
        for y in range(K):
            if not near[s, y]:
                ub[Q(s, y)] = 0.0
    for i in range(n):
        for c in range(NP):
            for y in range(K):
                lb[W(i, c, y)] = -1.0
    integ = np.zeros(NV)
    for i in range(n):
        for y in range(K):
            integ[P(i, y)] = 1

    t0 = time.time()
    res = milp(c=np.zeros(NV), constraints=LinearConstraint(A, np.array(lo), np.array(hi)),
               integrality=integ, bounds=Bounds(lb, ub),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0, presolve=True))
    out = dict(n=n, K=K, gamma=gamma, status=int(res.status),
               message=str(res.message), seconds=round(time.time() - t0, 2))
    if res.x is None:
        out["feasible"] = False
        return out

    # ---- post-hoc verification, independent of the solver ----
    q = np.clip(res.x[:nq].reshape(N, K), 0.0, 1.0)
    q = q / q.sum(1, keepdims=True)
    p = np.array([[round(res.x[P(i, y)]) for y in range(K)] for i in range(n)], float)
    D = 0.0
    for i in range(n):
        for y in range(K):
            p0 = q[S[:, i] == 0, y].sum() / N
            p1 = q[S[:, i] == 1, y].sum() / N
            D += min(p0, p1)
    margins = []
    for i in range(n):
        worst = np.inf
        for c in range(NP):
            s1, s0 = edge(i, c)
            worst = min(worst, float(np.dot(p[i], q[s1] - q[s0])))
        margins.append(worst)
    support_ok = bool(np.all(q[~near] < 1e-9))
    out.update(feasible=True, D_recomputed=float(D), min_margin=float(min(margins)),
               per_agent_margin=[float(m) for m in margins],
               support_respected=support_ok)
    if return_solution:
        out.update(centers=[S[c].tolist() for c in C], q=q.round(9).tolist(),
                   p=p.astype(int).tolist())
    return out


def general_p_margin(n, C, q):
    """
    Exact best achievable margin for agent i with a GENERAL p_i in [0,1]^K,
    via the elimination theorem: margin_i = min over lambda in the simplex of
    (1/2)||E_lambda[d_i]||_1, computed as an LP. Used to confirm that a
    construction found with binary p is not an artefact of that restriction.
    """
    S = states(n); N = 2 ** n; K = len(C)
    profiles = list(itertools.product([0, 1], repeat=n - 1))
    NP = len(profiles)
    out = []
    for i in range(n):
        d = np.zeros((NP, K))
        for c in range(NP):
            pr = profiles[c]
            s1 = int("".join(map(str, list(pr[:i]) + [1] + list(pr[i:]))), 2)
            s0 = int("".join(map(str, list(pr[:i]) + [0] + list(pr[i:]))), 2)
            d[c] = q[s1] - q[s0]
        # min_lambda sum_y t_y  s.t.  t >= +/- (lambda^T d), lambda in simplex
        nv = NP + K
        A_ub = np.zeros((2 * K, nv)); b_ub = np.zeros(2 * K)
        for y in range(K):
            A_ub[y, :NP] = d[:, y];  A_ub[y, NP + y] = -1.0
            A_ub[K + y, :NP] = -d[:, y]; A_ub[K + y, NP + y] = -1.0
        A_eq = np.zeros((1, nv)); A_eq[0, :NP] = 1.0
        c_obj = np.zeros(nv); c_obj[NP:] = 1.0
        res = linprog(c_obj, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0],
                      bounds=[(0, None)] * NP + [(0, None)] * K, method="highs")
        out.append(float(res.fun) / 2.0 if res.status == 0 else None)
    return out


# ------------------------------------------------------------------- driver
def main():
    n = int(sys.argv[1])
    Ks = [int(x) for x in sys.argv[2].split(",")]
    gammas = [float(g) for g in sys.argv[3].split(",")]
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    N = 2 ** n
    out = {}

    D0tab = {}
    for K in range(1, N + 1):
        D0tab[K] = solve_D0_pmedian(n, K, time_limit=120)["D_recomputed"]
    out["D0_table"] = D0tab
    strict = all(D0tab[K + 1] < D0tab[K] - 1e-12 for K in range(1, N))
    out["D0_strictly_decreasing"] = bool(strict)
    print(f"D0 strictly decreasing over K=1..{N}: {strict}  (Lemma 2 premise)",
          flush=True)

    for K in Ks:
        t0 = time.time()
        D0 = D0tab[K]
        cb = counting_bound(n, K, D0)
        row = dict(D0=D0, counting_bound=cb)
        # Lemma 3 constrains only states at distance EXACTLY 1 from C. The code
        # enumeration below imposes double-domination on every non-centre, which
        # coincides with Lemma 3 iff every non-centre is at distance 1, i.e.
        # iff N*D0(K) == N-K. Outside that regime the constraint is stronger
        # than Lemma 3, so an empty enumeration would NOT prove non-flatness.
        dominating_regime = abs(N * D0 - (N - K)) < 1e-6
        row["dominating_regime"] = bool(dominating_regime)
        row["enumeration_constraint_equals_lemma3"] = bool(dominating_regime)
        print(f"\n--- n={n} K={K}  D0={D0}  counting: N*D0={cb['lhs_N_D0']:.4f} "
              f"vs rhs={cb['rhs']:.4f} -> "
              f"{'FLATNESS IMPOSSIBLE' if cb['flatness_excluded'] else 'not excluded'}",
              flush=True)
        if cb["flatness_excluded"]:
            row["verdict"] = ("NOT FLAT (proved, arbitrary bounded payment decoders, "
                              "via Lemma 3 counting corollary)")
            out[K] = row
            json.dump(out, open(f"kflat_structure_n{n}.json", "w"), indent=1, default=float)
            continue

        codes, exhausted = enumerate_codes(n, K, D0, limit=limit)
        row["n_codes_enumerated"] = len(codes)
        row["code_enumeration_exhaustive"] = bool(exhausted)
        print(f"    optimal codes satisfying Lemma 3: {len(codes)} "
              f"(exhaustive={exhausted})", flush=True)
        if not codes:
            if exhausted and dominating_regime:
                row["verdict"] = ("NOT FLAT (proved: no optimal K-median code "
                                  "satisfies the Lemma 3 necessary condition)")
            elif exhausted:
                row["verdict"] = ("INCONCLUSIVE: enumeration exhausted but the "
                                  "double-domination constraint is STRONGER than "
                                  "Lemma 3 outside the dominating regime")
            else:
                row["verdict"] = "INCONCLUSIVE (code enumeration did not finish)"
            out[K] = row
            json.dump(out, open(f"kflat_structure_n{n}.json", "w"), indent=1, default=float)
            continue

        row["gammas"] = {}
        for g in gammas:
            best = None
            for ci, C in enumerate(codes):
                r = margin_mip(n, C, g, return_solution=True)
                if r.get("feasible") and r["support_respected"] \
                        and abs(r["D_recomputed"] - D0) < 1e-6 \
                        and r["min_margin"] >= g - 1e-6:
                    r["general_p_margin"] = general_p_margin(
                        n, C, np.array(r["q"]))
                    r["code_index"] = ci
                    best = r
                    break
            if best is not None:
                row["gammas"][str(g)] = dict(
                    verdict="FLAT_CERTIFIED", code_index=best["code_index"],
                    D_recomputed=best["D_recomputed"],
                    min_margin_binary_p=best["min_margin"],
                    general_p_margin=best["general_p_margin"],
                    centers=best["centers"], q=best["q"], p=best["p"],
                    seconds=best["seconds"])
                print(f"    gamma={g}: FLAT_CERTIFIED  (code #{best['code_index']}, "
                      f"D={best['D_recomputed']:.6f}, binary-p margin="
                      f"{best['min_margin']:.6f}, general-p margin="
                      f"{min(x for x in best['general_p_margin']):.6f})", flush=True)
            else:
                row["gammas"][str(g)] = dict(
                    verdict=("NOT FLAT for binary p over all enumerated codes"
                             if exhausted else "INCONCLUSIVE"),
                    codes_tested=len(codes))
                print(f"    gamma={g}: no construction among {len(codes)} codes "
                      f"(exhaustive={exhausted})", flush=True)
        row["seconds"] = round(time.time() - t0, 1)
        out[K] = row
        json.dump(out, open(f"kflat_structure_n{n}.json", "w"), indent=1, default=float)

    json.dump(out, open(f"kflat_structure_n{n}.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
