# SE4AgenticAI 2026 Research Proposal: Causal, Repair-Validated Failure Attribution

**Working title:** From Blame to Repair: Intervention-Validated Failure Attribution in LLM-Based Multi-Agent Systems

**Short name:** RepairCheck-MAS

**Target venue:** [2nd IEEE Big Data International Workshop on Software Engineering for Agentic AI, SE4AgenticAI 2026](https://cs.uwaterloo.ca/~palencar/se4agenticai/)

**Submission deadline:** 10 October 2026

**Formats:** Short paper, 3-4 pages including references; regular paper, 8-10 pages including references; IEEE conference two-column format

**Review date:** 9 September 2026

> Administrative caution: the workshop website lists 2026 submission dates but currently states conference dates of 14-17 December 2025. This appears inconsistent and should be confirmed with the organizers before making travel or registration decisions.

## Reader's guide

This document serves two purposes. The first sections explain the idea without assuming knowledge of causal inference, software testing, or multi-agent systems. The later sections specify the research questions, benchmark, experiments, statistics, engineering, prior art, and submission strategy needed to turn the idea into a defensible paper.

The entire proposal can be summarized in one question:

> If a diagnostic method blames part of an agent system for a failure, does repairing that part actually make the system succeed?

That question sounds obvious, but most current evaluations do not test it. They compare a model's attribution with a human label or another model's judgment. RepairCheck-MAS instead treats repair as an experiment. It changes the blamed event, reruns the relevant part of the system many times, and measures whether the probability of success actually improves.

## Introduction for a general reader

### What is an LLM-based multi-agent system?

A multi-agent system uses several AI agents to complete one larger task. An agent is normally an LLM with a role, instructions, memory, and access to tools. A system might contain a planner, researcher, coder, tester, reviewer, and manager. These agents exchange messages and produce a chain of decisions that eventually changes an environment, such as a code repository, customer database, calendar, or email account.

Splitting work among agents can make a system more capable, but it also makes failures harder to understand. The final mistake may be visible in one agent's response even though the mistake originated several steps earlier. The visible agent may have acted reasonably given incorrect information supplied by another agent.

### The everyday analogy

Imagine a hospital team in which:

1. one person records the patient's symptoms;
2. another orders a test;
3. a laboratory produces a result;
4. a doctor selects a treatment; and
5. a nurse administers it.

If the treatment is wrong, blaming the nurse because they performed the final action would be misleading. The original problem could be an incorrect symptom record, the wrong test, a faulty result, or a mistaken interpretation. A useful investigation should ask what would have happened if each suspected mistake had been corrected.

Agent systems have the same problem, except that their decisions are probabilistic. Repeating an unchanged LLM call may produce a different answer. Consequently, one successful rerun after a repair does not prove that the repair caused the improvement. The system may simply have been lucky on that run.

### What are we trying to do?

We want to create an evaluation standard, benchmark, and experimental protocol called RepairCheck-MAS. It will judge failure-attribution methods by whether their diagnoses predict effective repairs.

The basic procedure is:

1. Run an agent system and record a detailed trace of agents, messages, tools, memory, and environment changes.
2. Identify a failed execution using an objective outcome test.
3. Ask one or more attribution methods which event caused the failure.
4. Repair or replace the event each method selected.
5. Replay the remainder of the workflow repeatedly under controlled conditions.
6. Estimate how much the repair changes the probability of success.
7. Compare that evidence with the original attribution rankings and human labels.

The central output is not merely a sentence saying who was at fault. It is evidence such as:

> Repairing event 12 increased task success from 8% to 71%, while repairing the visible error at event 29 increased success only to 13%.

That result distinguishes a plausible story from an operationally useful diagnosis.

### What this project contributes

The proposed paper is primarily a meta-evaluation paper. It does not need to claim that it has invented a universally superior debugging algorithm. Instead, it supplies a test for evaluating other attribution algorithms and explanations.

Its intended contributions are:

- a precise vocabulary separating roots, propagation points, symptoms, and repair sites;
- a collection of failed agent executions with executable outcome checks;
- controlled interventions at agent, message, memory, tool, and orchestration events;
- repeated replay procedures for probabilistic systems;
- metrics connecting a diagnosis to measured repair success;
- comparisons of observational, structural, and intervention-based attribution methods;
- evidence about when apparently correct explanations fail to predict useful repairs; and
- a reproducible artifact that other researchers can use to test their attribution methods.

### What the project does not claim

The project does not claim that causal debugging, fault injection, program slicing, counterfactual reasoning, or repair-based testing is new. Those ideas have decades of prior work. It asks whether existing attribution practices and causal-debugging assumptions transfer to LLM-based multi-agent executions, and it builds an evaluation standard for testing that transfer.

## Plain-language glossary

| Term | Meaning in this project |
|---|---|
| Agent | An LLM-based component given a role, context, and possibly tools or memory. |
| Multi-agent system | Several agents that communicate or delegate work to complete one task. |
| Trace | The recorded history of what agents, tools, memory, and the environment did. |
| Event | One recorded action, such as a message, model response, memory write, or tool call. |
| Failure attribution | A claim about which agent or event caused a failed outcome. |
| Observational attribution | A diagnosis based on inspecting what happened, without changing the execution. |
| Intervention | A controlled change to a suspected event followed by another execution. |
| Counterfactual | A question about what would have happened if one relevant event had been different. |
| Root cause | An upstream condition that generated or enabled the failure. |
| Propagation point | A step that carried or amplified an earlier error. |
| Symptom | A visible consequence of the error rather than its origin. |
| Repair site | A location where intervention can restore success, even if it is not the original root. |
| Oracle | An executable rule that determines whether the task actually succeeded. |
| Checkpoint | A saved execution and environment state from which replay can begin. |
| Stochastic | Capable of producing different results across otherwise similar runs. |
| Repair probability | The estimated fraction of controlled repaired runs that succeed. |
| Negative control | A change expected not to repair the problem, used to detect misleading effects. |

## Executive summary

LLM-based multi-agent systems distribute reasoning and action across planners, specialists, critics, memory components, tool users, and human approval points. When the overall system fails, developers need to know which component caused the failure and which intervention will repair it. Current failure-attribution methods generally infer a responsible agent or decisive step from observed traces. A plausible attribution, however, is not necessarily causal. The blamed event may be a visible symptom, an error-propagation point, or a downstream response to an earlier hidden defect.

This proposal introduces an intervention-based standard for evaluating multi-agent failure attribution:

> An attribution is useful only if repairing the attributed agent-step, while controlling the rest of the execution as carefully as possible, reliably changes the failed outcome.

The project will construct checkpointed pairs of failed and repaired multi-agent executions using controlled fault injection. It will distinguish root causes, propagation points, observable symptoms, and repair opportunities. Candidate attribution methods will be evaluated not only against human labels, but also through counterfactual replay and measured repair success.

The central research question is:

> Can intervention-validated attribution identify multi-agent failure causes more reliably and more usefully than attribution based only on observational traces?

The proposal is a strong match for SE4AgenticAI because it directly addresses testing, verification, validation, observability, traceability, reproducibility, evaluation, and maintenance of agentic systems.

## Why this is a strong SE4AgenticAI fit

### Why submit this work

This is a good submission candidate because the research question is important, directly testable, and aligned with the workshop's stated scope. Agent systems are increasingly permitted to write code, query databases, interact with users, and take external actions. When those systems fail, developers need explanations that help them repair the system rather than explanations that merely sound credible.

The work is especially suitable for SE4AgenticAI for six reasons:

1. **It is fundamentally a software-engineering problem.** The paper concerns testing, debugging, observability, reproducibility, fault localization, and repair.
2. **It produces an executable artifact.** Reviewers can inspect the traces, rerun interventions, and test additional attribution methods.
3. **It has a falsifiable central claim.** The experiment can reveal that observational attribution and repair success agree, disagree, or agree only under particular conditions.
4. **It connects modern agents to mature engineering research.** AID, causal testing, delta debugging, fault injection, and program slicing are treated as foundations rather than ignored.
5. **It can influence evaluation practice.** If attribution methods are currently ranked using labels that do not predict repairs, the community needs a better evaluation target.
6. **It remains useful without a complex new model.** A careful benchmark and a surprising empirical result can be a complete contribution even if the best attribution method is simple.

The most persuasive submission framing is:

> RepairCheck-MAS is an evaluation standard for determining whether failure-attribution methods identify interventions that improve system outcomes.

It should not be framed primarily as a new causal-discovery algorithm or as a claim that LLM nondeterminism has never been studied. Both framings create unnecessary prior-art exposure and obscure the cleaner contribution-type distinction.

| Workshop topic | Fit | Contribution |
|---|---:|---|
| Testing, verification, and validation | 10/10 | The work defines an executable causal test for failure-attribution claims. |
| Observability and audit trails | 10/10 | It evaluates which trace evidence is necessary for diagnosis and repair. |
| Evaluation approaches and frameworks | 10/10 | It contributes a benchmark, metrics, intervention protocol, and baselines. |
| Reproducibility and traceability | 10/10 | Checkpointed environments and controlled replay are central artifacts. |
| Design and architecture of multi-agent systems | 8/10 | It studies how topology and component boundaries affect failure propagation. |
| Empirical studies of agent frameworks | 9/10 | Equivalent failures will be exercised across several frameworks. |
| Self-adaptation | 8/10 | Repair and recovery policies can be evaluated after causal localization. |
| Dynamic agentic execution | 9/10 | The benchmark captures long, branching, and cyclic agent trajectories. |
| Human-in-the-loop | 7/10 | Human approval and diagnostic escalation can be modeled as causal components. |
| Agent-tool protocols | 7/10 | Tool responses, task state, and protocol handoffs are included as fault locations. |

This paper should be framed as software-engineering research. The main artifact is not another agent framework. It is a method and evaluation infrastructure for determining whether failure explanations lead to successful repairs.

## Motivating example

Consider a software-release multi-agent workflow:

1. A planner decomposes an issue into code changes and tests.
2. A repository agent retrieves relevant files.
3. A coding agent edits the implementation.
4. A test agent executes the suite and summarizes failures.
5. A review agent inspects the patch.
6. A release agent decides whether the change is ready.

Suppose the final patch fails a hidden integration test. A diagnostic model blames the coding agent because it produced the faulty line. That attribution may still be wrong or incomplete:

- The repository agent omitted a required configuration file.
- The planner specified an invalid decomposition.
- The test agent summarized a failing test incorrectly.
- The review agent received truncated context.
- Several agents shared the same incorrect assumption.
- The coding step was locally reasonable given corrupted upstream information.
- Replacing the coding response would not repair the run because the planner would recreate the same error.

Observational attribution asks which event looks responsible. Causal attribution asks which controlled intervention changes the outcome and through what pathway.

## Precise research gap

The gap is not generic fault localization, causal debugging, fault injection, or program repair. Each has a substantial classical literature. Recent multi-agent work also provides failure taxonomies, annotated traces, and agent-step attribution benchmarks.

The defensible gap is:

> Existing LLM multi-agent failure-attribution research primarily evaluates agreement with observational labels. It does not yet provide a mature, reproducible standard for validating whether the attributed agent-step is causally responsible and whether repairing it reliably repairs the system outcome under stochastic, interacting, and long-horizon execution.

This gap contains five concrete problems:

1. **Correlation versus causation:** the most suspicious trace event may only correlate with the failure.
2. **Root cause versus propagation:** a downstream handoff may make an upstream problem visible without originating it.
3. **Multiple causes:** two faults may each be sufficient, jointly necessary, or mutually reinforcing.
4. **Stochastic replay:** changing one response can alter the entire downstream trajectory, making naive before-after comparison unreliable.
5. **Repair utility:** a diagnostically correct label may still be too broad or too late to guide an effective repair.

### The gap in detail

Current evaluation commonly follows this pattern: researchers collect failed traces, humans or expert models label the responsible agent and step, and a new attribution method is scored by agreement with those labels. This establishes label prediction, not causal validity. A label can be reasonable and reproducible while still identifying an event whose replacement rarely repairs the task.

There are four different objects that existing evaluations can accidentally collapse into one:

1. **Origin:** where incorrect information, state, or intent first entered the execution.
2. **Propagation:** where the error was copied, trusted, amplified, or converted into another form.
3. **Observation:** where the failure became visible to a human or evaluator.
4. **Control:** where a practical intervention can prevent the final failure.

These objects sometimes coincide, but they need not. For example, a planner may omit a requirement, a coder may implement the resulting incomplete plan correctly, and a test agent may be the first component to expose the defect. The planner is the origin, the coding response is a propagation point, the failed test is a symptom, and adding a verification step before coding may be the cheapest repair site.

The project therefore asks two separate questions:

- **Causal question:** Which event or combination of events made the failure more likely?
- **Engineering question:** Which feasible repair most reliably restores success at acceptable cost and risk?

### Why this remains a research gap

The gap persists even though several neighboring fields are mature:

- Failure taxonomies describe recurring error types but do not prove that a labeled event caused a particular outcome.
- Trace-attribution benchmarks measure agreement with annotated agents or steps but generally do not validate those labels with repair experiments.
- Observability frameworks improve the information available to investigators but do not determine which observed event is causally responsible.
- Agent benchmarks evaluate final success and sometimes intermediate progress but do not ordinarily test whether a diagnosis predicts a successful repair.
- Classical causal debugging intervenes on program predicates, inputs, or schedules, but its assumptions do not automatically resolve semantic agent events, non-canonical repairs, external tool effects, or probabilistic suffixes.
- Fault injection supplies controlled failures, but knowing where a fault was injected is not identical to proving where an effective or actual cause lies. A fault may be masked, amplified, or interact with native defects.

The missing object is a reproducible bridge between an attribution and its operational consequence:

```text
attribution claim
    -> controlled repair at the claimed location
    -> repeated counterfactual replay
    -> measured change in task-success probability
```

### Why the gap is difficult

This is not solved by replacing one message and rerunning once. Several complications must be handled explicitly:

1. **LLM variation:** an unchanged suffix can succeed or fail across samples.
2. **Trajectory divergence:** a small repair can generate an entirely different downstream conversation.
3. **No canonical replacement:** unlike substituting a known passing program value, several semantically different agent responses may all be valid repairs.
4. **Stateful tools:** sending an email, placing an order, editing a repository, or writing memory can alter external state and may not be safely reversible.
5. **Multiple causation:** failures can be conjunctive, disjunctive, redundant, or overdetermined.
6. **Repair versus cause:** a downstream guard may prevent failure without being the event that originally caused it.
7. **Confounding:** model choice, prompts, temperature, tool state, and earlier messages can affect both the suspected event and the outcome.
8. **Oracle quality:** an evaluator must distinguish genuine task success from a plausible final answer.
9. **Intervention validity:** a repair must preserve the intended task rather than make the test pass by changing the goal.
10. **Cost:** exhaustive intervention at every trace event can require many model and environment executions.

Solving these measurement problems is itself a substantial research contribution.

## State of the art

### Modern multi-agent failure research

#### Failure taxonomies

Cemri et al., [Why Do Multi-Agent LLM Systems Fail?](https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2025 Datasets and Benchmarks, develop MAST and identify 14 failure modes across system design, inter-agent misalignment, and verification or termination. This establishes a valuable descriptive and annotation foundation. It does not make a taxonomy label causal merely by assigning it to a trace.

#### Agent and step attribution

Zhang et al., [Which Agent Causes Task Failures and When?](https://proceedings.mlr.press/v267/zhang25cq.html), ICML 2025, introduce Who&When using execution logs from 127 multi-agent configurations. The reported best performance remains limited, particularly for decisive-step localization. This demonstrates that observational attribution is difficult even before causal validity is tested.

Chen et al., [Seeing the Whole Elephant](https://aclanthology.org/2026.acl-long.912/), ACL 2026, introduce TraceElephant with full traces and reproducible environments. Their results show that full observability can substantially improve attribution. The remaining question is whether improved label prediction also identifies interventions that repair the outcome.

Deshpande et al., [TRAIL](https://arxiv.org/abs/2505.08638), 2025, provide human-annotated traces from GAIA and SWE-bench and show that trace debugging remains challenging. This supports the need for a stronger validation target than subjective diagnosis alone.

TRAIL's verified title is *TRAIL: Trace Reasoning and Agentic Issue Localization*. It contains 148 human-annotated single-agent and multi-agent traces, and its reported best model solves only about 11% of the benchmark. This is evidence that reasoning over traces is difficult, but TRAIL still evaluates localization rather than whether the localized event predicts an effective repair.

#### Observability infrastructure

[AgentTrace](https://arxiv.org/abs/2602.10133), whose verified title is *AgentTrace: A Structured Logging Framework for Agent System Observability*, separates operational, cognitive, and contextual logging for agent systems. It is directly useful as an observability reference and possible trace-design input. Structured logging makes causal testing possible, but logging alone does not validate a causal attribution. RepairCheck-MAS operates one layer above observability: it uses recorded events to construct interventions and measure repair effects.

#### Process-aware agent evaluation

[AgentBoard](https://proceedings.neurips.cc/paper_files/paper/2024/hash/877b40688e330a0e2a3fc24084208dfa-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2024, provides fine-grained evaluation of multi-turn agent progress. It demonstrates why final success alone hides process failures.

[tau-bench](https://arxiv.org/abs/2406.12045), ICLR 2025, uses executable end-state evaluation and repeated-run reliability measures for tool-agent-user interaction. It offers useful environments and a strong repeated-execution precedent, but it is not a causal attribution benchmark.

[MultiAgentBench](https://aclanthology.org/2025.acl-long.421/), ACL 2025, evaluates collaboration and competition under multiple coordination topologies using milestone-based metrics. It supplies suitable multi-agent tasks, but not intervention-grounded failure causes.

[OSWorld](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5d413e48f84dc61244b6be550f1cd8f5-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2024, provides executable computer-use tasks with state-based evaluation. Its reproducible environments are helpful for testing causal interventions involving real applications.

### Classical prior art that must be acknowledged

The project must not claim to invent counterfactual debugging, causal fault localization, program slicing, failure-inducing input isolation, or fault injection.

#### Program slicing

Weiser's [Program Slicing](https://courses.cs.washington.edu/courses/cse503/11au/readings/weiser-slicing-icse81.pdf), ICSE 1981, reduces programs to the portions relevant to selected behavior. It is a foundational method for tracing dependencies from outcomes back to program elements.

#### Fault injection

Arlat et al., [Fault Injection for Dependability Validation](https://homepages.laas.fr/arlat/documents/89124/89124.pdf), IEEE TSE 1990, establish a systematic methodology for deliberately introducing faults and measuring their effects on system dependability.

#### Delta debugging

Zeller and Hildebrandt, [Simplifying and Isolating Failure-Inducing Input](https://www.cs.columbia.edu/~junfeng/08fa-e6998/sched/readings/delta-debug-input.pdf), IEEE TSE 2002, isolate minimal failure-inducing circumstances by comparing passing and failing executions.

#### Structural causal models

Halpern and Pearl, [Causes and Explanations: A Structural-Model Approach](https://doi.org/10.1093/bjps/axi147), 2005, formalize actual causation using structural equations and counterfactuals. Their treatment is relevant to necessity, sufficiency, contingency, and multiple causes.

#### Causal testing

Johnson, Brun, and Meliou, [Causal Testing](https://arxiv.org/abs/1809.06991), use counterfactual executions to identify defect causes and evaluate the method on Defects4J and with developers.

Fariha, Nath, and Meliou, [Causality-Guided Adaptive Interventional Debugging](https://www.microsoft.com/en-us/research/publication/causality-guided-adaptive-interventional-debugging/), SIGMOD 2020, combine statistical debugging, causal analysis, fault injection, and adaptive interventions to discover root causes and causal paths for intermittent failures.

#### Targeted comparison with AID

AID is the nearest classical neighbor and must be treated as foundational work, not merely included in a long reference list. It already addresses intermittent failure, runtime nondeterminism, causal graphs, fault injection, and adaptive selection of interventions. Therefore, the proposal cannot defend its novelty by saying that conventional software is deterministic or that intervention-based debugging is absent.

A direct reading of the AID paper establishes the following:

- AID diagnoses intermittent failures caused by timing, thread scheduling, transient faults, and other runtime nondeterminism.
- It begins with successful and failed predicate logs and selects fully discriminative predicates.
- It uses temporal precedence to construct an approximate causal directed acyclic graph.
- It intervenes on predicates by changing them toward values observed in successful executions.
- It uses adaptive group testing to reduce the number of intervention runs.
- Its intended output is a root cause and a causal explanation path from that root to the failure.
- Its general group-testing description allows `D` defective items and gives an `O(D log N)` intervention bound.
- Its applied causal model nevertheless explicitly assumes counterfactual causality and a single root cause.
- It can represent conjunctive causes by preconstructing a compound predicate such as `A and B`.
- It explicitly does not support disjunctive root causes because they are not counterfactual causes under its chosen definition.
- It restricts intervention to developer-declared safe predicates. Methods that change internal or external state may be removed because their side effects can invalidate the intervention.

The multiple-cause distinction must consequently be stated carefully. It would be inaccurate to say simply that AID's group testing handles only one defective item. A precise comparison is:

> AID applies a single counterfactual root-cause model; conjunctive causes must be represented as compound predicates, and disjunctive roots are unsupported. RepairCheck-MAS explicitly evaluates single, conjunctive, disjunctive, redundant, and overdetermined agent-level causes without requiring the benchmark user to precompile them into one predicate.

The strongest differences are structural rather than claims about stochasticity:

| Dimension | AID | RepairCheck-MAS |
|---|---|---|
| Contribution type | A diagnostic algorithm for discovering a root cause and explanation path | A meta-evaluation benchmark for testing whether attribution methods predict effective repairs |
| Primary diagnostic unit | Instrumented program predicate | Semantic agent, message, memory, tool, environment, or orchestration event |
| Validation target | Whether intervention on predicates identifies the root and causal path | Whether an attribution predicts a meaningful increase in task-success probability |
| Replacement value | Generally moves a predicate toward a value observed in successful executions | Often has no unique correct repair; several semantically distinct replacements may be valid |
| State effects | Excludes interventions that cannot be declared safe, including problematic state-changing methods | Must measure, sandbox, or explicitly rule out semantic and potentially irreversible tool effects |
| Multiple causation | Single-root counterfactual model; conjunction through compound predicates; no disjunctive roots | Explicit experimental conditions for single, conjunctive, disjunctive, redundant, and overdetermined causes |
| Evaluation role | One method that could be adapted as a baseline | A standard on which AID-inspired and other attribution methods can be compared |

The proposed paper should lead with the first row. Nondeterminism remains a methodological complication, but it is not the primary novelty defense because AID already handles important forms of nondeterministic software failure.

### How AID should be used in this project

AID should influence the research rather than appear only as a threat:

1. Use an AID-inspired intervention strategy as a causal baseline where event predicates can be constructed.
2. Compare adaptive intervention with exhaustive event intervention on a small subset.
3. Report when fully discriminative predicate filtering fails for probabilistic agent events.
4. Separate failures caused by safe, reversible internal events from failures involving external state.
5. Test single-root conditions before extending to conjunction, disjunction, and overdetermination.
6. Credit AID for the general mechanism while positioning RepairCheck-MAS as the evaluation standard and agent-specific experimental adaptation.

#### Metamorphic testing

Chen, Cheung, and Yiu, [Metamorphic Testing](https://www.cse.ust.hk/faculty/scc/publ/CS98-01-metamorphictesting.pdf), 1998, generate related test cases whose outcomes should satisfy defined relations. Metamorphic relations are useful when exact output oracles are difficult to specify.

These literatures own the general ideas of interventions, counterfactuals, cause isolation, dependency analysis, and repair-oriented debugging. The new work must show what changes when the unit under diagnosis is a stochastic multi-agent trajectory rather than a deterministic program statement or input fragment.

## Novelty boundary

### Claims that must not be made

- Failure attribution is new.
- Counterfactual debugging is new.
- Repair-based validation is universally new.
- Fault injection is new.
- Causal graphs for debugging are new.
- Trace-based failure localization is new.
- Multi-agent failure taxonomies are missing.
- Full observability has not been studied.

### Defensible contribution

The strongest claim is empirical and methodological:

> We adapt intervention-based causal validation to stochastic LLM multi-agent executions, define replay and control procedures needed to separate intervention effects from sampling variation, and evaluate whether modern attribution methods identify repairs that reliably restore system-level success.

Potentially novel elements include:

- A benchmark containing paired failed and intervention-repaired multi-agent traces.
- A fault model spanning agents, messages, memory, tools, orchestration, verification, termination, and human approval.
- Explicit separation of root causes, propagation points, symptoms, and repair sites.
- A stochastic counterfactual replay protocol with common-randomness and repeated-intervention estimates.
- Evaluation of interacting and overdetermined causes rather than only one injected fault.
- Repair success as a primary attribution metric.
- Cross-framework evidence about how architecture affects diagnosability.

## Research questions

### Primary question

**RQ1:** Does intervention-validated attribution predict successful repairs more reliably than observational trace-label attribution?

### Supporting questions

**RQ2:** How often do existing attribution methods identify a symptom or propagation point rather than a causal root?

**RQ3:** Which trace representations and architectural signals are necessary to distinguish root causes from downstream manifestations?

**RQ4:** How should causal effects be estimated when repairing one step changes a stochastic downstream trajectory?

**RQ5:** How accurately can attribution methods identify multiple sufficient, jointly necessary, or interacting faults?

**RQ6:** Do methods trained on injected failures generalize to naturally occurring failures and held-out fault classes?

**RQ7:** How do topology, framework, model heterogeneity, trace length, and shared memory affect attribution and repair success?

**RQ8:** What is the quality-cost trade-off between exhaustive intervention search, adaptive intervention, graph-based localization, and LLM-judge diagnosis?

## Hypotheses

- **H1:** Agreement with observational labels will overestimate causal attribution quality compared with intervention-validated repair success.
- **H2:** Full traces will improve localization accuracy but will not eliminate symptom-root confusion.
- **H3:** Temporal and dependency-aware methods will outperform transcript-only LLM judges on causal repair success.
- **H4:** Methods that perform explicit interventions will be better calibrated than purely observational methods.
- **H5:** Attribution accuracy will decline substantially under interacting faults, cycles, shared memory, and correlated agent errors.
- **H6:** Attribution rankings will vary across frameworks even when task and model are held constant.
- **H7:** Adaptive intervention search will achieve similar causal accuracy to exhaustive search at substantially lower token and execution cost.

## Conceptual model

### Units

An execution is represented as a versioned event graph:

```text
Execution
  -> agent invocation
  -> message or handoff
  -> memory read or write
  -> tool invocation and result
  -> environment transition
  -> verifier or judge decision
  -> human approval or intervention
```

Each event records:

- Stable event identifier
- Parent and causal-dependency identifiers
- Agent role and implementation
- Model and configuration
- Input and output hashes
- Sanitized content or content reference
- Memory version
- Tool and environment state version
- Timing and retry information
- Randomness controls where available
- Outcome predicates affected by the event

### Four labels

The benchmark should distinguish four concepts:

1. **Root cause:** an event or condition whose intervention has a necessary or substantial causal effect on failure.
2. **Propagation point:** an event that transmits or amplifies an earlier fault.
3. **Symptom:** an event that reveals failure without causing it.
4. **Repair site:** a location where intervention can restore success, even if it is not the original cause.

A repair site can differ from a root cause. This distinction is important because software maintenance may prioritize the cheapest robust repair rather than the earliest causal event.

## Causal estimands

Let `Y = 1` denote system success and `I_e` denote an intervention that repairs event `e`. The primary empirical estimand is:

```text
ACE(e) = P(Y = 1 | do(I_e = repair)) - P(Y = 1 | do(I_e = unchanged))
```

Because model APIs and downstream environments are stochastic, each intervention must be repeated. Report a distribution and confidence interval rather than a single counterfactual outcome.

Additional estimands:

- Probability of necessity: how often failure would not occur without the fault.
- Probability of sufficiency: how often introducing the fault produces failure.
- Repair probability: how often repairing the attributed event restores success.
- Robust repair probability: how often success persists across downstream sampling variation.
- Minimal repair set: the smallest set of interventions needed to restore success.
- Propagation effect: change in downstream error mass when the event is repaired.

The project should state clearly whether it estimates interventional causality in a controlled benchmark or claims actual causality in naturally occurring executions. The former is more defensible.

## Benchmark design

### Recommended scope

Use two primary domains and one secondary validation domain:

1. **Tool-mediated customer service:** tau-bench retail or airline tasks provide executable state and policy oracles.
2. **Software engineering:** a constrained SWE-bench-style issue-to-patch workflow provides objective tests and realistic multi-agent roles.
3. **Optional computer use:** OSWorld provides a secondary external-validity check.

Do not start by supporting every benchmark. A clean causal evaluation on two domains is stronger than shallow support for six.

### Frameworks

Implement equivalent workflows in at least three systems, such as:

- AutoGen
- CrewAI
- LangGraph

If exact equivalence is impossible, document and measure architectural differences rather than hiding them.

### Models

Include:

- At least one strong proprietary model
- At least one strong open-weight model
- At least one smaller or cheaper model
- Homogeneous and heterogeneous agent teams

Version-pin model identifiers where providers permit it and record access dates.

## Fault model

### Planner faults

- Missing required subtask
- Incorrect dependency
- Invalid ordering
- Premature termination condition
- Wrong role assignment

### Message and handoff faults

- Omitted evidence
- Corrupted value
- Referential drift
- Ambiguous instruction
- Message truncation
- Delayed, duplicated, or reordered handoff

### Agent faults

- Incorrect reasoning result
- Hallucinated fact
- Wrong tool selection
- Overconfident conclusion
- Sycophantic agreement
- Failure to ask for clarification

### Memory faults

- Stale retrieval
- Poisoned memory
- Missing write
- Incorrect consolidation
- Cross-agent contamination
- Contradictory state

### Tool faults

- Incorrect result
- Timeout

- Partial failure
- Schema drift
- Stale API response
- Irreversible side effect followed by error

### Verification faults

- False approval
- False rejection
- Incomplete test coverage
- Biased LLM judge
- Incorrect consensus

### Orchestration faults

- Incorrect routing
- Retry storm
- Duplicate execution
- Deadlock or livelock
- Agent crash
- Budget exhaustion

### Human-in-the-loop faults

- Incorrect approval
- Delayed response
- Ambiguous correction
- Approval applied to the wrong state

## Fault injection procedure

1. Execute a clean baseline and preserve all observable state.
2. Select an injection location and fault operator.
3. Inject the fault deterministically where possible.
4. Confirm that the fault is activated and reaches the execution.
5. Retain cases producing an objectively verified failure.
6. Record the true injection location separately from benchmark-facing labels.
7. Generate controlled repairs at the root, propagation points, and plausible symptoms.
8. Replay each intervention repeatedly.
9. Measure whether and how often the outcome changes.
10. Hold out fault operators and workflows for generalization evaluation.

Injection location is not automatically the only true cause. The experimental environment must allow a fault to be masked, amplified, or combined with naturally occurring errors.

## Stochastic replay protocol

Naive replay is the largest methodological risk. The following controls are recommended:

- Snapshot external environment state before the intervention.
- Pin prompts, policies, tools, framework commits, and model versions.
- Reuse recorded tool outputs when testing an upstream language-only intervention, unless tool response adaptation is itself part of the causal path.
- Use common random seeds for local models and simulators where meaningful.
- Repeat cloud-model interventions enough times to estimate outcome probability.
- Distinguish exact replay, partial replay, and live resampling.
- Report the first event where repaired and control traces diverge.
- Use negative-control interventions at unrelated events.
- Include sham repairs that modify formatting without changing semantics.
- Measure intervention leakage into supposedly fixed components.

Three replay modes should be reported:

1. **Frozen suffix replay:** recorded downstream responses are replayed to isolate local structural effects.
2. **Live suffix replay:** downstream agents resample naturally, estimating practical repair effectiveness.
3. **Hybrid replay:** deterministic tools and state are frozen while language agents resample.

Frozen replay supports causal isolation but can be unrealistic. Live replay captures operational repair utility but increases variance. Reporting both is a strength.

## Attribution methods to compare

### Baselines

- Random agent and random step
- Last agent before failure
- Earliest anomalous step
- Injection-location oracle
- Human expert trace annotation
- Single whole-trace LLM judge
- Diverse LLM judge panel
- Who&When-style attribution baseline
- TraceElephant-compatible attribution baseline

### Structural methods

- Temporal dependency graph ranking
- Message and artifact provenance slicing
- Graph neural network over event traces
- Spectrum-style suspiciousness from passing and failing traces
- Delta-debugging-style event minimization

### Causal methods

- Exhaustive single-event intervention
- Adaptive group intervention
- Causal-graph-guided search
- Bayesian experimental design
- Intervention-aware LLM diagnostic agent

The benchmark must not make the proposed method the only approach capable of using intervention data. Provide a clean API so other researchers can implement new attribution and search methods.

## Evaluation metrics

### Localization

- Responsible-agent top-1 and top-k accuracy
- Decisive-step exact accuracy
- Step distance from causal event
- Span intersection-over-union
- Root-cause precision, recall, and F1
- Ranking quality

### Causal validity

- Repair success probability
- Average causal effect of repair
- Probability of necessity and sufficiency
- Minimal intervention-set accuracy
- False-causal attribution rate
- Symptom-root confusion rate
- Propagation-point confusion rate

### Calibration

- Brier score
- Expected calibration error
- Risk-coverage curve
- Selective accuracy under abstention

### Operational value

- Time to diagnosis
- Number of interventions
- Token and monetary cost
- Environment executions
- Time to successful repair
- Regression rate introduced by repair
- Robust success under resampling

### Reproducibility

- Replay success rate
- First-divergence position
- Run-to-run variance
- Cross-laboratory reproduction rate
- Architecture-ranking stability

## Experimental matrix

The full matrix can become too large. Prioritize these factors:

| Factor | Minimum levels |
|---|---|
| Domain | Customer service, software engineering |
| Framework | Three frameworks |
| Model team | Strong homogeneous, smaller homogeneous, heterogeneous |
| Fault layer | Planner, handoff, memory, tool, verifier, orchestration |
| Fault count | One, two interacting |
| Trace visibility | Partial, full structured trace |
| Replay | Frozen, live, hybrid |
| Attribution method | At least six meaningful baselines |

Use a fractional factorial or carefully blocked design rather than executing every possible combination.

## Statistical analysis

- Use hierarchical logistic or Bayesian models for repair success.
- Treat workflow, framework, model, fault operator, and trace length as varying effects.
- Report confidence or credible intervals, not only mean accuracy.
- Correct for repeated comparisons where appropriate.
- Use paired analysis because attribution methods evaluate the same failures.
- Conduct sensitivity analysis over the number of replay samples.
- Report rank reversals between observational accuracy and causal repair success.
- Analyze single and interacting faults separately.
- Predefine primary metrics before the final experiment.
- Publish negative and null results.

At least 20 independent repetitions per important intervention condition are desirable unless a power or precision analysis supports another number.

## Ablation studies

- Remove causal interventions and use observational traces only.
- Remove graph structure and use linear transcripts.
- Remove message provenance.
- Remove memory versions.
- Replace executable oracles with an LLM judge.
- Use only one replay instead of repeated estimates.
- Remove negative controls.
- Restrict evaluation to single faults.
- Freeze versus resample downstream agents.
- Train and test on the same versus held-out fault operators.

## Expected contributions

1. **Problem definition:** a precise distinction between trace-label attribution and repair-validated causal attribution.
2. **Benchmark:** paired failed and repaired multi-agent traces with executable outcome oracles.
3. **Fault library:** reproducible operators across reasoning, communication, memory, tools, orchestration, verification, and human approval.
4. **Replay protocol:** controlled intervention procedures for stochastic multi-agent systems.
5. **Metrics:** repair success, causal effect, symptom-root confusion, and minimal repair sets.
6. **Empirical study:** evidence about which attribution methods actually predict repairs.
7. **Engineering guidance:** recommendations for observable, diagnosable, and repairable agent architectures.

## Threats to validity

### Construct validity

Injected fault location, causal root, repair site, and organizational responsibility are different constructs. The benchmark must not equate them.

### Internal validity

Cloud-model nondeterminism may make an intervention appear effective by chance. Repeated replay, negative controls, frozen environment state, and confidence intervals are mandatory.

### External validity

Injected faults may not represent naturally occurring failures. Include a smaller corpus of naturally observed failures from framework issue trackers, benchmark runs, or manually reproduced incidents.

### Oracle validity

LLM judges are not reliable primary outcome oracles. Prefer database state, tests, policy predicates, files, and environment state. Use expert annotation for semantic cases and report inter-rater agreement.

### Intervention validity

Repairing one step may unintentionally modify several semantic variables. Define intervention scope carefully and measure trace divergence.

### Multiple causation

Single-fault benchmarks can make methods appear unrealistically strong. Include interacting and overdetermined cases.

### Framework equivalence

Different frameworks encode state, retries, and message routing differently. Do not claim exact equivalence without evidence. Treat architecture as an experimental factor.

## Ethical considerations

- Use sandboxed tools and environments.
- Do not inject faults into production systems.
- Remove secrets, personal data, and proprietary prompts from released traces.
- Clearly distinguish technical causality from moral, organizational, or legal blame.
- Avoid releasing directly reusable attacks against live services.
- Document provider data-retention policies.
- Report whether human trace annotators encounter sensitive or harmful content.

## Reproducibility package

The artifact should include:

- Version-pinned containers
- Framework commits and configuration
- Model identifiers and access dates
- Prompts and role definitions
- Workflow specifications
- Fault operators
- Environment snapshots
- Trace schema
- Replay controller
- Executable oracles
- Attribution baseline implementations
- Intervention results
- Statistical analysis scripts
- A reproducibility card

For provider-hosted models that cannot be frozen, preserve raw responses where licensing permits and clearly separate replayable from non-replayable experiments.

## Engineering architecture

```text
Task source
  -> workflow adapter
  -> agent framework
  -> instrumented event bus
  -> tools and environment

Fault controller
  -> selects event and operator
  -> injects controlled mutation

Trace recorder
  -> records event graph and versions
  -> checkpoints environment state

Attribution runner
  -> executes diagnostic methods
  -> produces ranked agent-step hypotheses

Replay controller
  -> applies candidate repair
  -> runs frozen, live, or hybrid suffix

Oracle and analyzer
  -> evaluates system outcome
  -> estimates causal and repair metrics
```

### Component responsibilities

1. **Workflow adapter:** maps benchmark tasks into equivalent roles and tools for each framework.
2. **Event bus:** provides stable interception points for messages, memory, tools, and agent calls.
3. **Fault controller:** applies deterministic, versioned fault operators.
4. **Trace recorder:** produces a framework-neutral causal event graph.
5. **Checkpoint manager:** preserves environment and tool state.
6. **Attribution runner:** normalizes outputs from baselines and proposed methods.
7. **Replay controller:** performs controlled interventions and repeated suffix execution.
8. **Oracle:** evaluates final state and process constraints.
9. **Analyzer:** estimates effects, uncertainty, calibration, and cost.

## Week-1 scientific go/no-go gate

The project must demonstrate the central phenomenon before building general event-graph, checkpointing, or cross-framework infrastructure. Otherwise, several weeks could be spent constructing a platform before learning whether observational blame and repair effectiveness differ in a measurable way.

### Minimal experiment

Use the smallest end-to-end setting that still contains a meaningful causal chain:

1. Select one agent framework.
2. Select one executable tau-bench task with an objective outcome oracle.
3. Obtain one reproducible failure.
4. Introduce or identify one upstream fault.
5. Mark three candidate intervention locations: root, propagation point, and visible symptom.
6. Construct a controlled repair for each candidate.
7. Replay each repaired suffix enough times to estimate a repair probability.
8. Run at least one observational attribution method on the original failed trace.
9. Compare its ranking with the intervention-measured repair ranking.

In plain language, the pilot asks: if we fix the first mistake, the place it spread, or the place it became visible, which fix actually works most often, and does the diagnostic method choose that location?

### Minimum measurements

For every candidate repair, record:

- baseline success probability without repair;
- success probability after repair;
- absolute and relative improvement;
- confidence interval or Bayesian credible interval;
- number of executions and token cost;
- first point at which repaired and original traces diverge;
- whether the intervention changed the task's intended meaning;
- internal and external state changes; and
- the observational attribution rank of the repaired event.

### Decision rule

Proceed to general infrastructure if the pilot shows both of the following:

1. repair probabilities differ materially across root, propagation, and symptom interventions; and
2. at least one credible observational attribution ranks those locations differently from their measured repair utility.

The pilot need not establish statistical generality. Its purpose is to demonstrate that the proposed measurement captures a real and non-trivial phenomenon.

If the intervention effects do not differ, do not conceal the result. First check intervention validity, oracle sensitivity, and whether the chosen failure has a meaningful causal chain. If several well-chosen pilot failures remain uninformative, narrow, pivot, or stop the project before building a general platform.

## Implementation plan from start to finish

### Phase 0: Prove the phenomenon

1. Run the week-1 minimal experiment above.
2. Write the result as a single trace diagram and repair-probability table.
3. Confirm that the disagreement is not created by a broken outcome oracle or semantically invalid repair.
4. Record the exact prompt, model, framework, seed controls, tool state, and number of trials.

**Exit criterion:** a defensible example in which candidate repair locations produce meaningfully different outcomes and an observational diagnosis does not trivially recover their ordering.

### Phase 1: Freeze the scientific claim

1. State that the work evaluates causal and repair utility, not the invention of causal debugging.
2. Define root cause, propagation point, symptom, and repair site.
3. Select two domains and three frameworks.
4. Choose primary metrics before implementation.
5. Create a prior-art comparison table covering modern MAS attribution and classical causal debugging.

**Exit criterion:** a one-page protocol that another researcher could use to decide whether an attribution is causally validated.

### Phase 2: Reproduce existing baselines

1. Reproduce or adapt Who&When-style attribution on an accessible trace corpus.
2. Run a whole-trace LLM judge baseline.
3. Confirm that executable outcome oracles work.
4. Measure run-to-run variability before adding interventions.

**Exit criterion:** observational attribution results can be reproduced with recorded versions and confidence intervals.

### Phase 3: Build the trace and checkpoint layer

1. Define the framework-neutral event schema.
2. Instrument agent invocations, messages, memory, tools, and environment transitions.
3. Implement environment checkpoint and restore.
4. Add first-divergence detection.
5. Verify that tracing does not change task behavior materially.

**Exit criterion:** the same execution can be inspected and replayed from selected checkpoints.

### Phase 4: Implement fault operators

1. Begin with six fault operators spanning different layers.
2. Validate activation and outcome effects.
3. Add provenance labels hidden from attribution methods.
4. Introduce negative-control and sham mutations.
5. Create a held-out fault subset.

**Exit criterion:** at least 100 objectively failed executions with known injection conditions and diverse propagation behavior.

### Phase 5: Implement repair interventions

1. Define root repair for each injected fault.
2. Define plausible symptom and propagation-point repairs.
3. Implement frozen, live, and hybrid suffix replay.
4. Repeat interventions and estimate repair probabilities.
5. Validate that unrelated negative-control interventions rarely repair failures.

**Exit criterion:** paired failure-repair records demonstrate that injection location and effective repair site are not always identical.

### Phase 6: Run attribution methods

1. Execute observational baselines.
2. Execute structural trace methods.
3. Execute exhaustive intervention on a manageable subset.
4. Implement adaptive intervention search.
5. Measure localization, causal validity, calibration, cost, and latency.

**Exit criterion:** at least one clear comparison between label accuracy and repair success with uncertainty estimates.

### Phase 7: Add difficult cases

1. Introduce double faults.
2. Add shared-memory and cyclic workflows.
3. Test heterogeneous model teams.
4. Evaluate held-out fault operators.
5. Add naturally occurring failures where feasible.

**Exit criterion:** results do not depend entirely on single, isolated, synthetic errors.

### Phase 8: Analyze and write

1. Freeze the dataset before final analysis.
2. Run the preregistered primary analysis.
3. Perform sensitivity checks and ablations.
4. Write results before discussion.
5. State negative findings and limitations prominently.
6. Prepare the anonymous artifact.

**Exit criterion:** every headline claim maps to an executable result, figure, table, or released artifact.

## Scope control for the October deadline

The full proposal is larger than one month of work unless substantial infrastructure already exists. Use the following priority order.

### Minimum credible regular paper

- Two domains
- Two or three frameworks
- Six fault operators
- Single and double faults
- Four observational baselines
- One structural baseline
- Exhaustive intervention oracle on a subset
- One adaptive intervention method
- Frozen and live replay
- At least 100 failures
- Primary result comparing attribution-label accuracy with repair success

### Minimum credible short paper

- One domain
- Two frameworks
- Three fault operators
- Fifty or more failures
- Whole-trace judge and one attribution baseline
- Repeated causal replay
- Clear evidence that observational blame and repair success diverge
- Released pilot dataset and protocol

Do not submit a broad framework description without a completed causal intervention result. The causal mismatch is the paper.

## Suggested timeline

### Week 1

- Run the one-framework, one-task, one-failure minimal experiment first.
- Compare repairs at the root, propagation point, and symptom.
- Estimate repair probabilities through repeated execution.
- Compare one observational attribution with the intervention ranking.
- Make the scientific go/no-go decision.
- Only after a positive gate, freeze definitions and RQs and design the general trace schema.

### Week 2

- Instrument two frameworks.
- Implement checkpointing.
- Add three high-quality fault operators.
- Generate pilot failures.
- Validate negative controls.

### Week 3

- Implement repair replay.
- Run observational and intervention baselines.
- Add one double-fault class.
- Begin statistical analysis.
- Draft methods and related work.

### Week 4

- Freeze data.
- Complete primary and sensitivity analyses.
- Prepare figures and tables.
- Write results, discussion, and limitations.
- Package artifact.
- Conduct citation and claim audit.
- Format and anonymize submission.

## Recommended figures and tables

1. System diagram showing failure, attribution, intervention, and replay.
2. Example trace separating root cause, propagation point, symptom, and repair site.
3. Scatter plot of observational attribution accuracy versus repair success.
4. Repair probability by fault layer and method.
5. Cost-accuracy Pareto curve for intervention strategies.
6. Rank changes between label-based and causal evaluation.
7. Table comparing modern attribution benchmarks and classical causal-debugging approaches.
8. Table of framework, model, fault, and replay configurations.

## Likely reviewer concerns

### "AID already combines nondeterminism, causal analysis, fault injection, and adaptive interventions."

Response: agree and cite AID as the principal methodological foundation. RepairCheck-MAS is not presented as another claim to invent intervention-based diagnosis. It is a benchmark and evaluation standard that tests whether attribution methods predict effective repairs in agent event graphs. It also studies non-canonical semantic repairs, state-changing tools, and causal structures outside AID's single-root counterfactual model.

### "Repair validation is just delta debugging or causal testing."

Response: those are foundational methods and must be cited. The contribution is a controlled adaptation and empirical study for stochastic multi-agent event graphs, with agent-level interventions, repeated suffix replay, interacting faults, and modern attribution baselines.

### "The injected fault is obviously the cause."

Response: injection establishes a candidate cause, not guaranteed actual causality. Faults can be masked, amplified, or combined with native errors. The benchmark includes negative controls, propagation repairs, interacting faults, and outcome-based intervention tests.

### "Replaying an LLM is not a valid counterfactual."

Response: report frozen, live, and hybrid replay separately. Estimate repair probabilities across repeated executions and explicitly limit claims to controlled interventional effects.

### "An effective repair site is not a root cause."

Response: correct. The benchmark labels and evaluates root causes, propagation points, symptoms, and repair sites separately.

### "Synthetic faults lack realism."

Response: derive operators from MAST and framework issue reports, hold out operators, and include a smaller naturally occurring failure corpus.

### "LLM judges define both labels and evaluation."

Response: primary outcomes use executable environment state and tests. Human and LLM labels are secondary comparisons.

### "The experiment is too expensive."

Response: use blocked sampling, local models for high-volume intervention search, provider models for external validation, and adaptive rather than exhaustive intervention where possible.

### "One pilot failure cannot support a general claim."

Response: the pilot is a scientific gate, not the final evidence. It establishes that attribution-repair disagreement is measurable before infrastructure is generalized. The submitted claims must be limited to the number and diversity of failures, tasks, models, and frameworks actually evaluated.

## Alternative titles

1. **From Blame to Repair: Intervention-Validated Failure Attribution in LLM-Based Multi-Agent Systems**
2. **Did the Blamed Agent Cause the Failure? Counterfactual Repair for Multi-Agent Diagnosis**
3. **RepairCheck-MAS: Evaluating Multi-Agent Failure Attribution Through Controlled Intervention**
4. **Beyond Trace Labels: Causal Evaluation of Failure Attribution in Agentic Systems**
5. **Who Broke It, and Will Fixing Them Help? Repair-Oriented Diagnosis for LLM Agents**

The first title is the most appropriate for a formal workshop submission. The second is memorable but slightly informal.

## Draft abstract

LLM-based multi-agent systems distribute planning, reasoning, memory, verification, and tool use across interacting components. When an execution fails, existing attribution methods attempt to identify a responsible agent and decisive step from its trace. Agreement with an observational label, however, does not establish that the attributed event caused the failure or that changing it will repair the system. We introduce RepairCheck-MAS, an intervention-based framework for evaluating failure attribution in LLM multi-agent systems. RepairCheck-MAS represents executions as versioned event graphs, injects controlled faults across planning, communication, memory, tools, verification, and orchestration, and produces checkpointed failed executions with executable outcome oracles. Candidate attributions are validated through repeated counterfactual replay in which the named agent-step is repaired while environment and downstream variation are controlled using frozen, live, and hybrid replay. The benchmark distinguishes causal roots, propagation points, observable symptoms, and effective repair sites, and includes interacting faults and negative-control interventions. We evaluate trace-based LLM judges, structural localization methods, and intervention-guided diagnosis across multiple agent frameworks and task domains. The primary outcomes are repair success probability, causal effect, localization accuracy, calibration, and diagnostic cost. This work provides a reproducible standard for determining whether multi-agent failure explanations are merely plausible or operationally useful for repair.

## Suggested paper outline

1. Introduction
2. Motivating failure and problem definition
3. Classical causal debugging and modern MAS attribution
4. RepairCheck-MAS benchmark and event model
5. Fault injection and replay protocol
6. Attribution and intervention methods
7. Experimental setup
8. Results
9. Threats to validity
10. Implications for agentic software engineering
11. Conclusion

## Submission checklist

- [ ] Confirm the workshop date discrepancy with organizers.
- [ ] Choose short or regular format based on completed evidence.
- [ ] Follow IEEE two-column formatting.
- [ ] Verify every citation against its primary source.
- [ ] Include classical debugging and causal-inference literature.
- [ ] Freeze root-cause, symptom, propagation, and repair-site definitions.
- [ ] Use executable primary outcome oracles.
- [ ] Include repeated interventions and uncertainty estimates.
- [ ] Include negative-control and sham interventions.
- [ ] Include at least one interacting-fault condition.
- [ ] Compare label accuracy with repair success directly.
- [ ] Report frozen and live replay separately.
- [ ] Include strong modern attribution baselines.
- [ ] Record exact framework, model, prompt, and tool versions.
- [ ] Report task utility, cost, latency, and flakiness.
- [ ] Release an anonymized artifact where policy permits.
- [ ] Scan the manuscript for claims of being the first.
- [ ] Distinguish technical causality from organizational blame.
- [ ] Check page count including references.
- [ ] Complete anonymization before submission.

## Final assessment

### Calibrated acceptance assessment

SE4AgenticAI does not publish a submission count or acceptance rate. Its [2025 public program](https://cs.uwaterloo.ca/~palencar/se4agenticai/2025/) listed three papers, but that number cannot reveal how many papers were submitted or rejected. The following estimates are informed judgments, not historical acceptance statistics.

| State of the submission | Estimated acceptance chance |
|---|---:|
| Position or framework paper without intervention results | 25-40% |
| Short paper with one convincing pilot and careful prior-art framing | 55-65% |
| Short paper with several failures, repeated interventions, and credible baselines | 65-75% |
| Regular paper with multiple tasks or frameworks, strong controls, and a reproducible artifact | 70-80% |
| Infrastructure-heavy paper that does not demonstrate attribution-repair disagreement | 25-35% |

Before experiments, the idea alone is approximately a 40-50% acceptance proposition. The venue fit is about 9/10, idea quality about 8/10, and currently defensible novelty about 7.5/10. The empirical result, not additional conceptual complexity, is what can move the probability upward.

These estimates assume competent execution and clear writing. They can fall sharply if repairs are not semantically comparable, trials are too few, the outcome oracle is subjective, AID is described inaccurately, or the paper claims novelty for intervention-based debugging itself.

### Overall verdict

This proposal is a 9/10 fit for SE4AgenticAI 2026. It converts failure attribution from a label-prediction problem into an executable software-engineering question: does fixing the blamed component actually fix the system?

Its primary strength is a clear falsifiable endpoint. A method can produce persuasive explanations and high agreement with annotators while still failing the repair test. That creates a meaningful empirical result even if the proposed attribution algorithm is simple.

Its main risk is no longer simply that classical prior art exists. That prior art is known and can be incorporated honestly. The larger risk is failing to demonstrate that the proposed evaluation changes any scientific conclusion. Counterfactual debugging, causal testing, fault injection, delta debugging, program slicing, and AID are established foundations. The paper must show that label-based rankings and repair-based rankings diverge, or discover a similarly useful boundary condition.

The cleanest novelty defense is the difference in contribution type:

> AID is a root-cause-discovery method. RepairCheck-MAS is an evaluation standard for determining whether AID-inspired and other attribution methods predict repairs.

The second defense is methodological. Agent repairs often lack one known substitute value, and they can alter downstream meaning or external state. The third defense is broader causal structure, including disjunctive and overdetermined failures. Stochasticity should be presented as an experimental challenge rather than the primary novelty claim.

For the October deadline, the recommended minimum result is:

> On a reproducible set of multi-agent failures, observational attribution rankings differ materially from intervention-measured repair success, and repeated causal replay provides a more reliable target for selecting repair locations.

If that result is supported, the paper has a strong, focused contribution even without a highly complex new attribution model.

### Recommended submission strategy

Prefer a strong short paper over an under-evaluated regular paper. A credible short submission needs a clear phenomenon, repeated interventions, a trustworthy task oracle, at least one strong observational baseline, an AID-aware related-work section, uncertainty estimates, and a small released artifact. Expand to a regular paper only when the evidence covers enough tasks, failures, or frameworks to support comparative claims.

The paper's opening should emphasize three points in this order:

1. Existing attribution benchmarks predominantly reward agreement with observational labels.
2. RepairCheck-MAS evaluates whether an attribution predicts an intervention that improves system success.
3. Agent interventions introduce non-canonical repairs, probabilistic suffixes, semantic divergence, and external-state risks that require a specialized protocol.

## References

1. Weiser, M. Program Slicing. *ICSE*, 1981. https://courses.cs.washington.edu/courses/cse503/11au/readings/weiser-slicing-icse81.pdf
2. Arlat, J. et al. Fault Injection for Dependability Validation: A Methodology and Some Applications. *IEEE Transactions on Software Engineering*, 1990. https://homepages.laas.fr/arlat/documents/89124/89124.pdf
3. Chen, T. Y., Cheung, S. C., and Yiu, S. M. Metamorphic Testing: A New Approach for Generating Next Test Cases, 1998. https://www.cse.ust.hk/faculty/scc/publ/CS98-01-metamorphictesting.pdf
4. Zeller, A. and Hildebrandt, R. Simplifying and Isolating Failure-Inducing Input. *IEEE Transactions on Software Engineering*, 2002. https://www.cs.columbia.edu/~junfeng/08fa-e6998/sched/readings/delta-debug-input.pdf
5. Halpern, J. Y. and Pearl, J. Causes and Explanations: A Structural-Model Approach. Part I: Causes. *British Journal for the Philosophy of Science*, 2005. https://doi.org/10.1093/bjps/axi147
6. Johnson, B., Brun, Y., and Meliou, A. Causal Testing: Finding Defects' Root Causes, 2018/2020. https://arxiv.org/abs/1809.06991
7. Fariha, A., Nath, S., and Meliou, A. Causality-Guided Adaptive Interventional Debugging. *SIGMOD*, 2020. https://arxiv.org/abs/2003.09539
8. Debenedetti, E. et al. AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents. *NeurIPS Datasets and Benchmarks*, 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html
9. Ma, C. et al. AgentBoard: An Analytical Evaluation Board of Multi-Turn LLM Agents. *NeurIPS Datasets and Benchmarks*, 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/877b40688e330a0e2a3fc24084208dfa-Abstract-Datasets_and_Benchmarks_Track.html
10. Xie, T. et al. OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments. *NeurIPS Datasets and Benchmarks*, 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/5d413e48f84dc61244b6be550f1cd8f5-Abstract-Datasets_and_Benchmarks_Track.html
11. Yao, S. et al. tau-bench: A Benchmark for Tool-Agent-User Interaction. *ICLR*, 2025. https://arxiv.org/abs/2406.12045
12. Cemri, M. et al. Why Do Multi-Agent LLM Systems Fail? *NeurIPS Datasets and Benchmarks*, 2025. https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html
13. Zhang, Y. et al. Which Agent Causes Task Failures and When? *ICML*, 2025. https://proceedings.mlr.press/v267/zhang25cq.html
14. Zhu, K. et al. MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents. *ACL*, 2025. https://aclanthology.org/2025.acl-long.421/
15. Deshpande, A. et al. TRAIL: Trace Reasoning and Agentic Issue Localization, 2025. https://arxiv.org/abs/2505.08638
16. Chen, M. et al. Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-Based Multi-Agent Systems. *ACL*, 2026. https://aclanthology.org/2026.acl-long.912/
17. AgentTrace: A Structured Logging Framework for Agent System Observability, 2026. https://arxiv.org/abs/2602.10133
18. SE4AgenticAI 2026 Call for Papers. https://cs.uwaterloo.ca/~palencar/se4agenticai/
