#!/usr/bin/env python3
"""
MANDATORY Test Validator for ClaudeDirector
===========================================

This script runs critical tests before any commit and PREVENTS commits
if any tests fail. This enforces the MANDATORY RULE: All features must
have passing tests before commit.

Usage:
    python mandatory_test_validator.py

Exit Codes:
    0: All tests passed
    1: Critical tests failed (BLOCKS COMMIT)
    2: Test setup/environment issues
"""

import sys
import subprocess
import os
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )

        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            if result.stdout.strip():
                print("Output:", result.stdout.strip())
            return True
        else:
            print(f"❌ {description} - FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def check_environment():
    """Verify test environment is set up correctly."""
    print("\n🔧 Checking test environment...")

    # Check virtual environment
    venv_python = PROJECT_ROOT / "venv" / "bin" / "python"
    if not venv_python.exists():
        print("❌ Virtual environment not found at venv/bin/python")
        return False

    # Check ClaudeDirector installation
    check_cmd = f'{venv_python} -c "import claudedirector; print(\\"ClaudeDirector import: OK\\")"'
    if not run_command(check_cmd, "ClaudeDirector Import Check"):
        print("❌ ClaudeDirector not properly installed")
        return False

    print("✅ Test environment ready")
    return True

def run_critical_tests():
    """Run the critical tests that must pass."""
    print("\n🎯 Running CRITICAL tests (MUST PASS for commit)...")

    venv_python = PROJECT_ROOT / "venv" / "bin" / "python"

    # Test 1: Rumelt & WRAP Framework Integration Tests
    test_cmd = f"{venv_python} -m pytest .claudedirector/tests/integration/test_rumelt_wrap_frameworks.py -v --tb=short"
    if not run_command(test_cmd, "Rumelt & WRAP Framework Integration Tests"):
        print("\n❌ CRITICAL FAILURE: Strategic framework tests failed!")
        print("🚫 These tests validate the core embedded strategic intelligence.")
        print("🚫 COMMIT BLOCKED - Fix failing tests before committing.")
        return False

    # Test 2: Core embedded framework engine tests (if they exist)
    core_tests = PROJECT_ROOT / ".claudedirector" / "tests" / "unit" / "test_embedded_framework_engine.py"
    if core_tests.exists():
        test_cmd = f"{venv_python} -m pytest {core_tests} -v --tb=short"
        if not run_command(test_cmd, "Embedded Framework Engine Unit Tests"):
            print("\n❌ CRITICAL FAILURE: Core framework engine tests failed!")
            return False

    # Test 3: Quick smoke test of complexity analyzer
    complexity_tests = PROJECT_ROOT / ".claudedirector" / "tests" / "unit" / "test_complexity_analyzer.py"
    if complexity_tests.exists():
        test_cmd = f"{venv_python} -m pytest {complexity_tests} -v --tb=short"
        if not run_command(test_cmd, "Complexity Analyzer Unit Tests"):
            print("\n❌ CRITICAL FAILURE: Complexity analyzer tests failed!")
            return False

    print("\n✅ ALL CRITICAL TESTS PASSED!")
    return True

def run_quick_smoke_tests():
    """Run quick smoke tests to catch obvious issues."""
    print("\n🚀 Running quick smoke tests...")

    venv_python = PROJECT_ROOT / "venv" / "bin" / "python"

    # Basic import test
    import_cmd = f'{venv_python} -c "from claudedirector.core.embedded_framework_engine import EmbeddedFrameworkEngine; print(\\"✅ Core imports working\\")"'
    if not run_command(import_cmd, "Core Module Import Test"):
        return False

    # Configuration loading test
    config_cmd = f'{venv_python} -c "import yaml; yaml.safe_load(open(\\".claudedirector/config/claude_config.yaml\\")); print(\\"✅ Config loading working\\")"'
    if not run_command(config_cmd, "Configuration Loading Test"):
        return False

    print("\n✅ Smoke tests passed!")
    return True

def main():
    """Main test validation function."""
    print("🛡️  MANDATORY TEST VALIDATOR")
    print("="*60)
    print("Enforcing: All features must have passing tests before commit")
    print("="*60)

    # Check environment
    if not check_environment():
        print("\n❌ ENVIRONMENT SETUP FAILED")
        print("🔧 Please ensure virtual environment is set up and ClaudeDirector is installed")
        return 2

    # Run smoke tests
    if not run_quick_smoke_tests():
        print("\n❌ SMOKE TESTS FAILED")
        print("🚫 COMMIT BLOCKED - Basic functionality is broken")
        return 1

    # Run critical tests
    if not run_critical_tests():
        print("\n❌ CRITICAL TESTS FAILED")
        print("🚫 COMMIT BLOCKED - Fix failing tests before committing")
        print("\nTo debug:")
        print("1. Run tests manually: ./venv/bin/python -m pytest .claudedirector/tests/integration/test_rumelt_wrap_frameworks.py -v")
        print("2. Fix any failing tests")
        print("3. Re-run this validator")
        return 1

    print("\n🎉 ALL TESTS PASSED!")
    print("✅ Commit allowed - code quality validated")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
