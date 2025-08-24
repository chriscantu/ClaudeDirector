"""
MCP Transparency Middleware
Tracks and discloses MCP server usage across all ClaudeDirector personas
"""

from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
import time


@dataclass
class MCPCall:
    """Represents a single MCP server call"""

    server_name: str
    capability: str
    processing_time: float
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None


@dataclass
class MCPContext:
    """Tracks MCP context during persona response generation"""

    mcp_calls: List[MCPCall]
    total_processing_time: float
    has_failures: bool

    def __init__(self):
        self.mcp_calls = []
        self.total_processing_time = 0.0
        self.has_failures = False

    def add_mcp_call(self, call: MCPCall):
        """Add an MCP call to the context"""
        self.mcp_calls.append(call)
        self.total_processing_time += call.processing_time
        if not call.success:
            self.has_failures = True

    def has_mcp_calls(self) -> bool:
        """Check if any MCP calls were made"""
        return len(self.mcp_calls) > 0

    def get_server_names(self) -> List[str]:
        """Get list of unique server names used"""
        return list(set(call.server_name for call in self.mcp_calls))

    def get_capabilities_used(self) -> List[str]:
        """Get list of unique capabilities accessed"""
        return list(set(call.capability for call in self.mcp_calls))


class MCPTransparencyMiddleware:
    """Middleware to provide transparent disclosure of MCP server usage"""

    def __init__(self):
        self.persona_disclosure_templates = {
            "diego": "🔧 Accessing MCP Server: {server} ({capability})",
            "camille": "🔧 Consulting MCP Server: {server} for executive-level {capability}",
            "rachel": "🔧 Accessing MCP Server: {server} for design system {capability}",
            "alvaro": "🔧 Consulting MCP Server: {server} for business {capability}",
            "martin": "🔧 Accessing MCP Server: {server} for architectural {capability}",
        }

        self.processing_indicators = {
            "diego": "Analyzing your organizational challenge using systematic frameworks...",
            "camille": "Consulting executive strategy patterns for technology leadership...",
            "rachel": "Accessing design system scaling methodologies and coordination frameworks...",
            "alvaro": "Reviewing strategic business frameworks for competitive analysis...",
            "martin": "Consulting proven architectural patterns and decision methodologies...",
        }

        self.fallback_templates = {
            "diego": "The strategic analysis framework is temporarily unavailable, so I'll provide guidance based on my organizational leadership experience...",
            "camille": "The executive strategy framework is temporarily unavailable, so I'll provide guidance based on technology leadership experience...",
            "rachel": "The design system methodology framework is currently unavailable, so I'll share insights from my experience scaling design systems...",
            "alvaro": "The business strategy framework is currently unavailable, so I'll provide analysis based on competitive intelligence patterns...",
            "martin": "The architectural pattern framework is temporarily unavailable, so I'll provide guidance based on architectural principles...",
        }

    def create_enhancement_announcement(
        self, persona: str, server_calls: List[MCPCall]
    ) -> str:
        """Generate enhancement announcement for MCP server access"""
        if not server_calls:
            return ""

        # Get unique server + capability combinations
        unique_calls = {}
        for call in server_calls:
            key = f"{call.server_name}_{call.capability}"
            if key not in unique_calls:
                unique_calls[key] = call

        # Generate disclosure for each unique call
        disclosures = []
        template = self.persona_disclosure_templates.get(
            persona, self.persona_disclosure_templates["diego"]
        )

        for call in unique_calls.values():
            disclosure = template.format(
                server=call.server_name, capability=call.capability
            )
            disclosures.append(disclosure)

        if len(disclosures) > 1:
            return " + ".join(disclosures)
        else:
            return disclosures[0] if disclosures else ""

    def create_processing_indicator(self, persona: str) -> str:
        """Get processing indicator message for persona"""
        return f"*{self.processing_indicators.get(persona, self.processing_indicators['diego'])}*"

    def create_fallback_message(self, persona: str, failed_calls: List[MCPCall]) -> str:
        """Generate fallback message when MCP calls fail"""
        if not failed_calls:
            return ""

        fallback = self.fallback_templates.get(
            persona, self.fallback_templates["diego"]
        )
        return f"\n\n{fallback}"

    def wrap_persona_response(
        self, persona: str, response: str, mcp_context: MCPContext
    ) -> str:
        """Wrap persona response with MCP transparency disclosure"""
        if not mcp_context.has_mcp_calls():
            return response

        # Create enhancement announcement
        successful_calls = [call for call in mcp_context.mcp_calls if call.success]
        failed_calls = [call for call in mcp_context.mcp_calls if not call.success]

        parts = []

        # Add MCP server disclosure
        if successful_calls:
            announcement = self.create_enhancement_announcement(
                persona, successful_calls
            )
            if announcement:
                parts.append(announcement)

        # Add processing indicator
        if successful_calls:
            processing_indicator = self.create_processing_indicator(persona)
            parts.append(processing_indicator)

        # Add main response
        parts.append(response)

        # Add fallback message if there were failures
        if failed_calls:
            fallback = self.create_fallback_message(persona, failed_calls)
            if fallback:
                parts.append(fallback)

        return "\n\n".join(parts)

    def track_mcp_call(
        self,
        mcp_context: MCPContext,
        server_name: str,
        capability: str,
        processing_time: float,
        success: bool,
        error_message: Optional[str] = None,
    ):
        """Track an MCP call for transparency reporting"""
        call = MCPCall(
            server_name=server_name,
            capability=capability,
            processing_time=processing_time,
            timestamp=datetime.now(),
            success=success,
            error_message=error_message,
        )
        mcp_context.add_mcp_call(call)


class MCPCallTracker:
    """Context manager for tracking MCP calls during persona response generation"""

    def __init__(
        self,
        mcp_context: MCPContext,
        transparency_middleware: MCPTransparencyMiddleware,
    ):
        self.mcp_context = mcp_context
        self.transparency_middleware = transparency_middleware
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        time.time() - self.start_time
        exc_type is None
        str(exc_val) if exc_val else None

        # This would be called with actual server details in implementation
        # self.transparency_middleware.track_mcp_call(
        #     self.mcp_context, server_name, capability, processing_time, success, error_message
        # )

    def track_call(
        self,
        server_name: str,
        capability: str,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """Manually track an MCP call"""
        processing_time = time.time() - self.start_time if self.start_time else 0.0
        self.transparency_middleware.track_mcp_call(
            self.mcp_context,
            server_name,
            capability,
            processing_time,
            success,
            error_message,
        )
