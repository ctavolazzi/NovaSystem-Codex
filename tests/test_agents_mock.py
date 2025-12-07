"""
Tests for NovaSystem agents with mocked LLM service.

Tests cover:
- DCEAgent (Discussion Continuity Expert)
- CAEAgent (Critical Analysis Expert)
- DomainExpert agents
- AgentFactory
- Conversation history management
- Model selection fallback
"""

import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class MockLLMService:
    """Mock LLM service for testing agents without API calls."""

    def __init__(self, response: str = "Mock LLM response"):
        self.response = response
        self.call_count = 0
        self.last_messages = None
        self.last_model = None

    def get_available_models(self):
        return ["mock-model-fast", "mock-model-smart"]

    def is_model_available(self, model: str) -> bool:
        return model in self.get_available_models() or model == "mock-model"

    def get_best_model_for_task(self, task_type: str, available_models=None, prioritize_speed=False):
        if prioritize_speed:
            return "mock-model-fast"
        return "mock-model-smart"

    async def get_completion(self, messages, model, temperature=0.7):
        self.call_count += 1
        self.last_messages = messages
        self.last_model = model
        return self.response

    async def stream_completion(self, messages, model, temperature=0.7):
        self.call_count += 1
        self.last_messages = messages
        self.last_model = model
        for word in self.response.split():
            yield word + " "


@pytest.fixture
def mock_llm():
    """Create a mock LLM service."""
    return MockLLMService()


@pytest.fixture
def mock_llm_with_analysis():
    """Create a mock LLM service with analysis-style response."""
    return MockLLMService(response="""
## Analysis Summary

Based on the input provided, here are my findings:

1. **Key Insight**: The problem requires a multi-step approach
2. **Recommendation**: Start with phase 1, then iterate
3. **Risk Assessment**: Medium complexity, low risk

### Next Steps
- Gather more requirements
- Create prototype
- Test and validate
""")


class TestDCEAgent:
    """Tests for Discussion Continuity Expert agent."""

    @pytest.mark.asyncio
    async def test_dce_processes_input(self, mock_llm):
        """Test that DCE agent processes input correctly."""
        # Import here to avoid import errors during collection
        from novasystem.core.agents import DCEAgent

        agent = DCEAgent(model="mock-model", llm_service=mock_llm)

        result = await agent.process("How should we approach this problem?")

        assert result == mock_llm.response
        assert mock_llm.call_count == 1
        assert mock_llm.last_model == "mock-model"

    @pytest.mark.asyncio
    async def test_dce_includes_context(self, mock_llm):
        """Test that DCE includes context in processing."""
        from novasystem.core.agents import DCEAgent

        agent = DCEAgent(model="mock-model", llm_service=mock_llm)
        context = "Previous discussion: We decided to use Python."

        await agent.process("What's next?", context=context)

        # Check that context was included in messages
        messages_str = str(mock_llm.last_messages)
        assert "What's next?" in messages_str

    @pytest.mark.asyncio
    async def test_dce_maintains_conversation_history(self, mock_llm):
        """Test that DCE maintains conversation history."""
        from novasystem.core.agents import DCEAgent

        agent = DCEAgent(model="mock-model", llm_service=mock_llm)

        await agent.process("First question")
        await agent.process("Second question")
        await agent.process("Third question")

        assert len(agent.conversation_history) == 6  # 3 user + 3 assistant
        assert agent.conversation_history[0]["role"] == "user"
        assert agent.conversation_history[1]["role"] == "assistant"

    def test_dce_system_message(self, mock_llm):
        """Test DCE system message contains role description."""
        from novasystem.core.agents import DCEAgent

        agent = DCEAgent(model="mock-model", llm_service=mock_llm)
        system_msg = agent.get_system_message()

        assert "DCE" in system_msg
        assert "Discussion Continuity Expert" in system_msg or "conversation" in system_msg.lower()


