# Access Log: Microsoft Agent Framework

Researcher: B (executed on their behalf per team request)
Date/time started: 2026-09-11

## 1. Versions and mode

- Package/library versions: `agent-framework==1.18.0` (core), `agent-framework-foundry-hosting` — tested at two pins: `1.0.0b260813` (defective) and `1.0.0b260910`/`1.0.0b260827` (corrected, both confirmed to contain the fix — see case record §1), `azure-ai-agentserver-core==2.1.0`, `azure-ai-agentserver-responses==2.2.0b1` (resolved as dependencies).
- Runtime version: Python 3.11.0, isolated venv at `pilot_study/work/agent-framework/venv/`.
- Docker: not needed for this framework's access path.
- Exact serving mode, named precisely: **self-hosted `agent_framework_foundry_hosting.ResponsesHostServer`, run as a standalone local process (`hypercorn`-backed ASGI server via `.run()`)** — this is a **self-hosted OpenAI-compatible `/responses` server that implements the same protocol Azure AI Foundry's managed hosting expects**, not Azure's actual managed cloud service. This distinction is the single most important thing to keep straight for this case (plan §2.1 environment 2 vs. 3) — see §5 and the case record §7.
- Git/revision pin for the historical case: `agent-framework-foundry-hosting==1.0.0b260813` (defective, published 2026-08-14) → `1.0.0b260827` (corrected, published 2026-08-28) — verified via wheel content, not just publish timestamps (see case record §1).

## 2. Account / credential / permission requirements

- [x] Account required? **No** — `ResponsesHostServer` runs entirely locally with no Azure account, no Azure AI Foundry project, and no Azure subscription. This was confirmed empirically (the server started and served real requests with zero Azure configuration), not assumed from documentation.
- [x] API key / credential required? No API key of any kind was needed — the deterministic chat client (`repro/deterministic_chat_client.py`) makes no live model call, so no OpenAI/Azure OpenAI key was needed either.
- [x] Paid tier/quota/entitlement required? No — this ran entirely free and local, consistent with the $0 default budget.
- [x] License/ToS restriction on redistributing artifacts? `agent-framework` and `agent-framework-foundry-hosting` are MIT-licensed; no restriction found.
- **The team offered to supply LangSmith/LangGraph Cloud/other credentials if needed for this framework's access — none were needed.** The self-hosted path fully qualified without any external account. If the team specifically wants confirmation against Azure's actual managed AI Foundry cloud service (a distinct, separate condition per plan §8.1), that would need a real Azure subscription with an AI Foundry project and deployed model — not attempted here, and not required for the finding below (see case record §7 for why the self-hosted result is expected to generalize).

## 3. Server startup evidence

