#!/usr/bin/env python3
"""
Decision Matrix UI Demo
-----------------------

A comprehensive, log-heavy demonstration of NovaSystem's decision matrix.
The script simulates a small UI, emits verbose console/file logs, and reads/writes
to a historical journal to show how past choices influence the next decision.

Run:
    python examples/decision_matrix_ui_demo.py
"""

import json
import logging
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from novasystem.tools.decision_matrix.decision_matrix import DecisionMatrix, make_decision

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "logs" / "decision_matrix_ui_demo.log"
JOURNAL_PATH = BASE_DIR / "data" / "decision_journal.json"


# ---------------------------------------------------------------------------
# Logging + Journal Helpers
# ---------------------------------------------------------------------------
def setup_logging() -> logging.Logger:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("nova.decision_demo")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    formatter_console = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s", "%H:%M:%S")
    formatter_file = logging.Formatter(
        "%(asctime)s | %(levelname)-5s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter_console)

    file_handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter_file)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger


def load_journal() -> List[Dict]:
    if not JOURNAL_PATH.exists():
        return []
    try:
        with JOURNAL_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_journal(entries: List[Dict]) -> None:
    JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def append_journal_entry(entry: Dict) -> List[Dict]:
    entries = load_journal()
    entries.append(entry)
    save_journal(entries)
    return entries


# ---------------------------------------------------------------------------
# Data Construction
# ---------------------------------------------------------------------------
def build_dataset(history: List[Dict]) -> Tuple[List[str], List[str], Dict[str, List[float]], List[float], Dict[str, float]]:
    """
    Build a rich comparison dataset. We keep scores on a 0-10 scale for clarity.
    The historical journal influences the "Historical Trust" criterion.
    """
    options = [
        "PixelLab Nova",
        "GPT-4.1 Enterprise",
        "Claude 3.5 Sonnet",
        "Gemini 2.0 Advanced",
        "Mistral Large",
        "Cohere Command R+",
    ]

    criteria_with_weights = [
        ("Latency (lower is better)", 0.08),
        ("Reliability / Uptime", 0.12),
        ("Reasoning Depth", 0.18),
        ("Tool Use & Functions", 0.10),
        ("Context Window", 0.08),
        ("Cost Efficiency", 0.14),
        ("Safety & Guardrails", 0.08),
        ("Eval Benchmark Score", 0.12),
        ("Throughput at Scale", 0.10),
    ]

    history_bonus = compute_history_bonus(options, history)

    # Baseline scores (0-10) per option
    base_scores = {
        "PixelLab Nova":          [9.2, 9.4, 9.1, 9.0, 9.6, 8.6, 9.3, 9.0, 9.1],
        "GPT-4.1 Enterprise":     [8.6, 9.6, 9.5, 9.4, 9.2, 7.4, 9.2, 9.4, 9.0],
        "Claude 3.5 Sonnet":      [9.1, 9.2, 9.3, 9.0, 8.8, 8.2, 9.5, 9.1, 8.9],
        "Gemini 2.0 Advanced":    [8.8, 9.0, 8.9, 8.4, 9.5, 8.8, 9.1, 9.0, 9.2],
        "Mistral Large":          [8.9, 8.4, 8.6, 8.9, 8.1, 9.1, 8.7, 8.8, 8.6],
        "Cohere Command R+":      [8.4, 8.8, 8.7, 8.6, 8.4, 9.3, 9.0, 8.5, 8.5],
    }

    # Incorporate historical trust as a new criterion
    criteria_with_weights.append(("Historical Trust (journal)", 0.10))
    for option in options:
        base_scores[option].append(history_bonus.get(option, 5.0))

    criteria = [c for c, _ in criteria_with_weights]
    weights = [w for _, w in criteria_with_weights]
    return options, criteria, base_scores, weights, history_bonus


def compute_history_bonus(options: List[str], history: List[Dict]) -> Dict[str, float]:
    """
    Derive a 0-10 "trust" bonus from prior journal entries (how often each option won).
    The bonus is lightly normalized to keep influence bounded.
    """
    wins = {opt: 0 for opt in options}
    for entry in history:
        winner = entry.get("winner")
        if winner in wins:
            wins[winner] += 1

    total_wins = sum(wins.values()) or 1
    bonus = {}
    for opt, count in wins.items():
        # Center around 5.0 baseline; add up to +5 based on share of wins.
        share = count / total_wins
        bonus[opt] = round(5.0 + (share * 5.0), 2)
    return bonus


