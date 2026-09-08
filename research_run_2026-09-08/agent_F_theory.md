# Agent F — Theory and Formalization Audit

Date: 2026-09-08

## Executive verdict

I audited the candidate families in Agents A, B, C, E, and H and retained ten narrow formulations for a theory pass. This is a formalization audit, not a novelty certification. The strongest theoretical opportunities are **causal attribution of multi-agent non-stationarity**, **offline ad-hoc-teamwork identifiability**, **tracking co-drifting communication protocols**, **open-population fairness under resettable identity**, and **dynamic coalition capability learning with aggregate feedback**. Each has a natural lower-bound or identifiability question that determines whether an algorithm can work at all.

Several attractive candidates lose most of their novelty once the older theory is restored. Strategic teaching of an adaptive designer is directly pressured by recent non-myopic principal–agent learning. Strategic relays collide with Byzantine agreement and communication-network games. Distributed retraction collides with truth-maintenance systems. Coalition-only hidden effort collides with combinatorial agency. Correlated evidence aggregation is now directly occupied by a September 2026 paper. These are not automatic rejections, but the residual claim must be narrower than the headline.

No theorem stated below should be presented as established. “Theorem opportunity” means a concrete statement that appears both useful and attackable; it still needs proof and a dedicated backward citation audit.

## Common notation

For sequential candidates, use a partially observable stochastic game

\[
G=(N,S,(A_i),(O_i),P,(r_i),\gamma),
\]

with local history \(h^i_t=(o^i_{0:t},a^i_{0:t-1},m^i_{0:t})\). Agent \(i\)'s policy is \(\pi_i(a_i,m_i\mid h^i_t)\). Any latent teammate type, learning rule, reputation state, or communication lexicon must be made part of an augmented latent state rather than casually called “non-stationarity.” This distinction is essential: once all other agents and their update rules are fixed and observable, several proposals collapse to a single-agent POMDP. A surviving formulation must preserve strategic response, decentralized information, or relational welfare in the solution concept.

---

## T1. Causal source attribution for multi-agent non-stationarity

**Source candidates:** H02 and B01.

### Minimal formal model

Use a two-player partially observable Markov game with physical state \(x_t\), exogenous regime \(e_t\), opponent parameter \(\theta_t\), ego action \(a_t\), opponent action \(b_t\), and observation \(o_t\). Compare three structural model classes:

1. **Exogenous drift:** \(e_{t+1}=F_e(e_t,\xi_t)\), while \(\theta\) is fixed.
2. **Independent co-learning:** \(\theta_{t+1}=F_0(\theta_t,h^{-i}_t,\eta_t)\), with no causal edge from ego's policy update or intervention variable to \(\theta_{t+1}\).
3. **Responsive/strategic adaptation:** \(\theta_{t+1}=F_1(\theta_t,h^{-i}_t,a_t,\pi^i_t,\eta_t)\).

The ego observes only \(h^i_t\). It may spend an intervention budget \(B\) on safe policy perturbations \(I_t\in\mathcal I\). Its objective is

\[
\min_\pi \; \mathbb E\left[\sum_{t=1}^T r^*_t-r_t + \lambda c(I_t)\right],
\]

where \(r^*_t\) is an oracle response that knows the source class. Report both dynamic regret and causal-source error; predictive likelihood alone is not the target.

### Theorem and estimand opportunities

- **Observational non-identifiability:** construct one exogenous-drift game and one responsive-opponent game inducing the same distribution over \(h^i_{1:T}\) under a fixed ego policy, but different distributions under \(do(I_t)\). Therefore no passive predictor can uniformly select the correct response class.
- **Minimal separating interventions:** characterize an intervention set \(\mathcal I\) whose interventional kernels have full column rank over the candidate source models. Below this rank condition, attribution is impossible; above it, posterior error can decay at a rate controlled by the minimum interventional KL separation.
- **Regret with sparse interventions:** for a finite source class and bounded total variation, aim for a bound of the form \(\tilde O(\sqrt{T|\mathcal M|})+O(Bc)+O(T\epsilon_B)\), where \(\epsilon_B\) is residual attribution error. A lower bound should show unavoidable regret when all safe interventions are observationally equivalent.
- **New estimand:** the *source-conditioned intervention value*, \(\Delta(I)=V(do(I))-V(I\text{ treated as passive evidence})\), separates acting to learn another agent's response from simply tracking drift.

