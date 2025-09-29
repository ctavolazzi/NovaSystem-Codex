#!/usr/bin/env python3
"""
Basic usage example for NovaSystem.

This example demonstrates how to use the Nova Process to solve a problem
programmatically.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from novasystem import NovaProcess
from novasystem.core.memory import MemoryManager

async def main():
    """Main example function."""
    print("🧠 NovaSystem Basic Usage Example")
    print("=" * 50)

    # Create memory manager
    memory_manager = MemoryManager()

    # Create Nova Process with specific domains
    nova_process = NovaProcess(
        domains=["Technology", "Business", "User Experience"],
        model="gpt-4",
        memory_manager=memory_manager
    )

    # Define the problem
    problem = """
    Our e-commerce platform is experiencing slow page load times, especially on mobile devices.
    We need to optimize performance while maintaining all existing functionality and not breaking
    any current features. The platform serves thousands of users daily and processes hundreds of
    transactions per hour.
    """

    print(f"Problem: {problem.strip()}")
    print("\n🤔 Starting Nova Process...")
    print("-" * 30)

    # Run the Nova Process
    result = await nova_process.solve_problem(
        problem,
        max_iterations=3,
        stream=False
    )

    # Display results
    print("\n🚀 Nova Process Results")
    print("=" * 50)

    if result:
        # Display final synthesis
        if "final_synthesis" in result:
            print("\n📋 Final Synthesis:")
            print("-" * 20)
            print(result["final_synthesis"])

        # Display final validation
        if "final_validation" in result:
            print("\n✅ Final Validation:")
            print("-" * 20)
            print(result["final_validation"])

        # Display process summary
        if "total_iterations" in result:
            print(f"\n📊 Process Summary:")
            print("-" * 20)
            print(f"Total Iterations: {result['total_iterations']}")
            print(f"Process Phase: {result.get('phase', 'Unknown')}")
    else:
        print("No result available.")

    # Display memory statistics
    stats = memory_manager.get_memory_stats()
    print(f"\n🧠 Memory Statistics:")
    print("-" * 20)
    print(f"Short-term memories: {stats['short_term_count']}")
    print(f"Long-term memories: {stats['long_term_count']}")
    print(f"Total contexts: {stats['total_contexts']}")

if __name__ == "__main__":
    asyncio.run(main())
