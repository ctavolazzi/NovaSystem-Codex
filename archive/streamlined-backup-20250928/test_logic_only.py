#!/usr/bin/env python3
"""
Test script to verify the default model logic without API calls.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from novasystem.utils.llm_service import LLMService

def test_logic_only():
    """Test the default model logic without making API calls."""
    print("🔧 Testing Default Model Logic (No API Calls)")
    print("=" * 50)

    # Test with different client configurations
    test_cases = [
        {
            "name": "Anthropic client available",
            "anthropic_key": "test-key",
            "openai_key": None,
            "expected": "claude-3-5-sonnet-20241022"
        },
        {
            "name": "No Anthropic, Ollama available",
            "anthropic_key": None,
            "openai_key": None,
            "expected": "ollama model"
        },
        {
            "name": "No Anthropic, no Ollama",
            "anthropic_key": None,
            "openai_key": None,
            "expected": "ValueError"
        }
    ]

    for test_case in test_cases:
        print(f"\n🧪 {test_case['name']}:")

        # Create LLMService with test configuration
        llm_service = LLMService(
            openai_api_key=test_case["openai_key"],
            anthropic_api_key=test_case["anthropic_key"]
        )

        try:
            default_model = llm_service.get_default_model()
            print(f"✅ Default model: {default_model}")

            if test_case["expected"] == "claude-3-5-sonnet-20241022":
                if default_model == "claude-3-5-sonnet-20241022":
                    print("✅ Correctly using Claude 3.5 Sonnet")
                else:
                    print(f"❌ Expected Claude 3.5 Sonnet, got: {default_model}")
            elif test_case["expected"] == "ollama model":
                if default_model.startswith("ollama:"):
                    print("✅ Correctly using Ollama model")
                else:
                    print(f"❌ Expected Ollama model, got: {default_model}")

        except ValueError as e:
            if test_case["expected"] == "ValueError":
                print(f"✅ Correctly raised ValueError: {str(e)}")
            else:
                print(f"❌ Unexpected ValueError: {str(e)}")
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")

    # Test available models
    print(f"\n🧪 Available models test:")
    llm_service = LLMService(anthropic_api_key="test-key")
    available_models = llm_service.get_available_models()

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

def main():
    """Main test function."""
    print("🚀 Logic-Only Test")
    print("=" * 50)

    test_logic_only()

    print(f"\n🎉 Logic-only test completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
