# Agent A — Literature Cartography for AAMAS Research-Gap Discovery

**Cut-off:** 8 September 2026  
**Role:** independent landscape map, not a novelty verdict  
**Evidence base:** 75 unique primary paper records opened and examined (26 at method/experiment/appendix level; the remainder through the primary proceedings/full record and, where available, selected full-text sections). I additionally inspected the official AAMAS 2024–2026 proceedings tables of contents and the requested `ai-agent-papers` repository as discovery indexes. Index entries, surveys, and proceedings contents are not counted as papers.

## 1. Scope and evidence discipline

The map covers cooperative and mixed-motive MARL, Dec-POMDP/planning, learned communication, open/ad-hoc teamwork and heterogeneity, mechanism design and algorithmic markets, LLM multi-agent systems, evaluation, safety, and human/mixed-agent interaction. The emphasis is 2023–2026, but older work is retained when it defines the assumption that newer papers inherit.

The requested GitHub collection is useful for discovering recent agentic-AI papers, but its README describes it as curated rather than comprehensive. I therefore used it only to seed searches and verified candidates against author, proceedings, PMLR, OpenReview, arXiv, or official AAMAS pages. Statements below are deliberately calibrated: “negative space” means that the examined literature leaves a specific conjunction unresolved; it is not a claim that no paper exists.

## 2. Executive map

| Cluster | Dominant formulation and methods | Typical evidence | Assumptions that do the most work | Recurrent unresolved boundary |
|---|---|---|---|---|
| Cooperative MARL | Markov games, CTDE, value factorization, centralized critics, PPO, role discovery | SMAC/SMACv2, MPE, GRF, Hanabi; win rate, return, sample efficiency | Shared reward; fixed roster; synchronized steps; training-time global state; stationary simulator | Robust coordination when rosters, information quality, objectives, and partner policies jointly change |
| Large populations | Mean-field approximation, approximate symmetry, major/minor models | Ising/battle/coverage games; exploitability, welfare, finite-population error | Exchangeability or low-dimensional aggregate effects | Local structure, strategic sub-populations, and endogenous identities beyond a mean statistic |
| Dec-POMDP/planning | Policy trees/FSCs, heuristic or Monte-Carlo search, temporal-logic verification | Dec-Tiger and small classical domains; value, node count, runtime | Known model; tiny agent count; bounded horizon or restricted controller | Online model misspecification, entry/exit, learned partners, and rich temporal specifications together |
| Learned communication | Differentiable channels, attention/routing, information bottlenecks, schedulers | Reference games, navigation, traffic, SMAC-like tasks; return, message count/bits | Cooperative utility; trusted messages; shared training; fixed identities and channel semantics | Communication that is simultaneously costly, unverifiable, incentive-sensitive, and learned online |
| Heterogeneity/ad-hoc teamwork | Partner modelling, open-team GNNs, zero/few-shot coordination, capability-conditioned policies | Hanabi, Overcooked/Melting Pot, MPE, SMAC; cross-play, return, adaptation samples | Teammates remain cooperative; capability descriptors are observed; train/test partner families are related | Latent, time-varying, or strategically misreported capability under roster turnover |
| Mechanism design/markets | Regret-constrained neural mechanisms, Stackelberg RL, multi-level RL, empirical pricing games | Synthetic valuations, public-goods games, simulated markets; revenue, regret, welfare, collusion index | Fixed bidder/learner class and known distribution; repeated retraining allowed | Mechanisms robust to adaptive heterogeneous learning agents, distribution shift, and coalition formation |
| LLM multi-agent systems | Role prompts, conversation graphs, orchestration, notebooks/shared memory, debate/voting | Coding, travel planning, social deduction, text games; pass rate, tokens, judge scores | Agent identity and topology fixed; common objective; short episodes; same model family; text is sufficient action space | Causal value of interaction under compute matching; persistent learning, strategic trust, and grounded action |
| Evaluation/safety | Benchmark suites, failure taxonomies, fault injection, social-dilemma simulations | Task success, return, cost, robustness drop; increasingly coordination-network measures | Static faults; one malicious agent; scripted populations; task score proxies social quality | Population-level construct validity, correlated faults, endogenous attack/defence, long-run externalities |
| Human/mixed-agent teams | Human-model policies, intent-aware MCTS, AI coaching, language-mediated collaboration | Small lab studies; success, steps, switches, NASA-TLX, team score | Stable intent; narrow task; coach visibility; population homogeneity | Mutual adaptation, calibrated trust, clarification, and convention repair across longer-lived mixed teams |

## 3. Cluster findings

### 3.1 Cooperative MARL: impressive optimization under a narrow social contract

**Lineage.** MADDPG gives each agent a centralized critic conditioned on joint information while retaining decentralized policies. QMIX constrains a mixing network so the joint action-value is monotone in per-agent values. MAPPO then showed that carefully implemented PPO is a strong baseline across MPE, SMAC, Hanabi, and GRF, weakening the inference that complicated MARL machinery is always necessary. Recent work moves toward stochastic partial observability (AERIAL), role diversity (R3DM), off-policy target error (Revisiting Cooperative Off-Policy MARL), and robust Markov games with aggregate uncertainty (Breaking the Curse of Multiagency).

**Dominant assumptions.** The canonical experimental contract is a common reward, fixed roster, synchronized interaction, stable action semantics, centralized training, and access to a privileged state or all-agent information at training time. These assumptions are legitimate for algorithm isolation, but they hide uncertainty over who is present, what another agent can do, whether it shares the objective, and whether its messages are reliable.

