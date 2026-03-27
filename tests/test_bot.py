"""Tests for the Bot - the seed of NovaSystem."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from novasystem.bot import Bot


class TestBotCreation:
    """Bot can be created with sensible defaults."""

    def test_default_bot(self):
        bot = Bot()
        assert bot.name == "Nova"
        assert bot.messages == []
        assert "claude" in bot.model

    def test_custom_bot(self):
        bot = Bot(name="Atlas", system_prompt="You are Atlas.")
        assert bot.name == "Atlas"
        assert bot.system_prompt == "You are Atlas."

    def test_clear_messages(self):
        bot = Bot()
        bot.messages.append({"role": "user", "content": "hi"})
        bot.clear()
        assert bot.messages == []


class TestBotConversation:
    """Bot maintains conversation history."""

    @pytest.mark.asyncio
    async def test_say_appends_messages(self):
        bot = Bot()

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Hello back!")]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)
        bot._client = mock_client

        reply = await bot.say("Hello!")

        assert reply == "Hello back!"
        assert len(bot.messages) == 2
        assert bot.messages[0] == {"role": "user", "content": "Hello!"}
        assert bot.messages[1] == {"role": "assistant", "content": "Hello back!"}

    @pytest.mark.asyncio
    async def test_conversation_builds_context(self):
        bot = Bot()

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="response")]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)
        bot._client = mock_client

        await bot.say("first")
        await bot.say("second")

        assert len(bot.messages) == 4
        assert bot.messages[2] == {"role": "user", "content": "second"}


class TestBotImport:
    """Package structure works."""

    def test_import_from_package(self):
        from novasystem import Bot

        assert Bot is not None

    def test_version(self):
        import novasystem

        assert novasystem.__version__ == "0.4.0a1"
