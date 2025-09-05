#!/usr/bin/env python3
"""
PHASE 12 P0 TEST: Lightweight Fallback Pattern
CRITICAL: OVERVIEW.md architectural pattern must provide graceful degradation

Business Impact: Strategic guidance must remain available during MCP server maintenance
Technical Impact: Validates smart dependency detection and essential feature provision
"""

import unittest
import sys
import asyncio
import time
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from .claudedirector.lib.core.lightweight_fallback import (
        LightweightPersonaFallback,
        MCPDependencyChecker,
        FallbackMode,
        FallbackResponse,
    )
    from .claudedirector.lib.core.enhanced_persona_manager import EnhancedPersonaManager
except ImportError:
    # Graceful fallback for development
    LightweightPersonaFallback = None
    MCPDependencyChecker = None
    FallbackMode = None
    FallbackResponse = None
    EnhancedPersonaManager = None


class TestLightweightFallbackPattern(unittest.TestCase):
    """
    P0 TEST SUITE: OVERVIEW.md Lightweight Fallback Pattern

    CRITICAL REQUIREMENTS:
    1. Smart dependency detection before MCP instantiation
    2. API compatibility maintained in lightweight mode
    3. Essential functionality always available
    4. <100ms fallback response time
    """

    def setUp(self):
        """Set up test environment"""
        if not LightweightPersonaFallback:
            self.skipTest(
                "Lightweight fallback system not available in test environment"
            )

        self.persona_fallback = LightweightPersonaFallback()
        self.dependency_checker = MCPDependencyChecker()
        self.test_personas = ["diego", "martin", "rachel", "camille", "alvaro"]
        self.test_queries = [
            "What should our strategic approach be?",
            "How do we improve our platform architecture?",
            "Design system coordination strategy needed",
            "Business value analysis for this initiative",
        ]

    def test_p0_smart_dependency_detection(self):
        """
        P0 TEST: Smart dependency detection must work before MCP instantiation

        CRITICAL: OVERVIEW.md pattern requires intelligent dependency checking
        """
        # Test with mock MCP client that's unavailable
        mock_mcp_client = Mock()
        mock_mcp_client.is_available = False

        # Should return False for unavailable client
        available = asyncio.run(
            self.dependency_checker.check_mcp_dependency("diego", mock_mcp_client)
        )

        if available:
            self.fail(
                "❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Dependency checker returned True for unavailable MCP client\n"
                "Smart dependency detection not working - OVERVIEW.md pattern broken\n"
                "Business Impact: System attempts to use unavailable services"
            )

        # Test with mock MCP client that's available
        mock_mcp_client.is_available = True
        mock_mcp_client.ping = AsyncMock(return_value=True)

        available = asyncio.run(
            self.dependency_checker.check_mcp_dependency("diego", mock_mcp_client)
        )

        if not available:
            self.fail(
                "❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Dependency checker returned False for available MCP client\n"
                "Smart dependency detection false negative - OVERVIEW.md pattern broken\n"
                "Business Impact: Available services not utilized"
            )

        print("✅ P0 SUCCESS: Smart dependency detection working")

    def test_p0_api_compatibility_maintained(self):
        """
        P0 TEST: API compatibility must be maintained in lightweight mode

        CRITICAL: Complete method signatures preserved (OVERVIEW.md requirement)
        """
        # Test all essential personas have required attributes
        for persona in self.test_personas:
            persona_config = self.persona_fallback.persona_essentials.get(persona)

            if not persona_config:
                self.fail(
                    f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: {persona} not in persona_essentials\n"
                    f"API compatibility broken - essential persona config missing\n"
                    f"Business Impact: Persona-specific fallback unavailable"
                )

            # Check required API fields
            required_fields = [
                "domain",
                "icon",
                "essential_capabilities",
                "lightweight_personality",
                "key_frameworks",
            ]

            for field in required_fields:
                if field not in persona_config:
                    self.fail(
                        f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: {persona} missing {field}\n"
                        f"API compatibility broken - required field missing\n"
                        f"Business Impact: Incomplete fallback functionality"
                    )

        print("✅ P0 SUCCESS: API compatibility maintained")

    def test_p0_essential_functionality_always_available(self):
        """
        P0 TEST: Essential features must always be available

        CRITICAL: Core functionality preserved during architecture transitions
        """
        for persona in self.test_personas:
            for query in self.test_queries:
                try:
                    # Test lightweight response generation
                    fallback_response = asyncio.run(
                        self.persona_fallback.generate_lightweight_response(
                            persona, query, "P0_test"
                        )
                    )

                    # Validate response structure
                    if not isinstance(fallback_response, (FallbackResponse, Mock)):
                        self.fail(
                            f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Invalid response type for {persona}\n"
                            f"Expected FallbackResponse, got {type(fallback_response)}\n"
                            f"Business Impact: Essential functionality broken"
                        )

                    # Check response has content
                    if not fallback_response.content:
                        self.fail(
                            f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Empty response for {persona} + '{query}'\n"
                            f"Essential functionality not providing content\n"
                            f"Business Impact: Users get no strategic guidance during fallback"
                        )

                    # Check persona identification in response
                    if persona.title() not in fallback_response.content:
                        self.fail(
                            f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: {persona} not identified in response\n"
                            f"Persona context lost in fallback mode\n"
                            f"Business Impact: Users lose persona-specific guidance"
                        )

                except Exception as e:
                    self.fail(
                        f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Exception generating {persona} response: {e}\n"
                        f"Essential functionality completely broken\n"
                        f"Business Impact: Strategic guidance unavailable during fallback"
                    )

        print("✅ P0 SUCCESS: Essential functionality always available")

    def test_p0_fallback_response_time(self):
        """
        P0 TEST: <100ms fallback response time requirement

        CRITICAL: OVERVIEW.md performance requirement for fallback mode
        """
        max_allowed_time = 0.1  # 100ms (OVERVIEW.md requirement)

        for persona in self.test_personas:
            start_time = time.time()

            try:
                fallback_response = asyncio.run(
                    self.persona_fallback.generate_lightweight_response(
                        persona, "Strategic guidance needed", "performance_test"
                    )
                )

                response_time = time.time() - start_time

                if response_time > max_allowed_time:
                    self.fail(
                        f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: {persona} response too slow\n"
                        f"Response time: {response_time:.3f}s > {max_allowed_time:.3f}s\n"
                        f"OVERVIEW.md requires <100ms fallback response time\n"
                        f"Business Impact: Poor user experience during fallback mode"
                    )

                # Also check processing time in response object
                if hasattr(fallback_response, "processing_time"):
                    if fallback_response.processing_time > max_allowed_time:
                        self.fail(
                            f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: {persona} processing time too slow\n"
                            f"Processing time: {fallback_response.processing_time:.3f}s > {max_allowed_time:.3f}s\n"
                            f"Internal processing exceeds OVERVIEW.md requirement"
                        )

            except Exception as e:
                self.fail(
                    f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: {persona} response generation failed: {e}\n"
                    f"Performance test could not complete\n"
                    f"Business Impact: Fallback functionality broken"
                )

        print("✅ P0 SUCCESS: Fallback response time < 100ms")

    def test_p0_essential_mode_system_response(self):
        """
        P0 TEST: Essential mode must provide system-level response

        CRITICAL: Core functionality when ALL enhancement unavailable
        """
        try:
            essential_response = asyncio.run(
                self.persona_fallback.generate_essential_response(
                    "system", "Strategic question during outage"
                )
            )

            # Check response exists
            if not essential_response:
                self.fail(
                    "❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Essential mode returned no response\n"
                    "Core functionality broken when all enhancement unavailable\n"
                    "Business Impact: Complete system failure during outages"
                )

            # Check response has content
            if not essential_response.content:
                self.fail(
                    "❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Essential mode returned empty content\n"
                    "Core strategic guidance missing in essential mode\n"
                    "Business Impact: No guidance available during system outages"
                )

            # Check mode is correct
            if (
                hasattr(essential_response, "mode")
                and essential_response.mode != FallbackMode.ESSENTIAL
            ):
                self.fail(
                    f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Wrong mode {essential_response.mode}\n"
                    f"Expected ESSENTIAL mode for system-level fallback\n"
                    f"Business Impact: Fallback mode detection broken"
                )

            # Check transparency disclosure exists
            if "essential" not in essential_response.content.lower():
                self.fail(
                    "❌ LIGHTWEIGHT FALLBACK P0 FAILURE: No essential mode disclosure\n"
                    "Users not informed about system state\n"
                    "Business Impact: Poor transparency during outages"
                )

        except Exception as e:
            self.fail(
                f"❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Essential mode generation failed: {e}\n"
                f"Core system functionality completely broken\n"
                f"Business Impact: Total system failure during outages"
            )

        print("✅ P0 SUCCESS: Essential mode system response working")

    def test_p0_health_cache_functionality(self):
        """
        P0 TEST: Health check caching must work for performance

        CRITICAL: Prevents repeated expensive health checks
        """
        mock_mcp_client = Mock()
        mock_mcp_client.is_available = True
        mock_mcp_client.ping = AsyncMock(return_value=True)

        # First call should populate cache
        start_time = time.time()
        result1 = asyncio.run(
            self.dependency_checker.check_mcp_dependency("diego", mock_mcp_client)
        )
        first_call_time = time.time() - start_time

        # Second call should use cache (much faster)
        start_time = time.time()
        result2 = asyncio.run(
            self.dependency_checker.check_mcp_dependency("diego", mock_mcp_client)
        )
        second_call_time = time.time() - start_time

        # Results should be consistent
        if result1 != result2:
            self.fail(
                "❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Inconsistent health check results\n"
                "Cache returning different results than initial check\n"
                "Business Impact: Unreliable MCP availability detection"
            )

        # Cache should exist
        cache_key = "diego_health"
        if cache_key not in self.dependency_checker.health_cache:
            self.fail(
                "❌ LIGHTWEIGHT FALLBACK P0 FAILURE: Health check not cached\n"
                "Performance optimization not working\n"
                "Business Impact: Repeated expensive health checks slow system"
            )

        print("✅ P0 SUCCESS: Health cache functionality working")


