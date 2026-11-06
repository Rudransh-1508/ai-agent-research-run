import warnings, json; warnings.filterwarnings("ignore")
import exp_kflat
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[1]))
from c39.paths import data, out as outpath
out={}
print("=== p-median D0 vs generic D0Model ===", flush=True)
for n in [3,5]:
    for K in range(1, 2**n+1):
        a = exp_kflat.solve_D0_pmedian(n,K,time_limit=300)
        line=dict(n=n,K=K,pmedian=a["value"],pmed_recomp=a["D_recomputed"],gap=a["gap"],sec=a["seconds"])
        if n==3 or K<=4:
            b = exp_kflat.solve_D0(n,K,time_limit=300)
            line.update(generic=b["value"],generic_gap=b["gap"],generic_sec=b["seconds"],
                        dev=(None if b["value"] is None else a["D_recomputed"]-b["value"]))
        out[f"n{n}_K{K}"]=line
        print("  ",line, flush=True)
    json.dump(out, open(outpath("d0_pmedian_check.json"),"w", newline="\n"), indent=1, default=float)
