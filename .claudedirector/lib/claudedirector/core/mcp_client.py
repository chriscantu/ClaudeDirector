"""
MCP (Model Context Protocol) Client Implementation
Handles communication with MCP servers for enhanced persona capabilities.

Author: Martin (Principal Platform Architect)
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from urllib.parse import urlparse

import aiohttp
import structlog

# Configure logging
logger = structlog.get_logger(__name__)


class MCPServerStatus(Enum):
    """MCP server connection status"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting" 
    CONNECTED = "connected"
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server"""
    name: str
    url: str
    capabilities: List[str]
    personas: List[str]
    timeout: int = 8
    max_retries: int = 3
    health_check_interval: int = 300  # 5 minutes


@dataclass
class MCPRequest:
    """MCP request structure"""
    method: str
    params: Dict[str, Any]
    id: Optional[str] = None
    timeout: Optional[int] = None


@dataclass
class MCPResponse:
    """MCP response structure"""
    id: Optional[str]
    result: Optional[Dict[str, Any]]
    error: Optional[Dict[str, Any]]
    success: bool = True
    server_name: str = ""
    response_time_ms: int = 0


@dataclass
class MCPConnection:
    """Active MCP server connection"""
    server_config: MCPServerConfig
    session: Optional[aiohttp.ClientSession] = None
    status: MCPServerStatus = MCPServerStatus.DISCONNECTED
    last_health_check: float = 0.0
    error_count: int = 0
    consecutive_failures: int = 0


class MCPConnectionPool:
    """Manages pool of MCP server connections"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections: Dict[str, MCPConnection] = {}
        self._connection_lock = asyncio.Lock()
        
    async def get_connection(self, server_config: MCPServerConfig) -> Optional[MCPConnection]:
        """Get or create connection to MCP server"""
        async with self._connection_lock:
            connection = self.connections.get(server_config.name)
            
            if connection is None:
                connection = MCPConnection(server_config=server_config)
                self.connections[server_config.name] = connection
                
            # Check if connection needs refresh
            if await self._needs_reconnection(connection):
                await self._reconnect(connection)
                
            return connection if connection.status == MCPServerStatus.CONNECTED else None
    
    async def _needs_reconnection(self, connection: MCPConnection) -> bool:
        """Check if connection needs to be refreshed"""
        if connection.status == MCPServerStatus.DISCONNECTED:
            return True
            
        if connection.status == MCPServerStatus.ERROR:
            return True
            
        # Health check interval
        time_since_check = time.time() - connection.last_health_check
        if time_since_check > connection.server_config.health_check_interval:
            return True
            
        return False
    
    async def _reconnect(self, connection: MCPConnection) -> None:
        """Reconnect to MCP server"""
        try:
            connection.status = MCPServerStatus.CONNECTING
            
            # Close existing session if any
            if connection.session and not connection.session.closed:
                await connection.session.close()
            
            # Create new session
            timeout = aiohttp.ClientTimeout(total=connection.server_config.timeout)
            connection.session = aiohttp.ClientSession(timeout=timeout)
            
            # Validate server endpoint
            async with connection.session.get(f"{connection.server_config.url}/health") as response:
                if response.status == 200:
                    connection.status = MCPServerStatus.CONNECTED
                    connection.consecutive_failures = 0
                    connection.last_health_check = time.time()
                    logger.info(
                        "mcp_server_connected",
                        server_name=connection.server_config.name,
                        url=connection.server_config.url
                    )
                else:
                    raise aiohttp.ClientError(f"Health check failed: {response.status}")
                    
        except Exception as e:
            connection.status = MCPServerStatus.ERROR
            connection.consecutive_failures += 1
            connection.error_count += 1
            logger.error(
                "mcp_server_connection_failed",
                server_name=connection.server_config.name,
                error=str(e),
                consecutive_failures=connection.consecutive_failures
            )
    
    async def close_all(self) -> None:
        """Close all connections in the pool"""
        for connection in self.connections.values():
            if connection.session and not connection.session.closed:
                await connection.session.close()
        self.connections.clear()


