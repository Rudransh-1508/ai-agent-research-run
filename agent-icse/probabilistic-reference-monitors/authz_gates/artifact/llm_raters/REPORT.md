# Automated rater panel (n = 88, seed 20260929)

Blind sheet + rubric action definitions; allow / ask / deny. Supporting evidence only: rater models are also judges elsewhere in the study.

| rater | n | kappa (3-way) | agreement | kappa safe vs unsafe | allow<->deny inversions |
|---|---|---|---|---|---|
| gptoss120b | 88 | 0.707 | 81% | 0.989 | 0 |
| qwen3 | 88 | 0.741 | 83% | 0.955 | 0 |
| gptoss20b | 88 | 0.563 | 70% | 0.943 | 0 |
| allam7b | 88 | 0.148 | 38% | 0.432 | 19 |

| panel | items | Fleiss kappa among raters | majority vs corpus kappa | majority agreement | majority inversions |
|---|---|---|---|---|---|
| all (gptoss120b, qwen3, gptoss20b, allam7b) | 88 | 0.406 | 0.676 | 78% | 0 |
| strongest3 (gptoss120b, qwen3, gptoss20b) | 88 | 0.666 | 0.692 | 80% | 0 |