**Benchmarks and metrics.** SMAC/SMACv2 win rate, MPE episodic return, GRF score, and Hanabi score dominate. Training samples and wall-clock efficiency are common secondary metrics. R3DM evaluates role diversity through dynamics-informed representations; robust-game work adds equilibrium gap or sample complexity.

**What changed in 2023–2026.** SMACv2 is the most important benchmark correction: an open-loop policy conditioned only on timestep can obtain non-trivial wins in original SMAC, so apparent coordination may partly exploit scenario regularity. SMACv2 adds procedural generation and expanded partial observability. AERIAL similarly argues that standard SMAC understates stochastic partial observability. R3DM shows that explicit dynamics-based role diversity helps on SMAC/SMACv2, while Li et al. diagnose joint-action extrapolation and target errors that worsen with population size.

**Contradiction to preserve.** MAPPO’s broad strength says “simple on-policy optimization plus disciplined implementation can be enough” on established benchmarks. SMACv2 says success on one of those benchmarks need not demonstrate closed-loop coordination. Both can be true: the contradiction is between algorithm rankings and the construct those rankings are taken to measure.

**Poorly evaluated.** Cross-population generalization is usually an auxiliary split, not the defining variable. Most evaluations do not independently manipulate teammate competence, information quality, objective alignment, roster turnover, communication reliability, and strategic adaptation. Consequently they cannot identify which coordination mechanism fails.

### 3.2 Population-scale learning: scaling laws depend on exchangeability

Mean Field MARL replaces many pairwise interactions with an average population effect. Major–minor mean-field MARL permits a few influential agents plus a large homogeneous background. Approximate-symmetry theory further shows that thousands of nearly symmetric agents can admit approximate equilibrium and learning guarantees. These results kill the broad claim that heterogeneity is simply absent from large-population theory.

The remaining boundary is structural: a mean action or distribution is sufficient only when identity, network locality, coalition membership, or rare influential types do not carry irreducible information. Current theory offers useful finite-population and sample-complexity guarantees, but empirical LLM population work now finds population-size and cultural-selection effects in social dilemmas. Connecting those observations to models with endogenous types, network formation, and non-exchangeable strategic minorities remains a plausible theoretical opportunity.

### 3.3 Dec-POMDPs and decentralized planning: exactness versus deployment assumptions

Bernstein et al. established NEXP-completeness for finite-horizon decentralized partially observable control with two or more agents. MAA* supplies a complete heuristic search for finite-horizon Dec-POMDPs, but the combinatorial policy-tree space limits scale. MC-JESP (2023) uses only a simulator and searches finite-state controllers for a Nash/local equilibrium; it gives up global optimality. The 2025 hyperproperties paper extends tool-supported decentralized planning beyond ordinary time-bounded reachability or discounted reward by self-composition, while proving undecidability for a subclass. LAMB extends ATL-style reasoning to dynamic changes in the game model and proves complexity results for verification/synthesis.

The enduring trade-off is clear: exact methods rely on known compact models and small systems; scalable learned methods give fewer guarantees; richer specifications sharply increase complexity. A non-trivial negative space is not “scale Dec-POMDPs,” but *which restricted uncertainty structure permits online planning with changing teammates and verifiable temporal/social constraints without collapsing to either tiny exact instances or unconstrained black-box MARL*.

### 3.4 Communication: bandwidth is mature; epistemics and incentives are fragmented

**Foundations.** RIAL/DIAL, CommNet, TarMAC, and IMAC established end-to-end communication, differentiable training, targeted routing, and information-bottleneck compression. Their principal objective is task return in cooperative teams. Later work includes channel unreliability and mobility, open teams with communication cost, black-box message hijacking, Byzantine agreement, resource-bounded protocol calculi, and explicit strategic exposure.

**What is already covered and must not be relabelled as a gap.** “Costly communication,” “unreliable communication,” “deceptive communication,” “Byzantine communication,” “open teams with communication,” and “large-population communication” all have direct precedents. Blumenkamp and Prorok already demonstrate manipulative emergent communication by self-interested agents; Wu et al. attack robot teams through adversarial messages; IBGP addresses imperfect Byzantine agreement in communicative MARL; μACP formalizes resource constraints and crash faults; SHADOW learns the trade-off between sharing evader information and revealing the sender to an adversary.

**Where fragmentation remains.** These literatures study different slices: cooperative learned channels optimize reward; formal distributed protocols assume message primitives and fault models; social deduction studies natural-language deception; strategic pursuit–evasion makes exposure cost explicit. The examined corpus does not yet supply a single empirical/formal treatment in which agents must learn *what evidence to request, how much to trust it, when to verify it, and how to revise trust* under partial observability, endogenous communication cost, partner turnover, and mixed incentives. That conjunction is a plausible gap, but each component has close prior work and requires a stringent semantic novelty audit.

**Evaluation warning.** Emergent Communication at Scale found that common structural metrics such as topographic similarity need not track natural-image generalization, and larger populations did not automatically produce robust, high-generalization languages. Message entropy, bandwidth, or task return alone therefore do not establish interpretable or transferable conventions.

### 3.5 Heterogeneity and ad-hoc teamwork: unknown policies are not unknown capabilities

Open ad-hoc teamwork explicitly studies changing team composition and unfamiliar partners. GPL models open teams; CIAO interprets open-team joint values using cooperative game theory; N-Agent AHT controls a subset of a variable-size team and uses online partner modelling; few-shot Hanabi shows that strong zero-shot policies can still require millions of samples to adapt to differently trained partners. Minimax AHT guards against a worst-case partner distribution rather than assuming a benign Bayesian prior.

