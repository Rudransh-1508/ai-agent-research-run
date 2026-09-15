# Agent Research Program --- Master Context & Next Steps

**Last consolidated:** 13 September 2026\
**Current research target:** Multi-Agent Systems / Agentic AI, with
**MASO** as the primary immediate venue and **SE4AgenticAI** as the
secondary venue if the work gets a concrete software-engineering
grounding.

------------------------------------------------------------------------

# 1. Where we are

We ran a deliberately adversarial research-discovery process rather than
brainstorming one idea and trying to justify it.

The process searched broadly across:

-   Multi-agent systems and agentic AI
-   Organizational learning, adaptation, resilience, and specialization
-   Agent replacement/evolution and ad-hoc teamwork
-   Software maintenance, transactions, rollback, semantic consistency
-   Diagnosis, causality, counterfactual replay, repair
-   Incentive design, monitoring, delegation, reputation, accountability
-   Information theory, rate-distortion, random-access coding, strategic
    source coding
-   Distributed systems, fault tolerance, checkpointing, provenance
-   Mechanism design, dominant implementation, false-name manipulation,
    coalition monitoring
-   Control, operations research, evaluation, adaptive testing

The discovery funnel produced **40 candidate records**:

-   **C00--C37: killed in their registered scopes**
-   **C38: unresolved / not recommended**
-   **C39: current scoped survivor**

This does **not** mean 40 ideas received equally deep literature audits.
The process intentionally killed many ideas using small counterexamples,
reductions, and known stronger baselines before spending expensive
effort.

The current evidence contains **81 literature records**, with a focused
**16-paper primary-section audit** for C39. These are not 81 fully read
papers.

The most important conclusion:

> **We do not yet have a submission-ready paper. We have one formal
> research lead that earned another focused research week.**

C39's current novelty confidence was assessed at about **60/100**,
significance about **63/100**, with **MASO fit \~72/100** and
**SE4AgenticAI fit \~60/100**. These are qualitative research judgments,
not measurements.

------------------------------------------------------------------------

# 2. What we are currently working on

## C39 --- Reconstruction-Incentive Frontiers for Self-Contained Agent Audit Records

### Core question

> **How much extra reconstruction distortion must a self-contained
> persistent record incur to preserve bounded incentives for each
> agent's effort, regardless of teammate actions, when that same record
> is the sole input to deferred settlement?**

The central phenomenon is a tension between two uses of the same
compressed record:

1.  **Reconstruction:** the record must let the organization
    recover/reconstruct the team's execution state after the fact.
2.  **Incentives:** the record must retain enough information about each
    individual's unilateral effort that a later bounded payment can
    reward effort regardless of what teammates did.

The important point is not simply that compression loses information.

The proposed contribution is a **quantitative frontier**:

> Under a finite memory budget, what is the minimum reconstruction error
> required to preserve a specified unilateral effort-incentive margin?

The record is **self-contained**: all information available to the
reconstruction/payment decoders must be counted in the retained state.
Free shared randomness, free auxiliary seeds, or an independent audit
channel cannot secretly be treated as free.

The settlement is **deferred**: the payment is computed after
compression, from the retained record.

------------------------------------------------------------------------

# 3. Why the older idea changed

The earlier candidate was:

## "Delayed-Query Contracts for Lossy Agent Memory: Minimum Evidence for Incentive-Compatible Recovery"

Its original question was:

> When an agent can strategically compress its execution history before
> learning which historical decision will later need verification or
> repair, how much independently retained evidence is minimally needed
> to make both targeted recovery and honest resource expenditure
> enforceable?

The proposed formal model had:

-   execution history `H`
-   agent-controlled retained state `Z = C_sigma(H)` with budget `B`
-   independently captured evidence `A(H)` with budget `M`
-   delayed invalidation query `f ∈ F`
-   repair policy `rho(Z,A,f)` with compute budget `R`
-   bounded contract `tau` with reward/continuation range `P`
-   strategic effort/reporting/erasure policy `sigma`

and sought a minimum trusted-memory quantity:

`M*(B,R,P,F,epsilon,delta)`

subject to incentive compatibility and recovery guarantees.

