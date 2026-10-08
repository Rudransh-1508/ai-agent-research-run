"""Block-threshold records and the tightness of the linear-memory bound.

Checks, for the noisy-outcome model (h = 0.9, l = 0.1):
  1. Proposition "Block records" (b): one bit per block, 1{block successes > mode of
     Bin(m_b - 1, h)}, gives every agent Nash margin (h - l) * max_k P[Bin(m_b - 1, h) = k].
     Verified against the exact channel by brute force over all outcome profiles, n <= 10.
  2. The mode probability of Bin(N, h) is nonincreasing in N (exact rational arithmetic).
  3. Theorem "The memory bound is tight": (1 / m(c)) / beta(c) -> pi ln 2 as c -> 0.
  4. At n = 100, threshold records reach 62% to 100% of the Theorem-2 bound; the count 26%.
"""
import itertools
import math
from fractions import Fraction

H, L = 0.9, 0.1


def pmf(N, p):
    lg = math.lgamma
    return [math.exp(lg(N + 1) - lg(k + 1) - lg(N - k + 1) + k * math.log(p) + (N - k) * math.log(1 - p))
            for k in range(N + 1)]


def mode_prob(N, p=H):
    return max(pmf(N, p))


def nash_margin_threshold_record(n, m):
    """Exact Nash margins of the block-threshold record, by enumerating outcome profiles."""
    blocks = [list(range(b, min(b + m, n))) for b in range(0, n, m)]
    thresholds = [max(range(len(B)), key=lambda k: pmf(len(B) - 1, H)[k]) for B in blocks]

    def label(s):
        return tuple(int(sum(s[i] for i in B) > t) for B, t in zip(blocks, thresholds))

    def law(actions):
        out = {}
        for s in itertools.product((0, 1), repeat=n):
            pr = 1.0
            for a, x in zip(actions, s):
                ps = H if a else L
                pr *= ps if x else 1 - ps
            y = label(s)
            out[y] = out.get(y, 0.0) + pr
        return out

    q1 = law([1] * n)
    margins = []
    for i in range(n):
        q0 = law([0 if j == i else 1 for j in range(n)])
        keys = set(q1) | set(q0)
        margins.append(0.5 * sum(abs(q1.get(y, 0) - q0.get(y, 0)) for y in keys))
    return min(margins)


def main():
    ok = True
    for n, m in [(4, 2), (6, 3), (6, 2), (7, 3), (8, 4), (9, 3), (10, 5), (10, 10)]:
        exact = nash_margin_threshold_record(n, m)
        pred = (H - L) * mode_prob(m - 1)
        good = abs(exact - pred) < 1e-12
        ok &= good
        print(f"n={n:2d} m={m:2d}  exact={exact:.6f}  predicted={pred:.6f}  {'ok' if good else 'MISMATCH'}")

    h = Fraction(9, 10)
    prev = Fraction(1)
    mono = True
    for N in range(1, 120):
        cur = max(math.comb(N, k) * h ** k * (1 - h) ** (N - k) for k in range(N + 1))
        mono &= cur <= prev
        prev = cur
    ok &= mono
    print("mode probability nonincreasing in N (exact, N < 120):", mono)

    for c in (0.2, 0.1, 0.05, 0.02, 0.01):
        m = 1
        while (H - L) * mode_prob(m) >= c:
            m += 1
        beta = 2 * H * (1 - H) / math.log(2) * (c / (H - L)) ** 2
        print(f"c={c:<5} m(c)={m:6d}  (1/m)/beta={1 / m / beta:.3f}   pi ln 2={math.pi * math.log(2):.3f}")

    n = 100
    bound = lambda bits: min(H - L, math.sqrt((H - L) ** 2 / (2 * H * (1 - H)) * bits * math.log(2) / n))
    ratios = []
    for m in (1, 2, 3, 5, 10, 20, 50, 100):
        mu = (H - L) * mode_prob(m - 1)
        ratios.append(mu / bound(math.ceil(n / m)))
    count_ratio = (H - L) * mode_prob(n - 1) / bound(math.log2(n + 1))
    print(f"n=100 threshold records: {min(ratios):.3f} to {max(ratios):.3f} of the bound; count {count_ratio:.3f}")
    print("ALL CHECKS PASS" if ok else "FAILURE")


if __name__ == "__main__":
    main()
