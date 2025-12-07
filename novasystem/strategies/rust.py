"""
Rust Repository Strategy.

Handles Rust projects with:
- Cargo.toml
- cargo
"""

import os
from typing import Dict, List, Optional

from .base import RepositoryStrategy, StrategyResult


class RustStrategy(RepositoryStrategy):
    """
    Strategy for Rust repositories.

    Detection:
    - Cargo.toml
    - Cargo.lock

    Base Image: rust:latest

    Pre-install:
    - Update cargo

    Post-install:
    - Run cargo check
    """

    name = "rust"
    priority = 80

    INDICATOR_FILES = [
        ("Cargo.toml", 1.0),
        ("Cargo.lock", 0.95),
        ("rust-toolchain", 0.9),
        ("rust-toolchain.toml", 0.9),
    ]

    def detect(self, repo_path: str) -> StrategyResult:
        """Detect Rust project."""
        detected_files = []
        max_confidence = 0.0

        for filename, confidence in self.INDICATOR_FILES:
            filepath = os.path.join(repo_path, filename)
            if os.path.exists(filepath):
                detected_files.append(filename)
                max_confidence = max(max_confidence, confidence)

        # Check for .rs files
        src_dir = os.path.join(repo_path, "src")
        if os.path.isdir(src_dir):
            has_rs = any(f.endswith(".rs") for f in os.listdir(src_dir))
            if has_rs and max_confidence == 0:
                max_confidence = 0.6
                detected_files.append("src/*.rs")

        return StrategyResult(
            detected=max_confidence > 0,
            strategy_name=self.name,
            confidence=max_confidence,
            detected_files=detected_files,
        )

    def get_base_image(self) -> str:
        """Get Rust base image."""
        return "rust:latest"

    def get_pre_install_commands(self, repo_path: str) -> List[str]:
        """Setup Rust environment."""
        return [
            "rustup update stable",
            "rustup component add clippy rustfmt",
        ]

    def get_install_command(self, repo_path: str) -> Optional[str]:
        """Get primary install command."""
        return "cargo build"

    def get_post_install_commands(self, repo_path: str) -> List[str]:
        """Verify installation."""
        return [
            "cargo check",
            "cargo clippy --all-targets || true",
        ]

    def get_env_vars(self) -> Dict[str, str]:
        """Rust environment variables."""
        return {
            "CARGO_HOME": "/app/.cargo",
            "RUSTUP_HOME": "/app/.rustup",
        }
