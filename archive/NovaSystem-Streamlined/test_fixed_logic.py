#!/usr/bin/env python3
"""
Test script to verify the fixed default model logic.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from novasystem.utils.llm_service import LLMService

async def test_fixed_logic():
    """Test the fixed default model logic."""
    print("🔧 Testing Fixed Default Model Logic")
    print("=" * 50)

    llm_service = LLMService()

    # Test 1: Check default model
    print("🧪 Test 1: Default model selection")
    try:
        default_model = llm_service.get_default_model()
        print(f"✅ Default model: {default_model}")

        # Check if it's Claude or Ollama (NOT GPT)
        if default_model.startswith("claude-"):
            print("✅ Correctly using Claude model")
        elif default_model.startswith("ollama:"):
            print("✅ Correctly using Ollama model")
        else:
            print(f"❌ ERROR: Using unexpected model type: {default_model}")

    except Exception as e:
        print(f"❌ Error getting default model: {str(e)}")

    # Test 2: Test completion with default model
    print(f"\n🧪 Test 2: Completion with default model")
    try:
        response = await llm_service.get_completion(
            messages=[{"role": "user", "content": "What is 2+2? Answer with just the number."}],
            temperature=0.1,
            max_tokens=10
        )
        print(f"✅ Completion successful: {response.strip()}")
    except Exception as e:
        print(f"❌ Completion failed: {str(e)}")

    # Test 3: Test streaming with default model
    print(f"\n🧪 Test 3: Streaming with default model")
    try:
        print("Streaming response:")
        print("-" * 20)
        async for chunk in llm_service.stream_completion(
            messages=[{"role": "user", "content": "Count 1, 2, 3"}],
            temperature=0.1
        ):
            print(chunk, end="", flush=True)
        print("\n" + "-" * 20)
        print("✅ Streaming successful!")
    except Exception as e:
        print(f"❌ Streaming failed: {str(e)}")

    # Test 4: Check available models
    print(f"\n🧪 Test 4: Available models")
    available_models = llm_service.get_available_models()
    print(f"Available models: {len(available_models)}")

    claude_models = [m for m in available_models if m.startswith("claude-")]
    ollama_models = [m for m in available_models if m.startswith("ollama:")]
    gpt_models = [m for m in available_models if m.startswith("gpt")]

    print(f"Claude models: {len(claude_models)}")
    print(f"Ollama models: {len(ollama_models)}")
    print(f"GPT models: {len(gpt_models)}")

    if gpt_models:
        print(f"❌ ERROR: GPT models should not be available: {gpt_models}")
    else:
        print("✅ No GPT models in available list (correct)")

async def main():
    """Main test function."""
    print("🚀 Fixed Logic Test")
    print("=" * 50)

    await test_fixed_logic()

    print(f"\n🎉 Fixed logic test completed!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
