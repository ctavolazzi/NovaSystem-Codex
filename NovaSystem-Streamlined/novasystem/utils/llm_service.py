"""
LLM Service for NovaSystem.

This module provides a unified interface for interacting with different
LLM providers (OpenAI, Anthropic, Google Gemini, Ollama).
"""

import os
import sys
import asyncio
import logging
import time
from datetime import datetime

from typing import List, Dict, Any, Optional, AsyncGenerator
import httpx
from openai import AsyncOpenAI
import anthropic
import ollama

# Gemini uses OpenAI-compatible API - no separate SDK needed!
# Just use AsyncOpenAI with different base_url
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

from .metrics import get_metrics_collector
from .model_cache import get_model_cache
from ..config import get_config
from ..session import get_session_manager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Console logging helper with emojis
def llm_log(emoji: str, category: str, message: str, details: dict = None):
    """Log an LLM event with emoji prefix for easy console scanning."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [LLM/{category}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            print(f"           └─ {key}: {val_str}")

class LLMService:
    """Unified LLM service for multiple providers."""

    def __init__(self,
                 openai_api_key: Optional[str] = None,
                 anthropic_api_key: Optional[str] = None,
                 gemini_api_key: Optional[str] = None,
                 ollama_host: str = "http://localhost:11434",
                 enable_session_recording: bool = True):
        """
        Initialize the LLM service.

        Args:
            openai_api_key: OpenAI API key
            anthropic_api_key: Anthropic API key
            gemini_api_key: Google Gemini API key
            ollama_host: Ollama server host
            enable_session_recording: Whether to record sessions automatically
        """
        print("\n" + "="*80)
        llm_log("🔧", "INIT", "Initializing LLMService...")
        print("="*80)

        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.ollama_host = ollama_host
        self.metrics_collector = get_metrics_collector()
        self.model_cache = get_model_cache()

        # Log API key status (redacted)
        llm_log("🔑", "INIT", "API Key Status:", {
            "OPENAI": "✅ SET" if self.openai_api_key else "❌ NOT SET",
            "ANTHROPIC": "✅ SET" if self.anthropic_api_key else "❌ NOT SET",
            "GEMINI": "✅ SET" if self.gemini_api_key else "❌ NOT SET",
            "OLLAMA_HOST": self.ollama_host
        })

        # Session management
        self.enable_session_recording = enable_session_recording
        self.config = get_config()
        if self.enable_session_recording:
            self.session_manager = get_session_manager()
        else:
            self.session_manager = None

        # Initialize clients
        if self.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=self.openai_api_key)
            llm_log("✅", "INIT", "OpenAI client initialized")
        else:
            self.openai_client = None
            llm_log("⚠️", "INIT", "OpenAI client NOT initialized (no API key)")

        if self.anthropic_api_key:
            self.anthropic_client = anthropic.AsyncAnthropic(api_key=self.anthropic_api_key)
            llm_log("✅", "INIT", "Anthropic client initialized")
        else:
            self.anthropic_client = None
            llm_log("⚠️", "INIT", "Anthropic client NOT initialized (no API key)")

        # Initialize Gemini client (uses OpenAI-compatible API!)
        self.gemini_client = None
        if self.gemini_api_key:
            try:
                # Gemini supports OpenAI-compatible API - just use different base_url
                self.gemini_client = AsyncOpenAI(
                    api_key=self.gemini_api_key,
                    base_url=GEMINI_BASE_URL
                )
                llm_log("✅", "INIT", "Gemini client initialized (OpenAI-compatible)")
            except Exception as e:
                llm_log("❌", "INIT", f"Gemini client initialization failed: {str(e)}")
        else:
            llm_log("⚠️", "INIT", "Gemini client NOT initialized (no API key)")

        try:
            self.ollama_client = ollama.AsyncClient(host=self.ollama_host)
            # Test if Ollama is running
            available_models = self.get_ollama_models()
            if available_models and len(available_models) > 0:
                llm_log("✅", "INIT", f"Ollama client initialized", {
                    "models": len(available_models),
                    "available": [m.replace('ollama:', '') for m in available_models]
                })
            else:
                llm_log("⚠️", "INIT", "Ollama client initialized but no models found")
        except Exception as e:
            self.ollama_client = None
            llm_log("⚠️", "INIT", f"Ollama client initialization failed: {str(e)}")

        # Final summary
        all_models = self.get_available_models()
        print("="*80)
        llm_log("🎉", "INIT", f"LLMService ready!", {
            "total_models": len(all_models),
            "providers": ", ".join([
                p for p, c in [
                    ("OpenAI", self.openai_client),
                    ("Anthropic", self.anthropic_client),
                    ("Gemini", self.gemini_client),
                    ("Ollama", self.ollama_client)
                ] if c
            ])
        })
        print("="*80 + "\n")

    def is_model_available(self, model: Optional[str]) -> bool:
        """Check whether the requested model can be used with the current clients/installations."""
        if not model:
            return False

        # Normalize model name for Ollama comparisons
        normalized = model.replace("ollama:", "").replace("gemini:", "")

        if model.startswith(("gpt", "o1")):
            return self.openai_client is not None
        if model.startswith("claude-"):
            return self.anthropic_client is not None
        if model.startswith("gemini") or model.startswith("gemini:"):
            return self.gemini_client is not None

        # Treat anything else as an Ollama model
        available_ollama = self.get_ollama_models()
        return any(normalized == m.replace("ollama:", "") for m in available_ollama)

    async def get_completion(self,
                           messages: List[Dict[str, Any]],
                           model: str = None,
                           temperature: float = 0.7,
                           max_tokens: Optional[int] = None) -> str:
        """
        Get completion from the specified model.

        Args:
            messages: List of messages in OpenAI format
            model: Model name (if None, uses default model)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        # Use default model if none specified
        if model is None:
            model = self.get_default_model()

        start_time = time.time()
        tokens_input = sum(len(msg.get('content', '').split()) for msg in messages)

        # Extract first user message for logging
        user_msg = next((m.get('content', '')[:80] for m in messages if m.get('role') == 'user'), 'N/A')

        llm_log("📤", "REQUEST", f"Sending request to {model}", {
            "messages": len(messages),
            "tokens_est": tokens_input,
            "temperature": temperature,
            "max_tokens": max_tokens or "default",
            "prompt_preview": user_msg + "..." if len(user_msg) == 80 else user_msg
        })

        # Check cache first
        if model.startswith("ollama:"):
            model_type = "ollama"
        elif model.startswith("claude-"):
            model_type = "anthropic"
        elif model.startswith("gemini"):
            model_type = "gemini"
        else:
            model_type = "openai"
        cache_entry = self.model_cache.get_model(model, model_type)

        if cache_entry and cache_entry.is_loaded:
            llm_log("💾", "CACHE", f"Using cached model: {model}")

        try:
            # If model starts with ollama:, use Ollama directly
            if model.startswith("ollama:"):
                llm_log("🦙", "ROUTE", f"Routing to Ollama: {model}")
                result = await self._get_ollama_completion(messages, model, temperature)

            # If model starts with claude-, use Anthropic
            elif model.startswith("claude-"):
                llm_log("🤖", "ROUTE", f"Routing to Anthropic: {model}")
                if self.anthropic_client:
                    result = await self._get_anthropic_completion(messages, model, temperature, max_tokens)
                else:
                    raise ValueError("Anthropic client not initialized. Set ANTHROPIC_API_KEY or choose an available model.")

            # If model starts with gemini, use Google Gemini
            elif model.startswith("gemini"):
                llm_log("💎", "ROUTE", f"Routing to Gemini: {model}")
                if self.gemini_client:
                    result = await self._get_gemini_completion(messages, model, temperature, max_tokens)
                else:
                    raise ValueError("Gemini client not initialized. Set GEMINI_API_KEY and install google-generativeai package.")

            # If model starts with gpt or o1, try OpenAI first
            elif model.startswith("gpt") or model.startswith("o1"):
                llm_log("🧠", "ROUTE", f"Routing to OpenAI: {model}")
                if self.openai_client:
                    result = await self._get_openai_completion(messages, model, temperature, max_tokens)
                else:
                    raise ValueError("OpenAI client not initialized. Set OPENAI_API_KEY or choose an available model.")

            # For any other model, try Ollama first
            else:
                llm_log("🦙", "ROUTE", f"Routing to Ollama (fallback): {model}")
                try:
                    result = await self._get_ollama_completion(messages, model, temperature)
                except Exception:
                    raise ValueError(f"Model {model} not supported. Please use a valid model.")

        except Exception as e:
            llm_log("❌", "ERROR", f"Error getting completion: {str(e)}")
            logger.error(f"Error getting completion: {str(e)}")
            result = f"Error: {str(e)}"

        # Record metrics
        end_time = time.time()
        response_time = end_time - start_time
        tokens_generated = len(result.split()) if result else 0

        # Log response summary
        result_preview = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
        llm_log("📥", "RESPONSE", f"Received response from {model}", {
            "response_time": f"{response_time:.2f}s",
            "tokens_in": tokens_input,
            "tokens_out": tokens_generated,
            "response_preview": result_preview.replace('\n', ' ')
        })

        self.metrics_collector.record_llm_call(
            model=model,
            response_time=response_time,
            tokens_input=tokens_input,
            tokens_generated=tokens_generated
        )

        # Update cache if this was a new model
        if not cache_entry:
            memory_usage = self.model_cache._estimate_memory_usage(model, model_type)
            self.model_cache.put_model(
                model_name=model,
                model_type=model_type,
                load_time=response_time,
                memory_usage_mb=memory_usage,
                metadata={'last_used': datetime.now().isoformat()}
            )

        # Record session if enabled
        if self.enable_session_recording and self.session_manager:
            try:
                # Add user messages to session
                for msg in messages:
                    if msg.get("role") == "user":
                        self.session_manager.add_message(
                            role="user",
                            content=msg.get("content", ""),
                            metadata={"model": model, "temperature": temperature}
                        )

                # Add assistant response to session
                self.session_manager.add_message(
                    role="assistant",
                    content=result,
                    metadata={
                        "model": model,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "response_time": response_time,
                        "tokens_input": tokens_input,
                        "tokens_generated": tokens_generated
                    }
                )

                # Update session metadata
                current_session = self.session_manager.get_current_session()
                if current_session:
                    current_session.metadata.model_used = model
                    current_session.metadata.total_tokens += tokens_input + tokens_generated

            except Exception as e:
                logger.warning(f"Failed to record session: {e}")

        return result

    async def _get_ollama_fallback(self, messages: List[Dict[str, Any]], temperature: float) -> str:
        """Fallback to Ollama when OpenAI is not available."""
        if not self.ollama_client:
            raise ValueError("No LLM service available (OpenAI key missing and Ollama not running)")

        # Get available Ollama models
        ollama_models = self.get_ollama_models()
        if not ollama_models:
            raise ValueError("No Ollama models available")

        # Use the first available model
        fallback_model = ollama_models[0]
        logger.info(f"Falling back to Ollama model: {fallback_model}")
        return await self._get_ollama_completion(messages, fallback_model, temperature)

    async def _get_openai_completion(self,
                                   messages: List[Dict[str, Any]],
                                   model: str,
                                   temperature: float,
                                   max_tokens: Optional[int]) -> str:
        """Get completion from OpenAI."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")

        llm_log("🧠", "OPENAI", f"Calling OpenAI API", {
            "model": model,
            "messages": len(messages),
            "temperature": temperature
        })

        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            result = response.choices[0].message.content

            # Log token usage from API response
            usage = response.usage
            if usage:
                llm_log("📊", "OPENAI/TOKENS", f"Token usage", {
                    "input": f"{usage.prompt_tokens} tokens",
                    "output": f"{usage.completion_tokens} tokens",
                    "total": f"{usage.total_tokens} tokens"
                })

            llm_log("✅", "OPENAI", f"Response received", {
                "response_length": len(result) if result else 0,
                "finish_reason": response.choices[0].finish_reason
            })

            return result
        except Exception as e:
            llm_log("❌", "OPENAI", f"Error: {str(e)}")
            if "rate limit" in str(e).lower():
                return "Error: Rate limit exceeded. Please try again later."
            elif "insufficient_quota" in str(e).lower():
                return "Error: Insufficient API quota. Please check your OpenAI account."
            else:
                return f"OpenAI Error: {str(e)}"

    async def _get_anthropic_completion(self,
                                      messages: List[Dict[str, Any]],
                                      model: str,
                                      temperature: float,
                                      max_tokens: Optional[int]) -> str:
        """Get completion from Anthropic."""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")

        llm_log("🤖", "ANTHROPIC", f"Preparing Anthropic request", {
            "model": model,
            "messages": len(messages),
            "temperature": temperature
        })

        try:
            # Convert OpenAI format to Anthropic format
            # Anthropic expects system message and user messages
            system_message = ""
            user_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)

            # Handle the case where we have user messages
            if user_messages:
                # If we have multiple messages, combine them
                if len(user_messages) > 1:
                    content = ""
                    for msg in user_messages:
                        content += f"{msg['role']}: {msg['content']}\n"
                else:
                    # Single user message
                    content = user_messages[0]["content"]

                # Prepare the API call parameters
                api_params = {
                    "model": model,
                    "max_tokens": max_tokens or 1000,
                    "temperature": temperature,
                    "messages": [{"role": "user", "content": content}]
                }

                # Only add system parameter if we have a system message
                if system_message:
                    api_params["system"] = system_message

                llm_log("🤖", "ANTHROPIC", f"Calling Anthropic API", {
                    "has_system": bool(system_message),
                    "content_length": len(content)
                })

                response = await self.anthropic_client.messages.create(**api_params)
            else:
                raise ValueError("No user messages provided")

            result = response.content[0].text

            # Log token usage from Anthropic response
            if hasattr(response, 'usage'):
                llm_log("📊", "ANTHROPIC/TOKENS", f"Token usage", {
                    "input": f"{response.usage.input_tokens} tokens",
                    "output": f"{response.usage.output_tokens} tokens"
                })

            llm_log("✅", "ANTHROPIC", f"Response received", {
                "response_length": len(result) if result else 0,
                "stop_reason": response.stop_reason
            })

            return result
        except Exception as e:
            llm_log("❌", "ANTHROPIC", f"Error: {str(e)}")
            if "rate limit" in str(e).lower():
                return "Error: Rate limit exceeded. Please try again later."
            elif "insufficient_quota" in str(e).lower():
                return "Error: Insufficient API quota. Please check your Anthropic account."
            else:
                return f"Anthropic Error: {str(e)}"

    async def _get_gemini_completion(self,
                                    messages: List[Dict[str, Any]],
                                    model: str,
                                    temperature: float,
                                    max_tokens: Optional[int]) -> str:
        """Get completion from Google Gemini using OpenAI-compatible API."""
        # Remove gemini: prefix if present
        model_name = model.replace("gemini:", "")

        llm_log("💎", "GEMINI", f"Preparing Gemini request (OpenAI-compatible)", {
            "model": model_name,
            "messages": len(messages),
            "temperature": temperature,
            "max_tokens": max_tokens or "default"
        })

        if not self.gemini_client:
            raise ValueError("Gemini client not initialized. Set GEMINI_API_KEY.")

        try:
            # Gemini uses OpenAI-compatible API - same format as OpenAI!
            llm_log("💎", "GEMINI", f"Calling Gemini API via OpenAI compatibility layer", {
                "endpoint": GEMINI_BASE_URL,
                "model": model_name
            })

            response = await self.gemini_client.chat.completions.create(
                model=model_name,
                messages=messages,  # No conversion needed - same format!
                temperature=temperature,
                max_tokens=max_tokens or 4096
            )

            result = response.choices[0].message.content

            # Extract actual token usage from API response
            usage = response.usage
            token_info = {}
            if usage:
                token_info = {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                    "cost_estimate": f"~${(usage.prompt_tokens * 0.000001 + usage.completion_tokens * 0.000004):.6f}"
                }

            llm_log("✅", "GEMINI", f"Gemini response received", {
                "response_length": len(result) if result else 0,
                "finish_reason": response.choices[0].finish_reason,
                "model": response.model,
                **token_info
            })

            # Log token breakdown for debugging
            if usage:
                llm_log("📊", "GEMINI/TOKENS", f"Token usage breakdown", {
                    "input": f"{usage.prompt_tokens} tokens (~{usage.prompt_tokens * 4} chars)",
                    "output": f"{usage.completion_tokens} tokens (~{usage.completion_tokens * 4} chars)",
                    "total": f"{usage.total_tokens} tokens"
                })

            return result

        except Exception as e:
            llm_log("❌", "GEMINI", f"Gemini error: {str(e)}")
            if "rate limit" in str(e).lower() or "quota" in str(e).lower():
                return "Error: Rate limit exceeded. Please try again later."
            elif "api key" in str(e).lower() or "401" in str(e):
                return "Error: Invalid Gemini API key. Please check your GEMINI_API_KEY."
            else:
                return f"Gemini Error: {str(e)}"

    async def _get_ollama_completion(self,
                                   messages: List[Dict[str, Any]],
                                   model: str,
                                   temperature: float,
                                   timeout: int = 120) -> str:
        """Get completion from Ollama with timeout."""
        if not self.ollama_client:
            raise ValueError("Ollama client not initialized")

        try:
            # Convert OpenAI format to Ollama format
            ollama_messages = []
            for msg in messages:
                content = msg.get("content", "")
                if isinstance(content, list):
                    # Extract text from content array
                    text = " ".join(item.get("text", "") for item in content if item.get("type") == "text")
                else:
                    text = str(content)
                ollama_messages.append({"role": msg["role"], "content": text})

            # Remove ollama: prefix if present
            model_name = model.replace("ollama:", "")

            # Add timeout to prevent hanging
            import asyncio
            response = await asyncio.wait_for(
                self.ollama_client.chat(
                    model=model_name,
                    messages=ollama_messages,
                    options={"temperature": temperature}
                ),
                timeout=timeout
            )
            return response['message']['content']

        except asyncio.TimeoutError:
            return f"Error: Ollama model '{model}' timed out after {timeout} seconds. Try a smaller/faster model."
        except Exception as e:
            if "model not found" in str(e).lower():
                return f"Error: Model '{model}' not found. Please run 'ollama pull {model}' first."
            elif "connection refused" in str(e).lower():
                return "Error: Cannot connect to Ollama. Is it running? Start with 'ollama serve'"
            else:
                return f"Ollama Error: {str(e)}"

    async def stream_completion(self,
                              messages: List[Dict[str, Any]],
                              model: str = None,
                              temperature: float = 0.7) -> AsyncGenerator[str, None]:
        """
        Stream completion from the specified model.

        Args:
            messages: List of messages in OpenAI format
            model: Model name (if None, uses default model)
            temperature: Sampling temperature

        Yields:
            Generated text chunks
        """
        # Use default model if none specified
        if model is None:
            model = self.get_default_model()

        try:
            if model.startswith("claude-"):
                async for chunk in self._stream_anthropic_completion(messages, model, temperature):
                    yield chunk
            elif model.startswith("gpt"):
                async for chunk in self._stream_openai_completion(messages, model, temperature):
                    yield chunk
            elif model.startswith("gemini"):
                async for chunk in self._stream_gemini_completion(messages, model, temperature):
                    yield chunk
            elif model.startswith("ollama:"):
                async for chunk in self._stream_ollama_completion(messages, model, temperature):
                    yield chunk
            else:
                # Try Ollama first
                try:
                    async for chunk in self._stream_ollama_completion(messages, model, temperature):
                        yield chunk
                except Exception:
                    raise ValueError(f"Model {model} not supported. Please use a valid model.")

        except Exception as e:
            logger.error(f"Error streaming completion: {str(e)}")
            yield f"Error: {str(e)}"

    async def _stream_openai_completion(self,
                                      messages: List[Dict[str, Any]],
                                      model: str,
                                      temperature: float) -> AsyncGenerator[str, None]:
        """Stream completion from OpenAI."""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")

        try:
            stream = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"OpenAI Streaming Error: {str(e)}"

    async def _stream_anthropic_completion(self,
                                         messages: List[Dict[str, Any]],
                                         model: str,
                                         temperature: float) -> AsyncGenerator[str, None]:
        """Stream completion from Anthropic."""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")

        try:
            # Convert OpenAI format to Anthropic format
            system_message = ""
            user_messages = []

            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)

            # Handle the case where we have user messages
            if user_messages:
                # If we have multiple messages, combine them
                if len(user_messages) > 1:
                    content = ""
                    for msg in user_messages:
                        content += f"{msg['role']}: {msg['content']}\n"
                else:
                    # Single user message
                    content = user_messages[0]["content"]

                # Prepare the API call parameters
                api_params = {
                    "model": model,
                    "max_tokens": 1000,
                    "temperature": temperature,
                    "messages": [{"role": "user", "content": content}],
                    "stream": True
                }

                # Only add system parameter if we have a system message
                if system_message:
                    api_params["system"] = system_message

                stream = await self.anthropic_client.messages.create(**api_params)
            else:
                raise ValueError("No user messages provided")

            async for chunk in stream:
                if chunk.type == "content_block_delta":
                    if chunk.delta.text:
                        yield chunk.delta.text

        except Exception as e:
            yield f"Anthropic Streaming Error: {str(e)}"

    async def _stream_gemini_completion(self,
                                       messages: List[Dict[str, Any]],
                                       model: str,
                                       temperature: float) -> AsyncGenerator[str, None]:
        """Stream completion from Google Gemini using OpenAI-compatible API."""
        model_name = model.replace("gemini:", "")

        llm_log("💎", "GEMINI/STREAM", f"Starting Gemini streaming request", {
            "model": model_name,
            "messages": len(messages)
        })

        if not self.gemini_client:
            raise ValueError("Gemini client not initialized")

        try:
            # Gemini supports OpenAI-compatible streaming!
            stream = await self.gemini_client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                stream=True
            )

            chunk_count = 0
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    chunk_count += 1
                    yield chunk.choices[0].delta.content

            llm_log("✅", "GEMINI/STREAM", f"Gemini streaming complete", {
                "chunks": chunk_count
            })

        except Exception as e:
            llm_log("❌", "GEMINI/STREAM", f"Gemini streaming error: {str(e)}")
            yield f"Gemini Streaming Error: {str(e)}"

    async def _stream_ollama_completion(self,
                                      messages: List[Dict[str, Any]],
                                      model: str,
                                      temperature: float) -> AsyncGenerator[str, None]:
        """Stream completion from Ollama."""
        if not self.ollama_client:
            raise ValueError("Ollama client not initialized")

        try:
            # Convert OpenAI format to Ollama format
            ollama_messages = []
            for msg in messages:
                content = msg.get("content", "")
                if isinstance(content, list):
                    text = " ".join(item.get("text", "") for item in content if item.get("type") == "text")
                else:
                    text = str(content)
                ollama_messages.append({"role": msg["role"], "content": text})

            # Remove ollama: prefix if present
            model_name = model.replace("ollama:", "")

            stream = await self.ollama_client.chat(
                model=model_name,
                messages=ollama_messages,
                options={"temperature": temperature},
                stream=True
            )

            async for chunk in stream:
                if chunk.get('message', {}).get('content'):
                    yield chunk['message']['content']

        except Exception as e:
            yield f"Ollama Streaming Error: {str(e)}"

    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        models = []

        if self.openai_client:
            models.extend([
                "gpt-4",
                "gpt-4-turbo",
                "gpt-3.5-turbo",
                "o1-preview",
                "o1-mini"
            ])

        if self.anthropic_client:
            models.extend([
                "claude-opus-4-1-20250805",
                "claude-opus-4-20250514",
                "claude-sonnet-4-20250514",
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022",
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ])

        if self.gemini_client:
            models.extend([
                "gemini-2.5-flash",
                "gemini-2.5-pro",
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro"
            ])

        # Get actual Ollama models
        ollama_models = self.get_ollama_models()
        if ollama_models and len(ollama_models) > 0:
            models.extend(ollama_models)

        return models

    def get_ollama_models(self) -> List[str]:
        """Get list of available Ollama models."""
        try:
            import subprocess
            import json

            # Run ollama list command (try JSON format first, then fallback to text parsing)
            try:
                result = subprocess.run(
                    ["ollama", "list", "--format", "json"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    models_data = json.loads(result.stdout)
                    models = []
                    for model in models_data:
                        model_name = model.get("name", "")
                        if model_name:
                            # Remove :latest suffix for cleaner display
                            clean_name = model_name.replace(":latest", "")
                            models.append(f"ollama:{clean_name}")
                    return models

            except Exception:
                # Fallback to text parsing if JSON format not supported
                pass

            # Try text parsing
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                models = []
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        # Parse model name from line (format: "model_name    id    size    modified")
                        # Split by whitespace and take the first part (model name)
                        parts = line.split()
                        if parts:
                            model_name = parts[0]
                            # Remove :latest suffix for cleaner display
                            clean_name = model_name.replace(":latest", "")
                            models.append(f"ollama:{clean_name}")
                return models
            else:
                logger.warning(f"Failed to get Ollama models: {result.stderr}")
                return []

        except subprocess.TimeoutExpired:
            logger.warning("Timeout getting Ollama models")
            return []
        except FileNotFoundError:
            logger.warning("Ollama not found in PATH")
            return []
        except Exception as e:
            logger.warning(f"Error getting Ollama models: {str(e)}")
            return []

    def get_default_model(self) -> str:
        """Get the default model to use, preferring Claude 3.5 Sonnet for optimal balance."""
        config_default = self.config.llm.default_model

        # Honor configured default if we can actually run it
        if self.is_model_available(config_default):
            return config_default

        available_models = self.get_available_models()
        if available_models:
            try:
                return self.get_best_model_for_task("general", available_models, prioritize_speed=True)
            except ValueError:
                pass

        # No fallback - raise error if no models available
        raise ValueError("No LLM models available. Please configure an API key or ensure Ollama is running with models.")

    def get_model_capabilities(self, model_name: str) -> Dict[str, Any]:
        """Get capabilities for a specific model."""
        # Remove prefixes for lookup
        clean_name = model_name.replace("ollama:", "").replace("gemini:", "").lower()

        # Model capability database
        capabilities = {
            # OpenAI models
            "gpt-4": {
                "reasoning": 95,
                "coding": 90,
                "analysis": 95,
                "creativity": 85,
                "speed": 70,
                "context_length": 128000,
                "type": "openai"
            },
            "gpt-4-turbo": {
                "reasoning": 95,
                "coding": 90,
                "analysis": 95,
                "creativity": 85,
                "speed": 85,
                "context_length": 128000,
                "type": "openai"
            },
            "gpt-3.5-turbo": {
                "reasoning": 80,
                "coding": 75,
                "analysis": 80,
                "creativity": 75,
                "speed": 90,
                "context_length": 16000,
                "type": "openai"
            },
            "o1-preview": {
                "reasoning": 98,
                "coding": 95,
                "analysis": 98,
                "creativity": 90,
                "speed": 30,
                "context_length": 128000,
                "type": "openai",
                "description": "OpenAI o1-preview: Advanced reasoning model with exceptional problem-solving capabilities"
            },
            "o1-mini": {
                "reasoning": 95,
                "coding": 90,
                "analysis": 95,
                "creativity": 85,
                "speed": 50,
                "context_length": 128000,
                "type": "openai",
                "description": "OpenAI o1-mini: Fast reasoning model with strong analytical capabilities"
            },

            # Anthropic Claude 4 models
            "claude-opus-4-1-20250805": {
                "reasoning": 98,
                "coding": 98,
                "analysis": 98,
                "creativity": 95,
                "speed": 60,
                "context_length": 200000,
                "type": "anthropic",
                "description": "Claude Opus 4.1: Most powerful and capable model with superior reasoning capabilities"
            },
            "claude-opus-4-20250514": {
                "reasoning": 97,
                "coding": 97,
                "analysis": 97,
                "creativity": 95,
                "speed": 65,
                "context_length": 200000,
                "type": "anthropic",
                "description": "Claude Opus 4: Previous flagship model with very high intelligence and capability"
            },
            "claude-sonnet-4-20250514": {
                "reasoning": 95,
                "coding": 95,
                "analysis": 95,
                "creativity": 90,
                "speed": 85,
                "context_length": 200000,
                "type": "anthropic",
                "description": "Claude Sonnet 4: High-performance model with exceptional reasoning and efficiency"
            },

            # Anthropic Claude 3.5 models
            "claude-3-5-sonnet-20241022": {
                "reasoning": 95,
                "coding": 95,
                "analysis": 95,
                "creativity": 90,
                "speed": 85,
                "context_length": 200000,
                "type": "anthropic",
                "description": "Claude 3.5 Sonnet: Latest and most capable Claude 3.5 model with excellent reasoning and coding"
            },
            "claude-3-5-haiku-20241022": {
                "reasoning": 90,
                "coding": 85,
                "analysis": 90,
                "creativity": 85,
                "speed": 95,
                "context_length": 200000,
                "type": "anthropic",
                "description": "Claude 3.5 Haiku: Fast and efficient Claude model for quick tasks"
            },

            # Anthropic Claude 3 models
            "claude-3-opus-20240229": {
                "reasoning": 95,
                "coding": 90,
                "analysis": 95,
                "creativity": 95,
                "speed": 70,
                "context_length": 200000,
                "type": "anthropic",
                "description": "Claude 3 Opus: Most capable Claude 3 model with exceptional reasoning and creativity"
            },
            "claude-3-sonnet-20240229": {
                "reasoning": 90,
                "coding": 90,
                "analysis": 90,
                "creativity": 85,
                "speed": 85,
                "context_length": 200000,
                "type": "anthropic",
                "description": "Claude 3 Sonnet: Balanced Claude 3 model with strong all-around capabilities"
            },
            "claude-3-haiku-20240307": {
                "reasoning": 85,
                "coding": 80,
                "analysis": 85,
                "creativity": 80,
                "speed": 95,
                "context_length": 200000,
                "type": "anthropic",
                "description": "Claude 3 Haiku: Fast Claude 3 model for quick and efficient tasks"
            },

            # Google Gemini models
            "gemini-2.5-flash": {
                "reasoning": 92,
                "coding": 90,
                "analysis": 92,
                "creativity": 88,
                "speed": 95,
                "context_length": 1000000,
                "type": "gemini",
                "description": "Gemini 2.5 Flash: Fast and capable model with 1M token context"
            },
            "gemini-2.5-pro": {
                "reasoning": 96,
                "coding": 95,
                "analysis": 96,
                "creativity": 92,
                "speed": 75,
                "context_length": 1000000,
                "type": "gemini",
                "description": "Gemini 2.5 Pro: Most capable Gemini model with advanced reasoning"
            },
            "gemini-2.0-flash": {
                "reasoning": 90,
                "coding": 88,
                "analysis": 90,
                "creativity": 85,
                "speed": 92,
                "context_length": 1000000,
                "type": "gemini",
                "description": "Gemini 2.0 Flash: Fast multimodal model"
            },
            "gemini-1.5-flash": {
                "reasoning": 88,
                "coding": 85,
                "analysis": 88,
                "creativity": 82,
                "speed": 90,
                "context_length": 1000000,
                "type": "gemini",
                "description": "Gemini 1.5 Flash: Efficient model with large context window"
            },
            "gemini-1.5-pro": {
                "reasoning": 93,
                "coding": 90,
                "analysis": 93,
                "creativity": 88,
                "speed": 70,
                "context_length": 2000000,
                "type": "gemini",
                "description": "Gemini 1.5 Pro: High-capability model with 2M token context"
            },

            # Common Ollama models
            "phi3": {
                "reasoning": 85,
                "coding": 80,
                "analysis": 85,
                "creativity": 80,
                "speed": 95,
                "context_length": 32000,
                "size_gb": 2.2,
                "type": "ollama",
                "description": "Microsoft Phi-3: Fast and efficient for general reasoning"
            },
            "gpt-oss": {
                "reasoning": 90,
                "coding": 95,
                "analysis": 90,
                "creativity": 85,
                "speed": 60,  # Much slower due to size
                "context_length": 32000,
                "size_gb": 13.0,
                "type": "ollama",
                "description": "GPT-OSS: Excellent for coding but slow due to size"
            },
            "gemma3n": {
                "reasoning": 85,
                "coding": 75,
                "analysis": 80,
                "creativity": 90,
                "speed": 75,  # Slower due to size
                "context_length": 32000,
                "size_gb": 7.5,
                "type": "ollama",
                "description": "Gemma 3N: Good for creative tasks but slower"
            },
            "llama3": {
                "reasoning": 90,
                "coding": 85,
                "analysis": 90,
                "creativity": 85,
                "speed": 80,
                "context_length": 128000,
                "type": "ollama",
                "description": "Llama 3: Strong general-purpose model"
            },
            "llama3.2": {
                "reasoning": 88,
                "coding": 80,
                "analysis": 88,
                "creativity": 82,
                "speed": 85,
                "context_length": 128000,
                "type": "ollama",
                "description": "Llama 3.2: Good balance of capabilities"
            },
            "mistral": {
                "reasoning": 85,
                "coding": 90,
                "analysis": 85,
                "creativity": 80,
                "speed": 90,
                "context_length": 32000,
                "type": "ollama",
                "description": "Mistral: Strong coding and reasoning"
            },
            "codellama": {
                "reasoning": 80,
                "coding": 95,
                "analysis": 75,
                "creativity": 70,
                "speed": 85,
                "context_length": 100000,
                "type": "ollama",
                "description": "Code Llama: Specialized for coding tasks"
            },
            "neural-chat": {
                "reasoning": 82,
                "coding": 75,
                "analysis": 85,
                "creativity": 90,
                "speed": 85,
                "context_length": 32000,
                "type": "ollama",
                "description": "Neural Chat: Good for conversational and creative tasks"
            }
        }

        # Try exact match first
        if clean_name in capabilities:
            return capabilities[clean_name]

        # Try partial matches
        for model_key, caps in capabilities.items():
            if clean_name in model_key or model_key in clean_name:
                return caps

        # Default capabilities for unknown models
        if "ollama:" in model_name:
            model_type = "ollama"
        elif "claude-" in model_name:
            model_type = "anthropic"
        elif "gemini" in model_name.lower():
            model_type = "gemini"
        else:
            model_type = "openai"

        return {
            "reasoning": 70,
            "coding": 70,
            "analysis": 70,
            "creativity": 70,
            "speed": 80,
            "context_length": 32000,
            "type": model_type,
            "description": "Unknown model with default capabilities"
        }

    def get_best_model_for_task(self,
                                task_type: str,
                                available_models: List[str] = None,
                                prioritize_speed: bool = False,
                                preferred_model: Optional[str] = None) -> str:
        """Get the best model for a specific task type."""
        if preferred_model and self.is_model_available(preferred_model):
            return preferred_model

        if available_models is None:
            available_models = self.get_available_models()

        if not available_models:
            raise ValueError("No LLM models available. Configure OPENAI_API_KEY, ANTHROPIC_API_KEY, or start Ollama with models.")

        # Task type weights
        task_weights = {
            "reasoning": ["reasoning", "analysis"],
            "coding": ["coding", "reasoning"],
            "analysis": ["analysis", "reasoning"],
            "creativity": ["creativity", "reasoning"],
            "general": ["reasoning", "analysis", "creativity", "coding"],
            "dce": ["reasoning", "analysis"],  # Discussion Continuity Expert
            "cae": ["analysis", "reasoning"],  # Critical Analysis Expert
            "domain": ["analysis", "reasoning", "coding"]  # Domain Expert
        }

        weights = task_weights.get(task_type, task_weights["general"])

        best_model = None
        best_score = 0

        for model in available_models:
            caps = self.get_model_capabilities(model)
            score = 0

            for weight in weights:
                score += caps.get(weight, 0)

            if prioritize_speed:
                # Heavily weight speed for fast mode
                score += caps.get("speed", 0) * 0.5
                # Penalty for large models
                size_gb = caps.get("size_gb", 0)
                if size_gb > 5:  # Penalty for models > 5GB
                    score -= (size_gb - 5) * 10
            else:
                # Normal speed bonus
                score += caps.get("speed", 0) * 0.1

            if score > best_score:
                best_score = score
                best_model = model

        return best_model or available_models[0]

    def get_model_info(self, model_name: str) -> str:
        """Get human-readable information about a model."""
        caps = self.get_model_capabilities(model_name)
        clean_name = model_name.replace("ollama:", "")

        info = f"Model: {clean_name}\n"
        info += f"Type: {caps.get('type', 'unknown').upper()}\n"
        info += f"Description: {caps.get('description', 'No description available')}\n\n"
        info += "Capabilities (0-100):\n"
        info += f"  Reasoning: {caps.get('reasoning', 0)}\n"
        info += f"  Coding: {caps.get('coding', 0)}\n"
        info += f"  Analysis: {caps.get('analysis', 0)}\n"
        info += f"  Creativity: {caps.get('creativity', 0)}\n"
        info += f"  Speed: {caps.get('speed', 0)}\n"
        info += f"  Context Length: {caps.get('context_length', 0):,} tokens"

        return info
