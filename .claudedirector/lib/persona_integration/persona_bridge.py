"""
Persona Bridge

Main bridge connecting persona framework with P2.1 Executive Communication.
Handles persona-specific routing and response formatting.
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .chat_interface import PersonaChatInterface
from .conversation_formatters import ConversationFormatter


@dataclass
class PersonaRequest:
    """Structured request from persona framework."""
    persona_name: str
    user_message: str
    context: Dict[str, Any]
    timestamp: str


@dataclass
class PersonaResponse:
    """Structured response for persona framework."""
    response_text: str
    confidence_score: float
    data_sources: List[str]
    follow_up_suggestions: List[str]
    metadata: Dict[str, Any]


class PersonaP2Bridge:
    """
    Main bridge between persona framework and P2.1 system.

    Routes persona requests to appropriate P2.1 functionality and
    formats responses for natural conversation.
    """

    def __init__(self):
        """Initialize persona bridge with P2.1 components."""
        self.chat_interface = PersonaChatInterface()
        self.conversation_formatter = ConversationFormatter()

        # Persona activation keywords
        self.persona_keywords = {
            "diego": ["platform", "engineering", "cross-team", "coordination", "infrastructure"],
            "camille": ["strategic", "technology", "competitive", "advantage", "scaling"],
            "rachel": ["design", "ux", "accessibility", "user", "interface", "system"],
            "alvaro": ["business", "roi", "value", "investment", "financial", "cost"],
            "martin": ["architecture", "technical", "debt", "platform", "scalability"],
            "sofia": ["vendor", "partnership", "tools", "integration", "external"],
            "elena": ["compliance", "accessibility", "legal", "audit", "wcag"],
            "marcus": ["adoption", "onboarding", "training", "marketing", "internal"],
            "david": ["budget", "financial", "planning", "allocation", "cost"],
            "security": ["security", "vulnerabilities", "threats", "compliance"],
            "data": ["analytics", "metrics", "data", "insights", "measurement"]
        }

        # Common request patterns that trigger P2.1 functionality
        self.p2_trigger_patterns = [
            r"executive summary",
            r"status update",
            r"how are things",
            r"team health",
            r"alerts?",
            r"critical issues?",
            r"blockers?",
            r"velocity",
            r"performance",
            r"risks?",
            r"initiatives?",
            r"projects?"
        ]

    def handle_persona_request(self, persona_name: str, user_message: str, context: Optional[Dict[str, Any]] = None) -> PersonaResponse:
        """
        Handle request from persona framework.

        Args:
            persona_name: Name of the requesting persona
            user_message: User's natural language message
            context: Additional context from persona framework

        Returns:
            PersonaResponse with conversational response
        """
        try:
            # Determine if this should be routed to P2.1
            should_use_p2 = self._should_route_to_p2(user_message, persona_name)

            if should_use_p2:
                return self._handle_p2_request(persona_name, user_message, context or {})
            else:
                return self._handle_general_persona_request(persona_name, user_message, context or {})

        except Exception as e:
            return PersonaResponse(
                response_text=f"I apologize, but I encountered an issue: {str(e)}. Let me try to help with a general overview instead.",
                confidence_score=0.5,
                data_sources=["error_handling"],
                follow_up_suggestions=[
                    "Ask for an executive summary",
                    "Check current alerts",
                    "Request team health status"
                ],
                metadata={"error": str(e), "fallback": True}
            )

    def _should_route_to_p2(self, user_message: str, persona_name: str) -> bool:
        """Determine if request should be routed to P2.1 system."""
        message_lower = user_message.lower()

        # Check for explicit P2.1 trigger patterns
        for pattern in self.p2_trigger_patterns:
            if re.search(pattern, message_lower):
                return True

        # Check for persona-specific keywords that would benefit from P2.1 data
        persona_keywords = self.persona_keywords.get(persona_name.lower(), [])
        keyword_matches = sum(1 for keyword in persona_keywords if keyword in message_lower)

        # If multiple persona keywords + general status request, route to P2.1
        general_status_words = ["status", "update", "overview", "summary", "how", "what"]
        has_status_request = any(word in message_lower for word in general_status_words)

        return keyword_matches >= 2 and has_status_request

    def _handle_p2_request(self, persona_name: str, user_message: str, context: Dict[str, Any]) -> PersonaResponse:
        """Handle request that should use P2.1 functionality."""
        # Route to P2.1 chat interface
        chat_response = self.chat_interface.handle_chat_request(persona_name, user_message)

        # Convert to persona response format
        return PersonaResponse(
            response_text=chat_response.response_text,
            confidence_score=chat_response.confidence_score or 0.8,
            data_sources=chat_response.data_sources,
            follow_up_suggestions=chat_response.follow_up_suggestions,
            metadata={
                "used_p2_system": True,
                "technical_details": chat_response.technical_details,
                "persona": persona_name
            }
        )

    def _handle_general_persona_request(self, persona_name: str, user_message: str, context: Dict[str, Any]) -> PersonaResponse:
        """Handle general persona request that doesn't need P2.1."""
        # Generate persona-appropriate response without P2.1 data
        response_text = self._generate_general_persona_response(persona_name, user_message)

        return PersonaResponse(
            response_text=response_text,
            confidence_score=0.7,
            data_sources=["persona_knowledge"],
            follow_up_suggestions=self._get_general_follow_ups(persona_name),
            metadata={
                "used_p2_system": False,
                "response_type": "general_persona",
                "persona": persona_name
            }
        )

    def _generate_general_persona_response(self, persona_name: str, user_message: str) -> str:
        """Generate general response for persona without P2.1 data."""
        persona_responses = {
            "diego": "As your platform engineering partner, I'd be happy to help. For current operational data and team metrics, I can provide detailed insights on engineering performance, cross-team coordination, and platform health.",

            "camille": "From a strategic technology perspective, I can help analyze our technical positioning and competitive advantages. For real-time operational metrics, I can provide strategic insights on technology investments and organizational scaling.",

            "rachel": "As your design systems strategist, I focus on UX impact and cross-functional alignment. For current team performance and design system adoption metrics, I can provide detailed analysis of our design platform health.",

            "alvaro": "Looking at this from a business value perspective, I can help quantify ROI and strategic impact. For operational metrics and financial performance data, I can provide business-focused analysis of our technology investments.",

            "martin": "From an architectural standpoint, I can help with platform scalability and technical strategy. For current system health and technical debt metrics, I can provide detailed architectural assessments.",

            "sofia": "Regarding vendor partnerships and tool integrations, I can provide insights on our external relationships. For operational data on tool adoption and partnership effectiveness, I can analyze our vendor ecosystem health.",

            "elena": "From a compliance and accessibility perspective, I can help with WCAG requirements and audit preparation. For current accessibility metrics and compliance status, I can provide detailed compliance assessments.",

            "marcus": "For platform adoption and internal marketing, I can help with onboarding strategies and team engagement. For current adoption metrics and training effectiveness, I can provide detailed adoption analysis.",

            "david": "From a financial planning perspective, I can help with budget allocation and cost optimization. For current spending metrics and ROI analysis, I can provide detailed financial performance insights.",

            "security": "Regarding security architecture and threat management, I can help with security strategy and risk assessment. For current security metrics and vulnerability status, I can provide detailed security posture analysis.",

            "data": "For analytics strategy and metrics frameworks, I can help with data-driven decision making. For current performance metrics and data quality assessments, I can provide detailed analytics insights."
        }

        base_response = persona_responses.get(persona_name.lower(),
            "I'm here to help with strategic insights and analysis. For current operational data and performance metrics, I can provide detailed assessments of our technology and team performance.")

        return f"{base_response}\n\nWould you like me to provide current operational insights, team health data, or strategic analysis based on our latest metrics?"

    def _get_general_follow_ups(self, persona_name: str) -> List[str]:
        """Get general follow-up suggestions for persona."""
        return [
            "Ask for an executive summary with current metrics",
            "Check current alerts and critical issues",
            "Request team health and performance analysis",
            f"Get {persona_name}-specific strategic insights"
        ]

    def get_available_personas(self) -> List[Dict[str, str]]:
        """Get list of available personas with descriptions."""
        return [
            {
                "name": "diego",
                "title": "Director of Engineering, UI Foundation",
                "focus": "Platform engineering, cross-team coordination, multinational scaling",
                "capabilities": ["Executive communication", "Platform strategy", "Team coordination"]
            },
            {
                "name": "camille",
                "title": "Strategic Technology Executive",
                "focus": "Organizational scaling, technology strategy, competitive advantage",
                "capabilities": ["Strategic analysis", "Technology roadmaps", "Executive advisory"]
            },
            {
                "name": "rachel",
                "title": "Sr Director Design Systems",
                "focus": "Design systems strategy, cross-functional alignment, UX leadership",
                "capabilities": ["Design strategy", "UX analysis", "Accessibility expertise"]
            },
            {
                "name": "alvaro",
                "title": "Business Value & ROI Strategist",
                "focus": "Investment ROI, business value, stakeholder communication",
                "capabilities": ["ROI analysis", "Business impact", "Financial strategy"]
            },
            {
                "name": "martin",
                "title": "Principal Platform Architect",
                "focus": "Platform scalability, technical debt strategy, evolutionary design",
                "capabilities": ["Architecture strategy", "Technical analysis", "Platform scaling"]
            }
        ]

    def get_persona_capabilities(self, persona_name: str) -> Dict[str, Any]:
        """Get detailed capabilities for specific persona."""
        capabilities = {
            "diego": {
                "primary_focus": "Platform engineering leadership and cross-team coordination",
                "data_sources": ["JIRA", "Team metrics", "Platform health"],
                "report_types": ["Executive summaries", "Team health", "Platform status"],
                "alert_types": ["Platform issues", "Cross-team blockers", "Engineering capacity"],
                "stakeholder_perspective": "VP Engineering"
            },
            "camille": {
                "primary_focus": "Strategic technology and organizational scaling",
                "data_sources": ["Strategic metrics", "Technology roadmaps", "Competitive analysis"],
                "report_types": ["Strategic analysis", "Technology trends", "Competitive positioning"],
                "alert_types": ["Strategic risks", "Technology shifts", "Competitive threats"],
                "stakeholder_perspective": "CEO/CTO"
            },
            "rachel": {
                "primary_focus": "Design systems strategy and cross-functional design",
                "data_sources": ["Design metrics", "UX analytics", "Accessibility compliance"],
                "report_types": ["Design system health", "UX impact", "Accessibility status"],
                "alert_types": ["Design inconsistencies", "Accessibility violations", "UX degradation"],
                "stakeholder_perspective": "Product Team"
            },
            "alvaro": {
                "primary_focus": "Business value quantification and ROI analysis",
                "data_sources": ["Financial metrics", "ROI data", "Business impact"],
                "report_types": ["ROI analysis", "Business impact", "Investment returns"],
                "alert_types": ["ROI concerns", "Budget variances", "Value delivery risks"],
                "stakeholder_perspective": "CEO/CFO"
            },
            "martin": {
                "primary_focus": "Platform architecture and technical strategy",
                "data_sources": ["Technical metrics", "Architecture health", "System performance"],
                "report_types": ["Architecture analysis", "Technical debt", "Platform scaling"],
                "alert_types": ["Technical debt", "Architecture risks", "Scalability issues"],
                "stakeholder_perspective": "VP Engineering"
            }
        }

        return capabilities.get(persona_name.lower(), {
            "primary_focus": "General strategic analysis",
            "data_sources": ["Operational metrics"],
            "report_types": ["General summaries"],
            "alert_types": ["General alerts"],
            "stakeholder_perspective": "General"
        })

    def format_persona_help(self, persona_name: str) -> str:
        """Format help information for specific persona."""
        capabilities = self.get_persona_capabilities(persona_name)

        help_text = f"""
**{persona_name.title()} - AI Strategic Partner**

**Primary Focus:** {capabilities['primary_focus']}

**Available Insights:**
• Executive summaries with stakeholder-specific analysis
• Current alerts and critical issues requiring attention
• Team health and performance metrics
• Strategic analysis and recommendations

**Example Requests:**
• "Give me an executive summary"
• "What alerts should I know about?"
• "How is team health looking?"
• "Any risks I should be concerned about?"

**Data Sources:** {', '.join(capabilities['data_sources'])}
**Perspective:** {capabilities['stakeholder_perspective']}

I can provide real-time insights based on current operational data, formatted specifically for your strategic needs.
"""

        return help_text.strip()

    def quick_status_check(self, persona_name: str) -> PersonaResponse:
        """Provide quick status check for persona."""
        # Use P2.1 system for quick overview
        chat_response = self.chat_interface.handle_chat_request(persona_name, "quick status overview")

        return PersonaResponse(
            response_text=f"**Quick Status for {persona_name.title()}:**\n\n{chat_response.response_text}",
            confidence_score=chat_response.confidence_score or 0.8,
            data_sources=chat_response.data_sources,
            follow_up_suggestions=[
                "Ask for detailed executive summary",
                "Check specific alerts or risks",
                "Deep dive into team health metrics"
            ],
            metadata={
                "response_type": "quick_status",
                "persona": persona_name,
                "used_p2_system": True
            }
        )
