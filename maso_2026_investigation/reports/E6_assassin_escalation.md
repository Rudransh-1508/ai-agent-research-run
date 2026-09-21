# ASSASSIN E6 — Kill Attempt via Human-Escalation & Mixed-Initiative Recovery

**Date:** 2026-09-21
**Mission:** Try to kill/subsume the seed hypothesis ("organizational failure propagation and recovery in LLM multi-agent systems; organizational blast radius; containment/recovery mechanisms that minimize systemic impact while preserving task utility") via the literature on human-in-the-loop fault recovery, escalation as containment, mixed-initiative recovery, oversight-as-intervention with measured cost, and any 2025–2026 comparison of human escalation vs automated containment.
**Stance:** Adversarial. Goal is to find the paper(s) that make the seed redundant.

## Search channels actually used (and their failures)

- arXiv **abs pages** and **monthly listing pages** (`arxiv.org/abs/<id>`, `arxiv.org/list/cs.XX/YYYY-MM`) — WORKED; primary verification + discovery channel. Scanned cs.MA/cs.AI/cs.CL/cs.HC/cs.CR for 2026-08 and 2026-09 with a keyword filter (escalat*, human-in-the-loop, recover*, oversight, mixed-initiative, defer*, interven*, contain*, fault, failure, blast, resilien*, handoff, supervis*, monitor*).
- **Crossref API** — WORKED; metadata + some abstracts (incl. SSRN).
- **OpenReview search API** (`api2.openreview.net/notes/search`) — WORKED but shallow corpus; note-detail endpoints challenged (403).
- **Semantic Scholar API, arXiv export API, arXiv HTML search, dblp, OpenAlex** — all rate-limited/bot-blocked from this IP during the session (429/403). Searches there may have been exhausted by other swarm agents; residual discovery risk noted below.

## Bottom-line judgment

**The E6 kill attempt FAILS to kill the seed, but it badly wounds one dimension of it.** The *human-agent boundary* mechanism space (escalation, deferral, oversight-with-cost, HITL approval) is heavily occupied from classical MAS (adjustable autonomy, 2001–2002) through learning-to-defer (2018–2024), robot help-seeking (CoRL 2023), AI-control protocols with measured audit budgets (ICML 2024), HRI failure recovery (HRI 2026), up to Sept-2026 arXiv work measuring human interventions at fault points in LLM multi-agent systems and attacks on HITL approval itself. **However, no located paper compares human escalation vs automated containment for *propagating* failures in *organizational* LLM MAS, and none measures escalation's effect on a multi-boundary blast radius.** The seed's novelty, if any, lies in the org-level propagation + containment comparison, not in escalation per se. A separate Aug-2026 paper (OrchestraBench, §4.1) is a bigger threat to the seed than anything in my assigned lane.

---

## 1. Most damaging paper (E6 lane)

### 1.1 "Examining the Vulnerability of Multi-Agent Medical Systems to Human Interventions for Clinical Reasoning" — arXiv:2609.02191 (Sept 2026)

| Field | Value |
|---|---|
| Title | Examining the Vulnerability of Multi-Agent Medical Systems to Human Interventions for Clinical Reasoning |
| Authors | Benjamin C. Liu, Dillon Mehta, Rishi Malhotra, Adam Zobian, Yong Ying Tan, Samir Chopra, Daniella Rand, Natalie Pang, Abhiram Gudimella, Kevin Zhu |
| Year/Venue | 2026-09, arXiv preprint (cs.AI) |
| ID/URL | arXiv:2609.02191, https://arxiv.org/abs/2609.02191 |
| Problem | What happens when a *human* intervenes at "fault points" inside a multi-agent LLM medical system? |
| Method | Defines fault points as moments in agent conversations where reasoning is most vulnerable to external influence; injects correct vs incorrect/biased human interventions; measures shifts in reasoning and accuracy. |
| Setting/Data | Simulated doctor–patient conversations; MedQA dataset. |
| Metrics | Diagnostic accuracy change, diagnostic drift, uncertainty. |
| Major findings | Correct interventions improve baseline diagnostic accuracy up to **+40%**; incorrect/bias-related interventions degrade it up to **−6%** and increase drift/uncertainty. |
| Author-stated limitations | Not extracted (abstract only inspected). |
| Inferred limitations | Single domain (medical QA conversation), no tool/authority/memory boundaries, no propagation across an org topology, no comparison against *automated* containment, simulated (not real) patients. |
| Code | Not found. |
| Relation to seed | Directly occupies "oversight-as-intervention with measured cost/benefit" on the human-agent boundary of an LLM MAS, including the double-edged nature of human escalation (helps when right, hurts when wrong). It does NOT measure blast radius or compare escalation to automated containment — so it wounds the human-boundary dimension without subsuming the seed. |

