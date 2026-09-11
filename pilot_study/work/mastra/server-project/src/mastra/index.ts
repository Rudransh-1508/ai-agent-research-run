import { Mastra } from '@mastra/core';
import { AgentController } from '@mastra/core/agent-controller';
import { Agent } from '@mastra/core/agent';
import { InMemoryStore } from '@mastra/core/storage';
import { Workspace } from '@mastra/core/workspace';

const agent = new Agent({
  id: 'repro-agent',
  name: 'repro-agent',
  instructions: 'Test agent for request-context access qualification.',
  model: { provider: 'openai', name: 'gpt-4o', toolChoice: 'auto' } as any,
});

const repro = new AgentController({
  id: 'repro-controller',
  storage: new InMemoryStore(),
  modes: [{ id: 'default', name: 'Default', default: true, agent }],
  workspace: new Workspace({ name: 'repro-workspace', skills: ['/tmp/repro-skills'] }),
});

export const mastra = new Mastra({
  agentControllers: { repro },
});
