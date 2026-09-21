# B16 — Cost/Reliability Trade-offs in LLM (Multi-)Agent Systems

**Investigator:** Landscape B16 specialist
**Date:** 2026-09-21
**Assignment:** Map work on token cost, latency, cost-aware orchestration, model cascading/routing for cost, reliability-per-dollar. Determine whether the **cost of recovery** (tokens / tool calls / human time spent containing a fault) is measured anywhere.
**Seed hypothesis under test:** organizational failure propagation and recovery in LLM MAS — what determines "organizational blast radius," and which containment/recovery mechanisms minimize systemic impact while preserving task utility.

---

## 0. Bottom line

1. **The cost/reliability trade-off literature is large and mature for steady-state operation** (routing, cascading, test-time compute, cost-aware MAS topology design, cost-aware agent evaluation). Nothing there kills the seed hypothesis — it is about *normal-operation* efficiency, not *fault-recovery* efficiency.
2. **The cost of recovery is measured only in two narrow pockets:**
   - **AIOps/SRE incident agents**: AIOpsLab (arXiv 2501.06706) measures token cost of incident-handling episodes; ITBench (arXiv 2502.05352) measures MTTD/MTTR in seconds. Both treat the *whole incident episode* as the unit — neither isolates containment cost, compares recovery mechanisms on cost, nor counts human time.
   - **Failure attribution**: Who&When (arXiv 2505.00212) quantifies human hours for manual failure attribution (23–31 h per annotator) and API cost of automated attribution (Appendix D). This is *diagnosis* cost, not containment/execution cost.
3. **In the core LLM-MAS resilience literature, recovery cost is NOT measured.** The closest paper, "On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents" (arXiv 2408.00989), evaluates its Inspector/Challenger recovery mechanisms only on error-recovery rate (up to 96.4%); full-text inspection confirms zero token/dollar/latency analysis of the recovery mechanisms. MAST (arXiv 2503.13657) has no cost analysis of failures or recovery.
4. **Classical distributed-systems/MAS literature treats recovery cost as first-class** (checkpoint overhead: Young 1974, Daly 2006; microreboot "cheap recovery": Candea et al. OSDI 2004; recovery-oriented computing/MTTR: Patterson et al. 2002; plan-repair cost: van der Krogt & de Weerdt AAMAS 2005; workflow exception handling: Klein & Dellarocas 2000). This vocabulary and methodology is importable but has not been imported into LLM-MAS evaluation.
5. **Verdict for the seed: NOT killed, NOT subsumed.** A "cost-of-recovery / cost-of-containment vs. blast radius" study in organizational LLM MAS is a genuine measurement gap. The seed must differentiate from AIOpsLab/ITBench (SRE-domain recovery time/token measurement) and from arXiv 2408.00989 (structure→blast-radius via performance drop, no cost dimension).

---

## 1. Method and search-channel limitations

Verification channels used: arXiv abstract pages (direct fetch), arXiv HTML full text (for cost-metric inspection of key papers), CrossRef API (classical DOIs), OpenReview API (discovery + venue confirmation), OpenAI website (GDPval). Semantic Scholar API, OpenAlex, DBLP, DataCite, and arXiv full-text search were rate-limited/blocked from this network for most of the session; discovery therefore relied on OpenReview search plus targeted arXiv ID verification. Every paper cited below was verified by inspecting its actual abstract page or publisher record — no citation is taken from search snippets alone. Items I could not verify are listed in §7 and excluded from the evidence tables.

Terminology coverage for the recovery-cost question (all searched, mostly via OpenReview full-text search): "cost of recovery", "recovery cost multi-agent LLM", "mean time to recovery agent", "human intervention cost LLM agent", "self-healing multi-agent LLM systems", "containment failure propagation agent", "fault injection LLM agents", "rollback checkpoint LLM agent recovery", "transactional LLM agent compensating action", "oversight cost AI agent monitoring", "budget-constrained LLM agent cost-aware orchestration", "reliability per dollar", "blast radius agent". Absence of hits on all of these (beyond the items reported here) is weak-but-real evidence of a gap; see §7 caveats.

---

## 2. Landscape map

