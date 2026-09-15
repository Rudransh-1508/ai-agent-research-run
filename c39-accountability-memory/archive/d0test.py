import exp_kflat, time, warnings
warnings.filterwarnings("ignore")
print('--- validate D0Model against UBModel(gamma=0) at n=3', flush=True)
for K in [2,3,4]:
    a = exp_kflat.solve_D0(3,K,time_limit=300)
    b = exp_kflat.solve(3,K,0.0,time_limit=300)
    print(f'  K={K}: D0Model={a["value"]:.10f} ({a["seconds"]}s) UBModel={b["value"]:.10f} ({b["seconds"]}s) dev={a["value"]-b["value"]:+.2e}', flush=True)
print('--- D0(K) at n=5', flush=True)
for K in [2,3,4,5,6,7,8,10,12,16]:
    a = exp_kflat.solve_D0(5,K,time_limit=300)
    print(f'  K={K:2d}: D0={a["value"]} recomputed={a["D_recomputed"]} gap={a["gap"]} [{a["seconds"]}s]', flush=True)
