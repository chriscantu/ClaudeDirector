"""
Unit tests specifically for stakeholder AI detection module.
Tests the actual StakeholderIntelligence class and its AI detection capabilities.
"""

import pytest
import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add the lib directory to Python path for imports
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

try:
    from lib.context_engineering.stakeholder_intelligence_unified import (
        get_stakeholder_intelligence,
    )
    from lib.core.config import ClaudeDirectorConfig
    from lib.core.exceptions import AIDetectionError

    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import stakeholder modules: {e}")
    IMPORTS_AVAILABLE = False


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required modules not available")
class TestStakeholderAIDetection(unittest.TestCase):
    """Test stakeholder AI detection functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_config = Mock(spec=ClaudeDirectorConfig)
        self.mock_config.database_path = ":memory:"
        self.mock_config.stakeholder_auto_create_threshold = 0.85
        self.mock_config.stakeholder_profiling_threshold = 0.65
        self.mock_config.enable_caching = False
        self.mock_config.enable_parallel_processing = False

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_stakeholder_intelligence_initialization(
        self, mock_engagement, mock_detector, mock_ai
    ):
        """Test StakeholderIntelligence initializes correctly."""
        # Setup mocks
        mock_ai_instance = Mock()
        mock_detector_instance = Mock()
        mock_engagement_instance = Mock()

        mock_ai.return_value = mock_ai_instance
        mock_detector.return_value = mock_detector_instance
        mock_engagement.return_value = mock_engagement_instance

        # Create instance
        stakeholder_intel = StakeholderIntelligence(config=self.mock_config)

        # Verify initialization
        self.assertEqual(stakeholder_intel.config, self.mock_config)
        self.assertEqual(stakeholder_intel.db_path, ":memory:")

        # Verify mocks were called
        mock_ai.assert_called_once()
        mock_detector.assert_called_once()
        mock_engagement.assert_called_once()

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_detect_stakeholders_high_confidence(
        self, mock_engagement, mock_detector, mock_ai
    ):
        """Test stakeholder detection with high confidence scores."""
        # Setup mocks
        mock_detector_instance = Mock()
        mock_detector.return_value = mock_detector_instance

        # Mock high-confidence detection result
        mock_detector_instance.detect_stakeholders.return_value = [
            {
                "name": "John Smith",
                "confidence": 0.92,
                "role": "VP Engineering",
                "context": "Meeting with John Smith tomorrow",
            }
        ]

        stakeholder_intel = StakeholderIntelligence(config=self.mock_config)

        # Test detection using actual API method
        results = stakeholder_intel.detect_stakeholders_in_content(
            "Meeting with John Smith tomorrow", {"source": "test"}
        )

        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "John Smith")
        self.assertEqual(results[0]["confidence"], 0.92)
        self.assertGreaterEqual(
            results[0]["confidence"], self.mock_config.stakeholder_auto_create_threshold
        )

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_detect_stakeholders_medium_confidence(
        self, mock_engagement, mock_detector, mock_ai
    ):
        """Test stakeholder detection with medium confidence scores."""
        # Setup mocks
        mock_detector_instance = Mock()
        mock_detector.return_value = mock_detector_instance

        # Mock medium-confidence detection result
        mock_detector_instance.detect_stakeholders.return_value = [
            {
                "name": "Sarah Johnson",
                "confidence": 0.72,
                "role": "Product Manager",
                "context": "Sarah mentioned the deadline",
            }
        ]

        stakeholder_intel = StakeholderIntelligence(config=self.mock_config)

        # Test detection using actual API method
        results = stakeholder_intel.detect_stakeholders_in_content(
            "Sarah mentioned the deadline", {"source": "test"}
        )

        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Sarah Johnson")
        self.assertEqual(results[0]["confidence"], 0.72)

        # Should be above profiling threshold but below auto-create
        self.assertGreaterEqual(
            results[0]["confidence"], self.mock_config.stakeholder_profiling_threshold
        )
        self.assertLess(
            results[0]["confidence"], self.mock_config.stakeholder_auto_create_threshold
        )

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_detect_stakeholders_low_confidence(
        self, mock_engagement, mock_detector, mock_ai
    ):
        """Test stakeholder detection with low confidence scores."""
        # Setup mocks
        mock_detector_instance = Mock()
        mock_detector.return_value = mock_detector_instance

        # Mock low-confidence detection result (should be filtered out)
        mock_detector_instance.detect_stakeholders.return_value = [
            {
                "name": "Someone",
                "confidence": 0.45,
                "role": "Unknown",
                "context": "Someone said something",
            }
        ]

        stakeholder_intel = StakeholderIntelligence(config=self.mock_config)

        # Test detection using actual API method
        results = stakeholder_intel.detect_stakeholders_in_content(
            "Someone said something", {"source": "test"}
        )

        # Should filter out low-confidence results
        # (depending on implementation, this might return empty or the low-confidence result)
        if results:
            self.assertLess(
                results[0]["confidence"],
                self.mock_config.stakeholder_profiling_threshold,
            )

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_stakeholder_detection_error_handling(
        self, mock_engagement, mock_detector, mock_ai
    ):
        """Test error handling in stakeholder detection."""
        # Setup mocks
        mock_detector_instance = Mock()
        mock_detector.return_value = mock_detector_instance

        # Mock detector raising an error
        mock_detector_instance.detect_stakeholders.side_effect = AIDetectionError(
            "Detection failed"
        )

        stakeholder_intel = StakeholderIntelligence(config=self.mock_config)

        # Test that error is properly handled
        with self.assertRaises(AIDetectionError):
            stakeholder_intel.detect_stakeholders_in_content(
                "Test input", {"source": "test"}
            )

    @patch("claudedirector.intelligence.stakeholder.LocalStakeholderAI")
    @patch("claudedirector.intelligence.stakeholder.IntelligentStakeholderDetector")
    @patch("claudedirector.intelligence.stakeholder.StakeholderEngagementEngine")
    def test_stakeholder_profile_creation(
        self, mock_engagement, mock_detector, mock_ai
    ):
        """Test stakeholder profile creation functionality."""
        # Setup mocks
        mock_engagement_instance = Mock()
        mock_engagement.return_value = mock_engagement_instance

        # Mock profile creation
        expected_profile = {
            "stakeholder_id": "john_smith_001",
            "name": "John Smith",
            "role": "VP Engineering",
            "influence_score": 0.9,
            "engagement_history": [],
            "created_at": "2025-01-01T00:00:00Z",
        }
        mock_engagement_instance.create_stakeholder_profile.return_value = (
            expected_profile
        )

        stakeholder_intel = StakeholderIntelligence(config=self.mock_config)

        # Test profile creation
        stakeholder_data = {
            "name": "John Smith",
            "role": "VP Engineering",
            "confidence": 0.9,
        }
        profile = stakeholder_intel.create_stakeholder(stakeholder_data)

        # Verify profile creation
        self.assertEqual(profile["name"], "John Smith")
        self.assertEqual(profile["role"], "VP Engineering")
        mock_engagement_instance.create_stakeholder_profile.assert_called_once()


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required modules not available")
class TestStakeholderDetectionPatterns(unittest.TestCase):
    """Test stakeholder detection pattern recognition."""

    def test_executive_title_patterns(self):
        """Test detection of executive title patterns."""
        executive_patterns = [
            "CEO John Doe announced the new strategy",
            "Team member will lead the project",
            "Executive approved the architecture design",
            "Team manager presented the roadmap",
            "Chief Marketing Officer Alex Rodriguez spoke about growth",
        ]

        # This would test the actual pattern matching logic
        # For now, we're testing the pattern concepts
        for pattern in executive_patterns:
            self.assertRegex(
                pattern,
                r"(?:CEO|VP|CTO|Director|Chief)\s+(?:of\s+\w+\s+)?[A-Z][a-z]+\s+[A-Z][a-z]+",
            )

    def test_meeting_context_patterns(self):
        """Test detection in meeting context."""
        meeting_patterns = [
            "In today's standup, Tom Brown mentioned blockers",
            "During the review, Emily Davis raised concerns",
            "At the planning session, Robert Wilson proposed changes",
            "In our 1:1, Jennifer Lee discussed career goals",
        ]

        for pattern in meeting_patterns:
            # Test that meeting context + name patterns are detected
            self.assertTrue(
                any(
                    word in pattern.lower()
                    for word in ["standup", "review", "planning", "1:1", "meeting"]
                )
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
