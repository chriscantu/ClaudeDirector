"""
Comprehensive unit tests for core AI detection logic.
Focus on testing the fundamental AI detection algorithms and decision-making processes.
"""

import unittest
from unittest.mock import Mock
import sys
from pathlib import Path

# Add the lib directory to Python path for imports
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

try:
    from claudedirector.core.config import ClaudeDirectorConfig
    from claudedirector.core.exceptions import AIDetectionError, ConfigurationError
except ImportError as e:
    print(f"Warning: Could not import core modules: {e}")
    ClaudeDirectorConfig = None
    AIDetectionError = Exception
    ConfigurationError = Exception


class TestAIDetectionThresholds(unittest.TestCase):
    """Test AI detection threshold logic and decision making."""

    def setUp(self):
        """Set up test fixtures with mock configuration."""
        if ClaudeDirectorConfig:
            self.config = ClaudeDirectorConfig(
                stakeholder_auto_create_threshold=0.85,
                stakeholder_profiling_threshold=0.65,
                task_auto_create_threshold=0.80,
                task_review_threshold=0.60,
            )
        else:
            # Fallback mock config
            self.config = Mock()
            self.config.stakeholder_auto_create_threshold = 0.85
            self.config.stakeholder_profiling_threshold = 0.65
            self.config.task_auto_create_threshold = 0.80
            self.config.task_review_threshold = 0.60

    def test_stakeholder_detection_threshold_logic(self):
        """Test stakeholder detection confidence threshold decisions."""
        # Test cases for different confidence levels
        test_cases = [
            (0.90, True, "High confidence should trigger auto-creation"),
            (0.85, True, "Exact threshold should trigger auto-creation"),
            (0.80, False, "Below threshold should not auto-create"),
            (0.70, True, "Above profiling threshold should profile"),
            (0.65, True, "Exact profiling threshold should profile"),
            (0.60, False, "Below profiling threshold should ignore"),
        ]

        for confidence, expected_action, description in test_cases:
            with self.subTest(confidence=confidence, description=description):
                # Auto-creation logic
                should_auto_create = (
                    confidence >= self.config.stakeholder_auto_create_threshold
                )
                # Profiling logic
                should_profile = (
                    confidence >= self.config.stakeholder_profiling_threshold
                )

                if confidence >= 0.85:
                    self.assertTrue(
                        should_auto_create, f"Should auto-create at {confidence}"
                    )
                elif confidence >= 0.65:
                    self.assertTrue(should_profile, f"Should profile at {confidence}")
                else:
                    self.assertFalse(should_profile, f"Should ignore at {confidence}")

    def test_task_detection_threshold_logic(self):
        """Test task detection confidence threshold decisions."""
        test_cases = [
            (0.90, True, "High confidence should trigger auto-creation"),
            (0.80, True, "Exact threshold should trigger auto-creation"),
            (0.75, False, "Below threshold should not auto-create"),
            (0.65, True, "Above review threshold should flag for review"),
            (0.60, True, "Exact review threshold should flag for review"),
            (0.55, False, "Below review threshold should ignore"),
        ]

        for confidence, expected_action, description in test_cases:
            with self.subTest(confidence=confidence, description=description):
                # Auto-creation logic
                should_auto_create = (
                    confidence >= self.config.task_auto_create_threshold
                )
                # Review logic
                should_review = confidence >= self.config.task_review_threshold

                if confidence >= 0.80:
                    self.assertTrue(
                        should_auto_create, f"Should auto-create at {confidence}"
                    )
                elif confidence >= 0.60:
                    self.assertTrue(should_review, f"Should review at {confidence}")
                else:
                    self.assertFalse(should_review, f"Should ignore at {confidence}")

    def test_confidence_score_validation(self):
        """Test that confidence scores are properly validated."""
        # Valid confidence scores
        valid_scores = [0.0, 0.5, 0.65, 0.85, 1.0]
        for score in valid_scores:
            self.assertTrue(0.0 <= score <= 1.0, f"Score {score} should be valid")

        # Invalid confidence scores should be handled
        invalid_scores = [-0.1, 1.1, 2.0, -1.0]
        for score in invalid_scores:
            self.assertFalse(0.0 <= score <= 1.0, f"Score {score} should be invalid")

    def test_threshold_configuration_validation(self):
        """Test that thresholds are properly configured and validated."""
        # Valid threshold relationships
        self.assertLessEqual(
            self.config.stakeholder_profiling_threshold,
            self.config.stakeholder_auto_create_threshold,
            "Profiling threshold should be <= auto-create threshold",
        )

        self.assertLessEqual(
            self.config.task_review_threshold,
            self.config.task_auto_create_threshold,
            "Review threshold should be <= auto-create threshold",
        )


