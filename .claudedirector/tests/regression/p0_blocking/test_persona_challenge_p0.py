"""
P0 Test: Persona Challenge Framework

BUSINESS CRITICAL: Persona challenge framework must provide 80%+ challenge detection accuracy
and maintain persona authenticity while adding strategic challenge behaviors.

ARCHITECTURAL COMPLIANCE:
- Follows TESTING_ARCHITECTURE.md P0 test patterns
- Integrates with unified test runner system
- Validates business-critical persona functionality

Author: Martin (Platform Architecture)
"""

import sys
import unittest
from pathlib import Path
from typing import Dict, Any, List
import time

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
lib_path = str(PROJECT_ROOT / ".claudedirector" / "lib")

# Robust import strategy - ensure lib path is first in sys.path
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
elif sys.path.index(lib_path) != 0:
    sys.path.remove(lib_path)
    sys.path.insert(0, lib_path)

# Import with explicit error handling for CI debugging
try:
    from personas.strategic_challenge_framework import (
        StrategicChallengeFramework,
        ChallengeType,
        strategic_challenge_framework,
    )
    from core.persona_enhancement_engine import PersonaEnhancementEngine
    from core.complexity_analyzer import AnalysisComplexityDetector
except ImportError as e:
    print(f"🚨 IMPORT ERROR: {e}")
    print(f"🔍 sys.path[0]: {sys.path[0]}")
    print(f"🔍 lib_path: {lib_path}")
    print(f"🔍 lib_path exists: {Path(lib_path).exists()}")
    print(f"🔍 personas dir exists: {Path(lib_path, 'personas').exists()}")
    raise


