# D2 — Fault-Injection Papers: Verification and Positioning Report

**Investigator:** Specialist D2 (fault-injection line)
**Date:** 2026-09-21
**Assignment:** Verify and position (1) MAS-FIRE, (2) AgentChaos, (3) any work named IMACS related to multi-agent fault injection, (4) 2026 successors to the fault-injection line. Full structured records + what they do NOT do (containment policies? recovery evaluation? organizational roles?).
**Seed hypothesis under test:** organizational failure propagation and recovery in LLM MAS — what determines "organizational blast radius" across role/communication/authority/tool/memory/accountability/human boundaries, and which containment/recovery mechanisms minimize systemic impact while preserving task utility.

**Verification methods used:** arXiv API + abstract pages + full-text HTML, OpenReview API (api2.openreview.net/notes/search), Semantic Scholar API (paper search + citations endpoints). DBLP blocked by Anubis anti-bot; Google/Bing/DuckDuckGo search blocked or polluted. All papers below were verified against primary pages, not search snippets.

---

## 1. Bottom line

- **MAS-FIRE and AgentChaos both exist and are verified.** They are the two pillars of the 2026 LLM-MAS fault-injection line. Neither kills nor subsumes the seed hypothesis.
- **"IMACS related to multi-agent fault injection" is a FALSE LEAD.** The only verified IMACS is the *Intelligent Multi-Agent Collaboration System* (arXiv:2607.25446), an organizational-design framework with **no fault-injection content**. It is, however, directly relevant adjacent work for the seed's organizational layer (executable Belbin/Mintzberg/RACI configuration).
- **None of the verified works design or evaluate containment policies, compare recovery mechanisms as an independent variable, or measure blast radius across organizational boundaries.** They measure task-success degradation under injected faults and observe *emergent* fault tolerance. The seed's core gap remains open.
- **One terminological collision to note:** DamageFlow/BlastGuard (ICML 2026 AIWILD workshop) already uses "blast radius" (Blast Radius Score) + containment runtime + utility preservation — but in the *adversarial security* domain (prompt injection, MCP tool poisoning), single-agent tool-use centric. The seed must differentiate from this.

---

## 2. Mandatory paper records

### 2.1 MAS-FIRE — VERIFIED

| Field | Value |
|---|---|
| Title | MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems |
| Authors | Jin Jia, Zhiling Deng (equal contribution), Zhuangbin Chen (corresponding), Yingqi Wang, Zibin Zheng |
| Affiliation | Sun Yat-sen University, Zhuhai, China |
| Date | 2026-02-23 (v1, only version) |
| Venue | arXiv preprint; no venue listed as of 2026-09-21. PDF is ACM-formatted with placeholder conference text ("Make sure to enter the correct conference title… June 03–05, 2026; Woodstock, NY"), i.e., formatted for an ACM submission, venue unconfirmed |
| ID | arXiv:2602.19843 [cs.SE, cs.AI]; DOI 10.48550/arXiv.2602.19843 |
| URL | https://arxiv.org/abs/2602.19843 |

- **Research problem:** MAS coordinate via unstructured natural language, so semantic failures (hallucination, misinterpreted instructions, reasoning drift) propagate silently without runtime exceptions. Outcome-only metrics (task success) cannot diagnose how failures arise or whether agents recover.
- **Method:** Fault-injection + reliability-evaluation framework. Taxonomy of **15 fault types**: intra-agent cognitive (planning, memory, reasoning, action) and inter-agent coordination (configuration, instruction, communication). Three non-invasive injection mechanisms: **prompt modification, response rewriting, message routing manipulation**. Dual-level metrics: system-level resilience RS_f (task success under fault f); process-level O_f (fault-tolerant-behavior occurrence/detection rate), L_f (local success rate), S_f. Observed fault-tolerant behaviors organized into **four tiers: mechanism, rule, prompt, reasoning**.
- **Experimental setting:** Three MAS architectures — **MetaGPT** (hierarchical org workflow, shared message pool, linear pipeline) on HumanEval; **Table-Critic** (iterative critique-refinement loop) on WikiTableQuestions (400 sampled of 4,344); **Camel** (linear bilateral) on WebShop. Two backbone models: GPT-5 and DeepSeek-V3. 99% injection success rate.
- **Major findings:**
  - Stronger foundation models do **not** uniformly improve robustness.
  - **Topology is decisive:** iterative closed-loop designs neutralize >40% of faults that cause catastrophic collapse in linear workflows. MetaGPT linear pipeline drops to RS_f = 0.0% under "Blind Trust" configuration faults.
  - Configuration/Instruction faults are most severe (corrupt semantic foundations; RS ≤ 13.7–40%); Communication faults are least destructive (RS > 93% in MetaGPT) because hard-wired rule-based filtering (dedup, cycle detection) neutralizes them deterministically.
  - **Blind-Trust paradox:** GPT-5's stricter instruction adherence caused near-total collapse (RS 6.32%) where DeepSeek-V3's weaker compliance preserved function (RS 70.61%).
  - Reasoning-level FT is the only defense against semantic faults (hallucination, instruction conflict/ambiguity), with universal activation (O_f=100%) but variable success.
