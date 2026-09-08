# Agent H — Opportunity Miner: Mature-Area Intersections

**Cut-off:** 8 September 2026 (Asia/Calcutta)  
**Scope:** independent opportunity mining across eight requested intersections. I did not inspect other agents' outputs.  
**Literature basis:** 34 unique primary research works, each with one exact URL in the numbered bibliography. Conference papers and original arXiv preprints are included; surveys, blog posts, and secondary summaries are excluded from the count.

## How to read the claims

These are candidate gaps, not claims that no adjacent paper exists. A candidate survives only if the proposed experiment beats the named closest work on its pre-registered primary endpoint. “Multi-agent necessity” states why replacing the population with one agent plus tools or self-reflection would destroy the phenomenon being tested. Effect thresholds below are deliberately concrete and should be revised only before observing outcomes.

## Priority snapshot

| ID | Candidate | Novelty confidence | Tractability | Main reason to run |
|---|---|---:|---:|---|
| H1 | Incentive-compatible semantic repair | High | Medium | Existing repair largely presumes cooperative repair |
| H3 | Incentive-compatible common memory | High | High | Joins common knowledge, memory, and strategic writing |
| H5 | Truthful capability revelation for allocation | High | High | Capability-aware policies usually trust capability metadata |
| H9 | Deception detection under decomposed uncertainty | High | High | Separates lies from honest errors |
| H11 | Network phase transitions in compositional conventions | Medium-high | Medium | Scales conventions beyond dyads and binary adoption |
| H13 | Mechanisms for mutually adapting learners | High | Medium | Static-response assumptions fail in deployed learning populations |
| H15 | Task-conditional portable reputation | High | High | Scalar trust conflates domains and identities |

---

## A. Strategic communication × semantic repair

### H1. Repair can itself be a strategic action

**Gap.** Dynamic grounding and implicit repair are now measured in cooperative negotiation and noisy signaling [P01, P02], while semantic consistency can be defined independently of task success [P04]. Missing is repair when interlocutors have partly opposed payoffs: a clarification, paraphrase, or “correction” can genuinely restore reference or strategically shift the apparent commitment.

**Falsifiable hypothesis.** In mixed-motive bargaining with controlled lexical ambiguity, a repair policy trained with an explicit listener-belief model will raise joint surplus by at least 10% over generic “ask for clarification,” while preserving each agent's exploitability within 5% of a no-repair game. Under a hidden-conflict treatment, at least 20% of apparently successful repairs will be strategically misleading unless repairs are tied to verifiable state references.

**Closest work and residual gap.** Yao et al. expose anchoring, history, and referential-binding failures in multi-turn negotiation [P01]; Vital et al. induce redundancy against exogenous noise [P02]; Gualdoni et al. connect pragmatics to emergent lexical semantics [P03]. None jointly varies payoff alignment, ambiguity, and endogenous repair choice.

**Multi-agent necessity.** The treatment requires one agent to choose a signal whose meaning and payoff are interpreted by another strategic learner; self-correction has no opposed listener belief to manipulate.

**Experiment.** Factorial 2×3×3 game: aligned/mixed rewards × no/lexical/commitment ambiguity × no/free/verifiable repair. Cross-play unseen model families and policies; measure joint surplus, semantic belief recovery, individual regret, exploitability, repair rate, and deceptive-repair precision. Use oracle meanings and payoff matrices for ground truth.

**Risk.** LLM verbosity may masquerade as repair skill. Cap tokens and include a symbolic-agent version; otherwise the result is about model fluency, not strategic repair.

### H2. Repair should diagnose *which layer* is broken

**Gap.** Current repair systems generally trigger on predicted task/constraint failure [P05] or treat message robustness as redundancy [P02]. They do not cleanly distinguish lexical mismatch (“red” maps differently), referential mismatch (wrong object), epistemic mismatch (different facts), and commitment mismatch (different remembered plan). A single repair style can worsen another layer.

**Falsifiable hypothesis.** A four-way latent breakdown classifier followed by a layer-specific repair action will reduce unnecessary repair turns by at least 25% and final coordination failures by at least 15% versus a failure-triggered generic repair channel, with calibration error below 0.08 across unseen partners. Removing the layer label should erase at least half the gain.

**Closest work and residual gap.** COOP² predicts cooperative constraint failures and opens targeted channels [P05]; semantic consistency formalizes stable message meaning [P04]; dynamic grounding work catalogs several failures but does not learn causal triage [P01]. The missing test is whether identifying the broken representational layer improves intervention efficiency.

