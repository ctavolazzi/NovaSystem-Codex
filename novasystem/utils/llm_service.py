"""
LLM Service for NovaSystem.

Unified interface for interacting with LLM providers (OpenAI, Anthropic, Gemini, Ollama).
"""

import os
import asyncio
import logging
import time
import subprocess
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, AsyncGenerator

import httpx
from openai import AsyncOpenAI
import anthropic
import ollama

from .colors import console_log, print_separator
from .metrics import get_metrics_collector
from .model_cache import get_model_cache
from ..config import get_config
from ..config.model_capabilities import (
    get_model_capabilities, get_task_weights,
    OPENAI_MODELS, ANTHROPIC_MODELS, GEMINI_MODELS
)
from ..session import get_session_manager

logger = logging.getLogger(__name__)

# Constants
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


class LLMService:
    """Unified LLM service for multiple providers."""

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
        ollama_host: str = "http://localhost:11434",
        enable_session_recording: bool = True,
        verbose: bool = False
    ):
        self.verbose = verbose
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.ollama_host = ollama_host
        self.metrics_collector = get_metrics_collector()
        self.model_cache = get_model_cache()
        self.config = get_config()

        # Session management
        self.enable_session_recording = enable_session_recording
        self.session_manager = get_session_manager() if enable_session_recording else None

        self._init_clients()

    def _log(self, emoji: str, category: str, message: str, details: dict = None):
        """Log only if verbose mode enabled."""
        if self.verbose:
            console_log(emoji, f"LLM/{category}", message, details)

    def _init_clients(self):
        """Initialize all LLM clients."""
        print_separator()
        console_log("🔧", "LLM/INIT", "Initializing LLMService...")
        print_separator()

        console_log("🔑", "LLM/INIT", "API Key Status:", {
            "OPENAI": "✅ SET" if self.openai_api_key else "❌ NOT SET",
            "ANTHROPIC": "✅ SET" if self.anthropic_api_key else "❌ NOT SET",
            "GEMINI": "✅ SET" if self.gemini_api_key else "❌ NOT SET",
            "OLLAMA_HOST": self.ollama_host
        })

        # OpenAI
        self.openai_client = AsyncOpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
        if self.openai_client:
            console_log("✅", "LLM/INIT", "OpenAI client initialized")
        else:
            console_log("⚠️", "LLM/INIT", "OpenAI client NOT initialized (no API key)")

        # Anthropic
        self.anthropic_client = anthropic.AsyncAnthropic(api_key=self.anthropic_api_key) if self.anthropic_api_key else None
        if self.anthropic_client:
            console_log("✅", "LLM/INIT", "Anthropic client initialized")
        else:
            console_log("⚠️", "LLM/INIT", "Anthropic client NOT initialized (no API key)")

        # Gemini (OpenAI-compatible)
        self.gemini_client = None
        if self.gemini_api_key:
            try:
                self.gemini_client = AsyncOpenAI(api_key=self.gemini_api_key, base_url=GEMINI_BASE_URL)
                console_log("✅", "LLM/INIT", "Gemini client initialized (OpenAI-compatible)")
            except Exception as e:
                console_log("❌", "LLM/INIT", f"Gemini init failed: {e}")

        # Ollama
        self.ollama_client = None
        try:
            self.ollama_client = ollama.AsyncClient(host=self.ollama_host)
            ollama_models = self._get_ollama_models_sync()
            if ollama_models:
                console_log("✅", "LLM/INIT", f"Ollama client initialized", {"models": len(ollama_models)})
            else:
                console_log("⚠️", "LLM/INIT", "Ollama client initialized but no models found")
        except Exception as e:
            console_log("⚠️", "LLM/INIT", f"Ollama init failed: {e}")

        # Summary
        all_models = self.get_available_models()
        print_separator()
        console_log("🎉", "LLM/INIT", f"LLMService ready!", {
            "total_models": len(all_models),
            "providers": ", ".join([
                p for p, c in [
                    ("OpenAI", self.openai_client), ("Anthropic", self.anthropic_client),
                    ("Gemini", self.gemini_client), ("Ollama", self.ollama_client)
                ] if c
            ])
        })
        print_separator()
        print()

    def is_model_available(self, model: Optional[str]) -> bool:
        """Check if model is available."""
        if not model:
            return False

        normalized = model.replace("ollama:", "").replace("gemini:", "")

        if model.startswith(("gpt", "o1")):
            return self.openai_client is not None
        if model.startswith("claude-"):
            return self.anthropic_client is not None
        if model.startswith("gemini"):
            return self.gemini_client is not None

        # Check Ollama models
        ollama_models = self.get_ollama_models()
        return any(normalized == m.replace("ollama:", "") for m in ollama_models)

    def get_available_models(self) -> List[str]:
        """Get list of all available models."""
        models = []
        if self.openai_client:
            models.extend(OPENAI_MODELS)
        if self.anthropic_client:
            models.extend(ANTHROPIC_MODELS)
        if self.gemini_client:
            models.extend(GEMINI_MODELS)
        models.extend(self.get_ollama_models())
        return models

    def get_ollama_models(self) -> List[str]:
        """Get list of Ollama models."""
        return self._get_ollama_models_sync()

    def _get_ollama_models_sync(self) -> List[str]:
        """Get Ollama models synchronously."""
        try:
            result = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                models = []
                for line in result.stdout.strip().split('\n')[1:]:
                    if line.strip():
                        parts = line.split()
                        if parts:
                            clean = parts[0].replace(":latest", "")
                            models.append(f"ollama:{clean}")
                return models
        except Exception as e:
            logger.debug(f"Failed to get Ollama models: {e}")
        return []

    def get_default_model(self) -> str:
        """Get the default model."""
        config_default = self.config.llm.default_model
        if self.is_model_available(config_default):
            return config_default

        available = self.get_available_models()
        if available:
            return self.get_best_model_for_task("general", available, prioritize_speed=True)

        raise ValueError("No LLM models available. Configure API keys or start Ollama.")

    def get_model_capabilities(self, model_name: str) -> Dict[str, Any]:
        """Get capabilities for a model."""
        return get_model_capabilities(model_name)

    def get_best_model_for_task(
        self,
        task_type: str,
        available_models: List[str] = None,
        prioritize_speed: bool = False,
        preferred_model: Optional[str] = None
    ) -> str:
        """Get the best model for a task."""
        if preferred_model and self.is_model_available(preferred_model):
            return preferred_model

        if available_models is None:
            available_models = self.get_available_models()

        if not available_models:
            raise ValueError("No models available.")

        weights = get_task_weights(task_type)
        best_model, best_score = None, 0

        for model in available_models:
            caps = self.get_model_capabilities(model)
            score = sum(caps.get(w, 0) for w in weights)

            if prioritize_speed:
                score += caps.get("speed", 0) * 0.5
                size_gb = caps.get("size_gb", 0)
                if size_gb > 5:
                    score -= (size_gb - 5) * 10
            else:
                score += caps.get("speed", 0) * 0.1

            if score > best_score:
                best_score, best_model = score, model

        return best_model or available_models[0]

    def get_model_info(self, model_name: str) -> str:
        """Get human-readable model info."""
        caps = self.get_model_capabilities(model_name)
        clean = model_name.replace("ollama:", "")
        return (
            f"Model: {clean}\n"
            f"Type: {caps.get('type', 'unknown').upper()}\n"
            f"Description: {caps.get('description', 'N/A')}\n\n"
            f"Capabilities:\n"
            f"  Reasoning: {caps.get('reasoning', 0)}/100\n"
            f"  Coding: {caps.get('coding', 0)}/100\n"
            f"  Analysis: {caps.get('analysis', 0)}/100\n"
            f"  Speed: {caps.get('speed', 0)}/100\n"
            f"  Context: {caps.get('context_length', 0):,} tokens"
        )

    # =========================================================================
    # COMPLETION METHODS
    # =========================================================================

    async def get_completion(
        self,
        messages: List[Dict[str, Any]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Get completion from specified model."""
        model = model or self.get_default_model()
        start_time = time.time()

        self._log("📤", "REQUEST", f"Sending to {model}", {"messages": len(messages)})

        try:
            if model.startswith("ollama:"):
                result = await self._ollama_completion(messages, model, temperature)
            elif model.startswith("claude-"):
                result = await self._anthropic_completion(messages, model, temperature, max_tokens)
            elif model.startswith("gemini"):
                result = await self._gemini_completion(messages, model, temperature, max_tokens)
            elif model.startswith(("gpt", "o1")):
                result = await self._openai_completion(messages, model, temperature, max_tokens)
            else:
                result = await self._ollama_completion(messages, model, temperature)

        except Exception as e:
            logger.error(f"Completion error: {e}")
            result = f"Error: {e}"

        # Record metrics
        response_time = time.time() - start_time
        self._record_metrics(model, response_time, messages, result)
        self._record_session(model, temperature, max_tokens, messages, result, response_time)

        return result

    async def _openai_completion(self, messages, model, temperature, max_tokens):
        """OpenAI completion."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")

        response = await self.openai_client.chat.completions.create(
            model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
        )
        return response.choices[0].message.content

    async def _anthropic_completion(self, messages, model, temperature, max_tokens):
        """Anthropic completion."""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")

        system_msg, content = self._convert_anthropic_messages(messages)

        params = {
            "model": model,
            "max_tokens": max_tokens or 1000,
            "temperature": temperature,
            "messages": [{"role": "user", "content": content}]
        }
        if system_msg:
            params["system"] = system_msg

        response = await self.anthropic_client.messages.create(**params)
        return response.content[0].text

    async def _gemini_completion(self, messages, model, temperature, max_tokens):
        """Gemini completion (OpenAI-compatible)."""
        if not self.gemini_client:
            raise ValueError("Gemini client not initialized")

        model_name = model.replace("gemini:", "")
        response = await self.gemini_client.chat.completions.create(
            model=model_name, messages=messages, temperature=temperature, max_tokens=max_tokens or 4096
        )
        return response.choices[0].message.content

    async def _ollama_completion(self, messages, model, temperature, timeout=120):
        """Ollama completion."""
        if not self.ollama_client:
            raise ValueError("Ollama client not initialized")

        ollama_messages = self._convert_ollama_messages(messages)
        model_name = model.replace("ollama:", "")

        try:
            response = await asyncio.wait_for(
                self.ollama_client.chat(
                    model=model_name, messages=ollama_messages, options={"temperature": temperature}
                ),
                timeout=timeout
            )
            return response['message']['content']
        except asyncio.TimeoutError:
            return f"Error: Ollama model '{model}' timed out after {timeout}s"

    # =========================================================================
    # STREAMING METHODS
    # =========================================================================

    async def stream_completion(
        self,
        messages: List[Dict[str, Any]],
        model: str = None,
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """Stream completion from specified model."""
        model = model or self.get_default_model()

        try:
            if model.startswith("claude-"):
                async for chunk in self._stream_anthropic(messages, model, temperature):
                    yield chunk
            elif model.startswith(("gpt", "o1")):
                async for chunk in self._stream_openai(messages, model, temperature):
                    yield chunk
            elif model.startswith("gemini"):
                async for chunk in self._stream_gemini(messages, model, temperature):
                    yield chunk
            else:
                async for chunk in self._stream_ollama(messages, model, temperature):
                    yield chunk
        except Exception as e:
            yield f"Error: {e}"

    async def _stream_openai(self, messages, model, temperature):
        """Stream from OpenAI."""
        if not self.openai_client:
            raise ValueError("OpenAI not initialized")

        stream = await self.openai_client.chat.completions.create(
            model=model, messages=messages, temperature=temperature, stream=True
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def _stream_anthropic(self, messages, model, temperature):
        """Stream from Anthropic."""
        if not self.anthropic_client:
            raise ValueError("Anthropic not initialized")

        system_msg, content = self._convert_anthropic_messages(messages)

        params = {
            "model": model, "max_tokens": 1000, "temperature": temperature,
            "messages": [{"role": "user", "content": content}], "stream": True
        }
        if system_msg:
            params["system"] = system_msg

        stream = await self.anthropic_client.messages.create(**params)
        async for chunk in stream:
            if chunk.type == "content_block_delta" and chunk.delta.text:
                yield chunk.delta.text

    async def _stream_gemini(self, messages, model, temperature):
        """Stream from Gemini."""
        if not self.gemini_client:
            raise ValueError("Gemini not initialized")

        model_name = model.replace("gemini:", "")
        self._log("💎", "GEMINI/STREAM", f"Starting stream", {"model": model_name})

        stream = await self.gemini_client.chat.completions.create(
            model=model_name, messages=messages, temperature=temperature, stream=True
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

        self._log("✅", "GEMINI/STREAM", "Complete")

    async def _stream_ollama(self, messages, model, temperature):
        """Stream from Ollama."""
        if not self.ollama_client:
            raise ValueError("Ollama not initialized")

        ollama_messages = self._convert_ollama_messages(messages)
        model_name = model.replace("ollama:", "")

        stream = await self.ollama_client.chat(
            model=model_name, messages=ollama_messages,
            options={"temperature": temperature}, stream=True
        )
        async for chunk in stream:
            if chunk.get('message', {}).get('content'):
                yield chunk['message']['content']

    # =========================================================================
    # MESSAGE CONVERSION HELPERS
    # =========================================================================

    def _convert_anthropic_messages(self, messages: List[Dict]) -> tuple:
        """Convert OpenAI messages to Anthropic format. Returns (system_msg, content)."""
        system_message = ""
        user_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)

        if not user_messages:
            raise ValueError("No user messages provided")

        if len(user_messages) > 1:
            content = "\n".join(f"{m['role']}: {m['content']}" for m in user_messages)
        else:
            content = user_messages[0]["content"]

        return system_message, content

    def _convert_ollama_messages(self, messages: List[Dict]) -> List[Dict]:
        """Convert messages to Ollama format."""
        ollama_messages = []
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, list):
                text = " ".join(item.get("text", "") for item in content if item.get("type") == "text")
            else:
                text = str(content)
            ollama_messages.append({"role": msg["role"], "content": text})
        return ollama_messages

    # =========================================================================
    # METRICS AND SESSION RECORDING
    # =========================================================================

    def _record_metrics(self, model: str, response_time: float, messages: List[Dict], result: str):
        """Record performance metrics."""
        tokens_in = sum(len(msg.get('content', '').split()) for msg in messages)
        tokens_out = len(result.split()) if result else 0

        self.metrics_collector.record_llm_call(
            model=model, response_time=response_time,
            tokens_input=tokens_in, tokens_generated=tokens_out
        )

    def _record_session(self, model, temperature, max_tokens, messages, result, response_time):
        """Record session if enabled."""
        if not self.enable_session_recording or not self.session_manager:
            return

        try:
            for msg in messages:
                if msg.get("role") == "user":
                    self.session_manager.add_message(
                        role="user", content=msg.get("content", ""),
                        metadata={"model": model, "temperature": temperature}
                    )

            tokens_in = sum(len(msg.get('content', '').split()) for msg in messages)
            tokens_out = len(result.split()) if result else 0

            self.session_manager.add_message(
                role="assistant", content=result,
                metadata={
                    "model": model, "temperature": temperature, "max_tokens": max_tokens,
                    "response_time": response_time, "tokens_input": tokens_in, "tokens_generated": tokens_out
                }
            )

            session = self.session_manager.get_current_session()
            if session:
                session.metadata.model_used = model
                session.metadata.total_tokens += tokens_in + tokens_out

        except Exception as e:
            logger.warning(f"Failed to record session: {e}")
