# LANDSCAPE B17 — Inter-Agent Communication Protocols

**Investigator:** B17 specialist (adversarial evidence-gathering)
**Date:** 21 September 2026
**Mission:** Map A2A, MCP, ACP, ANP, Agora and academic protocol work with respect to message reliability, lost/delayed messages, protocol-level faults, and interoperability failures. Determine whether communication faults (dropped/delayed/corrupted messages) are studied as failure injectors in MAS evaluation. Assess implications for the seed hypothesis ("organizational failure propagation and recovery in LLM multi-agent systems" / "organizational blast radius").

**Verification method:** Every paper below was verified by fetching the actual arXiv abstract page, the official protocol specification site, the Wayback Machine (FIPA), or the Crossref API (classical DOIs) — not search snippets. arXiv IDs, authors, and submission dates are quoted from the abstract pages. Where a claim could not be verified it is marked UNVERIFIED and excluded from the evidence tables.

---

## 1. Bottom line

**The seed hypothesis survives this landscape, but two 2026 papers are dangerous neighbors that a MASO reviewer will cite, and the framing must be narrowed to stay defensible.**

- Communication faults **are** starting to be used as failure injectors in LLM-MAS evaluation — MAS-FIRE (Feb 2026), AgentChaosBench (Aug 2026), TraceFix (May 2026), llmmas-otel (Aug 2026), ProtocolBench (Oct 2025), and a chaos-engineering proposal (May 2025). A claim of "first to inject communication faults into LLM MAS" would be **false**.
- However, **no verified work studies what determines the organizational blast radius of a communication fault** (spread across role, authority/delegation, memory, accountability, human-agent boundaries) **or compares containment/recovery mechanisms under a utility-preservation objective**. Existing work stops at detection/localization (AgentChaosBench), fault-tolerance tiering by topology (MAS-FIRE), protocol benchmarking (ProtocolBench), deadlock prevention by verification (TraceFix), or attribution (AgenTracer, DCFA, Who&When).
- The industry protocols themselves (A2A, MCP, ACP, ANP) are analyzed almost exclusively through a **security** lens (A2ABreak, threat modeling, MCPTox), not a **reliability/fault-tolerance** lens. Their specs provide no message-delivery guarantees (no exactly-once semantics, no standardized retry/timeout discipline) — an open, verifiable gap.
- Classical MAS (FIPA ACL, KQML, Contract Net) and distributed systems (Byzantine faults, CAP, lineage-driven fault injection, chaos engineering) supply mature fault vocabulary that LLM-MAS evaluation is only now importing — useful for framing, and a novelty check: the *ideas* are old, the *instantiation* in organizational LLM-MAS is new.

---

## 2. The industry protocol landscape (verified from official sources)

| Protocol | Origin / governance | Verified source | Core model | Reliability-relevant mechanisms in spec |
|---|---|---|---|---|
| **MCP** (Model Context Protocol) | Anthropic, announced 25 Nov 2024; open spec | modelcontextprotocol.io spec 2025-06-18 (fetched) | JSON-RPC 2.0; host/client/server; tools, resources, prompts; sampling, roots, elicitation | Cancellation, progress tracking, error reporting, logging. **No delivery guarantees, no retry/timeout standard, no message ordering across sessions.** Security principles explicitly delegated to implementors ("MCP itself cannot enforce these security principles at the protocol level"). |
| **A2A** (Agent2Agent) | Google (Apr 2025), donated to Linux Foundation; TSC incl. AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, ServiceNow | a2a-protocol.org/latest/ (fetched) | Agent Cards (capability discovery), Tasks with lifecycle states, peer task delegation across "opaque" agents | Task lifecycle states and push notifications/streaming; **spec-level reliability semantics (retries, idempotency, delivery guarantees) are minimal**; positioned as complement to MCP. |
| **ACP** (Agent Communication Protocol) | IBM/BeeAI, Linux Foundation | agentcommunicationprotocol.dev (fetched) | RESTful HTTP, MIME-typed multipart messages, sync + async, streaming, stateful/stateless, online/offline discovery | Async-first design for long-running tasks; **no protocol-level reliability/ordering guarantees documented**; relies on HTTP semantics. |
| **ANP** (Agent Network Protocol) | ANP community (China-led); white paper on arXiv | agent-network-protocol.com (fetched, ANP 1.1); arXiv:2508.00007 | Three-layer stack: DID:WBA identity + encrypted communication, meta-protocol negotiation, application protocols (discovery, payment, commerce) | Identity/authentication focus; reliability semantics not a stated design goal in the white paper. |
| **Agora** | Academic (Oxford: Marro, La Malfa, Wright, Li, Shadbolt, Wooldridge, Torr) | arXiv:2410.11905 (submitted 14 Oct 2024) | **Meta-protocol**: standardized routines for frequent communication, natural language for rare cases, LLM-written routines in between; "Agent Communication Trilemma" (versatility, efficiency, portability) | Explicitly designed to "robustly handle changes in interfaces and members"; self-organizing protocols emerge at scale. **No fault model for message loss/delay; robustness = adaptability, not delivery guarantees.** |

