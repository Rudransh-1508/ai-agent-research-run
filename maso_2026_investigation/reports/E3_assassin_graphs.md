# E3 Assassin Report — Killing the Seed via Graph/Provenance Formulations

**Investigator:** ASSASSIN E3
**Date:** 2026-09-21
**Assignment:** Search dependency graphs for agent failure analysis, causal traces, provenance-based recovery, data lineage + fault containment, influence graphs in MAS. Core question: *does anyone already formulate fault spread on a weighted graph of agents/roles/memory/tools/decisions?* Report the single most damaging paper.
**Seed hypothesis under attack:** "Organizational failure propagation and recovery in LLM multi-agent systems" — what determines the *organizational blast radius* of a local fault (spread across role, communication, authority/delegation, tool, memory, accountability, human-agent boundaries), and which containment/recovery mechanisms minimize systemic impact while preserving task utility.

---

## 0. Bottom-line judgment

**The seed is NOT killed, but it is badly surrounded.** No verified paper formulates fault spread on a weighted graph spanning the *organizational* boundary set (roles, authority/delegation, accountability, human-agent handoffs) with containment/recovery evaluated under task-utility preservation. However:

1. The **exact "blast radius" construct is already claimed** for agentic systems: *DamageFlow / BlastGuard* (ICML 2026 AIWILD workshop) defines a Blast Radius Score decomposed into resource sensitivity, action impact, **propagation**, and **recovery cost**, with a provenance-aware least-privilege capability-graph runtime that gates tool calls and preserves 87.5% benign utility. This is the single most damaging paper (Section 2).
2. The **graph formulation of fault spread/attribution in LLM-MAS is occupied territory as of mid/late 2026**: EDGE (error dependency graphs + counterfactual rollout, EMNLP 2026), AIG (adaptive influence graphs, Aug 2026), DepTracer (attribution dependency graphs with deterministic propagation, ACL ARR 2026 May), FAMAS (spectrum-based attribution, PACMSE 2026), DUOTRACE (cascade failure attribution, Aug 2026).
3. **Error propagation vs. communication topology, including suppression-versus-utility tradeoffs, is published**: Shen et al. (EMNLP 2025) explicitly analyze how erroneous outputs propagate under topology sparsity and design topologies that suppress error propagation *while preserving beneficial information diffusion* — i.e., containment-with-utility on the communication dimension.
4. **Fault injection + recovery-behavior evaluation for LLM-MAS exists**: MAS-FIRE (Feb 2026) injects 15 fault types into 3 MAS architectures and tiers fault-tolerant behaviors, showing topology (iterative closed-loop) neutralizes 40%+ of faults that collapse linear workflows.
5. **Transactional recovery (rollback/compensation) for multi-agent LLM planning exists**: SagaLLM (PVLDB 2025).

A MASO submission framed as "we model failure propagation on a graph of agents" or "we introduce blast radius for agentic systems" would be scooped. The defensible residue is the **organizational boundary semantics** (authority, delegation, accountability, human-agent decision rights) and **cross-boundary containment/recovery mechanisms** — which none of the verified works address — but the proposal must cite and differentiate from all of the above.

---

## 1. Method and sources

Search infrastructure status on 2026-09-21: Semantic Scholar API and arXiv API rate-limited (HTTP 429, shared-IP budgets); OpenAlex worked until its daily shared budget was exhausted; DBLP unreachable. Successful channels: **OpenAlex** (`title_and_abstract.search`, ~20 queries), **OpenReview API v2 search** (covers ICLR/ICML/NeurIPS/ACL-ARR submissions and workshop posters), **arXiv abstract pages** (direct verification), **ACL Anthology** (direct verification), **Crossref** (DOI verification for classical works), **GitHub** (code availability).

