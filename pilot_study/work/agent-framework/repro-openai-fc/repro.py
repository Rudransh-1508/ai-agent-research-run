"""
Reproduction of microsoft/agent-framework issue #3295 / PR #5690:
"Fix duplicate item error for tool-using agents under service-side storage."

Mechanism, confirmed directly against downloaded wheels for both pinned
versions (not just the PR description): `RawOpenAIChatClient._prepare_message_for_openai`
builds a wire-format "function_call" item straight from any assistant message
carrying one, with no guard, in `agent-framework-openai==1.3.0`. In `1.4.0`,
the exact same branch is wrapped in
`if request_uses_service_side_storage: continue` before the item is ever
built, dropping it -- since the OpenAI Responses API already has that item
server-side once `previous_response_id`/`conversation` is set, and rejects
a request that includes it again with:

    Error code: 400 - "Duplicate item found with id fc_xxx.
    Remove duplicate items from your input and try again."

This reproduction calls `_prepare_messages_for_openai` directly -- the exact
function that builds the outbound wire payload -- with a synthetic assistant
message carrying a function_call item, under `request_uses_service_side_storage=True`
(the flag that's set whenever a session, RedisHistoryProvider,
CosmosHistoryProvider, or replayed-conversation continuation is in play --
i.e. any hosted/persisted-history serving shape, not a one-shot embedded
call). No live OpenAI API call is made or needed: the defect is entirely in
what gets serialized into the request body, independent of whether that
body is ever actually sent.
"""

import json

from agent_framework import Content, Message
from agent_framework_openai._chat_client import RawOpenAIChatClient
from agent_framework_openai import __version__ as installed_version


def build_client() -> RawOpenAIChatClient:
    # A fake key is fine: no network call is made anywhere in this script.
    return RawOpenAIChatClient(model="gpt-4o", api_key="sk-fake-not-a-real-key")


def build_history_with_function_call() -> list[Message]:
    """A two-turn history: user asks, assistant calls a tool with a
    server-issued fc_* id (as it would after a real Responses API turn),
    tool returns a result. This is exactly the shape a HistoryProvider
    (Redis/Cosmos) or a workflow replaying conversation would hand back on
    the *next* turn."""
    return [
        Message(role="user", contents=[Content.from_text(text="what's the weather in Paris?")]),
        Message(
            role="assistant",
            contents=[
                Content(
                    type="function_call",
                    call_id="call_abc123",
                    name="get_weather",
                    arguments='{"city": "Paris"}',
                    additional_properties={"fc_id": "fc_server_issued_001"},
                )
            ],
        ),
        Message(
            role="tool",
            contents=[Content(type="function_result", call_id="call_abc123", result="18C, cloudy")],
        ),
    ]


def main():
    client = build_client()
    history = build_history_with_function_call()

    # "Embedded"-equivalent: no service-side storage in play (a one-shot
    # call with no continuation marker) -- function_call items are expected
    # to be present, since there's no prior server-side response to
    # duplicate against.
    embedded_wire_items = client._prepare_messages_for_openai(
        history, request_uses_service_side_storage=False
    )
    embedded_has_function_call = any(item.get("type") == "function_call" for item in embedded_wire_items)

    # "Served"-equivalent: request_uses_service_side_storage=True -- set
    # whenever the request carries previous_response_id/conversation_id/
    # conversation, i.e. a session, RedisHistoryProvider, CosmosHistoryProvider,
    # or a workflow replaying prior conversation. All three of the issue's
    # field reports set this flag through one of those paths.
    served_wire_items = client._prepare_messages_for_openai(
        history, request_uses_service_side_storage=True
    )
    served_has_function_call = any(item.get("type") == "function_call" for item in served_wire_items)

    # Contract: under service-side storage, the wire payload must not
    # re-include a function_call item the server already has, or the
    # Responses API rejects the whole request with a 400.
    embedded_pass = embedded_has_function_call  # expected to be present when there's no continuation
    served_pass = not served_has_function_call  # expected to be dropped when continuing

    print(
        json.dumps(
            {
                "agentFrameworkOpenaiVersion": installed_version,
                "embedded_no_continuation": {
                    "function_call_item_present": embedded_has_function_call,
                    "pass": embedded_pass,
                },
                "served_with_continuation": {
                    "function_call_item_present": served_has_function_call,
                    "pass": served_pass,
                    "consequence_if_present": (
                        'OpenAI Responses API would reject this request with '
                        '400 "Duplicate item found with id fc_xxx"'
                    ),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
