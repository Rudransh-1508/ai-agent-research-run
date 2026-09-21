# B15 — Evaluation Metrics for Agentic Systems: Landscape Report

**Investigator:** Landscape B15 (evaluation metrics for agentic systems)
**Date:** 21 September 2026
**Mission question:** Map the agent-evaluation metric landscape (the two anchor surveys + 2025–2026 metric work on reliability, process/trajectory evaluation, LLM-as-judge validity) and answer: **is there any established metric for failure SPREAD, containment latency, or recovery quality in multi-agent systems (MAS)?**

**Verification method:** Every cited work was verified against its primary record — arXiv abstract pages (fetched in full), Crossref metadata, DataCite DOI records, Semantic Scholar metadata, or Zenodo API records. No citation rests on search snippets alone. Semantic Scholar search API and DBLP were heavily rate-limited/blocked from this host; discovery was done via DataCite (covers all arXiv DOIs), Crossref, and direct arXiv abstract-page fetches.

---

## 1. Bottom line

1. **Mainstream agent evaluation has NO metric for failure spread, containment latency, or recovery quality.** Both anchor surveys, and every credible benchmark examined, measure: end-task success, cost/steps, reliability-as-consistency (pass^k), process/milestone credit, judge agreement, safety/policy compliance, and post-hoc failure *attribution*. None measure how far a fault propagates, how fast it is contained, or how well the system recovers.
2. **The exact metric vocabulary of the seed hypothesis already exists — in one weak-venue 2026 paper.** *Containing the Cascade* (ICERA 2026) explicitly proposes **containment rate, cascade depth, blast radius, and mean time-to-detection** for tool-using LLM MAS, plus a fault-injection testbed (Cascade-Bench) and a mediator (Sentinel). This is a direct novelty threat that must be cited and differentiated (venue quality, simulation-only, no organizational boundaries, preprint deleted from Zenodo for copyright).
3. **Spread dynamics are studied almost exclusively in the adversarial (attack) framing** — infectious jailbreak (Agent Smith), LLM-to-LLM prompt infection, propagation-aware remediation (PropGuard), topology-guided intervention (G-Safeguard) — with metrics like attack success rate and performance-recovery-%, not organizational blast radius of *organic* faults.
4. **Recovery is measured only as single-agent repair rate** (AgentTether) or claimed qualitatively (self-healing framework, low-tier journal). Classical dependability concepts (fault→error→failure chain, MTTR/MTTD, chaos engineering, Byzantine fault tolerance, cascading-failure network science) exist but have not been operationalized as LLM-MAS metrics.
5. A self-published September 2026 position paper (Mahendrakar, Zenodo) explicitly argues that current failure-attribution benchmarks **cannot** measure containment — direct evidence the gap is recognized but unfilled.

**Verdict for the seed hypothesis:** Not killed. Partially scooped on *metric names* by one low-credibility paper; the rigorous, real-LLM, organizationally-structured version of "blast radius / containment / recovery" measurement remains open.

---

## 2. Anchor survey #1 — verified

| Field | Value |
|---|---|
| Title | A Survey on Evaluation of LLM-based Agents |
| Authors | Asaf Yehudai, Lilach Eden, Alan Li, Guy Uziel, Yilun Zhao, Roy Bar-Haim, Arman Cohan, Michal Shmueli-Scheuer |
| Year/venue | 2025 (v1, arXiv, 20 Mar 2025); v2 Apr 2026; published **Findings of ACL 2026** |
| IDs | arXiv:2503.16416 · DOI 10.18653/v1/2026.findings-acl.1330 · https://arxiv.org/abs/2503.16416 |
| Problem | First comprehensive survey of evaluation methods for LLM-based agents |
| Method/scope | Five-perspective taxonomy: (1) core capabilities (planning, tool use); (2) application benchmarks (web, SWE); (3) generalist agents; (4) benchmark core dimensions; (5) evaluation frameworks/tools for developers |
| Findings | Trend toward realistic, continuously updated benchmarks; **identified gaps: cost-efficiency, safety, robustness, and fine-grained scalable evaluation** |
| Author-stated gaps | Cost-efficiency, safety, robustness under-assessed; fine-grained scalable methods missing |
| Inferred limitations | Survey only; no new metrics; multi-agent failure dynamics not a focus |
| Relation to seed | Confirms the mainstream metric canon (success/cost/capability) and explicitly flags robustness/safety as gaps; contains no spread/containment/recovery metric |

## 3. Anchor survey #2 — verified

