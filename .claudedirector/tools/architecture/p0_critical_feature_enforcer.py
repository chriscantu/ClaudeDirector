#!/usr/bin/env python3
"""
P0 Critical Feature Enforcer

🚨 CRITICAL ENFORCEMENT: Sequential Thinking + Context7 Utilization P0 Features
🎯 ZERO TOLERANCE: These features must be enabled at all times
🏗️ SYSTEMATIC VALIDATION: Ensures P0 critical features are always functional

This enforcer validates that P0 critical features are consistently enabled
and functional across all development activities.

Author: Martin | Platform Architecture with Sequential Thinking methodology
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


class P0CriticalFeatureEnforcer:
    """
    🚨 P0 CRITICAL FEATURE ENFORCEMENT ENGINE

    MANDATORY P0 FEATURES:
    1. Sequential Thinking Methodology - Must be applied to ALL development
    2. Context7 MCP Utilization - Must be used for strategic frameworks

    ENFORCEMENT LEVELS:
    - BLOCKING: Prevents commits without P0 compliance
    - MONITORING: Tracks P0 feature utilization rates
    - REPORTING: Generates P0 compliance reports
    """

    def __init__(self):
        self.project_root = self._find_project_root()
        self.enforcement_results = {
            "sequential_thinking": {"status": "unknown", "details": []},
            "context7_utilization": {"status": "unknown", "details": []},
            "overall_compliance": False,
            "timestamp": datetime.now().isoformat(),
        }

        # P0 Critical thresholds
        self.min_sequential_thinking_compliance = 95.0
        self.min_context7_utilization_rate = 80.0

    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".claudedirector").exists():
                return current
            current = current.parent
        return Path.cwd()

    def enforce_sequential_thinking(self) -> Tuple[bool, List[str]]:
        """Enforce Sequential Thinking P0 critical feature"""
        print("🏗️ ENFORCING P0 CRITICAL: Sequential Thinking Methodology")
        print("-" * 60)

        issues = []

        # Check Sequential Thinking validator availability
        validator_path = (
            self.project_root
            / ".claudedirector"
            / "tools"
            / "architecture"
            / "sequential_thinking_validator.py"
        )
        if not validator_path.exists():
            issues.append("BLOCKING: Sequential Thinking validator missing")
            self.enforcement_results["sequential_thinking"][
                "status"
            ] = "CRITICAL_FAILURE"
            return False, issues

        # Run Sequential Thinking validation
        try:
            result = subprocess.run(
                [sys.executable, str(validator_path)],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=30,
            )

            if result.returncode == 0:
                issues.append("✅ Sequential Thinking validation PASSED")
                self.enforcement_results["sequential_thinking"]["status"] = "COMPLIANT"
                return True, issues
            else:
                issues.append("❌ Sequential Thinking validation FAILED")
                issues.append(f"Error output: {result.stderr}")
                self.enforcement_results["sequential_thinking"][
                    "status"
                ] = "NON_COMPLIANT"
                return False, issues

        except subprocess.TimeoutExpired:
            issues.append("❌ Sequential Thinking validation TIMEOUT")
            self.enforcement_results["sequential_thinking"]["status"] = "TIMEOUT"
            return False, issues
        except Exception as e:
            issues.append(f"❌ Sequential Thinking validation ERROR: {e}")
            self.enforcement_results["sequential_thinking"]["status"] = "ERROR"
            return False, issues

    def enforce_context7_utilization(self) -> Tuple[bool, List[str]]:
        """Enforce Context7 MCP Utilization P0 critical feature"""
        print("🔧 ENFORCING P0 CRITICAL: Context7 MCP Utilization")
        print("-" * 60)

        issues = []

        # Check for Context7 integration patterns in codebase
        context7_patterns = [
            "Context7",
            "context7",
            "🔧 Accessing MCP Server.*context7",
            "pattern_access",
            "framework_patterns",
        ]

        context7_files = []
        lib_dir = self.project_root / ".claudedirector" / "lib"

        if lib_dir.exists():
            for py_file in lib_dir.glob("**/*.py"):
                try:
                    with open(py_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    if any(
                        pattern.lower() in content.lower()
                        for pattern in context7_patterns
                    ):
                        context7_files.append(
                            str(py_file.relative_to(self.project_root))
                        )

                except Exception:
                    continue

        # Calculate Context7 utilization rate
        total_strategic_files = len(list(lib_dir.glob("**/strategic*.py"))) + len(
            list(lib_dir.glob("**/framework*.py"))
        )
        if total_strategic_files == 0:
            total_strategic_files = 1  # Avoid division by zero

        context7_utilization_rate = (len(context7_files) / total_strategic_files) * 100

        if context7_utilization_rate >= self.min_context7_utilization_rate:
            issues.append(
                f"✅ Context7 utilization rate: {context7_utilization_rate:.1f}%"
            )
            issues.append(f"✅ Context7 integrated files: {len(context7_files)}")
            self.enforcement_results["context7_utilization"]["status"] = "COMPLIANT"
            return True, issues
        else:
            issues.append(
                f"❌ Context7 utilization rate: {context7_utilization_rate:.1f}% (minimum: {self.min_context7_utilization_rate}%)"
            )
            issues.append(
                f"❌ Context7 integrated files: {len(context7_files)} (insufficient)"
            )
            issues.append(
                "❌ BLOCKING: Context7 MCP server must be utilized for strategic frameworks"
            )
            self.enforcement_results["context7_utilization"]["status"] = "NON_COMPLIANT"
            return False, issues

    def enforce_p0_critical_features(self) -> bool:
        """Enforce all P0 critical features"""
        print("🚨 P0 CRITICAL FEATURE ENFORCEMENT")
        print("=" * 70)
        print(
            "🎯 ZERO TOLERANCE: Sequential Thinking + Context7 must be enabled at all times"
        )
        print()

        all_compliant = True

        # Enforce Sequential Thinking
        sequential_compliant, sequential_issues = self.enforce_sequential_thinking()
        for issue in sequential_issues:
            print(f"  {issue}")
        print()

        # Enforce Context7 Utilization
        context7_compliant, context7_issues = self.enforce_context7_utilization()
        for issue in context7_issues:
            print(f"  {issue}")
        print()

        # Overall compliance
        overall_compliant = sequential_compliant and context7_compliant
        self.enforcement_results["overall_compliance"] = overall_compliant

        print("=" * 70)
        print("📊 P0 CRITICAL FEATURE ENFORCEMENT RESULTS")
        print("=" * 70)
        print(
            f"Sequential Thinking: {'✅ COMPLIANT' if sequential_compliant else '❌ NON-COMPLIANT'}"
        )
        print(
            f"Context7 Utilization: {'✅ COMPLIANT' if context7_compliant else '❌ NON-COMPLIANT'}"
        )
        print(
            f"Overall P0 Status: {'✅ COMPLIANT' if overall_compliant else '❌ NON-COMPLIANT'}"
        )

        if overall_compliant:
            print()
            print("🎉 ALL P0 CRITICAL FEATURES ENABLED")
            print("✅ Sequential Thinking methodology active")
            print("✅ Context7 MCP utilization functional")
            print("✅ Development can proceed")
        else:
            print()
            print("🚨 P0 CRITICAL FEATURE FAILURES DETECTED")
            print("❌ Development must address P0 compliance issues")
            print("❌ COMMIT BLOCKED until P0 features are enabled")
            print()
            print("📚 REQUIRED ACTIONS:")
            if not sequential_compliant:
                print("1. Enable Sequential Thinking methodology for all development")
                print("2. Add Sequential Thinking documentation to non-compliant files")
                print("3. Apply systematic approach to all technical decisions")
            if not context7_compliant:
                print("1. Integrate Context7 MCP server with strategic frameworks")
                print("2. Add Context7 pattern access to architectural guidance")
                print("3. Ensure Context7 transparency disclosure in MCP usage")

        return overall_compliant

    def save_enforcement_results(self):
        """Save enforcement results for monitoring and reporting"""
        results_dir = self.project_root / ".claudedirector" / "enforcement_results"
        results_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"p0_critical_enforcement_{timestamp}.json"

        with open(results_file, "w") as f:
            json.dump(self.enforcement_results, f, indent=2)

        print(f"📋 Enforcement results saved: {results_file}")

    def generate_compliance_report(self):
        """Generate P0 critical feature compliance report"""
        report_dir = self.project_root / ".claudedirector" / "compliance_reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"p0_critical_compliance_{timestamp}.md"

        # Build compliance status
        compliance_status = (
            "✅ COMPLIANT"
            if self.enforcement_results["overall_compliance"]
            else "❌ NON-COMPLIANT"
        )

        report_content = f"""# P0 Critical Feature Compliance Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Status**: {compliance_status}

