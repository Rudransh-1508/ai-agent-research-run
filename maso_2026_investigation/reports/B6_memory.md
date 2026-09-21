# LANDSCAPE B6 — Agent Memory and Shared Memory

**Investigator:** B6 specialist (adversarial evidence-gathering)
**Date:** 2026-09-21
**Mission:** Map Collaborative Memory, Governed Shared Memory/MemClaw, memory poisoning, memory provenance, memory contamination/rollback, and long-term memory architectures for MAS. Core questions: (Q1) Does any work measure or contain fault propagation THROUGH shared memory? (Q2) Is memory contamination recovery studied?

**Verification method:** Every paper below was verified by inspecting the actual arXiv abstract page (arxiv.org/abs/...), the arXiv HTML full text, the OpenReview API record, or the Crossref record — never search snippets. Two initially recalled arXiv IDs turned out to be wrong on inspection (a vision paper and a physics paper); the correct IDs below come from verified reference lists. dblp.org was unreachable from this network; Semantic Scholar API was rate-limited throughout; arXiv API was rate-limited after the first few calls, so most verification used arxiv.org/abs pages and the OpenReview search API.

---

## BOTTOM LINE

**Q1 (fault propagation through shared memory): NO work measures or contains fault propagation through shared multi-agent memory as an organizational phenomenon.** The closest works are: MemClaw (governance failure modes of shared memory, but no fault injection, no blast-radius measurement, no recovery); DamageFlow/BlastGuard (measures "blast radius" of tool-using agents including multi-agent relay attacks, but the channel is tool calls under prompt injection, not shared memory); MINJA (single-agent memory injection; multi-agent propagation explicitly deferred to future work). **The specific gap — fault injection into one agent's memory write, measurement of cross-agent/cross-role spread via shared memory, and containment/recovery — is unoccupied.**

**Q2 (memory contamination recovery): PARTIALLY studied, single-agent only.** FamilyRepair (OpenReview, 2026) studies rollback families for corrupted self-evolving agent memory with replay verification — the only direct "memory contamination recovery" work found, and it is single-agent, pre-publication. GATEMEM benchmarks active forgetting after deletion requests in multi-principal shared memory (governance, not fault recovery). MINJA and the systematic MPBench study evaluate defenses against poisoning and find them insufficient, but do not study post-compromise recovery. **No work studies recovery of a shared multi-agent memory substrate after contamination, nor quantifies what fraction of a fleet's behavior was affected (blast radius) before/after rollback.**

**Terminology alert:** the phrase "blast radius" is already in use for agentic tool-use damage (DamageFlow, OpenReview MYvsxnxbCf, 2026). A MASO paper on "organizational blast radius" must differentiate from that work explicitly.

---

## 1. Assigned anchor papers

### 1.1 Collaborative Memory (assigned anchor)

| Field | Value |
|---|---|
| Title | Collaborative Memory: Multi-User Memory Sharing in LLM Agents with Dynamic Access Control |
| Authors | Alireza Rezazadeh, Zichao Li, Ange Lou, Yuying Zhao, Wei Wei, Yujia Bao (Accenture Center for Advanced AI) |
| Year/venue | 2025-05-23, arXiv preprint (cs.MA) |
| ID/URL | arXiv:2505.18279, https://arxiv.org/abs/2505.18279 |
| Problem | Multi-user, multi-agent memory sharing under asymmetric, time-evolving permissions |
| Method | Bipartite user–agent–resource access graphs; two-tier memory (private + shared fragments); immutable provenance attributes (contributing agents, accessed resources, timestamps) on every fragment; granular read policies projecting fragments into filtered views; write policies with context-aware transformations; provable policy adherence and auditability |
| Experimental setting | Three progressively complex scenarios (incl. logistical/supply-chain), simulated multi-user environments, grant/revoke permission dynamics over time steps t1–t8 |
| Metrics | Accuracy vs ground truth, agent utilization, resource utilization (call counts) |
| Major findings | Lower resource utilization than single-user baselines while maintaining privacy compliance under dynamic grant/revoke |
| Author-stated limitations | Synthetic/simulated multi-user data; moderate scale; LLM probabilistic policy breaches possible; no production latency analysis |
| Inferred limitations | **No adversarial or fault model at all** — full-text grep finds zero occurrences of poison/contaminat/rollback/recover/fault/propagat/attack. Access control prevents unauthorized reads but says nothing about what happens when an authorized write is wrong or malicious, or how a bad fragment's influence is measured or undone |
| Code | Not stated on abstract page |
| Relation to seed | Provides provenance machinery (immutable fragment provenance, retrospective permission checks) that a blast-radius study would need, but occupies the access-control/governance corner, not fault propagation or recovery |

