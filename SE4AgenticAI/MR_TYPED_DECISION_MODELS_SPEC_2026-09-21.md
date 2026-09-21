# Metamorphic testing for typed decision models: paper spec

Date: 2026-09-21. Target: SE4AgenticAI 2026 regular paper (8-10 pp, IEEE 2-col), deadline 2026-10-10.
Companions: [gap audit](JEV_RESEARCH_GAP_AUDIT_2026-09-21.md) | [lit review](JEV_IDEA_EXPANSION_AND_LIT_REVIEW_2026-09-21.md)

## 1. The problem in one paragraph

A typed decision model (TypeSafe's Jev, and the ~20 open replicas that appeared within days of it) is a new kind of software dependency: you send state plus a typed question, and it returns a *probability distribution* over a fixed option set. Teams are already wiring these into control flow - routers, permission gates, rerankers, context pruners. But you cannot write a conventional unit test against a probability distribution. `assertEqual` does not apply, and a golden-output test fails the moment the vendor bumps a model behind a `latest` alias. The oracle problem is total.

Metamorphic testing is the standard answer to the oracle problem, and the [MT survey](https://arxiv.org/html/2605.13898v1) names the remaining open piece explicitly: **how to define stable and statistically meaningful metamorphic relations for probabilistic systems**, given that existing work relies on one-shot executions. Nobody has built an MR catalogue for a typed decision API, and the vendor's own jaggedness page already concedes that at least three relations a caller would assume are not guaranteed.

## 2. Contribution

1. **An MR catalogue for typed decision APIs** (Section 3) - nine relations, several of which exist only because this API shape has multiple primitives, an option set, and batched parallel questions.
2. **A statistical violation procedure** (Section 4) - an empirical noise floor plus a corrected test, so a violation is a claim rather than an anecdote. This is the piece the MT survey names as open.
3. **Measured violation rates** on Jev 1.13 and on 2-3 open replicas (Section 5), which makes it a comparative study of a model *class*, not a product review of one vendor.
4. **A runnable MR suite** teams can point at their own question set, plus a CI canary design for pinning a probabilistic dependency across a version bump.

## 3. The MR catalogue

Notation: state `S`, question `q`, returned distribution `p(. | S, q)` over options `O`, scalar confidence `c` (a deterministic function of `p`, per the vendor's confidence doc).

**MR0 - Idempotence.** Identical `(S, q)` submitted twice returns an identical distribution. *Establishes whether the model is deterministic at all, and defines the noise floor for every other MR. Must run first.*

**MR1 - Complement duality (Noul).** For claim `x`, `p(yes | x) + p(yes | not x) = 1`. **Pre-admitted to fail** by the jaggedness page. The contribution is the magnitude of `|p(x) + p(¬x) - 1|`, its distribution across question types, and whether confidence falls when it is violated.

**MR2 - Option permutation invariance (Choice).** Permuting the order of options and re-indexing back should leave `p` unchanged. Measure total variation distance. This tests the marketed consistency claim directly, and connects to position bias in the LLM-as-judge literature.

**MR3 - Irrelevant context invariance.** Appending semantically irrelevant text to `S` should not change `p`. Vendor concedes "context pollution." Report TV distance as a function of padding length and type - this converts a vague warning into a filtering budget an engineer can use.

**MR4 - Paraphrase invariance.** Semantically equivalent restatement of `S` or `q` yields the same `p`.

**MR5 - Score monotonicity.** For the ordered Score primitive, strengthening evidence toward a higher level must not decrease the expected score (first-order stochastic dominance). *Only expressible because Score levels are ordered - ordinary classifiers have no such relation.*

**MR6 - Cross-primitive agreement.** The same underlying judgment asked as a binary Choice over {A, B} and as a Noul "is it A?" should give `p_choice(A) ~ p_noul(yes)`. *Only expressible because the API offers several primitives over the same semantics.*

**MR7 - Partition refinement additivity.** Split option `A` into disjoint `A1, A2` spanning the same meaning. Then `p(A1) + p(A2) = p(A)`. This asks whether the output behaves like a probability measure at all. **High stakes:** the vendor caps cardinality at 255 and recommends a two-stage decomposition for larger option sets. If additivity fails, that recommended workaround is unsound.

**MR8 - Batching invariance.** The API evaluates many questions in parallel against one state in a single call. Asking `q` alone must give the same `p` as asking `q` batched with unrelated questions. **This is the highest-value relation in the catalogue.** The vendor's fan-out pattern and its advertised 12.2x cost saving depend on it, it is trivially cheap to test, and nobody has tested it. A violation means the cost-saving pattern silently changes answers.

**MR9 - Composite distributivity.** The documented composite-scoring pattern sums weighted independent dimension scores. Compare against one holistic question. One grey-literature data point already exists (0.9076 holistic vs 0.8373 decomposed), unexamined as an MR.

### The cross-cutting result
For every violated MR, ask: **does confidence drop?** If the model is incoherent while confident, then confidence-gated routing - the deployment pattern the entire product line is sold on, and the one 22 public permission gates rely on - cannot detect the incoherence. This links the testing paper to the stakes of the authorization paper without needing a security threat model.

## 4. The statistical procedure

The methodological contribution, and the reason this is a paper rather than a bug list.

1. **Noise floor.** Run MR0 `n` times per item to measure the spread of identical calls. If the model is deterministic, the floor is zero and MRs become exact; if not, the floor is the null distribution. Precedent: `scienthoon/jev-ood-calibration` established an ECE noise floor of 0.024 and compared the measured 0.107 against it.
2. **Effect size, not a boolean.** Report TV distance (or the appropriate divergence per MR) with confidence intervals, not a pass/fail count.
3. **Multiple comparisons.** Nine MRs across many items needs correction; report it.
4. **Pre-register** the relations and the violation threshold before collecting. `priorbench` set this precedent publicly, and a reviewer who finds the grey literature will find that repo too.

## 5. Experimental design

**Subjects.** Jev 1.13 (pinned, via Vercel AI Gateway `typesafe-ai/jev`, confirmed live 2026-09-21) plus 2-3 open replicas from the community corpus (Laya, NanoJev, von, LitJev are candidates - local, free, no key). The replicas do three jobs at once: they kill the "single-vendor product review" objection, they make the catalogue's generality demonstrable, and they de-risk API access entirely.

**Items.** A question corpus spanning the three primitives and a spread of difficulty, with the MR transformations generated programmatically rather than by hand. Programmatic mutation is what lets the item count be large and the construction auditable - the same move TraceSafe used.

**Budget.** Single-digit dollars. The comparable OOD study cost $0.06.

**Artifact.** Raw JSONL of every call, the MR suite, the recount script, exact model ids, dates, and gateway used.

## 6. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Gateway flattens the response and drops `probabilities` | Verify on day 1. Every MR except MR0 needs the distribution. If lost, fall back to the waitlist or run the catalogue on open replicas only. |
| Model is deterministic and all MRs pass cleanly | Unlikely given the pre-admitted violations, but if so the paper becomes "these relations hold, here is the suite and the floor" - a weaker but still publishable negative result with a usable artifact. |
| Reviewer says "this is just API testing" | The framing must be the *methodology for a class of dependency*, instantiated on the first available instance plus replicas. The multi-subject design is what makes this credible. |
| MR7/MR8 require careful semantic construction of option splits and distractor questions | Pilot these two first; they are the highest-value and the most fragile. |

## 7. Why this over the authorization paper

Fewer moving parts, no security reviewer needed, no dependency on obtaining TraceSafe, single-digit cost, degrades cleanly to a short paper, and it is completely untouched by the 232-project grey corpus. The authorization paper is the better story; this one is the better bet.
