"""
STEP 1: brute-force cross-validation of the fast D0(K) solver.

Session 1 replaced a stalled MILP with `exp_kflat.solve_D0_pmedian`, which
computes

    D0(K) = (1/2^n) * min_{C subset of {0,1}^n, |C| <= K} sum_s d_H(s, C)

as a p-median MILP through HiGHS. That solver was never checked against
anything but itself and a single T2 sanity point, and every downstream number
(K_flat(5)=10, K_flat(7)>=29, the whole scaling law) rests on it. This file
recomputes the same quantity with NO LP and NO MILP.

Two independent methods, both exact:

  METHOD E (exhaustive).  Enumerate literally every subset of the 2^n
  vertices, compute sum_s d_H(s,C) directly, and keep the minimum for each
  cardinality. Complete, no pruning, no heuristics. Feasible for n<=4
  (2^16 = 65536 subsets at n=4).

  METHOD B (branch and bound).  Exact search for n=5, where 2^32 subsets is
  out of reach. Correctness rests on two facts:
    * WLOG 0 is a centre. Aut(Q_n) is vertex-transitive and sum_s d_H(s,C) is
      invariant under it, so every C can be mapped to one containing 0.
    * The pruning bound is admissible. Write delta(c) = f(C) - f(C + {c}) for
      the marginal reduction of a single centre. The reduction function is
      submodular (adding centres has diminishing returns: the min over a
      larger set can only be reached sooner), so for any S,
          f(C) - f(C union S)  <=  sum_{c in S} delta(c),
      hence f(C union S) >= f(C) - (sum of the |S| largest deltas). Branches
      are cut only when that lower bound is already >= the incumbent for every
      reachable cardinality.
  The incumbent is seeded by our OWN greedy, never by the p-median solver, so
  a wrong p-median value cannot prune away the true optimum and thereby
  "confirm" itself.

METHOD B is validated against METHOD E at n=3 and n=4 before being trusted at
n=5.
"""
import itertools, json, time
import numpy as np
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out


def dist_matrix(n):
    S = np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int8)
    return (S[:, None, :] != S[None, :, :]).sum(2).astype(np.int32), S


# --------------------------------------------------------------- method E
def d0_exhaustive(n):
    """Every subset of the 2^n vertices. Complete enumeration, no pruning."""
    D, _ = dist_matrix(n)
    N = 2 ** n
    best = np.full(N + 1, np.iinfo(np.int64).max, dtype=np.int64)
    best_set = [None] * (N + 1)
    for mask in range(1, 1 << N):
        members = [i for i in range(N) if (mask >> i) & 1]
        cost = int(D[:, members].min(1).sum())
        k = len(members)
        if cost < best[k]:
            best[k] = cost
            best_set[k] = members
    return best, best_set


# --------------------------------------------------------------- method B
def _greedy(D, N, Kmax):
    """Own-code greedy incumbents; only ever used as an upper bound."""
    best = np.full(N + 1, np.iinfo(np.int64).max, dtype=np.int64)
    for start in range(N):
        chosen = [start]
        dist = D[start].copy()
        best[1] = min(best[1], int(dist.sum()))
        while len(chosen) < Kmax:
            cand = np.minimum(dist[None, :], D)          # N x N
            sums = cand.sum(1)
            sums[chosen] = np.iinfo(np.int32).max
            c = int(np.argmin(sums))
            chosen.append(c)
            dist = np.minimum(dist, D[c])
            k = len(chosen)
            best[k] = min(best[k], int(dist.sum()))
    return best


def sphere_lower_bound(n, K):
    """
    Valid lower bound on min_{|C|=K} sum_s d_H(s,C), from sphere packing.

        sum_s d(s,C) = sum_{r>=0} |{s : d(s,C) > r}| = sum_{r>=0} (N - |ball_r(C)|)

    and |ball_r(C)| <= K * V(r) with V(r) = sum_{i<=r} C(n,i). Hence

        sum_s d(s,C) >= sum_{r=0}^{n-1} max(0, N - K*V(r)).

    Tight whenever a perfect or near-perfect covering exists, which settles
    most K with no search at all.
    """
    N = 2 ** n
    from math import comb
    tot, V = 0, 0
    for r in range(n):
        V += comb(n, r)
        tot += max(0, N - K * V)
    return tot


def d0_bnb_single(n, K, D=None, verbose=False):
    """
    Exact branch and bound for ONE cardinality K. Searching a single K lets
    the bound cut deep branches, which the all-K version cannot do (deep
    branches are always still needed for some larger cardinality).

    Returns (best_cost, best_set, nodes, proved_by_bound).
    """
    if D is None:
        D, _ = dist_matrix(n)
    N = 2 ** n
    lb = sphere_lower_bound(n, K)

    g = _greedy(D, N, K)
    best = [int(g[K])]
    best_set = [None]
    nodes = [0]
    if best[0] <= lb:                      # incumbent already meets the bound
        return best[0], None, 0, True

    def dfs(start, chosen, dist, cost):
        nodes[0] += 1
        k = len(chosen)
        if k == K:
            if cost < best[0]:
                best[0] = cost
                best_set[0] = list(chosen)
            return
        m = K - k
        if start >= N or N - start < m:
            return
        cand = np.arange(start, N)
        newd = np.minimum(dist[None, :], D[cand])
        sums = newd.sum(1)
        deltas = cost - sums
        order = np.argsort(-deltas)
        prefix = np.concatenate([[0], np.cumsum(deltas[order])])
        if m > len(cand) or cost - prefix[m] >= best[0]:
            return                          # admissible (submodularity)
        for j in order:
            c = int(cand[int(j)])
            if N - c - 1 < m - 1:
                continue
            chosen.append(c)
            dfs(c + 1, chosen, newd[int(j)], int(sums[int(j)]))
            chosen.pop()
            if best[0] <= lb:
                return

    dfs(1, [0], D[0].copy(), int(D[0].sum()))   # WLOG 0 in C (vertex-transitive)
    if verbose:
        print(f"      [K={K}: {nodes[0]} nodes, lb={lb}, best={best[0]}]", flush=True)
    return best[0], best_set[0], nodes[0], False


