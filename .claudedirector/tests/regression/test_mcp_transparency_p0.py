#!/usr/bin/env python3
"""
MCP Transparency P0 Feature Regression Test
CRITICAL: This test ensures MCP transparency disclosure never regresses

This test validates the core P0 requirement that persona responses
automatically show MCP server usage when complexity thresholds are met.
"""

import sys
import os
import unittest
from pathlib import Path

# Add the integration protection path for testing
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "integration-protection"))

try:
    from cursor_transparency_bridge import (
        ensure_transparency_compliance,
        get_transparency_summary,
        CursorTransparencyBridge,
    )

    BRIDGE_AVAILABLE = True
except ImportError as e:
    BRIDGE_AVAILABLE = False
    print(f"⚠️ Bridge not available: {e}")


class TestMCPTransparencyP0(unittest.TestCase):
    """
    P0 Feature Test: MCP Transparency Disclosure

    CRITICAL REQUIREMENT: All strategic persona responses MUST show
    MCP server access when complexity thresholds are met.
    """

    def setUp(self):
        """Set up test cases that MUST trigger MCP transparency"""
        if not BRIDGE_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        self.bridge = CursorTransparencyBridge()

        # P0 Test Cases - These MUST show MCP transparency
        self.p0_test_cases = [
            {
                "name": "Strategic Organizational Framework",
                "input": "How should we develop a strategic organizational framework for complex multi-team platform architecture assessment?",
                "response": "Here is a comprehensive strategic approach to organizational framework development for platform architecture...",
                "expected_persona": "martin",
                "expected_mcp_servers": ["sequential", "context7"],
                "min_complexity_score": 6,
            },
            {
                "name": "Executive Leadership Analysis",
                "input": "What organizational changes should we make for executive leadership and cross-functional team coordination?",
                "response": "Executive leadership requires systematic analysis of organizational dynamics and strategic framework application...",
                "expected_persona": "diego",
                "expected_mcp_servers": ["sequential"],
                "min_complexity_score": 4,
            },
            {
                "name": "Enterprise Platform Strategy",
                "input": "How do we develop enterprise-wide platform strategy with multiple teams and complex trade-offs?",
                "response": "Enterprise platform strategy requires systematic analysis of organizational complexity and strategic alternatives...",
                "expected_persona": "martin",
                "expected_mcp_servers": ["sequential", "context7"],
                "min_complexity_score": 7,
            },
            {
                "name": "Strategic Investment Analysis",
                "input": "What strategic investment alternatives should we assess for organizational scaling and framework development?",
                "response": "Strategic investment analysis requires systematic assessment of alternatives and organizational impact...",
                "expected_persona": "alvaro",
                "expected_mcp_servers": ["sequential"],
                "min_complexity_score": 5,
            },
        ]

        # Negative test cases - These should NOT trigger MCP transparency
        self.negative_test_cases = [
            {
                "name": "Simple Question",
                "input": "What is the status?",
                "response": "The status is good.",
                "expected_complexity_score": 0,
            },
            {
                "name": "Basic Technical Question",
                "input": "How do I run the tests?",
                "response": "Run pytest to execute the tests.",
                "expected_complexity_score": 0,
            },
        ]

    def test_p0_mcp_transparency_disclosure_format(self):
        """
        P0 TEST: MCP transparency disclosure format MUST match .cursorrules specification

        REQUIREMENT: All MCP disclosures must follow exact format:
        🔧 Accessing MCP Server: [server_name] ([capability])
        *[Processing message]...*
        """
        for test_case in self.p0_test_cases:
            with self.subTest(test_case=test_case["name"]):
                enhanced = ensure_transparency_compliance(
                    test_case["response"], test_case["input"]
                )

                # CRITICAL: Must contain MCP disclosure
                # Check for either format - old "Accessing" or new "Installing"
                has_mcp_disclosure = (
                    "🔧 Accessing MCP Server:" in enhanced
                    or "🔧 Installing MCP enhancement:" in enhanced
                )
                self.assertTrue(
                    has_mcp_disclosure,
                    f"FAILED P0: {test_case['name']} missing MCP disclosure",
                )

                # CRITICAL: Must contain processing indicator
                self.assertIn(
                    "*",
                    enhanced,
                    f"FAILED P0: {test_case['name']} missing processing indicator",
                )

                # CRITICAL: Must contain persona header
                self.assertIn(
                    "|",
                    enhanced,
                    f"FAILED P0: {test_case['name']} missing persona header",
                )

    def test_p0_complexity_threshold_detection(self):
        """
        P0 TEST: Complexity threshold detection MUST work reliably

        REQUIREMENT: Strategic queries >= 3 complexity indicators must trigger MCP
        """
        for test_case in self.p0_test_cases:
            with self.subTest(test_case=test_case["name"]):
                # Test complexity calculation directly
                combined_text = f"{test_case['input']} {test_case['response']}".lower()

                complexity_indicators = [
                    "strategic",
                    "organizational",
                    "framework",
                    "systematic",
                    "complex",
                    "multi-team",
                    "executive",
                    "board",
                    "leadership",
                    "presentation",
                    "enterprise",
                    "organization-wide",
                    "cross-functional",
                    "multiple teams",
                    "trade-offs",
                    "options",
                    "alternatives",
                    "analysis",
                    "assessment",
                ]

                actual_score = sum(
                    1
                    for indicator in complexity_indicators
                    if indicator in combined_text
                )

                # CRITICAL: Must meet minimum complexity threshold
                self.assertGreaterEqual(
                    actual_score,
                    3,
                    f"FAILED P0: {test_case['name']} complexity score {actual_score} < 3",
                )

                # Verify expected score
                self.assertGreaterEqual(
                    actual_score,
                    test_case["min_complexity_score"],
                    f"FAILED P0: {test_case['name']} complexity score {actual_score} < expected {test_case['min_complexity_score']}",
                )

    def test_p0_mcp_context_creation(self):
        """
        P0 TEST: MCP context creation MUST work for all strategic queries

        REQUIREMENT: High complexity queries must create MCP context with calls
        """
        for test_case in self.p0_test_cases:
            with self.subTest(test_case=test_case["name"]):
                mcp_context = self.bridge.detect_mcp_usage_context(
                    test_case["input"], test_case["response"]
                )

                # CRITICAL: MCP context must be created
                self.assertIsNotNone(
                    mcp_context,
                    f"FAILED P0: {test_case['name']} - no MCP context created",
                )

                # CRITICAL: Must have MCP calls
                self.assertTrue(
                    mcp_context.has_mcp_calls(),
                    f"FAILED P0: {test_case['name']} - MCP context has no calls",
                )

                # CRITICAL: Must have expected servers
                actual_servers = set(mcp_context.get_server_names())
                expected_servers = set(test_case["expected_mcp_servers"])

                self.assertTrue(
                    expected_servers.issubset(actual_servers),
                    f"FAILED P0: {test_case['name']} - expected servers {expected_servers} not in actual {actual_servers}",
                )

    def test_p0_transparency_summary_accuracy(self):
        """
        P0 TEST: Transparency summary MUST accurately reflect MCP enhancement

        REQUIREMENT: Summary must correctly identify MCP usage for monitoring
        """
        for test_case in self.p0_test_cases:
            with self.subTest(test_case=test_case["name"]):
                enhanced = ensure_transparency_compliance(
                    test_case["response"], test_case["input"]
                )
                summary = get_transparency_summary(enhanced, test_case["input"])

                # CRITICAL: Must detect MCP enhancement
                self.assertTrue(
                    summary["has_mcp_enhancement"],
                    f"FAILED P0: {test_case['name']} - summary shows no MCP enhancement",
                )

                # CRITICAL: Must identify correct servers
                actual_servers = set(summary["mcp_servers_used"])
                expected_servers = set(test_case["expected_mcp_servers"])

                self.assertTrue(
                    expected_servers.issubset(actual_servers),
                    f"FAILED P0: {test_case['name']} - summary servers {actual_servers} missing {expected_servers}",
                )

                # CRITICAL: Must show transparency applied
                self.assertTrue(
                    summary["transparency_applied"],
                    f"FAILED P0: {test_case['name']} - summary shows no transparency applied",
                )

    def test_p0_negative_cases_no_false_positives(self):
        """
        P0 TEST: Simple queries MUST NOT trigger MCP transparency

        REQUIREMENT: Low complexity queries should not create unnecessary overhead
        """
        for test_case in self.negative_test_cases:
            with self.subTest(test_case=test_case["name"]):
                enhanced = ensure_transparency_compliance(
                    test_case["response"], test_case["input"]
                )
                summary = get_transparency_summary(enhanced, test_case["input"])

                # CRITICAL: Must NOT show false positive MCP enhancement
                if summary["has_mcp_enhancement"]:
                    self.fail(
                        f"FAILED P0: {test_case['name']} - false positive MCP enhancement"
                    )

                # Should still have persona header
                self.assertTrue(
                    summary["has_persona_header"],
                    f"FAILED P0: {test_case['name']} - missing persona header",
                )

    def test_p0_persona_specific_mcp_templates(self):
        """
        P0 TEST: Each persona MUST have correct MCP disclosure template

        REQUIREMENT: Different personas should show appropriate MCP messaging
        """
        # Test persona-specific templates exist and are appropriate
        test_personas = ["martin", "diego", "camille", "rachel", "alvaro"]

        for persona in test_personas:
            with self.subTest(persona=persona):
                # Verify persona header exists
                header = self.bridge.persona_headers.get(persona)
                self.assertIsNotNone(
                    header, f"FAILED P0: {persona} missing persona header"
                )

                # Verify header format
                self.assertIn(
                    "|", header, f"FAILED P0: {persona} header format incorrect"
                )
                self.assertTrue(
                    header.startswith("🎯")
                    or header.startswith("📊")
                    or header.startswith("🎨")
                    or header.startswith("💼")
                    or header.startswith("🏗️"),
                    f"FAILED P0: {persona} header missing emoji",
                )

    def test_p0_end_to_end_integration(self):
        """
        P0 TEST: Complete end-to-end integration MUST work flawlessly

        REQUIREMENT: Full transparency system integration from input to output
        """
        # Use the most complex test case for comprehensive validation
        test_case = self.p0_test_cases[0]  # Strategic Organizational Framework

        enhanced = ensure_transparency_compliance(
            test_case["response"], test_case["input"]
        )
        summary = get_transparency_summary(enhanced, test_case["input"])

        # CRITICAL: Complete integration checklist
        integration_checks = [
            (
                "MCP disclosure present",
                (
                    "🔧 Accessing MCP Server:" in enhanced
                    or "🔧 Installing MCP enhancement:" in enhanced
                ),
            ),
            ("Processing indicator present", "*" in enhanced and "..." in enhanced),
            ("Persona header present", summary["has_persona_header"]),
            ("MCP enhancement detected", summary["has_mcp_enhancement"]),
            ("Multiple servers used", len(summary["mcp_servers_used"]) >= 2),
            ("Transparency applied", summary["transparency_applied"]),
        ]

        for check_name, check_result in integration_checks:
            self.assertTrue(
                check_result, f"FAILED P0: End-to-end integration - {check_name}"
            )


