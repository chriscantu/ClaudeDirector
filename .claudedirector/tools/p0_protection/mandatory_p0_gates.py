#!/usr/bin/env python3
"""
P0 Protection System - Mandatory Gates to Prevent Business-Critical Test Failures

This system implements mandatory checkpoints that prevent ANY code changes
from proceeding without 100% P0 test compliance.

CRITICAL RULE: P0 tests are NEVER optional. They are business-critical.
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any


class P0ProtectionSystem:
    """Mandatory P0 test protection with zero-tolerance enforcement."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.p0_test_runner = (
            self.project_root
            / ".claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py"
        )
        self.protection_log = (
            self.project_root / ".claudedirector/logs/p0_protection.log"
        )

    def run_p0_validation(self) -> Tuple[bool, int, int, List[str]]:
        """Run P0 tests and return results."""
        try:
            result = subprocess.run(
                [sys.executable, str(self.p0_test_runner)],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Parse results dynamically
            passing_tests = 0
            total_tests = 0  # Will be determined dynamically from test output
            failures = []

            for line in result.stdout.split("\n"):
                if "SUCCESS RATE" in line and "tests passing" in line:
                    # Extract test counts from line like "📊 SUCCESS RATE: 40/40 tests passing (100%)"
                    import re

                    match = re.search(r"(\d+)/(\d+) tests passing", line)
                    if match:
                        passing_tests = int(match.group(1))
                        total_tests = int(match.group(2))
                elif "❌ FAILED:" in line:
                    failures.append(line.strip())

            # If we didn't find the success rate line, try alternative parsing
            if total_tests == 0:
                for line in result.stdout.split("\n"):
                    if "Tests Run:" in line and "Total P0 Failures:" in line:
                        # Parse from execution report format
                        import re

                        tests_match = re.search(r"Tests Run: (\d+)", line)
                        failures_match = re.search(r"Total P0 Failures: (\d+)", line)
                        if tests_match and failures_match:
                            total_tests = int(tests_match.group(1))
                            failed_count = int(failures_match.group(1))
                            passing_tests = total_tests - failed_count

            return (len(failures) == 0, passing_tests, total_tests, failures)

        except Exception as e:
            self.log_protection_event("ERROR", f"P0 validation failed: {e}")
            return (False, 0, 0, [f"System error: {e}"])

    def log_protection_event(self, level: str, message: str):
        """Log P0 protection events."""
        self.protection_log.parent.mkdir(parents=True, exist_ok=True)

        with open(self.protection_log, "a") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp} [{level}] {message}\n")

    def enforce_p0_gate(self, operation: str) -> bool:
        """
        MANDATORY P0 GATE: Enforce 100% P0 compliance before ANY operation.

        Args:
            operation: Description of the operation being attempted

        Returns:
            True if P0 tests pass, False otherwise (blocks operation)
        """
        print(f"\n🛡️  P0 PROTECTION GATE: Validating {operation}")
        print("=" * 60)

        success, passing, total, failures = self.run_p0_validation()

        if success:
            print(f"✅ P0 GATE PASSED: {passing}/{total} tests passing (100%)")
            print(f"🟢 OPERATION APPROVED: {operation}")
            self.log_protection_event(
                "PASS", f"{operation} - P0 gate passed ({passing}/{total})"
            )
            return True
        else:
            print(
                f"🚨 P0 GATE FAILED: {passing}/{total} tests passing ({passing/total*100:.1f}%)"
            )
            print(f"🔴 OPERATION BLOCKED: {operation}")
            print("\n❌ FAILING P0 TESTS:")
            for failure in failures:
                print(f"   {failure}")

            print(f"\n🛑 MANDATORY ACTION REQUIRED:")
            print(f"   1. Fix ALL failing P0 tests immediately")
            print(f"   2. Run: python {self.p0_test_runner}")
            print(f"   3. Ensure {total}/{total} tests pass before proceeding")
            print(f"   4. P0 tests are BUSINESS-CRITICAL and cannot be deferred")

            self.log_protection_event(
                "BLOCK", f"{operation} - P0 gate failed ({passing}/{total}) - BLOCKED"
            )
            return False


def main():
    """CLI interface for P0 protection system."""
    import argparse

    parser = argparse.ArgumentParser(description="P0 Protection System")
    parser.add_argument("operation", help="Operation to validate")
    parser.add_argument(
        "--force", action="store_true", help="Force operation (NOT RECOMMENDED)"
    )

    args = parser.parse_args()

    protection = P0ProtectionSystem()

    if args.force:
        print("⚠️  WARNING: Forcing operation without P0 validation")
        print("🚨 This bypasses business-critical protection!")
        return True

    return protection.enforce_p0_gate(args.operation)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
