import { readFileSync } from 'node:fs';

const envPath = new URL('../../agent-framework/repro-openai-fc/.env', import.meta.url);
const envContent = readFileSync(envPath, 'utf8');
const apiKey = envContent.match(/OPENAI_API_KEY=(.+)/)[1].trim();

const resp = await fetch('https://api.openai.com/v1/models', {
  headers: { Authorization: `Bearer ${apiKey}` },
});
const data = await resp.json();
const ids = data.data.map((m) => m.id).sort();
for (const id of ids) {
  if (/o1|o3|o4|gpt-5/.test(id)) console.log(id);
}
