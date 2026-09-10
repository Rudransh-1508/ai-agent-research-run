# Pilot Study: Testing the Deployment Boundary of Agent Frameworks

**Status:** Not started. This folder is the operational implementation of the research plan in
[`SE4AgenticAI/DEPLOYMENT_BOUNDARY_RESEARCH_PLAN_2026-09-10.md`](../SE4AgenticAI/DEPLOYMENT_BOUNDARY_RESEARCH_PLAN_2026-09-10.md).
That document is the source of truth for *why* we are doing this and what counts as a valid result.
This folder is the source of truth for *who does what, in what order, with what commands, and
recorded where*.

If anything here conflicts with the research plan, the research plan wins. This folder should be
updated to match it, not the other way around.

## What this pilot is and is not

- It is a 72-hour, three-person effort to answer one question: **can we get real serving access to
  at least two agent frameworks, and does that access reveal at least one substantive,
  causally-explained, mode-dependent behavior difference worth building a full study around?**
- It is **not** the main study. No paper claim, sample-size justification, or acceptance argument
  should be drawn from pilot output alone.
- It is **not** an automated pipeline. No agents, cron jobs, or scripts should be launched to
  "run the pilot." Three humans do this work by hand, with scripts only as lightweight aids
  (harness code, log parsers), per the global instruction to avoid building automation machinery
  for one-off work.
- No paid inference, cloud account creation, or infrastructure spend happens without an agreed
  budget cap (Section 6 of this README) and explicit go-ahead. Free/local tiers only until that
  cap is agreed.

## Folder contents

| File | Purpose |
|---|---|
| `00_TIMELINE_AND_ROLES.md` | The 72-hour schedule, the three-person role split, cross-check assignments, and the go/no-go decision rules. Read this first. |
| `01_RESEARCHER_A_LANGGRAPH.md` | Full implementation guide for Researcher A: LangGraph access, qualification, and case reproduction. |
| `02_RESEARCHER_B_AGENT_FRAMEWORK.md` | Full implementation guide for Researcher B: Microsoft Agent Framework access, qualification, and historical-revision cases. |
| `03_RESEARCHER_C_MASTRA_AND_COORDINATION.md` | Full implementation guide for Researcher C: Mastra access and qualification, plus sampling, contract-writing, oracle design, and analysis coordination across all three frameworks. |
| `templates/access_log.md` | Per-framework template for recording the Hour 0-6 access evidence required by the research plan (Section 8.2). |
| `templates/case_record.md` | Per-case template for recording a workflow-property pair: contract, embedded result, served result, causal note, adjudication. |
| `templates/outcome_tracker.csv` | Running spreadsheet-style log of every attempted case (attempted/eligible/excluded/interpretable), so nothing gets silently dropped. |
| `templates/go_no_go_decision.md` | Template for the Hour 60-72 written go/no-go judgment, filled in collaboratively by all three researchers. |

## 1. Prerequisites before Hour 0

Confirm all three before anyone starts the clock:

