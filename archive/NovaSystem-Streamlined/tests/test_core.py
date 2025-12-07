"""
Tests for NovaSystem core components.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

from novasystem.core.agents import DCEAgent, CAEAgent, DomainExpert, AgentFactory
from novasystem.core.memory import MemoryManager
from novasystem.core.process import NovaProcess

class TestAgents:
    """Test agent functionality."""

    def test_dce_agent_creation(self):
        """Test DCE agent creation."""
        agent = DCEAgent()
        assert agent.name == "DCE"
        assert "Discussion Continuity Expert" in agent.role_description
        assert agent.model == "gpt-4"

    def test_cae_agent_creation(self):
        """Test CAE agent creation."""
        agent = CAEAgent()
        assert agent.name == "CAE"
        assert "Critical Analysis Expert" in agent.role_description
        assert agent.model == "gpt-4"

    def test_domain_expert_creation(self):
        """Test domain expert creation."""
        agent = DomainExpert("Technology")
        assert agent.name == "Domain Expert (Technology)"
        assert "Technology" in agent.role_description
        assert agent.domain == "Technology"

    def test_agent_factory(self):
        """Test agent factory."""
        team = AgentFactory.create_agent_team(["AI", "Business"])

        assert "dce" in team
        assert "cae" in team
        assert "expert_ai" in team
        assert "expert_business" in team

        assert isinstance(team["dce"], DCEAgent)
        assert isinstance(team["cae"], CAEAgent)
        assert isinstance(team["expert_ai"], DomainExpert)
        assert isinstance(team["expert_business"], DomainExpert)

class TestMemoryManager:
    """Test memory management functionality."""

    @pytest.mark.asyncio
    async def test_memory_storage(self):
        """Test memory storage and retrieval."""
        memory = MemoryManager()

        # Store context
        await memory.store_context("test_key", "test_data")

        # Retrieve context
        result = await memory.get_context("test_key")
        assert result == "test_data"

    @pytest.mark.asyncio
    async def test_memory_retrieval_nonexistent(self):
        """Test retrieving non-existent context."""
        memory = MemoryManager()

        result = await memory.get_context("nonexistent_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_relevant_context(self):
        """Test relevant context retrieval."""
        memory = MemoryManager()

        # Store multiple contexts
        await memory.store_context("ai_problem", "Machine learning optimization")
        await memory.store_context("business_problem", "Revenue optimization")
        await memory.store_context("tech_problem", "Database performance")

        # Get relevant context
        relevant = await memory.get_relevant_context("machine learning", limit=2)
        assert "ai_problem" in relevant
        assert "Machine learning optimization" in relevant

    def test_memory_stats(self):
        """Test memory statistics."""
        memory = MemoryManager()
        stats = memory.get_memory_stats()

        assert "short_term_count" in stats
        assert "long_term_count" in stats
        assert "total_contexts" in stats
        assert stats["short_term_count"] == 0
        assert stats["long_term_count"] == 0
        assert stats["total_contexts"] == 0

class TestNovaProcess:
    """Test Nova Process functionality."""

    def test_nova_process_creation(self):
        """Test Nova Process creation."""
        process = NovaProcess(domains=["AI", "Business"])

        assert process.domains == ["AI", "Business"]
        # Model should be intelligently selected (default is ollama:phi3)
        assert process.model is not None
        assert process.model.startswith("ollama:") or process.model.startswith("openai:")
        assert process.current_iteration == 0
        assert not process.is_active
        assert process.problem_statement == ""

    def test_nova_process_status(self):
        """Test Nova Process status."""
        process = NovaProcess(domains=["AI"])
        status = process.get_status()

        assert "is_active" in status
        assert "current_iteration" in status
        assert "total_iterations" in status
        assert "problem_statement" in status
        assert "domains" in status
        assert "model" in status

        assert status["is_active"] is False
        assert status["current_iteration"] == 0
        assert status["domains"] == ["AI"]
        # Model should be intelligently selected (default is ollama:phi3)
        assert status["model"] is not None
        assert status["model"].startswith("ollama:") or status["model"].startswith("openai:")

    def test_solution_history(self):
        """Test solution history."""
        process = NovaProcess()
        history = process.get_solution_history()

        assert isinstance(history, list)
        assert len(history) == 0

    @pytest.mark.asyncio
    async def test_problem_solving_mock(self):
        """Test problem solving with mocked agents."""
        # Create process with mocked agents
        process = NovaProcess(domains=["Test"])

        # Mock the agents to return predictable responses
        for agent in process.agents.values():
            agent.process = AsyncMock(return_value="Mocked response")

        # Run problem solving
        result = await process.solve_problem(
            "Test problem",
            max_iterations=1,
            stream=False
        )

        # Verify result structure
        assert isinstance(result, dict)
        assert "phase" in result
        assert result["phase"] == "final_synthesis"

if __name__ == "__main__":
    pytest.main([__file__])
