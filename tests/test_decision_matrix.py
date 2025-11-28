"""
Tests for Decision Matrix utility
"""

import pytest
from novasystem.core_utils import (
    make_decision,
    compare_methods,
    DecisionMatrix,
    DecisionResult,
)


class TestDecisionMatrix:
    """Test DecisionMatrix class."""

    def test_basic_decision_matrix(self):
        """Test basic decision matrix creation and analysis."""
        options = ["Option A", "Option B", "Option C"]
        criteria = ["Cost", "Speed", "Quality"]
        scores = {
            "Option A": [7, 8, 6],
            "Option B": [9, 5, 7],
            "Option C": [6, 9, 8],
        }

        matrix = DecisionMatrix(options, criteria, scores)
        result = matrix.analyze()

        assert isinstance(result, DecisionResult)
        assert result.winner in options
        assert len(result.rankings) == 3
        assert all(opt in options for opt, _ in result.rankings)

    def test_weighted_decision(self):
        """Test weighted decision matrix."""
        options = ["Python", "JavaScript", "Go"]
        criteria = ["Learning Curve", "Performance", "Community"]
        scores = {
            "Python": [9, 7, 10],
            "JavaScript": [8, 6, 9],
            "Go": [6, 9, 7],
        }
        weights = [0.3, 0.4, 0.3]

        matrix = DecisionMatrix(options, criteria, scores, weights)
        result = matrix.analyze()

        assert result.winner in options
        assert len(result.rankings) == 3
        assert 0 <= result.confidence_score <= 100

    def test_validation_missing_option_scores(self):
        """Test validation catches missing scores."""
        options = ["A", "B", "C"]
        criteria = ["X", "Y"]
        scores = {"A": [1, 2], "B": [3, 4]}  # Missing C

        with pytest.raises(ValueError, match="Missing scores for option"):
            DecisionMatrix(options, criteria, scores)

    def test_validation_wrong_score_count(self):
        """Test validation catches wrong number of scores."""
        options = ["A", "B"]
        criteria = ["X", "Y", "Z"]
        scores = {"A": [1, 2], "B": [3, 4]}  # Only 2 scores, need 3

        with pytest.raises(ValueError, match="has .* scores but .* criteria"):
            DecisionMatrix(options, criteria, scores)

    def test_validation_empty_inputs(self):
        """Test validation catches empty inputs."""
        with pytest.raises(ValueError):
            DecisionMatrix([], ["X"], {"A": [1]})

        with pytest.raises(ValueError):
            DecisionMatrix(["A"], [], {"A": []})

        with pytest.raises(ValueError):
            DecisionMatrix(["A"], ["X"], {})

    def test_equal_weights_default(self):
        """Test that equal weights are used by default."""
        options = ["A", "B"]
        criteria = ["X", "Y", "Z"]
        scores = {"A": [1, 2, 3], "B": [4, 5, 6]}

        matrix = DecisionMatrix(options, criteria, scores)

        assert len(matrix.weights) == 3
        assert all(abs(w - 1 / 3) < 0.001 for w in matrix.weights)

    def test_weight_normalization(self):
        """Test that weights are normalized to sum to 1."""
        options = ["A", "B"]
        criteria = ["X", "Y"]
        scores = {"A": [1, 2], "B": [3, 4]}
        weights = [2, 3]  # Sum is 5, should normalize to 0.4, 0.6

        matrix = DecisionMatrix(options, criteria, scores, weights)

        assert abs(sum(matrix.weights) - 1.0) < 0.001
        assert abs(matrix.weights[0] - 0.4) < 0.001
        assert abs(matrix.weights[1] - 0.6) < 0.001

    def test_normalized_method(self):
        """Test normalized scoring method."""
        options = ["A", "B", "C"]
        criteria = ["X", "Y"]
        scores = {"A": [10, 5], "B": [20, 10], "C": [15, 7]}

        matrix = DecisionMatrix(
            options, criteria, scores, method="normalized"
        )
        result = matrix.analyze()

        assert result.analysis_method == "Normalized Score (0-100)"
        assert result.winner in options
        assert all(0 <= score <= 100 for score in result.total_score.values())

    def test_ranking_method(self):
        """Test ranking method."""
        options = ["A", "B", "C"]
        criteria = ["X", "Y"]
        scores = {"A": [10, 5], "B": [20, 10], "C": [15, 7]}

        matrix = DecisionMatrix(options, criteria, scores, method="ranking")
        result = matrix.analyze()

        assert result.analysis_method == "Ranking Method"
        assert result.winner in options

    def test_best_worst_method(self):
        """Test best-worst scaling method."""
        options = ["A", "B", "C"]
        criteria = ["X", "Y"]
        scores = {"A": [10, 5], "B": [20, 10], "C": [15, 7]}

        matrix = DecisionMatrix(
            options, criteria, scores, method="best_worst"
        )
        result = matrix.analyze()

        assert result.analysis_method == "Best-Worst Scaling"
        assert result.winner in options

    def test_invalid_method(self):
        """Test that invalid method raises error."""
        options = ["A", "B"]
        criteria = ["X"]
        scores = {"A": [1], "B": [2]}

        matrix = DecisionMatrix(
            options, criteria, scores, method="invalid_method"
        )

        with pytest.raises(ValueError, match="Unknown analysis method"):
            matrix.analyze()


