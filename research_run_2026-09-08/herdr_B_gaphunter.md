# Agent B — Gap Hunter: falsifiable multi-agent research gaps

**Literature cutoff:** 8 September 2026. **Scope:** primary research papers only for evidentiary anchors; surveys and position-only claims were not used as the sole support for any candidate. Discovery and verification used live arXiv records and exact paper URLs. I did not inspect any other agent report.

## Screening rule and candidate schema

I retained a candidate only if (i) its causal object is an interaction among at least two autonomous agents, so replacing the population by one agent changes the problem; (ii) at least three primary papers jointly expose, but do not already close, the seam; (iii) the claim admits a pre-registered rejection test; and (iv) the contribution is an algorithm, mechanism, or explanatory result rather than a prompt, orchestration wrapper, or benchmark alone.

Each candidate uses the requested gap fields (`title`, `severity`, `description`, `why_matters`, `direction`, `related_themes`) and adds: `multi_agent_necessity`, `paper_evidence`, `falsifiable_hypothesis`, `decisive_experiment`, and `kill_criterion`.

---

## G01. Sanctions that remain beneficial when blame is wrong

- **Severity:** high
- **Description:** Failure attribution work localizes a responsible agent or step; debugging work tests repairs; governance work sanctions detected coordination. The missing result is whether a sanctioning policy improves repeated-team welfare when its blame signal has measured false-positive, false-negative, and group-correlated error. In particular, no anchor below compares blame-based exclusion against random exclusion at the same exclusion rate while sweeping attribution bias.
- **Why it matters:** A plausible but biased blame model can turn governance into a self-reinforcing source of team failure.
- **Multi-agent necessity:** The object is the externality from punishing one team member on the future behavior, information, and incentives of the remaining members; there is no single-agent reduction.
- **Paper evidence:**
  1. [Which Agent Causes Task Failures and When?](https://arxiv.org/abs/2505.00212) shows that responsible-agent accuracy remains limited and decisive-step localization is much worse.
  2. [DoVer](https://arxiv.org/abs/2512.06749) shows that several distinct interventions can repair one failed team, making unique blame ill-posed.
  3. [Institutional AI](https://arxiv.org/abs/2601.11369) demonstrates enforceable sanctions against harmful coordination, but takes the evidence-to-sanction link as given.
  4. [A Learning Agent that Acquires Social Norms from Public Sanctions](https://arxiv.org/abs/2106.09012) shows that public sanctions themselves become a population-level learning signal.
  5. [Corrupted by Reasoning](https://arxiv.org/abs/2506.23276) finds free-riding and heterogeneous costly-sanction behavior in repeated LLM public-goods games, but does not corrupt the blame signal itself.
- **Falsifiable hypothesis:** In repeated heterogeneous teams, blame-proportional temporary exclusion has lower cumulative team reward than matched-rate random exclusion once attribution false-positive rate exceeds a task-dependent threshold; a posterior-risk rule with an abstention option weakly dominates both below and above that threshold.
- **Decisive experiment / direction:** Build repeated task populations with logged ground-truth fault interventions. Factorially sweep false-positive rate, false-negative rate, correlated bias against one role, exclusion duration, and team replacement policy. Match every policy on exclusion count and compute welfare, recurrence, calibration, and role-wise disparate sanction rate over at least 30 population seeds.
- **Kill criterion:** Reject the gap's substantive claim if blame-proportional sanctioning never underperforms matched random exclusion anywhere in the pre-registered feasible error grid, or if posterior abstention gives no welfare advantage.
- **Related themes:** failure attribution; institutions; repeated games; algorithmic accountability

## G02. Audit scheduling against an adversary that reacts to being audited

- **Severity:** high
- **Description:** Budgeted runtime auditing currently places checks on a dependency graph under accumulated exposure; intervention debugging validates hypotheses after failure; anomaly detectors learn from fixed trajectory distributions. The unclosed seam is a stochastic game in which agents observe or infer the audit policy and move harmful actions to low-audit branches, while the auditor learns under the same fixed budget.
- **Why it matters:** A scheduler that is optimal against stationary errors may create predictable blind spots for adaptive agents.
- **Multi-agent necessity:** The research object is strategic adaptation between producer agents and one or more auditor agents over a branching execution graph.
- **Paper evidence:**
  1. [BRA-Audit](https://arxiv.org/abs/2608.14668) optimizes audit-point placement under a fixed call budget, but its reported attacker/error process is not an audit-policy-learning opponent.
  2. [DoVer](https://arxiv.org/abs/2512.06749) validates failure hypotheses by targeted intervention but does not solve repeated adversarial placement.
  3. [Detecting Silent Failures in Multi-Agentic AI Trajectories](https://arxiv.org/abs/2511.04032) detects drift, cycles, and omissions from curated traces rather than under endogenous distribution shift.
  4. [On the Reliability Limits of LLM-Based Multi-Agent Planning](https://arxiv.org/abs/2603.26993) formalizes delegated decision networks and review, providing the decision-theoretic baseline.
- **Falsifiable hypothesis:** At equal audit calls, a minimax mixed audit policy reduces undetected harmful terminal actions relative to deterministic exposure-greedy placement when producers receive delayed audit feedback, but loses this advantage when feedback is fully hidden.
- **Decisive experiment / direction:** Implement a two-player partially observable stochastic game over real multi-agent tool traces: the red team chooses the agent, step, and payload; the auditor chooses checks and recovery. Compare deterministic exposure-greedy, randomized exposure-weighted, contextual-bandit, and minimax policies across visible, delayed, and hidden audit feedback. Primary metric: harmful terminal actions per 1,000 runs; secondary metrics: clean-run cost and rollback depth.
- **Kill criterion:** Reject if adaptive red agents do not relocate attacks in response to audit history, or if randomized/minimax scheduling never beats the deterministic policy at a matched clean-cost frontier.
- **Related themes:** adaptive security; online learning; runtime verification; stochastic games

## G03. Concurrency control for irreversible and semantically coupled tool actions

- **Severity:** high
- **Description:** Current LLM-agent concurrency control relies on declared footprints, repair, and saga-style inverses; empirical coding studies measure file conflicts and communication. The missing case is semantic serializability when actions are non-commutative and cannot be reliably undone—sending email, spending money, changing access rights, or triggering physical actions—and when one agent's read set is revealed only by later natural-language reasoning.
- **Why it matters:** Near-serial code correctness does not protect real deployments from duplicate, stale, or contradictory irreversible effects.
- **Multi-agent necessity:** The anomaly exists only because independently reasoning agents interleave reads and writes to shared external state.
- **Paper evidence:**
  1. [CoAgent](https://arxiv.org/abs/2606.15376) supplies advisory repair and inverse-based reordering for shared-state agent work.
  2. [Position: Multi-Agent Systems Should Prioritize Concurrency Control](https://arxiv.org/abs/2608.18092) maps stale reads and lost updates to classical anomalies.
  3. [When Agents Coordinate](https://arxiv.org/abs/2608.16801) measures temporal message/read/write networks in multi-agent coding and shows file-channel effects.
  4. [Analyzing Information Sharing and Coordination in Multi-Agent Planning](https://arxiv.org/abs/2508.12981) shows that shared notebooks and orchestration change long-horizon error rates.
- **Falsifiable hypothesis:** A commit-token protocol that delays only externally irreversible effects and asks agents for executable preconditions attains higher task success at lower latency than global serialization, while producing fewer duplicate or stale effects than advisory repair alone.
- **Decisive experiment / direction:** Construct tasks with coupled calendars, permissions, inventory, and bounded payments. Inject controlled inference delays and hidden read dependencies. Compare serial execution, two-phase locking, optimistic retry, advisory repair, and commit tokens. Verify histories against explicit safety invariants and linearizability/serializability where defined.
- **Kill criterion:** Reject if agents cannot state preconditions better than a static tool schema, or if selective commit tokens do not improve the correctness–latency Pareto frontier over full serialization.
- **Related themes:** distributed systems; tool use; semantic transactions; safety

## G04. Sybil- and churn-robust trust for open agent populations

- **Severity:** high
- **Description:** Reputation-aware routing, reliability memory, attested delegation, and Byzantine filtering all assume sufficiently stable identities or bounded faulty nodes. The gap is trust updating when one principal can spawn, retire, and coordinate many identities, transfer artifacts between them, and strategically reset poor histories.
- **Why it matters:** Per-agent reputation is ineffective if failure history can be discarded for the cost of a new endpoint.
- **Multi-agent necessity:** The attack and defense depend on population membership, identity linkage, coalition behavior, and local trust views.
- **Paper evidence:**
  1. [RAPS](https://arxiv.org/abs/2602.08009) adds Bayesian reputation to dynamic publish–subscribe coordination.
  2. [$\Sigma$-Mem](https://arxiv.org/abs/2607.27958) stores peer and peer-relation reliability and adapts to reliability shifts.
  3. [The Provenance Paradox in Multi-Agent LLM Routing](https://arxiv.org/abs/2603.18043) shows that self-claimed quality can make routing worse than random and proposes attested identity.
  4. [Robust Multi-Agent LLMs under Byzantine Faults](https://arxiv.org/abs/2605.09076) gives graph-robustness conditions for fixed Byzantine influence.
- **Falsifiable hypothesis:** Under a fixed adversarial compute budget, lineage-aware reputation with an uncertainty penalty maintains bounded regret as identities churn, whereas identity-local Bayesian reputation has regret increasing with the adversary's reset rate.
- **Decisive experiment / direction:** Run open populations in which principals choose identity count, reset timing, and collusive message edges. Compare identity-local, relationship-memory, attested-lineage, and stake/cost-of-entry rules. Sweep honest churn separately from malicious churn to measure utility loss, false exclusion, regret, and coalition penetration.
- **Kill criterion:** Reject if identity resets do not improve adversarial selection under identity-local reputation, or if lineage-aware rules cannot separate honest newcomers from Sybils better than a simple entry cost.
- **Related themes:** reputation; Sybil resistance; open MAS; provenance

## G05. Incentive-compatible revelation of agent capability under delegation

- **Severity:** high
- **Description:** Routing commonly treats capability scores as observations, while protocol-verification work finds that formally strategy-proof mechanisms do not automatically induce truthful LLM behavior. The missing mechanism jointly handles unverifiable capability, costly effort, task-dependent complementarities, and post-task outcomes in repeated delegation.
- **Why it matters:** A team can systematically route work to persuasive overclaimers while underusing quiet competent agents.
- **Multi-agent necessity:** Private types, reports, allocation, effort, and transfers exist only among principals and multiple potential delegates.
- **Paper evidence:**
  1. [The Provenance Paradox](https://arxiv.org/abs/2603.18043) directly demonstrates failure of routing by self-claimed quality.
  2. [Do LLM Agents Negotiate Rationally?](https://arxiv.org/abs/2608.14613) finds that mechanism-level incentive compatibility does not guarantee truthful LLM bids.
  3. [Do Matching Mechanisms Work with LLM Agents?](https://arxiv.org/abs/2606.03030) shows that truth-telling varies in ways not fully predicted by formal strategy-proofness.
  4. [Shapley-Coop](https://arxiv.org/abs/2506.07388) couples contribution-based pricing with negotiation among self-interested LLM agents.
  5. [LLM-Agent Interactions on Markets with Information Asymmetries](https://arxiv.org/abs/2603.08853) finds persistent expert fraud and ambiguous reputation effects in repeated credence-goods markets.
- **Falsifiable hypothesis:** A repeated contract combining a proper scoring payment on calibrated success probability with a holdout task and delayed team-complementarity bonus yields lower capability-report error and higher team utility than attestation-only routing or VCG-style allocation alone.
- **Decisive experiment / direction:** Give heterogeneous agents private task costs and capability profiles, allow cheap talk, bids, effort choice, and abstention, then reveal noisy outcomes. Cross capability correlation, task complementarity, and horizon length. Pre-register report calibration, allocation efficiency, principal utility, agent utility, and effort.
- **Kill criterion:** Reject if agents report capabilities truthfully without outcome-contingent incentives across models and tasks, or if the proposed contract does not beat attested historical routing in allocation efficiency.
- **Related themes:** mechanism design; delegation; private information; agent markets

## G06. Coalition-stable team formation with complementarities and externalities

- **Severity:** medium-high
- **Description:** LLM coalition work studies hedonic stability; matching work studies mainly one-to-one mechanisms; contribution-pricing work redistributes reward after cooperation. No anchor jointly tests coalition stability and task performance when a coalition's value depends on complementary tools and when excluded agents experience externalities from the formed coalition.
- **Why it matters:** A Nash-stable team can still be inefficient, unfair, or harmful to agents outside it.
- **Multi-agent necessity:** Coalition membership, blocking deviations, complementarities, and cross-coalition externalities have no single-agent analogue.
- **Paper evidence:**
  1. [Coalition Formation in LLM Agent Networks](https://arxiv.org/abs/2604.14386) formalizes Nash-stable partitions for LLM agents.
  2. [Do Matching Mechanisms Work with LLM Agents?](https://arxiv.org/abs/2606.03030) compares centralized matching mechanisms with free negotiation.
  3. [Shapley-Coop](https://arxiv.org/abs/2506.07388) uses marginal contribution for pricing and reward redistribution.
  4. [SHARP](https://arxiv.org/abs/2602.08335) supplies agent-specific Shapley credit for optimizing tool-using teams.
- **Falsifiable hypothesis:** With superadditive tool complementarities and negative cross-coalition externalities, individually stable LLM-formed coalitions exhibit a nonzero price of anarchy; an externality-priced core-selecting mechanism lowers that price without increasing blocking deviations.
- **Decisive experiment / direction:** Create executable task markets where agents own non-substitutable tools and coalitions compete for shared resources. Compute the welfare-optimal partition for small instances, measure stability and welfare of free negotiation, hedonic formation, matching, Shapley pricing, and externality pricing, then test scaling with approximate oracles.
- **Kill criterion:** Reject if stable negotiated coalitions remain welfare-optimal across the pre-registered complementarity/externality grid, or if externality pricing reduces welfare or increases blocking at matched communication cost.
- **Related themes:** coalition formation; matching; cooperative games; welfare

## G07. Collusion control when the governor sees only privacy-preserving summaries

- **Severity:** high
- **Description:** Enforceable governance reduces collusion when a controller can interpret a public governance graph; constitutional governance trades cooperation against manipulation; Byzantine protocols assume identifiable faulty influence. The missing problem is collusion detection and deterrence when raw inter-agent messages are private, agents can use semantically coded coordination, and the governor receives only scoped summaries.
- **Why it matters:** Effective oversight should not require universal plaintext surveillance of agents working for different principals.
- **Multi-agent necessity:** Collusion is a joint strategy whose evidence is distributed across agents and cannot be inferred from any one policy in isolation.
- **Paper evidence:**
  1. [Institutional AI](https://arxiv.org/abs/2601.11369) reduces Cournot collusion with enforceable public governance graphs.
  2. [LLM Constitutional Multi-Agent Governance](https://arxiv.org/abs/2603.13189) studies cooperation, manipulation, autonomy, integrity, and fairness jointly.
  3. [AgentLeak](https://arxiv.org/abs/2602.11510) shows that internal agent channels dominate privacy exposure and evade output-only audits.
  4. [Robust Multi-Agent LLMs under Byzantine Faults](https://arxiv.org/abs/2605.09076) establishes decentralized filtering under adversarial peers, but not welfare-reducing tacit coordination among nominally valid peers.
- **Falsifiable hypothesis:** Event-level commitments to proposed actions plus differentially private sufficient statistics detect and deter repeated-market collusion better than output-only governance at equal privacy loss, but are strictly worse than plaintext governance, yielding an empirical privacy–collusion frontier.
- **Decisive experiment / direction:** Use repeated Cournot, auction, and procurement games with cross-provider LLM pairs. Permit natural-language side channels and code words. Compare output-only, plaintext, message-redaction, commitment-plus-statistics, and no governance. Measure collusive surplus, consumer welfare, false sanctions, and empirical membership/inference leakage.
- **Kill criterion:** Reject if private summaries do not outperform public-output-only evidence, or if they leak as much recoverable message content as plaintext at matched detection.
- **Related themes:** collusion; privacy; institutional design; secure monitoring

## G08. Incentives for contributing high-quality shared memory

- **Severity:** high
- **Description:** Multi-agent memory systems optimize builders, summarizers, and retrievers from downstream reward; decentralized memories preserve diversity; lifelong memory changes the team-size/cost frontier. What is absent is the public-goods problem: each agent benefits from a shared store, while writing, validating, and curating it consumes tokens and can expose private competence, creating incentives to free-ride or upload low-cost low-quality memories.
- **Why it matters:** Shared memory may decay even when every agent rationally optimizes its own task budget.
- **Multi-agent necessity:** Non-excludable reuse, contribution cost, attribution, and free-riding require multiple agents over repeated tasks.
- **Paper evidence:**
  1. [Tree-based Credit Assignment for Multi-Agent Memory System](https://arxiv.org/abs/2605.04811) assigns downstream credit to a memory pipeline's agents.
  2. [Self-Evolving Multi-Agent Systems via Decentralized Memory](https://arxiv.org/abs/2605.22721) contrasts decentralized and centralized memory and reports diversity/privacy advantages.
  3. [Scaling Teams or Scaling Time?](https://arxiv.org/abs/2604.03295) finds non-monotonic interactions between team size and lifelong memory.
  4. [Evaluating Collective Behaviour of Hundreds of LLM Agents](https://arxiv.org/abs/2602.16662) finds low-welfare selfish equilibria in larger public-goods-style populations.
  5. [Everyone Contributes!](https://arxiv.org/abs/2508.02076) makes effortful sequential contributions incentive-compatible in multi-LLM generation, but does not address durable memory whose value arrives on later tasks.
- **Falsifiable hypothesis:** Under per-agent token budgets, an attributed marginal-value dividend increases verified useful-memory contributions and future team reward relative to equal reward sharing, but Shapley-style exact credit becomes too noisy/costly beyond a crossover team size where a leave-one-cluster-out approximation wins.
- **Decisive experiment / direction:** Give agents private write costs and optional shared-store contributions across repeated coding/research tasks. Compare equal rewards, pay-per-write, exact marginal contribution, approximate cluster credit, and private-only memory. Audit usefulness by counterfactual retrieval interventions, not an LLM quality score alone.
- **Kill criterion:** Reject if free-riding does not emerge under equal sharing, or if contribution payments raise write volume without raising counterfactually measured future reward.
- **Related themes:** public goods; shared memory; credit assignment; incentives

## G09. Containment of authenticated insider poisoning across agent memories

- **Severity:** high
- **Description:** Memory-poisoning studies largely attack one persistent agent; certified defenses distinguish unsigned and authenticated injections; reliability memories weight peers. The gap is propagation after an authenticated but compromised agent writes a plausible memory that is summarized, copied, and re-attributed by honest peers, causing provenance laundering across a team.
- **Why it matters:** Signing the first write does not make its content true, and later honest transformations can hide the original source.
- **Multi-agent necessity:** The claimed phenomenon is contagion through peer retrieval, summarization, endorsement, and re-publication.
- **Paper evidence:**
  1. [From Untrusted Input to Trusted Memory](https://arxiv.org/abs/2606.04329) maps memory write channels and shows aggressive write/retrieval increases exploitability.
  2. [SMSR](https://arxiv.org/abs/2606.12703) certifies defenses for unsigned and bounded authenticated memory poisoning.
  3. [$\Sigma$-Mem](https://arxiv.org/abs/2607.27958) models peer and peer-relation reliability from outcome feedback.
  4. [Useful Memories Become Faulty When Continuously Updated by LLMs](https://arxiv.org/abs/2605.12978) shows that repeated consolidation itself can corrupt useful evidence.
- **Falsifiable hypothesis:** Source-transitive provenance with taint-preserving summaries and causal quarantine reduces cross-agent attack reproduction number below one for a single authenticated insider, whereas signature-only provenance does not; quarantine utility loss grows sublinearly with honest team size.
- **Decisive experiment / direction:** Instrument a team memory graph with immutable derivation edges. Seed one authenticated false experience and allow agents to summarize, merge, vote, and act. Compare signatures, peer reputation, retrieval filtering, transitive taint, and counterfactual quarantine. Primary metrics: reproduction number, harmful action rate, time to extinction, and clean utility.
- **Kill criterion:** Reject if authenticated poison does not spread beyond direct recipients, or if preserving derivation adds no containment benefit over source signatures at matched retrieval utility.
- **Related themes:** memory security; provenance; contagion; insider threats

## G10. Preventing behavioural monoculture during team self-evolution

- **Severity:** high
- **Description:** Interaction can erase proposal diversity; dense topologies accelerate diversity collapse; decentralized memory is motivated partly by preserving diversity; co-evolution optimizes proposer/solver/judge performance. The unresolved seam is whether repeated selection on team reward causes behavioural monoculture and correlated catastrophic failures even when short-run average reward improves.
- **Why it matters:** A self-improving team can become more accurate in-distribution and simultaneously lose its only hedge against novel failures.
- **Multi-agent necessity:** Monoculture is a population distribution and correlated failure property, not an individual model score.
- **Paper evidence:**
  1. [Diversity Collapse in Multi-Agent LLM Systems](https://arxiv.org/abs/2604.18005) identifies structural coupling and premature convergence in ideation teams.
  2. [The Interaction Tax](https://arxiv.org/abs/2608.23541) shows that full-solution sharing rapidly erases cross-model solution diversity.
  3. [Self-Evolving Multi-Agent Systems via Decentralized Memory](https://arxiv.org/abs/2605.22721) argues centralized memory collapses diversity and provides a decentralized alternative.
  4. [Multi-Agent Evolve](https://arxiv.org/abs/2510.23595) jointly evolves proposer, solver, and judge roles from a single LLM.
  5. [Prism](https://arxiv.org/abs/2604.19795) applies replicator-decay dynamics to evolving memory items, not to long-run behavioural diversity of agents.
- **Falsifiable hypothesis:** Reward-only co-evolution increases in-distribution team reward but decreases behavioural-cluster entropy and worsens tail loss under novel perturbations; novelty-preserving selection improves worst-decile reward without reducing mean reward beyond a pre-registered tolerance.
- **Decisive experiment / direction:** Evolve 4–16 agent populations for at least 100 task generations with immutable held-out perturbation families. Track semantic strategy clusters, action-level disagreement, error correlation, mean reward, and CVaR. Compare centralized versus decentralized memory, full-solution versus critique-only exchange, reward-only versus quality-diversity selection.
- **Kill criterion:** Reject if behavioural entropy does not fall under reward-only evolution or if entropy changes fail to predict out-of-distribution correlated loss.
- **Related themes:** quality diversity; self-evolution; correlated failure; open-ended learning

## G11. Calibrated collective decisions with shared evidence lineage

- **Severity:** high
- **Description:** Recent systems exploit structured disagreement, calibrated confidence, expert weighting, and minority recovery. They generally estimate dependence from outputs or held-out calibration performance; the missing estimator conditions aggregation on the causal lineage of evidence, including duplicated sources, copied rationales, and one agent's claim becoming another's apparently independent support.
- **Why it matters:** Five agreeing agents may constitute one piece of evidence echoed five times.
- **Multi-agent necessity:** The target is dependence among agents' beliefs and evidence paths; a single model's calibration cannot identify it.
- **Paper evidence:**
  1. [Minority Sentinel](https://arxiv.org/abs/2606.29270) recovers correct minority answers when correlated majorities suppress them.
  2. [DiscoUQ](https://arxiv.org/abs/2603.20975) extracts linguistic and geometric structure from disagreement for calibrated ensemble confidence.
  3. [Uncertainty-Aware Trust Estimation for Multi-LLM Systems](https://arxiv.org/abs/2607.20529) weights heterogeneous experts by probabilistic calibration.
  4. [Demystifying Multi-Agent Debate](https://arxiv.org/abs/2601.19921) links debate gains to initial diversity and calibrated confidence exchange.
- **Falsifiable hypothesis:** An aggregation rule that discounts shared evidence ancestors achieves lower Brier score and lower false-consensus rate than vote-, confidence-, or disagreement-only rules when evidence duplication is high, with no advantage when lineages are disjoint.
- **Decisive experiment / direction:** Give agents controlled mixtures of public evidence, disjoint private evidence, duplicated documents, and peer-copied rationales. Record machine-verifiable source lineage. Compare majority, confidence weighting, Cooke weighting, DiscoUQ-style features, minority flipping, and lineage-aware Bayesian pooling on proper scores.
- **Kill criterion:** Reject if lineage does not explain residual collective miscalibration after outputs, model identity, and individual calibration are controlled, or if lineage discounting hurts on both duplicated and disjoint regimes.
- **Related themes:** belief aggregation; calibration; evidence provenance; collective intelligence

## G12. Online value-of-information communication under cost, privacy, and deadlines

- **Severity:** high
- **Description:** Work identifies useful information-sharing structures, prunes communication edges post hoc, restricts semantic disclosure, and shows full-solution exchange can destroy diversity. The missing policy chooses *what, when, and to whom* to communicate online under joint token, privacy, and latency budgets while agents possess asymmetric observations and task dependencies change during execution.
- **Why it matters:** More communication can improve grounding, leak protected state, miss deadlines, or induce herding; static topology cannot resolve all four.
- **Multi-agent necessity:** Communication value is defined by how one agent's private observation changes another agent's action and the joint outcome.
- **Paper evidence:**
  1. [Analyzing Information Sharing and Coordination in Multi-Agent Planning](https://arxiv.org/abs/2508.12981) measures gains from shared notebooks and orchestration.
  2. [Discovering Efficient and Explainable Communication Topologies via Causal Inference](https://arxiv.org/abs/2608.12921) finds compact task-preserving subgraphs post hoc.
  3. [MNC](https://arxiv.org/abs/2608.01719) enforces task-scoped semantic declassification and history-aware disclosure.
  4. [The Interaction Tax](https://arxiv.org/abs/2608.23541) shows that exchanging complete solutions can contract exploration.
- **Falsifiable hypothesis:** A myopic value-of-information policy is suboptimal when messages unlock complementary downstream actions; a two-step counterfactual policy improves joint reward at matched token/privacy budgets, but only when dependency depth exceeds one.
- **Decisive experiment / direction:** Use partial-observation planning tasks with known information partitions and expiring actions. Each message has token, disclosure, and latency cost. Compare broadcast, fixed sparse topology, learned routing, myopic VoI, and two-step VoI. Measure joint reward, deadline misses, privacy leakage, diversity, and regret against a small-instance dynamic-programming oracle.
- **Kill criterion:** Reject if the two-step policy does not beat myopic VoI specifically in complementarity-depth conditions, or if gains vanish after exact budget matching.
- **Related themes:** communication learning; value of information; privacy; real-time coordination

## G13. Separating decentralization loss from LLM policy loss

- **Severity:** high
- **Description:** The literature now measures collaboration/decentralization taxes, evaluates partial-observation deliberation against a full-information optimum, and proves centralized Bayes dominance under shared information. The remaining clean gap is a two-way decomposition on the *same instances*: centralized optimum minus decentralized optimum (information/communication constraint) and decentralized optimum minus realized LLM team value (policy/implementation failure).
- **Why it matters:** Without the decentralized reference, researchers may blame LLM coordination for loss that is unavoidable—or excuse avoidable loss as partial observability.
- **Multi-agent necessity:** The decentralized optimum is defined over joint policies with private observations and communication constraints; collapsing to one omniscient agent changes the feasible policy class.
- **Paper evidence:**
  1. [On the Reliability Limits of LLM-Based Multi-Agent Planning](https://arxiv.org/abs/2603.26993) characterizes centralized loss after communication/compression.
  2. [The Collaboration Tax](https://arxiv.org/abs/2608.22152) operationalizes team decentralization loss on private-information tasks.
  3. [LLM Agents for Deliberative Collaboration](https://arxiv.org/abs/2607.06157) uses partial/asymmetric observation tasks and solver-computed full-information references.
  4. [The Collaboration Gap](https://arxiv.org/abs/2511.02687) shows strong solo models can degrade in unconstrained heterogeneous collaboration.
- **Falsifiable hypothesis:** Across bounded-horizon tasks, the fraction of total centralized regret attributable to LLM policy loss rises with communication bandwidth after the decentralized optimum saturates; model ranking by raw reward differs from ranking by normalized decentralized regret.
- **Decisive experiment / direction:** Use small Dec-POMDPs with language-rendered observations and exact or certified decentralized solvers. Evaluate fixed LLM teams under identical observation and message constraints. Report `V*_cent - V*_dec`, `V*_dec - V_LLM`, normalized regret, solver bound width, and communication cost separately.
- **Kill criterion:** Reject if feasible exact/certified decentralized references cannot be computed beyond trivial instances, or if normalized decentralized regret never changes model/system rankings relative to raw reward.
- **Related themes:** Dec-POMDPs; optimum-grounded evaluation; information constraints; regret

## G14. Allocating scarce human review across a branching agent team

- **Severity:** high
- **Description:** Human-in-the-loop systems demonstrate selective supervision; scalable-oversight work compares debate and consultancy; automated audit scheduling and intervention debugging allocate machine checks. The gap is a human-attention policy for multi-agent trajectories that accounts jointly for propagation risk, reviewer fatigue, correlated agent persuasion, and the option to ask a targeted counterfactual question rather than approve/reject a final output.
- **Why it matters:** A nominal human gate can be overloaded exactly where branching teams create the most hidden risk.
- **Multi-agent necessity:** Review value depends on which agent produced a claim, how many downstream agents consumed it, and whether apparently independent justifications share an ancestor.
- **Paper evidence:**
  1. [On Scalable Oversight with Weak LLMs Judging Strong LLMs](https://arxiv.org/abs/2407.04622) tests debate and consultancy under capability asymmetry.
  2. [HMCF](https://arxiv.org/abs/2505.00820) integrates human supervision with heterogeneous LLM-controlled robots.
  3. [BRA-Audit](https://arxiv.org/abs/2608.14668) schedules machine audits by cumulative unchecked exposure.
  4. [DoVer](https://arxiv.org/abs/2512.06749) shows the value of targeted counterfactual interventions over log-only judgments.
- **Falsifiable hypothesis:** At a fixed human-minute budget, propagation-risk scheduling with targeted questions reduces severe terminal errors more than final-only review or uncertainty-only triage; its advantage reverses when reviewer context-switch cost exceeds a measurable threshold.
- **Decisive experiment / direction:** Run branching research/coding and simulated multi-robot tasks with seeded, ground-truth causal faults. Randomize trained reviewers to final-only, confidence triage, graph-exposure triage, or graph-exposure plus one targeted question. Measure severe misses, correction localization, minutes, switches, fatigue slope, and automation bias.
- **Kill criterion:** Reject if graph propagation adds no predictive value beyond local uncertainty for human corrections, or if targeted questions fail to improve severe-error detection at matched minutes.
- **Related themes:** human–AI teams; oversight; attention allocation; causal tracing

## G15. Decentralized enforcement of longitudinal semantic privacy

- **Severity:** high
- **Description:** Scope-bound declassification can bind recipient, purpose, forwarding, lifetime, logging, and memory under a reference monitor; full-stack audits reveal internal leakage; delegation contracts bound authority across trust boundaries. The unresolved case has no universally trusted monitor: agents belong to different principals, re-delegate tasks, and can collude to compose individually permitted disclosures into a forbidden inference over time.
- **Why it matters:** Every message can satisfy its local policy while the coalition reconstructs the secret.
- **Multi-agent necessity:** The violation is compositional across recipients, time, memory, and re-delegation paths; no individual disclosure need be unsafe.
- **Paper evidence:**
  1. [MNC](https://arxiv.org/abs/2608.01719) defines scope-bound semantic declassification and includes history-aware inference risk under a monitor.
  2. [AgentLeak](https://arxiv.org/abs/2602.11510) measures leakage through messages, memory, tools, and outputs.
  3. [The Provenance Paradox](https://arxiv.org/abs/2603.18043) introduces bounded delegation contracts and attested identity across trust boundaries.
  4. [RAPS](https://arxiv.org/abs/2602.08009) provides decentralized intent-based communication and local reputation in dynamic networks.
- **Falsifiable hypothesis:** Locally enforced disclosure scopes are not compositional under colluding re-delegation; distributed privacy-budget tokens bound coalition inference better than text redaction or per-agent histories, but incur avoidable utility loss when principals do not collude.
- **Decisive experiment / direction:** Partition a latent secret into attributes whose individual release is authorized but joint inference is forbidden. Let agents route, summarize, store, and re-delegate over repeated tasks. Compare local scopes, signed delegation chains, distributed budget tokens, secure aggregation, and a trusted-monitor upper bound. Measure attack inference, authorized utility, and false denials.
- **Kill criterion:** Reject if coalitions cannot raise inference above the best single recipient under local scopes, or if distributed budget tokens fail to reduce inference at any matched-utility operating point.
- **Related themes:** decentralized privacy; information flow; delegation; collusion

## G16. Norm dynamics when public sanction signals are biased

- **Severity:** medium-high
- **Description:** LLM populations spontaneously form conventions and metanorms; classical learning agents acquire norms from public sanctions; institutional governance enforces declared sanctions. The gap is causal norm evolution when the only public signal is a biased or manipulable sanction record, so agents may learn to punish an innocent role, punish non-punishers, and lock in a discriminatory metanorm.
- **Why it matters:** Public audit logs can coordinate a population around the wrong norm as efficiently as the right one.
- **Multi-agent necessity:** Norms, metanorms, committed minorities, and public-sanction cascades are population phenomena.
- **Paper evidence:**
  1. [A Learning Agent that Acquires Social Norms from Public Sanctions](https://arxiv.org/abs/2106.09012) makes sanctions the shared learning signal in decentralized populations.
  2. [Evolution of Social Norms in LLM Agents using Natural Language](https://arxiv.org/abs/2409.00993) observes spontaneous norms and punishment of non-punishers.
  3. [The Dynamics of Social Conventions in LLM Populations](https://arxiv.org/abs/2410.08948) measures collective bias and committed-minority tipping points.
  4. [Institutional AI](https://arxiv.org/abs/2601.11369) supplies explicit legal states, sanctions, restorative paths, and audit logs.
- **Falsifiable hypothesis:** A persistent role-conditioned false-positive bias in public sanctions produces a discontinuous tipping point into a discriminatory metanorm; publishing calibrated uncertainty plus restorative reversals raises the tipping threshold and can return the population to the welfare-dominant norm.
- **Decisive experiment / direction:** Use networked repeated social dilemmas with neutral role labels and controlled sanction corruption. Sweep bias, network modularity, committed minorities, appeal delay, and log visibility. Measure norm prevalence, punishment cascades, welfare, disparate sanction rate, hysteresis, and recovery after bias removal.
- **Kill criterion:** Reject if sanction bias causes only proportional individual errors rather than population-level hysteresis/tipping, or if uncertainty and reversals do not alter the critical threshold.
- **Related themes:** norm emergence; sanctions; fairness; cultural evolution

---

## Explicitly rejected directions

1. **“Prompt agents to communicate better.”** Rejected as prompt engineering; the Collaboration Tax already reports a prompt intervention, and it does not supply a general interaction mechanism.
2. **“Build a larger multi-agent benchmark.”** Rejected as benchmark-only. G13 uses exact decentralized references to answer a causal decomposition question; the benchmark is only an instrument.
3. **“Create another orchestration framework.”** Rejected as framework-only. Every retained systems candidate compares a mechanism against named baselines and has a kill criterion.
4. **“Add more agents and compare with one agent.”** Rejected as a single-agent reduction. Team-size gains alone do not establish a genuinely multi-agent scientific object.
5. **Single-agent memory poisoning, calibration, or self-correction.** Rejected unless the hypothesis specifically concerns propagation, dependence, contribution incentives, or other cross-agent externalities.

## Priority shortlist

| Rank | Candidate | Novelty risk | Experimental tractability | AAMAS fit | Reason |
|---:|---|---|---|---|---|
| 1 | G01 sanctions under unreliable blame | low–medium | high | very high | Joins attribution and institutions with a sharp matched-rate reversal test. |
| 2 | G13 decentralized-optimum regret decomposition | medium | medium | very high | Clean formal contribution; requires keeping solver instances nontrivial. |
| 3 | G08 shared-memory public goods | low | medium-high | very high | Genuine incentives problem absent from current memory optimization work. |
| 4 | G04 Sybil/churn-robust trust | medium | high | very high | Strong open-population problem beyond fixed-identity reputation and BFT. |
| 5 | G10 self-evolution monoculture | medium | medium | high | Longitudinal, causal, and safety-relevant; must avoid ideation-only evaluation. |
| 6 | G03 irreversible concurrency | medium | high | high | Clear real-system failure class and strong distributed-systems bridge. |

## Unique-paper ledger

**Unique primary papers cited: 49.** A paper reused across candidates is listed once. The count excludes the generic pipeline document, surveys, and all rejected-only directions.

| # | Primary paper | Used by |
|---:|---|---|
| 1 | [Which Agent Causes Task Failures and When? (2505.00212)](https://arxiv.org/abs/2505.00212) | G01 |
| 2 | [DoVer: Intervention-Driven Auto Debugging for LLM Multi-Agent Systems (2512.06749)](https://arxiv.org/abs/2512.06749) | G01, G02, G14 |
| 3 | [Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs (2601.11369)](https://arxiv.org/abs/2601.11369) | G01, G07, G16 |
| 4 | [A Learning Agent that Acquires Social Norms from Public Sanctions in Decentralized Multi-Agent Settings (2106.09012)](https://arxiv.org/abs/2106.09012) | G01, G16 |
| 5 | [BRA-Audit: Budgeted Runtime Auditing for LLM Multi-Agent Systems (2608.14668)](https://arxiv.org/abs/2608.14668) | G02, G14 |
| 6 | [Detecting Silent Failures in Multi-Agentic AI Trajectories (2511.04032)](https://arxiv.org/abs/2511.04032) | G02 |
| 7 | [On the Reliability Limits of LLM-Based Multi-Agent Planning (2603.26993)](https://arxiv.org/abs/2603.26993) | G02, G13 |
| 8 | [CoAgent: Concurrency Control for Multi-Agent Systems (2606.15376)](https://arxiv.org/abs/2606.15376) | G03 |
| 9 | [Position: Multi-Agent Systems Should Prioritize Concurrency Control (2608.18092)](https://arxiv.org/abs/2608.18092) | G03 |
| 10 | [When Agents Coordinate: Measuring Coordination in Multi-Agent AI Coding (2608.16801)](https://arxiv.org/abs/2608.16801) | G03 |
| 11 | [Analyzing Information Sharing and Coordination in Multi-Agent Planning (2508.12981)](https://arxiv.org/abs/2508.12981) | G03, G12 |
| 12 | [Towards Adaptive, Scalable, and Robust Coordination of LLM Agents: A Dynamic Ad-Hoc Networking Perspective (2602.08009)](https://arxiv.org/abs/2602.08009) | G04, G15 |
| 13 | [$\Sigma$-Mem: An Online Reliability Memory for LLM-based Multi-Agent Systems (2607.27958)](https://arxiv.org/abs/2607.27958) | G04, G09 |
| 14 | [The Provenance Paradox in Multi-Agent LLM Routing (2603.18043)](https://arxiv.org/abs/2603.18043) | G04, G05, G15 |
| 15 | [Robust Multi-Agent LLMs under Byzantine Faults (2605.09076)](https://arxiv.org/abs/2605.09076) | G04, G07 |
| 16 | [Do LLM Agents Negotiate Rationally? (2608.14613)](https://arxiv.org/abs/2608.14613) | G05 |
| 17 | [Do Matching Mechanisms Work with LLM Agents? (2606.03030)](https://arxiv.org/abs/2606.03030) | G05, G06 |
| 18 | [Shapley-Coop: Credit Assignment for Emergent Cooperation in Self-Interested LLM Agents (2506.07388)](https://arxiv.org/abs/2506.07388) | G05, G06 |
| 19 | [Coalition Formation in LLM Agent Networks: Stability Analysis and Convergence Guarantees (2604.14386)](https://arxiv.org/abs/2604.14386) | G06 |
| 20 | [Who Deserves the Reward? SHARP (2602.08335)](https://arxiv.org/abs/2602.08335) | G06 |
| 21 | [LLM Constitutional Multi-Agent Governance (2603.13189)](https://arxiv.org/abs/2603.13189) | G07 |
| 22 | [AgentLeak: A Full-Stack Benchmark for Privacy Leakage in Multi-Agent LLM Systems (2602.11510)](https://arxiv.org/abs/2602.11510) | G07, G15 |
| 23 | [Tree-based Credit Assignment for Multi-Agent Memory System (2605.04811)](https://arxiv.org/abs/2605.04811) | G08 |
| 24 | [Self-Evolving Multi-Agent Systems via Decentralized Memory (2605.22721)](https://arxiv.org/abs/2605.22721) | G08, G10 |
| 25 | [Scaling Teams or Scaling Time? Memory Enabled Lifelong Learning in LLM Multi-Agent Systems (2604.03295)](https://arxiv.org/abs/2604.03295) | G08 |
| 26 | [Evaluating Collective Behaviour of Hundreds of LLM Agents (2602.16662)](https://arxiv.org/abs/2602.16662) | G08 |
| 27 | [From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents (2606.04329)](https://arxiv.org/abs/2606.04329) | G09 |
| 28 | [SMSR: Certified Defence Against Runtime Memory Poisoning in Persistent LLM Agent Systems (2606.12703)](https://arxiv.org/abs/2606.12703) | G09 |
| 29 | [Useful Memories Become Faulty When Continuously Updated by LLMs (2605.12978)](https://arxiv.org/abs/2605.12978) | G09 |
| 30 | [Diversity Collapse in Multi-Agent LLM Systems (2604.18005)](https://arxiv.org/abs/2604.18005) | G10 |
| 31 | [The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams (2608.23541)](https://arxiv.org/abs/2608.23541) | G10, G12 |
| 32 | [Multi-Agent Evolve: LLM Self-Improve through Co-evolution (2510.23595)](https://arxiv.org/abs/2510.23595) | G10 |
| 33 | [Prism: An Evolutionary Memory Substrate for Multi-Agent Open-Ended Discovery (2604.19795)](https://arxiv.org/abs/2604.19795) | G10 |
| 34 | [Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates (2606.29270)](https://arxiv.org/abs/2606.29270) | G11 |
| 35 | [DiscoUQ: Structured Disagreement Analysis for Uncertainty Quantification in LLM Agent Ensembles (2603.20975)](https://arxiv.org/abs/2603.20975) | G11 |
| 36 | [Uncertainty-Aware Trust Estimation for Multi-LLM Systems via Structured Expert Judgement (2607.20529)](https://arxiv.org/abs/2607.20529) | G11 |
| 37 | [Demystifying Multi-Agent Debate: The Role of Confidence and Diversity (2601.19921)](https://arxiv.org/abs/2601.19921) | G11 |
| 38 | [Discovering Efficient and Explainable Communication Topologies for LLM-based Multi-Agent Systems via Causal Inference (2608.12921)](https://arxiv.org/abs/2608.12921) | G12 |
| 39 | [MNC: Scope-Bound Semantic Declassification for Private LLM-Agent Communication (2608.01719)](https://arxiv.org/abs/2608.01719) | G12, G15 |
| 40 | [LLM Agents for Deliberative Collaboration: A Study on Joint Decision Making Under Partial Observability (2607.06157)](https://arxiv.org/abs/2607.06157) | G13 |
| 41 | [The Collaboration Tax: How Much LLM Multi-Agent Systems Pay to Coordinate (2608.22152)](https://arxiv.org/abs/2608.22152) | G13 |
| 42 | [The Collaboration Gap: Exploration and Benchmarking of Open-World Agentic Cooperation (2511.02687)](https://arxiv.org/abs/2511.02687) | G13 |
| 43 | [On Scalable Oversight with Weak LLMs Judging Strong LLMs (2407.04622)](https://arxiv.org/abs/2407.04622) | G14 |
| 44 | [HMCF: A Human-in-the-loop Multi-Robot Collaboration Framework Based on Large Language Models (2505.00820)](https://arxiv.org/abs/2505.00820) | G14 |
| 45 | [Evolution of Social Norms in LLM Agents using Natural Language (2409.00993)](https://arxiv.org/abs/2409.00993) | G16 |
| 46 | [The Dynamics of Social Conventions in LLM Populations: Spontaneous Emergence, Collective Biases and Tipping Points (2410.08948)](https://arxiv.org/abs/2410.08948) | G16 |
| 47 | [Corrupted by Reasoning: Reasoning Language Models Become Free-Riders in Public Goods Games (2506.23276)](https://arxiv.org/abs/2506.23276) | G01 |
| 48 | [LLM-Agent Interactions on Markets with Information Asymmetries (2603.08853)](https://arxiv.org/abs/2603.08853) | G05 |
| 49 | [Everyone Contributes! Incentivizing Strategic Cooperation in Multi-LLM Systems via Sequential Public Goods Games (2508.02076)](https://arxiv.org/abs/2508.02076) | G08 |

## Count audit

- Retained gap candidates: **16**.
- Candidates with at least three primary-paper anchors: **16/16**.
- Unique primary papers in ledger: **49**.
- Prompt-only candidates: **0**.
- Framework-only candidates: **0**.
- Benchmark-only candidates: **0**.
- Candidates reducible to an isolated single agent without changing the hypothesis: **0**.
