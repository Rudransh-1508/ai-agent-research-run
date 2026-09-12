# Fresh niche idea search and adversarial adjudication

Date: 12 September 2026. Target: SE4AgenticAI 2026. Research review only: no pilot, paid model calls, or implementation was performed.

## 1. Decision

**The best surviving proposal from this search is an empirical study of effect-aware tool consolidation.** Working title:

> **Grouping Agent Tools by Effects: Task Reliability, Context Cost, and Approval Precision**

The question is whether grouping operations by their effects, rather than only by the resource they act on, offers a useful operational trade-off for an LLM agent. Compare it with atomic tools, resource-grouped tools with correct argument-aware approval handling, and atomic tools with search/discovery.

This survived the bounded literature review as an **incremental, falsifiable architectural research question**. It did not emerge as a new algorithm, proven improvement, or a high-confidence positive pilot. I recommend it over the other fresh candidates reviewed here, but authorize only a bounded pilot next, not an unconditional main-study commitment.

The important distinction is between three claims:

| Claim | Current assessment |
| --- | --- |
| The engineering decision is real | Supported by protocol proposals and an official product's tool-consolidation design. |
| The specific controlled comparison is not already answered | No direct answer located in the reviewed primary methods and experiments. This is a bounded search finding, not a novelty guarantee. |
| Effect-aware grouping will improve a useful outcome | Unknown. The pilot must test this; literature cannot establish it. |

There is no defensible numerical acceptance estimate. A well-executed result could justify a workshop short paper. An underpowered null or an obvious annotation calculation would not.

## 2. How this search was conducted

Three reviewers worked in bounded parallel branches: reliability/testing, state/data lifecycle, and assurance/interface design. After initial elimination, the reliability and state reviewers independently challenged the interface candidate. The coordinating review also inspected the closest interface papers, protocol discussion, current annotation schema, existing resolution proposal, and the Plane catalog documentation.

The brainstorming skill was used to separate candidate selection from implementation. Its practical effect was to require explicit alternatives and rejection criteria before proposing a build.

Searches combined niche SE constructs with agents: delta debugging, partial-order equivalence, exception contracts, command-query separation, tool grouping, state invalidation, provenance, consent binding, complete-set retrieval, pagination, and approval granularity. Sources included arXiv, ACL, author-hosted papers, official specifications, and source repositories. Technical conclusions rely on primary sources; search snippets and secondary summaries were used to discover leads.

The companion reviews record literal reading depths. A methods/experiments read is not labelled an entire-paper read. Papers, proposed standards, practitioner artifacts and repository documentation are not treated as equivalent evidence. No experiment reported by another author was independently reproduced in this search. Most repository references point to a moving branch; freeze commits before a pilot.

Companion evidence:

- [Reliability candidates and recovery-ownership review](reviews/niche_reliability_search_2026-09-12.md)
- [State lifecycle and pagination review](reviews/niche_state_search_2026-09-12.md)
- [Assurance and closest interface papers](reviews/niche_assurance_search_2026-09-12.md)
- [Independent interface red-team review](reviews/effect_grouping_redteam_2026-09-12.md)
- [Independent design and artifact review](reviews/effect_grouping_design_review_2026-09-12.md)

These are bounded research audits, not a systematic review with exhaustive database coverage. Agent agreement is not evidence of novelty; the source comparisons below are the evidence.

## 3. Comparison of the serious propositions