### Falsifiable hypothesis

On pairs of games matched for passive trajectory likelihood, sparse separating interventions will reduce source misclassification and dynamic regret relative to a joint world/opponent predictor; if passive prediction performs equally well after compute matching, the proposed causal decomposition adds no decision value.

### Theory fit and collision audit

Theory is **natural and central**, not decorative. The third source exists only because another decision-maker responds to ego. A single-agent non-stationary MDP can emulate the observed process, but cannot answer the counterfactual “would the process have changed under a different ego policy?” without importing a response model—precisely the missing multi-agent object.

The closest theoretical pressure is the impossibility of universal cooperation with adaptive partners, which already proves that unrestricted partner adaptation defeats learning ([Loftin & Oliehoek, ICML 2022](https://proceedings.mlr.press/v162/loftin22a.html)). Recent repeated-policy regret also formalizes counterfactual regret against adaptive opponents and proves necessary restrictions ([Liu et al., COLT 2026](https://proceedings.mlr.press/v336/liu26c.html)). Causal games already formalize interventions when agents may respond ([Mishra, Fox & Wooldridge, 2024](https://arxiv.org/abs/2406.09318)). Empirical neighbors include [Fast teammate adaptation](https://proceedings.mlr.press/v216/zhang23a.html) and [SOM](https://arxiv.org/abs/2605.07301). The residual novelty is not “opponents cause non-stationarity”; it is **identifying which causal source generated matched local histories and using that attribution to choose tracking, robust control, or shaping**.

**Assessment:** high theoretical leverage; medium-high novelty confidence after the inspected search.

---

## T2. Identifiability and selective deployment in offline ad-hoc teamwork

**Source candidate:** B09.

### Minimal formal model

Let \(\tau\in\mathcal T\) index a teammate policy or teammate-controlled transition component in a cooperative Dec-POMDP. An offline dataset

\[
D=\{(\tau_k,h_k,a^i_k,a^{-i}_k,r_k,h'_k)\}_{k=1}^n
\]

is collected under training teammate mixture \(q(\tau)\) and ego behavior policies \(\mu_i\). At deployment, \(\tau_*\) is new and may be observed only through its actions or their consequences. Define the ambiguity set \(\mathcal G(D)\) of games/teammate models statistically indistinguishable on the support of \(D\).

The key object should be a **teammate-conditional coverage coefficient**, for example

\[
C_{\rm TC}(\pi,\tau_*)=\sup_{h,a_i,a_{-i}}
\frac{d^{\pi_i,\tau_*}(h,a_i,a_{-i})}
     {d^D(h,a_i,a_{-i})},
\]

or a weaker unilateral/joint factorization when the numerator cannot be estimated directly. The deployed policy may choose \(\pi_i\), abstain, or purchase \(k\) online probes. Optimize worst-case value over \(\mathcal G(D)\) minus probe cost.

### Theorem and estimand opportunities

- **Two-world impossibility:** exhibit two Dec-POMDPs identical on \(D\) but requiring incompatible ego actions with the same unseen teammate. Any purely offline policy then has constant worst-partner suboptimality.
- **Necessary coverage:** prove that support only for the training joint policies is insufficient; coverage of strategically relevant unilateral teammate deviations or an explicit structural relation between \(\tau_*\) and training types is necessary.
- **Sufficient condition:** under finite types, realizability, and bounded \(C_{\rm TC}\), give a robust value-confidence interval and a high-probability worst-teammate bound.
- **Selective guarantee:** define the ambiguity width \(W_D(h,\tau)=\sup_{G,G'\in\mathcal G(D)}|Q_G-Q_{G'}|\). Act only when \(W_D\le\epsilon\); otherwise abstain or request the probe maximizing worst-case version-space reduction. Prove calibrated selective risk rather than pretending universal zero-shot coordination.

### Falsifiable hypothesis

A teammate-conditional ambiguity/coverage score should predict held-out teammate failure and choose useful probes better than ordinary behavior likelihood, uncertainty ensembles, or generic offline-RL density ratios. Failure to improve selective risk or worst-partner return would refute the proposed multi-agent coverage distinction.

### Theory fit and collision audit

Theory is **natural**. The ambiguity is over the other participant's policy and over joint occupancies; it is not resolved by single-agent state-action coverage. However, if teammates are merely latent environment modes that never respond and all joint actions are logged, the problem becomes offline meta-RL. The paper must demonstrate a separation between ordinary task identifiability and teammate-conditioned coordination identifiability.

Major collisions are [offline RL under single-policy concentrability](https://proceedings.mlr.press/v178/zhan22a.html), offline Markov-game unilateral coverage—including a 2026 corruption-robust result ([Nika et al., AISTATS 2026](https://proceedings.mlr.press/v300/nika26a.html))—and offline meta-RL identifiability ([Dorfman et al., 2021](https://openreview.net/forum?id=IBdEfhLveS)). AHT-specific pressure comes from [Minimum Coverage Sets](https://arxiv.org/abs/2308.09595) and [DiTAC](https://doi.org/10.3233/FAIA251257). The defensible residual is **coverage with respect to an unseen teammate-conditioned joint occupancy plus a calibrated offline-to-online abstention/probing rule**, not generic offline MARL coverage.

**Assessment:** very high theoretical leverage; medium-high novelty confidence.

---

## T3. Tracking limits for two co-drifting communication protocols

**Source candidates:** B02 and H07's non-adversarial core.

### Minimal formal model

In a repeated signaling game, sender \(i\) maps private state \(z^i_t\) to symbol \(m^i_t\) through encoder \(E^i_t\); receiver \(j\) maps the symbol and its observation to an action through decoder \(D^j_t\). Both encoder/decoder pairs update independently and online. No paired semantic labels, natural-language anchor, central gradient, or shared latent representation is available. Agents observe task payoff and local trajectories only.

Let protocol drift be

\[
V_T=\sum_{t=2}^T
\left(d(E^1_t,E^1_{t-1})+d(D^1_t,D^1_{t-1})+d(E^2_t,E^2_{t-1})+d(D^2_t,D^2_{t-1})\right),
\]

where distance is quotient by payoff-preserving symbol permutations. A translation layer \(T^{1\to2}_t\) is evaluated by dynamic semantic regret against the best time-indexed translation sequence with variation budget \(V_T\).

### Theorem and estimand opportunities

- **Permutation impossibility:** without an anchor event, asymmetric task consequence, or deliberate probe, multiple translations related by semantic permutations are observationally equivalent. Exact semantic recovery is impossible even when task return is high.
- **Drift-rate threshold:** establish a lower bound showing linear tracking regret when the joint protocol changes faster than the rate at which task feedback distinguishes translations.
- **Sufficient tracking bound:** under persistent excitation, bounded delay, and two-timescale updates, obtain dynamic regret scaling with \(V_T\), feedback noise, and symbol complexity; compare simultaneous updates with deliberately staggered translation/agent updates.
- **Stability result:** linearize coupled encoder–translator dynamics around a convention and give a spectral condition separating stable tracking from oscillation/semantic collapse.

### Falsifiable hypothesis

Timescale separation plus consequence-based probes should exhibit a measurable drift threshold below which translation error remains bounded and above which all methods collapse. If ordinary online fine-tuning or 2026 recertification baselines track equally well at matched feedback, the proposed stability theory is unnecessary.

### Theory fit and collision audit

Theory is **natural** because meaning is relational and both sides' updates alter the data-generating process. It becomes ordinary non-stationary domain adaptation if one protocol is frozen or an external semantic label is exposed.

The nearest translation papers include [CLAP / Learning Translations](https://arxiv.org/abs/2402.16247), [Unsupervised Translation of Emergent Communication](https://ojs.aaai.org/index.php/AAAI/article/view/34489), and [Emergent Translation](https://arxiv.org/abs/1710.06922). [Verifiable Semantics](https://arxiv.org/abs/2602.16424) already proves bounded disagreement for certified terms and explicitly proposes recertification/renegotiation under drift. [Talk is Cheap, Communication is Hard](https://arxiv.org/abs/2605.01750) documents dynamic grounding failures. Consequently the new object must be **decentralized simultaneous co-drift and its tracking/stability limit**, not drift detection or protocol translation separately.

**Assessment:** high theoretical leverage; medium novelty confidence.

---

## T4. Sound decentralized retraction after lossy multi-agent summarization

**Source candidate:** B15.

### Minimal formal model

Represent an agent society's beliefs as a distributed justification hypergraph \(H=(V,E,owner)\). A source claim \(x\in V\) may be transformed by agent-local, possibly lossy summary maps \(f_e\), combined with other claims, and transmitted. A derived node carries a bounded certificate \(c(v)\) rather than its full derivation. After retraction of \(x\), agents must mark every claim whose remaining support is invalid while preserving independently supported claims.

Optimize four quantities: repair soundness, repair completeness, communication cost, and replay cost. The protocol is decentralized: no node stores the global graph, agents can be offline, and local trust policies may reject a correction.

### Theorem and estimand opportunities

- **Provenance lower bound:** construct two derivation hypergraphs producing the same lossy summaries but different affected-descendant sets. Any protocol lacking enough dependency information must either leave a false descendant or retract a valid independent belief.
- **Certificate sufficiency:** for monotone derivations with bounded fan-in, show that compact source-set sketches or authenticated justification DAG fragments enable sound targeted invalidation with false-positive probability \(\delta\), and characterize certificate size versus repair precision.
- **Network lower bound:** under partial connectivity, any complete repair must communicate across every cut separating an affected owner from the retraction source; this supplies a topology-dependent minimum cost.
- **New estimand:** residual unsupported-belief mass after a retraction, weighted by downstream decision influence, is more scientific than “number of deleted memory records.”

### Falsifiable hypothesis

Bounded justification certificates should sharply reduce unsupported descendant beliefs and replay cost versus source tags, deletion-only, and full replay. If source tags plus ordinary cache invalidation achieve the same frontier, the MAS contribution is mostly systems engineering.

### Theory fit and collision audit

The theory is **natural but novelty-fragile**. Distributed ownership, disagreement, and partial reachability are genuinely multi-agent. Yet with truthful agents and reliable messages, this is distributed truth maintenance, a mature area. Classic truth-maintenance systems already store justifications and propagate retractions ([Doyle, 1979](https://doi.org/10.1016/0004-3702(79)90008-7)); distributed belief revision is old ([Dragoni & Puliti, 1994](https://doi.org/10.1109/TAI.1994.346451)). A recent multi-agent revision formalism further raises the bar ([A Study of Belief Revision Postulates in Multi-Agent Systems, 2026](https://arxiv.org/abs/2605.02249)). The defensible residual requires **non-invertible learned summaries, bounded certificates, and decentralized repair under incomplete connectivity or conflicting trust**. Without a lower bound unique to those ingredients, reject.

**Assessment:** medium-high theoretical leverage; low-medium novelty confidence.

---

## T5. Fairness debt in open populations with resettable identities

**Source candidate:** B10.

### Minimal formal model

At time \(t\), an active set \(N_t\) competes for resource \(R_t\). Each persistent principal \(p\) may instantiate one or more observable identities \(i\), enter, leave, or change roles. Let exposure \(e_{p,t}\), contribution \(c_{p,t}\), allocation \(x_{p,t}\), and historical fairness debt \(d_{p,t}\) evolve across overlapping participation intervals. The mechanism sees either authenticated principals or only resettable pseudonyms.

Candidate axioms should be explicit: newcomer protection, cumulative envy/debt boundedness, role normalization, Pareto efficiency, anonymity, and churn-proofness (no principal improves by leaving and re-entering or splitting identities).

### Theorem and estimand opportunities

- **Reset impossibility:** with free unauthenticated pseudonyms, no anonymous mechanism can simultaneously provide nontrivial newcomer guarantees, preserve cumulative obligations, and be immune to beneficial resets. This should be proved with a two-period/two-principal construction before any MARL algorithm is proposed.
- **Identity-continuity trade-off:** characterize the minimum authentication/deposit/continuity signal needed for bounded manipulation gain.
- **Authenticated positive result:** under persistent principal IDs and bounded churn, a primal–dual debt update may achieve sublinear welfare regret and bounded cumulative exposure-normalized envy.
- **Open-population estimand:** define fairness over principals and active exposure, not over instantaneous visible identities; quantify reset manipulation gain separately from ordinary envy.

### Falsifiable hypothesis

A debt-carrying rule should improve cumulative fairness without increasing reset/splitting gains under strategic churn. If results disappear when compared with dynamic max-min fairness or when measured at the principal rather than identity level, the proposal fails.

### Theory fit and collision audit

Theory is **natural**; fairness is inherently relational and roster changes alter other agents' claims. However, a central allocator with nonstrategic jobs is an online-allocation problem, not substantively MAS. Strategic identity choice and overlapping obligations must be essential.

The mature neighbors are [Dynamic Weighted Fairness with Minimal Disruptions](https://arxiv.org/abs/2001.06841), [Fair and Efficient Online Allocations](https://doi.org/10.1287/opre.2022.0332), [long-term fairness in dynamic allocation](https://arxiv.org/abs/2208.05898), and manipulation-resistant reputation/whitewashing theory ([Algorithmic Game Theory, Chapter 27](https://www.cambridge.org/core/books/algorithmic-game-theory/manipulationresistant-reputation-systems/13DBDA298DFFD00E6DA230C48267BBF1)). The residual is the incompatibility of **intertemporal fairness debt with open-agent identity resets**, not dynamic fairness alone.

**Assessment:** high theoretical leverage; medium novelty confidence.

---

## T6. Approximate common belief under strategic message relays

**Source candidate:** H08.

### Minimal formal model

Use a networked Bayesian game on graph \(G=(N,E)\). A subset observes state \(s\); relay \(j\) has private alignment type \(\alpha_j\) and may forward, delay, alter, or censor a message. Coordination action at deadline \(T\) pays only if an appropriate coalition acts consistently. Agents maintain nested beliefs; the operational target is \(p\)-common belief of event \(E_s\), not exact common knowledge over a lossy asynchronous channel.

Protocol actions include signed forwarding, acknowledgements, redundant paths, and randomized challenge queries. Optimize welfare minus communication and challenge cost under equilibrium relay behavior.

### Theorem and estimand opportunities

- **Signed-origin insufficiency:** signatures authenticate sent content but cannot reveal omitted content; construct equilibria with identical received transcripts and different censored states.
- **Connectivity condition:** under at most \(f\) strategically misaligned relays and a restricted utility model, derive a necessary/sufficient vertex-connectivity or disjoint-path condition for bounded common-belief error.
- **Challenge value:** characterize when random challenges make censorship unprofitable and bound bandwidth versus belief error.
- **Impossibility boundary:** exact common knowledge remains impossible with unbounded delay; the legitimate result is deadline-indexed approximate common belief and action safety.

### Falsifiable hypothesis

Redundant paths plus challenges should improve coordination specifically when relay incentives are uncertain, beyond signed flooding and Byzantine-robust baselines at equal bandwidth. If the same guarantees follow directly from a standard Byzantine protocol under the chosen assumptions, the game-theoretic layer adds nothing.

### Theory fit and collision audit

Theory is **natural but heavily occupied**. Three or more agents and nested beliefs are essential; a sender–receiver reduction removes strategic intermediation. But classic Byzantine agreement, the coordinated-attack problem, epistemic logic, and communication-network mechanism design already own much of the theorem space. Recent economic work directly studies strategic transmission through intermediaries ([Strategic Disclosure in Networks, 2026](https://doi.org/10.3982/TE6446)); [Incentives and the Structure of Communication](https://doi.org/10.1016/j.jet.2018.03.009) characterizes implementable outcomes on restricted networks; [Network-Induced Strategic Communication](https://arxiv.org/abs/2607.16036) is a 2026 neighbor. Retain only if partial alignment plus long-horizon stateful coordination produces a result not inherited from rational Byzantine consensus.

**Assessment:** high theorem potential; low-medium novelty confidence because of mature-theory collision.

---

## T7. Dynamic coalition capability learning with hidden effort and full-bandit feedback

**Source candidates:** H04 and B06.

### Minimal formal model

There are \(n\) agents with private capability states \(\theta_{i,t}\) evolving as controlled Markov processes (learning, fatigue, depletion). In each round a principal selects coalition \(C_t\), agents report \(\hat\theta_{i,t}\), privately choose effort \(e_{i,t}\), and the principal observes only coalition outcome

\[
y_t\sim P(\cdot\mid C_t,\theta_{C_t,t},e_{C_t,t}).
\]

The task technology is complementary rather than additive. Transfers may be allowed in one version and prohibited in another. The objective must combine allocation regret, incentive regret (profitable report/effort deviation), and diagnostic burden.

### Theorem and estimand opportunities

- **Coalition identifiability:** for a parametric technology, characterize rank/separability conditions on the selected-coalition design matrix under which individual capability trajectories are identifiable from coalition-only outcomes.
- **No-transfer impossibility:** with hidden effort, private type, and only aggregate outcome, show that truthful reports and first-best effort cannot generally both be implemented without audits, repeated-game discipline, or transfers.
- **Dynamic lower bound:** derive regret depending on capability variation \(V_T\), minimal diagnostic coalition eigenvalue, and complementarity degree; prove that always choosing currently best coalitions leaves some pivotal capabilities unidentifiable.
- **Restricted positive result:** randomized diagnostic coalitions plus delayed outcome-contingent transfers may yield sublinear regret and \(\epsilon_T\)-incentive compatibility under slow Markov drift.

### Falsifiable hypothesis

Diagnostic coalition selection should improve capability calibration and welfare while limiting strategic withholding relative to UCB, Shapley credit, and truthful/cooperative MRTA. If an ordinary full-bandit combinatorial UCB baseline matches performance once drift is modeled, the incentive layer is not doing scientific work.

### Theory fit and collision audit

Theory is **natural**, but the broad formulation is already classical combinatorial agency: multiple hidden efforts jointly determine an observable outcome ([Babaioff, Feldman & Nisan](https://arxiv.org/abs/1401.3837)). Multi-agent contract design also directly studies a principal observing stochastic outcomes but not actions ([Castiglioni et al., 2023](https://arxiv.org/abs/2301.13654)). Full-bandit combinatorial feedback is mature ([Rejwan & Mansour, 2020](https://proceedings.mlr.press/v117/rejwan20a.html)), as are principal–agent bandits ([Scheid et al., ICML 2024](https://proceedings.mlr.press/v235/scheid24a.html)). The residual must jointly require **action-dependent capability evolution, complementary coalitions, and strategic effort/reporting**. Scope it to one binary-skill technology; otherwise the theorem program is too broad.

**Assessment:** high theoretical leverage; medium novelty confidence, with severe scope risk.

---

## T8. Joint safety certification from distributed, delayed, and strategic risk reports

**Source candidate:** B12.

### Minimal formal model

Use a constrained POSG with joint hazard indicator \(g(s_t,a_t)\) and chance constraint

\[
\Pr_\pi\!\left(\exists t\le H:g(s_t,a_t)=1\right)\le\delta.
\]

No agent observes a sufficient risk state. Each sends a set-valued risk summary \(M_{i,t}\) with timestamp and confidence level; up to \(f\) agents may misreport and benign messages may be delayed or lost. A decentralized shield maps local histories and received reports to admissible local actions.

### Theorem and estimand opportunities

- **Local-certification impossibility:** give two joint states with identical local certificates but different feasibility of the same joint action; no product of purely local shields can enforce the coupled constraint.
- **Compositional sufficient condition:** if authenticated confidence sets have simultaneous coverage and communication delay is bounded, use robust reachable sets or risk-budget composition to guarantee the joint chance constraint, with explicit conservatism.
- **Byzantine threshold:** characterize when \(f\)-robust aggregation plus graph connectivity permits a nontrivial safe action; below the threshold only a fail-safe action can be certified.
- **Safety–communication lower bound:** relate minimum information rate to the gap between decentralized and centralized safe value.

### Falsifiable hypothesis

Age-aware set-valued reports should preserve the target violation probability under bounded delay/loss while giving higher return than always-safe fallback. Any empirical violation above the promised confidence envelope falsifies the guarantee; excessive fallback makes the result vacuous.

### Theory fit and collision audit

Theory is **natural** when the constraint is genuinely coupled. It reduces to ordinary robust control if a central shield sees all reports or if strategic misreporting is represented as undifferentiated bounded noise. Nearby work includes [shield decomposition for partially observable multi-agent environments](https://rlj.cs.umass.edu/2024/papers/Paper254.html), [Robust Constrained Markov Games, UAI 2026](https://proceedings.mlr.press/v337/chang26a.html), and communication-aware multi-agent POMDP work ([Garraffa et al., 2026](https://doi.org/10.1109/LRA.2026.3703246)). The novelty burden is a non-vacuous compositional guarantee when sufficient statistics are distributed and reports can be strategic, not another GNN safety aggregator.

**Assessment:** medium-high theoretical leverage; medium novelty confidence; assumptions may make the positive theorem too narrow.

---

## T9. Reputation redemption as strategic diagnostic allocation

**Source candidate:** H10.

### Minimal formal model

Model a population partner-selection game as a restless bandit with strategic arms. Agent \(j\)'s latent type \(q_{j,t}\) can genuinely improve at unobserved change points, while a strategic type can cooperate selectively on diagnostic tasks and defect on valuable tasks. Other agents allocate a scarce number of low-stakes diagnostic interactions and update public or local reputations. Opportunity cost arises because each diagnostic slot displaces a trusted partner.

The objective is social welfare minus diagnostic cost, subject to bounded time-to-redemption for truly improved agents and bounded exploitation gain for intermittent defectors.

### Theorem and estimand opportunities

- **Redemption–exploitation lower bound:** construct improved and strategic-recidivist types that are observationally identical for \(k\) diagnostic interactions; any rule granting redemption by time \(k\) suffers a corresponding attacker gain.
- **Impossibility without change evidence:** no policy can guarantee both finite uniform redemption time and vanishing false-redemption probability when type changes and strategic mimicry are unrestricted.
- **Positive result:** under bounded switch count, diagnostic-task informativeness, and a cost of strategic cooperation, a change-point posterior plus randomized tests may achieve sublinear welfare regret and explicit attacker-gain bounds.
- **New estimands:** lockout regret for genuinely improved agents, false-redemption loss, and strategic diagnostic return on investment.

### Falsifiable hypothesis

Randomized change-sensitive diagnostics should reduce lockout regret without increasing periodic-defector payoff relative to reputation decay, reset, and optimistic bandit exploration.

### Theory fit and collision audit

Theory is **natural but economically crowded**. Selection by other agents creates the evidence and strategic incentive; without partner choice it is a standard non-stationary bandit. Yet [The Reputation Trap](https://doi.org/10.3982/ECTA17891) already formalizes persistent bad reputation and underinvestment in rehabilitation, and [(Bad) Reputation in Relational Contracting](https://doi.org/10.3982/TE4803) explicitly describes a strategic-arm bandit with experimentation. Whitewashing is also mature. The surviving novelty is diagnostic allocation **after real policy change in a population of reciprocal selectors**, not the existence of reputational lockout.

**Assessment:** medium theoretical leverage; low-medium novelty confidence.

---

## T10. Active evidence acquisition under interaction-created dependence

**Source candidate:** B04.

### Minimal formal model

Represent root observations \(Z_1,\ldots,Z_k\) and agent reports \(R_1,\ldots,R_n\) in a causal evidence DAG. Edges record copying, shared retrieval, or exposure to prior messages. A coordinator has budget \(B\) to commission new evidence, hide/show selected reports, or verify roots. It chooses a final action \(a\) under posterior loss. The relevant value of a report is conditional mutual information \(I(Y;R_i\mid R_{-i},\text{ancestry})\), not vote count.

### Theorem and estimand opportunities

- **Effective-evidence bound:** under known ancestry and conditionally independent root noise, bound decision error by the number/quality of independent roots rather than reports.
- **Non-identifiability without provenance:** two evidence DAGs—one copied, one independent—can induce identical surface similarity yet require different aggregation weights. Textual diversity cannot identify epistemic independence.
- **Adaptive acquisition:** under submodularity conditions, greedy conditional-information acquisition gets a \((1-1/e)\) approximation; identify how strategic report selection breaks submodularity.

### Falsifiable hypothesis

Ancestry-aware active verification should outperform majority, confidence, and surface-diversity routing when many reports share a root. If it does not improve utility per verification under controlled ancestry, the causal graph adds no value.

### Theory fit and collision audit

Theory is coherent, but the broad gap is now **mostly occupied**. [Epistemic Sybil Resistance](https://arxiv.org/abs/2609.01873) directly argues that multiplying agents does not multiply evidence, separates similarity from ancestry, and supplies theory and experiments. [Controlling Uncertainty and Hallucination Risk in Multi-Agent Fact Verification](https://proceedings.mlr.press/v337/kostka26a.html) addresses correlated consensus and calibrated risk. Classical social-learning and information-cascade theory is extensive. Only the **sequential allocation of new independent evidence under a budget and interaction-created dependence** remains plausibly distinct. This may still reduce to Bayesian experimental design unless decentralized incentives or message exposure causally changes future reports.

**Assessment:** medium theoretical leverage; low novelty confidence. Do not place in the final top five without a sharper residual.

---

## Hard collisions and hidden single-agent reductions

### Strategic teaching of an adaptive mechanism designer (H03/B07)

Do not claim that participants manipulating a learning designer is missing. [Learning to Lead: Incentivizing Strategic Agents in the Dark](https://arxiv.org/abs/2506.08438) already studies a non-myopic strategic agent that misreports to manipulate the principal's learning and gives a near-optimal regret guarantee. [Strategic Teaching and Learning in Games](https://doi.org/10.1257/mic.20170139) proves broad incentives to teach learning opponents, and [Regret Minimization with Adaptive Opponents](https://proceedings.mlr.press/v336/liu26c.html) adds a 2026 counterfactual regret framework. A residual might involve several participants creating cross-agent externalities while jointly shaping a population-level institution, but “designer-shaping regret” itself is not safely novel.

### Solver-guided Dec-POMDP policy realization by language agents (Agent C H1)

The proposed policy-realization regret is measurable, but its theory risks being forced. Once an exact solver gives each black-box agent its complete local contingent policy, the remaining mismatch is often interface compliance or bounded-memory policy execution. If agents have no strategic objectives and the compiler centrally encodes all contingencies, this can reduce to testing two local transducers rather than solving a new multi-agent decision problem. Old commitment-driven joint-policy search and common joint-history execution already supply the coordination theory. Retain only if private-history ambiguity causes a provable joint realization loss that cannot be diagnosed from each local policy independently.

### Shared memory as a commons (Agent C H3b)

Public-goods formalization is available, but the framing is already explicit in 2026 institutional-design work. If agents share a common reward and contribution costs are artificial bookkeeping, free-riding is not credible. A theory paper would need heterogeneous utilities, costly verification, endogenous consumption, and a mechanism result not inherited from peer prediction or public-good provision. This is lower leverage than T4's precise retraction lower bound.

## Top five by genuine theoretical leverage

This ranking weights whether theory determines the scientific question, not mathematical elegance or ease of proving something.

| Rank | Candidate | Why theory is decisive | Main novelty threat | Theory verdict |
|---:|---|---|---|---|
| 1 | **T1 causal source attribution** | Passive observational equivalence versus interventional separability is the core phenomenon; an impossibility theorem directly motivates the algorithm | Causal games and adaptive-opponent regret may already imply part of the boundary | **Natural, highest leverage** |
| 2 | **T2 offline AHT identifiability** | Without teammate-conditional coverage, no empirical method can promise coordination; selective deployment follows from ambiguity width | Offline Markov-game unilateral coverage and offline meta-RL identifiability | **Natural, very high leverage** |
| 3 | **T3 co-drifting protocol tracking** | Symmetry, excitation, drift rate, and coupled-update stability determine whether translation is possible | 2026 semantic certification/recertification and dynamic grounding | **Natural, high leverage** |
| 4 | **T5 open-population fairness debt** | An axiomatic impossibility can establish which identity continuity assumption is indispensable before designing a learner | Dynamic fair allocation and whitewashing theory are mature separately | **Natural, high leverage** |
| 5 | **T7 dynamic coalition capability learning** | Coalition design rank, hidden effort, and variation budget yield concrete identifiability and regret limits | Combinatorial agency, contract design, and full-bandit CMAB already cover most components | **Natural but scope-sensitive** |

Close sixth: **T8 distributed joint safety** has strong theorem potential, but a positive guarantee may depend on delay, fault, and calibration assumptions so restrictive that the scientific claim becomes a robust-control special case. **T6 strategic relays** is mathematically rich but has the most dangerous mature-theory collision. **T4 retraction repair** needs a new lossy-summary lower bound to escape old truth-maintenance systems.

## Recommendation to the synthesis agent

1. Put T1 and T2 through the final novelty kill test first. Both can begin with a two-world impossibility construction, so a failed proof attempt will reveal a weak premise quickly.
2. Treat T3 as the strongest communication candidate, but explicitly compare against Verifiable Semantics and dynamic-grounding repair.
3. Keep T5 only if the population principal/identity distinction is formal and reset manipulation is tested; otherwise it is ordinary dynamic allocation.
4. Narrow T7 to a binary complementary-skill technology and choose either transfers or no transfers. Do not attempt evolving types, hidden effort, coalition formation, payments, fatigue, and deep MARL all at once.
5. Downgrade H03, H08, B04, B15, and H10 unless a second novelty audit finds a theorem unique to their residual formulation.

The strongest general design principle is: **prove the information or incentive obstruction before proposing an architecture**. For these candidates, the lower bound is not an optional theory section; it is what prevents a reviewer from reducing the contribution to a standard POMDP, bandit, distributed cache, or prompt-level agent wrapper.
