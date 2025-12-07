#!/usr/bin/env python3
"""
Simple integration test for NovaSystem with all new features.

This script tests the complete system integration including:
- Performance monitoring
- Model caching
- Large model support
- CLI commands
"""

import asyncio
import sys
import os
import time
import logging
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("🔍 Testing imports...")

    try:
        from novasystem.core.process import NovaProcess
        from novasystem.core.memory import MemoryManager
        from novasystem.utils.llm_service import LLMService
        from novasystem.utils.metrics import get_metrics_collector
        from novasystem.utils.model_cache import get_model_cache
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_llm_service():
    """Test LLM service initialization."""
    print("\n🤖 Testing LLM Service...")

    try:
        llm_service = LLMService()
        models = llm_service.get_available_models()
        print(f"✅ LLM Service initialized with {len(models)} models")

        if models:
            print("Available models:")
            for model in models:
                print(f"  - {model}")

        return True
    except Exception as e:
        print(f"❌ LLM Service test failed: {e}")
        return False

def test_metrics_system():
    """Test metrics collection system."""
    print("\n📊 Testing Metrics System...")

    try:
        metrics_collector = get_metrics_collector()

        # Test session creation
        session_id = "test_session_123"
        metrics_collector.start_session(session_id)

        # Simulate some metrics
        metrics_collector.record_llm_call("ollama:phi3", 1.5, 100, 200)
        metrics_collector.record_iteration()
        metrics_collector.record_memory_usage()

        # End session
        metrics = metrics_collector.end_session(session_id)

        if metrics:
            print(f"✅ Metrics system working - recorded {metrics.total_time:.2f}s session")
            return True
        else:
            print("❌ No metrics recorded")
            return False

    except Exception as e:
        print(f"❌ Metrics test failed: {e}")
        return False

def test_model_cache():
    """Test model caching system."""
    print("\n🗄️  Testing Model Cache...")

    try:
        cache = get_model_cache()

        # Test cache operations
        cache.put_model("test_model", "ollama", 2.0, 1000.0)
        entry = cache.get_model("test_model", "ollama")

        if entry and entry.model_name == "test_model":
            print("✅ Model cache working")

            # Test cache stats
            stats = cache.get_cache_stats()
            print(f"  Cache size: {stats['cache_size']}")
            print(f"  Hit rate: {stats['hit_rate_percent']:.1f}%")

            return True
        else:
            print("❌ Cache entry not found")
            return False

    except Exception as e:
        print(f"❌ Model cache test failed: {e}")
        return False

async def test_nova_process():
    """Test Nova Process with metrics and caching."""
    print("\n🧠 Testing Nova Process...")

    try:
        # Create Nova Process
        memory_manager = MemoryManager()
        nova_process = NovaProcess(
            domains=["Technology", "Testing"],
            model="ollama:phi3",  # Use fast model for testing
            memory_manager=memory_manager
        )

        print(f"✅ Nova Process created with model: {nova_process.model}")

        # Test status
        status = nova_process.get_status()
        print(f"  Status: {status}")

        # Test metrics methods
        metrics = nova_process.get_performance_metrics()
        print(f"  Performance metrics available: {bool(metrics)}")

        system_metrics = nova_process.get_system_metrics()
        print(f"  System metrics available: {bool(system_metrics)}")

        return True

    except Exception as e:
        print(f"❌ Nova Process test failed: {e}")
        return False

def test_cli_commands():
    """Test CLI command availability."""
    print("\n💻 Testing CLI Commands...")

    try:
        from novasystem.cli import create_parser

        parser = create_parser()
        subcommands = [action.dest for action in parser._actions if hasattr(action, 'dest') and action.dest == 'command']

        # Check for expected commands
        expected_commands = ['solve', 'interactive', 'list-models', 'model-info', 'metrics', 'cache']

        print("Available CLI commands:")
        for subparser in parser._subparsers._actions:
            if hasattr(subparser, 'choices'):
                for cmd_name, cmd_parser in subparser.choices.items():
                    print(f"  - {cmd_name}: {cmd_parser.description}")

        # Check if all expected commands exist
        available_commands = []
        for subparser in parser._subparsers._actions:
            if hasattr(subparser, 'choices'):
                available_commands.extend(subparser.choices.keys())

        missing_commands = set(expected_commands) - set(available_commands)
        if missing_commands:
            print(f"⚠️  Missing commands: {missing_commands}")
            return False
        else:
            print("✅ All expected CLI commands available")
            return True

    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 NovaSystem Integration Test Suite")
    print("=" * 60)
    print("Testing all new features and system integration")

    tests = [
        ("Imports", test_imports),
        ("LLM Service", test_llm_service),
        ("Metrics System", test_metrics_system),
        ("Model Cache", test_model_cache),
        ("Nova Process", test_nova_process),
        ("CLI Commands", test_cli_commands),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False

    # Summary
    print(f"\n📊 Test Results Summary")
    print("=" * 60)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! System is ready for large model testing.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
