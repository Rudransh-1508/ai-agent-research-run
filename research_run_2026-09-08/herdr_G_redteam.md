# Agent G — red-team novelty audit

**Cutoff:** 8 September 2026, 18:30 IST  
**Role:** adversarial prior-art and construct-validity reviewer  
**Independence:** I read `research_specs/**` and primary literature only. I did **not** read `research_run_2026-09-08/agent_C_novelty_initial.md` or any other agent output.

## Bottom line

I attacked **20 candidate claims**: 16 formulations drawn from the specs (including separable method claims and one duplicate) plus 4 likely ideas of my own. Result: **6 narrow survivors, 12 kills, 2 merges as non-independent claims**.

The original flagship ordering does not survive. The generic sanctioning-threshold claim is classical prior art; STAV is mostly a single-controller problem built from occupied pieces; strategic shared-memory work is exposed to severe construct-validity failure; and several architecture ideas are ordinary distribution shift or integration testing dressed as mechanism design. The strongest remaining projects are:

1. exact optimum-grounded LLM-team evaluation on instances proven to require Dec-POMDP reasoning;
2. harness-configuration manipulation of leaderboard aggregation rules;
3. teammate-change-conditioned *entry-level* memory invalidation;
4. persistent experience pools as quality-manipulable public goods;
5. adversarial robustness of verifier panels under a fixed total persuasion budget;
6. role-structured attribution error causing reputation-rank inversion.

None is safe as originally phrased. Each survivor below has a narrower claim and an explicit kill test.

## Search ledger

### Coverage