### 2A. Single-model cost routing & cascading (cost vs. quality at the LLM call level)

| Paper | ID / venue | Problem & method | Setting & metrics | Key findings | Limitations (stated + inferred) | Relation to seed |
|---|---|---|---|---|---|---|
| FrugalGPT (Chen, Zaharia, Zou) | arXiv 2305.05176, May 2023 | Reduce LLM inference cost via prompt adaptation, LLM approximation, learned LLM cascade | HEADLINES etc.; cost ($) vs accuracy | Matches GPT-4 with up to 98% cost reduction, or +4% accuracy at same cost | Cascade errors compound; no fault/recovery model | Establishes cost-quality cascade primitive; recovery = "escalate to stronger model" is a costed fallback, but failure-driven escalation not studied |
| RouteLLM (Ong et al.) | arXiv 2406.18665, Jun 2024 (v4 Feb 2025) | Learn routers between strong/weak LLM from preference data | MT-Bench etc.; cost reduction at iso-quality | >2× cost reduction without quality loss; routers transfer across model swaps | Binary routing; no reliability/fault framing | Routing is a *prevention* lever, not recovery |
| Hybrid LLM (Ding et al.) | arXiv 2404.14618, ICLR 2024 | Route by predicted query difficulty with tunable quality level | 40% fewer large-model calls at no quality drop | Quality-cost dial at test time | Difficulty prediction errors | Same as above |
| LLM Cascades w/ Mixture-of-Thoughts (Yue et al.) | arXiv 2310.03094, ICLR 2024 | Defer to strong LLM when weak LLM's answer consistency is low | 6 reasoning benchmarks; GPT-3.5→GPT-4; cost vs accuracy | Comparable performance at 40% of cost | Consistency is a proxy for difficulty, not correctness | "Escalation on uncertainty" is the closest classical analogue to costed recovery-from-suspected-error; still not framed as fault containment |
| EcoAssistant (Zhang et al.) | arXiv 2310.03046, Oct 2023 (LLMAgents@ICLR 2024) | Code-driven QA: executor loop + LLM hierarchy + solution retrieval | Success rate vs $ cost | +10 pts over GPT-4 at <50% of its cost | Iterative code refinement cost grows with failures | Retry/refinement loop cost is implicit, not isolated |
| GraphRouter (Feng et al.) | arXiv 2410.03834, Oct 2024 | Inductive graph router over task/query/LLM nodes, predicts effect & cost | 3 effect-cost weight scenarios | ≥12.3% improvement over routers; generalizes to new LLMs | — | Steady-state routing |

### 2B. Test-time compute & reasoning-cost control (reliability-per-token at the single-model level)

| Paper | ID / venue | Contribution | Metrics | Findings | Relation to seed |
|---|---|---|---|---|---|
| Snell et al., "Scaling LLM Test-Time Compute Optimally…" | arXiv 2408.03314, Aug 2024 | Compute-optimal allocation of test-time compute per prompt difficulty | FLOPs-matched accuracy | >4× efficiency vs best-of-N; small model + compute can beat 14× larger model | Compute allocation ≠ fault recovery, but provides the "where to spend repair compute" substrate |
| Large Language Monkeys (Brown et al.) | arXiv 2407.21787, Jul 2024 | Repeated sampling scaling laws | Coverage vs #samples (cost) | Coverage log-linear over 4 orders of magnitude; SWE-bench Lite 15.9%→56% with 250 samples; verifier-free selection plateaus | Retry-as-recovery has power-law cost; selection failure = recovery failure mode |
| s1: budget forcing (Muennighoff et al.) | arXiv 2501.19393, Jan 2025 | Force terminate/extend reasoning ("Wait") | AIME/MATH accuracy vs token budget | s1-32B > o1-preview by up to 27% | Token budget as explicit control knob |
| TALE: Token-Budget-Aware Reasoning (Han et al.) | arXiv 2412.18547, Dec 2024 | Prompt-injected token budget, dynamic per question | Token cost vs accuracy | Large token reduction, slight accuracy loss | Budget awareness; used as TALE-EP in cost-of-pass paper |
| Chain of Draft (Xu et al.) | arXiv 2502.18600, Feb 2025 | Minimalist intermediate steps | Tokens, cost, latency vs accuracy | Matches CoT with as little as 7.6% of tokens | Latency explicitly costed |
| Overthinking of o1-like LLMs (Chen et al.) | arXiv 2412.21187, Dec 2024 | First study of overthinking; efficiency metrics (outcome & process) | GSM8K/MATH500/GPQA/AIME | Self-training reduces compute without accuracy loss | Efficiency metrics for reasoning |
| TokenSkip (Xia et al.) | arXiv 2502.12067, EMNLP 2025 | Controllable CoT compression | Token usage vs performance | −40% reasoning tokens, <0.4% drop | — |
| O1-Pruner (Luo et al.) | arXiv 2501.12570, Jan 2025 | Length-harmonizing RL fine-tune | Inference overhead vs accuracy | Lower overhead, higher accuracy | — |

