# B14 — Self-Healing and Self-Improving Agents: Recovery Strategies and Their Evaluation

**Investigator:** Landscape B14 specialist
**Date:** 21 September 2026
**Mission question:** Map self-repair, reflection-based recovery, automated error recovery, self-healing MAS (classical self-* + LLM era), retry/replan strategies. What recovery strategies exist and how are they evaluated? Is recovery evaluated at SYSTEM level (containing spread) or only task level?
**Seed hypothesis under test:** "Organizational failure propagation and recovery in LLM MAS" — what determines the *organizational blast radius* of a local fault, and which containment/recovery mechanisms minimize systemic impact while preserving task utility.

---

## 0. Bottom-line judgment

**The seed hypothesis survives this landscape.** Recovery/self-healing is a heavily worked area, but its evaluation is overwhelmingly **task-level** (did the task succeed after recovery?), not **system-level** (how far did the fault spread before containment, and what did containment cost?). The nearest neighbors — faulty-agent resilience under topology variation (arXiv:2408.00989), budgeted self-healing orchestration (arXiv:2606.01416), intervention-driven debugging (arXiv:2512.06749), AIOps incident-mitigation benchmarks (AIOpsLab, ITBench), and cross-layer fault-propagation testing in GPU infrastructure (ADA-ST, arXiv:2607.16161) — each capture one ingredient (fault injection, recovery-strategy comparison, propagation graphs, mitigation evaluation) but none measures propagation *across organizational boundaries* (role, communication, authority/delegation, tool, memory, accountability, human-agent) as a first-class variable, and none evaluates containment mechanisms on systemic impact vs. preserved utility. The *diagnosis* side (failure attribution) is now crowded and should not be the contribution; the *containment-and-recovery-with-spread-measurement* side is open.

**Caveats:** (a) Two 2026 papers titled "self-healing" for LLM agents exist (arXiv:2605.06737 claims to "reduce failure propagation" in a multi-agent workflow — inspect before claiming novelty of *any* propagation-reduction framing); (b) classical self-* literature (autonomic computing, recovery-oriented computing, exception-handling MAS) anticipated most concepts, so framing must be about what LLM agents change, not about inventing self-healing; (c) strong negative results on intrinsic self-correction mean any proposed mechanism should rely on external/verifiable feedback, not the model's self-assessment.

---

## 1. Scope, method, and verification channels

**Queries/areas covered:** self-healing systems (classical + LLM), self-repair/self-correction/self-debugging, reflection-based recovery (Reflexion lineage), retry vs. replan strategies, fault injection and resilience of LLM MAS, failure attribution → repair loops, AIOps/incident recovery benchmarks, runtime containment (undo, confinement, rerouting), classical exception handling in MAS, rollback-recovery and Byzantine fault tolerance.

**Verification channels used (with reliability notes):**
- arXiv abstract pages via direct fetch — **primary verification channel, all arXiv claims below verified this way** (title, authors where shown, dates, abstract, venue comments).
- Crossref API — for classical/non-arXiv works (DOIs, venues, dates verified).
- USENIX proceedings pages — for OSDI works.
- arXiv title search — worked intermittently (heavy rate limiting); used for "self-healing" title sweep through ~1 Sep 2026.
- Semantic Scholar API, OpenAlex, OpenReview API, DBLP — **all rate-limited/blocked from this network during the sweep**; not used for verification.
- Secondary: `masamasa59/ai-agent-papers` curated corpus (incl. its Aug-2026 failure-attribution newsletter, which claims full-text reading) — used for discovery only; every load-bearing item below was independently re-verified on arXiv/Crossref.

**Not verified (flagged, not relied on):** Koopman, "Elements of the Self-Healing System Problem Space" (WADS 2003 / CMU) — well-known but unreachable through available channels (not in Crossref; DBLP bot-blocked; CMU page unrenderable). Cite only after independent check.

---

## 2. Classical self-* lineage (pre-LLM)

The concepts "self-healing," "blast radius containment," and "recovery vs. repair" predate LLMs by decades. Any MASO paper must position against these.