**Naming collision warning:** "ACP" is used for at least three different things in this literature: (a) IBM/BeeAI Agent Communication Protocol; (b) "ACPs: Agent Collaboration Protocols for the Internet of Agents" (arXiv:2505.13523, Liu et al., May 2025); (c) "A Unified Agent Communication Protocol (ACP)" (arXiv:2602.15055, Feb 2026). Reviews must disambiguate.

---

## 3. Academic protocol surveys and analyses (all verified via arXiv abstract pages)

| arXiv ID | Title / Authors / Date | What it does | Relevance to communication faults |
|---|---|---|---|
| 2505.02279 | *A survey of agent interoperability protocols: MCP, ACP, A2A, ANP* — Ehtesham, Singh, Gupta, Kumar (4 May 2025, v2 23 May 2025) | First side-by-side survey of the four industry protocols; compares interaction modes, discovery, communication patterns, security models; proposes phased adoption roadmap | Descriptive; **no fault/reliability evaluation**; security models compared qualitatively |
| 2606.19135 | *A Technical Taxonomy of LLM Agent Communication Protocols* — Sander, Gidey, Lenz, Knoll (17 Jun 2026) | Iterative taxonomy over 9 actively maintained open-source protocols; 5 dimensions (counterparty, payload, interaction state, discovery, schema flexibility) | Finds decentralized discovery rare; predicts federated layered stack; **reliability not a taxonomy dimension** — evidence the field does not treat message faults as first-class |
| 2506.19676 | *A Survey of LLM-Driven AI Agent Communication: Protocols, Security Risks, and Defense Countermeasures* — Kong et al. (24 Jun 2025, v4 27 Nov 2025; 48pp) | Defines agent communication, 3-class framework, 3-layer architecture; dissects protocols per class; runs MCP/A2A vulnerability experiments | Security-focused; confirms protocol-layer risks are studied as **attacks**, not as **accidental faults** |
| 2604.02369 | *Beyond Message Passing: A Semantic View of Agent Communication Protocols* — Yuan et al. (30 Mar 2026, v3 13 Apr 2026) | Organizes 18 protocols into communication/syntactic/semantic layers | Key finding: protocols mature on transport/streaming/schema but **"offer limited protocol-level mechanisms for clarification, context alignment, and verification"** — semantic responsibilities pushed into prompts/wrappers. Direct support for a semantic-fault gap claim |
| 2602.11327 | *Security Threat Modeling for Emerging AI-Agent Protocols: MCP, A2A, Agora, ANP* — Anbiaee et al. (11 Feb 2026, v2 17 Apr 2026) | Structured threat model; 12 protocol-level risks across creation/operation/update; measurement case study on MCP wrong-provider tool execution | Security lens again; lifecycle-phase risk framing is reusable for fault-injection design |
| 2607.23884 | *A Comparative Study of MCP and A2A for Inter-Agent Coordination in LLM-Based Systems* — Predoaia, Vu, Barmpis, Kolovos, García-Domínguez (26 Jul 2026) | Implementation-grounded comparison: same SE task built on MCP vs A2A; requirements incl. discoverability, async, observability, access control | Finds MCP pushes conversational state/task lifecycle to the application layer; A2A has richer native stateful coordination but more complexity. **No fault injection** |
| 2508.15819 | *Agent Communications toward Agentic AI at Edge — A Case Study of the Agent2Agent Protocol* — Duan, Lu (17 Aug 2025) | Assesses A2A against edge-computing challenges | Notes protocols designed "without sufficient consideration" of constrained/lossy environments — closest to a reliability critique of A2A |
| 2510.13821 | *LACP Requires Urgent Standardization: A Telecom-Inspired Protocol is Necessary* — Li, Liu, Yuen (26 Sep 2025) | Position paper; 3-layer telecom-inspired protocol (semantic clarity, transactional integrity, built-in security) | Argues current ecosystem is a fragmented "protocol wars" situation; **transactional integrity** explicitly named as missing |
| 2508.10146 | *Agentic AI Frameworks: Architectures, Protocols, and Design Challenges* — Derouiche, Brahmi, Mazeni (13 Aug 2025) | Compares CrewAI, LangGraph, AutoGen, Semantic Kernel, Agno, ADK, MetaGPT; analyzes CNP, A2A, ANP, Agora | Bridges classical (Contract Net) and modern protocols |
| 2601.13671 | *The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption* — Adimulam, Gupta, Kumar (20 Jan 2026) | Consolidated orchestration architecture; MCP + A2A as communication substrate | Enterprise/governance framing; no fault model |
| 2505.13523 | *ACPs: Agent Collaboration Protocols for the Internet of Agents* — Liu et al. (18 May 2025) | Proposes protocol suite (registration, discovery, interaction, tooling); restaurant-booking demo | Claims MCP/A2A/ANP "fragmented and scenario-specific" |
| 2407.07061 | *Internet of Agents: Weaving a Web of Heterogeneous Agents for Collaborative Intelligence* — Chen et al. (9 Jul 2024) | IM-like architecture, agent integration protocol, dynamic teaming/flow control | Notes existing frameworks' "hard-coded communication pipelines" limit adaptability |