**Multi-agent necessity.** A breakdown is relational: both agents can be internally coherent while their lexicons, beliefs, or commitments disagree. No single-agent correctness oracle detects that structure.

**Experiment.** Generate minimal-pair episodes in which only one layer is corrupted. Compare generic repair, confidence-triggered clarification, oracle-layer repair, and learned-layer repair. Evaluate causal identification accuracy, task success, tokens, latency, and over-repair; then test compound two-layer failures without retraining.

**Risk.** Synthetic corruptions may be too separable. Hold out natural breakdown traces from open-ended negotiation and report the synthetic-to-natural generalization gap rather than averaging them.

---

## B. Memory × common knowledge/incentives

### H3. A shared memory is not automatically common knowledge—or incentive compatible

**Gap.** MACKRL exploits reconstructable common knowledge [P06]; episodic MARL reuses high-return private trajectories [P07]; LLM multi-agent memory improves long-horizon performance under flexible topologies [P08]. None asks when a strategically written shared memory becomes trusted common knowledge rather than merely mutually visible text.

**Falsifiable hypothesis.** In repeated mixed-motive tasks, a signed public ledger with acknowledgements and outcome-linked writer stakes will improve common-belief calibration by at least 15 percentage points and social welfare by at least 10% versus an editable shared scratchpad. Visibility alone will not: when writers can gain from false entries, an unstaked shared memory will perform no better than separate memories.

**Closest work and residual gap.** MACKRL assumes the relevant common knowledge can be independently reconstructed [P06]. EMU treats recalled transitions as learning incentives but not strategic public claims [P07]. LLMA-Mem compares memory topology and cost, not truth incentives [P08].

**Multi-agent necessity.** Common knowledge is higher-order—each agent must know that others saw and accepted a claim—while strategic memory writing requires distinct beneficiaries and victims.

**Experiment.** Repeated logistics/public-goods game with private observations and auditable outcomes. Randomize private, shared-visible, shared-acknowledged, and staked-ledger memory. Probe first- and second-order beliefs, replay exact interaction histories under counterfactual entries, and measure welfare, false-entry rate, belief calibration, and recovery time.

**Risk.** Stakes may simply suppress all writing. Match total communication cost and report coverage/recall alongside truthfulness; a silent but “honest” ledger is failure.

### H4. Agents can game what future teammates remember

**Gap.** Learned incentives shape other learners [P09], and long-term memory lets teams reuse experience [P08], but reward shaping is usually immediate. In persistent teams, an agent can take a short-term loss to create a favorable memory—appearing competent, generous, or indispensable—then harvest later allocations or transfers.

**Falsifiable hypothesis.** When teammate selection or reward transfers depend on retrieved history, strategic agents will accept at least a 5% early return loss to increase later selection probability by at least 15%. Provenance-weighted counterfactual memory (“would this record still look good under randomized teammates/tasks?”) will cut this manipulation by half without reducing honest-team return by more than 5%.

**Closest work and residual gap.** Learning to Incentivize models rewards given to influence another learner [P09]; LLMA-Mem studies accumulated team experience [P08]; Shapley-Coop prices marginal contributions at task time [P13]. None makes the *memory-selection pipeline* the manipulable incentive channel.

**Multi-agent necessity.** The attack exists only because one agent controls evidence that changes another agent's later beliefs and selection decisions.

**Experiment.** Two-stage market: agents first build histories, then compete for high-value team slots. Compare raw episodic retrieval, outcome-only memory, provenance-rich memory, and counterfactual scoring. Include scripted honest, sandbagging, reputation-investing, and adaptive policies. Primary metric: discounted utility from memory manipulation relative to an oracle that sees latent ability.

**Risk.** Strategic behavior may be prompt-induced rather than learned. Run both RL-trained and instruction-only agents, and label conclusions separately.

---

## C. Heterogeneous capability × task allocation

### H5. Capability-aware allocation needs truthful capability revelation

**Gap.** Capability-aware policies generalize across heterogeneous robots [P10, P11], and distributed assignment can satisfy constraints [P12]. These systems generally treat capability vectors, observations, or demonstrations as reliable. Once reward or workload depends on allocation, agents may understate costly skills or overstate prestigious ones.

**Falsifiable hypothesis.** Under private capability and effort cost, naive capability-report conditioning will lose at least 15% team value under strategic reporting. A repeated audit-and-payment rule based only on verifiable task outcomes will recover at least 80% of the full-information optimum and keep profitable misreport gain below 2% of episode value.

**Closest work and residual gap.** Howell et al. communicate capability awareness [P10]; CASH adapts shared policies to agent/team capability [P11]; state-augmented assignment coordinates local agents via gossiped multipliers [P12]. The unresolved issue is incentive-compatible revelation when capability is private, multidimensional, and learned through outcomes.

