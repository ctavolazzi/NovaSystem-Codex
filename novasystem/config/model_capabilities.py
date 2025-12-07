"""
Model capability definitions.

Centralized configuration for LLM model capabilities.
"""

from typing import Dict, Any

# Model capability database
MODEL_CAPABILITIES: Dict[str, Dict[str, Any]] = {
    # OpenAI models
    "gpt-4": {
        "reasoning": 95, "coding": 90, "analysis": 95, "creativity": 85, "speed": 70,
        "context_length": 128000, "type": "openai",
        "description": "GPT-4: Highly capable reasoning model"
    },
    "gpt-4-turbo": {
        "reasoning": 95, "coding": 90, "analysis": 95, "creativity": 85, "speed": 85,
        "context_length": 128000, "type": "openai",
        "description": "GPT-4 Turbo: Fast version of GPT-4"
    },
    "gpt-3.5-turbo": {
        "reasoning": 80, "coding": 75, "analysis": 80, "creativity": 75, "speed": 90,
        "context_length": 16000, "type": "openai",
        "description": "GPT-3.5 Turbo: Fast and efficient"
    },
    "o1-preview": {
        "reasoning": 98, "coding": 95, "analysis": 98, "creativity": 90, "speed": 30,
        "context_length": 128000, "type": "openai",
        "description": "OpenAI o1-preview: Advanced reasoning model"
    },
    "o1-mini": {
        "reasoning": 95, "coding": 90, "analysis": 95, "creativity": 85, "speed": 50,
        "context_length": 128000, "type": "openai",
        "description": "OpenAI o1-mini: Fast reasoning model"
    },

    # Claude 4 models
    "claude-opus-4-1-20250805": {
        "reasoning": 98, "coding": 98, "analysis": 98, "creativity": 95, "speed": 60,
        "context_length": 200000, "type": "anthropic",
        "description": "Claude Opus 4.1: Most powerful model"
    },
    "claude-opus-4-20250514": {
        "reasoning": 97, "coding": 97, "analysis": 97, "creativity": 95, "speed": 65,
        "context_length": 200000, "type": "anthropic",
        "description": "Claude Opus 4: Flagship model"
    },
    "claude-sonnet-4-20250514": {
        "reasoning": 95, "coding": 95, "analysis": 95, "creativity": 90, "speed": 85,
        "context_length": 200000, "type": "anthropic",
        "description": "Claude Sonnet 4: High-performance model"
    },

    # Claude 3.5 models
    "claude-3-5-sonnet-20241022": {
        "reasoning": 95, "coding": 95, "analysis": 95, "creativity": 90, "speed": 85,
        "context_length": 200000, "type": "anthropic",
        "description": "Claude 3.5 Sonnet: Excellent reasoning and coding"
    },
    "claude-3-5-haiku-20241022": {
        "reasoning": 90, "coding": 85, "analysis": 90, "creativity": 85, "speed": 95,
        "context_length": 200000, "type": "anthropic",
        "description": "Claude 3.5 Haiku: Fast and efficient"
    },

    # Claude 3 models
    "claude-3-opus-20240229": {
        "reasoning": 95, "coding": 90, "analysis": 95, "creativity": 95, "speed": 70,
        "context_length": 200000, "type": "anthropic",
        "description": "Claude 3 Opus: Most capable Claude 3"
    },
    "claude-3-sonnet-20240229": {
        "reasoning": 90, "coding": 90, "analysis": 90, "creativity": 85, "speed": 85,
        "context_length": 200000, "type": "anthropic",
        "description": "Claude 3 Sonnet: Balanced capabilities"
    },
    "claude-3-haiku-20240307": {
        "reasoning": 85, "coding": 80, "analysis": 85, "creativity": 80, "speed": 95,
        "context_length": 200000, "type": "anthropic",
        "description": "Claude 3 Haiku: Fast for quick tasks"
    },

    # Gemini models
    "gemini-2.5-flash": {
        "reasoning": 92, "coding": 90, "analysis": 92, "creativity": 88, "speed": 95,
        "context_length": 1000000, "type": "gemini",
        "description": "Gemini 2.5 Flash: Fast with 1M token context"
    },
    "gemini-2.5-pro": {
        "reasoning": 96, "coding": 95, "analysis": 96, "creativity": 92, "speed": 75,
        "context_length": 1000000, "type": "gemini",
        "description": "Gemini 2.5 Pro: Most capable Gemini"
    },
    "gemini-2.0-flash": {
        "reasoning": 90, "coding": 88, "analysis": 90, "creativity": 85, "speed": 92,
        "context_length": 1000000, "type": "gemini",
        "description": "Gemini 2.0 Flash: Fast multimodal"
    },
    "gemini-1.5-flash": {
        "reasoning": 88, "coding": 85, "analysis": 88, "creativity": 82, "speed": 90,
        "context_length": 1000000, "type": "gemini",
        "description": "Gemini 1.5 Flash: Efficient model"
    },
    "gemini-1.5-pro": {
        "reasoning": 93, "coding": 90, "analysis": 93, "creativity": 88, "speed": 70,
        "context_length": 2000000, "type": "gemini",
        "description": "Gemini 1.5 Pro: 2M token context"
    },

    # Ollama models
    "phi3": {
        "reasoning": 85, "coding": 80, "analysis": 85, "creativity": 80, "speed": 95,
        "context_length": 32000, "size_gb": 2.2, "type": "ollama",
        "description": "Microsoft Phi-3: Fast and efficient"
    },
    "llama3": {
        "reasoning": 90, "coding": 85, "analysis": 90, "creativity": 85, "speed": 80,
        "context_length": 128000, "type": "ollama",
        "description": "Llama 3: Strong general-purpose"
    },
    "llama3.2": {
        "reasoning": 88, "coding": 80, "analysis": 88, "creativity": 82, "speed": 85,
        "context_length": 128000, "type": "ollama",
        "description": "Llama 3.2: Good balance"
    },
    "mistral": {
        "reasoning": 85, "coding": 90, "analysis": 85, "creativity": 80, "speed": 90,
        "context_length": 32000, "type": "ollama",
        "description": "Mistral: Strong coding"
    },
    "codellama": {
        "reasoning": 80, "coding": 95, "analysis": 75, "creativity": 70, "speed": 85,
        "context_length": 100000, "type": "ollama",
        "description": "Code Llama: Specialized for coding"
    },
}

