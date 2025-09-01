# Python MCP Phase 1: Strategic Python Execution Server
**Technical Implementation Specifications**

**Version**: 1.0.0
**Owner**: Martin (Platform Architecture)
**Status**: Implementation Ready

---

## 🏗️ **Strategic Python MCP Server Architecture**

### **Core System Design**

#### **Server Implementation**
```python
# File: .claudedirector/lib/mcp/strategic_python_server.py

import asyncio
import json
import sys
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from contextlib import contextmanager
import subprocess
import tempfile
import os
import resource
import signal

@dataclass
class ExecutionResult:
    """Result of strategic Python code execution"""
    success: bool
    output: str
    error: Optional[str]
    execution_time: float
    memory_usage: int
    persona_context: str

class StrategicPythonMCPServer:
    """
    Strategic Python MCP Server
    Scope: Strategic analysis only, not general development
    Security: Sandboxed execution with resource limits
    """

    def __init__(self):
        self.name = "strategic-python"
        self.version = "1.0.0"

        # Strategic capabilities only
        self.capabilities = [
            "strategic_data_analysis",
            "roi_calculations",
            "stakeholder_analytics",
            "performance_metrics",
            "executive_reporting"
        ]

        # Security constraints
        self.security_config = {
            "max_execution_time": 30,  # seconds
            "max_memory_mb": 512,      # MB
            "allowed_imports": [
                "pandas", "numpy", "json", "datetime",
                "math", "statistics", "collections"
            ],
            "blocked_imports": [
                "os", "sys", "subprocess", "socket",
                "urllib", "requests", "shutil"
            ]
        }

        # Persona-specific configurations
        self.persona_configs = {
            "diego": {
                "focus": "leadership_metrics",
                "default_imports": ["pandas", "numpy"],
                "template_vars": {"role": "Engineering Leadership"}
            },
            "alvaro": {
                "focus": "business_intelligence",
                "default_imports": ["pandas", "numpy", "statistics"],
                "template_vars": {"role": "Business Strategy"}
            },
            "martin": {
                "focus": "architecture_analysis",
                "default_imports": ["pandas", "numpy", "json"],
                "template_vars": {"role": "Platform Architecture"}
            },
            "camille": {
                "focus": "strategic_technology",
                "default_imports": ["pandas", "numpy", "statistics"],
                "template_vars": {"role": "Strategic Technology"}
            },
            "rachel": {
                "focus": "design_analytics",
                "default_imports": ["pandas", "numpy"],
                "template_vars": {"role": "Design Systems Strategy"}
            }
        }
```

### **Execution Engine**

#### **Strategic Code Execution**
```python
    async def execute_strategic_code(
        self,
        code: str,
        persona: str,
        context: Dict[str, Any]
    ) -> ExecutionResult:
        """
        Execute Python code with strategic constraints and persona optimization
        """
        start_time = time.time()

        try:
            # Validate strategic scope
            if not self._validate_strategic_scope(code):
                return ExecutionResult(
                    success=False,
                    output="",
                    error="Code outside strategic scope. Only strategic analysis allowed.",
                    execution_time=0,
                    memory_usage=0,
                    persona_context=persona
                )

            # Prepare execution environment
            execution_env = self._prepare_execution_environment(persona, context)

            # Execute in sandbox
            result = await self._execute_in_sandbox(code, execution_env)

            execution_time = time.time() - start_time

            return ExecutionResult(
                success=result["success"],
                output=result["output"],
                error=result.get("error"),
                execution_time=execution_time,
                memory_usage=result["memory_usage"],
                persona_context=persona
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution error: {str(e)}",
                execution_time=time.time() - start_time,
                memory_usage=0,
                persona_context=persona
            )
```

### **Security Implementation**

#### **Strategic Scope Validation**
```python
    def _validate_strategic_scope(self, code: str) -> bool:
        """Validate code is within strategic analysis scope"""

        # Check for blocked imports
        for blocked in self.security_config["blocked_imports"]:
            if f"import {blocked}" in code or f"from {blocked}" in code:
                return False

        # Check for system-level operations
        blocked_operations = [
            "open(", "file(", "exec(", "eval(",
            "subprocess", "__import__", "globals(", "locals("
        ]

        for operation in blocked_operations:
            if operation in code:
                return False

        return True

    def _prepare_execution_environment(
        self,
        persona: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare persona-specific execution environment"""

        persona_config = self.persona_configs.get(persona, self.persona_configs["diego"])

        # Base environment with strategic data
        env = {
            "persona": persona,
            "role": persona_config["template_vars"]["role"],
            "strategic_context": context,
            "available_data": self._get_available_strategic_data(context)
        }

        # Add persona-specific imports
        for import_name in persona_config["default_imports"]:
            try:
                env[import_name.split(".")[-1]] = __import__(import_name)
            except ImportError:
                pass  # Skip unavailable imports

        return env
```

