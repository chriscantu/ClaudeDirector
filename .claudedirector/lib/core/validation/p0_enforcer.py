#!/usr/bin/env python3
"""
P0 Enforcement Suite - Consolidated Critical Feature Validation

🚨 CRITICAL ENFORCEMENT: All P0 features in one unified tool
🎯 ZERO TOLERANCE: Sequential Thinking + Context7 + P0 compliance
🏗️ CONSOLIDATED: Replaces multiple enforcement tools with single efficient suite

This consolidated enforcer validates all P0 critical features:
- Sequential Thinking Methodology compliance
- Context7 MCP Utilization rates
- P0 test integrity and compliance

Author: Martin | Platform Architecture with Sequential Thinking methodology
"""

import os
import sys
import subprocess
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Set
from datetime import datetime


class P0EnforcementSuite:
    """
    🚨 UNIFIED P0 CRITICAL FEATURE ENFORCEMENT ENGINE

    CONSOLIDATED ENFORCEMENT:
    1. Sequential Thinking Methodology - Must be applied to ALL development
    2. Context7 MCP Utilization - Must be used for strategic frameworks
    3. P0 Test Compliance - All P0 tests must pass

    ENFORCEMENT LEVELS:
    - BLOCKING: Prevents commits without P0 compliance
    - MONITORING: Tracks P0 feature utilization rates
    - REPORTING: Generates unified P0 compliance reports
    """

    def __init__(self):
        self.project_root = self._find_project_root()
        self.enforcement_results = {
            "sequential_thinking": {
                "status": "unknown",
                "details": [],
                "compliance_rate": 0.0,
            },
            "context7_utilization": {
                "status": "unknown",
                "details": [],
                "utilization_rate": 0.0,
            },
            "p0_test_compliance": {
                "status": "unknown",
                "details": [],
                "pass_rate": 0.0,
            },
            "overall_compliance": False,
            "timestamp": datetime.now().isoformat(),
        }

        # P0 Critical thresholds
        self.min_sequential_thinking_compliance = 95.0
        self.min_context7_utilization_rate = 80.0
        self.min_p0_test_pass_rate = 100.0

        # Sequential Thinking compliance patterns
        self.sequential_thinking_patterns = [
            r"Sequential Thinking",
            r"🏗️.*Sequential Thinking",
            r"systematic.*approach",
            r"step.*by.*step",
            r"methodical.*analysis",
        ]

        # Context7 utilization patterns
        self.context7_patterns = [
            r"Context7.*MCP",
            r"🔧.*Accessing.*MCP.*Server.*context7",
            r"strategic.*framework.*patterns",
            r"enhance_with_context7",
        ]

    def _find_project_root(self) -> Path:
        """Find the project root directory."""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".claudedirector").exists():
                return current
            current = current.parent
        return Path.cwd()

    def validate_sequential_thinking(self) -> Dict[str, Any]:
        """Validate Sequential Thinking compliance across ALL development files."""
        try:
            # P0 CRITICAL: Validate ALL development files, not just staged files
            # Sequential Thinking must be applied to ALL development and analysis activities

            # Get all Python files in .claudedirector (core development area)
            development_files = []
            claudedirector_path = self.project_root / ".claudedirector"

            if claudedirector_path.exists():
                for py_file in claudedirector_path.rglob("*.py"):
                    # Skip test files and __init__.py files
                    if (
                        not py_file.name.startswith("test_")
                        and py_file.name != "__init__.py"
                    ):
                        # Skip backup directories, legacy files, and utility files
                        skip_patterns = [
                            "backups/",
                            "__pycache__",
                            "setup.py",
                            "conftest.py",
                            "demo_",
                            "simple_test.py",
                            "regression_test.py",
                        ]
                        if not any(skip in str(py_file) for skip in skip_patterns):
                            # Focus on core development areas
                            if any(
                                core_area in str(py_file)
                                for core_area in [
                                    "lib/core/",
                                    "lib/personas/",
                                    "lib/ai_intelligence/",
                                    "lib/context_engineering/",
                                    "tools/architecture/",
                                ]
                            ):
                                development_files.append(
                                    str(py_file.relative_to(self.project_root))
                                )

            if not development_files:
                return {
                    "status": "pass",
                    "details": ["No development files found"],
                    "compliance_rate": 100.0,
                }

            compliant_files = []
            non_compliant_files = []

            for file_path in development_files:
                full_path = self.project_root / file_path
                if full_path.exists():
                    if self._check_sequential_thinking_compliance(full_path):
                        compliant_files.append(file_path)
                    else:
                        non_compliant_files.append(file_path)

            total_files = len(development_files)
            compliance_rate = (
                (len(compliant_files) / total_files * 100) if total_files > 0 else 100.0
            )

            status = (
                "pass"
                if compliance_rate >= self.min_sequential_thinking_compliance
                else "fail"
            )

            return {
                "status": status,
                "compliance_rate": compliance_rate,
                "details": [
                    f"Compliant files: {len(compliant_files)}/{total_files}",
                    f"Compliance rate: {compliance_rate:.1f}%",
                    (
                        f"Non-compliant: {non_compliant_files}"
                        if non_compliant_files
                        else "All files compliant"
                    ),
                ],
            }

        except Exception as e:
            return {
                "status": "error",
                "details": [f"Sequential Thinking validation failed: {str(e)}"],
            }

    def _check_sequential_thinking_compliance(self, file_path: Path) -> bool:
        """Check if a file demonstrates Sequential Thinking compliance."""
        try:
            content = file_path.read_text(encoding="utf-8")

            # Check for Sequential Thinking patterns
            pattern_matches = sum(
                1
                for pattern in self.sequential_thinking_patterns
                if re.search(pattern, content, re.IGNORECASE)
            )

            # File is compliant if it has at least one Sequential Thinking pattern
            # or if it's a test file (tests inherit methodology from implementation)
            return pattern_matches > 0 or "test_" in file_path.name

        except Exception:
            return False

    def validate_context7_utilization(self) -> Dict[str, Any]:
        """Validate Context7 MCP utilization across the codebase."""
        try:
            # Find all Python files that should use Context7
            strategic_files = []
            context7_files = []

            for py_file in self.project_root.rglob("*.py"):
                if any(
                    keyword in py_file.read_text(encoding="utf-8").lower()
                    for keyword in ["strategic", "framework", "pattern", "architecture"]
                ):
                    strategic_files.append(py_file)

                    # Check if file uses Context7
                    content = py_file.read_text(encoding="utf-8")
                    if any(
                        re.search(pattern, content, re.IGNORECASE)
                        for pattern in self.context7_patterns
                    ):
                        context7_files.append(py_file)

            total_strategic = len(strategic_files)
            context7_using = len(context7_files)
            utilization_rate = (
                (context7_using / total_strategic * 100)
                if total_strategic > 0
                else 100.0
            )

            status = (
                "pass"
                if utilization_rate >= self.min_context7_utilization_rate
                else "fail"
            )

            return {
                "status": status,
                "utilization_rate": utilization_rate,
                "details": [
                    f"Strategic files using Context7: {context7_using}/{total_strategic}",
                    f"Utilization rate: {utilization_rate:.1f}%",
                    f"Target: {self.min_context7_utilization_rate}%",
                ],
            }

        except Exception as e:
            return {
                "status": "error",
                "details": [f"Context7 validation failed: {str(e)}"],
            }

    def validate_p0_test_compliance(self) -> Dict[str, Any]:
        """Validate P0 test compliance by running the P0 test suite."""
        try:
            p0_test_runner = (
                self.project_root
                / ".claudedirector"
                / "tests"
                / "p0_enforcement"
                / "run_mandatory_p0_tests.py"
            )

            if not p0_test_runner.exists():
                return {"status": "error", "details": ["P0 test runner not found"]}

            # Run P0 tests
            result = subprocess.run(
                [sys.executable, str(p0_test_runner)],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300,  # 5 minute timeout
            )

            # Parse results (simplified - looks for "ALL P0 FEATURES PASSED")
            if "ALL P0 FEATURES PASSED" in result.stdout:
                return {
                    "status": "pass",
                    "pass_rate": 100.0,
                    "details": ["All P0 tests passing"],
                }
            else:
                return {
                    "status": "fail",
                    "pass_rate": 0.0,
                    "details": [
                        "P0 test failures detected",
                        result.stdout[-500:],
                    ],  # Last 500 chars
                }

        except subprocess.TimeoutExpired:
            return {"status": "error", "details": ["P0 test validation timed out"]}
        except Exception as e:
            return {
                "status": "error",
                "details": [f"P0 test validation failed: {str(e)}"],
            }

    def run_enforcement(self) -> Dict[str, Any]:
        """Run complete P0 enforcement suite."""
        print("🚨 P0 ENFORCEMENT SUITE - CRITICAL FEATURE VALIDATION")
        print("=" * 60)

        # Run all validations
        self.enforcement_results["sequential_thinking"] = (
            self.validate_sequential_thinking()
        )
        self.enforcement_results["context7_utilization"] = (
            self.validate_context7_utilization()
        )
        self.enforcement_results["p0_test_compliance"] = (
            self.validate_p0_test_compliance()
        )

        # Determine overall compliance
        all_pass = all(
            result["status"] == "pass"
            for result in [
                self.enforcement_results["sequential_thinking"],
                self.enforcement_results["context7_utilization"],
                self.enforcement_results["p0_test_compliance"],
            ]
        )

        self.enforcement_results["overall_compliance"] = all_pass

        # Print results
        self._print_results()

        # Save results
        self._save_results()

        return self.enforcement_results

    def _print_results(self):
        """Print enforcement results to console."""
        print("\n📊 P0 ENFORCEMENT RESULTS:")
        print("-" * 40)

        for feature, result in self.enforcement_results.items():
            if feature in ["overall_compliance", "timestamp"]:
                continue

            status_emoji = (
                "✅"
                if result["status"] == "pass"
                else "❌" if result["status"] == "fail" else "⚠️"
            )
            print(
                f"{status_emoji} {feature.replace('_', ' ').title()}: {result['status'].upper()}"
            )

            for detail in result.get("details", []):
                print(f"   • {detail}")
            print()

        overall_emoji = "✅" if self.enforcement_results["overall_compliance"] else "❌"
        print(
            f"{overall_emoji} OVERALL P0 COMPLIANCE: {'PASS' if self.enforcement_results['overall_compliance'] else 'FAIL'}"
        )

    def _save_results(self):
        """Save enforcement results to file."""
        results_dir = self.project_root / ".claudedirector" / "enforcement_results"
        results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"p0_enforcement_results_{timestamp}.json"

        with open(results_file, "w") as f:
            json.dump(self.enforcement_results, f, indent=2)

        print(f"\n📋 Results saved: {results_file}")


def main():
    """Main enforcement entry point."""
    enforcer = P0EnforcementSuite()
    results = enforcer.run_enforcement()

    # Exit with appropriate code
    sys.exit(0 if results["overall_compliance"] else 1)


if __name__ == "__main__":
    main()
