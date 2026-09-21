# B10 — Organizational Multi-Agent Systems: Landscape Map

**Investigator:** B10 specialist (adversarial evidence-gathering)
**Date:** 2026-09-21
**Assignment:** Map "Toward an Organizational Science of Multi-Agent LLM Systems" and all work treating LLM MAS as organizations (org design, hierarchy vs flat, division of labor, span of control, organizational routines, classical MAS org models MOISE/AGR/OperA and their LLM-era revival). Is organizational-structure-vs-failure-resilience studied?

**Verification note:** arXiv API, Semantic Scholar API, DBLP, and OpenAlex were intermittently hard rate-limited (429) from this IP. All papers below were verified by inspecting the actual arXiv abstract page (FetchURL on arxiv.org/abs/...), the DataCite API (which indexes arXiv DOIs), the Crossref API, the HAL open-archive API, or publisher pages (Cambridge Core). Items that could not be fully verified are explicitly flagged.

---

## 1. Bottom line

The "organizational science of LLM MAS" is a **real, active, and rapidly crowding landscape as of mid/late 2026**, but it is almost entirely organized around **performance and cost**, not **failure propagation and recovery**. The seed hypothesis ("what determines organizational blast radius, and which containment/recovery mechanisms minimize systemic impact while preserving utility") is **partially occupied at its core** by three papers — Zhou et al.'s *On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents* (structure × faulty agents × defenses), Kim et al.'s *Towards a Science of Scaling Agent Systems* (architecture × error amplification), and CTHA (hierarchical constraints × failure cascades) — but **none of them operationalizes "blast radius" across organizational boundaries** (role, authority/delegation, tool, memory, accountability, human-agent), none studies **recovery** as a first-class mechanism, and all use small teams and benchmark QA-style tasks rather than organizational workflows. The classical MAS organization literature (MOISE, AGR, OperA, Horling & Lesser, Carley) is **barely revived**: two flagship LLM-MAS surveys cite none of it; the revival that exists is thin and recent (2024–2026). "Span of control" and "organizational routines" are essentially **unstudied** in LLM MAS.

---

## 2. The anchor paper

