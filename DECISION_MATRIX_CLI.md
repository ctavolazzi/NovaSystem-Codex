# Decision Matrix CLI - Command-Line Interface

A powerful command-line interface for the Decision Matrix utility, making data-driven decisions accessible from the terminal, scripts, and CI/CD pipelines.

---

## 🚀 Quick Start

```bash
# Create an example input file
python -m novasystem.core_utils.decision_matrix_cli --example my_decision.json

# Run analysis
python -m novasystem.core_utils.decision_matrix_cli my_decision.json

# Compare all methods
python -m novasystem.core_utils.decision_matrix_cli my_decision.json --compare
```

---

## 📥 Input Format

Create a JSON file with your decision data:

```json
{
  "options": ["Option A", "Option B", "Option C"],
  "criteria": ["Cost", "Quality", "Speed"],
  "scores": {
    "Option A": [7, 8, 6],
    "Option B": [9, 5, 7],
    "Option C": [6, 9, 8]
  },
  "weights": [0.3, 0.5, 0.2]
}
```

**Fields:**
- `options` (required): List of option names to compare
- `criteria` (required): List of criteria to evaluate
- `scores` (required): Dictionary mapping option names to score lists
- `weights` (optional): Importance weight for each criterion (defaults to equal)

---

## 💻 Usage Examples

### Basic Analysis

```bash
python -m novasystem.core_utils.decision_matrix_cli input.json
```

Output:
```
======================================================================
DECISION MATRIX RESULTS (Weighted Score)
======================================================================

🏆 WINNER: Python
   Confidence: 14.9%

✨ WHY PYTHON WON:
   Excelled in Performance (30% weight, +0.3 points)

📊 RANKINGS:
   1. Python               Score:   8.90 (100.0%)
      💪 Strengths: Job Market (3.0), Performance (2.1)
      ⚠️  Weaknesses: Performance (2.1), Community (2.0)
...
```

### Different Analysis Method

```bash
# Use normalized method (scales scores to 0-100)
python -m novasystem.core_utils.decision_matrix_cli input.json --method normalized

# Use ranking method (converts to rankings)
python -m novasystem.core_utils.decision_matrix_cli input.json --method ranking

# Use best-worst scaling
python -m novasystem.core_utils.decision_matrix_cli input.json --method best_worst
```

### Show Only Top N Options

```bash
# Show only top 3 results
python -m novasystem.core_utils.decision_matrix_cli input.json --top-n 3
```

Output shows:
```
📊 RANKINGS:
   1. Python               Score:   8.90 (100.0%)
   2. JavaScript           Score:   8.20 ( 92.1%)
   3. Go                   Score:   7.70 ( 86.5%)
   ... and 1 more option
```

### JSON Output (for scripting/piping)

```bash
python -m novasystem.core_utils.decision_matrix_cli input.json --json
```

Output:
```json
{
  "winner": "Python",
  "rankings": [["Python", 8.9], ["JavaScript", 8.2]],
  "confidence_score": 14.9,
  "recommendation": "Weak recommendation: ...",
  ...
}
```

### Comparison Table

```bash
python -m novasystem.core_utils.decision_matrix_cli input.json --table
```

Shows side-by-side comparison:
```
📊 COMPARISON TABLE:
======================================================================
Criterion                 |    Python    |  JavaScript  |      Go
--------------------------------------------------------------------------
Learning Curve            |     1.8      |     1.6      |     1.2
Performance               |     2.1      |     1.8      |     2.7
Community                 |     2.0      |     1.8      |     1.4
```

### Compare All Methods

```bash
python -m novasystem.core_utils.decision_matrix_cli input.json --compare
```

Output:
```
======================================================================
DECISION MATRIX - METHOD COMPARISON
======================================================================

WEIGHTED METHOD:
  Winner: Python
  Confidence: 14.9%

NORMALIZED METHOD:
  Winner: Python
  Confidence: 16.5%

RANKING METHOD:
  Winner: Python
  Confidence: 32.3%

BEST_WORST METHOD:
  Winner: Python
  Confidence: 21.3%

======================================================================
CONSENSUS: Python (4/4 methods)
======================================================================
```

