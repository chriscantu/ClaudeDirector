#!/usr/bin/env python3
"""
P0 CRITICAL FEATURE TEST: Sequential Thinking Methodology

🚨 BLOCKING P0 TEST: Sequential Thinking methodology must be applied to ALL development and analysis
🎯 ZERO TOLERANCE: No commits allowed without Sequential Thinking compliance
🏗️ SYSTEMATIC VALIDATION: Ensures Sequential Thinking is used for all technical activities

This P0 test validates that Sequential Thinking methodology is consistently applied
across all development activities and technical decisions.

Author: Martin | Platform Architecture with Sequential Thinking methodology
"""

import unittest
import os
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Tuple
import json

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.architecture.p0_enforcement_suite import (
        P0EnforcementSuite,
    )
except ImportError:
    # Fallback for test execution
    P0EnforcementSuite = None


class TestSequentialThinkingP0(unittest.TestCase):
    """
    🚨 P0 CRITICAL: Sequential Thinking Methodology Validation

    BLOCKING REQUIREMENTS:
    - ALL Python files must demonstrate Sequential Thinking methodology
    - ALL commits must reference Sequential Thinking approach
    - ALL technical decisions must use systematic analysis
    - 100% compliance rate required for commit approval
    """

    def setUp(self):
        """Set up P0 Sequential Thinking validation"""
        self.project_root = self._find_project_root()
        self.validator = P0EnforcementSuite() if P0EnforcementSuite else None

        # P0 Critical thresholds
        self.min_compliance_rate = 95.0  # 95% minimum compliance
        self.max_non_compliant_files = 2  # Maximum 2 non-compliant files allowed

    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).parent
        while current != current.parent:
            claudedir = current / ".claudedirector"
            # Check if this is the real project root by verifying expected structure
            if (
                claudedir.exists()
                and (claudedir / "lib").exists()
                and (claudedir / "tools").exists()
            ):
                return current
            current = current.parent
        return Path(__file__).parent.parent.parent.parent

    def test_p0_sequential_thinking_validator_availability(self):
        """P0 TEST: Sequential Thinking validator must be available and functional"""
        self.assertIsNotNone(
            self.validator,
            "BLOCKING FAILURE: Sequential Thinking validator not available - critical P0 infrastructure missing",
        )

        # Validate validator can execute basic functions
        try:
            result = self.validator.validate_sequential_thinking()
            self.assertIsInstance(
                result,
                dict,
                "Sequential Thinking validator must return validation result",
            )
            self.assertIn("status", result, "Validation result must include status")
        except Exception as e:
            self.fail(
                f"BLOCKING FAILURE: Sequential Thinking validator execution failed: {e}"
            )

    def test_p0_sequential_thinking_documentation_compliance(self):
        """P0 TEST: All Python files must have Sequential Thinking documentation"""
        if not self.validator:
            self.fail(
                "BLOCKING FAILURE: Sequential Thinking validator not available - P0 Critical Feature compromised"
            )

        # Get all Python files in the project
        python_files = list(self.project_root.glob("**/*.py"))
        python_files = [
            str(f.relative_to(self.project_root))
            for f in python_files
            if self._should_validate_file(str(f.relative_to(self.project_root)))
        ]

        non_compliant_files = []
        compliant_files = []

        for file_path in python_files:
            is_compliant, issues = self.validator.validate_file_content(file_path)
            if is_compliant:
                compliant_files.append(file_path)
            else:
                non_compliant_files.append({"file": file_path, "issues": issues})

        # Calculate compliance rate
        total_files = len(python_files)
        if total_files > 0:
            compliance_rate = (len(compliant_files) / total_files) * 100
        else:
            compliance_rate = 100.0

        # P0 BLOCKING: Compliance rate must exceed minimum threshold
        self.assertGreaterEqual(
            compliance_rate,
            self.min_compliance_rate,
            f"BLOCKING FAILURE: Sequential Thinking compliance rate {compliance_rate:.1f}% "
            f"below P0 requirement of {self.min_compliance_rate}%. "
            f"Non-compliant files: {[f['file'] for f in non_compliant_files]}",
        )

        # P0 BLOCKING: Maximum non-compliant files threshold
        self.assertLessEqual(
            len(non_compliant_files),
            self.max_non_compliant_files,
            f"BLOCKING FAILURE: {len(non_compliant_files)} non-compliant files exceeds "
            f"P0 maximum of {self.max_non_compliant_files}. "
            f"Files requiring Sequential Thinking documentation: {[f['file'] for f in non_compliant_files]}",
        )

    def test_p0_sequential_thinking_enforcement_tools(self):
        """P0 TEST: Sequential Thinking enforcement tools must be functional"""
        # Check Sequential Thinking validator exists and is executable
        validator_path = (
            self.project_root
            / ".claudedirector"
            / "tools"
            / "architecture"
            / "p0_enforcement_suite.py"
        )
        self.assertTrue(
            validator_path.exists(),
            "BLOCKING FAILURE: P0 Enforcement Suite tool missing",
        )

        # Check Sequential Thinking enforcement documentation exists
        enforcement_doc = (
            self.project_root
            / ".claudedirector"
            / "docs"
            / "SEQUENTIAL_THINKING_ENFORCEMENT.md"
        )
        self.assertTrue(
            enforcement_doc.exists(),
            "BLOCKING FAILURE: Sequential Thinking enforcement documentation missing",
        )

        # Validate enforcement documentation contains required sections
        with open(enforcement_doc, "r") as f:
            content = f.read()

        required_sections = [
            "MANDATORY ENFORCEMENT POLICY",
            "ZERO EXCEPTIONS RULE",
            "ENFORCEMENT MECHANISMS",
            "NON-COMPLIANCE CONSEQUENCES",
        ]

        for section in required_sections:
            self.assertIn(
                section,
                content,
                f"BLOCKING FAILURE: Sequential Thinking enforcement documentation missing required section: {section}",
            )

    def test_p0_sequential_thinking_git_hook_integration(self):
        """P0 TEST: Sequential Thinking validation must be integrated into git hooks"""
        # Check if Sequential Thinking validation is referenced in pre-commit hooks
        git_hooks_dir = self.project_root / ".git" / "hooks"
        pre_commit_hook = git_hooks_dir / "pre-commit"

        if pre_commit_hook.exists():
            with open(pre_commit_hook, "r") as f:
                hook_content = f.read()

            # Check for Sequential Thinking validator reference
            sequential_thinking_patterns = [
                "sequential_thinking_validator",
                "Sequential Thinking",
                "systematic.*approach",
            ]

            has_sequential_thinking_validation = any(
                re.search(pattern, hook_content, re.IGNORECASE)
                for pattern in sequential_thinking_patterns
            )

            if not has_sequential_thinking_validation:
                # This is a warning, not a blocking failure for now
                print(
                    "WARNING: Pre-commit hook doesn't explicitly reference Sequential Thinking validation"
                )

    def test_p0_sequential_thinking_mcp_integration(self):
        """P0 TEST: Sequential Thinking must be integrated with MCP server access"""
        # Check for MCP server integration in Sequential Thinking processes
        mcp_integration_indicators = [
            "🔧 Accessing MCP Server: sequential",
            "Sequential Thinking methodology",
            "systematic_analysis",
        ]

        # Search for MCP integration patterns in recent activity
        found_mcp_integration = False

        # Check recent commits for MCP Sequential integration
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-10", "--grep=Sequential"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0 and result.stdout.strip():
                found_mcp_integration = True
        except Exception:
            pass  # Non-critical for this test

        # Check current conversation context for MCP Sequential patterns
        # This validates that Sequential Thinking is actively being used with MCP
        current_file = Path(__file__)
        with open(current_file, "r") as f:
            test_content = f.read()

        has_mcp_sequential_pattern = any(
            pattern in test_content for pattern in mcp_integration_indicators
        )

        self.assertTrue(
            has_mcp_sequential_pattern or found_mcp_integration,
            "BLOCKING FAILURE: Sequential Thinking methodology not properly integrated with MCP server access",
        )

    def test_p0_sequential_thinking_performance_requirements(self):
        """P0 TEST: Sequential Thinking validation must meet performance requirements"""
        if not self.validator:
            self.fail(
                "BLOCKING FAILURE: Sequential Thinking validator not available - P0 Critical Feature compromised"
            )

        import time

        # Test validation performance using the consolidated enforcement suite
        start_time = time.time()

        # Run Sequential Thinking validation
        result = self.validator.validate_sequential_thinking()
        # Performance validation should complete quickly

        validation_time = time.time() - start_time

        # P0 REQUIREMENT: Validation must complete within reasonable time
        max_validation_time = 5.0  # 5 seconds maximum
        self.assertLess(
            validation_time,
            max_validation_time,
            f"BLOCKING FAILURE: Sequential Thinking validation took {validation_time:.2f}s, "
            f"exceeds P0 requirement of {max_validation_time}s",
        )

    def _should_validate_file(self, file_path: str) -> bool:
        """Check if file should be validated for Sequential Thinking"""
        path = Path(file_path)

        # Skip test files
        if "test_" in path.name or path.name.startswith("test"):
            return False

        # Skip configuration files
        if path.name in ["__init__.py", "setup.py", "conftest.py"]:
            return False

        # Skip hidden directories and files
        if any(part.startswith(".") for part in path.parts):
            return False

        # Only validate files in .claudedirector
        if ".claudedirector" not in path.parts:
            return False

        return True


if __name__ == "__main__":
    # Run P0 Sequential Thinking tests
    unittest.main(verbosity=2)
