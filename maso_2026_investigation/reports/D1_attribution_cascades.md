# D1 — Failure Attribution & Error-Cascade Papers: Verification and Positioning Report

**Investigator:** D1 (attribution/cascades specialist)
**Date:** 2026-09-21
**Mission:** Verify and position four mandatory papers (Who&When, CHIEF, DCFA, From Spark to Fire); map 2026 extensions; adversarially assess whether any of them kill or subsume the seed hypothesis ("organizational failure propagation and recovery in LLM MAS — organizational blast radius + containment/recovery mechanisms").
**Verification methods:** arXiv abstract pages fetched directly (arxiv.org/abs/...), Google Scholar result pages, PMLR v267 proceedings listing, prior sweep raw data in `maso_2026_investigation/raw/c3_s2_hits.json` (Semantic Scholar dumps). Semantic Scholar live API, arXiv export API, DBLP, OpenAlex, and IEEE Xplore were rate-limited/bot-blocked from this IP during the investigation window; every paper recorded below was verified against at least one primary page (arXiv abs, PMLR, or Scholar cluster snippet quoting the abstract). Items verified only via secondary snippets are explicitly flagged.

---

## 1. Bottom-line judgment

**None of the four mandatory papers kills or subsumes the seed hypothesis.** Who&When, CHIEF, and DCFA are *post-hoc attribution* works: they localize a single "decisive error" after a run has failed. They do not model spread, do not propose containment or recovery mechanisms, and do not touch organizational boundaries. "From Spark to Fire" does model propagation and does propose a message-layer containment mechanism, but its spread construct is a binary "final infection" on a message-dependency graph — not a multi-dimensional organizational blast radius — and it does no recovery and no boundary-type analysis.

**The most dangerous partial overlap found is NOT in the mandatory set:** OrchestraBench (arXiv:2608.05263) already uses "cascade radius" and per-failure-mode recovery as *primary metrics* with a failure-injection harness, and "Containing the Cascade" (IEEE ICERA 2026) benchmarks a reference mediator for failure propagation with propagation metrics (e.g., mean time-to-detection). These narrow the novelty surface: the seed must differentiate on (a) organizational boundary constructs (role, authority, memory, accountability, human-agent), (b) realistic task utility preservation, and (c) richer workflows than controlled chains. See §5.

---

## 2. Mandatory papers — full structured records

### 2.1 Who&When — "Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems"

| Field | Value |
|---|---|
| arXiv ID | 2505.00212 (v1 2025-04-30; v3 2025-06-02, "camera-ready") |
| Venue | **ICML 2025** — verified in PMLR v267, pp. 76583–76599 (proceedings.mlr.press/v267) |
| Authors | Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu, Zhiguang Han, Jingyang Zhang, Beibin Li, Chi Wang, Huazheng Wang, Yiran Chen, Qingyun Wu |
| URL | https://arxiv.org/abs/2505.00212 |
| Citations | 228 (Google Scholar, 2026-09-21) |
| Research problem | Formulates automated failure attribution for LLM MAS: given a failed trajectory, identify the failure-responsible **agent** (who) and the **decisive error step** (when). |
| Method | Introduces the Who&When dataset; evaluates three method families: all-at-once prompting, step-by-step probing, binary-search-style attribution. |
| Experimental setting | 127 failure logs from LLM MAS (both hand-crafted and algorithm-generated systems), fine-grained human annotations linking failures to agents/steps. |
| Datasets/benchmarks | Who&When dataset (released). |
| Metrics | Agent-level accuracy; step-level accuracy. |
| Major findings | Best method: 53.5% agent identification, only 14.2% step pinpointing; some methods below random; OpenAI o1 and DeepSeek R1 not practically usable at the task. |
| Author-stated limitations | Task complexity high; current methods far from practical usability. |
| My inferred limitations | Post-hoc only; single decisive-error assumption (distributed causation out of scope — see "One Reflex, Two Answers", §4.3, showing judges weakly discriminate localized vs distributed causes); no propagation dynamics; no intervention. |
| Code availability | Yes — code and dataset released (link on arXiv page). |
| Relation to seed hypothesis | **Complementary infrastructure, not a competitor.** Provides the ground-truth labeling methodology and the de facto benchmark that the whole 2026 attribution ecosystem builds on. Contains zero containment/recovery/spread-metric content. |

