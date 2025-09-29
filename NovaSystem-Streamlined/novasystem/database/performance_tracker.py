"""
Performance Tracking Service

This module provides comprehensive performance tracking for NovaSystem,
including session tracking, agent metrics, model usage, and system health.
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from contextlib import contextmanager
from dataclasses import dataclass

from .database import get_database_manager
from .models import (
    SystemSession, WorkflowExecution, AgentExecution,
    ModelUsage, PerformanceMetrics, SystemHealth
)

logger = logging.getLogger(__name__)

@dataclass
class SessionMetrics:
    """Container for session performance metrics."""
    session_id: str
    session_type: str
    problem_statement: str
    domains: List[str]
    model_used: str
    max_iterations: int
    started_at: datetime
    status: str = "running"
    success: bool = False
    error_message: Optional[str] = None
    total_tokens_used: int = 0
    total_cost_usd: float = 0.0
    iterations_completed: int = 0

@dataclass
class AgentMetrics:
    """Container for agent execution metrics."""
    session_id: str
    agent_type: str
    agent_name: str
    model_used: str
    input_text: str
    output_text: str
    context: Optional[str] = None
    node_id: Optional[str] = None
    workflow_execution_id: Optional[int] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    tokens_input: int = 0
    tokens_output: int = 0
    cost_usd: float = 0.0
    success: bool = True
    error_message: Optional[str] = None
    quality_score: Optional[float] = None
    relevance_score: Optional[float] = None

class PerformanceTracker:
    """Comprehensive performance tracking for NovaSystem."""

    def __init__(self):
        """Initialize performance tracker."""
        self.db_manager = get_database_manager()
        self._active_sessions: Dict[str, SessionMetrics] = {}
        self._active_agents: Dict[str, AgentMetrics] = {}

    # Session Management
    def start_session(self, session_metrics: SessionMetrics) -> str:
        """
        Start tracking a new session.

        Args:
            session_metrics: Session metrics to track

        Returns:
            Session ID
        """
        try:
            with self.db_manager.get_session() as session:
                # Create database record
                db_session = SystemSession(
                    session_id=session_metrics.session_id,
                    session_type=session_metrics.session_type,
                    problem_statement=session_metrics.problem_statement,
                    domains=session_metrics.domains,
                    model_used=session_metrics.model_used,
                    max_iterations=session_metrics.max_iterations,
                    started_at=session_metrics.started_at,
                    status=session_metrics.status
                )

                session.add(db_session)
                session.commit()

                # Store in memory for active tracking
                self._active_sessions[session_metrics.session_id] = session_metrics

                logger.info(f"Started tracking session: {session_metrics.session_id}")
                return session_metrics.session_id

        except Exception as e:
            logger.error(f"Failed to start session tracking: {e}")
            raise

    def complete_session(self, session_id: str, success: bool = True,
                        error_message: Optional[str] = None,
                        total_tokens: int = 0, total_cost: float = 0.0,
                        iterations_completed: int = 0) -> None:
        """
        Complete session tracking.

        Args:
            session_id: Session ID to complete
            success: Whether session was successful
            error_message: Error message if failed
            total_tokens: Total tokens used
            total_cost: Total cost in USD
            iterations_completed: Number of iterations completed
        """
        try:
            with self.db_manager.get_session() as session:
                # Update database record
                db_session = session.query(SystemSession).filter(
                    SystemSession.session_id == session_id
                ).first()

                if db_session:
                    db_session.completed_at = datetime.utcnow()
                    db_session.duration_seconds = (
                        db_session.completed_at - db_session.started_at
                    ).total_seconds()
                    db_session.status = "completed" if success else "failed"
                    db_session.success = success
                    db_session.error_message = error_message
                    db_session.total_tokens_used = total_tokens
                    db_session.total_cost_usd = total_cost
                    db_session.iterations_completed = iterations_completed

                    session.commit()

                    # Remove from active sessions
                    if session_id in self._active_sessions:
                        del self._active_sessions[session_id]

                    logger.info(f"Completed session tracking: {session_id}")
                else:
                    logger.warning(f"Session not found for completion: {session_id}")

        except Exception as e:
            logger.error(f"Failed to complete session tracking: {e}")
            raise

    # Workflow Tracking
    def start_workflow(self, session_id: str, workflow_id: str,
                      nodes: List[Dict], connections: List[Dict]) -> int:
        """
        Start tracking a workflow execution.

        Args:
            session_id: Parent session ID
            workflow_id: Workflow identifier
            nodes: List of workflow nodes
            connections: List of node connections

        Returns:
            Workflow execution ID
        """
        try:
            with self.db_manager.get_session() as session:
                workflow_exec = WorkflowExecution(
                    session_id=session_id,
                    workflow_id=workflow_id,
                    nodes=nodes,
                    connections=connections,
                    total_nodes=len(nodes),
                    started_at=datetime.utcnow(),
                    status="running"
                )

                session.add(workflow_exec)
                session.commit()

                logger.info(f"Started workflow tracking: {workflow_id}")
                return workflow_exec.id

        except Exception as e:
            logger.error(f"Failed to start workflow tracking: {e}")
            raise

    def complete_workflow(self, workflow_execution_id: int,
                         node_outputs: Dict[str, str],
                         final_output: str) -> None:
        """
        Complete workflow tracking.

        Args:
            workflow_execution_id: Workflow execution ID
            node_outputs: Outputs from each node
            final_output: Final workflow output
        """
        try:
            with self.db_manager.get_session() as session:
                workflow_exec = session.query(WorkflowExecution).filter(
                    WorkflowExecution.id == workflow_execution_id
                ).first()

                if workflow_exec:
                    workflow_exec.completed_at = datetime.utcnow()
                    workflow_exec.duration_seconds = (
                        workflow_exec.completed_at - workflow_exec.started_at
                    ).total_seconds()
                    workflow_exec.status = "completed"
                    workflow_exec.node_outputs = node_outputs
                    workflow_exec.final_output = final_output
                    workflow_exec.nodes_completed = len(node_outputs)

                    session.commit()

                    logger.info(f"Completed workflow tracking: {workflow_execution_id}")
                else:
                    logger.warning(f"Workflow execution not found: {workflow_execution_id}")

        except Exception as e:
            logger.error(f"Failed to complete workflow tracking: {e}")
            raise

    # Agent Tracking
    def start_agent_execution(self, agent_metrics: AgentMetrics) -> str:
        """
        Start tracking an agent execution.

        Args:
            agent_metrics: Agent execution metrics

        Returns:
            Agent execution ID
        """
        try:
            with self.db_manager.get_session() as session:
                agent_exec = AgentExecution(
                    session_id=agent_metrics.session_id,
                    workflow_execution_id=agent_metrics.workflow_execution_id,
                    agent_type=agent_metrics.agent_type,
                    agent_name=agent_metrics.agent_name,
                    node_id=agent_metrics.node_id,
                    input_text=agent_metrics.input_text,
                    context=agent_metrics.context,
                    model_used=agent_metrics.model_used,
                    temperature=agent_metrics.temperature,
                    max_tokens=agent_metrics.max_tokens,
                    started_at=datetime.utcnow()
                )

                session.add(agent_exec)
                session.commit()

                # Store in memory for active tracking
                execution_id = f"{agent_metrics.session_id}_{agent_metrics.agent_type}_{agent_exec.id}"
                self._active_agents[execution_id] = agent_metrics

                logger.debug(f"Started agent execution tracking: {agent_exec.id}")
                return str(agent_exec.id)

        except Exception as e:
            logger.error(f"Failed to start agent execution tracking: {e}")
            raise

    def complete_agent_execution(self, agent_execution_id: str,
                               output_text: str,
                               tokens_input: int = 0,
                               tokens_output: int = 0,
                               cost_usd: float = 0.0,
                               success: bool = True,
                               error_message: Optional[str] = None,
                               quality_score: Optional[float] = None,
                               relevance_score: Optional[float] = None) -> None:
        """
        Complete agent execution tracking.

        Args:
            agent_execution_id: Agent execution ID
            output_text: Agent output text
            tokens_input: Input tokens used
            tokens_output: Output tokens generated
            cost_usd: Cost in USD
            success: Whether execution was successful
            error_message: Error message if failed
            quality_score: Quality score (0-1)
            relevance_score: Relevance score (0-1)
        """
        try:
            with self.db_manager.get_session() as session:
                agent_exec = session.query(AgentExecution).filter(
                    AgentExecution.id == int(agent_execution_id)
                ).first()

                if agent_exec:
                    agent_exec.completed_at = datetime.utcnow()
                    agent_exec.duration_seconds = (
                        agent_exec.completed_at - agent_exec.started_at
                    ).total_seconds()
                    agent_exec.output_text = output_text
                    agent_exec.tokens_input = tokens_input
                    agent_exec.tokens_output = tokens_output
                    agent_exec.cost_usd = cost_usd
                    agent_exec.success = success
                    agent_exec.error_message = error_message
                    agent_exec.quality_score = quality_score
                    agent_exec.relevance_score = relevance_score

                    session.commit()

                    # Remove from active agents
                    for key, metrics in list(self._active_agents.items()):
                        if key.endswith(f"_{agent_execution_id}"):
                            del self._active_agents[key]
                            break

                    logger.debug(f"Completed agent execution tracking: {agent_execution_id}")
                else:
                    logger.warning(f"Agent execution not found: {agent_execution_id}")

        except Exception as e:
            logger.error(f"Failed to complete agent execution tracking: {e}")
            raise

    # Model Usage Tracking
    def track_model_usage(self, session_id: str, model_name: str,
                         provider: str, tokens_input: int, tokens_output: int,
                         cost_usd: float, response_time: float) -> None:
        """
        Track model usage statistics.

        Args:
            session_id: Session ID
            model_name: Model name
            provider: Model provider
            tokens_input: Input tokens
            tokens_output: Output tokens
            cost_usd: Cost in USD
            response_time: Response time in seconds
        """
        try:
            with self.db_manager.get_session() as session:
                # Find or create model usage record
                model_usage = session.query(ModelUsage).filter(
                    ModelUsage.session_id == session_id,
                    ModelUsage.model_name == model_name
                ).first()

                if not model_usage:
                    model_usage = ModelUsage(
                        session_id=session_id,
                        model_name=model_name,
                        provider=provider
                    )
                    session.add(model_usage)

                # Update statistics
                model_usage.total_requests = (model_usage.total_requests or 0) + 1
                model_usage.total_input_tokens = (model_usage.total_input_tokens or 0) + tokens_input
                model_usage.total_output_tokens = (model_usage.total_output_tokens or 0) + tokens_output
                model_usage.total_tokens = (model_usage.total_tokens or 0) + tokens_input + tokens_output
                model_usage.total_cost_usd = (model_usage.total_cost_usd or 0) + cost_usd

                # Update response time metrics
                if model_usage.average_response_time == 0 or model_usage.average_response_time is None:
                    model_usage.average_response_time = response_time
                    model_usage.min_response_time = response_time
                    model_usage.max_response_time = response_time
                else:
                    # Calculate running average
                    total_requests = model_usage.total_requests
                    model_usage.average_response_time = (
                        (model_usage.average_response_time * (total_requests - 1) + response_time)
                        / total_requests
                    )
                    model_usage.min_response_time = min(model_usage.min_response_time or response_time, response_time)
                    model_usage.max_response_time = max(model_usage.max_response_time or response_time, response_time)

                session.commit()

        except Exception as e:
            logger.error(f"Failed to track model usage: {e}")
            raise

    # System Health Tracking
    def record_system_health(self, system_status: str = "healthy",
                           active_sessions: int = 0,
                           queued_sessions: int = 0,
                           cpu_usage: Optional[float] = None,
                           memory_usage: Optional[float] = None,
                           disk_usage: Optional[float] = None,
                           openai_status: Optional[str] = None,
                           anthropic_status: Optional[str] = None,
                           ollama_status: Optional[str] = None,
                           average_response_time: Optional[float] = None,
                           error_rate_5min: Optional[float] = None,
                           throughput_per_minute: Optional[float] = None) -> None:
        """
        Record system health metrics.

        Args:
            system_status: Overall system status
            active_sessions: Number of active sessions
            queued_sessions: Number of queued sessions
            cpu_usage: CPU usage percentage
            memory_usage: Memory usage percentage
            disk_usage: Disk usage percentage
            openai_status: OpenAI API status
            anthropic_status: Anthropic API status
            ollama_status: Ollama status
            average_response_time: Average response time
            error_rate_5min: Error rate over 5 minutes
            throughput_per_minute: Throughput per minute
        """
        try:
            with self.db_manager.get_session() as session:
                health_record = SystemHealth(
                    system_status=system_status,
                    active_sessions=active_sessions,
                    queued_sessions=queued_sessions,
                    cpu_usage_percent=cpu_usage,
                    memory_usage_percent=memory_usage,
                    disk_usage_percent=disk_usage,
                    openai_api_status=openai_status,
                    anthropic_api_status=anthropic_status,
                    ollama_status=ollama_status,
                    average_response_time=average_response_time,
                    error_rate_5min=error_rate_5min,
                    throughput_per_minute=throughput_per_minute
                )

                session.add(health_record)
                session.commit()

        except Exception as e:
            logger.error(f"Failed to record system health: {e}")
            raise

    # Analytics and Reporting
    def get_session_analytics(self, days: int = 7) -> Dict[str, Any]:
        """
        Get session analytics for the specified period.

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with session analytics
        """
        try:
            with self.db_manager.get_session() as session:
                start_date = datetime.utcnow() - timedelta(days=days)

                # Query session statistics
                total_sessions = session.query(SystemSession).filter(
                    SystemSession.started_at >= start_date
                ).count()

                successful_sessions = session.query(SystemSession).filter(
                    SystemSession.started_at >= start_date,
                    SystemSession.success == True
                ).count()

                failed_sessions = session.query(SystemSession).filter(
                    SystemSession.started_at >= start_date,
                    SystemSession.success == False
                ).count()

                # Calculate success rate
                success_rate = (successful_sessions / total_sessions * 100) if total_sessions > 0 else 0

                # Get average duration
                avg_duration = session.query(SystemSession).filter(
                    SystemSession.started_at >= start_date,
                    SystemSession.duration_seconds.isnot(None)
                ).with_entities(
                    session.func.avg(SystemSession.duration_seconds)
                ).scalar() or 0

                # Get total cost
                total_cost = session.query(SystemSession).filter(
                    SystemSession.started_at >= start_date
                ).with_entities(
                    session.func.sum(SystemSession.total_cost_usd)
                ).scalar() or 0

                return {
                    "period_days": days,
                    "total_sessions": total_sessions,
                    "successful_sessions": successful_sessions,
                    "failed_sessions": failed_sessions,
                    "success_rate": round(success_rate, 2),
                    "average_duration_seconds": round(avg_duration, 2),
                    "total_cost_usd": round(total_cost, 4)
                }

        except Exception as e:
            logger.error(f"Failed to get session analytics: {e}")
            return {}

    def get_model_performance(self, model_name: Optional[str] = None,
                            days: int = 7) -> Dict[str, Any]:
        """
        Get model performance analytics.

        Args:
            model_name: Specific model to analyze (None for all models)
            days: Number of days to analyze

        Returns:
            Dictionary with model performance data
        """
        try:
            with self.db_manager.get_session() as session:
                start_date = datetime.utcnow() - timedelta(days=days)

                query = session.query(ModelUsage).filter(
                    ModelUsage.session_id.in_(
                        session.query(SystemSession.session_id).filter(
                            SystemSession.started_at >= start_date
                        )
                    )
                )

                if model_name:
                    query = query.filter(ModelUsage.model_name == model_name)

                model_usages = query.all()

                if not model_usages:
                    return {"models": [], "summary": {}}

                # Aggregate data by model
                model_data = {}
                for usage in model_usages:
                    if usage.model_name not in model_data:
                        model_data[usage.model_name] = {
                            "model_name": usage.model_name,
                            "provider": usage.provider,
                            "total_requests": 0,
                            "total_tokens": 0,
                            "total_cost_usd": 0,
                            "average_response_time": 0,
                            "success_rate": 0
                        }

                    data = model_data[usage.model_name]
                    data["total_requests"] += usage.total_requests
                    data["total_tokens"] += usage.total_tokens
                    data["total_cost_usd"] += usage.total_cost_usd
                    data["average_response_time"] = max(
                        data["average_response_time"],
                        usage.average_response_time
                    )

                # Calculate summary statistics
                total_requests = sum(data["total_requests"] for data in model_data.values())
                total_cost = sum(data["total_cost_usd"] for data in model_data.values())

                return {
                    "models": list(model_data.values()),
                    "summary": {
                        "total_models": len(model_data),
                        "total_requests": total_requests,
                        "total_cost_usd": round(total_cost, 4)
                    }
                }

        except Exception as e:
            logger.error(f"Failed to get model performance: {e}")
            return {"models": [], "summary": {}}

    def get_agent_effectiveness(self, agent_type: Optional[str] = None,
                              days: int = 7) -> Dict[str, Any]:
        """
        Get agent effectiveness analytics.

        Args:
            agent_type: Specific agent type to analyze (None for all agents)
            days: Number of days to analyze

        Returns:
            Dictionary with agent effectiveness data
        """
        try:
            with self.db_manager.get_session() as session:
                start_date = datetime.utcnow() - timedelta(days=days)

                query = session.query(AgentExecution).filter(
                    AgentExecution.started_at >= start_date
                )

                if agent_type:
                    query = query.filter(AgentExecution.agent_type == agent_type)

                agent_executions = query.all()

                if not agent_executions:
                    return {"agents": [], "summary": {}}

                # Aggregate data by agent type
                agent_data = {}
                for execution in agent_executions:
                    if execution.agent_type not in agent_data:
                        agent_data[execution.agent_type] = {
                            "agent_type": execution.agent_type,
                            "total_executions": 0,
                            "successful_executions": 0,
                            "total_duration": 0,
                            "average_quality_score": 0,
                            "average_relevance_score": 0,
                            "total_cost_usd": 0
                        }

                    data = agent_data[execution.agent_type]
                    data["total_executions"] += 1
                    if execution.success:
                        data["successful_executions"] += 1
                    if execution.duration_seconds:
                        data["total_duration"] += execution.duration_seconds
                    if execution.quality_score:
                        data["average_quality_score"] = max(
                            data["average_quality_score"],
                            execution.quality_score
                        )
                    if execution.relevance_score:
                        data["average_relevance_score"] = max(
                            data["average_relevance_score"],
                            execution.relevance_score
                        )
                    data["total_cost_usd"] += execution.cost_usd

                # Calculate success rates and averages
                for data in agent_data.values():
                    if data["total_executions"] > 0:
                        data["success_rate"] = round(
                            data["successful_executions"] / data["total_executions"] * 100, 2
                        )
                        data["average_duration"] = round(
                            data["total_duration"] / data["total_executions"], 2
                        )

                return {
                    "agents": list(agent_data.values()),
                    "summary": {
                        "total_agent_types": len(agent_data),
                        "total_executions": sum(data["total_executions"] for data in agent_data.values())
                    }
                }

        except Exception as e:
            logger.error(f"Failed to get agent effectiveness: {e}")
            return {"agents": [], "summary": {}}

# Global performance tracker instance
_performance_tracker: Optional[PerformanceTracker] = None

def get_performance_tracker() -> PerformanceTracker:
    """Get the global performance tracker instance."""
    global _performance_tracker
    if _performance_tracker is None:
        _performance_tracker = PerformanceTracker()
    return _performance_tracker
