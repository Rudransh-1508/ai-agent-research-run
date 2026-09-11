# Case Record: agent-framework-foundry-usage-01

Researcher: B (executed on their behalf per team request)
Framework: Microsoft Agent Framework
Sample type: historical issue/fix
Date: 2026-09-11

## 1. Provenance

- Source: [Agent Framework issue #7416](https://github.com/microsoft/agent-framework/issues/7416), ".NET: Python: [Bug]: Foundry Hosting omits usage from /responses terminal events," opened 2026-07-30, still open on GitHub (no PR was ever explicitly cross-linked as "Fixes #7416"), but **the underlying defect is fixed and published** — see below.
- Defective revision pin: `agent-framework-foundry-hosting==1.0.0b260813` (published 2026-08-14T02:39:13Z).
- Corrected revision pin: `agent-framework-foundry-hosting==1.0.0b260827` (published 2026-08-28T01:10:31Z) — also independently confirmed fixed in the current latest, `1.0.0b260910` (2026-09-10).
- **Verification method (not just timestamps or issue text):** downloaded the actual `.whl` files for `1.0.0b260722`, `1.0.0b260730`, `1.0.0b260813` (all pre-fix) and `1.0.0b260827` (post-fix) from PyPI directly, extracted them, and grepped `_responses.py` for `emit_completed(` / `emit_failed(` call sites. The three earlier versions all call `emit_completed()` / `emit_failed(message=message)` with **no usage argument at all**, exactly matching the issue's description; `1.0.0b260827` (and the current latest) call `emit_completed(usage=tracker.usage)` and `emit_failed(message=message, usage=tracker.usage if tracker is not None else None)`. The exact commit/PR that introduced the fix wasn't cross-referenced from the issue (GitHub shows no linking PR); commits in that window touching `_responses.py` include #7670 ("Foundry Hosted Agent Resiliency Support," 2026-08-21) and #7921 ("Upgrade agentserver dependencies," 2026-08-27) — the fix most likely landed as part of one of these, but attribution to a single PR wasn't confirmed with certainty and is stated as such rather than guessed.

## 2. Property contract (freeze before running)

- Property family: **observability metadata** (plan §2.2 table) — "contractually exposed accounting or trace fields survive conversion." Per plan §2.2's own caution, echoed here deliberately: "missing usage information does not, by itself, establish an incorrect bill or a failed user task" — this is scoped as a metadata-family finding throughout, not a task-consequence claim.
- Contract: usage/accounting fields present in the agent's native response (`AgentResponse.usage_details` / the chat client's reported `UsageDetails`) should survive conversion into the hosted OpenAI-compatible `/responses` terminal event (`response.completed.response.usage`).
- Evidence to inspect: field-by-field comparison of the native response's usage data against the hosted endpoint's `usage` field for the identical underlying response.
- Oracle: a **deterministic** chat client (`repro/deterministic_chat_client.py`) that always reports a fixed usage total (`input_token_count=100, output_token_count=25, total_token_count=125`) regardless of any live model — so the pass/fail check is exact equality against a known constant, not a fuzzy comparison against nondeterministic model output.

## 3. Configuration pairing

- Application code: identical `Agent` + `DeterministicChatClient` + `ResponsesHostServer` setup (`repro/server.py`, `repro/deterministic_chat_client.py`) used unmodified for both conditions — only the installed `agent-framework-foundry-hosting` version differs.
- Framework/dependency versions: `agent-framework==1.18.0` held constant; `agent-framework-foundry-hosting` swapped between `1.0.0b260813` and `1.0.0b260910`/`1.0.0b260827`, each confirmed via `pip show` before running.
- Initial state: a fresh server process started per condition (no shared state between runs — each is a separate `python server.py` invocation).
- Caller identity/permissions: n/a for this property family.
- Tool fixtures: n/a — no tool calls involved.
- Model configuration: **deterministic double** (plan §9.4) — `DeterministicChatClient`, a minimal hand-written `BaseChatClient` subclass, returns a fixed text response and a fixed `UsageDetails` total with no network call and no API key, so the result is not affected by model nondeterminism at all. A live-model confirmation (using a real Azure OpenAI/OpenAI-backed chat client) was not additionally run, since the mechanism (whether `usage` gets passed to `emit_completed`) doesn't depend on what produced the usage numbers — this is stated as a reasoned choice, not an oversight.
- **A version-compatibility snag worth recording, not silently patched around:** the defective pin (`1.0.0b260813`)'s `ResponsesHostServer.__init__` does not accept a `history_source` keyword argument that a later version added; the first attempt to run the server against the defective pin failed with `TypeError: Starlette.__init__() got an unexpected keyword argument 'history_source'`. Fixed by inspecting `ResponsesHostServer.__init__`'s signature at runtime and only passing `history_source` when the installed version actually declares it — so the same `server.py` script runs unmodified against both pins, which matters for keeping "application code identical across conditions" actually true rather than nominally true.

## 4. Embedded execution