| Work | Venue/Year | Identifier | Core idea | Relation to seed |
|---|---|---|---|---|
| Kephart & Chess, "The Vision of Autonomic Computing" | IEEE Computer, Jan 2003 | DOI 10.1109/MC.2003.1160055 (Crossref ✓) | Self-* properties: self-configuring, self-healing, self-optimizing, self-protecting | Origin of "self-healing systems" framing; organizational metaphor explicit (autonomic nervous system) |
| Ghosh et al., "Self-healing systems — survey and synthesis" | Decision Support Systems, 2007 | DOI 10.1016/j.dss.2006.06.011 (Crossref ✓) | Survey of self-healing: detection, diagnosis, recovery | Classical evaluation = availability/MTTR, not task utility |
| "A survey on self-healing systems: approaches and systems" | Computing, 2010 | DOI 10.1007/s00607-010-0107-y (Crossref ✓) | Second survey wave | Same |
| Candea et al., "Microreboot—A Technique for Cheap Recovery" | OSDI 2004, pp. 31–44 | USENIX proceedings page ✓ | Fine-grain component reboot; recover without disturbing rest of application; "rejuvenation by parts" | **Direct classical analog of containment**: minimize the recovery's own blast radius |
| Candea et al., "Recovery-oriented computing: building multitier dependability" | IEEE Computer, Nov 2004 | DOI 10.1109/MC.2004.219 (Crossref ✓) | ROC: accept failures, optimize fast recovery | Recovery-first design philosophy |
| "Recovery oriented computing: a new research agenda" | HPCA 2002 | DOI 10.1109/HPCA.2002.995714 (Crossref ✓) | ROC agenda | Same |
| Elnozahy et al., "A survey of rollback-recovery protocols in message-passing systems" | ACM Computing Surveys, Sep 2002 | DOI 10.1145/568522.568525 (Crossref ✓) | Checkpoint/rollback; **domino effect** (rollback propagation) | The classical "blast radius" problem: rollback cascades; orphan messages |
| Castro & Liskov, "Practical Byzantine fault tolerance and proactive recovery" | ACM TOCS, Nov 2002 | DOI 10.1145/571637.571640 (Crossref ✓) | Replication + proactive recovery | Containment via redundancy; assumes f < n/3 |
| Klein & Dellarocas, "Exception handling in agent systems" | Autonomous Agents '99 | DOI 10.1145/301136.301164 (Crossref ✓) | Exceptions as first-class in agent systems | MAS-native recovery vocabulary |
| Klein & Dellarocas, "A Knowledge-based Approach to Handling Exceptions in Workflow Systems" | CSCW journal, 2000 | DOI 10.1023/A:1008759413689 (Crossref ✓) | Generic exception taxonomy + resolution strategies for workflows | Organizational workflow recovery, pre-LLM |
| Dellarocas & Klein, "An experimental evaluation of domain-independent fault handling services in open multi-agent systems" | ICMAS 2000 | DOI 10.1109/ICMAS.2000.858440 (Crossref ✓) | Sentinel agents providing fault-handling services | **Classical MAS recovery architecture** — sentinel/watchdog pattern |
| Klein & Dellarocas, "Using Domain-Independent Exception Handling Services to Enable Robust Open MAS: The Case of Agent Death" | Autonomous Agents and Multi-Agent Systems, 2003 | DOI 10.1023/A:1024145408578 (Crossref ✓) | Agent-death detection and task reassignment | Role/boundary recovery in open MAS |
| "Economically Inspired Self-healing Model for Multi-Agent Systems" | IEEE/WIC/ACM IAT 2007 | DOI 10.1109/IAT.2007.80 (Crossref ✓) | Market-based self-healing in MAS | Classical self-healing MAS |
| "Multi-Agent Technology for Self-Healing Shipboard Power Systems" | ISAP 2005 | DOI 10.1109/ISAP.2005.1599264 (Crossref ✓) | MAS self-healing in power systems | Domain application lineage |
| "A decentralised self-healing approach for network topology maintenance" | Autonomous Agents and Multi-Agent Systems, 2020 | DOI 10.1007/s10458-020-09486-3 (Crossref ✓) | Topology self-repair | Classical lineage persists into 2020s |

**Takeaway:** detection → diagnosis → recovery loops, sentinels, microreboot-style surgical recovery, rollback cascades (domino effect), and market/role-based reallocation are all classical. The LLM-era contribution cannot be "self-healing for agents" as a concept — it must be about what is *new* when components are stochastic language models with natural-language state, shared memory, and organizational roles.

---

## 3. LLM era, single-agent: self-repair, reflection, retry/replan

### 3.1 Foundations (verified)

