"""Where real compaction mechanisms land on the reconstruction/accountability plane.

The paper's theorems describe records chosen optimally. This evaluates records
chosen the way a coordinator actually chooses them -- keep a count, keep a
threshold, keep the first few agents, hash it into a fixed number of buckets --
and measures where each one lands.

Nothing is sampled. Every profile is enumerated, so the numbers below are exact
and there is no seed.

Two quantities per mechanism:

  D      expected Hamming error of the Bayes reconstruction from the record;
  gamma  the largest all-teammate-profile margin any bounded payment rule can
         achieve from that record.

gamma is computed via the elimination theorem (Theorem 3), which turns the
otherwise bilinear search over payment rules into one LP per agent:

    gamma_i = min over mixtures lambda of teammate profiles of
              (1/2) * || E_lambda[ d_i ] ||_1

so the experiment also exercises the paper's main tool as its instrument.

Under noise, effort S_i is observed as X_i with P(X_i != S_i) = eta; the
mechanism sees X, while reconstruction and payment are still judged against S.
A record that factors through X is a RESTRICTED kind of stochastic encoder, so
two baselines are reported and must not be confused: D0_unrestricted is the
paper's D_0(K) over all stochastic encoders, and D0_channel is the best any
record can do given the channel. 'flat' always means the paper's notion --
attaining D0_unrestricted with positive margin. A record can be optimal within
the channel class without being flat, and that is reported separately.

    python experiment_agents.py            # n = 3,5   -> experiment_agents.json
    python experiment_agents.py 7          # add n = 7
"""
import json, math, sys, time
import numpy as np
from scipy.optimize import linprog
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out as outpath

TOL = 1e-9


def popcount(x):
    return bin(x).count("1")


def prior(n, q):
    return np.array([q ** popcount(s) * (1 - q) ** (n - popcount(s))
                     for s in range(1 << n)])


# --------------------------------------------------------------- mechanisms
def mech_full(n):
    return [s for s in range(1 << n)], "full"


def mech_count(n):
    return [popcount(s) for s in range(1 << n)], "count"


def mech_threshold(n):
    t = math.ceil(n / 2)
    return [1 if popcount(s) >= t else 0 for s in range(1 << n)], "threshold"


def mech_prefix(n, m):
    return [s & ((1 << m) - 1) for s in range(1 << n)], f"prefix{m}"


def mech_hash(n, K):
    # a deterministic, structure-blind bucketing -- generic lossy compaction
    return [(s * 2654435761) % K for s in range(1 << n)], f"hash{K}"


def mech_topk(n, k):
    """Keep which agents contributed, but only the first k of them."""
    out = []
    for s in range(1 << n):
        kept, c = 0, 0
        for i in range(n):
            if (s >> i) & 1:
                if c < k:
                    kept |= 1 << i
                c += 1
        out.append(kept)
    return out, f"top{k}"


def labels_to_encoder(n, labels):
    """Deterministic mechanism -> encoder q[s][y], plus the label alphabet."""
    alphabet = sorted(set(labels))
    idx = {a: j for j, a in enumerate(alphabet)}
    N, K = 1 << n, len(alphabet)
    q = np.zeros((N, K))
    for s in range(N):
        q[s, idx[labels[s]]] = 1.0
    return q, K


def encoder_flat(n, centres):
    """The Lemma 8 construction: point mass on centres, non-centres spread."""
    N = 1 << n
    idx = {c: j for j, c in enumerate(centres)}
    q = np.zeros((N, len(centres)))
    for s in range(N):
        if s in idx:
            q[s, idx[s]] = 1.0
        else:
            nb = [c for c in centres if popcount(s ^ c) == 1]
            if not nb:
                return None                      # not dominating: undefined
            for c in nb:
                q[s, idx[c]] = 1.0 / len(nb)
    return q


def apply_noise(n, q, eta):
    """The mechanism sees X, not S:  q'[s] = sum_x P(x|s) q[x]."""
    if eta == 0:
        return q
    N = 1 << n
    P = np.empty((N, N))
    for s in range(N):
        for x in range(N):
            d = popcount(s ^ x)
            P[s, x] = (eta ** d) * ((1 - eta) ** (n - d))
    return P @ q


