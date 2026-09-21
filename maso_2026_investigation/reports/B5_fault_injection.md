# B5 — Fault Injection, Robustness, and Chaos Engineering for LLM Multi-Agent Systems

**Investigator:** B5 (Fault injection / robustness / chaos engineering landscape)
**Date:** 21 September 2026
**Mission:** Map MAS-FIRE, AgentChaos, IMACS-related work, chaos engineering / fault injection for agentic systems broadly, and robustness benchmarks. Answer: What fault models exist? What metrics? Do any measure CONTAINMENT or RECOVERY quality (not just task success under faults)? Do any use realistic organizational workflows? Adversarial stance toward the seed hypothesis ("organizational failure propagation and recovery in LLM MAS; organizational blast radius; containment/recovery mechanisms preserving task utility").

**Coordination note:** This report deliberately avoids re-covering the Jul–Sep 2026 preprint wave already mapped in `C2_arxiv_30d.md` and `C3_arxiv_90d.md` (e.g., Emergence World, Hallucination Snowball, Collective Loss of Control, SafeFlow, SymTrace/SymFail, ParaRecover). B5's unique contributions: (1) first deep verification of **MAS-FIRE** (Feb 2026 — outside C2/C3 windows; the single closest occupant of the seed's fault-injection territory), (2) full-text analysis of **AgentChaos** (ASE 2026), (3) independent verification of **IMACS**, (4) the classical chaos-engineering/fault-injection lineage, (5) newly found items not in C2/C3: **llmmas-otel (ICST 2026)**, **ToolMaze**, **ChaosEater**, the failure-attribution survey, and the LLM-for-CE sub-literature.

---

## 1. Bottom line

**The seed hypothesis is NOT killed by the fault-injection landscape, but its "fault injection + reliability evaluation for LLM MAS" scaffolding is now occupied twice over (MAS-FIRE, Feb 2026; AgentChaos, ASE 2026).** What remains unoccupied after this sweep:

