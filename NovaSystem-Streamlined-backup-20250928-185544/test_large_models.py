#!/usr/bin/env python3
"""
Test script for NovaSystem with large Ollama models.

This script tests the system's ability to handle very large models (13GB+)
and verifies that performance monitoring and caching work correctly.
"""

import asyncio
import sys
import os
import time
import logging
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from novasystem.core.process import NovaProcess
from novasystem.core.memory import MemoryManager
from novasystem.utils.llm_service import LLMService
from novasystem.utils.metrics import get_metrics_collector
from novasystem.utils.model_cache import get_model_cache

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_large_model(model_name: str, problem: str = "Design a scalable microservices architecture"):
    """Test a specific large model."""
    print(f"\n🧪 Testing Large Model: {model_name}")
    print("=" * 60)

    # Create session ID for metrics tracking
    session_id = f"test_{model_name}_{int(time.time())}"

    try:
        # Initialize services
        llm_service = LLMService()
        memory_manager = MemoryManager()

        # Check if model is available
        available_models = llm_service.get_available_models()
        if model_name not in available_models:
            print(f"❌ Model {model_name} not available")
            print(f"Available models: {available_models}")
            return False

        print(f"✅ Model {model_name} is available")

        # Create Nova Process
        nova_process = NovaProcess(
            domains=["Technology", "Architecture", "Performance"],
            model=model_name,
            memory_manager=memory_manager,
            llm_service=llm_service
        )

        print(f"🚀 Starting Nova Process with {model_name}")
        print(f"📋 Problem: {problem}")
        print(f"🆔 Session ID: {session_id}")

        # Record start time
        start_time = time.time()

        # Run the process with limited iterations for testing
        result = await nova_process.solve_problem(
            problem_statement=problem,
            max_iterations=2,  # Limited for testing
            stream=False,
            session_id=session_id
        )

        # Record end time
        end_time = time.time()
        total_time = end_time - start_time

        print(f"\n✅ Process completed in {total_time:.2f} seconds")

        # Display results summary
        if result and "final_synthesis" in result:
            synthesis = result["final_synthesis"]
            print(f"\n📋 Final Synthesis (first 200 chars):")
            print(f"{synthesis[:200]}...")

        # Get performance metrics
        metrics = nova_process.get_performance_metrics(session_id)
        if metrics:
            print(f"\n📊 Performance Metrics:")
            print(f"  Total Time: {metrics.get('total_time', 0):.2f}s")
            print(f"  Average LLM Response Time: {metrics.get('average_llm_response_time', 0):.2f}s")
            print(f"  Total Tokens Generated: {metrics.get('total_tokens_generated', 0)}")
            print(f"  Total Iterations: {metrics.get('total_iterations', 0)}")
            print(f"  Models Used: {', '.join(metrics.get('models_used', []))}")

        # Get cache stats
        cache = get_model_cache()
        cache_stats = cache.get_cache_stats()
        print(f"\n🗄️  Cache Stats:")
        print(f"  Cache Hit Rate: {cache_stats['hit_rate_percent']:.1f}%")
        print(f"  Models in Cache: {cache_stats['cache_size']}")
        print(f"  Memory Usage: {cache_stats['total_memory_mb']:.1f}MB")

        return True

    except Exception as e:
        print(f"❌ Error testing model {model_name}: {e}")
        logger.exception("Detailed error:")
        return False

async def test_model_loading_performance():
    """Test model loading performance."""
    print("\n⚡ Testing Model Loading Performance")
    print("=" * 60)

    # Test models in order of size
    test_models = [
        "ollama:phi3",           # ~2.2GB (fast)
        "ollama:gemma3n",        # ~7.5GB (medium)
        "ollama:gpt-oss:20b",    # ~13GB (large)
    ]

    results = {}

    for model in test_models:
        print(f"\n🔄 Testing {model}...")

        try:
            llm_service = LLMService()

            # Check if model is available
            available_models = llm_service.get_available_models()
            if model not in available_models:
                print(f"⏭️  Skipping {model} - not available")
                continue

            # Test simple completion
            start_time = time.time()

            messages = [
                {"role": "user", "content": "Hello! Please respond with a brief greeting."}
            ]

            response = await llm_service.get_completion(
                messages=messages,
                model=model,
                temperature=0.7
            )

            end_time = time.time()
            response_time = end_time - start_time

            results[model] = {
                'response_time': response_time,
                'response_length': len(response),
                'success': True
            }

            print(f"✅ {model}: {response_time:.2f}s, {len(response)} chars")

        except Exception as e:
            print(f"❌ {model}: Error - {e}")
            results[model] = {
                'response_time': 0,
                'response_length': 0,
                'success': False,
                'error': str(e)
            }

    # Summary
    print(f"\n📊 Model Loading Performance Summary:")
    print("=" * 60)

    successful_models = [m for m, r in results.items() if r['success']]
    if successful_models:
        fastest_model = min(successful_models, key=lambda m: results[m]['response_time'])
        slowest_model = max(successful_models, key=lambda m: results[m]['response_time'])

        print(f"✅ Successfully tested {len(successful_models)} models")
        print(f"🚀 Fastest: {fastest_model} ({results[fastest_model]['response_time']:.2f}s)")
        print(f"🐌 Slowest: {slowest_model} ({results[slowest_model]['response_time']:.2f}s)")

        # Performance comparison
        if len(successful_models) > 1:
            fastest_time = results[fastest_model]['response_time']
            slowest_time = results[slowest_model]['response_time']
            speedup = slowest_time / fastest_time if fastest_time > 0 else 0
            print(f"⚡ Speed difference: {speedup:.1f}x")
    else:
        print("❌ No models were successfully tested")

    return results

