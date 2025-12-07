"""Cost estimation utilities for Gemini-compatible models."""

from dataclasses import dataclass
from typing import Dict
import math


TOKEN_ESTIMATE_RATIO = 4  # Approximate characters per token


@dataclass
class CostEstimate:
    """Projected cost details for a request."""

    input_tokens: int
    projected_cost: float
    currency: str = "USD"


class CostEstimator:
    """Estimate token usage and projected spend before making API calls."""

    # Pricing per 1M tokens (input/output) unless noted otherwise
    PRICING: Dict[str, Dict[str, float]] = {
        "gemini-2.5-flash": {"input": 0.10, "output": 0.40},
        "gemini-2.5-flash-lite": {"input": 0.075, "output": 0.30},
        "gemini-3-pro": {"input": 2.00, "output": 12.00},
        "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
        # Imagen pricing is fixed per generated image
        "imagen-3-fast": {"fixed": 0.03},
    }

    def estimate(
        self,
        model: str,
        input_text: str,
        estimated_output_tokens: int = 1000,
    ) -> CostEstimate:
        """Estimate tokens and projected USD cost for a request.

        Args:
            model: Target model name.
            input_text: Prompt text used for estimation.
            estimated_output_tokens: Anticipated completion length.

        Returns:
            CostEstimate with token count and projected cost.
        """

        normalized_model = model.lower()
        pricing = self.PRICING.get(normalized_model)
        if pricing is None:
            raise ValueError(f"No pricing available for model: {model}")

        input_tokens = self._estimate_tokens(input_text)

        # Imagen is priced per image rather than per token
        if "fixed" in pricing:
            projected_cost = pricing["fixed"]
        else:
            projected_cost = self._calculate_token_cost(
                pricing, input_tokens, estimated_output_tokens
            )

        return CostEstimate(
            input_tokens=input_tokens,
            projected_cost=round(projected_cost, 6),
        )

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Rudimentary token estimation based on character length."""

        return math.ceil(len(text) / TOKEN_ESTIMATE_RATIO)

    @staticmethod
    def _calculate_token_cost(
        pricing: Dict[str, float], input_tokens: int, output_tokens: int
    ) -> float:
        """Calculate cost using pricing dictionary and token counts."""

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost
