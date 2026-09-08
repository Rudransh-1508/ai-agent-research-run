# Causal Source Attribution of Multi-Agent Non-Stationarity

**Status:** Recommended research gap for AAMAS 2027. Selected after two independent large-scale literature audits and a from-scratch mathematical kill test, following the rejection of five prior candidates over a multi-day investigation.

**Prepared:** 9 September 2026
**Target venue:** AAMAS 2027 main track (LEARN area), fallback Blue Sky Ideas track
**Key deadlines:** OpenReview author registration 17 Sep 2026 · Abstract 1 Oct 2026 · Paper 8 Oct 2026 (all AoE)

---

## Part 0 — Executive Summary

### The gap, in one sentence

> When a teammate's behavior changes, and the passively observed evidence looks identical no matter *why* it changed, can an agent choose costly, strategically-visible interventions that tell apart three causally distinct explanations — the environment shifted, the teammate is learning on its own, or the teammate is reacting to *you* — and does knowing the answer actually change what it should do next?

No searched work — across two independent audits covering roughly 90 substantively-inspected primary papers between them — combines all four of: (1) three passively-matched causal sources, (2) restricted, costly, strategically-visible interventions, (3) formal partial identifiability under that restriction, and (4) evidence that the resulting diagnosis changes optimal multi-agent control. Every individual ingredient (change detection, opponent modelling, active probing, opponent shaping, causal games) is mature and well-published. The conjunction is not.

### Why this is the recommendation, not just a candidate

This document is the end product of a search that killed five prior candidates on their own evidence, then found this one by two different processes that never spoke to each other:

1. An 8-role internal literature audit (`research_run_2026-09-08/`) independently ranked this idea #1 out of 42 candidates (score 8.80/10), the same day this session was also independently pursuing an unrelated LLM-substrate candidate.
2. A separate, harder 15-role audit (`AAMAS_2027_TWO_CANDIDATE_RESEARCH_AUDIT.md`) pitted this idea head-to-head against the strongest surviving candidate from this session's own work and ranked it decisively ahead — 8.3/10 vs 5.1/10, with 82% stated confidence.
3. This document's own from-scratch mathematical construction (Part II) verifies the audits' own prescribed kill test *passes* on the cheap gates, and — going further than either audit did — locates exactly where the real risk lives: not in whether interventions have value (they clearly do), but in whether *explicit source-structured* reasoning beats an *equally-informed flexible controller*. That distinction only shows up under transfer to a new task, which is precisely what the audits' own next experimental stage is designed to test.

### Recommended immediate action

Do not start with implementation. Run **Gate A0** (does the source label carry any control value beyond a source-agnostic predictive controller?) and **Gate A1** (can every control-distinct source pair be separated by a legal intervention?) on the smallest possible exact game, per Part II below — this document already runs a first version of that gate and it passes, but the real-stakes version (a flexible Bayes-adaptive baseline, not a hand-built flat controller) still needs to be run before committing further time. If either gate fails on the honest baseline, stop. The whole point of this staged approach is that failure here is cheap; failure after weeks of JaxAHT integration is not.

---

## Part I — The Research Gap

### 1.1 Precise gap statement

> No identified work jointly (i) constructs exogenous-regime-drift, autonomous-peer-learning, and ego-responsive-peer-adaptation processes that produce the *same* passive local-history law, (ii) characterizes their equivalence classes under a restricted, costly, strategically-visible family of interventions, and (iii) demonstrates that identifying the resulting **control-relevant equivalence class** improves multi-agent control over the strongest source-agnostic predictive/adaptive baseline.

This is deliberately narrower than "multi-agent non-stationarity is unstudied" — that claim is false and would be rejected immediately. The novelty is the **conjunction**: passive observational equivalence + restricted intervention + formal identifiability + demonstrated control value, applied to a **reflexive** problem where the diagnostic action can itself change the very peer being diagnosed.

### 1.2 Why the reflexivity is the load-bearing, MAS-native property

A change-point detector tells you *that* behavior changed, not *why*. An opponent model predicts a peer's future behavior without asking whether that behavior is a strategic response to the observer's own past actions. Opponent-shaping methods (LOLA, M-FOS, Meta-MAPG) assume responsiveness and exploit it, without first testing whether the assumption holds. Robust control does the opposite — hedges against the peer being anything at all — which can leave value on the table when the peer would in fact respond productively to shaping.

Choosing the wrong response to the wrong diagnosis has a real cost: tracking a genuinely responsive peer wastes an opportunity to shape it profitably; attempting to shape a peer that is in fact autonomously and independently adapting can manipulate it needlessly, destabilize a working convention, or simply fail. **The three sources are not interchangeable, and the whole research question collapses to ordinary single-agent latent-mode system identification unless the diagnostic action can itself alter the object being diagnosed** — a peer that reacts to being probed is not the same problem as a hidden Markov state that does not know it is being observed. That reflexivity is the reason this is a multi-agent systems contribution and not a control-theory exercise wearing MAS vocabulary.

### 1.3 Multi-agent necessity — the purity test

Both audits converge on the same three-part test, and this document adopts it as the standing bar the project must clear before any paper is written:

