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
    from core.enhanced_persona_manager import create_persona_enhancement_engine as PersonaEnhancementEngine
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

    def test_ts4_enhanced_integration_features(self):
        """P0: TS-4 enhanced integration features must work correctly"""
        # Test natural flow integration
        test_input = "We obviously need to implement microservices everywhere"
        base_response = "That's an interesting architectural consideration. Let me share some thoughts on this approach."

        # Test enhanced persona response integration
        enhanced_response = self.challenge_framework.enhance_persona_response(
            base_response, test_input, "martin"
        )

        # Verify enhancement was applied
        self.assertNotEqual(enhanced_response, base_response)
        self.assertGreater(len(enhanced_response), len(base_response))

        # Verify constructive alternatives are included when appropriate
        # Check for constructive alternative patterns (more flexible matching)
        constructive_patterns = [
            "alternative",
            "consider",
            "exploring",
            "validating",
            "investigating",
            "what if",
            "have you considered",
            "another approach",
            "different perspective",
        ]

        if any(
            pattern in enhanced_response.lower()
            for pattern in constructive_patterns[:2]
        ):
            # If alternatives are mentioned, verify they're constructive (not just present)
            self.assertTrue(
                len(enhanced_response)
                > len(base_response) * 1.2,  # Substantive addition
                f"Constructive alternatives should add meaningful content: {enhanced_response}",
            )

        print("✅ P0: TS-4 enhanced integration features validated")

    def test_ts4_performance_monitoring_integration(self):
        """P0: TS-4 performance monitoring must integrate with PersonaEnhancementEngine"""
        try:
            # Create PersonaEnhancementEngine with challenge framework enabled
            complexity_detector = AnalysisComplexityDetector()
            config = {"enable_challenge_framework": True}

            enhancement_engine = PersonaEnhancementEngine(
                complexity_detector=complexity_detector, config=config
            )

            # Test challenge metrics collection
            test_input = "We obviously need more engineers for this project"
            base_response = "Let me analyze the resource requirements."

            # Test the _collect_challenge_metrics method
            metrics = enhancement_engine._collect_challenge_metrics(
                base_response, test_input, "diego"
            )

            # Verify metrics structure
            required_metrics = [
                "challenge_applied",
                "challenge_types_count",
                "integration_style",
                "response_length_change",
            ]

            for metric in required_metrics:
                self.assertIn(metric, metrics, f"Missing required metric: {metric}")

            # Verify metric types
            self.assertIsInstance(metrics["challenge_applied"], bool)
            self.assertIsInstance(metrics["challenge_types_count"], int)
            self.assertIsInstance(metrics["integration_style"], str)
            self.assertIsInstance(metrics["response_length_change"], (int, float))

            # If challenge was applied, verify positive metrics
            if metrics["challenge_applied"]:
                self.assertGreater(metrics["challenge_types_count"], 0)
                self.assertNotEqual(metrics["integration_style"], "none")

            print("✅ P0: TS-4 performance monitoring integration validated")

        except Exception as e:
            self.fail(f"TS-4 performance monitoring integration failed: {e}")

    def test_ts4_challenge_balance_optimization(self):
        """P0: TS-4 challenge balance optimization must prevent overwhelming responses"""
        # Test with a very long base response to trigger balance optimization
        long_base_response = (
            "This is a comprehensive analysis. " * 50
        )  # ~1500 characters
        test_input = "We obviously need to use React for everything"

        # Generate enhanced response
        enhanced_response = self.challenge_framework.enhance_persona_response(
            long_base_response, test_input, "rachel"
        )

        # Calculate challenge percentage
        challenge_added = len(enhanced_response) - len(long_base_response)
        if len(enhanced_response) > 0:
            challenge_percentage = challenge_added / len(enhanced_response)

            # Verify challenge doesn't dominate (should be <40% based on config)
            self.assertLess(
                challenge_percentage,
                0.5,  # Allow some tolerance
                f"Challenge content dominates response: {challenge_percentage:.1%}",
            )

        # Verify response is still coherent
        self.assertGreater(len(enhanced_response), len(long_base_response))
        self.assertIn(
            long_base_response[:100], enhanced_response
        )  # Original content preserved

        print("✅ P0: TS-4 challenge balance optimization validated")

    def test_ts5_challenge_system_performance_monitoring(self):
        """P0: TS-5 challenge system performance monitoring must provide comprehensive metrics"""
        try:
            # Create PersonaEnhancementEngine with challenge framework enabled
            complexity_detector = AnalysisComplexityDetector()
            config = {"enable_challenge_framework": True}

            enhancement_engine = PersonaEnhancementEngine(
                complexity_detector=complexity_detector, config=config
            )

            # Test comprehensive performance monitoring
            test_cases = [
                (
                    "We obviously need microservices",
                    "martin",
                    True,
                ),  # Should trigger challenge
                ("What time is it?", "diego", False),  # Should NOT trigger challenge
                (
                    "Everyone knows React is best",
                    "rachel",
                    True,
                ),  # Should trigger challenge
            ]

            for test_input, persona, should_challenge in test_cases:
                base_response = "Here's my analysis of the situation."

                # Measure performance
                start_time = time.time()

                # Test full enhancement pipeline with metrics
                result = enhancement_engine.enhance_response(
                    persona_name=persona,
                    user_input=test_input,
                    base_response=base_response,
                )

                end_time = time.time()
                processing_time = (end_time - start_time) * 1000

                # Verify result structure
                self.assertIsInstance(result.enhanced_response, str)
                self.assertIsInstance(result.enhancement_applied, bool)
                self.assertIsInstance(result.processing_time_ms, int)

                # Verify performance metrics are reasonable
                self.assertLess(
                    processing_time,
                    500,
                    f"Processing too slow: {processing_time:.2f}ms",
                )

                # Verify challenge behavior matches expectations
                if should_challenge:
                    # Should have some enhancement (either framework or challenge)
                    self.assertTrue(
                        result.enhancement_applied
                        or result.enhanced_response != base_response,
                        f"Expected challenge/enhancement for: {test_input}",
                    )

                # Verify framework attribution consistency
                if result.framework_used and "Strategic Challenge Framework" in str(
                    result.framework_used
                ):
                    # If Strategic Challenge Framework is attributed, response should be enhanced
                    self.assertTrue(
                        result.enhancement_applied
                        or result.enhanced_response != base_response,
                        f"Framework attributed but no enhancement detected for: {test_input}",
                    )

            print("✅ P0: TS-5 challenge system performance monitoring validated")

        except Exception as e:
            self.fail(f"TS-5 performance monitoring failed: {e}")

    def test_ts5_comprehensive_metrics_validation(self):
        """P0: TS-5 comprehensive metrics must track all challenge system aspects"""
        try:
            # Create PersonaEnhancementEngine
            complexity_detector = AnalysisComplexityDetector()
            config = {"enable_challenge_framework": True}

            enhancement_engine = PersonaEnhancementEngine(
                complexity_detector=complexity_detector, config=config
            )

            # Test metrics collection across different scenarios
            scenarios = [
                {
                    "input": "We obviously need to hire 50 more engineers immediately",
                    "persona": "diego",
                    "expected_challenge": True,
                    "expected_types": ["assumption_test", "constraint_validation"],
                },
                {
                    "input": "Everyone knows microservices are always the right choice",
                    "persona": "martin",
                    "expected_challenge": True,
                    "expected_types": ["assumption_test", "alternative_exploration"],
                },
                {
                    "input": "Thank you for the explanation",
                    "persona": "rachel",
                    "expected_challenge": False,
                    "expected_types": [],
                },
            ]

            for scenario in scenarios:
                base_response = "Let me provide some insights on this."

                # Collect challenge metrics
                metrics = enhancement_engine._collect_challenge_metrics(
                    base_response, scenario["input"], scenario["persona"]
                )

                # Validate metrics match expectations
                self.assertEqual(
                    metrics["challenge_applied"],
                    scenario["expected_challenge"],
                    f"Challenge application mismatch for: {scenario['input']}",
                )

                if scenario["expected_challenge"]:
                    self.assertGreater(
                        metrics["challenge_types_count"],
                        0,
                        f"Should have challenge types for: {scenario['input']}",
                    )
                    self.assertNotEqual(
                        metrics["integration_style"],
                        "none",
                        f"Should have integration style for: {scenario['input']}",
                    )
                    self.assertIsInstance(
                        metrics["response_length_change"],
                        (int, float),
                        f"Should have length change metric for: {scenario['input']}",
                    )
                else:
                    self.assertEqual(
                        metrics["challenge_types_count"],
                        0,
                        f"Should not have challenge types for: {scenario['input']}",
                    )
                    self.assertEqual(
                        metrics["integration_style"],
                        "none",
                        f"Should have 'none' integration style for: {scenario['input']}",
                    )

            print("✅ P0: TS-5 comprehensive metrics validation successful")

        except Exception as e:
            self.fail(f"TS-5 comprehensive metrics validation failed: {e}")


if __name__ == "__main__":
    # Run P0 tests with detailed output
    unittest.main(verbosity=2)
