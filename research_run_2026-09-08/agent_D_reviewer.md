# Agent D — Skeptical AAMAS main-track review

**Cut-off:** 8 September 2026  
**Inputs reviewed:** Agents A, B, C, E, and H; the official AAMAS 2025–2026 proceedings; and targeted primary-source kill searches.  
**Decision rule:** a candidate survives only if interaction among autonomous decision-makers creates the scientific problem, the contribution can exceed a benchmark or engineering wrapper, and a falsifying experiment is practical. “Survives” means *worth deeper novelty audit*, not “verified novel.”

## Reviewer bottom line

I would send **10** formulations to the next audit. Only five are strong enough to develop now. None has earned a “first” claim.

| Rank | Narrow formulation | Reviewer status | Novelty confidence | Main-track outlook |
|---:|---|---|---|---|
| 1 | Causal source attribution for multi-agent non-stationarity | Proceed | Medium–high | High if it includes non-identifiability and intervention results |
| 2 | Identifiability and selective probing in offline ad-hoc teamwork | Proceed | Medium–high | High |
| 3 | Dual-control probing of a learning teammate | Proceed | Medium | High if influence is causal, not just faster adaptation |
| 4 | Common belief under strategic message relays | Proceed conditionally | Medium | High with graph/epistemic theorem |
| 5 | Coalition allocation with evolving private capability and coalition-only feedback | Proceed conditionally | Medium | High if sharply restricted |
| 6 | Strategic teaching of an adaptive mechanism designer | Hold | Medium | High variance |
| 7 | Tracking mutually drifting communication protocols | Hold | Medium | Medium–high |
| 8 | Reputation redemption without whitewashing | Hold | Medium | Medium–high |
| 9 | Receiver-side selective verification against adapting senders | Hold/high prior-art risk | Medium–low | Medium |
| 10 | Distributed retraction after lossy multi-agent summarization | Hold/near-kill | Low–medium | Medium only after differentiating from Grounded Continuation |

The recommended portfolio is ranks 1–5. Ranks 6–10 are legitimate research questions, but each has a dangerous neighboring literature or scope problem.

## Immediate rejections

