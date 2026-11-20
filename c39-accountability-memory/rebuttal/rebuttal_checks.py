"""Numerical sanity checks for claims proposed in the AAMAS 2027 rebuttal (Submission 3289).

A. Generalised Theorem 2: heterogeneous, non-binary outcomes, exogenous common shock Z with
   outcomes conditionally independent given Z.  Claim: sum_i mu_i^2 / chi2_i <= H(Y)/2,
   chi2_i = E_Z chi2(G_i(.|Z) || F_i(.|Z)).  Reduces to the paper's constant in the binary case.
B. Budget-balanced margin is positive iff every d_i != 0 and the d_i are not all positive
   multiples of one vector (Farkas).  Bounded payments in [0,1], sum_i p_i(y) = B.
C. Dominant-strategy margin of a block-count record under noise scales like 1/m.
"""
import itertools
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261121)


def H(p):
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def tv(a, b):
    return 0.5 * float(np.abs(a - b).sum())


def chi2(g, f):
    return float(((g - f) ** 2 / f).sum())


# ---------------------------------------------------------------- A
def check_A(trials=4000):
    worst = 0.0
    for t in range(trials):
        n = int(rng.integers(2, 5))
        A = int(rng.integers(2, 4))          # outcome alphabet size
        nz = int(rng.integers(1, 4))         # common-shock support size (1 = independent)
        K = int(rng.integers(2, 7))
        sees_z = bool(rng.integers(0, 2))
        rz = rng.dirichlet(np.ones(nz))
        F = rng.dirichlet(np.ones(A), size=(n, nz))   # work law of S_i given z
        G = rng.dirichlet(np.ones(A), size=(n, nz))   # shirk law of S_i given z
        if t % 4 == 0:                                # near-adversarial: G close to F
            G = 0.8 * F + 0.2 * G
        profiles = list(itertools.product(range(A), repeat=n))
        q = rng.dirichlet(np.ones(K) * rng.choice([0.2, 1.0]), size=(len(profiles), nz if sees_z else 1))
        if t % 5 == 0:                                # some deterministic records
            q = np.eye(K)[rng.integers(0, K, size=(len(profiles), q.shape[1]))]

        def law_Y(dev=None):
            out = np.zeros(K)
            for z in range(nz):
                for idx, s in enumerate(profiles):
                    pr = rz[z]
                    for i in range(n):
                        pr *= (G if i == dev else F)[i, z, s[i]]
                    out += pr * q[idx, z if sees_z else 0]
            return out

        Q1 = law_Y()
        lhs = 0.0
        for i in range(n):
            mu = tv(Q1, law_Y(dev=i))
            c2 = sum(rz[z] * chi2(G[i, z], F[i, z]) for z in range(nz))
            lhs += mu ** 2 / c2
        ratio = lhs / (H(Q1) / 2) if H(Q1) > 0 else (0.0 if lhs < 1e-12 else np.inf)
        worst = max(worst, ratio)
    # binary homogeneous independent case reproduces the paper's constant
    h, l = 0.9, 0.1
    paper = (h - l) ** 2 / (2 * h * (1 - h))
    ours = chi2(np.array([l, 1 - l]), np.array([h, 1 - h])) / 2
    return worst, paper, ours


# ---------------------------------------------------------------- B
def bb_margin(d):
    """max t s.t. p_i in [0,1]^K, sum_i p_i = B*1, <p_i,d_i> >= t.  Vars: p (n*K), B, t."""
    n, K = d.shape
    nv = n * K + 2
    c = np.zeros(nv); c[-1] = -1.0
    A_ub, b_ub = [], []
    for i in range(n):
        row = np.zeros(nv); row[i * K:(i + 1) * K] = -d[i]; row[-1] = 1.0
        A_ub.append(row); b_ub.append(0.0)
    A_eq, b_eq = [], []
    for y in range(K):
        row = np.zeros(nv)
        for i in range(n):
            row[i * K + y] = 1.0
        row[-2] = -1.0
        A_eq.append(row); b_eq.append(0.0)
    bounds = [(0, 1)] * (n * K) + [(0, n), (None, None)]
    r = linprog(c, A_ub=np.array(A_ub), b_ub=b_ub, A_eq=np.array(A_eq), b_eq=b_eq, bounds=bounds, method="highs")
    return -r.fun