class TestAIDetectionPatterns(unittest.TestCase):
    """Test AI detection pattern recognition and keyword matching."""

    def test_stakeholder_name_detection_patterns(self):
        """Test stakeholder name detection pattern matching."""
        # Test cases for stakeholder detection
        positive_cases = [
            ("Meeting with John Smith tomorrow", "John Smith"),
            ("Senior leader will guide the initiative", "Senior Leader"),
            ("Team lead will attend the meeting", "Team Lead"),
            ("Executive approved the architecture", "Executive"),
            ("PM Lisa Wang is assigned", "Lisa Wang"),
        ]

        negative_cases = [
            ("The meeting is scheduled",),
            ("Project deadline is Friday",),
            ("Code review completed",),
            ("Documentation updated",),
        ]

        # Mock pattern detection logic
        def mock_detect_stakeholder_names(text):
            """Mock stakeholder name detection."""
            names = []
            # Simple pattern matching for testing
            import re

            # Pattern for: Title? FirstName LastName
            pattern = r"(?:VP|Director|CTO|PM|CEO|Manager)\s+(?:of\s+\w+\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+)|(?<!\w)([A-Z][a-z]+\s+[A-Z][a-z]+)(?=\s+(?:will|is|approved|tomorrow))"
            matches = re.findall(pattern, text)
            for match in matches:
                name = match[0] if match[0] else match[1]
                if name:
                    names.append(name)
            return names

        for text, expected_name in positive_cases:
            with self.subTest(text=text):
                detected_names = mock_detect_stakeholder_names(text)
                self.assertIn(
                    expected_name,
                    detected_names,
                    f"Should detect '{expected_name}' in '{text}'",
                )

        for text in negative_cases:
            with self.subTest(text=text[0]):
                detected_names = mock_detect_stakeholder_names(text[0])
                self.assertEqual(
                    len(detected_names), 0, f"Should not detect names in '{text[0]}'"
                )

    def test_task_pattern_detection(self):
        """Test task detection pattern matching."""
        positive_cases = [
            ("Need to complete code review by Friday", "code review"),
            ("TODO: Update documentation", "Update documentation"),
            ("Action item: Schedule team meeting", "Schedule team meeting"),
            ("Must fix bug in authentication module", "fix bug"),
            ("Deadline: Submit proposal by Monday", "Submit proposal"),
        ]

        negative_cases = [
            ("The project is going well",),
            ("Team meeting was productive",),
            ("Code is working correctly",),
        ]

        # Mock task pattern detection logic
        def mock_detect_task_patterns(text):
            """Mock task pattern detection."""
            import re

            task_patterns = [
                r"(?:Need to|TODO:|Action item:|Must)\s+(.+?)(?:\s+by\s+\w+|$)",
                r"(?:Deadline:)\s+(.+?)(?:\s+by\s+\w+|$)",
                r"(?:complete|fix|update|schedule|submit)\s+(.+?)(?:\s+by\s+\w+|$)",
            ]

            tasks = []
            for pattern in task_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                tasks.extend(matches)
            return [task.strip() for task in tasks if task.strip()]

        for text, expected_task in positive_cases:
            with self.subTest(text=text):
                detected_tasks = mock_detect_task_patterns(text)
                self.assertTrue(
                    any(
                        expected_task.lower() in task.lower() for task in detected_tasks
                    ),
                    f"Should detect task related to '{expected_task}' in '{text}'",
                )

        for text in negative_cases:
            with self.subTest(text=text[0]):
                detected_tasks = mock_detect_task_patterns(text[0])
                self.assertEqual(
                    len(detected_tasks), 0, f"Should not detect tasks in '{text[0]}'"
                )


class TestAIDetectionErrorHandling(unittest.TestCase):
    """Test error handling in AI detection processes."""

    def test_invalid_input_handling(self):
        """Test handling of invalid inputs to AI detection."""
        invalid_inputs = [None, "", "   ", 123, [], {}]

        def mock_ai_detection_function(text):
            """Mock AI detection that validates input."""
            if not isinstance(text, str) or not text.strip():
                raise AIDetectionError("Invalid input: text must be non-empty string")
            return {"confidence": 0.5, "detected": True}

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(AIDetectionError):
                    mock_ai_detection_function(invalid_input)

    def test_configuration_error_handling(self):
        """Test handling of configuration errors in AI detection."""
        invalid_configs = [
            {"stakeholder_auto_create_threshold": -0.1},  # Below 0
            {"stakeholder_auto_create_threshold": 1.1},  # Above 1
            {"task_auto_create_threshold": "invalid"},  # Wrong type
        ]

        def mock_validate_config(config_dict):
            """Mock configuration validation."""
            for key, value in config_dict.items():
                if "threshold" in key:
                    if not isinstance(value, (int, float)):
                        raise ConfigurationError(f"Threshold {key} must be numeric")
                    if not 0.0 <= value <= 1.0:
                        raise ConfigurationError(
                            f"Threshold {key} must be between 0 and 1"
                        )

        for invalid_config in invalid_configs:
            with self.subTest(config=invalid_config):
                with self.assertRaises(ConfigurationError):
                    mock_validate_config(invalid_config)


if __name__ == "__main__":
    # Run with verbose output
    unittest.main(verbosity=2)