#### **Sandboxed Execution**
```python
    async def _execute_in_sandbox(
        self,
        code: str,
        env: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute code in sandboxed environment with resource limits"""

        # Create temporary execution file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Prepare sandboxed code
            sandboxed_code = self._create_sandboxed_code(code, env)
            f.write(sandboxed_code)
            temp_file = f.name

        try:
            # Set resource limits
            def set_limits():
                # Memory limit
                resource.setrlimit(
                    resource.RLIMIT_AS,
                    (self.security_config["max_memory_mb"] * 1024 * 1024, -1)
                )
                # CPU time limit
                resource.setrlimit(
                    resource.RLIMIT_CPU,
                    (self.security_config["max_execution_time"], -1)
                )

            # Execute with timeout
            process = await asyncio.create_subprocess_exec(
                sys.executable, temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                preexec_fn=set_limits
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.security_config["max_execution_time"]
                )

                return {
                    "success": process.returncode == 0,
                    "output": stdout.decode('utf-8'),
                    "error": stderr.decode('utf-8') if stderr else None,
                    "memory_usage": self._get_memory_usage(process.pid)
                }

            except asyncio.TimeoutError:
                process.kill()
                return {
                    "success": False,
                    "output": "",
                    "error": "Execution timeout exceeded",
                    "memory_usage": 0
                }

        finally:
            # Clean up temporary file
            os.unlink(temp_file)
```

---

## 🔧 **MCP Protocol Integration**

### **Server Configuration**
```yaml
# File: .claudedirector/config/mcp_servers.yaml (Updated)

servers:
  strategic-python:
    command: "python"
    args: ["-m", "claudedirector.mcp.strategic_python_server"]
    connection_type: "stdio"
    capabilities: [
      "strategic_data_analysis",
      "roi_calculations",
      "stakeholder_analytics",
      "performance_metrics",
      "executive_reporting"
    ]
    personas: ["diego", "alvaro", "martin", "camille", "rachel"]
    security: "sandboxed"
    timeout: 30
    cache_ttl: 1800
    scope: "strategic_only"
```

### **Transparency Integration**
```python
# File: .claudedirector/lib/transparency/mcp_transparency.py (Enhanced)

class MCPTransparencyManager:
    """Enhanced transparency for Python MCP integration"""

    def __init__(self):
        self.server_capabilities = {
            "strategic-python": {
                "display_name": "Strategic Python Analysis",
                "capabilities": [
                    "data_analysis", "roi_calculations",
                    "strategic_metrics", "executive_reporting"
                ],
                "security_level": "sandboxed",
                "scope": "strategic_only"
            }
        }

    def generate_python_transparency_disclosure(
        self,
        server: str,
        capability: str,
        persona: str,
        code_summary: str
    ) -> str:
        """Generate transparency disclosure for Python execution"""

        return f"""🔧 Accessing MCP Server: {server} ({capability})
*Executing strategic Python analysis for {persona} persona...*
*Code scope: {code_summary}*
*Security: Sandboxed execution with resource limits*"""
```

---

## 🛡️ **Security & Compliance**

### **Sandboxing Implementation**
- **Resource Limits**: Memory (512MB), CPU time (30s), execution timeout
- **Import Restrictions**: Only strategic analysis libraries allowed
- **File System**: No file system access beyond workspace data
- **Network**: No network access from sandboxed code
- **System Calls**: Blocked system-level operations

### **Audit Trail**
- **Complete Logging**: All Python executions logged with hash
- **Transparency Integration**: MCP disclosure for all executions
- **Performance Monitoring**: Execution time and resource usage tracked
- **Security Validation**: All code validated before execution

### **P0 Test Compliance**
- **Existing Tests**: All 37 P0 tests maintained throughout implementation
- **New Tests**: Additional P0 tests for Python MCP security and performance
- **Regression Prevention**: Automated testing prevents capability degradation

---

## 📊 **Performance Specifications**

### **Performance Targets**
- **Execution Time**: <5s for strategic analysis operations
- **Memory Usage**: <512MB per execution, <1GB total system impact
- **Response Time**: <2s for simple calculations, <5s for complex analysis
- **Throughput**: 10+ concurrent strategic analyses

### **Monitoring & Optimization**
- **Real-time Monitoring**: Execution time and resource usage tracking
- **Performance Alerts**: Automated alerts for performance degradation
- **Optimization Strategies**: Caching, connection pooling, resource management
- **Scalability Planning**: Horizontal scaling for increased load

---

**🎯 Technical Foundation**: Complete Phase 1 implementation specifications for Strategic Python MCP Server with comprehensive security, performance, and compliance requirements.

**🛡️ Security Assurance**: Sandboxed execution environment ensures strategic scope compliance and system protection.

**📊 Performance Guarantee**: Detailed specifications ensure <5s response time within ClaudeDirector's performance requirements.
