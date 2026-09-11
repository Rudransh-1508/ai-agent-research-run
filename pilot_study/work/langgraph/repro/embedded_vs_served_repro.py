"""
Embedded (checkpointer attached at compile time) vs. served (checkpointer
injected via config) reproduction of langchain-ai/langgraph issue #8653:
"update_state can permanently erase a thread's messages."

Mechanism, confirmed by reading the installed langgraph 1.2.11 package's
langgraph/pregel/main.py directly (not just trusted from the issue body):
`_prepare_state_snapshot` (behind get_state / get_state_history /
update_state, sync and async) hydrates channels with
`saver=self.checkpointer if isinstance(self.checkpointer, BaseCheckpointSaver)
else None` -- the graph-attached checkpointer -- while everything else in
those code paths resolves the checkpointer from
`config[CONF][CONFIG_KEY_CHECKPOINTER]`.

- Embedded / dev shape: `.compile(checkpointer=saver)` attaches the
  checkpointer directly, so `self.checkpointer` IS a BaseCheckpointSaver.
  Channel hydration works. `langgraph dev` uses this same attachment shape
  for a graph you hand it.
- Served / LangGraph Platform shape: the graph is compiled WITHOUT a
  checkpointer (`self.checkpointer` is `None`), and the checkpointer is
  supplied per-request via `config[CONF][CONFIG_KEY_CHECKPOINTER]` -- this is
  the shape LangGraph Platform's server actually uses (one compiled graph,
  a request-scoped checkpointer injected via config) -- see ACCESS_LOG.md §5
  for the server-side verification of this claim. Channel hydration then
  silently gets `saver=None`; a DeltaChannel needing ancestor replay reads
  empty, and `update_state` commits that emptiness as the new head.

Same graph, same input, same operations -- only the checkpointer attachment
method (a "relevant feature setting" per plan §9.3) differs between the two
conditions.
"""

import asyncio
import importlib.metadata
import json
from typing import Annotated, TypedDict

from langgraph.channels.delta import DeltaChannel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import CONFIG_KEY_CHECKPOINTER
from langgraph.graph import START, StateGraph
from langgraph.graph.message import _messages_delta_reducer


class State(TypedDict):
    messages: Annotated[list, DeltaChannel(_messages_delta_reducer)]


def build_graph():
    builder = StateGraph(State)
    builder.add_node("model", lambda state: {})
    builder.add_edge(START, "model")
    builder.set_finish_point("model")
    return builder


async def run_embedded():
    """Checkpointer attached directly at compile time -- the embedded/dev shape."""
    saver = InMemorySaver()
    graph = build_graph().compile(checkpointer=saver)
    config = {"configurable": {"thread_id": "embedded-t1"}}

    await graph.ainvoke({"messages": [("user", "hello"), ("ai", "hi!")]}, config)
    after_first_turn = len((await graph.aget_state(config)).values.get("messages", []))

    await graph.aupdate_state(config, {"messages": [("user", "third")]}, as_node="model")
    after_update = len((await graph.aget_state(config)).values.get("messages", []))

    return {"after_first_turn": after_first_turn, "after_update": after_update}


async def run_served():
    """Checkpointer injected via config -- the LangGraph Platform / served shape."""
    saver = InMemorySaver()
    graph = build_graph().compile()  # no checkpointer attached, matching the platform shape
    config = {"configurable": {"thread_id": "served-t1", CONFIG_KEY_CHECKPOINTER: saver}}

    await graph.ainvoke({"messages": [("user", "hello"), ("ai", "hi!")]}, config)
    after_first_turn = len((await graph.aget_state(config)).values.get("messages", []))

    await graph.aupdate_state(config, {"messages": [("user", "third")]}, as_node="model")
    after_update = len((await graph.aget_state(config)).values.get("messages", []))

    return {"after_first_turn": after_first_turn, "after_update": after_update}


async def main():
    embedded = await run_embedded()
    served = await run_served()

    # Contract (plan §2.2, "state continuity"): a subsequent request should see
    # the state the checkpointer contract says should persist, regardless of
    # attachment method. First turn should read 2 messages back; after
    # update_state adds one more, it should read 3.
    embedded_pass = embedded["after_first_turn"] == 2 and embedded["after_update"] == 3
    served_pass = served["after_first_turn"] == 2 and served["after_update"] == 3

    print(
        json.dumps(
            {
                "langgraphVersion": importlib.metadata.version("langgraph"),
                "embedded": embedded,
                "served": served,
                "embeddedPass": embedded_pass,
                "servedPass": served_pass,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
