"""Freeze the explicit witnesses into certified_codes.json.

Run once (needs the MILP). Everything downstream -- verify_all.py, and the
paper's reproducibility package -- reads the JSON and needs no solver.
"""
import json, platform, sys, time
import numpy as np, scipy
import warnings
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out
warnings.filterwarnings("ignore")

from kflat_theory import two_dominating_set, check_two_dominating

TARGETS = [(3, 4), (5, 10), (6, 16), (7, 32)]

out = {
    "environment": {
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
    },
    "codes": {},
}

for n, K in TARGETS:
    t0 = time.time()
    C, info = two_dominating_set(n, K, time_limit=1800)
    assert C is not None, f"no 2-dominating set found at n={n}, K={K}"
    chk = check_two_dominating(n, C)
    assert chk["is_2_dominating"], (n, K, chk)
    out["codes"][f"n{n}"] = {
        "n": n, "K": K, "centres": sorted(int(c) for c in C),
        "min_deg_outside": int(chk["min_deg_outside"]),
        "milp_seconds": round(time.time() - t0, 2),
        "source": "MILP witness, rechecked",
    }
    print(f"n={n} K={K}: min_deg={chk['min_deg_outside']} ({time.time()-t0:.2f}s)",
          flush=True)

# n = 9 upper-bound witness, already on disk from the local-search run
ls = json.load(open(data("n9_localsearch.json")))
C9 = sorted(int(c) for c in ls["centers"])
chk9 = check_two_dominating(9, C9)
assert chk9["is_2_dominating"], chk9
out["codes"]["n9"] = {
    "n": 9, "K": len(C9), "centres": C9,
    "min_deg_outside": int(chk9["min_deg_outside"]),
    "source": "algebraic parity-check construction (upper bound witness)",
}
print(f"n=9 K={len(C9)}: min_deg={chk9['min_deg_outside']}", flush=True)

json.dump(out, open(out("certified_codes.json"), "w"), indent=1)
print("\nwrote certified_codes.json")
