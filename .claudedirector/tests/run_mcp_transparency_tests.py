#!/usr/bin/env python3
"""
Unified Test Runner for MCP Transparency P0 Feature
CRITICAL: Validates that MCP transparency disclosure never regresses

This script runs comprehensive tests to ensure the P0 MCP transparency
feature works correctly in all scenarios and integration points.
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add test paths - robust for different execution contexts
test_dir = Path(__file__).parent
claudedirector_root = test_dir.parent  # .claudedirector directory
lib_path = claudedirector_root / "lib"

# Add all necessary paths
sys.path.insert(0, str(test_dir / "regression"))
sys.path.insert(0, str(test_dir / "integration"))
# Use absolute path for lib to ensure imports work in all contexts
sys.path.insert(0, str(lib_path.resolve()))


def run_test_module(module_path, description):
    """Run a test module and return results"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print("=" * 60)

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, str(module_path)],
            capture_output=True,
            text=True,
            cwd=test_dir.parent.parent,
        )

        end_time = time.time()
        duration = end_time - start_time

        success = result.returncode == 0

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"\n{status} - {description} ({duration:.2f}s)")

        return {
            "name": description,
            "success": success,
            "duration": duration,
            "output": result.stdout,
            "error": result.stderr,
        }

    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time

        print(f"❌ FAILED - {description} ({duration:.2f}s)")
        print(f"Exception: {e}")

        return {
            "name": description,
            "success": False,
            "duration": duration,
            "output": "",
            "error": str(e),
        }


def run_quick_validation():
    """Run quick validation of core functionality"""
    print("🚀 Quick MCP Transparency Validation")
    print("-" * 40)

    try:
        from cursor_transparency_bridge import (
            ensure_transparency_compliance,
            get_transparency_summary,
        )

        # Test basic functionality
        test_input = "How should we develop strategic organizational framework for complex assessment?"
        test_response = (
            "Strategic analysis requires systematic framework application..."
        )

        enhanced = ensure_transparency_compliance(test_response, test_input)
        summary = get_transparency_summary(test_response, test_input)

        # Validate core requirements
        checks = [
            (
                "MCP disclosure present",
                (
                    "🔧 Accessing MCP Server:" in enhanced
                    or "🔧 Installing MCP enhancement:" in enhanced
                ),
            ),
            ("Persona header present", summary["has_persona_header"]),
            ("MCP enhancement detected", summary["has_mcp_enhancement"]),
            ("Transparency applied", summary["transparency_applied"]),
        ]

        all_passed = True
        for check_name, check_result in checks:
            status = "✅" if check_result else "❌"
            print(f"  {status} {check_name}")
            if not check_result:
                all_passed = False

        if all_passed:
            print("  ✅ Core functionality working")
            return True
        else:
            print("  ❌ Core functionality broken")
            return False

    except Exception as e:
        print(f"  ❌ Quick validation failed: {e}")
        return False


def main():
    """Run comprehensive MCP transparency test suite"""
    print("🔍 MCP TRANSPARENCY COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("CRITICAL P0 FEATURE: MCP server transparency disclosure")
    print("This test suite ensures the feature never regresses.")
    print("=" * 60)

    # Start with quick validation
    quick_validation_success = run_quick_validation()

    if not quick_validation_success:
        print("\n❌ CRITICAL: Quick validation failed!")
        print("   Core MCP transparency functionality is broken.")
        print("   Skipping comprehensive tests.")
        return False

    # Define test modules to run
    test_modules = [
        {
            "path": test_dir / "regression" / "test_mcp_transparency_p0.py",
            "description": "P0 Regression Tests - Core MCP transparency functionality",
        },
        {
            "path": test_dir / "integration" / "test_cursor_integration.py",
            "description": "Cursor Integration Tests - Live conversation flow",
        },
    ]

    # Run all test modules
    results = []
    total_start_time = time.time()

    for test_module in test_modules:
        if test_module["path"].exists():
            result = run_test_module(test_module["path"], test_module["description"])
            results.append(result)
        else:
            print(f"⚠️ Test module not found: {test_module['path']}")
            results.append(
                {
                    "name": test_module["description"],
                    "success": False,
                    "duration": 0,
                    "output": "",
                    "error": f"Test file not found: {test_module['path']}",
                }
            )

    total_end_time = time.time()
    total_duration = total_end_time - total_start_time

    # Generate summary report
    print(f"\n{'='*60}")
    print("📊 TEST SUITE SUMMARY")
    print("=" * 60)

    passed_tests = [r for r in results if r["success"]]
    failed_tests = [r for r in results if not r["success"]]

    print(f"Total Tests: {len(results)}")
    print(f"Passed: {len(passed_tests)}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Total Duration: {total_duration:.2f}s")

    if failed_tests:
        print(f"\n❌ FAILED TESTS:")
        for test in failed_tests:
            print(f"  • {test['name']} ({test['duration']:.2f}s)")
            if test["error"]:
                print(f"    Error: {test['error']}")

    if passed_tests:
        print(f"\n✅ PASSED TESTS:")
        for test in passed_tests:
            print(f"  • {test['name']} ({test['duration']:.2f}s)")

    # Final verdict
    all_passed = len(failed_tests) == 0

    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL TESTS PASSED - MCP TRANSPARENCY IS BULLETPROOF")
        print("   P0 feature is protected against regression")
        print("   Safe to deploy to production")
    else:
        print("🚨 TESTS FAILED - MCP TRANSPARENCY NEEDS FIXES")
        print("   P0 feature has critical issues")
        print("   DO NOT DEPLOY until all tests pass")
    print("=" * 60)

    return all_passed


def run_continuous_monitoring():
    """Run in continuous monitoring mode for development"""
    print("🔄 Continuous MCP Transparency Monitoring")
    print("Press Ctrl+C to stop")
    print("-" * 40)

    try:
        while True:
            success = run_quick_validation()
            if success:
                print("  ✅ Monitoring: All systems operational")
            else:
                print("  ❌ Monitoring: Issues detected!")

            time.sleep(5)  # Check every 5 seconds

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        run_continuous_monitoring()
    else:
        success = main()
        sys.exit(0 if success else 1)
