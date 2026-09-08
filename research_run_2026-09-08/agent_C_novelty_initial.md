# Agent C — Novelty audit (initial pass)

**Search cut-off:** 2026-09-08  
**Role:** adversarial novelty auditor; this document tries to invalidate, not promote, the hypotheses.  
**Evidence standard:** primary proceedings, journal pages, OpenReview, and arXiv records. Search-result scarcity is not treated as novelty. 2026 arXiv-only papers are marked as preprints and should not be treated as peer-reviewed validation.

## Executive verdict

| Hypothesis as supplied | Conservative class | Verdict |
|---|---:|---|
| 1. Dec-POMDP-optimum-grounded evaluation and solver-guided joint-policy commitment for LLM teams | **B — partially explored** | The compound formulation was not found verbatim, but every major ingredient is occupied: exact/approximate Dec-POMDP solving, commitment-driven joint-policy search, LLM collaboration explicitly formulated as a Dec-POMDP, and LLM coordination benchmarks with optimal answers. Only a narrow **policy-realization-gap** formulation remains defensible. |
| 2. Strategic adaptive verification under uncertainty / scarce oversight | **D — already addressed as a broad gap** | 2025–2026 work directly studies strategic agents with adaptive costly audits, LLM fleets with adversarially miscalibrated confidence under a small audit budget, and budgeted runtime audit placement in LLM-MAS dependency graphs. A narrower endogenous-response/noisy-verifier game may remain, but it is a new formulation rather than evidence for the original broad claim. |
| 3a. Peer sanctioning under unreliable blame | **C — mostly solved / crowded** | Imperfect monitoring, wrongful punishment, noisy sanctioning, blame attribution under policy uncertainty, and learned/endogenous reputation have all been studied. Porting the intersection to LLM agents is not enough. |
| 3b. Shared agent memory as a commons | **C — framing occupied; mechanism question partly open** | A 2026 workshop paper explicitly calls shared memory an “artificial commons”; 2026 preprints formalize governed fleet memory, collaborative-memory selection, and poisoning-resistant authority. The residual must be an actual incentive/mechanism-design result, not the commons metaphor or provenance/access-control engineering. |

**Bottom line:** Hypothesis 1 is the only one of the three worth retaining for deeper audit, and only after narrowing it to a measurable gap between a solved optimal contingent joint policy and what black-box language agents actually execute under decentralized private histories. Hypothesis 2 should be rewritten from scratch around an interaction not covered by Dai et al., Zavattari et al., or BRA-Audit. Hypothesis 3a should be rejected. Hypothesis 3b may survive only as a formal public-goods/mechanism-design problem whose agents strategically decide whether to write, verify, challenge, or repair shared memory.

---

## Classification rubric

- **A — clearly novel:** no close prior formulation found after exact, semantic, older-term, and latest-work searches.
- **B — partially explored:** substantial related work exists, but a technically meaningful residual formulation is not directly solved.
- **C — mostly solved:** only a narrow intersection, domain transfer, or incremental relaxation remains.
- **D — already solved/addressed:** a close paper directly formulates and studies the proposed problem at the supplied level of specificity.

No supplied hypothesis earns A in this pass.

---

# H1. Dec-POMDP-optimum-grounded evaluation and solver-guided joint-policy commitment for LLM teams

## Kill searches used

Exact and semantic variants included: `Dec-POMDP LLM multi-agent`, `LLM optimal joint policy benchmark`, `joint policy commitment`, `commitment-driven distributed joint policy search`, `solver-guided joint policy`, `optimal coordination LLM`, `Dec-POMDP communication suggested joint actions`, `joint policy realization`, `zero-shot coordination optimal conventions`, and 2025–2026 combinations of those terms.

## Strongest invalidating literature