### 1.2 Governed Shared Memory / MemClaw (assigned anchor)

| Field | Value |
|---|---|
| Title | Governed Shared Memory for Multi-Agent LLM Systems |
| Authors | Nurit Cohen-Inger (Ben-Gurion University), Erni Avram (Caura.ai), Ran Taig (Caura.ai), Oded Margalit (BGU) |
| Year/venue | 2026-06-23, arXiv preprint (cs.AI) |
| ID/URL | arXiv:2606.24535, https://arxiv.org/abs/2606.24535 |
| Problem | Formalizes the "fleet-memory problem": shared memory for fleets of cooperating agents as a governed distributed-systems problem |
| Method | Four failure modes defined: **unauthorized leakage, stale propagation, contradiction persistence, provenance collapse**. Primitives: scoped retrieval, temporal supersession, provenance tracking, policy-governed propagation. Implemented in MemClaw (production multi-tenant memory service); evaluated with ArgusFleet harness (one experiment per failure mode against the live REST API) |
| Experimental setting | Live production service, single tenant, 200 trials/experiment, 9696 GET-by-id re-probes, 50 depth-four provenance chains, committed JSONL traces |
| Metrics | Leak rate (Wilson CI), stale-read rate, provenance reconstruction accuracy/latency, write-to-visible latency, contradiction supersession rate |
| Major findings | Provenance: 50/50 depth-4 chains reconstructed, p50 ≈291 ms/hop. Propagation: 117/120 intra-fleet visibility, 0/80 cross-fleet leakage; strong-write-mode write-to-visible p50 ≈0.8 s. Found real bugs: sub-tenant scope bypassed on direct GET-by-id (disclosed + remediated); synchronous near-duplicate dedup gate starves the asynchronous contradiction detector (pipeline-ordering conflict) |
| Author-stated limitations | Self-evaluation (same group built MemClaw and ArgusFleet); single tenant (cross-tenant untested); no baseline comparison; 200-trial scale; staleness-after-supersession only partially measured |
| Inferred limitations | **Failure modes are consistency/governance failures, not injected faults.** No adversarial writer, no measurement of how far a wrong/contradictory memory spreads into downstream agent behavior (no task-utility impact measurement), no recovery/rollback mechanism beyond supersession. "Stale propagation" here means update-visibility lag, not error spread |
| Code | ArgusFleet harness described as open/reproducible (committed traces) |
| Relation to seed | **Closest systems work to the seed hypothesis.** It occupies "shared-memory governance + provenance + failure-mode taxonomy" territory. A MASO paper must cite it as the governance baseline and differentiate: blast radius = task-utility impact of an injected fault as it propagates through shared memory to other agents/roles, plus containment/recovery — none of which MemClaw studies |

### 1.3 AIM (adjacent, found during sweep)

| Field | Value |
|---|---|
| Title | AIM: A Privacy-Aware Interoperable Memory Framework for Multi-Agent Multi-User LLM Systems |
| Authors | Zachary Johnson, Nigel Boachie Kumankumah, Somya Chatterjee, Tejas Sathyamurthi, Min Chen, Xinyi Alice Li, Xiao Wang, Emily Morgan Gelchie, Jessica Lin, Sadid A. Hasan, Sulaiman Vesal |
| Year/venue | 2026-09-11, arXiv preprint (cs.AI) |
| ID/URL | arXiv:2609.12320, https://arxiv.org/abs/2609.12320 |
| Problem | Private vs public memory classification and index-level access control in multi-agent multi-user systems |
| Method | Dynamic private/public classification; index-level access control; introduces MUMBench (first multi-user memory benchmark covering retrieval/creation/update/deletion across four domains) |
| Metrics | 96.0% visibility classification accuracy, 58.8% strict operation accuracy, 70.5% state-aware operation accuracy (3 runs) |
| Relation to seed | Governance/access-control corner; no fault or recovery study. MUMBench could serve as substrate for contamination experiments |

