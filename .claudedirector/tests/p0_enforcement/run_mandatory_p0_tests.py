#!/usr/bin/env python3
"""
MANDATORY P0 Test Enforcement System
CRITICAL: These tests must NEVER be skipped and MUST pass before any commit.

Michael's requirement: "ensure that all P0 features are always tested moving forward and never skipped"
"""

import sys
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

class P0TestEnforcer:
    """
    Enforces mandatory P0 feature testing with zero tolerance for skipping
    """

    def __init__(self):
        self.start_time = datetime.now()
        self.p0_tests_defined = [
            {
                "name": "MCP Transparency P0",
                "module": ".claudedirector/tests/regression/test_mcp_transparency_p0.py",
                "critical_level": "BLOCKING",
                "description": "MCP server transparency disclosure must work",
                "failure_impact": "Strategic persona responses lose transparency"
            },
            {
                "name": "Conversation Tracking P0",
                "module": ".claudedirector/tests/conversation/test_conversation_tracking_p0.py",
                "critical_level": "BLOCKING",
                "description": "Strategic memory conversation capture must work",
                "failure_impact": "Strategic context preservation fails across sessions"
            },
            {
                "name": "Conversation Quality P0",
                "module": ".claudedirector/tests/conversation/test_p0_quality_target.py",
                "critical_level": "BLOCKING",
                "description": "Conversation quality must exceed 0.7 threshold",
                "failure_impact": "Strategic intelligence data quality degrades"
            },
            {
                "name": "First-Run Wizard P0",
                "module": "docs/testing/first_run_wizard_tests.py",
                "critical_level": "HIGH",
                "description": "First-run user experience must work",
                "failure_impact": "New users cannot customize system"
            },
            {
                "name": "Cursor Integration P0",
                "module": "docs/testing/run_cursor_tests.py",
                "critical_level": "HIGH",
                "description": "Cursor environment integration must work",
                "failure_impact": "Core usage environment fails"
            }
        ]

        self.test_results = []
        self.total_tests_run = 0
        self.blocking_failures = 0

    def validate_test_files_exist(self) -> bool:
        """Ensure all P0 test files exist before running"""
        print("🔍 VALIDATING P0 TEST FILES EXIST")
        print("=" * 60)

        missing_files = []
        for test in self.p0_tests_defined:
            test_path = PROJECT_ROOT / test["module"]
            if not test_path.exists():
                missing_files.append({
                    "test": test["name"],
                    "path": test["module"],
                    "critical": test["critical_level"]
                })
                print(f"❌ MISSING: {test['name']} -> {test['module']}")
            else:
                print(f"✅ EXISTS: {test['name']} -> {test['module']}")

        if missing_files:
            print(f"\n🚨 CRITICAL ERROR: {len(missing_files)} P0 test files missing!")
            for missing in missing_files:
                print(f"   - {missing['test']} ({missing['critical']}) -> {missing['path']}")
            print("\n❌ CANNOT PROCEED: All P0 tests must exist")
            return False

        print(f"✅ ALL {len(self.p0_tests_defined)} P0 TEST FILES VALIDATED")
        return True

    def run_single_p0_test(self, test_config: Dict) -> Dict:
        """Run a single P0 test with detailed tracking"""
        test_name = test_config["name"]
        test_module = test_config["module"]
        critical_level = test_config["critical_level"]

        print(f"\n🧪 RUNNING P0 TEST: {test_name}")
        print(f"   Module: {test_module}")
        print(f"   Critical Level: {critical_level}")
        print("-" * 50)

        start_time = time.time()

        try:
            # Run the test module
            test_path = PROJECT_ROOT / test_module
            cmd = [sys.executable, str(test_path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,  # 2 minute timeout
                cwd=PROJECT_ROOT
            )

            duration = time.time() - start_time

            test_result = {
                "name": test_name,
                "module": test_module,
                "critical_level": critical_level,
                "exit_code": result.returncode,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "description": test_config["description"],
                "failure_impact": test_config["failure_impact"]
            }

            if test_result["success"]:
                print(f"✅ PASSED: {test_name} ({duration:.2f}s)")
            else:
                print(f"❌ FAILED: {test_name} ({duration:.2f}s)")
                print(f"   Exit Code: {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")

                if critical_level == "BLOCKING":
                    self.blocking_failures += 1
                    print(f"🚨 BLOCKING FAILURE: {test_config['failure_impact']}")

            return test_result

        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT: {test_name} exceeded 2 minute limit")
            return {
                "name": test_name,
                "module": test_module,
                "critical_level": critical_level,
                "exit_code": -1,
                "duration": 120,
                "success": False,
                "error": "Test timeout after 2 minutes",
                "description": test_config["description"],
                "failure_impact": test_config["failure_impact"]
            }

        except Exception as e:
            print(f"💥 ERROR: {test_name} failed to run: {e}")
            return {
                "name": test_name,
                "module": test_module,
                "critical_level": critical_level,
                "exit_code": -1,
                "duration": 0,
                "success": False,
                "error": str(e),
                "description": test_config["description"],
                "failure_impact": test_config["failure_impact"]
            }

    def run_all_p0_tests(self) -> bool:
        """Run all P0 tests with zero tolerance for skipping"""
        print("\n🚨 MANDATORY P0 TEST EXECUTION")
        print("=" * 60)
        print("ZERO TOLERANCE: All P0 features must pass")
        print("NO SKIPPING ALLOWED")
        print()

        # Validate files exist first
        if not self.validate_test_files_exist():
            return False

        # Run each P0 test
        for test_config in self.p0_tests_defined:
            test_result = self.run_single_p0_test(test_config)
            self.test_results.append(test_result)
            self.total_tests_run += 1

        return self.blocking_failures == 0

    def generate_comprehensive_report(self) -> None:
        """Generate detailed P0 test execution report"""
        total_duration = (datetime.now() - self.start_time).total_seconds()

        print("\n" + "=" * 80)
        print("📊 MANDATORY P0 TEST EXECUTION REPORT")
        print("=" * 80)
        print(f"Execution Time: {total_duration:.2f} seconds")
        print(f"Tests Run: {self.total_tests_run}")
        print(f"Blocking Failures: {self.blocking_failures}")
        print()

        # Categorize results
        blocking_passed = [r for r in self.test_results if r["critical_level"] == "BLOCKING" and r["success"]]
        blocking_failed = [r for r in self.test_results if r["critical_level"] == "BLOCKING" and not r["success"]]
        high_passed = [r for r in self.test_results if r["critical_level"] == "HIGH" and r["success"]]
        high_failed = [r for r in self.test_results if r["critical_level"] == "HIGH" and not r["success"]]

        print("🚨 BLOCKING P0 FEATURES (MUST PASS):")
        for result in blocking_passed:
            print(f"   ✅ {result['name']} ({result['duration']:.2f}s)")
        for result in blocking_failed:
            print(f"   ❌ {result['name']} ({result['duration']:.2f}s)")
            print(f"      Impact: {result['failure_impact']}")

        print(f"\n🔺 HIGH PRIORITY P0 FEATURES:")
        for result in high_passed:
            print(f"   ✅ {result['name']} ({result['duration']:.2f}s)")
        for result in high_failed:
            print(f"   ⚠️ {result['name']} ({result['duration']:.2f}s)")
            print(f"      Impact: {result['failure_impact']}")

        # Overall status
        print("\n" + "-" * 80)
        if self.blocking_failures == 0:
            print("🎉 ALL BLOCKING P0 FEATURES PASSED")
            print("✅ COMMIT ALLOWED - P0 feature integrity maintained")
        else:
            print(f"🚨 {self.blocking_failures} BLOCKING P0 FAILURES DETECTED")
            print("❌ COMMIT BLOCKED - P0 feature integrity compromised")
            print("\n🛠️ REQUIRED ACTIONS:")
            for result in blocking_failed:
                print(f"   - Fix {result['name']}: {result['description']}")

        # High priority warnings
        high_failure_count = len(high_failed)
        if high_failure_count > 0:
            print(f"\n⚠️ {high_failure_count} HIGH PRIORITY P0 WARNINGS")
            print("Recommended to address before merge")

        print("=" * 80)

    def save_test_results(self) -> None:
        """Save test results for audit trail"""
        try:
            import json

            results_dir = PROJECT_ROOT / ".claudedirector/tests/p0_enforcement/results"
            results_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = results_dir / f"p0_test_results_{timestamp}.json"

            audit_data = {
                "timestamp": datetime.now().isoformat(),
                "total_tests": self.total_tests_run,
                "blocking_failures": self.blocking_failures,
                "total_duration": (datetime.now() - self.start_time).total_seconds(),
                "test_results": self.test_results,
                "compliance_status": "PASSED" if self.blocking_failures == 0 else "FAILED"
            }

            with open(results_file, 'w') as f:
                json.dump(audit_data, f, indent=2)

            print(f"📋 Test results saved: {results_file}")

        except Exception as e:
            print(f"⚠️ Failed to save test results: {e}")


def main():
    """
    Main P0 test enforcement entry point
    Returns exit code 0 only if all BLOCKING P0 tests pass
    """
    print("🛡️ MANDATORY P0 TEST ENFORCEMENT SYSTEM")
    print("=" * 80)
    print("Michael's Requirement: All P0 features always tested, never skipped")
    print("Zero tolerance for P0 feature regressions")
    print()

    enforcer = P0TestEnforcer()

    try:
        # Run all P0 tests
        success = enforcer.run_all_p0_tests()

        # Generate comprehensive report
        enforcer.generate_comprehensive_report()

        # Save results for audit
        enforcer.save_test_results()

        # Return appropriate exit code
        if success:
            print("\n✅ ALL MANDATORY P0 TESTS PASSED")
            print("🚀 P0 feature integrity maintained - commit allowed")
            return 0
        else:
            print(f"\n❌ {enforcer.blocking_failures} BLOCKING P0 FAILURES")
            print("🚫 P0 feature integrity compromised - commit blocked")
            return 1

    except KeyboardInterrupt:
        print("\n⚠️ P0 test execution interrupted")
        print("❌ Cannot verify P0 feature integrity - commit blocked")
        return 1

    except Exception as e:
        print(f"\n💥 P0 test enforcement system error: {e}")
        print("❌ Cannot verify P0 feature integrity - commit blocked")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
