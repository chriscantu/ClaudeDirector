#!/usr/bin/env python3
"""
P0 CI Coverage Validator
Ensures all P0 tests from definitions are included in CI
"""

import yaml
import sys


def validate_ci_coverage():
    """Validate CI includes all P0 tests from definitions"""

    # Load P0 definitions
    with open(
        ".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml", "r"
    ) as f:
        definitions = yaml.safe_load(f)

    # Load CI workflow
    with open(".github/workflows/next-phase-ci-cd.yml", "r") as f:
        ci_content = f.read()

    p0_features = definitions.get("p0_features", [])

    print("🔍 P0 CI COVERAGE VALIDATION")
    print("=" * 50)

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