- **Author-stated limitations:** No explicit limitations section; "Data Availability" section is **empty**. Discussion notes linear-workflow vulnerability and recommends multi-source validation + inline verification checkpoints (as design guidance, not evaluated interventions).
- **My inferred limitations:** (a) Only 3 architectures, one benchmark each — architecture and domain confounded. (b) "Recovery" is observed emergent behavior, not an evaluated design variable — no containment/recovery mechanism is proposed and compared. (c) No organizational constructs beyond coarse topology (no authority/delegation, accountability, memory-boundary, or human-agent boundary faults). (d) Faults are single-type injections; no compound/cascading fault scenarios. (e) No code/data released (empty Data Availability).
- **Code availability:** None stated (empty Data Availability section in v1).
- **Relationship to seed hypothesis:** Closest existing work on the "what determines spread" question — establishes that topology modulates fault impact and provides process-level detection/recovery metrics (O_f, L_f). But it is **diagnostic/observational**: it catalogs emergent fault tolerance rather than evaluating containment policies, and its boundaries are architectural (linear vs. closed-loop vs. bilateral), not organizational (role/authority/accountability/memory/human). Does NOT subsume the seed.

### 2.2 AgentChaos — VERIFIED

| Field | Value |
|---|---|
| Title | AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection |
| Authors | Gou Tan, Zhensu Sun, Jieke Shi, Ting Zhang, Zilong He, Qingfu Wu, Shuai Liang, Weifeng Sun, Junda He, Pengfei Chen (corresponding), Chuanfu Zhang, Lwin Khin Shar, David Lo |
| Affiliations | Singapore Management University; Sun Yat-sen University; Monash University; China Unicom |
| Date | 2026-08-07 (v1); received 2026-06-18 |
| Venue | **ASE 2026** (41st IEEE/ACM Int. Conf. on Automated Software Engineering), Munich, Oct 12–16, 2026 |
| ID | arXiv:2608.06790 [cs.SE]; DOI 10.48550/arXiv.2608.06790; proceedings DOI 10.1145/3832783.3837437 |
| URL | https://arxiv.org/abs/2608.06790 |

- **Research problem:** Agent systems depend on LLM APIs that return server errors, truncated responses, corrupted content; these propagate to downstream agents. Existing injection methods are offline (AgenTracer, AutoInject), intrusive (MAS-FIRE), or cannot modify specific response fields (Rainmaker, ChaosBlade, CrashFuzz).
- **Method:** Chaos-engineering framework injecting faults at the shared **HTTP layer** of LLM APIs — runtime, non-intrusive (no source-code modification). Taxonomy: **crash, omission, value faults** on **content** and **tool_calls** fields (6 types: error, timeout, empty, truncate, schema, corrupt). Injection strategies: single, persistent, intermittent, burst; position experiments (1st/2nd/3rd call); 8 compound scenarios → **65 fault configurations**. Trigger verification filters untriggered tasks to avoid underestimating impact.
- **Experimental setting:** Five systems reimplemented on Google ADK — AutoGen, MAD (multi-agent debate), MapCoder (pipeline), EvoMAC (iterative), Mini-SE (single-agent SWE) — on HumanEval, HumanEval+, MBPP, MMLU-Pro, MATH-500, SWE-bench Pro; four backbones (Claude-Sonnet-4.5, GPT-5.2, DeepSeek-V3.2, Seed-1.8); 300 samples/dataset; temperature 0.7; 3 independent seeds.
- **Metrics:** pass@1, Δpass@1 (degradation); fault-diagnosis type/step accuracy.
- **Major findings:**
  - All systems degrade; Δpass@1 up to **49.66pp** (MapCoder, HumanEval+, GPT-5.2). Robustness ranking (MapCoder worst → AutoGen best) **consistent across models → robustness is implementation-dependent, not model-dependent**.
  - **Pipeline systems most vulnerable:** a single fault at the first stage drops pass@1 by up to **83.87%**; iterative systems most robust (later rounds correct earlier faults).
  - Content faults hurt more than tool-call faults (tool error handling catches most); **severe ≠ harmful** — omission faults (truncate/empty) return HTTP 200, bypass error handling, and cause drops comparable to crash faults.
  - Persistent injection worst (up to 62.39%); compound content-modifying faults amplify (up to 86.36%).
  - **Fault diagnosis is poor:** rule-based 52.45% type / 55.5% step accuracy; LLM-based 47.25%/53.52% — neither exceeds 56%.
