"""K_flat under a general full-support prior, computed by direct enumeration.

    python prior_threshold.py            # n = 3, 4 over a grid of q

WHAT THIS SCRIPT REPLACES, AND WHY
----------------------------------
An earlier version of this script computed

    K_flat(pi) = min { K : some pi-optimal K-median set is 2-DOMINATING }

by two MILPs. That specification is WRONG. Lemma 3' (necessity) says every
non-centre has at least two centres at ITS OWN NEAREST DISTANCE d(s,C) -- not at
distance 1. The two coincide only when the pi-optimal code is dominating. Under
the uniform prior with K >= gamma(Q_n) it is, which is why Theorem 9 is fine.
Under a tilted prior the optimal code concentrates on heavy profiles and can
leave a light profile at distance 2, and then the 2-domination test is far too
strong: it reports a threshold of 2^n - (n-1) where the truth is much smaller.

Counterexample the old script could not see, at n = 3, q = 0.7, K = 4:

    C = {011, 101, 110, 111} is the unique pi-optimal 4-median set,
    D_0(4) = 0.2430, and 000 is at distance 2 from C -- so C is NOT
    2-dominating and the old script rejected K = 4. But spreading each
    non-centre's mass uniformly over its nearest centres gives D = 0.2430
    exactly, with margin 1/3. The record is flat. The old threshold of 6 was
    wrong, and so was the "collapse to ratio 1" conclusion drawn from it.

So this script does not test a proxy condition at all. It enumerates every
K-subset, finds the pi-optimal ones, builds the spread record on each, and asks
the Theorem 3 LP directly whether the margin is positive while D == D_0(K). A
flat record is reported only when one has actually been exhibited.

Enumeration is 2^(2^n) subsets, so n <= 4 only. That is enough to refute the
withdrawn claim; the general-prior threshold is left open in the paper.
"""
import json, sys, itertools, time
import numpy as np
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from c39.paths import out
from experiment_agents import popcount, prior, margin, distortion

TOL = 1e-9


def hamming(n):
    N = 1 << n
    return np.array([[popcount(a ^ b) for b in range(N)] for a in range(N)])


def code_cost(pi, H, C):
    """Expected Hamming error of the best reconstruction from centre set C."""
    return float(pi @ H[:, list(C)].min(axis=1))


def nearest(H, C, s):
    """(distance to C, the centres attaining it)."""
    d = min(H[s][c] for c in C)
    return d, [c for c in C if H[s][c] == d]


def spread_record(n, C, H):
    """Each centre a point mass; each non-centre uniform on its NEAREST centres.

    This is the Lemma-2 construction with distance 1 relaxed to d(s,C). It
    attains D_0(K) whenever C is pi-optimal, because every profile's mass sits
    entirely on centres at its own minimum distance.
    """
    N = 1 << n
    K = len(C)
    idx = {c: j for j, c in enumerate(C)}
    q = np.zeros((N, K))
    for s in range(N):
        _, nr = nearest(H, C, s)
        for c in nr:
            q[s, idx[c]] = 1.0 / len(nr)
    return q


def necessary_condition(n, C, H):
    """Lemma 3' in the form that holds for any prior."""
    return all(len(nearest(H, C, s)[1]) >= 2 for s in range(1 << n) if s not in C)


def scan(n, q_, verbose=True):
    """Least K at which a flat record exists, by exhibiting one."""
    N = 1 << n
    pi = prior(n, q_)
    H = hamming(n)
    rows = []
    for K in range(2, N + 1):
        best = min(code_cost(pi, H, C) for C in itertools.combinations(range(N), K))
        opt = [C for C in itertools.combinations(range(N), K)
               if code_cost(pi, H, C) <= best + TOL]
        flat, witness, gam = False, None, 0.0
        n_nec = 0
        for C in opt:
            if not necessary_condition(n, C, H):
                continue
            n_nec += 1
            rec = spread_record(n, C, H)
            D = distortion(n, pi, rec)
            g = margin(n, rec)
            if D <= best + TOL and g > TOL:
                flat, witness, gam = True, C, g
                break
        rows.append(dict(K=K, D0=best, n_optimal=len(opt),
                         n_meeting_condition=n_nec, flat=bool(flat),
                         gamma=float(gam),
                         witness=[format(c, "0" + str(n) + "b") for c in witness]
                         if witness else None,
                         witness_dominating=bool(witness is not None and
                             all(nearest(H, witness, s)[0] <= 1
                                 for s in range(N)))))
        if verbose:
            r = rows[-1]
            print(f"  K={K:3d}  D0={best:.6f}  optimal codes={len(opt):5d}"
                  f"  meeting cond={n_nec:5d}  flat={'YES' if flat else 'no ':>3}"
                  f"  gamma={gam:.4f}"
                  + ("  dominating" if r["witness_dominating"] else ""))
        if flat:
            return K, rows
    return None, rows


if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:]] or [3, 4]
    res = {}
    t0 = time.time()
    for n in ns:
        for q_ in (0.5, 0.7):
            tag = f"n={n} q={q_}"
            print(f"\n{tag}")
            K, rows = scan(n, q_)
            print(f"  -> K_flat = {K}")
            res[tag] = dict(n=n, q=q_, K_flat=K, rows=rows,
                            withdrawn_claim=(1 << n) - (n - 1) if q_ != 0.5 else None)
    res["_meta"] = dict(seconds=round(time.time() - t0, 1),
                        note="flatness is exhibited, not inferred from a proxy")
    p = out("prior_threshold.json")
    json.dump(res, open(p, "w"), indent=1)
    print(f"\nwrote {p}")
    print("\nsummary")
    for tag, v in res.items():
        if tag.startswith("_"):
            continue
        w = v["withdrawn_claim"]
        print(f"  {tag:12s} K_flat = {v['K_flat']}"
              + (f"   (earlier version claimed {w})" if w else "   (uniform)"))
