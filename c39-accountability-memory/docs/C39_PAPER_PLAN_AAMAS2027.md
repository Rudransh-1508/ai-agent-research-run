# C39 — Paper plan

**Date:** 2026-09-14
**Decision:** COMPLETE AND SUBMIT. Reframed, not switched.
**Target:** AAMAS 2027 main track, **COINE** (Coordination, Organizations,
Institutions, Norms, and Ethics), secondary keyword GTEP / GAAI.
**Status of gates:** P1 done (`literature_review.md` + §6 of the P4 addendum),
P4 resolved to STAKES PRESENT (`P4_ADDENDUM_2026-09-14.md`), Arulanand et al.
closed out as cite-don't-rely.

---

## 0. The deadline that decides everything

| Milestone | Date | Note |
|---|---|---|
| **Author registration** | **17 Sep 2026** | **3 days away. Miss this and there is no submission.** No paper needed — register the authors. |
| Abstract submission | 1 Oct 2026 | title + abstract only |
| Paper submission | 8 Oct 2026 | 8 pages + unlimited references, LaTeX mandatory |
| Rebuttal | 20–24 Nov 2026 | |
| Notification | 21 Dec 2026 | |
| Camera-ready | 25 Jan 2027 | |
| Conference | 3–7 May 2027 | Hanoi, Vietnam |

Unselected main-track papers are automatically considered for **Findings of
AAMAS 2027** (same length and format) unless the authors opt out. Do not opt out.
That is a real safety net and it costs nothing.

