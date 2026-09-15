"""One-command, SOLVER-FREE verification of every claim the paper makes.

    python verify_all.py

No LP, no MILP, no search: the MILP-derived witnesses are read from
certified_codes.json (produced once by make_certificates.py) and re-checked
here from scratch. Everything else is recomputed by direct enumeration.

Exit code 0 iff every check passes.
"""
import json, math, sys
import itertools
from itertools import combinations
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out

FAILS = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAILS.append(name)


# ----------------------------------------------------------------- helpers
def popcount(x):
    return bin(x).count("1")


def neighbours(n):
    return [[v ^ (1 << i) for i in range(n)] for v in range(1 << n)]


def is_2_dominating(n, C):
    inC = [False] * (1 << n)
    for c in C:
        inC[c] = True
    nb = neighbours(n)
    return all(sum(inC[u] for u in nb[v]) >= 2 for v in range(1 << n) if not inC[v])


def min_centre_degree(n, C):
    inC = [False] * (1 << n)
    for c in C:
        inC[c] = True
    nb = neighbours(n)
    degs = [sum(inC[u] for u in nb[v]) for v in range(1 << n) if not inC[v]]
    return min(degs) if degs else None


# ============================================ A. gamma_2 by full enumeration
def gamma2_bruteforce(n):
    """Smallest 2-dominating set, by enumerating every subset by size."""
    N = 1 << n
    for K in range(1, N + 1):
        for C in combinations(range(N), K):
            if is_2_dominating(n, C):
                return K
    return None


print("\nA. gamma_2(Q_n) by complete enumeration of all subsets")
EXPECTED_SMALL = {1: 2, 2: 2, 3: 4, 4: 7}
for n, want in EXPECTED_SMALL.items():
    got = gamma2_bruteforce(n)
    check(f"gamma_2(Q_{n}) = {want}", got == want, f"got {got}")


# ======================================= B. the flat records, built and checked
def flat_record(n, C):
    """Build the Lemma-sufficiency record and return (D, margin, d_min).

    q[c]   = point mass on c
    q[t]   = uniform over N(t) ^ C
    p_i[y] = i-th bit of the centre labelled y
    Reconstruction: label y -> its centre. All computed exactly, no solver.
    """
    N = 1 << n
    nb = neighbours(n)
    inC = [False] * N
    for c in C:
        inC[c] = True
    centres = sorted(C)
    label = {c: j for j, c in enumerate(centres)}

    # encoder as a dict state -> {label: prob}
    q = {}
    for s in range(N):
        if inC[s]:
            q[s] = {label[s]: 1.0}
        else:
            nbrs = [u for u in nb[s] if inC[u]]
            q[s] = {label[u]: 1.0 / len(nbrs) for u in nbrs}

    # reconstruction distortion
    D = 0.0
    for s in range(N):
        for y, p in q[s].items():
            D += p * bin(s ^ centres[y]).count("1")
    D /= N

    # all-teammate-profile unilateral margin
    margin = math.inf
    for i in range(n):
        bit = [(centres[y] >> i) & 1 for y in range(len(centres))]
        for s0 in range(N):
            if (s0 >> i) & 1:
                continue
            s1 = s0 | (1 << i)
            v = sum(p * bit[y] for y, p in q[s1].items()) \
                - sum(p * bit[y] for y, p in q[s0].items())
            margin = min(margin, v)
    return D, margin, min_centre_degree(n, C)


print("\nB. flat records: D = D_0(K) and margin = 1 - 1/d_min, solver-free")
try:
    CERT = json.load(open(data("certified_codes.json")))["codes"]
except FileNotFoundError:
    print("  certified_codes.json missing -- run make_certificates.py first")
    sys.exit(1)

for key in sorted(CERT, key=lambda k: int(k[1:])):
    rec = CERT[key]
    n, K, C = rec["n"], rec["K"], rec["centres"]
    N = 1 << n
    ok_dom = is_2_dominating(n, C)
    D, margin, dmin = flat_record(n, C)
    D0 = (N - K) / N
    check(f"n={n} K={K}: C is 2-dominating", ok_dom)
    check(f"n={n} K={K}: D = D_0(K) = {D0}", abs(D - D0) < 1e-12,
          f"D={D:.12f}")
    check(f"n={n} K={K}: margin = 1 - 1/d_min", abs(margin - (1 - 1 / dmin)) < 1e-12,
          f"margin={margin:.6f}  d_min={dmin}")
    check(f"n={n} K={K}: margin >= 1/2", margin >= 0.5 - 1e-12)

