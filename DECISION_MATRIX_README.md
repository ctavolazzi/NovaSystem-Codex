# Decision Matrix Utility

A comprehensive decision-making tool for quantifying and comparing options against multiple criteria.

## Quick Start

```python
from novasystem.core_utils import make_decision

result = make_decision(
    options=["Option A", "Option B", "Option C"],
    criteria=["Cost", "Quality", "Speed"],
    scores={
        "Option A": [7, 8, 6],
        "Option B": [9, 5, 7],
        "Option C": [6, 9, 8]
    },
    weights=[0.3, 0.5, 0.2]  # Optional: importance of each criterion
)

print(result)  # Beautiful formatted output with recommendations
```

## Features

### 🎯 Multiple Analysis Methods

1. **Weighted Score** (default) - Traditional weighted decision matrix
2. **Normalized Score** - Scales all scores to 0-100 range
3. **Ranking Method** - Converts scores to rankings per criterion
4. **Best-Worst Scaling** - Compares each option to best and worst possible

### 📊 Rich Output

- Clear winner identification
- Confidence scoring
- Detailed rankings
- Criterion-by-criterion breakdown
- Actionable recommendations
- JSON/Dict export for further analysis

### 🔧 Flexible Input

- Optional criterion weighting
- Automatic weight normalization
- Support for any number of options and criteria
- Validation and helpful error messages

### 💻 Command-Line Interface

Use the decision matrix from the terminal, scripts, or CI/CD pipelines:

```bash
# Create example input file
python -m novasystem.core_utils.decision_matrix_cli --example my_decision.json

# Run analysis
python -m novasystem.core_utils.decision_matrix_cli my_decision.json

# Compare all methods
python -m novasystem.core_utils.decision_matrix_cli my_decision.json --compare

# JSON output for piping
python -m novasystem.core_utils.decision_matrix_cli my_decision.json --json
```

**See:** `DECISION_MATRIX_CLI.md` for complete CLI documentation and examples.

## Usage Examples

### Basic Usage

```python
from novasystem.core_utils import make_decision

# Simple technology selection
result = make_decision(
    options=["Python", "JavaScript", "Go"],
    criteria=["Learning Curve", "Performance", "Community"],
    scores={
        "Python": [9, 7, 10],
        "JavaScript": [8, 6, 9],
        "Go": [6, 9, 7]
    }
)

print(result)
```

Output:
```
======================================================================
DECISION MATRIX RESULTS (Weighted Score)
======================================================================

🏆 WINNER: Python
   Confidence: 11.5%

📊 RANKINGS:
   1. Python               Score:   8.67 (100.0%)
   2. JavaScript           Score:   7.67 ( 88.5%)
   3. Go                   Score:   7.33 ( 84.6%)

💡 RECOMMENDATION:
   Weak recommendation: Options are closely matched...
```

### Weighted Criteria

```python
# Vendor selection with weighted criteria
result = make_decision(
    options=["Vendor A", "Vendor B", "Vendor C"],
    criteria=["Price", "Quality", "Delivery", "Support"],
    scores={
        "Vendor A": [8, 7, 6, 9],
        "Vendor B": [6, 9, 8, 7],
        "Vendor C": [7, 8, 9, 8]
    },
    weights=[0.4, 0.3, 0.2, 0.1]  # Price is most important (40%)
)
```

### Different Analysis Methods

```python
# Try different methods
for method in ["weighted", "normalized", "ranking", "best_worst"]:
    result = make_decision(
        options=["A", "B", "C"],
        criteria=["X", "Y"],
        scores={"A": [7, 8], "B": [9, 5], "C": [6, 9]},
        method=method
    )
    print(f"{method}: Winner = {result.winner}")
```

### Compare All Methods

```python
from novasystem.core_utils import compare_methods

# See which option wins across all methods
comparison = compare_methods(
    options=["Option 1", "Option 2", "Option 3"],
    criteria=["Criterion A", "Criterion B"],
    scores={
        "Option 1": [8, 7],
        "Option 2": [7, 9],
        "Option 3": [9, 6]
    }
)

print(comparison)  # Shows consensus across methods
```

### Get All Method Results

```python
results = make_decision(
    options=["A", "B", "C"],
    criteria=["X", "Y"],
    scores={"A": [7, 8], "B": [9, 5], "C": [6, 9]},
    show_all_methods=True  # Returns dict of all 4 methods
)

# Access individual results
print(results["weighted"].winner)
print(results["normalized"].winner)
```

### Export Results

```python
result = make_decision(...)

# Export as dictionary
data = result.to_dict()

# Export as JSON
json_str = result.to_json()

# Use in your application
save_to_database(data)
send_to_api(json_str)
```

## Real-World Use Cases

### 1. Technology Stack Selection

```python
result = make_decision(
    options=["Python", "JavaScript", "Go", "Rust"],
    criteria=["Learning Curve", "Performance", "Community", "Jobs"],
    scores={
        "Python": [9, 7, 10, 10],
        "JavaScript": [8, 6, 9, 10],
        "Go": [6, 9, 7, 8],
        "Rust": [4, 10, 6, 7]
    },
    weights=[0.2, 0.3, 0.2, 0.3]
)
```

### 2. Vendor Selection

