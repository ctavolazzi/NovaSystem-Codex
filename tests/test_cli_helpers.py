import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Ensure the repository root is importable when running the tests without an
# installed package (e.g., in CI or fresh clones).
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import novasystem.cli as cli


class DummyNova:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def test_create_nova_without_db_path(monkeypatch):
    created = []

    def _factory(*args, **kwargs):
        nova = DummyNova(*args, **kwargs)
        created.append(nova)
        return nova

    monkeypatch.setattr(cli, "Nova", _factory)

    args = SimpleNamespace()  # no db_path attribute
    nova = cli._create_nova(args)

    assert isinstance(nova, DummyNova)
    assert created[0].kwargs == {}


def test_create_nova_with_db_path(monkeypatch, tmp_path):
    created = []

    def _factory(*args, **kwargs):
        nova = DummyNova(*args, **kwargs)
        created.append(nova)
        return nova

    monkeypatch.setattr(cli, "Nova", _factory)

    args = argparse.Namespace(db_path=tmp_path / "nova.db")
    nova = cli._create_nova(args)

    assert isinstance(nova, DummyNova)
    assert created[0].kwargs == {"db_path": args.db_path}


def test_install_repository_uses_helper(monkeypatch, capsys):
    created_args = []

    class StubNova:
        def __init__(self):
            self.calls = []

        def process_repository(self, repository, mount_local, detect_type):
            self.calls.append((repository, mount_local, detect_type))
            return {
                "repository": repository,
                "success": True,
                "message": "ok",
                "run_id": 1,
                "execution_time": 0.1,
            }

    stub = StubNova()

    def fake_create(args):
        created_args.append(args)
        return stub

    monkeypatch.setattr(cli, "_create_nova", fake_create)

    args = argparse.Namespace(
        repository="https://example.com/repo.git",
        mount=True,
        no_detect=False,
        output="json",
        verbose=False,
    )

    exit_code = cli.install_repository(args)

    assert exit_code == 0
    assert created_args == [args]
    assert stub.calls == [(args.repository, args.mount, not args.no_detect)]

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["repository"] == args.repository
    assert payload["success"] is True


def test_install_repository_handles_exception(monkeypatch, capsys):
    class StubNova:
        def process_repository(self, repository, mount_local, detect_type):
            raise RuntimeError("explode")

    monkeypatch.setattr(cli, "_create_nova", lambda args: StubNova())

    args = argparse.Namespace(
        repository="repo",
        mount=False,
        no_detect=False,
        output="json",
        verbose=False,
    )

    exit_code = cli.install_repository(args)

    assert exit_code == 1
    assert "explode" in capsys.readouterr().out


def test_list_runs_uses_helper(monkeypatch, capsys):
    created_args = []

    class StubNova:
        def __init__(self):
            self.calls = []

        def list_runs(self, limit, offset, status):
            self.calls.append((limit, offset, status))
            return [
                {
                    "id": 1,
                    "repo_url": "repo",
                    "status": "completed",
                    "success": True,
                    "start_time": datetime.now().isoformat(),
                }
            ]

    stub = StubNova()

    def fake_create(args):
        created_args.append(args)
        return stub

    monkeypatch.setattr(cli, "_create_nova", fake_create)

    args = argparse.Namespace(limit=5, offset=0, status=None, output="json", verbose=False)

    exit_code = cli.list_runs(args)

    assert exit_code == 0
    assert created_args == [args]
    assert stub.calls == [(args.limit, args.offset, args.status)]

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload[0]["repo_url"] == "repo"
    assert payload[0]["status"] == "completed"


def test_list_runs_handles_exception(monkeypatch, capsys):
    class StubNova:
        def list_runs(self, limit, offset, status):
            raise RuntimeError("db down")

    monkeypatch.setattr(cli, "_create_nova", lambda args: StubNova())

    args = argparse.Namespace(limit=1, offset=0, status=None, output="json", verbose=False)

    exit_code = cli.list_runs(args)

    assert exit_code == 1
    assert "db down" in capsys.readouterr().out


