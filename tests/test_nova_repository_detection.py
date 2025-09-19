"""Tests for Nova repository processing metadata handling."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.nova import Nova


def test_process_repository_records_detected_type(tmp_path, monkeypatch):
    """Ensure Nova can persist detected repository type metadata without errors."""

    repo_dir = tmp_path / "sample_repo"
    repo_dir.mkdir()
    # Presence of a requirements file should trigger Python detection
    (repo_dir / "requirements.txt").write_text("flask==2.0.0\n", encoding="utf-8")

    db_path = tmp_path / "nova-test.db"
    nova = Nova(db_path=str(db_path), test_mode=True)

    # Avoid heavy repository and command processing by stubbing discovery
    monkeypatch.setattr(
        nova.repo_handler,
        "find_documentation_files",
        lambda path: [],
        raising=False,
    )

    result = nova.process_repository(str(repo_dir), detect_type=True)

    assert result["run_id"] > 0

    run_record = nova.db_manager.get_run(result["run_id"])
    assert run_record is not None
    assert run_record.get("metadata", {}).get("repository_type") == "python"
