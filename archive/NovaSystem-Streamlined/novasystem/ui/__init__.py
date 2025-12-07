"""
User Interface layer for NovaSystem.

This module provides multiple UI options for interacting with the Nova Process:
- Web interface (Flask-based)
- Gradio interface (simple web form)
- CLI interface
"""

from .web import WebInterface
from .gradio import GradioInterface

__all__ = [
    "WebInterface",
    "GradioInterface",
]
