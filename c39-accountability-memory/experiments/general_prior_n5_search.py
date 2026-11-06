"""Phase 1, part 3: does the bad configuration exist at n = 5?

    python experiments/general_prior_n5_search.py 5

Part 2 found ZERO configurations at n = 4 by exhaustive search over all 2^16
codes: no code with nu >= 2 everywhere has a descending edge along which nu
fails to strictly decrease. That suggests

    Proposition 12  =>  nu strictly decreases along every descending edge
                    =>  the generalised construction has positive margin,

i.e. Proposition 12 is not merely necessary but sufficient. Before attempting a
proof, test n = 5, where 2^32 codes are too many to enumerate.

REDUCTION. The cube is vertex-transitive and coordinate-permutation symmetric,
so a bad edge can be moved to (s_0, s_1) = (0^n, e_0) without loss of
generality. The configuration then demands, with r = d(0^n, C) >= 2:

  * no centre of weight < r                        (so d(0,C) = r)
  * N(0) = N(e_0), i.e. every weight-r centre has bit 0 set
    (a weight-r centre with bit 0 clear would sit in N(0) but not N(e_0))
  * nu(s) >= 2 for every non-centre s

Everything of weight < r is excluded, so the only freedom is which weight-r
words containing bit 0 to take, and which words of weight > r to take. That is
a search of size 2^(#weight-r words with bit 0) x 2^(#words of weight > r),
which is small enough to enumerate exactly at n = 5 for each r.
"""
import sys, itertools, json, time
import numpy as np
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from c39.paths import out
from experiment_agents import popcount


def search(n, verbose=True):
    N = 1 << n
    Hrow = [[popcount(a ^ b) for b in range(N)] for a in range(N)]
    hits = []
    total = 0
    for r in range(2, n + 1):
        # centres of weight exactly r must all carry bit 0
        wr = [v for v in range(N) if popcount(v) == r and (v & 1)]
        # anything of weight > r is unconstrained
        big = [v for v in range(N) if popcount(v) > r]
        if verbose:
            print(f"  r={r}: {len(wr)} weight-{r} candidates (bit 0 set), "
                  f"{len(big)} words of weight > r "
                  f"-> {2**len(wr) * 2**len(big):,} codes")
        for kmask in range(1, 1 << len(wr)):
            near = [wr[j] for j in range(len(wr)) if kmask >> j & 1]
            if len(near) < 2:                 # nu(0) = |near| must be >= 2
                continue
            for bmask in range(1 << len(big)):
                total += 1
                C = near + [big[j] for j in range(len(big)) if bmask >> j & 1]
                inC = set(C)
                if 0 in inC or 1 in inC:
                    continue
                d = [min(Hrow[s][c] for c in C) for s in range(N)]
                if d[0] != r or d[1] != r - 1:
                    continue
                nu = [sum(Hrow[s][c] == d[s] for c in C) for s in range(N)]
                if any(nu[s] < 2 for s in range(N) if s not in inC):
                    continue
                if nu[1] != nu[0]:            # the edge must actually be dead
                    continue
                hits.append((sorted(C), r, nu[0]))
                if verbose and len(hits) <= 5:
                    w = "0" + str(n) + "b"
                    print(f"    HIT C={[format(c,w) for c in sorted(C)]} "
                          f"r={r} nu={nu[0]}")
    return hits, total


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    t0 = time.time()
    print(f"searching n={n} for a Prop-12 code with a dead descending edge "
          f"(WLOG s_0 = 0^n, i = 0)")
    hits, total = search(n)
    dt = time.time() - t0
    print(f"\n{total:,} codes examined in {dt:.1f}s")
    print(f"configurations found: {len(hits)}")
    p = out(f"general_prior_n{n}_search.json")
    json.dump(dict(n=n, examined=total, hits=len(hits),
                   examples=[[int(c) for c in h[0]] for h in hits[:20]],
                   seconds=round(dt, 1)), open(p, "w", newline="\n"), indent=1)
    print(f"wrote {p}")
    if not hits:
        print(f"\n=> no configuration exists at n={n}: Proposition 12 appears "
              f"SUFFICIENT, and the construction always has positive margin.")
