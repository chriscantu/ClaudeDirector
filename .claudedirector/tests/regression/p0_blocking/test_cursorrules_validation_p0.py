#!/usr/bin/env python3
"""
P0 Test: .cursorrules Validation

BUSINESS CRITICAL: .cursorrules file structure and content must be valid
to ensure consistent behavior across Cursor and Claude Code platforms.

ARCHITECTURAL COMPLIANCE:
- Follows TESTING_ARCHITECTURE.md P0 test patterns
- Integrates with unified test runner system
- Validates business-critical .cursorrules functionality
- Adheres to PROJECT_STRUCTURE.md and BLOAT_PREVENTION_SYSTEM.md

Author: Martin (Platform Architecture)
"""

import sys
import unittest
import re
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add project root to path for imports - following existing P0 test patterns
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
lib_path = str(PROJECT_ROOT / ".claudedirector" / "lib")

# Robust import strategy - ensure lib path is first in sys.path (DRY: reuse existing pattern)
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
elif sys.path.index(lib_path) != 0:
    sys.path.remove(lib_path)
    sys.path.insert(0, lib_path)


class CursorrrulesValidationError(Exception):
    """Custom exception for .cursorrules validation errors"""

    pass


class TestCursorrrulesValidationP0(unittest.TestCase):
    """
    P0 Tests for .cursorrules Validation

    BUSINESS CRITICAL REQUIREMENTS:
    - .cursorrules file must exist and be readable
    - All required sections must be present
    - Essential personas must be defined
    - Core frameworks must be documented
    - Required commands must be configured
    - Cross-platform compatibility must be maintained
    - Validation must complete within performance requirements (<5s)
    """

    # SOLID: Single Responsibility - Configuration constants separated
    REQUIRED_SECTIONS = {
        "Strategic Personas": {
            "pattern": r"###?\s*Strategic Personas",
            "description": "Strategic persona definitions",
            "required": True,
        },
        "Strategic Frameworks": {
            "pattern": r"###?\s*Strategic Frameworks",
            "description": "Framework detection configuration",
            "required": True,
        },
        "Context-Aware Activation Rules": {
            "pattern": r"###?\s*Context-Aware Activation Rules",
            "description": "Activation pattern definitions",
            "required": True,
        },
        "Personal Retrospective Commands": {
            "pattern": r"###?\s*Personal Retrospective Commands",
            "description": "Retrospective command definitions",
            "required": True,
        },
        "MCP Integration": {
            "pattern": r"##?\s*.*MCP.*",
            "description": "MCP integration configuration",
            "required": True,
        },
    }

    REQUIRED_PERSONAS = {
        "diego": {
            "pattern": r"\*\*🎯\s*diego\*\*",
            "description": "Engineering leadership persona",
            "emoji": "🎯",
            "required": True,
        },
        "camille": {
            "pattern": r"\*\*📊\s*camille\*\*",
            "description": "Strategic technology persona",
            "emoji": "📊",
            "required": True,
        },
        "rachel": {
            "pattern": r"\*\*🎨\s*rachel\*\*",
            "description": "Design systems strategy persona",
            "emoji": "🎨",
            "required": True,
        },
        "alvaro": {
            "pattern": r"\*\*💼\s*alvaro\*\*",
            "description": "Platform investment persona",
            "emoji": "💼",
            "required": True,
        },
        "martin": {
            "pattern": r"\*\*🏗️\s*martin\*\*",
            "description": "Platform architecture persona",
            "emoji": "🏗️",
            "required": True,
        },
    }

    REQUIRED_FRAMEWORKS = {
        "Team Topologies": {
            "pattern": r"Team Topologies",
            "description": "Team structure and cognitive load management",
            "required": True,
        },
        "Capital Allocation": {
            "pattern": r"Capital Allocation",
            "description": "Engineering investment and ROI analysis",
            "required": True,
        },
        "Crucial Conversations": {
            "pattern": r"Crucial Conversations",
            "description": "High-stakes discussions and stakeholder alignment",
            "required": True,
        },
        "Good Strategy Bad Strategy": {
            "pattern": r"Good Strategy Bad Strategy",
            "description": "Strategy kernel development and fluff detection",
            "required": True,
        },
        "WRAP Framework": {
            "pattern": r"WRAP Framework",
            "description": "Strategic decision-making methodology",
            "required": True,
        },
    }

    REQUIRED_COMMANDS = {
        "/retrospective create": {
            "pattern": r"/retrospective\s+create",
            "description": "Start interactive weekly retrospective",
            "required": True,
        },
        "/retrospective view": {
            "pattern": r"/retrospective\s+view",
            "description": "View recent retrospective entries",
            "required": True,
        },
        "/retrospective help": {
            "pattern": r"/retrospective\s+help",
            "description": "Show retrospective command help",
            "required": True,
        },
        "/generate-weekly-report": {
            "pattern": r"/generate-weekly-report",
            "description": "Generate weekly executive report",
            "required": True,
        },
        "/configure": {
            "pattern": r"/configure",
            "description": "Restart first-run wizard",
            "required": True,
        },
        "/status": {
            "pattern": r"/status",
            "description": "Show current configuration",
            "required": True,
        },
    }

    # Performance requirement from spec
    MAX_VALIDATION_TIME_SECONDS = 5

    def setUp(self):
        """Set up test environment - following existing P0 test patterns"""
        self.cursorrules_path = PROJECT_ROOT / ".cursorrules"
        self.cursorrules_content = None
        self.validation_start_time = None

        # Load .cursorrules content once for all tests (DRY principle)
        try:
            self.cursorrules_content = self._load_cursorrules_content()
        except Exception as e:
            self.fail(f"CRITICAL P0 FAILURE: Cannot load .cursorrules file: {e}")

    def _load_cursorrules_content(self) -> str:
        """
        Load .cursorrules file content

        ARCHITECTURAL COMPLIANCE:
        - DRY: Single method for file loading
        - Error handling: Clear error messages
        - Performance: Single file read per test run
        """
        if not self.cursorrules_path.exists():
            raise CursorrrulesValidationError(
                f".cursorrules file not found at {self.cursorrules_path}"
            )

        try:
            with open(self.cursorrules_path, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.strip():
                raise CursorrrulesValidationError(".cursorrules file is empty")

            return content

        except Exception as e:
            raise CursorrrulesValidationError(f"Failed to read .cursorrules file: {e}")

    def _start_performance_timer(self):
        """Start performance timing for validation"""
        self.validation_start_time = time.time()

    def _check_performance_requirement(self, operation_name: str):
        """Check that operation meets <5 second performance requirement"""
        if self.validation_start_time is None:
            return

        elapsed_time = time.time() - self.validation_start_time
        self.assertLess(
            elapsed_time,
            self.MAX_VALIDATION_TIME_SECONDS,
            f"P0 PERFORMANCE FAILURE: {operation_name} took {elapsed_time:.2f}s, must be <{self.MAX_VALIDATION_TIME_SECONDS}s",
        )

    def _format_validation_error(self, error_type: str, details: List[str]) -> str:
        """
        Format clear, actionable error messages for developers

        SOLID: Single responsibility for error formatting
        DRY: Reusable error formatting across all validation methods
        """
        return f"""
❌ .cursorrules Validation Failed: {error_type}

Issues Found:
{chr(10).join(f'  • {detail}' for detail in details)}

Fix Required:
Update .cursorrules to include missing {error_type.lower()} sections.

Documentation:
See docs/architecture/CURSORRULES_VALIDATION_STRATEGY.md for details.

Emergency Bypass:
Use CURSORRULES_VALIDATION_BYPASS=true git commit for emergencies.
"""

    def test_cursorrules_file_exists(self):
        """P0: .cursorrules file must exist and be readable"""
        self._start_performance_timer()

        self.assertTrue(
            self.cursorrules_path.exists(),
            f"CRITICAL P0 FAILURE: .cursorrules file not found at {self.cursorrules_path}",
        )

        self.assertIsNotNone(
            self.cursorrules_content,
            "CRITICAL P0 FAILURE: .cursorrules file exists but content is None",
        )

        self.assertGreater(
            len(self.cursorrules_content.strip()),
            0,
            "CRITICAL P0 FAILURE: .cursorrules file is empty",
        )

        self._check_performance_requirement("File existence check")
        print("✅ P0: .cursorrules file exists and is readable")

    def test_required_sections_present(self):
        """P0: All required sections must be present"""
        self._start_performance_timer()

        missing_sections = []

        for section_name, section_config in self.REQUIRED_SECTIONS.items():
            if not section_config["required"]:
                continue

            pattern = section_config["pattern"]
            if not re.search(pattern, self.cursorrules_content, re.IGNORECASE):
                missing_sections.append(f"{section_name} (pattern: {pattern})")

        if missing_sections:
            error_message = self._format_validation_error(
                "Required Sections", missing_sections
            )
            self.fail(
                f"CRITICAL P0 FAILURE: Missing required sections\n{error_message}"
            )

        self._check_performance_requirement("Section validation")
        print(f"✅ P0: All {len(self.REQUIRED_SECTIONS)} required sections present")

    def test_persona_completeness(self):
        """P0: All essential personas must be present"""
        self._start_performance_timer()

        missing_personas = []

        for persona_name, persona_config in self.REQUIRED_PERSONAS.items():
            if not persona_config["required"]:
                continue

            pattern = persona_config["pattern"]
            if not re.search(pattern, self.cursorrules_content, re.IGNORECASE):
                missing_personas.append(
                    f"{persona_name} ({persona_config['emoji']}) - {persona_config['description']}"
                )

        if missing_personas:
            error_message = self._format_validation_error(
                "Essential Personas", missing_personas
            )
            self.fail(
                f"CRITICAL P0 FAILURE: Missing essential personas\n{error_message}"
            )

        self._check_performance_requirement("Persona validation")
        print(f"✅ P0: All {len(self.REQUIRED_PERSONAS)} essential personas present")

    def test_framework_completeness(self):
        """P0: Core frameworks must be present"""
        self._start_performance_timer()

        missing_frameworks = []

        for framework_name, framework_config in self.REQUIRED_FRAMEWORKS.items():
            if not framework_config["required"]:
                continue

            pattern = framework_config["pattern"]
            if not re.search(pattern, self.cursorrules_content, re.IGNORECASE):
                missing_frameworks.append(
                    f"{framework_name} - {framework_config['description']}"
                )

        if missing_frameworks:
            error_message = self._format_validation_error(
                "Core Frameworks", missing_frameworks
            )
            self.fail(f"CRITICAL P0 FAILURE: Missing core frameworks\n{error_message}")

        self._check_performance_requirement("Framework validation")
        print(f"✅ P0: All {len(self.REQUIRED_FRAMEWORKS)} core frameworks present")

    def test_command_routing_present(self):
        """P0: Required commands must be present"""
        self._start_performance_timer()

        missing_commands = []

        for command_name, command_config in self.REQUIRED_COMMANDS.items():
            if not command_config["required"]:
                continue

            pattern = command_config["pattern"]
            if not re.search(pattern, self.cursorrules_content, re.IGNORECASE):
                missing_commands.append(
                    f"{command_name} - {command_config['description']}"
                )

        if missing_commands:
            error_message = self._format_validation_error(
                "Required Commands", missing_commands
            )
            self.fail(
                f"CRITICAL P0 FAILURE: Missing required commands\n{error_message}"
            )

        self._check_performance_requirement("Command validation")
        print(f"✅ P0: All {len(self.REQUIRED_COMMANDS)} required commands present")

    def test_cross_platform_compatibility(self):
        """P0: No external dependencies that break Claude Code compatibility"""
        self._start_performance_timer()

        compatibility_issues = []

        # Check for external file references (breaks Claude Code)
        external_file_patterns = [
            r"\.claudedirector/config/.*\.yaml",
            r"from\s+.*\.yaml",
            r"import\s+.*\.yaml",
            r"load.*\.yaml",
            r"read.*\.yaml",
        ]

        for pattern in external_file_patterns:
            matches = re.findall(pattern, self.cursorrules_content, re.IGNORECASE)
            if matches:
                compatibility_issues.append(
                    f"External file references found: {matches}"
                )

        # Check for dynamic loading references (breaks Claude Code)
        dynamic_loading_patterns = [
            r"Load.*from.*file",
            r"Dynamic.*loading",
            r"External.*configuration",
        ]

        for pattern in dynamic_loading_patterns:
            if re.search(pattern, self.cursorrules_content, re.IGNORECASE):
                compatibility_issues.append(
                    f"Dynamic loading reference found: {pattern}"
                )

        if compatibility_issues:
            error_message = self._format_validation_error(
                "Cross-Platform Compatibility", compatibility_issues
            )
            self.fail(
                f"CRITICAL P0 FAILURE: Cross-platform compatibility issues\n{error_message}"
            )

        self._check_performance_requirement("Compatibility validation")
        print("✅ P0: Cross-platform compatibility maintained (Cursor + Claude Code)")

    def test_performance_requirements(self):
        """P0: Validation must complete within performance requirements"""
        overall_start_time = time.time()

        # Run a comprehensive validation cycle
        self._start_performance_timer()

        # Simulate all validation operations
        sections_found = 0
        for section_config in self.REQUIRED_SECTIONS.values():
            if re.search(
                section_config["pattern"], self.cursorrules_content, re.IGNORECASE
            ):
                sections_found += 1

        personas_found = 0
        for persona_config in self.REQUIRED_PERSONAS.values():
            if re.search(
                persona_config["pattern"], self.cursorrules_content, re.IGNORECASE
            ):
                personas_found += 1

        frameworks_found = 0
        for framework_config in self.REQUIRED_FRAMEWORKS.values():
            if re.search(
                framework_config["pattern"], self.cursorrules_content, re.IGNORECASE
            ):
                frameworks_found += 1

        commands_found = 0
        for command_config in self.REQUIRED_COMMANDS.values():
            if re.search(
                command_config["pattern"], self.cursorrules_content, re.IGNORECASE
            ):
                commands_found += 1

        overall_elapsed = time.time() - overall_start_time

        self.assertLess(
            overall_elapsed,
            self.MAX_VALIDATION_TIME_SECONDS,
            f"CRITICAL P0 FAILURE: Complete validation took {overall_elapsed:.2f}s, must be <{self.MAX_VALIDATION_TIME_SECONDS}s",
        )

        print(
            f"✅ P0: Performance requirement met ({overall_elapsed:.2f}s < {self.MAX_VALIDATION_TIME_SECONDS}s)"
        )
        print(f"   • Sections found: {sections_found}/{len(self.REQUIRED_SECTIONS)}")
        print(f"   • Personas found: {personas_found}/{len(self.REQUIRED_PERSONAS)}")
        print(
            f"   • Frameworks found: {frameworks_found}/{len(self.REQUIRED_FRAMEWORKS)}"
        )
        print(f"   • Commands found: {commands_found}/{len(self.REQUIRED_COMMANDS)}")


def run_cursorrules_validation_test():
    """
    Run .cursorrules validation test with detailed reporting
    Following existing P0 test runner patterns
    """
    print("\n🔍 .cursorrules Validation P0 Test")
    print("=" * 50)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCursorrrulesValidationP0)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    if result.wasSuccessful():
        print("\n✅ ALL .cursorrules VALIDATION P0 TESTS PASSED")
        return True
    else:
        print(f"\n❌ .cursorrules VALIDATION P0 TESTS FAILED")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        return False


if __name__ == "__main__":
    # Support both unittest and direct execution
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--run-test":
        success = run_cursorrules_validation_test()
        sys.exit(0 if success else 1)
    else:
        unittest.main()