---

## 2. Memory poisoning attacks (fault injection into memory — the attack side exists)

| Paper | ID / venue | Verified | Threat model | Multi-agent? | Recovery studied? |
|---|---|---|---|---|---|
| AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases (Zhaorun Chen et al.) | arXiv:2407.12784, Jul 2024 | arXiv abs page | Backdoor triggers optimized to map to unique embedding region; poisons long-term memory or RAG KB; no training needed | No (driving/QA/EHR agents) | No |
| MINJA: Memory Injection Attacks on LLM Agents via Query-Only Interaction (Shen Dong, Shaochen Xu, Pengfei He, Yige Li, Jiliang Tang, Tianming Liu, Hui Liu, Zhen Xiang) | arXiv:2503.03704, Mar 2025 (v5 Feb 2026) | arXiv abs + HTML full text | Query-only injection of malicious records with bridging steps + progressive shortening; no direct memory write access | **Explicitly deferred**: "MINJA can be potentially extended to multi-agent systems where the memory injection for one agent can affect the operation of other agents through inter-agent communication" (Appendix O) | Defenses evaluated (adversarial training, embedding sanitization, prompt detection, isolation/rate-limit/temporal decay) — all circumventable; no post-hoc recovery |
| PoisonedRAG: Knowledge Corruption Attacks to RAG (Wei Zou et al.) | arXiv:2402.07867, USENIX Security 2025 | arXiv abs page | Inject ≤5 malicious texts per target question into KB; 90% ASR; existing defenses insufficient | No | No (defenses found insufficient) |
| MEXTRA: Unveiling Privacy Risks in LLM Agent Memory (Bo Wang et al.) | arXiv:2502.13172, ACL 2025 Main | arXiv abs page | Black-box memory extraction attack (privacy, not poisoning) | No | No |
| From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents (Pritam Dash, Tongyu Ge, Aditi Jain, Tanmay Shah, Zhiwei Shang) | OpenReview 5cgg9yenCZ, 2026 | OpenReview API record | 4 memory write channels, 9 structural vulnerabilities, taxonomy of 6 poisoning attack classes; MPBench benchmark | Not stated (agent systems generally) | No — key finding: "agents designed to write and retrieve memory more aggressively are more exploitable"; prompt-injection defenses fail to cover memory poisoning |
| Hidden in Memory: Sleeper Memory Poisoning in LLM Agents (Sidharth Pulipaka, Stanislau Hlebik, Leonidas Raghav, Sahar Abdelnabi, Vyas Raina, Ivaxi Sheth, Mario Fritz) | OpenReview gdMNGQRTuS, 2026 | OpenReview API record | Delayed/dormant poisoning via manipulated external content; fabricated memories persist across sessions; 99.8% write success (GPT-5.5), 60–89% attacker-intended agentic actions among successful injections | No (single assistant, cross-session) | No |
| Poison Once, Exploit Forever: Environment-Injected Memory Poisoning (eTAMP) (Mingwen Dong, Wei Zou, Miguel Romero Calvo, Shuaichen Chang, Jiang Guo, Dongkyu Lee, Xing Niu, Xiaofei Ma, Yanjun Qi, Jiarong Jiang) | OpenReview sfUpgUKF2Y, 2026 | OpenReview API record | Contamination via environmental observation alone (no direct memory access); cross-session, cross-site activation; bypasses permission-based defenses; ASR up to 32.5% (GPT-5-mini) on (Visual)WebArena; "Frustration Exploitation" (ASR up to 9× under environmental stress) | Cross-site but single-agent | No |
| Watch Out for Your Agents! Investigating Backdoor Threats to LLM-Based Agents (Wenkai Yang et al.) | arXiv:2402.11208, NeurIPS 2024 | arXiv abs page | Agent backdoors via query or intermediate observation triggers; textual backdoor defenses fail | No | No |
| Episodic memory in AI agents poses risks that should be studied and mitigated (Chad DeChant) | arXiv:2501.11739, SaTML 2025 | arXiv abs page | Position paper: risks of episodic memory + 4 design principles | — | Calls for study; no mechanism |
| Environmental poisoning attack on raw agentic memory in web environments | OpenReview LohuI05ArW, 2026 | OpenReview search record (title only; abstract not exposed) | Title indicates environment-driven poisoning of raw agentic memory | Unknown | Unknown |

