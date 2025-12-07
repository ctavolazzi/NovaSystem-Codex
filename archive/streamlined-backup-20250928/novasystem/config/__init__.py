"""
NovaSystem Configuration Module

This module provides centralized configuration management for the NovaSystem.
All configuration is managed through a single source of truth.
"""

from .settings import NovaConfig, get_config

__all__ = ['NovaConfig', 'get_config']