---

## 4. Security analysis of protocols (verified; relevant because it is the dominant lens)

| arXiv ID | Title / Authors / Date | Core result |
|---|---|---|
| 2609.10871 | *A2ABreak: Systematic Security Analysis of the A2A Protocol* — Lotfi, Rahman, Karim, Bertino (9 Sep 2026) | LLM-assisted extraction of verified FSM from A2A spec (37 states, 76 transitions, 929 formalized statements); **11 new specification-level vulnerabilities exploitable by a fully spec-compliant adversary** (cross-client context injection via unprotected context IDs, credential harvesting via multi-hop identity loss in delegation chains, data exfiltration via unattested capability claims). Zero-shot LLM baseline finds zero. |
| 2503.23278 | *Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions* — Hou, Zhao, Wang, Wang (30 Mar 2025, v3 7 Oct 2025) | MCP server lifecycle (4 phases, 16 activities); threat taxonomy across 4 attacker types, 16 threat scenarios; real-world case studies |
| 2504.08623 | *Enterprise-Grade Security for MCP* — Narajala, Habler (11 Apr 2025, v2 2 May 2025) | Threat modeling + mitigation framework; tool poisoning |
| 2508.14925 | *MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers* — Wang et al. (19 Aug 2025) | 45 live MCP servers, 353 authentic tools; tool-poisoning robustness benchmark |
| 2608.14613 | *Do LLM Agents Negotiate Rationally? Mechanism-Design over A2A/MCP* — Albayaydh, Zhao (10 Jul 2026) | Encodes bargaining/VCG mechanisms as A2A message-schema constraints; runtime verification/repair layer; shows protocols "specify transport and discovery rather than strategic correctness" |