**Assessment:** the attack literature is rich and growing fast (2024→2026), but it is overwhelmingly **single-agent**. The two 2026 systematic works (MPBench study, eTAMP) establish that memory is a persistent, cross-session attack surface and that existing defenses fail. None measures how a poisoned memory spreads across an agent organization or how to recover the shared substrate.

---

## 3. Recovery, rollback, and contamination repair (the thin edge)

| Paper | ID / venue | Verified | What it does | Gap vs seed |
|---|---|---|---|---|
| Repair Sets Before Repair Choices: Identifiable Rollback Families for Self-Evolving Agent Memory (FamilyRepair) | OpenReview IJoWb6T3RJ, 2026 (anonymous) | OpenReview API record | **The only direct memory-contamination-recovery work found.** Recovers the complete family of minimal rollbacks for corrupted memory updates; enumerates assignments over registered fault atoms, closes under dependency, verifies by replay; defers rollback choice until query arrives; sound bounds under incomplete provenance. 33,680 oracle checks with zero failures vs exhaustive replay; preregistered 415-trace, 8-backend MemoryArena evaluation; query-adaptive scoring superior on 6 backends (+5.3–9.3 pts), "no added poison leakage" | **Single-agent self-evolving memory.** No multi-agent shared memory, no cross-agent propagation measurement, no organizational roles/authority. But its machinery (fault atoms, replay verification, poison-leakage metric) is directly reusable for a MAS blast-radius study — both a building block and a partial occupant of the "recovery" corner |
| GATEMEM: Benchmarking Memory Governance in Multi-Principal Shared-Memory Agents | OpenReview i8zzVWLDX2, 2026 (anonymous) | OpenReview API record | Benchmark for shared-memory assistants (medical/office/education/household): joint utility + access control across authorization boundaries + **active forgetting after explicit deletion requests**; long-form multi-party episodes, incremental memory injection, hidden checkpoints, leak-target annotations. Finding: no method achieves utility + access control + reliable forgetting simultaneously; retrieval/external-memory methods leak unauthorized or deleted info | Governance benchmark: deletion/forgetting is user-requested, not fault-triggered; no fault injection, no propagation measurement |
| What Can This Skill Safely Undo? Rollback-Oriented Auditability for Agent Skills (Zifan Peng, Mingchen Li) | OpenReview zS5eRqW2QQ, 2026 | OpenReview API record | Position/sketch: skill-induced state changes as recovery objects with persistence, recoverability, dependency, conflict, remediation properties; recovery-preview interface; SKILL.md metadata hooks | Sketch only; about tool/skill side effects, not memory |
| Cognitive Immunity for Trustworthy LLM Agents (Mian Zhang) | OpenReview eiw7dgCNad, 2026 | OpenReview API record | Runtime failure-memory layer: antigen descriptor from observed failure → antibody rules with decay/reinforcement → retrieved before future responses; repeat failure rate 0.764→0.650 on 20-task longitudinal benchmark | Prevention of *repeated* failures via memory, single-agent; modest effect; not recovery of contaminated shared state |
| Quantifying Rollback Propagation in Distributed Checkpointing (Adnan Agbaria, Hagit Attiya, Roy Friedman, Roman Vitenberg) | SRDS 2001, DOI 10.1109/reldis.2001.969737; journal version JPDC 2004, DOI 10.1016/j.jpdc.2004.01.003 | Crossref | **Classical analogue of blast radius**: k-rollback classification — max number of checkpoints that must be rolled back during recovery; coordinated checkpointing and ZPF are 1-rollback; ZCF is (n−1)-rollback; d-BC protocol bounds rollback propagation | Classical distributed systems, no LLM agents; provides formal vocabulary (rollback propagation, domino effect, recovery lines) that a MASO paper should import |
| Evaluating Distributed Checkpointing Protocol (Agbaria, Freund, Friedman) | OpenReview sDCLELXriQ (archival record) | OpenReview API record | Overhead-ratio measure incorporating rollback propagation into protocol evaluation | Classical |
| Distributed snapshots: determining global states of distributed systems (Chandy & Lamport) | ACM TOCS 1985, DOI 10.1145/214451.214456 | Crossref | Consistent global snapshots — the substrate for any checkpoint/rollback recovery | Classical |
| Self-stabilizing systems in spite of distributed control (Dijkstra) | CACM 1974, DOI 10.1145/361179.361202 | Crossref | Recovery to legitimate states without external intervention | Classical |