**Why this is the single most damaging in-lane paper:** it is the closest 2025–2026 work to "human escalation as a recovery intervention in an LLM multi-agent system, with measured effect." Any MASO submission must cite it and differentiate (org topology, propagation, containment comparison).

### 1.2 Runner-up (different kill vector): AI Control — the only verified *comparison* of human escalation vs automated containment

| Field | Value |
|---|---|
| Title | AI Control: Improving Safety Despite Intentional Subversion |
| Authors | Ryan Greenblatt, Buck Shlegeris, Kshitij Sachan, Fabien Roger |
| Year/Venue | 2023-12 (v1); ICML 2024 (per arXiv comments) |
| ID/URL | arXiv:2312.06942, https://arxiv.org/abs/2312.06942 |
| Problem | Safety protocols for LLM agents that remain robust when the model actively subverts them. |
| Method | Pipelines ("protocols") mixing an untrusted strong model (GPT-4), a trusted weak model (GPT-3.5), and **limited trusted (human) labor**; e.g., trusted editing, defer-to-human on suspiciousness threshold. Evaluates usefulness vs safety tradeoff. |
| Setting/Data | Sequence of programming problems; backdoors operationalized as errors uncaught by tests. |
| Metrics | Safety (no backdoored submissions) vs usefulness; cost of trusted labor. |
| Major findings | Protocols such as trusted editing dominate; human labor is a budgeted escalation resource traded against automated checking. |
| Limitations (inferred) | Adversarial-subversion frame (not accidental organizational faults); single-agent code generation, not multi-agent org; human labor modeled as abstract resource, not an organizational role. |
| Code | Released by Redwood Research (per project; not re-verified today). |
| Relation to seed | This IS a rigorous human-escalation-vs-automated-containment comparison with measured cost — but for intentional subversion in single-agent coding, not failure propagation in org MAS. It occupies the *methodological template* (Pareto of containment cost vs utility) the seed would need. |

---

## 2. Human-in-the-loop fault recovery / escalation-as-containment (verified)