| Proposition | Why initially attractive | Why selected or rejected |
| --- | --- | --- |
| **Effect-aware tool consolidation** | A routine architectural decision with competing pressures: compact catalogs, action-selection complexity, and precise approval handling. Controllable experiment. | **Selected conditionally.** Broad interface-design claims are occupied, but the specific grouping/policy comparison was not located. Must demonstrate a nontrivial trade-off against strong existing alternatives. |
| Equally informed model-owned versus runtime-owned recovery | Local fault injection and explicit state oracles; no rare incident dependency. | Reserve, not selected. Verified Tool Calls, ToolMaze, SHIELDA and ToolRobustBench occupy most ingredients. A fairer ownership comparison remains possible, but its expected contribution is weaker than simply showing deterministic recovery beats advice. |
| Complete-set pagination and result offloading | Exact set/state oracles and authentic partial-result problems. | Reject as a fresh central question. Large Result Offloading already compares delivery architectures on whole-corpus tasks; ComtradeBench evaluates complete paginated workflows. Correcting baseline confounds would be replication/extension, not a newly discovered gap. |
| Derived-memory invalidation before actions | Concrete state-lifecycle mechanism, explicit dependency metadata. | Reject. MemTX, STALE/CUPMem, Invalidation Contracts and CoAgent substantially cover the proposed boundary and mechanisms. |
| Approval freshness and exact-action binding | Clear correctness property and cheap substitution tests. | Reject. Consent Integrity and existing approval protocols directly cover action binding and TOCTOU cases. |

Trace reduction and observation-order testing were also screened and not promoted. GCJR and ICSE-SEIP delta debugging occupy much of the former; permutation relations and stable-order buffering weaken the latter. Telemetry redaction and state-oracle mutation were early exclusions after close-title/abstract discovery, not full independent audits in this round.

The rejected papers are individually linked and compared in the companion reviews. We did not reject them because an area is merely crowded. We rejected specific proposed contributions because of substantive overlap or insufficient remaining benefit.

## 4. The proposed idea in plain language

Suppose an agent can inspect, create and delete project labels. An API can expose those same capabilities in different ways:

| Design | Illustrative model-visible interface |
| --- | --- |
| Atomic | `list_labels(...)`, `create_label(...)`, `delete_label(...)` |
| Resource-grouped | `labels(action="list/create/delete", ...)` |
| Resource plus effect | `labels_query(action="list/retrieve", ...)`, `labels_update(action="create/update", ...)`, `labels_delete(...)` |

The third row is illustrative. The actual partition must follow a declared approval policy and verified effects, not assume that every operation named `update` has the same risk. If the policy only distinguishes read from write, use that distinction. If it distinguishes destructive operations, the partition must preserve it. Parameter-dependent effects require conservative treatment or argument-aware resolution.

All presentations dispatch to the **same primitive implementation**. No condition gets extra powers, easier validation, secret state, or a better task solver.

The research question is:

> **When exposing the same operations to an LLM agent, can effect-aware grouping provide a useful task-success/context-cost trade-off at precise approval handling, compared with resource grouping plus argument-aware policy and atomic tools plus discovery?**

This is not a proposal to invent CQRS, a new MCP permission standard, or a security boundary based on trusting arbitrary tool descriptions.

### Five-statement test

1. **Existing technique:** command-query separation, cohesive interface partitioning, operation-level policy checks, and tool consolidation.
2. **Specific mechanism:** changing interface packaging changes the model's action-selection problem. Fewer tool names can mean more action-discriminator and argument ambiguity. Effect-based separation can clarify operation classes while increasing catalog size. Unlike a prewritten caller, an LLM chooses actions from this presentation at runtime.
3. **Engineering consequence:** a compact interface can alter task reliability and the granularity available to an approval layer. Neither catalog size nor a simple read-only label determines end-to-end utility.
4. **Contribution:** controlled comparative evidence, equivalent interface adapters, executable task oracles and a deployment decision rule. Not a claim that classical SE patterns fail universally.
5. **Decisive experiment:** change only catalog partition and explicitly model policy granularity; evaluate task success, real token/call cost and approval decisions against strong baselines.

The classical pattern itself supplies no novel algorithm. The remaining contribution must be the measured architectural decision.

## 5. Authentic grounding, with evidence limits

### A real consolidated catalog

Plane's official MCP documentation describes 30 resource-level tools exposing 204 actions, following a previously advertised 177-tool interface. It documents per-action metadata and mappings for many retired names. This is concrete evidence of the architectural choice, not evidence that Plane is defective. Its offline SpyClient tests check dispatch against SDK signatures; they do not establish persistent-state task correctness. [Plane tool-surface documentation](https://github.com/makeplane/plane-mcp-server/blob/main/plane_mcp/tools/README.md).

