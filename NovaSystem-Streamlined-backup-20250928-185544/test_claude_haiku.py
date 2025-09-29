#!/usr/bin/env python3
"""
Test script specifically for Claude 3.5 Haiku model.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from novasystem.utils.llm_service import LLMService

async def test_claude_haiku():
    """Test Claude 3.5 Haiku specifically."""
    print("Testing Claude 3.5 Haiku...")
    print("=" * 50)

    # Initialize the LLM service
    llm_service = LLMService()

    # Check if Anthropic client is initialized
    if llm_service.anthropic_client:
        print("✅ Anthropic client initialized successfully")
    else:
        print("❌ Anthropic client not initialized")
        print("Please set your ANTHROPIC_API_KEY environment variable")
        return False

    # Test Claude 3.5 Haiku specifically
    model = "claude-3-5-haiku-20241022"
    print(f"\nTesting model: {model}")

    # Get model capabilities
    capabilities = llm_service.get_model_capabilities(model)
    print(f"Model capabilities:")
    print(f"  Type: {capabilities.get('type')}")
    print(f"  Reasoning: {capabilities.get('reasoning')}")
    print(f"  Coding: {capabilities.get('coding')}")
    print(f"  Analysis: {capabilities.get('analysis')}")
    print(f"  Creativity: {capabilities.get('creativity')}")
    print(f"  Speed: {capabilities.get('speed')}")
    print(f"  Context Length: {capabilities.get('context_length'):,} tokens")
    print(f"  Description: {capabilities.get('description')}")

    # Test a simple completion
    print(f"\n🧪 Testing completion with Claude 3.5 Haiku...")
    messages = [
        {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me you're Claude 3.5 Haiku. Keep it short and friendly."}
    ]

    try:
        response = await llm_service.get_completion(
            messages=messages,
            model=model,
            temperature=0.7,
            max_tokens=100
        )
        print(f"✅ Completion successful!")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Completion failed: {str(e)}")
        return False

async def test_streaming():
    """Test streaming completion with Claude 3.5 Haiku."""
    print(f"\n🌊 Testing streaming completion...")

    llm_service = LLMService()

    if not llm_service.anthropic_client:
        print("❌ Anthropic client not available for streaming test")
        return False

    model = "claude-3-5-haiku-20241022"
    messages = [
        {"role": "user", "content": "Count from 1 to 5, one number per line. Be brief."}
    ]

    try:
        print(f"Streaming response from {model}:")
        print("-" * 30)
        async for chunk in llm_service.stream_completion(
            messages=messages,
            model=model,
            temperature=0.7
        ):
            print(chunk, end="", flush=True)
        print("\n" + "-" * 30)
        print("✅ Streaming successful!")
        return True
    except Exception as e:
        print(f"\n❌ Streaming failed: {str(e)}")
        return False

async def test_speed_comparison():
    """Test speed of Claude 3.5 Haiku."""
    print(f"\n⚡ Testing speed performance...")

    llm_service = LLMService()

    if not llm_service.anthropic_client:
        print("❌ Anthropic client not available for speed test")
        return False

    model = "claude-3-5-haiku-20241022"
    messages = [
        {"role": "user", "content": "What is 2+2? Answer in one word."}
    ]

    import time
    start_time = time.time()

    try:
        response = await llm_service.get_completion(
            messages=messages,
            model=model,
            temperature=0.1,
            max_tokens=10
        )
        end_time = time.time()
        response_time = end_time - start_time

        print(f"✅ Speed test successful!")
        print(f"Response: {response}")
        print(f"Response time: {response_time:.2f} seconds")
        print(f"Speed rating: {llm_service.get_model_capabilities(model).get('speed')}/100")
        return True
    except Exception as e:
        print(f"❌ Speed test failed: {str(e)}")
        return False

async def main():
    """Main test function."""
    print("Claude 3.5 Haiku Integration Test")
    print("=" * 50)

    # Test basic integration
    basic_test = await test_claude_haiku()

    # Test streaming
    streaming_test = await test_streaming()

    # Test speed
    speed_test = await test_speed_comparison()

    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Basic Integration: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"Streaming: {'✅ PASS' if streaming_test else '❌ FAIL'}")
    print(f"Speed Test: {'✅ PASS' if speed_test else '❌ FAIL'}")

    if basic_test and streaming_test and speed_test:
        print("\n🎉 All tests passed! Claude 3.5 Haiku is working perfectly.")
        print("Claude 3.5 Haiku is optimized for speed and efficiency!")
    else:
        print("\n⚠️  Some tests failed. Check your ANTHROPIC_API_KEY and network connection.")

    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
