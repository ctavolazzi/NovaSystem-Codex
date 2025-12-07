#!/usr/bin/env python3
"""
Decision Matrix CLI - Command-line interface for decision matrix utility

Usage:
    # From JSON file
    python -m novasystem.core_utils.decision_matrix_cli input.json

    # From stdin
    cat input.json | python -m novasystem.core_utils.decision_matrix_cli

    # With options
    python -m novasystem.core_utils.decision_matrix_cli input.json --method normalized --top-n 3

    # Output as JSON
    python -m novasystem.core_utils.decision_matrix_cli input.json --json

    # Compare all methods
    python -m novasystem.core_utils.decision_matrix_cli input.json --compare

Input JSON format:
    {
        "options": ["Option A", "Option B", "Option C"],
        "criteria": ["Cost", "Quality", "Speed"],
        "scores": {
            "Option A": [7, 8, 6],
            "Option B": [9, 5, 7],
            "Option C": [6, 9, 8]
        },
        "weights": [0.3, 0.5, 0.2]  // Optional
    }
"""

import argparse
import json
import sys
from typing import Dict, Any, Optional
from pathlib import Path

from .decision_matrix import make_decision, compare_methods


def load_input(input_source: Optional[str] = None) -> Dict[str, Any]:
    """Load input from file or stdin."""
    if input_source and input_source != '-':
        # Load from file
        input_path = Path(input_source)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_source}")

        with open(input_path, 'r') as f:
            data = json.load(f)
    else:
        # Load from stdin
        if sys.stdin.isatty():
            raise ValueError(
                "No input provided. Either specify a file or pipe JSON to stdin.\n"
                "Example: cat input.json | python -m novasystem.core_utils.decision_matrix_cli"
            )
        data = json.load(sys.stdin)

    return data


def validate_input(data: Dict[str, Any]) -> None:
    """Validate input data structure."""
    required_fields = ['options', 'criteria', 'scores']
    missing = [field for field in required_fields if field not in data]

    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    if not isinstance(data['options'], list):
        raise ValueError("'options' must be a list")

    if not isinstance(data['criteria'], list):
        raise ValueError("'criteria' must be a list")

    if not isinstance(data['scores'], dict):
        raise ValueError("'scores' must be a dictionary")

    # Check all options have scores
    for option in data['options']:
        if option not in data['scores']:
            raise ValueError(f"Missing scores for option: {option}")


def create_example_file(output_path: str) -> None:
    """Create an example input JSON file."""
    example = {
        "options": ["Python", "JavaScript", "Go"],
        "criteria": ["Learning Curve", "Performance", "Community", "Jobs"],
        "scores": {
            "Python": [9, 7, 10, 10],
            "JavaScript": [8, 6, 9, 10],
            "Go": [6, 9, 7, 8]
        },
        "weights": [0.2, 0.3, 0.2, 0.3]
    }

    with open(output_path, 'w') as f:
        json.dump(example, f, indent=2)

    print(f"✅ Example file created: {output_path}")
    print("\nRun with:")
    print(f"  python -m novasystem.core_utils.decision_matrix_cli {output_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Decision Matrix CLI - Make data-driven decisions from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python -m novasystem.core_utils.decision_matrix_cli input.json

  # Use normalized method
  python -m novasystem.core_utils.decision_matrix_cli input.json --method normalized

  # Show only top 3 options
  python -m novasystem.core_utils.decision_matrix_cli input.json --top-n 3

  # Output as JSON
  python -m novasystem.core_utils.decision_matrix_cli input.json --json

  # Compare all methods
  python -m novasystem.core_utils.decision_matrix_cli input.json --compare

  # Show comparison table
  python -m novasystem.core_utils.decision_matrix_cli input.json --table

  # From stdin
  cat input.json | python -m novasystem.core_utils.decision_matrix_cli

  # Create example file
  python -m novasystem.core_utils.decision_matrix_cli --example my_decision.json

Input JSON format:
  {
    "options": ["Option A", "Option B"],
    "criteria": ["Criterion X", "Criterion Y"],
    "scores": {
      "Option A": [7, 8],
      "Option B": [9, 5]
    },
    "weights": [0.6, 0.4]
  }
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        help='Input JSON file (or - for stdin)'
    )

    parser.add_argument(
        '-m', '--method',
        choices=['weighted', 'normalized', 'ranking', 'best_worst'],
        default='weighted',
        help='Analysis method (default: weighted)'
    )

    parser.add_argument(
        '-n', '--top-n',
        type=int,
        metavar='N',
        help='Show only top N options'
    )

    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output results as JSON'
    )

    parser.add_argument(
        '-c', '--compare',
        action='store_true',
        help='Compare all 4 methods'
    )

    parser.add_argument(
        '-t', '--table',
        action='store_true',
        help='Show comparison table'
    )

    parser.add_argument(
        '-e', '--example',
        metavar='FILE',
        help='Create example input file and exit'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Handle --example
    if args.example:
        create_example_file(args.example)
        return 0

    # Require input if not creating example, but auto-read stdin when piped
    if not args.input:
        if not sys.stdin.isatty():
            args.input = '-'
        else:
            parser.error(
                "Input file required (or pipe JSON via stdin, e.g. "
                "'cat input.json | python -m novasystem.core_utils.decision_matrix_cli')"
            )

    try:
        # Load input
        if args.verbose:
            print("Loading input...", file=sys.stderr)

        data = load_input(args.input)
        validate_input(data)

        if args.verbose:
            print(f"✓ Loaded {len(data['options'])} options, {len(data['criteria'])} criteria",
                  file=sys.stderr)

        # Extract parameters
        options = data['options']
        criteria = data['criteria']
        scores = data['scores']
        weights = data.get('weights')

        # Run analysis
        if args.compare:
            # Compare all methods
            if args.verbose:
                print("Comparing all methods...", file=sys.stderr)

            comparison = compare_methods(options, criteria, scores, weights)

            if args.json:
                # Get all method results for JSON output
                results = make_decision(
                    options, criteria, scores, weights,
                    show_all_methods=True,
                    top_n=args.top_n
                )
                output = {
                    method: result.to_dict()
                    for method, result in results.items()
                }
                print(json.dumps(output, indent=2))
            else:
                print(comparison)

        else:
            # Single method analysis
            if args.verbose:
                print(f"Running {args.method} analysis...", file=sys.stderr)

            result = make_decision(
                options, criteria, scores, weights,
                method=args.method,
                top_n=args.top_n
            )

            if args.json:
                # JSON output
                print(result.to_json())
            else:
                # Formatted output
                print(result)

                # Show comparison table if requested
                if args.table:
                    print("\n")
                    print(result.comparison_table())

        return 0

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        print(f"❌ Invalid input: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        if args.verbose:
            import traceback
            traceback.print_exc()
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