Do not compare historical counts as though 177 old operations and 204 current actions were an equivalent experiment. Construct every experimental facade from one frozen current operation manifest. Use historical aliases only as provenance or mapping help.

### A documented policy-granularity concern

A contributor in the official MCP repository describes how mixed-action tools require conservative aggregate annotations and can trigger unnecessary confirmations for individual read operations. This is a contributor's argument, not a core-maintainer empirical finding or a reproduced incident corpus. The corresponding meeting notes encourage ecosystem experimentation. [MCP discussion 2204](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/2204).

### An existing solution that must be allowed to win

SEP-1862 explicitly proposed argument-specific tool resolution. The core PR is closed; a linked experimental extension PR remains open in the inspected source. The extension includes reference helpers and conformance material. These are proposal/artifact evidence, not proof of universal deployment. A local argument-aware dispatcher is also a legitimate, potentially cheaper baseline. [SEP-1862](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1862), [experimental extension PR 9](https://github.com/modelcontextprotocol/experimental-ext-tool-annotations/pull/9).

### Trust boundary

The inspected MCP 2026-07-28 schema still defines tool-level annotations and warns that they are hints, not guaranteed behavioral descriptions. Do not rely on annotations from untrusted servers for enforcement. The experiment concerns owned or verified tools with independently established operation effects and an independent executor. [Current inspected schema](https://modelcontextprotocol.io/specification/2026-07-28/schema#toolannotations).

## 6. Closest literature and exact residual

| Primary source | What it already contributes | What remains different here |
| --- | --- | --- |
| [The Devil Is in the Interface, 2608.11386](https://arxiv.org/html/2608.11386v1) | Six similar-capability coding interfaces; task success, repeated-attempt consistency, exploration, efficiency and interaction errors. Main setup/results and relevant Appendix B.3 inspected by multiple reviewers. | Does not isolate effect-homogeneous versus resource-homogeneous action-enum partitioning at matched policy precision. Its malformed-command/broken-edit analysis is not the same as successful but unwanted effects. This is the strongest scholarly overlap. |
| [ToolScope, ACL 2026](https://aclanthology.org/2026.acl-long.1573.pdf) | Consolidates overlapping/semantically equivalent tools and evaluates selection, functionality preservation and a small end-to-end answer study. Merger methods and relevant final-paper appendices inspected. | Combining equivalent functions is different from grouping distinct read/write operations behind a discriminator. No approval-precision comparison located in the inspected evaluation. Do not misdescribe ToolScope as merging arbitrary CRUD actions. |
| [The Art of Tool Interface Design, REALM 2025](https://aclanthology.org/2025.realm-1.5/) | Thinker combines state-machine business logic, confirmation sequencing, delegated reasoning and context management. Methods and relevant evaluation/ablations inspected. | Changes several execution mechanisms. It does not isolate a capability-equivalent catalog partition under identical primitive execution. |
| [IPIGuard, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.53/) | Already applies command/query separation in graph-constrained prompt-injection defense. Query expansion and evaluation sections inspected. | Changes permitted execution behavior rather than solely catalog presentation. A new CQS-for-agents claim would be wrong. |
| [AgenTRIM, 2601.12449](https://arxiv.org/html/2601.12449v1) | Least-privilege tool exposure, risk classification and validation. Relevant methods and policy experiments inspected by the assurance reviewer. | Permission reduction is not the intervention proposed here. Hold primitive authority fixed. |
| [HyperTool, 2606.13663](https://arxiv.org/html/2606.13663v1) | Changes execution granularity by composing tools inside executable blocks. Interface, setup and relevant risk material inspected. | Our core conditions execute one primitive per action. Introducing code blocks would require a separate, explicitly broader comparison. |
| [Semantic Method Naming and LLM Agent Accuracy, SSRN 6460766](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6460766) | Controlled CRUD-versus-intent naming study. Primary abstract screened, full paper not audited here. | Makes naming/description controls mandatory. A better name alone is not the proposed contribution. |
| [Diagnosing Tool-Selection Reasoning with Canary Tools, 2608.04719](https://arxiv.org/html/2608.04719v1) | Diagnostic distractor tools and selection errors. Methods/results and relevant appendices inspected by the assurance reviewer. | Warns of low error rates for strong models. We must not depend on manufacturing accidental unsafe actions. |
| [Command Query Separation](https://martinfowler.com/bliki/CommandQuerySeparation.html) | Established design principle and its trade-offs. Primary practitioner exposition inspected. | Classical foundation, not our invention. The project does not require separate read/write databases or a full CQRS architecture. |

**Permissible novelty statement:** We evaluate an unresolved catalog-partition decision for agent-facing APIs, measuring executable task utility and cost jointly with policy precision while holding primitive capabilities fixed. The searched prior work establishes interface effects, tool consolidation and fine-grained policies separately; we did not locate this controlled comparison.

**Impermissible claims:** first tool-interface study; first separation of reads/writes for agents; first recognition of annotation imprecision; first argument-aware policy; evidence that MCP is inherently insecure; guaranteed safer agents.

## 7. Reviewer disagreement and final adjudication

The assurance reviewer regards the cost/utility/approval comparison as a legitimate incremental survivor. The reliability reviewer agrees no exact experiment was found but warns that approval precision under conservative aggregate labels is predetermined. A correct local argument-aware dispatcher can remove the imprecision with negligible policy compute.

**I accept that objection.** It becomes a hard experimental requirement, not a caveat buried in related work:

- Fewer unnecessary approvals than a coarse tool-level gate is not enough.
- Do not invent a costly resolver, network delay or human penalty for the strongest baseline.
- Do not count construction-time annotation correctness as an empirical discovery.
- Effect grouping must have a meaningful held-out utility/cost advantage or useful non-dominated trade-off against resource grouping with argument-aware policy and atomic tools with discovery.
- If it does not, stop the proposed positive-method paper. Do not add another qualifier or omit the winning baseline.

The final recommendation is therefore stronger than a topic suggestion, but weaker than a greenlit paper: **one selected, literature-surviving empirical question with explicit failure conditions.**

## 8. Minimum implementation and experiment

### Artifact

Build a small adapter layer over an existing executable environment, not a new agent framework. An operation manifest records primitive ID, real arguments, return behavior, verified effect class, and dispatch target. Generate equivalent catalog presentations from it. Keep mapping information in the artifact so reviewers can inspect exactly what changed.

Use Plane as authentic catalog provenance. Use an existing local stateful environment such as AgentDojo for task execution where suitable. Do not pretend AgentDojo tasks are Plane tasks. An optional Plane-derived backend fixture must be labelled a simulator and separately checked against operation semantics. [AgentDojo repository](https://github.com/ethz-spylab/agentdojo).

Selected AgentDojo Workspace source checks provide concrete starting points: unchanged-state assertions for read tasks and explicit calendar/email state additions. They also permit legitimate incidental effects, such as marking previously unread email as read. Classify effects from behavior, not verbs such as `get` or `read`. Some answer checks are substring-based, so selecting this benchmark does not remove the need to audit each task oracle. [Inspected task source](https://github.com/ethz-spylab/agentdojo/blob/main/src/agentdojo/default_suites/v1/workspace/user_tasks.py).

Before model runs, replay reference primitive sequences through each facade and compare outputs, exceptions, transitions and final state. Verify argument validation and error text are not systematically better in the proposed condition. Test every exposed action mapping and omitted-argument behavior. Pin code, schema, task and model versions.

### Main comparison

| Condition | Presentation | Approval interpretation |
| --- | --- | --- |
| A | Atomic operation tools | Operation-level metadata |
| R | Resource-based mixed-effect bundles | Conservative whole-tool metadata |
| E | Resource/effect partition | Conservative homogeneous-group metadata |
| R+P | Same resource bundles as R | Correct argument-aware operation policy |
| A+S | Atomic tools with search/progressive discovery | Operation-level metadata; search is not allowed to hide valid operations permanently |

R and R+P may share exactly the same model trajectory if policy decisions are evaluated only in shadow mode. They are then one rollout with two policy analyses, **not independent repeated evidence**.

A and E must also be checked with the same argument-aware policy in sensitivity analysis. This separates catalog-induced behavior from enforcement effects.

For the primary behavioral comparison, use the identical argument-aware executor policy in every arm, or the identical sandbox-only non-enforcing policy in every arm. Never attribute a difference caused by stronger enforcement to grouping. The table's alternative annotation interpretations are a separately labelled policy-precision analysis.

### Two evaluation layers

1. **Interface behavior:** execute safe sandbox tasks with fixed backend permissions; measure completion, invalid actions, tokens, calls and requested-versus-observed effects. No live accounts or external writes.
2. **Policy precision:** replay proposed primitive calls through a frozen approval policy and record required, unnecessary and missed approval decisions. Shadow mode avoids confounding catalog quality with simulated human replies. It measures software decision precision, not actual human behavior or alert fatigue.

A later closed-loop confirmation experiment may use a clearly specified scripted approver. Its behavior must be identical across conditions and not reveal the hidden task answer. Do not claim reduced human mistakes without a human study.

### Essential controls

- Primary practical comparison: realistic resource partitions versus realistic effect partitions. Report their actual tool counts and schema sizes.
- Causal control: matched-cardinality, matched-group-size partitions over the same operation set, with multiple allocations. Do not use meaningless dummy tools as the only count control.
- Naming and description control: shared source descriptions, clear names in every arm, counterbalanced order, and independently authored alternate naming templates. No deliberately confusing baseline.
- Identical argument constraints and operation preconditions. Do not give only one condition discriminated-union validation or better error recovery.
- Catalog-size regimes chosen before outcomes, using real supported operations rather than duplicated distractors.
- Read-only, legitimate-write and mixed read/write tasks. Less activity is not better reliability.
- No oracle task labels, target IDs or hidden state are exposed only to the proposed method.
- Actual input/output/cache-token accounting, backend calls and latency. Search and runtime policy compute are measured, not assigned arbitrary penalties.
- Independent state/trace checks for extra effects; an existing benchmark's success checker is not automatically a complete no-extra-effects oracle.

### Outcomes

Primary: executable task completion and total model cost per assigned task at the specified approval precision. Report both, not an opaque weighted score. Also show cost per correct task, but never only this ratio because selection on success can conceal failures.

Secondary: unnecessary approvals per task, missed required approvals, invalid calls, extra persistent effects, number of tool selections and latency. Exact action IDs and effect ledgers support diagnosis, not string matching on final answers.

## 9. Bounded pilot and what passing would mean

Suggested cap: five working days after authorization and a separately approved API-spend ceiling. No expenditure is authorized by this report.

### Stage 1: local feasibility, before API spend

Freeze one stateful backend, a representative operation subset, independent task oracles and the equivalence tests. Inspect a second catalog for external validity. Confirm real model access and billing limits before scheduling runs. A dispatch spy alone does not pass this stage.

### Stage 2: controlled screen

Illustrative plan: 24 fixed tasks across at least two task families, four model-visible presentations (A, R, E, A+S), two model families, and two repetitions: **384 episodes**. Evaluate R+P on the same R trajectories when using shadow approval. Include simple reference-solvable tasks and realistic multistep tasks, not only specially adversarial wording.

Reserve at most another 192 episodes before calling the pilot a pass: 96 for two cardinality-matched presentations on 12 held-out tasks, two models and two repetitions; 96 for a prewritten naming variant of that comparison. Total proposed ceiling: **576 episodes**, not an open-ended search. If the main screen is plainly negative, do not spend this reserve. If the required controls cannot fit the agreed spend/time cap, record an inconclusive investment gate rather than claiming a pass.

This is a feasibility and effect-size screen, not a powered equivalence study. Set a reachable per-episode cap after reference execution; do not make baseline success impossible through a shorter call budget. Stop at the fixed cap, including failed runs in the record.

### Pilot passes for main-study investment only if

1. Equivalent facades and independent outcome checks work end to end.
2. A material, interpretable utility/cost trade-off appears beyond the deterministic annotation result.
3. The candidate is not plainly dominated by R+P or A+S, and the signal is not solely a count, wording or malformed-schema effect.
4. The result is not confined to one contrived task or an irrelevant weak model.
5. Observed variance implies that an independent confirmation study can fit the remaining budget and deadline.

Choose the practical effect threshold before calls. An example investment target is a 15% cost reduction at no more than a 5 percentage-point task-success loss, or a materially improved success rate at matched cost. These are **proposed decision margins**, not predicted results, literature-derived constants or claims of sufficient pilot power. A beneficial trade-off must also survive comparison with the strongest alternatives.

A passing pilot means the artifact works and the evidence justifies confirmation. It does not establish generalization, prove security, demonstrate human benefit, or imply acceptance.

### Hard stops

- Strong baselines dominate at measured cost and policy precision.
- Only the known overprompting arithmetic improves.
- Only a poorly documented/invalid baseline fails.
- Apparent gain disappears under matched cardinality or shared argument validation.
- Both model families are at a floor/ceiling that makes a meaningful difference unidentifiable within budget.
- The main study would require unbounded task invention, rare bugs, cloud access delays or continual increases in sample size.

Do not treat a nonsignificant difference as equivalence. Do not keep collecting until significance appears. Low unintended-effect rates are not automatically fatal to the architecture study, but they prohibit an unsafe-action-reduction claim; another genuinely useful empirical result must carry the paper.

## 10. Confirmation study and analysis

Keep confirmation tasks separate from pilot tasks and from description tuning. Use task-level pairing and cluster uncertainty by independently authored task or task family as appropriate. Rollouts are repeated measurements, not extra independent task discoveries. Keep model families separate in primary tables; a pooled average can hide a reversal.

Predeclare one primary comparison or correct multiple confirmatory comparisons. Use confidence intervals for success differences and cost ratios; specify any non-inferiority margin before confirmation. Report all configurations and task failures. Show catalog size as a prespecified moderator, not a post-hoc favorable subgroup.

The main study should include a second independent operation/task setting. Freeze the strongest baseline before the holdout. A small precise result is preferable to an expansive model/framework sweep with unreliable oracles.

If a precise negative result establishes that effect grouping adds nothing over simple argument-aware policies, it may still be scientifically useful. It is not the anticipated positive-method contribution, and this report does not promise that a small negative pilot is publishable. Decide whether a replication/negative-result paper is worth writing separately rather than automatically relabelling failure as success.

## 11. Why SE4AgenticAI, and submission judgment

The workshop explicitly covers architecture, agent-tool protocols, testing/evaluation, data management and human-in-the-loop systems. This proposal studies the software surrounding the model, with an executable artifact and a concrete developer decision. That is a direct topical fit. The official page currently lists a 10 October 2026 deadline, short papers of 3-4 pages and regular papers of 8-10 pages, including references. [Workshop CFP](https://cs.uwaterloo.ca/~palencar/se4agenticai/).

The project's [past-paper review](PAST_PAPERS_AND_SUBMISSION_STRATEGY_2026-09-09.md) suggests the workshop accepts different contribution forms, including architectural work. Its small past program cannot support acceptance-rate predictions or a claim that a particular style is favored statistically.

For a team of 3-4, divide ownership into: interface equivalence/backend; tasks and independent oracles; experiments/statistics; literature/writing/reproducibility. Start drafting the methods and related-work comparison before results, but do not start a large implementation until the bounded design is approved.

**Submission recommendation:** aim for a rigorous short paper if the pilot leads to an independently confirmed, actionable trade-off. Consider a regular paper only with broader evidence and a commensurate contribution. A passing harness and a few favorable examples are not enough.

## 12. Bottom line

Choose **effect-aware tool consolidation** if choosing one fresh idea from this review. Its strengths are authentic design pressure, a concrete artifact, objective evaluation and no dependence on finding rare production bugs. Its weaknesses are incremental novelty and the possibility that simple argument-aware grouping/search baselines remove all advantage.

The honest current label is **literature-surviving, worth a bounded pilot, not yet a validated positive research result**. We should not replace uncertainty with an acceptance percentage or promise that the pilot will pass.