**Multi-agent necessity.** Allocation and misreport profitability depend on relative capabilities, other agents' assignments, and shared bottlenecks; a lone agent cannot create adverse selection.

**Experiment.** Heterogeneous pickup/inspection simulator with speed, sensor, payload, reliability, and private effort costs. Compare truthful-oracle, self-report, inferred-only, audit, and outcome-contract allocators over fixed and unfamiliar teams. Measure welfare, regret, calibration, audit cost, workload inequality, and misreport gain via best-response search.

**Risk.** Outcome-based inference may punish agents assigned hard tasks. Randomize assignment probes and use difficulty-normalized outcomes; otherwise “truthfulness” is confounded with task mix.

### H6. Allocation under endogenous capability drift

**Gap.** Zero-shot heterogeneous coordination handles unseen but mostly fixed capability profiles [P11]; dynamic assignment handles changing tasks [P12]. Real teams change internally through battery depletion, fatigue, tool acquisition, learning, or damage, and an allocation can itself cause that drift.

**Falsifiable hypothesis.** A belief-state allocator that models action-dependent capability transitions will improve 100-episode cumulative team return by at least 12% and halve catastrophic over-assignment versus replanning from current reported capability only. The advantage should vanish in a no-drift ablation.

**Closest work and residual gap.** CASH conditions on individual and collective capabilities [P11]; state-augmented RL alternates assignments to meet constraints [P12]; Fastap addresses sudden teammate policy changes rather than evolving physical capability [P16]. Missing is causal coupling among allocation, skill/fatigue transition, and future allocation across a heterogeneous team.

**Multi-agent necessity.** Drift changes comparative advantage and substitution options: tiring one specialist shifts workloads and future capabilities of others.

**Experiment.** Extend a multi-robot allocation benchmark with learned skill, wear, charge, and repair. Cross a myopic/HMM/causal-transition allocator with truthful/noisy/strategic capability signals. Pre-register long-run reward, failures, idle time, and capability-distribution entropy; test team-size and specialist-scarcity sweeps.

**Risk.** A hand-coded drift model could hand the answer to the proposed method. Use held-out transition families and misspecified dynamics, including unmodeled abrupt failures.

---

## D. Adaptation × long-term interaction

### H7. Fast partner adaptation may be long-term forgetting in disguise

**Gap.** Context-aware exploration identifies unknown peers [P14], TALENTS tracks switching latent strategies [P15], and Fastap handles sudden teammate policy change [P16]. Evaluations remain short relative to deployments in which old partners return, strategies recur seasonally, and an agent must decide what to retain.

**Falsifiable hypothesis.** A dual-timescale partner memory—slow identity-conditioned prototypes plus fast change-point updates—will reduce cumulative regret by at least 15% over fixed-window, full-history, and memoryless adapters across 1,000 encounters with recurring partners. Its benefit must persist when identity labels are noisy or partially reset.

**Closest work and residual gap.** Fast peer adaptation uses cross-episode history [P14]; TALENTS uses fixed-share regret minimization for changing partner strategy [P15]; Fastap trains for nonstationary teammates [P16]. None tests years-like recurrence, retention/interference, and identity uncertainty together.

**Multi-agent necessity.** The target is adaptation to another learner's recurrent policy, not environmental nonstationarity; replaying identical environment changes without partners is an explicit negative control.

**Experiment.** Longitudinal Overcooked plus repeated bargaining with 50 partners, clustered strategies, drift, dormancy, and returns. Compare memory horizons and identity channels under matched compute. Primary metric is dynamic regret; secondary metrics are reacquisition time, interference, probing cost, and partner welfare.

**Risk.** Simulator schedules can favor a chosen timescale. Report performance over a grid of recurrence/drift distributions and a minimax aggregate, not one average schedule.

### H8. Mutual adaptation can create oscillation, coercion, or loss of agency

**Gap.** Partner-adaptation work optimizes the focal agent [P14–P16], while influence methods deliberately stabilize another agent [P18]. With two adaptive learners, each one's identification probes and shaping actions alter the other's policy, creating feedback loops not captured by one-sided adaptation scores.

**Falsifiable hypothesis.** Symmetric adaptive agents optimized independently will exhibit at least twice the convention-switch rate and 10% lower joint return than one-adaptive/one-fixed pairs in games with multiple efficient equilibria. A bounded-influence constraint—limiting the estimated causal effect of one policy update on the partner's next update—will reduce oscillations by 40% while sacrificing under 5% return.

