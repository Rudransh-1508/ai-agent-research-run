# TODO — review round 2 (opened 2026-09-15)

Source: reviewer feedback asking for MAS positioning, more empirical validation,
and precision about what the model does and does not claim. Ordered by what
blocks what, not by the order given.

**Standing constraint from the brief:** do not expand the theory, and do not
change the core research question. The story stays: *compression is not merely
losing information; under deferred accountability it can destroy the information
structure needed to distinguish individual effort.*

**Standing constraint discovered while planning:** the body is at **exactly 8
pages**, the limit. Items 12–18 all add content. Something must move to the
appendix for each thing added; this is tracked as item 26 and must be re-checked
after every batch.

---

## Phase 1 — framing and precision (no new experiments, page-neutral)

- [x] 1. **MAS-first framing.** Open on multi-agent context/trace compression
      destroying individual accountability. The hypercube is machinery, not the
      subject. Title, abstract, §1 opening.
- [x] 2. **Sharper theorem roadmap, early.** State plainly: Thm 3 removes the
      payment rule; Thm 5 gives the exact extreme-compression tradeoff; Thm 9
      gives the point where the tradeoff vanishes; the experiments show real
      compaction exhibits the predicted identity loss.
- [x] 3. **Payment model precision.** Stop implying incentive compatibility.
      $\langle p_i,d_i\rangle \ge \gamma$ is a **payment margin** /
      **accountability margin**. Either add an explicit effort-cost model or say
      clearly that costs are not modelled.
- [x] 4. **Not an equilibrium model.** Make it impossible to read the result as
      complete mechanism design.
- [x] 5. **$K$ versus bits.** $K$ is a label count; fixed-length memory is
      $\log_2 K$ bits. Keep separate everywhere.
- [x] 6. **Scope of stochastic encoding.** What randomness is allowed, what
      persists, and why encoder-side randomness or auxiliary state cannot supply
      accountability for free.
- [x] 7. **$n=9$ status.** Theorem exact; invariant only bracketed
      $97 \le \Kflat(9) \le 128$. (Remark 11 exists — surface it earlier.)
- [x] 8. **Bittensor reframed** as evidence of the merged-record accountability
      problem, not an instance of the size-constrained frontier.
- [x] 9. **Remove defensive wording**, specifically the Arulanand retrieval
      story. Cite narrowly or not at all.
- [x] 10. **Certificates in the main text**, not only the appendix.
- [x] 11. **Threats to validity**: binary effort, synthetic episodes, one-shot,
      bounded payments, no external audit or shared state.

## Phase 2 — empirical, the reviewer's core ask

- [x] 12. **Explicit empirical hypothesis (H1):** *compression that removes agent
      identity causes a disproportionate loss in accountability relative to its
      reduction in storage.* Pre-register before running anything new.
- [x] 13. **More compaction mechanisms in §7.1** — at least three more, chosen to
      be realistic rather than convenient.
- [x] 14. **Several $n$**, not only $n=5$.
- [x] 15. **Intermediate $K$.** $K = 3,4,\dots$ at small $n$ by LP/MILP, showing
      how the frontier moves between severe compression, intermediate, and
      flatness.
- [x] 16. **Plots**: (a) compression vs reconstruction error vs accountability
      margin; (b) $\Dopt(K,\gamma)$ across $K$.
- [ ] 17. **Pipeline diagram**: agents → traces → compactor → record →
      reconstruction + payment.
- [ ] 18. **Summary figure**: record budget → reconstruction quality →
      accountability margin → flatness threshold.
- [x] 19. **Identity-vs-volume promoted** to a headline contribution.
- [ ] 20. **Noise result elevated**, with the mechanism stated: it buys margin by
      sacrificing reconstruction.
- [ ] 21. **Uniform prior promoted** from limitation to insight: the symmetric
      case is the most favourable one for accountability.
- [x] 22. **Design Implications subsection** straight after the empirical
      section: preserve agent identity; keep an independent witness per agent
      where possible; do not rely on global counts; more retained content does
      not mean more accountability.
- [x] 23. **A real LLM-agent experiment.** A genuine multi-agent task, agents
      producing artifacts, then compare full trace / per-agent summaries / global
      summary / artifact multiset / ID-preserving compression / final-output-only,
      measuring attribution explicitly.
      **Blocked:** needs API credentials and the user's approval for spend. The
      harness should be built to ingest real traces so that running it is the
      only remaining step.

