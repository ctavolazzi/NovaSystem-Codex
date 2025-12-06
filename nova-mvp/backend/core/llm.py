"""LLM Provider Abstraction Layer.

Supports:
- Claude (Anthropic)
- OpenAI (GPT-4)
- Mock (for testing without API keys)

Designed for easy swapping to Ollama or other providers later.
"""

import os
import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    model: str
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 60


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or self._default_config()

    @abstractmethod
    def _default_config(self) -> LLMConfig:
        """Return default configuration for this provider."""
        pass

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

    def __init__(self, config: Optional[LLMConfig] = None, api_key: Optional[str] = None):
        super().__init__(config)
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
        client = self._get_client()

        # Run in thread pool since anthropic client is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.messages.create(
                model=kwargs.get("model", self.config.model),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
        )

        return response.content[0].text


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def __init__(self, config: Optional[LLMConfig] = None, api_key: Optional[str] = None):
        super().__init__(config)
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
        client = self._get_client()

        # Run in thread pool since openai client is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=kwargs.get("model", self.config.model),
                max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                temperature=kwargs.get("temperature", self.config.temperature),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
        )

        return response.choices[0].message.content


class MockProvider(LLMProvider):
    """Mock provider for testing without API keys."""

    def __init__(self, config: Optional[LLMConfig] = None, delay: float = 0.5):
        super().__init__(config)
        self.delay = delay

    def _default_config(self) -> LLMConfig:
        return LLMConfig(model="mock-v1", max_tokens=4096, temperature=0.7)

    def is_available(self) -> bool:
        return True  # Always available

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        **kwargs
    ) -> str:
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