# --------------------------------------------------------------- measurement
def distortion(n, pi, q):
    """Bayes reconstruction from each label, expected Hamming error."""
    N = 1 << n
    joint = q * pi[:, None]                      # joint[s, y]
    D = 0.0
    for y in range(q.shape[1]):
        col = joint[:, y]
        if col.sum() <= 0:
            continue
        best = min(range(N), key=lambda t: sum(col[s] * popcount(s ^ t)
                                               for s in range(N)))
        D += sum(col[s] * popcount(s ^ best) for s in range(N))
    return D


def margin(n, q):
    """Theorem 3: gamma_i = min_lambda (1/2)||E_lambda[d_i]||_1, then min over i."""
    N, K = q.shape
    worst = math.inf
    for i in range(n):
        rows = []
        for sm in range(1 << (n - 1)):           # teammate profiles
            lo = sm & ((1 << i) - 1)
            hi = (sm >> i) << (i + 1)
            s0 = lo | hi
            s1 = s0 | (1 << i)
            rows.append(q[s1] - q[s0])
        A = np.array(rows)                       # (T, K)
        T = A.shape[0]
        # min (1/2) sum_y u_y   s.t.  u >= +A^T lambda,  u >= -A^T lambda,
        #                             lambda >= 0, sum lambda = 1
        nv = T + K
        c = np.concatenate([np.zeros(T), 0.5 * np.ones(K)])
        A_ub = np.block([[A.T, -np.eye(K)], [-A.T, -np.eye(K)]])
        b_ub = np.zeros(2 * K)
        A_eq = np.concatenate([np.ones(T), np.zeros(K)])[None, :]
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0],
                      bounds=[(0, None)] * T + [(0, None)] * K,
                      method="highs")
        if not res.success:
            return None
        worst = min(worst, float(res.fun))
    return worst


def d0_exact(n, pi, K, eta=0.0):
    """Best distortion ANY K-label record can achieve through the channel.

    With eta = 0 this is the weighted K-median of the paper. With noise the
    record is a function of the observation x, so the right baseline is

        min over K centres of  sum_x P(x) * min_t sum_s P(s|x) d_H(s,t),

    the same program with a channel-aware cost. Comparing a noisy record
    against the NOISELESS optimum would make flatness unreachable by
    construction and would prove nothing.
    """
    from prior_threshold import d0_weighted, d0_general
    if eta == 0.0:
        val, centres, _ = d0_weighted(n, pi, K)
        return val, centres
    N = 1 << n
    P = np.empty((N, N))                        # P[s, x]
    for s in range(N):
        for x in range(N):
            d = popcount(s ^ x)
            P[s, x] = (eta ** d) * ((1 - eta) ** (n - d))
    joint = P * pi[:, None]                     # joint[s, x]
    px = joint.sum(axis=0)
    post = joint / np.where(px > 0, px, 1.0)    # post[s, x] = P(s|x)
    cost = [[sum(post[s, x] * popcount(s ^ t) for s in range(N))
             for t in range(N)] for x in range(N)]
    val, centres, _ = d0_general(px, cost, K)
    return val, centres