| Field | Value |
|---|---|
| Title | Evaluation and Benchmarking of LLM Agents: A Survey |
| Authors | Mahmoud Mohammadi, Yipeng Li, Jean-Pierre Lo, Wendy Yip |
| Year/venue | 2025, **KDD 2025** (Proc. 31st ACM SIGKDD, V.2), 3 Aug 2025 |
| IDs | DOI 10.1145/3711896.3736570 · arXiv:2507.21504 · DBLP conf/kdd/MohammadiLLY25 |
| Problem | Agent evaluation is "complex and underdeveloped"; fragmented landscape |
| Method/scope | Two-dimensional taxonomy: **evaluation objectives** (behavior, capabilities, reliability, safety) × **evaluation process** (interaction modes, datasets/benchmarks, metric computation, tooling) |
| Findings | Highlights **enterprise-specific challenges**: role-based data access, need for reliability guarantees, dynamic long-horizon interaction, compliance — "often overlooked in current research" |
| Author-stated gaps | Holistic, more realistic, scalable evaluation needed |
| Inferred limitations | Reliability treated as an objective category, not as propagation/containment; no MAS failure-spread metrics |
| Relation to seed | Its enterprise-reliability framing is adjacent to the seed's organizational framing, but it catalogs no spread/containment/recovery metric — supports the gap claim |

---

## 4. The 2025–2026 metric landscape (verified)

### 4.1 Reliability metrics (consistency over repeated trials)

| Paper | ID / venue | Metric(s) | Setting | Key findings | Limitations | Relation to seed |
|---|---|---|---|---|---|---|
| τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (Yao et al., Sierra) | arXiv:2406.12045, Jun 2024 | **pass^k** (probability all k trials succeed) — the canonical *reliability-as-consistency* metric; final-DB-state comparison | Simulated retail/airline tool-agent-user conversations | gpt-4o <50% success; pass^8 <25% retail | Single agent; reliability = cross-run consistency, not fault tolerance; no propagation notion | Defines "reliability" in agent-land as consistency — orthogonal to blast radius |
| τ²-bench: Evaluating Conversational Agents in a Dual-Control Environment (Sierra) | arXiv:2506.07982, Jun 2025 | pass^k; ablation separating **reasoning vs communication/coordination errors** | Telecom dual-control Dec-POMDP; compositional task generator | Large drops from no-user to dual-control | Still outcome-anchored; two-party only | Error-source decomposition is the closest mainstream thing to failure localization; no spread metric |

### 4.2 Process / trajectory evaluation

| Paper | ID / venue | Metric(s) | Setting | Key findings | Limitations | Relation to seed |
|---|---|---|---|---|---|---|
| Agent-as-a-Judge: Evaluate Agents with Agents (Zhuge et al., Meta) | arXiv:2410.10934, Oct 2024 | Intermediate step-wise reward signals; requirement-wise credit | DevAI benchmark (55 AI-dev tasks, 365 hierarchical requirements), code generation | Matches human baseline; beats LLM-as-a-Judge | Single-agent dev tasks; judge reliability itself unvalidated beyond agreement | Process credit assignment, not failure propagation |
| TRAIL: Trace Reasoning and Agentic Issue Localization (Deshpande et al.) | arXiv:2505.08638, May 2025 (v3 Jun 2025) | Trace-debugging accuracy over formal error taxonomy | 148 human-annotated traces, single+multi-agent, SWE & info-retrieval | Best model (Gemini-2.5-pro) scores **11%** | Post-hoc localization on completed traces; small dataset | Diagnosis-after-the-fact; explicitly not containment |
| MultiAgentBench (MARBLE) (Zhu et al., UIUC) | arXiv:2503.01935, Mar 2025 | **Milestone-based KPIs** for collaboration/competition quality; task score | Diverse interactive scenarios; star/chain/tree/graph coordination protocols | gpt-4o-mini highest avg task score; graph topology best in research scenario; cognitive planning +3% milestone rate | KPIs measure coordination quality, not fault behavior | Coordination-quality metrics exist; failure-spread metrics absent |
| Who&When: Which Agent Causes Task Failures and When? (Zhang et al., Penn State/MSR) | arXiv:2505.00212, Apr–Jun 2025 (camera-ready) | Attribution accuracy (agent-level, step-level) | Failure logs from 127 LLM MAS with fine-grained annotations | Best method 53.5% agent-ID accuracy, **14.2% step-level**; below-random methods exist; o1/R1 fail | Post-hoc, single-decisive-step ground truth | The attribution primitive a containment system would need is shown to be weak |
| MAST — Why Do Multi-Agent LLM Systems Fail? (Cemri et al., Berkeley) | arXiv:2503.13657, Mar 2025 (v3 Oct 2025) | Failure-mode frequency over **14-mode / 3-category taxonomy** (system design, inter-agent misalignment, task verification); κ=0.88 annotation agreement | MAST-Data: 1600+ annotated traces, 7 MAS frameworks, GPT-4/Claude-3/Qwen2.5/CodeLlama | MAS gains often minimal; failures require more sophisticated solutions | Taxonomy + frequency counts; no propagation dynamics or metrics | The standard failure vocabulary — but static, not dynamic/spread-oriented |
| Beyond Task Completion: Procedure-Aware Evaluation (PAE) (Cao et al.) | arXiv:2603.03116, Mar 2026 | Utility/Efficiency/Interaction-Quality/Procedural-Integrity axes + multi-dimensional gating; **corrupt-success rate** | τ-bench re-evaluation of frontier agents | **27–78% of reported successes are "corrupt"** (conceal policy/integrity violations); gating collapses Pass^4 and re-ranks models | Single-agent τ-bench; procedure = per-agent compliance | Shows outcome metrics mask hidden violations — motivation for propagation-aware measurement |

