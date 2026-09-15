"""
Step 3 of the session plan: validate the bracket model in the pinned
environment before anything downstream is trusted.

Three checks:

 A. exp3_bracket.solve(mode="UB") at K=2 must reproduce the T1 closed form
    D*(2,gamma) = M_n + n*gamma*((n-1)/2 - M_n) at n=3 and n=5 with MIP gap 0.
    (Valid target: T1's proof normalises nonconstant bounded payment pairs to
    endpoint orientations, so restricting p_i to {0,1}^2 is WLOG at K=2.)

 B. The sparse re-implementation in exp_kflat.UBModel must agree with the
    dense exp3_bracket.solve(mode="UB") value on every small case, with
    symmetry breaking OFF (so the two models are literally the same polytope).

 C. Symmetry breaking must not change the optimal value on those same cases.

If A fails, the bracket model is wrong and everything downstream is void.
"""
import itertools, json, time
import numpy as np

import exp3_bracket
import exp_kflat
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out


def M_n(n):
    S = np.array(list(itertools.product([0, 1], repeat=n)))
    w = S.sum(1)
    return float(np.mean(np.minimum(w, n - w)))


def t1(n, gamma):
    m = M_n(n)
    return m + n * gamma * ((n - 1) / 2.0 - m)


if __name__ == "__main__":
    out = {"A_t1_reproduction": [], "B_sparse_vs_dense": [], "C_symmetry_breaking": []}

    print("=== A. exp3_bracket UB at K=2 vs T1 closed form ===", flush=True)
    okA = True
    for n in [3, 5]:
        for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
            g = frac / n
            t0 = time.time()
            r = exp3_bracket.solve(n, 2, g, "UB", time_limit=600)
            cf = t1(n, g)
            dev = None if r["value"] is None else r["value"] - cf
            good = (r["value"] is not None and abs(dev) < 1e-6
                    and r.get("gap", 1.0) <= 1e-9)
            okA &= good
            out["A_t1_reproduction"].append(
                dict(n=n, gamma=g, UB=r["value"], gap=r.get("gap"),
                     T1=cf, dev=dev, pass_=bool(good)))
            print(f"  n={n} gamma={g:.6f}  UB={r['value']}  T1={cf:.10f}  "
                  f"dev={dev:+.3e}  gap={r.get('gap')}  "
                  f"{'PASS' if good else 'FAIL'}  [{time.time()-t0:.1f}s]", flush=True)
    out["A_pass"] = bool(okA)
    print(f"  A: {'PASS' if okA else 'FAIL'}\n", flush=True)

    if not okA:
        json.dump(out, open(out("validate_kflat_model.json"), "w"), indent=1, default=float)
        raise SystemExit("STOP: exp3_bracket K=2 does not reproduce T1 in the "
                         "pinned environment. Bracket model is void.")

    print("=== B. sparse exp_kflat.UBModel vs dense exp3_bracket (symbreak OFF) ===",
          flush=True)
    okB = True
    cases = [(3, 2), (3, 3), (3, 4), (5, 2), (5, 3)]
    for n, K in cases:
        for frac in [0.0, 0.5, 1.0]:
            g = frac / n
            d = exp3_bracket.solve(n, K, g, "UB", time_limit=600)
            s = exp_kflat.solve(n, K, g, time_limit=600, symbreak=False)
            dev = (None if (d["value"] is None or s["value"] is None)
                   else s["value"] - d["value"])
            good = dev is not None and abs(dev) < 1e-6
            okB &= good
            out["B_sparse_vs_dense"].append(
                dict(n=n, K=K, gamma=g, dense=d["value"], sparse=s["value"],
                     dense_gap=d.get("gap"), sparse_gap=s.get("gap"),
                     sparse_recomputed=(s["verified"] or {}).get("D_recomputed"),
                     dev=dev, pass_=bool(good)))
            print(f"  n={n} K={K} gamma={g:.6f}  dense={d['value']}  "
                  f"sparse={s['value']}  dev={dev}  "
                  f"{'PASS' if good else 'FAIL'}", flush=True)
    out["B_pass"] = bool(okB)
    print(f"  B: {'PASS' if okB else 'FAIL'}\n", flush=True)

    print("=== C. symmetry breaking must not change the optimum ===", flush=True)
    okC = True
    for n, K in cases:
        for frac in [0.0, 1.0]:
            g = frac / n
            a = exp_kflat.solve(n, K, g, time_limit=600, symbreak=False)
            b = exp_kflat.solve(n, K, g, time_limit=600, symbreak=True)
            dev = (None if (a["value"] is None or b["value"] is None)
                   else b["value"] - a["value"])
            good = dev is not None and abs(dev) < 1e-6
            okC &= good
            out["C_symmetry_breaking"].append(
                dict(n=n, K=K, gamma=g, nosym=a["value"], sym=b["value"],
                     nosym_sec=a["seconds"], sym_sec=b["seconds"],
                     dev=dev, pass_=bool(good)))
            print(f"  n={n} K={K} gamma={g:.6f}  nosym={a['value']} "
                  f"({a['seconds']}s)  sym={b['value']} ({b['seconds']}s)  "
                  f"dev={dev}  {'PASS' if good else 'FAIL'}", flush=True)
    out["C_pass"] = bool(okC)
    print(f"  C: {'PASS' if okC else 'FAIL'}", flush=True)

    json.dump(out, open(out("validate_kflat_model.json"), "w"), indent=1, default=float)
    print(f"\nOVERALL: A={okA} B={okB} C={okC}")
