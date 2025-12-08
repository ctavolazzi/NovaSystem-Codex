#!/usr/bin/env python3
"""
NovaSystem Full Demonstration
=============================

A comprehensive demonstration of NovaSystem's capabilities including:
- Event-driven architecture (event bus + state machine + pipeline)
- Memory systems (short-term, long-term, vector store)
- Decision matrix for AI-powered decision making
- Rich logging with both console and file output
- Historical journaling for decision tracking

Run:
    python examples/novasystem_full_demo.py

    # With verbose mode
    python examples/novasystem_full_demo.py --verbose

    # Specify custom log directory
    python examples/novasystem_full_demo.py --log-dir /path/to/logs
"""

import argparse
import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from novasystem.domain.events import (
    CommandCompleted,
    CommandQueued,
    CommandStarted,
    EventBus,
    RunCreated,
    RunStatusChanged,
    StepCompleted,
    StepFailed,
    StepStarted,
    get_event_bus,
)
from novasystem.domain.models import (
    CommandLog,
    CommandStatus,
    ParsedCommand,
    PipelineContext,
    RunStatus,
)
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult, SummarizeStep
from novasystem.domain.state_machine import RunStateMachine
from novasystem.core.memory import MemoryManager
from novasystem.core.vector_store import LocalVectorStore
from novasystem.tools.decision_matrix.decision_matrix import DecisionMatrix, make_decision

# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
JOURNAL_PATH = DATA_DIR / "novasystem_demo_journal.json"
MEMORY_PATH = DATA_DIR / "novasystem_demo_memory.json"

# =============================================================================
# Logging Setup
# =============================================================================


class ColorFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""

    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
    }

    ICONS = {
        "DEBUG": "🔍",
        "INFO": "✅",
        "WARNING": "⚠️ ",
        "ERROR": "❌",
        "CRITICAL": "🚨",
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        icon = self.ICONS.get(record.levelname, "")
        reset = self.COLORS["RESET"]

        # Add color and icon
        record.levelname_colored = f"{color}{record.levelname}{reset}"
        record.icon = icon

        return super().format(record)


def setup_logging(verbose: bool = False, log_dir: Optional[Path] = None) -> logging.Logger:
    """Configure logging for both console and file output."""
    log_dir = log_dir or LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"novasystem_demo_{timestamp}.log"

    logger = logging.getLogger("novasystem.demo")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_fmt = ColorFormatter(
        "%(icon)s [%(asctime)s] %(levelname_colored)s | %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_fmt)
    logger.addHandler(console_handler)

    # File handler with detailed format
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_fmt)
    logger.addHandler(file_handler)

    logger.info(f"Logging initialized. Log file: {log_file}")
    return logger


# =============================================================================
# Journal Management
# =============================================================================


def load_journal() -> List[Dict]:
    """Load historical journal entries."""
    JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not JOURNAL_PATH.exists():
        return []
    try:
        with JOURNAL_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_journal(entries: List[Dict]) -> None:
    """Persist journal entries."""
    JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL_PATH.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, default=str)


def append_journal_entry(entry: Dict) -> List[Dict]:
    """Add entry to journal and save."""
    entries = load_journal()
    entries.append(entry)
    save_journal(entries)
    return entries


# =============================================================================
# Event Logging
# =============================================================================


