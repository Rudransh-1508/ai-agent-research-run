# Pilot pass design

## Objective

Bring the deployment-boundary pilot to a genuine substantive pass under
`agent-icse/se4agenticai-exploration/DEPLOYMENT_BOUNDARY_RESEARCH_PLAN_2026-09-10.md` section 11.1.
The work must produce new, auditable evidence rather than weaken or relabel the
gate.

## Scope

The work covers four linked deliverables:

1. Repair and validate the response-capture oracle and artifact metadata.
2. Complete the matched Agent Framework control for the remaining system-message
   difference, using real API calls and clean package environments.
3. Obtain a consequential, faithfully matched embedded-versus-official-serving
   case in a second framework, with a distinct mechanism.
4. Run a frozen outcome-blind sample, perform independent reproduction from the
   written record, and publish a gate-based go/no-go decision.

If serving access or a qualifying second-framework case is genuinely unavailable,
the records must state that blocker and the pilot must remain not-passed. Existing
cases must not be upgraded by changing their definitions after observing results.

## Evidence integrity

The capture format will require, for every response record:

- HTTP status code;
- parser/instrumentation revision;
- response ID or an explicit valid-error marker;
- extracted function-call items;
- the parent continuation ID used by the request.

Ancestry traversal will return `inconclusive` when a referenced parent response
is absent. Synthetic tests will cover missing parents, capture failures,
unrelated chains, valid 4xx responses, and confirmed duplicates.

All existing Agent Framework matrix runs will be regenerated from clean,
version-pinned environments. Historical artifacts will be retained only when
their instrumentation revision is explicit and their oracle status is
conclusive.

## Agent Framework control

The raw-replay experiment will add a control that supplies
`AgentSession(service_session_id=...)` together with the same explicit replay
history, tool, instructions, streaming mode, tool choice, and continuation ID.
The control must demonstrate from captured requests that the extra system item
is removed while the defective package still preserves the replayed function
call ID. Both package versions must be run through embedded and official served
paths. The result must be checked by the same oracle and independently rerun
from the written protocol.

## Second-framework qualification

LangGraph and Mastra will be screened against the same requirements:

- official, reachable HTTP serving entrypoint;
- identical application contract across embedded and served conditions;
- a real persistence, serialization, dispatch, or reconstruction boundary;
- consequential outcome oracle, not metadata alone;
- reproduced defective and corrected behavior where a correction exists;
- no direct-SDK-versus-storage substitution or reconstructed-only correction.

The selected case will be documented before its outcome is examined. Real model
or downstream API calls will be used only when needed to establish the
consequence, with secrets excluded from logs and artifacts.

## Outcome-blind and held-out evidence

The workflow sample and inclusion rules will be frozen before execution. The
sample will include successful outcomes, attempted and excluded cases, and
explicit denominators. Variants of one defect family will stay in one partition.
The held-out plan will specify the boundary-focused test policy, fuller E2E
reference, oracle, benefit criterion, and clustering unit before results are
interpreted.

## Acceptance criteria

The pilot is marked passed only if all section 11.1 conditions are evidenced:

- relevant serving access in at least two frameworks;
- consequential matched differences in at least two frameworks;
- more than one root-cause mechanism, including evidence beyond persistence or
  resume semantics;
- valid contracts with trivial configuration, version, and oracle errors
  excluded;
- a concrete incremental testing decision;
- feasible held-out evaluation and completion path.

The final report will distinguish discovery evidence, historical issue evidence,
outcome-blind evidence, and independent reproduction. It will not use repeated
runs or multiple properties from one workflow as independent framework cases.