### 2C. Cost-aware multi-agent orchestration & topology (the core MAS cost literature)

| Paper | ID / venue | Problem & method | Setting & metrics | Key findings | Limitations | Relation to seed |
|---|---|---|---|---|---|---|
| AgentPrune — "Cut the Crap" (Li, Zhang et al.) | arXiv 2410.02506, ICLR 2025 | Defines communication redundancy in MAS; one-shot spatial-temporal graph pruning | 6 benchmarks; $ cost, token reduction, adversarial robustness | $5.6 vs $43.7 for SOTA topologies; 28.1–72.8% token reduction; +3.5–10.8% under adversarial attack | Pruning is static per-task; attack model = malicious messages, not organic faults | **Closest cost+robustness intersection**: cheaper communication graphs that also resist adversarial agents — but robustness measured as accuracy retention, not recovery cost |
| DyLAN (Liu et al.) | arXiv 2310.02170, COLM 2024 | Agent selection via Agent Importance Score + dynamic communication | Code/decision/reasoning; accuracy, "moderate computational cost" | +25% MMLU subjects via team optimization | Cost reported qualitatively | Team composition as cost lever |
| G-Designer (Zhang et al.) | arXiv 2410.11782, Oct 2024 | VGAE designs task-adaptive communication topology | 6 benchmarks; accuracy, token consumption, adversarial robustness | −95.33% tokens on HumanEval; 0.3% accuracy drop under attack | — | Topology ↔ cost ↔ robustness triad, no recovery |
| AFlow (Zhang et al.) | arXiv 2410.10762, ICLR 2025 | MCTS search over code-represented workflows | 6 benchmarks; accuracy, $ inference cost | Small models beat GPT-4o at 4.55% of its cost | Search cost itself is large | Workflow optimization for cost |
| MaAS (Zhang et al.) | arXiv 2502.04180, Feb 2025 | Agentic supernet; query-dependent architecture sampling | 6 benchmarks; inference cost (LLM calls, tool calls, tokens) | 6–45% of baselines' cost, +0.54–11.82% performance | — | Per-query resource allocation |
| MAS-Zero (Ke et al.) | arXiv 2505.14996, May 2025 (SEA@NeurIPS 2025 oral) | Inference-time self-evolved MAS design, no validation set; can reduce to simpler systems | Reasoning/coding/agentic benchmarks; accuracy + "cost efficiency" | +16.69% avg accuracy; maintains cost efficiency | Meta-design adds its own tokens | Dynamic decomposition; cost-aware but fault-agnostic |
| MasRouter (Yue/Zhang et al.) | arXiv 2502.11133, Feb 2025 | Defines MAS Routing (MASR): collaboration mode + role allocation + LLM routing via cascaded controller | MBPP/HumanEval; performance, overhead | +1.8–8.2% over SOTA; −52.07% overhead; plug-and-play −17–28% | — | First unified cost-routing for MAS |
| GPTSwarm (Zhuge et al.) | arXiv 2402.16823, ICML 2024 | Agents as optimizable computational graphs; node+edge optimization | QA etc. | Automatic orchestration improvement | — | Graph optimization substrate |
| MacNet (Qian et al.) | arXiv 2406.07155, ICLR 2025 | DAG-organized collaboration >1000 agents; collaborative scaling law | Performance vs #agents | Logistic growth; irregular topologies better | Cost of 1000-agent runs not the focus | Scaling law without cost law |
| Mixture-of-Agents (Wang et al.) | arXiv 2406.04692, Jun 2024 | Layered LLM aggregation | AlpacaEval 2.0 etc. | 65.1% vs GPT-4o 57.5% | Cost critique followed in later work | — |
| More Agents Is All You Need (Li et al.) | arXiv 2402.05120, TMLR | Sampling-and-voting agent forest | Accuracy vs #agents | Performance scales with agent count | Linear cost growth | — |
| Corex (Sun et al.) | arXiv 2310.00280, COLM 2024 | Debate/Review/Retrieve multi-model paradigms | Reasoning tasks; cost-effectiveness analysis | Better performance + cost-effectiveness | — | — |
| Multiagent Debate (Du et al.) | arXiv 2305.14325, May 2023 | Multi-round debate | Factuality/reasoning | Improves accuracy | Token cost multiplies with rounds (later quantified by others) | — |
| AutoGen (Wu et al.) | arXiv 2308.08155, Aug 2023 | Framework | — | — | — | Infrastructure |
| ChatDev (Qian et al.) | arXiv 2307.07924, ACL 2024 | Role-played software company | Software generation | — | — | Organizational role structure (seed-relevant setting) |
| MetaGPT (Hong et al.) | arXiv 2308.00352, Aug 2023 | SOP-encoded workflows; notes "cascading hallucinations" from naive chaining | SWE benchmarks | SOPs reduce error cascades | — | **Explicitly motivated by error propagation across roles** — organizational blast radius in embryo, no cost measurement |

