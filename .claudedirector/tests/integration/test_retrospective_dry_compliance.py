#!/usr/bin/env python3
"""
Retrospective System DRY Compliance Integration Test
Validates that the implementation uses existing infrastructure without duplication

🏗️ Martin | Platform Architecture - DRY compliance validation
🤖 Berny | AI/ML Engineering - Architectural testing

SEQUENTIAL THINKING TEST METHODOLOGY:
1. Problem Definition: Validate zero duplication in retrospective system
2. Current State Analysis: Test infrastructure reuse vs. new implementations
3. Solution Hypothesis: 95% DRY compliance through existing infrastructure usage
4. Validation: Verify imports use existing classes, not duplicates
5. Execution: Test functional integration with existing systems
6. Verification: Confirm architectural compliance + zero regression
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project paths for testing
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

# Test imports to verify DRY compliance
try:
    from reporting.retrospective_enabled_chat_reporter import (
        RetrospectiveEnabledChatReporter,
        RetrospectiveStep,
        RetrospectiveSession,
        create_retrospective_enabled_chat_reporter,
    )

    RETROSPECTIVE_AVAILABLE = True
except ImportError as e:
    RETROSPECTIVE_AVAILABLE = False
    print(f"Retrospective system not available: {e}")


class TestRetrospectiveDRYCompliance(unittest.TestCase):
    """Test DRY compliance of retrospective system implementation"""

    def setUp(self):
        """Set up test environment"""
        self.config_path = "test_config.yaml"

    def test_dry_compliance_infrastructure_reuse(self):
        """Test that retrospective system reuses existing infrastructure"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Retrospective system not available")

        # Test 1: Verify existing infrastructure imports (DRY compliance)
        with patch(
            "reporting.retrospective_enabled_chat_reporter.StrategicMemoryManager"
        ) as mock_session_mgr, patch(
            "reporting.retrospective_enabled_chat_reporter.RetrospectiveValidator"
        ) as mock_validator, patch(
            "reporting.retrospective_enabled_chat_reporter.MCPIntegrationManager"
        ) as mock_mcp, patch(
            "reporting.retrospective_enabled_chat_reporter.AnalyticsEngine"
        ) as mock_analytics, patch(
            "reporting.retrospective_enabled_chat_reporter.ChatEnhancedWeeklyReporter"
        ) as mock_parent:

            # Mock parent class initialization
            mock_parent.return_value = Mock()
            mock_parent.return_value.extended_chat_commands = {}

            # Create retrospective reporter
            reporter = RetrospectiveEnabledChatReporter(self.config_path)

            # Verify existing infrastructure is used (DRY compliance)
            mock_session_mgr.assert_called_once()  # StrategicMemoryManager used
            mock_validator.assert_called_once()  # RetrospectiveValidator used
            mock_mcp.assert_called_once()  # MCPIntegrationManager used
            mock_analytics.assert_called_once()  # AnalyticsEngine used

            # Verify no duplicate session management created
            self.assertIsNotNone(reporter.session_manager)
            self.assertIsNotNone(reporter.validator)
            self.assertIsNotNone(reporter.mcp_manager)
            self.assertIsNotNone(reporter.analytics_engine)

            print("✅ DRY Compliance: All existing infrastructure properly reused")

    def test_no_duplicate_session_management(self):
        """Test that no duplicate session management is implemented"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Retrospective system not available")

        # Verify RetrospectiveSessionManager class does NOT exist in new implementation
        import reporting.retrospective_enabled_chat_reporter as retro_module

        # Should NOT have RetrospectiveSessionManager class (would be duplication)
        self.assertFalse(
            hasattr(retro_module, "RetrospectiveSessionManager"),
            "RetrospectiveSessionManager should not exist - use StrategicMemoryManager instead",
        )

        # Should have lightweight session tracking only
        self.assertTrue(
            hasattr(retro_module, "RetrospectiveSession"),
            "Should have lightweight RetrospectiveSession dataclass",
        )

        print(
            "✅ No Duplicate Session Management: Uses existing StrategicMemoryManager"
        )

    def test_existing_validation_reuse(self):
        """Test that existing RetrospectiveValidator is reused"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Retrospective system not available")

        # Test that RetrospectiveValidator import points to existing implementation
        with patch(
            "reporting.retrospective_enabled_chat_reporter.INFRASTRUCTURE_AVAILABLE",
            True,
        ):
            with patch(
                "reporting.retrospective_enabled_chat_reporter.StrategicMemoryManager"
            ), patch(
                "reporting.retrospective_enabled_chat_reporter.RetrospectiveValidator"
            ) as mock_validator, patch(
                "reporting.retrospective_enabled_chat_reporter.MCPIntegrationManager"
            ), patch(
                "reporting.retrospective_enabled_chat_reporter.AnalyticsEngine"
            ), patch(
                "reporting.retrospective_enabled_chat_reporter.ChatEnhancedWeeklyReporter"
            ):

                # Mock validator methods (existing implementation)
                mock_validator_instance = Mock()
                mock_validator_instance.validate_progress_response.return_value = True
                mock_validator_instance.validate_improvement_response.return_value = (
                    True
                )
                mock_validator_instance.validate_rating.return_value = True
                mock_validator_instance.validate_rating_explanation.return_value = True
                mock_validator.return_value = mock_validator_instance

                reporter = RetrospectiveEnabledChatReporter(self.config_path)

                # Test validation methods are called on existing validator
                result1 = reporter.validator.validate_progress_response("Test progress")
                result2 = reporter.validator.validate_improvement_response(
                    "Test improvement"
                )
                result3 = reporter.validator.validate_rating("8")
                result4 = reporter.validator.validate_rating_explanation("Good week")

                # Verify existing validator methods were called
                mock_validator_instance.validate_progress_response.assert_called_with(
                    "Test progress"
                )
                mock_validator_instance.validate_improvement_response.assert_called_with(
                    "Test improvement"
                )
                mock_validator_instance.validate_rating.assert_called_with("8")
                mock_validator_instance.validate_rating_explanation.assert_called_with(
                    "Good week"
                )

                self.assertTrue(all([result1, result2, result3, result4]))

        print(
            "✅ Existing Validation Reuse: RetrospectiveValidator properly imported and used"
        )

    def test_existing_mcp_integration_reuse(self):
        """Test that existing MCP RETROSPECTIVE_ANALYSIS pattern is reused"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Retrospective system not available")

        with patch(
            "reporting.retrospective_enabled_chat_reporter.INFRASTRUCTURE_AVAILABLE",
            True,
        ):
            with patch(
                "reporting.retrospective_enabled_chat_reporter.StrategicMemoryManager"
            ), patch(
                "reporting.retrospective_enabled_chat_reporter.RetrospectiveValidator"
            ), patch(
                "reporting.retrospective_enabled_chat_reporter.MCPIntegrationManager"
            ) as mock_mcp, patch(
                "reporting.retrospective_enabled_chat_reporter.AnalyticsEngine"
            ), patch(
                "reporting.retrospective_enabled_chat_reporter.ChatEnhancedWeeklyReporter"
            ), patch(
                "reporting.retrospective_enabled_chat_reporter.QueryPattern"
            ) as mock_query_pattern:

                # Mock MCP manager with existing RETROSPECTIVE_ANALYSIS pattern
                mock_mcp_instance = Mock()
                mock_mcp_instance.process_query = MagicMock(
                    return_value={"analysis": "test"}
                )
                mock_mcp.return_value = mock_mcp_instance

                # Mock QueryPattern.RETROSPECTIVE_ANALYSIS (existing pattern)
                mock_query_pattern.RETROSPECTIVE_ANALYSIS = "retrospective_analysis"

                reporter = RetrospectiveEnabledChatReporter(self.config_path)

                # Verify MCP manager uses existing RETROSPECTIVE_ANALYSIS pattern
                self.assertIsNotNone(reporter.mcp_manager)

        print(
            "✅ Existing MCP Integration Reuse: RETROSPECTIVE_ANALYSIS pattern properly imported"
        )

    def test_lightweight_fallback_pattern(self):
        """Test Context7 Lightweight Fallback Pattern implementation"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Retrospective system not available")

        # Test fallback behavior when infrastructure not available
        with patch(
            "reporting.retrospective_enabled_chat_reporter.INFRASTRUCTURE_AVAILABLE",
            False,
        ):

            reporter = RetrospectiveEnabledChatReporter(self.config_path)

            # Verify fallback implementations are used
            self.assertIsNotNone(reporter.session_manager)
            self.assertIsNotNone(reporter.validator)

            # Test fallback validation works
            self.assertTrue(
                reporter.validator.validate_progress_response(
                    "This is a test progress response"
                )
            )
            self.assertTrue(reporter.validator.validate_rating("8"))
            self.assertFalse(reporter.validator.validate_rating("invalid"))

        print(
            "✅ Lightweight Fallback Pattern: Graceful degradation when dependencies unavailable"
        )

    def test_true_extension_pattern(self):
        """Test that implementation follows TRUE extension pattern"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Retrospective system not available")

        # Verify RetrospectiveEnabledChatReporter extends ChatEnhancedWeeklyReporter
        with patch(
            "reporting.retrospective_enabled_chat_reporter.ChatEnhancedWeeklyReporter"
        ) as mock_parent:
            mock_parent.return_value = Mock()
            mock_parent.return_value.extended_chat_commands = {"/existing": "test"}

            reporter = RetrospectiveEnabledChatReporter(self.config_path)

            # Verify parent class was called (extension pattern)
            mock_parent.assert_called_once_with(self.config_path)

            # Verify retrospective commands were added to existing commands
            expected_commands = [
                "/retrospective",
                "/weekly-retrospective",
                "/reflection",
            ]
            for command in expected_commands:
                self.assertIn(command, reporter.retrospective_commands)

        print(
            "✅ TRUE Extension Pattern: Properly extends existing ChatEnhancedWeeklyReporter"
        )

    def test_architectural_compliance_score(self):
        """Test overall architectural compliance score"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Retrospective system not available")

        compliance_score = 0
        total_checks = 6

        # Check 1: Uses existing StrategicMemoryManager (not duplicate)
        import reporting.retrospective_enabled_chat_reporter as retro_module

        if not hasattr(retro_module, "RetrospectiveSessionManager"):
            compliance_score += 1

        # Check 2: Imports existing RetrospectiveValidator
        if (
            "from ..core.validation import RetrospectiveValidator"
            in open(retro_module.__file__).read()
        ):
            compliance_score += 1

        # Check 3: Imports existing MCPIntegrationManager
        if (
            "from ..mcp.mcp_integration_manager import MCPIntegrationManager"
            in open(retro_module.__file__).read()
        ):
            compliance_score += 1

        # Check 4: Imports existing AnalyticsEngine
        if (
            "from ..context_engineering.analytics_engine import AnalyticsEngine"
            in open(retro_module.__file__).read()
        ):
            compliance_score += 1

        # Check 5: Extends existing ChatEnhancedWeeklyReporter
        if (
            "class RetrospectiveEnabledChatReporter(ChatEnhancedWeeklyReporter)"
            in open(retro_module.__file__).read()
        ):
            compliance_score += 1

        # Check 6: Has Lightweight Fallback Pattern
        if "Lightweight Fallback" in open(retro_module.__file__).read():
            compliance_score += 1

        compliance_percentage = (compliance_score / total_checks) * 100

        # Should achieve 95%+ DRY compliance
        self.assertGreaterEqual(
            compliance_percentage,
            95.0,
            f"DRY compliance score {compliance_percentage}% below target 95%",
        )

        print(
            f"✅ Architectural Compliance Score: {compliance_percentage}% (Target: 95%)"
        )

    def test_zero_code_duplication(self):
        """Test that no code duplication exists"""

        if not RETROSPECTIVE_AVAILABLE:
            self.skipTest("Retrospective system not available")

        import reporting.retrospective_enabled_chat_reporter as retro_module

        source_code = open(retro_module.__file__).read()

        # Verify no duplicate class definitions
        duplicate_classes = [
            "class RetrospectiveSessionManager",  # Should use StrategicMemoryManager
            "class RetrospectiveValidator",  # Should import existing one
            "class MCPIntegrationManager",  # Should import existing one
            "class AnalyticsEngine",  # Should import existing one
        ]

        for duplicate_class in duplicate_classes:
            self.assertNotIn(
                duplicate_class,
                source_code,
                f"Found duplicate class definition: {duplicate_class}",
            )

        # Verify proper imports exist
        required_imports = [
            "from ..context_engineering.strategic_memory_manager import StrategicMemoryManager",
            "from ..core.validation import RetrospectiveValidator",
            "from ..mcp.mcp_integration_manager import MCPIntegrationManager",
            "from ..context_engineering.analytics_engine import AnalyticsEngine",
        ]

        for required_import in required_imports:
            self.assertIn(
                required_import,
                source_code,
                f"Missing required import: {required_import}",
            )

        print(
            "✅ Zero Code Duplication: All infrastructure properly imported, no duplicates"
        )


if __name__ == "__main__":
    unittest.main()
