# Access Log: Mastra

Researcher: C
Date/time started: 2026-09-11 (Hour 0)

## 1. Versions and mode

- Package/library versions: `mastra@1.29.0` (CLI, via `npx mastra`), `@mastra/core@1.66.0`, `@mastra/loggers@1.3.1` — all resolved together via `npm install @mastra/core@latest` inside the CLI project so peer versions stayed consistent. `@mastra/core@1.57.0` was tried first but is stale enough that the CLI's own `@mastra/loggers` dependency (resolved to latest, `1.3.1`) expects exports `@mastra/core@1.57.0` doesn't have (`buildLogRecordData` from `@mastra/core/logger`) — see §6 for this as a recorded limitation.
- Runtime version: Node v25.8.2 (no `.nvmrc`/engines constraint hit any incompatibility).
- Docker: not required — Mastra's built/started server is a plain Node process (`.mastra/output/index.mjs`), no container needed for this access path.
- Exact serving mode, named precisely: **"`mastra build` + `mastra start`, in-memory storage (no persistent adapter configured), single local process"** — this is environment 2 (self-hosted/official server) per plan §2.1, not environment 3 (managed cloud). Mastra Cloud/managed platform was not attempted and is out of scope for this log (plan §8.1: "managed-platform behavior remains a separate condition").
- Git/revision pin for the historical case: `@mastra/core@1.56.0` (defective, pre-#20741) and `@mastra/core@1.57.0` (corrected, post-#20748) — pinned and verified by downloading both tarballs and confirming `setRequestContext` is entirely absent from 1.56.0's built `agent-controller` bundle and fully present (all 3 entry-point call sites: send/steer, `sendNotificationSignal`, `resumeToolCall`) in 1.57.0's. See `cases/mastra-request-context-01/case_record.md` §1 for the full verification.

## 2. Account / credential / permission requirements

- [x] Account required? No — self-hosted build/start needs no Mastra account.
- [x] API key / credential required? No, for access qualification itself (server starts and routes dispatch without a model credential; a live model call would need one, but wasn't required to reach the implicated component — see §4).
- [x] Paid tier/quota/entitlement required? No — everything here ran on free, local resources per the $0 default budget.
- [x] License/ToS restriction on redistributing artifacts? Mastra is MIT-licensed (per npm registry metadata); no restriction found on redistributing sanitized request/response logs or version-pin evidence.

## 3. Server startup evidence

- Startup commands:
  ```
  npx mastra build
  npx mastra start
  ```
  (run from `pilot_study/work/mastra/server-project/`, with `@mastra/core@latest` (1.66.0) and a minimal `src/mastra/index.ts` registering one `AgentController`.)
- Startup time: build ~12s (Analyzing → Optimizing → Bundling → dependency install), start ~2-3s to first successful request.
- Confirmation the server is listening on a real network endpoint:
  ```
  $ lsof -iTCP -sTCP:LISTEN -P | grep node
  node 68260 rudranshrathore 12u IPv6 ... TCP *:4111 (LISTEN)
  ```
- Client used to connect: `curl`, a separate OS process from the running `node .mastra/output/index.mjs` server.
- Sanitized request/response log excerpt:
  ```
  $ curl -s http://localhost:4111/api/agent-controller
  {"agentControllers":[{"id":"repro"}]}

  $ curl -s -X POST http://localhost:4111/api/agent-controller/repro/sessions \
      -H "Content-Type: application/json" -d '{"resourceId":"repro-resource"}'
  {"controllerId":"repro","resourceId":"repro-resource","threadId":"dd3296e4-031a-43e0-89f0-7788c50a2b29"}
  ```

## 4. Task-relevant feature round trip (beyond hello-world)

- What you ran: after creating a session (above), sent a `POST` to the tool-approval route and the notification route — the two entry points #20741/#20748 patch — with a separate curl client:
  ```
  $ curl -s -w "\nHTTP:%{http_code}\n" -X POST \
      http://localhost:4111/api/agent-controller/repro/sessions/repro-resource/tool-approval \
      -H "Content-Type: application/json" -d '{"toolCallId":"nonexistent","approved":true}'
  {"ok":true}
  HTTP:200

  $ curl -s -w "\nHTTP:%{http_code}\n" -X POST \
      http://localhost:4111/api/agent-controller/repro/sessions/repro-resource/notifications \
      -H "Content-Type: application/json" -d '{"tagName":"system","contents":"ping"}'
  {"error":"Invalid request body","issues":[...]}
  HTTP:400
  ```
- What you observed: both routes dispatch to real request-schema validation and session-method logic (not 404s, not framework-level errors) — the 400 above is a body-shape rejection from the notification schema (it wants `source`/`kind`/`summary`, not `tagName`/`contents` — my ad hoc probe body was wrong shape, not a routing failure), and the tool-approval call executed and returned 200 even with a non-existent `toolCallId`, consistent with `respondToToolApproval` being a documented no-op when nothing is parked (session.d.ts docstring: "A no-op when nothing is awaiting approval").
- Why this counts as more than hello-world: both routes are the exact two entry points (`tool-approval`, `notifications`) that PR #20748 fixed for caller-context propagation. Hitting them from a separate client through the real dispatch stack (route → Zod validation → session method) is direct evidence the official server route reaches the implicated component's HTTP surface, not just its in-process API.

## 5. Reachability of the implicated component

- Candidate case: [Mastra PR #20741](https://github.com/mastra-ai/mastra/pull/20741) + [#20748](https://github.com/mastra-ai/mastra/pull/20748) (combined contract — see case record).
- Implicated component: `packages/core/src/agent-controller/session-run-engine.ts`'s `processSubscribedThreadStream`, and the `Session` methods (`sendMessage`/`steer`, `sendNotificationSignal`, `resumeToolCall`) that feed it a request context via `SessionRunEngine#setRequestContext`.
- Evidence this route reaches it: `/api/agent-controller/:controllerId/sessions/:resourceId/*` (notifications, tool-approval, tool-suspension, messages) are all wired to `packages/server/src/server/handlers/agent-controller.ts`, which calls the exact same `Session` methods (`session.sendNotificationSignal(...)`, `session.respondToToolApproval(...)`, `session.respondToToolSuspension(...)`) that the embedded reproduction calls directly. Confirmed by reading the handler source (not assumed) — see case record §1.
- **Important scoping note, established by reading the source rather than assumed:** the actual defect lives entirely inside `Session`/`SessionRunEngine` — the HTTP handlers are thin, and they don't add or remove any context-propagation logic of their own; they just forward a `requestContext` built from server middleware into the same session methods an embedded caller would invoke directly. This means the served route reaches the implicated component, but the defect itself is not boundary-specific — see the case record's causal note for why this matters for the embedded-vs-served framing.

## 6. Unresolved limitations

- The historical pin (`@mastra/core@1.56.0`/`1.57.0`) could not be run through the **built CLI server** as-is — `mastra build`/`start` pull `@mastra/loggers@latest`, which is incompatible with `@mastra/core@1.57.0`'s exports. Building a served (HTTP) reproduction of the *exact pinned historical pair* would require either pinning `@mastra/loggers` to a matching older release too (not attempted — lower priority given the mechanism is confirmed internal to `@mastra/core`, not boundary-specific, per §5) or vendoring a minimal custom HTTP wrapper (explicitly disallowed by plan §2.1/§8.3: "a manually written HTTP wrapper around an SDK call is not a substitute for the official serving integration"). Recorded as a scoping limitation, not a fabricated workaround.
- Mastra Cloud / managed platform: not attempted (plan §8.1 treats it as a separate condition; out of scope for this access log).
- No live model credential was used or needed for anything logged here; the deterministic/embedded reproduction (case record) isolates the mechanism without a live model call, consistent with plan §9.4's "deterministic isolation first."

## 7. Hour-6 status

- [x] Qualified — real serving access confirmed (build+start, separate client, real network endpoint), and the exercised routes reach the component implicated by PR #20741/#20748 (confirmed by source inspection of the handler wiring, §5).