| Work | arXiv / venue | Method | Evaluation | Key finding / limitation |
|---|---|---|---|---|
| ReAct (Yao et al.) | 2210.03629, ICLR 2023 | Interleaved reasoning+acting; reasoning traces "handle exceptions" | HotpotQA, FEVER, ALFWorld, WebShop; task success | Exception handling is implicit in prompting, not measured |
| Reflexion (Shinn et al.) | 2303.11366, NeurIPS 2023 | Verbal self-reflection stored in episodic memory; retry with reflection in context | ALFWorld, HotpotQA, HumanEval (91% pass@1); task success | Task-level only; needs reliable feedback signal |
| Self-Refine (Madaan et al.) | 2303.17651, NeurIPS 2023 | Same model generates → critiques → refines iteratively | 7 tasks; preference/accuracy | ~20% avg improvement; no failure-spread analysis |
| Self-Debug (Chen et al.) | 2304.05128 | Rubber-duck debugging of generated code from execution results | Spider, TransCoder, MBPP | Up to +12% with unit tests; +2-3% without oracle |
| CRITIC (Gou et al.) | 2305.11738, ICLR 2024 | Tool-interactive critique: external tools validate then revise | QA, math program synthesis, toxicity | External feedback is the active ingredient |
| ReWOO (Xu et al.) | 2305.18323 | Decouple reasoning from tool observations | 6 NLP benchmarks + **tool-failure robustness test** | One of few with an explicit tool-failure robustness claim |
| Olausson et al., "Is Self-Repair a Silver Bullet for Code Generation?" | 2306.09896, ICLR 2024 | Analysis of self-repair | HumanEval, APPS | **Negative-ish**: gains modest once repair cost counted; bottlenecked by self-feedback quality; human debugging far better |
| Huang et al., "LLMs Cannot Self-Correct Reasoning Yet" | 2310.01798, ICLR 2024 | Analysis of intrinsic self-correction | Reasoning benchmarks | **Negative**: without external feedback, self-correction degrades performance |
| Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes?" | 2406.01297, TACL 2024 | Critical survey + checklist | — | Self-correction works only with reliable external feedback or fine-tuning; most prior evaluations unfair |
| GoEX (Patil et al.) | 2404.06921 | Runtime for LLM actions: **undo + damage confinement**, post-facto validation | Design + open research questions | **Closest classical-style containment idea in LLM era**; not empirically evaluated as containment |
| Plan-and-Act (Lee et al.) | 2503.09572, ICML 2025 | Planner/Executor separation, synthetic plan training | WebArena-Lite 57.6%, WebVoyager 81.4% | Plan-level recovery not measured |
| ReflAct (Kim et al.) | 2505.15182, EMNLP 2025 | Goal-state reflection backbone | ALFWorld 93.3% | Claims ReAct's incoherent reasoning causes "compounding errors" — propagation acknowledged, not measured |
| Reflect, Retry, Reward (Russak et al.) | 2505.24726 | RL rewarding self-reflection tokens that precede successful retry | Math, function calling (+18.1%) | Retry-with-reflection trained; task-level |
| SAMULE (Ge et al.) | 2509.20562, EMNLP 2025 | Trained retrospective model; micro/meso/macro reflection synthesis | TravelPlanner, NATURAL PLAN, τ-bench | Error taxonomies across trials; still task-success metric |

### 3.2 What this means for the seed

Single-agent recovery is a mature, saturated area with **three robust negative results** (intrinsic self-correction fails; self-repair is feedback-bottlenecked; self-correction needs external oracles). Evaluation is uniformly task-level (pass@1, success rate, preference). Nobody measures collateral effects of a failed recovery attempt (e.g., corrupted shared state, wasted budget, downstream agents misled) — the seed's "blast radius" is absent even here.

---

## 4. LLM era, multi-agent: failure diagnosis → repair loops

This is the **crowded** region. Diagnosis/attribution is now an established subfield with benchmarks; repair is being attached to diagnosis, evaluated by task-recovery rate.

