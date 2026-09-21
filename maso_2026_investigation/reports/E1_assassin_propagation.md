# E1 ASSASSIN REPORT — Killing "Organizational Blast Radius" via Propagation Synonyms

**Investigator:** ASSASSIN E1
**Date:** 2026-09-21
**Mission:** Prove that "organizational blast radius" (failure propagation + containment in LLM multi-agent systems) is NOT novel. Search cascading errors, failure/fault propagation, error amplification, semantic faults, downstream failure, information contagion, error cascades across LLM MAS, classical MAS, and distributed systems. Find the closest existing quantitative spread metric. Name the single most damaging paper.

---

## BOTTOM LINE

**The seed's core novelty claim is DEAD.** Failure/error propagation in LLM multi-agent systems is an actively crowded 2025–2026 research area with (a) a paper that already uses **"blast radius" as a named containment metric** in a fault-injection benchmark for tool-using LLM MAS ("Containing the Cascade", IEEE ICERA 2026), (b) peer-reviewed EMNLP 2025 / NeurIPS 2025 / IEEE TASLP 2026 / EMNLP 2026 papers quantifying error propagation across communication topologies and pipelines, (c) a dedicated ICML 2026 workshop (FAGEN: Failure Modes in Agentic AI), and (d) a 25+-year classical lineage (sentinel fault handling in MAS 1997, exception handling in agent systems 1999, cascading-failure branching-process metrics 2004, DebtRank 2012, chaos engineering's "Minimize Blast Radius" principle ~2016–2019). The term "blast radius" itself is established chaos-engineering vocabulary for exactly this concept.

**Single most damaging paper:** *Containing the Cascade: A Benchmark and Reference Mediator for Failure Propagation in Tool-Using LLM Multi-Agent Systems* (Divi, Gullapalli, Brahmandam; IEEE ICERA 2026; DOI 10.1109/ICERA72709.2026.11666599). It already contains: a cascading-failure taxonomy, the metrics **containment rate, cascade depth, blast radius, mean time-to-detection**, a 1080-scenario fault-injection benchmark (Cascade-Bench), and a containment/recovery mediator (Sentinel: message contracts, anomaly gate, circuit breaker, checkpoint rollback) evaluated on task-utility preservation. That is the seed hypothesis in one paper.

**Residual wedges (what survives):** (1) "Containing the Cascade" runs on a *discrete-event simulation* of agent message passing calibrated to reported statistics, not real LLM MAS executions; (2) nobody found covers the full *organizational* boundary set — authority/delegation, accountability, and human-agent boundaries are only partially touched (CTHA covers authority manifolds; accountability is covered by the already-occupied delegation proposal); (3) recovery (vs. containment) under *organizational* semantics (role reassignment, delegation revocation, human escalation) is not systematically studied. A resubmission framed as "organizational blast radius in real LLM MAS across authority/accountability/human boundaries" retains a narrow wedge, but the propagation-metric novelty claim cannot be made.

---

## METHODOLOGY

Sources queried 2026-09-21: Semantic Scholar Graph API (spaced single calls; heavy shared-IP 429s), Crossref REST API (primary workhorse, `query.bibliographic` + per-DOI metadata), OpenAlex (shared daily budget exhausted mid-sweep), OpenReview API v2, arXiv abs pages via direct fetch (arXiv search UI and export API were 429/blocked from this host all session), DBLP (unreachable from this host), principlesofchaos.org, fagen-workshop.github.io. Every paper below was verified by inspecting its arXiv abstract page, Crossref/S2 metadata record, or publisher page — not search snippets. Synonym coverage: error propagation, failure propagation, fault propagation, cascading errors/failures, error cascade, error amplification, hallucination propagation/snowball/cascade, information contagion/diffusion, compounding errors, error accumulation, downstream failure, blast radius, failure containment, metastable failures, sentinel/exception handling (classical MAS), prompt infection/worm (adversarial contagion).

---

## TABLE A — DIRECT KILLS: propagation in LLM MAS (2023–2026), all verified

