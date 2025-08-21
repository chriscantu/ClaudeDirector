"""
MCP-Use Client Integration
Interface to mcp-use library for STDIO/HTTP MCP server connections with zero-setup approach.
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


@dataclass
class MCPResponse:
    """Response from MCP server execution"""
    content: str
    source_server: str
    processing_time: float
    success: bool
    error_message: Optional[str] = None
    cached: bool = False


@dataclass
class ConnectionStatus:
    """Status of MCP server connections"""
    available_servers: List[str]
    failed_servers: List[str]
    total_servers: int
    success_rate: float


class MCPUseClient:
    """Interface to mcp-use library for STDIO/HTTP MCP server connections"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize MCP client with zero-setup approach

        Args:
            config_path: Path to MCP server configuration file
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.mcp_client = None
        self.is_available = self._check_availability()
        self.connected_servers = {}
        self.failed_servers = set()

    def _get_default_config_path(self) -> str:
        """Get default configuration path"""
        return str(Path(__file__).parent.parent.parent / "config" / "mcp_servers.yaml")

    def _load_config(self) -> Dict[str, Any]:
        """Load MCP server configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"MCP config file not found: {self.config_path}")
            return {"servers": {}}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing MCP config: {e}")
            return {"servers": {}}

    def _check_availability(self) -> bool:
        """Check if mcp-use library is available"""
        try:
            logger.info("mcp-use library available")
            return True
        except ImportError:
            logger.info("mcp-use library not available - graceful degradation enabled")
            return False

    async def initialize_connections(self) -> ConnectionStatus:
        """
        Initialize MCP server connections using STDIO/HTTP

        Returns:
            ConnectionStatus with connection results
        """
        if not self.is_available:
            logger.info("MCP client not available - skipping initialization")
            return ConnectionStatus([], [], 0, 0.0)

        try:
            # Import mcp-use dynamically
            from mcp_use import MCPClient

            # Create mcp-use client configuration
            client_config = self._build_client_config()

            # Initialize mcp-use client
            self.mcp_client = MCPClient.from_dict(client_config)

            # Attempt to create all sessions
            await self.mcp_client.create_all_sessions()

            # Track connection status
            available_servers = []
            failed_servers = []

            for server_name in self.config.get("servers", {}).keys():
                try:
                    session = self.mcp_client.get_session(server_name)
                    if session:
                        available_servers.append(server_name)
                        self.connected_servers[server_name] = session
                        logger.info(f"Connected to MCP server: {server_name}")
                    else:
                        failed_servers.append(server_name)
                        self.failed_servers.add(server_name)
                        logger.warning(f"Failed to connect to MCP server: {server_name}")
                except Exception as e:
                    failed_servers.append(server_name)
                    self.failed_servers.add(server_name)
                    logger.error(f"Error connecting to {server_name}: {e}")

            total_servers = len(self.config.get("servers", {}))
            success_rate = len(available_servers) / total_servers if total_servers > 0 else 0.0

            logger.info(f"MCP connections initialized: {len(available_servers)}/{total_servers} servers available")

            return ConnectionStatus(
                available_servers=available_servers,
                failed_servers=failed_servers,
                total_servers=total_servers,
                success_rate=success_rate
            )

        except Exception as e:
            logger.error(f"Error initializing MCP connections: {e}")
            return ConnectionStatus([], [], 0, 0.0)

    def _build_client_config(self) -> Dict[str, Any]:
        """Build mcp-use client configuration from our config"""
        client_config = {"mcpServers": {}}

        for server_name, server_config in self.config.get("servers", {}).items():
            if server_config.get("connection_type") == "stdio":
                # STDIO connection configuration
                client_config["mcpServers"][server_name] = {
                    "command": server_config.get("command"),
                    "args": server_config.get("args", [])
                }
            elif server_config.get("fallback", {}).get("transport") == "http":
                # HTTP fallback configuration
                client_config["mcpServers"][server_name] = {
                    "transport": "http",
                    "url": server_config["fallback"]["url"]
                }

        return client_config

    async def execute_analysis(self, server: str, query: str, timeout: int = 8) -> MCPResponse:
        """
        Execute analysis request on specified MCP server

        Args:
            server: Name of MCP server to use
            query: Analysis query/prompt
            timeout: Request timeout in seconds

        Returns:
            MCPResponse with analysis results or error
        """
        start_time = asyncio.get_event_loop().time()

        try:
            # Check if server is available
            if server in self.failed_servers:
                return MCPResponse(
                    content="",
                    source_server=server,
                    processing_time=0.0,
                    success=False,
                    error_message=f"Server {server} is not available"
                )

            if not self.mcp_client or server not in self.connected_servers:
                return MCPResponse(
                    content="",
                    source_server=server,
                    processing_time=0.0,
                    success=False,
                    error_message=f"No connection to server {server}"
                )

            # Execute request with timeout
            session = self.connected_servers[server]

            # Use asyncio.wait_for for timeout handling
            result = await asyncio.wait_for(
                session.call_tool("analyze", {"query": query}),
                timeout=timeout
            )

            processing_time = asyncio.get_event_loop().time() - start_time

            # Extract content from result
            content = ""
            if result and hasattr(result, 'content') and result.content:
                if isinstance(result.content, list) and len(result.content) > 0:
                    content = result.content[0].text if hasattr(result.content[0], 'text') else str(result.content[0])
                else:
                    content = str(result.content)

            logger.debug(f"MCP analysis completed for {server}: {processing_time:.2f}s")

            return MCPResponse(
                content=content,
                source_server=server,
                processing_time=processing_time,
                success=True
            )

        except asyncio.TimeoutError:
            processing_time = asyncio.get_event_loop().time() - start_time
            logger.warning(f"MCP request timeout for {server}: {timeout}s")
            return MCPResponse(
                content="",
                source_server=server,
                processing_time=processing_time,
                success=False,
                error_message=f"Request timeout after {timeout}s"
            )

        except Exception as e:
            processing_time = asyncio.get_event_loop().time() - start_time
            logger.error(f"MCP request error for {server}: {e}")
            return MCPResponse(
                content="",
                source_server=server,
                processing_time=processing_time,
                success=False,
                error_message=str(e)
            )

    async def cleanup_connections(self) -> None:
        """Cleanup MCP server connections"""
        try:
            if self.mcp_client:
                await self.mcp_client.close_all_sessions()
                logger.info("MCP connections closed")
        except Exception as e:
            logger.error(f"Error cleaning up MCP connections: {e}")
        finally:
            self.mcp_client = None
            self.connected_servers.clear()
            self.failed_servers.clear()

    def get_available_servers(self) -> List[str]:
        """Get list of available MCP servers"""
        return list(self.connected_servers.keys())

    def is_server_available(self, server: str) -> bool:
        """Check if specific server is available"""
        return server in self.connected_servers

    def get_server_capabilities(self, server: str) -> List[str]:
        """Get capabilities for specific server"""
        server_config = self.config.get("servers", {}).get(server, {})
        return server_config.get("capabilities", [])

    def get_personas_for_server(self, server: str) -> List[str]:
        """Get personas that can use specific server"""
        server_config = self.config.get("servers", {}).get(server, {})
        return server_config.get("personas", [])