```python
result = make_decision(
    options=["Vendor A", "Vendor B", "Vendor C"],
    criteria=["Price", "Quality", "Delivery Time", "Support"],
    scores={
        "Vendor A": [8, 7, 6, 9],
        "Vendor B": [6, 9, 8, 7],
        "Vendor C": [7, 8, 9, 8]
    },
    weights=[0.4, 0.3, 0.2, 0.1]
)
```

### 3. Hiring Decision

```python
result = make_decision(
    options=["Candidate A", "Candidate B", "Candidate C"],
    criteria=["Technical Skills", "Experience", "Culture Fit", "Salary"],
    scores={
        "Candidate A": [9, 5, 8, 6],
        "Candidate B": [7, 9, 9, 4],
        "Candidate C": [8, 7, 7, 7]
    },
    weights=[0.4, 0.3, 0.2, 0.1]
)
```

### 4. Project Prioritization

```python
result = make_decision(
    options=["Project X", "Project Y", "Project Z"],
    criteria=["ROI", "Effort (inverse)", "Risk (inverse)", "Strategic Value"],
    scores={
        "Project X": [8, 4, 7, 9],
        "Project Y": [7, 7, 8, 6],
        "Project Z": [9, 3, 6, 8]
    },
    weights=[0.3, 0.2, 0.2, 0.3]
)
```

### 5. Feature Comparison

```python
result = make_decision(
    options=["AWS", "Google Cloud", "Azure", "DigitalOcean"],
    criteria=["Pricing", "Services", "Ease of Use", "Docs", "Performance"],
    scores={
        "AWS": [6, 10, 6, 8, 9],
        "Google Cloud": [7, 9, 7, 9, 9],
        "Azure": [6, 9, 6, 7, 9],
        "DigitalOcean": [9, 6, 9, 8, 7]
    },
    weights=[0.25, 0.25, 0.20, 0.15, 0.15]
)
```

## Advanced Features

### Confidence Scoring

The decision matrix calculates a confidence score (0-100%) based on the gap between the top two options:

- **>70%**: Strong recommendation - clear winner
- **40-70%**: Moderate recommendation - winner is best but consider runner-up
- **<40%**: Weak recommendation - options are closely matched

### Automatic Recommendations

Based on confidence scores, the system generates actionable recommendations:

```python
result = make_decision(...)
print(result.recommendation)
# "Strong recommendation: 'Option A' clearly outperforms other options with 95.2% score."
```

### Normalization

Weights are automatically normalized to sum to 1.0:

```python
weights = [2, 3, 5]  # Will be normalized to [0.2, 0.3, 0.5]
```

## API Reference

### `make_decision()`

Main function for decision-making.

**Parameters:**
- `options` (List[str]): List of option names to compare
- `criteria` (List[str]): List of criteria to evaluate against
- `scores` (Dict[str, List[float]]): Dictionary mapping option names to score lists
- `weights` (Optional[List[float]]): Weights for each criterion (defaults to equal)
- `method` (str): Analysis method - 'weighted', 'normalized', 'ranking', 'best_worst'
- `show_all_methods` (bool): If True, returns results from all methods

**Returns:**
- `DecisionResult` or `Dict[str, DecisionResult]` if show_all_methods=True

### `compare_methods()`

Compare results across all analysis methods.

**Parameters:**
- Same as `make_decision()` except no `method` or `show_all_methods`

**Returns:**
- `str`: Formatted comparison of all methods with consensus

### `DecisionResult`

Result object with attributes:
- `winner` (str): Winning option
- `rankings` (List[Tuple[str, float]]): Sorted list of (option, score)
- `scores_breakdown` (Dict): Detailed breakdown by criterion
- `confidence_score` (float): Confidence percentage (0-100)
- `recommendation` (str): Generated recommendation text
- `to_dict()`: Export as dictionary
- `to_json()`: Export as JSON string

## Tips for Best Results

1. **Score Consistently**: Use the same scale for all criteria (e.g., 1-10)
2. **Weight Thoughtfully**: Higher weights = more important criteria
3. **Consider Multiple Methods**: Different methods may reveal different insights
4. **Check Confidence**: Low confidence means options are similar - consider more criteria
5. **Invert When Needed**: For "lower is better" criteria, use inverse scores

## Examples File

See `examples/decision_matrix_examples.py` for 10 comprehensive examples covering:
1. Basic usage
2. Weighted criteria
3. Method comparison
4. Project prioritization
5. Feature comparison
6. All methods at once
7. Binary decisions
8. Career decisions
9. Investment decisions
10. Custom template

Run examples:
```bash
python examples/decision_matrix_examples.py
```

## Testing

Comprehensive test suite with 29 tests:

```bash
pytest tests/test_decision_matrix.py -v
```

Tests cover:
- All analysis methods
- Input validation
- Edge cases
- Real-world scenarios
- Export functionality

## Location

- **Module**: `novasystem/core_utils/decision_matrix.py`
- **Tests**: `tests/test_decision_matrix.py`
- **Examples**: `examples/decision_matrix_examples.py`

## Import

```python
# Convenience function (recommended)
from novasystem.core_utils import make_decision, compare_methods

# Full class access
from novasystem.core_utils import DecisionMatrix, DecisionResult

# Direct import
from novasystem.core_utils.decision_matrix import make_decision
```

## License

Part of the NovaSystem project.
