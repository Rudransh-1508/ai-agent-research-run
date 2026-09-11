// Embedded vs. served reproduction of mastra-ai/mastra PR #22734 / issue
// #21941: "mastra dev" spawns its dev server with NODE_ENV=production
// (deliberately, so dependencies run in production mode), but
// Mastra.getEnvironment() fell back to raw process.env.NODE_ENV for
// observability tagging — so identical application code produced traces
// tagged environment:"production" when run through the served `mastra dev`
// route, and environment:"development" (or undefined) when run directly/
// embedded, even though both are the same local development work.
//
// Mechanism confirmed by reading packages/core/src/mastra/index.ts (the
// `#environment` assignment in the Mastra constructor) and
// packages/cli/src/commands/dev/dev.ts (the child-process env the `mastra
// dev` CLI actually spawns with: NODE_ENV defaults to 'production',
// MASTRA_DEV is always 'true').
//
// Run against @mastra/core 1.63.2 (defective, pre-#22734) and 1.64.0
// (corrected, post-#22734) — see ACCESS_LOG.md for the dist-content
// verification of this pin (not just npm publish timestamps).

import { Mastra } from '@mastra/core';

function getVersion(): string {
  return JSON.parse(readFileSync(new URL('./node_modules/@mastra/core/package.json', import.meta.url), 'utf8')).version;
}

import { readFileSync } from 'node:fs';

function withEnv<T>(vars: Record<string, string | undefined>, fn: () => T): T {
  const saved: Record<string, string | undefined> = {};
  for (const k of Object.keys(vars)) saved[k] = process.env[k];
  for (const [k, v] of Object.entries(vars)) {
    if (v === undefined) delete process.env[k];
    else process.env[k] = v;
  }
  try {
    return fn();
  } finally {
    for (const [k, v] of Object.entries(saved)) {
      if (v === undefined) delete process.env[k];
      else process.env[k] = v;
    }
  }
}

// EMBEDDED condition: a developer's own script, calling the agent/Mastra
// instance directly in-process. Nothing sets NODE_ENV or MASTRA_DEV — this
// is the ambient state of a plain `tsx`/`node` invocation on a dev machine.
const embedded = withEnv({ NODE_ENV: undefined, MASTRA_DEV: undefined }, () => {
  const mastra = new Mastra({ logger: false });
  return mastra.getEnvironment();
});

// SERVED condition: the exact environment `mastra dev` actually spawns its
// child process with (verified directly against
// packages/cli/src/commands/dev/dev.ts in the cloned source: `NODE_ENV:
// env.get('NODE_ENV') ?? 'production'`, `MASTRA_DEV: 'true'`).
const served = withEnv({ NODE_ENV: 'production', MASTRA_DEV: 'true' }, () => {
  const mastra = new Mastra({ logger: false });
  return mastra.getEnvironment();
});

// Contract (from the PR's own docs changes + changeset, not assumed): an
// unconfigured run must never surface a *misleading* environment tag.
// Embedded, with nothing set, leaving the field undefined ("rather than
// guessed") satisfies that. Served via `mastra dev` — genuinely local
// development work — satisfies it only by resolving to 'development', not
// by inheriting the dev-server's internal NODE_ENV=production override.
const embeddedPass = embedded === undefined; // documented "leave undefined rather than guess" behavior
const servedPass = served === 'development'; // the actual, real-world contract mastra dev must meet

console.log(
  JSON.stringify(
    {
      mastraCoreVersion: getVersion(),
      embeddedEnvironmentTag: embedded,
      servedEnvironmentTag: served,
      embeddedPass,
      servedPass,
    },
    null,
    2,
  ),
);
