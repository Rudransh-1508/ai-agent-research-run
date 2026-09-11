# Case Record: langgraph-checkpointer-01

Researcher: A (executed on their behalf per team request)
Framework: LangGraph
Sample type: historical issue/fix (partially — see §1, no merged fix exists yet)
Date: 2026-09-11

## 1. Provenance

- Source: [LangGraph issue #8653](https://github.com/langchain-ai/langgraph/issues/8653), "update_state can permanently erase a thread's messages," opened 2026-08-19, **still open** as of this record. Two candidate fix PRs exist, both **closed without merging**: [#8654](https://github.com/langchain-ai/langgraph/pull/8654) (closed same day, superseded) and [#8828](https://github.com/langchain-ai/langgraph/pull/8828) (a community contributor's fix, independently verified working by another commenter on the issue thread, still unmerged as of this record).
- **This is not yet a true historical defective/corrected pair** — there is no merged, released "corrected" revision to pin. What follows instead: (a) the defective state, pinned to a real release (`langgraph==1.2.11`, matching the issue's own reported version), and (b) an **unmerged candidate fix** (#8828), applied as a source patch on top of the same installed version — labeled throughout as unmerged, per plan §4's explicit caution not to treat community PRs as established corrected revisions.
- Verification method: downloaded the exact PR diffs fresh via `curl .../pull/NNNN.diff`, read the affected file (`langgraph/pregel/main.py`) in the actually-installed `langgraph==1.2.11` package to confirm the pre-patch code matches what the issue and PR describe (it does — `saver=self.checkpointer if isinstance(self.checkpointer, BaseCheckpointSaver) else None` at the exact call site named in the issue), then applied PR #8828's patch directly to the installed package and re-ran the reproduction to confirm it flips the result (it does — see §4).

## 2. Property contract (freeze before running)

- Property family: **state continuity** (plan §2.2 table).
- Contract: a subsequent request should see the state the checkpointer contract says should persist, regardless of whether the checkpointer was attached directly at compile time or supplied via `config[CONF][CONFIG_KEY_CHECKPOINTER]`.
- Evidence to inspect: message count read back via `get_state` after an initial run, and again after `update_state`, compared against the expected count (2, then 3) under both checkpointer-attachment methods.
- Oracle: `embedded_pass = (after_first_turn == 2 and after_update == 3)`; same formula applied to whatever condition is being evaluated (embedded, served, or the isolated library-level "config-injection-only" condition — see §5 for why these three ended up needing to be kept separate).

## 3. Configuration pairing

- Application code: identical graph definition (`DeltaChannel`-backed `messages` state, one no-op node) reused verbatim across every script and the live server's `graph.py`.
- Framework/dependency versions: `langgraph==1.2.11` pinned throughout; verified via `importlib.metadata.version("langgraph")` printed in every script's output.
- Initial state: fresh `InMemorySaver()` and fresh thread ID per condition; no state shared across conditions.
- Caller identity/permissions: n/a for this property family.
- Tool fixtures: deterministic — the graph's only node is `lambda state: {}` (a no-op), so any divergence is attributable to checkpointer/channel-hydration handling, not model or tool nondeterminism (plan §9.4).
- Model configuration: n/a — no model call anywhere in this case; the bug is purely in state-channel hydration.

## 4. Embedded execution

- Command/harness: `repro/embedded_vs_served_repro.py`, `run_embedded()` — `.compile(checkpointer=saver)` (checkpointer attached directly at compile time, matching a plain script or `langgraph dev`'s own graph-attachment convention for a non-factory graph).
- Result: `after_first_turn: 2, after_update: 3` → **PASS**, on both the defective (`langgraph==1.2.11`, unpatched) and candidate-fix-patched states — the embedded path never touches the buggy branch at all, since `self.checkpointer` is already the real saver.

## 5. Served execution

Three distinct conditions turned out to be necessary here, not two — this needs to be stated plainly rather than collapsed into a single "served" result, because they gave different answers and the difference is the actual finding.

**5a. Real `langgraph dev` server (the actual accessible official route):**
- Serving mode: `langgraph dev`, in-memory backend, factory-style graph (no checkpointer attached at compile time — matching the issue reporter's setup and the shape that makes `langgraph_api` treat the graph as needing a request-scoped checkpointer).
- Command/harness: live HTTP requests via `curl` — `POST /threads`, `POST /threads/{id}/runs/wait`, `GET /threads/{id}/state`, `POST /threads/{id}/state` (the update_state route), `GET /threads/{id}/state` again. See `ACCESS_LOG.md` §3-4 for the full transcript.
- Result: message count read back correctly at every step (2, then 3) → **PASS**. The bug did **not** reproduce through the real, accessible serving route.

**5b. Hand-rolled "config-injection-only" simulation (what the issue's own minimal repro does, and what an initial, incomplete reading of the server source suggested was the whole mechanism):**
- Harness: `repro/embedded_vs_served_repro.py`, `run_served()` — `.compile()` with no checkpointer attached, checkpointer supplied only via `config[CONF][CONFIG_KEY_CHECKPOINTER]`, no server involved at all.
- Result: `after_first_turn: 0, after_update: 0` → **FAIL**, matching the issue's own reported numbers exactly.
- **This condition is not a valid stand-in for "served"** — see §7. It's kept in the record because it's a clean, deterministic isolation of the library-level defect, useful for explaining the mechanism, but it must not be reported as "the served condition" since the real server does something this simulation doesn't.

**5c. Real server's actual checkpointer-attachment pattern, reproduced directly (confirms *why* 5a passes):**
- Harness: `repro/server_copy_pattern_repro.py` — mirrors `langgraph_api/graph.py`'s `get_graph()` exactly: `graph = graph_obj.copy(update={"checkpointer": saver})`, then the same run/get_state/update_state/get_state sequence.
- Result: `after_first_turn: 2, after_update: 3` → **PASS**, matching 5a exactly, confirming that the `.copy(update=...)` step (a direct attribute assignment, not just config injection) is what protects the real server from this defect.

**Candidate-fix corroboration (unmerged PR #8828):** applying #8828's patch directly to the installed `langgraph==1.2.11` package's `main.py` flips condition 5b's result to `after_first_turn: 2, after_update: 3` (PASS) — confirmed by re-running the identical script before and after the patch, with the patch reverted afterward to restore the original installed state.

- State reset confirmed before each run: yes — fresh `InMemorySaver()`, fresh thread ID, and (for the patch comparison) a diffed confirmation that reverting restored the file byte-for-byte (`diff main.py backup.py` reported no differences).

## 6. Outcome classification (plan §9.5)

- [x] **Embedded pass / served pass** — using the real, accessible `langgraph dev` server (condition 5a) as the "served" condition, which is the methodologically correct choice per plan §2.1 ("evidence from environment 2 is not automatically evidence about environment 3," and the converse: a manually written substitute for the official route isn't evidence about environment 2 either).
- The library-level defect (condition 5b) is real, verified, and has a working unmerged candidate fix — but it does not currently qualify as a "served" outcome for this case, because it was never actually exercised through the official server. It's recorded as supporting mechanism evidence, not as the case's headline outcome.

## 7. Causal note

- **The library defect itself:** divergence localized to channel hydration in `_prepare_state_snapshot`/`_aprepare_state_snapshot` (and the `bulk_update_state` family), which read `self.checkpointer` (the graph-attached checkpointer) instead of the checkpointer resolved from `config[CONF][CONFIG_KEY_CHECKPOINTER]` that every other code path in those same functions uses. When a graph is compiled without an attached checkpointer, `self.checkpointer` is `None`, silently skipping `DeltaChannel` ancestor-replay and hydrating an empty message list, which `update_state` then commits as the new head.
- **Why the accessible served route doesn't hit it:** `langgraph_api.graph.get_graph()` — the function backing every `/threads/*` request in both `langgraph dev` and (sharing the same code) `langgraph up` — always hands request handlers `graph_obj.copy(update={"checkpointer": checkpointer, ...})`. That sets `self.checkpointer` directly to a real `BaseCheckpointSaver` object on every request, so the buggy `None` branch is never reached through this route, regardless of whether the graph was compiled with or without one.
- **What this means for the case, stated plainly:** the issue reporter's claim is specifically about **LangGraph Platform** (the managed cloud product), which is a separate, closed-source runtime we don't have access to (plan §2.1 environment 3). Everything we *can* access — the open-source `langgraph-api` package underlying both `langgraph dev` and `langgraph up` — actively protects against this defect via the `.copy(update=...)` normalization. Two explanations are both plausible and neither can be ruled out without genuine Platform access: (a) LangGraph Platform's actual production runtime differs from the open-source `langgraph-api` package in a way that omits this protection, or (b) the reporter's app hit some other invocation path (a subgraph, a background/cron run, an older `langgraph-api` version, or a direct library call bypassing the standard request dispatch) that this reproduction didn't exercise.
- **This is exactly the kind of finding plan §14's reviewer-objection table anticipates** ("You only tested localhost, not deployment") and plan §2.1 requires staying honest about ("do not claim managed-cloud conclusions from a self-hosted experiment"). The correct scope for this case, as things stand, is: **a real, consequential, verified library defect with a working unmerged fix, whose claimed production/served manifestation could not be confirmed or refuted through the access actually available to this pilot.**

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher B or C, not yet reviewed as of this record's writing}}
- Cause classification: {{pending — candidates include "confirmed implementation defect, scope unconfirmed for the served condition" or "unresolved pending managed-Platform access"}}
- Adjudicator notes: {{pending}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (pre-#8828 test suite) | No | `tests/test_delta_channel_update_state.py` before the PR had 11 tests, none of which exercised a config-injected-only checkpointer against `DeltaChannel` hydration; #8828 adds the first 4 that do. |
| Boundary-focused tests (this study's harness) | Partially | The library-level isolation (5b) caught it; the actual served-route test (5a) did not, because the real route doesn't reach the buggy state. This is a useful, literal example of plan §10's warning not to conflate "boundary test found it" with "we just changed what we're testing" — here, going to the boundary changed the *outcome*, not just the assertion. |
| Fuller E2E reference | Not run (would require genuine LangGraph Platform access) | See §7. |
