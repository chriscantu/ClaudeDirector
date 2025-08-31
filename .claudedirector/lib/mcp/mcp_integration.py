"""
Strategic Python MCP Integration
Connects Strategic Python MCP Server with existing ClaudeDirector MCP infrastructure

🏗️ Martin | Platform Architecture
🤖 Berny | AI/ML Engineering
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from .strategic_python_server import StrategicPythonMCPServer, ExecutionResult

logger = logging.getLogger(__name__)


@dataclass
class MCPRequest:
    """MCP request structure for Strategic Python server"""

    capability: str
    persona: str
    code: str
    context: Dict[str, Any]
    priority: str = "normal"


@dataclass
class MCPResponse:
    """MCP response structure with transparency information"""

    success: bool
    result: Any
    transparency_disclosure: str
    execution_metrics: Dict[str, Any]
    error: Optional[str] = None


class StrategicPythonMCPIntegration:
    """
    Integration layer between Strategic Python MCP Server and ClaudeDirector MCP infrastructure

    🎯 Purpose: Bridge strategic Python execution with existing MCP coordination
    🔍 Transparency: Complete MCP disclosure and audit trail
    ⚡ Performance: <5s response time with comprehensive metrics
    """

    def __init__(self):
        self.server = StrategicPythonMCPServer()
        self.integration_metrics = {
            "requests_processed": 0,
            "successful_requests": 0,
            "avg_response_time": 0.0,
            "transparency_disclosures": 0,
        }

        logger.info("Strategic Python MCP Integration initialized")

    async def process_mcp_request(self, request: MCPRequest) -> MCPResponse:
        """
        Process MCP request through Strategic Python server

        Args:
            request: MCP request with capability, persona, code, and context

        Returns:
            MCPResponse with results and transparency information
        """
        start_time = asyncio.get_event_loop().time()

        try:
            # Update metrics
            self.integration_metrics["requests_processed"] += 1

            # Validate request
            if not self._validate_request(request):
                return MCPResponse(
                    success=False,
                    result=None,
                    transparency_disclosure="",
                    execution_metrics={},
                    error="Invalid MCP request: capability or persona not supported",
                )

            # Generate transparency disclosure
            transparency_disclosure = self.server.get_transparency_disclosure(
                request.capability, request.persona, self._summarize_code(request.code)
            )

            # Execute strategic code
            execution_result = await self.server.execute_strategic_code(
                request.code, request.persona, request.context
            )

            # Calculate response time
            response_time = asyncio.get_event_loop().time() - start_time

            # Update success metrics
            if execution_result.success:
                self.integration_metrics["successful_requests"] += 1

            # Update average response time
            total_requests = self.integration_metrics["requests_processed"]
            current_avg = self.integration_metrics["avg_response_time"]
            self.integration_metrics["avg_response_time"] = (
                current_avg * (total_requests - 1) + response_time
            ) / total_requests

            # Update transparency metrics
            self.integration_metrics["transparency_disclosures"] += 1

            # Prepare execution metrics
            execution_metrics = {
                "execution_time": execution_result.execution_time,
                "memory_usage": execution_result.memory_usage,
                "response_time": response_time,
                "code_hash": execution_result.code_hash,
                "timestamp": execution_result.timestamp,
            }

            return MCPResponse(
                success=execution_result.success,
                result=execution_result.output,
                transparency_disclosure=transparency_disclosure,
                execution_metrics=execution_metrics,
                error=execution_result.error,
            )

        except Exception as e:
            logger.error(f"MCP request processing error: {str(e)}")
            return MCPResponse(
                success=False,
                result=None,
                transparency_disclosure="",
                execution_metrics={},
                error=f"MCP integration error: {str(e)}",
            )

    def _validate_request(self, request: MCPRequest) -> bool:
        """Validate MCP request parameters"""

        # Check capability
        if request.capability not in self.server.capabilities:
            logger.warning(f"Unsupported capability: {request.capability}")
            return False

        # Check persona
        if request.persona not in self.server.persona_configs:
            logger.warning(f"Unsupported persona: {request.persona}")
            return False

        # Check code presence
        if not request.code or not request.code.strip():
            logger.warning("Empty code in MCP request")
            return False

        return True

    def _summarize_code(self, code: str) -> str:
        """Create a summary of code for transparency disclosure"""

        # Extract key operations for summary
        lines = code.strip().split("\n")

        # Look for key patterns
        operations = []

        for line in lines:
            line = line.strip()
            if line.startswith("import ") or line.startswith("from "):
                operations.append("data import")
            elif "pandas" in line or "pd." in line:
                operations.append("data analysis")
            elif "numpy" in line or "np." in line:
                operations.append("numerical computation")
            elif "plot" in line or "chart" in line:
                operations.append("visualization")
            elif "calculate" in line or "compute" in line:
                operations.append("calculation")
            elif "analyze" in line or "analysis" in line:
                operations.append("analysis")

        if operations:
            return f"{', '.join(set(operations))}"
        else:
            return f"strategic analysis ({len(lines)} lines)"

    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status and metrics"""

        server_info = self.server.get_server_info()

        return {
            "integration_version": "1.0.0",
            "server_info": server_info,
            "integration_metrics": self.integration_metrics,
            "supported_capabilities": self.server.capabilities,
            "supported_personas": list(self.server.persona_configs.keys()),
            "status": "active",
        }

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on Strategic Python MCP integration"""

        try:
            # Test basic execution
            test_request = MCPRequest(
                capability="strategic_data_analysis",
                persona="diego",
                code="result = 'Health check successful'",
                context={},
            )

            response = await self.process_mcp_request(test_request)

            return {
                "status": "healthy" if response.success else "degraded",
                "server_metrics": self.server.execution_metrics,
                "integration_metrics": self.integration_metrics,
                "last_health_check": asyncio.get_event_loop().time(),
            }

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_health_check": asyncio.get_event_loop().time(),
            }


# Integration factory function
def create_strategic_python_integration() -> StrategicPythonMCPIntegration:
    """Create and configure Strategic Python MCP Integration"""
    return StrategicPythonMCPIntegration()


# Async context manager for integration lifecycle
class StrategicPythonMCPContext:
    """Async context manager for Strategic Python MCP integration lifecycle"""

    def __init__(self):
        self.integration = None

    async def __aenter__(self) -> StrategicPythonMCPIntegration:
        self.integration = create_strategic_python_integration()

        # Perform startup health check
        health_status = await self.integration.health_check()
        logger.info(
            f"Strategic Python MCP integration startup: {health_status['status']}"
        )

        return self.integration

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.integration:
            # Log final metrics
            status = self.integration.get_integration_status()
            logger.info(
                f"Strategic Python MCP integration shutdown: {status['integration_metrics']}"
            )

        return False
