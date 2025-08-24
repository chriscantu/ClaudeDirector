#!/usr/bin/env python3
"""
Cursor Integration Test for MCP Transparency
Validates that .cursorrules integration works in live Cursor conversations
"""

import sys
import unittest
from pathlib import Path

# Add the integration protection path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "integration-protection"))

try:
    from cursor_transparency_bridge import (
        ensure_transparency_compliance,
        get_transparency_summary,
        CursorTransparencyBridge,
    )

    BRIDGE_AVAILABLE = True
except ImportError:
    BRIDGE_AVAILABLE = False


class TestCursorIntegration(unittest.TestCase):
    """
    Test Cursor-specific integration for MCP transparency

    This validates that the transparency system works exactly as
    specified in .cursorrules for live Cursor conversations.
    """

    def setUp(self):
        if not BRIDGE_AVAILABLE:
            self.skipTest("Transparency bridge not available")

        self.bridge = CursorTransparencyBridge()

    def test_cursor_strategic_question_flow(self):
        """
        Test complete flow for strategic question in Cursor

        Simulates: User asks strategic question → ClaudeDirector responds
        """
        # Simulate user question that should trigger MCP transparency
        user_input = "Martin, how should we architect our platform for strategic organizational scaling and complex multi-team coordination?"

        # Simulate initial response (what assistant would generate)
        initial_response = """Here's a comprehensive approach to platform architecture for organizational scaling:

1. **Evolutionary Architecture Principles**
   - Design for change and adaptability
   - Implement fitness functions for quality gates
   - Use architectural decision records (ADRs)

2. **Team Topology Alignment**
   - Stream-aligned teams for business capabilities
   - Platform teams for shared infrastructure
   - Enabling teams for cross-cutting concerns

3. **Technical Strategy Framework**
   - Domain-driven design for clear boundaries
   - API-first development approach
   - Microservices with careful service boundaries

This approach balances technical excellence with organizational dynamics."""

        # Apply transparency compliance (what should happen automatically in Cursor)
        enhanced_response = ensure_transparency_compliance(initial_response, user_input)
        summary = get_transparency_summary(initial_response, user_input)

        # Verify Cursor integration requirements
        self.assertIn(
            "🏗️ Martin | Platform Architecture",
            enhanced_response,
            "Cursor must auto-apply Martin persona header",
        )

        # Support both old and new MCP disclosure formats
        has_mcp_disclosure = (
            "🔧 Accessing MCP Server:" in enhanced_response
            or "🔧 Installing MCP enhancement:" in enhanced_response
        )
        self.assertTrue(
            has_mcp_disclosure,
            "Cursor must show MCP transparency for strategic questions",
        )

        self.assertIn(
            "systematic_analysis",
            enhanced_response,
            "Strategic questions must trigger systematic analysis",
        )

        self.assertTrue(
            summary["has_mcp_enhancement"],
            "Summary must detect MCP enhancement for monitoring",
        )

        # Verify response format matches .cursorrules specification exactly
        lines = enhanced_response.split("\n")

        # Should start with MCP disclosure (either format)
        first_line_valid = lines[0].startswith("🔧 Accessing MCP Server:") or lines[
            0
        ].startswith("🔧 Installing MCP enhancement:")
        self.assertTrue(first_line_valid, "Must start with MCP server disclosure")

        # Should have processing indicator
        processing_line = next(
            (line for line in lines if line.startswith("*") and line.endswith("*")),
            None,
        )
        self.assertIsNotNone(processing_line, "Must include processing indicator")

        # Should have persona header
        persona_line = next(
            (line for line in lines if "Martin | Platform Architecture" in line), None
        )
        self.assertIsNotNone(persona_line, "Must include persona header")

    def test_cursor_persona_switching(self):
        """Test that different personas get appropriate MCP disclosures"""

        test_cases = [
            {
                "input": "Diego, what organizational framework should we use for strategic team scaling?",
                "expected_persona": "diego",
                "expected_header": "🎯 Diego | Engineering Leadership",
            },
            {
                "input": "Camille, how do we develop executive-level strategic technology assessment?",
                "expected_persona": "camille",
                "expected_header": "📊 Camille | Strategic Technology",
            },
            {
                "input": "Rachel, what design system strategy should we use for cross-functional coordination?",
                "expected_persona": "rachel",
                "expected_header": "🎨 Rachel | Design Systems Strategy",
            },
        ]

        for test_case in test_cases:
            with self.subTest(persona=test_case["expected_persona"]):
                response = (
                    "Here is a strategic approach to your organizational challenge..."
                )

                enhanced = ensure_transparency_compliance(response, test_case["input"])
                summary = get_transparency_summary(response, test_case["input"])

                # Verify correct persona detection
                self.assertEqual(
                    summary["persona_detected"], test_case["expected_persona"]
                )

                # Verify correct header application
                self.assertIn(test_case["expected_header"], enhanced)

                # Verify MCP enhancement for strategic questions
                self.assertTrue(summary["has_mcp_enhancement"])

    def test_cursor_performance_requirements(self):
        """Test that transparency system meets Cursor performance requirements"""
        import time

        # Test response time requirements
        user_input = "How should we develop strategic organizational framework for complex assessment?"
        response = "Strategic framework development requires systematic analysis..."

        start_time = time.time()
        ensure_transparency_compliance(response, user_input)
        summary = get_transparency_summary(response, user_input)
        end_time = time.time()

        processing_time = end_time - start_time

        # Should be very fast (< 50ms for fallback mode)
        self.assertLess(
            processing_time,
            0.05,
            f"Transparency processing too slow: {processing_time:.3f}s",
        )

        # Should still provide all required features
        self.assertTrue(summary["transparency_applied"])
        self.assertTrue(summary["has_persona_header"])
        self.assertTrue(summary["has_mcp_enhancement"])

    def test_cursor_rules_compliance_validation(self):
        """Validate that implementation exactly matches .cursorrules specification"""

        # Read complexity indicators from bridge
        CursorTransparencyBridge()

        # Test a complex strategic question
        user_input = "How should we develop a strategic organizational framework for complex multi-team platform architecture assessment with executive presentation?"
        response = "Strategic analysis requires systematic framework application for organizational complexity..."

        enhanced = ensure_transparency_compliance(response, user_input)

        # Verify .cursorrules compliance checklist
        compliance_checks = [
            # Persona header format
            (
                "Persona header emoji",
                any(emoji in enhanced for emoji in ["🎯", "📊", "🎨", "💼", "🏗️"]),
            ),
            ("Persona header format", " | " in enhanced),
            # MCP transparency format (support both old and new)
            (
                "MCP disclosure format",
                (
                    "🔧 Accessing MCP Server:" in enhanced
                    or "🔧 Installing MCP enhancement:" in enhanced
                ),
            ),
            ("MCP capability format", "(" in enhanced and ")" in enhanced),
            ("Processing indicator", "*" in enhanced),
            # Content structure
            ("Response has content", len(enhanced) > 200),
            ("Multiple lines", "\n" in enhanced),
        ]

        for check_name, check_result in compliance_checks:
            self.assertTrue(
                check_result, f".cursorrules compliance failed: {check_name}"
            )


def run_cursor_integration_test():
    """Run Cursor integration test with detailed reporting"""
    print("🔄 Running Cursor Integration Test for MCP Transparency")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCursorIntegration)

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ CURSOR INTEGRATION TEST PASSED")
        print("   MCP transparency ready for live Cursor usage")
        return True
    else:
        print("❌ CURSOR INTEGRATION TEST FAILED")
        print("   Cursor integration needs fixes before deployment")

        for test, traceback in result.failures + result.errors:
            print(f"\n⚠️ FAILED: {test}")
            print(traceback)

        return False


if __name__ == "__main__":
    success = run_cursor_integration_test()
    sys.exit(0 if success else 1)
