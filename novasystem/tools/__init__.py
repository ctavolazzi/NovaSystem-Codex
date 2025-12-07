"""
NovaSystem Tools Module.

This module provides utility tools for repository management,
Docker execution, documentation parsing, and decision-making.

Merged from:
- novasystem v0.1.1 CLI tools
- Decision Matrix framework
"""

# Docker execution
from .docker import DockerExecutor, CommandResult

# Repository management
from .repository import RepositoryHandler

# Documentation parsing
from .parser import DocumentationParser, Command, CommandSource, CommandType

# Technical debt tracking
from .technical_debt import TechnicalDebtManager, TechnicalDebtItem, Severity, Status

# Nova orchestrator
from .nova import Nova

# Legacy database (for backwards compatibility)
from .legacy_database import DatabaseManager as LegacyDatabaseManager

# Decision Matrix subpackage
from .decision_matrix import (
    decision_matrix,
    decision_matrix_cli,
    DecisionMatrix,
    DecisionResult,
    make_decision,
    compare_methods,
    generate_doc_map,
)

__all__ = [
    # Docker
    "DockerExecutor",
    "CommandResult",
    # Repository
    "RepositoryHandler",
    # Parser
    "DocumentationParser",
    "Command",
    "CommandSource",
    "CommandType",
    # Technical Debt
    "TechnicalDebtManager",
    "TechnicalDebtItem",
    "Severity",
    "Status",
    # Nova
    "Nova",
    # Legacy
    "LegacyDatabaseManager",
    # Decision Matrix
    "decision_matrix",
    "decision_matrix_cli",
    "DecisionMatrix",
    "DecisionResult",
    "make_decision",
    "compare_methods",
    "generate_doc_map",
]
