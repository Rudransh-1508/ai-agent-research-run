import asyncio
import sys

sys.path.insert(0, ".")
from deterministic_chat_client import DeterministicChatClient

from agent_framework import Agent


async def main():
    agent = Agent(DeterministicChatClient(), name="repro-agent", instructions="test agent")
    response = await agent.run("hello")
    print("text:", response.text)
    print("usage_details:", response.usage_details)


asyncio.run(main())