Every load-bearing paper below was verified by inspecting its actual arXiv abstract page, ACL Anthology page, OpenReview record, or Crossref record — not search snippets. Queries covered: failure/error/hallucination propagation in multi-agent (LLM) systems; failure attribution (spectrum-based, causal, graph-based); contagious/recursive/prompt-infection attacks; topological safety/defense; blast radius; provenance-based recovery; lineage fault recovery; checkpoint/rollback/domino effect; cascading failures (classical and LLM); self-healing/quarantine/circuit-breaker containment; organizational failure models.

Synonym/adjacent-field sweeps (per mission rules): microservices root-cause analysis (causal/dependency graphs), distributed-systems rollback recovery, data lineage (Spark RDD), network science (cascading failures, influence maximization), control-theoretic MAS (containment control, fault-tolerant consensus), classical organizational MAS models (MOISE).

---

## 2. THE SINGLE MOST DAMAGING PAPER

### "What Can One Bad Tool Call Destroy? Measuring and Minimizing Blast Radius in Agentic Tool Use" (DamageFlow + BlastGuard)

| Field | Value |
|---|---|
| Authors | Muhammet Anil Yagiz (single author) |
| Venue | ICML 2026 AIWILD workshop (OpenReview forum `MYvsxnxbCf`) |
| URL | https://openreview.net/forum?id=MYvsxnxbCf |
| Problem | Binary attack-success evaluation hides radically different operational damage; agent safety evaluation should measure *how far failure spreads*, not just whether it occurs |
| Method | **DamageFlow** benchmark: sandboxed email, documents/RAG, repository, MCP-style registry environments (calendar/CRM/filesystem extensions specified); deterministic **state-diff oracles** scoring committed tool effects. Metric: **Blast Radius Score (BRS)** decomposing unauthorized tool effects by *resource sensitivity, action impact, propagation, recovery cost*. Defense: **BlastGuard**, a **provenance-aware runtime** compiling trusted user intent into **least-privilege capability graphs**, tracking untrusted context flow, gating state-changing tool calls via dry-run, policy checks, scoped tokens, and **rollback logs** |
| Experimental setting | 80-scenario controlled pilot; threats: indirect prompt injection, MCP tool poisoning, tool shadowing, **multi-agent relay attacks** |
| Metrics | BRS (composite), committed unauthorized damage, benign task utility, counterfactual "prevented BRS at the tool boundary" |
| Major findings | Two agents with identical 20% attack-success rate differ by **89× in BRS**; BlastGuard reduces committed unauthorized damage while retaining **87.5% benign task utility** |
| Author-stated scope | Pilot-scale; safety/attack framing |
| My inferred limitations | Workshop paper, single author, small pilot; fault model is *adversarial* (prompt injection/tool poisoning), not organic organizational faults; boundaries are tool/resource boundaries, not organizational role/authority/accountability boundaries; no human-agent escalation semantics; no cross-organization setting |
| Code | Not linked in the OpenReview record inspected (PDF attachment only) |
| **Relation to seed** | **Occupies the "blast radius" term, the propagation+recovery-cost metric decomposition, provenance-based containment, and utility-preserving defense for agentic systems.** Any MASO paper using "organizational blast radius" must cite and differentiate this. It does NOT cover: non-adversarial faults, organizational role/authority/accountability boundaries, human-agent handoffs, or weighted graphs over roles/memory/decisions |

**Why this is the most damaging:** it is the only verified work that (a) uses the seed's headline construct ("blast radius"), (b) decomposes it into propagation and recovery cost, (c) implements provenance/capability-graph containment, and (d) demonstrates utility preservation — four of the seed's pillars — albeit in a security rather than organizational-fault frame.

---

## 3. Evidence table A — Graph/provenance formulations of fault spread & attribution in LLM-MAS (the "occupied graph" cluster)

