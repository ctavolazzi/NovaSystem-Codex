"""A simple conversational bot. The seed of something bigger."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
from typing import AsyncIterator


@dataclass
class Bot:
    """A conversational AI bot powered by Anthropic's Claude.

    Usage:
        bot = Bot()
        reply = await bot.say("Hello!")
    """

    name: str = "Nova"
    model: str = "claude-sonnet-4-20250514"
    system_prompt: str = "You are Nova, a helpful AI assistant."
    messages: list[dict] = field(default_factory=list)
    _client: object = field(default=None, repr=False)

    @property
    def client(self):
        if self._client is None:
            from anthropic import AsyncAnthropic

            self._client = AsyncAnthropic()
        return self._client

    async def say(self, user_message: str) -> str:
        """Send a message and get a response."""
        self.messages.append({"role": "user", "content": user_message})

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.messages,
        )

        reply = response.content[0].text
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    async def stream(self, user_message: str) -> AsyncIterator[str]:
        """Send a message and stream the response token by token."""
        self.messages.append({"role": "user", "content": user_message})

        full_reply = ""
        async with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.messages,
        ) as stream:
            async for text in stream.text_stream:
                full_reply += text
                yield text

        self.messages.append({"role": "assistant", "content": full_reply})

    def clear(self) -> None:
        """Clear conversation history."""
        self.messages.clear()


async def chat() -> None:
    """Run an interactive chat session."""
    bot = Bot()
    print(f"\n  {bot.name} is ready. Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("you: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print(f"\n  {bot.name}: ", end="", flush=True)
        async for token in bot.stream(user_input):
            print(token, end="", flush=True)
        print("\n")

    print(f"  {bot.name}: Goodbye!\n")


def main() -> None:
    """Entry point."""
    asyncio.run(chat())


if __name__ == "__main__":
    main()
