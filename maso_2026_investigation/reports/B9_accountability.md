# LANDSCAPE B9 — Accountability, Governance, Responsibility

**Investigator:** B9 specialist (adversarial evidence-gathering)
**Date:** 21 September 2026
**Seed hypothesis under test:** *Organizational failure propagation and recovery in LLM multi-agent systems* — when a local fault occurs in an organizational multi-agent workflow, what determines its "organizational blast radius" (spread across role, communication, authority/delegation, tool, memory, accountability, and human-agent boundaries), and which containment/recovery mechanisms minimize systemic impact while preserving task utility.
**Assignment question:** Map responsibility attribution, accountability frameworks, governance of agentic systems, audit trails, liability, normative MAS governance (classical + LLM era). Does any governance work operationalize accountability DURING execution (runtime containment) vs post-hoc auditing?

**Verification method.** Every load-bearing paper below was verified by inspecting the actual record: arXiv abstract pages (fetched individually), the OpenReview API (`api2.openreview.net/notes/search`, which also indexes Crossref/DBLP records), the Crossref API (`api.crossref.org`), publisher pages via DOI, and the OWASP site. Semantic Scholar and the arXiv listing API were heavily rate-limited from this host and used only partially; DBLP was unreachable. Where a record could not be inspected (marked *unverified-abstract*), only bibliographic metadata from Crossref/OpenReview is asserted. Two curated corpora were used for discovery only, with each load-bearing entry independently re-verified: `masamasa59/ai-agent-papers` (operations/governance.md, operations/agentops.md) and a local `awesome-llm-agent-papers` copy found at `/tmp/AGENTS.md`.

---

## 1. Bottom-line judgment

**The seed hypothesis survives Landscape B9. Nothing found kills or subsumes it, but three works are close enough that the paper must differentiate explicitly:**

1. **DamageFlow / BlastGuard** (ICML 2026 AIWILD workshop, OpenReview `MYvsxnxbCf`) already uses "blast radius" terminology, measures propagation and recovery cost of *one bad tool call*, and proposes a runtime containment layer with utility preservation. Delta: adversarial-security threat model (prompt injection, tool poisoning, relay attacks), tool-effect damage rather than organizational propagation across role/authority/memory/accountability/human boundaries, single-author 80-scenario pilot, no responsibility attribution.
2. **Adaptive Accountability Framework (AAF)** (arXiv:2512.18561) is the *only* verified work that closes the full runtime accountability loop — provenance → change-point detection → causal responsibility attribution → cost-bounded intervention — during execution. Delta: RL/PPO agents in simulated networked MAS, target is emergent norm violations (collusion, hoarding), interventions are reward shaping / policy patching; no LLMs, no organizational workflows, no local-fault blast radius.
3. **Governance at the Boundary / Fiducia-bench** (arXiv:2608.16055) shows policy-relevant facts are attenuated at agent-decomposition handoff boundaries (0% → 56% → 85% attenuation across architectures) — direct evidence that handoffs degrade governance. Delta: measures compliance/escalation degradation, not fault propagation; proposes no containment or recovery mechanism.

**Answer to the assignment question:** Governance work is overwhelmingly **post-hoc** (failure attribution, audit trails, forensics, liability frameworks). Runtime governance exists and is booming in 2026, but it is **preventive policy/permission enforcement** (guardrails, deontic policies, capability scoping, execution-boundary control) — it gates actions, it does not *attribute and contain*. The tiny set of runtime works that do combine attribution with intervention (AAF; AgentTether; CHARM; DamageFlow/BlastGuard; Cognitive Immunity; classical Robust-JaCaMo accountability feedback chains) are all either non-LLM, single-agent/single-pipeline, or security-threat-modelled. **No verified work operationalizes accountability during execution to contain the organizational blast radius of a local fault in an LLM multi-agent workflow.** The closest classical tradition — normative MAS runtime enforcement (guards, supervisory control, electronic institutions) — has never been connected to LLM agent organizations.

---

## 2. Classical MAS: responsibility, blame, normative governance

### 2.1 Formal responsibility/blame models