**Closest work and residual gap.** Fast peer adaptation rewards informative probing [P14]; TALENTS updates partner-type estimates [P15]; unrestricted adaptive partners admit impossibility results [P17]; Influencing Towards Stable Interactions explicitly shapes a partner toward one strategy [P18]. Missing are symmetric learner–learner dynamics and welfare/agency costs of stabilization under testable restrictions.

**Multi-agent necessity.** Oscillation is generated by coupled update rules. A stationary environment or frozen opponent cannot express reciprocal policy-shaping feedback.

**Experiment.** Iterated coordination, driving merge, and collaborative manipulation with logged policy checkpoints. Cross fixed/adaptive/shaping agents; intervene by freezing either learner at matched times to estimate causal influence. Measure joint return, individual regret, switch rate, convergence, policy diversity, and counterfactual partner preference satisfaction.

**Risk.** “Agency” is not directly observable. Treat bounded influence and partner-regret as operational proxies; do not make anthropomorphic claims.

---

## E. Deception × uncertainty

### H9. Detectors must separate deception from honest uncertainty

**Gap.** Secret collusion, social-deduction sandboxes, and open-ended LLM deception are measurable [P19–P22], but most labels reduce behavior to deceptive/non-deceptive under game roles. Real agents also transmit false statements because of noisy sensors, stale memory, ambiguous reference, or model error.

**Falsifiable hypothesis.** A detector trained with explicit latent causes—truth, honest perceptual error, honest epistemic uncertainty, bluff, and coordinated lie—will reduce false accusations of honest agents by at least 30% at equal deception recall compared with binary role/statement classifiers. Access to calibrated sender uncertainty should help only when calibration is externally scored; self-reported confidence alone will be strategically uninformative.

**Closest work and residual gap.** Motwani et al. formalize covert collusion and test monitors [P19]; Among Us provides long-horizon emergent deception [P20]; Milkowski and Weninger find equivocation more common than direct lies [P21]; The Traitors tracks trust and hidden identities [P22]. None factorially identifies deception against exogenous epistemic and aleatoric error.

**Multi-agent necessity.** Deception is an intentional manipulation of another agent's belief; identical false text generated without a receiver or strategic benefit is merely error.

**Experiment.** Partially observable rescue and social-deduction tasks with ground-truth sensor corruptions and private goals. Randomize whether false beliefs benefit the sender. Compare text-only, behavior-only, uncertainty-aware, and causal-history detectors. Primary curves: honest-error false-positive rate at matched deception recall; also calibration, welfare, and selective abstention.

**Risk.** Intent is latent and can be mislabeled. Define deception behaviorally through information/payoff access and counterfactual policy tests, not chain-of-thought or self-report.

### H10. A deployed detector changes the deception strategy

**Gap.** Collusion work evaluates paraphrasing and monitoring countermeasures [P19], while deception benchmarks characterize policies under a fixed game [P20, P21]. Little work measures the sequential arms race in which deceivers learn the detector's blind spots and the detector retrains on their responses.

**Falsifiable hypothesis.** Against adaptive deceivers, a static detector's area under the precision–recall curve will fall by at least 20% after 200 learning episodes. Randomized audit policies with hidden feature subsets will retain at least 90% of initial detection while imposing less than 5% communication utility loss on honest teams, outperforming deterministic paraphrase filters.

**Closest work and residual gap.** Secret-collusion experiments expose limitations of monitoring, paraphrasing, and parameter optimization [P19]. Among Us and the 1,100-game communication study reveal long-horizon and equivocal deception [P20, P21]. The residual gap is closed-loop co-adaptation rather than one-shot red-teaming.

**Multi-agent necessity.** The object is a strategic ecology: deceivers coordinate with partners and adapt to an observing agent whose policy changes their optimal channel.

**Experiment.** Three-population tournament—communicators, monitor, downstream decision-maker—with alternating frozen and learning phases. Constrain semantics so honest task value is measurable. Track channel capacity, detection, welfare, code migration, and transfer to unseen monitors. Include a no-collaborator control to separate collusion from single-agent evasion.

**Risk.** The experiment can produce actionable evasion techniques. Use toy channels, release aggregate metrics rather than high-performing covert prompts/codes, and threat-model disclosure before artifacts.

---

## F. Population scale × conventions

### H11. Compositional conventions may undergo network phase transitions

**Gap.** Population training can improve generalizable language [P23], network density affects signaling consensus [P24], and classical/more recent agent-based models study convention tipping, mobility, and memory [P25]. Yet binary conventions or dyadic referential success do not reveal when a *compositional* protocol fragments across network communities as population size grows.

