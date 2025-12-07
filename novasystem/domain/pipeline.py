"""
Pipeline Orchestrator for NovaSystem.

Breaks the monolithic process_repository into discrete, hookable steps.
Each step can:
- Be retried on failure
- Be skipped
- Emit events for observers
- Add to the shared context

Pipeline Steps:
1. Clone - Clone or mount repository
2. Detect Strategy - Identify repository type
3. Discover Docs - Find documentation files
4. Parse Commands - Extract installation commands
5. Validate Commands - Apply policy checks
6. Execute - Run commands in container
7. Summarize - Generate run summary
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar

from .events import (
    EventBus,
    StepStarted,
    StepCompleted,
    StepFailed,
    PipelineStep,
    get_event_bus,
)
from .models import PipelineContext, RunStatus
from .state_machine import RunStateMachine

logger = logging.getLogger(__name__)

T = TypeVar("T")


# =============================================================================
# STEP RESULT
# =============================================================================

@dataclass
class StepResult(Generic[T]):
    """
    Result of a pipeline step execution.
    """
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    duration: float = 0.0
    should_continue: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: T = None, **metadata) -> "StepResult[T]":
        """Create a successful result."""
        return cls(success=True, data=data, metadata=metadata)

    @classmethod
    def fail(cls, error: str, recoverable: bool = True, **metadata) -> "StepResult[T]":
        """Create a failed result."""
        return cls(
            success=False,
            error=error,
            should_continue=recoverable,
            metadata=metadata,
        )

    @classmethod
    def skip(cls, reason: str) -> "StepResult[T]":
        """Create a skipped result."""
        return cls(success=True, metadata={"skipped": True, "reason": reason})


# =============================================================================
# PIPELINE STEP INTERFACE
# =============================================================================

class PipelineStepBase(ABC):
    """
    Base class for pipeline steps.

    Each step receives a PipelineContext and returns a StepResult.
    Steps can modify the context to pass data to subsequent steps.
    """

    name: str = "unnamed_step"
    retryable: bool = True
    max_retries: int = 3

    @abstractmethod
    def execute(self, context: PipelineContext) -> StepResult:
        """
        Execute the step.

        Args:
            context: Pipeline context with all state

        Returns:
            StepResult indicating success/failure
        """
        pass

    def can_skip(self, context: PipelineContext) -> bool:
        """Check if this step can be skipped given current context."""
        return False

    def rollback(self, context: PipelineContext) -> None:
        """Rollback any changes made by this step (optional)."""
        pass


# =============================================================================
# PIPELINE ORCHESTRATOR
# =============================================================================

class Pipeline:
    """
    Pipeline orchestrator that executes steps in sequence.

    Features:
    - Step-by-step execution with event emission
    - Retry logic for failed steps
    - Skip logic for unnecessary steps
    - Hook points for observers

    Usage:
        pipeline = Pipeline()
        pipeline.add_step(CloneStep())
        pipeline.add_step(DetectStrategyStep())
        pipeline.add_step(ExecuteStep())

        result = pipeline.run(context)
    """

    def __init__(self,
                 event_bus: Optional[EventBus] = None,
                 state_machine: Optional[RunStateMachine] = None):
        """
        Initialize the pipeline.

        Args:
            event_bus: Event bus for emitting events
            state_machine: State machine for run lifecycle
        """
        self._steps: List[PipelineStepBase] = []
        self._event_bus = event_bus or get_event_bus()
        self._state_machine = state_machine
        self._hooks: Dict[str, List[Callable]] = {
            "before_step": [],
            "after_step": [],
            "on_error": [],
            "on_complete": [],
        }

    def add_step(self, step: PipelineStepBase) -> "Pipeline":
        """
        Add a step to the pipeline.

        Args:
            step: Step to add

        Returns:
            Self for chaining
        """
        self._steps.append(step)
        return self

    def add_hook(self, hook_type: str, callback: Callable) -> "Pipeline":
        """
        Add a hook callback.

        Args:
            hook_type: One of "before_step", "after_step", "on_error", "on_complete"
            callback: Function to call

        Returns:
            Self for chaining
        """
        if hook_type in self._hooks:
            self._hooks[hook_type].append(callback)
        return self

    def _call_hooks(self, hook_type: str, *args, **kwargs) -> None:
        """Call all registered hooks of a type."""
        for hook in self._hooks.get(hook_type, []):
            try:
                hook(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {hook_type} hook: {e}")

    def run(self, context: PipelineContext) -> StepResult:
        """
        Run all pipeline steps.

        Args:
            context: Pipeline context

        Returns:
            Final StepResult
        """
        logger.info(f"Starting pipeline for run {context.run_id}")

        results: List[StepResult] = []

        for step in self._steps:
            # Check if we should stop
            if context.should_stop:
                logger.info(f"Pipeline stopped: {context.stop_reason}")
                break

            # Check if step can be skipped
            if step.can_skip(context):
                logger.info(f"Skipping step: {step.name}")
                results.append(StepResult.skip(f"Step {step.name} skipped"))
                continue

            # Execute step with retries
            result = self._execute_step_with_retry(step, context)
            results.append(result)

            # Stop on non-recoverable failure
            if not result.success and not result.should_continue:
                logger.error(f"Pipeline failed at step {step.name}: {result.error}")
                self._call_hooks("on_error", step, result, context)
                return StepResult.fail(
                    f"Pipeline failed at {step.name}: {result.error}",
                    recoverable=False,
                )

        # All steps completed
        self._call_hooks("on_complete", results, context)

        # Aggregate results
        total_duration = sum(r.duration for r in results)
        all_success = all(r.success for r in results)

        return StepResult(
            success=all_success,
            data=context,
            duration=total_duration,
            metadata={"step_count": len(results)},
        )

    def _execute_step_with_retry(self,
                                 step: PipelineStepBase,
                                 context: PipelineContext) -> StepResult:
        """Execute a step with retry logic."""
        retries = 0
        last_result: Optional[StepResult] = None

        while retries <= step.max_retries:
            # Emit step started event
            self._event_bus.emit(StepStarted(
                run_id=context.run_id,
                step_name=step.name,
                metadata={"attempt": retries + 1},
            ))

            self._call_hooks("before_step", step, context)

            start_time = time.time()
            try:
                result = step.execute(context)
                result.duration = time.time() - start_time

                self._call_hooks("after_step", step, result, context)

                if result.success:
                    # Emit step completed event
                    self._event_bus.emit(StepCompleted(
                        run_id=context.run_id,
                        step_name=step.name,
                        result=result.data,
                        duration=result.duration,
                    ))
                    return result

                last_result = result

            except Exception as e:
                duration = time.time() - start_time
                logger.exception(f"Step {step.name} raised exception: {e}")
                last_result = StepResult.fail(str(e), recoverable=step.retryable)
                last_result.duration = duration

            # Should we retry?
            if not step.retryable or retries >= step.max_retries:
                break

            retries += 1
            logger.warning(f"Retrying step {step.name} (attempt {retries + 1})")

        # All retries exhausted
        self._event_bus.emit(StepFailed(
            run_id=context.run_id,
            step_name=step.name,
            error=last_result.error if last_result else "Unknown error",
            recoverable=step.retryable,
        ))

        return last_result or StepResult.fail("Unknown error", recoverable=False)


# =============================================================================
# BUILT-IN PIPELINE STEPS
# =============================================================================

class CloneStep(PipelineStepBase):
    """Clone or mount the repository."""

    name = "clone"

    def __init__(self, repo_handler=None):
        self._repo_handler = repo_handler

    def execute(self, context: PipelineContext) -> StepResult:
        """Clone the repository and set repo_path in context."""
        from ..tools.repository import RepositoryHandler

        handler = self._repo_handler or RepositoryHandler()

        repo_url = context.repo_url

        try:
            if repo_url.startswith(("http://", "https://", "git://")):
                repo_path = handler.clone_repository(repo_url)
                context.add_metadata("is_local", False)
            else:
                repo_path = repo_url
                context.add_metadata("is_local", True)

            context.repo_path = repo_path
            return StepResult.ok(repo_path)

        except Exception as e:
            return StepResult.fail(f"Failed to clone: {e}", recoverable=True)


class DetectStrategyStep(PipelineStepBase):
    """Detect repository type and select strategy."""

    name = "detect_strategy"

    def execute(self, context: PipelineContext) -> StepResult:
        """Detect repository type from files."""
        import os

        repo_path = context.repo_path
        if not repo_path:
            return StepResult.fail("No repository path set")

        # Detection logic (from original nova.py)
        detectors = [
            (["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"], "python"),
            (["package.json"], "javascript"),
            (["Gemfile"], "ruby"),
            (["pom.xml"], "java"),
            (["go.mod"], "go"),
            (["Cargo.toml"], "rust"),
            (["composer.json"], "php"),
            (["Dockerfile"], "docker"),
        ]

        detected_type = None
        detected_files = []

        for files, repo_type in detectors:
            for f in files:
                if os.path.exists(os.path.join(repo_path, f)):
                    detected_type = repo_type
                    detected_files.append(f)
                    break
            if detected_type:
                break

        context.repository_type = detected_type
        context.strategy_name = detected_type or "generic"

        return StepResult.ok(
            detected_type,
            detected_files=detected_files,
        )


class DiscoverDocsStep(PipelineStepBase):
    """Find documentation files in the repository."""

    name = "discover_docs"

    def execute(self, context: PipelineContext) -> StepResult:
        """Find documentation files."""
        from ..tools.repository import RepositoryHandler

        handler = RepositoryHandler()

        try:
            doc_files = handler.find_documentation_files(context.repo_path)
            context.doc_files = doc_files
            return StepResult.ok(doc_files, count=len(doc_files))

        except Exception as e:
            return StepResult.fail(f"Failed to find docs: {e}")


class ParseCommandsStep(PipelineStepBase):
    """Parse commands from documentation files."""

    name = "parse_commands"

    def execute(self, context: PipelineContext) -> StepResult:
        """Extract commands from documentation."""
        from ..tools.parser import DocumentationParser
        from ..tools.repository import RepositoryHandler
        from .models import ParsedCommand

        parser = DocumentationParser()
        handler = RepositoryHandler()

        all_commands = []

        for doc_file in context.doc_files:
            try:
                content = handler.read_documentation_content(doc_file)
                commands = parser.get_installation_commands(content, doc_file)

                # Convert to domain model
                for cmd in commands:
                    parsed = ParsedCommand(
                        text=cmd.text,
                        source=cmd.source.value,
                        command_type=cmd.command_type.value if cmd.command_type else "shell",
                        context=cmd.context,
                        line_number=cmd.line_number,
                        file_path=cmd.file_path,
                        priority=cmd.priority,
                    )
                    all_commands.append(parsed)

            except Exception as e:
                logger.warning(f"Error parsing {doc_file}: {e}")

        # Deduplicate and prioritize
        unique_commands = self._deduplicate(all_commands)
        prioritized = sorted(unique_commands, key=lambda c: -c.priority)

        context.commands = prioritized

        return StepResult.ok(
            prioritized,
            total_found=len(all_commands),
            unique_count=len(prioritized),
        )

    def _deduplicate(self, commands: List["ParsedCommand"]) -> List["ParsedCommand"]:
        """Remove duplicate commands, keeping highest priority."""
        seen = {}
        for cmd in commands:
            key = cmd.text.strip()
            if key not in seen or cmd.priority > seen[key].priority:
                seen[key] = cmd
        return list(seen.values())


class ValidateCommandsStep(PipelineStepBase):
    """Validate commands against security policies."""

    name = "validate_commands"
    retryable = False

    def __init__(self, policies=None):
        self._policies = policies or []

    def execute(self, context: PipelineContext) -> StepResult:
        """Apply policy checks to commands."""
        from .events import PolicyViolation, get_event_bus

        bus = get_event_bus()
        violations = []

        for cmd in context.commands:
            # Basic dangerous pattern check
            dangerous = [
                ("rm -rf /", "Destructive root deletion"),
                ("rm -rf /*", "Destructive wildcard deletion"),
                ("> /dev/sda", "Disk overwrite"),
                ("mkfs", "Filesystem format"),
                (":(){:|:&};:", "Fork bomb"),
                ("dd if=/dev/random", "Disk wipe"),
                ("| bash", "Remote code execution"),
                ("| sh", "Remote code execution"),
            ]

            for pattern, reason in dangerous:
                if pattern in cmd.text:
                    cmd.allowed = False
                    cmd.policy_violations.append(f"{pattern}: {reason}")
                    violations.append((cmd, pattern, reason))

                    bus.emit(PolicyViolation(
                        run_id=context.run_id,
                        command=cmd.text,
                        policy_name="dangerous_patterns",
                        reason=reason,
                        severity="critical",
                    ))

        # If any critical violations, gate the run
        if violations:
            context.awaiting_user_input = True
            return StepResult.ok(
                violations,
                violation_count=len(violations),
                gated=True,
            )

        return StepResult.ok(None, violation_count=0)


class ExecuteCommandsStep(PipelineStepBase):
    """Execute commands in container."""

    name = "execute"
    retryable = False

    def __init__(self, docker_executor=None, test_mode: bool = False):
        self._executor = docker_executor
        self._test_mode = test_mode

    def execute(self, context: PipelineContext) -> StepResult:
        """Execute commands."""
        from ..tools.docker import DockerExecutor
        from .models import CommandLog, CommandStatus
        from .events import (
            CommandQueued, CommandStarted, CommandCompleted,
            get_event_bus,
        )

        bus = get_event_bus()

        executor = self._executor or DockerExecutor(test_mode=self._test_mode)

        # Filter to allowed commands
        allowed_commands = [c for c in context.commands if c.allowed]

        if not allowed_commands:
            return StepResult.ok([], message="No commands to execute")

        # Start container
        container_id = executor.start_container(context.repo_path)
        if not container_id:
            return StepResult.fail("Failed to start container")

        results = []
        all_success = True

        try:
            for cmd in allowed_commands:
                # Emit queued event
                bus.emit(CommandQueued(
                    run_id=context.run_id,
                    command=cmd.text,
                    priority=cmd.priority,
                    command_type=cmd.command_type,
                ))

                # Emit started event
                bus.emit(CommandStarted(
                    run_id=context.run_id,
                    command=cmd.text,
                    container_id=container_id,
                ))

                # Execute
                result = executor.execute_command(cmd.text)

                # Convert to domain model
                cmd_log = CommandLog(
                    id=0,  # Will be set by DB
                    run_id=context.run_id,
                    command=cmd.text,
                    status=CommandStatus.SUCCESS if result.successful else CommandStatus.FAILED,
                    timestamp=datetime.now(),
                    exit_code=result.exit_code,
                    output=result.output,
                    error=result.error,
                    execution_time=result.execution_time,
                    command_type=cmd.command_type,
                    priority=cmd.priority,
                )
                results.append(cmd_log)

                # Emit completed event
                bus.emit(CommandCompleted(
                    run_id=context.run_id,
                    command=cmd.text,
                    exit_code=result.exit_code,
                    output=result.output,
                    error=result.error,
                    execution_time=result.execution_time,
                ))

                # Stop on failure
                if not result.successful:
                    all_success = False
                    break

        finally:
            executor.stop_container()

        context.results = results

        if all_success:
            return StepResult.ok(results, executed=len(results))
        else:
            return StepResult.fail(
                f"Command failed: {results[-1].command}",
                recoverable=False,
            )


class SummarizeStep(PipelineStepBase):
    """Generate run summary."""

    name = "summarize"
    retryable = False

    def execute(self, context: PipelineContext) -> StepResult:
        """Generate summary of the run."""
        results = context.results

        total = len(results)
        successful = sum(1 for r in results if r.successful)
        failed = total - successful

        if failed == 0:
            summary = f"Executed {total} commands successfully."
        else:
            summary = f"Executed {total} commands: {successful} successful, {failed} failed."

        context.add_metadata("summary", summary)
        context.add_metadata("total_commands", total)
        context.add_metadata("successful_commands", successful)
        context.add_metadata("failed_commands", failed)

        return StepResult.ok(summary)


# =============================================================================
# PIPELINE FACTORY
# =============================================================================

def create_default_pipeline(
    test_mode: bool = False,
    event_bus: Optional[EventBus] = None,
) -> Pipeline:
    """
    Create a pipeline with all default steps.

    Args:
        test_mode: Whether to run in test mode
        event_bus: Event bus to use

    Returns:
        Configured Pipeline instance
    """
    pipeline = Pipeline(event_bus=event_bus)

    pipeline.add_step(CloneStep())
    pipeline.add_step(DetectStrategyStep())
    pipeline.add_step(DiscoverDocsStep())
    pipeline.add_step(ParseCommandsStep())
    pipeline.add_step(ValidateCommandsStep())
    pipeline.add_step(ExecuteCommandsStep(test_mode=test_mode))
    pipeline.add_step(SummarizeStep())

    return pipeline
