# Experiment log — C39 / P0 (flatness threshold)

Session: 2026-09-13, Claude Code session 1.
Environment: Python 3.10.11 / NumPy 2.2.6 / SciPy 1.15.3 (venv `.venv310`),
HiGHS via `scipy.optimize.milp`. Matches the pinned reproducibility
environment exactly (`environment.json`, `matches_pinned: true`).

All rows below ran in the pinned environment. "certified" means MIP gap 0.0
AND agreement with an independent post-hoc recomputation; "inconclusive"
means the solve did not terminate with a zero gap, or the model can only
speak about binary payment decoders.

---

## E13 — Environment recreation

| item | result |
|---|---|
| Python 3.10.11 | OK |
| NumPy 2.2.6 | OK |
| SciPy 1.15.3 | OK |
| pinned match | true |

## E14 — Step 2 substitute: independent T1 validation

**The step-2 comparison as written could not be run.** `verify_incentive_distortion.py`
and `incentive_distortion_onebit_extension.py` are NOT present in this repo
checkout (neither are `research_state.md`, `experiment_log.md`,
`environment.json`, `artifact_hashes.json` — all were created fresh this
session). Substituted a newly written independent implementation,
`verify_t1_independent.py`, sharing no code with `exp1b.py`:

* Method A: single MILP in monotone-cone residual variables `r = q - gamma|s|`,
  coordinate-wise-MAP objective, 2n binaries, no decoder enumeration.
* Method B: exhaustive enumeration of all `4^n` min-branch sign patterns (n<=5).

| n | gammas | max abs dev A vs exp1b | max abs dev A vs closed form | max abs dev B vs A | status |
|---|---|---|---|---|---|
| 3 | 0, 1/12, 1/6, 1/4, 1/3 | 2.2e-16 | 2.2e-16 | 0.0 | certified |
| 5 | 0 .. 1/5 (5 pts) | 4.4e-16 | 4.4e-16 | 0.0 | certified |
| 7 | 0 .. 1/7 (5 pts) | 8.5e-14 | 8.4e-14 | n/a | certified |
| 9 | 0, 1/36, 1/18 | 3.6e-15 | 2.2e-15 | n/a | certified (values); Method A gap 0.32-0.38 at gamma>0, so A is an upper bound there that coincides with exp1b's exact LP enumeration |

`exp1b.py` rerun in the pinned environment reproduces T1 at n=3,5,7,9 with max
deviation 3.1e-15; orbit-vs-full cross-check exact at n=3,5; orientation
spread at n=3 = 0.0. **Three independent implementations agree.**

Note: the n=9 tail of `verify_t1_independent.py` (gamma = 1/12, 1/9) was cut
short when the process was killed; still unrun as of session 2.

## E15 — Step 3: bracket model validation

### Check A — `exp3_bracket.solve(mode="UB")` at K=2 vs T1 closed form

| n | gamma | UB | T1 | dev | MIP gap | status |
|---|---|---|---|---|---|---|
| 3 | 0 | 0.750000 | 0.750000 | -1.1e-16 | 0.0 | PASS |
| 3 | 1/12 | 0.812500 | 0.812500 | -4.4e-16 | 0.0 | PASS |
| 3 | 1/6 | 0.875000 | 0.875000 | -2.6e-15 | 0.0 | PASS |
| 3 | 1/4 | 0.937500 | 0.937500 | -4.3e-15 | 0.0 | PASS |
| 3 | 1/3 | 1.000000 | 1.000000 | -1.2e-15 | 0.0 | PASS |
| 5 | 0 | 1.562500 | 1.562500 | -3.1e-13 | 0.0 | PASS |
| 5 | 0.05 | 1.671875 | 1.671875 | -8.0e-15 | 0.0 | PASS |
| 5 | 0.10 | 1.781250 | 1.781250 | -3.6e-15 | 0.0 | PASS |
| 5 | 0.15 | 1.890625 | 1.890625 | -4.4e-16 | 0.0 | PASS |
| 5 | 0.20 | 2.000000 | 2.000000 | -8.9e-16 | 0.0 | PASS |

**Check A PASSES.** The bracket model reproduces T1 in the pinned
environment. Downstream work is not void.

### Check B — sparse `exp_kflat.UBModel` vs dense `exp3_bracket` (symmetry breaking OFF)

13 cases at (n,K) in {(3,2),(3,3),(3,4),(5,2),(5,3)} x gamma in {0, 0.5/n, 1/n}:
**all bit-identical (dev exactly 0.0)**. Remaining 2 cases at (5,3) were cut
short when the process was killed; rerun to complete.

### Check C — symmetry breaking does not change the optimum

**NOT RUN in session 1** (process killed before reaching it). **Run in
session 2 — see E22, PASS** (12 cases, max deviation 1.7e-13).

## E16 — D0(K) via the Hamming-cube K-median reduction

New: with optimal reconstruction, `D(q)` is linear in `q` for fixed
reconstruction points, so the gamma=0 optimum is deterministic nearest-centre
assignment and

    D0(K) = (1/2^n) * min_{|C|<=K} sum_s d_H(s, C),

the classical p-median problem. `solve_D0_pmedian` implements it: 2^n binaries,
tight relaxation.

Cross-validated against the generic `D0Model` MILP on every case where both
terminate (n=3, all K=1..8; n=5, K=1..4): max deviation **2.5e-11**, with
speedups up to ~4000x (n=5,K=4: 0.21s vs 121s).

Certified D0 table, n=5 (all MIP gap 0.0):

| K | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 14 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D0 | 1.5625 | 1.375 | 1.125 | 1.03125 | 0.875 | 0.78125 | 0.75 | 0.71875 | 0.6875 | 0.65625 | 0.625 | 0.5625 | 0.5 |

D0(5,2)=1.5625=M_5 and D0(5,3)=1.375 both match the values recorded in
`C39_UPDATE_2026-09-13.md`. D0 is strictly decreasing in K for n=3 and n=5
(needed as the premise of Lemma 2 below).

## E17 — Monolithic UB MILP at n=5 (ABANDONED)

12 processes, K in {3,4,5,6,7,8,9,10,11,12,14,16}, gamma in {0.1,0.15,0.19},
900 s per solve, symmetry breaking on. **No gamma row completed in ~15
minutes of wall time on any K.** The LP relaxation of the min-encoding is 0
(set z=1/2), so the bound is useless and branch-and-bound stalls. Recorded as
inconclusive and superseded by E18. Partial JSON (D0 rows only) in
`kflat_n5_K*.json`.

## E18 — Structural reduction (`kflat_structure.py`)

Three lemmas, stated and proved in the file header:

* **Lemma 1 (support restriction).** `D(q) = D0(K)` forces the label
  reconstruction points to form an optimal K-median code `C`, and forces each
  state to put mass only on labels whose centre is one of its NEAREST centres.
* **Lemma 2 (distinct centres).** If D0 is strictly decreasing at K, the K
  centres are pairwise distinct. (Premise verified numerically for n=3,5.)
* **Lemma 3 (flatness necessary condition).** A centre `c` has a unique
  nearest centre, so `q[c]` is a point mass. If a neighbour `t` of `c` has `c`
  as its only centre at distance 1, `q[t]` is a point mass on the same label,
  so the edge `(c,t)` has `d_i = 0` and `<p_i, d_i> = 0` for **every**
  `p_i in [0,1]^K`. Hence flatness requires: *every state at distance exactly 1
  from C has at least two centres at distance 1.*

**Counting corollary.** With `e` = edges inside C and `a` = non-centres at
distance 1: `nK = 2e + sum deg_C(t) >= 2e + 2a`, so `a <= nK/2 - e`, and

    N * D0(K)  =  sum_s d(s,C)  >=  a + 2(N - K - a)  =  2(N-K) - a  >=  2(N-K) - nK/2.

If `N*D0(K) < 2(N-K) - nK/2`, flatness at (n,K) is **impossible**.

This argument constrains arbitrary bounded payment decoders, not just binary
ones, so rows it excludes are genuine NON-FLAT results, not merely failures of
the UB model.

### E18a — n=3 control case (method validation), `kflat_structure_n3.json`

| K | D0 | N*D0 | rhs | counting verdict | codes (exhaustive) | gamma=0.1 | gamma=1/6 | gamma=1/3 |
|---|---|---|---|---|---|---|---|---|
| 2 | 0.750 | 6.0 | 9.0 | **NOT FLAT (proved)** | - | - | - | - |
| 3 | 0.625 | 5.0 | 5.5 | **NOT FLAT (proved)** | - | - | - | - |
| 4 | 0.500 | 4.0 | 2.0 | not excluded | 8 (yes) | FLAT certified | FLAT certified | FLAT certified |
| 5 | 0.375 | 3.0 | -1.5 | not excluded | 32 (yes) | FLAT certified | FLAT certified | FLAT certified |
| 6 | 0.250 | 2.0 | -5.0 | not excluded | 28 (yes) | FLAT certified | (run cut short) | (run cut short) |

All FLAT rows carry an explicit `(centres, q, p)` construction whose distortion
and worst-case per-agent margin are recomputed post hoc, and whose margin is
re-confirmed for GENERAL `p in [0,1]^K` via the elimination-theorem LP
(`general_p_margin`), not only for binary p.

**`K_flat(3) = 4`, reproduced exactly**, including the two non-flat rows
(K=2 matches T1's strict tradeoff; K=3 matches the open bracket LB 0.708 >
D0 0.625 recorded in the update). The method reproduces every previously
known n=3 value. Note the counting bound is TIGHT at n=3.

### E18b — n=5 counting bound (computed, not yet written to JSON)

`rhs = 2(32-K) - 2.5K`:

| K | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| N*D0 | 50 | 44 | 36 | 33 | 28 | 25 | 24 | 23 | 22 |
| rhs | 55 | 50.5 | 46 | 41.5 | 37 | 32.5 | 28 | 23.5 | 19 |
| flatness | **impossible** | **impossible** | **impossible** | **impossible** | **impossible** | **impossible** | **impossible** | **impossible** | not excluded |

**K_flat(5) >= 10, proved, for arbitrary bounded payment decoders.**