Source: [AAMAS 2027 CFP](https://warwick.ac.uk/fac/sci/dcs/aamas2027/calls/),
[first call, full text](http://dmatheorynet.blogspot.com/2026/08/dmanet-aamas-2027-call-for-papers-first.html).

If "MASO" refers to a specific workshop rather than the MAS venue family, this
plan ports to it unchanged — AAMAS workshop deadlines land around February, which
would give the paper a second, later outlet with the same content.

---

## 1. The one-sentence pitch

> When a multi-agent record is compressed, the amount you may compress it before
> accountability starts costing reconstruction accuracy is exactly `2^n /
> gamma_2(Q_n)` — at most a factor of `(n+2)/2` — and every summarisation step in
> a modern agent stack is far past that point.

The paper is a **theorem about organizational memory under deferred
accountability**, which is precisely what §21 of `agent_research_master_context.md`
pre-registered as the right MASO framing. Nothing in the framing is new
opportunism; it is the plan the project already committed to, now with the
evidence it was waiting for.

---

## 2. Title

**How Much Memory Does Accountability Cost? Exact Reconstruction–Incentive
Frontiers for Compressed Multi-Agent Records**

Alternatives if a shorter title is wanted:
* *The Price of Accountability in Compressed Agent Memory*
* *What a Compressed Record Must Keep About Who Did the Work*

---

## 3. Abstract (draft — use nearly as-is)

> Multi-agent systems routinely discard their own execution histories.
> Sub-agents return summaries rather than transcripts, orchestrators compact
> their context to fit a fixed window, and observability backends sample runs
> away. Whatever survives is then the only evidence available when the system
> must later decide what each agent actually did — for payment, for credit, or
> for accountability. We study that conflict exactly. A record with `K` labels
> must simultaneously (i) permit reconstruction of the joint effort profile
> `S in {0,1}^n` with small expected Hamming error and (ii) retain enough about
> each agent's unilateral contribution that a bounded payment computed from the
> record alone rewards effort by at least `gamma`, whatever the teammates did.
> Our first result removes the payment rule from the problem: a record admits a
> bounded `gamma`-margin payment for agent `i` if and only if every unilateral
> deviation by `i` moves the retained label distribution by at least `gamma` in
> total variation, minimised over mixtures of teammate profiles. Accountability
> is therefore exactly a lower bound on the record's sensitivity to each
> individual. Using it we obtain (a) the exact frontier for a one-bit record,
> `D*(2,gamma) = M_n + n*gamma*((n-1)/2 - M_n)` for `0 <= gamma <= 1/n`, verified
> to machine precision at `n = 3,5,7,9`; and (b) an exact identification of the
> threshold at which accountability becomes free as a classical graph invariant,
> `K_flat(n) = gamma_2(Q_n)`, the 2-domination number of the `n`-cube, with an
> explicit optimal record achieving margin `1 - 1/d_min >= 1/2`. Hence
> `K_flat(3) = 4`, `K_flat(5) = 10`, `K_flat(7) = 32`, and
> `97 <= K_flat(9) <= 128`. The free compression ratio is `Theta(n)` and at most
> `(n+2)/2`, so a record that is free of the tension must retain
> `n - log2 Theta(n)` bits — roughly 85% of per-agent resolution at `n = 20`.
> Every summarisation step in a contemporary agent stack compresses far harder
> than that, placing it inside the regime where the two uses of the record
> genuinely trade off.

Word budget: trim to ~200 words for submission; the long version above is the
content inventory.

---

## 4. Contributions, as they will be listed

1. **Payment-decoder elimination (Theorem 1).** Bounded payment functions are
   eliminated from the feasibility question by a minimax argument, leaving an
   optimisation over the encoder alone. The clean corollary — *every unilateral
   deviation must move the retained label distribution by at least `gamma` in
   total variation* — is the general statement of the phenomenon, and it is what
   a MAS audience should take away even if they read nothing else.
2. **Exact one-bit frontier (Theorem 2, = T1).** `D*(2,gamma)` in closed form,
   linear in `gamma`, with the structural reason for linearity (the feasible set
   is an affine shift of the monotone cone and the objective is linear).
3. **Exact flatness threshold (Theorem 3).** `K_flat(n) = gamma_2(Q_n)`, both
   directions, with an explicit optimal construction and its exact margin.
4. **Certified values and a new counting bound.** `K_flat = 4, 10, 32` at
   `n = 3,5,7`, `97 <= K_flat(9) <= 128`, via a shell counting bound that is
   tight at every known flat point.
5. **The engineering reading.** Free compression ratio `Theta(n)`, bounded by
   `(n+2)/2`; the design rule that one retained bit per agent is always flat;
   and a deployed case (Bittensor) where a merged settlement record destroyed
   unilateral effort sensitivity and was repaired by changing the record.

---

## 5. Section plan and page budget (8 pages + references)

### §1 Introduction — 1.0 p
Open on the concrete fact, not the abstraction: in a fan-out, *only the
sub-agent's final message returns to the parent*, and on compaction the
orchestrator is *handed back a summary*. So the parent's record of what each
sub-agent did is a lossy aggregate produced under a hard budget. Then: that same
record is what any later settlement, credit assignment, or post-hoc report must
read. State the two demands, state that they conflict, state that we give the
exact rate.

Use the Bittensor sentence early — *"optimized weight copiers achieve higher
validator dividends per stake than honest validators"* — as the existence proof
that the failure is not hypothetical. One paragraph, no more.

Close with the contribution list from §4 and the headline number: at most
`(n+2)/2` compression is free.

### §2 Model — 0.75 p
`S in {0,1}^n` uniform; stochastic encoder `q[s,y]`, `y in [K]`; reconstruction
decoder; bounded per-agent payment `p_i in [0,1]^K`; all-teammate-profile
unilateral margin `gamma`; `D*(K,gamma)`.

**Do not skip the counting rule:** all decoder-side state counts toward `K`.
Say why in one sentence — otherwise the tradeoff is defeated by hiding a seed,
receipt, or auxiliary variable outside the counted record. A referee will look
for exactly this hole.

Flag the three modelling choices honestly here, not only in limitations: binary
effort, uniform prior, symmetric Hamming loss.

### §3 Eliminating the payment rule — 1.0 p
Theorem 1 with its proof (it is short: inner min over a finite set equals min
over its convex hull; bilinear objective on a convex compact cube; minimax; then
`sum_y (E_lambda[d])_y^+ = (1/2)||E_lambda[d]||_1` because `sum_y d_y = 0`).

State the point-mass corollary as the headline: **every hypercube edge must move
the retained label distribution by at least `gamma` in total variation.**

One remark on what this buys computationally: the bilinear MILP that did not
terminate at `n = 7` is replaced by a feasibility question over `2^n` binaries.
This is the sentence that makes the rest of the paper's numbers credible.

### §4 The one-bit frontier — 1.25 p
Theorem 2. Present via the decomposition `q(s) = gamma*|s| + r(s)`, so the
constraint is exactly "`r` is monotone on the cube"; then a linear objective over
a shifted monotone cone; then the optimum is majority plus a random-bit sampler.

**Fix the proof-order gap from `C39_UPDATE_2026-09-13.md` §1.2** before writing:
`D(q)` is concave in `q` under optimal decoding, so permutation averaging runs
the wrong way for a lower bound. Correct order: fix the decoder pair, average
(objective now linear), optimise over `q`, then optimise over decoder pairs.
This must be right in the submitted version; it is the single most likely
technical objection.

Figure 1: the frontier lines for `n = 3,5,7,9` (data in `exp1b_results.json`;
`frontier.png`/`frontier.svg` already exist — regenerate to match final styling).
Table 1: exact agreement with the closed form, max deviation `0`, `0`, `4.4e-16`,
`2.7e-15`.

### §5 When is accountability free? — 1.75 p  ← the heart of the paper
* Definition of `K_flat(n)`.
* **Necessity (Lemma 3').** Unique nearest centre propagates along the edge
  toward it, both endpoints become point masses on the same label, the edge
  derivative vanishes, so `<p_i, d_i> = 0` for *every* bounded payment. Stress
  that this constrains arbitrary bounded decoders — it is not a binary-payment
  artifact.
* **Sufficiency.** The construction: point mass on each centre, non-centres
  spread uniformly over their centre neighbours, pay agent `i` the reconstructed
  `i`-th bit. Then `D = D0(K)` exactly and the margin is exactly `1 - 1/d_min`.
* **Theorem 3:** `K_flat(n) = gamma_2(Q_n)` in the dominating regime, with the
  small-`K` regime excluded separately by the shell bound.
* **The shell counting bound**, stated as a lemma: shell `r` holds at most
  `floor(K*C(n,r)/2)` states, fill shells from the inside, compare against an
  upper bound on `N*D0(K)`. Note it is tight at every known flat point.
* Table 2: the certificate chain per `n` — which `K` excluded by the shell bound,
  which by proved MILP infeasibility, which achieved by an explicit verified code.
* Be explicit that `97 <= K_flat(9) <= 128` is open and say which three routes
  failed. Referees reward this; hiding it is what gets punished.

Figure 2 (cheap, high value): `Q_3` with its 4-element 2-dominating set, arrows
showing the uniform spread, and the payment `p_i` = reconstructed bit. One
column wide. It makes the construction obvious in three seconds.

### §6 What this says about agent systems — 1.0 p
* `C(n) = 2^n / K_flat(n)` is `Theta(n)`, bracketed by
  `2^floor(log2(n/2+1))` and `(n+2)/2`.
* **Both normalisations, stated honestly** (this is `research_state.md` §4 and it
  is the intellectually strongest page in the project): as a ratio the safe zone
  widens with team size; in bits the free allowance is only `log2(n/2)` out of
  `n`, so the free *fraction* of per-agent resolution shrinks — 33.6% at `n = 5`,
  15–17% at `n = 20`, 8–9% at `n = 50`. Linear growth of a ratio against an
  exponential baseline is logarithmic growth in bits. Give the table.
* **The design rule:** one retained bit per agent is always flat and has no
  tension at all. An aggregate such as "how many agents succeeded"
  (`log2(n+1)` bits) is deep in the tension regime. That is a rule a MAS engineer
  can act on, and it is the paper's practical payload.
* **The deployed case.** Bittensor in one short paragraph with the mapping table
  from `P4_ADDENDUM_2026-09-14.md` §E1, including the honest caveat that its
  record bound is temporal rather than size-based, and the observation that
  commit-reveal interval tuning (converging at 1800 blocks) is an operator
  literally choosing a point on a reconstruction-vs-incentive curve.

### §7 Related work — 0.75 p
Five groups, one or two sentences each:
1. **Distributed source coding / binary CEO problem.** Closest in form; no CEO
   result imposes a lower bound on the summary's sensitivity to an individual
   input bit. Table of structural differences if space allows, otherwise prose.
2. **Domination and covering codes.** `gamma_2` is a studied invariant; the
   `gamma_k(G) >= k|V|/(Delta+k)` bound is **Fink–Jacobson (1985)** and must be
   attributed there, not to us. Cite Cohen–Honkala–Litsyn–Lobstein for multiple
   coverings and note that 2-domination differs from a 2-fold 1-covering exactly
   by the internal-edge condition. Cite Arulanand et al. (2023) from its abstract
   as existing work on `gamma_2` of hypercube classes.
3. **Provenance and failure attribution in MAS.** IET / "When Only the Final Text
   Survives" (arXiv:2603.17445) is the same setting with honest agents; Who&When,
   FAMAS for failure attribution. Position: they ask whether attribution is
   *recoverable*, we ask what the record must keep for payment from it to remain
   *incentive-compatible*.
4. **Trace compression for agents.** TRACE, TRACER — compression policies
   optimised for task performance, no incentive term. This is the gap sentence.
5. **Credit assignment under collapsed reward.** Dec-POMDP shared team reward,
   QMIX/COMA/value decomposition, RLHF sequence-level reward and process reward
   models. Note these exhibit the consequence without the record-budget mechanism
   — the per-agent signal never existed. Being precise here is a credibility win.

### §8 Limitations and open problems — 0.5 p
State as a numbered list, unhedged:
1. Uniform prior and binary effort; the input-flip step is only valid because the
   uniform prior is flip-invariant, so non-uniform priors need a new argument,
   not a perturbation.
2. `K_flat(9)` open in `[97, 128]`; `gamma_2(Q_n)` has no closed form and is a
   hard invariant — that is a feature of the reduction, not a defect of it.
3. One-shot; no repeated interaction, reputation, or external audit channel.
4. The money-plus-storage-bound conjunction is not yet observed in a single
   deployed system (P4 addendum §4). Say it in the paper. A referee who finds it
   themselves will hold it against the paper; a paper that states it reads as
   careful.

---

## 6. Reviewer objections, and the answers to have ready

| # | Objection | Answer |
|---|---|---|
| 1 | "Just log per agent, or pay immediately." | One retained bit per agent *is* our flat case — the theorem says so, and we say so. The result is about what happens when you cannot: a fixed context window, a fan-out summarised into a paragraph, settlement deferred to a dispute. We quantify exactly when that assumption bites. |
| 2 | "This is rate-distortion / the CEO problem." | No CEO result bounds the summary's sensitivity to an individual input bit; the incentive constraint has no analogue there. We also never claim `D0` or the coding constructions are new — only the frontier under the constraint. |
| 3 | "`gamma_2(Q_n)` is already known." | Agreed and cited. The contribution is the reduction, not the invariant. Once `K_flat = gamma_2(Q_n)`, computing values is evaluating a known invariant — we say that in the paper. |
| 4 | "Where is the real system?" | §6: the compaction/sub-agent evidence for the geometry, Bittensor for the consequence, IET (arXiv:2603.17445) for the regime being a stated open problem elsewhere. Plus the honest gap. |
| 5 | "Binary effort and a uniform prior are toys." | Conceded and bounded in §8. The `K = 2` frontier is exact for arbitrary bounded payments and arbitrary reconstruction, which is the strongest form available at that record size. |
| 6 | "The margin condition is unusually strong." | Intentionally: all-teammate-profile, not Nash. That makes the impossibility results *stronger* and the construction results *harder*, which is the conservative direction for both. |
| 7 | "Is the `n=7` value right?" | Two independent routes agree (MILP infeasibility chain at 29–31 plus an explicit verified code at 32; the algebraic construction produces the same 32), and `gamma_2(Q_6) = 16`, `gamma_2(Q_7) = 32` coincide with the published `gamma(Q_7)`, `gamma(Q_8)`. |

---

## 7. The predeclared kill test — recommended resolution

**Recommendation: record the discriminator as retired, not as fired.**

The test keys on `K_flat(5) = 10 = 2n` being the "expected/trivial" outcome. The
hypothesis behind it — that `K_flat` grows like `2n` — is now decisively refuted:
`K_flat(3) = 4` (not 6) and `K_flat(7) = 32` (not 14). A discriminator that is
wrong at `n = 3` and wrong by more than a factor of two at `n = 7`, and right at
`n = 5` only because `2n` and `ceil(2^(n+1)/(n+2))` happen to collide at 10, is
mis-specified rather than satisfied.

Two guardrails, because session 1's replacement formula was itself falsified and
that is a reason to trust fitted stories less:
* Do not replace it with another fitted curve. The defensible object is the exact
  identification `K_flat = gamma_2(Q_n)`, which is a proof, not a fit.
* Write the retirement down in `research_state.md` §7 with this reasoning, dated,
  so the decision is on the record rather than implied by having written a paper.

This remains the user's call. It is the only item in this plan that is.

---

## 8. Work plan, 14 Sep → 8 Oct

**Now (by 17 Sep) — non-negotiable**
- [ ] Register authors on the AAMAS 2027 submission site. **17 Sep.**
- [ ] Decide and record the kill test (§7).
- [ ] Re-run every session-2 result in the pinned environment (Python 3.10.11,
      NumPy 2.2.6, SciPy 1.15.3). `C39_UPDATE_2026-09-13.md` records that the
      current numbers came from 3.12.3 / 2.4.4 / 1.17.1, which does not match
      `environment.json`. Refresh `artifact_hashes.json` after.

**17–23 Sep — the mathematics**
- [ ] Fix the T1 proof order (concavity/averaging direction, §5 above).
- [ ] Write §2, §3, §4, §5 in LaTeX in the AAMAS template.
- [ ] Figure 1 (frontier), Figure 2 (`Q_3` construction), Tables 1–2.

**24–28 Sep — the framing**
- [ ] Write §1, §6, §7, §8.
- [ ] Pull §6's numbers directly from `research_state.md` §4 — do not re-derive
      them in prose and risk drift.

**29 Sep – 1 Oct**
- [ ] Full read-through; cut to 8 pages; move proof detail to the appendix.
- [ ] **Submit title + abstract, 1 Oct.**

**2–7 Oct**
- [ ] Appendix: full proofs, certificate tables, the explicit codes.
- [ ] Reproducibility package: code, `environment.json`, `artifact_hashes.json`,
      a one-command verifier that re-checks the `n = 3,5,7,9` certificates with
      no solver.
- [ ] **Submit, 8 Oct.** Do not opt out of Findings.

---

## 9. Honest assessment of acceptance chances

**What is strong:** a clean theorem with a short proof (Theorem 1 is the kind of
result a referee enjoys); an unexpected exact reduction to a classical invariant;
solver-free verifiable certificates; a falsified earlier conjecture reported as
falsified, which reads as unusual discipline; and a deployed failure case with a
deployed fix.

**What is weak:** the model is small (binary effort, uniform prior); the
headline threshold is a known-hard invariant with no closed form; the strongest
real-world instance (Bittensor) matches on consequence rather than on the size
mechanism; and the whole thing is being written in three weeks.

**Net:** genuinely competitive for COINE on substance, with schedule as the
dominant risk rather than content. Findings of AAMAS is a real fallback and the
February workshop round is a second one. The expected value of writing it clearly
exceeds the expected value of returning to candidate discovery, which is the
decision this plan actually settles.

---

## 10. Files this plan depends on

| File | Role in the paper |
|---|---|
| `research_state.md` | §5 and §6 content; the certificate chains; the two-normalisation argument |
| `C39_UPDATE_2026-09-13.md` | Theorem 1 statement and proof; the T1 proof-order fix |
| `kflat_theory.py` | Lemma 3', the construction, solver-free verification |
| `literature_review.md` | §7, and the Fink–Jacobson attribution correction |
| `P4_ADDENDUM_2026-09-14.md` | §1 and §6 motivation; all deployed-system claims |
| `exp1b_results.json` | Table 1, Figure 1 |
| `environment.json`, `artifact_hashes.json` | reproducibility package (refresh first) |