- Read all eight Markdown sources under `research_specs/` and `_survey/`.
- Searched the official [AAMAS 2026 proceedings](https://www.ifaamas.org/Proceedings/aamas2026/forms/contents.htm), then opened the relevant official PDFs.
- Queried the arXiv API for `(all:"LLM agent" OR all:"multi-agent") AND submittedDate:[202609010000 TO 202609082359]`, sorted newest first, maximum 200 records. The newest returned submissions were dated 4 September, consistent with the arXiv release calendar at the cutoff.
- Ran targeted August/September searches for Dec-POMDPs, verifier panels, trust/verification, sanctioning/reputation, self-evolving harnesses, shared memory, contagion, diversity collapse, role specialization, model scaling, and compute-matched single-agent reductions.
- Inspected primary abstracts for all cited arXiv papers and selected full official AAMAS PDFs. Negative-search statements below mean “no exact match found in this bounded pass,” not a proof of nonexistence.

### Decision ledger

| # | Candidate attacked | Source | Verdict | Decisive red-team reason |
|---:|---|---|---|---|
| 1 | Computed `V*Dec`/`V*Cent` decomposition for LLM teams | flagship 01 | **SURVIVES, narrowed** | The Collaboration Tax is close, but does not compute the Dec-POMDP optimum and centralized ceiling on verified instances. |
| 2 | Joint-policy commitment beats extra dialogue | flagship 01 | **KILL standalone** | AAMAS 2026 symbolic guidance already varies autonomy from free reasoning to prescribed algorithms; one LLM can emit all local policies, eliminating the claimed team mechanism. |
| 3 | Solver-guided local counterexample repair | flagship 01 | **MERGE into #1** | Without a new theorem or search-efficiency result it is an implementation arm of optimum-grounded evaluation, adjacent to Planner–Coder–Critic refinement. |
| 4 | STAV endogenous delayed verification controller | flagship 02 | **KILL** | Core state is a single delayed feedback controller; delayed-verification stability is occupied, and simple floors/rate limits/fixed budget policies are stronger trivial baselines. |
| 5 | Sanctioning threshold under unreliable blame | flagship 03 / B1 | **SURVIVES only as structured-error inversion** | Generic accuracy thresholds and welfare loss from erroneous punishment are classical. Only a measured role/verbosity/position error kernel causing rank inversion remains. |
| 6 | Manipulation-resistant harness-update gate | A1 | **KILL** | “Double held out” is ordinary adaptive-overfitting control; sealed tests, replay, significance gates, and explicit harness world models already exist. Strategic prompting does not establish a game. |
| 7 | Solo-safe harness update creates team externality | A2 | **KILL as paper** | This is unit-vs-integration testing unless a nontrivial test-allocation result exists; Sep 2026 already measures convention-specific swap costs in persistent teams. |
| 8 | Harness configuration as leaderboard manipulation lever | A3 | **SURVIVES, very narrow** | The phenomenon and social-choice frame exist separately; robust aggregation against *configuration choice* is not yet evaluated in the located work. |
| 9 | Strategic persuader against verifier panels | B2 | **SURVIVES, reformulated** | Individual persuasion, correlated panels, and pivotal substitution are occupied; fixed-budget adversarial cost-to-flip across panel sizes is not. Non-monotonicity cannot be assumed. |
| 10 | Strategic skill reuse as epidemic externality | B3 | **KILL** | EVOMAL supplies self-propagation; reliability-contagion supplies the threshold; adding prompted choice of reuse rate is a thin composition with dubious behavioral validity. |
| 11 | Teammate evolution invalidates shared experience | C1 | **SURVIVES, narrowed** | Sep interchangeability work occupies convention drift, but not causal per-entry utility decay conditioned on teammate changes versus matched exogenous drift. |
| 12 | Sharing rate controls evolutionary monoculture | C2 | **KILL** | Diversity collapse, topology effects, decentralized memory’s anti-collapse motivation, and Sep debate-diversity theory occupy the result; adding a memory round index is incremental. |
| 13 | Strategic contribution quality in an experience commons | C3 | **SURVIVES, merged** | Sequential public-goods incentives are occupied, but reusable artifacts separate contribution volume from downstream value and permit persistent pollution. |
| 14 | Shared memory commons/access pricing | D1 | **MERGE into #13** | Same scientific object. Access pricing is one mechanism arm, not a second gap. |
| 15 | Peer sanctioning for operational policy compliance | D2 | **KILL** | Held-out-clause advantage is information leakage or impossibility: if peers know the clause, a central verifier can know it; if nobody knows it, compliance is unidentifiable. Formal composable controls dominate. |
| 16 | Incentive-compatible escalation to scarce human review | D3 | **KILL** | AAMAS 2026 already characterizes truthful competence reports under limited/noisy verification; cost-aware escalation is also occupied. Congestion alone is not enough novelty. |
| 17 | Own idea: compute-matched multi-agent “synergy” decomposition | own | **KILL** | Multiple 2026 studies already show strong single agents match or beat MAS under equal compute and that collaboration benefits shrink with model capability. |
| 18 | Own idea: roles create real specialization | own | **KILL** | ExRole tests manual/random/shuffled controls; Mixture of Roles compresses MAS specialization into one agent at 20× lower token cost. |
| 19 | Own idea: shared-memory authorization governance | own | **KILL** | Sep work already formalizes authorization laundering and end-to-end security-context contracts with deterministic fault injection. |
| 20 | Own idea: causal/dependency-aware multi-agent error attribution | own | **KILL** | EDGE (1 Sep) explicitly builds intervention-validated error-dependency graphs for multi-error attribution. |

**Count:** 20 attacked = 6 survivors + 12 killed + 2 merged.

## Cross-cutting attacks every survivor must answer

### 1. Hidden single-agent reduction

The default null hypothesis is that the “team” is a lossy way to spend more inference. [Single-Agent LLMs Outperform Multi-Agent Systems under equal thinking-token budgets](https://arxiv.org/abs/2604.02460) gives both an information-efficiency argument and multi-family evidence. [Capable language models can outgrow the benefits of collaboration](https://www.nature.com/articles/s42256-026-01268-y) controls prompts, tools, compute, architecture, model capability, and six benchmarks. [Mixture of Roles](https://arxiv.org/abs/2608.27338) reproduces multi-perspective role behavior in a single agent with 20× lower token cost.

Therefore every retained project must include:

- one agent given the union of legally available information;
- one agent producing all role-conditioned outputs sequentially;
- best-of-`n` or self-consistency at matched calls/tokens;
- the strongest model affordable at the same total cost;
- a check that the task truly requires distributed private information, rather than prompt partitioning.

If the multi-agent intervention loses to any of these on the claimed metric, the MAS mechanism claim dies.

### 2. Model scaling explanation

[The Collaboration Tax](https://arxiv.org/abs/2608.22152) reports monotonic tax reduction with capability, and the Nature study above finds capable models can outgrow collaboration benefits. A result on one small/open model may therefore be a temporary competence deficit, not a multi-agent law. Minimum acceptable design: three capability levels, two model families, and an interaction between intervention and independently measured base capability. Parameter count alone is not the capability axis.

### 3. Benchmark insufficiency

AAMAS 2026’s [Probing Dec-POMDP Reasoning in Cooperative MARL](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/ECCJ1033.pdf) finds reactive policies match memory-based agents in more than half of 37 scenarios and that apparent coordination often uses brittle synchronous coupling. Small classic benchmarks can also be memorized from pretraining or solved after centralized natural-language compilation. Benchmark inclusion must be earned through history-dependence, private-information, and temporal-influence diagnostics—not by the label “Dec-POMDP” or “multi-agent.”

### 4. Strategic-LLM construct validity

[When Guardrails Look Effective](https://arxiv.org/abs/2609.01519) shows that protocol asymmetry, stochastic generation noise, and non-monotone responses to profit pressure can invalidate welfare claims in LLM-agent economies. This directly attacks C3/D1, D2, D3, and any “self-interested LLM” experiment. A prompt saying “maximize score” is not evidence that the model implements a payoff-responsive agent.

Any strategic claim needs:

- scripted rational-agent positive controls;
- monotone response to payoff changes while wording stays fixed;
- identical action schemas and choice procedures across conditions;
- repeated generations/seeds sufficient to separate treatment from generation noise;
- equilibrium predictions stated before observing LLM behavior;
- INVALID/INCONCLUSIVE outputs when incentive or protocol checks fail.

### 5. Deterministic/native baseline

If a policy is known and machine-readable, a deterministic rule, test, type system, event log, or solver is the real baseline. A panel of LLM peers is not a fair competitor to code. September’s [CONTINUITY](https://arxiv.org/abs/2609.05269) is a particularly strong warning: authenticated context and assume-guarantee contracts can prevent compositional security failures without hoping that peer agents learn a norm.

## Survivors

### S1. Optimum-grounded Dec-POMDP evaluation of LLM teams

**Residual claim.** No located paper evaluates LLM agents on instances with independently verified `V*Dec` and `V*Cent`, then separates intrinsic decentralization cost from excess coordination loss while verifying that execution policies use only legal local histories.

**Why it survives.** [The Collaboration Tax](https://arxiv.org/abs/2608.22152) formalizes a related team-decentralization loss but uses a solo/team oracle over 32 tasks rather than a computed decentralized optimum. AAMAS 2026 [Symbolic Guidance](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/KEVK7310.pdf) studies autonomy levels on distributed graph problems, and [LLM-SMAC](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/RVAB7186.pdf) generates executable decision-tree code, but neither gives the two optimum references and decomposition. That narrow measurement object remains distinct.

**Main attacks.** The proposed mechanism claims do not survive independently. Joint-policy commitment can be produced centrally by one LLM; solver-guided repair resembles ordinary counterexample-guided synthesis; classic Dec-Tiger-like tasks risk memorization and trivial reactive policies. Calling separate model instances “agents” adds nothing if a single compiler writes every local controller.

**Required stronger baselines and controls.** Exact/best-certified solver; centralized symbolic compiler; one LLM emitting all decentralized local policies; independent LLMs; token-matched dialogue; reactive and finite-memory policies; shuffled/private-observation leak tests; five semantic renderings; at least two unseen generated instance families; model capability ladder. Run the AAMAS 2026 history/private-information diagnostics on every benchmark family first.

**Kill test.** Kill the paper if (i) reactive policies are near-optimal, (ii) one centralized LLM produces equal or better legal local policies, (iii) rendering variance dominates coordination variance, or (iv) the reference value is merely best-known but presented as exact.

**Retained form.** Evaluation/instrument paper first. Add commitment/repair only if it beats the centralized policy compiler and classical local search per token and per evaluator call.

### S2. Leaderboard robustness to adversarial harness-configuration choice

**Residual claim.** Existing social-choice robustness results model benchmark-specific training as the manipulation lever, while harness-fragility work shows that configuration selects winners but does not compare aggregation rules under adversarial configuration selection. The missing object is the minimax/instance-level robustness of an aggregation rule over a preregistered admissible configuration set.

**Why it survives.** [How Hard is it to Rig a Benchmark?](https://arxiv.org/abs/2605.23628) derives manipulation robustness for arithmetic mean, median, mean win rate, and pairwise majority under training-set bribery. [There Is No Neutral Harness](https://arxiv.org/abs/2608.21382) holds weights/items/decoding fixed across 26 harnesses and shows four of 12 models can rank first. The first treats scores as fixed scalars; the second diagnoses bands but does not solve robust aggregation.

**Main attacks.** “Fragility-weighted score” is an obvious noise-discounting heuristic and may destroy construct validity by removing discriminative items. The admissible-config set can be cherry-picked by the researcher. If all configurations are semantically non-equivalent, robustness merely rewards a bad evaluator.

**Required stronger baselines and controls.** Score/rank intervals with no new rule; worst-case rank; minimax regret; stable-item-only ranking; median over configurations; pairwise majority over configuration-specific rankings; held-out harness axes; discrimination/calibration trade-off; sensitivity to the admissible-set definition. Compare against AAMAS 2026 clone-robust aggregation, not only arithmetic mean.

**Kill test.** Kill if disclosure of rank bands or the median-over-configurations baseline matches the proposed rule, or if the winner changes only because one scoring method is invalid for the model family.

**Retained form.** A compact, computation-only social-choice paper. Do not claim a general solution to leaderboard gaming.

### S3. Entry-level memory invalidation caused by teammate evolution

**Residual claim.** No located work causally measures whether a specific retrieved experience changes from helpful to harmful as *other agents* update, after matching elapsed time and exogenous environment drift.

**Why it survives.** [Testing Interchangeability in LLM Agent Teams](https://arxiv.org/abs/2609.05279) is now the closest threat: role-matched swaps raise communication cost 16–63%, and the effect co-moves with team-history divergence. It occupies learned convention mismatch, not per-memory-entry utility or teammate-change-conditioned hazard. [Skill Following](https://arxiv.org/abs/2609.00549) supplies the right matched actual-use principle—same task with skill enabled and disabled—but does not study co-evolving teams.

**Main attacks.** This can collapse to ordinary software dependency invalidation or a timestamp recency effect. “Evolution event count” may proxy for time, model randomness, or more accumulated text. September’s interchangeability result also suggests the main effect may be communication convention drift rather than factual memory invalidation.

**Required stronger baselines and controls.** Same-task inject/no-inject effect conditioned on actual retrieval; frozen-team arm; placebo roster disruption; reset-notebook arm; matched exogenous API drift; pure recency and TTL eviction; version-tag invalidation; current-state-only context; greedy versus stochastic decoding; at least two backbones. Separate task success from communication-per-progress.

**Kill test.** Kill if recency/TTL matches teammate-aware provenance, if the effect vanishes under greedy decoding, or if communication overhead changes but entry-level task utility does not.

**Retained form.** “Dependency-aware memory validity under changing teammates,” not the broad claim that MARL non-stationarity was undiscovered.

### S4. Persistent experience pools as quality-manipulable public goods

**Residual claim.** A reusable experience artifact separates contribution *volume* from verified downstream marginal value. No located work jointly models that persistent quality choice, downstream reuse externalities, and payoff-responsive contribution by LLM agents.

**Why it survives.** AAMAS 2026 [Everyone Contributes!](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/SJPO2377.pdf) already designs incentives for strategic multi-LLM contribution in sequential public-goods games, so “LLM public goods” is occupied. [Knowledge-Centric Self-Improvement](https://arxiv.org/abs/2607.19592) builds the cooperative pool. [Useful Memories Become Faulty](https://arxiv.org/abs/2605.12978) shows pool utility can fall below no-memory because of consolidation. [Governed Collaborative Memory](https://arxiv.org/abs/2605.04264) explicitly frames persistence as a selection regime. What remains is strategic manipulation of a persistent artifact’s downstream value.

**Main attacks.** LLMs may merely obey competitive wording. Usage-based reward is not incentive-compatible if retrieval is manipulable, popular entries crowd out new ones, or success credit is confounded. A flat payment vs usage payment comparison is not mechanism design without equilibrium analysis. Shared pools may be unnecessary if episodic retention already matches consolidation.

**Required stronger baselines and controls.** Scripted rational contributors; cooperative LLM control; no pool; raw episodic pool; oracle-curated pool; flat/usage/marginal-contribution payments; randomized retrieval exposure; author-blind evaluation; counterfactual inject/no-inject value; manipulation of payoff magnitude with fixed wording; model-scale ladder; pool-level welfare and contributor welfare separately.

**Kill test.** Kill if contribution quality does not respond monotonically to payoff, if honesty instructions match payments, if episodic retention dominates all mechanisms, or if the payment signal can be gamed without improving downstream welfare.

**Retained form.** Merge C3 and D1. Lead with persistent quality manipulation and auditable marginal contribution, not “memory is a commons.”

### S5. Verifier-panel robustness under adaptive, budgeted persuasion

**Residual claim.** No exact match was located for an adaptive persuader allocating a fixed total attack budget across a correlated verifier panel while measuring empirical cost-to-flip as panel size and ballot visibility vary.

**Why it survives.** [Jagged Judges](https://arxiv.org/abs/2608.12645) attacks individual judges. [Nine Judges, Two Effective Votes](https://arxiv.org/abs/2605.29800) studies correlated natural errors. [Blind to the Pivotal Vote](https://arxiv.org/abs/2608.06940) shows independent evidence helps only on one-vote-margin cases and gives a defensive substitution rule. The offensive combination is not in the located papers.

**Main attacks.** The original hypothesis “more judges makes you wronger” is not theoretically warranted under a fixed total attack budget; majority size can only increase the number of ballots that must be flipped under common threat models. Letting the attacker inspect ballots and privately message selected judges may be unrealistic. If the same persuasion is broadcast, the problem is correlated prompt injection, not social choice.

**Required stronger baselines and controls.** Strongest single judge; diverse-family panel; hidden versus visible ballots; public versus private persuasion; fixed total tokens/calls, not fixed per-judge budget; random targeting; optimal targeting computed from measured response curves; deterministic external evidence; abstention; direct test-only decision. Report attack cost-to-flip and robust accuracy, not only accuracy versus `k`.

**Kill test.** Kill if the optimal attacker policy is simple broadcast, if deterministic evidence alone dominates every panel at lower cost, or if non-monotonicity appears only when attack budget scales with panel size.

**Retained form.** Adversarial robustness of a collective verifier, not a foregone Condorcet reversal.

### S6. Reputation-rank inversion from structured attribution error

**Residual claim.** Generic noisy-reputation thresholds are not novel. The defensible residual is empirical estimation of an LLM-attributor error kernel structured by agent role, verbosity, and trace position, followed by a preregistered test that this kernel inverts competence rankings and makes sanctioning worse than matched random exclusion.

**Why it survives.** Classical indirect-reciprocity theory already states accuracy conditions such as social resolution exceeding cost/benefit and shows erroneous costly punishment often reduces welfare; see [Indirect reciprocity provides a narrow margin of efficiency for costly punishment](https://pmc.ncbi.nlm.nih.gov/articles/PMC2614697/) and [Deception undermines cooperation stability](https://pmc.ncbi.nlm.nih.gov/articles/PMC4732813/). AAMAS 2026 [RepuNet](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/UEHN4980.pdf) already uses reputation to prevent LLM cooperation collapse. Therefore `a*` alone is occupied. The possible novelty is *measured directional misattribution* tied to modern traces and its downstream inversion.

**Main attacks.** The headline accuracy constant is already moving: [EDGE](https://arxiv.org/abs/2609.01360) uses counterfactual rollout and dependency graphs for multi-error attribution, weakening any claim based on a fixed 34% or 53.5% ceiling. Direct behavior observation can dominate inferred blame. The simulator may manufacture inversion through its team-formation and sanction rules.

**Required stronger baselines and controls.** No sanction; matched random exclusion; direct-observation reputation; Bayesian noisy-label correction; role-balanced attribution; abstention/conformal sets; oracle culprit; multiple real attributors including EDGE-style dependency attribution; sensitivity across team-formation models. Estimate the kernel on held-out real traces before choosing the sanction model.

**Kill test.** Kill if errors are near-uniform after role balancing, if direct-observation reputation is available and cheap, if rank inversion disappears across plausible team-formation rules, or if improved attribution places all deployed methods above the harmful region.

**Retained form.** Drop “first accuracy threshold.” Claim and test structured-error-induced governance inversion.

## Detailed kills

### Joint-policy commitment and solver-guided repair

AAMAS 2026 already shows partial pseudocode guidance can outperform both free reasoning and full prescription in distributed coordination ([official PDF](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/KEVK7310.pdf)). [LLM-SMAC](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/RVAB7186.pdf) already implements Planner–Coder–Critic decision-tree refinement. A single LLM can generate all legal local policy trees; if that baseline matches a negotiating team, the “commitment” story is false. Keep these as arms inside S1, not headline contributions.

### STAV

[Delayed Verification Destabilizes Multi-Agent LLM Belief](https://arxiv.org/abs/2606.27409) already gives delay/dose stability thresholds and corrector placement. AAMAS 2026 [RBC](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/MFLP4403.pdf) addresses belief compensation under information delay. Sep 2026 [Speculative Uncertainty](https://arxiv.org/abs/2609.05274) supplies a cheap transferable pre-execution veto signal. STAV’s equations reduce to one delayed audit controller; the network is not load-bearing unless heterogeneous graph modes change the optimal policy. A fixed audit floor, clipping, or rate limiter may dominate the projection controller. The full package is therefore an occupied composition unless real behavioral identification first produces a robust, nontrivial fixed-vs-adaptive separation.

### Harness-update manipulation resistance

[SEAGym](https://arxiv.org/abs/2606.17546), [Self-Evolving Agent Harnesses via Gated Semantic Quality-Diversity](https://arxiv.org/abs/2607.13683), and Sep [Belief-Calibrated Optimization](https://arxiv.org/abs/2609.01861) already use held-out splits, replay/transfer views, deterministic crediting, significance gates, and persistent optimizer beliefs. A “score-seeking” system prompt does not make the proposer strategically payoff-responsive. A second sealed set just moves the overfitting boundary. Without a new adaptive-data-analysis guarantee or a real attacker with query access constraints, this is benchmark red-teaming, not mechanism design.

### Solo-safe/team-harmful harness updates

The observation is valid but too obvious: deploy-time teamwork is an omitted test distribution. [When Agents Coordinate](https://arxiv.org/abs/2608.16801) already measures team-size, topology, messaging, and file-policy costs; [Testing Interchangeability](https://arxiv.org/abs/2609.05279) already isolates convention mismatch using placebo swaps. “Run integration tests before accepting a component update” is not an AAMAS contribution. It revives only with a theorem/algorithm for selecting a small team test set that detects externalities under a hard evaluation budget.

### Skill-reuse contagion

[EVOMAL](https://arxiv.org/abs/2608.25776) demonstrates persistent self-propagating skill poisoning and a branching-process condition. [Reliability-Contagion](https://arxiv.org/abs/2607.21912) supplies network epidemic thresholds. Sep [Skill Following](https://arxiv.org/abs/2609.00549) shows even benign retrieval can have negative same-task causal effect. Asking prompted agents to choose retrieval breadth adds questionable strategic behavior, while quarantine is already the obvious defense. No independent gap remains without a formal mechanism whose equilibrium differs from standard access control.

### Sharing-rate monoculture

[DecentMem](https://arxiv.org/abs/2605.22721) explicitly motivates decentralized memory by centralized-memory diversity collapse. [Diversity Collapse in Multi-Agent Systems](https://arxiv.org/abs/2604.18005) measures topology-dependent convergence, and Sep [Creative Generation via Multi-Agent Debate](https://arxiv.org/abs/2609.00683) proves within-session diversity is necessary for cross-run diversity and proposes diversity-preserving peer selection. A sharing-probability sweep over more rounds is an ablation, not a paper. Embedding-cluster entropy also risks measuring encoder choice rather than behavioral diversity.

### Peer sanctioning for operational policy

The held-out-clause hypothesis is incoherent. If peers receive the held-out policy, the centralized baseline must receive it too. If neither receives it, “generalization” is accidental agreement with an unknown rule. A deterministic workflow verifier, [IntentGuard](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/PJGH6650.pdf), or Sep [CONTINUITY](https://arxiv.org/abs/2609.05269) provides a stronger safety baseline with inspectable guarantees. Peer sanctions add LLM calls and diffuse responsibility.

### Incentive-compatible escalation

AAMAS 2026 [Truthful Reporting of Competence with Minimal Verification](https://arxiv.org/abs/2602.14076) directly characterizes dominant-strategy truthful mechanisms under scarce perfect or noisy verification. [LLM Performance Predictors](https://arxiv.org/abs/2601.07006) addresses cost-aware escalation. Combining these with a congested reviewer and then testing whether prompted LLMs notice a kink is derivative; Sep construct-validity results make the behavioral part especially fragile.

### Own candidates

- **Compute-matched MAS synergy:** occupied by [2604.02460](https://arxiv.org/abs/2604.02460), [2601.12307](https://arxiv.org/abs/2601.12307), and the Nature scaling study.
- **Real role specialization:** occupied by [ExRole](https://arxiv.org/abs/2608.11949) with manual/random/shuffled controls and reduced to a single-agent implementation by [Mixture of Roles](https://arxiv.org/abs/2608.27338).
- **Memory authorization governance:** occupied by [Agent Memory Is a Surface for Endogenous Authorization Laundering](https://arxiv.org/abs/2609.01836) and [CONTINUITY](https://arxiv.org/abs/2609.05269).
- **Dependency-aware error attribution:** occupied exactly by [EDGE](https://arxiv.org/abs/2609.01360).

## Primary-source URL ledger

### AAMAS 2026

1. Proceedings: https://www.ifaamas.org/Proceedings/aamas2026/forms/contents.htm
2. Probing Dec-POMDP Reasoning: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/ECCJ1033.pdf
3. Symbolic Guidance: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/KEVK7310.pdf
4. LLM-SMAC: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/RVAB7186.pdf
5. RepuNet: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/UEHN4980.pdf
6. Everyone Contributes: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/SJPO2377.pdf
7. RBC: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/MFLP4403.pdf
8. IntentGuard: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/PJGH6650.pdf
9. LEGOMem: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/VLUA1303.pdf
10. Responsibility analysis: https://www.ifaamas.org/Proceedings/aamas2026/pdfs/PVFH7189.pdf

### September 2026 pressure set

11. Testing Interchangeability in LLM Agent Teams: https://arxiv.org/abs/2609.05279
12. Speculative Uncertainty gate: https://arxiv.org/abs/2609.05274
13. CONTINUITY: https://arxiv.org/abs/2609.05269
14. Belief-Calibrated Optimization: https://arxiv.org/abs/2609.01861
15. Authorization Laundering: https://arxiv.org/abs/2609.01836
16. Construct Validity Failures in LLM Agent Commerce: https://arxiv.org/abs/2609.01519
17. EDGE attribution: https://arxiv.org/abs/2609.01360
18. Creative Generation via Multi-Agent Debate: https://arxiv.org/abs/2609.00683
19. Safe Agents Fail Together SoK: https://arxiv.org/abs/2609.00595
20. Skill Following: https://arxiv.org/abs/2609.00549

### August and earlier decisive neighbors

21. Collaboration Tax: https://arxiv.org/abs/2608.22152
22. No Neutral Harness: https://arxiv.org/abs/2608.21382
23. When Agents Coordinate: https://arxiv.org/abs/2608.16801
24. ExRole: https://arxiv.org/abs/2608.11949
25. Jagged Judges: https://arxiv.org/abs/2608.12645
26. Blind to the Pivotal Vote: https://arxiv.org/abs/2608.06940
27. EVOMAL: https://arxiv.org/abs/2608.25776
28. Mixture of Roles: https://arxiv.org/abs/2608.27338
29. Knowledge-Centric Self-Improvement: https://arxiv.org/abs/2607.19592
30. HarnessBank/GSME: https://arxiv.org/abs/2607.13683
31. Reliability-Contagion: https://arxiv.org/abs/2607.21912
32. Delayed Verification Destabilizes Belief: https://arxiv.org/abs/2606.27409
33. SEAGym: https://arxiv.org/abs/2606.17546
34. Nine Judges, Two Effective Votes: https://arxiv.org/abs/2605.29800
35. How Hard is it to Rig a Benchmark?: https://arxiv.org/abs/2605.23628
36. DecentMem: https://arxiv.org/abs/2605.22721
37. Useful Memories Become Faulty: https://arxiv.org/abs/2605.12978
38. Governed Collaborative Memory: https://arxiv.org/abs/2605.04264
39. Diversity Collapse in MAS: https://arxiv.org/abs/2604.18005
40. Single-Agent LLMs Outperform MAS: https://arxiv.org/abs/2604.02460
41. Truthful Competence Reporting: https://arxiv.org/abs/2602.14076
42. Strong Single-Agent Baseline: https://arxiv.org/abs/2601.12307
43. LLM Performance Predictors: https://arxiv.org/abs/2601.07006
44. Nature collaboration scaling study: https://www.nature.com/articles/s42256-026-01268-y
45. Classical punishment/noisy reputation: https://pmc.ncbi.nlm.nih.gov/articles/PMC2614697/
46. Classical deception/accuracy threshold: https://pmc.ncbi.nlm.nih.gov/articles/PMC4732813/

**URL ledger count:** 46 primary paper/proceedings URLs.

## Final ranking and recommendation

| Rank | Survivor | Novelty margin | Execution risk | Recommendation |
|---:|---|---|---|---|
| 1 | S1 optimum-grounded Dec-POMDP evaluation | medium-high after narrowing | medium | Best AAMAS-aligned scientific instrument; run benchmark-validity and single-compiler gates first. |
| 2 | S2 harness-config robust aggregation | medium | low | Fastest decisive project; zero API spend if released grid is complete. |
| 3 | S3 teammate-change memory invalidation | medium, squeezed by Sep 05279 | medium | Run entry-level causal pilot immediately; abandon if TTL wins. |
| 4 | S4 persistent experience commons | medium | high construct-validity risk | Proceed only with scripted controls and payoff monotonicity gate. |
| 5 | S5 adversarial verifier panels | low-medium | medium | Retain as backup; formalize threat/budget before any calls. |
| 6 | S6 structured blame inversion | low-medium | medium-high | No generic threshold claim. First estimate the real error kernel with current attributors. |

The hard recommendation is to pursue **S1** if the goal is an AAMAS main-track paper and **S2** if the goal is the highest probability of a clean, reproducible result before the deadline. Do not start STAV, peer sanctions, or generic noisy-blame threshold work in their current forms.
