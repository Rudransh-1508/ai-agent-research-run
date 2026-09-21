# LANDSCAPE B3 — Failure Attribution and Debugging in LLM Multi-Agent Systems

**Investigator:** B3 specialist (adversarial evidence-gathering)
**Date:** 2026-09-21
**Mission context:** Test the seed hypothesis "organizational failure propagation and recovery in LLM MAS" (organizational blast radius across role / communication / authority / tool / memory / accountability / human-agent boundaries; containment & recovery mechanisms). This report maps automated failure attribution and debugging, and asks specifically: **does attribution work connect to containment/recovery, or stop at localization?**

**Method note:** All papers below were verified by fetching the actual arXiv abstract page (arxiv.org/abs/<id>), the Semantic Scholar API, or OpenReview — not search snippets. arXiv IDs and dates are taken from the pages themselves. Two non-arXiv papers were verified via Semantic Scholar match API (DOIs recorded). Classical distributed-systems references at the end are cited from established knowledge (DBLP was bot-blocked at investigation time); they are flagged as such.

---

## 1. Bottom line

1. **Failure attribution in LLM MAS is a crowded, fast-moving area (50+ papers May 2025 – Sep 2026), but it is NOT solved.** Best step-level accuracy on the standard Who&When benchmark has moved from ~14% (Who&When paper, May 2025) to roughly 30–50% depending on method and subset; on long-horizon traces (LongRCA, median 145 steps) the best exact root-step accuracy is 24.1%. Agent-level attribution is easier (~50–70%+). Multiple 2026 papers show the single-root-cause assumption itself is shaky (MP-Bench, DoVer, GCJR).
2. **The overwhelming majority of attribution work stops at localization.** A 2026 wave (DoCtOR, MARS, FlowFixer, CausalFlow, AgentTether, RESKILL, DoVer, Conformal rollback, MASC) does connect attribution/diagnosis to *repair* — but "repair" means fixing the failed task trajectory (reflection, re-execution, patch, rollback), not *containing propagation across organizational boundaries*.
3. **Two papers partially subsume the seed's framing and must be addressed head-on:**
   - **"Containing the Cascade" (ICERA 2026, DOI 10.1109/ICERA72709.2026.11666599)** already uses the exact term **"blast radius"** plus containment rate, cascade depth, MTTD, and a Sentinel mediator (typed message contracts, anomaly gate, circuit breaker, checkpoint recovery). *But* it is a discrete-event **simulation** calibrated to published failure statistics — no real LLM MAS executions — at a low-tier venue. Novelty threat on terminology; defensible gap on ecological validity and organizational boundaries.
   - **"From Spark to Fire" (arXiv:2603.04474)** models error-cascade propagation dynamics in LLM-MAS and deploys a governance layer that suppresses amplification (≥89% prevention). Closest real-LLM-MAS work to the seed, but operates at the message-dependency level only — no role/authority/memory/accountability boundaries.
4. **The attribution→containment link is the clearest open gap.** Attribution outputs (who/when/why) are not consumed by containment mechanisms; containment mechanisms (circuit breakers, corrector placement, anomaly gates) do not use attribution. Nobody measures whether better attribution yields smaller blast radius. Nobody studies propagation across *organizational* boundaries (delegation authority, shared memory, accountability, human-agent handoffs).

---

## 2. The assigned core papers (verified)

### 2.1 Who&When — the task-defining paper

