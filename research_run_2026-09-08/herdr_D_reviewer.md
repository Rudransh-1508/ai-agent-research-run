# Agent D: skeptical AAMAS main-track review

**Review date:** 8 September 2026  
**Scope:** I read the eight existing specifications/surveys under `research_specs/` and did not read any files produced by the other agents in `research_run_2026-09-08/`. I independently checked the primary paper pages listed below live.  
**Standard:** AAMAS main track, not “interesting workshop idea.” I reject papers whose contribution is mainly combining adjacent papers, wrapping an existing benchmark, or engineering a new harness.

## Bottom line

**No candidate is an unconditional main-track accept today.** The best conditional bet is **sanctioning under unreliable blame**, but its current novelty statement is false in generic form. Pippin and Christensen (2012) already show a noisy-label regime (about 75% accuracy in their setting) below which social-norm/reputation sanctions hurt cooperators relative to a naive strategy. Classical sanctioning-reputation work also studies imperfect monitoring and truthful feedback. The candidate is viable only after narrowing to a new result:

> In collaborative LLM teams, empirically estimated, role-dependent attribution errors can invert the competence ordering induced by reputation, and an uncertainty-aware sanction rule prevents that inversion.

That is stronger and more specific than “there is an accuracy threshold.” It also makes the real attribution kernel, not the simulator, load-bearing.

My ordering is:

1. **Sanctioning under unreliable blame — conditional proceed.** Kill it immediately if the structured-error inversion is already in classical trust/reputation work or does not appear in real Who&When/Who&When Pro outputs.
2. **Teammate evolution invalidates shared experience — pilot only.** Clean multi-agent necessity and a real empty-looking intersection, but the claimed intervention may collapse to a recency heuristic and the proposed evaluation is expensive and harness-sensitive.
3. **Strategic contribution to a persistent experience commons — pilot only.** AAMAS-native mechanism design, but behavioral incentive validity and prior public-goods occupancy are serious risks.
4. **Dec-POMDP optimum-grounded LLM teams — Findings/evaluation track unless the policy-synthesis result becomes algorithmic.** Exact decentralized regret is useful, but most ingredients are established and the current “method” is solver plus LLM repair.

STAV, incentive-compatible escalation, peer policy sanctioning, skill contagion, and the proposed candidate combinations should not be selected for this deadline.

## Triage of 13 candidate families

Scores are skeptical 1–5 judgments. “MA” asks whether more than one autonomous decision-maker is scientifically necessary, not merely present in the implementation.