1. **Witwicki & Durfee, “Commitment-Driven Distributed Joint Policy Search,” AAMAS 2007.** The paper represents probabilistic commitments as constraints on local policies, uses linear programming to compute commitment-satisfying local policies, and searches commitment space for near-optimal or (under exhaustive search) globally optimal joint policies. This is a direct collision with the algorithmic phrase “solver-guided joint-policy commitment,” though it uses restricted decentralized MDPs rather than black-box LLM agents. [DOI](https://doi.org/10.1145/1329125.1329216); [AAMAS program](https://www.ifaamas.org/Proceedings/aamas07/html/tec16_08.html).
2. **Liu, Chen & Amato, “Improved Multi-Agent Collaboration with Multi-Turn Reinforcement Learning,” NeurIPS 2025 workshop.** MAGRPO explicitly models LLM collaboration as a cooperative Dec-POMDP and optimizes a joint reward across multi-turn coding interactions. This invalidates any claim that formulating LLM collaboration as a Dec-POMDP is missing. [NeurIPS page](https://neurips.cc/virtual/2025/128017).
3. **Agashe et al., “LLM-Coordination,” Findings of NAACL 2025.** It evaluates agentic coordination in four pure-coordination games and includes CoordQA questions with clear optimal solutions for environment comprehension, theory of mind, and joint planning. This invalidates a broad claim that LLM coordination has not been evaluated against optimal decisions. It does **not** compare full contingent language-agent policies to a solved Dec-POMDP optimum. [ACL Anthology](https://aclanthology.org/2025.findings-naacl.448/).
4. **Asmar & Kochenderfer, “Efficient Multiagent Planning via Shared Action Suggestions,” AAAI 2026.** In Dec-POMDP-Com, agents share suggested joint actions, maintain possible beliefs about other agents, and use a centralized policy while avoiding full observation sharing; experiments report performance comparable to centralized methods on standard Dec-POMDP benchmarks. This is dangerously close to a solver-provided coordination/commitment channel. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/40171).
5. **Wu, Zilberstein & Chen, “Multi-Agent Online Planning with Communication,” ICAPS 2009.** Agents maintain common joint-history pools so they derive the same joint policy and communicate when local observations make that common pool inconsistent. This is an older exact semantic neighbor for maintaining joint-policy coordination under decentralized observations. [ICAPS](https://ojs.aaai.org/index.php/ICAPS/article/view/13366).
6. **You et al., “Monte-Carlo Search for an Equilibrium in Dec-POMDPs,” UAI 2023.** MC-JESP searches finite-state-controller equilibria using only a generative simulator and is competitive with offline solvers. It supplies a practical solver baseline, though it targets equilibrium rather than global optimum. [PMLR](https://proceedings.mlr.press/v216/you23a.html).
7. **Gessler et al., “OvercookedV2: Rethinking Overcooked for Zero-Shot Coordination,” ICLR 2025.** It argues ordinary Overcooked ZSC failure is largely a state-coverage artifact, introduces asymmetric information and stochasticity, and includes test-time protocol formation. This is a warning that an LLM-vs-optimum benchmark can measure distribution coverage or protocol formation rather than commitment. [arXiv](https://arxiv.org/abs/2503.17821).
8. **Ding et al., “Sparse Action-Dependent Policy Iteration under Coordination Structures,” UAI 2026.** The paper supplies a recent optimality/convergence result for structured coordination and deep MARL, increasing the burden for any “solver guidance yields optimal coordination” contribution. [PMLR](https://proceedings.mlr.press/v337/ding26a.html).

Additional pressure comes from **SILO-BENCH** (ACL 2026), which uses tasks with exact ground-truth answers and optimal communication-complexity levels, though it is distributed computation rather than Dec-POMDP control ([ACL](https://aclanthology.org/2026.acl-long.1354/)); and **ACPO** (2026 preprint), whose agents sequentially commit actions under beliefs while jointly implementing an exact joint-policy gradient ([arXiv](https://arxiv.org/abs/2606.30072)).

## Closest paper most likely to invalidate the gap

**Commitment-Driven Distributed Joint Policy Search (Witwicki & Durfee, 2007)** is the closest invalidator of the proposed algorithmic core. It already turns commitments into policy constraints and searches those commitments to recover high-quality joint policies. If the claimed contribution is merely “a solver computes a joint policy and agents commit to it,” the gap is dead.

For the **LLM-specific Dec-POMDP formalization**, the closest invalidator is **MAGRPO (Liu et al., 2025)**. For the **evaluation** portion, the closest invalidator is **LLM-Coordination (Agashe et al., 2025)**.

## Exact residual difference

The only residual I could defend is:

> Given a small Dec-POMDP for which an exact solver supplies an optimal **contingent** joint policy, quantify and reduce the **policy-realization regret** of black-box language agents that must execute their local policy components from private action-observation histories, without exposing hidden observations or centralizing execution.

That differs from prior work in four simultaneous ways:

1. The reference object is a solved full-horizon contingent joint policy, not only a final answer, an optimal next move, or empirical reward.
2. The measured failure is execution fidelity/regret conditional on each agent's private history, not raw task success.
3. The agents are black-box language policies interpreting a symbolic policy/commitment artifact, not trained tabular/neural controllers whose policy is the artifact.
4. The intervention must preserve decentralized information constraints; simply revealing the global state or asking one central LLM to choose all actions collapses the scientific question.

## Why the residual may still fail novelty review

- **Trivial-interface risk:** serializing an exact policy tree into a prompt can look like engineering or privileged planning assistance rather than an algorithmic contribution.
- **Tiny-domain risk:** exact Dec-POMDP optima are feasible only on small instances; reviewers may see a diagnostic toy benchmark.
- **Old-ideas risk:** commitment constraints, common-knowledge joint-policy execution, and suggested-action communication already exist. The paper must discover a new phenomenon or objective, not rename them for LLMs.
- **Hidden single-agent reduction:** a centralized solver plus centrally distributed instructions may leave no real multi-agent decision problem.
- **Policy-class mismatch:** natural-language LLM actions may not map cleanly to the finite action/observation alphabets required by exact solvers.
- **Recent-work risk:** the 2025 MAGRPO paper and 2026 AAAI action-suggestion paper make broad positioning untenable; 2026 work is still moving quickly.

## Conservative classification

**B — partially explored.**  
**Residual novelty confidence:** Medium-low.  
**Recommendation:** Retain only for deeper audit if it is framed around a new measurable realization-regret phenomenon, an information-preserving policy compiler, and falsifiable hypotheses about when language agents deviate from optimal contingent commitments. Reject the generic “Dec-POMDP grounding for LLM collaboration” and “solver-guided commitment” claims.

---

# H2. Strategic adaptive verification under uncertainty / scarce oversight

## Kill searches used

Variants included: `strategic agents costly verification`, `adaptive costly audits`, `scarce audits mechanism design`, `budgeted noisy inspection`, `audit-budget LLM agent fleet`, `miscalibrated confidence auditing`, `budgeted runtime auditing LLM MAS`, `verification allocation uncertainty`, `inspection games`, `monitoring mechanism design`, `truthfulness on a budget`, and 2025–2026 work on agentic oversight and verifier allocation.

## Strongest invalidating literature

1. **Dai, Blanchard & Jaillet, “Non-Monetary Mechanism Design without Distributional Information: Using Scarce Audits Wisely,” COLT 2025 extended abstract / full preprint.** This is a repeated allocation problem with strategic agents, no prior over utility distributions, expensive audits that reveal truth, adaptive future punishments, and welfare-regret/audit-complexity guarantees. It obtains \(O(K^2)\) welfare regret with \(O(K^3\log T)\) expected audits and includes lower bounds. This directly occupies “strategic adaptive verification with scarce oversight.” [PMLR](https://proceedings.mlr.press/v291/dai25a.html); [full arXiv](https://arxiv.org/abs/2502.08412).
2. **Zavattari, Tommasi & Prencipe, “One Human, N Agents: Audit-Budget Allocation for LLM Agent Fleets under Miscalibrated, Correlated Confidence,” 2026 preprint.** It studies one human with \(B\ll N\) audits, adversarially miscalibrated self-reported confidence, correlated errors, noisy inspection, and conditions under which confidence-ranked auditing is worse than random. This is the closest LLM-fleet collision. [arXiv](https://arxiv.org/abs/2607.28317).
3. **Wang et al., “BRA-Audit: Budgeted Runtime Auditing for LLM Multi-Agent Systems via Cumulative-Exposure Audit-Point Placement,” 2026 preprint.** It models LLM-MAS execution as a dynamic dependency graph and places audit points under a fixed audit-call budget to limit unchecked exposure, with localized recovery. This occupies adaptive budgeted verification inside interacting workflows. [arXiv](https://arxiv.org/abs/2608.14668).
4. **Patel, “Anytime Verified Agents: Adaptive Compute Allocation for Reliable LLM Reasoning under Budget Constraints,” TMLR 2026.** It jointly allocates compute among search, sampling, verification, and tools using uncertainty and estimated marginal gains. It is mostly single-agent reasoning, but kills generic “adaptive verification under a budget” novelty. [OpenReview](https://openreview.net/forum?id=JMDCMf7mlF).
5. **Mguni et al., “MANSA: Learning Fast and Slow in Multi-Agent Systems,” ICML 2023.** A learned selector invokes centralized learning under a limited budget; MANSA-B learns optimal use of the central-learning call budget under its assumptions. It is not auditing, but it is an older multi-agent analogue of scarce expensive oversight/intervention. [PMLR](https://proceedings.mlr.press/v202/mguni23a.html).
6. **Ferraioli & Ventre, “Obvious Strategyproofness Needs Monitoring for Good Approximations,” AAAI 2017.** It shows monitoring/scrutiny can enable optimal mechanisms, grounding the older mechanism-design lineage. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/10588).

## Closest paper most likely to invalidate the gap

**Dai, Blanchard & Jaillet (2025)** is the strongest invalidator because it simultaneously contains strategic adaptation, repeated interaction, uncertainty about distributions, expensive audits, adaptive punishments, regret, and audit bounds. The phrase “strategic adaptive verification under scarce oversight” is not a novel research question after this paper.

For an explicitly LLM-fleet formulation, **One Human, N Agents (2026 preprint)** is the closest invalidator. Its peer-review status must be checked before final positioning, but it cannot be ignored in a novelty claim.

## Exact residual difference

A narrower problem may remain:

> In an interdependent multi-agent workflow, choose noisy verification actions when agents strategically change effort, communication, routing, or concealment in response to the audit policy, so that auditing changes both future error probabilities and the dependency graph itself.

This is not directly covered by the located work:

- Dai et al. audit the round winner and assume a powerful audit reveals true utility; their strategic object is resource-allocation reporting, not a changing collaborative dependency graph.
- Zavattari et al. replay audit policies over recorded confidence/error traces; the agents do not appear to learn or change workflow behavior in response to being audited.
- BRA-Audit adapts audit locations to dependency/exposure structure, but its scheduler treats auditors/audit outcomes as trusted and does not model equilibrium adaptation by the audited agents.
- AVA allocates compute but does not study multiple strategic actors.

## Why even the residual is risky

- Inspection games, principal-agent learning, strategic classification, monitoring mechanisms, and repeated games under imperfect public monitoring are large older literatures; an equivalent formulation may use non-LLM vocabulary.
- Combining Dai-style incentives with BRA-Audit-style graphs could be judged “method A + method B” unless a new impossibility result, equilibrium phenomenon, or regret lower bound appears.
- If agents are all controlled by the same designer and share a reward, calling them “strategic” is questionable; model misspecification is not strategic behavior.
- A fallible verifier can create an identifiability problem that makes evaluation depend on unavailable ground truth.

## Conservative classification

**D — already addressed as supplied.**  
**Narrow residual:** B, medium-low confidence, requiring a substantially new formal game.  
**Recommendation:** Reject the supplied broad gap. If retained, rename it around **endogenous audit response in interdependent workflows with noisy verification**, and make clear that it extends rather than precedes Dai et al., Zavattari et al., and BRA-Audit.

---

# H3a. Peer sanctioning under unreliable blame

## Kill searches used

Variants included: `peer punishment imperfect monitoring`, `noisy public monitoring punishment`, `wrongful punishment cooperation`, `blame attribution policy uncertainty multi-agent`, `sanctioning under noise`, `reputation disagreement`, `bottom-up reputation MARL`, `punishment noise public goods`, and `learning punishment MARL`.

## Strongest invalidating literature

1. **Fischer, Grechenig & Meier, “Monopolizing Sanctioning Power under Noise Eliminates Perverse Punishment But Does Not Increase Cooperation,” Frontiers in Behavioral Neuroscience 2016.** A repeated public-goods experiment varies signal accuracy and decentralized versus centralized sanctioning. It directly studies punishment decisions based on unreliable information. [Primary full text](https://www.frontiersin.org/journals/behavioral-neuroscience/articles/10.3389/fnbeh.2016.00180/full).
2. **Salahshour, Oberhauser & Smerlak, “The Cost of Noise: Stochastic Punishment Falls Short of Sustaining Cooperation in Social Dilemma Experiments,” PLOS ONE 2022.** It finds that punishment noise lowers contributions and welfare and increases antisocial punishment. [PLOS](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0263028); [arXiv](https://arxiv.org/abs/2109.13547).
3. **van Miltenburg, Przepiorka & Buskens, “Consensual punishment does not promote cooperation in the six-person prisoner’s dilemma game with noisy public monitoring,” PLOS ONE 2017.** It directly compares peer-punishment decision rules under misobserved cooperation/defection. [Primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC5703489/).
4. **Triantafyllou, Singla & Radanovic, “On Blame Attribution for Accountable Multi-Agent Sequential Decision Making,” NeurIPS 2021.** It formalizes blame methods in cooperative multi-agent MDPs and explicitly accounts for uncertainty about agents' policies, experimentally testing robustness. [arXiv](https://arxiv.org/abs/2107.11927).
5. **Ren et al., “Bottom-Up Reputation Promotes Cooperation with Multi-Agent Reinforcement Learning,” AAMAS 2025.** Agents jointly learn dilemma and evaluation policies; private assessments may disagree, and the paper studies biased social information. This already couples learned judgment/reputation to cooperation. [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1745.pdf).
6. **Dasgupta & Musolesi, “Investigating the Impact of Direct Punishment on the Emergence of Cooperation in Multi-agent Reinforcement Learning Systems,” JAAMAS / AAAI 2026 abstract reprint.** It jointly examines direct punishment, third-party punishment, partner selection, and reputation in MARL populations. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/41376).
7. **Ren et al., “Reputation as a Solution to Cooperation Collapse in LLM-based MASs,” AAMAS 2026.** RepuNet uses direct encounters, gossip, dynamic reputations, and network rewiring to sustain LLM-agent cooperation. This kills “add reputation/sanctions to LLM societies” as a gap. [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/UEHN4980.pdf).

## Closest paper most likely to invalidate the gap

For the exact unreliable-information-to-punishment phenomenon, **Monopolizing Sanctioning Power under Noise… (2016)** is the closest. For computational multi-agent blame, **On Blame Attribution… (2021)** is the closest. Together they occupy nearly the whole proposed intersection.

## Residual difference and why it is insufficient

One can still formulate learned peer sanctions driven by uncertain **causal** blame in long-horizon Markov games, with endogenous manipulation of the evidence used for blame. I did not find one located paper that simultaneously learns (i) causal blame inference, (ii) sanction allocation, and (iii) strategic evidence manipulation by sanctioned agents.

However, this residual currently looks like a crowded three-way combination rather than a clean missing problem. A paper would need a non-obvious theorem or a sharply demonstrated phase transition (for example, a calibrated-blame threshold beyond which decentralized sanctions reduce welfare) to escape incrementalism.

## Conservative classification

**C — mostly solved/crowded.**  
**Residual novelty confidence:** Low.  
**Recommendation:** Reject from the top set unless a genuinely new formal result is developed before experiments.

---

# H3b. Shared agent memory as a commons

## Kill searches used

Variants included: `shared memory commons multi-agent AI`, `artificial commons shared memory`, `governed shared memory LLM MAS`, `collaborative memory governance`, `memory poisoning multi-agent agents`, `provenance shared memory agents`, `institutional memory LLM agents`, and 2025–2026 work on write/read/repair authority.

## Strongest invalidating literature

1. **Truong et al., “Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment,” ICML 2026 Trustworthy AI4GOOD workshop spotlight.** It explicitly labels shared memory/context as an **artificial commons** and asks who can write, edit, verify, roll back, or repair it; it also discusses memory pollution and verification free-riding. This directly occupies the framing. [OpenReview PDF](https://openreview.net/attachment?id=5ow68CzpRg&name=pdf).
2. **Margalit et al., “Governed Shared Memory for Multi-Agent LLM Systems,” 2026 preprint.** It formalizes the fleet-memory problem and implements scope, temporal supersession, provenance, and propagation controls, evaluated with a reproducible harness. This occupies governance primitives and systems evaluation. [arXiv](https://arxiv.org/abs/2606.24535).
3. **Cuadros et al., “Governed Collaborative Memory as Artificial Selection in LLM-Based Multi-Agent Systems,” 2026 viewpoint preprint.** It asks which candidate memories become shared institutional state and distinguishes governance/selection regimes, layered memory, provenance, correction, and role preservation. [arXiv](https://arxiv.org/abs/2605.04264).
4. **Louck, “Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees,” 2026 preprint.** It formalizes laundering attacks on memory authority, proves content/lineage defenses insufficient under its threat model, and proposes origin-bound authority with Sybil-resistant corroboration. This strongly occupies the security/provenance side. [arXiv](https://arxiv.org/abs/2606.24322).
5. **Ren et al., RepuNet, AAMAS 2026.** The system stores self- and peer-reputations in agent memory databases and lets gossip alter future network interaction. It is not a commons mechanism, but it demonstrates that socially consequential shared historical information and reputation-mediated access are already active AAMAS topics. [AAMAS PDF](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/UEHN4980.pdf).

## Closest paper most likely to invalidate the gap

**Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment (2026)** most directly invalidates the phrase “shared agent memory as a commons”: it uses essentially that exact framing and enumerates write, verification, rollback, pollution, and free-riding questions.

**Governed Shared Memory for Multi-Agent LLM Systems (2026)** is the closest implementation invalidator.

## Exact residual difference

A defensible residual would be:

> Model shared memory as a repeated public-goods/common-pool game in which heterogeneous agents choose costly write, verify, challenge, supersede, and repair actions; design a decentralized mechanism that makes epistemically useful maintenance incentive-compatible under uncertain contribution quality and provenance.

The located 2026 papers do **not** provide that full result:

- The institutional-design paper is a workshop agenda/formal sketch, not a solved dynamic mechanism.
- MemClaw supplies systems controls but does not model self-interested agents, equilibrium, welfare, or free-riding on verification labor.
- The artificial-selection viewpoint proposes governance regimes but not an incentive-compatible algorithm or equilibrium analysis.
- The origin-bound-authority paper addresses adversarial poisoning/security, not costly public-good maintenance or social welfare.

## Why the residual remains high-risk

- The exact “artificial commons” story is already published; novelty must come entirely from the formal mechanism and results.
- Classical public-goods, common-pool-resource, peer-prediction, reputation, and costly-verification mechanisms may transfer almost directly.
- If all agents share one system reward, free-riding must arise from local cost/partial observability or it is artificial.
- A benchmark-only contribution measuring memory pollution will be compared unfavorably with MemClaw/ArgusFleet and poisoning benchmarks.
- Three of the most direct technical sources are recent preprints; priority can move before submission.

## Conservative classification

**C — framing and engineering problem occupied; formal mechanism residual partially open.**  
**Residual novelty confidence:** Medium-low.  
**Recommendation:** Do not use “shared memory as a commons” as the novelty claim. If pursued, lead with a new repeated game, impossibility/bound, and incentive-compatible maintenance mechanism; cite the 2026 institutional-design paper as prior framing.

---

# Commonly suggested “gaps” that should be killed or heavily narrowed

| Common suggestion | Class | Why it is already solved or crowded | Closest primary work |
|---|---:|---|---|
| “We need a benchmark for multi-agent LLM coordination.” | D | Multiple broad and focused benchmarks now cover collaboration/competition, pure coordination, exact distributed-computation answers, scale, topology, and communication cost. | [MultiAgentBench, ACL 2025](https://aclanthology.org/2025.acl-long.421/); [LLM-Coordination, NAACL 2025](https://aclanthology.org/2025.findings-naacl.448/); [SILO-BENCH, ACL 2026](https://aclanthology.org/2026.acl-long.1354/) |
| “Automatically assign roles to LLM agents.” | D | Role embeddings, task-specific automatic role differentiation, and dynamic model-role assignment are explicit contributions. | [Advancing Collaborative Debates with Role Differentiation, ACL 2025](https://aclanthology.org/2025.acl-long.1105/); [Dynamic Role Assignment, 2026 preprint](https://arxiv.org/abs/2601.17152) |
| “Build heterogeneous LLM teams automatically.” | D | Heterogeneous models, roles, topologies, cost, and generalization to unseen models/roles are directly optimized. | [Hetero-Designer, ACL 2026](https://aclanthology.org/2026.acl-long.1272/); [RouterHGC, Findings ACL 2026](https://aclanthology.org/2026.findings-acl.1589/) |
| “Dynamically choose which agent/workflow to run to save tokens.” | D | Next-agent prediction, context selection, workflow cascades, and cost-aware routing are established. | [AnyMAC, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.584/); [LLM-as-Scheduler, ACL 2026](https://aclanthology.org/2026.acl-long.581/) |
| “Use reputation to prevent cooperation collapse in LLM societies.” | D | RepuNet is an AAMAS 2026 main-track paper built around exactly this claim; bottom-up learned reputation is already in AAMAS 2025 MARL. | [RepuNet, AAMAS 2026](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/UEHN4980.pdf); [LR2, AAMAS 2025](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1745.pdf) |
| “Study social learning/norm formation for cooperation in LLM agents.” | D | The exact title appears in AAMAS 2026; sequential public-goods incentives for multi-LLM systems also exist. | [Social Learning and Collective Norm Formation, AAMAS 2026](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/CZDC3237.pdf); [Everyone Contributes!, AAMAS 2026](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/SJPO2377.pdf) |
| “Make multi-agent communication cost-aware/adaptive.” | C/D | The literature now optimizes why/whom to communicate, communication topology, next-agent/context selection, and exact communication-complexity strata. A new paper needs a distinct strategic or information-theoretic phenomenon. | [Why and Whom to Communicate?, AAMAS 2026](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/TAYO7266.pdf); [AnyMAC](https://aclanthology.org/2025.emnlp-main.584/); [SILO-BENCH](https://aclanthology.org/2026.acl-long.1354/) |
| “Defend multi-agent LLMs from one malicious agent/message attack.” | D | Communication interception, topology-guided detection/remediation, pragmatic prompt attacks, and cooperative attackers all have dedicated papers. | [AiTM red-teaming, Findings ACL 2025](https://aclanthology.org/2025.findings-acl.349/); [G-Safeguard, ACL 2025](https://aclanthology.org/2025.acl-long.359/); [STAR, 2026 preprint](https://arxiv.org/abs/2605.28104) |
| “Study cross-agent prompt-composition attacks.” | D | ACL 2026 explicitly studies conjunctive triggers/templates across star, chain, and DAG routing. | [Conjunctive Prompt Attacks, ACL 2026](https://aclanthology.org/2026.acl-long.1577/) |
| “Handle changing/unknown teammates in cooperative MARL.” | C | Open Dec-POMDPs, ad hoc teamwork, fast teammate adaptation, and modern ZSC are mature. A new gap must specify a genuinely new non-stationarity or information constraint. | [Fast Teammate Adaptation, UAI 2023](https://proceedings.mlr.press/v216/zhang23a.html); [OvercookedV2](https://arxiv.org/abs/2503.17821) |
| “Model LLM collaboration as a Dec-POMDP and train jointly.” | D | MAGRPO does this explicitly, with joint reward and multi-turn LLM training. | [MAGRPO, NeurIPS 2025 workshop](https://neurips.cc/virtual/2025/128017) |
| “Govern shared memory/provenance for multiple agents.” | C/D | Governance primitives, institutional framing, collaborative selection, and poisoning-resistant authority all appeared in 2026. A residual must be more than access control or provenance. | [Governed Shared Memory](https://arxiv.org/abs/2606.24535); [Institutional Design](https://openreview.net/attachment?id=5ow68CzpRg&name=pdf); [Origin-Bound Authority](https://arxiv.org/abs/2606.24322) |

---

# Unique-paper ledger and count

**Count: 40 unique papers/proceedings records examined in this pass.** “Examined” means the primary abstract/proceedings record was inspected; for 17 of the closest items, method/full-text passages were also inspected. Duplicate arXiv/proceedings versions count once.

## Dec-POMDP, coordination, commitment, and evaluation (14)

1. Witwicki & Durfee (2007), *Commitment-Driven Distributed Joint Policy Search*. [DOI](https://doi.org/10.1145/1329125.1329216)
2. Wu, Zilberstein & Chen (2009), *Multi-Agent Online Planning with Communication*. [ICAPS](https://ojs.aaai.org/index.php/ICAPS/article/view/13366)
3. Kao & Subramanian (2022), *Common Information based Approximate State Representations in MARL*. [PMLR](https://proceedings.mlr.press/v151/kao22a.html)
4. You et al. (2023), *Monte-Carlo Search for an Equilibrium in Dec-POMDPs*. [PMLR](https://proceedings.mlr.press/v216/you23a.html)
5. Zhang et al. (2023), *Fast Teammate Adaptation in the Presence of Sudden Policy Change*. [PMLR](https://proceedings.mlr.press/v216/zhang23a.html)
6. Mguni et al. (2023), *MANSA: Learning Fast and Slow in Multi-Agent Systems*. [PMLR](https://proceedings.mlr.press/v202/mguni23a.html)
7. Koops, Junges & Jansen (2024), *Approximate Dec-POMDP Solving Using Multi-Agent A\**. [arXiv](https://arxiv.org/abs/2405.05662)
8. Liu, Chen & Amato (2025), *Improved Multi-Agent Collaboration with Multi-Turn Reinforcement Learning*. [NeurIPS](https://neurips.cc/virtual/2025/128017)
9. Agashe et al. (2025), *LLM-Coordination*. [ACL](https://aclanthology.org/2025.findings-naacl.448/)
10. Zhu et al. (2025), *MultiAgentBench*. [ACL](https://aclanthology.org/2025.acl-long.421/)
11. Gessler et al. (2025), *OvercookedV2*. [arXiv](https://arxiv.org/abs/2503.17821)
12. Asmar & Kochenderfer (2026), *Efficient Multiagent Planning via Shared Action Suggestions*. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/40171)
13. Zhang et al. (2026), *SILO-BENCH*. [ACL](https://aclanthology.org/2026.acl-long.1354/)
14. Matsunaga et al. (2026), *ACPO: Agent-Chained Policy Optimization*. [arXiv](https://arxiv.org/abs/2606.30072)

## Verification, auditing, and monitoring (7)

15. Ferraioli & Ventre (2017), *Obvious Strategyproofness Needs Monitoring for Good Approximations*. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/10588)
16. Dai, Blanchard & Jaillet (2025), *Non-Monetary Mechanism Design without Distributional Information: Using Scarce Audits Wisely*. [PMLR](https://proceedings.mlr.press/v291/dai25a.html)
17. Patel (2026), *Anytime Verified Agents*. [OpenReview](https://openreview.net/forum?id=JMDCMf7mlF)
18. Zavattari, Tommasi & Prencipe (2026), *One Human, N Agents*. [arXiv](https://arxiv.org/abs/2607.28317)
19. Wang et al. (2026), *BRA-Audit*. [arXiv](https://arxiv.org/abs/2608.14668)
20. Itkin (2026), *Delayed Verification Destabilizes Multi-Agent LLM Belief*. [arXiv](https://arxiv.org/abs/2606.27409)
21. Goshen et al. (2025), *Estimating Value of Assistance for Online POMDP Robotic Agents*. [PMLR](https://proceedings.mlr.press/v305/goshen25a.html)

## Sanctions, blame, reputation, and cooperation (9)

22. Fischer, Grechenig & Meier (2016), *Monopolizing Sanctioning Power under Noise…*. [Frontiers](https://www.frontiersin.org/journals/behavioral-neuroscience/articles/10.3389/fnbeh.2016.00180/full)
23. van Miltenburg, Przepiorka & Buskens (2017), *Consensual punishment…with noisy public monitoring*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5703489/)
24. Triantafyllou, Singla & Radanovic (2021), *On Blame Attribution for Accountable Multi-Agent Sequential Decision Making*. [arXiv](https://arxiv.org/abs/2107.11927)
25. Salahshour, Oberhauser & Smerlak (2022), *The Cost of Noise*. [PLOS](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0263028)
26. Ren et al. (2025), *Bottom-Up Reputation Promotes Cooperation with MARL*. [AAMAS](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1745.pdf)
27. Ren et al. (2026), *Reputation as a Solution to Cooperation Collapse in LLM-based MASs*. [AAMAS](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/UEHN4980.pdf)
28. Liang et al. (2026), *Everyone Contributes! Incentivizing Strategic Cooperation in Multi-LLM Systems via Sequential Public Goods Games*. [AAMAS](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/SJPO2377.pdf)
29. Gupta et al. (2026), *The Role of Social Learning and Collective Norm Formation in Fostering Cooperation in LLM Multi-Agent Systems*. [AAMAS](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/CZDC3237.pdf)
30. Dasgupta & Musolesi (2026), *Investigating the Impact of Direct Punishment…in MARL Systems*. [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/41376)

## Shared memory and institutional governance (4)

31. Cuadros et al. (2026), *Governed Collaborative Memory as Artificial Selection*. [arXiv](https://arxiv.org/abs/2605.04264)
32. Margalit et al. (2026), *Governed Shared Memory for Multi-Agent LLM Systems*. [arXiv](https://arxiv.org/abs/2606.24535)
33. Louck (2026), *Securing LLM-Agent Long-Term Memory Against Poisoning*. [arXiv](https://arxiv.org/abs/2606.24322)
34. Truong et al. (2026), *Multi-Agent AI Systems Need Institutional Design, Not Just Model-Level Alignment*. [OpenReview](https://openreview.net/attachment?id=5ow68CzpRg&name=pdf)

## Dynamic architecture and security (6)

35. Li et al. (2025), *Advancing Collaborative Debates with Role Differentiation through MARL*. [ACL](https://aclanthology.org/2025.acl-long.1105/)
36. Wang et al. (2025), *AnyMAC*. [ACL](https://aclanthology.org/2025.emnlp-main.584/)
37. He et al. (2025), *Red-Teaming LLM Multi-Agent Systems via Communication Attacks*. [ACL](https://aclanthology.org/2025.findings-acl.349/)
38. Wang et al. (2025), *G-Safeguard*. [ACL](https://aclanthology.org/2025.acl-long.359/)
39. Zhang et al. (2026), *Hetero-Designer*. [ACL](https://aclanthology.org/2026.acl-long.1272/)
40. Xiang et al. (2026), *LLM-as-Scheduler*. [ACL](https://aclanthology.org/2026.acl-long.581/)

---

# What should proceed to the next research stage

1. **Proceed, but narrow H1:** formulate and measure **decentralized policy-realization regret** against an exactly solved Dec-POMDP. The novelty claim must be the newly identified execution phenomenon or a principled information-preserving compiler/commitment mechanism—not the Dec-POMDP model itself.
2. **Do not proceed with H2 as written:** the broad gap is directly occupied. Only proceed after writing a new formal game with endogenous strategic response, noisy verification, and changing workflow dependencies, then re-run searches in inspection games, strategic classification, principal-agent bandits, and imperfect-monitoring repeated games.
3. **Reject H3a:** unreliable blame plus peer punishment is too mature and crowded absent a theorem-level surprise.
4. **Conditionally retain H3b:** only as an incentive-compatible shared-memory maintenance game. Treat the “artificial commons” metaphor, governance primitives, provenance, supersession, and poisoning defenses as prior work, not contribution.

## Final calibration

- **Verified gap:** None yet. An initial novelty audit cannot verify novelty, and all three hypotheses have close collisions.
- **Plausible gap requiring deeper verification:** H1's policy-realization-regret residual; H3b's incentive-compatible memory-maintenance residual; the radically narrowed endogenous-response version of H2.
- **Rejected/already addressed:** broad strategic adaptive scarce auditing; generic peer sanctioning under unreliable blame; generic “shared memory as commons”; generic Dec-POMDP formalization or optimal-move evaluation for LLM collaboration.