| Paper | Venue/ID (verified) | What it does | Relation to seed |
|---|---|---|---|
| **EDGE: Error Dependency Graph-Guided Multi-Error Attribution in Multi-Agent LLM Systems** — Jun Hou, Priya Pitre, Yi Fang, Xuan Wang | EMNLP 2026; arXiv:2609.01360 (1 Sep 2026) | Constructs an **error dependency graph** from observed error events; validates a causal subset via **counterfactual rollout**; two-stage LLM-as-judge attribution; intervention-validated subgraph supports "explanation and **repair analysis**". Evaluated on TRAIL and MAST | Directly formulates failure analysis as a graph over error events with causal validation. Occupies "fault spread as dependency graph" for attribution; does not model organizational boundaries or containment mechanisms |
| **Adaptive Influence Graphs (AIGs) for Failure Attribution in Multi-Agent Systems** — Bakish, Dudai, Ganz, Nuriel, Ben Avraham, Shpigel Nacson, Litman | arXiv:2608.24361 (25 Aug 2026) | Transforms a failed trace into a **structured influence graph** (components, actions, dependencies), then agent-directed traversal to find the critical error. SOTA on Who&When | Occupies "influence graph over agent traces" — the exact phrase in my assignment. Attribution only; no recovery/containment |
| **DepTracer: Propagation-Aware Failure Attribution for Agentic Optimization** (anon.) | ACL ARR 2026 May submission (OpenReview `lzyB79SJVL`) | Builds a **trajectory-grounded attribution dependency graph**; **deterministic attribution propagation** computes continuous scores over segments/steps; feeds closed-loop optimizers (+10.16pp on GEPA vs +2.16pp single-pass) | "Propagation-aware" attribution on a dependency graph, explicitly motivated by repair/optimization. Closest to linking spread-analysis → repair, but no organizational semantics, no containment |
| **FAMAS: Spectrum-Based Failure Attribution for MAS / "Who is Introducing the Failure?"** — Yu Ge, Linna Xie, Zhonghui Li, Yu Pei, Tian Zhang | PACMSE 2026 (DOI 10.1145/3797113); arXiv:2509.13782 (17 Sep 2025) | Systematic **trajectory replay** + abstraction + spectrum analysis (software-fault-localization style suspiciousness) over agent/action activation patterns; beats 12 baselines on Who&When | Imports classical spectrum-based fault localization into LLM-MAS. Attribution, not propagation modeling or containment |
| **DUOTRACE: Detect Before You Attribute — Cascade Failure Attribution for MAS** — Jiayi Zhang et al. | arXiv:2608.29646 (30 Aug 2026) | VAE anomaly detection over dual-view semantic-structural node representations + Tree-LSTM trajectory encoder; "detect-before-attribute" filter; +8.7% agent-level, +7.0% step-level attribution | Title claims "cascade failure attribution"; exploits trajectory **topology**; still localization, not spread modeling or containment |
| **A2P (Abduct-Act-Predict) Scaffolding** — West, Weng, Zhu, Lin, Ning, Zhang | arXiv:2509.10401 (12 Sep 2025) | Causal-inference scaffolding for failure attribution: abduction → minimal corrective intervention → counterfactual trajectory simulation. 47.46% step accuracy on Who&When Algorithm-Generated (2.85× baseline). Code released | Counterfactual "would fixing X have averted failure" — causal traces, but single decisive-error framing, no spread graph |
| **Which Agent Causes Task Failures and When? (Who&When)** — Shaokun Zhang, Ming Yin, Jieyu Zhang, et al. | **ICML 2025 Spotlight** (OpenReview `GazlTYxZss`); code: github.com/mingyin1/Agents_Failure_Attribution | Task formulation + benchmark: 184 annotated failure logs (algorithm-generated via CaptainAgent; hand-crafted Magnetic-One); who/when/explanation annotations; GAIA/AssistantBench queries | Defines the failure-attribution task the graph methods above build on |
| **TRAIL: Trace Reasoning and Agentic Issue Localization** — Deshpande et al. | arXiv:2505.08638 (13 May 2025); dataset+code public | Formal error taxonomy + 148 human-annotated single- and multi-agent traces (SWE, open-world IR); best model (Gemini-2.5-pro) scores 11% | Trace-level error localization benchmark; substrate for graph methods |
| **Seeing the Whole Elephant / TraceElephant** — Mengzhuo Chen et al. | ACL 2026 Long, pp. 19888–19905 (10.18653/v1/2026.acl-long.912) | Failure-attribution benchmark with **full execution observability** (inputs+context, reproducible environments); full traces improve attribution up to 76.5% | Establishes full-trace observability as the attribution setting |
| **AgentRx** — Barke, Goyal, Khare, Singh, Nath, Bansal | EMNLP Findings 2026; arXiv:2602.02475 (2 Feb 2026) | 170 annotated failed trajectories, 11 task settings (API workflows, incident management); constraint-synthesis + validation log + LLM judge; +75% step localization | Diagnosis framework; incident-management setting overlaps "organizational" flavor but no spread/containment model |
| **MAST / Why Do Multi-Agent LLM Systems Fail?** — Cemri, Pan, Yang, …, Zaharia, Gonzalez, Stoica | arXiv:2503.13657 (v1 17 Mar 2025); MAST-Data public | 14 failure modes in 3 categories; 1600+ annotated traces across 7 frameworks | The canonical failure taxonomy; vocabulary substrate, not a graph/spread model |

