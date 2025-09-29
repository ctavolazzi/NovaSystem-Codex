"""
Analytics and Reporting for NovaSystem Performance

This module provides comprehensive analytics, reporting, and visualization
capabilities for the NovaSystem performance database.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from sqlalchemy import func, and_, or_

from .database import get_database_manager
from .models import SystemSession, WorkflowExecution, AgentExecution, ModelUsage, SystemHealth
from .performance_tracker import get_performance_tracker

logger = logging.getLogger(__name__)

@dataclass
class PerformanceReport:
    """Container for performance report data."""
    period_start: datetime
    period_end: datetime
    total_sessions: int
    successful_sessions: int
    failed_sessions: int
    success_rate: float
    average_duration: float
    total_cost: float
    total_tokens: int
    top_models: List[Dict[str, Any]]
    top_agents: List[Dict[str, Any]]
    system_health: Dict[str, Any]

class AnalyticsEngine:
    """Advanced analytics engine for NovaSystem performance data."""

    def __init__(self):
        """Initialize analytics engine."""
        self.db_manager = get_database_manager()
        self.performance_tracker = get_performance_tracker()

    def generate_performance_report(self, days: int = 7) -> PerformanceReport:
        """
        Generate comprehensive performance report.

        Args:
            days: Number of days to analyze

        Returns:
            PerformanceReport object
        """
        try:
            with self.db_manager.get_session() as session:
                end_date = datetime.utcnow()
                start_date = end_date - timedelta(days=days)

                # Get session statistics
                session_stats = self._get_session_statistics(session, start_date, end_date)

                # Get model performance
                model_performance = self._get_model_performance(session, start_date, end_date)

                # Get agent performance
                agent_performance = self._get_agent_performance(session, start_date, end_date)

                # Get system health
                system_health = self._get_system_health_summary(session, start_date, end_date)

                return PerformanceReport(
                    period_start=start_date,
                    period_end=end_date,
                    total_sessions=session_stats["total_sessions"],
                    successful_sessions=session_stats["successful_sessions"],
                    failed_sessions=session_stats["failed_sessions"],
                    success_rate=session_stats["success_rate"],
                    average_duration=session_stats["average_duration"],
                    total_cost=session_stats["total_cost"],
                    total_tokens=session_stats["total_tokens"],
                    top_models=model_performance["top_models"],
                    top_agents=agent_performance["top_agents"],
                    system_health=system_health
                )

        except Exception as e:
            logger.error(f"Failed to generate performance report: {e}")
            raise

    def _get_session_statistics(self, session, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get session statistics for the period."""
        # Total sessions
        total_sessions = session.query(SystemSession).filter(
            and_(
                SystemSession.started_at >= start_date,
                SystemSession.started_at <= end_date
            )
        ).count()

        # Successful sessions
        successful_sessions = session.query(SystemSession).filter(
            and_(
                SystemSession.started_at >= start_date,
                SystemSession.started_at <= end_date,
                SystemSession.success == True
            )
        ).count()

        # Failed sessions
        failed_sessions = total_sessions - successful_sessions

        # Success rate
        success_rate = (successful_sessions / total_sessions * 100) if total_sessions > 0 else 0

        # Average duration
        avg_duration = session.query(SystemSession).filter(
            and_(
                SystemSession.started_at >= start_date,
                SystemSession.started_at <= end_date,
                SystemSession.duration_seconds.isnot(None)
            )
        ).with_entities(
            func.avg(SystemSession.duration_seconds)
        ).scalar() or 0

        # Total cost
        total_cost = session.query(SystemSession).filter(
            and_(
                SystemSession.started_at >= start_date,
                SystemSession.started_at <= end_date
            )
        ).with_entities(
            func.sum(SystemSession.total_cost_usd)
        ).scalar() or 0

        # Total tokens
        total_tokens = session.query(SystemSession).filter(
            and_(
                SystemSession.started_at >= start_date,
                SystemSession.started_at <= end_date
            )
        ).with_entities(
            func.sum(SystemSession.total_tokens_used)
        ).scalar() or 0

        return {
            "total_sessions": total_sessions,
            "successful_sessions": successful_sessions,
            "failed_sessions": failed_sessions,
            "success_rate": round(success_rate, 2),
            "average_duration": round(avg_duration, 2),
            "total_cost": round(total_cost, 4),
            "total_tokens": total_tokens
        }

    def _get_model_performance(self, session, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get model performance for the period."""
        # Get model usage statistics
        model_stats = session.query(
            ModelUsage.model_name,
            ModelUsage.provider,
            func.sum(ModelUsage.total_requests).label('total_requests'),
            func.sum(ModelUsage.total_tokens).label('total_tokens'),
            func.sum(ModelUsage.total_cost_usd).label('total_cost'),
            func.avg(ModelUsage.average_response_time).label('avg_response_time'),
            func.avg(ModelUsage.success_rate).label('success_rate')
        ).filter(
            ModelUsage.session_id.in_(
                session.query(SystemSession.session_id).filter(
                    and_(
                        SystemSession.started_at >= start_date,
                        SystemSession.started_at <= end_date
                    )
                )
            )
        ).group_by(
            ModelUsage.model_name, ModelUsage.provider
        ).order_by(
            func.sum(ModelUsage.total_requests).desc()
        ).limit(10).all()

        top_models = []
        for stat in model_stats:
            top_models.append({
                "model_name": stat.model_name,
                "provider": stat.provider,
                "total_requests": stat.total_requests,
                "total_tokens": stat.total_tokens,
                "total_cost_usd": round(stat.total_cost, 4),
                "average_response_time": round(stat.avg_response_time, 2),
                "success_rate": round(stat.success_rate, 2)
            })

        return {"top_models": top_models}

    def _get_agent_performance(self, session, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get agent performance for the period."""
        # Get agent execution statistics (simplified without case function)
        agent_stats = session.query(
            AgentExecution.agent_type,
            func.count(AgentExecution.id).label('total_executions'),
            func.avg(AgentExecution.duration_seconds).label('avg_duration'),
            func.avg(AgentExecution.quality_score).label('avg_quality'),
            func.avg(AgentExecution.relevance_score).label('avg_relevance'),
            func.sum(AgentExecution.cost_usd).label('total_cost')
        ).filter(
            and_(
                AgentExecution.started_at >= start_date,
                AgentExecution.started_at <= end_date
            )
        ).group_by(
            AgentExecution.agent_type
        ).order_by(
            func.count(AgentExecution.id).desc()
        ).limit(10).all()

        # Get successful executions separately
        successful_stats = session.query(
            AgentExecution.agent_type,
            func.count(AgentExecution.id).label('successful_executions')
        ).filter(
            and_(
                AgentExecution.started_at >= start_date,
                AgentExecution.started_at <= end_date,
                AgentExecution.success == True
            )
        ).group_by(
            AgentExecution.agent_type
        ).all()

        # Create lookup for successful executions
        successful_lookup = {stat.agent_type: stat.successful_executions for stat in successful_stats}

        top_agents = []
        for stat in agent_stats:
            successful_executions = successful_lookup.get(stat.agent_type, 0)
            success_rate = (successful_executions / stat.total_executions * 100) if stat.total_executions > 0 else 0
            top_agents.append({
                "agent_type": stat.agent_type,
                "total_executions": stat.total_executions,
                "successful_executions": successful_executions,
                "success_rate": round(success_rate, 2),
                "average_duration": round(stat.avg_duration, 2) if stat.avg_duration else None,
                "average_quality_score": round(stat.avg_quality, 2) if stat.avg_quality else None,
                "average_relevance_score": round(stat.avg_relevance, 2) if stat.avg_relevance else None,
                "total_cost_usd": round(stat.total_cost, 4) if stat.total_cost else 0
            })

        return {"top_agents": top_agents}

    def _get_system_health_summary(self, session, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get system health summary for the period."""
        # Get latest health record
        latest_health = session.query(SystemHealth).filter(
            SystemHealth.timestamp >= start_date
        ).order_by(SystemHealth.timestamp.desc()).first()

        if not latest_health:
            return {"status": "unknown", "last_updated": None}

        # Get health statistics for the period
        health_stats = session.query(
            func.avg(SystemHealth.cpu_usage_percent).label('avg_cpu'),
            func.avg(SystemHealth.memory_usage_percent).label('avg_memory'),
            func.avg(SystemHealth.disk_usage_percent).label('avg_disk'),
            func.avg(SystemHealth.average_response_time).label('avg_response_time'),
            func.avg(SystemHealth.error_rate_5min).label('avg_error_rate')
        ).filter(
            and_(
                SystemHealth.timestamp >= start_date,
                SystemHealth.timestamp <= end_date
            )
        ).first()

        return {
            "status": latest_health.system_status,
            "last_updated": latest_health.timestamp,
            "active_sessions": latest_health.active_sessions,
            "queued_sessions": latest_health.queued_sessions,
            "average_cpu_usage": round(health_stats.avg_cpu, 2) if health_stats.avg_cpu else None,
            "average_memory_usage": round(health_stats.avg_memory, 2) if health_stats.avg_memory else None,
            "average_disk_usage": round(health_stats.avg_disk, 2) if health_stats.avg_disk else None,
            "average_response_time": round(health_stats.avg_response_time, 2) if health_stats.avg_response_time else None,
            "average_error_rate": round(health_stats.avg_error_rate, 2) if health_stats.avg_error_rate else None,
            "api_status": {
                "openai": latest_health.openai_api_status,
                "anthropic": latest_health.anthropic_api_status,
                "ollama": latest_health.ollama_status
            }
        }

    def get_trend_analysis(self, metric: str, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get trend analysis for a specific metric.

        Args:
            metric: Metric to analyze ('sessions', 'cost', 'duration', 'tokens')
            days: Number of days to analyze

        Returns:
            List of daily trend data points
        """
        try:
            with self.db_manager.get_session() as session:
                end_date = datetime.utcnow()
                start_date = end_date - timedelta(days=days)

                # Generate daily data points
                trend_data = []
                current_date = start_date

                while current_date <= end_date:
                    next_date = current_date + timedelta(days=1)

                    if metric == "sessions":
                        count = session.query(SystemSession).filter(
                            and_(
                                SystemSession.started_at >= current_date,
                                SystemSession.started_at < next_date
                            )
                        ).count()
                    elif metric == "cost":
                        result = session.query(SystemSession).filter(
                            and_(
                                SystemSession.started_at >= current_date,
                                SystemSession.started_at < next_date
                            )
                        ).with_entities(
                            func.sum(SystemSession.total_cost_usd)
                        ).scalar()
                        count = result or 0
                    elif metric == "duration":
                        result = session.query(SystemSession).filter(
                            and_(
                                SystemSession.started_at >= current_date,
                                SystemSession.started_at < next_date,
                                SystemSession.duration_seconds.isnot(None)
                            )
                        ).with_entities(
                            func.avg(SystemSession.duration_seconds)
                        ).scalar()
                        count = result or 0
                    elif metric == "tokens":
                        result = session.query(SystemSession).filter(
                            and_(
                                SystemSession.started_at >= current_date,
                                SystemSession.started_at < next_date
                            )
                        ).with_entities(
                            func.sum(SystemSession.total_tokens_used)
                        ).scalar()
                        count = result or 0
                    else:
                        count = 0

                    trend_data.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "value": round(count, 2) if isinstance(count, float) else count
                    })

                    current_date = next_date

                return trend_data

        except Exception as e:
            logger.error(f"Failed to get trend analysis: {e}")
            return []

    def get_cost_analysis(self, days: int = 30) -> Dict[str, Any]:
        """
        Get detailed cost analysis.

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with cost analysis data
        """
        try:
            with self.db_manager.get_session() as session:
                end_date = datetime.utcnow()
                start_date = end_date - timedelta(days=days)

                # Total cost
                total_cost = session.query(SystemSession).filter(
                    and_(
                        SystemSession.started_at >= start_date,
                        SystemSession.started_at <= end_date
                    )
                ).with_entities(
                    func.sum(SystemSession.total_cost_usd)
                ).scalar() or 0

                # Cost by model
                cost_by_model = session.query(
                    SystemSession.model_used,
                    func.sum(SystemSession.total_cost_usd).label('total_cost'),
                    func.count(SystemSession.id).label('session_count')
                ).filter(
                    and_(
                        SystemSession.started_at >= start_date,
                        SystemSession.started_at <= end_date
                    )
                ).group_by(
                    SystemSession.model_used
                ).order_by(
                    func.sum(SystemSession.total_cost_usd).desc()
                ).all()

                # Cost by session type
                cost_by_type = session.query(
                    SystemSession.session_type,
                    func.sum(SystemSession.total_cost_usd).label('total_cost'),
                    func.count(SystemSession.id).label('session_count')
                ).filter(
                    and_(
                        SystemSession.started_at >= start_date,
                        SystemSession.started_at <= end_date
                    )
                ).group_by(
                    SystemSession.session_type
                ).order_by(
                    func.sum(SystemSession.total_cost_usd).desc()
                ).all()

                # Daily cost trend
                daily_costs = []
                current_date = start_date
                while current_date <= end_date:
                    next_date = current_date + timedelta(days=1)
                    daily_cost = session.query(SystemSession).filter(
                        and_(
                            SystemSession.started_at >= current_date,
                            SystemSession.started_at < next_date
                        )
                    ).with_entities(
                        func.sum(SystemSession.total_cost_usd)
                    ).scalar() or 0

                    daily_costs.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "cost": round(daily_cost, 4)
                    })

                    current_date = next_date

                return {
                    "total_cost_usd": round(total_cost, 4),
                    "average_daily_cost": round(total_cost / days, 4),
                    "cost_by_model": [
                        {
                            "model": row.model_used,
                            "total_cost": round(row.total_cost, 4),
                            "session_count": row.session_count,
                            "percentage": round(row.total_cost / total_cost * 100, 2) if total_cost > 0 else 0
                        }
                        for row in cost_by_model
                    ],
                    "cost_by_type": [
                        {
                            "type": row.session_type,
                            "total_cost": round(row.total_cost, 4),
                            "session_count": row.session_count,
                            "percentage": round(row.total_cost / total_cost * 100, 2) if total_cost > 0 else 0
                        }
                        for row in cost_by_type
                    ],
                    "daily_trend": daily_costs
                }

        except Exception as e:
            logger.error(f"Failed to get cost analysis: {e}")
            return {}

    def get_performance_benchmarks(self) -> Dict[str, Any]:
        """
        Get performance benchmarks and thresholds.

        Returns:
            Dictionary with performance benchmarks
        """
        return {
            "response_time_benchmarks": {
                "excellent": 2.0,  # seconds
                "good": 5.0,
                "acceptable": 10.0,
                "poor": 30.0
            },
            "success_rate_benchmarks": {
                "excellent": 95.0,  # percentage
                "good": 90.0,
                "acceptable": 80.0,
                "poor": 70.0
            },
            "cost_benchmarks": {
                "low": 0.01,  # USD per session
                "medium": 0.05,
                "high": 0.10,
                "very_high": 0.25
            },
            "quality_benchmarks": {
                "excellent": 0.9,  # 0-1 scale
                "good": 0.8,
                "acceptable": 0.7,
                "poor": 0.6
            }
        }

# Global analytics engine instance
_analytics_engine: Optional[AnalyticsEngine] = None

def get_analytics_engine() -> AnalyticsEngine:
    """Get the global analytics engine instance."""
    global _analytics_engine
    if _analytics_engine is None:
        _analytics_engine = AnalyticsEngine()
    return _analytics_engine
