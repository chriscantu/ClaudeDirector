"""
Conversation Formatters

Specialized formatters for converting P2.1 data into natural conversation responses.
Optimized for different persona types and stakeholder contexts.
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime

from ..p2_communication.interfaces.report_interface import GeneratedReport


class ConversationTone(Enum):
    """Conversation tone options for different contexts."""

    EXECUTIVE = "executive"  # Formal, strategic, high-level
    COLLABORATIVE = "collaborative"  # Friendly, team-focused, detailed
    TECHNICAL = "technical"  # Precise, architecture-focused, detailed
    STRATEGIC = "strategic"  # Long-term, business-focused, analytical


class ConversationFormatter:
    """
    Formats P2.1 data for natural conversation responses.

    Adapts tone, detail level, and focus based on persona and context.
    """

    def __init__(self):
        """Initialize conversation formatter."""
        self.tone_templates = self._initialize_tone_templates()
        self.persona_tone_mapping = self._initialize_persona_tones()

    def format_executive_summary_response(
        self, report: GeneratedReport, persona_name: str
    ) -> str:
        """
        Format executive summary for conversational response.

        Args:
            report: Generated P2.1 report
            persona_name: Persona requesting the summary

        Returns:
            Natural language conversation response
        """
        tone = self._get_persona_tone(persona_name)

        # Start with persona-appropriate greeting
        response_parts = []
        response_parts.append(self._get_summary_greeting(persona_name, tone))
        response_parts.append("")

        # Extract and format key insights
        key_insights = self._extract_key_insights(report)
        response_parts.extend(
            self._format_insights_for_conversation(key_insights, tone)
        )

        # Add persona-specific analysis
        persona_analysis = self._generate_persona_specific_analysis(
            report, persona_name
        )
        if persona_analysis:
            response_parts.append("")
            response_parts.append(persona_analysis)

        # Add confidence and data context
        response_parts.append("")
        response_parts.append(self._format_confidence_statement(report, tone))

        return "\n".join(response_parts)

    def format_alerts_response(self, alerts: List, persona_name: str) -> str:
        """Format alerts for conversational response."""
        tone = self._get_persona_tone(persona_name)

        if not alerts:
            return self._format_no_alerts_response(persona_name, tone)

        response_parts = []
        response_parts.append(
            self._get_alerts_greeting(len(alerts), persona_name, tone)
        )
        response_parts.append("")

        # Categorize alerts by severity
        critical_alerts = [a for a in alerts if a.severity.value == "critical"]
        high_alerts = [a for a in alerts if a.severity.value == "high"]
        medium_alerts = [a for a in alerts if a.severity.value == "medium"]

        # Format critical alerts with urgency
        if critical_alerts:
            response_parts.extend(self._format_critical_alerts(critical_alerts, tone))
            response_parts.append("")

        # Format high priority alerts
        if high_alerts:
            response_parts.extend(self._format_high_priority_alerts(high_alerts, tone))
            response_parts.append("")

        # Mention medium alerts briefly
        if medium_alerts:
            response_parts.append(
                self._format_medium_alerts_summary(medium_alerts, tone)
            )

        # Add recommended actions
        response_parts.append("")
        response_parts.append(
            self._format_alert_recommendations(alerts, persona_name, tone)
        )

        return "\n".join(response_parts)

    def format_team_health_response(
        self, health_data: Dict[str, Any], persona_name: str
    ) -> str:
        """Format team health data for conversational response."""
        tone = self._get_persona_tone(persona_name)

        response_parts = []
        response_parts.append(self._get_team_health_greeting(persona_name, tone))
        response_parts.append("")

        # Overall health assessment
        overall_health = self._assess_overall_health(health_data)
        response_parts.append(self._format_health_assessment(overall_health, tone))
        response_parts.append("")

        # Key metrics in conversational format
        key_metrics = self._extract_health_metrics(health_data)
        response_parts.extend(self._format_health_metrics(key_metrics, tone))

        # Persona-specific health insights
        persona_insights = self._generate_health_insights_for_persona(
            health_data, persona_name
        )
        if persona_insights:
            response_parts.append("")
            response_parts.append(persona_insights)

        return "\n".join(response_parts)

    def _initialize_tone_templates(self) -> Dict[ConversationTone, Dict[str, str]]:
        """Initialize tone-specific response templates."""
        return {
            ConversationTone.EXECUTIVE: {
                "greeting_formal": "Based on current operational data",
                "confidence_high": "I'm confident in this assessment",
                "confidence_medium": "This analysis is based on available data",
                "urgency_high": "This requires immediate executive attention",
                "status_good": "Operations are performing well",
                "status_concern": "There are some areas that need attention",
            },
            ConversationTone.COLLABORATIVE: {
                "greeting_formal": "Here's what I'm seeing across the teams",
                "confidence_high": "The data looks solid on this",
                "confidence_medium": "Based on what we're tracking",
                "urgency_high": "We should definitely address this",
                "status_good": "Things are looking good",
                "status_concern": "We've got a few things to work on",
            },
            ConversationTone.TECHNICAL: {
                "greeting_formal": "From an architectural perspective",
                "confidence_high": "The metrics clearly indicate",
                "confidence_medium": "Current data suggests",
                "urgency_high": "This requires immediate technical intervention",
                "status_good": "All systems are operating within parameters",
                "status_concern": "Several metrics indicate attention needed",
            },
            ConversationTone.STRATEGIC: {
                "greeting_formal": "Looking at the strategic implications",
                "confidence_high": "This aligns with our strategic indicators",
                "confidence_medium": "Based on current strategic metrics",
                "urgency_high": "This has significant strategic implications",
                "status_good": "We're on track strategically",
                "status_concern": "There are strategic risks to consider",
            },
        }

    def _initialize_persona_tones(self) -> Dict[str, ConversationTone]:
        """Map personas to their preferred conversation tones."""
        return {
            "diego": ConversationTone.COLLABORATIVE,
            "camille": ConversationTone.STRATEGIC,
            "rachel": ConversationTone.COLLABORATIVE,
            "alvaro": ConversationTone.EXECUTIVE,
            "martin": ConversationTone.TECHNICAL,
            "sofia": ConversationTone.COLLABORATIVE,
            "elena": ConversationTone.TECHNICAL,
            "marcus": ConversationTone.COLLABORATIVE,
            "david": ConversationTone.EXECUTIVE,
            "security": ConversationTone.TECHNICAL,
            "data": ConversationTone.TECHNICAL,
        }

    def _get_persona_tone(self, persona_name: str) -> ConversationTone:
        """Get appropriate conversation tone for persona."""
        return self.persona_tone_mapping.get(
            persona_name.lower(), ConversationTone.COLLABORATIVE
        )

    def _get_summary_greeting(self, persona_name: str, tone: ConversationTone) -> str:
        """Generate persona-appropriate summary greeting."""
        greetings = {
            "diego": "🏗️ Here's your platform engineering summary:",
            "camille": "🎯 Strategic technology overview:",
            "rachel": "🎨 Design systems and UX summary:",
            "alvaro": "💼 Business value and ROI summary:",
            "martin": "⚡ Platform architecture status:",
            "sofia": "🤝 Partnership and vendor status:",
            "elena": "🛡️ Compliance and accessibility summary:",
            "marcus": "📢 Platform adoption summary:",
            "david": "💰 Financial and investment summary:",
            "security": "🔒 Security architecture summary:",
            "data": "📊 Analytics and metrics summary:",
        }

        return greetings.get(persona_name.lower(), "📋 Executive summary:")

    def _extract_key_insights(self, report: GeneratedReport) -> List[Dict[str, Any]]:
        """Extract key insights from P2.1 report for conversation."""
        insights = []

        for section in report.sections:
            if section.title == "Executive Summary":
                # Parse bullet points as insights
                lines = section.content.split("\n")
                for line in lines:
                    if line.strip() and line.startswith("•"):
                        insights.append(
                            {
                                "type": "highlight",
                                "content": line[1:].strip(),
                                "priority": "high",
                            }
                        )

            elif section.title == "Risks & Opportunities":
                lines = section.content.split("\n")
                for line in lines:
                    if line.strip():
                        if line.startswith("⚠️"):
                            insights.append(
                                {
                                    "type": "risk",
                                    "content": line[2:].strip(),
                                    "priority": "high",
                                }
                            )
                        elif line.startswith("✅"):
                            insights.append(
                                {
                                    "type": "opportunity",
                                    "content": line[2:].strip(),
                                    "priority": "medium",
                                }
                            )

        return insights

    def _format_insights_for_conversation(
        self, insights: List[Dict[str, Any]], tone: ConversationTone
    ) -> List[str]:
        """Format insights for natural conversation."""
        lines = []

        # Group insights by type
        highlights = [i for i in insights if i["type"] == "highlight"]
        risks = [i for i in insights if i["type"] == "risk"]
        opportunities = [i for i in insights if i["type"] == "opportunity"]

        if highlights:
            lines.append("**Key Highlights:**")
            for insight in highlights[:3]:  # Top 3 highlights
                lines.append(f"• {insight['content']}")
            lines.append("")

        if risks:
            lines.append("**Items to Watch:**")
            for risk in risks[:2]:  # Top 2 risks
                lines.append(f"⚠️ {risk['content']}")
            lines.append("")

        if opportunities:
            lines.append("**Positive Indicators:**")
            for opp in opportunities[:2]:  # Top 2 opportunities
                lines.append(f"✅ {opp['content']}")

        return lines

    def _generate_persona_specific_analysis(
        self, report: GeneratedReport, persona_name: str
    ) -> Optional[str]:
        """Generate analysis specific to the requesting persona."""
        analyses = {
            "diego": "**Platform Engineering Perspective:** Cross-team coordination and infrastructure scaling remain strong priorities.",
            "camille": "**Strategic Technology View:** Current technical trajectory supports our competitive positioning.",
            "rachel": "**Design Systems Impact:** Consistency and user experience metrics trending positively.",
            "alvaro": "**Business Value Assessment:** Platform investments showing measurable ROI through improved delivery metrics.",
            "martin": "**Architecture Health:** Technical debt management and platform evolution proceeding as planned.",
            "sofia": "**Partnership Impact:** Vendor relationships and tool integrations supporting team productivity.",
            "elena": "**Compliance Status:** Accessibility and legal requirements being met within established frameworks.",
            "marcus": "**Adoption Metrics:** Platform utilization and team onboarding progressing well.",
            "david": "**Financial Performance:** Technology investments aligned with budget expectations and ROI targets.",
            "security": "**Security Posture:** Architecture security and threat management within acceptable parameters.",
            "data": "**Analytics Insight:** Data quality and metrics reliability supporting informed decision-making.",
        }

        return analyses.get(persona_name.lower())

    def _format_confidence_statement(
        self, report: GeneratedReport, tone: ConversationTone
    ) -> str:
        """Format confidence and data freshness for conversation."""
        confidence = report.confidence_score or 0.8

        templates = self.tone_templates[tone]

        if confidence >= 0.9:
            confidence_phrase = templates["confidence_high"]
        else:
            confidence_phrase = templates["confidence_medium"]

        # Format timestamp
        report_time = datetime.fromisoformat(report.generated_at.replace("Z", "+00:00"))
        time_str = report_time.strftime("%B %d at %I:%M %p")

        return f"*{confidence_phrase} (confidence: {confidence:.0%}). Data current as of {time_str}.*"

    def _format_no_alerts_response(
        self, persona_name: str, tone: ConversationTone
    ) -> str:
        """Format response when no alerts are active."""
        responses = {
            "diego": "✅ **All clear on the platform front!** No critical issues requiring your attention. Engineering operations are running smoothly.",
            "camille": "✅ **Strategic technology status is green.** No urgent technical issues impacting our strategic objectives.",
            "rachel": "✅ **Design systems and UX are healthy.** No critical user experience issues to address right now.",
            "alvaro": "✅ **Business operations are stable.** No alerts affecting ROI or business value delivery.",
            "martin": "✅ **Platform architecture is stable.** All systems operating within normal parameters.",
        }

        return responses.get(
            persona_name.lower(),
            "✅ **No critical alerts.** All monitored systems are operating normally.",
        )

    def _get_alerts_greeting(
        self, alert_count: int, persona_name: str, tone: ConversationTone
    ) -> str:
        """Generate appropriate greeting for alerts."""
        if alert_count == 1:
            return f"🚨 **1 Alert** needs your attention:"
        else:
            return f"🚨 **{alert_count} Alerts** require attention:"

    def _format_critical_alerts(
        self, alerts: List, tone: ConversationTone
    ) -> List[str]:
        """Format critical alerts with appropriate urgency."""
        lines = []
        lines.append("**🔴 Critical Issues (Immediate Action Required):**")

        for alert in alerts:
            lines.append(f"• **{alert.title}**")
            lines.append(f"  {alert.message}")
            if alert.actionable_items:
                lines.append(f"  *Immediate action: {alert.actionable_items[0]}*")
            lines.append("")

        return lines

    def _format_high_priority_alerts(
        self, alerts: List, tone: ConversationTone
    ) -> List[str]:
        """Format high priority alerts."""
        lines = []
        lines.append("**🟡 High Priority Items:**")

        for alert in alerts:
            lines.append(f"• **{alert.title}**: {alert.message}")

        return lines

    def _format_medium_alerts_summary(
        self, alerts: List, tone: ConversationTone
    ) -> str:
        """Format summary of medium priority alerts."""
        if len(alerts) == 1:
            return f"**🟠 Also tracking:** 1 medium priority item."
        else:
            return f"**🟠 Also tracking:** {len(alerts)} medium priority items."

    def _format_alert_recommendations(
        self, alerts: List, persona_name: str, tone: ConversationTone
    ) -> str:
        """Format recommendations based on alerts and persona."""
        critical_count = len([a for a in alerts if a.severity.value == "critical"])

        if critical_count > 0:
            recommendations = {
                "diego": "**Recommended:** Review with platform team leads and escalate blocked issues to unblock delivery.",
                "camille": "**Strategic Impact:** These issues may affect our technology roadmap. Consider resource reallocation.",
                "rachel": "**UX Impact:** Monitor for user experience degradation and adjust design system priorities if needed.",
                "alvaro": "**Business Risk:** Critical alerts may impact ROI. Review mitigation strategies and timeline adjustments.",
                "martin": "**Architecture Action:** Review system health and consider emergency architectural decisions if needed.",
            }

            return recommendations.get(
                persona_name.lower(),
                "**Recommendation:** Address critical issues immediately to prevent escalation.",
            )
        else:
            return "**Recommendation:** Monitor these items but no immediate intervention required."

    def _get_team_health_greeting(
        self, persona_name: str, tone: ConversationTone
    ) -> str:
        """Generate team health greeting for persona."""
        greetings = {
            "diego": "💪 **Platform Team Health Check:**",
            "camille": "🎯 **Strategic Team Performance:**",
            "rachel": "🎨 **Design Team Health Overview:**",
            "martin": "⚡ **Engineering Team Status:**",
        }

        return greetings.get(persona_name.lower(), "💪 **Team Health Overview:**")

    def _assess_overall_health(self, health_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall team health from data."""
        team_health = health_data.get("team_health", {})
        overall_score = team_health.get("overall_score", 75)

        if overall_score >= 85:
            return {
                "status": "excellent",
                "score": overall_score,
                "message": "performing exceptionally well",
            }
        elif overall_score >= 75:
            return {
                "status": "good",
                "score": overall_score,
                "message": "performing well with minor areas for improvement",
            }
        elif overall_score >= 65:
            return {
                "status": "fair",
                "score": overall_score,
                "message": "showing some concerning trends that need attention",
            }
        else:
            return {
                "status": "poor",
                "score": overall_score,
                "message": "requiring immediate intervention and support",
            }

    def _format_health_assessment(
        self, assessment: Dict[str, Any], tone: ConversationTone
    ) -> str:
        """Format overall health assessment."""
        score = assessment["score"]
        message = assessment["message"]

        status_icons = {"excellent": "🟢", "good": "✅", "fair": "⚠️", "poor": "🔴"}

        icon = status_icons.get(assessment["status"], "📊")

        return f"{icon} **Overall Health: {score}%** - Team is {message}."

    def _extract_health_metrics(
        self, health_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract key health metrics for conversation."""
        metrics = []

        team_velocity = health_data.get("team_velocity", {})
        if team_velocity:
            current_velocity = team_velocity.get("current_sprint", 0)
            trend = team_velocity.get("trend", "stable")
            metrics.append(
                {
                    "name": "Velocity",
                    "value": f"{current_velocity} story points",
                    "trend": trend,
                    "type": "velocity",
                }
            )

        team_health = health_data.get("team_health", {})
        if team_health:
            collab_score = team_health.get("collaboration_score", 80)
            metrics.append(
                {
                    "name": "Collaboration",
                    "value": f"{collab_score}%",
                    "trend": "stable",
                    "type": "collaboration",
                }
            )

            quality_score = team_health.get("quality_metrics", 80)
            metrics.append(
                {
                    "name": "Quality",
                    "value": f"{quality_score}%",
                    "trend": "stable",
                    "type": "quality",
                }
            )

        return metrics

    def _format_health_metrics(
        self, metrics: List[Dict[str, Any]], tone: ConversationTone
    ) -> List[str]:
        """Format health metrics for conversation."""
        lines = []

        for metric in metrics:
            trend_indicators = {"increasing": "📈", "decreasing": "📉", "stable": "📊"}

            trend_icon = trend_indicators.get(metric["trend"], "📊")
            lines.append(f"• **{metric['name']}**: {metric['value']} {trend_icon}")

        return lines

    def _generate_health_insights_for_persona(
        self, health_data: Dict[str, Any], persona_name: str
    ) -> Optional[str]:
        """Generate health insights specific to persona."""
        insights = {
            "diego": "**Platform Perspective:** Cross-team coordination metrics indicate healthy collaboration patterns.",
            "rachel": "**Design Impact:** Team quality scores support consistent user experience delivery.",
            "martin": "**Architecture View:** Technical quality metrics align with platform health objectives.",
            "camille": "**Strategic Assessment:** Team performance supports our technology strategy execution.",
        }

        return insights.get(persona_name.lower())
