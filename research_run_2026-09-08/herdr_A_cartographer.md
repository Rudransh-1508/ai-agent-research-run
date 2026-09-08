# Agent A — MAS literature cartography

**Cut-off:** 8 September 2026 (Asia/Calcutta)  
**Role:** independent literature cartographer  
**Scope:** multi-agent systems (MAS) broadly construed: game-theoretic/formal MAS, MARL, communication and coordination, LLM-agent teams, multi-robot systems, human–AI cooperation, robustness, trust, and multi-agent path finding (MAPF).

## Bottom line

The 2023–2026 literature is not one coherent MAS field. It is at least four partially disconnected programs:

1. **Classical MAS and game theory** prove equilibrium, regret, verification, contract, allocation, and trust results under explicit assumptions.
2. **MARL** optimizes cooperative policies, usually in Dec-POMDP-style simulators, but remains benchmark-fragile and strongly shaped by CTDE, parameter sharing, shared rewards, and privileged training information.
3. **LLM multi-agent systems** increasingly learn or search roles, prompts, communication graphs, routers, and workflows; most evidence is still short-horizon math/code/QA with API models and token cost as the main systems metric.
4. **Robotics/MAPF** supplies the sharpest physical constraints—collision, timing, partial observability, motion feasibility—but many “robot” evaluations remain simulation-heavy or place a centralized planner beneath language-level decentralization.

The most defensible cross-program conclusion is conditional: **coordination structure matters more than agent count**. More agents can help when they add independent information or complementary competence and when a protocol preserves it. They can hurt through conformity, integration loss, propagation of false information, communication cost, or a weak coordinator.

## Method and audit boundary

- I searched live primary venue archives, publisher pages, OpenReview records, proceedings PDFs, and author-hosted full papers. Surveys were used for orientation but are not counted in the 52-paper evidence ledger.
- I did not read or use any other agent's output. A directory listing was used only to confirm the requested destination filename did not already exist; no other report was opened.
- **R** below means section-level inspection of the primary full text (method, experiment/results, and limitations or boundary conditions). **C** means a concentrated primary-record read: exact venue/title and method/experiment details were verified, but the publisher interface did not expose every full-text section in the same way. Claims from C papers are correspondingly conservative.
- “Limitation” includes an explicit author limitation and, where labelled **inference**, a boundary that follows directly from the stated model or experiment. I do not turn a simulation, benchmark, or proof under assumptions into a deployment claim.
- The ledger contains **52 unique papers**. Duplicate arXiv/conference versions are one paper.

## Venue and year coverage

| Venue | 2023 | 2024 | 2025 | 2026 status at cut-off | Evidence used |
|---|---:|---:|---:|---|---|
| AAMAS | yes | yes | yes | proceedings live | 6 papers; official IFAAMAS proceedings |
| NeurIPS | yes | yes | yes | conference/proceedings not yet occurred | 7 papers |
| ICML | yes | yes | yes | official 2026 program available | 7 papers |
| ICLR | yes | yes | yes | accepted 2026 records available | 7 papers |
| AAAI | yes | yes | yes | OJS proceedings live | 5 papers |
| IJCAI | yes | yes | yes | 2026 conference occurred, but a stable public proceedings archive was not discoverable in this run | 4 papers; no unverified 2026 acceptance claims |
| ACL-family | yes | yes | yes | ACL 2026 Anthology live | 5 papers |
| JAIR | yes | yes | yes | no 2026 paper admitted to this purposive sample | 3 papers |
| Artificial Intelligence (AIJ) | yes | yes | yes | online/September 2026 article available | 3 papers |
| Autonomous Agents and Multi-Agent Systems (JAAMAS) | yes | yes | yes | 2026 articles live | 3 papers |
| Robotics (ICRA/IROS) | — | yes | — | used as a bridge rather than exhaustive venue census | 2 papers |

