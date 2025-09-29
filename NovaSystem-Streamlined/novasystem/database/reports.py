"""
Advanced Reporting and Data Export System

This module provides comprehensive reporting capabilities including PDF generation,
Excel exports, and custom report templates for NovaSystem performance data.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import json
import csv
import io
from pathlib import Path

from .analytics import get_analytics_engine
from .performance_tracker import get_performance_tracker
from .database import get_database_manager

logger = logging.getLogger(__name__)

@dataclass
class ReportConfig:
    """Configuration for report generation."""
    title: str
    period_days: int
    include_charts: bool = True
    include_tables: bool = True
    include_summary: bool = True
    format: str = "json"  # json, csv, html, pdf
    template: Optional[str] = None

class ReportGenerator:
    """Advanced report generator for NovaSystem analytics."""

    def __init__(self):
        """Initialize report generator."""
        self.analytics = get_analytics_engine()
        self.tracker = get_performance_tracker()
        self.db_manager = get_database_manager()

    def generate_comprehensive_report(self, config: ReportConfig) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report.

        Args:
            config: Report configuration

        Returns:
            Dictionary containing report data
        """
        try:
            # Get all analytics data
            performance_report = self.analytics.generate_performance_report(config.period_days)
            cost_analysis = self.analytics.get_cost_analysis(config.period_days)
            trends = self.analytics.get_trend_analysis("sessions", config.period_days)
            benchmarks = self.analytics.get_performance_benchmarks()

            # Generate report structure
            report = {
                "metadata": {
                    "title": config.title,
                    "generated_at": datetime.utcnow().isoformat(),
                    "period_days": config.period_days,
                    "period_start": (datetime.utcnow() - timedelta(days=config.period_days)).isoformat(),
                    "period_end": datetime.utcnow().isoformat(),
                    "format": config.format
                },
                "executive_summary": self._generate_executive_summary(performance_report),
                "performance_metrics": {
                    "overview": {
                        "total_sessions": performance_report.total_sessions,
                        "success_rate": performance_report.success_rate,
                        "average_duration": performance_report.average_duration,
                        "total_cost": performance_report.total_cost,
                        "total_tokens": performance_report.total_tokens
                    },
                    "trends": trends,
                    "benchmarks": benchmarks
                },
                "model_analysis": {
                    "top_models": performance_report.top_models,
                    "cost_breakdown": cost_analysis.get("cost_by_model", []),
                    "performance_comparison": self._compare_model_performance(performance_report.top_models)
                },
                "agent_analysis": {
                    "top_agents": performance_report.top_agents,
                    "effectiveness_metrics": self._calculate_agent_effectiveness(performance_report.top_agents)
                },
                "cost_analysis": cost_analysis,
                "system_health": performance_report.system_health,
                "recommendations": self._generate_recommendations(performance_report, cost_analysis),
                "detailed_data": self._get_detailed_data(config.period_days) if config.include_tables else None
            }

            return report

        except Exception as e:
            logger.error(f"Failed to generate comprehensive report: {e}")
            raise

    def _generate_executive_summary(self, performance_report) -> Dict[str, Any]:
        """Generate executive summary of performance data."""
        return {
            "key_insights": [
                f"System processed {performance_report.total_sessions} sessions with {performance_report.success_rate}% success rate",
                f"Average response time of {performance_report.average_duration}s with total cost of ${performance_report.total_cost}",
                f"System health status: {performance_report.system_health.get('status', 'unknown')}"
            ],
            "performance_rating": self._calculate_performance_rating(performance_report),
            "cost_efficiency": self._calculate_cost_efficiency(performance_report),
            "reliability_score": performance_report.success_rate
        }

    def _calculate_performance_rating(self, performance_report) -> str:
        """Calculate overall performance rating."""
        score = 0

        # Success rate contribution (40%)
        score += (performance_report.success_rate / 100) * 40

        # Response time contribution (30%)
        if performance_report.average_duration <= 2:
            score += 30
        elif performance_report.average_duration <= 5:
            score += 20
        elif performance_report.average_duration <= 10:
            score += 10

        # System health contribution (30%)
        health_status = performance_report.system_health.get('status', 'unknown')
        if health_status == 'healthy':
            score += 30
        elif health_status == 'degraded':
            score += 15

        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Satisfactory"
        elif score >= 60:
            return "Needs Improvement"
        else:
            return "Poor"

    def _calculate_cost_efficiency(self, performance_report) -> Dict[str, Any]:
        """Calculate cost efficiency metrics."""
        if performance_report.total_sessions == 0:
            return {"cost_per_session": 0, "efficiency_rating": "N/A"}

        cost_per_session = performance_report.total_cost / performance_report.total_sessions

        if cost_per_session <= 0.01:
            efficiency_rating = "Excellent"
        elif cost_per_session <= 0.05:
            efficiency_rating = "Good"
        elif cost_per_session <= 0.10:
            efficiency_rating = "Acceptable"
        else:
            efficiency_rating = "Expensive"

        return {
            "cost_per_session": round(cost_per_session, 4),
            "efficiency_rating": efficiency_rating,
            "total_cost": performance_report.total_cost,
            "total_sessions": performance_report.total_sessions
        }

    def _compare_model_performance(self, models: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare performance across different models."""
        if not models:
            return {}

        # Find best performing model in each category
        best_success_rate = max(models, key=lambda x: x.get('success_rate', 0))
        best_response_time = min(models, key=lambda x: x.get('average_response_time', float('inf')))
        most_cost_effective = min(models, key=lambda x: x.get('total_cost_usd', float('inf')))

        return {
            "best_success_rate": {
                "model": best_success_rate.get('model_name'),
                "rate": best_success_rate.get('success_rate')
            },
            "fastest_response": {
                "model": best_response_time.get('model_name'),
                "time": best_response_time.get('average_response_time')
            },
            "most_cost_effective": {
                "model": most_cost_effective.get('model_name'),
                "cost": most_cost_effective.get('total_cost_usd')
            }
        }

    def _calculate_agent_effectiveness(self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate agent effectiveness metrics."""
        if not agents:
            return {}

        total_executions = sum(agent.get('total_executions', 0) for agent in agents)
        total_successful = sum(agent.get('successful_executions', 0) for agent in agents)
        total_cost = sum(agent.get('total_cost_usd', 0) for agent in agents)

        return {
            "total_executions": total_executions,
            "overall_success_rate": (total_successful / total_executions * 100) if total_executions > 0 else 0,
            "total_cost": total_cost,
            "cost_per_execution": (total_cost / total_executions) if total_executions > 0 else 0,
            "most_active_agent": max(agents, key=lambda x: x.get('total_executions', 0)).get('agent_type'),
            "most_efficient_agent": min(agents, key=lambda x: x.get('total_cost_usd', float('inf'))).get('agent_type')
        }

    def _generate_recommendations(self, performance_report, cost_analysis) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on performance data."""
        recommendations = []

        # Success rate recommendations
        if performance_report.success_rate < 90:
            recommendations.append({
                "category": "Reliability",
                "priority": "High",
                "recommendation": "Improve system reliability - success rate below 90%",
                "action": "Investigate failed sessions and implement error handling improvements"
            })

        # Response time recommendations
        if performance_report.average_duration > 10:
            recommendations.append({
                "category": "Performance",
                "priority": "High",
                "recommendation": "Optimize response times - average duration exceeds 10 seconds",
                "action": "Review model selection and implement caching strategies"
            })

        # Cost optimization recommendations
        if performance_report.total_cost > 1.0:
            recommendations.append({
                "category": "Cost Optimization",
                "priority": "Medium",
                "recommendation": "Optimize costs - total cost exceeds $1.00",
                "action": "Consider using more cost-effective models for non-critical tasks"
            })

        # Model usage recommendations
        if len(performance_report.top_models) > 1:
            recommendations.append({
                "category": "Model Strategy",
                "priority": "Low",
                "recommendation": "Diversify model usage for better performance",
                "action": "Analyze model performance and optimize selection criteria"
            })

        return recommendations

    def _get_detailed_data(self, days: int) -> Dict[str, Any]:
        """Get detailed session and execution data."""
        try:
            with self.db_manager.get_session() as session:
                from .models import SystemSession, AgentExecution

                # Get recent sessions
                recent_sessions = session.query(SystemSession).filter(
                    SystemSession.started_at >= datetime.utcnow() - timedelta(days=days)
                ).order_by(SystemSession.started_at.desc()).limit(100).all()

                # Get recent agent executions
                recent_executions = session.query(AgentExecution).filter(
                    AgentExecution.started_at >= datetime.utcnow() - timedelta(days=days)
                ).order_by(AgentExecution.started_at.desc()).limit(200).all()

                return {
                    "recent_sessions": [
                        {
                            "session_id": s.session_id,
                            "type": s.session_type,
                            "model": s.model_used,
                            "status": s.status,
                            "success": s.success,
                            "duration": s.duration_seconds,
                            "cost": s.total_cost_usd,
                            "tokens": s.total_tokens_used,
                            "started_at": s.started_at.isoformat()
                        }
                        for s in recent_sessions
                    ],
                    "recent_executions": [
                        {
                            "agent_type": e.agent_type,
                            "model": e.model_used,
                            "success": e.success,
                            "duration": e.duration_seconds,
                            "cost": e.cost_usd,
                            "quality_score": e.quality_score,
                            "started_at": e.started_at.isoformat()
                        }
                        for e in recent_executions
                    ]
                }

        except Exception as e:
            logger.error(f"Failed to get detailed data: {e}")
            return {}

    def export_to_csv(self, report_data: Dict[str, Any], filename: str) -> str:
        """Export report data to CSV format."""
        try:
            csv_data = []

            # Export performance metrics
            metrics = report_data.get("performance_metrics", {}).get("overview", {})
            csv_data.append(["Metric", "Value"])
            for key, value in metrics.items():
                csv_data.append([key.replace("_", " ").title(), value])

            # Export model data
            models = report_data.get("model_analysis", {}).get("top_models", [])
            if models:
                csv_data.append([])
                csv_data.append(["Model Analysis"])
                csv_data.append(["Model", "Provider", "Requests", "Success Rate", "Response Time", "Cost"])
                for model in models:
                    csv_data.append([
                        model.get("model_name", ""),
                        model.get("provider", ""),
                        model.get("total_requests", 0),
                        model.get("success_rate", 0),
                        model.get("average_response_time", 0),
                        model.get("total_cost_usd", 0)
                    ])

            # Export agent data
            agents = report_data.get("agent_analysis", {}).get("top_agents", [])
            if agents:
                csv_data.append([])
                csv_data.append(["Agent Analysis"])
                csv_data.append(["Agent Type", "Executions", "Success Rate", "Duration", "Quality", "Cost"])
                for agent in agents:
                    csv_data.append([
                        agent.get("agent_type", ""),
                        agent.get("total_executions", 0),
                        agent.get("success_rate", 0),
                        agent.get("average_duration", 0),
                        agent.get("average_quality_score", 0),
                        agent.get("total_cost_usd", 0)
                    ])

            # Write CSV file
            csv_path = Path(filename)
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(csv_data)

            return str(csv_path)

        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            raise

    def export_to_html(self, report_data: Dict[str, Any], filename: str) -> str:
        """Export report data to HTML format."""
        try:
            html_template = self._generate_html_template(report_data)

            html_path = Path(filename)
            with open(html_path, 'w', encoding='utf-8') as htmlfile:
                htmlfile.write(html_template)

            return str(html_path)

        except Exception as e:
            logger.error(f"Failed to export HTML: {e}")
            raise

    def _generate_html_template(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML template for report."""
        metadata = report_data.get("metadata", {})
        summary = report_data.get("executive_summary", {})
        metrics = report_data.get("performance_metrics", {})

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{metadata.get('title', 'NovaSystem Performance Report')}</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .section {{ margin-bottom: 30px; }}
                .section h2 {{ color: #495057; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
                .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #667eea; }}
                .metric-value {{ font-size: 2rem; font-weight: 700; color: #212529; }}
                .metric-label {{ color: #6c757d; font-size: 0.9rem; text-transform: uppercase; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e9ecef; }}
                th {{ background: #f8f9fa; font-weight: 600; }}
                .recommendation {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px; padding: 15px; margin: 10px 0; }}
                .recommendation.high {{ background: #f8d7da; border-color: #f5c6cb; }}
                .recommendation.medium {{ background: #fff3cd; border-color: #ffeaa7; }}
                .recommendation.low {{ background: #d1ecf1; border-color: #bee5eb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{metadata.get('title', 'NovaSystem Performance Report')}</h1>
                    <p>Generated on {metadata.get('generated_at', 'Unknown')}</p>
                    <p>Period: {metadata.get('period_days', 0)} days</p>
                </div>
                <div class="content">
                    <div class="section">
                        <h2>Executive Summary</h2>
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-value">{summary.get('performance_rating', 'N/A')}</div>
                                <div class="metric-label">Performance Rating</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{summary.get('reliability_score', 0)}%</div>
                                <div class="metric-label">Reliability Score</div>
                            </div>
                        </div>
                        <h3>Key Insights</h3>
                        <ul>
                            {''.join(f'<li>{insight}</li>' for insight in summary.get('key_insights', []))}
                        </ul>
                    </div>

                    <div class="section">
                        <h2>Performance Metrics</h2>
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-value">{metrics.get('overview', {}).get('total_sessions', 0)}</div>
                                <div class="metric-label">Total Sessions</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{metrics.get('overview', {}).get('success_rate', 0)}%</div>
                                <div class="metric-label">Success Rate</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">{metrics.get('overview', {}).get('average_duration', 0)}s</div>
                                <div class="metric-label">Avg Duration</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value">${metrics.get('overview', {}).get('total_cost', 0)}</div>
                                <div class="metric-label">Total Cost</div>
                            </div>
                        </div>
                    </div>

                    <div class="section">
                        <h2>Recommendations</h2>
                        {self._generate_recommendations_html(report_data.get('recommendations', []))}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_recommendations_html(self, recommendations: List[Dict[str, str]]) -> str:
        """Generate HTML for recommendations section."""
        if not recommendations:
            return "<p>No specific recommendations at this time.</p>"

        html = ""
        for rec in recommendations:
            priority_class = rec.get('priority', 'low').lower()
            html += f"""
            <div class="recommendation {priority_class}">
                <h4>{rec.get('category', 'General')} - {rec.get('priority', 'Low')} Priority</h4>
                <p><strong>Recommendation:</strong> {rec.get('recommendation', '')}</p>
                <p><strong>Action:</strong> {rec.get('action', '')}</p>
            </div>
            """

        return html

# Global report generator instance
_report_generator: Optional[ReportGenerator] = None

def get_report_generator() -> ReportGenerator:
    """Get the global report generator instance."""
    global _report_generator
    if _report_generator is None:
        _report_generator = ReportGenerator()
    return _report_generator