**What it does NOT do (seed-relevant):** no containment; no recovery; no spread/blast-radius metrics (output is a single (agent, step) pair, not a set of affected components); no organizational boundary constructs (role/authority/memory/accountability/human-agent never operationalized); no task-utility-preservation analysis.

### 2.2 CHIEF — "From Flat Logs to Causal Graphs: Hierarchical Failure Attribution for LLM-based Multi-Agent Systems"

| Field | Value |
|---|---|
| arXiv ID | 2602.23701 (v1 2026-02-27) |
| Venue | arXiv preprint (cs.AI, cs.SE); no venue indicated on abs page |
| Authors | Yawen Wang, Wenjie Wu, Junjie Wang, Qing Wang |
| URL | https://arxiv.org/abs/2602.23701 |
| Research problem | Failure attribution treating execution logs as *flat sequences* fails to disentangle causal links → weak observability, ambiguous responsibility boundaries. |
| Method | CHIEF: (1) transform trajectories into a structured **hierarchical causal graph**; (2) hierarchical oracle-guided backtracking with synthesized virtual oracles to prune search; (3) **counterfactual attribution** via progressive causal screening to separate true root causes from *propagated symptoms*. |
| Experimental setting | Who&When benchmark, 8 strong/SOTA baselines; ablations. |
| Metrics | Agent-level and step-level attribution accuracy. |
| Major findings | Outperforms all 8 baselines at both levels; each module contributes (ablations). |
| Author-stated limitations | Not stated on abs page. |
| My inferred limitations | Depends on synthesized virtual oracles (quality ceiling); evaluated only on Who&When; "propagated symptoms" are filtered out as noise for attribution — the propagation itself is never measured or used. |
| Code availability | Not indicated on abs page. |
| Relation to seed hypothesis | Acknowledges propagation exists (root cause vs propagated symptom distinction) but weaponizes it only for attribution accuracy. **No spread quantification, no containment, no recovery, no organizational boundaries.** |

### 2.3 DCFA — "Dual-view Causal-inspired Attribution for Failure Reasoning in LLM-based Multi-agent Systems"

| Field | Value |
|---|---|
| arXiv ID | 2609.04749 (v1 2026-09-04) |
| Venue | arXiv preprint (cs.AI) |
| Authors | Zehao Wang, L. Wang, S. Jin, J. Chen, Y. Xiao (per Scholar cluster; abs page submission by Zehao Wang) |
| URL | https://arxiv.org/abs/2609.04749 |
| Research problem | Two failure modes of attribution: (1) *shallow attribution* — methods latch onto minor correctable deviations (bad retrieval, formatting) instead of the decisive cause; (2) *contextual degradation* — reasoning deteriorates on long traces. |
| Method | Training-free dual-view framework: global module builds structured causal-inspired dependency graphs from traces to find the initial decisive error (defined as earliest action whose correction reverses system failure); local module applies counterfactual-inspired reasoning to refine. |
| Experimental setting | Who&When benchmark, six LLMs. |
| Metrics | Step-level (and agent-level) attribution accuracy. |
| Major findings | Up to +8.27% step-level accuracy over SOTA baselines. |
| Author-stated limitations | Implicit: still benchmark-bound; decisive-error framing assumes a single earliest correctable action. |
| My inferred limitations | "Causal-inspired" ≠ interventional causality; no validation that fixing the attributed step actually reverses failure at scale; post-hoc; no propagation measurement. |
| Code availability | Not indicated on abs page. |
| Relation to seed hypothesis | Same post-hoc attribution paradigm as Who&When/CHIEF. **No containment, no recovery, no spread metrics, no organizational boundaries.** Very recent (Sept 2026) — signals the attribution subfield is still actively publishing; a MASO submission must cite it as SOTA. |

### 2.4 From Spark to Fire — "Modeling and Mitigating Error Cascades in LLM-Based Multi-Agent Collaboration"

