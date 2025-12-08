"""
Core Nova Process implementation.

This module contains the fundamental components of the Nova Process:
- Agent definitions and behaviors
- Process orchestration
- Memory and context management
- ASCII animation and PixelLab integration
"""

from .agents import DCEAgent, CAEAgent, DomainExpert
from .process import NovaProcess
from .memory import MemoryManager

# ASCII animation exports
try:
    from .ascii_animation import (
        play_sleeping_wizard,
        image_to_ascii,
        generate_breathing_frames,
        ASCIIAnimationPlayer,
        TypewriterMessageBox,
    )
    ASCII_AVAILABLE = True
except ImportError:
    ASCII_AVAILABLE = False
    play_sleeping_wizard = None
    image_to_ascii = None
    generate_breathing_frames = None
    ASCIIAnimationPlayer = None
    TypewriterMessageBox = None

# PixelLab exports
try:
    from .pixellab import generate_wizard_animation, AnimationResult
    PIXELLAB_AVAILABLE = True
except ImportError:
    PIXELLAB_AVAILABLE = False
    generate_wizard_animation = None
    AnimationResult = None

__all__ = [
    "DCEAgent",
    "CAEAgent",
    "DomainExpert",
    "NovaProcess",
    "MemoryManager",
    "play_sleeping_wizard",
    "image_to_ascii",
    "generate_breathing_frames",
    "ASCIIAnimationPlayer",
    "TypewriterMessageBox",
    "generate_wizard_animation",
    "AnimationResult",
    "ASCII_AVAILABLE",
    "PIXELLAB_AVAILABLE",
]
