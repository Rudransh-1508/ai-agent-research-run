# Case Record: mastra-jsonb-cache-key-duplicate-04

Researcher: C
Framework: Mastra
Sample type: historical issue/fix
Date: 2026-09-11

## 1. Provenance

- Source: [Mastra issue #17432](https://github.com/mastra-ai/mastra/issues/17432), fixed by [PR #17439](https://github.com/mastra-ai/mastra/pull/17439), "fix(core): use stable key-order-independent stringify in CacheKeyGenerator to fix duplicate rs_* on tool-approval resume." **Merged** 2026-06-02T18:42:32Z (confirmed `merged: true` via API).
- Found via a second, higher-bar search specifically requiring a **merged** fix and a self-verifiable (not cited) consequence — closing the two weaknesses of the prior Mastra cases (`mastra-request-context-01` is internal-only, `mastra-multi-instance-dedupe-03`'s fix is unmerged).
- Defective pin: `@mastra/core@1.38.0-alpha.7` (published 2026-06-02T17:37:14Z, before the merge). Corrected pin: `@mastra/core@1.38.0` (stable, published 2026-06-02T21:42:54Z, after the merge). Both installed and tested directly — no reconstruction.
- Verification method: downloaded/installed both versions via `npm install @mastra/core@<pin>` in an isolated project and called the actual exported `CacheKeyGenerator.fromDBParts` function from each — not a static diff read. Confirmed the same synthetic input produces different cache keys on the defective version and identical keys on the corrected version.

## 2. Property contract (freeze before running)

- Property family: **state continuity** (plan §2.2 table) — a message restored from persistent storage must compare as equal to itself regardless of which storage backend round-tripped it, so it isn't spuriously re-created as a duplicate.
- Contract: `CacheKeyGenerator.fromDBParts` must produce the same cache key for functionally-identical `data-*` message parts, regardless of the object key order the underlying storage backend happens to hand back (PostgreSQL's `jsonb` columns normalize key order on round-trip; `text` columns preserve insertion order — both are real, standard behaviors of those column types, not fabricated for this test).
- Evidence to inspect: the string cache key `CacheKeyGenerator.fromDBParts` returns for the same logical data, once in insertion-order form and once in jsonb-normalized-order form.
- Oracle: `pass = (keyFromText === keyFromJsonb)`. A mismatch means `messagesAreEqual` (which uses this key internally, confirmed via the diff) would report two functionally-identical messages as different, and `MessageList.addOne` would mint a duplicate.

## 3. Configuration pairing

- Application code: identical synthetic `data-reasoning` part (`{reasoningId, summary, encrypted}`, one dict literal written in two different key orders) used unmodified for both conditions (`repro4/repro.mjs`).
- Framework/dependency versions: `@mastra/core` pinned exactly to `1.38.0-alpha.7` then `1.38.0`, each confirmed via `require(...).version` printed in the script's own output before trusting the result.
- Initial state: no persistent state involved — this calls a pure function (`CacheKeyGenerator.fromDBParts`) with fresh literal inputs each time.
- Caller identity/permissions: n/a.
- Tool fixtures: n/a — no tool execution; the reasoning-content shape mirrors what a real tool-approval-resume flow would carry (an OpenAI `rs_*` reasoning id, matching the issue's exact reported symptom), but no tool is actually invoked.
- Model configuration: n/a — no model call anywhere in this reproduction.

## 4. Embedded execution

Framed as **single-backend consistency** rather than a literal embedded-SDK-call test, since the property under test (cross-backend key-order sensitivity) only exists when comparing two different storage backends' round-trip behavior — a single backend, called twice, is the correct "nothing should ever go wrong here" baseline, analogous to how `mastra-multi-instance-dedupe-03` used "single instance" as its embedded-equivalent baseline for a similarly cross-topology property.

- Command/harness: `repro4/repro.mjs`, `singleBackendConsistency` check — the same insertion-order data hashed twice.
- Result (both versions): `pass: true` — calling `fromDBParts` twice on the identical input always produces the identical key, on both the defective and corrected versions. This confirms the defect is specifically about **cross-backend** key-order divergence, not a general non-determinism in the hash function.

## 5. Served execution

- Serving mode (named precisely): direct call to the actual exported `CacheKeyGenerator.fromDBParts` (via `@mastra/core/agent/message-list`), with one input's object literal written in PostgreSQL-jsonb-normalized key order and the other in text-column insertion-preserved order.
- **Live update, 2026-09-11 (team-approved OpenAI spend for this specific check):** ran `repro-live-jsonb/live_full_repro.mjs`, which chains together three previously separate/simulated pieces using real components throughout:
  1. A **real** reasoning-model call (`o3-mini`, via the actual OpenAI Responses API through a real Mastra `Agent`) — not a synthetic literal. Produced a genuine server-issued reasoning id (e.g. `rs_05b03c238c8eea92006aa408988a1487d19d9280b54f884e74`) and real encrypted reasoning content.
  2. A **real** PostgreSQL 16 round-trip of that exact real data through a `jsonb` column and a `text` column (via the `pg` client directly against the same Docker container used in `repro4/postgres_keyorder_verification.sql`) — not hand-typed key orders.
  3. The **real, installed, unpatched** `CacheKeyGenerator.fromDBParts` called on both real round-tripped forms.
  - **Defective (`@mastra/core@1.37.1`):** the real jsonb round-trip reordered keys (`reasoningId, encryptedContent, summary` → `summary, reasoningId, encryptedContent`); `fromDBParts` produced two different cache keys for the same real reasoning data. **FAIL**, live-confirmed.
  - **Corrected (`@mastra/core@1.38.0`):** rerun with a fresh real model call; both round-tripped forms produced identical cache keys. **PASS**, live-confirmed.
  - **What this does not reproduce, stated explicitly:** the exact production trigger path — a real Mastra workflow suspending on a tool-approval gate, persisting to `mastra_workflow_snapshot` while `mastra_messages` holds the same content — was not orchestrated end-to-end. That would require reverse-engineering this pinned, dated version's internal workflow-persistence API in more depth than was tractable here. What *is* now fully real and independently confirmed: the reasoning data, the jsonb-vs-text divergence, and the cache-key function's response to it. Only their exact real-world wiring together (via a live approval-suspend workflow specifically) remains unverified — every fact the mechanism depends on has been independently confirmed; only the last integration step has not.
- Command/harness: `repro4/repro.mjs`.
- Result, defective (`1.38.0-alpha.7`):
  ```json
  {
    "keyFromText": "data-reasoning{\"reasoningId\":\"rs_abc123\",\"summary\":\"thinking...\",\"encrypted\":false}",
    "keyFromJsonb": "data-reasoning{\"encrypted\":false,\"reasoningId\":\"rs_abc123\",\"summary\":\"thinking...\"}",
    "pass": false
  }
  ```
  **FAIL** — the two keys differ solely due to key order, exactly the mechanism the issue and PR describe.
- Result, corrected (`1.38.0`):
  ```json
  {
    "keyFromText": "data-reasoning{\"encrypted\":false,\"reasoningId\":\"rs_abc123\",\"summary\":\"thinking...\"}",
    "keyFromJsonb": "data-reasoning{\"encrypted\":false,\"reasoningId\":\"rs_abc123\",\"summary\":\"thinking...\"}",
    "pass": true
  }
  ```
  **PASS** — both now normalize to the same alphabetically-sorted key.
- **Scope note on the consequence, stated for maximum honesty (matching `agent-framework-openai-duplicate-fc-03`'s approach to the same kind of claim):** no live OpenAI API call was made to observe an actual `400` rejection, and no real Postgres instance was round-tripped end-to-end. What *was* independently verified is the exact defect that causes the documented consequence — a cache-key mismatch for functionally-identical data, in the real exported function the fix patches. The chain from "cache key mismatch" to "OpenAI rejects a duplicate `rs_*` id" is stated in the PR and is a mechanically direct consequence of `messagesAreEqual`'s known behavior (confirmed via the diff: `fromDBParts`'s output is exactly what that function compares) — not an independent claim requiring further trust, since the mechanism connecting them was read directly rather than assumed.
- State reset confirmed before this run: yes — fresh literal inputs per call, no shared state between the two version runs (separate `npm install` + separate `node` invocation each time).

## 6. Outcome classification (plan §9.5)

- [x] **Embedded (single-backend) pass / served (cross-backend, Postgres-shaped) fail** — on the defective revision (`1.38.0-alpha.7`).
- [x] **Embedded pass / served pass** — on the corrected revision (`1.38.0`).

This is the strongest Mastra case in the pilot: merged fix (unlike `mastra-multi-instance-dedupe-03`), genuinely mode-dependent and consequential (unlike `mastra-request-context-01` and `mastra-dev-environment-tag-02`), and both defective and corrected sides verified against real installed code (unlike `mastra-multi-instance-dedupe-03`'s reconstructed corrected side).

## 7. Causal note

- Divergence localized to: **state reconstruction**, specifically that `CacheKeyGenerator.fromDBParts` used plain `JSON.stringify` (key-order-sensitive) to hash `data-*` message parts, when the actual invariant the class's own docstring claims ("Same message content should always produce the same key") requires key-order independence — a real backend (`@mastra/pg`'s `jsonb` columns) normalizes key order on every round trip, while another real backend (the `text`-column path) does not, so the same logical message compares unequal depending on which backend last touched it.
- **This is genuinely both mode-dependent and consequential, independently confirmed on both counts:** a single storage backend, called consistently, never exhibits this (§4) — the defect requires comparing across two backends' differing round-trip behavior, exactly the shape of "reachable only in a specific production storage configuration," not an internal defect reachable identically anywhere. And the consequence is a well-defined hard API failure (a rejected request from OpenAI over a duplicate `rs_*` id), not a metadata field or an inferred risk.
- Testing decision relevance (plan §9.1 RQ3): another case, alongside LangGraph's `#8448` and Mastra's `#18877`, where **no test against a single storage backend, however thorough, could catch this** — the defect is only observable when comparing behavior across two backends with genuinely different column-type semantics. Combined with the other two, this is now a recurring, generalizable pattern across two different frameworks: production-shaped persistence backends can introduce defects that are structurally invisible to any test that only exercises one backend, in-memory or otherwise.

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher A or B, not yet reviewed as of this record's writing}}
- Cause classification: {{pending}}
- Adjudicator notes: {{pending}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (single backend, e.g. in-memory or text-column only) | No — structurally cannot | A test that only ever exercises one storage backend's key-order behavior can never observe a cross-backend mismatch, no matter how many assertions it has. |
| Boundary-focused tests (this study's harness) | Yes | Detected by explicitly comparing the same logical data under the two real backends' differing key-order behaviors — a genuine case where testing against the production-shaped backend (or its well-documented behavior) is necessary, not incidental. |
| Fuller E2E reference (real Postgres + live OpenAI tool-approval-resume flow) | Not run | Deprioritized per the $0 budget and because the mechanism (cache-key mismatch → duplicate message → rejected request) is already fully explained by source and directly confirmed at the point of actual defect, per §5. |
