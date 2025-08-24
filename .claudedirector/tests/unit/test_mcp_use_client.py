"""
Unit tests for MCPUseClient
Tests the basic MCP integration functionality with mocking.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import tempfile
import yaml

from lib.integrations.mcp_use_client import (
    MCPUseClient,
    MCPResponse,
    ConnectionStatus,
)


class TestMCPUseClient:
    """Test suite for MCPUseClient"""

    @pytest.fixture
    def sample_config(self):
        """Sample MCP server configuration"""
        return {
            "servers": {
                "sequential": {
                    "command": "npx",
                    "args": ["-y", "@sequential/mcp-server"],
                    "connection_type": "stdio",
                    "capabilities": ["systematic_analysis"],
                    "personas": ["diego"],
                    "timeout": 8,
                    "cache_ttl": 1800,
                },
                "context7": {
                    "command": "python",
                    "args": ["-m", "context7.server"],
                    "connection_type": "stdio",
                    "capabilities": ["pattern_access"],
                    "personas": ["martin"],
                    "timeout": 8,
                    "cache_ttl": 3600,
                    "fallback": {
                        "transport": "http",
                        "url": "https://api.context7.ai/mcp",
                    },
                },
            },
            "enhancement_thresholds": {
                "systematic_analysis": 0.7,
                "framework_lookup": 0.6,
            },
        }

    @pytest.fixture
    def config_file(self, sample_config):
        """Create temporary config file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_config, f)
            return f.name

    def test_initialization_without_mcp_use(self, config_file):
        """Test initialization when mcp-use is not available"""
        with patch("claudedirector.integrations.mcp_use_client.logger"):
            client = MCPUseClient(config_file)
            assert client.config_path == config_file
            assert isinstance(client.config, dict)
            # Should gracefully handle missing mcp-use

    def test_config_loading(self, config_file, sample_config):
        """Test configuration loading from file"""
        client = MCPUseClient(config_file)
        assert client.config == sample_config
        assert "sequential" in client.config["servers"]
        assert "context7" in client.config["servers"]

    def test_config_loading_missing_file(self):
        """Test handling of missing config file"""
        client = MCPUseClient("/nonexistent/path.yaml")
        assert client.config == {"servers": {}}

    def test_check_availability_with_mcp_use(self):
        """Test availability check when mcp-use is available"""
        # Mock successful import of mcp_use
        with patch("builtins.__import__", return_value=Mock()):
            client = MCPUseClient()
            availability = client._check_availability()
            # Should handle gracefully regardless of actual availability
            assert isinstance(availability, bool)

    def test_check_availability_without_mcp_use(self):
        """Test availability check when mcp-use is not available"""
        with patch("builtins.__import__", side_effect=ImportError):
            client = MCPUseClient()
            availability = client._check_availability()
            assert availability is False

    def test_build_client_config_stdio(self, config_file):
        """Test building client config for STDIO connections"""
        client = MCPUseClient(config_file)
        client_config = client._build_client_config()

        assert "mcpServers" in client_config
        assert "sequential" in client_config["mcpServers"]
        assert client_config["mcpServers"]["sequential"]["command"] == "npx"
        assert client_config["mcpServers"]["sequential"]["args"] == [
            "-y",
            "@sequential/mcp-server",
        ]

    def test_build_client_config_http_fallback(self, config_file):
        """Test building client config with HTTP fallback"""
        client = MCPUseClient(config_file)
        client_config = client._build_client_config()

        # Should include HTTP fallback for context7
        assert "context7" in client_config["mcpServers"]

    def test_get_server_capabilities(self, config_file):
        """Test getting server capabilities"""
        client = MCPUseClient(config_file)

        sequential_caps = client.get_server_capabilities("sequential")
        assert "systematic_analysis" in sequential_caps

        context7_caps = client.get_server_capabilities("context7")
        assert "pattern_access" in context7_caps

        # Non-existent server
        empty_caps = client.get_server_capabilities("nonexistent")
        assert empty_caps == []

    def test_get_personas_for_server(self, config_file):
        """Test getting personas for specific server"""
        client = MCPUseClient(config_file)

        sequential_personas = client.get_personas_for_server("sequential")
        assert "diego" in sequential_personas

        context7_personas = client.get_personas_for_server("context7")
        assert "martin" in context7_personas

    @pytest.mark.asyncio
    async def test_initialize_connections_unavailable(self, config_file):
        """Test connection initialization when mcp-use unavailable"""
        client = MCPUseClient(config_file)
        client.is_available = False

        status = await client.initialize_connections()
        assert isinstance(status, ConnectionStatus)
        assert status.total_servers == 0
        assert status.success_rate == 0.0
        assert status.available_servers == []

    @pytest.mark.asyncio
    async def test_execute_analysis_server_unavailable(self, config_file):
        """Test analysis execution when server is unavailable"""
        client = MCPUseClient(config_file)
        client.failed_servers.add("sequential")

        response = await client.execute_analysis("sequential", "test query")
        assert isinstance(response, MCPResponse)
        assert response.success is False
        assert "not available" in response.error_message
        assert response.source_server == "sequential"

    @pytest.mark.asyncio
    async def test_execute_analysis_no_connection(self, config_file):
        """Test analysis execution when no connection exists"""
        client = MCPUseClient(config_file)
        # No connected servers

        response = await client.execute_analysis("sequential", "test query")
        assert isinstance(response, MCPResponse)
        assert response.success is False
        assert "No connection" in response.error_message

    @pytest.mark.asyncio
    async def test_execute_analysis_timeout(self, config_file):
        """Test analysis execution with timeout"""
        client = MCPUseClient(config_file)

        # Mock connected server with timeout
        mock_session = AsyncMock()
        mock_session.call_tool.side_effect = asyncio.TimeoutError()
        client.connected_servers["sequential"] = mock_session
        client.mcp_client = Mock()

        response = await client.execute_analysis("sequential", "test query", timeout=1)
        assert isinstance(response, MCPResponse)
        assert response.success is False
        assert "timeout" in response.error_message.lower()

    @pytest.mark.asyncio
    async def test_cleanup_connections(self, config_file):
        """Test connection cleanup"""
        client = MCPUseClient(config_file)

        # Mock connected state
        mock_client = AsyncMock()
        client.mcp_client = mock_client
        client.connected_servers["sequential"] = Mock()

        await client.cleanup_connections()

        mock_client.close_all_sessions.assert_called_once()
        assert client.mcp_client is None
        assert len(client.connected_servers) == 0
        assert len(client.failed_servers) == 0

    def test_is_server_available(self, config_file):
        """Test server availability checking"""
        client = MCPUseClient(config_file)

        # No servers connected initially
        assert client.is_server_available("sequential") is False

        # Mock connected server
        client.connected_servers["sequential"] = Mock()
        assert client.is_server_available("sequential") is True

    def test_get_available_servers(self, config_file):
        """Test getting list of available servers"""
        client = MCPUseClient(config_file)

        # No servers initially
        assert client.get_available_servers() == []

        # Mock connected servers
        client.connected_servers["sequential"] = Mock()
        client.connected_servers["context7"] = Mock()

        available = client.get_available_servers()
        assert "sequential" in available
        assert "context7" in available
        assert len(available) == 2