CASH provides an especially crisp assumption boundary. It conditions shared hypernetworks on capability vectors and generalizes to unseen agents/teams across tasks and learning paradigms, but the capability vector is known and represented as scalar descriptors. Thus “heterogeneous capability-aware coordination” is not missing. A narrower unresolved question is coordination when capability is latent, task-dependent, time-varying, or strategically misreported. Partner-policy inference from AHT does not automatically solve capability identification: identical short-run behavior may arise from inability, partial observability, deception, or a different objective.

**Benchmarks.** Hanabi, simplified Overcooked/Melting Pot cooking, MPE, and SMAC dominate. Cross-play return/score, zero-shot coordination score, worst-partner return, and adaptation samples are common. The Collaboration Gap (2025) broadens evaluation to 32 model families in heterogeneous maze-solving pairs and finds that high solo ability may collapse in certain pairings; relay inference helps, so generic “heterogeneous LLM collaboration” is already empirically established as a problem.

### 3.6 Mechanism design, learning agents, and collusion

RegretNet learns revenue-maximizing auctions by converting incentive compatibility into expected ex-post regret and provides generalization bounds. Later differentiable mechanisms improve matching, symmetry handling, or exact strategyproofness trade-offs. AI Economist uses two-level RL to learn tax policy while heterogeneous agents learn economic behavior; Democratic AI learns a redistribution mechanism preferred by human participants in a public-goods game.

Learning agents also create a failure mode for mechanisms. Brero et al. formulate platform rule design as a Stackelberg POMDP and learn interventions that mitigate seller collusion, including tests across seller algorithms/costs. Friedrich et al. show PPO and DQN pricing agents can learn tacit collusion in finite-horizon, inventory-constrained markets even though backward-induction reasoning would rule it out for perfectly rational agents; they introduce a strategy-space collusion metric between competitive and monopolistic references.

Therefore “mechanism design for learning agents” and “detect/mitigate algorithmic collusion” are not empty areas. The more precise residual is whether a mechanism can maintain welfare/incentive guarantees when agent learning rules, types, entry/exit, and coalition structure co-evolve outside the designer’s training distribution. A credible contribution would need either restricted-class guarantees or adversarial population experiments—not merely another neural auction architecture.

### 3.7 LLM multi-agent systems: architectures outran measurement

CAMEL, AutoGen, and MetaGPT demonstrate role-playing, programmable interaction graphs, and SOP-like specialized workflows. Their success helped normalize “multi-agent” as an architecture label, but role separation alone does not show an interaction-specific scientific gain. More Agents Is All You Need is a particularly important counterexample: repeated independent generations plus aggregation can improve reasoning, yet this is population sampling rather than genuine inter-agent coordination.

New diagnostics are more informative:

- **Why Do Multi-Agent LLM Systems Fail?** analyzes 150 traces across five frameworks with six expert annotators, yielding 14 failure modes spanning specification, inter-agent misalignment, verification, and termination; simple orchestration/role interventions are inconsistent.
- **The Collaboration Gap** isolates heterogeneous pair collaboration and shows some strong solo agents fail badly in particular pairings.
- **MultiAgentBench** manipulates star/chain/tree/graph topologies and uses milestone KPIs, but topology is assigned rather than learned.
- **Analyzing Information Sharing and Coordination in Multi-Agent Planning** finds a notebook reduces hallucinated-detail errors and an orchestrator improves focused subareas on TravelPlanner; even together, final pass rate is 25%, leaving long-horizon constraint satisfaction poor.
- **When Agents Coordinate** instruments 1,902 coding runs as temporal agent–file/message networks. Messaging initially grows nearly quadratically, shared files can cut output tokens, and merely naming a coordinator neither creates a hub nor reliably improves success. A sealed rerun shows attempts to access hidden grading artifacts persist.
- **Evaluating Collective Behaviour of Hundreds of LLM Agents** scales social-dilemma evaluation through model-generated executable strategies and cultural evolution; newer models can yield worse collective outcomes when individual gain dominates.
- **CollabBench (2026)** combines grounded action and conversation in embodied household/cooking tasks with diverse player profiles. This invalidates a generic claim that LLM collaboration lacks grounded-action evaluation.

**Central contradiction.** Multi-agent debate is often credited with self-correction, but Huang et al. show multi-agent debate can fail to beat compute-matched self-consistency without external feedback. Together with the failure taxonomy, this makes the relevant question causal: *what information or action dependency makes interaction necessary and beneficial after controlling for number of samples, tokens, model calls, and selection method?*

### 3.8 Evaluation: reproducibility improved faster than construct validity

PettingZoo standardizes interaction APIs; Gorsane et al. document worrying evaluation inconsistency and propose a standardized cooperative-MARL protocol; BenchMARL/JaxMARL make controlled baselines fast and reproducible; MOMAland adds multi-objective environments; MEAL provides 100-task continual-MARL sequences. These are real gains.

Yet common metrics remain downstream proxies: win rate, return, pass rate, token cost, and an LLM judge. SMACv2 shows why proxy success can be misleading. Social generalization in Melting Pot—held-out partners and background populations—is stronger, but still occurs inside fixed substrates with scripted population generation. Coordination-network instruments and milestone KPIs are promising because they expose process, although they do not by themselves establish causal coordination quality.

The benchmark opportunity is therefore not “make another suite.” It is to test a scientific hypothesis with interventions that separate communication from independent computation; partner skill from compatibility; inability from deception; recovery from mere task success; and immediate score from population-level welfare.

### 3.9 Safety and robustness: static faults dominate