class EventLogger:
    """Comprehensive event logger that tracks all system events."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.events: List[Dict] = []
        self.metrics = {
            "total_events": 0,
            "by_type": {},
            "commands_executed": 0,
            "commands_failed": 0,
            "steps_completed": 0,
            "steps_failed": 0,
        }

    def log_event(self, event):
        """Log and track an event."""
        event_type = type(event).__name__
        self.metrics["total_events"] += 1
        self.metrics["by_type"][event_type] = self.metrics["by_type"].get(event_type, 0) + 1

        event_record = {
            "type": event_type,
            "timestamp": event.timestamp.isoformat() if hasattr(event, "timestamp") else datetime.now().isoformat(),
            "run_id": getattr(event, "run_id", None),
        }

        if isinstance(event, RunStatusChanged):
            self.logger.info(
                f"📊 RUN {event.run_id}: {event.old_status} → {event.new_status} "
                f"(reason: {event.reason})"
            )
            event_record["old_status"] = event.old_status
            event_record["new_status"] = event.new_status
            event_record["reason"] = event.reason

        elif isinstance(event, StepStarted):
            attempt = event.metadata.get("attempt", 1)
            self.logger.info(f"🚀 STEP '{event.step_name}' started (attempt {attempt})")
            event_record["step_name"] = event.step_name
            event_record["attempt"] = attempt

        elif isinstance(event, StepCompleted):
            self.metrics["steps_completed"] += 1
            self.logger.info(
                f"✅ STEP '{event.step_name}' completed in {event.duration:.3f}s"
            )
            event_record["step_name"] = event.step_name
            event_record["duration"] = event.duration

        elif isinstance(event, StepFailed):
            self.metrics["steps_failed"] += 1
            self.logger.error(f"❌ STEP '{event.step_name}' FAILED: {event.error}")
            event_record["step_name"] = event.step_name
            event_record["error"] = event.error

        elif isinstance(event, CommandQueued):
            self.logger.debug(f"📋 CMD queued: {event.command[:60]}...")
            event_record["command"] = event.command

        elif isinstance(event, CommandStarted):
            self.logger.info(f"▶️  CMD started: {event.command[:60]}...")
            event_record["command"] = event.command

        elif isinstance(event, CommandCompleted):
            if event.exit_code == 0:
                self.metrics["commands_executed"] += 1
                self.logger.info(
                    f"✅ CMD completed: {event.command[:40]}... "
                    f"(exit={event.exit_code}, time={event.execution_time:.2f}s)"
                )
            else:
                self.metrics["commands_failed"] += 1
                self.logger.warning(
                    f"⚠️  CMD failed: {event.command[:40]}... "
                    f"(exit={event.exit_code}, error={event.error[:50]})"
                )
            event_record["command"] = event.command
            event_record["exit_code"] = event.exit_code
            event_record["execution_time"] = event.execution_time

        elif isinstance(event, RunCreated):
            self.logger.info(f"🆕 RUN {event.run_id} created for {event.repo_url}")
            event_record["repo_url"] = event.repo_url

        else:
            self.logger.debug(f"📌 Event: {event_type}")

        self.events.append(event_record)

    def get_summary(self) -> Dict:
        """Get event metrics summary."""
        return {
            **self.metrics,
            "event_log": self.events,
        }


# =============================================================================
# Pipeline Steps
# =============================================================================


class AnalyzeRepositoryStep(PipelineStepBase):
    """Step that simulates repository analysis."""
    name = "analyze_repository"

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def execute(self, context: PipelineContext) -> StepResult:
        self.logger.debug("Starting repository analysis...")

        # Simulate analysis
        analysis = {
            "language": "Python",
            "version": "3.11",
            "framework": "FastAPI",
            "test_framework": "pytest",
            "has_docker": True,
            "doc_files": ["README.md", "docs/setup.md", "CONTRIBUTING.md"],
            "dependencies_count": 23,
        }

        context.repository_type = analysis["language"]
        context.doc_files = analysis["doc_files"]
        context.add_metadata("analysis", analysis)

        self.logger.info(f"Repository analysis: {analysis['language']} / {analysis['framework']}")
        return StepResult.ok(analysis)


class ParseDocumentationStep(PipelineStepBase):
    """Step that simulates documentation parsing."""
    name = "parse_documentation"

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def execute(self, context: PipelineContext) -> StepResult:
        self.logger.debug("Parsing documentation files...")

        # Simulated commands discovered from docs
        commands = [
            ParsedCommand(text="python -m venv .venv", source="README.md", priority=90),
            ParsedCommand(text="source .venv/bin/activate", source="README.md", priority=85),
            ParsedCommand(text="pip install -r requirements.txt", source="README.md", priority=80),
            ParsedCommand(text="pip install -e .", source="setup guide", priority=75),
            ParsedCommand(text="pytest tests/", source="CONTRIBUTING.md", priority=60),
            ParsedCommand(text="python -m mypy src/", source="CONTRIBUTING.md", priority=50),
        ]

        context.commands = commands
        context.add_metadata("commands_discovered", len(commands))

        self.logger.info(f"Discovered {len(commands)} installation commands")
        return StepResult.ok({"commands": len(commands)})


class ExecuteCommandsStep(PipelineStepBase):
    """Step that simulates command execution with detailed logging."""
    name = "execute_commands"

    def __init__(self, logger: logging.Logger, simulate_failure: bool = False):
        self.logger = logger
        self.simulate_failure = simulate_failure

    def execute(self, context: PipelineContext) -> StepResult:
        bus = get_event_bus()
        results = []

        for idx, cmd in enumerate(context.commands):
            self.logger.debug(f"Executing command {idx + 1}/{len(context.commands)}: {cmd.text}")

            bus.emit(CommandQueued(
                run_id=context.run_id,
                command=cmd.text,
                priority=cmd.priority,
                command_type="install"
            ))

            # Simulate execution delay
            time.sleep(0.05)

            bus.emit(CommandStarted(
                run_id=context.run_id,
                command=cmd.text,
                container_id="demo-container-001"
            ))

            # Simulate failure on specific command if configured
            exit_code = 0
            error = ""
            if self.simulate_failure and "mypy" in cmd.text:
                exit_code = 1
                error = "Type errors found: 3 issues in 2 files"

            time.sleep(0.02)

            log = CommandLog(
                id=idx,
                run_id=context.run_id,
                command=cmd.text,
                status=CommandStatus.SUCCESS if exit_code == 0 else CommandStatus.FAILED,
                timestamp=datetime.now(),
                exit_code=exit_code,
                output="Command executed successfully" if exit_code == 0 else "",
                error=error,
                execution_time=0.1 + (idx * 0.02),
                command_type="install",
                priority=cmd.priority,
            )
            results.append(log)

            bus.emit(CommandCompleted(
                run_id=context.run_id,
                command=cmd.text,
                exit_code=exit_code,
                output=log.output or "",
                error=log.error or "",
                execution_time=log.execution_time or 0.0,
            ))

            if exit_code != 0:
                context.results = results
                return StepResult.fail(f"Command failed: {cmd.text}", recoverable=False)

        context.results = results
        return StepResult.ok({"executed": len(results), "all_success": True})


class MakeDecisionStep(PipelineStepBase):
    """Step that uses decision matrix to make strategic choices."""
    name = "strategic_decision"

    def __init__(self, logger: logging.Logger, memory: MemoryManager):
        self.logger = logger
        self.memory = memory

    def execute(self, context: PipelineContext) -> StepResult:
        self.logger.info("Making strategic decisions based on analysis...")

        # Decision: Which testing strategy to use
        testing_decision = make_decision(
            options=["Unit Tests Only", "Unit + Integration", "Full E2E Suite"],
            criteria=["Execution Speed", "Coverage", "Maintenance Cost", "Confidence"],
            scores={
                "Unit Tests Only": [10, 5, 9, 6],
                "Unit + Integration": [7, 8, 7, 8],
                "Full E2E Suite": [3, 10, 4, 10],
            },
            weights=[0.2, 0.3, 0.2, 0.3],
            show_all_methods=True,  # Returns dict of method results
        )

        winner = testing_decision["weighted"]

        self.logger.info(
            f"Decision: {winner.winner} "
            f"(confidence: {winner.confidence_score:.1f}%)"
        )

        if winner.warnings:
            for w in winner.warnings:
                self.logger.warning(f"Decision warning: {w}")

        context.add_metadata("testing_decision", {
            "winner": winner.winner,
            "confidence": winner.confidence_score,
            "rankings": winner.rankings,
        })

        return StepResult.ok({
            "decision": winner.winner,
            "confidence": winner.confidence_score,
        })


# =============================================================================
# Main Demo
# =============================================================================


async def run_demo(verbose: bool = False, log_dir: Optional[Path] = None):
    """Run the full NovaSystem demonstration."""
    logger = setup_logging(verbose=verbose, log_dir=log_dir)

    print("\n" + "=" * 80)
    print(" NOVASYSTEM FULL DEMONSTRATION ".center(80, "="))
    print("=" * 80 + "\n")

    logger.info("Starting NovaSystem demonstration")
    logger.info(f"Data directory: {DATA_DIR}")
    logger.info(f"Log directory: {LOG_DIR}")

    # Initialize systems
    bus = get_event_bus()
    event_logger = EventLogger(logger)
    bus.subscribe_all(event_logger.log_event)

    memory = MemoryManager(max_short_term=20, max_long_term=100)
    vector_store = LocalVectorStore(memory_file=MEMORY_PATH, persist=True)

    # Load historical context
    journal = load_journal()
    logger.info(f"Loaded {len(journal)} historical journal entries")

    # Store session context
    run_id = int(datetime.now().timestamp())
    session_context = {
        "run_id": run_id,
        "started_at": datetime.now().isoformat(),
        "demo_mode": True,
        "verbose": verbose,
    }
    await memory.store_context("session", session_context, "short_term")

    # =========================================================================
    # Phase 1: Initialize Run
    # =========================================================================
    print("\n" + "-" * 40)
    print("PHASE 1: INITIALIZATION")
    print("-" * 40)

    sm = RunStateMachine(run_id=run_id, event_bus=bus)
    bus.emit(RunCreated(run_id=run_id, repo_url="https://github.com/novasystem/demo-project"))

    # Store knowledge in vector store
    vector_store.remember(
        "NovaSystem uses event-driven architecture with state machines",
        tags=["architecture", "system"]
    )
    vector_store.remember(
        "The pipeline processes steps sequentially with retry support",
        tags=["pipeline", "execution"]
    )
    vector_store.remember(
        "Decision matrix supports weighted, normalized, ranking, and best-worst methods",
        tags=["decision", "methods"]
    )

    logger.info("Knowledge base populated with system information")

    # =========================================================================
    # Phase 2: Analysis
    # =========================================================================
    print("\n" + "-" * 40)
    print("PHASE 2: ANALYSIS")
    print("-" * 40)

    sm.start_analyzing()

    # Build analysis pipeline
    analysis_pipeline = Pipeline(event_bus=bus)
    analysis_pipeline.add_step(AnalyzeRepositoryStep(logger))
    analysis_pipeline.add_step(ParseDocumentationStep(logger))
    analysis_pipeline.add_step(MakeDecisionStep(logger, memory))

    context = PipelineContext(run_id=run_id, repo_url="demo-project")
    analysis_result = analysis_pipeline.run(context)

    if not analysis_result.success:
        logger.error(f"Analysis failed: {analysis_result.error}")
        sm.complete(success=False)
        return

    # Store analysis results
    await memory.store_context("analysis_result", {
        "success": analysis_result.success,
        "analysis": context.metadata.get("analysis"),
        "commands_discovered": context.metadata.get("commands_discovered"),
        "testing_decision": context.metadata.get("testing_decision"),
    }, "short_term")

    # =========================================================================
    # Phase 3: Execution
    # =========================================================================
    print("\n" + "-" * 40)
    print("PHASE 3: EXECUTION")
    print("-" * 40)

    sm.start_running()

    # Build execution pipeline
    execution_pipeline = Pipeline(event_bus=bus)
    execution_pipeline.add_step(ExecuteCommandsStep(logger, simulate_failure=False))
    execution_pipeline.add_step(SummarizeStep())

    execution_result = execution_pipeline.run(context)

    # =========================================================================
    # Phase 4: Completion
    # =========================================================================
    print("\n" + "-" * 40)
    print("PHASE 4: COMPLETION")
    print("-" * 40)

    sm.complete(success=execution_result.success)

    # Store final results
    final_result = {
        "run_id": run_id,
        "success": execution_result.success,
        "summary": context.metadata.get("summary"),
        "total_commands": context.metadata.get("total_commands"),
        "successful_commands": context.metadata.get("successful_commands"),
        "failed_commands": context.metadata.get("failed_commands"),
        "testing_decision": context.metadata.get("testing_decision", {}).get("winner"),
    }

    await memory.store_context("final_result", final_result, "long_term")

    # Compress memory
    await memory.compress_memory()

    # Update journal
    journal_entry = {
        "timestamp": datetime.now().isoformat(),
        "run_id": run_id,
        "success": execution_result.success,
        "status": sm.status.value,
        "commands_executed": context.metadata.get("total_commands", 0),
        "testing_strategy": context.metadata.get("testing_decision", {}).get("winner"),
        "event_metrics": event_logger.metrics,
    }
    updated_journal = append_journal_entry(journal_entry)

    # =========================================================================
    # Summary Report
    # =========================================================================
    print("\n" + "=" * 80)
    print(" DEMONSTRATION SUMMARY ".center(80, "="))
    print("=" * 80)

    metrics = event_logger.get_summary()

    print(f"""
