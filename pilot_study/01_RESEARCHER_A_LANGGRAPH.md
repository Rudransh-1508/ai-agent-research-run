# Researcher A: LangGraph

Framework: LangGraph. Candidate case: [LangGraph issue #8653](https://github.com/langchain-ai/langgraph/issues/8653)
(attached vs. configuration-injected checkpointers; claimed incorrect state reads in a
platform-shaped graph). Read research plan §4 and §8.1 before starting.

Work directory: `pilot_study/work/langgraph/` (create it; put your `ACCESS_LOG.md`, harness code,
and sanitized logs there). Case records go in `pilot_study/work/langgraph/cases/`.

## Hours 0-6: Access qualification

### What to install and run

1. Install `langgraph-cli` and pin the version. Try both candidate serving modes documented at
   [LangGraph local development and testing](https://docs.langchain.com/langsmith/local-dev-testing):
   - `langgraph dev` — lightweight, in-memory/local storage.
   - `langgraph up` (Docker-based) — Postgres-backed stack.
   The checkpointer bug in #8653 is specifically about attached-vs-config-injected checkpointer
   behavior, so **prefer `langgraph up`** if it's tractable in 6 hours, since that's closer to the
   production-shaped path the issue describes. If it's not tractable, run `langgraph dev` first to
   at least confirm the server and API surface, and note explicitly that this does not establish
   access to the Postgres-backed path.
2. Confirm the server starts and responds to a request from a **separate client** (a second
   terminal/process using the LangGraph SDK or plain HTTP, not an in-process Python call).
3. Task-relevant round trip suggestion: build a minimal graph with two nodes and a checkpointer
   attached both (a) directly on the compiled graph and (b) via server/platform configuration
   injection. Run the same input through both paths and record what state each reads back on a
   second turn. This is exactly the mechanism #8653 reports as diverging — so this round trip
   doubles as your Hour 0-6 "reachability" evidence per access-log §5.
4. Fill in `templates/access_log.md` as you go, saved to `pilot_study/work/langgraph/ACCESS_LOG.md`.

### What "reaching the implicated component" means here

You need evidence that your served route actually goes through LangGraph's own checkpointer
resolution logic in the server/platform path, not just that a graph with a checkpointer runs
in-process. If `langgraph dev`'s in-memory mode uses a different code path than the
Postgres-backed platform mode, say so explicitly — plan §8.1 warns that a working dev endpoint does
not establish access to a production-only mechanism.

### Hour 6 checkpoint

Post your status (qualified / partially qualified / blocked) per `00_TIMELINE_AND_ROLES.md`.

## Hours 6-12: Freeze your case(s)

Work with Researcher C to finalize which LangGraph case(s) go into the pilot (target: your share of
the ~6 total across frameworks — likely 2 for LangGraph). The primary candidate is #8653. If C's
outcome-blind sampling needs a second, unrelated LangGraph workflow, pick one based on supported
features/accessibility, not expected outcome.

For #8653, write the property contract using `templates/case_record.md` before reproducing
anything:

- Property family: **state continuity** (plan §2.2 table).
- Contract: a subsequent request should see the state the checkpointer contract says should
  persist, regardless of whether the checkpointer was attached directly or injected via
  configuration.
- Oracle: compare the state read back on turn 2 across both checkpointer-attachment methods, under
  otherwise identical configuration.

Also check what LangGraph's own existing test suite covers for checkpointer attachment (plan §10)
— note that the LangGraph docs already claim the dev server shares integration tests with
production; verify what those actually assert about this specific mechanism before assuming they
don't cover it.

## Hours 12-36: Reproduce matched embedded/served behavior

1. **Embedded condition:** invoke the compiled graph directly in-process with each checkpointer
   attachment method. Record state read-back.
2. **Served condition:** invoke the same graph through the qualified serving route (from Hours 0-6)
   with each checkpointer attachment method, from a separate client. Reset state between runs.
   Counterbalance order (don't always run "attached" before "injected").
3. Use a deterministic tool/model double for the graph's node logic where possible, so any
   divergence is attributable to checkpointer handling, not model nondeterminism (plan §9.4).
4. If you find a genuine embedded-pass/served-fail divergence, localize it: is it in state
   reconstruction, dispatch, or something else? This is your primary candidate for the "historical
   defective/corrected pair" target in the Hours 12-36 checkpoint — check whether #8653 has since
   been fixed upstream and, if so, pin both the defective and corrected revisions and reproduce
   both (this makes it a historical pair — hand this reproduction detail to Researcher B if they
   need a second historical example, but you own the LangGraph one).
5. Fill a `case_record.md` for every attempt, log every attempt to `outcome_tracker.csv`
   immediately.

## Hours 36-60: Outcome-blind workflow sample

Researcher C will assign you a subset of the outcome-blind LangGraph workflow sample. For each:

- Run local baseline tests, boundary-focused tests, and the fuller E2E reference (plan §10), using
  the same oracle across all three where possible.
- Record every attempt (including unsupported/blocked/indeterminate) in the tracker.

## Hours 60-72: Cross-check and adjudication

- Reproduce one of Researcher B's built cases end-to-end from B's `case_record.md` alone (no extra
  context from B beyond what's written down — this tests whether the record is actually
  reproducible).
- Report discrepancies to the group rather than resolving them unilaterally.
- Participate in filling out `templates/go_no_go_decision.md`.

## Watch-outs specific to LangGraph

- Don't conflate `langgraph dev`'s in-memory checkpointer with the Postgres-backed platform
  checkpointer — they may not share the exact reconstruction code path implicated by #8653.
- LangGraph's docs claim shared integration tests between dev and production servers — treat this
  as a claim to verify, not a reason to skip local-suite coverage checking.
- If Docker/Postgres setup for `langgraph up` blows past a couple hours, don't quietly keep trying
  — flag it at Hour 6 as "partially qualified" and let the team decide whether `langgraph dev`
  alone is enough to keep LangGraph in the pilot.
