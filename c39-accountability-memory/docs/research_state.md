# Research state — C39

**Last updated:** 2026-09-13 (session 2)
**Scope of session 2:** close session 1's integrity gaps, make `K_flat` exact,
and re-normalise the significance argument. P1 and P4 untouched.

---

## 1. Headline: session 1's formula is FALSIFIED, and `K_flat` is now identified exactly

| n | session-1 prediction `ceil(2^(n+1)/(n+2))` | measured `K_flat(n)` | status |
|---|---|---|---|
| 3 | 4 | **4** | exact, agrees |
| 5 | 10 | **10** | exact, agrees |
| 7 | 29 | **32** | exact, **formula WRONG** |
| 9 | 94 | **97 <= K_flat(9) <= 128** | **formula WRONG** |

`K_flat(n) = ceil(2^(n+1)/(n+2))` was fitted to two exact points and one
consistent lower bound. It fails at the first genuinely new data point. Session
1 labelled `K_flat(7) = 29` a conjecture and only claimed `>= 29`; that bound
was correct (32 >= 29), but the conjecture was not.

**What replaces it is not another fitted curve but an exact identification:**

> **`K_flat(n) = gamma_2(Q_n)`, the 2-domination number of the n-cube** —
> the smallest set of vertices such that every vertex outside it has at least
> two neighbours inside it.

Both directions are proved (`kflat_theory.py`):

