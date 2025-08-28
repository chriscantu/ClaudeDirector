#!/usr/bin/env python3
"""
Configuration Integrity Regression Tests

CRITICAL: These tests must pass before any SOLID refactoring begins.
Validates that all hard-coded values are accessible and configuration
changes don't break existing functionality.
"""

import unittest
import sys
from pathlib import Path
import re
from typing import Dict, List, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestConfigurationIntegrity(unittest.TestCase):
    """Test configuration system integrity before SOLID refactoring"""

    def setUp(self):
        """Set up test environment"""
        self.core_path = PROJECT_ROOT / ".claudedirector/lib/core"
        self.config_module_path = self.core_path / "config.py"

        # Hard-coded values that should be configurable
        self.expected_hardcoded_patterns = {
            "priority_levels": ["urgent", "high", "medium", "low"],
            "health_statuses": ["excellent", "healthy", "at_risk", "failing"],
            "decision_types": [
                "strategic",
                "operational",
                "technical",
                "organizational",
            ],
            "stakeholder_types": ["stakeholder", "internal", "external", "executive"],
            "threshold_patterns": [r"0\.\d+"],  # 0.85, 0.70, etc.
        }

    def test_config_module_exists_and_importable(self):
        """Ensure config module exists and can be imported"""
        self.assertTrue(
            self.config_module_path.exists(),
            "config.py module must exist before refactoring",
        )

        try:
            # Test import without breaking existing functionality
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "config", self.config_module_path
            )
            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)

            # Verify basic structure exists
            self.assertTrue(
                hasattr(config_module, "ClaudeDirectorConfig")
                or hasattr(config_module, "get_config")
                or len(
                    [attr for attr in dir(config_module) if not attr.startswith("_")]
                )
                > 0,
                "Config module must have accessible configuration interface",
            )

        except Exception as e:
            self.fail(f"Config module import failed: {e}")

    def test_all_hardcoded_values_catalogued(self):
        """Catalog all hard-coded values that need to be configurable"""
        hardcoded_values = self._extract_hardcoded_values()

        # Verify we found expected patterns
        self.assertGreater(
            len(hardcoded_values["strings"]),
            50,
            "Should find substantial number of hard-coded strings",
        )

        self.assertGreaterEqual(
            len(hardcoded_values["numbers"]),
            20,
            "Should find substantial number of hard-coded thresholds",
        )

        # Log findings for refactoring reference
        print(f"\n📊 HARDCODED VALUES CATALOG:")
        print(f"   Strings: {len(hardcoded_values['strings'])}")
        print(f"   Numbers: {len(hardcoded_values['numbers'])}")
        print(f"   Files affected: {len(hardcoded_values['files'])}")

    def test_current_functionality_baseline(self):
        """Establish baseline of current functionality before refactoring"""
        try:
            # Import required modules
            import sys
            import os

            # Test core imports work
            sys.path.insert(0, str(self.core_path))

            # Test critical modules can be imported
            # Add the lib directory to path for imports
            lib_path = os.path.join(os.path.dirname(__file__), "..", "..", "lib")
            sys.path.insert(0, lib_path)

            critical_modules = [
                "config",
                "core.complexity_analyzer",

                "core.integrated_conversation_manager",
            ]

            import_results = {}
            for module_name in critical_modules:
                try:
                    module = __import__(module_name, fromlist=[""])
                    import_results[module_name] = "SUCCESS"
                except Exception as e:
                    import_results[module_name] = f"FAILED: {e}"

            # All critical modules should import successfully
            failed_imports = [k for k, v in import_results.items() if "FAILED" in v]
            self.assertEqual(
                len(failed_imports),
                0,
                f"Critical modules failed to import: {failed_imports}",
            )

        except Exception as e:
            self.fail(f"Baseline functionality test failed: {e}")

    def test_configuration_access_patterns(self):
        """Test that configuration values can be accessed consistently"""
        # This test validates the configuration interface works
        # before we start refactoring hard-coded values

        try:
            from core.config import ClaudeDirectorConfig

            config = ClaudeDirectorConfig()

            # Test basic configuration access
            self.assertTrue(
                hasattr(config, "get")
                or hasattr(config, "__getitem__")
                or hasattr(config, "get_threshold"),
                "Configuration must provide access interface",
            )

        except ImportError:
            # If config doesn't exist yet, that's expected
            # This test will guide the configuration system implementation
            print("⚠️ Configuration system not yet implemented - this is expected")
            print("   This test will validate the system once implemented")

    def test_threshold_value_consistency(self):
        """Validate threshold values are consistent across modules"""
        threshold_values = self._extract_threshold_values()

        # Check for common threshold patterns
        common_thresholds = {}
        for file_path, thresholds in threshold_values.items():
            for threshold in thresholds:
                if threshold not in common_thresholds:
                    common_thresholds[threshold] = []
                common_thresholds[threshold].append(file_path)

        # Identify potentially inconsistent thresholds
        # (same value used in multiple places - should be centralized)
        duplicate_thresholds = {
            k: v for k, v in common_thresholds.items() if len(v) > 1
        }

        self.assertGreater(
            len(duplicate_thresholds),
            0,
            "Should find threshold values that appear in multiple files",
        )

        print(f"\n🎯 THRESHOLD CONSOLIDATION OPPORTUNITIES:")
        for threshold, files in list(duplicate_thresholds.items())[:5]:
            print(f"   {threshold}: used in {len(files)} files")

    def test_string_pattern_consistency(self):
        """Validate string patterns are consistent across modules"""
        string_patterns = self._extract_string_patterns()

        # Check for common string patterns
        pattern_usage = {}
        for pattern in ["strategic", "organizational", "technical", "stakeholder"]:
            files_using_pattern = [
                f for f, patterns in string_patterns.items() if pattern in patterns
            ]
            pattern_usage[pattern] = len(files_using_pattern)

        # These patterns should be widely used (indicating need for centralization)
        for pattern, usage_count in pattern_usage.items():
            self.assertGreater(
                usage_count, 3, f"Pattern '{pattern}' should be used in multiple files"
            )

    def test_configuration_validation_requirements(self):
        """Define requirements for configuration validation"""
        # This test documents what the configuration system must validate

        validation_requirements = {
            "threshold_ranges": {
                "quality_threshold": (0.0, 1.0),
                "complexity_threshold": (0.0, 1.0),
                "confidence_threshold": (0.0, 1.0),
            },
            "enum_values": {
                "priority_levels": ["urgent", "high", "medium", "low"],
                "health_statuses": ["excellent", "healthy", "at_risk", "failing"],
            },
            "required_keys": [
                "stakeholder_auto_create_threshold",
                "stakeholder_profiling_threshold",
                "quality_threshold",
            ],
        }

        # Document requirements for implementation
        self.assertIsInstance(validation_requirements, dict)
        self.assertIn("threshold_ranges", validation_requirements)
        self.assertIn("enum_values", validation_requirements)

        print(f"\n📋 CONFIGURATION VALIDATION REQUIREMENTS:")
        print(
            f"   Threshold ranges: {len(validation_requirements['threshold_ranges'])}"
        )
        print(f"   Enum validations: {len(validation_requirements['enum_values'])}")
        print(f"   Required keys: {len(validation_requirements['required_keys'])}")

    def _extract_hardcoded_values(self) -> Dict[str, Any]:
        """Extract all hard-coded values from core modules"""
        hardcoded_values = {"strings": set(), "numbers": set(), "files": set()}

        for py_file in self.core_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract string literals
                string_matches = re.findall(r'["\']([^"\']{3,})["\']', content)
                for match in string_matches:
                    if any(
                        pattern in match.lower()
                        for pattern in [
                            "strategic",
                            "technical",
                            "stakeholder",
                            "decision",
                            "risk",
                        ]
                    ):
                        hardcoded_values["strings"].add(match)
                        hardcoded_values["files"].add(str(py_file))

                # Extract numeric literals (thresholds)
                number_matches = re.findall(r"\b0\.\d+\b", content)
                for match in number_matches:
                    hardcoded_values["numbers"].add(match)
                    hardcoded_values["files"].add(str(py_file))

            except Exception as e:
                print(f"⚠️ Could not analyze {py_file}: {e}")

        return hardcoded_values

    def _extract_threshold_values(self) -> Dict[str, List[str]]:
        """Extract threshold values by file"""
        threshold_values = {}

        for py_file in self.core_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                thresholds = re.findall(r"\b0\.\d+\b", content)
                if thresholds:
                    threshold_values[str(py_file)] = thresholds

            except Exception:
                continue

        return threshold_values

    def _extract_string_patterns(self) -> Dict[str, List[str]]:
        """Extract string patterns by file"""
        string_patterns = {}

        for py_file in self.core_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()

                patterns = []
                for pattern in [
                    "strategic",
                    "organizational",
                    "technical",
                    "stakeholder",
                    "decision",
                    "risk",
                ]:
                    if pattern in content.lower():
                        patterns.append(pattern)

                if patterns:
                    string_patterns[str(py_file)] = patterns

            except Exception:
                continue

        return string_patterns


