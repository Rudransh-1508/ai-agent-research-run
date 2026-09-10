# Pilot Timeline and Roles

Source: research plan §11 (the 72-hour pilot table), §16 (team/resources), §8.2-8.3 (access gate).
This document turns those into concrete per-person, per-hour-block assignments for a 3-person team.

Clock starts when all three researchers have read the prerequisites in `README.md` and are ready
to begin work simultaneously. Do not stagger start times across researchers — the Hour 6 gate
depends on all three having spent comparable effort.

## Team

| Researcher | Owns | File |
|---|---|---|
| **A** | LangGraph | `01_RESEARCHER_A_LANGGRAPH.md` |
| **B** | Microsoft Agent Framework, historical revisions across frameworks | `02_RESEARCHER_B_AGENT_FRAMEWORK.md` |
| **C** | Mastra, sampling/contracts/oracles, cross-framework analysis coordination | `03_RESEARCHER_C_MASTRA_AND_COORDINATION.md` |

Since this is a 3-person team (not 4), there is no dedicated 4th "reproducibility and manuscript
integration" role from plan §16 — C absorbs sampling/analysis/coordination, and manuscript work is
deferred entirely until after the pilot passes (see `templates/go_no_go_decision.md`).

## Hour-by-hour plan

### Hours 0-6: Access and relevant-path qualification (all three, in parallel)

Each researcher works **only on their own framework** during this block. Goal: get past
"documentation exists" to "I ran a real client against a real official serving route and it
touched the component implicated by a candidate case."

Required output per researcher, logged in their own `ACCESS_LOG.md` (from
`templates/access_log.md`):

1. Exact package/runtime versions and the exact serving mode used (name it precisely — e.g.
   "`langgraph dev`, in-memory checkpointer" vs. "`langgraph up`, Postgres-backed").
2. Account/credential/permission requirements — record that they exist and were satisfied, never
   the secret values themselves.
3. Evidence of a successful server startup and a request from a **separate client process** through
   the real network endpoint (not an in-process call).
4. One task-relevant feature round trip beyond hello-world (see each researcher's file for a
   concrete suggested probe).
