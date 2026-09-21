# Adversarial Novelty Audit — Final Report (21 Sep 2026)

**Process:** Stage 1: 12 independent specialists (fault tolerance, org structure, recovery, scarcity red-team, classical MAS, distributed systems, human oversight, tool benchmarks, hostile reviewer, hypothesis generator, terminology expansion, citation network). Stage 3/4: full-text verification of the 3 H3-deciding papers + 9 secondary threats, and dedicated adversarial attacks on 4 candidate directions. Reports: `maso_2026_investigation/audit2/` (A1–A12, S3/S4 series). Stage 1 found **11 papers missed by all 48 prior reports** — the vocabulary-failure warning was vindicated.

---

## A. Executive verdict

| Hypothesis | Verdict | Reason |
|---|---|---|
| **H1** (depth → propagation/recovery cost) | **SURVIVES WITH NARROWING** | As a phenomenon it is classical (D&K unzippering, 600–700% inflation at depth 4) and the amplify-vs-attenuate *framing* is 29 years old (Hägg 1997 states both positions verbatim). OrchestraBench varies chain depth under faults (single-LLM chains). Survives only as a transfer test: delegation *authority* depth under semantic faults with recovery **cost** measurement — that exact cell is empty. |
| **H2** (containment reduces propagation at a cost) | **COLLIDED as a headline** | Cost premise triple-occupied at full-text level: Sherlock (2511.00330, cost-optimal verifier placement + rollback), Verifier Tax (2603.19328, enforcement cost on tau-bench), BRA-Audit (2608.14668, budgeted auditing + rollback on real MAS). Mechanism comparisons exist (RoMa, CtC, SHO). Demote to background. |
| **H3** (containment backfires under scarcity) | **SURVIVES WITH NARROWING — but not as "demonstrate the backfire"** | The phenomenon is occupied classically twice (D&K slight; **Kota TAAS 2012 strong** — maximal recovery drives profit *below zero*, FULL TEXT) and mechanistically in distributed systems (metastable failures). On LLM substrate, Xiang (SSRN 7348298, FULL TEXT) has a sign reversal but single-agent, no propagation, degenerate mechanism. See §C. |

**Recommended direction (§G):** keep the classical-transfer paper, but re-aim its headline from "demonstrate backfire" to **"map when the crossover occurs"** — with three non-classical mechanisms no prior work has, a detection-quality de-confounding instrument, and a natural-attenuation control.

## B. Most dangerous prior art (verified)

| Paper | Threatens | Verification |
|---|---|---|
| Kota, Gibbins & Jennings, TAAS 2012 (10.1145/2168260.2168261) | H3 — recovery consumes task capacity; maximal recovery net-harmful; cost-aware meta-reasoned recovery tracks upper bound. **This is the refined H3′ contrast, published 2012.** | FULL TEXT |
| Dellarocas & Klein, ICMAS 2000 (10.1109/ICMAS.2000.858440) | H1 + H3 classically (unzippering; sentinel backfire under scarcity) | FULL TEXT |
| Xiang, SSRN 7348298 | H3 sign reversal on LLM agents (gate effect −0.315 at zero budget → +0.140 at budget 6, DiD +0.456) — but single-agent, accuracy DV, degenerate harm mechanism, not pre-registered as hypothesis | FULL TEXT |
| Bronson et al., HotOS 2021 + Huang et al., OSDI 2022 (metastable failures) | H3's mechanism conceptually identical in distsys; powers the "just retry storms" reject | FULL/PARTIAL |
| BRA-Audit (2608.14668) | H2 — budgeted auditing + rollback + token cost on real MAS; one scarcity ablation away from H3 | FULL TEXT |
| Sherlock (2511.00330, Microsoft) | H2 cost premise — cost-optimal verifier placement | FULL TEXT |
| Outcome Monitors (2608.19303) | Our exact environment (tau-bench retail) + silent semantic tool faults + recovery, single-agent, stronger protocol than our plan | FULL TEXT |
| Huang et al. 2408.00989 | Structure × faults (linear/flat/hierarchical; Inspector recovers 96.4%) | FULL TEXT |
| OrchestraBench (2608.05263) | Depth varied under faults with cascade radius + recovery rates (single-LLM chains) | FULL TEXT |
| Self-Healing Orchestrators (2606.01416) | Budget sweep exists; H3-silent (no no-recovery arm, decoupled budgets) — not opposite-sign as Stage 1 feared | FULL TEXT |
| Loop-Back Authority (2609.14767); Leadership-as-Control (2606.19111); Resilient Consensus (2606.15024) | Generic "first classical transfer test" framing — occupied three times. Only the **fault-handling** instantiation survives | FULL/ABSTRACT |
| Kaminka & Tambe, JAIR 2000 | Kills the premise "classical MAS assumed perfect detection" (monitoring-selectivity theorems, FP/FN-asymmetric heuristics). Claim only "detection quality was never an experimental factor" | FULL TEXT |
| Oversight Has a Capacity (2606.08919) | Reviewer-capacity inverted-U (modeling, single-agent gating) | ABSTRACT |
| Memory-poisoning repair (10.20944/preprints202602.1188.v1) | Kills "memory boundary is the open wedge" (isolation/rewriting repair, −78.1% propagation) | ABSTRACT (Crossref) |
| Sentinel Agents (2509.14956) | Occupies the *word* "sentinel" for LLM MAS without citing classics — cite and differentiate | FULL TEXT |
| 2606.20695 (tau2-retail MA methodology) | **Power constraint: paired noise floor up to +18pp at n=100; binary contrasts need n≥250/cell** | FULL TEXT |

