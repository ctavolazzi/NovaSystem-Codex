#!/usr/bin/env python3
"""
Vision Demo for NovaSystem.

Demonstrates Gemini's image understanding capabilities:
1. Image captioning
2. Visual question answering
3. Object detection with bounding boxes
4. Segmentation masks
5. Multi-image comparison

Requires: pip install google-genai Pillow numpy

Usage:
    python vision_demo.py --image path/to/image.jpg
    python vision_demo.py --demo caption --image photo.jpg
    python vision_demo.py --demo detect --image scene.jpg
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.utils.vision_service import (
    VisionService,
    caption_image,
    ask_about_image,
    detect_in_image
)


async def demo_caption(image_path: str):
    """Demo: Caption an image in different styles."""
    print("\n" + "="*60)
    print("📝 Demo: Image Captioning")
    print("="*60)

    service = VisionService()

    styles = ["descriptive", "brief", "technical", "creative"]
    for style in styles:
        print(f"\n🎯 Style: {style}")
        result = await service.caption(image_path, style)
        print(f"   {result.text[:200]}..." if len(result.text) > 200 else f"   {result.text}")


async def demo_question(image_path: str, question: str = None):
    """Demo: Ask questions about an image."""
    print("\n" + "="*60)
    print("❓ Demo: Visual Question Answering")
    print("="*60)

    service = VisionService()

    questions = [
        question or "What is the main subject of this image?",
        "What colors are prominent in this image?",
        "What is the mood or atmosphere of this image?",
    ]

    for q in questions:
        print(f"\n❓ {q}")
        result = await service.ask(q, image_path)
        answer = result.text[:300] + "..." if len(result.text) > 300 else result.text
        print(f"💬 {answer}")


async def demo_detection(image_path: str, target: str = None):
    """Demo: Object detection with bounding boxes."""
    print("\n" + "="*60)
    print("🔍 Demo: Object Detection")
    print("="*60)

    service = VisionService()

    print(f"\n📸 Analyzing: {image_path}")
    if target:
        print(f"🎯 Target: {target}")

    result = await service.detect_objects(image_path, target)

    if result.objects:
        print(f"\n✅ Found {len(result.objects)} objects:")
        for i, obj in enumerate(result.objects, 1):
            print(f"   {i}. {obj.label}")
            print(f"      Box: ({obj.x1}, {obj.y1}) -> ({obj.x2}, {obj.y2})")
            print(f"      Size: {obj.width}x{obj.height}px")

        # Draw boxes on image
        output_path = Path(image_path).stem + "_detected.png"
        service.draw_boxes(image_path, result.objects, output_path)
        print(f"\n💾 Saved annotated image: {output_path}")
    else:
        print("\n⚠️ No objects detected")
        print(f"Raw response: {result.text[:200]}...")


async def demo_segmentation(image_path: str, target: str = "prominent objects"):
    """Demo: Segmentation masks."""
    print("\n" + "="*60)
    print("✂️ Demo: Image Segmentation")
    print("="*60)

    service = VisionService()

    print(f"\n📸 Analyzing: {image_path}")
    print(f"🎯 Target: {target}")

    result = await service.segment(image_path, target)

    if result.segments:
        print(f"\n✅ Found {len(result.segments)} segments:")
        for i, seg in enumerate(result.segments, 1):
            print(f"   {i}. {seg.label}")
            print(f"      Box: ({seg.box.x1}, {seg.box.y1}) -> ({seg.box.x2}, {seg.box.y2})")

            # Save individual mask overlay
            try:
                from PIL import Image
                original = Image.open(image_path)
                overlay = seg.to_overlay(original)
                output_path = f"segment_{i}_{seg.label.replace(' ', '_')}.png"
                overlay.save(output_path)
                print(f"      Saved: {output_path}")
            except Exception as e:
                print(f"      ⚠️ Could not save overlay: {e}")
    else:
        print("\n⚠️ No segments found")
        print(f"Raw response: {result.text[:200]}...")


async def demo_comparison(image_paths: list):
    """Demo: Compare multiple images."""
    print("\n" + "="*60)
    print("🔄 Demo: Image Comparison")
    print("="*60)

    if len(image_paths) < 2:
        print("⚠️ Need at least 2 images for comparison")
        return

    service = VisionService()

    print(f"\n📸 Comparing {len(image_paths)} images:")
    for i, path in enumerate(image_paths, 1):
        print(f"   {i}. {path}")

    result = await service.compare(image_paths)
    print(f"\n📊 Comparison:\n{result.text}")


async def demo_comprehensive(image_path: str):
    """Demo: Comprehensive image analysis."""
    print("\n" + "="*60)
    print("🔬 Demo: Comprehensive Analysis")
    print("="*60)

    service = VisionService()

    print(f"\n📸 Analyzing: {image_path}")

    result = await service.analyze(
        image_path,
        aspects=["composition", "colors", "mood", "style", "technical quality"]
    )

    print(f"\n📊 Analysis:\n{result.text}")


async def run_all_demos(image_path: str):
    """Run all demos on a single image."""
    print("\n" + "="*60)
    print("🚀 NovaSystem Vision Demo")
    print("    Using Gemini Multimodal Models")
    print("="*60)

    demos = [
        ("Captioning", lambda: demo_caption(image_path)),
        ("Q&A", lambda: demo_question(image_path)),
        ("Detection", lambda: demo_detection(image_path)),
        ("Analysis", lambda: demo_comprehensive(image_path)),
    ]

    for name, demo_func in demos:
        try:
            await demo_func()
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")

    print("\n" + "="*60)
    print("✨ Demo complete!")
    print("="*60)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Vision Demo for NovaSystem")
    parser.add_argument(
        "--image",
        type=str,
        help="Path to image file",
    )
    parser.add_argument(
        "--images",
        type=str,
        nargs="+",
        help="Multiple image paths (for comparison)",
    )
    parser.add_argument(
        "--demo",
        choices=["all", "caption", "ask", "detect", "segment", "compare", "analyze"],
        default="all",
        help="Which demo to run"
    )
    parser.add_argument(
        "--question",
        type=str,
        help="Question to ask about the image"
    )
    parser.add_argument(
        "--target",
        type=str,
        help="Target for detection/segmentation"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="URL of image to analyze"
    )

    args = parser.parse_args()

    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("   Get your key at: https://aistudio.google.com/apikey")
        return

    # Get image path
    image_path = args.image
    if args.url:
        # Download image from URL
        import requests
        print(f"📥 Downloading image from {args.url}...")
        response = requests.get(args.url)
        image_path = "downloaded_image.jpg"
        with open(image_path, "wb") as f:
            f.write(response.content)
        print(f"   Saved to: {image_path}")

    if not image_path and args.demo != "compare":
        # Create a simple test image if none provided
        try:
            from PIL import Image, ImageDraw

            print("📸 No image provided, creating a test image...")
            img = Image.new('RGB', (400, 300), color=(135, 206, 235))
            draw = ImageDraw.Draw(img)

            # Draw sun
            draw.ellipse([300, 30, 370, 100], fill=(255, 255, 0))

            # Draw grass
            draw.rectangle([0, 250, 400, 300], fill=(34, 139, 34))

            # Draw house
            draw.rectangle([100, 150, 200, 250], fill=(139, 69, 19))
            draw.polygon([(100, 150), (150, 100), (200, 150)], fill=(128, 0, 0))

            # Draw tree
            draw.rectangle([280, 180, 300, 250], fill=(101, 67, 33))
            draw.ellipse([250, 120, 330, 200], fill=(0, 100, 0))

            image_path = "test_scene.png"
            img.save(image_path)
            print(f"   Created: {image_path}")

        except ImportError:
            print("❌ PIL not available and no image provided")
            return

    # Run appropriate demo
    if args.demo == "all":
        await run_all_demos(image_path)
    elif args.demo == "caption":
        await demo_caption(image_path)
    elif args.demo == "ask":
        await demo_question(image_path, args.question)
    elif args.demo == "detect":
        await demo_detection(image_path, args.target)
    elif args.demo == "segment":
        await demo_segmentation(image_path, args.target or "prominent objects")
    elif args.demo == "compare":
        if args.images:
            await demo_comparison(args.images)
        else:
            print("⚠️ --images required for comparison demo")
    elif args.demo == "analyze":
        await demo_comprehensive(image_path)


if __name__ == "__main__":
    asyncio.run(main())