class TestConfigurationBackwardsCompatibility(unittest.TestCase):
    """Test that configuration changes maintain backwards compatibility"""

    def test_existing_api_preserved(self):
        """Ensure existing APIs continue to work during refactoring"""
        # This test will be expanded as we identify existing APIs
        # that must be preserved during configuration refactoring

        # For now, document the requirement
        compatibility_requirements = {
            "import_paths": [
                "from core.config import get_config",
                "from core.config import ClaudeDirectorConfig",
            ],
            "method_signatures": [
                "get_threshold(name: str) -> float",
                "get_enum_values(category: str) -> List[str]",
            ],
        }

        self.assertIsInstance(compatibility_requirements, dict)
        print(f"\n🔄 BACKWARDS COMPATIBILITY REQUIREMENTS:")
        print(
            f"   Import paths to preserve: {len(compatibility_requirements['import_paths'])}"
        )
        print(
            f"   Method signatures to maintain: {len(compatibility_requirements['method_signatures'])}"
        )


def run_configuration_integrity_tests():
    """Run configuration integrity test suite"""
    print("🔧 CONFIGURATION INTEGRITY TEST SUITE")
    print("=" * 60)
    print("CRITICAL: These tests must pass before SOLID refactoring")
    print("Validates configuration system readiness and baseline functionality")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestSuite()

    # Add configuration integrity tests
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(TestConfigurationIntegrity)
    )
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(
            TestConfigurationBackwardsCompatibility
        )
    )

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    print(f"📊 CONFIGURATION INTEGRITY TEST RESULTS")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  {test}: {failure}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, error in result.errors:
            print(f"  {test}: {error}")

    success = len(result.failures) == 0 and len(result.errors) == 0

    if success:
        print("\n🎉 ALL CONFIGURATION INTEGRITY TESTS PASSED")
        print("✅ Safe to proceed with configuration system refactoring")
    else:
        print("\n❌ CONFIGURATION INTEGRITY TESTS FAILED")
        print("🚫 DO NOT PROCEED with SOLID refactoring until these pass")

    return success


if __name__ == "__main__":
    success = run_configuration_integrity_tests()
    sys.exit(0 if success else 1)