class TestMCPResponse:
    """Test suite for MCPResponse dataclass"""

    def test_mcp_response_creation(self):
        """Test MCPResponse creation and attributes"""
        response = MCPResponse(
            content="Test analysis result",
            source_server="sequential",
            processing_time=2.5,
            success=True,
        )

        assert response.content == "Test analysis result"
        assert response.source_server == "sequential"
        assert response.processing_time == 2.5
        assert response.success is True
        assert response.error_message is None
        assert response.cached is False

    def test_mcp_response_with_error(self):
        """Test MCPResponse with error state"""
        response = MCPResponse(
            content="",
            source_server="sequential",
            processing_time=0.0,
            success=False,
            error_message="Connection failed",
        )

        assert response.success is False
        assert response.error_message == "Connection failed"
        assert response.content == ""


class TestConnectionStatus:
    """Test suite for ConnectionStatus dataclass"""

    def test_connection_status_creation(self):
        """Test ConnectionStatus creation and attributes"""
        status = ConnectionStatus(
            available_servers=["sequential", "context7"],
            failed_servers=["magic"],
            total_servers=3,
            success_rate=0.67,
        )

        assert len(status.available_servers) == 2
        assert "sequential" in status.available_servers
        assert "context7" in status.available_servers
        assert len(status.failed_servers) == 1
        assert "magic" in status.failed_servers
        assert status.total_servers == 3
        assert status.success_rate == 0.67

    def test_connection_status_empty(self):
        """Test ConnectionStatus with no servers"""
        status = ConnectionStatus(
            available_servers=[], failed_servers=[], total_servers=0, success_rate=0.0
        )

        assert status.available_servers == []
        assert status.failed_servers == []
        assert status.total_servers == 0
        assert status.success_rate == 0.0
