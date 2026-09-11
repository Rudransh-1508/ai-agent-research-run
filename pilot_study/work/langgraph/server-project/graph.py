"""
Minimal graph for LangGraph access qualification and reproduction of issue
#8653. Exported as a FACTORY function (not a bare compiled graph) and
compiled WITHOUT an attached checkpointer, exactly matching the shape the
issue reporter used and the shape langgraph_api's graph.py injects a
request-scoped checkpointer into via CONFIG_KEY_CHECKPOINTER (confirmed by
reading langgraph_api/graph.py directly -- see ACCESS_LOG.md §5).
"""

from typing import Annotated, TypedDict

from langgraph.channels.delta import DeltaChannel
from langgraph.graph import START, StateGraph
from langgraph.graph.message import _messages_delta_reducer


class State(TypedDict):
    messages: Annotated[list, DeltaChannel(_messages_delta_reducer)]


def make_graph(config=None):
    builder = StateGraph(State)
    builder.add_node("model", lambda state: {})
    builder.add_edge(START, "model")
    builder.set_finish_point("model")
    return builder.compile()  # no checkpointer attached -- the platform/served shape