| Field | Value |
|---|---|
| arXiv ID | 2603.04474 (v1 2026-03-04; v2 2026-05-11) |
| Venue | arXiv preprint (cs.MA, cs.AI) |
| Authors | YiZhe Xie, C. Zhu, X. Zhang, T. Zhu, D. Ye, M. Qi, et al. (first author verified via arXiv submission history; rest via Scholar cluster) |
| URL | https://arxiv.org/abs/2603.04474 |
| Citations | 24 (Google Scholar, 2026-09-21) |
| Research problem | Minor inaccuracies solidify into system-level **false consensus** through iteration; errors propagate and amplify through message dependencies; existing protections need single-agent validation or architecture modification. |
| Method | (1) **Propagation dynamics model**: collaboration abstracted as directed dependency graph; early-stage risk criterion for amplification risk. (2) Identifies three vulnerability classes: **cascade amplification, topological sensitivity, consensus inertia**. (3) Instantiates an attack: one atomic error seed → widespread failure. (4) **Genealogy-graph-based governance layer** as a message-layer plugin suppressing endogenous and exogenous error amplification without altering collaboration architecture. |
| Experimental setting | Six mainstream MAS frameworks; attack + defense evaluation across operating modes. |
| Metrics | Final-infection prevention rate; cascade spread mitigation. |
| Major findings | Governance layer prevents final infection in ≥89% of runs across operating modes; significantly mitigates cascading spread of minor errors. |
| Author-stated limitations | Protection must not weaken effective information flow (design constraint they claim to respect). |
| My inferred limitations | "Infection" is essentially a binary/endpoint outcome, not a graded multi-dimensional blast radius; no recovery-after-failure (the layer prevents spread, it does not repair); no organizational boundary semantics (roles, authority, memory, accountability, human-agent handoffs absent); message-layer only — tool/memory boundaries out of scope; task-utility cost of suppression not deeply quantified. |
| Code availability | Not indicated on abs page. |
| Relation to seed hypothesis | **Closest mandatory paper to the seed: it does propagation modeling + containment.** But its containment is a single mechanism class (message genealogy gating), its spread metric is infection-style, and recovery + organizational boundaries are absent. The seed survives but MUST cite and differentiate from this paper. |

---

## 3. 2026 papers citing/extending the mandatory set (verified)

All attribution extensions below evaluate on Who&When (hence cite it). Verified via arXiv abs pages unless noted.

