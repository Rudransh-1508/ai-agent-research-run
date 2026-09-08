# Agent C — second-wave novelty kill test

**Search cut-off:** 8 September 2026  
**Inputs crosswalked:** `agent_A_cartographer.md`, `agent_B_gap_hunter.md`, `agent_E_feasibility.md`, `agent_H_opportunity.md`, and `agent_C_novelty_initial.md`  
**Decision rule:** rejection is the default. A survivor means only that the searched literature did not collapse the *narrow residual formulation*; it is not a priority or “first” claim.

## Executive result

I collapsed the source agents' proposals into **42 distinct candidate formulations**. The crosswalk matters: for example, “latent capability in open teams,” “private capability task allocation,” and “coalition-only feedback” are one scientific family, not three gaps. I reject **32/42** and retain **10/42** for further review. Every survivor is **B (partially explored)**; none earns A.

The most consequential new kills are:

1. **Causal value of LLM-to-LLM interaction under matched compute — C/D.** A July 2026 *Nature Machine Intelligence* study already evaluates 260 compute-matched configurations and models when collaboration helps; equal-thinking-token work reaches the same confounding concern from another direction. The remaining causal-mediation analysis is useful science, but no longer a clean gap.
2. **Correlated-evidence / shared-ancestry aggregation — D as proposed.** *Epistemic Sybil Resistance* (submitted 1 September 2026) formalizes conditional evidential redundancy, proves report-only non-identifiability, models correlated extraction error, and validates an ancestry-aware aggregator with more than 20,000 controlled calls. A generic “do not count copies as independent evidence” project is preempted.
3. **Cross-implementation ZSC evaluation — D.** The August 2026 paper *Is Inter-Seed Cross-Play Enough?* introduces cross-implementation cross-play and runs the test directly.
4. **Generic sparse/directed adaptive communication — D.** DGSDC, published 5 September 2026, learns sparse directed interaction graphs from local relevance estimates. Strategic allocation of airtime remains distinct; ordinary graph sparsification does not.
5. **Descendant repair after retraction — C/D.** Distributed truth-maintenance systems already propagated retractions through justification networks in 1990–1994, and August 2026 ReTree explicitly repairs downstream summaries/branches. “Apply this to multi-agent LLM memory” is not enough.

The ten retained residuals are: exact-policy realization regret for language agents; source attribution of multi-agent non-stationarity; dual-control ad-hoc teamwork with a learning teammate; co-drifting protocol translation; payment-free allocation with private evolving capabilities and coalition-only outcomes; manipulation-resistant scarce bandwidth allocation; offline AHT identifiability with selective interaction; strategic teaching of an adaptive mechanism designer; endogenous-evidence trust calibration in human–AI teams; and cumulative fairness under churn with cheap identity resets.

## Classification rubric

- **A — clearly novel:** no close formulation found after exact, synonym, older-field, adjacent-field, and 2025–2026 searches.
- **B — partially explored:** the ingredients and close formulations exist, but a technically substantial conjunction remains.
- **C — mostly solved / incremental residual:** the remaining difference is likely an assumption tweak, new benchmark, or domain transfer.
- **D — directly occupied:** a paper already poses and substantially addresses the claimed problem.

## Unified candidate pool and duplicate crosswalk