| Paper | Authors, year, venue | ID | What it does | Metrics / quantitative spread | Relation to seed |
|---|---|---|---|---|---|
| **Containing the Cascade: A Benchmark and Reference Mediator for Failure Propagation in Tool-Using LLM Multi-Agent Systems** | Divi, Gullapalli, Brahmandam; 2026 (July), IEEE ICERA 2026 | DOI 10.1109/ICERA72709.2026.11666599; open artifact Zenodo 10.5281/zenodo.21314250 | Taxonomy of 6 cascading-failure modes; Cascade-Bench fault-injection testbed (1080 scenarios, 6 domains, discrete-event simulation calibrated to reported MAS failure stats); Sentinel mediator (typed message contracts, semantic anomaly gate, circuit breaker, checkpoint recovery); 48 configs, 590k simulated executions | **Containment rate, cascade depth, BLAST RADIUS, mean time-to-detection**; task success 31.3%→83.7%, containment 46.2%→99.4%, cascade depth flat as system scales 3→12 agents | **Subsumes the seed's core**: fault → propagation → spread metrics (incl. the exact term "blast radius") → containment + recovery with utility preservation. Gaps: simulated (not real-LLM) message passing; low-tier venue; no authority/accountability/human boundaries |
| Beware of the Woozle Effect: Exploring and Mitigating Hallucination Propagation in Multi-Agent Debate | Zhang, Zhang, Zeng, Liu, Zhao; 2026, IEEE Trans. Audio, Speech & Language Processing (peer-reviewed journal) | DOI 10.1109/TASLPRO.2026.3675803 | First empirical identification of hallucination propagation among debating agents ("woozle effect"); attributes spread to static fully-connected communication topology; proposes DIGRA (dynamic topology via information gain ratio) to mitigate | Hallucination propagation rates across debate rounds; mitigation effectiveness across benchmarks | Propagation across the **communication boundary** + topology-based containment, peer-reviewed. Scoped to debate/hallucination only |
| Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems | Shen et al.; 2025, EMNLP 2025 (main) | arXiv:2505.23352; DBLP conf/emnlp/ShenLDWMTPW25 | Causal framework for how correct/erroneous outputs propagate under topologies of varying sparsity; EIB-learner balances error suppression vs beneficial diffusion | Error propagation vs information diffusion trade-off; task performance, communication cost, robustness | Directly studies "what determines spread" on the communication axis with utility-preserving design |
| The Hallucination Snowball: Modeling Error Propagation as State Transitions in Multi-Agent LLM Pipelines | Singh et al.; 2026, FAGEN Workshop @ ICML 2026 | arXiv:2608.14588 | Markov model of hallucination transformation across 4 pipeline states (Raw→Derived→Narrative→Invisible); 346 injected hallucinations in 4-agent financial pipeline (FinanceBench); boundary gates vs end-checking | **Per-boundary escape probabilities (24.6%/48.3%/89.3%)**, survival rate (23.7% undetected), detection drop 72.0%→50.9%; boundary gates cut survival 58.4%→16.2% | Quantitative per-boundary spread model + containment placement ("when you verify matters more than whether") |
| Hallucination Cascade: Analyzing Error Propagation in Multi-Agent LLM Systems | Jamshidi et al.; 2026 (June), arXiv | arXiv:2606.07937 | Claim-level tracking of factual inconsistency across sequential agent cascades; 500 cascade experiments, 10 domains, GPT-5.3/DeepSeek-V3/LLaMA-3-70B | **Amplification factor 0.644** (net attenuation), hallucination score 0.422→0.272 over 3-agent chains, per-transition reduction 0.072 | Quantitative error-propagation measurement in agent chains; finds attenuation not amplification in that setting |
| PropUQ-MAS: Propagation-Aware Uncertainty Quantification for LLM Multi-Agent Systems | Liu et al.; 2026, EMNLP 2026 (main) | arXiv:2608.22130 | UQ framework modeling MAS execution as communication-structured graph; errors "inherited and amplified by downstream agents" | AUROC +6.10%, PRR +47.58% relative gains | Propagation-aware reliability quantification over the communication graph |
| GUARDIAN: Safeguarding LLM Multi-Agent Collaborations with Temporal Graph Modeling | Zhou et al.; 2025, NeurIPS 2025 | arXiv:2505.19234; DBLP journals/corr/abs-2505-19234 | Models collaboration as temporal attributed graph; "explicitly captures the propagation dynamics of hallucinations and errors"; detects anomalous nodes/edges | SOTA detection accuracy of anomalous nodes/edges | Propagation dynamics + detection/mitigation, top venue |
| CTHA: Constrained Temporal Hierarchical Architecture for Stable Multi-Agent LLM Systems | Jardine et al.; 2026 (Jan), arXiv | arXiv:2601.10738 | Hierarchical MAS suffer "unbounded error propagation"; message-contract constraints, **authority manifold constraints**, arbiter resolution | **47% reduction in failure cascades**, 2.3× sample efficiency | Containment via authority bounding — touches the authority/delegation boundary |
| The Confused Deputy in the Swarm: Cascading Privilege Escalation and Memory Poisoning in Multi-agent LLMs | Vishwakarma; 2026, SSRN | DOI 10.2139/ssrn.7360399 | Empirical lab study: subordinate agents refine/concentrate indirect prompt injections; cascading privilege escalation across IPC; latent memory poisoning in RAG stores; deterministic policy firewall eliminates escalation | **Cascading escalation rate up to 65.0%**, reasoning-drift trigger rate 75.0% | Propagation across **authority + memory boundaries** with quantitative rates and a containment mechanism (adversarial setting) |
| Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems | Lee, Tiwari; 2024, arXiv; ESORICS 2025 | arXiv:2410.07283; DOI 10.1007/978-3-032-16092-8_28 | Self-replicating malicious prompts propagate agent-to-agent "like a computer virus"; LLM Tagging defense | Infection spread across communication patterns; attack success rates | Adversarial contagion across communication boundary + containment |
| Here Comes The AI Worm (Morris II) | Cohen, Bitton, Nassi; 2024, arXiv | arXiv:2403.02817 | Zero-click worm cascading indirect prompt injections across GenAI email-assistant ecosystem; Virtual Donkey guardrail | Propagation vs **number of hops**, context size, embedding type; guardrail TPR 1.0 / FPR 0.015 | Hop-count spread metric in GenAI ecosystems (adversarial) |
| Behavioral Drift in Multi-Agent LLM Systems: Emergent Failure Modes, Cascade Dynamics, and Measurement Challenges | Gagne; 2026, SSRN | DOI 10.2139/ssrn.6420858 | 200–500-turn 3-agent conversations; documents **"cascade propagation (one agent's failure triggering degradation in others)"**, agent collapse, compensatory expansion; collapse is triggered, not spontaneous (0/12 baselines) | Longitudinal behavioral trajectories; statistical replication | Non-adversarial failure cascade observed empirically; single-author SSRN, conversational setting |
| Failure Modes in Production Multi-Agent LLM Systems | Ahmed, Akbar; 2026, SSRN | DOI 10.2139/ssrn.7041478 | Production platform failure classes incl. **cross-session state contamination** and **cache poisoning in retrieval**; mitigations | Supervisor misclassification >80% pre-remediation; latency data | Memory/RAG boundary contamination in real deployments (practice report) |
| Why Do Multi-Agent LLM Systems Fail? (MAST) | Cemri et al.; 2025, arXiv (v3 Oct 2025) | arXiv:2503.13657 | 14-mode failure taxonomy over 1600+ annotated traces, 7 frameworks | Failure-mode frequencies; κ=0.88 | Diagnosis/taxonomy, no spread metric — the gap "Containing the Cascade" explicitly claims to fill |
| TRAIL: Trace Reasoning and Agentic Issue Localization | Deshpande et al.; 2025, arXiv | arXiv:2505.08638 | Error taxonomy + 148 annotated traces; LLMs score ~11% at trace debugging | Localization accuracy | Trace-level error analysis; no propagation metric |
| Which Agent Causes Task Failures and When? (Who&When) | Zhang et al.; 2025, ICML 2025 (camera-ready) | arXiv:2505.00212 | Automated failure attribution dataset (127 MAS) | 53.5% agent / 14.2% step attribution accuracy | Blame localization (adjacent to accountability boundary; occupied territory) |
| Generative Agents | Park et al.; 2023, UIST 2023 | arXiv:2304.03442 | Information (party invitations) spreads autonomously through 25-agent sandbox | — | Canonical demonstration of information diffusion in LLM agent societies |
| AgentSociety | Piao et al.; 2025, arXiv (v2 Apr 2026) | arXiv:2502.08691 | 10k-agent social simulation; studies **spread of inflammatory messages**, polarization, shocks | Population-level spread outcomes | Information contagion at societal scale |