| Work | arXiv / venue | What it does | Evaluation | System-level? |
|---|---|---|---|---|
| MAST — "Why Do Multi-Agent LLM Systems Fail?" (Cemri et al.) | 2503.13657 (v3 Oct 2025) | 14-mode failure taxonomy; MAST-Data, 1600+ annotated traces, 7 frameworks | Taxonomy + LLM-judge annotation agreement (κ=0.88) | No — descriptive taxonomy; identifies "inter-agent misalignment" category but no propagation metric |
| Who&When (Zhang et al.) | 2505.00212 (camera-ready) | Failure attribution: which agent, which step; 127 MAS failure logs | Attribution accuracy: best 53.5% agent-level, **14.2% step-level** | No — diagnosis only; shows attribution is hard |
| AgenTracer (Zhang et al.) | 2509.03312 | Counterfactual replay + programmed fault injection to annotate failures; trains 8B tracer | Who&When benchmark; +4.8–14.2% gains when feeding diagnoses to MetaGPT/MaAS | Partially — fault injection + counterfactual replay, but success measured as task performance |
| DoVer (Ma et al.) | 2512.06749 (v3 Jan 2026) | **Intervention-driven debugging**: edit messages/plans, verify by re-execution; multiple interventions can independently repair | Magentic-One on GAIA/AssistantBench: flips 18–28% of failed trials; AG2/GSMPlus: recovers 49% | Task-recovery rate; explicitly outcome-oriented, not spread-oriented |
| AgentRx (Barke et al.) | 2602.02475, EMNLP Findings 2026 | Constraint-synthesis diagnosis; 170-trajectory benchmark, 11 task settings | Step localization +75% over prior | No |
| Who&When Pro (Liu et al.) | 2607.09996 | 12,326 failed trajectories via replay-then-inject pipeline; 26 benchmarks | Attribution patterns across modalities | No — bigger diagnosis benchmark |
| TRAJDEBUG (Qi et al.) | 2608.06346 | Error-lifecycle tracing; critical-error localization; TrajErrBench (486 annotated) | **Avg 7.62 local errors per failed trajectory, only 1 critical**; diagnosis feedback → +10.8% re-run success | No — but the 7.62:1 ratio is direct evidence most local faults self-mask, i.e., natural containment exists and is unstudied |
| SearchAuditor (Liang et al.) | 2608.05212 | Audit + repair long-horizon search agents; SearchAuditBench (1,243 failed trajectories) | Best end-to-end pass 32.3%; repairs enable recovery on resume | Task-level recovery |
| Credit Without Ground Truth (Zhang et al.) | 2608.19760 | Audits step-level credit signals against executed-replay causal ground truth | **Negative**: LLM-judge, logprob-ratio, confidence signals all ≈ chance vs causal contribution; implicit credit echoes fluency (+0.75) | No — but undermines diagnosis-driven repair that relies on these signals |
| Automata from Agent Traces (Cho et al.) | 2608.23670 | Collapse trace corpora into FSMs; failure prediction AUROC ≤0.94; early stopping at ~32% progress | 12 datasets | Runtime monitoring/early-stop = crude containment; not evaluated as containment |
| "Model or Harness?" (Raj et al.) | 2607.28802 | Interaction-centric taxonomy, 41 failure modes mapped to component edges; frames the **"repair-assignment problem"** | Judge agreement κ=0.76 | No — but explicitly asks "which intervention would improve the system" |
| "Towards Risk-free AI Agent Deployment" (Huo et al.) | 2608.16411 | Position: trajectory-grounded testing/debugging; attribution → repair → self-evolution roadmap | — | Roadmap only |
| LIFE survey (Qi et al.) | 2605.14892 | Survey: capability → collaboration → **fault attribution** → evolution; states "errors can propagate across agents and interaction rounds" | — | Acknowledges propagation; no measurement framework |
| "Detecting Silent Failures in Multi-Agentic AI Trajectories" (Pathak et al.) | 2511.04032 | Anomaly detection on trajectories; 2 datasets (4,275 + 894) | XGBoost/SVDD up to 98% accuracy | Detection only |
| RGD (Jin et al.) | 2410.01242 | Multi-LLM debugging for code generation | HumanEval +9.8%, MBPP +16.2% | No |
| Seeker (Zhang et al.) | 2412.11713 | Multi-agent exception-handling for code | Real-repo analysis | Code-level, not system-level |

**Takeaway:** The diagnosis→repair loop is closing (TRAJDEBUG, SearchAuditor, DoVer all show diagnosis-fed re-execution improves success), but **every evaluation endpoint is the recovered task's success**. None asks: while the fault was live, how many other agents/artifacts/memories did it contaminate? DoVer's finding that "multiple distinct interventions can independently repair the failed task" is adjacent to the seed's question (which containment point minimizes spread?) but is framed as attribution ill-posedness, not as containment optimization.

---

## 5. "Self-healing"-titled LLM systems (2026 wave) — the nearest neighbors

A distinct 2026 cluster explicitly uses "self-healing" for LLM/agent systems. Verified via arXiv title search + abs pages:

