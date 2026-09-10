# Access Log: {{FRAMEWORK NAME}}

Researcher: {{name}}
Date/time started: {{iso timestamp}}

Fill this in live during Hours 0-6. Do not backfill from memory at Hour 6 — write each item as you
do it. See research plan §8.2 for the required evidence list this template is built from.

## 1. Versions and mode

- Package/library version(s): {{e.g. langgraph==X.Y.Z, langgraph-cli==X.Y.Z}}
- Runtime version: {{python/node version}}
- Docker image/tag if applicable: {{...}}
- Exact serving mode, named precisely: {{e.g. "langgraph dev, in-memory checkpointer" vs.
  "langgraph up, Postgres-backed" — do not just say "local"}}
- Git/revision pin if reproducing a historical case: {{commit sha or release tag}}

## 2. Account / credential / permission requirements

- [ ] Account required? {{yes/no + which}}
- [ ] API key / credential required? {{yes/no — record that one exists and was obtained, not the
  value}}
- [ ] Any paid tier, quota, or entitlement required? {{yes/no — if yes and no free tier exists,
  STOP and record as a budget blocker per README §6, do not pay without approval}}
- [ ] Any license/ToS restriction relevant to redistributing artifacts later? {{note it}}

## 3. Server startup evidence

- Startup command: {{exact command}}
- Startup time: {{seconds}}
- Confirmation the server is listening on a real network endpoint: {{curl/log excerpt, sanitized}}
- Client used to connect: {{must be a separate process from the server — name it}}
- Sanitized request/response log excerpt:

```
{{paste}}
```

## 4. Task-relevant feature round trip (beyond hello-world)

Describe the one non-trivial round trip you ran (e.g., context reaching an isolated tool, a
follow-up request reading session state, an approval continuation through the public route).

- What you ran: {{...}}
- What you observed: {{...}}
- Why this counts as more than hello-world: {{...}}

## 5. Reachability of the implicated component

Which candidate case (from research plan §4) does this framework map to, and does the route you
just exercised actually reach the component that case implicates (e.g., the checkpointer
reconstruction path, the Foundry response-conversion path, the caller-context wiring)?

- Candidate case: {{issue/PR link}}
- Implicated component: {{...}}
- Evidence this route reaches it: {{...}}
- If it does NOT reach it yet: what's missing, and is it fixable within Hours 0-6? {{...}}

## 6. Unresolved limitations

{{Anything left uncertain — a feature you couldn't test, a config you're unsure is correct, a
question for the team.}}

## 7. Hour-6 status

- [ ] Qualified — real serving access confirmed, reaches implicated component
- [ ] Partially qualified — server runs, but does not yet reach implicated component
- [ ] Blocked — reason: {{...}}