## C. H3 deep audit

**Has scarcity-induced containment backfire been demonstrated?**
- **Directly, classically:** yes, twice (D&K slight; Kota strong, with the budget-aware/budget-unaware contrast and design prescription included).
- **Directly, distributed systems:** yes, mechanistically (metastable failures; retry storms; a 2026 SSRN retry paper turned out weaker than billed — retry worse in *all* scenarios, no abundance arm).
- **Directly, LLM substrate:** only Xiang — and the mechanism is the *opposite causal direction* (scarcity starves the gate's input; the gate doesn't consume the scarce resource), single-agent, no propagation, not a pre-registered hypothesis.
- **In executing organizational LLM-MAS with propagating semantic faults, where containment spends the task's own budget:** **no. The conjunction is empty (HIGH confidence — three independent search processes + citation-network sweep of ~1,060 citers).**

**Why hasn't adjacent literature made it obvious?** Because the LLM-MAS version has three non-classical mechanisms: (i) detection is imperfect and costly (classical/distsys detection is free and perfect — the backfire threshold *shifts* with detection quality); (ii) false-positive containment has organizational collateral (quarantining a healthy agent strands its subtasks — BRA-Audit's FP→unnecessary-rollback channel, unquantified); (iii) the reviewer budget is a post-fault race with queue interference. These are what stop the "just retry storms" review — not the multi-agent setting alone (that *is* a trivial-extension reject: FTDI, BRA-Audit, Arslan 2608.06949 are already budget×containment in LLM MAS).

**Exact remaining gap:** not *that* the crossover exists (Kota showed it) but *when* — the crossover point mapped parametrically across budget currencies (tokens, tool calls, latency, reviewer minutes) under imperfect detection, on real tool-executing organizations. Genuine suspense exists: SHO's sweep is H3-silent, so the LLM-MAS sign pattern is empirically open.

## D. Contradictions in the literature (usable for a conflict-resolution frame)

