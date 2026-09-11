"""Unmodified minimal repro from langchain-ai/langgraph issue #8653, run
as-is against the pinned defective version before any adaptation, to confirm
the reported behavior independently rather than trusting the issue text."""

import asyncio
from typing import Annotated, TypedDict

from langgraph.channels.delta import DeltaChannel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import CONFIG_KEY_CHECKPOINTER
from langgraph.graph import START, StateGraph
from langgraph.graph.message import _messages_delta_reducer


class State(TypedDict):
    messages: Annotated[list, DeltaChannel(_messages_delta_reducer)]


async def main() -> None:
    builder = StateGraph(State)
    builder.add_node("model", lambda state: {})
    builder.add_edge(START, "model")
    builder.set_finish_point("model")
    graph = builder.compile()  # no checkpointer attached, as on the platform

    saver = InMemorySaver()
    config = {"configurable": {"thread_id": "t1", CONFIG_KEY_CHECKPOINTER: saver}}

    await graph.ainvoke({"messages": [("user", "hello"), ("ai", "hi!")]}, config)

    snapshot = await graph.aget_state(config)
    print("get_state sees:", len(snapshot.values.get("messages", [])), "- expected 2")

    await graph.aupdate_state(config, {"messages": [("user", "third")]}, as_node="model")
    snapshot = await graph.aget_state(config)
    print("after update_state:", len(snapshot.values.get("messages", [])), "- expected 3")


asyncio.run(main())
