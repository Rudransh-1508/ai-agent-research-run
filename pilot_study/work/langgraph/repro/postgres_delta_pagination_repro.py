"""
Reproduction of langchain-ai/langgraph issue #8448: PostgresSaver's
get_delta_channel_history permanently poisons its walk cursor when the
target checkpoint's ancestor-delta walk needs to cross a pagination boundary
(_DELTA_PAGE_SIZE = 1024 checkpoints), silently dropping DeltaChannel
history instead of raising.

Unlike #8653 (which the real langgraph dev/up server compensates for via
graph_obj.copy(update={"checkpointer": ...})), this defect is a genuinely
different mechanism -- it lives entirely inside the Postgres-specific
checkpoint-history pagination logic
(langgraph/checkpoint/postgres/base.py::_try_advance_walks), which the
in-memory checkpointer (InMemorySaver, used by `langgraph dev` and any
embedded/local test) doesn't share at all (InMemorySaver doesn't page).

Confirmed against the installed langgraph-checkpoint-postgres==3.1.2
(latest) source directly: `if ch not in walk_cursor_by_ch:
walk_cursor_by_ch[ch] = parent_of.get(target_id)` at base.py:445-446.

This script:
1. Seeds a DeltaChannel `messages` state via one `ainvoke` (checkpoint 0).
2. Performs enough `aupdate_state` delta-only writes to push the total
   checkpoint count for this thread past 1024, so the original seed is no
   longer in the newest-1024-rows page.
3. Compares reading the state back via PostgresSaver (the production-shaped
   backend `langgraph up` actually uses) against InMemorySaver (the
   dev-server-shaped backend), under otherwise identical graph/operations.
"""

import asyncio
import importlib.metadata
import json
import os
import sys
import uuid
from typing import Annotated, TypedDict

from langgraph.channels.delta import DeltaChannel
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import _messages_delta_reducer

N_EXTRA_UPDATES = int(os.environ.get("N_EXTRA_UPDATES", "1030"))  # > _DELTA_PAGE_SIZE (1024)


class State(TypedDict):
    messages: Annotated[list, DeltaChannel(_messages_delta_reducer)]


def build_graph():
    builder = StateGraph(State)
    builder.add_node("model", lambda state: {})
    builder.add_edge(START, "model")
    builder.set_finish_point("model")
    return builder


async def run_with_saver(saver, thread_id: str):
    graph = build_graph().compile(checkpointer=saver)
    config = {"configurable": {"thread_id": thread_id}}

    # Seed: full snapshot written on the first turn.
    await graph.ainvoke({"messages": [("user", "hello"), ("ai", "hi!")]}, config)
    seed_snapshot = await graph.aget_state(config)
    after_seed = len(seed_snapshot.values.get("messages", []))
    # The seed checkpoint's own id -- the specific historical target we'll
    # request after it's no longer in the newest-1024-rows page. A plain
    # get_state(config) with no checkpoint_id always targets HEAD, which by
    # definition is always in page 1 -- that's why the naive version of this
    # test (no explicit checkpoint_id) never exercised the reported bug.
    seed_checkpoint_id = seed_snapshot.config["configurable"]["checkpoint_id"]

    # Push the thread's checkpoint count past the pagination boundary with
    # delta-only writes (each update_state call writes one new checkpoint,
    # none of which re-seed the channel with a full snapshot).
    for i in range(N_EXTRA_UPDATES):
        await graph.aupdate_state(config, {"messages": [("user", f"msg-{i}")]}, as_node="model")

    final_state = await graph.aget_state(config)
    after_many_updates = len(final_state.values.get("messages", []))
    expected_after_many_updates = 2 + N_EXTRA_UPDATES

    # Now explicitly target the seed checkpoint -- old enough (if
    # N_EXTRA_UPDATES > _DELTA_PAGE_SIZE) to no longer be in the newest-1024
    # page -- exactly the condition the issue describes.
    historical_config = {
        "configurable": {"thread_id": thread_id, "checkpoint_id": seed_checkpoint_id}
    }
    historical_snapshot = await graph.aget_state(historical_config)
    after_historical_read = len(historical_snapshot.values.get("messages", []))
    expected_after_historical_read = 2  # the seed checkpoint should still read its own 2 messages

    return {
        "after_seed": after_seed,
        "after_many_updates": after_many_updates,
        "expected_after_many_updates": expected_after_many_updates,
        "after_historical_read": after_historical_read,
        "expected_after_historical_read": expected_after_historical_read,
        "pass": after_many_updates == expected_after_many_updates
        and after_historical_read == expected_after_historical_read,
    }


async def main():
    dsn = os.environ.get(
        "POSTGRES_DSN", "postgresql://postgres:postgres@localhost:5442/langgraph_test?sslmode=disable"
    )

    results = {}

    # Fresh, unique thread ID per run so re-running this script never reuses
    # another run's checkpoint history (plan §9.3: never let one run's state
    # become another's starting point).
    run_tag = uuid.uuid4().hex[:8]

    # In-memory / dev-shaped condition.
    im_saver = InMemorySaver()
    results["in_memory (dev-shaped)"] = await run_with_saver(im_saver, f"inmem-thread-{run_tag}")

    # Postgres / production-shaped condition.
    async with AsyncPostgresSaver.from_conn_string(dsn) as pg_saver:
        await pg_saver.setup()
        results["postgres (production-shaped, langgraph up backend)"] = await run_with_saver(
            pg_saver, f"pg-thread-{run_tag}"
        )

    print(
        json.dumps(
            {
                "langgraphVersion": importlib.metadata.version("langgraph"),
                "langgraphCheckpointPostgresVersion": importlib.metadata.version(
                    "langgraph-checkpoint-postgres"
                ),
                "nExtraUpdates": N_EXTRA_UPDATES,
                "results": results,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
