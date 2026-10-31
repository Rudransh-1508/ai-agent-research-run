# From Lint Compliance to Task Reliability: Evaluating Repairs to Agent Skills

Research brief and proposed next-step protocol

Date: 12 September 2026

Status: **Candidate for a bounded feasibility check. Not a validated novelty claim, not a passed pilot, and not authorization to spend API budget.**

## 1. Executive decision

Investigate whether repairing reported quality problems in agent skill packages improves the behavior of agents that consume those packages.

The proposed research question is:

> When developers repair quality warnings in agent skills, which repairs improve task reliability, which merely remove warnings, and which introduce regressions?

The immediate goal is to establish whether this question has a distinct contribution and a runnable, informative experiment. The goal is not to invent another linter, make every skill lint-clean, or demonstrate that our preferred repair method wins.

The intended contribution is an empirical evaluation of a development practice, supported by executable artifacts and controlled comparisons. A novel algorithm is not currently proposed.

Recommended next action: conduct the no-model Gate 0 in Section 9. Only approve a behavioral pilot after that gate passes. Do not start implementing a new evaluation platform.

## 2. Motivation: why this problem matters

Agent skills package natural-language procedures together with optional scripts, references, and assets. Their quality is increasingly checked using structural validators, lint rules, authoring guidelines, and automated revisions.

There are at least three distinct meanings of quality:

1. **Conformance:** the package satisfies a particular specification or host's loading requirements.
2. **Authoring quality:** the package follows recommendations about organization, verbosity, dependencies, and instruction style.
3. **Behavioral utility:** an agent using the package completes the intended task correctly and at acceptable cost.

These properties can support each other, but they are not interchangeable. A successful lint repair establishes that a detector no longer fires. It does not by itself establish better task execution.

The agent-specific mechanism is that the edited artifact is also an instruction source. Moving an example into a reference, removing setup guidance, or rewriting a procedural constraint can change what the agent reads, infers, and does. An edit intended as packaging cleanup can therefore change operational behavior without changing any executable script.

This motivates a concrete engineering decision:

> Which repair recommendations should developers apply automatically, and which require task-level validation or context-sensitive review?

The study must not attack the strawman that linters promise complete correctness. Static checks can be useful without guaranteeing success. The question is whether particular recommended repairs deliver their intended benefit and what regressions or costs accompany them.

## 3. What the existing evidence supports