## P0 Critical Features

### 1. Sequential Thinking Methodology"""

        # Build individual compliance sections
        sequential_status = self.enforcement_results["sequential_thinking"]["status"]
        sequential_compliance = (
            "✅ PASSED" if sequential_status == "COMPLIANT" else "❌ FAILED"
        )

        context7_status = self.enforcement_results["context7_utilization"]["status"]
        context7_compliance = (
            "✅ PASSED" if context7_status == "COMPLIANT" else "❌ FAILED"
        )

        report_content += f"""
- **Status**: {sequential_status}
- **Requirement**: Must be applied to ALL development and analysis activities
- **Compliance**: {sequential_compliance}

### 2. Context7 MCP Utilization
- **Status**: {context7_status}
- **Requirement**: Must be utilized for all strategic framework applications
- **Compliance**: {context7_compliance}

## Enforcement Actions Required

"""

        # Add actions section
        if self.enforcement_results["overall_compliance"]:
            report_content += "### ✅ No Actions Required - All P0 Features Compliant"
        else:
            report_content += """### ❌ Critical Actions Required

1. **Sequential Thinking Compliance**
   - Add Sequential Thinking methodology to all development activities
   - Ensure systematic approach documentation in all technical decisions
   - Validate Sequential Thinking validator functionality

2. **Context7 Utilization Compliance**
   - Integrate Context7 MCP server with strategic frameworks
   - Add Context7 pattern access to architectural guidance
   - Implement Context7 transparency disclosure

3. **Immediate Actions**
   - Run P0 critical feature tests: `python -m pytest .claudedirector/tests/regression/p0_blocking/test_sequential_thinking_p0.py`
   - Run Context7 validation: `python -m pytest .claudedirector/tests/regression/p0_blocking/test_context7_utilization_p0.py`
   - Address all P0 test failures before proceeding with development"""

        report_content += f"""

## Next Review
**Scheduled**: {datetime.now().strftime("%Y-%m-%d")} (Daily monitoring required)
"""

        with open(report_file, "w") as f:
            f.write(report_content)

        print(f"📊 Compliance report generated: {report_file}")


def main():
    """Main execution function"""
    enforcer = P0CriticalFeatureEnforcer()

    try:
        is_compliant = enforcer.enforce_p0_critical_features()
        enforcer.save_enforcement_results()
        enforcer.generate_compliance_report()

        # Exit with appropriate code
        sys.exit(0 if is_compliant else 1)

    except Exception as e:
        print(f"🚨 P0 ENFORCEMENT ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