**Venue signal:** FAGEN — *Failure Modes in Agentic AI* — was a full ICML 2026 workshop (July 10, 2026, Seoul; verified at fagen-workshop.github.io) whose call explicitly covers reproducible failure triggers, trace diagnostics, and "mitigation, repair, or intervention strategies with explicit evidence." The territory has a dedicated venue already.

---

## TABLE B — Closest existing quantitative spread metrics (the assignment's key question)

| Metric | Definition | Source (verified) | Distance from "organizational blast radius" |
|---|---|---|---|
| **Blast radius** (named metric for LLM MAS) | Extent of cascade spread in tool-using LLM MAS, alongside containment rate, cascade depth, MTTD | Divi et al. 2026, DOI 10.1109/ICERA72709.2026.11666599 | **Zero — the exact term, in the exact setting** |
| **"Minimize Blast Radius"** | One of the 5 Principles of Chaos Engineering: contain fallout of failure experiments | principlesofchaos.org (Netflix, verified; last update 2019-03); Basiri et al., "Chaos Engineering", IEEE Software 2016, DOI 10.1109/MS.2016.60 | Zero at the concept level; industry term predates the seed by ~a decade |
| **Branching factor σ / propagation λ** | Expected number of secondary failures per failure in cascading blackouts; cascade size distribution | Dobson, Carreras, Newman, HICSS 2004, DOI 10.1109/HICSS.2004.1265185; HICSS 2005, DOI 10.1109/HICSS.2005.125; Kim & Dobson, IEEE Trans. Reliability 2010, DOI 10.1109/TR.2010.2055928 | The canonical quantitative "spread per fault" metric, 20+ years old |
| **DebtRank** | Fraction of total system economic value affected by distress originating at a node | Battiston, Puliga, Kaushik, Tasca, Scientific Reports 2012, DOI 10.1038/srep00541 | Node-level systemic-impact metric — mathematically an "organizational blast radius" for financial networks |
| **Expected influence spread σ(S)** | Expected cascade size under Independent Cascade / Linear Threshold models | Kempe, Kleinberg, Tardos, KDD 2003, DOI 10.1145/956750.956769 | Canonical spread metric in network science |
| **Per-boundary escape probability / survival rate** | Probability an error crosses a pipeline stage undetected | Hallucination Snowball, arXiv:2608.14588 | Boundary-resolved spread metric in LLM MAS pipelines |
| **Amplification factor** | Ratio of hallucination score at final vs first agent in a cascade | Hallucination Cascade, arXiv:2606.07937 | Direct LLM-MAS error-amplification metric |
| **Cascade escalation rate / hop-count propagation** | % of downstream orchestrators escalated; worm success vs hops | Confused Deputy in the Swarm (65.0%); Morris II (arXiv:2403.02817) | Adversarial spread metrics across authority/communication boundaries |
| **Metastable failure amplification** | Failure modes sustained by feedback loops (retry storms, load amplification) after trigger removal | Bronson, Aghayev, Charapko, Zhu, HotOS 2021, DOI 10.1145/3458336.3465286 | Distributed-systems analog of self-sustaining organizational failure |
| **Error propagation probability / permeability** | Fault-injection-based measurement of error flow through software modules | Voas, COMPSAC 1997, DOI 10.1109/CMPSAC.1997.625059; Hiller et al. fault-injection lineage (e.g., DOI 10.1109/ISSRE.1998.730903) | Classical software-engineering spread quantification |