| Work | arXiv | Setting | Recovery mechanism | Evaluation | Spread/containment measured? |
|---|---|---|---|---|---|
| **Self-Healing Agentic Orchestrators** (Babu & Agrawal) | 2606.01416 (May 2026) | Tool-augmented LLM orchestration | Failure signal → failure class → targeted recovery under explicit budgets → verification | **100-task controlled fault-injection benchmark; vs. static / retry-only / ReAct / full-replanning**; 98.8% success; budget sweep; silent-failure rate → 0.0% with verifier | **No** — single orchestrator; task success + silent-failure rate. But it is the **only verified work that head-to-head compares retry vs. replan vs. targeted recovery under matched budgets** |
| **A Self-Healing Framework for Reliable LLM-Based Autonomous Agents** (Jeong & Shin) | 2605.06737 (May 2026); Int. J. Software Engineering & Knowledge Engineering 2026, DOI 10.1142/S0218194026500695 | Multi-agent workflow environment | Failure detection + reliability scoring + adaptive replanning + corrective prompting | Real-world task scenarios; success rate; **abstract claims "reduces failure propagation"** | **Claimed but unquantified in abstract** — MUST inspect full text before claiming novelty of propagation-reduction framing. 13 pages, 3 figures — likely thin |
| **Graph-Based Self-Healing Tool Routing** (Bholani) | 2603.01548 (Mar 2026) | Tool routing as graph problem | Deterministic Dijkstra re-routing on tool failure (edges → ∞); LLM only for goal demotion/escalation | 19 scenarios, 3 topologies; matches ReAct correctness, −93% control-plane LLM calls; eliminates silent skips under compound failures | Partially — "every failure is a logged reroute or explicit escalation, never a silent skip" is binary observability, not spread measurement |
| **Think it, Run it** (Bara et al.) | 2604.27096 (Apr 2026) | 5-agent ML pipeline generation | LLM error interpretation + adaptive learning from execution history | 150 ML tasks; 84.7% end-to-end success | No |
| **Agentic Self-Healing for Data and AI Pipelines** (Eshun et al.) | 2608.01955 (Aug 2026) | Data/ML/delivery pipelines | Reference architecture: monitoring + deterministic policy checks + AI diagnosis + approval workflows + controlled remediation | Architecture paper; vendor comparison | No — but "approval workflows" = human-boundary containment, org-flavored |
| **X-SHIELD: Explainability-by-Design for Self-Healing Orchestration in MAS** (Joseph, Belouard, El Kardi, Yaacoub) | ENASE 2026, pp. 662–669, DOI 10.5220/0015045500004015 (Crossref ✓ + SCITEPRESS page ✓) | Orchestrated AI components (adaptive-quiz domain) | Each recovery intervention rendered as a structured **explanation artifact** (trigger, evidence, diagnosis hypotheses w/ uncertainty, recovery actions, expected effects, audit metadata); deterministic rule-based Auto-Explainer | Artifact-level validation on compact scenario suite + formative user study (N=10): clarity/actionability vs raw logs | **No** — recovery *explainability/auditability*, not spread measurement. Adjacent to the seed's accountability boundary (auditable recovery), not to blast-radius quantification |
| **ADA-ST: Adaptive Fault Injection Planning for Multi-Layer Self-Healing AI Infrastructure** (Kulkarni et al.) | 2607.16161 (Jul 2026) | GPU platform self-healing pipelines (HW→FW→mgmt→orchestration) | Weighted **fault-propagation graph**; adaptive scenario selection for coverage | 72,550 repair tickets over 4 years; **49% of tickets involve cross-layer fault propagation**; static campaigns cover only 20–25% of propagation edges | **Yes, but for infrastructure layers** — the strongest verified evidence that cross-boundary propagation dominates real failures, and that per-layer testing misses it. Directly transferable methodology (propagation graph + coverage) |

**Takeaway:** The phrase "self-healing" is being colonized by applied/orchestration papers in 2026, all evaluated at task-success or coverage level. ADA-ST is the most important find of this sweep for the seed: it proves (in infra) that cross-layer propagation is the dominant failure mode and builds the measurement machinery (propagation graphs, edge coverage) that the seed hypothesis wants for *organizational* boundaries.

---

## 6. Resilience, containment, and propagation evaluation

