"""
Unit Tests for PredictionModels - PROJECT_SUCCESS Enhancement

🏗️ Martin | Platform Architecture - Spec 002 FR2 Test Coverage

Tests the enhanced prediction_models.py with PROJECT_SUCCESS challenge type
and its associated indicators and probability calculations.

TESTING STANDARD: unittest.TestCase (per TESTING_ARCHITECTURE.md)
COVERAGE TARGET: >90% for prediction_models.py
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add lib directory to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from ai_intelligence.predictive.prediction_models import (
    PredictionModels,
    ChallengeType,
)


class TestPredictionModels(unittest.TestCase):
    """Test suite for PredictionModels with PROJECT_SUCCESS enhancement"""

    def setUp(self):
        """Set up test environment"""
        self.config = {
            "prediction_threshold": 0.7,
            "confidence_threshold": 0.85,
        }
        self.models = PredictionModels(self.config)

    def test_initialization(self):
        """Test PredictionModels initialization"""
        self.assertIsNotNone(self.models)
        self.assertEqual(self.models.config, self.config)
        self.assertIsNotNone(self.models.challenge_indicators)

    def test_project_success_challenge_type_exists(self):
        """Test PROJECT_SUCCESS was added to ChallengeType enum"""
        # Verify PROJECT_SUCCESS is in enum
        self.assertTrue(hasattr(ChallengeType, "PROJECT_SUCCESS"))
        self.assertEqual(ChallengeType.PROJECT_SUCCESS.value, "project_success")

    def test_project_success_indicators_exist(self):
        """Test PROJECT_SUCCESS indicators are configured"""
        indicators = self.models.get_challenge_indicators(ChallengeType.PROJECT_SUCCESS)

        # Verify indicators are present
        self.assertIsNotNone(indicators)
        self.assertIn("team_velocity_trend", indicators)
        self.assertIn("stakeholder_satisfaction_min", indicators)
        self.assertIn("scope_stability_threshold", indicators)
        self.assertIn("quality_metrics_min", indicators)
        self.assertIn("timeline_adherence_min", indicators)
        self.assertIn("team_morale_min", indicators)

    def test_project_success_key_signals(self):
        """Test PROJECT_SUCCESS key signals are defined"""
        indicators = self.models.get_challenge_indicators(ChallengeType.PROJECT_SUCCESS)

        key_signals = indicators.get("key_signals", [])
        self.assertEqual(len(key_signals), 6)
        self.assertIn("consistent_velocity", key_signals)
        self.assertIn("stakeholder_alignment", key_signals)
        self.assertIn("stable_scope", key_signals)
        self.assertIn("high_quality", key_signals)
        self.assertIn("on_schedule", key_signals)
        self.assertIn("team_health", key_signals)

    def test_get_supported_challenge_types_includes_project_success(self):
        """Test PROJECT_SUCCESS is in supported challenge types"""
        supported_types = self.models.get_supported_challenge_types()

        self.assertIn(ChallengeType.PROJECT_SUCCESS, supported_types)

    def test_calculate_base_probability_returns_default(self):
        """Test calculate_base_probability returns default value (stub implementation)"""
        context_data = {
            "velocity_trend": 0.85,
            "stakeholder_satisfaction": 0.90,
        }

        probability = self.models.calculate_base_probability(
            ChallengeType.PROJECT_SUCCESS, context_data
        )

        # Current stub implementation returns 0.4
        self.assertEqual(probability, 0.4)

    def test_calculate_base_probability_with_empty_context(self):
        """Test probability calculation with empty context"""
        context_data = {}

        probability = self.models.calculate_base_probability(
            ChallengeType.PROJECT_SUCCESS, context_data
        )

        # Should return default probability
        self.assertEqual(probability, 0.4)

    def test_calculate_base_probability_for_unknown_challenge_type(self):
        """Test probability calculation for non-existent challenge type"""
        # Mock a challenge type that doesn't have indicators
        mock_type = Mock()
        mock_type.value = "unknown_type"

        probability = self.models.calculate_base_probability(mock_type, {})

        # Should return 0.0 for unknown types
        self.assertEqual(probability, 0.0)

    def test_existing_challenge_types_still_work(self):
        """Test existing challenge types (TEAM_BURNOUT) still function"""
        # Verify TEAM_BURNOUT still exists
        self.assertTrue(hasattr(ChallengeType, "TEAM_BURNOUT"))

        indicators = self.models.get_challenge_indicators(ChallengeType.TEAM_BURNOUT)
        self.assertIsNotNone(indicators)
        self.assertIn("velocity_decline_threshold", indicators)

    def test_get_challenge_indicators_for_all_types(self):
        """Test get_challenge_indicators works for all ChallengeType values"""
        for challenge_type in ChallengeType:
            indicators = self.models.get_challenge_indicators(challenge_type)
            self.assertIsNotNone(indicators)
            self.assertIsInstance(indicators, dict)

    def test_get_prediction_confidence_threshold(self):
        """Test getting prediction confidence threshold from config"""
        threshold = self.models.get_prediction_confidence_threshold()
        self.assertEqual(threshold, 0.7)

    def test_get_prediction_confidence_threshold_default(self):
        """Test default confidence threshold when not in config"""
        models_no_config = PredictionModels({})
        threshold = models_no_config.get_prediction_confidence_threshold()
        self.assertEqual(threshold, 0.7)  # Default value

    def test_project_success_indicator_thresholds(self):
        """Test PROJECT_SUCCESS indicator thresholds are reasonable"""
        indicators = self.models.get_challenge_indicators(ChallengeType.PROJECT_SUCCESS)

        # Verify thresholds are in reasonable ranges
        self.assertGreaterEqual(indicators["team_velocity_trend"], 0.0)
        self.assertLessEqual(indicators["team_velocity_trend"], 1.0)

        self.assertGreaterEqual(indicators["stakeholder_satisfaction_min"], 0.5)
        self.assertLessEqual(indicators["stakeholder_satisfaction_min"], 1.0)

        self.assertGreaterEqual(indicators["scope_stability_threshold"], 0.7)
        self.assertLessEqual(indicators["scope_stability_threshold"], 1.0)

        self.assertGreaterEqual(indicators["quality_metrics_min"], 0.7)
        self.assertLessEqual(indicators["quality_metrics_min"], 1.0)

        self.assertGreaterEqual(indicators["timeline_adherence_min"], 0.8)
        self.assertLessEqual(indicators["timeline_adherence_min"], 1.0)

        self.assertGreaterEqual(indicators["team_morale_min"], 0.6)
        self.assertLessEqual(indicators["team_morale_min"], 1.0)


class TestChallengeTypeEnum(unittest.TestCase):
    """Test suite for ChallengeType enum completeness"""

    def test_all_expected_challenge_types_exist(self):
        """Test all expected challenge types are present"""
        expected_types = [
            "TEAM_BURNOUT",
            "STAKEHOLDER_CONFLICT",
            "DELIVERY_RISK",
            "TECHNICAL_DEBT",
            "RESOURCE_SHORTAGE",
            "COMMUNICATION_BREAKDOWN",
            "STRATEGIC_MISALIGNMENT",
            "TALENT_RETENTION",
            "PROJECT_SUCCESS",  # Spec 002 FR2 enhancement
        ]

        for expected_type in expected_types:
            self.assertTrue(
                hasattr(ChallengeType, expected_type),
                f"ChallengeType missing: {expected_type}",
            )

    def test_challenge_type_values_are_lowercase_snake_case(self):
        """Test ChallengeType enum values follow naming convention"""
        for challenge_type in ChallengeType:
            value = challenge_type.value
            # Should be lowercase with underscores
            self.assertEqual(value, value.lower())
            self.assertNotIn(" ", value)
            self.assertNotIn("-", value)

    def test_get_supported_challenge_types_count(self):
        """Test correct number of supported challenge types with indicators"""
        models = PredictionModels({})
        supported_types = models.get_supported_challenge_types()

        # Should have 5 types with indicators configured:
        # TEAM_BURNOUT, STAKEHOLDER_CONFLICT, DELIVERY_RISK, TECHNICAL_DEBT, PROJECT_SUCCESS
        self.assertEqual(len(supported_types), 5)


if __name__ == "__main__":
    unittest.main()