**Observation for the seed hypothesis:** protocol-level analysis energy is going into *adversarial* faults (specification-compliant attacks), not *operational* faults (loss, delay, corruption, misrouting). The operational-fault study of these protocols is nearly empty except for the evaluation work in §5.

---

## 5. Communication faults as failure injectors in MAS evaluation — the core question

### 5.1 Direct evidence: LLM-MAS fault injection works (all verified)

| arXiv ID | Title / Authors / Date | Fault model | Injection mechanism | What is measured | Relationship to seed hypothesis |
|---|---|---|---|---|---|
| 2602.19843 | **MAS-FIRE**: *Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems* — Jia, Deng, Chen, Wang, Zheng (23 Feb 2026) | Taxonomy of **15 fault types**: intra-agent cognitive errors (hallucination, reasoning drift) + **inter-agent coordination failures** | 3 non-invasive mechanisms: prompt modification, **response rewriting, message routing manipulation** | Fault-tolerance behaviors organized into 4 tiers (mechanism, rule, prompt, reasoning); 3 MAS architectures; finds stronger base models do NOT uniformly improve robustness; **iterative closed-loop topologies neutralize >40% of faults that cause catastrophic collapse in linear workflows** | **Most dangerous neighbor.** Already shows architecture/topology determines fault impact — one determinant of "blast radius." But: faults are *semantic*, not protocol-level message faults; no organizational boundaries (authority/delegation/memory); no containment-mechanism comparison; no utility-preservation objective |
| 2608.14680 | **AgentChaosBench**: *When Agentic Executions Fail: Detecting and Localizing Runtime Faults from Telemetry* — Zhang, Li, Tian, Bachras, Jacobsen (4 Aug 2026) | **10 operational fault types: unavailable/slow tools, corrupted/oversized responses, delayed/looped/misrouted delegations, bypassed guardrails** — injected at tool, model, guardrail, and **inter-agent boundaries** | Fault injection in 5 heterogeneous apps coordinating agents over **A2A** and tools over **MCP**; 275 traces (250 faulty + 25 controls), each aligned with no-fault twin | Task = detect + localize fault from telemetry. Zero-shot LLMs reach only 13.6–19.2% top-1 fault-type accuracy (local ≤14B), 24.8% (DeepSeek-v4-pro) | **Most direct evidence that communication faults (delayed/misrouted/looped delegations, corrupted responses) are now injected into A2A/MCP systems.** But the research question is *diagnosis from telemetry*, not propagation dynamics or containment. Dataset/benchmark, not mechanism study |
| 2605.07935 | **TraceFix**: *Repairing Agent Coordination Protocols with TLA+ Counterexamples* — Xia, Li, Ehsan, Ortiz (8 May 2026) | Deadlock/livelock in coordination protocols; runtime fault injection ablation | LLM synthesizes protocol IR → PlusCal → TLC model checking → repair loop; runtime monitor rejects out-of-topology ops | 48 tasks, 16 scenario families; 3,456-run comparison; verified protocols cut DL/LL from 31.1%→14.1%, **largest separation under fault injection**; verified protocols degrade at half the rate under weakened models | Shows *prevention by formal verification* works for coordination faults. Complementary, not subsuming: no organizational semantics, no blast-radius measure |
| 2608.24271 | *Observability and Fault Injection for LLM-Based MAS in Software Engineering* (llmmas-otel) — Seyedghorban, Klimov, van Deursen, Panichella, Ozkan (25 Aug 2026) | Targeted faults at "selected interaction points" across workflow phases, agent steps, **inter-agent communication**, tool calls, LLM invocations | OpenTelemetry tracing + fault injection, framework-agnostic | Tool paper; baseline-vs-faulty trace comparison; validated on demo + real SE MAS | Infrastructure evidence: fault injection tooling for LLM-MAS now exists and is publishable as a tool paper |
| 2505.03096 | *Assessing and Enhancing the Robustness of LLM-based Multi-Agent Systems Through Chaos Engineering* — Owotogbe (6 May 2025) | Hallucinations, agent failures, **agent communication failures** | Proposes chaos-engineering framework for LLM-MAS in production-like settings | Proposal-level (single author, no comments/venue info on arXiv page; abstract describes framework proposal) | Earliest explicit call for chaos engineering of LLM-MAS incl. communication failures; shallow but citable as prior art for the *idea* |
| 2510.17149 | **ProtocolBench**: *Which LLM MultiAgent Protocol to Choose?* — Du et al. (20 Oct 2025, v3 2 Jun 2026) | **"Fail-Storm Recovery" scenario**; robustness under failures is one of 4 benchmark axes (with task success, latency, message/byte overhead) | Systematic comparison of A2A, ACP, ANP, Agora et al.; ProtocolRouter learns per-scenario protocol selection | Completion time varies up to 36.5% across protocols (Streaming Queue); ProtocolRouter cuts Fail-Storm recovery time up to 18.1% vs best single protocol | **Proves protocol choice measurably affects fault recovery** — a blast-radius determinant. But it benchmarks protocols; does not model organizational structure or containment mechanisms |

