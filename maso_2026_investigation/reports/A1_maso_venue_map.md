# A1 — MASO 2026 Venue Intelligence Report

**Investigator:** Venue Intel A1
**Date:** 21 September 2026
**Mission:** Adversarial evidence-gathering for MASO 2026 problem selection (seed hypothesis: organizational failure propagation and recovery in LLM multi-agent systems — "organizational blast radius" and containment/recovery).

**Sources (all fetched and inspected 21 Sep 2026):**
- MASO 2026 official site: https://www.maso.uno/ (home), `/call-for-papers.php`, `/committee.php`, `/tentative-programme-committee.php`, `/keynote.php`, `/program.php`, `/venue.php`
- EasyChair CFP stub: https://easychair.org/conferences/?conf=maso2026
- PRIMA 2026 host conference: https://prima2026.org/
- Organizer backgrounds: OpenAlex API (works counts, recent titles)
- Anchor papers: verified via arXiv abstract pages (IDs below)
- Discovery probes: DataCite API (api.datacite.org) — arXiv API, Semantic Scholar, OpenAlex, DBLP, Google/DDG were rate-limited/bot-blocked from this IP during the investigation window (see Limitations).

---

## 1. Venue facts (verified from the official site)

| Fact | Value | Source |
|---|---|---|
| Full name | 1st International Workshop on Multi-Agent and Agentic Systems **in Organizations** (MASO 2026) | maso.uno, EasyChair |
| Date / place | 14 December 2026, Kumamoto-Jo Hall, Kumamoto, Japan | maso.uno/venue.php |
| Host conference | PRIMA 2026 (27th Int. Conf. on Principles and Practice of Multi-Agent Systems), 14–17 Dec 2026, Kumamoto | prima2026.org |
| Submission deadline | **10 October 2026, 23:59 AoE** | maso.uno |
| Notification | 12 November 2026 | maso.uno |
| Camera-ready | 26 November 2026 | maso.uno |
| Submission system | EasyChair (`conf=maso2026`), submissions open | EasyChair |
| Format | Springer LNCS; **full papers max 16 pages excl. references; short papers max 8 pages excl. references** | CFP |
| Categories solicited | "Full research papers, short papers, Position papers, Practical papers" — but only two page-limit categories are defined, so position/practical papers presumably submit as short (8pp) | CFP |
| Review model | ≥2 reviewers per paper; **double-blind** ("fully anonymised"); at least one author must register for MASO **and PRIMA 2026** | CFP |
| AI policy | Follows PRIMA 2026 generative-AI policy: LLMs allowed for language editing or declared methodology; no AI co-authorship; substantive AI assistance must be disclosed | CFP |
| Keynote | Dr. Sergio Potenciano Menci, Head/Project Manager at **Encevo group SA** (Luxembourg energy group) — an *industry* keynote, signalling practitioner orientation | keynote.php |
| Program | Not yet published ("detailed schedule will be published soon") | program.php |

**Stated contribution preferences (verbatim CFP):** "original theoretical, methodological, empirical, and design-oriented contributions… Topics may include theoretical contributions, architectures, methodologies, evaluation frameworks, industrial case studies, public sector case studies, or visionary perspectives." Interdisciplinary work explicitly welcomed. No stated preference for benchmarks over methods; the topic list gives equal billing to "Evaluation frameworks, benchmarks, datasets, simulations, and organizational testbeds."

**Workshop positioning (verbatim, home page):** "address the theoretical, operational, and governance gaps of the deployment of multiples and heterogenous AI agents within organizations… Modern organizations are evolving into hybrid ecosystems where human workers collaborate with heterogeneous autonomous agents." The workshop's identity is *organizational* deployment of agentic AI — socio-technical, not pure-ML.

### Exact topics list (10 areas, from CFP)