- Startup command: `python server.py` (from `pilot_study/work/agent-framework/repro/`), which constructs an `Agent` backed by a deterministic (no-network) chat client and hosts it via `ResponsesHostServer(agent).run(host="127.0.0.1", port=8088)`.
- Startup time: ~1 second to "Running on http://127.0.0.1:8088" in the server log (a handful of harmless warnings precede it — an OpenTelemetry auto-instrumentation import error unrelated to this framework, and an Azure Instance Metadata Service probe that times out after 0.2s since this isn't running on Azure infrastructure — neither affects server function).
- Confirmation of a real network endpoint:
  ```
  $ lsof -iTCP:8088 -sTCP:LISTEN -P
  Python 79060 ... TCP localhost:8088 (LISTEN)
  ```
- Client used to connect: a separate Python process using the official `openai` PyPI package's client (`OpenAI(base_url=..., api_key="sk-test")`), exactly matching the issue's own code sample — not a plain-`curl` or hand-rolled HTTP client.
- Sanitized request/response log excerpt (corrected version, `1.0.0b260910`):
  ```python
  resp = client.responses.create(model="repro-agent", input="Hello", stream=False)
  # resp.usage -> ResponseUsage(input_tokens=100, output_tokens=25, total_tokens=125, ...)
  # resp.output_text -> "hi from the deterministic chat client"
  ```

## 4. Task-relevant feature round trip (beyond hello-world)

- What you ran: a full request/response round trip through the OpenAI-compatible `/responses` endpoint the issue's own code sample targets — `client.responses.create(model=..., input=..., stream=False)` — against an agent whose backing chat client deterministically reports a fixed usage total (`input_token_count=100, output_token_count=25, total_token_count=125`), so the oracle doesn't depend on any live model's nondeterministic token counts.
- What you observed: on the pinned defective package version, `resp.usage` is `None` even though the agent's own response and the deterministic chat client both carried usage; on the corrected version, `resp.usage` correctly reports the fixed totals. See case record for the full embedded/served comparison.
- Why this counts as more than hello-world: it exercises the exact usage-aggregation-then-emit-completed code path the issue names, through the real HTTP protocol layer (OpenAI SDK → HTTP → `ResponsesHostServer` routing → agent invocation → response conversion), not a direct method call.

## 5. Reachability of the implicated component

- Candidate case: [Agent Framework issue #7416](https://github.com/microsoft/agent-framework/issues/7416).
- Implicated component: `agent_framework_foundry_hosting/_responses.py`'s response-completion handlers (the non-streaming and streaming regular-agent paths, and the failure path), specifically their calls to `response_event_stream.emit_completed(...)` / `emit_failed(...)`.
- Evidence this route reaches it: confirmed directly — the served (HTTP) request's response omitted usage on the defective pin and included it on the corrected pin, with the only variable being the installed package version, exactly matching what the issue's own diff-referenced line numbers describe.
- **Naming the exact serving mode precisely, per plan §2.1/§8.3 and the brief's own watch-out:** what was tested here is the **self-hosted `ResponsesHostServer`**, which implements the OpenAI-Foundry-compatible `/responses` protocol. It is **not** Azure's managed AI Foundry cloud service. The package name ("Foundry Hosting") refers to protocol compatibility, not to running on Azure's infrastructure — this was confirmed empirically, not assumed, by the fact that the server started and served correctly with zero Azure configuration present. Do not read this case's "served" result as a managed-cloud finding; it is a self-hosted (environment 2) finding. See case record §7 for the reasoning on why this is nonetheless likely to generalize to environment 3, stated as an assessment, not a confirmed fact.

## 6. Unresolved limitations

- The actual Azure AI Foundry **managed cloud** service (environment 3) was not tested — no Azure subscription/credentials were used or required for the finding above. If the team wants this confirmed independently, it would need a real Azure AI Foundry project deployment; this is a deliberate scope boundary, not an oversight (plan §8.1 treats managed-platform behavior as a separate condition from the self-hosted path).
- Streaming (`stream=True`) was not independently reproduced through the server, only non-streaming — the issue states both are affected, and the non-streaming reproduction alone is sufficient to establish the mechanism (same underlying usage-aggregation-then-emit code the issue's own diff names covers both paths in the same file). Streaming reproduction would strengthen this further but wasn't necessary to establish the finding.
- The second candidate case from the brief, [Azure SDK #46696](https://github.com/Azure/azure-sdk-for-python/issues/46696) (MCP on-behalf-of token exchange failing under Foundry deployment), was **not attempted**. It's specifically about a managed-Foundry-deployment token-exchange flow, which by its nature requires actual Azure identity/OBO configuration to test meaningfully — a local-only reproduction would risk exactly what plan §4 warns against ("a locally fabricated identity context cannot validate this cloud-specific claim"). Deprioritized in favor of the tractable, credential-free #7416 case; left for the team to decide whether it's worth pursuing with real Azure access.

## 7. Hour-6 status

- [x] Qualified — real serving access confirmed (self-hosted `ResponsesHostServer`, separate client via the official OpenAI SDK, real network endpoint), reaching and reproducing the exact defect #7416 describes, with zero external credentials required.
