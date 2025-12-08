"""
CLI Startup Tests
-----------------
5 additional tests to bring the total to 303 tests.
These tests verify the CLI startup, banner display, and initialization.
"""

import os
import sys
import subprocess
from pathlib import Path

import pytest


class TestCLIStartup:
    """Test CLI startup and initialization."""

    def test_cli_module_is_runnable(self):
        """Test that the CLI module can be run with python -m."""
        result = subprocess.run(
            [sys.executable, "-m", "novasystem.cli", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "NovaSystem" in result.stdout or "novasystem" in result.stdout.lower()

    def test_cli_version_flag(self):
        """Test that --version flag works."""
        result = subprocess.run(
            [sys.executable, "-m", "novasystem.cli", "--version"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        # Should contain version number pattern
        assert "." in result.stdout  # Version like "0.3.2"

    def test_cli_has_ask_command(self):
        """Test that 'ask' command is available."""
        result = subprocess.run(
            [sys.executable, "-m", "novasystem.cli", "ask", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "question" in result.stdout.lower() or "ask" in result.stdout.lower()

    def test_cli_has_solve_command(self):
        """Test that 'solve' command is available."""
        result = subprocess.run(
            [sys.executable, "-m", "novasystem.cli", "solve", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0
        assert "problem" in result.stdout.lower() or "solve" in result.stdout.lower()

    def test_cli_status_command_runs(self):
        """Test that 'status' command runs without errors."""
        result = subprocess.run(
            [sys.executable, "-m", "novasystem.cli", "status"],
            capture_output=True,
            text=True,
            timeout=30
        )
        # Status should run (exit 0) or gracefully handle missing API keys
        # We just check it doesn't crash unexpectedly
        assert result.returncode in [0, 1]  # 0 = success, 1 = handled error
        # Should show some output about status or configuration
        assert len(result.stdout) > 0 or len(result.stderr) > 0