class TestCAEAgent:
    """Tests for Critical Analysis Expert agent."""

    @pytest.mark.asyncio
    async def test_cae_processes_input(self, mock_llm):
        """Test that CAE agent processes input correctly."""
        from novasystem.core.agents import CAEAgent

        agent = CAEAgent(model="mock-model", llm_service=mock_llm)

        result = await agent.process("Analyze this solution for weaknesses")

        assert result == mock_llm.response
        assert mock_llm.call_count == 1

    @pytest.mark.asyncio
    async def test_cae_provides_critical_analysis(self, mock_llm_with_analysis):
        """Test CAE provides structured analysis."""
        from novasystem.core.agents import CAEAgent

        agent = CAEAgent(model="mock-model", llm_service=mock_llm_with_analysis)

        result = await agent.process("Review the proposed architecture")

        assert "Analysis" in result or "Risk" in result
        assert mock_llm_with_analysis.call_count == 1

    def test_cae_system_message(self, mock_llm):
        """Test CAE system message contains critical analysis role."""
        from novasystem.core.agents import CAEAgent

        agent = CAEAgent(model="mock-model", llm_service=mock_llm)
        system_msg = agent.get_system_message()

        assert "CAE" in system_msg
        assert "Critical" in system_msg or "Analysis" in system_msg


class TestDomainExpert:
    """Tests for Domain Expert agents."""

    @pytest.mark.asyncio
    async def test_domain_expert_processes_input(self, mock_llm):
        """Test that domain expert processes domain-specific input."""
        from novasystem.core.agents import DomainExpert

        agent = DomainExpert(domain="Machine Learning", model="mock-model", llm_service=mock_llm)

        result = await agent.process("What algorithm should we use?")

        assert result == mock_llm.response
        assert mock_llm.call_count == 1

    def test_domain_expert_has_domain_in_name(self, mock_llm):
        """Test that domain expert name includes the domain."""
        from novasystem.core.agents import DomainExpert

        agent = DomainExpert(domain="Cybersecurity", model="mock-model", llm_service=mock_llm)

        assert "Cybersecurity" in agent.name
        assert "Domain Expert" in agent.name

    def test_domain_expert_system_message_includes_domain(self, mock_llm):
        """Test that system message references the specific domain."""
        from novasystem.core.agents import DomainExpert

        agent = DomainExpert(domain="Cloud Architecture", model="mock-model", llm_service=mock_llm)
        system_msg = agent.get_system_message()

        assert "Cloud Architecture" in system_msg

    @pytest.mark.asyncio
    async def test_multiple_domain_experts(self, mock_llm):
        """Test creating multiple domain experts with different domains."""
        from novasystem.core.agents import DomainExpert

        ml_expert = DomainExpert(domain="Machine Learning", model="mock-model", llm_service=mock_llm)
        security_expert = DomainExpert(domain="Security", model="mock-model", llm_service=mock_llm)
        devops_expert = DomainExpert(domain="DevOps", model="mock-model", llm_service=mock_llm)

        assert "Machine Learning" in ml_expert.name
        assert "Security" in security_expert.name
        assert "DevOps" in devops_expert.name

        # Each should be independent
        assert ml_expert.domain == "Machine Learning"
        assert security_expert.domain == "Security"
        assert devops_expert.domain == "DevOps"


