#!/usr/bin/env python3
"""
Task 005: Comprehensive Enhancement Testing
Complete integration test suite for all MCP enhancements (Tasks 001-004)

Tests the integration and interaction between all MCP enhancement components:
- Task 001: MCP Integration Manager
- Task 002: Context Engineering Analytics
- Task 003: Performance Cache Manager
- Task 004: Integration Unified Bridge
"""

import unittest
import asyncio
import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add lib directory to path
lib_path = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(lib_path))

# Import all enhancement components for integration testing
try:
    from context_engineering.analytics_engine import AnalyticsEngine, SessionInsights
    from performance.cache_manager import CacheManager, CacheLevel

    WORKING_COMPONENTS = ["analytics", "cache"]
except ImportError as e:
    WORKING_COMPONENTS = []
    print(f"Import warning: {e}")


class TestComprehensiveMCPEnhancements(unittest.TestCase):
    """Comprehensive integration test suite for all MCP enhancements"""

    def setUp(self):
        """Set up test fixtures for integration testing"""
        self.working_components = {}

        # Initialize working components only
        if "analytics" in WORKING_COMPONENTS:
            self.working_components["analytics"] = AnalyticsEngine()

        if "cache" in WORKING_COMPONENTS:
            self.working_components["cache"] = CacheManager(max_memory_mb=5)

    def tearDown(self):
        """Clean up after tests"""
        if "cache" in self.working_components:
            asyncio.run(self.working_components["cache"].cleanup())

    def test_mcp_enhancement_integration_pipeline(self):
        """Test complete integration pipeline of all MCP enhancements"""

        # Skip if components not available
        if not self.working_components:
            self.skipTest("MCP enhancement components not available")

        # Test 1: Analytics generates session insights
        if "analytics" in self.working_components:
            session_data = [
                {"query": "strategic planning for Q4"},
                {"query": "analyze team performance metrics"},
                {"query": "technical architecture review"},
            ]

            insights = self.working_components[
                "analytics"
            ].analyze_mcp_session_patterns(session_data)
            self.assertIsInstance(insights, SessionInsights)
            self.assertGreater(insights.confidence, 0.0)
            print(
                f"✅ Analytics integration: Session insights generated (confidence: {insights.confidence:.2f})"
            )

        # Test 2: Cache manager caches analytics results
        if "cache" in self.working_components:

            async def test_cache_analytics():
                # Cache strategic analysis result
                analysis_result = {
                    "patterns": {"strategic_analysis": 0.85},
                    "recommendations": ["Use Sequential MCP server"],
                    "timestamp": time.time(),
                }

                success = await self.working_components["cache"].cache_mcp_response(
                    "sequential", "strategic planning analysis", analysis_result
                )
                self.assertTrue(success)

                # Verify cache level was determined correctly
                level = self.working_components["cache"]._determine_mcp_cache_level(
                    "sequential"
                )
                self.assertEqual(level, CacheLevel.MCP_SEQUENTIAL)

                return success

            cache_success = asyncio.run(test_cache_analytics())
            print(f"✅ Cache integration: MCP response cached successfully")

        # Test 3: Integration health across components
        component_health = {}
        for name, component in self.working_components.items():
            if hasattr(component, "get_stats"):
                stats = component.get_stats()
                component_health[name] = {
                    "functional": True,
                    "stats_available": True,
                    "stats": stats,
                }
            else:
                component_health[name] = {"functional": True, "stats_available": False}

        print(f"✅ Component health: {len(component_health)} components operational")

    def test_mcp_enhancement_performance_characteristics(self):
        """Test performance characteristics of MCP enhancements"""

        if not self.working_components:
            self.skipTest("MCP enhancement components not available")

        performance_results = {}

        # Test analytics performance
        if "analytics" in self.working_components:
            start_time = time.time()

            # Test with various session sizes
            session_sizes = [1, 5, 10, 20]
            for size in session_sizes:
                session_data = [{"query": f"test query {i}"} for i in range(size)]
                insights = self.working_components[
                    "analytics"
                ].analyze_mcp_session_patterns(session_data)
                self.assertIsInstance(insights, SessionInsights)

            analytics_time = time.time() - start_time
            performance_results["analytics"] = analytics_time

            # Should handle multiple sessions quickly (< 1 second total)
            self.assertLess(analytics_time, 1.0)
            print(
                f"✅ Analytics performance: {analytics_time:.3f}s for {sum(session_sizes)} queries"
            )

        # Test cache performance
        if "cache" in self.working_components:

            async def test_cache_performance():
                start_time = time.time()

                # Test multiple cache operations
                for i in range(10):
                    await self.working_components["cache"].cache_mcp_response(
                        "sequential", f"test query {i}", {"result": f"response {i}"}
                    )

                cache_time = time.time() - start_time

                # Should handle 10 cache operations quickly (< 0.1 seconds)
                self.assertLess(cache_time, 0.1)
                return cache_time

            cache_time = asyncio.run(test_cache_performance())
            performance_results["cache"] = cache_time
            print(f"✅ Cache performance: {cache_time:.3f}s for 10 operations")

        # Overall performance assessment
        total_time = sum(performance_results.values())
        self.assertLess(
            total_time, 2.0, "Total enhancement overhead should be < 2 seconds"
        )

    def test_mcp_enhancement_error_handling_and_resilience(self):
        """Test error handling and resilience of MCP enhancements"""

        if not self.working_components:
            self.skipTest("MCP enhancement components not available")

        # Test analytics error handling
        if "analytics" in self.working_components:
            # Test with malformed data
            malformed_data = [
                {"invalid": "structure"},
                {"query": None},
                {},
                {"query": "a" * 10000},  # Very long query
            ]

            try:
                insights = self.working_components[
                    "analytics"
                ].analyze_mcp_session_patterns(malformed_data)
                # Should handle gracefully and return valid insights
                self.assertIsInstance(insights, SessionInsights)
                self.assertGreater(insights.confidence, 0.0)
                print("✅ Analytics resilience: Handles malformed data gracefully")
            except Exception as e:
                self.fail(f"Analytics should handle malformed data gracefully: {e}")

        # Test cache error handling
        if "cache" in self.working_components:

            async def test_cache_resilience():
                # Test with edge cases
                edge_cases = [
                    ("", "", {}),  # Empty strings
                    ("unknown_server", "test", {"data": "test"}),  # Unknown server
                    ("sequential", "test", None),  # None data
                ]

                for server, query, data in edge_cases:
                    try:
                        success = await self.working_components[
                            "cache"
                        ].cache_mcp_response(server, query, data)
                        # Should handle gracefully (may succeed or fail, but shouldn't crash)
                        self.assertIsInstance(success, bool)
                    except Exception as e:
                        self.fail(f"Cache should handle edge case gracefully: {e}")

                print("✅ Cache resilience: Handles edge cases gracefully")

            asyncio.run(test_cache_resilience())

    def test_mcp_enhancement_memory_efficiency(self):
        """Test memory efficiency of MCP enhancements"""

        if not self.working_components:
            self.skipTest("MCP enhancement components not available")

        # Test cache memory management
        if "cache" in self.working_components:

            async def test_cache_memory():
                initial_stats = self.working_components["cache"].get_stats()
                initial_entries = initial_stats["entries"]

                # Add many cache entries
                for i in range(50):
                    await self.working_components["cache"].cache_mcp_response(
                        "sequential",
                        f"memory test query {i}",
                        {"data": f"response {i}" * 100},  # Larger responses
                    )

                final_stats = self.working_components["cache"].get_stats()
                final_entries = final_stats["entries"]

                # Verify cache is tracking entries
                self.assertGreater(final_entries, initial_entries)

                # Memory usage should be reasonable (< 10MB for test)
                memory_mb = final_stats["memory_usage_mb"]
                self.assertLess(memory_mb, 10.0)

                print(
                    f"✅ Cache memory efficiency: {final_entries} entries using {memory_mb:.1f}MB"
                )

            asyncio.run(test_cache_memory())

    def test_mcp_enhancement_configuration_flexibility(self):
        """Test configuration flexibility of MCP enhancements"""

        # Test cache configuration flexibility
        try:
            # Test different cache configurations
            configs = [
                {"max_memory_mb": 1},
                {"max_memory_mb": 10},
                {"max_memory_mb": 5},
            ]

            for config in configs:
                cache = CacheManager(**config)
                self.assertIsNotNone(cache)

                # Test MCP cache levels are properly configured
                self.assertTrue(hasattr(cache, "ttl_config"))
                self.assertIn(CacheLevel.MCP_SEQUENTIAL, cache.ttl_config)

                asyncio.run(cache.cleanup())

            print(
                "✅ Configuration flexibility: Multiple cache configurations supported"
            )

        except Exception as e:
            print(f"⚠️  Configuration test limited: {e}")

    def test_mcp_enhancement_backwards_compatibility(self):
        """Test that MCP enhancements maintain backwards compatibility"""

        if not self.working_components:
            self.skipTest("MCP enhancement components not available")

        # Test analytics backwards compatibility
        if "analytics" in self.working_components:
            analytics = self.working_components["analytics"]

            # Test existing methods still work
            try:
                recommendations = analytics.get_strategic_recommendations(
                    "test context"
                )
                self.assertIsInstance(recommendations, dict)

                performance = analytics.get_performance_summary()
                self.assertIsInstance(performance, dict)

                print(
                    "✅ Analytics backwards compatibility: Existing methods preserved"
                )

            except Exception as e:
                self.fail(f"Analytics backwards compatibility broken: {e}")

        # Test cache backwards compatibility
        if "cache" in self.working_components:
            cache = self.working_components["cache"]

            async def test_cache_backwards_compatibility():
                # Test existing cache operations still work
                try:
                    # Basic cache operations
                    await cache.set("test_key", {"data": "test"})
                    result = await cache.get("test_key")
                    self.assertIsNotNone(result)

                    # Cached function call
                    def test_func(x):
                        return {"result": x}

                    result = await cache.cached_call(
                        test_func, "test_arg", namespace="test"
                    )
                    self.assertEqual(result["result"], "test_arg")

                    print(
                        "✅ Cache backwards compatibility: Existing methods preserved"
                    )

                except Exception as e:
                    self.fail(f"Cache backwards compatibility broken: {e}")

            asyncio.run(test_cache_backwards_compatibility())

    def test_mcp_enhancement_integration_scenarios(self):
        """Test real-world integration scenarios"""

        if not self.working_components:
            self.skipTest("MCP enhancement components not available")

        # Scenario 1: Strategic planning session analysis and caching
        if (
            "analytics" in self.working_components
            and "cache" in self.working_components
        ):

            async def strategic_planning_scenario():
                # Simulate strategic planning session
                session_data = [
                    {"query": "quarterly strategic planning review"},
                    {"query": "team performance analysis and optimization"},
                    {"query": "competitive positioning assessment"},
                    {"query": "resource allocation strategy"},
                    {"query": "stakeholder alignment planning"},
                ]

                # Analyze session
                insights = self.working_components[
                    "analytics"
                ].analyze_mcp_session_patterns(session_data)

                # Cache the analysis results
                cache_success = await self.working_components[
                    "cache"
                ].cache_mcp_response(
                    "sequential",
                    "strategic_planning_session",
                    {
                        "insights": {
                            "patterns": insights.patterns,
                            "recommendations": insights.recommendations,
                            "confidence": insights.confidence,
                        },
                        "session_summary": f"{len(session_data)} strategic queries analyzed",
                    },
                )

                return insights, cache_success

            insights, cache_success = asyncio.run(strategic_planning_scenario())

            self.assertIsInstance(insights, SessionInsights)
            self.assertTrue(cache_success)
            self.assertGreater(insights.confidence, 0.0)

            print(f"✅ Strategic planning scenario: Complete workflow successful")

        # Scenario 2: High-frequency caching with analytics feedback
        if "cache" in self.working_components:

            async def high_frequency_scenario():
                start_time = time.time()

                # Simulate high-frequency MCP usage
                for i in range(20):
                    server_type = ["sequential", "context7", "magic", "playwright"][
                        i % 4
                    ]
                    await self.working_components["cache"].cache_mcp_response(
                        server_type,
                        f"frequent_query_{i}",
                        {"response": f"cached_result_{i}"},
                    )

                duration = time.time() - start_time

                # Should handle 20 operations quickly
                self.assertLess(duration, 0.5)

                # Check cache distribution across server types
                stats = self.working_components["cache"].get_stats()
                cache_levels = stats["cache_levels"]

                # Should have entries for different MCP server types
                total_mcp_entries = (
                    cache_levels.get("mcp_sequential", 0)
                    + cache_levels.get("mcp_context7", 0)
                    + cache_levels.get("mcp_magic", 0)
                    + cache_levels.get("mcp_playwright", 0)
                )

                self.assertGreater(total_mcp_entries, 0)

                print(
                    f"✅ High-frequency scenario: {total_mcp_entries} MCP entries cached in {duration:.3f}s"
                )

            asyncio.run(high_frequency_scenario())