| ID | Precise candidate after deduplication | Source crosswalk | Kill verdict | Reason |
|---|---|---|---:|---|
| U01 | Measure and reduce black-box language agents' regret in realizing local components of an exact contingent Dec-POMDP policy from private histories. | C-H1; related A planning map | **B — retain** | Exact-policy execution fidelity remains narrower than Dec-POMDP training, optimal-action QA, or old commitment search. |
| U02 | Use a solver to produce joint-policy commitments for LLM teams. | C-H1; E-F1 | **D** | Commitment-driven joint-policy search already turns commitments into policy constraints; suggested-joint-action Dec-POMDP methods are current. |
| U03 | Identify whether observed non-stationarity is exogenous drift, independent peer learning, or peer adaptation caused by the ego agent. | H02; A2/A8 | **B — retain** | 2026 causal teammate modeling separates context/noise from strategy, but not the full three-way interventional attribution problem. |
| U04 | Plan diagnostic actions when an unfamiliar teammate is itself learning from those actions. | B01; H02; E-F2 | **B — retain** | Team probing assumes a sufficiently stable target; opponent shaping assumes influence, but does not maintain a task-directed belief over an unknown partner learning rule. |
| U05 | Repeatedly allocate complementary tasks when capabilities are private, drifting/action-dependent, strategically reported, and only coalition success is observed, without transfers. | A1/A12; B06; H04; E-F2 | **B — retain** | Each ingredient is occupied, but their conjunction creates a nontrivial identification–incentive problem; an impossibility result may be the contribution. |
| U06 | Allocate teams by compatibility/complementarity rather than individual competence. | A12; E-F7 | **C** | CASH and heterogeneous team-formation/routing work already optimize skill combinations; a new paper needs private information or incentives, which is U05. |
| U07 | Track an online translation between two independently trained communication protocols while both protocols continue to drift, without paired meanings or shared grounding. | B02; A5; E-F5 | **B — retain** | Translation, community joining, and human-language grounding freeze or anchor at least one side; co-drift tracking/stability remains a defensible residual. |
| U08 | Repair a convention after teammate replacement or a mid-task model swap. | A5; E-F5/F8 | **C** | Open-team adaptation, protocol formation, and replacement recovery are crowded; without a new co-drift or strategic phenomenon this is an evaluation setting, not a gap. |
| U09 | Determine the fraction/topology of strategic entrants needed to covertly capture convention semantics while surface task success remains high. | H07; A5/A9 | **C** | Naming-game zealots, rogue-node manipulation, and committed-minority tipping thresholds already occupy the mechanism. Hidden semantic targeting is plausible but presently looks like an incremental attack objective. |
| U10 | Learn egalitarian communication that maximizes worst-partner value under capability asymmetry. | H06; A1 | **C** | Welfare objectives and heterogeneous communication already exist; the proposed difference is principally objective substitution unless accompanied by a theorem unavailable in generalized welfare MARL. |
| U11 | Learn when to verify strategic messages under costly audits and changing sender incentives. | B03; E-F3; H09; C-H2 | **D as broad claim** | Scarce-audit mechanism design, LLM fleet audit allocation, inspection games, evidence signaling, and 2026 runtime auditors directly cover the broad problem. |
| U12 | Allocate independent evidence gathering while discounting shared sources, shared models, and inherited messages. | A4/A7; B04 | **D** | Preempted by 1 September 2026 *Epistemic Sybil Resistance*, in addition to misinformation-propagation and debate-diversity work. |
| U13 | Allocate scarce speaking opportunities when senders can manipulate bids and the learned continuation-value estimator, with delayed endogenous message value and no transfers. | H01; B05 | **B — retain** | DALA auctions language-agent turns but trusts predicted value density; classic bandwidth auctions rely on transfers/verifiable outcomes. Strategic learned airtime capture is the residual. |
| U14 | Jointly control task actions, messages, queues, outages, and freshness. | B05; E-F1 | **C/D** | Queue-aware information control and September 2026 intermittent-communication auction/game coordination occupy the nonstrategic problem; adding variables is not novelty. |
| U15 | Certify when offline multi-team data identifies a safe policy for an unseen teammate and abstain/request minimal interaction when joint coverage is missing. | B09; A2 | **B — retain** | Offline MARL now diagnoses coordination shift, but teammate-conditional identifiability and a selective AHT guarantee are not directly supplied by the closest papers. |
| U16 | Handle changing or unknown teammates in cooperative MARL. | A1/A8; E-F2/F8 | **D as broad claim** | Open AHT, NAHT, rapid adaptation, ICRL4AHT, and ZSC already make this a mature problem statement. |
| U17 | Estimate the causal value of LLM inter-agent interaction under matched compute. | A3; B13 | **C/D** | July 2026 compute-matched 260-configuration analysis and April 2026 equal-token experiments directly target the confound. A causal decomposition is now a follow-up, not an open baseline question. |
| U18 | Design mechanisms robust to an unspecified learning algorithm or bounded strategic switches. | A6; B07; E-F6 | **C** | Dynamic mechanisms for learning agents, response-class guarantees, strategic arms, and adaptive mechanisms are established. “Any unknown learner” is too broad; deliberate shaping of the designer is U19. |
| U19 | Prevent participants from sacrificing current payoff to teach an online mechanism designer a favorable future tax/reward/allocation rule. | H03; narrower B07/A6 | **B — retain** | Strategic arms and learning-agent mechanism design show the phenomenon nearby; the residual is a multi-participant adaptive designer whose own parameter update is the manipulation channel. |
| U20 | Make learned institutions robust to co-evolving participants, collusion, and out-of-distribution coalitions. | A6; E-F6 | **C** | Deep mechanism design, opponent shaping, repeated auctions, collusion studies, and multi-timescale MARL occupy the ingredients; the proposal is still a broad robustness bundle. |
| U21 | Choose human–AI task assignments partly for information value because trust controls allocation and allocation controls what competence evidence becomes observable. | A10; B08; E-F9 | **B — retain** | Dynamic trust, delegation, calibration, and rejectors are active in 2026, but the self-confirming endogenous-observability loop is not directly solved by the closest work. |
| U22 | Allocate scarce human oversight to uncertain agents. | E-F9; C-H2 | **D as broad claim** | One-Human-N-Agents, BRA-Audit, AgentAuditor, and scarce-audit theory directly study budgeted selection. |
| U23 | Define cumulative fairness for a changing roster while preventing strategic leave/re-entry or identity reset from erasing fairness debt. | B10; A8 | **B — retain** | Repeated allocation, attrition, endogenous entry, and long-term fairness are occupied; cheap pseudonym resets across overlapping team histories remain a narrow mechanism question. |
| U24 | Transfer reputation across model upgrades/forks and resist whitewashing/Sybil identities. | B11; H10/H11; E-F4; A8 | **C/D** | 2026 identity-grounding, AgentReputation, ERC-8004 evidence, Sybil experiments, and hardware identity drafts make generic agent reputation/continuity crowded. |
| U25 | Maintain a distributed joint chance constraint using delayed/lost/strategic risk reports. | B12; A11 | **C** | Distributed chance-constrained task allocation, risk allocation, unreliable communication planning, and decentralized optimization are old and active. Strategic reporting is a mechanism-design variant, but the proposed bundle currently lacks a distinct theorem. |
| U26 | Negotiate simultaneous coalitions when offers endogenously create/destroy outside options. | B14; H05 | **D/C** | Dynamic coalitional bargaining with externalities and endogenous outside options dates at least to 2004–2006; 2026 LLM bargaining does not revive novelty. |
| U27 | Retract a claim and repair all lossy summarized/combined descendants without replay. | B15 | **C/D** | Distributed TMS/DATMS propagate belief retractions through dependencies; ReTree (August 2026) repairs downstream summaries/branches. Lossy certificates may be useful engineering, not a clean gap. |
| U28 | Track task-aware differential-privacy loss across adaptive many-to-many interactions and colluding recipient coalitions. | B16 | **C** | Interactive/concurrent composition is mature, cooperative multi-agent planning has DP guarantees, and the September 2025 multi-agent compositional-leak paper directly studies side information and cross-agent accumulation. |
| U29 | Establish approximate common belief through strategic relays that may delay, censor, or alter messages. | H08 | **C** | Strategic communication via intermediaries, network cheap talk, verifiable network communication, Byzantine agreement, and the two-generals/common-knowledge literature already occupy most of the formal core. |
| U30 | Make memory write/summarize/delete/disclose choices endogenous strategic actions in repeated cooperation. | H12 | **C** | Bounded-memory games, selective disclosure, strategic forgetting, and 2026 selective shared memory cover the components. An LLM instantiation is unlikely to clear novelty. |
| U31 | Incentivize high-quality contributions to a shared agent memory commons. | H13; C-H3b | **C** | Public-goods incentives, governed memory, collaborative memory selection, origin-bound authority, and institutional-design framing are already present. Only a sharply formal IC mechanism could revive it. |
| U32 | Sustain peer sanctions when blame is unreliable. | C-H3a | **C/D** | Imperfect-monitoring repeated games, noisy social norms, indirect reciprocity, MARL reputation, and LLM peer punishment occupy the mechanism. |
| U33 | Predict population-level coordination collapse from local traces and trigger minimal interventions. | H14; A9 | **C** | Early-warning/tipping-point and phase-transition literatures are extensive; absent a specific non-identifiability or intervention result this is a benchmark-transfer proposal. |
| U34 | Extend population/mean-field theory to rare strategic minorities and endogenous networks. | A9 | **C/D** | Major–minor, multi-population, graphon, and non-exchangeable mean-field games already address non-negligible rare types and structured interaction. |
| U35 | Give temporal-logic guarantees for decentralized planning with a learned/misspecified teammate model. | A11; E-F1 | **C** | Learned teammate planning, risk-constrained causal AHT, formal verification of learned communication, temporal-logic MARL, and 2026 contract shielding make this look like a combination paper. |
| U36 | Select an LLM team only when hard information/tool partitions make multiple agents necessary. | E-F7; A3/A12 | **C** | TeamBench enforces role separation; heterogeneous routers/team designers and matched-compute studies address selection. Necessity proofs would be valuable but are not yet a distinct algorithmic gap. |
| U37 | Build another general multi-agent LLM collaboration benchmark. | A evaluation map; C common kills | **D** | MultiAgentBench, LLM-Coordination, SILO-BENCH, TeamBench, and Collaboration Gap cover broad, exact, role-separated, and open-world variants. |
| U38 | Evaluate ZSC across independent implementations rather than only random seeds. | H15 | **D** | *Is Inter-Seed Cross-Play Enough?* (August 2026) introduces exactly cross-implementation cross-play. |
| U39 | Make plans selectively legible to differently aligned audiences. | H16 | **C** | Legibility, opacity, privacy-preserving planning, strategic disclosure, and audience-dependent explanations already occupy the ingredients. |
| U40 | Defend shared multi-agent memory from poisoning and provenance attacks. | A7; C-H3b | **D as broad claim** | MemClaw, ArgusFleet, memory poisoning, origin-bound authority, governed memory, and institutional memory governance directly target this. |
| U41 | Automatically assign dynamic roles/models/workflows to heterogeneous LLM agents. | A12; E-F7; C common kills | **D** | AnyMAC, LLM-as-Scheduler, dynamic role assignment, Hetero-Designer, and RouterHGC make this crowded systems work. |
| U42 | Use reputation or norm formation to prevent cooperation collapse in LLM societies. | A safety/social clusters; C-H3a | **D** | RepuNet and *Social Learning and Collective Norm Formation* are AAMAS 2026 papers with these claims; AAMAS 2025 LR2 and sequential public-goods work add algorithmic baselines. |