### 2D. Cost-aware agent evaluation & reliability-per-dollar metrics

| Paper | ID / venue | Contribution | Metrics | Findings | Relation to seed |
|---|---|---|---|---|---|
| AI Agents That Matter (Kapoor et al.) | arXiv 2407.01502, Jul 2024 | Critique of accuracy-only agent eval; joint cost+accuracy optimization | Cost-controlled accuracy; Pareto | SOTA agents needlessly complex/costly; simple optimizations cut cost at iso-accuracy | Foundational: cost must be co-measured; does not treat faults |
| **Cost-of-Pass** (Erol, El, Suzgun, Yuksekgonul, Zou) | arXiv 2504.13359, Apr 2025 | **Formalizes cost-of-pass = expected $ cost of generating a correct solution; frontier cost-of-pass vs human-expert hiring cost** | cost-of-pass across model classes & tasks | Lightweight models best for basic quant, reasoning models for complex quant; frontier cost halves every few months; majority voting/self-refinement gains rarely justify their cost | **The "reliability-per-dollar" metric.** Directly reusable to define "cost-of-recovery" = expected $ to restore correct execution after fault. Not yet applied to faults |
| Efficient Agents (Wang et al.) | arXiv 2508.02694, Jul 2025 | First systematic efficiency-effectiveness study of agent frameworks | cost-of-pass on GAIA | Efficient Agents retains 96.7% of OWL performance, $0.398→$0.228 (−28.4% cost-of-pass) | Applies cost-of-pass to agents; no fault dimension |
| Agentless (Xia et al.) | arXiv 2407.01489, Jul 2024 | 3-phase localization-repair-validation, no agent loop | SWE-bench Lite; % resolved + $ per task | 32% at $0.70 — best performance *and* lowest cost vs open-source agents | Shows agentic loops' cost can exceed their value |
| TheAgentCompany (Xu et al.) | arXiv 2412.14161, Dec 2024 | Simulated software company benchmark | Task completion; cost per task reported | Best agent completes 30% autonomously | Organizational setting; cost reported per task |
| OpenHands (Wang et al.) | arXiv 2407.16741, ICLR 2025 | Open agent platform | 15 benchmarks incl. SWE-bench, WebArena; cost per instance reported | — | — |
| SWE-Lancer (Wang et al., OpenAI) | arXiv 2502.12115, Feb 2025 | 1,400 Upwork tasks, $1M real payouts | $ earned | Frontier models can't solve most tasks | Dollar-denominated reliability |
| HCAST (Rein et al., METR) | arXiv 2503.17354, Mar 2025 | 189 tasks with 563 human baselines (1500+ h) | Human time vs agent success | Agents: 70–80% success on <1h-human tasks; <20% on >4h tasks | Human time as calibration; not containment time |
| RE-Bench (Wijk et al., METR) | arXiv 2411.15114, Nov 2024 | 7 AI-R&D environments vs 71 human expert attempts | Score vs time budget; notes agents "generate and test solutions 10× faster than humans, at much lower cost" | Agents win at 2h, humans at 32h | Human-vs-agent time/cost comparison |
| METR time horizon (Kwa et al.) | arXiv 2503.14499, NeurIPS 2025 | 50%-task-completion time horizon | Human-time horizon; doubling ~every 7 months | Horizon growth driven by "reliability and ability to adapt to mistakes" | **Recovery-from-mistakes identified as a capability driver — but measured as success, not cost** |
| GDPval (OpenAI) | openai.com/index/gdpval, Sep 2025 | 1,320 tasks across 44 occupations / 9 GDP sectors | Expert-graded win/tie vs humans; speed & cost comparison | Frontier models ~100× faster and ~100× cheaper than experts — **explicitly caveated: excludes human oversight, iteration, integration costs** | The human containment/oversight cost is acknowledged as the unmeasured residual |

