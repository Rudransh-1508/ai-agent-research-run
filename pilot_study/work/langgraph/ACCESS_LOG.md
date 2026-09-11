# Access Log: LangGraph

Researcher: A (executed on their behalf per team request)
Date/time started: 2026-09-11

## 1. Versions and mode

- Package/library versions: `langgraph==1.2.11`, `langgraph-cli==0.4.31` (installed via `pip install "langgraph-cli[inmem]"`), `langgraph-api==0.14.0`, `langgraph_runtime_inmem==0.34.0` (all resolved together in one isolated venv, no manual version pinning conflicts).
- Runtime version: Python 3.11.0 (this machine's default `python3`), isolated in a dedicated venv at `pilot_study/work/langgraph/venv/`.
- Docker: available (`Docker version 28.5.1`) but not exercised — see §6.
- Exact serving mode, named precisely: **`langgraph dev`, in-memory checkpointer backend (`langgraph_runtime_inmem`)** — this is the lightweight local-development server, not the Docker/Postgres-backed `langgraph up` path. Per plan §8.1's own caution, this does **not** by itself establish access to the Postgres-backed / managed-platform mechanism — see §5 for why this matters here specifically, and §6 for why `langgraph up` wasn't also run.
- Git/revision pin for the historical case: no merged corrected revision exists yet (issue #8653 is still open — see case record §1). A pinned defective revision (`langgraph==1.2.11`, matching the issue's own "Output on langgraph==1.2.11 and current main") and an **unmerged candidate fix** (PR #8828, applied as a source patch, not a released version) were used instead — clearly labeled as such throughout, per plan §4's caution against treating unmerged work as a corrected release.

## 2. Account / credential / permission requirements

- [x] Account required? No — `langgraph dev` needs no LangSmith/LangGraph Platform account for local use.
- [x] API key / credential required? No.
- [x] Paid tier/quota/entitlement required? No — everything here ran free and local.
- [x] License/ToS restriction on redistributing artifacts? LangGraph is MIT-licensed; no restriction found on redistributing sanitized logs or the patch-verification steps here.

## 3. Server startup evidence

- Startup command: `langgraph dev --no-browser --port 2024` (from `pilot_study/work/langgraph/server-project/`, which defines `langgraph.json` + a factory-style `graph.py`, matching the shape the issue reporter used).
- Startup time: ~2 seconds to "Application started up" in the server log.
- Confirmation of a real network endpoint:
  ```
  - 🚀 API: http://127.0.0.1:2024
  $ lsof -iTCP:2024 -sTCP:LISTEN -P
  Python 74173 ... TCP localhost:2024 (LISTEN)
  Python 74177 ... TCP localhost:2024 (LISTEN)
  ```
- Client used to connect: `curl`, a separate OS process from the running server.
- Sanitized request/response log excerpt:
  ```
  $ curl -s -X POST http://127.0.0.1:2024/threads -d '{}'
  {"thread_id":"01a0900d-6a8e-7d32-867e-8d5877591b9f", "status":"idle", ...}

  $ curl -s -X POST http://127.0.0.1:2024/threads/<id>/runs/wait \
      -d '{"assistant_id":"agent","input":{"messages":[["user","hello"],["ai","hi!"]]}}'
  {"messages":[{"content":"hello",...,"type":"human"},{"content":"hi!",...,"type":"ai"}]}
  ```

## 4. Task-relevant feature round trip (beyond hello-world)

- What you ran: built a minimal graph with a `DeltaChannel`-backed `messages` state (the exact channel type issue #8653 implicates), exported it as a **factory function** in `langgraph.json` (not a bare compiled graph — this is the shape that makes the server inject a checkpointer, matching how the issue reporter's app was structured). Ran the graph via `/threads/{id}/runs/wait`, then read state via `GET /threads/{id}/state`, then called `POST /threads/{id}/state` (the server's `update_state` route) with a new message, then re-read state — reproducing the issue's exact sequence of operations end-to-end over the real HTTP route.
- What you observed: the message count read back correctly at every step (2 after the initial run, 3 after `update_state`) — **the bug did not manifest** through this route. See case record §5 and §7 for why, and for the important distinction this draws between "the library has this defect" and "our accessible serving route exhibits it."
- Why this counts as more than hello-world: it exercises the exact checkpointer-resolution component the issue implicates (`get_state`/`update_state` against a `DeltaChannel`), through the real dispatch stack, with a genuinely separate client — this is real reachability evidence, even though the result was a clean pass rather than the expected fail.

## 5. Reachability of the implicated component

- Candidate case: [LangGraph issue #8653](https://github.com/langchain-ai/langgraph/issues/8653).
- Implicated component: `langgraph/pregel/main.py`'s `_prepare_state_snapshot`/`_aprepare_state_snapshot` (and `bulk_update_state`/`abulk_update_state`), specifically their checkpointer-resolution logic.
- Evidence this route reaches it: confirmed by reading `langgraph_api/graph.py`'s `get_graph()` (the function every `/threads/*` request handler calls to obtain a graph instance) — it calls the graph factory, then does `yield graph_obj.copy(update={"checkpointer": checkpointer, "store": store})`. That `.copy(update=...)` call sets `Pregel.checkpointer` directly (a public attribute), which is exactly what `_prepare_state_snapshot` reads. So yes — the served route does reach the implicated component, and does so on every request.
- **Correction to an earlier, incomplete reading of this file, recorded here rather than silently fixed:** an initial grep of `langgraph_api/graph.py` around the `CONFIG_KEY_CHECKPOINTER` injection line led to the (wrong) assumption that config-injection was the *only* checkpointer-attachment mechanism the server uses. Reading further in the same function surfaced the `.copy(update=...)` line, which also sets the checkpointer as a direct attribute on the graph object handed to every request. This is exactly why the live server did not reproduce the bug (§7) — the correction was made before finalizing this log, not after being caught out, but it's recorded because it changes the case's classification and a reviewer should be able to see the reasoning path, not just the conclusion.

## 6. Unresolved limitations

- `langgraph up` (the actual Postgres-backed production server) was **attempted and access-blocked**, not skipped. `langgraph up` printed, before doing anything else: `requires env var LANGSMITH_API_KEY with access to LangSmith Deployment` (local dev) or `LANGGRAPH_CLOUD_LICENSE_KEY` (production use). Neither credential is available, and per README §6 this is a clean access blocker to record rather than a paywall to work around — the attempt was stopped immediately (confirmed via `docker ps -a` that no `langgraph up`-spawned containers, e.g. its Redis/API-server stack, were ever created; only the standalone Postgres container used for the direct-library reproduction below was running).
- Given that blocker, the Postgres-backed checkpointer mechanism was instead tested via **direct library calls against a real, locally-run Postgres 16 container**, using the exact same `langgraph-checkpoint-postgres` package `langgraph up` would use. This produced a genuine, consequential, mode-dependent finding — see `cases/langgraph-postgres-delta-pagination-02/case_record.md`. This is a different (and separate) defect from #8653, found via `#8653`'s own "possibly related" cross-reference to issue #8448.
- The genuine LangGraph Platform managed cloud service (environment 3 per plan §2.1) was not attempted — no account/credential exists for it in this pass, and per plan §8.1 this is explicitly a separate condition from the self-hosted `langgraph dev`/`up` paths tested here. **This matters a lot for this specific case** — see case record §7: the issue reporter's claim is specifically about the managed Platform, and everything accessible to us (the open-source `langgraph-api` package) does not reproduce it.

## 7. Hour-6 status

- [x] Qualified — real serving access confirmed (`langgraph dev`, separate client, real network endpoint), reaching the exact component #8653 implicates (confirmed by source + live reproduction attempt, not assumed).
