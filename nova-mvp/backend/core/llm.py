"""LLM Provider Abstraction Layer.

Supports:
- Claude (Anthropic)
- OpenAI (GPT-4)
- Mock (for testing without API keys)

Designed for easy swapping to Ollama or other providers later.
Includes usage tracking for cost reconciliation.
"""

import os
import time
import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass

from .traffic import traffic_controller, estimate_tokens
from .pricing import CostEstimator
from .usage import get_usage_ledger, Transaction


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    model: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    # Override in subclasses
    PROVIDER_NAME: str = "unknown"

    def __init__(self, config: Optional[LLMConfig] = None, track_usage: bool = True):
        self.config = config or self._default_config()
        self._track_usage = track_usage
        self._cost_estimator = CostEstimator()
        self._ledger = get_usage_ledger() if track_usage else None

    @abstractmethod
    def _default_config(self) -> LLMConfig:
        """Return default configuration for this provider."""
        pass

    def _enforce_limits(
        self, system_prompt: str, user_message: str, **kwargs: Any
    ) -> Tuple[int, int]:
        """Estimate token usage and enforce local RPM/TPM ceilings.

        Returns (input_tokens, estimated_output_tokens) for usage tracking.
        """
        model_name = kwargs.get("model", self.config.model)
        input_tokens = estimate_tokens(system_prompt) + estimate_tokens(user_message)
        estimated_output_tokens = kwargs.get("max_tokens", self.config.max_tokens)
        traffic_controller.check_allowance(
            model_name,
            input_tokens,
            estimated_output_tokens=estimated_output_tokens,
        )
        return input_tokens, estimated_output_tokens

    def _record_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        actual_input: Optional[int] = None,
        actual_output: Optional[int] = None,
        context: str = "general",
    ) -> None:
        """Record a transaction to the usage ledger."""
        if not self._ledger:
            return

        # Estimate cost
        try:
            estimate = self._cost_estimator.estimate(
                model, " " * (input_tokens * 4), output_tokens
            )
            estimated_cost = estimate.projected_cost
        except ValueError:
            # Model not in pricing table - estimate zero
            estimated_cost = 0.0

        # Calculate actual cost if we have actual token counts
        actual_cost = None
        if actual_input is not None and actual_output is not None:
            try:
                actual_estimate = self._cost_estimator.estimate(
                    model, " " * (actual_input * 4), actual_output
                )
                actual_cost = actual_estimate.projected_cost
            except ValueError:
                pass

        txn = Transaction(
            timestamp=time.time(),
            model=model,
            provider=self.PROVIDER_NAME,
            input_tokens=actual_input or input_tokens,
            output_tokens=actual_output or output_tokens,
            estimated_cost=estimated_cost,
            actual_cost=actual_cost,
            context=context,
        )
        self._ledger.record(txn)

    @abstractmethod
    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        """
        Send a chat message and get a response.

        Args:
            system_prompt: The system prompt for the conversation
            user_message: The user's message

        Returns:
            The assistant's response text
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is available (API key configured)."""
        pass

    def get_model_name(self) -> str:
        """Return the model name being used by this provider."""
        return self.config.model


class ClaudeProvider(LLMProvider):
    """Anthropic Claude provider."""

    PROVIDER_NAME = "claude"

    def __init__(self, config: Optional[LLMConfig] = None, api_key: Optional[str] = None, track_usage: bool = True):
        super().__init__(config, track_usage)
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

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        input_tokens, est_output = self._enforce_limits(system_prompt, user_message, **kwargs)
        client = self._get_client()
        model = kwargs.get("model", self.config.model)

        # Run in thread pool since anthropic client is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.messages.create(
                model=model,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
        )

        # Extract actual usage from Claude response
        actual_in = getattr(response.usage, 'input_tokens', None)
        actual_out = getattr(response.usage, 'output_tokens', None)

        self._record_usage(
            model=model,
            input_tokens=input_tokens,
            output_tokens=est_output,
            actual_input=actual_in,
            actual_output=actual_out,
            context=kwargs.get("context", "general"),
        )

        return response.content[0].text


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    PROVIDER_NAME = "openai"

    def __init__(self, config: Optional[LLMConfig] = None, api_key: Optional[str] = None, track_usage: bool = True):
        super().__init__(config, track_usage)
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

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        input_tokens, est_output = self._enforce_limits(system_prompt, user_message, **kwargs)
        client = self._get_client()
        model = kwargs.get("model", self.config.model)

        # Run in thread pool since openai client is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=model,
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
        )

        # Extract actual usage from OpenAI response
        actual_in = getattr(response.usage, 'prompt_tokens', None) if response.usage else None
        actual_out = getattr(response.usage, 'completion_tokens', None) if response.usage else None

        self._record_usage(
            model=model,
            input_tokens=input_tokens,
            output_tokens=est_output,
            actual_input=actual_in,
            actual_output=actual_out,
            context=kwargs.get("context", "general"),
        )

        return response.choices[0].message.content


class MockProvider(LLMProvider):
    """Mock provider for testing without API keys."""

    PROVIDER_NAME = "mock"

    def __init__(self, config: Optional[LLMConfig] = None, delay: float = 0.5, track_usage: bool = True):
        super().__init__(config, track_usage)
        self.delay = delay

    def _default_config(self) -> LLMConfig:
        return LLMConfig(model="mock-v1", max_tokens=4096, temperature=0.7)

    def is_available(self) -> bool:
        return True  # Always available

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

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
        input_tokens, est_output = self._enforce_limits(system_prompt, user_message, **kwargs)
        model = kwargs.get("model", self.config.model)
        await asyncio.sleep(self.delay)

        # Generate response
        if "DCE" in system_prompt or "Discussion Continuity" in system_prompt:
            response = self._mock_dce_response(user_message)
        elif "CAE" in system_prompt or "Critical Analysis" in system_prompt:
            response = self._mock_cae_response(user_message)
        elif "Expert" in system_prompt:
            response = self._mock_domain_response(system_prompt, user_message)
        else:
            response = self._mock_generic_response(user_message)

        # Mock providers don't have actual token counts, use estimates
        self._record_usage(
            model=model,
            input_tokens=input_tokens,
            output_tokens=est_output,
            context=kwargs.get("context", "general"),
        )

        return response


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
