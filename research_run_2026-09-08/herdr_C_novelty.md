# Agent C — independent novelty kill audit

**Audit date:** 2026-09-08  
**Scope:** optimum-grounded Dec-POMDP evaluation of LLM teams; adaptive/scarce verification; sanctioning under unreliable blame; shared memory as a commons; endogenous teammate co-evolution; convention/deception repair.

## Bottom line

No family earns **A**. Two retain a technically meaningful residual (**B**) only after aggressive narrowing; four are **C** because their residual is an intersection of already active literatures. Broad versions of every family should be rejected.

| Candidate family | Class | Kill verdict | Closest invalidating paper | Exact residual that survives |
|---|---:|---|---|---|
| Optimum-grounded Dec-POMDP evaluation of LLM teams | **B** | The broad claim “LLM teams are not evaluated against an optimum under private information” is false. CalBench already reports realized-to-oracle excess cost in an inherently decentralized private-calendar task and supplies decentralized non-LLM references. Zero-Shot Coordination Among LLM Agents already evaluates LLMs in minimal Dec-POMDPs. | [CalBench (Zou et al., 2026)](https://arxiv.org/abs/2605.09823) | On the **same finite Dec-POMDP instances**, compute or certify both the centralized-information optimum and the decentralized-policy optimum, then attribute the gap into intrinsic information loss and LLM **policy-realization loss**. Preserve legal local histories and exactly value emitted policy trees/controllers. CalBench uses a full-information CP-SAT oracle, not a certified Dec-POMDP policy optimum or the two-optimum decomposition. |
| Adaptive/scarce verification | **B** | Budget allocation, adaptive compute, verifier placement, and delay-induced instability are all occupied. “Verification should be adaptive/budgeted” is dead. | [Delayed Verification Destabilizes Multi-Agent LLM Belief (Itkin, 2026)](https://arxiv.org/abs/2606.27409) | Fit an LLM’s **endogenous trust-to-audit law**, place that measured law inside a delayed error/trust loop, predict held-out stability transitions, and project adaptive audit actions onto a robust safe set while comparing with a verification-budget-matched fixed policy. Itkin optimizes fixed corrector dose/placement; AVA and BRA-Audit adapt allocation but do not close a behaviorally fitted trust feedback loop. |
| Sanctioning under unreliable blame | **C** | Noisy monitoring, mistaken punishment, causal blame under policy uncertainty, direct/third-party punishment, partner selection, and reputation are mature. Porting their intersection to LLM agents is not a paper. | [Monopolizing Sanctioning Power under Noise (Fischer, Grechenig & Meier, 2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5040719/) | A long-horizon Markov game in which agents strategically manipulate the evidence used for **causal** blame, while a learned sanction policy trades deterrence against false punishment and yields a new welfare/impossibility threshold. This is a narrow three-way combination; without a theorem or surprising phase transition it remains incremental. |
| Shared memory as a commons | **C** | The metaphor and governance engineering are occupied. A 2026 paper explicitly calls shared memory an “artificial commons”; provenance, supersession, propagation, access control, and poisoning repair already have implementations or formal defenses. | [Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment (Truong et al., 2026)](https://openreview.net/attachment?id=5ow68CzpRg&name=pdf) | A repeated public-goods/common-pool game with heterogeneous agents choosing costly write, verify, challenge, supersede, and repair actions, plus an incentive-compatible decentralized mechanism and equilibrium/welfare result. “Add provenance,” “govern writes,” or “measure pollution” is not residual novelty. |
| Endogenous teammate co-evolution | **C** | Co-evolving LLM teams, team-level experience-driven evolution, partner-policy shift detection, non-stationary teammates, and stale multi-agent replay are all prior art. “Agents evolve together” and “teammates changing causes non-stationarity” are dead. | [Evolve as a Team / Meta-Team (Hao et al., 2026)](https://arxiv.org/abs/2605.29790) | Measure the **causal validity hazard of a stored experience** as a function of teammate evolution events while the focal agent and teammates all evolve; separate teammate-caused drift from matched exogenous environment drift and elapsed time; test provenance keyed to teammate-policy lineage. Meta-Team improves teams from shared experience but does not estimate this hazard or isolate teammate evolution as its cause. |
| Convention/deception repair | **C** | Convention selection, convention formation, dynamic grounding repair, clarification at handoffs, noisy-channel conversational repair, deception propagation, malicious-agent filtering, and resilient consensus are separately crowded. A generic repair module is dead. | [Talk is Cheap, Communication is Hard (Yao, Zou & Hawkins, 2026)](https://arxiv.org/abs/2605.01750) | After a strategic agent corrupts an established convention, benign agents must distinguish deception from honest semantic drift and **decentrally restore an efficient convention** under continuing partial observability, without a truth oracle or merely ejecting the suspect. The surviving claim is this adversarial recovery problem, not convention learning, deception detection, or repair alone. |

### Classification rubric

- **A — clearly novel:** no close formulation after exact, semantic, legacy-term, and latest-work searches.
- **B — partially explored:** major adjacent work exists, but a technically meaningful problem remains directly unsolved.
- **C — mostly solved/crowded:** only a narrow intersection, domain transfer, or incremental relaxation remains.
- **D — directly addressed:** one close paper studies the proposed problem at essentially the supplied specificity.

The classifications apply to the strongest precise formulation recoverable from `research_specs`, not to their broader motivating language. Recent preprints can still move before submission; **B is permission for a pilot, not a verified novelty claim**.

## Search protocol

I did not accept novelty statements or “zero results” recorded in the workspace. The workspace supplied candidate definitions only. I independently inspected primary arXiv records, official ACL/ICLR/AAMAS/AAAI/PMLR proceedings pages, and publisher records, emphasizing work posted or published in 2025–2026. Older terminology was searched because four proposals rename established problems.

| Family | Exact / current terms | Synonyms | Older terminology used to attack the claim |
|---|---|---|---|
| Dec-POMDP evaluation | `LLM Dec-POMDP optimal`, `decentralized optimum LLM team`, `oracle optimal coordination` | excess cost, collaboration tax, policy-realization gap, coordination regret, solver-guided commitment | decentralized MDP, joint policy search, policy tree/FSC, centralised vs decentralized information, DCOP oracle, zero-shot coordination, other-play |
| Verification | adaptive verification, scarce audit, audit budget, verifier scheduling | selective verification, corrector placement, audit-point placement, confidence-ranked auditing, anytime verification | inspection games, monitoring mechanisms, costly monitoring, delayed feedback/consensus, value of information, strategic classification |
| Sanctions/blame | unreliable blame, noisy attribution, learned sanctions | false punishment, causal responsibility, failure attribution, peer punishment, reputation | imperfect public monitoring, stochastic punishment, second/third-party punishment, indirect reciprocity, accountable MMDP |
| Memory commons | shared agent memory commons, governed memory, memory pollution | institutional memory, fleet memory, collaborative memory, shared experience pool | public-goods game, common-pool resource, costly contribution/monitoring, peer prediction, knowledge-commons governance |
| Co-evolution | co-evolving LLM agents, teammate evolution, collaborative self-evolution | policy shift, experience invalidation, partner drift, team evolution | MARL non-stationarity, behavior-switching teammates, ad hoc teamwork, open Dec-POMDP, stale experience replay, opponent modelling |
| Convention/deception repair | convention repair, deception recovery, grounding repair | equilibrium selection, clarification, testimony adoption, misinformation remediation | naming/Lewis games, conversational repair, common ground, emergent communication, Byzantine/resilient consensus, zero-shot convention mismatch |

Searches were stopped only after each family had (i) a 2025–2026 collision, (ii) a legacy literature collision, and (iii) an exact residual stated in terms that the closest paper does not satisfy.

## Family findings

### 1. Optimum-grounded Dec-POMDP evaluation of LLM teams — B

**What is killed.** CalBench generates private-information scheduling instances with CP-SAT oracle solutions, reports excess cost, and compares decentralized reference protocols under matched information constraints. SILO-BENCH has exact answers and organizes tasks by optimal communication complexity. The Collaboration Tax formalizes team decentralization loss against solo execution. Zero-Shot Coordination Among LLM Agents uses minimal Dec-POMDP environments and exposes convention/partner-reasoning failures. Improved Multi-Agent Collaboration explicitly formalizes LLM collaboration as a Dec-POMDP. Therefore none of these are defensible novelty claims:

- introducing formal partial observability to LLM teams;
- using an oracle or optimum-normalized score;
- showing a gap between LLM teams and optimal task outcomes;
- asking LLM agents to coordinate in a Dec-POMDP;
- using explicit commitments or joint-policy search as a new multi-agent idea.

The last point has deep prior art: [Commitment-Driven Distributed Joint Policy Search (Witwicki & Durfee, 2007)](https://www.ifaamas.org/Proceedings/aamas07/html/tec16_08.html) searches commitment configurations and builds constrained local policies; modern Dec-POMDP work already searches finite-state controllers and equilibria.

**Why B rather than C/D.** CalBench’s oracle is a centralized combinatorial solution. It does not report a separately certified optimum over policies constrained to each agent’s legal observation history, nor subtract that from a centralized-information ceiling. The 2026 zero-shot paper uses Dec-POMDP structure but does not make this two-reference decomposition the evaluation instrument. A reproducible **policy-realization regret** result can therefore survive, but only if the paper exactly evaluates emitted decentralized controllers and proves that no private information leaked into them. A sampled rollout table against a task oracle collapses into CalBench/SILO-BENCH territory.

**Submission-kill test.** If CalBench’s CP-SAT oracle and a decentralized solver coincide on the proposed instances, leaving no nonzero intrinsic information cost, or if the paper reports only outcome regret rather than exact legal-policy value, downgrade to **C/D** and do not lead with the decomposition.

### 2. Adaptive/scarce verification — B

**What is killed.** The live 2025–2026 neighborhood is unusually dense:

- [Anytime Verified Agents](https://openreview.net/forum?id=JMDCMf7mlF) dynamically allocates search, sampling, and verification under a user budget using uncertainty and value of information.
- [One Human, N Agents](https://arxiv.org/abs/2607.28317) allocates a scarce human audit budget under miscalibrated, correlated confidence and derives the threshold where confidence ranking is worse than random.
- [BRA-Audit](https://arxiv.org/abs/2608.14668) places limited audit calls on dynamic LLM-MAS dependency graphs to minimize unchecked exposure.
- [Delayed Verification Destabilizes Multi-Agent LLM Belief](https://arxiv.org/abs/2606.27409) derives delay/dose stability thresholds and a greedy limited-corrector placement rule.
- [Using Scarce Audits Wisely](https://proceedings.mlr.press/v291/dai25a.html) gives a strategic repeated-allocation mechanism with audit and regret bounds.

Thus “allocate verification adaptively,” “audit where influence is high,” “verification delay can destabilize,” “confidence can misallocate audits,” and “strategic agents require scarce audits” are not gaps.

**Residual.** STAV survives only as a system-identification/control claim: measure how an LLM changes audit probability after observed success/failure; fit the law on separate data; insert it into a delayed trust/error model; predict a held-out instability region where a budget-matched fixed policy remains stable; then constrain the adaptive action with a robust guarantee. The scientific contribution must be the **endogenous coupling**, not another scheduler.

**Submission-kill test.** If a fixed verifier at the same average audit rate is no more stable, if the fitted trust law does not predict held-out transitions, or if instability exists only in an ungrounded signed-belief toy already covered by Itkin, reject the project.

### 3. Sanctioning under unreliable blame — C

**What is killed.** Human/economic experiments already show that noisy observation produces mistaken or antisocial punishment and can erase cooperation benefits. Computational work formalizes blame in cooperative sequential decisions under uncertain policies and causal effects propagated through teammates. Recent MARL work jointly studies direct punishment, third-party punishment, partner selection, and reputation; LLM-agent work already studies reputation-mediated cooperation, public-goods incentives, norm formation, and fine-grained failure attribution.

The closest pair nearly spans the proposal:

1. [Monopolizing Sanctioning Power under Noise](https://pmc.ncbi.nlm.nih.gov/articles/PMC5040719/) directly tests the unreliable-information-to-wrongful-sanction phenomenon.
2. [On Blame Attribution for Accountable Multi-Agent Sequential Decision Making](https://arxiv.org/abs/2107.11927) formalizes blame and robustness to uncertainty about agents’ policies in cooperative MMDPs.

Recent collisions make a domain-transfer defense weaker: [Bottom-Up Reputation Promotes Cooperation with MARL](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1745.pdf), [Investigating the Impact of Direct Punishment](https://ojs.aaai.org/index.php/AAAI/article/view/41376), and AAMAS 2026 work on sequential public-goods incentives and LLM norm formation.

**Residual.** Only strategic manipulation of the *evidence used for causal blame*, coupled to learned sanctions in a long-horizon task, is not directly located. That is not enough by itself. The paper needs a theorem, impossibility, or calibrated threshold showing when sanctioning reduces welfare despite improving apparent compliance.

**Submission-kill test.** If “unreliable blame” is implemented as an exogenous label flip, or the sanction is just reward shaping, the project is a direct recombination of old noisy-monitoring and MARL-punishment work: reject.

### 4. Shared memory as a commons — C

**What is killed.** The exact framing is occupied. Truong et al. define shared memory/context as an artificial commons and explicitly discuss write authority, verification labor, pollution, free-riding, rollback, and repair. [Governed Shared Memory](https://arxiv.org/abs/2606.24535) implements scope, temporal supersession, provenance, and propagation controls. [Governed Collaborative Memory as Artificial Selection](https://arxiv.org/abs/2605.04264) treats which memories become institutional state as a selection regime. [Origin-Bound Authority](https://arxiv.org/abs/2606.24322) provides formal, machine-checked defenses against memory-authority laundering. [Memory Poisoning Propagation and Repair](https://doi.org/10.1145/3806262.3806294) explicitly detects and repairs cross-agent poisoned memory.

So the following are crowded or invalid novelty claims: shared memory needs governance; provenance is important; stale/contradictory memories propagate; access/write permissions matter; poisoning should be detected and repaired; a “memory constitution” is needed.

**Residual.** The viable object is not a memory architecture. It is a game where maintenance labor is costly and agents have heterogeneous local objectives/information. It must characterize neutral-pool equilibria and supply an incentive-compatible mechanism for write/verify/challenge/repair decisions. If every agent is prompted to maximize one global reward and verification has no local cost, “free-riding” is manufactured rather than endogenous.

**Submission-kill test.** If the contribution can be described as access control + provenance + reputation, or the only result is lower memory pollution in a benchmark, reject it as **D-level engineering overlap**.

### 5. Endogenous teammate co-evolution — C

**What is killed.** The survey claim that co-adaptation/endogenous non-stationarity is “empty” does not survive 2026 search:

- [CoMAS](https://arxiv.org/abs/2510.08529) performs decentralized LLM-agent co-evolution from inter-agent interaction rewards.
- [Evolve as a Team](https://arxiv.org/abs/2605.29790) converts team execution experience into changes to agent behavior, coordination, and organization.
- [Self-Evolving Multi-Agent Systems via Decentralized Memory](https://arxiv.org/abs/2605.22721) explicitly couples self-evolving MAS with persistent decentralized memory.
- [Bayesian Partner Modelling enables Adaptive Replanning](https://arxiv.org/abs/2608.18490) handles LLM teammates whose strategies shift mid-task and introduces a belief-action gap.

The underlying problem is much older: [Fast Teammate Adaptation](https://arxiv.org/abs/2305.05911) models sudden teammate policy change as an open Dec-POMDP; [Stabilising Experience Replay for Deep MARL](https://arxiv.org/abs/1702.08887) addresses replay made stale by concurrently changing agent policies; behavior-switching ad hoc teammates were studied at IJCAI 2019.

**Residual.** A narrow measurement gap remains: no inspected paper estimates the counterfactual hazard that a *specific stored LLM-agent experience* becomes harmful after k teammate-evolution events, while separately matching exogenous environment drift and time. Provenance must identify the teammate policy/version on which the experience depended. The mitigation is secondary; generic pruning, freshness decay, or active re-verification already overlaps GLOVE and dynamic-memory work.

**Submission-kill test.** If the study merely shows that performance changes when teammates update, or compares frozen versus evolving teams without replaying and counterfactually ablating individual memories, it is already covered conceptually by co-evolution and non-stationary-teammate work.

### 6. Convention/deception repair — C

**What is killed.** Three active literatures collide:

- **Convention selection/formation:** [DICE](https://arxiv.org/abs/2606.08068) formalizes oscillation/drift among coordination conventions and supplies an equilibrium-selection method; [SIGN](https://arxiv.org/abs/2510.21855) steers LLM convention formation with schema-induced naming games.
- **Repair:** [Talk is Cheap](https://arxiv.org/abs/2605.01750) studies dynamic grounding failures and repair in multi-agent LLM negotiation; [COOP2-Repair](https://arxiv.org/abs/2603.00349) predicts cooperative-constraint failures and opens targeted repair channels; [AgentAsk](https://aclanthology.org/2026.acl-long.1294/) performs strategic clarification at error-prone handoffs. Conversational repair in emergent communication is already an ICLR 2024/AAMAS 2025 line.
- **Deception/malicious influence:** [When Truth Is Distributed](https://arxiv.org/abs/2608.03421) traces false testimony from a key evidence holder through honest agents; [Resilient Consensus in Agentic AI](https://arxiv.org/abs/2606.15024) applies Byzantine-resilient filters to adversarial LLM consensus; 2025–2026 work detects Trojan/rogue agents or remediates malicious graph nodes.

No novelty remains in “agents need conventions,” “conventions drift,” “ask for clarification,” “repair miscoordination,” “detect a deceiver,” or “filter malicious messages.”

**Residual.** The only credible gap joins all three under a hard constraint: an established convention is strategically corrupted; honest agents lack a truth oracle and cannot simply remove the suspected agent; they must infer whether the mismatch is deception or honest semantic drift and converge to a welfare-efficient replacement. The evaluation must compare recovery time, welfare regret, false accusation, and convention quality against DICE, clarification, and resilient-consensus baselines.

**Submission-kill test.** If the attacker is labeled, truth is externally supplied, repair means adding another reviewer, or success means majority agreement rather than recovering an efficient convention, reject.

## Crowded ideas to reject now

| Reject this pitch | Class | Why |
|---|---:|---|
| “A benchmark for LLM multi-agent coordination” | **D** | MultiAgentBench, LLM-Coordination, SILO-BENCH, CalBench, and multiple 2026 coordination suites already span general collaboration, exact answers, private information, communication complexity, privacy, and cost. |
| “Evaluate LLM teams against an oracle/optimal answer” | **D** | CalBench reports excess cost to a generated oracle; SILO-BENCH uses exact answers. Only the two-optimum legal-policy decomposition remains. |
| “Model LLM collaboration as a Dec-POMDP” | **D** | Improved Multi-Agent Collaboration and Zero-Shot Coordination Among LLM Agents do so explicitly. |
| “Use explicit commitment or a joint policy to coordinate agents” | **C/D** | Commitment-based distributed joint-policy search is old; explicit policies alone are not new. |
| “Adapt verification to uncertainty or a budget” | **D** | AVA, One Human N Agents, BRA-Audit, and scarce-audit mechanism design directly occupy it. |
| “Place verifiers at influential points in a graph” | **D** | BRA-Audit and Itkin optimize audit/corrector placement. |
| “Delayed verification can cause oscillation” | **D** | Itkin 2026 is the exact claim. |
| “Use peer punishment/reputation to sustain LLM cooperation” | **D** | RepuNet, AAMAS public-goods/norm-formation work, bottom-up MARL reputation, and punishment studies occupy it. |
| “Attribute LLM-team failures to agents/messages” | **D** | Who&When and 2025–2026 failure-attribution work directly formulate this area. |
| “Govern shared memory with provenance/access control/versioning” | **D** | Governed Shared Memory, Governed Memory, and origin-bound authority already implement/formalize these controls. |
| “Detect and repair shared-memory poisoning” | **D** | A 2026 ACM paper has essentially this title and task; origin-bound authority gives a stronger formal security result. |
| “Let LLM agents self-evolve as a team” | **D** | CoMAS and Meta-Team directly claim decentralized/collaborative team self-evolution. |
| “Adapt to a teammate whose policy changes” | **D** | FastAP and BayesBeliefAgent directly study sudden/mid-task teammate shifts. |
| “Learn or stabilize conventions among LLM agents” | **D** | DICE and SIGN directly address equilibrium/convention selection and formation. |
| “Repair multi-agent coordination with clarification/revision” | **D** | Talk is Cheap, COOP2-Repair, and AgentAsk directly study targeted repair. |
| “Defend a team from one deceptive/malicious agent” | **C/D** | Hi-Agreement, resilient consensus, AiTM attacks, Trojan interrogation, rogue-agent monitoring, and graph remediation make the broad space crowded. |

## Unique-paper ledger

**Count: 52 unique primary papers or official proceedings records inspected.** Duplicate arXiv/proceedings versions count once. A ledger entry means the primary abstract/record or accessible paper text was inspected for problem, method, and comparator; it does **not** imply full-paper verification of every theorem or empirical claim. Cross-family papers are listed once and tagged.

### Optimum, decentralized coordination, and policy commitment (11)

1. Zou et al. (2026), [CalBench: Evaluating Coordination-Privacy Trade-offs in Multi-Agent LLMs](https://arxiv.org/abs/2605.09823). **Closest H1 invalidator.**
2. Hayler et al. (2026), [Zero-Shot Coordination Among LLM Agents](https://openreview.net/pdf?id=HHPbQlyA7Y).
3. Sun et al. (2026), [The Collaboration Tax](https://arxiv.org/abs/2608.22152).
4. Qiu, Xu & Yue (2025), [Improved Multi-Agent Collaboration with Multi-Turn Reinforcement Learning](https://openreview.net/pdf/0dca6191fc2b02c7feaf9fe4c04efbad492abcb7.pdf).
5. Agashe et al. (2025), [LLM-Coordination](https://aclanthology.org/2025.findings-naacl.448/).
6. Zhu et al. (2025), [MultiAgentBench](https://aclanthology.org/2025.acl-long.421/).
7. Zhang et al. (2026), [SILO-BENCH](https://aclanthology.org/2026.acl-long.1354/).
8. Xie et al. (2026), [DICE](https://arxiv.org/abs/2606.08068). Also convention selection.
9. Yang et al. (2026), [COOP2](https://arxiv.org/abs/2603.00349). Also repair.
10. Witwicki & Durfee (2007), [Commitment-Driven Distributed Joint Policy Search](https://www.ifaamas.org/Proceedings/aamas07/html/tec16_08.html).
11. You et al. (2023), [Monte-Carlo Search for an Equilibrium in Dec-POMDPs](https://proceedings.mlr.press/v216/you23a.html).

### Verification, audit scarcity, and delayed feedback (6)

12. Itkin (2026), [Delayed Verification Destabilizes Multi-Agent LLM Belief](https://arxiv.org/abs/2606.27409). **Closest H2 invalidator.**
13. Wang et al. (2026), [BRA-Audit](https://arxiv.org/abs/2608.14668).
14. Zavattari, Tommasi & Prencipe (2026), [One Human, N Agents](https://arxiv.org/abs/2607.28317).
15. Patel (2026), [Anytime Verified Agents](https://openreview.net/forum?id=JMDCMf7mlF).
16. Dai, Blanchard & Jaillet (2025), [Using Scarce Audits Wisely](https://proceedings.mlr.press/v291/dai25a.html).
17. Yin & Du (2026), [GLOVE: Global Verifier for LLM Memory-Environment Realignment](https://arxiv.org/abs/2601.19249). Also stale-memory repair.

### Sanctions, blame, reputation, and cooperation (10)

18. Fischer, Grechenig & Meier (2016), [Monopolizing Sanctioning Power under Noise](https://pmc.ncbi.nlm.nih.gov/articles/PMC5040719/). **Closest H3 invalidator.**
19. Triantafyllou, Singla & Radanovic (2021), [On Blame Attribution for Accountable Multi-Agent Sequential Decision Making](https://arxiv.org/abs/2107.11927).
20. Triantafyllou et al. (2024), [Agent-Specific Effects](https://proceedings.mlr.press/v235/triantafyllou24a.html).
21. Yang et al. (2025), [Who Gets the Reward, Who Gets the Blame?](https://arxiv.org/abs/2511.10687).
22. Chen et al. (2025), [Which Agent Causes Task Failures and When?](https://arxiv.org/abs/2505.00212).
23. Ren et al. (2025), [Bottom-Up Reputation Promotes Cooperation with MARL](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1745.pdf).
24. Ren et al. (2026), [Reputation as a Solution to Cooperation Collapse in LLM-based MASs](https://arxiv.org/abs/2505.05029).
25. Dasgupta & Musolesi (2026), [Investigating the Impact of Direct Punishment](https://ojs.aaai.org/index.php/AAAI/article/view/41376).
26. Salahshour, Oberhauser & Smerlak (2022), [The Cost of Noise](https://pmc.ncbi.nlm.nih.gov/articles/PMC8890652/).
27. Ambrus & Greiner (2017), [Consensual Punishment under Noisy Public Monitoring](https://pmc.ncbi.nlm.nih.gov/articles/PMC5703489/).

### Shared memory and institutional governance (7)

28. Truong et al. (2026), [Multi-Agent AI Systems Need Institutional Design](https://openreview.net/attachment?id=5ow68CzpRg&name=pdf). **Closest H4 invalidator.**
29. Margalit et al. (2026), [Governed Shared Memory for Multi-Agent LLM Systems](https://arxiv.org/abs/2606.24535).
30. Cuadros et al. (2026), [Governed Collaborative Memory as Artificial Selection](https://arxiv.org/abs/2605.04264).
31. Louck (2026), [Securing LLM-Agent Long-Term Memory Against Poisoning](https://arxiv.org/abs/2606.24322).
32. Taheri (2026), [Governed Memory: A Production Architecture for Multi-Agent Workflows](https://arxiv.org/abs/2603.17787).
33. Liu et al. (2026), [Memory Poisoning Propagation and Repair Mechanism in Multi-Agent Collaborative Environments](https://doi.org/10.1145/3806262.3806294).
34. Hao, Long & Zhao (2026), [Self-Evolving Multi-Agent Systems via Decentralized Memory](https://arxiv.org/abs/2605.22721).

### Co-evolution and non-stationary teammates (8)

35. Hao et al. (2026), [Evolve as a Team: Collaborative Self-Evolution for LLM-based MAS](https://arxiv.org/abs/2605.29790). **Closest H5 invalidator.**
36. Xue et al. (2025), [CoMAS: Co-Evolving Multi-Agent Systems via Interaction Rewards](https://arxiv.org/abs/2510.08529).
37. Goel et al. (2026), [Bayesian Partner Modelling enables Adaptive Replanning for LLM Coordination](https://arxiv.org/abs/2608.18490).
38. Zhang et al. (2023), [Fast Teammate Adaptation in the Presence of Sudden Policy Change](https://arxiv.org/abs/2305.05911).
39. Foerster et al. (2017), [Stabilising Experience Replay for Deep Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1702.08887).
40. Vallinder & Hughes (2025), [Cultural Evolution of Cooperation among LLM Agents](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2771.pdf).
41. Yang et al. (2026), [CoEvolve: Training LLM Agents via Agent-Data Mutual Evolution](https://aclanthology.org/2026.acl-long.1055/).
42. Cheng et al. (2026), [Mem2Evolve](https://aclanthology.org/2026.acl-long.952/).

### Convention, deception, and repair (10)

43. Yao, Zou & Hawkins (2026), [Talk is Cheap, Communication is Hard](https://arxiv.org/abs/2605.01750). **Closest H6 invalidator.**
44. Lin et al. (2026), [AgentAsk: Multi-Agent Systems Need to Ask](https://aclanthology.org/2026.acl-long.1294/).
45. Zhang & Woisetschläger (2025), [SIGN: Schema-Induced Games for Naming](https://arxiv.org/abs/2510.21855).
46. Vital, Sardinha & Melo (2025), [Implicit Repair with Reinforcement Learning in Emergent Communication](https://arxiv.org/abs/2502.12624).
47. Nikolaus (2024), [Emergent Communication with Conversational Repair](https://proceedings.iclr.cc/paper_files/paper/2024/hash/27a2b7a22f91245200ebe89e468a1c54-Abstract-Conference.html).
48. Yan et al. (2026), [When Truth Is Distributed](https://arxiv.org/abs/2608.03421).
49. Anand & Pappas (2026), [Resilient Consensus in Agentic AI](https://arxiv.org/abs/2606.15024).
50. Khan et al. (2026), [The Adaptive Interrogator](https://aclanthology.org/2026.findings-acl.1348/).
51. He et al. (2025), [Red-Teaming LLM Multi-Agent Systems via Communication Attacks](https://aclanthology.org/2025.findings-acl.349/).
52. Barbi, Yoran & Geva (2025), [Preventing Rogue Agents Improves Multi-Agent Collaboration](https://aclanthology.org/2025.realm-1.34/).

## Ranked recommendation

1. **Conditional pilot: adaptive verification (B).** It has the clearest method-shaped residual, but only if the measured endogenous audit law predicts a real instability that a matched fixed verifier avoids.
2. **Conditional pilot: Dec-POMDP policy-realization regret (B).** Treat CalBench as the benchmark invalidator. Lead with legal decentralized-policy evaluation and the two-optimum decomposition, not “oracle-grounded coordination.”
3. **Hold: endogenous teammate co-evolution (C).** Run only a cheap falsification study of per-memory validity hazard; do not build another self-evolution framework.
4. **Hold: convention/deception repair (C).** It needs one formal adversarial-recovery game that cannot be reduced to DICE, clarification, or Byzantine filtering.
5. **Reject as currently framed: shared memory commons (C).** Re-enter only with an incentive-compatible maintenance mechanism and equilibrium result.
6. **Reject: sanctioning under unreliable blame (C).** The historical and current collision set is too strong without theorem-level novelty.

## Final novelty calibration

- **Verified A-level gap:** none.
- **Plausible but unverified B-level residuals:** endogenous trust-feedback stabilization; exact legal-policy realization regret with separate centralized/decentralized optima.
- **Crowded C-level residuals:** strategic causal-evidence manipulation for sanctions; incentive-compatible memory maintenance; per-memory hazard from teammate evolution; convention recovery after strategic corruption.
- **Directly dead broad claims:** oracle-grounded LLM coordination, adaptive/budgeted audits, reputation/punishment for cooperation, governed shared memory, collaborative self-evolution, and generic clarification/repair.

This is a novelty kill audit, not a priority proof. Before submission, rerun the six exact residual searches and inspect citations/revisions of CalBench, Itkin, Meta-Team, Talk is Cheap, and the 2026 institutional-memory papers.
