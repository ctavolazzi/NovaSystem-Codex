"""
Go Repository Strategy.

Handles Go projects with:
- go.mod
- go.sum
"""

import os
from typing import Dict, List, Optional

from .base import RepositoryStrategy, StrategyResult


class GoStrategy(RepositoryStrategy):
    """
    Strategy for Go repositories.

    Detection:
    - go.mod
    - go.sum

    Base Image: golang:1.22-alpine

    Pre-install:
    - None needed (Go handles deps)

    Post-install:
    - Run go vet
    """

    name = "go"
    priority = 80

    INDICATOR_FILES = [
        ("go.mod", 1.0),
        ("go.sum", 0.95),
        ("Gopkg.toml", 0.8),  # dep (legacy)
        ("Gopkg.lock", 0.8),
    ]

    def detect(self, repo_path: str) -> StrategyResult:
        """Detect Go project."""
        detected_files = []
        max_confidence = 0.0

        for filename, confidence in self.INDICATOR_FILES:
            filepath = os.path.join(repo_path, filename)
            if os.path.exists(filepath):
                detected_files.append(filename)
                max_confidence = max(max_confidence, confidence)

        # Check for .go files in root
        has_go = any(
            f.endswith(".go")
            for f in os.listdir(repo_path)
            if os.path.isfile(os.path.join(repo_path, f))
        )
        if has_go and max_confidence == 0:
            max_confidence = 0.5
            detected_files.append("*.go files")

        return StrategyResult(
            detected=max_confidence > 0,
            strategy_name=self.name,
            confidence=max_confidence,
            detected_files=detected_files,
        )

    def get_base_image(self) -> str:
        """Get Go base image."""
        return "golang:1.22-alpine"

    def get_pre_install_commands(self, repo_path: str) -> List[str]:
        """Setup Go environment."""
        return []  # Go module system handles everything

    def get_install_command(self, repo_path: str) -> Optional[str]:
        """Get primary install command."""
        return "go build ./..."

    def get_post_install_commands(self, repo_path: str) -> List[str]:
        """Verify installation."""
        return [
            "go mod download",
            "go vet ./...",
        ]

    def get_env_vars(self) -> Dict[str, str]:
        """Go environment variables."""
        return {
            "GOPATH": "/go",
            "CGO_ENABLED": "0",
        }
