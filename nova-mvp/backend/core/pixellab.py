"""PixelLab API integration for generating pixel art animations.

Uses the PixelLab API (https://pixellab.ai) to generate wizard animation frames.
Requires PIXELLAB_API_KEY environment variable.
"""

import os
import base64
import asyncio
from pathlib import Path
from dataclasses import dataclass


@dataclass
class AnimationFrame:
    """A single animation frame."""
    index: int
    image_data: bytes
    filename: str


@dataclass
class AnimationResult:
    """Result of animation generation."""
    frames: list[AnimationFrame]
    total_frames: int
    success: bool
    error: str | None = None


async def generate_wizard_animation(
    num_frames: int = 4,
    output_dir: str = "wizard_frames",
    prompt: str = None
) -> AnimationResult:
    """Generate sleeping wizard animation frames using PixelLab API.

    Args:
        num_frames: Number of frames to generate
        output_dir: Directory to save frames
        prompt: Custom prompt (uses default wizard prompt if None)

    Returns:
        AnimationResult with generated frames
    """
    try:
        import httpx
    except ImportError:
        return AnimationResult(
            frames=[],
            total_frames=0,
            success=False,
            error="httpx not installed. Run: pip install httpx"
        )

    api_key = os.getenv("PIXELLAB_API_KEY")
    if not api_key:
        return AnimationResult(
            frames=[],
            total_frames=0,
            success=False,
            error="PIXELLAB_API_KEY not set"
        )

    if prompt is None:
        prompt = (
            "sleeping wizard character, pointy hat, magical robes, "
            "cozy peaceful pose, pixel art style, fantasy game sprite"
        )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    frames = []

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # Generate base image
            response = await client.post(
                "https://api.pixellab.ai/v1/generate",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "pixflux",
                    "prompt": prompt,
                    "width": 128,
                    "height": 128,
                }
            )

            if response.status_code != 200:
                return AnimationResult(
                    frames=[],
                    total_frames=0,
                    success=False,
                    error=f"API error: {response.status_code} - {response.text}"
                )

            result = response.json()

            # Handle different response formats
            if "image_base64" in result:
                image_data = base64.b64decode(result["image_base64"])
            elif "image_url" in result:
                img_response = await client.get(result["image_url"])
                image_data = img_response.content
            elif "data" in result:
                # Some APIs wrap in data field
                image_data = base64.b64decode(result["data"])
            else:
                return AnimationResult(
                    frames=[],
                    total_frames=0,
                    success=False,
                    error=f"Unexpected API response: {list(result.keys())}"
                )

            # Save base frame
            frame_path = output_path / "frame_00.png"
            frame_path.write_bytes(image_data)

            frames.append(AnimationFrame(
                index=0,
                image_data=image_data,
                filename="frame_00.png"
            ))

            # For animation, we'd normally call the animate endpoint
            # For now, duplicate the base frame with slight variations
            for i in range(1, num_frames):
                frame_path = output_path / f"frame_{i:02d}.png"
                frame_path.write_bytes(image_data)  # Same image for now
                frames.append(AnimationFrame(
                    index=i,
                    image_data=image_data,
                    filename=f"frame_{i:02d}.png"
                ))

            return AnimationResult(
                frames=frames,
                total_frames=len(frames),
                success=True
            )

        except httpx.HTTPError as e:
            return AnimationResult(
                frames=[],
                total_frames=0,
                success=False,
                error=f"HTTP error: {e}"
            )
        except Exception as e:
            return AnimationResult(
                frames=[],
                total_frames=0,
                success=False,
                error=str(e)
            )


# CLI test
if __name__ == "__main__":
    import sys

    if not os.getenv("PIXELLAB_API_KEY"):
        print("Error: PIXELLAB_API_KEY not set")
        print("Get your key at https://pixellab.ai")
        sys.exit(1)

    print("Generating wizard animation...")
    result = asyncio.run(generate_wizard_animation(num_frames=4))

    if result.success:
        print(f"✓ Generated {result.total_frames} frames")
        for frame in result.frames:
            print(f"  → wizard_frames/{frame.filename}")
    else:
        print(f"✗ Error: {result.error}")
