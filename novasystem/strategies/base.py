"""
Repository Strategy Interface.

Defines the contract for language-specific repository handlers.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Type

logger = logging.getLogger(__name__)


@dataclass
class StrategyResult:
    """Result of strategy detection."""
    detected: bool
    strategy_name: str
    confidence: float = 1.0
    detected_files: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class RepositoryStrategy(ABC):
    """
    Base class for repository strategies.

    Each strategy knows how to handle a specific type of repository
    (Python, Node.js, Rust, Go, etc.).

    Responsibilities:
    - Detect if a repository matches this strategy
    - Provide the appropriate Docker base image
    - Generate pre-install commands (setup)
    - Generate post-install commands (verification)
    - Provide language-specific hints
    """

    name: str = "base"
    priority: int = 50  # Higher = checked first

    @abstractmethod
    def detect(self, repo_path: str) -> StrategyResult:
        """
        Detect if this strategy applies to the repository.

        Args:
            repo_path: Path to the repository

        Returns:
            StrategyResult with detection info
        """
        pass

    @abstractmethod
    def get_base_image(self) -> str:
        """
        Get the Docker base image for this strategy.

        Returns:
            Docker image name (e.g., "python:3.11-slim")
        """
        pass

    def get_pre_install_commands(self, repo_path: str) -> List[str]:
        """
        Get commands to run before installation.

        Args:
            repo_path: Path to the repository

        Returns:
            List of shell commands
        """
        return []

    def get_post_install_commands(self, repo_path: str) -> List[str]:
        """
        Get commands to run after installation.

        Args:
            repo_path: Path to the repository

        Returns:
            List of shell commands
        """
        return []

    def get_install_command(self, repo_path: str) -> Optional[str]:
        """
        Get the primary install command for this strategy.

        Args:
            repo_path: Path to the repository

        Returns:
            Install command or None to use detected commands
        """
        return None

    def get_env_vars(self) -> Dict[str, str]:
        """
        Get environment variables to set in the container.

        Returns:
            Dict of env var name to value
        """
        return {}

    def get_working_directory(self) -> str:
        """
        Get the working directory in the container.

        Returns:
            Path string
        """
        return "/app"


class StrategyRegistry:
    """
    Registry for repository strategies.

    Manages strategy registration and detection.

    Usage:
        registry = StrategyRegistry()
        registry.register(PythonStrategy())
        registry.register(NodeStrategy())

        strategy = registry.detect(repo_path)
        if strategy:
            image = strategy.get_base_image()
    """

    _instance: Optional["StrategyRegistry"] = None

    def __new__(cls) -> "StrategyRegistry":
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._strategies: List[RepositoryStrategy] = []
        self._initialized = True

    def register(self, strategy: RepositoryStrategy) -> None:
        """
        Register a strategy.

        Args:
            strategy: Strategy instance to register
        """
        self._strategies.append(strategy)
        # Sort by priority (higher first)
        self._strategies.sort(key=lambda s: -s.priority)
        logger.debug(f"Registered strategy: {strategy.name}")

    def unregister(self, strategy_name: str) -> bool:
        """
        Unregister a strategy by name.

        Args:
            strategy_name: Name of strategy to remove

        Returns:
            True if strategy was found and removed
        """
        for i, s in enumerate(self._strategies):
            if s.name == strategy_name:
                del self._strategies[i]
                return True
        return False

    def detect(self, repo_path: str) -> Optional[RepositoryStrategy]:
        """
        Detect the best strategy for a repository.

        Args:
            repo_path: Path to the repository

        Returns:
            Best matching strategy or None
        """
        best_strategy = None
        best_confidence = 0.0

        for strategy in self._strategies:
            try:
                result = strategy.detect(repo_path)
                if result.detected and result.confidence > best_confidence:
                    best_strategy = strategy
                    best_confidence = result.confidence
            except Exception as e:
                logger.warning(f"Error in {strategy.name} detection: {e}")

        if best_strategy:
            logger.info(f"Detected strategy: {best_strategy.name} (confidence: {best_confidence})")

        return best_strategy

    def get_all(self) -> List[RepositoryStrategy]:
        """Get all registered strategies."""
        return self._strategies.copy()

    def get_by_name(self, name: str) -> Optional[RepositoryStrategy]:
        """Get a strategy by name."""
        for s in self._strategies:
            if s.name == name:
                return s
        return None

    @classmethod
    def get_instance(cls) -> "StrategyRegistry":
        """Get the singleton instance."""
        return cls()

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton (for testing)."""
        cls._instance = None


def get_strategy_registry() -> StrategyRegistry:
    """Get the global strategy registry."""
    return StrategyRegistry.get_instance()
