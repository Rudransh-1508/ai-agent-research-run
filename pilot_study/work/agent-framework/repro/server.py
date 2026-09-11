"""
Self-hosted reproduction server for issue #7416: hosts a deterministic agent
(no live model, no API key) through agent_framework_foundry_hosting's
ResponsesHostServer -- the OpenAI-compatible /responses server -- exactly as
the issue's own code sample targets.

Run with the venv that has the DEFECTIVE or CORRECTED
agent-framework-foundry-hosting version installed (swap via pip install
between runs) to compare.
"""

import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from deterministic_chat_client import DeterministicChatClient

from agent_framework import Agent
from agent_framework_foundry_hosting import ResponsesHostServer

agent = Agent(DeterministicChatClient(), name="repro-agent", instructions="test agent")

# `history_source` was added to ResponsesHostServer in a later release than the
# defective pin used for this reproduction (1.0.0b260813); pass it only when
# the installed version actually accepts it, so the same script runs
# unmodified against both the defective and corrected pins.
_init_params = inspect.signature(ResponsesHostServer.__init__).parameters
if "history_source" in _init_params:
    server = ResponsesHostServer(agent, history_source="agent")
else:
    server = ResponsesHostServer(agent)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8088"))
    server.run(host="127.0.0.1", port=port)