That was interesting, but it was too broad and vulnerable to
decomposition into known ideas from:

-   strategic forgetting
-   memory/recovery systems
-   provenance
-   endogenous monitoring
-   contracting
-   causal logging
-   rollback/checkpointing
-   strategic source coding

The research process therefore narrowed the problem to a cleaner
finite-record theorem where the **same compressed record must serve both
reconstruction and deferred incentive payments**.

The important lesson:

> **Do not revive the old generic "memory + incentives + recovery"
> framing. The scientific object now is the constrained finite-record
> frontier.**

------------------------------------------------------------------------

# 4. The current formal object

Let:

-   `S ∈ {0,1}^n` be the vector of agent actions/effort outcomes.
-   `K` be the number of retained record labels/states.
-   The encoder observes `S` and stochastically produces a retained
    signal `Y ∈ [K]`.
-   A reconstruction decoder maps `Y` back to an estimate of `S`.
-   Each agent has a bounded payment decoder based only on `Y`.
-   Each payment is bounded, typically in `[0,1]`.
-   `gamma` is the required minimum unilateral effort/payment margin.

The incentive condition is deliberately strong:

> For every agent and every configuration of teammates, changing that
> agent from low effort to high effort must increase expected payment by
> at least `gamma`.

This is an **all-teammate-profile / robust unilateral margin**, not
merely a Nash-equilibrium condition.

Define:

`D*(K, gamma)`

as the minimum expected reconstruction error achievable by:

-   a stochastic encoder,
-   a reconstruction rule,
-   bounded per-agent reward decoders,

subject to the required incentive margin.

All decoder-side state counts toward `K`.

This is important because otherwise a supposed memory tradeoff can be
defeated by hiding a seed, identity, receipt, or auxiliary random
variable outside the counted record.

------------------------------------------------------------------------

# 5. What has actually been established

## T1 --- Exact arbitrary-contract binary-record frontier

For odd `n`, uniform source profiles, `K = 2`, arbitrary bounded payment
functions, and arbitrary reconstruction:

Define

`M_n = 2^(-n) * sum_{k=0}^n C(n,k) * min(k, n-k)`.

Then the established frontier is:

`D*(2, gamma) = M_n + n*gamma*((n-1)/2 - M_n)`

for:

`0 <= gamma <= 1/n`.

Above `gamma = 1/n`, positive-margin implementation is impossible in
this setting.

The proof uses:

-   normalization of nonconstant bounded payment pairs to endpoint
    orientations,
-   input flips to align incentive directions,
-   the fact that every hypercube edge must increase the relevant signal
    probability by at least `gamma`,
-   symmetry/permutation averaging,
-   Bayes-optimal Hamming reconstruction,
-   a characterization of the optimal weight-level signal probabilities.

The achiever is essentially a mixture of known classical constructions
such as majority and random-bit sampling.

**Important:** the coding construction itself is not claimed novel. The
proposed novelty is the **necessity/optimality frontier under the
incentive-margin constraint**.

------------------------------------------------------------------------

## T2 --- Perfect-rate incompatibility

For Hamming perfect-code parameters:

`n = 2^r - 1`

and

`K = 2^n / (n+1)`,

the ordinary unconstrained minimum reconstruction distortion is:

`D0 = n/(n+1)`.

At equality, a radius-one perfect covering is forced.

Every codeword and all of its unilateral neighbors collapse to the same
retained signal.

Therefore:

> A payment function depending only on that retained signal cannot
> provide a positive unilateral incentive margin along those edges.

A broader derived lower bound is:

`D - D0 >= min(2^(-n), 3*gamma/(n+1))`.

This is deliberately weak but applies to arbitrary repair codebooks and
reward decoders.

This result is **not** a claimed sharp multi-bit frontier.

------------------------------------------------------------------------

## T3 --- Sharp Hamming-family frontier for decoded-bit rewards

For a fixed binary Hamming repair code and decoded-bit reward functions:

`D*(gamma) = (1 + gamma) D0`

over the established margin range:

`0 <= gamma <= (n-1)/(n+3)`.

Here `D0` is the probability that the source lies outside the code.

The intuition:

