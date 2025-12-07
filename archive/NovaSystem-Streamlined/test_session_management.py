#!/usr/bin/env python3
"""
Test script for NovaSystem session management.
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

async def test_session_management():
    """Test the session management system."""
    print("📝 Testing Session Management System")
    print("=" * 50)

    # Get configuration
    config = get_config()
    print(f"Configuration loaded:")
    print(f"  Default model: {config.llm.default_model}")
    print(f"  Session directory: {config.get_session_dir()}")
    print(f"  Auto-save sessions: {config.session.auto_save_sessions}")

    # Initialize LLM service with session recording
    llm_service = LLMService(enable_session_recording=True)

    # Get session manager
    session_manager = get_session_manager()

    # Create a new session
    print(f"\n🧪 Creating new session...")
    session = session_manager.create_session(
        title="Test Session",
        description="Testing the session management system",
        tags=["test", "session", "management"]
    )
    print(f"✅ Created session: {session.metadata.session_id}")

    # Test completion with session recording
    print(f"\n💬 Testing completion with session recording...")
    messages = [
        {"role": "user", "content": "Hello! Please respond with a brief greeting and tell me you're working."}
    ]

    try:
        response = await llm_service.get_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )
        print(f"✅ Completion successful!")
        print(f"Response: {response[:100]}...")

        # Check if session was recorded
        current_session = session_manager.get_current_session()
        if current_session:
            print(f"✅ Session recorded: {len(current_session.messages)} messages")
            print(f"  Model used: {current_session.metadata.model_used}")
            print(f"  Total tokens: {current_session.metadata.total_tokens}")
        else:
            print("❌ No current session found")

    except Exception as e:
        print(f"❌ Completion failed: {str(e)}")

    # Test another completion
    print(f"\n💬 Testing another completion...")
    messages2 = [
        {"role": "user", "content": "What is 5 + 3? Answer with just the number."}
    ]

    try:
        response2 = await llm_service.get_completion(
            messages=messages2,
            temperature=0.1,
            max_tokens=10
        )
        print(f"✅ Completion successful!")
        print(f"Response: {response2.strip()}")

        # Check session again
        current_session = session_manager.get_current_session()
        if current_session:
            print(f"✅ Session updated: {len(current_session.messages)} messages")
            print(f"  Total tokens: {current_session.metadata.total_tokens}")

    except Exception as e:
        print(f"❌ Completion failed: {str(e)}")

    # Save session
    print(f"\n💾 Saving session...")
    try:
        file_path = session_manager.save_session()
        print(f"✅ Session saved to: {file_path}")

        # Also save as JSON
        json_path = session_manager.save_session_json()
        print(f"✅ Session JSON saved to: {json_path}")

    except Exception as e:
        print(f"❌ Failed to save session: {str(e)}")

    # List sessions
    print(f"\n📋 Listing sessions...")
    try:
        sessions = session_manager.list_sessions(limit=5)
        print(f"✅ Found {len(sessions)} sessions:")
        for session_info in sessions:
            print(f"  - {session_info['filename']} ({session_info['created_at'].strftime('%Y-%m-%d %H:%M')})")

    except Exception as e:
        print(f"❌ Failed to list sessions: {str(e)}")

    # Test session summary
    if session:
        print(f"\n📊 Getting session summary...")
        try:
            summary = session_manager.get_session_summary(session.metadata.session_id)
            if summary:
                print(f"✅ Session summary:")
                print(f"  Title: {summary['title']}")
                print(f"  Messages: {summary['total_messages']}")
                print(f"  Tokens: {summary['total_tokens']}")
                print(f"  Model: {summary['model_used']}")
            else:
                print("❌ No summary found")

        except Exception as e:
            print(f"❌ Failed to get session summary: {str(e)}")

async def test_configuration():
    """Test configuration system."""
    print(f"\n⚙️ Testing Configuration System")
    print("=" * 50)

    config = get_config()

    # Show current configuration
    print("Current configuration:")
    config_dict = config.to_dict()

    print(f"\nSession config:")
    for key, value in config_dict["session"].items():
        print(f"  {key}: {value}")

    print(f"\nLLM config:")
    for key, value in config_dict["llm"].items():
        if key == "model_priority":
            print(f"  {key}: {value[:3]}...")  # Show first 3 models
        else:
            print(f"  {key}: {value}")

    print(f"\nSystem config:")
    for key, value in config_dict["system"].items():
        print(f"  {key}: {value}")

    # Test directory creation
    print(f"\n📁 Testing directory creation...")
    session_dir = config.get_session_dir()
    data_dir = config.get_data_dir()
    logs_dir = config.get_logs_dir()

    print(f"  Session directory: {session_dir} (exists: {session_dir.exists()})")
    print(f"  Data directory: {data_dir} (exists: {data_dir.exists()})")
    print(f"  Logs directory: {logs_dir} (exists: {logs_dir.exists()})")

async def main():
    """Main test function."""
    print("🚀 NovaSystem Session Management Test")
    print("=" * 60)

    # Test configuration
    await test_configuration()

    # Test session management
    await test_session_management()

    print(f"\n🎉 Session management test completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