| # | Candidate family | Contribution | MA | Novelty | Depth | Evaluation and required baselines | Decisive falsifier | Verdict |
|---|---|---:|---:|---:|---:|---|---|---|
| 1 | Exact decentralized-regret decomposition and LLM policy synthesis | 3 | 5 | 3 | 3 | Exact `V*_Dec`, centralized ceiling, random, JESP/local search, approximate planner, centralized LLM, independent LLMs, token-matched chat, MARL where fair; exact legality/value checks for emitted policies | No stable excess-loss pattern; rendering/syntax dominates; token-matched chat equals commitment; exact references fail | **Hold/Findings.** The comparator is new for LLM teams, but optimum grounding, central ceilings, Dec-POMDP notation, and counterexample-guided controller repair all have close prior art. Main track needs a new synthesis or repair algorithm, not a benchmark plus prompt protocol. |
| 2 | STAV: fitted trust law plus delayed stability controller | 3 | 4 | 2 | 4 | Memoryful vs reset identification; memoryless/EWMA/Beta/asymmetric/hysteresis models; fixed/random/periodic audit, rate limit, clipping, floor, oracle; exact cost matching and held-out transition prediction | No behavioral history effect; fitted parameters never enter unstable region; rate limiter matches STAV; grounded truth removes effect | **Reject as a combination.** Chen supplies costly-verification behavior, Itkin supplies delayed-instability theory and corrector placement, classical control supplies projection/certification. The four-stage chain is too much for four weeks and its novelty is mostly coupling existing pieces. |
| 3 | Sanctioning under unreliable blame | 4 | 5 | 3 | 5 | No sanction, matched random exclusion, oracle blame, each real attributor, direct-observation RepuNet-style upper bound, uncertainty/abstention rule; sweep team size, severity, error bias, and team formation; validate on Who&When and Pro plus a live team | Real error kernel is near uniform; no competence inversion; blame sanctioning never loses to matched random exclusion; result vanishes outside one simulator; uncertainty rule almost always abstains | **Conditional proceed; rank 1.** Generic noise threshold is occupied by 2012 and older reputation work. Only structured attribution bias, measured on real traces and linked to a new inversion result, can carry novelty. |
| 4 | Manipulation-resistant harness-update gates | 3 | 2 | 3 | 3 | Honest vs payoff-equivalent score-seeking proposer; double-held-out set; non-regression, task-agnostic, stratified and resource-metered gates; inert-edit and planted-degradation controls | Gate pass rate tracks true gain; manipulation disappears under ordinary nested holdout; proposer condition is prompt wording, not payoff response | **Reject for this brief.** Potentially useful AI-evaluation work, but multi-agent necessity is weak and the likely contribution is a better evaluation protocol. It needs a formal manipulation result to be AAMAS main-track work. |
| 5 | Team-externality-aware harness update gates | 2 | 4 | 3 | 2 | Solo, homogeneous team, heterogeneous team; seed harness, accepted updates, matched tasks; scale team size; contention/message/file metrics | Solo and team deltas remain aligned; a small team validation set catches all regressions; effects are environment-specific contention | **Reject as engineering.** “Run accepted updates in team tests” is a sensible gate extension, not yet a research contribution. Do not combine it with family 4 to manufacture breadth. |
| 6 | Harness configuration as leaderboard manipulation/social choice | 3 | 1 | 3 | 3 | Reproduce full fragility grid; arithmetic mean, median, mean win-rate, pairwise majority; admissible-config attack; discrimination/robustness trade-off; held-out benchmarks | Aggregation ordering is invariant; fragility weighting only erases discrimination; release lacks item-level completeness | **Reject for the stated multi-agent program.** Social choice fits AAMAS, but the LLMs are alternatives being ranked, not interacting agents. This is a clean standalone evaluation paper, not a necessary MAS paper. |
| 7 | Strategic persuader versus verifier panels | 3 | 4 | 3 | 3 | Panel sizes 1/3/5/7/9; no attack, uniform, random-budget and pivotal-targeted attacks; majority and robust aggregators; independent-evidence escalation; exact attack-budget matching | Accuracy stays monotone with panel size under targeted attack; pivotal targeting offers no advantage; simple randomized ballots defeat it | **Reject as a combination.** It splices judge persuadability, correlated-panel error, and pivotal-vote selection. Non-monotonicity would be interesting, but the mechanism is largely implied by the three sources and the expensive experiment risks being the only contribution. |
| 8 | Skill reuse as a contagion externality | 3 | 5 | 2 | 3 | No sharing, controlled reuse breadth, selfishly chosen breadth, provenance gate, quarantine; capability/containment frontier; persistent benign marker; analytic and empirical invasion threshold | No sharp invasion threshold; chosen reuse is already safe; existing quarantine dominates; persistence adds no new dynamics | **Reject as a combination and build risk.** EvoMal supplies persistence/branching, reliability-contagion supplies epidemic framing, and provenance work supplies the gate. The proposed population harness is the largest engineering burden. |
| 9 | Teammate co-evolution as endogenous memory invalidation | 4 | 5 | 4 | 4 | Frozen teammates, co-evolving teammates, matched exogenous drift; no memory, recency, provenance/churn, GLOVE-style verifier, oracle-validity; paired entry injection and held-out churn schedules | Hazard is flat in teammate changes; matched exogenous drift explains it; recency equals provenance; effect depends on one synthetic API mutation scheme | **Pilot; rank 2.** Multi-agent necessity is genuine: another learner changes the focal agent’s effective environment. Main-track depth requires a predictive hazard model and held-out policy improvement, not only measuring stale memories. |
| 10 | Sharing rate/topology as a monoculture control parameter | 3 | 5 | 2 | 3 | Sharing-rate and topology sweep; no sharing, one-shot communication, full pool; two diversity encoders; mean and best-of-population performance; diversity-preserving admission | No long-horizon crossover; diversity metrics are encoder-dependent; existing one-shot structural-coupling result predicts everything | **Reject.** “Diversity Collapse” already owns the phenomenon, and adding persistent memory/evolution is an incremental extension unless a real critical transition is derived before experiments. |
| 11 | Persistent experience commons with strategic contributors (C3/D1) | 4 | 5 | 4 | 4 | No pool, cooperative pool, neutral pool, honesty-only, flat payment, downstream-utility payment/access pricing, oracle-curated pool; vary payoffs without changing wording; measure withholding, value, pollution, welfare, and free-riding | Incentives do not change behavior; honesty prompt matches mechanism; flat and usage-based payment tie; pool never beats no-memory enough to create a meaningful commons | **Pilot; rank 3.** This is one family, not two candidates and not a C3+D1 combination. Persistent artifact quality and future reuse distinguish it from MAC-SPGG. The paper lives or dies on payoff-sensitive behavior and a nontrivial equilibrium, not on building a memory service. |
| 12 | Peer sanctioning as operational policy enforcement | 2 | 5 | 3 | 2 | No guard, centralized action guard, workflow guard, peer sanctions, hybrid; equal enforcement cost; known and held-out clauses; task success/violations frontier | Peer/hybrid regimes are dominated at equal cost; “held-out” compliance is just semantic policy inference by the same model | **Reject as engineering.** Wrapping a single-agent policy benchmark in repeated peers creates agents but not a deep model. The held-out-clause claim is especially underspecified: sanctioners cannot enforce a policy they were never given without an independent norm-learning theory. |
| 13 | Incentive-compatible escalation under scarce oversight | 3 | 5 | 2 | 4 | Random, confidence-ranked, smooth proper score, kinked reserve rule, oracle risk; fixed audit budget and repeated payoff response; adversarial and ordinary tasks | LLM reports do not respond to payoffs; smooth and kinked rules tie; random audit remains best; simulated reviewer drives result | **Reject as an explicit combination.** The proposal itself is One-Human-N-Agents plus Endogeneity of Miscalibration plus CARP-style behavioral validation. The theory paper already names AI oversight as an application. Instantiation is not enough. |