-   a non-codeword normally decodes to its nearest center;
-   preserving positive unilateral sensitivity forces probability mass
    toward another codeword that differs in the relevant bit;
-   this increases reconstruction distance from `1` to at least
    `1 + gamma`;
-   a symmetric distance-three construction attains the bound.

This statement permits arbitrary source priors for the fixed-code
theorem.

Again:

> This does **not** prove the sharp arbitrary-payment optimum for `K=16`
> or other general multi-bit settings.

------------------------------------------------------------------------

# 6. Strongest small-state evidence

The research program did not just eyeball candidate constructions.

### C39 experiments completed

-   E08: incentive-distortion LP / rational checks
-   E09: global binary-contract MILP attack
-   E10: alternate codebooks and Nash-only baselines
-   E11: shared-randomness and early-settlement boundary attacks
-   E12: general one-bit binary-record extension

Key evidence:

-   10 fixed-family LP settings matched the formulas.
-   12 E12 full-cube LP checks matched the analytic expression.
-   `n=3` exhaustive comparison covered **28 two-label codebooks × 8
    payment orientations** across relevant settings.
-   This produced **672 LP solves** in the n=3 global comparison.
-   `n=7` tested **128 feasible alternative codebooks**; none improved
    the established Hamming construction in the tested settings.
-   Rational construction checks extended through `n=15` for the fixed
    decoded-bit family.
-   The one-bit extension was tested on `n=3,5,7,9`.
-   The MILP attack at `n=7` timed out, so it is **not** a proof of
    global optimality.

The timed-out MILP produced:

-   feasible incumbent: `1.001953125`
-   solver lower bound: `0.936796875`
-   known feasible construction: `0.9625`

Therefore:

> **The MILP found no counterexample, but it did not certify the
> optimum.**

Never describe it as a passed global optimality test.

------------------------------------------------------------------------

# 7. Boundary cases we deliberately tested

Two obvious escape routes were explicitly tested.

## Escape route A --- free shared randomness

If the decoder can receive an extra public random coset index for free,
the information bottleneck changes.

For example, the recorded experiments show:

-   `n=3`: positive margin can coexist with `D=0.75` at margin `0.5`.
-   `n=7`: positive margin can coexist with `D=0.875` at margin `0.75`.

But once the additional decoder-side state is counted, the total
retained state becomes larger.

This is not a hidden failure of C39.

It defines the boundary:

> The tradeoff matters only when the record is genuinely self-contained
> and all decoder-side information is counted.

## Escape route B --- immediate payment

If payment is settled before the record is compressed, the incentive
problem can disappear from the reconstruction channel.

Immediate payment can give margin `1` without changing later
reconstruction.

Again:

> This is an explicit design boundary, not something to hide.

The real research question therefore includes:

**When is deferred settlement genuinely necessary in an agentic
workflow?**

------------------------------------------------------------------------

# 8. What C39 is NOT claiming

Do not make these claims:

-   "Compression always destroys incentives."
-   "Agent memory is fundamentally incompatible with incentives."
-   "No one has studied memory and incentives."
-   "No existing coding theorem is related."
-   "This is a new coding algorithm."
-   "We have solved arbitrary multi-bit contracts."
-   "All n=7 contracts are globally optimized."
-   "LLM agents empirically behave according to this model."
-   "This has been validated in production."
-   "This is already a submission-ready MASO/SE4AgenticAI paper."
-   "The exact problem cannot be reduced to a single-agent model in
    every formulation."

The defensible claim is narrower:

> We have an apparently unaddressed finite-alphabet
> reconstruction-versus-unilateral-incentive frontier, supported by
> exact small-state analysis and an explicit separation from the closest
> inspected results, but it still requires a stronger prior-art and
> theory audit.

------------------------------------------------------------------------

# 9. Why the 38 other candidates were killed

The candidate funnel is important because it tells us what NOT to
rediscover.

## Main kill mechanisms

### Existing stronger objects

Many proposals reduced to established mechanisms:

-   invariant confluence
-   interface automata
-   cross-play / Other-Play
-   commitment lifecycles
-   codiagnosability
-   graph process number
-   false-name manipulation
-   provenance
-   standard rollback recovery
-   semantic transactions

