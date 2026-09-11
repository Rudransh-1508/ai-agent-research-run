// Embedded (in-process) reproduction of the request-context-loss mechanism
// behind mastra-ai/mastra PR #20741 / #20748 ("preserve caller context for
// stream approvals" + "set the caller context on every subscription entry
// point").
//
// Mechanism (confirmed by reading packages/core/src/agent-controller/session.ts
// and session-run-engine.ts at the pinned commits): when an approval decision
// arrives as a `tool-call-approval` chunk on a session's *subscribed* thread
// stream (the channel used to deliver runs/events across the async
// subscription boundary — the same boundary a multi-instance/pubsub-backed
// deployment relies on), the engine used to build the request context once,
// at subscription-open time, and never refresh it. Any caller identity set
// by a later entry point (a notification signal, a resume, a fresh send)
// was invisible to that in-flight approval processing.
//
// This script exercises the same public entry points the upstream
// regression tests use (`sendNotificationSignal`, `session.stream.attach`,
// `session.processSubscribedThreadStream`) to answer one question
// deterministically: when a `tool-call-approval` chunk is processed, which
// caller identity does the resulting `approveToolCall` invocation carry?
//
// Run against @mastra/core 1.56.0 (defective, pre-#20741) and 1.57.0
// (corrected, post-#20748) — see ACCESS_LOG.md for how those pins were
// verified against the actual published dist output, not just timestamps.

import { AgentController } from '@mastra/core/agent-controller';
import { Agent } from '@mastra/core/agent';
import { RequestContext } from '@mastra/core/request-context';
import { InMemoryStore } from '@mastra/core/storage';
import { Workspace } from '@mastra/core/workspace';
import { readFileSync } from 'node:fs';

async function main() {
  const agent = new Agent({
    id: 'repro-agent',
    name: 'repro-agent',
    instructions: 'Test agent for request-context reproduction.',
    model: { provider: 'openai', name: 'gpt-4o', toolChoice: 'auto' } as any,
  });

  const controller = new AgentController({
    id: 'repro-controller',
    storage: new InMemoryStore(),
    modes: [{ id: 'default', name: 'Default', default: true, agent }],
    // Skills-only config: no fs/sandbox/search engine required, so init() is a no-op.
    workspace: new Workspace({ name: 'repro-workspace', skills: ['/tmp/repro-skills'] }),
  });

  await controller.init();
  const session: any = await controller.createSession({ id: 'repro-session', ownerId: 'repro-owner' });

  // Allow the tool outright so `resolveToolApproval` short-circuits to
  // "allow" inside processSubscribedThreadStream, isolating the request-
  // context propagation mechanism from the interactive approval UI.
  await session.permissions.setForTool({ toolName: 'record_context', policy: 'allow' });

  // Record what context each approved tool-call invocation actually carried,
  // by wrapping the real `approveToolCall` (this is exactly the method the
  // upstream regression tests assert against). The wrapper still calls
  // through so any other side effects run normally; it declines instead of
  // erroring since there's no genuinely pending tool call in this isolated
  // harness (the causal question is *what context reaches this call*, not
  // whether the call fully completes).
  const calls: Array<{ toolCallId: string; callerId?: string; hadContext: boolean }> = [];
  const originalApproveToolCall = session.approveToolCall.bind(session);
  session.approveToolCall = async (args: { toolCallId: string; requestContext?: RequestContext }) => {
    calls.push({
      toolCallId: args.toolCallId,
      callerId: args.requestContext?.get('user')?.id,
      hadContext: args.requestContext !== undefined,
    });
    return undefined; // isolate: don't exercise real completion machinery
  };
  void originalApproveToolCall;

  // Step 1: a message is sent under caller A's identity (the "previous send"
  // the upstream bug report describes as the stale context a later approval
  // could fall back to).
  const contextA = new RequestContext();
  contextA.set('user', { id: 'caller-A' });
  if (typeof session.runEngine.setRequestContext === 'function') {
    // Public on the corrected revision; absent entirely pre-fix (there was
    // no per-session slot to update at all before #20741).
    session.runEngine.setRequestContext(contextA);
  }

  // Step 2: a *different* caller (B) sends a notification signal — a real,
  // unmocked entry point that (post-fix) updates the engine's tracked
  // request context before the subscription is (re)ensured.
  const contextB = new RequestContext();
  contextB.set('user', { id: 'caller-B' });
  await session.sendNotificationSignal({ tagName: 'system', contents: 'ping' } as any, { requestContext: contextB }).catch(() => undefined);

  // Step 3: simulate an approval arriving on the subscribed thread stream —
  // the exact scenario #20741/#20748 target. This mirrors the upstream
  // regression tests' own technique (a hand-built AgentThreadSubscription),
  // since faithfully reproducing real multi-instance pubsub delivery is out
  // of scope for an isolated causal probe.
  const chunks = [
    { type: 'start', runId: 'run-a' },
    { type: 'tool-call-approval', runId: 'run-a', payload: { toolCallId: 'tool-call-1', toolName: 'record_context', args: {} } },
    { type: 'finish', runId: 'run-a', payload: { stepResult: { reason: 'stop' } } },
  ];
  const subscription = {
    stream: (async function* () {
      for (const chunk of chunks) yield chunk;
    })(),
    activeRunId: () => 'run-a',
    abort: () => true,
    unsubscribe: () => {},
  };
  session.stream.attach({ subscription, key: 'repro-agent:repro-resource:repro-thread' });
  await session.processSubscribedThreadStream(subscription);

  console.log(JSON.stringify({ mastraCoreVersion: getVersion(), approveToolCallInvocations: calls }, null, 2));
}

function getVersion(): string {
  return JSON.parse(readFileSync(new URL('./node_modules/@mastra/core/package.json', import.meta.url), 'utf8')).version;
}

main().catch(err => {
  console.error('FATAL:', err);
  process.exit(1);
});
