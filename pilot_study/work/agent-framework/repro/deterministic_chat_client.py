"""A minimal, deterministic BaseChatClient for reproducing issue #7416
without any live model call or API key -- it returns a fixed text response
and a fixed usage total, for both streaming and non-streaming requests.
"""

from collections.abc import Sequence

from agent_framework import (
    BaseChatClient,
    ChatOptions,
    ChatResponse,
    ChatResponseUpdate,
    Content,
    Message,
    ResponseStream,
    UsageDetails,
)

FIXED_USAGE: UsageDetails = {
    "input_token_count": 100,
    "output_token_count": 25,
    "total_token_count": 125,
}
FIXED_TEXT = "hi from the deterministic chat client"


class DeterministicChatClient(BaseChatClient):
    """Always returns FIXED_TEXT and reports FIXED_USAGE, no network call."""

    def _inner_get_response(
        self,
        *,
        messages: Sequence[Message],
        stream: bool,
        options: dict,
        **kwargs,
    ):
        if stream:
            return ResponseStream(
                self._stream_updates(),
                finalizer=lambda updates: ChatResponse.from_updates(list(updates)),
            )
        return self._get_response_async()

    async def _get_response_async(self) -> ChatResponse:
        return ChatResponse(
            messages=[
                Message(role="assistant", contents=[Content.from_text(text=FIXED_TEXT)]),
            ],
            usage_details=FIXED_USAGE,
        )

    async def _stream_updates(self):
        yield ChatResponseUpdate(contents=[Content.from_text(text=FIXED_TEXT)], role="assistant")
        yield ChatResponseUpdate(contents=[Content(type="usage", usage_details=FIXED_USAGE)])
