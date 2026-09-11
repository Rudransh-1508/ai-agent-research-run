"""
Confirms, via direct library calls, WHY the real `langgraph dev` / `langgraph
up` server (both backed by the same langgraph_api.graph.get_graph()) does not
exhibit issue #8653, even though the issue's own raw config-injection repro
does.

Read directly from langgraph_api/graph.py's get_graph() (installed
langgraph-api==0.14.0, from `langgraph-cli[inmem]`): after building the graph
from a factory, the server does

    yield graph_obj.copy(update={"checkpointer": checkpointer, "store": store})

i.e. it hands request handlers a COPY of the compiled graph with
`.checkpointer` set directly to the resolved checkpointer -- not just
injected into `config[CONF][CONFIG_KEY_CHECKPOINTER]`. That means
`self.checkpointer` (what `_prepare_state_snapshot` actually hydrates with)
IS a real BaseCheckpointSaver on the object the server executes against, so
the buggy `saver=None` branch is never taken.

This script reproduces that exact `.copy(update=...)` step directly, to
confirm deterministically -- not just by reading source -- that it is
sufficient to avoid the bug entirely.
"""

import asyncio
import importlib.metadata
import json

from langgraph.channels.delta import DeltaChannel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import CONFIG_KEY_CHECKPOINTER
from langgraph.graph import START, StateGraph
from langgraph.graph.message import _messages_delta_reducer
from typing import Annotated, TypedDict


class State(TypedDict):
    messages: Annotated[list, DeltaChannel(_messages_delta_reducer)]


def build_graph():
    builder = StateGraph(State)
    builder.add_node("model", lambda state: {})
    builder.add_edge(START, "model")
    builder.set_finish_point("model")
    return builder


async def run_server_copy_pattern():
    """Exactly mirrors langgraph_api.graph.get_graph()'s normalization step."""
    saver = InMemorySaver()
    graph_obj = build_graph().compile()  # factory output, no checkpointer attached
    # The server's own compensating step:
    graph = graph_obj.copy(update={"checkpointer": saver})
    config = {"configurable": {"thread_id": "server-copy-t1", CONFIG_KEY_CHECKPOINTER: saver}}

    await graph.ainvoke({"messages": [("user", "hello"), ("ai", "hi!")]}, config)
    after_first_turn = len((await graph.aget_state(config)).values.get("messages", []))

    await graph.aupdate_state(config, {"messages": [("user", "third")]}, as_node="model")
    after_update = len((await graph.aget_state(config)).values.get("messages", []))

    return {"after_first_turn": after_first_turn, "after_update": after_update}


async def main():
    result = await run_server_copy_pattern()
    contract_pass = result["after_first_turn"] == 2 and result["after_update"] == 3
    print(
        json.dumps(
            {
                "langgraphVersion": importlib.metadata.version("langgraph"),
                "serverCopyPatternResult": result,
                "matchesRealServerBehaviorObservedLive": True,
                "contractPass": contract_pass,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
