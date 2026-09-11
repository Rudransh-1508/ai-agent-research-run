// Reproduction of mastra-ai/mastra issue #17432 / PR #17439:
// "use stable key-order-independent stringify in CacheKeyGenerator to fix
// duplicate rs_* on tool-approval resume."
//
// Mechanism, confirmed directly against the installed @mastra/core dist
// (both pinned versions): CacheKeyGenerator.fromDBParts hashes `data-*`
// message parts with plain JSON.stringify, which is key-order-sensitive.
// PostgreSQL's `jsonb` column (mastra_workflow_snapshot) normalizes object
// key order on round-trip; the `text` column (mastra_messages) preserves
// insertion order. So a message restored via the jsonb path and the same
// message restored via the text path -- functionally identical -- produce
// DIFFERENT cache keys, `messagesAreEqual` reports them as different, and
// `MessageList.addOne` mints a duplicate copy carrying the same
// OpenAI-issued `rs_*` reasoning id -- which OpenAI's API then rejects as a
// duplicate item.
//
// "Embedded" here = in-memory/text-column storage, which always preserves
// insertion order (key order never actually changes, so the bug can't
// manifest). "Served, production-shaped" = @mastra/pg's jsonb-backed
// storage, which normalizes key order on every round trip through
// PostgreSQL -- this reproduction simulates that normalization directly
// (object key order really does change after a real jsonb round trip; this
// is standard, well-known PostgreSQL jsonb behavior, not fabricated), since
// standing up a full Postgres instance isn't needed to exercise the exact
// hashing function that's actually defective.

import { CacheKeyGenerator, messagesAreEqual } from '@mastra/core/agent/message-list';

// The same logical data payload, restored in two different key orders --
// exactly what a `text` column (insertion order preserved) vs a `jsonb`
// column (key order normalized, typically alphabetical) would each hand
// back for the same underlying JSON value.
const dataInsertionOrder = { reasoningId: 'rs_abc123', summary: 'thinking...', encrypted: false };
const dataJsonbNormalizedOrder = { encrypted: false, reasoningId: 'rs_abc123', summary: 'thinking...' };

function buildPart(data) {
  return [{ type: 'data-reasoning', data }];
}

const keyFromText = CacheKeyGenerator.fromDBParts(buildPart(dataInsertionOrder));
const keyFromJsonb = CacheKeyGenerator.fromDBParts(buildPart(dataJsonbNormalizedOrder));

// Contract (plan §2.2, "state continuity"): the same logical message,
// restored from either storage backend, must produce the same cache key --
// otherwise MessageList.addOne treats it as a new message and mints a
// duplicate carrying the same server-issued reasoning id, which OpenAI
// rejects.
const sameStorageKeysMatch = keyFromText === CacheKeyGenerator.fromDBParts(buildPart(dataInsertionOrder));
const crossStorageKeysMatch = keyFromText === keyFromJsonb;

console.log(
  JSON.stringify(
    {
      mastraCoreVersion: (await import('@mastra/core/package.json', { with: { type: 'json' } })).default.version,
      singleBackendConsistency: { pass: sameStorageKeysMatch },
      crossBackendConsistency_textVsJsonbKeyOrder: {
        keyFromText,
        keyFromJsonb,
        pass: crossStorageKeysMatch,
        consequenceIfFail:
          'MessageList.addOne treats these as different messages and mints a duplicate carrying the same rs_* reasoning id; OpenAI rejects the request as a duplicate item',
      },
    },
    null,
    2,
  ),
);
