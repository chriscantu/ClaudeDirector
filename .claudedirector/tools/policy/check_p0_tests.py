#!/usr/bin/env python3
"""
P0 Test Protection Policy Enforcement
Ensures P0 tests are never disabled, skipped, or removed without proper approval.
"""

import sys
import os
import re
from pathlib import Path
from typing import List, Tuple


class P0TestProtector:
    """Protects P0 tests from being disabled or removed."""

    def __init__(self):
        self.p0_test_patterns = [
            r"test.*p0.*\.py$",
            r".*_p0_.*\.py$",
            r".*p0_test.*\.py$",
        ]

        self.dangerous_patterns = [
            (r"@pytest\.mark\.skip", "P0 test marked as skipped"),
            (r"@unittest\.skip", "P0 test marked as skipped"),
            (r"pytest\.skip\(", "P0 test contains skip call"),
            (r"self\.skipTest\(", "P0 test contains skipTest call"),
            (r"return\s*#.*skip", "P0 test returns early (potential skip)"),
            (r"pass\s*#.*skip", "P0 test contains pass statement (potential skip)"),
            (r"# TODO.*skip", "P0 test has skip TODO"),
            (r"# FIXME.*skip", "P0 test has skip FIXME"),
        ]

        self.required_p0_tests = [
            "test_hybrid_installation_p0.py",
            "test_mcp_transparency_p0.py",
            "test_conversation_tracking_p0.py",
            "test_p0_quality_target.py",
        ]

    def is_p0_test_file(self, file_path: Path) -> bool:
        """Check if file is a P0 test file."""
        filename = file_path.name.lower()

        for pattern in self.p0_test_patterns:
            if re.search(pattern, filename):
                return True

        return False

    def check_p0_test_integrity(self, file_path: Path) -> List[str]:
        """Check P0 test file for integrity violations."""
        violations = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for dangerous patterns
            for pattern, description in self.dangerous_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    line_num = content[: match.start()].count("\n") + 1
                    violations.append(f"Line {line_num}: {description}")

            # Check for test method presence
            test_methods = re.findall(r"def (test_\w+)", content)
            if not test_methods:
                violations.append("No test methods found in P0 test file")

            # Check for assertions
            assertion_patterns = [
                r"assert\s+",
                r"self\.assert",
                r"self\.assertEqual",
                r"self\.assertTrue",
            ]
            has_assertions = any(
                re.search(pattern, content) for pattern in assertion_patterns
            )
            if not has_assertions:
                violations.append("No assertions found in P0 test file")

        except Exception as e:
            violations.append(f"Error reading file: {e}")

        return violations

    def check_required_p0_tests_exist(self) -> List[str]:
        """Check that all required P0 tests exist."""
        missing_tests = []

        for required_test in self.required_p0_tests:
            test_found = False

            # Search in common test directories
            search_paths = [
                Path(".claudedirector/tests"),
                Path("tests"),
                Path(".claudedirector/tests/regression"),
                Path(".claudedirector/tests/integration"),
            ]

            for search_path in search_paths:
                if search_path.exists():
                    for test_file in search_path.rglob(required_test):
                        test_found = True
                        break

            if not test_found:
                missing_tests.append(f"Required P0 test not found: {required_test}")

        return missing_tests


def main():
    """Main policy enforcement function."""
    if len(sys.argv) < 2:
        print("Usage: check_p0_tests.py <file1.py> [file2.py] ...")
        sys.exit(1)

    protector = P0TestProtector()
    total_violations = []
    total_files = 0

    # Check individual files passed as arguments
    for file_arg in sys.argv[1:]:
        file_path = Path(file_arg)

        if not file_path.exists() or not file_path.suffix == ".py":
            continue

        if protector.is_p0_test_file(file_path):
            total_files += 1
            violations = protector.check_p0_test_integrity(file_path)

            if violations:
                total_violations.append((file_path, violations))

    # Check for missing required P0 tests
    missing_tests = protector.check_required_p0_tests_exist()
    if missing_tests:
        total_violations.append(("SYSTEM", missing_tests))

    # Report results
    if total_violations:
        print("🚨 P0 TEST PROTECTION VIOLATIONS DETECTED")
        print("=" * 60)
        print("Policy: P0 tests must never be disabled, skipped, or removed")
        print()

        for identifier, violations in total_violations:
            if identifier == "SYSTEM":
                print("❌ SYSTEM VIOLATIONS:")
                for violation in violations:
                    print(f"   • {violation}")
            else:
                print(f"❌ {identifier}")
                for violation in violations:
                    print(f"   • {violation}")
            print()

        print("💡 REMEDIATION REQUIRED:")
        print("- Remove @pytest.mark.skip and @unittest.skip decorators from P0 tests")
        print("- Remove pytest.skip() and self.skipTest() calls from P0 tests")
        print("- Fix P0 test logic instead of skipping tests")
        print("- Ensure all required P0 tests exist and are executable")
        print("- See docs/DEVELOPMENT_POLICY.md for P0 test requirements")
        print()
        print("🛡️ COMMIT BLOCKED: Fix P0 test violations before proceeding")
        sys.exit(1)
    else:
        if total_files > 0:
            print(
                f"✅ P0 Test Protection: All {total_files} P0 test files are properly protected"
            )
        else:
            print("✅ P0 Test Protection: No P0 test files in this commit")
        sys.exit(0)


if __name__ == "__main__":
    main()
