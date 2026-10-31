# Testing the Deployment Boundary of Agent Frameworks

## Research decision, gap assessment, access-first pilot, and submission strategy

**Prepared:** 10 September 2026.  
**Target:** SE4AgenticAI 2026.  
**Team:** 3-4 researchers, modest compute and API budget.  
**Primary objective:** Produce a valid, well-supported workshop submission, prioritizing research defensibility and completion over inventing a new algorithm.

**Status: proposal, not experimental results.** No serving environment has been started for this study, no access gate has passed, and no reported defect has been reproduced by our team. No paid inference or cloud deployment was performed while preparing this report. Every sample size, timeline, and decision threshold below is a proposed research-management choice, not a workshop acceptance requirement.

This document consolidates the current recommendation and replaces the older pilot ordering: serving access and execution-path qualification now happen at hour zero, inside the 72-hour budget. It does not overwrite the historical reviews.

## 1. Executive decision

**Choose deployment-boundary testing as the preferred acceptance-oriented research investment, conditional on an immediate access gate and a substantive pilot.** Keep the MCP adapter study as the single fallback if serving access is not tractable. Neither project is already a validated paper.

Recommended neutral working title:

> Testing the Deployment Boundary of Agent Frameworks: A Paired Study of Application-Property Transfer

An outcome-led title, such as *From Local Pass to Served Failure*, should only be used after results justify it. We must not select cases merely to produce that headline.

The question is:

> When an agent application satisfies a specified property through its embedded SDK, does that property still hold through an official serving entrypoint, and which additional tests provide useful assurance?

The intended contribution is a controlled empirical study and evaluated testing guidance. It is not a survey, a new orchestration framework, or a claim to have invented integration testing.

Why this is the current choice:

- There are concrete public motivating reports, rather than only hypothetical failure scenarios.
- The experiment can use externally checkable application properties rather than subjective answer-quality scores.
- A useful result can identify which testing configurations detect particular boundary failures and their cost.
- The scope aligns directly with the workshop.
- Unlike reference slicing, it does not first require proving that a new algorithm is necessary and then making that algorithm work.

The major unresolved risks are access, faithful reproduction, overlap with prior testing work, and whether the resulting lesson is more substantial than a collection of known bugs.

## 2. What the study actually compares

### 2.1 Embedded execution versus served execution

**Embedded execution:** application code directly invokes the framework's agent or workflow object in process, as a developer might do in an SDK test.

**Served execution:** a separate client invokes the application through an official framework serving route. That route performs its normal request handling, context construction, dispatch, serialization, and state integration.

These are execution modes, not geographical locations. Both can run on one machine. A locally running official server still crosses a genuine network and framework entrypoint boundary.

Three environments must remain distinct:

1. Embedded SDK execution.
2. Official self-hosted or development-server execution, with the exact mode named.
3. Managed cloud execution, including platform-provided identity, storage, routing, or lifecycle behavior.

Evidence from environment 2 is not automatically evidence about environment 3. A manually written HTTP wrapper around an SDK call is not a substitute for the official serving integration under study.

### 2.2 Compare properties, not identical transcripts

The same valid request can produce different natural-language wording while satisfying the same requirement. Consequently, byte-identical output is not the primary oracle.

Candidate properties, each requiring a documented or independently justified application contract, include:

| Property family | Illustrative observable requirement | Evidence to inspect |
|---|---|---|
| Request context | A tool receives the intended caller-specific context after server dispatch | Synthetic identity marker and tool-side record |
| Approval behavior | An action requiring approval does not execute before approval, and executes under the intended context afterward | Approval events and isolated side-effect ledger |
| State continuity | A subsequent request sees the state that the contract says should persist | Backend snapshots and follow-up observations |
| Error propagation | A failed tool operation is not exposed as successful completion | Tool outcome and terminal response |
| Streaming behavior | The promised events and terminal status reach the external client | Captured stream and terminal event |
| Observability metadata | Contractually exposed accounting or trace fields survive conversion | Native result and public response fields |

These are candidate families, not claims that every framework supports every property. An unsupported capability is an exclusion or a documented capability difference, not a bug.

Keep task/state/approval consequences separate from metadata-only differences. Missing usage information does not, by itself, establish an incorrect bill or a failed user task.

## 3. Why this could be a research gap

### 3.1 The established knowledge

