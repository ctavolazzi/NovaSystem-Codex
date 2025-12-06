"""Pricing and cost estimation utilities for Gemini models."""

from dataclasses import dataclass
from typing import Dict
import math


# Pricing per 1M tokens unless noted otherwise
PRICING: Dict[str, Dict[str, float]] = {
    "gemini-2.5-flash": {"input": 0.10, "output": 0.40},
    "gemini-2.5-flash-lite": {"input": 0.075, "output": 0.30},
    "gemini-3-pro-preview": {"input": 2.00, "output": 12.00},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    # Imagen has a fixed price per image
    "imagen-3-fast": {"image": 0.03},
}


MODEL_ALIASES = {
    "gemini-2.5-flash": "gemini-2.5-flash",
    "gemini-2-5-flash": "gemini-2.5-flash",
    "gemini-2_5-flash": "gemini-2.5-flash",
    "gemini-2.5-flash-lite": "gemini-2.5-flash-lite",
    "gemini-2-5-flash-lite": "gemini-2.5-flash-lite",
    "gemini-3-pro-preview": "gemini-3-pro-preview",
    "gemini-3-pro": "gemini-3-pro-preview",
    "gemini-2.5-pro": "gemini-2.5-pro",
    "gemini-2-5-pro": "gemini-2.5-pro",
    "imagen-3-fast": "imagen-3-fast",
    "imagen-3": "imagen-3-fast",
}


@dataclass
class CostEstimate:
    """Offline estimate of LLM cost."""

    model: str
    input_tokens: int
    output_tokens: int
    projected_cost: float
    currency: str = "USD"

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


def normalize_model_name(model: str) -> str:
    """Normalize various model name styles to internal keys."""
    key = (model or "").strip().lower().replace(" ", "-").replace("_", "-")
    # If names come in as model/version form, take the last segment
    key = key.split("/")[-1]
    return MODEL_ALIASES.get(key, key)


def estimate_tokens_from_text(text: str) -> int:
    """Heuristic: 1 token ≈ 4 characters."""
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


class CostEstimator:
    """Estimates token usage and projected price before execution."""

    def __init__(self, pricing: Dict[str, Dict[str, float]] | None = None):
        self.pricing = pricing or PRICING

    def estimate(
        self,
        model: str,
        input_text: str,
        estimated_output_tokens: int = 1000,
    ) -> CostEstimate:
        """
        Estimate token counts and projected dollar cost.

        Args:
            model: Target model name (Gemini family or Imagen)
            input_text: Prompt text
            estimated_output_tokens: Planned output tokens (default 1000)
        """
        normalized = normalize_model_name(model)
        if normalized not in self.pricing:
            raise ValueError(f"Pricing not configured for model '{model}'")

        input_tokens = estimate_tokens_from_text(input_text)
        output_tokens = max(0, estimated_output_tokens or 0)

        price = self.pricing[normalized]

        if "image" in price:
            projected_cost = price["image"]
        else:
            input_cost = (input_tokens / 1_000_000) * price["input"]
            output_cost = (output_tokens / 1_000_000) * price["output"]
            projected_cost = input_cost + output_cost

        # Round to 6 decimals for readability
        projected_cost = round(projected_cost, 6)

        return CostEstimate(
            model=normalized,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            projected_cost=projected_cost,
        )
