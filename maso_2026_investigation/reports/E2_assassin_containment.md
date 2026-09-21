# ASSASSIN E2 — Kill the Seed via Containment Synonyms

**Date:** 2026-09-21
**Mission:** Search fault isolation, agent quarantine, incident containment, rollback, revocation as containment, circuit breakers, bulkheads, containment policies — in agent systems and adjacent fields. Find any work that COMPARES containment/recovery interventions for agent failures. Report the single most damaging paper.
**Seed hypothesis under attack:** "Organizational failure propagation and recovery in LLM multi-agent systems" — what determines the "organizational blast radius" of a local fault across role/communication/authority/tool/memory/accountability/human boundaries, and which containment/recovery mechanisms minimize systemic impact while preserving task utility.

---

## BOTTOM LINE

**The seed is heavily damaged but not fully dead.** The generic core — "measure failure propagation / blast radius in tool-using LLM multi-agent systems and compare containment vs recovery mechanisms (circuit breaker, checkpoint rollback, isolation)" — is **already published prior art as of mid-2026**, including the exact term "blast radius" as a containment metric. The single most damaging paper is **"Containing the Cascade: A Benchmark and Reference Mediator for Failure Propagation in Tool-Using LLM Multi-Agent Systems" (IEEE ICERA 2026, DOI 10.1109/ICERA72709.2026.11666599)**, which does almost exactly the seed's core experiment (fault injection + containment metrics incl. blast radius + circuit-breaker-vs-rollback ablation) — albeit in a discrete-event *simulation*, in a low-tier venue, with 0 citations. A second, independent 2026 preprint (**DamageFlow/BlastGuard**, OpenReview) also claims "blast radius" measurement + minimization for agentic tool use, and **AIR (ICML 2026)** claims the "first incident response framework for LLM agent systems" with containment and recovery actions. What survives: (a) the explicitly **organizational** boundary taxonomy (authority/delegation, accountability, human-agent decision rights) — no found work frames propagation across *organizational* boundaries; (b) **real LLM MAS executions** rather than simulation; (c) organic-fault (non-adversarial) propagation in *real* multi-agent organizations. Note (a) partially collides with the already-occupied delegation-invariants proposal (maso/policy_preserving_delegation_research_proposal.md).

---

## 1. THE SINGLE MOST DAMAGING PAPER

### "Containing the Cascade: A Benchmark and Reference Mediator for Failure Propagation in Tool-Using LLM Multi-Agent Systems"

