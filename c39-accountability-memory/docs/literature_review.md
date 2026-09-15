# C39 — Literature review (P1)

**Date:** 2026-09-14
**Scope:** literature search only. No code run, no solver run, no computational
result in `research_state.md` modified.
**Method caveat (master context rule 7):** failed keyword searches are not
evidence of absence. Coverage and access limitations are recorded per direction.

---

## OVERALL VERDICT

### NOVEL WITH CLOSE PRIOR ART TO CITE — with one material downgrade and one unresolved risk

The **reduction** at the heart of C39 — that the flatness threshold of the
reconstruction/incentive frontier equals a classical graph invariant, via the
payment-decoder elimination theorem — was **not found** in any of the five
literatures searched. That remains the plausible contribution.

But two things must change in `research_state.md`'s framing:

1. **The counting bound is not new.** Session 1's
   `gamma_2(Q_n) >= 2^(n+1)/(n+2)`, derived from scratch and presented as a new
   corollary, is **exactly the Fink–Jacobson (1985) bound** `gamma_k(G) >= kn/(Delta+k)`
   specialised to `k=2`, `Delta=n`, `|V|=2^n`. This is a foundational, standard
   result in the k-domination literature. It must be cited as Fink–Jacobson and
   must stop being described as ours.
2. **gamma_2(Q_n) is an actively studied invariant**, and there is at least one
   published paper specifically on the 2-domination number of hypercubes. Once
   `K_flat = gamma_2(Q_n)` is established, computing `K_flat(3,5,7,9)` is
   "evaluating a known invariant", not a new combinatorial result. The novelty
   lives entirely in the reduction, not in the numbers.

**Unresolved risk (blocking):** Arulanand, Sundara Rajan & Prabhu (2023) is
paywalled and I could not read it. It may already contain `gamma_2` values for
the hypercube classes session 2 computed. **This must be obtained before any
write-up.** See direction 4.

**The OEIS check requested in step 4 could not be completed** — oeis.org
returned HTTP 403 to every URL form attempted. It is also mis-specified as
given; see direction 4(e). No headline OEIS finding, positive or negative.

---

## Direction 1 — One-bit distributed estimation / CEO problem

**Verdict: NO MEANINGFUL OVERLAP on the constrained problem. Prior art on the
unconstrained baseline only.**

The binary CEO problem (Berger et al.) has **n separate encoders**, each seeing
an independently noise-corrupted copy of the source, each sending a rate-limited
message to a fusion centre that reconstructs under Hamming distortion. Majority
decoding appears there, and so does Hamming-distortion analysis.

C39's model is structurally different in the way that matters:

| | binary CEO | C39 |
|---|---|---|
| encoders | n, distributed, each sees noisy copy | **1**, sees all of `S` exactly |
| what is estimated | a hidden source behind the noise | the profile `S` itself |
| side constraint | none | **every coordinate's discrete derivative >= gamma** |
| asymptotics | rate region, n -> infinity | one-shot, finite `K` |

No CEO-problem result imposes a lower bound on the summary's sensitivity to
each individual input bit. The incentive constraint has no analogue there.

**However** — the *unconstrained* baseline `D0(K)` (minimum expected Hamming
distortion of a K-label summary of n uniform bits) is classical quantisation
theory, and session 2 already identifies it as the Hamming-cube K-median
problem. **Nothing about `D0` should be claimed as novel.** `research_state.md`
does not currently claim it is, which is correct.