def d0_bnb(n, verbose=False):
    """Exact per-cardinality branch and bound. Returns best[k] for k=1..2^n."""
    D, _ = dist_matrix(n)
    N = 2 ** n
    best = np.zeros(N + 1, dtype=np.int64)
    sets = [None] * (N + 1)
    total_nodes = 0
    for K in range(1, N + 1):
        v, st, nodes, by_bound = d0_bnb_single(n, K, D=D, verbose=verbose)
        best[K] = v
        sets[K] = st
        total_nodes += nodes
    return best, sets, total_nodes


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    from exp_kflat import solve_D0_pmedian

    out = {}

    # ---- 1. validate method B against complete enumeration at n=3 and n=4
    print("=== METHOD B vs METHOD E (complete enumeration) ===", flush=True)
    okBE = True
    for n in [3, 4]:
        N = 2 ** n
        t0 = time.time()
        eb, _ = d0_exhaustive(n)
        t1 = time.time()
        bb, _, nodes = d0_bnb(n)
        t2 = time.time()
        agree = all(int(eb[k]) == int(bb[k]) for k in range(1, N + 1))
        okBE &= agree
        print(f"  n={n}: exhaustive {t1-t0:.1f}s ({2**N} subsets), "
              f"bnb {t2-t1:.1f}s ({nodes} nodes) -> "
              f"{'IDENTICAL' if agree else 'DISAGREE'}", flush=True)
        if not agree:
            for k in range(1, N + 1):
                if int(eb[k]) != int(bb[k]):
                    print(f"    first disagreement k={k}: E={eb[k]} B={bb[k]}")
                    break
        out[f"BE_n{n}"] = dict(agree=bool(agree),
                               exhaustive=[int(x) for x in eb[1:N + 1]],
                               bnb=[int(x) for x in bb[1:N + 1]],
                               subsets=2 ** N, bnb_nodes=int(nodes))
    out["method_B_validated"] = bool(okBE)
    print(f"  method B validated: {okBE}\n", flush=True)
    if not okBE:
        json.dump(out, open(out("bruteforce_d0.json"), "w"), indent=1, default=float)
        raise SystemExit("STOP: branch and bound disagrees with complete "
                         "enumeration. Brute-force reference is itself broken.")

    # ---- 2. brute force vs the fast p-median solver
    print("=== brute force vs exp_kflat.solve_D0_pmedian ===", flush=True)
    verdict_all = True
    first_bad = None
    for n in [3, 5]:
        N = 2 ** n
        t0 = time.time()
        if n <= 4:
            ref, ref_set = d0_exhaustive(n)
            method = "exhaustive (complete enumeration)"
            nodes = 2 ** N
        else:
            ref, ref_set, nodes = d0_bnb(n, verbose=True)
            method = "branch and bound (exact)"
        print(f"  n={n} reference by {method}, {time.time()-t0:.1f}s", flush=True)
        rows = []
        for K in range(2, N + 1):
            brute = int(ref[K]) / N
            r = solve_D0_pmedian(n, K, time_limit=900)
            fast = r["D_recomputed"]
            gap = r["gap"]
            match = abs(brute - fast) < 1e-9
            verdict_all &= match
            if not match and first_bad is None:
                first_bad = (n, K, brute, fast)
            rows.append(dict(K=K, brute_force=brute, fast_solver=fast,
                             fast_value=r["value"], mip_gap=gap,
                             diff=brute - fast, match=bool(match),
                             fast_seconds=r["seconds"]))
            flag = "ok" if match else "  <-- MISMATCH"
            print(f"    K={K:3d}  brute={brute:.10f}  fast={fast:.10f}  "
                  f"diff={brute-fast:+.2e}  gap={gap}{flag}", flush=True)
        out[f"compare_n{n}"] = dict(method=method, nodes=int(nodes), rows=rows)
        json.dump(out, open(out("bruteforce_d0.json"), "w"), indent=1, default=float)

    out["all_match"] = bool(verdict_all)
    out["first_disagreement"] = first_bad
    json.dump(out, open(out("bruteforce_d0.json"), "w"), indent=1, default=float)
    print(f"\nVERDICT: all K at n=3 and n=5 match: {verdict_all}")
    if first_bad:
        print(f"FIRST DISAGREEMENT: n={first_bad[0]} K={first_bad[1]} "
              f"brute={first_bad[2]} fast={first_bad[3]}")
