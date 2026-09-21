# S4-ATTACK-D2 — Adversarial attack on Direction D2: "The missing control: natural attenuation"

**Date:** 2026-09-21
**Stance:** hostile. Goal: kill or shrink D2 before it costs experiment budget.
**Reports read first:** audit2 A2, A3, A8, A10; reports B4, B14, D1, D2 (fault-injection line), E1, E6, F1, R1; CtC_fulltext_verification; raw full text of Hallucination Cascade (audit2/raw_s2/ar5iv/2606.07937.html).

**D2 as assigned:** published containment effects (CtC, DamageFlow, Huang 2408.00989, BRA-Audit) lack a would-have-died-anyway control; measure escape/attenuation base rates across structures and fault types in tool-executing LLM-MAS; re-evaluate containment mechanisms against the natural-attenuation baseline rather than zero-containment.

---

## 0. VERDICT: SURVIVES WITH NARROWING — heavy narrowing; demote from standalone direction to an embedded control arm + one re-evaluation analysis inside the main H1/H2 paper

The direction's *stated premise* is factually wrong about its own named targets (§2), its *framing* is conceptually confused (§3), and its *standalone publishability* is result-dependent (§5). What survives is a genuinely unoccupied, cheap, and load-bearing measurement: per-fault counterfactual decomposition of containment effects in tool-executing organizational MAS. That is a section of the main paper, not a paper.

---

## 1. ATTACK (a): is this just a methods critique that belongs in a blog post?

**Largely yes, as stated.** "You did not control for natural attenuation" is a referee-report paragraph, not a contribution. D2 becomes paper-shaped only if it delivers one of:
1. a base-rate map (escape/attenuation by structure × fault type) — **partially occupied** (see §2): Hallucination Snowball's per-stage escape probabilities (24.6/48.3/89.3%, ABSTRACT VERIFIED via B4/A2), Hallucination Cascade's attenuation factor (0.644, FULL TEXT re-verified this session), AgentProp-Bench's 0.62 propagation probability (ABSTRACT VERIFIED, A8), MAS-FIRE's emergent neutralization (40%+ of faults neutralized by iterative loops, FULL TEXT per D2-report);
2. a re-evaluation that *changes a conclusion* (mechanism ranking flips, or a named mechanism goes net-negative once self-masking faults are excluded) — unoccupied, but the authors cannot promise this outcome ex ante (see §5).

A MASO reviewer pool (classical-MAS-heavy) will read a standalone "missing control" paper as agent-eval methodology criticism — the genre R1 already flagged as recombination. The critique is also *self-undermining* if stated against CtC/Huang, because those papers contain the arm D2 claims is missing (§2).

## 2. ATTACK (b): has anyone already run no-intervention propagation baselines properly?

**Yes — repeatedly, including inside the exact papers D2 names.** This is the most damaging finding.