## September 2026 preemption audit

The cut-off was treated literally, not as “through 2025.” Four September records materially change triage:

| September 2026 work | Candidate(s) killed or narrowed | Why it matters |
|---|---|---|
| [Bara, *Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence* (arXiv:2609.01873, 1 Sep 2026)](https://arxiv.org/abs/2609.01873) | U12; narrows U13 | Formalizes conditional evidential redundancy, proves report-only impossibility, separates ancestry from text similarity, models correlated extraction error, and implements calibrated aggregation. |
| [Starbuck et al., *Implicit semantic control manifolds for learning-enabled multi-UAV coordination* (Autonomous Robots, 1 Sep 2026)](https://doi.org/10.1007/s10514-026-10265-4) | narrows U08/U35/U39 | Connects imperfect embodied semantic signals to executable, dynamically feasible coordination; “ground language in multi-agent control” is no longer a gap. |
| [Wang et al., *DGSDC: Dynamic Graph Learning for Sparse and Directed Communication* (Knowledge-Based Systems, 5 Sep 2026)](https://doi.org/10.1016/j.knosys.2026.116484) | U14; narrows U13 | Directly learns sparse directed communication graphs and prunes links using estimated influence. U13 survives only because strategic agents can game allocation, not because sparse communication is absent. |
| [Fu et al., *Predictive auction–game coordination for multi-agent pursuit under intermittent communication* (Robotics and Autonomous Systems, Sep 2026)](https://doi.org/10.1016/j.robot.2026.105538) | U14/U25 | Combines auctions and dynamic games under intermittent communication. Generic “auction communication/task allocation under outages” is preempted. |

The August cross-implementation ZSC paper is also too close to the cut-off to ignore: [Wolski et al., arXiv:2608.03644](https://arxiv.org/abs/2608.03644) directly kills U38.

## Ten surviving residuals after the kill test

### S1 / U01 — Exact contingent-policy realization regret for black-box language agents

**Exact gap.** Given a small Dec-POMDP with an exact optimal contingent joint policy, measure and reduce the regret caused when separate black-box language agents must realize only their local policy components from private action–observation histories, without global-state leakage or centralized action choice.

**Strongest invalidating paper.** Witwicki and Durfee's [*Commitment-Driven Distributed Joint Policy Search* (AAMAS 2007)](https://doi.org/10.1145/1329125.1329216) already represents commitments as local-policy constraints and searches commitment space; a generic “solver-guided commitment” claim is dead. [Asmar and Kochenderfer, AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/40171) is the dangerous recent neighbor because suggested joint actions let Dec-POMDP agents approach centralized performance.

**Residual difference.** Neither paper studies a policy-class/compiler mismatch in which the solved finite contingent policy is an artifact interpreted at execution time by black-box language policies. The outcome must be a new *history-conditioned realization-regret* measure and information-preserving intervention, not just prompting agents with a policy tree.

**Recent-work check.** LLM collaboration has already been formulated as a Dec-POMDP in [MAGRPO (2025)](https://neurips.cc/virtual/2025/128017); optimal-coordination questions appear in [LLM-Coordination (NAACL 2025)](https://aclanthology.org/2025.findings-naacl.448/); [ACPO (June 2026)](https://arxiv.org/abs/2606.30072) implements joint-policy gradients with sequential action commitments. No searched 2025–8 Sep 2026 paper directly uses an exact contingent policy as an execution-fidelity oracle for decentralized language agents.

**Verdict:** **B.** Medium-low novelty confidence. The likely rejection is “toy benchmark plus policy serialization.” A theorem or impossibility about lossy policy compilation, plus nontrivial failure phenomena, is needed.

### S2 / U03 — Interventional attribution of the source of multi-agent non-stationarity

**Exact gap.** From local histories plus a limited budget of safe interventions, distinguish environment drift, a peer learning independently, and a peer adapting *because of the ego agent*, then choose tracking, robust control, or shaping accordingly.

**Strongest invalidating paper.** [*Integrating causal-context-aware teammate modeling with risk-constrained online planning for meta reinforcement learning in Ad Hoc teamwork* (Knowledge-Based Systems, 2026)](https://www.sciencedirect.com/science/article/pii/S0950705125022786) uses a temporal causal graph to separate contextual confounders from intrinsic teammate strategy and couples it to CVaR planning. This removes any broad claim that causal disentangling of teammate versus context is missing.

**Residual difference.** The residual is specifically an *interventional equivalence/identifiability* question among three generative causes, including ego-caused adaptation. Predictively accurate causal context representations need not identify whether the teammate would have changed under a counterfactual ego policy.

**Recent-work check.** [LeMOL](https://arxiv.org/abs/2006.03923), [MBOM](https://arxiv.org/abs/2108.01843), [SOM (May 2026)](https://arxiv.org/abs/2605.07301), and [ShapeLLM](https://arxiv.org/abs/2510.08255) respectively model changing opponents, jointly model environment/opponent, learn structured opponent models, and shape peer learning. I found no direct three-source identifiability theorem or safe intervention policy by the cut-off.

**Verdict:** **B.** Medium novelty confidence, down from H's initial “high” because the 2026 causal-context AHT paper is close. The project is credible only if observationally matched generators and an impossibility/sufficient-intervention result are central.

### S3 / U04 — Dual-control ad-hoc teamwork with a learning teammate

**Exact gap.** Choose actions that both achieve the task and diagnose an unfamiliar teammate when those actions update the teammate's policy, so probing changes the object being inferred.

**Strongest invalidating paper.** [Kim et al., *Learning to Continually Learn with the Bayesian Principle* / Meta-MAPG (ICML 2021)](https://proceedings.mlr.press/v139/kim21g.html) differentiates through co-player learning, while [*Learning to Coordinate With Different Teammates via Team Probing* (TNNLS 2025)](https://ieeexplore.ieee.org/document/10988880) explicitly selects probes. Together they nearly span the proposal.

**Residual difference.** Team probing treats the latent coordination pattern as sufficiently stable within the diagnostic phase; opponent-aware meta-gradients generally presume access to or a learned model of a response update. The residual combines a belief over an independently designed partner's *learning rule* with the causal value and behavioral effect of probes in a cooperative task.

**Recent-work check.** [Fast teammate adaptation after sudden policy change](https://arxiv.org/abs/2305.05911), [N-Agent AHT](https://arxiv.org/abs/2404.10740), [ROTATE (2025)](https://arxiv.org/abs/2505.23686), and [ICRL4AHT (May 2026)](https://arxiv.org/abs/2605.24423) cover changing partners, open populations, adversarial teammate generation, and in-context adaptation. The 2026 causal-context AHT paper above also increases collision risk. None of these, in the searched records, makes teammate learning-rule uncertainty part of a dual-control state.

**Verdict:** **B.** Medium novelty confidence. This will be killed if the method is only “add an opponent model to team probing”; a formal belief–influence trade-off and partner-policy displacement metric are necessary.

### S4 / U07 — Decentralized translation between two co-drifting emergent protocols

**Exact gap.** Maintain task coordination when two independently trained encoders/decoders both update asynchronously online, without a parallel corpus, fixed reference community, shared natural language, or centralized gradient.

**Strongest invalidating paper.** Cope and McBurney's [*Learning Translations: Emergent Communication Pretraining for Cooperative Language Acquisition* (IJCAI 2024)](https://www.ijcai.org/proceedings/2024/0005) explicitly learns translation into a target community. [*Unsupervised Translation of Emergent Communication* (AAAI 2025)](https://ojs.aaai.org/index.php/AAAI/article/view/34489) is the closest method-level invalidator.

**Residual difference.** Those translation settings provide offline community interactions or protocols that are stationary enough to align. The residual asks for decentralized tracking when both semantic maps change because of task interaction and translation error, creating coupled feedback and possible oscillation.

**Recent-work check.** [LangGround (TMLR, Feb 2026)](https://openreview.net/pdf?id=LGsed0QQVq) anchors emergent messages to human language and explicitly discusses stability/adaptability; [SIGN](https://arxiv.org/abs/2510.21855) steers convention formation with schemas; [memetic-drift scaling (March 2026)](https://arxiv.org/abs/2603.24676) and [LLM naming-game dynamics (August 2026)](https://arxiv.org/abs/2608.02178) analyze population drift. I found no direct no-anchor co-drift tracking algorithm or drift-rate bound.

**Verdict:** **B.** Medium-high relative confidence, but only for the co-drift/stability formulation. A standard non-stationary domain-adaptation method evaluated on messages would be incremental.

### S5 / U05 — Payment-free repeated allocation with private evolving capability and coalition-only feedback

**Exact gap.** Allocate complementary/interdependent tasks when agents privately know capabilities that evolve with learning, fatigue, or workload, can misreport or strategically withhold effort, and the allocator observes coalition success rather than individual contribution, with no monetary transfers.

**Strongest invalidating paper.** [Porter et al., *Mechanism Design with Execution Uncertainty*](https://arxiv.org/abs/1301.0595) makes execution capability private and designs truthful allocation mechanisms. [Incentive-Compatible Distributed Robotic Service Allocation (2024)](https://arxiv.org/abs/2403.10733) is a recent robotics collision.

**Residual difference.** Existing mechanism results generally use transfers, fixed/private execution types, or verifiable individual outcomes. Cooperative MRTA learns changing capabilities but does not handle strategic reports/effort; coupled-reward allocation makes individual skill statistically confounded but assumes cooperation. The residual is the simultaneous exploration, attribution, and incentive problem under joint outcomes and no transfers.

**Recent-work check.** [Adaptive task allocation with unknown/evolving capabilities](https://arxiv.org/abs/2003.03344), [CASH (CoRL 2025)](https://proceedings.mlr.press/v305/fu25a.html), [uncertainty-aware MRTA with coupled rewards (Sep 2025)](https://arxiv.org/abs/2509.22469), and [capability-decrease replanning](https://arxiv.org/abs/2412.10087) occupy the cooperative side. [Multi-agent contract design](https://arxiv.org/abs/2301.13654) occupies hidden action with payments. I found no exact payment-free, drifting-type, coalition-feedback mechanism.

**Verdict:** **B.** Medium confidence and high theorem risk. Approximate truthfulness may be impossible without authentication, repeated interaction, or observable audits; a clean impossibility plus minimal escape assumptions could be stronger than a heuristic allocator.

### S6 / U13 — Manipulation-resistant allocation of scarce communication

**Exact gap.** Allocate limited speaking slots in a partially observable mixed-motive game when senders can manipulate both bids and the learned marginal-value estimator, message value is delayed and depends on receiver/rival continuation policies, and transfers may be unavailable.

**Strongest invalidating paper.** [DALA / *Cost-Effective Communication in Multi-Agent Systems* (AAAI 2026)](https://doi.org/10.1609/aaai.v40i35.40182) already centrally auctions scarce language-agent turns by predicted value density. Classic [interdependent-value bandwidth allocation](https://insights.sei.cmu.edu/library/handling-interdependent-values-in-an-auction-mechanism-for-bandwidth-allocation-in-tactical-data-networks/) handles strategic value reports with an outcome-contingent mechanism.

**Residual difference.** DALA treats the value estimator as an optimization signal rather than an object strategically influenced by current and future behavior. Classic mechanisms presume transfers and more verifiable outcomes. The residual is endogenous delayed value plus estimator gaming in a learned sequential policy.

**Recent-work check.** [Why and Whom to Communicate? (AAMAS 2026)](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/TAYO7266.pdf), [DGSDC (5 Sep 2026)](https://doi.org/10.1016/j.knosys.2026.116484), and [predictive auction–game coordination under intermittent communication (Sep 2026)](https://doi.org/10.1016/j.robot.2026.105538) close the nonstrategic scheduling/topology gap. I found no paper that tests deviation gain against a learned communication-value auction without transfers.

**Verdict:** **B.** Medium confidence. The novelty evaporates if the paper merely adversarially trains DALA. It needs a solution concept (incentive regret / airtime-capture gain), an impossibility or bound, and strategic best-response baselines.

### S7 / U15 — Identifiability certificates for offline ad-hoc teamwork

**Exact gap.** Given fixed logs from several team compositions, determine whether behavior with a new teammate is identified by the data; otherwise abstain or request the minimum safe online interaction needed to disambiguate relevant teammate-conditioned joint actions.

**Strongest invalidating paper.** [TAGET (ICML 2025)](https://proceedings.mlr.press/v267/zhang25h.html) learns goal-conditioned ad-hoc teamwork from offline data. [CODA (2026)](https://openreview.net/pdf?id=XfAR4v6iZM) directly diagnoses a structural offline coordination failure: current policies respond to teammates sampled from a fixed behavior distribution rather than current teammate policies.

**Residual difference.** These methods improve offline coordination but do not provide a teammate-shift-specific identifiability test, ambiguity set, or selective guarantee. Ordinary single-policy support is insufficient because a new partner changes joint reachability and the ego policy's relevant counterfactuals.

**Recent-work check.** [ComaDICE (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/hash/477d1531c260f9605bbf9d14d00952d4-Abstract-Conference.html) controls stationary-distribution shift; [Seldonian AHT (RLC 2025)](https://rlj.cs.umass.edu/2025/papers/Paper223.html) supplies user-specified safety constraints; [DiTAC (2026)](https://journals.sagepub.com/doi/10.3233/FAIA251257) learns teamwork abstractions; [Minimum Coverage Sets](https://arxiv.org/abs/2308.09595) studies training-population coverage. I found no direct coverage certificate whose unit is an unseen teammate policy coupled with selective probing.

**Verdict:** **B.** Medium-high relative confidence. A tabular impossibility/sufficient condition plus a scalable calibrated proxy is the minimum credible paper; an empirical uncertainty score alone is not.

### S8 / U19 — Strategic teaching of an adaptive mechanism designer

**Exact gap.** Design an online tax/reward/allocation mechanism when participants can sacrifice current utility to causally steer the designer's future learned parameters, including coordinated or heterogeneous-rate teaching.

**Strongest invalidating paper.** [Braverman et al., *Multi-armed Bandit Problems with Strategic Arms* (COLT 2019)](https://proceedings.mlr.press/v99/braverman19b.html) already models strategic agents manipulating a learning principal's selection rule. The broader mechanism-design-for-learning-agents program explicitly warns that a learning party can be “taught” by strategic counterparts. [Adaptive Mechanism Design using Multi-Agent Revealed Preferences (2024)](https://arxiv.org/abs/2404.15391) iteratively probes equilibrium responses.

**Residual difference.** Strategic-arm work concerns selection/revenue in a particular principal–agent bandit. Adaptive mechanism work generally models agents as equilibrium responders to each enacted mechanism. The residual treats the *designer update* as a long-horizon influence channel jointly manipulated by multiple participants and asks for designer-shaping regret or influence-robust updates.

**Recent-work check.** [Learning Dynamic Mechanisms in Unknown Environments (JMLR 2024)](https://www.jmlr.org/papers/v25/23-0159.html), [Adaptive Incentive Design with Learning Agents](https://arxiv.org/abs/2405.16716), [Learning a Game by Paying the Agents (2025)](https://arxiv.org/abs/2503.01976), [Microeconomic Foundations of Multi-Agent Learning (2026)](https://arxiv.org/abs/2601.03451), and [ShapeLLM](https://arxiv.org/abs/2510.08255) occupy nearby spaces. No searched record directly defines and bounds multi-participant manipulation of a learned mechanism-update rule.

**Verdict:** **B.** Medium confidence. This is particularly vulnerable to an older economics equivalent under “strategic experimentation,” “ratchet effect,” or “dynamic mechanism with forward-looking agents.” A final domain-expert audit is mandatory.

### S9 / U21 — Breaking self-confirming trust–allocation loops in human–AI teams

**Exact gap.** Choose safe “calibration assignments” for information value when current trust determines who gets tasks and those assignments determine which context-specific human/AI competence evidence becomes observable.

**Strongest invalidating paper.** [*Calibrating AI Trust in Complementary Human-AI Collaboration*](https://openreview.net/pdf?id=6KcewDz76A) models trust evolution and learns calibration policies. [Nalisnick et al., *Human-AI Teaming Through the Lens of Calibration* (June 2026)](https://arxiv.org/abs/2606.10906) gives a strong theoretical warning: delegation moves the calibration burden to a rejector that may be unable to observe the human's information.

**Residual difference.** Existing delegation/calibration work usually evaluates beliefs against evidence generated independently of the allocation rule or treats competence estimates as available features. Here, under-allocation prevents a distrusted but capable member from producing evidence, so greedy assignment can make false beliefs self-confirming; the intervention is task allocation, not an explanation/confidence display.

**Recent-work check.** [AI, Take the Wheel (May 2026)](https://arxiv.org/abs/2605.28255) jointly studies delegation and adoption, [Belief Updating and Delegation in Multi-Task Human–AI Interaction (CHI 2026)](https://doi.org/10.1145/3772318.3790775) studies performance-cue updating, and [Trust Repair in Human-Agent Teams](https://link.springer.com/article/10.1007/s10458-021-09515-9) supplies repair baselines. I found no direct active allocation algorithm whose objective explicitly values competence-identifying evidence and tests escape from matched self-confirming histories.

**Verdict:** **B.** Medium confidence. Simulation-only evidence will likely fail review; a preregistered human study is needed, and the scientific outcome must separate improved information from mere forced exposure.

### S10 / U23 — Cumulative fairness under strategic churn and cheap identity resets

**Exact gap.** Define and implement intertemporal fairness for overlapping, changing team populations when agents can time entry/exit or reset pseudonyms to erase disadvantage/debt, while preserving welfare and learnability.

**Strongest invalidating paper.** [Freund and Hssaine, *Fair Incentives for Repeated Engagement* (2025)](https://doi.org/10.1177/10591478241273874) models fair reward policies with agent attrition and an endogenous-entry extension. [Fairness in Repeated Matching (AAAI 2026)](https://doi.org/10.1609/aaai.v40i20.38760) studies optimal and anytime maximin sequences.

**Residual difference.** Repeated fair allocation largely fixes identity/population, while attrition models do not let an agent strategically reset its identity and re-enter an overlapping relational history. The residual needs a fairness axiom that says what debt persists under authenticated departure versus cheap pseudonym changes and a mechanism robust to reset deviations.

**Recent-work check.** [Repeated Fair Allocation of Indivisible Items (AAAI 2024)](https://doi.org/10.1609/aaai.v38i9.28837), [Fairness in Repeated House Allocation (AAMAS 2024)](https://aamas.csc.liv.ac.uk/Proceedings/aamas2024/pdfs/p2390.pdf), [Achieving Fairness in Multi-Agent MDP (ICLR 2024)](https://proceedings.iclr.cc/paper_files/paper/2024/hash/473cb5596e2b84648753ce26484d79c8-Abstract-Conference.html), and [Open-ended Coordination Using Modular Open Policies (JAAMAS 2025)](https://link.springer.com/article/10.1007/s10458-025-09723-7) cover repeated fairness, fair MARL, and open teams separately. Agent-identity work in 2026 makes authenticated continuity itself contested. I found no exact cheap-reset manipulation result for cumulative multi-agent fairness.

**Verdict:** **B.** Medium confidence. The main risk is normative arbitrariness: without explicit identity/authentication assumptions, “fairness debt should persist” is not a theorem-ready statement.

## Aggressive rejection notes for the strongest casualties

These rejections should remain visible in the parent synthesis; otherwise several will reappear under new labels.

1. **Correlated evidence / epistemic dependence (U12) — D.** [Epistemic Sybil Resistance](https://arxiv.org/abs/2609.01873) is not merely adjacent: it uses conditional mutual information to define redundant reports, proves a report-only impossibility, models shared-root/correlated errors, and evaluates ancestry-aware calibration. A residual would have to move to *decentralized action selection under privately held ancestry*, which is materially different from the submitted candidate and still needs verification.
2. **Matched-compute causal benefit of interaction (U17) — C/D.** [Capable language models can outgrow the benefits of collaboration](https://www.nature.com/articles/s42256-026-01268-y) already uses matched compute across 260 configurations and coordination covariates; [equal-thinking-token comparison](https://arxiv.org/abs/2604.02460) isolates the budget confound. A mediation paper is possible but not a gap claim.
3. **Strategic adaptive verification (U11/U22) — D broadly.** [Dai et al., scarce audits (COLT 2025)](https://proceedings.mlr.press/v291/dai25a.html), [One Human, N Agents](https://arxiv.org/abs/2607.28317), and the papers catalogued in the initial audit cover strategic reports, adaptive audit budgets, correlation/miscalibration, and runtime selection. A narrow evolving-sender signaling equilibrium might be B, but it duplicates the risks of U13 and lacks a clearer execution path.
4. **Convention capture (U09) — C.** Committed-minority naming games already derive tipping fractions; [the high-dimensional committed-minority analysis](https://www.cs.rpi.edu/~szymansk/papers/pre-93-05-16.pdf) and [rogue/stubborn-node naming-game analysis](https://cs.gmu.edu/~fangyiyu/papers/Naming_Game.pdf) directly study minority manipulation. [Byzantine Cheap Talk](https://arxiv.org/abs/2606.07790), [memetic drift](https://arxiv.org/abs/2603.24676), and [August 2026 LLM Naming Games](https://arxiv.org/abs/2608.02178) close recent empirical space. “Keep accuracy high while changing semantics” is interesting but not yet a full scientific distinction.
5. **Dynamic coalition bargaining with endogenous outside options (U26) — D/C.** [Bloch and Gomes, *Contracting with Externalities and Outside Options*](https://doi.org/10.1016/j.jet.2004.11.004) already models dynamic coalition formation and repeated interaction where actions affect outside options. [Coalition formation with dynamically changing externalities](https://doi.org/10.1016/j.engappai.2020.103577) and [dynamic multi-threaded negotiation with outside options](https://publications.ri.cmu.edu/bilateral-negotiation-decisions-with-uncertain-dynamic-outside-options-3) are close MAS work. LLM negotiators do not restore novelty.
6. **Semantic descendant repair (U27) — C/D.** [Bridgeland and Huhns, *Distributed Truth Maintenance* (AAAI 1990)](https://cdn.aaai.org/AAAI/1990/AAAI90-011.pdf) and [Malheiro, Jennings, and Oliveira, DATMS (ECAI 1994)](https://eprints.soton.ac.uk/252143/) already maintain distributed justifications and belief revision. [ReTree (Aug 2026)](https://arxiv.org/abs/2608.10676) localizes a contradicted claim, regenerates affected summaries, and prunes descendants. The residual “without storing enough dependency evidence and without replay” may be impossible rather than novel.
7. **Coalitional privacy composition (U28) — C.** [The Sum Leaks More Than Its Parts](https://arxiv.org/abs/2509.14284) studies auxiliary knowledge and accumulated cross-agent answers, including collaborative defenses. [Interactive DP composition](https://openreview.net/forum?id=xvlaiSHgPrC) and [Differential Privacy in Cooperative Multiagent Planning](https://openreview.net/pdf?id=9u-oj0mkIa) cover formal composition/planning. A task-aware accountant is likely an application unless it proves a new adversarial-composition result.
8. **Rare strategic minorities beyond exchangeability (U34) — C/D.** [Major–minor mean-field games](https://doi.org/10.1137/120889496), [multi-population MFGs](https://arxiv.org/abs/2103.12668), and [graphon MFGs](https://arxiv.org/abs/2606.28254) directly relax homogeneous exchangeability. The candidate needs a new regime, not the statement that rare types matter.
9. **Spec-aware planning with learned teammates (U35) — C.** [Decentralized MCTS with learned teammate models](https://www.ijcai.org/proceedings/2020/12), [risk-constrained causal AHT (2026)](https://www.sciencedirect.com/science/article/pii/S0950705125022786), [formal verification of learned communication policies](https://arxiv.org/abs/2606.19632), and [contract-based compositional shielding (2026)](https://arxiv.org/abs/2606.14130) leave only a combination claim.
10. **Shared memory commons/governance (U30/U31/U40) — C/D.** [Governed Shared Memory](https://arxiv.org/abs/2606.24535), [Origin-Bound Authority](https://arxiv.org/abs/2606.24322), [MemMA](https://arxiv.org/abs/2603.18718), and [Shared Selective Persistent Memory](https://arxiv.org/abs/2607.09493) already cover governance, source authority, verification/repair, and selective shared persistence. Older strategic forgetting and bounded-memory games remove the theory novelty.
11. **Generic agent reputation/Sybil resilience (U24/U42) — D/C.** [Dissociative Identity](https://arxiv.org/abs/2605.30169), [AgentReputation](https://arxiv.org/abs/2605.00073), [ERC-8004 empirical study](https://arxiv.org/abs/2606.26028), [RepuNet (AAMAS 2026)](https://www.ifaamas.org/Proceedings/aamas2026/pdfs/UEHN4980.pdf), and [LR2 (AAMAS 2025)](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1745.pdf) make broad trust/reputation claims untenable.
12. **Cross-implementation ZSC (U38) — D.** [Wolski et al.](https://arxiv.org/abs/2608.03644) do exactly the cross-implementation cross-play experiment. This candidate should not appear in the final top set.
13. **Another role/team/router architecture (U36/U41) — D.** [Hetero-Designer (ACL 2026)](https://aclanthology.org/2026.acl-long.1272/), [RouterHGC (Findings ACL 2026)](https://aclanthology.org/2026.findings-acl.1589/), [AnyMAC (EMNLP 2025)](https://aclanthology.org/2025.emnlp-main.584/), [LLM-as-Scheduler (ACL 2026)](https://aclanthology.org/2026.acl-long.581/), and [TeamBench](https://teambench.github.io/) occupy the engineering design space.
14. **Another broad benchmark (U37) — D.** [MultiAgentBench](https://aclanthology.org/2025.acl-long.421/), [LLM-Coordination](https://aclanthology.org/2025.findings-naacl.448/), [SILO-BENCH](https://aclanthology.org/2026.acl-long.1354/), [TeamBench](https://teambench.github.io/), and [Collaboration Gap](https://arxiv.org/abs/2511.02687) make a benchmark-only pitch exceptionally weak.

## Survivor comparison and recommendation to the parent

| Survivor | Verdict | Residual novelty confidence | Main novelty threat | Best likely paper core |
|---|---:|---:|---|---|
| S1 exact-policy realization regret | B | Medium-low | Old commitment search; toy/interface contribution | New execution-regret object plus compiler/impossibility |
| S2 causal source attribution | B | Medium | 2026 causal-context teammate modeling | Identifiability theorem plus safe interventions |
| S3 dual-control learning teammate | B | Medium | Team probing + opponent shaping nearly span it | Belief over update rules; influence-aware planning |
| S4 co-drifting protocol translation | B | Medium-high | Translation and drift studied separately | Tracking/stability bound and phase transition |
| S5 private evolving capability allocation | B | Medium | Contract/execution-uncertainty theory | Impossibility/approximate IC without transfers |
| S6 strategic scarce bandwidth | B | Medium | DALA plus classic bandwidth mechanisms | Incentive regret and estimator-gaming defense |
| S7 offline AHT identifiability | B | Medium-high | Offline coordination/coverage theory may subsume it | Coverage theorem, calibrated certificate, minimal probe |
| S8 teaching adaptive designer | B | Medium | Strategic arms; ratchet/strategic experimentation economics | Designer-shaping regret and robust update |
| S9 self-confirming human–AI allocation | B | Medium | Dynamic trust/delegation papers | Safe information-valued allocation + human study |
| S10 fairness under churn/reset | B | Medium | Repeated fairness and attrition theory | Axioms/impossibility plus reset-resistant algorithm |

My conservative novelty ordering is **S7 ≈ S4 > S2 ≈ S3 > S5 ≈ S6 ≈ S8 ≈ S9 ≈ S10 > S1**. This is not a publishability ordering: S1 is experimentally crisp but scientifically easiest to dismiss; S8 may be deep but requires a specialist economics audit; S9 needs human subjects. The cleanest two residuals for the final team to investigate further are:

1. **Offline AHT identifiability with selective probing (S7):** a clear theorem/algorithm/experiment path and a genuinely joint-coverage issue.
2. **Co-drifting decentralized protocol translation (S4):** a precise interaction effect with potential stability and tracking-regret results.

## Search accounting and limitations

- The five supplied reports collectively contained **260 paper/technical-record ledger entries before cross-report deduplication** (A 75, B 58, E 33, H 54, initial C 40); E separately listed 29 software/dataset/model artifacts. The 260 entries are not 260 globally unique papers because the reports intentionally overlap.
- In this second wave I re-queried exact terminology, semantic variants, older fields (truth maintenance, strategic experimentation, repeated fair allocation, naming-game zealots, major–minor MFGs, dynamic coalition bargaining), adjacent fields (HCI calibration, distributed systems, differential privacy), and 2025–8 September 2026 work. This report cites the primary records most relevant to each decision rather than pretending every search result was read in full.
- 2026 arXiv/preprint priority remains volatile. “No exact paper found” means only **no direct match in the searched literature by the cut-off**.
- Two survivors need additional specialist audits before any novelty claim: S8 against the economics of ratchet effects/strategic experimentation, and S10 against dynamic population-monotonic fair division and false-name-proof mechanism design.
- No survivor supports “first” or “nobody has studied” language.

## Final status labels

- **Verified gap:** none at this stage.
- **Plausible gap requiring further literature verification:** S1–S10, with the calibrated confidence table above.
- **Rejected / already addressed or too incremental:** U02, U06, U08–U12, U14, U16–U18, U20, U22, U24–U42 except retained IDs.
