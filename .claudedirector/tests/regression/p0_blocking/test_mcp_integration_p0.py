"""
P0 Blocking Tests for MCP Integration Manager

Phase 7 Week 3: Real MCP Server Integration with Zero Setup Compliance
Created: August 31, 2025
Owner: Martin (Platform Architecture) + Elena (Compliance Strategy)

CRITICAL: These tests ensure MCP integration never breaks zero-setup policy
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock

# Import path handling for different test environments
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

try:
    from .claudedirector.lib.mcp import (
        MCPIntegrationManager,
        MCPServerType,
        MCPServerStatus,
        MCPIntegrationResult,
        create_mcp_integration_manager,
    )
except ImportError:
    # Fallback for different test environments
    from claudedirector.lib.mcp import (
        MCPIntegrationManager,
        MCPServerType,
        MCPServerStatus,
        MCPIntegrationResult,
        create_mcp_integration_manager,
    )


class TestMCPIntegrationP0:
    """P0 tests for MCP Integration Manager - BLOCKING level tests"""

    @pytest.fixture
    def mcp_manager(self):
        """Create MCP Integration Manager for testing"""
        return create_mcp_integration_manager()

    def test_p0_mcp_manager_initialization(self, mcp_manager):
        """P0: MCP Integration Manager initializes successfully"""
        assert mcp_manager is not None
        assert mcp_manager.name == "mcp-integration-manager"
        assert mcp_manager.version == "1.0.0"
        assert isinstance(mcp_manager.mcp_servers, dict)
        assert MCPServerType.JIRA in mcp_manager.mcp_servers
        assert MCPServerType.GITHUB in mcp_manager.mcp_servers

    @pytest.mark.asyncio
    async def test_p0_zero_setup_compliance_jira(self, mcp_manager):
        """P0: Jira integration always works without setup (zero setup policy)"""
        # This must NEVER fail - zero setup compliance
        result = await mcp_manager.fetch_jira_data("sprint_metrics")

        assert result is not None
        assert result.success is True  # Always succeeds due to graceful fallback
        assert result.data is not None
        assert isinstance(result.data, dict)
        assert result.latency_ms < 5000  # PRD requirement

        # Must work even if MCP servers unavailable
        assert result.method in ["mcp", "api_fallback"]

    @pytest.mark.asyncio
    async def test_p0_zero_setup_compliance_github(self, mcp_manager):
        """P0: GitHub integration always works without setup (zero setup policy)"""
        # This must NEVER fail - zero setup compliance
        result = await mcp_manager.fetch_github_data("repository_activity")

        assert result is not None
        assert result.success is True  # Always succeeds due to graceful fallback
        assert result.data is not None
        assert isinstance(result.data, dict)
        assert result.latency_ms < 5000  # PRD requirement

        # Must work even if MCP servers unavailable
        assert result.method in ["mcp", "api_fallback"]

    @pytest.mark.asyncio
    async def test_p0_server_detection_never_blocks(self, mcp_manager):
        """P0: Server detection never blocks or fails"""
        # Detection must complete quickly and never throw
        detection_results = await mcp_manager.check_mcp_server_availability(MCPServerType.JIRA)

        assert detection_results in [
            MCPServerStatus.AVAILABLE,
            MCPServerStatus.UNAVAILABLE,
            MCPServerStatus.FALLBACK,
            MCPServerStatus.ERROR
        ]

        # GitHub detection
        github_results = await mcp_manager.check_mcp_server_availability(MCPServerType.GITHUB)
        assert github_results in [
            MCPServerStatus.AVAILABLE,
            MCPServerStatus.UNAVAILABLE,
            MCPServerStatus.FALLBACK,
            MCPServerStatus.ERROR
        ]

    @pytest.mark.asyncio
    async def test_p0_performance_requirements(self, mcp_manager):
        """P0: All MCP operations meet performance requirements"""
        import time

        # Jira performance test
        start_time = time.time()
        jira_result = await mcp_manager.fetch_jira_data("sprint_metrics")
        jira_latency = (time.time() - start_time) * 1000

        assert jira_latency < 5000  # PRD requirement: <5s
        assert jira_result.latency_ms < 5000

        # GitHub performance test
        start_time = time.time()
        github_result = await mcp_manager.fetch_github_data("repository_activity")
        github_latency = (time.time() - start_time) * 1000

        assert github_latency < 5000  # PRD requirement: <5s
        assert github_result.latency_ms < 5000

    def test_p0_server_configuration_integrity(self, mcp_manager):
        """P0: MCP server configurations are complete and valid"""
        # Jira servers
        jira_servers = mcp_manager.mcp_servers[MCPServerType.JIRA]
        assert len(jira_servers) >= 1  # At least one Jira server configured

        for server in jira_servers:
            assert server.package_name is not None
            assert server.version is not None
            assert server.capabilities is not None
            assert isinstance(server.capabilities, list)
            assert server.fallback_api_base is not None
            assert server.priority > 0

        # GitHub servers
        github_servers = mcp_manager.mcp_servers[MCPServerType.GITHUB]
        assert len(github_servers) >= 1  # At least one GitHub server configured

        for server in github_servers:
            assert server.package_name is not None
            assert server.version is not None
            assert server.capabilities is not None
            assert isinstance(server.capabilities, list)
            assert server.fallback_api_base is not None
            assert server.priority > 0

    @pytest.mark.asyncio
    async def test_p0_graceful_degradation(self, mcp_manager):
        """P0: System gracefully degrades when MCP servers fail"""
        # Test with invalid query types - should still return data
        jira_result = await mcp_manager.fetch_jira_data("invalid_query_type")
        assert jira_result.success is True  # Graceful handling

        github_result = await mcp_manager.fetch_github_data("invalid_query_type")
        assert github_result.success is True  # Graceful handling

    @pytest.mark.asyncio
    async def test_p0_metrics_tracking(self, mcp_manager):
        """P0: Integration metrics are properly tracked"""
        # Perform some operations
        await mcp_manager.fetch_jira_data("sprint_metrics")
        await mcp_manager.fetch_github_data("repository_activity")

        # Check metrics
        assert mcp_manager.integration_metrics["total_requests"] >= 2
        assert mcp_manager.integration_metrics["avg_latency_ms"] > 0
        assert 0 <= mcp_manager.integration_metrics["success_rate"] <= 1

    @pytest.mark.asyncio
    async def test_p0_integration_health_reporting(self, mcp_manager):
        """P0: Integration health reporting works correctly"""
        health = await mcp_manager.get_integration_health()

        assert health is not None
        assert "manager_name" in health
        assert "version" in health
        assert "metrics" in health
        assert "available_servers" in health
        assert "prd_compliance" in health

        # PRD compliance checks
        prd_compliance = health["prd_compliance"]
        assert prd_compliance["chat_only_interface"] is True
        assert prd_compliance["fallback_strategy"] is True

    def test_p0_no_external_dependencies_required(self, mcp_manager):
        """P0: Manager works without any external dependencies installed"""
        # This test ensures zero setup compliance
        # Manager should initialize and be ready to work even if no MCP servers installed
        assert mcp_manager is not None
        assert len(mcp_manager.mcp_servers) > 0  # Has server configurations

        # Should have fallback capabilities
        for server_type in [MCPServerType.JIRA, MCPServerType.GITHUB]:
            servers = mcp_manager.mcp_servers[server_type]
            for server in servers:
                assert server.fallback_api_base is not None  # Fallback available

    @pytest.mark.asyncio
    async def test_p0_concurrent_requests_handling(self, mcp_manager):
        """P0: Manager handles concurrent requests without issues"""
        # Test concurrent Jira requests
        jira_tasks = [
            mcp_manager.fetch_jira_data("sprint_metrics"),
            mcp_manager.fetch_jira_data("team_performance"),
        ]

        # Test concurrent GitHub requests
        github_tasks = [
            mcp_manager.fetch_github_data("repository_activity"),
            mcp_manager.fetch_github_data("pull_requests"),
        ]

        # Execute all concurrently
        all_tasks = jira_tasks + github_tasks
        results = await asyncio.gather(*all_tasks, return_exceptions=True)

        # All should succeed (no exceptions)
        for result in results:
            assert not isinstance(result, Exception)
            assert result.success is True

    @pytest.mark.asyncio
    async def test_p0_error_handling_never_crashes(self, mcp_manager):
        """P0: Error conditions never crash the system"""
        # Test with None parameters
        result1 = await mcp_manager.fetch_jira_data(None)
        assert result1 is not None

        # Test with empty parameters
        result2 = await mcp_manager.fetch_github_data("")
        assert result2 is not None

        # Test with malformed parameters
        result3 = await mcp_manager.fetch_jira_data("sprint_metrics", {"invalid": None})
        assert result3 is not None
        assert result3.success is True  # Graceful handling


class TestMCPIntegrationBusinessCritical:
    """Business critical tests for MCP Integration - HIGH priority"""

    @pytest.fixture
    def mcp_manager(self):
        return create_mcp_integration_manager()

    @pytest.mark.asyncio
    async def test_data_quality_consistency(self, mcp_manager):
        """Business Critical: Data quality is consistent across methods"""
        jira_result = await mcp_manager.fetch_jira_data("sprint_metrics")

        # Data should have expected structure
        assert "sprint_name" in jira_result.data or "message" in jira_result.data
        assert "source" in jira_result.data

        github_result = await mcp_manager.fetch_github_data("repository_activity")
        assert "repository" in github_result.data or "message" in github_result.data
        assert "source" in github_result.data

    @pytest.mark.asyncio
    async def test_mcp_vs_api_fallback_differentiation(self, mcp_manager):
        """Business Critical: Can differentiate between MCP and API fallback"""
        result = await mcp_manager.fetch_jira_data("sprint_metrics")

        # Should clearly indicate method used
        assert result.method in ["mcp", "api_fallback"]
        assert result.server_used is not None

        # Data source should be indicated
        if result.method == "mcp":
            assert "mcp" in result.data.get("source", "").lower()
        else:
            assert "api" in result.data.get("source", "").lower() or "fallback" in result.data.get("source", "").lower()

    def test_server_priority_ordering(self, mcp_manager):
        """Business Critical: Server priority ordering is correct"""
        for server_type in [MCPServerType.JIRA, MCPServerType.GITHUB]:
            servers = mcp_manager.mcp_servers[server_type]
            priorities = [server.priority for server in servers]

            # Should be sorted by priority (lower number = higher priority)
            assert priorities == sorted(priorities)


if __name__ == "__main__":
    # Run P0 tests only
    pytest.main([__file__ + "::TestMCPIntegrationP0", "-v"])
