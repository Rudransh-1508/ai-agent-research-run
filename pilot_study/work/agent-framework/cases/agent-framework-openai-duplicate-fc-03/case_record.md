# Case Record: agent-framework-openai-duplicate-fc-03

Researcher: B (executed on their behalf per team request)
Framework: Microsoft Agent Framework
Sample type: historical issue/fix
Date: 2026-09-11

## 1. Provenance

- Source: [Agent Framework issue #3295](https://github.com/microsoft/agent-framework/issues/3295), fixed by [PR #5690](https://github.com/microsoft/agent-framework/pull/5690), "Python: Fix duplicate item error for tool-using agents under service-side storage." **Merged** 2026-05-13T22:16:23Z (confirmed `merged: true` via the GitHub API, not just `closed`).
- Real, independently-corroborated production bug: the PR body cites **three separate field reports** converging on the same root cause — a multi-agent workflow replaying conversation across executors, a single agent with `RedisHistoryProvider`, and a single agent with `CosmosHistoryProvider` on Foundry (one reporter still reproducing it on the then-current release, `1.1.0`).
- Package: `agent-framework-openai`. Defective pin: `1.3.0` (published 2026-05-08, before the merge). Corrected pin: `1.4.0` (published 2026-05-15, after the merge) — **both stable releases**, no alpha/beta pins needed, unlike several other cases in this pilot.
- Verification method: downloaded both wheels directly from PyPI and diffed `_chat_client.py` line by line. Confirmed the exact mechanism: in `1.3.0`, the `"function_call"` branch of `RawOpenAIChatClient._prepare_message_for_openai` builds and includes the wire item unconditionally; in `1.4.0`, the identical branch is guarded by `if request_uses_service_side_storage: continue`, added before the item is built at all. The same guard is added for `function_approval_response`/`function_approval_request`, local-shell-call, and `mcp_call` items in the same diff — a coherent, single-mechanism fix, not several unrelated patches bundled together.

## 2. Property contract (freeze before running)

- Property family: **error propagation** (plan §2.2 table) — closest fit is actually stronger than the table's own framing suggests: this isn't "a failed tool operation exposed as success," it's the inverse — a well-formed request gets constructed in a way that a downstream service is contractually guaranteed to reject. Recorded under error propagation since the observable consequence is a hard, well-defined API failure.
- Contract: when a request continues a service-managed response or conversation (i.e., carries `previous_response_id`, `conversation_id`, or `conversation`), items whose identity the server already owns (`function_call`, reasoning, approval, local-shell-call) must not be re-included in the outbound wire payload — the server will reject a request containing a duplicate `id` it already has, with `400 - "Duplicate item found with id fc_xxx. Remove duplicate items from your input and try again."` This is not an inferred consequence; it's the literal error message documented in the PR and consistent with OpenAI's Responses API contract for `previous_response_id`-continued requests.
- Evidence to inspect: the actual wire-format dictionary list `_prepare_messages_for_openai` returns, checked for the presence of a `function_call`-typed item with a server-issued id when the request is a continuation.
- Oracle: `served_pass = not any(item["type"] == "function_call" for item in wire_items)` when `request_uses_service_side_storage=True`. This is checked directly against the exact function that builds the request body sent to OpenAI — not inferred, not simulated at a higher level.

## 3. Configuration pairing

- Application code: identical synthetic three-message history (user question, assistant function-call with a server-issued `fc_id`, tool result) used unmodified for both conditions (`repro-openai-fc/repro.py`).
- Framework/dependency versions: `agent-framework-openai` pinned exactly to `1.3.0` then `1.4.0`, each confirmed via `pip show` and the package's own `__version__` printed in the script's output — installed in a dedicated, isolated venv (`repro-openai-fc/venv/`) separate from the other Agent Framework cases' venv, to avoid the dependency-resolution warnings that appeared when installing an older `agent-framework-openai` alongside newer `agent-framework-foundry`/`agent-framework-foundry-local` packages in the shared venv.
- Initial state: a fresh `RawOpenAIChatClient` instance per run (`api_key` is a placeholder string; no network call is made anywhere in this script — the defect and its fix live entirely in request-body construction, not in anything requiring a live call).
- Caller identity/permissions: n/a.
- Tool fixtures: the synthetic `function_call`/`function_result` pair stands in for a real tool call; deterministic (no model or tool execution occurs).
- Model configuration: n/a — no model call anywhere in this reproduction.

## 4. Embedded execution

- Command/harness: `repro-openai-fc/repro.py`, `request_uses_service_side_storage=False` branch — the shape of a one-shot embedded call with no continuation marker (no session, no history provider, no `previous_response_id`).
- Result (both versions): `function_call_item_present: true`, **PASS** — correctly includes the function-call item, since there's no prior server-side response for it to duplicate against. Identical on both `1.3.0` and `1.4.0`, confirming the embedded path is untouched by this defect either way.

## 5. Served execution

- Serving mode (named precisely): direct call to `RawOpenAIChatClient._prepare_messages_for_openai` with `request_uses_service_side_storage=True` — the flag the actual chat client sets internally whenever the outgoing request carries `previous_response_id`, `conversation_id`, or `conversation`, which happens specifically when a session, `RedisHistoryProvider`, `CosmosHistoryProvider`, or a workflow replaying prior conversation is in play. This is not a full end-to-end HTTP call to OpenAI (see note below), but it is the exact, real, unmodified library function that constructs the request body OpenAI would receive — verified by reading the surrounding code, not assumed.
- Command/harness: `repro-openai-fc/repro.py`.
- Result, defective (`1.3.0`):
  ```json
  {"function_call_item_present": true, "pass": false, "consequence_if_present": "OpenAI Responses API would reject this request with 400 \"Duplicate item found with id fc_xxx\""}
  ```
  **FAIL** — the function-call item survives into the wire payload despite the request being a continuation, reproducing exactly the shape all three field reports describe.
- Result, corrected (`1.4.0`):
  ```json
  {"function_call_item_present": false, "pass": true, ...}
  ```
  **PASS** — the item is correctly dropped before the request would ever reach OpenAI.
- **Live confirmation, 2026-09-11 (budget explicitly approved by the team for this specific check):** ran `repro-openai-fc/live_repro.py` end-to-end against the real OpenAI Responses API (model `gpt-4o-mini`, negligible cost) — a genuine two-turn conversation where turn 1 has the model call a real tool, and turn 2 continues with `previous_response_id` set and the full history (including the turn-1 function-call and function-result) replayed, exactly the shape all three field reports describe.
  - **Defective (`1.3.0`):** OpenAI's real API rejected the request:
    ```
    Error code: 400 - {'error': {'message': 'Duplicate item found with id fc_06704a46ce0ff8e2006aa40733a12887d1845f643e44320492. Remove duplicate items from your input and try again.', 'type': 'invalid_request_error', ...}}
    ```
  - **Corrected (`1.4.0`):** the identical two-turn flow succeeded normally: `"The weather in Paris is still 18°C and cloudy."`
  - This closes the case's only remaining caveat. The consequence is no longer inferred from a documented API contract plus our own payload-level reproduction — it's a directly observed, live HTTP 400 with the exact error message the issue reports, immediately preceded by a successful run of the identical flow on the corrected version. There is nothing left in this case that rests on an external claim, a citation, or an assumption.
- State reset confirmed before this run: yes — fresh client and message list constructed per call; no state persisted between the two `_prepare_messages_for_openai` invocations or between the two package-version runs.

## 6. Outcome classification (plan §9.5)

- [x] **Embedded pass / served fail** — on the defective revision (`1.3.0`).
- [x] **Embedded pass / served pass** — on the corrected revision (`1.4.0`).

This is the cleanest case in the Agent Framework portion of this pilot: merged fix (unlike `agent-framework-agui-resume-02`), directly observable defect rather than a metadata field (unlike `agent-framework-foundry-usage-01`), and an independently-reproduced defect underlying the consequence rather than a cited one.

## 7. Causal note

- Divergence localized to: **output/request conversion**, specifically that `_prepare_message_for_openai`'s per-content-type branches did not originally check `request_uses_service_side_storage` before including server-owned item identities (function-call, approval, local-shell-call, MCP-call) — only the pre-existing reasoning-item branch had any storage-awareness at all, and even that used different (narrower) logic. The fix generalizes the same storage-awareness the reasoning branch already had to every server-issued item identity, at a single chokepoint all three field-reported repro paths flow through — a coherent single-mechanism explanation, not several unrelated symptoms coincidentally sharing a release.
- **This is genuinely mode-dependent, not internal-only:** an embedded, one-shot call with no continuation marker never sets `request_uses_service_side_storage=True` and is therefore structurally unaffected — confirmed directly (§4, identical pass on both versions). Only requests that continue a service-managed conversation — a hosted/persisted-history serving shape by construction — hit the defective branch.
- **Consequential, and directly demonstrated, not inferred from someone else's report:** the defect is a real, well-formed request that a downstream service is contractually guaranteed to reject. Three independent production users hit it through three different persistence mechanisms (workflow replay, Redis, Cosmos), and the fix's own regression tests (not independently re-run here, but referenced in the PR) assert the same wire-payload shape this reproduction checks.

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher A or C, not yet reviewed as of this record's writing}}
- Cause classification: {{pending}}
- Adjudicator notes: {{pending}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (embedded, no continuation) | No — structurally cannot | A one-shot embedded call never sets `request_uses_service_side_storage`, so no embedded-only test, however thorough, could exercise this branch at all. |
| Boundary-focused tests (this study's harness) | Yes | Detected by constructing the exact request shape a hosted/persisted-history serving path produces and inspecting the real wire-payload-building function directly. |
| Fuller E2E reference (live OpenAI API call with real session/history provider) | Not run | Deprioritized per the $0 budget — the defect itself (duplicate server-known item in the wire payload) was independently confirmed without needing to spend on a live call to observe the resulting HTTP 400, which is a documented, not assumed, consequence of that payload shape. |