print("\n   (D_0(K) >= (2^n - K)/2^n for every record: with K labels at most K")
print("    profiles are reconstructed exactly and each of the rest costs >= 1 bit,")
print("    so these records are optimal and the equality above is meaningful.)")


# ======================================================= C. the shell bound
def shell_lower(n, K):
    """Minimum of 2^n * D over records of size K forced by shell counting."""
    N = 1 << n
    remaining, total, r = N, 0, 0
    while remaining > 0:
        cap = N if r == 0 else (K * math.comb(n, r)) // 2
        if r == 0:
            cap = K                       # only the K centres are error-free
        take = min(remaining, cap)
        total += take * r
        remaining -= take
        r += 1
        if r > n:
            break
    return total


print("\nC. shell counting bound")
for n, K, ND0 in [(3, 4, 4), (5, 10, 22), (7, 32, 96)]:
    lb = shell_lower(n, K)
    check(f"does not exclude the flat point n={n} K={K}", lb <= ND0,
          f"shell_lower={lb}  N*D0={ND0}")

for n, kmax in [(3, 3), (5, 9), (7, 28), (9, 93)]:
    N = 1 << n
    bad = [K for K in range(2, kmax + 1) if shell_lower(n, K) <= N - K]
    check(f"n={n}: shell bound excludes every K <= {kmax}", not bad,
          f"survivors {bad}" if bad else "")


# ============================================ D. the one-bit frontier, achievability
def M_n(n):
    return sum(math.comb(n, k) * min(k, n - k) for k in range(n + 1)) / 2 ** n


def onebit_D(n, gamma):
    """D of the conjectured optimal one-bit record, antipodal decoding."""
    N = 1 << n
    tot = 0.0
    for s in range(N):
        w = bin(s).count("1")
        q = gamma * w + (1 - n * gamma) * (1 if w > n / 2 else 0)
        # decoder: label 1 -> all-ones, label 0 -> all-zeros
        tot += q * (n - w) + (1 - q) * w
    return tot / N


print("\nD. one-bit frontier: closed form vs the explicit record")
for n in [3, 5, 7, 9]:
    m = M_n(n)
    worst = 0.0
    for j in range(5):
        g = (j / 4) * (1 / n)
        closed = m + n * g * ((n - 1) / 2 - m)
        worst = max(worst, abs(onebit_D(n, g) - closed))
    check(f"n={n}: D(q_opt) matches M_n + n*gamma*((n-1)/2 - M_n)", worst < 1e-12,
          f"M_n={m:.6f}  max dev={worst:.2e}")


# ===================== E. decoder-pair minimisation (Theorem 1, step 5)
#
# For K = 2 the objective splits as
#     D(q; a,b) = E[d_H(S,a)] + E[q(S) * Delta(S)],   Delta(s) = d_H(s,b) - d_H(s,a),
# and on the feasible set q(s) = gamma*|s| + r(s) with 0 <= r <= 1 - n*gamma this
# gives, using the BOX constraint alone,
#     D >= n/2 + gamma*E[|S| Delta] + (1 - n*gamma) * E[min(Delta, 0)]  =:  LB(a,b).
# The block checks that LB is minimised by the antipodal pair, that the minimum
# equals the closed form of Theorem 1, and that the minimiser is feasible
# (monotone) there -- so the bound is attained, not merely valid.

def _delta(n, a, b):
    return [popcount(s ^ b) - popcount(s ^ a) for s in range(1 << n)]


def lower_bound_pair(n, gamma, a, b):
    N = 1 << n
    d = _delta(n, a, b)
    base = sum(popcount(s ^ a) for s in range(N)) / N
    t1 = sum(popcount(s) * d[s] for s in range(N)) / N
    t2 = sum(min(d[s], 0) for s in range(N)) / N
    return base + gamma * t1 + (1 - n * gamma) * t2, base


def E_abs_rademacher(k):
    return sum(math.comb(k, j) * abs(2 * j - k) for j in range(k + 1)) / 2 ** k


def canonical_pair(n, p, m):
    """a_i=0,b_i=1 on p coords; a_i=1,b_i=0 on m coords; a_i=b_i=0 elsewhere."""
    a = b = 0
    for i in range(p):
        b |= 1 << i
    for i in range(p, p + m):
        a |= 1 << i
    return a, b


print("\nE. decoder-pair minimisation: the antipodal pair is optimal")

# E|R_k| is nondecreasing in k -- the only inequality the general-n step needs.
vals = [E_abs_rademacher(k) for k in range(12)]
check("E|R_k| is nondecreasing in k (k <= 11)",
      all(vals[k + 1] >= vals[k] - 1e-15 for k in range(len(vals) - 1)),
      f"E|R_9|={vals[9]:.6f}")

