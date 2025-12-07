#!/usr/bin/env python3
"""Command-line demo for NovaSystem (guided, end-to-end).

This script walks through:
1) Building a throwaway repo with mixed install docs.
2) Running NovaSystem against it (test-mode by default, Docker optional).
3) Showing run history + stored docs/commands.
4) (Optional) Gemini image generation + image understanding if GEMINI_API_KEY is set.
"""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
from textwrap import dedent
from typing import List

from novasystem.nova import Nova


def build_demo_repository(root: Path) -> Path:
    """Create a throwaway repository with installation docs and commands."""
    repo_dir = root / "nova_demo_repo"
    docs_dir = repo_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    (repo_dir / "requirements.txt").write_text("requests==2.32.3\n", encoding="utf-8")

    readme_content = dedent(
        """\
        # NovaSystem Demo Repository

        This fake repository is only here to show how NovaSystem reads docs,
        extracts install commands, and runs them in an isolated environment.

        Typical setup commands:

        ```bash
        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
        python -m pytest
        ```

        Optional container workflow:

        ```bash
        docker build -t novasystem-demo .
        docker run --rm novasystem-demo --help
        ```
        """
    )
    (repo_dir / "README.md").write_text(readme_content, encoding="utf-8")

    install_content = dedent(
        """\
        # Deployment Notes

        These notes intentionally mix ecosystems so NovaSystem can show its
        command deduplication and prioritization.

        ```bash
        npm install
        npm run build
        npm test
        ```

        ```bash
        pip install -e .
        novasystem --version
        novasystem list-runs --db-path /workspace/novasystem_demo.db
        ```
        """
    )
    (docs_dir / "INSTALL.md").write_text(install_content, encoding="utf-8")

    return repo_dir


def print_results(result: dict) -> None:
    """Pretty-print the install summary."""
    print("\n=== Install Summary ===")
    print(f"Repository: {result.get('repository')}")
    print(f"Run ID: {result.get('run_id')}")
    print(f"Status: {'success' if result.get('success') else 'failed'}")
    print(f"Execution time: {result.get('execution_time', 0):.2f}s")

    executed = result.get("results") or []
    print(f"Commands executed: {len(executed)}")
    for idx, cmd in enumerate(executed, 1):
        status = "ok" if cmd.get("successful") else "failed"
        exit_code = cmd.get("exit_code")
        snippet = (cmd.get("output") or "").splitlines()
        first_line = snippet[0] if snippet else ""
        print(f"  {idx}. {cmd.get('command')} [{status}, exit {exit_code}] {first_line}")


class Stepper:
    def __init__(self) -> None:
        self._step = 0

    def section(self, title: str) -> None:
        self._step += 1
        print(f"\n[{self._step}] {title}")
        print("-" * (len(title) + 4))


def try_import_gemini():
    try:
        from google import genai  # type: ignore
        from google.genai import types  # type: ignore
        from PIL import Image, ImageDraw  # type: ignore
    except ImportError as exc:
        return None, None, None, exc
    return genai, types, (Image, ImageDraw), None


def ensure_out_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_sample_canvas(path: Path, Image, ImageDraw) -> Path:
    """Create a simple local image to feed into vision understanding."""
    img = Image.new("RGB", (720, 432), (245, 247, 252))
    draw = ImageDraw.Draw(img)

    draw.rectangle((40, 40, 350, 220), outline=(52, 108, 205), width=4, fill=(225, 235, 255))
    draw.rectangle((380, 60, 680, 260), outline=(84, 160, 92), width=4, fill=(222, 242, 224))
    draw.ellipse((90, 250, 250, 410), outline=(205, 140, 52), width=4, fill=(250, 230, 200))

    draw.text((60, 70), "NovaSystem Vision Demo", fill=(20, 45, 90))
    draw.text((400, 90), "Gemini counts shapes", fill=(30, 70, 30))
    draw.text((110, 300), "orange circle-ish", fill=(120, 70, 20))

    img.save(path)
    return path