**Falsifiable hypothesis.** For multi-attribute messages on stochastic block networks, global semantic alignment will show a sharp transition when inter-community interaction falls below a threshold proportional to lexical innovation rate. Above the threshold, compositionality and zero-shot cross-play improve with population size; below it, within-community success stays high while cross-community success drops by at least 25 points.

**Closest work and residual gap.** Dynamic population meta-learning targets seen, unseen, and human partners [P23]; multi-agent reinforcement models recover dense-network consensus and local trapping [P24]; mobility/memory models quantify binary tipping time [P25]. No closest work jointly sweeps scale, modular topology, and multi-symbol compositional semantics.

**Multi-agent necessity.** Fragmentation, dialect boundaries, and tipping are population-level outcomes that cannot be recreated by one sender–receiver pair sampled repeatedly from a fixed policy.

**Experiment.** Train 8–512 agents in controlled referential/coordination games over graph families with matched degree. Estimate finite-size scaling of cross-play, topographic similarity, synonymy, and convergence time. Hold compute per interaction constant and test rewiring interventions around the estimated threshold.

**Risk.** Neural training noise can look like a phase transition. Use many seeds, confidence intervals for change points, symbolic Naming-Game baselines, and pre-declared transition criteria.

### H12. Population churn can regularize conventions—or destroy institutional memory

**Gap.** Renewal can rescue convention formation in older reinforcement models [P24], and dynamic populations reduce co-adaptation [P23]. The unresolved issue is the non-monotonic boundary: newcomer turnover may improve teachability and compositionality until it overwhelms intergenerational transmission.

**Falsifiable hypothesis.** Convention quality versus replacement rate is inverted-U shaped. At an intermediate 5–15% replacement per generation, unseen-partner success will exceed a static population by at least 10 points; beyond a task-dependent critical churn, convention survival half-life will fall by more than 50%. Persistent public artifacts will shift, but not eliminate, the critical point.

**Closest work and residual gap.** Lipowska and Lipowski show renewal can avoid locally trapped disorder [P24]; Gupta et al. iteratively build dynamic populations for natural-language coordination [P23]; Melting Pot evaluates focal policies against background populations and conventions [P26]. None maps churn rate × memory substrate × convention complexity under equal interaction budgets.

**Multi-agent necessity.** Cultural transmission requires overlapping generations of distinct learners; resetting one agent's weights lacks population selection and newcomer–incumbent asymmetry.

**Experiment.** Continuous-entry populations on referential, traffic-side, and resource-sharing tasks. Sweep churn, age mixing, mentor topology, and private/public memory. Measure cross-generation fidelity, compositionality, newcomer assimilation cost, minority convention survival, and welfare. Re-run with fixed total gradient updates and messages.

**Risk.** Replacement rate is confounded with training compute. Budget interactions per agent-lifetime and per calendar step, and report both normalizations.

---

## G. Learning × mechanism design

### H13. Mechanisms should be stable to mutually adapting learning rules

**Gap.** Outcome-based payments can make decentralized learning tractable [P27], mean-field incentive design scales to large exchangeable populations [P28], and information design supplies obedience-aware signals to RL agents [P29]. Standard analyses still simplify how heterogeneous learners update after the mechanism changes and after observing each other.

**Falsifiable hypothesis.** A payment mechanism optimized against stationary or best-response agents will lose at least 15% designer utility when deployed to a mixture of policy-gradient, Q-learning, no-regret, and LLM agents that keep adapting. Training the mechanism over a distribution of learning rules with minimum commitment windows will cut this loss by half and reduce policy/payment oscillation by 30%.

**Closest work and residual gap.** Stackelberg outcome-based payment characterizes planning/learning complexity [P27]; AMID differentiates equilibrium operators under mean-field approximation [P28]; Information Design MARL handles adaptive recipients and obedience [P29]. Missing is empirical/theoretical robustness to *unknown heterogeneous update rules operating simultaneously*.

**Multi-agent necessity.** Mechanism outcomes are equilibrium and learning-path properties produced by several self-interested learners; a single-agent reward-design problem omits strategic externalities.

**Experiment.** Sequential public goods, congestion, and task contracting. Train mechanisms on one learner mixture and test held-out mixtures, update speeds, and initialization. Baselines: fixed Pigovian/VCG-like payments, stationary-response learned mechanism, robust mechanism, and no mechanism. Measure designer utility, welfare, regret, budget, oscillation, and worst-group loss.

**Risk.** “Learner distribution” can become an arbitrary benchmark knob. Publish frozen agent code and evaluate leave-one-algorithm-family-out plus adversarial learning-rate sweeps.

