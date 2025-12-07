"""
Single Source of Truth for Model Configuration

This module provides centralized model configuration for all NovaSystem agents.
All agents should use the models defined here to ensure consistency.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import os

@dataclass
class ModelConfig:
    """Centralized model configuration for all agents."""

    # Primary model for all agents
    DEFAULT_MODEL: str = "claude-3-5-haiku-20241022"

    # Alternative models for different use cases
    FAST_MODEL: str = "claude-3-5-haiku-20241022"
    BALANCED_MODEL: str = "claude-3-5-sonnet-20241022"
    POWERFUL_MODEL: str = "claude-3-opus-20240229"

    # Fallback models (Ollama)
    FALLBACK_MODELS: List[str] = None

    # Model assignments for specific agent types
    AGENT_MODELS: Dict[str, str] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.FALLBACK_MODELS is None:
            self.FALLBACK_MODELS = [
                "ollama:phi3",
                "ollama:llama3",
                "ollama:mistral"
            ]

        if self.AGENT_MODELS is None:
            # All agents use the same model for consistency
            self.AGENT_MODELS = {
                "dce": self.DEFAULT_MODEL,
                "cae": self.DEFAULT_MODEL,
                "domain_expert": self.DEFAULT_MODEL,
                "research_bot": self.DEFAULT_MODEL,
                "data_analyst": self.DEFAULT_MODEL,
                "code_helper": self.DEFAULT_MODEL,
                "marketing_bot": self.DEFAULT_MODEL,
                "problem_solver": self.DEFAULT_MODEL,
            }

    def get_model_for_agent(self, agent_type: str) -> str:
        """Get the model for a specific agent type."""
        return self.AGENT_MODELS.get(agent_type, self.DEFAULT_MODEL)

    def get_default_model(self) -> str:
        """Get the default model for all agents."""
        # Allow environment variable override
        return os.getenv("NOVASYSTEM_MODEL", self.DEFAULT_MODEL)

    def get_fast_model(self) -> str:
        """Get the fast model for quick tasks."""
        return self.FAST_MODEL

    def get_balanced_model(self) -> str:
        """Get the balanced model for general tasks."""
        return self.BALANCED_MODEL

    def get_powerful_model(self) -> str:
        """Get the most powerful model for complex tasks."""
        return self.POWERFUL_MODEL

    def get_fallback_models(self) -> List[str]:
        """Get fallback models."""
        return self.FALLBACK_MODELS

    def set_model_for_agent(self, agent_type: str, model: str):
        """Set a specific model for an agent type."""
        self.AGENT_MODELS[agent_type] = model

    def set_default_model(self, model: str):
        """Set the default model for all agents."""
        self.DEFAULT_MODEL = model
        # Update all agent models to use the new default
        for agent_type in self.AGENT_MODELS:
            self.AGENT_MODELS[agent_type] = model

# Global model configuration instance
_model_config: Optional[ModelConfig] = None

def get_model_config() -> ModelConfig:
    """Get the global model configuration instance."""
    global _model_config
    if _model_config is None:
        _model_config = ModelConfig()
    return _model_config

def get_model_for_agent(agent_type: str) -> str:
    """Get the model for a specific agent type."""
    return get_model_config().get_model_for_agent(agent_type)

def get_default_model() -> str:
    """Get the default model for all agents."""
    return get_model_config().get_default_model()

def set_default_model(model: str):
    """Set the default model for all agents."""
    get_model_config().set_default_model(model)

def set_model_for_agent(agent_type: str, model: str):
    """Set a specific model for an agent type."""
    get_model_config().set_model_for_agent(agent_type, model)
