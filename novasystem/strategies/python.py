"""
Python Repository Strategy.

Handles Python projects with:
- requirements.txt
- setup.py
- pyproject.toml
- Pipfile
"""

import os
from typing import Dict, List, Optional

from .base import RepositoryStrategy, StrategyResult


class PythonStrategy(RepositoryStrategy):
    """
    Strategy for Python repositories.

    Detection:
    - requirements.txt (pip)
    - setup.py (setuptools)
    - pyproject.toml (modern Python)
    - Pipfile (pipenv)
    - setup.cfg (setuptools)

    Base Image: python:3.11-slim

    Pre-install:
    - Create virtual environment
    - Upgrade pip

    Post-install:
    - Run tests if pytest available
    """

    name = "python"
    priority = 90  # High priority - very common

    # Files that indicate a Python project
    INDICATOR_FILES = [
        ("pyproject.toml", 1.0),      # Modern standard
        ("setup.py", 0.95),           # Classic setuptools
        ("requirements.txt", 0.9),    # pip requirements
        ("Pipfile", 0.85),            # pipenv
        ("setup.cfg", 0.8),           # setuptools config
        ("poetry.lock", 1.0),         # Poetry
        ("tox.ini", 0.7),             # tox testing
        ("pytest.ini", 0.7),          # pytest config
    ]

    def detect(self, repo_path: str) -> StrategyResult:
        """Detect Python project."""
        detected_files = []
        max_confidence = 0.0

        for filename, confidence in self.INDICATOR_FILES:
            filepath = os.path.join(repo_path, filename)
            if os.path.exists(filepath):
                detected_files.append(filename)
                max_confidence = max(max_confidence, confidence)

        # Check for .py files as additional signal
        has_py_files = any(
            f.endswith(".py")
            for f in os.listdir(repo_path)
            if os.path.isfile(os.path.join(repo_path, f))
        )

        if has_py_files and max_confidence == 0:
            max_confidence = 0.5
            detected_files.append("*.py files")

        return StrategyResult(
            detected=max_confidence > 0,
            strategy_name=self.name,
            confidence=max_confidence,
            detected_files=detected_files,
        )

    def get_base_image(self) -> str:
        """Get Python base image."""
        return "python:3.11-slim"

    def get_pre_install_commands(self, repo_path: str) -> List[str]:
        """Setup Python environment."""
        commands = [
            "python -m venv /app/venv",
            "source /app/venv/bin/activate",
            "pip install --upgrade pip",
        ]

        # If pyproject.toml exists, install build tools
        if os.path.exists(os.path.join(repo_path, "pyproject.toml")):
            commands.append("pip install build wheel")

        return commands

    def get_install_command(self, repo_path: str) -> Optional[str]:
        """Get primary install command."""
        # Check for different package managers in order of preference

        if os.path.exists(os.path.join(repo_path, "pyproject.toml")):
            # Modern Python project
            return "pip install -e ."

        if os.path.exists(os.path.join(repo_path, "Pipfile")):
            return "pipenv install"

        if os.path.exists(os.path.join(repo_path, "requirements.txt")):
            return "pip install -r requirements.txt"

        if os.path.exists(os.path.join(repo_path, "setup.py")):
            return "pip install -e ."

        return None

    def get_post_install_commands(self, repo_path: str) -> List[str]:
        """Verify installation."""
        commands = []

        # Check if pytest is available
        if os.path.exists(os.path.join(repo_path, "pytest.ini")) or \
           os.path.exists(os.path.join(repo_path, "tests")):
            commands.append("pip install pytest || true")
            commands.append("pytest --version || true")

        return commands

    def get_env_vars(self) -> Dict[str, str]:
        """Python environment variables."""
        return {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED": "1",
            "PATH": "/app/venv/bin:$PATH",
        }
