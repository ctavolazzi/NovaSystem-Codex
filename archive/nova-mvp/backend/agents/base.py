"""Base Agent class for Nova MVP."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Dict, Optional
from datetime import datetime
import uuid


@dataclass
class AgentResponse:
    """Structured response from an agent."""
    agent_id: str
    agent_type: str
    agent_name: str
    content: str
    model: str = "unknown"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None


class BaseAgent(ABC):
    """
    Abstract base class for all Nova agents.

    Each agent has a specific role in the problem-solving process:
    - DCE (Discussion Continuity Expert): Unpacks and clarifies the problem
    - CAE (Critical Analysis Expert): Provides critical analysis and edge cases
    - Domain Experts: Provide specialized domain knowledge
    """

    def __init__(self, name: str, agent_type: str, llm_provider=None):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.agent_type = agent_type
        self.llm = llm_provider
        self.created_at = datetime.utcnow()

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process input and return a response.

        Args:
            input_data: Dictionary containing 'problem' and optional context

        Returns:
            AgentResponse with the agent's analysis
        """
        pass

    async def _call_llm(self, user_message: str) -> str:
        """Call the LLM with the agent's system prompt."""
        if self.llm is None:
            return f"[{self.name}] LLM not configured - mock response for: {user_message[:100]}..."

        return await self.llm.chat(
            system_prompt=self.system_prompt,
            user_message=user_message
        )

    async def _call_llm_stream(self, user_message: str) -> AsyncIterator[str]:
        """Stream LLM response token by token."""
        if self.llm is None:
            yield f"[{self.name}] LLM not configured - mock response for: {user_message[:100]}..."
            return

        async for chunk in self.llm.chat_stream(
            system_prompt=self.system_prompt,
            user_message=user_message
        ):
            yield chunk

    async def process_stream(
        self,
        input_data: Dict[str, Any],
        on_token: Optional[callable] = None
    ) -> AgentResponse:
        """
        Process input with streaming output.

        Args:
            input_data: Dictionary containing 'problem' and optional context
            on_token: Optional callback called for each token (for real-time display)

        Returns:
            AgentResponse with the complete content after streaming
        """
        # Default implementation: collect streamed tokens
        # Subclasses can override for custom streaming behavior
        problem = input_data.get("problem", "")
        collected = []

        async for token in self._call_llm_stream(problem):
            collected.append(token)
            if on_token:
                on_token(token)

        content = "".join(collected)
        return self._create_response(content)

    def _create_response(
        self,
        content: str,
        success: bool = True,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Helper to create a standardized response."""
        # Get model name from LLM provider if available
        model_name = "unknown"
        if self.llm:
            model_name = self.llm.get_model_name()

        return AgentResponse(
            agent_id=self.id,
            agent_type=self.agent_type,
            agent_name=self.name,
            content=content,
            model=model_name,
            success=success,
            error=error,
            metadata=metadata or {}
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id}, name={self.name})>"
