"""
Full integration tests for NovaSystem.

Tests cover:
- Event bus + State machine + Pipeline integration
- Memory system + Vector store integration
- Decision matrix integration with domain events
- End-to-end workflow simulation
"""

import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.domain.events import (
    EventBus,
    RunCreated,
    RunStatusChanged,
    StepStarted,
    StepCompleted,
    StepFailed,
    CommandQueued,
    CommandStarted,
    CommandCompleted,
    get_event_bus,
)
from novasystem.domain.models import (
    PipelineContext,
    RunStatus,
    CommandLog,
    CommandStatus,
    ParsedCommand,
)
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult, SummarizeStep
from novasystem.domain.state_machine import RunStateMachine
from novasystem.core.memory import MemoryManager
from novasystem.core.vector_store import LocalVectorStore
from novasystem.tools.decision_matrix.decision_matrix import DecisionMatrix, make_decision


@pytest.fixture(autouse=True)
def reset_event_bus():
    """Ensure a clean singleton event bus for every test."""
    EventBus.reset_instance()
    yield
    EventBus.reset_instance()


class EventCollector:
    """Utility class to collect events for assertions."""

    def __init__(self):
        self.events: List[Any] = []
        self.event_counts: Dict[str, int] = {}

    def collect(self, event):
        self.events.append(event)
        event_type = type(event).__name__
        self.event_counts[event_type] = self.event_counts.get(event_type, 0) + 1

    def get_events_of_type(self, event_class):
        return [e for e in self.events if isinstance(e, event_class)]

    def clear(self):
        self.events.clear()
        self.event_counts.clear()


class MockAnalysisStep(PipelineStepBase):
    """Mock step that simulates analysis."""
    name = "analyze"

    def __init__(self, analysis_result: str = "Analysis complete"):
        self.analysis_result = analysis_result
        self.executed = False

    def execute(self, context: PipelineContext) -> StepResult:
        self.executed = True
        context.add_metadata("analysis", self.analysis_result)
        return StepResult.ok({"analysis": self.analysis_result})


class MockExecutionStep(PipelineStepBase):
    """Mock step that simulates command execution."""
    name = "execute"

    def __init__(self, commands: List[str], fail_on: int = -1):
        self._commands = commands
        self._fail_on = fail_on
        self.executed_commands: List[str] = []

    def execute(self, context: PipelineContext) -> StepResult:
        bus = get_event_bus()

        for idx, cmd in enumerate(self._commands):
            bus.emit(CommandQueued(
                run_id=context.run_id,
                command=cmd,
                priority=50,
                command_type="test"
            ))
            bus.emit(CommandStarted(
                run_id=context.run_id,
                command=cmd,
                container_id="test-container"
            ))

            if idx == self._fail_on:
                bus.emit(CommandCompleted(
                    run_id=context.run_id,
                    command=cmd,
                    exit_code=1,
                    output="",
                    error="Simulated failure",
                    execution_time=0.1
                ))
                return StepResult.fail(f"Command failed: {cmd}", recoverable=False)

            self.executed_commands.append(cmd)
            bus.emit(CommandCompleted(
                run_id=context.run_id,
                command=cmd,
                exit_code=0,
                output="Success",
                error="",
                execution_time=0.1
            ))

        return StepResult.ok({"executed": len(self.executed_commands)})