for n in [3, 5, 7, 9]:
    N = 1 << n
    # E[d_H(S,a)] = n/2 for every a: the first term does not depend on the pair
    check(f"n={n}: E[d_H(S,a)] = n/2 for every a",
          all(abs(sum(popcount(s ^ a) for s in range(N)) / N - n / 2) < 1e-12
              for a in range(N)))

    # E[Delta^-] = (1/2) E|R_{p+m}| on every orbit
    worst_id = 0.0
    for p in range(n + 1):
        for m in range(n + 1 - p):
            a, b = canonical_pair(n, p, m)
            d = _delta(n, a, b)
            em = sum(max(-x, 0) for x in d) / N
            worst_id = max(worst_id, abs(em - 0.5 * E_abs_rademacher(p + m)))
    check(f"n={n}: E[Delta^-] = (1/2)E|R_(p+m)| on every orbit",
          worst_id < 1e-12, f"max dev={worst_id:.2e}")

    mn = M_n(n)
    worst_gap, worst_ant = 0.0, 0.0
    for j in range(5):
        g = (j / 4) * (1 / n)
        target = mn + n * g * ((n - 1) / 2 - mn)
        if n <= 5:                      # exhaustive over all 4^n decoder pairs
            pairs = ((a, b) for a in range(N) for b in range(N))
        else:                           # one representative per S_n-orbit
            pairs = (canonical_pair(n, p, m)
                     for p in range(n + 1) for m in range(n + 1 - p))
        best = min(lower_bound_pair(n, g, a, b)[0] for a, b in pairs)
        worst_gap = max(worst_gap, target - best)   # >0 would beat Theorem 1
        anti, _ = lower_bound_pair(n, g, 0, N - 1)
        worst_ant = max(worst_ant, abs(anti - target))
    scope = "all 4^n pairs" if n <= 5 else "all (p,m) orbits"
    check(f"n={n}: no decoder pair beats Theorem 1 ({scope})",
          worst_gap < 1e-12, f"max improvement={max(worst_gap,0):.2e}")
    check(f"n={n}: the antipodal pair attains the closed form",
          worst_ant < 1e-12, f"max dev={worst_ant:.2e}")

    # the optimal r is feasible: monotone on the cube, and inside [0, 1-n*gamma]
    ok = True
    for j in range(5):
        g = (j / 4) * (1 / n)
        r = [(1 - n * g) * (1 if popcount(s) > n / 2 else 0) for s in range(N)]
        ok &= all(0 <= r[s] <= 1 - n * g + 1e-15 for s in range(N))
        ok &= all(r[s | (1 << i)] >= r[s] - 1e-15
                  for s in range(N) for i in range(n))
    check(f"n={n}: the minimiser r* is monotone, hence feasible", ok)


# ============================ F. the engineering table (Section 6, Table 3)
#
# C(n) = 2^n / K_flat(n) is bracketed by the two bounds on gamma_2(Q_n):
#     2^(n+1)/(n+2)  <=  gamma_2(Q_n)  <=  2^(n - floor(log2(n/2+1))).
# This block recomputes every published cell of that table, and the two
# concrete claims in the text, from those bounds alone.

def gamma2_bounds(n):
    lo = math.ceil(2 ** (n + 1) / (n + 2))
    hi = 2 ** (n - math.floor(math.log2(n / 2 + 1)))
    return lo, hi


print("\nF. compression ratio C(n) = 2^n / K_flat(n)")

# exact K_flat where known; bracket elsewhere
KNOWN = {3: (4, 4), 5: (10, 10), 7: (32, 32), 9: (97, 128)}
TABLE = {            # (C_lo, C_hi, free_bits_lo, free_bits_hi) as published
    3:  (2.00, 2.00, 1.00, 1.00),
    5:  (3.20, 3.20, 1.68, 1.68),
    7:  (4.00, 4.00, 2.00, 2.00),
    9:  (4.00, 5.28, 2.00, 2.40),
    20: (8.00, 11.00, 3.00, 3.46),
    50: (16.00, 26.00, 4.00, 4.70),
}
for n, (clo, chi, blo, bhi) in TABLE.items():
    lo, hi = KNOWN.get(n, gamma2_bounds(n))
    got_lo, got_hi = 2 ** n / hi, 2 ** n / lo     # bigger K => smaller ratio
    ok = abs(got_lo - clo) < 5e-3 and abs(got_hi - chi) < 5e-3
    check(f"n={n}: C(n) in [{clo}, {chi}]", ok,
          f"computed [{got_lo:.2f}, {got_hi:.2f}]")
    b1, b2 = math.log2(got_lo), math.log2(got_hi)
    okb = abs(b1 - blo) < 5e-3 and abs(b2 - bhi) < 5e-3
    check(f"n={n}: free bits in [{blo}, {bhi}]", okb,
          f"computed [{b1:.2f}, {b2:.2f}]")

