# Case Record: agent-framework-agui-resume-02

Researcher: B (executed on their behalf per team request)
Framework: Microsoft Agent Framework
Sample type: historical issue/fix (open, no merged fix yet — see §1)
Date: 2026-09-11

## 1. Provenance

- Source: [Agent Framework issue #8140](https://github.com/microsoft/agent-framework/issues/8140), "AG-UI resume duplicates the interrupted turn when the client replays its transcript" (Python), labeled `reproduced`. Candidate fix: [PR #8149](https://github.com/microsoft/agent-framework/pull/8149), "fix(ag-ui): dedupe client-replayed transcripts on resume" — **unmerged** as of this record. Same "open issue + unmerged candidate fix" situation as LangGraph's #8653.
- Found via a targeted search for a second Agent Framework candidate that is both mode-dependent and consequential — #7416 (already in the pilot) is mode-dependent but metadata-only.
- Package: `agent-framework-ag-ui`. Verified the defect is present in the **current latest release**, `1.3.0` (published 2026-09-10) — downloaded the wheel directly and confirmed `_snapshot_session.py`'s `resume_seeded_messages` still does the naive, unguarded concatenation the issue describes (no `if not incoming:` guard, which PR #8149 would add). No released version contains the fix; this is a currently-live defect in the newest available package, not a stale historical one.
- Verification method: read the issue's own exact code excerpts and line references against the actually-installed `1.3.0` package (not trusted as quoted) — confirmed at `agent_framework_ag_ui/_agent_run.py:2618` that the resume branch calls `snapshot_session.resume_seeded_messages(raw_messages)` (the naive path), while the sibling "client re-sent history" branch at line 2627 calls `_reconstruct_messages_from_thread_snapshot` (the reconciler) — both line numbers and function names matched what the issue reported at a slightly earlier commit, confirming the defect persists unchanged.

## 2. Property contract (freeze before running)

- Property family: **state continuity** (plan §2.2 table), with an **approval behavior** consequence (plan §2.2: "An action requiring approval does not execute before approval, and executes under the intended context afterward") — this case sits across both families and is recorded as such rather than forced into one.
- Contract: resuming a run with a client-replayed transcript that already overlaps the server's stored thread snapshot must not duplicate any message in the persisted snapshot. A tool call that has already run and been approved must not reappear in a state that a client would render as "awaiting approval."
- Evidence to inspect: the message list returned by the resume-seeding step, keyed by message id, checked for duplicate ids.
- Oracle: `pass = all(count == 1 for count in messages_grouped_by_id.values())` — any id appearing more than once is a contract violation, since it means the same logical message was persisted twice.

## 3. Configuration pairing

- Application code: identical synthetic stored-snapshot and client-replayed-transcript fixtures (`repro/agui_resume_dedup_repro.py`) used for both the defective and corrected code paths.
- Framework/dependency versions: `agent-framework-ag-ui==1.3.0` (current latest, unpatched) throughout — both the defective and corrected *functions* already exist side by side in this single installed version (see §1), so no version-swapping or patching was needed to compare them, unlike the other cases in this pilot.
- Initial state: fresh `AGUIThreadSnapshot`/`ThreadSnapshotSession` objects constructed per call, no shared state between the two function calls.
- Caller identity/permissions: n/a for this specific isolation (the approval-reopening consequence is described qualitatively from the issue's own report, not independently re-verified end-to-end through a full server — see §7 for the scope of what was and wasn't verified).
- Tool fixtures: the stored snapshot's assistant message includes a synthetic pending tool call (`transfer_funds`), matching the issue's own reproduction scenario (a tool requiring approval), though its downstream approval-UI consequence was not independently re-run through a live server.
- Model configuration: n/a — no model call anywhere in this test; it operates entirely on the message-list data structures the resume path manipulates.

## 4. Embedded execution

- **No embedded condition exists for this defect, and this is stated as a finding, not a gap.** "Resume with a client-replayed transcript" is a hosted-protocol concept: it requires a server-persisted thread snapshot, a resume payload keyed to a specific pending interrupt, and a client that maintains and replays its own transcript copy. An embedded/direct SDK call has none of these — there is no thread snapshot, no resume payload, and no separate client to replay anything. This mirrors the issue's own title, which calls it a "host-side issue" explicitly, and its body, which states "the AG-UI interrupt spec... " frames this as inherent to the hosted resume contract. Recorded as a documented capability difference (plan §2.2: "An unsupported capability is an exclusion or a documented capability difference, not a bug") for the *embedded* side specifically — the bug itself is real and is entirely on the served side.

## 5. Served execution

- Serving mode (named precisely): direct calls against the actual installed `agent_framework_ag_ui` package's internal resume-handling functions (`ThreadSnapshotSession.resume_seeded_messages` and `_reconstruct_messages_from_thread_snapshot`), confirmed to be the exact functions the real hosted server's `_agent_run.py` calls for this branch (§1) — not a full end-to-end HTTP round trip through a running `agent-framework-ag-ui` server with a real AG-UI-protocol client. See the scope note in §7 for why this is a reasoned choice here, distinct from the fuller HTTP-level reproductions done for the other cases in this pilot.
- Command/harness: `repro/agui_resume_dedup_repro.py`.
- Result, defective path (`resume_seeded_messages`, what `1.3.0` actually calls for this branch):
  ```json
  {
    "message_count": 4,
    "counts_by_id": {"msg-user-1": 2, "msg-assistant-1": 2},
    "pass": false
  }
  ```
  **FAIL** — both the user message and the assistant tool-call message are duplicated, exactly matching the issue's reported symptom.
- Result, corrected path (`_reconstruct_messages_from_thread_snapshot`, what PR #8149 routes this branch to):
  ```json
  {
    "message_count": 2,
    "counts_by_id": {"msg-user-1": 1, "msg-assistant-1": 1},
    "pass": true
  }
  ```
  **PASS** — the overlap is correctly detected and the replayed transcript is not re-persisted.
- State reset confirmed before this run: yes — fresh objects constructed per call, no state carried between the two.

## 6. Outcome classification (plan §9.5)

- [x] **Unsupported (embedded) / served fail** — recording the embedded side honestly as "the mechanism doesn't exist there" rather than a false "pass," per plan §9.5's classification options.
- The defective-path/corrected-path comparison itself is a clean **fail → pass** pair, directly analogous to an embedded-pass/served-fail case in spirit: the correct, non-duplicating logic (the reconciler) already exists and is used elsewhere in the very same package — it's simply not wired into this one call site.

## 7. Causal note

- Divergence localized to: **dispatch** — specifically, which of two already-existing message-reconciliation functions gets called for the AG-UI resume branch in `_agent_run.py`. This is not a case of missing logic (the correct reconciler, `_reconstruct_messages_from_thread_snapshot`, is fully implemented and already used by a sibling branch in the same file) — it's a routing decision that only recently-added: `elif not config.use_service_session:` chooses the reconciler, but the sibling `if resume_payload is not None and stored_pending_approval_interrupt_ids:` branch above it, which resume requests actually take, calls the naive `resume_seeded_messages` instead.
- **Consequence, stated precisely rather than assumed:** the issue's own report traces the downstream effect — the duplicated assistant tool-call message has no matching tool-result message after the duplication, so a client rendering approval state from the persisted snapshot **reopens an approval gate for a tool call that already executed**. This was **not independently re-verified end-to-end** in this reproduction (no live server, no client simulating the approval-UI rendering) — it is reported here as the issue's own traced consequence, cited rather than confirmed firsthand. What *was* independently confirmed firsthand is the underlying data corruption (duplicate message ids in the persisted snapshot), which is the mechanism the consequence depends on.
- **Scope discipline:** unlike the LangGraph and Mastra "consequential" framing built entirely on independently-run reproductions, this case's *downstream* consequence (the approval-gate reopening) rests partly on the issue reporter's own traced analysis. The *data corruption* itself (duplicate persisted messages) is independently confirmed. If this case is escalated toward the pilot's headline finding, the approval-reopening claim specifically should get an end-to-end server-level re-verification before being stated as independently established, not just cited.

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher A or C, not yet reviewed as of this record's writing}}
- Cause classification: {{pending}}
- Adjudicator notes: {{pending — specifically asked to weigh in on whether the un-re-verified approval-gate consequence is strong enough to call this "consequential" for plan §11.1 purposes, or whether it needs the end-to-end re-verification noted in §7 first}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (embedded) | N/A — mechanism doesn't exist embedded | See §4. |
| Boundary-focused tests (this study's harness) | Yes | Detected by calling the actual resume-handling functions with a synthetic replayed-transcript fixture — no live server needed to establish the mechanism, though a fuller server-level test would strengthen the downstream-consequence claim (see §7). |
| Fuller E2E reference (live `agent-framework-ag-ui` server + AG-UI client) | Not run | Deprioritized given time budget and that the mechanism is already fully explained and reproduced at the function level; flagged in §7 as the one gap worth closing before over-claiming the consequence. |
