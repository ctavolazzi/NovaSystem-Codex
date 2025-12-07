#!/usr/bin/env python3
"""Advanced Gemini image demo: generation + vision understanding.

Run from the repo root after installing dependencies:
  python gemini_image_demo.py --prompt "futuristic nano banana ad, neon blues"

The script:
1) Generates an image with the requested prompt (default: gemini-2.5-flash-image).
2) Builds a synthetic test image locally and asks a vision model to describe it.

Requirements:
- Environment variable GEMINI_API_KEY must be set.
- pip install google-genai pillow
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List

from PIL import Image, ImageDraw
from google import genai
from google.genai import types


def ensure_output_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def build_sample_canvas(path: Path) -> Path:
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


def save_inline_image(part: types.Part, base: Path, idx: int) -> Path:
    """Persist an inline image part to disk."""
    image = part.as_image()
    suffix = ".png"
    out_path = base / f"generated_{idx}{suffix}"
    image.save(out_path)
    return out_path


def run_generation(client: genai.Client, model: str, prompt: str, out_dir: Path) -> List[Path]:
    """Generate an image from text and save all returned image parts."""
    response = client.models.generate_content(model=model, contents=[prompt])

    saved: List[Path] = []
    base = ensure_output_dir(out_dir)
    for i, part in enumerate(response.parts):
        if part.inline_data is not None:
            saved.append(save_inline_image(part, base, i))
        elif part.text is not None:
            (base / f"generated_{i}.txt").write_text(part.text, encoding="utf-8")
    return saved


def run_vision_understanding(
    client: genai.Client, model: str, image_path: Path, prompt: str
) -> str:
    """Send a local image and a prompt to a multimodal model and return the text."""
    image_bytes = image_path.read_bytes()
    contents = [
        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        prompt,
    ]
    response = client.models.generate_content(model=model, contents=contents)
    return response.text or ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gemini image generation + vision understanding demo."
    )
    parser.add_argument(
        "--prompt",
        default="Create a Gemini-themed lab scene with holographic dashboards and a nano banana mascot.",
        help="Text prompt for image generation.",
    )
    parser.add_argument(
        "--model-gen",
        default="gemini-2.5-flash-image",
        help="Model for image generation (e.g., gemini-2.5-flash-image, gemini-3-pro-image-preview).",
    )
    parser.add_argument(
        "--model-vision",
        default="gemini-2.5-flash",
        help="Model for image understanding (text+image, e.g., gemini-2.5-flash or gemini-2.5-pro).",
    )
    parser.add_argument(
        "--out-dir",
        default="gemini_demo_outputs",
        help="Directory to save generated images and artifacts.",
    )
    parser.add_argument(
        "--vision-prompt",
        default="Describe the scene, list the dominant colors, and count the geometric shapes.",
        help="Prompt sent along with the synthetic test image for vision understanding.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY is not set. Please export your key and rerun.")
        return 1

    out_dir = Path(args.out_dir)
    client = genai.Client()

    print(f"[1/2] Generating image with model {args.model_gen} ...")
    generated_paths = run_generation(client, args.model_gen, args.prompt, out_dir)
    if generated_paths:
        print(f"Saved {len(generated_paths)} generated image(s) to {out_dir}")
    else:
        print("No image parts returned by the generation model.")

    print(f"\n[2/2] Vision understanding with model {args.model_vision} ...")
    synthetic_image = build_sample_canvas(out_dir / "vision_sample.png")
    vision_text = run_vision_understanding(client, args.model_vision, synthetic_image, args.vision_prompt)
    (out_dir / "vision_result.txt").write_text(vision_text, encoding="utf-8")
    print("Vision response:")
    print(vision_text)

    print(f"\nDone. Artifacts in: {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