Integration boundaries can introduce defects. Agent frameworks need unit, integration, and end-to-end tests. Deterministic model doubles, traces, and assertions are established techniques. Persistence and resume semantics have already received specialized cross-framework investigation.

We must acknowledge all of this. A new name for these principles is not a contribution.

### 3.2 The residual empirical question

The proposed gap is not whether deployment can fail. It is the absence, in the work located by our review, of the particular body of evidence needed to answer this decision:

> For supported agent applications, which locally verified properties transfer across official serving paths under matched configurations, and how much additional defect detection does a focused public-entrypoint test selection provide relative to local tests and fuller end-to-end tests?

This is a **candidate empirical gap**, not a certified absence from all literature. The closest-work comparisons below explain the current boundary. A newly located paper or already comprehensive upstream test suite could reduce the remaining contribution.

### 3.3 Why an empirical gap is still original research

A contribution can consist of new controlled evidence about an important engineering decision. It need not introduce a new algorithm. The original work would be:

1. Constructing an auditable, reproducible sample of relevant workflows and defects.
2. Executing paired comparisons with explicit contracts and causal controls.
3. Separating mechanisms and consequences rather than pooling every output difference.
4. Deriving a bounded testing recommendation and evaluating it on held-out cases.
5. Releasing enough artifacts for independent verification.

Conversely, reproducing a handful of already described defects and concluding that developers should run integration tests would be insufficient.

### 3.4 Why the agentic setting matters

The application properties concern agent-specific interactions: tool effects, approval continuation, conversation state, caller-specific tool context, and streamed agent execution. Model randomness can also hide framework behavior, requiring careful separation of orchestration from model decisions.

These considerations motivate the study, but do not prove that the underlying software faults are unique to agents. The manuscript should claim useful evidence for agent engineering, not a new universal class of distributed-system failure.

## 4. Authentic motivating evidence and its limits

The following are sampling leads. None is a completed result of this study.

