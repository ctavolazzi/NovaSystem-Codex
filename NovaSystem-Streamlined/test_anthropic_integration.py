#!/usr/bin/env python3
"""
Test script for Anthropic API integration in NovaSystem.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from novasystem.utils.llm_service import LLMService

async def test_anthropic_integration():
    """Test the Anthropic API integration."""
    print("Testing Anthropic API integration...")

    # Initialize the LLM service
    llm_service = LLMService()

    # Check if Anthropic client is initialized
    if llm_service.anthropic_client:
        print("✅ Anthropic client initialized successfully")
    else:
        print("❌ Anthropic client not initialized (check ANTHROPIC_API_KEY)")
        return False

    # Test available models
    available_models = llm_service.get_available_models()
    anthropic_models = [model for model in available_models if model.startswith("claude-")]

    print(f"Available Anthropic models: {anthropic_models}")

    if not anthropic_models:
        print("❌ No Anthropic models found in available models")
        return False

    # Test model capabilities
    test_model = anthropic_models[0]
    capabilities = llm_service.get_model_capabilities(test_model)
    print(f"Model capabilities for {test_model}:")
    print(f"  Type: {capabilities.get('type')}")
    print(f"  Reasoning: {capabilities.get('reasoning')}")
    print(f"  Coding: {capabilities.get('coding')}")
    print(f"  Context Length: {capabilities.get('context_length'):,}")

    # Test a simple completion
    print(f"\nTesting completion with {test_model}...")
    messages = [
        {"role": "user", "content": "Hello! Please respond with a simple greeting and confirm you're working."}
    ]

    try:
        response = await llm_service.get_completion(
            messages=messages,
            model=test_model,
            temperature=0.7,
            max_tokens=100
        )
        print(f"✅ Completion successful!")
        print(f"Response: {response[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Completion failed: {str(e)}")
        return False

async def test_streaming():
    """Test streaming completion."""
    print("\nTesting streaming completion...")

    llm_service = LLMService()

    if not llm_service.anthropic_client:
        print("❌ Anthropic client not available for streaming test")
        return False

    available_models = llm_service.get_available_models()
    anthropic_models = [model for model in available_models if model.startswith("claude-")]

    if not anthropic_models:
        print("❌ No Anthropic models available for streaming test")
        return False

    test_model = anthropic_models[0]
    messages = [
        {"role": "user", "content": "Count from 1 to 5, one number per line."}
    ]

    try:
        print(f"Streaming response from {test_model}:")
        async for chunk in llm_service.stream_completion(
            messages=messages,
            model=test_model,
            temperature=0.7
        ):
            print(chunk, end="", flush=True)
        print("\n✅ Streaming successful!")
        return True
    except Exception as e:
        print(f"\n❌ Streaming failed: {str(e)}")
        return False

async def main():
    """Main test function."""
    print("=" * 50)
    print("NovaSystem Anthropic Integration Test")
    print("=" * 50)

    # Test basic integration
    basic_test = await test_anthropic_integration()

    # Test streaming
    streaming_test = await test_streaming()

    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Basic Integration: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"Streaming: {'✅ PASS' if streaming_test else '❌ FAIL'}")

    if basic_test and streaming_test:
        print("\n🎉 All tests passed! Anthropic integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check your ANTHROPIC_API_KEY and network connection.")

    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
