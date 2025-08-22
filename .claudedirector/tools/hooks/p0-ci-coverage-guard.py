#!/usr/bin/env python3
"""
P0 CI Coverage Guard
Pre-commit hook to ensure P0 test coverage never regresses in CI
Prevents commits that would break P0 CI coverage
"""

import sys
import os
import subprocess


def main():
    """Main execution - validate P0 CI coverage"""
    print("🛡️ P0 CI COVERAGE GUARD")
    print("=" * 40)
    print("Ensuring all P0 tests remain in CI pipeline...")

    # Check if the validator exists
    validator_path = ".claudedirector/tools/ci/validate_p0_coverage.py"
    if not os.path.exists(validator_path):
        print(f"⚠️ P0 coverage validator not found: {validator_path}")
        print("✅ Skipping P0 coverage validation")
        return 0

    # Run the P0 coverage validator
    try:
        result = subprocess.run(
            ["python3", validator_path], capture_output=True, text=True, timeout=30
        )

        if result.returncode == 0:
            print("✅ P0 CI coverage validation: PASSED")
            print("✅ All P0 tests properly included in CI")
            return 0
        else:
            print("❌ P0 CI coverage validation: FAILED")
            print(result.stdout)
            print(result.stderr)
            print("")
            print("🚨 COMMIT BLOCKED: P0 CI coverage regression detected")
            print("🔧 Fix: Ensure all P0 tests from p0_test_definitions.yaml are in CI")
            return 1

    except subprocess.TimeoutExpired:
        print("❌ P0 coverage validation timed out")
        return 1
    except Exception as e:
        print(f"❌ Error running P0 coverage validation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
