"""
LIVE reproduction of microsoft/agent-framework #3295 / PR #5690, making
real calls to the OpenAI Responses API (small model, minimal tokens) to
observe the actual HTTP error, closing the one honesty caveat left in
`agent_framework-openai-duplicate-fc-03/case_record.md` (the payload-level
reproduction never made a live call).

Turn 1: ask the model to call a tool. It does; we get back a real
server-issued response id (response1.response_id) and a real server-issued
function-call id.

Turn 2: continue with `previous_response_id=response1.response_id` (this is
exactly what sets `request_uses_service_side_storage=True` inside the
client -- read directly from _chat_client.py:1267-1271) and replay the full
history, including the function_call + function_result from turn 1 -- the
exact shape all three of the issue's field reports describe (a
HistoryProvider or workflow replaying prior conversation while a
continuation marker is also set).

Expects, on the defective pin (agent-framework-openai==1.3.0): a real
"Error code: 400 - Duplicate item found with id fc_xxx" from OpenAI.
Expects, on the corrected pin (==1.4.0): turn 2 succeeds normally.

Run: OPENAI_API_KEY must be set (loaded from .env in this directory if
present). Uses gpt-4o-mini to keep cost negligible.
"""

import asyncio
import json
import os
import sys

# Minimal, dependency-free .env loader (no python-dotenv needed).
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

if not os.environ.get("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set (checked environment and .env in this directory). Aborting.", file=sys.stderr)
    sys.exit(1)

from agent_framework import ChatOptions, Content, Message, tool
from agent_framework_openai import OpenAIChatClient, __version__ as installed_version


def _get_weather_impl(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is 18C and cloudy."


get_weather = tool(_get_weather_impl, name="get_weather", description="Get the current weather for a city.")


async def main():
    client = OpenAIChatClient(model="gpt-4o-mini")

    # Turn 1: let the model actually call the tool for real.
    turn1_messages = [Message(role="user", contents=[Content.from_text(text="What's the weather in Paris? Use the tool.")])]
    response1 = await client.get_response(turn1_messages, options=ChatOptions(tools=[get_weather]))

    function_call_content = None
    for message in response1.messages:
        for content in message.contents:
            if content.type == "function_call":
                function_call_content = content
                break
    if function_call_content is None:
        print(json.dumps({"error": "model did not call the tool on turn 1 -- cannot proceed"}))
        return

    # Build the real tool result the framework would produce.
    try:
        city = json.loads(function_call_content.arguments or "{}").get("city", "Paris")
    except json.JSONDecodeError:
        city = "Paris"
    tool_result_text = _get_weather_impl(city)
    history = [
        *turn1_messages,
        Message(role="assistant", contents=[function_call_content]),
        Message(role="tool", contents=[Content(type="function_result", call_id=function_call_content.call_id, result=tool_result_text)]),
        Message(role="user", contents=[Content.from_text(text="Thanks, one more time please.")]),
    ]

    result = {
        "agentFrameworkOpenaiVersion": installed_version,
        "turn1_response_id": response1.response_id,
        "turn1_function_call_id": function_call_content.call_id,
    }

    try:
        response2 = await client.get_response(
            history,
            options=ChatOptions(tools=[get_weather], previous_response_id=response1.response_id),
        )
        result["turn2_outcome"] = "SUCCESS"
        result["turn2_text"] = response2.text
    except Exception as e:  # noqa: BLE001 -- we want the raw API error, whatever shape it takes
        result["turn2_outcome"] = "ERROR"
        result["turn2_error"] = str(e)
        result["turn2_error_type"] = type(e).__name__

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