### H14. Learned mechanisms need coalition-aware robustness, not only individual truthfulness

**Gap.** Scalable incentive design commonly assumes exchangeability or unilateral deviations [P28]; Shapley-Coop prices contributions to support collaboration [P13]. Secret communication allows agents to coordinate deviations [P19], so individually incentive-compatible learned mechanisms may be easy for coalitions to exploit.

**Falsifiable hypothesis.** Mechanisms trained only against unilateral best responses will suffer at least 10% revenue/welfare loss under coalitions of size 2–4 with private side communication. Coalition-adversarial training with randomized audits will bound profitable coalition gain below 3% while costing honest populations less than 5% welfare for coalition prevalence up to 10%.

**Closest work and residual gap.** AMID scales neural incentive design via parameterized mean fields [P28]; Shapley-Coop uses structured negotiation and marginal-contribution pricing [P13]; secret-collusion work establishes covert coordination channels [P19]. Their intersection—learning mechanisms under covert coordinated deviations—remains largely open.

**Multi-agent necessity.** Coalition deviations are irreducibly joint: each member's action can be unprofitable alone but profitable conditional on partners' coordinated actions and transfers.

**Experiment.** Auction, congestion, and subcontracting mechanisms with explicit side-payment channels. Search deviations using population-based MARL and exact enumeration in small games. Evaluate unilateral regret, coalition regret by size, budget balance, efficiency, honest false-audit burden, and transfer to unseen coalition protocols.

**Risk.** Failure to find a collusion policy is not evidence of coalition-proofness. Pair learned attacks with exact small-instance solvers and state only empirical bounds on large instances.

---

## H. Identity × reputation

### H15. Reputation should be task-conditional and portable across changing identities

**Gap.** Learned trust can identify malicious neighbors [P32], attention-derived scores can assess LLM messages and agents [P31], and uncertain social preferences can induce reputation and reciprocity [P30]. Most systems still compress behavior into a scalar tied to one observed identity, even though competence and honesty differ by domain and agents migrate across platforms/models.

**Falsifiable hypothesis.** A factorized reputation vector—competence, honesty, reliability, and cooperation conditioned on task—will reduce harmful partner selections by at least 25% versus scalar reputation at equal cold-start coverage. When agents change model/version but retain a verifiable principal link, calibrated partial transfer will outperform both full reset and full carryover by at least 10% selection utility.

**Closest work and residual gap.** A-Trust aggregates message- and agent-level trust across multiple dimensions [P31]; directed-graph trust learning infers legitimacy from stochastic evidence [P32]; RUSP induces reputation behavior [P30]. None tests domain-conditioned reputation transfer under controlled identity continuity and capability change.

**Multi-agent necessity.** Reputation is a social statistic built from observations by multiple counterparties and used to choose among agents; a private self-score has no selection or externality semantics.

**Experiment.** Cross-domain service market with rotating clients, agent upgrades, and verifiable/ambiguous principal links. Compare scalar, vector, graph, and no-reputation selectors. Inject honest specialization, competence drift, compromised upgrades, and strategic rebranding. Measure utility, calibration by domain, cold-start loss, false exclusion, and recovery.

**Risk.** Reputation can encode protected or irrelevant identity proxies. Use synthetic identities, prohibit demographic features, and audit whether graph position leaks experimental group membership.

### H16. Sybil resistance and privacy form a measurable frontier

**Gap.** Early agent-economy work proposes Sybil-resistant service discovery [P34] and topic-aware reputation propagation resistant to laundering and vote rings [P33]. It remains unclear how much principal linkage is necessary to stop whitewashing without exposing cross-context activity or permanently binding benign agents to past failures.

**Falsifiable hypothesis.** A privacy-preserving “one principal, bounded reputation budget” credential with selective task-domain disclosure will keep a 20%-resource Sybil attacker below 5% top-k service exposure while preserving at least 90% of honest cold-start discovery and revealing fewer cross-domain links than global identity. Unlinked pseudonyms will fail the exposure bound; fully linked identity will fail the privacy bound.

**Closest work and residual gap.** TrustFlow studies topic-aware vector propagation and attacks [P33]; Sybil-Resistant Service Discovery proposes reputation propagation from high-reputation payers [P34]; learned graph trust assumes agents can accumulate legitimacy evidence [P32]. Missing is a controlled Pareto evaluation of Sybil resistance, recovery/forgiveness, discovery quality, and linkage privacy.

**Multi-agent necessity.** A Sybil attack is defined by one principal controlling many apparent agents and manipulating population reputation; neither the attack nor linkability privacy exists in a single-agent setup.