### E18c — n=5, K=16 explicit construction (`verify_k16_construction.py`)

Centres = the 16 even-weight vectors of `{0,1}^5`; even-weight states map to
their own label with probability 1; odd-weight states spread uniformly over
their 5 (even-weight) neighbours; `p_i[y] = (centre of y)_i`.

| quantity | value |
|---|---|
| D | 0.4999999999999992 |
| D0(16) | 0.5 |
| per-agent margin | 0.8, 0.8, 0.8, 0.8, 0.8 |
| payments | binary |
| solver used | none (direct enumeration) |

**K=16 is FLAT at n=5, certified**, with margin 0.8 — far above the largest
gamma in the session plan (0.19). Combined with E18b:

    10 <= K_flat(5) <= 16.

### E18d — n=5, K in {10,...,16}, `kflat_structure_n5.json`

gamma in {0.1, 0.15, 0.19}; code-enumeration limit 200.

| K | D0 | N*D0 | rhs | counting | codes (exhaustive) | g=0.1 | g=0.15 | g=0.19 |
|---|---|---|---|---|---|---|---|---|
| 10 | 0.68750 | 22.0 | 19.0 | not excluded | **16 (yes)** | FLAT cert. | FLAT cert. | FLAT cert. |
| 11 | 0.65625 | 21.0 | 14.5 | not excluded | 200 (no) | FLAT cert. | FLAT cert. | FLAT cert. |
| 12 | 0.62500 | 20.0 | 10.0 | not excluded | 200 (no) | FLAT cert. | FLAT cert. | FLAT cert. |
| 13 | 0.59375 | 19.0 | 5.5 | not excluded | 200 (no) | FLAT cert. | FLAT cert. | FLAT cert. |
| 14 | 0.56250 | 18.0 | 1.0 | not excluded | 200 (no) | FLAT cert. | FLAT cert. | FLAT cert. |
| 15 | 0.53125 | 17.0 | -3.5 | not excluded | 200 (no) | FLAT cert. | FLAT cert. | FLAT cert. |
| 16 | 0.50000 | 16.0 | -8.0 | not excluded | 200 (no) | FLAT cert. | FLAT cert. | FLAT cert. |

Every FLAT row stores an explicit `(centres, q, p)`, recomputes D and the
worst-case per-agent margin post hoc, and re-confirms the margin for GENERAL
`p in [0,1]^K` via the elimination-theorem LP. `general-p margin` equalled the
binary-p margin in every row, so the binary restriction costs nothing here.

Non-exhaustive enumeration at K>=11 does not weaken anything: those rows are
POSITIVE (a construction was exhibited), and one construction suffices.

Combined with E18b (K <= 9 proved impossible):

> **`K_flat(5) = 10`, exactly.**

### E18e — n=5, K=10 margin robustness

| gamma | 0.1 | 0.15 | 0.19 | 0.25 | 0.3 | 0.4 | 0.5 | 0.6 | 0.8 |
|---|---|---|---|---|---|---|---|---|---|
| verdict | FLAT | FLAT | FLAT | FLAT | FLAT | FLAT | FLAT | none (exh.) | none (exh.) |

Flatness at K=10 holds for `0 <= gamma <= 0.5`, i.e. 2.5x beyond T1's whole
feasible range `gamma <= 1/n = 0.2`. Not an artefact of small gamma. The
gamma=0.6/0.8 rows say only that no binary-p construction exists over all 16
codes; they are not general-p statements.

## E19 — n=7 counting bound, `kflat_n7_bound.json`

Bound only, no code enumeration and no margin search: this is a **proof**, not
a search. `rhs = 2(128-K) - 3.5K = 256 - 5.5K`. All D0 certified via p-median
(gap 0 or ~1e-15).

| K | 8 | 12 | 14 | 16 | 20 | 24 | 26 | 27 | 28 | 29 | 30 | 32 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D0 | 1.4375 | 1.15625 | 1.03125 | 0.875 | 0.84375 | 0.8125 | 0.796875 | 0.789062 | 0.78125 | 0.773438 | 0.765625 | 0.75 |
| N*D0 | 184 | 148 | 132 | 112 | 108 | 104 | 102 | 101 | 100 | 99 | 98 | 96 |
| rhs | 212 | 190 | 179 | 168 | 146 | 124 | 113 | 107.5 | 102 | 96.5 | 91 | 80 |
| flat? | **no** | **no** | **no** | **no** | **no** | **no** | **no** | **no** | **no** | possible | possible | possible |

Consistency check: `D0(7,16) = 0.875 = 7/8 = n/(n+1)`, exactly T2's
perfect-Hamming-code distortion at `K = 2^n/(n+1) = 16`. Independent
corroboration that the p-median reduction is computing the right object.

> **`K_flat(7) >= 29`, proved.** In particular `K = 14 = 2n` is proved
> impossible, so the linear scaling hypothesis is FALSE.

## E20 — Scaling

The counting bound, in the regime where optimal codes are dominating sets
(`D0(K) = (N-K)/N`), reduces to `K >= 2^(n+1)/(n+2)`.

| n | `ceil(2^(n+1)/(n+2))` | `K_flat(n)` found | `2n` | `n+1` | `2^(n-1)` |
|---|---|---|---|---|---|
| 3 | 4 | **4** (exact) | 6 | 4 | 4 |
| 5 | 10 | **10** (exact) | 10 | 6 | 16 |
| 7 | 29 | **>= 29** (bound) | 14 | 8 | 64 |

The bound is TIGHT at both n=3 and n=5. `n+1` is dead (n=5). `2n` is dead
(n=7: 14 proved impossible). `2^(n-1)` is dead (n=5: K_flat=10 < 16).

`2^(n+1)/(n+2) = Theta(2^n / n)` is **exponential in n**.

**Important**: this formula was written down in `research_state.md` and
`experiment_log.md` and hashed into `artifact_hashes.json` BEFORE the n=5
K=10 and the n=7 rows were computed (previous turn of this session). It is a
pre-registered prediction that then held, not a curve fitted after the fact.
The constructive side at n=7 is untested, so `K_flat(7) = 29` is a conjecture;
`K_flat(7) >= 29` is proved.

---

# SESSION 2 — 2026-09-13

Same pinned environment (3.10.11 / 2.2.6 / 1.15.3). Every row records its
MIP gap or states that no solver was used.

## E21 — Step 1: brute-force cross-validation of the D0 solver [GATING]

`bruteforce_d0.py`. No LP, no MILP anywhere in the reference.

* Method E: complete enumeration of every subset of the 2^n vertices.
* Method B: exact per-cardinality branch and bound. Admissible bound from
  submodularity of the marginal reduction plus a sphere-packing bound.
  Incumbents seeded by our own greedy, never by the p-median solver.

**B vs E (validating the reference itself):**

| n | subsets enumerated | E time | B nodes | B time | result |
|---|---|---|---|---|---|
| 3 | 256 | 0.0s | 56 | 0.0s | IDENTICAL at every K |
| 4 | 65536 | 0.8s | 10056 | 0.2s | IDENTICAL at every K |

**Brute force vs `exp_kflat.solve_D0_pmedian`:**

| n | K range | max abs diff | MIP gaps | verdict |
|---|---|---|---|---|
| 3 | 2..8 | 0.00e+00 | all 0.0 | exact match |
| 5 | 2..32 | 0.00e+00 | all 0.0 | exact match |

**VERDICT: PASS at every K, difference exactly zero.** The scaling work is not
void. B&B node counts at n=5: K=3 55, K=4 8, K=5 4176, K=6 19650, K=7 293;
all other K settled by the sphere bound with no search.

## E22 — Validation check C (session 1's never-run item)

`check_c_symbreak.py`. 12 cases, (n,K) in {(3,2),(3,3),(3,4),(5,2)} x 3 gammas.
Max |sym - nosym| = 1.7e-13. **CHECK C: PASS.**
Scope: session-2 results come from `kflat_theory.py`, which uses no symmetry
breaking anywhere, so C bears only on the superseded `exp_kflat.UBModel` rows.

## E23 — K_flat(n) = gamma_2(Q_n)

Derived from inspecting the certified n=5 K=10 code: centres are point masses,
non-centres split evenly over nearest centres, `p_i[y] = centre_y[i]`, zero
internal edges, every non-centre with >= 2 centre-neighbours.

Lemma 3' (necessity) and the explicit construction (sufficiency) are stated
and proved in `kflat_theory.py`. Margin of the construction is exactly
`1 - 1/d_min`.

Equivalence check against the already-established values:

| n | gamma_2 found | known K_flat | infeasible below | construction check (no solver) |
|---|---|---|---|---|
| 3 | 4 | 4 | K=2,3 proved infeasible | D=D0=0.5, margin 0.6667 |
| 5 | 10 | 10 | K=8,9 proved infeasible | D=D0=0.6875, margin 0.5 |

MATCH at both. Solve times ~0.01s versus hours for the encoder search.

## E24 — Shell counting bound (strengthens session 1's corollary)

Every state at distance r needs >= 2 centres at distance exactly r, and there
are at most `K*C(n,r)` (state,centre) pairs at distance r, so shell r holds at
most `floor(K*C(n,r)/2)` states. Filling shells inward bounds `N*D0` below.

Sanity (must NOT exclude known flat points): n=3 K=4 shell=4 vs N*D0=4;
n=5 K=10 shell=22 vs 22; n=7 K=32 shell=96 vs 96. Tight, excludes none.

Coverage gained over session 1's bound: n=7 K=2,3,4,5; n=9 K=2..13.
After it, the only unexcluded K below the threshold are n=7 K=29,30,31 and
n=9 K=94,95,96 — all of which the 2-domination MILP proves infeasible.

## E25 — K_flat(7) = 32 EXACT

| K | evidence | gap/status |
|---|---|---|
| 2..28 | shell bound | no solver |
| 29 | 2-domination MILP infeasible | status 2, 0.99s |
| 30 | 2-domination MILP infeasible | status 2, 2.04s |
| 31 | 2-domination MILP infeasible | status 2, 24.1s |
| 32 | explicit code, verified solver-free | D=D0=0.75, margin 0.5, min_deg 2 |

