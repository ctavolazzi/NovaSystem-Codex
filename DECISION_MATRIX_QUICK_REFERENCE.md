# Decision Matrix - Quick Reference Card

**Version:** 2.0 | **Status:** Production Ready | **Tests:** 37/37 Passing

---

## 🚀 Quick Start

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
    weights=[0.3, 0.5, 0.2]  # Optional
)

print(result)
```

### 💻 CLI Quick Start

```bash
# Create example input
python -m novasystem.core_utils.decision_matrix_cli --example my_decision.json

# Run analysis
python -m novasystem.core_utils.decision_matrix_cli my_decision.json

# Compare methods or output JSON
python -m novasystem.core_utils.decision_matrix_cli my_decision.json --compare
python -m novasystem.core_utils.decision_matrix_cli my_decision.json --json
```

**See:** `DECISION_MATRIX_CLI.md` for complete CLI reference.

---

## 📋 Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `options` | List[str] | **Required** | Names of options to compare |
| `criteria` | List[str] | **Required** | Criteria to evaluate against |
| `scores` | Dict | **Required** | `{option: [scores]}` mapping |
| `weights` | List[float] | Equal | Importance of each criterion (0-1, sum to 1) |
| `method` | str | "weighted" | Analysis method (see below) |
| `show_all_methods` | bool | False | Run all 4 methods |
| `top_n` | int | None | Show only top N options |

---

## 🎯 Methods

| Method | Best For | Output Scale |
|--------|----------|--------------|
| `weighted` | General use, default | Weighted sum |
| `normalized` | Different score scales | 0-100 per criterion |
| `ranking` | Ordinal data | Rank-based |
| `best_worst` | Relative comparison | 0-1 scaled |

**Usage:**
```python
result = make_decision(..., method="normalized")
```

---

## 🔍 Result Object

### Attributes
```python
result.winner              # str: Winning option
result.confidence_score    # float: 0-100 confidence
result.rankings            # List[(option, score)]
result.recommendation      # str: Recommendation text
result.why_winner_won      # str: Explanation
result.strengths           # Dict: Top strengths per option
result.weaknesses          # Dict: Weaknesses per option
result.scores_breakdown    # Dict: Detailed scores
```

### Methods
```python
result.comparison_table()  # Side-by-side table
result.to_dict()          # Export as dict
result.to_json()          # Export as JSON
str(result)               # Formatted output
```

---

## 💡 Common Patterns

### 1. Basic Decision
```python
result = make_decision(
    options=["A", "B"],
    criteria=["X", "Y"],
    scores={"A": [7, 8], "B": [9, 5]}
)
```

### 2. Weighted Decision
```python
result = make_decision(
    options=["A", "B"],
    criteria=["Price", "Quality"],
    scores={"A": [8, 6], "B": [5, 9]},
    weights=[0.7, 0.3]  # Price matters more
)
```

### 3. Show Only Top 3
```python
result = make_decision(
    options=[...],  # 10 options
    criteria=[...],
    scores={...},
    top_n=3  # Display only top 3
)
```

### 4. Compare All Methods
```python
results = make_decision(
    options=[...],
    criteria=[...],
    scores={...},
    show_all_methods=True
)

for method, result in results.items():
    print(f"{method}: {result.winner}")
```

### 5. View Comparison Table
```python
result = make_decision(...)
print(result.comparison_table())
```

---

## 📊 Output Features

### Standard Output
```
🏆 WINNER: Option A
   Confidence: 75.0%

✨ WHY OPTION A WON:
   Excelled in Quality (50% weight, +2.5 points)

📊 RANKINGS:
   1. Option A    Score: 8.50 (100.0%)
      💪 Strengths: Quality (9.0), Speed (8.5)
      ⚠️  Weaknesses: Price (5.0)

💡 RECOMMENDATION:
   Strong recommendation: 'Option A' clearly outperforms...
```

### Comparison Table
```python
result.comparison_table()
```
```
Criterion    | Option A | Option B | Winner
Quality      |   9.0    |   6.0    | Option A
Price        |   5.0    |   9.0    | Option B
```

---

## 🎨 Confidence Levels

| Confidence | Level | Meaning |
|------------|-------|---------|
| >55% | **Strong** | Clear winner |
| 30-55% | **Moderate** | Good choice, consider runner-up |
| <30% | **Weak** | Close race, more analysis needed |

---

## 📦 Export & Integration

### JSON Export
```python
json_str = result.to_json()
# Use in API response, save to file, etc.
```

### Dict Export
```python
data = result.to_dict()
# Use in database, DataFrame, etc.
```

### Keys in Export
- `winner`, `confidence_score`, `recommendation`
- `rankings`, `scores_breakdown`, `total_score`
- `strengths`, `weaknesses`, `why_winner_won`
- `analysis_method`, `normalized_scores`, `top_n`

---

## 🔧 Advanced Usage

### Compare Methods
```python
from novasystem.core_utils import compare_methods

