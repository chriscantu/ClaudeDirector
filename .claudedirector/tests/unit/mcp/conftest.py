"""
MCP Component-Specific Test Fixtures

🏗️ Martin | Platform Architecture - MCP Test Support

Fixtures specific to MCP components (integration, coordination, server management).

EXTENDS: .claudedirector/tests/unit/conftest.py (root fixtures)
SCOPE: MCP component testing
"""

import pytest
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any, List


# ============================================================================
# MCP INTEGRATION FIXTURES
# ============================================================================


@pytest.fixture
def sample_mcp_config():
    """
    Sample MCP server configuration.
    """
    return {
        "servers": {
            "sequential": {
                "enabled": True,
                "command": "strategic-python-mcp",
                "args": [],
                "timeout_seconds": 30,
                "retry_attempts": 3,
            },
            "context7": {
                "enabled": True,
                "command": "context7-mcp",
                "args": ["--mode", "pattern_access"],
                "timeout_seconds": 20,
                "retry_attempts": 2,
            },
            "magic": {
                "enabled": True,
                "command": "magic-mcp",
                "args": ["--ui-generation"],
                "timeout_seconds": 25,
                "retry_attempts": 2,
            },
        },
        "default_timeout_seconds": 30,
        "enable_fallback": True,
        "enable_logging": True,
    }


@pytest.fixture
def mock_mcp_integration_manager():
    """
    Mock MCP integration manager with query routing.
    """
    mock = Mock()

    # Query classification
    mock.classify_query_pattern = Mock(return_value="STRATEGIC_ANALYSIS")

    # Server routing
    mock.route_to_server = Mock(return_value="sequential")

    # Server execution
    mock.execute_query = AsyncMock(
        return_value={
            "status": "success",
            "server": "sequential",
            "result": {
                "analysis": "Strategic analysis complete",
                "confidence": 0.88,
            },
            "execution_time_ms": 250.0,
        }
    )

    # Server availability
    mock.get_available_servers = Mock(return_value=["sequential", "context7", "magic"])
    mock.is_server_available = Mock(return_value=True)

    return mock


# ============================================================================
# MCP COORDINATOR FIXTURES
# ============================================================================


@pytest.fixture
def mock_mcp_coordinator():
    """
    Mock MCP coordinator for multi-server coordination.
    """
    mock = Mock()

    # Parallel execution
    mock.execute_parallel = AsyncMock(
        return_value={
            "results": {
                "sequential": {
                    "status": "success",
                    "data": {"analysis": "Strategic insight"},
                },
                "context7": {
                    "status": "success",
                    "data": {"patterns": ["pattern_1", "pattern_2"]},
                },
            },
            "total_time_ms": 300.0,
            "servers_used": ["sequential", "context7"],
        }
    )

    # Sequential execution
    mock.execute_sequential = AsyncMock(
        return_value={
            "stages": [
                {"server": "sequential", "status": "success", "duration_ms": 150.0},
                {"server": "context7", "status": "success", "duration_ms": 100.0},
            ],
            "total_time_ms": 250.0,
            "final_result": {"consolidated": "analysis"},
        }
    )

    # Fallback handling
    mock.execute_with_fallback = AsyncMock(
        return_value={
            "primary_server": "sequential",
            "fallback_used": False,
            "result": {"data": "success"},
        }
    )

    return mock


# ============================================================================
# MCP SERVER MOCK FIXTURES
# ============================================================================


@pytest.fixture
def mock_sequential_server():
    """
    Mock MCP Sequential Server for systematic analysis.
    """
    mock = Mock()

    # Sequential thinking analysis
    mock.analyze_systematically = AsyncMock(
        return_value={
            "analysis_stages": [
                "Problem Definition",
                "Root Cause Analysis",
                "Solution Architecture",
                "Implementation Strategy",
            ],
            "insights": [
                "Strategic challenge identified",
                "Organizational constraints mapped",
                "Solution path validated",
            ],
            "confidence_score": 0.88,
            "processing_time_ms": 180.0,
        }
    )

    return mock


@pytest.fixture
def mock_context7_server():
    """
    Mock MCP Context7 Server for pattern access.
    """
    mock = Mock()

    # Pattern retrieval
    mock.retrieve_patterns = AsyncMock(
        return_value={
            "patterns": [
                {
                    "name": "team_topologies",
                    "description": "Team Topologies organizational patterns",
                    "relevance_score": 0.92,
                },
                {
                    "name": "platform_thinking",
                    "description": "Platform-as-a-product patterns",
                    "relevance_score": 0.85,
                },
            ],
            "total_patterns": 2,
            "processing_time_ms": 120.0,
        }
    )

    # Best practices
    mock.get_best_practices = AsyncMock(
        return_value={
            "practices": [
                "Minimize cognitive load per team",
                "Clear team interaction modes",
            ],
            "framework": "team_topologies",
        }
    )

    return mock


@pytest.fixture
def mock_magic_server():
    """
    Mock MCP Magic Server for UI generation.
    """
    mock = Mock()

    # UI generation
    mock.generate_ui = AsyncMock(
        return_value={
            "component": "dashboard",
            "html": "<div>Generated UI</div>",
            "css": "/* Generated styles */",
            "generation_time_ms": 200.0,
        }
    )

    return mock


# ============================================================================
# SAMPLE MCP DATA
# ============================================================================


@pytest.fixture
def sample_mcp_query():
    """
    Sample MCP query for testing.
    """
    return {
        "query": "How should we structure our engineering organization?",
        "pattern": "STRATEGIC_ANALYSIS",
        "context": {
            "current_team_size": 50,
            "growth_target": 100,
            "time_frame": "6 months",
        },
        "preferred_servers": ["sequential", "context7"],
        "timeout_seconds": 30,
    }


@pytest.fixture
def sample_mcp_response():
    """
    Sample MCP server response for testing.
    """
    return {
        "status": "success",
        "server": "sequential",
        "query_pattern": "STRATEGIC_ANALYSIS",
        "result": {
            "analysis": "Comprehensive strategic analysis complete",
            "frameworks_recommended": ["team_topologies", "organizational_design"],
            "key_insights": [
                "Current structure shows signs of cognitive overload",
                "Platform team formation recommended",
                "Stream-aligned teams for product delivery",
            ],
            "confidence_score": 0.88,
        },
        "metadata": {
            "execution_time_ms": 250.0,
            "tokens_used": 1500,
            "cache_hit": True,
        },
    }
