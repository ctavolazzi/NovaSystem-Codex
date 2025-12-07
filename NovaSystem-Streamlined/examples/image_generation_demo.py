#!/usr/bin/env python3
"""
Image Generation Demo for NovaSystem.

Demonstrates Gemini's native image generation capabilities:
1. Text-to-image generation
2. Image editing
3. Style transfer
4. Multi-turn conversational editing

Requires: pip install google-genai Pillow

Models:
- gemini-2.5-flash-image: Fast, up to 1024px
- gemini-3-pro-image-preview: Advanced, up to 4K, thinking mode
"""

import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.utils.image_service import (
    ImageService,
    ConversationalImageEditor,
    ImageModel,
    AspectRatio,
    ImageSize,
    generate_image,
    edit_image
)


async def demo_text_to_image():
    """Demo: Generate an image from text."""
    print("\n" + "="*60)
    print("📸 Demo 1: Text-to-Image Generation")
    print("="*60)

    service = ImageService()

    prompt = """A photorealistic close-up portrait of an elderly Japanese
    ceramicist with deep, sun-etched wrinkles and a warm, knowing smile.
    He is carefully inspecting a freshly glazed tea bowl. Soft, golden
    hour light streaming through a window."""

    print(f"\n📝 Prompt: {prompt[:80]}...")

    result = await service.generate(
        prompt=prompt,
        model=ImageModel.FLASH,
        aspect_ratio=AspectRatio.PORTRAIT_3_4
    )

    output_path = Path("generated_ceramicist.png")
    result.save(output_path)

    print(f"\n✅ Generated: {output_path.absolute()}")
    if result.text_response:
        print(f"📝 Model says: {result.text_response[:100]}...")

    return output_path


async def demo_product_mockup():
    """Demo: Generate a product mockup."""
    print("\n" + "="*60)
    print("🛍️ Demo 2: Product Mockup")
    print("="*60)

    prompt = """A high-resolution, studio-lit product photograph of a
    minimalist ceramic coffee mug in matte black, presented on a polished
    concrete surface. Three-point softbox lighting creates soft, diffused
    highlights. Ultra-realistic with sharp focus on steam rising from the
    coffee. Square format."""

    print(f"\n📝 Prompt: {prompt[:80]}...")

    result = await generate_image(
        prompt=prompt,
        output_path="product_mockup.png",
        model="flash",
        aspect_ratio="1:1"
    )

    print(f"\n✅ Generated: product_mockup.png")
    return Path("product_mockup.png")


async def demo_logo_creation():
    """Demo: Create a logo with text."""
    print("\n" + "="*60)
    print("🎨 Demo 3: Logo with Text (Pro Model)")
    print("="*60)

    service = ImageService()

    prompt = """Create a modern, minimalist logo for a coffee shop called
    'The Daily Grind'. The text should be in a clean, bold, sans-serif
    font. The color scheme is black and white. Put the logo in a circle.
    Use a coffee bean in a clever way."""

    print(f"\n📝 Prompt: {prompt[:80]}...")

    result = await service.generate(
        prompt=prompt,
        model=ImageModel.PRO,  # Pro model for better text rendering
        aspect_ratio=AspectRatio.SQUARE,
        size=ImageSize.TWO_K
    )

    output_path = Path("coffee_logo.png")
    result.save(output_path)

    print(f"\n✅ Generated: {output_path.absolute()}")
    return output_path


async def demo_conversational_editing():
    """Demo: Multi-turn image editing conversation."""
    print("\n" + "="*60)
    print("💬 Demo 4: Conversational Image Editing")
    print("="*60)

    editor = ConversationalImageEditor(model=ImageModel.PRO)

    # Turn 1: Initial generation
    print("\n🎯 Turn 1: Create initial image...")
    result = await editor.send(
        "Create a beautiful mountain landscape with a lake at sunset"
    )
    result.save("conversation_turn1.png")
    print("✅ Saved: conversation_turn1.png")

    # Turn 2: Add element
    print("\n🎯 Turn 2: Adding a cabin...")
    result = await editor.send(
        "Add a cozy wooden cabin on the shore of the lake"
    )
    result.save("conversation_turn2.png")
    print("✅ Saved: conversation_turn2.png")

    # Turn 3: Modify style
    print("\n🎯 Turn 3: Adding atmosphere...")
    result = await editor.send(
        "Add some mist rising from the lake and warm light in the cabin windows"
    )
    result.save("conversation_turn3.png")
    print("✅ Saved: conversation_turn3.png")

    return Path("conversation_turn3.png")


async def demo_sticker_creation():
    """Demo: Create a kawaii sticker."""
    print("\n" + "="*60)
    print("🐼 Demo 5: Sticker Design")
    print("="*60)

    prompt = """A kawaii-style sticker of a happy red panda wearing a tiny
    bamboo hat. It's munching on a green bamboo leaf. The design features
    bold, clean outlines, simple cel-shading, and a vibrant color palette.
    The background must be white."""

    print(f"\n📝 Prompt: {prompt[:80]}...")

    result = await generate_image(
        prompt=prompt,
        output_path="panda_sticker.png",
        model="flash",
        aspect_ratio="1:1"
    )

    print(f"\n✅ Generated: panda_sticker.png")
    return Path("panda_sticker.png")


async def demo_all():
    """Run all demos sequentially."""
    print("\n" + "="*60)
    print("🚀 NovaSystem Image Generation Demo")
    print("    Using Gemini Native Image Models")
    print("="*60)

    demos = [
        ("Text-to-Image", demo_text_to_image),
        ("Product Mockup", demo_product_mockup),
        ("Logo Creation", demo_logo_creation),
        ("Sticker Design", demo_sticker_creation),
        # Conversational editing takes longer
        # ("Conversational Editing", demo_conversational_editing),
    ]

    results = []
    for name, demo_func in demos:
        try:
            result = await demo_func()
            results.append((name, result, "✅"))
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")
            results.append((name, None, "❌"))

    # Summary
    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    for name, path, status in results:
        if path:
            print(f"  {status} {name}: {path}")
        else:
            print(f"  {status} {name}: Failed")


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Image Generation Demo")
    parser.add_argument(
        "--demo",
        choices=["all", "text2img", "product", "logo", "chat", "sticker"],
        default="all",
        help="Which demo to run"
    )
    args = parser.parse_args()

    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("   Get your key at: https://aistudio.google.com/apikey")
        return

    demo_map = {
        "all": demo_all,
        "text2img": demo_text_to_image,
        "product": demo_product_mockup,
        "logo": demo_logo_creation,
        "chat": demo_conversational_editing,
        "sticker": demo_sticker_creation,
    }

    await demo_map[args.demo]()

    print("\n✨ Demo complete!")


if __name__ == "__main__":
    asyncio.run(main())