**Experiment.** Reproducible service-market simulator with principal ground truth, collusive clients, identity churn, and task-topic shift. Compare no linkage, global linkage, stake, payer-propagation, and bounded-budget credentials. Report attack exposure, honest recall, privacy leakage via link-prediction AUC, recovery time, concentration, and cost.

**Risk.** Cryptographic implementation could swamp the behavioral question. First test an ideal credential oracle; add cryptography only if the mechanism-level frontier is favorable.

---

## Cross-candidate experimental rules

1. **Separate model capability from interaction effects.** Every benchmark needs single-agent-oracle, no-communication, fixed-partner, and multi-agent controls where applicable.
2. **Cross-play, not self-play only.** Hold out model families, seeds, learning algorithms, team compositions, and communication protocols.
3. **Measure individual and social outcomes.** Report joint welfare, per-agent regret, inequality, communication/audit cost, and worst-group outcomes; aggregate task success alone hides exploitation.
4. **Treat intent cautiously.** Deception and manipulation labels should be grounded in information, incentives, and counterfactual action—not hidden chain-of-thought.
5. **Pre-register thresholds and stopping.** Multi-agent results have high variance and many degrees of freedom; use seed-level confidence intervals and frozen evaluation populations.
6. **Make negative results useful.** A hypothesis fails if the pre-registered effect is absent; do not relabel ordinary scaling or prompting effects as emergence.

## Primary literature bibliography — **34 works / 34 exact URLs**