- **Author-stated limitations (Threats to Validity):** systems reimplemented on ADK (behavioral drift possible); ~4.6 triggered tasks per configuration → variance; **only one system per architectural pattern — cannot separate pattern effects from system effects** (they explicitly downgrade their ranking claim to "a pattern that holds consistently across the systems we test"); Δpass@1 misses partial correctness; RAG-based architectures not covered.
- **My inferred limitations:** (a) API-layer faults only — no semantic faults (hallucination, role ambiguity), which MAS-FIRE covers; the two are complementary, not overlapping. (b) No containment or recovery mechanism evaluation — future work only ("design and evaluate defense strategies that validate LLM API responses"). (c) No organizational roles/authority/accountability constructs. (d) Diagnosis evaluated only on Mini-SE/SWE-bench Pro.
- **Code availability:** **Yes** — Zenodo artifact (Tan et al. 2026c, "Artifact of paper 'AgentChaos…'", Zenodo; linked from paper §9).
- **Relationship to seed hypothesis:** Strongest evidence that *implementation/architecture, not model capability*, determines fault impact — supports the seed's premise that organizational/structural factors determine blast radius. But it evaluates degradation only; containment/recovery is explicitly future work; no organizational boundaries. Does NOT subsume the seed.

### 2.3 "IMACS related to multi-agent fault injection" — FALSE LEAD (name exists, fault-injection association does not)

| Field | Value |
|---|---|
| Title | Toward an Organizational Science of Multi-Agent LLM Systems: Decoupling Who, How, and Which Algorithm |
| System name | **IMACS = Intelligent Multi-Agent Collaboration System** |
| Authors | Submitted by Huan Chen; affiliations: Shunfeng Technology Co., Ltd., China; Shenzhen University, China |
| Date | 2026-07-28 (v1) |
| Venue | arXiv preprint, 8 pages; no venue listed |
| ID | arXiv:2607.25446 [cs.AI, cs.LG]; DOI 10.48550/arXiv.2607.25446 |
| URL | https://arxiv.org/abs/2607.25446 |