* **Necessity (Lemma 3').** If a non-centre has a *unique* nearest centre,
  walk one step toward that centre; uniqueness propagates, so both endpoints of
  that edge are point masses on the same label, the edge derivative `d_i` is
  zero, and `<p_i, d_i> = 0` for **every** `p_i in [0,1]^K`. So flatness forces
  every non-centre to have >= 2 nearest centres. This constrains arbitrary
  bounded payment decoders, not just binary ones.
* **Sufficiency.** Given any 2-dominating `C` with `|C| >= gamma(Q_n)`, put a
  point mass on each centre, spread each non-centre uniformly over its centre
  neighbours, and pay agent `i` the reconstructed `i`-th bit
  (`p_i[y] = centre_y[i]`). Then `D = D0(K)` exactly and the all-profile margin
  is exactly `1 - 1/d_min >= 1/2`. Verified with no solver at n=3,5,7,9,11.

This turns `K_flat` from the output of an encoder/payment search into a
classical graph invariant over `2^n` binaries. Solve times dropped from hours
to milliseconds, which is what made n=7 and n=9 reachable.

## 2. Certificates

**`K_flat(7) = 32`, complete chain:**
* K = 2..28 — excluded by the shell bound (below). No search.
* K = 29, 30, 31 — 2-domination **proved infeasible** by MILP (status 2).
* K = 32 — explicit 2-dominating code; verified solver-free:
  `D = D0 = 0.75`, margin `0.5`, min_deg 2. Also produced independently by the
  algebraic construction below, so two routes agree.

**`97 <= K_flat(9) <= 128`:**
* K = 2..93 — excluded by the shell bound.
* K = 94, 95, 96 — 2-domination **proved infeasible** by MILP.
* K = 128 — explicit algebraic code, verified solver-free: `D = D0 = 0.75`,
  margin `0.667`, min_deg 3.
* K = 97..127 unresolved. Three routes were tried and all failed, so this is
  recorded as open rather than guessed:
  (a) feasibility MILPs at K = 98,100,104,108,112,116,120,124 (512 binaries)
      did not terminate within 40 min each;
  (b) shrink-only local search cannot move at all — the algebraic code has
      **zero internal edges**, so deleting any centre leaves that centre with
      no centre-neighbour;
  (c) destroy-and-repair search, 70,685 trials over 10 min, never beat 128.

**New: the shell counting bound** (strictly stronger than session 1's, and the
thing that closed the small-K regime). Every state at distance `r` needs >= 2
centres *at distance r*, and there are at most `K*C(n,r)` such (state, centre)
pairs, so shell `r` holds at most `floor(K*C(n,r)/2)` states. Filling shells
from the inside gives a lower bound on `N*D0`; if it exceeds an upper bound on
`N*D0(K)`, flatness at `(n,K)` is impossible. It reduces to session 1's bound
when everything fits in shell 1, and is tight (not merely valid) at all three
known flat points — it excludes none of them.

**Bounds on the invariant.**
* Lower: `gamma_2(Q_n) >= 2^(n+1)/(n+2)` (incidence counting). Tight at n=3, 5.
  **Not** tight at n=7 (29 vs 32) or n=9 (94 vs >=97).
* Upper: `gamma_2(Q_n) <= 2^(n - floor(log2(n/2+1)))` from a parity-check
  construction — take `H` with no zero column and every nonzero syndrome used
  at least twice; the centres at distance 1 from `x` are the columns equal to
  `x`'s syndrome. Tight at n=3 and n=7; loose at n=5 (gives 16 vs 10).

## 3. Step 1 — the solver is trusted (this gated everything else)

Session 1's `D0(K)` fast path was never checked against anything but itself.
`bruteforce_d0.py` recomputes it with **no LP and no MILP**:

* Method E — complete enumeration of literally every subset of the `2^n`
  vertices (256 at n=3, 65536 at n=4), no pruning.
* Method B — exact per-cardinality branch and bound, with an admissible bound
  from submodularity of the marginal reduction, and a sphere-packing bound.
  Incumbents seeded by our **own greedy**, never by the p-median solver, so a
  wrong p-median value cannot prune away the true optimum and confirm itself.

Method B was first validated against Method E at n=3 and n=4: **identical at
every cardinality**. Then:

> **Every K from 2 to 2^n, at both n=3 and n=5: brute force and the fast
> solver agree with difference exactly `0.00e+00`. All MIP gaps `0.0`.**

No disagreement anywhere. The scaling work is not void.

**Validation check C** (session 1's never-run item): recovered and run
(`check_c_symbreak.py`). It checks that the label-ordering symmetry-breaking
constraint in `exp_kflat.UBModel` does not change the optimum — valid only
because labels are exchangeable. Scope note recorded in the file: every
session-2 result comes from `kflat_theory.py`, which uses **no symmetry
breaking anywhere**, so check C bears only on superseded rows.

## 4. Significance, re-normalised — the compression ratio

Session 1 framed this as "escaping the tension needs `Theta(2^n/n)` labels."
That is the wrong normalisation and it made the result sound stronger than it
is. The quantity that maps onto engineering reality is the **compression ratio**

    C(n)  =  2^n / K_flat(n)

— how much smaller the record is than the full effort profile. Since
`K_flat(n) = gamma_2(Q_n)` and

    2^(n+1)/(n+2)  <=  gamma_2(Q_n)  <=  2^(n - floor(log2(n/2+1))),

dividing `2^n` through gives

    2^floor(log2(n/2+1))   <=   C(n)   <=   (n+2)/2.

Both ends are `Theta(n)`. **`C(n)` is linear and unbounded**, so the
safe-compression zone does widen as the team grows. Measured:

| n | 3 | 5 | 7 | 9 | 20 | 50 |
|---|---|---|---|---|---|---|
| `C(n)` | 2.00 | 3.20 | 4.00 | 4.00–5.28 | 8–11 | 16–26 |
| `(n+2)/2` | 2.50 | 3.50 | 4.50 | 5.50 | 11 | 26 |

Note `(n+2)/2` is an **upper** bound on `C(n)`, not its value — the measured
ratio sits at or below it everywhere, and the gap is real at n=7 (4.00 vs 4.50).

### The two normalisations disagree, and both are correct

Measured in **state-space ratio**, the safe zone widens: at n=5 you may compress
3.2x for free, at n=50 you may compress 26x.

Measured in **bits**, which is the unit a checkpoint is actually sized in, the
free allowance is `log2(C(n)) ~ log2(n/2)` bits out of `n`, so the *fraction* of
per-agent resolution you may discard for free **shrinks**:

| n | 5 | 7 | 20 | 50 |
|---|---|---|---|---|
| free bits | 1.68 | 2.00 | 3.00–3.46 | 4.00–4.70 |
| as % of n | 33.6% | 28.6% | 15.0–17.3% | 8.0–9.4% |

Linear growth in a ratio against an exponentially large baseline is
logarithmic growth in bits. Both statements describe the same numbers.

### The answer, with numbers

* **n = 20**: flat requires `K >= 95,326 .. 131,072` labels, i.e. retaining
  **16.5–17.0 of the 20 bits** (83–85% of per-agent resolution). The tension
  appears once the record discards more than ~3.5 bits, i.e. compresses the
  effort profile by more than ~11x.
* **n = 50**: flat requires `K >= 4.33e13 .. 7.04e13` labels, i.e. retaining
  **45.3–46.0 of the 50 bits** (91–92%). Tension once you discard more than
  ~4.7 bits, i.e. compress by more than ~26x.

So the honest reading is neither session 1's nor the one the compression-ratio
framing first suggests:

* The ratio `(n+2)/2` is a **small** absolute compression factor. 11x at n=20
  and 26x at n=50 are modest by the standards of real trace compaction, which
  routinely discards far more. On that reading real records sit inside the
  tension regime.
* But the flat side requires retaining **~90% of per-agent resolution**, which
  is very close to just storing the raw profile. A record that keeps one bit
  per agent is flat and has no tension at all.

**Restated P4 conclusion.** The tension regime is exactly *"records that discard
more than `log2(n/2)` bits of an n-bit effort profile"* — more than ~15% of
per-agent resolution at n=20, ~9% at n=50. Whether a real agent-team audit
record does that is a question about what checkpoints retain **about who did
what**, and it is not answered by P0 in either direction. A per-agent effort
bit (50 bits at n=50) is flat; an aggregate such as "how many agents succeeded"
(`log2(51) = 5.7` bits, 11% of resolution) is deep in the tension regime. The
engineering case therefore turns entirely on whether real records keep
per-agent resolution or aggregate it — which is precisely P4's job, still
unstarted, and still C39's main exposure.

This corrects, and does not rescue, session 1's claim. Session 1 said the
`Theta(2^n/n)` result made the significance claim survive "on scaling grounds."
That was overstated: the same numbers in bits say the free allowance is only
logarithmic, and the decisive question was always empirical.

## 5. What is claimable now

* `K_flat(n) = gamma_2(Q_n)`, both directions proved, with an explicit optimal
  construction and margin `1 - 1/d_min`.
* `K_flat(3) = 4`, `K_flat(5) = 10`, `K_flat(7) = 32` exact;
  `97 <= K_flat(9) <= 128`.
* The shell counting bound, tight at every known flat point.
* `D0(K)` equals the Hamming-cube K-median optimum; verified against complete
  enumeration at n=3, n=4 and against exact branch and bound at n=5.
* `C(n) = Theta(n)`, bracketed by `2^floor(log2(n/2+1))` and `(n+2)/2`.

**Not claimable:**
* `K_flat(n) = ceil(2^(n+1)/(n+2))` — **falsified**.
* Any closed form for `gamma_2(Q_n)`. It is a known-hard graph invariant; we
  have matching bounds only at n = 3, 5, 7.
* `K_flat(9)` exactly.
* That real agent records fall on either side of the threshold.

## 6. Loose ends

* `K_flat(9)` in [97, 128]. Needs either a better construction or an
  infeasibility proof above 96; the plain MILP will not get there.
* n=9, K=9..13 were not excluded by the weaker local condition, but **are**
  excluded by the shell bound, so the n=9 lower bound is clean.
* ~~The n=9 tail of `verify_t1_independent.py` (gamma = 1/12, 1/9) still
  unrun.~~ **Done 2026-09-15** — ran to completion in the pinned environment,
  all methods agree with the closed form to 8.5e-14. See E32.

## 7. Decision from session 1 — RESOLVED 2026-09-14: discriminator RETIRED

`K_flat(5) = 10` fires the predeclared kill test on its literal wording. The
decision recorded here is that the discriminator is **retired as mis-specified,
not satisfied**, and C39 continues.

**Reasoning.** The test treats `K_flat(5) = 10 = 2n` as the "trivial/expected"
outcome, so its content is the hypothesis that `K_flat` grows like `2n`. That
hypothesis is now refuted at both other exact points: `K_flat(3) = 4`, not 6,
and `K_flat(7) = 32`, not 14. A discriminator that is wrong at n=3, wrong by
more than a factor of two at n=7, and right at n=5 only because `2n` and
`ceil(2^(n+1)/(n+2))` happen to collide at 10, is testing a pattern that does
not exist. Firing it on the one coincidental point would kill the candidate on
an artefact.

**Guardrails attached to this decision**, because session 1's replacement
formula was itself falsified and that is a reason to trust fitted stories less,
not more:

* No fitted curve replaces it. The object carried forward is the exact
  identification `K_flat = gamma_2(Q_n)`, which is a proof, not a fit.
* The significance claim carried forward is the bit-level reading in §4, not the
  ratio reading alone.
* This retirement is recorded here, dated, so the decision stands on its own
  reasoning rather than being implied by the existence of a write-up.

## 8. Next action — superseded 2026-09-14

Session 2 ended "do not start the paper". That gate is now released: the
decision in §7 is made, P1 is done (`literature_review.md`, plus the multiple-
covering direction in `P4_ADDENDUM_2026-09-14.md` §6), and P4 resolved to STAKES
PRESENT (`P4_ADDENDUM_2026-09-14.md`).

**Current action: write the paper.** Target AAMAS 2027 main track, COINE.
Author registration 17 Sep 2026, abstract 1 Oct, paper 8 Oct. Section plan,
theorem ordering, figure list and the objection/rebuttal table are in
`C39_PAPER_PLAN_AAMAS2027.md`. Draft lives in `paper/`.

Still open as research, and explicitly out of scope for this submission:
`K_flat(9)` in [97, 128]; non-uniform priors; the n=9 tail of
`verify_t1_independent.py`.

## 9. Session 3 status — 2026-09-15

**Paper.** Draft complete and building (8 pages: body to p6, references, appendix
to p8). Every section is drafted; the appendix is written in full. See
`paper/README.md` for the per-file state and the three items that need a human
(author block, the official AAMAS class file, seven bibliography entries whose
identifiers we hold but whose author lists must come from publisher records).

**The open technical item is closed.** Appendix A step 5 — minimising over
reconstruction pairs for general odd n — is proved, not merely verified. The
argument is a Rademacher coupling: `E[Delta^-] = (1/2)E|R_{p+m}|` and `E|R_k|` is
nondecreasing, so every decoder pair is dominated by the antipodal one. It needs
no permutation averaging and no orbit enumeration. Recorded as E30 in
`experiment_log.md` and machine-checked as `verify_all.py` block E (21 checks,
all deviations exactly zero). `verify_all.py` is now 56 solver-free checks.

**Reproducibility is sealed.** Every session-2 number has been re-run under the
pin, including the n=9 MILP infeasibility at K=92..96 that carries
`K_flat(9) >= 97` (`gamma2_n9_lb_rerun.py`, E29). The artifact package —
`ARTIFACT.md`, `check_manifest.py`, `make_artifact.py`, `verify_all.py` — builds
a zip that passes MANIFEST EXACT and ALL CHECKS PASSED from a clean extract.

**Still open, unchanged and still out of scope for this submission:**
`K_flat(9)` in [97, 128]; non-uniform priors; graded effort.

*Correction (2026-09-15):* the n=20 lower bound above read 95,325; the exact
value is `ceil(2^21/22) = 95,326`. The bit figures (16.54–17.0 of 20) are
unchanged.

## 10. New result — the uniform prior is load-bearing (2026-09-15)

`K_flat(pi) = min { K : some pi-optimal K-median set of size K is 2-dominating }`
for every full-support prior (the margin condition never mentions the prior;
only D and D_0 do). Uniform is the case where every dominating K-set is optimal,
which recovers `K_flat = gamma_2(Q_n)`.

For any product Bernoulli(q) prior with `q != 1/2`:

    K_flat = 2^n - (n-1),   margin exactly 1/2

so the free compression ratio collapses from `Theta(n)` to `1 + O(n 2^-n)`.
Measured: 4 -> 6 at n=3, 10 -> 28 at n=5, 32 -> 122 at n=7, and at n=20 the free
allowance drops from 3.0-3.5 bits to 2.6e-5 bits. Two independent routes agree
(MILP sweep and a solver-free combinatorial argument); see E34 and
`verify_all.py` block G.

This is claimable and is now §5.7 of the paper. It makes §6's numbers
**conservative** — the uniform prior is the most favourable case for
accountability, not a neutral choice.

Still not claimable: the one-bit frontier (Theorem 2) under a non-uniform prior.
The orientation-alignment step genuinely needs flip-invariance, and that is now
the only place uniformity is load-bearing.