| Paper | Venue/Year | Identifier | What it does | Relation to seed |
|---|---|---|---|---|
| Chockler & Halpern, "Responsibility and Blame: A Structural-Model Approach" | JAIR 2004 | DOI 10.1613/jair.1391 (verified on jair.org) | Degree of responsibility extending Halpern–Pearl causality; degree of blame over epistemic states | Foundational formalism for graded blame; structural causal models, not agents-with-roles |
| Halpern & Pearl, "Causes and Explanations: A Structural-Model Approach" (Parts I–II) | BJPS 2005 | DOI 10.1093/bjps/axi147, axi148 (Crossref-verified) | Actual causality formalism | Underlies all later causal attribution |
| Braham & van Hees, "An Anatomy of Moral Responsibility" | Mind 2012 | DOI 10.1093/mind/fzs081 (Crossref-verified) | Philosophical anatomy of responsibility | Conceptual background |
| Lorini, Longin & Mayor, "A logical analysis of responsibility attribution: emotions, individuals and collectives" | J. Logic and Computation 2013 | DOI 10.1093/logcom/ext072 (Crossref-verified) | Logic of individual/collective responsibility | Formal background |
| Yazdanpanah & Dastani, "Distant Group Responsibility in Multi-agent Systems" | PRIMA 2016 | OpenReview `DpKp7PFJMU` (abstract inspected) | Graded group responsibility in concurrent structures; responsibility for precluding states of affairs within k steps; framed as "managerial decision support … in multi-agent organizations" | Closest classical formalism to *organizational* responsibility; ex ante/managerial, not runtime containment |
| Yazdanpanah et al., "Strategic Responsibility Under Imperfect Information" | AAMAS 2019 | DOI 10.65109/ulyw9936 (Crossref-verified) | Responsibility under partial observability | Formal background |
| Yazdanpanah et al., "Different Forms of Responsibility in Multiagent Systems: Sociotechnical Characteristics and Requirements" | IEEE Internet Computing 2021 | OpenReview `5loEgoB4cJ` (abstract inspected) | Distinguishes responsible / blameworthy / accountable / sanctionable; research agenda | Terminological anchor |
| Yazdanpanah et al., "Responsibility Research for Trustworthy Autonomous Systems" | AAMAS 2021 | OpenReview `mp5TqAjbmP` (abstract inspected) | Roadmap for responsibility reasoning in TAS | Agenda-setting |
| Triantafyllou, Singla & Radanovic, "On Blame Attribution for Accountable Multi-Agent Sequential Decision Making" | NeurIPS 2021 | arXiv:2107.11927 (abstract inspected) | Blame attribution in cooperative MMDPs via cooperative game theory (Shapley, Banzhaf); shows Shapley is not performance-incentivizing; proposes new method | Blame as credit assignment in MARL; offline analysis, no LLMs, no containment |
| Triantafyllou & Radanovic, "Towards Computationally Efficient Responsibility Attribution in Dec-POMDPs" | AAMAS 2023 | arXiv:2302.12676 (S2 metadata) | Efficient responsibility attribution in Dec-POMDPs | Same line |
| Mu & Najib, "Counterfactual Reasoning for Causal Responsibility Attribution in Probabilistic Multi-Agent Systems" | IJCAI 2026 | arXiv:2605.13077 (abstract inspected) | Backward counterfactual responsibility in concurrent stochastic games; Shapley allocation with fairness/consistency proofs; NE computation trading responsibility vs reward | State-of-the-art formal responsibility; verification/strategic reasoning, not runtime containment; no LLMs |
| Qi Shi, "Responsibility in Extensive Form Games" | AAAI 2024 | OpenReview `ZKHkPhQGi1` (abstract inspected) | Seeing-to-it vs counterfactual responsibility in sequential settings; responsibility gap analysis | Formal background |
| Shi & Naumov, "Responsibility in Multi-Step Decision Schemes" | J. Philosophical Logic 2025 | OpenReview `saw0Hqglm9` (abstract inspected) | Higher-order responsibility, responsibility gap | Formal background |

### 2.2 Normative MAS governance and RUNTIME enforcement (classical)

This is the classical literature that most threatens the "runtime" novelty claim — it *did* operationalize norms during execution, two decades before LLMs.

| Paper | Venue/Year | Identifier | What it does | Runtime? |
|---|---|---|---|---|
| Esteva et al., "On the Formal Specification of Electronic Institutions" | LNCS (AMEC) 2001 | DOI 10.1007/3-540-44682-6_8 (Crossref-verified) | Formal specification of electronic institutions (roles, norms, scenes) | Design-time + institution-enforced runtime |
| Esteva, de la Cruz & Sierra, "ISLANDER: an electronic institutions editor" | AAMAS 2002 | OpenReview `RKuZJCX9pt` (abstract inspected) | Tool for specification/verification of e-institutions | Design-time |
| Grossi, Aldewereld & Dignum, "Ubi Lex, Ibi Poena: Designing Norm Enforcement in E-Institutions" | COIN@AAMAS/ECAI 2006 | OpenReview `tpXKmXbd0V` (abstract inspected) | Regimentation vs enforcement theory for e-institutions | Runtime enforcement concept |
| Lee, Padget, Logan, Dybalova & Alechina, "Run-time norm compliance in BDI agents" (N-Jason) | AAMAS 2014 | OpenReview `v953u0a8o2` (abstract inspected) | Norm-aware BDI deliberation; obligations with deadlines/priorities at runtime | **Runtime (agent-side compliance)** |
| Alechina, Bulling, Dastani & Logan, "Practical Run-Time Norm Enforcement with Bounded Lookahead" | AAMAS 2015 | OpenReview `4m08CQ1xOO` (abstract inspected) | Guards restricting actions after event histories (past-LTL); proves which norms are enforceable with bounded lookahead | **Runtime (system-side guards); the key classical containment formalism** |
| Dastani, Sardiña & Yazdanpanah, "Norm Enforcement as Supervisory Control" | PRIMA 2017 | OpenReview `hDTzc0Xe4F` (abstract inspected) | Norm enforcement via supervisory control of discrete-event systems; synthesizes enforcement mechanisms | **Runtime (control-theoretic)** |
| Bulling & Dastani, "Monitoring norm violations in multi-agent systems" | AAMAS 2013 | DOI 10.65109/jqdy6002 (Crossref-verified) | Norm violation monitoring | Runtime monitoring (detection, not containment) |
| Alechina, Dastani & Logan, "Norm approximation for imperfect monitors" | AAMAS 2014 | DOI 10.65109/nlfq3998 (Crossref-verified) | Approximating norms when monitors are imperfect | Runtime monitoring under noise |
| Modgil et al., "Monitoring compliance with E-contracts and norms" | Artificial Intelligence and Law 2015 | DOI 10.1007/s10506-015-9167-9 (Crossref-verified) | Compliance monitoring for e-contracts | Runtime monitoring |
| Riveret et al., "A Study of Ex Ante Law Enforcement in Norm-Governed Learning Agents" | JSAI-isAI 2012 | OpenReview `8lkyBcYs27` (abstract inspected) | Ex ante enforcement vs sanctions; cost of monitoring/enforcement | Runtime, cost-aware |
| Yan, Nardin, Hübner & Boissier, "An Agent-Centric Perspective on Norm Enforcement and Sanctions" (NPL(s)) | CoRR 2024 | OpenReview `KVsqqhVFOY` (abstract inspected) | Sanctions as first-class abstractions in BDI normative architecture | Runtime sanctioning (classical platform) |
| Singh, "Norms as a basis for governing sociotechnical systems" | ACM TIST 2013 | DOI 10.1145/2542182.2542203 (Crossref-verified) | Norms as governance basis for STS | Framework |
| Chopra & Singh, "Accountability as a Foundation for Requirements in Sociotechnical Systems" | IEEE Internet Computing 2021 | OpenReview `cSzoV8g0Ai` (abstract inspected) | Accountability requirements as relational constructs (commitments, authorization, prohibition); healthcare case | Design-time requirements |
| Sloan & Ajmeri, "Commitment-based negotiation semantics for accountability in multi-agent systems" (Nala) | Ann. Math. Artif. Intell. 2024 | OpenReview `KGVmgGnVmK` (abstract inspected) | Commitments capture accountability in negotiation | Design/protocol level |