| Paper | ID / Venue | Date | Core idea | Seed-relevant gaps |
|---|---|---|---|---|
| AgenTracer — "Who is Inducing Failure in the LLM Agentic Systems" | arXiv:2509.03312; **ICLR 2026** (proceedings.iclr.cc); 99 Scholar cites | 2025-09 → 2026 | Counterfactual + injected training traces; trains lightweight AgenTracer-8B attributor; beats giant models on Who&When | Post-hoc attribution only |
| "Who is introducing the failure? … via spectrum analysis" (Spectrum-Based Failure Attribution) | arXiv:2509.13782; PACMSE, DOI 10.1145/3797113; 37 cites | 2025-09 / 2026-06 | Spectrum-based fault localization (classic SE technique) applied to MAS | Attribution only; no spread model |
| StepFinder | arXiv:2606.03467; **KDD 2026** | 2026-06 | Lightweight temporal-semantic framework; step-level root cause; 79% inference-time reduction vs fastest LLM baseline; code released | Attribution only |
| ASCon | arXiv:2608.10646 | 2026-08 | Direction-aware reciprocal agent–step contextualization; unified reps for who/when/why targets; +5.83% agent, +10.63% step micro-acc, +14.73% failure-mode Macro-F1 | Adds failure-*mode* detection; still post-hoc |
| AFANet — "Beyond LLM-Based Reasoning: Lightweight GNNs for Agent Failure Attribution" | arXiv:2608.18575 | 2026-08 | Lightweight GNN over step semantics + agent relations; matches/beats LLM baselines at near-zero inference cost; OOD test-time adaptation | Attribution only |
| Adaptive Influence Graphs (AIG) | arXiv:2608.24361 | 2026-08 | Two-stage agentic framework: trace → structured influence graph → agent-directed traversal; new SOTA on Who&When (authors: Y. Bakish, A. Dudai, R. Ganz, O. Nuriel) | Attribution only |
| DUOTRACE — "Detect Before You Attribute: Cascade Failure Attribution for MAS" | arXiv:2608.29646 | 2026-08 | Plug-and-play VAE anomaly-detection filter (Tree-LSTM trajectory encoder, dual-view node reps, augmentation) feeding LLM attributors; +8.7% agent / +7.0% step | Detection+attribution pipeline; "cascade" in title but no propagation metrics/containment |
| Who&When Pro | arXiv:2607.09996 | 2026-07 | 12,326 controlled-injection trajectories (replay successful prefix, then inject failure), 3 modalities, 26 benchmarks; systematic attribution patterns | Benchmark scale-up of Who&When; controlled injection methodology directly reusable by seed |
| AgentDebugX | arXiv:2607.18754; 4 cites | 2026-07 | Open-source closed loop **Detect–Attribute–Recover–Rerun**; DeepDebug multi-turn root-cause diagnosis; 28.8% strict agent+step accuracy (qwen3.5-9b); on GAIA repairs 13/73 failed tasks in one rerun (55.8%→63.6%) | **Only verified paper linking attribution to recovery** — but recovery = diagnose-and-rerun single episodes; no spread metrics, no organizational boundaries, no containment of in-flight propagation |
| AgentForesight | arXiv:2605.08715; 15 cites | 2026-05 | **Online auditing**: auditor sees only trace prefix, must alarm at earliest decisive error; AFTraj-2K corpus; AgentForesight-7B (RL, coarse-to-fine); +19.9% vs GPT-4.1, 3× lower step localization error; external eval on Who&When | Shifts attribution to *online* (enables intervention) but stops at alarming — no containment/recovery mechanism |
| CatchBench — "When Can an Agent Failure Be Caught?" | arXiv:2608.22808 (v4 2026-09-17) | 2026-08 | One auditor question across PRE/LIVE/POST information states; 7 task contracts; 72 entrants, 9 model families, 1187 configs / 1162 runs; adversarial self-audit of benchmark shortcuts | Detectability framing; no containment/recovery |
| "Finding Where the Buck Stops" (attribution-based reflection) | arXiv 2026 (ID unverified; Scholar snippet) | 2026 | Uses automated failure attribution to drive MAS self-reflection | Attribution→reflection link; details unverified |
| "Towards self-improving error diagnosis in MAS" | ACL Findings 2026 (aclanthology.org; snippet-verified) | 2026 | Self-improving error diagnosis | Attribution only |
| TRAJDEBUG — tracing error lifecycle in long-horizon agent trajectories | arXiv 2026 (ID unverified; Scholar snippet); 2 cites | 2026 | Critical error detection in long-horizon trajectories | Single-agent long-horizon focus |

**Ecosystem observation:** the Who&When attribution lineage is crowded and fast-moving (≥10 extensions in 2026 alone, incl. ICLR/KDD/ASE acceptances). The seed hypothesis should NOT frame itself as "attribution" — that space is saturated. Its defensible core is *spread + containment + recovery across organizational boundaries*, which none of these touch.

---

## 4. Adjacent cascade / propagation / containment literature (verified)

### 4.1 Highest threat to seed novelty

