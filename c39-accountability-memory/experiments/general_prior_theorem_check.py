"""Phase 1, part 4: the sufficiency theorem, and its proof step, checked.

    python experiments/general_prior_theorem_check.py

THEOREM (sufficiency, any full-support prior).
Let C be a code with nu(s) >= 2 for every non-centre s, where nu(s) is the
number of centres at distance d(s,C). Then along every edge (s_0, s_1) with
d(s_1,C) = d(s_0,C) - 1 we have nu(s_1) < nu(s_0); hence the construction

    q[s,.] = Unif(N(s)),   p_i[y] = (centre of y)_i

attains D = D_0(K) with margin gamma = 1 - max nu(s_1)/nu(s_0) > 0.

PROOF. If s_1 in C then nu(s_1) = 1 < 2 <= nu(s_0). Otherwise r := d(s_0,C) >= 2.
Always N(s_1) subset-of N(s_0); suppose they are equal. Translate s_0 to 0^n and
permute so the flipped coordinate is 0, so s_1 = e_0 and no centre has weight
< r. Then N(0^n) is the set of ALL weight-r centres, while N(e_0) is the set of
weight-r centres carrying bit 0; equality forces every weight-r centre to carry
bit 0. Pick any c in N(0^n) and set y = c XOR e_0, of weight r-1 >= 1, so y is
not a centre. A centre at distance 1 from y is y XOR e_m of weight r-1 +/- 1;
weight r-2 is excluded, so it has weight r and therefore carries bit 0, forcing
m = 0 and the centre to be c itself. So nu(y) = 1, contradicting the hypothesis.

This script checks the three load-bearing claims by direct computation:
  (i)   N(s_1) is always a subset of N(s_0) on a descending edge
  (ii)  nu >= 2 everywhere  =>  nu strictly decreases on every descending edge
  (iii) the closed-form margin equals the Theorem 3 margin, and D = D_0(K)
on random codes at n = 3..7, where exhaustive enumeration is impossible.
"""
import sys, json, time
import numpy as np
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from c39.paths import out
from experiment_agents import popcount, margin, distortion

SEED = 20260915


def analyse(n, C, H):
    N = 1 << n
    inC = set(C)
    cols = H[:, list(C)]
    d = cols.min(axis=1)
    nu = (cols == d[:, None]).sum(axis=1)
    for c in C:
        nu[c] = 1
    Nsets = []
    for s in range(N):
        Nsets.append({s} if s in inC else
                     {C[j] for j in range(len(C)) if cols[s, j] == d[s]})
    return d, nu, Nsets


def main(seed=SEED, trials_per_n=4000):
    rng = np.random.default_rng(seed)
    stats = {}
    t0 = time.time()
    for n in (3, 4, 5, 6, 7):
        N = 1 << n
        H = np.array([[popcount(a ^ b) for b in range(N)] for a in range(N)])
        n_p12 = n_nested = n_strict = n_margin = 0
        viol = []
        for _ in range(trials_per_n):
            K = int(rng.integers(2, N))
            C = sorted(rng.choice(N, size=K, replace=False).tolist())
            d, nu, Nsets = analyse(n, C, H)
            inC = set(C)

            # (i) nesting on descending edges -- claimed for EVERY code
            for s0 in range(N):
                for i in range(n):
                    s1 = s0 ^ (1 << i)
                    if d[s1] == d[s0] - 1 and not Nsets[s1] <= Nsets[s0]:
                        viol.append(("nesting", n, C, s0, s1))
                    if d[s1] == d[s0] and Nsets[s1] & Nsets[s0]:
                        viol.append(("disjointness", n, C, s0, s1))
            n_nested += 1

            if any(nu[s] < 2 for s in range(N) if s not in inC):
                continue
            n_p12 += 1

            # (ii) Prop 12 => strict decrease
            ok = True
            worst = 1.0
            for s0 in range(N):
                for i in range(n):
                    s1 = s0 ^ (1 << i)
                    if d[s1] == d[s0] - 1:
                        if nu[s1] >= nu[s0]:
                            ok = False
                            viol.append(("strict", n, C, s0, s1,
                                         int(nu[s0]), int(nu[s1])))
                        worst = min(worst, 1.0 - nu[s1] / nu[s0])
            if ok:
                n_strict += 1

            # (iii) closed form == Theorem 3 margin, and D = D_0, on a few
            if n <= 5 and n_margin < 250:
                idx = {c: j for j, c in enumerate(C)}
                q = np.zeros((N, K))
                for s in range(N):
                    for c in Nsets[s]:
                        q[s, idx[c]] = 1.0 / len(Nsets[s])
                pi = rng.dirichlet(np.ones(N) * 0.7)     # a random full-support prior
                pi = np.maximum(pi, 1e-9)
                pi /= pi.sum()
                g = float(margin(n, q))
                D = float(distortion(n, pi, q))
                D0 = float(pi @ d)
                if abs(g - worst) > 1e-9:
                    viol.append(("formula", n, C, g, worst))
                elif abs(D - D0) > 1e-9:
                    viol.append(("D0", n, C, D, D0))
                else:
                    n_margin += 1

        stats[n] = dict(codes=trials_per_n, satisfy_prop12=n_p12,
                        strict_decrease=n_strict, margin_checked=n_margin)
        print(f"n={n}: {trials_per_n} random codes | "
              f"{n_p12} satisfy Prop 12 | {n_strict} of those show strict "
              f"decrease on every descending edge | "
              f"{n_margin} closed-form/D_0 checks")
    dt = time.time() - t0
    print(f"\nviolations of any kind: {len(viol)}")
    for v in viol[:5]:
        print("   ", v)
    ok = not viol
    print(f"\n{'ALL CLAIMS HELD' if ok else 'A CLAIM FAILED'}  ({dt:.1f}s)")
    p = out("general_prior_theorem_check.json")
    json.dump(dict(seed=seed, per_n=stats, violations=len(viol),
                   seconds=round(dt, 1)), open(p, "w", newline="\n"), indent=1)
    print(f"wrote {p}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
