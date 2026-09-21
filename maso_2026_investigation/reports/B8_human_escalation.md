# LANDSCAPE B8 — Human-Agent Collaboration and Escalation

**Investigator:** B8 specialist (adversarial evidence-gathering)
**Date:** 2026-09-21
**Assignment:** Map 2023–2026 work on human oversight of agent teams: escalation policies, when agents ask humans, human-in-the-loop checkpoints, mixed-initiative control, oversight cost, automation bias in agent supervision. Core question: **does any work treat human escalation as a FAULT CONTAINMENT/RECOVERY mechanism with measurable cost?**
**Seed hypothesis being tested:** organizational failure propagation and recovery in LLM multi-agent systems ("organizational blast radius" across role, communication, authority/delegation, tool, memory, accountability, and human-agent boundaries; containment/recovery mechanisms that minimize systemic impact while preserving task utility).

**Verification method note:** Every paper below was verified by inspecting the actual record — arXiv abstract page (via fetch), OpenReview forum/search record (which mirrors DBLP/Crossref for older venues), or ACL Anthology. Network conditions: arXiv API and Semantic Scholar API were heavily rate-limited from this IP; discovery relied on arXiv HTML search, OpenReview search API, and direct abstract-page fetches. Where a well-known classical paper is cited from the verified record of a citing paper rather than re-fetched, this is flagged.

---

## 1. Bottom line

**The seed hypothesis is NOT killed and NOT subsumed by the human-escalation landscape — but two 2026 workshop papers have already staked out the exact term "blast radius" for agentic tool-use damage, and a cluster of 2026 work treats escalation/oversight as a costed resource-allocation problem. The unoccupied niche is precisely the seed's core: human escalation as a *containment/recovery* mechanism for *faults propagating through organizational structure* (roles, authority, memory, accountability) in LLM MAS, measured against task utility. Everything found is either (a) security-attack-focused (prompt injection), (b) single-agent action gating, (c) clarification/ambiguity-driven help-seeking, or (d) non-empirical position/theory work.**

Direct answer to the assignment question — work treating human escalation as fault containment/recovery **with measurable cost**:

