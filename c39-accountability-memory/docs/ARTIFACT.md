# C39 reproducibility artifact

Companion to *How Much Memory Does Accountability Cost? Exact
Reconstruction–Incentive Frontiers for Compressed Multi-Agent Records*
(AAMAS 2027 main track, COINE).

Everything the paper claims numerically is either recomputed here from scratch
with no solver, or is a MILP result whose **witness** is frozen and re-checked
without a solver. The two exceptions — claims that need a solver and cannot be
re-checked from a witness — are listed in §4 and are stated as such in the paper.

---

## 1. Verify it — three commands, no network, no solver

In the pinned environment (`environment.json`: Python 3.10.11, NumPy 2.2.6,
SciPy 1.15.3; a venv is at `.venv310`):

```powershell
.\.venv310\Scripts\python.exe run.py verify     # integrity, then 99 solver-free checks
.\.venv310\Scripts\python.exe run.py audit      # every printed number vs its artifact
.\.venv310\Scripts\python.exe run.py score      # the pre-registered predictions
.\.venv310\Scripts\python.exe run.py figures    # regenerate every figure
```

`run.py verify` prints `MANIFEST EXACT` and then
`ALL CHECKS PASSED` and exits 0. Neither touches the network, a solver, or a
search. Expected total runtime: a few seconds.

To rebuild the frozen MILP witnesses from scratch instead of trusting them
(this *does* need the solver, HiGHS via `scipy.optimize.milp`):

```powershell
.\.venv310\Scripts\python.exe make_certificates.py   # rewrites certified_codes.json
```

## 2. What `verify_all.py` actually proves

| block | checks | content |
|---|---|---|
| A | 4 | `gamma_2(Q_n)` for `n = 1..4` by complete enumeration of all `2^(2^n)` subsets — no MILP anywhere in the loop. Fixes the invariant the paper reduces to. |
| B | 20 | For `(n,K) = (3,4), (5,10), (6,16), (7,32), (9,128)`: the stored code is 2-dominating; the induced record achieves `D = D_0(K)` exactly; its margin equals `1 - 1/d_min`; and that margin is `>= 1/2`. This is the sufficiency half of Theorem 3, re-derived from the centres alone. |
| C | 7 | The shell counting bound. It excludes every `K <= 3` (n=3), `<= 9` (n=5), `<= 28` (n=7), `<= 93` (n=9), and it does **not** exclude any known flat point — so it is tight, not merely valid, wherever the truth is known. |
| D | 4 | The one-bit frontier closed form against the explicit record at `n = 3,5,7,9`; max deviation `2.2e-16`, `4.4e-16`, `1.8e-15`, `2.4e-14`. |
| E | 21 | Every step of the general-`n` decoder-pair argument (Appendix A.1, Proposition 14): the identity `E[Delta^-] = (1/2)E|R_(p+m)|` on every orbit, monotonicity of `E|R_k|`, the bound over **all** `4^n` reconstruction pairs at `n = 3,5` and all `(p,m)` orbits at `n = 7,9`, and feasibility of the minimiser `r*`. Every deviation is exactly `0`. |
| F | 25 | Section 6's engineering table recomputed from the two bounds on `gamma_2(Q_n)`: the compression ratio `C(n)` and the free-bit figures at `n = 3,5,7,9,20,50`, that the bounds bracket every known `K_flat`, that `C(n) <= (n+2)/2` everywhere, and the two concrete claims in the text (`n = 20` needs `K` in `[95326, 131072]`, i.e. 16.5-17.0 of 20 bits). |
| G | 44 | Both directions of the tilted-prior threshold `K_flat = 2^n-(n-1)` at `n = 3,5,7,9,11,13`: the witness is 2-dominating with `d_min = 2`, its complement is a minimum-mass set at every tilt, no minimum-mass complement of size `n` is 2-dominating, and the collapse of the free ratio to `1 + O(n 2^-n)`. Cross-checked against the MILP sweep at `n = 3,5,7`. |

`verify_all.py` is an **independent reimplementation**: it shares no code with
`kflat_theory.py`, which produced the results. A bug common to both would have
to be reintroduced twice.

## 3. Environment provenance

