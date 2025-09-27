"""
NovaSystem Settings - Single Source of Truth

This module contains all configuration settings for the NovaSystem.
All settings can be overridden via environment variables or config files.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class SessionConfig:
    """Configuration for session management."""
    # Default session storage location
    default_session_dir: str = "sessions"

    # Session file naming pattern
    session_file_pattern: str = "session_{timestamp}_{session_id}.md"

    # Whether to auto-save sessions
    auto_save_sessions: bool = True

    # Session metadata to include
    include_metadata: bool = True

    # Maximum session file size (in MB)
    max_session_size_mb: int = 10

    # Session retention (days, 0 = keep forever)
    session_retention_days: int = 0

@dataclass
class LLMConfig:
    """Configuration for LLM services."""
    # Default model
    default_model: str = "claude-3-5-sonnet-20241022"

    # Model priority order
    model_priority: list = field(default_factory=lambda: [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-sonnet-4-20250514",
        "claude-opus-4-1-20250805"
    ])

    # Fallback models (Ollama)
    fallback_models: list = field(default_factory=lambda: [
        "ollama:phi3",
        "ollama:llama3",
        "ollama:mistral"
    ])

    # Default parameters
    default_temperature: float = 0.7
    default_max_tokens: int = 1000

    # API keys (loaded from environment)
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

@dataclass
class SystemConfig:
    """System-wide configuration."""
    # Project root directory
    project_root: str = str(Path(__file__).parent.parent.parent)

    # Data directory
    data_dir: str = "data"

    # Logs directory
    logs_dir: str = "logs"

    # Config directory
    config_dir: str = "config"

    # Whether to create directories if they don't exist
    auto_create_dirs: bool = True

    # Logging level
    log_level: str = "INFO"

@dataclass
class NovaConfig:
    """Main NovaSystem configuration."""
    session: SessionConfig = field(default_factory=SessionConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    system: SystemConfig = field(default_factory=SystemConfig)

    def __post_init__(self):
        """Initialize configuration after creation."""
        self._load_from_environment()
        self._load_from_config_file()
        self._ensure_directories()

    def _load_from_environment(self):
        """Load configuration from environment variables."""
        # Session configuration
        self.session.default_session_dir = os.getenv(
            "NOVASYSTEM_SESSION_DIR",
            self.session.default_session_dir
        )
        self.session.auto_save_sessions = os.getenv(
            "NOVASYSTEM_AUTO_SAVE",
            str(self.session.auto_save_sessions)
        ).lower() == "true"

        # LLM configuration
        self.llm.default_model = os.getenv(
            "NOVASYSTEM_DEFAULT_MODEL",
            self.llm.default_model
        )
        self.llm.default_temperature = float(os.getenv(
            "NOVASYSTEM_TEMPERATURE",
            str(self.llm.default_temperature)
        ))
        self.llm.default_max_tokens = int(os.getenv(
            "NOVASYSTEM_MAX_TOKENS",
            str(self.llm.default_max_tokens)
        ))

        # API keys
        self.llm.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.llm.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        # System configuration
        self.system.project_root = os.getenv(
            "NOVASYSTEM_PROJECT_ROOT",
            self.system.project_root
        )
        self.system.data_dir = os.getenv(
            "NOVASYSTEM_DATA_DIR",
            self.system.data_dir
        )
        self.system.logs_dir = os.getenv(
            "NOVASYSTEM_LOGS_DIR",
            self.system.logs_dir
        )
        self.system.log_level = os.getenv(
            "NOVASYSTEM_LOG_LEVEL",
            self.system.log_level
        )

    def _load_from_config_file(self):
        """Load configuration from config file if it exists."""
        config_file = Path(self.system.project_root) / "config" / "novasystem.json"

        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)

                # Update configuration with file data
                if 'session' in config_data:
                    for key, value in config_data['session'].items():
                        if hasattr(self.session, key):
                            setattr(self.session, key, value)

                if 'llm' in config_data:
                    for key, value in config_data['llm'].items():
                        if hasattr(self.llm, key):
                            setattr(self.llm, key, value)

                if 'system' in config_data:
                    for key, value in config_data['system'].items():
                        if hasattr(self.system, key):
                            setattr(self.system, key, value)

                logger.info(f"Loaded configuration from {config_file}")

            except Exception as e:
                logger.warning(f"Failed to load config file {config_file}: {e}")

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        if not self.system.auto_create_dirs:
            return

        directories = [
            Path(self.system.project_root) / self.system.data_dir,
            Path(self.system.project_root) / self.system.logs_dir,
            Path(self.system.project_root) / self.system.config_dir,
            Path(self.system.project_root) / self.system.data_dir / self.session.default_session_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")

    def get_session_dir(self, custom_dir: Optional[str] = None) -> Path:
        """Get the session directory path."""
        if custom_dir:
            return Path(custom_dir)
        return Path(self.system.project_root) / self.system.data_dir / self.session.default_session_dir

    def get_data_dir(self) -> Path:
        """Get the data directory path."""
        return Path(self.system.project_root) / self.system.data_dir

    def get_logs_dir(self) -> Path:
        """Get the logs directory path."""
        return Path(self.system.project_root) / self.system.logs_dir

    def get_config_dir(self) -> Path:
        """Get the config directory path."""
        return Path(self.system.project_root) / self.system.config_dir

    def save_config(self, config_file: Optional[Path] = None):
        """Save current configuration to file."""
        if config_file is None:
            config_file = self.get_config_dir() / "novasystem.json"

        config_data = {
            "session": {
                "default_session_dir": self.session.default_session_dir,
                "auto_save_sessions": self.session.auto_save_sessions,
                "include_metadata": self.session.include_metadata,
                "max_session_size_mb": self.session.max_session_size_mb,
                "session_retention_days": self.session.session_retention_days,
            },
            "llm": {
                "default_model": self.llm.default_model,
                "model_priority": self.llm.model_priority,
                "fallback_models": self.llm.fallback_models,
                "default_temperature": self.llm.default_temperature,
                "default_max_tokens": self.llm.default_max_tokens,
            },
            "system": {
                "data_dir": self.system.data_dir,
                "logs_dir": self.system.logs_dir,
                "config_dir": self.system.config_dir,
                "auto_create_dirs": self.system.auto_create_dirs,
                "log_level": self.system.log_level,
            }
        }

        try:
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            logger.info(f"Saved configuration to {config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "session": {
                "default_session_dir": self.session.default_session_dir,
                "auto_save_sessions": self.session.auto_save_sessions,
                "include_metadata": self.session.include_metadata,
                "max_session_size_mb": self.session.max_session_size_mb,
                "session_retention_days": self.session.session_retention_days,
            },
            "llm": {
                "default_model": self.llm.default_model,
                "model_priority": self.llm.model_priority,
                "fallback_models": self.llm.fallback_models,
                "default_temperature": self.llm.default_temperature,
                "default_max_tokens": self.llm.default_max_tokens,
            },
            "system": {
                "project_root": self.system.project_root,
                "data_dir": self.system.data_dir,
                "logs_dir": self.system.logs_dir,
                "config_dir": self.system.config_dir,
                "auto_create_dirs": self.system.auto_create_dirs,
                "log_level": self.system.log_level,
            }
        }

# Global configuration instance
_config: Optional[NovaConfig] = None

def get_config() -> NovaConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = NovaConfig()
    return _config

def reload_config():
    """Reload the configuration."""
    global _config
    _config = NovaConfig()
    return _config
