#!/usr/bin/env python3
"""
Integration Test: Weekly Report Cursor Command

TESTING SCOPE:
✅ Command file exists and is properly formatted
✅ Command documentation is complete and follows pattern
✅ Command integration with weekly reporter system
✅ Architecture compliance (PROJECT_STRUCTURE.md, BLOAT_PREVENTION_SYSTEM.md)

ARCHITECTURAL COMPLIANCE:
- Follows TESTING_ARCHITECTURE.md integration test patterns
- Validates cursor command structure consistency
- Ensures proper documentation and usage examples
- Adheres to PROJECT_STRUCTURE.md placement requirements

Author: Martin (Platform Architecture)
"""

import sys
import unittest
import os
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path for imports - following existing integration test patterns
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
lib_path = str(PROJECT_ROOT / ".claudedirector" / "lib")

# Robust import strategy - ensure lib path is first in sys.path (DRY: reuse existing pattern)
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
elif sys.path.index(lib_path) != 0:
    sys.path.remove(lib_path)
    sys.path.insert(0, lib_path)


class TestWeeklyReportCursorCommand(unittest.TestCase):
    """
    Integration Tests for /generate-weekly-report Cursor Command

    BUSINESS REQUIREMENTS:
    - Command file must exist in .cursor/commands/
    - Command must follow established cursor command pattern
    - Command must document expected behavior
    - Command must reference existing weekly_reporter.py implementation
    - Command must include architecture compliance checklist
    - Command must document all command variations
    """

    # SOLID: Single Responsibility - Configuration constants separated
    COMMAND_FILE_PATH = (
        PROJECT_ROOT / ".cursor" / "commands" / "generate-weekly-report.md"
    )
    WEEKLY_REPORTER_PATH = (
        PROJECT_ROOT / ".claudedirector" / "lib" / "reporting" / "weekly_reporter.py"
    )

    REQUIRED_SECTIONS = {
        "title": {
            "pattern": "# Generate Weekly Report Command",
            "description": "Command title section",
            "required": True,
        },
        "instructions": {
            "pattern": "## Instructions for Claude:",
            "description": "Instructions for AI processing",
            "required": True,
        },
        "expected_behavior": {
            "pattern": "## Expected Behavior:",
            "description": "Expected command behavior",
            "required": True,
        },
        "command_variations": {
            "pattern": "## Command Variations:",
            "description": "Command usage variations",
            "required": True,
        },
        "architecture_compliance": {
            "pattern": "## Architecture Compliance:",
            "description": "Architecture compliance checklist",
            "required": True,
        },
    }

    REQUIRED_BEHAVIORS = {
        "cli_execution": {
            "pattern": "Direct CLI execution without code generation",
            "description": "Native CLI execution pattern",
            "required": True,
        },
        "jira_fetch": {
            "pattern": "Fetch live Jira data",
            "description": "Live data fetching capability",
            "required": True,
        },
        "mcp_enhancement": {
            "pattern": "MCP-enhanced analysis",
            "description": "MCP integration for strategic insights",
            "required": True,
        },
        "report_save": {
            "pattern": "Save report to leadership-workspace/reports/",
            "description": "Automatic report persistence",
            "required": True,
        },
    }

    REQUIRED_VARIATIONS = {
        "standard": {
            "pattern": "python .claudedirector/lib/reporting/weekly_reporter.py",
            "description": "Standard report generation command",
            "required": True,
        },
        "dry_run": {
            "pattern": "--dry-run",
            "description": "Dry run mode for testing",
            "required": True,
        },
        "custom_output": {
            "pattern": "--output",
            "description": "Custom output path option",
            "required": True,
        },
        "debug": {
            "pattern": "--debug",
            "description": "Debug mode with verbose logging",
            "required": True,
        },
    }

    ARCHITECTURE_COMPLIANCE_CHECKS = {
        "project_structure": {
            "pattern": "PROJECT_STRUCTURE.md",
            "description": "PROJECT_STRUCTURE.md compliance check",
            "required": True,
        },
        "bloat_prevention": {
            "pattern": "BLOAT_PREVENTION_SYSTEM.md",
            "description": "BLOAT_PREVENTION_SYSTEM.md compliance check",
            "required": True,
        },
        "native_execution": {
            "pattern": "Native execution",
            "description": "Native CLI execution requirement",
            "required": True,
        },
        "mcp_integration": {
            "pattern": "MCP Integration",
            "description": "MCP integration documentation",
            "required": True,
        },
    }

    def setUp(self):
        """Set up test environment"""
        self.command_content = None

        # Load command file content once for all tests (DRY principle)
        try:
            self.command_content = self._load_command_content()
        except Exception as e:
            self.fail(f"CRITICAL FAILURE: Cannot load command file: {e}")

    def _load_command_content(self) -> str:
        """
        Load command file content

        ARCHITECTURAL COMPLIANCE:
        - DRY: Single method for file loading
        - Error handling: Clear error messages
        - Performance: Single file read per test run
        """
        if not self.COMMAND_FILE_PATH.exists():
            raise FileNotFoundError(f"Command file not found: {self.COMMAND_FILE_PATH}")

        with open(self.COMMAND_FILE_PATH, "r", encoding="utf-8") as f:
            return f.read()

    def test_command_file_exists(self):
        """Test: Command file exists in correct location"""
        self.assertTrue(
            self.COMMAND_FILE_PATH.exists(),
            f"Command file must exist at: {self.COMMAND_FILE_PATH}",
        )

    def test_command_file_readable(self):
        """Test: Command file is readable and has content"""
        self.assertIsNotNone(
            self.command_content, "Command file content must be readable"
        )
        self.assertGreater(
            len(self.command_content), 0, "Command file must not be empty"
        )

    def test_required_sections_present(self):
        """Test: All required sections are present in command file"""
        missing_sections = []

        for section_name, section_config in self.REQUIRED_SECTIONS.items():
            if section_config["required"]:
                if section_config["pattern"] not in self.command_content:
                    missing_sections.append(
                        f"{section_name}: {section_config['description']}"
                    )

        self.assertEqual(
            len(missing_sections),
            0,
            f"Missing required sections:\n"
            + "\n".join(f"  - {s}" for s in missing_sections),
        )

    def test_expected_behaviors_documented(self):
        """Test: All expected behaviors are documented"""
        missing_behaviors = []

        for behavior_name, behavior_config in self.REQUIRED_BEHAVIORS.items():
            if behavior_config["required"]:
                if behavior_config["pattern"] not in self.command_content:
                    missing_behaviors.append(
                        f"{behavior_name}: {behavior_config['description']}"
                    )

        self.assertEqual(
            len(missing_behaviors),
            0,
            f"Missing required behaviors:\n"
            + "\n".join(f"  - {b}" for b in missing_behaviors),
        )

    def test_command_variations_documented(self):
        """Test: All command variations are documented"""
        missing_variations = []

        for variation_name, variation_config in self.REQUIRED_VARIATIONS.items():
            if variation_config["required"]:
                if variation_config["pattern"] not in self.command_content:
                    missing_variations.append(
                        f"{variation_name}: {variation_config['description']}"
                    )

        self.assertEqual(
            len(missing_variations),
            0,
            f"Missing required command variations:\n"
            + "\n".join(f"  - {v}" for v in missing_variations),
        )

    def test_architecture_compliance_documented(self):
        """Test: Architecture compliance is documented"""
        missing_compliance = []

        for (
            compliance_name,
            compliance_config,
        ) in self.ARCHITECTURE_COMPLIANCE_CHECKS.items():
            if compliance_config["required"]:
                if compliance_config["pattern"] not in self.command_content:
                    missing_compliance.append(
                        f"{compliance_name}: {compliance_config['description']}"
                    )

        self.assertEqual(
            len(missing_compliance),
            0,
            f"Missing architecture compliance documentation:\n"
            + "\n".join(f"  - {c}" for c in missing_compliance),
        )

    def test_weekly_reporter_reference(self):
        """Test: Command references the existing weekly reporter implementation"""
        self.assertIn(
            "weekly_reporter.py",
            self.command_content,
            "Command must reference weekly_reporter.py implementation",
        )

    def test_weekly_reporter_exists(self):
        """Test: Weekly reporter implementation exists"""
        self.assertTrue(
            self.WEEKLY_REPORTER_PATH.exists(),
            f"Weekly reporter must exist at: {self.WEEKLY_REPORTER_PATH}",
        )

    def test_no_code_duplication(self):
        """Test: Command does not duplicate weekly reporter implementation"""
        # Command file should be documentation only, not implementation
        code_indicators = [
            "def generate_report(",
            "class WeeklyReporter",
            "import requests",
            "import jira",
        ]

        found_code = []
        for indicator in code_indicators:
            if indicator in self.command_content:
                found_code.append(indicator)

        self.assertEqual(
            len(found_code),
            0,
            f"Command file should not contain implementation code. Found: {found_code}",
        )

    def test_command_follows_pattern(self):
        """Test: Command follows established cursor command pattern"""
        # Compare structure with daily-plan-start.md pattern
        daily_plan_path = PROJECT_ROOT / ".cursor" / "commands" / "daily-plan-start.md"

        if daily_plan_path.exists():
            with open(daily_plan_path, "r", encoding="utf-8") as f:
                daily_plan_content = f.read()

            # Both should have "Instructions for Claude:" section
            self.assertIn(
                "## Instructions for Claude:",
                daily_plan_content,
                "Reference command (daily-plan-start) should have 'Instructions for Claude:' section",
            )
            self.assertIn(
                "## Instructions for Claude:",
                self.command_content,
                "Weekly report command should follow same pattern as daily-plan-start",
            )


def run_integration_tests():
    """
    Run integration tests for weekly report cursor command

    USAGE:
        python -m pytest .claudedirector/tests/integration/test_weekly_report_cursor_command.py -v
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWeeklyReportCursorCommand)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
