| judge | runs | items scored identically | t (run 1) | t (worst case, deploy) | main safe automated | held-out destructive allowed | held-out safe automated | vendor 0.9 main false allows | vendor 0.9 held-out destructive allowed |
|---|---|---|---|---|---|---|---|---|---|
| gpt-oss-120b | 3 | 194/221 | 0.305 | 0.855 | 82% | **0/124** | 32/49 (65%) | 0/77 | 0/124 |
| gpt-oss-20b | 3 | 207/221 | 0.955 | 0.955 | 84% | **2/124** | 27/49 (55%) | 3/85 | 3/124 |
| gpt-oss-safeguard-20b | 3 | 61/221 | 0.995 | 0.995 | 1% | **0/124** | 0/49 (0%) | 3/86 | 1/124 |
| qwen3.8-27b | 3 | 220/220 | 0.955 | 0.955 | 75% | **0/124** | 7/48 (15%) | 8/101 | 6/124 |
| allam-2-7b | - | - | none | none | 0% (refuses) | 0 | 0 | 15/89 | 14/124 |
| gpt-oss-120b (gate prompt) | 3 | 161/180 | 0.405 | 0.405 | 100% | **0/108** | 35/49 (71%) | 0/69 | 0/108 |
| jev-1.13.0 (gate prompt) | 3 | 90/180 | 0.225 | 0.225 | 100% | **1/108** | 44/49 (90%) | 0/30 | 0/108 |
