#!/usr/bin/env python3
"""
🚨 CURSOR/CLAUDE HARD ENFORCEMENT SYSTEM
ZERO TOLERANCE - ZERO BYPASS - ZERO EXCEPTIONS

🧠 SEQUENTIAL THINKING METHODOLOGY APPLIED:

🎯 Problem Definition:
Need technical enforcement system that FORCES Cursor and Claude to comply with
established development policies before ANY code generation or file operations.

🔍 Root Cause Analysis:
The 5 systematic process failures occur because policy-based approaches are
ignored. Only technical enforcement that blocks operations until compliance
can prevent these recurring failures.

🏗️ Solution Architecture:
Hard enforcement system that intercepts Cursor/Claude operations and blocks
them until spec-kit, Sequential Thinking, Context7, SOLID/DRY compliance achieved.

⚡ Implementation Strategy:
1. Create enforcement engine that validates all requirements
2. Block Cursor/Claude operations until full compliance
3. Provide clear feedback on violations and required fixes
4. Zero bypass options - technical constraints only
5. Real-time monitoring and immediate blocking

📈 Strategic Enhancement:
Technical enforcement eliminates the 5 systematic failures through constraint-based
compliance rather than relying on policy adherence.

📊 Success Metrics:
- 0% policy violations (100% compliance through technical blocking)
- Zero systematic process failures
- Complete elimination of non-compliant work

This system FORCES Cursor and Claude to comply with:
- Spec-kit format for all specifications
- Sequential Thinking methodology for all development
- Context7 enhancement for strategic work
- DRY and SOLID principles for all code
- PROJECT_STRUCTURE.md compliance for file placement
- BLOAT_PREVENTION_SYSTEM.md integration for duplication prevention

🔧 Context7 MCP Integration:
Leverages Context7 architectural patterns for systematic enforcement methodologies
and enterprise-grade compliance validation.

Author: Martin | Platform Architecture
Sequential Thinking Applied | Context7 Enhanced
"""

import os
import sys
import json
import time
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import yaml
import re


class ComplianceLevel(Enum):
    """Compliance requirement levels"""

    MANDATORY = "MANDATORY"  # BLOCKS ALL OPERATIONS
    CRITICAL = "CRITICAL"  # BLOCKS COMMITS
    WARNING = "WARNING"  # LOGS BUT ALLOWS


@dataclass
class ComplianceViolation:
    """Represents a compliance violation"""

    rule: str
    level: ComplianceLevel
    message: str
    file_path: Optional[str] = None
    remediation: List[str] = None


@dataclass
class EnforcementResult:
    """Result of enforcement validation"""

    passed: bool
    violations: List[ComplianceViolation]
    execution_time_ms: float
    remediation_required: bool = False


