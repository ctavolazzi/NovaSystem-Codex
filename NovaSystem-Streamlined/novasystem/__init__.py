"""
NovaSystem - Unified Multi-Agent Problem-Solving Framework

A streamlined implementation of the Nova Process that provides multiple interfaces
(CLI, Web, Gradio) for complex problem-solving using specialized AI agents.
"""

__version__ = "2.0.0"
__author__ = "NovaSystem Team"

from .core.process import NovaProcess
from .core.agents import DCEAgent, CAEAgent, DomainExpert
from .api.rest import create_app
from .ui.web import WebInterface
from .ui.gradio import GradioInterface

__all__ = [
    "NovaProcess",
    "DCEAgent",
    "CAEAgent",
    "DomainExpert",
    "create_app",
    "WebInterface",
    "GradioInterface",
]
