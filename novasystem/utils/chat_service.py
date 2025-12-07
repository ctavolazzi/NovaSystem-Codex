"""
Native Gemini Chat Service for NovaSystem.

Provides multi-turn conversation support using the native Gemini SDK:
- Automatic conversation history management
- Streaming responses
- System instructions
- Thinking configuration

Uses: google-genai (the GA SDK)
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from dataclasses import dataclass, field
import logging

# Import google-genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None
    types = None

logger = logging.getLogger(__name__)


def chat_log(emoji: str, category: str, message: str, details: dict = None):
    """Log a chat service event."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [CHAT/{category}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"           └─ {key}: {val_str}")


@dataclass
class ChatMessage:
    """A message in the chat history."""
    role: str  # "user" or "model"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ChatConfig:
    """Configuration for chat sessions."""
    model: str = "gemini-2.5-flash"
    system_instruction: Optional[str] = None
    temperature: float = 1.0  # Gemini 3 recommends 1.0
    enable_thinking: bool = True
    thinking_budget: Optional[int] = None  # None = default, 0 = disabled


class ChatSession:
    """
    A multi-turn chat session using native Gemini SDK.

    Features:
    - Automatic history management
    - Streaming support
    - Thinking configuration
    - System instructions

    Usage:
        session = ChatSession(system_instruction="You are a helpful assistant.")

        # Non-streaming
        response = session.send("Hello!")
        print(response)

        # Streaming
        async for chunk in session.send_stream("Tell me a story"):
            print(chunk, end="")

        # Get history
        for msg in session.history:
            print(f"{msg.role}: {msg.content}")
    """

    def __init__(
        self,
        config: Optional[ChatConfig] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize a chat session.

        Args:
            config: Chat configuration
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
        """
        if not GENAI_AVAILABLE:
            raise ImportError(
                "google-genai package not installed. "
                "Install with: pip install google-genai"
            )

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.config = config or ChatConfig()
        self.client = genai.Client(api_key=self.api_key)
        self.history: List[ChatMessage] = []

        # Build generation config
        gen_config = {}
        if self.config.system_instruction:
            gen_config["system_instruction"] = self.config.system_instruction
        if self.config.temperature != 1.0:
            gen_config["temperature"] = self.config.temperature

        # Add thinking config if specified
        if not self.config.enable_thinking:
            gen_config["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
        elif self.config.thinking_budget is not None:
            gen_config["thinking_config"] = types.ThinkingConfig(
                thinking_budget=self.config.thinking_budget
            )

        # Create native chat
        self._chat = self.client.chats.create(
            model=self.config.model,
            config=types.GenerateContentConfig(**gen_config) if gen_config else None
        )

        chat_log("✅", "INIT", f"ChatSession created", {
            "model": self.config.model,
            "system_instruction": bool(self.config.system_instruction),
            "thinking": self.config.enable_thinking
        })

    def send(self, message: str) -> str:
        """
        Send a message and get a response (non-streaming).

        Args:
            message: User message

        Returns:
            Model response text
        """
        chat_log("📤", "SEND", f"Sending message", {
            "message_preview": message[:60]
        })

        # Record user message
        self.history.append(ChatMessage(role="user", content=message))

        # Send to API
        response = self._chat.send_message(message)
        response_text = response.text

        # Record model response
        self.history.append(ChatMessage(role="model", content=response_text))

        chat_log("📥", "RECV", f"Received response", {
            "response_length": len(response_text)
        })

        return response_text

    async def send_async(self, message: str) -> str:
        """
        Send a message asynchronously (non-streaming).

        Args:
            message: User message

        Returns:
            Model response text
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.send, message)

    def send_stream(self, message: str) -> AsyncGenerator[str, None]:
        """
        Send a message and stream the response.

        Args:
            message: User message

        Yields:
            Response chunks as they are generated
        """
        chat_log("📤", "STREAM", f"Starting streaming message", {
            "message_preview": message[:60]
        })

        # Record user message
        self.history.append(ChatMessage(role="user", content=message))

        # Stream from API
        response_chunks = []

        async def _stream():
            nonlocal response_chunks
            # Run synchronous streaming in executor
            loop = asyncio.get_event_loop()

            def _sync_stream():
                chunks = []
                for chunk in self._chat.send_message_stream(message):
                    chunks.append(chunk.text)
                    yield chunk.text
                return chunks

            # Use thread to iterate synchronous generator
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(list, self._chat.send_message_stream(message))
                chunks = []
                for chunk in self._chat.send_message_stream(message):
                    text = chunk.text
                    chunks.append(text)
                    yield text
                response_chunks = chunks

        return _stream()

    def send_stream_sync(self, message: str):
        """
        Send a message and stream the response (synchronous generator).

        Args:
            message: User message

        Yields:
            Response chunks as they are generated
        """
        chat_log("📤", "STREAM", f"Starting streaming", {
            "message_preview": message[:60]
        })

        # Record user message
        self.history.append(ChatMessage(role="user", content=message))

        # Stream from API
        full_response = []
        for chunk in self._chat.send_message_stream(message):
            text = chunk.text
            full_response.append(text)
            yield text

        # Record complete response
        complete_text = "".join(full_response)
        self.history.append(ChatMessage(role="model", content=complete_text))

        chat_log("✅", "STREAM", f"Streaming complete", {
            "total_length": len(complete_text)
        })

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history as list of dicts."""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in self.history
        ]

    def clear_history(self):
        """Clear conversation history and create new chat."""
        self.history = []

        # Recreate chat
        gen_config = {}
        if self.config.system_instruction:
            gen_config["system_instruction"] = self.config.system_instruction

        self._chat = self.client.chats.create(
            model=self.config.model,
            config=types.GenerateContentConfig(**gen_config) if gen_config else None
        )

        chat_log("🔄", "CLEAR", "Chat history cleared")


class ChatService:
    """
    Service for managing multiple chat sessions.

    Usage:
        service = ChatService()

        # Create a session
        session = service.create_session(
            session_id="user_123",
            system_instruction="You are a helpful coding assistant."
        )

        # Send messages
        response = session.send("How do I sort a list in Python?")

        # Get or create session
        session = service.get_or_create("user_123")
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the chat service."""
        if not GENAI_AVAILABLE:
            raise ImportError("google-genai package not installed.")

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.sessions: Dict[str, ChatSession] = {}

        chat_log("✅", "SERVICE", "ChatService initialized")

    def create_session(
        self,
        session_id: str,
        system_instruction: Optional[str] = None,
        model: str = "gemini-2.5-flash",
        enable_thinking: bool = True
    ) -> ChatSession:
        """
        Create a new chat session.

        Args:
            session_id: Unique session identifier
            system_instruction: Optional system instruction
            model: Model to use
            enable_thinking: Whether to enable thinking

        Returns:
            New ChatSession
        """
        config = ChatConfig(
            model=model,
            system_instruction=system_instruction,
            enable_thinking=enable_thinking
        )

        session = ChatSession(config=config, api_key=self.api_key)
        self.sessions[session_id] = session

        chat_log("✅", "SESSION", f"Created session: {session_id}")

        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get an existing session by ID."""
        return self.sessions.get(session_id)

    def get_or_create(
        self,
        session_id: str,
        system_instruction: Optional[str] = None,
        model: str = "gemini-2.5-flash"
    ) -> ChatSession:
        """Get existing session or create new one."""
        if session_id in self.sessions:
            return self.sessions[session_id]
        return self.create_session(session_id, system_instruction, model)

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            chat_log("🗑️", "SESSION", f"Deleted session: {session_id}")
            return True
        return False

    def list_sessions(self) -> List[str]:
        """List all session IDs."""
        return list(self.sessions.keys())


# Quick access functions

def create_chat(
    system_instruction: Optional[str] = None,
    model: str = "gemini-2.5-flash"
) -> ChatSession:
    """Create a quick chat session."""
    config = ChatConfig(
        model=model,
        system_instruction=system_instruction
    )
    return ChatSession(config=config)


def quick_chat(message: str, system_instruction: Optional[str] = None) -> str:
    """Send a single message and get response."""
    session = create_chat(system_instruction=system_instruction)
    return session.send(message)
