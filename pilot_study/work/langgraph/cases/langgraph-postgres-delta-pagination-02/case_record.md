# Case Record: langgraph-postgres-delta-pagination-02

Researcher: A (executed on their behalf per team request)
Framework: LangGraph
Sample type: historical issue/fix (open issue, no merged fix yet — see §1)
Date: 2026-09-11

## 1. Provenance

- Source: [LangGraph issue #8448](https://github.com/langchain-ai/langgraph/issues/8448), "PostgresSaver: get_delta_channel_history permanently poisons walk cursor when target checkpoint isn't in the first pagination page, silently dropping DeltaChannel history." Found while investigating [#8653](https://github.com/langchain-ai/langgraph/issues/8653) — that issue's own top comment flags #8448 as "possibly related in failure smell, different site." Confirmed on inspection that it's a **genuinely separate mechanism** (different package, different code path — see §7), not a duplicate.
- State: **open, no PR or fix found at time of writing** (unlike #8653, which at least has an unmerged candidate PR). This is currently defective-only — no corrected revision, pinned or otherwise, exists to compare against. Treat as an open defect finding, not a defective/corrected pair.
- Verification method: read `langgraph-checkpoint-postgres==3.1.2` (latest, installed fresh) directly — `base.py:445-446` contains exactly the code the issue names: `if ch not in walk_cursor_by_ch: walk_cursor_by_ch[ch] = parent_of.get(target_id)`, and `_DELTA_PAGE_SIZE = 1024` at `base.py:23`. Confirmed before writing any reproduction script, not assumed from the issue text.

## 2. Property contract (freeze before running)

- Property family: **state continuity** (plan §2.2 table).
- Contract: a request for a specific historical checkpoint's state should return that checkpoint's actual recorded values, regardless of how many checkpoints have accumulated on the thread since, and regardless of whether that checkpoint still falls within the storage backend's internal pagination window.
- Evidence to inspect: message count read back from `get_state(config_with_checkpoint_id=<old checkpoint>)`, compared against the count that checkpoint should have (its own recorded value, independent of later history).
- Oracle: `pass = (historical_read_count == expected_count_for_that_checkpoint)`.

## 3. Configuration pairing

- Application code: identical graph (one `DeltaChannel`-backed `messages` state, one no-op node) used for both conditions, same script (`repro/postgres_delta_pagination_repro.py`).
- Framework/dependency versions: `langgraph==1.2.11`, `langgraph-checkpoint-postgres==3.1.2` (latest), `InMemorySaver` from `langgraph.checkpoint.memory` (ships with core `langgraph`, same version).
- Initial state: **fresh, UUID-suffixed thread ID per script run** — this was not true on the first attempt (see below) and the fix mattered.
- Caller identity/permissions: n/a.
- Tool fixtures: deterministic no-op node; no model or tool call involved.
- Model configuration: n/a.
- **A test-hygiene failure worth recording plainly, not quietly fixing:** the first run of this script reused a literal `"pg-thread"` thread ID across two separate script invocations (an initial N=20 sanity check, then the full N=1030 run). Postgres persisted the first run's checkpoints, so the second run's "after_seed" and "after_many_updates" numbers were contaminated by leftover history (`after_seed` read 24 instead of 2). This produced a false "fail" that had nothing to do with the actual defect — it was plan §9.3's exact warning ("never let one run's side effects become another's starting state") caught in the act. Fixed by generating a fresh `uuid.uuid4().hex[:8]`-suffixed thread ID per run; verified via `SELECT thread_id, COUNT(*) FROM checkpoints GROUP BY thread_id` that each run's checkpoints land in their own isolated thread (`pg-thread-c359b422`: 1033 rows, `pg-thread-cc057f58`: 1033 rows — the contaminated `pg-thread` row, 1056, was left from the broken run and excluded from the final result).
- **A second false start, also worth recording:** the very first version of this script called plain `get_state(config)` with no explicit `checkpoint_id` after the update flood. That always targets the current HEAD checkpoint, which by construction is always the newest row and therefore always inside the pagination window — so the first version passed on both backends, even after crossing 1024 checkpoints, and would have wrongly concluded there was no bug. The issue's own text is explicit that the target must be a checkpoint "any... in the thread's history" reached via `checkpoint_id` (or `update_state`/`get_state_history` walking back through it) — fixed by capturing the seed checkpoint's own `checkpoint_id` right after seeding and explicitly requesting it after the update flood.

## 4. Embedded execution

- Command/harness: `repro/postgres_delta_pagination_repro.py`, `in_memory (dev-shaped)` condition — `InMemorySaver`, same graph, same operation sequence (seed, 1030 delta-only `update_state` calls, then an explicit historical read targeting the seed checkpoint).
- Result:
  ```json
  {
    "after_seed": 2,
    "after_many_updates": 1032,
    "expected_after_many_updates": 1032,
    "after_historical_read": 2,
    "expected_after_historical_read": 2,
    "pass": true
  }
  ```
  **PASS** — `InMemorySaver` has no pagination logic at all (it holds the full write log in memory), so there's no mechanism for this defect to exist in the in-memory/dev-shaped backend.

## 5. Served execution

- Serving mode (named precisely): **direct library call against a real, locally-run Postgres 16 instance (Docker), using `AsyncPostgresSaver` — the exact checkpointer backend `langgraph up`'s production-shaped path uses.** Not run through the actual `langgraph up` HTTP server — see the access-blocker note below for why, and the reasoning for why this is still valid evidence.
- Command/harness: `repro/postgres_delta_pagination_repro.py`, `postgres (production-shaped, langgraph up backend)` condition.
- Result:
  ```json
  {
    "after_seed": 2,
    "after_many_updates": 1032,
    "expected_after_many_updates": 1032,
    "after_historical_read": 0,
    "expected_after_historical_read": 2,
    "pass": false
  }
  ```
  **FAIL** — the historical checkpoint's own recorded messages (2) silently read back as 0. No exception, no warning, exactly as the issue describes.
- **Why direct-library-against-real-Postgres is valid "served" evidence here, unlike the naive approach would be for other bugs:** confirmed by reading `langgraph_api/graph.py` (the actual server request-dispatch code, already inspected in detail for case `langgraph-checkpointer-01`) that it does not wrap or modify checkpoint-history reads in any way — `get_state`/`get_state_history` calls resolve straight through to whatever checkpointer backend is configured, with no server-side normalization comparable to the `.copy(update=...)` step that protected against #8653. The defect here lives entirely inside `langgraph-checkpoint-postgres`'s own pagination logic, a dependency invoked identically whether called directly or dispatched to by the server. This is a materially different situation from case `langgraph-checkpointer-01`, where an assumption like this turned out to be wrong — the difference is stated explicitly rather than asserted by analogy.
- **Access blocker, recorded rather than worked around:** attempting the actual `langgraph up` server (which would provide the strongest possible evidence — a real HTTP round trip against the full production stack) hit a real credential requirement: the CLI printed `requires env var LANGSMITH_API_KEY with access to LangSmith Deployment` (or `LANGGRAPH_CLOUD_LICENSE_KEY` for production use) before proceeding to build/pull its Docker image. Per README §6 and plan §8.3, this is a clean access blocker to record, not a reason to acquire a key without team approval — the process was stopped (no compose stack was ever brought up; confirmed via `docker ps -a` showing only the standalone Postgres container used for the direct-library reproduction, not any `langgraph up`-spawned containers).
- State reset confirmed before this run: yes — see §3's UUID-suffixed thread ID fix, verified via direct SQL query against the checkpoints table.

## 6. Outcome classification (plan §9.5)

- [x] **Embedded pass / served fail** — this is the pattern plan §11.1 asks for: "consequential, faithfully reproduced mode-dependent differences," localized and explained, not forced.
- This is the first LangGraph or Mastra case in this pilot that is **both** genuinely mode-dependent **and** consequential (real data loss, not metadata) — see the running tally in `coordination/outcome_tracker.csv`.

## 7. Causal note

- Divergence localized to: **state reconstruction**, specifically `langgraph-checkpoint-postgres`'s `BasePostgresSaver._try_advance_walks` (`base.py:445-446`). `get_delta_channel_history` pages the `checkpoints` table newest-first in chunks of 1024 rows. For each `DeltaChannel`, `_try_advance_walks` initializes that channel's walk cursor exactly once, guarded by `if ch not in walk_cursor_by_ch`, seeding it from `parent_of.get(target_id)` — the *target* checkpoint's parent, looked up in a dict built only from rows fetched so far. If the target checkpoint (here, an old one, requested explicitly by `checkpoint_id`) isn't among the newest 1024 rows on the first page, `parent_of.get(target_id)` returns `None`, and the cursor is permanently set to `None` — treated identically to "this channel has no ancestor to replay," even though the real ancestor chain exists and will be loaded on a later page. The guard means the cursor is never re-derived once poisoned. The walk for that channel silently terminates with no `"seed"` and empty `"writes"`, and `channels_from_checkpoint` hydrates the channel to empty.
- **This is a mechanism entirely specific to the Postgres-backed, production-shaped checkpointer.** `InMemorySaver` doesn't page at all — it has no pagination boundary to poison a cursor against — so this defect is structurally invisible to any embedded test, any `langgraph dev` session, or any test suite using the in-memory checkpointer, no matter how thorough. This is a genuinely useful data point for RQ3 (testing decision, plan §9.1): **no amount of additional local or boundary-focused testing using the in-memory backend could ever catch this** — the only way to catch it is a test that runs against the real Postgres-backed checkpointer with a long enough thread history, which is specifically the kind of "fuller E2E, production-shaped" test plan §10 asks the study to evaluate the incremental value of.
- Practical trigger conditions, stated precisely so this isn't oversold: requires (a) a `DeltaChannel`-typed state key (used for message-list state, a common pattern but not universal), (b) more than 1024 checkpoints accumulated on a single thread since that channel was last fully re-seeded, and (c) a read targeting a checkpoint older than the newest 1024 rows — via an explicit `checkpoint_id`, or via `update_state`/`get_state_history` walking back that far. A short-lived thread, or one whose channel gets periodically re-seeded, would never hit this. This scopes the claim honestly: it's a real, production-only, silent-data-loss defect, but it requires an unusually long-lived single thread to trigger — worth stating plainly rather than implying every LangGraph Platform deployment is at risk.

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher B or C, not yet reviewed as of this record's writing}}
- Cause classification: {{pending}}
- Adjudicator notes: {{pending}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (embedded, in-memory backend) | No — structurally cannot | `InMemorySaver` has no pagination logic; no local/embedded test using it could ever exercise this code path, regardless of how thorough. |
| Boundary-focused tests (this study's harness) | Yes | Detected specifically by testing against the real Postgres backend with a long-enough thread history and an explicit historical-checkpoint read — this is a genuine "boundary/production-shaped test found something a local test structurally cannot" result, unlike the ambiguous or negative findings in the other two cases so far. |
| Fuller E2E reference (real `langgraph up` server) | Not run — access-blocked (§5) | The mechanism lives entirely in the checkpointer backend package, invoked identically by direct calls or server dispatch (confirmed via `langgraph_api/graph.py` inspection), so this is assessed as very likely to reproduce identically through the real server; stated as an assessment, not confirmed fact, given the credential blocker prevented direct confirmation. |
