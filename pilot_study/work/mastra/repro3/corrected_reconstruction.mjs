// Reconstruction of the RELEVANT PORTION of unmerged PR #22516's fix,
// built directly from its diff (fetched fresh via
// `curl -sL https://github.com/mastra-ai/mastra/pull/22516.diff`), NOT the
// actual patched @mastra/core class -- no released or built version of the
// fix exists to install. This is labeled explicitly as a reconstruction so
// it is never confused with a verified installed-package result the way
// every other reproduction in this pilot is.
//
// The diff's actual change to MastraStateAdapter.setIfNotExists:
//
//   async setIfNotExists(key, value, ttlMs) {
//     if (this.channelsStore) {
//       return this.channelsStore.setStateIfNotExists(this.stateOwnerId(), key, value, this.deadlineFrom(ttlMs));
//     }
//     ... (unchanged in-memory fallback below)
//   }
//
// i.e. when a `channelsStore` is supplied, the dedupe claim is delegated to
// it instead of the adapter's own private Map. The new `ChannelsStorage`
// interface's `setStateIfNotExists` is meant to be backed by an atomic
// conditional write in real storage (Postgres `INSERT ... ON CONFLICT`,
// etc.) -- this reconstruction stands in a plain shared JS Map for that,
// which is a faithful analogue for "exactly one instance wins" semantics
// (JS's single-threaded execution makes a Map.has-then-set check atomic
// within one process, the same guarantee an atomic DB constraint gives
// across processes).

class ReconstructedSharedChannelsStore {
  #state = new Map();
  async setStateIfNotExists(ownerId, key, value, expiresAt) {
    const fullKey = `${ownerId}:${key}`;
    if (this.#state.has(fullKey)) return false;
    this.#state.set(fullKey, { value, expiresAt });
    return true;
  }
}

class ReconstructedCorrectedStateAdapter {
  #cache = new Map();
  #channelsStore;
  constructor(memoryStore, getOwnerId, channelsStore) {
    this.getOwnerId = getOwnerId;
    this.#channelsStore = channelsStore;
  }
  #stateOwnerId() {
    return this.getOwnerId?.() ?? '__unscoped__';
  }
  async setIfNotExists(key, value, ttlMs) {
    if (this.#channelsStore) {
      return this.#channelsStore.setStateIfNotExists(this.#stateOwnerId(), key, value, ttlMs ? Date.now() + ttlMs : null);
    }
    if (this.#cache.has(key)) return false;
    this.#cache.set(key, value);
    return true;
  }
}

const DEDUPE_KEY = 'dedupe:slack:msg_123';

async function multiInstanceScenarioCorrected() {
  // Two instances, but now sharing one ChannelsStorage-backed store -- the
  // realistic production shape post-fix, where all instances point at the
  // same real database.
  const sharedStore = new ReconstructedSharedChannelsStore();
  const instanceA = new ReconstructedCorrectedStateAdapter({}, undefined, sharedStore);
  const instanceB = new ReconstructedCorrectedStateAdapter({}, undefined, sharedStore);
  const claimA = await instanceA.setIfNotExists(DEDUPE_KEY, { instanceId: 'A' });
  const claimB = await instanceB.setIfNotExists(DEDUPE_KEY, { instanceId: 'B' });
  return { claimA, claimB, repliesSent: [claimA, claimB].filter(Boolean).length };
}

const result = await multiInstanceScenarioCorrected();
const pass = result.repliesSent === 1;
console.log(JSON.stringify({ reconstructedCorrectedMultiInstance: { ...result, pass } }, null, 2));
