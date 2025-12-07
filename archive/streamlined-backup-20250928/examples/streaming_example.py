#!/usr/bin/env python3
"""
Streaming example for NovaSystem.

This example demonstrates how to use the Nova Process with streaming
to get real-time updates during problem-solving.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novasystem import NovaProcess, MemoryManager

async def main():
    """Main streaming example function."""
    print("🧠 NovaSystem Streaming Example")
    print("=" * 50)

    # Create memory manager
    memory_manager = MemoryManager()

    # Create Nova Process
    nova_process = NovaProcess(
        domains=["Software Engineering", "DevOps", "Security"],
        model="gpt-4",
        memory_manager=memory_manager
    )

    # Define the problem
    problem = """
    We need to implement a secure, scalable authentication system for our microservices
    architecture. The system should support multiple authentication methods (OAuth, JWT,
    API keys) and integrate with our existing user management system. We also need to
    ensure it can handle high traffic loads and maintain security best practices.
    """

    print(f"Problem: {problem.strip()}")
    print("\n🤔 Starting Nova Process with streaming...")
    print("-" * 50)

    # Run the Nova Process with streaming
    async for update in nova_process.solve_problem(
        problem,
        max_iterations=4,
        stream=True
    ):
        # Handle different types of updates
        if update["type"] == "start":
            print(f"🚀 Started: {update.get('problem', 'Unknown problem')[:100]}...")
            print(f"⏰ Timestamp: {update.get('timestamp', 'Unknown')}")

        elif update["type"] == "phase":
            print(f"\n📋 Phase: {update.get('phase', 'Unknown')}")
            print("-" * 30)

        elif update["type"] == "iteration":
            print(f"\n🔄 Iteration {update.get('number', 'Unknown')}")
            print("-" * 20)

        elif update["type"] == "agent_working":
            print(f"🤖 {update.get('agent', 'Unknown agent')} is working...")

        elif update["type"] == "result":
            if "phase" in update:
                print(f"✅ {update['phase']} completed")
            elif "iteration" in update:
                print(f"✅ Iteration {update['iteration']} completed")

        elif update["type"] == "convergence":
            print(f"🎯 Converged at iteration {update.get('iteration', 'Unknown')}")

        elif update["type"] == "complete":
            print(f"\n🎉 Process completed!")
            result = update.get("result", {})
            if result:
                print(f"📊 Total iterations: {result.get('total_iterations', 'Unknown')}")
                print(f"📋 Final phase: {result.get('phase', 'Unknown')}")

        elif update["type"] == "error":
            print(f"❌ Error: {update.get('error', 'Unknown error')}")

        else:
            print(f"📝 Update: {update}")

    print("\n" + "=" * 50)
    print("🏁 Streaming example completed!")

if __name__ == "__main__":
    asyncio.run(main())