**Session 1's conjecture K_flat(7)=29 is FALSIFIED. The bound >=29 was correct.**

## E26 — K_flat(9): 97 <= K_flat(9) <= 128

| K | evidence | gap/status |
|---|---|---|
| 2..93 | shell bound | no solver |
| 94, 95, 96 | 2-domination MILP infeasible | status 2; 23.0s, 25.4s, 122.5s |
| 97..127 | UNRESOLVED | MILPs did not terminate |
| 128 | explicit algebraic code, verified solver-free | D=D0=0.75, margin 0.6667, min_deg 3 |

Session 1's formula predicts 94 — **excluded**. The figure 57 quoted in the
session-2 brief corresponds to `2^n/n`, not to `2^(n+1)/(n+2)`; the formula's
own value at n=9 is `ceil(1024/11) = 94`. Both are ruled out.

Three routes failed to tighten the upper bound: feasibility MILPs at
K=98..124 (no termination in 40 min each); shrink-only local search (cannot
move — the code has zero internal edges, so deleting any centre leaves it with
no centre-neighbour); destroy-and-repair, **70,685 trials**, never beat 128.

## E27 — Algebraic construction (`linear_2dom.py`)

`C = ker H`, H with no zero column and every nonzero syndrome used >= 2 times,
gives `gamma_2(Q_n) <= 2^(n - floor(log2(n/2+1)))`. Verified solver-free:

| n | 3 | 5 | 7 | 9 | 11 | 13 | 15 |
|---|---|---|---|---|---|---|---|
| size | 4 | 16 | 32 | 128 | 512 | 2048 | 4096 |
| 2-dominating | yes | yes | yes | yes | yes | yes | yes |
| min_deg | 3 | 5 | 2 | 3 | 3 | 4 | 2 |
| flat (D=D0) | yes | yes | yes | yes | yes | - | - |

Tight at n=3 and n=7 (matches gamma_2 exactly); loose at n=5 (16 vs 10).

## E28 — Compression ratio C(n) = 2^n / K_flat(n)

| n | 3 | 5 | 7 | 9 | 20 | 50 |
|---|---|---|---|---|---|---|
| C(n) | 2.00 | 3.20 | 4.00 | 4.00–5.28 | 8–11 | 16–26 |
| (n+2)/2 | 2.50 | 3.50 | 4.50 | 5.50 | 11 | 26 |
| free bits log2 C(n) | 1.00 | 1.68 | 2.00 | 2.00–2.40 | 3.00–3.46 | 4.00–4.70 |
| free bits as % of n | 33.3% | 33.6% | 28.6% | 22.2–26.7% | 15.0–17.3% | 8.0–9.4% |

`(n+2)/2` is an upper bound on C(n), not its value. C(n) = Theta(n) survives.
See research_state.md section 4 for the two normalisations and the restated
P4 conclusion.

## E29 — Pinned-environment re-run completed; artifact package sealed (2026-09-15)

`environment.json` pins Python 3.10.11 / NumPy 2.2.6 / SciPy 1.15.3. Session 2
computed its numbers under 3.12.3 / 2.4.4 / 1.17.1. Everything has now been
re-run under the pin.

| re-run | result |
|---|---|
| `exp1b_results.json`, `gamma2_sequence.json`, `shell_exclusion.json` | identical to the pre-pin outputs except `seconds` fields; pre-pin copies kept in `prepinned_backup/` |
| `gamma2_n9_lb_rerun.py` → `.json`/`.log` | n=9, K=92..96 all **INFEASIBLE (proved)**, HiGHS status 2, agreeing with `gamma2_big.log` row for row |

The n=9 rows were the outstanding gap: `K_flat(9) >= 97` rested on
`gamma2_big.log`, which was produced *before* the pin and was never re-run.
Timings under the pin are faster (K=94: 11.4s vs 23.0s; K=95: 12.7s vs 25.4s;
K=96: 70.6s vs 122.5s) but every verdict is unchanged. K >= 97 was deliberately
not attempted — it does not terminate, and the lower bound does not need it.

**No number in the paper now rests on a run made outside the pinned environment.**

Artifact package, all of it solver-free except where noted:

| script | role |
|---|---|
| `verify_all.py` | 35 checks, independent reimplementation, no solver — passes (56 after E30) |
| `check_manifest.py` | NEW. sha256 of every archived file vs `artifact_hashes.json`; exit 1 if stale |
| `make_artifact.py` | NEW. builds `c39_artifact_YYYYMMDD.zip`; refuses a stale manifest |
| `ARTIFACT.md` | NEW. referee-facing README: what each check block proves, what is **not** verified, environment provenance |

Correction while writing it: `paper/README.md` claimed `verify_all.py` runs 40
checks. It runs 35 (A:4, B:20, C:7, D:4). Fixed in both places.

## E30 — Appendix A step 5 closed: the antipodal decoder pair is optimal for general odd n (2026-09-15)

The paper's one open technical item (`paper/README.md`, "the one open technical
item"; `C39_UPDATE_2026-09-13.md` §1.2) is now a proof rather than a verified
conjecture. Setting `Delta_{a,b}(s) = d_H(s,b) - d_H(s,a)`, the K=2 objective
splits as `D = n/2 + E[q(S) Delta(S)]`, and on the feasible set
`q = gamma*|s| + r`, `0 <= r <= 1-n*gamma`, the box constraint alone gives

    D >= n/2 + gamma*E[|S| Delta] - (1-n*gamma)*E[Delta^-]  =:  L(a,b).

Partition the coordinates of the pair: `p` positions with `(a_i,b_i) = (0,1)`,
`m` with `(1,0)`. Then

  * `E[|S| Delta] = -(p-m)/2`  (each coordinate contributes -1/2 or +1/2);
  * `-Delta(S) = X - Y` with X, Y independent Rademacher sums of length p and m,
    so `-Delta =d R_{p+m}` and `E[Delta^-] = E[R_{p+m}^+] = (1/2) E|R_{p+m}|`;
  * `E|R_k|` is nondecreasing in k, by conditional Jensen on `|.|`.

Since `p-m <= n` and `p+m <= n` and `1-n*gamma >= 0`, both terms are dominated by
the antipodal pair `(0^n, 1^n)`, where the bound is attained by
`r* = (1-n*gamma)*1{|s| > n/2}` — an up-set indicator, hence monotone, hence
feasible. Collecting terms with `(1/2)E|R_n| = n/2 - M_n` gives exactly
`M_n + n*gamma*((n-1)/2 - M_n)`.

The proof needs **no permutation averaging**, which is what the old proof-order
bug was about (under optimal decoding D is concave in q, so averaging runs the
wrong way), and **no orbit enumeration**: the binom(n+3,3) reduction is now only
a verification device.

Machine-checked as `verify_all.py` block E, 21 new solver-free checks: the
Rademacher identity on every orbit, monotonicity of `E|R_k|`, the bound over all
4^n decoder pairs at n=3,5 and all (p,m) orbits at n=7,9, and feasibility of
`r*`. Every deviation is exactly 0.00e+00. `verify_all.py` now runs **56 checks**
(was 35) and still uses no solver.

## E31 — Paper draft completed and building (2026-09-15)

| item | state |
|---|---|
| build | `pdflatex/bibtex/pdflatex x2` clean under MiKTeX: no errors, no undefined refs or citations |
| length | 8 pages total — body (§1–§8) ends p6, references p6, appendix to p8 |
| appendix | written in full: Theorem 1 Steps 1–5, both threshold lemmas with the case analysis, shell bound, reproduction instructions |
| abstract | trimmed 312 -> 224 words |
| intro | roadmap paragraph added |
| refs.bib | 4 -> 18 entries, all cited; 7 flagged FIELDS INCOMPLETE (identifier held, author list not) |
| fixes | certificate table declared 4 columns for 5 (silent misalignment); `\Bbbk` clash with acmart; three overfull displays rebroken |

Left for a human: author block and registration, the official AAMAS class file
(one line in `main.tex`), and completing the 7 bibliography entries from
publisher records rather than reconstructing them.

## E32 — verify_t1_independent.py: the n=9 tail, run at last (2026-09-15)

Session 1 left this script cut short at n=9, gamma=1/18; `research_state.md` §6
carried it as an open loose end. It has now run to completion in the pinned
environment, all four n and all five gamma values each.

| n=9 gamma | method A (MILP) | exp1b (orbit LP) | closed form | MIP gap |
|---|---|---|---|---|
| 0      | 3.269531250000 | same | same | 0.0 |
| 1/36   | 3.452148437500 | same | same | **0.26** |
| 1/18   | 3.634765625000 | same | same | 0.0 |
| 1/12   | 3.817382812500 | same | same | 0.0 |
| 1/9    | 4.000000000000 | same | same | 0.0 |

Worst deviation across all n and gamma: `|A - exp1b| = 8.5e-14`,
`|A - closed form| = 8.4e-14`, `|B - A| = 7.2e-15` (B = exhaustive branch
enumeration, n<=5 only). n=9 took 1450s.

**One honest caveat.** At n=9, gamma=1/36 the MILP hit its 600s limit with a
relative gap of 0.26, so method A there is an incumbent that happens to equal the
closed form, not a solver-certified optimum. Nothing depends on it: the
exhaustive-orbit LP is exact (LPs have no integrality gap) and agrees, and
Proposition 14 now proves the value outright. The other two previously
gap-carrying rows (1/36 and 1/18 in the pre-pin run, gaps 0.38 and 0.32) closed
to 0.0 under the pin.

With this, `research_state.md` §6 has no remaining loose ends: check C ran in
session 2, the n=3 K=6 control ran, and the n=9 tail is done.

## E33 — Verification extended to the engineering table; two dangling refs fixed (2026-09-15)

An audit of the draft for placeholders and dangling cross-references turned up
two real gaps and one verification hole.

* **Figure 1 was never cited in the text.** A float that nothing references is a
  copy-editing defect; §4 now points at it, and §1's roadmap points at
  Appendix A. Remaining unreferenced labels are all non-floats (two remarks, a
  definition, two appendix subsection anchors), which is fine.
