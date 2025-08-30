#!/usr/bin/env python3
"""
DEBUG: CI Import Issue Diagnostic
This file will help us understand why imports fail in CI but work locally
"""

import sys
import os
from pathlib import Path

print("🔍 CI IMPORT DIAGNOSTIC")
print("=" * 50)

# Show Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Show current working directory
print(f"Current working directory: {os.getcwd()}")

# Show PYTHONPATH
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'NOT SET')}")

# Show sys.path
print("\nPython sys.path:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

# Test our PROJECT_ROOT calculation
test_file = Path(__file__)
PROJECT_ROOT = (
    test_file.parent.parent.parent
)  # 3 levels up from .claudedirector/tests/debug_ci_import.py
print(f"\nPROJECT_ROOT calculation:")
print(f"  Test file: {test_file}")
print(f"  PROJECT_ROOT: {PROJECT_ROOT}")
print(f"  PROJECT_ROOT absolute: {PROJECT_ROOT.resolve()}")

# Check if lib directory exists
lib_path = PROJECT_ROOT / ".claudedirector" / "lib"
print(f"\nLib directory check:")
print(f"  Lib path: {lib_path}")
print(f"  Lib exists: {lib_path.exists()}")

if lib_path.exists():
    print(f"  Lib contents: {list(lib_path.iterdir())[:5]}...")  # First 5 items

# Check ai_intelligence directory
ai_intel_path = lib_path / "ai_intelligence"
print(f"\nAI Intelligence directory check:")
print(f"  AI Intel path: {ai_intel_path}")
print(f"  AI Intel exists: {ai_intel_path.exists()}")

if ai_intel_path.exists():
    print(
        f"  AI Intel contents: {list(ai_intel_path.iterdir())[:5]}..."
    )  # First 5 items

# Test import step by step
print("\n🧪 STEP-BY-STEP IMPORT TEST")
print("-" * 30)

# Add lib to path
sys.path.insert(0, str(lib_path))
print(f"Added to sys.path: {lib_path}")

try:
    import ai_intelligence

    print("✅ Step 1: import ai_intelligence - SUCCESS")
    print(f"   ai_intelligence.__file__: {ai_intelligence.__file__}")
except Exception as e:
    print(f"❌ Step 1: import ai_intelligence - FAILED: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

try:
    from ai_intelligence import decision_orchestrator

    print("✅ Step 2: from ai_intelligence import decision_orchestrator - SUCCESS")
except Exception as e:
    print(f"❌ Step 2: from ai_intelligence import decision_orchestrator - FAILED: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

try:
    from ai_intelligence.decision_orchestrator import DecisionIntelligenceOrchestrator

    print(
        "✅ Step 3: from ai_intelligence.decision_orchestrator import DecisionIntelligenceOrchestrator - SUCCESS"
    )
except Exception as e:
    print(f"❌ Step 3: DecisionIntelligenceOrchestrator import - FAILED: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

try:
    from ai_intelligence.mcp_decision_pipeline import MCPEnhancedDecisionPipeline

    print(
        "✅ Step 4: from ai_intelligence.mcp_decision_pipeline import MCPEnhancedDecisionPipeline - SUCCESS"
    )
except Exception as e:
    print(f"❌ Step 4: MCPEnhancedDecisionPipeline import - FAILED: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

print("\n🎉 ALL IMPORTS SUCCESSFUL!")
print("The import issue may be in the test file setup, not the modules themselves.")