class TestMakeDecisionFunction:
    """Test make_decision convenience function."""

    def test_make_decision_basic(self):
        """Test basic make_decision call."""
        result = make_decision(
            options=["A", "B", "C"],
            criteria=["X", "Y"],
            scores={"A": [7, 8], "B": [9, 5], "C": [6, 9]},
        )

        assert isinstance(result, DecisionResult)
        assert result.winner in ["A", "B", "C"]

    def test_make_decision_with_weights(self):
        """Test make_decision with custom weights."""
        result = make_decision(
            options=["A", "B"],
            criteria=["X", "Y", "Z"],
            scores={"A": [1, 2, 3], "B": [4, 5, 6]},
            weights=[0.5, 0.3, 0.2],
        )

        assert isinstance(result, DecisionResult)
        assert result.winner in ["A", "B"]

    def test_make_decision_different_methods(self):
        """Test make_decision with different methods."""
        options = ["A", "B", "C"]
        criteria = ["X", "Y"]
        scores = {"A": [7, 8], "B": [9, 5], "C": [6, 9]}

        for method in ["weighted", "normalized", "ranking", "best_worst"]:
            result = make_decision(
                options=options, criteria=criteria, scores=scores, method=method
            )
            assert isinstance(result, DecisionResult)
            assert result.winner in options

    def test_make_decision_show_all_methods(self):
        """Test make_decision with show_all_methods=True."""
        results = make_decision(
            options=["A", "B"],
            criteria=["X", "Y"],
            scores={"A": [7, 8], "B": [9, 5]},
            show_all_methods=True,
        )

        assert isinstance(results, dict)
        assert len(results) == 4
        assert all(
            method in results
            for method in ["weighted", "normalized", "ranking", "best_worst"]
        )
        assert all(isinstance(r, DecisionResult) for r in results.values())