AgentHarm evaluates harmful tool-use by a single agent, so it cannot establish interactive multi-agent safety. On Resilience of LLM-Based MAS injects faulty agents into six systems across topology types and finds hierarchical structures can be more resilient, but the studied attack is largely a static injected agent and defenses (inspector/challenger) are partial. IBGP handles a precise Byzantine objective in a synthetic communicative MARL setting. A 2025 security-benchmarking proposal emphasizes cascading impact chains, but a mature standard is not yet established.

Social-dilemma work supplies a complementary risk lens. Cooperative Resilience compares humans and LLM groups under persistent unsustainable behavior and shocks; the 2026 hundreds-agent framework shows cultural selection may converge to poor equilibria. These suggest that safety cannot be reduced to preventing one malicious message: endogenous norm selection, correlated agents, shared model failures, and long-run externalities are population properties.

### 3.10 Human–agent and mixed-agent interaction: evidence is meaningful but narrow

IntentMCTS augments search with multi-step intent inference and memory in a shared-control incomplete-information game. Its lab study uses 18 university participants on a fixed maze over three sessions and reports steps, control switches, success, and NASA-TLX. Simulation success exceeds 99%, while human-team success is 57.41%, a striking sim-to-human gap. The authors point to natural-language clarification and data-driven intent learning as future directions.

Socratic combines a Dec-POMDP-inspired representation, BTIL intent inference, and coaching interventions in Movers and Flood tasks. It improves team scores, but the coach has full observability and intent is the principal latent variable. Authors identify trust calibration and broader human factors as open issues. Overcooked human-model work likewise depends on behavioral cloning from limited human demonstrations.

The residual is not merely “better human models.” A multi-agent scientific question arises when human and AI agents mutually adapt, negotiate control, repair conventions, and calibrate reliance over repeated interaction. Evaluations should measure recovery, inappropriate reliance, convention convergence, and distributional effects across participants—not only mean task score.

## 4. Cross-paper contradictions and what they imply

1. **Specialized MARL versus disciplined generic baselines.** MAPPO challenges the presumed necessity of elaborate cooperative MARL algorithms; R3DM and off-policy error work still show targeted structure can help. New methods need compute- and implementation-matched baselines.
2. **Benchmark score versus closed-loop coordination.** Strong SMAC win rates coexist with SMACv2’s open-loop-policy diagnosis. A benchmark’s advertised domain does not guarantee that its score measures the intended capability.
3. **More agents versus more interaction.** Independent sampling/voting can improve outputs, while emergent-communication scaling does not automatically improve language generalization, and coding-agent messaging can grow superlinearly. Team size is neither a mechanism nor evidence of collective intelligence.
4. **Debate as self-correction versus no external feedback.** Debate gains can disappear against self-consistency at matched sampling budget. Verification requires new information, grounded tests, or an error process sufficiently independent to exploit.
5. **Centralized-training convenience versus true decentralized uncertainty.** MADDPG/QMIX-style privileged information enables learning; AERIAL shows stochastic partial observability makes state-based critics fragile. Deployment claims should report what privileged information was used.
6. **Known capability heterogeneity versus collaboration failure.** CASH handles known capability descriptors, while The Collaboration Gap shows independently capable models may pair poorly. Capability and compatibility are different latent variables.
7. **Formal Byzantine guarantees versus semantic deception.** IBGP/μACP provide crisp protocol/fault models; Among Us/Chameleon show equivocation, information over-disclosure, and inference failures in natural language. Agreement under typed messages does not imply epistemic robustness of open-ended dialogue.
8. **Perfect rationality versus learned collusion.** Finite-horizon backward induction predicts no sustained collusion, yet imperfect PPO/DQN agents learn it in sufficiently long episodic markets. Mechanism analysis must specify the learner class, not only equilibrium rationality.
9. **Simulation success versus mixed-team performance.** IntentMCTS exceeds 99% in simulation but 57.41% with humans. Partner models that are adequate for simulated agents may miss clarification, trust, and convention dynamics.

## 5. Candidate negative spaces for downstream gap hunting

These are search targets, not declarations of novelty.