async def test_memory_usage():
    """Test memory usage with large models."""
    print("\n💾 Testing Memory Usage")
    print("=" * 60)

    import psutil
    process = psutil.Process()

    # Get initial memory
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"Initial memory usage: {initial_memory:.1f}MB")

    # Test with largest available model
    llm_service = LLMService()
    available_models = llm_service.get_available_models()

    large_models = [m for m in available_models if "gpt-oss" in m or "20b" in m or "gemma" in m]

    if not large_models:
        print("⚠️  No large models available for memory testing")
        return

    largest_model = large_models[0]  # Use first large model found
    print(f"Testing with: {largest_model}")

    try:
        # Create Nova Process
        memory_manager = MemoryManager()
        nova_process = NovaProcess(
            domains=["Technology"],
            model=largest_model,
            memory_manager=memory_manager,
            llm_service=llm_service
        )

        # Run a simple problem
        result = await nova_process.solve_problem(
            problem_statement="Explain the concept of microservices in one paragraph.",
            max_iterations=1,
            stream=False
        )

        # Check memory after processing
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        print(f"Final memory usage: {final_memory:.1f}MB")
        print(f"Memory increase: {memory_increase:.1f}MB")

        if memory_increase > 1000:  # More than 1GB increase
            print("⚠️  Significant memory increase detected")
        else:
            print("✅ Memory usage within reasonable limits")

    except Exception as e:
        print(f"❌ Memory test failed: {e}")

async def main():
    """Main test function."""
    print("🧠 NovaSystem Large Model Test Suite")
    print("=" * 60)
    print("This script tests NovaSystem with very large Ollama models (13GB+)")
    print("and verifies performance monitoring and caching functionality.")

    # Check if Ollama is available
    try:
        llm_service = LLMService()
        available_models = llm_service.get_available_models()

        if not available_models:
            print("❌ No Ollama models available. Please ensure Ollama is running.")
            return

        print(f"✅ Found {len(available_models)} available models:")
        for model in available_models:
            print(f"  - {model}")

    except Exception as e:
        print(f"❌ Failed to connect to Ollama: {e}")
        return

    # Test 1: Model loading performance
    await test_model_loading_performance()

    # Test 2: Memory usage
    await test_memory_usage()

    # Test 3: Full Nova Process with large model
    large_models = [m for m in available_models if "gpt-oss" in m or "20b" in m]
    if large_models:
        await test_large_model(large_models[0])
    else:
        print("\n⚠️  No large models (13GB+) available for full testing")
        # Test with largest available model
        if available_models:
            await test_large_model(available_models[0])

    # Final cache and metrics summary
    print(f"\n📊 Final System Status")
    print("=" * 60)

    cache = get_model_cache()
    cache_stats = cache.get_cache_stats()
    print(f"Cache Hit Rate: {cache_stats['hit_rate_percent']:.1f}%")
    print(f"Models Cached: {cache_stats['cache_size']}")
    print(f"Cache Memory: {cache_stats['total_memory_mb']:.1f}MB")

    metrics_collector = get_metrics_collector()
    summary = metrics_collector.get_performance_summary()
    if 'total_sessions' in summary:
        print(f"Total Sessions: {summary['total_sessions']}")
        print(f"Average Response Time: {summary['average_llm_response_time']:.2f}s")

    print("\n✅ Large model testing completed!")

if __name__ == "__main__":
    asyncio.run(main())