### 2E. MAS failure, resilience & fault attribution (blast-radius side, mostly without cost)

| Paper | ID / venue | Contribution | Metrics | Findings | Recovery-cost content |
|---|---|---|---|---|---|
| MAST — Why Do Multi-Agent LLM Systems Fail? (Cemri et al.) | arXiv 2503.13657, Mar 2025 | 14-mode failure taxonomy; MAST-Data 1600+ traces, 7 frameworks | Taxonomy frequency; LLM-judge agreement (κ=0.88) | Failures in system design, inter-agent misalignment, verification; verification failures let errors "propagate undetected" | **None** (full-text checked: no cost/recovery analysis) |
| Resilience of LLM-MAS w/ Faulty Agents (Huang et al.) | arXiv 2408.00989, Aug 2024 | AutoTransform/AutoInject fault injection; structure comparison; Challenger & Inspector recovery mechanisms | Performance drop by structure; % errors recovered | Hierarchical structure most resilient (5.5% vs 23.7% drop); Inspector recovers up to 96.4% of errors | **None** (full-text checked: no token/$/latency analysis of Inspector/Challenger; "cost" appears only re: experiment budget) |
| Who&When (Zhang et al.) | arXiv 2505.00212, Apr 2025 (ICML 2025) | Automated failure attribution dataset (127 MAS) + 3 methods | Agent accuracy 53.5%, step accuracy 14.2% | Even o1/R1 fail at practical usability | **Partial**: annotation labor measured in human hours (30.9/30.2/23.2 h); Appendix D "Brief Cost Analysis" of attribution API cost |
| AgenTracer (Zhang et al.) | arXiv 2509.03312, Sep 2025 | Counterfactual replay + programmed fault injection; TracerTraj; AgenTracer-8B | Attribution accuracy on Who&When | +18.18% over Gemini-2.5-Pro/Claude-4-Sonnet; feedback gives MetaGPT/MaAS +4.8–14.2% | Lightweight 8B tracer framed as *efficient* diagnosis; no explicit $ accounting of repair loop |
| TRAIL (Deshpande et al.) | arXiv 2505.08638, May 2025 | 148 human-annotated traces; error taxonomy | Trace debugging accuracy | Best model (Gemini-2.5-pro) scores 11% | Motivated by manual trace analysis not scaling; no cost quantification |
| Multi-Agent Risks from Advanced AI (Hammond et al.) | arXiv 2502.14143, Feb 2025 (Cooperative AI Foundation TR#1) | Risk taxonomy: miscoordination/conflict/collusion + 7 risk factors | — | Conceptual | Names destabilizing dynamics; no measurement |

### 2F. Defense/containment mechanisms and their overhead (prompt-injection line)

| Paper | ID / venue | Mechanism | Trade-off measured | Cost accounting |
|---|---|---|---|---|
| AgentDojo (Debenedetti et al.) | arXiv 2406.13352, Jun 2024 (NeurIPS 2024 D&B) | Benchmark: 97 tasks, 629 attack cases | Utility vs attack success | No $ cost axis |
| MELON (Zhu et al.) | arXiv 2502.05174, ICML 2025 | Masked re-execution + tool comparison to detect IPI | Detection/utility on AgentDojo | Re-execution implies ~2× trajectory cost; overhead not reported as a headline metric |
| CaMeL (Debenedetti et al., Google DeepMind) | arXiv 2503.18813, Mar 2025 | Control/data-flow extraction + capabilities | 77% task success with provable security vs 84% undefended | Utility tax quantified; compute/token overhead not the focus |

### 2G. AIOps / incident-management agents — the one place recovery IS measured

| Paper | ID / venue | Setting | Recovery-relevant metrics | What is NOT measured |
|---|---|---|---|---|
| AIOpsLab (Chen/Shetty et al., Microsoft) | arXiv 2501.06706, Jan 2025 | Deployable microservice env, fault injection, incident lifecycle (detection→localization→RCA→mitigation); "AgentOps"/self-healing clouds vision | **Token cost (input+output) of the incident episode; Time-to-Detect; steps; success** | Cost decomposition (containment vs diagnosis vs fix); mechanism comparison on cost; human time; blast radius |
| ITBench (Jha et al., IBM + UIUC) | arXiv 2502.05352, Feb 2025 | 94 real-world IT scenarios (SRE/CISO/FinOps), fault injection | **MTTD (s), MTTR (s), pass@1, fault-propagation-chain metric (NTAM)** | Token/$ cost of mitigation; human time; cost vs spread trade-off |
| RCAgent (Wang et al., Alibaba) | arXiv 2310.16340, CIKM 2024 | Tool-augmented RCA agent, deployed on Flink platform | RCA accuracy (root cause, solution, evidence, responsibility) | Recovery cost |
| (Practitioner context) "Observability for LLMs: SRE and Chaos Engineering for AI at Scale" | 2026 book, SSRN 10.2139/ssrn.5882002 + Springer chapters | Chaos engineering for LLM systems | — | Practitioner, not experimental |

### 2H. Classical recovery-cost literature (pre-LLM; methodology importable)

| Work | Venue / ID | Recovery-cost content |
|---|---|---|
| Young, "A first order approximation to the optimum checkpoint interval" | CACM 1974, DOI 10.1145/361147.361115 | Optimal checkpoint interval trading checkpoint overhead vs lost rework — the original recovery-cost optimization |
| Daly, "A higher order estimate of the optimum checkpoint interval for restart dumps" | FGCS 2006, DOI 10.1016/j.future.2004.11.016 | Refined checkpoint-cost model |
| Candea et al., "Microreboot—A Technique for Cheap Recovery" | OSDI 2004 (usenix.org/legacy/events/osdi04/tech/candea.html) | Fine-grain recovery an order of magnitude faster with order-of-magnitude savings in lost work; "cheap recovery enables recover-at-slightest-hint" — **directly analogous to cheap-containment-enables-early-containment** |
| Patterson et al., "Recovery Oriented Computing (ROC): Motivation, Definition, Techniques, and Case Studies" | UC Berkeley TR UCB/CSD-02-1175, 2002 (book-chapter version: Building Dependable Distributed Systems 2014, DOI 10.1002/9781118912744.ch3) | MTTR over MTBF as the design objective; recovery as first-class systems metric |
| Klein & Dellarocas, "A Knowledge-Based Approach to Handling Exceptions in Workflow Systems" | CSCW 2000, DOI 10.1023/a:1008759413689 | Exception detection/diagnosis/resolution taxonomy for workflows — organizational exception handling |
| van der Krogt & de Weerdt, "Multiagent planning through plan repair" | AAMAS 2005, DOI 10.1145/1082473.1082761 | Plan repair vs replanning cost in multi-agent plans |
| Hägg, "A sentinel approach to fault handling in multi-agent systems" | LNCS 1997, DOI 10.1007/bfb0030090 | Sentinel agents dedicated to fault handling in MAS |

---

## 3. The assigned question: is the cost of recovery measured anywhere?

**Answer: partially, in three pockets — but nowhere in the form the seed hypothesis needs.**

1. **As wall-clock time (SRE domain).** ITBench measures MTTD and MTTR in seconds for LLM agents mitigating injected faults; AIOpsLab measures Time-to-Detect and episode length. This is genuine recovery-cost measurement, but (a) time only, (b) cloud-incident domain, (c) no comparison of alternative containment/recovery mechanisms on cost, (d) no human time.
2. **As episode token cost (SRE domain).** AIOpsLab explicitly defines cost = input+output tokens generated during the incident episode. Still episode-total: the marginal token cost attributable to the fault (vs. fault-free execution) and the cost of *containment choices* (isolate? retry? escalate to human?) are not isolated.
3. **As diagnosis cost (MAS debugging domain).** Who&When quantifies human annotation hours for manual failure attribution (23–31 h/annotator) and API cost of automated attribution; AgenTracer frames an 8B tracer as efficient diagnosis. Diagnosis is one component of recovery cost; containment execution and utility loss during propagation are not costed.

**Explicitly NOT measured anywhere found:**
- Token/tool-call/$ cost of a *recovery or containment mechanism* in general-purpose or organizational LLM MAS (verified by full-text inspection of the closest candidate, arXiv 2408.00989: Inspector recovers 96.4% of errors, zero cost analysis).
- Human time spent containing agent faults. GDPval explicitly excludes "human oversight, iteration, and integration" from its 100× cheaper/faster claim — the oversight residual is acknowledged and unmeasured. HCAST/RE-Bench measure human time for *tasks*, not for *supervising or repairing agent failures*.
- Cost-vs-blast-radius trade-off: no work varies containment aggressiveness and measures both propagation extent and containment spend.
- Retry/self-correction cost (Reflexion 2303.11366, Self-Refine 2303.17651, CRITIC 2305.11738) is folded into total task cost, never isolated as "recovery spend." Cost-of-Pass (2504.13359) finds self-refinement's marginal gains rarely justify its cost — the closest existing statement that recovery-flavored compute has a measurable, sometimes-negative ROI.
- No LLM-MAS work found using MTTR/checkpoint-overhead/plan-repair-cost framing from classical systems (§2H), despite the mapping being direct.

---

## 4. Does anything here kill or subsume the seed hypothesis?

**No.** Detailed assessment:

- **Not killed:** No paper measures or optimizes recovery/containment cost in organizational LLM MAS. The cost literature (§2A–2D) is about steady-state efficiency; the resilience literature (§2E) is about accuracy retention; the AIOps literature (§2G) is about a different domain and unit of analysis.
- **Closest neighbors the seed MUST cite and differentiate from:**
  1. arXiv 2408.00989 (structure determines blast radius; recovery mechanisms evaluated on effectiveness only) — the seed adds the missing cost axis and organizational boundary types.
  2. AIOpsLab/ITBench (recovery time/token measurement exists in SRE domain) — the seed must not claim "first to measure recovery cost" simpliciter; claim must be scoped to organizational/role-based MAS and to mechanism-comparative containment cost.
  3. Cost-of-Pass (2504.13359) + Efficient Agents (2508.02694) — provide the metric machinery (expected $ per correct outcome) that a "cost-of-recovery" metric should extend; reviewers may ask "isn't this just cost-of-pass applied to faults?" — the answer must foreground *propagation* (blast radius) and *mechanism choice*, which cost-of-pass lacks.
  4. Who&When/AgenTracer (diagnosis cost/accuracy) — adjacent; the seed subsumes diagnosis into end-to-end containment cost.
  5. MetaGPT's "cascading hallucinations" motivation and MAST's "errors propagate undetected" failure mode — evidence the propagation phenomenon is recognized but unquantified economically.
- **Subsumption risk: low.** The occupied delegation-invariants territory (maso/policy_preserving_delegation_research_proposal.md) is orthogonal: it constrains *delegation structure ex ante*; the seed studies *ex post* fault economics. AgentPrune-style topology-cost-robustness work is the only partial overlap, and it lacks faults/recovery.
- **Classical prior art risk: manageable.** Checkpoint-cost theory (Young/Daly), microreboot (cheap recovery → early recovery), ROC (MTTR-first design), plan repair (repair-vs-replan cost), sentinels (dedicated fault-handling agents) all predate LLMs. The seed should import these as framing (they strengthen, not kill, novelty: the *LLM-MAS instantiation* — token costs, stochastic agents, natural-language propagation channels, human-agent boundaries — is unstudied).

---

## 5. Experimental-tractability notes for the orchestrator

- Metric machinery ready to reuse: cost-of-pass (2504.13359), ITBench MTTD/MTTR definitions, AIOpsLab token-cost-per-episode, AgentPrune's $-per-benchmark accounting, AI-Agents-That-Matter Pareto evaluation.
- Fault-injection machinery ready to reuse: AutoTransform/AutoInject (2408.00989), AgenTracer's programmed fault injection, AIOpsLab/ITBench fault injectors, AgentDojo attack suites.
- Organizational settings ready to reuse: ChatDev/MetaGPT role pipelines, TheAgentCompany company simulation.
- The missing piece is precisely the seed: a fault→propagation→containment→recovery-cost accounting framework across organizational boundaries.

---

## 6. Verified-paper master list (identifiers)

All arXiv IDs verified against arxiv.org abstract pages on 2026-09-21: 2305.05176, 2406.18665, 2404.14618, 2310.03094, 2310.03046, 2410.03834, 2408.03314, 2407.21787, 2501.19393, 2412.18547, 2502.18600, 2412.21187, 2502.12067, 2501.12570, 2410.02506, 2310.02170, 2410.11782, 2410.10762, 2502.04180, 2505.14996, 2502.11133, 2402.16823, 2406.07155, 2406.04692, 2402.05120, 2310.00280, 2305.14325, 2308.08155, 2307.07924, 2308.00352, 2407.01502, 2504.13359, 2508.02694, 2407.01489, 2412.14161, 2407.16741, 2502.12115, 2503.17354, 2411.15114, 2503.14499, 2503.13657, 2505.00212, 2509.03312, 2505.08638, 2408.00989, 2502.14143, 2406.13352, 2502.05174, 2503.18813, 2501.06706, 2502.05352, 2310.16340, 2303.11366, 2303.17651, 2305.11738. Non-arXiv verified: GDPval (openai.com/index/gdpval); Young 1974 (10.1145/361147.361115); Daly 2006 (10.1016/j.future.2004.11.016); Candea et al. OSDI 2004 (usenix.org); ROC chapter (10.1002/9781118912744.ch3); Klein & Dellarocas 2000 (10.1023/a:1008759413689); van der Krogt & de Weerdt 2005 (10.1145/1082473.1082761); Hägg 1997 (10.1007/bfb0030090); "Observability for LLMs" book (10.2139/ssrn.5882002).

## 7. Unverified / excluded items (do not cite without re-verification)

- "Agents of Chaos" (multi-agent emergent vulnerabilities) — recalled from memory; could not locate via any working channel (arXiv search/S2/OpenAlex blocked; OpenReview title search negative). Excluded.
- "Why Are Multi-Agent LLM Systems Fragile?" — could not verify existence under this title; likely a misremembering of MAST (2503.13657). Excluded.
- "The Avengers" routing paper — confirmed to exist as ICLR submission via OpenReview, but arXiv ID unverified. Excluded from tables.
- "Remote Labor Index" (Scale AI) — recalled; arXiv ID unverified. Excluded.
- "ChaosEater" (LLM-automated chaos engineering) — seen only in OpenReview review text; claims reduced time/cost vs manual chaos engineering; paper record not verified. Mentioned here only as a signal that LLM-driven chaos engineering exists.
- "OneFlow" (single-agent KV-cache reuse matching MAS cost) — seen only in an OpenReview review snippet; unverified.
- ROC tech report UCB/CSD-02-1175 itself fetched unsuccessfully; verified indirectly via its 2014 book-chapter version (DOI above).
- Search-channel caveat: Semantic Scholar/OpenAlex/DBLP/arXiv-search were rate-limited for most of the session; a follow-up sweep with API keys could surface additional 2025–2026 items, especially very recent arXiv preprints on agent fault injection / chaos engineering.