* **Table 3 (the compression-ratio table) was not machine-checked.** It is the
  table §6's whole engineering argument rests on, and every number in it was
  hand-derived. `verify_all.py` block F now recomputes all of it from the two
  bounds on `gamma_2(Q_n)`: `C(n)` and the free-bit figures at
  n = 3,5,7,9,20,50; that the bounds bracket every known `K_flat`; that
  `C(n) <= (n+2)/2` everywhere; and the two concrete sentences in the text
  (n=20 needs K in [95326, 131072], i.e. 16.54-17.00 of 20 bits; n=50 gives
  45.30-46.00 of 50).

All 25 new checks pass. `verify_all.py` is now **81 solver-free checks**
(35 -> 56 -> 81 across E30 and this entry).

## E34 — The uniform prior is load-bearing: K_flat = 2^n - (n-1) under any tilt (2026-09-15)

Started as a check of §8's first limitation ("a non-uniform prior breaks the
proof technique") and turned into a theorem plus a corollary.

**Observation that opens it.** Condition (M) is an all-teammate-profile
condition — it never mentions the prior. Only D and D_0 do. So the threshold
question is well posed for any full-support prior, and both lemmas of §5 survive
verbatim:

    K_flat(pi) = min { K : some pi-optimal K-median set of size K is 2-dominating }

Necessity is Lemma 3' (prior-free). Sufficiency: a 2-dominating C is dominating,
so the Lemma-2 record costs exactly 1 - pi(C), which equals D_0(K) precisely when
C is pi-optimal. Uniform is the special case where every dominating K-set is
optimal, and Theorem 3 is recovered.

**The threshold moves, and a long way.** For a product Bernoulli(q) prior with
q != 1/2, pi is strictly monotone in |s|, so the maximum-mass K-sets are the K
heaviest vertices. Then:

* if 2^n - K >= n, every minimum-mass complement contains 0^n and at least n-1 of
  the n weight-one vertices, leaving 0^n with at most one neighbour in C — not
  2-dominating, so not flat;
* at K = 2^n - (n-1), C = complement of {0^n, e_1..e_{n-2}} is a maximum-mass
  K-set, is 2-dominating with d_min = 2, and gives margin exactly 1/2.

So **K_flat(Bernoulli(q != 1/2)) = 2^n - (n-1)**, whatever the tilt.

| n | uniform K_flat | tilted K_flat | C(n) uniform | C(n) tilted |
|---|---|---|---|---|
| 3 | 4 | 6 | 2.00 | 1.333 |
| 5 | 10 | 28 | 3.20 | 1.143 |
| 7 | 32 | 122 | 4.00 | 1.049 |
| 9 | [97,128] | 504 | 4.00–5.28 | 1.016 |
| 20 | >= 95326 | 2^20 - 19 | 8–11 | 1.000018 |

The free compression ratio collapses from Theta(n) to 1 + O(n 2^-n). At n=20 the
free allowance falls from 3.0–3.5 bits to 2.6e-5 bits. Note there is no smooth
degradation as q -> 1/2: for every q != 1/2 the mass ordering is strict and the
argument applies unchanged.

**Two independent routes agree.** `prior_threshold.py` solves, at each K, a
weighted K-median MILP and a maximum-mass 2-domination MILP and reports the least
K at which they meet: 6, 28, 122 at n=3,5,7. The solver-free argument above gives
the same, and extends to n=11,13. Both are in `verify_all.py` block G (44
checks). Total is now **125 solver-free checks**.

**Why it matters for the paper.** It converts §8's first limitation into
Theorem 11 + Corollary 12 (new §5.7), and it strengthens §6 rather than weakening
it: the uniform prior is the *most favourable* case for accountability, so the
engineering numbers were conservative. The mechanism is quotable — optimal
reconstruction under a tilted prior spends its labels on the likely profiles, and
the profiles it abandons are exactly the ones that become invisible to a
unilateral deviation.

Paper is now 9 pages: body to p7 (limit is 8 excluding references), references,
appendix to p9.

## E35 — Literature check on K_flat(9), and a reviewer-proofing pass (2026-09-15)