| Work | arXiv/venue | What it measures | System-level? |
|---|---|---|---|
| **On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents** (Huang et al.) | 2408.00989 (v4 May 2025) | Fault injection (AutoTransform/AutoInject) into 6 systems, 3 topologies, 4 tasks; hierarchical structure most resilient (5.5% vs 10.5%/23.7% drop); Challenger/Inspector defenses recover up to 96.4% of injected errors | **Closest existing work to the seed.** Topology-dependent performance drop ≈ implicit blast radius. But: static injected faulty agent (not a propagating fault), metric is aggregate task performance, no organizational boundaries, no recovery dynamics |
| Evaluating Cooperative Resilience (Chacon-Chamorro et al.) | 2512.11689 (Dec 2025) | Humans vs LLM groups in Tragedy-of-Commons under persistent unsustainable bot + stochastic shocks; resilience = anticipate/resist/**recover**/transform | **Population-level recovery under ongoing disruption** — one of very few measuring recovery dynamics rather than post-hoc success. Social-dilemma setting, not organizational workflow |
| Agents of Chaos (Shapira et al.) | 2602.20021 (Feb 2026) | 2-week live red-team of autonomous agents with memory/email/Discord/shell; 11 case studies incl. **cross-agent propagation of unsafe practices**, partial system takeover, false completion reports | Qualitative documentation that propagation across agents/boundaries happens in the wild; no metrics or containment |
| SABER (Cuadron et al.) | 2512.07850 (Nov 2025) | Mutating vs non-mutating steps; each mutating deviation cuts success odds up to 92–96%; mutation-gated verification + targeted reflection safeguard | Action-level containment (gate the irreversible steps); task-success endpoint |
| AIOpsLab (Chen et al., Microsoft) | 2501.06706 (Jan 2025) | Deploys microservice clouds, injects faults, evaluates agents across incident lifecycle; explicitly visions "self-healing cloud systems" (AgentOps) | **System-level recovery evaluation exists here** (fault localization, RCA, mitigation in a live environment) — but the "system" is cloud infra, and the recovered entity is the service, not an organization of agents |
| ITBench (IBM) | DSN-S 2025, DOI 10.1109/dsn-s65789.2025.00060 (Crossref ✓) | Benchmarking AI agents for IT automation (SRE/CISO incidents) | Same shape as AIOpsLab |
| RCAgent (Wang et al.) | CIKM 2024, DOI 10.1145/3627673.3680016 (Crossref ✓) | Cloud root-cause analysis by tool-augmented autonomous agents | Diagnosis-centric |
| Aegis (Song et al.) | 2508.19504 (Aug 2025) | 142 traces, 3,656 turns; 6-mode agent-environment failure taxonomy; environment-side optimizations (observability, offloading, speculative actions) | Environment as recovery lever; +6.7–12.5% success; task-level |
| The Handoff Tax (Ganz et al.) | 2608.24358 (Aug 2026) | Model-switching mid-trajectory; full-trajectory escalation recovers <50% of the quality gap | **Recovery across a handoff boundary is lossy** — direct evidence that boundary-crossing degrades recovery; single-agent lineage, not organizational |
| Language Model Teams as Distributed Systems (Mieczkowski et al.) | 2603.12229 (Mar 2026) | Position: use distributed-systems theory (the field that owns fault tolerance) as the foundation for LLM teams | Framing paper; invites exactly the classical↔LLM transfer the seed needs |
| Contemporary Agent Technology (Badica et al.) | 2509.02515 (Sep 2025) | LLM-driven vs classic MAS comparison | Context |

---

## 7. Answers to the assignment questions

### 7.1 What recovery strategies exist?

Seven families, all verified above:

1. **Inference-time self-correction** — reflection (Reflexion), self-feedback loops (Self-Refine), tool-validated critique (CRITIC), execution-grounded debugging (Self-Debug), anticipatory reflection. *Known to fail without external feedback* (Huang et al.; Kamoi et al.; Olausson et al.).
2. **Retry / replan** — retry-only, full replanning, targeted/budgeted recovery; the only matched-budget comparison is Self-Healing Orchestrators (2606.01416): targeted > retry-only > full replan at every budget; ReWOO shows plan-level decoupling gives tool-failure robustness; Plan-and-Act separates plan/execute.
3. **Runtime/harness containment** — undo + damage confinement (GoEX), deterministic re-routing (Self-Healing Router), mutation-gated verification (SABER), early stopping from trace structure (Automata, AUROC 0.94, fires at ~32% progress).
4. **Diagnosis-driven repair** — attribute then intervene (DoVer: 18–28%/49% of failed trials flipped; TRAJDEBUG: +10.8% on re-run; SearchAuditor: resume-with-repair; AgenTracer: +4.8–14.2% when feedback loops to MAS).
5. **Structural/organizational defenses** — topology choice (hierarchical most resilient, 2408.00989), Challenger/Inspector roles (recover ≤96.4% of injected errors), self-rectifying system composition (MAS², 2509.24323).
6. **Learning-based recovery** — RL on reflections (Reflect, Retry, Reward), trained retrospective models (SAMULE).
7. **Classical machinery** — checkpoint/rollback (with domino-effect cascade risk), microreboot (surgical component recovery), BFT replication + proactive recovery, sentinel/exception-handling services in open MAS (Klein & Dellarocas line), market-based self-healing (IAT 2007), topology self-repair (AAMAS-j 2020).

