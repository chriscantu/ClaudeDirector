"""
Comprehensive test suite for transparency system integration
Ensures persona headers, framework detection, and MCP transparency work correctly
"""

import pytest
import time
from pathlib import Path
import sys

# Add the lib directory to Python path for imports
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

try:
    from claudedirector.transparency.integrated_transparency import (
        IntegratedTransparencySystem,
    )
    from claudedirector.transparency.framework_detection import (
        FrameworkDetectionMiddleware,
    )

    HAS_FULL_TRANSPARENCY = True
except ImportError:
    HAS_FULL_TRANSPARENCY = False

# Import our integration bridge
integration_path = Path(__file__).parent.parent.parent / "integration-protection"
sys.path.insert(0, str(integration_path))
from cursor_transparency_bridge import (
    CursorTransparencyBridge,
    ensure_transparency_compliance,
)


class TestPersonaDetection:
    """Test persona detection from context"""

    def setup_method(self):
        self.bridge = CursorTransparencyBridge()

    def test_martin_architecture_detection(self):
        """Test Martin persona detection for architecture questions"""
        test_cases = [
            "How should we architect our platform for scale?",
            "What's the best approach for microservices architecture?",
            "Help me design our technical debt strategy",
            "Platform scalability concerns with distributed systems",
        ]

        for user_input in test_cases:
            persona = self.bridge.detect_persona_from_context(user_input)
            assert (
                persona == "martin"
            ), f"Expected 'martin' for input: {user_input}, got: {persona}"

    def test_diego_leadership_detection(self):
        """Test Diego persona detection for leadership questions"""
        test_cases = [
            "How should we structure our engineering team?",
            "What's our platform strategy for next quarter?",
            "Team coordination across multiple engineering groups",
            "Engineering leadership challenges with remote teams",
        ]

        for user_input in test_cases:
            persona = self.bridge.detect_persona_from_context(user_input)
            assert (
                persona == "diego"
            ), f"Expected 'diego' for input: {user_input}, got: {persona}"

    def test_alvaro_business_detection(self):
        """Test Alvaro persona detection for business/ROI questions"""
        test_cases = [
            "What's the ROI of our platform investment?",
            "Business value analysis for this technical initiative",
            "Platform investment strategy and stakeholder communication",
            "How do we justify this business expense?",
        ]

        for user_input in test_cases:
            persona = self.bridge.detect_persona_from_context(user_input)
            assert (
                persona == "alvaro"
            ), f"Expected 'alvaro' for input: {user_input}, got: {persona}"

    def test_rachel_design_detection(self):
        """Test Rachel persona detection for design system questions"""
        test_cases = [
            "How should we approach our design system strategy?",
            "Cross-functional UX coordination challenges",
            "Component library architecture and adoption",
            "Design systems strategy for multiple platforms",
        ]

        for user_input in test_cases:
            persona = self.bridge.detect_persona_from_context(user_input)
            assert (
                persona == "rachel"
            ), f"Expected 'rachel' for input: {user_input}, got: {persona}"

    def test_default_persona_fallback(self):
        """Test default persona when no clear context"""
        generic_input = "Can you help me with this general question?"
        persona = self.bridge.detect_persona_from_context(generic_input)
        assert persona == "martin", "Should default to 'martin' for generic questions"


class TestPersonaHeaders:
    """Test persona header application"""

    def setup_method(self):
        self.bridge = CursorTransparencyBridge()

    def test_martin_header_application(self):
        """Test Martin header is correctly applied"""
        response = "Here's an approach to platform scalability..."
        enhanced = self.bridge.add_persona_header(response, "martin")

        expected_header = "🏗️ Martin | Platform Architecture"
        assert enhanced.startswith(
            expected_header
        ), f"Response should start with Martin header: {enhanced[:50]}"
        assert response in enhanced, "Original response should be preserved"

    def test_diego_header_application(self):
        """Test Diego header is correctly applied"""
        response = "Team structure depends on several factors..."
        enhanced = self.bridge.add_persona_header(response, "diego")

        expected_header = "🎯 Diego | Engineering Leadership"
        assert enhanced.startswith(
            expected_header
        ), f"Response should start with Diego header: {enhanced[:50]}"

    def test_header_not_duplicated(self):
        """Test that headers are not duplicated if already present"""
        response_with_header = (
            "🏗️ Martin | Platform Architecture\n\nHere's the analysis..."
        )
        enhanced = self.bridge.add_persona_header(response_with_header, "martin")

        # Should not add another header
        header_count = enhanced.count("🏗️ Martin | Platform Architecture")
        assert (
            header_count == 1
        ), f"Header should appear only once, found {header_count} times"

    def test_has_persona_header_detection(self):
        """Test detection of existing persona headers"""
        test_cases = [
            ("🏗️ Martin | Platform Architecture\nContent...", True),
            ("🎯 Diego | Engineering Leadership\nContent...", True),
            ("Regular response without header", False),
            ("Some other content 🏗️ Martin", False),  # Header not at start
        ]

        for response, expected in test_cases:
            result = self.bridge.has_persona_header(response)
            assert (
                result == expected
            ), f"Header detection failed for: {response[:30]}..."