**Track C (timeboxed, closed).** Searched for a published value or bound for
`gamma_2(Q_9)`. There is none findable. What the literature does have is the
*ordinary* domination number, known exactly for n <= 9 with `gamma(Q_9) = 62`
(Ostergard and Blass, 2001, "On the size of optimal binary codes of length 9 and
covering radius 1"), and the multiple-covering tables, which give `K(9,1) = 62`
for mu = 1 but no mu = 2 entry we could locate. Conclusion: `97 <= K_flat(9) <=
128` stands, and may be the tightest bracket on record. Recorded rather than
retried.

Two things came out of the search that are worth keeping:

* **The dominating-regime restriction never binds.** Lemma 2 needs
  `K >= gamma(Q_n)`, and `gamma(Q_n) = 2, 7, 16, 62` at n = 3,5,7,9 — far below
  every threshold we report (4, 10, 32, >=97). Now stated in §5 with the
  citation, closing a question a referee would otherwise have to ask.
* **A coincidence, checked and rejected.** `gamma_2(Q_3) = 4 = gamma(Q_4)`,
  `gamma_2(Q_6) = 16 = gamma(Q_7)`, `gamma_2(Q_7) = 32 = gamma(Q_8)`. Three
  matches invites the guess `gamma_2(Q_n) = gamma(Q_{n+1})`. It is **false**: at
  n = 5, `gamma_2(Q_5) = 10` but `gamma(Q_6) = 12`. This project has already been
  burned once by a formula fitted to three points, so the paper now names the
  coincidence and kills it in §5 rather than leaving a referee to spot it.

**Track D (reviewer-proofing).** Walked the seven objections in
`C39_PAPER_PLAN_AAMAS2027.md` §6 against the draft. All seven are answered in
text: (1) one bit per agent is the flat case — §6; (2) not the CEO problem — §7;
(3) gamma_2 is not ours — §5 and §7; (4) where is the real system — §1, §6, §8;
(5) toy model — §8, and the prior half of it is now a theorem (E34); (6) the
margin condition is deliberately strong — §2; (7) is n=7 right — §5, two
independent routes. No gaps found, so nothing was added beyond the two items
above.

## E36 — Verification audit: what was wrong, and what now catches it (2026-09-15)

No new claims. This entry audits the claims already made. Two questions were
asked of every number: *is it true*, and *does anything actually check that it is
true* — a suite that cannot fail verifies nothing.

**Defects found and fixed.**

1. **A wrong number in the paper.** §5 quoted the Fink–Jacobson bound at n=9 as
   `93.9`. It is `2^10/11 = 93.09`. Corrected. Found by the new audit script,
   not by reading.
2. **A cross-check that checked nothing.** `verify_all.py` block G compared the
   solver-free threshold against `MILP_VALUES = {3: 6, 5: 28, 7: 122}` — three
   constants typed by hand. Worse, the n=7 value had **no saved artifact at
   all**: it came from an ad-hoc terminal run that was never written to disk,
   while the paper claimed MILP verification at n=3,5,7. Block G now *reads*
   `prior_threshold.json` and the new `prior_threshold_n7.json`, so a
   disagreement between solver and argument fails the suite.
3. **A silent skip.** When those artifacts were absent, block G printed a warning
   and the suite still exited 0, quietly dropping three checks. Missing artifacts
   now fail.
4. **A mis-citation.** VICT (arXiv:2608.28128) was cited in the trace-compression
   paragraph of §7. It is a credit-assignment paper. Moved to the credit
   assignment paragraph, where it is the strongest agent-era citation we have.
5. **A vacuous check I wrote myself.** The first draft of the audit contained
   `claim(..., f"${x}$" or True, ...)` — always true — and compared `M_n` against
   a constant restated in the audit rather than the number printed in Table 1.
   A deliberately corrupted `M_n` slipped through. Both fixed: the audit now
   parses Table 1 and Table 3 out of the LaTeX.

**The n=7 MILP evidence, properly recorded.** `prior_threshold.py` scans K upward
and is hardest at *small* K (128 candidate centres, 16384 assignment variables,
loose relaxation); it does not reach K≈122 in reasonable time and was killed.
That all smaller K fail is combinatorial, not computational, and is checked
solver-free. What a solver adds is confirmation of the *transition*, so
`prior_threshold_n7.py` records the MILP verdict on K = 117..125 at three tilts:
first flat K = 122 in every case.

**Mutation testing — do the suites fail when they should?**

| suite | mutations injected | caught |
|---|---|---|
| `verify_all.py` | corrupt a frozen MILP witness; wrong published C(5); wrong tilted witness; perturbed closed form; off-by-one shell capacity; non-antipodal pair; wrong gamma_2(Q_4); wrong K_flat(9) bracket | **8/8** |
| `audit_paper_numbers.py` | wrong M_n; deviation inflated 1000x; deviation claimed nonzero; wrong trial count; wrong shell entry; wrong n=20 bound; wrong Fink–Jacobson value; deleted internal-edge claim | **8/8** |
| `verify_all.py` (artifact tampering) | n=7 artifact edited to say 121; artifact deleted | **2/2** |

**Bibliography: every entry verified against the source.** All 19 entries were
checked against the publisher record, arXiv listing or DOI on 2026-09-15. Nothing
is reconstructed from memory. Corrections: the multifold-packings entry had an
approximate title and no authors (it is Krotov and Potapov, *On multifold
packings of radius-1 balls in Hamming graphs*, IEEE TIT 2021); Fink–Jacobson is
an `@incollection` with pages 283–300, Wiley, not an article; Chellali et al. is
*Graphs and Combinatorics* 28(1):1–55; Östergård–Blass is IEEE TIT 47:2556–2557;
the CCS poster is Liu, Yu and Steeves, *Poster: Solving the Free-rider Problem in
Bittensor*. Seven entries previously marked FIELDS INCOMPLETE are now complete;
**none remain**.

**One live-source caveat, recorded rather than hidden.** Both Bittensor
documentation URLs now 301-redirect to `bittensor.com/docs` — the docs domain
moved during 2026. The documents themselves are still indexed under the cited
titles and dates, and the `1800` blocks (5 tempos) figure in §6 was re-confirmed
independently. The bib entry states the redirect instead of presenting a dead
link as live.

**Checked and found correct, no change needed:** every cell of Tables 1, 2 and 3;
all shell exclusions against `shell_exclusion.json`; every MILP infeasibility
status (including that n=7 K=28 is also infeasible, which the table does not need
to claim); the 70,685 destroy-and-repair trials; the zero-internal-edges fact;
the n=20 and n=50 bit ranges; the gamma(Q_n) values and the gamma_2/gamma
coincidence together with its n=5 counterexample; and the environment triple.

## E37 — The mechanism experiment, pre-registered and scored (2026-09-15)

Built in response to a review whose decisive objection was empirical validation
3/10. Predictions were written to `PREREGISTRATION_2026-09-15.md` and hashed into
`artifact_hashes.json` **before** the harness existed; `analyse_experiment.py`
scores them mechanically so the prose does not get to decide what the results
mean.

**Design.** Named compaction mechanisms nobody designed to be optimal — `count`,
`threshold`, `prefix-m`, `top-k`, `hash-K` — plus the Lemma-8 construction and
the optimal quantiser. Every profile is enumerated, so the numbers are exact:
no sampling, no seed, no error bars. The margin is measured **via Theorem 3**,
one LP per agent, so the experiment uses the paper's own tool as its instrument.
Noise: effort is observed through a bit-flip channel of rate eta.

**Results.**

| prediction | outcome |
|---|---|
| P1 [D] nothing beats the frontier | CONFIRMED |
| P2 [D] nothing below gamma_2 is flat | CONFIRMED |
| P3 [D] same K, same D, opposite accountability | CONFIRMED |
| P4a [U] gamma(count) = 1 | **FALSIFIED** — it is exactly 1/n |
| P4b [U] count is reconstruction-poor | CONFIRMED |
| P5 [U] margin falls monotonically with noise | **FALSIFIED** — non-monotone |
| P6 [U] noise prevents the unrestricted optimum | CONFIRMED |
| P7 [U] tilt kills flatness below 2^n-(n-1) | CONFIRMED |
| P8 [U] partial per-agent retention gives zero | CONFIRMED |

**The headline.** At n=5, `flat` and `kmedian` use the same 10 labels and incur
the same distortion 0.6875 = D_0(10). One has margin 1/2; the other has margin
exactly 0, for any bounded payment at any price. A designer comparing records on
reconstruction quality cannot see the difference. Same at n=3 (2/3 against 0).

**Why P4a was wrong, and why it matters.** We reasoned from the point-mass edge
condition: one agent's deviation moves the count by exactly one, so the margin
should be 1. But Theorem 3 minimises over *mixtures* of teammate profiles, and a
uniform mixture telescopes — the intermediate shifts cancel and only the two
endpoints survive, leaving exactly 1/n (0.3333 at n=3, 0.2000 at n=5). This is
the clearest demonstration we have that the elimination theorem is needed rather
than its corollary. We also predicted D(count)=1.0 at n=3 and measured 0.75: the
hand calculation wrongly restricted the Bayes reconstruction to profiles of the
observed weight, when the true Bayes pick is 0^n or 1^n.

**An unforeseen effect.** Noise *creates* margin where a deterministic record had
none — six mechanism-instances go from gamma=0 to positive at eta=0.1, including
`kmedian` 0 -> 0.1973 at n=5. A deterministic record is blind to an agent whose
flip does not change the label; under noise every flip shifts the label
*distribution*. Blur can buy accountability. Reported, not developed.

**A labelling trap caught before it became a false claim.** The first noise runs
compared against the *noiseless* D_0(K), which made flatness unreachable by
construction, and a later version made K=2 look "flat" — which would have read as
a counterexample to Theorem 5. A record that factors through the channel is a
*restricted* encoder class. The harness now reports both `D0_unrestricted` (the
paper's notion) and `D0_channel`, and `flat` always means the former.

**Also fixed this round**, from the same review: a mapping table from formal
objects to agent-system readings (§2); an exactness remark next to Theorem 9
separating "the threshold *is* the invariant" from "here is what we know of its
value"; the two unmeasured claims about natural-language summaries scoped to what
the theory actually supports; a moral-hazard-in-teams paragraph opening §7
(Holmstrom 1982, verified) — the canonical reference for this problem, which the
related work had simply omitted; and a contributions entry plus a reproducibility
paragraph so the verification story is not buried in the appendix.

Table 4 is parsed out of the LaTeX and checked against `experiment_agents.json`
by `audit_paper_numbers.py`, like every other number in the paper.

## E38 — The episode-level experiment (2026-09-15)

E37's experiment compresses the effort profile itself, which concedes the
abstraction most open to attack. This one puts an episode in between: a
coordinator fans out n subtasks, agent i has a controlled effort bit and returns
an artifact whose quality is drawn from one of two distributions, the coordinator
ships iff at least half the subtasks complete. Records compress the **trace**, so
the encoder q(label | S) is measured, not defined. Predictions were added to
`PREREGISTRATION_2026-09-15.md` as a declared post-hoc addendum and hashed before
the harness existed.

| n=5, exact | K | D | gamma |
|---|---|---|---|
| full trace | 243 | 1.2500 | 0.5000 |
| one bit per agent | 32 | 1.2500 | 0.5000 |
| top-half agents only | 80 | 1.2923 | 0.2624 |
| multiset of artifacts | 21 | 1.9718 | 0.1425 |
| count of completions | 6 | 2.0194 | 0.1190 |
| final output only | 2 | 2.1118 | 0.0243 |

**E1, E2, E3, E6 confirmed; E4 and E5 falsified.**

* **Identity, not volume (E3).** The margin ordering follows how much per-agent
  identity survives, not how many bits do. The multiset of artifacts keeps every
  artifact in full and discards only authorship; at n=3 it has MORE labels than
  one-bit-per-agent (10 vs 8) and less than half the margin.
* **Unforeseen.** One bit per agent matches the full trace on **both** axes
  exactly (D=1.2500, gamma=0.5000, K=32 vs 243). Under this episode model the
  per-agent bit is a sufficient statistic for both jobs, so 7.6x compression is
  free in the strong sense.
* **E5 falsified, and it sharpens the design rule.** We predicted that keeping
  bits only for the top half of agents would give margin 0, as fixed truncation
  does. It gives 0.2624 of the available 0.5000 — because *which* agents are kept
  is itself determined by what they did, so shirking changes an agent's own
  probability of appearing. Behaviour-dependent selection is far better than a
  schedule fixed in advance.
* **E4 falsified.** The coordinator's ship/no-ship bit is not worthless: margin
  0.0900 at n=3, 0.0243 at n=5, decaying fast.
* **E6.** 200,000 sampled episodes reproduce every exact number to within 0.023,
  which is what licenses reporting enumeration as "running many episodes".

Body length went to 9 pages, over the limit, so the worked Q_3 example and
Figure 2 moved to the appendix; back to 8. Table 5 is parsed out of the LaTeX and
checked against `experiment_episodes.json` by `audit_paper_numbers.py`.

## E39 — Hypothesis audit and citation/novelty audit (2026-09-15)

### A. Every theorem's assumptions checked against its statement

Five defects found, all in the statements rather than the mathematics.

1. **Lemma 10 (shell bound) was stated without its hypothesis.** "Every profile
   at distance r from C needs at least two centres at distance r" is false for an
   arbitrary C — it holds only for a *flat* record, which is where the proof gets
   it (Lemma 7's contrapositive). Statement now carries the hypothesis.
2. **Theorem 9 invoked an undefined term.** "In the dominating regime" was never
   defined in the statement. Now: "Restricted to K >= gamma(Q_n) — the dominating
   regime, in which some optimal K-median code is dominating".
3. **The restriction was attributed to the wrong half.** §5 said Lemma 8
   (sufficiency) "needs K >= gamma(Q_n)". It does not: a 2-dominating set is
   dominating, so the bound is implied, not assumed — and §5.7's own proof of
   Theorem 11 already said so, making the paper inconsistent with itself. The
   restriction belongs to *necessity*: below gamma(Q_n) optimal codes are not
   dominating and Lemma 7 yields something weaker than 2-domination. Fixed in
   both places, and the redundant hypothesis dropped from Lemma 8.
4. **Corollary 12 admitted priors its own premise excludes.** It said
   "q != 1/2", which allows q in {0,1} — a point mass, not full support, so
   Theorem 11 does not apply and the proof's "strictly increasing in |s|" fails.
   Now "q in (0,1), q != 1/2".
5. **Corollary 12 assumed n odd, and does not need to.** The proof never uses
   parity. MILP at n=4 and n=6 gives first flat K = 13 and 59, exactly
   2^n-(n-1), so the hypothesis was spurious. Dropped; `verify_all.py` block G
   now runs over n = 3,4,5,6,7,8,9,11,13 and cross-checks the even-n MILP
   evidence recorded in `prior_threshold_even.json`.

**An unverified hypothesis, now verified.** Lemma 7 assumes D_0 is strictly
decreasing at K. Nothing checked it. It holds over the whole range at n=3 and
n=4 by exhaustive K-median (`prior_threshold_even.py`), and at n=5 by MILP.

`verify_all.py` is now **145 checks** (was 125).

### B. Citation and novelty audit of [1], [3], [5], [6], [10]

| ref | verdict |
|---|---|
| [6] Fink–Jacobson | **Clean.** Cited three times, always as theirs; the bound at k=2, Delta=n gives 2^(n+1)/(n+2), matching what the paper prints. We claim only that our shell bound strengthens its specialisation to Q_n. |
| [5] Cohen et al., *Covering Codes* | **Clean.** The stated relation is right: a 2-fold 1-covering is 2-domination *plus* every codeword having a codeword neighbour, since a codeword covers itself at distance 0. Our n=9 code has zero internal edges, so it is 2-dominating and not a 2-fold 1-covering — checked in the artifact. |
| [3] Bujtás–Jaskó | **Under-attributed.** Their delta(G) >= 3 => gamma_2 <= |V|/2 gives exactly the 2^(n-1) parity-class bound the appendix called "trivial". Now attributed. |
| [10] Krotov–Potapov | **MIS-CITED.** Cited among "the theory of multiple coverings". The paper is *On multifold packings of radius-1 balls in Hamming graphs* — packings, the dual condition (at *most* mu, not at least). Now cited correctly as the dual, with a note that its bounds do not apply to our covering-type constraint. Second mis-citation of this kind found this session, after VICT. |
| [1] Arulanand et al. | **The live exposure, now stated precisely.** Paywalled and unobtained. If it contains gamma_2(Q_n) for n=3,5,7, Table 2 re-derives known values. That changes attribution of the numbers, not the contribution, because the claim is the reduction and the paper explicitly disclaims novelty for the invariant and its values. The intro contribution now says so too, rather than listing the values as if they were the result. |

Body length went back over the limit; §4's derivation now duplicates the
appendix proof, so it was compressed to a pointer. Body ends p8 again.

## E40 — Directory scaffolding (2026-09-15)

The repo had grown to 135 files in a flat root: scripts, JSON, logs and prose
all in one heap, with every script opening bare filenames so nothing worked
unless it was run from exactly one directory.

**New layout.** `src/` for the method and everything that checks it;
`experiments/` for the harnesses; `results/` for what they wrote, with
`results/logs/` beneath it; `docs/` for the research record and
`docs/archive/` for superseded session documents; `archive/` for the 21 one-off
scripts from sessions 1-2, kept for provenance with their outputs frozen in
`results/`; `dist/` for the built zip. `artifact_hashes.json` and
`environment.json` stay at the root because they describe the whole tree.

**`c39/paths.py`** resolves every file from the repo root via `__file__`, so
scripts no longer depend on the working directory and the tree can be
rearranged again without touching them. 59 literal paths across 28 scripts were
rewritten to go through it.

**`run.py`** is a single entry point: `verify`, `audit`, `score`, `figures`,
`package`, `all`. It stops at the first failure so a broken step cannot be
mistaken for a passing run.

Two things the move caught. The rewrite introduced a shadowing bug in
`analyse_experiment.py`, where the module-level JSON was itself called `data`
and hid the path helper; and the audit shelled out to `verify_all.py` by bare
name. Both were caught by running the tools rather than by reading them.

The manifest now keys entries by path relative to the root, so it describes the
layout and not just a pile of names, and the archive unzips into the same
structure. Verified end to end: a clean extract of the zip runs `run.py all` and
gives MANIFEST EXACT, ALL CHECKS PASSED, EVERY AUDITED NUMBER MATCHES, and all
[D] predictions holding.

## E41 — The LLM-agent experiment: one real result, one failed instrument (2026-09-15)

Three agents review a code change; S_i = 1 means reading the diff and citing
identifiers, S_i = 0 means confident generic review written without it and not
admitting it. A coordinator ships or holds. Five records, a judge that predicts
who actually worked, and the paper's instruments applied to the induced channel.
Model codestral-2508, temperature 0, seed 20260915. 32 usable episodes, exactly
4 per profile, 1 failure, 139k prompt + 30k completion tokens.

The task was rewritten from incident analysis to code review because the
available key is Codestral-issued; declared as addendum 3a **before** any episode
ran.

### The result that stands

| record | bytes | attribution error (bits of 3) |
|---|---|---|
| full_trace | 2585 | **0.406** |
| per_agent_summary | 639 | 0.312 |
| artifact_multiset | 2555 | 1.375 |
| global_summary | 598 | 0.875 |
| final_output | 513 | 1.281 |

`full_trace` and `artifact_multiset` contain **the same reviews**, differing by
about 30 bytes of `Reviewer N:` labels. Attribution error is **0.969 bits worse**
without them, 95% bootstrap CI [0.625, 1.281] over 20,000 resamples, excluding
zero. On text a real model wrote, removing authorship and nothing else costs
about a third of the attributable signal.

### The instrument that failed, and why

**L5's pre-registered failure condition fired: gamma(full_trace) = 0.** Per the
pre-registration the margin analysis is reported as INCONCLUSIVE rather than
ranked. L1, L2 and L3 are recorded as falsified, and L4 as not evaluable, but
none of those verdicts means anything while the estimator is broken.

The cause is now understood and it is not the model. gamma is a *minimum over
agents* of an LP on the estimated channel. For agent 2 with teammates 010 the
judge returned (0,1,1) in all four episodes **both with and without** that
agent's effort, so d_i = 0 exactly and gamma_i collapses to 0. Seven such
exact-tie cells exist across the five records at four episodes per profile.

The key property: coincidental ties can only push the estimate **down**, never
up. Small-sample gamma is therefore a one-sided artefact, not a measurement, and
a gamma of zero is uninformative about the true margin. `D_judge` averages
instead of minimising and is well behaved at this sample size, which is why the
attribution result survives and the margin result does not.

The scorer now prints the tie diagnostic and the bootstrap interval, so the
weakness is visible in the output rather than buried in a caveat.

### What this changes

* For the paper: report the attribution gap, not the margin, from this
  experiment. It is the quantity the reviewer asked for and the one the data
  supports.
* `experiment_llm.py --append` now tops each profile up to a target instead of
  restarting, so more episodes are cheap. Roughly 24 per profile should make
  exact ties rare enough for gamma to be estimable; that is 192 episodes, about
  50 minutes and well under a dollar.
* The run died at episode 33 when the machine slept and then memory pressure
  killed the process. Nothing was lost -- episodes are written as they complete.

## E42 — The LLM experiment completed: 192 episodes, and four wrong predictions (2026-09-15)

Continued to 24 episodes per profile, 192 usable, 1 failure, 837k prompt +
179k completion tokens. **Zero exact-tie cells**, so the margin estimator that
failed at four per profile is now clean.

### The estimator recovered exactly as diagnosed

| episodes/profile | tie cells | gamma(full_trace) |
|---|---|---|
| 4 | 7 | 0.000 — L5 failure fired |
| 10 | 1 | 0.088 |
| 17 | 1 | 0.108 |
| 24 | **0** | 0.075 |

The zero was a sampling artefact, not a judge blind spot. **L5 is now CONFIRMED**
and the experiment is not inconclusive.

### The result that holds, across a sixfold increase in data

| episodes | attribution gap | 95% CI |
|---|---|---|
| 32 | 0.969 | [0.625, 1.281] |
| 80 | 0.900 | [0.675, 1.125] |
| 136 | 0.941 | [0.772, 1.110] |
| **192** | **0.943** | **[0.802, 1.089]** |

`full_trace` and `artifact_multiset` contain the same reviews, ~30 bytes of
`Reviewer N:` labels apart, and attribution error is 0.391 against 1.333 bits of
3. Removing authorship and nothing else costs about a third of the attributable
signal. The interval tightened around a stable value rather than drifting.

### L1-L4 falsified, and the reason is my task design, not the records

The margin ordering came out scrambled: per_agent_summary 0.292 >
artifact_multiset 0.207 > global_summary 0.083 > full_trace 0.075 >
final_output 0. `full_trace` is second from bottom, which contradicts L1 and
reverses L2.

Decomposing gamma by agent explains it. In `full_trace` the worst single-cell
total variation is 0.958 for agent 0 and 0.792 for agent 1, but **0.125 for
agent 2**. gamma is a minimum over agents, so agent 2 alone sets it — for every
record.

Agent 2's sub-question is "what specific behaviour is now untested or
incorrectly invalidated?", and a shirking answer ("add tests for the changed
behaviour and verify invalidation") is nearly indistinguishable from a real one.
The other two sub-questions ask for a named defect and a named resource problem,
which a content-free answer cannot fake.

**So the gamma ordering across records measures the audit difficulty of my
question set, not the records.** It should not be reported as a property of
record types. `D_judge` averages over agents instead of minimising, which is
exactly why it reflects the record and is stable.

### What goes in the paper

* The attribution gap, with its interval. That is the identity-versus-volume
  claim on real model output.
* The methodological point, stated plainly: an all-agents margin is only as
  informative as the *least auditable* sub-task, so an empirical gamma needs
  sub-tasks of comparable auditability. Ours were not, and we say so.
* Not the gamma ordering across records.

A fixed version would equalise auditability across sub-questions -- each asking
for a specific named artefact from the diff. That is a redesign, not a re-run,
and it is not needed for the claim the experiment is being used to support.

## E43 — Skeptical audit of the failed predictions (2026-09-15)

Root-cause audit of every falsified prediction, run against artifacts rather
than prose. Three findings about our own record-keeping, one about the paper,
and one that changes what §7.2 claims.

### Record-keeping defects found

* **L6 was registered and never scored.** As written it compares gamma against
  "the prose design", which was never run, so it is **not evaluable by
  construction**. It should not be counted either way.
* **P4 was registered as one prediction and scored as two (P4a/P4b).** Splitting
  after seeing results lets half of it confirm. P4 as registered contained two
  conjuncts and one failed, so P4 is falsified; the a/b split is reporting
  detail, not two independent predictions.
* **The paper's count was wrong.** §1 said "two were wrong". Across all
  registered predictions the true figure is 8 derived all holding and **18
  falsified**. Corrected.

### No implementation bug

Every headline number was recomputed from `results/experiment_llm.json` by an
independent script that shares no code with `analyse_llm.py` -- a separate
channel estimator and a separately written Theorem-3 LP. All values matched to
three decimals (`results/independent_recheck.json`). Root cause H is excluded.

### The actual root cause of L1-L4

Not "task design affected the results" -- specifically this:

| record | gamma agent 0 | agent 1 | agent 2 | binds |
|---|---|---|---|---|
| full_trace | 0.958 | 0.792 | **0.075** | agent 2 |
| per_agent_summary | 0.875 | 0.744 | **0.292** | agent 2 |
| artifact_multiset | **0.207** | 0.335 | 0.271 | agent 0 |
| global_summary | **0.083** | 0.272 | 0.103 | agent 0 |
| final_output | 0.500 | **0.000** | 0.021 | agent 1 |

Agent 2 binds **only the identity-preserving records**. Where identity is
destroyed no agent is detectable and all three sit together. The earlier claim
in E42 that "agent 2 sets the margin for every record" was **wrong** and is
corrected here.

Dropping agent 2 restores the registered ordering exactly:
0.792 >= 0.744 > 0.207 >= 0.083 >= 0, which is L1 as written. Reported as a
diagnosis, not a rescue -- the prediction was made over three agents.

Agent 2's difficulty is independently visible without the gamma machinery:
per-agent classification accuracy on the full trace is 0.990, 0.943, **0.677**.

**A confound we cannot resolve:** agent i always receives sub-question i, so
sub-question difficulty and position in the record are perfectly confounded.
Nothing in this data separates them. Now stated in the limitations.

### The finding that changes §7.2

Decomposing the attribution error into "how many" and "which":

| record | raw | best relabelling | count only |
|---|---|---|---|
| full_trace | 0.391 | 0.391 | 0.391 |
| artifact_multiset | 1.333 | **0.438** | **0.438** |

The multiset recovers the **count** about as well as the full trace (0.438 vs
0.391) and essentially none of the **assignment**. The 0.943-bit gap is almost
entirely assignment error.

This matters because it answers the obvious objection -- "you shuffled them, of
course attribution fails". Each agent answers a *different* sub-question, so the
reviews are topically self-identifying and re-identification was possible in
principle. The judge did not do it. The claim is therefore not that shuffling
destroys information the content still carries; it is that a competent reader
holding the content does not recover authorship without labels. §7.2 now says
this, and the decomposition is in the audit so it cannot drift.

### Verdict

Experimental-design issue, not a bug and not a threat to any theorem. No
theorem depends on any of L1-L4: they are conjectures about where concrete
mechanisms would rank, and all 8 derived predictions -- the ones whose failure
would implicate a theorem or the code -- held in every experiment.

## E44 — Novelty audit, attacked from outside (2026-09-15)

Searched the literature against each claim rather than assuming novelty. One
claim had to be re-attributed, one had to be narrowed, three survive.

### Theorem 3 — PARTIALLY novel; re-attributed

The two ingredients are textbook: von Neumann minimax, and the variational
characterisation of total variation. Worse for us, the *qualitative* content --
that accountability requires a deviation to move the signal distribution -- is
exactly the individual and pairwise full-rank conditions of **Fudenberg, Levine
and Maskin, Econometrica 62(5):997-1039 (1994)**, verified.

Presenting Theorem 3 as wholly new would have been an overclaim. §3 now says so
explicitly and states what is actually ours: the quantitative one-shot form (the
shift must be >= gamma in TV, robustly over teammate mixtures) and the
elimination of the payment rule. Detectability in repeated games is stated for a
*given* monitoring structure; here the monitoring structure is the unknown, and
removing p is what lets us ask which structures a budget buys.

### Finite-K frontier — NOVEL, with a clean differentiator

No rate-distortion treatment found in which per-coordinate sensitivity is
constrained from *below*. Added to §7: differential privacy bounds a record's
sensitivity to an individual from above and asks what utility survives; we bound
it from below and ask what compression survives. Not duals, but it places the
object exactly.

### 2-domination connection — NOVEL

No results connecting domination numbers to incentives or accountability.
gamma_2 itself is well studied and we already disclaim it.

### Prior-dependence — NOVEL

No results on prior-weighted K-median sets required to be 2-dominating, or on a
prior-dependent flatness threshold.

### Identity-vs-volume — WEAKEST; narrowed and re-positioned

Two hits bound what we may claim:

* **Chen et al., ACL 2026, 19888-19905** -- full traces improve failure
  attribution by up to 76.5% over outputs-only. Our `final_output` row reproduces
  this. **The volume axis is not ours.**
* **Dietrich 2026 (arXiv:2606.09854)** -- a *trained* stylometric classifier
  recovers which model wrote an anonymised text at macro F1 ~0.99. So authorship
  signal survives anonymisation, and a dedicated re-identifier could plausibly
  recover much of what our zero-shot judge missed.

Our §7.2 previously said "a competent reader with the content in front of it does
not recover authorship without labels." Given Dietrich that was **too strong**.
Narrowed to: under the compaction a deployed system would apply, read by the kind
of general-purpose judge such a system would use, the assignment is not
recovered; whether a fitted stylometric model could is a different question our
design does not answer.

* **Lu et al. 2026 (arXiv:2605.27621)** -- introspective LLM judges fail to
  approximate removal-based attribution faithfully. A caution we inherit, since
  our instrument is such a judge. Cited.

**What remains ours on this axis:** holding content *fixed* and varying only
whether authorship survives. Chen et al. vary how much of the trace is kept; we
keep all of it and remove 30 bytes of labels. That isolates identity from volume,
which is the variable the theory implicates.

All four new entries verified against publisher records before citing. The
bibliography is 24 entries, every one cited, every citation resolving.

---

## E45 — Theorem 11 / Corollary 12 are FALSE. Withdrawn. (2026-09-15)

Found while running an adversarial novelty review of Contribution 3 — the attack
was "does this follow trivially from known weighted hypercube covering results?"
and the answer turned out to be worse than trivial.

**The test that caught it.** Instead of re-checking the 2-domination condition,
relax $\gamma$ and ask an LP directly: is $D_0(K)$ attainable with $\gamma>0$?

```
n=3 q=0.7 K=4: D=0.243000  D_0=0.243000  gamma=0.333333  FLAT   C dominating? False
   claimed threshold 2^n-(n-1) = 6  -> CONTRADICTED
n=4 q=0.7 K=5: D=0.440100  D_0=0.440100  gamma=0.250000  FLAT   C dominating? False
   claimed threshold 2^n-(n-1) = 13 -> CONTRADICTED
```

**Root cause, one step.** Lemma 3' gives: every non-centre has $\ge 2$ centres at
*its own nearest distance* $d(s,C)$. We converted that to "2-dominating", which
requires $d(s,C)=1$. Equal only when the optimal code is dominating. Uniform
prior above $\gamma(Q_n)$: dominating, so **Theorem 9 is unaffected**. Tilted
prior: the optimal code piles onto heavy profiles and leaves $000$ at distance 2.

**Corrected thresholds** (by enumeration, flatness *exhibited* not inferred):

| $n$ | uniform | tilted $q{=}0.7$ | withdrawn claim |
|---|---|---|---|
| 3 | 4 | **4** | 6 |
| 4 | 7 | **5** | 13 |

Tilting can *lower* the threshold. The withdrawn claim was backwards, not merely
imprecise.

**Why two independent verifiers both passed it.** `prior_threshold.py` (MILP) and
`verify_all.py` block G (solver-free enumeration) share no code and agreed on
6, 28, 122 at $n=3,5,7$. Both encoded the same wrong *specification*. This is the
sharpest lesson of the project: cross-implementation agreement tests
implementation, not specification, and we had been treating it as if it tested
both. The only thing that caught this was changing the *question*.

**Changes made.**
* `paper/sections/05b-priors.tex` rewritten: Theorem 11 and Corollary 12 gone,
  replaced by Proposition 11 (the correct prior-free necessary condition), the
  two counterexamples, and an explicit "we withdraw it". General-prior threshold
  declared **open**.
* Abstract, intro contribution 4, intro roadmap, §6, §7.1, §9 limitation 1,
  Appendix A: every "collapse to ratio 1" claim removed.
* Appendix A gains a paragraph on the verification failure itself.
* `experiments/prior_threshold.py` rewritten to exhibit flat records by direct
  enumeration; no proxy condition anywhere in it.
* `verify_all.py` block G rebuilt: constructs both counterexamples from nothing,
  certifies $\gamma$ with an explicit payment rule, and re-derives
  $K_\text{flat}=\gamma_2(Q_n)$ for uniform $n=3,4$. 145 checks -> **99**.
* Old scripts/artifacts quarantined under `experiments/withdrawn/` and
  `results/withdrawn/` with a README, kept as evidence for the above.
* Addendum 4 appended to the pre-registration.

Pipeline green: manifest, 99 checks, paper-vs-artifact audit, scorer, figures.
Paper builds, 14 pages, no undefined references.

**Effect on the paper.** Three core contributions become two and a half:
Theorem 3 (elimination), Theorem 5 (one-bit frontier), Theorem 9 (uniform
threshold = $\gamma_2(Q_n)$) all stand and are unaffected. Contribution 4 is now
an honest negative — what the uniform prior is actually doing — plus an open
problem.

---

## E46 — the general-prior threshold is CHARACTERISED (2026-09-15)

AAMAS Phase 1. E45 left the general-prior threshold open with only the corrected
necessary condition (Prop 12: every non-centre has >= 2 centres at its own
nearest distance). It is now closed, positively.

**The generalised construction.** Spread each non-centre uniformly over its
nearest centres *at whatever distance r*, pay agent i the reconstructed i-th bit.

**Edge structure (the lemma that does the work).** For a *fixed* centre c,
d(s,c) flips by exactly 1 across an edge; the distance to the *set* is a minimum,
so it moves by -1, 0 or +1. Two cases only:
* equal distances -> N(s_0), N(s_1) are DISJOINT, TV = 1
* descending      -> N(s_1) SUBSET N(s_0), TV = 1 - nu(s_1)/nu(s_0)

and every c in N(s_1) has c_i = s_{1,i} while every c in N(s_0)\N(s_1) has
c_i = s_{0,i}. So the natural payment lands exactly on the positive part of d_i:
<p_i, d_i> = (1/2)||d_i||_1 on *every* edge. A linear functional is minimised at
a simplex vertex, so Theorem 3's min-over-mixtures collapses to min-over-edges,
and that lower bound meets Corollary 4's upper bound. Hence the margin is
**exact**:

    gamma = 1 - max over descending edges of nu(s_1)/nu(s_0)

r = 1 gives nu(s_1) = 1 and recovers Lemma 8's 1 - 1/d_min.

**Sufficiency.** So the construction works iff nu strictly decreases on every
descending edge. Prop 12 gives only nu >= 2 -- but they coincide:

> If nu >= 2 everywhere then nu(s_1) < nu(s_0) on every descending edge.
> Proof: s_1 in C is trivial. Else r >= 2; suppose N(s_1) = N(s_0). Translate
> s_0 to 0^n, permute the flipped coordinate to first: s_1 = e_1, no centre of
> weight < r. N(0^n) = all weight-r centres; N(e_1) = weight-r centres carrying
> bit 1; equality forces every weight-r centre to carry it. Take c in N(0^n),
> set y = c XOR e_1, weight r-1 >= 1, so y not a centre. A centre at distance 1
> from y is y XOR e_m of weight r-1 +/- 1; r-2 is excluded, so weight r, so it
> carries bit 1, so m = 1 and the centre is c. Then nu(y) = 1. Contradiction.

**Theorem.** For every full-support prior pi,
`K_flat(pi) = min { K : some pi-optimal K-median code has nu(s) >= 2 for all
non-centres s }`, attained by the construction. Theorem 9 is the corollary: under
the uniform prior above gamma(Q_n) the optimal code is dominating, nu >= 2 *is*
2-domination, and K_flat = gamma_2(Q_n).

**Evidence, all of it negative-searching first.**
* `general_prior_margin.py`: 47,017 pi-optimal codes, n = 3,4, eight product
  priors. Closed form matched the Theorem 3 LP to 1e-9 on every one; D = D_0 on
  every one; 0 counterexamples. (First run caught a genuine error in my own
  parity claim -- I had applied fixed-centre parity to distance-to-set. The
  structure check failed loudly at n=3 K=2 rather than passing silently.)
* `general_prior_counterexample.py`: exhaustive over ALL codes at n = 3 and
  n = 4 for the bad configuration (Prop 12 holding, nu not strictly decreasing).
  **Zero.** So no LP stage-B realisability search was needed.
* `general_prior_n5_search.py`: at n = 5, vertex-transitivity plus coordinate
  permutation put the bad edge at (0^n, e_1) WLOG, reducing 2^32 codes to
  724,566. **Zero.**
* `general_prior_theorem_check.py`: 20,000 random codes at n = 3..7; 8,517
  satisfy Prop 12 and all 8,517 show strict descent; nesting and disjointness
  held on every edge of every code. 0 violations.

**Effect on the paper.** Section 5.6 goes from "open, with the corrected
necessary condition recorded" to a complete characterisation with a proof. The
withdrawn Theorem 11 / Corollary 12 stay withdrawn and stay reported as
withdrawn; the corrected tilted values (n=3: 4, n=4: 5, against the withdrawn
6 and 13) are now consequences of the theorem rather than isolated
counterexamples.

---

## E47 — AAMAS 2027 restructure (2026-09-15)

New folder `paper_aamas/`, built from `paper/`. The LNCS/ACM draft in `paper/`
is untouched and still audits clean.

**Format facts (Phase 0).** 8 pages excluding references, not 16. `aamas.cls` =
`acmart` + IFAAMAS copyright; anonymous submission is
`\documentclass[sigconf,anonymous]{aamas}`. Double-blind. Supplementary material
is a separate zip and **reviewers are not required to read it**, so the appendix
cannot carry load-bearing argument. OpenReview. AI policy requires documented
prompts/tools for substantive assistance.

**Structure, general-first.** Section 5 now runs: necessity (any prior) ->
construction at radius r -> exact margin -> strict descent -> Theorem 8 (any
full-support prior) -> Corollary 9 (uniform, = gamma_2(Q_n)) -> shell bound ->
values + the withdrawn claim. The graph invariant is now the corollary, not the
headline.

**Phase 3 reframing.** New Corollary 5 (effort-cost bound): margin below c_i
means no bounded payment sustains agent i's effort under any equilibrium
concept, with the existing hedge that costs are not modelled. Holmstrom and the
DP direction contrast both moved into the introduction; the "not dual" hedge is
preserved verbatim. Opening paragraph rewritten for a reader who has never
thought about context windows -- the compaction motivation now arrives third.

**Moved to appendix** (same filenames, so the audit is unaffected): the episode
model, the LLM experiment, design rules R1-R4, the noise results, the full
reproducibility narrative. Body keeps one four-row mechanisms table.

**Page count: body 7 pages**, references 7-8, appendix 8-14. Under the limit
with about a page of headroom, so no cuts beyond those already agreed.

**Audit.** `SEC` in `audit_paper_numbers.py` is now `C39_PAPER_DIR`-driven
(default `paper`). Added a block covering the AAMAS body's compact table against
`experiment_agents.json` -- it is a different file with different row labels, so
parsing Table 4 said nothing about it. Audit is 86 -> 93 claims. Both papers
pass; 99 verify checks unchanged.

**Two real defects found and fixed while restructuring.**
1. `07-related.tex` carried heredoc damage in BOTH copies: a literal TAB where
   `\texttt` belonged and a CR where `\ref` belonged, so the LLM-experiment
   cross-reference had been silently broken. Repaired in `paper/` too.
2. Theorem 8's display ran 27pt past the column -- the paper's main theorem,
   overflowing into the gutter. Reset as prose plus a short display.

**Anonymisation.** No author names, affiliations, emails, acknowledgements or
repository URLs in sources or rendered PDF; one "Anonymous" byline. Appendix A.5
gives `run.py` commands but names no host.

**Still open for submission:** the AI-use disclosure the CFP requires (documented
prompts and tools) is not written, and the appendix is currently appended after
the references rather than packaged as the supplementary zip the CFP describes.

## E48 - Noisy outcomes: accountability needs linear memory; general-prior threshold re-checked (2026-09-30)

**Why.** Review of `main_aamas27.pdf` for AAMAS 2027 GTEP: with outcomes equal
to the effort profile, the two-label record "all succeeded or not" makes
all-work a Nash equilibrium with margin 1, so a GTEP reviewer can dismiss the
tension as an artefact of the ex-post quantifier. First check (scratchpad,
n = 3, 5): with noisy outcomes the zero-margin nearest-centre record gains a
positive margin and at n = 3 under Nash beats the flat record, so Table 5's
"1/2 against 0" does not survive noise as stated.

**Result (a proof, not a fit).** Outcomes S_i ~ Bernoulli(h) if i works,
Bernoulli(l) if not. For every record with K labels,
sum_i (Nash margin_i)^2 <= (h-l)^2 H(Y) / (2h(1-h)) <= (h-l)^2 ln K / (2h(1-h)).
Pinsker per agent plus sum_i I(Y;S_i) <= I(Y;S) for independent S_i. Block
success counts attain the order (margin (h-l) max pmf Bin(m-1,h)), so Theta(n)
bits are necessary and sufficient for a constant margin; any o(n)-bit summary
drives the sustainable effort cost to 0. Vacuous at h in {0,1}, as it must be.

**Checks.** `experiments/noisy_outcomes.py` (seed 20260930): gates G1-G4 pass;
3000 random stochastic records, max margin/bound 0.764. `verify_all.py` block
H recomputes the printed values independently, no solver. Under noise the
flat record's ex-post margin equals its Nash margin (0.5063 at n=5, 0.6317 at
n=9); the nearest-centre record on the same code has Nash 0.6786 but ex-post
0.3911 at n=9. So flatness buys robustness to shirking teammates under noise,
not a larger Nash margin.

**General prior.** The AAMAS draft calls the threshold open; paper_gtep proves
it (strict-descent lemma). `experiments/general_prior_strict_descent.py`
checks the lemma, the margin formula (against the Theorem 1 LP) and the
theorem against brute force on all 46,592 optimal codes at n = 3, 4 under
uniform, product(0.6, 0.7, 0.85) and three random priors: no exceptions.
product(0.6) at n = 4 gives K_flat = 13 against uniform 7: tilt moves the
threshold either way.

**Not pre-registered.** Both results are derivations checked by enumeration,
written after the first check above; no prediction was hashed beforehand.

**Paper text.** Drop-in LaTeX in `revision_2026-09-30/` (the source of
main_aamas27.pdf is not in this repo). Audit block `07_audit_noisy_block.py`
passes 23/23 against the revision text and catches two planted errors.

## E49 - Budget balance needs attribution; cost of implementation; designer's memory (2026-09-30)

**Why.** Make the GTEP content the spine of the paper: after E48 the draft
had one game-theoretic theorem beyond the minimax lemma.

**Budget balance (a proof).** For budget-balanced rules (sum_i p_i(y) = B for
every label) with p_i in [0,1]^K, the all-work margin t satisfies
t <= (1/n) sum_i TV(Q_{0,i}, mean_j Q_{0,j}): expand sum_i <p_i, d_i> around
the mean deviation, the B-term vanishes. Every record symmetric in the agents
(count, all succeeded, any function of the multiset of outcomes) has margin 0
at any size, which is the Holmstrom / Legros-Matthews / Rahman-Obara
attribution requirement, priced for compressed records. t <= 2 * mean Nash
margin, so E48's memory bound carries over.

**Cost of implementation (a proof).** Least expected payment for agent i at
cost c is >= c h/(h-l) for every record (the likelihood ratio of any label is
at least l/h), with equality iff c <= (h-l) P(Y certifies S_i = 1 | S_i = 1).
The count certifies only at "all succeeded", so it leaves the floor once
c > (h-l) h^(n-1): 1.699x the full record at n=100 and 6.989x at n=1000 for
c = 0.02. The flat record certifies nothing and pays 6-7% more at n=5.

**Designer.** From E48's bound (which holds at every action profile, summed
over working agents) and the cost floor: memory per accountable agent is
between beta = 2h(1-h)(c/(h-l))^2 / ln 2 and 1 bit.

**Checks.** `experiments/budget_balance_cost.py` (seed 20260930): all gates
pass; 1200 random records, max BB/attribution = 1.000 (attained); the
certification iff on 885 record/agent/cost cases (726 at the floor, 103
above, 56 infeasible). `verify_all.py` block I (solver-free), 135 checks.
Audit block 09 passes and catches planted errors.

**Not done: complexity.** An NP-hardness result would need arbitrary
deviation graphs and an unconfirmed hardness result for 2-domination on
triangle-free graphs; left as future work rather than claimed.

**Not pre-registered**, as in E48.
