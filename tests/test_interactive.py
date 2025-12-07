"""
Tests for the interactive terminal application.
"""

import pytest
import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestInteractiveApp:
    """Test the interactive application components."""

    def test_can_import_module(self):
        """Test that the interactive module can be imported."""
        from novasystem.interactive import VERSION
        assert VERSION == "0.3.1"

    def test_colors_defined(self):
        """Test that color codes are defined."""
        from novasystem.interactive import Colors
        assert hasattr(Colors, 'CYAN')
        assert hasattr(Colors, 'GREEN')
        assert hasattr(Colors, 'RESET')

    def test_app_state_initialization(self):
        """Test that AppState initializes correctly."""
        from novasystem.interactive import AppState
        state = AppState()
        assert state.running == True
        assert state.screensaver_active == False
        assert state.stats["commands_run"] == 0

    def test_screensaver_class(self):
        """Test that Screensaver class works."""
        from novasystem.interactive import Screensaver
        ss = Screensaver()

        # Test neural pulse
        lines = ss.render("neural")
        assert len(lines) > 0

        # Test starfield
        lines = ss.render("stars")
        assert len(lines) > 0

    def test_screensaver_timeout_configured(self):
        """Test that screensaver timeout is reasonable."""
        from novasystem.interactive import SCREENSAVER_TIMEOUT
        assert SCREENSAVER_TIMEOUT >= 10  # At least 10 seconds
        assert SCREENSAVER_TIMEOUT <= 300  # No more than 5 minutes
