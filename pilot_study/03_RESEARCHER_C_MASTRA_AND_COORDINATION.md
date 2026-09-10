# Researcher C: Mastra + Sampling, Contracts, Oracles, and Cross-Framework Coordination

You have two jobs: (1) qualify and work the Mastra framework yourself, and (2) run the
cross-framework sampling, contract-design, oracle-design, and analysis-coordination role that plan
§16 assigns to "C" ("coordinates writing... independently adjudicate proposed failures"). In a
3-person team this role carries more weight than A's or B's — budget your time accordingly, and
lean on A and B for execution help on Mastra itself if the coordination load gets heavy.

Candidate case: [Mastra PR #20741](https://github.com/mastra-ai/mastra/pull/20741) with follow-up
[#20748](https://github.com/mastra-ai/mastra/pull/20748) (caller-context preservation, with a
follow-up about tests bypassing public wiring). Read research plan §4 and §8.1. Note the plan's
explicit caveat: the #20748 follow-up could not be refetched during plan preparation, so **your
first task on this case is to actually read both PRs fresh** before trusting the plan's summary of
them.

Work directory: `pilot_study/work/mastra/` for your own framework work, and
`pilot_study/work/coordination/` for cross-cutting sampling/analysis artifacts.

## Hours 0-6: Mastra access qualification

1. Read the [Mastra server description and build/start route](https://mastra.ai/blog/announcing-mastra-platform).
   Note that the older client-doc URL referenced in earlier reviews now 404s — use the source
   above and verify version-specific setup by actually running it, not by trusting any cached doc
   summary.
2. Pin the supported Mastra CLI/package commands and versions. Build and start the official server
   (`mastra build` / `mastra start` or current equivalents — confirm exact command names against
   installed CLI help, since docs may drift).
3. Confirm a separate-client request through the real server endpoint.
4. Task-relevant round trip: re-read PR #20741's actual diff and tests, then construct a call that
   exercises the caller-context preservation path it touches — ideally the exact subscription/tool
   wiring the PR discusses — through the official server route, not a direct method call.
5. Fill in `templates/access_log.md` → `pilot_study/work/mastra/ACCESS_LOG.md`.
6. Managed-platform behavior (if Mastra has one distinct from the self-built server) is a separate
   condition per plan §8.1 — don't conflate it with the self-hosted build/start route unless you
   actually exercise it.

Post your Hour 6 status per `00_TIMELINE_AND_ROLES.md`, and tally A's and B's statuses too since
you own the Hour 6 go/no-go arithmetic (≥2 of 3 frameworks qualified → proceed).

## Hours 6-12: Sampling design and contract freeze (cross-framework, your lead)

This is your primary coordination block.

### 1. Freeze the historical issue/fix sample rules

Before anyone selects cases, write down (in `pilot_study/work/coordination/sampling_rules.md`):

- Date window for the search.
- Repositories in scope (LangGraph, Microsoft Agent Framework, Mastra, plus Azure SDK only insofar
  as it's tied to Agent Framework's Foundry case).
- Search terms used.
- Inclusion rules (e.g., "issue or PR describing a behavior difference between embedded/local and
  served/deployed execution, with enough detail to write a testable contract").

Apply these rules to select ~6 candidate issue cases total across A's, B's, and your own framework
(reference: #8653 for LangGraph, #7416 and optionally #46696 for Agent Framework, #20741/#20748 for
Mastra). Record explicit exclusions for anything considered and rejected.

### 2. Write your own Mastra contract

Using `templates/case_record.md`:
- Property family: **request context** (plan §2.2 table) — caller-specific context reaching a tool
  after server dispatch.
- Contract: derive from what #20741 actually implements/asserts (re-read it fresh, don't take the
  plan's summary as final).
- Oracle: synthetic identity marker + tool-side record comparison, per plan §2.2.

### 3. Design the outcome-blind official-workflow sampling plan

Write the rule for selecting official workflows for Hours 36-60 in
`pilot_study/work/coordination/sampling_rules.md`:

- Select by supported features and accessibility, **not** by expected failure.
- Freeze the selection list before any workflow is run.
- Keep every attempted case in the accounting even if setup-blocked or oracle-indeterminate.
- Target: 8 attempted workflows, aim for ≥6 interpretable, split across A's, B's, and your own
  qualified frameworks roughly evenly.

Hand each of A and B their workflow assignments once the list is frozen.

### 4. Check upstream-test coverage across all three frameworks

For each of the ~6 candidate cases, note (in the corresponding `case_record.md`, section 2) what
the framework's own existing test suite already asserts, so the team can later distinguish
"boundary-focused test found something new" from "we just added a stronger assertion" (plan §10).

## Hours 12-36: Your own Mastra reproduction + supporting A/B

1. Reproduce the #20741 caller-context case: embedded vs. served, matched configuration, state
   reset between runs, deterministic tool double first.
2. If #20748 turns out (on fresh reading) to describe tests bypassing public wiring rather than a
   behavior fix, treat this as evidence about **upstream test coverage**, not as a second bug case
   — fold it into your Hours 6-12 coverage notes instead of trying to force it into a second
   contract.
3. Spot-check A's and B's in-progress `case_record.md` files for contract clarity and drifting
   scope — flag issues early, don't wait until Hours 60-72 adjudication to raise a concern about a
   contract that was loosened mid-flight.

## Hours 36-60: Outcome-blind sample execution + running tally

1. Execute your own assigned Mastra workflows across the three test configurations (plan §10).
2. Own the live `outcome_tracker.csv` — check at least twice during this block that A's and B's
   entries are landing, not just your own. This tracker is what makes the Hour 60-72 accounting
   possible without reconstruction from memory (plan §12).
3. Begin drafting the discovery/validation split for any test-selection rule: freeze which cases
   are "discovery" (used to derive the rule) vs. "validation"/held-out (used to check it), keeping
   variants of the same root-cause mechanism in the same partition (plan §10).

## Hours 60-72: Independent adjudication, prior-art recheck, and decision draft

This is your heaviest block.

1. **Independent adjudication:** for every case where A or B marked the failure cause as anything
   other than obviously "confirmed implementation defect," you adjudicate it independently using
   the case record's raw evidence, not their conclusion. Fill in `case_record.md` §8 yourself for
   those cases.
2. **Prior-art recheck:** re-read the closest-work comparisons in plan §5 against what was actually
   found across all three frameworks. Ask specifically: does any completed pilot result change an
   engineering decision the existing literature doesn't already answer? Do a quick search for
   anything newly published since the plan's 2026-09-10 preparation date.
3. **Accounting:** pull the final attempted/eligible/excluded/interpretable counts from
   `outcome_tracker.csv` for `go_no_go_decision.md` §4.
4. **Draft the decision doc:** fill `templates/go_no_go_decision.md` with A and B, but you own
   producing the first draft of each section from the actual evidence on file, for the group to
   correct rather than write from scratch.

## Watch-outs specific to Mastra / your coordination role

- Don't let the sampling and contract work slip because Mastra's own access setup is easy — the
  coordination role is the harder half of your job in a 3-person team.
- Re-verify the #20748 follow-up firsthand; the research plan flags it as unrefetched and its
  interpretation as carried from an earlier review, not independently rechecked.
- When adjudicating A's or B's cases, use only what's written in their `case_record.md` plus raw
  logs — if you need to ask them clarifying questions to adjudicate, that's a signal the record
  itself is incomplete and should be fixed, not just explained verbally.
