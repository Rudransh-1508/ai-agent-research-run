# Case Record: mastra-multi-instance-dedupe-03

Researcher: C
Framework: Mastra
Sample type: historical issue/fix (open, no merged fix yet — see §1)
Date: 2026-09-11

## 1. Provenance

- Source: [Mastra issue #18877](https://github.com/mastra-ai/mastra/issues/18877), "channels: MastraStateAdapter cache (dedupe/modal-context) is per-process — duplicate Slack replies when running multiple instances," labeled `bug`, `impact:high`. Real, external, production-reported bug (reporter ran 2× ECS tasks behind an ALB with Postgres storage). Candidate fix: [PR #22516](https://github.com/mastra-ai/mastra/pull/22516), "fix(core): share channel state across instances through storage" — **unmerged** as of this record.
- Found via a targeted search for a third Mastra candidate that is both mode-dependent and consequential — the two existing Mastra cases each satisfy only one of those (mastra-request-context-01 is internal-only; mastra-dev-environment-tag-02 is metadata-only).
- Verified the defect is present in the **current latest `@mastra/core`** (`1.66.0`) — no released version contains the fix (it's an open PR); confirmed directly by reading the installed package's compiled `MastraStateAdapter` class rather than trusting the issue's own description.

## 2. Property contract (freeze before running)

- Property family: **state continuity** (plan §2.2 table), specifically an idempotency/dedupe contract rather than a checkpointer-read contract, but the same family — "a subsequent request should see the state the... contract says should persist," here applied to "the same inbound event should be claimed at most once."
- Contract: for a given dedupe key (representing one logical inbound message), at most one `setIfNotExists` call across however many server instances are running should return `true`. Any second or later claim, from any instance, must return `false`.
- Evidence to inspect: the boolean return values of `setIfNotExists` calls for the same key, issued from separate `MastraStateAdapter` instances (simulating separate server processes).
- Oracle: `pass = (number of true-returning claims for one key == 1)`.

## 3. Configuration pairing

- Application code: identical dedupe-key and claim-payload constants used across both scenarios (`repro3/repro.mjs`).
- Framework/dependency versions: `@mastra/core@1.66.0` (current latest, unpatched) for the defective/real-code side; a hand-reconstructed minimal class for the corrected side (see §5 for why, and the explicit labeling used throughout to keep this distinct from every other reproduction in this pilot, which tested actual installed or actually-patched code).
- Initial state: fresh `MastraStateAdapter` instance(s) constructed per scenario; the dedupe key itself (`dedupe:slack:msg_123`) is scenario-local and never reused across the single- and multi-instance runs.
- Caller identity/permissions: n/a.
- Tool fixtures: n/a — this operates entirely on the state-adapter's cache primitive, not on any agent/tool execution.
- Model configuration: n/a.
- A no-op stand-in was used for the constructor's required `memoryStore` argument, after confirming directly in the installed bundle that neither the constructor nor `setIfNotExists`/`get`/`set` ever call any method on it (only the thread-subscription methods, not exercised here, touch it) — this is stated rather than assumed, since passing an incompatible stub silently would be exactly the kind of setup mistake plan §9.3 warns must be ruled out.

## 4. Embedded execution

Framed here as **single-instance** rather than literally "embedded SDK vs. server," since the property under test (cross-process dedupe) has no embedded/in-process analogue at all — a single in-process call trivially can't race against itself in a way multiple instances can. "Single instance" is the correct embedded-equivalent baseline: it is exactly what a local dev run or a single `mastra start` process looks like, and it's exactly the condition under which the reporter says the bug does *not* manifest.

- Command/harness: `repro3/repro.mjs`, `singleInstanceScenario()` — one `MastraStateAdapter`, two `setIfNotExists` calls for the same key, simulating Slack's own duplicate event delivery (`app_mention` + `message.channels`) arriving at the same process.
- Result:
  ```json
  { "firstClaim": true, "secondClaim": false, "repliesSent": 1, "pass": true }
  ```
  **PASS** — the second call correctly sees the key already claimed.

## 5. Served execution

- Serving mode (named precisely): **two separate `MastraStateAdapter` instances**, constructed directly (not through a running server), simulating two server processes behind a load balancer — the exact topology the issue reports (2× ECS tasks + ALB). This is a direct-library simulation of the production topology, not a literal multi-process test (no two real Node processes or load balancer were started) — stated plainly as a scope choice, consistent with how other cases in this pilot distinguish direct-library reproduction from full infrastructure reproduction.
- Command/harness: `repro3/repro.mjs`, `multiInstanceScenario()` (defective/real code) and `corrected_reconstruction.mjs` (reconstructed corrected behavior — see below).
- Result, defective (`@mastra/core@1.66.0`, actual installed code):
  ```json
  { "claimA": true, "claimB": true, "repliesSent": 2, "pass": false }
  ```
  **FAIL** — both instances win the dedupe race, exactly matching the issue's reported symptom (duplicate Slack replies).
- Result, **reconstructed** corrected behavior — **explicitly not a verified installed-package result**: PR #22516 is unmerged, so no built or released version of the fix exists to install. `corrected_reconstruction.mjs` reimplements only the relevant `setIfNotExists` logic and a minimal `ChannelsStorage`-shaped shared store, built directly from the PR's diff (fetched fresh), not from memory or assumption:
  ```json
  { "claimA": true, "claimB": false, "repliesSent": 1, "pass": true }
  ```
  This demonstrates the *mechanism* of the fix (routing the dedupe claim through a store shared across instances, instead of a private per-instance Map) produces the correct result — but it is a reconstruction, not a confirmation that PR #22516's actual code, once merged and built, behaves identically. This distinction is treated as load-bearing, not a formality: every other "corrected" result in this pilot comes from running actual installed or actually-patched code.
- State reset confirmed before this run: yes — fresh adapter instances and a fresh dedupe key per scenario.

## 6. Outcome classification (plan §9.5)

- [x] **Embedded (single-instance) pass / served (multi-instance) fail** — on the current, real, unpatched `@mastra/core@1.66.0`.
- [x] **Embedded pass / served pass** — only in the **reconstructed** corrected scenario; not independently confirmed against real patched code.

## 7. Causal note

- Divergence localized to: **state handling**, specifically that `MastraStateAdapter`'s dedupe cache (`private readonly cache = new Map()`) is a plain in-process field with no persistence or cross-instance sharing at all in the current, real, installed package — confirmed directly in the compiled source, not inferred. The class's own docstring in the current version states this as an intentional design choice ("Cache, locks, and dedup keys remain in-memory — they are inherently short-lived... and don't need persistence"), which the issue's real-world report shows is wrong once more than one instance is running.
- **This is a genuinely mode-dependent, consequential defect**, not internal-only or metadata-only: a single instance (embedded-equivalent) is structurally incapable of hitting this bug (there's only one Map, so it always correctly dedupes against itself), while 2+ instances (the standard horizontally-scaled production shape) reliably duplicate every inbound event — real duplicate side effects (repeated agent runs, repeated external replies, repeated cost), not a wrong log field.
- **Honesty caveat, stated plainly rather than glossed over:** because no released fix exists, the "corrected" half of this case is a reconstruction from the PR's diff, not a verified installed-package result. This case should be weighted as: **defective side fully confirmed and independently reproduced; corrected side plausible and mechanism-consistent, but not independently verified against real patched code.** If PR #22516 merges and ships, re-running against the real released version (swap `repro3`'s `@mastra/core` pin, remove the reconstruction file entirely) would upgrade this from "plausible" to "confirmed," matching the rigor of every other case in this pilot.
- Testing decision relevance (plan §9.1 RQ3): this is a case where **no single-instance test, however thorough, could ever catch the bug** — the defect requires literally two concurrent instances racing on the same key. This is a stronger, cleaner version of the same lesson LangGraph's #8448 (Postgres pagination) established: some defects are invisible to any test topology that doesn't match the real multi-instance production shape, regardless of how good the individual test's assertions are.

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher A or B, not yet reviewed as of this record's writing}}
- Cause classification: {{pending}}
- Adjudicator notes: {{pending — specifically asked to weigh in on whether a reconstructed (not installed-package-verified) "corrected" result is acceptable evidence for this pilot's purposes, or whether this case should be held at "defective confirmed, fix pending" status until PR #22516 actually merges}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (single-instance) | No — structurally cannot | A single instance's own Map always correctly dedupes against itself; there is no way for a single-process test, however thorough, to exercise a cross-instance race. |
| Boundary-focused tests (this study's harness) | Yes | Detected specifically by simulating the real multi-instance production topology (two adapter instances racing on one key) rather than testing one adapter more thoroughly. |
| Fuller E2E reference (real 2+ server processes + load balancer + Slack) | Not run | Would match the reporter's own real-world setup exactly, but the direct-library simulation already isolates and confirms the mechanism; deprioritized as unnecessary additional infrastructure for what's already established. |
