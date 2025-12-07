"""
NovaSystem Database Package

This package provides database functionality for tracking system performance,
model metrics, agent effectiveness, and session analytics.

Note: For backwards compatibility with v0.1.1, the legacy DatabaseManager
(SQLite-based) is exported. The new SQLAlchemy-based manager is available
as SQLAlchemyDatabaseManager.
"""

from .models import *
from .database import get_database, init_database
from .database import DatabaseManager as SQLAlchemyDatabaseManager
from .performance_tracker import PerformanceTracker, get_performance_tracker

# Legacy compatibility: import old DatabaseManager (tests expect this)
from ..tools.legacy_database import DatabaseManager

__all__ = [
    'get_database',
    'init_database',
    'DatabaseManager',  # Legacy SQLite-based (for backwards compat)
    'SQLAlchemyDatabaseManager',  # New SQLAlchemy-based
    'PerformanceTracker',
    'get_performance_tracker',
    'SystemSession',
    'WorkflowExecution',
    'AgentExecution',
    'ModelUsage',
    'PerformanceMetrics'
]