### 5.2 Failure attribution / taxonomy work (context, not injection)

| arXiv ID | Title / Date | Role |
|---|---|---|
| 2503.13657 | *Why Do Multi-Agent LLM Systems Fail?* (MAST) — Cemri et al. (17 Mar 2025, v3 26 Oct 2025) | 14 failure modes in 3 categories (system design, **inter-agent misalignment**, task verification); 1600+ traces, 7 frameworks; κ=0.88. The standard failure taxonomy — but observational, not fault-injection |
| 2505.00212 | *Which Agent Causes Task Failures and When?* (Who&When) — Zhang et al. (30 Apr 2025, v3 2 Jun 2025) | Failure-attribution benchmark; best method 53.5% agent accuracy, 14.2% step accuracy |
| 2509.03312 | *AgenTracer* — Zhang et al. (3 Sep 2025) | Counterfactual replay + **programmed fault injection** to annotate failed trajectories; trains AgenTracer-8B; +4.8–14.2% gains on MetaGPT/MaAS |
| 2609.04749 | *DCFA: Dual-view Causal-inspired Attribution* — Wang et al. (4 Sep 2026) | Causal dependency graphs + counterfactual reasoning on Who&When; +8.27% step accuracy |
| 2606.18668 | *EARS: Explanatory Abstention for Reliable Sub-Agent Modeling* — Xie et al. (17 Jun 2026) | **Reframes sub-agent abstention as an inter-agent communication protocol**: exposes actionable failure state to coordinator instead of hallucinating. Closest verified work to a *containment* mechanism at the communication layer — but trained behavior, not protocol machinery, and single coordinator→sub-agent topology |

### 5.3 Negative results (searches that came back empty)

- arXiv searches for `"communication failure" multi-agent LLM`, `"message loss" multi-agent LLM`, `"network partition" LLM agents`, `chaos engineering LLM agents` returned **zero or near-zero results** beyond the papers in §5.1 (searches run 21 Sep 2026; arXiv search rate-limited heavily, so coverage is good but not provably complete).
- `"blast radius"` in the agent literature: the only arXiv hit titled *Blast Radius* (2608.07440, Pitsane & Mogale, Aug 2026) is about **token/context eviction in agentic coding**, unrelated to failure propagation. **The term is free in the LLM-MAS failure-propagation sense** (it is of course standard in security/SRE usage).
- No verified work injects **classical network faults** (partitions, asymmetric delay, message reordering, duplication, bit corruption at transport) into LLM-MAS. MAS-FIRE injects semantic faults; AgentChaosBench injects operational faults at boundaries (delay/misrouting/corruption of *responses/delegations*); neither models a network layer.

---

## 6. Classical anchors (verified via Crossref DOI / Wayback Machine)

