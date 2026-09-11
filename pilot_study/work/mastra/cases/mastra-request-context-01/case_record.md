# Case Record: mastra-request-context-01

Researcher: C
Framework: Mastra
Sample type: historical issue/fix
Date: 2026-09-11

## 1. Provenance

- Source: [Mastra PR #20741](https://github.com/mastra-ai/mastra/pull/20741) ("fix(core): preserve caller context for stream approvals", merged 2026-08-05T15:12:53Z), combined with its direct follow-up [#20748](https://github.com/mastra-ai/mastra/pull/20748) ("fix(core): set the caller context on every subscription entry point"). #20748 explicitly targets #20741's branch, not `main` — it is the second half of one change, not an independent case (re-checked by fetching both PRs' actual diffs fresh via `curl .../pull/NNNNN.diff` and the GitHub REST API, not the research plan's carried-over summary, which had flagged #20748 as unrefetched).
- Defective revision pin: `@mastra/core@1.56.0` (published 2026-08-05T00:16:50Z, before the 15:12:53Z merge).
- Corrected revision pin: `@mastra/core@1.57.0` (published 2026-08-05T20:36:29Z, after the merge).
- **Verification method (not just timestamps):** downloaded both npm tarballs (`npm pack @mastra/core@1.56.0` / `@1.57.0`) and grepped the built `dist/agent-controller-*.js` bundle for `setRequestContext`. Result: **zero occurrences** in 1.56.0 (the method doesn't exist at all — there is no per-session slot to hold a caller context), and the class definition plus all **three** entry-point call sites (`sendMessage`/`steer`, `sendNotificationSignal`, `resumeToolCall`) present in 1.57.0. This directly confirms 1.57.0 contains both #20741 and #20748's fixes, consistent with their identical merge timestamp.

## 2. Property contract (freeze before running)

- Property family: **request context** (plan §2.2 table) — "a tool receives the intended caller-specific context after server dispatch."
- Contract, derived from the actual PR diffs (not the plan's carried-over summary): when a `tool-call-approval` chunk is processed on a session's subscribed thread stream (`SessionRunEngine#processSubscribedThreadStream`), the request context in effect must be the most recently set one from any of the session's authenticated entry points — a fresh `sendMessage`/`steer`, a `resumeToolCall`, or a `sendNotificationSignal` — not a stale snapshot taken once when the subscription first opened.
- Evidence to inspect: the `requestContext` argument that `Session#approveToolCall` is actually invoked with when a `tool-call-approval` chunk is processed, compared against the identity set by the most recent entry-point call.
- Oracle: wrap the real (unmocked) `session.approveToolCall` method to record its `requestContext.get('user')` argument, then compare against the caller identity that was set via a real entry point immediately beforehand. This mirrors the technique the upstream regression tests themselves use (`vi.spyOn(session, 'approveToolCall')`), adapted to run outside the monorepo's internal test utilities.

## 3. Configuration pairing

- Application code: identical harness (`repro/embedded-repro.ts`) run unmodified against both pinned versions — only `node_modules/@mastra/core` was swapped (`npm install @mastra/core@1.56.0` then `@1.57.0`), confirmed via `require(...).version` printed in each run's output.
- Framework/dependency versions: pinned exactly (`@mastra/core@1.56.0` / `@1.57.0`, no caret range in `package.json` after the first install — see note below).
- Initial state: fresh `AgentController` + `InMemoryStore` + fresh `Session` constructed per run (new process each time via `npx tsx`), no shared state between conditions.
- Caller identity/permissions: `record_context` tool set to permission policy `allow` (via `session.permissions.setForTool`) so `resolveToolApproval` auto-continues inside `processSubscribedThreadStream`, isolating the request-context propagation mechanism from the separate, human-in-the-loop approval UI path (see causal note, §7, for why that path was excluded).
- Tool fixtures: deterministic — no live tool execution occurs; the oracle observes the `requestContext` argument at the `approveToolCall` call site directly (plan §9.4 "deterministic isolation").
- Model configuration: deterministic — no live or mocked model call was needed for this specific probe. The scenario is driven by directly invoking the public `Session#sendNotificationSignal` (a real, unmocked entry point) and a hand-built `AgentThreadSubscription` fed into the public `Session#processSubscribedThreadStream`, exactly mirroring the technique the upstream regression tests use (`processSubscribedChunks` helper in `trailing-guard-new-run.test.ts`), since those tests also don't require a live model.

Note: `package.json` in `repro/` was left with npm's default `^` range after `npm install`; the *effective* pin for each run is what actually got installed and was verified in the console output before running (`1.56.0` then `1.57.0` exactly), not a loose range trusted blindly.

## 4. Embedded execution

- Command/harness: `npx tsx embedded-repro.ts` in `pilot_study/work/mastra/repro/`, run once against each pinned version.
- Result, defective (`@mastra/core@1.56.0`):
  ```json
  {
    "mastraCoreVersion": "1.56.0",
    "approveToolCallInvocations": [
      { "toolCallId": "tool-call-1", "hadContext": true }
    ]
  }
  ```
  — `hadContext: true` but no `callerId` key at all: `approveToolCall` was invoked with a `RequestContext` object, but that context carried no caller identity (matching the changeset's own description: "after a restart it has nothing at all"). **FAIL** against the contract.
- Result, corrected (`@mastra/core@1.57.0`):
  ```json
  {
    "mastraCoreVersion": "1.57.0",
    "approveToolCallInvocations": [
      { "toolCallId": "tool-call-1", "callerId": "caller-B", "hadContext": true }
    ]
  }
  ```
  — the approval carried `caller-B`'s identity, which is exactly the identity set by the immediately-preceding `sendNotificationSignal` call. **PASS.**

## 5. Served execution

- Serving mode (named precisely): `mastra build` + `mastra start`, in-memory storage, single local process, `@mastra/core@1.66.0` (current latest — see limitation below on why the exact historical pins couldn't be run through the built CLI server).
- Command/harness: see `ACCESS_LOG.md` §3-4 — `curl` against `/api/agent-controller/repro/sessions/repro-resource/{notifications,tool-approval}`.
- Result: **not independently reproduced at the pinned historical versions** through the HTTP server — see §7 causal note for why this is a scoping limitation rather than a gap in the finding, and `ACCESS_LOG.md` §6 for the specific `@mastra/loggers`/`@mastra/core@1.57.0` version-skew blocker encountered when attempting it.
- State reset confirmed before this run: n/a (served historical reproduction not completed).

## 6. Outcome classification (plan §9.5)

- [x] Unsupported / setup-blocked / oracle-indeterminate for the **served** condition specifically — reason: the CLI toolchain's own dependency resolution (`@mastra/loggers@latest`) is incompatible with the pinned defective/corrected `@mastra/core` versions, and building a workaround (a hand-pinned matching `@mastra/loggers`, or a custom HTTP shim) either wasn't attempted (former, deprioritized — see §7) or is explicitly disallowed by plan §2.1/§8.3 (latter). This is recorded as a genuine setup limitation, not silently dropped.
- For the **embedded** condition alone: Embedded fail (1.56.0) / Embedded pass (1.57.0) — a valid defective→corrected regression pair, independent of the served/embedded classification grid (which compares embedded vs. served *within one framework version*, not defective vs. corrected).

## 7. Causal note

- Divergence localized to: **context handling**, specifically `SessionRunEngine#processSubscribedThreadStream` building its `requestContext` once via `await this.#machinery.buildRequestContext()` **before** the chunk-processing loop starts (defective), versus rebuilding it **per chunk** from the session's live `#requestContext` slot, refreshed by every authenticated entry point (corrected).
- **This is not a serving-boundary defect** — and this needs to be stated plainly rather than shaped to fit the study's headline pattern. Reading `packages/server/src/server/handlers/agent-controller.ts` (both in the cloned source and by re-deriving the route wiring independently) shows the HTTP handlers are thin: they build a `requestContext` from server middleware and pass it into the *same* `Session` methods (`sendNotificationSignal`, `respondToToolApproval`, `respondToToolSuspension`) that an embedded caller invokes directly. The defect lives entirely inside `Session`/`SessionRunEngine`, invoked identically regardless of caller. There is no dispatch/serialization/reconstruction step at the HTTP boundary that changes this behavior.
- Practical consequence for this study: this case does **not** produce the "embedded pass / served fail" pattern that motivates the deployment-boundary framing (plan §2.1). It is better understood as an **internal state-handling defect** that a purely in-process unit test — exactly the kind the maintainers' own new regression tests are — was sufficient to catch, and did catch, without needing any serving-boundary test. That is a real, if inconvenient, finding for RQ3 (plan §9.1): here, additional boundary-focused/public-entrypoint testing would have added no incremental detection over the embedded-level test the fix's own PR already shipped. Framing this case as evidence *for* the boundary-testing thesis would misrepresent it.
- What this case is still good for: it is a clean, verified historical defective→corrected pair (plan §9.2, §11 "aim for four tractable case pairs, including a historical defective/corrected pair") that explains a concrete request-context-propagation mechanism, and it is honest counter-evidence that keeps the eventual manuscript's testing recommendation properly bounded (plan §14: "Your stronger assertions, not serving, found the bug" is a live objection this case data supports, not one this case refutes).

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher A or B, not yet reviewed as of this record's writing}}
- Cause classification: {{pending}}
- Adjudicator notes: {{pending}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (pre-#20741 test suite) | No | The pre-fix test suite (`trailing-guard-new-run.test.ts` before the PR) had no test covering context propagation through `processSubscribedThreadStream`'s approval-chunk path at all — the PR added the first coverage. |
| Boundary-focused tests (this study's embedded-level harness) | Yes | Detected via direct, in-process calls to the same public `Session` API the maintainers' own fix-validating tests use — no HTTP layer needed to detect it. |
| Fuller E2E reference (served, via built server) | Not attempted | See §5/§6 — blocked by CLI/core version skew, not by the mechanism itself (which, per §7, would behave identically through HTTP). |