1. **Hierarchy helps** (2408.00989 fault resilience; OrgAgent +102.7%) **vs hierarchy hurts** (Loop-Back Authority, d=0.42) vs **flat=hierarchy at equal memory** (2608.00028). No settled account of when hierarchy pays.
2. **Depth amplifies** (D&K unzippering; CtC scaling) **vs attenuates** (Hallucination Cascade 0.644 net attenuation, FULL TEXT).
3. **Containment helps** (CtC 46→99%) **vs containment strands** (CtC's own no-rollback ablation: success 83.3→2.6%) **vs containment harms benign work** (Agent Mesh; Audit Without Verification 60.3→4.1%).
4. **More verification better** (mainstream) **vs verification sign-flips with budget** (Xiang) **vs corrupt successes pass verification** (PAE 2603.03116).
5. **Budget-aware recovery dominates** (SHO) **vs budget-unaware recovery catastrophic** (Kota) — never tested in the same system.

## E. New hypotheses (from hypothesis generator A10; top survivors after Stage-4 attacks)

Full list of 12 in `audit2/A10_hypotheses.md`. Strongest:
1. **Detection-quality × scarcity interaction** — the backfire threshold shifts as detection degrades (no classical analogue; absorbs D3).
2. **Reservoir-matched containment** — containment must target the fault's *current reservoir* (memory, environment state, adopted peer beliefs), not its origin medium or origin agent (TIDE shows agent-removal fails post-adoption; Emergence World shows 46h memory reactivation).
3. **False-positive quarantine collateral** — organizationally-stranded subtasks from wrongly quarantined healthy agents, as a first-class cost.
4. **Reviewer-budget race** — escalation consumes a shared, queuing reviewer budget; containment via escalation exhibits congestion collapse.
5. **Non-monotone verification laundering** (A10-H1) — verification status decays/launders through summarization (cf. 2609.20211).
6. **Committedness threshold** (A10-H9) — faults self-mask unless they cross a committedness threshold; containment value is concentrated above it (mandatory pilot measurement regardless).

## F. Top 3 research directions

### Direction 1 (RECOMMENDED): The transfer test, re-aimed — "When does containment pay?"
- **RQ:** Which predictions of the classical MAS fault-handling canon (D&K sentinels/unzippering; Kota recovery-cost reversal; Hägg) transfer to tool-executing LLM agent organizations, and where is the containment×scarcity crossover under imperfect, costly detection?
- **Hypotheses:** H1-transfer (depth inflates recovery cost — conflict-resolution vs Hallucination Cascade attenuation); H3′ (the crossover exists but its location depends on detection quality and budget currency — non-classical mechanisms); sentinel-vs-Inspector contrast with cost (H2 reframed).
- **Closest prior art:** Kota 2012, D&K 2000 (classical originals); Xiang (single-agent sign reversal); CtC (simulation containment); BRA-Audit (budgeted auditing).
- **Exact novelty:** the conjunction organizational × tool-executing × propagating semantic faults × containment-spends-task-budget × detection-quality instrument × parametric crossover map. Every pair is occupied; the conjunction is empty.
- **Experiment:** tau2-retail org wrapper; depth {2,3,4} × handling {none, survivalist, sentinel} × scarcity {abundant, scarce} × detector {oracle, syntactic, LLM-semantic}; natural-attenuation control arm; faults: agent death + corrupted handoff (+ memory-staleness arm if gates pass).
- **IVs:** depth, handling, scarcity, detector quality. **DVs:** task utility (deterministic DB state), recovery cost (tokens/tool-calls/latency/reviewer-minutes), propagation count (arm-invariant boundary inventory). **Controls:** no-fault baselines, no-mechanism (attenuation) arm, budget-matched scaffolds.
- **Minimal matrix:** ~18–24 core cells; **n≥250/cell for binary contrasts on tau2-retail** (2606.20695 noise floor, FULL TEXT) or continuous endpoints + full within-instance pairing at n≈40–70. Total ~2,500–4,000 runs.
- **Expected figures:** (1) recovery-cost inflation vs depth, classical-vs-LLM overlay; (2) containment-benefit × budget curves per detector quality with crossover points marked; (3) mechanism Pareto (utility vs cost) under abundance vs scarcity.
- **Outcomes:** positive (crossover found, shifts with detection quality) = headline; null (containment robustly pays) = resolves D&K/Kota transfer in the negative, publishable via pre-registered TOST; reversed (containment always hurts) = explosive, rules out prior concerns.
- **Difficulty:** moderate; reuses validated tau2+LangGraph plan. **Main attack:** "Kota did this in 2012." **Defense:** Kota demonstrated *that*; we map *when*, with mechanisms (detection quality, FP collateral, reviewer queue) that have no classical analogue, on a substrate whose failure modes are semantic.

### Direction 2: Reservoir-matched containment (D4, repaired)
- **RQ:** Must containment target the fault's current reservoir (agent / memory / environment state / adopted beliefs) rather than its origin?
- **Strong section, weak standalone paper.** Merge into Direction 1 as the memory/state arm. Prediction repaired after TIDE falsified the clean version.

### Direction 3: Detection-quality frontier (D3, narrowed)
- **RQ:** How does containment benefit change as detection degrades from oracle to localization-incapable?
- **Flat-frontier risk is real** (CUADebug: machine RCA ≈ oracle; Conformal: within 1 SD). Survives only with the flat outcome pre-registered as publishable. Best used as Direction 1's de-confounding instrument rather than a standalone paper.

## G. Recommended direction

**Direction 1**, with D3 embedded as the detector dial and D2 embedded as the attenuation control. This is the only configuration where: the gap is verified-empty after 3 adversarial rounds; the classical-MAS reviewer pool sees its own canon tested rather than ignored; the null result is publishable by design; and the build fits the deadline (it is the already-planned minimal design plus the detector dial and the n≥250 power correction).

Do NOT submit H3 as "we demonstrate containment backfire." That claim is occupied by the very classical paper we anchor on.

## H. Novelty sentences

1. **Aggressive (do not use):** "First demonstration that fault containment backfires under resource scarcity in LLM agent organizations." — Collides with Kota 2012, D&K 2000, and (weakly) Xiang 2026.
2. **Defensible (use):** "We present the first experimental transfer test of the classical MAS fault-handling canon (Dellarocas & Klein; Kota et al.) on tool-executing LLM agent organizations — where detection is imperfect and costly, faults are semantic, and containment spends the task's own resource budget — and parametrically map the containment×scarcity crossover that classical work demonstrated only qualitatively."
3. **Conservative (fallback):** "A pre-registered replication-and-extension of classical organizational fault-handling results in LLM-based agent organizations, with two measurement contributions: the detection-quality × containment-benefit frontier, and the containment×scarcity crossover location across four budget currencies."

## I. Evidence confidence

| Conclusion | Confidence |
|---|---|
| H3 phenomenon classically occupied (D&K, Kota) | HIGH (full text both) |
| H3 mechanism = metastable failures (distsys) | HIGH |
| LLM-substrate sign reversal exists but degenerate/single-agent (Xiang) | HIGH (full text via authors' repo) |
| SHO is H3-silent, not opposite-sign | HIGH (full text) |
| The full conjunction (org × tool-executing × propagation × containment-spends-budget × detection instrument) is empty | HIGH (3 independent processes + citation network) |
| Generic classical-transfer framing occupied; fault-handling instantiation open | HIGH |
| tau2-retail binary contrasts need n≥250 | HIGH (full text 2606.20695) |
| Flat-frontier risk for detection-quality dial | MEDIUM (CUADebug/Conformal full text, but different setting) |
| Absence claims for 19–21 Sep submissions | LOW (not yet announced; re-sweep before submission) |
| Memory-repair preprint's exact scope | MEDIUM (abstract-only; preprints.org bot-walled) |

## Pre-mortem: the five most likely novelty rejections

1. **"This is metastable failures / retry storms for LLM agents"** (Bronson HotOS 2021) — fixable only by framing + the non-classical mechanisms (detection quality, FP collateral, reviewer queue). Serious.
2. **"Kota et al. 2012 already showed recovery cost can exceed benefit, including the budget-aware contrast"** — fixable by reframing to crossover-mapping + transfer test. Serious if unaddressed.
3. **"Xiang already measured the sign reversal on LLM agents"** — fixable experimentally (multi-agent, propagation DV, non-degenerate mechanism). Moderate.
4. **"Your 'missing control' premise is wrong — every containment paper has a no-guard arm"** — fixable by scoping to per-fault counterfactual decomposition. Moderate.
5. **"Your effects are inside tau2-retail's noise floor"** (2606.20695) — fixable only experimentally (n≥250 or continuous+paired design). Serious.
