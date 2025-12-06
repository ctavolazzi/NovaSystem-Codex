"""LLM Provider Abstraction Layer.

Supports:
- Claude (Anthropic)
- OpenAI (GPT-4)
- Mock (for testing without API keys)

Designed for easy swapping to Ollama or other providers later.

Includes Traffic Control integration with Smart Retry:
- Pre-flight rate limit checks
- Exponential backoff with jitter on rate limit hits
- Automatic retry (no crashes during multi-agent debates)
"""

import os
import asyncio
import random
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass

from .traffic import get_traffic_controller, RateLimitExceeded
from .pricing import CostEstimator, estimate_tokens_from_text
from .usage import get_usage_tracker, extract_usage, UsageRecord


# Default retry configuration
DEFAULT_MAX_RETRIES = 5
DEFAULT_BASE_DELAY = 1.0  # seconds
DEFAULT_MAX_DELAY = 60.0  # seconds


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    model: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60
    # Retry configuration
    max_retries: int = DEFAULT_MAX_RETRIES
    base_delay: float = DEFAULT_BASE_DELAY
    max_delay: float = DEFAULT_MAX_DELAY


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: Optional[LLMConfig] = None, enable_traffic_control: bool = True, enable_usage_tracking: bool = True):
        self.config = config or self._default_config()
        self.enable_traffic_control = enable_traffic_control
        self.enable_usage_tracking = enable_usage_tracking
        self._traffic_controller = get_traffic_controller() if enable_traffic_control else None
        self._usage_tracker = get_usage_tracker() if enable_usage_tracking else None
        self.cost_estimator = CostEstimator()
        # Callback for logging/UI updates during retry
        self.on_retry: Optional[Callable[[int, float], None]] = None
        # Last raw API response (for usage extraction)
        self._last_raw_response: Any = None

    @abstractmethod
    def _default_config(self) -> LLMConfig:
        """Return default configuration for this provider."""
        pass

    @abstractmethod
    async def _execute_chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        """
        Execute the actual API call (implemented by subclasses).

        This is the "raw" call without retry logic.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is available (API key configured)."""
        pass

    def get_model_name(self) -> str:
        """Return the model name being used by this provider."""
        return self.config.model

    def estimate_cost(self, input_text: str, estimated_output_tokens: int = 1000):
        """Estimate cost for a request before making it."""
        try:
            return self.cost_estimator.estimate(
                model=self.config.model,
                input_text=input_text,
                estimated_output_tokens=estimated_output_tokens
            )
        except ValueError:
            # Model not in pricing table - return None
            return None

    def _estimate_tokens(self, system_prompt: str, user_message: str, max_tokens: int) -> int:
        """Estimate total tokens for a request."""
        input_tokens = estimate_tokens_from_text(system_prompt) + estimate_tokens_from_text(user_message)
        return input_tokens + max(0, max_tokens or 0)

    def _calculate_backoff(self, attempt: int, retry_after: float) -> float:
        """
        Calculate backoff time with exponential increase and jitter.

        Formula: min(max_delay, max(retry_after, base_delay * 2^attempt) + jitter)
        """
        base = self.config.base_delay * (2 ** attempt)
        # Use the larger of retry_after or calculated backoff
        delay = max(retry_after, base)
        # Cap at max_delay
        delay = min(delay, self.config.max_delay)
        # Add jitter (±20%) to prevent thundering herd
        jitter = delay * random.uniform(-0.2, 0.2)
        return delay + jitter

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        """
        Send a chat message with Smart Retry on rate limits.

        This is the main entry point that wraps _execute_chat with:
        1. Pre-flight rate limit check
        2. Exponential backoff retry on RateLimitExceeded
        3. Usage tracking with reconciliation (actual vs estimated)

        Args:
            system_prompt: The system prompt for the conversation
            user_message: The user's message

        Returns:
            The assistant's response text

        Raises:
            Exception: After max_retries exceeded
        """
        model = kwargs.get("model", self.config.model)
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)
        estimated_tokens = self._estimate_tokens(system_prompt, user_message, max_tokens)

        # Get estimated cost (if model is in pricing table)
        estimated_cost = 0.0
        try:
            cost_estimate = self.cost_estimator.estimate(model, system_prompt + user_message, max_tokens)
            estimated_cost = cost_estimate.projected_cost
        except ValueError:
            pass  # Model not in pricing table

        attempt = 0
        last_error = None
        usage_record: Optional[UsageRecord] = None

        while attempt <= self.config.max_retries:
            try:
                # 1. PRE-FLIGHT CHECK: Verify rate limits before calling
                if self._traffic_controller:
                    self._traffic_controller.check_allowance(model, estimated_tokens)

                # 2. EXECUTE: Make the actual API call
                response = await self._execute_chat(system_prompt, user_message, **kwargs)

                # 3. USAGE TRACKING: Record usage with reconciliation
                if self._usage_tracker:
                    usage_record = self._usage_tracker.record(
                        model=model,
                        estimated_tokens=estimated_tokens,
                        estimated_cost=estimated_cost,
                    )
                    
                    # RECONCILIATION: Try to extract actual usage from last response
                    if self._last_raw_response:
                        actual_usage = extract_usage(self._last_raw_response)
                        if actual_usage:
                            self._usage_tracker.update_actual(
                                usage_record,
                                actual_tokens=actual_usage["total_tokens"]
                            )

                return response

            except RateLimitExceeded as e:
                last_error = e
                attempt += 1

                if attempt > self.config.max_retries:
                    break

                # 4. SMART RETRY: Calculate backoff and wait
                wait_time = self._calculate_backoff(attempt - 1, e.retry_after)

                # Notify callback if registered (for UI/logging)
                if self.on_retry:
                    self.on_retry(attempt, wait_time)
                else:
                    # Default logging
                    print(f"🚦 Traffic Control: Rate limit hit. "
                          f"Retry {attempt}/{self.config.max_retries} in {wait_time:.1f}s...")

                await asyncio.sleep(wait_time)

        # All retries exhausted
        raise Exception(
            f"Rate limit exceeded after {self.config.max_retries} retries. "
            f"Last error: {last_error}"
        )


