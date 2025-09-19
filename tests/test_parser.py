import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from novasystem.parser import Command, CommandSource, CommandType, DocumentationParser


def _make_command(text: str, priority: int) -> Command:
    return Command(
        text=text,
        source=CommandSource.CODE_BLOCK,
        command_type=CommandType.SHELL,
        priority=priority,
    )


def test_deduplicate_commands_prefers_higher_priority():
    parser = DocumentationParser()
    commands = [
        _make_command("pip install example", priority=10),
        _make_command("pip install example", priority=80),
        _make_command("npm install other", priority=60),
        _make_command("npm install other", priority=20),
    ]

    deduped = parser.deduplicate_commands(commands)

    assert len(deduped) == 2
    command_texts = {cmd.text: cmd for cmd in deduped}
    assert command_texts["pip install example"].priority == 80
    assert command_texts["npm install other"].priority == 60


def test_get_installation_commands_deduplicates():
    parser = DocumentationParser()
    content = """
```bash
pip install package
```

Install via inline `pip install package` if needed.
"""

    commands = parser.get_installation_commands(content)

    occurrences = [cmd for cmd in commands if cmd.text == "pip install package"]
    assert len(occurrences) == 1
    assert occurrences[0].priority >= 50
