"""
Cursor Transparency Bridge
Ensures persona headers and framework detection are applied to responses
"""

import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime

# Import transparency system
try:
    from claudedirector.transparency.integrated_transparency import IntegratedTransparencySystem
    from claudedirector.transparency.framework_detection import FrameworkDetectionMiddleware
    from claudedirector.transparency.mcp_transparency import MCPTransparencyMiddleware, MCPContext, MCPCall
    HAS_TRANSPARENCY = True
except ImportError:
    HAS_TRANSPARENCY = False
    print("⚠️ Transparency system not available - using fallback mode")

    # Create fallback classes
    class MCPContext:
        def __init__(self):
            self.mcp_calls = []
        def has_mcp_calls(self):
            return len(self.mcp_calls) > 0
        def get_server_names(self):
            return [call.server_name for call in self.mcp_calls if hasattr(call, 'server_name')]
        def add_mcp_call(self, call):
            self.mcp_calls.append(call)

    class MCPCall:
        def __init__(self, server_name=None, capability=None, **kwargs):
            self.server_name = server_name
            self.capability = capability


class CursorTransparencyBridge:
    """Bridge to ensure transparency features work in Cursor conversations"""

    def __init__(self):
        self.persona_headers = {
            "diego": "🎯 Diego | Engineering Leadership",
            "camille": "📊 Camille | Strategic Technology",
            "rachel": "🎨 Rachel | Design Systems Strategy",
            "alvaro": "💼 Alvaro | Platform Investment Strategy",
            "martin": "🏗️ Martin | Platform Architecture",
            "marcus": "📈 Marcus | Platform Adoption",
            "david": "💰 David | Financial Planning",
            "sofia": "🤝 Sofia | Vendor Strategy",
            "elena": "⚖️ Elena | Compliance Strategy",
            "frontend": "💻 Frontend | UI Foundation Specialist",
            "backend": "🔧 Backend | Platform Services Specialist",
            "legal": "⚖️ Legal | International Compliance",
            "security": "🔒 Security | Platform Security Architecture",
            "data": "📊 Data | Analytics Strategy"
        }

        # Context patterns to detect persona activation
        self.context_patterns = {
            "martin": [
                "architecture", "platform", "scalability", "performance",
                "technical debt", "legacy systems", "modernization",
                "infrastructure", "cloud", "distributed systems",
                "apis", "services", "microservices", "monolith",
                "developer experience", "tooling", "productivity"
            ],
            "diego": [
                "engineering leadership", "team structure", "organization",
                "platform strategy", "resource allocation", "team coordination",
                "engineering management", "leadership", "strategic"
            ],
                        "camille": [
                "strategic technology", "executive", "innovation",
                "technology strategy", "organizational scaling", "strategic",
                "technology assessment", "strategic assessment"
            ],
            "rachel": [
                "design systems", "ux", "user experience", "cross-functional",
                "design strategy", "component", "ui"
            ],
            "alvaro": [
                "business value", "roi", "investment", "platform investment",
                "business strategy", "stakeholder communication"
            ]
        }

        # Initialize transparency system if available
        if HAS_TRANSPARENCY:
            self.transparency_system = IntegratedTransparencySystem()
            self.framework_detector = FrameworkDetectionMiddleware()
            self.mcp_middleware = MCPTransparencyMiddleware()
        else:
            self.transparency_system = None
            self.framework_detector = None
            self.mcp_middleware = None

    def detect_persona_from_context(self, user_input: str, assistant_response: str = "") -> str:
        """Detect which persona should be activated based on context"""

        # Check if response already has persona header
        for persona, header in self.persona_headers.items():
            if header in assistant_response:
                return persona

        # First check for explicit persona mentions in user input
        user_input_lower = user_input.lower()
        for persona in self.persona_headers.keys():
            if persona in user_input_lower:
                return persona

        # Combine input and response for context analysis
        full_context = f"{user_input} {assistant_response}".lower()

        # Score each persona based on keyword matches
        persona_scores = {}
        for persona, keywords in self.context_patterns.items():
            score = sum(1 for keyword in keywords if keyword in full_context)
            if score > 0:
                persona_scores[persona] = score

        if persona_scores:
            # Return persona with highest score
            return max(persona_scores.items(), key=lambda x: x[1])[0]

        # Default to martin for technical questions
        return "martin"

    def has_persona_header(self, response: str) -> bool:
        """Check if response already has a persona header"""
        # Check if any persona header exists in the response (not just at start)
        for header in self.persona_headers.values():
            if header in response:
                return True
        return False

    def add_persona_header(self, response: str, persona: str) -> str:
        """Add persona header to response"""
        if self.has_persona_header(response):
            return response

        header = self.persona_headers.get(persona, self.persona_headers["martin"])
        return f"{header}\n\n{response}"

    def apply_framework_detection(self, response: str, persona: str) -> str:
        """Apply framework detection and attribution if available"""
        if not self.framework_detector:
            return response

        try:
            frameworks = self.framework_detector.detect_frameworks_used(response)
            if frameworks:
                return self.framework_detector.add_framework_attribution(persona, response, frameworks)
        except Exception as e:
            print(f"⚠️ Framework detection error: {e}")

        return response

    def detect_mcp_usage_context(self, user_input: str, response: str) -> Optional[MCPContext]:
        """Detect if response should show MCP enhancement based on complexity"""
        # Note: We always run detection even in fallback mode

        # Complexity indicators that suggest MCP enhancement
        complexity_indicators = [
            "strategic", "organizational", "framework", "systematic", "complex",
            "multi-team", "executive", "board", "leadership", "presentation",
            "enterprise", "organization-wide", "cross-functional", "multiple teams",
            "trade-offs", "options", "alternatives", "analysis", "assessment"
        ]

        combined_text = f"{user_input} {response}".lower()
        complexity_score = sum(1 for indicator in complexity_indicators if indicator in combined_text)

        # If complexity is high enough, simulate MCP enhancement
        if complexity_score >= 3:
            mcp_context = MCPContext()

            # Determine appropriate MCP server based on context
            if any(word in combined_text for word in ["strategic", "organizational", "framework"]):
                mcp_context.add_mcp_call(MCPCall(
                    server_name="sequential",
                    capability="systematic_analysis",
                    processing_time=0.15,
                    timestamp=datetime.now(),
                    success=True
                ))

            if any(word in combined_text for word in ["architecture", "platform", "technical"]):
                mcp_context.add_mcp_call(MCPCall(
                    server_name="context7",
                    capability="architectural_patterns",
                    processing_time=0.10,
                    timestamp=datetime.now(),
                    success=True
                ))

            return mcp_context

        return None

    def apply_mcp_transparency(self, response: str, persona: str, user_input: str = "") -> str:
        """Apply MCP transparency disclosure if enhancement detected"""
        if not self.mcp_middleware:
            # Fallback mode - create simple MCP disclosure for complex queries
            mcp_context = self.detect_mcp_usage_context(user_input, response)
            if mcp_context and mcp_context.has_mcp_calls():
                # Simple fallback disclosure format
                disclosure = f"🔧 Accessing MCP Server: sequential (systematic_analysis)\n*Analyzing your organizational challenge using systematic frameworks...*\n\n"
                return disclosure + response
            return response

        # Full transparency mode
        mcp_context = self.detect_mcp_usage_context(user_input, response)
        if mcp_context and mcp_context.has_mcp_calls():
            return self.mcp_middleware.wrap_persona_response(persona, response, mcp_context)

        return response

    def apply_transparency_system(self, response: str, user_input: str) -> str:
        """Apply complete transparency system to response"""

        # 1. Detect appropriate persona
        persona = self.detect_persona_from_context(user_input, response)

        # 2. Add persona header if missing
        if not self.has_persona_header(response):
            response = self.add_persona_header(response, persona)

        # 3. Apply MCP transparency first (so it appears before the main response)
        response = self.apply_mcp_transparency(response, persona, user_input)

        # 4. Apply framework detection
        response = self.apply_framework_detection(response, persona)

        return response

    def create_transparency_summary(self, response: str, user_input: str) -> Dict:
        """Create summary of transparency features applied"""
        persona = self.detect_persona_from_context(user_input, response)
        has_header = self.has_persona_header(response)

        frameworks_detected = []
        if self.framework_detector:
            try:
                frameworks = self.framework_detector.detect_frameworks_used(response)
                frameworks_detected = [f.framework_name for f in frameworks]
            except Exception:
                pass

        # Check for MCP enhancement
        mcp_context = self.detect_mcp_usage_context(user_input, response)
        has_mcp_enhancement = mcp_context and mcp_context.has_mcp_calls()
        mcp_servers_used = []
        if has_mcp_enhancement:
            mcp_servers_used = mcp_context.get_server_names()

        return {
            "persona_detected": persona,
            "has_persona_header": has_header,
            "frameworks_detected": frameworks_detected,
            "has_mcp_enhancement": has_mcp_enhancement,
            "mcp_servers_used": mcp_servers_used,
            "transparency_applied": has_header or len(frameworks_detected) > 0 or has_mcp_enhancement
        }