`environment.json` pins Python 3.10.11 / NumPy 2.2.6 / SciPy 1.15.3
(`matches_pinned: true`). Session 2's numbers were originally computed under
3.12.3 / 2.4.4 / 1.17.1, which does **not** match the pin, so they were re-run:

| re-run | outcome |
|---|---|
| `exp1b_results.json`, `gamma2_sequence.json`, `shell_exclusion.json` | reproduce the pre-pin outputs byte for byte except for `seconds` timing fields; the pre-pin copies are kept in `prepinned_backup/` for diffing |
| `gamma2_n9_lb_rerun.json` | re-proves `K = 92..96` infeasible for 2-domination of `Q_9` under the pin — this is what carries `K_flat(9) >= 97`, and `gamma2_big.log` had it only from the unpinned run |
| `verify_t1_independent.json` | the independent Theorem 1 check, run to completion (session 1 stopped it at `n=9`, `gamma=1/18`): three implementations agree with the closed form to `8.5e-14` at every `n` and `gamma` |

No result in the paper rests on a number produced outside the pin.

## 4. What is *not* verified here, and why

* **MILP infeasibility at `n=7, K=29,30,31` and `n=9, K=92..96`.** Infeasibility
  has no small witness, so it cannot be re-checked solver-free. The logs
  (`gamma2_sequence.log`, `gamma2_n9_lb_rerun.log`) record HiGHS status 2
  (proved infeasible, not a time-out) for each, and the runs are reproducible
  with `make_certificates.py` / `gamma2_n9_lb_rerun.py`.
* **`K_flat(9)` exactly.** Open in `[97, 128]`. Three routes failed and are
  recorded as failures in `research_state.md` §2: MILP feasibility at
  `K = 98..124` (no termination in 40 min each), shrink-only local search (the
  algebraic code has zero internal edges, so it cannot move), and
  destroy-and-repair (70,685 trials, never beat 128).
* **Any closed form for `gamma_2(Q_n)`.** There is none; matching bounds exist
  only at `n = 3, 5, 7`.
* **That real agent records fall on either side of the threshold.** This is an
  empirical question; `P4_ADDENDUM_2026-09-14.md` argues the stakes are present
  but does not settle which side a given deployment sits on.

Session 1's conjecture `K_flat(n) = ceil(2^(n+1)/(n+2))` is **falsified** — it
fails at `n = 7` (predicts 29, truth is 32). It is reported as falsified in the
paper and its refutation is reproducible here.

## 5. File map

| file | role |
|---|---|
| `src/kflat_theory.py` | the method: Lemma 3', the construction, 2-domination models, solver-free verification |
| `src/verify_all.py` | the independent re-check; one command, no solver |
| `src/audit_paper_numbers.py` | parses the LaTeX and checks every printed number against the JSON artifact it came from; reports UNSOURCED claims rather than skipping them |
| `src/make_certificates.py` → `results/certified_codes.json` | freezes the MILP witnesses so §1 needs no solver |
| `src/make_figures.py` → `paper/figures/` | Figure 1 as pgfplots source, not an image |
| `src/check_manifest.py` / `src/update_hashes.py` → `artifact_hashes.json` | sha256 of every file in the archive |
| `src/make_artifact.py` | rebuilds the submission zip from the manifest |
| `environment.json` | the pin, and `matches_pinned` |
| `docs/research_state.md` | what is claimable and what is not — the authoritative status |
| `docs/experiment_log.md` | chronological record, including the runs that failed |
| `paper/` | LaTeX source; see `paper/README.md` |
| `prepinned_backup/` | pre-pin outputs, kept only as evidence for §3 |

## 6. Rebuilding the archive

```powershell
.\.venv310\Scripts\python.exe update_hashes.py    # refresh the manifest
.\.venv310\Scripts\python.exe make_artifact.py    # -> c39_artifact_YYYYMMDD.zip
```

`make_artifact.py` refuses to package a stale manifest. The zip contains exactly
the manifest's files plus the manifest and `prepinned_backup/`, so unzipping and
running the two commands in §1 reproduces `MANIFEST EXACT` and
`ALL CHECKS PASSED` on a clean machine.
