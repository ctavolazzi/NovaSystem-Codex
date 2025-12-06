"""NovaProcess - Multi-agent orchestration with parallel processing.

The NovaProcess manages the three-phase problem-solving workflow:
1. UNPACK - DCE breaks down the problem
2. ANALYZE - Domain experts and CAE analyze in parallel
3. SYNTHESIZE - DCE combines all perspectives

Agents run in parallel where possible using asyncio.gather().
"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from ..agents import (
    BaseAgent,
    DCEAgent,
    CAEAgent,
    DomainExpert,
    create_domain_expert,
    AgentResponse
)
from .llm import LLMProvider, get_llm


class ProcessPhase(str, Enum):
    """Phases of the Nova problem-solving process."""
    PENDING = "pending"
    UNPACKING = "unpacking"
    ANALYZING = "analyzing"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class SessionState:
    """State of a problem-solving session."""
    session_id: str
    problem: str
    domains: List[str]
    phase: ProcessPhase = ProcessPhase.PENDING
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # Results from each phase
    unpack_result: Optional[AgentResponse] = None
    analysis_results: List[AgentResponse] = field(default_factory=list)
    synthesis_result: Optional[AgentResponse] = None

    # Tracking
    error: Optional[str] = None
    execution_time: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "problem": self.problem,
            "domains": self.domains,
            "phase": self.phase.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "unpack_result": self.unpack_result.__dict__ if self.unpack_result else None,
            "analysis_results": [r.__dict__ for r in self.analysis_results],
            "synthesis_result": self.synthesis_result.__dict__ if self.synthesis_result else None,
            "error": self.error,
            "execution_time": self.execution_time
        }


class NovaProcess:
    """
    Main orchestrator for the Nova multi-agent problem-solving process.

    Usage:
        process = NovaProcess(llm_provider=get_llm("claude"))
        result = await process.solve(
            problem="How to scale our API?",
            domains=["technology", "security", "business"]
        )
    """

    def __init__(
        self,
        llm_provider: Optional[LLMProvider] = None,
        on_phase_change: Optional[Callable[[SessionState], None]] = None,
        on_agent_response: Optional[Callable[[AgentResponse], None]] = None
    ):
        """
        Initialize NovaProcess.

        Args:
            llm_provider: LLM provider for all agents (defaults to auto-detect)
            on_phase_change: Callback when phase changes (for streaming updates)
            on_agent_response: Callback when an agent responds (for streaming)
        """
        self.llm = llm_provider or get_llm("auto")
        self.on_phase_change = on_phase_change
        self.on_agent_response = on_agent_response

        # Core agents
        self.dce = DCEAgent(llm_provider=self.llm)
        self.cae = CAEAgent(llm_provider=self.llm)

    def _update_phase(self, state: SessionState, phase: ProcessPhase):
        """Update phase and trigger callback."""
        state.phase = phase
        state.updated_at = datetime.utcnow().isoformat()
        if self.on_phase_change:
            self.on_phase_change(state)

    def _agent_responded(self, response: AgentResponse):
        """Trigger agent response callback."""
        if self.on_agent_response:
            self.on_agent_response(response)

    async def solve(
        self,
        problem: str,
        domains: Optional[List[str]] = None
    ) -> SessionState:
        """
        Execute the full three-phase problem-solving process.

        Args:
            problem: The problem or question to solve
            domains: List of domain expertise to include (defaults to ["technology", "business"])

        Returns:
            SessionState with all results
        """
        # Initialize session
        session_id = str(uuid.uuid4())[:8]
        domains = domains or ["technology", "business"]

        state = SessionState(
            session_id=session_id,
            problem=problem,
            domains=domains
        )

        start_time = datetime.utcnow()

        try:
            # Phase 1: UNPACK
            self._update_phase(state, ProcessPhase.UNPACKING)
            state.unpack_result = await self.dce.process({
                "problem": problem,
                "phase": "unpack"
            })
            self._agent_responded(state.unpack_result)

            if not state.unpack_result.success:
                raise Exception(f"DCE unpack failed: {state.unpack_result.error}")

            # Phase 2: ANALYZE (parallel)
            self._update_phase(state, ProcessPhase.ANALYZING)

            # Create domain experts
            domain_experts = [
                create_domain_expert(domain, llm_provider=self.llm)
                for domain in domains
            ]

            # Prepare analysis input
            analysis_input = {
                "problem": problem,
                "dce_analysis": state.unpack_result.content
            }

            # Run all analysis agents in parallel
            analysis_tasks = [
                self.cae.process(analysis_input),
                *[expert.process(analysis_input) for expert in domain_experts]
            ]

            analysis_responses = await asyncio.gather(*analysis_tasks, return_exceptions=True)

            # Process results
            for response in analysis_responses:
                if isinstance(response, Exception):
                    # Log error but continue
                    error_response = AgentResponse(
                        agent_id="error",
                        agent_type="error",
                        agent_name="Error",
                        content="",
                        model="unknown",
                        success=False,
                        error=str(response)
                    )
                    state.analysis_results.append(error_response)
                else:
                    state.analysis_results.append(response)
                    self._agent_responded(response)

            # Phase 3: SYNTHESIZE
            self._update_phase(state, ProcessPhase.SYNTHESIZING)

            # Include successful analysis results in synthesis
            successful_analyses = [r for r in state.analysis_results if r.success]

            state.synthesis_result = await self.dce.process({
                "problem": problem,
                "phase": "synthesize",
                "agent_responses": successful_analyses
            })
            self._agent_responded(state.synthesis_result)

            # Complete
            self._update_phase(state, ProcessPhase.COMPLETED)

        except Exception as e:
            state.error = str(e)
            self._update_phase(state, ProcessPhase.ERROR)

        # Calculate execution time
        state.execution_time = (datetime.utcnow() - start_time).total_seconds()

        return state

    async def solve_streaming(
        self,
        problem: str,
        domains: Optional[List[str]] = None
    ):
        """
        Solve with async generator for streaming results.

        Yields:
            Dict with phase updates and agent responses
        """
        # Create a queue to collect events
        events = asyncio.Queue()

        original_phase_cb = self.on_phase_change
        original_agent_cb = self.on_agent_response

        def phase_callback(state: SessionState):
            events.put_nowait({
                "type": "phase_change",
                "phase": state.phase.value,
                "session_id": state.session_id
            })

        def agent_callback(response: AgentResponse):
            events.put_nowait({
                "type": "agent_response",
                "agent_name": response.agent_name,
                "agent_type": response.agent_type,
                "content": response.content,
                "model": response.model,
                "success": response.success
            })

        self.on_phase_change = phase_callback
        self.on_agent_response = agent_callback

        # Start solving in background
        solve_task = asyncio.create_task(self.solve(problem, domains))

        # Yield events as they come
        while not solve_task.done() or not events.empty():
            try:
                event = await asyncio.wait_for(events.get(), timeout=0.1)
                yield event
            except asyncio.TimeoutError:
                continue

        # Restore callbacks
        self.on_phase_change = original_phase_cb
        self.on_agent_response = original_agent_cb

        # Yield final result
        result = await solve_task
        yield {
            "type": "complete",
            "session": result.to_dict()
        }