**Cluster verdict:** by September 2026, "build a graph over agent execution and reason about failure on it" is a *crowded, benchmarked, venue-published* research line (EMNLP 2026, ACL 2026, PACMSE 2026, ICML 2025). The seed cannot claim novelty for graph-based fault-spread formulation per se.

---

## 4. Evidence table B — Error/information propagation dynamics on agent communication graphs

| Paper | Venue/ID (verified) | What it does | Relation to seed |
|---|---|---|---|
| **Understanding the Information Propagation Effects of Communication Topologies in LLM-based MAS** — Xu Shen, Yixin Liu, Yiwei Dai, Yili Wang, Rui Miao, Yue Tan, Shirui Pan, Xin Wang | **EMNLP 2025 main**, pp. 12347–12361 (10.18653/v1/2025.emnlp-main.623) | **Causal framework** for how correct/erroneous agent outputs propagate under topology sparsity; finds moderately sparse topologies suppress error propagation while preserving beneficial diffusion; proposes **EIB-Learner** topology design balancing error suppression vs beneficial information flow | **Occupies "what determines spread + how to contain it while preserving utility" on the communication dimension.** No roles/authority/memory/accountability; topology-only |
| **Hallucination Cascade: Analyzing Error Propagation in Multi-Agent LLM Systems** — Jamshidi, Moradi Dakhel, Nafi, Khomh | arXiv:2606.07937 (6 Jun 2026) | Claim-level factual-inconsistency tracking across sequential agent interactions; 500 cascade experiments, 10 domains, GPT-5.3/DeepSeek-V3/LLaMA-3-70B; finds net *attenuation* (amplification factor 0.644) with factual-accuracy tradeoff | Quantifies error spread vs cascade depth and model heterogeneity; sequential chains only, no organizational structure, no containment |
| **When Truth Is Distributed (ForesightSafety-TIDE)** — Chenfei Yan et al. | arXiv:2608.03421 (v3 13 Aug 2026) | Paired honest/deceptive conditions in 120 five-agent environments; analyzes multi-stage voting, testimony adoption, and **evidence-root lineage propagation**; truth recovery falls 72.5%→14.17% under one deceiver; false testimony persists after deceiver exits | Uses *lineage propagation* of evidence — provenance-flavored spread analysis; deception-focused, no recovery mechanisms |
| **Beware of the Woozle Effect: Hallucination Propagation in Multi-Agent Debate** — Zhiheng Zhang et al. | IEEE/ACM TASLP 2026 (10.1109/TASLP.2026.3675803) | Identifies and mitigates hallucination propagation in multi-agent debate | Debate-only spread dynamics |
| **Phase Transition for Budgeted Multi-Agent Synergy** — Bang Liu, Linglong Kong, Jian Pei | arXiv:2601.17311 (2026) | Minimal theory: compute-performance exponent β, message-fidelity γ(m), **shared-error correlation ρ**, context fan-in W ⇒ hierarchy necessity; predicts help/saturate/collapse regimes | Theoretical model of correlated failure in agent hierarchies; abstract, no containment |
| **Infodeme: Structural Determinants of Misinformation Propagation in LLM Agent Societies** — Shakib Howlader | OSF preprint 2026 (osf.io/3fxqn) | 75-agent society, 765 trials, 3×3 factorial over hierarchy, memory depth, network structure; misinformation propagation + spontaneous correction | Hierarchy/memory/network effects on spread — touches role-ish structure but misinformation sims, no containment/utility |