### Simple stronger baselines

Several ideas disappeared when compared with:

-   convention translation
-   corrected attribution
-   explicit repair-state bonuses
-   evidence deduplication
-   ordinary AND monitoring
-   shared random sampling
-   full-state contracts

### Mathematical cancellation

C27 was a particularly important warning.

The proposed joint causal-responsibility improvement looked promising,
but after exact modeling the joint interval reduced to ordinary
Fréchet/cancellation structure.

Across:

-   1,536 pair comparisons
-   3,072 LP solves

all apparent gains disappeared against the correct baseline.

Maximum numerical discrepancy was only about `1.33e-15`.

Lesson:

> Always derive the exact baseline before trusting an apparent
> multi-agent causal improvement.

### C37 joint memory + incentives

C37 initially showed a modular memory/incentive gap.

But the gap was matched by an elementary repair-label/sign-bonus
baseline in every tested configuration.

So the observed phenomenon was real, but the proposed contribution was
trivial.

### C38 audit alphabet

C38 asks:

> What is the minimum alphabet of a retained public audit signal that
> implements costly effort as strict dominant action for n agents under
> bounded payments?

It remains unresolved, but is **not recommended right now**.

Its strongest pilot found a randomized parity construction that beat
deterministic monitors.

However, that construction is classical random-access coding.

No novelty pass has been earned.

Do not treat C38 as a second winner.

------------------------------------------------------------------------

# 10. Closest literature threats to C39

The most important conceptual neighbors include:

### Endogenous monitoring / mechanism design

**Optimal Incentive Contract with Endogenous Monitoring Technology**

Already studies:

-   finite performance partitions,
-   multi-agent incentive constraints,
-   endogenous information/monitoring,
-   expected wages.

Potential threat:

> Is C39 merely a special case/corollary of constrained monitoring?

This must be attacked directly.

### Monitoring Teams

Team monitoring literature already distinguishes:

-   Nash implementation,
-   unique implementation,
-   monitoring partitions,
-   team structures,
-   random monitoring.

Potential threat:

> Does team monitoring already imply the relevant margin frontier?

### Strategic source coding

Strategic coding literature studies senders/receivers with misaligned
objectives.

Potential threat:

> Is the C39 optimization simply a strategic source-coding theorem in
> different notation?

Need an explicit comparison of assumptions and objective functions.

### Random-access coding

Random-access coding supplies several of the constructions and coding
bounds.

Potential threat:

> Is the reconstruction/incentive frontier just an ordinary coding bound
> with a renamed constraint?

The current defense is that C39 constrains **adjacent-profile payment
increments**, not merely reconstruction distortion or individual bit
recovery.

But this must be proved, not asserted.

### Classical coding / Hamming codes

The actual encoders and some geometric facts are classical.

Do not sell classical majority, parity, Hamming codes, or randomized
sampling as novel.

------------------------------------------------------------------------

# 11. The most dangerous unresolved theoretical question

## Direct theorem collision

The single biggest remaining novelty risk:

> An older theorem in constrained coding, mechanism design, strategic
> source coding, or implementation may already imply T1/T2.

The next research pass must independently derive the relationship to
those literatures.

If a previous theorem directly supplies the same frontier under
equivalent assumptions:

**KILL the novelty claim.**

Do not rescue it with terminology.

------------------------------------------------------------------------

# 12. Second major unresolved question: K \> 2

We currently have a strong one-bit result.

We do **not** yet have a sharp arbitrary-payment multi-bit result.

In particular:

-   `K=4`
-   `K=8`
-   `K=16`

remain important.

The previous MILP attack timed out.

Therefore the next implementation should use:

-   exact finite-state formulations,
-   global optimization where possible,
-   symmetry reduction,
-   integer/rational certificates,
-   branch-and-bound or other certified search,
-   saved solver certificates,
-   carefully separated upper and lower bounds.

Do not simply run more random restarts and call the best result optimal.

A feasible construction proves an upper bound.

A certified lower bound is needed for optimality.

------------------------------------------------------------------------

# 13. Third major unresolved question: realistic loss functions

The current cleanest mathematics uses:

