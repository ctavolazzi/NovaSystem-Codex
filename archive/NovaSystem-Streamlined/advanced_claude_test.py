#!/usr/bin/env python3
"""
Advanced test suite for Claude models - testing real-world scenarios,
performance under load, and edge cases.
"""

import asyncio
import os
import sys
import time
import statistics
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from novasystem.utils.llm_service import LLMService

class AdvancedClaudeTestSuite:
    def __init__(self):
        self.llm_service = LLMService()
        self.test_results = {}

    async def test_default_model_behavior(self):
        """Test default model behavior in various scenarios."""
        print("🎯 Testing Default Model Behavior")
        print("=" * 50)

        default_model = self.llm_service.get_default_model()
        print(f"Default model: {default_model}")

        # Test 1: Basic completion without specifying model
        print("\n📝 Test 1: Basic completion (no model specified)")
        messages = [{"role": "user", "content": "What is 5 + 3? Answer with just the number."}]

        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=messages,
                temperature=0.1,
                max_tokens=10
            )
            end_time = time.time()
            print(f"✅ Response: {response.strip()}")
            print(f"⏱️ Time: {end_time - start_time:.2f}s")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

        # Test 2: Streaming without specifying model
        print("\n🌊 Test 2: Streaming (no model specified)")
        messages = [{"role": "user", "content": "Count from 1 to 3, one number per line."}]

        start_time = time.time()
        try:
            chunks = []
            async for chunk in self.llm_service.stream_completion(
                messages=messages,
                temperature=0.1
            ):
                chunks.append(chunk)
            end_time = time.time()
            full_response = "".join(chunks)
            print(f"✅ Response: {full_response.strip()}")
            print(f"⏱️ Time: {end_time - start_time:.2f}s")
            print(f"📦 Chunks: {len(chunks)}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    async def test_conversation_flow(self):
        """Test multi-turn conversation with default model."""
        print(f"\n💬 Testing Conversation Flow")
        print("=" * 50)

        conversation = [
            {"role": "user", "content": "Hi! My name is Alice and I'm learning Python."},
            {"role": "assistant", "content": "Hello Alice! That's great that you're learning Python. What would you like to know about Python?"},
            {"role": "user", "content": "What's a good first project to build?"},
            {"role": "assistant", "content": "A great first Python project is a simple calculator or a to-do list app. These help you practice basic concepts like variables, functions, and user input."},
            {"role": "user", "content": "Can you help me build a simple calculator?"}
        ]

        print("Testing conversation context preservation...")
        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=conversation,
                temperature=0.7,
                max_tokens=200
            )
            end_time = time.time()
            print(f"✅ Response: {response[:100]}...")
            print(f"⏱️ Time: {end_time - start_time:.2f}s")

            # Check if response mentions Alice (context preservation)
            if "Alice" in response:
                print("✅ Context preserved: Response mentions Alice")
            else:
                print("⚠️ Context may not be fully preserved")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    async def test_system_prompt_handling(self):
        """Test system prompt functionality."""
        print(f"\n⚙️ Testing System Prompt Handling")
        print("=" * 50)

        # Test with system prompt
        messages = [
            {"role": "system", "content": "You are a helpful math tutor. Always show your work step by step and be encouraging."},
            {"role": "user", "content": "How do I solve 2x + 5 = 13?"}
        ]

        print("Testing with system prompt...")
        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=messages,
                temperature=0.3,
                max_tokens=300
            )
            end_time = time.time()
            print(f"✅ Response: {response[:150]}...")
            print(f"⏱️ Time: {end_time - start_time:.2f}s")

            # Check if response shows step-by-step work
            if "step" in response.lower() or "=" in response:
                print("✅ System prompt followed: Shows step-by-step work")
            else:
                print("⚠️ System prompt may not be fully followed")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    async def test_different_tasks(self):
        """Test various task types with default model."""
        print(f"\n🎯 Testing Different Task Types")
        print("=" * 50)

        tasks = [
            {
                "name": "Math Problem",
                "messages": [{"role": "user", "content": "What is the area of a circle with radius 5? Use π = 3.14"}],
                "expected_keywords": ["78.5", "area", "π"]
            },
            {
                "name": "Code Generation",
                "messages": [{"role": "user", "content": "Write a Python function to check if a number is prime."}],
                "expected_keywords": ["def", "prime", "return"]
            },
            {
                "name": "Creative Writing",
                "messages": [{"role": "user", "content": "Write a short haiku about coding."}],
                "expected_keywords": ["code", "program"]
            },
            {
                "name": "Analysis Task",
                "messages": [{"role": "user", "content": "What are the pros and cons of renewable energy?"}],
                "expected_keywords": ["pros", "cons", "renewable"]
            }
        ]

        for task in tasks:
            print(f"\n🧪 {task['name']}:")
            start_time = time.time()
            try:
                response = await self.llm_service.get_completion(
                    messages=task["messages"],
                    temperature=0.7,
                    max_tokens=200
                )
                end_time = time.time()

                # Check for expected keywords
                found_keywords = [kw for kw in task["expected_keywords"] if kw.lower() in response.lower()]
                keyword_score = len(found_keywords) / len(task["expected_keywords"])

                print(f"✅ Response: {response[:80]}...")
                print(f"⏱️ Time: {end_time - start_time:.2f}s")
                print(f"🎯 Keyword match: {keyword_score:.1%} ({len(found_keywords)}/{len(task['expected_keywords'])})")

            except Exception as e:
                print(f"❌ Error: {str(e)}")

    async def test_performance_under_load(self):
        """Test performance with multiple concurrent requests."""
        print(f"\n⚡ Testing Performance Under Load")
        print("=" * 50)

        # Create multiple concurrent requests
        async def single_request(request_id):
            messages = [{"role": "user", "content": f"Request {request_id}: What is {request_id} * 2?"}]
            start_time = time.time()
            try:
                response = await self.llm_service.get_completion(
                    messages=messages,
                    temperature=0.1,
                    max_tokens=20
                )
                end_time = time.time()
                return {
                    "id": request_id,
                    "success": True,
                    "response": response.strip(),
                    "time": end_time - start_time
                }
            except Exception as e:
                return {
                    "id": request_id,
                    "success": False,
                    "error": str(e),
                    "time": None
                }

        # Run 5 concurrent requests
        print("Running 5 concurrent requests...")
        start_time = time.time()
        tasks = [single_request(i) for i in range(1, 6)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # Analyze results
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        print(f"✅ Successful: {len(successful)}/5")
        print(f"❌ Failed: {len(failed)}/5")
        print(f"⏱️ Total time: {end_time - start_time:.2f}s")

        if successful:
            times = [r["time"] for r in successful]
            print(f"📊 Response times: avg={statistics.mean(times):.2f}s, min={min(times):.2f}s, max={max(times):.2f}s")

            # Show sample responses
            print("📝 Sample responses:")
            for result in successful[:3]:
                print(f"  Request {result['id']}: {result['response']}")

    async def test_model_switching(self):
        """Test switching between different Claude models."""
        print(f"\n🔄 Testing Model Switching")
        print("=" * 50)

        models_to_test = [
            "claude-3-5-sonnet-20241022",  # Default
            "claude-3-5-haiku-20241022",   # Fast
            "claude-sonnet-4-20250514"     # Latest
        ]

        messages = [{"role": "user", "content": "What is 7 * 8? Answer with just the number."}]

        for model in models_to_test:
            print(f"\n🧪 Testing {model}:")
            start_time = time.time()
            try:
                response = await self.llm_service.get_completion(
                    messages=messages,
                    model=model,
                    temperature=0.1,
                    max_tokens=10
                )
                end_time = time.time()
                print(f"✅ Response: {response.strip()}")
                print(f"⏱️ Time: {end_time - start_time:.2f}s")

                # Get model capabilities
                caps = self.llm_service.get_model_capabilities(model)
                print(f"📊 Speed rating: {caps.get('speed')}/100")

            except Exception as e:
                print(f"❌ Error: {str(e)}")

    async def test_error_handling(self):
        """Test error handling scenarios."""
        print(f"\n🚨 Testing Error Handling")
        print("=" * 50)

        error_scenarios = [
            {
                "name": "Invalid model name",
                "messages": [{"role": "user", "content": "Hello"}],
                "model": "invalid-model-name"
            },
            {
                "name": "Empty messages",
                "messages": [],
                "model": None
            },
            {
                "name": "Very high temperature",
                "messages": [{"role": "user", "content": "Hello"}],
                "model": None,
                "temperature": 2.0
            }
        ]

        for scenario in error_scenarios:
            print(f"\n🧪 {scenario['name']}:")
            try:
                response = await self.llm_service.get_completion(
                    messages=scenario["messages"],
                    model=scenario.get("model"),
                    temperature=scenario.get("temperature", 0.7),
                    max_tokens=50
                )
                print(f"✅ Handled gracefully: {response[:50]}...")
            except Exception as e:
                print(f"✅ Error caught: {str(e)[:100]}...")

    async def run_all_tests(self):
        """Run all advanced tests."""
        print("🚀 Advanced Claude Test Suite")
        print("=" * 60)

        # Check if Anthropic client is available
        if not self.llm_service.anthropic_client:
            print("❌ Anthropic client not initialized")
            print("Please set your ANTHROPIC_API_KEY environment variable")
            return

        print("✅ Anthropic client initialized successfully")

        # Run all tests
        await self.test_default_model_behavior()
        await self.test_conversation_flow()
        await self.test_system_prompt_handling()
        await self.test_different_tasks()
        await self.test_performance_under_load()
        await self.test_model_switching()
        await self.test_error_handling()

        print(f"\n🎉 Advanced testing completed!")
        print("=" * 60)

async def main():
    """Main test function."""
    test_suite = AdvancedClaudeTestSuite()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
