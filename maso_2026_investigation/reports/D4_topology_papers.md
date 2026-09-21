# D4 — Mandatory Topology Papers: Verification and Positioning

**Investigator:** D4 specialist (topology/restructuring track)
**Date:** 2026-09-21
**Assignment:** Verify and position four papers — (1) "Autonomous Topology Mutation: Safe Runtime Restructuring for Multi-Agent LLM Systems", (2) "AMAS: Adaptively Determining Communication Topology for LLM-based Multi-Agent System", (3) AgentConductor, (4) TopoPrior — with full structured records and a determination of whether any uses restructuring for **fault containment/recovery** (the seed-hypothesis angle).

## Verification method and environment caveats

Sources interrogated: arXiv API + arXiv abs pages + arXiv full-text HTML, arXiv search UI, Hugging Face Papers search, OpenReview API (`api2.openreview.net/notes/search`), Crossref API, GitHub API, ACL Anthology search, DBLP (blocked by anti-bot wall), Semantic Scholar API (persistently 429 from this shared IP), OpenAlex (daily budget exhausted), Google/Bing/DuckDuckGo/Mojeek (all captcha-blocked or returning garbage). All four papers were ultimately verified against **primary sources** (arXiv abstract pages + full text). Where a claim could not be independently confirmed (e.g., AMAS's EMNLP-2025 acceptance), this is flagged explicitly.

## Bottom line

| # | Paper (as assigned) | Verdict | Identifier | Uses restructuring for fault containment/recovery? |
|---|---|---|---|---|
| 1 | Autonomous Topology Mutation | **REAL** (title slightly longer than assigned) | arXiv:2607.20488 [cs.AI], v1 2026 | **PARTIAL — closest to seed.** Runtime restructuring gated by safety invariants, triggered by telemetry incl. tool-error/retry signals; but targets *overload/role-entropy*, not fault propagation or blast radius |
| 2 | AMAS | **REAL** | arXiv:2510.01617 [cs.CL], v3 Oct 2025 | **No.** Per-query topology *selection* for accuracy; static within a query |
| 3 | AgentConductor | **REAL** | arXiv:2602.17100 [cs.MA], v1 Feb 2026 | **No.** RL-generated per-query DAG topologies for code generation; execution feedback ≠ fault tolerance |
| 4 | TopoPrior | **REAL** (full title: "Learning Transferable Topology Priors for Multi-Agent LLM Collaboration Across Domains") | arXiv:2605.17359 [cs.CL], v1 May 2026 | **No.** Offline-learned topology priors for initialization; efficiency/cost focus |

**None of the four studies failure propagation, "blast radius", or containment of a local fault across organizational boundaries.** ATM occupies the adjacent mechanism space (safe runtime restructuring + invariants + privacy-aware memory routing) and is the paper the seed hypothesis must differentiate from — it demonstrates *feasibility* of invariant-gated runtime mutation but does not ask the *failure-propagation* question.

---

## Record 1 — Autonomous Topology Mutation (ATM)

| Field | Value |
|---|---|
| Exact title | Autonomous Topology Mutation: Safe Runtime Restructuring for Multi-Agent LLM Systems with Capability, State, and Shadow Invariants |
| Authors | Chaya Levi, Nizzan Kimhi (Toga Networks / Huawei, Israel); submitted by Bronislav Sidik |
| Year/date | arXiv v1, 2026 (page shows "Thu, 4 Jun 2026"; ID prefix 2607 ⇒ July 2026 — minor internal inconsistency on the page, ID treated as authoritative) |
| Venue | arXiv preprint only (cs.AI; ACM classes I.2.11, C.2.4, D.2.11). 9 pages, 5 tables. No peer-reviewed venue claimed |
| URL / ID | https://arxiv.org/abs/2607.20488 ; DOI 10.48550/arXiv.2607.20488 |
| Code | https://github.com/sidikbro/jiuwen_atm (verified to exist via GitHub API; created 2026-05-27; 0 stars). Implemented as `DeepAgentRail` subclasses for the openjiuwen runtime |

**Research problem.** Multi-agent LLM frameworks fix team topology at boot time. When a single agent becomes overloaded at runtime (mixing too many action categories, accumulating tool errors, queueing), the system has no mechanism to restructure itself safely.

**Method.** ATM = telemetry-driven overload detection + invariant-gated runtime mutation:
- **Bottleneck Index**: six signals — queue depth, context thrash, tool-error rate, role entropy, retry-loop rate, cross-agent wait time; weights (0.20, 0.15, 0.20, 0.20, 0.15, 0.10); warmup = 20 ticks; trigger on K=3 consecutive ticks above a warmup-calibrated 95th-percentile threshold.
- **Mutation**: factorise overloaded agent into specialised sub-agents; hot-swap parent into a coordinator role preserving external identity (agent_id and A2A address, so upstream callers see continuous service); role-conditioned state distillation routes each memory atom by privacy level (PL0–PL4) to a permitted child set or drops it with a logged reason.
- **Three formal invariants** gating every structural change: I1 capability monotonicity (children's capabilities ⊆ parent's), I2 state-routing completeness (every state atom routed only to a PL-permitted destination or explicitly dropped + logged), I3 shadow-before-live (no live traffic until a 5-task shadow validation window passes).
- Supporting rails: ToolRepairRail (bounded LLM repair of HARD tool failures in a 512-token isolated context), MemoryGuardRail (per-span PL classification + per-endpoint trust).

**Experimental setting.** 720 DeepSeek-V3 (deepseek-chat, temp 0.7) task runs — 4 ablation conditions (A0 monolith, A1 random split, A2 ATM factoriser split, A3 full rails+distillation; plus A4 live-trigger variant on a simulator loop) × 3 in-house synthesized workloads × 60 pooled trials (2 seeds × 30). Workloads: W1 research (web search+synthesis), W2 code/debug (high role entropy), W3 security (session triage with PL≥3 atoms). Tools (web_search, web_scrape, run_code) are **deterministic stubs** with parametric failure rates; W4 is a small live-tool probe with real Python execution (5 fixtures, 15 trials). Stats: Pearson chi-square with Yates correction.

**Metrics.** Task success rate; detected PL≥3 memory-exposure events/task (regex classifier); valid-topology rate; p99 hot-path latency of rails; firing rate.

**Major findings.**
- W2 code-task success: A0 3.3% → A2 61.7% (+58 pp, p<10⁻¹⁰); A1 random split 53.3% (factoriser adds ~8 pp over random).
- W1: monolith already 90.0%; ATM ≈ no change (workload doesn't exercise role entropy).
- W3: A0 leaks 2.0 PL≥3 atoms/task → A3 0.0 (3/60 → 0/60 events) with task quality preserved (48.3% vs 50.0%, p=1.00).
- Rails overhead <500 µs p99 on the agent hot path. A4 live triggering fires conservatively (25–55% of runs depending on workload) with automatic rollback.

**Author-stated limitations.** (1) deterministic tool stubs, not real web/code execution (W4 probe only 5 fixtures); (2) regex PL classifier misses paraphrases; (3) N=60/cell — a stronger venue should target N≥100 (A2 vs A3 gap Δ=−0.133, p=0.20 unresolved); (4) A4 live-trigger uses a simulator agent loop, not the real LLM loop; (5) single-level factorisation only — an overloaded child is not handled (no recursive invariant reasoning); (6) all workloads synthesized in-house, no standard benchmarks (GAIA, SWE-bench) — external validity open.

**Inferred limitations.** Single-LLM-vendor evaluation (DeepSeek-V3 only); the dramatic 3.3%→61.7% lift is on a workload deliberately constructed so the monolith fails; "faults" are parametric stub failure rates, not realistic correlated/adversarial agent failures; no measurement of error *propagation* across agents (blast radius never measured); no comparison to checkpoint/restart or redundancy-based recovery; industry preprint, not peer-reviewed; privacy "exposure" measured by a regex classifier the authors control.

**Relationship to seed hypothesis.** **Closest of the four.** It is the only assigned paper where restructuring is a *runtime health/safety* mechanism rather than a per-query performance optimization, and it directly touches two seed dimensions: memory boundary (PL-aware state routing = containment of memory spread during restructuring) and authority/identity (coordinator hot-swap preserving A2A identity). Its invariants (capability monotonicity, state-routing completeness, shadow-before-live) are containment-flavored *safety gates on the restructuring act itself*. **But** it does not study failure propagation, does not define or measure blast radius, does not inject local faults and observe systemic spread, and does not compare containment/recovery strategies. It is a mechanism paper adjacent to — not subsuming — the seed.

---

## Record 2 — AMAS

| Field | Value |
|---|---|
| Exact title | AMAS: Adaptively Determining Communication Topology for LLM-based Multi-Agent System |
| Authors | Hui Yi Leong, Yuheng Li, Yuqing Wu, Wenwen Ouyang, Wei Zhu (corresp.), Jiechao Gao (corresp.), Wei Han. Affiliations listed in full text: Univ. of Chicago, Johns Hopkins, CMU, Univ. of Hong Kong, Stanford, plus an "Independent Researcher" |
| Year/date | arXiv v1 2025-10-02; v3 2025-10-29 |
| Venue | arXiv comment claims "Accepted by EMNLP-2025". **Could NOT independently confirm**: no entry in ACL Anthology (searched 2026-09-21, title and author "Hui Yi Leong"), OpenReview indexes it only as "CoRR 2025". Treat acceptance claim as unverified (indexing lag possible but unlikely 10 months post-conference) |
| URL / ID | https://arxiv.org/abs/2510.01617 ; DOI 10.48550/arXiv.2510.01617 |
| Code | None found/claimed in the text inspected |

**Research problem.** Hand-crafted, fixed MAS graph topologies lack per-sample contextual responsiveness; RL-optimized topologies (GPTSwarm) are unstable and still produce one static graph per task distribution.

**Method.** A "dynamic graph designer": a LoRA-adapted LLM backbone that, per input query, ranks/selects among candidate graph configurations (K=4 top candidates) using a bespoke ordinal ranking loss with item-wise disparity weights m(i,j); the query is routed through the selected task-optimized agent pathway. Candidate graphs follow GPTSwarm-style composite structure (ToT agent depth 4 / branching 2 + Reflection agent + output node; n=12 nodes; learnable edge vector Θ; REINFORCE for the graph-optimization baseline config).

**Experimental setting.** Benchmarks: Crossword (5×5), Game-of-24, MMLU, "LLM-Eval-P" (**internal, non-public** benchmark of 47 domain challenges), HumanEval. 8:1:1 train/dev/test splits; designer trained only on train partitions. Backbones: LLaMA-3 8B/72B primary; extended to GPT-3.5-turbo, DeepSeek-R1-distill-7B, Qwen3-8B/30B. Baselines: IO, CoT, Self-Consistency, ToT, GoT (single-agent); AutoGPT, AgentVerse, GPTSwarm (multi-agent).

**Metrics.** Character-level precision (Crossword), success rate (Game-of-24), MC accuracy (MMLU, LLM-Eval-P), pass@10 (HumanEval); median over 5 seeds; latency in seconds.

**Major findings.** AMAS beats all baselines on all tasks (per Table 3), incl. AgentVerse and GPTSwarm; latency comparable to GPTSwarm (graph selection = one extra forward pass); ablations justify K=4 and the ranking-loss weight term.

**Author-stated limitations.** No evaluation on "exceptionally large open-source LLMs, including LlaMA-3 450B" (**note: no such model exists — likely means LLaMA-3.1 405B; quality red flag**); limited task-complexity scope.

**Inferred limitations.** Hyperbolic writing ("paradigm-shifting"); one benchmark is internal/unverifiable; per-query selection happens *before* execution — the topology is static within a query and there is no runtime adaptation; no robustness/fault analysis; EMNLP claim unverified; author list mixes major-lab affiliations with an independent researcher and the submission pattern (heavy self-citation to "Zhu et al." works) warrants caution.

**Relationship to seed hypothesis.** None on faults. Establishes that *per-query topology choice matters for utility* — useful as a baseline/terminology anchor for "topology adaptation", but restructuring is not runtime, not fault-triggered, and not containment-oriented.

---

## Record 3 — AgentConductor

| Field | Value |
|---|---|
| Exact title | AgentConductor: Topology Evolution for Multi-Agent Competition-Level Code Generation |
| Authors | Siyu Wang, Ruotian Lu, Zhihao Yang, Yuchao Wang, Yanzhou Zhang, Lei Xu, Qimin Xu, Guojun Yin (Meituan), Cailian Chen (corresp.), Xinping Guan (corresp.) — Shanghai Jiao Tong University + Meituan |
| Year/date | arXiv v1 2026-02-19 |
| Venue | arXiv preprint (cs.MA). Keywords line says "Machine Learning, ICML" and the appendix references "the reviewer's concern" ⇒ under review (ICML 2026 cycle) at time of writing; no accepted venue confirmed |
| URL / ID | https://arxiv.org/abs/2602.17100 ; DOI 10.48550/arXiv.2602.17100 |
| Code | No official repo identified. A third-party reproduction effort exists: github.com/RobinElysia/Agent-Contuctor (Chinese-language README describing a CLI re-implementation of the paper) |

**Research problem.** Fixed MAS topologies for code generation waste tokens on easy problems and under-serve hard ones; existing dynamic methods either prune one topology per dataset (reused across instances) or generate a query-conditioned graph that then stays frozen during execution.

**Method.** RL-optimized MAS with an LLM orchestrator ("Managing Agent") that per query infers agent roles (6-type pool, MapCoder-inspired) and task difficulty, then constructs a task-adapted, density-aware **layered DAG**; topology can evolve across two interaction turns using execution feedback. Key innovations: (1) a topological density function S_complex (node/edge/diameter terms) as a communication-aware mathematical characterization; (2) difficulty interval partitioning with per-difficulty density upper bounds (4/7/10, derived from SFT sample statistics). Training: CoT-style SFT then RL with separated rewards — r_e (execution correctness: YAML-format validity + code outcome) and r_g (density); invalid YAML ⇒ strong negative reward.

**Experimental setting.** Datasets: HumanEval, MBPP (basic); APPS, LiveCodeBench v4, CodeContests (contest-level). Sandbox execution. Baselines: Vanilla GPT-4o-mini; AutoGen, MetaGPT, MapCoder; AFlow, FlowReasoner, Chain-of-Agents; GPTSwarm, AgentPrune, G-Designer, MacNet (under both complex- and layered-graph inits; max 20 agent nodes).

**Metrics.** pass@1; prompt/completion token consumption; average S_complex density; valid-topology rate.

**Major findings.** pass@1: APPS 58.8% (+14.6 pp over second-best), LiveCodeBench-v4 46.3% (+3.1), CodeContests 38.8% (+1.1), HumanEval 97.5% (+1.0), MBPP 95.1% (+0.7); on APPS simultaneously best accuracy, sparsest topology, lowest token cost (abstract claims up to 13% density reduction, 68% token-cost reduction). Ablations: SFT stage crucial for valid topologies; YAML-format reward drives validity, code-execution reward drives accuracy; removing density sub-rewards degrades accuracy.

**Author-stated limitations.** Domain focus on competition-level code is "a deliberate choice rather than a limitation"; cross-domain applicability evaluated only in an appendix added in response to reviewers.

**Inferred limitations.** Feedback signal is code-execution correctness — the "evolution" responds to *task feedback*, not to agent faults; single domain family; density bounds hand-derived from SFT statistics; no robustness analysis to agent failure, message corruption, or tool faults; not yet peer-reviewed.

**Relationship to seed hypothesis.** None on faults. Relevant as evidence that *execution feedback can drive intra-instance topology change* (a mechanism the seed's recovery strategies could exploit), but there is no fault model, no propagation analysis, no containment.

---

## Record 4 — TopoPrior

| Field | Value |
|---|---|
| Exact title | Learning Transferable Topology Priors for Multi-Agent LLM Collaboration Across Domains |
| Authors | Taolin Zhang, Jiuheng Wan, Richang Hong (Hefei Univ. of Technology); Zijie Zhou (China Univ. of Petroleum, Beijing); Tingyuan Hu, Xiaofeng He (East China Normal Univ.); Chengyu Wang (Alibaba; corresp. with R. Hong) |
| Year/date | arXiv v1 2026-05-17 |
| Venue | arXiv preprint (cs.CL); IEEE-style formatting ("Index Terms") suggests journal/conference submission, none confirmed |
| URL / ID | https://arxiv.org/abs/2605.17359 ; DOI 10.48550/arXiv.2605.17359 |
| Code | None found/claimed in the text inspected |

**Research problem.** Topology-evolution methods (G-Designer, AgentPrune, ARG-Designer, AgentDropout…) search a collaboration graph **from scratch per query**, causing online search overhead, high inference-time token cost, and poor multi-domain scalability.

**Method.** Learn reusable topology priors **offline** from reference collaboration graphs (built with AgentDropout on training splits) across multiple domains; at inference, generate a query-conditioned **initial** graph that a downstream topology-evolution backbone then refines. Two components: (1) transferable topology-prior learning via a conditional variational graph framework (latent space over graphs; adjacency matrices over a candidate role pool); (2) query-conditioned latent adaptation with adversarial domain alignment. Frozen BERT encodes query/role representations; generator autoregressively selects agent nodes. Includes a theoretical cost model: better/sparser initialization ⇒ fewer refinement rounds and lower per-round token cost.

**Experimental setting.** MMLU (57 subjects → 7 domains) and C-Eval / C-Eval Hard, under multi-domain partitions. Backbones: Llama3-8B-Instruct (local), Qwen2.5-72B-Instruct, DeepSeek-V3-671B-Instruct (online). Backbones augmented: G-Designer, AgentPrune, ARG-Designer, AgentDropout. Single-agent baselines: PE, CoT, RAG. Training: PyTorch, 2× A800 GPUs, Adam lr 2e-4, 5 epochs; +3.3M trainable params.

**Metrics.** Classification accuracy per domain; online inference token usage (excludes offline prior training); communication rounds.

**Major findings.** TopoPrior improves most backbone×benchmark cells; e.g., MMLU + Llama3-8B: ARG-Designer 65.58→68.53 (+2.95), AgentDropout 65.72→67.31 (+1.59); C-Eval: ARG 54.25→57.04 (+2.79). Online inference token usage reduced up to 40.22%. ARG-Designer benefits most (autoregressive construction is initialization-sensitive). Gains transfer across backbones ⇒ priors capture reusable regularities beyond one teacher.

**Author-stated limitations / future work.** Reduce reliance on expensive offline supervision (weaker/cheaper reference graphs); extend predefined role pool to open-ended role discovery; tighter integration of prior learning with downstream refinement. No dedicated limitations section.

**Inferred limitations.** Only MC-QA benchmarks (MMLU/C-Eval); reference graphs come from one teacher method (AgentDropout) — teacher bias only partially ablated; gold domain labels used for partitioning; no fault/robustness dimension whatsoever.

**Relationship to seed hypothesis.** None on faults. Complementary infrastructure: if the seed needs cheap topology *re*-initialization during recovery, prior-based initialization is a candidate mechanism — but the paper itself never considers faults, propagation, or containment.

---

## Cross-cutting analysis: restructuring for fault containment/recovery?

| Paper | Restructuring trigger | When | Goal | Fault model? | Containment/recovery semantics? |
|---|---|---|---|---|---|
| ATM (2607.20488) | Runtime telemetry (Bottleneck Index incl. tool-error rate, retry-loop rate) | **Runtime, live system** | Relieve overload; preserve safety invariants + privacy during mutation | Implicit/overload only (parametric stub failure rates) | **Partial**: invariants gate mutation; PL-aware memory routing limits memory spread; shadow window + rollback are recovery-flavored. But no propagation/blast-radius study |
| AMAS (2510.01617) | Query content | Pre-execution, per query | Accuracy | None | None |
| AgentConductor (2602.17100) | Query difficulty + execution feedback | Per query, ≤2 turns | Accuracy + token cost | None (code-execution feedback ≠ faults) | None |
| TopoPrior (2605.17359) | Query content + offline priors | Initialization, per query | Accuracy + amortized search cost | None | None |

## Adjacent works surfaced during verification (for the swarm's map)

- **TacoMAS** (Xu et al., 2026) — test-time co-evolution of topology *and* capability, fast/slow loops, agent birth-death (edge edit, agent add/remove); ~20 baselines; code: github.com/chenxu2-gif/TacoMAS-MultiAgent. Cited in ATM's related work. (arXiv ID not independently captured — HF Papers listing only.)
- **DyTopo** (Lu et al., 2026) — reconstructs sparse directed communication graph each reasoning round via semantic query/key matching (cited in ATM).
- **MetaGen** (Wang et al., 2026) — edits role specs + rewrites execution graph from a dynamic role pool (cited in ATM).
- **SkillMAS** (Pan et al., 2026) — couples MAS restructuring with skill evolution (cited in ATM).
- **Self-Healing Router** (Bholani, 2026; arXiv:2603.01548) — reweights graph edges on tool failure so Dijkstra reroutes without invoking the LLM; cited by ATM as output/task-level healing, not team restructuring.
- Classical: **Rainbow** (Garlan et al., 2004) architecture-based self-adaptation (MAPE loop) — ATM's acknowledged lineage; "A decentralised self-healing approach for network topology maintenance" (JAAMAS 2020, DOI 10.1007/s10458-020-09486-3) — pre-LLM MAS topology self-healing (surfaced via Crossref).

## Does any of this kill or subsume the seed hypothesis?

**No.** Specifics:

1. **No blast-radius science exists here.** None of the four defines, measures, or models failure propagation across role/communication/authority/tool/memory/accountability/human boundaries. The seed's central construct is untouched.
2. **ATM is the nearest neighbor and must be cited/differentiated.** It shows invariant-gated runtime restructuring is buildable with <500 µs overhead and that memory-aware state routing during restructuring reduces privacy exposure. But its trigger is overload (not arbitrary local faults), its evaluation is synthetic single-level splits, and it never asks "how far does a fault spread" or "which containment mechanism minimizes systemic impact while preserving utility". The seed can position itself as *the missing science of failure propagation and containment*, with ATM-style invariants as one candidate containment mechanism to evaluate (not the research question itself).
3. **Overlap risk to watch, not a kill:** if the seed's contribution were framed as merely "runtime topology restructuring with safety invariants", ATM would substantially scoop it. Framed as "what determines organizational blast radius + comparative containment/recovery mechanisms under injected faults", it is differentiated.
4. **The performance-topology literature (AMAS, AgentConductor, TopoPrior, GPTSwarm-lineage)** supplies baselines and mechanisms (per-query selection, RL DAG generation, prior-based initialization) that a containment study can reuse as recovery actions — none of them consider faults, so no novelty conflict.
5. **Quality flags:** AMAS's EMNLP-2025 acceptance is unverified (absent from ACL Anthology) and the paper contains factual glitches ("LLaMA-3 450B"); AgentConductor and TopoPrior are unreviewed preprints; ATM is an industry preprint with synthetic workloads. Cite accordingly.
