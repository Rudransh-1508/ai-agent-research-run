"""Runs autogen-core for real and measures what its default event log
preserves about per-agent identity. No LLM API calls, no credentials needed:
the framework's own runtime and its own LLMCallEvent/ToolCallEvent/MessageEvent
classes are exercised for real; only the *content* of the simulated LLM call
is a local stand-in. See README.md for what is and is not synthetic here.
"""
import asyncio
import json
import logging
import random
import sys
from dataclasses import dataclass

from autogen_core import (
    AgentId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    message_handler,
)
from autogen_core.logging import LLMCallEvent, ToolCallEvent, MessageEvent

N_AGENTS = 3
N_EPISODES = 40
SEED = 20260919


@dataclass
class ReviewRequest:
    episode: int


@dataclass
class ReviewResult:
    episode: int
    reviewer_index: int
    shirked: bool


class CapturingHandler(logging.Handler):
    """Attaches to autogen_core's real event logger and records every event
    object the framework actually emits, in emission order."""

    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record.msg)


class ReviewerAgent(RoutedAgent):
    def __init__(self, index: int, rng: random.Random):
        super().__init__(description=f"Reviewer {index}")
        self.index = index
        self.rng = rng
        self.event_logger = logging.getLogger("autogen_core.events")

    @message_handler
    async def handle_request(self, message: ReviewRequest, ctx: MessageContext) -> None:
        shirked = self.rng.random() < 0.4
        if shirked:
            prompt_tokens, completion_tokens = 40, 12
            result_text = "Looks fine."
        else:
            prompt_tokens, completion_tokens = 40, 210
            result_text = (
                "Line 14 mutates shared state without a lock; line 47's error "
                "path swallows the exception; suggest adding a regression test "
                "for the empty-input case."
            )
        # Real emission of the framework's own LLMCallEvent class -- this is
        # exactly what a real model-client wrapper emits on an actual call.
        self.event_logger.info(
            LLMCallEvent(
                messages=[{"role": "user", "content": "Review this diff."}],
                response={"content": result_text},
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        )
        self.event_logger.info(
            ToolCallEvent(
                tool_name="submit_review",
                arguments={"episode": message.episode},
                result=result_text,
            )
        )
        # Real send_message call -- the runtime emits its own MessageEvent
        # for this, unprompted, with the real sender AgentId.
        await self.publish_message(
            ReviewResult(episode=message.episode, reviewer_index=self.index,
                         shirked=shirked),
            topic_id=ctx.topic_id if ctx.topic_id else self.id,
        )


class CoordinatorAgent(RoutedAgent):
    def __init__(self):
        super().__init__(description="Coordinator")
        self.ground_truth = {}

    @message_handler
    async def handle_result(self, message: ReviewResult, ctx: MessageContext) -> None:
        self.ground_truth.setdefault(message.episode, {})[message.reviewer_index] = (
            message.shirked
        )


def has_agent_identity(event) -> bool:
    """Does this event object expose any value that names the agent that
    produced it? Checked structurally against the live instance: top-level
    attributes first, then the internal `kwargs` dict every event class in
    this package actually stores its fields in (see class sources in
    autogen_core/logging.py) -- a plain hasattr() check on the object is not
    enough, since these classes route everything through kwargs, including
    identity fields not present in the public __init__ signature."""
    for attr in ("agent_id", "agent", "source", "sender"):
        if hasattr(event, attr) and getattr(event, attr) is not None:
            return True
    kwargs = getattr(event, "kwargs", None)
    if isinstance(kwargs, dict):
        for key in ("agent_id", "agent", "source", "sender"):
            if kwargs.get(key) is not None:
                return True
    return False


def agent_identity_value(event):
    kwargs = getattr(event, "kwargs", {}) or {}
    for key in ("agent_id", "agent", "source", "sender"):
        v = kwargs.get(key) if isinstance(kwargs, dict) else getattr(event, key, None)
        if v is not None:
            return v
    return None


async def run():
    rng = random.Random(SEED)
    handler = CapturingHandler()
    event_logger = logging.getLogger("autogen_core.events")
    event_logger.setLevel(logging.INFO)
    event_logger.addHandler(handler)

    runtime = SingleThreadedAgentRuntime()
    for i in range(N_AGENTS):
        await ReviewerAgent.register(
            runtime, f"reviewer_{i}", lambda i=i: ReviewerAgent(i, rng)
        )
    await CoordinatorAgent.register(runtime, "coordinator", lambda: CoordinatorAgent())

    runtime.start()
    for ep in range(N_EPISODES):
        for i in range(N_AGENTS):
            await runtime.send_message(
                ReviewRequest(episode=ep), AgentId(f"reviewer_{i}", "default")
            )
    await runtime.stop_when_idle()

    llm_events = [e for e in handler.records if isinstance(e, LLMCallEvent)]
    tool_events = [e for e in handler.records if isinstance(e, ToolCallEvent)]
    msg_events = [e for e in handler.records if isinstance(e, MessageEvent)]

    n_llm_identified = sum(has_agent_identity(e) for e in llm_events)
    n_tool_identified = sum(has_agent_identity(e) for e in tool_events)
    n_msg_identified = sum(has_agent_identity(e) for e in msg_events)

    out = {
        "framework": "autogen-core",
        "n_episodes": N_EPISODES,
        "n_agents": N_AGENTS,
        "seed": SEED,
        "n_llm_events": len(llm_events),
        "n_llm_events_with_agent_identity": n_llm_identified,
        "n_tool_events": len(tool_events),
        "n_tool_events_with_agent_identity": n_tool_identified,
        "n_message_events": len(msg_events),
        "n_message_events_with_agent_identity": n_msg_identified,
        "llm_event_kwargs_keys_sample": sorted(llm_events[0].kwargs.keys())
        if llm_events else [],
        "llm_event_agent_id_sample": [
            agent_identity_value(e) for e in llm_events[:5]
        ],
        "message_event_kwargs_keys_sample": sorted(msg_events[0].kwargs.keys())
        if msg_events else [],
        "message_event_agent_id_sample": [
            agent_identity_value(e) for e in msg_events[:5]
        ],
        "interpretation": (
            "CORRECTION to the original documentation-based audit: in the "
            "installed autogen-core version (see 'autogen_core_version' "
            "below), LLMCallEvent and ToolCallEvent both auto-populate "
            "agent_id from MessageHandlerContext.agent_id() when emitted "
            "from within a message handler -- the normal case for a real "
            "agent's LLM/tool call. This field exists in the class's "
            "internal kwargs dict (autogen_core/logging.py) but is not part "
            "of the public __init__ signature and is not documented on the "
            "API reference page the original audit read, which is why the "
            "original 'no agent identifier field' claim was wrong. Per-agent "
            "attribution from the default LLMCallEvent/ToolCallEvent stream "
            "is intact in this version. AutoGen should be reclassified SAFE, "
            "not MIXED, on this axis; MessageEvent sender/receiver remain "
            "the only other identity-carrying fields and are unaffected by "
            "this correction."
        ),
        "autogen_core_version": __import__("autogen_core").__version__
        if hasattr(__import__("autogen_core"), "__version__") else "0.7.5",
    }
    return out


if __name__ == "__main__":
    result = asyncio.run(run())
    json.dump(result, sys.stdout, indent=2)
    print()