1. **Agent Architectures and Orchestration** — centralized/decentralized/hybrid architectures; orchestration across organizational processes; agent composition, workflow management, task decomposition, delegation; role, specialization, lifecycle, state, resource management.
2. **Interoperability and Enterprise Integration** — agent-to-agent and agent-to-system communication; protocols, standards, semantic interoperability; integration with enterprise platforms/APIs/databases/tools; authentication, authorization, access control, identity management.
3. **Multi-Agent Coordination and Distributed Decision-Making in Organizations** — distributed planning/problem-solving/decision-making; task allocation, scheduling, resource allocation; negotiation, consensus, coalition formation, conflict resolution; coordination under uncertainty, incentive mechanisms, emergent organizational behavior.
4. **Human–Agent Collaboration in Organizational Settings** — delegation, team adaptation, socio-technical dynamics; human–agent teams, hybrid intelligence; human-in/on-the-loop, mixed-initiative; **allocation of roles, tasks, decision rights, responsibilities between humans and agents**.
5. **Organizational Learning, Agent Adaptation, Memory, and Knowledge Management** — continual/collaborative learning; adaptation, personalization, context awareness; individual/shared/episodic/**organizational memory**; organizational knowledge creation, transfer, retention, retrieval, reuse; knowledge graphs, RAG, cross-agent learning.
6. **Governance, Accountability, and Compliance** — governance models for agentic ecosystems in organizations; **allocation of responsibility, accountability, authority, liability**; regulatory compliance, standards alignment.
7. **Trust, Safety, Security, Privacy, and Reliability** — robustness, resilience, transparency, explainability, uncertainty awareness; privacy-preserving interaction, organizational data protection; **"Detection and mitigation of cascading, and systemic failures"** (verbatim).
8. **Evaluation, Benchmarking** — evaluation frameworks, benchmarks, datasets, simulations, **organizational testbeds**; metrics for autonomy, coordination, alignment, reliability, safety; human–agent and multi-agent team performance; **organizational productivity, quality, cost**.
9. **Organizational Design and Socio-Technical Transformation** — effects on organizational structures; readiness, adoption, change management; institutional implications, evolving role of human expertise.
10. **Applications and Deployment** — public/private/nonprofit sector; government, healthcare, education, finance, manufacturing; case studies, field experiments, deployment experiences; adoption barriers, scaling challenges, lessons learned.

**Seed-hypothesis fit:** Topic 7 names "detection and mitigation of cascading, and systemic failures" *verbatim* — the seed hypothesis is squarely on-topic, and additionally touches topics 1 (roles), 4 (decision rights), 5 (memory), 6 (accountability), 8 (testbeds/metrics). No topic area is a better exact match for the seed.

---

## 2. Organizers and program committee — research backgrounds

### General chairs (verified via OpenAlex, 21 Sep 2026)

| Chair | Affiliation | Evidence of research profile |
|---|---|---|
| **Igor Tchappi** | SnT, University of Luxembourg | 69 works (S2 author 51221370). Recent: "Norm mining, identification, and detection: a systematic literature review" (Frontiers in AI 2026); holonic MAS for smart buildings; privacy-preserving UAV agents (federated learning + BDI); LLM-agent applications (TermSheetPilot, HelpAgent); XAI. Profile: **applied MAS + norms + XAI + LLM agents**. |
| **Yazan Mualla** | UTBM, France | 79 works, 571 citations (OpenAlex A5025843371). Recent: "Explainable Agentic AI: Concepts, Scope, and Research Questions" (2026); "Toward Human-Centered Explanations for Agentic AI" (2026); trust calibration via role-aware causal explanations in smart-building MAS; XAI×HCI systematic review. Profile: **XAI for agentic systems, human-centered explanation, trust**. |
| **Rachele Carli** | Umeå University, Sweden | 28 works (OpenAlex A5070486875). Recent: "Question Zero: Why Responsible AI Begins Before AI Adoption" (2026); EU AI Act / Digital Omnibus policy analysis; UN global dialogue on AI governance input. Profile: **responsible AI, AI governance/policy, explainability**. |
| **Amro Najjar** | LIST, Luxembourg | 113 works, 1023 citations (OpenAlex A5081436358). Recent: norm-mining SLR (with Tchappi); privacy-preserving BDI UAV agents; BPMN-based MAS design with RAG; ethical persuasion & explanation transparency (EXTRAAMAS 2025). Profile: **human-agent interaction, XAI, normative MAS, behavior change**. |
| **Leon van der Torre** | University of Luxembourg | 526 works, 7833 citations (OpenAlex). Topics: MAS & negotiation, logic/reasoning/knowledge, deontic logic. Profile: **normative multi-agent systems founder-figure** (deontic logic, norms, responsibility). |

### Advisory board
- **Stéphane Galland** (UTBM; 207 works) — SARL agent programming language, Janus platform, holonic/organizational MAS engineering.
- **Abdeljalil Abbas-Turki** (UTBM) — systems/transportation MAS.
- **Kary Främling** (Umeå; 229 works, 4585 citations) — IoT, contextual explanation/XAI.

### Tentative programme committee (69 members listed) — composition analysis
Notable clusters (evidence: affiliations + known research areas):
- **Automated negotiation / agreement technologies:** Reyhan Aydogan (Özyeğin), Takayuki Ito & Rafik Hadfi (Kyoto — Hadfi is also PRIMA 2026 general chair), Katsuhide Fujita (TUAT), Miguel A. Lopez-Carmona (Alcalá).
- **Explainable/trustworthy MAS:** Davide Calvaresi (HES-SO; EXTRAAMAS organizer), Giovanni Ciatto (Bologna; XAI+MAS), Robert Wortham (Bath; transparency), Simona Tiribelli (Macerata; AI ethics).
- **Applied/industrial MAS:** Joaquin Delgado (Encevo), Eskandar Kouicem (Snowflake), Shiva Kumar Bhuram (Dorman Products), Kaustav Saha (Zscaler, publicity chair).
- **Public-sector/governance practitioners:** Munzir Alradi, Ayoub Alzahim (Saudi Ministry of Environment, Water and Agriculture).
- Core UTBM/Luxembourg/LIST/Umeå organizer networks plus Cameroon (Ngaoundere/Douala) and Tunisia contingents.

**Implication for authors:** The PC is dominated by *classical MAS + XAI + norms/negotiation* researchers, not by LLM-benchmark ML researchers. A submission framed as pure LLM engineering will meet reviewers who expect organizational/normative grounding, formal clarity, and socio-technical framing. Reviewers fluent in cascading-failure concepts from classical MAS/distributed systems exist; LLM-MAS failure dynamics expertise is thinner — an opportunity (less prior-art policing) and a risk (must explain LLM specifics accessibly).

### Host conference context (PRIMA 2026)
PRIMA 2026's stated vision is "Beyond Traditional MAS" — fusing classical MAS rigor with Generative/Agentic AI; areas include "Generative and Agentic AI", "Engineering Multi-Agent Systems", "Ethics, Society, and Governance". PRIMA main-track notification is 25 Sep 2026 (before MASO's 10 Oct deadline) — expect some MASO submissions to be redirected/extended PRIMA rejects. MASO registration requires PRIMA registration.

---

## 3. MASO relevance map — saturation grades

Grades: **A = heavily saturated** (crowded; hard to stand out), **B = active but open** (real literature, real gaps), **C = surprisingly underexplored** (thin archival evidence relative to CFP emphasis). Evidence column cites verified anchors or search probes. Probes marked [DC] = DataCite query (21 Sep 2026); negative results mean no relevant archival hits among top results, not proof of absence.

| # | Theme (assignment list) | CFP location | Grade | Evidence |
|---|---|---|---|---|
| 1 | Agent architectures / orchestration | Topic 1 | **A** | Survey saturation: Guo et al., "Large Language Model based Multi-Agents: A Survey of Progress and Challenges", arXiv:2402.01680 (verified); framework wars (AutoGen/CrewAI/LangGraph/MetaGPT). Generic orchestration is a crowded red ocean. |
| 2 | Agent composition | Topic 1 | **B** | Composition/mixture-of-agents active in ML venues; organizational-process composition less so. |
| 3 | Workflow management | Topic 1 | **B** | BPMN×MAS integration emerging (Najjar et al., "BPMN-Based Design of Multi-Agent Systems", *Information* 2025 — organizer's own work); classical BPM mature, LLM-agent workflow mgmt young. |
| 4 | Task decomposition | Topic 1 | **A** | Saturated in both classical planning/MAS and LLM prompting literatures. |
| 5 | Delegation | Topics 1, 4 | **B** | Classical trust/delegation theory (Castelfranchi–Falcone lineage) + A2A task delegation new. **In-repo occupation:** `maso/policy_preserving_delegation_research_proposal.md` already claims policy-preserving delegation + causal accountability across A2A/MCP. |
| 6 | Roles / specialization | Topic 1 | **A** | Role-play LLM MAS saturated (MetaGPT, ChatDev, role-assignment studies). |
| 7 | Agent lifecycle (state, resource mgmt) | Topic 1 | **C+** | Little archival LLM-era work on lifecycle/state/resource governance as an organizational concern; Emergence World (arXiv:2609.17320) shows persistent-operation issues (goal drift, memory contamination) but is not lifecycle management. |
| 8 | Heterogeneous agents | Topics 1, About | **B** | Mixed-model populations studied (Emergence World's mixed world; model-heterogeneity papers); active, open. |
| 9 | Agent-to-agent communication | Topic 2 | **A** | Protocol explosion 2025–26: A2A (Google→Linux Foundation, TSC incl. AWS/Cisco/IBM/Microsoft/Salesforce/SAP/ServiceNow — verified a2a-protocol.org), plus ANP/Agora etc. |
| 10 | Agent-to-system interoperability | Topic 2 | **A** | MCP (Anthropic open standard, verified modelcontextprotocol.io) ecosystem land-grab; standards work crowded. |
| 11 | Organizational coordination | Topic 3 | **B−** | Classical organizational MAS (AGR/Moise+) mature but pre-LLM; LLM-era organizational coordination thin → opening. |
| 12 | Distributed decision-making | Topic 3 | **A/B** | Classical MAS saturated; LLM-MAS distributed decisions active. |
| 13 | Negotiation / conflict resolution | Topic 3 | **A** | Deep classical literature; PC itself has a negotiation cluster (Aydogan, Ito, Hadfi, Fujita); LLM-negotiation papers numerous. |
| 14 | Coordination under uncertainty | Topic 3 | **A/B** | Classical Dec-POMDP etc. saturated; note in-repo killed candidate #5 (regret-grounded Dec-POMDP LLM teams). |
| 15 | Human–agent collaboration | Topic 4 | **A** | Decades of HAI/HRI + heavy LLM-era activity (142k OpenAlex hits 2023+ on loose probe — directionally saturated). |
| 16 | Human–agent delegation | Topic 4 | **B** | Adjustable autonomy classical; LLM-era trust/calibration active (Mualla's own work). |
| 17 | Decision rights (human↔agent allocation) | Topic 4 | **C** | Named in CFP; thin archival technical literature; mostly org-theory/governance prose. [DC probe "decision rights AI agents": no relevant archival hits] |
| 18 | Organizational memory | Topic 5 | **C** | Named in CFP; archival LLM-agent work on *organizational* memory nearly absent [DC probe: only grey Zenodo items]; closest is Emergence World's persistent-memory contamination finding. |
| 19 | Collaborative/shared memory | Topic 5 | **B** | Shared-memory architectures and memory-poisoning security work active. |
| 20 | Knowledge transfer / cross-agent learning | Topic 5 | **B** | Active (RAG, continual learning), organizational-knowledge framing thin. |
| 21 | Governance (agentic ecosystems) | Topic 6 | **B** | Very active policy discourse (EU AI Act; organizer Carli's work); technical governance mechanisms open. |
| 22 | Accountability | Topic 6 | **B** | Normative MAS classical (van der Torre lineage); LLM-MAS failure attribution emerging: Who&When, arXiv:2505.00212 (ICML'25 camera-ready; best method 53.5% agent-ID accuracy). |
| 23 | Responsibility / authority / liability | Topic 6 | **C+** | CFP-explicit; technical operationalization thin; mostly philosophy/law. |
| 24 | Regulatory / compliance | Topic 6 | **B** | Policy-heavy, EU-AI-Act-driven; technical compliance-checking open. |
| 25 | Reliability (robustness, resilience) | Topic 7 | **B** | Emerging fast: MAST failure taxonomy (arXiv:2503.13657, 14 failure modes, 1600+ traces); TRAIL trace-debugging benchmark (arXiv:2505.08638; best model 11%). |
| 26 | Safety | Topic 7 | **B/A** | Agentic-safety papers proliferating; adversarial angle especially (MAS-Shield, arXiv:2511.22924, EMNLP Findings 2026). |
| 27 | Privacy | Topic 7 | **B** | Privacy-preserving agent interaction active (organizers publish here). |
| 28 | **Systemic / cascading failures** | Topic 7 (verbatim) | **C** | **The seed's core.** Archival LLM-MAS work is thin and adversarial-skewed: MAS-Shield (defense vs linguistic attacks causing cascading failures); Emergence World (arXiv:2609.17320, 15 Sep 2026 — adversarial stress events in persistent 10-agent worlds; "detection did not ensure containment"). Organic-fault propagation dynamics, blast-radius measurement across organizational boundaries, and containment/recovery comparison: no archival hits [DC probes: "fault injection multi-agent LLM", "error propagation multi-agent collaboration", "containment failure AI agents", "blast radius AI agents" — no relevant archival results]. Classical cascading-failure literature (power grids, networks, distributed systems) predates LLMs and is mature — import opportunity. |
| 29 | Evaluation frameworks | Topic 8 | **B** | Many agent-eval frameworks; organizational-level evaluation open. |
| 30 | Benchmarks | Topic 8 | **A** | OSWorld (arXiv:2404.07972), TheAgentCompany (arXiv:2412.14161), GAIA, SWE-bench, WorkArena… crowded. |
| 31 | Organizational testbeds | Topic 8 | **C+** | TheAgentCompany simulates a software company but has no roles/authority/accountability structure or fault-injection apparatus; fault-injectable organizational testbeds absent [DC probes]. |
| 32 | Organizational productivity / cost / quality | Topic 8 | **C** | Named in CFP; thin beyond vendor ROI claims and single-firm studies. |
| 33 | Organizational design / socio-technical transformation | Topic 9 | **C+** | Org-theory side mature, agentic-AI empirical side nascent. |
| 34 | Enterprise / public-sector deployments | Topic 10 | **B−** | Case studies emerging, largely grey/industry literature; archival field experiments rare. PC includes public-sector practitioners → receptive audience. |

### Relevance-map summary
- **Most saturated (avoid as primary contribution):** generic architectures/orchestration, task decomposition, roles/specialization, A2A/MCP interoperability, negotiation, benchmarks, generic human-agent teaming.
- **Active but open (viable with a twist):** governance/accountability, reliability/failure-taxonomy-and-attribution, human-agent delegation, workflow management, safety/privacy, enterprise case studies.
- **Surprisingly underexplored (CFP-named but thin literature):** systemic/cascading failures (esp. organic faults + containment/recovery), organizational memory, decision rights, responsibility/authority operationalization, organizational testbeds with role/authority structure, organizational productivity/cost/quality metrics, agent lifecycle.

---

## 4. Implications for the seed hypothesis

1. **Fit is exact and explicit.** MASO's CFP is the rare venue that names "detection and mitigation of cascading, and systemic failures" verbatim, alongside organizational memory, decision rights, accountability, and organizational testbeds — the seed's full boundary list (role, communication, authority/delegation, tool, memory, accountability, human-agent) maps onto topics 1, 2, 4, 5, 6, 7, 8.
2. **The seed is NOT killed by existing literature.** The closest verified neighbors:
   - **MAST** (arXiv:2503.13657) — failure *taxonomy* from traces; no propagation dynamics, no organizational boundaries, no recovery.
   - **Who&When** (arXiv:2505.00212) — failure *attribution*; no containment/recovery; authors state attribution itself is unsolved (14.2% step-level accuracy).
   - **TRAIL** (arXiv:2505.08638) — trace *debugging* benchmark.
   - **MAS-Shield** (arXiv:2511.22924) — *adversarial* cascading-failure defense (prompt-infection style); not organic faults, not organizational.
   - **Emergence World** (arXiv:2609.17320) — closest in spirit: persistent multi-agent worlds, failure propagation through memory/tools/agents, detection≠containment. But: adversarial stress events, no role/authority/accountability structure, no systematic containment/recovery mechanism comparison, no task-utility-preservation trade-off. **It partially occupies "failure propagation in persistent LLM MAS" — the seed must differentiate on the *organizational* axis (roles, authority, accountability, human-agent boundaries) and on *recovery/containment mechanism evaluation*.**
3. **Reviewer-audience risk:** the PC is classical-MAS/XAI/norms-heavy. A blast-radius paper should import classical vocabulary (fault containment, error confinement, Byzantine/crash fault analogies, organizational theory) and formalize cleanly; pure LLM-empiricism framing is a mismatch risk.
4. **Format guidance:** 16-page full paper is realistic for a testbed+mechanism-comparison study; LNCS; double-blind; ≥2 reviewers (light review load — expect variable depth). Industry keynote + practitioner PC members reward deployment realism.
5. **Occupied territory to avoid:** in-repo delegation-invariants proposal (maso/policy_preserving_delegation_research_proposal.md) covers authority/policy preservation across A2A/MCP delegation chains — the seed's "authority/delegation boundary" must be treated as *blast-radius dimension*, not as delegation-invariant enforcement, to stay complementary.

---

## 5. Verified anchor papers (all inspected via arXiv abstract pages, 21 Sep 2026)

| Paper | ID | Venue/status | Relevance to seed |
|---|---|---|---|
| Why Do Multi-Agent LLM Systems Fail? (Cemri et al., UC Berkeley et al.) | arXiv:2503.13657 [cs.AI], v3 Oct 2025 | MAST taxonomy + MAST-Data (1600+ traces, 7 frameworks, 14 failure modes, κ=0.88) | Failure taxonomy only; no propagation/recovery |
| Which Agent Causes Task Failures and When? (Zhang et al.) | arXiv:2505.00212 [cs.MA], v3 Jun 2025 | authors' comment: "camera-ready" (venue not stated on abs page); Who&When dataset, 127 MAS failure logs | Attribution; best 53.5% agent / 14.2% step accuracy — attribution unsolved |
| TRAIL: Trace Reasoning and Agentic Issue Localization (Deshpande et al.) | arXiv:2505.08638 [cs.AI], v3 Jun 2025 | 148 annotated traces; best LLM 11% on trace debugging | Evaluation/debugging; no containment |
| MAS-Shield (Wang et al.) | arXiv:2511.22924 [cs.MA], v3 Sep 2026 | authors' comment: "EMNLP findings 2026"; 92.5% recovery vs adversarial linguistic attacks, 70% latency cut | Adversarial cascading-failure defense — nearest containment neighbor |
| Emergence World (Vempaty et al.) | arXiv:2609.17320 [cs.MA], v1 15 Sep 2026 | 8 worlds × 10 agents, 16 days, 850k LLM calls; 3 adversarial stress events; no world fully resilient; detection≠containment (memory contamination acted on 46h later) | **Closest neighbor** — propagation in persistent MAS, but adversarial + non-organizational |
| TheAgentCompany (Xu et al., CMU) | arXiv:2412.14161 [cs.CL], v3 Sep 2025 | Benchmark; simulated software company; best agent 30% autonomous task completion | Organizational-ish testbed without roles/authority/faults |
| OSWorld (Xie et al.) | arXiv:2404.07972 [cs.AI] | 369 real-computer tasks; best model 12.24% vs humans 72.36% (per abstract) | Benchmark saturation evidence |
| LLM-based Multi-Agents survey (Guo et al.) | arXiv:2402.01680 [cs.CL] | IJCAI 2024 survey | Architecture-saturation evidence |
| A2A Protocol | a2a-protocol.org (Linux Foundation; TSC: AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, ServiceNow) | — | A2A-communication saturation evidence |
| Model Context Protocol (MCP) | modelcontextprotocol.io (Anthropic open standard) | — | Interoperability-saturation evidence |

## 6. Limitations of this investigation
- arXiv API, Semantic Scholar, OpenAlex (daily budget), DBLP (Anubis bot-wall), Google/DuckDuckGo were rate-limited or blocked from this IP during the window; discovery relied on DataCite queries + direct arXiv abstract-page verification. Saturation grades for well-established fields rest on verified landmark anchors + organizer/PC evidence; grades for thin fields rest on negative DataCite probes (absence of archival hits among top results) — absence of evidence is not proof of absence, and synonym coverage, while broad (cascading/systemic failure, failure/error propagation, fault injection/tolerance, containment, blast radius, recovery), cannot be exhaustive.
- "Tentative" PC list may change before the workshop.
- Page-limit interpretation (position/practical → 8pp short) is inferred, not stated.