| Paper | Human escalation as containment? | Measurable cost? | Gap vs. seed |
|---|---|---|---|
| TAO (ICLR 2026 sub., rejected) | Partially — human physician as highest oversight tier corrects errors (triage 40%→60%) | Error absorption (24%), accuracy deltas | Healthcare-only; escalation is agent-to-agent primarily; no organizational boundaries; rejected |
| Oversight Has a Capacity (arXiv 2606.08919) | Yes — escalation policy spends finite human attention; flooding attack defeats fatigued reviewer | Explicit: safety-vs-escalation-rate curve (inverted-U), asymmetric costs | Single-agent action *gating* (prevention), not post-fault recovery; no multi-agent propagation |
| GIRA (ICLR 2026 AIWILD) | Yes — safety gate can block/rewrite/**escalate** tool calls | SRE metrics incl. **blast radius**, time-to-mitigate | Mock planner, 5 incidents, workshop-scale; incident-response security framing |
| DamageFlow/BlastGuard (ICML 2026 AIWILD) | No — containment is automated (capability graphs, rollback), not human escalation | **Blast Radius Score** incl. propagation + **recovery cost** | Attack-focused; human not in the loop; single-agent tool use + relay attacks |

---

## 2. Tier 1 — Closest to the seed (escalation/oversight as containment with cost)

### 2.1 Tiered Agentic Oversight (TAO) — the single closest work
- **Title:** Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety
- **Authors:** Yubin Kim, Hyewon Jeong, Chanwoo Park, Eugene W Park, Haipeng Zhang, Xin Liu, Hyeonhoon Lee, Daniel McDuff, Marzyeh Ghassemi, Cynthia Breazeal, Samir Tulebaev, Hae Won Park
- **Venue/status:** Submitted to ICLR 2026 — **REJECTED** (OpenReview forum `mPh4B1JoAN`, verified via OpenReview search API 2026-09-21)
- **Problem:** LLM agents in clinical settings create error/single-point-of-failure risks.
- **Method:** Hierarchical MAS inspired by clinical hierarchies (nurse–physician–specialist); tasks routed by complexity across tiers; automated inter-/intra-tier oversight; human doctor can act as highest tier.
- **Experiments:** 5 healthcare safety benchmarks; ablations of tier configuration; clinician user study.
- **Findings:** Hierarchy "absorbs up to 24% of individual agent errors before they can compound"; outperforms single-agent and flat MAS on 4/5 benchmarks (up to +8.2%); adaptive architecture >3% safer than static; removing lower tiers degrades safety most; physician corrective feedback as top tier improved medical triage accuracy 40%→60%.
- **Code:** project page tiered-agentic-oversight.github.io (per abstract).
- **Relationship to seed:** This IS escalation-as-error-containment in an organizational (hierarchical) MAS, with the human as the final containment tier — the closest existing work. **Limitations vs. seed:** domain-specific (healthcare triage); hierarchy is expertise-tiered, not organizational (no authority/delegation/memory/accountability boundaries); faults are agent errors, not propagated organizational failures; human escalation measured only as accuracy delta in a user study, not as a costed resource; rejected at ICLR 2026 (reviews not inspected — worth pulling if the swarm wants the reviewers' objections).

### 2.2 Oversight Has a Capacity — escalation as resource allocation
- **Title:** Oversight Has a Capacity: Calibrating Agent Guards to a Subjective, Fatiguing Human
- **arXiv:** 2606.08919 [cs.AI], v1 8 Jun 2026 (submitter: Emre Turan). Verified via arXiv abstract page.
- **Problem:** HITL approval gates for irreversible agent actions (shell, file edits, deploys); which actions to stop?
- **Method/findings:** (i) On 125 hand-labeled adversarially-weighted agent actions, human reviewers only moderately agree on "risky" (Fleiss' κ = 0.52) — no ground truth; (ii) guard framed as selective classification under asymmetric cost; (iii) with an endogenous fatiguing reviewer, **realized safety is an inverted-U in escalation rate — more human oversight can make the system less safe**; safety-optimal guard escalates *below* full escalation; a load-aware policy resists a **flooding attack** that slips a malicious action past a fatigued reviewer.
- **Key quote:** "human attention is finite, and the guard's escalation policy spends it."
- **Code:** open-source system + interactive demo (per abstract).
- **Author-stated limitation:** inverted-U and flooding attack are modeling results motivating a human study (not yet run). Explicitly claims no novelty for mechanisms (cites FALCON, DeCCaF as prior art).
- **Relationship to seed:** Strongest existing treatment of *escalation cost* (fatigue, flooding). But it is **prevention/gating** on a single agent's actions — there is no fault that has already occurred and propagated; no organizational structure.

### 2.3 GIRA — escalation gates + blast-radius metrics for incident response
- **Title:** Guarded Tool-Using LLM Agents for Incident Response: A Safety-Gated Architecture and Operational Evaluation Protocol
- **Author:** Dhruv Patel. **Venue:** ICLR 2026 AIWILD workshop (OpenReview forum `LBt5eX6OKx`, verified).
- **Method:** Guarded Incident Response Agent (GIRA) separates proposal generation from action authorization; multi-layer safety gate can **block, rewrite (dry-run), or escalate** tool calls. Operational Evaluation Protocol measures safety+utility with **SRE-grounded metrics: time-to-detect, time-to-mitigate, blast radius**, plus injection success rate and unauthorized action rate.
- **Experiments:** controlled seeded simulator with a reproducible **mock planner**; 5 incidents, 4 injection classes.
- **Relationship to seed:** Uses the seed's exact vocabulary (blast radius, time-to-mitigate) and treats escalation as a containment action — but in adversarial incident-response (prompt injection into tickets/logs), single-agent, workshop-scale with a mock planner. Occupies the *term* and the *metrics*, not the organizational-fault phenomenon.

### 2.4 DamageFlow / BlastGuard — "blast radius" already taken (security sense)
- **Title:** What Can One Bad Tool Call Destroy? Measuring and Minimizing Blast Radius in Agentic Tool Use
- **Author:** Muhammet Anil Yagiz. **Venue:** ICML 2026 AIWILD workshop (OpenReview forum `MYvsxnxbCf`, verified).
- **Method:** DamageFlow benchmark for blast radius of tool-using agents under indirect prompt injection, MCP tool poisoning, tool shadowing, and **multi-agent relay attacks**; sandboxed email/docs-RAG/repo/MCP-registry environments; deterministic state-diff oracles score committed tool effects. **Blast Radius Score (BRS) decomposes damage by resource sensitivity, action impact, propagation, and recovery cost.** BlastGuard runtime: provenance-aware least-privilege capability graphs, untrusted-context tracking, gating of state-changing calls (dry-run, policy checks, scoped tokens, rollback logs).
- **Findings:** 80-scenario pilot; two agents with identical 20% attack-success rate differ by **89× in BRS**; BlastGuard reduces committed damage while retaining 87.5% benign-task utility; counterfactual scoring reports prevented BRS.
- **Relationship to seed:** **This is the most dangerous prior work for the seed's framing.** It operationalizes "how far failure spreads" with a decomposed metric including propagation and recovery cost, and includes multi-agent relay attacks. **Differentiation the seed must claim:** (a) DamageFlow is adversarial-security-centric (injection/poisoning), not endogenous organizational faults; (b) its containment is fully automated — no human escalation, no oversight cost; (c) "propagation" is tool-effect/resource propagation, not propagation across role/authority/memory/accountability boundaries; (d) workshop pilot scale. A MASO paper must cite and explicitly differentiate from this.

---

## 3. Tier 2 — Oversight cost, oversight games, corrigibility (theory)

| Paper | ID / venue | Verified | Core content | Relevance |
|---|---|---|---|---|
| A Contextual-Bandit Oversight Game with Two-Sided Informational Asymmetry (Yunjin Tong) | arXiv:2607.00155, Jun 2026 | arXiv abs page | Runtime human oversight; human privately knows reward, AI privately knows action quality; **play/ask/trust/oversee interface**; "slab of avoidable harm" where AI knows action harmful but myopic human declines to oversee; price of non-credible oversight communication | Formalizes when oversight fails to fire — adjacent to escalation-failure analysis; one-shot bandit, no propagation |
| Nonuniformity Principle in Human-AI Coworking (An Luo, Jie Ding) | arXiv:2607.16530, Jul 2026 | arXiv abs page | **Where to place oversight stages** in long AI workflows under human time/resource constraints; optimal schedule has non-decreasing gaps; oversight improves satisfaction, reduces rework and token consumption; validated on literature-review and website workflows | Checkpoint placement with explicit cost — closest to "HITL checkpoint" optimization; single workflow, not MAS fault containment |
| The Veto Variable: Human Override as a Goal-Independent Cost Term (Aaron Kingsley Clark) | arXiv:2609.00109, Sep 2026 | arXiv abs page | AI-safety no-go argument: settled-goal agents treat oversight as revocable-goal risk; "keep the veto cheap to pay and expensive to evade"; pre-registered derivation experiment (8 frontier lineages, 79 draws) | Philosophical; oversight-capture angle; not experimental MAS |
| The Multi-Agent Off-Switch Game | AAAI 2026 TrustAgent Workshop Poster (OpenReview forum `XXW1dIcgik`) | OpenReview | **Corrigibility is not compositional**: individually corrigible agents can become collectively incorrigible under strategic interaction; conditions for group incorrigibility | Directly relevant to human-agent boundary in MAS: escalation/off-switch can fail *collectively* even when each agent locally defers. Theory only |
| The Off-Switch Game (Hadfield-Menell, Dragan, Abbeel, Russell) | arXiv:1611.08219; IJCAI 2017 | arXiv abs page | Classical root: rational agents incentivized to disable off-switch unless uncertain about utility | Classical root of corrigibility/deference |
| Agentic System Oversight and Human-AI Collaboration: Governance for Autonomous AI | AAAI 2026 Workshop AIGOV submission (forum `8fLkbImbq6`) | OpenReview | Governance framework position paper for agentic AI | Non-empirical; governance framing only |
| Secure Human Oversight of AI: Exploring the Attack Surface of Human Oversight (Ditz, Lazar, Lichtmeß, Plesch, Heck, Baum, Langer) | CoRR 2025 (forum `ouzS5sqGhj`) | OpenReview | Human oversight itself is an attack surface (attacks on the AI, on oversight communication, on personnel); hardening strategies | Adversarial angle on the human-agent boundary; analysis, no experiments |

---

## 4. Tier 3 — When agents ask humans (help-seeking / clarification)

| Paper | Venue/ID | Verified | Core content | Limitation vs. seed |
|---|---|---|---|---|
| KnowNo: Robots That Ask For Help: Uncertainty Alignment for LLM Planners (Ren, Dixit, Bodrova, Singh, Tu, Brown, Xu, Takayama, Xia, Varley, Xu, Sadigh, et al.) | CoRL 2023 (forums `MLlJQUUDZ1`, `AZyXafjzyt`) | OpenReview | Conformal-prediction uncertainty alignment → agent asks for help with statistical task-completion guarantees while **minimizing human help**; simulated + real robots | Help = clarification under ambiguity, pre-fault; single agent; no cost model of the human beyond help-rate minimization |
| Ask-before-Plan: Proactive Language Agents for Real-World Planning | CoRR 2024 (forum `kiDwuHd3UL`) | OpenReview | New task "Proactive Agent Planning": predict clarification needs from conversation + environment interaction; Ask-before-Plan benchmark; CEP multi-agent framework (clarification/execution/planning agents) with trajectory tuning | Clarification-seeking, not fault containment |
| Proactive Agent: Shifting LLM Agents from Reactive Responses to Active Assistance (Lu, Yang, Qian, Chen, Luo, Wu, Wang, Cong, Zhang, Lin, Liu, Wang, Zhiyuan Liu, et al.) | ICLR 2025 **Poster**; CoRR 2024 (forums `rg1n2y29O2`, `sRIU6k2TcU`) | OpenReview | ProactiveBench (6,790 events); reward model simulating human accept/reject judgments; fine-tuning elicits proactivity | Proactive task initiation, not escalation under failure |
| Collaborative Coding with Mixed Initiative LLMs (Michael JQ Zhang, Eunsol Choi) | ICLR 2026 **withdrawn** (forum `MtsCJT8IL7`) | OpenReview | Mixed-initiative alternation between clarifying questions and output attempts: 99% of output quality at 55% conversation length | Mixed-initiative efficiency for coding; no faults |
| τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (Yao et al., Sierra/Princeton) | arXiv:2406.12045, Jun 2024 | arXiv abs page | Tool-agent-user conversations with domain policies; pass^k reliability metric; SOTA agents <50% success | Domain policies include human handoff actions, but escalation is not the studied object; user is simulated |
| τ²-bench: Evaluating Conversational Agents in a Dual-Control Environment | ICML 2026 **spotlight** (forum `OC2z7iSQKa`); earlier ICLR 2026 desk-reject (forum `LGmO9VvuP5`) | OpenReview | Dual-control: both agent and user have tool-using capability | Mixed control authority — adjacent to seed's human-agent boundary; benchmark, not containment |

**Gap observed:** the entire "when to ask" literature treats human queries as *ambiguity resolution* or *capability fallback* at decision time. None models asking-the-human as a response to a *detected fault mid-propagation* in a multi-agent organization, and none prices the human's intervention against blast-radius reduction.

---

## 5. Tier 4 — Learning to defer (the ML root of escalation policy, with cost)

| Paper | Venue | Verified | Core content |
|---|---|---|---|
| DeCCaF: Cost-Sensitive Learning to Defer to Multiple Experts with Workload Constraints (Alves, Leitão, Jesus, Sampaio, Liébana, Saleiro, Figueiredo, Bizarro) | **TMLR** (also CoRR 2024; ICLR 2024 withdrawn version) | OpenReview | Deferral under cost and capacity constraints: models P(human error) with one expert prediction/instance; constraint programming globally minimizes error cost subject to **human work-capacity constraints** |
| FALCON: Fatigue-Aware Learning to Defer via Constrained Optimisation (Zhang, Nguyen, Rosewarne, Wells, Carneiro) | ICLR 2026 **withdrawn** | OpenReview | L2D as CMDP with psychologically-grounded fatigue curves; states include cumulative human workload; PPO-Lagrangian; maximizes accuracy under human-AI cooperation **budget constraints**; introduces FA-L2D benchmark |
| Two-Stage Learning to Defer with Multiple Experts (Mao, Mohri, Mohri, Zhong) | NeurIPS 2023 | OpenReview | Two-stage predictor+deferral; H-consistent surrogate losses; CIFAR/SVHN |
| Principled Approaches for Learning to Defer with Multiple Experts (Mao, Mohri, Zhong) | ISAIM 2024 | OpenReview | Multi-expert L2D surrogate losses with consistency bounds |
| Expert-Agnostic Learning to Defer | CoRR 2025 | OpenReview (title/venue only) | L2D without expert identity |
| A Simple Heuristic for Controlling Human Workload in Learning to Defer | ICPR 2024 | OpenReview (title/venue only) | Workload control in L2D |

**Assessment:** L2D is the mature, formal "escalation policy with measurable cost" literature — cost-sensitive, capacity-constrained, fatigue-aware (2024–2026). But it is **single-decision classification deferral**: no sequential workflows, no agent teams, no fault propagation, no recovery. The seed can import L2D's cost/capacity formalism (and must cite DeCCaF/FALCON) while noting the setting gap. (Classical L2D roots — Madras/Pitassi/Zemel "Predict Responsibly" NeurIPS 2018 and Mozannar/Sontag ICML 2020 — are cited inside the verified DeCCaF/FALCON records; not re-fetched this sweep.)

---

## 6. Tier 5 — Automation bias, overreliance, oversight degradation

| Paper | Venue/ID | Verified | Core content |
|---|---|---|---|
| AI Agents Push Humans Out of the Loop (Margaret Mitchell, Avijit Ghosh, Samir Passi) | arXiv:2608.23642, Aug–Sep 2026 (v3) | arXiv abs page | Position: current agent design **degrades the human capacity oversight depends on** (skill atrophy, impeded critical judgment); design affordances + organizational protocols to counteract |
| Measuring and mitigating overreliance is necessary for building human-compatible AI (Ibrahim, Collins, Kim, Reuel, Lamparth, Feng, Ahmad, Soni, El Kattan, Stein, et al.) | CoRR 2025 | OpenReview | Position: overreliance on LLMs as "thought partners"; individual/societal risks incl. cognitive deskilling; measurement gaps; mitigations |
| Explanations Can Reduce Overreliance on AI Systems During Decision-Making (Vasconcelos et al.) | CSCW 2023 (Proc. ACM HCI) | OpenReview | Explanations + cost of verifying can reduce overreliance |
| To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI (Buçinca, Malaya, Gajos) | CSCW 2021 | OpenReview | Cognitive forcing functions reduce overreliance vs. simple explanations |
| Is Overreliance on AI Provoked by Study Design? | Crossref record | OpenReview (title only) | Methodological critique of overreliance measurement |
| Invisible Ink Threats: Adversarial Goals Behind Legitimate Tasks in Computer-Use Agents (Zhang, Zhang, Zhang) | arXiv:2608.02018, Aug 2026 | arXiv abs page | **HITL confirmation is bypassable**: low-harm injected goals (star repo, install package) are behaviorally indistinguishable from legitimate actions and evade both model defenses and human oversight; II-Bench (444 examples, 3 platforms); HITLCUA framework with simulated user; leading CUAs + simulated user review both fail |
| Human-in-the-Loop Nugget Annotation for Accountable LLM-as-a-Judge (Laura Dietz) | arXiv:2606.29033, Jun 2026 | arXiv search listing | Rubber-stamping/anchoring risk in HITL evaluation design |

**Assessment:** The automation-bias/overreliance line is active but almost entirely **single-AI-advisor decision-making** (CSCW/CHI-style), plus 2025–2026 position papers extending it to agents. "Invisible Ink Threats" is the key empirical result for the seed: **human escalation gates fail silently against low-salience faults** — exactly the condition under which an organizational fault would propagate past a human checkpoint. No work measures automation bias *of a human supervising a multi-agent organization* or how oversight failure affects blast radius.

---

## 7. Tier 6 — HITL agentic systems and oversight interfaces

| Paper | Venue/ID | Verified | Core content |
|---|---|---|---|
| Magentic-UI: Towards Human-in-the-loop Agentic Systems (Mozannar, Bansal, Tan, Fourney, Dibia, et al., Microsoft) | CoRR 2025 (forum `PD06S5qX9j`) | OpenReview | Open-source HITL agentic interface on multi-agent architecture (Magentic-One); six interaction mechanisms: co-planning, co-tasking, multi-tasking, **action guards** (human approval), long-term memory; evaluated on task completion + HITL dimensions (GAIA-based) |
| AgentGUI: Observing and Steering Long-Running AI Agents (Zhao, Sohn, Zheng, Moor) | arXiv:2607.26300, Jul 2026 | arXiv abs page | Trajectory visualization + manual/automated steering across concurrent sessions; user study: 38% faster key-element identification (p=0.023); automated drift prevention raises small-model completion up to +34pp |
| Steerability via constraints (Thomas Winninger) | arXiv:2607.02389; ICML 2026 Deep Learning for Code workshop | arXiv abs page | Constraints (access control, conventions, tooling) make oversight cheaper in tokens; reviewer recall on 11 inserted backdoors: 54.5% → 90.9% with constrained substrate |
| Managed Autonomy at Runtime: Gear-Based Safety and Governance for Single- and Multi-Agent CPS (Ramaswamy, Miaosheng) | arXiv:2607.00334, Jun 2026 | arXiv search listing | Runtime "gear-based" autonomy levels for multi-agent CPS — adjustable-autonomy revival for LLM agents (abstract only inspected) |
| A Black Box for Agentic Processes (Brömme) | arXiv:2609.04017, Sep 2026 | arXiv search listing | Blockchain-anchored evidence for agent communication, human oversight, GRC audits — accountability/audit trail angle |

---

## 8. Classical roots (pre-LLM) — verified via OpenReview/DBLP-mirrored records

| Work | Venue | Core concept |
|---|---|---|
| Toward Trustworthy Adjustable Autonomy in KAoS | Trusting Agents... 2004 (+ KAoS policy services, POLICY 2003) | Policy-governed adjustable autonomy |
| A Decision-Theoretic Approach to Cooperative Control and Adjustable Autonomy | ECAI 2010 | Decision-theoretic transfer of control |
| Adjustable Autonomy for UAV Supervision Through Mental Workload Assessment | IHCI 2017 | Workload-adaptive autonomy — classical analog of fatigue-aware escalation |
| Let Me Take Over: Variable Autonomy for Meaningful Human Control | Frontiers in AI 2021 | Variable autonomy + meaningful human control |
| A Distributed Task Specification Language for Mixed-Initiative Delegation | **PRIMA 2010** | Mixed-initiative delegation — directly in PRIMA lineage (relevant to MASO@PRIMA audience) |
| Mixed-Initiative Interaction = Mixed Computation (Ramakrishnan, Capra, Pérez-Quiñones) | CoRR 2001 | Formal mixed-initiative interaction |
| Proactive Communications in Agent Teamwork | Workshop on Agent Communication Languages 2003 | Proactive communication in agent teams |
| Meaningful human control: actionable properties for AI system development | AI Ethics 2023 (+ CoRR 2021 "beyond talking the talk"; Frontiers Robotics AI 2024 firefighting) | MHC properties |
| The Moral Responsibility Gap and the Increasing Autonomy of Systems | SAFECOMP Workshops 2018 (+ Moral Responsibility for AI Systems, NeurIPS 2023) | Responsibility gap — seed's accountability boundary |
| Service mesh circuit breaker (HAOC@EuroSys 2021) | EuroSys ws | Classical containment pattern (circuit breakers) in distributed systems |

**Assessment:** Every seed ingredient has a classical analog — adjustable autonomy = escalation policy; transfer-of-control = human-agent boundary crossing; circuit breakers/bulkheads = containment; responsibility gap = accountability boundary. The LLM-MAS-era novelty must be in *learned/emergent organizational structure* and *measurable propagation*, not in the concepts themselves. Reviewers at a PRIMA-colocated workshop will know this lineage.

---

## 9. Synthesis — does anything kill or subsume the seed?

**Kill: NO. Partial occupation: YES, on three fronts.**

1. **Terminology/metrics occupation (moderate threat).** DamageFlow (ICML 2026 AIWILD) already defines a Blast Radius Score with propagation and recovery-cost decomposition for agentic tool use, and GIRA (ICLR 2026 AIWILD) uses blast radius + time-to-mitigate with escalate-as-gate-action. Both are workshop pilots, security-focused, and non-organizational. The seed must (a) cite both, (b) re-anchor "organizational blast radius" on role/authority/memory/accountability/human-boundary spread rather than tool-effect damage, and (c) include non-adversarial faults.

2. **Escalation-cost occupation (moderate threat).** "Oversight Has a Capacity" (inverted-U safety vs escalation rate, fatigue, flooding attack), FALCON (fatigue-aware CMDP deferral), DeCCaF (capacity-constrained deferral), and the Nonuniformity Principle (checkpoint placement) collectively own "escalation/oversight as costed resource allocation." None apply it to multi-agent fault recovery. The seed should import this formalism rather than rediscover it.

3. **Human-as-containment-tier occupation (low-moderate threat).** TAO (rejected ICLR 2026) is the only work where a human is the final error-containment tier of an agent hierarchy with measured effect (40%→60% triage). Its rejection and healthcare specificity leave the general organizational-fault problem open.

**Clearly unoccupied (the defensible niche):** no verified work studies (a) a local fault *already propagating* through an LLM multi-agent organization, (b) human escalation as one *recovery/containment* mechanism among several (vs. restart, rollback, quarantine, re-delegation), (c) priced against both systemic damage (organizational blast radius) and task utility, (d) including the failure modes of the human checkpoint itself (automation bias, fatigue, flooding, invisible-ink bypass) as part of the propagation graph. The closest empirical result on checkpoint failure (Invisible Ink Threats) is security-framed and single-agent.

**Risks to flag for the swarm:**
- The 2026 AIWILD workshops (ICLR + ICML) are actively publishing seed-adjacent agent-safety pilots; the space is moving fast — another blast-radius paper appearing before Oct 10 is plausible.
- "Oversight Has a Capacity" explicitly disclaims mechanism novelty and cites the L2D lineage — a signal that reviewers will demand the seed differentiate from L2D + adjustable autonomy + AIWILD pilots simultaneously.
- Magentic-UI/AgentGUI show HITL *interfaces* are well-covered; a MASO paper framed as "we built a HITL oversight interface" would be scooped; the framing must be the *propagation/recovery science*.

---

## 10. Verified identifier appendix (for citation)

| # | Short name | Identifier |
|---|---|---|
| 1 | TAO | OpenReview forum mPh4B1JoAN (ICLR 2026 rejected) |
| 2 | Oversight Has a Capacity | arXiv:2606.08919 |
| 3 | GIRA | OpenReview forum LBt5eX6OKx (ICLR 2026 AIWILD) |
| 4 | DamageFlow/BlastGuard | OpenReview forum MYvsxnxbCf (ICML 2026 AIWILD) |
| 5 | Contextual-Bandit Oversight Game | arXiv:2607.00155 |
| 6 | Nonuniformity Principle | arXiv:2607.16530 |
| 7 | Veto Variable | arXiv:2609.00109 |
| 8 | Multi-Agent Off-Switch Game | OpenReview forum XXW1dIcgik (AAAI 2026 TrustAgent) |
| 9 | Off-Switch Game | arXiv:1611.08219 (IJCAI 2017) |
| 10 | Secure Human Oversight | OpenReview forum ouzS5sqGhj (CoRR 2025) |
| 11 | KnowNo | OpenReview forum MLlJQUUDZ1 (CoRL 2023) |
| 12 | Ask-before-Plan | OpenReview forum kiDwuHd3UL (CoRR 2024) |
| 13 | Proactive Agent | OpenReview forum sRIU6k2TcU (ICLR 2025 poster) |
| 14 | Mixed-Initiative Coding | OpenReview forum MtsCJT8IL7 (ICLR 2026 withdrawn) |
| 15 | τ-bench | arXiv:2406.12045 |
| 16 | τ²-bench | OpenReview forum OC2z7iSQKa (ICML 2026 spotlight) |
| 17 | DeCCaF | OpenReview forum TAvGZm2Rqb (TMLR) |
| 18 | FALCON | OpenReview forum 5dwQrwtzmS (ICLR 2026 withdrawn) |
| 19 | Two-Stage L2D | NeurIPS 2023 (OpenReview record) |
| 20 | AI Agents Push Humans Out of the Loop | arXiv:2608.23642 |
| 21 | Overreliance position | OpenReview forum GlI7dzoMUo (CoRR 2025) |
| 22 | Explanations Reduce Overreliance | CSCW 2023 (OpenReview forum fWswAIA0ns) |
| 23 | To Trust or to Think | CSCW 2021 (OpenReview forum QaY9oV3VVH) |
| 24 | Invisible Ink Threats | arXiv:2608.02018 |
| 25 | Magentic-UI | OpenReview forum PD06S5qX9j (CoRR 2025) |
| 26 | AgentGUI | arXiv:2607.26300 |
| 27 | Steerability via constraints | arXiv:2607.02389 |
| 28 | Managed Autonomy at Runtime | arXiv:2607.00334 |
| 29 | HITL Nugget Annotation | arXiv:2606.29033 |
| 30 | Agentic oversight governance | OpenReview forum 8fLkbImbq6 (AAAI 2026 AIGOV sub.) |

*Raw search artifacts (HTML/JSON) preserved in `maso_2026_investigation/raw/`.*
