"""
Database Models for NovaSystem Performance Tracking

This module defines SQLAlchemy models for tracking system performance,
model usage, agent effectiveness, and session analytics.
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, Boolean,
    ForeignKey, JSON, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Dict, Any, Optional
import json

Base = declarative_base()

class SystemSession(Base):
    """Tracks overall system sessions and their metadata."""

    __tablename__ = 'system_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    session_type = Column(String(50), nullable=False)  # 'workflow', 'single_agent', 'interactive'
    problem_statement = Column(Text)
    domains = Column(JSON)  # List of domains used
    model_used = Column(String(100), nullable=False)
    max_iterations = Column(Integer, default=5)

    # Timing
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime)
    duration_seconds = Column(Float)

    # Status and results
    status = Column(String(50), nullable=False)  # 'running', 'completed', 'failed', 'timeout'
    success = Column(Boolean, default=False)
    error_message = Column(Text)

    # Performance metrics
    total_tokens_used = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0.0)
    iterations_completed = Column(Integer, default=0)

    # Relationships
    workflow_executions = relationship("WorkflowExecution", back_populates="session")
    agent_executions = relationship("AgentExecution", back_populates="session")
    model_usages = relationship("ModelUsage", back_populates="session")

    # Indexes
    __table_args__ = (
        Index('idx_session_type_status', 'session_type', 'status'),
        Index('idx_session_started_at', 'started_at'),
        Index('idx_session_model', 'model_used'),
    )

class WorkflowExecution(Base):
    """Tracks individual workflow executions within a session."""

    __tablename__ = 'workflow_executions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), ForeignKey('system_sessions.session_id'), nullable=False)
    workflow_id = Column(String(255), nullable=False)

    # Workflow structure
    nodes = Column(JSON)  # List of workflow nodes
    connections = Column(JSON)  # List of connections between nodes
    execution_order = Column(JSON)  # Order of node execution

    # Timing
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime)
    duration_seconds = Column(Float)

    # Status
    status = Column(String(50), nullable=False)  # 'running', 'completed', 'failed'
    nodes_completed = Column(Integer, default=0)
    total_nodes = Column(Integer, default=0)

    # Results
    final_output = Column(Text)
    node_outputs = Column(JSON)  # Outputs from each node

    # Relationships
    session = relationship("SystemSession", back_populates="workflow_executions")

    # Indexes
    __table_args__ = (
        Index('idx_workflow_session', 'session_id'),
        Index('idx_workflow_status', 'status'),
    )

class AgentExecution(Base):
    """Tracks individual agent executions and their performance."""

    __tablename__ = 'agent_executions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), ForeignKey('system_sessions.session_id'), nullable=False)
    workflow_execution_id = Column(Integer, ForeignKey('workflow_executions.id'), nullable=True)

    # Agent identification
    agent_type = Column(String(50), nullable=False)  # 'dce', 'cae', 'domain_expert', etc.
    agent_name = Column(String(100), nullable=False)
    node_id = Column(String(100))  # For workflow agents

    # Input/Output
    input_text = Column(Text)
    output_text = Column(Text)
    context = Column(Text)

    # Model and performance
    model_used = Column(String(100), nullable=False)
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer)

    # Timing
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime)
    duration_seconds = Column(Float)

    # Metrics
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)

    # Quality metrics
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    quality_score = Column(Float)  # 0-1 quality rating
    relevance_score = Column(Float)  # 0-1 relevance rating

    # Relationships
    session = relationship("SystemSession", back_populates="agent_executions")
    workflow_execution = relationship("WorkflowExecution")

    # Indexes
    __table_args__ = (
        Index('idx_agent_type', 'agent_type'),
        Index('idx_agent_model', 'model_used'),
        Index('idx_agent_session', 'session_id'),
        Index('idx_agent_timing', 'started_at'),
    )

class ModelUsage(Base):
    """Tracks detailed model usage statistics and performance."""

    __tablename__ = 'model_usage'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), ForeignKey('system_sessions.session_id'), nullable=False)

    # Model identification
    model_name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)  # 'openai', 'anthropic', 'ollama'

    # Usage statistics
    total_requests = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)

    # Token usage
    total_input_tokens = Column(Integer, default=0)
    total_output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)

    # Cost tracking
    total_cost_usd = Column(Float, default=0.0)
    cost_per_token = Column(Float, default=0.0)

    # Performance metrics
    average_response_time = Column(Float, default=0.0)
    min_response_time = Column(Float)
    max_response_time = Column(Float)

    # Quality metrics
    average_quality_score = Column(Float)
    success_rate = Column(Float, default=0.0)

    # Relationships
    session = relationship("SystemSession", back_populates="model_usages")

    # Indexes
    __table_args__ = (
        Index('idx_model_name', 'model_name'),
        Index('idx_model_provider', 'provider'),
        Index('idx_model_session', 'session_id'),
    )

class PerformanceMetrics(Base):
    """Aggregated performance metrics for reporting and analysis."""

    __tablename__ = 'performance_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Time period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    period_type = Column(String(20), nullable=False)  # 'hourly', 'daily', 'weekly', 'monthly'

    # Aggregation scope
    scope_type = Column(String(50), nullable=False)  # 'system', 'model', 'agent', 'workflow'
    scope_identifier = Column(String(100))  # model name, agent type, etc.

    # System metrics
    total_sessions = Column(Integer, default=0)
    successful_sessions = Column(Integer, default=0)
    failed_sessions = Column(Integer, default=0)
    timeout_sessions = Column(Integer, default=0)

    # Performance metrics
    average_duration = Column(Float, default=0.0)
    min_duration = Column(Float)
    max_duration = Column(Float)

    # Cost metrics
    total_cost_usd = Column(Float, default=0.0)
    average_cost_per_session = Column(Float, default=0.0)

    # Token metrics
    total_tokens = Column(Integer, default=0)
    average_tokens_per_session = Column(Float, default=0.0)

    # Quality metrics
    average_quality_score = Column(Float)
    average_relevance_score = Column(Float)

    # Success rates
    success_rate = Column(Float, default=0.0)
    error_rate = Column(Float, default=0.0)

    # Indexes
    __table_args__ = (
        Index('idx_performance_period', 'period_start', 'period_end'),
        Index('idx_performance_scope', 'scope_type', 'scope_identifier'),
        Index('idx_performance_type', 'period_type'),
        UniqueConstraint('period_start', 'period_end', 'period_type', 'scope_type', 'scope_identifier'),
    )

class SystemHealth(Base):
    """Tracks system health and operational metrics."""

    __tablename__ = 'system_health'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    # System status
    system_status = Column(String(20), nullable=False)  # 'healthy', 'degraded', 'down'
    active_sessions = Column(Integer, default=0)
    queued_sessions = Column(Integer, default=0)

    # Resource usage
    cpu_usage_percent = Column(Float)
    memory_usage_percent = Column(Float)
    disk_usage_percent = Column(Float)

    # API status
    openai_api_status = Column(String(20))  # 'up', 'down', 'rate_limited'
    anthropic_api_status = Column(String(20))
    ollama_status = Column(String(20))

    # Performance indicators
    average_response_time = Column(Float)
    error_rate_5min = Column(Float)
    throughput_per_minute = Column(Float)

    # Indexes
    __table_args__ = (
        Index('idx_health_timestamp', 'timestamp'),
        Index('idx_health_status', 'system_status'),
    )

# Utility functions for JSON serialization
def serialize_json(obj: Any) -> str:
    """Serialize object to JSON string."""
    return json.dumps(obj, default=str)

def deserialize_json(json_str: str) -> Any:
    """Deserialize JSON string to object."""
    return json.loads(json_str) if json_str else None
