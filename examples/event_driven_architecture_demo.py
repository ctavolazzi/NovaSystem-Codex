#!/usr/bin/env python3
"""
Demonstration of the event-driven architecture (event bus + state machine + pipeline).

Run:
    python examples/event_driven_architecture_demo.py
"""

from datetime import datetime

from novasystem.domain.events import (
    CommandCompleted,
    CommandQueued,
    CommandStarted,
    RunStatusChanged,
    StepCompleted,
    StepFailed,
    StepStarted,
    get_event_bus,
)
from novasystem.domain.models import CommandLog, CommandStatus, ParsedCommand, PipelineContext
from novasystem.domain.pipeline import Pipeline, PipelineStepBase, StepResult, SummarizeStep
from novasystem.domain.state_machine import RunStateMachine


def attach_console_event_logger():
    """Subscribe a lightweight console printer to all events."""

    def render(event):
        ts = event.timestamp.strftime("%H:%M:%S")

        if isinstance(event, RunStatusChanged):
            print(f"[{ts}] RUN {event.run_id}: {event.old_status} -> {event.new_status} ({event.reason})")
        elif isinstance(event, StepStarted):
            attempt = event.metadata.get("attempt")
            print(f"[{ts}] STEP {event.step_name} started (attempt {attempt})")
        elif isinstance(event, StepCompleted):
            print(f"[{ts}] STEP {event.step_name} completed in {event.duration:.3f}s")
        elif isinstance(event, StepFailed):
            print(f"[{ts}] STEP {event.step_name} failed: {event.error}")
        elif isinstance(event, CommandQueued):
            print(f"[{ts}] CMD queued: {event.command}")
        elif isinstance(event, CommandStarted):
            print(f"[{ts}] CMD started: {event.command}")
        elif isinstance(event, CommandCompleted):
            status = "ok" if event.exit_code == 0 else "error"
            print(f"[{ts}] CMD finished ({status}): {event.command}")
        else:
            print(f"[{ts}] {event.event_type}: {event}")

    get_event_bus().subscribe_all(render)


class PrepareContextStep(PipelineStepBase):
    name = "prepare_context"
    retryable = False

    def execute(self, context: PipelineContext) -> StepResult:  # type: ignore[override]
        context.repo_path = context.repo_url
        context.repository_type = "python"
        context.doc_files = ["README.md", "docs/setup.md"]
        context.add_metadata("strategy_hint", "python")
        return StepResult.ok({"doc_files": len(context.doc_files)})


class ParseDocsStep(PipelineStepBase):
    name = "parse_docs"
    retryable = False

    def __init__(self):
        self._commands = [
            ParsedCommand(text="python -m venv .venv", source="demo", priority=60),
            ParsedCommand(text="pip install -r requirements.txt", source="demo", priority=80),
            ParsedCommand(text="pytest", source="demo", priority=50),
        ]

    def execute(self, context: PipelineContext) -> StepResult:  # type: ignore[override]
        context.commands = self._commands
        return StepResult.ok(context.commands, discovered=len(context.commands))


class SimulateExecutionStep(PipelineStepBase):
    name = "execute_commands"
    retryable = False

    def __init__(self, exit_codes=None):
        self._exit_codes = exit_codes or []

    def execute(self, context: PipelineContext) -> StepResult:  # type: ignore[override]
        bus = get_event_bus()
        results = []

        for idx, cmd in enumerate(context.commands):
            bus.emit(CommandQueued(run_id=context.run_id, command=cmd.text, priority=cmd.priority, command_type=cmd.command_type))
            bus.emit(CommandStarted(run_id=context.run_id, command=cmd.text, container_id="demo-container"))

            exit_code = self._exit_codes[idx] if idx < len(self._exit_codes) else 0
            status = CommandStatus.SUCCESS if exit_code == 0 else CommandStatus.FAILED

            log = CommandLog(
                id=idx,
                run_id=context.run_id,
                command=cmd.text,
                status=status,
                timestamp=datetime.now(),
                exit_code=exit_code,
                output="completed",
                error="" if exit_code == 0 else "simulated failure",
                execution_time=0.02,
                command_type=cmd.command_type,
                priority=cmd.priority,
            )
            results.append(log)

            bus.emit(
                CommandCompleted(
                    run_id=context.run_id,
                    command=cmd.text,
                    exit_code=exit_code,
                    output=log.output or "",
                    error=log.error or "",
                    execution_time=log.execution_time or 0.0,
                )
            )

            if exit_code != 0:
                context.results = results
                return StepResult.fail(f"Command failed: {cmd.text}", recoverable=False)

        context.results = results
        return StepResult.ok(results, executed=len(results))


def build_demo_pipeline():
    pipeline = Pipeline(event_bus=get_event_bus())
    pipeline.add_step(PrepareContextStep())
    pipeline.add_step(ParseDocsStep())
    pipeline.add_step(SimulateExecutionStep(exit_codes=[0, 0, 0]))
    pipeline.add_step(SummarizeStep())
    return pipeline


def main():
    bus = get_event_bus()
    attach_console_event_logger()

    run_id = 2025
    state_machine = RunStateMachine(run_id=run_id, event_bus=bus)
    state_machine.start_analyzing()
    state_machine.start_running()

    context = PipelineContext(run_id=run_id, repo_url="demo-repo")
    pipeline = build_demo_pipeline()
    result = pipeline.run(context)

    state_machine.complete(success=result.success)

    print("\nFinal summary")
    print("-" * 40)
    print(f"Run status: {state_machine.status.value}")
    print(f"Summary:    {context.metadata.get('summary')}")
    print(f"Commands:   {context.metadata.get('total_commands')} (success={context.metadata.get('successful_commands')}, failed={context.metadata.get('failed_commands')})")


if __name__ == "__main__":
    main()