## Phase 3 — audits

- [ ] 24. **Novelty/related-work audit** across: mechanism design with limited
      signals; moral hazard under restricted observability; communication
      complexity and incentives; information design; provenance/attribution in
      MAS; LLM-agent trace compression; credit assignment.
- [ ] 25. **Every reference verified** — DOI/arXiv identifier, authors, venue.
      Target zero errors.

## Cross-cutting

- [ ] 26. **Page budget** re-checked after every batch; body must end by page 8.

---

## Log

Append one line per item as it closes, with the evidence.

### 2026-09-15 — first working session on this list

Closed: 1–16, 19, 22.

* 1,2,8 — MAS-first framing, four-move roadmap, Bittensor recast as evidence of
  the merged-record problem rather than an instance of the frontier.
* 3,4 — "accountability margin", not incentive compatibility; §2 now says
  explicitly that costs are not modelled and this is not an equilibrium model.
* 5 — labels vs bits separated throughout; storage is reported as log2 K.
* 6 — scope of stochastic encoding stated, including why encoder randomness and
  auxiliary state cannot buy margin for free.
* 7 — n=9 status made explicit at first mention, not only in Remark 11.
* 9 — the Arulanand retrieval narrative removed; cited narrowly.
* 10,11 — reproducibility paragraph in §1; threats-to-validity in §10.
* 12 — H1 pre-registered quantitatively (the "identity price") before any new run.
* 13,14 — three realistic mechanisms added (recency window, role rollup, quality
  summary); sweep widened to n = 3..7.
* 15,16 — intermediate-K frontier computed at n=3 for K=2,3,4 and plotted;
  storage-vs-margin plot added. Both figures generated from JSON, never typed.
* 19,22 — identity-vs-volume promoted; Design Implications section added (§8).

**Two results changed the paper rather than decorating it.**
H1a (identity price > 3 everywhere) is **falsified**: the worst matched-storage
price is 1.07–1.59 and the median 1.4–2.3. H1b (price grows with n) is
**falsified** too. The direction holds universally; the 5.9x case that motivated
the hypothesis is the extreme, not the rule, and §7.1 and rule R1 now say so.
E6 was mis-registered as a derivation when it is a statistical convergence claim;
it is re-graded openly, asserted only at the n where it was registered, with the
under-sampled records named.

### Still open

* 17, 18 — pipeline diagram and single summary figure.
* 20, 21 — noise and uniform-prior results promoted (partially done in text).
* 23 — the LLM-agent experiment. **Blocked on credentials and approval to spend.**
* 24, 25 — novelty audit across the seven named areas; final reference pass.
* 26 — **page budget is now the binding problem.** Body is 10 pages against a
  limit of 8. This needs a decision, not more trimming: the round-2 list adds
  roughly three pages to a paper that was already exactly at the limit.

### 2026-09-15 — item 23 closed

192 episodes, 24 per effort profile, codestral-2508 at temperature 0, 837k
prompt + 179k completion tokens, 1 failure. Written up as §7.2, audited against
`results/experiment_llm_scored.json` like every other table.

**The result:** two records holding the *same reviews*, 30 bytes of authorship
labels apart, differ by 0.943 bits of attribution error (95% CI [0.802, 1.089]).
Stable across a sixfold increase in data: 0.969 -> 0.900 -> 0.941 -> 0.943.

**Four of five predictions falsified, and the reason is ours.** gamma is a
minimum over agents, and one of our three review sub-questions ("what is now
untested?") is far harder to audit than the other two -- worst-cell TV of 0.125
against 0.958 and 0.792. That single sub-question sets gamma for every record,
so the gamma ordering measures our question set rather than compression. The
paper says this and reports attribution error instead. It is now also a stated
limitation.

**L5 confirmed after the estimator recovered.** At 4 episodes/profile gamma was
0 with 7 exact-tie cells; at 24 it is 0.075 with none. The failure condition
registered in advance did its job -- it stopped a noise ordering being reported
as a finding at the pause point.

Still open: 17, 18 (diagrams), 20, 21 (promotions), 24 (novelty audit, not
started), 25 (reference re-check), 26 (**page budget: body is now 11 pages
against a limit of 8**).