-   binary action profiles,
-   uniform source profiles for the main T1 result,
-   Hamming reconstruction loss.

This is useful for theorem discovery, but may be criticized as
artificial.

Next test:

-   nonuniform source priors,
-   heterogeneous agent effort costs,
-   heterogeneous payment caps,
-   asymmetric reconstruction penalties,
-   false-positive versus false-negative repair costs,
-   weighted agent/state importance,
-   noisy records.

Goal:

> Determine whether the frontier is structurally robust or whether it
> only appears under symmetric toy assumptions.

If the effect disappears immediately under realistic weighted losses:

**downgrade the significance claim.**

Do not hide that result.

------------------------------------------------------------------------

# 14. Fourth major unresolved question: real agent/software setting

This is the biggest gap for SE4AgenticAI and also a relevance risk for
MASO.

We need a minimal, natural workflow where:

1.  multiple agents perform costly work;
2.  their execution state is compressed/checkpointed;
3.  later, some failure/invalidation occurs;
4.  settlement or accountability happens after the compression point;
5.  the retained record is genuinely constrained;
6.  immediate payment is not an obvious free solution;
7.  shared randomness or a free external audit channel is not an obvious
    free solution.

Possible shape:

### Agent task-completion / checkpoint example

Agent A performs expensive validation.

Agent B plans based on A's output.

Agent C executes.

The system periodically compacts the trace/checkpoint.

Later:

-   a tool result is invalidated,
-   an external artifact changes,
-   a downstream state must be reconstructed,
-   and the system must determine whether A actually performed the
    expensive validation.

The record needs to serve both:

-   recovery/reconstruction,
-   deferred accountability/payment.

This should be tiny and measurable.

Do not build a giant agent framework.

The point is to demonstrate that the abstract model corresponds to an
actual engineering constraint.

------------------------------------------------------------------------

# 15. Exact next research plan

## Phase 1 --- PRIOR-ART KILL GATE

### Goal

Try as hard as possible to prove C39 is already known.

Search/read:

-   constrained source coding
-   strategic source coding
-   Bayesian persuasion with action-dependent costs
-   mechanism design with finite signals
-   endogenous monitoring
-   monitoring teams
-   informativeness / Blackwell orders
-   dominant implementation
-   implementation with restricted signals
-   rate-distortion under incentive constraints
-   communication complexity with incentives
-   information design with costly actions
-   coding with side information
-   team moral hazard
-   delegated decision making
-   contractible information
-   finite alphabet implementation

For every candidate theorem, write:

1.  exact model,
2.  exact assumptions,
3.  objective,
4.  constraint,
5.  whether it maps to C39,
6.  whether the mapping is exact,
7.  whether it yields T1,
8.  whether it yields T2,
9.  whether it yields the same lower bound,
10. what remains if it does not.

### Kill criterion

If an existing theorem gives the same frontier under equivalent
assumptions:

**C39 novelty is killed.**

------------------------------------------------------------------------

# 16. Phase 2 --- General K frontier

Target:

-   K=4
-   K=8
-   K=16

Start with `n=3` and `n=7`.

Need:

-   globally valid lower bounds,
-   explicit feasible constructions,
-   symmetry reductions,
-   exhaustive small cases where possible,
-   certified optimization.

Do not rely on:

-   local restarts,
-   random codebook sampling,
-   one timed-out MILP,
-   numerical coincidence.

### Kill criterion

If a better same-budget contract produces lower distortion than the
claimed sharp frontier:

kill that specific frontier.

The one-bit theorem may still survive.

Keep theorem scopes separate.

------------------------------------------------------------------------

# 17. Phase 3 --- weighted/nonuniform robustness

Run:

-   priors around `.1/.5/.9`,
-   random nonuniform distributions,
-   heterogeneous effort costs,
-   heterogeneous payment caps,
-   weighted Hamming loss,
-   asymmetric false-positive/false-negative costs.

Questions:

-   Does positive incentive margin still force extra distortion?
-   Does the qualitative frontier survive?
-   Can the same proof technique generalize?
-   Does a new quantity replace Hamming distance?
-   Are there meaningful regimes where the effect becomes stronger?