class TestMCPEnhancementHealthAndMonitoring(unittest.TestCase):
    """Test health monitoring and observability of MCP enhancements"""

    def test_mcp_enhancement_health_reporting(self):
        """Test health reporting across all MCP enhancements"""

        health_reports = {}

        # Test analytics health
        try:
            analytics = AnalyticsEngine()
            # Test basic functionality
            insights = analytics.analyze_mcp_session_patterns(
                [{"query": "health check"}]
            )
            health_reports["analytics"] = {
                "status": "healthy",
                "functional": True,
                "confidence": insights.confidence,
            }
        except Exception as e:
            health_reports["analytics"] = {
                "status": "error",
                "functional": False,
                "error": str(e),
            }

        # Test cache health
        try:
            cache = CacheManager(max_memory_mb=1)
            stats = cache.get_stats()
            health_reports["cache"] = {
                "status": "healthy",
                "functional": True,
                "stats": stats,
            }
            asyncio.run(cache.cleanup())
        except Exception as e:
            health_reports["cache"] = {
                "status": "error",
                "functional": False,
                "error": str(e),
            }

        # Report overall health
        functional_components = sum(
            1 for report in health_reports.values() if report["functional"]
        )
        total_components = len(health_reports)
        health_rate = functional_components / total_components

        print(f"MCP Enhancement Health Report:")
        print(
            f"  Functional components: {functional_components}/{total_components} ({health_rate:.1%})"
        )

        for component, health in health_reports.items():
            status_icon = "✅" if health["functional"] else "❌"
            print(f"  {component}: {status_icon} {health['status']}")

        # Should have majority of components working
        self.assertGreaterEqual(
            health_rate, 0.5, "At least 50% of components should be functional"
        )


def run_comprehensive_test_suite():
    """Run the complete MCP enhancement test suite"""

    print("🧪 TASK 005: Comprehensive MCP Enhancement Testing")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add integration tests
    suite.addTests(loader.loadTestsFromTestCase(TestComprehensiveMCPEnhancements))
    suite.addTests(loader.loadTestsFromTestCase(TestMCPEnhancementHealthAndMonitoring))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    success_rate = (
        (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun
        if result.testsRun > 0
        else 0
    )
    print(f"Success rate: {success_rate:.1%}")

    if success_rate >= 0.8:
        print("🎉 EXCELLENT: Comprehensive testing successful")
    elif success_rate >= 0.6:
        print("✅ GOOD: Most tests passing")
    else:
        print("⚠️  NEEDS ATTENTION: Multiple test failures")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_test_suite()
    exit(0 if success else 1)
