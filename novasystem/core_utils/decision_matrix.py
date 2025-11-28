"""
Decision Matrix Utility
-----------------------
A comprehensive decision-making tool for quantifying and comparing options
against multiple criteria.

Usage:
    from novasystem.core_utils import make_decision

    result = make_decision(
        options=["Option A", "Option B", "Option C"],
        criteria=["Cost", "Speed", "Quality"],
        scores={
            "Option A": [7, 8, 6],
            "Option B": [9, 5, 7],
            "Option C": [6, 9, 8]
        },
        weights=[0.3, 0.2, 0.5]  # Optional: importance of each criterion
    )

    print(result)  # Shows ranking and analysis
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import json


@dataclass
class DecisionResult:
    """Results from a decision matrix analysis."""

    winner: str
    rankings: List[Tuple[str, float]]
    scores_breakdown: Dict[str, Dict[str, float]]
    analysis_method: str
    total_score: Dict[str, float]
    normalized_scores: Dict[str, float] = field(default_factory=dict)
    confidence_score: float = 0.0
    recommendation: str = ""

    def __str__(self) -> str:
        """Format results for display."""
        lines = [
            "=" * 70,
            f"DECISION MATRIX RESULTS ({self.analysis_method})",
            "=" * 70,
            f"\n🏆 WINNER: {self.winner}",
            f"   Confidence: {self.confidence_score:.1f}%",
            f"\n📊 RANKINGS:",
        ]

        for i, (option, score) in enumerate(self.rankings, 1):
            normalized = self.normalized_scores.get(option, 0)
            lines.append(
                f"   {i}. {option:20s} "
                f"Score: {score:6.2f} ({normalized:5.1f}%)"
            )

        lines.extend(
            [
                f"\n💡 RECOMMENDATION:",
                f"   {self.recommendation}",
                "\n📋 DETAILED BREAKDOWN:",
            ]
        )

        for option, criteria_scores in self.scores_breakdown.items():
            lines.append(f"\n   {option}:")
            for criterion, score in criteria_scores.items():
                lines.append(f"      {criterion:20s}: {score:6.2f}")

        lines.append("=" * 70)
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "winner": self.winner,
            "rankings": [(opt, float(score)) for opt, score in self.rankings],
            "scores_breakdown": self.scores_breakdown,
            "analysis_method": self.analysis_method,
            "total_score": self.total_score,
            "normalized_scores": self.normalized_scores,
            "confidence_score": self.confidence_score,
            "recommendation": self.recommendation,
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


class DecisionMatrix:
    """
    A flexible decision matrix for evaluating options against criteria.

    Supports multiple analysis methods:
    - weighted: Traditional weighted score (default)
    - normalized: Normalized scores (0-100 scale)
    - ranking: Convert scores to rankings per criterion
    - best_worst: Best-worst scaling method
    """

    def __init__(
        self,
        options: List[str],
        criteria: List[str],
        scores: Dict[str, List[Union[int, float]]],
        weights: Optional[List[float]] = None,
        method: str = "weighted",
    ):
        """
        Initialize decision matrix.

        Args:
            options: List of option names
            criteria: List of criterion names
            scores: Dict mapping option names to lists of scores
            weights: Optional list of weights (0-1) for each criterion
            method: Analysis method (weighted, normalized, ranking, best_worst)
        """
        self.options = options
        self.criteria = criteria
        self.scores = scores
        self.method = method

        # Validate inputs
        self._validate_inputs()

        # Set weights (equal if not provided)
        if weights is None:
            self.weights = [1.0 / len(criteria)] * len(criteria)
        else:
            # Normalize weights to sum to 1
            total = sum(weights)
            self.weights = [w / total for w in weights]

    def _validate_inputs(self):
        """Validate input data."""
        if not self.options:
            raise ValueError("Must provide at least one option")

        if not self.criteria:
            raise ValueError("Must provide at least one criterion")

        if not self.scores:
            raise ValueError("Must provide scores")

        # Check all options have scores
        for option in self.options:
            if option not in self.scores:
                raise ValueError(f"Missing scores for option: {option}")

            if len(self.scores[option]) != len(self.criteria):
                raise ValueError(
                    f"Option '{option}' has {len(self.scores[option])} "
                    f"scores but {len(self.criteria)} criteria"
                )

    def analyze(self) -> DecisionResult:
        """
        Perform decision matrix analysis.

        Returns:
            DecisionResult with rankings and analysis
        """
        if self.method == "weighted":
            return self._analyze_weighted()
        elif self.method == "normalized":
            return self._analyze_normalized()
        elif self.method == "ranking":
            return self._analyze_ranking()
        elif self.method == "best_worst":
            return self._analyze_best_worst()
        else:
            raise ValueError(f"Unknown analysis method: {self.method}")

    def _analyze_weighted(self) -> DecisionResult:
        """Traditional weighted score analysis."""
        total_scores = {}
        breakdown = {}

        # Calculate weighted scores
        for option in self.options:
            option_scores = self.scores[option]
            weighted_total = sum(
                score * weight
                for score, weight in zip(option_scores, self.weights)
            )
            total_scores[option] = weighted_total

            # Build breakdown
            breakdown[option] = {}
            for i, criterion in enumerate(self.criteria):
                weighted_score = option_scores[i] * self.weights[i]
                breakdown[option][f"{criterion} (w={self.weights[i]:.2f})"] = (
                    weighted_score
                )

        # Rank options
        rankings = sorted(
            total_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Normalize scores to percentages
        max_score = max(total_scores.values())
        normalized = {
            opt: (score / max_score * 100) for opt, score in total_scores.items()
        }

        # Calculate confidence (gap between 1st and 2nd)
        if len(rankings) > 1:
            gap = rankings[0][1] - rankings[1][1]
            confidence = min(100, (gap / rankings[0][1]) * 100)
        else:
            confidence = 100.0

        # Generate recommendation
        recommendation = self._generate_recommendation(
            rankings, normalized, confidence
        )

        return DecisionResult(
            winner=rankings[0][0],
            rankings=rankings,
            scores_breakdown=breakdown,
            analysis_method="Weighted Score",
            total_score=total_scores,
            normalized_scores=normalized,
            confidence_score=confidence,
            recommendation=recommendation,
        )

    def _analyze_normalized(self) -> DecisionResult:
        """Normalized score analysis (0-100 scale per criterion)."""
        normalized_scores = {}
        breakdown = {}

        # Normalize each criterion to 0-100
        for criterion_idx, criterion in enumerate(self.criteria):
            criterion_scores = [
                self.scores[opt][criterion_idx] for opt in self.options
            ]
            min_score = min(criterion_scores)
            max_score = max(criterion_scores)
            score_range = max_score - min_score if max_score > min_score else 1

            for option in self.options:
                raw_score = self.scores[option][criterion_idx]
                normalized = ((raw_score - min_score) / score_range) * 100

                if option not in normalized_scores:
                    normalized_scores[option] = []
                normalized_scores[option].append(normalized)

        # Calculate weighted totals
        total_scores = {}
        for option in self.options:
            weighted_total = sum(
                score * weight
                for score, weight in zip(
                    normalized_scores[option], self.weights
                )
            )
            total_scores[option] = weighted_total

            # Build breakdown
            breakdown[option] = {}
            for i, criterion in enumerate(self.criteria):
                breakdown[option][f"{criterion} (normalized)"] = (
                    normalized_scores[option][i]
                )

        # Rank options
        rankings = sorted(
            total_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Scores already normalized to 100
        normalized = {
            opt: (score / 100 * 100) for opt, score in total_scores.items()
        }

        # Calculate confidence
        if len(rankings) > 1:
            gap = rankings[0][1] - rankings[1][1]
            confidence = min(100, gap)
        else:
            confidence = 100.0

        recommendation = self._generate_recommendation(
            rankings, normalized, confidence
        )

        return DecisionResult(
            winner=rankings[0][0],
            rankings=rankings,
            scores_breakdown=breakdown,
            analysis_method="Normalized Score (0-100)",
            total_score=total_scores,
            normalized_scores=normalized,
            confidence_score=confidence,
            recommendation=recommendation,
        )

    def _analyze_ranking(self) -> DecisionResult:
        """Ranking-based analysis (convert scores to rankings)."""
        total_ranks = {option: 0 for option in self.options}
        breakdown = {}

        # Convert scores to rankings for each criterion
        for criterion_idx, criterion in enumerate(self.criteria):
            criterion_scores = {
                opt: self.scores[opt][criterion_idx] for opt in self.options
            }
            ranked = sorted(
                criterion_scores.items(), key=lambda x: x[1], reverse=True
            )

            for rank, (option, score) in enumerate(ranked, 1):
                weighted_rank = rank * self.weights[criterion_idx]
                total_ranks[option] += weighted_rank

                if option not in breakdown:
                    breakdown[option] = {}
                breakdown[option][f"{criterion} (rank)"] = rank

        # Lower rank is better, so reverse
        rankings = sorted(total_ranks.items(), key=lambda x: x[1])

        # Normalize (invert since lower is better)
        max_rank = max(total_ranks.values())
        normalized = {
            opt: ((max_rank - rank) / max_rank * 100)
            for opt, rank in total_ranks.items()
        }

        if len(rankings) > 1:
            gap = rankings[1][1] - rankings[0][1]
            confidence = min(100, (gap / max_rank) * 100)
        else:
            confidence = 100.0

        recommendation = self._generate_recommendation(
            [(opt, normalized[opt]) for opt, _ in rankings],
            normalized,
            confidence,
        )

        return DecisionResult(
            winner=rankings[0][0],
            rankings=[(opt, normalized[opt]) for opt, _ in rankings],
            scores_breakdown=breakdown,
            analysis_method="Ranking Method",
            total_score={opt: normalized[opt] for opt, _ in rankings},
            normalized_scores=normalized,
            confidence_score=confidence,
            recommendation=recommendation,
        )

    def _analyze_best_worst(self) -> DecisionResult:
        """Best-worst scaling method."""
        scaled_scores = {}
        breakdown = {}

        # Scale each option relative to best and worst
        for option in self.options:
            option_scores = self.scores[option]
            min_possible = min(option_scores)
            max_possible = max(option_scores)

            # Calculate how close to best vs worst
            total_score = 0
            breakdown[option] = {}

            for i, criterion in enumerate(self.criteria):
                score = option_scores[i]
                criterion_scores = [
                    self.scores[opt][i] for opt in self.options
                ]
                best = max(criterion_scores)
                worst = min(criterion_scores)

                if best > worst:
                    scaled = (score - worst) / (best - worst)
                else:
                    scaled = 1.0

                weighted_scaled = scaled * self.weights[i]
                total_score += weighted_scaled

                breakdown[option][f"{criterion} (best-worst)"] = scaled * 100

            scaled_scores[option] = total_score

        # Rank options
        rankings = sorted(
            scaled_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Normalize to percentages
        max_score = max(scaled_scores.values())
        normalized = {
            opt: (score / max_score * 100)
            for opt, score in scaled_scores.items()
        }

        if len(rankings) > 1:
            gap = rankings[0][1] - rankings[1][1]
            confidence = min(100, (gap / rankings[0][1]) * 100)
        else:
            confidence = 100.0

        recommendation = self._generate_recommendation(
            rankings, normalized, confidence
        )

        return DecisionResult(
            winner=rankings[0][0],
            rankings=rankings,
            scores_breakdown=breakdown,
            analysis_method="Best-Worst Scaling",
            total_score=scaled_scores,
            normalized_scores=normalized,
            confidence_score=confidence,
            recommendation=recommendation,
        )

    def _generate_recommendation(
        self,
        rankings: List[Tuple[str, float]],
        normalized: Dict[str, float],
        confidence: float,
    ) -> str:
        """Generate a recommendation based on results."""
        winner = rankings[0][0]
        winner_score = normalized[winner]

        if confidence > 70:
            return (
                f"Strong recommendation: '{winner}' clearly outperforms "
                f"other options with {winner_score:.1f}% score."
            )
        elif confidence > 40:
            if len(rankings) > 1:
                runner_up = rankings[1][0]
                return (
                    f"Moderate recommendation: '{winner}' is best "
                    f"({winner_score:.1f}%), but '{runner_up}' "
                    f"({normalized[runner_up]:.1f}%) is competitive. "
                    f"Consider other factors."
                )
            return f"Moderate recommendation: '{winner}' with {winner_score:.1f}% score."
        else:
            top_3 = [opt for opt, _ in rankings[:3]]
            return (
                f"Weak recommendation: Options are closely matched. "
                f"Top choices: {', '.join(top_3)}. "
                f"Consider additional criteria or stakeholder input."
            )


def make_decision(
    options: List[str],
    criteria: List[str],
    scores: Dict[str, List[Union[int, float]]],
    weights: Optional[List[float]] = None,
    method: str = "weighted",
    show_all_methods: bool = False,
) -> Union[DecisionResult, Dict[str, DecisionResult]]:
    """
    Make a decision using a decision matrix.

    Args:
        options: List of option names to compare
        criteria: List of criteria to evaluate against
        scores: Dictionary mapping option names to lists of scores
        weights: Optional weights for each criterion (defaults to equal)
        method: Analysis method - 'weighted', 'normalized', 'ranking', 'best_worst'
        show_all_methods: If True, run all methods and return comparison

    Returns:
        DecisionResult with rankings and analysis, or dict of all methods if
        show_all_methods=True

    Example:
        >>> result = make_decision(
        ...     options=["Python", "JavaScript", "Go"],
        ...     criteria=["Learning Curve", "Performance", "Community"],
        ...     scores={
        ...         "Python": [9, 7, 10],
        ...         "JavaScript": [8, 6, 9],
        ...         "Go": [6, 9, 7]
        ...     },
        ...     weights=[0.3, 0.4, 0.3]
        ... )
        >>> print(result)
    """
    if show_all_methods:
        results = {}
        for method_name in ["weighted", "normalized", "ranking", "best_worst"]:
            matrix = DecisionMatrix(
                options, criteria, scores, weights, method_name
            )
            results[method_name] = matrix.analyze()
        return results
    else:
        matrix = DecisionMatrix(options, criteria, scores, weights, method)
        return matrix.analyze()


def compare_methods(
    options: List[str],
    criteria: List[str],
    scores: Dict[str, List[Union[int, float]]],
    weights: Optional[List[float]] = None,
) -> str:
    """
    Compare results across all analysis methods.

    Returns a formatted comparison of all methods.
    """
    results = make_decision(
        options, criteria, scores, weights, show_all_methods=True
    )

    lines = [
        "=" * 70,
        "DECISION MATRIX - METHOD COMPARISON",
        "=" * 70,
    ]

    for method_name, result in results.items():
        lines.append(f"\n{method_name.upper()} METHOD:")
        lines.append(f"  Winner: {result.winner}")
        lines.append(f"  Confidence: {result.confidence_score:.1f}%")
        lines.append("  Top 3:")
        for i, (opt, score) in enumerate(result.rankings[:3], 1):
            lines.append(f"    {i}. {opt}: {score:.2f}")

    # Consensus check
    lines.append("\n" + "=" * 70)
    winners = [result.winner for result in results.values()]
    winner_counts = {w: winners.count(w) for w in set(winners)}
    consensus = max(winner_counts.items(), key=lambda x: x[1])

    lines.append(f"CONSENSUS: {consensus[0]} ({consensus[1]}/4 methods)")
    lines.append("=" * 70)

    return "\n".join(lines)