---

## 5. Evidence table C — Contagion attacks and topology-based defenses (adversarial spread)

| Paper | Venue/ID (verified) | What it does | Relation to seed |
|---|---|---|---|
| **NetSafe: Exploring the Topological Safety of Multi-agent Networks** — Miao Yu, Shilong Wang, Guibin Zhang, et al. | arXiv:2410.15686 (21 Oct 2024) | RelCom framework unifying agent frameworks; studies which topological properties resist misinformation/bias/harmful-content spread; highly connected networks more susceptible (Star −29.7%); static metrics predicting dynamic safety | "What topological properties determine spread" — a blast-radius determinant study on the communication graph; attack-focused |
| **G-Safeguard: Topology-Guided Security Lens and Treatment** — Shilong Wang, Guibin Zhang, Miao Yu, et al. | **ACL 2025 Long** (10.18653/v1/2025.acl-long.359); arXiv:2502.11127; code public | GNN anomaly detection on the **multi-agent utterance graph** + **topological intervention for attack remediation**; recovers >40% performance under prompt injection | **Graph-based detection + containment-by-topological-intervention** — occupies graph containment machinery; adversarial scope |
| **TMCHT / "A Troublemaker with Contagious Jailbreak Makes Chaos in Honest Towns"** — Tianyi Men et al. | **ACL 2025 Main**; arXiv:2410.16155 | Multi-topology (line/star/100-agent) attack framework; Adversarial Replication Contagious Jailbreak (ARCJ) with retrieval+replication suffixes; "toxicity disappearing" phenomenon in non-complete graphs | Contagion across agent society topologies via memory retrieval |
| **CORBA: Contagious Recursive Blocking Attacks** — Zhenhong Zhou et al. | **ACL 2026 Findings**, pp. 6899–6908 (10.18653/v1/2026.findings-acl.342) | Formalizes **Denial-of-Collaboration (DoC)**: attacks corrupt collaborative structure, turning communication topology into self-sabotage; semantically benign contagious instructions cause paralysis across topologies/models | Failure spread *of the collaboration structure itself*; attack, no recovery |
| **Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems** — Dong-Hyun Lee, Mansi Tiwari, Brando Miranda | arXiv:2410.07283 (9 Oct 2024); LNCS version 2026 (10.1007/978-3-032-16092-8_28) | Self-replicating malicious prompts propagating agent-to-agent "like a computer virus"; LLM Tagging defense | The canonical "infection spread in MAS" paper |
| **MPAS: Individual-Epistemic Message Propagation** — J.-F. Yu et al. | **AAAI 2026** (10.1609/aaai.v40i35.40231) | Node-wise message propagation breaking DAG sequential constraints; notes backdoor vulnerability of sequential topologies | Topology/robustness interplay |
| **AgentPoison** — Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, Bo Li | NeurIPS 2024; arXiv:2407.12784 | Red-teaming via memory/knowledge-base poisoning | Memory-boundary corruption (adjacent to memory blast radius) |
| **Memory-poisoning follow-ups** | MINJA robustness study arXiv:2601.05504 (2026); Temporal Dynamics of Memory Poisoning, IEEE Access 2026 | Attack/defense evaluation for persistent agent memory | Memory as a propagation surface |
| **Agents of Chaos** — Shapira et al. (33 authors) | arXiv:2602.20021 (23 Feb 2026) | 2-week live red-team of autonomous agents with memory/email/Discord/shell; documents **cross-agent propagation of unsafe practices**, partial system takeover; raises accountability/delegated-authority questions | Empirical evidence of organizational-flavored spread; case studies, no formal model |

---

## 6. Evidence table D — Containment & recovery mechanisms for LLM(-MA) workflows

| Paper | Venue/ID (verified) | What it does | Relation to seed |
|---|---|---|---|
| **SagaLLM: Context Management, Validation, and Transaction Guarantees for Multi-Agent LLM Planning** — Edward Yi Chang, Longling Geng | **PVLDB 2025** (10.14778/3750601.3750611) | Saga transactional pattern + persistent memory + **automated compensation (rollback)** + independent validation agents for multi-agent LLM workflows | **Occupies transactional recovery/compensation in multi-agent LLM planning.** No blast-radius model; consistency-focused |
| **MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based MAS** — Jin Jia, Zhiling Deng, Zhuangbin Chen, Yingqi Wang, Zibin Zheng | arXiv:2602.19843 (23 Feb 2026) | Taxonomy of **15 fault types** (intra-agent cognitive + inter-agent coordination); 3 non-invasive injection mechanisms (prompt modification, response rewriting, **message routing manipulation**); 3 architectures; **four tiers of fault-tolerant behavior** (mechanism, rule, prompt, reasoning); iterative closed-loop topologies neutralize >40% of faults that collapse linear workflows | **The closest methodological template for the seed's experiments** (fault injection + propagation + recovery behavior + topology). It is evaluation/diagnosis, not an organizational blast-radius theory or containment design |
| **"The Economics of Recovery: Measuring What Retry, Rollback, and Escalation Buy in Long-Horizon LLM Agent Workflows" (Keel)** — Zhouran Song | Manuscript under review 2026; artifacts on Zenodo (10.5281/zenodo.22757813) | Event-sourced runtime logging every call/verification/retry/**checkpoint/rollback/escalation** with cost; ~41k model calls | Recovery-mechanism cost-benefit (retry/rollback/escalate) — single-agent workflows, economic framing |
| **SAMC: State-Aligned Micro-Checkpointing** — D. Vengadesh | Zenodo 2026 (10.5281/zenodo.19682952) | Unified state model (LLM engine + workflow + environment) with micro-checkpoint capture protocol | Checkpoint/recovery systems machinery |
| **Self-healing frameworks for LLM agents** — C. Jeong, Younggun Shin | arXiv:2605.06737 (2026); journal version IJSEKE 2026 | Failure taxonomy + reliability assessment + detection + automated recovery | Single-agent self-healing |
| **FTDI: budget-aware self-healing for LLM multi-agent code generation** — Sixue Men et al. | Expert Systems with Applications 2026 (10.1016/j.eswa.2026.134164) | Budget-aware fault-tolerant detection/intervention for multi-agent codegen | Domain-specific recovery |
| **PurgeBench** — T. Munirathinam | Zenodo 2026 (10.5281/zenodo.21379140) | Benchmark for adversarial **memory-poison recovery**: Recovery-Completeness = HM(eradication, **utility retention**) × re-emergence resistance; degenerate wipe scores zero | Recovery-with-utility-retention metric for the memory boundary |
| **Agentic Neural Networks / textual backpropagation** — (EvoMAC line) | ACL 2026 Findings; CoRR 2025 | Self-evolving MAS via textual backpropagation of errors | Error-driven self-repair, not containment |
| **Adaptive Semantic Gates (ASG)** — Castro et al. | ICCE 2026 (10.1109/ICCE67443.2026.11449653) | Runtime semantic-drift monitor blocking high-risk actions in multi-agent execution | Runtime containment gate (shallow) |

---

## 7. Evidence table E — Adjacent fields (prior art the seed must acknowledge)

| Work | Venue/ID (verified) | Relevance |
|---|---|---|
| **Microservices causal-graph RCA cluster**: Chain-of-Event (weighted event causal graph, KDD-ish 2024, 10.1145/3663529.3663827); MULAN (multi-modal causal structure learning, WWW 2024, 10.1145/3589334.3645442); Neural Granger RCA (AAAI 2024, 10.1609/aaai.v38i1.27772); TraceDiag (2023, 10.1145/3611643.3613864); **GALR** (graph RCA + **LLM-assisted recovery**, Electronics 2026, 10.3390/electronics15010243); **GALA+** (graph-augmented LLM agents for RCA + incident response, arXiv:2608.08968) | Mature literature formulating fault localization/propagation on **dependency/causal graphs of services**, increasingly with LLM agents and recovery. The seed's "weighted graph of components with fault spread" exists here — for microservices, not organizations of agents |
| **Rollback-recovery / domino effect**: Venkatesh et al. 1987 (10.1016/0020-0190(87)90203-1); Baldoni/Helary/Mostefaoui/Raynal 1995; Venkatesan 1997 (10.1109/71.584092); **Elnozahy et al., "A survey of rollback-recovery protocols in message-passing systems," ACM Computing Surveys 2002 (10.1145/568522.568525)** | Classical formulation of failure-propagation containment: the domino effect *is* uncontrolled cascading rollback; checkpointing protocols are containment mechanisms. 40-year-old prior art for "containing fault spread in distributed agent systems" |
| **Lineage-based recovery**: Spark RDDs (Zaharia et al., NSDI 2012); write-ahead lineage for pipelined query engines (CoRR 2024, OpenReview `fRrkDwlDxp`) | **Provenance/lineage-based fault recovery is a solved-pattern in data systems**: recompute lost partitions from the lineage DAG. The seed's "provenance-based recovery" must differentiate from this |
| **Cascading failures in networks**: Buldyrev et al., "Catastrophic cascade of failures in interdependent networks," Nature 2010 (10.1038/nature08932); Kempe/Kleinberg/Tardos influence maximization, KDD 2003 (10.1145/956750.956769); "Failure Propagation Graphs" for power networks (IEEE Systems J. 2025) | Spread-on-weighted-graph theory predates LLMs by decades; "blast radius" ≈ cascade size/expected influence |
| **Classical MAS containment**: Hines & Talukdar, "Controlling cascading failures with cooperative autonomous agents," Int. J. Critical Infrastructures 2006 (10.1504/IJCIS.2007.011551); fault-tolerant containment control (IEEE TNNLS 2023); contagious-fault resilience via "social distancing" in robotic MAS (INCOSE 2026, 10.1002/iis2.70247); uncrewed-swarm cross-layer failure diffusion modeling (RESS 2025, 10.1016/j.ress.2025.110831); MAPF blame attribution via Shapley values (Natan/Stern/Kalech 2023, 10.3233/FAIA230462) | Non-LLM MAS already studies cascading-failure containment by autonomous agents, contagion mitigation, and blame assignment |
| **Organizational MAS models**: MOISE (organizational model: roles/groups/missions); organizational-modeling literature (COIN/AAMAS line) | Role/authority structure formalisms exist classically — the seed can reuse them, but they predate LLMs |
| **"Failure Isolation and Blast Radius Control in Large-Scale Distributed Systems"** — Sirikonda et al. | 2026, DOI 10.29284/mkwrh621 (low-tier venue) | Uses "blast radius" + fault-containment boundaries (service/host/zone/region/**organizational**) for microservices ops. Terminology prior art, weak venue |
| **Risk Analysis Techniques for Governed LLM-based MAS** — Reid, O'Callaghan, Carroll, Caetano (Gradient Institute) | arXiv:2508.05687 (6 Aug 2025) | Organizational risk framing: six failure modes incl. **cascading reliability failures**, monoculture collapse; staged-validity methodology | Closest *organizational* framing of cascading failure in LLM-MAS; a toolkit/report, no graph formalism or containment evaluation |

---

## 8. Kill assessment — does anything here kill or subsume the seed?

**No single paper subsumes the seed.** The conjunction the seed requires — (a) fault spread modeled on a weighted graph whose nodes/edges span *organizational* constructs (roles, authority/delegation, accountability, human-agent boundaries, tools, memory), (b) determinants of spread ("blast radius") identified across those boundary types, (c) containment/recovery mechanisms compared under systemic-impact-vs-task-utility tradeoffs — is not present in any verified work.

**But each conjunct is individually occupied:**

| Seed pillar | Occupied by | Verdict |
|---|---|---|
| "Blast radius" as the headline metric for agentic failure | **DamageFlow/BlastGuard (ICML 2026 AIWILD)**; also distributed-systems usage | **Term + metric decomposition taken.** Seed must cite and differentiate (organizational vs security faults) or rename |
| Fault spread on a graph of agents/errors | **EDGE, AIG, DepTracer, FAMAS, DUOTRACE** (2025–2026) | **Graph formulation alone is not novel** |
| What determines spread (topology/structure) | **Shen et al. EMNLP 2025; NetSafe; Hallucination Cascade; TIDE; Phase-Transition theory** | Communication-topology determinants well studied; other boundary types open |
| Containment via graph intervention | **G-Safeguard** (topological intervention); service-mesh/microservices practice | Graph-based containment machinery exists (adversarial scope) |
| Recovery mechanisms (rollback/compensation/checkpoint) | **SagaLLM (PVLDB 2025)**; Keel; SAMC; classical domino-effect literature | Recovery machinery exists; not evaluated against organizational blast radius |
| Fault-injection methodology for LLM-MAS | **MAS-FIRE** | Experimental template exists — seed should build on/cite it |
| Organizational boundary semantics (authority, accountability, human-agent) | Only **Gradient Institute risk report** (conceptual) and **Agents of Chaos** (anecdotal); delegation-invariants territory occupied by the sibling MASO proposal | **This is the defensible residue** |

**Residual risk to the seed:** a reviewer reading DamageFlow + EDGE + MAS-FIRE + Shen et al. could conclude the seed is an incremental recombination ("apply MAS-FIRE-style injection to an organizational graph and measure DamageFlow-style blast radius"). The seed survives only if the *organizational boundary layer* (authority/delegation semantics, accountability assignment, human-agent decision rights, cross-organization memory) does real work — e.g., showing that containment optimal on the communication graph is suboptimal on the authority graph, or that accountability constraints change recovery choices. Note the sibling proposal (`maso/policy_preserving_delegation_research_proposal.md`) already occupies delegation invariants + causal accountability across A2A/MCP chains — the seed must not drift into that territory.

---

## 9. Search-log and verification notes

- All arXiv IDs above were verified by loading the abstract page (title/authors/date/abstract match). ACL/EMNLP/PVLDB/AAAI/ICML venues verified via ACL Anthology pages, OpenReview records, or Crossref. OpenAlex-derived items not independently re-verified are marked with their DOIs (Crossref-resolvable).
- Semantic Scholar API, arXiv API, and DBLP were rate-limited/unreachable during the sweep; OpenAlex daily budget exhausted mid-sweep. Coverage gap: I could not exhaustively crawl ICLR 2027 submissions or very recent (Sept 2026) arXiv cs.MA listings; a final pre-submission re-check of arXiv cs.MA/cs.AI September–October 2026 for "blast radius", "failure propagation", "containment" is recommended.
- Killed-candidate list and sibling-proposal boundary respected; no overlap found between this report's cluster and the five previously killed candidates.
