"""Unit tests for documentation discovery helpers in RepositoryHandler."""

from novasystem.repository import RepositoryHandler


def test_find_documentation_files_prioritized(tmp_path):
    repo_handler = RepositoryHandler()

    readme = tmp_path / "README.md"
    install = tmp_path / "INSTALL.md"
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    nested_readme = docs_dir / "README.rst"
    extra_doc = docs_dir / "guide.md"

    readme.write_text("Root README", encoding="utf-8")
    install.write_text("Installation instructions", encoding="utf-8")
    nested_readme.write_text("Docs README", encoding="utf-8")
    extra_doc.write_text("Additional guide", encoding="utf-8")

    results = repo_handler.find_documentation_files(str(tmp_path))

    assert results == [
        str(readme.resolve()),
        str(install.resolve()),
        str(nested_readme.resolve()),
        str(extra_doc.resolve()),
    ]


def test_find_documentation_files_returns_empty_when_missing(tmp_path):
    repo_handler = RepositoryHandler()

    results = repo_handler.find_documentation_files(str(tmp_path))

    assert results == []


def test_find_documentation_files_uses_last_cloned_repo(tmp_path):
    repo_handler = RepositoryHandler()

    repo_root = tmp_path / "cloned"
    repo_root.mkdir()
    readme = repo_root / "README.md"
    readme.write_text("Cloned README", encoding="utf-8")

    repo_handler.repo_dir = str(repo_root)

    results = repo_handler.find_documentation_files()

    assert results == [str(readme.resolve())]


def test_read_documentation_content(tmp_path):
    repo_handler = RepositoryHandler()

    doc_file = tmp_path / "README.md"
    doc_file.write_text("Some documentation", encoding="utf-8")

    content = repo_handler.read_documentation_content(doc_file)

    assert content == "Some documentation"