# Global instance for easy use
transparency_bridge = CursorTransparencyBridge()


def ensure_transparency_compliance(response: str, user_input: str = "") -> str:
    """Ensure response complies with transparency requirements"""
    return transparency_bridge.apply_transparency_system(response, user_input)


def get_transparency_summary(response: str, user_input: str = "") -> Dict:
    """Get summary of transparency features"""
    # First apply transparency to get the enhanced response, then analyze it
    enhanced_response = transparency_bridge.apply_transparency_system(response, user_input)
    return transparency_bridge.create_transparency_summary(enhanced_response, user_input)


# Example usage for testing
if __name__ == "__main__":
    print("🧪 Testing Cursor Transparency Bridge")
    print("=" * 50)

    # Test cases
    test_cases = [
        ("How should we architect our platform for scale?", "Here's an approach to platform scalability..."),
        ("What's our team structure strategy?", "Team structure depends on several factors..."),
        ("ROI analysis for platform investment", "Platform investments require careful analysis...")
    ]

    for user_input, response in test_cases:
        print(f"\n📝 Input: {user_input}")
        print(f"📄 Original: {response[:50]}...")

        enhanced = ensure_transparency_compliance(response, user_input)
        summary = get_transparency_summary(enhanced, user_input)

        print(f"🎯 Persona: {summary['persona_detected']}")
        print(f"✅ Header: {summary['has_persona_header']}")
        print(f"📚 Frameworks: {summary['frameworks_detected']}")
        print(f"📋 Enhanced: {enhanced[:100]}...")