| Paper | ID / Venue | What it does | Why it threatens the seed | Why it does NOT subsume the seed |
|---|---|---|---|---|
| **OrchestraBench** | arXiv:2608.05263 (2026-08-05) | Failure-injection harness over templated enterprise workflows; **"cascade radius" and per-failure-mode recovery as primary metrics**; routing-policy comparison w/ bootstrap CIs; mechanism probes with real Claude agent over verifiable arithmetic chain; 5 MAST modes; recovery tiers: tool faults 1.0, ambiguous delegation 0.30, latent/semantic 0.0; blind retry reproduces latent faults; cascade radius grows with depth (0.9→4.7, depths 3–7); trusted-state repair ablation | **Already operationalizes a blast-radius-like metric + recovery tiers + "detection and attribution are necessary for containment" claim.** Closest verified work to the seed. | Self-declared "controlled-chain mechanism probes, not domain-workload claims"; 26-case diagnostic; no organizational boundary constructs (role/authority/memory/accountability/human-agent); single verifiable-computation domain; no containment mechanism design (only measurement) |
| **Containing the Cascade** | IEEE ICERA 2026, DOI 10.1109/ICERA72709.2026.11666599 (V.R. Divi, S. Gullapalli) | Benchmark + **SENTINEL reference mediator** for failure propagation in tool-using LLM MAS; propagation metrics incl. **mean time-to-detection**; MAS failure statistics (Scholar snippet; IEEE page bot-blocked) | Directly benchmarks *containment* of failure propagation | Appears to be a short conf. paper; tool-using focus only; no organizational boundaries; details unverifiable from here — **follow-up: obtain full text** |
| From Spark to Fire | arXiv:2603.04474 | See §2.4 — propagation dynamics + genealogy-graph message-layer governance, ≥89% infection prevention | Mandatory paper; does containment | See §2.4 gaps |

### 4.2 Propagation dynamics / spread measurement (no containment or recovery)

| Paper | ID / Venue | Contribution | Gap vs seed |
|---|---|---|---|
| Hallucination Snowball | arXiv:2608.14588; **ICML 2026 FAGEN workshop** | Markov model of error transformation (Raw→Derived→Narrative→Invisible); per-boundary escape probabilities 24.6%/48.3%/89.3%; 346 injected hallucinations, 4-agent FinanceBench pipeline; **boundary gates cut survival 58.4%→16.2% vs end-checking; "when you verify matters more than whether"** | Linear pipeline, hallucination-only, one domain; no organizational boundaries; verification placement ≠ general containment |
| Hallucination Cascade | arXiv:2606.07937; 7 cites | 500 cascade experiments, 10 domains, GPT-5.3/DeepSeek-V3/LLaMA-3-70B; claim-level tracking; finds net *attenuation* (amplification factor 0.644) in 3-agent chains; hallucination–accuracy trade-off | Measurement only; chains only; no containment/recovery |
| QUIVER | arXiv:2605.23956 | Formal framework: sensitivity matrix (amplifier/absorber/threshold edges), trajectory divergence decomposition, bifurcation thresholds, distribution faithfulness; 8,200+ traces on 2 production enterprise pipelines + DSPy | Strong formalism for spread; zero organizational semantics; no recovery |
| PropUQ-MAS | arXiv:2608.22130 | Propagation-aware uncertainty quantification for LLM MAS | UQ only |
| Semantic Register Compression | arXiv:2607.14119 | Representational risk when intermediate agents transform content | Measurement only |
| "When Agents Call Agents: Failure Propagation Patterns in Multi-Model Agentic Pipelines" | SSRN 7234438 (2026) | Failure propagation patterns across model changes in pipelines (snippet-verified) | Grey literature; patterns only |
| "When Language-Model Errors Become Action Errors" (scoping review) | journal.uob.edu.bh, 2026 (N. Zamindar) | Systematic scoping review of error propagation in agentic AI; notes corpus cannot estimate cascade prevalence in deployed systems | Review; confirms field immaturity |
| Misinformation Propagation in Benign Multi-Agent Systems | arXiv:2606.16710 | Misinformation spread without adversaries | Misinformation-specific |

### 4.3 Detection / injection infrastructure (enabling tech for the seed)