## Recommended paper: narrowed contribution and experiment

### Contribution that could clear main track

The paper must not claim the first accuracy threshold for useful sanctioning. That claim is contradicted by live-checked classical work. The defensible package is:

1. **Empirical:** estimate an agent-level attribution error kernel from real collaborative failure traces, stratified by role, trace position, activity/verbosity, and true competence.
2. **Theoretical:** characterize when a biased kernel reverses the ordering between latent competence and stationary reputation, causing matched-rate sanctioning to select worse teams than random exclusion.
3. **Method:** design the smallest uncertainty-aware sanction rule that prevents the reversal under a stated coverage/robustness assumption.
4. **Validation:** predict the welfare ordering of sanctioning regimes from an independently estimated kernel, then test it in held-out simulated populations and a small live team.

The method should be abstention or robust reputation updating only if it follows from the theory. Do not bolt on conformal prediction merely because a conformal attribution paper exists. The live paper predicts contiguous **step** sets for rollback; it does not establish an agent-level sanction set suitable for this proposal.

### Evaluation I would require

- Split traces by task/system, not random rows, so the kernel is genuinely out of distribution at test time.
- Reproduce the original Who&When attributors and include Who&When Pro or explain why its injected-error construction is unsuitable for team-level blame.
- Use a synthetic kernel only for phase diagrams. The headline location of current systems relative to the threshold must use real outputs with confidence intervals.
- Compare no sanctioning, random exclusion at an exactly matched exclusion rate, direct-observation reputation, point-blame reputation, and the proposed uncertainty-aware rule.
- Vary at least team size, sanction severity, competence heterogeneity, and error-kernel bias. Show which conclusions are invariant.
- Report both task welfare and selection validity: rank correlation with competence, innocent exclusion, culprit retention, and time to population collapse/recovery.
- Include a deliberately uniform-noise kernel as a negative control. If inversion only occurs under an invented extreme bias, reject the claim.