- Command/harness: `repro/embedded_check.py` — constructs the same `Agent`+`DeterministicChatClient`, calls `agent.run("hello")` directly in-process (no server, no HTTP), and reads `response.usage_details`.
- Result: `usage_details: {'input_token_count': 100, 'output_token_count': 25, 'total_token_count': 125}` — **PASS**. This does not depend on the `agent-framework-foundry-hosting` package at all (the embedded path never imports it), so it's identical regardless of which foundry-hosting version is installed — confirmed by the fact that `agent-framework-foundry-hosting` was never even imported in this script.

## 5. Served execution

- Serving mode (named precisely): **self-hosted `agent_framework_foundry_hosting.ResponsesHostServer`**, run as a standalone local process (`hypercorn` ASGI server, `127.0.0.1:8088`) — explicitly **not** Azure's managed AI Foundry cloud service; see `ACCESS_LOG.md` §5 for why this distinction matters and how it was confirmed (zero Azure configuration needed to start and serve correctly).
- Command/harness: a separate Python process using the official `openai` package's client — `client.responses.create(model="repro-agent", input="Hello", stream=False)` — exactly matching the issue's own code sample (adapted from `stream=True` to `stream=False`; the issue states both paths are affected and share the same usage-aggregation code).
- Result, defective (`1.0.0b260813`):
  ```
  usage: None
  output_text: hi from the deterministic chat client
  ```
  **FAIL** — the response text arrives correctly, but usage, which the deterministic client explicitly reported, is silently dropped.
- Result, corrected (`1.0.0b260910`):
  ```
  usage: ResponseUsage(input_tokens=100, input_tokens_details=InputTokensDetails(cache_write_tokens=0, cached_tokens=0), output_tokens=25, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=125)
  output_text: hi from the deterministic chat client
  ```
  **PASS** — usage correctly reaches the client, exactly matching the fixed totals the deterministic chat client reported.
- State reset confirmed before this run: yes — the server process was fully stopped (`kill`, confirmed via `lsof` showing the port free) and the package version swapped (`pip install --pre agent-framework-foundry-hosting==<pin>`, confirmed via `pip show`) before each condition's server was started fresh.

## 6. Outcome classification (plan §9.5)

- [x] **Embedded pass / served fail** — on the defective revision (`1.0.0b260813`).
- [x] **Embedded pass / served pass** — on the corrected revision (`1.0.0b260827`/`1.0.0b260910`).

This is the third case across the whole pilot showing this exact "local pass → served fail, then fixed" pattern (after LangGraph's `#8448`), and — unlike LangGraph's `#8653` — this one required no correction to an initial assumption about server-side compensation: the defect and its manifestation through the real server matched the issue's own description on the first attempt.

## 7. Causal note

- Divergence localized to: **output conversion**, specifically the point where `agent_framework_foundry_hosting/_responses.py`'s response-completion handlers build the OpenAI-compatible terminal event. The underlying `AgentResponse`/`ChatResponse` already carries `usage_details` (confirmed directly in §4's embedded result); the handler simply never read it before calling `response_event_stream.emit_completed()` — a pure information-discarding bug in the conversion layer, not a missing capability anywhere upstream.
- **On the self-hosted vs. managed-cloud distinction (plan §2.1, §8.3; the brief's explicit watch-out for this framework):** the reproduction here is against the self-hosted `ResponsesHostServer`, which is a plain Python package implementing the Foundry-compatible `/responses` protocol — it required no Azure account, subscription, or credential to run, which was itself confirmed empirically rather than assumed. Whether Azure's actual managed AI Foundry cloud service exhibits the identical defect wasn't independently tested. However, unlike the LangGraph `#8653` case (where the accessible server turned out to have compensating logic the direct-library simulation lacked), there is no evidence here of any additional server-side normalization layer between this package and a "real" managed deployment — `agent_framework_foundry_hosting` is the package name Microsoft ships specifically for Foundry-compatible hosting, and the defect is inside its own response-building code, not in anything a managed wrapper would obviously intercept or fix. The assessment is that this is **very likely** to reproduce identically on the managed service too, but this is stated as an assessment based on the mechanism's location, not a confirmed fact — the honest label for this case is "self-hosted, environment 2, confirmed; environment 3 not independently tested."
- Consequence scope, stated plainly per plan §2.2's own caution: this is a metadata-only finding. A dropped usage field doesn't corrupt task output or user-visible behavior; it specifically prevents "token accounting, cost estimation, cache analysis, or reasoning-token analysis" downstream, as the issue itself states. It does not, by itself, satisfy plan §11.1's "consequential" bar — it sits alongside the two Mastra metadata cases in that respect, distinct from LangGraph's `#8448` (genuine data loss).

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher A or C, not yet reviewed as of this record's writing}}
- Cause classification: {{pending}}
- Adjudicator notes: {{pending}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (embedded `agent.run()`) | No — structurally cannot | The defect is entirely inside `agent_framework_foundry_hosting`'s response-conversion code, which an embedded call never touches at all. No amount of embedded-level testing, however thorough, could catch this. |
| Boundary-focused tests (this study's harness) | Yes | Detected specifically by testing the real hosted `/responses` endpoint with a deterministic usage oracle — a genuine case where going to the boundary is necessary, not just incidentally where the bug happened to be found. |
| Fuller E2E reference (streaming path, or genuine Azure-managed Foundry) | Not run | See `ACCESS_LOG.md` §6 — deprioritized as unnecessary to establish the mechanism, not access-blocked. |