---

## TABLE C — Classical MAS fault handling / containment (predates LLMs)

| Paper | Year, venue | ID | Contribution |
|---|---|---|---|
| Hägg, "A Sentinel Approach to Fault Handling in Multi-Agent Systems" | 1997, LNCS (ATAL/MAAMAW lineage) | DOI 10.1007/bfb0030090 | Sentinel agents that monitor and contain faults in MAS |
| Klein & Dellarocas, "Exception Handling in Agent Systems" | 1999, Autonomous Agents '99 | DOI 10.1145/301136.301164 | Domain-independent exception-handling services for agent systems |
| Dellarocas & Klein, experimental evaluation of fault-handling services in open MAS | 2000, ICMAS | DOI 10.1109/ICMAS.2000.858440 | Empirical evaluation of fault handling (incl. agent death) |
| Klein, Rodriguez-Aguilar, Dellarocas, "Using Domain-Independent Exception Handling Services…: The Case of Agent Death" | 2003, AAMAS journal | DOI 10.1023/A:1024145408578 | Robust open MAS via exception services |
| Stanković, Štula, Maras, "Evaluating fault tolerance approaches in multi-agent systems" | 2015, AAMAS journal | DOI 10.1007/s10458-015-9320-6 | Comparative experimental evaluation of MAS fault-tolerance approaches |

---

## TABLE D — Distributed systems / networks / org theory anchors

