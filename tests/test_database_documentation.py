"""Tests covering documentation storage and retrieval behavior."""

import argparse
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.database import DatabaseManager
from novasystem.nova import Nova
from novasystem import cli


def test_database_manager_roundtrips_documentation(tmp_path):
    """Documentation metadata should be stored as JSON and parsed back to dicts."""

    db_path = tmp_path / "documentation.db"
    manager = DatabaseManager(str(db_path))

    run_id = manager.create_run("https://example.com/repo.git")

    metadata = {"file_size": 42, "checksum": "deadbeef"}
    manager.store_documentation(
        run_id,
        "docs/README.md",
        "Installation steps",
        metadata=metadata,
    )

    docs = manager.get_documentation(run_id)

    assert len(docs) == 1
    doc = docs[0]

    assert doc["file_path"] == "docs/README.md"
    assert doc["content"] == "Installation steps"
    # Metadata should be parsed from JSON back into a dictionary
    assert doc["metadata"] == metadata


def test_nova_get_run_details_includes_documentation(tmp_path):
    """Nova exposes documentation records to downstream consumers."""

    db_path = tmp_path / "nova_details.db"
    nova = Nova(db_path=str(db_path), test_mode=True)

    run_id = nova.db_manager.create_run("https://example.com/awesome.git")
    nova.db_manager.store_documentation(
        run_id,
        "README.md",
        "Usage information",
        metadata={"file_size": 17},
    )

    details = nova.get_run_details(run_id)

    assert "documentation" in details
    docs = details["documentation"]
    assert isinstance(docs, list)
    assert len(docs) == 1
    assert docs[0]["metadata"] == {"file_size": 17}


def test_cli_show_run_outputs_documentation(monkeypatch, capsys):
    """The CLI should display documentation returned by Nova.get_run_details."""

    dummy_result = {
        "run": {
            "id": 7,
            "repo_url": "https://example.com/repo.git",
            "status": "completed",
            "start_time": datetime.now().isoformat(),
        },
        "commands": [],
        "documentation": [
            {
                "id": 1,
                "file_path": "README.md",
                "content": "Install by running make",
                "metadata": {"file_size": 24},
            }
        ],
    }

    class DummyNova:
        def __init__(self):
            self.run_ids = []

        def get_run_details(self, run_id):
            self.run_ids.append(run_id)
            return dummy_result

    dummy_nova = DummyNova()
    monkeypatch.setattr(cli, "Nova", lambda: dummy_nova)

    args = argparse.Namespace(run_id=7, verbose=False, output="text")
    exit_code = cli.show_run(args)

    captured = capsys.readouterr()

    assert exit_code == 0
    assert dummy_nova.run_ids == [7]
    assert "Documentation Files (1):" in captured.out
    assert "README.md" in captured.out