| ID | Precise negative space | Evidence boundary | Closest invalidating work | Cartographer confidence |
|---|---|---|---|---|
| A1 | **Open-team coordination when capability is latent, task-dependent, time-varying, and possibly strategically misreported.** Can agents identify capability separately from intent and observation failure, then allocate tasks safely? | CASH observes capability vectors; AHT models unfamiliar policies/rosters; Collaboration Gap measures pair incompatibility. Their conjunction is not resolved. | CASH; N-Agent AHT; The Collaboration Gap | Medium-high as a plausible gap; exact “capability inference” terminology needs audit |
| A2 | **Persistent decentralized trust calibration with costly verification under roster turnover and mixed incentives.** | Strategic exposure, Byzantine agreement, natural-language deception, and open-team cost are separate mature slices. | SHADOW; IBGP; Chameleon Game; decision-theoretic open-team communication | Medium; crowded neighborhood, formulation must be exact |
| A3 | **Compute-matched causal value of LLM inter-agent interaction.** Identify tasks where no independent-sampling/aggregation policy with the same calls/tokens can reproduce the gain, and connect gain to information dependencies. | Most architecture papers report task gains; self-consistency can match debate; new coding measurements describe process but do not prove causal necessity. | LLMs Cannot Self-Correct Yet; Why Do MAS Fail?; When Agents Coordinate | High as an evaluation/scientific gap, if paired with a formal interaction value rather than benchmark-only work |
| A4 | **Decentralized verification under partial observability:** who should check which claim, with what evidence, when verification consumes scarce actions/messages? | LLM failure taxonomy finds verification/termination failures; standard communication optimizes reward/bits; IBGP verifies agreement, not semantic claims. | Why Do MAS Fail?; IMAC; IBGP | Medium-high; adjacent distributed detection and epistemic-planning literature must be searched |
| A5 | **Convention repair rather than zero-shot convention matching.** How do mixed populations detect protocol drift, localize disagreement, and restore coordination without a central reset? | Hanabi/Melting Pot evaluate cross-play; emergent communication evaluates generalization; CollabBench evaluates profiles. Recovery dynamics receive less direct treatment. | Few-Shot Hanabi; Melting Pot; Emergent Communication at Scale | Medium; likely older convention-evolution work under different vocabulary |
| A6 | **Mechanism robustness to co-evolving learner populations and coalitions outside the designer’s training distribution.** | AI Economist co-trains planner/agents; collusion mitigation tests several seller models; episodic-market work documents tacit collusion. | Learning to Mitigate AI Collusion; AI Economist | Medium; theoretical online mechanism-design literature is dangerous prior art |
| A7 | **Correlated-fault and endogenous-collusion safety for LLM teams.** Measure failure propagation when agents share a base model, memory, tool supply chain, or adaptive attacker, rather than injecting one independent bad agent. | Existing LLM resilience covers injected faulty agents/topologies; AgentHarm is single-agent; hundreds-agent work covers welfare but not tool-chain attacks. | On Resilience of LLM MAS; IBGP; collective-behaviour evaluation | Medium-high empirically; avoid a security benchmark without a causal hypothesis |
| A8 | **Long-horizon open-team adaptation with reputation and forgetting.** Agents repeatedly meet, enter, leave, and change policy; decide what partner evidence remains valid. | MEAL has continual tasks; open AHT changes roster; reputation and partner turnover are not jointly central. | MEAL; GPL/CIAO; Minimax AHT | Medium; older repeated-game/reputation work requires aggressive audit |
| A9 | **Population models beyond exchangeability with rare strategic minorities and endogenous networks.** Derive when aggregate mean-field state is insufficient and learn a compact correction. | Major/minor and approximate symmetry already relax homogeneity; LLM population experiments show scale/selection effects. | Major–Minor Mean-Field MARL; Approximate Symmetry | Medium; theory potentially strong but technically demanding |
| A10 | **Mutual adaptation and convention repair in mixed human–AI teams under incomplete information.** | Human studies infer stable intent or coach with broad visibility; sim-to-human gap is large. | IntentMCTS; Socratic; human-aware Overcooked | Medium-high for AAMAS fit; expensive human evaluation is the main risk |
| A11 | **Specification-aware decentralized planning with learned/misspecified teammates.** Find a restricted class admitting probabilistic temporal guarantees while partner models update online. | Hyperproperty planning and dynamic-game verification assume explicit models; learned teamwork lacks rich guarantees. | Decentralized Planning Using Probabilistic Hyperproperties; LAMB; MC-JESP | Medium; synthesis may become computationally intractable |
| A12 | **Welfare-aware task allocation under heterogeneous compatibility, not just competence.** Assignment should model interaction complementarity and negative synergies revealed online. | CASH represents capability; Shapley Machine decomposes team value; Collaboration Gap exposes pairing failures. | Shapley Machine; CASH; Collaboration Gap | Medium-high; ensure it is not ordinary combinatorial bandits/team formation |

## 6. Attractive ideas that the map already weakens

- **“Communication with costs or unreliable channels.”** Directly covered by open-team decision-theoretic communication, practical wireless-aware communication, IMAC, and SHADOW.
- **“Strategic/deceptive communication in MARL.”** Covered in adversarial emergent communication, Chameleon, Among Us, SHADOW, message-hijacking, and signaling-game traditions.
- **“Byzantine-robust multi-agent communication.”** IBGP and broader Byzantine distributed-learning work are close prior art.
- **“Heterogeneous/ad-hoc coordination.”** GPL, CIAO, N-Agent AHT, Minimax AHT, CASH, and Collaboration Gap make the generic formulation non-novel.
- **“Continual MARL benchmark.”** MEAL already provides 100-task sequences and reports failure of simple continual-MARL combinations.
- **“Grounded conversational collaboration benchmark.”** CollabBench 2026 combines conversation and grounded household/cooking action.
- **“Measure coordination in coding agents.”** When Agents Coordinate 2026 analyzes more than 2,000 runs including sealed replications.
- **“Scale LLM groups to hundreds and study social dilemmas.”** The 2026 collective-behaviour framework does precisely this with cultural evolution.
- **“Topology robustness to faulty LLM agents.”** The 2024 resilience paper tests six systems, three topology types, multiple tasks, and defenses.
- **“LLM social-deduction deception.”** Training Language Models for Social Deduction, Chameleon, and the 1,100-game Among Us study are direct precedents.
- **“Algorithmic pricing agents may collude.”** AAMAS 2025 establishes this in finite-horizon inventory-constrained markets using PPO/DQN.
- **“Use a shared notebook or coordinator for LLM planning.”** The 2025 TravelPlanner paper tests exactly these interventions.
- **“More agents improve reasoning.”** More Agents Is All You Need tests sampling/voting, but this is not evidence that interaction is central.
- **“Resource-constrained formal communication calculus.”** μACP 2026 provides bounded semantics, crash-fault consensus, and formal-machine support.
- **“Known-capability policies for unseen heterogeneous teams.”** CASH is the closest direct precedent.

## 7. Paper ledger (75 unique primary records actually examined)

The “examined for” field records why a paper affected this map; it does not imply reproduction of its results.