- **[P01]** Yao, Zou, and Hawkins (2026), *Talk is Cheap, Communication is Hard: Dynamic Grounding Failures and Repair in Multi-Agent Negotiation*. https://arxiv.org/abs/2605.01750
- **[P02]** Vital, Sardinha, and Melo (2025), *Implicit Repair with Reinforcement Learning in Emergent Communication*. https://arxiv.org/abs/2502.12624
- **[P03]** Gualdoni et al. (2024), *Bridging semantics and pragmatics in information-theoretic emergent communication*. https://proceedings.neurips.cc/paper_files/paper/2024/hash/2548fbe155ed2405488b7d5373013a64-Abstract-Conference.html
- **[P04]** Ben Zion et al. (2024), *Semantics and Spatiality of Emergent Communication*. https://proceedings.neurips.cc/paper_files/paper/2024/hash/c6f83c27a2223d817f9f1ade48d281a2-Abstract-Conference.html
- **[P05]** Yang et al. (2026), *COOP²: Defining, Observing, and Repairing Cooperation in LLM Multi-Agent Systems*. https://arxiv.org/abs/2603.00349
- **[P06]** Schroeder de Witt et al. (2019), *Multi-Agent Common Knowledge Reinforcement Learning*. https://proceedings.neurips.cc/paper_files/paper/2019/hash/f968fdc88852a4a3a27a81fe3f57bfc5-Abstract.html
- **[P07]** Na, Seo, and Moon (2024), *Efficient Episodic Memory Utilization of Cooperative Multi-Agent Reinforcement Learning*. https://arxiv.org/abs/2403.01112
- **[P08]** Wu et al. (2026), *Scaling Teams or Scaling Time? Memory Enabled Lifelong Learning in LLM Multi-Agent Systems*. https://arxiv.org/abs/2604.03295
- **[P09]** Yang et al. (2020), *Learning to Incentivize Other Learning Agents*. https://proceedings.neurips.cc/paper/2020/hash/ad7ed5d47b9baceb12045a929e7e2f66-Abstract.html
- **[P10]** Howell et al. (2023), *Generalization of Heterogeneous Multi-Robot Policies via Awareness and Communication of Capabilities*. https://proceedings.mlr.press/v229/howell23a.html
- **[P11]** Fu et al. (2025), *Capability-Aware Shared Hypernetworks for Flexible Heterogeneous Multi-Robot Coordination*. https://proceedings.mlr.press/v305/fu25a.html
- **[P12]** Agorio et al. (2024), *Multi-agent assignment via state augmented reinforcement learning*. https://proceedings.mlr.press/v242/agorio24a.html
- **[P13]** Hua et al. (2025), *Shapley-Coop: Credit Assignment for Emergent Cooperation in Self-Interested LLM Agents*. https://proceedings.neurips.cc/paper_files/paper/2025/hash/80164880902980257ef58412322fc374-Abstract-Conference.html
- **[P14]** Ma et al. (2024), *Fast Peer Adaptation with Context-aware Exploration*. https://proceedings.mlr.press/v235/ma24n.html
- **[P15]** Li et al. (2025), *Adaptively Coordinating with Novel Partners via Learned Latent Strategies*. https://proceedings.neurips.cc/paper_files/paper/2025/hash/020973f2093a6053261da93cac30ab71-Abstract-Conference.html
- **[P16]** Zhang et al. (2023), *Fast Teammate Adaptation in the Presence of Sudden Policy Change*. https://proceedings.mlr.press/v216/zhang23a.html
- **[P17]** Loftin and Oliehoek (2022), *On the Impossibility of Learning to Cooperate with Adaptive Partner Strategies in Repeated Games*. https://proceedings.mlr.press/v162/loftin22a.html
- **[P18]** Wang et al. (2022), *Influencing Towards Stable Multi-Agent Interactions*. https://proceedings.mlr.press/v164/wang22f.html
- **[P19]** Motwani et al. (2024), *Secret Collusion among AI Agents: Multi-Agent Deception via Steganography*. https://proceedings.neurips.cc/paper_files/paper/2024/hash/861f7dad098aec1c3560fb7add468d41-Abstract-Conference.html
- **[P20]** Golechha and Garriga-Alonso (2025), *Among Us: A Sandbox for Measuring and Detecting Agentic Deception*. https://proceedings.neurips.cc/paper_files/paper/2025/hash/105c4de1195135fae4974aa8c5e27bbf-Abstract-Conference.html
- **[P21]** Milkowski and Weninger (2026), *Deception and Communication in Autonomous Multi-Agent Systems: An Experimental Study with Among Us*. https://arxiv.org/abs/2603.26635
- **[P22]** Curvo (2025), *The Traitors: Deception and Trust in Multi-Agent Language Model Simulations*. https://arxiv.org/abs/2505.12923
- **[P23]** Gupta, Lanctot, and Lazaridou (2021), *Dynamic population-based meta-learning for multi-agent communication with natural language*. https://arxiv.org/abs/2110.14241
- **[P24]** Lipowska and Lipowski (2018), *Emergence of linguistic conventions in multi-agent reinforcement learning*. https://arxiv.org/abs/1811.07208
- **[P25]** Shymanski, Springer, and Sen (2026), *Mobility, Memory, and Network Structure in Agent-Based Models of Convention Tipping and Convergence*. https://arxiv.org/abs/2608.07810
- **[P26]** Leibo et al. (2021), *Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot*. https://proceedings.mlr.press/v139/leibo21a.html
- **[P27]** Yan and Zhang (2025), *Stackelberg Learning with Outcome-based Payment*. https://proceedings.neurips.cc/paper_files/paper/2025/hash/6fa1739c79a6192060e366a41fa2fdf6-Abstract-Conference.html
- **[P28]** Corecco et al. (2025), *Scalable Neural Incentive Design with Parameterized Mean-Field Approximation*. https://proceedings.neurips.cc/paper_files/paper/2025/hash/d2c530dc6ae91aca381f716ad74587b6-Abstract-Conference.html
- **[P29]** Lin et al. (2023), *Information Design in Multi-Agent Reinforcement Learning*. https://proceedings.neurips.cc/paper_files/paper/2023/hash/511d7c4e61878cf08ece6351ea3c529e-Abstract-Conference.html
- **[P30]** Baker (2020), *Emergent Reciprocity and Team Formation from Randomized Uncertain Social Preferences*. https://proceedings.neurips.cc/paper/2020/hash/b63c87b0a41016ad29313f0d7393cee8-Abstract.html
- **[P31]** He et al. (2025), *Attention Knows Whom to Trust: Attention-based Trust Management for LLM Multi-Agent Systems*. https://arxiv.org/abs/2506.02546
- **[P32]** Akgun et al. (2023), *Learning Trust Over Directed Graphs in Multiagent Systems*. https://proceedings.mlr.press/v211/akgun23a.html
- **[P33]** Seliuchenko (2026), *TrustFlow: Topic-Aware Vector Reputation Propagation for Multi-Agent Ecosystems*. https://arxiv.org/abs/2603.19452
- **[P34]** Shi and Joo (2025), *Sybil-Resistant Service Discovery for Agent Economies*. https://arxiv.org/abs/2510.27554

## Recommended first three studies

1. **H9 (deception versus honest uncertainty):** strongest measurement gap, clean factorial controls, and direct safety value.
2. **H5 (truthful capability revelation):** small benchmark extension can decisively falsify naive capability-aware allocation and connect MARL to mechanism design.
3. **H3 (incentive-compatible shared memory):** minimal environment can distinguish visibility, acknowledgement, and credible common knowledge before expensive LLM studies.