class CursorClaudeHardEnforcer:
    """
    🚨 HARD ENFORCEMENT SYSTEM

    BLOCKS Cursor/Claude operations until FULL compliance achieved.
    NO BYPASS OPTIONS - NO EXCEPTIONS - NO WORKAROUNDS
    """

    def __init__(self):
        self.project_root = Path.cwd()
        self.enforcement_log = (
            self.project_root / ".claudedirector" / "logs" / "enforcement.log"
        )
        self.enforcement_log.parent.mkdir(parents=True, exist_ok=True)

        # Load PROJECT_STRUCTURE.md requirements
        self.project_structure = self._load_project_structure()

        # Load BLOAT_PREVENTION_SYSTEM.md requirements
        self.bloat_prevention = self._load_bloat_prevention_config()

        # Spec-kit template path
        self.spec_kit_template = (
            self.project_root / ".claudedirector" / "templates" / "spec-kit-template.md"
        )

    def enforce_hard_compliance(
        self, operation: str, context: Dict[str, Any]
    ) -> EnforcementResult:
        """
        🚨 HARD ENFORCEMENT ENTRY POINT

        BLOCKS ALL OPERATIONS until compliance achieved.
        Returns EnforcementResult with violations and remediation steps.
        """
        start_time = time.time()
        violations = []

        self._log_enforcement_event("HARD_ENFORCEMENT_START", operation, context)

        # MANDATORY COMPLIANCE CHECKS (BLOCKING)
        violations.extend(self._check_spec_kit_compliance(context))
        violations.extend(self._check_sequential_thinking_compliance(context))
        violations.extend(self._check_context7_compliance(context))
        violations.extend(self._check_solid_dry_compliance(context))
        violations.extend(self._check_project_structure_compliance(context))
        violations.extend(self._check_bloat_prevention_compliance(context))
        violations.extend(self._check_p0_protection_compliance(context))

        # Calculate execution time
        execution_time_ms = (time.time() - start_time) * 1000

        # Determine if operation should be blocked
        blocking_violations = [
            v for v in violations if v.level == ComplianceLevel.MANDATORY
        ]
        passed = len(blocking_violations) == 0

        result = EnforcementResult(
            passed=passed,
            violations=violations,
            execution_time_ms=execution_time_ms,
            remediation_required=not passed,
        )

        self._log_enforcement_result(operation, result)

        return result

    def _check_spec_kit_compliance(
        self, context: Dict[str, Any]
    ) -> List[ComplianceViolation]:
        """🚨 MANDATORY: All specifications must use spec-kit format"""
        violations = []

        # Check if creating/editing specification files
        files = context.get("files", [])
        for file_path in files:
            if self._is_specification_file(file_path):
                if not self._validates_spec_kit_format(file_path):
                    violations.append(
                        ComplianceViolation(
                            rule="SPEC_KIT_FORMAT_MANDATORY",
                            level=ComplianceLevel.MANDATORY,
                            message=f"Specification file {file_path} must use spec-kit format",
                            file_path=file_path,
                            remediation=[
                                f"Use template: {self.spec_kit_template}",
                                "Include all required sections: Input, User Scenarios, Functional Requirements, etc.",
                                "Follow executable specification format",
                                "Include SOLID/DRY compliance sections",
                                "Add PROJECT_STRUCTURE.md compliance validation",
                            ],
                        )
                    )

        return violations

    def _check_sequential_thinking_compliance(
        self, context: Dict[str, Any]
    ) -> List[ComplianceViolation]:
        """🚨 MANDATORY: All development must use Sequential Thinking methodology"""
        violations = []

        # Check for development activity without Sequential Thinking
        if self._is_development_activity(context):
            if not self._has_sequential_thinking_documentation(context):
                violations.append(
                    ComplianceViolation(
                        rule="SEQUENTIAL_THINKING_MANDATORY",
                        level=ComplianceLevel.MANDATORY,
                        message="Development activity requires Sequential Thinking methodology",
                        remediation=[
                            "Apply 6-step Sequential Thinking methodology:",
                            "1. Problem Definition - Clear articulation of issue",
                            "2. Root Cause Analysis - Systematic investigation",
                            "3. Solution Architecture - Comprehensive design",
                            "4. Implementation Strategy - Detailed execution plan",
                            "5. Strategic Enhancement - Business impact analysis",
                            "6. Success Metrics - Measurable validation criteria",
                            "Document all steps before proceeding with development",
                        ],
                    )
                )

        return violations

    def _check_context7_compliance(
        self, context: Dict[str, Any]
    ) -> List[ComplianceViolation]:
        """🚨 MANDATORY: Strategic work must use Context7 enhancement"""
        violations = []

        if self._is_strategic_work(context):
            if not self._has_context7_enhancement(context):
                violations.append(
                    ComplianceViolation(
                        rule="CONTEXT7_ENHANCEMENT_MANDATORY",
                        level=ComplianceLevel.MANDATORY,
                        message="Strategic work requires Context7 enhancement",
                        remediation=[
                            "Apply Context7 enhancement for strategic analysis",
                            "Use architectural patterns and best practices",
                            "Leverage framework integration capabilities",
                            "Include strategic context and business impact",
                            "Document Context7 enhancement in specification",
                        ],
                    )
                )

        return violations

    def _check_solid_dry_compliance(
        self, context: Dict[str, Any]
    ) -> List[ComplianceViolation]:
        """🚨 MANDATORY: All code must follow SOLID and DRY principles"""
        violations = []

        files = context.get("files", [])
        for file_path in files:
            if self._is_python_file(file_path):
                solid_violations = self._check_solid_principles(file_path)
                dry_violations = self._check_dry_principle(file_path)
                violations.extend(solid_violations)
                violations.extend(dry_violations)

        return violations

    def _check_project_structure_compliance(
        self, context: Dict[str, Any]
    ) -> List[ComplianceViolation]:
        """🚨 MANDATORY: All files must comply with PROJECT_STRUCTURE.md"""
        violations = []

        files = context.get("files", [])
        for file_path in files:
            if not self._validates_project_structure(file_path):
                violations.append(
                    ComplianceViolation(
                        rule="PROJECT_STRUCTURE_MANDATORY",
                        level=ComplianceLevel.MANDATORY,
                        message=f"File {file_path} violates PROJECT_STRUCTURE.md requirements",
                        file_path=file_path,
                        remediation=[
                            "Place files according to PROJECT_STRUCTURE.md:",
                            "- Core system files: .claudedirector/lib/",
                            "- Tests: .claudedirector/tests/",
                            "- Tools: .claudedirector/tools/",
                            "- Config: .claudedirector/config/",
                            "- Templates: .claudedirector/templates/",
                            "- Documentation: docs/",
                            "- User workspace: leadership-workspace/",
                        ],
                    )
                )

        return violations

    def _check_bloat_prevention_compliance(
        self, context: Dict[str, Any]
    ) -> List[ComplianceViolation]:
        """🚨 MANDATORY: Must integrate with BLOAT_PREVENTION_SYSTEM.md"""
        violations = []

        if self._is_code_reduction_effort(context):
            net_reduction = self._calculate_net_code_reduction(context)
            if net_reduction <= 0:
                violations.append(
                    ComplianceViolation(
                        rule="BLOAT_PREVENTION_MANDATORY",
                        level=ComplianceLevel.MANDATORY,
                        message=f"Code reduction effort shows net addition of {abs(net_reduction)} lines",
                        remediation=[
                            "Achieve net code reduction in bloat elimination efforts",
                            "Follow BLOAT_PREVENTION_SYSTEM.md guidelines",
                            "Use MCP-Enhanced duplication detection",
                            "Apply systematic consolidation strategies",
                            "Validate with pre-commit bloat prevention hooks",
                        ],
                    )
                )

        return violations

    def _check_p0_protection_compliance(
        self, context: Dict[str, Any]
    ) -> List[ComplianceViolation]:
        """🚨 MANDATORY: P0 tests must remain at 39/39 passing"""
        violations = []

        # Run P0 test check
        p0_status = self._check_p0_test_status()
        if not p0_status["all_passing"]:
            violations.append(
                ComplianceViolation(
                    rule="P0_PROTECTION_MANDATORY",
                    level=ComplianceLevel.MANDATORY,
                    message=f"P0 tests failing: {p0_status['failing_count']}/{p0_status['total_count']}",
                    remediation=[
                        "Fix all failing P0 tests immediately",
                        "Run: python .claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py",
                        "P0 tests are business-critical and cannot be deferred",
                        "All development stops until 39/39 P0 tests pass",
                    ],
                )
            )

        return violations

    def block_operation_with_message(
        self, result: EnforcementResult, operation: str
    ) -> None:
        """
        🚨 BLOCK OPERATION WITH DETAILED MESSAGE

        Displays comprehensive compliance violations and remediation steps.
        """
        print("\n" + "=" * 80)
        print("🚨 CURSOR/CLAUDE HARD ENFORCEMENT - OPERATION BLOCKED")
        print("=" * 80)
        print(f"Operation: {operation}")
        print(f"Violations: {len(result.violations)}")
        print(f"Validation Time: {result.execution_time_ms:.1f}ms")
        print("\n🚫 COMPLIANCE VIOLATIONS:")

        for i, violation in enumerate(result.violations, 1):
            print(f"\n{i}. {violation.rule} ({violation.level.value})")
            print(f"   📄 {violation.message}")
            if violation.file_path:
                print(f"   📁 File: {violation.file_path}")
            if violation.remediation:
                print(f"   🔧 Remediation:")
                for step in violation.remediation:
                    print(f"      • {step}")

        print("\n" + "=" * 80)
        print("🛑 OPERATION BLOCKED UNTIL ALL VIOLATIONS RESOLVED")
        print("=" * 80)
        print("NO BYPASS OPTIONS - NO EXCEPTIONS - NO WORKAROUNDS")
        print("Fix all violations above before proceeding.")
        print("=" * 80 + "\n")

    def _is_specification_file(self, file_path: str) -> bool:
        """Check if file is a specification document"""
        spec_patterns = ["-spec.md", "-specification.md", "spec.md", "specification.md"]
        return any(pattern in file_path.lower() for pattern in spec_patterns)

    def _validates_spec_kit_format(self, file_path: str) -> bool:
        """Validate file follows spec-kit format"""
        if not Path(file_path).exists():
            return False

        try:
            with open(file_path, "r") as f:
                content = f.read()

            # Check for required spec-kit sections
            required_sections = [
                "## Input",
                "## User Scenarios & Testing",
                "## Functional Requirements",
                "## Technical Requirements",
                "## Success Metrics",
                "## Execution Flow (main)",
            ]

            return all(section in content for section in required_sections)
        except:
            return False

    def _is_development_activity(self, context: Dict[str, Any]) -> bool:
        """Check if this is development activity requiring Sequential Thinking"""
        files = context.get("files", [])
        return any(
            file_path.endswith(".py")
            or file_path.endswith(".md")
            or "implementation" in file_path.lower()
            or "development" in file_path.lower()
            for file_path in files
        )

    def _has_sequential_thinking_documentation(self, context: Dict[str, Any]) -> bool:
        """Check if Sequential Thinking methodology is documented"""
        # Look for Sequential Thinking indicators in context or related files
        description = context.get("description", "")
        return "🧠 Sequential Thinking Applied" in description

    def _is_strategic_work(self, context: Dict[str, Any]) -> bool:
        """Check if this is strategic work requiring Context7"""
        description = context.get("description", "").lower()
        strategic_keywords = [
            "strategic",
            "framework",
            "architecture",
            "organizational",
            "executive",
            "business impact",
            "stakeholder",
            "platform",
        ]
        return any(keyword in description for keyword in strategic_keywords)

    def _has_context7_enhancement(self, context: Dict[str, Any]) -> bool:
        """Check if Context7 enhancement is applied"""
        description = context.get("description", "")
        return "🔧 Context7 Enhanced" in description

    def _is_python_file(self, file_path: str) -> bool:
        """Check if file is Python code"""
        return file_path.endswith(".py")

    def _check_solid_principles(self, file_path: str) -> List[ComplianceViolation]:
        """Check SOLID principle compliance"""
        violations = []

        if not Path(file_path).exists():
            return violations

        try:
            with open(file_path, "r") as f:
                content = f.read()

            # Simple heuristic checks for SOLID violations
            lines = content.split("\n")

            # Check for large classes (Single Responsibility violation)
            class_line_counts = self._count_class_lines(content)
            for class_name, line_count in class_line_counts.items():
                if line_count > 200:  # Arbitrary threshold
                    violations.append(
                        ComplianceViolation(
                            rule="SOLID_SINGLE_RESPONSIBILITY",
                            level=ComplianceLevel.MANDATORY,
                            message=f"Class {class_name} has {line_count} lines (>200), likely violates Single Responsibility",
                            file_path=file_path,
                            remediation=[
                                "Break large class into smaller, focused classes",
                                "Each class should have one reason to change",
                                "Use composition over inheritance",
                                "Extract related functionality into separate classes",
                            ],
                        )
                    )

        except Exception as e:
            # Don't block on parsing errors, but log them
            self._log_enforcement_event(
                "SOLID_CHECK_ERROR", str(e), {"file": file_path}
            )

        return violations

    def _check_dry_principle(self, file_path: str) -> List[ComplianceViolation]:
        """Check DRY principle compliance"""
        violations = []

        if not Path(file_path).exists():
            return violations

        try:
            with open(file_path, "r") as f:
                content = f.read()

            # Check for duplicate string literals
            string_literals = re.findall(r'"([^"]{10,})"', content)  # Strings 10+ chars
            string_counts = {}
            for literal in string_literals:
                string_counts[literal] = string_counts.get(literal, 0) + 1

            for literal, count in string_counts.items():
                if count > 2:  # More than 2 occurrences
                    violations.append(
                        ComplianceViolation(
                            rule="DRY_PRINCIPLE_VIOLATION",
                            level=ComplianceLevel.MANDATORY,
                            message=f"String literal '{literal}' repeated {count} times",
                            file_path=file_path,
                            remediation=[
                                "Extract repeated strings to constants",
                                "Use configuration files for repeated values",
                                "Create single source of truth for common strings",
                                "Consider using enums for repeated string values",
                            ],
                        )
                    )

        except Exception as e:
            self._log_enforcement_event("DRY_CHECK_ERROR", str(e), {"file": file_path})

        return violations

    def _validates_project_structure(self, file_path: str) -> bool:
        """Check if file placement follows PROJECT_STRUCTURE.md"""
        # Define valid paths according to PROJECT_STRUCTURE.md
        valid_paths = [
            ".claudedirector/lib/",
            ".claudedirector/tests/",
            ".claudedirector/tools/",
            ".claudedirector/config/",
            ".claudedirector/templates/",
            "docs/",
            "leadership-workspace/",
            "README.md",
            "requirements.txt",
            "bin/",
            "data/",
            "venv/",
        ]

        return any(file_path.startswith(path) for path in valid_paths)

    def _is_code_reduction_effort(self, context: Dict[str, Any]) -> bool:
        """Check if this is a code reduction/bloat elimination effort"""
        description = context.get("description", "").lower()
        reduction_keywords = [
            "bloat elimination",
            "code reduction",
            "consolidation",
            "eliminate duplication",
            "reduce lines",
            "cleanup",
        ]
        return any(keyword in description for keyword in reduction_keywords)

    def _calculate_net_code_reduction(self, context: Dict[str, Any]) -> int:
        """Calculate net code reduction (negative = net addition)"""
        # This would integrate with git diff or file analysis
        # For now, return 0 to trigger validation in actual implementation
        return context.get("net_line_change", 0)

    def _check_p0_test_status(self) -> Dict[str, Any]:
        """Check P0 test status"""
        try:
            result = subprocess.run(
                [
                    "python",
                    ".claudedirector/tests/p0_enforcement/run_mandatory_p0_tests.py",
                ],
                capture_output=True,
                text=True,
                timeout=60,
            )

            # Parse output for test results
            output = result.stdout
            if "SUCCESS RATE: 39/39" in output:
                return {"all_passing": True, "total_count": 39, "failing_count": 0}
            else:
                return {
                    "all_passing": False,
                    "total_count": 39,
                    "failing_count": 1,  # Simplified - would parse actual count
                }

        except Exception as e:
            self._log_enforcement_event("P0_CHECK_ERROR", str(e), {})
            return {
                "all_passing": False,
                "total_count": 39,
                "failing_count": 1,
                "error": str(e),
            }

    def _count_class_lines(self, content: str) -> Dict[str, int]:
        """Count lines per class for SOLID validation"""
        class_counts = {}
        lines = content.split("\n")
        current_class = None
        class_start_line = 0

        for i, line in enumerate(lines):
            if line.strip().startswith("class "):
                if current_class:
                    class_counts[current_class] = i - class_start_line

                class_match = re.match(r"class\s+(\w+)", line.strip())
                if class_match:
                    current_class = class_match.group(1)
                    class_start_line = i

        # Handle last class
        if current_class:
            class_counts[current_class] = len(lines) - class_start_line

        return class_counts

    def _load_project_structure(self) -> Dict[str, Any]:
        """Load PROJECT_STRUCTURE.md requirements"""
        # This would parse PROJECT_STRUCTURE.md for validation rules
        return {
            "core_lib_path": ".claudedirector/lib/",
            "tests_path": ".claudedirector/tests/",
            "tools_path": ".claudedirector/tools/",
            "docs_path": "docs/",
            "workspace_path": "leadership-workspace/",
        }

    def _load_bloat_prevention_config(self) -> Dict[str, Any]:
        """Load BLOAT_PREVENTION_SYSTEM.md configuration"""
        # This would parse BLOAT_PREVENTION_SYSTEM.md for rules
        return {
            "similarity_threshold": 0.75,
            "min_duplicate_lines": 10,
            "enable_mcp_analysis": True,
        }

    def _log_enforcement_event(
        self, event_type: str, message: str, context: Dict[str, Any]
    ) -> None:
        """Log enforcement events for audit trail"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "message": message,
            "context": context,
        }

        try:
            with open(self.enforcement_log, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Warning: Could not write to enforcement log: {e}")

    def _log_enforcement_result(
        self, operation: str, result: EnforcementResult
    ) -> None:
        """Log enforcement result for audit trail"""
        self._log_enforcement_event(
            "ENFORCEMENT_RESULT",
            f"Operation: {operation}, Passed: {result.passed}, Violations: {len(result.violations)}",
            {
                "operation": operation,
                "passed": result.passed,
                "violation_count": len(result.violations),
                "execution_time_ms": result.execution_time_ms,
            },
        )


def main():
    """CLI entry point for manual enforcement validation"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Cursor/Claude Hard Enforcement System"
    )
    parser.add_argument("operation", help="Operation being attempted")
    parser.add_argument("--files", nargs="*", help="Files being modified")
    parser.add_argument("--description", help="Description of the operation")

    args = parser.parse_args()

    enforcer = CursorClaudeHardEnforcer()

    context = {"files": args.files or [], "description": args.description or ""}

    result = enforcer.enforce_hard_compliance(args.operation, context)

    if not result.passed:
        enforcer.block_operation_with_message(result, args.operation)
        sys.exit(1)
    else:
        print(f"✅ COMPLIANCE VALIDATED: {args.operation}")
        print(f"   Execution time: {result.execution_time_ms:.1f}ms")
        sys.exit(0)


if __name__ == "__main__":
    main()