def test_install_repository_reports_failure(monkeypatch, capsys):
    class StubNova:
        def process_repository(self, repository, mount_local, detect_type):
            return {
                "repository": repository,
                "success": False,
                "message": "failed",
                "run_id": 10,
                "execution_time": 0.2,
            }

    monkeypatch.setattr(cli, "_create_nova", lambda args: StubNova())

    args = argparse.Namespace(
        repository="repo",
        mount=False,
        no_detect=False,
        output="json",
        verbose=False,
    )

    exit_code = cli.install_repository(args)

    assert exit_code == 1

    payload = json.loads(capsys.readouterr().out)
    assert payload["run_id"] == 10
    assert payload["success"] is False


def test_show_run_uses_helper(monkeypatch, capsys):
    created_args = []

    class StubNova:
        def __init__(self):
            self.calls = []

        def get_run_details(self, run_id):
            self.calls.append(run_id)
            now = datetime.now()
            return {
                "run": {
                    "id": run_id,
                    "repo_url": "repo",
                    "status": "completed",
                    "success": True,
                    "start_time": now.isoformat(),
                    "end_time": (now + timedelta(seconds=1)).isoformat(),
                },
                "commands": [
                    {
                        "command": "echo test",
                        "status": "completed",
                        "timestamp": now.isoformat(),
                        "exit_code": 0,
                        "execution_time": 0.1,
                        "output": "ok",
                    }
                ],
                "documentation": [
                    {"file_path": "README.md", "content": "docs"},
                ],
            }

    stub = StubNova()

    def fake_create(args):
        created_args.append(args)
        return stub

    monkeypatch.setattr(cli, "_create_nova", fake_create)

    args = argparse.Namespace(run_id=42, output="json", verbose=False)

    exit_code = cli.show_run(args)

    assert exit_code == 0
    assert created_args == [args]
    assert stub.calls == [args.run_id]

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["run"]["id"] == args.run_id
    assert payload["documentation"][0]["file_path"] == "README.md"


def test_show_run_reports_error(monkeypatch, capsys):
    class StubNova:
        def get_run_details(self, run_id):
            return {"error": "missing"}

    monkeypatch.setattr(cli, "_create_nova", lambda args: StubNova())

    args = argparse.Namespace(run_id=5, output="json", verbose=False)

    exit_code = cli.show_run(args)

    assert exit_code == 1
    assert "missing" in capsys.readouterr().out


def test_delete_run_uses_helper(monkeypatch, capsys):
    created_args = []

    class StubNova:
        def __init__(self):
            self.calls = []

        def delete_run(self, run_id):
            self.calls.append(run_id)
            return True

    stub = StubNova()

    def fake_create(args):
        created_args.append(args)
        return stub

    monkeypatch.setattr(cli, "_create_nova", fake_create)

    args = argparse.Namespace(run_id=99, verbose=False)

    exit_code = cli.delete_run(args)

    assert exit_code == 0
    assert created_args == [args]
    assert stub.calls == [args.run_id]

    captured = capsys.readouterr()
    assert "deleted successfully" in captured.out


def test_delete_run_handles_failure(monkeypatch, capsys):
    class StubNova:
        def delete_run(self, run_id):
            return False

    monkeypatch.setattr(cli, "_create_nova", lambda args: StubNova())

    args = argparse.Namespace(run_id=77, verbose=False)

    exit_code = cli.delete_run(args)

    assert exit_code == 1
    assert "Failed to delete run" in capsys.readouterr().out


def test_cleanup_runs_uses_helper(monkeypatch, capsys):
    created_args = []

    class StubNova:
        def __init__(self):
            self.calls = []

        def cleanup_old_runs(self, days):
            self.calls.append(days)
            return 3

    stub = StubNova()

    def fake_create(args):
        created_args.append(args)
        return stub

    monkeypatch.setattr(cli, "_create_nova", fake_create)

    args = argparse.Namespace(days=7, verbose=False)

    exit_code = cli.cleanup_runs(args)

    assert exit_code == 0
    assert created_args == [args]
    assert stub.calls == [args.days]

    captured = capsys.readouterr()
    assert "Deleted 3 runs" in captured.out


def test_cleanup_runs_handles_exception(monkeypatch, capsys):
    class StubNova:
        def cleanup_old_runs(self, days):
            raise RuntimeError("boom")

    monkeypatch.setattr(cli, "_create_nova", lambda args: StubNova())

    args = argparse.Namespace(days=1, verbose=False)

    exit_code = cli.cleanup_runs(args)

    assert exit_code == 1
    assert "boom" in capsys.readouterr().out
