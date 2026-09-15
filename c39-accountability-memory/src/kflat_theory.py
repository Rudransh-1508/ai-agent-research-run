"""
K_flat(n) = gamma_2(Q_n), the 2-DOMINATION NUMBER of the hypercube.

Session 1 left K_flat as the output of a search. Inspecting the certified
n=5, K=10 code showed what the search was actually finding, and it reduces
the whole problem to a classical graph invariant.

------------------------------------------------------------------ LEMMA 3'
(strengthens session 1's Lemma 3 from distance-1 states to ALL states)

Let D0 be strictly decreasing at K, so by Lemma 2 the K centres are distinct.
Suppose s is NOT a centre, d(s,C) = r >= 1, and s has a UNIQUE nearest centre
c. Flip a bit of s towards c to get s', so d(s',c) = r-1. For any other centre
c', uniqueness forces d(s,c') >= r+1, hence d(s',c') >= r > r-1. So c is also
the unique nearest centre of s'. By Lemma 1 both q[s] and q[s'] are point
masses on c's label, so that edge has d_i = 0 and

    <p_i, d_i> = 0 < gamma   for EVERY p_i in [0,1]^K.

Therefore: **flatness requires every non-centre to have at least two nearest
centres.** When C is dominating (every non-centre at distance 1) this is
exactly the statement that C is a 2-DOMINATING SET of Q_n.

------------------------------------------------------------- CONVERSE
Let C be 2-dominating with |C| = K >= gamma(Q_n). Define

    q[c]   = point mass on c's own label,           for c in C
    q[t]   = uniform over the labels of N(t) ∩ C,   for t not in C
    p_i[y] = (centre of label y)_i                  (pay agent i the
                                                     reconstructed i-th bit)

Since every non-centre is at distance 1 and q is supported on nearest centres,
Lemma 1 gives D(q) = (N-K)/N = D0(K). For the margin, take the edge
s1 = s0 + e_i and write d_t = |N(t) ∩ C|:

  * both in C:        margin = 1 - 0 = 1
  * s1 in C, s0 not:  s0's centre-neighbours are s1 (i-th bit 1) and others
                      s0+e_j, j != i (i-th bit 0), so margin = 1 - 1/d_{s0}
  * s0 in C, s1 not:  symmetrically, margin = 1 - 1/d_{s1}
  * neither in C:     every centre-neighbour of s1 other than s0 has i-th bit
                      1, and s0 is not a centre, so the average is 1; likewise
                      s0's average is 0; margin = 1

So the all-profile unilateral margin is exactly 1 - 1/d_min >= 1/2. Flat.

------------------------------------------------------------- CONSEQUENCE
    K_flat(n) = gamma_2(Q_n)   in the dominating regime,
and the pure counting bound on 2-domination, n*K - 2e >= 2(N-K), gives

    gamma_2(Q_n) >= 2^(n+1) / (n+2),

which is session 1's bound, now with its combinatorial meaning visible.
gamma_2 is a finite graph invariant, so K_flat becomes a feasibility question
over 2^n binaries instead of a search over encoders and payment decoders.

CAVEAT, stated up front: the converse needs K >= gamma(Q_n). Below that,
optimal codes are not dominating and Lemma 3' is weaker than 2-domination, so
small K must be excluded separately (`exclusion_scan` below). Every reported
K_flat records explicitly which K were covered and by what.
"""
import itertools, json, time
from math import comb

import numpy as np
import scipy.sparse as sp
from scipy.optimize import milp, LinearConstraint, Bounds

from bruteforce_d0 import dist_matrix, _greedy, sphere_lower_bound


# ------------------------------------------------------- 2-domination search
def two_dominating_set(n, K, time_limit=900, forbid=None):
    """
    Feasibility: is there C subset of Q_n with |C| = K such that every vertex
    outside C has at least 2 neighbours in C?

        v not in C  =>  sum_{w ~ v} u[w] >= 2
    linearised as  sum_{w~v} u[w] + 2*u[v] >= 2.

    Returns the set, or None with the solver status (2 = proved infeasible).
    """
    N = 2 ** n
    nb = [[v ^ (1 << i) for i in range(n)] for v in range(N)]
    rows, cols, vals, lo, hi = [], [], [], [], []
    r = [0]

    def add(idx, coef, l, h):
        rows.extend([r[0]] * len(idx)); cols.extend(idx); vals.extend(coef)
        lo.append(l); hi.append(h); r[0] += 1

    for v in range(N):
        add(nb[v] + [v], [1.0] * n + [2.0], 2.0, np.inf)
    add(list(range(N)), [1.0] * N, float(K), float(K))
    if forbid:
        for C in forbid:
            add(list(C), [1.0] * len(C), -np.inf, float(len(C) - 1))

    A = sp.coo_matrix((vals, (rows, cols)), shape=(r[0], N)).tocsr()
    t0 = time.time()
    res = milp(c=np.zeros(N),
               constraints=LinearConstraint(A, np.array(lo), np.array(hi)),
               integrality=np.ones(N),
               bounds=Bounds(np.zeros(N), np.ones(N)),
               options=dict(time_limit=time_limit, mip_rel_gap=0.0, presolve=True))
    secs = round(time.time() - t0, 2)
    if res.x is None:
        return None, dict(status=int(res.status), message=str(res.message),
                          seconds=secs, K=K, n=n)
    C = sorted(int(v) for v in range(N) if res.x[v] > 0.5)
    return C, dict(status=int(res.status), seconds=secs, K=K, n=n)