# --------------------------------------------------------------------- main
def evaluate(n, q_prior, eta, cert_codes):
    pi = prior(n, q_prior)
    N = 1 << n
    specs = [mech_full(n), mech_count(n), mech_threshold(n),
             mech_prefix(n, n - 1), mech_prefix(n, max(1, n // 2)),
             mech_topk(n, max(1, n // 2))]
    gamma2 = {3: 4, 5: 10, 7: 32}.get(n)
    if gamma2:
        specs.append(mech_hash(n, gamma2))
    rows = []
    for labels, name in specs:
        enc, K = labels_to_encoder(n, labels)
        enc = apply_noise(n, enc, eta)
        D = distortion(n, pi, enc)
        g = margin(n, enc)
        d0_ch, _ = d0_exact(n, pi, K, eta)          # best within the channel class
        d0_un, _ = d0_exact(n, pi, K, 0.0)          # the paper's unrestricted D_0(K)
        rows.append(dict(mechanism=name, K=K, D=D, gamma=g,
                         D0_channel=d0_ch, D0_unrestricted=d0_un,
                         flat=bool(abs(D - d0_un) < 1e-7 and g is not None and g > TOL),
                         optimal_in_class=bool(abs(D - d0_ch) < 1e-7)))
        tag = ("FLAT" if rows[-1]["flat"] else
               ("opt-in-class" if rows[-1]["optimal_in_class"] else ""))
        print(f"    {name:<12} K={K:<4} D={D:.6f}  D0={d0_un:.6f}"
              f"  D0|chan={d0_ch:.6f}  gamma={g:.6f}  {tag}", flush=True)

    # the two records at the threshold: optimal quantiser vs our construction
    if gamma2 and str(n) in cert_codes:
        centres = cert_codes[str(n)]
        enc = encoder_flat(n, centres)
        if enc is not None:
            enc = apply_noise(n, enc, eta)
            D = distortion(n, pi, enc)
            g = margin(n, enc)
            d0_ch, km_centres = d0_exact(n, pi, gamma2, eta)
            d0_un, _ = d0_exact(n, pi, gamma2, 0.0)
            rows.append(dict(mechanism="flat", K=gamma2, D=D, gamma=g,
                             D0_channel=d0_ch, D0_unrestricted=d0_un,
                             flat=bool(abs(D - d0_un) < 1e-7 and g > TOL),
                             optimal_in_class=bool(abs(D - d0_ch) < 1e-7)))
            tag = ("FLAT" if rows[-1]["flat"] else
                   ("opt-in-class" if rows[-1]["optimal_in_class"] else ""))
            print(f"    {'flat':<12} K={gamma2:<4} D={D:.6f}  D0={d0_un:.6f}"
                  f"  D0|chan={d0_ch:.6f}  gamma={g:.6f}  {tag}", flush=True)
            # nearest-centre quantiser on the SAME K -- optimal D, no margin?
            lab = [min(km_centres, key=lambda c: popcount(s ^ c)) for s in range(N)]
            enc2, K2 = labels_to_encoder(n, lab)
            enc2 = apply_noise(n, enc2, eta)
            D2, g2 = distortion(n, pi, enc2), margin(n, enc2)
            rows.append(dict(mechanism="kmedian", K=K2, D=D2, gamma=g2,
                             D0_channel=d0_ch, D0_unrestricted=d0_un,
                             flat=bool(abs(D2 - d0_un) < 1e-7 and g2 > TOL),
                             optimal_in_class=bool(abs(D2 - d0_ch) < 1e-7)))
            tag = ("FLAT" if rows[-1]["flat"] else
                   ("opt-in-class" if rows[-1]["optimal_in_class"] else ""))
            print(f"    {'kmedian':<12} K={K2:<4} D={D2:.6f}  D0={d0_un:.6f}"
                  f"  D0|chan={d0_ch:.6f}  gamma={g2:.6f}  {tag}", flush=True)
    return rows


if __name__ == "__main__":
    extra = [int(a) for a in sys.argv[1:]]
    cert = {}
    try:
        codes = json.load(open(data("certified_codes.json")))["codes"]
        cert = {str(v["n"]): v["centres"] for v in codes.values()}
    except (OSError, KeyError):
        pass

    out = {}
    for n in [3, 5] + extra:
        out[str(n)] = {}
        for q_prior in (0.5, 0.7):
            for eta in (0.0, 0.05, 0.1, 0.2):
                t0 = time.time()
                key = f"q{q_prior}_eta{eta}"
                print(f"n={n}  prior q={q_prior}  noise eta={eta}", flush=True)
                out[str(n)][key] = evaluate(n, q_prior, eta, cert)
                print(f"  [{time.time()-t0:.1f}s]\n", flush=True)
                json.dump(out, open(outpath("experiment_agents.json"), "w", newline="\n"), indent=1)
    print("wrote experiment_agents.json")