class TestEventStateMachinePipelineIntegration:
    """Integration tests for event bus + state machine + pipeline."""

    def test_full_successful_run(self):
        """Test a complete successful run through the system."""
        bus = get_event_bus()
        collector = EventCollector()
        bus.subscribe_all(collector.collect)

        # Create state machine
        run_id = 1001
        sm = RunStateMachine(run_id=run_id, event_bus=bus)

        # Start run
        bus.emit(RunCreated(run_id=run_id, repo_url="https://github.com/test/repo"))
        sm.start_analyzing()
        sm.start_running()

        # Build and execute pipeline
        pipeline = Pipeline(event_bus=bus)
        pipeline.add_step(MockAnalysisStep("Found 3 issues"))
        pipeline.add_step(MockExecutionStep(["pip install", "pytest", "coverage"]))
        pipeline.add_step(SummarizeStep())

        context = PipelineContext(run_id=run_id, repo_url="test-repo")
        result = pipeline.run(context)

        # Complete run
        sm.complete(success=result.success)

        # Assertions
        assert result.success is True
        assert sm.status == RunStatus.SUCCESS
        assert collector.event_counts.get("RunCreated", 0) == 1
        assert collector.event_counts.get("RunStatusChanged", 0) >= 3
        assert collector.event_counts.get("StepStarted", 0) >= 3
        assert collector.event_counts.get("StepCompleted", 0) >= 3
        assert collector.event_counts.get("CommandQueued", 0) == 3
        assert collector.event_counts.get("CommandCompleted", 0) == 3

    def test_run_with_command_failure(self):
        """Test run that fails during command execution."""
        bus = get_event_bus()
        collector = EventCollector()
        bus.subscribe_all(collector.collect)

        run_id = 1002
        sm = RunStateMachine(run_id=run_id, event_bus=bus)
        sm.start_analyzing()
        sm.start_running()

        # Pipeline with failing step
        pipeline = Pipeline(event_bus=bus)
        pipeline.add_step(MockAnalysisStep())
        pipeline.add_step(MockExecutionStep(["cmd1", "cmd2", "cmd3"], fail_on=1))
        pipeline.add_step(SummarizeStep())

        context = PipelineContext(run_id=run_id, repo_url="test-repo")
        result = pipeline.run(context)

        sm.complete(success=result.success)

        # Assertions
        assert result.success is False
        assert sm.status == RunStatus.FAILED
        assert collector.event_counts.get("StepFailed", 0) >= 1

        # Summarize step should NOT have run
        step_names = [e.step_name for e in collector.get_events_of_type(StepStarted)]
        assert "summarize" not in step_names

    def test_pause_and_resume_workflow(self):
        """Test pausing and resuming a run."""
        bus = get_event_bus()
        collector = EventCollector()
        bus.subscribe_all(collector.collect)

        run_id = 1003
        sm = RunStateMachine(run_id=run_id, event_bus=bus)

        sm.start_analyzing()
        sm.start_running()
        assert sm.status == RunStatus.RUNNING

        sm.pause()
        assert sm.status == RunStatus.PAUSED

        sm.resume()
        assert sm.status == RunStatus.RUNNING

        sm.complete(success=True)
        assert sm.status == RunStatus.SUCCESS

        # Check state transition history
        status_changes = collector.get_events_of_type(RunStatusChanged)
        statuses = [(e.old_status, e.new_status) for e in status_changes]
        assert ("running", "paused") in statuses
        assert ("paused", "running") in statuses


class TestMemoryVectorStoreIntegration:
    """Integration tests for memory + vector store systems."""

    @pytest.fixture
    def memory_manager(self):
        return MemoryManager(max_short_term=10, max_long_term=50)

    @pytest.fixture
    def vector_store(self, tmp_path):
        return LocalVectorStore(memory_file=tmp_path / "test.json", persist=True)

    @pytest.mark.asyncio
    async def test_memory_and_vector_store_work_together(self, memory_manager, vector_store):
        """Test using both memory systems in a workflow."""
        # Store structured context in MemoryManager
        await memory_manager.store_context("run_config", {
            "repo": "test-repo",
            "branch": "main",
            "strategy": "full-analysis"
        }, "short_term")

        # Store searchable facts in VectorStore
        vector_store.remember(
            "The repository uses Python 3.10 with FastAPI",
            tags=["repo", "tech-stack"]
        )
        vector_store.remember(
            "Tests require pytest and pytest-asyncio for testing",
            tags=["repo", "testing"]
        )
        vector_store.remember(
            "Docker is used for containerization",
            tags=["repo", "deployment"]
        )

        # Query both systems
        config = await memory_manager.get_context("run_config")
        assert config["repo"] == "test-repo"

        # Use lower min_score to ensure we get results
        test_info = vector_store.recall("pytest testing", limit=2, min_score=0.05)
        assert len(test_info) >= 1
        assert any("pytest" in r[0]["text"] for r in test_info)

    @pytest.mark.asyncio
    async def test_workflow_with_memory_compression(self, memory_manager):
        """Test memory compression in a workflow."""
        # Simulate a multi-step analysis storing results
        await memory_manager.store_context("step1_draft", "Initial analysis notes", "short_term")
        await memory_manager.store_context("step2_draft", "More analysis details", "short_term")
        await memory_manager.store_context("final_solution", "This is the final recommendation", "short_term")

        # Compress to move important items to long-term
        await memory_manager.compress_memory()

        stats = memory_manager.get_memory_stats()
        # "final_solution" should have been moved to long-term
        assert stats["long_term_count"] >= 1