### Kill criterion

If all interesting effects vanish outside the symmetric toy model:

do not claim broad organizational significance.

------------------------------------------------------------------------

# 18. Phase 4 --- software-shaped toy system

Build the smallest possible executable environment.

Example:

### Agents

-   Validator
-   Planner
-   Executor

### Work

Validator can perform:

-   cheap superficial check, or
-   expensive real validation.

The expensive action costs compute/time.

### State

The system checkpoints a compressed record.

### Later event

A tool result becomes invalid.

The system must reconstruct which decisions depended on the invalidated
result.

### Settlement

A bounded reward is calculated later from the retained checkpoint.

### Measurements

Measure:

-   checkpoint size,
-   reconstruction error,
-   unilateral incentive margin,
-   compute cost,
-   settlement timing,
-   effect of adding an external seed,
-   effect of immediate settlement,
-   effect of a separate audit channel.

This should first use **tabular strategic agents**, not LLMs.

------------------------------------------------------------------------

# 19. Phase 5 --- strategic-agent validation

Once the mathematical model survives:

Use small tabular agents with explicit utilities.

Compare:

-   all-profile robust incentive constraints,
-   Nash-only constraints,
-   average-case incentives,
-   heterogeneous costs,
-   exogenous teammate failures.

Do not confuse:

-   Nash equilibrium,
-   dominant strategy,
-   iterated dominance,
-   all-profile unilateral margin.

The organizational claim depends heavily on this distinction.

------------------------------------------------------------------------

# 20. Phase 6 --- optional LLM integration

Only if the previous gates survive.

Use a tiny LLM-agent workflow with:

-   tool-verified milestones,
-   actual checkpoint compression,
-   measurable storage limits,
-   deferred evaluation,
-   explicit compute costs.

Possible models/agents can be simple.

The point is **not** to show that LLMs are irrational.

The point is to demonstrate:

> the abstract information constraint can appear in a realistic agent
> runtime.

Never infer rational incentive effects merely from prompting an LLM to
"care about reward."

------------------------------------------------------------------------

# 21. Phase 7 --- paper decision

Only after the previous gates:

### MASO paper

Best framing:

**A theorem about organizational memory under deferred accountability.**

Lead with:

1.  joint execution-state reconstruction,
2.  unilateral effort sensitivity,
3.  self-contained record assumption,
4.  finite-alphabet frontier,
5.  impossibility/bound,
6.  constructive family,
7.  software-shaped case,
8.  explicit boundaries.

### SE4AgenticAI paper

Need a stronger engineering story:

-   checkpointing,
-   trace compaction,
-   agent execution records,
-   recovery,
-   deferred accountability,
-   storage/latency constraints.

Do not submit the pure theorem to SE4AgenticAI without a convincing
software workflow.

------------------------------------------------------------------------

# 22. Current artifact/repository structure

The research workspace currently contains or references:

-   `research_state.md`
-   `Research_Discovery_Report.md`
-   `README.md`
-   `candidate_ledger.csv`
-   `candidates.json`
-   `prior_art_graph.md`
-   `batch2_protocol.md`
-   `experiment_log.md`
-   `search_map.md`
-   `literature_matrix.csv`
-   `C39_formal_notes.md`
-   `C39_adversarial_review.md`
-   `C39_closest_papers.csv`
-   `incentive_distortion_pilot.py`
-   `verify_incentive_distortion.py`
-   `incentive_distortion_onebit_extension.py`
-   `incentive_distortion_baselines.py`
-   `incentive_distortion_boundaries.py`
-   `incentive_distortion_milp.py`
-   `dominance_memory_pilot.py`
-   killed-candidate scripts
-   raw JSON outputs
-   `frontier.png`
-   `frontier.svg`
-   `environment.json`
-   `artifact_hashes.json`

Reproducibility uses Python 3.10.11, NumPy 2.2.6 and SciPy 1.15.3 in the
recorded environment.

The key reproducibility commands are:

``` powershell
python -u incentive_distortion_pilot.py
python -u verify_incentive_distortion.py
python -u incentive_distortion_onebit_extension.py
python -u incentive_distortion_baselines.py
python -u incentive_distortion_boundaries.py
```

