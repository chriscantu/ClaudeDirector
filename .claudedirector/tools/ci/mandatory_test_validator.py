#!/usr/bin/env python3
"""
Mandatory Test Validator
Enforces P0 test policy: tests must never be disabled, skipped, or removed.
Integrates with pre-commit hooks and CI pipeline.
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path

# Add the project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def detect_python_environment():
    """Detect Python interpreter path for both local venv and CI environments."""

    # Local development with virtual environment
    venv_python = PROJECT_ROOT / "venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)

    # CI or system Python
    try:
        result = subprocess.run(["which", "python3"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    # Fallback to system python3
    return "python3"

def run_critical_tests():
    """Run mandatory P0 tests with proper environment detection."""

    print("🛡️ MANDATORY TEST VALIDATION - Starting")

    # Detect Python interpreter
    python_path = detect_python_environment()
    print(f"🐍 Using Python: {python_path}")

    # Path to P0 test runner
    p0_runner = PROJECT_ROOT / ".claudedirector" / "tests" / "p0_enforcement" / "run_mandatory_p0_tests.py"

    if not p0_runner.exists():
        print(f"❌ P0 test runner not found: {p0_runner}")
        return False

    print(f"🏃 Running P0 tests: {p0_runner}")

    try:
        # Run P0 tests with proper environment
        result = subprocess.run(
            [python_path, str(p0_runner)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        print("📤 P0 Test Output:")
        print(result.stdout)

        if result.stderr:
            print("⚠️ P0 Test Warnings:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ All mandatory P0 tests passed")
            return True
        else:
            print(f"❌ P0 tests failed with exit code: {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ P0 tests timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running P0 tests: {e}")
        return False

def main():
    """Main entry point for mandatory test validation."""

    print("=" * 60)
    print("🛡️ MANDATORY TEST VALIDATION")
    print("=" * 60)

    success = run_critical_tests()

    if success:
        print("✅ MANDATORY TEST VALIDATION PASSED")
        sys.exit(0)
    else:
        print("❌ MANDATORY TEST VALIDATION FAILED")
        print("🚨 Commit blocked due to P0 test failures")
        sys.exit(1)

if __name__ == "__main__":
    main()