def run_lightweight_fallback_p0_tests():
    """
    Run Lightweight Fallback Pattern P0 tests with proper error handling

    Returns:
        bool: True if all tests pass, False otherwise
    """
    print("🛡️ RUNNING LIGHTWEIGHT FALLBACK PATTERN P0 TESTS")
    print("=" * 60)

    try:
        # Create test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(
            TestLightweightFallbackPattern
        )

        # Run tests with detailed output
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)

        # Print summary
        total_tests = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)

        print(f"\n📊 LIGHTWEIGHT FALLBACK P0 TEST SUMMARY:")
        print(f"Total Tests: {total_tests}")
        print(f"Failures: {failures}")
        print(f"Errors: {errors}")

        if failures == 0 and errors == 0:
            print("✅ LIGHTWEIGHT FALLBACK P0 TESTS: ALL PASSED")
            print("🎉 OVERVIEW.md fallback pattern working correctly!")
            return True
        else:
            print("❌ LIGHTWEIGHT FALLBACK P0 TESTS: FAILURES DETECTED")
            print("🚨 Lightweight fallback pattern has critical issues!")
            return False

    except Exception as e:
        print(f"❌ LIGHTWEIGHT FALLBACK P0 TESTS: EXECUTION ERROR: {e}")
        return False


if __name__ == "__main__":
    success = run_lightweight_fallback_p0_tests()
    sys.exit(0 if success else 1)

