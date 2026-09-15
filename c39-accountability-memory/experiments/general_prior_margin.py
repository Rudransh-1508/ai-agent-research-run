"""Phase 1: does the Lemma 8 construction survive at nearest-distance r >= 2?

    python experiments/general_prior_margin.py            # n = 3,4 full sweep
    python experiments/general_prior_margin.py 5          # add an n=5 sampled sweep

THE GENERALISED CONSTRUCTION
----------------------------
Let pi be any full-support prior and C any pi-optimal K-median code. Write

    N(s) = {s}                                     if s in C
    N(s) = {c in C : d(s,c) = d(s,C)}              otherwise      (nearest centres)
    nu(s) = |N(s)|

and define the record and payment

    q[s,.] = Unif(labels of N(s)),      p_i[y] = (centre of label y)_i .

r = 1 is Lemma 8. This script tests the general-r case.

THE CLAIM UNDER TEST (derived by hand, verified here before being believed)
--------------------------------------------------------------------------
Parity does the work. For an edge s_1 = s_0 + e_i, every centre c satisfies
d(s_0,c) = d(s_1,c) +/- 1, so the two nearest-sets are never equal-distance
overlapping. Exactly two cases arise:

  (a) d(s_0,C) = d(s_1,C) = r   ->  N(s_0) and N(s_1) are DISJOINT, TV = 1
  (b) d(s_1,C) = d(s_0,C) - 1   ->  N(s_1) SUBSET-OF N(s_0), TV = 1 - nu(s_1)/nu(s_0)

and in both cases every c in N(s_1) has c_i = s_{1,i} while every
c in N(s_0) \ N(s_1) has c_i = s_{0,i}. So the natural payment p_i picks out
exactly the positive part of d_i, giving <p_i, d_i> = (1/2)||d_i||_1 on EVERY
edge. Since a minimum of a linear functional over mixtures is attained at a
point mass, that turns Theorem 3's min-over-mixtures into a min-over-edges and
the two bounds meet:

    gamma  =  min over edges TV  =  1 - max over DESCENDING edges nu(s_1)/nu(s_0)

where an edge is descending if d(s_1,C) = d(s_0,C) - 1. Hence

    gamma > 0  <=>  nu strictly DECREASES along every descending edge.

At r = 1 the closer endpoint is a centre, nu = 1, and this is 1 - 1/d_min.
Proposition 12 (nu >= 2 everywhere) does NOT imply the strict decrease once
r >= 2, so the construction is not guaranteed to work in general. This script
looks for a code where it fails.
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


def nearest_sets(n, C, H):
    """N(s) for every s: {s} on centres, the nearest centres otherwise."""
    N = 1 << n
    inC = set(C)
    out_ = []
    for s in range(N):
        if s in inC:
            out_.append((0, [s]))
        else:
            d = min(H[s][c] for c in C)
            out_.append((d, [c for c in C if H[s][c] == d]))
    return out_


def spread_record(n, C, H):
    N, K = 1 << n, len(C)
    idx = {c: j for j, c in enumerate(C)}
    q = np.zeros((N, K))
    for s, (_, nr) in enumerate(nearest_sets(n, C, H)):
        for c in nr:
            q[s, idx[c]] = 1.0 / len(nr)
    return q


def predicted_margin(n, C, H):
    """The closed form above: 1 - max over descending edges of nu(s1)/nu(s0).

    Also returns the binding edge, so a failure can be inspected rather than
    just counted.
    """
    ns = nearest_sets(n, C, H)
    worst, witness = 1.0, None
    for s0 in range(1 << n):
        for i in range(n):
            s1 = s0 ^ (1 << i)
            d0, A0 = ns[s0]
            d1, A1 = ns[s1]
            if d1 == d0 - 1:                      # descending edge
                tv = 1.0 - len(A1) / len(A0)
            elif d1 == d0:                        # disjoint nearest sets
                tv = 1.0
            else:
                continue                          # handled from the other end
            if tv < worst:
                worst, witness = tv, (s0, s1, i, d0, d1, len(A0), len(A1))
    return worst, witness


def structure_checks(n, C, H):
    """The parity facts the derivation rests on. Checked, not assumed."""
    ns = nearest_sets(n, C, H)
    inC = set(C)
    for s0 in range(1 << n):
        for i in range(n):
            s1 = s0 ^ (1 << i)
            d0, A0 = ns[s0]
            d1, A1 = ns[s1]
            # d(.,c) flips by exactly 1 for each FIXED centre c, but the
            # distance to the SET is a minimum and may be equal at both ends.
            if abs(d0 - d1) > 1:
                return f"distances differ by {abs(d0-d1)} on edge {s0}-{s1}"
            if d0 == d1:
                if set(A0) & set(A1):
                    return f"equal-distance edge {s0}-{s1} has overlapping N"
                b1 = (s1 >> i) & 1
                for c in A1:
                    if (c >> i) & 1 != b1:
                        return f"c in N(s1) disagrees with s1 on bit {i} (equal case)"
                for c in A0:
                    if (c >> i) & 1 != ((s0 >> i) & 1):
                        return f"c in N(s0) disagrees with s0 on bit {i} (equal case)"
            if d1 == d0 - 1:
                if not set(A1) <= set(A0):
                    return f"N(s1) not nested in N(s0) on edge {s0}-{s1}"
                b1 = (s1 >> i) & 1
                for c in A1:
                    if (c >> i) & 1 != b1:
                        return f"c in N(s1) disagrees with s1 on bit {i}"
                for c in set(A0) - set(A1):
                    if (c >> i) & 1 != ((s0 >> i) & 1):
                        return f"c in N(s0)\\N(s1) disagrees with s0 on bit {i}"
    return None


def prop12(n, C, H):
    """Proposition 12: every non-centre has >= 2 centres at its own distance."""
    ns = nearest_sets(n, C, H)
    return all(len(ns[s][1]) >= 2 for s in range(1 << n) if s not in set(C))


def code_cost(pi, H, C):
    return float(pi @ H[:, list(C)].min(axis=1))


def sweep(n, q_, Kmax=None, verbose=True):
    """Every K, every pi-optimal code, compare predicted vs measured margin."""
    N = 1 << n
    pi = prior(n, q_)
    H = hamming(n)
    rows = []
    for K in range(2, (Kmax or N) + 1):
        best = min(code_cost(pi, H, list(S)) for S in itertools.combinations(range(N), K))
        opt = [list(S) for S in itertools.combinations(range(N), K)
               if code_cost(pi, H, list(S)) <= best + TOL]
        for C in opt:
            err = structure_checks(n, C, H)
            if err:
                print(f"  !! STRUCTURE CHECK FAILED n={n} K={K} C={C}: {err}")
                sys.exit(1)
            pred, wit = predicted_margin(n, C, H)
            rec = spread_record(n, C, H)
            meas = float(margin(n, rec))
            D = float(distortion(n, pi, rec))
            if abs(pred - meas) > 1e-9:
                print(f"  !! FORMULA MISMATCH n={n} K={K} C={C}: "
                      f"predicted {pred:.6f} measured {meas:.6f}")
                sys.exit(1)
            if abs(D - best) > 1e-9:
                print(f"  !! construction did not attain D_0 at n={n} K={K}")
                sys.exit(1)
            rows.append(dict(n=n, q=q_, K=K, C=C, D0=best, margin=meas,
                             prop12=prop12(n, C, H),
                             maxdist=max(d for d, _ in nearest_sets(n, C, H)),
                             witness=wit))
    return rows


if __name__ == "__main__":
    ns = [int(a) for a in sys.argv[1:] if a.isdigit()] or [3, 4]
    QS = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.9]
    allrows, t0 = [], time.time()
    for n in ns:
        for q_ in QS:
            r = sweep(n, q_)
            allrows += r
            nopt = len(r)
            bad = [x for x in r if x["prop12"] and x["margin"] <= TOL]
            deep = [x for x in r if x["maxdist"] >= 2 and x["prop12"]]
            print(f"n={n} q={q_}: {nopt:5d} optimal codes checked, formula exact on all; "
                  f"{len(deep):4d} satisfy Prop 12 with radius >= 2; "
                  f"{len(bad):3d} COUNTEREXAMPLES")
            for x in bad[:3]:
                s0, s1, i, d0, d1, b, a = x["witness"]
                w = "0" + str(n) + "b"
                print(f"     K={x['K']} C={[format(c,w) for c in x['C']]}  "
                      f"dead edge {format(s0,w)}->{format(s1,w)} agent {i}: "
                      f"d {d0}->{d1}, nu {b}->{a}")
    print(f"\n{len(allrows)} (code, prior) pairs, {time.time()-t0:.1f}s")
    cx = [x for x in allrows if x["prop12"] and x["margin"] <= TOL]
    print(f"codes satisfying Prop 12 with radius >= 2: "
          f"{sum(1 for x in allrows if x['maxdist']>=2 and x['prop12'])}")
    print(f"COUNTEREXAMPLES (Prop 12 holds, construction has margin 0): {len(cx)}")
    p = out("general_prior_margin.json")
    def _clean(v):
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.floating,)):
            return float(v)
        if isinstance(v, (list, tuple)):
            return [_clean(z) for z in v]
        return v
    # Summarise rather than dumping all 47k rows. Every row is compared against
    # the Theorem 3 LP and against D_0 as it is generated, and the run exits
    # non-zero on the first mismatch -- so reaching this line already means all
    # of them passed, and a per-row dump is 14MB that nothing reads. What is
    # worth keeping is the coverage per prior and any code that fails, of which
    # there are none. Use --full to write the per-row dump locally instead.
    summary = {}
    for x in allrows:
        s = summary.setdefault(f"n={x['n']} q={x['q']}",
                               dict(n=x["n"], q=x["q"], optimal_codes=0,
                                    prop12_radius_ge2=0, counterexamples=0,
                                    K_flat=None, min_margin_over_prop12=1.0))
        s["optimal_codes"] += 1
        if x["prop12"]:
            if x["maxdist"] >= 2:
                s["prop12_radius_ge2"] += 1
            if x["margin"] <= TOL:
                s["counterexamples"] += 1
            elif s["K_flat"] is None:
                s["K_flat"] = x["K"]
            s["min_margin_over_prop12"] = min(s["min_margin_over_prop12"],
                                              x["margin"])
    json.dump(_clean(dict(
        summary=summary,
        codes_checked=len(allrows),
        formula_matched_the_LP_on_every_code=True,
        construction_attained_D0_on_every_code=True,
        counterexamples=len(cx),
        witnesses=[{k: v for k, v in x.items()} for x in cx],
        seconds=round(time.time() - t0, 1))), open(p, "w"), indent=1)
    print(f"wrote {p}")
    if "--full" in sys.argv:
        pf = out("general_prior_margin_full.json")
        json.dump(_clean([dict(x) for x in allrows]), open(pf, "w"), indent=1)
        print(f"wrote {pf}  (per-row dump; not part of the archive)")
