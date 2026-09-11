# Case Record: mastra-dev-environment-tag-02

Researcher: C
Framework: Mastra
Sample type: historical issue/fix
Date: 2026-09-11

## 1. Provenance

- Source: [Mastra PR #22734](https://github.com/mastra-ai/mastra/pull/22734) ("fix(core): resolve environment to development for mastra dev runs", merged 2026-09-01T08:13:16Z), fixing [issue #21941](https://github.com/mastra-ai/mastra/issues/21941). Real external bug report (filed by an outside team per the PR body), self-contained single-PR fix — no complicating follow-up like case 1's #20741→#20748.
- Defective revision pin: `@mastra/core@1.63.2` (stable release, published 2026-08-28T21:36:32Z, well before the fix).
- Corrected revision pin: `@mastra/core@1.64.0` (stable release, published 2026-09-03T04:18:34Z, after the fix). Both are **stable, non-alpha** releases (an improvement on case 1, which had to use alpha pins because no close stable bracket existed for that fix).
- **Verification method (not just timestamps):** downloaded both npm tarballs and grepped `dist/mastra-*.cjs` for the exact line the diff adds: `this.#environment = config?.environment ?? (process.env.MASTRA_DEV === "true" ? "development" : process.env.NODE_ENV)`. Absent in 1.63.2 (only pre-existing, unrelated `MASTRA_DEV` uses — log-level default and gateway-registry sync — are present); present verbatim in 1.64.0.
- Also verified directly against the CLI source (`packages/cli/src/commands/dev/dev.ts:157-164` in the cloned repo) that `mastra dev` actually spawns its server child process with `NODE_ENV: env.get('NODE_ENV') ?? 'production'` and `MASTRA_DEV: 'true'` — this is not assumed from the PR description, it's the literal `execa(...)` call.

## 2. Property contract (freeze before running)

- Property family: **observability metadata** (plan §2.2 table) — "contractually exposed accounting or trace fields survive conversion."
- Contract, derived from the PR's own doc changes (`docs/.../tracing/overview.mdx`, `docs/.../mastra-class.mdx`): if no explicit `environment` config is set, the field must either (a) stay `undefined` ("left undefined rather than guessed" — the documented behavior for a truly unconfigured/embedded run), or (b) for a run started through `mastra dev`, resolve to `'development'` — it must never surface `'production'` for what is, by construction, local development work.
- Evidence to inspect: the return value of `Mastra#getEnvironment()` under two conditions: (1) no `NODE_ENV`/`MASTRA_DEV` set (embedded baseline), and (2) the exact environment `mastra dev` actually spawns its child process with.
- Oracle: `embeddedPass = (embedded === undefined)`; `servedPass = (served === 'development')`. Per plan §2.2's own caution ("missing usage information does not, by itself, establish an incorrect bill or a failed user task"), the parallel caution applies here: a wrong tag doesn't break the user's task, so this case is scoped honestly as a metadata-family finding (see §7).

## 3. Configuration pairing

- Application code: identical harness (`repro2/embedded-repro.ts`) run unmodified against both pinned versions.
- Framework/dependency versions: pinned exactly (`@mastra/core@1.63.2` / `@1.64.0`), each verified via `require(...).version` printed in the run output before trusting the result.
- Initial state: fresh `Mastra` instance per condition, environment variables saved and restored around each condition (`withEnv` helper) so the two conditions don't leak into each other within one process run.
- Caller identity/permissions: n/a for this property family.
- Tool fixtures: n/a — no tool call involved; this exercises `Mastra`'s constructor-time environment resolution directly.
- Model configuration: n/a — no model call involved (`new Mastra({ logger: false })` only, mirroring the upstream PR's own added unit tests exactly).

## 4. Embedded execution

- Command/harness: `npx tsx embedded-repro.ts`, `embedded` branch — constructs `new Mastra({ logger: false })` with `NODE_ENV` and `MASTRA_DEV` both explicitly unset (the ambient state of a plain script/embedded SDK call with no dev-server involved).
- Result, defective (1.63.2): `embeddedEnvironmentTag` absent from output (i.e. `undefined`) → `embeddedPass: true`.
- Result, corrected (1.64.0): identical — `embeddedPass: true`.
- **Embedded execution is correct in both versions** — the bug never touches the embedded path at all, because nothing forces `NODE_ENV`/`MASTRA_DEV` there.

## 5. Served execution

- Serving mode (named precisely): the exact child-process environment `mastra dev` spawns with (`NODE_ENV: 'production'`, `MASTRA_DEV: 'true'`), applied directly to `new Mastra({ logger: false })` rather than via a running server process — see §7 for why this is a legitimate isolation of the mechanism and what a fuller live-server confirmation would still add.
- Command/harness: `npx tsx embedded-repro.ts`, `served` branch.
- Result, defective (1.63.2): `servedEnvironmentTag: "production"` → `servedPass: false`. **FAIL** — a genuinely local, in-progress development run gets tagged as if it were a production deployment.
- Result, corrected (1.64.0): `servedEnvironmentTag: "development"` → `servedPass: true`. **PASS.**
- State reset confirmed before this run: yes — each condition runs in the same process but restores the prior env-var state afterward (`withEnv`'s `finally` block), and each version comparison used a fresh `npm install` + fresh `npx tsx` process, so no state leaked between the defective and corrected runs.

## 6. Outcome classification (plan §9.5)

- [x] **Embedded pass / served fail** — on the defective revision (1.63.2).
- [x] **Embedded pass / served pass** — on the corrected revision (1.64.0).

This is the clean "local pass → served fail, then fixed" pattern plan §11.1 asks for, and case 1 (`mastra-request-context-01`) did not produce.

## 7. Causal note

- Divergence localized to: **dispatch/serving-boundary context injection**, specifically the `mastra dev` CLI (`packages/cli/src/commands/dev/dev.ts`) unconditionally overriding `NODE_ENV` to `'production'` on its spawned child process (a deliberate, documented choice — "so dependencies run in production mode" per the PR body — not itself a bug), combined with `Mastra`'s constructor (`packages/core/src/mastra/index.ts`) reading that overridden `NODE_ENV` for observability tagging without accounting for the CLI's own `MASTRA_DEV` signal that would disambiguate "this is really a dev run."
- Unlike case 1, this **is** a genuine boundary-introduced defect: the embedded path never manufactures a false signal (nothing forces `NODE_ENV` there), and the served path does — the serving route itself is the source of the divergence, not an internal defect equally reachable from both call styles.
- **Honest limitation of this reproduction:** the "served" condition here directly constructs `new Mastra({...})` under the exact environment `mastra dev` spawns its child process with, rather than running a live `mastra dev` server and inspecting an emitted trace end-to-end. This isolates the precise mechanism deterministically (plan §9.4: "use deterministic model doubles... when the framework supports them faithfully" — extended here to isolating the environment-resolution mechanism itself, since no model or tool call is involved in what this bug affects at all). The child-process environment variables were verified directly against the CLI's actual `execa(...)` call (§1), not assumed, so this isn't a fabricated substitute for the route — it's the exact input the route is confirmed to produce. A live `mastra dev` + Studio trace-store confirmation (as the PR author did manually, per the PR body: "Verified end-to-end against a live store") would strengthen this further but was not run here, given the mechanism is already fully explained by source and confirmed by version-pinned reproduction.
- **Scope discipline, matching case 1's honesty:** this is still a metadata-family finding. A mistagged trace doesn't break a user's task or corrupt state (plan §2.2's own caution, echoed in §11.1: "metadata-only observations can be retained, but cannot alone satisfy the proposed substantive-consequence gate"). Its value to the pilot is specifically that it **is** genuinely mode-dependent and boundary-introduced, which case 1 needed but didn't have — it doesn't, by itself, satisfy §11.1's "consequential" bar. Both properties (mode-dependent *and* consequential) still need to come from somewhere in the sample; this case supplies the first, not the second.

## 8. Adjudication (filled by a second researcher, not the case author)

- Adjudicator: {{pending — Researcher A or B, not yet reviewed as of this record's writing}}
- Cause classification: {{pending}}
- Adjudicator notes: {{pending}}

## 9. Test-configuration comparison (if this case is part of the Hours 36-60 sample)

| Configuration | Detected this outcome? | Notes |
|---|---|---|
| Local baseline (pre-#22734 test suite) | No | `environment.test.ts` before the PR only covered the explicit-config and bare-`NODE_ENV`-fallback cases; no test constructed `Mastra` under `mastra dev`'s actual spawn environment (`NODE_ENV=production` + `MASTRA_DEV=true` together). |
| Boundary-focused tests (this study's harness) | Yes | Detected specifically by reproducing the CLI's real spawn-environment values against the constructor — a test that models the *serving route's actual behavior*, not just the framework's internal API in isolation. |
| Fuller E2E reference (live `mastra dev` + Studio trace store) | Not run | Would confirm end-to-end (as the PR author did manually) but isn't needed to establish the mechanism, which is already fully pinned and explained; noted as a possible strengthening step, not a gap in the causal claim. |
