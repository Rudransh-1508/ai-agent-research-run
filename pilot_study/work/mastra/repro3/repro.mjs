// Reproduction of mastra-ai/mastra issue #18877: MastraStateAdapter's
// dedupe cache is a per-process in-memory Map, so two server instances
// behind a load balancer both "win" the dedupe race for the same inbound
// Slack event and both reply.
//
// Mechanism confirmed directly in the installed @mastra/core (current
// latest) bundle: `MastraStateAdapter`'s `cache` field is
// `new Map()` assigned per-instance in the constructor, and `setIfNotExists`
// only ever reads/writes that instance's own Map -- there is no shared-store
// path at all in the installed version (constructor takes exactly 2
// arguments: memoryStore, getOwnerId).
//
// "Embedded" here means a single server instance/process -- the adapter's
// own Map correctly dedupes repeated calls to the SAME instance. "Served,
// production-shaped" means 2+ instances behind a load balancer, each with
// its own MastraStateAdapter -- exactly the topology the issue reports.

import { MastraStateAdapter } from '@mastra/core/channels';

const DEDUPE_KEY = 'dedupe:slack:msg_123';
const CLAIM = { instanceId: 'placeholder' };

// A no-op stand-in for MemoryStorage: confirmed by reading the installed
// bundle that the constructor never calls any method on it, and neither do
// get/set/setIfNotExists (only thread-subscription methods touch it, which
// this reproduction doesn't exercise).
const fakeMemoryStore = {};

async function singleInstanceScenario() {
  // One adapter instance, two inbound events for the same message (Slack's
  // own duplicate delivery: app_mention + message.channels) -- the embedded/
  // single-process case.
  const adapter = new MastraStateAdapter(fakeMemoryStore);
  const firstClaim = await adapter.setIfNotExists(DEDUPE_KEY, { ...CLAIM, instanceId: 'A' });
  const secondClaim = await adapter.setIfNotExists(DEDUPE_KEY, { ...CLAIM, instanceId: 'A' });
  return { firstClaim, secondClaim, repliesSent: [firstClaim, secondClaim].filter(Boolean).length };
}

async function multiInstanceScenario() {
  // Two SEPARATE adapter instances (one per server process), each receiving
  // one of Slack's two duplicate-delivery events for the SAME message id --
  // the served, load-balanced-production case the issue reports.
  const instanceA = new MastraStateAdapter(fakeMemoryStore);
  const instanceB = new MastraStateAdapter(fakeMemoryStore);
  const claimA = await instanceA.setIfNotExists(DEDUPE_KEY, { ...CLAIM, instanceId: 'A' });
  const claimB = await instanceB.setIfNotExists(DEDUPE_KEY, { ...CLAIM, instanceId: 'B' });
  return { claimA, claimB, repliesSent: [claimA, claimB].filter(Boolean).length };
}

const single = await singleInstanceScenario();
const multi = await multiInstanceScenario();

// Contract (plan §2.2, "state continuity" / approval-adjacent dedupe
// semantics): the same logical inbound message must be claimed by at most
// one dedupe check, regardless of how many server instances are running.
const singlePass = single.repliesSent === 1;
const multiPass = multi.repliesSent === 1;

console.log(
  JSON.stringify(
    {
      mastraCoreVersion: (await import('@mastra/core/package.json', { with: { type: 'json' } })).default.version,
      singleInstance: { ...single, pass: singlePass },
      multiInstance: { ...multi, pass: multiPass },
    },
    null,
    2,
  ),
);