def check_two_dominating(n, C):
    """Independent recheck of the 2-domination property, no solver."""
    N = 2 ** n
    Cs = set(C)
    degs = []
    for v in range(N):
        if v in Cs:
            continue
        degs.append(sum(1 for i in range(n) if (v ^ (1 << i)) in Cs))
    e = sum(1 for c in C for i in range(n) if (c ^ (1 << i)) in Cs) // 2
    return dict(size=len(C), min_deg_outside=(min(degs) if degs else None),
                is_2_dominating=bool(degs and min(degs) >= 2),
                internal_edges=e, n_outside=len(degs))


# --------------------------------------------- verify the flat construction
def verify_flat_construction(n, C):
    """
    Build the canonical construction of the CONVERSE above and recompute
    everything directly: no solver, no reuse of any model.
    """
    N = 2 ** n
    S = np.array(list(itertools.product([0, 1], repeat=n)), dtype=int)
    Cs = sorted(C)
    lab = {c: y for y, c in enumerate(Cs)}
    K = len(Cs)

    q = np.zeros((N, K))
    for v in range(N):
        if v in lab:
            q[v, lab[v]] = 1.0
        else:
            nbs = [v ^ (1 << i) for i in range(n) if (v ^ (1 << i)) in lab]
            if not nbs:
                return dict(valid=False, reason=f"state {v} has no centre neighbour")
            for t in nbs:
                q[v, lab[t]] = 1.0 / len(nbs)
    assert np.allclose(q.sum(1), 1.0)

    # distortion via coordinate-wise MAP (optimal for Hamming loss)
    D = 0.0
    for i in range(n):
        for y in range(K):
            p0 = q[S[:, i] == 0, y].sum() / N
            p1 = q[S[:, i] == 1, y].sum() / N
            D += min(p0, p1)

    p = np.array([[S[c][i] for c in Cs] for i in range(n)], dtype=float)

    margins = []
    for i in range(n):
        worst = np.inf
        bit = 1 << (n - 1 - i)
        for v in range(N):
            if v & bit:
                continue
            worst = min(worst, float(np.dot(p[i], q[v | bit] - q[v])))
        margins.append(worst)

    Dmat, _ = dist_matrix(n)
    D0 = float(Dmat[:, Cs].min(1).sum()) / N
    return dict(valid=True, n=n, K=K, D=float(D), D0=D0,
                flat=bool(abs(D - D0) < 1e-9),
                min_margin=float(min(margins)),
                per_agent_margin=[float(m) for m in margins],
                predicted_margin=None)


# ------------------------------------------------------------ small-K scan
def exclusion_scan(n, Kmax, exact_D0=None):
    """
    Session 1's counting corollary: flatness at (n,K) is impossible when

        N*D0(K)  <  2(N-K) - nK/2.

    Exclusion needs an UPPER bound on D0, so a greedy code suffices: if
    greedy < rhs then D0 <= greedy < rhs. Greedy is our own code, no solver.
    Rows greedy cannot settle are reported as NOT COVERED rather than assumed.
    """
    N = 2 ** n
    D, _ = dist_matrix(n)
    g = _greedy(D, N, min(Kmax, N))
    rows = {}
    for K in range(2, Kmax + 1):
        ub = int(g[K])                       # upper bound on N*D0(K)
        if exact_D0 and K in exact_D0:
            ub = min(ub, int(round(exact_D0[K] * N)))
        rhs = 2 * (N - K) - n * K / 2.0
        lb = sphere_lower_bound(n, K)
        rows[K] = dict(N_D0_upper=ub, N_D0_lower=lb, rhs=rhs,
                       excluded=bool(ub < rhs - 1e-9))
    return rows


# ------------------------------------------------------- shell counting bound
def shell_bound(n, K):
    """
    STRONGER than the session-1 counting corollary, and the one that closes
    the small-K regime.

    By Lemma 3' every state at distance r >= 1 from C has at least TWO centres
    at distance exactly r. The number of (state, centre) pairs at distance r is
    at most K*C(n,r), since each centre has C(n,r) states at distance r. Hence
    the number of states in shell r satisfies

        n_r  <=  floor( K * C(n,r) / 2 ).

    Since sum_{r>=1} n_r = N - K and the distortion is sum_r r*n_r, filling the
    shells greedily from the inside gives a valid LOWER bound on N*D0 for any C
    that could possibly be flat:

        f_min(n,K) = min sum_r r*n_r  s.t.  sum n_r = N-K,  n_r <= cap_r.

    If f_min > N*D0(K), no flat C exists at (n,K). This reduces to the session-1
    bound exactly when everything fits in shell 1, and is strictly stronger
    otherwise. Sanity: it does NOT exclude the known flat points (n=3,K=4;
    n=5,K=10; n=7,K=32), where it is tight.
    """
    N = 2 ** n
    remaining = N - K
    cost = 0
    for r in range(1, n + 1):
        cap = (K * comb(n, r)) // 2
        take = min(cap, remaining)
        cost += r * take
        remaining -= take
        if remaining <= 0:
            break
    if remaining > 0:
        return None                      # cannot even place all states
    return cost


def shell_exclusion_scan(n, Kmax, extra_upper=None):
    """Exclude (n,K) when shell_bound > an UPPER bound on N*D0(K)."""
    N = 2 ** n
    D, _ = dist_matrix(n)
    g = _greedy(D, N, min(Kmax, N))
    rows = {}
    for K in range(2, Kmax + 1):
        ub = int(g[K])
        if extra_upper and K in extra_upper:
            ub = min(ub, int(round(extra_upper[K] * N)))
        fmin = shell_bound(n, K)
        old_rhs = 2 * (N - K) - n * K / 2.0
        rows[K] = dict(N_D0_upper=ub, shell_lower=fmin, old_rhs=old_rhs,
                       excluded_shell=bool(fmin is not None and fmin > ub + 1e-9),
                       excluded_old=bool(ub < old_rhs - 1e-9))
    return rows