| Paper | Authors, Year, Venue | ID | What it does | Relation to seed |
|---|---|---|---|---|
| Robots That Ask For Help (KnowNo) | Ren et al., 2023, CoRL 2023 Oral | arXiv:2307.01928 | Conformal-prediction uncertainty alignment so LLM planners ask for human help with statistical task-completion guarantees while **minimizing human help** | Escalation-as-containment with formal cost minimization; single robot, ambiguity-driven (not fault-propagation) |
| A Human-in-the-Loop Confidence-Aware Failure Recovery Framework for Modular Robot Policies | Banerjee, Palempalli, Yang, Fang, 2026, ACM/IEEE HRI 2026 | DOI 10.1145/3757279.3788668 | HITL failure recovery for robot policies, confidence-aware escalation | Direct "human-in-the-loop fault recovery" — robotics, single-agent |
| Explainable AI for Robot Failures | Das, Banerjee, Chernova, 2021, HRI | DOI 10.1145/3434073.3444657 | Explanations of robot failures to support human diagnosis/recovery | Precursor: human as recovery agent needs failure explanations |
| Predict Responsibly: Learning to Defer | Madras, Pitassi, Zemel, 2018, NeurIPS | arXiv:1711.06664 | Two-stage model+external decision-maker; model may "Pass" to human | Canonical deferral; classification, not agents |
| Post-Hoc Estimators for Learning to Defer to an Expert | Narasimhan, Jitkrittum, Menon, Rawat, 2022, NeurIPS 35 | DOI 10.52202/068431-2124 | Post-hoc deferral mechanisms | Deferral lineage |
| Loopjacking: Hijacking Human-in-the-Loop Approval | Arun Kumar, 2026-09, arXiv | arXiv:2609.21081 | Shows HITL approval is itself a failure/attack channel: human approves operation A, implementation executes materially different B (representation-based and post-approval state-substitution variants) | **Escalation channel is part of the blast radius, not outside it** — supports seed's premise that human boundary is a propagation surface |
| Human-on-the-Loop: A Theory of Oversight Capacity, Its Failure Modes, and the Non-Delegable Residual in the Age of AI Agents | Kadowaki, 2026, SSRN | DOI 10.2139/ssrn.7296638 | Theoretical: loop position fixed by ratio of consequence latency to overseer response latency; oversight as **consumable resource with solvency condition** (attention, context re-acquisition cost, neglect time) | "Oversight-as-intervention with measured cost" — theory only, no experiments |
| Conversational AI Agents for Financial Operations with Escalation-Aware Handoff Protocols | (no authors listed), 2026, IJISAE | DOI 10.17762/ijisae.v14.1s.8190 | Escalation-aware AI→human handoff protocols in financial ops | Design paper in low-quality venue; treat as weak evidence of occupied territory |
| Agent-MD: Selective LLM Intervention with Event-Driven Escalation | Wang, Yin, Tang, Chu, 2026-08, arXiv | arXiv:2608.07637 | Rule-based persistent campaign agent escalates to LLM reasoning at event-triggered review points (molecular-dynamics campaigns) | Tiered escalation between automated components (LLM as "supervisor tier"), not human; occupies "event-driven escalation" pattern |
| Tiered Agentic Oversight (TAO) | Kim et al. (incl. Ghassemi, Breazeal, H.W. Park), submitted ICLR 2026 | OpenReview mPh4B1JoAN | Hierarchical multi-agent oversight inspired by clinical nurse→physician→specialist escalation; "absorbs up to 24% of individual agent errors before they compound"; +8.2% over baselines on 4/5 healthcare safety benchmarks; ablations: adaptive > static tiers, lower tiers indispensable | **Automated hierarchical escalation as containment with measured error-absorption** — closest to "escalation as containment" in LLM MAS, but escalation stays machine-side |

## 3. Mixed-initiative / handoff (verified)

| Paper | Authors, Year, Venue | ID | Relation |
|---|---|---|---|
| CowPilot: A Framework for Autonomous and Human-Agent Collaborative Web Navigation | Huq, Wang, Xu, Ou, 2025, NAACL 2025 System Demos | DOI 10.18653/v1/2025.naacl-demo.17 | Human↔agent handoff during web tasks; mixed-initiative execution (task-driven, not fault-recovery-driven) |
| τ-bench: Tool-Agent-User Interaction | Yao, Shinn, Razavi, Narasimhan, 2024 | arXiv:2406.12045 | **Negative result:** full-text grep of HTML shows zero occurrences of "escalat*", "handoff", "transfer to human", "human agent/operator/representative" — flagship tool-agent-user benchmark has NO human-escalation action |
| τ²-bench: Dual-Control Environment | Barres, Dong, Ray, Si, Narasimhan, 2025 | arXiv:2506.07982 | User actively acts with tools in shared world (telecom domain modeled as Dec-POMDP); coordination/communication tested — but user is a task principal, not an escalation/containment resource |
| HAICOSYSTEM | Zhou et al., 2024 | arXiv:2409.16427 | Sandbox for safety risks in multi-turn human–AI interaction; interactional safety, not fault recovery |
| MIVAIS | 2026-09, arXiv | arXiv:2609.04983 | Study environment for multi-agent mixed-initiative visual analytics — mixed-initiative MAS exists as a label, but for sensemaking, not recovery |
| CALM: Configuration-Aware Human Intervention Boundaries During Robot Approach | 2026-09, arXiv (cs.HC) | arXiv:2609.07430 | Computes boundaries for when human intervention is appropriate — "intervention boundary" concept, robotics |
| Principles of Mixed-Initiative User Interfaces | Horvitz, 1999, CHI | DOI 10.1145/302979.303030 | Classical foundation: mixed-initiative interaction, cost of interruption |

## 4. Adjacent seed-threats found en route (flag to orchestrator)