def zero_sum(K):
    v = rng.normal(size=K)
    return v - v.mean()


def predicted_positive(d, tol=1e-9):
    """Claim: positive BB margin iff every d_i != 0 and not all d_i are positive multiples
    of one vector.  (With K = 2 all zero-sum vectors are collinear, so only signs matter.)"""
    if np.any(np.linalg.norm(d, axis=1) < tol):
        return False
    u = d[0] / np.linalg.norm(d[0])
    return any(np.linalg.norm(v / np.linalg.norm(v) - u) > 1e-7 for v in d[1:])


def check_B(trials=3000):
    mismatches, counts = 0, {True: 0, False: 0}
    for t in range(trials):
        n, K = int(rng.integers(2, 6)), int(rng.integers(2, 7))
        z = zero_sum(K)
        kind = t % 4
        if kind == 0:     # generic
            d = np.array([zero_sum(K) for _ in range(n)])
        elif kind == 1:   # all positively collinear (e.g. any symmetric record)
            d = np.array([rng.uniform(0.1, 2) * z for _ in range(n)])
        elif kind == 2:   # collinear with mixed signs
            d = np.array([rng.uniform(0.1, 2) * z * rng.choice([-1, 1]) for _ in range(n)])
        else:             # one undetectable agent
            d = np.array([zero_sum(K) for _ in range(n)]); d[int(rng.integers(n))] = 0
        p = predicted_positive(d)
        counts[p] += 1
        mismatches += (bb_margin(d) > 1e-9) != p
    return counts, mismatches


# ---------------------------------------------------------------- C
def binom_pmf(N, p):
    from scipy.stats import binom
    return binom.pmf(np.arange(N + 1), N, p)


def ds_margin_count(m, h, l):
    """DS margin for one agent under a block count of size m with noise (h,l).
    By symmetry teammates matter only through j = number of working block-mates."""
    from numpy import convolve
    vecs = []
    for j in range(m):
        X = convolve(binom_pmf(j, h), binom_pmf(m - 1 - j, l))       # support 0..m-1
        work = convolve(X, [1 - h, h]); shirk = convolve(X, [1 - l, l])
        vecs.append(work - shirk)                                      # support 0..m
    D = np.array(vecs).T                                               # (m+1) x m
    K = D.shape[0]
    # min_lambda 0.5 * sum |D lambda|  -> vars lambda (m), u (K)
    nv = m + K
    c = np.r_[np.zeros(m), 0.5 * np.ones(K)]
    A_ub = np.block([[D, -np.eye(K)], [-D, -np.eye(K)]])
    b_ub = np.zeros(2 * K)
    A_eq = np.r_[np.ones(m), np.zeros(K)][None, :]
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1], bounds=[(0, None)] * nv, method="highs")
    return r.fun


if __name__ == "__main__":
    worst, paper, ours = check_A()
    print(f"A  max over random instances of [sum mu_i^2/chi2_i] / [H(Y)/2] = {worst:.4f} (claim <= 1)")
    print(f"A  binary constant: paper {paper:.6f}, chi2/2 {ours:.6f}")
    counts, bad = check_B()
    print(f"B  predicted positive/zero: {counts}, mismatches with the LP: {bad} (claim 0)")
    h, l = 0.9, 0.1
    print("C  m, DS margin of block count, m*margin   (paper: count n=5 DS = 0.1600)")
    for m in [2, 3, 5, 8, 10, 15, 20, 30, 40, 60, 80]:
        mu = ds_margin_count(m, h, l)
        print(f"   {m:3d}  {mu:.4f}  {m * mu:.3f}")