# the bracket must contain the known exact values, and (n+2)/2 must bound C(n)
for n in (3, 5, 7, 9):
    lo, hi = gamma2_bounds(n)
    k_lo, k_hi = KNOWN[n]
    check(f"n={n}: the two bounds bracket K_flat", lo <= k_lo and k_hi <= hi,
          f"bounds [{lo}, {hi}]  K_flat [{k_lo}, {k_hi}]")
for n in (3, 5, 7, 9, 20, 50):
    lo, hi = KNOWN.get(n, gamma2_bounds(n))
    check(f"n={n}: C(n) <= (n+2)/2", 2 ** n / lo <= (n + 2) / 2 + 1e-9,
          f"C_max={2 ** n / lo:.2f}  (n+2)/2={(n + 2) / 2:.2f}")

# the two sentences in Section 6
lo20, hi20 = gamma2_bounds(20)
check("n=20: flatness needs K in [95326, 131072]", (lo20, hi20) == (95326, 131072),
      f"got [{lo20}, {hi20}]")
check("n=20: that is 16.5-17.0 of 20 bits",
      abs(math.log2(lo20) - 16.54) < 5e-3 and abs(math.log2(hi20) - 17.0) < 5e-3,
      f"[{math.log2(lo20):.2f}, {math.log2(hi20):.2f}]")
lo50, hi50 = gamma2_bounds(50)
check("n=50: that is 45.3-46.0 of 50 bits",
      abs(math.log2(lo50) - 45.30) < 5e-3 and abs(math.log2(hi50) - 46.0) < 5e-3,
      f"[{math.log2(lo50):.2f}, {math.log2(hi50):.2f}]")


# ============ G. the general-prior threshold: a retraction, checked
#
# An earlier version of this block verified the claim
#     K_flat(tilted) = 2^n - (n-1)
# by testing whether a pi-optimal K-median set is 2-DOMINATING. That test is
# wrong. Lemma 3' says every non-centre has >= 2 centres at ITS OWN NEAREST
# DISTANCE d(s,C); that is 2-domination only when the optimal code is
# dominating. The uniform prior makes it dominating above gamma(Q_n) -- which
# is why Theorem 9 stands -- but a tilted prior need not.
#
# The old block and the old MILP agreed on 6, 28, 122 at n = 3, 5, 7 because
# BOTH encoded the same wrong condition. Two implementations of one wrong
# specification agree; that is what independence of implementation cannot buy.
#
# What is checked here instead: the counterexamples, by construction. We build
# an explicitly flat record at a K BELOW the withdrawn threshold and measure its
# distortion and margin from scratch -- no solver, no proxy condition.

def bernoulli_mass(n, q, v):
    w = popcount(v)
    return q ** w * (1 - q) ** (n - w)


def _prior_vec(n, q):
    return [bernoulli_mass(n, q, v) for v in range(1 << n)]


def _code_cost(n, pi, C):
    return sum(pi[s] * min(popcount(s ^ c) for c in C) for s in range(1 << n))


def _nearest(n, C, s):
    d = min(popcount(s ^ c) for c in C)
    return d, [c for c in C if popcount(s ^ c) == d]


def _spread(n, C):
    """Point mass on each centre; each non-centre uniform on its nearest centres."""
    N, K = 1 << n, len(C)
    idx = {c: j for j, c in enumerate(C)}
    q = [[0.0] * K for _ in range(N)]
    for s in range(N):
        _, nr = _nearest(n, C, s)
        for c in nr:
            q[s][idx[c]] = 1.0 / len(nr)
    return q


def _margin_lb(n, q):
    """A solver-free LOWER bound on the margin: the worst single edge.

    Theorem 3 minimises over mixtures, so the per-edge minimum is an upper
    bound on gamma; to certify gamma > 0 without an LP we instead use the
    dual-feasible payment p_i[y] = (centre of y)_i, whose guaranteed value is
    the worst edge gap it achieves. That is a genuine lower bound.
    """
    K = len(q[0])
    worst = float("inf")
    for i in range(n):
        pay = [(C_GLOBAL[y] >> i) & 1 for y in range(K)]
        for sm in range(1 << (n - 1)):
            lo = sm & ((1 << i) - 1)
            hi = (sm >> i) << (i + 1)
            s0 = lo | hi
            s1 = s0 | (1 << i)
            gap = sum(pay[y] * (q[s1][y] - q[s0][y]) for y in range(K))
            worst = min(worst, gap)
    return worst


