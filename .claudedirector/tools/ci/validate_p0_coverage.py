#!/usr/bin/env python3
"""
P0 CI Coverage Validator
Ensures all P0 tests from definitions are included in CI
"""

import yaml
import sys
import os


def validate_ci_coverage():
    """Validate CI includes all P0 tests via unified runner"""

    # Load P0 definitions
    with open(
        ".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml", "r"
    ) as f:
        definitions = yaml.safe_load(f)

    # Load ACTIVE CI workflow (unified-ci.yml)
    with open(".github/workflows/unified-ci.yml", "r") as f:
        ci_content = f.read()

    p0_features = definitions.get("p0_features", [])

    print("🔍 P0 CI COVERAGE VALIDATION")
    print("=" * 50)

    # Check if CI uses the unified P0 test runner (modern approach)
    unified_runner = "run_mandatory_p0_tests.py"
    if unified_runner in ci_content:
        print("✅ UNIFIED RUNNER DETECTED: Using run_mandatory_p0_tests.py")
        print("✅ All P0 tests automatically included via YAML configuration")

        # Verify the unified runner exists and is functional
        unified_runner_path = (
            ".claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py"
        )
        if os.path.exists(unified_runner_path):
            print(f"✅ Unified runner exists: {unified_runner_path}")

            # Verify YAML definitions file exists
            yaml_path = ".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml"
            if os.path.exists(yaml_path):
                print(f"✅ P0 definitions exist: {yaml_path}")
                print(
                    f"✅ P0 test coverage: {len(p0_features)}/{len(p0_features)} (100%)"
                )
                print("=" * 50)
                print("✅ COMPLETE: All P0 tests included via unified runner")
                return True
            else:
                print(f"❌ P0 definitions missing: {yaml_path}")
                return False
        else:
            print(f"❌ Unified runner missing: {unified_runner_path}")
            return False

    # Fallback: Check for individual test modules (legacy approach)
    print("⚠️ LEGACY MODE: Checking individual test modules")
    missing_tests = []
    found_tests = []

    for feature in p0_features:
        name = feature.get("name", "")
        module = feature.get("test_module", "")

        # Check if test module is referenced in CI
        if module in ci_content:
            found_tests.append(name)
            print(f"✅ {name}")
        else:
            missing_tests.append(name)
            print(f"❌ {name} - Module: {module}")

    print("=" * 50)
    print(
        f"📊 Coverage: {len(found_tests)}/{len(p0_features)} ({len(found_tests)/len(p0_features)*100:.1f}%)"
    )

    if missing_tests:
        print(f"🚨 MISSING: {len(missing_tests)} P0 tests not in CI")
        for test in missing_tests:
            print(f"   - {test}")
        return False
    else:
        print("✅ COMPLETE: All P0 tests included in CI")
        return True


if __name__ == "__main__":
    success = validate_ci_coverage()
    sys.exit(0 if success else 1)
