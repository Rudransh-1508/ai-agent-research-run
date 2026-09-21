# A3 — Adjacent Venues and Crowding: Where MASO's Themes Are Being Worked On (2025–2026)

**Investigator:** VENUE INTEL A3
**Date:** 21 September 2026
**Mission:** Map where MASO 2026's themes are published across adjacent venues in 2025–2026; identify which themes are crowded elsewhere and which are orphaned (making MASO their natural home). Adversarial focus: test the seed hypothesis "organizational failure propagation and recovery in LLM multi-agent systems" (organizational blast radius; containment/recovery mechanisms preserving task utility).

**Target workshop:** MASO 2026, 1st International Workshop on Multi-Agent and Agentic Systems (in Organizations), colocated with PRIMA 2026, Kumamoto, Japan, 14 Dec 2026. Deadline 10 Oct 2026. CFP verified at [maso.uno](https://www.maso.uno/call-for-papers.php?lang=en).

---

## 1. Bottom line

**The seed hypothesis is NOT killed by any adjacent venue, but two flanks are now crowded and one key term is occupied:**

1. **Technical failure propagation/cascade/attribution in LLM MAS is crowded** (2025–2026): a dedicated ICML 2026 workshop (FAGEN — "Failure Modes of Agentic AI"), multiple 2026 arXiv papers on cascade detection (CASPIAN), cascade defense (MAS-Shield), pre-hoc failure risk (HalluProp), failure attribution (Who&When @ ICML 2025 spotlight; StepFinder), propagation-aware UQ (PropUQ-MAS), and error-propagation models (Hallucination Snowball, Hallucination Cascade). A purely technical "errors spread through agent networks" paper would be scooped.
2. **The term "blast radius" is occupied** by DamageFlow/BlastGuard (ICML 2026 AIWILD workshop): "Measuring and Minimizing Blast Radius in Agentic Tool Use" — but with a *security/tool-effect* semantics (unauthorized tool effects under prompt injection/MCP poisoning), not an *organizational* semantics (spread across role, authority, delegation, accountability, human-agent boundaries). The seed must cite and differentiate, or rename.
3. **The organizational angle is genuinely orphaned.** No adjacent venue publishes on failure propagation *as modulated by organizational structure* (roles, authority/delegation chains, accountability allocation, human-agent decision rights) or on containment/recovery as *organizational* controls (escalation, role reassignment, authority revocation, redundancy) with utility preservation. AAMAS/COINE owns classical organizations-and-norms (not LLM failure cascades); CHI/CSCW own human-AI interaction design (not systemic failure engineering); security venues own attack/defense mechanisms (not organizational recovery); ML venues own benchmarks and diagnostics (not organizational context); SE venues own coding agents (not orgs).

**MASO is the natural home for the seed precisely because the organizational layer is the intersection that every adjacent venue's remit excludes.**

---

## 2. MASO 2026 themes (verified from CFP)

| ID | MASO theme |
|---|---|
| T1 | Agent architectures and orchestration (incl. delegation, lifecycle) |
| T2 | Interoperability and enterprise integration (A2A, protocols, authN/authZ, identity) |
| T3 | Multi-agent coordination and distributed decision-making |
| T4 | Human–agent collaboration in organizational settings (decision rights, delegation) |
| T5 | Organizational learning, agent adaptation, memory, knowledge management |
| T6 | Governance, accountability, compliance (responsibility, authority, liability) |
| T7 | Trust, safety, security, privacy, reliability — **explicitly including "detection and mitigation of cascading, and systemic failures"** |
| T8 | Evaluation, benchmarking, organizational testbeds |
| T9 | Organizational design and socio-technical transformation |
| T10 | Applications and deployment in organizations |

The seed hypothesis sits at T7 × T6 × T4 × T8, with T9 framing.

---

## 3. Venue-by-venue findings

### 3.1 AAMAS 2026 (Paphos, Cyprus, 25–29 May 2026 — already held) and PRIMA 2026

Verified via [cyprusconferences.org/aamas2026](https://cyprusconferences.org/aamas2026/) (workshops page and accepted research track, fetched 21 Sep 2026). AAMAS 2025 (Detroit) site blocks automated access; continuity of the classical workshop series is confirmed by edition numbering on the verified 2026 page (COINE "held six times 2020–2025", EMAS 14th ed., EXTRAAMAS 8th ed., MABS 27th ed., ATT 14th ed., GAIW 8th ed.).

**AAMAS 2026 workshops (verified, 18 total):** AI4CNI (AI for critical national infrastructure — *cascading failures* but cyber-physical, not LLM agents), ALA (adaptive/learning agents), ARMS (robots), ASI (societal impact), ATT (traffic), C-MAS (citizen-centric), CLaRAMAS (causal learning/reasoning in agents), **COINE (Coordination, Organizations, Institutions, Norms and Ethics for Governance of MAS — the classical organizational-governance home)**, EMAS (engineering MAS; 2026 focus: hybrid agent architectures incl. LLM agentic systems, interoperability, coordination, governance), EXTRAAMAS (explainable/trustworthy/responsible AI & MAS), GAIW (games/incentives), MABS (agent-based simulation), MASSpace, NEXUS (neurosymbolic trustworthy), OptLearnMAS, RaD-AI (rebellion/disobedience), SE (strategic engineering).

**AAMAS 2026 main research track — verified LLM/agentic titles (grep of accepted-papers page):**

| Verified title | Relevance |
|---|---|
| The Triad of Identity, Trust and Responsibility in Multi-Agent Systems | T6 — responsibility, classical-formal |
| On Quantitative Analysis of Responsibility in Multiagent Systems | T6 — responsibility quantification |
| Reasoning About Responsibility for Taking Risks | T6 |
| Disobedience in normative multi-agent systems | T6/T9 — norms |
| Engineering norm-aware BDI agents; Leveraging Context-Oriented Programming to Implement Normative Rules | T6 — norms |
| Reputation as a Solution to Cooperation Collapse in LLM-based MASs | T3/T7 — LLM MAS cooperation failure |
| The Role of Social Learning and Collective Norm Formation in Fostering Cooperation in LLM Multi-Agent Systems | T3/T6 |
| Interpretable Failure Analysis in Multi-Agent Reinforcement Learning Systems | T7 — failure analysis but MARL, not LLM orgs |
| When LLM Agent Teams Fail at Topological Spatial Reasoning Under Partial Observability | T7 — team failure, narrow domain |
| Towards Failure-Resilient Lifelong Learning Agents (scene-graph proactive replanning) | T7 — single-agent resilience |
| IntentGuard: Securing MCP-Enabled LLM Agents via Post-Decision Semantic Plan Verification | T2/T7 — MCP security |
| Information Fidelity in Tool-Using LLM Agents: A Martingale Analysis of the Model Context Protocol | T2/T7 — MCP reliability |
| LEGOMem: Modular Procedural Memory for Multi-agent LLM Systems for Workflow Automation | T5 — memory for workflows |
| Developing Guidelines for Human-LLM Agent Teams: A Multi-Stakeholder Lens | T4 |
| Beyond Vibe Decision Theory: Asymmetric Manipulation Vulnerabilities in LLM Multi-Agent Coordination | T7 — manipulation |
| Everyone Contributes! Incentivizing Strategic Cooperation in Multi-LLM Systems | T3 |
| Symbolic Guidance for LLM Agents in Distributed Multiagent Coordination | T3 |
| Grassroots Federation: Fair Democratic Governance at Scale | T6/T9 |

**Assessment:** AAMAS is absorbing LLM-MAS fast (≈30+ LLM-agent papers in the 2026 main track) and owns the classical organizations/institutions/norms/governance conversation via COINE. But COINE is pre-LLM in method (normative systems, institutions), and the main-track LLM failure papers are about cooperation collapse, spatial reasoning, or MARL — **no organizational failure-propagation/recovery work**. PRIMA 2026 (verified at [prima2026.org](https://www.prima2026.org/): "Beyond Traditional MAS", fusing MAS with Generative/Agentic AI; areas include "Ethics, Society, and Governance", "Human-Agent Interaction") is MASO's host and signals the MAS community's pivot, but PRIMA's main track is general MAS, not organizational deployment.

### 3.2 NeurIPS 2025 (San Diego, Dec 2025)

Verified via OpenReview API (`NeurIPS.cc/2025/Workshop/*` groups, ~63 top-level workshop groups resolved by title). Agent-relevant workshops:

| Workshop | Full title (verified) | MASO themes |
|---|---|---|
| SEA | Workshop on Scaling Environments for Agents | T8 (environments) |
| LAW | Bridging Language, Agent, and World Models for Reasoning and Planning | T1 |
| MTI-LLM | First Workshop on Multi-Turn Interactions in Large Language Models | T1 |
| FMEA | Challenge on Foundation Models for Embodied Agents | T8 |
| EWM | Embodied World Models for Decision Making | T1 |
| Lock-LLM | Prevent Unauthorized Knowledge Use from Large Language Models | T7 (security) |
| Reliable_ML | Reliable ML from Unreliable Data | T7 (generic) |
| RegML | Regulatable ML | T6 (generic) |

**No multi-agent-systems workshop, no organizational workshop, no failure-propagation workshop at NeurIPS 2025.** Agent work is reasoning/planning/embodiment-centric. (A handful of group IDs — NORA, ResponsibleFM, E-SARS, CLRLC-LLMs, 7HVU, PersonaNLP — returned 404 on direct fetch; they are stale/renamed entries, and none matches an organizational-failure theme by acronym.)

### 3.3 ICML 2025 (Vancouver) and ICML 2026 (Seoul, Jul 2026)

Verified via OpenReview API group titles.

**ICML 2025:** **MAS — "Multi-Agent Systems in the Era of Foundation Models: Opportunities, Challenges and Futures"** (direct ML-venue home for LLM MAS); CFAgentic — "Collaborative and Federated Agentic Workflows"; WCUA — "Computer Use Agents"; TAIG — "Technical AI Governance". Main conference: **Who&When failure-attribution paper was an ICML 2025 spotlight** (verified via OpenReview venue field).

**ICML 2026:** **FAGEN — "Workshop on Failure Modes of Agentic AI"** (10 Jul 2026, COEX Seoul; verified at [fagen-workshop.github.io](https://fagen-workshop.github.io/): scope = "Reproducible Triggers, Trace Diagnostics, and Verified Fixes" — failure definitions, minimal reproducible triggers, trace-level diagnostics, cost-aware fixes); **AIWILD 2nd ed. — "Agents in the Wild: Safety, Security, and Beyond"**; **AgenticUQ — "Statistical Frameworks for Uncertainty in Agentic Systems"**; TAIGR (Technical AI Governance Research); LM4Plan.

**FAGEN@ICML 2026 accepted posters (verified via OpenReview search, ~60+ papers)** include: "Rethinking Failure Attribution in Multi-Agent Systems: A Multi-Perspective Benchmark"; "When Teamwork Fails: A Structural Autopsy of Multi-Agent Failures in Multimodal Clinical Risk Prediction"; "Introspecter: Diagnosing Multi-Agent LLM Debate Failures"; "Talk is Cheap, Communication is Hard: Dynamic Grounding Failures and Repair in Multi-Agent Negotiation"; "Instruction Bleed: Cross-Module Interference in Prompt-Composed Agentic Systems"; "Locally Coherent, Globally Incoherent: A Post-Aggregation Failure Mode in Multi-Component LLM Agents"; "Dark Triad and Seven Deadly Sins: Dark Companions as Reproducible Failure Modes in Multi-Agent LLM **Workplaces**" (verified abstract: LLM agents reproduce workplace coercion/credit-appropriation patterns under social pressure — organizational-behavior failure modes, but not propagation/containment); "EGI-BENCH: An Enterprise General Intelligence Benchmark Suite"; "MANTRA: SMT-Validated Compliance Benchmarks for Tool-Using LLM Agents"; "MemShield: Defense Against Coordinated Memory Poisoning in LLM Agents".

**Assessment:** As of mid-2026, ICML has a *dedicated, large* agentic-failure-modes workshop. This crowds the "failure taxonomy/diagnosis/benchmark" flank hard. FAGEN's framing is ML-reliability (traces, triggers, fixes), explicitly not organizational science.

### 3.4 ICLR 2025 (Singapore) and ICLR 2026 (Rio, Apr 2026)

Verified via OpenReview API group titles.

**ICLR 2025:** AgenticAI ("Towards Agentic AI for Science"), FM-Wild (Foundation Models in the Wild), HAIC (Human-AI Coevolution), BuildingTrust, VerifAI.

**ICLR 2026:** **MALGAI — "Multi-Agent Learning and Its Opportunities in the Era of Generative AI"**; **MemAgent — "Memory for LLM-Based Agentic Systems"** (T5!); LLA — "Lifelong Agents"; **Reliable_Autonomy — "Agentic AI in the Wild: From Hallucinations to Reliable Autonomy"**; **AIWILD 1st ed. — "Agents in the Wild: Safety, Security, and Beyond"**; VerifAI-2; AIMS — "AI for Mechanism Design and Strategic Decision Making"; AFA — "Advances in Financial AI: Towards Agentic and Responsible Systems"; AFAA — fairness in agentic systems.

**Assessment:** ICLR covers multi-agent *learning*, agent *memory*, agent *reliability/safety/security* — all as ML problems. No organizational constructs.

### 3.5 AAAI 2026 (Singapore, 20–27 Jan 2026)

Verified via [aaai.org AAAI-26 Workshop Program](https://aaai.org/conference/aaai/aaai-26/workshops-program/) (52 workshops). Agent-heavy slate:

| # | Workshop (verified) | MASO themes |
|---|---|---|
| W2 | Agentic AI in Financial Services | T10 |
| W8 | **Agentic AI Benchmarks and Applications for Enterprise Tasks** | T8/T10 — enterprise! |
| W36 | **LaMAS 2026: LLM-based Multi-Agent Systems — Towards Responsible, Reliable, and Scalable Agentic Systems** | T1/T6/T7 |
| W42 | Next-Gen Code Development with Collaborative AI Agents | T10 (SE) |
| W43 | **Orchestrating Synthesized Human and AI-Agentic Workflows: AI Agency Benefits, Disruptions and Management** | T4/T9 — closest to organizational |
| W45 | FAST — Foundations of Agentic Systems Theory | T1 |
| W51 | How Can We Trust and Control Agentic AI? Alignment, Robustness, Verifiability in Autonomous LLM Agents | T7 |
| W26 | AI Governance Workshop: Alignment, Morality, Law, and Design | T6 |

LaMAS 2026 scope verified at [sites.google.com/view/lamas2026](https://sites.google.com/view/lamas2026): "organization of multiple LLM agents… coordination strategies, communication protocols", "safety, trust, responsibility… human-in-the-loop oversight, regulatory frameworks", explicitly aims to "bridge the gap in understanding **failure modes**, alignment challenges, and responsible behavior". Here "organization" means agent organization, not human organizations. Non-archival.

**Assessment:** AAAI-26 is the most agentic-workshop-crowded AI venue (8/52 workshops on agentic AI). LaMAS is the closest neighbor to MASO in 2026 — but its center of gravity is agent-systems ML (reliability, alignment, scale), with governance as a topic rather than the organizational setting as the object of study.

### 3.6 NLP venues: ACL 2025 (Vienna), EMNLP 2025 (Suzhou), NAACL 2025 (Albuquerque)

Verified via official workshop pages.

- **ACL 2025:** REALM — "First Workshop for Research on Agent Language Models"; LLMSEC — "First Workshop on LLM Security". Agent work = language agents, tool use, security.
- **EMNLP 2025:** no agent-dedicated workshop (19 workshops listed; closest: HCI+NLP, UncertaiNLP, PALS personalization).
- **NAACL 2025:** no agent-dedicated workshop (24 workshops; closest: TrustNLP).

**Assessment:** NLP venues treat agents as language/task solvers. Zero organizational-failure coverage.

### 3.7 HCI venues: CHI 2026 (Barcelona, 13–17 Apr 2026), CSCW 2025 (Bergen, Oct 2025)

Verified via [chi2026.acm.org/workshops/accepted](https://chi2026.acm.org/workshops/accepted/) (69 workshops) and [cscw.acm.org/2025 workshops](https://cscw.acm.org/2025/index.php/workshops/) (12 workshops).

**CHI 2026 agent-relevant workshops:** W2 "Agentic Automation Experiences — Rethinking the Interaction of Humans and AI Agents"; W4 "AI CHAOS! 2nd Workshop on the Challenges for Human Oversight of AI Systems"; W30 "From Human-Human Collaboration to Human-Agent Collaboration… Partnerships Between Humans and LLM Agents"; W39 "Human-Centered Explainable AI… in the Era of Agentic AI"; W45 "PoliSim: LLM Agent Simulation for Policy"; W59 "Human-Centered Evaluation and Auditing of Language Models: AI Agents-in-the-Loop".

**CSCW 2025:** closest is "Augmenting Collaborative Problem-Solving: GenAI for Groupwork"; rest are data-ethics/futures-of-work/critical-studies.

**Assessment:** CHI owns the human-agent interaction/oversight/trust-calibration conversation (T4) from a design and empirical-HCI lens. It does not do systemic failure propagation, containment mechanisms, or organizational testbeds with fault injection. CSCW is even further (societal/qualitative).

### 3.8 Software-engineering venues: FSE 2025 (Trondheim), ICSE 2026 (Rio, Apr 2026)

Verified via conf.researchr.org pages.

- **FSE 2025 workshops:** AI IDE, AI-SDLC, BI4LLMC, HumanAISE, LLanMER, LLMapp, ResponsibleSE, CauSE — LLM/agentic SE process, requirements, human factors.
- **ICSE 2026:** dedicated "Agentic Engineering" and "Bots and Agents in Software Engineering" tracks/sessions; SE.next plenary panels "In the Agentic Trenches", "Research in the Agentic Era", "Raising the Agentic Engineer".

**Assessment:** SE venues are saturated with coding-agent and agentic-SDLC work. Failure work there = build/test/repair failures of coding agents, not organizational blast radius. No competition for the seed; also no home for it (wrong community).

### 3.9 Security venues: USENIX Security 2025 (Seattle, Aug 2025), CCS 2025 (Taipei, Oct 2025)

Verified via [USENIX Security '25 technical sessions](https://www.usenix.org/conference/usenixsecurity25/technical-sessions) (full program grep). Agent/LLM-security papers include:

| Verified paper | Content |
|---|---|
| StruQ: Defending Against Prompt Injection with Structured Queries | prompt-injection defense |
| Make Agent Defeat Agent: Automatic Detection of Taint-Style Vulnerabilities in LLM-based Agents | agent vuln detection |
| PATCHAGENT: A Practical Program Repair Agent Mimicking Human Expertise | repair agent |
| When LLMs Go Online: The Emerging Threat of Web-Enabled LLMs | web-agent threats |
| PoisonedRAG; Machine Against the RAG; Topic-FlipRAG | RAG poisoning/manipulation |
| Malicious LLM-Based Conversational AI Makes Users Reveal Personal Information | privacy |

CCS 2025's program page could not be enumerated (sigsac.org program URLs 404; Internet Archive CDX offline during investigation). The USENIX Sec '25 pattern plus the arXiv security wave (CASPIAN, MAS-Shield, OpenClaw security analysis — arXiv:2605.25435) is sufficient to characterize the venue class: **security venues own agent authorization, prompt injection, tool/MCP poisoning, and cascade *attacks* — attack/defense mechanisms, not organizational recovery or utility-preserving containment.**

---

## 4. Theme-by-venue crowding matrix

Crowding legend: ●●● heavy / ●● moderate / ● light / — absent (all rows verified as above)

| MASO theme | AAMAS | NeurIPS/ICML/ICLR ws | AAAI-26 ws | ACL/EMNLP | CHI/CSCW | FSE/ICSE | USENIX/CCS |
|---|---|---|---|---|---|---|---|
| T1 Architectures/orchestration | ●● (EMAS, main track) | ●●● (MAS, MALGAI, LAW, SEA) | ●●● (LaMAS, FAST) | ●● (REALM) | ● | ●● | ● |
| T2 Interop/enterprise integration (A2A/MCP/auth) | ●● (IntentGuard, MCP papers) | ● | ●● (W8 enterprise) | ● | — | ● | ●●● (authz, injection) |
| T3 Coordination/decision-making | ●●● (core AAMAS) | ●● (MALGAI, NExT-Game) | ●● | ● | — | — | — |
| T4 Human-agent collaboration in orgs | ●● (Human-LLM teams paper) | ● (HAIC, HCAIR) | ●● (W43) | ● (HCI+NLP) | ●●● (W2/W4/W30/W59) | ●● (HumanAISE) | — |
| T5 Org learning/memory | ●● (LEGOMem) | ●● (MemAgent, MemFM) | ● | ● | ● | ● | ● (memory poisoning) |
| T6 Governance/accountability/compliance | ●●● (COINE, responsibility papers) | ●● (TAIG/TAIGR, RegML, AIMS) | ●● (W26, LaMAS) | — | ●● (policy/governance ws) | ● (ResponsibleSE) | ● |
| T7 Trust/safety/security/reliability incl. cascading failure | ●● (EXTRAAMAS, cooperation-collapse) | ●●● (FAGEN, AIWILD, Reliable_Autonomy, AgenticUQ) | ●●● (LaMAS, W51, AIR-FM) | ●● (LLMSEC) | ●● (AI CHAOS oversight) | ● | ●●● (injection, cascade attacks) |
| T8 Evaluation/benchmarks/testbeds | ●● | ●●● (SEA, AgenticUQ, EGI-BENCH…) | ●●● (W8) | ●● | ●● (W59) | ●●● (SWE-bench lineage) | ●●● (AgentDojo lineage) |
| T9 Organizational design/socio-technical | ● (COINE adjacent) | — | ●● (W43) | — | ●● (CSCW futures of work) | — | — |
| T10 Applications/deployment in orgs | ●● (ASI, C-MAS) | ● (UrbanAI, finance) | ●●● (W2, W8) | ● | ●● | ●● | ● |
| **Organizational failure propagation + containment/recovery (seed)** | — | ● (FAGEN: diagnosis only; DamageFlow: security semantics) | ● (LaMAS: failure modes as topic) | — | — | — | ●● (cascade *attacks*) |

---

## 5. Verified papers most threatening to the seed hypothesis

All verified by fetching the actual arXiv abstract page or OpenReview record on 21 Sep 2026.

| # | Paper | ID / venue | What it does | Why it doesn't subsume the seed |
|---|---|---|---|---|
| 1 | **What Can One Bad Tool Call Destroy? Measuring and Minimizing Blast Radius in Agentic Tool Use** (DamageFlow benchmark + BlastGuard runtime; M.A. Yagiz) | OpenReview MYvsxnxbCf, **ICML 2026 AIWILD** | Defines Blast Radius Score (resource sensitivity × action impact × propagation × recovery cost) under indirect prompt injection, MCP poisoning, tool shadowing, multi-agent relay attacks; containment via least-privilege capability graphs, dry-run, scoped tokens, rollback; 80-scenario pilot; 87.5% benign utility retained | **Occupies the "blast radius" term.** But semantics = security damage of tool effects for a single trust principal; no organizational constructs (roles, authority, delegation chains, accountability, human decision rights); pilot-scale; no org-structure modulation of spread |
| 2 | **CASPIAN: Online Detection and Attribution of Cascade Attacks in LLM Multi-Agent Systems** (Venkatesh, Isbarov, Amin, Kantarcioglu, Cui) | arXiv:2605.19240 (May 2026) | Cross-channel causal monitoring (late-interaction conditional transfer entropy) to detect cascade *attacks*, attribute origin/bridge/amplifier agents | Adversarial cascades only; detection/attribution, not containment/recovery; no organizational layer |
| 3 | **MAS-Shield: A Defense Framework for Secure and Efficient LLM MAS** (Wang et al.) | arXiv:2511.22924 (Nov 2025; v2 Sep 2026) | Coarse-to-fine defense vs linguistic attacks triggering cascading failures; critical-agent selection, sentry models, committee escalation; 92.5% recovery rate, −70% latency | Attack-defense framing; "recovery" = attack recovery, not organizational recovery; no org boundaries |
| 4 | **Before Agents Speak: Pre-hoc Failure Risk Inference in Multi-Agent Systems** (HalluProp; Lin et al.) | arXiv:2607.26836 (Jul 2026) | Pre-interaction hallucination-propagation risk via role-task semantic misalignment + communication topology + Noisy-OR; AUROC 84.6% | Prediction only; hallucination-specific; roles as prompt constructs, not organizational roles |
| 5 | **StepFinder: Temporal Semantic Framework for Failure Attribution in MAS** (Zhu et al.) | arXiv:2606.03467 (Jun 2026) | Lightweight root-cause step attribution; evaluated on Who&When | Attribution ≠ propagation determinants ≠ containment |
| 6 | **Which Agent Causes Task Failures and When? (Who&When)** (Zhang et al.) | arXiv:2505.00212; **ICML 2025 spotlight** (verified via OpenReview) | Failure-attribution dataset (127 MAS logs) + methods; best 53.5% agent-ID accuracy | Founded the attribution subfield; doesn't ask what determines spread or how to contain |
| 7 | **Why Do Multi-Agent LLM Systems Fail? (MAST)** (Cemri et al., UC Berkeley et al.) | arXiv:2503.13657 (Mar 2025, v3 Oct 2025) | 14-mode failure taxonomy, 3 categories; 1600+ annotated traces, 7 frameworks; LLM-judge | Taxonomy/diagnosis; categories (system design, inter-agent misalignment, verification) are not organizational boundaries; no recovery mechanisms |
| 8 | **PropUQ-MAS: Propagation-Aware Uncertainty Quantification** | arXiv:2608.22130 (Aug 2026) | UQ with upstream-inheritance over communication graph | Quantification only |
| 9 | **The Hallucination Snowball** (error propagation as Markov state transitions) | arXiv:2608.14588 (Jun 2026) | 4-agent financial pipeline; per-boundary escape probabilities 24.6%/48.3%/89.3%; detection decays by stage | Sequential pipeline, hallucinations only; no org structure, no containment design |
| 10 | **Hallucination Cascade** | arXiv:2606.07937 (Jun 2026) | Claim-level propagation across 3-agent chains; net attenuation observed | Descriptive; no mechanisms |
| 11 | **Organizational Control Layer (OCL)** (Shi et al.) | arXiv:2606.04306 (Jun 2026) | Governance layer at execution boundary: intercepts actions, checks role/policy/economic constraints, approve/revise/block/escalate; unsafe executions 88%→0%, valid success 12%→96% on AgenticPay-derived negotiation env; ablations show **pre-execution enforcement + structured recovery** combo matters | Closest organizational-adjacent work — but single-agent execution boundary, not multi-agent org-wide propagation; no blast-radius characterization across org boundaries |
| 12 | **Organizational Memory for Agentic Business Process Execution** (Kirchdorfer, Rebmann, Kampik et al.) | arXiv:2607.03228 (Jul 2026) | Shared governed org-memory layer for agentic BPM; procurement PoC | Memory/knowledge (T5), not failure propagation |
| 13 | **Policy-Invisible Violations in LLM-Based Agents (PhantomPolicy/Sentinel)** (Wu, Gong) | arXiv:2604.12177 (Apr 2026) | Policy violations from hidden context; org knowledge-graph counterfactual enforcement | Overlaps the *occupied* delegation-invariants territory (existing MASO proposal) more than the seed |
| 14 | **Dark Companions: Dark Triad / Seven Deadly Sins failure modes in Multi-Agent LLM Workplaces** (J. Li) | FAGEN@ICML 2026 poster (verified abstract) | LLM agents reproduce workplace coercion, credit appropriation, free-riding under social pressure | Organizational-*behavior* failure modes; emergent misbehavior, not fault propagation/containment |
| 15 | **AgentDojo** (Debenedetti et al.) | arXiv:2406.13352; NeurIPS 2024 D&B | Prompt-injection attack/defense benchmark for tool-using agents | Security evaluation; pre-organizational |
| 16 | **τ²-bench** (Sierra et al.) | arXiv:2506.07982 (Jun 2025) | Dual-control conversational agent benchmark (Dec-POMDP telecom domain) | Agent-user coordination benchmark; no failure propagation |

Also noted (verified existence, lower threat): "Sabotage from Within: Analyzing the Vulnerability of LLM Multi-Agent Systems to Infiltration" (OpenReview); "Security of OpenClaw Agents" (arXiv:2605.25435); "A Self-Healing Framework for Reliable LLM-Based Autonomous Agents" (arXiv, May 2026, single-agent self-healing); "DIG to Heal" (arXiv:2603.00309, explainable dynamic decision paths).

---

## 6. Where MASO is the natural home (gap confirmation)

Themes where adjacent venues are **heavy** (MASO differentiates or avoids):
- Agent architectures/orchestration as ML (ICML MAS, ICLR MALGAI, AAAI LaMAS/FAST)
- Failure-mode taxonomies, trace diagnostics, attribution benchmarks (FAGEN, Who&When, MAST, StepFinder)
- Agent security: prompt injection, MCP/tool poisoning, cascade attacks, authorization (USENIX/CCS + AIWILD + CASPIAN/MAS-Shield)
- Coding agents / agentic SDLC (FSE/ICSE)
- Human-agent interaction design and oversight (CHI)
- Classical organizations/institutions/norms (AAMAS COINE)

Themes where adjacent venues are **absent** (MASO's uncontested ground — the seed's core):
1. **Failure propagation as a function of organizational structure** — how role hierarchies, authority/delegation depth, communication topology, and accountability allocation determine blast radius. Nobody measures this. (DamageFlow measures tool-effect damage; CASPIAN measures adversarial influence; neither varies org structure.)
2. **Containment and recovery as organizational controls** — escalation paths, role reassignment, authority revocation, redundancy/deputization, human takeover — evaluated on systemic impact *and* task utility. (OCL has "escalate" and "structured recovery" at a single execution boundary; nothing org-wide, nothing multi-agent.)
3. **Cross-boundary spread semantics** — propagation across role / communication / authority / tool / memory / accountability / human-agent boundaries as distinct channels with different dynamics. (Existing work treats one channel at a time: hallucination text, adversarial influence, tool effects.)
4. **Organizational testbeds with fault injection** — FAGEN wants "reproducible triggers" but in ML benchmarks; MASO's CFP explicitly asks for organizational testbeds. No org-fault-injection testbed exists in any adjacent venue.

**Positioning warning for the seed:** the paper must (a) cite DamageFlow and explicitly redefine "blast radius" organizationally (or coin a distinct term, e.g., "organizational blast radius"), (b) cite MAST/Who&When/FAGEN and position as *mechanisms and determinants*, not another taxonomy, (c) cite CASPIAN/MAS-Shield and distinguish non-adversarial faults + recovery from attack detection/defense, (d) stay clear of the delegation-invariants territory occupied by the sibling MASO proposal (PhantomPolicy/OCL are adjacent to *that* proposal too).

---

## 7. Explicit answer: does anything here kill or subsume the seed hypothesis?

**No kill. Partial flanking on three sides:**

- **Not killed:** No venue or paper studies what determines the *organizational* blast radius of a local fault in an LLM multi-agent workflow, nor org-level containment/recovery with utility preservation. The organizational angle is systematically excluded by every adjacent venue's remit: ML venues strip org context; security venues assume adversaries not accidents; HCI venues study experience not systemic failure; SE venues study code not orgs; AAMAS/COINE's organizational theory predates and hasn't yet metabolized LLM-agent failure cascades.
- **Flank 1 (terminology):** "Blast radius" now has an established security semantics (DamageFlow, ICML 2026 AIWILD). Must differentiate.
- **Flank 2 (technical propagation):** Cascade detection/attribution/UQ/taxonomies are crowded (FAGEN workshop; ~8 arXiv papers 2025–2026). The seed must not read as "another failure taxonomy/diagnosis paper."
- **Flank 3 (governance infrastructure):** OCL and PhantomPolicy show organizational-policy enforcement at execution boundaries is emerging on arXiv (Apr–Jun 2026) — likely to appear at 2026–2027 venues. The seed's novelty window is open now but narrowing.

**Timeliness note:** MASO's deadline (10 Oct 2026) lands after ICML 2026 (Jul) and before NeurIPS 2026 (Dec; workshop slate not yet public as of 21 Sep 2026). FAGEN/LaMAS/AIWILD proceedings will be citable; a MASO submission is well-positioned to be the first *organizational* treatment rather than a late *technical* one.

---

## 8. Verification log and access notes

- Verified live on 21 Sep 2026: MASO CFP (maso.uno); AAMAS 2026 workshops + accepted research track (cyprusconferences.org/aamas2026); PRIMA 2026 (prima2026.org); AAAI-26 workshop program (aaai.org); ACL 2025 / EMNLP 2025 / NAACL 2025 workshop pages; CHI 2026 accepted workshops; CSCW 2025 workshops; FSE 2025 workshops; ICSE 2026 tracks; USENIX Security '25 technical sessions; LaMAS 2026 site; FAGEN site.
- OpenReview API v2 used to resolve workshop titles and papers: NeurIPS 2025 (~63 workshops), ICML 2025 (36), ICML 2026 (45), ICLR 2025 (38), ICLR 2026 (43); FAGEN and AIWILD@ICML2026 paper records; DamageFlow note MYvsxnxbCf; Who&When venue confirmation (ICML 2025 spotlight).
- arXiv abstract pages fetched directly for: 2503.13657, 2406.13352, 2505.00212, 2506.07982, 2605.19240, 2511.22924, 2607.26836, 2606.03467, 2608.22130, 2608.14588, 2606.07937, 2606.04306, 2607.03228, 2604.12177.
- Access failures (documented, not silently skipped): DBLP (Anubis anti-bot), Semantic Scholar API (persistent HTTP 429 on this IP), arXiv API/HTML search (intermittent 429 — searches succeeded for "cascading failures", "failure propagation", "error propagation", "organizational" queries with retries), aamas2025.org (403; continuity argued from edition numbering on verified 2026 pages), CCS 2025 program (sigsac.org program URLs 404; Internet Archive CDX offline), NeurIPS 2026 workshops (not yet announced), six stale NeurIPS 2025 OpenReview group IDs (404).
- ICML 2025 MAS workshop and FAGEN submission lists are not fully public (`public_submissions: False`); FAGEN poster titles were recovered via OpenReview full-text search on venue strings.
