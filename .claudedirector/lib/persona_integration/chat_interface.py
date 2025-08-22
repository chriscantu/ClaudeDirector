"""
Persona Chat Interface

Main interface for persona-based chat interactions with P2.1 system.
Handles natural language requests and provides conversational responses.
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from ..p2_communication.integrations.demo_data_source import DemoDataSource
from ..p2_communication.report_generation.executive_summary import (
    ExecutiveSummaryGenerator,
)
from ..p2_communication.integrations.alert_system import IntelligentAlertSystem
from ..p2_communication.interfaces.report_interface import (
    StakeholderType,
    ReportContext,
    ReportFormat,
)


class PersonaType(Enum):
    """Supported persona types for chat integration."""

    DIEGO = "diego"
    CAMILLE = "camille"
    RACHEL = "rachel"
    ALVARO = "alvaro"
    MARTIN = "martin"
    SOFIA = "sofia"
    ELENA = "elena"
    MARCUS = "marcus"
    DAVID = "david"
    SECURITY = "security"
    DATA = "data"


@dataclass
class ChatRequest:
    """Structured chat request from persona interaction."""

    persona: PersonaType
    request_type: str
    stakeholder_context: Optional[StakeholderType]
    time_period: str
    additional_context: Dict[str, Any]
    raw_message: str


@dataclass
class ChatResponse:
    """Structured response for persona chat interaction."""

    response_text: str
    data_sources: List[str]
    confidence_score: Optional[float]
    follow_up_suggestions: List[str]
    technical_details: Optional[Dict[str, Any]]


class PersonaChatInterface:
    """
    Main interface for persona-based chat interactions with P2.1 system.

    Handles natural language interpretation, P2.1 system invocation,
    and conversational response formatting.
    """

    def __init__(self):
        """Initialize chat interface with P2.1 components."""
        # Initialize data source (using demo for now)
        self.data_source = DemoDataSource()

        # Initialize P2.1 components
        self.summary_generator = ExecutiveSummaryGenerator(self.data_source)
        self.alert_system = IntelligentAlertSystem(self.data_source)

        # Persona to stakeholder mapping
        self.persona_stakeholder_map = {
            PersonaType.DIEGO: StakeholderType.VP_ENGINEERING,
            PersonaType.CAMILLE: StakeholderType.CEO,
            PersonaType.RACHEL: StakeholderType.PRODUCT_TEAM,
            PersonaType.ALVARO: StakeholderType.CEO,
            PersonaType.MARTIN: StakeholderType.VP_ENGINEERING,
            PersonaType.SOFIA: StakeholderType.VP_ENGINEERING,
            PersonaType.ELENA: StakeholderType.VP_ENGINEERING,
            PersonaType.MARCUS: StakeholderType.VP_ENGINEERING,
            PersonaType.DAVID: StakeholderType.CEO,
            PersonaType.SECURITY: StakeholderType.VP_ENGINEERING,
            PersonaType.DATA: StakeholderType.VP_ENGINEERING,
        }

        # Request pattern matching
        self.request_patterns = {
            "executive_summary": [
                r"executive summary",
                r"weekly summary",
                r"status update",
                r"how are things",
                r"team status",
                r"overview",
            ],
            "alerts": [
                r"alerts?",
                r"critical issues?",
                r"problems?",
                r"what should I know",
                r"urgent",
                r"blockers?",
            ],
            "team_health": [
                r"team health",
                r"how is the team",
                r"team performance",
                r"velocity",
            ],
            "risks": [
                r"risks?",
                r"concerns?",
                r"what worries you",
                r"potential issues",
            ],
            "initiatives": [r"initiatives?", r"projects?", r"strategic", r"roadmap"],
        }

    def handle_chat_request(self, persona_name: str, message: str) -> ChatResponse:
        """
        Handle a chat request from a persona interaction.

        Args:
            persona_name: Name of the persona (e.g., "diego", "rachel")
            message: Natural language message from user

        Returns:
            ChatResponse with conversational response
        """
        try:
            # Parse the request
            request = self._parse_chat_request(persona_name, message)

            # Route to appropriate handler
            if request.request_type == "executive_summary":
                return self._handle_executive_summary_request(request)
            elif request.request_type == "alerts":
                return self._handle_alerts_request(request)
            elif request.request_type == "team_health":
                return self._handle_team_health_request(request)
            elif request.request_type == "risks":
                return self._handle_risks_request(request)
            elif request.request_type == "initiatives":
                return self._handle_initiatives_request(request)
            else:
                return self._handle_general_request(request)

        except Exception as e:
            return ChatResponse(
                response_text=f"I apologize, but I encountered an issue processing your request: {str(e)}. Let me help you with a general status update instead.",
                data_sources=["error_handling"],
                confidence_score=0.5,
                follow_up_suggestions=[
                    "Try asking for an executive summary",
                    "Ask about current alerts",
                    "Request team health status",
                ],
                technical_details={"error": str(e)},
            )

    def _parse_chat_request(self, persona_name: str, message: str) -> ChatRequest:
        """Parse natural language message into structured request."""
        # Determine persona type
        try:
            persona = PersonaType(persona_name.lower())
        except ValueError:
            persona = PersonaType.DIEGO  # Default fallback

        # Determine request type based on message content
        request_type = "general"
        message_lower = message.lower()

        for req_type, patterns in self.request_patterns.items():
            if any(re.search(pattern, message_lower) for pattern in patterns):
                request_type = req_type
                break

        # Extract time period context
        time_period = "current_week"
        if re.search(r"today|daily", message_lower):
            time_period = "today"
        elif re.search(r"this week|weekly", message_lower):
            time_period = "current_week"
        elif re.search(r"this month|monthly", message_lower):
            time_period = "current_month"
        elif re.search(r"quarter|quarterly", message_lower):
            time_period = "current_quarter"

        # Map persona to stakeholder context
        stakeholder_context = self.persona_stakeholder_map.get(
            persona, StakeholderType.VP_ENGINEERING
        )

        return ChatRequest(
            persona=persona,
            request_type=request_type,
            stakeholder_context=stakeholder_context,
            time_period=time_period,
            additional_context={},
            raw_message=message,
        )

    def _handle_executive_summary_request(self, request: ChatRequest) -> ChatResponse:
        """Handle executive summary requests."""
        # Generate P2.1 executive summary
        context = ReportContext(
            stakeholder_type=request.stakeholder_context,
            time_period=request.time_period,
            format=ReportFormat.CLI_RICH,  # Will be converted to conversation
            include_predictions=True,
            include_risks=True,
        )

        report = self.summary_generator.generate_report(context)

        # Convert to conversational response
        response_text = self._format_executive_summary_for_conversation(
            report, request.persona
        )

        # Generate follow-up suggestions
        follow_ups = self._generate_follow_up_suggestions(
            request.persona, "executive_summary"
        )

        return ChatResponse(
            response_text=response_text,
            data_sources=report.data_sources,
            confidence_score=report.confidence_score,
            follow_up_suggestions=follow_ups,
            technical_details={"report_sections": len(report.sections)},
        )

    def _handle_alerts_request(self, request: ChatRequest) -> ChatResponse:
        """Handle alerts and critical issues requests."""
        # Get current data and generate alerts
        current_data = self.data_source.get_data(
            "current_status",
            ["team_velocity", "risk_indicators", "initiative_health", "team_health"],
        )

        # Get stakeholder-specific alerts
        alerts = self.alert_system.get_stakeholder_alerts(
            request.stakeholder_context, current_data
        )

        # Convert to conversational response
        response_text = self._format_alerts_for_conversation(alerts, request.persona)

        follow_ups = self._generate_follow_up_suggestions(request.persona, "alerts")

        return ChatResponse(
            response_text=response_text,
            data_sources=["jira", "claudedirector"],
            confidence_score=0.95 if alerts else 1.0,
            follow_up_suggestions=follow_ups,
            technical_details={"alert_count": len(alerts)},
        )

    def _handle_team_health_request(self, request: ChatRequest) -> ChatResponse:
        """Handle team health and performance requests."""
        current_data = self.data_source.get_data(
            "team_health", ["team_velocity", "team_health", "delivery_metrics"]
        )

        response_text = self._format_team_health_for_conversation(
            current_data, request.persona
        )

        follow_ups = self._generate_follow_up_suggestions(
            request.persona, "team_health"
        )

        return ChatResponse(
            response_text=response_text,
            data_sources=["jira", "claudedirector"],
            confidence_score=0.90,
            follow_up_suggestions=follow_ups,
            technical_details={"metrics_analyzed": len(current_data)},
        )

    def _handle_risks_request(self, request: ChatRequest) -> ChatResponse:
        """Handle risk and concern requests."""
        current_data = self.data_source.get_data(
            "risk_analysis",
            ["risk_indicators", "initiative_health", "cross_team_dependencies"],
        )

        response_text = self._format_risks_for_conversation(
            current_data, request.persona
        )

        follow_ups = self._generate_follow_up_suggestions(request.persona, "risks")

        return ChatResponse(
            response_text=response_text,
            data_sources=["jira", "claudedirector"],
            confidence_score=0.85,
            follow_up_suggestions=follow_ups,
            technical_details={"risk_factors_analyzed": 5},
        )

    def _handle_initiatives_request(self, request: ChatRequest) -> ChatResponse:
        """Handle strategic initiatives requests."""
        current_data = self.data_source.get_data(
            "initiatives", ["initiative_health", "strategic_alignment"]
        )

        response_text = self._format_initiatives_for_conversation(
            current_data, request.persona
        )

        follow_ups = self._generate_follow_up_suggestions(
            request.persona, "initiatives"
        )

        return ChatResponse(
            response_text=response_text,
            data_sources=["jira", "claudedirector"],
            confidence_score=0.88,
            follow_up_suggestions=follow_ups,
            technical_details={"initiatives_tracked": 11},
        )

    def _handle_general_request(self, request: ChatRequest) -> ChatResponse:
        """Handle general requests with overview."""
        # Provide a general status overview
        current_data = self.data_source.get_data(
            "overview", ["team_velocity", "risk_indicators", "initiative_health"]
        )

        response_text = self._format_general_overview_for_conversation(
            current_data, request.persona
        )

        follow_ups = [
            "Ask for a detailed executive summary",
            "Check current alerts and critical issues",
            "Review team health and performance metrics",
            "Analyze strategic initiative progress",
        ]

        return ChatResponse(
            response_text=response_text,
            data_sources=["jira", "claudedirector"],
            confidence_score=0.80,
            follow_up_suggestions=follow_ups,
            technical_details={"overview_scope": "general"},
        )

    def _format_executive_summary_for_conversation(
        self, report, persona: PersonaType
    ) -> str:
        """Convert P2.1 executive summary to conversational format."""
        lines = []

        # Persona-specific opening
        if persona == PersonaType.DIEGO:
            lines.append(
                "📊 **Executive Summary - Engineering Leadership Perspective**"
            )
        elif persona == PersonaType.CAMILLE:
            lines.append("🎯 **Strategic Technology Executive Summary**")
        elif persona == PersonaType.RACHEL:
            lines.append("🎨 **Design & UX Leadership Summary**")
        elif persona == PersonaType.ALVARO:
            lines.append("💼 **Business Value & ROI Executive Summary**")
        else:
            lines.append("📋 **Executive Summary**")

        lines.append("")

        # Extract key insights from report sections
        for section in report.sections:
            if section.title == "Executive Summary":
                lines.append("**Key Highlights:**")
                content_lines = section.content.split("\n")
                for line in content_lines:
                    if line.strip() and line.startswith("•"):
                        lines.append(f"• {line[1:].strip()}")
                lines.append("")

            elif section.title == "Risks & Opportunities":
                lines.append("**Critical Items:**")
                content_lines = section.content.split("\n")
                for line in content_lines:
                    if line.strip() and (line.startswith("⚠️") or line.startswith("✅")):
                        lines.append(f"{line.strip()}")
                lines.append("")

        # Persona-specific insights
        lines.append(self._add_persona_specific_insights(persona, report))

        # Data freshness
        lines.append(
            f"*Data as of {report.generated_at.split('T')[0]} | Confidence: {report.confidence_score:.0%}*"
        )

        return "\n".join(lines)

    def _format_alerts_for_conversation(self, alerts, persona: PersonaType) -> str:
        """Convert alerts to conversational format."""
        if not alerts:
            return f"✅ **Good news!** No critical alerts for your attention right now. All systems are operating normally and within expected parameters."

        lines = []
        lines.append(f"🚨 **Alert Summary** ({len(alerts)} items require attention)")
        lines.append("")

        # Group by severity
        critical_alerts = [a for a in alerts if a.severity.value == "critical"]
        high_alerts = [a for a in alerts if a.severity.value == "high"]
        medium_alerts = [a for a in alerts if a.severity.value == "medium"]

        if critical_alerts:
            lines.append("**🔴 Critical Issues:**")
            for alert in critical_alerts:
                lines.append(f"• **{alert.title}**: {alert.message}")
                if alert.actionable_items:
                    lines.append(f"  *Recommended action: {alert.actionable_items[0]}*")
            lines.append("")

        if high_alerts:
            lines.append("**🟡 High Priority:**")
            for alert in high_alerts:
                lines.append(f"• **{alert.title}**: {alert.message}")
            lines.append("")

        if medium_alerts and len(medium_alerts) <= 2:
            lines.append("**🟠 Medium Priority:**")
            for alert in medium_alerts:
                lines.append(f"• {alert.title}")
        elif medium_alerts:
            lines.append(
                f"**🟠 Medium Priority:** {len(medium_alerts)} additional items tracking normally"
            )

        return "\n".join(lines)

    def _format_team_health_for_conversation(self, data, persona: PersonaType) -> str:
        """Format team health data for conversation."""
        lines = []

        if persona == PersonaType.DIEGO:
            lines.append("🏗️ **Team Health - Platform Engineering Perspective**")
        elif persona == PersonaType.RACHEL:
            lines.append("🎨 **Team Health - Design & UX Perspective**")
        else:
            lines.append("💪 **Team Health Overview**")

        lines.append("")

        # Extract health metrics
        team_health = data.get("team_health", {})
        team_velocity = data.get("team_velocity", {})

        overall_score = team_health.get("overall_score", 80)
        if overall_score >= 80:
            lines.append(
                f"✅ **Overall Health: {overall_score}%** - Team performing well"
            )
        elif overall_score >= 70:
            lines.append(
                f"⚠️ **Overall Health: {overall_score}%** - Some areas need attention"
            )
        else:
            lines.append(
                f"🔴 **Overall Health: {overall_score}%** - Requires immediate focus"
            )

        lines.append("")

        # Velocity information
        current_velocity = team_velocity.get("current_sprint", 40)
        trend = team_velocity.get("trend", "stable")

        if trend == "increasing":
            lines.append(
                f"📈 **Velocity: {current_velocity} points** - Trending upward, good momentum"
            )
        elif trend == "decreasing":
            lines.append(
                f"📉 **Velocity: {current_velocity} points** - Declining, investigate blockers"
            )
        else:
            lines.append(
                f"📊 **Velocity: {current_velocity} points** - Stable and predictable"
            )

        return "\n".join(lines)

    def _format_risks_for_conversation(self, data, persona: PersonaType) -> str:
        """Format risk analysis for conversation."""
        lines = []
        lines.append("⚠️ **Risk Analysis**")
        lines.append("")

        risk_indicators = data.get("risk_indicators", {})

        # Critical risks
        blocked_issues = risk_indicators.get("blocked_issues", 0)
        critical_bugs = risk_indicators.get("critical_bugs", 0)
        security_vulns = risk_indicators.get("security_vulnerabilities", 0)

        if security_vulns > 0:
            lines.append(
                f"🔴 **Security**: {security_vulns} vulnerabilities need immediate attention"
            )

        if blocked_issues > 2:
            lines.append(
                f"🔴 **Delivery Risk**: {blocked_issues} blocked issues may impact timelines"
            )

        if critical_bugs > 1:
            lines.append(
                f"🔴 **Quality Risk**: {critical_bugs} critical bugs require escalation"
            )

        # Dependencies
        dependencies = data.get("cross_team_dependencies", {})
        total_deps = dependencies.get("total_dependencies", 0)
        blocked_deps = dependencies.get("blocked_dependencies", 0)

        if blocked_deps > 0:
            lines.append(
                f"🟡 **Dependencies**: {blocked_deps}/{total_deps} cross-team dependencies blocked"
            )

        if not any(
            [security_vulns, blocked_issues > 2, critical_bugs > 1, blocked_deps]
        ):
            lines.append(
                "✅ **Risk Status**: No significant risks identified. Operations within normal parameters."
            )

        return "\n".join(lines)

    def _format_initiatives_for_conversation(self, data, persona: PersonaType) -> str:
        """Format strategic initiatives for conversation."""
        lines = []

        if persona == PersonaType.ALVARO:
            lines.append("💼 **Strategic Initiatives - Business Value Perspective**")
        elif persona == PersonaType.CAMILLE:
            lines.append("🎯 **Strategic Technology Initiatives**")
        else:
            lines.append("🚀 **Strategic Initiative Status**")

        lines.append("")

        initiative_health = data.get("initiative_health", {})
        on_track = initiative_health.get("on_track", 0)
        at_risk = initiative_health.get("at_risk", 0)
        critical = initiative_health.get("critical", 0)

        total = on_track + at_risk + critical
        if total > 0:
            success_rate = (on_track / total) * 100
            lines.append(
                f"📊 **Success Rate: {success_rate:.0f}%** ({on_track}/{total} initiatives on track)"
            )
            lines.append("")

            if critical > 0:
                lines.append(
                    f"🔴 **Critical**: {critical} initiatives need immediate intervention"
                )
            if at_risk > 0:
                lines.append(f"🟡 **At Risk**: {at_risk} initiatives require attention")
            if on_track > 0:
                lines.append(
                    f"✅ **On Track**: {on_track} initiatives progressing well"
                )
        else:
            lines.append("📋 No tracked initiatives at this time.")

        return "\n".join(lines)

    def _format_general_overview_for_conversation(
        self, data, persona: PersonaType
    ) -> str:
        """Format general overview for conversation."""
        lines = []

        # Persona-specific greeting
        persona_greetings = {
            PersonaType.DIEGO: "👋 Hey! Here's your engineering platform overview:",
            PersonaType.CAMILLE: "🎯 Strategic technology status at a glance:",
            PersonaType.RACHEL: "🎨 Design systems and UX overview:",
            PersonaType.ALVARO: "💼 Business value and ROI snapshot:",
            PersonaType.MARTIN: "🏗️ Platform architecture status:",
        }

        greeting = persona_greetings.get(
            persona, "📊 Here's your current status overview:"
        )
        lines.append(greeting)
        lines.append("")

        # Quick health check
        team_velocity = data.get("team_velocity", {})
        risk_indicators = data.get("risk_indicators", {})

        current_velocity = team_velocity.get("current_sprint", 40)
        blocked_issues = risk_indicators.get("blocked_issues", 0)

        if blocked_issues == 0:
            lines.append("✅ **Status: Healthy** - No critical blockers")
        elif blocked_issues <= 2:
            lines.append("⚠️ **Status: Minor Issues** - Some items need attention")
        else:
            lines.append(
                "🔴 **Status: Attention Needed** - Multiple blockers identified"
            )

        lines.append(f"📈 **Current Velocity**: {current_velocity} story points")
        lines.append("")
        lines.append(
            "*Ask me for a detailed executive summary, alerts, or specific area deep-dive.*"
        )

        return "\n".join(lines)

    def _add_persona_specific_insights(self, persona: PersonaType, report) -> str:
        """Add persona-specific insights to summary."""
        if persona == PersonaType.DIEGO:
            return "**Platform Engineering Focus:** Cross-team coordination strong, infrastructure scaling on track."
        elif persona == PersonaType.RACHEL:
            return "**UX Impact:** Design system adoption maintaining consistency across product teams."
        elif persona == PersonaType.ALVARO:
            return "**Business Impact:** Platform investments showing measurable ROI through improved delivery velocity."
        elif persona == PersonaType.CAMILLE:
            return "**Strategic Technology:** Current trajectory supports competitive advantage and market positioning."
        elif persona == PersonaType.MARTIN:
            return "**Architecture Health:** Technical debt under control, platform evolution on schedule."
        else:
            return "**Overall Assessment:** Operations proceeding within expected parameters."

    def _generate_follow_up_suggestions(
        self, persona: PersonaType, request_type: str
    ) -> List[str]:
        """Generate persona-appropriate follow-up suggestions."""
        base_suggestions = {
            "executive_summary": [
                "Ask about specific team performance metrics",
                "Review current risk factors and mitigation strategies",
                "Check strategic initiative progress",
            ],
            "alerts": [
                "Request detailed executive summary",
                "Ask about team health and capacity",
                "Review upcoming deliverable timeline",
            ],
            "team_health": [
                "Analyze velocity trends over time",
                "Check for blockers and dependencies",
                "Review individual team performance",
            ],
        }

        return base_suggestions.get(
            request_type,
            [
                "Ask for an executive summary",
                "Check current alerts",
                "Review team health status",
            ],
        )