| Paper | ID / Venue | Contribution |
|---|---|---|
| AgentChaos | arXiv:2608.06790; **ASE 2026** | Runtime non-intrusive LLM-API fault injection (crash/omission/value faults on content & tool-call fields); 65 fault configs; pass@1 drops up to 50pp; robustness depends on system implementation, not model; existing diagnosis <53% fault-type / <56% fault-step accuracy |
| CatchBench | arXiv:2608.22808 | PRE/LIVE/POST catchability benchmark (§3) |
| AgentForesight | arXiv:2605.08715 | Online early-warning auditor (§3) |
| "One Reflex, Two Answers: Model Judges Weakly Discriminate Localized from Distributed Causes in Agent Failure Attribution" | MDPI MAKE 8(9):275, DOI 10.3390/make8090275 (2026-09-08) | **Directly relevant caveat:** model judges struggle exactly where the seed lives — distributed causation across components (snippet + S2 metadata; MDPI page bot-blocked) |
| CASPIAN — online detection/attribution of *cascade attacks* via cross-channel causal monitoring | arXiv 2026 (K. Venkatesh, J. Isbarov, S. Amin, M. Kantarcioglu; 4 cites; ID unverified — Scholar snippet only) | Adversarial cascade detection; security framing |
| SoK: "When Safe Agents Fail Together: The Security of Multi Agent LLM Systems" | arXiv 2026 (R. Yang et al.; ID unverified) | Security SoK; explicitly notes MAS "move information, state, decisions, and **authority across principal boundaries**, creating failures that local checks may miss" — closest rhetorical match to "organizational blast radius", but security/attack-focused |
| "Compound AI System Reliability: A Failure Taxonomy and Resilience Pattern Catalog from 150 Production Incidents" | OpenReview, 2nd Workshop on Agents in the Wild (2026) | Failure taxonomy + resilience patterns from production incidents; cascading errors at component boundaries |
| "Characterizing faults in agentic AI: A taxonomy of types, symptoms, and root causes" | arXiv 2026; 21 cites | Fault taxonomy for agentic AI |

---

## 5. Does anything here kill or subsume the seed hypothesis?

**No kill. Two partial overlaps that constrain framing:**

1. **OrchestraBench (arXiv:2608.05263)** — occupies "cascade radius + recovery metrics + failure injection" as *measurement* territory, but explicitly limited to controlled mechanism probes, with no organizational boundary constructs and no containment mechanism design. The seed must cite it and claim the organizational-boundary generalization + containment/recovery mechanism design as its contribution.
2. **From Spark to Fire (arXiv:2603.04474)** + **Containing the Cascade (IEEE ICERA 2026)** — occupy "message-layer/tool-layer propagation containment" with infection-style or detection-latency metrics. Neither does recovery, multi-boundary blast radius, or utility-preservation trade-offs.

**What remains genuinely open for the seed (supported by this sweep):**
- No verified paper operationalizes failure spread across *organizational* boundary types (role, communication, authority/delegation, tool, memory, accountability, human-agent) — the closest rhetorical match is a security SoK (§4.3).
- No verified paper studies *recovery* beyond diagnose-and-rerun (AgentDebugX) or measures recovery per failure mode beyond OrchestraBench's controlled chains.
- No verified paper couples containment mechanisms to task-utility preservation (Spark-to-Fire gestures at information-flow preservation; Hallucination Snowball quantifies a verification-placement trade-off in one linear domain).
- The attribution ecosystem (Who&When → AgenTracer/CHIEF/DCFA/AIG/ASCon/StepFinder/DUOTRACE/AgentForesight) supplies mature ground-truth methodology and benchmarks the seed can build on rather than compete with.

**Risks to monitor:** Who&When Pro's controlled-injection pipeline (12,326 trajectories) could be extended to spread measurement by others quickly; the FAGEN/Agents-in-the-Wild workshop circuit is actively publishing adjacent work; DCFA (Sept 2026) shows the attribution line is still moving.

---

## 6. Verification gaps / follow-ups

- CASPIAN, "Finding Where the Buck Stops", TRAJDEBUG, SoK "When Safe Agents Fail Together": arXiv IDs unverified (Scholar snippets only; APIs rate-limited). Follow up when Semantic Scholar/arXiv API access recovers.
- "Containing the Cascade" (IEEE ICERA 2026): full text not obtained (IEEE Xplore bot-blocked). Its SENTINEL mediator and propagation metric definitions need direct inspection — highest-priority follow-up.
- Citation counts are Google Scholar snapshots as of 2026-09-21.
- MDPI "One Reflex, Two Answers": abstract-level verification only (bot-blocked full text).