1. **No fault-injection study measures blast radius / containment as a first-class metric on real LLM MAS.** The only work with literal containment metrics (containment rate, cascade depth, "blast radius", MTTD) is *Containing the Cascade* (ICERA 2026) — pure discrete-event simulation, zero LLM calls, no organizational semantics (verified by C3; Crossref re-verified here).
2. **Recovery is measured only as (a) local-error correction (MAS-FIRE's L_f), (b) recovery-conditional task success (MAS-FIRE's S_f), or (c) single-agent replanning (ToolMaze's PRR/RC).** No organizational recovery primitives (re-delegation, escalation, role reassignment, authority revocation) are injected, measured, or compared anywhere in this landscape.
3. **No fault-injection work uses genuinely organizational workflows.** MAS-FIRE's MetaGPT (software-company SOP pipeline) is the closest; AgentChaos uses generic debate/pipeline systems; IMACS has executable organizational structure (Belbin/Mintzberg/RACI) but injects no faults. **The cross product (org substrate × fault injection × containment/recovery measurement) is empty.**
4. Both anchor papers converge on the seed's premise empirically: topology/architecture dominates model capability for robustness (MAS-FIRE: closed-loop neutralizes >40% of faults that collapse linear pipelines; AgentChaos: robustness ranking is harness-determined, pipeline first-stage fault → −83.87pp pass@1). The seed can cite these as motivation, not as prior art that closes the question.

**Danger to the seed:** a proposal framed as "fault-injection benchmark for MAS reliability" is scooped. A proposal framed as "organizational blast radius + containment/recovery mechanism comparison on real organizational MAS" is not — provided it cites and differentiates MAS-FIRE, AgentChaos, and Containing-the-Cascade head-on.

---

## 2. Method and verification channels

- arXiv export API and Semantic Scholar API were rate-limited (HTTP 429) for most of the session (heavy swarm traffic from this host; documented in `raw/b7_arxiv_results.txt`). DBLP is behind an Anubis anti-bot challenge; OpenReview API intermittently challenged.
- Working channels used: **arxiv.org/abs and arxiv.org/html full texts via FetchURL** (MAS-FIRE and AgentChaos full papers read), **Google Scholar via FetchURL** (discovery + abstract verification), **Crossref API** (DOI metadata), **OpenReview search API** (one successful query), GitHub README (ToolMaze metrics).
- Every load-bearing paper below was inspected on its actual abstract page, full text, DOI record, or project page — not search snippets. Items whose identifiers could not be fully confirmed are explicitly flagged.

---

## 3. Core papers — deep verification

### 3.1 MAS-FIRE (the closest occupant)

| Field | Value |
|---|---|
| Title | MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems |
| Authors | Jin Jia, Zhiling Deng (equal contribution), Zhuangbin Chen (corresponding), Yingqi Wang, Zibin Zheng — Sun Yat-sen University, Zhuhai |
| Date/venue | arXiv v1, 23 Feb 2026. ACM-format preprint with placeholder conference block ("Woodstock, NY" template) — **no venue acceptance indicated**; 17 citations per Google Scholar (Sep 2026) |
| ID | arXiv:2602.19843 [cs.SE, cs.AI]; DOI 10.48550/arXiv.2602.19843 |
| Problem | MAS coordinate via unstructured natural language → semantic failures (hallucination, misinterpreted instructions, reasoning drift) propagate silently without runtime exceptions; outcome-only metrics (task success) cannot diagnose detection/recovery |
| Fault model | **15 injectable fault types in 7 categories.** Intra-agent: Planning (inexecutable plan, critical information loss), Memory (memory loss, context-length violation), Reasoning (hallucination), Action (tool selection error, parameter filling error, parameter format error). Inter-agent: Configuration (**role ambiguity**, **blind trust**), Instruction (logic conflict, ambiguity), Communication (message cycle, message storm, broadcast amplification) |
| Injection mechanisms | 3 non-invasive mechanisms: prompt modification (system/user prompts), interception + response rewriting (LLM-guided semantic mutation + rule-based structural mutation at middleware), message routing manipulation (programmatic) |
| Metrics | **System-level:** Robustness Score RS_f = success-under-fault / baseline-success. **Process-level:** O_f (detection/activation rate of fault-tolerant behavior), L_f (local recovery rate — immediate error fixed), S_f (end-to-end success given recovery triggered). The L_f–S_f gap explicitly captures "local recovery insufficient for global success" |
| Systems / data | MetaGPT (hierarchical SOP workflow, shared message pool, linear pipeline; HumanEval), Table-Critic (iterative critic-refiner closed loop; WikiTableQuestions, 400 sampled), Camel (bilateral role-play; WebShop). Models incl. GPT-5, DeepSeek-V3 |
| Major findings | (1) Stronger foundation models do NOT uniformly improve robustness (GPT-5's strict instruction-following collapses under Blind Trust: RS=6.32% vs DeepSeek-V3's 70.61%). (2) Topology is decisive: iterative closed-loop designs neutralize >40% of faults that cause catastrophic collapse in linear workflows; MetaGPT linear pipeline → RS as low as 0% under configuration/instruction faults. (3) Four-tier fault-tolerance taxonomy: Mechanism-level (retries, voting, redundancy), Rule-based (hardcoded filters — perfect O=L=100% on structural faults in MetaGPT), Prompt-level (role semantics), Reasoning-level (only defense vs semantic faults; O=100% but recovery varies). (4) Blind Trust defeats MetaGPT/Camel entirely (S_f=0%) |
| Author-stated limitations | None found in v1 text (no limitations section; some faults cannot be injected on some architectures — gray cells in Fig. 4) |
| Inferred limitations | Only 3 architectures, one per pattern; no containment/blast-radius metric (spread extent across agents is not measured — recovery is measured at the fault site, not across boundaries); no authority/delegation/accountability/human-boundary faults (role ambiguity and blind trust are the only "organizational" faults); no mechanism *interventions* compared — it characterizes inherent fault tolerance of existing systems rather than evaluating containment designs; no artifact/code link found in v1 |
| Relation to seed | **Occupies "fault injection + process-level reliability metrics for LLM MAS".** Its discussion (§6.2) even prescribes multi-source validation and inline verification checkpoints — i.e., containment-flavored mitigations — but as design advice, not measured interventions. Does NOT measure blast radius, does NOT vary organizational structure experimentally, does NOT study recovery mechanisms as the independent variable |

### 3.2 AgentChaos (ASE 2026 — the chaos-engineering occupant)

| Field | Value |
|---|---|
| Title | AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection |
| Authors | Gou Tan, Zhensu Sun, Jieke Shi, Ting Zhang, Zilong He, Qingfu Wu, Shuai Liang, Weifeng Sun, Junda He, Pengfei Chen, Chuanfu Zhang, Lwin Khin Shar, David Lo — SMU / Monash / Sun Yat-sen U / China Unicom |
| Date/venue | arXiv v1 7 Aug 2026; **accepted ASE 2026** (41st IEEE/ACM Int. Conf. on Automated Software Engineering, Munich, Oct 2026) |
| ID | arXiv:2608.06790 [cs.SE]; DOI 10.1145/3832783.3837437; **artifact on Zenodo** (Tan et al. 2026c, cited in §9 of paper) |
| Problem | LLM APIs return server errors, truncated responses, corrupted content that propagate downstream; existing injection is offline (AgenTracer, AutoInject), intrusive (MAS-FIRE — "requires adapting the injection logic to each system"), or cannot modify response fields (ChaosBlade, Rainmaker, CrashFuzz) |
| Fault model | Classical Avizienis et al. (2004) dependability taxonomy adapted to LLM API responses: **crash** (Error, Timeout), **omission** (Empty, Truncate), **value** (Corrupt, Schema) faults × {content, tool_calls} fields; plus compound scenarios reproducing real deployment failures (max-tokens+content-filter, API degradation, proxy HTML, wrong entity, stale cache/data, slow response) → **65 fault configurations**; injection strategies single/persistent/burst/intermittent × injection positions |
| Method | Runtime, non-intrusive HTTP-layer wrapper (all agent systems share the LLM API interface); post-hoc trigger verification filters untriggered tasks to avoid underestimating fault impact |
| Metrics | pass@1 and **Δpass@1** (triggered tasks only); resource consumption (0.71×–4.24× shifts); fault-diagnosis accuracy (type/step) for rule-based vs LLM-based diagnosis |
| Systems / data | AutoGen, MAD (multi-agent debate), MapCoder (pipeline), EvoMAC (iterative), Mini-SE — all reimplemented on Google ADK; HumanEval(+), MBPP, MMLU-Pro, MATH-500, SWE-bench Pro (300-sample subsets); backbones Claude-Sonnet-4.5, GPT-5.2, DeepSeek-V3.2, Seed |
| Major findings | All systems degrade (Δpass@1 up to 49.66pp; pipeline first-stage fault −83.87pp). Robustness ranking consistent across models → **harness/implementation, not model capability, determines robustness**. Iterative EvoMAC most robust; pipeline MapCoder most fragile. Content faults > tool-call faults (tool error-handling catches most). Omission faults (truncate/empty) as damaging as crashes but near-invisible (rule-based diagnosis of truncate: 4.3% type accuracy). Existing diagnosis <53% fault-type / <56% fault-step accuracy |
| Author-stated limitations | One system per architectural pattern (cannot separate pattern from instance); Δpass@1 misses partial correctness; RAG-style architectures uncovered; **no defenses evaluated — "future work will … design and evaluate defense strategies that validate LLM API responses before downstream use"** |
| Inferred limitations | Faults are API-transport-level (crash/omission/value on fields), not organizational or semantic-intent faults (hallucination classified but explicitly NOT injected — "originate in the model … our framework classifies them here but does not inject them"); no containment or recovery metrics; no organizational workflow |
| Relation to seed | Occupies "chaos engineering for agent systems" at a top SE venue, with the strongest engineering rigor in the space. Its own future-work statement (defense evaluation) is part of the seed's territory — but AgentChaos's fault layer and metrics would need organizational semantics to touch the seed's core |

### 3.3 IMACS (organizational substrate — independently verified)

| Field | Value |
|---|---|
| Title | Toward an Organizational Science of Multi-Agent LLM Systems: Decoupling Who, How, and Which Algorithm |
| Authors | Huan Chen, Xiang Song, Jian Jin, Pan Ren, Liang-Jie Zhang |
| Date/venue | arXiv v1, 28 Jul 2026; 8 pages; cs.AI/cs.LG; no venue indicated |
| ID | arXiv:2607.25446 |
| Content | IMACS (Intelligent Multi-Agent Collaboration System) separates organization (who), coordination (how), collaboration protocol (which algorithm) into orthogonal swappable layers; **Belbin roles, Mintzberg coordination mechanisms, RACI accountability as executable configuration**; six published collaboration algorithms behind a common interface; Adaptive Org Routing (contextual bandit) selects protocol per task under quality-cost tradeoff. Key mechanism finding: **accountability placement changes outcomes exactly when the protocol routes the deliverable through the accountable agent; winning placement flips across model families** |
| Relation to seed | The natural experimental substrate for the seed: organizational structure as a controlled variable, already built. But IMACS injects no faults and measures no failures — org science for *performance* only. The seed = IMACS-style org layers × MAS-FIRE-style injection × blast-radius/containment/recovery metrics (currently empty cross product) |

### 3.4 AutoInject / "Resilience with Faulty Agents" (ICML 2025)

| Field | Value |
|---|---|
| Title | On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents |
| Authors | Jen-Tse Huang, Jianxuan Zhou, Tailin Jin, Xuhui Zhou, Zirui Chen, Warren Wang, Youliang Yuan, Michael R. Lyu, Maarten Sap |
| Date/venue | arXiv v1 Aug 2024, v4 May 2025; **ICML 2025** |
| ID | arXiv:2408.00989 [cs.AI]; code+data released |
| Content | Two fault simulators: AutoTransform (corrupts agent profiles) and AutoInject (injects mistakes into responses). Structures: chain A→B→C, full-duplex A↔B↔C, hierarchical A→(B↔C). Hierarchical most resilient (5.5% drop vs 10.5%/23.7%). Defenses: **Challenger** (agents challenge each other) and **Inspector** (dedicated review agent) recover up to 96.4% of injected errors. 4 tasks, 6 systems |
| Relation to seed | The original "structure determines fault spread" result for LLM MAS, with actual defense mechanisms compared. But: 2–3 agent toy topologies, no organizational boundaries, no containment metrics (recovery = % errors corrected), no utility-cost tradeoff of defenses. Cited by both MAS-FIRE and AgentChaos as the offline/trace-level predecessor |

### 3.5 TAMAS (adversarial robustness benchmark)

| Field | Value |
|---|---|
| Title | TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems |
| Authors | Ishan Kavathekar, Harshit Jain, Aditya Rathod, Ponnurangam Kumaraguru, Tanuja Ganu |
| Date/venue | arXiv v1, 7 Nov 2025; **ICML 2025 MAS Workshop** |
| ID | arXiv:2511.05269 [cs.MA] |
| Content | 5 scenarios, 300 adversarial instances, 6 attack types, 211 tools, 100 harmless tasks; AutoGen + CrewAI, 10 backbone LLMs, 3 interaction configs; **Effective Robustness Score (ERS)** trading safety vs task effectiveness. MAS highly vulnerable to adversarial attacks |
| Relation to seed | Adversarial (intentional sabotage) not endogenous faults; ERS is a safety-utility tradeoff metric — a template the seed's containment-vs-utility tradeoff can cite. No containment/recovery mechanisms |

---

## 4. Newly found items (not in C2/C3 reports)

| Paper | Venue/Date | ID | Content | Relevance |
|---|---|---|---|---|
| **Observability and Fault Injection for LLM-Based Multi-Agent Systems in SE (llmmas-otel)** — Seyedghorban, Klimov, van Deursen, Panichella, Ozkan (TU Delft) | **ICST 2026** | DOI 10.1109/icst69053.2026.00037 | OpenTelemetry tracing + targeted fault injection at interaction points (workflow phases, agent steps, inter-agent communication, tool calls, LLM invocations); baseline-vs-faulty trace comparison; tool paper, demo validation | Third occupant of "fault injection for LLM MAS" — infrastructure/tooling angle. No metrics beyond trace alignment; no containment/recovery |
| **ToolMaze: When Tools Fail** — Zhu, Ma, Shen, Li, Zhao, Wang, Yan, Yin | arXiv 2026 (Scholar: 14 citations) | arXiv:2606.05806; code: github.com/Zhudongsheng75/ToolMaze | DAG-topological complexity (C1–C4) × tool perturbation taxonomy (explicit/implicit × transient/permanent, P0–P4). **Metrics: TSR, Perturbation Recovery Rate (PRR = recoveries/hits), Recovery Cost (RC vs oracle suffix cost)**. PRR drops ~37% under implicit semantic faults; systemic over-trust in corrupted outputs; fault-tolerance scales slower than task ability | **The only verified benchmark with explicit recovery-quality metrics (PRR, RC)** — but single-agent tool-use, no MAS, no organizational dimension |
| **ChaosEater** — Kikuta, Ikeuchi, Tajiri (NTT) | arXiv Jan 2025; journal version in *Automated Software Engineering* (Springer) 2025 | arXiv:2501.11107 (via Google Scholar record); 9 citations | LLM agents automate the entire chaos-engineering cycle (hypothesis → experiment design → execution → analysis) for **Kubernetes systems** | Direction inversion: LLM-*driven* CE of traditional systems, not CE *of* LLM agents. Shows CE methodology is being agentified — expect reviewer familiarity |
| **From Failure Attribution to Reliability Enhancement in LLM-based MAS: A Survey** | OpenReview, cdate ≈ May 2026 | OpenReview note RbhZpFJAjY | Formalizes attribution as 5Ws (What/When/Who/Where/Why) over traces; 4 method paradigms; adds "How" = runtime intervention + post-hoc refinement | Survey-level occupation of attribution→intervention framing; attribution saturated (agrees with C2) |
| **AgenTracer** — Zhang et al. | **ICLR 2026** (proceedings.iclr.cc) | via Scholar; 99 citations | Programmatic fault injection (counterfactual + perturbed traces) to build failure-attribution training data; AgenTracer-8B tracer model | Uses fault injection as *data generation for attribution*, not reliability evaluation. Attribution cluster — avoid as primary contribution |
| **Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows (AgentFail)** — Ma, Xie, Wang, Wang, Wu, Li et al. | arXiv 2025 | arXiv ID unconfirmed (Scholar-verified) | 307 annotated failure logs from Dify/Coze low-code platform workflows; failure lifecycle taxonomy | Closest to "realistic organizational-ish workflows" in the observational literature — production platform workflows, but no injection, no containment |
| **LLMGuard: Multi-Agent Fault Diagnosis for Reliable LMaaS** — Zhong, Yu, Huang, Fu, Ren et al. | **DSN 2026** (IEEE/IFIP Dependable Systems & Networks) | via Scholar | Multi-agent fault *diagnosis* for LLM-as-a-service | Dependability-venue interest in LLM-MAS faults; diagnosis only |
| **OperAID** — de Castro, Vandikas, Ferlin et al. | IEEE conf 2026 | via Scholar | LLM agents for autonomous Kubernetes fault remediation; closed-loop fault injection → diagnosis → remediation | Agentic *AIOps*: agents as reliability operators of cloud systems, not the subject of faults |
| **FTDI: Budget-Aware Self-Healing for Resilient LLM MAS Code Generation** — Men, Tong, Zuo, Lu | SSRN 2026 (unrefereed) | SSRN 6387100 | Parameterized fault injection + self-healing for MAS code generation; recovery-efficiency metrics | Low-tier, but signals "self-healing MAS under injection" is being attempted; watch for upgrades |
| **VRRF: Validation and Recovery Reliability Framework** — Zhao | SSRN 2026 (unrefereed) | SSRN 7444279 | "A fault-injection study can only measure an agent if the injected fault is survivable" — validation+recovery reliability for tool-enabled agents | Single-agent; methodological point worth citing on fault-survivability design |
| **Efficient Forecasting of Task Failures via Adaptive Fault Injection** — Sengar et al. | OpenReview (Forecasting workshop) | via Scholar | Adaptive fault injection to train failure forecasting; Who&When weighted-F1 78.01 | Injection as training signal for prediction, not containment |
| **When Agentic Executions Fail: Detecting and Localizing Runtime Faults from Telemetry** — Zhang et al. | arXiv 2026 | via Scholar | Telemetry-based runtime fault detection/localization; notes adaptation of chaos-engineering ideas (tool unavailability, latency, hangs, incorrect responses) to agentic systems | Detection/localization cluster |
| **Belayer** — Zhou et al. | arXiv:2608.14635, 2026 | arXiv-verified ID via Scholar record | Fault tolerance for agentic RL *training* infrastructure; non-intrusive runtime fault-injection tool; fine-grained context recovery | Infrastructure fault tolerance (training), not MAS task-level reliability |

---

## 5. Classical lineage (verified via Crossref)

| Work | ID | Content | Lesson for the seed |
|---|---|---|---|
| Hsueh, Tsai, Iyer, "Fault Injection Techniques and Tools", *IEEE Computer* 1997 | DOI 10.1109/2.585157 | Classical fault-injection survey (hardware/simulation/software-implemented) | Fault-model representativeness question is 30 years old — grounds the "are LLM-MAS faults realistic?" discussion |
| Avizienis, Laprie, Randell, Landwehr, "Basic Concepts and Taxonomy of Dependable and Secure Computing", *IEEE TDSC* 2004 | DOI 10.1109/tdsc.2004.2 | The fault-error-failure chain; crash/omission/value classification | AgentChaos's taxonomy source; the seed's "organizational blast radius" maps to error-propagation analysis in this canonical vocabulary |
| Basiri et al., "Chaos Engineering", *IEEE Software* 2016 | DOI 10.1109/ms.2016.60 | Netflix lineage; steady-state hypothesis, real-world event injection in production | CE's defining metric is *steady-state deviation*, not pass/fail — the seed's utility-preservation framing is native CE thinking |
| Blohowiak et al., "A Platform for Automating Chaos Experiments", ISSREW 2016 | DOI 10.1109/issrew.2016.52 | Netflix's automation platform (ChAP) | Precedent for controlled blast-radius-limiting experiments (canary scope) in industry CE |
| Alvaro, Rosen, Hellerstein, "Lineage-driven Fault Injection", SIGMOD 2015 | DOI 10.1145/2723372.2723711 | LDFI: use data lineage to find fault-injection points that maximally test fault-tolerance | Directly transferable idea: lineage/provenance graphs of MAS message flow → minimal fault sets that expose containment gaps. Nobody has done LDFI-for-LLM-MAS |
| ChaosBlade (GitHub, chaosblade-io/chaosblade) | tool | OS/container/network-layer injection | AgentChaos's contrast class: infra tools cannot touch LLM response semantics |
| "Ten Years of Chaos Engineering… Now What?" — Owotogbe, Fossati, Kumara et al. / Di Nucci, Tamburri | IEEE Internet Computing / Computer 2026 (via Scholar) | Decade retrospective of CE | CE is mature and looking for new frontiers — agentic systems are a natural one; good positioning citation |
| Sharma, *Observability for Large Language Models: SRE and Chaos Engineering for AI at Scale* (Apress 2026) | DOI 10.1007/979-8-8688-2827-0 (book; chapters 12–14 on CE for LLMs) | Practitioner book with "Chaos Experiments for LLMs" | Practitioner literature has arrived; academic novelty must go beyond "apply CE to LLM systems" |

---

## 6. Answers to the assignment's four questions

### Q1. What fault models exist?

| Fault model | Source | Layer | Fault classes | Organizational? |
|---|---|---|---|---|
| MAS-FIRE taxonomy | arXiv:2602.19843 | Prompt / response / message-routing | 15 types: planning, memory, reasoning, action, configuration (role ambiguity, blind trust), instruction, communication (cycle/storm/broadcast) | **Partially** — role ambiguity + blind trust are the only org-flavored faults; no authority/delegation/accountability/human-boundary faults |
| AgentChaos taxonomy | arXiv:2608.06790 | LLM API response (HTTP) | crash/omission/value × {content, tool_calls} + compound deployment scenarios (65 configs) | No |
| AutoTransform/AutoInject | arXiv:2408.00989 | Agent profile / response content | "Clumsy or malicious agent" error injection | No |
| TAMAS | arXiv:2511.05269 | Adversarial inputs | 6 attack types (intentional sabotage) | No (adversarial, not endogenous) |
| ToolMaze perturbations | arXiv:2606.05806 | Tool outputs | explicit/implicit × transient/permanent (P0–P4) on DAG-structured tool tasks | No (single-agent) |
| MAST (observational) | arXiv:2503.13657 | — (taxonomy of *natural* failures) | 14 failure modes in 3 categories (system design, inter-agent misalignment, task verification); 1600+ traces, κ=0.88 | Partially (inter-agent misalignment) — but observational, not injectable |
| llmmas-otel | ICST 2026 | OpenTelemetry spans | Targeted injection at interaction points (tool paper; fault set not taxonomized) | No |
| Classical | Avizienis 2004; Hsueh 1997 | Hardware/OS/network | crash, omission, value, timing, Byzantine | No |

### Q2. What metrics exist?

| Metric family | Metrics | Used by |
|---|---|---|
| Outcome robustness | pass@1 / Δpass@1; Robustness Score RS_f; Effective Robustness Score (safety-utility); pass^k (consistency over trials) | AgentChaos; MAS-FIRE; TAMAS; τ-bench (arXiv:2406.12045) |
| Process-level detection/recovery | **O_f (fault-tolerance activation), L_f (local recovery), S_f (recovery-conditioned global success)** | **MAS-FIRE only** |
| Recovery quality | **PRR (perturbation recovery rate), RC (recovery cost vs oracle)** | **ToolMaze only (single-agent)** |
| Containment / spread | containment rate, cascade depth, **blast radius**, MTTD | **Containing the Cascade (ICERA 2026) only — simulation, no LLM calls** (C3 Tier-1; Crossref re-verified here: DOI 10.1109/ICERA72709.2026.11666599) |
| Diagnosis/attribution | fault-type/step accuracy; Who&When agent/step accuracy | AgentChaos (<53%/<56%); Who&When (arXiv:2505.00212; 53.5%/14.2%) |
| Defense effectiveness | % errors recovered (Challenger/Inspector: up to 96.4%) | AutoInject paper |

### Q3. Do any measure CONTAINMENT or RECOVERY quality (not just task success under faults)?

- **Recovery: yes, partially.** MAS-FIRE's (O_f, L_f, S_f) triplet is the most sophisticated verified recovery measurement on real LLM MAS — but it measures recovery *at the fault site*, not containment of spread, and compares no recovery *mechanisms* (it catalogs emergent behaviors of fixed systems). ToolMaze's PRR/RC are genuine recovery-quality metrics but single-agent. AutoInject's Inspector/Challenger compare two defenses (% errors recovered) on toy topologies.
- **Containment / blast radius: only in simulation.** Containing the Cascade (ICERA 2026) has the literal metric set (containment rate, cascade depth, blast radius, MTTD) and a mediator with circuit breaker + checkpoint rollback — but zero LLM calls, no organizational semantics, low-tier venue. **On real LLM MAS, no verified work measures how far a fault spreads (agents/boundaries touched) or whether a mechanism limits that spread while preserving utility.**

### Q4. Do any use realistic organizational workflows?

- **MAS-FIRE's MetaGPT** (software-company SOPs, role hierarchy, shared message pool) is the closest to an organizational workflow among fault-injection studies — but the org structure is fixed, not an experimental variable.
- **AgentChaos**: generic systems (debate, pipeline, iterative) on standard benchmarks — not organizational.
- **IMACS**: executable org theory (Belbin/Mintzberg/RACI) with controlled org variation — but no faults.
- **AgentFail** (Dify/Coze production platform workflows): realistic workflows, observational only.
- **Verdict: no verified work injects faults into an organizational workflow where org structure is the controlled variable.**

---

## 7. Does anything here kill or subsume the seed hypothesis?

**Kill: No. Subsume: the generic scaffolding, yes; the organizational core, no.**

- **Occupied (must cite + differentiate):** "fault injection + reliability evaluation for LLM MAS" (MAS-FIRE, Feb 2026, 17 citations); "chaos engineering for agent systems" (AgentChaos, ASE 2026 + Zenodo artifact); "structure determines fault spread + simple defenses" (AutoInject, ICML 2025); "containment metrics incl. blast radius" (Containing the Cascade, ICERA 2026 — simulation only); fault-injection tooling (llmmas-otel, ICST 2026); adversarial robustness benchmarks (TAMAS).
- **Empty cross product (the seed's defensible core, confirmed by this landscape):** organizational boundary types (role, authority/delegation, accountability, memory, human-agent) as the *measured units* of blast radius × real LLM MAS execution × containment/recovery *mechanism comparison* × utility-preservation tradeoff. MAS-FIRE has injection+process metrics but no org variation or containment; AgentChaos has engineering rigor but API-level faults and no recovery metrics; IMACS has org variation but no faults; Containing-the-Cascade has the metrics but no real system. Nobody joins these.
- **Transferable classical idea not yet applied:** lineage-driven fault injection (Alvaro 2015) over MAS message/provenance graphs to *select* minimal fault sets that expose containment gaps — a methodological differentiator available to the seed.
- **Collision warning:** AgentChaos's stated future work ("design and evaluate defense strategies that validate LLM API responses") and FTDI-style "self-healing MAS" preprints are moving toward mechanism evaluation; the window for mechanism-comparison framing is open but not indefinitely.

---

## 8. Verification log

| Item | Channel | Date |
|---|---|---|
| MAS-FIRE arXiv:2602.19843 — abstract page + full HTML text (taxonomy, metrics, results, discussion read in full) | arxiv.org/abs + arxiv.org/html via FetchURL | 21 Sep 2026 |
| AgentChaos arXiv:2608.06790 — abstract page + full HTML text (taxonomy, 65 configs, Tables 3–8, RQs, threats to validity, related work, Zenodo artifact ref) | arxiv.org/abs + arxiv.org/html via FetchURL | 21 Sep 2026 |
| IMACS arXiv:2607.25446 — abstract page | arxiv.org/abs via FetchURL | 21 Sep 2026 |
| AutoInject/resilience arXiv:2408.00989 — abstract page | arxiv.org/abs via FetchURL | 21 Sep 2026 |
| TAMAS arXiv:2511.05269 — abstract page | arxiv.org/abs via FetchURL | 21 Sep 2026 |
| MAST arXiv:2503.13657; Who&When arXiv:2505.00212; τ-bench arXiv:2406.12045 — abstract pages | arxiv.org/abs via FetchURL | 21 Sep 2026 |
| ChaosEater arXiv:2501.11107 (Kikuta/Ikeuchi/Tajiri; journal version in *Automated Software Engineering* 2025) | Google Scholar record via FetchURL | 21 Sep 2026 |
| ToolMaze arXiv:2606.05806 — abstract (Scholar) + full metric definitions (GitHub README) | Scholar + github.com/Zhudongsheng75/ToolMaze via FetchURL | 21 Sep 2026 |
| llmmas-otel ICST 2026 — DOI metadata (Crossref) + abstract (Scholar) | Crossref + Scholar | 21 Sep 2026 |
| Containing the Cascade ICERA 2026 — Crossref DOI record re-verified (title/authors/venue/date); full text NOT inspected (Zenodo 403, same as C3) | Crossref | 21 Sep 2026 |
| Classical: Hsueh 1997 (10.1109/2.585157), Avizienis 2004 (10.1109/tdsc.2004.2), Basiri 2016 (10.1109/ms.2016.60), Blohowiak 2016 (10.1109/issrew.2016.52), Alvaro 2015 (10.1145/2723372.2723711), Sharma book 2026 (10.1007/979-8-8688-2827-0) | Crossref | 21 Sep 2026 |
| AgenTracer (ICLR 2026), AgentFail (arXiv 2025, ID unconfirmed), LLMGuard (DSN 2026), OperAID, FTDI (SSRN 6387100), VRRF (SSRN 7444279), Belayer arXiv:2608.14635, failure-attribution survey (OpenReview RbhZpFJAjY) | Google Scholar / OpenReview search API | 21 Sep 2026 |
| Blocked channels: arXiv export API (persistent 429 under swarm load), Semantic Scholar API (429), DBLP (Anubis challenge), Zenodo (403) | — | 21 Sep 2026 |
