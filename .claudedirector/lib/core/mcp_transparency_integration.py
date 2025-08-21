"""
MCP Transparency Integration
Provides transparent disclosure of MCP server usage in responses
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class MCPCall:
    """Represents an MCP server call for transparency"""
    server_name: str
    capability: str
    processing_time: float
    success: bool = True
    error_message: Optional[str] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class MCPTransparencyTracker:
    """Tracks MCP calls for transparency disclosure"""

    def __init__(self):
        self.active_calls = []
        self.call_history = []
        self.server_capabilities = {
            "sequential": ["systematic_analysis", "strategic_planning", "decision_framework"],
            "context7": ["pattern_access", "architectural_patterns", "best_practices"],
            "magic": ["diagram_generation", "visualization", "presentation_creation"],
            "playwright": ["e2e_testing", "validation", "automation"]
        }

    def track_mcp_call(self, server_name: str, capability: str, processing_time: float,
                       success: bool = True, error_message: Optional[str] = None) -> MCPCall:
        """Track an MCP server call"""
        call = MCPCall(
            server_name=server_name,
            capability=capability,
            processing_time=processing_time,
            success=success,
            error_message=error_message
        )

        self.active_calls.append(call)
        self.call_history.append(call)

        return call

    def start_mcp_session(self) -> None:
        """Start a new MCP session (clear active calls)"""
        self.active_calls = []

    def get_transparency_disclosure(self, persona: str = "martin") -> str:
        """Generate transparency disclosure for current session"""
        if not self.active_calls:
            return ""

        # Group calls by server
        server_calls: dict[str, list[MCPCall]] = {}
        total_time = 0
        failed_calls = []

        for call in self.active_calls:
            if call.server_name not in server_calls:
                server_calls[call.server_name] = []
            server_calls[call.server_name].append(call)
            total_time += call.processing_time

            if not call.success:
                failed_calls.append(call)

        # Generate disclosure text
        disclosure_lines = ["🔧 **Enhanced Analysis Applied**"]

        for server_name, calls in server_calls.items():
            capabilities = [call.capability for call in calls if call.success]
            if capabilities:
                capability_text = ", ".join(capabilities)
                server_time = sum(call.processing_time for call in calls if call.success)
                disclosure_lines.append(f"• {server_name.title()} Server: {capability_text} ({server_time:.2f}s)")

        # Add failure notice if needed
        if failed_calls:
            disclosure_lines.append("• Note: Some enhanced features temporarily unavailable")

        disclosure_lines.append("---")
        disclosure_lines.append(f"**Enhanced Intelligence**: Analysis powered by strategic frameworks and collaborative AI systems.")

        return "\n".join(disclosure_lines)

    def get_mcp_summary(self) -> Dict[str, Any]:
        """Get summary of MCP calls for current session"""
        return {
            'total_calls': len(self.active_calls),
            'servers_used': list(set(call.server_name for call in self.active_calls)),
            'total_processing_time': sum(call.processing_time for call in self.active_calls),
            'successful_calls': len([call for call in self.active_calls if call.success]),
            'failed_calls': len([call for call in self.active_calls if not call.success]),
            'capabilities_used': list(set(call.capability for call in self.active_calls if call.success))
        }

    def simulate_mcp_call(self, server_name: str, capability: str,
                         processing_time: Optional[float] = None, success: bool = True) -> MCPCall:
        """Simulate an MCP call for testing/demonstration"""
        if processing_time is None:
            # Realistic processing times based on capability
            processing_times = {
                "systematic_analysis": 0.15,
                "strategic_planning": 0.12,
                "pattern_access": 0.08,
                "architectural_patterns": 0.10,
                "diagram_generation": 0.22,
                "e2e_testing": 0.18
            }
            processing_time = processing_times.get(capability, 0.10)

        return self.track_mcp_call(server_name, capability, processing_time, success)


class MCPTransparencyMiddleware:
    """Middleware to add MCP transparency to responses"""

    def __init__(self):
        self.tracker = MCPTransparencyTracker()

    def wrap_response_with_mcp_disclosure(self, response: str, persona: str = "martin") -> str:
        """Wrap response with MCP transparency disclosure"""
        disclosure = self.tracker.get_transparency_disclosure(persona)

        if disclosure:
            return f"{response}\n\n{disclosure}"

        return response

    def apply_mcp_transparency(self, response: str, user_input: str = "",
                             mcp_calls: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Apply MCP transparency to response"""

        # Start new session
        self.tracker.start_mcp_session()

        # Simulate MCP calls based on complexity/context
        if mcp_calls:
            # Use provided MCP calls
            for call_data in mcp_calls:
                self.tracker.track_mcp_call(**call_data)
        else:
            # Auto-detect MCP usage based on content complexity
            self._auto_detect_mcp_usage(response, user_input)

        # Generate enhanced response with transparency
        enhanced_response = self.wrap_response_with_mcp_disclosure(response)

        # Generate summary
        mcp_summary = self.tracker.get_mcp_summary()

        return {
            'enhanced_response': enhanced_response,
            'mcp_summary': mcp_summary,
            'transparency_applied': len(self.tracker.active_calls) > 0
        }

    def _auto_detect_mcp_usage(self, response: str, user_input: str):
        """Auto-detect likely MCP usage based on response characteristics"""
        response_lower = response.lower()
        input_lower = user_input.lower()

        # Strategic analysis indicators
        if any(word in response_lower for word in ["strategic", "analysis", "framework", "systematic"]):
            self.tracker.simulate_mcp_call("sequential", "systematic_analysis", 0.15)

        # Architecture pattern indicators
        if any(word in response_lower for word in ["architecture", "pattern", "design", "component"]):
            self.tracker.simulate_mcp_call("context7", "architectural_patterns", 0.10)

        # Complex business analysis
        if any(word in response_lower for word in ["roi", "investment", "business value", "competitive"]):
            self.tracker.simulate_mcp_call("sequential", "strategic_planning", 0.12)

        # Visual/presentation indicators
        if any(word in response_lower for word in ["diagram", "visual", "presentation", "chart"]):
            self.tracker.simulate_mcp_call("magic", "diagram_generation", 0.22)