| Work | Year, venue | ID | Relevance |
|---|---|---|---|
| Buldyrev et al., "Catastrophic cascade of failures in interdependent networks" | 2010, Nature | DOI 10.1038/nature08932 | Cascade dynamics across interdependent systems; percolation threshold |
| Basiri et al., "Chaos Engineering" | 2016, IEEE Software | DOI 10.1109/MS.2016.60 | Industry discipline of fault injection; cascading failure as core target |
| Basiri et al., "Automating Chaos Experiments in Production" | 2019, ICSE-SEIP | DOI 10.1109/ICSE-SEIP.2019.00012 | Automated fault injection with blast-radius control |
| Reason, "Managing the Risks of Organizational Accidents" (+ "Organizational Accidents Revisited" 2016; "Identification of Latent Organizational Failures" 1993) | 1997/2016/1993 | DOI 10.4324/9781315543543; 10.4324/9781315562841; 10.1007/978-3-662-02933-6_13 | Swiss-cheese model: latent organizational failures propagate through defense layers — the *conceptual* template for "organizational blast radius" |
| Perrow, "Normal Accidents: Living with High-Risk Technologies" | 1984 | DOI 10.1515/9781400828494 (Princeton reprint) | Interactive complexity + tight coupling ⇒ inevitable system accidents — the original "what determines spread" theory for organizations |

---

## BOUNDARY-BY-BOUNDARY COVERAGE vs THE SEED'S 7 BOUNDARIES

| Seed boundary | Covered by prior art? | Strongest prior art |
|---|---|---|
| Role | Partially | Containing the Cascade (role drift as cascade mode); MAST |
| Communication | **Fully** | Shen et al. EMNLP 2025; Woozle/DIGRA TASLP 2026; GUARDIAN NeurIPS 2025; PropUQ-MAS EMNLP 2026 |
| Authority/delegation | Substantially | Confused Deputy in the Swarm (65% escalation); CTHA authority manifolds; delegation-invariants territory already occupied by existing MASO proposal |
| Tool | **Fully** | Containing the Cascade (tool-using MAS fault injection + blast radius metric) |
| Memory | Substantially | Confused Deputy (memory poisoning); Production Failure Modes (cross-session contamination, cache poisoning) |
| Accountability | Partially (occupied) | Who&When failure attribution; TRAIL; existing MASO delegation/accountability proposal |
| Human-agent | **Weakly covered** — residual wedge | Only FAGEN workshop scope (Maarten Sap keynote on human-agent risk); no quantitative spread study found |

## DOES ANYTHING KILL OR SUBSUME THE SEED?

**Yes — substantially.** "Containing the Cascade" (ICERA 2026) alone occupies: fault injection in tool-using LLM MAS + propagation taxonomy + the literal metric name "blast radius" + containment/recovery mediator + utility-preservation results. The communication-boundary spread question is peer-reviewed occupied (EMNLP 2025, NeurIPS 2025, TASLP 2026, EMNLP 2026). The term is chaos-engineering standard. The organizational framing is Reason (1997)/Perrow (1984).

**Not fully subsumed:** (1) real-LLM (non-simulated) organizational workflows; (2) the human-agent boundary and accountability boundary as *propagation* dimensions; (3) recovery mechanisms with organizational semantics (role reassignment, delegation revocation, human escalation) rather than generic circuit breakers/checkpoints; (4) cross-boundary interaction effects (e.g., does a memory-boundary fault amplify through authority chains?). Any viable MASO submission must cite and differentiate from Divi et al. 2026, Shen et al. 2025, Woozle/DIGRA 2026, GUARDIAN, PropUQ-MAS, and the chaos-engineering blast-radius lineage — and cannot claim the propagation-metric framing as novel.

## VERIFICATION NOTES / LIMITATIONS OF THIS REPORT

- All Table A papers verified via arXiv abs pages or Crossref/S2 metadata records inspected 2026-09-21. "Containing the Cascade" full text not retrieved (IEEE Xplore/Zenodo blocked from host); its abstract, authors, venue, metrics, and numbers come from its Semantic Scholar record (CorpusId 291663225) corroborated by Crossref DOI metadata. Numbers quoted are from the abstract.
- arXiv search UI, arXiv export API, DBLP, and OpenAlex were rate-limited/blocked from this host for parts of the session; recall on 2026 preprints may be incomplete. Semantic Scholar was queried with spaced single calls.
- SSRN items (Confused Deputy, Behavioral Drift, Production Failure Modes) are non-peer-reviewed preprints; flagged accordingly.