Citations:
- [A Lower Bound Analysis of Hamming Distortion for a Binary CEO Problem](https://ieeexplore.ieee.org/document/7322201/)
- [Analysis and Code Design for the Binary CEO Problem under Logarithmic Loss (arXiv:1801.00435)](https://arxiv.org/html/1801.00435v1)
- [Mean Estimation from One-Bit Measurements (arXiv:1901.03403)](https://arxiv.org/pdf/1901.03403)

---

## Direction 2 — Boolean function analysis / extremal problems on the hypercube

**Verdict: NO MEANINGFUL OVERLAP. The literature runs in the opposite direction.**

This was the direction the C39 update flagged as the most dangerous ("one-bit
summaries of uniform bits under Hamming loss with majority optimal is close to
folklore"). It does not collide, for a specific reason:

Boolean-function analysis studies **upper** bounds on influence — Friedgut
(low total influence implies junta), KKL, Talagrand, and the low-influence /
slice literature. The object is "functions whose influence is small."

T1's constraint is the **exact opposite**: every individual discrete derivative
is bounded **below** by gamma, uniformly over all `2^n` edges. That is a
minimum-influence-per-coordinate constraint, with a *linear* objective
(expected Hamming distortion) minimised over the resulting polytope.

I searched specifically for the LP that T1 reduces to — a linear objective over
`{q : q(s + e_i) - q(s) >= gamma for all i, s}`, i.e. over an affine shift of
the monotone cone on `{0,1}^n` — under the names monotone cone LP, Lipschitz
Boolean function, minimum-influence extremal problem, and discrete-derivative
constraint. **I found no named object matching it.** The monotone cone itself is
well studied (monotone Boolean functions, LP-type problems), but not this
extremal problem over it.

This is a genuine non-collision in structure, not a technicality I am hiding
behind. But it is also the weakest kind of evidence — absence of a keyword
match. A referee from this community could still know the object under a name I
did not guess.

Citations (nearest neighbours, all upper-bound-on-influence):
- [Low Influence Functions over Slices of the Boolean Hypercube](https://ieeexplore.ieee.org/document/6875481/)
- [Concentration on the Boolean hypercube via pathwise stochastic analysis (arXiv:1909.12067)](https://arxiv.org/html/1909.12067)
- [Monotone Boolean Functions, LP-type problems and MaxCon (arXiv:2005.05490)](https://arxiv.org/pdf/2005.05490)

---

## Direction 3 — Rate-distortion with a side constraint

**Verdict: NO MEANINGFUL OVERLAP. One structural analogue worth citing.**

The closest *shape* match is **rate-distortion-perception (RDP) theory** /
output-constrained lossy source coding: classical rate-distortion plus an extra
side constraint that moves the optimum, which is exactly C39's shape. But the
side constraint is **distribution-matching** (the reconstruction must have a
prescribed output distribution / small Wasserstein distance to the source), not
a per-coordinate sensitivity lower bound. Different constraint, different
mathematics, no path from one to the other.

Searches for "Lipschitz constraint", "minimum sensitivity", and
"distinguishability guarantee" in a rate-distortion context returned only
classical entropy-constrained quantisation and MMSE-Lipschitz results, which are
unrelated.

Cite RDP as the structural precedent for "rate-distortion with an extra
constraint", nothing stronger:
- [Output-Constrained Lossy Source Coding with Application to RDP Theory (arXiv:2403.14849)](https://arxiv.org/pdf/2403.14849)
- [Gaussian Rate-Distortion-Perception Coding and Entropy-Constrained Scalar Quantization (arXiv:2409.02388)](https://arxiv.org/pdf/2409.02388)

---

## Direction 4 — gamma_2(Q_n): the 2-domination number [HEADLINE]

This is where the real findings are. Four sub-results.

### (a) Session 2 named the right object — CONFIRMED

Bujtás & Jaskó state the definition verbatim as session 2 uses it:

> "In a graph G, a set D subset of V(G) is called 2-dominating set if each
> vertex not in D has at least two neighbors in D. The 2-domination number
> gamma_2(G) is the minimum cardinality of such a set D."

The same paper explicitly distinguishes this from the other natural
generalisation — **k-tuple domination**, where `|N[v] ∩ D| >= k` is required for
*all* `v`, including those inside `D`. Web sources routinely conflate the two
("double domination"), so this mattered. Session 2's object is `gamma_2`, the
standard k-domination number with k=2, and the naming in `research_state.md` is
correct.

Also checked and **not** the right object: **k-limited domination** (Cartesian
products paper, arXiv:2606.22428), which requires every vertex *in* the set to
have at most k neighbours *outside* it — an inverse constraint, unrelated.

- [Bounds on the 2-domination number, Bujtás & Jaskó (arXiv:1612.08301)](https://arxiv.org/pdf/1612.08301)

### (b) The counting bound is Fink–Jacobson (1985) — NOT NOVEL

**This is the clearest prior-art hit of the session and I am not softening it.**

Fink and Jacobson, who introduced k-domination in 1985, proved

    gamma_k(G) >= k*n / (Delta + k)      (n = |V|, Delta = max degree)

Specialise to `Q_n`: `k = 2`, `Delta = n`, `|V| = 2^n`, giving

    gamma_2(Q_n) >= 2 * 2^n / (n + 2) = 2^(n+1) / (n+2).

That is **character-for-character session 1's counting bound**, the one
`research_state.md` §2 lists under "Bounds on the invariant" and session 1
derived by incidence counting. It is a 1985 result and a standard lemma in the
k-domination literature.

**Required correction:** `research_state.md` §2 and `experiment_log.md` E18/E24
must attribute `2^(n+1)/(n+2)` to Fink & Jacobson (1985) and stop presenting it
as a contribution. The *derivation via Lemma 3'* (that flatness forces the
2-domination condition) is still ours; the bound on `gamma_2` that follows is
not.

The **shell counting bound** (session 2's strengthening, using distance shells
and `floor(K*C(n,r)/2)`) is a statement about `N*D0` in the K-median problem,
not a bound on `gamma_2`, so Fink–Jacobson does not subsume it. I found no match
for it. Plausibly still ours — but it is only used to exclude small K, and its
role should be described narrowly.

- Fink, J.F. and Jacobson, M.S., "n-domination in graphs", *Graph Theory with
  Applications to Algorithms and Computer Science*, Wiley, New York, 1985,
  pp. 283–300.
- [k-Domination and k-Independence in Graphs: A Survey (Chellali et al.)](https://www.academia.edu/29214098/k_Domination_and_k_Independence_in_Graphs_A_Survey)

### (c) A directly on-topic paper exists and I could not read it — BLOCKING RISK

> S. Arulanand, R. Sundara Rajan, S. Prabhu, **"2-domination number for special
> classes of hypercubes, enhanced hypercubes and Knödel graphs"**, *International
> Journal of Networking and Virtual Organisations* **29**(2), 168–182, 2023.

From the abstract: they determine `gamma_2` for specific hypercube classes,
establish that "the lower bound obtained in Fink and Jacobson (1985) [is] quite
precise", and give linear-time algorithms.

**Paywalled (Inderscience); no preprint found.** I could not verify which
dimensions they cover or what values they report.

This matters concretely. Session 2 found Fink–Jacobson is tight at n=3 (4) and
n=5 (10) but **not** at n=7 (bound 29, true value 32) or n=9 (bound 94, true
value >= 97). A published claim that the FJ bound is "quite precise" for
hypercube classes is either consistent with that (if "precise" means within a
small factor) or in tension with it (if they claim tightness at n=7). Either
way:

**Action required before any write-up: obtain this paper and check its values
against `K_flat(3)=4`, `K_flat(5)=10`, `K_flat(7)=32`.** If it already reports
these, session 2's computational section is a re-derivation of published values
and must be reframed as confirmation, not discovery.

- [Abstract / record (RePEc)](https://ideas.repec.org/a/ids/ijnvor/v29y2023i2p168-182.html)
- [Publisher page (Inderscience)](https://www.inderscienceonline.com/doi/abs/10.1504/IJNVO.2022.128463?af=R)

### (d) Known general upper bounds to compare session 2's construction against

From Bujtás & Jaskó's survey of the state of the art:

* `delta(G) >= 3` implies `gamma_2(G) <= |V|/2`, **tight for delta = 3 and 4**.
  Note `gamma_2(Q_3) = 4 = 8/2` — session 2's n=3 value sits exactly on this
  known tight bound, an independent consistency check on the computation.
* Bujtás–Jaskó improve this for `6 <= delta <= 21`: `delta = 7` gives
  `gamma_2 < 0.467|V|`, so `gamma_2(Q_7) < 59.8`. True value 32 — consistent,
  far from tight.
* Probabilistic bound `gamma_2(G) <= (2 ln(delta+1) + 1)/(delta+1) * |V|`
  gives `gamma_2(Q_7) <= 82.5` and `gamma_2(Q_9) <= 287`.

Session 2's algebraic parity-check construction gives 32 and 128 respectively,
**beating all of these general bounds substantially**. Whether that construction
is new for hypercubes is exactly what (c) would settle.

### (e) The OEIS check — COULD NOT BE COMPLETED, and is mis-specified as written

Two separate problems, both worth recording.

**Access.** `oeis.org` returned **HTTP 403 Forbidden** on every URL attempted:
the text search, the JSON API, the wiki page, and individual A-number pages. I
have no direct OEIS result, positive or negative. I am not reporting "no match
found" — I am reporting "not checked".

**Specification.** Even with access, searching `4, 10, 32` would likely fail
regardless of whether the sequence is present. Those are
`gamma_2(Q_3), gamma_2(Q_5), gamma_2(Q_7)` — **non-consecutive** terms of
`gamma_2(Q_n)`. OEIS matches *consecutive* subsequences. The sequence to search
is `gamma_2(Q_1..Q_7) = 2, 2, 4, ?, 10, ?, 32`, and **`gamma_2(Q_4)` and
`gamma_2(Q_6)` were never computed** — session 2 only ran odd n.

Recommended (next computational session, not this one): compute `gamma_2(Q_4)`
and `gamma_2(Q_6)`. Both are small — the Fink–Jacobson bound gives
`gamma_2(Q_4) >= 6` and `gamma_2(Q_6) >= 16` — and the same feasibility MILP
that settled n=5 in milliseconds will settle them. Then search the full
consecutive sequence.

Indirect searching did establish that **A000983** is the ordinary domination
number `gamma(Q_n)` (1, 2, 2, 4, 7, 12, 16, 32, 62), and surfaced **no**
`gamma_2(Q_n)` sequence. Weak evidence only.

**Incidental confirmation:** published `gamma(Q_n)` values include
`gamma(Q_7) = 16` and `gamma(Q_9) = 62`, both of which session 2 relied on as
background facts (the dominating-regime threshold). Independently confirmed.

---

## Direction 5 — Strategic source coding / mechanism design

**Verdict: NO COLLISION. Related-work paragraph, as the C39 update predicted.**

The nearest work models a **strategic sender** who may misreport, with
incentive compatibility meaning *truthfulness of the sender*, posed as a
Stackelberg game. C39's encoder is designed by the principal and is honest; the
incentive constraint is on the **downstream payment's sensitivity to each
agent's action**, which is a constraint on the *record*, not on the encoder's
honesty. The elimination theorem (payments removable, leaving a total-variation
condition on edges) has no counterpart there.

A 2026 paper unifying rate-distortion, strategic communication, Bayesian
persuasion and semantic compression under a "posterior design" framework is the
closest umbrella, and is worth citing as the frame C39 sits beside — but it
optimises inference under misaligned objectives, not per-agent action
sensitivity of a shared record.

- [Achievable Rates for Information Extraction from a Strategic Sender (arXiv:2307.02644)](https://arxiv.org/pdf/2307.02644)
- [Semantic Rate Distortion and Posterior Design (arXiv:2602.03949)](https://arxiv.org/html/2602.03949)

---

## Summary table

| # | Direction | Verdict |
|---|---|---|
| 1 | One-bit CEO / distributed estimation | No overlap on the constrained problem; `D0` baseline is classical, do not claim it |
| 2 | Boolean analysis / influence extremal | No overlap — literature bounds influence *above*, C39 bounds it *below* |
| 3 | Rate-distortion with side constraint | No overlap; cite RDP as structural precedent |
| 4 | `gamma_2(Q_n)` | **Counting bound = Fink–Jacobson 1985, NOT novel.** Invariant is correctly named. One on-topic paywalled paper must be checked. OEIS check not completed. |
| 5 | Strategic source coding / mechanism design | No collision; related-work only |

## What survives, stated narrowly

* The **payment-decoder elimination theorem** and the resulting TV edge
  condition — no counterpart found in any direction searched.
* The **reduction** `K_flat(n) = gamma_2(Q_n)` — connecting a
  reconstruction/incentive frontier to a domination invariant. Not found
  anywhere. This is the contribution.
* **T1**, the exact `K=2` frontier `D*(2,gamma) = M_n + n*gamma*((n-1)/2 - M_n)`
  — no collision found, but on direction-2 evidence that is an absence of
  keyword matches, not a proof of novelty.

## What must be corrected or downgraded

1. Attribute `2^(n+1)/(n+2)` to **Fink & Jacobson (1985)** throughout.
2. Reframe `K_flat(3,5,7,9)` as *evaluating a known invariant*, not as new
   combinatorics. The reduction is the contribution; the numbers are a corollary.
3. Obtain Arulanand–Sundara Rajan–Prabhu (2023) before writing anything.
4. Compute `gamma_2(Q_4)`, `gamma_2(Q_6)`, then redo the OEIS check properly.

---

# VERIFICATION SESSION — 2026-09-14

Verification only. No new theory, no P4, no paper drafting. No computational
result in `research_state.md` was modified.

## Task 1 — The consecutive sequence gamma_2(Q_n)

### A solver that had never been validated

Correction to an assumption in the task brief: session 2's brute-force
cross-validation (`bruteforce_d0.py`) validated **`solve_D0_pmedian`**, the
K-median solver. The 2-domination feasibility MILP **`two_dominating_set`** is a
different solver and had **never** been independently checked. Since every
`K_flat` value now rests on it, it was validated first.

* **METHOD X** — complete enumeration of all `2^(2^n)` subsets of `V(Q_n)`,
  no LP, no MILP, no pruning. Feasible for n <= 4.
* **METHOD M** — the session-2 MILP.

| n | subsets enumerated | METHOD X | METHOD M | result |
|---|---|---|---|---|
| 1 | 4 | 2 | 2 | AGREE |
| 2 | 16 | 2 | 2 | AGREE |
| 3 | 256 | 4 | 4 | AGREE |
| 4 | 65536 | 7 | 7 | AGREE |

The gamma_2 solver is now independently validated on every case where complete
enumeration is possible.

### The sequence

> **gamma_2(Q_n), n = 1..7  =  2, 2, 4, 7, 10, 16, 32**
>
> plus `97 <= gamma_2(Q_9) <= 128` from session 2. `gamma_2(Q_8)` not computed
> (Fink-Jacobson gives `>= 52`).

`gamma_2(Q_3) = 4` and `gamma_2(Q_5) = 10` reproduce in the current checkout, as
required. **New values: `gamma_2(Q_4) = 7`, `gamma_2(Q_6) = 16`.**

### Per-solve status

**On "MIP gap": these are pure feasibility problems with a zero objective, so
the MIP gap is trivially 0 and is not the meaningful quantity.** The meaningful
quantity is the solver status. Recorded honestly as such:

| n | K values tested | statuses | time |
|---|---|---|---|
| 1 | 1, 2 | infeasible(2), feasible(0) | 0.01s |
| 2 | 1, 2 | infeasible(2), feasible(0) | 0.00s |
| 3 | 1, 2, 3, 4 | infeasible x3, feasible | 0.01s |
| 4 | 1..6, 7 | infeasible x6, feasible | 0.03s |
| 5 | 9, 10 | infeasible(2), feasible(0) | 0.01s |
| 6 | 16 | feasible(0) | 0.00s |
| 7 | 28, 29, 30, 31, 32 | infeasible x4, feasible | 12.6s |

**No solve timed out; every row terminated with status 0 or status 2. There are
no inconclusive rows.** Each feasible witness was independently rechecked by
`check_two_dominating` (all returned `is_2_dominating = True`, `min_deg >= 2`).

At n = 5, 6 the scan starts at the Fink-Jacobson bound rather than at K = 1;
that is rigorous, since FJ proves no smaller K can work. At n = 6 the bound is
`128/8 = 16` exactly and K = 16 is feasible, so `gamma_2(Q_6) = 16` needs no
search below.

### Fink-Jacobson tightness — a new data point, and it matters for Task 3

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| gamma_2(Q_n) | 2 | 2 | 4 | **7** | 10 | 16 | 32 |
| `ceil(2^(n+1)/(n+2))` | 2 | 2 | 4 | 6 | 10 | 16 | 29 |
| FJ tight? | yes | yes | yes | **NO (+1)** | yes | yes | **NO (+3)** |

The new n=4 value is a **second** counterexample to tightness, independent of
n=7. This sharpens the tension with the Arulanand et al. abstract (Task 3).

## Task 2 — Check against published values, without OEIS

Per instruction, oeis.org paths were **not** retried and no negative is inferred
from last session's 403s.

**(a) Literal sequence search.** Searched `2, 2, 4, 7, 10, 16, 32` and
`4, 7, 10, 16, 32` in comma- and space-separated form. **No page quoting the
sequence was found.** Hits were unrelated (polar-coding patents).

**(b) Tables in the domination literature.** Searched Fink-Jacobson,
Bujtas-Jasko, the Chellali et al. k-domination survey, and hypercube-domination
papers for tables of small gamma_2(Q_n). Bujtas-Jasko give only general upper
bounds by minimum degree, no hypercube table. **No published table of
gamma_2(Q_n) small values was located.**

One consistency check did land: Bujtas-Jasko record that `gamma_2(G) <= |V|/2`
for `delta >= 3` is **tight for delta = 3**, and `gamma_2(Q_3) = 4 = 8/2` sits
exactly on it.

**(c) Mirrors/caches.** No accessible OEIS mirror or cache was found.
**The OEIS check remains NOT CHECKED.** Not a negative result.

### Ruling out the most likely false match

Our sequence is close to a published one, and this needed eliminating.
**2-rainbow domination** satisfies `gamma_r2(G) = gamma(G x K_2)`, and
`Q_(n+1) = Q_n x K_2` (Cartesian product), so `gamma_r2(Q_n) = gamma(Q_(n+1))`:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| ours, gamma_2(Q_n) | 2 | 2 | 4 | 7 | **10** | 16 | 32 |
| gamma_r2(Q_n) = gamma(Q_(n+1)) | 2 | 2 | 4 | 7 | **12** | 16 | 32 |

Identical at six of seven points and differing only at n = 5. This is a genuine
near-miss between two distinct invariants, not a rediscovery: our value 10 is
backed by an explicit verified witness plus the FJ bound `>= 9.14`, and
`gamma(Q_6) = 12` is published. **Our sequence is not the rainbow sequence and
not `gamma(Q_n)`.** Anyone checking this by eye could easily conflate them, so
it is recorded explicitly.

**Task 2 outcome: NOT FOUND.** No published gamma_2(Q_n) values were located to
compare against — neither matching nor contradicting.

## Task 3 — The blocking paper

> S. Arulanand, R. Sundara Rajan, S. Prabhu, "2-domination number for special
> classes of hypercubes, enhanced hypercubes and Knodel graphs",
> IJNVO **29**(2), 168-182, 2023.

**Not obtained.** Routes attempted:

| route | outcome |
|---|---|
| (a) later/extended/conference/thesis version | none found |
| (b) institutional pages, ResearchGate, dblp | dblp returned **Access Denied**; no deposited copy found |
| (b) Semantic Scholar API | **HTTP 429** on all attempts, including after backoff |
| (c) citing papers quoting their hypercube values | the authors' open-access RAIRO paper returned **HTTP 403**; no citing paper quoting their values found |
| (c) Inderscience article page | the page reached under the artid returned by search is a **different paper** (*On 2-domination number in certain octahedral networks*, IJNVO 27(3), 2022) — the hypercube paper's own page was not reachable and exposes no contact details |
| (d) email draft | written to `author_request_draft.txt`, **not sent**; recipient address could not be determined and is left as a placeholder rather than guessed |

**Our n=7 value of 32 is therefore still UNKNOWN against this paper — neither
confirmed nor contradicted.**

The open question is unchanged and now sharper. Their abstract says the
Fink-Jacobson bound is "quite precise" for their classes. We now have **two**
dimensions where it is not attained (n=4 by 1, n=7 by 3). Either their "special
classes" are dimensions where it is attained, or "quite precise" means a ratio
rather than equality, or there is a genuine disagreement. An abstract cannot
distinguish these.

## VERDICT: UNRESOLVED

Not CONFIRMED, and deliberately not upgraded to CONFIRMED. What this session
produced is **stronger internal validation** — complete enumeration agreeing
with the MILP at n = 1..4, a filled-in consecutive sequence, and independent
rechecks of every witness. That is our computation agreeing with itself, and
with one published *bound*. It is not agreement with published *values*, because
no published values were found.

### Still unknown

1. Whether any published source states gamma_2(Q_n) for n = 4..7.
2. Whether Arulanand et al. (2023) already contains 4, 10, 32 or the n=4 and n=6
   values — which would make session 2's computation a re-derivation.
3. Whether "quite precise" in that abstract conflicts with our n=4 and n=7
   counterexamples to FJ tightness.
4. Whether OEIS contains gamma_2(Q_n). Never checked, in either session.

### What would close it

* **Obtain IJNVO 29(2):168-182.** Interlibrary loan, an institutional
  subscription, or sending the drafted email. This is the single highest-value
  action and closes items 2 and 3.
* **One OEIS query from an unblocked network** for `2, 2, 4, 7, 10, 16, 32`,
  now that the sequence is consecutive and correctly specified. Closes item 4.
  This is a browser lookup, not a research task.
* **`gamma_2(Q_8)`** would extend the sequence and strengthen any OEIS match.
  Currently only `>= 52` from FJ; likely expensive (256 binaries).

### What does NOT change

The earlier sections of this file stand. In particular the Fink-Jacobson
attribution is unaffected — that hit was confirmed from independent sources and
does not depend on the Arulanand paper. The overall verdict **NOVEL WITH CLOSE
PRIOR ART TO CITE** is unchanged, with the same blocking caveat, now with two
additional FJ counterexamples that make the caveat more pointed rather than less.
