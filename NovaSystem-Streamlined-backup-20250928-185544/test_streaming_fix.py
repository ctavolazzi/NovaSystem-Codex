#!/usr/bin/env python3
"""
Test script to verify streaming works with default model.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from novasystem.utils.llm_service import LLMService

async def test_streaming_fix():
    """Test that streaming works with default model."""
    print("🌊 Testing Streaming Fix")
    print("=" * 50)

    llm_service = LLMService()

    # Test 1: Streaming with default model (no model specified)
    print("🧪 Test 1: Streaming with default model (no model specified)")
    messages = [{"role": "user", "content": "Count from 1 to 5, one number per line."}]

    try:
        print("Streaming response:")
        print("-" * 30)
        async for chunk in llm_service.stream_completion(
            messages=messages,
            temperature=0.7
        ):
            print(chunk, end="", flush=True)
        print("\n" + "-" * 30)
        print("✅ Streaming with default model successful!")
    except Exception as e:
        print(f"❌ Streaming failed: {str(e)}")

    # Test 2: Streaming with explicit Claude model
    print(f"\n🧪 Test 2: Streaming with explicit Claude model")
    try:
        print("Streaming response:")
        print("-" * 30)
        async for chunk in llm_service.stream_completion(
            messages=messages,
            model="claude-3-5-sonnet-20241022",
            temperature=0.7
        ):
            print(chunk, end="", flush=True)
        print("\n" + "-" * 30)
        print("✅ Streaming with explicit model successful!")
    except Exception as e:
        print(f"❌ Streaming failed: {str(e)}")

    # Test 3: Regular completion with default model
    print(f"\n🧪 Test 3: Regular completion with default model")
    try:
        response = await llm_service.get_completion(
            messages=[{"role": "user", "content": "What is 3 + 4? Answer with just the number."}],
            temperature=0.1,
            max_tokens=10
        )
        print(f"✅ Regular completion successful: {response.strip()}")
    except Exception as e:
        print(f"❌ Regular completion failed: {str(e)}")

async def main():
    """Main test function."""
    print("🚀 Streaming Fix Test")
    print("=" * 50)

    await test_streaming_fix()

    print(f"\n🎉 Streaming fix test completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
