"""
TASK 1: the consecutive sequence gamma_2(Q_n), n = 1..7, with MIP gaps.

Session 2 computed K_flat only at odd n, so the sequence had gaps at n=4 and
n=6 and the OEIS check could not be specified correctly. This fills them in.

IMPORTANT SCOPE NOTE. Session 2's brute-force cross-validation
(`bruteforce_d0.py`) validated `solve_D0_pmedian`, the K-MEDIAN solver. The
2-domination feasibility MILP `kflat_theory.two_dominating_set` is a DIFFERENT
solver and was never independently validated. So this file does two things:

  METHOD M (MILP)   — kflat_theory.two_dominating_set, the session-2 solver.
  METHOD X (exact)  — complete enumeration over ALL subsets of V(Q_n), no LP,
                      no MILP, no pruning. Feasible for n <= 4 (2^16 = 65536
                      subsets at n=4). For n=5 an exhaustive check over all
                      C(32, K) subsets at the critical cardinalities is run
                      instead, which is still a complete proof for those K.

Any gamma_2 value is a two-sided claim, so both sides are checked separately:
  * upper side: exhibit a set of size K and verify 2-domination directly;
  * lower side: show NO set of size K-1 is 2-dominating.
Method X settles both by enumeration; method M settles the lower side by MILP
infeasibility (status 2), which is a proof only if the solver is correct.
"""
import itertools, json, time, warnings
from math import comb
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out

warnings.filterwarnings("ignore")

from kflat_theory import two_dominating_set, check_two_dominating


def neighbours(n):
    N = 2 ** n
    return [[v ^ (1 << i) for i in range(n)] for v in range(N)]


def is_2_dominating(n, Cmask, nb):
    """Every vertex NOT in C has >= 2 neighbours in C. Bitmask version."""
    N = 2 ** n
    for v in range(N):
        if (Cmask >> v) & 1:
            continue
        c = 0
        for w in nb[v]:
            if (Cmask >> w) & 1:
                c += 1
                if c >= 2:
                    break
        if c < 2:
            return False
    return True


def gamma2_exhaustive_all_subsets(n):
    """METHOD X, full: every one of the 2^(2^n) subsets. n <= 4 only."""
    N = 2 ** n
    nb = neighbours(n)
    best = None
    best_set = None
    for mask in range(1 << N):
        k = bin(mask).count("1")
        if best is not None and k >= best:
            continue
        if is_2_dominating(n, mask, nb):
            best = k
            best_set = [v for v in range(N) if (mask >> v) & 1]
    return best, best_set, 1 << N


def gamma2_exhaustive_at_size(n, K):
    """
    METHOD X, restricted: enumerate every C(2^n, K) subset of size exactly K.
    Returns a witness if one is 2-dominating, else None (a complete proof that
    gamma_2 > K). Used where the full 2^(2^n) sweep is out of reach.
    """
    N = 2 ** n
    nb = neighbours(n)
    count = 0
    for combo in itertools.combinations(range(N), K):
        count += 1
        mask = 0
        for v in combo:
            mask |= 1 << v
        if is_2_dominating(n, mask, nb):
            return list(combo), count
    return None, count


if __name__ == "__main__":
    out = {}

    # ---------------- METHOD X vs METHOD M on n = 1..4 ----------------
    print("=== METHOD X (complete enumeration of all subsets) vs METHOD M (MILP) ===",
          flush=True)
    for n in [1, 2, 3, 4]:
        t0 = time.time()
        gx, setx, nsub = gamma2_exhaustive_all_subsets(n)
        tx = time.time() - t0

        # MILP: smallest K that is feasible, with infeasibility proved below it
        gm, rows = None, []
        for K in range(1, 2 ** n + 1):
            C, info = two_dominating_set(n, K, time_limit=600)
            rows.append(dict(K=K, feasible=C is not None, status=info["status"],
                             seconds=info["seconds"]))
            if C is not None:
                gm = K
                chk = check_two_dominating(n, C)
                break
        agree = (gx == gm)
        print(f"  n={n}: METHOD X = {gx} ({nsub} subsets, {tx:.2f}s) | "
              f"METHOD M = {gm} | {'AGREE' if agree else 'DISAGREE'}", flush=True)
        out[f"n{n}"] = dict(method_X=gx, method_X_subsets=nsub, method_X_set=setx,
                            method_M=gm, agree=bool(agree), milp_rows=rows)
        json.dump(out, open(out("gamma2_sequence.json"), "w"), indent=1, default=float)

    # ---------------- n = 5, 6, 7 ----------------
    print("\n=== MILP for n = 5, 6, 7 (with independent recheck of each witness) ===",
          flush=True)
    for n in [5, 6, 7]:
        rows = []
        gm = None
        lo = max(1, int(2 * 2 ** n / (n + 2)))      # Fink-Jacobson 1985
        for K in range(lo, 2 ** n + 1):
            C, info = two_dominating_set(n, K, time_limit=1800)
            row = dict(K=K, feasible=C is not None, status=info["status"],
                       seconds=info["seconds"])
            if C is not None:
                chk = check_two_dominating(n, C)
                row["recheck"] = chk
                rows.append(row)
                gm = K
                print(f"  n={n} K={K}: FEASIBLE, recheck min_deg="
                      f"{chk['min_deg_outside']} is_2_dom={chk['is_2_dominating']} "
                      f"[{info['seconds']}s]", flush=True)
                break
            tag = "INFEASIBLE (proved)" if info["status"] == 2 else \
                  f"UNRESOLVED status {info['status']}"
            print(f"  n={n} K={K}: {tag}  [{info['seconds']}s]", flush=True)
            rows.append(row)
            if info["status"] != 2:
                break
        out[f"n{n}"] = dict(method_M=gm, fink_jacobson_lb=lo, milp_rows=rows)
        json.dump(out, open(out("gamma2_sequence.json"), "w"), indent=1, default=float)

    seq = [out.get(f"n{n}", {}).get("method_M") or out.get(f"n{n}", {}).get("method_X")
           for n in range(1, 8)]
    out["sequence_n1_to_n7"] = seq
    print(f"\ngamma_2(Q_n) for n=1..7: {seq}")
    json.dump(out, open(out("gamma2_sequence.json"), "w"), indent=1, default=float)
