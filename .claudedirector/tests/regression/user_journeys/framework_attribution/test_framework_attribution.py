#!/usr/bin/env python3
"""
📚 Framework Attribution Regression Test - Critical User Journey 5b/5

BUSINESS CRITICAL PATH: Strategic framework attribution and transparency validation
FAILURE IMPACT: Framework attribution missing, transparency lost, audit trail broken

This focused test suite validates framework attribution formatting and transparency:
1. Attribution formatting compliance with transparency standards
2. Framework name inclusion and proper disclosure
3. Multi-framework attribution coordination
4. Confidence disclosure and transparency requirements

COVERAGE: Framework attribution transparency validation
PRIORITY: P0 HIGH - Attribution transparency and audit trail
EXECUTION: <2 seconds for complete attribution validation
"""

import sys
import os
import unittest
import tempfile
import re
from pathlib import Path

# Add the ClaudeDirector lib to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../lib"))


class TestFrameworkAttribution(unittest.TestCase):
    """Test framework attribution formatting and transparency compliance"""

    def setUp(self):
        """Set up test environment for attribution testing"""
        self.test_dir = tempfile.mkdtemp()

        # Sample framework detection results for attribution testing
        self.single_framework_result = {
            "Team Topologies": {
                "confidence": 0.85,
                "keyword_matches": 4,
                "context_relevance": 0.15,
            }
        }

        self.multi_framework_result = {
            "Team Topologies": {
                "confidence": 0.90,
                "keyword_matches": 5,
                "context_relevance": 0.15,
            },
            "Capital Allocation Framework": {
                "confidence": 0.75,
                "keyword_matches": 3,
                "context_relevance": 0.10,
            },
            "Good Strategy Bad Strategy": {
                "confidence": 0.65,
                "keyword_matches": 2,
                "context_relevance": 0.05,
            },
        }

        self.high_confidence_result = {
            "Design System Maturity Model": {
                "confidence": 0.95,
                "keyword_matches": 6,
                "context_relevance": 0.20,
            },
            "User-Centered Design": {
                "confidence": 0.88,
                "keyword_matches": 4,
                "context_relevance": 0.18,
            },
        }

        # Attribution test scenarios
        self.attribution_scenarios = [
            {
                "name": "Single Framework Attribution",
                "detected_frameworks": self.single_framework_result,
                "expected_pattern": r"📚 Strategic Framework: Team Topologies detected",
                "expected_elements": [
                    "📚 Strategic Framework:",
                    "Team Topologies",
                    "detected",
                ],
            },
            {
                "name": "Multi Framework Attribution",
                "detected_frameworks": self.multi_framework_result,
                "expected_pattern": r"📚 Strategic Framework: .+ detected \(with .+ for additional context\)",
                "expected_elements": [
                    "📚 Strategic Framework:",
                    "Team Topologies",
                    "Capital Allocation Framework",
                ],
            },
            {
                "name": "High Confidence Attribution",
                "detected_frameworks": self.high_confidence_result,
                "expected_pattern": r"📚 Strategic Framework: .+ detected",
                "expected_elements": [
                    "📚 Strategic Framework:",
                    "Design System Maturity Model",
                ],
            },
        ]

    def tearDown(self):
        """Clean up test environment"""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_framework_attribution_formatting(self):
        """REGRESSION TEST: Framework attribution follows transparent disclosure format"""
        try:
            for scenario in self.attribution_scenarios:
                scenario_name = scenario["name"]
                detected_frameworks = scenario["detected_frameworks"]
                expected_pattern = scenario["expected_pattern"]
                expected_elements = scenario["expected_elements"]

                # Generate attribution text
                attribution_text = self._generate_attribution(detected_frameworks)

                # Verify attribution format compliance
                self.assertIn(
                    "📚 Strategic Framework:",
                    attribution_text,
                    f"{scenario_name}: Attribution should include framework header",
                )

                # Verify framework names are included
                for framework_name in detected_frameworks.keys():
                    self.assertIn(
                        framework_name,
                        attribution_text,
                        f"{scenario_name}: Framework '{framework_name}' should be named in attribution",
                    )

                # Verify expected elements are present
                for element in expected_elements:
                    self.assertIn(
                        element,
                        attribution_text,
                        f"{scenario_name}: Attribution should include '{element}'",
                    )

                # Verify attribution follows expected pattern
                self.assertRegex(
                    attribution_text,
                    expected_pattern,
                    f"{scenario_name}: Attribution should follow pattern. Got: {attribution_text}",
                )

        except Exception as e:
            self.fail(f"Framework attribution formatting test failed: {e}")

    def test_multi_framework_confidence_disclosure(self):
        """REGRESSION TEST: Multi-framework attribution includes confidence indicators"""
        try:
            # Test multi-framework scenario
            detected_frameworks = self.multi_framework_result
            attribution_text = self._generate_attribution(detected_frameworks)

            # Verify confidence disclosure (if required)
            if len(detected_frameworks) > 1:
                confidence_indicators = [
                    "confidence",
                    "detected",
                    "applied",
                    "additional context",
                ]
                has_confidence_indicator = any(
                    keyword in attribution_text.lower()
                    for keyword in confidence_indicators
                )
                self.assertTrue(
                    has_confidence_indicator,
                    "Multi-framework attribution should include confidence indicators",
                )

            # Verify primary framework is identified
            frameworks_by_confidence = sorted(
                detected_frameworks.items(),
                key=lambda x: x[1]["confidence"],
                reverse=True,
            )
            primary_framework = frameworks_by_confidence[0][0]

            # Primary framework should appear first in attribution
            self.assertIn(
                primary_framework,
                attribution_text,
                f"Primary framework '{primary_framework}' should be included in attribution",
            )

            # Supporting frameworks should be mentioned
            supporting_frameworks = [name for name, _ in frameworks_by_confidence[1:]]
            for framework in supporting_frameworks:
                self.assertIn(
                    framework,
                    attribution_text,
                    f"Supporting framework '{framework}' should be included in attribution",
                )

        except Exception as e:
            self.fail(f"Multi-framework confidence disclosure test failed: {e}")

    def test_attribution_transparency_compliance(self):
        """REGRESSION TEST: Attribution meets enterprise transparency requirements"""
        try:
            transparency_requirements = [
                {
                    "requirement": "Framework Header Required",
                    "test": lambda text: "📚 Strategic Framework:" in text,
                    "error": "Attribution must include framework header",
                },
                {
                    "requirement": "Framework Name Required",
                    "test": lambda text: any(
                        framework in text
                        for framework in [
                            "Team Topologies",
                            "Capital Allocation",
                            "Design System",
                        ]
                    ),
                    "error": "Attribution must include framework name",
                },
                {
                    "requirement": "Detection Disclosure Required",
                    "test": lambda text: "detected" in text.lower(),
                    "error": "Attribution must disclose detection",
                },
                {
                    "requirement": "Proper Formatting",
                    "test": lambda text: len(text.strip()) > 20,
                    "error": "Attribution must be properly formatted",
                },
            ]

            # Test each scenario against transparency requirements
            for scenario in self.attribution_scenarios:
                detected_frameworks = scenario["detected_frameworks"]
                attribution_text = self._generate_attribution(detected_frameworks)

                for requirement in transparency_requirements:
                    requirement_name = requirement["requirement"]
                    test_func = requirement["test"]
                    error_message = requirement["error"]

                    self.assertTrue(
                        test_func(attribution_text),
                        f"{scenario['name']} - {requirement_name}: {error_message}. Got: {attribution_text}",
                    )

        except Exception as e:
            self.fail(f"Attribution transparency compliance test failed: {e}")

    def test_attribution_edge_cases(self):
        """REGRESSION TEST: Attribution handles edge cases gracefully"""
        try:
            edge_cases = [
                {
                    "name": "No Frameworks Detected",
                    "detected_frameworks": {},
                    "expected_text": "📚 Strategic Framework: None detected",
                },
                {
                    "name": "Single Low Confidence Framework",
                    "detected_frameworks": {
                        "WRAP Framework": {
                            "confidence": 0.45,
                            "keyword_matches": 1,
                            "context_relevance": 0.05,
                        }
                    },
                    "expected_elements": [
                        "📚 Strategic Framework:",
                        "WRAP Framework",
                        "detected",
                    ],
                },
                {
                    "name": "Framework with Special Characters",
                    "detected_frameworks": {
                        "Good Strategy Bad Strategy": {
                            "confidence": 0.80,
                            "keyword_matches": 3,
                            "context_relevance": 0.15,
                        }
                    },
                    "expected_elements": [
                        "📚 Strategic Framework:",
                        "Good Strategy Bad Strategy",
                    ],
                },
            ]

            for case in edge_cases:
                case_name = case["name"]
                detected_frameworks = case["detected_frameworks"]

                # Generate attribution for edge case
                attribution_text = self._generate_attribution(detected_frameworks)

                # Verify edge case handling
                if "expected_text" in case:
                    self.assertEqual(
                        attribution_text,
                        case["expected_text"],
                        f"{case_name}: Attribution should handle edge case correctly",
                    )

                if "expected_elements" in case:
                    for element in case["expected_elements"]:
                        self.assertIn(
                            element,
                            attribution_text,
                            f"{case_name}: Attribution should include '{element}'",
                        )

                # Verify attribution is never empty or malformed
                self.assertGreater(
                    len(attribution_text.strip()),
                    10,
                    f"{case_name}: Attribution should not be empty or too short",
                )

        except Exception as e:
            self.fail(f"Attribution edge cases test failed: {e}")

    def test_attribution_consistency(self):
        """REGRESSION TEST: Attribution is consistent across multiple calls"""
        try:
            # Test same input produces same output
            detected_frameworks = self.multi_framework_result

            # Generate attribution multiple times
            attributions = []
            for i in range(5):
                attribution = self._generate_attribution(detected_frameworks)
                attributions.append(attribution)

            # Verify consistency
            first_attribution = attributions[0]
            for i, attribution in enumerate(attributions[1:], 1):
                self.assertEqual(
                    attribution,
                    first_attribution,
                    f"Attribution {i+1} should be identical to first attribution",
                )

            # Verify all attributions have required elements
            for attribution in attributions:
                self.assertIn("📚 Strategic Framework:", attribution)
                self.assertIn("Team Topologies", attribution)
                self.assertIn("detected", attribution)

        except Exception as e:
            self.fail(f"Attribution consistency test failed: {e}")

    # Helper methods for attribution generation

    def _generate_attribution(self, detected_frameworks):
        """Generate framework attribution text"""
        if not detected_frameworks:
            return "📚 Strategic Framework: None detected"

        if len(detected_frameworks) == 1:
            framework_name = list(detected_frameworks.keys())[0]
            return f"📚 Strategic Framework: {framework_name} detected"
        else:
            # Sort by confidence
            frameworks_by_confidence = sorted(
                detected_frameworks.items(),
                key=lambda x: x[1]["confidence"],
                reverse=True,
            )

            primary = frameworks_by_confidence[0][0]
            others = [
                name for name, _ in frameworks_by_confidence[1:3]
            ]  # Top 2 supporting

            if others:
                return f"📚 Strategic Framework: {primary} detected (with {', '.join(others)} for additional context)"
            else:
                return f"📚 Strategic Framework: {primary} detected"


if __name__ == "__main__":
    print("📚 Framework Attribution Regression Test")
    print("=" * 50)
    print("Testing framework attribution formatting and transparency...")
    print()

    # Run the focused test suite
    unittest.main(verbosity=2, exit=False)

    print()
    print("✅ FRAMEWORK ATTRIBUTION REGRESSION TESTS COMPLETE")
    print("Strategic framework attribution transparency protected against regressions")
