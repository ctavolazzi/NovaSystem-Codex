"""
Nova Process Agent Definitions.

This module defines the specialized agents used in the Nova Process:
- DCE (Discussion Continuity Expert): Manages conversation flow
- CAE (Critical Analysis Expert): Provides critical evaluation
- Domain Expert: Provides specialized knowledge
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import asyncio
import logging

from ..utils.llm_service import LLMService

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all Nova Process agents."""

    def __init__(self, name: str, role_description: str, model: str = "gpt-4", llm_service: Optional[LLMService] = None):
        self.name = name
        self.role_description = role_description
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.llm_service = llm_service or LLMService()

    @abstractmethod
    async def process(self, input_text: str, context: Optional[str] = None) -> str:
        """Process input and return response."""
        pass

    def add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_system_message(self) -> str:
        """Get the system message for this agent."""
        return f"You are {self.name}. {self.role_description}"

    async def _call_llm(self, input_text: str, context: Optional[str] = None) -> str:
        """Make a call to the LLM service."""
        try:
            # Get the best model for this agent's task type
            task_type = self._get_task_type()
            best_model = self.llm_service.get_best_model_for_task(task_type)

            # Use the best model if different from current
            model_to_use = best_model if best_model != self.model else self.model

            # Build messages
            messages = [
                {"role": "system", "content": self.get_system_message()}
            ]

            # Add context if provided
            if context:
                messages.append({"role": "user", "content": f"Context: {context}\n\nInput: {input_text}"})
            else:
                messages.append({"role": "user", "content": input_text})

            # Add conversation history
            for msg in self.conversation_history[-5:]:  # Last 5 messages for context
                messages.append(msg)

            # Call LLM service with the best model for the task
            response = await self.llm_service.get_completion(
                messages=messages,
                model=model_to_use,
                temperature=0.7
            )

            # Add to conversation history
            self.add_to_history("user", input_text)
            self.add_to_history("assistant", response)

            return response

        except Exception as e:
            logger.error(f"Error calling LLM for {self.name}: {str(e)}")
            # Fallback to mock response if LLM fails
            return self._get_fallback_response(input_text)

    def _get_task_type(self) -> str:
        """Get the task type for this agent."""
        # Override in subclasses for specific task types
        return "general"

    def _get_fallback_response(self, input_text: str) -> str:
        """Get a fallback response when LLM fails."""
        return f"[{self.name} - LLM Error] Processing: {input_text[:100]}..."

class DCEAgent(BaseAgent):
    """
    Discussion Continuity Expert (DCE) Agent.

    Responsible for maintaining conversation flow and ensuring coherent problem-solving.
    """

    def __init__(self, model: str = "gpt-4", llm_service: Optional[LLMService] = None):
        role_description = """
        You are the Discussion Continuity Expert (DCE). Your role is to:

        1. **Maintain Conversation Flow**: Keep discussions focused and coherent
        2. **Summarize Progress**: Provide clear summaries of what has been accomplished
        3. **Guide Next Steps**: Suggest logical next steps in the problem-solving process
        4. **Synthesize Insights**: Combine different perspectives into coherent understanding
        5. **Ensure Completion**: Make sure all aspects of the problem are addressed

        Always structure your responses with:
        - Clear summary of current state
        - Key insights identified
        - Recommended next steps
        - Questions for clarification if needed
        """
        super().__init__("DCE", role_description, model, llm_service)

    def _get_task_type(self) -> str:
        """DCE specializes in reasoning and analysis."""
        return "dce"

    async def process(self, input_text: str, context: Optional[str] = None) -> str:
        """Process input as DCE and return structured response."""
        return await self._call_llm(input_text, context)

class CAEAgent(BaseAgent):
    """
    Critical Analysis Expert (CAE) Agent.

    Provides critical evaluation and identifies potential issues.
    """

    def __init__(self, model: str = "gpt-4", llm_service: Optional[LLMService] = None):
        role_description = """
        You are the Critical Analysis Expert (CAE). Your role is to:

        1. **Critical Evaluation**: Analyze proposed solutions for weaknesses
        2. **Risk Assessment**: Identify potential risks and failure points
        3. **Quality Assurance**: Ensure solutions meet quality standards
        4. **Alternative Perspectives**: Suggest alternative approaches
        5. **Validation**: Verify assumptions and claims

        Always provide:
        - Specific concerns with evidence
        - Alternative approaches to consider
        - Risk mitigation strategies
        - Validation requirements
        """
        super().__init__("CAE", role_description, model, llm_service)

    def _get_task_type(self) -> str:
        """CAE specializes in critical analysis."""
        return "cae"

    async def process(self, input_text: str, context: Optional[str] = None) -> str:
        """Process input as CAE and return critical analysis."""
        return await self._call_llm(input_text, context)

class DomainExpert(BaseAgent):
    """
    Domain Expert Agent.

    Provides specialized knowledge in specific domains.
    """

    def __init__(self, domain: str, model: str = "gpt-4", llm_service: Optional[LLMService] = None):
        role_description = f"""
        You are a Domain Expert in {domain}. Your role is to:

        1. **Domain Knowledge**: Provide expertise in {domain}
        2. **Best Practices**: Recommend industry standards and best practices
        3. **Technical Solutions**: Suggest specific technical approaches
        4. **Implementation Guidance**: Provide practical implementation advice
        5. **Resource Recommendations**: Suggest tools, libraries, and resources

        Always provide:
        - Specific technical recommendations
        - Industry best practices
        - Implementation considerations
        - Resource suggestions
        """
        super().__init__(f"Domain Expert ({domain})", role_description, model, llm_service)
        self.domain = domain

    def _get_task_type(self) -> str:
        """Domain Expert specializes in domain-specific analysis."""
        return "domain"

    async def process(self, input_text: str, context: Optional[str] = None) -> str:
        """Process input as Domain Expert and return specialized advice."""
        return await self._call_llm(input_text, context)

class AgentFactory:
    """Factory for creating Nova Process agents."""

    @staticmethod
    def create_dce(model: str = "gpt-4", llm_service: Optional[LLMService] = None) -> DCEAgent:
        """Create a DCE agent."""
        return DCEAgent(model, llm_service)

    @staticmethod
    def create_cae(model: str = "gpt-4", llm_service: Optional[LLMService] = None) -> CAEAgent:
        """Create a CAE agent."""
        return CAEAgent(model, llm_service)

    @staticmethod
    def create_domain_expert(domain: str, model: str = "gpt-4", llm_service: Optional[LLMService] = None) -> DomainExpert:
        """Create a domain expert agent."""
        return DomainExpert(domain, model, llm_service)

    @staticmethod
    def create_agent_team(domains: List[str], model: str = "gpt-4", llm_service: Optional[LLMService] = None) -> Dict[str, BaseAgent]:
        """Create a complete team of agents."""
        team = {
            "dce": AgentFactory.create_dce(model, llm_service),
            "cae": AgentFactory.create_cae(model, llm_service),
        }

        for domain in domains:
            team[f"expert_{domain.lower().replace(' ', '_')}"] = AgentFactory.create_domain_expert(domain, model, llm_service)

        return team
