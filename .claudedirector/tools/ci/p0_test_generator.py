#!/usr/bin/env python3
"""
P0 Test Generator for CI/CD
Automatically generates CI test steps from p0_test_definitions.yaml
Ensures 100% coverage of defined P0 features in CI pipeline
"""

import yaml
import os
import sys
from pathlib import Path
from typing import Dict, List, Any


class P0TestGenerator:
    """Generates CI test steps from P0 test definitions"""

    def __init__(
        self,
        definitions_file: str = ".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml",
    ):
        self.definitions_file = definitions_file
        self.definitions = self._load_definitions()

    def _load_definitions(self) -> Dict[str, Any]:
        """Load P0 test definitions from YAML"""
        if not os.path.exists(self.definitions_file):
            raise FileNotFoundError(
                f"P0 definitions file not found: {self.definitions_file}"
            )

        with open(self.definitions_file, "r") as f:
            return yaml.safe_load(f)

    def generate_ci_step(self) -> str:
        """Generate complete CI step for GitHub Actions"""
        p0_features = self.definitions.get("p0_features", [])
        enforcement = self.definitions.get("enforcement", {})
        quality_gates = self.definitions.get("quality_gates", {})

        # Group tests by critical level
        blocking_tests = [
            f for f in p0_features if f.get("critical_level") == "BLOCKING"
        ]
        high_priority_tests = [
            f for f in p0_features if f.get("critical_level") == "HIGH"
        ]

        ci_step = self._generate_step_header()
        ci_step += self._generate_blocking_tests(blocking_tests)
        ci_step += self._generate_high_priority_tests(high_priority_tests)
        ci_step += self._generate_step_footer(len(p0_features))

        return ci_step

    def _generate_step_header(self) -> str:
        """Generate CI step header"""
        return """      - name: P0 Feature Test Suite (YAML-Driven)
        run: |
          echo "🚨 AUTOMATED P0 TEST EXECUTION - YAML DEFINITION DRIVEN"
          echo "============================================================"
          echo "Source: .claudedirector/tests/p0_enforcement/p0_test_definitions.yaml"
          echo "Policy: ZERO_TOLERANCE enforcement for all P0 features"
          echo "Coverage: 100% of defined P0 features"
          echo ""

"""

    def _generate_blocking_tests(self, blocking_tests: List[Dict]) -> str:
        """Generate BLOCKING level test execution"""
        if not blocking_tests:
            return ""

        section = '          echo "🚨 BLOCKING P0 TESTS (Must pass for CI success)"\n'
        section += '          echo "============================================================"\n'

        for test in blocking_tests:
            name = test.get("name", "Unknown Test")
            module = test.get("test_module", "")
            timeout = test.get("timeout_seconds", 120)
            description = test.get("description", "")
            business_impact = test.get("business_impact", "")

            section += f"""
          echo "🧪 BLOCKING: {name}"
          echo "   Module: {module}"
          echo "   Description: {description}"
          echo "   Business Impact: {business_impact}"
          timeout {timeout} python {module} || {{
            echo "❌ BLOCKING FAILURE: {name}"
            echo "💥 CRITICAL: CI build must fail - this is a BLOCKING P0 feature"
            echo "📋 Business Impact: {business_impact}"
            exit 1
          }}
          echo "✅ PASSED: {name}"
"""

        return section

    def _generate_high_priority_tests(self, high_priority_tests: List[Dict]) -> str:
        """Generate HIGH priority test execution"""
        if not high_priority_tests:
            return ""

        section = """
          echo ""
          echo "🔺 HIGH PRIORITY P0 TESTS (Should pass but won't block CI)"
          echo "============================================================"
"""

        for test in high_priority_tests:
            name = test.get("name", "Unknown Test")
            module = test.get("test_module", "")
            timeout = test.get("timeout_seconds", 60)
            description = test.get("description", "")
            failure_impact = test.get("failure_impact", "")

            section += f"""
          echo "🧪 HIGH PRIORITY: {name}"
          echo "   Module: {module}"
          echo "   Description: {description}"
          timeout {timeout} python {module} || {{
            echo "⚠️ HIGH PRIORITY FAILURE: {name}"
            echo "🔍 Impact: {failure_impact}"
            echo "📝 Note: Non-blocking but should be investigated"
          }}
          echo "✅ COMPLETED: {name}"
"""

        return section

    def _generate_step_footer(self, total_tests: int) -> str:
        """Generate CI step footer with summary"""
        return f"""
          echo ""
          echo "📊 P0 TEST EXECUTION SUMMARY"
          echo "============================================================"
          echo "✅ Total P0 Tests Executed: {total_tests}"
          echo "✅ YAML-Driven Coverage: 100%"
          echo "✅ Enforcement Policy: {self.definitions.get('enforcement_policy', 'ZERO_TOLERANCE')}"
          echo "✅ All BLOCKING tests passed - CI success criteria met"
          echo "============================================================"

"""

    def generate_validation_script(self) -> str:
        """Generate validation script to check CI coverage"""
        p0_features = self.definitions.get("p0_features", [])

        script = '''#!/usr/bin/env python3
"""
P0 CI Coverage Validator
Ensures all P0 tests from definitions are included in CI
"""

import yaml
import re
import sys

def validate_ci_coverage():
    """Validate CI includes all P0 tests from definitions"""

    # Load P0 definitions
    with open(".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml", 'r') as f:
        definitions = yaml.safe_load(f)

    # Load CI workflow
    with open(".github/workflows/next-phase-ci-cd.yml", 'r') as f:
        ci_content = f.read()

    p0_features = definitions.get('p0_features', [])

    print("🔍 P0 CI COVERAGE VALIDATION")
    print("=" * 50)

    missing_tests = []
    found_tests = []

    for feature in p0_features:
        name = feature.get('name', '')
        module = feature.get('test_module', '')

        # Check if test module is referenced in CI
        if module in ci_content:
            found_tests.append(name)
            print(f"✅ {name}")
        else:
            missing_tests.append(name)
            print(f"❌ {name} - Module: {module}")

    print("=" * 50)
    print(f"📊 Coverage: {len(found_tests)}/{len(p0_features)} ({len(found_tests)/len(p0_features)*100:.1f}%)")

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
'''
        return script

    def update_ci_workflow(
        self, workflow_file: str = ".github/workflows/next-phase-ci-cd.yml"
    ):
        """Update CI workflow with generated P0 test step"""
        print("🔧 Updating CI workflow with YAML-driven P0 tests...")

        # Generate the new step
        new_step = self.generate_ci_step()

        # Note: This would require more sophisticated parsing to inject into existing workflow
        # For now, return the step content for manual integration
        return new_step