**Assessment:** memory contamination *recovery* exists in exactly one fresh, unpublished, single-agent work (FamilyRepair). The classical distributed-systems literature has mature formal machinery for rollback propagation (k-rollback, domino effect, recovery lines) that has **never been connected to LLM multi-agent memory**. This is a genuine, defensible gap.

---

## 4. Blast-radius terminology collision (important for positioning)

| Paper | ID | Verified | Relevance |
|---|---|---|---|
| What Can One Bad Tool Call Destroy? Measuring and Minimizing Blast Radius in Agentic Tool Use (Muhammet Anil Yagiz) | OpenReview MYvsxnxbCf, 2026 | OpenReview API record | DamageFlow benchmark + **Blast Radius Score (BRS)** decomposing unauthorized tool effects by resource sensitivity, action impact, **propagation**, and **recovery cost**; covers indirect prompt injection, MCP tool poisoning, tool shadowing, and **multi-agent relay attacks**; BlastGuard runtime (least-privilege capability graphs, untrusted-context tracking, dry-run, scoped tokens, **rollback logs**); 80-scenario pilot: same 20% ASR can differ 89× in BRS; BlastGuard retains 87.5% benign utility |

**This is the nearest neighbor to the seed hypothesis in terminology and spirit** ("agent safety evaluation should measure not only whether agents fail, but how far failure can spread"). Differentiation available: DamageFlow's channel is tool-call side effects under injection attacks; it does not study shared memory as the propagation medium, nor organizational structure (roles, delegation, authority) as the determinant of spread, nor memory recovery. But a MASO submission must cite and clearly differentiate from it. (Note: single-author OpenReview record, pilot-scale — likely a workshop submission, possibly to MASO itself.)

---

## 5. Long-term memory architectures for MAS (capability side — no fault studies)