Primary venue indexes: [AAMAS 2023](https://www.ifaamas.org/Proceedings/aamas2023/forms/contents.htm), [AAMAS 2024](https://www.ifaamas.org/Proceedings/aamas2024/forms/contents.htm), [AAMAS 2025](https://www.ifaamas.org/Proceedings/aamas2025/forms/contents.htm), [AAMAS 2026](https://www.ifaamas.org/Proceedings/aamas2026/forms/contents.htm), [NeurIPS proceedings](https://proceedings.neurips.cc/), [ICML/PMLR](https://proceedings.mlr.press/), [ICLR/OpenReview](https://openreview.net/group?id=ICLR.cc), [AAAI proceedings](https://ojs.aaai.org/index.php/AAAI), [IJCAI proceedings](https://www.ijcai.org/proceedings/), [ACL Anthology](https://aclanthology.org/), [JAIR](https://www.jair.org/), [JAAMAS](https://link.springer.com/journal/10458), and [AIJ](https://www.sciencedirect.com/journal/artificial-intelligence).

## Evidence ledger — 52 unique papers

### AAMAS

**A01 — R. “Trust Region Bounds for Decentralized PPO Under Non-stationarity.” 2023, AAMAS.** [Primary PDF](https://www.ifaamas.org/Proceedings/aamas2023/pdfs/p5.pdf)  
Assumes cooperative decentralized policies and bounds changing co-agent policies as non-stationarity. Derives trust-region-style decentralized PPO guarantees and evaluates policy performance/stability on cooperative MARL tasks. The useful correction is that single-agent PPO intuition does not transfer unchanged when every learner changes the transition/reward landscape. Limit: the bound depends on controlled policy divergence and does not remove partial-observability or equilibrium-selection problems.

**A02 — C. “TiZero: Mastering Multi-Agent Football with Curriculum Learning and Self-Play.” 2023, AAMAS.** [Primary PDF](https://www.ifaamas.org/Proceedings/aamas2023/pdfs/p67.pdf)  
Uses self-play plus curriculum stages for Google Research Football; reports win-rate/Elo-style progress and football-specific performance. It shows curriculum can make a difficult competitive benchmark tractable, not that the learned conventions transfer to open-world teams. The fixed simulator, reward, roster, and self-play population are material assumptions.

**A03 — R. “JaxMARL: Multi-Agent RL Environments and Algorithms in JAX.” 2024, AAMAS.** [Primary PDF](https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p2444.pdf)  
Vectorizes common MARL environments and baselines in JAX. Benchmarks throughput and learning curves across environments/algorithms, making compute-normalized replication much easier. Its contribution is infrastructure, not a new coordination principle; accelerated simulation can also accelerate overfitting to the same narrow benchmark family.

**A04 — C. “MESA: Cooperative Meta-Exploration in Multi-Agent Learning through Exploiting State-Action Space Structure.” 2024, AAMAS.** [Primary PDF](https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p2085.pdf)  
Exploits state–action structure to transfer exploratory behavior across cooperative tasks. Evaluations use return/success and sample efficiency on MARL benchmarks. Assumes reusable structure across source and target tasks; negative transfer and representation mismatch remain the practical boundary.

**A05 — R. “An Extended Benchmarking of Multi-Agent Reinforcement Learning Algorithms in Complex Fully Cooperative Tasks.” 2025, AAMAS.** [Primary PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1613.pdf)  
Compares 11 established methods (including QMIX, MAPPO, QPLEX, HAPPO, MAT-DEC and exploration variants) over fully cooperative PettingZoo, Overcooked, PressurePlate, MPE, LBF, RWARE, Capture Target, and Box Pushing tasks, including RGB observations and training time. Many SMAC/GRF leaders underperform standard baselines; some sparse cooperative tasks remain unsolved. This directly contradicts leaderboard-to-generality inference. Limits: no explicit execution-time communication, a selected rather than exhaustive hyperparameter budget, and simulated tasks only.

**A06 — R. “HyperAgent: Leveraging Hypergraphs for Topology Optimization in Multi-Agent Communication.” 2026, AAMAS.** [Primary PDF](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/QTVF9552.pdf)  
Represents group collaboration with hyperedges; a variational hypergraph autoencoder plus policy gradient and sparsity regularization generates task-conditioned topologies. Five GPT-based agents are tested on MMLU, GSM8K, MultiArith, SVAMP, AQuA, and HumanEval. The paper reports 91.77% mean, 96.57% GSM8K, 92.40% HumanEval pass@1, and up to 25.33% token reduction; removing hypergraphs drops the mean 2.44 points. Important caveats: gpt-4-1106-preview/gpt-3.5-turbo-0125 are dated API snapshots; single-agent temperature is 0 while multi-agent temperature is 1; all tasks have cheap automatic final-answer scoring; five agents and three rounds do not establish population-scale behavior.

### NeurIPS

**N01 — C. “Decompose a Task into Generalizable Subtasks in Multi-Agent Reinforcement Learning.” 2023, NeurIPS.** [Primary page](https://proceedings.neurips.cc/paper_files/paper/2023/hash/f7d3cef7ff579f2f903c8f458e730cae-Abstract-Conference.html)  
DT2GS learns scalable subtask encodings and an adaptive semantic module, then tests zero-shot/task transfer in cooperative environments. The key assumption is that tasks share compositional latent substructure. Metrics are episodic return/success and transfer generalization. Boundary: learned decomposition is benchmark-semantic, not a guaranteed causal task factorization.

**N02 — C. “Multi-Agent Meta-Reinforcement Learning: Sharper Convergence Rates with Task Similarity.” 2023, NeurIPS.** [Primary page](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d1b1a091088904cbc7f7faa2b45c8f36-Abstract-Conference.html)  
Provides task-similarity-dependent convergence results for zero-sum Markov games, potential games, and general-sum coarse correlated equilibrium, supported by numerical simulations. Its value is a formal account of when meta-learning should help. Limit: the similarity measure and game classes are known mathematical objects; numerical validation is far from high-dimensional partially observed teams.

**N03 — R. “Multi-Agent Coordination via Multi-Level Communication.” 2024, NeurIPS.** [Primary page/PDF](https://proceedings.neurips.cc/paper_files/paper/2024/hash/d6be51e667e0b263e89a23294b57f8cf-Abstract-Conference.html)  
SeqComm orders decisions asynchronously and communicates hidden states, intentions, and actions before simultaneous environment execution. Under bounded world-model error and bounded policy divergences it proves monotonic improvement; experiments cover cooperative combat and predator–prey-style tasks using win/return and communication comparisons. Boundary: sequential deliberation adds latency and depends on a useful learned model; random ordering can converge to poor local optima.

**N04 — R. “MDAgents: An Adaptive Collaboration of LLMs for Medical Decision-Making.” 2024, NeurIPS.** [Primary page](https://proceedings.neurips.cc/paper_files/paper/2024/hash/90d1fc07f46e31387978b88e7e057a31-Abstract-Conference.html)  
Routes a query to solo or group collaboration based on estimated complexity, with moderator and external medical knowledge variants. Across 10 medical knowledge/multimodal benchmarks it is best on 7, reports up to +4.2 percentage points (p<.05), and moderator plus external knowledge averages +11.8%. These are benchmark answers, not patient outcomes; complexity routing, model knowledge, and LLM-generated deliberation can share correlated errors.

**N05 — C. “Autonomous Agents for Collaborative Task under Information Asymmetry.” 2024, NeurIPS.** [Primary page](https://proceedings.neurips.cc/paper_files/paper/2024/hash/0534abc9e6db91683d82186ef0d68202-Abstract-Conference.html)  
iAgents combine information navigation and mixed memory for tasks split across private communication histories. InformativeBench is built from a real communication network (140 people, 588 edges, about 70k messages) and evaluates task success under time/turn constraints. It tests information asymmetry more realistically than identical-agent debate, but privacy, permission, and distribution-shift questions remain; a curated historical graph is not a live organization.

**N06 — R. “Why Do Multi-Agent LLM Systems Fail?” 2025, NeurIPS Datasets and Benchmarks Track.** [Primary page/PDF](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html)  
MAST derives 14 failure modes in three groups from 1,642 traces across seven MAS frameworks. Expert inter-annotator κ is .88; an o1-based judge reports .94 accuracy, .77 κ, and .80 F1; targeted interventions improve performance by as much as 15.6% with the same base model. Limit: taxonomy completeness is not guaranteed, traces are dominated by coding/math/general reasoning, and automated diagnosis still misses or confuses failures.

**N07 — R. “Multi-Agent Collaboration via Evolving Orchestration.” 2025, NeurIPS.** [Primary page/PDF](https://proceedings.neurips.cc/paper_files/paper/2025/hash/f1320d2e2842169c6fc89dcbd80e94d0-Abstract-Conference.html)  
A central RL “Puppeteer” evolves compact cyclic agent workflows. It improves task scores while searching coordination structures, but training uses 8×A800 GPUs, roughly 28.8–78.4 GB per GPU for 2–6 hours. Authors note coarse final-output/token rewards, fixed agents/tools, and occasional miscoordination or deceptive agreement. Cost comparisons with non-RL search are not fully like-for-like.

### ICML

**M01 — C. “Cooperative Multi-Agent Reinforcement Learning: Asynchronous Communication and Linear Function Approximation.” 2023, ICML.** [Primary page](https://proceedings.mlr.press/v202/min23a.html)  
Studies episodic cooperative learning with a central server, asynchronous agents, and linear function approximation. It proves regret about \(\tilde O(d^{3/2}H^2\sqrt K)\), communication about \(\tilde O(dHM^2)\), and an \(\Omega(dM)\) lower bound. This is communication-efficient distributed learning under a precise model, not decentralized execution in an unknown Dec-POMDP.

**M02 — C. “RACE: Improve Multi-Agent Reinforcement Learning with Representation Asymmetry and Collaborative Evolution.” 2023, ICML.** [Primary page](https://proceedings.mlr.press/v202/li23i.html)  
Combines evolutionary team search with a shared nonlinear encoder, distinct linear policy representations, value-aware mutual information, crossover, and mutation. Evaluations span discrete and continuous cooperative tasks using return and learning efficiency. Boundary: evolutionary compute and population design are substantial hidden resources; learned representational asymmetry does not imply interpretable roles.

**M03 — R. “Adaptive Coordination in Social Embodied Rearrangement.” 2023, ICML.** [Primary OpenReview record](https://openreview.net/forum?id=BYEsw113sz)  
Introduces Social Rearrangement for embodied zero-shot coordination and a Behavioral Diversity Play objective that makes partner policies discriminable. In simulated two-robot rearrangement with unseen partners/environments it reports 35% higher success and 32% higher efficiency than baselines. Limit: simulated partners and homes, two-agent scale, and task success do not establish safe human–robot collaboration.

**M04 — C. “Detecting Influence Structures in Multi-Agent Reinforcement Learning.” 2024, ICML.** [Primary page](https://proceedings.mlr.press/v235/pieroth24a.html)  
Agents infer which other agents influence their rewards/transitions while observing others’ actions; the paper gives average-reward convergence results and experiments on structured influence networks. The assumption that relevant actions are observable is strong. Detection identifies statistical influence under the modeled process, not necessarily causal responsibility under hidden confounding.

**M05 — R. “Multi-agent Architecture Search via Agentic Supernet.” 2025, ICML.** [Primary page](https://proceedings.mlr.press/v267/zhang25bi.html)  
MaAS learns a query-conditioned distribution over agent systems using an agentic supernet, then transfers architectures across data and model backbones. Across six benchmarks it reports +0.54 to +11.82 points while using 6–45% of baseline inference cost. Limits: the supernet bounds the search space, evaluation is final-answer-centric, and transfer across benchmarks is not open-ended adaptation.

**M06 — C. “AutoML-Agent: A Multi-Agent LLM Framework for Full-Pipeline AutoML.” 2025, ICML.** [Primary page](https://proceedings.mlr.press/v267/trirat25a.html)  
Uses retrieval-grounded planning, parallel specialist agents, and multi-stage verification over seven tasks and 14 datasets. Metrics include predictive performance and pipeline/task success. “Full pipeline” is within supported tabular/ML tooling; reproducibility, data leakage, compute budgets, and production governance remain outside the benchmark claim.

**M07 — R. “Multi-Agent Teams Hold Experts Back.” 2026, ICML.** [Primary preprint linked to accepted work](https://arxiv.org/abs/2602.01011)  
Tests self-organizing LLM teams when one member is an expert and even when expertise is revealed. Teams fail to match the expert, with losses up to 37.6%; larger teams increasingly produce integrative compromise. Consensus can improve adversarial robustness, creating a real accuracy–robustness trade-off. Limit: LLM-mediated reasoning tasks and chosen team protocols; the result is not a universal theorem about human or robotic teams.

### ICLR

**I01 — C. “Can We Find Nash Equilibria at a Linear Rate in Markov Games?” 2023, ICLR.** [Primary record](https://openreview.net/forum?id=eQzLwwGyQrb)  
Homotopy policy optimization alternates locally fast and globally slow updates for two-player zero-sum discounted Markov games, obtaining global linear convergence without observing the opponent policy. The guarantee depends on the zero-sum discounted tabular structure and exact update conditions; it does not solve general-sum equilibrium multiplicity.

**I02 — C. “Collaborative Pure Exploration in Kernel Bandit.” 2023, ICLR.** [Primary record](https://openreview.net/forum?id=hLbeJ6jObDD)  
CoKernelFC/FB exploit shared kernel structure across related agents and prove near-matching sample/communication bounds. Synthetic/kernel experiments measure identification error, samples, and communication. Gains require task similarity captured by the effective dimension; unrelated agents erase the premise.

**I03 — R. “MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework.” 2024, ICLR.** [Primary record](https://openreview.net/forum?id=VtmBAGCN7o)  
Encodes software-company roles and standard operating procedures, passing structured artifacts between product manager, architect, engineer, and QA-like agents. Evaluations use code-generation/software-engineering quality, executability, and cost. Static roles/workflows, LLM-judged quality, and small generated projects limit the “software company” analogy.

**I04 — R. “Learning Multi-Agent Communication from Graph Modeling Perspective.” 2024, ICLR.** [Primary record](https://openreview.net/forum?id=Qox9rO0kN0)  
CommFormer learns a sparse communication graph through continuous relaxation, bi-level optimization, and attention. Cooperative benchmark returns and communication edges/cost test task and agent-count generalization. It assumes cooperative differentiable training and a stable graph-learning distribution; it does not address strategic message deception.

**I05 — R. “Large Language Models Cannot Self-Correct Reasoning Yet.” 2024, ICLR.** [Primary record](https://openreview.net/forum?id=IkmD3fKBPQ)  
Controls response budgets across intrinsic self-correction, multi-agent debate, and self-consistency. Without external feedback, revision often hurts and debate does not beat equal-budget self-consistency. Oracle feedback changes the problem. Boundary: model/prompt generations available at the time (notably ChatGPT/GPT-4) and reasoning benchmarks; future trained verifiers may change the result.

**I06 — R. “Hypothetical Minds: Scaffolding Theory of Mind for Multi-Agent Tasks with Large Language Models.” 2025, ICLR.** [Primary PDF](https://openreview.net/pdf?id=MSDFeMXkI7)  
Maintains scored hypotheses about other agents, uses counterfactual prediction, and turns the top hypotheses into plans/subgoals. In Melting Pot-style Running With Scissors, Collaborative Cooking, Prisoner’s Dilemma, and an eight-player arena, it often beats ReAct/Reflexion/PlanReAct and RL baselines; e.g., in repeated RWS it leads all nine listed scenarios, while in Prisoner’s Dilemma it leads only 5/10. Low-level embodied control remains worse than RL in dense-reward settings; GPT-4, handcrafted scaffolding, and scenario-specific text interfaces are central dependencies.

**I07 — R. “SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning.” 2026, ICLR.** [Primary record/PDF](https://openreview.net/forum?id=7Yayy5fNLg)  
Trains language models online through self-play in Tic-Tac-Toe, Kuhn Poker, and simple negotiation; role-conditioned advantage estimation stabilizes the two-sided learning process. Across four Qwen/Llama-family models and eight reasoning benchmarks, transfer gains reach about 10%, beating supervised training on 25,000 expert game trajectories. Limitation: small text games, zero-sum or stylized bargaining, expensive autoregressive self-play, and post-hoc reasoning-pattern interpretation rather than a causal mechanism.

### AAAI

**AA01 — C. “Learning to Play General-Sum Games against Multiple Boundedly Rational Agents.” 2023, AAAI.** [Primary page](https://ojs.aaai.org/index.php/AAAI/article/view/26391)  
Optimizes a principal’s policy against multiple no-regret but boundedly rational learners in smooth games. Matrix and spatiotemporal economy experiments include dynamic taxation, reporting about 15% welfare improvement over unseen bounded-rational taxpayers. The response model and learning class define the result; real people are not guaranteed to follow those dynamics.

**AA02 — C. “Robust Multi-Agent Coordination via Evolutionary Generation of Auxiliary Adversarial Attackers.” 2023, AAAI.** [Primary page](https://ojs.aaai.org/index.php/AAAI/article/view/26388)  
ROMANCE evolves a diverse population of sparse action attackers for robust training in cooperative Dec-POMDPs. SMAC perturbation tests report win/return robustness. The threat model is action perturbation inside a simulator; observation poisoning, communication compromise, and adaptive human adversaries are separate problems.

**AA03 — R. “T2MAC: Targeted and Trusted Multi-Agent Communication through Selective Engagement and Evidence-Driven Integration.” 2024, AAAI.** [Primary page](https://ojs.aaai.org/index.php/AAAI/article/view/29438)  
Learns when, to whom, and what to communicate, then fuses messages using evidence estimates. Hallway, MPE, and SMAC experiments measure return/win rate, communication, and generalization. Trust is operationalized as learned evidence inside cooperative training, not institutional or adversarial trust.

**AA04 — R. “AgentMixer: Multi-Agent Correlated Policy Factorization.” 2025, AAAI.** [Primary page](https://ojs.aaai.org/index.php/AAAI/article/view/34048)  
Nonlinearly mixes decentralized partial policies into a correlated joint policy while enforcing mode consistency; it connects the solution to an ε-approximate correlated equilibrium. Tests include matrix games, Predator–Prey, SMAC-v2, and Multi-Agent MuJoCo using return/win metrics. Approximate-equilibrium interpretation depends on learned factorization and benchmark stationarity.

**AA05 — R. “BAMAS: Structuring Budget-Aware Multi-Agent Systems.” 2026, AAAI.** [Primary page](https://ojs.aaai.org/index.php/AAAI/article/view/40226)  
Uses integer programming to choose models under a cost/performance budget, then reinforcement learning to select topology. Across three tasks it reports comparable performance with up to 86% cost reduction. Price/token assumptions are provider- and date-sensitive; three tasks and a predefined model/role pool do not establish general architecture selection.

### IJCAI

**J01 — C. “GPLight: Grouped Multi-agent Reinforcement Learning for Large-scale Traffic Signal Control.” 2023, IJCAI.** [Primary page](https://www.ijcai.org/proceedings/2023/23)  
Dynamically groups intersections using road topology and real-time flows, with information-theoretic grouping objectives. Synthetic and real traffic data scale to 1,089 intersections; metrics include travel time, delay, and throughput. Simulation fidelity, sensor availability, and policy transfer to live traffic control remain the deployment gap.

**J02 — C. “Multi-Agent Systems with Quantitative Satisficing Goals.” 2023, IJCAI.** [Primary page](https://www.ijcai.org/proceedings/2023/32)  
Models agents with quantitative threshold goals and studies pure-strategy Nash equilibrium through automata/optimization machinery, including approximate multi-threshold objectives. The formalism exposes that “good enough” differs from maximizing utility. Complexity and one-way approximation correspondences limit direct scaling to learned continuous policies.

**J03 — R. “Synthesis of Communication Policies for Multi-Agent Systems Robust to Communication Restrictions.” 2025, IJCAI.** [Primary page](https://www.ijcai.org/proceedings/2025/30)  
Synthesizes joint action and communication policies for reach–avoid objectives that remain correct when only a bounded number of agents can communicate, and optimizes information use beyond a budget. Benchmarks measure satisfaction and communication cost. Assumes a known finite transition model and specified restriction class; robustness is not to false messages or unknown dynamics.

**J04 — C. “Improving Consistency Identification in Task-oriented Dialogue Through Multi-Agent Collaboration.” 2025, IJCAI.** [Primary page](https://www.ijcai.org/proceedings/2025/918)  
Uses question-, history-, and knowledge-based specialist agents in full, cyclic, or centralized topologies for zero-shot consistency identification. Standard dialogue benchmarks report classification metrics and surpass supervised methods on most metrics. The system identifies consistency in static transcripts; it does not test live bargaining, strategic users, or compounding multi-turn intervention.

### ACL and related NLP venues

**L01 — R. “Theory of Mind for Multi-Agent Collaboration via Large Language Models.” 2023, EMNLP.** [Primary page/PDF](https://aclanthology.org/2023.emnlp-main.13/)  
Tests LLM agents in a cooperative text game against MARL/planning approaches and adds explicit belief-state reasoning. Metrics are task return/success and behavior by belief order. LLMs exhibit useful higher-order reasoning, but long horizons and context produce hallucination and inconsistent belief tracking; text games are not evidence of human-grade theory of mind.

**L02 — R. “LLMArena: Assessing Capabilities of Large Language Models in Dynamic Multi-Agent Environments.” 2024, ACL.** [Primary page/PDF](https://aclanthology.org/2024.acl-long.705/)  
Evaluates LLMs in seven interactive games and ranks performance with TrueSkill while probing spatial, planning, numerical, risk, communication, opponent, and teammate abilities. Human comparisons expose substantial opponent-modeling and teamwork gaps. Game interfaces, prompt policy, and model access constrain reproducibility.

**L03 — R. “ReConcile: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs.” 2024, ACL.** [Primary page/PDF](https://aclanthology.org/2024.acl-long.381/)  
Iterates heterogeneous model discussions with confidence-weighted consensus and human rectification demonstrations. Across seven benchmarks it reports up to +11.4 points; three weaker models can beat GPT-4, and a heterogeneous ensemble gains 8 points on MATH. Diversity is critical. Cost and response-budget matching matter, and the result conflicts with equal-budget studies where debate does not beat self-consistency.

**L04 — R. “MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents.” 2025, ACL.** [Primary page/PDF](https://aclanthology.org/2025.acl-long.421/)  
Introduces interactive cooperative/competitive scenarios, milestone KPIs, and star/chain/tree/graph topologies. Graph topology performs best in a research scenario; adding cognitive planning improves about 3%, and GPT-4o-mini is strongest on average among tested models. Benchmark agents still share designed protocols and compact worlds; milestone KPIs can reward procedural progress without external-world validity.

**L05 — R. “SILO-BENCH: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems.” 2026, ACL.** [Primary page/PDF](https://aclanthology.org/2026.acl-long.1354/)  
Defines 30 exact algorithmic tasks across aggregation, mesh, and global-shuffle communication; 3 protocols × 6 scales × 3 frontier LLMs yield 54 configurations and 1,620 experiments. Metrics are exact success, tokens, and communication density. On Level III tasks no tested system succeeds beyond 50 agents, revealing a communication–reasoning gap. Boundary: exact synthetic distributed algorithms isolate scaling failure but do not represent social incentives or embodied uncertainty.

### JAIR

**R01 — R. “On Centralized Critics in Multi-Agent Reinforcement Learning.” 2023, JAIR.** [Primary page/PDF](https://www.jair.org/index.php/jair/article/view/14386)  
Formally compares centralized/decentralized and state-/history-based critics under partial observability, then evaluates common MARL benchmarks. Contrary to common CTDE intuition, state critics can introduce bias and variance relative to history critics; representation-learning difficulty can conceal the theoretical effect. This is a direct warning against treating privileged state as automatically better.

**R02 — R. “Right Place, Right Time: Proactive Multi-Robot Task Allocation Under Spatiotemporal Uncertainty.” 2024, JAIR.** [Primary page/PDF](https://www.jair.org/index.php/jair/article/view/15057)  
Models future task announcements with continuous-time Markov chains and allocates robots proactively to minimize expected waiting time. Simulation beats reactive and partially informed baselines. The task-generation process must be learnable/stationary enough, and the paper does not provide physical-robot deployment evidence.

**R03 — R. “Generative Curricula for Multi-Agent Path Finding via Unsupervised and Reinforcement Learning.” 2025, JAIR.** [Primary page/PDF](https://www.jair.org/index.php/jair/article/view/17403)  
VAULT first learns a map latent space with a variational autoencoder, then generates a bi-level curriculum for decentralized learning-based MAPF. Public MAPF and generated maps test sample efficiency and unseen-map generalization; data pruning reduces map dependence. Limitation: curriculum quality inherits the training-map distribution and the learned MAPF policy still lacks the hard optimality/safety guarantees of exact solvers.

### Artificial Intelligence (AIJ)

**AI01 — R. “Solving simultaneous target assignment and path planning efficiently with time-independent execution.” 2023, Artificial Intelligence.** [Primary page](https://www.sciencedirect.com/science/article/pii/S0004370223000929)  
TSWAP interleaves arbitrary target assignment, one-step path planning, and target swaps, yielding a complete suboptimal solver and time-independent execution. Experiments report orders-of-magnitude speedups, near-optimal costs, and tolerance to real-robot execution delay. It targets unlabeled/assignable goals and does not optimize every MAPF objective.

**AI02 — R. “A stochastic process approach for multi-agent path finding with non-asymptotic performance guarantees.” 2024, Artificial Intelligence.** [Primary page](https://www.sciencedirect.com/science/article/pii/S0004370224000201)  
Combines conflict-based search and randomized/MCTS-like sampling; it is almost surely optimal and gives an \(O(1/\sqrt N)\) suboptimality bound after N single-agent subproblems. Grid benchmarks test solution cost/runtime. Known static graph, sources, goals, and offline planning are central assumptions; dynamic obstacles and uncertain execution are excluded.

**AI03 — R. “Robust and effective multi-agent path execution with timing uncertainty.” 2026, Artificial Intelligence.** [Primary page](https://www.sciencedirect.com/science/article/pii/S0004370226001128)  
Uses a Location Dependency Graph for executing precomputed paths under uncertain timing; remaining-plan feasibility is NP-complete, so the work supplies sound tests and online maximal move-set methods. Experiments measure delay/makespan and robustness. It protects execution of a fixed plan, not task reassignment or replanning under perception failures.

### Autonomous Agents and Multi-Agent Systems (JAAMAS)

**S01 — R. “Combining theory of mind and abductive reasoning in agent-oriented programming.” 2023, Autonomous Agents and Multi-Agent Systems.** [Primary full text](https://link.springer.com/article/10.1007/s10458-023-09613-w)  
TomAbd extends Jason/BDI agents with nested perspective and abductive reasoning. Hanabi evaluates score, uncertainty, and communication efficiency. It is an interpretable symbolic alternative to prompt-only ToM, but relies on hand-authored beliefs/rules and a domain where conventions and actions are discretized.

**S02 — R. “Formal contracts mitigate social dilemmas in multi-agent reinforcement learning.” 2024, Autonomous Agents and Multi-Agent Systems.** [Primary full text](https://link.springer.com/article/10.1007/s10458-024-09682-5)  
Agents voluntarily enter binding state/action-contingent reward-transfer contracts; under sufficiently rich contracts and observability, all subgame-perfect equilibria can be socially optimal. Multi-Objective Contract Augmentation Learning is tested in matrix/social-dilemma, traffic, pollution, Cleanup, and Harvest settings. Enforcement, observability, contractible features, and distributional fairness are not free; welfare gains do not settle who receives it.

**S03 — R. “A task delegation model: An approach based on trustworthiness in sub-delegations and delegation chain formation.” 2026, Autonomous Agents and Multi-Agent Systems.** [Primary full text](https://link.springer.com/article/10.1007/s10458-026-09741-z)  
Represents recursive delegation and AND/OR task decomposition as delegation chains; ε-greedy bandits select partners using success history, social image, reputation, know-how, and references, with alternative failure-propagation penalties. Synthetic dynamic environments show higher task success/satisfaction and faster adaptation than mono-episodic delegation. Authors explicitly do not compare trust models or learning algorithms in isolation; external factors are represented indirectly as behavior changes, so ecological validity is limited.

### Robotics bridge

**RB01 — R. “RoCo: Dialectic Multi-Robot Collaboration with Large Language Models.” 2024, ICRA.** [Author primary paper/project](https://project-roco.github.io/) · [DOI](https://doi.org/10.1109/ICRA57147.2024.10610855)  
Robot-specific LLMs discuss strategy, emit subtask/waypoint plans, receive collision/feasibility feedback, and pass validated goals to a centralized multi-arm motion planner. RoCoBench has six tabletop collaboration tasks; simulation and selected real/human-in-loop demonstrations report high task success. Critical boundary: language-level decentralization sits above centralized collision-aware motion planning; perception, hardware diversity, safety cases, and long deployments are narrow.

**RB02 — R. “Scalable Multi-Robot Collaboration with Large Language Models: Centralized or Decentralized Systems?” 2024, ICRA.** [Author/publisher primary record](https://research.ibm.com/publications/scalable-multi-robot-collaboration-with-large-language-models-centralized-or-decentralized-systems)  
Compares centralized, decentralized, and two hybrid LLM communication frameworks on four coordination-dependent 2D tasks as agent count grows, then demonstrates hybrids in 3D simulation with vision-to-text and dynamics errors. A hybrid gives the best success/token scaling. This contradicts a simple “decentralization scales” story: some hierarchy helps. Still, tasks are simulated and token efficiency omits networking, sensing, actuation, and real-time safety overhead.

## What the papers collectively say

### 1. Communication is a resource and a failure channel

The field has moved from “learn messages” to **design the communication substrate**: selective partners/timing (T2MAC), learned sparse graphs (CommFormer), sequential intent exchange (SeqComm), supernet architecture search (MaAS), hyperedges (HyperAgent), budgeted selection/topology (BAMAS), and exact protocol scaling tests (SILO-BENCH). Formal work separately asks what can be guaranteed when communication is delayed, asynchronous, restricted, or observable.

The convergence is real, but the semantics differ. A MARL message vector, an LLM transcript, and a certified reach–avoid communication action are not interchangeable. Token savings are not bandwidth/latency guarantees, and sparse topology is not security.

### 2. Centralization is neither simply good nor simply bad

- CTDE makes training tractable, yet state critics can be biased or high variance under partial observability (JAIR 2023).
- A central orchestration policy can efficiently search workflows (NeurIPS 2025), but introduces a single integrator and expensive training.
- Hybrid multi-robot communication can beat both fully centralized and fully decentralized language planners (ICRA 2024).
- Formal restricted-communication synthesis can guarantee reach–avoid objectives, but only with a known finite model.

The useful design axis is therefore **what is centralized, when, with what information, and under what failure model**, not a binary architecture label.

### 3. Benchmark success transfers weakly

AAMAS 2025 provides the clearest direct evidence: algorithms celebrated on SMAC/GRF can lose to ordinary baselines on fully cooperative RGB/sparse tasks. JaxMARL improves throughput and reproducibility but does not fix task diversity. LLM-agent work repeats the pattern with MATH/GSM8K/HumanEval/MMLU; these have exact cheap scoring and short feedback loops, favoring topology/revision optimization. SILO-BENCH then shows collapse beyond 50 agents on exact distributed tasks despite strong base models.

No reviewed paper justifies “general multi-agent intelligence.” The strongest claims are local: a protocol improves a stated metric under a stated team, model, budget, and environment.

### 4. Diversity helps only if integration preserves it

ReConcile’s heterogeneous models beat homogeneous or single-model reasoning in some settings. Hypothetical Minds benefits from maintaining separate hypotheses about different partners. Evolutionary RACE and attacker-population ROMANCE exploit population diversity. Yet Multi-Agent Teams Hold Experts Back finds integrative compromise can dilute the best member by up to 37.6%, and controlled-budget ICLR evidence finds debate no better than self-consistency. Diversity is an input; **aggregation is the algorithm**.

### 5. Formal MAS and LLM MAS use the same words differently

“Trust” can mean social-image/reputation dynamics in recursive delegation, an evidence weight in learned MARL communication, or confidence in an LLM answer. “Robustness” can mean bounded communication loss, sparse action attacks, uncertain execution timing, or resistance to a persuasive bad agent. “Agent” can mean a utility-bearing strategic actor, a decentralized policy, a robot, or an LLM call with a role prompt. Cross-paper comparisons must first align these semantics.

## Explicit contradictions and reconciliations

| Apparent contradiction | Evidence | Reconciliation / testable moderator |
|---|---|---|
| Debate improves reasoning vs debate adds nothing | ReConcile reports up to +11.4; ICLR self-correction study finds equal-budget debate does not beat self-consistency | Heterogeneous models, confidence aggregation, demonstrations, and unequal compute can create gains. Compare under identical total samples/tokens and verifier access. |
| More agents improve collective intelligence vs teams suppress experts | HyperAgent/MultiAgentBench show topology gains; ICML 2026 reports up to 37.6% expert loss | Gains require complementary errors and competence-aware routing. Consensus pressure and integrative compromise destroy sharp minority information. |
| Centralized information helps learning vs centralized critics can hurt | CTDE is standard; JAIR 2023 proves state critics may add bias/variance | State is not the same sufficient statistic as an agent’s history. Centralization helps only when the critic representation matches policy-relevant information. |
| Dense communication improves coordination vs sparse communication scales | Complete/dense graphs often improve task score; CommFormer/HyperAgent/BAMAS prune or restructure | Performance–cost frontier is task-dependent. Hyperedges can represent a group without all pairwise edges, but group formation itself must be learned and tested under distribution shift. |
| Decentralization scales vs hierarchy scales | Distributed methods remove bottlenecks; ICRA hybrid planner and central Puppeteer win in tested settings | Pure decentralization increases integration burden; pure centralization increases context and failure concentration. Hierarchical/hybrid systems often occupy the practical middle. |
| Self-play produces general reasoning vs self-play overfits conventions | TiZero/SPIRAL show strong learning and transfer | Transfer appears when games induce reusable operations; zero-sum/simple-game curricula may still teach brittle conventions. Hold out game families, partners, protocols, and incentives—not just instances. |
| Learned MAPF generalizes vs exact planning is needed for guarantees | VAULT improves unseen-map learning; AIJ gives completeness/optimality/sound execution results | Learning improves amortized decisions; exact/sound layers handle rare safety-critical conflicts. Hybrid evaluation should report both success and violation guarantees. |

## Negative spaces — what is still poorly evidenced

1. **Open systems with entry/exit and heterogeneous incentives.** Most MARL assumes fixed teams and shared reward; most LLM MAS assigns cooperative roles. Strategic participation, identity, Sybil behavior, coalition formation, and churn are rare together.
2. **Long-lived learning organizations.** Almost all LLM teams reset between benchmark questions. Persistent memory, staff turnover, policy evolution, and accumulation/correction of organizational errors lack longitudinal tests.
3. **Causal credit and responsibility.** Final-answer rewards dominate. MAST diagnoses traces, but causal attribution under interventions, counterfactual responsibility, and liability across delegation chains remain weak.
4. **Communication security as a systems property.** Topology papers optimize accuracy/tokens; security papers typically perturb messages/actions. Confidentiality, authentication, provenance, replay, compromised routers, and privacy leakage are seldom evaluated jointly with task quality.
5. **Calibration and abstention at team level.** Accuracy and reward dominate. Few papers measure whether a team knows when its consensus is unreliable, whether minority dissent is preserved, or whether delegation should stop.
6. **Fair compute accounting.** Agent count, rounds, temperature, model mix, tool calls, search budgets, training GPUs, and retry policies often differ. Equal-token, equal-latency, equal-dollar, and equal-energy comparisons are uncommon.
7. **Reproducible API-model experiments.** Model aliases drift; closed prompts and stochastic services hinder replication. HyperAgent’s 2026 paper still evaluates 2023/early-2024 OpenAI snapshots, illustrating the archival problem.
8. **Beyond math/code/QA.** Exact scoring enables fast research but weakens claims about negotiation, institutions, science, operations, and uncertain real-world evidence.
9. **Real multi-robot duration and scale.** Tabletop demonstrations and simulation dominate. Multi-day operation, dozens of heterogeneous robots, communications failure, wear, calibration drift, and safety certification are largely absent.
10. **Human partners beyond one-shot studies.** “Human-in-loop” often means a few demonstrations. Adaptation to diverse people, consent, workload, trust repair, and longitudinal team performance are under-measured.
11. **Bridges between formal guarantees and foundation-model agents.** Formal MAS assumes finite models/rationality/known dynamics; LLM MAS assumes black-box stochastic text generation. Verified wrappers exist in fragments, not end-to-end guarantees.
12. **Negative results and failed replications.** The expert-dilution, self-correction, MAST, centralized-critic, and extended-benchmark papers are unusually valuable because they challenge default intuitions. Comparable preregistered replication across model families and seeds is still rare.

## High-value research tests suggested by the map

These are not claims of novelty; they are falsifiable gaps exposed by the ledger.

1. **Competence-aware dissent-preserving routing:** compare majority consensus, best-member oracle, calibrated router, and topology learner under hidden/exposed expertise, adversarial members, and equal total tokens. Primary metrics: regret to best member, calibration, minority-information retention, attack success, and cost.
2. **Protocol transfer, not instance transfer:** train communication/topology on one family, then hold out agent count, role inventory, reward structure, communication constraints, and partner learning rule. Report worst-group and out-of-distribution performance, not only average accuracy.
3. **Verified LLM-to-robot stack:** allow LLM agents to allocate/decompose tasks, but require formal motion/temporal shields and provenance-carrying messages. Measure intervention rate, infeasible proposal rate, mission success, delay, and safety violations on physical hardware.
4. **Persistent MAS failure ecology:** run teams for weeks with memory, joining/leaving agents, changing competence, and planted misinformation. Measure error half-life, trust recovery, stale-memory propagation, delegation-chain responsibility, and accumulated cost.
5. **Compute-matched architecture tournament:** compare one strong agent with sampling, heterogeneous ensemble, debate, graph/hypergraph, and RL-searched workflows under equal dollar, wall-clock, token, and verifier budgets. This is the minimum fair test behind “multi-agent advantage.”

## Confidence and exclusions

- **High confidence:** exact titles, years, venues, and URLs in the ledger; these were checked against primary records. The strongest quantitative statements are restricted to numbers visible in primary full text.
- **Moderate confidence:** cross-paper synthesis, because benchmarks and metrics are deliberately heterogeneous. Reconciliation hypotheses are marked as such and should be tested.
- **Not claimed:** exhaustive enumeration of every MAS paper from 2023–2026; production readiness; clinical/traffic/robot safety; or a complete IJCAI 2026 census.
- NeurIPS 2026 was not treated as published because it had not occurred by the cut-off. I did not promote ICLR 2026 submissions to accepted papers; only an accepted conference record (SPIRAL) is used. I did not infer IJCAI 2026 acceptance from preprints or author pages without a stable proceedings record.

## Compact paper count audit

| Group | Count |
|---|---:|
| AAMAS | 6 |
| NeurIPS | 7 |
| ICML | 7 |
| ICLR | 7 |
| AAAI | 5 |
| IJCAI | 4 |
| ACL/EMNLP | 5 |
| JAIR | 3 |
| AIJ | 3 |
| JAAMAS | 3 |
| ICRA robotics bridge | 2 |
| **Unique papers** | **52** |