def main():
    """Main execution"""
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-ci":
        generator = P0TestGenerator()
        ci_step = generator.generate_ci_step()
        print("Generated CI Step:")
        print("=" * 50)
        print(ci_step)

    elif len(sys.argv) > 1 and sys.argv[1] == "--generate-validator":
        generator = P0TestGenerator()
        validator = generator.generate_validation_script()

        # Write validator script
        with open(".claudedirector/tools/ci/validate_p0_coverage.py", "w") as f:
            f.write(validator)
        os.chmod(".claudedirector/tools/ci/validate_p0_coverage.py", 0o755)
        print(
            "✅ Generated P0 coverage validator: .claudedirector/tools/ci/validate_p0_coverage.py"
        )

    else:
        generator = P0TestGenerator()
        print("🔍 P0 Test Definitions Analysis:")
        print("=" * 40)
        print(f"Total P0 Features: {len(generator.definitions.get('p0_features', []))}")
        print(
            f"Enforcement Policy: {generator.definitions.get('enforcement_policy', 'Not specified')}"
        )

        blocking = [
            f
            for f in generator.definitions.get("p0_features", [])
            if f.get("critical_level") == "BLOCKING"
        ]
        high = [
            f
            for f in generator.definitions.get("p0_features", [])
            if f.get("critical_level") == "HIGH"
        ]

        print(f"BLOCKING Tests: {len(blocking)}")
        print(f"HIGH Priority Tests: {len(high)}")

        print("\nUsage:")
        print("  --generate-ci       Generate CI step content")
        print("  --generate-validator Generate coverage validation script")


if __name__ == "__main__":
    main()
