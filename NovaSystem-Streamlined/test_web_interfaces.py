#!/usr/bin/env python3
"""
Test script for NovaSystem web interfaces.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all web interface modules can be imported."""
    print("Testing imports...")

    try:
        from novasystem.ui.web import WebInterface
        print("✅ Web interface imports successfully")
    except Exception as e:
        print(f"❌ Web interface import failed: {e}")
        return False

    try:
        from novasystem.ui.gradio import GradioInterface
        print("✅ Gradio interface imports successfully")
    except Exception as e:
        print(f"❌ Gradio interface import failed: {e}")
        return False

    return True

def test_web_interface():
    """Test web interface creation."""
    print("\nTesting web interface creation...")

    try:
        from novasystem.ui.web import WebInterface
        interface = WebInterface()
        print("✅ Web interface created successfully")

        # Test that routes are set up
        routes = [rule.rule for rule in interface.app.url_map.iter_rules()]
        print(f"✅ Routes configured: {routes}")

        return True
    except Exception as e:
        print(f"❌ Web interface creation failed: {e}")
        return False

def test_gradio_interface():
    """Test Gradio interface creation."""
    print("\nTesting Gradio interface creation...")

    try:
        from novasystem.ui.gradio import GradioInterface
        interface = GradioInterface()
        print("✅ Gradio interface created successfully")

        return True
    except Exception as e:
        print(f"❌ Gradio interface creation failed: {e}")
        return False

def test_core_functionality():
    """Test that core NovaSystem functionality works."""
    print("\nTesting core functionality...")

    try:
        from novasystem.core.process import NovaProcess
        from novasystem.core.memory import MemoryManager

        # Create a simple process
        memory_manager = MemoryManager()
        process = NovaProcess(domains=["Test"], memory_manager=memory_manager)

        print(f"✅ NovaProcess created with model: {process.model}")
        print(f"✅ Domains: {process.domains}")

        return True
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧠 NovaSystem Web Interface Test Suite")
    print("=" * 50)

    tests = [
        test_imports,
        test_core_functionality,
        test_web_interface,
        test_gradio_interface,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Web interfaces are ready.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