### 4.3 LLM-as-judge validity

| Paper | ID / venue | Contribution | Key findings | Relation to seed |
|---|---|---|---|---|
| Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al.) | arXiv:2306.05685, **NeurIPS 2023 D&B** | Foundational judge-validity study | Position, verbosity, self-enhancement biases; GPT-4 judge >80% agreement with humans (≈ human-human) | Any LLM-judged blast-radius metric inherits these bias concerns |
| A Survey on LLM-as-a-Judge (Gu et al.) | arXiv:2411.15594, Nov 2024 (v6 Oct 2025) | Survey of judge reliability: consistency, bias mitigation, meta-evaluation benchmark | Reliability of judges requires careful design/standardization | Reference for judge-validity caveats |
| JudgeBench (Tan et al.) | arXiv:2410.12784, **ICLR 2025** | Objective-correctness judge benchmark (knowledge/reasoning/math/code) | GPT-4o-class judges only slightly better than random on hard pairs | Judges are weakest exactly on hard reasoning — where fault-propagation judgments would live |
| LLM Evaluators Recognize and Favor Their Own Generations (Liusie et al.) | arXiv:2404.13076, 2024 (NeurIPS 2024) | Self-preference/self-recognition bias quantification | Evaluators favor own outputs | Bias caveat for agent-judged containment scoring |

### 4.4 Safety / policy-compliance metrics (adjacent)