5. Evidence that the exercised route reaches the component implicated by that framework's
   candidate case from research plan §4 (e.g., for LangGraph, the checkpointer path from issue
   #8653; for Agent Framework, the Foundry hosting response-conversion path from issue #7416; for
   Mastra, the caller-context wiring from PR #20741/#20748).
6. Reproduction commands, sanitized logs (no secrets), startup time, and any unresolved limitation.

**Checkpoint at Hour 6:** all three researchers post their access log status (qualified / partially
qualified / blocked) to the shared channel. Researcher C tallies the result.

- **If 2 or 3 frameworks qualify:** proceed to Hours 6-12.
- **If fewer than 2 qualify:** stop the cross-framework pilot. Do not extend the access window
  informally. Escalate to the team for the MCP-study fallback decision (research plan §18) — this
  is outside the scope of this folder.
- A framework can also be excluded cleanly (e.g., it depends on an inaccessible managed service)
  without burning the whole pilot — record the exclusion and, if another accessible case in the
  same framework exists, swap to it rather than silently dropping the framework. (Plan §8.3.)

### Hours 6-12: Freeze pilot cases, contracts, and upstream-test evidence (all three, joint)

- Researcher C leads: for each qualified framework, select ~2 candidate issue cases (aiming for
  ~6 total across the accessible frameworks) using the inclusion rules in
  `03_RESEARCHER_C_MASTRA_AND_COORDINATION.md`.
- A and B each review the candidate cases for their own framework and confirm the case is
  reachable given what was actually qualified in Hours 0-6 (not just documented as reachable).
- For every case selected, write the property contract using `templates/case_record.md`'s contract
  section before any reproduction work starts. Contracts are frozen once written — do not loosen a
  contract because a result "almost" satisfies it.
- Record explicit exclusions (candidate cases considered and rejected) with reasons. An exclusion
  is not a failure of the pilot; a silently dropped case is.
- Check what the framework's own existing test suite already covers for each candidate case (plan
  §10 — this is needed later to distinguish "boundary tests found this" from "we just asserted
  something the local suite never checked").

**Checkpoint:** by Hour 12, every selected case has a filled-in contract and a "reachable given
Hour 0-6 access" confirmation from its framework's owner.

### Hours 12-36: Reproduce matched embedded/served behavior (A and B primarily, C supporting)

- A and B each work their own framework's cases: run the embedded condition, then the served
  condition, through the actual qualified route from Hours 0-6, with state reset between runs and
  execution order counterbalanced where shared dependencies could matter (plan §9.3).
- Target: 4 tractable case pairs total across the two/three frameworks, including at least one
  historical defective/corrected pair (owned by B — see `02_RESEARCHER_B_AGENT_FRAMEWORK.md`).
- Use deterministic model/tool doubles first; only add a live-model confirmation run for
  representative cases if needed to establish realism, and report the two separately (plan §9.4).
- Every attempt — pass, fail, or blocked — gets a `case_record.md` and a row in
  `outcome_tracker.csv`, appended live, not batched at the end.
- C spot-checks in-progress records for contract clarity, not for outcome-correctness yet (that's
  Hours 60-72's adjudication step) — the goal here is catching ambiguous or drifting contracts
  early.

**Checkpoint:** by Hour 36, at least one causal case (valid contract, embedded pass, served fail,
localized divergence) should exist, or the team should already see that this target is at risk and
say so rather than quietly running past the block.

### Hours 36-60: Outcome-blind official-workflow sample and test-configuration comparison (all three)

- C runs the outcome-blind sampling process (select workflows by supported features/accessibility,
  not by expected failure) and hands assignments to A and B.
- A and B execute assigned workflows against all three test configurations from plan §10: local
  baseline, boundary-focused tests, fuller E2E reference — using the same oracle across
  configurations for a given case.
- Target: 8 attempted workflows, at least 6 interpretable pairs. Every attempt (including
  unsupported/setup-blocked/oracle-indeterminate) goes in the outcome tracker (plan §9.5).
- C begins assembling the discovery/validation split for any test-selection rule, keeping variants
  of the same root cause together in one partition (plan §10).

**Checkpoint:** by Hour 60, the outcome tracker should reflect every attempt from Hours 12-60 with
no gaps, and C should be able to produce the plan §12 accounting (attempted/eligible/
excluded/interpretable) directly from it.

### Hours 60-72: Independent review, prior-art recheck, and go/no-go (all three, joint)

- Cross-checks: A reproduces one of B's built cases end-to-end from B's record; B reproduces one of
  A's. Discrepancies get resolved by discussion, not by whoever built the case originally
  overruling the reviewer.
- C independently adjudicates any case where the failure cause is ambiguous (implementation defect
  vs. intended difference vs. configuration mistake vs. model-dependent variation vs. unresolved —
  plan §9.5).
- C does a quick recheck of the closest-prior-work table (plan §5) against whatever was actually
  found, specifically asking: does anything we found change an engineering decision that the
  existing literature didn't already answer? Not just "does another paper share our title."
- All three jointly fill out `templates/go_no_go_decision.md` against the criteria in plan §11.1
  (substantive pilot pass) and §11.2 (stop or reassess triggers).

**Final output of the pilot:** a filled `go_no_go_decision.md`, a complete `outcome_tracker.csv`,
and a `case_record.md` for every attempted case, committed to
`pilot_study/work/<researcher>/`. This is the entire deliverable of the pilot — no manuscript
work happens until this passes.

## Escalation rule

If any researcher is blocked for more than ~2 hours on something outside their control (e.g.,
credential provisioning, a broken official doc, a flaky Docker image), say so immediately rather
than silently burning the timeline — the whole point of time-boxing access is to fail fast on
access, not to quietly extend it.
