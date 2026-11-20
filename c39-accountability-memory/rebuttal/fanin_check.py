"""Rebuttal check D: interdependent production with bounded fan-in.

Outcomes S_1..S_m; outcome j's law depends on the efforts of its parent agents Pa(j), and
outcomes are independent given actions.  Agent i's deviation changes the laws of its children
N(i) = {j : i in Pa(j)}.  Let d = max_j |Pa(j)| (fan-in) and
chi2_i = chi2(law of S_{N(i)} if i shirks || if all work) = prod_{j in N(i)} (1 + chi2_j) - 1.
Claim:   sum_i mu_i^2 / chi2_i  <=  d * H(Y) / 2.
Proof:   mu_i^2 <= chi2_i I(Y; S_{N(i)}) / 2 (Cauchy-Schwarz + Pinsker, as before), and with
         independent S, A -> I(Y; S_A) is monotone supermodular with value 0 at the empty set,
         so a family covering each outcome at most d times has sum_i I(Y; S_{N(i)}) <= d I(Y; S).
d = 1 is Theorem 2 (each outcome has one owner); one outcome driven by all n agents gives d = n,
consistent with a single "pipeline passed" bit detecting every deviation.
"""
import itertools
import numpy as np

rng = np.random.default_rng(7)


def H(p):
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def run(trials=3000):
    worst, worst_super = 0.0, 0.0
    for t in range(trials):
        n = int(rng.integers(2, 5)); m = int(rng.integers(2, 6)); K = int(rng.integers(2, 7))
        pa = []
        for j in range(m):
            k = int(rng.integers(1, n + 1)) if t % 3 else 1
            pa.append(sorted(rng.choice(n, size=k, replace=False).tolist()))
        for i in range(n):                       # make sure every agent affects something
            if not any(i in p for p in pa):
                pa[int(rng.integers(m))].append(i)
        d = max(len(p) for p in pa)
        # success prob of outcome j given number of shirking parents (any monotone-ish table)
        theta = [np.sort(rng.uniform(0.05, 0.95, size=len(p) + 1))[::-1] for p in pa]
        profiles = list(itertools.product([0, 1], repeat=m))
        q = rng.dirichlet(np.ones(K) * rng.choice([0.2, 1.0]), size=len(profiles))
        if t % 4 == 0:
            q = np.eye(K)[rng.integers(0, K, size=len(profiles))]

        def p_success(shirker):
            return np.array([theta[j][1 if shirker in pa[j] else 0] for j in range(m)])

        def law_S(shirker=None):
            ps = p_success(shirker)
            return np.array([np.prod([ps[j] if s[j] else 1 - ps[j] for j in range(m)]) for s in profiles])

        PS = law_S(); Q1 = PS @ q
        HY = H(Q1)
        lhs, sum_I = 0.0, 0.0
        for i in range(n):
            mu = 0.5 * np.abs(Q1 - law_S(i) @ q).sum()
            ch = [j for j in range(m) if i in pa[j]]
            p1, p0 = p_success(None), p_success(i)
            c2 = np.prod([1 + (p0[j] - p1[j]) ** 2 / (p1[j] * (1 - p1[j])) for j in ch]) - 1
            lhs += mu ** 2 / c2
            # I(Y; S_ch) under all-work
            idx = {}
            for k, s in enumerate(profiles):
                idx.setdefault(tuple(s[j] for j in ch), []).append(k)
            I = HY
            for ks in idx.values():
                w = PS[ks].sum()
                I -= w * H((PS[ks] @ q[ks]) / w)
            sum_I += I
        IYS = HY - sum(PS[k] * H(q[k]) for k in range(len(profiles)))
        worst = max(worst, lhs / (d * HY / 2) if HY > 1e-12 else 0.0)
        worst_super = max(worst_super, sum_I / (d * IYS) if IYS > 1e-12 else 0.0)
    return worst, worst_super


if __name__ == "__main__":
    w, s = run()
    print(f"D  max [sum mu_i^2/chi2_i] / [d H(Y)/2]        = {w:.6f} (claim <= 1)")
    print(f"D  max [sum_i I(Y;S_N(i))] / [d I(Y;S)]         = {s:.12f} (claim <= 1; "
          f"equality is attained when d = 1, so expect 1 up to float rounding)")
    assert w <= 1 + 1e-9 and s <= 1 + 1e-9