- **Generic Dec-POMDP-optimum grounding for LLM teams:** useful evaluation, but [Commitment-Driven Distributed Joint Policy Search](https://doi.org/10.1145/1229555.1229619), [MAGRPO](https://neurips.cc/virtual/2025/128017), [LLM-Coordination](https://aclanthology.org/2025.findings-naacl.448/), and [Shared Action Suggestions](https://ojs.aaai.org/index.php/AAAI/article/view/40171) leave only a narrow policy-realization residual. Without a new synthesis/repair result, this is a Findings or evaluation paper.
- **Generic scarce adaptive verification:** occupied by [Truthful Reporting of Competence with Minimal Verification](https://arxiv.org/abs/2602.14076), [One Human, N Agents](https://arxiv.org/abs/2607.28317), and the broader inspection/mechanism-design literature.
- **Peer sanctioning under noisy blame:** classical noisy reputation and sanctioning already contain harmful-noise thresholds. A real structured-bias inversion could be a separate conditional project, but the generic gap is closed.
- **Shared memory “as a commons”:** the framing is explicitly occupied by 2026 institutional/shared-memory work. A new equilibrium forced by costly verification and downstream reuse might survive, but “add contribution incentives” is not enough.
- **Generic correlated-error-aware debate:** [AgentAuditor](https://arxiv.org/abs/2602.09341), [One Human, N Agents](https://arxiv.org/abs/2607.28317), and [When Truth Is Distributed](https://arxiv.org/abs/2608.03421) already study correlated consensus, evidential structure, auditing, and evidence lineage. A causal acquisition theorem might survive, but the current pitch is too close.
- **Generic identity-churn/Sybil reputation:** [Dissociative Identity](https://arxiv.org/abs/2605.30169) and [Epistemic Sybil Resistance](https://arxiv.org/abs/2609.01873) substantially raise the novelty bar.
- **Communication congestion plus correlated loss:** [CAIC](https://proceedings.mlr.press/v337/li26h.html) is too close unless the externality yields a new theorem rather than another network impairment.
- **Cross-implementation zero-shot coordination:** directly addressed by [Is Inter-Seed Cross-Play Enough?](https://arxiv.org/abs/2608.03644).
- **Audience-selective legibility:** directly occupied by [From Legible to Inscrutable Trajectories](https://arxiv.org/abs/2602.09227).
- **Another topology/role/team-formation benchmark:** benchmark-only unless tied to an identifiable multi-agent phenomenon; [MultiAgentBench](https://arxiv.org/abs/2503.01935), [TeamBench](https://arxiv.org/abs/2505.21668), and [Too Many Specialists](https://arxiv.org/abs/2605.08540) make generic variants incremental.
- **Generic convention collapse from information sharing:** [The Interaction Tax](https://arxiv.org/abs/2608.23541) and 2026 diversity-collapse work occupy the phenomenon.
- **Policy-enforcement peers, harness-update gates, and verifier panels:** currently engineering/evaluation combinations. They lack a necessary strategic model or new formal result.

## 1. Causal source attribution for multi-agent non-stationarity

### Contribution and significance

**Question.** From local histories, can an agent distinguish exogenous environment drift, independent peer adaptation, and peer adaptation caused by the ego agent, then choose tracking, robust control, or shaping accordingly?

This is genuinely multi-agent because the third process is reflexive: another decision-maker updates *because of* the focal policy. A non-stationary MDP cannot preserve that causal channel. The contribution should be: (i) an observational non-identifiability construction; (ii) conditions under which bounded interventions identify the source; and (iii) an attribution-conditioned controller with dynamic-regret or harmful-shaping guarantees.

Closest work models non-stationary opponents or causal opponent structure—[LeMOL](https://arxiv.org/abs/2006.03923), [MBOM](https://arxiv.org/abs/2108.01843), [Influencing Towards Stable Multi-Agent Interactions](https://arxiv.org/abs/2110.08229), [SOM](https://arxiv.org/abs/2605.07301), and [ShapeLLM](https://arxiv.org/abs/2510.08255)—but the reviewed formulations do not make source attribution among matched observational processes the decision problem.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** a factored non-stationary Markov game with latent source variable and ego interventions.
- **Required experiment:** paired generators whose passive trajectory distributions match while their interventional responses differ; matrix games first, then MPE/Overcooked/SMAC-lite.
- **Metrics:** source calibration, interventional log loss, dynamic regret, exploitability, team welfare, and harmful-shaping rate.
- **Mandatory baselines:** stationary policy; sliding-window/change-point learner; LeMOL/MBOM-style predictor; SOM; robust policy; opponent-shaping policy; source oracle; equal intervention budget.
- **Decisive falsifier:** passive prediction quality or a generic change-point statistic selects the correct response as well as source inference; interventions add no held-out control benefit.

### Five objections and responses

1. **Objection:** This is ordinary system identification with a renamed latent variable.  
   **Response:** prove two passive-observation-equivalent games that require opposite optimal actions because only one peer responds causally to ego. If that construction fails, reject the project.
2. **Objection:** SOM already uses structural causal models for opponents.  
   **Response:** compare directly; claim only source attribution and intervention selection, not causal opponent modeling in general.
3. **Objection:** Random interventions make the problem easy and unsafe.  
   **Response:** bound an explicit intervention budget/cost and include safe, observational-only, and oracle policies.
4. **Objection:** The latent source classes are artificial.  
   **Response:** instantiate each class with the same peer policy family under environment shocks, independent learning, and meta-gradient/response learning; verify observational overlap empirically.
5. **Objection:** Better control may come from extra exploration rather than correct attribution.  
   **Response:** match interventions exactly and permute inferred source labels. Improvement must track attribution correctness on held-out generators.

**Verdict:** strongest candidate. It has a clear impossibility result, a minimal controlled test, and an algorithmic consequence.

## 2. Identifiability and selective probing in offline ad-hoc teamwork

### Contribution and significance

**Question.** When does a fixed multi-team dataset identify a policy that coordinates with a new teammate, and when should the ego agent abstain or buy limited online probes?

[TAGET](https://proceedings.mlr.press/v267/zhang25h.html), [ComaDICE](https://proceedings.iclr.cc/paper_files/paper/2025/hash/477d1531c260f9605bbf9d14d00952d4-Abstract-Conference.html), [DiTAC](https://doi.org/10.3233/FAIA251257), and Seldonian AHT establish offline coordination/adaptation methods. The proposed paper is different only if it gives teammate-shift-specific indistinguishability/coverage conditions and a calibrated selective policy—not merely another offline learner.

The problem is fundamentally multi-agent because unilateral dataset coverage does not imply coverage of states reached under a different partner policy; the support is a property of joint behavior.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** offline AHT in a POSG with a deployment teammate outside the behavior-population mixture.
- **Required result:** lower-bound pair of observationally equivalent datasets plus sufficient teammate-conditional coverage condition; scalable ambiguity proxy.
- **Environment:** tabular coordination games, LBF, Overcooked, and Hanabi with deliberately confounded teammate populations.
- **Metrics:** worst-partner return, selective risk/coverage curve, calibration of failure probability, online probes, and regret to a teammate-aware oracle.
- **Mandatory baselines:** behavior cloning; conservative offline RL; TAGET; ComaDICE; DiTAC if code is available; standard density/OOD scores; always-act/always-abstain; online AHT oracle.
- **Decisive falsifier:** standard state-action support predicts shifted-partner failure as well as the new diagnostic, or abstention does not improve selective risk at useful coverage.

### Five objections and responses

1. **Objection:** Offline-RL concentrability already says this.  
   **Response:** show a joint-policy counterexample where marginal ego coverage is identical but teammate-conditioned reachability changes the optimal action; derive the new term exactly.
2. **Objection:** The scalable proxy cannot estimate the theorem’s quantity.  
   **Response:** report proxy error against exact tabular values before neural experiments; do not imply guarantees in function approximation.
3. **Objection:** Abstention evades the task.  
   **Response:** use risk–coverage curves and charge probes/abstentions explicitly; compare total utility, not success conditional on accepted episodes.
4. **Objection:** Held-out partners are hand-designed to break baselines.  
   **Response:** preregister both constructed impossibility cases and independently trained partner populations across algorithms/seeds.
5. **Objection:** This is single-agent offline RL with context.  
   **Response:** include a reduction showing the single-agent criterion is insufficient precisely because partner actions alter transitions and reachable histories.

**Verdict:** proceed. Strong theory/empirics balance and manageable compute.

## 3. Dual-control probing of a learning teammate

### Contribution and significance

**Question.** How should an ad-hoc agent probe an unfamiliar teammate when the probe also teaches, anchors, or changes that teammate?

[Team Probing](https://ieeexplore.ieee.org/document/10988880) treats probing as identification; [Meta-MAPG](https://proceedings.mlr.press/v139/kim21g.html) differentiates through peer learning; [Fast Teammate Adaptation](https://proceedings.mlr.press/v216/zhang23a.html) handles sudden change; [Influencing Towards Stable Multi-Agent Interactions](https://arxiv.org/abs/2110.08229) deliberately stabilizes peers. The residual is not their union: it is a dual-control problem where information gain and causal displacement of an unknown learning rule are jointly valued.

Multi-agent centrality is excellent: the experiment ceases to be the same problem if peer drift is exogenous.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** Bayesian POSG over teammate policy and update-rule type.
- **Method:** influence-aware belief update and finite-horizon planner; a restricted identifiability or Bayesian-regret result.
- **Environment:** repeated coordination matrices, Overcooked, LBF; held-out Q-learning, policy-gradient, aspiration, and bounded-rational learners.
- **Metrics:** return, update-rule calibration, convention efficiency, peer-policy displacement, recovery after rule switches, regret.
- **Mandatory baselines:** no probe; stationary-type Bayes probe; Team Probing/CDP; Meta-MAPG or differentiable peer learner; influence/stabilization objective; robust/minimax AHT; rule oracle.
- **Decisive falsifier:** matched exogenous drift produces the same gains, or peer-update modeling does not beat stationary probing on held-out rules.

### Five objections and responses

1. **Objection:** This is simply opponent shaping.  
   **Response:** require uncertainty over learning rule and measure identification calibration as well as influence; shaping with a known learner is a baseline.
2. **Objection:** Learning-rule inference is unidentifiable.  
   **Response:** state the equivalence classes and prove restricted conditions; uncertainty-aware robust actions are acceptable where point identification is impossible.
3. **Objection:** The ego manipulates a cooperative teammate.  
   **Response:** include partner welfare/autonomy and harmful-displacement metrics; compare Pareto-constrained and ego-return objectives.
4. **Objection:** Results depend on toy learners.  
   **Response:** use toys for theorem validation, then held-out algorithms and hyperparameters in public domains.
5. **Objection:** More adaptation steps explain the result.  
   **Response:** exactly match interactions, compute, and horizon; vary only whether causal influence enters the belief/planner.

**Verdict:** proceed, but novelty depends on formalizing the belief–influence trade-off rather than combining two losses.

## 4. Common belief under strategic message relays

### Contribution and significance

**Question.** Under what graph and protocol conditions can agents attain enough common belief for coordinated action when intermediate relays may selectively censor, delay, or alter messages and their alignment is uncertain?

The closest lines are strategic network communication ([Incentives and the Structure of Communication](https://doi.org/10.1016/j.jet.2018.03.003)), cooperative Dec-POMDP communication ([Communication-Efficient Dec-POMDP Learning](https://arxiv.org/abs/2104.10923)), uncertain alignment ([AAMAS 2024 paper](https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p1521.pdf)), Byzantine agreement, and dynamic epistemic logic. The defensible residual is incentive-driven selective omission in stateful partial-observation coordination—not generic packet faults.

This is irreducibly multi-agent: common belief contains nested beliefs about delivery through third-party relays; a sender–receiver reduction removes the phenomenon.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** dynamic epistemic/signaling game over a network with hidden relay alignment.
- **Theory:** necessary/sufficient topology or redundancy conditions in a restricted alarm/stag-hunt case; impossibility of provenance-only certification under omission.
- **Environment:** distributed alarm, networked stag hunt, and multi-hop search/rescue with 5–50 agents.
- **Metrics:** false coordination, missed coordination, common-belief approximation error, welfare, bandwidth, and relay gain.
- **Mandatory baselines:** flooding; authenticated provenance; acknowledgements; Byzantine reliable broadcast where assumptions apply; reputation routing; redundant paths; alignment oracle.
- **Decisive falsifier:** standard Byzantine protocols solve the test at equal assumptions/cost, or nested-belief estimates do not predict action coordination beyond delivery probability.

### Five objections and responses

1. **Objection:** Byzantine reliable broadcast already solves this.  
   **Response:** state precisely which synchrony, fault-bound, authentication, and utility assumptions are absent; if a standard protocol applies unchanged, reject the paper.
2. **Objection:** Cheap-talk network theory already characterizes strategic relays.  
   **Response:** novelty must be long-horizon partial observability plus adaptive alignment inference and action consequences; cite the economic result as foundation.
3. **Objection:** Approximate common belief is not observable.  
   **Response:** define it behaviorally through coordinated-action thresholds and validate against exact finite epistemic states in small games.
4. **Objection:** Learned routing adds engineering, not science.  
   **Response:** make the theorem/topological threshold the central result; the learner only demonstrates robustness outside the solvable case.
5. **Objection:** Strategic omission is indistinguishable from loss.  
   **Response:** treat that as an explicit impossibility and use randomized challenges/interventions to establish when separation becomes possible.

**Verdict:** conditional proceed. Strong AAMAS fit, but the distributed-computing kill test must be exhaustive.

## 5. Coalition allocation with evolving private capability and coalition-only feedback

### Contribution and significance

**Question.** How should repeated complementary tasks be allocated when capability evolves through learning/fatigue, agents can misreport or withhold effort, and only coalition success is observed?

Execution-uncertainty mechanisms, adaptive task allocation ([Adaptive Task Allocation with Unknown/Evolving Capabilities](https://arxiv.org/abs/2003.03344)), strategic online allocation, truthful competence reports ([Truthful Reporting of Competence with Minimal Verification](https://arxiv.org/abs/2602.14076)), [CASH](https://proceedings.mlr.press/v305/fu25a.html), and coupled-reward MRTA each cover components. The residual survives only because coalition-only feedback jointly confounds complementarity, individual capability drift, and effort incentives.

It is fundamentally multi-agent: an individual capability is identifiable only by recombining it with other agents, and profitable effort/report deviations depend on alternative coalitions.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** dynamic combinatorial/coalition semi-bandit with latent Markov capabilities but bandit coalition outcomes and strategic effort/reporting.
- **Scope:** binary complementary skills, one explicit drift model, and either no transfers or bounded transfers—not every variant at once.
- **Theory:** identifiability conditions plus allocation and incentive regret; an impossibility result is acceptable if payment-free truthfulness fails.
- **Environment:** synthetic complementary tasks and one public robot allocation simulator; 5–30 agents.
- **Metrics:** welfare/allocation regret, capability-estimation error, manipulation gain, failure attribution, fairness, and diagnostic-coalition cost.
- **Mandatory baselines:** UCB/combinatorial bandit; cooperative adaptive MRTA; CASH descriptor oracle; Shapley credit; truthful-report mechanism; static and drift oracle.
- **Decisive falsifier:** coalition recombination offers no identification benefit, or a standard combinatorial bandit/mechanism achieves equal regret and incentive properties.

### Five objections and responses

1. **Objection:** The formulation contains four papers’ worth of complications.  
   **Response:** freeze complementarities and drift to the smallest nontrivial case; derive one impossibility/algorithm around coalition-only feedback.
2. **Objection:** Truthfulness without payments is impossible.  
   **Response:** prove the boundary, then target approximate IC under repeated diagnostic assignments or explicitly permit bounded transfers.
3. **Objection:** Coalition success cannot identify individuals.  
   **Response:** characterize rank/connectivity conditions on the coalition design matrix and show failure outside them.
4. **Objection:** Strategic under-effort is indistinguishable from fatigue.  
   **Response:** this is the core confounding; state what interventions or audits identify it and otherwise provide robust bounds, not confident labels.
5. **Objection:** Robot simulation makes incentives artificial.  
   **Response:** establish results with utility-maximizing algorithmic agents; do not rely on prompted LLM “self-interest.”

**Verdict:** conditional proceed. Excellent AAMAS centrality, but ruthless narrowing is mandatory.

## 6. Strategic teaching of an adaptive mechanism designer

### Contribution and significance

**Question.** Can participants manipulate an online mechanism’s update rule by sacrificing present utility to teach the designer a favorable future model?

Relevant foundations include [Learning Dynamic Mechanisms in Unknown Environments](https://www.jmlr.org/papers/v25/23-0159.html), [Adaptive Incentive Design with Learning Agents](https://arxiv.org/abs/2405.16716), [Learning a Game by Paying the Agents](https://arxiv.org/abs/2503.01976), [Microeconomic Foundations of Multi-Agent Learning](https://arxiv.org/abs/2601.03451), and opponent shaping. The contribution must define designer-shaping regret and give a lower bound or robust update; showing an RL agent games AI Economist is insufficient.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** repeated principal–multi-agent game with public predictable designer updates and bounded-switch learners.
- **Environment:** one family only—repeated public goods, congestion pricing, or a simple auction.
- **Metrics:** designer-shaping gain, welfare/policy regret, IC violation, cycling, adaptation speed.
- **Mandatory baselines:** fixed mechanism; standard online designer; two-timescale adaptive incentives; randomized/holdout updates; omniscient robust oracle; non-strategic learners.
- **Decisive falsifier:** history-conditioned best response in existing principal-agent theory already gives the same guarantee, or strategic agents gain no more than ordinary model misspecification.

### Five objections and responses

1. **Objection:** Strategic teaching is already contained in dynamic mechanism design.  
   **Response:** identify the exact prior solution concept and prove the new regret notion is not equivalent; otherwise kill the idea.
2. **Objection:** This is opponent shaping with the designer renamed.  
   **Response:** require population-wide incentive/welfare effects and mechanism constraints; standard shaping is a mandatory baseline.
3. **Objection:** The attacker unrealistically knows the update rule.  
   **Response:** sweep full, partial, and learned knowledge; the theorem may use full knowledge as a lower bound.
4. **Objection:** Randomization trivially fixes predictability.  
   **Response:** measure adaptation loss and prove the manipulation–adaptation trade-off, not merely add noise.
5. **Objection:** Deep bilevel RL is irreproducible.  
   **Response:** lead with small exact games and released code; deep MARL is optional validation.

**Verdict:** hold. Potentially excellent, but prior-art equivalence is the main risk.

## 7. Tracking mutually drifting communication protocols

### Contribution and significance

**Question.** Can independently trained agents maintain coordination when both latent protocols continue to change online, without paired meanings, shared natural language, or centralized gradients?

[Learning Translations/CLAP](https://arxiv.org/abs/2402.16247), [Unsupervised Translation of Emergent Communication](https://ojs.aaai.org/index.php/AAAI/article/view/34489), LangGround, and older emergent translation align fixed or anchored protocols. Recent repair/certification work—[Verifiable Semantics for Agent-to-Agent Communication](https://arxiv.org/abs/2602.16424) and [Talk Is Cheap, Communication Is Hard](https://arxiv.org/abs/2605.01750)—makes generic “repair semantic drift” crowded. The residual must be mutual online drift with a stability/tracking threshold.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** decentralized co-drifting signaling game with bounded update rates.
- **Theory:** tracking-regret or stability bound and an impossibility above a relative-drift threshold.
- **Environment:** referential game, cooperative navigation, and Hanabi-like signaling; heterogeneous architectures and asynchronous updates.
- **Metrics:** cross-play return, semantic tracking error, oscillation, recovery, and communication cost.
- **Mandatory baselines:** frozen translator; CLAP/ECTL; unsupervised translator; shared grounding; independent adaptation; semantic certification/repair; protocol oracle.
- **Decisive falsifier:** ordinary online domain adaptation matches performance, or instability is entirely eliminated by freezing one small decoder.

### Five objections and responses

1. **Objection:** This is non-stationary machine translation.  
   **Response:** require action-coupled meanings generated only through joint outcomes and show a single-agent translator lacks the needed identifiability.
2. **Objection:** Timescale separation is an obvious solution.  
   **Response:** characterize the threshold and failure modes; a heuristic schedule alone is not publishable.
3. **Objection:** Drift is injected artificially.  
   **Response:** generate it through independent policy learning and population replacement, then compare to matched exogenous symbol permutation.
4. **Objection:** Natural language solves interoperability.  
   **Response:** include it as a strong baseline and identify domains/capacities where no shared language or grounding exists.
5. **Objection:** Semantic metrics are arbitrary.  
   **Response:** prioritize intervention-defined task meanings and cross-play outcomes; representation metrics are diagnostics only.

**Verdict:** hold. Strong formal shape, but recent semantic-repair papers make the novelty margin narrow.

## 8. Reputation redemption without enabling whitewashing

### Contribution and significance

**Question.** How should a system allocate scarce low-stakes interactions to test whether a low-reputation agent genuinely changed, without giving intermittent defectors profitable reset opportunities?

[Reputation-based Partner Choice](https://arxiv.org/abs/2103.04982), [Bottom-up Reputation](https://arxiv.org/abs/2502.01971), [COOPER](https://arxiv.org/abs/2606.04359), [Skill-Conditional Trust](https://arxiv.org/abs/2606.14200), and classical whitewashing cover reputation, partner choice, task-conditional trust, and resets. The residual is the endogenous evidence loop: low reputation denies the very interactions needed to detect improvement.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** non-stationary strategic partner-selection bandit with costly diagnostic matches.
- **Theory:** lower bound on redemption delay versus whitewashing/recidivism gain; change-point audit allocation.
- **Environment:** repeated exchange/public-goods/task router with reciprocal partner choice, upgrades, sleepers, and periodic defectors.
- **Metrics:** welfare regret, time-to-redemption, false redemption, attacker gain, audit cost, and opportunity inequality.
- **Mandatory baselines:** permanent reputation; exponential decay; hard reset; sliding-window/change-point bandit; random diagnostics; skill-conditional reputation; behavior oracle.
- **Decisive falsifier:** standard non-stationary bandits solve the problem unchanged, or reciprocal selection produces no new trade-off.

### Five objections and responses

1. **Objection:** This is a non-stationary bandit with a fairness gloss.  
   **Response:** formalize reciprocal rejection and strategic recidivism; show a lower bound absent from exogenous arm drift.
2. **Objection:** “Genuine update” is unverifiable.  
   **Response:** define it behaviorally on a task distribution, not by model lineage or stated identity.
3. **Objection:** Diagnostics can be gamed by sleeper policies.  
   **Response:** include adaptive sleepers and randomized task selection; report the residual impossibility rather than promise perfect detection.
4. **Objection:** Whitewashing/Sybil literature already solves resets.  
   **Response:** distinguish identity reset from real policy improvement under retained identity; cite Sybil work as an adversary baseline.
5. **Objection:** Opportunity inequality is normative.  
   **Response:** present the welfare/security frontier and parameter sensitivity; do not hide a normative choice inside one score.

**Verdict:** hold. Feasible and AAMAS-native, but recent identity work requires careful distinction.

## 9. Receiver-side selective verification against adapting senders

### Contribution and significance

**Question.** In a repeated mixed-motive signaling game, when should a receiver verify, ignore, or act when verification is costly and the audit policy changes sender behavior?

[Adversarial Cheap Talk](https://proceedings.mlr.press/v202/lu23h.html), deception studies, [Truthful Reporting of Competence with Minimal Verification](https://arxiv.org/abs/2602.14076), [One Human, N Agents](https://arxiv.org/abs/2607.28317), and classical inspection games are dangerous prior art. The only defensible contribution is learning under partial observability with endogenous sender adaptation and an explicit welfare/audit-budget guarantee.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** verified cheap-talk Markov game with hidden, evolving sender incentives.
- **Environment:** exact signaling game plus sequential public goods/resource exchange; natural-language tasks only as validation.
- **Metrics:** welfare, deception rate, belief calibration, verification cost, and profitable sender deviation.
- **Mandatory baselines:** no/full/random audit; Bayesian trust; reputation; confidence-ranked audit; truthful-report mechanism where applicable; sender/receiver oracle.
- **Decisive falsifier:** existing inspection/mechanism solution applies directly, or random audits match the learned rule after exact budget matching.

### Five objections and responses

1. **Objection:** Inspection games solved this decades ago.  
   **Response:** perform the equivalence audit first; novelty must arise from hidden evolving types and learned partial observation, with a new bound.
2. **Objection:** The sender’s adaptation is scripted.  
   **Response:** use exact best response, no-regret learners, RL, and held-out adaptive strategies.
3. **Objection:** Truthful competence reporting already minimizes verification.  
   **Response:** distinguish competence reports from state-contingent cheap talk and compare directly in overlapping settings.
4. **Objection:** A trust score is enough.  
   **Response:** construct cases where identical historical accuracy yields different optimal audits because current continuation incentives differ.
5. **Objection:** Language-model behavior does not implement utility maximization.  
   **Response:** establish the result with algorithmic strategic agents; LLMs are secondary ecological validation only.

**Verdict:** high-risk hold. Good question, crowded mathematical neighborhood.

## 10. Distributed retraction after lossy multi-agent summarization

### Contribution and significance

**Question.** When a claim has been summarized and used by several agents to derive new beliefs, how can a correction repair affected descendants without globally replaying all private histories?

The original pitch is nearly killed by [Grounded Continuation](https://arxiv.org/abs/2605.14175), which already maintains dependency graphs and propagates retractions with formal guarantees, including multi-agent scenarios. [The Observer-Situation Lattice](https://arxiv.org/abs/2603.01407) also supplies incremental multi-perspective belief management. A residual remains only for *decentralized ownership, partial connectivity, distrust, and non-invertible cross-agent summaries*, where no central graph exists.

### Technical depth, evaluation, baselines, falsification

- **Formal object:** distributed justification graph with agent-local stores, lossy transformations, offline nodes, and trust constraints.
- **Theory:** lower bound on certificate information needed for sound targeted retraction; protocol with soundness/completeness/cost trade-off.
- **Environment:** symbolic distributed investigation first, then 3–20-agent collaborative planning with delayed corrections.
- **Metrics:** residual false belief, repair precision/recall, task recovery, communication, storage, replay cost.
- **Mandatory baselines:** full replay; source tags/deletion; Grounded Continuation centralized dependency graph; truth-maintenance system; observer-situation lattice; flooding/gossip repair.
- **Decisive falsifier:** a centralized dependency graph or ordinary distributed truth-maintenance algorithm transfers unchanged at equal assumptions and cost.

### Five objections and responses

1. **Objection:** Grounded Continuation already does exactly this.  
   **Response:** make decentralization and missing global lineage formal necessities; if its graph can simply be sharded, reject.
2. **Objection:** This is distributed-systems bookkeeping.  
   **Response:** tie certificate limits to agents’ epistemic/action correctness and strategic trust; otherwise it is not an AAMAS main-track contribution.
3. **Objection:** Lossy summaries destroy dependencies by definition.  
   **Response:** prove the minimum retained certificate and characterize unavoidable false-positive/false-negative trade-offs.
4. **Objection:** LLM extraction errors dominate the protocol.  
   **Response:** separate structural soundness from extraction faithfulness and evaluate both, as Grounded Continuation does.
5. **Objection:** Full replay is cheap enough.  
   **Response:** identify the connectivity/privacy/storage regimes where replay is impossible, not merely slower; otherwise drop the systems claim.

**Verdict:** near-kill. Retain only for one last distributed truth-maintenance audit.

## Ranked recommendation to the synthesis team

Develop no more than these five:

1. **Causal source attribution for non-stationarity.** Best combination of clean scientific question, formal impossibility, low-cost controlled experiments, and irreducible interaction.
2. **Offline AHT identifiability and selective probing.** Strongest theory-to-benchmark route; precise distinction from method-centric offline AHT.
3. **Dual-control probing of a learning teammate.** High multi-agent centrality and feasible, but needs a formal belief–influence result.
4. **Common belief under strategic relays.** Most AAMAS-native epistemic/game-theoretic candidate; proceed only after Byzantine/distributed-computing audit.
5. **Dynamic private capability with coalition-only feedback.** Strong coalition/mechanism/learning intersection; scope must be one minimal model.

Do not rescue ranks 6–10 by combining them. Combination would add scope while weakening the central claim.

## Reviewer-wide experimental requirements

- Compare against the simplest non-multi-agent or exogenous-drift reduction and demonstrate where it fails.
- Use exact small games to validate formal quantities before neural/LLM approximation.
- Match interactions, communication, verification, and compute—not just episodes.
- Separate phenomenon evidence from method improvement. A new algorithm is not evidence that the motivating phenomenon caused the gain.
- Report at least five seeds for learned policies, confidence intervals, preregistered primary metrics, and held-out partner/learner/topology families.
- Treat LLMs as one agent class, not the definition of the problem. Algorithmic best responders and simple learners are required whenever strategic incentives are claimed.
- A benchmark is test infrastructure. The paper must remain scientifically meaningful if the implementation is replaced by a small simulator.

## Final kill-test instructions

Before implementation, spend one focused week on these exact equivalence searches:

1. **Rank 1:** causal influence identification, endogenous versus exogenous non-stationarity, reflexive system identification, adaptive-opponent causal discovery.
2. **Rank 2:** offline stochastic-game concentrability, unilateral/joint coverage, offline AHT impossibility, selective offline RL under opponent shift.
3. **Rank 3:** dual control with adaptive humans/agents, machine teaching in AHT, Bayesian opponent shaping with unknown learning rules.
4. **Rank 4:** strategic reliable broadcast, rational Byzantine agreement, mediated cheap talk on networks, common p-belief under omission faults.
5. **Rank 5:** strategic combinatorial bandits with aggregate feedback, dynamic execution uncertainty, moral hazard in teams, coalition-bandit identifiability.

If an existing theorem subsumes the proposed model under a change of notation, remove the candidate rather than adding an LLM experiment.
