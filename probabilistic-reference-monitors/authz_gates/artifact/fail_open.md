# Fail-open tabulation and P1-P4

## Full corpus (n=31)

| failure mode | fail-open | fail-closed | partial | undocumented | unclassifiable |
|---|---|---|---|---|---|
| timeout | 12 | 15 | 4 | 0 | 0 |
| http_429 | 11 | 16 | 4 | 0 | 0 |
| http_5xx | 11 | 16 | 4 | 0 | 0 |
| malformed_response | 12 | 15 | 4 | 0 | 0 |

- **P1**: supported=True — {"n_determinable": 31, "n_fail_open": 16, "fraction": 0.5161, "ci95": [0.3484, 0.6803], "threshold": 0.5}
- **P2**: supported=True — {"n_thresholds": 88, "n_no_derivation": 69, "fraction": 0.7841, "ci95": [0.6872, 0.8572], "threshold": 0.6}
- **P3**: supported=True — {"vendor_constants": [0.9, 0.5]}
- **P4**: supported=True — {"gates_citing_cross_evaluation": []}

## Held-out remainder (non-pilot gates) (n=15)

| failure mode | fail-open | fail-closed | partial | undocumented | unclassifiable |
|---|---|---|---|---|---|
| timeout | 3 | 9 | 3 | 0 | 0 |
| http_429 | 2 | 10 | 3 | 0 | 0 |
| http_5xx | 2 | 10 | 3 | 0 | 0 |
| malformed_response | 3 | 9 | 3 | 0 | 0 |

- **P1**: supported=False — {"n_determinable": 15, "n_fail_open": 6, "fraction": 0.4, "ci95": [0.1982, 0.6425], "threshold": 0.5}
- **P2**: supported=True — {"n_thresholds": 39, "n_no_derivation": 29, "fraction": 0.7436, "ci95": [0.5892, 0.8543], "threshold": 0.6}
- **P3**: supported=True — {"vendor_constants": [0.9, 0.5]}
- **P4**: supported=True — {"gates_citing_cross_evaluation": []}
