"""Integration-style tests ensuring repositories are mounted for command execution."""

import subprocess
from typing import Optional

from novasystem.nova import Nova
from novasystem.docker import CommandResult


class StubDockerExecutor:
    """Minimal Docker executor that runs commands on the host for testing."""

    def __init__(self):
        self.started_with = None
        self.executed_commands = []
        self.mounted_repo_dir = None

    def check_image_exists(self) -> bool:  # pragma: no cover - trivial stub
        return True

    def create_image(self) -> bool:  # pragma: no cover - trivial stub
        return True

    def start_container(self, repo_dir: Optional[str] = None) -> str:
        assert repo_dir is not None, "Expected repository directory to be mounted"
        self.started_with = repo_dir
        self.mounted_repo_dir = repo_dir
        return "stub-container"

    def execute_command(self, command: str) -> CommandResult:
        assert self.mounted_repo_dir is not None, "Repository not mounted"
        completed = subprocess.run(
            command,
            shell=True,
            cwd=self.mounted_repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        result = CommandResult(
            command=command,
            exit_code=completed.returncode,
            output=completed.stdout,
            error=completed.stderr,
            execution_time=0.0,
            status="completed" if completed.returncode == 0 else "error",
        )
        self.executed_commands.append(result)
        return result

    def stop_container(self) -> bool:  # pragma: no cover - trivial stub
        return True


def test_remote_clone_commands_can_access_repository(tmp_path, monkeypatch):
    """Commands extracted from documentation should run against the cloned repo."""

    repo_dir = tmp_path / "remote_repo"
    repo_dir.mkdir()

    documentation = repo_dir / "README.md"
    documentation.write_text(
        """# Example

```bash
cat README.md
```
""",
        encoding="utf-8",
    )

    db_path = tmp_path / "nova-test.db"
    nova = Nova(db_path=str(db_path), test_mode=True)

    def fake_clone(url: str) -> str:  # pragma: no cover - executed via Nova
        nova.repo_handler.repo_dir = str(repo_dir)
        nova.repo_handler.repo_url = url
        return str(repo_dir)

    monkeypatch.setattr(nova.repo_handler, "clone_repository", fake_clone)
    monkeypatch.setattr(
        nova.repo_handler,
        "find_documentation_files",
        lambda _: [str(documentation)],
    )

    stub_executor = StubDockerExecutor()
    nova.docker_executor = stub_executor

    result = nova.process_repository("https://example.com/example/repo.git", detect_type=False)

    assert result["success"] is True
    assert stub_executor.started_with == str(repo_dir)
    assert stub_executor.executed_commands, "Expected at least one executed command"
    executed = stub_executor.executed_commands[0]
    assert executed.successful
    assert "Example" in executed.output