class TestDecisionResult:
    """Test DecisionResult class."""

    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        result = make_decision(
            options=["A", "B"],
            criteria=["X", "Y"],
            scores={"A": [7, 8], "B": [9, 5]},
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert "winner" in result_dict
        assert "rankings" in result_dict
        assert "scores_breakdown" in result_dict
        assert "confidence_score" in result_dict

    def test_result_to_json(self):
        """Test converting result to JSON."""
        result = make_decision(
            options=["A", "B"],
            criteria=["X", "Y"],
            scores={"A": [7, 8], "B": [9, 5]},
        )

        json_str = result.to_json()

        assert isinstance(json_str, str)
        assert "winner" in json_str
        assert "rankings" in json_str

    def test_result_str_formatting(self):
        """Test string formatting of result."""
        result = make_decision(
            options=["Python", "JavaScript"],
            criteria=["Performance", "Community"],
            scores={"Python": [8, 10], "JavaScript": [7, 9]},
        )

        result_str = str(result)

        assert "DECISION MATRIX RESULTS" in result_str
        assert "WINNER:" in result_str
        assert "RANKINGS:" in result_str
        assert "RECOMMENDATION:" in result_str

    def test_confidence_levels(self):
        """Test confidence score calculation."""
        # High confidence (clear winner)
        result_high = make_decision(
            options=["A", "B"],
            criteria=["X"],
            scores={"A": [10], "B": [1]},
        )
        assert result_high.confidence_score > 70

        # Low confidence (close scores)
        result_low = make_decision(
            options=["A", "B"],
            criteria=["X"],
            scores={"A": [10], "B": [9.5]},
        )
        assert result_low.confidence_score < 30

    def test_recommendation_text(self):
        """Test recommendation text generation."""
        result = make_decision(
            options=["A", "B", "C"],
            criteria=["X", "Y"],
            scores={"A": [10, 10], "B": [5, 5], "C": [3, 3]},
        )

        assert len(result.recommendation) > 0
        assert isinstance(result.recommendation, str)


class TestCompareMethodsFunction:
    """Test compare_methods function."""

    def test_compare_methods(self):
        """Test comparing multiple methods."""
        comparison = compare_methods(
            options=["A", "B", "C"],
            criteria=["X", "Y"],
            scores={"A": [7, 8], "B": [9, 5], "C": [6, 9]},
        )

        assert isinstance(comparison, str)
        assert "METHOD COMPARISON" in comparison
        assert "CONSENSUS:" in comparison

    def test_compare_methods_with_weights(self):
        """Test comparing methods with custom weights."""
        comparison = compare_methods(
            options=["A", "B"],
            criteria=["X", "Y", "Z"],
            scores={"A": [1, 2, 3], "B": [4, 5, 6]},
            weights=[0.5, 0.3, 0.2],
        )

        assert isinstance(comparison, str)
        assert "WEIGHTED METHOD:" in comparison
        assert "NORMALIZED METHOD:" in comparison
        assert "RANKING METHOD:" in comparison
        assert "BEST_WORST METHOD:" in comparison


class TestRealWorldScenarios:
    """Test real-world decision-making scenarios."""

    def test_technology_selection(self):
        """Test selecting a technology stack."""
        result = make_decision(
            options=["Python", "JavaScript", "Go", "Rust"],
            criteria=[
                "Learning Curve",
                "Performance",
                "Community Support",
                "Job Market",
            ],
            scores={
                "Python": [9, 7, 10, 10],
                "JavaScript": [8, 6, 9, 10],
                "Go": [6, 9, 7, 8],
                "Rust": [4, 10, 6, 7],
            },
            weights=[0.2, 0.3, 0.2, 0.3],
        )

        assert result.winner in ["Python", "JavaScript", "Go", "Rust"]
        assert len(result.rankings) == 4

    def test_vendor_selection(self):
        """Test selecting a vendor."""
        result = make_decision(
            options=["Vendor A", "Vendor B", "Vendor C"],
            criteria=["Price", "Quality", "Delivery Time", "Support"],
            scores={
                "Vendor A": [8, 7, 6, 9],
                "Vendor B": [6, 9, 8, 7],
                "Vendor C": [7, 8, 9, 8],
            },
            weights=[0.4, 0.3, 0.2, 0.1],
        )

        assert result.winner in ["Vendor A", "Vendor B", "Vendor C"]

    def test_hiring_decision(self):
        """Test candidate selection."""
        result = make_decision(
            options=["Candidate 1", "Candidate 2", "Candidate 3"],
            criteria=["Technical Skills", "Experience", "Culture Fit", "Salary"],
            scores={
                "Candidate 1": [9, 8, 7, 6],
                "Candidate 2": [7, 9, 9, 8],
                "Candidate 3": [8, 7, 8, 7],
            },
            weights=[0.4, 0.3, 0.2, 0.1],
        )

        assert result.winner in ["Candidate 1", "Candidate 2", "Candidate 3"]
        assert 0 <= result.confidence_score <= 100

    def test_project_prioritization(self):
        """Test project prioritization."""
        comparison = compare_methods(
            options=["Project X", "Project Y", "Project Z"],
            criteria=["ROI", "Effort", "Risk", "Strategic Value"],
            scores={
                "Project X": [8, 3, 7, 9],
                "Project Y": [7, 5, 8, 7],
                "Project Z": [9, 2, 6, 8],
            },
            weights=[0.3, 0.2, 0.2, 0.3],
        )

        assert "CONSENSUS:" in comparison

    def test_edge_case_single_option(self):
        """Test with single option (should always win)."""
        result = make_decision(
            options=["Only Option"],
            criteria=["X", "Y"],
            scores={"Only Option": [5, 5]},
        )

        assert result.winner == "Only Option"
        assert result.confidence_score == 100.0

    def test_edge_case_tied_scores(self):
        """Test with identical scores."""
        result = make_decision(
            options=["A", "B", "C"],
            criteria=["X", "Y"],
            scores={"A": [5, 5], "B": [5, 5], "C": [5, 5]},
        )

        assert result.winner in ["A", "B", "C"]
        # Confidence should be low for tied scores
        assert result.confidence_score < 1.0

    def test_extreme_values(self):
        """Test with extreme score values."""
        result = make_decision(
            options=["A", "B"],
            criteria=["X"],
            scores={"A": [1000], "B": [1]},
        )

        assert result.winner == "A"
        assert result.confidence_score > 90