### 2.3 Classical organizational accountability (JaCaMo line) — the closest classical analogue to the seed

| Paper | Venue/Year | Identifier | What it does | Relation to seed |
|---|---|---|---|---|
| Baldoni, Baroglio, May, Micalizio & Tedeschi, "Supporting Organizational Accountability Inside Multiagent Systems" | AI*IA 2017 | OpenReview `CH8rJ7NcfH` (abstract inspected) | Accountability as design property; accountability protocol between agent and organization; JaCaMo case study | Organizational accountability inside MAS — the seed's classical ancestor |
| Baldoni et al., "ADOPT JaCaMo: Accountability-Driven Organization Programming Technique" | PRIMA 2017 | OpenReview `xouHJ5SW4D` (abstract inspected) | ADOPT accountability protocol; model-checked | Organizational accountability protocol |
| Baldoni, Baroglio, Boissier, Micalizio & Tedeschi, "Accountability and Responsibility in Multiagent Organizations for Engineering Business Processes" | EMAS@AAMAS 2019 | OpenReview `wVsF2iwhXG` (abstract inspected) | Accountability patterns for business processes; "reporting to the right agents feedback about success or failure of a task" | **Accountability-driven failure feedback in organizational workflows — but design-time patterns, no blast-radius measurement** |
| Baldoni, Baroglio, Micalizio & Tedeschi, "Robust JaCaMo Applications via Exceptions and Accountability" | AAMAS 2023 | OpenReview `0MmARlZkEu` (abstract inspected) | Exception handling for MAS + accountability feedback chains for robustness | **Classical runtime recovery via accountability — but BDI/JaCaMo, no LLMs, no propagation measurement** |
| Cranefield, Oren & Vasconcelos, "Accountability for Practical Reasoning Agents" | AT 2018 | OpenReview `jBDTGE3Von` (abstract inspected) | "Accountable autonomy"; requirements for accountable agents | Conceptual |

**Classical verdict:** runtime norm enforcement, monitoring, and organizational accountability protocols all exist — for symbolic/BDI agents, with hand-specified norms, no stochastic LLM behavior, no natural-language communication channels, no memory poisoning, and no measurement of failure *spread*. The seed's contribution would be importing this tradition into LLM organizational workflows and adding the missing measurement (blast radius) and utility-preserving containment.

---

## 3. LLM era: failure attribution and responsibility (POST-HOC)

This cluster exploded in 2025–2026 and is now **crowded**. All of it is post-hoc diagnosis over completed traces.

| Paper | Venue/Year | Identifier | Key facts (verified from abstract) |
|---|---|---|---|
| Zhang et al., "Which Agent Causes Task Failures and When?" (Who&When) | ICML 2025 | arXiv:2505.00212 | Foundational failure-attribution benchmark; 127 MAS failure logs; best method 53.5% agent accuracy, 14.2% step accuracy; code+data public |
| Deshpande et al., "TRAIL: Trace Reasoning and Agentic Issue Localization" | CoRR 2025 | arXiv:2505.08638 | Error taxonomy + 148 annotated traces; best model (Gemini-2.5-pro) scores 11% |
| Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (MAST) | CoRR 2025 (NeurIPS 2025 ws) | arXiv:2503.13657 | 14 failure modes in 3 categories; 1600+ traces; κ=0.88 |
| Zhang et al., "AgenTracer" | CoRR Sep 2025 | arXiv:2509.03312 | Counterfactual replay + programmed fault injection; TracerTraj dataset; AgenTracer-8B beats Gemini-2.5-Pro/Claude-4-Sonnet by up to 18.18%; feedback gives MetaGPT/MaAS +4.8–14.2% |
| Chen et al., "Seeing the Whole Elephant" (TraceElephant) | ACL 2026 | arXiv:2604.22708 | Full-observability attribution benchmark; full traces improve accuracy up to 76% |
| Wang et al., "From Flat Logs to Causal Graphs" (CHIEF) | CoRR Feb 2026 | arXiv:2602.23701 | Hierarchical causal graph; distinguishes "true root causes from propagated symptoms" — propagation-aware but post-hoc |
| Qiao et al., "VerifyMAS" | CoRR May 2026 | arXiv:2605.17467 | Hypothesis-verification attribution over full trajectories |
| Wang et al., "DCFA" | CoRR Sep 2026 | arXiv:2609.04749 | Training-free dual-view causal attribution; +8.27% step accuracy on Who&When |
| Liu et al., "MASPrism" | CoRR 2026 | arXiv:2605.07509 (S2 metadata) | Lightweight prefill-stage-signal attribution |
| Xia et al., "Who Broke the System?" (AgentLocate) | COLM 2026 | arXiv:2607.07989 | Agent + earliest decisive step localization; multi-perspective verification |
| Li et al., "Towards Self-Improving Error Diagnosis" (ErrorProbe) | CoRR 2026 | arXiv:2604.17658 (listed; abstract from curated corpus) | Strategist/Investigator/Arbiter team with verified episodic memory |
| TRIAGE | ACL ARR 2026 May | OpenReview `dX2bmGPY3X` | Severity-ranked triage instead of single blamed step; 73.9% top-5 on Who&When; quantifies annotator/LLM disagreement (TriageBench) |
| FirstCause | ACL ARR 2026 Aug | OpenReview `CmglANVJkB` | Failure-lifecycle attribution: Rupture/Origin/Persistence factorization; Persistence tests whether the source remains relevant "after subsequent recovery opportunities" — recovery-aware but still post-hoc |
| DepTracer | ACL ARR 2026 May | OpenReview `lzyB79SJVL` | **Propagation-aware** attribution: continuous scores over trajectory segments; feeds closed-loop optimization (+10.16pp on GEPA) |
| In et al., "Rethinking Failure Attribution" (MP-Bench) | FAGEN@ICML 2026 | OpenReview `MSZgg7mUVZ` | Multi-perspective attribution; argues prior "LLMs can't attribute" conclusions were benchmark artifacts |
| Hu, Shukla & Huang, "Verifying the Verifiers" (AutoTriage) | LLA 2026; ICLR 2026 DATA-FM ws | OpenReview `B6QfT7SHh8`, `9cP3pDqcrZ` | Attributes benchmark failures to agent vs task defects; agentic judge with sandbox access |
| "From Failure Attribution to Reliability Enhancement in LLM-based MAS: A Survey" | ACL ARR 2026 May | OpenReview `RbhZpFJAjY` | 5Ws formalization; four method paradigms; **explicitly adds "How" — turning attribution into runtime intervention and post-hoc refinement** (roadmap, not a system) |
| Qi et al., "Beyond Individual Intelligence" (survey) | CoRR 2026 | arXiv:2605.14892 (S2 metadata) | Collaboration + failure attribution + self-evolution survey |
| Parakh & Feigh, "Biased Error Attribution in Multi-Agent Human-AI Systems Under Delayed Feedback" | CoRR 2026 | arXiv:2603.23419 | Humans misattribute responsibility across AI agents under delayed feedback (human-subjects) |

**Verdict:** attribution is saturated and explicitly post-hoc; the survey (`RbhZpFJAjY`) already names runtime intervention as the open "How". A pure "attribute the fault better" paper is DOA. The seed is *not* an attribution paper — it is about what happens after/between attribution: propagation and containment. But it must cite this cluster and position against it.

---

## 4. LLM era: audit trails, provenance, observability (POST-HOC infrastructure)

| Paper | Venue/Year | Identifier | Key facts |
|---|---|---|---|
| Du & Chen, "AUDITA: certified auditing and causal attribution of adverse outcomes in autonomous MAS" | CoRR Aug 2026 | arXiv:2608.22160 | Tamper-evident inter-agent command record + certified graded causal attribution; provably ungameable verdicts; ~3× lower responsibility error than judge baseline on live LM pipelines; **post-hoc audit layer, embodied-fleet framing** |
| Liu et al., "LEDGER: Claim-to-Evidence Trace Graphs for Auditing LLM Agents" | CoRR Aug 2026 | arXiv:2608.18398 | Layered evidence/decision graphs over agent sessions for human review |
| Sharad, "Observability for Delegated Execution in Agentic AI Systems" | CoRR Jun 2026 | arXiv:2606.09692 | Proves delegation scope is not identifiable from standard traces; gateway + common information model binding delegation context at execution time; forensic queries |
| Yu et al., "Agent-Native Telemetry" | CoRR Aug 2026 | arXiv:2608.16178 | Verifiable state-delta evidence ledger; hash-chained, signed; verified-negative theorem; AIOpsLab evaluation |
| "Governance Trace Embedding" | AAAI 2026 AIGOV ws submission | OpenReview `ivTQR1fS1K` | Conceptual: accountability metadata embedded in outputs |
| "Governance Drift" | AAAI 2026 AIGOV ws submission | OpenReview `LlQntOHdyl` | Citation instability as accountability violation; Governance Stability Index |
| Guan et al., "Monitoring Monitorability" | CoRR Dec 2025 | arXiv:2512.18311 | CoT monitorability metrics; monitor scaling |
| Staufer et al., "The 2025 AI Agent Index" | FAccT 2026 | arXiv:2602.17753 | 30 deployed agents; most developers share little safety/evaluation info |
| Pathak et al., "Detecting Silent Failures in Multi-Agentic AI Trajectories" | CoRR Nov 2025 | arXiv:2511.04032 | Anomaly detection over trajectories (drift, cycles); up to 98% accuracy |
| Huo et al., "Towards Risk-free AI Agent Deployment" | CoRR Aug 2026 | arXiv:2608.16411 | Position: trajectory-grounded testing/debugging; deployment-readiness checklist |

