# Regret-Grounded Evaluation of LLM Agent Teams

## Decision

**Rank: #1 for an AAMAS 2027 submission.**

Working title: **How Far Are LLM Agent Teams from Optimal? Regret-Grounded Evaluation of Decentralized Coordination**

This is a methodological multi-agent paper, not a claim that LLMs are universally poor coordinators. Its central contribution is an evaluation method that separates:

1. the loss that is intrinsically caused by decentralized, partial observations; from
2. the additional loss caused by an LLM team failing to coordinate.

That separation is directly useful to AAMAS: a Dec-POMDP is already the standard formalism for cooperative agents with local observations, while most current LLM-team evaluations only compare one prompt or architecture against another.

## One-paragraph thesis

LLM-agent teams are increasingly evaluated on tasks that have no trustworthy optimum, so a reported improvement over another agent architecture cannot say whether coordination is good in an absolute sense. Small finite-horizon Dec-POMDPs provide a controlled exception: the optimal decentralized value can be computed or obtained from verified solver results, and the fully observable centralized value can also be computed. We evaluate LLM teams against both references, decompose performance into an unavoidable **price of decentralization** and an avoidable **coordination excess loss**, and test whether explicit pre-execution joint-policy commitment closes that latter gap more efficiently than extra dialogue or test-time reasoning.

## The gap

### Precise gap statement

> No identified LLM multi-agent evaluation measures team performance against a computed decentralized optimum while separately reporting the intrinsic cost of decentralized information.

This is deliberately narrower than “LLMs have never been used with Dec-POMDPs.” Some LLM-agent papers use Dec-POMDP notation or operate in partially observable cooperative tasks. The novelty is the **optimum-grounded measurement and decomposition**, not introducing the formalism to LLM agents.

### Why it is a real gap

For a finite-horizon cooperative environment, calculate:

\[
V^*_{\mathrm{Dec}} = \max_{\pi \in \Pi_{\mathrm{decentralized}}} V(\pi),
\]

\[
V^*_{\mathrm{Cent}} = \max_{\pi \in \Pi_{\mathrm{centralized}}} V(\pi),
\]

where the first policy sees only each agent’s local history and the second sees the joint state/history. For an LLM team with value \(\widehat V_{\mathrm{LLM}}\):

\[
\text{intrinsic decentralization cost}=V^*_{\mathrm{Cent}}-V^*_{\mathrm{Dec}},
\]

\[
\text{coordination excess loss}=V^*_{\mathrm{Dec}}-\widehat V_{\mathrm{LLM}}.
\]

The first quantity belongs to the environment. The second belongs to the team. Without this distinction, a difficult coordination problem and a bad coordination protocol look identical.

## Research questions and hypotheses

| ID | Question / hypothesis | Decisive evidence |
|---|---|---|
| RQ1 | How much normalized regret do LLM teams incur relative to \(V^*_{\mathrm{Dec}}\)? | Confidence intervals over paired episodes and language renderings. |
| RQ2 | Does excess loss grow with coupling, horizon, observation noise, and team size? | A preregistered structural sweep, not selected examples. |
| H1 | Teams are closer to optimal on weakly coupled tasks than strongly coupled tasks. | Interaction between coupling strength and normalized regret. |
| H2 | Other-agent modelling, rather than world-state belief tracking, explains most excess loss. | Exact-belief probes and partner-policy prediction probes. |
| H3 | Explicit joint-policy commitment improves regret per token more than additional free-form dialogue. | Token-matched commitment versus dialogue comparison. |
| RQ3 | Can LLMs synthesize a machine-evaluable decentralized policy from prose? | Exact value of synthesized policy trees/controllers. |

## Proposed solution

### Three evaluation modes

**Mode A — Online decentralized play.** Each agent receives only its own observation history in natural language and acts episode by episode. Estimate \(\widehat V_{\mathrm{LLM}}\) from many paired rollouts.

**Mode B — Explicit policy synthesis.** The team emits a policy tree or finite-state controller in a constrained schema. Evaluate that policy exactly against the Dec-POMDP model. This removes rollout noise and makes the result comparable to classical solver policies.

**Mode C — LLM-to-solver hybrid.** An LLM parses a prose task specification into a candidate Dec-POMDP representation and initial controller; a classical solver refines it. This is optional, and belongs in the main paper only if it improves time-to-good-policy or parsing accuracy under a clean protocol.

### Candidate mechanism: joint-policy commitment

Before execution, agents negotiate a finite mapping from local observation histories to actions. During execution they follow that mapping, with narrowly specified revision triggers. The baseline receives the same token budget but spends it on free-form dialogue at action time.

The important claim is not that structure always helps. It is that an explicit decentralized policy is the object required by the formal problem, so it may resolve a coordination defect that more private reasoning cannot.

## Benchmark design

Use only instances with verified exact or high-confidence reference values. State plainly when a value is best-known rather than proven optimal.

| Family | Role in paper | Required property |
|---|---|---|
| Dec-Tiger | Tiny, strongly coupled diagnostic | Exact value and simple policy-space audit. |
| Broadcast Channel | Communication/protocol contrast | Known model and controllable communication cost. |
| Meeting on a Grid | Spatial coordination | Multiple sizes, transparent state rendering. |
| Recycling Robots | Weakly coupled contrast | Tests the predicted low-regret regime. |
| Box Pushing / Fire Fighting / Mars Rovers | Larger external-validity cases | Use only horizons with verified reference values. |
| Dec-POMDP-Com variants | Communication ablation | The value of communication must be independently computable. |

