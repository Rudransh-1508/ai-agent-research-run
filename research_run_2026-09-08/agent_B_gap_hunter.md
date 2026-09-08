# Agent B — Gap Hunter

**Search cutoff:** 8 September 2026.  
**Role boundary:** independent candidate generation, not final novelty certification. Every “missing” claim below means *not directly addressed in the searched literature under the stated conditions*, not “no paper exists.”  
**Search process:** screened 90+ bibliographic records; retained a unique ledger of 58 primary-paper/proceedings records that materially informed the candidates. I inspected available methods/assumptions/experiment descriptions and limitation text when indexed, not only titles. The required `ai-agent-papers` repository was checked as a useful but explicitly selective LLM-agent index; its README says it does not aim for comprehensiveness. Classical MARL, game theory, ad-hoc teamwork, HRI, robotics, privacy, and mechanism-design searches were therefore performed separately.

## Fast map of recurring assumptions that produced gaps

1. **Unknown partners are usually fixed while being identified.** Ad-hoc-teamwork methods adapt to a latent teammate type or sudden change, but active probes are rarely modeled as simultaneously *teaching or steering* a learning partner.
2. **Communication semantics are jointly stationary.** Translation and cross-play methods handle incompatible protocols, while continual co-drift of both protocols is usually absent.
3. **Cooperative communication is evaluated as information transfer.** Mixed-motive work documents deception, but does not yet yield general, cost-sensitive receiver policies that decide when claims need independent verification.
4. **Independent votes are treated as independent evidence.** LLM debate work measures error propagation and aggregation, but source/model correlation is not normally an online decision variable for allocating verification effort.
5. **Network impairments are exogenous.** CAIC is an important 2026 exception for queueing congestion, but sender scheduling, receiver freshness, and task control are still not jointly solved under correlated failures and endogenous contention.
6. **Capabilities are either known, honestly reported, or mechanically observable.** Task-allocation and mechanism-design literatures each relax parts of this, but private, drifting, action-dependent capability without transferable payments remains thin.
7. **A mechanism knows the agents' response class.** Recent adaptive incentive work often assumes equilibrium response, no-regret learning, or a two-timescale model; algorithm-switching agents create a different robustness question.
8. **Trust changes after performance is observed, but allocation also controls which performance is observed.** This feedback creates self-confirming beliefs in mixed human–AI teams and is under-modeled.
9. **Offline team data are treated as adequate once return is good.** There is little diagnostic theory for whether a fixed multi-agent dataset can identify a policy robust to a shifted teammate population.
10. **Fairness is measured for a fixed roster.** Open systems study churn and fair MARL studies welfare, but continuity of obligations across arrivals/departures is not normally the object.

---

## Candidate B01

