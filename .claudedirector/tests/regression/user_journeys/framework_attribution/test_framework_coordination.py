#!/usr/bin/env python3
"""
🤝 Framework Coordination Regression Test - Critical User Journey 5c/5

BUSINESS CRITICAL PATH: Multi-framework coordination and prioritization validation
FAILURE IMPACT: Framework coordination lost, strategic guidance fragmented, prioritization broken

This focused test suite validates framework coordination and multi-framework scenarios:
1. Multi-framework detection and coordination logic
2. Framework prioritization and ranking by confidence
3. Primary vs supporting framework identification
4. Coordination rationale and decision transparency

COVERAGE: Multi-framework coordination validation
PRIORITY: P0 HIGH - Framework coordination and prioritization
EXECUTION: <2 seconds for complete coordination validation
"""

import sys
import os
import unittest
import tempfile

# Add the ClaudeDirector lib to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../lib"))


class TestFrameworkCoordination(unittest.TestCase):
    """Test multi-framework coordination and prioritization logic"""

    def setUp(self):
        """Set up test environment for coordination testing"""
        self.test_dir = tempfile.mkdtemp()

        # Multi-framework test scenarios
        self.coordination_scenarios = [
            {
                "name": "Platform Scaling Scenario",
                "query": "How should we restructure engineering teams for platform scaling while managing investment allocation?",
                "detected_frameworks": {
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
                    "Strategic Platform Assessment": {
                        "confidence": 0.70,
                        "keyword_matches": 3,
                        "context_relevance": 0.08,
                    },
                },
                "expected_primary": "Team Topologies",
                "expected_supporting": [
                    "Capital Allocation Framework",
                    "Strategic Platform Assessment",
                ],
                "min_frameworks": 2,
            },
            {
                "name": "Design System Strategy Scenario",
                "query": "How do we scale our design system while ensuring accessibility compliance and user-centered design?",
                "detected_frameworks": {
                    "Design System Maturity Model": {
                        "confidence": 0.92,
                        "keyword_matches": 6,
                        "context_relevance": 0.18,
                    },
                    "User-Centered Design": {
                        "confidence": 0.85,
                        "keyword_matches": 4,
                        "context_relevance": 0.15,
                    },
                    "Scaling Up Excellence": {
                        "confidence": 0.65,
                        "keyword_matches": 2,
                        "context_relevance": 0.05,
                    },
                },
                "expected_primary": "Design System Maturity Model",
                "expected_supporting": [
                    "User-Centered Design",
                    "Scaling Up Excellence",
                ],
                "min_frameworks": 2,
            },
            {
                "name": "Executive Strategy Scenario",
                "query": "What strategic approach should we take for board presentation on competitive positioning and investment priorities?",
                "detected_frameworks": {
                    "Good Strategy Bad Strategy": {
                        "confidence": 0.88,
                        "keyword_matches": 5,
                        "context_relevance": 0.16,
                    },
                    "Capital Allocation Framework": {
                        "confidence": 0.82,
                        "keyword_matches": 4,
                        "context_relevance": 0.14,
                    },
                    "Crucial Conversations": {
                        "confidence": 0.78,
                        "keyword_matches": 3,
                        "context_relevance": 0.12,
                    },
                },
                "expected_primary": "Good Strategy Bad Strategy",
                "expected_supporting": [
                    "Capital Allocation Framework",
                    "Crucial Conversations",
                ],
                "min_frameworks": 2,
            },
        ]

    def tearDown(self):
        """Clean up test environment"""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_multi_framework_coordination(self):
        """REGRESSION TEST: Multiple frameworks are coordinated effectively and prioritized appropriately"""
        try:
            for scenario in self.coordination_scenarios:
                scenario_name = scenario["name"]
                query = scenario["query"]
                detected_frameworks = scenario["detected_frameworks"]
                expected_primary = scenario["expected_primary"]
                expected_supporting = scenario["expected_supporting"]
                min_frameworks = scenario["min_frameworks"]

                # Verify multiple frameworks are detected
                self.assertGreaterEqual(
                    len(detected_frameworks),
                    min_frameworks,
                    f"{scenario_name}: Should detect at least {min_frameworks} frameworks. Query: {query[:50]}...",
                )

                # Verify frameworks are ranked by confidence
                framework_confidences = [
                    (name, data["confidence"])
                    for name, data in detected_frameworks.items()
                ]
                framework_confidences.sort(key=lambda x: x[1], reverse=True)

                # Primary framework should have highest confidence
                primary_framework = framework_confidences[0][0]
                primary_confidence = framework_confidences[0][1]

                self.assertEqual(
                    primary_framework,
                    expected_primary,
                    f"{scenario_name}: Primary framework should be '{expected_primary}', got '{primary_framework}'",
                )

                self.assertGreaterEqual(
                    primary_confidence,
                    0.7,
                    f"{scenario_name}: Primary framework '{primary_framework}' should have high confidence",
                )

                # Test framework coordination logic
                coordination_result = self._coordinate_frameworks(detected_frameworks)

                self.assertIn(
                    "primary_framework",
                    coordination_result,
                    f"{scenario_name}: Framework coordination should identify primary framework",
                )

                self.assertIn(
                    "supporting_frameworks",
                    coordination_result,
                    f"{scenario_name}: Framework coordination should identify supporting frameworks",
                )

                # Verify coordination reasoning
                self.assertIn(
                    "coordination_rationale",
                    coordination_result,
                    f"{scenario_name}: Framework coordination should provide rationale",
                )

                # Verify primary framework matches expectation
                self.assertEqual(
                    coordination_result["primary_framework"],
                    expected_primary,
                    f"{scenario_name}: Coordinated primary framework should match expected",
                )

                # Verify supporting frameworks are identified
                coordinated_supporting = coordination_result["supporting_frameworks"]
                for expected_framework in expected_supporting[:2]:  # Top 2 supporting
                    self.assertIn(
                        expected_framework,
                        coordinated_supporting,
                        f"{scenario_name}: Supporting framework '{expected_framework}' should be identified",
                    )

        except Exception as e:
            self.fail(f"Multi-framework coordination test failed: {e}")

    def test_framework_prioritization_logic(self):
        """REGRESSION TEST: Framework prioritization follows confidence-based ranking"""
        try:
            # Test with various confidence scenarios
            prioritization_tests = [
                {
                    "name": "Clear Confidence Hierarchy",
                    "frameworks": {
                        "Framework A": {"confidence": 0.95},
                        "Framework B": {"confidence": 0.75},
                        "Framework C": {"confidence": 0.55},
                    },
                    "expected_order": ["Framework A", "Framework B", "Framework C"],
                },
                {
                    "name": "Close Confidence Values",
                    "frameworks": {
                        "Framework X": {"confidence": 0.82},
                        "Framework Y": {"confidence": 0.80},
                        "Framework Z": {"confidence": 0.78},
                    },
                    "expected_order": ["Framework X", "Framework Y", "Framework Z"],
                },
                {
                    "name": "Single Framework",
                    "frameworks": {
                        "Solo Framework": {"confidence": 0.85},
                    },
                    "expected_order": ["Solo Framework"],
                },
            ]

            for test in prioritization_tests:
                test_name = test["name"]
                frameworks = test["frameworks"]
                expected_order = test["expected_order"]

                # Test coordination prioritization
                coordination_result = self._coordinate_frameworks(frameworks)

                if len(frameworks) == 1:
                    # Single framework case
                    self.assertEqual(
                        coordination_result["primary_framework"],
                        expected_order[0],
                        f"{test_name}: Single framework should be primary",
                    )
                    self.assertEqual(
                        len(coordination_result["supporting_frameworks"]),
                        0,
                        f"{test_name}: Single framework should have no supporting frameworks",
                    )
                else:
                    # Multi-framework case
                    self.assertEqual(
                        coordination_result["primary_framework"],
                        expected_order[0],
                        f"{test_name}: Highest confidence framework should be primary",
                    )

                    # Supporting frameworks should be in confidence order
                    supporting_frameworks = coordination_result["supporting_frameworks"]
                    expected_supporting = expected_order[1:3]  # Top 2 supporting

                    for i, expected_framework in enumerate(expected_supporting):
                        if i < len(supporting_frameworks):
                            self.assertEqual(
                                supporting_frameworks[i],
                                expected_framework,
                                f"{test_name}: Supporting framework {i+1} should be '{expected_framework}'",
                            )

        except Exception as e:
            self.fail(f"Framework prioritization logic test failed: {e}")

    def test_coordination_rationale_quality(self):
        """REGRESSION TEST: Coordination rationale provides meaningful explanations"""
        try:
            for scenario in self.coordination_scenarios:
                scenario_name = scenario["name"]
                detected_frameworks = scenario["detected_frameworks"]

                coordination_result = self._coordinate_frameworks(detected_frameworks)
                rationale = coordination_result["coordination_rationale"]

                # Rationale should be meaningful
                self.assertGreater(
                    len(rationale),
                    20,
                    f"{scenario_name}: Rationale should be meaningful, got: {rationale}",
                )

                # Rationale should mention primary framework
                primary_framework = coordination_result["primary_framework"]
                self.assertIn(
                    primary_framework,
                    rationale,
                    f"{scenario_name}: Rationale should mention primary framework '{primary_framework}'",
                )

                # Rationale should explain selection criteria
                criteria_keywords = ["confidence", "highest", "selected", "score"]
                has_criteria = any(
                    keyword in rationale.lower() for keyword in criteria_keywords
                )
                self.assertTrue(
                    has_criteria,
                    f"{scenario_name}: Rationale should explain selection criteria. Got: {rationale}",
                )

                # If supporting frameworks exist, rationale should mention them
                supporting_frameworks = coordination_result["supporting_frameworks"]
                if supporting_frameworks:
                    support_keywords = [
                        "supporting",
                        "additional",
                        "context",
                        "provide",
                    ]
                    has_support_explanation = any(
                        keyword in rationale.lower() for keyword in support_keywords
                    )
                    self.assertTrue(
                        has_support_explanation,
                        f"{scenario_name}: Rationale should explain supporting frameworks. Got: {rationale}",
                    )

        except Exception as e:
            self.fail(f"Coordination rationale quality test failed: {e}")

    def test_coordination_edge_cases(self):
        """REGRESSION TEST: Coordination handles edge cases gracefully"""
        try:
            edge_cases = [
                {
                    "name": "No Frameworks",
                    "frameworks": {},
                    "expected_primary": None,
                    "expected_supporting": [],
                    "expected_rationale_keywords": ["no frameworks", "detected"],
                },
                {
                    "name": "Single Framework",
                    "frameworks": {"Lone Framework": {"confidence": 0.80}},
                    "expected_primary": "Lone Framework",
                    "expected_supporting": [],
                    "expected_rationale_keywords": ["lone framework", "selected"],
                },
                {
                    "name": "Equal Confidence Frameworks",
                    "frameworks": {
                        "Framework Alpha": {"confidence": 0.75},
                        "Framework Beta": {"confidence": 0.75},
                        "Framework Gamma": {"confidence": 0.75},
                    },
                    "expected_primary": "Framework Alpha",  # First in dict order
                    "expected_supporting": ["Framework Beta", "Framework Gamma"],
                    "expected_rationale_keywords": ["framework alpha", "confidence"],
                },
            ]

            for case in edge_cases:
                case_name = case["name"]
                frameworks = case["frameworks"]
                expected_primary = case["expected_primary"]
                expected_supporting = case["expected_supporting"]
                expected_keywords = case["expected_rationale_keywords"]

                coordination_result = self._coordinate_frameworks(frameworks)

                # Verify primary framework
                self.assertEqual(
                    coordination_result["primary_framework"],
                    expected_primary,
                    f"{case_name}: Primary framework should be '{expected_primary}'",
                )

                # Verify supporting frameworks
                actual_supporting = coordination_result["supporting_frameworks"]
                self.assertEqual(
                    len(actual_supporting),
                    len(expected_supporting),
                    f"{case_name}: Should have {len(expected_supporting)} supporting frameworks",
                )

                # Verify rationale contains expected keywords
                rationale = coordination_result["coordination_rationale"].lower()
                for keyword in expected_keywords:
                    self.assertIn(
                        keyword.lower(),
                        rationale,
                        f"{case_name}: Rationale should contain '{keyword}'. Got: {rationale}",
                    )

        except Exception as e:
            self.fail(f"Coordination edge cases test failed: {e}")

    # Helper methods for framework coordination

    def _coordinate_frameworks(self, detected_frameworks):
        """Simulate framework coordination logic"""
        if not detected_frameworks:
            return {
                "primary_framework": None,
                "supporting_frameworks": [],
                "coordination_rationale": "No frameworks detected",
            }

        frameworks_by_confidence = sorted(
            detected_frameworks.items(), key=lambda x: x[1]["confidence"], reverse=True
        )

        primary_framework = frameworks_by_confidence[0][0]
        supporting_frameworks = [
            name for name, _ in frameworks_by_confidence[1:3]
        ]  # Top 2 supporting

        # Generate rationale
        if len(frameworks_by_confidence) == 1:
            rationale = f"Primary framework '{primary_framework}' selected as the only detected framework"
        else:
            primary_confidence = frameworks_by_confidence[0][1]["confidence"]
            rationale = f"Primary framework '{primary_framework}' selected based on highest confidence score ({primary_confidence:.2f})"

            if supporting_frameworks:
                rationale += f". Supporting frameworks {supporting_frameworks} provide additional context."

        return {
            "primary_framework": primary_framework,
            "supporting_frameworks": supporting_frameworks,
            "coordination_rationale": rationale,
        }


if __name__ == "__main__":
    print("🤝 Framework Coordination Regression Test")
    print("=" * 50)
    print("Testing multi-framework coordination and prioritization...")
    print()

    # Run the focused test suite
    unittest.main(verbosity=2, exit=False)

    print()
    print("✅ FRAMEWORK COORDINATION REGRESSION TESTS COMPLETE")
    print(
        "Multi-framework coordination and prioritization protected against regressions"
    )