def run_gemini_segment(
    model_gen: str,
    model_vision: str,
    prompt: str,
    vision_prompt: str,
    out_dir: Path,
) -> None:
    genai, types, pillow_mods, import_err = try_import_gemini()
    if import_err:
        print(f"Skipping Gemini segment: {import_err}. Install with `pip install google-genai pillow`.")
        return

    if not os.getenv("GEMINI_API_KEY"):
        print("Skipping Gemini segment: GEMINI_API_KEY not set.")
        return

    Image, ImageDraw = pillow_mods
    ensure_out_dir(out_dir)

    client = genai.Client()

    print(f"- Generating image with model: {model_gen}")
    try:
        response_gen = client.models.generate_content(model=model_gen, contents=[prompt])
    except Exception as exc:  # noqa: BLE001
        print(f"  Gemini generation failed: {exc}")
        return

    saved: List[Path] = []
    for i, part in enumerate(response_gen.parts):
        if part.inline_data is not None:
            image = part.as_image()
            path = out_dir / f"gemini_generated_{i}.png"
            image.save(path)
            saved.append(path)
        elif part.text is not None:
            (out_dir / f"gemini_generated_{i}.txt").write_text(part.text, encoding="utf-8")

    if saved:
        print(f"  Saved {len(saved)} generated image(s):")
        for p in saved:
            print(f"    - {p}")
    else:
        print("  No image parts returned by generation model.")

    sample_img = build_sample_canvas(out_dir / "vision_sample.png", Image, ImageDraw)
    contents = [
        types.Part.from_bytes(data=sample_img.read_bytes(), mime_type="image/png"),
        vision_prompt,
    ]

    print(f"- Vision understanding with model: {model_vision}")
    try:
        vision_resp = client.models.generate_content(model=model_vision, contents=contents)
        text = vision_resp.text or ""
        (out_dir / "vision_result.txt").write_text(text, encoding="utf-8")
        print("  Vision response saved to vision_result.txt")
        print("  Preview:")
        print("  ", text.strip()[:500] + ("..." if len(text) > 500 else ""))
    except Exception as exc:  # noqa: BLE001
        print(f"  Gemini vision failed: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a self-contained NovaSystem demo from the repo root."
    )
    parser.add_argument(
        "--db-path",
        default=Path(__file__).with_name("novasystem_demo.db"),
        help="Path to the demo SQLite database (default: ./novasystem_demo.db).",
    )
    parser.add_argument(
        "--use-docker",
        action="store_true",
        help="Execute commands in Docker instead of the safe simulated mode.",
    )
    parser.add_argument(
        "--keep-repo",
        action="store_true",
        help="Keep the generated demo repository on disk for inspection.",
    )
    parser.add_argument(
        "--with-gemini",
        action="store_true",
        help="Also run the Gemini image generation + vision-understanding segment (requires GEMINI_API_KEY). "
        "If GEMINI_API_KEY is set, the segment will run even without this flag.",
    )
    parser.add_argument(
        "--gemini-model-gen",
        default="gemini-2.5-flash-image",
        help="Gemini model for image generation.",
    )
    parser.add_argument(
        "--gemini-model-vision",
        default="gemini-2.5-flash",
        help="Gemini model for image understanding (text+image).",
    )
    parser.add_argument(
        "--gemini-prompt",
        default="Create a Gemini-themed lab with holographic dashboards and a nano banana mascot.",
        help="Prompt for image generation.",
    )
    parser.add_argument(
        "--gemini-vision-prompt",
        default="Describe the scene, list dominant colors, and count the geometric shapes.",
        help="Prompt paired with the synthetic image for vision understanding.",
    )
    parser.add_argument(
        "--out-dir",
        default="novasystem_demo_outputs",
        help="Directory to save demo artifacts (Nova + Gemini).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    test_mode = not args.use_docker
    db_path = Path(args.db_path)
    out_dir = Path(args.out_dir)
    step = Stepper()

    temp_dir_obj = None
    if args.keep_repo:
        demo_root = Path(tempfile.mkdtemp(prefix="novasystem-demo-"))
    else:
        temp_dir_obj = tempfile.TemporaryDirectory(prefix="novasystem-demo-")
        demo_root = Path(temp_dir_obj.name)

    print("NovaSystem CLI Demo (guided)")
    print("============================")
    print(f"Mode: {'test (no Docker needed)' if test_mode else 'Docker-backed'}")
    print(f"Database: {db_path}")
    print(f"Artifacts: {out_dir}")

    step.section("Prepare demo repository")
    repo_path = build_demo_repository(demo_root)
    print(f"- Created synthetic repo at {repo_path}")

    try:
        step.section("Run NovaSystem against the demo repo")
        print(f"- Instantiating NovaSystem (test_mode={test_mode})")
        nova = Nova(db_path=str(db_path), test_mode=test_mode)
        result = nova.process_repository(str(repo_path), mount_local=True)
    except Exception as exc:
        print(f"\nDemo failed: {exc}")
        return 1
    finally:
        if temp_dir_obj:
            temp_dir_obj.cleanup()
        elif args.keep_repo:
            print(f"Demo repository kept at: {repo_path}")

    step.section("Review install summary")
    print_results(result)

    run_id = result.get("run_id")
    nova = Nova(db_path=str(db_path), test_mode=test_mode)
    runs = nova.list_runs(limit=5)

    step.section("Show recent runs")
    print("\n=== Recent Runs (from the demo database) ===")
    if runs:
        for run in runs:
            success = (
                "yes" if run.get("success") else "no" if run.get("success") is False else "-"
            )
            print(
                f"#{run['id']} | {run['repo_url']} | status: {run['status']} | success: {success}"
            )
    else:
        print("No runs found.")

    if run_id:
        details = nova.get_run_details(run_id)
        commands = details.get("commands") or []
        docs = details.get("documentation") or []

        step.section("Inspect stored artifacts")
        print("\n=== Stored Documentation ===")
        if docs:
            for doc in docs:
                print(f"- {doc['file_path']} ({len(doc.get('content', ''))} bytes)")
        else:
            print("No documentation stored.")

        print("\n=== Command Log ===")
        if commands:
            for idx, cmd in enumerate(commands, 1):
                status = cmd.get("status") or "unknown"
                print(
                    f"{idx}. {cmd['command']} | status: {status} | exit: {cmd.get('exit_code')}"
                )
        else:
            print("No command records found.")

    should_run_gemini = args.with_gemini or bool(os.getenv("GEMINI_API_KEY"))
    if should_run_gemini:
        step.section("Gemini image generation + vision understanding (optional)")
        run_gemini_segment(
            model_gen=args.gemini_model_gen,
            model_vision=args.gemini_model_vision,
            prompt=args.gemini_prompt,
            vision_prompt=args.gemini_vision_prompt,
            out_dir=out_dir,
        )
    else:
        step.section("Gemini segment (skipped)")
        print(
            "Set GEMINI_API_KEY and optionally pass --with-gemini to include image generation "
            "and image understanding in the demo."
        )

    print("\nDone. Re-run with --use-docker once Docker is available to exercise the full stack.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