| Paper | ID / venue | Verified | One-line |
|---|---|---|---|
| MemGPT (Charles Packer et al.) | arXiv:2310.08560, Oct 2023 | arXiv abs | OS-inspired virtual context management, memory tiers |
| MemoryBank (Wanjun Zhong et al.) | arXiv:2305.10250, May 2023 | arXiv abs | Ebbinghaus-curve forgetting for long-term companion memory |
| A-MEM: Agentic Memory (Wujiang Xu et al.) | arXiv:2502.12110, NeurIPS 2025 | arXiv abs | Zettelkasten-style dynamic linking/evolution of memory notes |
| Mem0 (Prateek Chhikara et al.) | arXiv:2504.19413, Apr 2025 | arXiv abs | Production memory extraction/consolidation; LOCOMO SOTA; graph variant |
| Zep (Preston Rasmussen et al.) | arXiv:2501.13956, Jan 2025 | arXiv abs | Temporal knowledge-graph memory (Graphiti); temporal invalidation of facts |
| MIRIX (Yu Wang, Xi Chen) | arXiv:2507.07957, Jul 2025 | arXiv abs | Six memory types + multi-agent framework controlling updates/retrieval; multimodal; 85.4% LOCOMO |
| G-Memory: Tracing Hierarchical Memory for MAS (Guibin Zhang, Muxin Fu, Guancheng Wan, Miao Yu, Kun Wang, Shuicheng Yan) | arXiv:2506.07398, Jun 2025 | arXiv abs + HTML | Three-tier graph hierarchy (insight/query/interaction) for MAS trajectories, inspired by **organizational memory theory** (Walsh & Ungson 1991); +20.89% embodied success; finds prevailing MAS memory "overly simplistic" |
| INMS: Memory Sharing for LLM-based Agents (H. Gao, Y. Zhang) | arXiv:2404.09982, Apr 2024 (v3 Mar 2026) | arXiv abs | Asynchronous shared conversational memory pool for multi-agent systems |
| MetaGPT (Sirui Hong et al.) | arXiv:2308.00352, Aug 2023 | arXiv abs | Shared message pool + SOPs; motivates with "cascading hallucinations caused by naively chaining LLMs" |
| AutoGen (Qingyun Wu et al.) | arXiv:2308.08155, 2023 | via MemClaw reference list | Multi-agent conversation framework |
| A Survey on the Memory Mechanism of LLM-based Agents (Zeyu Zhang et al.) | arXiv:2404.13501, Apr 2024 | arXiv abs | The standard memory survey (STM/LTM taxonomy) |
| Multi-Agent Memory from a Computer Architecture Perspective (Zhongming Yu … Jishen Zhao) | OpenReview 00knws86Qu, 2026 | OpenReview API record | Position paper: shared vs distributed memory paradigms, 3-layer hierarchy; "the most pressing open challenge is multi-agent memory **consistency**" |
| MemoryArena (Zexue He, Yu Wang, …, Yejin Choi, Alex Pentland) | OpenReview JI6lVgLPjp / tBrBPQMFHO, 2026 | OpenReview API record | Multi-session interdependent memory benchmark; agents near-saturated on LoCoMo fail here |
| MUMBench (in AIM paper) | arXiv:2609.12320 | arXiv abs | First multi-user memory benchmark (retrieval/creation/update/deletion) |

**Assessment:** capability-side memory architectures are crowded (2023–2026). None of them studies failure behavior: no fault injection, no corruption spread, no recovery. G-Memory's use of organizational memory theory and the computer-architecture position paper's "memory consistency is the pressing open challenge" both corroborate that the *failure/consistency* side of MAS memory is recognized as open.

---

## 6. Containment mechanisms adjacent to memory (partial occupants)

| Paper | ID / venue | Verified | Relevance |
|---|---|---|---|
| Securing AI Agents with Information-Flow Control (Fides) (M. Costa, B. Köpf et al., Microsoft) | arXiv:2505.23643, May 2025 | arXiv abs | Dynamic taint tracking with confidentiality/integrity labels in the planner; formal enforceability characterization; AgentDojo eval. IFC is a *containment* mechanism that could bound memory-mediated spread, but it is single-agent planner-level, not organizational |
| Defeating Prompt Injections by Design (CaMeL) (Edoardo Debenedetti et al.) | arXiv:2503.18813, Mar 2025 | arXiv abs | Control/data-flow extraction + capabilities; 77% tasks with provable security on AgentDojo. Prevents untrusted data from affecting control flow — would prevent some memory-poisoning write paths but is not a memory-recovery mechanism |
| RobustRAG: Certifiably Robust RAG against Retrieval Corruption (Chong Xiang et al.) | arXiv:2405.15556, May 2024 (v2 Apr 2026) | arXiv abs | Isolate-then-aggregate; certifiable robustness to bounded malicious passages. Retrieval-time containment; does not repair the poisoned store |
| On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents (Jen-Tse Huang et al.) | arXiv:2408.00989, Aug 2024 | arXiv abs | **Fault injection into MAS communication** (AutoTransform/AutoInject); hierarchical structure most resilient (5.5% vs 23.7% drop); Challenger/Inspector recover up to 96.4% of errors. Adjacent: propagation via messages, not memory; likely covered by another landscape |

