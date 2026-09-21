# W2 — STATISTICS Reviewer F-C: Statistical Plan for CAND-1, CAND-2, CAND-3

**Investigator:** Wave-2 STATISTICS reviewer F-C
**Date:** 21 Sep 2026
**Assignment:** Design the statistical plan for the three leading candidates (CAND-1 OrgBlast, CAND-2 ClassicalTransfer, CAND-3 AttribContain): IVs/DVs, controls, task-instance counts, repeats/seeds, CIs, effect sizes, significance tests, multiple-comparison correction. Concrete power analysis at n=30–50 runs/cell for 15–30pp effects on containment rate. Minimum viable experiment matrix.
**Builds on (read in full):** F1_feasibility_scan.md, B15_metrics.md, B5_fault_injection.md, B3_failure_attribution.md, E2_assassin_containment.md, E5_assassin_classical_mas.md, B8_human_escalation.md, B16_cost_reliability.md. No new literature search was needed; this report is the design/analysis layer on top of those verified facts.

---

## 1. Bottom line

1. **The wave-1 power claim is optimistic and must be corrected before it propagates into a proposal.** F1 states "n=30/cell detects ~25–30pp; n=50/cell detects ~20pp" for binary outcomes. Exact computation (two-proportion test, α=.05 two-sided, power=.80, baseline near p=0.5): **n=50/cell detects ~28pp, n=40 detects ~31pp, n=30 detects ~36pp. A 20pp difference needs 90/cell unpaired; a 15pp difference needs ~167/cell.** At n=50/cell, power for a true 20pp effect is only 0.55; for 15pp, 0.34. **15–20pp effects on a binary containment rate are NOT adequately powered at n=30–50/cell under any unpaired design.**
2. **Three design moves recover the power:** (a) make the **continuous blast-radius fraction the co-primary endpoint** (d=0.65 detectable at n=37/cell unpaired, 19 pairs paired); (b) **pair by task instance** — run every instance under every containment arm, giving McNemar/conditional-logistic power (20pp detectable at ~53–71 pairs for realistic within-instance correlation ρ=0.3–0.5); (c) for CAND-3, replace cell-by-cell comparison with **regression over a controlled attribution-accuracy dial**, which uses all observations to estimate the threshold with a bootstrap CI.
3. **Interactions are the power bottleneck.** A difference-in-differences of 20pp needs ~188/cell — infeasible. Only large crossover interactions (DiD ≥ ~40pp, e.g., CAND-2's predicted containment-backfires-under-scarcity sign reversal) are detectable at n≈35–40/cell. All modest interactions must be reported as effect sizes with CIs, labeled exploratory.
4. **Minimum viable matrix (all three candidates, shared testbed): ≈2,800 runs**, ~$60–220 on GPT-5-mini/DeepSeek-class models (F1 pricing) — feasible in the window. If only one candidate survives selection, CAND-1 core = 1,360 runs.
5. **Deterministic ground truth is achievable for every primary endpoint** (tau2-style DB-state diff + trace-provenance propagation measurement). LLM-as-judge is confined to one secondary semantic-quality DV with rubric, two judge models, κ≥0.7 gate, and a 10% human audit.

---

## 2. Cross-cutting design principles (apply to all three candidates)

### 2.1 Unit of analysis and the instance-vs-seed budget

- **Unit of analysis = one workflow execution (run).** Runs cluster within **task instances** (a specific refund/incident/procurement scenario with an annotated goal DB state).
- **Between-instance variance dominates.** τ-bench evidence: pass@1 <50% but pass^8 <25% on retail (arXiv:2406.12045) — i.e., instance difficulty, not seed noise, is the largest variance component. Therefore: **spend budget on more instances, not more seeds.**
- Recommended allocation: **I = 40–50 distinct instances per workflow × R = 1–2 seeds per (instance × condition) cell**, with each instance run under *every* condition (full within-instance pairing). Plus a **reliability sub-study**: 10 instances × 8 seeds in key cells to estimate seed-level variance and report pass^k.
- **Pilot (mandatory, days 9–11 per F1):** 10 instances × 5 seeds × a subset of cells → estimate variance components (ICC), fault-trigger rates, and instance-difficulty spread. Use blinded variance re-estimation to confirm or adjust I before main runs. This is an internal-pilot design; the pilot data are not pooled into the confirmatory analysis if the design changes.

### 2.2 Deterministic ground truth (primary endpoints never use a judge)

All primary DVs are computed deterministically from logs and environment state:

| DV | Deterministic operationalization |
|---|---|
| Task success | End DB state == annotated goal state (tau2-bench pattern; verified substrate in F1) |
| Blast radius (BR) | Fraction of downstream organizational boundaries crossed by fault effects, computed from the **trace provenance graph** (which roles/agents consumed fault-tainted messages) + count of DB records diverging from goal state + count of tool calls with fault-tainted arguments. Boundary types: role, communication, authority/delegation, tool, memory, accountability, human-agent |
| Containment rate (C) | Binary: 1[fault effects confined to the boundary of origin] = 1[BR = 0 beyond origin boundary] |
| Recovery cost | Tokens (in/out), tool calls, wall-clock, steps-to-containment, simulated human minutes (deterministic latency model × human actions) |
| Collateral damage | Count of healthy agents quarantined / healthy steps rolled back / unnecessary verification calls (all from logs) |

**Fault-trigger verification (AgentChaos's lesson, arXiv:2608.06790):** every injected fault is checked post-hoc for actual manifestation. Primary analysis = **triggered-only (per-protocol on trigger)**; sensitivity analysis = intention-to-treat over all injected runs (injection as an instrumental encouragement). Report trigger rate per fault type; any fault type with <70% trigger rate is redesigned or dropped before main runs.

### 2.3 LLM-as-judge policy (secondary only)

- One secondary DV may be judge-scored: **semantic containment quality** (did the user-facing outcome reflect the fault despite DB-state success — the PAE corrupt-success concern, arXiv:2603.03116).
- Rubric-anchored ordinal items; **two judge models from different families**; require Cohen's κ ≥ 0.7 between judges, else the DV is dropped, not averaged.
- **Human audit:** stratified random 10% of runs (min 50) manually inspected by two annotators (κ reported, disagreements adjudicated); report judge–human agreement. Judge results are labeled secondary in all tables.

### 2.4 Controls and confound management

- **Fixed backbone** per experiment block (GPT-5-mini primary; DeepSeek v3.2 as generalization block). Model is a fixed factor; never pool across models without a model×condition interaction check.
- Temperature: low/default for main runs; a 10% subset re-run at temperature 1.0 as a robustness check. API seeds fixed and logged where the provider supports it; all prompts/responses/traces persisted (JSONL per run, per F1 instrumentation plan).
- **Fault-free baseline runs** for every instance in every structure arm: needed as the blast-radius reference and as an instance-difficulty covariate (ANCOVA-style adjustment).
- No-fault control cells in every factorial to separate fault effects from mechanism overhead (mechanisms cost utility even without faults — the Sentinel ablation lesson: circuit breaker vs checkpoint rollback have different fail-safe/fail-operational roles, DOI 10.1109/ICERA72709.2026.11666599).
- Human escalation arm uses a **scripted simulated human** (deterministic oracle + a noisy variant with pre-specified error rate, e.g., 80% correct, fixed response latency) — real-human study is out of scope for the deadline and is stated as a limitation. This keeps the human-agent boundary condition reproducible and costed (human minutes = latency × interventions).

### 2.5 Estimation and reporting standards

- Proportions: risk differences with **Newcombe score CIs**; odds ratios from logistic models.
- Continuous: mean differences with bootstrap percentile CIs (10,000 resamples at the **instance** level to respect clustering); Cohen's d and rank-biserial correlations as standardized effects.
- Derived quantities (CAND-3 threshold, inflation ratios in CAND-2): bootstrap CIs resampling instances.
- Primary models: **GLMM with random intercept per task instance** (logistic for C/success, Gaussian or beta-regression for BR). If GLMM fails to converge: GEE with exchangeable correlation and cluster-robust SEs. Paired binary contrasts: McNemar / conditional logistic regression stratified by instance.
- Every claim reports effect size + CI, not p alone. Pre-register the analysis plan (timestamped internal doc or OSF) before main runs.

---

## 3. Power analysis (exact computations, α=.05 two-sided, power=.80)

### 3.1 Unpaired two-proportion test — required n per cell

| Baseline p₁ | +15pp | +20pp | +25pp | +30pp |
|---|---|---|---|---|
| 0.30 | 160 | 90 | 57 | 39 |
| 0.50 | **167** | **90** | 55 | 36 |
| 0.70 | 118 | 59 | 32 | — |

### 3.2 Power actually achieved at n = 30/40/50 per cell (baseline p₁=0.5)

| True difference | n=30 | n=40 | n=50 |
|---|---|---|---|
| 15pp | 0.22 | 0.28 | 0.34 |
| 20pp | 0.37 | 0.46 | 0.55 |
| 25pp | 0.54 | 0.67 | 0.76 |
| 30pp | 0.73 | 0.84 | 0.91 |

**Direct answer to the assignment question:** at n=30–50/cell, unpaired binary containment-rate comparisons are adequately powered (≥.80) **only for effects ≥ ~28–30pp** (and only at n≥40–50). 15pp and 20pp effects are underpowered at every feasible n in this band. The F1 feasibility claim ("n=50 detects ~20pp") overstates power by ~25 points and must not be quoted in the proposal.

### 3.3 Instance-paired binary (McNemar) — required pairs

Within-instance correlation ρ arises because the same instance is run under both arms (shared difficulty). Realistic range ρ=0.3–0.5 (to be estimated in the pilot).

| Effect (p₁=0.5) | ρ=0.0 | ρ=0.3 | ρ=0.5 |
|---|---|---|---|
| 15pp | 174 | 125 | 91 |
| 20pp | 98 | 71 | 53 |
| 25pp | 63 | 46 | 36 |

Pairing brings 20pp within reach at I≈55–70 instances and 25pp at I≈40–46. **15pp remains out of reach** — do not promise it on a binary endpoint.

### 3.4 Continuous blast-radius fraction — required n per cell

| Effect size | Unpaired t | Paired (ρ=0.5) |
|---|---|---|
| d=0.5 (medium) | 63 | 31 |
| d=0.65 | 37 | 19 |
| d=0.8 (large) | 25 | 12 |

Prior effect magnitudes suggest large effects are plausible: Sentinel containment 46.2%→99.4% (simulation; ICERA 2026), hierarchical vs flat robustness gaps of 5.5 vs 23.7pp drop (arXiv:2408.00989), MAS-FIRE RS 6.3% vs 70.6% across models under Blind Trust (arXiv:2602.19843). **BR as a continuous co-primary endpoint is the statistical workhorse; the binary containment rate is the interpretable headline but the underpowered one.**

### 3.5 Interactions (difference-in-differences of proportions), n per cell

| Interaction magnitude | Example cells | n/cell |
|---|---|---|
| Large crossover, DiD=45pp | .50/.80 vs .50/.35 | 34 |
| Moderate, DiD=30pp | .50/.75 vs .50/.55 | 82 |
| Modest, DiD=20pp | .50/.70 vs .50/.50 | 188 |

Only **sign-reversal crossovers** are powered at feasible n. This shapes CAND-2 (its key prediction is exactly a crossover) and warns CAND-1 to treat structure×mechanism interactions as exploratory.

### 3.6 CAND-3 regression design

With 6 accuracy levels × 40 instances = 240 observations per policy arm, per-level proportion CIs are ±14–16pp, and a logistic-regression slope over the accuracy dial is well powered for moderate effects; the crossing-point (threshold) estimator uses all 240 obs/arm. Expected threshold CI width ≈ ±0.10–0.20 accuracy units if the guided and verify-everything curves are separated by ≥20pp at mid-range (to be confirmed by pilot-based simulation).

---

## 4. CAND-1 (OrgBlast) — statistical plan

**Research questions.** RQ1: does organizational structure determine blast radius of an injected local fault? RQ2: which containment mechanism minimizes blast radius while preserving task utility? RQ3 (exploratory): do mechanism rankings interact with structure/fault type?

### 4.1 Factors

| Factor | Levels | Role |
|---|---|---|
| Org structure S | flat chain; 3-tier hierarchy (frontline→supervisor→approver) | Primary IV (RQ1). Matrix/cross-functional deferred to extended study |
| Fault type F | 4 types, one per boundary cluster: hallucinated tool-call args (tool), stale/poisoned shared memory (memory), role/authority confusion via instruction fault (authority), corrupted inter-agent message (communication) | IV; down-scoped from MAS-FIRE's 15 per F1 descoping |
| Containment mechanism M | none; retry+verifier gate; checkpoint-rollback (LangGraph); quarantine+reroute; (optional 5th: simulated human escalation) | Primary IV (RQ2) |
| Injection site | mid-hierarchy role (fixed in main study; varied in a secondary sub-study) | Control |
| Workflow W | refund (tau2 retail adaptation) in core; IT-incident in extended | Blocking/generalization |

### 4.2 Design

**Within-instance full pairing on M:** each of I=40 instances is run under every mechanism arm with the same injected fault → 4–5 paired observations per instance per (S×F) cell. Core matrix: 2 S × 4 F × 4 M × 40 I = **1,280 runs** + 2 S × 40 fault-free baselines = 80 → **1,360 runs**. Extended (2nd workflow, human-escalation 5th arm): +~1,400.

### 4.3 Endpoints and hypotheses

- **Co-primary:** (i) BR (continuous, §2.2); (ii) containment rate C (binary). Gatekeeping: omnibus likelihood-ratio test of M in the GLMM first; then planned contrasts.
- **Secondary:** task success, utility-preservation ratio (success under fault+mechanism ÷ fault-free success), recovery cost (tokens, steps, human minutes), time-to-containment, collateral damage.
- Pre-registered directional hypotheses: H1: hierarchy reduces BR for communication/authority faults but not memory faults (memory bypasses hierarchy — the memory boundary is the classical-literature gap per E5); H2: quarantine+reroute ≥ rollback ≥ verifier ≥ none on C; H3: mechanism utility overhead ordering in no-fault cells (verifier cheapest, human escalation most expensive).

### 4.4 Analysis

- BR: beta-regression or LMM with random intercept per instance; fixed effects S, F, M + S×M (exploratory).
- C and success: GLMM (logistic), random intercept per instance; **primary family = 3 mechanism-vs-none contrasts, Holm-corrected**; same gatekeeping for BR.
- Structure effect (RQ1): contrast of S pooled over F, plus per-fault-type estimates with BH-FDR across the 4 fault types.
- Mechanism×structure and mechanism×fault interactions: exploratory, BH-FDR, effect sizes + CIs (powered only for crossovers per §3.5).
- Report pass^k from the reliability sub-study for the no-mechanism and best-mechanism arms.

### 4.5 What CAND-1 can and cannot claim at this n

- **Can:** mechanism differences ≥25pp on C (paired, I=40); d≥0.5 on BR (paired); structure main effects of similar magnitude; large crossover interactions.
- **Cannot:** 15–20pp mechanism differences on binary C; modest interactions; per-(S×F×M) cell estimates (32–40 cells × 40 instances = 1–2 obs/cell — cells are only estimable through the paired/mixed model, not as standalone proportions). State this explicitly in the paper to pre-empt reviewer miscounting.

---

## 5. CAND-2 (ClassicalTransfer) — statistical plan

**Framing:** pre-registered replication/falsification of Dellarocas & Klein ICMAS 2000 (DOI 10.1109/ICMAS.2000.858440) predictions on an LLM substrate. The inferential logic is **directional prediction + equivalence testing**, not null-hunting.

### 5.1 Pre-registered predictions (from the classical record, E5-verified)

- **P1 (unzippering):** completion-time inflation and BR increase monotonically with delegation depth. Classical magnitude: 600–700% of baseline at depth 4 — a huge effect, trivially powered if it transfers.
- **P2 (sentinel containment):** sentinel/EH-style handling ≪ survivalist timeout/retry on inflation and failure rate (classically ≤1–216% vs 600–700% inflation).
- **P3 (containment backfires under scarcity):** **crossover** — sentinel handling worse than survivalist with short tasks + scarce subcontractors. This is the signature non-obvious finding; its DiD is a sign reversal (≥40pp classically) → powered at n≈34/cell (§3.5).
- **P4 (new, exploratory):** fault class (crash vs semantic) moderates P1–P3 — 3-way interaction, underpowered by design; reported as effect sizes to generate the "where classical theory breaks" claims qualitatively.

### 5.2 Factors and matrix

depth {2-level, 4-level} × scarcity {abundant, scarce} × handling {none, survivalist-retry, sentinel} × fault class {crash/unresponsive agent, semantic (hallucinated handoff)} = 24 cells. **Core: 12 cells (crash) × 40 instances = 480 runs; semantic-fault transfer probe: 4 key cells × 40 = 160 runs → 640 total.**

### 5.3 Endpoints and tests

- Primary: task success (binary); completion-time/steps inflation ratio vs fault-free baseline (continuous); BR.
- P1: Jonckheere–Terpstra trend test + monotone contrast in LMM. P2: GLMM contrast sentinel vs survivalist. P3: handling×scarcity interaction contrast (DiD) with Newcombe CI.
- **Equivalence testing (TOST)** for any "prediction fails to transfer" claim: pre-register SESOI (smallest effect size of interest) = ±10pp on success, inflation ratio 1.25. Each prediction classified as: **replicated** (CI excludes null, predicted direction), **falsified** (equivalence bound met or reversal), or **inconclusive** (CI spans both) — inconclusive is an honest, reportable outcome and the likely fate of P4.
- Multiplicity: 3 confirmatory predictions, **Holm across P1–P3**; P4 and all semantic-fault analyses exploratory with BH-FDR.

### 5.4 Statistical risks specific to CAND-2

- The classical experiments are deterministic simulations with crash faults; LLM semantic faults add within-cell variance — the pilot must measure how much BR/inflation varies across seeds for semantic faults; if seed-ICC is high, raise I, not R.
- "Scarcity" must be operationalized deterministically (limited pool of qualified subcontractor agents/tools) or the crossover condition is not identifiable.
- Reviewer expectation management: the contribution is the **transfer map** (which predictions survive semantic faults), so null/equivalence results must be designed-in as publishable — hence TOST, hence pre-registration.

---

## 6. CAND-3 (AttribContain) — statistical plan

**RQ:** how accurate must attribution be before attribution-guided containment beats attribution-free containment? Derive the threshold empirically.

### 6.1 The key design move: accuracy as a controlled dial

Because faults are **injected**, attribution ground truth is perfect (we know the responsible agent/step) — sidestepping Who&When's annotation noise (53.5%/14.2% agent/step accuracy, arXiv:2505.00212). Attribution accuracy is then an **experimental dial**: guided-containment decisions are driven by a synthetic attributor mixing oracle attribution with uniform-random attribution at rates a ∈ {0.0, 0.2, 0.4, 0.6, 0.8, 1.0}. This converts "find attributors of every accuracy level" (impossible) into a controlled continuous IV.

### 6.2 Factors and matrix

- IV1: attribution accuracy a (6 levels, above).
- IV2: containment policy P ∈ {attribution-guided targeted (quarantine/rollback only the attributed agent/span), verify-everything (attribution-free), restart-all (attribution-free)}.
- Matrix: 6 a × 3 P × 40 instances = **720 runs** (guided policy varies over a; the two attribution-free policies are a-invariant but are run at all a levels to keep the design balanced and pairing clean — their variation across a estimates pure instance/seed noise, a free variance component).
- **Validation sub-study:** 2 real attributors (Who&When-style all-at-once prompting; a step-by-step variant) run on the same injected traces; their *measured* accuracy on our ground truth places them on the empirically derived curve → tests whether real systems sit on the right side of the threshold. +80–160 runs.

### 6.3 Endpoints

- Primary: task success; collateral-damage rate (healthy agents quarantined / healthy spans rolled back — deterministic from logs); total cost (tokens + tool calls).
- Secondary: BR, time-to-containment.

### 6.4 Analysis

- Per policy, logistic regression of success on a (continuous), random intercept per instance. **Primary estimand: threshold τ̂ = the a at which the guided-policy curve crosses the verify-everything curve** (and separately restart-all), with **bootstrap 95% CI resampling instances (2,000 reps)**.
- Secondary: same for collateral damage and cost (guided should dominate on collateral at high a; verify-everything on cost at low a — the crossing pattern is the paper's figure 1).
- Multiplicity: one primary estimand (τ̂ vs verify-everything); the τ̂ vs restart-all and cost/collateral crossings are secondary, Holm within the secondary family.
- Sensitivity: threshold re-estimated per fault type (exploratory, BH-FDR); check whether τ̂ depends on base attribution difficulty (long traces per LongRCA, arXiv:2608.15242).

### 6.5 Power note

The regression design is the most statistically efficient of the three candidates: 240 obs/policy arm, no cell-sparsity, threshold CI ≈ ±0.10–0.20 accuracy units under plausible curve separations (§3.6). The binding risk is not power but **curve separation**: if guided containment only beats verify-everything by <15pp at a=1.0, the threshold exists but the practical claim weakens — pilot must estimate the a=1.0 gap first.

---

## 7. Minimum viable experiment matrix (all candidates, shared testbed)

| Candidate | Core cells | Instances | Runs | Marginal cost (GPT-5-mini class, F1 pricing) |
|---|---|---|---|---|
| Shared build | tau2-substrate org wrapper, injection layer, provenance logging | — | — | 3.5–5 person-weeks (F1 descoped estimate) |
| CAND-1 core | 2 S × 4 F × 4 M | 40 | 1,280 + 80 baselines | ~$110 |
| CAND-2 core | 2 depth × 2 scarcity × 3 handling (crash) + 4 semantic probe cells | 40 | 480 + 160 | ~$50 |
| CAND-3 core | 6 a × 3 P | 40 | 720 + ~120 validation | ~$65 |
| Reliability sub-study | 10 instances × 8 seeds, key cells | 10 | ~240 | ~$20 |
| Pilot | 10 instances × 5 seeds, cell subset | 10 | ~300 | ~$25 |
| **Total** | | | **≈3,400** | **≈$270 (GPT-5-mini); ≈$165 DeepSeek; ≈$1,300 GPT-5** |

**Descope ladder (if engineering slips, cut in this order):** (1) CAND-1 5th mechanism arm (human escalation → simulated-only, −320 runs); (2) CAND-2 semantic probe cells (−160); (3) CAND-3 restart-all policy (−240); (4) CAND-1 fault types 4→3 (−320). **Never cut instances below 40 or merge pairing** — that destroys the power that makes any of this publishable. Floor: CAND-1 alone at 1,360 runs is a complete workshop paper.

---

## 8. Multiple-comparison policy (summary)

| Family | Contents | Correction |
|---|---|---|
| CAND-1 primary | 3–4 mechanism-vs-none contrasts on C (and gated BR) | Omnibus LR gate → Holm |
| CAND-1 secondary | utility, cost, time-to-containment, collateral | Holm within family |
| CAND-1 exploratory | S×M, M×F interactions, per-fault-type structure effects | BH-FDR |
| CAND-2 confirmatory | P1, P2, P3 | Holm across 3 predictions |
| CAND-2 exploratory | P4, semantic-fault transfer | BH-FDR |
| CAND-3 primary | τ̂ (guided vs verify-everything) | Single estimand, bootstrap CI |
| CAND-3 secondary | τ̂ vs restart-all; cost/collateral crossings | Holm |

Pre-registration before main runs; any analysis not in the pre-registration is labeled exploratory in the paper.

---

## 9. Threats to validity and mitigations

1. **Untriggered faults** bias effects toward zero → trigger verification + triggered-only primary analysis (AgentChaos lesson).
2. **Instance overfitting** (40 instances from one workflow) → compositional task generation (τ² generator, F1-verified) to widen the instance pool; second workflow in extended matrix; workflow as random effect where estimable.
3. **Judge validity** for the one judged DV → κ gate + 10% human audit (§2.3); primary endpoints never judged.
4. **Model dependence** → two backbone blocks; no cross-model pooling without interaction check; MAS-FIRE's finding that robustness rankings flip across models (RS 6.3% vs 70.6%) means single-model claims must be explicitly scoped.
5. **Simulated human** in the escalation arm → stated limitation; sensitivity over human error rates {1.0, 0.8, 0.6}.
6. **Multiple-comparison creep** across three candidates sharing infrastructure → the family table in §8 is pre-registered; exploratory screens FDR-controlled.
7. **Seed non-reproducibility** (provider-side nondeterminism even at temperature 0) → treat runs as stochastic regardless; log everything; reliability sub-study quantifies it via pass^k.

---

## 10. Verification log

- All literature facts (effect magnitudes, substrate properties, pricing, attribution accuracies, classical predictions) are taken from the wave-1 reports listed above, which verified them against primary sources on 21 Sep 2026; no new external citations are introduced in this report.
- τ-bench abstract re-fetched (arXiv:2406.12045) to confirm pass^k / DB-state evaluation pattern; tau2-bench repo README re-fetched (domains, v1.0.1 grading caveat — **pin tau2-bench ≥1.0.1 for the banking_knowledge fix; results from older versions are not comparable**).
- All power numbers computed exactly (standard two-proportion, McNemar discordant-pair, t-test, and DiD formulas; z_{.975}=1.96, z_{.80}=0.842) via script on 21 Sep 2026; tables in §3 are reproducible from the formulas shown.
- Exact usable instance counts per tau2 domain (retail/telecom task files) to be confirmed at build time; the plan requires ≥40 usable instances per workflow, which the F1-verified compositional generator can guarantee regardless.