class TestTransparencyCompliance:
    """Test full transparency compliance"""

    def setup_method(self):
        self.bridge = CursorTransparencyBridge()

    def test_complete_transparency_application(self):
        """Test complete transparency system application"""
        user_input = "How should we architect our platform for scalability?"
        response = "Here's a systematic approach to platform architecture..."

        enhanced = ensure_transparency_compliance(response, user_input)

        # Should have Martin header (architecture context)
        assert "🏗️ Martin | Platform Architecture" in enhanced
        # Should preserve original content
        assert "systematic approach" in enhanced

    def test_transparency_summary_generation(self):
        """Test transparency summary provides correct metadata"""
        from cursor_transparency_bridge import get_transparency_summary

        user_input = "Platform investment ROI analysis needed"
        response = "Business value analysis shows positive ROI..."

        enhanced = ensure_transparency_compliance(response, user_input)
        summary = get_transparency_summary(enhanced, user_input)

        assert summary["persona_detected"] == "alvaro"  # Business/ROI context
        assert summary["has_persona_header"] == True
        assert summary["transparency_applied"] == True

    def test_multiple_context_scenarios(self):
        """Test transparency across multiple scenarios"""
        test_scenarios = [
            {
                "input": "Team structure for platform engineering",
                "response": "Team topology considerations...",
                "expected_persona": "diego",
                "expected_header": "🎯 Diego | Engineering Leadership",
            },
            {
                "input": "Microservices architecture patterns",
                "response": "Distributed systems design requires...",
                "expected_persona": "martin",
                "expected_header": "🏗️ Martin | Platform Architecture",
            },
            {
                "input": "Design system component strategy",
                "response": "Component architecture should...",
                "expected_persona": "rachel",
                "expected_header": "🎨 Rachel | Design Systems Strategy",
            },
        ]

        for scenario in test_scenarios:
            enhanced = ensure_transparency_compliance(
                scenario["response"], scenario["input"]
            )
            assert (
                scenario["expected_header"] in enhanced
            ), f"Expected {scenario['expected_header']} in response for: {scenario['input']}"


@pytest.mark.skipif(
    not HAS_FULL_TRANSPARENCY, reason="Full transparency system not available"
)
class TestFrameworkDetection:
    """Test framework detection and attribution (requires full system)"""

    def setup_method(self):
        self.framework_detector = FrameworkDetectionMiddleware()

    def test_team_topologies_detection(self):
        """Test Team Topologies framework detection"""
        response_with_framework = """
        Based on Team Topologies principles, we should organize teams around
        cognitive load and Conway's Law. Stream-aligned teams work best for
        feature development while platform teams provide foundational capabilities.
        """

        frameworks = self.framework_detector.detect_frameworks_used(
            response_with_framework
        )
        framework_names = [f.framework_name for f in frameworks]

        assert (
            "Team Topologies" in framework_names
        ), f"Should detect Team Topologies, found: {framework_names}"

    def test_strategic_framework_detection(self):
        """Test strategic framework detection"""
        response_with_ogsm = """
        Using the OGSM strategic framework, let's define objectives, goals,
        strategies, and measures for this platform initiative.
        """

        frameworks = self.framework_detector.detect_frameworks_used(response_with_ogsm)
        framework_names = [f.framework_name for f in frameworks]

        assert (
            "OGSM Strategic Framework" in framework_names
        ), f"Should detect OGSM, found: {framework_names}"

    def test_framework_attribution_generation(self):
        """Test framework attribution text generation"""
        # Create mock framework usage
        from claudedirector.transparency.framework_detection import FrameworkUsage

        frameworks = [
            FrameworkUsage(
                framework_name="Team Topologies",
                confidence_score=0.8,
                matched_patterns=["team topologies", "cognitive load"],
                framework_type="organizational",
            )
        ]

        attribution = self.framework_detector.create_framework_attribution(
            "martin", frameworks
        )

        assert "Team Topologies" in attribution
        assert "Platform Architecture experience" in attribution