These are outside my assigned lane but directly bear on the seed's survival:

### 4.1 OrchestraBench — the biggest threat seen in this sweep
- **"OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality"**, Y. Chen, Y. Gu, N. Vidra, S. Setty, S. Zheng, arXiv:2608.05263 (Aug 2026).
- Controlled, seed-reproducible **failure-injection harness** over templated enterprise workflows; introduces **"cascade radius"** and **per-failure-mode recovery** as primary metrics; compares routing policies with bootstrap CIs and paired tests; 26-case gold-labelled diagnostic; mechanism probes with a real Claude agent over a verifiable arithmetic dependency chain.
- This is essentially the seed's core measurement apparatus (blast radius ≈ "cascade radius", failure injection, recovery metrics) already published. Differentiators the seed could still claim: organizational boundary taxonomy (role/authority/memory/accountability/human), human escalation as a mechanism, richer org topologies vs templated enterprise workflows. Code availability not verified.

### 4.2 Other adjacent threats (all verified via arXiv abs pages)
| Paper | ID | One-line threat |
|---|---|---|
| Collective Loss of Control in LLM Agent Systems: An Epidemic Account of Mutation, Contagion, and Recovery (Wu et al.) | arXiv:2609.18460 | Epidemic model of failure propagation + containment/recovery in LLM MAS — occupies "propagation dynamics" framing |
| The Illusion of Independent Quorums: Epistemic Fault Domains and Correlated Cognitive Failures (He & Yu) | arXiv:2609.02925 | Formalizes correlated-failure "fault domains" in agent quorums — occupies redundancy-doesn't-imply-containment argument |
| Why LLM Agents Collapse Without Oversight: The Enforcement Gap (Wang) | arXiv:2609.15293 | Detection→action enforcement gap; closing it cuts attack success >4× — oversight mechanism with measured effect |
| Recoverability as a System Primitive for Long-Horizon AI Agents (Zhang & Liu) | arXiv:2609.13672 | Resume-vs-restart as explicit decision with evidence-bound contract; can "withhold automatic continuation" (≈escalation hook) |
| Do Not Restart: Residual Completion for Stateful Agent Handoffs (Deng et al.) | arXiv:2609.13800 | Commitment-constrained handoffs across models with authority/evidence contracts — occupies authority-transfer-during-recovery |
| CatchBench: When Can an Agent Failure Be Caught? (Zhao et al.) | arXiv:2608.22808 | Auditing at PRE/LIVE/POST information states, 72 entrants — occupies detection side of containment |
| The Agent Incident Registry (Kumar et al.) | arXiv:2609.11030 | 487 catalogued agent incidents 2022–2026, 24% realized harm — empirical grounding for blast-radius claims |
| Counter-Swarm Doctrine (Frank) | arXiv:2609.06140 | Containment of coordinated agent intrusions; "coordination episode" as unit of defence |
| TRACE: Human–AI Controller Coordination Under Drift and Failure (Zuniga et al.) | arXiv:2608.06657 | Multi-layer (human/AI/controller) benchmark, 1,918 drifted traces from ALFRED, failure propagation across layers incl. human layer |
| AIOpsLab (Chen, Shetty, …, Rajmohan, Microsoft) | arXiv:2501.06706 | Fault injection + agent evaluation across incident lifecycle ("AgentOps"); no human-escalation arm — the comparison the seed could add |
| Why Do Multi-Agent LLM Systems Fail? (MAST) (Cemri et al., NeurIPS 2025) | DOI 10.52202/085713-4082 (arXiv:2503.13657) | Failure taxonomy; full-text grep shows **no** human-in-the-loop/oversight/escalation content — recovery/escalation not covered |
| SHADE-Arena (Kutasov et al.) | arXiv:2506.15740 | Sabotage vs monitoring in LLM agents — monitoring-as-containment, adversarial |
| "Blast Radius" (Pitsane & Mogale) | arXiv:2608.07440 | **Term collision only**: token/memory management for agentic coding (reversible context eviction), unrelated to failure propagation. Also "credential blast radius" (arXiv:2609.04566) in security. The phrase "blast radius" is already used in agentic/security venues — seed should expect reviewers to know the term from reliability/security engineering. |