1. The ego's policy is a structural parent of the peer's update in the *responsive* source, but not in the *autonomous* source.
2. The peer can react to, mask, delay, or strategically exploit a diagnostic intervention.
3. Correct attribution selects a different future interaction policy and improves team value, safety, or regret relative to getting the attribution wrong.

**Substitution test:** replace the peer with a passive stochastic kernel that produces the same marginal behavior. If nothing about the problem breaks, the "multi-agent" framing is decorative and the paper is single-agent system identification with agent-themed labels. This is not a rhetorical device — it is the first thing a reviewer will try, and the project should try it on itself first.

---

## Part II — Kill Test: Construction and Results

The following is a self-contained mathematical construction, built and computed directly (not drawn from either source audit, though it follows their prescribed method) to test whether a construction satisfying the gap's own requirements is even possible, and where its value concentrates.

### 2.1 The construction

Two agents: ego `i`, peer `j`. Ego observes a fused signal `y = x ∨ θ`, where `x` is a physical/environment bit and `θ` is the peer's parameter — the ego cannot see `x` and `θ` separately without paying for a sensor.

Three deterministic latent sources, drawn with a uniform prior:

| Source | Mechanism | Interpretation |
|---|---|---|
| **E** | `x = 1`, `θ = 0`, both fixed | Environment-driven; unaffected by the ego |
| **L** | `x = 0`, `θ = 1`, both fixed | Peer's own independent state; unaffected by the ego |
| **R** | `x = 0`, `θ = a₁` (the ego's round-1 action) | The only source where the peer reacts to the ego |

**Round 0 (passive, default action `a₀ = 1`):** `y₀ = 1` under all three sources — confirmed by direct computation. **Passive equivalence holds by construction**, exactly as the gap statement requires: an ego that never intervenes cannot tell the sources apart no matter how long it watches.

**Round 1 (ego chooses a probe `a₁ ∈ {0,1}`):** playing `a₁ = 0` yields `y₁ = 0` only under R (the peer instantaneously reacts) and `y₁ = 1` under both E and L. This one legal, cheap intervention separates **R from {E, L}** but not E from L.

**Optional costly sensor:** directly reveals `x`. `x = 1` only under E. This separates **E from {L, R}** but not L from R.

**Neither channel alone achieves full identification. Combined, they do** — this is exactly the kind of result Gate A1 asks for: a real, non-trivial separability matrix, not an assumption that identification is possible.

### 2.2 Gate A1 — legal separability — verified numerically

```
Action-probe (a1=0) signature y1: {'E': 1, 'L': 1, 'R': 0}
Sensor signature x:               {'E': 1, 'L': 0, 'R': 0}

Pairwise separability matrix:
  E vs L: probe-only=False  sensor-only=True   combined=True
  E vs R: probe-only=True   sensor-only=True   combined=True
  L vs R: probe-only=True   sensor-only=False  combined=True

Full 3-way identification achievable with {probe, sensor} combined? True
```

**Result: PASS.** Every source pair is separable using the combined intervention family; no pair requires an unrealistic privileged sensor or a reset.

### 2.3 Gate A0 — does the label carry control value? — verified numerically

Reward structure: a ternary payoff round with source-conditional optimal actions `target(E)=1, target(L)=2, target(R)=0` (chosen so all three sources genuinely require different responses — with a binary action space at most two of three sources could ever be distinguished by their optimal response, which would understate the test).

```
J(full source-model oracle)                     = 1.000  (always correct)
J(true source label)                            = 1.000
J(predictive controller, probe only, no sensor) = 0.333
J(no intervention at all, blind guess)          = -0.333

G_label (true label vs probe-only predictive) = 0.667
G_model (full model vs probe-only predictive) = 0.667
G_label / G_model ratio = 1.000   (stop threshold: < 0.05)
```

**Result: PASS, decisively.** Source information is worth 0.667 units of expected reward over a predictive controller that has only the cheap channel — nowhere near the audits' 5% stop threshold.

### 2.4 The sharper test the audits flag as the real risk — and where it actually breaks

Both audits name the same "fatal concern": *high source-classification accuracy is publishably irrelevant if a source-agnostic controller with access to the same evidence reaches the same return.* This document tested that directly rather than assuming the easy gates settle it.

**On a single fixed task, a flat controller — same raw evidence (probe outcome, sensor reading), no explicit notion of "source" at all, just memorizing evidence→action — scores identically to the source-labeled controller: 1.0 vs 1.0.** This is not a near-miss; it is exact. **In this construction, explicit source labels add zero value over a flexible controller with equal information, on a fixed task.** This confirms the audits' fatal concern is real, not hypothetical — and any submission built on this idea must not claim otherwise.

**Under transfer — the same causal mechanism, a new reward mapping — the two diverge sharply:**

```
[Task 2] J(flat controller, FROZEN from Task 1, no retraining)        = -0.333
[Task 2] J(source-structured controller, given Task 2's reward rule)  =  1.000
```

A flat controller trained on task 1's evidence→action associations transfers *worse than blind guessing* to a new task with the same mechanism but different payoffs, because it confidently applies stale, task-specific associations. A controller that explicitly infers the *source* — "this peer is responsive" — and re-derives the correct action from the new task's reward rule recovers full performance immediately, with no retraining.

### 2.5 What this means for the project, precisely

The value of this whole research direction does **not** live in "labeled beats unlabeled on one task" — that claim is false in this construction and would be an easy reviewer kill. It lives specifically in **transfer across held-out mechanisms and reward structures**, which is exactly why both audits' proposed Stage 2 experiment is JaxAHT with *held-out update rules*, not more single-task tuning. This document's toy independently arrives at the same experimental design requirement from first principles, which is a meaningfully stronger form of validation than either audit alone provides.

**The gates that can be checked cheaply (A0, A1) pass. The gate that actually decides the project (does structured attribution beat an equally-informed, equally-adaptive Bayes-optimal controller under transfer — not a hand-built flat controller, but a real Bayes-adaptive baseline that can in principle learn an implicit sufficient statistic equivalent to a source posterior) has not yet been run and is the true next step, not implementation.**

---

## Part III — Formal Problem Statement

### 3.1 Source-factored POSG / SCM

For ego `i`, peer `j`, physical state `x_t`, environment regime `e_t`, peer learning state `θ_t`, joint actions `a_t = (a_t^i, a_t^j)`, local history `h_t^i`:

```
a_t^j ~ π^j_θt(· | h_t^j),        x_{t+1} ~ P_et(· | x_t, a_t)
```

Latent source `S ∈ {E, L, R}`:

```
S=E:  e_{t+1} = F_E(e_t, x_t, a_t, ξ_t),                    θ_{t+1} = θ_t
S=L:  e_{t+1} = e_t,                                        θ_{t+1} = F_L(θ_t, z_t, η_t)
S=R:  e_{t+1} = e_t,                                        θ_{t+1} = F_R(θ_t, h_t^j, a^i_{0:t}, m^i_{0:t}, η_t)
```

`z_t` must be an exogenous learning stream *invariant to the diagnostic treatment* — without that restriction, "independent" learning could still be secretly caused by ego-mediated rewards, and the source labels become ill-defined. This restriction is a genuine modeling commitment that must be stated and defended explicitly in any write-up, not glossed over.

### 3.2 Passive impossibility

If under behavior policy `π⁰`, `P_E^π⁰(H_T^i) = P_L^π⁰(H_T^i) = P_R^π⁰(H_T^i)`, no passive classifier can beat the largest source prior — under a uniform prior, Bayes error is at least 2/3. This is a direct finite-hypothesis consequence, not by itself a novel theorem; the novelty is in what comes next.

### 3.3 Restricted interventional equivalence

For permitted diagnostic-policy family `Γ(𝒰)`, sources `s, s'` are equivalent if `P_s^γ(H_T^i) = P_{s'}^γ(H_T^i)` for all `γ ∈ Γ(𝒰)`. With finite known source models and resettable trials, consistent identification requires (and, under standard repeated-excitation conditions, is enabled by) a separating permitted policy for every source pair. **In a non-resetting game, a first probe may permanently alter the peer, so the practical problem is Bayes-adaptive control, not i.i.d. hypothesis testing** — this is the single most important modeling subtlety and is the reason a naive "just probe and classify" design will not work in a real deployment.

### 3.4 Control relevance

Two sources are **decision-equivalent** if every permitted future ego policy induces the same distribution of future ego observations and rewards. Revealing a semantic label has zero value within such a class — this is exactly what Part II §2.4 demonstrated concretely. The true target of the research is therefore the **coarsest control-sufficient source partition**, not necessarily the full E/L/R taxonomy; a paper that forces a three-way split where only a coarser two-way split is control-relevant will be — correctly — read as decorative.

Objective:

```
V_t(b) = max_u∈𝒰  E_b[ r_t − λc(u) + γV_{t+1}(b_{t+1}) ]
```

evaluated on: source-oracle dynamic regret, explicit probe cost, posterior calibration, peer displacement caused by probing, joint return, and adaptation delay.

---

## Part IV — Research Questions and Hypotheses

| ID | Question / hypothesis | Decisive evidence |
|---|---|---|
| RQ1 | Under what conditions can a decentralized agent distinguish exogenous drift, autonomous peer learning, and ego-caused peer adaptation from local histories plus bounded interventions? | Formal identifiability result (Part III.3) plus the empirical separability matrix (Part II.2.2). |
| H1 | For passively observationally-matched process pairs, a source-aware policy using a fixed intervention budget reduces dynamic regret and harmful shaping relative to change-point, opponent-modeling, and shaping baselines. | Held-out mechanism comparison against BOCPD, LeMOL/MBOM, Fast Peer Adaptation, robust control, always-shape. |
| H1-falsify | Permuting the inferred source label removes the advantage. | Label-permutation ablation — mandatory, not optional. |
| H2 (the real test, per Part II.5) | Source-structured control transfers across held-out reward mappings and update mechanisms better than an equally-informed flexible/Bayes-adaptive controller without explicit source structure. | JaxAHT Overcooked-style transfer with held-out peer-update rules, per Stage 2 below. **This is the actual go/no-go for the project**, not H1. |
| RQ2 | Does source factorization improve out-of-family transfer even when in-family return matches an anonymous latent controller? | Direct comparison, matched capacity, held-out mechanism families. |

---

## Part V — Experimental Design

### Stage 0 — oracle-value gate (≈1 day, CPU only)

In an exact toy game (the construction in Part II is a first pass at this; a slightly richer version with a genuine Bayes-adaptive baseline should replace the hand-built flat controller), compute: (1) the strongest source-agnostic predictive latent controller, (2) the same-capacity controller given the true source label, (3) the oracle with the full source-generating model. **Stop if the upper 95% confidence bound on true-label gain is below 5% of the oracle-model gap.** Part II already ran a version of this and it passed at ratio 1.0 — but with a deliberately weak "no-sensor predictive" baseline, not a real Bayes-adaptive one. Re-running with a proper baseline is the immediate next step, not implementation.

### Stage 1 — certified diagnostic game (3–5 days)

- **Agents:** two — ego and learning peer.
- **Passive phase:** fixed behavior policy; source parameters constructed so held-out passive trajectory laws are indistinguishable.
- **Interventions:** ego action probe; optional costly state sensor/task reassignment; later, a communication signal.
- **Baselines (mandatory):** chance/source prior, BOCPD, passive Bayes, recurrent predictor, anonymous expected-information-gain, Bayes-adaptive controller, always-track, always-shape, oracle.
- **Metrics:** pairwise source/equivalence-class accuracy, Brier/log loss, probe count/cost, return/regret, time-to-adaptation, peer displacement.
- **Predeclared thresholds:** passive accuracy ≈ chance (0.31–0.36 for balanced three-way trials); active accuracy ≥ 0.80 within two probes; ≥ 10% regret reduction over the strongest source-agnostic baseline. These are project gates, chosen before seeing results, not community standards to be argued about post hoc.

### Stage 2 — external validity (the decisive stage, per Part II.5)

Use [JaxAHT](https://github.com/uoe-agents/jax-aht) Overcooked-style ad hoc teamwork rather than building a new benchmark. Instantiate a small set of transparent teammate update rules and environment changes, hold out update mechanisms (not just seeds or hyperparameters), and test whether source-structured control transfers where a flexible baseline does not. **Do not begin with Melting Pot or a large LLM environment — they obscure the identifiability question this project is actually about.**

### Decisive ablations (mandatory, not optional)

- Remove the source posterior but retain predictive latent state.
- Remove predictive state but retain source posterior.
- Permute semantic source labels.
- Replace source prediction with a random auxiliary task.
- Remove each intervention channel independently.
- Vary peer learning rate, delay, strategic masking, probe visibility.
- Mixed sources and common-cause changes.
- Matched vs. deliberately unmatched passive histories.
- Source-factorized vs. equal-capacity anonymous latent model.

### Compute

- Exact chamber: CPU only, hours to a few days including sweeps.
- JaxAHT experiments: one modern GPU or high-core CPU, approximately 2–7 days for controlled runs if existing policies/checkpoints are reused.
- **No frontier LLM API is required for this project.** This is a genuinely different resource profile from every LLM-substrate candidate this investigation considered earlier.

---

## Part VI — Nearest Prior Work

| # | Paper | What it establishes | Exact residual difference | Threat level |
|---|---|---|---|---|
| 1 | [Wang et al., Causal-Context-aware Teammate Modeling with Risk-Constrained Online Planning (2026)](https://www.sciencedirect.com/science/article/pii/S0950705125022786) | Temporal causal representations disentangle external confounders from intrinsic teammate strategy for AHT, combined with online planning. | No explicit three-source interventional identification under matched passive laws; does not ask whether a teammate *would have changed* under a counterfactual ego policy. | **CRITICAL** — the closest single paper found across both audits |
| 2 | [Ma et al., Fast Peer Adaptation with Context-aware Exploration (ICML 2024)](https://proceedings.mlr.press/v235/ma24n.html) | Active exploration rapidly infers peer context/type. | Probes peer type, not the causal origin of a policy *change*. | **CRITICAL** |
| 3 | [Carmel & Markovitch (1999)](https://doi.org/10.1023/A:1010007108196) | Reward-bearing actions trade off against opponent-model information — classical active opponent diagnosis. | No source-factorized endogenous-change treatment. | **HIGH** |
| 4 | [Selamet & Tümer, MARL-CD (2022)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4123080) | Detects environment-dynamics vs. agent-policy changes. | Does not distinguish autonomous peer learning from ego-induced response under passive equivalence. | **HIGH** |
| 5 | [Foerster et al., LOLA (AAMAS 2018)](https://arxiv.org/html/1709.04326); [Lu et al., M-FOS (ICML 2022)](https://proceedings.mlr.press/v162/lu22d.html) | Account for and exploit the ego's effect on an opponent's update. | Assume responsiveness and exploit it; do not diagnose *whether* an observed change was actually ego-caused before acting on that assumption. | **HIGH** |
| 6 | [Papoudakis et al., LeMOL (2020)](https://arxiv.org/abs/2006.03923); [Yu et al., MBOM (2021)](https://arxiv.org/abs/2108.01843) | Model an opponent's learning dynamics predictively. | Predictive models, not source attribution or intervention design — mandatory baselines, not competitors to be merely cited. | **MEDIUM-HIGH** |
| 7 | [Mishra, Fox & Wooldridge, Characterising Interventions in Causal Games (2024)](https://arxiv.org/html/2406.09318); [Triantafyllou et al., Agent-Specific Effects (ICML 2024)](https://proceedings.mlr.press/v235/triantafyllou24a.html) | Formal intervention primitives and strategic-response propagation in causal games. | Intervention semantics and effect propagation, not online hidden-source discrimination from restricted, costly interventions. | **HIGH / MEDIUM-HIGH** |

**Reviewer's most likely opening objection, verbatim from both audits:** *"This is dual control / active opponent modelling with anthropomorphic labels."* The mandatory response is a strategic peer whose update genuinely depends on and reacts to the intervention, plus the non-agent substitution test from Part I.3 — if that substitution destroys nothing, the objection is correct and the project should be narrowed or killed.

### 6.1 Narrower formulations already killed — do not re-propose these

`AAMAS_2027_TWO_CANDIDATE_RESEARCH_AUDIT.md` ran a component-level kill pass on the broad idea before settling on the narrow formulation used throughout this document. Each of these was tried and explicitly rejected — they are recorded here so the project does not accidentally drift back into one of them mid-write-up:

| Narrower formulation | Verdict | Killed by |
|---|---|---|
| Generic multi-agent non-stationarity detection | **ALREADY DONE** | Large MARL literature; MARL-CD directly addresses switches |
| Causal teammate representation disentangling environment and strategy | **ALREADY DONE / occupied** | CCTM (Wang et al. 2026) is a direct recent collision |
| Active teammate probing | **ALREADY DONE** | Classical active opponent modelling, team probing, Fast Peer Adaptation |
| Infer whether an opponent is learning | **PARTIALLY ADDRESSED** | LeMOL and model-based opponent models already model learning/adaptation |
| Account for our influence on another learner | **ALREADY DONE as a primitive** | LOLA, Meta-MAPG, M-FOS, stable-influence work |
| Use information gain alone to choose diagnostic actions | **INCREMENTAL** | Standard experimental design / dual control; not MAS novelty by itself |
| Three-way source classification without a downstream control result | **REJECTED** | Labels may be explanatory decoration; no full-paper contribution without control value — this is exactly what Part II §2.4 tests and finds is a live risk |
| Ego-action-only identification of all three sources | **FORMALLY FALSE in general** | The minimal example in Part II separates R from {E, L} but cannot separate E from L on the action channel alone — a second channel (the sensor) is required |

The last row is a useful sanity check on this document's own construction: Part II's toy is not a lucky accident where one channel happens to solve everything — it needed exactly the two channels the audit's own analysis says are necessary, no fewer.

---

## Part VII — Falsification Gates

Kill or radically narrow the project if any of the following occurs:

1. Passive prediction already separates the worlds — the intended observational-equivalence construction is invalid.
2. Permitted interventions fail to separate a source pair that genuinely requires different control responses.
3. Anonymous expected-information-gain or Fast Peer Adaptation-style exploration matches source-aware diagnosis at equal cost.
4. True labels add less than 5% of the oracle-model value gap (Gate A0).
5. All source-conditioned optimal policies agree on more than 95% of reachable beliefs (the sources are control-equivalent after all).
6. Posterior removal or label permutation does not measurably affect behavior.
7. Gains disappear outside one hand-built SCM and do not survive transfer to held-out mechanisms (Part II.5 — **this is the single most likely failure mode identified in this document's own analysis**).
8. A paper is found that already performs matched-passive E/L/R interventional attribution with source-contingent control — this should be re-checked in the week before submission, since both audits explicitly note their searches cannot certify global absence.

---

## Part VIII — Risks, Ranked

1. **The real go/no-go has not been run yet.** Part II shows the cheap gates pass with a hand-built flat baseline; it does not yet show source-structured control beats a genuine Bayes-adaptive baseline under transfer. This is the highest-priority open item, not a hypothetical future concern.
2. **CCTM (Wang et al. 2026) is the closest published work and must be directly compared against, not merely cited.** The paper's novelty defense must be precise: passive-equivalent E/L/R source models, restricted identifying interventions, and control-sufficient equivalence classes — not "causal separation of environment and teammate factors," which CCTM already does.
3. **The label may have zero decision value beyond a strong predictive controller in the real (non-toy) setting.** Part II.4 demonstrates this is a real, not hypothetical, risk — it happened in the toy on a fixed task. The paper's actual defense must live entirely in the transfer result.
4. **Simulator/label leakage.** Must hold out update mechanisms and rates, not just random seeds, and permute source labels as a standing ablation.
5. **The intervention changes the teammate, which could be read as invalidating the diagnosis rather than being the point.** This must be framed explicitly as the MAS-native feature being studied, with peer-displacement modeled and measured directly, not treated as noise to be minimized away.
6. **Reviewer risk is rated lower than the alternative candidate this investigation considered** (6.5/10 vs. 9.5/10 in the two-candidate audit's own scoring), but is not zero — "renamed dual control" is a live and anticipated objection with a prepared but unproven response.

### 8.1 Full scored comparison against the strongest alternative

`AAMAS_2027_TWO_CANDIDATE_RESEARCH_AUDIT.md` scored this direction (its "Candidate A") against the strongest surviving alternative from this session's own work (spec 04, its "Candidate B") across 14 criteria. Reproduced in full because the per-row breakdown is more informative than the single overall number quoted elsewhere in this document:

| Criterion | This direction | Spec 04 (compaction/attrition) |
|---|---:|---:|
| Novelty | 7.0/10 | 3.5/10 |
| Scientific importance | 8.5/10 | 6.5/10 |
| AAMAS relevance | 9.0/10 | 5.0/10 |
| Multi-agent centrality | 9.0/10 | 4.5/10 |
| Technical depth | 9.0/10 | 6.0/10 |
| Theory potential | 9.0/10 | 3.5/10 |
| Experimental feasibility | 8.5/10 | 6.5/10 |
| Compute efficiency | 9.5/10 | 4.5/10 |
| Baseline availability | 8.5/10 | 8.0/10 |
| Falsifiability | 9.5/10 | 9.0/10 |
| Reproducibility | 9.0/10 | 6.5/10 |
| Risk of prior art (10 = worse) | 6.5/10 | 9.5/10 |
| Reviewer risk (10 = worse) | 6.5/10 | 9.0/10 |
| **Overall** | **8.3/10** | **5.1/10** |

The widest gaps are theory potential (9.0 vs 3.5), multi-agent centrality (9.0 vs 4.5), and risk of prior art (6.5 vs 9.5, lower is better) — consistent with the structural lesson in Appendix A.6: spec 04's components were individually well-published by mid-2026, while this direction's specific conjunction was not found anywhere in either audit's search.

---

## Part IX — AAMAS Contribution Package

1. A source-factored POSG/SCM formalization of endogenous multi-agent non-stationarity, with a proved passive-observation impossibility result.
2. A restricted-intervention identifiability characterization — the coarsest control-sufficient source partition, with an explicit minimal-channel construction (Part II is a working instance of exactly this).
3. A cost- and safety-aware belief-space active-diagnosis algorithm that conditions the control mode (track / hedge / shape) on posterior uncertainty.
4. Empirical validation in an exact chamber plus transfer to a public ad-hoc-teamwork environment (JaxAHT) with held-out peer-update mechanisms — the transfer result is the paper's actual central claim, not a secondary robustness check.

**Primary area: LEARN.** Use a Representation and Reasoning framing only if the formal results, not the empirical system, end up dominating the finished paper.

---

## Part X — Venue and Timeline

| Milestone | Date | Note |
|---|---|---|
| OpenReview author registration | **17 Sep 2026** | Hard gate, independent of everything else — do this regardless of how the pilot goes. |
| Abstract submission | **1 Oct 2026 AoE** | |
| Full paper submission | **8 Oct 2026 AoE** | |
| Rebuttal | 20–24 Nov 2026 | |
| Notification | 21 Dec 2026 | |
| Camera-ready | 25 Jan 2027 | |
| Conference | 3–7 May 2027 | |

Main track: 8 pages + unlimited references, LaTeX template, double-blind. Papers not selected for the main proceedings are automatically considered for Findings of AAMAS 2027 unless authors opt out, same length and format.

**Fallback: AAMAS 2027 Blue Sky Ideas track** — 4 pages, explicitly does not require experimental results, abstract 5 Nov / paper 12 Nov 2026. Given the project's real risk concentrates in one experiment (the JaxAHT transfer result), a Blue Sky framing — stating the identifiability problem, the toy construction and its result from Part II, and the research program, without claiming the transfer result is yet in hand — is a legitimate and honest fallback if the 3-week main-track window proves too tight for a defensible transfer experiment.

### Suggested 3-week schedule if pursuing main track

- **Week 1:** Freeze source definitions and intervention permissions. Implement exact E/L/R kernels (extending Part II). Re-run Gate A0 with a genuine Bayes-adaptive baseline, not a hand-built flat controller. Produce the legal separability matrix for the real chamber. **Stop condition: either core gate fails on the honest baseline.**
- **Week 2:** Implement mandatory baselines (BOCPD, recurrent predictive controller, anonymous EIG, source-factored belief controller). Predeclare episode counts, confidence intervals, thresholds. Run label-permutation and posterior-removal ablations.
- **Week 3:** Sweep peer update delays/rates, probe visibility, strategic masking, mixed sources. Hold out update *mechanisms*, not just parameters. Port one minimal change family to JaxAHT if chamber gates survive. Produce a go/no-go memo — not a polished paper draft — as the week's actual deliverable.

**Pilot success is not "the method beats chance."** It is: the source distinction has oracle control value on an honest baseline; legal probes separate the needed classes; the factorized controller beats strong anonymous prediction/exploration; and — the part this document's own analysis flags as most likely to fail — results survive transfer to held-out mechanisms.

---

## Appendix A — Investigation History: What Was Tried and Rejected

This project reached its current recommendation only after five prior candidates were built out, adversarially checked against both modern and classical literature, and rejected or retracted on their own evidence. This history is preserved because (a) it demonstrates the recommendation survived a genuinely adversarial process rather than being the first idea considered, and (b) several of the rejected directions independently corroborate parts of this recommendation's own risk analysis.

### A.1 Spec 01 — Regret-grounded evaluation of LLM agent teams against a computed Dec-POMDP optimum (`research_specs/01_regret_grounded_llm_teams.md`)

**Retracted.** The core measurement idea — decomposing LLM-team shortfall into an intrinsic "price of decentralization" (centralized optimum minus decentralized optimum) and an "excess coordination loss" (decentralized optimum minus achieved value) — is not new. Goldman & Zilberstein (JAIR 2004) already name this exact gap the **"value of communication,"** and Pynadath & Tambe (JAIR 2002, COM-MTDP) formalize the identical comparison, built explicitly on Marschak & Radner's 1962/1972 team decision theory. A narrower synthesis-method framing (LLM-emitted, solver-verified decentralized policy controllers) survived partially but was eroded by RADIANT (arXiv:2607.16708) and POMDP Coder/Pinductor (arXiv:2505.02216), leaving only thin, derivative slivers. See `research_specs/01_novelty_review.md`, `01_classical_exposure_check.md`, `01_evaluation_practice_check.md`, `01_synthesis_check.md`, `01_scoop_check.md`.

### A.2 Spec 02 — STAV: Stability-Constrained Adaptive Verification (`research_specs/02_stav_adaptive_verification.md`)

**Rank #2, not fully explored, deprioritized in favor of the current recommendation.** Proposed measuring LLM costly-verification behavior as a fitted trust-update law, using it in a delayed error-propagation model, and constraining an adaptive verifier with a robust stability certificate. Never independently killed in this investigation, but superseded once the causal-source-attribution direction was found and validated by two independent audits.

### A.3 Spec 03 — Sanctioning under unreliable blame (`research_specs/03_sanctioning_under_unreliable_blame.md`)

**Retracted.** Proposed defining the attribution-accuracy threshold below which reputation-based sanctioning becomes net-harmful. Killed by Grechenig, Nicklisch & Thöni (2010, *Journal of Empirical Legal Studies*), who swept signal accuracy directly and found welfare under noisy punishment equal to no-punishment at ~90% accuracy and *below* no-punishment at 50% — replicated by Ambrus & Greiner (*AER* 2012). Closed-form error-rate thresholds for reputation norms also independently exist in Glynatsi, Hilbe & Murase (*PLoS Comp Bio* 2025). See `research_specs/03_novelty_review.md`.

### A.4 Spec 04 — Compaction and architecture effects on peer-commitment attrition (`research_specs/04_factual_attrition_mechanism.md`)

**Superseded, substantially weakened on final review.** Originally proposed disentangling "attentional loss" from "motivated suppression" in multi-agent LLM deliberation via a recall probe; that half was cut after being identified as Tulving & Pearlstone's (1966) free-recall-vs-cued-recall paradigm applied to LLMs, plus a venue-fit problem (single-agent-shaped, not multi-agent-necessary). The restructured residual (compaction hitting peer-established commitments; architecture shaping attrition *shape*) was then independently and more severely weakened by `AAMAS_2027_TWO_CANDIDATE_RESEARCH_AUDIT.md` (Candidate B in that document), which found: the anchor paper (Deliberative Illusion, arXiv:2606.03032) already varies communication topology and reports different attrition by topology; MemUse (arXiv:2608.24189) already does recall-vs-spontaneous-use dissociation directly for LLMs; and MafiaScope (arXiv:2607.10645) already built the fork-context/frozen-replay probe methodology this candidate relied on, while also showing single-probe reliability is itself noisy (34.8% inconsistency on re-asking). Final scored comparison against the causal-source-attribution candidate: 5.1/10 vs 8.3/10. See `research_specs/04_classical_check.md`, `04_scoop_check.md`, `04_venue_fit_check.md`.

### A.5 Killed candidates from the LLM-substrate hunt (`research_specs/hunt_A/B/C_*.md`, `candidate_*_check.md`)

A separate multi-agent search deliberately targeted phenomena specific to transformer substrates (attention mechanics, trained-bias cascades, in-context peer imitation) to avoid the "classical concept import" failure mode. All headline candidates in this line were killed or narrowed to fragile residuals:

- **Acceptance-gate manipulation-resistance** for self-evolving agent harnesses — closed by PACE (arXiv:2606.08106), which already frames the problem as "a textbook case of adaptive data analysis," plus Hardt et al.'s (2016) strategic-classification NP-hardness result.
- **The shared experience pool as a strategic commons** — closed by Ghosh & McAfee (WWW 2011), whose equilibrium prediction ("a flood of low-quality contributions") is the exact claim, word for word, fifteen years earlier; also independently pre-empted on the LLM side by EquiMem (arXiv:2605.09278).
- **Verifier panels vs. a strategic persuader** — closed by Kaniovski (2008), whose Corollary 1.4 proves panel-competence non-monotonicity from correlation alone, and Feddersen & Pesendorfer (*APSR* 1998).
- **Self-preference bias as an iterated collaborator-selection pressure** — real and unclaimed, but exposed to a Becker (1973) assortative-matching re-derivation risk; not pursued further once the causal-attribution direction was validated.
- **Orthogonal contagion of style vs. correctness in peer imitation** — survives narrowly but reads as an incremental factorial cross of already-published single-axis results (Contagion Networks, arXiv:2606.20493; BOUNDARY_SYNC, arXiv:2607.01600).

### A.6a Full ranking across everything this investigation produced

| Rank | Candidate | Status | Why |
|---|---|---|---|
| **1** | **Causal source attribution of non-stationarity (this document)** | **Recommended, gates partially cleared** | Independently found and top-ranked by two separate audits (8.80/10 and 8.3/10); this document's own kill test (Part II) confirms the cheap gates pass and pinpoints the real remaining risk precisely. No paper found occupying the specific conjunction. |
| 2 | Spec 02 — STAV (stability-constrained adaptive verification) | Live but deprioritized | Never independently killed in this investigation — simply superseded once a doubly-audited stronger candidate appeared. Worth a proper kill test if this direction's transfer gate (Part V, Stage 2) fails. |
| 3 | Spec 04 — Compaction/architecture attrition | Superseded, scored 5.1/10 above | This document's own §8.1 table gives the full breakdown. Anchor paper already varies topology; MemUse and MafiaScope already own its measurement methodology. |
| 4 | Self-preference bias as collaborator-selection pressure | Weak survivor, not pursued | Real and unclaimed, but one Becker (1973) assortative-matching re-derivation away from the same fate as everything below it. |
| 5 | Spec 01 — Dec-POMDP-optimum-grounded LLM evaluation | **Retracted** | Core decomposition is a named 2002–2004 result (value of communication). **Note:** neither of the two audits behind this document's recommendation revisits or contradicts this — `AAMAS_2027_TWO_CANDIDATE_RESEARCH_AUDIT.md` mentions POMDPs only as a purity-test warning against Candidate A collapsing into single-agent latent-mode identification, and as one throwaway alternative-formulation suggestion. Spec 01's retraction rests entirely on Goldman & Zilberstein / Pynadath & Tambe / Marschak & Radner and stands independently of everything in this document. |
| 6 | Spec 03 — Sanctioning under unreliable blame | **Retracted** | Headline threshold is a 2010 experimental-economics result (Grechenig, Nicklisch & Thöni), replicated 2012. |
| 6= | Acceptance-gate manipulation-resistance | **Closed** | PACE (Jun 2026) already frames it as "a textbook case of adaptive data analysis" and ships the fix, three months before this project proposed it. |
| 6= | Shared experience pool as strategic commons | **Closed** | Ghosh & McAfee (WWW 2011) states the exact equilibrium prediction, word for word, fifteen years early. |
| 6= | Verifier panels vs. strategic persuader | **Closed** | Kaniovski (2008) proves the non-monotonicity result from correlation alone, no adversary needed. |

### A.6 The structural lesson this investigation produced

Every LLM-substrate candidate that took the shape "import a classical AAMAS concept (reputation, sanctioning, jury aggregation, public-goods provision, team decision theory) and graft an LLM onto it" was killed by pre-2020 economics, game theory, or control theory — invisible to any search confined to the modern LLM-agent literature, because the killing paper predates LLM agents entirely. **The current recommendation was selected in part because it does not have this shape**: its core mechanism (a peer that reacts to being probed, in a setting with restricted and costly intervention) is a live, actively-studied MAS-theoretic object with mature adjacent literature (opponent shaping, dual control, causal games) but no single paper that already occupies the specific conjunction — a genuinely different risk profile from every prior candidate in this investigation.

---

## Appendix B — Provenance and Methodology Notes

- Two independent literature audits are the primary evidentiary basis for this recommendation: `research_run_2026-09-08/AAMAS_HIGH_CONFIDENCE_GAPS_REPORT.md` (8 independent agent roles, 75 substantively-examined primary papers, 42 candidates generated and reduced to 5) and `AAMAS_2027_TWO_CANDIDATE_RESEARCH_AUDIT.md` (15 independent role-audits in three waves, 90+ distinct research records screened, 63 unique arXiv identifiers plus 31 unique DOIs).
- Neither audit claims verified novelty. Both explicitly rate this direction's novelty confidence as **Medium**, not High — this document preserves that honesty rather than overstating the case. Absence of a killing paper in a search is evidence for continued investigation, not proof of absence; both audits state this directly, and it applies here.
- The kill test in Part II of this document was constructed and computed independently in this session, following the audits' prescribed method (Gate A0 / Gate A1) but not copying either audit's specific example — it extends the audits' own illustrative minimal example into a full construction with an explicit reward structure, then runs the harder transfer test neither audit itself executed.
- A second literature check for anything published between the anchor evidence's dates and the actual submission date is required before committing to submission — both source audits state this as a standing limitation of any search with a fixed cutoff, and this document inherits that obligation.
- **Explicit note on spec 01 (Appendix A.1):** a direct keyword check of `AAMAS_2027_TWO_CANDIDATE_RESEARCH_AUDIT.md` for Dec-POMDP, decentralization/centralization value-of-communication, Goldman, Zilberstein, Pynadath, or Tambe returns no substantive hits — the file's only POMDP-adjacent content is a purity-test warning that Candidate A degenerates into single-agent POMDP identification if the multi-agent reflexivity is stripped out, and one throwaway line among five alternative formulations suggesting a *decentralized* variant of Candidate A itself. Neither engages spec 01's actual claim. This was verified by direct `grep` on 9 September 2026, not inferred.
