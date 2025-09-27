#!/usr/bin/env python3
"""
Comprehensive test suite for all Claude models in NovaSystem.
Tests performance, capabilities, edge cases, and real-world scenarios.
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

class ClaudeTestSuite:
    def __init__(self):
        self.llm_service = LLMService()
        self.results = {}
        self.claude_models = [
            "claude-opus-4-1-20250805",
            "claude-opus-4-20250514",
            "claude-sonnet-4-20250514",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]

    async def test_model_availability(self):
        """Test which Claude models are available."""
        print("🔍 Testing Model Availability")
        print("=" * 50)

        available_models = self.llm_service.get_available_models()
        claude_available = [model for model in available_models if model.startswith("claude-")]

        print(f"Total Claude models configured: {len(self.claude_models)}")
        print(f"Claude models available: {len(claude_available)}")
        print("\nAvailable Claude models:")
        for model in claude_available:
            print(f"  ✅ {model}")

        # Test unavailable models
        unavailable = [model for model in self.claude_models if model not in claude_available]
        if unavailable:
            print(f"\nUnavailable models:")
            for model in unavailable:
                print(f"  ❌ {model}")

        self.results['available_models'] = claude_available
        return claude_available

    async def test_model_capabilities(self, models):
        """Test model capability reporting."""
        print(f"\n📊 Testing Model Capabilities")
        print("=" * 50)

        for model in models:
            caps = self.llm_service.get_model_capabilities(model)
            print(f"\n{model}:")
            print(f"  Type: {caps.get('type')}")
            print(f"  Reasoning: {caps.get('reasoning')}/100")
            print(f"  Coding: {caps.get('coding')}/100")
            print(f"  Analysis: {caps.get('analysis')}/100")
            print(f"  Creativity: {caps.get('creativity')}/100")
            print(f"  Speed: {caps.get('speed')}/100")
            print(f"  Context: {caps.get('context_length'):,} tokens")
            print(f"  Description: {caps.get('description')}")

    async def test_basic_completion(self, model):
        """Test basic completion functionality."""
        messages = [
            {"role": "user", "content": "Hello! Please respond with a brief greeting and identify yourself."}
        ]

        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=messages,
                model=model,
                temperature=0.7,
                max_tokens=100
            )
            end_time = time.time()
            response_time = end_time - start_time

            return {
                "success": True,
                "response": response,
                "response_time": response_time,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "response_time": None,
                "error": str(e)
            }

    async def test_streaming(self, model):
        """Test streaming completion."""
        messages = [
            {"role": "user", "content": "Count from 1 to 3, one number per line."}
        ]

        try:
            start_time = time.time()
            chunks = []
            async for chunk in self.llm_service.stream_completion(
                messages=messages,
                model=model,
                temperature=0.7
            ):
                chunks.append(chunk)
            end_time = time.time()
            response_time = end_time - start_time

            full_response = "".join(chunks)
            return {
                "success": True,
                "response": full_response,
                "response_time": response_time,
                "chunk_count": len(chunks),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "response_time": None,
                "chunk_count": 0,
                "error": str(e)
            }

    async def test_reasoning_task(self, model):
        """Test reasoning capabilities."""
        messages = [
            {"role": "user", "content": "If a train leaves station A at 60 mph and another leaves station B at 40 mph, and they are 200 miles apart, how long until they meet if they're heading toward each other?"}
        ]

        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=messages,
                model=model,
                temperature=0.3,
                max_tokens=200
            )
            end_time = time.time()
            response_time = end_time - start_time

            return {
                "success": True,
                "response": response,
                "response_time": response_time,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "response_time": None,
                "error": str(e)
            }

    async def test_coding_task(self, model):
        """Test coding capabilities."""
        messages = [
            {"role": "user", "content": "Write a simple Python function that calculates the factorial of a number. Keep it concise."}
        ]

        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=messages,
                model=model,
                temperature=0.3,
                max_tokens=300
            )
            end_time = time.time()
            response_time = end_time - start_time

            return {
                "success": True,
                "response": response,
                "response_time": response_time,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "response_time": None,
                "error": str(e)
            }

    async def test_creativity_task(self, model):
        """Test creativity capabilities."""
        messages = [
            {"role": "user", "content": "Write a short, creative haiku about artificial intelligence."}
        ]

        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=messages,
                model=model,
                temperature=0.9,
                max_tokens=100
            )
            end_time = time.time()
            response_time = end_time - start_time

            return {
                "success": True,
                "response": response,
                "response_time": response_time,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "response_time": None,
                "error": str(e)
            }

    async def test_system_message(self, model):
        """Test system message handling."""
        messages = [
            {"role": "system", "content": "You are a helpful math tutor. Always show your work step by step."},
            {"role": "user", "content": "What is 15 * 23?"}
        ]

        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=messages,
                model=model,
                temperature=0.3,
                max_tokens=200
            )
            end_time = time.time()
            response_time = end_time - start_time

            return {
                "success": True,
                "response": response,
                "response_time": response_time,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "response_time": None,
                "error": str(e)
            }

    async def test_conversation_context(self, model):
        """Test multi-turn conversation."""
        messages = [
            {"role": "user", "content": "My name is Alice."},
            {"role": "assistant", "content": "Hello Alice! Nice to meet you."},
            {"role": "user", "content": "What's my name?"}
        ]

        start_time = time.time()
        try:
            response = await self.llm_service.get_completion(
                messages=messages,
                model=model,
                temperature=0.7,
                max_tokens=100
            )
            end_time = time.time()
            response_time = end_time - start_time

            return {
                "success": True,
                "response": response,
                "response_time": response_time,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "response_time": None,
                "error": str(e)
            }

    async def test_edge_cases(self, model):
        """Test edge cases and error handling."""
        edge_cases = [
            {
                "name": "Empty message",
                "messages": [{"role": "user", "content": ""}]
            },
            {
                "name": "Very long message",
                "messages": [{"role": "user", "content": "Hello " * 1000}]
            },
            {
                "name": "Special characters",
                "messages": [{"role": "user", "content": "Test: @#$%^&*()_+{}|:<>?[]\\;'\",./"}]
            }
        ]

        results = {}
        for case in edge_cases:
            try:
                response = await self.llm_service.get_completion(
                    messages=case["messages"],
                    model=model,
                    temperature=0.7,
                    max_tokens=50
                )
                results[case["name"]] = {
                    "success": True,
                    "response": response[:100] + "..." if len(response) > 100 else response,
                    "error": None
                }
            except Exception as e:
                results[case["name"]] = {
                    "success": False,
                    "response": None,
                    "error": str(e)
                }

        return results

    async def run_comprehensive_test(self, model):
        """Run all tests for a specific model."""
        print(f"\n🧪 Comprehensive Testing: {model}")
        print("=" * 60)

        model_results = {}

        # Basic completion test
        print("📝 Testing basic completion...")
        basic_result = await self.test_basic_completion(model)
        model_results['basic_completion'] = basic_result
        if basic_result['success']:
            print(f"  ✅ Success ({basic_result['response_time']:.2f}s): {basic_result['response'][:50]}...")
        else:
            print(f"  ❌ Failed: {basic_result['error']}")

        # Streaming test
        print("🌊 Testing streaming...")
        streaming_result = await self.test_streaming(model)
        model_results['streaming'] = streaming_result
        if streaming_result['success']:
            print(f"  ✅ Success ({streaming_result['response_time']:.2f}s, {streaming_result['chunk_count']} chunks)")
        else:
            print(f"  ❌ Failed: {streaming_result['error']}")

        # Reasoning test
        print("🧠 Testing reasoning...")
        reasoning_result = await self.test_reasoning_task(model)
        model_results['reasoning'] = reasoning_result
        if reasoning_result['success']:
            print(f"  ✅ Success ({reasoning_result['response_time']:.2f}s)")
        else:
            print(f"  ❌ Failed: {reasoning_result['error']}")

        # Coding test
        print("💻 Testing coding...")
        coding_result = await self.test_coding_task(model)
        model_results['coding'] = coding_result
        if coding_result['success']:
            print(f"  ✅ Success ({coding_result['response_time']:.2f}s)")
        else:
            print(f"  ❌ Failed: {coding_result['error']}")

        # Creativity test
        print("🎨 Testing creativity...")
        creativity_result = await self.test_creativity_task(model)
        model_results['creativity'] = creativity_result
        if creativity_result['success']:
            print(f"  ✅ Success ({creativity_result['response_time']:.2f}s)")
        else:
            print(f"  ❌ Failed: {creativity_result['error']}")

        # System message test
        print("⚙️ Testing system messages...")
        system_result = await self.test_system_message(model)
        model_results['system_message'] = system_result
        if system_result['success']:
            print(f"  ✅ Success ({system_result['response_time']:.2f}s)")
        else:
            print(f"  ❌ Failed: {system_result['error']}")

        # Conversation context test
        print("💬 Testing conversation context...")
        context_result = await self.test_conversation_context(model)
        model_results['conversation_context'] = context_result
        if context_result['success']:
            print(f"  ✅ Success ({context_result['response_time']:.2f}s)")
        else:
            print(f"  ❌ Failed: {context_result['error']}")

        # Edge cases test
        print("🔍 Testing edge cases...")
        edge_results = await self.test_edge_cases(model)
        model_results['edge_cases'] = edge_results
        edge_success_count = sum(1 for result in edge_results.values() if result['success'])
        print(f"  ✅ {edge_success_count}/{len(edge_results)} edge cases passed")

        return model_results

    async def run_performance_comparison(self, models):
        """Run performance comparison across models."""
        print(f"\n⚡ Performance Comparison")
        print("=" * 50)

        # Simple speed test
        speed_test_messages = [
            {"role": "user", "content": "What is 2+2? Answer in one word."}
        ]

        performance_results = {}

        for model in models:
            print(f"\nTesting {model}...")
            times = []

            # Run 3 speed tests and average
            for i in range(3):
                start_time = time.time()
                try:
                    response = await self.llm_service.get_completion(
                        messages=speed_test_messages,
                        model=model,
                        temperature=0.1,
                        max_tokens=10
                    )
                    end_time = time.time()
                    times.append(end_time - start_time)
                except Exception as e:
                    print(f"  ❌ Test {i+1} failed: {str(e)}")
                    times.append(None)

            # Calculate statistics
            valid_times = [t for t in times if t is not None]
            if valid_times:
                avg_time = statistics.mean(valid_times)
                min_time = min(valid_times)
                max_time = max(valid_times)
                performance_results[model] = {
                    "avg_time": avg_time,
                    "min_time": min_time,
                    "max_time": max_time,
                    "success_rate": len(valid_times) / len(times)
                }
                print(f"  ✅ Avg: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s")
            else:
                performance_results[model] = None
                print(f"  ❌ All tests failed")

        return performance_results

    def print_summary(self, all_results, performance_results):
        """Print comprehensive test summary."""
        print(f"\n📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)

        # Overall success rate
        total_tests = 0
        successful_tests = 0

        for model, results in all_results.items():
            for test_name, result in results.items():
                if test_name == 'edge_cases':
                    for edge_case, edge_result in result.items():
                        total_tests += 1
                        if edge_result['success']:
                            successful_tests += 1
                else:
                    total_tests += 1
                    if result['success']:
                        successful_tests += 1

        success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"Overall Success Rate: {success_rate:.1f}% ({successful_tests}/{total_tests})")

        # Model-by-model summary
        print(f"\nModel Performance Summary:")
        for model, results in all_results.items():
            model_success = 0
            model_total = 0

            for test_name, result in results.items():
                if test_name == 'edge_cases':
                    for edge_case, edge_result in result.items():
                        model_total += 1
                        if edge_result['success']:
                            model_success += 1
                else:
                    model_total += 1
                    if result['success']:
                        model_success += 1

            model_rate = (model_success / model_total) * 100 if model_total > 0 else 0
            perf_info = ""
            if model in performance_results and performance_results[model]:
                perf_info = f" (Avg: {performance_results[model]['avg_time']:.2f}s)"

            print(f"  {model}: {model_rate:.1f}%{perf_info}")

        # Speed ranking
        print(f"\n🏃 Speed Ranking (Fastest to Slowest):")
        valid_performance = {k: v for k, v in performance_results.items() if v is not None}
        sorted_models = sorted(valid_performance.items(), key=lambda x: x[1]['avg_time'])

        for i, (model, perf) in enumerate(sorted_models, 1):
            print(f"  {i}. {model}: {perf['avg_time']:.2f}s avg")

        print(f"\n🎉 Comprehensive testing completed!")

async def main():
    """Main test function."""
    print("🚀 Claude Models Comprehensive Test Suite")
    print("=" * 60)

    # Check if Anthropic client is available
    test_suite = ClaudeTestSuite()
    if not test_suite.llm_service.anthropic_client:
        print("❌ Anthropic client not initialized")
        print("Please set your ANTHROPIC_API_KEY environment variable")
        return

    print("✅ Anthropic client initialized successfully")

    # Test model availability
    available_models = await test_suite.test_model_availability()

    if not available_models:
        print("❌ No Claude models available for testing")
        return

    # Test model capabilities
    await test_suite.test_model_capabilities(available_models)

    # Run comprehensive tests on each model
    all_results = {}
    for model in available_models:
        all_results[model] = await test_suite.run_comprehensive_test(model)

    # Run performance comparison
    performance_results = await test_suite.run_performance_comparison(available_models)

    # Print summary
    test_suite.print_summary(all_results, performance_results)

if __name__ == "__main__":
    asyncio.run(main())