The initial search was seeded by the [ai-agent-papers repository](https://github.com/masamasa59/ai-agent-papers). Six lists were screened: skills, harnesses, evaluation, AgentOps, human-agent interaction, and governance. Relevant primary-paper sections were then inspected, with additional searches outside the repository.

This was a targeted review, not an exhaustive systematic literature review or an artifact reproduction. No skill-repair experiments have been run for this proposal.

The strongest motivating source is [What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files](https://arxiv.org/html/2608.08453v1). It studies static quality findings, routing metadata, and repair. Its 200-skill repair experiment measures removal of detected defects; its routing experiment uses BM25. Sections 4.3 and 6 explicitly leave end-to-end evaluation of most non-routing categories outside scope. The authors identify further behavioral evaluation as intended follow-up work.

That is a specific missing connection between a measured repair outcome and an engineering outcome, but it is also a warning about competing work. A future-work statement is not ownership of a topic, nor proof that nobody else has completed it.

Separately, the [official Agent Skills specification](https://agentskills.io/specification) permits environment requirements through `compatibility`, and distinguishes unrestricted Markdown body content from recommended organization. Consequently, a platform-specific instruction is not automatically a fault in a platform-specific skill. Historical specification versions and host-specific rules must be checked before declaring a published rule incorrect.

## 4. Proposed gap and its limits

### Defensible working gap

Existing work provides static skill-quality checks, skill-failure analyses, compression methods, and execution-guided revision methods. The material inspected does not establish the behavioral value of a fixed set of lint-directed repairs, compared against unchanged skills and equally budgeted generic revisions, on independently evaluated tasks.

This statement is deliberately about the comparison inspected, not a claim that skill testing or repair is unexplored.

### What is already covered

- Skills can improve or harm task outcomes.
- Skill text can create unnecessary work or displace useful reasoning.
- Skill compression can preserve or improve task performance.
- Execution traces can guide useful skill revisions.
- Linting and behavioral testing can coexist in a development workflow.

None of these should be presented as our discovery.

### What would make the contribution substantive

The paper should establish a relationship between a specified repair practice and an actionable outcome, for example:

- A frequently recommended repair category removes warnings but reproducibly harms task behavior under identifiable conditions.
- Another category improves behavior beyond a comparable generic rewrite, supporting a concrete maintenance recommendation.
- The same warning has different consequences inside versus outside a skill's declared operating assumptions.
- Behavioral improvements are attributable to particular repaired instructions or resource access changes, rather than just shorter prompts.

These are possible findings, not claims about observed results. Do not select the final hypothesis after seeing which one produces a favorable significance test.

## 5. Relevant reading and exact comparisons

Read these in the following order. The read-depth descriptions record the preceding review, not a claim that every appendix or implementation was audited.

### P1. Official Agent Skills specification

Link: [Specification](https://agentskills.io/specification).

Read first to distinguish required syntax, recommended authoring practices, environment declarations, and host-dependent behavior. Pin the applicable version before classifying findings. Do not promote every guideline into a mandatory conformance rule.

Review so far: relevant field definitions, body-content guidance, resource organization, and validation descriptions inspected.

### P2. What Keeps Agent Skills from Being Reusable?

Link: [arXiv:2608.08453v1](https://arxiv.org/html/2608.08453v1).

Read the taxonomy, detector validation, routing experiment, authoring guidelines, repair procedure, and limitations. Distinguish measured detector outcomes from downstream task outcomes. Its [SkillMD-138K dataset](https://huggingface.co/datasets/FayeZC/SkillMD-138K) is a discovery source, not automatically a runnable package corpus: a skill file alone may omit required supporting resources.

Our difference would be controlled behavioral evaluation of specified repairs. Our paper cannot simply repeat its prevalence analysis or warning-removal experiment.

Review so far: relevant methodology, results, repair discussion, and limitations inspected. Dataset and scripts not executed.

### P3. Agent Skills Can Be Harmful

Link: [arXiv:2608.11888v1](https://arxiv.org/html/2608.11888v1).

This is direct prior art for paired skill-failure analysis. It compares skill-guided runs with no-skill or matched-skill references and studies functional and efficiency failures. Environment mismatch, implementation faults, artifact placement, and excessive procedure are useful interpretation categories.

Our difference must be the intervention under evaluation: repairing a specified warning using a frozen procedure. We should reuse relevant failure categories rather than claim a new taxonomy unless evidence genuinely requires one.

Review so far: methodology descriptions, failure categories, attribution approach, and research-direction sections inspected. No reproduction of its dataset or attribution tool.

### P4. SkillReducer: Optimizing LLM Agent Skills for Token Efficiency

Link: [arXiv:2603.29919v1](https://arxiv.org/html/2603.29919v1).

This already restructures and compresses skills, uses progressive disclosure, and evaluates functional retention. It compares with direct compression and other compression baselines. It also identifies failures where examples carry behaviorally important information.

This is the main threat to a proposal that becomes only body cleanup, shorter instructions, or moving examples into references. If those edits dominate our corpus, either include a faithful SkillReducer comparison and establish a distinct question, or stop the proposal as insufficiently differentiated.

Review so far: method overview, baseline comparisons, functional evaluation, ablations, and transfer sections inspected. Implementation not executed.

### P5. SkillRevise: Improving LLM-Authored Agent Skills via Trace-Conditioned Skill Revision

Link: [arXiv:2606.01139v3](https://arxiv.org/html/2606.01139v3).

This already uses execution evidence, diagnosis, repair principles, and repeated verification to revise skills. Its evaluation includes bounded revision conditions, and selected outcomes must be understood in terms of that evaluation budget.

Our primary question concerns repair from static warnings without execution feedback. If comparing against SkillRevise, account for its additional information, execution attempts, and revision cost. Evaluate retained artifacts on fresh runs or held-out instances; do not compare our one-shot outcome with another method's best observed attempt as though their budgets were identical.

Review so far: relevant methodology, evaluation conditions, and selection semantics inspected. Code not executed. Prefer this primary paper over third-party repositories explaining or vendoring it.

### P6. The Regression Tax: Decomposing Why Skills Help and Hurt LLM Agents

Link: [arXiv:2607.22520v1](https://arxiv.org/html/2607.22520v1).

This motivates reporting gains and regressions separately rather than only a net average. It also studies influence from descriptions even without skill-body retrieval.

Our difference is repair-specific evidence. Merely showing that adding a skill changes performance would be duplicative. Its description effects are also a reason to hold the skill catalog fixed when studying body repairs.

Review so far: experimental setup, comparison design, mechanism descriptions, and relevant related work inspected. No independent reproduction.

### P7. SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks

Links: [Paper](https://arxiv.org/html/2602.12670v1), [repository](https://github.com/benchflow-ai/skillsbench).

Use as a candidate source of skill-task pairs, environments, and executable verifiers. Verify the exact repository revision, task requirements, dependencies, and grader behavior before adopting tasks. Do not assume every task is suitable, cheap, or informative for this experiment.

Review so far: benchmark descriptions and public repository documentation inspected. No environments launched; no suitable subset established.

### Practical tools to inspect, not reimplement automatically

- [agnix](https://github.com/agent-sh/agnix): candidate source of existing diagnostics. Its rules must be distinguished from the research taxonomy above.
- [skilllint](https://github.com/bueti/skilllint): candidate mechanical-fix comparator, subject to source inspection and version pinning.
- [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref): reference structural validation, not an end-to-end task oracle.

Tool documentation was discovered or inspected during the search; their behavior has not been audited locally. Do not claim that a published research detector and these implementations implement the same rules.

## 6. Why this might work, and why it might not

### Reasons to investigate

- There is an explicit, source-backed distinction between warning removal and demonstrated behavioral improvement.
- Existing benchmarks may provide complete tasks and independent verifiers, reducing dependence on finding rare historical incidents.
- Repairs can be frozen before task outcomes, allowing a controlled intervention instead of correlating unrelated good and bad skills.
- Both useful improvements and reproducible harms can inform a real development decision.
- A team of three or four can separate corpus selection, repair preparation, and outcome adjudication.

### Reasons to be cautious

- A seemingly distinct study can collapse into an existing compression or skill-revision experiment.
- Benchmark skills may have too few meaningful natural warnings. Large file corpora may lack matching executable tasks.
- Many warnings may concern readability or maintainability, not runtime reliability. No runtime benefit does not prove such a rule is useless.
- Modern agents may compensate for changes, producing small effects that require more independent tasks than the deadline permits.
- Automated repairs may change several things at once, preventing attribution to the targeted rule.
- Existing authors are actively pursuing neighboring questions.

Therefore, no positive pilot probability or acceptance probability is justified at this stage.

## 7. Goal, research questions, and non-goals

### Research goal

Estimate the behavioral consequences of a predeclared repair procedure for a small, justified set of agent-skill quality warnings, and determine whether the findings support actionable development guidance.

### Primary questions

- **RQ1:** Do lint-directed repairs change independently measured task success and execution cost relative to the original skill?
- **RQ2:** Do targeted warnings add value beyond a comparable generic revision procedure?
- **RQ3:** Which observed changes can be explained by the repaired instructions, resource access, or environment assumptions?

Warning reduction is a manipulation check and secondary outcome, not the definition of success.

### Non-goals

- A universal skill-quality score.
- A new linter, marketplace, agent framework, or repair platform.
- Proving lint-clean skills are safe.
- Proving all static checks are inadequate.
- Measuring ecosystem-wide defect prevalence from a small benchmark sample.
- Demonstrating a novel repair algorithm.
- Reopening the effect-grouping pilot or relabelling its failure as a pass.

## 8. Experimental design

### Unit of study

A case consists of a complete, pinned skill package; its intended environment; a natural warning; a frozen repair; and independently specified task instances.

Count skill packages, repositories, task families, task instances, models, and repeated runs separately. Hundreds of repeated calls are not hundreds of independent skills.

### Recommended initial scope

Start with non-security, execution-facing authoring or compatibility warnings in skills that already have runnable tasks. Hold routing metadata, skill selection, and unrelated catalog entries fixed, and explicitly activate the same intended skill in each skill-enabled arm.

This isolates post-activation behavior. It does not test routing quality. If routing is later studied, use a separately specified discovery experiment with competing skills and negative queries.

Do not weaken safeguards, remove licensing material, or execute suspicious public code just to eliminate a warning. Review package code before execution and use isolated, disposable environments without personal credentials.

### Comparison arms

| Arm | Artifact used | Purpose |
| --- | --- | --- |
| O: Original | Unmodified skill and supporting files | Behavioral reference |
| L: Lint-directed | Skill revised using fixed targeted warnings and repair guidance | Intervention of interest |
| G: Generic revision | Same original revised with general quality guidance, without the targeted diagnostic list | Controls for the value of simply revising the artifact |
| N: No skill | Same task environment without skill guidance or skill-specific injected procedures | Measures whether the skill provides useful guidance at all |

Use the same editing model and a fixed one-candidate revision budget for L and G in the initial screen. Neither sees task outcomes, hidden tests, evaluation traces, or final test answers. Both receive the same permitted package and environment information. Additional validation or regeneration attempts must be explicitly budgeted and logged.

Inspect whether L and G actually produce different edits. If generic revision independently makes the same repair, that limits what the comparison can identify; it is not a reason to alter G after observing results.

If a task requires skill-bundled scripts or assets to be solvable, define the N condition carefully. Do not remove an essential capability and present its resulting failure as proof that natural-language guidance helps. Report such capability differences or restrict the matched no-guidance analysis to cases where tools and task resources remain equivalent.

### Repair preparation

1. Record the detector version, rule identifier, severity, source clause, and rationale.
2. Classify the warning as mandatory conformance, advisory practice, or environment-dependent concern.
3. Produce L and G before running evaluation episodes.
4. Preserve all artifacts and record exact diffs, including scripts and references.
5. Have a second team member check repair scope without seeing behavioral outcomes.
6. Record failed, incomplete, or out-of-scope repairs. Do not silently exclude them from claims about the repair workflow.

Distinguish the effect of attempting a repair from the effect among repairs that actually remove the warning. The latter is a selected subset and must not replace the primary workflow result.

### Task and outcome controls

- Preserve the original user requirement, tool capabilities, execution limits, and environment across arms.
- Use fresh workspace state and context for every episode.
- Keep evaluation tests inaccessible to both repair and execution agents when they contain hidden answers.
- Write or adopt oracles before seeing arm outcomes. Check that a valid reference artifact passes and relevant invalid artifacts fail.
- Record task success, unresolved warnings, model requests, input/output/cache tokens, tool calls, elapsed time, and environment failures.
- Charge reference loading and extra execution steps to the arm that incurs them.
- Report task failures in denominators. Distinguish infrastructure failures and apply a frozen retry/exclusion rule.
- Randomize or interleave arm order to reduce provider/time effects.
- If outcome adjudication needs humans, conceal the arm identity where practical.

### Analysis

Primary contrasts are L minus O and L minus G in task success. Report end-to-end costs separately, including the cost of preparing the revised artifact and assumptions about reuse frequency.

Separate improved, worsened, and unchanged outcomes, but do not claim a skill caused a failure based on one discordant pair. Use repeated runs and task/skill-cluster-aware uncertainty. When multiple task instances share a skill, resampling individual episodes alone will overstate independent evidence.

For mechanism analysis, inspect traces and artifact differences. Use controlled follow-up ablations only after marking them exploratory, then confirm important explanations on fresh instances. Preserve the original experiment unchanged.

Do not infer equivalence from a non-significant difference. A negligible-effect claim requires a predeclared practical margin and sufficiently narrow uncertainty. Pilot data should inform attainable precision, not justify an arbitrary final sample count.

## 9. Gate 0: the next concrete action

Timebox: one to two working days. No model episodes required. Do not let this become an open-ended corpus-building project.

### Work to do

- [ ] Recheck the closest papers for newer versions, released comparisons, or artifacts that answer the same question.
- [ ] Inspect the published detector definitions and candidate linter implementations. Record which rules actually overlap.
- [ ] Map a small set of promising rules to pinned specification or authoring sources. Separate recommendations from requirements.
- [ ] Find complete original packages with natural warnings and existing task requirements. Do not inject arbitrary defects to make the primary corpus work.
- [ ] Demonstrate that candidate environments build and reset without production accounts or personal secrets.
- [ ] Exercise existing reference solutions or representative tool operations and test the oracles without an LLM.
- [ ] Establish a sampling frame and document every inclusion/exclusion before model outcomes.
- [ ] Determine whether the necessary baselines are feasible and whether the proposed comparison goes beyond compression alone.
- [ ] Write a pilot manifest, explicit spending ceiling, and predeclared decision rules for approval.

### Suggested feasibility target

Aim for approximately eight independent skill packages with two suitable task instances each, from more than one source. This is a practical planning target, not statistical justification. Preserve each skill's declared operating scope. If new task instances are required, have two team members validate their requirements and oracles before running agents.

### Pass condition

Gate 0 passes only if there is a distinct question, a bounded runnable corpus, meaningful natural repairs, independent evaluation, and feasible comparisons.

### Stop conditions

- The exact comparison is already adequately answered by existing work.
- The candidate corpus consists mainly of cosmetic changes whose intended benefit is not behavioral.
- Available changes reduce to an already-studied compression method without a distinct engineering question.
- Packages cannot be reconstructed or evaluated without extensive new infrastructure.
- Task matching or warning selection requires choosing cases based on observed failures.
- The proposed revisions cannot be scoped or compared fairly.

If the gate fails, record the reason and stop. Do not repeatedly add qualifiers to keep the idea alive.

## 10. Proposed behavioral pilot, only after approval

An illustrative matrix is:

> 8 skills x 2 task instances x 4 arms x 2 models x 2 repetitions = 256 execution episodes.

This excludes revision-model calls, any necessary calibration calls, and infrastructure retries. Final count and dollar cap must be approved after measuring or estimating realistic per-episode cost. Do not infer cost from the previous AgentDojo pilot: these environments may have very different runtimes.

Two repetitions are a screening budget, not enough to make precise per-skill reliability claims. Use separately designated calibration cases to debug the runner and estimate cost; do not quietly fold outcomes used to tune the protocol into confirmatory evidence.

### What a pilot pass would mean

A pass would mean that the study is feasible, identifies the intended repair contrast, and has a credible route to an informative main result. It would not mean that all repairs help or that publication is assured.

Three outcome paths could justify further work:

1. **Benefit:** targeted repairs show a practically interesting advantage that is not explained by generic rewriting, changed capabilities, or cost omissions.
2. **Harm or conditional benefit:** reproducible differences identify a nontrivial repair risk or a meaningful operating condition, with a plausible mechanism worth confirming independently.
3. **Potentially informative negligible effect:** the study can realistically obtain enough independent evidence to bound an effect relevant to the selected rules' stated purpose. A small, noisy pilot null is not enough.

Predeclare how these paths will be assessed before executing the matrix. Do not require every model to show the same numerical effect, but do not generalize a single-model artifact to agents as a whole.

### Pilot stop conditions

- Warning removal is the only demonstrated change and the task experiment cannot resolve a useful effect at feasible scale.
- The apparent effect disappears under fair capability, revision-budget, or state-reset controls.
- Findings are dominated by one broken package, unrelated oracle errors, or a task-selection artifact.
- Nearly all tasks are at floor or ceiling and there is no prejustified independent test population.
- L and G are operationally indistinguishable, so the diagnostic contribution cannot be identified.
- The contribution becomes only "static lint does not guarantee correctness."

## 11. Main-study deliverables if the pilot warrants continuation

1. A rule-to-source table distinguishing mandatory, advisory, and environment-dependent checks.
2. A versioned corpus of complete packages, natural findings, original/repaired artifacts, and task requirements.
3. Frozen editing and execution protocols with honest cost accounting.
4. Raw trajectories and oracle results, with secrets excluded and redistribution rights checked.
5. Cluster-aware effect estimates and clearly separated exploratory analyses.
6. A small set of independently confirmed repair mechanisms or recommendations.
7. A reproducibility package using existing benchmark infrastructure wherever possible.

Use new task instances or reserved independent packages to confirm hypotheses generated by the pilot. Repeating the same selected failures more often does not establish broader generality.

Choose main-study size based on the smallest useful effect and observed clustering/variance. No exact sample size is justified before feasibility and pilot evidence exist.

## 12. Why SE4AgenticAI is a plausible venue

The [official workshop CFP](https://cs.uwaterloo.ca/~palencar/se4agenticai/) includes development processes, agent architecture, reproducibility, testing, verification, evaluation, and empirical studies. Skill packages are maintained agent-system artifacts, so their repair and validation fit that engineering focus.

As checked on 12 September 2026, the submission deadline is 10 October 2026. Short papers are 3-4 pages and regular papers 8-10 pages, including references, in IEEE two-column format. Recheck these details before submission.

A realistic initial target is a short empirical paper with one clear question, a controlled experiment, and bounded implications. A regular paper would require broader evidence than the proposed pilot.

Potential paper structure:

1. Motivation and the distinction between detected quality and operational quality.
2. Closest work and the precise unanswered comparison.
3. Corpus, repair protocol, controls, and evaluation.
4. Results and mechanisms.
5. Threats to validity and practical guidance.

Do not claim that the workshop guarantees acceptance of negative results. Topic fit is necessary but insufficient. There is no defensible numerical acceptance estimate for this proposal. A passed pilot would support investment in a submission, not predict its acceptance rate.

## 13. Team allocation and bounded schedule

| Responsibility | Primary work | Independence safeguard |
| --- | --- | --- |
| Literature/rule lead | Prior-art updates, source clauses, detector mapping | Does not choose rules based on agent outcomes |
| Corpus/evaluation lead | Packages, environments, tasks, oracle checks | Freezes tasks before inspecting repairs' behavioral results |
| Repair/execution lead | Frozen revisions, manifests, isolated runs | Has no access to hidden expected answers during revision |
| Analysis/reviewer lead | Outcome analysis, trace review, adversarial checks | Reviews exclusions and claims independently |

For a three-person team, combine literature and analysis duties but retain second-person checks of oracles and repair scope.

Suggested decision schedule, not a promise of completion:

- Days 1-2: no-model Gate 0, with an explicit go/no-go record.
- Days 3-5: approved bounded pilot and independent adjudication.
- Following week: only if justified, freeze and execute the main protocol on independent evidence.
- Remaining time before the deadline: analysis, writing, artifact verification, and internal review.

If the main study cannot be completed and checked rigorously, reduce the claims and paper scope rather than omit necessary controls.

## 14. Final recommendation

Proceed with Gate 0 for **behavioral validation of agent-skill repair recommendations**.

The central opportunity is an unestablished connection between a development-quality signal and its operational consequences. The central risk is that the question becomes either an already-studied compression experiment or the trivial observation that linting is not testing.

Success is not "our repairs win." Success is obtaining trustworthy, useful evidence about which repairs developers should make, under what conditions, and with what validation. If that evidence cannot be obtained within the bounded protocol, stop the candidate honestly.
