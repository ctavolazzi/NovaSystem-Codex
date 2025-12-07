"""
Configuration management for NovaSystem.

This module provides configuration management for the Nova Process.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    """Configuration class for NovaSystem."""

    # LLM Configuration
    openai_api_key: Optional[str] = None
    ollama_host: str = "http://localhost:11434"
    default_model: str = "claude-3-5-haiku-20241022"

    # Process Configuration
    max_iterations: int = 5
    default_domains: list = None

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Web Interface Configuration
    web_host: str = "0.0.0.0"
    web_port: int = 5000

    # Gradio Configuration
    gradio_host: str = "0.0.0.0"
    gradio_port: int = 7860

    # Memory Configuration
    max_short_term_memory: int = 10
    max_long_term_memory: int = 100

    def __post_init__(self):
        """Post-initialization setup."""
        if self.default_domains is None:
            self.default_domains = ["General", "Technology", "Business"]

        # Load from environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY", self.openai_api_key)
        self.ollama_host = os.getenv("OLLAMA_HOST", self.ollama_host)
        self.default_model = os.getenv("DEFAULT_MODEL", self.default_model)

        # API configuration
        self.api_host = os.getenv("API_HOST", self.api_host)
        self.api_port = int(os.getenv("API_PORT", self.api_port))

        # Web configuration
        self.web_host = os.getenv("WEB_HOST", self.web_host)
        self.web_port = int(os.getenv("WEB_PORT", self.web_port))

        # Gradio configuration
        self.gradio_host = os.getenv("GRADIO_HOST", self.gradio_host)
        self.gradio_port = int(os.getenv("GRADIO_PORT", self.gradio_port))

# Global configuration instance
_config: Optional[Config] = None

def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config

def set_config(config: Config) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config

def load_config_from_file(config_path: str) -> Config:
    """Load configuration from a file."""
    # This could be extended to load from JSON, YAML, etc.
    # For now, just return default config
    return Config()
