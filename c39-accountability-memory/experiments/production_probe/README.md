# Production-framework probe

Limitations item 5 in the paper says plainly: "Measuring per-agent bit
retention in a real compaction step is the obvious next step and we have not
taken it." This directory takes that step for one framework.

**What this is not.** It does not call a real LLM API and does not need
credentials. `docs/real_world_relevance.md` already audited framework
*documentation* (schema definitions, docs pages, one open GitHub issue) for
whether per-agent attribution survives by default. This probe goes one level
deeper: it runs `autogen-core` for real, drives a real multi-agent episode
through the real `SingleThreadedAgentRuntime`, and inspects the **actual
Python objects the framework emits**, not its documentation. `LLMCallEvent`
and `ToolCallEvent` are real emissions of the real dataclass the framework
ships (`autogen_core.logging.LLMCallEvent` / `ToolCallEvent`) — the same
class a real model-client wrapper would emit on a genuine API call. What is
synthetic is the content of the call (a local function stands in for the
model), not the event schema or the runtime's own instrumentation.
`MessageEvent` objects are not synthesised at all: the runtime emits them
itself, unprompted, every time `send_message` is called (see
`_single_threaded_agent_runtime.py`, confirmed by source inspection during
this session, not by reading docs).

## Setup

Requires a venv with `autogen-core` installed (not part of the project's
pinned reproducibility environment in `environment.json` — this probe is
deliberately kept out of that pin, since it is a one-off framework check, not
part of the theorem-verification chain).

```
python3 -m venv .venv_probe
source .venv_probe/bin/activate
pip install autogen-core==<version pinned in requirements.txt>
python run_probe.py
```

## What it measures

Three `ReviewerAgent`s receive a review request from one `CoordinatorAgent`
each episode. Each reviewer has a hidden ground-truth shirk bit; a shirking
reviewer emits a real `LLMCallEvent` with fewer completion tokens and a
generic result, submitted via a real `ToolCallEvent`. Reviewers report back
to the coordinator, which triggers the runtime's own `MessageEvent` emission.

For every episode we capture every event the framework's `autogen_core.events`
logger actually emits (via a `logging.Handler` attached to that logger, not by
hand-collecting anything) and check, per event instance: does it expose any
attribute that identifies which agent produced it?

`results.json` reports the counts across N episodes. The finding is
structural, not probabilistic: it is either possible to name the agent from
the field on the object, or the field does not exist.