print("\nG. the general-prior threshold: the withdrawn claim, refuted")

# The two counterexamples reported in Section 5.7, rebuilt from nothing.
for n, q_, C, D0_expect, gam_expect in [
        (3, 0.7, [0b011, 0b101, 0b110, 0b111], 0.2430, 1 / 3),
        (4, 0.7, [0b0111, 0b1011, 0b1101, 0b1110, 0b1111], 0.4401, 0.25)]:
    N = 1 << n
    pi = _prior_vec(n, q_)
    K = len(C)

    # (a) C really is pi-optimal at its size -- checked against every K-subset
    best = min(_code_cost(n, pi, list(S))
               for S in itertools.combinations(range(N), K))
    check(f"n={n} q={q_}: the witness code is pi-optimal at K={K}",
          abs(_code_cost(n, pi, C) - best) < 1e-12,
          f"D_0({K}) = {best:.6f}")
    check(f"n={n} q={q_}: D_0({K}) = {D0_expect}",
          abs(best - D0_expect) < 5e-5, f"{best:.6f}")

    # (b) it is NOT dominating -- which is exactly why the old test rejected it
    far = [s for s in range(N) if s not in C and _nearest(n, C, s)[0] > 1]
    check(f"n={n} q={q_}: the witness is NOT dominating",
          len(far) > 0,
          "at distance >= 2: " + ", ".join(format(s, "0" + str(n) + "b")
                                           for s in far))

    # (c) but it does satisfy the CORRECT necessary condition
    check(f"n={n} q={q_}: every non-centre has >= 2 centres at its own distance",
          all(len(_nearest(n, C, s)[1]) >= 2 for s in range(N) if s not in C))

    # (d) and the record built on it is flat: D = D_0 exactly, margin > 0
    C_GLOBAL = C
    rec = _spread(n, C)
    D = 0.0
    for y in range(K):
        col = [pi[s] * rec[s][y] for s in range(N)]
        if sum(col) <= 0:
            continue
        t_best = min(range(N),
                     key=lambda t: sum(col[s] * popcount(s ^ t) for s in range(N)))
        D += sum(col[s] * popcount(s ^ t_best) for s in range(N))
    check(f"n={n} q={q_}: the spread record attains D_0 exactly",
          abs(D - best) < 1e-12, f"D = {D:.6f}  D_0 = {best:.6f}")

    g = _margin_lb(n, rec)
    check(f"n={n} q={q_}: it achieves a positive margin, so it is FLAT",
          g > 1e-9, f"gamma >= {g:.6f} (certified by an explicit payment rule)")
    check(f"n={n} q={q_}: that margin is {gam_expect:.4f}",
          abs(g - gam_expect) < 1e-9, f"{g:.6f}")

    # (e) therefore the withdrawn threshold is refuted at this n
    withdrawn = N - (n - 1)
    check(f"n={n} q={q_}: K={K} < {withdrawn}, refuting the withdrawn claim",
          K < withdrawn,
          f"a flat record exists at K={K}; the withdrawn claim said {withdrawn}")

# The uniform prior is unaffected: there the optimal codes ARE dominating above
# gamma(Q_n), so the condition does specialise to 2-domination and Theorem 9
# holds. Check that specialisation on the two cases we can enumerate.
for n, kflat in [(3, 4), (4, 7)]:
    N = 1 << n
    pi = [1.0 / N] * N
    found = None
    for K in range(2, N + 1):
        best = min(_code_cost(n, pi, list(S))
                   for S in itertools.combinations(range(N), K))
        ok = False
        for S in itertools.combinations(range(N), K):
            if abs(_code_cost(n, pi, list(S)) - best) > 1e-12:
                continue
            if all(len(_nearest(n, list(S), s)[1]) >= 2
                   for s in range(N) if s not in S) and \
               all(_nearest(n, list(S), s)[0] <= 1 for s in range(N)):
                ok = True
                break
        if ok:
            found = K
            break
    check(f"n={n} uniform: K_flat = gamma_2(Q_{n}) = {kflat}", found == kflat,
          f"enumeration gives {found}")


# ================================================================== summary
print("\n" + "=" * 62)
if FAILS:
    print(f"{len(FAILS)} CHECK(S) FAILED:")
    for f in FAILS:
        print("  -", f)
    sys.exit(1)
print("ALL CHECKS PASSED -- no solver was used.")
sys.exit(0)
