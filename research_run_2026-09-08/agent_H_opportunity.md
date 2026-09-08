# Agent H — Research Opportunity Mining at Mature-Area Intersections

**Search date:** 8 September 2026  
**Role:** independent opportunity miner; this report does not use other agents' outputs.  
**Evidence base:** 54 distinct research records in the ledger below, including older mechanism-design, game-theory, ad-hoc-teamwork, and reputation terminology as well as 2025–2026 AAMAS and adjacent work. The `ai-agent-papers` repository was used only as a discovery aid: its own README describes a selective LLM-agent collection, so absence from it is not treated as evidence of novelty.

## Claim calibration

- **Verified missing formulation in this comparison set** means I found no direct formulation after exact, synonymous, older-term, and 2025–2026 searches. It is not a claim that the entire literature contains no such paper.
- **Plausible gap requiring further verification** means the interaction effect is not directly handled by the closest papers, but a citation-chain audit may uncover an equivalent formulation.
- **Rejected / already addressed** means a seemingly attractive intersection collapses into recent or older work, or remains only a generic combination.

The most defensible opportunities are not topic pairs. They have a mechanism that makes the intersection non-separable: an agent can manipulate the communication allocator; a designer can itself be strategically taught; observations confound environmental drift with opponent adaptation; coalition-level outcomes confound evolving private capabilities; or reputation prevents the very interactions needed to verify improvement.

## Candidate gaps

### H01 — Manipulation-resistant allocation of scarce communication