### Read from Stdin

```bash
cat input.json | python -m novasystem.core_utils.decision_matrix_cli

# Or inline
echo '{"options": ["A", "B"], "criteria": ["X"], "scores": {"A": [7], "B": [9]}}' | \
  python -m novasystem.core_utils.decision_matrix_cli
```

### Verbose Mode

```bash
python -m novasystem.core_utils.decision_matrix_cli input.json --verbose
```

Shows progress messages on stderr:
```
Loading input...
✓ Loaded 3 options, 4 criteria
Running weighted analysis...
```

---

## 🎯 Command-Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--method` | `-m` | Analysis method: `weighted`, `normalized`, `ranking`, `best_worst` |
| `--top-n N` | `-n N` | Show only top N options |
| `--json` | `-j` | Output as JSON (for piping/scripting) |
| `--compare` | `-c` | Compare all 4 analysis methods |
| `--table` | `-t` | Show comparison table |
| `--example FILE` | `-e FILE` | Create example input file |
| `--verbose` | `-v` | Show progress messages |
| `--help` | `-h` | Show help message |

---

## 📋 Real-World Use Cases

### 1. CI/CD Integration

```yaml
# .github/workflows/decide.yml
- name: Evaluate deployment options
  run: |
    python -m novasystem.core_utils.decision_matrix_cli deploy_options.json --json > result.json
    WINNER=$(jq -r '.winner' result.json)
    echo "Deploying to: $WINNER"
```

### 2. Batch Processing

```bash
# Analyze multiple decisions
for file in decisions/*.json; do
  echo "Analyzing $file..."
  python -m novasystem.core_utils.decision_matrix_cli "$file" --json >> results.jsonl
done
```

### 3. Interactive Shell Scripts

```bash
#!/bin/bash
# ask_user_for_decision.sh

echo "Creating decision input..."
cat > temp_decision.json <<EOF
{
  "options": ["$1", "$2", "$3"],
  "criteria": ["Cost", "Quality"],
  "scores": {
    "$1": [8, 7],
    "$2": [6, 9],
    "$3": [7, 8]
  }
}
EOF

python -m novasystem.core_utils.decision_matrix_cli temp_decision.json
```

### 4. Data Pipeline

```bash
# Generate decision data from database
psql -c "SELECT * FROM options" -t -A -F',' | \
  python convert_to_decision_json.py | \
  python -m novasystem.core_utils.decision_matrix_cli --json | \
  python process_decision.py
```

### 5. Quick Decision Making

```bash
# Create, analyze, and decide in one line
python -m novasystem.core_utils.decision_matrix_cli --example quick.json && \
  python -m novasystem.core_utils.decision_matrix_cli quick.json --top-n 1
```

---

## 🔧 Advanced Usage

### Combining Multiple Outputs

```bash
# Get both formatted and JSON output
python -m novasystem.core_utils.decision_matrix_cli input.json > formatted.txt
python -m novasystem.core_utils.decision_matrix_cli input.json --json > result.json
```

### Extract Specific Data with jq

```bash
# Get just the winner
python -m novasystem.core_utils.decision_matrix_cli input.json --json | jq -r '.winner'

# Get confidence score
python -m novasystem.core_utils.decision_matrix_cli input.json --json | jq '.confidence_score'

# Get top 3 options
python -m novasystem.core_utils.decision_matrix_cli input.json --json | jq '.rankings[:3]'
```

### Compare Methods Programmatically

```bash
# Get all methods as JSON
python -m novasystem.core_utils.decision_matrix_cli input.json --compare --json > all_methods.json

# Extract consensus
jq -r '.weighted.winner' all_methods.json
```

### Create Alias for Common Usage

```bash
# Add to ~/.bashrc or ~/.zshrc
alias decide='python -m novasystem.core_utils.decision_matrix_cli'

# Now use it simply
decide my_options.json
decide my_options.json --compare
decide --example new_decision.json
```

---

## 📊 Input Validation

The CLI validates all input and provides helpful error messages:

**Missing Required Field:**
```bash
$ python -m novasystem.core_utils.decision_matrix_cli bad_input.json
❌ Invalid input: Missing required fields: criteria
```