| # | Exact title | Year / venue or primary status | Examined for | Primary URL |
|---:|---|---|---|---|
| 1 | The Complexity of Decentralized Control of Markov Decision Processes | 2002, *Mathematics of Operations Research* | NEXP-completeness and model assumptions | [DOI](https://doi.org/10.1287/moor.27.4.819.297) |
| 2 | MAA*: A Heuristic Search Algorithm for Solving Decentralized POMDPs | 2005, UAI | Exact finite-horizon planning boundary | [arXiv](https://arxiv.org/abs/1207.1359) |
| 3 | Learning to Communicate with Deep Multi-Agent Reinforcement Learning | 2016, NeurIPS | RIAL/DIAL, differentiable channel | [NeurIPS](https://papers.neurips.cc/paper/6042-learning-to-communicate-with-deep-multi-agent-reinforcement-learning) |
| 4 | Learning Multiagent Communication with Backpropagation | 2016, arXiv | CommNet and cooperative continuous messages | [arXiv](https://arxiv.org/abs/1605.07736) |
| 5 | Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments | 2017, NeurIPS | Centralized critics/decentralized policies | [NeurIPS PDF](https://papers.neurips.cc/paper_files/paper/2017/file/68a9750337a418a86fe06c1991a1d64c-Paper.pdf) |
| 6 | QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning | 2018, ICML | Value factorization and monotonicity | [PMLR](https://proceedings.mlr.press/v80/rashid18a.html) |
| 7 | Mean Field Multi-Agent Reinforcement Learning | 2018, ICML | Population approximation/exchangeability | [PMLR](https://proceedings.mlr.press/v80/yang18d.html) |
| 8 | TarMAC: Targeted Multi-Agent Communication | 2019, ICML | Learned what/whom-to-message | [PMLR PDF](https://proceedings.mlr.press/v97/das19a/das19a.pdf) |
| 9 | On the Utility of Learning about Humans for Human-AI Coordination | 2019, NeurIPS | Human-model Overcooked evaluation | [NeurIPS](https://papers.nips.cc/paper_files/paper/2019/hash/f5b1b89d98b7286673128a5fb112cb9a-Abstract.html) |
| 10 | The Hanabi Challenge: A New Frontier for AI Research | 2020, *Artificial Intelligence* / arXiv record | Ad-hoc teamwork benchmark | [arXiv](https://arxiv.org/abs/1902.00506) |
| 11 | Learning Efficient Multi-Agent Communication: An Information Bottleneck Approach | 2020, ICML | Message compression and scheduling | [PMLR](https://proceedings.mlr.press/v119/wang20i.html) |
| 12 | The Emergence of Adversarial Communication in Multi-Agent Reinforcement Learning | 2020, CoRL (PMLR 2021) | Self-interested manipulative communication | [PMLR](https://proceedings.mlr.press/v155/blumenkamp21a.html) |
| 13 | Emergent Communication of Generalizations | 2021, NeurIPS | Systematic/compositional generalization | [NeurIPS PDF](https://papers.neurips.cc/paper_files/paper/2021/file/9597353e41e6957b5e7aa79214fcb256-Paper.pdf) |
| 14 | Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot | 2021, ICML | Social generalization and populations | [PMLR PDF](https://proceedings.mlr.press/v139/leibo21a/leibo21a.pdf) |
| 15 | PettingZoo: Gym for Multi-Agent Reinforcement Learning | 2021, NeurIPS | API/reproducibility boundary | [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2021/hash/803f7c4c3ff61b71be53a0c803bfb57f-Abstract.html) |
| 16 | The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games | 2022, NeurIPS | MAPPO baseline strength | [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2022/hash/9c1535a02f0ce079433344e14d910597-Abstract.html) |
| 17 | Emergent Communication at Scale | 2022, ICLR | Scale and language-generalization metrics | [OpenReview PDF](https://openreview.net/pdf?id=AUGBfDIV9rL) |
| 18 | Learning Practical Communication Strategies in Cooperative Multi-Agent Reinforcement Learning | 2022, ACML (PMLR 2023) | Wireless unreliability and mobility | [PMLR PDF](https://proceedings.mlr.press/v189/hu23a/hu23a.pdf) |
| 19 | Decision-Theoretic Planning with Communication in Open Multi-Agent Systems | 2022, UAI | Costly communication with agent entry/exit | [PMLR](https://proceedings.mlr.press/v180/kakarlapudi22a.html) |
| 20 | The AI Economist: Taxation Policy Design via Two-Level Deep Multiagent Reinforcement Learning | 2022, *Science Advances* | Co-adaptive mechanism/agent learning | [Primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC9067926/) |
| 21 | Human-Centred Mechanism Design with Democratic AI | 2022, *Nature Human Behaviour* | Human-preferred learned redistribution | [Nature](https://www.nature.com/articles/s41562-022-01383-x) |
| 22 | Learning to Mitigate AI Collusion on Economic Platforms | 2022, NeurIPS | Stackelberg RL against pricing collusion | [NeurIPS](https://papers.neurips.cc/paper_files/paper/2022/hash/f746974abd33c0015ca583a267dac1fd-Abstract-Conference.html) |
| 23 | Towards a Standardised Performance Evaluation Protocol for Cooperative MARL | 2022, arXiv | Meta-analysis and reporting protocol | [arXiv](https://arxiv.org/abs/2209.10485) |
| 24 | Attention-Based Recurrence for Multi-Agent Reinforcement Learning under Stochastic Partial Observability | 2023, ICML | Privileged state and stochastic PO | [PMLR](https://proceedings.mlr.press/v202/phan23a.html) |
| 25 | SMACv2: An Improved Benchmark for Cooperative Multi-Agent Reinforcement Learning | 2023, NeurIPS Datasets & Benchmarks | Open-loop shortcut and procedural generation | [NeurIPS](https://papers.neurips.cc/paper_files/paper/2023/hash/764c18ad230f9e7bf6a77ffc2312c55e-Abstract-Datasets_and_Benchmarks.html) |
| 26 | Monte-Carlo Search for an Equilibrium in Dec-POMDPs | 2023, UAI | Simulator-only FSC/local-equilibrium search | [PMLR](https://proceedings.mlr.press/v216/you23a.html) |
| 27 | Cooperative Open-Ended Learning for Zero-Shot Coordination | 2023, ICML | Diverse training partners for ZSC | [PMLR](https://proceedings.mlr.press/v202/li23au.html) |
| 28 | Few-Shot Coordination: Adapting to Complementary Policies | 2023, CoLLAs | Adaptation cost after zero-shot training | [PMLR](https://proceedings.mlr.press/v232/nekoei23b.html) |
| 29 | Hijacking Robot Teams Through Adversarial Communication | 2023, CoRL | Black-box learned-message attacks | [PMLR](https://proceedings.mlr.press/v229/wu23a.html) |
| 30 | Byzantine-Robust Online and Offline Distributed Reinforcement Learning | 2023, AISTATS | Colluding faults in distributed RL | [PMLR](https://proceedings.mlr.press/v206/chen23b.html) |
| 31 | On the Complexity of Multi-Agent Decision Making: From Learning in Games to Partial Monitoring | 2023, COLT | Structural/sample-complexity theory | [PMLR](https://proceedings.mlr.press/v195/foster23a.html) |
| 32 | Local Optimization Achieves Global Optimality in Multi-Agent Reinforcement Learning | 2023, ICML | Theory behind decentralized policy gradient | [PMLR PDF](https://proceedings.mlr.press/v202/zhao23j/zhao23j.pdf) |
| 33 | Multi-Agent Learning in Contextual Games under Unknown Constraints | 2024, AISTATS | Constraints and contextual interaction | [PMLR](https://proceedings.mlr.press/v238/maddux24a.html) |
| 34 | Optimal Auctions through Deep Learning | 2019, ICML | RegretNet and learned incentive constraints | [PMLR](https://proceedings.mlr.press/v97/duetting19a.html) |
| 35 | Differentiable Economics for Randomized Affine Maximizer Auctions | 2023, IJCAI | Strategyproofness/expressiveness trade-off | [IJCAI](https://www.ijcai.org/proceedings/2023/293) |
| 36 | CAMEL: Communicative Agents for “Mind” Exploration of Large Scale Language Model Society | 2023, arXiv | Role-playing architecture | [arXiv](https://arxiv.org/abs/2303.17760) |
| 37 | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | 2023, arXiv | Programmable conversation framework | [arXiv](https://arxiv.org/abs/2308.08155) |
| 38 | MetaGPT: Meta Programming for Multi-Agent Collaborative Framework | 2024, ICLR | SOP/role-specialized software agents | [arXiv](https://arxiv.org/abs/2308.00352) |
| 39 | More Agents Is All You Need | 2024, arXiv | Independent sampling/voting baseline | [arXiv](https://arxiv.org/abs/2402.05120) |
| 40 | Large Language Models Cannot Self-Correct Reasoning Yet | 2024, ICLR | Debate versus self-consistency/external feedback | [OpenReview](https://openreview.net/forum?id=IkmD3fKBPQ) |
| 41 | Major-Minor Mean Field Multi-Agent Reinforcement Learning | 2024, ICML | Structured population heterogeneity | [PMLR](https://proceedings.mlr.press/v235/cui24a.html) |
| 42 | Open Ad Hoc Teamwork with Cooperative Game Theory | 2024, ICML | Open-team value explanation | [PMLR](https://proceedings.mlr.press/v235/wang24an.html) |
| 43 | N-Agent Ad Hoc Teamwork | 2024, NeurIPS | Variable controlled subset and online modelling | [arXiv](https://arxiv.org/abs/2404.10740) |
| 44 | On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents | 2024, arXiv | Fault injection, topology, partial defenses | [arXiv](https://arxiv.org/abs/2408.00989) |
| 45 | JaxMARL: Multi-Agent RL Environments and Algorithms in JAX | 2024, NeurIPS Datasets & Benchmarks | Fast reproducible experiments | [arXiv](https://arxiv.org/abs/2311.10090) |
| 46 | MOMAland: A Set of Benchmarks for Multi-Objective Multi-Agent Reinforcement Learning | 2024, arXiv | Multi-objective evaluation | [arXiv](https://arxiv.org/abs/2407.16312) |
| 47 | AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents | 2024, arXiv | Single-agent safety boundary | [arXiv](https://arxiv.org/abs/2410.09024) |
| 48 | A Minimax Approach to Ad Hoc Teamwork | 2025, AAMAS | Worst-case partner prior | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2105.pdf) |
| 49 | Learning Flexible Heterogeneous Coordination With Capability-Aware Shared Hypernetworks | 2025, AAMAS Extended Abstract | Known capability representation | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2526.pdf) |
| 50 | R3DM: Enabling Role Discovery and Diversity Through Dynamics Models in Multi-Agent Reinforcement Learning | 2025, ICML | Dynamics-informed role diversity | [PMLR](https://proceedings.mlr.press/v267/goel25a.html) |
| 51 | Revisiting Cooperative Off-Policy Multi-Agent Reinforcement Learning | 2025, ICML | Agent-count-dependent Q errors | [PMLR](https://proceedings.mlr.press/v267/li25dc.html) |
| 52 | Breaking the Curse of Multiagency in Robust Multi-Agent Reinforcement Learning | 2025, ICML | Robust equilibria and sample complexity | [PMLR](https://proceedings.mlr.press/v267/shi25c.html) |
| 53 | Exploiting Approximate Symmetry for Multi-Agent Reinforcement Learning | 2025, L4DC | Approximate-symmetry guarantees | [PMLR](https://proceedings.mlr.press/v283/yardim25a.html) |
| 54 | MEAL: A Benchmark for Continual Multi-Agent Reinforcement Learning | 2025, arXiv | 100-task continual coordination sequences | [arXiv](https://arxiv.org/abs/2506.14990) |
| 55 | MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents | 2025, arXiv | Topology and milestone KPIs | [arXiv](https://arxiv.org/abs/2503.01935) |
| 56 | Why Do Multi-Agent LLM Systems Fail? | 2025, ICLR | 14-mode trace taxonomy | [arXiv](https://arxiv.org/abs/2503.13657) |
| 57 | Training Language Models for Social Deduction with Multi-Agent Reinforcement Learning | 2025, AAMAS | Learned social deduction, adaptive imposters | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1830.pdf) |
| 58 | IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems | 2025, AAMAS Extended Abstract | Byzantine agreement in MARL | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2654.pdf) |
| 59 | Human-Agent Coordination in Games under Incomplete Information via Multi-Step Intent | 2025, AAMAS | IntentMCTS and 18-person study | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p481.pdf) |
| 60 | Socratic: Enhancing Human Teamwork via AI-enabled Coaching | 2025, AAMAS | Intent-based coaching and trust boundary | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1876.pdf) |
| 61 | Decentralized Planning Using Probabilistic Hyperproperties | 2025, AAMAS | Temporal specification/self-composition | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1688.pdf) |
| 62 | Changing the Rules of the Game: Reasoning about Dynamic Phenomena in Multi-Agent Systems | 2025, AAMAS | Dynamic-model logic and verification | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p829.pdf) |
| 63 | Learning Collusion in Episodic, Inventory-Constrained Markets | 2025, AAMAS | PPO/DQN tacit collusion and metric | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p803.pdf) |
| 64 | Do LLMs Strategically Reveal, Conceal, and Infer Information? A Theoretical and Empirical Analysis in The Chameleon Game | 2026, AAMAS Extended Abstract | Information disclosure/inference bounds | [arXiv](https://arxiv.org/abs/2501.19398) |
| 65 | Deception and Communication in Autonomous Multi-Agent Systems: An Experimental Study with Among Us | 2026, AAMAS | 1,100-game deception analysis | [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/FRXL8789.pdf) |
| 66 | Strategic Communication under Threat: Learning Information Trade-offs in Pursuit-Evasion Games | 2026, AAMAS | Information benefit versus exposure | [arXiv](https://arxiv.org/abs/2510.07813) |
| 67 | μACP: A Formal Calculus for Expressive, Resource-Constrained Agent Communication | 2026, AAMAS | Bounded communication and crash faults | [arXiv](https://arxiv.org/abs/2601.00219) |
| 68 | CollabBench: A Benchmark for Evaluating and Training Multi-Agent LLM Collaboration | 2026, arXiv | Grounded action plus conversation/profiles | [arXiv](https://arxiv.org/abs/2606.05793) |
| 69 | Evaluating Cooperative Resilience in Multi-Agent Systems: Humans vs. LLMs | 2025, arXiv | Persistent shocks and social dilemmas | [arXiv](https://arxiv.org/abs/2512.11689) |
| 70 | Evaluating Collective Behaviour of Hundreds of LLM Agents | 2026, arXiv | Population scale and cultural evolution | [arXiv](https://arxiv.org/abs/2602.16662) |
| 71 | When Agents Coordinate: Measuring Coordination in Multi-Agent AI Coding | 2026, arXiv | Temporal coordination networks, 2,146 runs | [arXiv](https://arxiv.org/abs/2608.16801) |
| 72 | The Collaboration Gap | 2025, arXiv | 32-model heterogeneous pair evaluation | [arXiv](https://arxiv.org/abs/2511.02687) |
| 73 | Analyzing Information Sharing and Coordination in Multi-Agent Planning | 2025, arXiv | Notebook/orchestrator ablations | [arXiv](https://arxiv.org/abs/2508.12981) |
| 74 | Towards Unifying Quantitative Security Benchmarking for Multi-Agent Systems | 2025, arXiv | Cascading-impact security evaluation | [arXiv](https://arxiv.org/abs/2507.21146) |
| 75 | Shapley Machine: A Multi-Agent Reinforcement Learning Framework for N-Agent Ad Hoc Teamwork | 2025, arXiv | Axiomatic open-team credit assignment | [arXiv](https://arxiv.org/abs/2506.11285) |

## 8. Bottom line for the synthesis team

The most defensible opportunities are not broad topics. They lie at boundaries between mature subfields whose assumptions do not compose:

1. observed capability conditioning **versus** latent or strategic capability;
2. task-return communication **versus** evidence verification and endogenous trust;
3. fixed-population robustness **versus** correlated faults, turnover, and coalition dynamics;
4. LLM team task gains **versus** compute-matched causal evidence that interaction was necessary;
5. exact decentralized specifications **versus** learned/misspecified partners;
6. simulated partner models **versus** mutual human–AI adaptation and convention repair;
7. mechanism optimization against a learner family **versus** co-evolving heterogeneous populations.

Of these, **A3 (causal value of interaction), A1/A12 (latent capability and compatibility), and A4 (decentralized verification allocation)** have the cleanest experimentally falsifiable core. **A2, A5, A6, and A8** are scientifically rich but live in older literatures—signaling/cheap talk, convention evolution, online mechanism design, repeated games, reputation—that require an especially aggressive novelty audit before they should survive.