| Field | Value |
|---|---|
| Authors | Veera Ravindra Divi, Sneha Gullapalli, Balajee Asish Brahmandam |
| Venue | 2026 5th International Conference on Electronics Representation and Algorithm (ICERA), IEEE, pp. 604–609 |
| Date | Published 2026-07-01 |
| DOI | 10.1109/ICERA72709.2026.11666599 |
| URLs | https://doi.org/10.1109/ICERA72709.2026.11666599 ; Semantic Scholar paperId fbfed6b528e6808d77ec2e0c9261714ccdb24e81 |
| Verification | Crossref metadata (title/authors/pages/publisher IEEE) + Semantic Scholar abstract + Zenodo tombstone (OA copy deposited then **deleted 2026-07-22, removal reason "copyright"** — citation text in tombstone matches). 0 citations, 32 references. |
| Research problem | No standard, reproducible benchmark for measuring whether a tool-using LLM MAS can *contain* a failure cascade as it unfolds (vs diagnosing after the fact). |
| Method | (1) Taxonomy of six recurring cascading-failure modes; (2) **containment metrics: containment rate, cascade depth, BLAST RADIUS, mean time-to-detection**; (3) Cascade-Bench: controlled fault-injection testbed, 1080 scenarios × 6 task domains, on a **discrete-event simulation of agent message passing calibrated to reported MAS failure statistics**; (4) Sentinel: reference mediator combining typed inter-agent message contracts, semantic anomaly gate, **circuit breaker**, and **checkpoint-based recovery (rollback)**. |
| Experimental setting | 48 system configurations, >590,000 simulated task executions, scaling 3→12 agents. |
| Metrics | Task success, containment rate, cascade depth, blast radius, MTTD. |
| Major findings | Sentinel raises task success 31.3%→83.7% and containment 46.2%→99.4%; cascade depth held ~constant with scale (unguarded depth ~doubles). **Ablation cleanly separates fail-safe role (circuit breaker → containment) from fail-operational role (checkpoint rollback → task completion).** |
| Author-stated limitations | Simulation calibrated to reported statistics (implicitly: not real LLM executions). |
| My inferred limitations | (1) **Simulation-only** — no real LLM agents, no real API costs, calibration validity unproven; (2) low-tier venue (ICERA), authors with minimal track record (lead author's co-author has h-index 2, 13 papers); suspiciously clean numbers (99.4% containment); (3) deleted Zenodo copy hinders scrutiny; (4) no organizational dimensions (authority, accountability, human boundaries) — message-passing/tool layer only; (5) 0 citations to date. |
| Code availability | Claimed ("We release Cascade-Bench and Sentinel as an open baseline") but the Zenodo artifact is deleted; no live repository located. |
| Relationship to seed | **Near-direct overlap with the seed's core**: failure propagation in tool-using LLM MAS, blast radius as a metric, containment-vs-recovery mechanism comparison (circuit breaker vs checkpoint rollback), utility-preservation measurements. A reviewer aware of this paper would reject a "first to measure blast radius / compare containment mechanisms in LLM MAS" novelty claim. |

**Why this is the most damaging (not the others):** it is *published* (IEEE proceedings, July 2026), targets *organic* faults (hallucination, malformed tool call, role drift — not just adversarial attacks), uses the seed's exact "blast radius" language, and includes a controlled comparison/ablation of containment vs recovery interventions with task-utility measurements. DamageFlow is adversarial-framed and a preprint; AIR is single-agent; RoMa optimizes success rate not propagation containment.

---

## 2. TIER 1 — OTHER DIRECTLY DAMAGING WORKS (containment/recovery for agent failures, with comparison elements)

### 2.1 DamageFlow + BlastGuard — "What Can One Bad Tool Call Destroy? Measuring and Minimizing Blast Radius in Agentic Tool Use"

| Field | Value |
|---|---|
| Author | Muhammet Anil Yagiz (single author) |
| Venue/status | OpenReview preprint, ID MYvsxnxbCf, posted 2026-05-08 (no venue assignment visible) |
| URL | https://openreview.net/forum?id=MYvsxnxbCf |
| Problem | Binary attack-success labels hide radically different realized damage; agents should be evaluated by how far failure spreads. |
| Method | DamageFlow benchmark: sandboxed email, documents/RAG, repository, MCP-style registry environments; deterministic state-diff oracles scoring committed tool effects. **Blast Radius Score (BRS)** decomposes unauthorized tool effects by resource sensitivity, action impact, **propagation**, and **recovery cost**. BlastGuard runtime: least-privilege capability graphs compiled from trusted user intent, untrusted-context flow tracking, gating of state-changing calls via dry-run, policy checks, scoped tokens, **rollback logs**. |
| Setting | 80-scenario controlled pilot; attacks: indirect prompt injection, MCP tool poisoning, tool shadowing, **multi-agent relay attacks**. |
| Findings | Two agents with identical 20% attack-success differ by 89× in BRS; BlastGuard reduces committed unauthorized damage while retaining 87.5% benign task utility; counterfactual scoring reports prevented BRS. |
| Limitations | Small pilot (80 scenarios); adversarial-security frame, not organic faults; single-author preprint, unreviewed; organizational dimensions absent. |
| Relation to seed | Occupies "blast radius" terminology + propagation + recovery-cost metrics + containment runtime with utility-retention measurement. Multi-agent relay is one attack mode but not the organizational frame. |

### 2.2 AIR: Improving Agent Safety through Incident Response

| Field | Value |
|---|---|
| arXiv | 2602.11749 (v1 2026-02-12, v2 2026-06-20); **accepted at ICML 2026** |
| URL | https://arxiv.org/abs/2602.11749 |
| Problem | Safety mechanisms focus on prevention; limited capability to respond to, **contain, or recover from** incidents after they arise. Claims "the first incident response framework for LLM agent systems." |
| Method | DSL for the incident-response lifecycle integrated into the agent execution loop: (1) detect incidents via semantic checks grounded in environment state + recent context; (2) guide the agent to execute **containment and recovery actions via its tools**; (3) synthesize guardrail rules during eradication to block recurrence. |
| Setting | Three representative agent types; detection, remediation, eradication success all >90%; ablations of key components; timeliness and overhead measured; LLM-generated rules approach developer-authored rules. |
| Limitations | Single-agent systems (not MAS); no propagation/blast-radius measurement; no cross-agent organizational boundaries. |
| Relation to seed | Strong-venue (ICML 2026) occupation of "incident containment + recovery for agent failures" as a first-class mechanism. Kills any claim that containment/recovery-as-lifecycle for LLM agents is novel; leaves multi-agent organizational propagation open. |

---

## 3. TIER 2 — FAULT-TOLERANCE / RECOVERY FRAMEWORKS FOR LLM MAS (mechanism comparisons, weaker propagation focus)

| Paper | Venue / ID | Verified via | What it does | Containment/recovery comparison? | Relation to seed |
|---|---|---|---|---|---|
| **RoMa: A Credibility-Aware Fault-Tolerance Framework for LLM Multi-Agent Systems** (Kunyu Li, FengHe Wu) | CSCWD 2026, DOI 10.1109/cscwd68734.2026.11582680 | Crossref + Semantic Scholar abstract | Bayesian credibility evaluation + three strategies: redundant execution w/ credibility-weighted voting, primary-backup failover, **dynamic agent isolation with rehabilitation (= quarantine)**; POMDP formalization; adversarial fault injection during training; collaborative software debugging eval | Yes — three FT strategies compared against baselines on success rate / fault-detection accuracy; but metrics are task success, not propagation/blast radius | Occupies "agent quarantine/isolation + failover + redundancy" for LLM MAS. Damaging to quarantine-novelty; does not measure organizational spread |
| **FAIR-Swarm: Fault-Tolerant Multi-Agent LLM Systems for Scientific Hypothesis Discovery** (Roy & Roy) | AAAI LaMAS Workshop 2026 (Poster), OpenReview 6WyG2iZHes / FMKf4CZLiH | OpenReview API | Specialized roles + redundancy and consensus-based fault tolerance against hallucinated hypotheses and failure cascades | Redundancy+consensus vs baseline; poster-level detail | Niche domain; "failure cascades caused by unreliable agents" acknowledged as target |
| **FTDI: A Budget-Aware Self-Healing Framework for Resilient LLM Multi-Agent Code Generation** (Men, Tong, Zuo, Lu) | SSRN 2026, DOI 10.2139/ssrn.6387100 | Crossref abstract | Controlled fault-injection protocol (parameterized faults into Coder output, replayed injection manifests); Auditor (anomaly score, failure type, suspected span); budget-gated triggering; **tiered repair policy** (rule-based patch → deep repair → regeneration); distilled-immunity module | Yes — tiered recovery policies under budget constraints; code-generation MAS only | Occupies "budget-aware recovery loop + fault injection" for LLM MAS pipelines |
| **ALAS: A Stateful Multi-LLM Agent Framework for Disruption-Aware Planning** (Chang & Geng) | ACM Multi-LLM Agent Collaborative Intelligence 2025, DOI 10.1145/3749421.3749436 | Crossref + Semantic Scholar | Role-specialized agents with automatic state tracking; on disruption, **history-aware local compensation** avoiding global replanning and "containing cascade effects"; job-shop scheduling SOTA | Local compensation vs global replanning | "Containing cascade effects" via locality — a containment design principle, demonstrated in scheduling domain |
| **A Reliability Control Framework for Robust Multi-Agent LLM Systems (ARCF)** | Zenodo preprint 2026-05-07, DOI 10.5281/zenodo.20071517 | Zenodo API | Seven-layer framework; Reliability Control Layer detects failures and triggers automatic fault recovery; MAST-based monitoring; "formally verified fault-recovery protocols"; simulation evaluation | Claims recovery protocols; simulation-only; likely low quality | Weak occupation of "fault recovery layer for LLM MAS" |
| **Failure Modes in Production Multi-Agent LLM Systems: Lessons from Real Deployments** (Ahmed & Akbar) | SSRN 2026, DOI 10.2139/ssrn.7041478 | Crossref abstract | Five production failure classes (intent misclassification, context amnesia, cache poisoning, inference bottlenecks, cross-session state contamination) + mitigations applied in practice | Experience report; mitigations described not compared | Evidence that production MAS failures + containment mitigations are being documented industrially |

---

## 4. TIER 3 — MECHANISM-SPECIFIC PRIOR ART (each occupies one containment synonym)

| Synonym | Paper | ID / venue | Verified | What it occupies |
|---|---|---|---|---|
| **Rollback / checkpoint-restore** | ACRFence: Preventing Semantic Rollback Attacks in Agent Checkpoint-Restore | arXiv 2603.20625, CoDAIM workshop 2026 | arXiv abs page | Establishes that **checkpoint-restore is already a standard recovery feature of LLM agent frameworks**; identifies semantic rollback attacks (Action Replay, Authority Resurrection) and a mitigation (replay-or-fork semantics). Rollback-as-recovery is assumed infrastructure, not novel |
| Rollback (reasoning level) | Generator-Assistant Stepwise Rollback (GA-Rollback) (Li et al.) | ACL ARR 2025 submissions + CoRR 2025, OpenReview nberwaleXN / UciptDElgK | OpenReview API | Assistant triggers **rollback on incorrect actions** to stop "irreversible error propagation" in single-agent trajectories |
| Rollback auditability | What Can This Skill Safely Undo? Rollback-Oriented Auditability for Agent Skills (Peng & Li) | AgentSkills 2026 Poster, OpenReview zS5eRqW2QQ | OpenReview API | Recovery objects with persistence/recoverability/dependency/conflict properties for agent skills (position sketch) |
| Recovery strategy comparison | Did It Happen? Counterfactual Evaluation of LLM Agent Recovery from Ambiguous Tool Outcomes | Research Square 2026, DOI 10.21203/rs.3.rs-10730245/v1 | Publisher page | **Direct comparison of recovery interventions** (prompt advice vs status reconciliation vs stable idempotency contract) under ambiguous tool outcomes; exactly-once semantics; 81 templates, 756-pair main cell. Single-agent tool-call level |
| **Circuit breaker** | Beyond Content Filtering: A "Circuit Breaker" Architecture for Autonomous Agent Action Safety (Sridharan & Nair) | SoutheastCon 2026, DOI 10.1109/southeastcon63549.2026.11475929 | Crossref + Semantic Scholar | "Action Circuit Breaker" deterministic middleware gating each structured action against risk policy; prototype + simulation, theoretical latency/risk analysis |
| **Sandboxing / blast radius (security)** | ceLLMate: Sandboxing Browser AI Agents (Meng et al.) | arXiv 2512.12594 (Dec 2025) | arXiv abs page | Browser-level sandbox at HTTP layer; explicitly "reduces the **blast radius** of prompt injections"; WASP benchmark, 7.25–15% overhead |
| Fault injection / chaos | ReliabilityBench (Gupta et al.) | arXiv 2601.06112 (Jan 2026) | arXiv abs page | Chaos-engineering-style fault injection (timeouts, rate limits, partial responses, schema drift); reliability surface R(k,ε,λ); ReAct vs Reflexion, 1,280 episodes. Single-agent |
| Fault injection tooling (MAS) | Observability and Fault Injection for LLM-Based Multi-Agent Systems in SE (llmmas-otel) (Seyedghorban et al.) | arXiv 2608.24271; ICST 2026 DOI 10.1109/ICST69053.2026.00037 | arXiv abs page | OpenTelemetry tracing + targeted fault injection at interaction points for LLM MAS; compare baseline vs faulty executions. Tool paper — infrastructure for exactly the seed's experiments |
| Fault detection benchmark | AgentTelemetry (Balusu) | AIware 2026, DOI 10.1145/3805760.3814931 | Crossref + Semantic Scholar | 14 fault types × 9 span kinds; 490 fault-detection cells; detection rate focus, not containment |
| Guardrails / failure-first | MurphyGuard (Singh) | SSRN 2026, DOI 10.2139/ssrn.6262758 | Crossref abstract | Failure-mode enumeration, layered defense, **chaos engineering for agents**, adversarial validation; position/framework paper |
| Defense comparison (security) | Agent Security Bench (ASB) (Zhang et al.) | arXiv 2410.02644, **ICLR 2025** | arXiv abs page | 10 attacks + **11 defenses benchmarked** across 13 backbones; utility-vs-security metric. Single-agent adversarial |
| Cascade modeling (security) | Towards Unifying Quantitative Security Benchmarking for MAS — Agent Cascading Injection (Huang et al.) | arXiv 2507.21146 (Jul 2025) | arXiv abs page | Formalizes cascading compromise across inter-agent trust; "**Impact Chain and Blast Radius**" across agent networks; OWASP-aligned; methodology/position |
| Propagation measurement (security) | Beyond Binary Success: Propagation Profiles for LLM Agent Security Traces (AIPF) (Cheng & Zhu) | SSRN 2026, DOI 10.2139/ssrn.7035858 | Crossref abstract | Trace-level propagation levels L1–L3 on 180 AgentDojo traces; shows binary outcomes hide propagation depth |
| Cascade empirics (organic) | Behavioral Drift in Multi-Agent LLM Systems (Gagne) | SSRN 2026, DOI 10.2139/ssrn.6420858 | Crossref abstract | Empirical cascade propagation: one agent's collapse degrades peers (3-agent conversations, 200–500 turns); collapse is triggered, not spontaneous |
| Isolation / privilege (security) | IsolateGPT (2403.04960, 2024); Progent (2504.11703, 2025); AgentSpec (2503.18666, 2025); GuardAgent (2406.09187, 2024); SAGA (2504.21034, 2025); AgentArmor (2508.01249, 2025) | arXiv | DataCite title search (IDs verified) | Execution isolation, privilege control, runtime enforcement, guard agents — the security-side containment design space is crowded |
| Chaos engineering *by* agents | ChaosEater | arXiv 2501.11107 (2025) | DataCite | LLM agents performing chaos engineering on software systems — opposite direction (agents as fault injectors, not victims) |

---

## 5. TIER 4 — CLASSICAL PRIOR ART (pre-LLM; the concepts are old)

| Work | Venue / DOI | What it established |
|---|---|---|
| Hägg, "A sentinel approach to fault handling in multi-agent systems" | LNCS (Multi-Agent Systems Methodologies and Applications), 1997, DOI 10.1007/bfb0030090 | **Sentinel agents** that monitor and handle faults in MAS — 1997 |
| Klein, Rodriguez-Aguilar, Dellarocas, "Using Domain-Independent Exception Handling Services to Enable Robust Open Multi-Agent Systems: The Case of Agent Death" | JAAMAS 2003, DOI 10.1023/a:1024145408578 | Domain-independent **exception-handling services** for agent death in open MAS |
| Stanković, Štula, Maras, "Evaluating fault tolerance approaches in multi-agent systems" | JAAMAS 2015, DOI 10.1007/s10458-015-9320-6 | **Direct comparison of fault-tolerance approaches in MAS** (classical, pre-LLM; only 1 citation — the comparison was done and ignored) |
| Challenges in exception handling in MAS (2006, DOI 10.1145/1138063.1138072); Building MAS for Workflow Enactment and Exception Handling (2010, DOI 10.1007/978-3-642-14962-7_4) | workshop/LNCS | Exception handling as a MAS research subfield |
| Distributed-systems background (not individually re-verified — textbook-level): circuit breaker & bulkhead patterns (Nygard, *Release It!*), rollback recovery / checkpointing surveys (Elnozahy et al.), Byzantine fault tolerance (Castro & Liskov PBFT), recovery-oriented computing / microreboot / crash-only software (Candea, Fox, Patterson et al.), cell-based architectures & "blast radius" in cloud ops (AWS) | — | Every containment synonym in the assignment has decades of distributed-systems lineage; "blast radius" itself is imported from cloud/security ops |

---

## 6. SEARCH PROCESS & COVERAGE NOTES

- **APIs used:** Crossref (worked throughout), DataCite (indexes arXiv DOIs — used as arXiv full-text search), Semantic Scholar (rate-limited; spaced single queries), OpenReview API v2 (rate-limited; spaced), Zenodo API, arXiv abstract pages via fetch. DBLP was unreachable (Anubis bot protection); arXiv export API returned 429/empty from this network.
- **Synonym queries run (all with agent/LLM qualifiers):** fault isolation, quarantine, circuit breaker, rollback, checkpoint-restore, blast radius, bulkhead, fault containment, containment, incident response, kill switch/tripwire, Byzantine isolation, compromised-agent detection, exception handling, self-healing, graceful degradation, watchdog/supervisor, human escalation, hallucination cascade, error cascade, chaos engineering, fault injection, resilience, recovery comparison, organizational failure propagation.
- **Negative results worth recording:** "organizational failure propagation" + agent → **0 hits** (DataCite). "exception handling" + LLM agent → 0 hits. "bulkhead" + LLM agent → no relevant hits. "kill switch" + AI agent → only governance/Zenodo-slop hits. No work found that frames propagation across *organizational* boundaries (authority, accountability, human-agent decision rights) as such.
- **Noise note:** 2026 Zenodo/SSRN is flooded with low-quality and likely AI-generated "framework" papers; I recorded only items with verifiable metadata and on-topic abstracts, and flagged quality concerns per item.

---

## 7. DOES ANYTHING HERE KILL OR SUBSUME THE SEED?

**Partially kills (novelty of the core frame):**
1. "First to measure failure propagation / blast radius in LLM MAS" — **dead** (Containing the Cascade, ICERA 2026, published; DamageFlow, 2026 preprint; AIPF propagation profiles, 2026).
2. "First to compare containment vs recovery interventions for agent failures" — **dead** (Containing the Cascade's circuit-breaker-vs-checkpoint-rollback ablation; Did-It-Happen's recovery-strategy comparison; RoMa's isolation/failover/redundancy comparison; AIR's incident-response ablations; ASB's 11-defense benchmark on the security side).
3. "Agent quarantine/isolation as a novel mechanism" — **dead** (RoMa dynamic isolation + rehabilitation; classical sentinel/exception-handling lineage since 1997).
4. "Rollback/checkpoint recovery for agents is novel" — **dead** (standard framework feature per ACRFence; GA-Rollback; AgentSkills rollback auditability).

**Survives (differentiation the seed could still claim):**
1. **Organizational boundary taxonomy** — no found work studies propagation across role/authority/accountability/human-agent boundaries *as organizational structure*; all found works operate at message/tool/security layers. (Caution: authority/delegation partially collides with the existing delegation-invariants MASO proposal.)
2. **Real LLM MAS execution at scale** — Containing the Cascade is simulation-only; a real-execution organizational blast-radius study remains open (llmmas-otel and AgentTelemetry provide tooling but not the study).
3. **Organic (non-adversarial) faults in real multi-agent organizations with human-agent boundaries** — DamageFlow/ASB/AIPF are adversarial; AIR is single-agent; the organic-fault + organizational + real-execution intersection appears unoccupied as of 2026-09-21.

**Recommendation to orchestrator:** the seed must be reframed away from "blast radius / containment of cascades in tool-using LLM MAS" (occupied, incl. the exact term) toward the **organizational-structure determinants** of propagation (authority graphs, accountability assignment, human-agent escalation boundaries) with **real-execution** experiments — and must cite and differentiate from Containing the Cascade (ICERA 2026), DamageFlow/BlastGuard (2026), AIR (ICML 2026), and RoMa (CSCWD 2026) to survive review.
