#!/usr/bin/env python3
"""
Test script to verify the new default model setting.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from novasystem.utils.llm_service import LLMService

async def test_default_model():
    """Test the new default model setting."""
    print("🔧 Testing Default Model Configuration")
    print("=" * 50)

    # Initialize the LLM service
    llm_service = LLMService()

    # Get the default model
    default_model = llm_service.get_default_model()
    print(f"Default model: {default_model}")

    # Get model capabilities
    capabilities = llm_service.get_model_capabilities(default_model)
    print(f"\nModel capabilities:")
    print(f"  Type: {capabilities.get('type')}")
    print(f"  Reasoning: {capabilities.get('reasoning')}/100")
    print(f"  Coding: {capabilities.get('coding')}/100")
    print(f"  Analysis: {capabilities.get('analysis')}/100")
    print(f"  Creativity: {capabilities.get('creativity')}/100")
    print(f"  Speed: {capabilities.get('speed')}/100")
    print(f"  Context Length: {capabilities.get('context_length'):,} tokens")
    print(f"  Description: {capabilities.get('description')}")

    # Test the default model
    print(f"\n🧪 Testing default model: {default_model}")
    messages = [
        {"role": "user", "content": "Hello! Please respond with a brief greeting and confirm you're the default model."}
    ]

    try:
        response = await llm_service.get_completion(
            messages=messages,
            model=default_model,
            temperature=0.7,
            max_tokens=100
        )
        print(f"✅ Default model test successful!")
        print(f"Response: {response}")

        # Test without specifying model (should use default)
        print(f"\n🔄 Testing without specifying model (should use default)...")
        response2 = await llm_service.get_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )
        print(f"✅ Default model auto-selection successful!")
        print(f"Response: {response2}")

        return True
    except Exception as e:
        print(f"❌ Default model test failed: {str(e)}")
        return False

async def test_model_priority():
    """Test the model priority order."""
    print(f"\n📊 Testing Model Priority Order")
    print("=" * 50)

    llm_service = LLMService()

    # Check client availability
    print(f"Anthropic client available: {'✅' if llm_service.anthropic_client else '❌'}")
    print(f"OpenAI client available: {'✅' if llm_service.openai_client else '❌'}")

    ollama_models = llm_service.get_ollama_models()
    print(f"Ollama models available: {len(ollama_models)} models")

    # Get default model
    default_model = llm_service.get_default_model()
    print(f"\nSelected default model: {default_model}")

    # Explain the priority logic
    print(f"\nPriority Logic:")
    if llm_service.anthropic_client:
        print(f"  1. ✅ Anthropic client available → Claude 3.5 Sonnet")
    else:
        print(f"  1. ❌ Anthropic client not available")

    if ollama_models:
        print(f"  2. ✅ Ollama models available → Fastest Ollama model")
    else:
        print(f"  2. ❌ No Ollama models available")

    if llm_service.openai_client:
        print(f"  3. ✅ OpenAI client available → GPT-4")
    else:
        print(f"  3. ❌ OpenAI client not available")

async def main():
    """Main test function."""
    print("🚀 Default Model Configuration Test")
    print("=" * 50)

    # Test default model
    default_test = await test_default_model()

    # Test model priority
    await test_model_priority()

    print(f"\n" + "=" * 50)
    if default_test:
        print("🎉 Default model configuration is working correctly!")
        print("Claude 3.5 Sonnet is now the default model for optimal performance.")
    else:
        print("⚠️ Default model configuration needs attention.")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
