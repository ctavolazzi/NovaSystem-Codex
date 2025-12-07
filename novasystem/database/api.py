"""
Database API Endpoints

This module provides REST API endpoints for accessing NovaSystem performance
data, analytics, and reporting functionality.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from flask import Blueprint, jsonify, request
from functools import wraps

from .analytics import get_analytics_engine
from .performance_tracker import get_performance_tracker
from .database import get_database_manager
from .reports import get_report_generator, ReportConfig

logger = logging.getLogger(__name__)

# Create Blueprint for database API
db_api = Blueprint('db_api', __name__, url_prefix='/api/database')

def require_auth(f):
    """Decorator to require authentication for database endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Add authentication logic here if needed
        # For now, allow all requests
        return f(*args, **kwargs)
    return decorated_function

@db_api.route('/health', methods=['GET'])
@require_auth
def health_check():
    """Check database connectivity and health."""
    try:
        db_manager = get_database_manager()
        is_healthy = db_manager.health_check()

        return jsonify({
            "status": "healthy" if is_healthy else "unhealthy",
            "database_url": db_manager.database_url,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@db_api.route('/analytics/performance-report', methods=['GET'])
@require_auth
def get_performance_report():
    """Get comprehensive performance report."""
    try:
        days = request.args.get('days', 7, type=int)
        analytics = get_analytics_engine()
        report = analytics.generate_performance_report(days)

        return jsonify({
            "period_start": report.period_start.isoformat(),
            "period_end": report.period_end.isoformat(),
            "total_sessions": report.total_sessions,
            "successful_sessions": report.successful_sessions,
            "failed_sessions": report.failed_sessions,
            "success_rate": report.success_rate,
            "average_duration": report.average_duration,
            "total_cost": report.total_cost,
            "total_tokens": report.total_tokens,
            "top_models": report.top_models,
            "top_agents": report.top_agents,
            "system_health": report.system_health
        })
    except Exception as e:
        logger.error(f"Failed to get performance report: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/analytics/sessions', methods=['GET'])
@require_auth
def get_session_analytics():
    """Get session analytics."""
    try:
        days = request.args.get('days', 7, type=int)
        tracker = get_performance_tracker()
        analytics = tracker.get_session_analytics(days)

        return jsonify(analytics)
    except Exception as e:
        logger.error(f"Failed to get session analytics: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/analytics/models', methods=['GET'])
@require_auth
def get_model_analytics():
    """Get model performance analytics."""
    try:
        days = request.args.get('days', 7, type=int)
        model_name = request.args.get('model')
        tracker = get_performance_tracker()
        analytics = tracker.get_model_performance(model_name, days)

        return jsonify(analytics)
    except Exception as e:
        logger.error(f"Failed to get model analytics: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/analytics/agents', methods=['GET'])
@require_auth
def get_agent_analytics():
    """Get agent effectiveness analytics."""
    try:
        days = request.args.get('days', 7, type=int)
        agent_type = request.args.get('agent_type')
        tracker = get_performance_tracker()
        analytics = tracker.get_agent_effectiveness(agent_type, days)

        return jsonify(analytics)
    except Exception as e:
        logger.error(f"Failed to get agent analytics: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/analytics/trends', methods=['GET'])
@require_auth
def get_trend_analysis():
    """Get trend analysis for specific metrics."""
    try:
        metric = request.args.get('metric', 'sessions')
        days = request.args.get('days', 30, type=int)

        if metric not in ['sessions', 'cost', 'duration', 'tokens']:
            return jsonify({"error": "Invalid metric. Must be one of: sessions, cost, duration, tokens"}), 400

        analytics = get_analytics_engine()
        trends = analytics.get_trend_analysis(metric, days)

        return jsonify({
            "metric": metric,
            "period_days": days,
            "trend_data": trends
        })
    except Exception as e:
        logger.error(f"Failed to get trend analysis: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/analytics/cost', methods=['GET'])
@require_auth
def get_cost_analysis():
    """Get detailed cost analysis."""
    try:
        days = request.args.get('days', 30, type=int)
        analytics = get_analytics_engine()
        cost_analysis = analytics.get_cost_analysis(days)

        return jsonify(cost_analysis)
    except Exception as e:
        logger.error(f"Failed to get cost analysis: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/analytics/benchmarks', methods=['GET'])
@require_auth
def get_performance_benchmarks():
    """Get performance benchmarks and thresholds."""
    try:
        analytics = get_analytics_engine()
        benchmarks = analytics.get_performance_benchmarks()

        return jsonify(benchmarks)
    except Exception as e:
        logger.error(f"Failed to get performance benchmarks: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/sessions', methods=['GET'])
@require_auth
def get_sessions():
    """Get list of sessions with optional filtering."""
    try:
        with get_database_manager().get_session() as session:
            from .models import SystemSession

            # Get query parameters
            limit = request.args.get('limit', 100, type=int)
            offset = request.args.get('offset', 0, type=int)
            status = request.args.get('status')
            session_type = request.args.get('type')
            model = request.args.get('model')
            days = request.args.get('days', 7, type=int)

            # Build query
            query = session.query(SystemSession)

            # Apply filters
            if days:
                start_date = datetime.utcnow() - timedelta(days=days)
                query = query.filter(SystemSession.started_at >= start_date)

            if status:
                query = query.filter(SystemSession.status == status)

            if session_type:
                query = query.filter(SystemSession.session_type == session_type)

            if model:
                query = query.filter(SystemSession.model_used == model)

            # Apply pagination
            total_count = query.count()
            sessions = query.order_by(SystemSession.started_at.desc()).offset(offset).limit(limit).all()

            # Serialize results
            session_data = []
            for s in sessions:
                session_data.append({
                    "session_id": s.session_id,
                    "session_type": s.session_type,
                    "problem_statement": s.problem_statement[:200] + "..." if s.problem_statement and len(s.problem_statement) > 200 else s.problem_statement,
                    "domains": s.domains,
                    "model_used": s.model_used,
                    "max_iterations": s.max_iterations,
                    "started_at": s.started_at.isoformat(),
                    "completed_at": s.completed_at.isoformat() if s.completed_at else None,
                    "duration_seconds": s.duration_seconds,
                    "status": s.status,
                    "success": s.success,
                    "error_message": s.error_message,
                    "total_tokens_used": s.total_tokens_used,
                    "total_cost_usd": s.total_cost_usd,
                    "iterations_completed": s.iterations_completed
                })

            return jsonify({
                "sessions": session_data,
                "total_count": total_count,
                "limit": limit,
                "offset": offset
            })

    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/sessions/<session_id>', methods=['GET'])
@require_auth
def get_session_details(session_id: str):
    """Get detailed information about a specific session."""
    try:
        with get_database_manager().get_session() as session:
            from .models import SystemSession, WorkflowExecution, AgentExecution

            # Get session
            system_session = session.query(SystemSession).filter(
                SystemSession.session_id == session_id
            ).first()

            if not system_session:
                return jsonify({"error": "Session not found"}), 404

            # Get workflow executions
            workflow_executions = session.query(WorkflowExecution).filter(
                WorkflowExecution.session_id == session_id
            ).all()

            # Get agent executions
            agent_executions = session.query(AgentExecution).filter(
                AgentExecution.session_id == session_id
            ).all()

            # Serialize data
            session_data = {
                "session_id": system_session.session_id,
                "session_type": system_session.session_type,
                "problem_statement": system_session.problem_statement,
                "domains": system_session.domains,
                "model_used": system_session.model_used,
                "max_iterations": system_session.max_iterations,
                "started_at": system_session.started_at.isoformat(),
                "completed_at": system_session.completed_at.isoformat() if system_session.completed_at else None,
                "duration_seconds": system_session.duration_seconds,
                "status": system_session.status,
                "success": system_session.success,
                "error_message": system_session.error_message,
                "total_tokens_used": system_session.total_tokens_used,
                "total_cost_usd": system_session.total_cost_usd,
                "iterations_completed": system_session.iterations_completed,
                "workflow_executions": [
                    {
                        "id": we.id,
                        "workflow_id": we.workflow_id,
                        "nodes": we.nodes,
                        "connections": we.connections,
                        "execution_order": we.execution_order,
                        "started_at": we.started_at.isoformat(),
                        "completed_at": we.completed_at.isoformat() if we.completed_at else None,
                        "duration_seconds": we.duration_seconds,
                        "status": we.status,
                        "nodes_completed": we.nodes_completed,
                        "total_nodes": we.total_nodes,
                        "final_output": we.final_output,
                        "node_outputs": we.node_outputs
                    }
                    for we in workflow_executions
                ],
                "agent_executions": [
                    {
                        "id": ae.id,
                        "agent_type": ae.agent_type,
                        "agent_name": ae.agent_name,
                        "node_id": ae.node_id,
                        "workflow_execution_id": ae.workflow_execution_id,
                        "input_text": ae.input_text,
                        "output_text": ae.output_text,
                        "context": ae.context,
                        "model_used": ae.model_used,
                        "temperature": ae.temperature,
                        "max_tokens": ae.max_tokens,
                        "started_at": ae.started_at.isoformat(),
                        "completed_at": ae.completed_at.isoformat() if ae.completed_at else None,
                        "duration_seconds": ae.duration_seconds,
                        "tokens_input": ae.tokens_input,
                        "tokens_output": ae.tokens_output,
                        "cost_usd": ae.cost_usd,
                        "success": ae.success,
                        "error_message": ae.error_message,
                        "quality_score": ae.quality_score,
                        "relevance_score": ae.relevance_score
                    }
                    for ae in agent_executions
                ]
            }

            return jsonify(session_data)

    except Exception as e:
        logger.error(f"Failed to get session details: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/models', methods=['GET'])
@require_auth
def get_models():
    """Get list of models with usage statistics."""
    try:
        with get_database_manager().get_session() as session:
            from .models import ModelUsage

            days = request.args.get('days', 30, type=int)
            start_date = datetime.utcnow() - timedelta(days=days)

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
                        SystemSession.started_at >= start_date
                    )
                )
            ).group_by(
                ModelUsage.model_name, ModelUsage.provider
            ).order_by(
                func.sum(ModelUsage.total_requests).desc()
            ).all()

            models_data = []
            for stat in model_stats:
                models_data.append({
                    "model_name": stat.model_name,
                    "provider": stat.provider,
                    "total_requests": stat.total_requests,
                    "total_tokens": stat.total_tokens,
                    "total_cost_usd": round(stat.total_cost, 4),
                    "average_response_time": round(stat.avg_response_time, 2),
                    "success_rate": round(stat.success_rate, 2)
                })

            return jsonify({"models": models_data})

    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/export', methods=['GET'])
@require_auth
def export_data():
    """Export performance data in various formats."""
    try:
        format_type = request.args.get('format', 'json')
        days = request.args.get('days', 30, type=int)

        if format_type not in ['json', 'csv']:
            return jsonify({"error": "Invalid format. Must be 'json' or 'csv'"}), 400

        # Get performance report
        analytics = get_analytics_engine()
        report = analytics.generate_performance_report(days)

        if format_type == 'json':
            return jsonify({
                "export_type": "performance_report",
                "period_days": days,
                "exported_at": datetime.utcnow().isoformat(),
                "data": {
                    "period_start": report.period_start.isoformat(),
                    "period_end": report.period_end.isoformat(),
                    "total_sessions": report.total_sessions,
                    "successful_sessions": report.successful_sessions,
                    "failed_sessions": report.failed_sessions,
                    "success_rate": report.success_rate,
                    "average_duration": report.average_duration,
                    "total_cost": report.total_cost,
                    "total_tokens": report.total_tokens,
                    "top_models": report.top_models,
                    "top_agents": report.top_agents,
                    "system_health": report.system_health
                }
            })
        else:
            # CSV export would be implemented here
            return jsonify({"error": "CSV export not yet implemented"}), 501

    except Exception as e:
        logger.error(f"Failed to export data: {e}")
        return jsonify({"error": str(e)}), 500

# Error handlers
@db_api.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@db_api.route('/reports/generate', methods=['POST'])
@require_auth
def generate_report():
    """Generate comprehensive performance report."""
    try:
        data = request.get_json() or {}

        config = ReportConfig(
            title=data.get('title', 'NovaSystem Performance Report'),
            period_days=data.get('days', 7),
            include_charts=data.get('include_charts', True),
            include_tables=data.get('include_tables', True),
            include_summary=data.get('include_summary', True),
            format=data.get('format', 'json')
        )

        report_generator = get_report_generator()
        report_data = report_generator.generate_comprehensive_report(config)

        return jsonify({
            "status": "success",
            "report": report_data,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to generate report: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.route('/reports/export', methods=['POST'])
@require_auth
def export_report():
    """Export report in various formats."""
    try:
        data = request.get_json() or {}

        config = ReportConfig(
            title=data.get('title', 'NovaSystem Performance Report'),
            period_days=data.get('days', 7),
            format=data.get('format', 'json')
        )

        report_generator = get_report_generator()
        report_data = report_generator.generate_comprehensive_report(config)

        # Generate filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"novasystem_report_{timestamp}.{config.format}"

        if config.format == 'csv':
            file_path = report_generator.export_to_csv(report_data, filename)
        elif config.format == 'html':
            file_path = report_generator.export_to_html(report_data, filename)
        else:
            # JSON export
            import json
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2)
            file_path = filename

        return jsonify({
            "status": "success",
            "file_path": file_path,
            "format": config.format,
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to export report: {e}")
        return jsonify({"error": str(e)}), 500

@db_api.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@db_api.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
