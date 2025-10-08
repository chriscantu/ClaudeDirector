"""
Pytest configuration and shared fixtures for reporting unit tests.

This module provides shared test fixtures for the reporting module tests,
following the established pattern from other test directories.

🏗️ Martin | Platform Architecture - TESTING_ARCHITECTURE.md compliance
"""

import pytest
from unittest.mock import Mock
from typing import Dict, Any


@pytest.fixture
def sample_jira_issue():
    """
    Sample Jira issue for testing reporting components.

    Returns a mock JiraIssue object with common test data.
    """
    mock_issue = Mock()
    mock_issue.key = "WEB-12345"
    mock_issue.summary = "Implement Strategic Feature"
    mock_issue.status = "In Progress"
    mock_issue.priority = "High"
    mock_issue.project = "Web Platform"
    mock_issue.assignee = "test.user@company.com"
    return mock_issue


@pytest.fixture
def sample_cycle_time_data():
    """
    Sample cycle time data for testing performance analysis.

    Returns a list of cycle times in days representing realistic
    work completion patterns.
    """
    return [3.5, 5.2, 7.1, 4.8, 6.3, 2.9, 8.1, 5.5, 4.2, 6.7]


@pytest.fixture
def mcp_config():
    """
    MCP integration configuration for testing.

    Returns a configuration dictionary with MCP settings enabled,
    suitable for testing MCP-enhanced reporting features.
    """
    return {
        "enable_mcp_integration": True,
        "mcp_performance_threshold": 5.0,
        "enable_sequential_reasoning": True,
        "enable_context7_benchmarking": True,
        "fallback_strategy": "graceful",
        "executive_focus": True,
    }


@pytest.fixture
def disabled_mcp_config():
    """
    Disabled MCP configuration for fallback testing.

    Returns a configuration dictionary with MCP integration disabled,
    suitable for testing graceful degradation scenarios.
    """
    return {
        "enable_mcp_integration": False,
        "mcp_performance_threshold": 5.0,
    }


@pytest.fixture
def mock_mcp_manager():
    """
    Mock MCPIntegrationManager for testing MCP bridge.

    Returns a mock manager with common methods stubbed out,
    suitable for unit testing without real MCP dependencies.
    """
    mock = Mock()
    mock.route_query_intelligently = Mock(return_value={})
    mock._query_claude_code_mcp_server = Mock(return_value={})
    mock.is_enabled = Mock(return_value=True)
    return mock


@pytest.fixture
def mock_mcp_enhancement_result():
    """
    Mock MCPEnhancementResult for testing.

    Returns a mock enhancement result with typical test data,
    representing successful MCP processing.
    """
    mock = Mock()
    mock.reasoning_trail = ["Strategic insight 1", "Strategic insight 2"]
    mock.executive_summary = "Executive analysis complete"
    mock.risk_factors = ["Risk factor 1"]
    mock.industry_context = {"percentile": "80th"}
    mock.processing_time = 2.5
    mock.fallback_used = False
    mock.error_message = ""
    return mock