class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider."""

    def __init__(self, config: Optional[LLMConfig] = None, api_key: Optional[str] = None, enable_traffic_control: bool = True):
        super().__init__(config, enable_traffic_control)
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._client = None

    def _default_config(self) -> LLMConfig:
        return LLMConfig(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            temperature=0.7
        )

    def is_available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("anthropic package required. Install with: pip install anthropic")
        return self._client

    async def _execute_chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        """Execute the actual Claude API call."""
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)
        model = kwargs.get("model", self.config.model)

        client = self._get_client()

        # Run in thread pool since anthropic client is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
        )

        # Store raw response for usage extraction (reconciliation)
        self._last_raw_response = response

        return response.content[0].text


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def __init__(self, config: Optional[LLMConfig] = None, api_key: Optional[str] = None, enable_traffic_control: bool = True):
        super().__init__(config, enable_traffic_control)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self._client = None

    def _default_config(self) -> LLMConfig:
        return LLMConfig(
            model="gpt-4o",
            max_tokens=4096,
            temperature=0.7
        )

    def is_available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("openai package required. Install with: pip install openai")
        return self._client

    async def _execute_chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        """Execute the actual OpenAI API call."""
        max_tokens = kwargs.get("max_tokens", self.config.max_tokens)
        model = kwargs.get("model", self.config.model)

        client = self._get_client()

        # Run in thread pool since openai client is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                temperature=kwargs.get("temperature", self.config.temperature),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
        )

        # Store raw response for usage extraction (reconciliation)
        self._last_raw_response = response

        return response.choices[0].message.content


class MockProvider(LLMProvider):
    """Mock provider for testing without API keys."""

    def __init__(self, config: Optional[LLMConfig] = None, delay: float = 0.5, enable_traffic_control: bool = True):
        super().__init__(config, enable_traffic_control)
        self.delay = delay

    def _default_config(self) -> LLMConfig:
        return LLMConfig(model="mock-v1", max_tokens=4096, temperature=0.7)

    def is_available(self) -> bool:
        return True  # Always available

    async def _execute_chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        """Execute the mock response generation."""
        await asyncio.sleep(self.delay)

        # Generate a structured mock response based on system prompt
        if "DCE" in system_prompt or "Discussion Continuity" in system_prompt:
            return self._mock_dce_response(user_message)
        elif "CAE" in system_prompt or "Critical Analysis" in system_prompt:
            return self._mock_cae_response(user_message)
        elif "Expert" in system_prompt:
            return self._mock_domain_response(system_prompt, user_message)
        else:
            return self._mock_generic_response(user_message)

    def _mock_dce_response(self, problem: str) -> str:
        return f"""## Problem Analysis