**Invalid JSON:**
```bash
$ python -m novasystem.core_utils.decision_matrix_cli broken.json
❌ Invalid JSON: Expecting ',' delimiter: line 5 column 3 (char 87)
```

**Missing Option Scores:**
```bash
$ python -m novasystem.core_utils.decision_matrix_cli incomplete.json
❌ Invalid input: Missing scores for option: Option C
```

**File Not Found:**
```bash
$ python -m novasystem.core_utils.decision_matrix_cli missing.json
❌ Error: Input file not found: missing.json
```

---

## 🎨 Output Formats

### 1. Formatted (default)
Beautiful, human-readable output with:
- Winner identification
- Confidence scores
- Why winner won
- Strengths/weaknesses per option
- Rankings
- Detailed breakdowns
- Recommendations

### 2. JSON (`--json`)
Machine-readable output with all data:
- Easy to parse with tools like `jq`
- Perfect for piping to other scripts
- Integration with APIs and databases
- Can be re-imported for analysis

### 3. Comparison Table (`--table`)
Side-by-side criterion comparison:
- Shows all options across all criteria
- Identifies winner per criterion
- Easy to spot patterns and trade-offs
- Printable format for meetings

### 4. Method Comparison (`--compare`)
Shows results from all 4 methods:
- Identifies consensus across methods
- Shows confidence per method
- Helps validate decision robustness
- Can output as JSON for further analysis

---

## 💡 Tips & Best Practices

### ✅ DO:

1. **Use `--example` to start**: Creates a template with proper structure
2. **Validate with `--verbose`**: Shows what's being loaded and processed
3. **Use `--json` for automation**: Machine-readable output for scripts
4. **Try `--compare` for important decisions**: Validates across methods
5. **Use `--top-n` for many options**: Reduces clutter when comparing 10+ options

### ❌ DON'T:

1. **Mix score scales**: Use consistent 1-10 or 1-100 across all criteria
2. **Forget weights**: Important criteria should have higher weights
3. **Ignore low confidence**: If <30%, consider adding more criteria
4. **Use for binary decisions**: Overkill for simple yes/no choices

---

## 🚀 Quick Reference

```bash
# Most Common Commands

# Create example
python -m novasystem.core_utils.decision_matrix_cli --example decision.json

# Basic analysis
python -m novasystem.core_utils.decision_matrix_cli decision.json

# With comparison table
python -m novasystem.core_utils.decision_matrix_cli decision.json --table

# Compare all methods
python -m novasystem.core_utils.decision_matrix_cli decision.json --compare

# JSON output
python -m novasystem.core_utils.decision_matrix_cli decision.json --json

# Show top 3 only
python -m novasystem.core_utils.decision_matrix_cli decision.json --top-n 3

# From stdin
cat decision.json | python -m novasystem.core_utils.decision_matrix_cli

# Different method
python -m novasystem.core_utils.decision_matrix_cli decision.json -m normalized
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named novasystem" | Run from project root or install package |
| "Invalid JSON" | Check JSON syntax with `python -m json.tool file.json` |
| "Missing required fields" | Ensure `options`, `criteria`, `scores` are present |
| "No input provided" | Specify input file or pipe to stdin |
| Weights don't sum to 1.0 | That's OK! They're auto-normalized |

---

## 📚 Related Documentation

- **User Guide**: `DECISION_MATRIX_README.md`
- **Quick Reference**: `DECISION_MATRIX_QUICK_REFERENCE.md`
- **Enhancements**: `DECISION_MATRIX_ENHANCEMENTS.md`
- **Test Report**: `DECISION_MATRIX_TEST_REPORT.md`
- **Python API**: `examples/decision_matrix_examples.py`

---

## 🎓 Examples

See `examples/decision_input_example.json` for a complete example input file.

Run it:
```bash
python -m novasystem.core_utils.decision_matrix_cli examples/decision_input_example.json
```

Try different methods:
```bash
python -m novasystem.core_utils.decision_matrix_cli examples/decision_input_example.json --compare
```

---

**CLI Version:** 1.0
**Compatible with:** Decision Matrix v2.0+
**Python:** 3.7+
