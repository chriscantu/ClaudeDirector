#!/usr/bin/env python3
"""
Comprehensive Unit Test Suite Runner
Orchestrates all unit tests with coverage reporting for CI/CD pipeline
"""

import sys
import unittest
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple

# Add project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

class UnitTestSuiteRunner:
    """Comprehensive unit test runner with coverage reporting"""

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.unit_tests_dir = self.project_root / ".claudedirector/tests/unit"
        self.lib_dir = self.project_root / ".claudedirector/lib"
        self.results = {}

    def discover_unit_tests(self) -> List[Path]:
        """Discover all unit test files"""
        test_files = []

        # Find all test_*.py files in unit tests directory
        for test_file in self.unit_tests_dir.glob("test_*.py"):
            if test_file.name != "test_suite_runner.py":  # Exclude self
                test_files.append(test_file)

        return sorted(test_files)

    def run_single_test_file(self, test_file: Path) -> Tuple[bool, Dict]:
        """Run a single test file and return results"""
        test_name = test_file.stem
        print(f"🧪 Running Unit Tests: {test_name}")

        start_time = time.time()

        try:
            # Run the test file directly
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=120,  # 2 minute timeout per test file
                cwd=self.project_root
            )

            duration = time.time() - start_time

            success = result.returncode == 0

            test_result = {
                "name": test_name,
                "success": success,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }

            if success:
                print(f"   ✅ PASSED ({duration:.2f}s)")
            else:
                print(f"   ❌ FAILED ({duration:.2f}s)")
                print(f"      Error: {result.stderr[:200]}...")

            return success, test_result

        except subprocess.TimeoutExpired:
            print(f"   ⏰ TIMEOUT (>120s)")
            return False, {
                "name": test_name,
                "success": False,
                "duration": 120.0,
                "error": "Test timed out after 120 seconds"
            }
        except Exception as e:
            print(f"   💥 ERROR: {str(e)}")
            return False, {
                "name": test_name,
                "success": False,
                "duration": 0.0,
                "error": str(e)
            }

    def run_coverage_analysis(self) -> Dict:
        """Run coverage analysis on the codebase"""
        print("\n📊 Running Coverage Analysis...")

        try:
            # Check if coverage is available
            subprocess.run([sys.executable, "-m", "coverage", "--version"],
                          capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ⚠️  Coverage tool not available - installing...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "coverage"],
                              check=True)
            except subprocess.CalledProcessError:
                return {
                    "available": False,
                    "error": "Could not install coverage tool"
                }

        try:
            # Run coverage on unit tests
            unit_test_files = self.discover_unit_tests()

            if not unit_test_files:
                return {
                    "available": True,
                    "coverage_percent": 0,
                    "message": "No unit test files found"
                }

            # Create coverage command
            coverage_cmd = [
                sys.executable, "-m", "coverage", "run",
                "--source", str(self.lib_dir),
                "--omit", "*/test*,*/tests/*,*/__pycache__/*",
                "-m", "unittest", "discover",
                "-s", str(self.unit_tests_dir),
                "-p", "test_*.py",
                "-v"
            ]

            result = subprocess.run(
                coverage_cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300  # 5 minute timeout for coverage
            )

            # Generate coverage report
            report_result = subprocess.run(
                [sys.executable, "-m", "coverage", "report", "--show-missing"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )

            # Parse coverage percentage
            coverage_lines = report_result.stdout.split('\n')
            total_line = [line for line in coverage_lines if line.startswith('TOTAL')]

            coverage_percent = 0
            if total_line:
                # Extract percentage from line like "TOTAL     123    45    63%"
                parts = total_line[0].split()
                if len(parts) >= 4 and parts[-1].endswith('%'):
                    coverage_percent = int(parts[-1][:-1])

            return {
                "available": True,
                "success": result.returncode == 0,
                "coverage_percent": coverage_percent,
                "report": report_result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }

        except subprocess.TimeoutExpired:
            return {
                "available": True,
                "success": False,
                "error": "Coverage analysis timed out"
            }
        except Exception as e:
            return {
                "available": True,
                "success": False,
                "error": f"Coverage analysis failed: {str(e)}"
            }

    def run_all_unit_tests(self) -> Dict:
        """Run all unit tests and return comprehensive results"""
        print("🧪 COMPREHENSIVE UNIT TEST SUITE")
        print("=" * 60)
        print("Target: >85% code coverage for CI/CD pipeline")
        print()

        start_time = time.time()

        # Discover tests
        test_files = self.discover_unit_tests()

        if not test_files:
            return {
                "success": False,
                "message": "No unit test files found",
                "tests_run": 0,
                "tests_passed": 0,
                "duration": 0.0
            }

        print(f"📋 Discovered {len(test_files)} unit test files")
        print()

        # Run each test file
        tests_passed = 0
        test_results = []

        for test_file in test_files:
            success, result = self.run_single_test_file(test_file)
            test_results.append(result)

            if success:
                tests_passed += 1

        # Run coverage analysis
        coverage_result = self.run_coverage_analysis()

        total_duration = time.time() - start_time

        # Generate summary
        print("\n" + "=" * 60)
        print("📊 UNIT TEST SUITE SUMMARY")
        print("=" * 60)
        print(f"Tests Run: {len(test_files)}")
        print(f"Tests Passed: {tests_passed}")
        print(f"Tests Failed: {len(test_files) - tests_passed}")
        print(f"Total Duration: {total_duration:.2f}s")

        if coverage_result.get("available"):
            coverage_percent = coverage_result.get("coverage_percent", 0)
            print(f"Code Coverage: {coverage_percent}%")

            if coverage_percent >= 85:
                print("✅ Coverage Target Met (≥85%)")
            else:
                print(f"⚠️  Coverage Below Target ({coverage_percent}% < 85%)")
        else:
            print("⚠️  Coverage Analysis Not Available")

        print()

        # Overall success criteria
        all_tests_passed = tests_passed == len(test_files)
        coverage_target_met = coverage_result.get("coverage_percent", 0) >= 85

        overall_success = all_tests_passed and (
            not coverage_result.get("available") or coverage_target_met
        )

        if overall_success:
            print("🎉 ALL UNIT TESTS PASSED")
            if coverage_result.get("available"):
                print("✅ Coverage target achieved (≥85%)")
        else:
            print("❌ UNIT TEST SUITE FAILED")
            if not all_tests_passed:
                print(f"   {len(test_files) - tests_passed} test file(s) failed")
            if coverage_result.get("available") and not coverage_target_met:
                print(f"   Coverage below target ({coverage_result.get('coverage_percent', 0)}% < 85%)")

        return {
            "success": overall_success,
            "tests_run": len(test_files),
            "tests_passed": tests_passed,
            "duration": total_duration,
            "coverage": coverage_result,
            "test_results": test_results,
            "coverage_target_met": coverage_target_met
        }

def run_unit_test_suite():
    """Main entry point for unit test suite"""
    runner = UnitTestSuiteRunner()
    results = runner.run_all_unit_tests()

    # Exit with appropriate code for CI/CD
    sys.exit(0 if results["success"] else 1)

if __name__ == "__main__":
    run_unit_test_suite()