## 5. Classical foundations that predate LLMs (verified via Crossref)

| Paper | Venue/Year | ID | Concept it already owns |
|---|---|---|---|
| Scerri, Pynadath, Tambe, "Towards Adjustable Autonomy for the Real World" | JAIR 2002 | DOI 10.1613/jair.1037 | Transfer-of-control strategies: when agents escalate decisions to humans, with costs — **escalation-as-containment is 24 years old in MAS** |
| Scerri, Pynadath, Tambe, "Adjustable Autonomy in Real-World Multi-Agent Environments" | Autonomous Agents 2001 | DOI 10.1145/375735.376314 | Same lineage, conference version |
| Chalupsky et al., "Electric Elves: Agent Technology for Supporting Human Organizations" | 2002 | DOI 10.21236/ada459956 | Agent-supported human organizations, adjustable autonomy |
| Horvitz, "Principles of Mixed-Initiative User Interfaces" | CHI 1999 | DOI 10.1145/302979.303030 | Mixed-initiative interaction principles |
| Automated-driving takeover-request literature (e.g., Yang et al. 2023, DOI 10.3390/su15097270; Horáková et al. 2025, DOI 10.1186/s12544-025-00745-6) | 2010s–2025 | various | Human escalation with measured cost (takeover time, degraded performance) — mature HFI science of "when to hand control back to a human" |

## 6. Answers to the assigned questions

1. **Human-in-the-loop fault recovery:** Occupied in robotics (HRI 2026 confidence-aware recovery; XAI for robot failures 2021), in robot planning (KnowNo 2023), and now inside LLM MAS (arXiv:2609.02191 fault-point interventions, +40%/−6%).
2. **Escalation as containment:** Occupied classically (adjustable autonomy, JAIR 2002) and in LLM MAS machine-side (TAO tiered oversight absorbing 24% of agent errors; Agent-MD event-driven escalation). Human-side escalation in LLM MAS is measured only in 2609.02191 (medical conversations).
3. **Mixed-initiative recovery:** Mixed-initiative *interaction* is ancient (Horvitz 1999) and alive (CowPilot NAACL 2025; MIVAIS 2026), but mixed-initiative *fault recovery in agentic workflows* specifically was not found as a published frame — partial opening.
4. **Oversight-as-intervention with measured cost:** Occupied methodologically by AI Control (ICML 2024, audit-budget Pareto) and theoretically by Kadowaki 2026 (oversight capacity/solvency). Loopjacking (2609.21081) shows the oversight channel itself fails.
5. **Any 2025–2026 comparison of human escalation vs automated containment?** **Not found** in the org-fault-recovery setting. AI Control (2024) is the nearest comparison but adversarial/single-agent. OpenReview searches for "automated containment", "escalate to humans", "human versus automated recovery" returned nothing relevant; arXiv listing scans (Aug–Sep 2026, five categories) surfaced no such title. Residual risk: Semantic Scholar/arXiv-API/dblp were rate-limited, so coverage of non-arXiv venues (e.g., some IEEE/ACM 2026 venues) is incomplete.

## 7. Does anything here kill or subsume the seed?

- **Kill via E6 lane: NO.** No located paper studies human escalation vs automated containment for propagating organizational failures in LLM MAS, and none measures escalation's effect on a multi-boundary organizational blast radius.
- **But:** the human-agent boundary is the *least* novel dimension of the seed — deferral, escalation, oversight-cost, and HITL-approval-fragility are all occupied and must be cited/differentiated. Reviewers with MAS background will cite adjustable autonomy (2002); safety reviewers will cite AI Control (2024); HRI reviewers will cite KnowNo/HRI-2026.
- **Largest collateral threat:** OrchestraBench (arXiv:2608.05263) already operationalizes "cascade radius" + per-failure-mode recovery under failure injection in multi-agent orchestration. Combined with the epidemic model (2609.18460) and epistemic fault domains (2609.02925), the *propagation-measurement* core of the seed is also crowded. The seed's defensible residue: (a) explicit organizational boundary taxonomy incl. human escalation as one containment mechanism, (b) head-to-head containment-mechanism comparison (incl. human escalation vs automated) on blast radius vs task utility — exactly the comparison my sweep could not find.