class MCPClient:
    """
    MCP (Model Context Protocol) Client
    
    Handles communication with MCP servers for enhanced persona capabilities.
    Provides connection pooling, error handling, and graceful degradation.
    """
    
    def __init__(self, server_configs: List[MCPServerConfig]):
        self.server_configs = {config.name: config for config in server_configs}
        self.connection_pool = MCPConnectionPool()
        self._circuit_breaker: Dict[str, Dict[str, Any]] = {}
        self._request_cache: Dict[str, MCPResponse] = {}
        self._cache_ttl = 300  # 5 minutes
        
    async def send_request(
        self, 
        server_name: str, 
        request: MCPRequest,
        use_cache: bool = True
    ) -> Optional[MCPResponse]:
        """
        Send request to MCP server with error handling and caching
        
        Args:
            server_name: Name of target MCP server
            request: MCP request to send
            use_cache: Whether to use cached responses
            
        Returns:
            MCPResponse if successful, None if failed or server unavailable
        """
        start_time = time.time()
        
        # Check circuit breaker
        if self._is_circuit_open(server_name):
            logger.debug(
                "mcp_circuit_breaker_open",
                server_name=server_name,
                method=request.method
            )
            return None
        
        # Check cache first
        if use_cache:
            cached_response = self._get_cached_response(server_name, request)
            if cached_response:
                logger.debug(
                    "mcp_cache_hit",
                    server_name=server_name,
                    method=request.method
                )
                return cached_response
        
        # Get server configuration
        server_config = self.server_configs.get(server_name)
        if not server_config:
            logger.error("mcp_server_config_not_found", server_name=server_name)
            return None
        
        # Get connection
        connection = await self.connection_pool.get_connection(server_config)
        if not connection:
            self._record_failure(server_name)
            return None
        
        try:
            # Send request
            response = await self._send_http_request(connection, request)
            response.response_time_ms = int((time.time() - start_time) * 1000)
            response.server_name = server_name
            
            # Cache successful response
            if response.success and use_cache:
                self._cache_response(server_name, request, response)
            
            # Record success
            self._record_success(server_name)
            
            logger.info(
                "mcp_request_success",
                server_name=server_name,
                method=request.method,
                response_time_ms=response.response_time_ms
            )
            
            return response
            
        except Exception as e:
            self._record_failure(server_name)
            logger.error(
                "mcp_request_failed",
                server_name=server_name,
                method=request.method,
                error=str(e),
                response_time_ms=int((time.time() - start_time) * 1000)
            )
            return None
    
    async def _send_http_request(self, connection: MCPConnection, request: MCPRequest) -> MCPResponse:
        """Send HTTP request to MCP server"""
        if not connection.session:
            raise RuntimeError("No active session for connection")
        
        # Prepare request payload
        payload = {
            "jsonrpc": "2.0",
            "method": request.method,
            "params": request.params,
            "id": request.id or f"req_{int(time.time() * 1000)}"
        }
        
        # Send request
        timeout = request.timeout or connection.server_config.timeout
        async with connection.session.post(
            f"{connection.server_config.url}/rpc",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as response:
            
            if response.status != 200:
                raise aiohttp.ClientError(f"HTTP {response.status}: {response.reason}")
            
            # Parse response
            response_data = await response.json()
            
            return MCPResponse(
                id=response_data.get("id"),
                result=response_data.get("result"),
                error=response_data.get("error"),
                success="error" not in response_data
            )
    
    def _get_cached_response(self, server_name: str, request: MCPRequest) -> Optional[MCPResponse]:
        """Get cached response if available and not expired"""
        cache_key = self._make_cache_key(server_name, request)
        cached_response = self._request_cache.get(cache_key)
        
        if cached_response:
            # Check if cache entry is still valid
            cache_age = time.time() - (cached_response.response_time_ms / 1000)
            if cache_age < self._cache_ttl:
                return cached_response
            else:
                # Remove expired entry
                del self._request_cache[cache_key]
        
        return None
    
    def _cache_response(self, server_name: str, request: MCPRequest, response: MCPResponse) -> None:
        """Cache successful response"""
        cache_key = self._make_cache_key(server_name, request)
        self._request_cache[cache_key] = response
        
        # Clean up old cache entries
        self._cleanup_cache()
    
    def _make_cache_key(self, server_name: str, request: MCPRequest) -> str:
        """Generate cache key for request"""
        params_str = json.dumps(request.params, sort_keys=True)
        return f"{server_name}:{request.method}:{hash(params_str)}"
    
    def _cleanup_cache(self) -> None:
        """Remove expired cache entries"""
        current_time = time.time()
        expired_keys = []
        
        for key, response in self._request_cache.items():
            cache_age = current_time - (response.response_time_ms / 1000)
            if cache_age >= self._cache_ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._request_cache[key]
    
    def _is_circuit_open(self, server_name: str) -> bool:
        """Check if circuit breaker is open for server"""
        breaker = self._circuit_breaker.get(server_name, {})
        
        if breaker.get("state") == "open":
            # Check if we should try to close circuit
            if time.time() - breaker.get("opened_at", 0) > 60:  # 1 minute cooldown
                self._circuit_breaker[server_name]["state"] = "half_open"
                return False
            return True
        
        return False
    
    def _record_success(self, server_name: str) -> None:
        """Record successful request for circuit breaker"""
        if server_name not in self._circuit_breaker:
            self._circuit_breaker[server_name] = {
                "failures": 0,
                "state": "closed"
            }
        
        breaker = self._circuit_breaker[server_name]
        breaker["failures"] = 0
        breaker["state"] = "closed"
    
    def _record_failure(self, server_name: str) -> None:
        """Record failed request for circuit breaker"""
        if server_name not in self._circuit_breaker:
            self._circuit_breaker[server_name] = {
                "failures": 0,
                "state": "closed"
            }
        
        breaker = self._circuit_breaker[server_name]
        breaker["failures"] += 1
        
        # Open circuit if too many failures
        if breaker["failures"] >= 5:
            breaker["state"] = "open"
            breaker["opened_at"] = time.time()
            logger.warning(
                "mcp_circuit_breaker_opened",
                server_name=server_name,
                failure_count=breaker["failures"]
            )
    
    async def get_server_capabilities(self, server_name: str) -> Optional[List[str]]:
        """Get capabilities from MCP server"""
        request = MCPRequest(
            method="capabilities",
            params={}
        )
        
        response = await self.send_request(server_name, request)
        if response and response.success:
            return response.result.get("capabilities", [])
        
        return None
    
    async def health_check(self, server_name: str) -> bool:
        """Perform health check on MCP server"""
        server_config = self.server_configs.get(server_name)
        if not server_config:
            return False
        
        try:
            connection = await self.connection_pool.get_connection(server_config)
            return connection is not None and connection.status == MCPServerStatus.CONNECTED
        except Exception:
            return False
    
    async def get_connection_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all MCP server connections"""
        status = {}
        
        for name, config in self.server_configs.items():
            connection = self.connection_pool.connections.get(name)
            breaker = self._circuit_breaker.get(name, {})
            
            status[name] = {
                "url": config.url,
                "status": connection.status.value if connection else "not_connected",
                "capabilities": config.capabilities,
                "personas": config.personas,
                "circuit_breaker_state": breaker.get("state", "closed"),
                "failure_count": breaker.get("failures", 0),
                "error_count": connection.error_count if connection else 0,
                "last_health_check": connection.last_health_check if connection else 0
            }
        
        return status
    
    async def close(self) -> None:
        """Close all connections and cleanup resources"""
        await self.connection_pool.close_all()
        self._request_cache.clear()
        self._circuit_breaker.clear()


# Utility functions for common MCP operations

async def create_mcp_client_from_config(config_path: str) -> MCPClient:
    """Create MCP client from configuration file"""
    import yaml
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        server_configs = []
        for name, server_data in config.get('servers', {}).items():
            server_config = MCPServerConfig(
                name=name,
                url=server_data['url'],
                capabilities=server_data.get('capabilities', []),
                personas=server_data.get('personas', []),
                timeout=server_data.get('timeout', 8),
                max_retries=server_data.get('max_retries', 3)
            )
            server_configs.append(server_config)
        
        return MCPClient(server_configs)
        
    except Exception as e:
        logger.error("failed_to_create_mcp_client", error=str(e), config_path=config_path)
        raise


def create_analysis_request(analysis_type: str, context: Dict[str, Any]) -> MCPRequest:
    """Create MCP request for systematic analysis"""
    return MCPRequest(
        method="analyze",
        params={
            "type": analysis_type,
            "context": context,
            "systematic": True
        }
    )


def create_framework_request(framework_type: str, domain: str, context: Dict[str, Any]) -> MCPRequest:
    """Create MCP request for framework lookup"""
    return MCPRequest(
        method="lookup_framework",
        params={
            "framework_type": framework_type,
            "domain": domain,
            "context": context
        }
    )