| Source | What it supports | What remains unestablished |
|---|---|---|
| [LangGraph issue #8653](https://github.com/langchain-ai/langgraph/issues/8653) | The reporter describes a distinction between attached and configuration-injected checkpointers, with incorrect state reads in a platform-shaped graph and a claimed platform data-loss consequence. | The supplied in-memory example is not a full served, durable reproduction. `langgraph dev` success would not establish access to the implicated production-shaped path. |
| [Microsoft Agent Framework issue #7416](https://github.com/microsoft/agent-framework/issues/7416) | The report locates usage omission in the Python Foundry hosting response conversion path despite usage existing in the native response. | A different self-hosting package or a .NET endpoint is not automatically a reproduction. This is initially a metadata case, not evidence of user-task failure. |
| [Azure SDK issue #46696](https://github.com/Azure/azure-sdk-for-python/issues/46696) | A customer reports MCP on-behalf-of token exchange failing under Foundry deployment. | Correct configuration, causal attribution, and actual managed-service access must be established. A locally fabricated identity context cannot validate this cloud-specific claim. |
| [Mastra PR #20741](https://github.com/mastra-ai/mastra/pull/20741), with [follow-up #20748](https://github.com/mastra-ai/mastra/pull/20748) | Our earlier review recorded caller-context preservation work and a follow-up concerning tests bypassing public wiring. This is a particularly relevant lead for testing practice. | The follow-up could not be fetched again during this report's refresh. Its detailed interpretation is carried from the earlier review and must be rechecked against the actual source and tests before relying on it in the manuscript. Neither a merged fix nor a direct-method test proves an HTTP-path reproduction. |

Historical fixes can support a regression-testing study. They must be labelled historical and evaluated at pinned defective and corrected revisions. Do not present them as newly discovered or necessarily present in current releases.

Several issue variants from one mechanism do not constitute independent replication. Similarly, the Azure SDK and Agent Framework reports may share infrastructure and must not be counted as two independent framework ecosystems without justification.

## 5. Closest prior work and what we must add

This section carries forward the method-focused comparisons in the [fresh-gap review](FRESH_GAP_SEARCH_2026-09-09.md). Primary records for the first four works were refreshed for this document; this was not a new full-text review of every paper.

| Prior work | Already covered | Required distinction for this study |
|---|---|---|
| [The OpenHands Software Agent SDK, v2](https://arxiv.org/html/2511.03690v2) | Local/remote portability, integrated services, production reliability evaluation, and layered testing. The current record identifies MLSys 2026 acceptance. | A paired, cross-framework application-property study and independently evaluated test-selection result, not another demonstration that remote agents need testing. |
| [Automated structural testing of LLM-based agents](https://arxiv.org/html/2601.18827v1) | Trace-based structural testing, deterministic LLM mocking, assertions, and a testing pyramid that includes deployed acceptance testing. The record identifies a Big Data 2025 main-track paper. | Evidence about where local verification fails to transfer and which additional configurations are useful. We must not claim mocks or deployed tests as new. |
| [LogicHunter](https://arxiv.org/html/2607.06195v1) | Specification-aware framework testing, authentic usage patterns, behavioral probes, and an investigative oracle for semantic bugs. | Study the relationship between supported execution modes and test coverage, rather than introduce another generic framework fuzzer or count API bugs. |
| [Resume Means Resume](https://arxiv.org/abs/2608.03836) | A persistence conformance contract, deterministic testing, and cross-process/cross-host failure analysis. | The central evidence must extend beyond persistence and resume semantics. Rehosting existing persistence probes does not suffice. |
| [Where Agent Frameworks Fall Short, v4](https://arxiv.org/html/2602.21806v4) | Earlier review identifies substantial framework-bug analysis. | Avoid a generic bug taxonomy with new framework names. |
| [Dissecting Bug Triggers and Failure Modes](https://arxiv.org/html/2604.08906v1) | Earlier review identifies fixed-bug analysis, triggering configurations, tests, and cross-framework transfer. | Establish the specific local-to-served contrast and a testing decision that this work does not already answer. |

Version note: the earlier persistence comparison used v1 of *Resume Means Resume*. Its current record lists v3 and describes the latest revision as presentational, with unchanged results. Exact methods and ancillary material should nevertheless be pinned during study preparation.

The novelty sentence should be modest: "We investigate application-property transfer across official serving paths and evaluate the incremental coverage of boundary-focused tests." Avoid "the first study" unless a renewed search at submission time warrants it.

## 6. Why doing this is worthwhile

The intended beneficiary is a developer deciding whether an existing agent test suite supplies enough evidence for a deployment or serving-integration change.

A successful study could distinguish tests that exercise only internal behavior from tests that also exercise request construction, context propagation, dispatch, and externally visible results. Its useful output is a concrete, measured choice among testing configurations, including their misses and costs.

It may also give framework maintainers reproducible regression cases and show whether existing tests traverse the relevant public wiring. Developer confirmation would strengthen interpretation but is not a prerequisite we should depend on under the deadline.

The research should remain useful without needing dramatic failure prevalence. A bounded result about a recurring mechanism can matter. But a small purposive sample cannot establish how often failures occur across the ecosystem.

## 7. Why SE4AgenticAI is a suitable venue

The current call explicitly includes testing and validation, evaluation approaches, reproducibility, observability, dynamic execution, and empirical studies of agent frameworks. This study addresses the engineering of agent systems themselves, rather than merely applying an LLM to an unrelated task. [Official 2026 call](https://cs.uwaterloo.ca/~palencar/se4agenticai/)

The [2025 program](https://cs.uwaterloo.ca/~palencar/se4agenticai/2025/) contains an empirical multi-agent development study, a NoSQL multi-agent framework paper, and an accountability architectural-tactic paper. This supports the suitability of empirical and constructive engineering contributions; it does not establish that an algorithm is required.

Our inference is that a rigorous, well-scoped engineering study is a plausible contribution form. We do not know the submission denominator, rejection reasons, reviewer scores, or how the next program will be selected. Three program entries are not an acceptance-rate estimate.

The [past-papers report](PAST_PAPERS_AND_SUBMISSION_STRATEGY_2026-09-09.md) contains the fuller precedent analysis and its access limitations. In particular, the NoSQL paper's methods were not available for our full-text inspection; its program listing must not be used to infer experimental standards.

## 8. Serving access: the first hard gate

### 8.1 What the current documentation permits us to infer

| Framework | Candidate official path | Qualification required |
|---|---|---|
| LangGraph | `langgraph dev` or the Docker-based `langgraph up`, as appropriate to the mechanism. Documentation distinguishes lightweight local storage from a PostgreSQL-backed stack. | Check installed runtime, Docker if needed, account/key requirements, and any feature-specific licensing. Prove that the implicated state or context path is exercised; a working development endpoint is insufficient for a production-only mechanism. |
| Microsoft Agent Framework | The exact hosting integration implicated by the case, with self-hosting where faithful. | Do not substitute an unrelated protocol package merely because it launches. For Foundry-specific identity or service behavior, actual managed access is needed. |
| Mastra | An official server entrypoint, with the built server where the relevant deployment behavior requires it. | Pin the supported commands and packages, execute the relevant public route, and inspect subscription/approval wiring where applicable. Managed-platform behavior remains a separate condition. |

Sources: [LangGraph local development and testing](https://docs.langchain.com/langsmith/local-dev-testing), [Microsoft hosting models](https://learn.microsoft.com/en-us/agent-framework/hosting/), [Foundry hosting prerequisites and local/managed distinctions](https://learn.microsoft.com/en-us/agent-framework/hosting/foundry-hosted-agent), [Mastra's server description and build/start route](https://mastra.ai/blog/announcing-mastra-platform).

LangGraph's guide already recommends production-like validation and states that its development server shares integration tests with production. This is counterevidence to a broad claim that deployment testing is absent. Our contribution must investigate what those tests actually cover, not ignore them.

An older Mastra client-documentation URL used in the discussion now redirects to a missing page. The author-published server description above is the refreshed supporting source. Actual version-specific setup still has to be verified by execution.

**All three access statuses are currently NOT TESTED.** Documentation availability is not access confirmation. A nominally free service may still need account setup, permissions, a model credential, or a feature entitlement.

### 8.2 Hours 0-6: required evidence

Assign the three candidate frameworks to available team members concurrently. This is a proposed human work allocation, not an instruction to launch automated agents or purchase infrastructure.

For each framework, retain:

1. Exact package versions, revision identifiers, runtime versions, and server mode.
2. The account/credential/permission requirements, recording presence without copying secrets.
3. Successful server startup and a request from a separate client through the real network endpoint.
4. One task-relevant feature round trip beyond hello-world.
5. Evidence that the route reaches the component implicated by the candidate case.
6. Reproduction commands, sanitized logs, startup time, and any unresolved limitation.

A relevant feature round trip could demonstrate context reaching an isolated tool, a follow-up request reading session state, or an approval continuation through the public route. Its purpose here is access qualification, not declaring a defect reproduced.

### 8.3 Access decision rules

- Immediately exclude a case when it depends on an unavailable external approval, account, subscription, or license. Do not wait for that dependency inside the pilot.
- Another already identified, faithfully accessible case in the same framework can qualify; record the exclusion instead of silently replacing it.
- At hour six, proceed only if at least two frameworks have relevant working paths. Three frameworks are desirable, not mandatory.
- If fewer than two qualify, stop this cross-framework pilot and move to the MCP study's own feasibility gate. MCP remains a candidate, not an automatically validated fallback.
- Do not claim managed-cloud conclusions from a self-hosted experiment. Do not replace official routing with internal helper calls to force qualification.

The six-hour limit is a project-management gate, not a claim that every legitimate setup should take less than six hours.

## 9. Research questions and experiment design

### 9.1 Questions

**RQ1: Transfer.** Which predeclared supported properties pass in embedded execution but fail through the qualified serving route?

**RQ2: Explanation.** Which differences are attributable to reconstruction, context handling, dispatch, state integration, or output conversion, and which are intended behavior or configuration errors?

**RQ3: Testing decision.** What failures do additional public-entrypoint tests detect, miss, and cost relative to local tests and a fuller end-to-end suite?

### 9.2 Two separate samples

**Historical issue/fix sample:** freeze a date window, repositories, search terms, and inclusion rules before running cases. Use this sample to explain mechanisms and assess regression coverage. It is outcome-enriched by construction and cannot estimate current prevalence.

**Official workflow sample:** choose examples based on supported features and accessibility without selecting them for observed failure. Keep every attempted case in the accounting. This provides a bounded assessment of test transfer in the selected population, not the whole ecosystem.

Do not pool defective historical versions and current examples into one headline failure rate. Do not quietly remove successful or difficult cases.

### 9.3 Pair construction and causal controls

For each workflow-property pair, match the application code, framework and dependency versions, initial state, equivalent caller identity and permissions, tool fixtures, model configuration, and relevant feature settings.

Some serving-induced differences, such as how caller context is reconstructed, are the treatment rather than confounders. Record them and trace their effect; do not normalize away the very mechanism being investigated.

Run each condition from isolated, equivalent initial state. Restore state between conditions and counterbalance execution order where shared external dependencies could matter. Never let an embedded run's side effects become the served run's starting state.

A causal case should include a valid contract, an embedded pass, a served failure, and evidence localizing the divergence. A fixed/unfixed comparison or narrowly scoped repair is useful corroboration. A crash caused by a missing environment variable is not evidence of a framework defect until correct setup has been established.

### 9.4 Deterministic isolation, then live-model confirmation

Use deterministic model doubles to isolate framework behavior when the framework supports them faithfully. A response must be valid for the actual prompt and tool schema in both conditions. If serving changes those inputs, blind replay may be invalid; treat that mismatch explicitly.

Use simple synthetic tools with inspectable side effects. Keep nondeterministic identifiers and time-dependent fields controlled where they are irrelevant to the property, without removing a dependency that is itself the mechanism.

After isolation, confirm representative cases with a real model if needed to establish realism. Report deterministic and live-model results separately. No large training run or custom simulator is part of the proposed study.

### 9.5 Outcome classification

Record both outcomes, not only failures:

- Embedded pass / served pass.
- Embedded pass / served fail.
- Embedded fail / served pass.
- Embedded fail / served fail.
- Unsupported, setup-blocked, or oracle-indeterminate, with reasons.

Separately adjudicate failure causes: confirmed implementation defect, intended difference, configuration mistake, model-dependent variation, or unresolved. Use a second researcher to review ambiguous contracts and root-cause classifications.

## 10. Testing baselines and the useful result

Compare three test configurations on the same eligible cases:

1. **Local baseline:** existing or representative embedded tests, with their actual assertions recorded.
2. **Boundary-focused tests:** a small selection exercising relevant official entrypoints and application properties.
3. **Fuller E2E reference:** a more complete public workflow sequence, using the same independent outcome oracle where possible.

The fuller suite is a comparative reference, not proof of all correctness. Distinguish adding a new oracle from changing the execution path: if the local baseline never checked the property at all, that is an assertion-coverage issue as well as, or instead of, a boundary issue.

For RQ1, apply the same property oracle across paired modes. For RQ3, examine native suite coverage and incremental tests separately. This avoids claiming that the network boundary alone explains a difference actually caused by stronger assertions.

Derive any proposed test-selection rule on discovery cases, freeze it, and evaluate on held-out workflows or defect families. Keep variants of the same root cause in the same partition. Historical fixes and their close variants must not leak across discovery and validation.

Prefer the term **small boundary-focused test set** over **minimal test set** unless minimality is defined and demonstrated. We are not proposing a new test-generation algorithm or a large testing platform.

The strongest result would identify a practical condition under which specific boundary tests add measurable coverage, show cases where they are unnecessary or insufficient, and report the tradeoff relative to fuller E2E testing.

## 11. The complete 72-hour pilot

| Elapsed time | Work | Required record |
|---|---|---|
| 0-6 hours | Access and relevant-path qualification for all three candidate frameworks | Two or more qualified frameworks, or stop and switch to fallback feasibility |
| 6-12 hours | Freeze pilot cases, contracts, configuration pairs, and upstream-test evidence | About six candidate issue cases across the accessible frameworks; explicit exclusions |
| 12-36 hours | Reproduce matched embedded/served behavior through actual endpoints | Aim for four tractable case pairs, including a historical defective/corrected pair |
| 36-60 hours | Exercise an outcome-blind sample of official workflows and compare test configurations | Aim for eight attempted workflows and at least six interpretable pairs; record successes too |
| 60-72 hours | Independent causal review, prior-art comparison, and continuation decision | A written go/no-go judgment supported by raw evidence |

These targets guide workload and feasibility. They are neither statistical significance thresholds nor a guaranteed sufficient final sample.

### 11.1 A substantive pilot pass requires all of the following

- Relevant serving access in at least two frameworks.
- Consequential, faithfully reproduced mode-dependent differences across at least two frameworks, which may include clearly labelled historical cases.
- More than one root-cause mechanism, with substantive evidence beyond already studied persistence/resume behavior.
- Valid contracts and credible exclusion of trivial version, configuration, and oracle errors.
- A concrete incremental testing decision, not merely proof that a network endpoint can be tested.
- A feasible path to held-out evaluation and completion within the remaining schedule.

Metadata-only observations can be retained, but cannot alone satisfy the proposed substantive-consequence gate.

### 11.2 Stop or reassess if

- Access requires waiting for external approvals or inaccessible managed services.
- All apparent failures disappear under correct supported configuration.
- All results concern previously studied persistence semantics, with no new test-transfer insight.
- Existing equivalent upstream tests already cover the entire phenomenon and the study adds no useful comparison.
- The only evidence consists of a few selected old bugs and generic integration-testing advice.
- A comparison requires bypassing official wiring, using incompatible model replay, or silently changing the application contract.
- Too few independent workflows remain to support the intended testing recommendation.

A null result is not scientifically invalid. But a tiny pilot finding no failures does not demonstrate broad reliability. A properly powered null-result study would require its own substantive question and design; it should not be improvised solely to rescue this proposal.

## 12. Main-study scale and analysis

After the pilot, a planning target is 20-30 paired workflows plus a separately reported defect corpus, across two or three qualified frameworks. This is a manageable starting scope, not a sample-size justification. Final scope must reflect available independent cases, expected precision, and setup attrition.

The basic record is a workflow-property pair within a specified framework, version, and serving mode. Multiple properties from one workflow and repeated runs of one case are correlated. They do not become independent tasks merely because the table has more rows.

Report:

- Attempted, eligible, excluded, and interpretable cases, with reasons.
- Paired outcome counts, separately by sample and consequence family.
- Number of independent mechanisms and framework configurations supporting each conclusion.
- Detection and misses for each test configuration, on discovery and held-out sets separately.
- Per-case runtime, startup cost, model-call count, and failures/retries.
- Human setup and adjudication effort, since infrastructure effort may dominate API expense.

For an outcome-blind eligible sample, the fraction of served failures among embedded passes can be reported with its explicit denominator. For issue-selected cases, label the same fraction as corpus coverage, not a deployment failure probability.

Use paired uncertainty estimates with clustering at the workflow or defect-family level when sample size supports them. With very few independent clusters, raw counts and case-level evidence are more honest than precise-looking confidence intervals. Do not treat repeated stochastic runs as new framework replications.

Choose the analysis and a practically meaningful benefit criterion before inspecting held-out outcomes. Do not optimize sample size, exclusions, or test policy until a desired significance result appears.

## 13. What a passing pilot means for acceptance chances

### 13.1 Direct answer

**A substantive passing pilot would make this worth developing into a SE4AgenticAI submission. It would not justify calling acceptance likely or assigning a numerical probability.**

We have not located a reliable submission/rejection denominator for the workshop. More importantly, a venue-wide acceptance rate would not directly give this paper's probability. We also do not yet have results, a finished manuscript, reviewer judgments, or knowledge of competing submissions.

Numbers such as 70%, 80%, or 90% would therefore be invented rather than evidence-based. This report intentionally does not provide one.

### 13.2 Separate three milestones

| Milestone | What it establishes | Submission judgment |
|---|---|---|
| Access gate passes | The relevant experiment can actually be run | No conclusion about the gap or acceptance |
| Substantive pilot passes | Credible mechanisms, useful comparison, and feasible evidence collection | Worth investing in the main study; not automatically submission-ready |
| Completed study passes validity and novelty checks | A bounded original result, evaluated guidance, honest claims, and reproducible evidence | Credible submission candidate; acceptance still uncertain |

### 13.3 Qualitative outlook under different results

**Strong completed result:** Multiple independently supported mechanisms, clear causal controls, substantive held-out testing evidence, and a usable artifact. Recommendation: submit confidently in the sense that the work is defensible, not that acceptance is predictable.

**Bounded but solid result:** Fewer cases, an important narrow lesson, and unusually clear evidence. Recommendation: consider a short paper and restrict the claim. Do not imply that the short-paper category is inherently easier to enter.

**Pilot-only result:** A few reproductions without independent validation or a useful test-selection result. Recommendation: insufficient for the intended contribution, even if every pilot example behaves as hoped.

**Weak result:** Only harmless metadata differences, setup mistakes, duplicated known findings, or unsupported claims about cloud behavior. Recommendation: do not submit this framing merely to meet the deadline.

### 13.4 Why this remains the acceptance-oriented preference

The choice is a judgment about the route to a complete, defensible manuscript: concrete motivation, direct scope fit, and fewer unresolved mechanism assumptions than slicing. It is not a measured ranking of paper acceptance probabilities.

The MCP idea remains more thoroughly reviewed in some respects and avoids serving-infrastructure risk. Deployment-boundary testing only retains its practical priority after the access gate succeeds. A deeper literature review is not the same as a stronger experimental contribution.

## 14. Reviewer objections and required answers

| Likely objection | Evidence needed, not rhetorical reassurance |
|---|---|
| "This just says integration testing matters." | A specific unresolved testing decision, held-out comparative detection results, and documented misses/costs |
| "You selected bugs, so of course you found bugs." | Separate issue-derived and outcome-blind samples; no prevalence claim from the former |
| "The two modes have different configurations." | Pinned versions and equivalent supported settings; explicit separation of treatment from accidental mismatch |
| "You only tested localhost, not deployment." | Name the actual serving mode and component; limit claims to that boundary; managed-only claims require managed execution |
| "The paper is another resume/persistence study." | Substantive non-persistence mechanisms and a precise comparison with persistence prior art |
| "Your stronger assertions, not serving, found the bug." | Same-oracle paired experiment separated from native-test coverage analysis |
| "The proposed test set is overfit." | Frozen discovery/validation split with related defect variants grouped together |
| "The model caused the difference." | Faithful deterministic isolation, captured inputs, and selected live-model confirmation |
| "These bugs are already fixed." | Historical labels and defective/corrected replay; contribution framed as test evidence, not novel bug discovery |
| "Two frameworks cannot represent the ecosystem." | Bounded conclusions, explicit sampling limits, and no universal framework ranking |

If a required answer is unavailable, reduce the claim or stop that part of the study. Do not add adjectives such as novel, robust, or generalizable in place of evidence.

## 15. Deliverables and paper structure

### 15.1 Research artifact

Produce simple scripts and fixtures rather than a new platform. The eventual artifact should contain:

- A framework/version/serving-mode manifest and reproducible environment setup.
- An access record with no credentials or private account details.
- Case provenance, property contracts, and inclusion/exclusion records.
- Embedded and public-entrypoint execution commands.
- Deterministic model/tool fixtures and explanations of their fidelity limits.
- Sanitized request/response traces, state snapshots, side-effect records, and raw outcomes.
- Discovery/validation assignments and frozen test-selection rules.
- Analysis scripts and data sufficient to reconstruct reported tables.
- Known limitations, licenses, and redistribution restrictions.

Do not redistribute third-party artifacts without checking permissions. An accessible GitHub repository is not by itself a license grant for every contained artifact.

### 15.2 Manuscript outline

1. **Problem and contribution:** the test-transfer decision and exact claim.
2. **Related work:** structural testing, framework bugs, portability, and persistence conformance.
3. **Study design:** scope, access, sampling, contracts, paired controls, and oracles.
4. **Results:** transfer outcomes and representative causal mechanisms.
5. **Testing implications:** incremental coverage, held-out validation, misses, and cost.
6. **Threats to validity and artifact:** access bias, version drift, model doubles, small samples, and generalization limits.
7. **Conclusion:** only what the data supports.

Do not write a results-bearing abstract before the experiments. The initial outline can describe objectives and methods in future tense.

## 16. Team, resources, and deadline

Suggested responsibilities:

| Researcher | Primary responsibility | Cross-check |
|---|---|---|
| A | First framework and served-path reproduction | Reproduce one case built by B |
| B | Second framework and historical revisions | Reproduce one case built by A |
| C | Sampling, contracts, oracles, and analysis | Independently adjudicate proposed failures |
| D, if available | Third framework, reproducibility, and manuscript integration | Audit held-out separation and claims |

For a three-person team, C coordinates writing and the third framework is optional after access qualification. At least one researcher other than a case's author should review its causal interpretation.

No training run is required. Begin with local resources and deterministic probes; estimate live-model and infrastructure costs from actual pilot usage. Include retries, failed runs, container startup, storage, and human setup time. A budget cap must be agreed before paid execution; this document authorizes no spending or account creation.

Illustrative schedule if work begins immediately:

- September 10-13: access-first pilot and written go/no-go decision.
- September 14-17: freeze main-study scope, property contracts, samples, and held-out split.
- September 18-27: main executions, independent reproductions, and analysis.
- September 28-October 4: manuscript and artifact completion, including negative and excluded cases.
- October 5-9: adversarial review, claim audit, formatting, and submission checks.

The current call lists an October 10, 2026 deadline, IEEE two-column formatting, 3-4 pages for short papers, and 8-10 pages for regular papers, including references. It also contains an inconsistent workshop-date line showing a 2025 year. Verify the final logistics through official channels before submission or travel planning; do not silently correct that line. [Official submission information](https://cs.uwaterloo.ca/~palencar/se4agenticai/)

Plan for a complete short paper first, expanding only if results and space requirements justify it. Do not compress essential validity information merely to force a page category. Registration, presentation obligations, anonymization, and any venue-specific AI-assistance requirements still require checking.

## 17. Audit of what is known and unknown

| Claim | Current evidence level |
|---|---|
| Topic is within the workshop scope | Official call verified |
| Empirical engineering contributions have appeared in the program | Official previous schedule verified; detailed methods access varies |
| Developers report relevant boundary problems | Primary issue/PR leads inspected, with the Mastra follow-up refresh limitation stated |
| Two or more relevant serving paths run in our environment | Not tested |
| Our team can reproduce consequential differences | Not tested |
| A new testing recommendation improves held-out detection | Not tested |
| No prior paper covers the exact useful contribution | Not proven; current review identifies a plausible residual gap |
| The paper has a high numerical acceptance probability | Unsupported |

This report reuses the earlier literature analysis rather than claiming a fresh exhaustive review. Current checks covered the official venue pages, principal issue leads, selected paper records, and serving documentation. Browser access failed for the Mastra follow-up, and an older Mastra documentation link no longer resolved. No inaccessible source was silently promoted into newly verified evidence.

Before the final manuscript, revisit the exact nearest papers and upstream tests using the actual selected mechanisms. A final focused novelty check should ask whether our completed result changes an engineering decision, not merely whether another paper has the same title.

## 18. Final recommendation and readiness checklist

**Proceed with the access-first deployment-boundary pilot. Commit to the full paper only after access, substantive evidence, and prior-art gates pass.**

If access fails, switch to the MCP study's feasibility gate. If access succeeds but the scientific contribution fails, do not automatically assume another idea is valid. Stop and reassess the evidence without extending the current proposal through arbitrary qualifiers.

Before submission, confirm:

- [ ] Actual official entrypoints are exercised and serving modes are accurately named.
- [ ] At least two frameworks contribute substantive evidence to the cross-framework claim.
- [ ] Historical and current-version findings are separated.
- [ ] Claims about task/state/approval effects are not based only on metadata loss.
- [ ] Properties have justified contracts and independent adjudication.
- [ ] Configuration differences and model randomness are controlled or explicitly analyzed.
- [ ] Prior work does not already supply the claimed substantive finding.
- [ ] The testing recommendation is validated on held-out cases, or its claim is explicitly retrospective.
- [ ] All attempts, exclusions, successes, and uncertainties are reported.
- [ ] Repeated runs are not misrepresented as independent workflows.
- [ ] The artifact reproduces the reported evidence and contains no secrets.
- [ ] The manuscript is complete, fits the format, and makes no invented acceptance or prevalence claim.

**Bottom line:** This is a legitimate candidate for original empirical research and our preferred acceptance-oriented investment, not a guaranteed acceptance. A passing pilot means the full study is worth doing. A strong completed study means submission is defensible. Those are separate decisions.

## Supporting project reviews

- [Fresh gap search and prior-art comparisons](FRESH_GAP_SEARCH_2026-09-09.md)
- [Past SE4AgenticAI papers and submission strategy](PAST_PAPERS_AND_SUBMISSION_STRATEGY_2026-09-09.md)
- [Earlier PR-test and MCP-adapter literature review](TOP_TWO_IDEAS_DEEP_LITERATURE_REVIEW_2026-09-09.md)

Where older documents differ on pilot order or fallback priority, this report reflects the latest decision: access first, deployment-boundary testing preferred for submission-oriented goals, and MCP as the access-risk fallback.