| Field | Value |
|---|---|
| Title | Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems |
| Authors | Shaokun Zhang, Ming Yin, Jieyu Zhang, Jiale Liu, Zhiguang Han, Jingyang Zhang, Beibin Li, Chi Wang, Huazheng Wang, Yiran Chen, Qingyun Wu |
| ID | arXiv:2505.00212 (v1 30 Apr 2025; v3 2 Jun 2025, "camera-ready" per arXiv comment; widely cited as ICML 2025) |
| Problem | Formulates automated failure attribution: given a failed MAS trajectory, identify the failure-responsible **agent** and the **decisive error step** |
| Data | Who&When dataset: failure logs from 127 LLM MAS, fine-grained annotations; two subsets (algorithm-generated, hand-crafted) |
| Methods | Three families: all-at-once prompting, step-by-step, binary search; plus fine-tuned variants |
| Findings | Best method: 53.5% agent-level accuracy, **only 14.2% step-level**; some methods below random; o1 and DeepSeek-R1 not practically usable |
| Limitations (stated/inferred) | Single decisive-error assumption; partial observability (agent outputs only, per TraceElephant's later critique); hand-crafted subset small |
| Code | Publicly released (link on arXiv page) |
| Relation to seed | Defines localization only. Explicitly frames attribution as "clues for systems debugging" — debugging left as future work. The seed's containment question starts where this stops. |

### 2.2 CHIEF — hierarchical causal-graph attribution

| Field | Value |
|---|---|
| Title | From Flat Logs to Causal Graphs: Hierarchical Failure Attribution for LLM-based Multi-Agent Systems |
| Authors | Wenjie Wu et al. (first author per submission history) |
| ID | arXiv:2602.23701 (v1 27 Feb 2026), cs.AI/cs.SE |
| Method | CHIEF: transforms trajectories into a **hierarchical causal graph**; hierarchical oracle-guided backtracking with synthesized virtual oracles to prune search; **counterfactual attribution** via progressive causal screening to separate root causes from propagated symptoms |
| Evaluation | Who&When benchmark; beats 8 baselines at agent- and step-level; ablations per module |
| Limitations | Still post-hoc, single-failure localization; counterfactuals are screening heuristics over the log, not executed interventions; no recovery action |
| Relation to seed | Explicitly distinguishes "true root causes from propagated symptoms" — acknowledges propagation but only to *discount* it for attribution, not to measure or contain it |

### 2.3 DCFA — dual-view causal-inspired attribution

| Field | Value |
|---|---|
| Title | DCFA: Dual-view Causal-inspired Attribution for Failure Reasoning in LLM-based Multi-agent Systems |
| Authors | Zehao Wang et al. |
| ID | arXiv:2609.04749 (v1 4 Sep 2026), cs.AI |
| Method | Training-free. Global module: structured causal-inspired dependency graph from traces to find the **initial decisive error** (defined as earliest action whose correction reverses failure). Local module: counterfactual-inspired reasoning to refine |
| Problems addressed | "Shallow attribution" (methods latch onto minor correctable deviations) and "contextual degradation" (long traces) |
| Evaluation | Who&When, six LLMs; step-level +8.27% over SOTA baselines |
| Limitations | "Causal-inspired" — no actual interventions; localization only; gains are incremental |
| Relation to seed | Same as CHIEF: propagation treated as noise for attribution, not as the object of study |

---

## 3. Benchmarks and datasets (verified)

| Benchmark | ID | Date | Size / scope | What it measures |
|---|---|---|---|---|
| Who&When | 2505.00212 | Apr 2025 | 127 MAS failure logs | Agent + decisive-step attribution |
| TRAIL | 2505.08638 | May 2025 | 148 human-annotated traces (single+multi-agent, SWE & IR) | Trace debugging w/ error taxonomy; best Gemini-2.5-pro = 11% |
| MAST-Data | 2503.13657 | Mar 2025 | 1600+ annotated traces, 7 frameworks | 14 failure modes in 3 categories (taxonomy, not attribution per se) |
| Aegis-Bench | 2509.14295 | Sep 2025 | 9,533 trajectories w/ injected errors | Faulty-agent + error-mode attribution; SFT/RL/contrastive training |
| TracerTraj | 2509.03312 | Sep 2025 | counterfactual-replay-annotated failed trajectories | Training resource for AgenTracer-8B |
| CORRECT-Error | 2509.24088 | Sep 2025 | 2,000+ annotated trajectories | Step-level error localization |
| TraceElephant | 2604.22708 | Apr 2026 (ACL 2026) | full-execution-trace benchmark w/ reproducible environments | Full vs partial observability: full traces improve attribution up to 76% |
| LongRCA Bench | 2608.15242 | Aug 2026 | 1,140 failed trajectories, 5 domains, median 145 steps, no injected errors | Responsible-role vs exact root-step; best root-step = 24.1% (RCTA) |
| MP-Bench | 2603.25001 | Mar 2026 | multi-perspective attribution | Attribution ambiguity — multiple plausible attributions per failure |
| Who&When Pro | 2607.09996 | Jul 2026 | 12,326 failed trajectories, 3 modalities, 26 benchmarks; failure injected after exact replay of successful prefix | Large-scale attribution w/ golden labels |
| TelemetrySuffBench | 2608.07899 | Aug 2026 | controlled traces w/ delayed-binding faults, telemetry masks | Detection–localization gap: metadata-only telemetry keeps detection F1 ≈ 1.0 but origin-step accuracy ≤ 0.5% |
| CatchBench | 2608.22808 | Aug 2026 | 1,187 configs, 1,162 runs, 72 entrants | When can a failure be caught: PRE (config) / LIVE (prefix) / POST (full trace) |
| AgenticRAG-FP | 2608.20627 | Aug 2026 | 80 3-hop MuSiQue questions, certified fault injection + downstream re-execution | **Propagation depth as evaluation axis**: coverage-based diagnosis 0.91 at hop 1 → 0.00 at hops 2–3 |
| StateMAS | 2607.29055 | Jul 2026 | 1,310 replayable MAS failure trajectories, 4 architectures, 4 LLMs | Repair (not just attribution) |
| RootSE | 2605.26563 | May 2026 | 102 repo-level coding instances | Earliest decisive error in coding-agent trajectories |
| BLAME | 2606.02282 | Jun 2026 | safety-critical MAS fault attribution | Benchmark accompanying POIROT |
| AgentErrata | 2609.02371 | Sep 2026 | agent failure dataset | Accompanies AGENTSCOPE |
| Long-horizon attribution bench | 2608.06909 | Aug 2026 | 1,300+ annotated trajectories (AgentDojo, Agent3Sigma) | Primary attribution localization + attribution-chain recovery |
| AgentHallu | 2601.06818 | Jan 2026 | hallucination attribution | (listed in Who&When citations; not separately fetched) |

**Benchmark-level takeaways for the seed:**
- Attribution ground truth is built either by human annotation (expensive, small) or **fault injection** (Aegis, Who&When Pro, AgenticRAG-FP). Fault-injection infrastructure already exists and is directly reusable for a blast-radius study.
- AgenticRAG-FP is the only benchmark that makes **propagation depth** an explicit axis — and shows post-hoc signal decays to zero by hop 2–3. This is direct evidence that *post-hoc* attribution cannot substitute for *online* containment.
- TelemetrySuffBench shows a hard detection–localization gap from telemetry structure alone — relevant to what an organizational containment layer could even observe.

---

## 4. Attribution methods — taxonomy of what exists (verified)

### 4.1 Prompting / LLM-judge pipelines (post-hoc, log-based)
| Method | ID | Date | Core idea | Stops at |
|---|---|---|---|---|
| RAFFLES | 2509.06822 | Sep 2025 (EACL 2026) | Iterative Judge + specialized Evaluators | Localization (>20% Who&When-HC) |
| A2P Scaffolding | 2509.10401 | Sep 2025 | Abduct–Act–Predict causal scaffolding in one pass; simulated counterfactual | Localization (47.5% step acc. on AG subset) |
| ECHO | 2510.04886 | Oct 2025 | Hierarchical context + consensus voting | Localization |
| AgentLocate | 2607.07989 | Jul 2026 (COLM 2026) | LLM judge + multi-perspective verification + confidence-aware aggregation | Localization |
| POIROT | 2606.02282 | Jun 2026 | System's own agents as diagnostic layer (epistemic diversity) | Detection/attribution |
| SAFARI | 2606.24626 | Jun 2026 (ICML 2026 AIWILD ws) | Tool-augmented active investigation over >context-window traces; +20% on Who&When within 1M-token budget | Localization |
| TrajAudit | 2605.26563 | May 2026 | Saliency folding + test-failure priors for coding agents | Localization |
| AgentRx | 2602.02475 | Feb 2026 (EMNLP Findings 2026) | Constraint synthesis + stepwise validation log | Localization (+75% step loc.) |
| AGENTSCOPE | 2609.02371 | Sep 2026 | Neuro-symbolic; behavioral abstractions + "neural invariants" | Localization |

### 4.2 Trained / lightweight models
| Method | ID | Date | Core idea | Stops at |
|---|---|---|---|---|
| AgenTracer-8B | 2509.03312 | Sep 2025 | Counterfactual-replay-annotated data + multi-granular RL; beats Gemini-2.5-Pro/Claude-4-Sonnet by up to 18.2% | Localization — **but** feeds actionable feedback to MetaGPT/MaAS (+4.8–14.2% task gains) |
| Aegis | 2509.14295 | Sep 2025 | Automated error injection → SFT/RL/contrastive | Localization |
| ASCon | 2608.10646 | Aug 2026 | Direction-aware agent–step contextualization; unified heads for agent/step/failure-mode | Localization (+5.8% agent, +10.6% step, +14.7% mode F1) |
| AFANet | 2608.18575 | Aug 2026 | Lightweight GNN over step semantics + agent relations; near-zero inference cost | Localization |
| StepFinder | 2606.03467 | Jun 2026 (KDD 2026) | Temporal semantic encoding + attention; 79% faster than fastest LLM baseline | Localization |
| MASPrism | 2605.07509 | May 2026 | Prefill-stage NLL/attention signals from 0.6B SLM; 2.66 s/trace | Localization |
| OAT | 2607.12747 | Jul 2026 | One-class neural-CDE trained only on *successful* trajectories; anomaly scores at inference | Localization |
| HPFA | 2608.02026 | Aug 2026 | Hypergraph paired failure-vs-success comparison; trains lightweight attributor | Localization (single-agent reasoning focus) |

### 4.3 Structure/graph- and spectrum-based
| Method | ID | Date | Core idea | Stops at |
|---|---|---|---|---|
| CHIEF | 2602.23701 | Feb 2026 | Hierarchical causal graph + counterfactual screening | Localization |
| DCFA | 2609.04749 | Sep 2026 | Dual-view causal-inspired graphs | Localization |
| AIGs | 2608.24361 | Aug 2026 | Adaptive Influence Graphs; agentic traversal; SOTA on Who&When | Localization |
| FALAT | 2606.00765 | May 2026 | Dependency-guided search; separates error-introducing from error-*propagating* steps; checks if correcting candidate suffices | Localization (46.0%/29.1% step acc.) |
| FAMAS | 2509.13782 | Sep 2025 | Spectrum-based fault localization (from SE) via trajectory replay | Localization |
| DUOTRACE | 2608.29646 | Aug 2026 | VAE anomaly detection filter before LLM attribution ("detect-before-attribute") | Localization (+8.7%/+7.0%) |
| CORRECT | 2509.24088 | Sep 2025 | Online cache of distilled error schemata | Localization |
| EAGER | 2603.21522 | Mar 2026 (FSE'26-IVR) | Contrastive trace embeddings; real-time detection + diagnosis + **reflexive mitigation** from historical failures | Detection + lightweight mitigation |
| DIG | 2603.00309 | Feb 2026 | Dynamic Interaction Graph of emergent collaboration; real-time identification + correction of collaboration-induced errors | Detection + correction |
| Coarse-to-Fine | DOI 10.1109/MRAI70020.2026.11621223 | 2026 (MRAI, low-tier IEEE) | Segment recall → agent attribution → step localization | Localization |

### 4.4 Interventional / counterfactual attribution (executed, not simulated)
| Method | ID | Date | Core idea | Recovery link |
|---|---|---|---|---|
| DoVer | 2512.06749 | Dec 2025 | Intervention-driven debugging: hypothesis generation + **active verification via targeted interventions** (edit messages, alter plans); outcome-oriented eval. Key finding: **multiple distinct interventions can independently repair the same failure** → single-cause attribution is ill-posed | Yes — flips 18–28% failed trials (Magnetic-One/GAIA/AssistantBench), 49% on AG2/GSMPlus |
| CAR (Causal Agent Replay) | 2606.08275 | Jun 2026 | SCM model of agent run; do-operations + re-execution; Monte-Carlo Shapley over steps; CIs. Validated on synthetic SCMs | No — attribution only, but interventional |
| CausalFlow | 2605.25338 | May 2026 | Causal Responsibility Scores via step-level counterfactual intervention → **minimal repairs that flip outcome**; contrastive pairs for training | Yes — test-time repair + training supervision (single-agent benchmarks) |
| GCJR / MRFR | 2608.29228 | Aug 2026 | **Minimal Repair Family Recovery**: all inclusion-minimal event sets whose counterfactual replay restores success; graph-constrained joint replay; exact within graph domain; 4-agent LLM pilot | Yes — recovers *repair families*, showing singleton attribution misses jointly-necessary repairs |
| BranchPoint-Latent | 2606.14805 | Jun 2026 | Predicts counterfactual-replay oracle results at zero replay cost (learning-to-rank over event KG) | No — cost model for replay |
| Conformal attribution | 2605.06788 | May 2026 | Conformal prediction sets (contiguous) over error steps, finite-sample coverage | **Yes — uses prediction sets to roll back MAS so it corrects its own errors** |
| Causal Attribution for Agentic Decisions | 2609.06445 | Sep 2026 | Estimator theory: marginal total effect vs common-random-numbers effect vs natural direct effect; proves both estimands fail in identifiable ways; traceability spec tied to EU AI Act | No — theoretical limits of attribution |

### 4.5 Online / early detection (pre-failure or mid-trajectory)
| Method | ID | Date | Core idea | Intervention? |
|---|---|---|---|---|
| AgentForesight | 2605.08715 | May 2026 | Online auditor alarms at earliest decisive error from prefix only; 7B model via coarse-to-fine RL; AFTraj-2K corpus | Alarm only — "opens the loop" to intervention but does not intervene |
| ProMAS | 2603.20260 | Mar 2026 | Markov transition dynamics + jump detection; 23% step acc. reading only 27% of logs | No |
| MASC | 2510.14319 | Oct 2025 | Metacognitive next-execution reconstruction + prototype prior; flags anomaly step and **triggers correction agent to revise output before it flows downstream** | **Yes — online pre-propagation correction** |
| Real-Time Detection & Repair | 2608.02464 | Aug 2026 | One-class echo-state monitors (µs/step) + deterministic verification; **rollback + live re-run recovers 45% of failures** (vs 16% resampling), success 52%→73% | Yes — rollback/re-run (single-agent episodes) |
| CatchBench | 2608.22808 | Aug 2026 | Benchmark: PRE/LIVE/POST auditability | Measurement only |

---

## 5. Does attribution connect to CONTAINMENT / RECOVERY? (the mission-critical question)

### 5.1 Attribution → repair (exists, growing, but "repair" ≠ "containment")
| Work | ID | What it does after attribution |
|---|---|---|
| DoCtOR | 2608.28264 (EMNLP 2026) | Attribution-targeted reflection: only the decisive-error agent reflects (others' memory not contaminated); counterfactual correction of the decisive step; +22–27% success on HotPotQA/ChartQAPro/Mind2Web |
| MARS + StateMAS | 2607.29055 | MCTS over repair space w/ diagnosis-guided expansion + taxonomy-augmented evaluation; partial rollouts; +3.0–12.1% over SOTA on 1,310-trajectory repair benchmark. States explicitly: "automated mechanisms to recover from such mistakes remain largely unexplored" |
| FlowFixer | 2607.02882 | Symbolic inference over workflow traces → executable behavioral specs → root-cause analysis → targeted repair patches; 71.3% repair success on Dify/Coze/n8n workflows |
| RESKILL | 2609.15684 (EMNLP 2026) | Explicit repair state across rounds; links failure hypotheses to skill patches; coverage-based attribution for repair selection. **Key stated finding: "explicit attribution alone is insufficient; durable improvement emerges when attribution is integrated with repair selection and persistent retest-conditioned update"** (single-agent, ALFWorld/TextCraft) |
| AgentTether | 2607.06273 | Critical Transition Graph → localize failure-critical subtrajectory → behavior-scoped guidance + repair memory + guarded runtime intervention; repairs 59–65% of failed tau-bench tasks (single-agent) |
| HarnessFix | 2606.06324 | Attributes failures to harness artifacts (not just steps) → scoped repair operators on the agent harness; +6.3–18.4% |
| EMAS | 2608.07196 | Trace → structured diagnosis → MAS topology/prompt revision when diagnosis recurs |
| AgentGrad | 2609.08572 | Sequential intervention identifies target agent → textual-gradient prompt repair |
| SHIELDA | 2508.07935 | 36-exception taxonomy over 12 agent artifacts; runtime exception handling w/ state recovery (single case study) |
| AgenTracer | 2509.03312 | Attribution feedback plugged into MetaGPT/MaAS improves task success 4.8–14.2% |

**Pattern:** every one of these treats recovery as *fixing the current failed run* (reflect, re-execute, patch, roll back, edit prompt/topology). None models how far the fault has already spread through the organization, none decides *what to isolate*, and none trades off containment against task utility.

### 5.2 Propagation / cascade work (closest to the seed)
| Work | ID/Venue | What it does | Gap vs seed |
|---|---|---|---|
| **From Spark to Fire** | 2603.04474 (Mar 2026) | Propagation-dynamics model over directed dependency graph; early-stage amplification-risk criterion; 3 vulnerability classes (cascade amplification, topological sensitivity, consensus inertia); single atomic error seed → widespread failure; **genealogy-graph governance layer (message-layer plugin) prevents final infection in ≥89% of runs** across 6 frameworks | Message/communication level only; no role/authority/memory/accountability/human boundaries; mitigation is uniform message-layer governance, not attribution-informed or boundary-aware |
| **Containing the Cascade (Cascade-Bench + Sentinel)** | DOI 10.1109/ICERA72709.2026.11666599, ICERA 2026 (5th Int. Conf. on Electronics Representation and Algorithm); authors Divi, Gullapalli, Brahmandam | Taxonomy of 6 cascading-failure modes; **containment metrics: containment rate, cascade depth, "blast radius", MTTD**; fault-injection testbed (1,080 scenarios, 6 domains) on a **discrete-event simulation** of agent message passing calibrated to published MAS failure stats; Sentinel mediator: typed message contracts + semantic anomaly gate + **circuit breaker** + **checkpoint-based recovery**; 590k simulated executions; success 31.3%→83.7%, containment 46.2%→99.4%; ablation separates fail-safe (circuit breaker → containment) from fail-operational (checkpoint rollback → completion) | **Simulation only — no real LLM agents**; low-tier venue; no organizational boundaries; but it *names and measures* the seed's central concept |
| CASPIAN | 2605.19240 (May 2026) | Online detection + attribution of **adversarial cascade attacks**; cross-channel causal influence matrix (late-interaction conditional transfer entropy); identifies origin/bridge/amplifier agents and propagation pathways; sub-1% overhead | Adversarial focus; detection/attribution, no containment action |
| Delayed Verification | 2606.27409 (Jun 2026) | False-claim propagation as delayed consensus on a graph; closed-form stability thresholds (inverse golden ratio at delay 2); **supermodular corrector-placement objective w/ greedy (1−1/e) approximation**; verified on 5 open models | Belief/consensus dynamics, not task workflows; placement is static, not attribution-driven |
| AgenticRAG-FP | 2608.20627 (Aug 2026) | Interventional benchmark; **propagation depth as explicit evaluation axis**; post-hoc diagnosis decays 0.91→0.00 from hop 1 to hops 2–3 | RAG-only; measurement, no containment |
| Misattribution Gap | 2605.22842 (May 2026) | Memory-poisoning failures are systematically misattributed to model failure; counterfactual composition testing (87.5% acc.); memory-persistent information-flow control blocks 97% | Security/attack framing; memory boundary only |
| Traceability & Accountability pipelines | 2510.07614 (ASE-W 2025) | Planner→Executor→Critic; structured accountable handoffs; quantifies per-role repair/harm rates; shows where errors start and spread | Small pipeline; descriptive, no containment mechanism |
| AUDITA | 2608.22160 (Aug 2026) | Tamper-evident inter-agent command record + certified graded causal attribution; provably ungameable verdicts; overdetermined/preempted/omission causes | Accountability/audit, embodied fleets; no recovery |

### 5.3 Verdict on the connection question
- **Attribution → localization:** saturated (Section 4).
- **Attribution → repair of the failed run:** emerging and competitive (Section 5.1) — MARS, DoCtOR, FlowFixer, DoVer, CausalFlow, AgentTether, RESKILL.
- **Attribution → containment of propagation (limiting blast radius):** **absent.** The two propagation-aware containment works (From Spark to Fire; Containing the Cascade) do **not** consume attribution output — Sentinel uses generic anomaly gates/circuit breakers; the genealogy graph is structural. Conversely, no attribution paper evaluates whether its output reduces spread. The closed loop "attribute → decide containment action → measure blast radius vs utility" is unoccupied.
- **Organizational boundaries (role, authority/delegation, memory, accountability, human-agent):** untouched by the propagation/containment literature. MASO-relevant angle intact. (Note: the delegation-invariants/accountability-chain territory is occupied by the existing MASO proposal at maso/policy_preserving_delegation_research_proposal.md — the seed should frame around *fault propagation and containment*, not delegation policy.)

---

## 6. What is solved vs open

**Solved-ish (diminishing returns for a new paper):**
- Agent-level attribution on Who&When-scale benchmarks (multiple SOTA claims: AIGs, CHIEF, DCFA, SAFARI, AgenTracer, ASCon).
- Cheap/lightweight attribution (MASPrism, AFANet, StepFinder, OAT).
- Benchmarking attribution itself (Who&When Pro, TraceElephant, LongRCA, MP-Bench, TelemetrySuffBench, CatchBench).
- Single-run repair given a diagnosis (MARS, FlowFixer, AgentTether, CausalFlow).

**Open (defensible for MASO):**
1. **Attribution → containment coupling.** No work feeds attribution into a containment decision (isolate agent? revoke tool? quarantine memory? escalate to human?) or measures downstream spread prevented.
2. **Blast radius as a first-class, empirically grounded metric on real LLM MAS.** The term exists only in a simulation study at a low-tier venue; AgenticRAG-FP measures diagnosability-vs-depth but not spread size; From Spark to Fire measures infection rate but not boundary-typed spread.
3. **Organizational boundary crossing.** Role, authority, tool, memory, accountability, human-agent boundaries as distinct propagation channels — no existing taxonomy or measurement (MAST's 14 modes are failure *types*, not propagation *channels*).
4. **Attribution under propagation is known to degrade** (AgenticRAG-FP: 0.91→0.00 by hop 2–3; TelemetrySuffBench: detection–localization gap) — so *when* to attribute vs *when* to contain is an open trade-off nobody studies.
5. **Multi-cause / jointly-necessary failures** (MP-Bench, DoVer, GCJR) undermine the single-culprit assumption that most attribution benchmarks bake in — a containment framing (sets of minimal isolation actions) sidesteps this.
6. **Utility–containment trade-off.** Containment actions cost task utility (Sentinel's ablation hints at this: circuit breaker governs containment, rollback governs completion). No principled study exists.

**Threats to the seed (must cite and differentiate):**
- *Containing the Cascade* (terminology + metrics + circuit-breaker/checkpoint mechanisms) — differentiate via real LLM MAS, organizational boundaries, attribution-informed containment.
- *From Spark to Fire* (propagation dynamics + mitigation on real frameworks) — differentiate via boundary-typed blast radius and recovery, not just message-layer suppression.
- *MARS/StateMAS* and *DoCtOR* (attribution→repair) — differentiate: repair fixes the run; containment limits spread across the organization.
- *Delayed Verification* (corrector placement) — differentiate: static belief-consensus model vs dynamic organizational workflows.

---

## 7. Classical grounding (pre-LLM concepts; cited from established knowledge — DBLP verification blocked by anti-bot at investigation time)

| Concept | Reference | Relevance |
|---|---|---|
| Model-based diagnosis | Reiter, "A Theory of Diagnosis from First Principles," Artificial Intelligence 32(1), 1987 | Minimal hitting sets of faulty components ≈ GCJR's minimal repair families |
| Spectrum-based fault localization | Jones & Harrold (Tarantula, ICSE 2002); Abreu et al. (Ochiai, 2007) | Directly imported by FAMAS (2509.13782) |
| Distributed snapshots / rollback | Chandy & Lamport, "Distributed Snapshots," ACM TOCS 3(1), 1985; checkpoint-recovery literature | Sentinel's checkpoint recovery; Conformal rollback (2605.06788) |
| Byzantine fault tolerance | Castro & Liskov, PBFT, OSDI 1999 | Containment of arbitrary agent behavior; largely unimported into LLM-MAS containment |
| Actual causality | Halpern & Pearl, BJPS 2005 | Basis of counterfactual attribution (CAR, CausalFlow, DCFA "decisive error" definition) |
| Cascading failures in networks | Motter & Lai (2002); epidemic/SIS threshold models | From Spark to Fire and Delayed Verification implicitly use these dynamics |

---

## 8. Appendix — quick-reference paper table (all verified this run)

| # | Paper | ID | Date | Venue note |
|---|---|---|---|---|
| 1 | Who&When | 2505.00212 | Apr 2025 | camera-ready (ICML 2025) |
| 2 | MAST (Why Do MAS Fail) | 2503.13657 | Mar 2025 | — |
| 3 | TRAIL | 2505.08638 | May 2025 | — |
| 4 | SHIELDA | 2508.07935 | Aug 2025 | — |
| 5 | AgenTracer | 2509.03312 | Sep 2025 | — |
| 6 | RAFFLES | 2509.06822 | Sep 2025 | EACL 2026 |
| 7 | A2P Scaffolding | 2509.10401 | Sep 2025 | — |
| 8 | FAMAS (spectrum) | 2509.13782 | Sep 2025 | — |
| 9 | Aegis | 2509.14295 | Sep 2025 | — |
| 10 | CORRECT | 2509.24088 | Sep 2025 | — |
| 11 | ECHO | 2510.04886 | Oct 2025 | — |
| 12 | Traceability & Accountability | 2510.07614 | Oct 2025 | ASE-W 2025 |
| 13 | Failure-Driven Workflow Refinement (CE-Graph) | 2510.10035 | Oct 2025 | — |
| 14 | MASC | 2510.14319 | Oct 2025 | — |
| 15 | DoVer | 2512.06749 | Dec 2025 | — |
| 16 | AgentHallu | 2601.06818 | Jan 2026 | (cited, not fetched) |
| 17 | AgentRx | 2602.02475 | Feb 2026 | EMNLP Findings 2026 |
| 18 | CHIEF | 2602.23701 | Feb 2026 | — |
| 19 | DIG to Heal | 2603.00309 | Feb 2026 | — |
| 20 | From Spark to Fire | 2603.04474 | Mar 2026 | — |
| 21 | ProMAS | 2603.20260 | Mar 2026 | — |
| 22 | EAGER | 2603.21522 | Mar 2026 | FSE'26-IVR |
| 23 | MP-Bench | 2603.25001 | Mar 2026 | under review |
| 24 | ErrorProbe | 2604.17658 | Apr 2026 | ACL 2026 Findings |
| 25 | TraceElephant | 2604.22708 | Apr 2026 | ACL 2026 |
| 26 | Conformal Agent Error Attribution | 2605.06788 | May 2026 | — |
| 27 | MASPrism | 2605.07509 | May 2026 | — |
| 28 | AgentForesight | 2605.08715 | May 2026 | — |
| 29 | LIFE survey | 2605.14892 | May 2026 | — |
| 30 | VerifyMAS | 2605.17467 | May 2026 | — |
| 31 | CASPIAN | 2605.19240 | May 2026 | — |
| 32 | Misattribution Gap | 2605.22842 | May 2026 | under review (security venue) |
| 33 | CausalFlow | 2605.25338 | May 2026 | — |
| 34 | TrajAudit / RootSE | 2605.26563 | May 2026 | — |
| 35 | FALAT | 2606.00765 | May 2026 | — |
| 36 | POIROT / BLAME | 2606.02282 | Jun 2026 | — |
| 37 | StepFinder | 2606.03467 | Jun 2026 | KDD 2026 |
| 38 | HarnessFix | 2606.06324 | Jun 2026 | — |
| 39 | CAR | 2606.08275 | Jun 2026 | open source |
| 40 | BranchPoint-Latent | 2606.14805 | Jun 2026 | submitted to KBS |
| 41 | SAFARI | 2606.24626 | Jun 2026 | ICML 2026 AIWILD ws |
| 42 | Delayed Verification | 2606.27409 | Jun 2026 | — |
| 43 | FlowFixer | 2607.02882 | Jul 2026 | — |
| 44 | AgentTether | 2607.06273 | Jul 2026 | — |
| 45 | AgentLocate | 2607.07989 | Jul 2026 | COLM 2026 |
| 46 | Who&When Pro | 2607.09996 | Jul 2026 | — |
| 47 | OAT | 2607.12747 | Jul 2026 | — |
| 48 | MARS / StateMAS | 2607.29055 | Jul 2026 | under review |
| 49 | HPFA | 2608.02026 | Aug 2026 | — |
| 50 | Real-Time Detection & Repair | 2608.02464 | Aug 2026 | code released |
| 51 | EMAS | 2608.07196 | Aug 2026 | — |
| 52 | Long-horizon attribution bench | 2608.06909 | Aug 2026 | — |
| 53 | TelemetrySuffBench | 2608.07899 | Aug 2026 | — |
| 54 | ASCon | 2608.10646 | Aug 2026 | — |
| 55 | LongRCA Bench / RCTA | 2608.15242 | Aug 2026 | — |
| 56 | AFANet | 2608.18575 | Aug 2026 | — |
| 57 | AgenticRAG-FP | 2608.20627 | Aug 2026 | — |
| 58 | AUDITA | 2608.22160 | Aug 2026 | — |
| 59 | CatchBench | 2608.22808 | Aug 2026 | — |
| 60 | AIGs | 2608.24361 | Aug 2026 | — |
| 61 | llmmas-otel | 2608.24271 | Aug 2026 | ICST 2026 (tool) |
| 62 | DoCtOR | 2608.28264 | Aug 2026 | EMNLP 2026 |
| 63 | GCJR / MRFR | 2608.29228 | Aug 2026 | conference paper |
| 64 | DUOTRACE | 2608.29646 | Aug 2026 | — |
| 65 | AGENTSCOPE / AgentErrata | 2609.02371 | Sep 2026 | — |
| 66 | DCFA | 2609.04749 | Sep 2026 | — |
| 67 | Causal Attribution for Agentic Decisions | 2609.06445 | Sep 2026 | — |
| 68 | AgentGrad | 2609.08572 | Sep 2026 | — |
| 69 | AgentAudit | 2609.09875 | Sep 2026 | — |
| 70 | RESKILL | 2609.15684 | Sep 2026 | EMNLP 2026 |
| 71 | Containing the Cascade (Cascade-Bench + Sentinel) | DOI 10.1109/ICERA72709.2026.11666599 | 2026 | ICERA (low-tier IEEE); verified via Semantic Scholar |
| 72 | Coarse-to-Fine Failure Attribution | DOI 10.1109/MRAI70020.2026.11621223 | 2026 | MRAI (low-tier IEEE); verified via Semantic Scholar |

*Coverage note: Who&When has ~160 citing papers; I fetched and verified all citation-list entries relevant to attribution/debugging/repair/propagation (both S2 citation pages, 159 entries scanned). Items clearly off-topic (e.g., MoE pruning, VQA, audio-visual eval) were excluded.*