- **Search process:** arXiv API (`all:"IMACS"`, `ti:"IMACS"`, `all:"IMACS" AND all:"fault injection"`, `all:"IMACS" AND all:"multi-agent"`), OpenReview search (`IMACS`, `IMACS fault injection`, `IMACS multi-agent`, `IMACS agents`), Semantic Scholar (`IMACS multi-agent`, `IMACS fault injection`). No fault-injection work named IMACS found anywhere. The only IMACS in the LLM-MAS literature is this paper. (Unrelated: "IMAC: Intelligent Multi-Agent Content Steering for DASH", Mile-High Video Conf. 2025 — video streaming.)
- **What IMACS actually is:** A framework decoupling **organization (WHO: Belbin roles, model bindings, RACI accountability)**, **coordination (HOW: Mintzberg's five mechanisms)**, and **collaboration protocol (WHICH: voting, MoA, blender, debate, reflexion, plan-execute)** into orthogonal, swappable layers on AgentScope 2.0, with an orthogonality proposition. Adaptive Org Routing (LinUCB contextual bandit, 7-dim task features) selects protocols per task under quality–cost trade-off; 82% routing accuracy on a controlled simulated oracle, beats all six fixed protocols.
- **Key finding relevant to seed:** Controlled RACI ablations (3 repeats) show **accountability placement changes outcomes exactly when the protocol routes the deliverable through the accountable agent** (LLM-Blender: paired Critic−Chair gap +0.08±0.02, sign-consistent in 3/3 repeats; MoA control shuffles), operating by changing which model does the work; the winning placement **flips across model families** → organizational design cannot be hard-coded, must be revalidated/learned per model binding.
- **Author-stated limitations:** synthetic oracle for regret study; small-N real runs (N=10/cell, 3 repeats); **"they do not cover long-horizon tool use, human approval loops, or failures caused by changing external state"**; English-centric features; AgentsNet evaluated as whole-graph deliverable.
- **Relationship to seed hypothesis:** No fault injection, no failure propagation, no recovery — the assignment's premise is wrong. BUT it is the only work making **organizational theory (Belbin/Mintzberg/RACI) an executable, validated configuration layer** — a natural substrate for the seed's organizational-blast-radius manipulations, and its "accountability placement matters only when the deliverable routes through the accountable agent" result is direct evidence that organizational structure modulates outcome sensitivity. Adjacent, complementary, potentially citable as the org-design layer the seed stresses under faults.

---

## 3. The fault-injection line: full verified map

### 3.1 Foundational / predecessor works (verified via citing papers' bibliographies + OpenReview)

| Paper | Venue/ID | What it does | What it does NOT do |
|---|---|---|---|
| **On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents** (AutoTransform + **AutoInject**); Jen-tse Huang, Jiaxu Zhou, Tailin Jin, Xuhui Zhou, Zixi Chen, Wenxuan Wang, Youliang Yuan, Michael Lyu, Maarten Sap | **ICML 2025** poster; OpenReview bkiM54QftZ; code: github.com/CUHK-ARISE/MAS-Resilience | Injects "faulty agent" behavior (AutoTransform rewrites role to secretly err; AutoInject slips errors into messages); 4 tasks, 6 systems; **hierarchical A→(B↔C) most resilient (5.5% drop vs 10.5% flat / 23.7% chain)**; proposes **Challenger** (agents challenge each other) and **Inspector** (reviewer agent) recovering **up to 96.4%** of errors | Persistent faulty-agent model (clumsy/malicious), not transient local faults; toy 3-agent structures, not organizational workflows; only 2 recovery mechanisms; no authority/memory/accountability/human boundaries; offline trace-level analysis per AgentChaos's characterization |
| **AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?**; G. Zhang et al. | arXiv:2509.03312 (2025) | Offline: LLM perturbs completed execution traces, replays to build fault datasets for failure attribution | Offline only — no runtime behavior (retries, early termination); attribution, not containment/recovery |
| **Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems**; S. Zhang et al. | ICML 2025 | Failure attribution (which agent, which step) | Attribution only; no injection control, no recovery |
| Rainmaker (Chen et al. 2023); CrashFuzz (Gao et al. 2023); ChaosBlade | — | Infrastructure-layer fault injection (HTTP 503/timeout; crash/reboot; OS/container/network) | Cannot modify LLM response-body fields; no agent semantics |

### 3.2 2026 successors and adjacent works (all verified against primary pages)

| Paper | Venue/ID | Relevance to fault-injection line | Relationship to seed |
|---|---|---|---|
| **AgentChaos** | ASE 2026; arXiv:2608.06790 | The direct 2026 successor: runtime, non-intrusive, API-layer | See §2.2 — degradation only, no containment/recovery |
| **Efficient Forecasting of Task Failures in LLM Agents through Adaptive Fault Injection**; Sengar, Thakkar, Panda, Satapara, Liu, Viswanathan, Takemori, Neubig, Devaguptapu | **Forecast@ICML26** poster; OpenReview d3Qq4weuwz | Uses **adaptive fault injection** (bandit-prioritized perturbations of successful traces, verified via rollouts) to train a failure forecaster (Qwen-3-8B, 78.01% weighted F1, beats Claude-4.5 Sonnet by 18 pts at 100× lower cost); improves agent success 2–16pp | Single-agent long-horizon focus; forecasting for runtime intervention, not organizational containment; "recoverable vs fatal" distinction is seed-adjacent |
| **FAIR-Swarm: Fault-Tolerant Multi-Agent LLM Systems for Scientific Hypothesis Discovery**; Mahule Roy, Subhas Roy | **LaMAS 2026** poster (AAAI workshop); OpenReview 6WyG2iZHes | Fault-tolerant MAS architecture: specialized agents (Hypothesis Generator, Simulation, Validation, Rebuttal, Reasoning Auditor) + **redundancy and consensus-based fault tolerance** against failure cascades | Domain-specific (scientific discovery); architecture proposal, no systematic blast-radius measurement; no code |
| **Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance**; Lifan Zheng, Jiawei Chen, Qinghong Yin, Jingyuan Zhang, Xinyi Zeng, Yu Tian | **AAAI 2026**; OpenReview gEnIqziV8j | Quantifies LLM-agent reliability via BFT lens across topologies; **CP-WBFT** confidence-probe weighted BFT consensus; works under 85.7% fault rate | Consensus-layer robustness to Byzantine (worst-case adversarial) faults; topology studied as network structure, not organizational roles/authority; no recovery/utility trade-off |
| **What Can One Bad Tool Call Destroy? Measuring and Minimizing Blast Radius in Agentic Tool Use** (DamageFlow + BlastGuard); Muhammet Anil Yagiz | **ICML 2026 AIWILD** workshop; OpenReview MYvsxnxbCf | **Terminological collision: "Blast Radius Score (BRS)"** decomposing unauthorized tool effects by resource sensitivity, action impact, propagation, recovery cost; **BlastGuard** containment runtime (least-privilege capability graphs, provenance tracking, dry-run/policy gates, scoped tokens, rollback); 80-scenario pilot; same 20% attack-success → 89× BRS difference; 87.5% benign utility retained | **Adversarial security domain** (indirect prompt injection, MCP tool poisoning, tool shadowing, multi-agent relay); single-agent tool-use centric; "blast radius" = unauthorized state mutation, not organizational fault spread. The seed must differentiate: non-adversarial faults, organizational boundaries, MAS workflow setting |
| **Atomix: Timely, Transactional Tool Use for Reliable Agentic Workflows** | arXiv:2602.14849 v2 (2026-05-29); cs.LG/AI/DC/MA | Progress-aware **transactions** for tool effects: seal when footprint complete, commit after per-resource frontiers clear, abort suppresses/compensates; evaluated under **injected faults** — "improves clean recovery", microsecond overhead | Tool-effect settlement/recovery mechanism (single-agent workflows + concurrent agents); no organizational layer; closest existing "recovery mechanism" work |
| **Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems** (H-RePlan + HeraBench) | arXiv:2606.20487 (2026-06-18); cs.CL | **HeraBench: fault-injected benchmark** (strategy- and device-level failures) for cross-device workflows; hierarchical recovery separating device-local strategy recovery from global replanning | Multi-device computer-use, not organizational MAS; recovery granularity (local vs global) is seed-adjacent |
| **CASPIAN: Online Detection and Attribution of Cascade Attacks in LLM Multi-Agent Systems** | arXiv:2605.19240 (2026-05-19); cs.MA | Cross-channel causal monitoring (LI-CTE transfer entropy influence matrix) for **cascade detection + attribution** (origin/bridge/amplifier agents, propagation pathways); sub-1% overhead | Adversarial cascade attacks; detection/attribution only, no containment evaluation |
| **VerifyMAS: Hypothesis Verification for Failure Attribution in LLM MAS** | arXiv:2605.17467 (2026) | Failure attribution via hypothesis verification | Attribution only |
| **MASPrism: Lightweight Failure Attribution for MAS Using Prefill-Stage Signals** | arXiv:2605.07509 (2026) | Lightweight failure attribution | Attribution only |
| **Instruction Bleed: Cross-Module Interference in Prompt-Composed Agentic Systems** | arXiv:2606.26356; **ICML 2026 FAGEN workshop** | Compositional behavioral leakage (CBL) between prompt modules sharing a context window; 3-channel perturbation protocol; Cohen's d=0.63 content-channel effect | Single-agent prompt modules; explicitly positions itself as orthogonal to "multi-agent fault propagation" |
| **ToMAS: A Pilot Failure-Grounded Theory-of-Mind Benchmark from Multi-Agent LLM Failures** | arXiv:2609.16986 (2026-09-15); cs.MA | Converts diagnosed inter-agent misalignment failures (MAST-Data FC2) into partner-state reasoning items; negative training result (LoRA update negligible) | Benchmark/pipeline; pilot-scale, no containment |

---

## 4. What the fault-injection line does NOT do (gap analysis vs. seed)

| Seed requirement | MAS-FIRE | AgentChaos | AutoInject (ICML'25) | DamageFlow (ICML'26w) | Anyone? |
|---|---|---|---|---|---|
| Fault/failure injection in LLM MAS | ✅ semantic, runtime, intrusive | ✅ API-layer, runtime, non-intrusive | ✅ faulty agents (offline-ish) | ✅ adversarial tool faults | covered |
| Topology/architecture modulates impact | ✅ (linear vs closed-loop) | ✅ (pipeline vs iterative) | ✅ (chain/flat/hierarchy) | partial | covered |
| Process-level detection/recovery metrics | ✅ O_f, L_f, S_f | partial (diagnosis accuracy) | ❌ | ✅ recovery cost in BRS | partial |
| **Containment policies as evaluated interventions** | ❌ (design guidance only) | ❌ (explicit future work) | partial (Challenger/Inspector, 2 mechanisms, toy structures) | ✅ BlastGuard (but security domain) | **OPEN (non-adversarial, organizational)** |
| **Recovery mechanism comparison + utility preservation trade-off** | ❌ emergent only | ❌ | partial (recovery % of errors) | ✅ (87.5% utility retained) | **OPEN** |
| **Blast radius measured across organizational boundaries (role/authority/delegation/memory/accountability/human)** | ❌ architectural boundaries only | ❌ call-chain position only | ❌ 3-agent graphs | partial (propagation + resource sensitivity, but tool-state not org) | **OPEN** |
| Organizational roles/authority/accountability constructs | ❌ | ❌ | ❌ | ❌ | **OPEN** (IMACS provides the org layer but no faults) |
| Human-agent boundary faults | ❌ | ❌ | ❌ | ❌ | **OPEN** |
| Memory-boundary faults (shared vs private memory corruption) | partial (memory faults = info loss) | ❌ | ❌ | ❌ | **mostly OPEN** |

---

## 5. Does anything here kill or subsume the seed hypothesis?

**No.** Detailed judgment:

1. **Not killed:** No verified work contradicts the seed's premise. On the contrary, MAS-FIRE (topology decisive; iterative loops neutralize 40%+ of faults), AgentChaos (implementation > model; pipeline first-stage fault → 83.87% drop), and AutoInject (hierarchy most resilient; Challenger/Inspector recover 96.4%) all *support* the premise that organizational/structural factors determine failure spread and that recovery mechanisms matter.

2. **Not subsumed:** The entire line is **diagnostic** (measure degradation, catalog emergent tolerance, attribute failures) — none evaluates **containment/recovery policies as the independent variable** in non-adversarial organizational settings, and none defines or measures an **organizational blast radius** across the seed's seven boundaries (role, communication, authority/delegation, tool, memory, accountability, human-agent). AutoInject's Challenger/Inspector is the closest recovery evaluation but uses 2 mechanisms on toy 3-agent structures with persistent faulty agents. AgentChaos explicitly lists defense evaluation as future work.

3. **Two differentiation obligations for the seed:**
   - **DamageFlow/BlastGuard (ICML 2026 AIWILD)** already owns "blast radius" + containment + utility-preservation framing in the *adversarial tool-use* domain. The seed must frame itself as the *non-adversarial, organizational* counterpart (faults from coordination failure, not attacks; spread across org boundaries, not tool state).
   - **IMACS (arXiv:2607.25446)** owns "executable organizational theory (Belbin/Mintzberg/RACI) for LLM MAS" — the seed should cite it as the org-design substrate and can position itself as stress-testing exactly those organizational constructs under faults, which IMACS explicitly leaves out of scope.

4. **Crowding note:** The failure-*attribution* sub-area is getting crowded in 2026 (AgenTracer, Which-Agent-ICML'25, VerifyMAS, MASPrism, CASPIAN, RAFFLES-EACL'26). A MASO submission should not be framed as attribution; the open lane is **containment/recovery policy evaluation with organizational blast-radius metrics**.

---

## 6. Verification log (sources actually inspected)

- arXiv abstract + full-text HTML: 2602.19843 (MAS-FIRE), 2608.06790 (AgentChaos), 2607.25446 (IMACS), 2602.14849 (Atomix), 2606.20487 (H-RePlan), 2605.19240 (CASPIAN), 2606.26356 (Instruction Bleed), 2609.16986 (ToMAS)
- OpenReview API records: bkiM54QftZ (AutoInject/ICML'25), d3Qq4weuwz (Forecast@ICML26), 6WyG2iZHes (FAIR-Swarm), gEnIqziV8j (CP-WBFT/AAAI'26), MYvsxnxbCf (DamageFlow)
- Semantic Scholar API: citations of arXiv:2602.19843 (11 citing works enumerated); citations of arXiv:2608.06790 (0 — too recent); search "IMACS multi-agent" (10 results, no fault-injection IMACS)
- Blocked/unusable: DBLP (Anubis anti-bot), Google/Bing/DuckDuckGo (JS challenge/polluted), arXiv API intermittent 429 after initial queries
