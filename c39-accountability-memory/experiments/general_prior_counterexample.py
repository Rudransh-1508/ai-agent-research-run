"""Phase 1, part 2: is Proposition 12 SUFFICIENT for the construction to work?

    python experiments/general_prior_counterexample.py

Part 1 (general_prior_margin.py) established, and verified on 47,017 codes, that
the generalised construction has margin exactly

    gamma = 1 - max over descending edges of nu(s_1)/nu(s_0)

so gamma > 0 iff nu strictly decreases along every edge that moves closer to C.
Proposition 12 only gives nu >= 2. The two differ once the covering radius is
>= 2. The question is whether the gap is real.

Part 1 searched pi-optimal codes under PRODUCT Bernoulli priors and found none.
That is weak evidence: product priors admit few optimal codes of radius >= 2.
The paper's claim is about ANY full-support prior, so this script does the
search properly, in two stages:

  STAGE A (combinatorics). Over all codes, find C with nu >= 2 everywhere and a
  descending edge on which nu does NOT strictly decrease. Does the configuration
  exist at all, ignoring optimality?

  STAGE B (realisability). For each such C, ask an LP whether some full-support
  prior pi makes C a pi-optimal K-median code:

      find pi > 0, sum pi = 1, with  <pi, cost(C)> <= <pi, cost(C')>
      for every other K-subset C'.

  Strict positivity is imposed as pi >= eps and then rescaled, so a feasible
  point is a genuine full-support prior, not a degenerate limit.

If Stage B returns a prior, Proposition 12 is NOT sufficient and the question
closes negatively. If Stage A is empty, Proposition 12 IS sufficient and the
question closes positively.
"""
import json, sys, itertools, time
import numpy as np
from scipy.optimize import linprog
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from c39.paths import out
from experiment_agents import popcount, margin, distortion

TOL = 1e-9


def hamming(n):
    N = 1 << n
    return np.array([[popcount(a ^ b) for b in range(N)] for a in range(N)])


def nu_and_dist(n, C, H):
    """(distance to C, nearest-centre count) for every vertex; centres get (0,1)."""
    inC = set(C)
    d = H[:, list(C)].min(axis=1)
    nu = (H[:, list(C)] == d[:, None]).sum(axis=1)
    for c in C:
        nu[c] = 1
    return d, nu


def diagnose(n, C, H):
    """Returns (prop12_holds, gamma_predicted, witness_edge_or_None)."""
    inC = set(C)
    d, nu = nu_and_dist(n, C, H)
    p12 = all(nu[s] >= 2 for s in range(1 << n) if s not in inC)
    worst, wit = 1.0, None
    for s0 in range(1 << n):
        for i in range(n):
            s1 = s0 ^ (1 << i)
            if d[s1] == d[s0] - 1:
                tv = 1.0 - nu[s1] / nu[s0]
                if tv < worst:
                    worst, wit = tv, (s0, s1, i, int(d[s0]), int(d[s1]),
                                      int(nu[s0]), int(nu[s1]))
    return p12, float(worst), wit


def stage_a(n, Kmax=None):
    """All codes: nu >= 2 everywhere, but some descending edge keeps nu constant."""
    N = 1 << n
    H = hamming(n)
    hits = []
    for K in range(2, (Kmax or N) + 1):
        for S in itertools.combinations(range(N), K):
            C = list(S)
            d, nu = nu_and_dist(n, C, H)
            if d.max() < 2:
                continue                      # radius 1: Lemma 8 already covers it
            inC = set(C)
            if any(nu[s] < 2 for s in range(N) if s not in inC):
                continue                      # Prop 12 fails, not a candidate
            p12, g, wit = diagnose(n, C, H)
            if g <= TOL:
                hits.append((C, g, wit))
    return hits


def realisable(n, C, H, eps=1e-4):
    """Is there a full-support pi making C a pi-optimal |C|-median code?"""
    N = 1 << n
    K = len(C)
    cost_C = H[:, list(C)].min(axis=1).astype(float)
    rows = []
    for S in itertools.combinations(range(N), K):
        if list(S) == sorted(C):
            continue
        rows.append(cost_C - H[:, list(S)].min(axis=1).astype(float))
    A_ub = np.array(rows)                     # <pi, cost_C - cost_C'> <= 0
    b_ub = np.zeros(len(rows))
    res = linprog(np.zeros(N), A_ub=A_ub, b_ub=b_ub,
                  A_eq=np.ones((1, N)), b_eq=[1.0],
                  bounds=[(eps, None)] * N, method="highs")
    return (res.x if res.status == 0 else None), res.status


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    H = hamming(n)
    t0 = time.time()
    print(f"STAGE A  n={n}: searching every code for Prop 12 + a non-decreasing "
          f"descending edge")
    hits = stage_a(n)
    print(f"  {len(hits)} configurations found in {time.time()-t0:.1f}s")
    w = "0" + str(n) + "b"
    for C, g, wit in hits[:6]:
        s0, s1, i, d0, d1, nu0, nu1 = wit
        print(f"   C={[format(c,w) for c in C]}  gamma={g:.4f}  "
              f"dead edge {format(s0,w)}->{format(s1,w)} agent {i}: "
              f"d {d0}->{d1}, nu {nu0}->{nu1}")

    if not hits:
        print("\n=> Proposition 12 IS sufficient at this n: no configuration exists.")
        sys.exit(0)

    print(f"\nSTAGE B  n={n}: is any of them pi-optimal for a full-support prior?")
    found = []
    for C, g, wit in hits:
        pi, status = realisable(n, C, H)
        if pi is not None:
            # confirm independently: measure the construction, do not trust the LP
            idx = {c: j for j, c in enumerate(C)}
            d = H[:, list(C)].min(axis=1)
            q = np.zeros((1 << n, len(C)))
            for s in range(1 << n):
                nr = [c for c in C if H[s][c] == d[s]]
                if s in set(C):
                    nr = [s]
                for c in nr:
                    q[s, idx[c]] = 1.0 / len(nr)
            D = float(distortion(n, pi, q))
            D0 = float(pi @ d)
            gm = float(margin(n, q))
            found.append(dict(C=[int(c) for c in C], pi=[float(x) for x in pi],
                              D=D, D0=D0, gamma_measured=gm,
                              gamma_predicted=g, witness=[int(z) for z in wit]))
            print(f"   REALISABLE  C={[format(c,w) for c in C]}")
            print(f"     min pi = {pi.min():.3e} (full support), D = {D:.6f}, "
                  f"D_0 = {D0:.6f}, gamma measured = {gm:.6f}")
            if len(found) >= 3:
                break
    print(f"\n  {len(found)} of {len(hits)} configurations are pi-optimal for some "
          f"full-support prior")
    p = out(f"general_prior_counterexample_n{n}.json")
    json.dump(dict(n=n, stage_a=len(hits), realisable=len(found), found=found,
                   seconds=round(time.time() - t0, 1)), open(p, "w", newline="\n"), indent=1)
    print(f"wrote {p}")
