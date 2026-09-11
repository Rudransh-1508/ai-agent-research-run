# Sampling Rules (frozen Hours 6-12)

Owner: Researcher C. Written before any additional case selection beyond the plan's own leads, per
plan §9.2 and `03_RESEARCHER_C_MASTRA_AND_COORDINATION.md` §6-12.

## Historical issue/fix sample

- Date window: issues/PRs authored or merged on or before 2026-09-10 (the research plan's
  preparation date) — no forward-looking search for newer leads was run in this pass; a fresh
  search is still owed before the Hours 60-72 prior-art recheck.
- Repositories in scope: `langchain-ai/langgraph`, `microsoft/agent-framework`,
  `mastra-ai/mastra`, plus `Azure/azure-sdk-for-python` only insofar as it's tied to Agent
  Framework's Foundry case (plan §4 explicit caveat: may share infrastructure with #7416, not an
  independent ecosystem).
- Search terms used so far: none run independently in this pass — all four candidates below are
  carried from the research plan's own motivating-evidence table (plan §4), which is not itself an
  independent search result. A fresh keyword search (terms like "context lost", "usage omitted",
  "caller identity", "checkpointer" scoped per-repo) is still owed before treating six candidates as
  final.
- Inclusion rule: an issue or PR describes a behavior difference between embedded/local and
  served/deployed execution (or, for historical fix pairs, a defective/corrected pair of the same
  mechanism), with enough detail to write a testable contract per plan §2.2's property families.

### Candidates (from plan §4) and status

| Candidate | Framework | Status |
|---|---|---|
| [LangGraph #8653](https://github.com/langchain-ai/langgraph/issues/8653) | LangGraph | **Worked — see `pilot_study/work/langgraph/cases/langgraph-checkpointer-01/case_record.md`.** Real, consequential library defect (data loss), verified with an unmerged candidate fix (PR #8828). But the actual accessible `langgraph dev` server does NOT reproduce it — `langgraph_api` always re-attaches the checkpointer server-side, sidestepping the bug. Outcome: embedded pass / served pass through the accessible route; the claimed Platform-specific failure is unconfirmed, not refuted (no managed-Platform access). See case record §7. |
| [LangGraph #8448](https://github.com/langchain-ai/langgraph/issues/8448) | LangGraph | **Worked — see `pilot_study/work/langgraph/cases/langgraph-postgres-delta-pagination-02/case_record.md`.** Found via #8653's own "possibly related" cross-reference, not the original plan §4 leads. Genuine embedded-pass/served-fail (real Postgres backend) — first clean, consequential, mode-dependent case across the whole pilot so far. `langgraph up` itself access-blocked (needs a LangSmith/license key); reproduced instead via direct calls against real Postgres, the same backend package `langgraph up` uses. |
| [Agent Framework #7416](https://github.com/microsoft/agent-framework/issues/7416) | Microsoft Agent Framework | Not yet worked (Researcher B, not started as of 2026-09-11) |
| [Azure SDK #46696](https://github.com/Azure/azure-sdk-for-python/issues/46696) | Agent Framework (shared infra) | Not yet worked; plan flags possible non-independence from #7416 |
| [Mastra #20741](https://github.com/mastra-ai/mastra/pull/20741) + [#20748](https://github.com/mastra-ai/mastra/pull/20748) | Mastra | **Worked — see `pilot_study/work/mastra/cases/mastra-request-context-01/case_record.md`.** Combined into one contract (verified via fresh diff read: #20748 is the second half of #20741's fix, not an independent bug — see case record §1). Turned out to be an internal defect, not mode-dependent (embedded == served) — see case record §7. |
| [Mastra #22734](https://github.com/mastra-ai/mastra/pull/22734) (fixes [#21941](https://github.com/mastra-ai/mastra/issues/21941)) | Mastra | **Worked — see `pilot_study/work/mastra/cases/mastra-dev-environment-tag-02/case_record.md`.** Found via a targeted search (not in the original plan §4 leads) specifically for a mode-dependent Mastra case, since #20741/#20748 wasn't one. Produces a genuine embedded-pass/served-fail→served-pass pattern; still metadata-only (observability tag), not consequential — see case record §7. |

This gives one worked case so far, short of the ~6-candidate target in plan §11 (6-12h row). The
remaining candidates are gated on A and B qualifying LangGraph and Agent Framework access, which
had not started as of this writing.

### Explicit exclusions

- None yet — no candidate has been considered and rejected. (Distinct from "not yet worked": every
  row above is still in scope, just not yet actioned by its owner.)

## Official workflow sample (outcome-blind, for Hours 36-60)

Not yet selected — this rule must be written and frozen *before* any workflow is run (plan §9.2:
"freeze the selection list before any workflow is run"). Placeholder rule, to be finalized once at
least two frameworks are access-qualified (Hour 6 gate):

- Select workflows by supported features and accessibility, not by expected failure.
- Target: 8 attempted workflows total, aim for ≥6 interpretable, split roughly evenly across
  qualified frameworks.
- Keep every attempted case in the accounting, including setup-blocked or oracle-indeterminate
  ones.

## Upstream test coverage notes (plan §10)

- Mastra / `mastra-request-context-01`: see case record §9 — the pre-fix test suite had no
  coverage of the `processSubscribedThreadStream` approval-chunk context path at all; #20741 added
  the first coverage for it. Recorded so the eventual manuscript doesn't conflate "boundary test
  found this" with "we just added a stronger assertion" (plan §10) — in this case neither framing
  applies cleanly: an *embedded* test added the first coverage.