Run ID:              {run_id}
Final Status:        {sm.status.value.upper()}
Success:             {'✅ Yes' if execution_result.success else '❌ No'}

Events:
  Total Events:      {metrics['total_events']}
  Steps Completed:   {metrics['steps_completed']}
  Steps Failed:      {metrics['steps_failed']}
  Commands Executed: {metrics['commands_executed']}
  Commands Failed:   {metrics['commands_failed']}

Memory:
  Short-term items:  {memory.get_memory_stats()['short_term_count']}
  Long-term items:   {memory.get_memory_stats()['long_term_count']}
  Vector store docs: {vector_store.count()}

Decision:
  Testing Strategy:  {context.metadata.get('testing_decision', {}).get('winner', 'N/A')}
  Confidence:        {context.metadata.get('testing_decision', {}).get('confidence', 0):.1f}%

Journal:
  Total entries:     {len(updated_journal)}
  Latest success:    {'✅' if updated_journal[-1]['success'] else '❌'}
""")

    # Show recent journal entries
    print("Recent Journal Entries:")
    print("-" * 40)
    for entry in updated_journal[-3:]:
        ts = entry.get("timestamp", "")[:19]
        status = "✅" if entry.get("success") else "❌"
        strategy = entry.get("testing_strategy", "N/A")
        print(f"  {ts} | {status} | Strategy: {strategy}")

    print(f"\n📁 Full log: {LOG_DIR}")
    print(f"📁 Journal: {JOURNAL_PATH}")
    print(f"📁 Memory: {MEMORY_PATH}")

    # Recall some knowledge
    print("\n" + "-" * 40)
    print("Knowledge Recall Test:")
    print("-" * 40)
    recall_results = vector_store.recall("decision matrix methods", limit=2)
    for result, score in recall_results:
        print(f"  [{score:.2f}] {result['text'][:70]}...")

    print("\n" + "=" * 80)
    print(" DEMONSTRATION COMPLETE ".center(80, "="))
    print("=" * 80 + "\n")

    return {
        "success": execution_result.success,
        "run_id": run_id,
        "metrics": metrics,
        "memory_stats": memory.get_memory_stats(),
        "vector_stats": vector_store.stats(),
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NovaSystem Full Demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python novasystem_full_demo.py
  python novasystem_full_demo.py --verbose
  python novasystem_full_demo.py --log-dir /tmp/nova_logs
        """
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose (DEBUG level) logging"
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        help="Custom directory for log files"
    )

    args = parser.parse_args()

    try:
        result = asyncio.run(run_demo(verbose=args.verbose, log_dir=args.log_dir))
        sys.exit(0 if result and result.get("success") else 1)
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