---

## 7. Classical MAS / distributed-systems grounding (pre-LLM)

- **Blackboard architectures** (HEARSAY-II lineage): shared structured workspace as the original "shared memory" MAS coordination medium — the historical ancestor of MetaGPT's message pool and fleet memory.
- **Organizational memory**: Walsh & Ungson, *Academy of Management Review* 16(1):57–91, 1991 (verified via G-Memory reference list) — the org-theory basis G-Memory invokes.
- **Checkpoint/rollback recovery & rollback propagation**: Chandy–Lamport 1985 (DOI 10.1145/214451.214456); Agbaria et al. SRDS 2001 / JPDC 2004 (DOIs verified) — k-rollback = formal blast radius for rollback recovery; domino effect.
- **Self-stabilization**: Dijkstra 1974 (DOI 10.1145/361179.361202).
- **Replication/consistency for shared state**: Bayou (Terry et al., SOSP 1995), Dynamo (DeCandia et al., 2007), Spanner (Corbett et al., 2013), CRDTs (Shapiro et al., SSS 2011) — all verified via MemClaw's reference list; MemClaw explicitly imports this lineage.
- **Access control**: RBAC (Sandhu et al., IEEE Computer 1996), ABAC (NIST SP 800-162, 2014) — verified via MemClaw's reference list.

**The concept of fault propagation through shared state predates LLMs by decades; what does not exist is its instantiation for LLM multi-agent memory with task-utility-aware measurement.**

---

## 8. Explicit answers to the assignment questions

**Q1: Does any work measure or contain fault propagation THROUGH shared memory?**
No. Verified closest approaches and why they don't count:
- MemClaw (2606.24535): measures propagation *latency/visibility* and governance failure modes; no injected faults, no behavioral impact, no recovery.
- GATEMEM (i8zzVWLDX2): measures leakage and forgetting in multi-principal shared memory; no fault injection or spread measurement.
- DamageFlow (MYvsxnxbCf): measures blast radius of tool-use attacks incl. multi-agent relay; channel is tool side effects, not shared memory.
- MINJA (2503.03704): memory injection, single-agent; multi-agent spread named as future work only.
- Resilience-with-faulty-agents (2408.00989): fault propagation via communication, not memory.

**Q2: Is memory contamination recovery studied?**
Barely. FamilyRepair (IJoWb6T3RJ) is the only direct hit (rollback families + replay verification + poison-leakage metric) and is single-agent and unpublished. GATEMEM covers deletion/forgetting as governance. MINJA/MPBench show defenses fail but offer no recovery. Classical rollback-propagation theory (Agbaria et al.) is unconnected to LLM agents.

**Does anything here kill or subsume the seed hypothesis?**
No kill. The seed's memory-boundary component is *supported* as open by multiple independent 2026 signals (MemClaw's failure-mode taxonomy stops at governance; the computer-architecture position paper calls MAS memory consistency the pressing open challenge; attack papers show persistence and defense failure; FamilyRepair shows recovery is just beginning, single-agent). Two positioning constraints: (1) differentiate from DamageFlow's "blast radius" (tool-use) and from MemClaw (governance) explicitly; (2) the memory-only slice alone may be too thin for a full paper — the seed's strength is exactly the cross-boundary (role/authority/communication/memory) generalization that none of these works attempt. Note also the repo boundary: the killed "experience commons / zero-trust memory games" candidate overlaps with MemClaw/GATEMEM governance territory — the live gap is *fault-injection-driven propagation measurement and recovery*, not memory governance games.

**Confidence caveats:** dblp unreachable; Semantic Scholar and arXiv APIs heavily rate-limited, so discovery relied on reference mining of verified full texts plus OpenReview search. Coverage of arXiv-only 2026 submissions may be incomplete. Several key 2026 records are anonymous OpenReview submissions without exposed venue — treat as pre-publication.
