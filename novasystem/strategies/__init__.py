"""
Repository Strategies for NovaSystem.

Per-language installers that know how to:
- Detect repository type
- Generate appropriate base Docker image
- Provide pre/post install hooks
- Handle language-specific setup
"""

from .base import RepositoryStrategy, StrategyRegistry
from .python import PythonStrategy
from .node import NodeStrategy
from .rust import RustStrategy
from .go import GoStrategy

__all__ = [
    "RepositoryStrategy",
    "StrategyRegistry",
    "PythonStrategy",
    "NodeStrategy",
    "RustStrategy",
    "GoStrategy",
]