| Paper (verification) | No-intervention / natural-dynamics content | What it lacks (D2's residue) |
|---|---|---|
| **CtC, ICERA 2026 (FULL TEXT, reports/CtC_fulltext_verification.md)** | Has an explicit **NoGuard arm** in its 5-condition bake-off; unguarded containment 46.2%, unguarded cascade depth ~doubles with scale | Simulation only; no per-fault counterfactual; no cost vector |
| **Huang 2408.00989, ICML 2025 (ABSTRACT via 4 prior reports + D2-report)** | The **vs-none arm is structure-conditional natural resilience already measured**: hierarchy 5.5% vs flat 10.5% vs chain 23.7% degradation under faulty agents with no mechanism. That *is* "attenuation varies across structures," published, at a top venue | Aggregate task-performance metric, not escape probability; persistent faulty-agent model; toy 3-agent structures |
| **MAS-FIRE, arXiv:2602.19843 (FULL TEXT per reports/D2)** | **Entirely a no-intervention observational study**: process-level detection/recovery metrics (O_f, L_f); "iterative loops neutralize 40%+ of faults" — natural recovery quantified across 3 architectures | Reasoning benchmarks (HumanEval/WikiTableQuestions/WebShop); architecture confounded with domain; no containment re-evaluation |
| **Hallucination Cascade 2606.07937 (FULL TEXT re-verified this session from local ar5iv copy)** | Injected-hallucination cascades traced with **no containment**; net attenuation 0.644 (Chain-3), per-transition −0.072, explicit recovery-rate metric; "injected-hallucination cascades trace controlled factual errors across agents" | One fault type (factual hallucination); sequential chains depth ≤3; no tools; no mechanisms to re-evaluate |
| **Hallucination Snowball 2608.14588 (ABSTRACT VERIFIED)** | Per-stage **escape probabilities** (24.6/48.3/89.3%) with 346 injected hallucinations — an escape base-rate table across pipeline stages | Linear pipeline; hallucination only; no org structure |
| **Spark-to-Fire 2603.04474 (ABSTRACT VERIFIED via B4)** | No-mitigation arm: one atomic seed → widespread failure; mitigation ≥89% prevention measured *against* that natural-propagation baseline | Message-dependency medium only; binary final-infection construct |
| **OrchestraBench 2608.05263 (FULL TEXT per W2/D1/E6)** | **Per-failure-mode recovery tiers**: tool faults 1.0, ambiguous delegation 0.30, latent/semantic 0.0; blind retry reproduces latent faults — natural/naive recovery differentiated by fault type | Controlled chains; no org boundaries; no containment-mechanism design |
| **AgentChaos, ASE 2026 (FULL TEXT per D2-report)** | Trigger verification filters untriggered tasks (a would-have-fired control); degradation-only | No recovery/attenuation measurement; no mechanisms |
| **AgentProp-Bench 2604.16706 (ABSTRACT VERIFIED, A8)** | Natural propagation probability ≈0.62 error→wrong-answer, no intervention | Single-agent; answer-level |
| **TRAJDEBUG 2608.06346 (ABSTRACT via B14/D1)** | 7.62 local errors per failed trajectory, only 1 critical — natural self-masking quantified | Single-agent; offline diagnosis framing |
| **DamageFlow (OpenReview full record, B4)** | Already has a **counterfactual** measure: "BRS prevented at tool boundary" | Adversarial security; single-agent-centric; 80-scenario pilot |

**Consequence:** D2's premise "published containment effects lack a would-have-died-anyway control" is **false in its literal form for CtC and Huang** — both have no-mechanism arms, and a no-mechanism arm *is* the natural-attenuation condition. A10's meta-observation ("the natural escape base rate is unmeasured everywhere") also overstates: escape/attenuation base rates are measured in at least four venues (Snowball, Cascade, AgentProp-Bench, MAS-FIRE). The accurate residual claim is narrow: **no paper measures per-fault-type × organizational-structure escape/attenuation base rates in tool-executing LLM-MAS, and no paper re-grades containment mechanisms conditional on the per-fault counterfactual (would this specific fault have propagated unaided?).** Everything broader is occupied.

## 3. ATTACK (c): is "mechanisms must beat natural attenuation" already the implicit standard?

**Yes, and this is D2's deepest conceptual problem.** Any mechanism-vs-no-mechanism comparison *is* a comparison against natural attenuation — the no-mechanism arm is not "zero containment" as distinct from natural attenuation; it *is* natural attenuation. D2's framing ("re-evaluate against the natural-attenuation baseline rather than zero-containment") names a distinction that does not exist. A reviewer will say: "the NoGuard arm already did that."

The non-trivial content hiding inside D2 is different and must be stated precisely or the direction dies in review: **per-fault counterfactual attribution** — decompose a mechanism's measured effect into (i) benefit on faults that would have propagated unaided, vs (ii) wasted intervention on faults that would have self-masked. The field is already groping at this without formalizing it: BRA-Audit's false positives cause unnecessary rollbacks (FULL TEXT per stage-1 inventory); AgentChaos's trigger verification; AgenTracer/DoVer's counterfactual-replay machinery (mature, but aimed at attribution, not containment grading). Note the implication: D2's *method* (counterfactual replay) already exists in the attribution line — D2 is an application of existing machinery to a new target, which caps its methodological novelty.

## 4. ATTACK (d): does it fit MASO, or is it generic agent-eval methodology?

**As stated: generic.** Nothing in "measure base rates, re-grade mechanisms" is organizational. Salvage path: attenuation-as-organizational-property — *which structures self-contain which fault classes without any mechanism* is a genuinely organizational question (Huang's none-arm hints hierarchy self-contains better; A10's internal hypotheses A10-H2/A10-H9 already frame depth × fault-class and committedness-threshold versions of this). MASO topic 7 (cascading/systemic failure detection and mitigation, per B14) accommodates it. But note: **A10 has already internalized this content** — A10-H9 ("which faults escape natural containment") is D2's base-rate half proposed as a hypothesis inside the main paper, and A10 recommends it as a *mandatory control condition*. That is the correct home for D2, and its existence as an internal hypothesis confirms D2 is a component, not a direction.

## 5. ATTACK (e): null-result test — if containment mechanisms DO beat natural attenuation, is it publishable?

**Weakly, and this is fatal for D2 as a standalone direction.** If mechanisms beat the base rate, the headline reduces to "containment works" — already shown by CtC (46.2→99.4%, sim), Huang (96.4% recovery), BRA-Audit (monotone improvement) — plus a base-rate map that replicates Snowball/Cascade in a new setting. Classical-MAS reviewers will call that a solid but incremental measurement paper. D2's publishable mass is concentrated in outcomes the authors cannot guarantee: mechanism rankings change, a named mechanism goes net-negative after excluding self-masking faults, or attenuation is sharply structure-dependent (which would feed H1). A direction whose value hinges on the sign of its result is a bet, not a plan. Mitigating fact: the no-intervention arm is *required anyway* for H1/H2, so D2's marginal cost as an embedded analysis is near zero — which is exactly why it should be embedded, not standalone.

## 6. What precisely survives

1. **Per-fault counterfactual re-evaluation of containment** in tool-executing organizational MAS: report mechanism benefit conditional on would-have-propagated, and wasted-intervention cost on self-masking faults. Unoccupied (verified negative across B4/B14/D1/D2/E1/A2/A3/A8 sweeps); BRA-Audit's false-positive rollbacks show the cost is real and unquantified.
2. **The escape/attenuation base-rate map across organizational structures × fault classes** (content vs commitment faults) in tool-executing MAS — occupied only for chains/pipelines/single-agent/hallucination-only.
3. **As framing for the main paper:** "CtC assigns detectability; Huang's none-arm hints structure self-contains; we measure the base rate and grade mechanisms against it" — one related-work paragraph plus one results section.

**Dead on arrival:** any claim of the form "containment papers lack a no-intervention control" (CtC NoGuard, Huang vs-none, Spark-to-Fire no-mitigation arms exist); any claim that escape/attenuation base rates are "unmeasured everywhere" (Snowball, Cascade, AgentProp-Bench, MAS-FIRE); any standalone-paper framing of the critique.

## 7. Confidence

**Moderate-high.** Load-bearing items re-verified this session: Hallucination Cascade full text (local ar5iv copy — attenuation 0.644, injected-fault arm, recovery metric all confirmed verbatim); CtC NoGuard arm (FULL TEXT verification note); MAS-FIRE/AgentChaos/Spark-to-Fire/OrchestraBench designs (FULL TEXT per D2/D1/E6/W2 reports). Huang 2408.00989 none-arm numbers and Snowball escape probabilities are ABSTRACT-level via multiple prior reports — the one residual risk is that Huang's none-arm detail is richer than reported, which would *strengthen* this attack, not weaken it.