# Task type weights for model selection
TASK_WEIGHTS: Dict[str, list] = {
    "reasoning": ["reasoning", "analysis"],
    "coding": ["coding", "reasoning"],
    "analysis": ["analysis", "reasoning"],
    "creativity": ["creativity", "reasoning"],
    "general": ["reasoning", "analysis", "creativity", "coding"],
    "dce": ["reasoning", "analysis"],
    "cae": ["analysis", "reasoning"],
    "domain": ["analysis", "reasoning", "coding"],
}

# Provider model lists
OPENAI_MODELS = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "o1-preview", "o1-mini"]

ANTHROPIC_MODELS = [
    "claude-opus-4-1-20250805", "claude-opus-4-20250514", "claude-sonnet-4-20250514",
    "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022",
    "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
]

GEMINI_MODELS = [
    "gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash",
    "gemini-1.5-flash", "gemini-1.5-pro"
]


def get_model_capabilities(model_name: str) -> Dict[str, Any]:
    """Get capabilities for a specific model."""
    clean_name = model_name.replace("ollama:", "").replace("gemini:", "").lower()

    # Try exact match
    if clean_name in MODEL_CAPABILITIES:
        return MODEL_CAPABILITIES[clean_name]

    # Try partial match
    for model_key, caps in MODEL_CAPABILITIES.items():
        if clean_name in model_key or model_key in clean_name:
            return caps

    # Determine type for default
    if "ollama:" in model_name:
        model_type = "ollama"
    elif "claude-" in model_name:
        model_type = "anthropic"
    elif "gemini" in model_name.lower():
        model_type = "gemini"
    else:
        model_type = "openai"

    # Default capabilities
    return {
        "reasoning": 70, "coding": 70, "analysis": 70, "creativity": 70, "speed": 80,
        "context_length": 32000, "type": model_type,
        "description": "Unknown model"
    }


def get_task_weights(task_type: str) -> list:
    """Get capability weights for a task type."""
    return TASK_WEIGHTS.get(task_type, TASK_WEIGHTS["general"])