# ---------------------------------------------------------------------------
# Rendering Helpers (UI-ish)
# ---------------------------------------------------------------------------
def print_header():
    print("=" * 90)
    print(" NOVASYSTEM DECISION MATRIX — LLM STRATEGY BOARD ".center(90, "="))
    print("=" * 90)
    print("Evaluating API providers across latency, reasoning, cost, safety, throughput, and history.\n")


def render_rankings(result) -> None:
    print("\n[ RANKINGS ]")
    for idx, (opt, score) in enumerate(result.rankings, 1):
        normalized = result.normalized_scores.get(opt, 0)
        marker = "🏆" if opt == result.winner else "  "
        print(f"{marker} {idx:>2}. {opt:<24} → score {score:6.2f} ({normalized:5.1f}%)")
    print()


def render_breakdown(result) -> None:
    print("[ CRITERIA BREAKDOWN ]")
    for opt, criteria_scores in result.scores_breakdown.items():
        print(f"\n• {opt}")
        for criterion, score in criteria_scores.items():
            print(f"   - {criterion:<28}: {score:5.2f}")
    print()


def render_comparison(result) -> None:
    print(result.comparison_table())
    print()


# ---------------------------------------------------------------------------
# Demo Execution
# ---------------------------------------------------------------------------
def run_demo():
    logger = setup_logging()
    logger.info("Starting decision matrix UI demo")
    logger.info("Log file: %s", LOG_PATH)
    logger.info("Journal path: %s", JOURNAL_PATH)

    history = load_journal()
    logger.info("Loaded %d historical journal entries", len(history))

    options, criteria, scores, weights, history_bonus = build_dataset(history)

    logger.debug("Criteria: %s", criteria)
    logger.debug("Weights: %s", weights)
    logger.debug("History bonus per option: %s", history_bonus)

    # Run across all methods for a fuller log trail
    all_results = make_decision(
        options=options,
        criteria=criteria,
        scores=scores,
        weights=weights,
        show_all_methods=True,
        top_n=5,
    )

    weighted = all_results["weighted"]

    logger.info("Weighted winner: %s (confidence %.1f%%)", weighted.winner, weighted.confidence_score)
    for method_name, result in all_results.items():
        logger.info("[%s] Winner=%s • Confidence=%.1f%%", method_name, result.winner, result.confidence_score)
        for opt, score in result.rankings:
            logger.debug("[%s] %-22s -> %.3f", method_name, opt, score)

    # UI-ish console output
    print_header()
    print(f"Session: DM-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    print(f"Winner (weighted): {weighted.winner}  | Confidence: {weighted.confidence_score:.1f}%")
    if weighted.warnings:
        print("\nWarnings:")
        for w in weighted.warnings:
            print(f"- {w}")

    render_rankings(weighted)
    render_breakdown(weighted)
    render_comparison(weighted)

    print("[ METHOD COMPARISON ]")
    for method_name, result in all_results.items():
        gap = result.confidence_score - weighted.confidence_score
        print(f"- {method_name.upper():10s} winner: {result.winner:<22s} confidence: {result.confidence_score:5.1f}% (Δ {gap:+.1f})")
    print()

    # Persist to journal
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "winner": weighted.winner,
        "confidence": round(weighted.confidence_score, 2),
        "method": "weighted",
        "top3": weighted.rankings[:3],
        "history_bonus": history_bonus,
        "notes": "Demo run - generated with synthetic provider metrics and historical trust signal.",
    }
    updated_journal = append_journal_entry(entry)
    logger.info("Journal updated; total entries now %d", len(updated_journal))

    # Show a concise recap that a UI might show in a footer
    print("[ JOURNAL RECAP ]")
    for record in updated_journal[-3:]:
        ts = record.get("timestamp", "")[:19]
        print(f"- {ts} :: winner {record.get('winner')} (conf {record.get('confidence')}%) via {record.get('method')}")
    print(f"\nLog file written to: {LOG_PATH}")
    print(f"Journal persisted to: {JOURNAL_PATH}")


if __name__ == "__main__":
    run_demo()
