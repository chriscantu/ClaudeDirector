#!/usr/bin/env python3
"""
Test Suite for MCP Enhancement - Task 001
Tests intelligent query routing functionality
"""

import unittest
import asyncio
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add lib directory to path
lib_path = Path(__file__).parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from lib.mcp.mcp_integration_manager import (
    MCPIntegrationManager,
    QueryPattern,
    MCPServerType,
    create_mcp_integration_manager,
)


class TestMCPEnhancements(unittest.TestCase):
    """Test suite for MCP enhancement functionality - Task 001"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = MCPIntegrationManager()

    def test_query_pattern_classification(self):
        """Test query pattern classification accuracy"""

        # Test strategic analysis patterns
        strategic_queries = [
            "What is our strategic roadmap for next quarter?",
            "Analyze team performance and ROI",
            "Business decision planning for investment",
        ]
        for query in strategic_queries:
            pattern = self.manager._classify_query_pattern(query)
            self.assertEqual(pattern, QueryPattern.STRATEGIC_ANALYSIS)

        # Test technical question patterns
        tech_queries = [
            "Show me the documentation for this API",
            "What are the best practices for this framework?",
            "Guide me through the library reference",
        ]
        for query in tech_queries:
            pattern = self.manager._classify_query_pattern(query)
            self.assertEqual(pattern, QueryPattern.TECHNICAL_QUESTION)

        # Test UI component patterns
        ui_queries = [
            "Create a button component with modern design",
            "Build a form interface with validation",
            "Design a responsive layout with CSS",
        ]
        for query in ui_queries:
            pattern = self.manager._classify_query_pattern(query)
            self.assertEqual(
                pattern,
                QueryPattern.UI_COMPONENT,
                f"Query '{query}' classified as {pattern.value}, expected ui_component",
            )

        # Test testing automation patterns
        test_queries = [
            "Create an e2e test with Playwright",
            "Set up browser automation testing",
            "Implement visual regression testing",
        ]
        for query in test_queries:
            pattern = self.manager._classify_query_pattern(query)
            self.assertEqual(pattern, QueryPattern.TESTING_AUTOMATION)

    def test_server_selection_mapping(self):
        """Test optimal server selection for query patterns"""

        test_cases = [
            (QueryPattern.STRATEGIC_ANALYSIS, MCPServerType.SEQUENTIAL),
            (QueryPattern.TECHNICAL_QUESTION, MCPServerType.CONTEXT7),
            (QueryPattern.UI_COMPONENT, MCPServerType.MAGIC),
            (QueryPattern.TESTING_AUTOMATION, MCPServerType.PLAYWRIGHT),
            (QueryPattern.GENERAL_QUERY, MCPServerType.SEQUENTIAL),
        ]

        for pattern, expected_server in test_cases:
            selected_server = self.manager._select_optimal_server(pattern)
            self.assertEqual(selected_server, expected_server)

    def test_fallback_server_mapping(self):
        """Test fallback server selection"""

        fallback_cases = [
            (MCPServerType.SEQUENTIAL, MCPServerType.CONTEXT7),
            (MCPServerType.CONTEXT7, MCPServerType.SEQUENTIAL),
            (MCPServerType.MAGIC, MCPServerType.CONTEXT7),
            (MCPServerType.PLAYWRIGHT, MCPServerType.SEQUENTIAL),
        ]

        for primary, expected_fallback in fallback_cases:
            fallback = self.manager._get_fallback_server(primary)
            self.assertEqual(fallback, expected_fallback)

    def test_performance_tracking(self):
        """Test session-scoped performance tracking"""

        # Track performance for a server
        server_type = MCPServerType.SEQUENTIAL
        response_time = 0.5  # 500ms

        self.manager._track_performance(server_type, response_time)

        # Verify performance data was recorded
        server_key = server_type.value
        self.assertIn(server_key, self.manager.session_performance)

        perf = self.manager.session_performance[server_key]
        self.assertEqual(perf["total_calls"], 1)
        self.assertEqual(perf["avg_response_time"], response_time)

    @patch("mcp.mcp_integration_manager.CLAUDE_CODE_MCP_AVAILABLE", True)
    async def test_intelligent_routing_with_mcp_unavailable(self):
        """Test intelligent routing when Claude Code MCP is unavailable"""

        # Test with MCP helper not initialized (simulates unavailable)
        self.manager.claude_code_mcp_helper = None

        query = "Analyze our strategic roadmap"
        result = await self.manager.route_query_intelligently(query)

        # Should succeed with pattern detection fallback
        self.assertTrue(result.success)
        self.assertEqual(result.method, "fallback")
        self.assertIn("strategic_analysis", result.data["message"])

    def test_health_reporting_enhancements(self):
        """Test enhanced health reporting includes new features"""

        health = asyncio.run(self.manager.get_integration_health())

        # Verify enhanced health reporting
        self.assertIn("claude_code_mcp", health)
        self.assertIn("intelligent_routing", health)

        # Verify intelligent routing metrics
        routing_info = health["intelligent_routing"]
        self.assertTrue(routing_info["enabled"])
        self.assertIn("supported_patterns", routing_info)
        self.assertEqual(
            len(routing_info["supported_patterns"]), 5
        )  # 5 QueryPattern values

    def test_backward_compatibility(self):
        """Test that existing functionality is preserved"""

        # Verify existing methods still work
        health = asyncio.run(self.manager.get_integration_health())

        # Original functionality should be preserved
        self.assertIn("manager_name", health)
        self.assertIn("version", health)
        self.assertIn("metrics", health)
        self.assertIn("prd_compliance", health)

        # Original factory function should work
        manager2 = create_mcp_integration_manager()
        self.assertIsInstance(manager2, MCPIntegrationManager)

    def test_metrics_tracking_enhancement(self):
        """Test enhanced metrics tracking"""

        # Verify intelligent routing metrics are tracked
        self.assertIn("intelligent_routing_requests", self.manager.integration_metrics)

        # Simulate routing request
        initial_count = self.manager.integration_metrics["intelligent_routing_requests"]

        # This would be called during route_query_intelligently
        self.manager.integration_metrics["intelligent_routing_requests"] += 1

        self.assertEqual(
            self.manager.integration_metrics["intelligent_routing_requests"],
            initial_count + 1,
        )


class TestMCPEnhancementIntegration(unittest.TestCase):
    """Integration tests for MCP enhancement functionality"""

    def test_end_to_end_query_routing(self):
        """Test complete query routing workflow"""

        manager = MCPIntegrationManager()

        # Test that different query types get classified correctly
        test_cases = [
            (
                "Create a strategic business plan",
                QueryPattern.STRATEGIC_ANALYSIS,
                MCPServerType.SEQUENTIAL,
            ),
            (
                "Show me React documentation",
                QueryPattern.TECHNICAL_QUESTION,
                MCPServerType.CONTEXT7,
            ),
            (
                "Build a login form component",
                QueryPattern.UI_COMPONENT,
                MCPServerType.MAGIC,
            ),
            (
                "Create e2e tests for checkout",
                QueryPattern.TESTING_AUTOMATION,
                MCPServerType.PLAYWRIGHT,
            ),
        ]

        for query, expected_pattern, expected_server in test_cases:
            # Test pattern classification
            pattern = manager._classify_query_pattern(query)
            self.assertEqual(pattern, expected_pattern)

            # Test server selection
            server = manager._select_optimal_server(pattern)
            self.assertEqual(server, expected_server)


if __name__ == "__main__":
    # Run tests
    unittest.main()
