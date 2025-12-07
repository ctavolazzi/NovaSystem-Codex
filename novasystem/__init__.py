"""
NovaSystem - Unified Multi-Agent Problem-Solving Framework

A CLI-first implementation of the Nova Process that provides multiple interfaces
(CLI, API, Web, Gradio) for complex problem-solving using specialized AI agents.

This is the consolidated v0.3.0 release, merging:
- NovaSystem-Streamlined (v2.0) - Multi-agent framework
- novasystem CLI (v0.1.1) - Repository tools, Docker, Decision Matrix
- nova-mvp - LocalVectorStore, pricing, usage tracking

Note: Components are lazy-loaded to prevent import-time overhead and logging spam.
Use explicit imports when needed:
    from novasystem.core.process import NovaProcess
    from novasystem.core.agents import DCEAgent, CAEAgent
    from novasystem.tools import DecisionMatrix, DockerExecutor
"""

__version__ = "0.3.0"
__author__ = "NovaSystem Team"

# Lazy loading - only import when accessed
def __getattr__(name):
    """Lazy load components on first access."""
    if name == "NovaProcess":
        from .core.process import NovaProcess
        return NovaProcess
    elif name == "DCEAgent":
        from .core.agents import DCEAgent
        return DCEAgent
    elif name == "CAEAgent":
        from .core.agents import CAEAgent
        return CAEAgent
    elif name == "DomainExpert":
        from .core.agents import DomainExpert
        return DomainExpert
    elif name == "create_app":
        from .api.rest import create_app
        return create_app
    elif name == "WebInterface":
        from .ui.web import WebInterface
        return WebInterface
    elif name == "GradioInterface":
        from .ui.gradio import GradioInterface
        return GradioInterface
    # Tools
    elif name == "DecisionMatrix":
        from .tools.decision_matrix import DecisionMatrix
        return DecisionMatrix
    elif name == "DockerExecutor":
        from .tools.docker import DockerExecutor
        return DockerExecutor
    elif name == "RepositoryHandler":
        from .tools.repository import RepositoryHandler
        return RepositoryHandler
    elif name == "DocumentationParser":
        from .tools.parser import DocumentationParser
        return DocumentationParser
    elif name == "DatabaseManager":
        from .tools.legacy_database import DatabaseManager
        return DatabaseManager
    # Legacy alias
    elif name == "RepositoryManager":
        from .tools.repository import RepositoryHandler
        return RepositoryHandler
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # Core
    "NovaProcess",
    "DCEAgent",
    "CAEAgent",
    "DomainExpert",
    # API/UI
    "create_app",
    "WebInterface",
    "GradioInterface",
    # Tools
    "DecisionMatrix",
    "DockerExecutor",
    "RepositoryHandler",
    "DocumentationParser",
    "DatabaseManager",
]
