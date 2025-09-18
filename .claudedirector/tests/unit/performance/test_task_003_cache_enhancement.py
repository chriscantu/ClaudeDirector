#!/usr/bin/env python3
"""
Test Suite for Task 003: Performance Cache Manager Enhancement
Tests MCP-specific intelligent caching functionality
"""

import unittest
import asyncio
import sys
from pathlib import Path

# Add lib directory to path
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from performance.cache_manager import CacheManager, CacheLevel


class TestMCPCacheEnhancement(unittest.TestCase):
    """Test suite for MCP cache enhancement functionality - Task 003"""

    def setUp(self):
        """Set up test fixtures"""
        self.cache_manager = CacheManager(max_memory_mb=10)

    def tearDown(self):
        """Clean up after tests"""
        asyncio.run(self.cache_manager.cleanup())

    def test_mcp_cache_levels_exist(self):
        """Test that MCP-specific cache levels are defined"""

        # Verify all MCP cache levels exist
        self.assertTrue(hasattr(CacheLevel, "MCP_SEQUENTIAL"))
        self.assertTrue(hasattr(CacheLevel, "MCP_CONTEXT7"))
        self.assertTrue(hasattr(CacheLevel, "MCP_MAGIC"))
        self.assertTrue(hasattr(CacheLevel, "MCP_PLAYWRIGHT"))

        # Verify values are correct
        self.assertEqual(CacheLevel.MCP_SEQUENTIAL.value, "mcp_sequential")
        self.assertEqual(CacheLevel.MCP_CONTEXT7.value, "mcp_context7")
        self.assertEqual(CacheLevel.MCP_MAGIC.value, "mcp_magic")
        self.assertEqual(CacheLevel.MCP_PLAYWRIGHT.value, "mcp_playwright")

    def test_mcp_ttl_configuration(self):
        """Test MCP-specific TTL configuration"""

        # Verify MCP TTL values are properly configured
        self.assertEqual(
            self.cache_manager.ttl_config[CacheLevel.MCP_SEQUENTIAL], 600
        )  # 10 min
        self.assertEqual(
            self.cache_manager.ttl_config[CacheLevel.MCP_CONTEXT7], 1800
        )  # 30 min
        self.assertEqual(
            self.cache_manager.ttl_config[CacheLevel.MCP_MAGIC], 900
        )  # 15 min
        self.assertEqual(
            self.cache_manager.ttl_config[CacheLevel.MCP_PLAYWRIGHT], 300
        )  # 5 min

    def test_mcp_cache_level_determination(self):
        """Test intelligent cache level determination for MCP servers"""

        # Test Sequential server mapping
        level = self.cache_manager._determine_mcp_cache_level("sequential")
        self.assertEqual(level, CacheLevel.MCP_SEQUENTIAL)

        # Test Context7 server mapping
        level = self.cache_manager._determine_mcp_cache_level("context7")
        self.assertEqual(level, CacheLevel.MCP_CONTEXT7)

        # Test Magic server mapping
        level = self.cache_manager._determine_mcp_cache_level("magic")
        self.assertEqual(level, CacheLevel.MCP_MAGIC)

        # Test Playwright server mapping
        level = self.cache_manager._determine_mcp_cache_level("playwright")
        self.assertEqual(level, CacheLevel.MCP_PLAYWRIGHT)

        # Test unknown server fallback
        level = self.cache_manager._determine_mcp_cache_level("unknown")
        self.assertEqual(level, CacheLevel.MCP_RESPONSES)

    def test_mcp_response_caching(self):
        """Test MCP response caching functionality"""

        async def test_caching():
            # Test caching different server types
            test_response = {
                "result": "strategic analysis complete",
                "confidence": 0.95,
            }

            # Cache Sequential response
            success = await self.cache_manager.cache_mcp_response(
                "sequential", "analyze strategic planning approach", test_response
            )
            self.assertTrue(success)

            # Cache Context7 response
            doc_response = {"documentation": "API reference", "examples": []}
            success = await self.cache_manager.cache_mcp_response(
                "context7", "show API documentation", doc_response
            )
            self.assertTrue(success)

            # Verify cache entries were created with correct levels
            stats = self.cache_manager.get_stats()
            self.assertEqual(stats["entries"], 2)

            # Verify different cache levels are used
            mcp_sequential_count = stats["cache_levels"]["mcp_sequential"]
            mcp_context7_count = stats["cache_levels"]["mcp_context7"]
            self.assertEqual(mcp_sequential_count, 1)
            self.assertEqual(mcp_context7_count, 1)

        asyncio.run(test_caching())

    def test_case_insensitive_server_mapping(self):
        """Test case-insensitive server type mapping"""

        # Test uppercase
        level = self.cache_manager._determine_mcp_cache_level("SEQUENTIAL")
        self.assertEqual(level, CacheLevel.MCP_SEQUENTIAL)

        # Test mixed case
        level = self.cache_manager._determine_mcp_cache_level("Context7")
        self.assertEqual(level, CacheLevel.MCP_CONTEXT7)

        level = self.cache_manager._determine_mcp_cache_level("Magic")
        self.assertEqual(level, CacheLevel.MCP_MAGIC)

        level = self.cache_manager._determine_mcp_cache_level("PLAYWRIGHT")
        self.assertEqual(level, CacheLevel.MCP_PLAYWRIGHT)

    def test_mcp_cache_key_generation(self):
        """Test MCP cache key generation"""

        async def test_key_generation():
            # Test that different server types generate different keys
            await self.cache_manager.cache_mcp_response(
                "sequential", "test query", {"result": "seq"}
            )
            await self.cache_manager.cache_mcp_response(
                "context7", "test query", {"result": "ctx7"}
            )

            # Should have 2 different cache entries for same query but different servers
            stats = self.cache_manager.get_stats()
            self.assertEqual(stats["entries"], 2)

        asyncio.run(test_key_generation())

    def test_enhancement_backward_compatibility(self):
        """Test that enhancement doesn't break existing functionality"""

        async def test_compatibility():
            # Test existing cache operations still work
            success = await self.cache_manager.set(
                "test_key", {"data": "test"}, CacheLevel.CONTEXT_ANALYSIS
            )
            self.assertTrue(success)

            # Test retrieval works
            result = await self.cache_manager.get("test_key")
            self.assertIsNotNone(result)
            self.assertEqual(result["data"], "test")

            # Test cached_call works
            def test_function(arg):
                return {"processed": arg}

            result = await self.cache_manager.cached_call(
                test_function,
                "test_arg",
                cache_level=CacheLevel.FRAMEWORK_PATTERNS,
                namespace="test",
            )
            self.assertEqual(result["processed"], "test_arg")

        asyncio.run(test_compatibility())

    def test_integration_with_base_manager(self):
        """Test that MCP enhancement integrates properly with BaseManager"""

        # Test that BaseManager metrics still work
        stats = self.cache_manager.get_stats()

        # Should have both cache-specific and BaseManager metrics
        self.assertIn("entries", stats)
        self.assertIn("cache_hits", stats)
        self.assertIn("cache_misses", stats)
        self.assertIn("cache_levels", stats)

        # Verify MCP cache levels are included in stats
        cache_levels = stats["cache_levels"]
        self.assertIn("mcp_sequential", cache_levels)
        self.assertIn("mcp_context7", cache_levels)
        self.assertIn("mcp_magic", cache_levels)
        self.assertIn("mcp_playwright", cache_levels)


if __name__ == "__main__":
    unittest.main()
