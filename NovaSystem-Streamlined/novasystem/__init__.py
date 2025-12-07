"""
NovaSystem - Unified Multi-Agent Problem-Solving Framework

A streamlined implementation of the Nova Process that provides multiple interfaces
(CLI, Web, Gradio) for complex problem-solving using specialized AI agents.

Note: Components are lazy-loaded to prevent import-time overhead and logging spam.
Use explicit imports when needed:
    from novasystem.core.process import NovaProcess
    from novasystem.core.agents import DCEAgent, CAEAgent
"""

__version__ = "2.0.0"
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
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "NovaProcess",
    "DCEAgent",
    "CAEAgent",
    "DomainExpert",
    "create_app",
    "WebInterface",
    "GradioInterface",
]