For every underlying instance, make at least five semantically equivalent natural-language renderings. Rendering is an experimental factor, not a cosmetic prompt choice.

## Baselines

### Classical references

- Random valid joint policy.
- Exact solver where tractable.
- Best verified published solver value otherwise, clearly labelled as such.
- JESP / local-search policy.
- MBDP or another scalable approximate planner.
- Centralized POMDP/MPOMDP ceiling.

### LLM references

- One centralized LLM with all observations.
- Independent decentralized LLMs without communication.
- Free-form multi-agent chat.
- Explicit belief-state prompting.
- Test-time-reasoning budget sweep.
- Joint-policy commitment.
- A non-LLM MARL policy when a fair implementation is available.

All LLM variants must use the same model version, action schema, task instances, retry policy, and total token budget where comparison is about communication.

## Metrics

\[
\text{normalized regret}=\frac{V^*_{\mathrm{Dec}}-\widehat V}{V^*_{\mathrm{Dec}}-V_{\mathrm{random}}}.
\]

Report additionally:

- centralized and decentralized reference values;
- intrinsic decentralization cost and coordination excess loss;
- exact value of Mode-B synthesized policies;
- belief-tracking error against exact filtered beliefs where feasible;
- partner-policy prediction accuracy;
- agreement/commitment fidelity;
- tokens, wall-clock time, and cost per unit regret reduction;
- parse failures separately from strategic errors.

## Falsification and decision gates

Stop or substantially narrow the project if any of the following occurs:

1. Regret is almost entirely caused by malformed actions or task parsing.
2. Variation across language renderings dominates variation across coordination conditions.
3. LLM teams are already near \(V^*_{\mathrm{Dec}}\) across both weakly and strongly coupled tasks.
4. Token-matched free-form chat matches joint-policy commitment.
5. References cannot be independently verified for the chosen horizon.

Negative findings still produce a useful evaluation result if the reference values and controls are sound.

## Prerequisite reading: understand the gap

Read these before writing or implementing the core paper.

1. **Oliehoek & Amato, _A Concise Introduction to Decentralized POMDPs_.** The model, joint-policy objects, benchmark conventions, and solver landscape. [Book page](https://link.springer.com/book/10.1007/978-3-319-28929-8)
2. **Bernstein et al. (2002), “The Complexity of Decentralized Control of Markov Decision Processes.”** Why exact optimization is difficult and why small verified instances are valuable. [DOI](https://doi.org/10.1287/moor.27.4.819.297)
3. **Dibangoye et al. (2016), FB-HSVI.** Modern optimal/approximate solution foundations. [JAIR paper](https://jair.org/index.php/jair/article/view/10995)
4. **Wu et al. (2017), decentralized planning/regret literature.** Avoid using “regret” informally; define the comparator precisely. [IJCAI proceedings](https://www.ijcai.org/Proceedings/2017/0063.pdf)
5. **The Collaboration Tax (2026).** The immediate LLM-team motivation: coordination loss is measurable but current measurement has a different oracle. [arXiv](https://arxiv.org/abs/2608.22152)
6. **LLM-Coordination (2025).** Representative modern LLM coordination benchmark and the gap between task outcomes and formal optimality. [arXiv](https://arxiv.org/abs/2310.03903)

## Novelty-defense reading list

These papers must be checked again immediately before submission. The goal is not to find citations that agree with the paper; it is to falsify the novelty claim.

| Search risk | What to inspect | Required distinction if close |
|---|---|---|
| LLMs already evaluated against Dec-POMDP optima | Search Semantic Scholar, OpenReview, arXiv: `Dec-POMDP` × (`LLM`, `language model`, `agent team`) | Must lack either computed \(V^*_{\mathrm{Dec}}\), the central ceiling, or the decomposition. |
| Classical planning evaluation already does this | Dec-POMDP solver benchmarks | These are not LLM-agent evaluations; do not overclaim novelty in the classical component. |
| LLM planning papers use exact plan validity | PlanBench; formal planning benchmarks | Plan validity is not decentralized optimality under local observations. |
| Collaboration-tax papers define a similar quantity | [Collaboration Tax](https://arxiv.org/abs/2608.22152) and successors | Their solo-versus-team loss is not the computed Dec-POMDP optimum decomposition. |
| Communication-value work is close | Dec-POMDP communication/value-of-information papers | It optimizes communication, rather than measuring LLM excess coordination loss. |

## AAMAS contribution package

1. A formal, reproducible metric suite with verified reference values.
2. An empirical structural profile of LLM coordination regret.
3. A causal mechanism test: joint-policy commitment versus extra chat at matched budget.
4. An exact policy-synthesis evaluation mode, not just sampled task scores.
5. Public instance renderings, policies, seeds, action parsers, and solver/reference verification scripts.

This is main-track material only if items 2 and 3 expose a robust, interpretable pattern. A pure benchmark table is more naturally a Findings contribution.

## Suggested eight-page outline

1. Problem and failure of relative-only evaluation.
2. Dec-POMDP optimum-grounded decomposition.
3. Evaluation suite and reference-value verification.
4. LLM-team protocols and commitment intervention.
5. Main regret/coupling results.
6. Exact synthesized-policy and error decomposition results.
7. Related work and limitations.

## Immediate pilot

Within one week, implement Dec-Tiger and Recycling Robots with two independent prose renderings, one strong model, centralized/single-agent/decentralized-chat/commitment conditions, and machine-checked action parsing. Do not proceed to a large sweep until the pilot shows nontrivial coordination excess loss that is not explained by rendering or syntax.
