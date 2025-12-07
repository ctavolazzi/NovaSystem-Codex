"""
Nova Process Agent Definitions.

This module defines the specialized agents used in the Nova Process:
- DCE (Discussion Continuity Expert): Manages conversation flow
- CAE (Critical Analysis Expert): Provides critical evaluation
- Domain Expert: Provides specialized knowledge

Uses structured prompts following Gemini best practices.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import logging

from ..utils.llm_service import LLMService
from ..utils.prompt_builder import PromptBuilder, Verbosity, Tone, Example
from ..config.models import get_model_for_agent, get_default_model

logger = logging.getLogger(__name__)

# Console logging helper
def agent_log(emoji: str, agent: str, message: str, details: dict = None):
    """Log an agent event with emoji prefix."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [AGENT/{agent}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"           └─ {key}: {val_str}")

class BaseAgent(ABC):
    """Base class for all Nova Process agents."""

    def __init__(self, name: str, role_description: str, model: Optional[str] = None, llm_service: Optional[LLMService] = None):
        self.name = name
        self.role_description = role_description
        # Use single source of truth for model configuration
        self.model = model or get_default_model()
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

    def _build_structured_prompt(self) -> PromptBuilder:
        """Build a structured prompt using the PromptBuilder."""
        builder = PromptBuilder()
        builder.set_role(f"You are {self.name}. {self.role_description}")
        builder.set_verbosity(Verbosity.MEDIUM)
        builder.set_tone(Tone.TECHNICAL)
        builder.add_constraint("Be precise and analytical")
        builder.add_constraint("Support conclusions with reasoning")
        return builder

    async def _call_llm(self, input_text: str, context: Optional[str] = None) -> str:
        """Make a call to the LLM service with structured prompts."""
        try:
            task_type = self._get_task_type()

            agent_log("🎯", self.name, f"Processing request", {
                "task_type": task_type,
                "input_preview": input_text[:60],
                "has_context": bool(context)
            })

            # Prefer the explicitly configured model when available
            available_models = self.llm_service.get_available_models()
            if self.model and self.llm_service.is_model_available(self.model):
                model_to_use = self.model
            elif available_models:
                model_to_use = self.llm_service.get_best_model_for_task(
                    task_type,
                    available_models=available_models,
                    prioritize_speed=True
                )
                if model_to_use != self.model:
                    agent_log("⚠️", self.name, f"Model fallback: {self.model} → {model_to_use}")
            else:
                raise ValueError("No LLM models available. Please configure API keys or ensure Ollama is running with models.")

            # Build structured messages using PromptBuilder
            builder = self._build_structured_prompt()

            # Build the user prompt with context
            user_prompt = builder.build_user_prompt(
                task=input_text,
                context=context,
                final_instruction="Think step-by-step and provide a clear, structured response."
            )

            messages = [
                {"role": "system", "content": builder.build_system_prompt()},
                {"role": "user", "content": user_prompt}
            ]

            # Add conversation history (last 5 messages for continuity)
            for msg in self.conversation_history[-5:]:
                messages.append(msg)

            agent_log("📤", self.name, f"Calling LLM", {
                "model": model_to_use,
                "messages": len(messages)
            })

            # Call LLM service with the best model for the task
            response = await self.llm_service.get_completion(
                messages=messages,
                model=model_to_use,
                temperature=0.7
            )

            # Add to conversation history
            self.add_to_history("user", input_text)
            self.add_to_history("assistant", response)

            agent_log("✅", self.name, f"Response received", {
                "response_length": len(response)
            })

            return response

        except Exception as e:
            agent_log("❌", self.name, f"Error: {str(e)}")
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

    def __init__(self, model: Optional[str] = None, llm_service: Optional[LLMService] = None):
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
        # Use centralized model configuration
        agent_model = model or get_model_for_agent("dce")
        super().__init__("DCE", role_description, agent_model, llm_service)

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

    def __init__(self, model: Optional[str] = None, llm_service: Optional[LLMService] = None):
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
        # Use centralized model configuration
        agent_model = model or get_model_for_agent("cae")
        super().__init__("CAE", role_description, agent_model, llm_service)

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

    def __init__(self, domain: str, model: Optional[str] = None, llm_service: Optional[LLMService] = None):
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
        # Use centralized model configuration
        agent_model = model or get_model_for_agent("domain_expert")
        super().__init__(f"Domain Expert ({domain})", role_description, agent_model, llm_service)
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
    def create_dce(model: Optional[str] = None, llm_service: Optional[LLMService] = None) -> DCEAgent:
        """Create a DCE agent."""
        return DCEAgent(model, llm_service)

    @staticmethod
    def create_cae(model: Optional[str] = None, llm_service: Optional[LLMService] = None) -> CAEAgent:
        """Create a CAE agent."""
        return CAEAgent(model, llm_service)

    @staticmethod
    def create_domain_expert(domain: str, model: Optional[str] = None, llm_service: Optional[LLMService] = None) -> DomainExpert:
        """Create a domain expert agent."""
        return DomainExpert(domain, model, llm_service)

    @staticmethod
    def create_agent_team(domains: List[str], model: Optional[str] = None, llm_service: Optional[LLMService] = None) -> Dict[str, BaseAgent]:
        """Create a complete team of agents."""
        team = {
            "dce": AgentFactory.create_dce(model, llm_service),
            "cae": AgentFactory.create_cae(model, llm_service),
        }

        for domain in domains:
            team[f"expert_{domain.lower().replace(' ', '_')}"] = AgentFactory.create_domain_expert(domain, model, llm_service)

        return team