**Verdict:** audit infrastructure is being built actively, all oriented to *after-the-fact* review or compliance evidence. AUDITA is the strongest (certified, ungameable, causal) and is explicitly an audit layer, not a runtime containment mechanism.

---

## 5. LLM era: runtime governance — preventive, not accountability-driven

A dense 2025–2026 cluster enforces policy/permissions **during** execution. None performs responsibility attribution or models failure propagation; enforcement is action-level gating.

| Paper | Venue/Year | Identifier | What it enforces at runtime |
|---|---|---|---|
| Poskitt et al., "AgentSpec" | ICSE 2026 | arXiv:2503.18666 | DSL rules (trigger/predicate/enforcement) over single-agent action streams; ms overhead |
| Xiang et al., "GuardAgent" | ICML 2025 | arXiv:2406.09187 | Guardrail agent generating guardrail code from safety requests; EICU-AC, Mind2Web-SC |
| Liu et al., "AgentDoG" | CoRR 2026 | arXiv:2601.18491 | Diagnostic guardrail with root-cause labels over trajectories (3-dim risk taxonomy, ATBench) |
| Liu et al., "Organizational Control Layer (OCL)" | CoRR Jun 2026 | arXiv:2606.04306 | Execution-boundary interception: approve/revise/block/escalate against role, policy, economic constraints; unsafe executions 88%→0%, valid success 12%→96%; ablations credit "pre-execution enforcement with structured recovery" |
| Finin et al., "Deontic Policies / AgenticRei" | IEEE ICWS 2026 | arXiv:2606.19464 | Obligations, dispensations, conflict resolution over tool calls and A2A messages; logic engine outside the LLM |
| Shlomov et al., "Governance by Construction" (CUGA) | CoRR May 2026 | arXiv:2605.20874 | Five governance checkpoints (intent guard, playbook, tool guide, human approvals, output formatter) |
| Kang et al., "PolicyGuide" | CoRR Aug 2026 | arXiv:2608.19861 | Policy compiled to workflow graph; proactive verifier at user-turn boundaries with remediation; τ²-bench Pass⁴ 0.42→0.62 |
| Ge et al., "Layered Governance Architecture (LGA)" | CoRR Mar 2026 | arXiv:2603.07191 | Sandboxing, intent verification, zero-trust inter-agent authorization, immutable audit logging; 96% interception |
| Syros et al., "SAGA" | CoRR 2025 | arXiv:2504.21034 | Cryptographic access-control tokens for inter-agent communication; user-controlled agent lifecycle |
| Noyan et al., "Dynamic Capability Scoping" | ICML 2026 AIWILD | arXiv:2607.22445 | Dynamic least privilege: role ceilings + task-context classifier + combination prohibitions; 600-prompt dataset |
| Malik et al., "Decentralized Granular Access Control" | CoRR 2026 (Microsoft Azure report) | arXiv:2607.22611 | Compound identity binding agent actions to delegated human authority; 5-level permission granularity; production: 20+ agents, zero unauthorized writes in 8 months |
| Michael et al., "How Agents Ask for Permission" | CoRR 2026 | arXiv:2607.13718 | Survey of 21 permission proposals + 5 commercial agents; runtime enforcement taxonomy and gaps |
| Rabinovich et al., "Towards Enforcing Company Policy Adherence in Agentic Workflows" | EMNLP 2025 industry | arXiv:2507.16459 | Policy documents compiled to guard code checked before each action; τ-bench Airlines |
| Alamdari, Klassen & McIlraith, "Auditing, Monitoring, and Intervention for Compliance" | ICML 2025 R2-FM ws | OpenReview `F7stSziqXZ` | Formal-methods monitors for temporally extended behavioral constraints; **intervening monitors that act at runtime** |
| Debenedetti et al., "CaMeL" | CoRR 2025 | arXiv:2503.18813 | Capability-based security policies at tool calls; prompt-injection proof; 77% AgentDojo with provable security |
| Villa et al., "Prismata" | CoRR 2026 | arXiv:2607.08147 | Contextual least privilege + structural confinement for web agents |
| Stanley et al., "GAAP" | CoRR 2026 | arXiv:2604.19657 | Information-flow control over private data disclosures across tasks |
| Fan et al., "Harness-MU" | CoRR 2026 | arXiv:2606.21856 (listed; curated-corpus abstract) | Multi-principal access control via deterministic execution hooks |
| Wang et al., "Agent Safety Should Be a Runtime Contract" | CoRR 2026 (position) | arXiv:2608.11274 | Position: preventive + evidential runtime contract in the harness; Agent Trajectory Schema and Evidence Chain; documents 8–12× training-vs-deployment publication imbalance |
| Jing et al., "Isolation as a First-Class Principle" | CoRR 2026 (survey/position) | arXiv:2607.12406 | **Boundary-centric taxonomy (user-agent, agent-tool, agent-execution, agent-agent, system-environment); cross-boundary failure paths; "how compromise propagates across boundaries"** — security framing, no accountability, no recovery |
| South et al., "Authenticated Delegation and Authorized AI Agents" | CoRR Jan 2025 | arXiv:2501.09674 | OAuth/OIDC extension for delegation chains with accountability metadata |
| Lee & Park, "AI Kill Switch for Malicious Web-based LLM Agents" (AutoGuard) | ICLR 2026 submission | OpenReview `NaWaS3eaKx` | Defensive prompts in DOM trigger malicious agents' own safety mechanisms to halt them |

**Verdict:** runtime *governance* is real and crowded; runtime *accountability* (attribute → contain → recover) is not what any of these do. The Isolation survey (2607.12406) owns the "boundaries + propagation" vocabulary in the security register; the seed must distinguish organizational-fault propagation from adversarial-compromise propagation.

