# MASO 2026 Research Proposal: Policy-Preserving Delegation and Causal Accountability

**Working title:** Who Authorized This Agent? Policy-Preserving Delegation and Causal Accountability in Cross-Organizational Agentic Systems

**Target venue:** [MASO 2026, 1st International Workshop on Multi-Agent and Agentic Systems in Organizations](https://www.maso.uno/call-for-papers.php?lang=en), colocated with PRIMA 2026

**Submission deadline:** 10 October 2026, 23:59 AoE

**Workshop date:** 14 December 2026, Kumamoto, Japan

**Recommended submission type:** Full research paper if the complete cross-framework evaluation is finished; short paper if only the model, testbed, and preliminary evaluation are ready

**Review date:** 9 September 2026

## Executive summary

This proposal studies what happens to organizational authority, policy, and accountability when one autonomous agent delegates work to another agent, which then invokes external tools. The motivating execution chain is:

```text
Human principal
  -> organizational agent
  -> external or partner agent
  -> tool protocol client
  -> enterprise system or tool
```

Current agent protocols make this chain technically possible. They do not ensure that the original authority, purpose, consent, restrictions, and responsibility remain intact at every hop. An agent can therefore be syntactically authorized to communicate while being organizationally unauthorized to make a particular decision.

The proposed research will define executable delegation invariants, enforce them across heterogeneous A2A and MCP workflows, and evaluate them in a realistic cross-organizational testbed. Controlled faults and adversarial cases will test authority amplification, confused-deputy behavior, policy conflicts, revocation, agent substitution, replay, and incomplete provenance. Causal replay will then determine which handoff caused a violation and whether repairing that handoff prevents recurrence.

The central research question is:

> How can organizations preserve decision rights, policy constraints, and accountability when autonomous agents delegate work across organizational and technical boundaries?

This is a particularly strong MASO topic because it treats an agentic system as an organizational and socio-technical system rather than merely a collection of LLM calls.

## Why this is a strong MASO fit

MASO explicitly welcomes research on agent architecture, orchestration, enterprise integration, communication protocols, access control, distributed decision-making, human-agent decision rights, governance, accountability, compliance, safety, systemic failure, organizational testbeds, and real deployment challenges. This proposal connects nearly all of those themes through one focused problem.

| MASO theme | Fit | Connection to this proposal |
|---|---:|---|
| Governance, accountability, and compliance | 10/10 | The research formalizes authority, obligations, prohibitions, policy precedence, revocation, and responsibility across delegation chains. |
| Interoperability and enterprise integration | 10/10 | It evaluates A2A agent communication and MCP tool access across independently implemented organizational systems. |
| Agent architecture and orchestration | 9/10 | Delegation, state, agent roles, task lifecycle, and policy enforcement are evaluated as architectural concerns. |
| Trust, safety, security, and reliability | 9/10 | The experiment includes authority amplification, confused-deputy failures, substitution, replay, collusion, and incomplete provenance. |
| Multi-agent coordination and decision-making | 9/10 | Agents distribute decisions across organizational roles while operating under different policies and information boundaries. |
| Evaluation and organizational testbeds | 9/10 | The primary artifact is an executable, fault-injectable cross-organizational testbed with process and outcome metrics. |
| Human-agent collaboration | 8/10 | A human manager or compliance officer retains decision rights and receives risk-sensitive escalation requests. |
| Organizational design and transformation | 7/10 | The study compares centralized and distributed authority structures and examines how agents change responsibility allocation. |
| Organizational learning and memory | 6/10 | Provenance and policy versions must persist through agent memory and derived artifacts, but memory is not the main contribution. |

The topic would be less suitable if framed primarily as an MCP or OAuth security paper. For MASO, protocols must remain implementation mechanisms supporting an organizational research question. The paper should lead with decision rights, delegation, policy, responsibility, and organizational boundaries.

## Motivating organizational problem

Consider a procurement workflow involving a buyer organization and a supplier organization:

1. A human manager asks a procurement agent to source equipment under a fixed budget.
2. The procurement agent delegates supplier discovery to an external broker agent.
3. The broker delegates quote collection to supplier agents.
4. A supplier agent invokes MCP tools that read catalog data and prepare an order.
5. The procurement agent evaluates the quotes and requests approval.
6. A purchasing tool places the final order.

The human authorization might contain several conditions:

- Spend no more than a specified amount.
- Use only approved suppliers.
- Do not share employee or project information.
- Obtain a human approval before an irreversible purchase.
- Prefer lower-carbon delivery if price and deadline constraints remain satisfied.
- Stop all pending work if authorization is revoked.

Every individual protocol message can be valid while the overall workflow violates one of these conditions. Examples include:

- The broker interprets a budget as applying per supplier rather than to the complete order.
- A supplier agent receives more employee information than is necessary.
- An external agent calls a tool using authority inherited from the orchestrator without explicit attenuation.
- A policy changes while an agent is executing an old plan.
- An approval is replayed for a different transaction.
- The final action is compliant, but the path taken included prohibited disclosure.
- A downstream agent reasonably follows incorrect upstream information, making technical blame and organizational responsibility different.

These are organizational failures expressed through software architecture. Existing protocol authorization is necessary but insufficient to resolve them.

## Precise research gap

The research gap is not that multi-agent governance, norms, roles, or access control have never been studied. Classical multi-agent systems already provide rich theories of organizations and normative institutions. Modern protocols also provide authentication and authorization mechanisms.

The defensible gap is narrower:

> There is no mature, empirically validated method for preserving and verifying organizational authority, purpose, policy, provenance, revocation, and accountability across heterogeneous, stochastic, multi-hop LLM-agent delegation chains that cross agent, tool, framework, and organizational boundaries.

Five limitations in current research support this gap:

1. **Protocol validity is not semantic or organizational validity.** Message schemas and authentication do not prove that an agent interpreted a capability, policy, task state, or decision right correctly.
2. **Authorization is commonly checked locally.** A local access check does not guarantee that authority was attenuated correctly across the complete delegation chain.
3. **Policies are evaluated mainly at individual actions.** Organizational obligations can span several agents and several steps, including required approvals and purpose restrictions.
4. **Logs do not automatically establish causality or responsibility.** A downstream failure may be a symptom of an upstream error, shared context, policy ambiguity, or human approval mistake.
5. **Most benchmarks are short and technically scoped.** They rarely combine organizational roles, heterogeneous agents, changing policies, irreversible tools, human escalation, and cross-organizational boundaries.

## Literature review

### Classical organizational and normative multi-agent systems

The proposal should acknowledge rather than rediscover the classical foundations.

- Dignum et al.'s [OperA model](https://doi.org/10.1017/S0269888904000244) combines agent autonomy with prescribed organizational roles, objectives, interactions, and norms.
- Cuní et al.'s work on [electronic institutions](https://doi.org/10.1016/j.engappai.2004.11.019) formalizes roles, permissions, prohibitions, scenes, and compliant interaction workflows.
- Horling and Lesser's [organizational paradigms review](https://mas.cs.umass.edu/Documents/bhorling/horling-paradigms.pdf) compares hierarchies, coalitions, teams, federations, markets, matrices, and other multi-agent organizational structures.

These foundations show that organizational rules and roles are established research topics. The modern challenge arises from stochastic language-model behavior, tool-mediated side effects, mutable memory, dynamic policy, framework heterogeneity, and natural-language delegation.

### Agent protocols and interoperability

- The official [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) specifies protected resources, OAuth-based authorization, token audience binding, and related security requirements.
- The official [A2A specification](https://a2a-protocol.org/latest/specification/) specifies Agent Cards, skills, messages, tasks, artifacts, authentication, and multiple bindings.
- Ehtesham et al.'s [survey of agent interoperability protocols](https://arxiv.org/abs/2505.02279) compares MCP, ACP, A2A, and ANP, but is primarily taxonomic.
- Predoaia et al.'s [implementation-grounded MCP and A2A comparison](https://arxiv.org/abs/2607.23884) evaluates one software-engineering coordination scenario and identifies different trade-offs between lightweight integration and richer task lifecycle support.

This work explains what protocols provide. It does not establish whether independently implemented agents preserve organizational meaning, authority, and purpose across mixed-protocol execution.

### Policy enforcement and agent safety

- [AgentDojo](https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2024, provides 97 realistic tasks and 629 security test cases for tool-using agents under prompt-injection attacks.
- Zwerdling et al.'s [policy-to-guard work](https://aclanthology.org/2025.emnlp-industry.41/), EMNLP Industry 2025, compiles organizational policies into tool guards.
- [AgentSpec](https://arxiv.org/abs/2503.18666) proposes a domain-specific language and runtime enforcement mechanism for agent constraints.
- Xiang et al.'s [GuardAgent](https://proceedings.mlr.press/v267/xiang25a.html), ICML 2025, provides knowledge-enabled safety guards for agent actions.
- [Towards Verifiably Safe Tool Use for LLM Agents](https://doi.org/10.1145/3786582.3786839), ICSE 2026, combines hazard analysis, capability labels, information-flow controls, and formal modeling at tool boundaries.

These systems offer important local controls. The unresolved issue is compositional assurance: whether locally compliant agents and tool calls jointly satisfy an organizational invariant across delegation, policy conflicts, and individually benign actions that combine into harm.

### Multi-agent failures and attribution

- Cemri et al.'s [Why Do Multi-Agent LLM Systems Fail?](https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2025, identifies 14 failure modes involving system design, inter-agent misalignment, verification, and termination.
- Zhang et al.'s [Who&When](https://proceedings.mlr.press/v267/zhang25cq.html), ICML 2025, studies the responsible agent and decisive failure step across 127 multi-agent configurations. Its reported best attribution results show that the problem remains difficult.
- Chen et al.'s [Seeing the Whole Elephant](https://aclanthology.org/2026.acl-long.912/), ACL 2026, provides complete traces and reproducible environments and demonstrates the diagnostic value of full observability.
- [MultiAgentBench](https://aclanthology.org/2025.acl-long.421/), ACL 2025, evaluates collaboration and competition across several coordination topologies.

These studies identify or localize failures from observed traces. They generally do not validate causality by intervening on the blamed handoff and demonstrating that the repair prevents the violation.

### Human-agent authority and organizational outcomes

- Vaccaro, Almaatouq, and Malone's [systematic review and meta-analysis](https://www.nature.com/articles/s41562-024-02024-1), Nature Human Behaviour 2024, synthesizes 106 experiments. Human-AI combinations performed better than humans alone on average but worse than the better standalone human or AI, demonstrating that collaboration does not automatically create synergy.
- Wu et al.'s [human-generative AI collaboration study](https://www.nature.com/articles/s41598-025-98385-2), Scientific Reports 2025, found immediate performance gains alongside negative effects on intrinsic motivation and boredom across four online experiments.
- Guo et al.'s [organized embodied agent teams](https://arxiv.org/abs/2403.12482) show that imposed organizational structures and leadership affect communication cost and team performance.

Most human-AI experiments use a single AI, fixed authority, short tasks, and little consequential tool use. Evidence remains limited for multi-human, multi-agent teams with dynamically changing decision rights and responsibility after failures.

### Enterprise evaluation

- [EnterpriseBench](https://arxiv.org/abs/2510.27287) simulates fragmented enterprise data, access-control hierarchies, and cross-functional workflows across software engineering, HR, finance, and administration.
- [CI-Work](https://arxiv.org/abs/2604.21308) evaluates contextual integrity in enterprise workflows and reports a tension between task utility and privacy.
- [EnterpriseArena](https://arxiv.org/abs/2603.23638) studies long-horizon resource allocation under partial observability and budgeted tools.

These benchmarks improve organizational realism but do not provide a general cross-organizational delegation and policy-continuity testbed.

## Novelty boundary

The paper should not make any of these claims:

- Organizational roles for agents are new.
- Norms and permissions in multi-agent systems are new.
- MCP or A2A interoperability is unexplored.
- Tool authorization is unexplored.
- Multi-agent failure attribution is unexplored.
- Provenance logging alone solves accountability.

The paper can defensibly claim novelty if it delivers all or most of the following:

- A formal model of authority attenuation and policy continuity across A2A and MCP handoffs.
- An executable oracle for cross-organizational invariants.
- A cross-framework conformance and fault-injection testbed.
- Runtime enforcement covering policy versions, exceptions, revocation, purpose, and provenance.
- Intervention-based causal validation that a repaired handoff prevents a violation.
- An evaluation that jointly reports organizational utility, compliance, security, accountability, latency, and cost.

## Research questions

### Primary research question

**RQ1:** How can organizational authority and policy constraints be represented, attenuated, transmitted, and verified across heterogeneous multi-agent and agent-tool delegation chains?

### Supporting questions

**RQ2:** Where do syntactically valid A2A and MCP interactions produce silent semantic disagreement about roles, capabilities, task states, errors, artifacts, or decision rights?

**RQ3:** Does handoff-level policy enforcement outperform prompt-only, tool-boundary-only, and centralized enforcement without unacceptable loss of legitimate task utility?

**RQ4:** How reliably do revocation and policy changes propagate through active tasks, cached plans, delegated capabilities, and pending tool calls?

**RQ5:** Can causal intervention on a suspected delegation failure distinguish the root cause from a propagation point or visible symptom?

**RQ6:** Which audit representation allows humans to assign responsibility accurately while minimizing disclosure of sensitive organizational content?

## Testable hypotheses

- **H1:** Task-scoped, purpose-bound capabilities will reduce unauthorized action and excess privilege compared with prompt-only rules and conventional role-based access control.
- **H2:** Provenance-aware handoff enforcement will reduce policy violations more than tool-boundary-only enforcement, particularly for multi-step obligations.
- **H3:** Policy versioning and active revocation will reduce stale-policy actions, although they will increase false denials and recovery latency.
- **H4:** Counterfactual repair success will disagree materially with attribution based solely on trace inspection or an LLM judge.
- **H5:** Selective trace disclosure will preserve most causal diagnostic accuracy while exposing fewer secrets than complete transcript logging.

## Proposed governance model

Each delegated task should carry a machine-verifiable governance envelope containing:

- Principal identity and organizational domain
- Delegating agent identity and role
- Delegate identity or admissible delegate class
- Permitted actions
- Explicitly prohibited actions
- Purpose and permitted data-use purpose
- Resource and financial limits
- Required approvals and separation-of-duty constraints
- Validity interval and policy version
- Delegation depth or onward-delegation rule
- Data sensitivity and disclosure restrictions
- Revocation endpoint or status reference
- Provenance reference to the originating request
- Expected artifacts and completion conditions
- Accountability and escalation contact

This is a research abstraction, not a claim that all fields must be placed directly inside an A2A or MCP message. Different implementations can pass signed references, capability tokens, policy identifiers, or side-channel metadata.

## Core organizational invariants

The evaluation oracle should check at least these properties:

1. **No authority amplification:** A delegate cannot exercise authority that the delegator did not possess or transmit.
2. **Purpose binding:** Data and tools may only be used for the authorized organizational purpose.
3. **Delegation attenuation:** Each onward delegation is equal to or narrower than its parent authorization.
4. **Separation of duties:** Roles that must remain independent cannot be silently merged by orchestration.
5. **Required approval:** Irreversible or high-risk actions cannot execute without the specified human or organizational approval.
6. **Policy-version consistency:** An action must be evaluated against the applicable policy version.
7. **Revocation safety:** Revoked authority cannot be used for new actions, including actions based on cached plans.
8. **Provenance continuity:** Every consequential action can be traced to the originating principal, policy, delegation chain, and evidence.
9. **Replay resistance:** Approval or authorization for one task cannot be reused for a different task or state.
10. **Accountable failure handling:** Violations, ambiguity, or incomplete authority trigger escalation, safe stopping, or compensation.

## Experimental design

### Testbed

Use a cross-organizational procurement workflow as the primary domain because it naturally contains budgets, suppliers, confidential information, approval thresholds, contracts, and irreversible actions. Use incident response as a secondary domain if time permits because it adds urgency, partial information, role reassignment, and temporary emergency authority.

Implement equivalent organizational roles in at least three agent frameworks, for example:

- LangGraph
- AutoGen
- CrewAI or Semantic Kernel

Connect organizational agents with A2A and expose enterprise tools through MCP. Include minimal reference implementations so framework behavior can be separated from protocol behavior.

### Organizational roles

- Human requester
- Human manager or budget owner
- Procurement agent
- Compliance or audit agent
- External broker agent
- Supplier agent
- Purchasing tool
- Catalog or enterprise data tool

### Experimental factors

- Centralized versus distributed enforcement
- Prompt-only versus RBAC/OAuth versus capability-based versus provenance-aware enforcement
- Homogeneous versus heterogeneous model providers
- Static versus changing policy
- Single organization versus cross-organization workflow
- Fixed versus risk-sensitive human escalation
- Complete versus redacted versus provenance-only trace visibility
- Native framework communication versus A2A plus MCP composition

### Baselines

1. Natural-language policy in system prompts only
2. Conventional RBAC and OAuth scopes
3. Tool-boundary policy guard
4. Centralized policy-checking agent
5. Task-scoped capability chain without provenance reasoning
6. Proposed capability and provenance-aware handoff enforcement

### Fault and attack library

- Capability inflation
- Confused-deputy request
- Agent substitution
- Malicious or compromised delegate
- Approval replay
- Stale Agent Card or tool description
- Policy change during execution
- Delayed revocation
- Conflicting organizational policies
- Missing or ambiguous exception
- Tool poisoning
- Prompt injection through tool data
- Collusion between two agents
- Message duplication, delay, loss, or reordering
- Partial tool failure after an irreversible side effect
- Incorrect upstream fact followed by reasonable downstream reliance

### Causal evaluation

For every failure, checkpoint the environment and record a structured event graph. Then replay the execution with controlled interventions:

- Replace only the suspected agent response.
- Repair only the suspected delegation envelope.
- Replace only the policy interpretation.
- Repair only the tool result.
- Remove or repair the human approval.
- Apply pairs of interventions for interacting causes.

An attribution is causally supported when the intervention changes the violation outcome while appropriate controls do not. This distinguishes causal root causes from correlated symptoms.

## Evaluation metrics

### Organizational and governance outcomes

- Policy violation rate
- Unauthorized action rate
- Excess privilege exercised
- Purpose-violation rate
- Required-approval bypass rate
- Revocation propagation time
- Stale-policy action rate
- Provenance completeness
- Responsibility attribution accuracy
- Human auditor agreement and audit time

### Task utility

- End-to-end task completion
- Process-compliant completion
- Output quality
- False denial rate
- Human escalation frequency
- Recovery success
- Compensation correctness

### Reliability and security

- Attack success rate
- Silent semantic failure rate
- Duplicate irreversible action rate
- Cascade depth and blast radius
- Time to containment
- Replay resistance
- Recovery under message and service faults

### Efficiency

- End-to-end latency, including p50 and p95
- Token and monetary cost
- Number of agent messages
- Policy-checking overhead
- Human intervention time
- Storage and trace overhead

### Causal attribution

- Agent top-1 and top-k attribution accuracy
- Decisive-step distance
- Root-cause precision and recall
- Repair success rate
- Causal necessity and sufficiency
- Minimal intervention size
- Attribution calibration

## Analysis plan

Use repeated executions because LLM systems are stochastic. A credible full paper should use at least 20 independent runs per important experimental cell or provide a power analysis supporting another number.

Recommended analysis:

- Hierarchical or mixed-effects models with workflow, framework, model, policy, and fault as factors
- Confidence intervals for all primary outcomes
- Effect sizes rather than only significance tests
- Survival or time-to-event analysis for revocation and containment
- Calibration analysis for attribution confidence
- Pareto analysis across task utility, compliance, latency, and cost
- Held-out workflows and fault types to evaluate generalization
- Ablations of capabilities, provenance, policy versioning, causal replay, and human escalation

Avoid reporting one average task-success number as the main result. MASO reviewers should be able to see the trade-off between organizational performance and governance safeguards.

## Expected contributions

1. **Theory:** A precise organizational model connecting principals, agents, roles, decision rights, delegation, policy, and responsibility.
2. **Specification:** Executable invariants for policy-preserving multi-hop delegation.
3. **Architecture:** A framework-independent enforcement approach spanning A2A agents and MCP tools.
4. **Testbed:** A reproducible cross-organizational workflow with controllable policy and delegation faults.
5. **Evaluation:** Comparative evidence across frameworks, models, policies, and enforcement strategies.
6. **Accountability method:** Intervention-validated causal attribution rather than transcript-based blame alone.
7. **Practical guidance:** Design recommendations for organizations deploying heterogeneous agent ecosystems.

## Threats to validity

### Construct validity

Authorization, responsibility, compliance, and accountability are not interchangeable. The paper must define each construct separately. Technical causality should not automatically be presented as moral or legal liability.

### Internal validity

LLM nondeterminism, provider updates, framework defaults, and judge bias can confound results. Record exact model and framework versions, preserve prompts and policy artifacts, use executable state-based oracles where possible, and report repeated-run distributions.

### External validity

A procurement testbed cannot represent all organizations. Include a second workflow or validate scenarios with practitioners. State clearly which conclusions concern protocols, organizational structures, or the selected domains.

### Ecological validity

Synthetic organizations lack informal practices, incentives, power relationships, and real consequences. A practitioner review or small human-team study would strengthen the organizational claims.

### Evaluation validity

LLM judges can exhibit position, verbosity, self-preference, and persuasive-language biases. Use deterministic policy and end-state checks for primary outcomes. Use independent human annotation for an auditability subset and report inter-rater agreement.

## Ethics and responsible research

- Use synthetic or properly anonymized organizational data.
- Do not expose live purchasing, finance, or administrative systems to autonomous experimental agents.
- Isolate adversarial tools and prompts in a sandbox.
- Clearly distinguish technical responsibility attribution from legal or moral conclusions.
- Report false denials and productivity loss, not only safety improvements.
- Document model providers, data retention, and any external API exposure.
- Release fault cases without operational credentials or directly reusable attack secrets.

MASO's call states that substantive generative-AI assistance must be disclosed and that authors remain responsible for accuracy and originality. This document is research planning material and should not be submitted unchanged. Every reference, experimental claim, and generated passage must be reviewed and verified by the authors, and assistance must be disclosed according to the venue policy.

## Reproducibility package

The artifact should contain:

- Version-pinned agent and tool containers
- A2A and MCP implementation versions
- Model identifiers and dates of access
- Complete prompts and organizational policies
- Machine-readable governance envelopes
- Workflow and policy-state snapshots
- Fault-injection schedules
- Structured traces with privacy-safe examples
- Executable outcome and policy oracles
- Repetition seeds where they affect the surrounding simulator
- Analysis scripts and raw aggregate results
- An agentic-system reproducibility card

## Recommended paper positioning

### Central claim

Local protocol authorization does not guarantee organizationally valid delegation. End-to-end policy continuity requires explicit authority attenuation, purpose binding, policy versioning, provenance, and causal auditability across agent and tool boundaries.

### Strong framing

- Organizational decision rights expressed as executable delegation invariants
- Cross-organizational agent ecosystems
- Governance enforcement across heterogeneous agents
- Human escalation and meaningful organizational control
- Causal accountability supported by controlled interventions

### Weak framing to avoid

- A generic MCP security scanner
- A generic OAuth implementation
- Another agent protocol survey
- A conceptual governance framework without implementation
- A static accuracy comparison of agent frameworks
- A logging dashboard without validated diagnostic or auditor value
- Claims that classical organizational MAS concepts are newly invented

## Likely reviewer concerns and responses

### "This is established access-control research."

Response: access control provides necessary primitives, but the study targets stochastic semantic delegation, natural-language policies, dynamic replanning, cross-protocol execution, and causal accountability. The empirical comparison must demonstrate which failures are not resolved by standard RBAC or OAuth.

### "This belongs at a security venue."

Response: frame the dependent variables around organizational decision rights, policy compliance, human control, responsibility, and cross-organizational coordination. Security attacks are stress tests of the organizational governance model.

### "The testbed is synthetic."

Response: derive workflows and policies from realistic procurement or incident processes, validate them with practitioners, and include heterogeneous frameworks and models. Make limitations explicit.

### "A2A and MCP are moving targets."

Response: version-pin all protocol implementations and treat version skew as an experimental factor. The conceptual invariants should remain protocol-independent.

### "Trace attribution is not accountability."

Response: explicitly separate technical causality, process responsibility, organizational responsibility, and legal liability. Evaluate human auditor judgments rather than equating causal origin with blame.

### "The proposal is too broad."

Response: keep procurement as the single primary domain, use four core invariants in the main experiment, and treat incident response, privacy-preserving tracing, and advanced human studies as extensions.

## Minimum viable paper and full-paper scope

### Minimum viable short paper

- Formalize four invariants: no amplification, purpose binding, approval, and provenance continuity.
- Implement one procurement workflow using two frameworks, A2A, and MCP.
- Compare prompt-only rules with capability-based enforcement.
- Evaluate four fault classes across repeated runs.
- Include preliminary causal replay for one failure class.

### Strong full paper

- Ten organizational invariants
- Three agent frameworks plus reference implementations
- Multiple open and closed models
- Static and changing policies
- Eight or more fault classes
- Complete counterfactual replay evaluation
- Human auditor subset
- Utility, compliance, security, latency, and cost analysis
- Reproducible public artifact

## Alternative titles

1. **Who Authorized This Agent? Policy-Preserving Delegation and Causal Accountability in Cross-Organizational Agentic Systems**
2. **From Access Tokens to Decision Rights: Verifiable Delegation Across Organizational Agent Ecosystems**
3. **Policy Continuity Across A2A and MCP: Governing Multi-Hop Agent Delegation in Organizations**
4. **When Agents Delegate: Authority Attenuation and Accountability Across Organizational Boundaries**
5. **Executable Organizational Governance for Heterogeneous Agentic Workflows**

The first title is the strongest for MASO because it is memorable and foregrounds the organizational accountability problem. The third is more technical and may fit SE4AgenticAI better.

## Draft abstract

Organizations are beginning to deploy heterogeneous agentic systems in which human principals delegate tasks to organizational agents, agents delegate to external agents, and downstream agents invoke enterprise tools. Existing agent and tool protocols support communication, discovery, authentication, and task execution, but they do not guarantee that organizational authority, purpose, policy, and responsibility remain intact across the full delegation chain. We study policy-preserving delegation in cross-organizational agentic workflows. We define executable invariants for authority attenuation, purpose binding, required approval, policy-version consistency, revocation, and provenance continuity. We implement these invariants across heterogeneous A2A agents and MCP tools in a reproducible procurement testbed. We compare prompt-only policies, conventional role-based authorization, tool-boundary guards, and provenance-aware capability enforcement under controlled policy conflicts, agent substitution, confused-deputy requests, replay, revocation, and communication faults. We further use checkpointed counterfactual replay to test whether an attributed agent handoff is a causal source of a violation and whether repairing it prevents recurrence. The evaluation measures process-compliant task completion, policy violations, excess privilege, revocation latency, causal repair success, human auditability, latency, and cost. The study connects classical organizational multi-agent governance with the operational realities of LLM-based agents and provides evidence and reusable infrastructure for governing agent ecosystems across organizational boundaries.

## Suggested paper outline

1. Introduction and motivating organizational failure
2. Background: organizational MAS, A2A, MCP, and policy enforcement
3. Research gap and organizational threat model
4. Delegation and governance model
5. Executable organizational invariants
6. Cross-organizational testbed and implementation
7. Experimental design and causal replay method
8. Results
9. Organizational implications
10. Threats to validity and ethical considerations
11. Related work
12. Conclusion

## Submission readiness checklist

- [ ] Confirm the precise A2A and MCP versions used.
- [ ] Verify every bibliographic entry against the publisher or official repository.
- [ ] Select the four to six primary organizational invariants.
- [ ] Freeze the procurement workflow and policy corpus.
- [ ] Define executable outcome and compliance oracles before running experiments.
- [ ] Implement at least two frameworks and one minimal reference implementation.
- [ ] Include strong RBAC, OAuth, prompt-only, and tool-guard baselines.
- [ ] Preregister primary outcomes and analysis where practical.
- [ ] Run enough repetitions to report uncertainty and flakiness.
- [ ] Include held-out faults or workflows.
- [ ] Validate causal attributions through repair interventions.
- [ ] Report false denials, latency, cost, and human burden.
- [ ] Conduct practitioner review of organizational realism.
- [ ] Prepare anonymized code and data artifacts for review.
- [ ] Add the required generative-AI assistance disclosure.
- [ ] Follow the Springer LNCS format and MASO anonymization requirements.

## Final assessment

This proposal is a 9/10 fit for MASO 2026. Its main strength is the direct integration of organizational theory and executable agent engineering. It addresses how decision rights, delegation, compliance, and responsibility operate inside a heterogeneous agent ecosystem, while providing a concrete technical artifact and empirical evaluation.

Its main risk is drifting into protocol security without sufficient organizational analysis. The paper should therefore treat A2A, MCP, capabilities, and provenance as mechanisms for answering an organizational question. Including a human decision-maker, dynamic authority, policy change, and responsibility evaluation will make the MASO contribution substantially stronger.

If the complete proposal is too large for the available time, the recommended narrower paper is:

> Do task-scoped, provenance-aware delegation capabilities reduce policy violations and authority amplification across A2A-to-MCP procurement workflows compared with prompt-only rules and conventional role-based authorization?

That question is focused, testable, strongly aligned with MASO, and capable of producing a reusable benchmark and meaningful empirical result.

## References

1. Dignum, V. et al. OperA: A model for institutional organizations. *The Knowledge Engineering Review*, 2004. https://doi.org/10.1017/S0269888904000244
2. Cuní, G. et al. Engineering open environments with electronic institutions. *Engineering Applications of Artificial Intelligence*, 2005. https://doi.org/10.1016/j.engappai.2004.11.019
3. Horling, B. and Lesser, V. A survey of multi-agent organizational paradigms. *The Knowledge Engineering Review*, 2005. https://mas.cs.umass.edu/Documents/bhorling/horling-paradigms.pdf
4. Debenedetti, E. et al. AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents. *NeurIPS Datasets and Benchmarks*, 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/97091a5177d8dc64b1da8bf3e1f6fb54-Abstract-Datasets_and_Benchmarks_Track.html
5. Vaccaro, M., Almaatouq, A., and Malone, T. When combinations of humans and AI are useful: A systematic review and meta-analysis. *Nature Human Behaviour*, 2024. https://www.nature.com/articles/s41562-024-02024-1
6. Guo, X. et al. Embodied LLM agents learn to cooperate in organized teams, 2024. https://arxiv.org/abs/2403.12482
7. Yao, S. et al. tau-bench: A benchmark for tool-agent-user interaction, 2024/2025. https://arxiv.org/abs/2406.12045
8. Cemri, M. et al. Why Do Multi-Agent LLM Systems Fail? *NeurIPS Datasets and Benchmarks*, 2025. https://papers.nips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html
9. Zhang, Y. et al. Which Agent Causes Task Failures and When? *ICML*, 2025. https://proceedings.mlr.press/v267/zhang25cq.html
10. Zhu, K. et al. MultiAgentBench: Evaluating the collaboration and competition of LLM agents. *ACL*, 2025. https://aclanthology.org/2025.acl-long.421/
11. Zwerdling, N. et al. Company policy compliance through executable tool guards. *EMNLP Industry*, 2025. https://aclanthology.org/2025.emnlp-industry.41/
12. Wu, S. et al. Human-generative AI collaboration enhances task performance but undermines human intrinsic motivation. *Scientific Reports*, 2025. https://www.nature.com/articles/s41598-025-98385-2
13. Ehtesham, A. et al. A survey of agent interoperability protocols, 2025. https://arxiv.org/abs/2505.02279
14. AgentSpec: Customizable runtime enforcement for safe and reliable LLM agents, 2025. https://arxiv.org/abs/2503.18666
15. Xiang, Y. et al. GuardAgent: Safeguard LLM agents by a guard agent via knowledge-enabled reasoning. *ICML*, 2025. https://proceedings.mlr.press/v267/xiang25a.html
16. EnterpriseBench: Can LLM agents help you at work? 2025. https://arxiv.org/abs/2510.27287
17. Chen, M. et al. Seeing the Whole Elephant: A benchmark for failure attribution in LLM-based multi-agent systems. *ACL*, 2026. https://aclanthology.org/2026.acl-long.912/
18. Predoaia, I. et al. A comparative study of MCP and A2A for inter-agent coordination in LLM-based systems, 2026. https://arxiv.org/abs/2607.23884
19. Fu, W. et al. CI-Work: Benchmarking contextual integrity in enterprise LLM agents, 2026. https://arxiv.org/abs/2604.21308
20. Han, Y. et al. Can LLM agents be CFOs? A benchmark for resource allocation in dynamic enterprise environments, 2026. https://arxiv.org/abs/2603.23638
21. Towards Verifiably Safe Tool Use for LLM Agents. *ICSE*, 2026. https://doi.org/10.1145/3786582.3786839
22. Model Context Protocol authorization specification. https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
23. Agent2Agent protocol specification. https://a2a-protocol.org/latest/specification/
24. MASO 2026 Call for Papers. https://www.maso.uno/call-for-papers.php?lang=en
