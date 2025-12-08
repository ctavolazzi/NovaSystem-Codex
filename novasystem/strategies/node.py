"""
Node.js Repository Strategy.

Handles Node.js/JavaScript projects with:
- package.json
- npm
- yarn
- pnpm
"""

import json
import os
from typing import Dict, List, Optional

from .base import RepositoryStrategy, StrategyResult


class NodeStrategy(RepositoryStrategy):
    """
    Strategy for Node.js repositories.

    Detection:
    - package.json (npm/yarn/pnpm)
    - yarn.lock (yarn)
    - pnpm-lock.yaml (pnpm)
    - package-lock.json (npm)

    Base Image: node:20-alpine

    Pre-install:
    - Detect package manager

    Post-install:
    - Run build if defined
    - Run tests if defined
    """

    name = "javascript"
    priority = 85

    INDICATOR_FILES = [
        ("package.json", 1.0),
        ("yarn.lock", 1.0),
        ("pnpm-lock.yaml", 1.0),
        ("package-lock.json", 0.95),
        ("tsconfig.json", 0.8),  # TypeScript
        (".npmrc", 0.7),
        ("lerna.json", 0.9),  # Monorepo
    ]

    def detect(self, repo_path: str) -> StrategyResult:
        """Detect Node.js project."""
        detected_files = []
        max_confidence = 0.0

        for filename, confidence in self.INDICATOR_FILES:
            filepath = os.path.join(repo_path, filename)
            if os.path.exists(filepath):
                detected_files.append(filename)
                max_confidence = max(max_confidence, confidence)

        metadata = {}

        # Parse package.json for more info
        package_json = os.path.join(repo_path, "package.json")
        if os.path.exists(package_json):
            try:
                with open(package_json) as f:
                    pkg = json.load(f)
                    metadata["name"] = pkg.get("name", "")
                    metadata["has_build"] = "build" in pkg.get("scripts", {})
                    metadata["has_test"] = "test" in pkg.get("scripts", {})
            except Exception:
                pass

        return StrategyResult(
            detected=max_confidence > 0,
            strategy_name=self.name,
            confidence=max_confidence,
            detected_files=detected_files,
            metadata=metadata,
        )

    def get_base_image(self) -> str:
        """Get Node.js base image."""
        return "node:20-alpine"

    def _detect_package_manager(self, repo_path: str) -> str:
        """Detect which package manager to use."""
        if os.path.exists(os.path.join(repo_path, "pnpm-lock.yaml")):
            return "pnpm"
        if os.path.exists(os.path.join(repo_path, "yarn.lock")):
            return "yarn"
        return "npm"

    def get_pre_install_commands(self, repo_path: str) -> List[str]:
        """Setup Node.js environment."""
        pm = self._detect_package_manager(repo_path)

        commands = []

        if pm == "pnpm":
            commands.append("npm install -g pnpm")
        elif pm == "yarn":
            commands.append("corepack enable || npm install -g yarn")

        return commands

    def get_install_command(self, repo_path: str) -> Optional[str]:
        """Get primary install command."""
        pm = self._detect_package_manager(repo_path)

        if pm == "pnpm":
            return "pnpm install"
        elif pm == "yarn":
            return "yarn install"
        else:
            return "npm install"

    def get_post_install_commands(self, repo_path: str) -> List[str]:
        """Verify installation."""
        commands = []

        # Check package.json for scripts
        package_json = os.path.join(repo_path, "package.json")
        if os.path.exists(package_json):
            try:
                with open(package_json) as f:
                    pkg = json.load(f)
                    scripts = pkg.get("scripts", {})

                    pm = self._detect_package_manager(repo_path)

                    # Run build if available
                    if "build" in scripts:
                        if pm == "pnpm":
                            commands.append("pnpm run build")
                        elif pm == "yarn":
                            commands.append("yarn build")
                        else:
                            commands.append("npm run build")
            except Exception:
                pass

        return commands

    def get_env_vars(self) -> Dict[str, str]:
        """Node.js environment variables."""
        return {
            "NODE_ENV": "development",
            "NPM_CONFIG_LOGLEVEL": "warn",
        }