---

## 6. The four works that DO combine attribution with runtime action

| Work | Venue/Year | Identifier | Runtime loop | Why it does NOT subsume the seed |
|---|---|---|---|---|
| **AAF — Adaptive Accountability Framework** (Alqithami) | CoRR Dec 2025, v3 Mar 2026 | arXiv:2512.18561 | Crypto-verifiable provenance → streaming change-point detection → causal-influence-graph responsibility attribution → cost-bounded interventions (reward shaping, policy patching); bounded-compromise guarantee; 87,480-run factorial, up to 500 agents; 96% of regimes improved; attribution accuracy 0.97 at 10% Byzantine | RL/PPO agents, not LLMs; target is emergent norm violation (collusion/hoarding), not local faults; interventions are RL-specific; no organizational boundaries (roles, authority, human); no task-utility-preservation analysis (social welfare is a side metric) |
| **DamageFlow + BlastGuard** (Yagiz) | ICML 2026 AIWILD | OpenReview `MYvsxnxbCf` | Blast Radius Score (resource sensitivity × action impact × **propagation** × recovery cost) via deterministic state-diff oracles; BlastGuard runtime: least-privilege capability graphs, untrusted-flow tracking, dry-run gating, scoped tokens, rollback logs; 80-scenario pilot; 87.5% benign utility retained | Adversarial threat model (prompt injection, tool poisoning, shadowing, relay attacks); damage = unauthorized tool effects on environment state, not organizational propagation; no responsibility attribution; single-author workshop pilot |
| **AgentTether** (Zhao et al.) | CoRR Jul 2026 | arXiv:2607.06273 | Post-run diagnosis (Critical Transition Graph) + repair memory + **guarded runtime intervention during re-execution**; repairs 59–65% of failed τ-bench tasks | Single-agent tool-use; repair of the same agent's trajectory, not containment of spread to other agents/roles; no accountability semantics |
| **CHARM** (cascading hallucination) | CoRR 2026 | OpenReview `EjifLedI9C` | Stage-level fact verification + cross-stage consistency + confidence-propagation monitoring + **cascade resolution triggering** — detects and interrupts error propagation in agentic RAG pipelines | Single-pipeline factual-error cascades; no multi-agent organization, no accountability |

Plus two smaller runtime items: **Cognitive Immunity** (KDD 2026 SeT-LLM ws, OpenReview `eiw7dgCNad`) — runtime failure-memory layer with auditable intervention provenance, single agent; **Robust JaCaMo** (AAMAS 2023, §2.3) — classical accountability feedback chains for robustness.

**This is the decisive table for the assignment question.** Runtime accountability-as-containment exists only as (a) AAF in RL-MAS, (b) security containment in DamageFlow, (c) single-agent repair in AgentTether/CHARM. The organizational, LLM-native, fault-(not-attack-)driven, utility-preserving version is unoccupied.

---

## 7. Governance frameworks, liability, and the legal/philosophical layer

