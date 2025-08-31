#!/usr/bin/env python3
"""
Simple Strategic Python MCP Server Test
Basic functionality validation without external dependencies

🏗️ Martin | Platform Architecture
"""

import asyncio
import sys
import os

# Add the lib directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from mcp.strategic_python_server import StrategicPythonMCPServer
from mcp.mcp_integration import StrategicPythonMCPIntegration, MCPRequest


async def test_basic_functionality():
    """Test basic Strategic Python MCP functionality"""
    
    print("🧪 Testing Strategic Python MCP Server...")
    
    # Initialize server
    server = StrategicPythonMCPServer()
    print(f"✅ Server initialized: {server.name} v{server.version}")
    
    # Test simple code execution (no external dependencies)
    simple_code = """
result = 2 + 2
print(f"Calculation result: {result}")
"""
    
    execution_result = await server.execute_strategic_code(
        simple_code, "diego", {"test": True}
    )
    
    print(f"✅ Simple execution: {'SUCCESS' if execution_result.success else 'FAILED'}")
    if execution_result.success:
        print(f"   Output: {execution_result.output.strip()}")
    else:
        print(f"   Error: {execution_result.error}")
    
    # Test security validation
    dangerous_code = "import os; os.system('echo dangerous')"
    
    security_result = await server.execute_strategic_code(
        dangerous_code, "diego", {}
    )
    
    print(f"✅ Security validation: {'BLOCKED' if not security_result.success else 'FAILED'}")
    
    # Test integration layer
    integration = StrategicPythonMCPIntegration()
    print(f"✅ Integration initialized with {len(integration.server.capabilities)} capabilities")
    
    # Test MCP request processing
    request = MCPRequest(
        capability="strategic_data_analysis",
        persona="diego",
        code="print('MCP integration test successful')",
        context={}
    )
    
    response = await integration.process_mcp_request(request)
    print(f"✅ MCP request processing: {'SUCCESS' if response.success else 'FAILED'}")
    
    # Test transparency disclosure
    disclosure = server.get_transparency_disclosure(
        "strategic_data_analysis",
        "diego", 
        "basic calculation"
    )
    print(f"✅ Transparency disclosure generated: {len(disclosure)} characters")
    
    # Test server info
    info = server.get_server_info()
    print(f"✅ Server info: {info['name']} with {len(info['capabilities'])} capabilities")
    
    # Health check
    health = await integration.health_check()
    print(f"✅ Health check: {health['status']}")
    
    print("\n🎉 Basic functionality tests completed!")
    print(f"📊 Server metrics: {server.execution_metrics}")
    print(f"📈 Integration metrics: {integration.integration_metrics}")


if __name__ == "__main__":
    asyncio.run(test_basic_functionality())
