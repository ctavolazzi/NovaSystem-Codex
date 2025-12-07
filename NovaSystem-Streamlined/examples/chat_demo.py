#!/usr/bin/env python3
"""
Native Gemini Chat Demo for NovaSystem.

Demonstrates multi-turn conversations using the native Gemini SDK:
1. Basic chat with history
2. Streaming chat responses
3. System instructions
4. Multiple chat sessions
5. Thinking configuration

Usage:
    python chat_demo.py
    python chat_demo.py --demo streaming
    python chat_demo.py --demo multi
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.utils.chat_service import (
    ChatSession,
    ChatService,
    ChatConfig,
    create_chat,
    quick_chat
)


def demo_basic_chat():
    """Demo: Basic multi-turn chat."""
    print("\n" + "="*60)
    print("💬 Demo: Basic Multi-Turn Chat")
    print("="*60)

    # Create a chat session
    session = create_chat(
        system_instruction="You are a friendly math tutor. Keep answers concise."
    )

    # Have a conversation
    conversations = [
        "I have 3 apples and 2 oranges. How many fruits do I have?",
        "If I eat one apple, how many fruits do I have now?",
        "What if I buy 4 more oranges?"
    ]

    for message in conversations:
        print(f"\n👤 User: {message}")
        response = session.send(message)
        print(f"🤖 Model: {response}")

    # Show history
    print("\n📜 Conversation History:")
    for msg in session.get_history():
        role_emoji = "👤" if msg["role"] == "user" else "🤖"
        print(f"  {role_emoji} {msg['role']}: {msg['content'][:80]}...")


def demo_streaming_chat():
    """Demo: Streaming chat responses."""
    print("\n" + "="*60)
    print("⚡ Demo: Streaming Chat")
    print("="*60)

    session = create_chat(
        system_instruction="You are a storyteller. Be creative and engaging."
    )

    prompts = [
        "Start a short story about a robot learning to paint.",
        "Continue the story - what does the robot paint first?",
    ]

    for prompt in prompts:
        print(f"\n👤 User: {prompt}")
        print("🤖 Model: ", end="", flush=True)

        for chunk in session.send_stream_sync(prompt):
            print(chunk, end="", flush=True)

        print()  # Newline after streaming


def demo_thinking_control():
    """Demo: Controlling thinking behavior."""
    print("\n" + "="*60)
    print("🧠 Demo: Thinking Configuration")
    print("="*60)

    # With thinking enabled (default)
    print("\n📝 With Thinking Enabled (default):")
    config_thinking = ChatConfig(
        model="gemini-2.5-flash",
        enable_thinking=True
    )
    session_thinking = ChatSession(config=config_thinking)
    response = session_thinking.send("What is 15% of 847?")
    print(f"   Response: {response}")

    # With thinking disabled
    print("\n📝 With Thinking Disabled:")
    config_no_thinking = ChatConfig(
        model="gemini-2.5-flash",
        enable_thinking=False
    )
    session_no_thinking = ChatSession(config=config_no_thinking)
    response = session_no_thinking.send("What is 15% of 847?")
    print(f"   Response: {response}")


def demo_multi_session():
    """Demo: Multiple chat sessions."""
    print("\n" + "="*60)
    print("📱 Demo: Multiple Chat Sessions")
    print("="*60)

    service = ChatService()

    # Create sessions for different users
    alice = service.create_session(
        session_id="alice",
        system_instruction="You are helping Alice plan a birthday party."
    )

    bob = service.create_session(
        session_id="bob",
        system_instruction="You are helping Bob debug Python code."
    )

    # Alice's conversation
    print("\n👩 Alice's Session:")
    print(f"   Alice: I'm planning a party for 10 people.")
    response = alice.send("I'm planning a party for 10 people.")
    print(f"   Model: {response[:150]}...")

    # Bob's conversation
    print("\n👨 Bob's Session:")
    print(f"   Bob: My list.sort() returns None, why?")
    response = bob.send("My list.sort() returns None, why?")
    print(f"   Model: {response[:150]}...")

    # Continue Alice's conversation
    print("\n👩 Alice (continued):")
    print(f"   Alice: What about decorations?")
    response = alice.send("What about decorations?")
    print(f"   Model: {response[:150]}...")

    # List sessions
    print(f"\n📋 Active sessions: {service.list_sessions()}")


def demo_quick_chat():
    """Demo: Quick one-off chat."""
    print("\n" + "="*60)
    print("⚡ Demo: Quick Chat")
    print("="*60)

    response = quick_chat(
        "What's the capital of France?",
        system_instruction="Answer in exactly one word."
    )
    print(f"\n❓ Question: What's the capital of France?")
    print(f"✅ Answer: {response}")


def demo_code_assistant():
    """Demo: Code assistant chat."""
    print("\n" + "="*60)
    print("💻 Demo: Code Assistant")
    print("="*60)

    session = create_chat(
        system_instruction="""You are an expert Python developer.
        Provide concise, working code examples.
        Use proper formatting and explain key concepts briefly.""",
        model="gemini-2.5-flash"
    )

    # Coding conversation
    prompts = [
        "How do I read a JSON file in Python?",
        "What if the file doesn't exist? Add error handling.",
        "Now wrap it in a function with type hints."
    ]

    for prompt in prompts:
        print(f"\n👤 Developer: {prompt}")
        print("🤖 Assistant: ", end="", flush=True)

        for chunk in session.send_stream_sync(prompt):
            print(chunk, end="", flush=True)

        print()


async def run_all_demos():
    """Run all demos."""
    print("\n" + "="*60)
    print("🚀 Native Gemini Chat Demo")
    print("="*60)

    demos = [
        ("Basic Chat", demo_basic_chat),
        ("Quick Chat", demo_quick_chat),
        ("Streaming", demo_streaming_chat),
    ]

    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")

    print("\n" + "="*60)
    print("✨ Demo complete!")
    print("="*60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Chat Demo")
    parser.add_argument(
        "--demo",
        choices=["all", "basic", "streaming", "thinking", "multi", "quick", "code"],
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
        "all": lambda: asyncio.run(run_all_demos()),
        "basic": demo_basic_chat,
        "streaming": demo_streaming_chat,
        "thinking": demo_thinking_control,
        "multi": demo_multi_session,
        "quick": demo_quick_chat,
        "code": demo_code_assistant,
    }

    demo_map[args.demo]()


if __name__ == "__main__":
    main()
