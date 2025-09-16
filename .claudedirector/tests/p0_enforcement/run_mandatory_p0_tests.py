#!/usr/bin/env python3
"""
MANDATORY P0 Test Enforcement System
CRITICAL: These tests must NEVER be skipped and MUST pass before any commit.

Enforces user requirement: "ensure that all P0 features are always tested moving forward and never skipped"
"""

import sys
import subprocess
import time
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

# Import user configuration
try:
    from config.user_config import get_user_attribution, get_user_name

    USER_ATTRIBUTION = get_user_attribution()
    USER_NAME = get_user_name("professional")
except ImportError:
    # Fallback if user config not available
    USER_ATTRIBUTION = "User's requirement"
    USER_NAME = "User"


class P0TestEnforcer:
    """
    Enforces mandatory P0 feature testing with zero tolerance for skipping
    """

    def __init__(self):
        self.start_time = datetime.now()
        self.p0_tests_defined = self._load_p0_tests_from_yaml()
        self.test_results = []
        self.total_tests_run = 0
        self.blocking_failures = 0
        self.total_failures = 0  # Track ALL P0 failures regardless of critical level

    def _load_p0_tests_from_yaml(self) -> List[Dict]:
        """Load P0 test definitions from YAML configuration file"""
        yaml_path = (
            PROJECT_ROOT
            / ".claudedirector/tests/p0_enforcement/p0_test_definitions.yaml"
        )

        if not yaml_path.exists():
            print(f"⚠️ P0 definitions file not found: {yaml_path}")
            print("⚠️ Falling back to minimal P0 test set")
            return [
                {
                    "name": "MCP Transparency P0",
                    "test_module": ".claudedirector/tests/regression/p0_blocking/test_mcp_transparency.py",
                    "critical_level": "BLOCKING",
                    "description": "MCP server transparency disclosure must work",
                    "failure_impact": "Strategic persona responses lose transparency",
                }
            ]

        try:
            with open(yaml_path, "r") as f:
                config = yaml.safe_load(f)

            # Convert YAML format to expected format
            p0_tests = []
            for test_def in config.get("p0_features", []):
                p0_tests.append(
                    {
                        "name": test_def["name"],
                        "module": test_def[
                            "test_module"
                        ],  # YAML uses 'test_module', code expects 'module'
                        "critical_level": test_def["critical_level"],
                        "description": test_def["description"],
                        "failure_impact": test_def["failure_impact"],
                    }
                )

            print(f"✅ Loaded {len(p0_tests)} P0 tests from YAML configuration")
            return p0_tests

        except Exception as e:
            print(f"❌ Error loading P0 definitions from YAML: {e}")
            print("⚠️ Falling back to minimal P0 test set")
            return [
                {
                    "name": "MCP Transparency P0",
                    "module": ".claudedirector/tests/regression/p0_blocking/test_mcp_transparency.py",
                    "critical_level": "BLOCKING",
                    "description": "MCP server transparency disclosure must work",
                    "failure_impact": "Strategic persona responses lose transparency",
                }
            ]

    def validate_test_files_exist(self) -> bool:
        """Ensure all P0 test files exist before running"""
        print("🔍 VALIDATING P0 TEST FILES EXIST")
        print("=" * 60)

        missing_files = []
        for test in self.p0_tests_defined:
            test_path = PROJECT_ROOT / test["module"]
            if not test_path.exists():
                missing_files.append(
                    {
                        "test": test["name"],
                        "path": test["module"],
                        "critical": test["critical_level"],
                    }
                )
                print(f"❌ MISSING: {test['name']} -> {test['module']}")
            else:
                print(f"✅ EXISTS: {test['name']} -> {test['module']}")

        if missing_files:
            print(f"\n🚨 CRITICAL ERROR: {len(missing_files)} P0 test files missing!")
            for missing in missing_files:
                print(
                    f"   - {missing['test']} ({missing['critical']}) -> {missing['path']}"
                )
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
            # Run the test module (handle both files and directories)
            test_path = PROJECT_ROOT / test_module

            if test_path.is_dir():
                # Handle modular tests (directory with multiple test files)
                return self._run_modular_tests(test_config, test_path, start_time)
            else:
                # Handle single test file
                cmd = [sys.executable, str(test_path)]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,  # 2 minute timeout
                    cwd=PROJECT_ROOT,
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
                "failure_impact": test_config["failure_impact"],
            }

            if test_result["success"]:
                print(f"✅ PASSED: {test_name} ({duration:.2f}s)")
            else:
                print(f"❌ FAILED: {test_name} ({duration:.2f}s)")
                print(f"   Exit Code: {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")

                # ALL P0 failures are critical regardless of level
                self.total_failures += 1
                if critical_level == "BLOCKING":
                    self.blocking_failures += 1
                    print(f"🚨 BLOCKING FAILURE: {test_config['failure_impact']}")
                else:
                    print(f"🚨 P0 FAILURE: {test_config['failure_impact']}")

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
                "failure_impact": test_config["failure_impact"],
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
                "failure_impact": test_config["failure_impact"],
            }

    def _run_modular_tests(
        self, test_config: Dict, test_path: Path, start_time: float
    ) -> Dict:
        """Run all test files in a directory (modular tests)"""
        test_name = test_config["name"]
        critical_level = test_config["critical_level"]

        # Find all test files in the directory
        test_files = list(test_path.glob("test_*.py"))

        if not test_files:
            print(f"⚠️ No test files found in {test_path}")
            duration = time.time() - start_time
            return {
                "name": test_name,
                "module": test_config["module"],
                "critical_level": critical_level,
                "exit_code": 1,
                "duration": duration,
                "success": False,
                "error": f"No test files found in directory {test_path}",
                "description": test_config["description"],
                "failure_impact": test_config["failure_impact"],
            }

        print(f"   Running {len(test_files)} modular tests...")

        all_passed = True
        combined_stdout = []
        combined_stderr = []
        failed_tests = []

        for test_file in sorted(test_files):
            print(f"     • {test_file.name}")

            result = subprocess.run(
                [sys.executable, str(test_file)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=60,  # 1 minute per modular test
            )

            if result.returncode == 0:
                combined_stdout.append(f"✅ {test_file.name}: PASSED")
                if result.stdout.strip():
                    combined_stdout.append(result.stdout.strip())
            else:
                all_passed = False
                failed_tests.append(test_file.name)
                combined_stderr.append(
                    f"❌ {test_file.name}: FAILED (exit {result.returncode})"
                )
                if result.stdout.strip():
                    combined_stderr.append(result.stdout.strip())
                if result.stderr.strip():
                    combined_stderr.append(result.stderr.strip())

        duration = time.time() - start_time

        if all_passed:
            print(
                f"✅ PASSED: {test_name} ({duration:.2f}s) - All {len(test_files)} modular tests passed"
            )
            return {
                "name": test_name,
                "module": test_config["module"],
                "critical_level": critical_level,
                "exit_code": 0,
                "duration": duration,
                "success": True,
                "stdout": "\n".join(combined_stdout),
                "stderr": "",
                "description": test_config["description"],
                "failure_impact": test_config["failure_impact"],
            }
        else:
            print(
                f"❌ FAILED: {test_name} ({duration:.2f}s) - {len(failed_tests)} modular tests failed: {', '.join(failed_tests)}"
            )

            # ALL P0 failures are critical regardless of level
            self.total_failures += 1
            if critical_level == "BLOCKING":
                self.blocking_failures += 1
                print(f"🚨 BLOCKING FAILURE: {test_config['failure_impact']}")
            else:
                print(f"🚨 P0 FAILURE: {test_config['failure_impact']}")

            return {
                "name": test_name,
                "module": test_config["module"],
                "critical_level": critical_level,
                "exit_code": 1,
                "duration": duration,
                "success": False,
                "stdout": "\n".join(combined_stdout),
                "stderr": "\n".join(combined_stderr),
                "description": test_config["description"],
                "failure_impact": test_config["failure_impact"],
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

        return self.total_failures == 0  # ALL P0 failures block commits

    def generate_comprehensive_report(self) -> None:
        """Generate detailed P0 test execution report"""
        total_duration = (datetime.now() - self.start_time).total_seconds()

        print("\n" + "=" * 80)
        print("📊 MANDATORY P0 TEST EXECUTION REPORT")
        print("=" * 80)
        print(f"Execution Time: {total_duration:.2f} seconds")
        print(f"Tests Run: {self.total_tests_run}")
        print(f"Blocking Failures: {self.blocking_failures}")
        print(f"Total P0 Failures: {self.total_failures}")
        print()

        # Categorize results
        blocking_passed = [
            r
            for r in self.test_results
            if r["critical_level"] == "BLOCKING" and r["success"]
        ]
        blocking_failed = [
            r
            for r in self.test_results
            if r["critical_level"] == "BLOCKING" and not r["success"]
        ]
        high_passed = [
            r
            for r in self.test_results
            if r["critical_level"] == "HIGH" and r["success"]
        ]
        high_failed = [
            r
            for r in self.test_results
            if r["critical_level"] == "HIGH" and not r["success"]
        ]

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
        if self.total_failures == 0:
            print("🎉 ALL P0 FEATURES PASSED")
            print("✅ COMMIT ALLOWED - P0 feature integrity maintained")
        else:
            print(f"🚨 {self.total_failures} P0 FAILURES DETECTED")
            print("❌ COMMIT BLOCKED - P0 feature integrity compromised")
            print("\n🛠️ REQUIRED ACTIONS:")
            for result in [r for r in self.test_results if not r["success"]]:
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
                "total_failures": self.total_failures,
                "total_duration": (datetime.now() - self.start_time).total_seconds(),
                "test_results": self.test_results,
                "compliance_status": (
                    "PASSED" if self.total_failures == 0 else "FAILED"
                ),
            }

            with open(results_file, "w") as f:
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
    print(f"{USER_ATTRIBUTION}: All P0 features always tested, never skipped")
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
            # Add CI-compatible success rate format for GitHub workflows
            print(
                f"📊 SUCCESS RATE: {enforcer.total_tests_run}/{enforcer.total_tests_run} tests passing (100%)"
            )
            return 0
        else:
            print(f"\n❌ {enforcer.total_failures} P0 FAILURES")
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
