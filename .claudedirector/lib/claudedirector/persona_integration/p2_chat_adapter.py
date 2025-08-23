"""
P2.1 Chat Adapter

Direct integration layer for using P2.1 features through natural language.
Provides simple functions that can be called from persona framework.
"""

from typing import Dict, List, Any
from datetime import datetime

from .persona_bridge import PersonaP2Bridge
from ..p2_communication.integrations.demo_data_source import DemoDataSource
from ..p2_communication.report_generation.executive_summary import (
    ExecutiveSummaryGenerator,
)
from ..p2_communication.integrations.alert_system import IntelligentAlertSystem


class P2ChatAdapter:
    """
    Simple adapter for using P2.1 features via natural language.

    This provides the main integration points for persona framework.
    """

    def __init__(self):
        """Initialize chat adapter."""
        self.bridge = PersonaP2Bridge()

        # Direct P2.1 components for specific functionality
        self.data_source = DemoDataSource()
        self.summary_generator = ExecutiveSummaryGenerator(self.data_source)
        self.alert_system = IntelligentAlertSystem(self.data_source)

    def get_executive_summary(
        self, persona_name: str, stakeholder: str = "auto", period: str = "current_week"
    ) -> str:
        """
        Get executive summary for persona.

        Args:
            persona_name: Name of requesting persona
            stakeholder: Stakeholder type (auto-detected if "auto")
            period: Time period for summary

        Returns:
            Formatted executive summary text
        """
        # Auto-detect stakeholder if needed
        if stakeholder == "auto":
            stakeholder_map = {
                "diego": "vp_engineering",
                "camille": "ceo",
                "rachel": "product_team",
                "alvaro": "ceo",
                "martin": "vp_engineering",
            }
            stakeholder = stakeholder_map.get(persona_name.lower(), "vp_engineering")

        # Create natural language request
        request = f"Give me an executive summary for {stakeholder} covering {period}"

        # Use persona bridge
        response = self.bridge.handle_persona_request(persona_name, request)
        return response.response_text

    def get_current_alerts(self, persona_name: str, severity: str = "all") -> str:
        """
        Get current alerts for persona.

        Args:
            persona_name: Name of requesting persona
            severity: Alert severity filter

        Returns:
            Formatted alerts text
        """
        request = f"What critical alerts and issues should I know about? Focus on {severity} severity."
        response = self.bridge.handle_persona_request(persona_name, request)
        return response.response_text

    def get_team_health(self, persona_name: str) -> str:
        """
        Get team health status for persona.

        Args:
            persona_name: Name of requesting persona

        Returns:
            Formatted team health text
        """
        request = "How is team health and performance looking?"
        response = self.bridge.handle_persona_request(persona_name, request)
        return response.response_text

    def get_risk_analysis(self, persona_name: str) -> str:
        """
        Get risk analysis for persona.

        Args:
            persona_name: Name of requesting persona

        Returns:
            Formatted risk analysis text
        """
        request = "What risks and concerns should I be aware of?"
        response = self.bridge.handle_persona_request(persona_name, request)
        return response.response_text

    def get_initiative_status(self, persona_name: str) -> str:
        """
        Get strategic initiative status for persona.

        Args:
            persona_name: Name of requesting persona

        Returns:
            Formatted initiative status text
        """
        request = "What's the status of our strategic initiatives and projects?"
        response = self.bridge.handle_persona_request(persona_name, request)
        return response.response_text

    def handle_natural_request(
        self, persona_name: str, user_message: str
    ) -> Dict[str, Any]:
        """
        Handle any natural language request.

        Args:
            persona_name: Name of requesting persona
            user_message: Natural language message

        Returns:
            Dictionary with response and metadata
        """
        response = self.bridge.handle_persona_request(persona_name, user_message)

        return {
            "response": response.response_text,
            "confidence": response.confidence_score,
            "data_sources": response.data_sources,
            "suggestions": response.follow_up_suggestions,
            "metadata": response.metadata,
            "timestamp": datetime.now().isoformat(),
        }

    def get_persona_capabilities(self, persona_name: str) -> Dict[str, Any]:
        """Get capabilities for specific persona."""
        return self.bridge.get_persona_capabilities(persona_name)

    def list_available_personas(self) -> List[Dict[str, str]]:
        """Get list of available personas."""
        return self.bridge.get_available_personas()


# Global instance for easy access
p2_chat = P2ChatAdapter()


# Convenience functions for direct use
def executive_summary(persona_name: str, **kwargs) -> str:
    """Get executive summary for persona."""
    return p2_chat.get_executive_summary(persona_name, **kwargs)


def current_alerts(persona_name: str, **kwargs) -> str:
    """Get current alerts for persona."""
    return p2_chat.get_current_alerts(persona_name, **kwargs)


def team_health(persona_name: str) -> str:
    """Get team health for persona."""
    return p2_chat.get_team_health(persona_name)


def risk_analysis(persona_name: str) -> str:
    """Get risk analysis for persona."""
    return p2_chat.get_risk_analysis(persona_name)


def initiative_status(persona_name: str) -> str:
    """Get initiative status for persona."""
    return p2_chat.get_initiative_status(persona_name)


def ask_persona(persona_name: str, question: str) -> Dict[str, Any]:
    """Ask any question to a persona."""
    return p2_chat.handle_natural_request(persona_name, question)


def get_capabilities(persona_name: str) -> Dict[str, Any]:
    """Get persona capabilities."""
    return p2_chat.get_persona_capabilities(persona_name)


def list_personas() -> List[Dict[str, str]]:
    """List available personas."""
    return p2_chat.list_available_personas()


# Example usage patterns for documentation
USAGE_EXAMPLES = {
    "executive_summary": """
# Executive Summary Examples
from lib.claudedirector.persona_integration.p2_chat_adapter import executive_summary

# Get summary for Diego (platform engineering perspective)
summary = executive_summary("diego")

# Get CEO-focused summary via Camille
summary = executive_summary("camille", stakeholder="ceo", period="current_month")
""",
    "current_alerts": """
# Alerts Examples
from lib.claudedirector.persona_integration.p2_chat_adapter import current_alerts

# Get all alerts for Rachel (design perspective)
alerts = current_alerts("rachel")

# Get only critical alerts for Martin
alerts = current_alerts("martin", severity="critical")
""",
    "natural_language": """
# Natural Language Examples
from lib.claudedirector.persona_integration.p2_chat_adapter import ask_persona

# Ask Diego about platform status
response = ask_persona("diego", "How are our platform teams doing this week?")

# Ask Alvaro about business risks
response = ask_persona("alvaro", "Any ROI concerns I should know about?")

# Ask Rachel about UX health
response = ask_persona("rachel", "How is our design system adoption?")
""",
    "persona_discovery": """
# Persona Discovery
from lib.claudedirector.persona_integration.p2_chat_adapter import list_personas, get_capabilities

# See all available personas
personas = list_personas()

# Get detailed capabilities for a specific persona
caps = get_capabilities("martin")
""",
}
