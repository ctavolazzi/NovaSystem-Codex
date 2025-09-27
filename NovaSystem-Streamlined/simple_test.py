#!/usr/bin/env python3
print("Testing NovaSystem imports...")

try:
    import novasystem
    print("✅ Main module imported")
except Exception as e:
    print(f"❌ Main module failed: {e}")

try:
    from novasystem.ui.web import WebInterface
    print("✅ Web interface imported")
except Exception as e:
    print(f"❌ Web interface failed: {e}")

try:
    from novasystem.ui.gradio import GradioInterface
    print("✅ Gradio interface imported")
except Exception as e:
    print(f"❌ Gradio interface failed: {e}")

print("Test complete!")