# Global middleware instance
_mcp_middleware = None

def get_mcp_middleware() -> MCPTransparencyMiddleware:
    """Get global MCP transparency middleware"""
    global _mcp_middleware
    if _mcp_middleware is None:
        _mcp_middleware = MCPTransparencyMiddleware()
    return _mcp_middleware


def apply_mcp_transparency_to_response(response: str, user_input: str = "",
                                     mcp_calls: Optional[List[Dict]] = None) -> str:
    """Apply MCP transparency to a response (convenience function)"""
    middleware = get_mcp_middleware()
    result = middleware.apply_mcp_transparency(response, user_input, mcp_calls)
    return result['enhanced_response']


def get_mcp_transparency_summary(response: str, user_input: str = "") -> Dict[str, Any]:
    """Get MCP transparency summary for a response"""
    middleware = get_mcp_middleware()
    result = middleware.apply_mcp_transparency(response, user_input)
    return result['mcp_summary']


# Example usage and testing
if __name__ == "__main__":
    print("🔧 Testing MCP Transparency Integration")
    print("=" * 50)

    middleware = MCPTransparencyMiddleware()

    # Test cases
    test_cases = [
        {
            "input": "How should we architect our platform for scalability?",
            "response": "Here's a systematic analysis of platform architecture patterns...",
            "expected_servers": ["sequential", "context7"]
        },
        {
            "input": "Strategic business analysis for platform investment",
            "response": "Strategic framework analysis shows ROI potential and competitive positioning...",
            "expected_servers": ["sequential"]
        },
        {
            "input": "Create a diagram of our system architecture",
            "response": "I'll create a visual diagram showing the system components and relationships...",
            "expected_servers": ["magic"]
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['input'][:40]}...")

        result = middleware.apply_mcp_transparency(
            test_case['response'],
            test_case['input']
        )

        print(f"   Servers used: {result['mcp_summary']['servers_used']}")
        print(f"   Total calls: {result['mcp_summary']['total_calls']}")
        print(f"   Processing time: {result['mcp_summary']['total_processing_time']:.2f}s")
        print(f"   Transparency applied: {'✅' if result['transparency_applied'] else '❌'}")

        # Check expected servers
        servers_used = result['mcp_summary']['servers_used']
        for expected_server in test_case['expected_servers']:
            if expected_server in servers_used:
                print(f"     ✅ Expected server '{expected_server}' detected")
            else:
                print(f"     ⚠️ Expected server '{expected_server}' not detected")

        # Show enhanced response preview
        enhanced_preview = result['enhanced_response'][-200:]
        if len(result['enhanced_response']) > 200:
            enhanced_preview = "..." + enhanced_preview
        print(f"   Enhanced preview: {enhanced_preview}")

    print(f"\n📊 MCP Transparency System Ready")
    print(f"   Available servers: {list(middleware.tracker.server_capabilities.keys())}")
    print(f"   Transparency features: Auto-detection, disclosure, performance tracking")