**Core Challenge**: Analyzing "{problem[:50]}..."

**Key Components**:
1. Primary concern identified
2. Secondary factors to consider
3. Stakeholder impacts

**Stakeholders**:
- Direct users
- Technical team
- Business stakeholders

**Constraints**:
- Time and resource limitations
- Technical feasibility
- Budget considerations

**Success Criteria**:
- Clear deliverables defined
- Measurable outcomes established

**Questions for Experts**:
- What technical approaches are most suitable?
- What risks should we prioritize?"""

    def _mock_cae_response(self, problem: str) -> str:
        return f"""## Critical Analysis

**Assumption Check**:
- Assumption 1: Users have necessary access - Risk: Medium
- Assumption 2: Timeline is realistic - Risk: High

**Risk Assessment**:
| Risk | Severity | Mitigation |
|------|----------|------------|
| Scope creep | High | Define clear boundaries |
| Technical debt | Medium | Code review process |
| Resource constraints | Medium | Prioritize features |

**Edge Cases**:
1. High load scenarios
2. Network failures
3. Invalid input handling

**Blind Spots**:
- Long-term maintenance implications
- Cross-team dependencies

**Mitigation Strategies**:
- Implement monitoring early
- Create fallback mechanisms
- Document assumptions"""

    def _mock_domain_response(self, system_prompt: str, problem: str) -> str:
        domain = "Technical"
        if "Business" in system_prompt:
            domain = "Business"
        elif "Security" in system_prompt:
            domain = "Security"
        elif "UX" in system_prompt or "User Experience" in system_prompt:
            domain = "UX"

        return f"""## {domain} Expert Analysis

**Domain Relevance**: This problem directly impacts {domain.lower()} considerations.

**Key Insights**:
1. Industry best practices suggest iterative approach
2. Similar solutions have proven effective elsewhere
3. Key metrics should be established early

**Best Practices**:
- Follow established {domain.lower()} standards
- Implement proper testing frameworks
- Document decisions and rationale

**Opportunities**:
- Leverage existing tools and frameworks
- Build on proven patterns
- Create reusable components

**Domain Risks**:
- Underestimating complexity
- Insufficient expertise
- Changing requirements

**Recommendations**:
1. Start with proof of concept
2. Gather early feedback
3. Iterate based on results"""

    def _mock_generic_response(self, message: str) -> str:
        return f"""## Response

Analyzing: "{message[:100]}..."

Key points:
1. Consider the primary objectives
2. Evaluate available options
3. Recommend evidence-based approach

Next steps:
- Gather additional context
- Consult relevant stakeholders
- Develop detailed plan"""


def get_llm(
    provider: str = "auto",
    api_key: Optional[str] = None,
    config: Optional[LLMConfig] = None
) -> LLMProvider:
    """
    Factory function to get an LLM provider.

    Args:
        provider: "claude", "openai", "mock", or "auto" (tries claude, then openai, then mock)
        api_key: Optional API key (overrides environment variable)
        config: Optional LLMConfig

    Returns:
        Configured LLMProvider instance
    """
    if provider == "claude":
        return ClaudeProvider(config=config, api_key=api_key)
    elif provider == "openai":
        return OpenAIProvider(config=config, api_key=api_key)
    elif provider == "mock":
        return MockProvider(config=config)
    elif provider == "auto":
        # Try Claude first, then OpenAI, then Mock
        claude = ClaudeProvider(config=config, api_key=api_key)
        if claude.is_available():
            return claude

        openai = OpenAIProvider(config=config, api_key=api_key)
        if openai.is_available():
            return openai

        # Fall back to mock
        return MockProvider(config=config)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'claude', 'openai', 'mock', or 'auto'")