class TestPersonaChallengeP0(unittest.TestCase):
    """
    P0 Tests for Persona Challenge Framework

    BUSINESS CRITICAL REQUIREMENTS:
    - 80%+ challenge detection accuracy
    - Persona voice preservation during challenges
    - <100ms performance overhead
    - Integration with PersonaEnhancementEngine
    """

    def setUp(self):
        """Set up test environment"""
        self.challenge_framework = StrategicChallengeFramework()

        # Test personas
        self.test_personas = ["diego", "camille", "rachel", "alvaro", "martin"]

        # Test inputs that should trigger challenges
        self.challenge_trigger_inputs = [
            "We obviously need to hire more engineers",
            "Everyone knows microservices are the best practice",
            "The solution is clearly to use React",
            "We should definitely implement this feature",
            "This approach always works well",
            "The problem is our deployment process is too slow",
            "We need to optimize our database performance",
            "The budget constraints make this impossible",
            "Users expect this functionality",
            "The team prefers this technology stack",
        ]

        # Test inputs that should NOT trigger challenges
        self.non_challenge_inputs = [
            "What time is it?",
            "How are you doing today?",
            "Can you help me understand this concept?",
            "Thank you for the explanation",
            "I appreciate your help",
        ]

    def test_challenge_framework_availability(self):
        """P0: Challenge framework must be available and properly initialized"""
        # Framework instance exists
        self.assertIsNotNone(self.challenge_framework)
        self.assertIsNotNone(strategic_challenge_framework)

        # Configuration loaded successfully
        self.assertIsNotNone(self.challenge_framework.config)
        self.assertGreater(len(self.challenge_framework.challenge_patterns), 0)
        self.assertGreater(len(self.challenge_framework.persona_styles), 0)

        # All required personas configured
        for persona in self.test_personas:
            self.assertIn(persona, self.challenge_framework.persona_styles)

        print("✅ P0: Challenge framework availability validated")

    def test_persona_challenge_accuracy(self):
        """P0: Challenge detection must achieve 80%+ accuracy"""
        total_tests = 0
        correct_detections = 0

        # Test challenge trigger inputs (should detect challenges)
        for user_input in self.challenge_trigger_inputs:
            for persona in self.test_personas:
                total_tests += 1
                challenge_types = self.challenge_framework.should_challenge(
                    user_input, persona
                )

                if len(challenge_types) > 0:
                    correct_detections += 1
                else:
                    print(f"❌ Missed challenge: '{user_input}' for {persona}")

        # Test non-challenge inputs (should NOT detect challenges)
        for user_input in self.non_challenge_inputs:
            for persona in self.test_personas:
                total_tests += 1
                challenge_types = self.challenge_framework.should_challenge(
                    user_input, persona
                )

                if len(challenge_types) == 0:
                    correct_detections += 1
                else:
                    print(
                        f"❌ False positive: '{user_input}' for {persona} -> {challenge_types}"
                    )

        # Calculate accuracy
        accuracy = (correct_detections / total_tests) * 100

        print(
            f"📊 Challenge Detection Accuracy: {accuracy:.1f}% ({correct_detections}/{total_tests})"
        )

        # P0 REQUIREMENT: 80%+ accuracy
        self.assertGreaterEqual(
            accuracy,
            80.0,
            f"Challenge detection accuracy {accuracy:.1f}% below required 80%",
        )

        print("✅ P0: Challenge detection accuracy meets 80%+ requirement")

    def test_challenge_response_quality_threshold(self):
        """P0: Challenge responses must maintain quality and persona voice"""
        test_cases = [
            ("We obviously need more engineers", "diego"),
            ("Everyone knows React is the best", "rachel"),
            ("This solution always works", "martin"),
            ("The budget makes this impossible", "alvaro"),
            ("Users definitely want this feature", "camille"),
        ]

        for user_input, persona in test_cases:
            # Generate challenge response
            challenge_types = self.challenge_framework.should_challenge(
                user_input, persona
            )
            self.assertGreater(
                len(challenge_types), 0, f"Should challenge: {user_input}"
            )

            challenge_response = self.challenge_framework.generate_challenge_response(
                user_input, persona, challenge_types
            )

            # Quality checks
            self.assertIsInstance(challenge_response, str)
            self.assertGreater(
                len(challenge_response), 10, "Challenge response too short"
            )
            self.assertLess(
                len(challenge_response), 1000, "Challenge response too long"
            )

            # Must contain challenge indicators
            self.assertTrue(
                any(
                    indicator in challenge_response.lower()
                    for indicator in [
                        "challenge",
                        "assumption",
                        "evidence",
                        "validation",
                        "what if",
                    ]
                ),
                f"Challenge response lacks challenge indicators: {challenge_response}",
            )

            # Must be professional (no aggressive/inflammatory language)
            # Updated for Phase 4: Allow assertive professional language while blocking truly aggressive terms
            aggressive_words = [
                "stupid",
                "idiotic",
                "moronic",
                "dumb",
                "ridiculous",
                "pathetic",
                "worthless",
                "garbage",
                "trash",
                "useless",
                "incompetent",
                "clueless",
                "hopeless",
                "disaster",
            ]

            # Assertive professional terms are allowed: "fail", "wrong", "bad", "terrible", "awful",
            # "catastrophically", "critically", "significantly", "substantially"
            self.assertFalse(
                any(word in challenge_response.lower() for word in aggressive_words),
                f"Challenge response contains aggressive/inflammatory language: {challenge_response}",
            )

        print("✅ P0: Challenge response quality meets professional standards")

    def test_challenge_framework_performance(self):
        """P0: Challenge framework must perform within <100ms overhead"""
        test_input = "We obviously need to implement microservices because everyone knows they're the best practice"
        performance_samples = []

        # Run multiple performance tests
        for _ in range(10):
            start_time = time.time()

            # Test challenge detection
            challenge_types = self.challenge_framework.should_challenge(
                test_input, "diego"
            )

            # Test challenge response generation
            if challenge_types:
                challenge_response = (
                    self.challenge_framework.generate_challenge_response(
                        test_input, "diego", challenge_types
                    )
                )

            end_time = time.time()
            processing_time_ms = (end_time - start_time) * 1000
            performance_samples.append(processing_time_ms)

        # Calculate average performance
        avg_performance = sum(performance_samples) / len(performance_samples)
        max_performance = max(performance_samples)

        print(f"📊 Challenge Framework Performance:")
        print(f"   Average: {avg_performance:.2f}ms")
        print(f"   Maximum: {max_performance:.2f}ms")
        print(f"   Target: <100ms")

        # P0 REQUIREMENT: <100ms overhead
        self.assertLess(
            avg_performance,
            100.0,
            f"Average challenge processing time {avg_performance:.2f}ms exceeds 100ms limit",
        )

        self.assertLess(
            max_performance,
            200.0,  # Allow some variance for max
            f"Maximum challenge processing time {max_performance:.2f}ms too high",
        )

        print("✅ P0: Challenge framework performance meets <100ms requirement")

    def test_persona_enhancement_engine_integration(self):
        """P0: Challenge framework must integrate with PersonaEnhancementEngine"""
        try:
            # Create PersonaEnhancementEngine with challenge framework enabled
            complexity_detector = AnalysisComplexityDetector()
            config = {"enable_challenge_framework": True}

            enhancement_engine = PersonaEnhancementEngine(
                complexity_detector=complexity_detector, config=config
            )

            # Verify challenge framework is integrated
            self.assertTrue(enhancement_engine.challenge_enabled)
            self.assertIsNotNone(enhancement_engine.challenge_framework)

            # Test integration with a challenging input
            test_input = "We should obviously use microservices for everything"
            base_response = "That's an interesting architectural consideration."

            # Test the _apply_challenge_framework method
            enhanced_response = enhancement_engine._apply_challenge_framework(
                base_response, test_input, "martin"
            )

            # Verify challenge was applied
            self.assertNotEqual(enhanced_response, base_response)
            # Check for challenge indicators (various forms)
            challenge_indicators = [
                "challenge",
                "push back",
                "assumptions",
                "evidence",
                "validation",
            ]
            self.assertTrue(
                any(
                    indicator in enhanced_response.lower()
                    for indicator in challenge_indicators
                ),
                f"Enhanced response should contain challenge indicators: {enhanced_response}",
            )

            print("✅ P0: PersonaEnhancementEngine integration successful")

        except Exception as e:
            self.fail(f"PersonaEnhancementEngine integration failed: {e}")

    def test_configuration_system_robustness(self):
        """P0: Configuration system must handle errors gracefully"""
        # Test with invalid config path
        try:
            invalid_framework = StrategicChallengeFramework(
                config_path="/nonexistent/path.yaml"
            )

            # Should fall back to minimal configuration
            self.assertIsNotNone(invalid_framework.config)
            self.assertEqual(invalid_framework.config.version, "1.0.0-fallback")

            # Should still be functional with fallback
            challenge_types = invalid_framework.should_challenge(
                "We should obviously do this", "diego"
            )
            self.assertIsInstance(challenge_types, list)

            print("✅ P0: Configuration system graceful fallback works")

        except Exception as e:
            self.fail(f"Configuration system should handle errors gracefully: {e}")

    def test_persona_voice_preservation(self):
        """P0: Challenge framework must preserve persona authenticity"""
        test_cases = [
            ("We obviously need more budget", "alvaro"),  # Business focus
            ("Users clearly want this feature", "rachel"),  # User focus
            (
                "The architecture should obviously be microservices",
                "martin",
            ),  # Technical focus
            ("Teams definitely prefer this process", "diego"),  # Organizational focus
            ("Executives clearly expect this outcome", "camille"),  # Strategic focus
        ]

        for user_input, persona in test_cases:
            challenge_types = self.challenge_framework.should_challenge(
                user_input, persona
            )

            if challenge_types:
                challenge_response = (
                    self.challenge_framework.generate_challenge_response(
                        user_input, persona, challenge_types
                    )
                )

                # Check for persona-specific challenge patterns
                persona_config = self.challenge_framework.persona_styles.get(
                    persona, {}
                )
                domain = persona_config.get("domain", "")

                # Verify domain-appropriate challenges
                if persona == "alvaro":
                    self.assertTrue(
                        any(
                            word in challenge_response.lower()
                            for word in ["business", "roi", "investment", "market"]
                        ),
                        f"Alvaro challenge should include business terms: {challenge_response}",
                    )
                elif persona == "rachel":
                    self.assertTrue(
                        any(
                            word in challenge_response.lower()
                            for word in [
                                "user",
                                "design",
                                "experience",
                                "accessibility",
                            ]
                        ),
                        f"Rachel challenge should include UX terms: {challenge_response}",
                    )
                elif persona == "martin":
                    self.assertTrue(
                        any(
                            word in challenge_response.lower()
                            for word in [
                                "technical",
                                "architecture",
                                "performance",
                                "scalability",
                            ]
                        ),
                        f"Martin challenge should include technical terms: {challenge_response}",
                    )

        print("✅ P0: Persona voice preservation validated")


if __name__ == "__main__":
    # Run P0 tests with detailed output
    unittest.main(verbosity=2)
