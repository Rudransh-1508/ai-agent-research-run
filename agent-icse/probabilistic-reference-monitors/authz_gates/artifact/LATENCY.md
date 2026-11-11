# Gate decision latency (same machine; model-backed gates include network RTT)

Wall-clock seconds per decision, from the live main-corpus runs. Deterministic gates pay local compute only; model-backed gates pay a model round-trip.

| gate | kind | n | median (s) | p95 (s) |
|---|---|---|---|---|
| agentguards | model-backed | 346 | 0.64 | 1.23 |
| cc-safety-net | deterministic | 692 | 0.10 | 0.13 |
| dcg | deterministic | 692 | 0.01 | 0.03 |
| design | model-backed | 692 | 0.49 | 0.66 |
| jev-engineering | model-backed | 346 | 0.71 | 1.04 |
| jev-engineering(auto) | model-backed | 346 | 0.54 | 0.92 |
| jev-engineering(guard) | model-backed | 346 | 0.71 | 1.02 |
| jev-guard | model-backed | 346 | 0.59 | 1.06 |
| sdkks(cli) | model-backed | 346 | 0.27 | 6.39 |

## Design: fast path vs model path

Of 692 decisions, **322 (47%) were decided deterministically with no model call**; 370 paid the judge.

| path | n | median (s) | p95 (s) |
|---|---|---|---|
| deterministic (fast) | 322 | 0.09 | 0.15 |
| model | 370 | 0.56 | 0.69 |