comparison = compare_methods(
    options=[...],
    criteria=[...],
    scores={...}
)
print(comparison)  # Shows consensus
```

### Access All Data
```python
# Get detailed breakdown
for option, scores in result.scores_breakdown.items():
    print(f"{option}: {scores}")

# Get strengths
for option, strengths in result.strengths.items():
    print(f"{option} strengths: {strengths}")
```

---

## ✅ Validation

### Automatic Checks
- ✅ All options have scores
- ✅ Score count matches criteria count
- ✅ Weights normalize to 1.0
- ✅ Non-empty inputs

### Error Handling
```python
try:
    result = make_decision(...)
except ValueError as e:
    print(f"Invalid input: {e}")
```

---

## 🎯 Best Practices

### DO ✅
- Use consistent scoring scale (e.g., 1-10)
- Weight criteria by importance
- Compare similar options
- Check confidence before deciding
- Use `top_n` for many options (>5)

### DON'T ❌
- Mix different scales without normalization
- Use for binary yes/no decisions
- Ignore low confidence warnings
- Over-weight single criteria (>0.6)

---

## 🔥 Pro Tips

1. **Tie-Breaker:** Low confidence? Add another criterion
2. **Sensitivity:** Change weights slightly, see if winner changes
3. **Visual:** Use `comparison_table()` to spot patterns
4. **Multiple Views:** Try different methods for same data
5. **Documentation:** Use `why_winner_won` to justify decisions

---

## 📚 Real-World Examples

### Technology Selection
```python
make_decision(
    options=["Python", "JavaScript", "Go"],
    criteria=["Learning", "Performance", "Jobs"],
    scores={
        "Python": [9, 7, 10],
        "JavaScript": [8, 6, 9],
        "Go": [6, 9, 8]
    },
    weights=[0.3, 0.4, 0.3]
)
```

### Vendor Selection
```python
make_decision(
    options=["Vendor A", "Vendor B", "Vendor C"],
    criteria=["Price", "Quality", "Support"],
    scores={
        "Vendor A": [8, 7, 9],
        "Vendor B": [6, 9, 7],
        "Vendor C": [7, 8, 8]
    },
    weights=[0.5, 0.3, 0.2]
)
```

### Hiring Decision
```python
make_decision(
    options=["Alice", "Bob", "Carol"],
    criteria=["Skills", "Experience", "Fit"],
    scores={
        "Alice": [9, 5, 8],
        "Bob": [7, 9, 7],
        "Carol": [8, 7, 9]
    },
    weights=[0.4, 0.3, 0.3]
)
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing scores for option" | Ensure all options in `scores` dict |
| "Wrong score count" | Match scores length to criteria length |
| Low confidence on clear winner | Expected for close scores, add criteria |
| All options look same | Check if weights too equal, vary them |

---

## 📖 Full Documentation

- **User Guide:** `DECISION_MATRIX_README.md`
- **Test Report:** `DECISION_MATRIX_TEST_REPORT.md`
- **Enhancements:** `DECISION_MATRIX_ENHANCEMENTS.md`
- **Examples:** `examples/decision_matrix_examples.py`
- **Tests:** `tests/test_decision_matrix.py`

---

## 🚦 Quick Decision Tree

```
Do you have 2+ options to compare?
├─ YES → Do you have quantifiable criteria?
│  ├─ YES → Do some criteria matter more?
│  │  ├─ YES → Use weights
│  │  └─ NO → Use equal weights (default)
│  └─ NO → Decision matrix may not be suitable
└─ NO → No need for decision matrix
```

---

## 💻 Import Paths

```python
# Recommended
from novasystem.core_utils import make_decision, compare_methods

# Alternative
from novasystem.core_utils import DecisionMatrix, DecisionResult

# Direct
from novasystem.core_utils.decision_matrix import make_decision
```

---

## 🎓 Learning Path

1. **Beginner:** Start with basic 2-3 options, equal weights
2. **Intermediate:** Add custom weights, try different methods
3. **Advanced:** Use `top_n`, export data, compare methods
4. **Expert:** Build workflows, integrate with systems

---

**Quick Start Command:**
```bash
python -c "from novasystem.core_utils import make_decision; help(make_decision)"
```

**Run Examples:**
```bash
python examples/decision_matrix_examples.py
```

**Run Tests:**
```bash
pytest tests/test_decision_matrix.py -v
```

---

**Version:** 2.0 Enhanced | **License:** Part of NovaSystem | **Tests:** 37/37 ✅