### Toward an Organizational Science of Multi-Agent LLM Systems: Decoupling Who, How, and Which Algorithm (IMACS)
- **arXiv:** 2607.25446 (v1, 28 Jul 2026). Authors from Shunfeng Technology Co. and Shenzhen University (submission by Huan Chen). 8 pages.
- **Problem:** LLM MAS frameworks entangle three concerns: organization (WHO: roles, model bindings, accountability), coordination (HOW: Mintzberg's five mechanisms), collaboration protocol (WHICH algorithm: debate, voting, MoA, etc.).
- **Method:** IMACS framework — organizations declared in YAML grounded in **Belbin's nine team roles**, **Mintzberg coordination mechanisms**, **RACI accountability tags** (validated at-most-one-Accountable constraint); six published protocols (voting, MoA, LLM-Blender, debate, Reflexion, plan-execute) behind one interface on AgentScope 2.0; "Adaptive Org Routing" = LinUCB contextual bandit selecting protocol per task under quality−λ·cost.
- **Experiments:** Controlled RACI ablations (3 repeats, N=10 items/cell) on GSM8K, HumanEval, HotpotQA, AgentsNet, AlpacaEval; simulated-oracle routing study (T=400) plus small real-reward runs.
- **Findings:** (i) Organization is a real independent lever — fixed protocol moves up to 0.20 exact-match across org presets; (ii) accountability placement matters **exactly when the protocol routes the deliverable through the accountable agent** (Blender yes, MoA/voting/debate no) — a mechanistic, replicated, sign-consistent effect; (iii) the winning placement **flips across model families** → org design cannot be hard-coded, must be revalidated/learned per model binding; (iv) router beats all fixed protocols on the simulated oracle (82% routing accuracy).
- **Author-stated limitations:** small-N real runs (N=10/cell, 3 repeats), simulated oracle for headline routing result, English-centric features, no long-horizon tool use / human approval loops / changing external state.
- **Inferred limitations:** Belbin/Mintzberg/RACI are *management-science* constructs, not computational org models; no fault injection, no failure propagation, no recovery; "organization" = static role/RACI assignment, not structure (no hierarchy depth, span of control, or reporting graph); single-owner RACI constraint is the only validated invariant.
- **Code:** released with paper (per abstract).
- **Relation to seed:** Establishes org-variables-as-independent-lever methodology and shows accountability placement has causal, mechanism-specific effects — directly usable framing. But it studies **performance/cost only, zero failure/resilience content**. It is a complement, not a killer.

---

## 3. Landscape map (all verified)

### 3.1 Org-design-as-configuration / governance structure (LLM era)

| Paper | ID | Year/Venue | Core idea | Relation to seed |
|---|---|---|---|---|
| IMACS (anchor) | arXiv:2607.25446 | 2026 preprint | Belbin/Mintzberg/RACI as executable config; org × protocol ablation | Methodological template; no failure study |
| **When Agents Evolve, Institutions Follow** (Fei, Guo, Xiao) | arXiv:2604.27691 | 2026 preprint | 7 historical political institutions (4 governance patterns) compiled into executable MAS architectures; "who proposes, reviews, executes, **how errors are corrected**"; best–worst institution gap >57pp within one model; optimum shifts with model capability and task | Closest "org form" sweep; includes error-correction as design dimension but evaluates task performance, not fault containment |
| **Loop-Back Authority in LLM Agent Teams** (Zohrehvand) | arXiv:2609.14767 | 13 Sep 2026 preprint | Paired experiment (43 paired products, 86 runs) holding 5 agents fixed, varying only the Manager's reject/revise authority link. **Flat beats hierarchical on Utility (d=0.42, p=0.009) and Clarity (d=0.34, p=0.030)**; hierarchical reports hedge 53% more; supervisor tier costs 51.5% more tokens for no quality gain; "a supervisor pays for itself when it can verify and becomes a liability when it can only opine" | Direct hierarchy-vs-flat causal evidence; authority link as the unit of analysis. Cites MOISE+ and Horling & Lesser (revival evidence). Performance-focused, no faults |
| **Organizational Control Layer (OCL)** (Liu et al.) | arXiv:2606.04306 | 2026 preprint | Governance layer at the execution boundary: intercepts agent-proposed actions, checks role/policy/economic constraints, approve/revise/block/escalate. Adversarial buyer–seller (AgenticPay): unsafe executions 88%→0%, valid success 12%→96% | Containment at the **tool/action boundary** — one seed dimension; single-agent-boundary focus, not propagation across an org graph |
| Semantic Consensus Framework (Acharya) | arXiv:2604.16339 | 2026 preprint | Enterprise MAS failure rates 41–86.7%, ~79% from specification/coordination issues; "Semantic Intent Divergence"; process-aware middleware with policy–authority–temporal hierarchy; 600 runs over AutoGen/CrewAI/LangGraph | Failure taxonomy-ish + governance middleware. Inferred limitation: conflict detection 65.2% recall at 27.9% precision is weak; "100% vs 25.1% workflow completion" claim warrants skepticism |
| Unaccountable Delegation, Fading Skills (La Malfa et al.) | arXiv:2608.08601 | 2026 preprint | 15-category workplace-AI-agent risk taxonomy from 8,356 O*NET-derived scenarios validated with 45 workers; "Erroneous Agent Actions" largest/severe category, many at the **human–agent boundary**; automation→organizational risks, augmentation→worker risks | Human–agent boundary risks; taxonomy only, no experiments on propagation |
| Institutional AI (governance framework) | arXiv:2601.10599 | 2026 preprint | Governance framework for "distributional AGI" (cites MOISE+) | Conceptual; not experimental |

### 3.2 Topology/structure optimization (structure as a performance/cost variable)

| Paper | ID | Venue | Core idea |
|---|---|---|---|
| MacNet — Scaling LLM-based Multi-Agent Collaboration (Qian et al.) | arXiv:2406.07155 | ICLR 2025 | DAG "collaboration networks" >1000 agents; **irregular topologies outperform regular ones**; logistic collaborative scaling law |
| GPTSwarm (Zhuge et al.) | arXiv:2402.16823 | ICML 2024 | Agents as optimizable computational graphs; edge optimization = orchestration search |
| DyLAN (Liu et al.) | arXiv:2310.02170 | COLM 2024 | Dynamic team selection (Agent Importance Score) + dynamic communication structure |
| AgentPrune — "Cut the Crap" (Li et al.) | arXiv:2410.02506 | 2024 preprint (ICLR 2025) | One-shot spatial-temporal pruning of message-passing graph; defends 2 adversarial attack types (+3.5–10.8%) |
| G-Designer (Zhang et al.) | arXiv:2410.11782 | 2024–25 preprint | VAE designs task-adaptive communication topology; adversarial robustness (0.3% accuracy drop under attack) |
| MaAS (Zhang et al.) | arXiv:2502.04180 | 2025 preprint | Agentic supernet; query-dependent architecture sampling; 6–45% of inference cost |
| MAS-Zero | arXiv:2505.14996 | 2025 preprint | Zero-supervision MAS design (self-play) |
| AFlow | arXiv:2410.10762 | 2024 preprint (ICLR 2025) | Monte Carlo tree search over agentic workflows |
| ADAS — Meta Agent Search (Hu, Lu, Clune) | arXiv:2408.08435 | 2024 preprint | Meta-agent programs new agents in code; archive of designs |
| AgentSquare | arXiv:2410.06153 | 2024 preprint | Modular design space (planning/reasoning/tools/memory) search |
| SwarmAgentic | arXiv:2506.15672 | 2025 preprint | Swarm-intelligence generation of agentic systems |

**Assessment:** This cluster treats structure as a *performance/cost* optimization variable. Robustness appears only as adversarial-attack defense (AgentPrune, G-Designer), not as fault containment/recovery. None cites MOISE/AGR/OperA.

### 3.3 Hierarchy vs flat / coordination structure comparisons

| Paper | ID | Venue | Finding |
|---|---|---|---|
| **Towards a Science of Scaling Agent Systems** (Kim et al., MIT/Google et al.) | arXiv:2512.08296 | Dec 2025 preprint (v3 Apr 2026) | 260 configs × 6 benchmarks × 5 architectures (Single, Independent, Centralized, Decentralized, Hybrid) × 3 LLM families. **Trace-level error amplification: Independent 17.2×, Decentralized 7.8×, Hybrid 5.1×, Centralized 4.4×, Single 1.0×** — "architectures without centralized verification propagate errors more." Capability ceiling: MAS hurts when single-agent >45% accuracy. Performance +80.8% (decomposable finance) to −70.0% (sequential planning). **Adversarial nuance: after controlling for other coordination metrics, error amplification's main effect is NOT significant (p=0.658)** — architecture effects are better explained by efficiency/overhead. Predicts best architecture for 87% held-out configs |
| MultiAgentBench (Zhu et al.) | arXiv:2503.01935 | ACL 2025 | Benchmark with milestone KPIs; evaluates **star, chain, tree, graph** coordination topologies; graph best in research scenario |
| AgentsNet (Grötschla et al.) | arXiv:2507.08616 | 2025 preprint | Distributed-systems-inspired benchmark: agents must self-organize protocols over a network topology; frontier LLMs degrade as network scales to 100 |
| Loop-Back Authority | arXiv:2609.14767 | 2026 | See §3.1 — flat > hierarchical on open-ended work when supervisor cannot verify |
| Exploring Collaboration Mechanisms for LLM Agents: A Social Psychology View (Deng et al.) | arXiv:2310.02124 | ACL 2024 | 4 "societies" varying agent traits × thinking patterns; conformity/consensus emerge |
| More Agents Is All You Need (Li et al.) | arXiv:2402.05120 | 2024 preprint | Sampling-and-voting (flat ensemble) scales performance |

### 3.4 Role-based division of labor frameworks (SOPs ≈ organizational routines)

| Paper | ID | Venue | Note |
|---|---|---|---|
| MetaGPT (Hong et al.) | arXiv:2308.00352 | ICLR 2024 | SOPs encoded as role pipeline; **cites AGR (Ferber & Gutknecht 1998)** — rare classical-org citation |
| ChatDev (Qian et al.) | arXiv:2307.07924 | ACL 2024 | Waterfall software-company roles |
| AutoGen (Wu et al.) | arXiv:2308.08155 | COLM 2024 | Conversational agents framework |
| MegaAgent (Wang et al.) | arXiv:2408.09955 | 2024–25 preprint | No predefined SOPs; dynamic task decomposition; 590-agent policy simulation |
| SoA — Self-Organized Agents (Ishibashi & Nishimura) | arXiv:2404.02183 | 2024 preprint | Agents self-multiply with problem complexity; constant per-agent code load (implicit span-of-control-like invariant, but never framed as such) |
| HAS — Hierarchical Auto-Organizing System | arXiv:2403.08282 | ICLR 2024 WS | Centralized planning + decentralized execution in Minecraft |
| AgentScope (Gao et al.) | arXiv:2402.14034 | 2024 preprint | Platform with built-in **fault-tolerance mechanisms** (message-level retry/validation), actor-based distribution |

### 3.5 Organizational behavior simulation (LLM agents as org members)

| Paper | ID | Venue | Note |
|---|---|---|---|
| CareerAgent — Holacracy simulation (Zhu et al.) | arXiv:2408.11826 | 2024 preprint | Generative OB simulation of a Holacracy; competence ↑ reduces stress but hurts task completion; sub-communities form around competent members |
| The Politician, the Liar, and the Obedient Worker (Babaei et al.) | arXiv:2608.09574 | Aug 2026 preprint | Hierarchical Game (public goods + managerial authority + elections + private comms), 6 frontier models, 12 experiments; honesty fragile when manager role salaried; anonymous punishment → cheating; same-family groups entrench incumbents |
| I Want to Break Free! (Staiano et al.) | arXiv:2410.07109 | 2024–25 | Stanford-Prison-inspired guard/prisoner hierarchy; 2,400 conversations, 6 LLMs; anti-social behavior emerges without negative prompts |
| TheAgentCompany (Xu et al.) | arXiv:2412.14161 | 2024–25 | Simulated software company; best agent completes 30% of tasks |
| AgentSociety (Piao et al.) | arXiv:2502.08691 | 2025–26 | 10k+ agents, 5M interactions; social experiments (polarization, shocks) |
| Generative Agents (Park et al.) | arXiv:2304.03442 | UIST 2023 | 25-agent town simulacra |
| Project Sid (Altera) | arXiv:2411.00114 | 2024 | Many-agent civilization simulations |

### 3.6 Failure, resilience, error attribution (the seed-relevant cluster)

| Paper | ID | Venue | What it does | What it lacks vs seed |
|---|---|---|---|---|
| **On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents** (Zhou, Jin, Zhou, Chen, Wang, Yuan, Lyu, Sap; CUHK/Tsinghua/CMU et al.) | arXiv:2408.00989 | 2024–25 preprint | **THE closest prior work.** Q: resilience of system *structures* under faulty agents. Fault injection via AutoTransform (subtle mistakes) & AutoInject (explicit errors). 6 systems (MetaGPT, CAMEL, MAD, AgentVerse, Self-collab, +1) mapped onto **linear / flat / hierarchical** 3-agent patterns; 4 tasks (code/HumanEval, math, translation, text evaluation). **Hierarchical most resilient: 5.5% drop vs 10.5% (linear) and 23.7% (flat).** Defenses: **Challenger** (peer challenge) and **Inspector** (review agent) recover up to 96.4% of injected errors. Code public (CUHK-ARISE/MAS-Resilience) | 3-agent toy patterns; structure entangled with framework prompts (authors admit); faults are response mistakes only — no authority/tool/memory/accountability boundary crossing; no recovery dynamics over time; no blast-radius metric |
| **CTHA — Constrained Temporal Hierarchical Architecture** (Jardine et al.) | arXiv:2601.10738 | Jan 2026 preprint | Temporal-hierarchy MAS suffer "inter-layer conflicts, **unbounded error propagation**"; CTHA projects inter-layer communication onto structured manifolds: typed message contracts, authority manifolds bounding each layer's decision space, arbiter resolution. **47% reduction in failure cascades**, 2.3× sample efficiency | Single architecture proposal, not a structure-sweep; no organizational boundary taxonomy; unverified claims (small paper, 75KB) |
| **Tiered Agentic Oversight (TAO)** (Kim et al., MIT) | arXiv:2506.12482 | 2025 preprint | Clinical-hierarchy-inspired tiered oversight; **hierarchy as error-correction: absorbs up to 24% of individual agent errors before compounding**; ablations: adaptive > static tiers; lower tiers indispensable; human physician as top tier improves triage 40%→60% | Healthcare-safety domain; oversight tiers only; no propagation model |
| **Emergence World** (Vempaty et al.) | arXiv:2609.17320 | 15 Sep 2026 preprint | 8 persistent worlds × 10 agents, 16 days, 850k LLM calls; 3 stress events via ordinary surfaces (indirect prompt injection, misinformation, private-memory exposure). **No world fully resilient; detection ≠ containment** — threats written into persistent memory and acted on **up to 46h later**; conformity despite private disagreement; coordinated refusal of assigned work | Open-ended world, not organizational workflow; no roles/authority structure varied; descriptive, no containment mechanism comparison |
| MAST — Why Do Multi-Agent LLM Systems Fail? (Cemri et al., Berkeley) | arXiv:2503.13657 | NeurIPS 2025 | 1,600+ annotated traces, 7 frameworks; 14 failure modes in 3 categories (system design, inter-agent misalignment, task verification); κ=0.88 | Taxonomy/diagnosis, not structure × resilience; no interventions |
| Who&When (Zhang et al.) | arXiv:2505.00212 | ICML 2025 (camera-ready) | Automated failure attribution: which agent + which step. 127 MAS failure logs; best method 53.5% agent accuracy, 14.2% step accuracy | Attribution only; no structure manipulation |
| ECHO — Where Did It All Go Wrong? (Banerjee et al.) | arXiv:2510.04886 | Oct 2025 preprint | Hierarchical context + consensus voting for error attribution | Attribution only |
| MAS-Shield (Wang et al.) | arXiv:2511.22924 | EMNLP Findings 2026 | Defense vs linguistic attacks causing **cascading failures**; critical-agent selection (high-influence nodes) + tiered auditing; 92.5% recovery rate, −70% latency | Adversarial prompts, not endogenous faults; structure fixed |
| Prompt Infection (Lee et al.) | arXiv:2410.07283 | 2024 preprint | Self-replicating LLM-to-LLM prompt injection propagating across agents; LLM Tagging defense | Attack vector; propagation yes, org structure no |
| Breaking Agents (Zhang et al.) | arXiv:2407.20859 | 2024 preprint | Malfunction amplification attacks; >80% failure rates; multi-agent scenarios | Attack-focused |
| Diagnose, Localize, Align (Wan et al.) | arXiv:2509.23188 | 2025 preprint | **Hierarchical compliance under instruction conflicts** (system–user, peer–peer) as systemic MAS failure mode; CRAS metric; SAIL surgical alignment | Model-level fix, not org-level containment |
| Evil Geniuses (Tian et al.) | arXiv:2311.11855 | 2023 preprint | Safety/robustness of LLM-based agents under adversarial scenarios | Single-agent focus mostly |

---

## 4. Classical MAS organization models and their LLM-era revival

### 4.1 Verified classical anchors

| Work | Reference (verified) | Core content |
|---|---|---|
| **AGR meta-model** | Ferber & Gutknecht, "A meta-model for the analysis and design of organizations in multi-agent systems," ICMAS 1998, DOI 10.1109/icmas.1998.699041 (894 citations per Semantic Scholar) | Agent–Group–Role: agents play roles within groups; minimal org meta-model |
| AGR application | Ferber, Gutknecht, Michel, "From Agents to Organizations: An Organizational View of Multi-Agent Systems," AOSE 2003, LNCS, DOI 10.1007/978-3-540-24620-6_15 (HAL lirmm-00269681) | AGR as organizational view of MAS |
| **MOISE** | Hübner, Sichman, Boissier, "A Model for the Structural, Functional, and Deontic Specification of Organizations in Multiagent Systems," SBIA 2002, DOI 10.1007/3-540-36127-8_12 (HAL emse-00745177) | Structural (roles/links/groups), functional (goals/plans/missions), deontic (permissions/obligations) specification |
| **MOISE+** | Hübner, Sichman, Andreoli, Boissier, AAMAS 2002, DOI 10.1145/544741.544858 (HAL emse-00758315) | Refined MOISE; org reorganization line followed |
| **OperA/OMNI** | Dignum, Vázquez-Salceda, Dignum, "OMNI: Introducing Social Structure, Norms and Ontologies into Agent Organizations," PROMAS 2004, LNCS, DOI 10.1007/978-3-540-32260-3_10; Dignum et al., AAMAS 2004 "A Model of Almost Everything: Norms, Structure and Ontologies in Agent Organizations." (Canonical OperA reference is V. Dignum's 2004 Utrecht PhD thesis — thesis itself not re-verified, but the publication line is) | Organizational interaction model: social structure, norms, ontologies; org as first-class design object |
| **Horling & Lesser survey** | "A survey of multi-agent organizational paradigms," Knowledge Engineering Review 19(4), 2004, DOI 10.1017/S0269888905000317 (752 citations; abstract verified at Cambridge Core) | Hierarchies, holarchies, coalitions, teams, congregations, societies, federations, markets, matrix; "organizational design can have a significant, quantitative effect on performance" |
| **Carley & Lin** | "A Theoretical Study of Organizational Performance Under Information Distortion," Management Science 43(7), 1997, DOI 10.1287/mnsc.43.7.976 | Computational org theory: org structure × performance under distorted information — the classical ancestor of "structure vs error resilience" |
| Lin & Carley | "Maydays and Murphies: A Study of the Effect of Organizational Design, Task, and Stress on Organizational Performance," 1992, DOI 10.21236/ada261901; book "Designing Stress Resistant Organizations" (2003, Springer, DOI 10.1007/978-1-4757-3703-5) | Org design explicitly for **stress resistance** — closest classical framing to the seed |
| So & Durfee | "Designing tree-structured organizations for computational agents," Computational & Mathematical Organization Theory 2(3), 1996, DOI 10.1007/bf00127275 | Analytical design of hierarchical agent orgs |
| Dignum, Dignum, Sonenberg | "Exploring Congruence Between Organizational Structure and Task Performance: A Simulation Approach," COIN 2005/2006, DOI 10.1007/11775331_15 | Simulation of org structure × task performance congruence |
| Kota, Gibbins, Jennings | "Self-organising agent organisations," AAMAS 2009; "Decentralised Structural Adaptation in Agent Organisations," LNCS DOI 10.1007/978-3-642-02377-4_4; ACM TAAS 2012, DOI 10.1145/2168260.2168261 | Decentralized **structural adaptation/reorganization** of agent orgs under changing conditions |

### 4.2 Does LLM-era work cite/revive them? — Mostly NO, with thin exceptions

**Negative evidence (strong):**
- Guo et al., "Large Language Model based Multi-Agents: A Survey of Progress and Challenges" (arXiv:2402.01680, IJCAI 2024): full-text grep of the HTML — **zero** mentions of MOISE, AGR/agent-group-role, OperA, Dignum, Ferber, Hübner, Sichman, Boissier, Horling, Carley, Mintzberg, Belbin, "organization theory", "organizational paradigm", "span of control".
- Tran et al., "Multi-Agent Collaboration Mechanisms: A Survey of LLMs" (arXiv:2501.06322, 2025): same grep — **zero** classical-org mentions; "division of labor" appears 3× but only as informal role-specialization language.
- IMACS (the anchor): uses Belbin/Mintzberg/RACI (management science) — **no MOISE/AGR/OperA**.
- Scaling Agent Systems (arXiv:2512.08296): zero classical-org citations (grep of full HTML).
- Resilience paper (arXiv:2408.00989): zero classical-org citations.

**Positive evidence (thin, recent):**
- **MetaGPT** (arXiv:2308.00352) cites AGR (Ferber & Gutknecht 1998) — the only LLM-era citer of AGR found in the first 100 Semantic Scholar citations.
- **Loop-Back Authority** (arXiv:2609.14767, Sep 2026) cites **MOISE+ and Horling & Lesser**.
- **Organizational Control Layer** (arXiv:2606.04306, 2026) cites Horling & Lesser.
- **Institutional AI** (arXiv:2601.10599, 2026) cites MOISE+.
- "An organizational theory for multi-agent interactions integrating human agents, LLMs, and specialized AI" (2025; Semantic Scholar-indexed, venue/ID not verified — SS rate limits) cites Horling & Lesser.
- "Cognitive Agents Powered by Large Language Models for Agile Software Project Management" (2024; SS-indexed, not further verified) cites Horling & Lesser.
- Also citing MOISE+ (2026, SS-indexed, not further verified): "An Agent Execution Control Layer for Organizational Multi-Agent Systems"; "From Co-Pilots to Co-Workers: A Formal Typology of Human–Agent Collaboration in Organizations"; "Dynamic roles in AgentSpeak".

**Verdict:** The LLM era is re-inventing organizational MAS mostly **without** the classical computational-org literature; where it engages "org theory" it prefers management-science constructs (Belbin, Mintzberg, RACI, holacracy, historical political institutions) over MOISE/AGR/OperA. A small 2025–2026 revival cluster exists. This is a genuine **opportunity gap**: formal org specification (structural/functional/deontic) as the substrate for blast-radius analysis is unclaimed.

### 4.3 Span of control and organizational routines

- **Span of control:** searches ("span of control" + agent/LLM) return only a 2017 non-LLM paper (arXiv:1702.04449). **No LLM-MAS work studies span of control** (how many subordinates per supervisor before coordination degrades). SoA's constant-per-agent-load design and AgentsNet's scaling degradation are adjacent but never framed this way. **Open gap.**
- **Organizational routines:** no LLM-MAS work found using the routines construct (Nelson & Winter lineage). The closest instantiated analogue is **SOPs** in MetaGPT/ChatDev — static procedural scripts — and MegaAgent explicitly removes them. Whether routines/SOPs act as **fault containment** (standardized handoffs limiting error spread) or as **propagation channels** is unstudied. **Open gap.**

---

## 5. Is organizational-structure-vs-failure-resilience studied?

**Yes, but narrowly and recently — three papers form the existing core:**

1. **Zhou et al. (arXiv:2408.00989)** — structure (linear/flat/hierarchical) × injected faulty agents × defenses (Challenger/Inspector). Hierarchical most resilient (5.5% vs 10.5%/23.7% drops). Limitations: 3-agent patterns, response-level faults only, structure–prompt entanglement, no organizational boundaries, no recovery-over-time, no blast-radius metric.
2. **Kim et al. (arXiv:2512.08296)** — 5 architectures × error amplification (Independent 17.2× → Centralized 4.4×). Limitations: error amplification **not significant after controls** (p=0.658); trace-level token-based proxy; no injected faults; no recovery mechanisms.
3. **CTHA (arXiv:2601.10738)** — hierarchical constraints cut failure cascades 47%. Single-architecture proposal, not a sweep.

Adjacent: TAO (oversight tiers absorb 24% of errors), MAS-Shield (cascade defense vs attacks), Emergence World (propagation through memory/tools/agents in persistent worlds; detection ≠ containment), OCL (execution-boundary containment).

**What none of them does (the seed's defensible core):**
- No **organizational blast-radius construct**: spread quantified across role / communication / authority-delegation / tool / memory / accountability / human-agent boundaries.
- No **fault taxonomy mapped to org boundaries** (existing fault injection = wrong answers or adversarial prompts).
- No **recovery** as studied mechanism (checkpoint/rollback, reorganization, delegation re-routing, quarantine) — classical MAS had reorganization (Kota et al.), LLM era does not.
- No **containment mechanism comparison under controlled structure variation** at workflow scale (existing: 3-agent patterns or fixed architectures).
- No use of **formal org specification** (MOISE-like structural/deontic constraints) as the independent variable.

---

## 6. Does anything here kill or subsume the seed hypothesis?

**No kill. Partial occupancy at the core question, with substantial defensible space:**

- The *generic* question "does structure affect error spread in LLM MAS?" is **answered affirmatively** by arXiv:2408.00989 and arXiv:2512.08296 — a MASO submission must cite and differentiate from both, plus CTHA. Claiming "first to study structure × failure" would be fatal.
- The *specific* hypothesis — organizational blast radius across seven boundary types, determinants thereof, and containment/recovery mechanisms preserving utility — is **not subsumed**: no paper operationalizes blast radius, crosses authority/tool/memory/accountability/human boundaries, studies recovery, or uses formal org models.
- **Risk note 1:** Emergence World (Sep 2026) is converging on propagation-through-memory/tools in persistent agent societies; if extended with org structure it would subsume more of the seed.
- **Risk note 2:** The delegation-invariants territory (policy-preserving delegation, A2A/MCP accountability chains) is occupied by the existing MASO proposal (maso/policy_preserving_delegation_research_proposal.md) and by OCL (arXiv:2606.04306) at the execution boundary — the seed should avoid re-treading authority-boundary enforcement alone.
- **Risk note 3:** "Toward an Organizational Science" (IMACS) already claims the *framing* of organizational science for LLM MAS; the seed should position as "organizational **resilience** science" — the failure/recovery half IMACS explicitly leaves out (its scope note excludes failures from changing external state).

---

## 7. Unverified / could-not-verify items (honesty log)

- "Which LLM Multi-Agent Protocol to Choose?" (Du et al., ICML 2026, cited by IMACS) — not found on arXiv/DataCite; existence attested only via IMACS reference list.
- "An organizational theory for multi-agent interactions integrating human agents, LLMs, and specialized AI" (2025) — Semantic Scholar-indexed (cites Horling & Lesser); abstract/venue not retrievable due to SS 429s.
- "An Agent Execution Control Layer for Organizational Multi-Agent Systems" (2026); "From Co-Pilots to Co-Workers" (2026); "Dynamic roles in AgentSpeak" (2026) — SS-indexed MOISE+ citers; not further verified.
- Dignum's OperA PhD thesis (Utrecht, 2004) — canonical reference not directly re-verified; the OperA-line publications (OMNI 2004, AAMAS 2004) were verified via Crossref.
- "The 45% Rule" and "When Adding One Agent Breaks Everything" (Zenodo 2026) — checked and **excluded**: AI-generated podcast episodes (creators listed as "Gemini 3.1 (Flash)", "Chatterbox TTS"), not research papers.
- Semantic Scholar citation sampling was limited to the first 100 citations per classical paper (rate limits); LLM-era citer counts are lower bounds.
