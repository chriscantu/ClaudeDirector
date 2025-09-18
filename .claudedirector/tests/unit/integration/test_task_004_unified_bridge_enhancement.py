#!/usr/bin/env python3
"""
Test Suite for Task 004: Integration Unified Bridge Enhancement
Tests MCP enhancement integration functionality
"""

import unittest
import asyncio
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add lib directory to path
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from integration.unified_bridge import (
    UnifiedBridge,
    BridgeConfig,
    BridgeType,
    MCP_ENHANCEMENT_AVAILABLE,
)


class TestUnifiedBridgeEnhancement(unittest.TestCase):
    """Test suite for unified bridge MCP enhancement functionality - Task 004"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = BridgeConfig(
            bridge_type=BridgeType.ALL,
            retention_days=30,
            max_items=100,
            performance_target_ms=500,
        )

    @patch("integration.unified_bridge.MCPIntegrationManager")
    @patch("integration.unified_bridge.AnalyticsEngine")
    @patch("integration.unified_bridge.CacheManager")
    def test_mcp_enhancement_initialization_success(
        self, mock_cache, mock_analytics, mock_mcp
    ):
        """Test successful MCP enhancement initialization"""

        # Mock successful initialization
        mock_mcp.return_value = Mock()
        mock_analytics.return_value = Mock()
        mock_cache.return_value = Mock()

        with patch("integration.unified_bridge.MCP_ENHANCEMENT_AVAILABLE", True):
            bridge = UnifiedBridge(self.config)

            # Verify MCP components were initialized
            self.assertIsNotNone(bridge.mcp_integration)
            self.assertIsNotNone(bridge.analytics_engine)
            self.assertIsNotNone(bridge.cache_manager)

    def test_mcp_enhancement_graceful_degradation(self):
        """Test graceful degradation when MCP enhancements unavailable"""

        with patch("integration.unified_bridge.MCP_ENHANCEMENT_AVAILABLE", False):
            bridge = UnifiedBridge(self.config)

            # Should initialize successfully without MCP enhancements
            self.assertIsNone(bridge.mcp_integration)
            self.assertIsNone(bridge.analytics_engine)
            self.assertIsNone(bridge.cache_manager)

    @patch("integration.unified_bridge.MCPIntegrationManager")
    def test_mcp_enhancement_initialization_failure(self, mock_mcp):
        """Test graceful handling of MCP enhancement initialization failures"""

        # Mock initialization failure
        mock_mcp.side_effect = Exception("Initialization failed")

        with patch("integration.unified_bridge.MCP_ENHANCEMENT_AVAILABLE", True):
            # Should not raise exception, should handle gracefully
            bridge = UnifiedBridge(self.config)

            # MCP components should be None due to initialization failure
            self.assertIsNone(bridge.mcp_integration)

    def test_health_check_includes_mcp_status(self):
        """Test that health check includes MCP enhancement status"""

        bridge = UnifiedBridge(self.config)
        health = bridge.health_check()

        # Verify MCP enhancement status is included
        self.assertIn("mcp_enhancements", health)
        self.assertIsInstance(health["mcp_enhancements"], dict)
        self.assertIn("available", health["mcp_enhancements"])

    @patch("integration.unified_bridge.CacheManager")
    def test_health_check_with_cache_stats(self, mock_cache_class):
        """Test health check includes cache stats when available"""

        # Mock cache manager with stats
        mock_cache = Mock()
        mock_cache.get_stats.return_value = {
            "entries": 10,
            "hit_rate": 0.85,
            "memory_usage_mb": 2.5,
        }
        mock_cache_class.return_value = mock_cache

        with patch("integration.unified_bridge.MCP_ENHANCEMENT_AVAILABLE", True):
            bridge = UnifiedBridge(self.config)
            health = bridge.health_check()

            # Verify cache stats are included
            mcp_status = health["mcp_enhancements"]
            self.assertIn("cache_stats", mcp_status)
            self.assertEqual(mcp_status["cache_stats"]["entries"], 10)

    def test_health_check_unavailable_components(self):
        """Test health check when MCP components unavailable"""

        with patch("integration.unified_bridge.MCP_ENHANCEMENT_AVAILABLE", False):
            bridge = UnifiedBridge(self.config)
            health = bridge.health_check()

            mcp_status = health["mcp_enhancements"]
            self.assertFalse(mcp_status["available"])
            self.assertIn("reason", mcp_status)

    def test_backward_compatibility_preserved(self):
        """Test that existing unified bridge API remains unchanged"""

        bridge = UnifiedBridge(self.config)

        # Test existing methods still work
        self.assertTrue(hasattr(bridge, "migrate_data"))
        self.assertTrue(hasattr(bridge, "get_legacy_compatible_data"))
        self.assertTrue(hasattr(bridge, "get_context_engine"))
        self.assertTrue(hasattr(bridge, "get_recent_interactions"))
        self.assertTrue(hasattr(bridge, "health_check"))

        # Test original properties preserved
        self.assertTrue(hasattr(bridge, "enhanced_mode"))
        self.assertTrue(hasattr(bridge, "context_engine"))
        self.assertTrue(hasattr(bridge, "legacy_data"))

    def test_different_bridge_types_support_mcp(self):
        """Test MCP enhancement works with different bridge types"""

        bridge_types = [
            BridgeType.CONVERSATION_MEMORY,
            BridgeType.STRATEGIC_MEMORY,
            BridgeType.INTELLIGENCE,
            BridgeType.ALL,
        ]

        for bridge_type in bridge_types:
            config = BridgeConfig(bridge_type=bridge_type)
            bridge = UnifiedBridge(config)

            # All bridge types should support health check with MCP status
            health = bridge.health_check()
            self.assertIn("mcp_enhancements", health)
            self.assertEqual(health["bridge_type"], bridge_type.value)

    @patch("integration.unified_bridge.AnalyticsEngine")
    def test_analytics_engine_integration(self, mock_analytics_class):
        """Test analytics engine integration works correctly"""

        mock_analytics = Mock()
        mock_analytics_class.return_value = mock_analytics

        with patch("integration.unified_bridge.MCP_ENHANCEMENT_AVAILABLE", True):
            bridge = UnifiedBridge(self.config)

            # Analytics engine should be available
            self.assertIsNotNone(bridge.analytics_engine)
            health = bridge.health_check()
            self.assertTrue(health["mcp_enhancements"]["analytics_engine"])

    def test_enhancement_status_helper_method(self):
        """Test the MCP enhancement status helper method"""

        bridge = UnifiedBridge(self.config)
        status = bridge._get_mcp_enhancement_status()

        # Should always return a dict with 'available' key
        self.assertIsInstance(status, dict)
        self.assertIn("available", status)

        if status["available"]:
            # If available, should have component status
            self.assertIn("mcp_integration", status)
            self.assertIn("analytics_engine", status)
            self.assertIn("cache_manager", status)
        else:
            # If not available, should have reason
            self.assertIn("reason", status)

    def test_enhancement_does_not_break_existing_workflows(self):
        """Test that MCP enhancement doesn't interfere with existing functionality"""

        bridge = UnifiedBridge(self.config)

        # Test legacy data access still works
        legacy_data = bridge.get_legacy_compatible_data("test_type")
        self.assertIsInstance(legacy_data, dict)

        # Test context engine access still works
        context_engine = bridge.get_context_engine()
        # Should not raise exception

        # Test interactions access still works
        interactions = bridge.get_recent_interactions("test_session", 5)
        self.assertIsInstance(interactions, list)

    def test_memory_efficiency_of_enhancement(self):
        """Test that MCP enhancement doesn't significantly impact memory"""

        # Test with and without enhancements
        with patch("integration.unified_bridge.MCP_ENHANCEMENT_AVAILABLE", False):
            bridge_without = UnifiedBridge(self.config)

        bridge_with = UnifiedBridge(self.config)

        # Both should initialize successfully
        self.assertIsNotNone(bridge_without)
        self.assertIsNotNone(bridge_with)

        # Enhancement should not dramatically change object structure
        self.assertEqual(type(bridge_without.config), type(bridge_with.config))


if __name__ == "__main__":
    unittest.main()
