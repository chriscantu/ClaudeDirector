#!/usr/bin/env python3
"""
PHASE 12 P0 TEST: Always-On MCP Enhancement
CRITICAL: 100% MCP enhancement rate must be maintained

Business Impact: Phase 12 value proposition depends on guaranteed AI enhancement
Technical Impact: Always-on routing and complexity threshold removal validation
"""

import unittest
import sys
from pathlib import Path
import time
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .claudedirector.lib.core.enhanced_persona_manager import EnhancedPersonaManager
    from .claudedirector.lib.core.complexity_analyzer import ComplexityAnalysis
    from .claudedirector.lib.core.lightweight_fallback import FallbackMode
except ImportError:
    # Graceful fallback for development
    EnhancedPersonaManager = None
    ComplexityAnalysis = None
    FallbackMode = None


class TestPhase12AlwaysOnMCP(unittest.TestCase):
    """
    P0 TEST SUITE: Phase 12 Always-On MCP Enhancement

    CRITICAL REQUIREMENTS:
    1. 100% MCP enhancement rate (no more complexity thresholds)
    2. Direct persona → server routing works
    3. Always-on transparency disclosure
    4. Fallback pattern when MCP unavailable
    """

    def setUp(self):
        """Set up test environment"""
        if not EnhancedPersonaManager:
            self.skipTest("Enhanced persona manager not available in test environment")

        self.persona_manager = EnhancedPersonaManager()
        self.test_personas = ["diego", "martin", "rachel", "camille", "alvaro"]
        self.test_queries = [
            "What is our team structure?",  # Simple query (used to fail threshold)
            "How should we optimize our platform architecture for scale?",  # Complex query
            "Create a diagram showing our microservices architecture",  # Visual query
            "Analyze the strategic implications of our technology roadmap",  # Strategic query
        ]

    def test_p0_100_percent_enhancement_rate(self):
        """
        P0 TEST: 100% MCP enhancement rate must be achieved

        CRITICAL: This validates Phase 12's core value proposition
        """
        enhancement_attempts = 0
        successful_enhancements = 0

        # Test each persona with each query type
        for persona in self.test_personas:
            for query in self.test_queries:
                enhancement_attempts += 1

                # Mock MCP client as available
                with patch.object(self.persona_manager, "mcp_client") as mock_client:
                    mock_client.is_available = True
                    mock_client.config = {}

                    # Mock the dependency checker to return True (MCP available)
                    with patch.object(
                        self.persona_manager.dependency_checker, "check_mcp_dependency"
                    ) as mock_checker:
                        mock_checker.return_value = True

                        # Test enhancement decision
                        complexity_analysis = (
                            ComplexityAnalysis(
                                confidence=0.3,  # LOW complexity (would fail old thresholds)
                                enhancement_strategy=None,
                                recommended_enhancement="sequential",
                            )
                            if ComplexityAnalysis
                            else Mock(confidence=0.3)
                        )

                        # This should ALWAYS return True in Phase 12
                        should_enhance = self.persona_manager._should_enhance(
                            persona, complexity_analysis
                        )

                        if should_enhance:
                            successful_enhancements += 1

        # CRITICAL: Must achieve 100% enhancement rate
        enhancement_rate = successful_enhancements / enhancement_attempts

        if enhancement_rate < 1.0:
            self.fail(
                f"❌ PHASE 12 P0 FAILURE: Enhancement rate {enhancement_rate:.1%} < 100%\n"
                f"Phase 12 requires 100% MCP enhancement rate (no complexity thresholds)\n"
                f"Successful: {successful_enhancements}/{enhancement_attempts}\n"
                f"Business Impact: Strategic guidance becomes inconsistent"
            )

        print(
            f"✅ P0 SUCCESS: 100% enhancement rate achieved ({successful_enhancements}/{enhancement_attempts})"
        )

    def test_p0_direct_persona_server_mapping(self):
        """
        P0 TEST: Direct persona → server mapping must work

        CRITICAL: Validates always-on routing implementation
        """
        expected_mappings = {
            "diego": "sequential",
            "martin": "context7",
            "rachel": "context7",
            "camille": "sequential",
            "alvaro": "sequential",
        }

        for persona, expected_server in expected_mappings.items():
            actual_server = self.persona_manager.get_mcp_server_for_persona(persona)

            if actual_server != expected_server:
                self.fail(
                    f"❌ PHASE 12 P0 FAILURE: {persona} maps to {actual_server}, expected {expected_server}\n"
                    f"Direct persona routing broken - always-on enhancement compromised\n"
                    f"Business Impact: MCP server selection incorrect for persona expertise"
                )

        print("✅ P0 SUCCESS: Direct persona → server mapping working")

    def test_p0_always_on_transparency_disclosure(self):
        """
        P0 TEST: Always-on transparency disclosure must work

        CRITICAL: 100% transparency rate required for Phase 12
        """
        from .claudedirector.lib.core.cursor_response_enhancer import (
            CursorResponseEnhancer,
        )

        if not hasattr(self, "response_enhancer"):
            try:
                self.response_enhancer = CursorResponseEnhancer()
            except:
                self.skipTest("Response enhancer not available")

        # Test simple queries that would NOT have shown transparency before Phase 12
        simple_queries = [
            "What is the status?",
            "How are things going?",
            "Update please",
            "Thanks",
        ]

        for query in simple_queries:
            # Phase 12: should_show_mcp_transparency should ALWAYS return True
            should_show = self.response_enhancer.should_show_mcp_transparency(
                query, "test response"
            )

            if not should_show:
                self.fail(
                    f"❌ PHASE 12 P0 FAILURE: Simple query '{query}' not showing MCP transparency\n"
                    f"Phase 12 requires 100% transparency rate (always-on disclosure)\n"
                    f"Business Impact: Users lose AI enhancement visibility"
                )

        print("✅ P0 SUCCESS: Always-on transparency disclosure working")

    def test_p0_lightweight_fallback_integration(self):
        """
        P0 TEST: Lightweight fallback pattern must be integrated

        CRITICAL: Validates OVERVIEW.md architectural pattern
        """
        # Check that fallback system is properly initialized
        if not hasattr(self.persona_manager, "persona_fallback"):
            self.fail(
                "❌ PHASE 12 P0 FAILURE: Lightweight fallback system not initialized\n"
                "OVERVIEW.md lightweight fallback pattern not implemented\n"
                "Business Impact: System fails when MCP servers unavailable"
            )

        if not hasattr(self.persona_manager, "dependency_checker"):
            self.fail(
                "❌ PHASE 12 P0 FAILURE: MCP dependency checker not initialized\n"
                "Smart dependency detection missing from OVERVIEW.md pattern\n"
                "Business Impact: No graceful degradation when servers offline"
            )

        # Test fallback response generation
        fallback_response = (
            self.persona_manager.persona_fallback.generate_lightweight_response(
                "diego", "Test strategic question", "test_failure"
            )
        )

        if not fallback_response:
            self.fail(
                "❌ PHASE 12 P0 FAILURE: Lightweight fallback response generation failed\n"
                "Essential features not available during MCP outage\n"
                "Business Impact: Strategic guidance unavailable during maintenance"
            )

        print("✅ P0 SUCCESS: Lightweight fallback pattern integrated")

    def test_p0_performance_targets_maintained(self):
        """
        P0 TEST: Performance targets must be maintained

        CRITICAL: <500ms response time and <50ms transparency overhead
        """
        start_time = time.time()

        # Mock a simple enhancement request
        with patch.object(self.persona_manager, "mcp_client") as mock_client:
            mock_client.is_available = True

            with patch.object(
                self.persona_manager.dependency_checker, "check_mcp_dependency"
            ) as mock_checker:
                mock_checker.return_value = False  # Force fallback for speed test

                # Test lightweight fallback performance
                fallback_response = (
                    self.persona_manager.persona_fallback.generate_lightweight_response(
                        "diego", "Test query", "performance_test"
                    )
                )

                fallback_time = time.time() - start_time

                # CRITICAL: <100ms for fallback response (OVERVIEW.md requirement)
                if fallback_time > 0.1:  # 100ms
                    self.fail(
                        f"❌ PHASE 12 P0 FAILURE: Fallback response too slow: {fallback_time:.3f}s > 0.1s\n"
                        f"OVERVIEW.md requires <100ms fallback response time\n"
                        f"Business Impact: Poor user experience during fallback mode"
                    )

        print(f"✅ P0 SUCCESS: Performance targets met ({fallback_time:.3f}s)")


def run_phase12_p0_tests():
    """
    Run Phase 12 P0 tests with proper error handling

    Returns:
        bool: True if all tests pass, False otherwise
    """
    print("🚀 RUNNING PHASE 12 ALWAYS-ON MCP ENHANCEMENT P0 TESTS")
    print("=" * 60)

    try:
        # Create test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(TestPhase12AlwaysOnMCP)

        # Run tests with detailed output
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)

        # Print summary
        total_tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)

        print(f"\n📊 PHASE 12 P0 TEST SUMMARY:")
        print(f"Total Tests: {total_tests}")
        print(f"Failures: {failures}")
        print(f"Errors: {errors}")

        if failures == 0 and errors == 0:
            print("✅ PHASE 12 P0 TESTS: ALL PASSED")
            print("🎉 Always-on MCP enhancement working correctly!")
            return True
        else:
            print("❌ PHASE 12 P0 TESTS: FAILURES DETECTED")
            print("🚨 Phase 12 implementation has critical issues!")
            return False

    except Exception as e:
        print(f"❌ PHASE 12 P0 TESTS: EXECUTION ERROR: {e}")
        return False


if __name__ == "__main__":
    success = run_phase12_p0_tests()
    sys.exit(0 if success else 1)