| Work | Venue/Year | Identifier | Content |
|---|---|---|---|
| Kolt, "Governing AI Agents" | SSRN 2024 (law) | DOI 10.2139/ssrn.4772956 (Crossref-verified; SSRN page 403 from this host, abstract not inspected) | Legal governance of AI agents — *unverified-abstract* |
| Osmond, "Liability Frameworks for Agentic AI Systems" | ICML 2026 AIWILD | OpenReview `SZhxWYzKb1` (abstract inspected) | Trajectory-based governance, strict-liability tiers, mandatory trajectory auditing, Basel-style capital charges; regulatory proposal |
| Chopra & White, "A Legal Theory for Autonomous Artificial Agents" | Book, Univ. of Michigan Press 2011 | DOI 10.3998/mpub.356801 (Crossref-verified) | Legal theory of agent liability/contracting |
| Chopra, "OAuth Is Not Enough: Authorization Challenges for Autonomous AI Agents" | TechRxiv 2025 | DOI 10.36227/techrxiv.174952577.74018032/v1 (Crossref-verified) | Authorization gaps for agents |
| Matthias, "The responsibility gap" | Ethics and Information Technology 2004 | DOI 10.1007/s10676-004-3422-1 (Crossref-verified) | Foundational responsibility-gap argument |
| Elish, "Moral Crumple Zones" | Engaging Science, Technology, and Society 2019 | DOI 10.17351/ests2019.260 (Crossref-verified) | Humans as liability sinks in hybrid systems — directly relevant to the seed's human-agent boundary dimension |
| Porter et al., "Unravelling Responsibility for AI" | CoRR 2023 | OpenReview `8ZZR1hZrzo` (abstract inspected) | "Actor A responsible for Occurrence O" clarification |
| Porter et al., "The Moral Responsibility Gap and the Increasing Autonomy of Systems" | SAFECOMP ws 2018 | OpenReview `3Jy12fXcyW` (abstract inspected) | Causal + epistemic dimensions of the gap |
| Tomasev et al., "Virtual Agent Economies" | CoRR Sep 2025 | arXiv:2509.10147 | Sandbox-economy framework; socio-technical infrastructure for trust/safety/accountability in agent markets |
| Franklin et al., "AI Governance through Markets" | CoRR 2025 | arXiv:2501.17755 | Insurance/auditing/procurement/due-diligence as market governance |
| OWASP Agentic Security Initiative, "Agentic AI — Threats and Mitigations" | OWASP 2025 (web) | genai.owasp.org (page inspected) | Threat-model reference for agentic systems; industry governance baseline |
| Hu et al., "Stop Reducing Responsibility in LLM-Powered MAS to Local Alignment" | CoRR 2025 (position) | OpenReview `1EwGlEYYLl` | Responsibility as lifecycle-wide property (agreement, uncertainty, security); dual-perspective governance framework; no experiments |
| Zhu et al., "Interpreting Agentic Systems: … System-Level Accountability" | CoRR 2026 (position) | OpenReview `rxdYAi3YbD` | Interpretability-by-design for traceability/accountability; position |
| Imteyaz et al., "'Nobody Did This': Contribution, Originality, and Accountability in Agent-Mediated Collaboration" | CoRR 2026 (workshop proposal) | arXiv:2607.26387 | "Contribution dissolution" in agent-mediated knowledge work |
| La Malfa et al., "Unaccountable Delegation, Fading Skills" | CoRR 2026 | arXiv:2608.08601 | 15-category workplace agent-risk taxonomy over 2,078 O*NET tasks; erroneous agent actions largest/severe category, concentrated at human-agent boundary |
| Mitchell et al., "AI Agents Push Humans Out of the Loop" | CoRR 2026 (position) | arXiv:2608.23642 | Oversight degradation by design; human-overseer support agenda |
| Seth et al., "Behavioural Assurance Cannot Verify the Safety Claims Governance Now Demands" | CoRR 2026 (position) | arXiv:2605.15164 | The "audit gap": required vs achievable verification access |
| Ye & Steinhardt, "Norm Enforcement for AI Agents: Robustly Shaping Behavior in MAS" | CoRR 2026; COLM 2026 WAB; AI4GOOD 2026 spotlight | OpenReview `el9n84w0Wq` | **Runtime norm enforcement for LLM agents**: reliability estimation + escalating penalties; simple enforcement is exploited by misaligned agents; 3 simulated environments. Sanctioning-regime work — overlaps the already-killed "sanctioning under unreliable blame" territory |
| Paglieri et al., "Emergent Cheating and Whistleblowing in Autonomous Research Swarms" | CoRR Sep 2026 | arXiv:2609.04170 | 100-agent swarm; exploit spreads via shared knowledge library + P2P messages; emergent auditing/whistleblowing/boycotts; Ostrom commons-governance framing. **Evidence of behavioral contagion across memory+communication boundaries and emergent containment — but strategic cheating, not faults; no accountability mechanism design** |
| Li et al., "Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce" | CoRR Aug 2026 | arXiv:2608.14825 | 12.6% of 2,583 inter-agent emails misaligned; reciprocal (1.65×) and stress-conditioned (1.58×) — misalignment propagates between agents |
| Li et al., "Governance at the Boundary / Fiducia-bench" | CoRR Aug 2026 | arXiv:2608.16055 | Decomposition degrades governability at handoffs (0%/56%/85% fact attenuation by architecture); escalation/abstention/audit-trail benchmark |
| Ding et al., "Always-On Agents" (survey) | CoRR Jun 2026 | arXiv:2606.30306 | 435-work corpus: "literature concentrates more heavily on accumulating and retrieving state than on **governing, recovering, or relinquishing** it"; AOEP-v0 scores state mutation and **recovery** obligations |

---

## 8. Direct answer: runtime containment vs post-hoc auditing

**Post-hoc dominates.** Failure attribution (§3), audit/provenance (§4), liability/regulatory frameworks (§7) are all after-the-fact. The attribution survey (`RbhZpFJAjY`) explicitly flags the attribution→intervention connection as an open "How".

**Runtime work splits into three kinds, none of which is organizational accountability-driven containment:**
1. **Preventive gating** (§5): action-level policy/permission/capability enforcement. It prevents *unauthorized* actions; it does not detect a local fault, attribute it, and contain its *spread*. OCL's "structured recovery" and PolicyGuide's "remediation" are per-action/per-turn, not system-level containment.
2. **Runtime diagnosis + repair of a single agent/pipeline** (§6: AgentTether, CHARM, Cognitive Immunity): recovery exists but is agent-local; nothing about propagation to other agents, roles, shared memory, or human principals.
3. **System-level runtime accountability loops** (§6: AAF; classically §2.2–2.3): AAF is the only LLM-era-adjacent closed loop and it is RL-only, norm-violation-only. The classical normative-MAS tradition (guards, supervisory control, e-institutions, JaCaMo accountability) did runtime enforcement/containment for symbolic agents and has not been re-instantiated for LLM organizations.

**Negative results (searched, nothing found):** no "circuit breaker for LLM agents" work (OpenReview term search returns only power-systems papers); no agent "quarantine" mechanisms; no "error propagation in LLM multi-agent" measurement work; no "cascading failure" work for agentic systems beyond CHARM's single-pipeline version; no organizational-failure testbeds.

---

## 9. Threats to the seed hypothesis and required differentiation

