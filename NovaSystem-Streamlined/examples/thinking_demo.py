#!/usr/bin/env python3
"""
Thinking Demo for NovaSystem.

Demonstrates Gemini's thinking capabilities:
1. Thought summaries (see reasoning process)
2. Thinking levels (Gemini 3: low/high)
3. Thinking budgets (Gemini 2.5: token control)
4. Streaming with incremental thoughts
5. Problem solving (math, logic, code)

Requires: pip install google-genai

Usage:
    python thinking_demo.py
    python thinking_demo.py --demo math
    python thinking_demo.py --demo logic
    python thinking_demo.py --demo stream
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.utils.thinking_service import (
    ThinkingService,
    ThinkingLevel,
    ThinkingModel,
    think_about,
    solve_math,
    solve_logic,
    code_solution
)


async def demo_basic_thinking():
    """Demo: Basic thinking with thought summaries."""
    print("\n" + "="*60)
    print("🧠 Demo: Basic Thinking with Summaries")
    print("="*60)

    service = ThinkingService()

    prompt = "What is the sum of the first 50 prime numbers?"

    print(f"\n❓ Question: {prompt}")
    print("\n⏳ Thinking...")

    result = await service.think(prompt, include_thoughts=True)

    if result.thought_summary:
        print(f"\n💭 Thought Summary:")
        summary = result.thought_summary[:500] + "..." if len(result.thought_summary) > 500 else result.thought_summary
        print(f"   {summary}")

    print(f"\n✅ Answer:")
    print(f"   {result.answer}")

    print(f"\n📊 Token Usage:")
    print(f"   Thinking tokens: {result.thoughts_token_count}")
    print(f"   Output tokens: {result.output_token_count}")


async def demo_math_problem():
    """Demo: Solve complex math problems."""
    print("\n" + "="*60)
    print("🔢 Demo: Math Problem Solving")
    print("="*60)

    problems = [
        "Find the sum of all integer bases b > 9 for which 17_b is a divisor of 97_b",
        "Calculate the integral of x^2 * e^x from 0 to 1",
        "Prove that the square root of 2 is irrational (outline the proof)"
    ]

    service = ThinkingService()

    for problem in problems[:1]:  # Just first one for demo
        print(f"\n📝 Problem: {problem}")
        print("\n⏳ Thinking deeply...")

        result = await service.solve(problem, problem_type="math", show_work=True)

        if result.thought_summary:
            print(f"\n💭 Reasoning Process:")
            summary = result.thought_summary[:600] + "..." if len(result.thought_summary) > 600 else result.thought_summary
            print(f"   {summary}")

        print(f"\n✅ Solution:")
        answer = result.answer[:800] + "..." if len(result.answer) > 800 else result.answer
        print(f"   {answer}")


async def demo_logic_puzzle():
    """Demo: Solve logic puzzles."""
    print("\n" + "="*60)
    print("🧩 Demo: Logic Puzzle Solving")
    print("="*60)

    puzzle = """
    Alice, Bob, and Carol each live in a different house on the same street: red, green, and blue.
    The person who lives in the red house owns a cat.
    Bob does not live in the green house.
    Carol owns a dog.
    The green house is to the left of the red house.
    Alice does not own a cat.
    
    Who lives in each house, and what pet do they own?
    """

    print(f"\n📝 Puzzle: {puzzle}")

    service = ThinkingService()

    print("\n⏳ Reasoning through the puzzle...")

    result = await service.solve(puzzle.strip(), problem_type="logic", show_work=True)

    if result.thought_summary:
        print(f"\n💭 Reasoning Process:")
        print(f"   {result.thought_summary}")

    print(f"\n✅ Solution:")
    print(f"   {result.answer}")


async def demo_reasoning():
    """Demo: Logical reasoning from premises."""
    print("\n" + "="*60)
    print("🔍 Demo: Logical Reasoning")
    print("="*60)

    service = ThinkingService()

    premises = [
        "All mammals are warm-blooded.",
        "All whales are mammals.",
        "Some sea creatures are whales.",
        "All warm-blooded animals need to eat regularly."
    ]

    question = "Can we conclude that some sea creatures need to eat regularly?"

    print("\n📋 Premises:")
    for i, p in enumerate(premises, 1):
        print(f"   {i}. {p}")

    print(f"\n❓ Question: {question}")
    print("\n⏳ Reasoning...")

    result = await service.reason(premises, question)

    if result.thought_summary:
        print(f"\n💭 Reasoning Chain:")
        print(f"   {result.thought_summary}")

    print(f"\n✅ Conclusion:")
    print(f"   {result.answer}")


async def demo_code_generation():
    """Demo: Generate code with thinking."""
    print("\n" + "="*60)
    print("💻 Demo: Code Generation with Thinking")
    print("="*60)

    problem = """
    Write a Python function that implements binary search on a sorted list.
    Include:
    - Iterative implementation
    - Edge case handling
    - Time complexity analysis in comments
    """

    print(f"\n📝 Task: {problem}")

    service = ThinkingService()

    print("\n⏳ Thinking about implementation...")

    result = await service.solve(problem, problem_type="code", show_work=True)

    if result.thought_summary:
        print(f"\n💭 Design Thoughts:")
        summary = result.thought_summary[:400] + "..." if len(result.thought_summary) > 400 else result.thought_summary
        print(f"   {summary}")

    print(f"\n✅ Code:")
    print(result.answer)


async def demo_streaming():
    """Demo: Streaming with incremental thoughts."""
    print("\n" + "="*60)
    print("🌊 Demo: Streaming Thoughts")
    print("="*60)

    prompt = "Explain step by step how to calculate 47 * 83 mentally."

    print(f"\n❓ Question: {prompt}")
    print("\n🌊 Streaming response with thoughts...\n")

    service = ThinkingService()

    thoughts_shown = False
    answer_shown = False

    async for part in service.think_stream(prompt, include_thoughts=True):
        if part.is_thought:
            if not thoughts_shown:
                print("💭 THOUGHTS:")
                thoughts_shown = True
            print(f"   {part.text}", end="")
        else:
            if not answer_shown:
                if thoughts_shown:
                    print("\n")
                print("✅ ANSWER:")
                answer_shown = True
            print(f"   {part.text}", end="")

    print("\n")


async def demo_thinking_budget():
    """Demo: Controlling thinking budget."""
    print("\n" + "="*60)
    print("⚙️ Demo: Thinking Budget Control")
    print("="*60)

    prompt = "What is 15 * 17?"

    service = ThinkingService(model=ThinkingModel.GEMINI_25_FLASH)

    budgets = [
        (0, "Thinking disabled"),
        (1024, "Light thinking"),
        (4096, "Deep thinking"),
    ]

    for budget, description in budgets:
        print(f"\n📊 {description} (budget={budget}):")

        result = await service.think(
            prompt,
            include_thoughts=True,
            thinking_budget=budget
        )

        print(f"   Answer: {result.answer}")
        print(f"   Thought tokens: {result.thoughts_token_count or 'N/A'}")


async def run_all_demos():
    """Run all demos."""
    print("\n" + "="*60)
    print("🚀 NovaSystem Thinking Demo")
    print("    Using Gemini's Reasoning Capabilities")
    print("="*60)

    demos = [
        ("Basic Thinking", demo_basic_thinking),
        ("Logic Puzzle", demo_logic_puzzle),
        ("Reasoning", demo_reasoning),
        ("Streaming", demo_streaming),
    ]

    for name, demo_func in demos:
        try:
            await demo_func()
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")

    print("\n" + "="*60)
    print("✨ Demo complete!")
    print("="*60)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Thinking Demo")
    parser.add_argument(
        "--demo",
        choices=["all", "basic", "math", "logic", "reason", "code", "stream", "budget"],
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
        "all": run_all_demos,
        "basic": demo_basic_thinking,
        "math": demo_math_problem,
        "logic": demo_logic_puzzle,
        "reason": demo_reasoning,
        "code": demo_code_generation,
        "stream": demo_streaming,
        "budget": demo_thinking_budget,
    }

    await demo_map[args.demo]()


if __name__ == "__main__":
    asyncio.run(main())