## Five likely reviewer objections and acceptable responses

1. **Objection: “Noisy reputation thresholds are old.”**  
   **Response:** Agree and cite them prominently. Claim only the first threshold/inversion driven by a *measured collaborative-failure attribution kernel* whose errors correlate with agent role/trace structure. If the theorem reduces to the 2012 result under renamed variables, withdraw.

2. **Objection: “The result is a simulator artifact.”**  
   **Response:** Estimate the kernel on one trace family, preregister the predicted ordering, and test it on held-out systems plus a small live routing population. Synthetic sweeps explain the mechanism but are not empirical evidence about current LLM teams.

3. **Objection: “The LLM is incidental; this is ordinary label noise.”**  
   **Response:** Show that real attributors produce structured error that a uniform-noise model cannot explain, and that this structure changes the optimal sanction policy. If ordinary symmetric noise predicts the same outcome, the LLM contribution is incidental and the paper should not be submitted in this form.

4. **Objection: “Conformal attribution does not justify sanctioning an agent.”**  
   **Response:** Correct. Either construct and validate an agent-label conformal predictor with the required exchangeability/coverage scope, or drop the conformal claim and use a calibrated abstention rule. Do not transfer a contiguous-step rollback guarantee to reputation updates.

5. **Objection: “The threshold is arbitrary because the sanction and team-formation rules are arbitrary.”**  
   **Response:** Prove qualitative monotonicity or inversion conditions for a class of soft/hard sanctions and team selectors, then show sensitivity bands. A single hand-tuned `a*` is not a contribution.

## Combination and engineering rejection register

- **Do not combine STAV with regret-grounded evaluation.** A delayed verifier inside a Dec-POMDP benchmark adds scope, not novelty.
- **Do not combine harness-gate manipulation with team-externality tests.** The latter is an ablation or deployment check, not a second contribution.
- **Do not combine C1 memory staleness with C3/D1 commons incentives.** One is endogenous non-stationarity; the other is strategic public-goods provision. Their models, falsifiers, and baselines differ.
- **Treat C3 and D1 as duplicates.** Select one mechanism and one equilibrium; do not present two names as breadth.
- **Reject D3’s three-paper splice.** A new application of an existing kinked reporting mechanism is insufficient without a new theorem forced by congestion.
- **Reject policy-enforcement wrappers and memory-service construction as contributions.** They are test infrastructure. The paper must stand if the implementation is replaced by a simpler simulator.

## Live primary-source audit

**Paper count: 23 primary papers/pages checked live.** This is not the corpus paper count; it is the number independently opened or surfaced from primary author, publisher, proceedings, or arXiv pages during this review. Survey-only neighbors not in this list were not re-verified and should not be represented as independently checked here.