1. **DamageFlow/BlastGuard** owns "blast radius" + propagation + recovery-cost + runtime containment + utility preservation — in the *security* register. The seed must either (a) frame explicitly as non-adversarial organizational faults across organizational boundaries (role, authority, memory, accountability, human), or (b) risk looking like a workshop-paper extension. Note DamageFlow's BRS propagation component is about instruction relay between agents under attack — partially overlapping the communication boundary.
2. **AAF** owns "runtime accountability" as a closed loop. Differentiate: LLM organizational workflows, fault (not norm-violation) trigger, containment mechanisms that are organizational (escalation, delegation revocation, role failover, memory isolation, human handoff) rather than reward shaping.
3. **Governance at the Boundary** owns "decomposition/handoffs degrade governance" empirics. Cite as motivation; it has no containment/recovery.
4. **Isolation survey** owns boundary-centric propagation vocabulary for security. Cite and distinguish threat model.
5. **Failure-attribution cluster** (§3) owns post-hoc blame. The seed should use it as the attribution substrate, not compete with it.
6. **Occupied territory reminder:** policy-preserving delegation + causal accountability across A2A/MCP chains is taken by the existing MASO proposal (`maso/policy_preserving_delegation_research_proposal.md`); sanctioning/reputation regimes are killed (`research_specs/03_sanctioning_under_unreliable_blame.md`, and Ye & Steinhardt 2026 further occupy robust norm enforcement). The seed's containment mechanisms should avoid re-entering sanctioning-as-governance.
7. **Classical exposure:** reviewers from COINE will know e-institutions, guards (Alechina et al. 2015), supervisory control (Dastani et al. 2017), and JaCaMo accountability (Baldoni et al. 2017–2023). The paper must frame as *re-instantiating organizational containment for stochastic LLM agents with measured blast radius* — the measurement and the LLM-specific propagation channels (natural-language context, shared memory, tool state) are the novel core.

## 10. What remains genuinely open (supporting the seed)

- No measured "organizational blast radius" construct for LLM MAS faults (DamageFlow's BRS is the nearest, security-only, tool-state-only).
- No containment mechanism comparison (quarantine, escalation, rollback, delegation revocation, memory isolation, human handoff) under fault injection in organizational LLM workflows.
- No runtime accountability loop for LLM organizations (AAF is the template, RL-bound).
- No testbed with organizational boundaries (role/authority/memory/human) as first-class propagation surfaces.
- Always-On Agents survey (2606.30306) independently confirms governance/recovery are the neglected poles of the agent-state literature.

## 11. Verification log

- arXiv abstract pages inspected individually: 2505.00212, 2505.08638, 2512.18561, 2503.18666, 2504.21034, 2503.18813, 2606.04306, 2606.19464, 2406.09187, 2605.20874, 2606.09692, 2608.19861, 2608.22160, 2605.13077, 2602.23701, 2604.22708, 2605.17467, 2603.23419, 2609.04749, 2607.22445, 2607.22611, 2107.11927, 2509.10147, 2501.09674, 2509.03312, 2608.18398, 2511.04032, 2608.16178, 2607.26387, 2603.07191, 2608.08601, 2501.17755, 2608.23642, 2605.15164, 2609.07984, 2503.13657, 2512.18311, 2608.16411, 2607.06273, 2608.16055, 2607.12406, 2608.11274, 2601.18491, 2607.07989, 2607.13718, 2606.30306, 2609.04170, 2607.08147, 2604.19657, 2608.14825, 2507.16459, 2602.17753.
- OpenReview records inspected (abstracts): MYvsxnxbCf (DamageFlow), lzyB79SJVL (DepTracer), dX2bmGPY3X (TRIAGE), CmglANVJkB (FirstCause), RbhZpFJAjY (FA survey), MSZgg7mUVZ (MP-Bench), B6QfT7SHh8/9cP3pDqcrZ (AutoTriage), VDi06uX433 (TraceElephant), el9n84w0Wq (Ye & Steinhardt), 1EwGlEYYLl, rxdYAi3YbD, ivTQR1fS1K, LlQntOHdyl, SZhxWYzKb1, 8ZZR1hZrzo, eiw7dgCNad, NaWaS3eaKx, EjifLedI9C (CHARM), oQ22OMla64 (CFRL), F7stSziqXZ (Alamdari), 4m08CQ1xOO, v953u0a8o2, DpKp7PFJMU, mp5TqAjbmP, 5loEgoB4cJ, CGIXwNdsdA, ZKHkPhQGi1, saw0Hqglm9, 3Jy12fXcyW, tpXKmXbd0V, cd6NSHHR7v, 8lkyBcYs27, hDTzc0Xe4F, WFIHvp0ZEk/KVsqqhVFOY, RKuZJCX9pt, a0VXoP9DQY, cSzoV8g0Ai, KGVmgGnVmK, uKgaspW3V8, jBDTGE3Von, CH8rJ7NcfH, xouHJ5SW4D, wVsF2iwhXG, xZCzo0XvEx, 0MmARlZkEu, 2KKqp7MWJM (AgentAuditor).
- Crossref-verified bibliographic records: 10.1613/jair.1391 (also inspected on jair.org), 10.1093/bjps/axi147, 10.1093/bjps/axi148, 10.1093/mind/fzs081, 10.1093/logcom/ext072, 10.65109/ulyw9936, 10.65109/jqdy6002, 10.65109/nlfq3998, 10.1007/s10506-015-9167-9, 10.1145/2542182.2542203, 10.1007/3-540-44682-6_8, 10.1007/s10676-004-3422-1, 10.17351/ests2019.260, 10.3998/mpub.356801, 10.36227/techrxiv.174952577.74018032/v1, 10.2139/ssrn.4772956.
- Web pages inspected: OWASP Agentic AI Threats and Mitigations (genai.owasp.org).
- Discovery-only corpora (entries re-verified before inclusion): masamasa59/ai-agent-papers operations/governance.md + operations/agentops.md; /tmp/AGENTS.md (awesome-llm-agent-papers copy).
- Channel limitations: Semantic Scholar API and arXiv listing API heavily rate-limited (partial use); DBLP unreachable; SSRN 403; OpenReview challenged intermittently (paced retries succeeded). Items marked *unverified-abstract* assert bibliographic metadata only.