Optional MILP:

``` powershell
python -u incentive_distortion_milp.py
python -u incentive_distortion_boundaries.py
```

The MILP timeout must remain explicitly documented as inconclusive.

------------------------------------------------------------------------

# 23. Research methodology going forward

This is the operating protocol.

## Rule 1 --- Novelty is conceptual/formal

A different name is not a new idea.

If an existing mechanism captures the same phenomenon, kill it.

## Rule 2 --- Every candidate gets a predeclared kill test

Before implementing:

> What observation would make us abandon this?

Write it down.

## Rule 3 --- Cheapest kill first

Use:

1.  literature collision,
2.  reduction,
3.  exact toy model,
4.  exhaustive finite search,
5.  optimization,
6.  tabular agents,
7.  LLM integration.

Do not spend compute on an idea that fails a two-page proof.

## Rule 4 --- Strong baselines are mandatory

Always compare against the strongest obvious construction.

## Rule 5 --- Keep scopes exact

If K=2 is proven, do not silently generalize to K=16.

If a Hamming-family theorem is proven, do not call it an arbitrary-code
theorem.

## Rule 6 --- Upper bounds are not optimality

A construction is not a theorem of optimality.

## Rule 7 --- Failed searches are not evidence of absence

Record search coverage and access limitations.

## Rule 8 --- Separate mathematical and empirical evidence

Exact enumeration is not a statistical sample.

Random optimization seeds are not independent organizations.

LLM behavior is not proof of rational incentive compatibility.

## Rule 9 --- Explicitly test escape routes

Always ask:

-   Can immediate payment solve it?
-   Can a shared seed solve it?
-   Can an auxiliary audit channel solve it?
-   Can full-state storage solve it?
-   Can a simple repair-state bonus solve it?
-   Is the conflict merely an artifact of a bad modular baseline?

## Rule 10 --- If everything dies, restart discovery

C39 is not sacred.

If it fails the final gates, generate a new candidate batch.

The goal is the strongest publishable problem, not preserving C39.

------------------------------------------------------------------------

# 24. Master autonomous research prompt

Use the following as the instruction set for future deep research agents
/ coding agents:

> You are the research agent executing an adversarial research
> investigation, not a consultant giving suggestions.
>
> The objective is to discover and validate a genuinely novel,
> technically meaningful research problem in multi-agent systems /
> agentic AI, with primary relevance to MASO and possible relevance to
> SE4AgenticAI.
>
> Search broadly across multi-agent systems, agentic AI, organizational
> learning, coordination, adaptation, resilience, incentives, memory,
> provenance, delegation, debugging, fault tolerance, software
> engineering, distributed systems, MARL, mechanism design, economics,
> information theory, causal inference, control, operations research,
> security, and adjacent older literature.
>
> Novelty must be conceptual/formal. Keyword novelty is insufficient.
>
> For every promising candidate:
>
> 1.  State the exact research question.
> 2.  State the proposed mechanism/result.
> 3.  Identify the closest existing mechanisms.
> 4.  Search primary literature and read the relevant sections.
> 5.  Map the candidate to prior mechanisms explicitly.
> 6.  Define a predeclared kill test.
> 7.  Build the smallest exact mathematical model that can kill the
>     idea.
> 8.  Run exhaustive finite tests where feasible.
> 9.  Implement actual code and save all artifacts.
> 10. Attack the candidate with stronger baselines.
> 11. Search for alternative explanations.
> 12. Check whether a known theorem already implies the result.
> 13. Record every kill and why it died.
>
> Generate a broad initial pool of substantially different candidates.
> Do not stop at the first promising idea.
>
> Maintain persistent artifacts:
>
> -   `research_state.md`
> -   `candidate_ledger.csv`
> -   `prior_art_graph.md`
> -   `experiment_log.md`
> -   literature matrices
> -   formal notes
> -   code
> -   raw results
> -   plots
> -   environment/provenance files
>
> Every modified hypothesis gets a new candidate ID or an explicitly
> versioned refinement.
>
> Never silently broaden a theorem after a failed test.
>
> Never claim optimality from a local optimization.
>
> Never claim empirical organizational behavior from synthetic state
> enumeration.
>
> Never call a candidate novel merely because no exact keyword match was
> found.
>
> If a candidate is killed, record the strongest reason and move on.
>
> If all candidates are killed, generate another batch.
>
> Continue until one candidate survives:
>
> -   literature collision,
> -   conceptual equivalence,
> -   reduction to a known mechanism,
> -   formal triviality,
> -   stronger-baseline attacks,
> -   exact counterexamples,
> -   optimization attacks,
> -   adversarial reviewer objections,
> -   and a minimal realistic application test.
>
> The final output must distinguish:
>
> -   proven theorem,
> -   computational evidence,
> -   conjecture,
> -   literature-based inference,
> -   empirical evidence,
> -   unresolved risk.
>
> Do not describe a surviving candidate as submission-ready until those
> gates are actually passed.