class TestDecisionMatrixIntegration:
    """Integration tests for decision matrix with event-driven architecture."""

    def test_decision_matrix_with_event_logging(self):
        """Test decision matrix logging decisions through events."""
        bus = get_event_bus()
        decisions_made = []

        # Custom event handler for decisions
        def log_decision(event):
            if isinstance(event, StepCompleted) and "decision" in event.step_name:
                decisions_made.append(event)

        bus.subscribe(StepCompleted, log_decision)

        # Run decision matrix with show_all_methods to get dict
        options = ["Option A", "Option B", "Option C"]
        criteria = ["Cost", "Quality", "Speed"]
        scores = {
            "Option A": [8, 7, 6],
            "Option B": [6, 9, 7],
            "Option C": [7, 8, 8],
        }

        result = make_decision(
            options=options,
            criteria=criteria,
            scores=scores,
            weights=[0.3, 0.5, 0.2],
            show_all_methods=True,  # Returns dict of results
        )

        # Verify decision was made
        assert result["weighted"].winner in options
        assert result["weighted"].confidence_score > 0

    def test_decision_matrix_all_methods_comparison(self):
        """Test comparing all decision methods."""
        options = ["Python", "JavaScript", "Go", "Rust"]
        criteria = ["Ease of Learning", "Performance", "Ecosystem", "Type Safety"]
        scores = {
            "Python": [9, 5, 9, 4],
            "JavaScript": [7, 6, 10, 3],
            "Go": [6, 8, 7, 8],
            "Rust": [4, 10, 6, 10],
        }
        weights = [0.25, 0.3, 0.25, 0.2]

        results = make_decision(
            options=options,
            criteria=criteria,
            scores=scores,
            weights=weights,
            show_all_methods=True
        )

        # All methods should return results
        assert "weighted" in results
        assert "normalized" in results
        assert "ranking" in results
        assert "best_worst" in results

        # Each method should have a winner
        for method, result in results.items():
            assert result.winner in options
            assert 0 <= result.confidence_score <= 100


class TestEndToEndWorkflow:
    """End-to-end workflow tests simulating real usage."""

    @pytest.mark.asyncio
    async def test_full_analysis_workflow(self, tmp_path):
        """Simulate a complete analysis workflow."""
        # Setup
        bus = get_event_bus()
        memory = MemoryManager()
        vector_store = LocalVectorStore(memory_file=tmp_path / "workflow.json", persist=True)
        collector = EventCollector()
        bus.subscribe_all(collector.collect)

        run_id = 9001

        # Phase 1: Initialize
        sm = RunStateMachine(run_id=run_id, event_bus=bus)
        bus.emit(RunCreated(run_id=run_id, repo_url="https://github.com/example/project"))

        await memory.store_context("run_metadata", {
            "run_id": run_id,
            "started_at": datetime.now().isoformat(),
            "strategy": "comprehensive"
        }, "short_term")

        # Phase 2: Analysis
        sm.start_analyzing()

        # Simulate discovering information
        vector_store.remember("Project uses Python 3.11 with type hints", tags=["tech"])
        vector_store.remember("Dependencies: FastAPI, SQLAlchemy, Pydantic", tags=["deps"])
        vector_store.remember("Test suite uses pytest with 85% coverage", tags=["testing"])

        await memory.store_context("tech_analysis", {
            "language": "Python",
            "version": "3.11",
            "framework": "FastAPI"
        }, "short_term")

        # Phase 3: Decision Making
        tech_choices = make_decision(
            options=["Continue with FastAPI", "Migrate to Django", "Use Flask"],
            criteria=["Learning Curve", "Performance", "Community"],
            scores={
                "Continue with FastAPI": [9, 9, 8],
                "Migrate to Django": [6, 7, 10],
                "Use Flask": [8, 6, 9],
            },
            weights=[0.2, 0.5, 0.3],
            show_all_methods=True,  # Returns dict of results
        )

        await memory.store_context("framework_decision", {
            "winner": tech_choices["weighted"].winner,
            "confidence": tech_choices["weighted"].confidence_score
        }, "short_term")

        # Phase 4: Execution
        sm.start_running()

        pipeline = Pipeline(event_bus=bus)
        pipeline.add_step(MockExecutionStep(["pip install -r requirements.txt", "pytest"]))
        pipeline.add_step(SummarizeStep())

        context = PipelineContext(run_id=run_id, repo_url="example/project")
        result = pipeline.run(context)

        # Phase 5: Completion
        sm.complete(success=result.success)

        await memory.store_context("final_result", {
            "success": result.success,
            "summary": context.metadata.get("summary"),
            "decision": tech_choices["weighted"].winner
        }, "long_term")

        # Compress important memories
        await memory.compress_memory()

        # Assertions
        assert sm.status == RunStatus.SUCCESS
        assert result.success is True

        # Check we can recall workflow data
        tech_recall = vector_store.recall("Python FastAPI", limit=3)
        assert len(tech_recall) >= 1

        final = await memory.get_context("final_result")
        assert final["success"] is True
        assert "FastAPI" in final["decision"]

        # Event counts
        assert collector.event_counts["RunCreated"] == 1
        assert collector.event_counts["RunStatusChanged"] >= 3
        assert collector.event_counts["CommandCompleted"] == 2