**Candidate ID:** H01  
**Research area:** communication × strategic behavior × mechanism design  
**Precise research question:** How can a bandwidth allocator assign speaking opportunities in a sequential partially observable mixed-motive game when message value is state-, receiver-, and continuation-policy-dependent, and agents can strategically manipulate both bids and the learned value estimator?  
**Existing assumption:** Recent learned communication auctions treat predicted contribution or value density as a trustworthy scheduling signal in common-payoff reasoning tasks; classic auction mechanisms with interdependent values assume verifiable realized outcomes and monetary transfers.  
**Why the assumption matters:** A manipulator can overstate urgency, monopolize airtime, suppress rivals' information, or send messages whose apparent marginal value is created by its own subsequent behavior.  
**Closest prior work:** [DALA / Cost-Effective Communication (AAAI 2026)](https://doi.org/10.1609/aaai.v40i35.40182); [Handling Interdependent Values in an Auction Mechanism for Bandwidth Allocation (2007)](https://insights.sei.cmu.edu/library/handling-interdependent-values-in-an-auction-mechanism-for-bandwidth-allocation-in-tactical-data-networks/); [Communication and Efficiency in Auctions (2012)](https://www.sciencedirect.com/science/article/pii/S089982561100176X).  
**What existing work does:** DALA centrally auctions scarce language-agent turns using predicted value density; the 2007 mechanism elicits private data quality with outcome-contingent transfers; communication-complexity work studies efficient auction outcomes under restricted messages.  
**What remains unsolved:** Incentive compatibility when marginal message value is delayed, endogenous to several agents' continuation policies, only partially observed, and transfers may be unavailable.  
**Why it is genuinely multi-agent:** Both the resource conflict and the strategic value of a message arise from receivers' and rivals' adaptive policies; independent single-agent calls cannot express airtime capture.  
**Potential hypothesis:** Randomized audit slots plus outcome-conditioned peer prediction and influence-capped bids will reduce welfare loss and airtime concentration against strategic senders relative to DALA-style value gating, without materially hurting cooperative efficiency.  
**Potential contribution:** A dynamic mechanism formulation, an impossibility result without audits or transfers, and a manipulation-resistant learned scheduler.  
**Potential experiment:** 4–16 agents in bandwidth-limited mixed-motive grid rescue, Overcooked-with-private-side-goals, and a hidden-role dialogue game; compare learned gates, DALA, round robin, VCG-like outcome payment, and no communication. Measure welfare, incentive regret, bandwidth, Jain airtime fairness, exploitability, and truthful-report deviation gain.  
**Novelty confidence:** Medium-high — **plausible gap requiring further verification**.  
**AAMAS relevance:** High.  
**Feasibility:** Medium-high; small neural policies and symbolic messages are sufficient.  
**Main risk:** Dynamic mechanism-design or network-auction work may contain an equivalent outcome-audited construction under different terminology.

### H02 — Causal attribution of multi-agent non-stationarity

**Candidate ID:** H02  
**Research area:** opponent modelling × causal inference × non-stationary learning  
**Precise research question:** From local interaction histories, can an agent distinguish (i) exogenous environment drift, (ii) an independently learning opponent or teammate, and (iii) an agent strategically adapting in response to the learner, and then select tracking, robust control, or shaping accordingly?  
**Existing assumption:** World-model and opponent-model methods generally optimize total predictive accuracy and label policy change as “non-stationarity,” without identifying its causal source.  
**Why the assumption matters:** The correct response is source-dependent: tracking a weather shock, robustifying against an independent learner, and attempting to shape a responsive opponent are not interchangeable. Observationally similar trajectories can require opposite interventions.  
**Closest prior work:** [LeMOL (2020)](https://arxiv.org/abs/2006.03923); [MBOM (2021)](https://arxiv.org/abs/2108.01843); [Applying Opponent and Environment Modelling to Enhance MARL (2025)](https://doi.org/10.1016/j.cogsys.2024.101306); [SOM: Structured Opponent Modeling (2026)](https://arxiv.org/abs/2605.07301); [ShapeLLM (2025/ICLR 2026)](https://arxiv.org/abs/2510.08255).  
**What existing work does:** It infers latent opponent policy, jointly predicts world and opponent behavior, learns structural causal opponent models, or explicitly shapes opponents.  
**What remains unsolved:** Identifiability and decision rules when the same local observation distribution can be generated by external drift, independent adaptation, or adaptation caused by ego's interventions.  
**Why it is genuinely multi-agent:** The third source is relational: another policy changes because of the focal agent's policy. It has no single-agent reduction to an exogenous non-stationary MDP.  
**Potential hypothesis:** A causal latent model trained with sparse safe interventions can identify the source class and achieve lower dynamic regret than joint predictive models on matched observational distributions.  
**Potential contribution:** A causally factored non-stationary Markov-game model; an observational non-identifiability theorem; an intervention-budgeted attribution-and-control algorithm.  
**Potential experiment:** Factorial generator crossing fixed/drifting environment dynamics with fixed, independently adapting, and ego-responsive opponents in matrix games, MPE, Overcooked, and SMAC-lite. Metrics: source-classification accuracy, interventional prediction, dynamic regret, exploitability, welfare, and harmful-shaping rate.  
**Novelty confidence:** High within the inspected comparison set — **verified missing formulation in this comparison set**.  
**AAMAS relevance:** Very high.  
**Feasibility:** High; the crucial experiments can use small controlled games.  
**Main risk:** Causal multi-agent influence or non-stationary system-identification work outside standard MARL vocabulary may already formalize the decomposition.

### H03 — Strategic teaching of an adaptive mechanism designer

**Candidate ID:** H03  
**Research area:** learning × mechanism design × opponent shaping  
**Precise research question:** Can an online mechanism designer learn taxes, transfers, or reward-sharing rules from behavior without participants strategically “teaching” the update rule toward a favorable future mechanism?  
**Existing assumption:** Deep mechanism-design pipelines acknowledge co-learning non-stationarity but usually train agents to best respond to a designer, not to manipulate the designer's learning dynamics as a long-horizon action channel.  
**Why the assumption matters:** A participant may sacrifice current utility to bias inferred preferences, eligibility, or elasticities, making apparently convergent online design incentive-incompatible.  
**Closest prior work:** [Deep Mechanism Design survey/experiments (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12207456/); [Microeconomic Foundations of Multi-Agent Learning (2026)](https://arxiv.org/abs/2601.03451); [Adaptive Reward Sharing (2025)](https://openreview.net/pdf?id=NVGrTKTGhe); [Multi-Timescale MARL (2023)](https://proceedings.mlr.press/v232/nekoei23a.html); [ShapeLLM (2026)](https://openreview.net/pdf?id=yJoHTqUNry).  
**What existing work does:** It studies bilevel or alternating designer–agent learning, regret in principal–agent MDPs, adaptive reward sharing, timescale separation, and opponent shaping.  
**What remains unsolved:** A mechanism update robust to deliberate participant influence on the designer's future parameters, especially with heterogeneous learning rates and entry/exit.  
**Why it is genuinely multi-agent:** Manipulation works through another learning agent—the designer—and affects all participants' future incentives.  
**Potential hypothesis:** Holdout audit rounds, randomized policy perturbations, and influence-bounded mechanism updates can bound strategic teaching gain while retaining sublinear welfare regret.  
**Potential contribution:** “Designer-shaping regret,” an impossibility result for fully predictable on-policy updates, and a robust online mechanism algorithm.  
**Potential experiment:** Repeated public goods, tax games, auctions, and Commons Harvest with one designer and 4–20 no-regret/RL participants; adversaries optimize long-horizon utility against the update rule. Measure welfare regret, designer-shaping gain, cycling, incentive violations, and adaptation speed.  
**Novelty confidence:** Medium-high — **plausible gap requiring further verification**.  
**AAMAS relevance:** Very high.  
**Feasibility:** High in small games; medium for deep MARL.  
**Main risk:** Recent principal–agent learning theory may subsume strategic teaching once policies condition on the full history.

### H04 — Repeated allocation with strategic, evolving capability and coalition-only feedback

**Candidate ID:** H04  
**Research area:** heterogeneity × task allocation × execution uncertainty × incentives  
**Precise research question:** How should repeated tasks be allocated when agents privately know capabilities that evolve through learning or fatigue, can misreport or withhold effort, and the allocator observes only the success of the assigned coalition rather than individual contributions?  
**Existing assumption:** Execution-uncertainty mechanisms often assume fixed types or verifiable individual completion; adaptive robot task allocation assumes cooperative truthful agents; coalition rewards make individual reliability statistically confounded.  
**Why the assumption matters:** The allocator must simultaneously explore capabilities, exploit complementarities, identify failure causes, and deter strategic under-performance.  
**Closest prior work:** [Mechanism Design with Execution Uncertainty (2013)](https://arxiv.org/abs/1301.0595); [Fault-Tolerant General-Purpose Task Allocation (AAMAS 2016)](https://eprints.soton.ac.uk/388365/); [Adaptive Task Allocation with Unknown/Evolving Capabilities (2020)](https://arxiv.org/abs/2003.03344); [Online Allocation with Strategic Agents (2022)](https://arxiv.org/abs/2209.12112); [CASH (CoRL 2025)](https://proceedings.mlr.press/v305/fu25a.html); [Uncertainty-Aware Coupled Rewards (2025)](https://arxiv.org/abs/2509.22469).  
**What existing work does:** It designs mechanisms for uncertain execution, maintains trust, learns robot capabilities, studies strategic online allocation, or coordinates heterogeneous skills.  
**What remains unsolved:** The joint problem of dynamic private capability, complementary coalitions, strategic effort/reporting, and only coalition-level delayed outcomes.  
**Why it is genuinely multi-agent:** Complementarity and coalition-only feedback make each agent's capability unidentifiable without varying teammates; incentives depend on alternative team compositions.  
**Potential hypothesis:** Randomized diagnostic coalitions plus causal coalition credit and delayed capability-contingent transfers can obtain sublinear allocation regret and bounded profitable misreporting.  
**Potential contribution:** A dynamic coalition-bandit mechanism, identifiability conditions, regret/incentive bounds, and an execution benchmark.  
**Potential experiment:** 5–30 heterogeneous agents in synthetic complementary-skill tasks and a public multi-robot simulator; impose learning, fatigue, and effort withholding. Compare UCB allocation, truthful adaptive MRTA, execution-uncertainty mechanisms, Shapley credit, and oracle. Metrics: task welfare, allocation regret, capability estimation, incentive regret, failure attribution, and fairness.  
**Novelty confidence:** Medium-high — **plausible gap requiring further verification**.  
**AAMAS relevance:** Very high.  
**Feasibility:** High for simulator/theory; no large models required.  
**Main risk:** The full formulation may become too broad; a paper should fix one evolution model and one transfer setting.

### H05 — Pivotal-skill extortion in long-lived heterogeneous teams

**Candidate ID:** H05  
**Research area:** heterogeneous cooperation × bargaining × dynamic team formation  
**Precise research question:** When a specialist's non-substitutable skill makes it pivotal to team success, when will a learning agent withhold effort or demand surplus, and what allocation/reward rule preserves participation and long-run efficiency as capabilities change?  
**Existing assumption:** Cooperative heterogeneous MARL typically assumes shared reward; coalition-formation and bargaining work often ends at team formation rather than modelling costly execution, learning, and fatigue.  
**Why the assumption matters:** Skill complementarity creates endogenous market power. A team can be allocatively optimal yet fail at execution because the pivotal member's bargaining position changes over time.  
**Closest prior work:** [Negotiating Team Formation with DRL (AI 2020)](https://doi.org/10.1016/j.artint.2020.103356); [Heterogeneous-Agent RL (2023)](https://arxiv.org/abs/2304.09870); [COPA dynamic team composition (2021)](https://proceedings.mlr.press/v139/liu21m.html); [Task Load Allocation in Heterogeneous Teams (2022)](https://arxiv.org/abs/2207.08279).  
**What existing work does:** It learns bargaining/team formation, transfers policies across agent types, composes teams dynamically, or balances cooperative workload.  
**What remains unsolved:** Endogenous pivotality exploitation during repeated execution under private, changing capability and outside options.  
**Why it is genuinely multi-agent:** Pivotality exists only relative to the other agents' skills and feasible coalitions.  
**Potential hypothesis:** Counterfactual-feasibility compensation combined with investment in substitute skills reduces strategic withholding and lock-in better than Shapley pay or equal sharing.  
**Potential contribution:** A repeated coalition-execution game, a characterization of extortion equilibria, and a skill-option compensation rule.  
**Potential experiment:** Weighted-voting/bargaining games coupled to sequential pickup, repair, or rescue tasks with 4–12 agents; manipulate specialist scarcity, learning, fatigue, and outside options. Metrics: welfare, holdout rate, payments, team stability, and substitute-skill acquisition.  
**Novelty confidence:** Medium — **plausible gap requiring further verification**.  
**AAMAS relevance:** High.  
**Feasibility:** High.  
**Main risk:** Reviewers may view this as a direct dynamic extension of coalition formation unless execution generates a qualitatively new result.

### H06 — Egalitarian emergent communication under capability asymmetry

**Candidate ID:** H06  
**Research area:** heterogeneity × emergent communication × fairness  
**Precise research question:** Can a population learn a protocol that preserves worst-partner communicative value when agents differ in perception, memory, compute, vocabulary, and learning speed, rather than allowing a high-capacity majority's convention to exclude weak agents?  
**Existing assumption:** Team return or mean cross-play success is the dominant objective; it can hide asymmetric representational burden and failure concentrated on low-capability partners.  
**Why the assumption matters:** A protocol can score highly while forcing weak agents to encode distinctions they cannot represent or while making only one direction of communication effective.  
**Closest prior work:** [Role/Population Heterogeneity in Emergent Communication (ICLR 2022)](https://arxiv.org/abs/2204.12982); [Communication Heterogeneity via Language Alignment / CLAP (IJCAI 2024)](https://www.ijcai.org/proceedings/2024/0005); [Revisiting Populations in Emergent Communication (ICLR 2023)](https://iclr.cc/virtual/2023/poster/11098); [Heterogeneous Visual Agents and Directional Bias (2026)](https://arxiv.org/abs/2605.11695).  
**What existing work does:** It studies heterogeneous roles/populations, aligns independently learned languages, and documents capacity-driven directional asymmetry.  
**What remains unsolved:** A principled objective and generalization test for burden-aware, worst-partner communication across several simultaneous capability asymmetries.  
**Why it is genuinely multi-agent:** Meaning and representational burden are relational properties of sender–receiver pairs and population conventions.  
**Potential hypothesis:** A minimax communicative-value objective with per-agent rate constraints improves bottom-decile cross-play and bidirectional success, at a measurable but bounded mean-return cost.  
**Potential contribution:** Pairwise/burden-aware metrics, a constrained population objective, and a characterization of efficiency–inclusion trade-offs.  
**Potential experiment:** 8–64 heterogeneous agents in Lewis/reference games and embodied cooking, varying encoder size, observation quality, memory, and token budgets. Measure per-pair success, bottom-decile return, directional gap, message rate, compositionality, and unseen-partner cross-play.  
**Novelty confidence:** Medium — **plausible gap requiring further verification**.  
**AAMAS relevance:** High.  
**Feasibility:** High.  
**Main risk:** “Optimize the worst group” alone is too obvious; the paper needs a nontrivial burden/identifiability result.

### H07 — Strategic convention capture under population churn

**Candidate ID:** H07  
**Research area:** population scale × emergent conventions × strategic minorities  
**Precise research question:** What fraction and network position of utility-driven entrants is sufficient to capture the semantics of a population convention while preserving surface coordination accuracy, under ongoing turnover?  
**Existing assumption:** Population-language work treats partners as cooperative draws; naming-game migration work treats committed variants or migrants structurally, not as agents optimizing targeted semantic recoding while remaining behaviorally inconspicuous.  
**Why the assumption matters:** Task success can remain high even if a minority changes what symbols imply in strategically chosen states, so aggregate cross-play misses capture.  
**Closest prior work:** [Other-Play (ICML 2020)](https://proceedings.mlr.press/v119/hu20a.html); [Revisiting Populations in Emergent Communication (ICLR 2023)](https://iclr.cc/virtual/2023/poster/11098); [Population-level Linguistic Conventionality and Turnover (2026)](https://doi.org/10.1093/jole/lzag006); [Migration in the Naming Game (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8001451/).  
**What existing work does:** It promotes convention-independent coordination, trains populations, and studies conventionality or migration under turnover.  
**What remains unsolved:** Adversarially optimized, semantically targeted convention capture under realistic entry/exit and sparse interaction graphs.  
**Why it is genuinely multi-agent:** Capture is a population-dynamic phenomenon depending on interaction topology, learning rules, and minority influence.  
**Potential hypothesis:** Surface success has near-zero power to detect targeted capture; semantic provenance and partner-diversity regularization increase the critical capture threshold.  
**Potential contribution:** A formal capture definition and threshold analysis plus detection/robust-training methods.  
**Potential experiment:** 32–512 agents in naming and referential games on random, scale-free, and community graphs; 1–20% strategic entrants with churn. Metrics: attacker utility, semantic drift, task success, capture threshold, community fragmentation, and detection delay.  
**Novelty confidence:** Medium — **plausible gap requiring further verification**.  
**AAMAS relevance:** Very high.  
**Feasibility:** High with cheap symbolic agents.  
**Main risk:** Committed-minority and norm-tipping literature may already imply the key threshold; targeted hidden semantic capture must produce more than a relabeling of zealotry.

### H08 — Common knowledge under strategic message relays

**Candidate ID:** H08  
**Research area:** imperfect information × communication networks × strategic censorship  
**Precise research question:** In a dynamic partially observable game, under what graph and protocol conditions can agents attain sufficient common belief for coordinated action when intermediate relays may selectively delay, drop, or alter messages and their alignment is uncertain?  
**Existing assumption:** Cooperative Dec-POMDP communication trusts the team channel; strategic communication-network theory often uses one-shot cheap talk or a static outcome rather than learned, stateful coordination.  
**Why the assumption matters:** Signed provenance proves who originated a message but not which messages a relay censored; acknowledgements themselves can be strategically withheld.  
**Closest prior work:** [Incentives and the Structure of Communication (2018)](https://www.sciencedirect.com/science/article/abs/pii/S0022053118300140); [Communication-Efficient Dec-POMDP Learning (2021)](https://arxiv.org/abs/2104.10923); [Uncertain Incentive Alignment in Multi-Agent Systems (AAMAS 2024)](https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p1521.pdf).  
**What existing work does:** It characterizes when networked strategic communication can work, learns when cooperative agents communicate, and reasons about uncertain partner alignment.  
**What remains unsolved:** Approximate common-belief guarantees and adaptive protocols with strategic censorship in long-horizon, partially observable coordination.  
**Why it is genuinely multi-agent:** The epistemic state depends on nested beliefs about who received what through other agents; a sender–receiver reduction removes relay censorship and common knowledge.  
**Potential hypothesis:** Signed provenance plus acknowledgement is insufficient; redundant vertex-disjoint paths with randomized challenges restore bounded common-belief error above a graph-connectivity threshold.  
**Potential contribution:** A dynamic epistemic-game formalization, necessary/sufficient topology conditions in a restricted case, and a learned challenge-routing protocol.  
**Potential experiment:** 5–50 agents in multi-hop search-and-rescue, distributed alarm, and networked stag-hunt tasks with hidden relay types. Compare flooding, signed messages, acknowledgement, reputation routing, and redundant challenge protocols. Measure welfare, false coordination, bandwidth, belief error, and adversarial relay gain.  
**Novelty confidence:** Medium-high — **plausible gap requiring further verification**.  
**AAMAS relevance:** Very high.  
**Feasibility:** High for theory and simulation.  
**Main risk:** Distributed-computing Byzantine agreement may dominate the formulation unless partial alignment, incentives, and learned stateful behavior are essential.

### H09 — Strategic confidence calibration in repeated mixed-motive teams

**Candidate ID:** H09  
**Research area:** communication × uncertainty × competence/alignment inference  
**Precise research question:** How should receivers learn whether a sender is competent, aligned, both, or neither when expressed confidence affects who controls the team's action and therefore changes which claims become verifiable?  
**Existing assumption:** Confidence-calibration methods generally treat reports as non-strategic; cheap-talk models commonly abstract away sequential perception and endogenous authority allocation.  
**Why the assumption matters:** A sender can obtain authority through calibrated-looking selective claims, avoid difficult cases, or make its claims self-confirming by steering the team's action.  
**Closest prior work:** [Strategic Communication of Confidence (AEJ: Microeconomics 2024)](https://www.aeaweb.org/articles?id=10.1257%2Fmic.20220166); [Deceptive Confidence in Advice (2025)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12048683/); [Emergent Deception and Skepticism via Theory of Mind (ICML 2023)](https://icml.cc/virtual/2023/27886); [Uncertain Incentive Alignment (AAMAS 2024)](https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p1521.pdf).  
**What existing work does:** It models strategic confidence in economic communication, demonstrates confidence-based deception, and studies skepticism or uncertain alignment.  
**What remains unsolved:** Joint online identification of competence and alignment when reports endogenously affect decision rights and observation of ground truth.  
**Why it is genuinely multi-agent:** Calibration incentives arise because one agent's report changes another agent's action and the allocation of future authority.  
**Potential hypothesis:** Randomized delayed verification with a proper score over a factorized competence/alignment posterior prevents selective-confidence gaming and improves team utility over naive calibration or reputation.  
**Potential contribution:** An endogenous-verification signaling game, identifiability result, and authority-aware elicitation rule.  
**Potential experiment:** 3–8 agents receive signals of heterogeneous quality and hidden side goals, report answer/confidence, and jointly choose an irreversible action. Compare majority, confidence weighting, proper scoring, trust models, and randomized audit. Metrics: calibration, decision welfare, authority concentration, deceptive-report gain, and competence/alignment recovery.  
**Novelty confidence:** Medium — **plausible gap requiring further verification**.  
**AAMAS relevance:** High.  
**Feasibility:** High.  
**Main risk:** The economic information-elicitation literature may already solve a mathematically equivalent problem; sequential endogenous verification must be central.

### H10 — Reputation redemption without enabling whitewashing

**Candidate ID:** H10  
**Research area:** reputation × adaptation × long-term cooperation  
**Precise research question:** How should a multi-agent system allocate scarce opportunities to test whether a genuinely updated or retrained low-reputation agent has improved, without letting intermittent defectors exploit resets, decay, or “redemption” probes?  
**Existing assumption:** Reputation methods infer relatively stable behavioral type or use decay; adaptation work assumes agents continue receiving interactions from which improvement can be learned.  
**Why the assumption matters:** Bad reputation can create a self-confirming lockout: an improved agent never receives diagnostic tasks. Aggressive forgetting solves lockout but enables strategic whitewashing.  
**Closest prior work:** [Reputation-based Partner Choice in MARL (2021)](https://arxiv.org/abs/2103.04982); [Bottom-up Reputation Promotes Cooperation (AAMAS 2025)](https://arxiv.org/abs/2502.01971); [COOPER: Emergent Reputation (2026)](https://arxiv.org/abs/2606.04359); [Skill-Conditional Trust and Cross-Skill Laundering (2026)](https://arxiv.org/abs/2606.14200); [Whitewashing in Reputation Systems (2017)](https://academic.oup.com/comjnl/article-abstract/60/8/1223/3064965).  
**What existing work does:** It learns reputation for partner choice, studies emergent cooperation, makes trust task-conditional, and analyzes identity resets.  
**What remains unsolved:** Optimal allocation of diagnostic interactions after real policy change, balancing time-to-redemption against strategic recidivism and opportunity cost.  
**Why it is genuinely multi-agent:** Reputation changes who is selected by others; the evidence needed to update it is jointly produced and competitively scarce.  
**Potential hypothesis:** A change-point posterior plus costly, randomized low-stakes diagnostic tasks reduces lockout regret without increasing intermittent-defector gain relative to decay, reset, or global reputation.  
**Potential contribution:** A redemption–whitewashing trade-off, lower bound, and audit-allocation algorithm.  
**Potential experiment:** Repeated partner-selection bandit and task-router environments with competence upgrades, policy fine-tuning, failures, and strategic periodic defectors. Metrics: welfare/regret, time-to-redemption, false redemption, attacker gain, audit cost, and opportunity inequality.  
**Novelty confidence:** Medium-high — **plausible gap requiring further verification**.  
**AAMAS relevance:** Very high.  
**Feasibility:** Very high; primarily simulation/bandit scale.  
**Main risk:** It can look like standard non-stationary bandits unless reciprocal partner choice and strategic behavior yield distinctive theory.

### H11 — Reputation identity for cloneable and forkable agents

**Candidate ID:** H11  
**Research area:** agent identity × reputation × cooperation  
**Precise research question:** When policies can be cloned, fine-tuned, merged, or cheaply re-instantiated, should liability and reputation attach to runtime instance, policy lineage, operator, or task-specific behavior—and what cooperation guarantees are possible under each choice?  
**Existing assumption:** Classical reputation and Sybil analyses treat identities as principals; agentic systems make behavioral code and operating identity separable and cheaply forkable.  
**Why the assumption matters:** Per-instance reputation collapses under cloning, full lineage inheritance punishes beneficial forks, and operator-level reputation may pool unrelated policies.  
**Closest prior work:** [Whitewashing in Reputation Systems (2017)](https://academic.oup.com/comjnl/article-abstract/60/8/1223/3064965); [Achieving Sybil-Proofness in Distributed Work Systems](https://research.tudelft.nl/en/publications/achieving-sybil-proofness-in-distributedwork-systems/); [Reputation-based Partner Choice in MARL (2021)](https://arxiv.org/abs/2103.04982); [Talk, Judge, Cooperate (2026)](https://arxiv.org/abs/2602.07777).  
**What existing work does:** It analyzes reset/Sybil attacks, reputation-based partner choice, and reputation-like cooperation among language agents.  
**What remains unsolved:** Liability inheritance over mutable policy lineages and the cooperation–innovation trade-off produced by forks.  
**Why it is genuinely multi-agent:** Identity choice affects partner selection, sanctions, and strategic cloning across a population.  
**Potential hypothesis:** Bounded lineage-linked liability with task-conditional audits sustains cooperation under cheap cloning while permitting honest forks better than instance-only or full-inheritance reputation.  
**Potential contribution:** A policy-lineage identity game, equilibrium bounds on clone attacks, and a lineage-aware reputation rule.  
**Potential experiment:** 50–1,000 agents in repeated social dilemmas and an agent-service marketplace; vary clone cost, mutation, operator multiplicity, and task similarity. Metrics: cooperation, attack profit, honest-fork survival, concentration, and false inheritance.  
**Novelty confidence:** Medium — **plausible gap requiring further verification**.  
**AAMAS relevance:** High.  
**Feasibility:** High in simulation.  
**Main risk:** Without a credible provenance model this becomes infrastructure policy rather than MAS science.

### H12 — Endogenous selective memory in repeated cooperation

**Candidate ID:** H12  
**Research area:** memory × incentives × repeated games  
**Precise research question:** What cooperation equilibria arise when agents choose which interaction evidence to store, summarize, delete, or disclose under a memory budget, rather than receiving an exogenous bounded-memory state?  
**Existing assumption:** Bounded-recall and memory-length models fix what agents remember; shared-memory systems optimize retrieval but rarely model strategic evidence curation.  
**Why the assumption matters:** Agents may deliberately forget their own commitments, hide defections, retain only favorable precedents, or strategically forgive partners.  
**Closest prior work:** [Cooperation with Forgetfulness (2012)](https://doi.org/10.1287/mnsc.1100.1271); [Repeated Games with Endogenous Information (1999)](https://doi.org/10.1287/moor.24.4.785); [Memory Length and Cooperation (2023)](https://arxiv.org/abs/2307.04612); [Imperfect Recall Games (2024)](https://arxiv.org/abs/2406.15970).  
**What existing work does:** It characterizes cooperation under forgetfulness, endogenous signals, bounded memory, or imperfect recall.  
**What remains unsolved:** Memory writes/deletions as observable or hidden strategic actions with compression error and downstream partner selection.  
**Why it is genuinely multi-agent:** The value and truthfulness of memory arise from future partners conditioning their behavior on retained evidence.  
**Potential hypothesis:** Unrestricted self-curation creates motivated-forgetting equilibria; jointly committed append-only compressed summaries sustain cooperation with sublinear storage while unverifiable private summaries do not.  
**Potential contribution:** An endogenous-memory repeated game, equilibrium characterization, and verifiable compression protocol.  
**Potential experiment:** 4–20 agents in repeated public goods, Cleanup, or trust games with explicit memory-write/delete actions and budgets. Compare full history, fixed windows, private summarizers, append-only commitments, and random audits. Metrics: welfare, exploitability, storage, evidence retention, and false-accusation rate.  
**Novelty confidence:** Medium-low — **plausible gap requiring further verification**.  
**AAMAS relevance:** High.  
**Feasibility:** High.  
**Main risk:** The game may reduce to costly record-keeping or disclosure theory already studied in economics.

### H13 — Incentives to contribute verified shared memory

**Candidate ID:** H13  
**Research area:** shared memory × public-goods provision × data valuation  
**Precise research question:** How can agents be induced to pay the cost of verifying and contributing useful experiences to a shared memory when benefit is delayed and coalition-dependent?  
**Existing assumption:** Shared-memory systems assume cooperative writers or focus on access control, poisoning, leakage, and provenance rather than contribution incentives.  
**Why the assumption matters:** Rational agents can free-ride on the memory, and naive contribution counts reward spam rather than causal value.  
**Closest prior work:** [Governed Shared Memory (2026)](https://arxiv.org/abs/2606.24535); [Memory Poisoning in Multi-Agent Systems (2026)](https://arxiv.org/abs/2603.20357); [Incentivizing Data Collaboration (NeurIPS 2025)](https://neurips.cc/virtual/2025/129467); [Fair and Efficient Memory Sharing (AAAI 2019)](https://doi.org/10.1609/aaai.v33i01.33011965).  
**What existing work does:** It governs shared stores, attacks memory integrity, designs data-collaboration incentives, or allocates cache resources.  
**What remains unsolved:** Causal credit for epistemic memory items consumed by interacting agents under non-stationary policies.  
**Why it is genuinely multi-agent:** Memory is a public good whose value arises from other agents' later decisions.  
**Potential hypothesis:** Counterfactual replay credits reduce free-riding and spam relative to count- or rating-based rewards.  
**Potential contribution:** A memory-contribution game and approximate value estimator.  
**Potential experiment:** 4–16 agents in cooperative exploration or a research workflow with planted verifiable facts, contribution/verification costs, and a shared store.  
**Novelty confidence:** Low-medium — **rejected as currently framed**.  
**AAMAS relevance:** Medium.  
**Feasibility:** Medium-high.  
**Main risk:** This is currently a generic transfer of data-market valuation to memory and may be mainly systems engineering. Retain only if a distinctly interaction-dependent impossibility or behavioral phenomenon is established.

### H14 — Early warning of population-level coordination collapse

**Candidate ID:** H14  
**Research area:** population scale × heterogeneous learning × intervention  
**Precise research question:** Can local behavioral traces predict an endogenous transition from a high-welfare convention to a low-welfare equilibrium early enough for a minimal targeted intervention, when agents use heterogeneous learning rules on a sparse network?  
**Existing assumption:** Mean-field models summarize populations; large-agent evaluations report aggregate outcomes; neither necessarily predicts an impending transition from deployable local signals.  
**Why the assumption matters:** Aggregate reward may stay stable until bridge agents switch, after which a convention cascades; broadcast intervention is expensive and may itself destabilize norms.  
**Closest prior work:** [Mean Field Multi-Agent RL (2018)](https://arxiv.org/abs/1802.05438); [Networked Communication in Mean-Field Games (2023)](https://arxiv.org/abs/2306.02766); [Phase Structure of Independent Q-Learning (2025)](https://arxiv.org/abs/2511.23315); [Evaluating Collective Behaviour of Hundreds of LLM Agents (AAMAS 2026)](https://arxiv.org/abs/2602.16662).  
**What existing work does:** It scales learning through mean-field approximation, studies communication topology or learning phases, and measures collective behavior at large agent counts.  
**What remains unsolved:** Prospective, locally observable warning indicators tied to a cost-minimal causal intervention under heterogeneous adaptation.  
**Why it is genuinely multi-agent:** Collapse is a cascade generated by policy coupling, topology, and population response; no independent-run metric captures it.  
**Potential hypothesis:** Spectral bridge-instability and policy-response indicators predict welfare collapse before reward decline; intervening on bridge agents outperforms broadcast incentives at equal cost.  
**Potential contribution:** A tipping-risk statistic, intervention policy, and finite-population analysis.  
**Potential experiment:** 100–10,000 cheap agents in spatial public goods, congestion, commons, and convention games on several graph families; mix Q-learning, aspiration, imitation, and no-regret learners. Metrics: warning lead time, false alarms, intervention cost, welfare recovery, and robustness to learner mix.  
**Novelty confidence:** Medium — **plausible gap requiring further verification**.  
**AAMAS relevance:** Very high.  
**Feasibility:** High with algorithmic agents; no LLMs required.  
**Main risk:** Early-warning indicators for network cascades are mature outside MAS; the learning-specific causal advantage must be demonstrated.

### H15 — Cross-implementation zero-shot coordination

**Candidate ID:** H15  
**Research area:** heterogeneity × zero-shot coordination  
**Precise research question:** Do conventions learned by different codebases, architectures, observation encodings, and training pipelines coordinate zero-shot, rather than merely across random seeds of one implementation?  
**Existing assumption:** Inter-seed cross-play is often used as evidence of robustness to unfamiliar partners.  
**Why the assumption matters:** Shared implementation choices can leak a common convention and substantially overstate open-system interoperability.  
**Closest prior work:** [Other-Play (2020)](https://proceedings.mlr.press/v119/hu20a.html); [Any-Play (AAMAS 2022)](https://ifaamas.org/Proceedings/aamas2022/pdfs/p853.pdf); [Heterogeneous Zero-Shot Coordination (2022)](https://arxiv.org/abs/2208.04957); [Is Inter-Seed Cross-Play Enough? (August 2026)](https://arxiv.org/abs/2608.03644).  
**What existing work does:** It trains convention-robust agents, diverse partner populations, heterogeneous agents, and—critically—the August 2026 paper directly studies cross-implementation evaluation.  
**What remains unsolved:** Possibly online repair after mismatch discovery, but that is a different ad-hoc teamwork problem.  
**Why it is genuinely multi-agent:** Cross-play is defined by interaction with independently developed partners.  
**Potential hypothesis:** The generic hypothesis is already being directly tested by 2026 work.  
**Potential contribution:** None sufficiently distinct in this formulation.  
**Potential experiment:** A broader implementation matrix would mainly extend the existing evaluation.  
**Novelty confidence:** Low — **rejected / already directly addressed**.  
**AAMAS relevance:** High.  
**Feasibility:** Medium.  
**Main risk:** It would be an incremental benchmark follow-up to a paper that asks essentially the same question.

### H16 — Audience-selective legibility in mixed-motive planning

**Candidate ID:** H16  
**Research area:** predictability/legibility × strategic observers  
**Precise research question:** Can a planner be predictable to aligned observers while hiding intent from adversarial observers with different visibility?  
**Existing assumption:** Cooperative predictability methods assume observers benefit from predictability; deceptive planning often assumes the observer is adversarial.  
**Why the assumption matters:** Real environments contain both audiences simultaneously.  
**Closest prior work:** [Predictability Awareness for Multi-Agent Coordination (AAMAS 2025)](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p886.pdf); [From Legible to Inscrutable Trajectories (2026)](https://arxiv.org/abs/2602.09227); [Observer-Aware Probabilistic Planning (2025)](https://arxiv.org/abs/2502.10568); [Interpretable Agent Behavior taxonomy (2019)](https://arxiv.org/abs/1811.09722).  
**What existing work does:** The 2026 MMLO-LMP formulation explicitly optimizes legibility for positive-motive observers and illegibility for negative-motive observers under limited visibility.  
**What remains unsolved:** Dynamic observer teams and learned observer adaptation are extensions, but not enough by themselves to establish a new gap.  
**Why it is genuinely multi-agent:** Different observers infer and act on the planner's intent.  
**Potential hypothesis:** The generic hypothesis is already supported by DUBIOUS in the 2026 paper.  
**Potential contribution:** None sufficiently distinct without a new scientific mechanism.  
**Potential experiment:** Moving observer coalitions would be an extension of the published formulation.  
**Novelty confidence:** Low — **rejected / already directly addressed**.  
**AAMAS relevance:** High.  
**Feasibility:** Medium-high.  
**Main risk:** A paper already does almost exactly this; this candidate fails the kill test.

## Opportunity triage

| Priority | Candidate | Interaction effect that cannot be reduced to “A + B” | Status |
|---:|---|---|---|
| 1 | H02 causal attribution of non-stationarity | Another agent may change *because of ego's policy*; observational prediction cannot determine whether to track, robustify, or shape | Verified missing formulation in this comparison set |
| 2 | H04 evolving strategic capability with coalition feedback | Capability learning, effort incentives, and credit are jointly unidentifiable from coalition outcomes | Plausible; strong |
| 3 | H03 strategic teaching of the designer | A mechanism update becomes an action channel participants can shape for future gain | Plausible; strong |
| 4 | H08 strategic relays and common belief | Message censorship changes nested beliefs and the feasibility of coordinated action | Plausible; strong formal route |
| 5 | H10 reputation redemption | Reputation determines access to the evidence needed to revise reputation | Plausible; strong and feasible |
| 6 | H01 scarce strategic communication | A message's value is jointly created by receiver and continuation policies, so a sender can manipulate both auction and outcome | Plausible; dangerous old auction prior |
| 7 | H07 strategic convention capture | A minority can change semantics while preserving aggregate task success | Plausible; needs norm-tipping audit |
| 8 | H14 collapse early warning | Topology-coupled heterogeneous learning produces a cascade before reward reveals it | Plausible; adjacent network-science risk |
| 9 | H06 egalitarian emergent communication | Protocol efficiency and representational burden are pairwise and asymmetric | Plausible; contribution must exceed a fairness objective |
| 10 | H05 pivotal-skill extortion | Complementarity creates endogenous bargaining power during execution | Plausible; coalition-formation risk |
| 11 | H09 strategic confidence | Reports allocate authority and thereby determine later verifiability | Plausible; economics overlap |
| 12 | H11 lineage reputation | Cheap policy forking separates behavioral lineage from runtime identity | Plausible; provenance assumptions matter |
| 13 | H12 endogenous memory | Remembering/deleting evidence is itself a strategic action | Plausible but fragile |
| — | H13 shared-memory contribution | Currently a generic data-valuation transfer | Rejected as framed |
| — | H15 cross-implementation ZSC | Directly addressed by August 2026 work | Rejected |
| — | H16 selective legibility | Directly formulated and solved in a February 2026 paper | Rejected |

### Best opportunities for the parent synthesis

1. **H02** has the cleanest scientific core. A deliberately constructed pair of observationally equivalent Markov games can prove why prediction-only opponent models are insufficient, while controlled interventions give a measurable path forward.
2. **H04** has unusually good AAMAS centrality: coalition formation, learning, incentives, and uncertainty genuinely interact. Narrow it to binary complementary skills, Markov capability drift, and coalition success feedback to keep theory and experiments executable.
3. **H03** connects opponent shaping to online mechanism design in a way the inspected work acknowledges indirectly through co-learning but does not isolate as the principal problem.
4. **H08** offers the strongest theorem route, but must explicitly distinguish incentive-driven strategic relays from crash/Byzantine faults and static cheap-talk networks.
5. **H10** is the lowest-compute opportunity and has a crisp endogenous-observation loop; a non-stationary strategic partner-selection model can support lower bounds and robust experiments.

## Blind combinations and attractive ideas rejected by the search

- **“Add cost-aware communication to LLM agents.”** Rejected: DALA already auctions speaking opportunities and evaluates token-efficient interaction. The remaining question must be strategic manipulation under mixed motives (H01).
- **“Model both opponent and environment.”** Rejected: joint environment–opponent models exist in 2025–2026. The surviving question is causal source attribution under observational equivalence (H02).
- **“Use opponent shaping with language agents.”** Rejected: ShapeLLM directly occupies this space.
- **“Learn an adaptive mechanism with MARL.”** Rejected: deep mechanism design, adaptive reward sharing, and principal–agent learning already do this. Strategic teaching of the designer is the narrower opportunity (H03).
- **“Task allocation for unknown heterogeneous capabilities.”** Rejected: adaptive capability-learning MRTA and CASH cover the generic version. Strategic evolving types plus coalition-only feedback is the missing interaction (H04).
- **“Fair communication for heterogeneous agents.”** Too generic. H06 survives only if fairness is formalized as pairwise representational burden and a nontrivial worst-partner constraint.
- **“Study convention change under turnover.”** Rejected generically: 2026 work directly studies conventionality and turnover. H07 requires goal-directed, hidden semantic capture by utility-maximizing entrants.
- **“Secure provenance for shared memory.”** Rejected generically: governed shared memory and memory-poisoning papers already target provenance/security. Contribution incentives (H13) still looked too close to data markets.
- **“Contextual reputation.”** Rejected: 2026 skill-conditional trust explicitly analyzes cross-skill reputation laundering. H10 instead asks who receives diagnostic opportunities after real change.
- **“Reputation promotes LLM-agent cooperation.”** Rejected: reputation-based MARL, AAMAS 2025 bottom-up reputation, COOPER, and 2026 language-agent cooperation already cover it.
- **“Evaluate hundreds of LLM agents.”** Rejected as an opportunity: AAMAS 2026 already evaluates collective behavior at this scale. H14 needs a prospective intervention hypothesis, not a scaling benchmark.
- **“Cross-implementation zero-shot coordination.”** Rejected: the August 2026 paper *Is Inter-Seed Cross-Play Enough?* directly performs this audit.
- **“Be legible to allies and illegible to adversaries.”** Rejected: MMLO-LMP/DUBIOUS (February 2026) asks exactly this under motive and visibility heterogeneity.
- **“Benchmark deception in multi-agent LLMs.”** Rejected as benchmark-first: recent hidden-role, collusion, and deception work already makes generic deception evaluation crowded; a paper needs a mechanism such as strategic confidence or relay censorship.
- **“Just combine memory and cooperation.”** Rejected: repeated-game forgetfulness and memory-length effects are old and active. H12 only survives by making retention/deletion an endogenous strategic action.

## Search strategy and recent-work audit

Searches were intentionally vocabulary-diverse. Besides the modern labels in the task, I searched **cheap talk, signaling, information elicitation, confidence reports, communication equilibrium, interdependent-value bandwidth auctions, Dec-POMDP communication, strategic network relay, execution uncertainty, coalition formation, pivotal player, ad hoc teamwork, opponent shaping, policy teaching, principal–agent learning, bounded/imperfect recall, endogenous information, whitewashing, Sybil identities, naming games, committed minorities, mean-field games, phase transitions, and cross-play**.

The 2025–2026 kill pass materially changed the result:

- DALA killed generic communication-cost ideas but exposed the mixed-motive manipulation question.
- 2025–2026 joint world/opponent models and causal opponent models killed generic model-factorization ideas but did not answer causal source attribution.
- 2026 skill-conditional trust killed generic contextual-reputation ideas.
- 2026 turnover/conventionality work killed generic convention-churn ideas.
- August 2026 cross-implementation work killed H15.
- February 2026 mixed-motive legible planning killed H16.
- 2026 shared-memory governance/poisoning work made H13 too incremental without a deeper public-goods theorem.

## Unique-paper ledger (54 records)

Each row denotes one distinct research record used in candidate generation or elimination. “Inspected” ranges from full text/method/limitations where accessible to abstract plus primary metadata for peripheral kill-test records; it does **not** mean all 54 papers were read line-by-line.

| ID | Year | Research record | Relevance |
|---:|---:|---|---|
| L01 | 2026 | [Cost-Effective Communication: An Auction-based Method for Language Agent Interaction (DALA)](https://doi.org/10.1609/aaai.v40i35.40182) | scarce communication auction |
| L02 | 2007 | [Handling Interdependent Values in an Auction Mechanism for Bandwidth Allocation](https://insights.sei.cmu.edu/library/handling-interdependent-values-in-an-auction-mechanism-for-bandwidth-allocation-in-tactical-data-networks/) | strategic bandwidth allocation |
| L03 | 2012 | [Communication and Efficiency in Auctions](https://www.sciencedirect.com/science/article/pii/S089982561100176X) | auction communication complexity |
| L04 | 2021 | [Learning When to Communicate at Scale in Multiagent Cooperative and Competitive Tasks](https://arxiv.org/abs/2104.10923) | Dec-POMDP communication |
| L05 | 2020 | [LeMOL: Learning to Model Opponent Learning](https://arxiv.org/abs/2006.03923) | opponent adaptation |
| L06 | 2021 | [Model-Based Opponent Modeling (MBOM)](https://arxiv.org/abs/2108.01843) | opponent latent models |
| L07 | 2025 | [Applying Opponent and Environment Modelling to Enhance MARL](https://doi.org/10.1016/j.cogsys.2024.101306) | joint environment/opponent models |
| L08 | 2026 | [Structured Opponent Modeling with Structural Causal Models (SOM)](https://arxiv.org/abs/2605.07301) | causal opponent model |
| L09 | 2026 | [Hierarchical Fusion of World and Opponent Models](https://doi.org/10.1016/j.engappai.2026.114402) | fused prediction |
| L10 | 2025 | [ShapeLLM: Behavior Shaping with Multi-Agent LLMs](https://arxiv.org/abs/2510.08255) | explicit opponent shaping |
| L11 | 2025 | [Deep Mechanism Design: Learning Social and Economic Policies](https://pmc.ncbi.nlm.nih.gov/articles/PMC12207456/) | designer/player co-learning |
| L12 | 2026 | [Microeconomic Foundations of Multi-Agent Learning](https://arxiv.org/abs/2601.03451) | learning principal–agent mechanisms |
| L13 | 2025 | [Adaptive Reward Sharing for Cooperative MARL](https://openreview.net/pdf?id=NVGrTKTGhe) | adaptive incentives |
| L14 | 2023 | [Multi-Timescale Multi-Agent Reinforcement Learning](https://proceedings.mlr.press/v232/nekoei23a.html) | heterogeneous learning rates |
| L15 | 2013 | [Mechanism Design with Execution Uncertainty](https://arxiv.org/abs/1301.0595) | strategic uncertain execution |
| L16 | 2016 | [Fault-Tolerant General-Purpose Task Allocation in Multi-Agent Systems](https://eprints.soton.ac.uk/388365/) | trust/task allocation |
| L17 | 2020 | [Adaptive Task Allocation for Multi-Robot Teams with Unknown and Evolving Capabilities](https://arxiv.org/abs/2003.03344) | evolving capabilities |
| L18 | 2025 | [Uncertainty-Aware Multi-Agent Credit Assignment with Coupled Rewards](https://arxiv.org/abs/2509.22469) | coalition outcome uncertainty |
| L19 | 2022 | [Online Allocation with Strategic Agents](https://arxiv.org/abs/2209.12112) | strategic repeated allocation |
| L20 | 2025 | [CASH: Capability-Aware Skill Coordination for Heterogeneous Multi-Robot Teams](https://proceedings.mlr.press/v305/fu25a.html) | capability-aware coordination |
| L21 | 2020 | [Negotiating Team Formation Using Deep Reinforcement Learning](https://doi.org/10.1016/j.artint.2020.103356) | bargaining/pivotal agents |
| L22 | 2023 | [Heterogeneous-Agent Reinforcement Learning](https://arxiv.org/abs/2304.09870) | capability heterogeneity |
| L23 | 2021 | [COPA: Coordinated Policy Optimization for Dynamic Team Composition](https://proceedings.mlr.press/v139/liu21m.html) | dynamic teams |
| L24 | 2022 | [On the Role of Population Heterogeneity in Emergent Communication](https://arxiv.org/abs/2204.12982) | heterogeneous protocols |
| L25 | 2026 | [Emergent Communication in Heterogeneous Visual Agents](https://arxiv.org/abs/2605.11695) | capacity-driven directional bias |
| L26 | 2024 | [Cross-Lingual Agent Protocol / CLAP](https://www.ijcai.org/proceedings/2024/0005) | aligning heterogeneous languages |
| L27 | 2023 | [Revisiting Populations in Emergent Communication](https://iclr.cc/virtual/2023/poster/11098) | population cross-play |
| L28 | 2020 | [Other-Play for Zero-Shot Coordination](https://proceedings.mlr.press/v119/hu20a.html) | convention-independent coordination |
| L29 | 2026 | [Population-level Linguistic Conventionality Benefits from Turnover](https://doi.org/10.1093/jole/lzag006) | convention/churn kill test |
| L30 | 2021 | [Migration and Consensus in the Naming Game](https://pmc.ncbi.nlm.nih.gov/articles/PMC8001451/) | population convention dynamics |
| L31 | 2018 | [Incentives and the Structure of Communication](https://www.sciencedirect.com/science/article/abs/pii/S0022053118300140) | strategic relays/topology |
| L32 | 2024 | [Strategic Communication of Confidence](https://www.aeaweb.org/articles?id=10.1257%2Fmic.20220166) | strategic confidence reports |
| L33 | 2025 | [Confidence as a Vehicle for Deceptive Advice](https://pmc.ncbi.nlm.nih.gov/articles/PMC12048683/) | confidence deception |
| L34 | 2023 | [Emergent Deception and Skepticism with Theory of Mind](https://icml.cc/virtual/2023/27886) | deception/skepticism |
| L35 | 2024 | [Reasoning about Uncertain Incentive Alignment in Multi-Agent Systems](https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p1521.pdf) | hidden alignment |
| L36 | 2021 | [Social Diversity and Reputation in MARL](https://arxiv.org/abs/2103.04982) | reputation/partner choice |
| L37 | 2025 | [Bottom-up Reputation Promotes Cooperation (AAMAS)](https://arxiv.org/abs/2502.01971) | reputation emergence |
| L38 | 2026 | [COOPER: Emergent Reputation and Cooperation](https://arxiv.org/abs/2606.04359) | reputation cooperation |
| L39 | 2026 | [Skill-Conditional Trust and Cross-Skill Reputation Laundering](https://arxiv.org/abs/2606.14200) | contextual reputation kill test |
| L40 | 2017 | [Whitewashing in Reputation Systems](https://academic.oup.com/comjnl/article-abstract/60/8/1223/3064965) | identity reset attacks |
| L41 | — | [Achieving Sybil-Proofness in Distributed Work Systems](https://research.tudelft.nl/en/publications/achieving-sybil-proofness-in-distributedwork-systems/) | clone/Sybil identity |
| L42 | 2012 | [Cooperation with Forgetfulness](https://doi.org/10.1287/mnsc.1100.1271) | bounded recall/cooperation |
| L43 | 1999 | [Repeated Games with Endogenous Information](https://doi.org/10.1287/moor.24.4.785) | strategic information state |
| L44 | 2023 | [Memory Length and the Evolution of Cooperation](https://arxiv.org/abs/2307.04612) | memory/cooperation |
| L45 | 2024 | [The Complexity of Games with Imperfect Recall](https://arxiv.org/abs/2406.15970) | formal imperfect memory |
| L46 | 2026 | [Governed Shared Memory for Multi-Agent Systems](https://arxiv.org/abs/2606.24535) | memory governance |
| L47 | 2026 | [Memory Poisoning in Multi-Agent Systems](https://arxiv.org/abs/2603.20357) | shared-memory security |
| L48 | 2025 | [Incentivizing Data Collaboration (NeurIPS)](https://neurips.cc/virtual/2025/129467) | contribution incentives kill test |
| L49 | 2019 | [Fair and Efficient Memory Sharing for Collaborative Multi-Agent Systems](https://doi.org/10.1609/aaai.v33i01.33011965) | memory-resource allocation |
| L50 | 2018 | [Mean Field Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1802.05438) | population scale |
| L51 | 2023 | [Networked Communication in Mean-Field Games](https://arxiv.org/abs/2306.02766) | topology/population learning |
| L52 | 2025 | [Phase Structure of Independent Q-Learning](https://arxiv.org/abs/2511.23315) | learning transitions |
| L53 | 2026 | [Evaluating Collective Behaviour of Hundreds of LLM Agents](https://arxiv.org/abs/2602.16662) | large-population kill test |
| L54 | 2026 | [Is Inter-Seed Cross-Play Enough?](https://arxiv.org/abs/2608.03644) | cross-implementation kill test |

## Bottom line

No candidate should yet be advertised as a universal “first.” The strongest narrow claim supported by this search is: **the inspected opponent/world-model, opponent-shaping, and non-stationary MARL papers do not directly test whether an agent can causally distinguish exogenous drift, independent co-learner adaptation, and ego-induced strategic adaptation under matched observational behavior.** That makes H02 the clearest Agent-H recommendation.

H04, H03, H08, and H10 are strong **plausible gaps** with executable experimental designs and genuine interaction effects, but each needs a dedicated backward/forward citation audit before paper positioning. H13, H15, and H16 should not proceed in their current forms.
