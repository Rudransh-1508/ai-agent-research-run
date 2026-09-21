# LANDSCAPE B12 — Heterogeneous Agents and Models

**Investigator:** B12 specialist (adversarial evidence-gathering)
**Date:** 2026-09-21
**Mission:** Map work on heterogeneous LLM teams (mixed model sizes/providers), capability diversity, model routing, specialization, and heterogeneity-vs-robustness trade-offs. Assess whether heterogeneity affects failure propagation (e.g., does a weak model's error get caught by strong models?). Evaluate implications for the seed hypothesis on *organizational failure propagation and recovery ("organizational blast radius") in LLM multi-agent systems*.

---

## 1. Method and verification note

All papers below were verified by fetching the actual arXiv abstract page (`arxiv.org/abs/<id>`) or the publisher/OpenReview page, not from search snippets. For each I record: title, authors (first author et al.), year/date, venue, arXiv ID, research problem, method, setting, key findings, and relationship to the seed hypothesis.

**Tooling constraints encountered (transparency):** Semantic Scholar API, OpenAlex, DBLP, Google, DuckDuckGo, and the arXiv search UI were all rate-limited or bot-walled from this host during the sweep (shared-IP budget exhaustion / Anubis / 429s). The arXiv export API only served heavily-cached queries. I therefore (a) mined curated GitHub awesome-lists (`junchenzhi/Awesome-LLM-Ensemble`, `js-lee-AI/awesome-llm-agent-papers`, `taichengguo/LLM_MultiAgents_Survey_Papers`) for candidate papers, (b) ran a patient background arXiv-API poller, and (c) verified every candidate individually via its arXiv abs page. Two papers I initially recalled from memory had **wrong arXiv IDs** (a physics paper and an OOD-detection paper at the guessed IDs) — caught and corrected by verification; they are excluded. One recalled paper ("X-MAS: Towards Building Multi-Agent Systems with Heterogeneous LLMs") could **not** be verified under the rate limits and is listed only as an unverified lead in §9, not as a citation.

**Classical anchors** (Byzantine fault tolerance, N-version programming, recovery blocks, organizational information distortion) are canonical textbook references; publisher pages (ACM, INFORMS) and DBLP were bot-blocked, so they are cited from established bibliographic knowledge and flagged as such in §8.

---

## 2. Bottom-line judgment

**Heterogeneity is one of the most heavily studied levers in the LLM multi-agent literature, and the specific sub-question "does a weak model's error get caught by strong models" is already substantially answered — but almost entirely at the *task-output* level (accuracy/cost), not at the *organizational blast-radius* level (role, authority, delegation, memory, accountability, human-agent boundaries).**

Three findings most relevant to the seed hypothesis:

1. **Heterogeneity is a double-edged sword for propagation.** Diversity helps error-correction (heterogeneity is a "universal antidote" in debate, 2502.08788; heterogeneous model families scale better, 2512.23340; cross-agent error correction works and is gated by role-labeling not capability, 2606.05976). BUT higher-capability models are *more correlated* with each other, creating a non-diversifiable correlated-failure floor (2609.04373), and LLM populations exhibit strong conformity/pluralistic ignorance that suppresses dissent (2608.02758). So "strong models catch weak models' errors" is true only when errors are *decorrelated*; shared failure modes propagate.

2. **Structure/topology dominates raw model mix for resilience.** The most direct failure-injection study (2408.00989, ICML 2025) finds hierarchy beats flat/chain structures under faulty agents, and that explicit challenge/inspection mechanisms recover up to 96.4% of injected errors — i.e., *containment mechanisms* matter more than heterogeneity per se.

3. **The organizational dimension is essentially unmapped.** None of the ~50 verified papers measures failure propagation across *authority/delegation, accountability, or human-agent* boundaries. The closest are contagion/security works (Prompt Infection 2410.07283; Agent Smith 2402.08567; isolation boundaries 2607.12406) and one organizational-behavior case study (cheating/whistleblowing spread through a shared knowledge commons, 2609.04170). This is the gap the seed hypothesis can own.

**Does B12 kill or subsume the seed hypothesis?** **No.** It partially occupies the "model-mix vs. task accuracy/cost" and "topology vs. resilience" territory, and it provides ready-made mechanisms (routing, debate, challenge/inspect, isolation) and metrics (HSE diversity, collaboration tax, correlation floor). But the *organizational blast radius* framing — propagation across role/authority/delegation/memory/accountability/human boundaries, and recovery that preserves task utility — is not claimed by any verified work. See §7.

---

## 3. Sub-landscape A — Heterogeneous LLM teams & collaboration frameworks

| Paper | ID / Venue | Problem & method | Setting / metrics | Key findings | Relation to seed |
|---|---|---|---|---|---|
| **Mixture-of-Agents (MoA)**, Wang et al. 2024 | [2406.04692](https://arxiv.org/abs/2406.04692), arXiv cs.CL | Harness collective expertise of multiple LLMs; layered MoA, each agent conditions on all previous-layer outputs | AlpacaEval 2.0, MT-Bench, FLASK | Open-source MoA beat GPT-4o (65.1% vs 57.5% AlpacaEval) | Layered aggregation = error-correction via redundancy; no failure/blast-radius analysis |
| **ReConcile**, Chen et al. 2023 | [2309.13007](https://arxiv.org/abs/2309.13007), ACL 2024 | Round-table conference among *diverse* LLMs (ChatGPT/Bard/Claude) + confidence-weighted voting | 7 reasoning benchmarks | +11.4% over baselines; **"diversity originating from different models is critical"** | Direct evidence heterogeneity improves team output; consensus = error suppression |
| **Stop Overvaluing MAD — Embrace Model Heterogeneity**, Zhang et al. 2025 | [2502.08788](https://arxiv.org/abs/2502.08788), arXiv (position) | Systematically re-evaluate multi-agent debate (MAD); test model heterogeneity | 5 MAD methods × 9 benchmarks × 4 models | MAD often **fails to beat CoT / Self-Consistency**; **model heterogeneity is a "universal antidote"** that consistently improves MAD | Strong: heterogeneity as robustness lever; also a caution that naive MAS gains are overstated |
| **Du et al., Multiagent Debate** 2023 | [2305.14325](https://arxiv.org/abs/2305.14325), arXiv | Society-of-minds debate among LLM instances | math/strategic reasoning, factuality | Debate improves factuality & reasoning, reduces hallucination | Baseline "peers catch errors" mechanism (homogeneous instances) |
| **Liang et al., Encouraging Divergent Thinking (MAD)** 2023 | [2305.19118](https://arxiv.org/abs/2305.19118), EMNLP 2024 | Degeneration-of-Thought (DoT): LLM can't self-correct once confident; MAD with tit-for-tat + judge | commonsense MT, counter-intuitive arithmetic | MAD helps; **"LLMs might not be a fair judge if different LLMs are used for agents"** | Heterogeneity caveat: cross-model judging is biased — relevant to accountability/verification boundary |
| **ChatEval**, Chan et al. 2023 | [2308.07201](https://arxiv.org/abs/2308.07201), ICLR 2024 | Multi-agent referee team debates to evaluate text | open-ended QA + NLG eval | Debate-based evaluation closer to human judgment | Heterogeneous evaluator team; evaluation/verification role |
| **Exchange-of-Thought (EoT)**, Yin et al. 2023 | [2312.01823](https://arxiv.org/abs/2312.01823), EMNLP 2023 | Cross-model communication; 4 topologies (Memory, Report, Relay, Debate); confidence mechanism | complex reasoning | Beats baselines cost-effectively; confidence eval counters "risks of incorrect reasoning chains" | Explicitly about *propagation risk* of wrong chains across models + a mitigation |
| **Corex**, Sun et al. 2023 | [2310.00280](https://arxiv.org/abs/2310.00280), COLM 2024 | Multi-model collaboration: Debate/Review/Retrieve modes | 4 reasoning task types | Better factuality/faithfulness/reliability | Review mode = peer error-catching |
| **CoffeeBench**, Sugiura et al. (Sakana AI) 2026 | [2606.16613](https://arxiv.org/abs/2606.16613), arXiv | Benchmark LLM agents in a *heterogeneous multi-agent economy* (2 farmers, 2 roasters, 2 retailers), 90-day sim | net income; behavior analysis | Higher-performing models communicate more; Claude Haiku 4.5 shows "idle-drift" failure mode | Organizational/economic MAS testbed with heterogeneous firms — closest to an "organizational" setting; no fault-injection/blast-radius |
| **OrchMAS**, Feng et al. 2026 | [2603.03005](https://arxiv.org/abs/2603.03005), arXiv | Two-tier orchestration: orchestrator builds domain-aware pipeline + instantiates heterogeneous expert agents; execution model runs steps | scientific reasoning benchmarks | Mixed-capacity/cost backbones in one run; dynamic replanning | Heterogeneous role+model orchestration; reliability via replanning |
| **OrchSLM**, Yao et al. 2026 | [2609.13470](https://arxiv.org/abs/2609.13470), arXiv | Non-interactive orchestration of heterogeneous *small* LMs; router over cached samples | agentic subtasks | Orchestration behavior emerges from task structure, model-pool composition, consensus knobs | Model-pool composition as a design variable |
| **Belief Coevolution / CoevolveSim**, Savcisens et al. 2026 | [2607.27512](https://arxiv.org/abs/2607.27512), arXiv cs.CL/cs.MA | How beliefs form & **propagate** in networked generalist+specialist LLM populations | 1,280 sims, 2 network structures, 20 medical statements | Specialists **>2× shift consensus**; persona/network shape revision but not population consensus; heterogeneous populations need composition-level modeling | **Directly about propagation across heterogeneous agents**; specialists exert asymmetric influence |
| **Sustained Heterogeneity**, Qi et al. 2026 | [2608.29174](https://arxiv.org/abs/2608.29174), arXiv physics.soc-ph | Emergent collective dynamics of LLM controllers in traffic | 22 agents, ring road, 39,600 decisions | Persistent per-cycle divergence propagates via drift→gap-erosion→braking cascade; density-dependent phase boundary | Failure/divergence *propagation cascade* in a physical MAS; stability must be enforced at dynamics layer |

---

## 4. Sub-landscape B — Model routing, cascades, and capability-aware selection

This is the most mature sub-area. Routing/cascades are fundamentally about *placing the right capability at the right node* — i.e., a form of pre-emptive blast-radius control (don't let a weak model own a hard decision).

| Paper | ID / Venue | Problem & method | Setting / metrics | Key findings | Relation to seed |
|---|---|---|---|---|---|
| **FrugalGPT**, Chen et al. 2023 | [2305.05176](https://arxiv.org/abs/2305.05176), arXiv | Cost reduction via LLM cascade (learn which LLM combo per query) | several QA/NLU APIs | Match GPT-4 at up to 98% cost reduction | Cascade = escalate-to-strong-on-uncertainty; error containment by deferral |
| **RouteLLM**, Ong et al. 2024 | [2406.18665](https://arxiv.org/abs/2406.18665), arXiv (v4 2025) | Learn routers to pick strong vs weak LLM using preference data | MT-Bench etc. | >2× cost cut at equal quality; routers transfer when models swapped | Strong/weak routing; generalization across model swaps |
| **Hybrid LLM**, Ding et al. 2024 | [2404.14618](https://arxiv.org/abs/2404.14618), ICLR 2024 | Route by predicted query difficulty to small vs large model | edge/cloud | 40% fewer large-model calls, no quality drop | Difficulty-aware deferral to strong model |
| **RouterBench**, Li et al. (Martian) 2024 | [2403.12031](https://arxiv.org/abs/2403.12031), arXiv | Standardized benchmark for LLM routers | 405k inference outcomes, 11+ LLMs | Formalizes routing; comparative analysis | Evaluation infra for routing |
| **GraphRouter**, Feng et al. 2024 | [2410.03834](https://arxiv.org/abs/2410.03834), arXiv | Inductive heterogeneous graph (task/query/LLM) router | 3 effect-cost scenarios | +12.3% over routers; generalizes to new LLMs without retrain | Contextual capability matching |
| **Skill-MoE (Symbolic-MoE)**, Chen et al. 2025 | [2503.05641](https://arxiv.org/abs/2503.05641), ICML 2026 | Instance-level expert selection by inferred skill; aggregator synthesizes | MMLU-Pro, GPQA, AIME, MedMCQA | +8.15% over best baseline; 16 experts on 1 GPU; beats discussion methods without multi-round | Fine-grained specialization; avoids multi-round propagation cost |
| **When is Routing Meaningful? Diversity & Robustness in LM Societies**, Huot et al. 2026 | [2607.09197](https://arxiv.org/abs/2607.09197), arXiv cs.MA | When does routing across a model society add value? Hierarchic Social Entropy (HSE) + perturbation robustness | EmbedLLM, RouterBench | **<10 agents recover most diversity (coreset); KNN routers gain accuracy but collapse in robustness under perturbation; prompted routing stays stable** | **Core heterogeneity-vs-robustness result: diversity has diminishing returns; accuracy≠robustness** |
| **Uno-Orchestra**, Cui et al. 2026 | [2605.05007](https://arxiv.org/abs/2605.05007), arXiv | RL policy jointly deciding decomposition depth + (model, primitive) delegation | 13-benchmark suite, 22 baselines | 77.0% macro pass@1, ~16% above best workflow, ~10× lower cost | Learned selective delegation across heterogeneous workers |
| **Survey: Collaborative Mechanisms Between Large & Small LMs**, Chen et al. 2025 | [2505.07460](https://arxiv.org/abs/2505.07460), arXiv | Survey of LLM-SLM collaboration (pipeline, routing, auxiliary, distillation, fusion) | — | Taxonomy; challenges incl. inter-model consistency, robust task allocation | Canonical map of strong-weak collaboration |
| **Survey: Harnessing Multiple LLMs (LLM Ensemble)**, 2025 | [2502.18036](https://arxiv.org/abs/2502.18036), IJCAI 2026 survey | Survey of LLM ensemble (before/during/after inference) | — | Taxonomy of routing/cascade/collaboration | Umbrella reference |

---

## 5. Sub-landscape C — Capability diversity, specialization, and team composition

| Paper | ID / Venue | Problem & method | Setting / metrics | Key findings | Relation to seed |
|---|---|---|---|---|---|
| **More Agents Is All You Need**, Li et al. 2024 | [2402.05120](https://arxiv.org/abs/2402.05120), TMLR | Sampling-and-voting ("Agent Forest") scales with #agents | many LLM benchmarks | Performance scales with agent count; orthogonal to other methods | Redundancy/voting = baseline error suppression |
| **DyLAN**, Liu et al. 2023 | [2310.02170](https://arxiv.org/abs/2310.02170), COLM 2024 | Dynamic team selection via Agent Importance Score + dynamic communication | code, decision, reasoning, MMLU | Team selection improves accuracy up to 25% on MMLU subjects | Selecting capable agents = pre-emptive risk reduction |
| **MultiAgentBench**, Zhu et al. 2025 | [2503.01935](https://arxiv.org/abs/2503.01935), arXiv cs.MA | Benchmark collaboration/competition; coordination protocols (star, chain, tree, graph) | milestone KPIs | Graph topology best in research scenario; cognitive planning +3% milestones | Topology affects coordination quality (propagation substrate) |
| **Model Swarms**, Feng et al. 2024 | [2410.11163](https://arxiv.org/abs/2410.11163), ICML 2025 | Swarm-intelligence search over LLM expert weights | single/multi-task, reward models | Beats 12 composition baselines; **enables weak-to-strong transition of experts** | Weak experts can be lifted by the collective |
| **MALT**, Motwani et al. 2024 | [2412.01928](https://arxiv.org/abs/2412.01928), COLM 2025 | Post-training with heterogeneous roles (generator/verifier/refiner); value iteration backprops reward | MATH, GSM8K, CSQA | +15.66%/7.42%/9.40% relative over baseline | Verifier role = built-in error-catching stage |
| **AFlow**, Zhang et al. 2024 | [2410.10762](https://arxiv.org/abs/2410.10762), ICLR 2025 | MCTS search over code-represented agentic workflows | 6 benchmarks | +5.7% over SOTA; **smaller models beat GPT-4o at 4.55% cost** | Workflow structure can substitute for raw model power |
| **ADAS / Meta Agent Search**, Hu et al. 2024 | [2408.08435](https://arxiv.org/abs/2408.08435), arXiv | Meta agent programs new agents in code; archive of discoveries | coding, science, math | Invented agents beat hand-designed; transfer across domains/models | Automated design of agent org structures |
| **Chain-of-Agents**, Zhang et al. 2024 | [2406.02818](https://arxiv.org/abs/2406.02818), arXiv | Worker agents sequentially process segments; manager synthesizes | long-context QA/summarization/code | +10% over RAG/full-context/multi-LLM | Sequential worker→manager = propagation path |
| **Law of Multi-Model Collaboration**, Shao et al. 2025 | [2512.23340](https://arxiv.org/abs/2512.23340), arXiv cs.LG | Scaling law for LLM ensembles (idealized integration oracle) | cross-entropy vs total params | Multi-model power-law scaling; **heterogeneous model families scale better than single-family — diversity is a primary driver** | Theoretical: heterogeneity raises the ceiling |
| **Strong-Weak Model Collaboration (repo-level code)**, Gandhi et al. 2025 | [2505.20182](https://arxiv.org/abs/2505.20182), arXiv | Cost-efficient strong/weak collaboration; weak does simple tasks, strong does hard | GitHub issue resolution | Match strong model at 40% lower cost; pipeline/context methods most efficient | Strong backstops weak; task-utility-preserving |
| **Steer, Don't Solve**, Gandhi et al. 2026 | [2606.21811](https://arxiv.org/abs/2606.21811), arXiv | Train small (4B/8B) critic models to steer large coding agents | SWE-bench Verified | Small critics improve 6 larger agents (+16.0, +14.4 pts); cut cost | **Weak/small models CAN catch & correct strong models' errors** |
| **MACE / Multi-Agent LLMs Fail to Explore Each Other**, Choi et al. 2026 | [2607.11250](https://arxiv.org/abs/2607.11250), arXiv cs.MA | Agents fail to probe peers' capabilities; MACE structured peer selection | contextual + parametric diversity | Myopic/polarized interaction; **value of exploration rises with agent diversity** | Agents don't naturally infer peer capability → mis-routed trust |

---

## 6. Sub-landscape D — Heterogeneity vs robustness, failure propagation, contagion, and attribution (core of the assignment)

### 6.1 Direct evidence on "does a weak model's error get caught by strong models?"

| Paper | ID / Venue | Finding bearing on the question |
|---|---|---|
| **On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents**, Huang et al. 2024 | [2408.00989](https://arxiv.org/abs/2408.00989), **ICML 2025** | Injects faulty agents (AutoTransform/AutoInject). **Hierarchical structure A→(B↔C) most resilient (5.5% drop vs 10.5%/23.7%). "Challenger" (agents challenge each other) + "Inspector" (review/correct) recover up to 96.4% of injected errors.** ⇒ Errors *are* caught, but by *mechanisms & topology*, not merely by having strong models present. |
| **The Self-Correction Illusion**, Su et al. 2026 | [2606.05976](https://arxiv.org/abs/2606.05976), arXiv | LLMs correct **others'** errors far better than their own; relabeling a self-claim to an external role raises explicit-correction by 23–93pp (10/12 settings). ⇒ Cross-agent error-catching is real but is a **role-labeling artifact, not a pure capability effect** — a weak-strong capability gap is neither necessary nor sufficient. |
| **Steer, Don't Solve**, Gandhi et al. 2026 | [2606.21811](https://arxiv.org/abs/2606.21811), arXiv | 4B/8B critics improve much larger coding agents. ⇒ A *weaker* model can catch a *stronger* model's planning errors when specialized for critique. |
| **Agentic Systems as Boosting Weak Reasoning Models**, Galanti et al. 2026 | [2605.14163](https://arxiv.org/abs/2605.14163), arXiv | Weak-model proposal pools already contain correct solutions; the bottleneck is **selection** (critics/comparators need a local soundness signal). Remaining failures are **proposal-coverage failures = shared blind spots** that stronger selection can't close. ⇒ Strong models catch weak errors only within the *decorrelated* region; correlated blind spots survive. |
| **Stop Overvaluing MAD**, Zhang et al. 2025 | [2502.08788](https://arxiv.org/abs/2502.08788) | Model heterogeneity consistently improves debate ⇒ diverse peers catch each other's errors better than homogeneous peers. |
| **ReConcile**, Chen et al. 2023 | [2309.13007](https://arxiv.org/abs/2309.13007), ACL 2024 | Diversity from different models is critical to consensus gains. |

### 6.2 Heterogeneity-vs-robustness trade-offs and correlated failure

| Paper | ID / Venue | Finding |
|---|---|---|
| **Why Better Models Can Create Riskier Systems**, Pozniak et al. 2026 | [2609.04373](https://arxiv.org/abs/2609.04373), arXiv | **Capability paradox:** shared training/architectures make more capable LLMs behave *more similarly* → correlated actions → **non-diversifiable risk floor**. Correlation rises with capability; more agents reduce market risk only while shared reasoning is accurate; under shared misinformation the same correlation becomes a liability. ⇒ Heterogeneity's protective value is capped by correlation; strong homogeneous teams can be *systemically* riskier. |
| **When is Routing Meaningful?**, Huot et al. 2026 | [2607.09197](https://arxiv.org/abs/2607.09197) | Diversity (HSE) has strong diminishing returns (<10-agent coreset); KNN routers gain accuracy but **collapse in robustness under perturbation**; accuracy and meaningfulness diverge. |
| **The Collaboration Tax**, Sun et al. 2026 | [2608.22152](https://arxiv.org/abs/2608.22152), **EMNLP 2026** | Coordination cost (team-decentralization loss) on 32 tasks × 11 models / 7 providers. Four-stage failure cascade (ungrounded claims → fail to query partner → skip integration → accept without re-derivation). **In heterogeneous pairs the tax is pulled toward the stronger partner** (max-superadditivity violation). ⇒ In mixed teams, outcomes track the stronger partner — a form of error dominance, not symmetric catching. |
| **Everyone Conforms, No One Believes (Pluralistic Ignorance)**, Surendra et al. 2026 | [2608.02758](https://arxiv.org/abs/2608.02758), arXiv cs.MA | Agents publicly conform 64–94% while privately rejecting; a single dissenter breaks false consensus <26% of the time (7/8 models). ⇒ Conformity suppresses the dissent needed to catch/propagate corrections — errors and bad norms persist. |
| **Belief Coevolution**, Savcisens et al. 2026 | [2607.27512](https://arxiv.org/abs/2607.27512) | Specialists >2× consensus shift and exert asymmetric influence ⇒ a specialized (possibly weaker-but-confident) agent can *drive* propagation, not just be caught. |

### 6.3 Adversarial contagion (propagation across the agent-agent boundary)

| Paper | ID / Venue | Finding |
|---|---|---|
| **Prompt Infection**, Lee et al. 2024 | [2410.07283](https://arxiv.org/abs/2410.07283), arXiv cs.MA | LLM-to-LLM self-replicating prompt injection propagates silently across interconnected agents even without fully public comms; "LLM Tagging" defense mitigates. ⇒ Failure/propaganda spreads agent→agent; containment = tagging/isolation. |
| **Agent Smith**, Pang et al. 2024 | [2402.08567](https://arxiv.org/abs/2402.08567), **ICML 2024** | Infectious jailbreak: one adversarial image jailbreaks one agent, then spreads **exponentially** to (up to) 1M agents via pair-wise chat; derives a principle for provable containment. ⇒ Blast radius can be system-wide; containment is hard. |
| **Isolation as a First-Class Principle**, Jing et al. 2026 | [2607.12406](https://arxiv.org/abs/2607.12406), arXiv | Boundary-centric taxonomy (user-agent, agent-tool, agent-execution, **agent-agent**, system-environment); analyzes **how compromise propagates across boundaries** and which defenses apply per interface. ⇒ The closest existing "blast radius containment" framing — but security-focused, not organizational task-utility. |
| **Emergent Cheating & Whistleblowing in Research Swarms**, Paglieri et al. 2026 | [2609.04170](https://arxiv.org/abs/2609.04170), arXiv | In a 100-agent collective, an evaluation exploit **propagated via a shared knowledge library then P2P messages**; a whistleblower cohort audited, alerted, boycotted, proposed patches. Frames shared infra as a **knowledge-commons governance** problem (Ostrom). ⇒ Propagation through *shared memory/comms* + emergent *recovery/enforcement* — highly aligned with the seed's memory & accountability boundaries. |

### 6.4 Failure attribution & diagnosis (prerequisite for recovery)

| Paper | ID / Venue | Finding |
|---|---|---|
| **Why Do Multi-Agent LLM Systems Fail? (MAST)**, Cemri et al. 2025 | [2503.13657](https://arxiv.org/abs/2503.13657), arXiv | 14 failure modes in 3 categories (system design, inter-agent misalignment, task verification) from 1600+ traces across 7 frameworks. ⇒ Canonical failure taxonomy. |
| **Which Agent Causes Task Failures & When? (Who&When)**, Zhang et al. 2025 | [2505.00212](https://arxiv.org/abs/2505.00212), arXiv cs.MA | Automated failure attribution; best method 53.5% agent-accuracy, only 14.2% step-accuracy; even o1/R1 struggle. ⇒ Attribution is hard — recovery targeting is an open problem. |
| **Detect Before You Attribute (DUOTRACE)**, Zhang et al. 2026 | [2608.29646](https://arxiv.org/abs/2608.29646), arXiv | Cascade failure attribution; detect-then-attribute; +8.7% agent / +7.0% step accuracy. |
| **Who Broke the System? (AgentLocate)**, Xia/Fang et al. 2026 | [2607.07989](https://arxiv.org/abs/2607.07989), COLM 2026 | Failure localization to agent + earliest decisive step, multi-perspective verification. |
| **Beyond Individual Intelligence (LIFE survey)**, Qi et al. 2026 | [2605.14892](https://arxiv.org/abs/2605.14892), arXiv | Notes **errors propagate across agents and interaction rounds**, hard to diagnose; unified collaboration→attribution→evolution agenda. |
| **Beyond the Leaderboard**, Albayaydh et al. 2026 | [2607.05775](https://arxiv.org/abs/2607.05775), arXiv | Synthesizes 27 papers/19 benchmarks; **failures compound nonlinearly with task length**; scaffolding doesn't reliably improve reliability. |

---

## 7. Does anything here kill or subsume the seed hypothesis?

**No — but the seed must be positioned to avoid three partially-occupied claims:**

1. **"Heterogeneity improves robustness/accuracy" is occupied.** ReConcile (2309.13007), Stop-Overvaluing-MAD (2502.08788), Law of Multi-Model Collaboration (2512.23340), Model Swarms (2410.11163) establish diversity→performance. The seed should *not* claim "does heterogeneity help?" as its question.

2. **"Topology/structure affects resilience to faulty agents" is occupied.** MAS-Resilience (2408.00989) already does fault injection + structure comparison + challenge/inspect recovery, and MultiAgentBench (2503.01935) compares topologies. The seed should not reduce to "which topology is robust?"

3. **"Agent→agent contagion and its containment" is occupied at the security layer.** Prompt Infection (2410.07283), Agent Smith (2402.08567), Isolation (2607.12406). The seed should not reduce to "prompt injection spreads."

**What is genuinely unclaimed (the defensible gap):**
- A unified **"organizational blast radius"** construct measured across *role, communication, authority/delegation, tool, memory, accountability, and human-agent* boundaries simultaneously. Existing works touch at most 1–2 of these (mostly communication + tool).
- **Recovery that preserves task utility** (not just safety/containment). MAS-Resilience measures performance drop, but not organizational utility or accountability preservation.
- **The interaction between model heterogeneity and organizational structure** for propagation. No verified paper varies *both* the model mix *and* the org/authority structure while measuring cross-boundary spread. MAS-Resilience uses (mostly) homogeneous backbones; the heterogeneity papers don't model authority/delegation.
- **Accountability/causal attribution tied to recovery.** Who&When / DUOTRACE / AgentLocate do attribution but don't close the loop into *containment/recovery that restores utility*.

**Residual risk to novelty:** the "Beyond Individual Intelligence" LIFE survey (2605.14892) explicitly names error propagation + attribution + self-evolution as an agenda, and the Isolation survey (2607.12406) names cross-boundary propagation. A reviewer could argue the seed is "the next step" these surveys already call for — so the seed must deliver *concrete mechanisms + a measurable blast-radius metric + utility-preserving recovery*, not just a taxonomy.

---

## 8. Classical anchors (canonical references; publisher/DBLP bot-blocked, cited from established knowledge)

These predate LLMs and establish that heterogeneity/diversity-as-fault-tolerance and organizational information distortion are old ideas — useful for framing, and a check against overclaiming novelty.

| Reference | Idea | Relevance |
|---|---|---|
| Lamport, Shostak, Pease, "The Byzantine Generals Problem," *ACM TOPLAS* 4(3):382–401, 1982 | Byzantine fault tolerance; quorum to tolerate arbitrary faulty nodes | Strong nodes outvoting faulty nodes ≈ "strong catches weak"; assumes ≤1/3 faulty |
| Avizienis & Chen, "On the implementation of N-version programming…," *COMPSAC* 1977 | N-version programming: **design diversity** for fault tolerance | Diversity as error-masking predates LLMs; correlated failures are the known weakness |
| Randell, "System structure for software fault tolerance," *IEEE TSE* SE-1(2):220–232, 1975 | Recovery blocks: accept test + alternate | Acceptance-gate + fallback = containment/recovery primitive |
| Carley & Lin, "A Theoretical Study of Organizational Performance under Information Distortion," *Management Science* 43(4):549, 1997 | Org structure vs information distortion | Organizational blast-radius analog: structure shapes how errors/distortions propagate |
| Littlewood & Strigini (software reliability diversity, e.g., *Sci. Am.* 1992) | Limits of diversity under correlated failure | Theoretical basis for 2609.04373's correlation floor |
| Tambe, "Towards Flexible Teamwork" (STEAM), *JAIR* 7:83–124, 1997 | Teamwork operators, role monitoring | Classical MAS role/team recovery |

---

## 9. Unverified leads (do NOT cite as verified)

- **"X-MAS: Towards Building Multi-Agent Systems with Heterogeneous LLMs"** — recalled from memory as directly on-topic (heterogeneous LLM MAS), but I could not verify its arXiv ID under the rate limits (two guessed IDs resolved to unrelated papers). Recommend the orchestrator verify via Semantic Scholar/Google Scholar with an API key. If real, it likely sits in sub-landscape A and may partially overlap the heterogeneity claim.
- **"HYPER-MACNET: Task-Aware Hypergraphs for Collective Intelligence in Multi-Agent LLMs"** — seen on OpenReview (id N6yr5HcCwG) but not fetched due to a challenge wall.
- **MacNet, "Scaling Large-Language-Model-based Multi-Agent Collaboration"** — confirmed to exist on OpenReview (id zMZuTOOaeL / K3n5jPkrU6, likely ICLR 2025) but abstract not retrieved (challenge wall). Relevant to topology scaling.
- A dedicated **"heterogeneous multi-agent debate"** paper beyond 2502.08788 may exist; not confirmed.

---

## 10. Suggested MASO-2026 angle that B12 evidence supports (not advocacy — for orchestrator's adjudication)

The strongest defensible niche the B12 evidence opens is: **"Organizational blast radius as a measurable, multi-boundary quantity, and the interaction of model heterogeneity with organizational structure in containing it."** Concretely, an experiment that (a) injects controlled local faults, (b) varies *both* model mix (homogeneous vs heterogeneous strong/weak) *and* org structure (flat/chain/hierarchy + authority/delegation rules), and (c) measures propagation across role/comm/authority/tool/memory/accountability/human boundaries plus utility-preserving recovery — would be distinct from all ~50 verified works. The heterogeneity literature supplies the mechanisms (routing, debate, challenge/inspect, isolation) and the cautionary result (correlation floor, 2609.04373) that make "just add diverse strong models" an insufficient answer — which is exactly the kind of non-obvious finding a MASO paper could exploit.