**Candidate ID:** B01  
**Research area:** Ad-hoc teamwork × non-stationary multi-agent learning  
**Precise research question:** How can an ad-hoc agent choose actions that both identify and coordinate with an unfamiliar teammate when that teammate is itself learning from those same actions, so that probing changes the object being identified?  
**Existing assumption:** Team-probing and teammate-modeling methods usually treat the teammate policy/type as fixed within the probing window; simultaneous-learning MARL models peer learning but not zero-shot identification of an independently designed partner.  
**Why the assumption matters:** A “diagnostic” action can teach, anchor, or deter an adaptive teammate. A posterior over a stationary type is then misspecified and can produce self-fulfilling convention lock-in.  
**Closest prior work:** [Learning to Coordinate With Different Teammates via Team Probing (TNNLS 2025)](https://ieeexplore.ieee.org/document/10988880); [Meta-MAPG (ICML 2021)](https://proceedings.mlr.press/v139/kim21g.html); [Fast Teammate Adaptation in the Presence of Sudden Policy Change](https://arxiv.org/abs/2305.05911); [N-Agent Ad Hoc Teamwork (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/cabf611498431ad89a85ace75f790d93-Paper-Conference.pdf).  
**What existing work does:** CDP separates a probing phase from adaptation for fixed latent coordination patterns; Meta-MAPG differentiates through peer learning; fast adaptation detects abrupt changes; POAM handles varying teammate number/type.  
**What remains unsolved:** A unified *dual-control* problem in which the ego agent maintains beliefs over both teammate policy and learning rule, values information, and accounts for its causal influence on future teammate updates.  
**Why it is genuinely multi-agent:** The uncertainty and system dynamics are generated by another decision-maker updating in response to the ego agent; replacing it with exogenous drift changes the problem.  
**Potential hypothesis:** Modeling the partner’s update rule and planning over belief–influence trade-offs reduces convention lock-in and dynamic regret compared with stationary-type probing or immediate best response.  
**Potential contribution:** A co-adaptive POSG/Bayesian game, an influence-aware belief update/planner, and identifiability or regret results for restricted learning-rule families.  
**Potential experiment:** Iterated matrix coordination, Overcooked, Level-Based Foraging, and Melting Pot with held-out Q-learners, policy-gradient learners, and human-like bounded learners; measure team return, identification calibration, partner-policy displacement, convention optimality, and recovery after partner update-rule switches.  
**Novelty confidence:** Medium–High.  
**AAMAS relevance:** Very high.  
**Feasibility:** High; public environments and small policies suffice.  
**Main risk:** “Influencing Towards Stable Multi-Agent Interactions” and teaching/leading AHT lineages may contain an equivalent formalization; the auditor must compare exact belief and learning-rule assumptions.

## Candidate B02

**Candidate ID:** B02  
**Research area:** Emergent communication × open systems  
**Precise research question:** Can independently trained agents maintain coordination by learning an online translation layer when both agents’ latent communication protocols continue to drift during deployment and neither exposes paired meanings or a shared grounding representation?  
**Existing assumption:** Cross-play, translation, and community-joining methods typically freeze at least one protocol, use offline interaction data, or align agents through a shared language/grounding space.  
**Why the assumption matters:** Real open teams update policies asynchronously. A translation learned at time (t) becomes stale, and both sides adapting to translation errors can create oscillation or semantic collapse.  
**Closest prior work:** [Learning Translations / CLAP (IJCAI 2024)](https://www.ijcai.org/proceedings/2024/0005); [Emergent Translation in Multi-Agent Communication](https://arxiv.org/abs/1710.06922); [Unsupervised Translation of Emergent Communication (AAAI 2025)](https://ojs.aaai.org/index.php/AAAI/article/view/34489); [LangGround (TMLR 2026)](https://openreview.net/pdf?id=LGsed0QQVq); [Emergent Linguistic Phenomena in Multi-Agent Communication Games](https://aclanthology.org/D19-1384/).  
**What existing work does:** CLAP learns a joiner’s translation from community interaction data; earlier work induces translation between protocols; LangGround aligns communication with human language; cross-play exposes incompatible idiolects.  
**What remains unsolved:** Stability and adaptation when *both* encoders/decoders change online, with no parallel corpus, shared natural language, or centralized gradient.  
**Why it is genuinely multi-agent:** Meaning is relational: it is identified only through another adaptive agent’s messages, actions, and outcomes.  
**Potential hypothesis:** Timescale-separated translation updates with change-point detection and cycle-consistency over task consequences can track co-drift below a calculable drift-rate threshold; naïve joint adaptation will exhibit phase transitions into semantic collapse.  
**Potential contribution:** A formal co-drifting signaling game, a tracking-regret/stability bound, and decentralized translation algorithm.  
**Potential experiment:** Referential games, cooperative navigation, Hanabi-like communication, and heterogeneous robot sensor/action abstractions; vary asynchronous update rates, architecture, population churn, message alphabets, and drift direction; measure cross-play return, semantic tracking error, recovery time, and oscillation.  
**Novelty confidence:** Medium–High.  
**AAMAS relevance:** High.  
**Feasibility:** High.  
**Main risk:** The formulation must not reduce to ordinary non-stationary domain adaptation; task-coupled co-adaptation and decentralized observability must be essential.

## Candidate B03

**Candidate ID:** B03  
**Research area:** Strategic communication × verification  
**Precise research question:** In a sequential mixed-motive game, how should a receiver learn *which messages to verify, ignore, or act on* when verification is costly, sender incentives and types are uncertain, and truthfulness can change over time?  
**Existing assumption:** Cooperative Comm-MARL optimizes informativeness; deception studies measure attacks or behavior; classical signaling/cheap-talk models usually assume known game structure and rational types.  
**Why the assumption matters:** Always trusting is exploitable and always verifying destroys the value of communication. Strategic adaptation makes static trust scores inadequate.  
**Closest prior work:** [Learning in public goods games: uncertainty and communication (2024)](https://link.springer.com/article/10.1007/s00521-024-10530-6); [Adversarial Cheap Talk (ICML 2023)](https://proceedings.mlr.press/v202/lu23h.html); [Should I Trust You? Detecting Deception in Negotiations (2025)](https://openreview.net/forum?id=KKEBFu9Tln); [Strategic Communication under Threat (AAMAS 2026 proceedings)](https://www.ifaamas.org/Proceedings/aamas2026/forms/contents.htm); [Even More Deception (2026)](https://arxiv.org/abs/2607.26120).  
**What existing work does:** Documents emergent deception under asymmetric uncertainty, adversarially manipulates cheap talk, detects deceptive Diplomacy proposals, and studies strategic revelation/concealment.  
**What remains unsolved:** A receiver-side sequential decision rule with explicit verification actions/costs, evolving sender types, and equilibrium/learning guarantees connecting communication, belief calibration, and task reward.  
**Why it is genuinely multi-agent:** Verification policy changes sender incentives and future messages; it is an endogenous signaling game, not single-agent fact checking.  
**Potential hypothesis:** Commitment to randomized, evidence-contingent audits can induce more truthful equilibria and higher welfare than learned trust alone at the same verification budget.  
**Potential contribution:** A verified cheap-talk Markov game; incentive-aware selective-audit algorithm; bounds on deception rate/welfare versus audit budget.  
**Potential experiment:** Repeated public-goods games, Diplomacy deal fragments, Chameleon/Among Us, and resource exchange with executable claims; compare no verification, full verification, confidence filtering, reputation, and Bayesian audit policies.  
**Novelty confidence:** High for the joint sequential formulation; Medium pending mechanism-design audit.  
**AAMAS relevance:** Very high.  
**Feasibility:** High.  
**Main risk:** Classical auditing and inspection games may already imply the core result; novelty must be in learning under partial observability and evolving strategic senders, not merely applying audits to LLMs.

## Candidate B04

**Candidate ID:** B04  
**Research area:** Collective intelligence × correlated error  
**Precise research question:** How should a multi-agent team allocate limited independent evidence-gathering actions when agents’ errors are correlated through shared models, sources, and previous messages, so that agreement is not mistaken for corroboration?  
**Existing assumption:** Debate/voting often aggregates agent outputs without a causal model of shared evidence lineage; diversity is usually induced by prompts or model choice rather than estimated and acted upon online.  
**Why the assumption matters:** Ten agents repeating one upstream error provide one piece of evidence, not ten. Communication itself changes dependence, invalidating static ensemble assumptions.  
**Closest prior work:** [Misinformation Propagation in Benign Multi-Agent Systems (2026)](https://arxiv.org/abs/2606.16710); [Should we be going MAD? (ICML 2024)](https://proceedings.mlr.press/v235/smit24a.html); [GUARDIAN (NeurIPS 2025)](https://proceedings.neurips.cc/paper_files/paper/2025/file/0bc795afae289ed465a65a3b4b1f4eb7-Paper-Conference.pdf); [Encouraging Divergent Thinking (EMNLP 2024)](https://aclanthology.org/2024.emnlp-main.992/).  
**What existing work does:** MINT measures benign misinformation persistence; MAD evaluations question universal gains; GUARDIAN defends collaboration graphs; divergent-thinking methods increase answer diversity.  
**What remains unsolved:** Online estimation of epistemic dependence from provenance/interventions and optimal routing of a finite verification budget to maximize information gain or decision accuracy.  
**Why it is genuinely multi-agent:** The dependence graph is created by agent-to-agent observation and aggregation; independent single-agent calls do not exhibit social amplification or correction cascades.  
**Potential hypothesis:** Verification selected by expected *conditional* information gain after discounting shared ancestry beats majority, confidence, and diversity-only routing, especially when the majority inherits one source.  
**Potential contribution:** A causal evidence graph, a budgeted verification policy, and a theorem relating effective independent evidence to error probability under bounded dependence.  
**Potential experiment:** Tool-using QA, diagnosis games, collaborative planning with hidden ground truth, and code-review teams; manipulate shared retrieval corpora, model family, message topology, and misinformation exposure; measure calibration, Brier score, error cascade size, utility per tool call, and recovery.  
**Novelty confidence:** Medium–High.  
**AAMAS relevance:** High.  
**Feasibility:** High with open models and deterministic evidence tools.  
**Main risk:** Could look like ensemble uncertainty estimation unless interaction-generated dependence and decentralized evidence acquisition are central.

## Candidate B05

**Candidate ID:** B05  
**Research area:** Communication-constrained MARL × endogenous networks  
**Precise research question:** Can agents jointly learn task control, message generation, and contention-aware transmission policies under correlated link failures, where each transmission changes queue delay and therefore the future value/staleness of everyone else’s messages?  
**Existing assumption:** Delay-aware methods generally use fixed/stochastic delays; asynchronous methods reduce messages; even CAIC’s shared queue does not model correlated failures and strategic cross-agent externalities in transmission scheduling as a decentralized game.  
**Why the assumption matters:** Under burst loss and shared channels, individually useful messages can cause congestion collapse; stale intent can be worse than silence.  
**Closest prior work:** [CAIC (UAI 2026)](https://proceedings.mlr.press/v337/li26h.html); [DACOM (AAAI 2023)](https://ojs.aaai.org/index.php/AAAI/article/view/26389); [AsynCoMARL (AAMAS 2025)](https://arxiv.org/abs/2502.00558); [IMAC (ICML 2020)](https://proceedings.mlr.press/v119/wang20i.html); [Multi-Agent Bandits through Heterogeneous Erasure Channels (AISTATS 2024)](https://proceedings.mlr.press/v238/hanna24a.html).  
**What existing work does:** CAIC explicitly models queueing and future-trajectory intent; DACOM handles delay; AsynCoMARL handles sparse asynchronous links; IMAC compresses/schedules messages; erasure-channel bandits provide regret results.  
**What remains unsolved:** Decentralized control of the coupled queue/failure/task system with agent-specific value-of-freshness, correlated outages, and transmission externalities.  
**Why it is genuinely multi-agent:** One agent’s communication action directly changes other agents’ delays and decisions.  
**Potential hypothesis:** Difference-reward or price-based congestion signals plus receiver-estimated age-of-information yield stable efficient equilibria and avoid message storms better than independent communication gates.  
**Potential contribution:** A communication-congestion Markov game, welfare/regret analysis, and decentralized pricing/scheduling algorithm.  
**Potential experiment:** SMAC/MPE plus ns-3-like queues, Multi-Agent Particle Environments, satellite coordination, and multi-robot exploration; vary burst correlation, topology, load, and agent count; metrics include reward, collision, bytes, AoI, queue stability, and worst-agent delay.  
**Novelty confidence:** Medium.  
**AAMAS relevance:** High.  
**Feasibility:** Medium–High.  
**Main risk:** CAIC is dangerously close; a paper must demonstrate that correlated failure and strategic externality change optimal policies/theory, not just add a network model.

## Candidate B06

**Candidate ID:** B06  
**Research area:** Heterogeneous task allocation × mechanism design  
**Precise research question:** How can a team allocate interdependent tasks when agents have private, drifting, action-dependent capabilities, can strategically under/overstate them, and side payments are unavailable?  
**Existing assumption:** Heterogeneous MRTA typically observes or estimates capability cooperatively; truthful allocation mechanisms use payments or fixed private types; degradation work treats capability change as physical state, not strategically reported information.  
**Why the assumption matters:** Self-reported competence is manipulable, while allocation outcomes are also the only observations revealing competence. Complementary tasks make free-riding and blame shifting profitable.  
**Closest prior work:** [Strategyproof RL for Online Resource Allocation (AAMAS 2020)](https://research.ibm.com/publications/strategyproof-reinforcement-learning-for-online-resource-allocation); [Incentive-Compatible Distributed Robotic Service Allocation (2024)](https://arxiv.org/abs/2403.10733); [Uncertainty-Aware MRTA with Coupled Rewards (2025)](https://arxiv.org/abs/2509.22469); [Consensus-Based Dynamic Task Allocation with Capability Decrease (2024)](https://arxiv.org/abs/2412.10087); [Online Capability-Based Task Allocation (2024)](https://doi.org/10.1007/s10846-024-02050-1).  
**What existing work does:** Provides payment-based truthfulness, uncertain-capability allocation, strongly coupled rewards, and replanning as physical capabilities decline.  
**What remains unsolved:** Payment-free repeated allocation that jointly learns capability, limits manipulation, and handles endogenous fatigue/depletion plus complementarities.  
**Why it is genuinely multi-agent:** Assignments couple agents’ workloads, observations, incentives, and future capacities; a single-agent scheduler cannot model strategic cross-reports or coalition complementarities.  
**Potential hypothesis:** Rotation/audit assignments and outcome-based reputation can make truthful capability revelation approximately incentive compatible while bounding welfare loss under slow drift.  
**Potential contribution:** A repeated Bayesian allocation game without transfers, approximate IC/welfare bounds, and exploration-aware allocator.  
**Potential experiment:** Heterogeneous multi-robot pickup/delivery, disaster response, or compute-agent scheduling with hidden skill/fatigue; scripted and learned misreporters; measure welfare, task failures, calibration, envy/workload, manipulation gain, and regret.  
**Novelty confidence:** Medium.  
**AAMAS relevance:** Very high.  
**Feasibility:** High in simulation.  
**Main risk:** Payment-free truthfulness may be impossible without strong repeated-game assumptions; an impossibility result could still be publishable.

## Candidate B07

**Candidate ID:** B07  
**Research area:** Learning × dynamic mechanism design  
**Precise research question:** Can a mechanism maintain welfare and incentive guarantees when participating agents use unknown learning algorithms and may switch algorithms strategically after detecting the mechanism’s adaptation?  
**Existing assumption:** Recent work commonly fixes the response class—best response, no-regret learner, or a known two-timescale adaptive dynamic.  
**Why the assumption matters:** A mechanism optimized against no-regret behavior can be gamed by an agent that temporarily mimics one learner and then switches; the designer’s observations are endogenous to prices/incentives.  
**Closest prior work:** [Learning Dynamic Mechanisms in Unknown Environments (JMLR 2024)](https://www.jmlr.org/papers/v25/23-0159.html); [Adaptive Incentive Design with Learning Agents (2024)](https://arxiv.org/abs/2405.16716); [Learning a Game by Paying the Agents (2025)](https://arxiv.org/abs/2503.01976); [No-Regret and Incentive-Compatible Online Learning (ICML 2020)](https://arxiv.org/abs/2002.08837); [RAID (2026)](https://arxiv.org/abs/2606.02529).  
**What existing work does:** Learns dynamic VCG mechanisms in unknown MDPs, uses two-timescale incentives, steers arbitrary no-regret learners, and provides regret/IC guarantees for specified response models.  
**What remains unsolved:** Robust mechanism learning over a set of response algorithms with endogenous switches, including detecting whether behavioral change is environmental, adaptive, or strategic.  
**Why it is genuinely multi-agent:** Guarantees concern strategic reactions of several learning agents to a common adaptive institution; no single-agent reduction preserves incentive interactions.  
**Potential hypothesis:** Mechanism randomization and response-class confidence sets can bound policy regret against piecewise-stationary learner classes, whereas deterministic adaptive mechanisms are exploitable.  
**Potential contribution:** Policy-regret solution concept for mechanism/learner co-adaptation, lower bounds, and robust adaptive mechanism.  
**Potential experiment:** Repeated auctions, congestion pricing, public goods, and resource allocation with Hedge, Q-learning, policy gradient, LLM, and strategic switchers.  
**Novelty confidence:** Medium.  
**AAMAS relevance:** Very high.  
**Feasibility:** Medium.  
**Main risk:** Theoretical scope can explode; restrict to one mechanism family and bounded-switch learner class.

## Candidate B08

**Candidate ID:** B08  
**Research area:** Human–agent teamwork × active trust calibration  
**Precise research question:** How should a mixed human–AI team allocate tasks to learn each member’s context-dependent capability when current trust determines allocation and allocation determines what performance evidence becomes observable?  
**Existing assumption:** Trust-calibration studies generally manipulate visible reliability/errors and observe reliance; task-allocation methods often treat capability estimates as exogenous or passively updated.  
**Why the assumption matters:** Under-allocation prevents a capable but distrusted agent from demonstrating competence, while over-allocation can hide human skill decay. These self-confirming beliefs can persist despite repeated interaction.  
**Closest prior work:** [Impact of Training on HAT Communication and Trust Calibration (Human Factors 2023)](https://journals.sagepub.com/doi/10.1177/00187208211047323); [Trust Repair in Human-Agent Teams (JAAMAS 2021)](https://link.springer.com/article/10.1007/s10458-021-09515-9); [Mutual Theory of Mind in Human-AI Collaboration (2024)](https://arxiv.org/abs/2409.08811); [Multilevel Trust in Multioperator–Multiagent Teams (2026)](https://doi.org/10.5406/19398298.139.1.07); [Guilty Until Proven Innocent (2026)](https://doi.org/10.1016/j.apergo.2026.104770).  
**What existing work does:** Shows trust/performance interdependence, studies failures and repair, evaluates team-level trust referents, and finds that experiencing imperfection changes monitoring and calibration.  
**What remains unsolved:** A sequential active-learning/allocation policy for multi-member teams that explicitly breaks self-confirming trust loops while limiting risk and workload.  
**Why it is genuinely multi-agent:** Each member holds beliefs about several others, communicates, delegates, and changes behavior under observed trust; team evidence and performance are jointly generated.  
**Potential hypothesis:** Safe “calibration assignments” chosen for information value reduce long-run calibration error and improve resilience more than transparency messages or performance-greedy allocation alone.  
**Potential contribution:** A Bayesian team model with endogenous observability, safe exploration algorithm, and human-subject validation.  
**Potential experiment:** 2 humans + 2 agents in collaborative block moving/search-and-rescue; controlled contextual competence shifts; measure task performance, calibration error, reliance, workload, communication, and recovery.  
**Novelty confidence:** Medium–High.  
**AAMAS relevance:** High.  
**Feasibility:** Medium because a human study is required for the strongest claim.  
**Main risk:** If evaluated only with simulated humans it will look artificial; preregistered human evidence is important.

## Candidate B09

**Candidate ID:** B09  
**Research area:** Offline MARL × ad-hoc teamwork  
**Precise research question:** Given a fixed dataset collected from several team compositions, when is robust coordination with a new teammate *identifiable*, and can an algorithm abstain or request online interaction when the necessary unilateral/joint coverage is absent?  
**Existing assumption:** Offline AHT papers demonstrate empirical generalization but rarely certify that the dataset distinguishes teammate-conditioned actions relevant under deployment shift.  
**Why the assumption matters:** High held-out return on a few teammate types can conceal observationally equivalent policies that diverge catastrophically with a new partner.  
**Closest prior work:** [TAGET: Offline Goal-Based Decision Transformers (ICML 2025)](https://proceedings.mlr.press/v267/zhang25h.html); [DiTAC (ECAI/AI Communications 2026)](https://journals.sagepub.com/doi/10.3233/FAIA251257); [Seldonian RL for AHT (RLC 2025)](https://rlj.cs.umass.edu/2025/papers/Paper223.html); [ComaDICE (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/hash/477d1531c260f9605bbf9d14d00952d4-Abstract-Conference.html); [Making Friends in the Dark (2023)](https://arxiv.org/abs/2310.01439).  
**What existing work does:** TAGET adapts returns/subgoals from offline data; DiTAC learns teamwork abstractions; Seldonian methods guarantee user-specified behaviors; ComaDICE controls stationary distribution shift; partial-observability work removes teammate-action/reward access.  
**What remains unsolved:** Coverage/identifiability conditions specific to teammate shifts, practical diagnostics, and a selective policy that knows when offline evidence cannot support coordination.  
**Why it is genuinely multi-agent:** Data support depends on coupled joint actions and teammate-conditioned transitions; single-policy coverage is insufficient when unilateral partner deviations change reachable states.  
**Potential hypothesis:** A teammate-conditional concentrability/ambiguity score predicts failure better than standard behavior-policy likelihood and enables calibrated abstention or minimal probing.  
**Potential contribution:** Impossibility result, sufficient coverage condition, estimator, and selective offline-to-online AHT algorithm.  
**Potential experiment:** LBF, Overcooked, Hanabi, and Predator–Prey datasets with deliberately confounded teammate populations; metrics include worst-partner return, coverage calibration, selective risk, and probes to safe adaptation.  
**Novelty confidence:** High.  
**AAMAS relevance:** Very high.  
**Feasibility:** High.  
**Main risk:** Formal coverage may be too pessimistic or hard to estimate in function approximation; tabular theorem plus scalable proxy is a credible scope.

## Candidate B10

**Candidate ID:** B10  
**Research area:** Fair MARL × open agent systems  
**Precise research question:** What fairness notion and learning rule preserve meaningful cumulative obligations when agents arrive, leave, or change roles, without allowing strategic churn to erase historical disadvantage?  
**Existing assumption:** Fair MARL normally fixes agent identities and optimizes expected returns; open-team MARL handles dynamic rosters but usually optimizes task performance, not intertemporal fairness.  
**Why the assumption matters:** Per-episode equality can be cumulatively unfair, and an agent can reset identity or time participation to exploit roster-normalized guarantees.  
**Closest prior work:** [Learning Fair Policies in Decentralized Cooperative MARL](https://arxiv.org/abs/2012.09421); [Achieving Fairness in Multi-Agent MDP (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/hash/473cb5596e2b84648753ce26484d79c8-Abstract-Conference.html); [Open-ended Coordination Using Modular Open Policies (JAAMAS 2025)](https://link.springer.com/article/10.1007/s10458-025-09723-7); [Long-Term Fairness with Unknown Dynamics (NeurIPS 2023)](https://arxiv.org/abs/2304.09362); [A General Incentives-Based Framework for Fairness (AAMAS 2026 proceedings)](https://www.ifaamas.org/Proceedings/aamas2026/forms/contents.htm).  
**What existing work does:** Optimizes generalized welfare for fixed teams, models long-term fairness in dynamic systems, and coordinates under agent/task openness.  
**What remains unsolved:** Identity/participation-aware fairness over a changing roster, together with learnability, efficiency, and manipulation resistance.  
**Why it is genuinely multi-agent:** Fairness is relational and histories overlap only partially; arrivals/departures alter feasible allocations and other agents’ claims.  
**Potential hypothesis:** Contribution- and exposure-normalized fairness with carry-over debt yields bounded cumulative envy/regret under non-strategic churn, while any anonymous resettable rule is manipulable.  
**Potential contribution:** Axioms/impossibility result, open-population fairness metric, and primal–dual MARL method.  
**Potential experiment:** Open Overcooked, dynamic ride/task allocation, and resource sharing; vary churn, identity resets, roles, and scarcity; measure welfare, cumulative envy/debt, worst-agent return, and manipulation gain.  
**Novelty confidence:** Medium–High.  
**AAMAS relevance:** Very high.  
**Feasibility:** High.  
**Main risk:** Identity persistence is a normative design choice; formal results should separate authenticated churn from cheap pseudonyms.

## Candidate B11

**Candidate ID:** B11  
**Research area:** Reputation × adaptive/forkable agents  
**Precise research question:** How much reputation should transfer when an autonomous agent is upgraded, fine-tuned, or forked, and can behavioral tests distinguish continuity from a strategically reputation-laundering successor?  
**Existing assumption:** Classical reputation attaches history to a stable identity; agentic identity systems attach credentials to an entity, but model/policy continuity is not guaranteed by credentials.  
**Why the assumption matters:** Zero transfer destroys useful reputation after benign updates; full transfer lets a changed or forked policy inherit trust it did not earn.  
**Closest prior work:** [Dissociative Identity: LM Agents Lack Grounding for Reputation Mechanisms (2026)](https://arxiv.org/abs/2605.30169); [A MARL Model of Reputation and Cooperation](https://arxiv.org/abs/2103.04982); [Cooperation and Reputation Dynamics with RL](https://arxiv.org/abs/2102.07523); [Addressing Concept Drift in Reputation Assessment](https://www.researchgate.net/publication/333868246_Addressing_Concept_Drift_in_Reputation_Assessment); [AgentReputation (2026)](https://borowiecki.dev/pdf/2605.00073).  
**What existing work does:** Shows identifiability is important for cooperation, models learning of reputation norms, adapts trust under drift, and recently attacks the grounding assumptions of LLM-agent reputation.  
**What remains unsolved:** A decision-theoretic transfer rule tied to measured task-conditional behavioral continuity, including fork correlation and strategic attempts to pass tests.  
**Why it is genuinely multi-agent:** Reputation affects partner selection, cooperation, and incentives across a population; successors can interact strategically to launder history.  
**Potential hypothesis:** Conservative transfer based on sequential challenge tests and correlated-fork discounting improves market welfare and deters laundering versus identity-only or reset rules.  
**Potential contribution:** Reputation-continuity game, impossibility/transfer bounds, and adversarial behavioral audit protocol.  
**Potential experiment:** Repeated exchange/public-goods marketplace with policy updates/forks; honest drift and strategic sleeper successors; measure trust calibration, cooperation, false transfer/reset, welfare, and laundering payoff.  
**Novelty confidence:** Medium–Low after the September 2026 identity papers; retain only as a plausible gap needing deeper audit.  
**AAMAS relevance:** High.  
**Feasibility:** High.  
**Main risk:** The very recent “Dissociative Identity” paper may already frame most of the scientific question; novelty may collapse to protocol engineering.

## Candidate B12

**Candidate ID:** B12  
**Research area:** Safe MARL × epistemic/communication uncertainty  
**Precise research question:** Can decentralized agents guarantee a joint chance constraint when no agent observes all risk variables and safety-relevant messages may be delayed, lost, or strategically misreported?  
**Existing assumption:** Safe MARL often assumes access to joint state/cost during training or reliable peer updates; communication-robust MARL usually optimizes reward rather than formal joint safety.  
**Why the assumption matters:** Local shields can each certify an action while their combination violates a coupled constraint; stale “safe” messages can invalidate guarantees.  
**Closest prior work:** [Multi-Agent Constrained Policy Optimisation](https://arxiv.org/abs/2110.02793); [Shield Decomposition for General Partially Observable Multi-Agent Environments (RLC 2024)](https://rlj.cs.umass.edu/2024/papers/Paper254.html); [Safe Dec-PG (AAAI 2021)](https://research.ibm.com/publications/decentralized-policy-gradient-descent-ascent-for-safe-multi-agent-reinforcement-learning); [Robust Constrained Markov Games (UAI 2026)](https://proceedings.mlr.press/v337/chang26a.html); [R3R decentralized infinite-horizon collision avoidance (2026)](https://dasc-lab.github.io/papers/2026/2026_r3r_decentralized_gatekeeper/).  
**What existing work does:** Handles constrained Markov games, decomposed shields under partial observability, decentralized coupled constraints, model uncertainty, and asynchronous collision avoidance in specific dynamics.  
**What remains unsolved:** General learning and guarantees for coupled chance constraints whose sufficient statistics are distributed and communicated unreliably or strategically.  
**Why it is genuinely multi-agent:** Safety depends on a joint action and distributed private risk observations; no agent can certify alone.  
**Potential hypothesis:** Set-valued risk messages with age/confidence bounds and a robust distributed shield can guarantee violation probability under bounded loss/delay, degrading gracefully to safe fallback.  
**Potential contribution:** Constrained POSG with epistemic message uncertainty, compositional safety theorem, and communication-aware shield.  
**Potential experiment:** Multi-robot intersection, drone separation, voltage control, and warehouse navigation; vary sensor blind spots, message delay/loss, benign faults, and misreporters; measure violations, return, conservatism, and communication.  
**Novelty confidence:** Medium.  
**AAMAS relevance:** High.  
**Feasibility:** Medium.  
**Main risk:** Formal guarantees may require assumptions so strong that the empirical contribution becomes narrow.

## Candidate B13

**Candidate ID:** B13  
**Research area:** Evaluation science × causal coordination  
**Precise research question:** Can we measure *coordination elasticity*—the causal dependence of team performance on partners’ responsive behavior—separately from common-cause correlation, individual competence, and brittle co-adaptation?  
**Existing assumption:** Team return and behavioral correlation are often used as coordination proxies; causal attribution work tends to explain an observed outcome, not quantify generalizable partner responsiveness under controlled replacements.  
**Why the assumption matters:** A shared policy can make agents look synchronized without interaction; a brittle convention can score highly in self-play while failing with minimally changed partners.  
**Closest prior work:** [Unified Game-Theoretic MARL / joint-policy correlation](https://arxiv.org/abs/1711.00832); [Evaluating Emergent Coordination through Causal Inference and Sub-Team Identification](https://ieeexplore.ieee.org/document/9996557/); [MACIE causal multi-agent explainer (2026)](https://doi.org/10.1007/s44163-026-01543-2); [Benchmarking MARL in Cooperative Tasks](https://arxiv.org/abs/2006.07869); [N-Agent Ad Hoc Teamwork](https://arxiv.org/abs/2404.10740).  
**What existing work does:** Measures joint-policy overfitting/correlation, uses causal inference for sub-team behavior, attributes outcomes with counterfactuals, and evaluates partner generalization.  
**What remains unsolved:** A task-normalized interventional measure with an explicit null for common causes, a responsiveness axis, and a brittleness/generalization axis that can compare architectures.  
**Why it is genuinely multi-agent:** The quantity is the causal effect of one agent’s policy response on another’s outcome; independent agents should score zero by construction.  
**Potential hypothesis:** Many high-return/self-play MARL and LLM-agent systems have low coordination elasticity or high brittleness; training on response-diverse partners raises elasticity and cross-play return.  
**Potential contribution:** Formal estimand, minimal intervention suite, estimator with confidence intervals, and scientific findings—not merely a leaderboard.  
**Potential experiment:** Matrix games with known ground truth, Overcooked, Hanabi, SMACv2, and tool-using LLM teams; partner replacements, action scrambling preserving marginals, delayed responses, and common-observation controls.  
**Novelty confidence:** Medium.  
**AAMAS relevance:** High.  
**Feasibility:** High.  
**Main risk:** Reviewer may call it “just another metric”; it needs identifiability theory and a substantive finding that reverses conclusions from standard evaluation.

## Candidate B14

**Candidate ID:** B14  
**Research area:** Coalition formation × repeated negotiation  
**Precise research question:** How do learning agents negotiate and form coalitions when outside options are endogenous to other simultaneous negotiations, and today’s disclosure changes tomorrow’s partner set and bargaining power?  
**Existing assumption:** Automated bargaining is often dyadic or uses fixed outside options; coalition learning often abstracts away natural-language/strategic disclosure and interdependent concurrent bargains.  
**Why the assumption matters:** Accepting, delaying, or revealing in one negotiation changes feasible coalitions and reservation values elsewhere, creating option-value and reputation externalities.  
**Closest prior work:** [Dynamic Coalition Structure Detection (AAMAS 2025)](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1227.pdf); [Decentralized Online Learning by Selfish Agents in Coalition Formation (IJCAI 2025)](https://www.ijcai.org/proceedings/2025/0422.pdf); [Dynamic Outside Options and Optimal Negotiation Strategies (AER 2024)](https://www.aeaweb.org/articles?id=10.1257/aer.20230015); [When LLM Agents Negotiate: Private Information and Dynamic Bargaining (2026)](https://arxiv.org/abs/2608.07538); [Cooperate to Compete (2026)](https://arxiv.org/abs/2604.25088).  
**What existing work does:** Detects shifting Diplomacy coalitions, learns coalitions from repeated interactions, solves bilateral bargaining with dynamic outside options, benchmarks private-information LLM bargaining, and provides multi-party negotiated environments.  
**What remains unsolved:** A formal and learnable multi-negotiation process where outside options are endogenously created/destroyed by coalition offers and disclosure affects future matching.  
**Why it is genuinely multi-agent:** Values and feasible agreements depend on at least three agents and simultaneous partner alternatives; the phenomenon vanishes in a dyad.  
**Potential hypothesis:** Myopic agreement maximization produces inefficient early lock-in; option-aware policies that price information/reputation externalities improve long-run welfare but may reduce immediate agreement rate.  
**Potential contribution:** Stochastic coalition-bargaining game, equilibrium/inefficiency analysis, and learning algorithm for coupled negotiations.  
**Potential experiment:** Structured 4–8-agent coalition games, Diplomacy-derived bargaining, supply-network formation; vary private values, deadlines, re-entry, and communication; metrics include welfare, stability, delay, regret, deception, and coalition churn.  
**Novelty confidence:** Medium.  
**AAMAS relevance:** Very high.  
**Feasibility:** Medium–High.  
**Main risk:** Broadness; start with structured offers and verifiable actions, not unrestricted LLM dialogue.

## Candidate B15

**Candidate ID:** B15  
**Research area:** Multi-agent memory × belief revision  
**Precise research question:** When an agent retracts or corrects a claim that has already been summarized, combined, and used by other agents to derive new beliefs, how can a decentralized team identify and repair the affected descendants without globally replaying all histories?  
**Existing assumption:** Recent memory-security work focuses on blocking or authenticating poisoned writes; shared-memory access-control work tracks provenance, but semantic dependency after lossy summarization and downstream derivation is not generally maintained.  
**Why the assumption matters:** Deleting the original false note does not retract plans, summaries, or reputations derived from it. Honest corrections can arrive long after belief propagation.  
**Closest prior work:** [Memory Poisoning and Secure Multi-Agent Systems (2026)](https://arxiv.org/abs/2603.20357); [Securing LLM-Agent Long-Term Memory Against Poisoning (2026)](https://arxiv.org/abs/2606.24322); [Collaborative Memory (ICLR 2026)](https://openreview.net/pdf?id=pJUQ5YA98Z); [Misinformation Propagation in Benign MAS](https://arxiv.org/abs/2606.16710); [Robustness of Epistemic Gossip Protocols Against Data Loss (AAMAS 2025 listing)](https://aamas2025.org/index.php/conference/program/accepted-papers/).  
**What existing work does:** Characterizes poisoning, proves origin-binding defenses, adds access/provenance controls, measures benign misinformation spread, and studies epistemic gossip robustness.  
**What remains unsolved:** Incremental semantic truth maintenance across agent-local memories after non-invertible summaries, conflicting evidence, and partial connectivity, with bounded repair cost and explicit uncertainty.  
**Why it is genuinely multi-agent:** Different agents own derived beliefs and may be offline or distrust the correction; dependency and repair propagate through interaction topology.  
**Potential hypothesis:** Compact justification certificates attached to memory transformations enable targeted retraction with far lower replay cost and less residual error than source tags or deletion alone.  
**Potential contribution:** Formal distributed belief-dependency model, lower bound on provenance required for sound retraction, and repair protocol.  
**Potential experiment:** Long-horizon collaborative investigation/planning with seeded honest errors and delayed corrections; 3–20 open LLMs or symbolic-neural agents; measure residual false-belief rate, repair precision/recall, task recovery, communication, and replay cost.  
**Novelty confidence:** Medium–High.  
**AAMAS relevance:** High.  
**Feasibility:** High.  
**Main risk:** Must remain a scientific belief-revision problem rather than distributed-systems bookkeeping; symbolic baselines and soundness definitions are essential.

## Candidate B16

**Candidate ID:** B16  
**Research area:** Privacy × repeated multi-agent communication  
**Precise research question:** How can agents allocate and compose privacy budgets over long-horizon, adaptive, many-to-many communication when recipients collude and messages useful for coordination become more revealing when combined with others’ observations?  
**Existing assumption:** Privacy-preserving MARL often gives per-sender or per-protocol DP guarantees under cooperative recipients and fixed communication patterns; empirical leakage work measures but does not optimize adaptive coalition inference.  
**Why the assumption matters:** Individually private messages can jointly reveal a latent state; team topology and task actions provide side information, and privacy loss compounds across repeated interactions.  
**Closest prior work:** [DPMAC (IJCAI 2023)](https://www.ijcai.org/proceedings/2023/0516.pdf); [Privacy-Preserving Decentralized Actor-Critic (AISTATS 2024)](https://proceedings.mlr.press/v238/ahmed24a.html); [Differential Privacy in Cooperative Multiagent Planning](https://arxiv.org/abs/2301.08811); [Quantifying Privacy Leakage in Multi-Agent LLMs (BigData 2025)](https://doi.org/10.1109/BigData66926.2025.11401523); [Privacy Preserving Multi Agent Path Finding (AAMAS 2026 proceedings)](https://www.ifaamas.org/Proceedings/aamas2026/forms/contents.htm).  
**What existing work does:** Learns DP message senders, restricts shared information, provides private planning policies, quantifies LLM inter-agent leakage, and studies privacy in specific planning domains.  
**What remains unsolved:** Task-aware privacy accounting and communication control robust to adaptive colluding recipient coalitions and interaction-derived side information.  
**Why it is genuinely multi-agent:** Privacy loss and utility arise from who communicates with whom and what other agents jointly infer; a single recipient cannot reproduce coalition leakage.  
**Potential hypothesis:** Coalition-aware privacy filters using conditional mutual-information upper bounds can maintain task utility at a fixed worst-coalition leakage budget better than per-message DP noise.  
**Potential contribution:** Repeated private POSG, coalition leakage metric/composition result, and topology-aware communication policy.  
**Potential experiment:** Cooperative navigation with private goals, distributed diagnosis, and negotiation; 3–12 agents, varying coalitions/side information; compare DPMAC, local DP, secure aggregation, and no communication on return, empirical inference gain, RDP/MI bounds, and fairness.  
**Novelty confidence:** Medium.  
**AAMAS relevance:** High.  
**Feasibility:** Medium–High.  
**Main risk:** Differential-privacy composition and collusion are mature topics; novelty requires task-coupled adaptive topology and decisions, not relabeling standard DP.

---

## Gap-hunter triage (not the final team ranking)

**Strongest to send forward:** B01, B02, B03, B04, B09, B10, B15. These have a precise interaction effect, direct falsification route, and no exact match found in the September 2026 search.  
**Promising but needs a sharper novelty audit:** B05, B06, B07, B08, B12, B13, B14, B16.  
**Likely kill unless differentiated from the newest paper:** B11.

## Search casualties — apparent gaps invalidated during this pass

- **“Queue-aware multi-agent communication.”** Rejected as stated: CAIC (UAI 2026) directly models a shared queue, state-dependent service, stale messages, and congestion-aware sending.
- **“Adaptive reasoning depth / Theory of Mind.”** Rejected: *Adaptive Theory of Mind for LLM-based Multi-Agent Coordination* (AAAI 2026) explicitly adapts ToM order and studies order mismatch.
- **“Offline ad-hoc teamwork with unseen teammates.”** Rejected as a generic gap: TAGET (ICML 2025), DiTAC (2026), and Seldonian AHT already occupy it. B09 survives only as an identifiability/coverage question.
- **“Memory poisoning in multi-agent systems.”** Rejected as generic: several 2026 papers address attacks, provenance, and certified defense. B15 survives only because correction of downstream derived beliefs is different.
- **“Communication between merged populations.”** Rejected: a 2025 paper is titled *Emergent Communication in Merging Artificial Agent Populations*; CLAP and convention-reliant MARL are also close.
- **“Heterogeneous zero-shot MARL.”** Rejected: SHPPO and multiple 2025 heterogeneous-policy papers address dynamic scale/roles.
- **“Strategic communication/deception in LLM teams.”** Rejected as a broad idea: multiple 2025–2026 studies do exactly this. B03 requires costly selective verification and endogenous incentive effects.
- **“Causal multi-agent credit assignment.”** Rejected: 2024 model-based counterfactual work and several 2026 counterfactual/Shapley papers make this crowded.

## Unique-paper ledger (58 records)

Count rule: each title is counted once even if arXiv and proceedings pages were both inspected. Proceedings tables of contents are not counted as papers.

1. Kim et al., **A Policy Gradient Algorithm for Learning to Learn in MARL (Meta-MAPG)**, ICML 2021 — https://proceedings.mlr.press/v139/kim21g.html
2. Li et al., **Learning to Coordinate With Different Teammates via Team Probing**, TNNLS 2025 — https://ieeexplore.ieee.org/document/10988880
3. Nekoei et al., **Fast Teammate Adaptation in the Presence of Sudden Policy Change**, 2023 — https://arxiv.org/abs/2305.05911
4. Rahman et al., **N-Agent Ad Hoc Teamwork**, NeurIPS 2024 — https://arxiv.org/abs/2404.10740
5. Cope & McBurney, **Learning Translations**, IJCAI 2024 — https://www.ijcai.org/proceedings/2024/0005
6. Cao et al., **Emergent Translation in Multi-Agent Communication**, 2017 — https://arxiv.org/abs/1710.06922
7. **Unsupervised Translation of Emergent Communication**, AAAI 2025 — https://ojs.aaai.org/index.php/AAAI/article/view/34489
8. **LangGround**, TMLR 2026 — https://openreview.net/pdf?id=LGsed0QQVq
9. Chaabouni et al., **Emergent Linguistic Phenomena in Multi-Agent Communication Games**, EMNLP-IJCNLP 2019 — https://aclanthology.org/D19-1384/
10. Lo et al., **Cheap Talk Discovery and Utilization in MARL**, 2023 — https://arxiv.org/abs/2303.10733
11. Lu et al., **Adversarial Cheap Talk**, ICML 2023 — https://proceedings.mlr.press/v202/lu23h.html
12. Anastassacos et al., **Learning in Public Goods Games: Effects of Uncertainty and Communication**, 2024 — https://link.springer.com/article/10.1007/s00521-024-10530-6
13. Wongkamjan et al., **Should I Trust You? Detecting Deception in Negotiations**, 2025 — https://openreview.net/forum?id=KKEBFu9Tln
14. Buscemi et al., **Strategic Communication and Language Bias in Multi-Agent LLM Coordination**, 2025 — https://arxiv.org/abs/2508.00032
15. **Even More Deception: Objective Misalignment in Mixed-Motive LLM MAS**, 2026 — https://arxiv.org/abs/2607.26120
16. Becker et al., **Misinformation Propagation in Benign Multi-Agent Systems**, 2026 — https://arxiv.org/abs/2606.16710
17. Smit et al., **Should We Be Going MAD?**, ICML 2024 — https://proceedings.mlr.press/v235/smit24a.html
18. **GUARDIAN: Safeguarding LLM Multi-Agent Systems**, NeurIPS 2025 — https://proceedings.neurips.cc/paper_files/paper/2025/file/0bc795afae289ed465a65a3b4b1f4eb7-Paper-Conference.pdf
19. Liang et al., **Encouraging Divergent Thinking Through Multi-Agent Debate**, EMNLP 2024 — https://aclanthology.org/2024.emnlp-main.992/
20. Li et al., **CAIC**, UAI 2026 — https://proceedings.mlr.press/v337/li26h.html
21. Yuan et al., **DACOM**, AAAI 2023 — https://ojs.aaai.org/index.php/AAAI/article/view/26389
22. Dolan et al., **Asynchronous Cooperative MARL with Limited Communication**, AAMAS 2025 — https://arxiv.org/abs/2502.00558
23. Wang et al., **Learning Efficient Multi-Agent Communication: Information Bottleneck**, ICML 2020 — https://proceedings.mlr.press/v119/wang20i.html
24. Hanna et al., **Multi-Agent Bandit Learning through Heterogeneous Action Erasure Channels**, AISTATS 2024 — https://proceedings.mlr.press/v238/hanna24a.html
25. Stein et al., **Strategyproof RL for Online Resource Allocation**, AAMAS 2020 — https://research.ibm.com/publications/strategyproof-reinforcement-learning-for-online-resource-allocation
26. Zhao & Zhu, **Incentive-Compatible and Distributed Allocation for Robotic Service Provision**, 2024 — https://arxiv.org/abs/2403.10733
27. Rossano et al., **Uncertainty-Aware MRTA with Strongly Coupled Inter-Robot Rewards**, 2025 — https://arxiv.org/abs/2509.22469
28. **Consensus-Based Dynamic Task Allocation Considering Payload Consumption**, 2024 — https://arxiv.org/abs/2412.10087
29. **Online Capability Based Task Allocation of Cooperative Manipulators**, 2024 — https://doi.org/10.1007/s10846-024-02050-1
30. Lyu et al., **Learning Dynamic Mechanisms in Unknown Environments**, JMLR 2024 — https://www.jmlr.org/papers/v25/23-0159.html
31. **Adaptive Incentive Design with Learning Agents**, 2024 — https://arxiv.org/abs/2405.16716
32. **Learning a Game by Paying the Agents**, 2025 — https://arxiv.org/abs/2503.01976
33. Freeman et al., **No-Regret and Incentive-Compatible Online Learning**, ICML 2020 — https://arxiv.org/abs/2002.08837
34. **A No-Regret Framework for Adaptive Incentive Design**, 2026 — https://arxiv.org/abs/2606.02529
35. Johnson et al., **Impact of Training on HAT Communications and Trust Calibration**, Human Factors 2023 — https://journals.sagepub.com/doi/10.1177/00187208211047323
36. de Visser et al., **Trust Repair in Human-Agent Teams**, JAAMAS 2021 — https://link.springer.com/article/10.1007/s10458-021-09515-9
37. **Mutual Theory of Mind in Human-AI Collaboration**, 2024 — https://arxiv.org/abs/2409.08811
38. **Multilevel, Multireferent Trust in Human-Agent Teams**, 2026 — https://doi.org/10.5406/19398298.139.1.07
39. **Guilty Until Proven Innocent**, 2026 — https://doi.org/10.1016/j.apergo.2026.104770
40. Zhang et al., **TAGET**, ICML 2025 — https://proceedings.mlr.press/v267/zhang25h.html
41. **DiTAC**, 2026 — https://journals.sagepub.com/doi/10.3233/FAIA251257
42. Zorzi et al., **Seldonian RL for Ad Hoc Teamwork**, RLC 2025 — https://rlj.cs.umass.edu/2025/papers/Paper223.html
43. **ComaDICE**, ICLR 2025 — https://proceedings.iclr.cc/paper_files/paper/2025/hash/477d1531c260f9605bbf9d14d00952d4-Abstract-Conference.html
44. **Making Friends in the Dark**, 2023 — https://arxiv.org/abs/2310.01439
45. Jiang & Lu, **Learning Fair Policies in Decentralized Cooperative MARL**, 2020 — https://arxiv.org/abs/2012.09421
46. **Achieving Fairness in Multi-Agent MDP**, ICLR 2024 — https://proceedings.iclr.cc/paper_files/paper/2024/hash/473cb5596e2b84648753ce26484d79c8-Abstract-Conference.html
47. **Open-ended Coordination for MAS Using Modular Open Policies**, JAAMAS 2025 — https://link.springer.com/article/10.1007/s10458-025-09723-7
48. **Long-Term Fairness with Unknown Dynamics**, NeurIPS 2023 — https://arxiv.org/abs/2304.09362
49. La Malfa et al., **Dissociative Identity**, 2026 — https://arxiv.org/abs/2605.30169
50. McKee et al., **A MARL Model of Reputation and Cooperation in Human Groups**, 2021 — https://arxiv.org/abs/2103.04982
51. Anastassacos et al., **Cooperation and Reputation Dynamics with RL**, 2021 — https://arxiv.org/abs/2102.07523
52. Gu et al., **Multi-Agent Constrained Policy Optimisation**, 2021 — https://arxiv.org/abs/2110.02793
53. **Shield Decomposition for General Partially Observable Multi-Agent Environments**, RLC 2024 — https://rlj.cs.umass.edu/2024/papers/Paper254.html
54. Chang et al., **Robust Constrained Markov Games**, UAI 2026 — https://proceedings.mlr.press/v337/chang26a.html
55. Lanctot et al., **A Unified Game-Theoretic Approach to MARL**, 2017 — https://arxiv.org/abs/1711.00832
56. **Evaluating Emergent Coordination through Causal Inference and Sub-Team Identification**, 2022 — https://ieeexplore.ieee.org/document/9996557/
57. **Dynamic Coalition Structure Detection in Natural Language Interactions**, AAMAS 2025 — https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1227.pdf
58. Liu & Agmon, **Decentralized Online Learning by Selfish Agents in Coalition Formation**, IJCAI 2025 — https://www.ijcai.org/proceedings/2025/0422.pdf

## Evidence-calibration note

- The ledger is a **gap-hunter evidence set**, not a systematic-review corpus. Search-engine indexing is uneven, especially for August–September 2026 and workshop papers.
- B03, B06, B07, B10, and B14 require an older game-theory audit because equivalent questions may use inspection games, dynamic contracts, repeated mechanism design, or stochastic coalition formation terminology.
- B11 is intentionally marked low-confidence because two papers from May/September 2026 directly attack reputation without persistent identity.
- The strongest “verified enough to investigate deeply” gaps from this pass are B01, B02, B04, B09, B10, and B15. None should yet be described as “first.”
