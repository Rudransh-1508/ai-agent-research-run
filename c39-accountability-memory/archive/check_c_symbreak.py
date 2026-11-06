"""
Validation check C from session 1, which never ran: symmetry breaking on the
label ordering must not change the optimum of exp_kflat.UBModel.

What it checks: UBModel optionally imposes non-increasing marginal label mass
to break the K! label-permutation symmetry. That is valid only because labels
are exchangeable, so any feasible solution can be relabelled to satisfy it
without changing feasibility or objective. If the constraint ever changed the
optimal value, the argument would be wrong and every symmetry-broken row would
be void.

Scope note: the session-2 results come from kflat_structure.py, which uses NO
symmetry breaking anywhere (solve_D0_pmedian, enumerate_codes and margin_mip
all omit it). So check C bears only on the superseded exp_kflat.UBModel rows.
It is run here for completeness.
"""
import json, time, warnings
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out
warnings.filterwarnings("ignore")
import exp_kflat

cases = [(3, 2), (3, 3), (3, 4), (5, 2)]
rows = []
ok = True
for n, K in cases:
    for frac in [0.0, 0.5, 1.0]:
        g = frac / n
        a = exp_kflat.solve(n, K, g, time_limit=600, symbreak=False)
        b = exp_kflat.solve(n, K, g, time_limit=600, symbreak=True)
        dev = (None if (a["value"] is None or b["value"] is None)
               else b["value"] - a["value"])
        good = dev is not None and abs(dev) < 1e-6
        ok &= good
        rows.append(dict(n=n, K=K, gamma=g, nosym=a["value"], sym=b["value"],
                         nosym_gap=a["gap"], sym_gap=b["gap"],
                         nosym_sec=a["seconds"], sym_sec=b["seconds"],
                         dev=dev, pass_=bool(good)))
        print(f"  n={n} K={K} gamma={g:.6f}  nosym={a['value']} ({a['seconds']}s) "
              f"sym={b['value']} ({b['seconds']}s)  dev={dev}  "
              f"{'PASS' if good else 'FAIL'}", flush=True)
        json.dump(dict(rows=rows, C_pass=bool(ok)),
                  open(out("check_c_symbreak.json"), "w", newline="\n"), indent=1, default=float)
print(f"CHECK C: {'PASS' if ok else 'FAIL'}")