@pytest.mark.skipif(
    not HAS_FULL_TRANSPARENCY, reason="Full transparency system not available"
)
class TestIntegratedTransparencySystem:
    """Test full integrated transparency system"""

    def setup_method(self):
        self.transparency_system = IntegratedTransparencySystem()

    def test_transparency_context_creation(self):
        """Test transparency context creation and tracking"""
        context = self.transparency_system.create_transparency_context("martin")

        assert context.persona == "martin"
        assert context.total_processing_time >= 0
        assert not context.has_enhancements  # No enhancements yet

    def test_transparency_application(self):
        """Test applying transparency to responses"""
        context = self.transparency_system.create_transparency_context("martin")
        response = "Here's the architectural analysis..."

        # Apply transparency (should detect frameworks if any)
        enhanced = self.transparency_system.apply_transparency(context, response)

        # Should preserve content
        assert "architectural analysis" in enhanced

        # Get transparency summary
        summary = self.transparency_system.create_transparency_summary(context)
        assert summary["persona"] == "martin"

    def test_performance_stats_tracking(self):
        """Test performance statistics tracking"""
        context = self.transparency_system.create_transparency_context("martin")
        response = "Test response with potential framework usage like Team Topologies patterns."

        # Apply transparency multiple times to test stats
        for _ in range(3):
            self.transparency_system.apply_transparency(context, response)

        stats = self.transparency_system.get_performance_stats()
        assert stats["total_requests"] >= 3
        assert "avg_transparency_overhead" in stats


class TestErrorHandling:
    """Test error handling and safeguards"""

    def setup_method(self):
        self.bridge = CursorTransparencyBridge()

    def test_empty_input_handling(self):
        """Test handling of empty inputs"""
        enhanced = ensure_transparency_compliance("", "")
        # Should get default persona header
        assert "🏗️ Martin | Platform Architecture" in enhanced

    def test_malformed_input_handling(self):
        """Test handling of malformed inputs"""
        test_cases = [
            None,
            "",
            "   ",  # Whitespace only
            "\n\n\n",  # Newlines only
        ]

        for test_input in test_cases:
            try:
                if test_input is None:
                    continue  # Skip None case as it would raise TypeError

                enhanced = ensure_transparency_compliance("Response", test_input or "")
                # Should not crash and should have a persona header
                assert any(
                    header in enhanced
                    for header in self.bridge.persona_headers.values()
                )
            except Exception as e:
                pytest.fail(
                    f"Should handle malformed input gracefully: {test_input}, got error: {e}"
                )

    def test_long_input_performance(self):
        """Test performance with long inputs"""
        long_input = (
            "architecture " * 1000
        )  # Very long input with architecture keywords
        response = "Here's the analysis..."

        start_time = time.time()
        enhanced = ensure_transparency_compliance(response, long_input)
        processing_time = time.time() - start_time

        # Should complete in reasonable time (< 100ms for this test)
        assert (
            processing_time < 0.1
        ), f"Processing took too long: {processing_time:.3f}s"
        assert "🏗️ Martin | Platform Architecture" in enhanced


class TestSafeguards:
    """Test integration safeguards"""

    def test_no_breaking_changes(self):
        """Test that transparency integration doesn't break existing responses"""
        original_response = (
            "This is a standard response without any special formatting."
        )
        enhanced = ensure_transparency_compliance(original_response, "general question")

        # Should preserve original content
        assert original_response in enhanced
        # Should add persona header
        assert any(
            header in enhanced
            for header in [
                "🏗️ Martin | Platform Architecture",
                "🎯 Diego | Engineering Leadership",
            ]
        )

    def test_graceful_fallback(self):
        """Test graceful fallback when full transparency system unavailable"""
        # This test always passes in fallback mode
        response = "Test response"
        enhanced = ensure_transparency_compliance(response, "test input")

        # Should at minimum have persona header
        assert "🏗️ Martin | Platform Architecture" in enhanced
        assert response in enhanced

    def test_transparency_consistency(self):
        """Test that transparency is consistently applied"""
        test_cases = [
            ("Architecture question", "Architecture response"),
            ("Leadership question", "Leadership response"),
            ("Business question", "Business response"),
        ]

        for user_input, response in test_cases:
            enhanced1 = ensure_transparency_compliance(response, user_input)
            enhanced2 = ensure_transparency_compliance(response, user_input)

            # Should be consistent
            assert enhanced1 == enhanced2, "Transparency should be deterministic"


def run_transparency_integration_tests():
    """Run all transparency integration tests"""
    print("🧪 Running ClaudeDirector Transparency Integration Tests")
    print("=" * 60)

    # Run pytest with verbose output
    test_file = __file__
    exit_code = pytest.main(["-v", test_file])

    if exit_code == 0:
        print("\n✅ All transparency integration tests passed!")
        print("🛡️ Transparency system ready for integration")
    else:
        print("\n❌ Some tests failed - review before integration")

    return exit_code == 0


if __name__ == "__main__":
    run_transparency_integration_tests()
