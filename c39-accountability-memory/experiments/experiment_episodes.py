"""A controlled multi-agent episode, and records that compress its trace.

The mechanism experiment (`experiment_agents.py`) compresses the effort profile
itself, which concedes the abstraction most open to attack. This one puts an
episode in between:

        coordinator  ->  agent 1 .. agent n  ->  artifacts  ->  final output

Each agent i has a controlled ground-truth effort bit S_i. Given it, the agent
returns an artifact A_i in {0..L-1} -- a quality level -- drawn from one of two
distributions. The coordinator emits a final output F from the artifacts. The
trace is (A_1..A_n, F), and a RECORD is a function of that trace, not of S.

The encoder the theory talks about,

    q[s][y] = P(record label = y | effort profile = s),

is therefore something this experiment *measures* rather than defines. Agents
are conditionally independent given S, so it is computed exactly by enumerating
the L^n artifact tuples; a sampled run over episodes is reported alongside as a
cross-check, since "run many episodes" is what the design is meant to be.

    python experiment_episodes.py          # n = 3,5 -> experiment_episodes.json
"""
import json, math, sys, time
from itertools import product
import numpy as np

from experiment_agents import popcount, prior, distortion, margin
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out

L = 3                      # artifact quality levels
TAU = 2                    # A_i >= TAU counts as a completed subtask
P_EFFORT = np.array([0.1, 0.3, 0.6])      # P(A_i | S_i = 1)
P_SHIRK = np.array([0.6, 0.3, 0.1])       # P(A_i | S_i = 0)
SEED = 20260915


def artifact_dist(n, s):
    """P(A | S = s) over all L^n artifact tuples, as a dict keyed by tuple."""
    per = [P_EFFORT if (s >> i) & 1 else P_SHIRK for i in range(n)]
    out = {}
    for A in product(range(L), repeat=n):
        p = 1.0
        for i, a in enumerate(A):
            p *= per[i][a]
        out[A] = p
    return out


def final_output(n, A):
    """The coordinator ships if at least half the subtasks completed."""
    return int(sum(1 for a in A if a >= TAU) >= math.ceil(n / 2))


# ------------------------------------------------------------ record schemes
def rec_full_trace(n, A):
    return ("full",) + A + (final_output(n, A),)


def rec_per_agent_bit(n, A):
    return tuple(1 if a >= TAU else 0 for a in A)


def rec_per_agent_coarse(n, A):
    """Keep the success bit only for the top half of agents by quality."""
    keep = sorted(range(n), key=lambda i: (-A[i], i))[: math.ceil(n / 2)]
    return tuple((1 if A[i] >= TAU else 0) if i in set(keep) else -1
                 for i in range(n))


def rec_global_summary(n, A):
    """All the content, none of the identity: the multiset of artifacts."""
    return tuple(sorted(A))


def rec_aggregate(n, A):
    return sum(1 for a in A if a >= TAU)


def rec_final_output(n, A):
    return final_output(n, A)


def rec_recency_k(n, A):
    """Context-window eviction: keep the last ceil(n/2) agents' artifacts."""
    k = math.ceil(n / 2)
    keep = set(range(n - k, n))
    return tuple(A[i] if i in keep else -1 for i in range(n))


def rec_role_rollup(n, A):
    """Agents split into two named roles; keep completions per role."""
    half = n // 2
    lo = sum(1 for i in range(half) if A[i] >= TAU)
    hi = sum(1 for i in range(half, n) if A[i] >= TAU)
    return (lo, hi)


def rec_quality_only(n, A):
    """The archetypal summary statistic: best quality seen, and how many finished."""
    return (max(A), sum(1 for a in A if a >= TAU))


SCHEMES = [("full_trace", rec_full_trace),
           ("recency_k", rec_recency_k),
           ("role_rollup", rec_role_rollup),
           ("quality_only", rec_quality_only),
           ("per_agent_bit", rec_per_agent_bit),
           ("per_agent_coarse", rec_per_agent_coarse),
           ("global_summary", rec_global_summary),
           ("aggregate", rec_aggregate),
           ("final_output", rec_final_output)]


def induced_encoder(n, scheme):
    """q[s][y] = sum over artifact tuples A of P(A|s) 1{scheme(A) = y}."""
    N = 1 << n
    dists = [artifact_dist(n, s) for s in range(N)]
    labels = sorted({scheme(n, A) for A in product(range(L), repeat=n)},
                    key=repr)
    idx = {y: j for j, y in enumerate(labels)}
    q = np.zeros((N, len(labels)))
    for s in range(N):
        for A, p in dists[s].items():
            q[s, idx[scheme(n, A)]] += p
    return q, len(labels)


def sampled_encoder(n, scheme, pi, episodes, rng):
    """The same encoder, estimated by actually running episodes."""
    N = 1 << n
    labels = sorted({scheme(n, A) for A in product(range(L), repeat=n)},
                    key=repr)
    idx = {y: j for j, y in enumerate(labels)}
    counts = np.zeros((N, len(labels)))
    seen = np.zeros(N)
    profiles = rng.choice(N, size=episodes, p=pi / pi.sum())
    for s in profiles:
        A = tuple(rng.choice(L, p=(P_EFFORT if (s >> i) & 1 else P_SHIRK))
                  for i in range(n))
        counts[s, idx[scheme(n, A)]] += 1
        seen[s] += 1
    q = np.where(seen[:, None] > 0, counts / np.maximum(seen, 1)[:, None], 0.0)
    for s in range(N):                      # unseen profile: fall back to uniform
        if seen[s] == 0:
            q[s] = 1.0 / len(labels)
    return q


if __name__ == "__main__":
    extra = [int(a) for a in sys.argv[1:]]
    rng = np.random.default_rng(SEED)
    out = {"config": dict(L=L, tau=TAU, p_effort=P_EFFORT.tolist(),
                          p_shirk=P_SHIRK.tolist(), seed=SEED,
                          coordinator="ships iff >= ceil(n/2) subtasks complete")}
    for n in [3, 4, 5, 6, 7] + extra:
        pi = prior(n, 0.5)
        rows = []
        print(f"n={n}  (L={L} quality levels, {L**n} artifact tuples)", flush=True)
        for name, scheme in SCHEMES:
            t0 = time.time()
            q, K = induced_encoder(n, scheme)
            D, g = distortion(n, pi, q), margin(n, q)
            rows.append(dict(scheme=name, K=K, bits=math.log2(K), D=D, gamma=g,
                             seconds=time.time() - t0))
            print(f"    {name:<17} K={K:<5} bits={math.log2(K):5.2f}  D={D:.6f}  gamma={g:.6f}"
                  f"  [{time.time()-t0:.1f}s]", flush=True)
        # E6: does running episodes reproduce the exact numbers?
        eps = 200000
        check = []
        for name, scheme in SCHEMES:
            qs = sampled_encoder(n, scheme, pi, eps, rng)
            Ds, gs = distortion(n, pi, qs), margin(n, qs)
            exact = next(r for r in rows if r["scheme"] == name)
            check.append(dict(scheme=name, D_sampled=Ds, gamma_sampled=gs,
                              dD=abs(Ds - exact["D"]),
                              dgamma=abs(gs - exact["gamma"])))
            print(f"    [{eps} episodes] {name:<17} dD={abs(Ds-exact['D']):.4f}"
                  f"  dgamma={abs(gs-exact['gamma']):.4f}", flush=True)
        out[str(n)] = dict(exact=rows, sampled=check, episodes=eps)
        json.dump(out, open(out("experiment_episodes.json"), "w"), indent=1)
        print(flush=True)
    print("wrote experiment_episodes.json")