1. Wang et al., *LLM Agents for Deliberative Collaboration* — https://arxiv.org/abs/2607.06157
2. Sun et al., *The Collaboration Tax* — https://arxiv.org/abs/2608.22152
3. Ao, Gao, and Simchi-Levi, *On the Reliability Limits of LLM-Based Multi-Agent Planning* — https://arxiv.org/abs/2603.26993
4. Oliehoek and Amato, *Decentralized Control of Partially Observable Markov Decision Processes* — https://people.csail.mit.edu/camato/publications/DecPOMDP-survey-final.pdf
5. Chen, *Trust Between AI Agents* — https://arxiv.org/abs/2606.14923
6. Itkin, *Delayed Verification Destabilizes Multi-Agent LLM Belief* — https://arxiv.org/abs/2606.27409
7. Sah et al., *The Verifier Tax* — https://arxiv.org/abs/2603.19328
8. Zhang et al., *Which Agent Causes Task Failures and When?* — https://arxiv.org/abs/2505.00212
9. Liu et al., *Who&When Pro* — https://arxiv.org/abs/2607.09996
10. Ren et al., *Reputation as a Solution to Cooperation Collapse in LLM-based MASs* — https://arxiv.org/abs/2505.05029
11. Feng et al., *Conformal Agent Error Attribution* — https://arxiv.org/abs/2605.06788
12. Pippin and Christensen, *Incentive Based Cooperation in Multi-Agent Auctions* — https://cdn.aaai.org/ocs/4325/4325-19492-1-PB.pdf
13. Witkowski, *Truthful Feedback for Sanctioning Reputation Mechanisms* — https://las.inf.ethz.ch/files/witkowski-uai2010.pdf
14. Ursekar et al., *HarnessOpt-Bench* — https://arxiv.org/abs/2608.06301
15. Parupudi, *There Is No Neutral Harness* — https://arxiv.org/abs/2608.21382
16. Yin and Du, *GLOVE* — https://arxiv.org/abs/2601.19249
17. Chen et al., *Diversity Collapse in Multi-Agent LLM Systems* — https://arxiv.org/abs/2604.18005
18. Cuadros et al., *Governed Collaborative Memory as Artificial Selection* — https://arxiv.org/abs/2605.04264
19. Zhang et al., *Useful Memories Become Faulty When Continuously Updated by LLMs* — https://arxiv.org/abs/2605.12978
20. Liang et al., *Everyone Contributes! Incentivizing Strategic Cooperation in Multi-LLM Systems via Sequential Public Goods Games* — https://arxiv.org/abs/2508.02076
21. Turan, *Oversight Has a Capacity* — https://arxiv.org/abs/2606.08919
22. Zavattari, Tommasi, and Prencipe, *One Human, N Agents* — https://arxiv.org/abs/2607.28317
23. Lovén and Tarkoma, *The Endogeneity of Miscalibration* — https://arxiv.org/abs/2605.07671

### Corrections and cautions from the live audit

- The generic novelty claim for sanctioning under noisy blame is not open. The 2012 auction paper already reports a harmful-noise threshold for reputation/social-norm sanctioning.
- The original Who&When paper is `2505.00212`; `2607.09996` is Who&When Pro. They should not be cited interchangeably.
- The 53.5% agent-level and 14.2% step-level figures belong to the original Who&When paper and were confirmed live.
- Conformal Agent Error Attribution’s published abstract supports contiguous trajectory-step sets and rollback. It does not, by itself, support agent-level conformal sanctioning.
- The Collaboration Tax is real and occupies the “team decentralisation loss” framing; exact decentralized optimality remains a narrower distinction.
- The Endogeneity of Miscalibration explicitly names AI oversight as an application, increasing the prior-art burden on the proposed escalation paper.
- Governed Collaborative Memory is explicitly a Viewpoint/design agenda, while Useful Memories is a single-agent consolidation study. This leaves room for a strategic persistent-memory commons, but not for an engineering-only memory-governance paper.

## Final recommendation

Run one cheap kill test before building anything: obtain or reproduce real agent-level attribution outputs on Who&When, estimate whether innocent blame is materially role/position/verbosity dependent, and simulate matched random versus blame-based exclusion using that empirical kernel. Proceed only if the competence ordering actually inverts and the result survives mild changes in team formation and sanction severity. In parallel, search the classical trust/reputation literature specifically for biased observation kernels and misclassification-driven reputation inversion.

If either check fails, switch to the C1 teammate-co-evolution pilot. Do not rescue the blame paper by adding more mechanisms, benchmarks, or engineering.
