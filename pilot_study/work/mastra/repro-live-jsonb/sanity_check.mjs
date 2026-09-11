import { readFileSync } from 'node:fs';
import { Agent } from '@mastra/core/agent';
import { openai } from '@ai-sdk/openai';

const envPath = new URL('../../agent-framework/repro-openai-fc/.env', import.meta.url);
const envContent = readFileSync(envPath, 'utf8');
process.env.OPENAI_API_KEY = envContent.match(/OPENAI_API_KEY=(.+)/)[1].trim();

const agent = new Agent({
  name: 'sanity-agent',
  instructions: 'You are a helpful assistant. Think step by step before answering.',
  model: openai.responses('o3-mini'),
});

const result = await agent.generate('What is 17 * 24? Show your reasoning briefly.');
console.log('text:', result.text);
console.log('response messages:', JSON.stringify(result.response?.messages ?? result, null, 2).slice(0, 3000));