| Paper | ID / venue | Metric(s) | Relation to seed |
|---|---|---|---|
| AgentHarm (Andriushchenko et al.) | arXiv:2410.09024, **ICLR 2025** | Harm-refusal + capability-retention after jailbreak; 110 malicious tasks / 11 categories | Harm metrics, not fault-spread metrics |
| ST-WebAgentBench (Shlomov et al., IBM) | arXiv:2410.06703, **ICLR 2026** | **Completion-under-Policy (CuP)**, **Risk Ratio** across 6 ST dimensions; 222 enterprise tasks | Policy-boundary compliance metric — closest to an "organizational boundary" metric, but single-agent web tasks, no propagation |
| ShieldAgent | arXiv:2503.22738, 2025 (ICML'25) | Verifiable safety-policy reasoning guardrails | Guardrail efficacy, not spread |
| QuadSentinel (Jiang et al.) | arXiv:2512.16279, Dec 2025 | Guardrail accuracy / rule recall / false positives for machine-checkable sequent policies; evaluated on ST-WebAgentBench + AgentHarm | Runtime policy enforcement; containment-adjacent mechanism without spread metrics |
| OSGuard | arXiv:2606.15034, 2026 | Safety benchmark for computer-use agents | Same pattern: violation metrics, not propagation |
| Enforcing Benign Trajectories: Behavioral Firewall (Dang et al.) | arXiv:2604.26274, Apr 2026 | Attack success rate (ASR), benign task failure rate, per-call latency; pDFA tool-sequence firewall on Agent Security Bench | "Firewall" = prevention at one boundary; no measurement of spread past the boundary |

---

## 5. Failure SPREAD / containment / recovery — the direct search

### 5.1 The one paper that uses the seed's exact metric vocabulary — SCOOP RISK

| Field | Value |
|---|---|
| Title | **Containing the Cascade: A Benchmark and Reference Mediator for Failure Propagation in Tool-Using LLM Multi-Agent Systems** |
| Authors | Veera Ravindra Divi, Sneha Gullapalli, Balajee Asish Brahmandam |
| Year/venue | 2026, **5th Int. Conf. on Electronics Representation and Algorithm (ICERA 2026)** — a minor IEEE-branded venue; Zenodo preprint (10.5281/zenodo.21314249) **deleted 22 Jul 2026 for copyright** (tombstone verified via Zenodo API) |
| IDs | DOI 10.1109/ICERA72709.2026.11666599 (abstract verified via Semantic Scholar record fbfed6b5…) |
| Problem | "No standard, reproducible benchmark for measuring whether a system can contain a cascade as it unfolds" |
| Method | Taxonomy of **six cascading-failure modes**; **Cascade-Bench**: 1080 fault-injection scenarios, 6 domains, **discrete-event simulation** of agent message passing calibrated to reported MAS failure statistics; **Sentinel** mediator: typed message contracts, semantic anomaly gate, circuit breaker, checkpoint recovery |
| **Metrics** | **containment rate, cascade depth, blast radius, mean time-to-detection** — plus task success |
| Findings | Across 48 configs / 590k simulated executions: task success 31.3%→83.7%, containment 46.2%→99.4%; cascade depth ~constant 3→12 agents with Sentinel vs ~doubling unguarded; ablation separates fail-safe (circuit breaker → containment) from fail-operational (checkpoint rollback → completion) |
| Limitations (inferred) | Simulation-only (no real LLM agents); weak venue; authors primarily industry/self-publishing track record; preprint withdrawn; no organizational boundaries (role/authority/memory/accountability); "blast radius" defined over a simulated message graph only |
| Relation to seed | **Direct partial scoop of the metric layer.** Any MASO submission must cite it and differentiate: real LLM MAS vs simulation, organizational boundary dimensions vs message-graph-only, credible venue, reproducibility |

### 5.2 Adversarial spread (attack framing) — verified

| Paper | ID / venue | What it measures about spread | Relation to seed |
|---|---|---|---|
| Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast (Gu, …, Pang et al.) | arXiv:2402.08567, **ICML 2024** | **Infectious jailbreak**: exponential infection of up to 1M LLaVA agents via pairwise chat + shared memory; derives a *principle* for whether a defense can provably restrain spread | Canonical "failure spreads through MAS" result — but adversarial, memory/chat-channel only, no containment-latency or recovery metric |
| Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems (Lee & Tiwari) | arXiv:2410.07283, Oct 2024 | Self-replicating malicious prompts across agents; infection spread even without full comm sharing; defense = LLM Tagging | Spread dynamics again only in attack framing |
| G-Safeguard (Zhang et al.) | arXiv:2502.11127, Feb 2025 | GNN anomaly detection on multi-agent utterance graph + **topological intervention** (edge cutting) for remediation; recovers >40% performance under prompt injection | Closest to a "containment mechanism" — graph surgery — but metric is performance recovery under attack |
| PropGuard: Safeguarding LLM-MAS via Propagation-Aware Exploration and Remediation (Yan et al.) | arXiv:2605.16346, May 2026 | Dual-view spatio-temporal propagation graph; RL-trained inspector recovers suspicious propagation subgraphs; **source-guided remediation + replay of contaminated downstream interactions**; metrics: attack success, defense success, efficiency | Most sophisticated propagation-tracing + remediation to date; still adversarial-injection framing, security metrics |

### 5.3 Resilience / fault tolerance (organic-fault framing) — verified

| Paper | ID / venue | What it measures | Relation to seed |
|---|---|---|---|
| On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents (Huang et al., HKU) | arXiv:2408.00989, Aug 2024 (v4 May 2025) | Fault injection (AutoTransform/AutoInject); **performance drop % by topology** (hierarchical 5.5% vs 23.7%); Challenger/Inspector defenses recover up to **96.4% of injected errors** | The reference organic-fault injection study — but metrics are degradation and error-correction rate, not spread extent or containment latency |
| Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance (Chen, Tian et al.) | arXiv:2511.10400, Nov 2025; **AAAI 2026** | Accuracy under extreme Byzantine fault rates (up to 85.7%) across topologies; CP-WBFT confidence-probe weighted consensus | Reliability = accuracy under faulty majority; consensus framing, no propagation/recovery metrics |
| Byzantine-Robust Decentralized Coordination of LLM Agents (DecentLLMs) (Jo et al.) | arXiv:2507.14928, Jul 2025 | Answer quality + consensus cost under Byzantine agents | Consensus robustness, not containment |
| IBGP: Imperfect Byzantine Generals Problem (Mao et al.) | arXiv:2410.16237, Oct 2024 | Provable resilience of local consensus under communication attacks | Classical BGP bridge; no spread metric |

### 5.4 Recovery — verified

| Paper | ID / venue | What it measures | Relation to seed |
|---|---|---|---|
| AgentTether: Graph-Guided Diagnosis and Runtime Intervention (Zhao et al.) | arXiv:2607.06273, Jul 2026 | **Repair rate** (59.0% Qwen3.7-max, 65.1% GPT-5.4 of initially failed τ-bench Banking tasks), turns/token cost of repair; Critical Transition Graph localization + Repair Memory | Best current "recovery quality" measurement — but single-agent, post-failure re-execution, not MAS-wide recovery |
| A Self-Healing Framework for Reliable LLM-Based Autonomous Agents (Jeong) | arXiv:2605.06737, May 2026; Int. J. SW Eng. & Knowledge Eng. 2026 (10.1142/S0218194026500695) | Task success, claimed **reduction of failure propagation**; failure detection + adaptive replanning/corrective prompting | Only peer-reviewed claim of "failure propagation reduction" found — low-tier journal, vague propagation metric, single-workflow setting |
| Delayed Verification Destabilizes Multi-Agent LLM Belief: Instability Thresholds and Optimal Corrector Placement (Itkin) | arXiv:2606.27409, Jun 2026 (v2 **16 Sep 2026**) | Control-theoretic model: false-claim propagation as delayed consensus; closed-form **stability threshold for verification dose/delay** (delay-2 threshold = 1/φ); supermodular **corrector-placement** objective with greedy (1−1/e) approximation; dose-delay oscillations confirmed on 5 open models | The only formal treatment linking **verification latency → propagation stability** — theoretical backbone a containment-latency metric could build on; belief-propagation setting, not task workflows |

### 5.5 Gap-acknowledging position/survey work — verified

| Paper | ID / venue | Relevance |
|---|---|---|
| Attribution Is Scored on a Finished Trace: What Failure-Attribution Benchmarks Measure, What Cascade Containment Would Need, and Why Neither Result Bounds the Other (Mahendrakar) | Zenodo 10.5281/zenodo.22750267, **10 Sep 2026** (self-published, CC-BY; not peer-reviewed) | Argues attribution benchmarks (Who&When, TRAIL) score completed traces with known failure + single-step ground truth, while containment must act on a **prefix** without knowing failure will occur — i.e., **current metrics structurally cannot measure containment**. Enumerates a "family of recent proposals" for stopping error spread (genealogy-graph governance, cross-channel causal monitoring, propagation-aware remediation, infection-aware safeguarding, corrector placement). Direct evidence the seed's gap is real and recognized |
| Beyond Individual Intelligence: Surveying Collaboration, Failure Attribution, and Self-Evolution (LIFE) (Qi et al.) | arXiv:2605.14892, May 2026 | Survey explicitly notes "errors can propagate across agents and interaction rounds" but organizes the field as attribution→evolution; no spread metrics catalogued |
| Isolation as a First-Class Principle for LLM-Agent System Safety (Jing et al.) | arXiv:2607.12406, Jul 2026 (v2 Sep 2026) | Boundary-centric taxonomy: user-agent, agent-tool, agent-execution, **agent-agent**, system-environment; maps "how compromise propagates across boundaries" qualitatively; no metrics — the boundary structure for an organizational blast-radius definition already exists here |
| Beyond the Leaderboard: Synthesis of Tool-Use, Planning, Reasoning Failures (Albayaydh) | arXiv:2607.05775, Jul 2026 (abstract verified) | Synthesizes 27 benchmark/taxonomy/audit papers (2023–2026, 19 benchmarks) into six failure clusters incl. multi-agent coordination failures and **measurement-validity problems**; finds failures compound nonlinearly with task length and scaffolding does not reliably improve reliability |

### 5.6 Classical / pre-LLM foundations (verified via Crossref)

| Work | ID | Relevance |
|---|---|---|
| Avizienis, Laprie, Randell, Landwehr — Basic Concepts and Taxonomy of Dependable and Secure Computing | IEEE TDSC 2004, DOI 10.1109/tdsc.2004.2 | Canonical **fault→error→failure chain**; error propagation is definitionally the mechanism — the vocabulary a blast-radius metric should reuse |
| Lamport, Shostak, Pease — The Byzantine Generals Problem | ACM TOPLAS 1982, DOI 10.1145/357172.357176 | Fault-tolerance-under-arbitrary-faults root; underlies §5.3 LLM works |
| Motter & Lai — Cascade-based attacks on complex networks | Phys. Rev. E 66, 2002, DOI 10.1103/physreve.66.065102 | Cascading-failure modeling on networks (load redistribution) — classical "blast radius" science |
| Candea et al. — Recovery-Oriented Computing: Building Multitier Dependability | IEEE Computer 2004, DOI 10.1109/mc.2004.219 (see also Fox & Patterson, IEEE Internet Computing 2005, 10.1109/mic.2005.39) | ROC: measure **time-to-recover** rather than only failure avoidance — the MTTR lineage |
| Basiri et al. — Chaos Engineering | IEEE Software 2016, DOI 10.1109/ms.2016.60 | Fault injection as practice (Netflix); the methodological ancestor of Cascade-Bench-style testbeds |
| SRE/incident-metrics practice (MTTD, MTTR, MTTC) | industry standard, no single canonical paper | Containment-latency vocabulary exists in incident response, unadopted in agent evaluation |

---

## 6. Direct answer to the assignment question

**Is there any established metric for failure SPREAD in MAS?**
No *established* (credibly peer-reviewed, adopted) metric. The terms **blast radius / containment rate / cascade depth / MTTD** appear exactly once, in *Containing the Cascade* (ICERA 2026 — weak venue, simulation-only, withdrawn preprint). Adversarial-spread work (Agent Smith, Prompt Infection, PropGuard, G-Safeguard) measures infection/attack success and performance recovery, not organic-fault spread across organizational boundaries.

**Containment latency?**
No operational metric. Closest: Itkin's 2026 control-theoretic verification-delay stability thresholds (arXiv:2606.27409), and MTTD/MTTR/MTTC from SRE practice (never operationalized for LLM MAS).

**Recovery quality?**
Only single-agent repair rate (AgentTether, arXiv:2607.06273) and qualitative claims (Jeong 2026 self-healing). No MAS-level recovery-quality metric exists.

**Does anything here kill or subsume the seed hypothesis?**
- **Kill: no.** No credible venue publishes spread/containment/recovery metrics for LLM MAS; multiple 2026 sources explicitly state the gap (Mohammadi survey's reliability-guarantee gap; Yehudai survey's robustness gap; Mahendrakar's structural argument; LIFE survey's propagation remark).
- **Partial subsume: yes, two flanks.**
  1. *Containing the Cascade* (ICERA 2026) already claims the metric names and a fault-injection testbed — must be cited and differentiated on rigor (real LLM MAS vs discrete-event simulation), organizational boundary dimensions (role/authority/memory/accountability/human — absent there), and venue credibility.
  2. The adversarial-containment line (PropGuard, G-Safeguard, Agent Smith, Prompt Infection) owns "propagation + remediation" in the *attack* framing — the seed must stake the *organic fault + organizational boundary* framing explicitly, and can reuse their graph-tracing machinery.
- **Useful building blocks the seed should appropriate:** pass^k (τ-bench) for reliability baseline; MAST/Who&When/TRAIL for failure vocabulary and the shown weakness of step-level attribution (14.2%); PAE's corrupt-success finding (outcome metrics hide violations — motivation); Itkin's delay-stability theory for containment latency; Isolation survey's five-boundary taxonomy as the structural skeleton for "organizational blast radius."

## 7. Risks and caveats for this report

- Semantic Scholar search and DBLP were unusable from this host during the sweep (429/timeout); discovery relied on DataCite + Crossref + direct arXiv fetches. Coverage of non-arXiv, non-Crossref venues (e.g., some OpenReview-only workshops) may be incomplete.
- The ICERA 2026 paper's full text was not obtainable (IEEE paywall; Zenodo copy deleted); analysis rests on its complete abstract + metadata, which is unusually detailed.
- Zenodo self-published items (Mahendrakar; "Multiplicative Handoff Decay / Circuit-Breaker" zenodo.21216166; "Keel" recovery-economics zenodo.22754511) are real artifacts but not peer-reviewed; treat as weak signals of an emerging micro-literature, not as established prior art.
- A curated reading list on this machine supplied some leads; every item cited in this report was independently fetched and verified against its primary record (arXiv abstract page, Crossref, DataCite, Semantic Scholar, or Zenodo API).
