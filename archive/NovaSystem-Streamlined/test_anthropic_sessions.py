#!/usr/bin/env python3
"""
Test script for NovaSystem session management with Anthropic.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from novasystem.utils.llm_service import LLMService
from novasystem.config import get_config
from novasystem.session import get_session_manager

async def test_anthropic_sessions():
    """Test session management with Anthropic models."""
    print("🤖 Testing Anthropic Session Management")
    print("=" * 50)

    # Check if Anthropic API key is available
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if not anthropic_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        print("Please set your Anthropic API key:")
        print("export ANTHROPIC_API_KEY='your-key-here'")
        return False

    print("✅ Anthropic API key found")

    # Get configuration
    config = get_config()
    print(f"Configuration:")
    print(f"  Default model: {config.llm.default_model}")
    print(f"  Session directory: {config.get_session_dir()}")

    # Initialize LLM service with session recording
    llm_service = LLMService(enable_session_recording=True)

    # Check which model will be used
    default_model = llm_service.get_default_model()
    print(f"  Will use model: {default_model}")

    if not default_model.startswith("claude-"):
        print(f"❌ Expected Claude model, got: {default_model}")
        return False

    # Get session manager
    session_manager = get_session_manager()

    # Create a new session
    print(f"\n🧪 Creating new Anthropic session...")
    session = session_manager.create_session(
        title="Anthropic Test Session",
        description="Testing session management with Claude models",
        tags=["anthropic", "claude", "test", "session"]
    )
    print(f"✅ Created session: {session.metadata.session_id}")

    # Test 1: Basic completion
    print(f"\n💬 Test 1: Basic completion with Claude")
    messages = [
        {"role": "user", "content": "Hello! Please respond with a brief greeting and identify yourself as a Claude model."}
    ]

    try:
        response = await llm_service.get_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        print(f"✅ Completion successful!")
        print(f"Response: {response}")

        # Check session recording
        current_session = session_manager.get_current_session()
        if current_session:
            print(f"✅ Session recorded: {len(current_session.messages)} messages")
            print(f"  Model used: {current_session.metadata.model_used}")
            print(f"  Total tokens: {current_session.metadata.total_tokens}")

    except Exception as e:
        print(f"❌ Completion failed: {str(e)}")
        return False

    # Test 2: Streaming completion
    print(f"\n🌊 Test 2: Streaming completion with Claude")
    messages2 = [
        {"role": "user", "content": "Count from 1 to 5, one number per line."}
    ]

    try:
        print("Streaming response:")
        print("-" * 20)
        async for chunk in llm_service.stream_completion(
            messages=messages2,
            temperature=0.1
        ):
            print(chunk, end="", flush=True)
        print("\n" + "-" * 20)
        print("✅ Streaming successful!")

    except Exception as e:
        print(f"❌ Streaming failed: {str(e)}")
        return False

    # Test 3: Different Claude model
    print(f"\n🔄 Test 3: Using different Claude model")
    try:
        response3 = await llm_service.get_completion(
            messages=[{"role": "user", "content": "What is 7 * 8? Answer with just the number."}],
            model="claude-3-5-haiku-20241022",  # Use Haiku for speed
            temperature=0.1,
            max_tokens=10
        )
        print(f"✅ Haiku completion successful!")
        print(f"Response: {response3.strip()}")

    except Exception as e:
        print(f"❌ Haiku completion failed: {str(e)}")
        return False

    # Test 4: System message
    print(f"\n⚙️ Test 4: System message with Claude")
    try:
        system_messages = [
            {"role": "system", "content": "You are a helpful math tutor. Always show your work step by step."},
            {"role": "user", "content": "How do I solve 3x + 7 = 22?"}
        ]

        response4 = await llm_service.get_completion(
            messages=system_messages,
            temperature=0.3,
            max_tokens=200
        )
        print(f"✅ System message completion successful!")
        print(f"Response: {response4[:100]}...")

    except Exception as e:
        print(f"❌ System message completion failed: {str(e)}")
        return False

    # Save session
    print(f"\n💾 Saving session...")
    try:
        file_path = session_manager.save_session()
        print(f"✅ Session saved to: {file_path}")

        # Show session content
        print(f"\n📄 Session content preview:")
        with open(file_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines[:15]):  # Show first 15 lines
                print(f"  {line}")
            if len(lines) > 15:
                print(f"  ... ({len(lines) - 15} more lines)")

    except Exception as e:
        print(f"❌ Failed to save session: {str(e)}")
        return False

    # Final session stats
    current_session = session_manager.get_current_session()
    if current_session:
        print(f"\n📊 Final session statistics:")
        print(f"  Session ID: {current_session.metadata.session_id}")
        print(f"  Title: {current_session.metadata.title}")
        print(f"  Total messages: {current_session.metadata.total_messages}")
        print(f"  Total tokens: {current_session.metadata.total_tokens}")
        print(f"  Model used: {current_session.metadata.model_used}")
        print(f"  Tags: {', '.join(current_session.metadata.tags)}")

    return True

async def test_model_availability():
    """Test which Anthropic models are available."""
    print(f"\n🔍 Testing Anthropic Model Availability")
    print("=" * 50)

    llm_service = LLMService()
    available_models = llm_service.get_available_models()

    claude_models = [model for model in available_models if model.startswith("claude-")]

    print(f"Available Claude models: {len(claude_models)}")
    for model in claude_models:
        caps = llm_service.get_model_capabilities(model)
        print(f"  ✅ {model}")
        print(f"     Reasoning: {caps.get('reasoning')}/100")
        print(f"     Speed: {caps.get('speed')}/100")
        print(f"     Context: {caps.get('context_length'):,} tokens")

    return len(claude_models) > 0

async def main():
    """Main test function."""
    print("🚀 Anthropic Session Management Test")
    print("=" * 60)

    # Test model availability
    models_available = await test_model_availability()

    if not models_available:
        print("❌ No Claude models available. Check your API key.")
        return

    # Test session management with Anthropic
    success = await test_anthropic_sessions()

    print(f"\n" + "=" * 60)
    if success:
        print("🎉 Anthropic session management test completed successfully!")
        print("✅ All Claude models working with session recording")
    else:
        print("❌ Anthropic session management test failed")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