| Reference | Verified identifier | What it contributes to this landscape |
|---|---|---|
| Smith, *The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver* | IEEE Trans. Computers, 1980. DOI 10.1109/TC.1980.1675516 (Crossref-verified) | Classical task-allocation protocol (announce/bid/award); still the template for delegation; surveyed alongside A2A/ANP/Agora in 2508.10146 |
| Finin, Fritzson, McKay, McEntire, *KQML as an Agent Communication Language* | CIKM 1994. DOI 10.1145/191246.191322 (Crossref-verified) | Performatives + content language separation; the ancestor of all ACLs. (Also: Labrou & Finin, *A semantics approach for KQML*, CIKM'94, DOI 10.1145/191246.191320; Mayfield, Labrou, Finin, *Evaluation of KQML…*, 1996, DOI 10.1007/3540608052_77) |
| FIPA, *ACL Message Structure Specification* SC00061G | FIPA TC Communication, **Standard** status 2002-12-03 (verified via Wayback Machine capture of fipa.org) | Message parameters: performative, sender, receiver, content, **conversation-id, reply-with, in-reply-to, reply-by (timeout)** — i.e., classical ACLs standardized conversation tracking and reply deadlines that MCP/A2A only partially reinvent. **Note: fipa.org is now a casino spam domain (fetched 21 Sep 2026); the spec survives only via archive.org — a cautionary data point on protocol governance longevity, and citable motivation for studying protocol failure/evolution itself.** |
| Cohen & Levesque, *Intention is Choice with Commitment* | Artificial Intelligence, 1990. DOI 10.1016/0004-3702(90)90055-5 (Crossref-verified) | Speech-act semantics underlying ACLs |
| Lamport, Shostak, Pease, *The Byzantine Generals Problem* | ACM TOPLAS, 1982. DOI 10.1145/357172.357176 (Crossref-verified) | Canonical fault model for corrupted/spoofed messages |
| Gilbert & Lynch, *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services* | ACM SIGACT News, 2002. DOI 10.1145/564585.564601 (Crossref-verified) | CAP: partitions force consistency/availability trade-offs — directly applicable to partitioned agent organizations, unapplied so far |
| Alvaro, Rosen, Hellerstein, *Lineage-driven Fault Injection* | ACM SIGMOD 2015. DOI 10.1145/2723372.2723711 (Crossref-verified) | Molly: use data lineage to inject only outcome-relevant faults — the methodological template an organizational blast-radius study should cite and extend |
| (Practice) Netflix Chaos Monkey / Jepsen | Industry practice, no single canonical paper | Chaos engineering and partition testing of distributed systems; Owotogbe (2505.03096) is the LLM-MAS import |

**MARL communication robustness (verified via arXiv):** CommNet (1605.07736, Sukhbaatar et al., 2016); IC3Net (1812.09755, Singh et al., 2018 — learns *when* to communicate); SchedNet (1902.01554, Kim et al., 2019); **Message-Dropout (1902.06527, Kim, Cho, Sung, 2019 — explicitly trains robustness to communication errors at execution)**; and the line continues: *Value-Aware Prediction for Robust Multi-Agent Coordination Under Communication Loss* (2607.17914, Kafadar et al., Jul 2026, extending MARO observation-sharing under communication dropout). **Message loss/delay robustness is a mature MARL topic — but with learned policies, continuous messages, and no organizational boundaries. Nothing transfers directly to LLM-MAS, and no MARL paper studies role/authority/memory propagation.**

---

## 7. Synthesis: does this landscape kill or subsume the seed hypothesis?

**No kill. Partial adjacency that must be cited and differentiated.**

1. **"Communication faults as failure injectors in MAS evaluation" — the answer is now YES, barely.** Six verified works (MAS-FIRE, AgentChaosBench, TraceFix, llmmas-otel, ProtocolBench, Owotogbe) inject communication/coordination faults into LLM-MAS, all from May 2025–Aug 2026. The seed hypothesis cannot claim priority on fault injection per se.

2. **What none of them do** (the defensible residue):
   - No work defines or measures an **organizational blast radius** — spread of a local fault across role, communication, authority/delegation, tool, memory, accountability, and human-agent boundaries. MAS-FIRE varies topology but not organizational structure; AgentChaosBench localizes faults but does not trace cross-boundary spread; ProtocolBench times recovery but does not explain it.
   - No work compares **containment/recovery mechanisms** (circuit breakers, quarantine, message replay, checkpoint/rollback, graceful degradation, escalation-to-human) under a **task-utility-preservation** objective. TraceFix prevents deadlock by construction; EARS signals failure states; neither is a containment-mechanism study.
   - No work injects **protocol-level network faults** (partition, asymmetric delay, reorder, duplicate, corrupt) into A2A/MCP/ACP/ANP deployments and observes organizational consequences. AgentChaosBench is closest (delayed/misrouted/looped delegations) but its unit of analysis is the trace, not the organization.
   - The protocols' **missing reliability semantics** (no delivery guarantees in MCP/A2A/ACP specs — verified from the specs themselves) is an unstudied design gap that the seed project can document as motivation.

3. **Differentiation from the occupied delegation-invariants territory** (maso/policy_preserving_delegation_research_proposal.md): that proposal owns authority/policy/provenance preservation across A2A/MCP delegation chains. B17's residue is **operational communication faults and their organizational propagation/containment**, not policy invariants. Keep the seed framed on reliability/blast-radius, cite the delegation proposal as sibling work, and do not rebuild delegation invariants.

4. **Reviewer traps to pre-empt:**
   - "MAS-FIRE already did fault injection in MAS" → differentiate: semantic vs protocol/operational faults; fault-tolerance tiers vs organizational blast radius; no containment comparison.
   - "AgentChaosBench already injects delayed/misrouted delegations over A2A/MCP" → differentiate: diagnosis benchmark vs propagation-and-containment study; their own result (LLMs at 13.6–24.8% fault-type accuracy) motivates *mechanisms*, not just detection.
   - "ProtocolBench already measures robustness under failures" → differentiate: protocol selection benchmark vs organizational fault-containment science.
   - "This is just chaos engineering / LDFI rebranded" → cite Alvaro et al. 2015 and Owotogbe 2025 explicitly; the novelty is the organizational boundary model and utility-preserving containment, not fault injection itself.
   - "FIPA ACL had reply-by timeouts in 2002" → true; use it as framing (classical conversation machinery abandoned by modern protocols) rather than pretending the concepts are new.

---

## 8. Verified paper index (quick reference)

| # | arXiv/DOI | Short name | Verified via |
|---|---|---|---|
| 1 | 2410.11905 | Agora (Marro et al., Oct 2024) | arXiv abs page |
| 2 | 2505.02279 | Interoperability protocols survey (Ehtesham et al.) | arXiv abs page |
| 3 | 2606.19135 | Technical Taxonomy of LLM Agent Comm. Protocols | arXiv abs page |
| 4 | 2506.19676 | Agent communication security survey (Kong et al.) | arXiv abs page |
| 5 | 2604.02369 | Beyond Message Passing (Yuan et al.) | arXiv abs page |
| 6 | 2602.11327 | Threat modeling MCP/A2A/Agora/ANP (Anbiaee et al.) | arXiv abs page |
| 7 | 2508.00007 | ANP Technical White Paper (Chang et al.) | arXiv abs page |
| 8 | 2607.23884 | MCP vs A2A comparative study (Predoaia et al.) | arXiv abs page |
| 9 | 2609.10871 | A2ABreak (Lotfi et al.) | arXiv abs page |
| 10 | 2503.23278 | MCP landscape & security (Hou et al.) | arXiv abs page |
| 11 | 2504.08623 | Enterprise MCP security (Narajala & Habler) | arXiv abs page |
| 12 | 2508.14925 | MCPTox (Wang et al.) | arXiv abs page |
| 13 | 2508.20453 | MCP-Bench (Wang et al.) | arXiv abs page |
| 14 | 2602.19843 | **MAS-FIRE** (Jia et al.) | arXiv abs page |
| 15 | 2608.14680 | **AgentChaosBench** (Zhang et al.) | arXiv abs page |
| 16 | 2605.07935 | TraceFix (Xia et al.) | arXiv abs page |
| 17 | 2608.24271 | llmmas-otel (Seyedghorban et al.) | arXiv abs page |
| 18 | 2505.03096 | Chaos engineering for LLM-MAS (Owotogbe) | arXiv abs page |
| 19 | 2510.17149 | **ProtocolBench** (Du et al.) | arXiv abs page |
| 20 | 2503.13657 | MAST (Cemri et al.) | arXiv abs page |
| 21 | 2505.00212 | Who&When (Zhang et al.) | arXiv abs page |
| 22 | 2509.03312 | AgenTracer (Zhang et al.) | arXiv abs page |
| 23 | 2609.04749 | DCFA (Wang et al.) | arXiv abs page |
| 24 | 2606.18668 | EARS (Xie et al.) | arXiv abs page |
| 25 | 2508.15819 | A2A at edge (Duan & Lu) | arXiv abs page |
| 26 | 2601.13671 | MAS orchestration (Adimulam et al.) | arXiv abs page |
| 27 | 2510.13821 | LACP position paper (Li et al.) | arXiv abs page |
| 28 | 2505.13523 | ACPs (Liu et al.) | arXiv abs page |
| 29 | 2508.10146 | Agentic AI Frameworks (Derouiche et al.) | arXiv abs page |
| 30 | 2407.07061 | Internet of Agents (Chen et al.) | arXiv abs page |
| 31 | 2608.14613 | Rational negotiation over A2A/MCP (Albayaydh & Zhao) | arXiv abs page |
| 32 | 2608.07440 | "Blast Radius" (token eviction; unrelated) | arXiv abs page |
| 33 | 1605.07736 | CommNet | arXiv abs page |
| 34 | 1812.09755 | IC3Net | arXiv abs page |
| 35 | 1902.01554 | SchedNet | arXiv abs page |
| 36 | 1902.06527 | Message-Dropout | arXiv abs page |
| 37 | 2607.17914 | Value-Aware MARO (comm-loss MARL) | arXiv abs page |
| 38 | DOI 10.1109/TC.1980.1675516 | Contract Net (Smith 1980) | Crossref |
| 39 | DOI 10.1145/191246.191322 | KQML (Finin et al. 1994) | Crossref |
| 40 | FIPA SC00061G (2002) | FIPA ACL Message Structure Spec | Wayback Machine |
| 41 | DOI 10.1016/0004-3702(90)90055-5 | Cohen & Levesque 1990 | Crossref |
| 42 | DOI 10.1145/357172.357176 | Byzantine Generals (1982) | Crossref |
| 43 | DOI 10.1145/564585.564601 | Gilbert & Lynch CAP (2002) | Crossref |
| 44 | DOI 10.1145/2723372.2723711 | Lineage-driven Fault Injection (2015) | Crossref |
| 45 | a2a-protocol.org/latest/ | A2A official spec/docs | fetched live |
| 46 | modelcontextprotocol.io (spec 2025-06-18) | MCP official spec | fetched live |
| 47 | agentcommunicationprotocol.dev | ACP official docs | fetched live |
| 48 | agent-network-protocol.com | ANP official site (v1.1) | fetched live |

**Coverage caveat:** arXiv search was heavily rate-limited during this investigation (HTTP 429 for extended windows); discovery used arXiv search (when available), arXiv abs-page verification, Crossref, OpenReview API, Bing, and official spec sites. Coverage of the named protocols and of fault-injection-in-LLM-MAS is believed complete through ~mid-September 2026, but a final scoop-check pass on Semantic Scholar/DBLP (both rate-limited/bot-blocked during this run) is recommended before submission.