### 7.2 How are they evaluated?

- **Dominant paradigm:** task-level endpoint metrics — success rate / pass@1 / accuracy after recovery; % of failed trials flipped (DoVer); recovery-budget sweeps (2606.01416); attribution accuracy for diagnosis (Who&When, AgentRx, TRAJDEBUG, SearchAuditor).
- **Fault injection is established practice:** AutoTransform/AutoInject (2408.00989), replay-then-inject pipelines (Who&When Pro, AgenTracer), 100-task controlled injection (2606.01416), cross-layer propagation graphs from 72,550 real repair tickets (ADA-ST).
- **Robustness/resilience evaluations** express impact as *aggregate performance drop* under faults (2408.00989) or *population welfare under persistent shock* (2512.11689) — not as extent-of-spread.
- **AIOps benchmarks** (AIOpsLab, ITBench) evaluate the incident lifecycle (detect → localize → mitigate) in live environments — the closest thing to system-level recovery evaluation, but the system under repair is infrastructure, and the agents are the repairers, not the failing organization.

### 7.3 Is recovery evaluated at SYSTEM level (containing spread) or only task level?

**Almost entirely task level.** Verified exceptions and near-misses:
- ADA-ST (2607.16161) measures *propagation-edge coverage* across infrastructure layers — system-level spread measurement, wrong domain (GPU platforms, not agent organizations).
- Resilience-of-MAS (2408.00989) varies topology and measures degradation — system structure matters, but the metric is still aggregate task performance and the fault is a static injected agent.
- Cooperative Resilience (2512.11689) measures population-level recovery dynamics under ongoing shocks — system-level, but social-dilemma setting without roles/authority/tools.
- Agents of Chaos (2602.20021) documents cross-agent propagation qualitatively — no measurement framework.
- TRAJDEBUG's 7.62:1 ratio (local errors : critical errors) implies most faults are naturally contained — but nobody measures *which* faults escape, *through which boundary*, or *what containment would have cost*.

**No verified work measures:** number/identity of affected roles, agents, tools, memories, or artifacts after a fault; time-to-containment; boundary-crossing counts; collateral damage to unrelated tasks; integrity of the accountability chain after recovery; or the trade-off between containment strictness and preserved task utility. That is precisely the seed hypothesis's claim space.

---

## 8. Does anything here kill or subsume the seed hypothesis?

**No kill. Partial occupation to design around:**

1. **Failure attribution is occupied** (Who&When, AgenTracer, AgentRx, Who&When Pro, TRAJDEBUG, SearchAuditor, MAST) — the seed must not present diagnosis as its contribution. Note also Credit Without Ground Truth's negative result: LLM-judge/confidence credit signals ≈ chance vs causal replay — any attribution component must use interventional ground truth.
2. **Recovery-strategy comparison under fault injection is occupied for single orchestrators** (2606.01416: retry vs replan vs targeted, matched budgets) — the seed's novelty must be the *multi-agent organizational* setting and *spread* metrics, not the strategy comparison itself.
3. **Topology-resilience with faulty agents is occupied at the aggregate-performance level** (2408.00989) — the seed must go beyond "hierarchical is more robust" to boundary-typed propagation and containment mechanisms.
4. **"Self-healing" terminology is being colonized by applied 2026 papers** (2605.06737, 2606.01416, 2603.01548, 2604.27096, 2608.01955, X-SHIELD) — framing should use the organizational/cascading-failure vocabulary (which MASO topic 7 explicitly invites: "detection and mitigation of cascading, and systemic failures") rather than "self-healing agents."
5. **Inspect before submitting:** 2605.06737 (claims "reduces failure propagation" in a multi-agent workflow — mechanism/metric unknown from abstract; the single most likely reviewer-cited prior-art item). X-SHIELD is now resolved: it is recovery-*explanation* artifacts + N=10 user study (ENASE 2026, pp. 662–669), adjacent to auditability, not a propagation-measurement competitor.
6. **Classical exposure is heavy but manageable:** autonomic computing, ROC, microreboot, rollback-recovery (domino effect = classical blast radius), sentinel-based exception handling in open MAS (Klein & Dellarocas 1999–2003). The honest framing: the *machinery* is classical; the *open problem* is that LLM agents fail semantically, share natural-language state, and occupy organizational roles — so fault propagation crosses boundary types (authority, memory, accountability) that classical models don't have.

