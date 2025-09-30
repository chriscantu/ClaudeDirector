# MCP Integration Development Guide

**Developing and integrating Model Context Protocol (MCP) servers with ClaudeDirector.**

---

## 🔧 **MCP Integration Development**

### **Basic MCP Client Implementation**
```python
# .claudedirector/lib/claudedirector/mcp/client_manager.py
import asyncio
from typing import Optional, Dict, Any

class MCPClient:
    """MCP protocol client for server communication"""

    def __init__(self):
        self.connections: Dict[str, MCPConnection] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}

    async def connect_server(self, server_config: dict) -> bool:
        """Establish connection to MCP server"""
        try:
            connection = MCPConnection(server_config)
            await connection.initialize()
            self.connections[server_config['name']] = connection
            return True
        except Exception as e:
            print(f"❌ Failed to connect to {server_config['name']}: {e}")
            return False

    async def call_capability(self, server: str, capability: str, params: dict) -> dict:
        """Call specific capability on MCP server"""
        if server not in self.connections:
            raise ConnectionError(f"Server {server} not connected")

        connection = self.connections[server]
        return await connection.call_capability(capability, params)
```

### **MCP Server Configuration**
```yaml
# .claudedirector/config/mcp_servers.yaml
servers:
  sequential:
    command: "npx"
    args: ["-y", "@sequential/mcp-server"]
    connection_type: "stdio"
    capabilities: ["systematic_analysis", "business_strategy"]
    timeout: 8

  context7:
    command: "python"
    args: ["-m", "context7.server"]
    connection_type: "stdio"
    capabilities: ["pattern_access", "methodology_lookup"]
    timeout: 8
    fallback:
      transport: "http"
      url: "https://api.context7.ai/mcp"
```

---

## 🎯 **Constitutional Development Integration**

### **Automatic MCP Activation**
When using the constitutional development process, MCP servers activate automatically:

```bash
--constitutional-development

[Your development request here]

Please follow the GitHub Spec-Kit constitutional development process:
1. Create executable specification using .claudedirector/templates/spec-template.md
2. Apply Sequential Thinking methodology (6-step process)
3. Ensure PROJECT_STRUCTURE.md and BLOAT_PREVENTION_SYSTEM.md compliance
4. Include strategic framework integration (Team Topologies, WRAP, Capital Allocation)
5. Validate constitutional compliance (max 3 projects, max 5 components)
6. Apply TDD workflow (RED-GREEN-Refactor)
7. Include P0 testing requirements
```

**🔧 Automatic Activation**: Sequential Thinking (`--think-hard`) and Context7 (`--c7`) MCP servers activate automatically when using `--constitutional-development`.

### **Manual MCP Control**
For advanced users who want explicit control:

```bash
--think-hard --c7 --constitutional-development

[Your development request here]

Please follow the GitHub Spec-Kit constitutional development process:
1. Create executable specification using .claudedirector/templates/spec-template.md
2. Apply Sequential Thinking methodology (6-step process)
3. Ensure PROJECT_STRUCTURE.md and BLOAT_PREVENTION_SYSTEM.md compliance
4. Include strategic framework integration (Team Topologies, WRAP, Capital Allocation)
5. Validate constitutional compliance (max 3 projects, max 5 components)
6. Apply TDD workflow (RED-GREEN-Refactor)
7. Include P0 testing requirements
```

**Full Guide**: [Constitutional Development Prompts](CONSTITUTIONAL_DEVELOPMENT_PROMPTS.md)

---

## 📋 **Development Guidelines**

### **MCP Server Requirements**
- **Protocol Compliance**: Follow MCP specification for communication
- **Capability Declaration**: Clearly define available capabilities
- **Error Handling**: Graceful failure and fallback mechanisms
- **Performance**: Response times under 8 seconds for strategic analysis

### **Integration Patterns**
- **Circuit Breaker**: Automatic fallback when servers unavailable
- **Health Monitoring**: Real-time status tracking
- **Load Balancing**: Distribute requests across available servers
- **Transparency Integration**: Complete audit trail for MCP usage

### **Testing Requirements**
- **Unit Tests**: Individual MCP client functionality
- **Integration Tests**: End-to-end server communication
- **Performance Tests**: Response time and throughput validation
- **Fallback Tests**: Graceful degradation when servers fail

---

*Part of the [ClaudeDirector Development Guide](../DEVELOPMENT_GUIDE.md) suite.*
