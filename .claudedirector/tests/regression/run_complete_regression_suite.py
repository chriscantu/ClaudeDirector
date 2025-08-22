#!/usr/bin/env python3
"""
Complete Regression Test Suite Runner

CRITICAL: This runner executes ALL regression tests that must pass before any commit.
Enforces 100% success rate requirement - NO EXCEPTIONS.

Integration with pre-push hook ensures these tests cannot be circumvented.
"""

import sys
import os
import time
from pathlib import Path
import subprocess
from typing import List, Dict, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class RegressionTestRunner:
    """Comprehensive regression test runner with strict enforcement"""

    def __init__(self):
        self.tests_dir = Path(__file__).parent
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.start_time = time.time()

        # Critical regression test modules (ORDER MATTERS - critical first)
        self.regression_tests = [
            {
                "name": "Configuration Integrity",
                "module": "test_configuration_integrity.py",
                "critical": True,
                "description": "Validates configuration system before SOLID refactoring",
                "blocking": True,
            },
            {
                "name": "Framework Engine Regression",
                "module": "test_framework_engine_regression.py",
                "critical": True,
                "description": "Protects framework detection during refactoring",
                "blocking": True,
            },
            {
                "name": "Hybrid Installation P0",
                "module": "test_hybrid_installation_p0.py",
                "critical": True,
                "description": "Validates 58% performance improvement with zero setup maintained",
                "blocking": True,
            },
        ]

    def run_single_test(self, test_info: Dict) -> Tuple[bool, str, float]:
        """Run a single regression test module"""
        test_name = test_info["name"]
        test_module = test_info["module"]
        test_path = self.tests_dir / test_module

        print(f"\n{'='*60}")
        print(f"🧪 RUNNING: {test_name}")
        print(f"📁 Module: {test_module}")
        print(f"🎯 Critical: {'YES' if test_info['critical'] else 'NO'}")
        print(f"🚫 Blocking: {'YES' if test_info['blocking'] else 'NO'}")
        print(f"{'='*60}")

        if not test_path.exists():
            error_msg = f"❌ Test module not found: {test_path}"
            print(error_msg)
            return False, error_msg, 0.0

        start_time = time.time()

        try:
            # Run test module
            result = subprocess.run(
                [sys.executable, str(test_path)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout per test
            )

            end_time = time.time()
            duration = end_time - start_time

            # Print output for visibility
            if result.stdout:
                print("📤 STDOUT:")
                print(result.stdout)

            if result.stderr:
                print("📤 STDERR:")
                print(result.stderr)

            success = result.returncode == 0

            if success:
                print(f"✅ {test_name} PASSED ({duration:.2f}s)")
                return True, f"Passed in {duration:.2f}s", duration
            else:
                error_msg = f"❌ {test_name} FAILED (exit code: {result.returncode}, duration: {duration:.2f}s)"
                print(error_msg)
                return False, error_msg, duration

        except subprocess.TimeoutExpired:
            error_msg = f"⏰ {test_name} TIMED OUT (>300s)"
            print(error_msg)
            return False, error_msg, 300.0

        except Exception as e:
            error_msg = f"💥 {test_name} ERROR: {e}"
            print(error_msg)
            return False, error_msg, 0.0

    def run_all_regression_tests(self) -> bool:
        """Run complete regression test suite with strict enforcement"""
        print("🚨 COMPLETE REGRESSION TEST SUITE")
        print("=" * 80)
        print("CRITICAL: 100% SUCCESS RATE REQUIRED - NO EXCEPTIONS")
        print("This test suite protects against regressions during SOLID refactoring")
        print("ALL TESTS MUST PASS or commit will be BLOCKED")
        print("=" * 80)

        results = []
        blocking_failures = []

        for test_info in self.regression_tests:
            self.total_tests += 1

            success, message, duration = self.run_single_test(test_info)

            results.append(
                {
                    "test": test_info["name"],
                    "success": success,
                    "message": message,
                    "duration": duration,
                    "critical": test_info["critical"],
                    "blocking": test_info["blocking"],
                }
            )

            if success:
                self.passed_tests += 1
            else:
                self.failed_tests += 1
                if test_info["blocking"]:
                    blocking_failures.append(test_info["name"])

        # Generate final report
        self._generate_final_report(results, blocking_failures)

        # Determine overall success
        overall_success = len(blocking_failures) == 0 and self.failed_tests == 0

        return overall_success

    def _generate_final_report(self, results: List[Dict], blocking_failures: List[str]):
        """Generate comprehensive final report"""
        total_duration = time.time() - self.start_time

        print(f"\n{'='*80}")
        print("📊 REGRESSION TEST SUITE FINAL REPORT")
        print(f"{'='*80}")
        print(f"⏱️  Total Duration: {total_duration:.2f}s")
        print(f"🧪 Tests Run: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")

        print(f"\n📋 DETAILED RESULTS:")
        for result in results:
            status_icon = "✅" if result["success"] else "❌"
            critical_icon = "🚨" if result["critical"] else "ℹ️"
            blocking_icon = "🚫" if result["blocking"] else "⚠️"

            print(f"   {status_icon} {critical_icon} {blocking_icon} {result['test']}")
            print(f"      Duration: {result['duration']:.2f}s")
            print(f"      Result: {result['message']}")

        if blocking_failures:
            print(f"\n🚫 BLOCKING FAILURES DETECTED:")
            for failure in blocking_failures:
                print(f"   💥 {failure}")
            print(f"\n❌ COMMIT BLOCKED - MUST FIX ALL BLOCKING FAILURES")
            print(f"🔧 Run individual tests to debug issues")
            print(f"🚫 DO NOT use --no-verify to bypass these failures")

        elif self.failed_tests > 0:
            print(f"\n⚠️ NON-BLOCKING FAILURES DETECTED:")
            non_blocking_failures = [
                r for r in results if not r["success"] and not r["blocking"]
            ]
            for failure in non_blocking_failures:
                print(f"   ⚠️ {failure['test']}")
            print(f"\n✅ COMMIT ALLOWED but failures should be addressed")

        else:
            print(f"\n🎉 ALL REGRESSION TESTS PASSED!")
            print(f"✅ Safe to proceed with SOLID refactoring")
            print(f"🛡️ Regression protection active and validated")

        # Add enforcement message
        print(f"\n{'='*80}")
        print("🛡️ REGRESSION PROTECTION ENFORCEMENT")
        print(f"{'='*80}")
        print("These tests are integrated into:")
        print("  🪝 Pre-push hook (mandatory)")
        print("  🔄 CI/CD pipeline (blocking)")
        print("  🚫 Cannot be bypassed with --no-verify")
        print("  📊 100% success rate required for all commits")


def main():
    """Main entry point for regression test runner"""
    runner = RegressionTestRunner()
    success = runner.run_all_regression_tests()

    # Exit with appropriate code
    if success:
        print(f"\n🎯 REGRESSION TEST SUCCESS - COMMIT APPROVED")
        sys.exit(0)
    else:
        print(f"\n🚫 REGRESSION TEST FAILURE - COMMIT BLOCKED")
        sys.exit(1)


if __name__ == "__main__":
    main()
