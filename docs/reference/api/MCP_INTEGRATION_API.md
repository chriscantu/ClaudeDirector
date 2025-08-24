# MCP Integration API

**Model Context Protocol server management and capability invocation.**

*Part of [ClaudeDirector API Reference](../API_REFERENCE.md)*

---

## 🔧 **MCP Integration API**

### **MCP Client Manager**
```python
# .claudedirector/lib/claudedirector/mcp/client_manager.py
class MCPClientManager:
    """Manage MCP server connections and capabilities"""

    def __init__(self):
        self.clients = {}
        self.server_configs = self._load_server_configs()
        self.circuit_breakers = {}

    async def initialize_servers(self) -> Dict[str, bool]:
        """Initialize all configured MCP servers"""
        results = {}

        for server_name, config in self.server_configs.items():
            try:
                client = MCPClient(config)
                await client.connect()
                self.clients[server_name] = client
                self.circuit_breakers[server_name] = CircuitBreaker()
                results[server_name] = True
            except Exception as e:
                print(f"❌ Failed to initialize {server_name}: {e}")
                results[server_name] = False

        return results

    async def call_capability(self,
                            server: str,
                            capability: str,
                            params: dict,
                            timeout: float = 5.0) -> dict:
        """Call specific capability on MCP server with circuit breaker"""
        if server not in self.clients:
            raise ServerNotAvailableError(f"Server {server} not available")

        circuit_breaker = self.circuit_breakers[server]

        if circuit_breaker.is_open:
            raise CircuitBreakerOpenError(f"Circuit breaker open for {server}")

        try:
            async with asyncio.timeout(timeout):
                result = await self.clients[server].call_capability(capability, params)
                circuit_breaker.record_success()
                return result
        except Exception as e:
            circuit_breaker.record_failure()
            raise MCPCallError(f"Failed to call {capability} on {server}: {e}")

    def get_server_capabilities(self, server: str) -> List[str]:
        """Get available capabilities for specific server"""
        if server not in self.server_configs:
            return []

        return self.server_configs[server].get('capabilities', [])

    def health_check(self, server: str) -> bool:
        """Check health of specific MCP server"""
        if server not in self.clients:
            return False

        try:
            return self.clients[server].is_healthy()
        except Exception:
            return False
```

### **MCP Client Implementation**
```python
# .claudedirector/lib/claudedirector/mcp/mcp_client.py
class MCPClient:
    """Individual MCP server client"""

    def __init__(self, config: dict):
        self.config = config
        self.connection = None
        self.capabilities = config.get('capabilities', [])

    async def connect(self):
        """Establish connection to MCP server"""
        transport_type = self.config.get('transport', 'stdio')

        if transport_type == 'stdio':
            self.connection = await self._create_stdio_connection()
        elif transport_type == 'http':
            self.connection = await self._create_http_connection()
        else:
            raise UnsupportedTransportError(f"Transport {transport_type} not supported")

    async def call_capability(self, capability: str, params: dict) -> dict:
        """Call specific capability with parameters"""
        if capability not in self.capabilities:
            raise CapabilityNotSupportedError(f"Capability {capability} not supported")

        request = {
            'method': capability,
            'params': params,
            'id': self._generate_request_id()
        }

        response = await self.connection.send_request(request)
        return response

    def is_healthy(self) -> bool:
        """Check if connection is healthy"""
        if not self.connection:
            return False

        return self.connection.is_alive()

    async def _create_stdio_connection(self):
        """Create stdio transport connection"""
        # Implementation for stdio transport
        pass

    async def _create_http_connection(self):
        """Create HTTP transport connection"""
        # Implementation for HTTP transport
        pass
```

---

**🎯 The MCP integration provides reliable, circuit-breaker protected access to external AI capabilities.**
