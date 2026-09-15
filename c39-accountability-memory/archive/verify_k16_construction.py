"""
Direct verification of the analytic K=16 flat construction at n=5.

Construction: centres C = the 16 even-weight vectors of {0,1}^5.
  * every even-weight state maps to its own label with probability 1;
  * every odd-weight state spreads UNIFORMLY over the labels of its 5
    neighbours (all even-weight);
  * agent i's payment decoder is p_i[y] = (centre of y)_i.

Claim: D = D0(16) = 0.5 exactly, and the all-profile unilateral margin is
1 - 1/n = 0.8 for every agent. Verified here by direct enumeration, with no
solver involved.
"""
import itertools, json
import numpy as np
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out

n = 5; N = 2 ** n
S = np.array(list(itertools.product([0, 1], repeat=n)), dtype=int)
w = S.sum(1)
even = [i for i in range(N) if w[i] % 2 == 0]
K = len(even)
lab = {c: y for y, c in enumerate(even)}

q = np.zeros((N, K))
for s in range(N):
    if w[s] % 2 == 0:
        q[s, lab[s]] = 1.0
    else:
        nb = [int(s) ^ (1 << (n - 1 - i)) for i in range(n)]
        for t in nb:
            q[s, lab[t]] = 1.0 / n

assert np.allclose(q.sum(1), 1.0)

D = sum(min(q[S[:, i] == 0, y].sum() / N, q[S[:, i] == 1, y].sum() / N)
        for i in range(n) for y in range(K))

p = np.array([[S[c][i] for c in even] for i in range(n)], dtype=float)

margins = []
for i in range(n):
    worst = np.inf
    for prof in itertools.product([0, 1], repeat=n - 1):
        s1 = int("".join(map(str, list(prof[:i]) + [1] + list(prof[i:]))), 2)
        s0 = int("".join(map(str, list(prof[:i]) + [0] + list(prof[i:]))), 2)
        worst = min(worst, float(np.dot(p[i], q[s1] - q[s0])))
    margins.append(worst)

res = dict(n=n, K=K, D=float(D), D0_target=0.5, per_agent_margin=margins,
           min_margin=float(min(margins)),
           flat=bool(abs(D - 0.5) < 1e-12), payments_binary=True)
print(json.dumps(res, indent=1))
json.dump(res, open(out("verify_k16_construction.json"), "w"), indent=1)
