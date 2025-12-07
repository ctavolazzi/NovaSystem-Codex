"""
Nova Process Agent Definitions.

This module defines the specialized agents used in the Nova Process:
- DCE (Discussion Continuity Expert): Manages conversation flow
- CAE (Critical Analysis Expert): Provides critical evaluation
- Domain Expert: Provides specialized knowledge
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, AsyncGenerator, Tuple
import logging

from ..utils.llm_service import LLMService
from ..utils.prompt_builder import PromptBuilder, Verbosity, Tone
from ..utils.colors import Colors, AGENT_COLORS, console_log
from ..config.models import get_model_for_agent, get_default_model

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role_description: str
    task_type: str
    model: Optional[str] = None


class BaseAgent(ABC):
    """Base class for all Nova Process agents."""

    def __init__(
        self,
        name: str,
        role_description: str,
        model: Optional[str] = None,
        llm_service: Optional[LLMService] = None
    ):
        self.name = name
        self.role_description = role_description
        self.model = model or get_default_model()
        self.conversation_history: List[Dict[str, str]] = []
        self.llm_service = llm_service or LLMService()

    @abstractmethod
    async def process(self, input_text: str, context: Optional[str] = None) -> str:
        """Process input and return response."""
        pass

    async def process_stream(self, input_text: str, context: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Process input and stream response token by token."""
        async for chunk in self._call_llm_stream(input_text, context):
            yield chunk

    def add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_system_message(self) -> str:
        """Get the system message for this agent."""
        return f"You are {self.name}. {self.role_description}"

    def _get_task_type(self) -> str:
        """Get the task type for this agent. Override in subclasses."""
        return "general"

    def _get_fallback_response(self, input_text: str) -> str:
        """Get a fallback response when LLM fails."""
        return f"[{self.name} - LLM Error] Processing: {input_text[:100]}..."

    def _build_messages(self, input_text: str, context: Optional[str] = None) -> List[Dict[str, str]]:
        """Build messages list for LLM call."""
        builder = PromptBuilder()
        builder.set_role(f"You are {self.name}. {self.role_description}")
        builder.set_verbosity(Verbosity.MEDIUM)
        builder.set_tone(Tone.TECHNICAL)
        builder.add_constraint("Be precise and analytical")
        builder.add_constraint("Support conclusions with reasoning")

        user_prompt = builder.build_user_prompt(
            task=input_text,
            context=context,
            final_instruction="Think step-by-step and provide a clear, structured response."
        )

        messages = [
            {"role": "system", "content": builder.build_system_prompt()},
            {"role": "user", "content": user_prompt}
        ]

        # Add conversation history (last 5 messages)
        for msg in self.conversation_history[-5:]:
            messages.append(msg)

        return messages

    def _select_model(self) -> str:
        """Select the best available model for this agent."""
        task_type = self._get_task_type()
        available_models = self.llm_service.get_available_models()

        # Prefer explicitly configured model
        if self.model and self.llm_service.is_model_available(self.model):
            return self.model

        # Fallback to best model for task
        if available_models:
            best = self.llm_service.get_best_model_for_task(
                task_type,
                available_models=available_models,
                prioritize_speed=True
            )
            if best != self.model:
                console_log("⚠️", f"AGENT/{self.name}", f"Model fallback: {self.model} → {best}")
            return best

        raise ValueError("No LLM models available. Please configure API keys or ensure Ollama is running.")

    async def _call_llm(self, input_text: str, context: Optional[str] = None) -> str:
        """Make a call to the LLM service."""
        try:
            console_log("🎯", f"AGENT/{self.name}", "Processing request", {
                "task_type": self._get_task_type(),
                "input_preview": input_text[:60],
                "has_context": bool(context)
            })

            model = self._select_model()
            messages = self._build_messages(input_text, context)

            console_log("📤", f"AGENT/{self.name}", f"Calling LLM", {
                "model": model,
                "messages": len(messages)
            })

            response = await self.llm_service.get_completion(
                messages=messages,
                model=model,
                temperature=0.7
            )

            # Update conversation history
            self.add_to_history("user", input_text)
            self.add_to_history("assistant", response)

            console_log("✅", f"AGENT/{self.name}", "Response received", {
                "response_length": len(response)
            })

            return response

        except Exception as e:
            console_log("❌", f"AGENT/{self.name}", f"Error: {e}")
            logger.error(f"Error calling LLM for {self.name}: {e}")
            return self._get_fallback_response(input_text)

    async def _call_llm_stream(self, input_text: str, context: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Stream tokens from the LLM service."""
        try:
            console_log("🎯", f"AGENT/{self.name}", "Starting streaming request", {
                "task_type": self._get_task_type(),
                "input_preview": input_text[:60],
            })

            model = self._select_model()
            messages = self._build_messages(input_text, context)

            # Get agent color
            agent_color = AGENT_COLORS.get(self.name.split(" (")[0], Colors.BLUE)

            # Print agent header
            print(f"\n{agent_color}{Colors.BOLD}{'='*60}{Colors.END}")
            print(f"{agent_color}{Colors.BOLD}📢 {self.name}{Colors.END}")
            print(f"{agent_color}{'='*60}{Colors.END}")
            print(f"{agent_color}", end="", flush=True)

            # Stream tokens
            full_response = []
            async for chunk in self.llm_service.stream_completion(
                messages=messages,
                model=model,
                temperature=0.7
            ):
                full_response.append(chunk)
                print(chunk, end="", flush=True)
                yield chunk

            print(f"{Colors.END}\n")

            # Update history
            complete_text = "".join(full_response)
            self.add_to_history("user", input_text)
            self.add_to_history("assistant", complete_text)

            console_log("✅", f"AGENT/{self.name}", "Streaming complete", {
                "total_words": len(complete_text.split())
            })

        except Exception as e:
            console_log("❌", f"AGENT/{self.name}", f"Streaming error: {e}")
            yield self._get_fallback_response(input_text)


class DCEAgent(BaseAgent):
    """
    Discussion Continuity Expert (DCE) Agent.

    Responsible for maintaining conversation flow and ensuring coherent problem-solving.
    """

    ROLE_DESCRIPTION = """
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

    def __init__(self, model: Optional[str] = None, llm_service: Optional[LLMService] = None):
        agent_model = model or get_model_for_agent("dce")
        super().__init__("DCE", self.ROLE_DESCRIPTION, agent_model, llm_service)

    def _get_task_type(self) -> str:
        return "dce"

    async def process(self, input_text: str, context: Optional[str] = None) -> str:
        return await self._call_llm(input_text, context)


class CAEAgent(BaseAgent):
    """
    Critical Analysis Expert (CAE) Agent.

    Provides critical evaluation and identifies potential issues.
    """

    ROLE_DESCRIPTION = """
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

    def __init__(self, model: Optional[str] = None, llm_service: Optional[LLMService] = None):
        agent_model = model or get_model_for_agent("cae")
        super().__init__("CAE", self.ROLE_DESCRIPTION, agent_model, llm_service)

    def _get_task_type(self) -> str:
        return "cae"

    async def process(self, input_text: str, context: Optional[str] = None) -> str:
        return await self._call_llm(input_text, context)


class DomainExpert(BaseAgent):
    """
    Domain Expert Agent.

    Provides specialized knowledge in specific domains.
    """

    ROLE_TEMPLATE = """
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

    def __init__(self, domain: str, model: Optional[str] = None, llm_service: Optional[LLMService] = None):
        role_description = self.ROLE_TEMPLATE.format(domain=domain)
        agent_model = model or get_model_for_agent("domain_expert")
        super().__init__(f"Domain Expert ({domain})", role_description, agent_model, llm_service)
        self.domain = domain

    def _get_task_type(self) -> str:
        return "domain"

    async def process(self, input_text: str, context: Optional[str] = None) -> str:
        return await self._call_llm(input_text, context)


class AgentFactory:
    """Factory for creating Nova Process agents."""

    @staticmethod
    def create_dce(model: Optional[str] = None, llm_service: Optional[LLMService] = None) -> DCEAgent:
        return DCEAgent(model, llm_service)

    @staticmethod
    def create_cae(model: Optional[str] = None, llm_service: Optional[LLMService] = None) -> CAEAgent:
        return CAEAgent(model, llm_service)

    @staticmethod
    def create_domain_expert(
        domain: str,
        model: Optional[str] = None,
        llm_service: Optional[LLMService] = None
    ) -> DomainExpert:
        return DomainExpert(domain, model, llm_service)

    @staticmethod
    def create_agent_team(
        domains: List[str],
        model: Optional[str] = None,
        llm_service: Optional[LLMService] = None
    ) -> Dict[str, BaseAgent]:
        """Create a complete team of agents."""
        team = {
            "dce": AgentFactory.create_dce(model, llm_service),
            "cae": AgentFactory.create_cae(model, llm_service),
        }

        for domain in domains:
            key = f"expert_{domain.lower().replace(' ', '_')}"
            team[key] = AgentFactory.create_domain_expert(domain, model, llm_service)

        return team