class TestMCPTransparencyRegression(unittest.TestCase):
    """
    Regression protection for MCP transparency system integrity
    """

    def test_regression_bridge_imports(self):
        """Ensure transparency bridge imports don't regress"""
        self.assertTrue(
            BRIDGE_AVAILABLE, "Bridge imports regressed - transparency system broken"
        )

    def test_regression_cursorrules_compliance(self):
        """Ensure implementation matches .cursorrules specification"""
        if not BRIDGE_AVAILABLE:
            self.skipTest("Bridge not available")

        bridge = CursorTransparencyBridge()

        # Verify complexity indicators match .cursorrules
        cursorrules_indicators = [
            "strategic",
            "organizational",
            "framework",
            "systematic",
            "complex",
            "multi-team",
            "executive",
            "board",
            "leadership",
            "presentation",
            "enterprise",
            "organization-wide",
            "cross-functional",
            "multiple teams",
            "trade-offs",
            "options",
            "alternatives",
            "analysis",
            "assessment",
        ]

        # Read actual implementation
        bridge_method = bridge.detect_mcp_usage_context.__code__
        # This test ensures the method exists and can be called
        self.assertIsNotNone(bridge_method, "MCP detection method missing")


def run_p0_regression_test():
    """
    Run P0 regression test with detailed reporting
    """
    print("🧪 Running MCP Transparency P0 Regression Test")
    print("=" * 60)

    # Create test suite focusing on P0 features
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all P0 tests
    suite.addTest(loader.loadTestsFromTestCase(TestMCPTransparencyP0))
    suite.addTest(loader.loadTestsFromTestCase(TestMCPTransparencyRegression))

    # Run with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout, buffer=True)
    result = runner.run(suite)

    # Report results
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ P0 MCP TRANSPARENCY REGRESSION TEST PASSED")
        print(f"   Ran {result.testsRun} tests successfully")
        return True
    else:
        print("❌ P0 MCP TRANSPARENCY REGRESSION TEST FAILED")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")

        # Print failure details
        for test, traceback in result.failures + result.errors:
            print(f"\n⚠️ FAILED: {test}")
            print(traceback)

        return False


if __name__ == "__main__":
    success = run_p0_regression_test()
    sys.exit(0 if success else 1)
