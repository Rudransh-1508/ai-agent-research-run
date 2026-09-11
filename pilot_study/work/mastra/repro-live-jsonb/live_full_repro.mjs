// LIVE reproduction of mastra-ai/mastra #17432, combining three real
// components that were previously separate/simulated:
//   1. A REAL reasoning-model response (o3-mini via the real OpenAI
//      Responses API) carrying a genuine server-issued rs_* reasoning id.
//   2. A REAL PostgreSQL 16 round-trip of that exact data through a jsonb
//      column and a text column (not a synthetic literal typed in a
//      different key order by hand).
//   3. The REAL, installed, unpatched @mastra/core's exported
//      `CacheKeyGenerator.fromDBParts` function, called on both
//      round-tripped forms.
//
// What this does NOT reproduce: the exact production trigger path (a real
// Mastra workflow suspending on a tool-approval gate, persisting to
// mastra_workflow_snapshot while mastra_messages holds the same content).
// Orchestrating that exact integration was assessed as high-effort/high-risk
// given this pinned, dated Mastra version's undocumented-to-us internal
// workflow-persistence API, and was not attempted. What follows is the
// strongest tractable alternative: every individual real-world fact the bug
// depends on (real jsonb reordering, real reasoning data, the real function)
// is independently confirmed; only their exact production wiring together
// is not.

import { readFileSync } from 'node:fs';
import pg from 'pg';
import { Agent } from '@mastra/core/agent';
import { CacheKeyGenerator } from '@mastra/core/agent/message-list';
import { openai } from '@ai-sdk/openai';

const envPath = new URL('../../agent-framework/repro-openai-fc/.env', import.meta.url);
const envContent = readFileSync(envPath, 'utf8');
process.env.OPENAI_API_KEY = envContent.match(/OPENAI_API_KEY=(.+)/)[1].trim();

const agent = new Agent({
  name: 'live-repro-agent',
  instructions: 'You are a helpful assistant. Think step by step before answering.',
  model: openai.responses('o3-mini'),
});

console.log('Calling the real OpenAI Responses API (o3-mini) for a real reasoning response...');
const result = await agent.generate('What is 23 * 31? Show your reasoning briefly.');

const reasoningContent = result.response.messages
  .flatMap((m) => (Array.isArray(m.content) ? m.content : []))
  .find((c) => c.type === 'reasoning');

if (!reasoningContent) {
  console.log(JSON.stringify({ error: 'no reasoning content in the real response -- cannot proceed' }));
  process.exit(1);
}

const realReasoningItemId = reasoningContent.providerOptions?.openai?.itemId;
console.log('Real server-issued reasoning id:', realReasoningItemId);

// This is the exact shape CacheKeyGenerator.fromDBParts hashes for a stored
// reasoning message part -- built from REAL data (the actual itemId and
// encrypted content OpenAI returned), not a hand-typed placeholder.
const realDataPayload = {
  reasoningId: realReasoningItemId,
  encryptedContent: reasoningContent.providerOptions?.openai?.reasoningEncryptedContent ?? null,
  summary: reasoningContent.text ?? '',
};

const client = new pg.Client({ connectionString: 'postgresql://postgres:postgres@localhost:5443/mastra_test' });
await client.connect();
await client.query('CREATE TABLE IF NOT EXISTS live_jsonb_test (id serial, data jsonb)');
await client.query('CREATE TABLE IF NOT EXISTS live_text_test (id serial, data text)');
await client.query('DELETE FROM live_jsonb_test');
await client.query('DELETE FROM live_text_test');

await client.query('INSERT INTO live_jsonb_test (data) VALUES ($1)', [JSON.stringify(realDataPayload)]);
await client.query('INSERT INTO live_text_test (data) VALUES ($1)', [JSON.stringify(realDataPayload)]);

const jsonbRow = await client.query('SELECT data::text AS data FROM live_jsonb_test');
const textRow = await client.query('SELECT data FROM live_text_test');
await client.end();

const dataFromJsonb = JSON.parse(jsonbRow.rows[0].data);
const dataFromText = JSON.parse(textRow.rows[0].data);

const keyFromJsonb = CacheKeyGenerator.fromDBParts([{ type: 'data-reasoning', data: dataFromJsonb }]);
const keyFromText = CacheKeyGenerator.fromDBParts([{ type: 'data-reasoning', data: dataFromText }]);

const pass = keyFromJsonb === keyFromText;

console.log(
  JSON.stringify(
    {
      realReasoningItemId,
      rawInsertionOrderKeys: Object.keys(realDataPayload),
      keysAfterRealJsonbRoundTrip: Object.keys(dataFromJsonb),
      keysAfterRealTextRoundTrip: Object.keys(dataFromText),
      keyFromJsonb,
      keyFromText,
      pass,
      note: pass
        ? 'keys matched -- this real reasoning payload happened not to get reordered, or the installed version has the fix'
        : 'MISMATCH: the real reasoning response, round-tripped through real Postgres, produces different cache keys depending on column type -- this is the live defect',
    },
    null,
    2,
  ),
);
