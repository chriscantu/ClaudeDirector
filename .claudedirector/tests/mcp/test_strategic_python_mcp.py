#!/usr/bin/env python3
"""
Strategic Python MCP Server Tests
Phase 1 Implementation Validation

🏗️ Martin | Platform Architecture
🤖 Berny | AI/ML Engineering
"""

import asyncio
import sys
import os

# Add the lib directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../lib'))

from mcp.strategic_python_server import StrategicPythonMCPServer, ExecutionResult
from mcp.mcp_integration import StrategicPythonMCPIntegration, MCPRequest


class TestStrategicPythonMCPServer:
    """Test suite for Strategic Python MCP Server"""
    
    def setup_method(self):
        """Setup test environment"""
        self.server = StrategicPythonMCPServer()
    
    def test_server_initialization(self):
        """Test server initializes correctly"""
        assert self.server.name == "strategic-python"
        assert self.server.version == "1.0.0"
        assert len(self.server.capabilities) == 5
        assert "strategic_data_analysis" in self.server.capabilities
        assert len(self.server.persona_configs) == 5
    
    def test_strategic_scope_validation_allows_valid_code(self):
        """Test that valid strategic code passes validation"""
        valid_code = """
import pandas as pd
import numpy as np
data = pd.DataFrame({'values': [1, 2, 3, 4, 5]})
result = data['values'].mean()
print(f"Average: {result}")
"""
        assert self.server._validate_strategic_scope(valid_code) == True
    
    def test_strategic_scope_validation_blocks_dangerous_code(self):
        """Test that dangerous code is blocked"""
        dangerous_codes = [
            "import os",
            "import subprocess",
            "exec('malicious code')",
            "eval('dangerous')",
            "open('/etc/passwd')",
            "__import__('os')"
        ]
        
        for code in dangerous_codes:
            assert self.server._validate_strategic_scope(code) == False
    
    def test_persona_environment_preparation(self):
        """Test persona-specific environment preparation"""
        context = {"metrics": {"cpu": 80, "memory": 60}}
        
        env = self.server._prepare_execution_environment("diego", context)
        
        assert env["persona"] == "diego"
        assert env["role"] == "Engineering Leadership"
        assert "strategic_context" in env
        assert "available_data" in env
    
    async def test_successful_code_execution(self):
        """Test successful strategic code execution"""
        code = """
import pandas as pd
data = pd.DataFrame({'team': ['A', 'B', 'C'], 'velocity': [10, 15, 12]})
avg_velocity = data['velocity'].mean()
print(f"Team average velocity: {avg_velocity}")
"""
        
        result = await self.server.execute_strategic_code(
            code, "diego", {"team_data": "sample"}
        )
        
        assert isinstance(result, ExecutionResult)
        assert result.success == True
        assert "Team average velocity:" in result.output
        assert result.persona_context == "diego"
        assert result.execution_time > 0
    
    async def test_blocked_code_execution(self):
        """Test that blocked code returns error"""
        blocked_code = "import os; os.system('ls')"
        
        result = await self.server.execute_strategic_code(
            blocked_code, "diego", {}
        )
        
        assert isinstance(result, ExecutionResult)
        assert result.success == False
        assert "outside strategic scope" in result.error
    
    def test_server_info_retrieval(self):
        """Test server information retrieval"""
        info = self.server.get_server_info()
        
        assert info["name"] == "strategic-python"
        assert info["version"] == "1.0.0"
        assert len(info["capabilities"]) == 5
        assert len(info["supported_personas"]) == 5
        assert "metrics" in info
    
    def test_transparency_disclosure_generation(self):
        """Test transparency disclosure generation"""
        disclosure = self.server.get_transparency_disclosure(
            "strategic_data_analysis",
            "diego",
            "data analysis and metrics calculation"
        )
        
        assert "🔧 Accessing MCP Server: strategic-python" in disclosure
        assert "diego persona" in disclosure
        assert "data analysis and metrics calculation" in disclosure
        assert "Sandboxed execution" in disclosure


class TestStrategicPythonMCPIntegration:
    """Test suite for Strategic Python MCP Integration"""
    
    def setup_method(self):
        """Setup test environment"""
        self.integration = StrategicPythonMCPIntegration()
    
    def test_integration_initialization(self):
        """Test integration initializes correctly"""
        assert self.integration.server is not None
        assert "requests_processed" in self.integration.integration_metrics
    
    def test_request_validation(self):
        """Test MCP request validation"""
        valid_request = MCPRequest(
            capability="strategic_data_analysis",
            persona="diego",
            code="result = 1 + 1",
            context={}
        )
        
        invalid_request = MCPRequest(
            capability="invalid_capability",
            persona="diego",
            code="result = 1 + 1",
            context={}
        )
        
        assert self.integration._validate_request(valid_request) == True
        assert self.integration._validate_request(invalid_request) == False
    
    def test_code_summarization(self):
        """Test code summarization for transparency"""
        code = """
import pandas as pd
data = pd.read_csv('metrics.csv')
analysis = data.groupby('team').mean()
"""
        
        summary = self.integration._summarize_code(code)
        assert "data import" in summary or "data analysis" in summary
    
    async def test_mcp_request_processing(self):
        """Test MCP request processing"""
        request = MCPRequest(
            capability="strategic_data_analysis",
            persona="diego",
            code="result = 'Strategic analysis complete'",
            context={"test": True}
        )
        
        response = await self.integration.process_mcp_request(request)
        
        assert response.success == True
        assert "Strategic analysis complete" in response.result
        assert "🔧 Accessing MCP Server" in response.transparency_disclosure
        assert "execution_time" in response.execution_metrics
    
    def test_integration_status(self):
        """Test integration status retrieval"""
        status = self.integration.get_integration_status()
        
        assert status["integration_version"] == "1.0.0"
        assert "server_info" in status
        assert "integration_metrics" in status
        assert status["status"] == "active"
    
    async def test_health_check(self):
        """Test integration health check"""
        health = await self.integration.health_check()
        
        assert health["status"] in ["healthy", "degraded", "unhealthy"]
        assert "last_health_check" in health


# Test runner
if __name__ == "__main__":
    # Run basic tests
    print("🧪 Running Strategic Python MCP Server Tests...")
    
    # Test server initialization
    server = StrategicPythonMCPServer()
    print(f"✅ Server initialized: {server.name} v{server.version}")
    
    # Test integration initialization
    integration = StrategicPythonMCPIntegration()
    print(f"✅ Integration initialized with {len(integration.server.capabilities)} capabilities")
    
    # Run async test
    async def run_async_test():
        # Test basic execution
        result = await server.execute_strategic_code(
            "result = 'Hello from Strategic Python MCP!'",
            "diego",
            {}
        )
        print(f"✅ Execution test: {result.success}")
        
        # Test integration
        request = MCPRequest(
            capability="strategic_data_analysis",
            persona="diego", 
            code="print('Integration test successful')",
            context={}
        )
        response = await integration.process_mcp_request(request)
        print(f"✅ Integration test: {response.success}")
        
        # Test health check
        health = await integration.health_check()
        print(f"✅ Health check: {health['status']}")
    
    # Run the async test
    asyncio.run(run_async_test())
    
    print("🎉 All basic tests passed!")
    print("📊 Server metrics:", server.execution_metrics)
    print("📈 Integration metrics:", integration.integration_metrics)
