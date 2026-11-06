"""Re-prove the n=9 lower bound in the PINNED environment.

gamma2_big.log recorded K=92..96 as MILP-infeasible for 2-domination of Q_9,
which is what gives K_flat(9) >= 97. Those rows were computed under Python
3.12.3 / NumPy 2.4.4 / SciPy 1.17.1, which is not environment.json's pin.
This re-runs exactly those rows under the pin and compares the verdicts.

K >= 97 is deliberately not attempted: it does not terminate (see
research_state.md section 2) and the lower bound does not depend on it.
"""
import json, sys, time, warnings
import numpy as np, scipy
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out as outpath
warnings.filterwarnings("ignore")
from kflat_theory import two_dominating_set

PRIOR = {92: False, 93: False, 94: False, 95: False, 96: False}  # from gamma2_big.log

print(f"env: python {sys.version.split()[0]}  numpy {np.__version__}  scipy {scipy.__version__}",
      flush=True)
print("=== n=9: re-proving K=92..96 infeasible under the pin ===", flush=True)

rows, agree = {}, True
for K in sorted(PRIOR):
    C, info = two_dominating_set(9, K, time_limit=1800)
    feasible = C is not None
    proved = (not feasible) and info["status"] == 2
    tag = "INFEASIBLE (proved)" if proved else (
        "FEASIBLE" if feasible else f"unresolved (status {info['status']})")
    ok = proved and (PRIOR[K] is False)
    agree &= ok
    print(f"  K={K}: {tag}  [{info['seconds']}s]  vs gamma2_big.log: "
          f"{'AGREE' if ok else 'DISAGREE'}", flush=True)
    rows[K] = dict(feasible=feasible, status=info["status"],
                   seconds=info["seconds"], agrees_with_prepin=bool(ok))

out = {
    "environment": {"python": sys.version.split()[0], "numpy": np.__version__,
                    "scipy": scipy.__version__},
    "claim": "gamma_2(Q_9) >= 97, i.e. K_flat(9) >= 97",
    "rows": rows,
    "all_agree_with_prepinned": bool(agree),
}
json.dump(out, open(outpath("gamma2_n9_lb_rerun.json"), "w", newline="\n"), indent=1)
print("\n" + ("ALL ROWS AGREE -- the n=9 lower bound holds in the pinned environment."
              if agree else "DISAGREEMENT -- the n=9 lower bound is NOT reproduced."),
      flush=True)
sys.exit(0 if agree else 1)