1. Each researcher has a local dev machine with Python 3.11+, Node.js 20+, Docker (for LangGraph's
   Postgres-backed mode and Mastra's built server), and git.
2. Each researcher has their own scratch repo or branch to avoid interfering with each other's
   environment setup. Suggested: a `pilot/<framework>` branch or subfolder per researcher under
   this repo, e.g. `pilot_study/work/langgraph/`, `pilot_study/work/agent-framework/`,
   `pilot_study/work/mastra/` (create these as you start; they are not pre-created here since they
   will hold each researcher's actual harness code and logs, not planning docs).
3. Everyone has read the research plan end to end, especially Section 2 (what counts as embedded
   vs. served), Section 8 (access gate), Section 9.5 (outcome classification), and Section 14
   (reviewer objections) — these define what "done" looks like for each piece of work.
4. Agree on the budget cap (Section 6 below) and who holds payment authority, even if the expected
   spend is $0 for the pilot.
5. Agree on a shared, low-friction way to post evidence as you go (a shared doc thread, a Slack
   channel, or just committing to `pilot_study/work/<name>/` frequently) so the Hour 6 and Hour 36
   checkpoints in `00_TIMELINE_AND_ROLES.md` are not a surprise.

## 2. How to use the case and access templates

- Copy `templates/access_log.md` into your own `pilot_study/work/<framework>/ACCESS_LOG.md` at the
  start of Hour 0 and fill it in live as you go, not retroactively at Hour 6.
- Copy `templates/case_record.md` once per workflow-property pair you attempt, whether it succeeds,
  fails, or gets excluded. Every attempt gets a record — this is what keeps the study honest per
  plan Section 9.5 and 12.
- Every researcher appends every attempt (including excluded/setup-blocked ones) to the shared
  `templates/outcome_tracker.csv` so Researcher C can produce the Section 12 accounting without
  reconstructing history from memory at the end.

## 3. Non-negotiable rules carried over from the research plan

These are restated here because they are the most common ways a pilot silently becomes invalid.
Full reasoning is in the linked sections of the research plan.

- **Never substitute a hand-written HTTP wrapper for the official serving entrypoint.** If the
  official route is not reachable, that is an access failure to record, not a workaround to build.
  (Plan §2.1, §8.3)
- **Never let an embedded run's side effects become the served run's starting state.** Reset state
  between conditions. (Plan §9.3)
- **A crash from a missing environment variable is a setup issue, not a framework defect**, until
  correct setup is confirmed. (Plan §9.3)
- **Do not claim managed-cloud (e.g., Foundry-hosted) conclusions from a self-hosted run.** Name the
  exact serving mode you actually exercised. (Plan §2.1, §8.3, §14)
- **Label historical issue/fix cases as historical**, pinned to defective and corrected revisions.
  Do not imply current-release presence without checking. (Plan §4, §9.2)
- **Record successes, not just failures.** An outcome-blind sample loses its meaning if only
  failing cases get written up. (Plan §9.5, §12)
- **Do not optimize which cases to keep after seeing results.** Freeze inclusion rules before
  running the outcome-blind sample. (Plan §9.2, §12)

## 4. Decision gates (see `00_TIMELINE_AND_ROLES.md` for full detail)

- **Hour 6:** proceed only if at least 2 of the 3 frameworks have a qualified, relevant serving
  path. If fewer than 2 qualify, stop the cross-framework pilot and escalate to the MCP-study
  fallback gate (not covered by this folder; see the research plan §18).
- **Hour 60-72:** all three researchers jointly produce the go/no-go judgment using
  `templates/go_no_go_decision.md`, checking it against the "substantive pilot pass" criteria in
  plan §11.1 and the "stop or reassess" triggers in §11.2.

## 5. Roles at a glance

| Researcher | Framework | Also owns |
|---|---|---|
| A | LangGraph (`langgraph dev` / `langgraph up`) | Cross-checks one of B's reproduced cases |
| B | Microsoft Agent Framework (self-hosted; Foundry only if access is actually available) | Historical issue/fix revisions across all frameworks; cross-checks one of A's reproduced cases |
| C | Mastra (built server / official route) | Sampling design, property contracts, oracle design, outcome-blind case selection, independent adjudication of ambiguous cases from A and B, running the outcome tracker, drafting the Hour 60-72 decision doc |

Full task-by-task breakdown is in `00_TIMELINE_AND_ROLES.md` and each researcher's own file.

## 6. Budget cap

**Default: $0.** The pilot is scoped to run entirely on free tiers, local Docker containers, and
existing API credits the team already holds for other work. If a researcher hits a paywall
(a required paid tier, a metered API key with no free quota, a cloud trial that needs a credit
card), **stop and record it as an access blocker** in the access log rather than paying. Bring it
back to the team for an explicit, separately agreed budget decision before spending anything. This
mirrors research plan §16: "A budget cap must be agreed before paid execution; this document
authorizes no spending or account creation."