**Strengthening evidence for the seed found in this sweep:** ADA-ST's 49%-of-tickets-are-cross-layer finding (real-world dominance of boundary-crossing faults); TRAJDEBUG's 7.62:1 self-masking ratio (natural containment exists and is unstudied); Handoff Tax's <50% recovery across model handoffs (boundary-crossing degrades recovery); Agents of Chaos's observed cross-agent propagation in the wild; DoVer's multiple-valid-interventions finding (containment-point choice is real and underdetermined).

---

## 9. Verified reference list (all identifiers checked this sweep)

**Classical:** Kephart & Chess 2003 (10.1109/MC.2003.1160055); Ghosh et al. 2007 (10.1016/j.dss.2006.06.011); Computing survey 2010 (10.1007/s00607-010-0107-y); Candea et al. OSDI 2004 (USENIX, pp. 31–44); Candea et al. 2004 (10.1109/MC.2004.219); ROC agenda HPCA 2002 (10.1109/HPCA.2002.995714); Elnozahy et al. 2002 (10.1145/568522.568525); Castro & Liskov 2002 (10.1145/571637.571640); Klein & Dellarocas Agents'99 (10.1145/301136.301164); Klein & Dellarocas CSCW 2000 (10.1023/A:1008759413689); Dellarocas & Klein ICMAS 2000 (10.1109/ICMAS.2000.858440); Klein & Dellarocas AAMAS-j 2003 (10.1023/A:1024145408578); IAT 2007 economic self-healing (10.1109/IAT.2007.80); ISAP 2005 shipboard (10.1109/ISAP.2005.1599264); AAMAS-j 2020 topology self-healing (10.1007/s10458-020-09486-3). *Unverified: Koopman WADS 2003.*

**LLM single-agent:** 2210.03629 (ReAct); 2303.11366 (Reflexion); 2303.17651 (Self-Refine); 2304.05128 (Self-Debug); 2305.11738 (CRITIC); 2305.18323 (ReWOO); 2306.09896 (Self-Repair analysis); 2310.01798 (Cannot Self-Correct); 2406.01297 (TACL critical survey); 2404.06921 (GoEX); 2503.09572 (Plan-and-Act); 2505.15182 (ReflAct); 2505.24726 (Reflect-Retry-Reward); 2509.20562 (SAMULE).

**LLM MAS diagnosis/recovery:** 2503.13657 (MAST); 2505.00212 (Who&When); 2509.03312 (AgenTracer); 2512.06749 (DoVer); 2602.02475 (AgentRx); 2607.09996 (Who&When Pro); 2608.06346 (TRAJDEBUG); 2608.05212 (SearchAuditor); 2608.19760 (Credit Without Ground Truth); 2608.23670 (Automata from Traces); 2607.28802 (Model or Harness?); 2608.16411 (Risk-free Deployment); 2605.14892 (LIFE survey); 2511.04032 (Silent Failures); 2410.01242 (RGD); 2412.11713 (Seeker); 2509.24323 (MAS²).

**Self-healing-titled 2026:** 2606.01416 (Self-Healing Orchestrators); 2605.06737 (Self-Healing Framework, IJSEKE 2026, 10.1142/S0218194026500695); 2603.01548 (Self-Healing Router); 2604.27096 (Think-it-Run-it); 2608.01955 (Agentic Self-Healing Pipelines); X-SHIELD ENASE 2026 (10.5220/0015045500004015); 2607.16161 (ADA-ST).

**Resilience/containment/AIOps:** 2408.00989 (Resilience w/ Faulty Agents); 2512.11689 (Cooperative Resilience); 2602.20021 (Agents of Chaos); 2512.07850 (SABER); 2501.06706 (AIOpsLab); ITBench DSN-S 2025 (10.1109/dsn-s65789.2025.00060); RCAgent CIKM 2024 (10.1145/3627673.3680016); 2508.19504 (Aegis); 2608.24358 (Handoff Tax); 2603.12229 (LM Teams as Distributed Systems); 2509.02515 (Contemporary Agent Technology).

*Report ends. Verification performed 21 Sep 2026; channels: arXiv abs pages, Crossref, USENIX, arXiv title search. Semantic Scholar/OpenAlex/OpenReview/DBLP were rate-limited or bot-blocked from this network; a follow-up pass through those channels is recommended for citation-count data and any 2026 items not on arXiv.*
