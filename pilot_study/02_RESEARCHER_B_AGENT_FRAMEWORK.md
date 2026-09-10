# Researcher B: Microsoft Agent Framework + Historical Revisions

Framework: Microsoft Agent Framework. Candidate cases: [Agent Framework issue #7416](https://github.com/microsoft/agent-framework/issues/7416)
(usage metadata omitted in Foundry hosting response conversion despite existing in the native
response) and, if access allows, [Azure SDK issue #46696](https://github.com/Azure/azure-sdk-for-python/issues/46696)
(MCP on-behalf-of token exchange failing under Foundry deployment). Read research plan §4 and §8.1
before starting.

You also own the cross-framework **historical issue/fix sample** (plan §9.2, §11 Hours 12-36
target: "including a historical defective/corrected pair") — coordinate with A and C so at least
one historical pair exists somewhere in the pilot, not necessarily in your own framework if theirs
is a better fit.

Work directory: `pilot_study/work/agent-framework/`. Case records in
`pilot_study/work/agent-framework/cases/`.

## Hours 0-6: Access qualification

### What to install and run

1. Read [Microsoft hosting models](https://learn.microsoft.com/en-us/agent-framework/hosting/) and
   [Foundry hosting prerequisites](https://learn.microsoft.com/en-us/agent-framework/hosting/foundry-hosted-agent)
   in full before writing any code — this framework has multiple hosting integrations and plan §8.1
   is explicit that you must not substitute an unrelated protocol package just because it launches.
2. **Self-hosted path first.** Set up the self-hosting integration that most directly matches
   #7416's response-conversion path. Confirm server startup and a separate-client request through
   the real endpoint.
3. **Foundry-specific path only if actually accessible.** Issue #7416 is specifically about Foundry
   hosting response conversion — a self-hosted-only reproduction may not fully qualify this case.
   Attempt Foundry access (account/credential requirements per the access log), but under the
   $0-default budget cap: if it requires a paid tier or an inaccessible managed subscription, record
   it as a blocker and do NOT pay without team approval (README §6). If Foundry access is blocked,
   explicitly downgrade your claim: you can reproduce the *self-hosted* response-conversion
   behavior, but not the Foundry-managed one, and the manuscript-level distinction from plan §2.1
   (environment 2 vs. environment 3) must be preserved — don't blur this later.
4. Task-relevant round trip suggestion: run a tool call that produces native usage/accounting
   metadata, through both the embedded SDK path and the hosted response-conversion path, and
   compare whether usage fields survive.
5. Fill in `templates/access_log.md`, saved to
   `pilot_study/work/agent-framework/ACCESS_LOG.md`.

### On Azure SDK issue #46696

This is a second, MCP-token-exchange-specific case that plan §4 flags as possibly sharing
infrastructure with #7416 — "must not be counted as two independent framework ecosystems without
justification." Only pursue this as a second case if you have real budget/time after #7416 is
qualified, and if you do, explicitly check and report whether it's actually causally independent
of #7416's mechanism or just another symptom of the same underlying hosting path.

### Hour 6 checkpoint

Post your status per `00_TIMELINE_AND_ROLES.md`.

## Hours 6-12: Freeze your case(s) and the historical pair

1. Write the property contract for #7416 using `templates/case_record.md`:
   - Property family: **observability metadata** (plan §2.2 table).
   - Contract: contractually-exposed usage/accounting fields present in the native response should
     survive conversion to the hosted response.
   - Oracle: field-by-field comparison of native vs. converted response for the same call.
   - Note explicitly per plan §2.2: "missing usage information does not, by itself, establish an
     incorrect bill or a failed user task" — keep this framed as a metadata-family finding unless
     you find task-level consequences too.
2. **Historical pair:** check whether #7416 (or your LangGraph/Mastra teammates' cases) has a
   pinned defective commit and a corrected commit available. Whichever framework has the cleanest
   before/after pair becomes the pilot's historical example — coordinate with A and C rather than
   each of you independently building one. If Agent Framework has the cleanest pair, you own
   pinning both revisions and reproducing both.
3. Check existing upstream tests for the response-conversion path (plan §10) before assuming no
   coverage exists.

## Hours 12-36: Reproduce matched embedded/served behavior

1. **Embedded condition:** call the agent directly via SDK, capture the native response with usage
   fields.
2. **Served condition:** call through the qualified hosted route, capture the converted response.
3. Compare field-by-field. If usage fields are dropped, localize whether it's the conversion layer
   specifically or something upstream (dispatch, serialization).
4. If pursuing the historical pair: reproduce both the defective-revision and corrected-revision
   behavior under matched conditions, and confirm the fix actually resolves the divergence you
   observed (not just that the diff looks plausible).
5. Fill a `case_record.md` per attempt; log to `outcome_tracker.csv` immediately, including
   any Foundry-access attempts that got blocked.

## Hours 36-60: Outcome-blind workflow sample

Take your assignment from Researcher C. Run local baseline, boundary-focused, and fuller E2E test
configurations per plan §10 on each assigned Agent Framework workflow, using a consistent oracle.
Log every attempt, including non-failures.

## Hours 60-72: Cross-check and adjudication

- Reproduce one of Researcher A's built cases end-to-end from A's `case_record.md` alone.
- Report discrepancies to the group.
- Bring the historical-pair evidence and the metadata-vs-task-consequence framing into the
  go/no-go discussion — this is the case most likely to draw the "just a metadata bug" objection
  from plan §14, so be ready to state plainly whether you found task-level consequences or not.
- Participate in filling out `templates/go_no_go_decision.md`.

## Watch-outs specific to Agent Framework

- Do not let a working self-hosted reproduction get described as a Foundry-managed-cloud finding.
  Name the exact hosting mode in every record (plan §2.1, §14).
- #7416 and #46696 may share infrastructure — don't silently count them as two independent
  ecosystems in any cross-framework tally.
- If Foundry access requires payment or an inaccessible subscription, that is a clean access
  blocker to record, not a reason to fabricate a substitute identity/context locally (plan §4
  explicitly calls this out for the Azure SDK case: "a locally fabricated identity context cannot
  validate this cloud-specific claim").