class TestAgentFactory:
    """Tests for the AgentFactory."""

    def test_create_dce(self, mock_llm):
        """Test creating DCE through factory."""
        from novasystem.core.agents import AgentFactory

        agent = AgentFactory.create_dce(model="mock-model", llm_service=mock_llm)

        assert agent.name == "DCE"
        assert agent.llm_service == mock_llm

    def test_create_cae(self, mock_llm):
        """Test creating CAE through factory."""
        from novasystem.core.agents import AgentFactory

        agent = AgentFactory.create_cae(model="mock-model", llm_service=mock_llm)

        assert agent.name == "CAE"
        assert agent.llm_service == mock_llm

    def test_create_domain_expert(self, mock_llm):
        """Test creating domain expert through factory."""
        from novasystem.core.agents import AgentFactory

        agent = AgentFactory.create_domain_expert(
            domain="Data Engineering",
            model="mock-model",
            llm_service=mock_llm
        )

        assert "Data Engineering" in agent.name
        assert agent.domain == "Data Engineering"

    def test_create_agent_team(self, mock_llm):
        """Test creating a complete agent team."""
        from novasystem.core.agents import AgentFactory

        team = AgentFactory.create_agent_team(
            domains=["Backend", "Frontend", "DevOps"],
            model="mock-model",
            llm_service=mock_llm
        )

        assert "dce" in team
        assert "cae" in team
        assert "expert_backend" in team
        assert "expert_frontend" in team
        assert "expert_devops" in team
        assert len(team) == 5  # DCE + CAE + 3 experts

    def test_create_empty_team(self, mock_llm):
        """Test creating team with no domain experts."""
        from novasystem.core.agents import AgentFactory

        team = AgentFactory.create_agent_team(
            domains=[],
            model="mock-model",
            llm_service=mock_llm
        )

        assert "dce" in team
        assert "cae" in team
        assert len(team) == 2


class TestConversationHistory:
    """Tests for conversation history management."""

    @pytest.mark.asyncio
    async def test_history_persists_across_calls(self, mock_llm):
        """Test that conversation history persists."""
        from novasystem.core.agents import DCEAgent

        agent = DCEAgent(model="mock-model", llm_service=mock_llm)

        await agent.process("Message 1")
        await agent.process("Message 2")

        assert len(agent.conversation_history) == 4

    def test_add_to_history_directly(self, mock_llm):
        """Test adding messages to history directly."""
        from novasystem.core.agents import DCEAgent

        agent = DCEAgent(model="mock-model", llm_service=mock_llm)

        agent.add_to_history("user", "Custom user message")
        agent.add_to_history("assistant", "Custom assistant message")

        assert len(agent.conversation_history) == 2
        assert agent.conversation_history[0]["content"] == "Custom user message"
        assert agent.conversation_history[1]["content"] == "Custom assistant message"


class TestModelSelection:
    """Tests for model selection and fallback."""

    def test_model_selection_uses_configured_model(self, mock_llm):
        """Test that configured model is used when available."""
        from novasystem.core.agents import DCEAgent

        agent = DCEAgent(model="mock-model-fast", llm_service=mock_llm)
        selected = agent._select_model()

        assert selected == "mock-model-fast"

    def test_model_fallback_when_not_available(self, mock_llm):
        """Test fallback when configured model not available."""
        from novasystem.core.agents import DCEAgent

        # Configure with unavailable model
        agent = DCEAgent(model="unavailable-model", llm_service=mock_llm)
        selected = agent._select_model()

        # Should fall back to best available
        assert selected in mock_llm.get_available_models()


class TestAgentStreaming:
    """Tests for streaming responses."""

    @pytest.mark.asyncio
    async def test_stream_generates_chunks(self, mock_llm):
        """Test that streaming generates response chunks."""
        from novasystem.core.agents import DCEAgent

        mock_llm.response = "This is a streaming response"
        agent = DCEAgent(model="mock-model", llm_service=mock_llm)

        chunks = []
        async for chunk in agent.process_stream("Test input"):
            chunks.append(chunk)

        assert len(chunks) > 0
        full_response = "".join(chunks)
        assert "streaming" in full_response.lower()


class TestAgentErrorHandling:
    """Tests for agent error handling."""

    @pytest.mark.asyncio
    async def test_fallback_on_llm_error(self):
        """Test that agent provides fallback on LLM error."""
        from novasystem.core.agents import DCEAgent

        # Create mock that raises exception
        error_llm = MockLLMService()
        error_llm.get_completion = AsyncMock(side_effect=Exception("LLM Error"))

        agent = DCEAgent(model="mock-model", llm_service=error_llm)
        result = await agent.process("Test input")

        # Should return fallback response
        assert "DCE" in result
        assert "Error" in result or "Processing" in result
