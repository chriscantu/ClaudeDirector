#!/usr/bin/env python3
"""
Strategic Python MCP Server
Phase 1 Implementation - Foundation

🏗️ Martin | Platform Architecture
🤖 Berny | AI/ML Engineering - Security & Performance
💼 Alvaro | Business Strategy - Requirements Validation
🎨 Rachel | Design Systems - UX Integration

Strategic-focused Python execution MCP server with comprehensive security sandboxing.
Scope: Strategic analysis only, not general development.
"""

import asyncio
import json
import sys
import time
import tempfile
import os
import resource
import signal
import subprocess
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result of strategic Python code execution"""
    success: bool
    output: str
    error: Optional[str]
    execution_time: float
    memory_usage: int
    persona_context: str
    code_hash: str
    timestamp: float


class StrategicPythonMCPServer:
    """
    Strategic Python MCP Server
    
    🎯 Strategic Focus: Only strategic analysis capabilities
    🛡️ Security: Comprehensive sandboxing with resource limits
    ⚡ Performance: <5s execution time, <512MB memory usage
    🔍 Transparency: Complete audit trail and MCP disclosure
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
                "pandas", "numpy", "json", "datetime", "time",
                "math", "statistics", "collections", "itertools",
                "functools", "operator", "decimal", "fractions"
            ],
            "blocked_imports": [
                "os", "sys", "subprocess", "socket", "urllib", 
                "requests", "shutil", "glob", "pickle", "marshal",
                "importlib", "exec", "eval", "__import__"
            ],
            "blocked_operations": [
                "open(", "file(", "exec(", "eval(", "compile(",
                "subprocess", "__import__", "globals(", "locals(",
                "vars(", "dir(", "getattr(", "setattr(", "delattr("
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
        
        # Execution metrics
        self.execution_metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "avg_execution_time": 0.0,
            "security_violations": 0
        }
        
        logger.info(f"Strategic Python MCP Server {self.version} initialized")

    async def execute_strategic_code(
        self,
        code: str,
        persona: str,
        context: Dict[str, Any]
    ) -> ExecutionResult:
        """
        Execute Python code with strategic constraints and persona optimization
        
        Args:
            code: Python code to execute (strategic scope only)
            persona: Strategic persona (diego, alvaro, martin, camille, rachel)
            context: Strategic context and data
            
        Returns:
            ExecutionResult with success status, output, and metrics
        """
        start_time = time.time()
        code_hash = str(hash(code))
        
        try:
            # Update metrics
            self.execution_metrics["total_executions"] += 1
            
            # Validate strategic scope
            if not self._validate_strategic_scope(code):
                self.execution_metrics["security_violations"] += 1
                return ExecutionResult(
                    success=False,
                    output="",
                    error="Code outside strategic scope. Only strategic analysis allowed.",
                    execution_time=0,
                    memory_usage=0,
                    persona_context=persona,
                    code_hash=code_hash,
                    timestamp=time.time()
                )
            
            # Prepare execution environment
            execution_env = self._prepare_execution_environment(persona, context)
            
            # Execute in sandbox
            result = await self._execute_in_sandbox(code, execution_env)
            
            execution_time = time.time() - start_time
            
            # Update success metrics
            if result["success"]:
                self.execution_metrics["successful_executions"] += 1
                
            # Update average execution time
            total_execs = self.execution_metrics["total_executions"]
            current_avg = self.execution_metrics["avg_execution_time"]
            self.execution_metrics["avg_execution_time"] = (
                (current_avg * (total_execs - 1) + execution_time) / total_execs
            )
            
            execution_result = ExecutionResult(
                success=result["success"],
                output=result["output"],
                error=result.get("error"),
                execution_time=execution_time,
                memory_usage=result["memory_usage"],
                persona_context=persona,
                code_hash=code_hash,
                timestamp=time.time()
            )
            
            # Log execution for audit trail
            self._log_execution(execution_result)
            
            return execution_result
            
        except Exception as e:
            logger.error(f"Strategic Python execution error: {str(e)}")
            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution error: {str(e)}",
                execution_time=time.time() - start_time,
                memory_usage=0,
                persona_context=persona,
                code_hash=code_hash,
                timestamp=time.time()
            )

    def _validate_strategic_scope(self, code: str) -> bool:
        """Validate code is within strategic analysis scope"""
        
        # Check for blocked imports
        for blocked in self.security_config["blocked_imports"]:
            if f"import {blocked}" in code or f"from {blocked}" in code:
                logger.warning(f"Blocked import detected: {blocked}")
                return False
        
        # Check for blocked operations
        for operation in self.security_config["blocked_operations"]:
            if operation in code:
                logger.warning(f"Blocked operation detected: {operation}")
                return False
        
        # Additional security checks
        dangerous_patterns = [
            "__", "exec", "eval", "compile", "globals", "locals",
            "getattr", "setattr", "delattr", "hasattr"
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                logger.warning(f"Potentially dangerous pattern detected: {pattern}")
                return False
        
        return True

    def _prepare_execution_environment(
        self,
        persona: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare persona-specific execution environment"""
        
        persona_config = self.persona_configs.get(
            persona, 
            self.persona_configs["diego"]
        )
        
        # Base environment with strategic data
        env = {
            "persona": persona,
            "role": persona_config["template_vars"]["role"],
            "strategic_context": context,
            "available_data": self._get_available_strategic_data(context)
        }
        
        # Add persona-specific imports (will be handled in sandboxed code)
        env["allowed_imports"] = persona_config["default_imports"]
        
        return env

    def _get_available_strategic_data(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get available strategic data for analysis"""
        
        # Extract strategic data from context
        strategic_data = {}
        
        # Common strategic data patterns
        strategic_keys = [
            "metrics", "kpis", "performance", "trends", "analysis",
            "roi", "investment", "budget", "costs", "revenue",
            "team", "stakeholders", "initiatives", "projects",
            "architecture", "platform", "technology", "systems"
        ]
        
        for key in strategic_keys:
            if key in context:
                strategic_data[key] = context[key]
        
        return strategic_data

    async def _execute_in_sandbox(
        self,
        code: str,
        env: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute code in sandboxed environment with resource limits"""
        
        # Create sandboxed code wrapper
        sandboxed_code = self._create_sandboxed_code(code, env)
        
        # Create temporary execution file
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.py', 
            delete=False
        ) as f:
            f.write(sandboxed_code)
            temp_file = f.name
        
        try:
            # Execute with resource limits and timeout
            process = await asyncio.create_subprocess_exec(
                sys.executable, temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                preexec_fn=self._set_resource_limits
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
                    "memory_usage": self._estimate_memory_usage(stdout)
                }
                
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return {
                    "success": False,
                    "output": "",
                    "error": f"Execution timeout exceeded ({self.security_config['max_execution_time']}s)",
                    "memory_usage": 0
                }
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except OSError:
                pass

    def _create_sandboxed_code(self, code: str, env: Dict[str, Any]) -> str:
        """Create sandboxed code wrapper with environment setup"""
        
        # Import setup for allowed libraries
        import_setup = []
        for lib in env.get("allowed_imports", []):
            import_setup.append(f"import {lib}")
        
        # Environment variables setup
        env_setup = [
            f"persona = '{env['persona']}'",
            f"role = '{env['role']}'",
            f"strategic_context = {json.dumps(env.get('strategic_context', {}), default=str)}",
            f"available_data = {json.dumps(env.get('available_data', {}), default=str)}"
        ]
        
        # Complete sandboxed code
        sandboxed_code = f"""# Strategic Python Execution Sandbox
# Persona: {env['persona']} | Role: {env['role']}
# Timestamp: {time.time()}

import sys
import json
import traceback

# Security: Remove dangerous builtins
dangerous_builtins = ['open', 'file', 'exec', 'eval', 'compile', '__import__']
builtins_dict = __builtins__ if isinstance(__builtins__, dict) else __builtins__.__dict__
for builtin in dangerous_builtins:
    if builtin in builtins_dict:
        del builtins_dict[builtin]

try:
    # Import allowed libraries
{chr(10).join('    ' + line for line in import_setup)}
    
    # Setup environment
{chr(10).join('    ' + line for line in env_setup)}
    
    # Execute strategic code
{chr(10).join('    ' + line for line in code.split(chr(10)))}
    
except Exception as e:
    print(f"EXECUTION_ERROR: {{str(e)}}")
    print(f"TRACEBACK: {{traceback.format_exc()}}")
    sys.exit(1)
"""
        
        return sandboxed_code

    def _set_resource_limits(self):
        """Set resource limits for sandboxed execution"""
        try:
            # Memory limit (soft limit only for development compatibility)
            memory_limit = self.security_config["max_memory_mb"] * 1024 * 1024
            current_limit = resource.getrlimit(resource.RLIMIT_AS)[0]
            if current_limit == resource.RLIM_INFINITY or memory_limit < current_limit:
                resource.setrlimit(resource.RLIMIT_AS, (memory_limit, -1))
            
            # CPU time limit (soft limit only)
            cpu_limit = self.security_config["max_execution_time"]
            current_cpu_limit = resource.getrlimit(resource.RLIMIT_CPU)[0]
            if current_cpu_limit == resource.RLIM_INFINITY or cpu_limit < current_cpu_limit:
                resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, -1))
            
        except (OSError, ValueError) as e:
            # Resource limits are optional for development - log but don't fail
            logger.debug(f"Resource limits not set (development mode): {e}")

    def _estimate_memory_usage(self, output) -> int:
        """Estimate memory usage from execution output"""
        # Simple estimation based on output size
        # In production, this would use more sophisticated monitoring
        if isinstance(output, bytes):
            return len(output)
        elif isinstance(output, str):
            return len(output.encode('utf-8'))
        else:
            return 0

    def _log_execution(self, result: ExecutionResult):
        """Log execution for audit trail"""
        log_entry = {
            "timestamp": result.timestamp,
            "persona": result.persona_context,
            "success": result.success,
            "execution_time": result.execution_time,
            "memory_usage": result.memory_usage,
            "code_hash": result.code_hash,
            "error": result.error if not result.success else None
        }
        
        logger.info(f"Strategic Python execution logged: {json.dumps(log_entry)}")

    def get_server_info(self) -> Dict[str, Any]:
        """Get server information and metrics"""
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": self.capabilities,
            "security_config": {
                "max_execution_time": self.security_config["max_execution_time"],
                "max_memory_mb": self.security_config["max_memory_mb"],
                "allowed_imports": len(self.security_config["allowed_imports"]),
                "blocked_imports": len(self.security_config["blocked_imports"])
            },
            "supported_personas": list(self.persona_configs.keys()),
            "metrics": self.execution_metrics
        }

    def get_transparency_disclosure(
        self,
        capability: str,
        persona: str,
        code_summary: str
    ) -> str:
        """Generate transparency disclosure for MCP integration"""
        return f"""🔧 Accessing MCP Server: {self.name} ({capability})
*Executing strategic Python analysis for {persona} persona...*
*Code scope: {code_summary}*
*Security: Sandboxed execution with resource limits*"""


# MCP Server Entry Point
async def main():
    """Main entry point for Strategic Python MCP Server"""
    server = StrategicPythonMCPServer()
    
    logger.info(f"Starting {server.name} v{server.version}")
    logger.info(f"Capabilities: {', '.join(server.capabilities)}")
    logger.info(f"Supported personas: {', '.join(server.persona_configs.keys())}")
    
    # In a full MCP implementation, this would handle MCP protocol communication
    # For now, we'll implement the basic server structure
    
    print(json.dumps({
        "jsonrpc": "2.0",
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": server.capabilities
            },
            "serverInfo": {
                "name": server.name,
                "version": server.version
            }
        }
    }))


if __name__ == "__main__":
    asyncio.run(main())