------------------------------------------------------------------------

# 25. Current status in one screen

## WINNER

**C39 --- Reconstruction-Incentive Frontiers for Self-Contained Agent
Audit Records**

### Core phenomenon

A compressed record used both for:

-   reconstructing joint agent execution,
-   and paying agents later,

may need to sacrifice reconstruction quality to preserve unilateral
effort sensitivity.

### Strongest established result

Exact one-bit arbitrary-payment frontier for odd binary-action agent
teams.

### Additional result

Perfect-rate reconstruction and positive robust incentive margin are
incompatible under the self-contained/deferred-settlement assumptions.

### What is novel

Potentially the **finite-alphabet reconstruction-vs-unilateral-incentive
frontier**, not the underlying coding constructions.

### Confidence

Promising but not secure.

### Biggest threat

A prior theorem may already imply the frontier.

### Biggest mathematical gap

Sharp general `K>2` arbitrary-payment frontier.

### Biggest empirical gap

No real agent workflow has demonstrated that deferred settlement +
self-contained memory is a genuine constraint.

### Best venue now

**MASO**

### SE4AgenticAI condition

Needs a concrete checkpoint/trace-compaction/deferred-accountability
engineering case.

------------------------------------------------------------------------

# 26. Immediate next action

Do **not** start with an LLM experiment.

Do **not** start writing the paper.

Do **not** assume C39 is novel.

Start with the hardest kill:

## NEXT TASK

### "Can an existing constrained-monitoring / strategic-source-coding / implementation theorem already derive T1?"

Produce a theorem-by-theorem comparison.

If yes → kill/reframe.

If no → proceed immediately to certified `K=4/8/16` optimization.

Then test weighted/nonuniform settings.

Then build the tiny software-shaped workflow.

Only after all four survive should we invest in the paper and LLM
integration.

------------------------------------------------------------------------

# 27. Definition of success

We have succeeded only if we can eventually say:

> We identified a precise phenomenon that is not already captured by the
> closest literature; we can state a mathematically nontrivial theorem
> or impossibility result; we can defend its optimality or scope with
> certified analysis; stronger obvious mechanisms do not explain it
> away; and a realistic agent/software workflow makes the formal
> assumptions meaningful.

Anything weaker is a **research lead**, not a finished contribution.

------------------------------------------------------------------------

# 28. Final mental model

The entire project can be reduced to this:

``` text
              SAME COMPRESSED RECORD
                     |
          +----------+----------+
          |                     |
          v                     v
   RECONSTRUCT STATE       PAY AGENTS LATER
          |                     |
     wants states          wants effort
     to be merged          to remain
     efficiently           distinguishable
          |                     |
          +----------+----------+
                     |
                     v
          INFORMATION TRADEOFF
                     |
                     v
       What is the exact frontier?
                     |
                     v
     distortion  <--> incentive margin
                     |
          +----------+----------+
          |                     |
       theorem               application
          |                     |
        MASO             SE4AgenticAI
```

The research question is therefore **not** "how do we build a better
agent memory system?"

It is:

> **When one finite persistent record must simultaneously support later
> reconstruction and later incentive enforcement, what
> information-theoretic price must be paid for preserving unilateral
> effort sensitivity?**

That is the question we now need to either **kill decisively or prove
into a real paper**.
