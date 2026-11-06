"""
Algebraic upper bound on gamma_2(Q_n), hence on K_flat(n).

Let H be an m x n binary parity-check matrix with NO zero column such that
every nonzero syndrome appears at least twice among the columns. Put
C = ker H, so |C| = 2^(n-m). For x not in C, the centres at distance 1 from x
are the weight-1 vectors in the coset x + C, i.e. the columns of H equal to
x's syndrome. There are >= 2 of them by construction, so C is 2-dominating.

Feasible whenever 2(2^m - 1) <= n, i.e. m = floor(log2(n/2 + 1)), giving

    gamma_2(Q_n) <= 2^(n - floor(log2(n/2 + 1))).

Verified here directly against the flat construction, no solver.
"""
import json, warnings
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out as outpath
warnings.filterwarnings("ignore")
from math import floor, log2
import numpy as np
from kflat_theory import check_two_dominating, verify_flat_construction


def linear_2dom_code(n):
    m = int(floor(log2(n / 2 + 1)))
    if m < 1:
        return None, None
    syndromes = list(range(1, 2 ** m))          # nonzero syndromes
    cols = []
    i = 0
    while len(cols) < n:                        # round-robin: each used >= 2x
        cols.append(syndromes[i % len(syndromes)])
        i += 1
    counts = {s: cols.count(s) for s in syndromes}
    if min(counts.values()) < 2:
        return None, None
    N = 2 ** n
    # syndrome of v = XOR of columns where v has a 1 (bit n-1-i is coord i)
    C = []
    for v in range(N):
        s = 0
        for i in range(n):
            if v & (1 << (n - 1 - i)):
                s ^= cols[i]
        if s == 0:
            C.append(v)
    return C, dict(m=m, columns=cols, syndrome_counts=counts, size=len(C))


if __name__ == "__main__":
    out = {}
    for n in [3, 5, 7, 9, 11, 13, 15]:
        C, meta = linear_2dom_code(n)
        if C is None:
            print(f"n={n}: no valid H", flush=True)
            continue
        chk = check_two_dominating(n, C)
        row = dict(meta=meta, check=chk)
        if n <= 11:
            v = verify_flat_construction(n, C)
            row["verify"] = v
            print(f"n={n:3d}: |C|=2^{n}-{meta['m']} = {len(C):5d}  "
                  f"2-dominating={chk['is_2_dominating']} min_deg={chk['min_deg_outside']} "
                  f"| D={v['D']:.8f} D0={v['D0']:.8f} FLAT={v['flat']} "
                  f"margin={v['min_margin']:.6f}", flush=True)
        else:
            print(f"n={n:3d}: |C|={len(C):6d}  2-dominating={chk['is_2_dominating']} "
                  f"min_deg={chk['min_deg_outside']}", flush=True)
        out[n] = row
        json.dump(out, open(outpath("linear_2dom.json"), "w", newline="\n"), indent=1, default=float)
