"""
Intelligent Alert System

Smart alerting with CLI integration for ClaudeDirector P2.1 features.
Provides executive-friendly alerts with contextual intelligence and priority scoring.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ..interfaces.report_interface import IAlertSystem, StakeholderType


class AlertSeverity(Enum):
    """Alert severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertCategory(Enum):
    """Alert categories for filtering and routing."""

    DELIVERY_RISK = "delivery_risk"
    TEAM_HEALTH = "team_health"
    TECHNICAL_DEBT = "technical_debt"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STAKEHOLDER = "stakeholder"
    STRATEGIC = "strategic"


@dataclass
class Alert:
    """Individual alert with metadata and routing information."""

    id: str
    title: str
    message: str
    severity: AlertSeverity
    category: AlertCategory
    stakeholders: List[StakeholderType]
    data_source: str
    created_at: datetime
    context: Dict[str, Any]
    actionable_items: List[str]
    confidence_score: float


@dataclass
class AlertRule:
    """Alert rule configuration."""

    name: str
    category: AlertCategory
    severity: AlertSeverity
    stakeholders: List[StakeholderType]
    condition_func: str  # Function name to evaluate
    cooldown_hours: int = 24
    enabled: bool = True


class IntelligentAlertSystem(IAlertSystem):
    """
    Intelligent alert system with executive context and priority scoring.

    Features:
    - Executive-friendly alert prioritization
    - Stakeholder-specific routing and content
    - Smart cooldown to prevent alert fatigue
    - Contextual recommendations and actions
    - CLI integration with rich formatting
    """

    def __init__(self, data_source):
        self.data_source = data_source
        self.alert_rules = self._initialize_alert_rules()
        self.alert_history = []
        self.cooldown_tracker = {}

    def should_alert(self, data: Dict[str, Any]) -> bool:
        """Determine if any alerts should be triggered based on data."""
        alerts = self.generate_alerts(data)
        return len(alerts) > 0

    def generate_alert(self, data: Dict[str, Any]) -> str:
        """Generate alert message based on data (IAlertSystem interface)."""
        alerts = self.generate_alerts(data)
        if not alerts:
            return "No alerts at this time."

        # Return formatted summary of all alerts
        critical_alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]
        high_alerts = [a for a in alerts if a.severity == AlertSeverity.HIGH]

        summary = f"🚨 {len(critical_alerts)} critical, {len(high_alerts)} high priority alerts"
        return summary

    def get_alert_channels(self) -> List[str]:
        """Return list of available alert channels."""
        return ["cli", "email", "slack", "dashboard"]

    def generate_alerts(self, data: Dict[str, Any]) -> List[Alert]:
        """Generate all applicable alerts based on current data."""
        alerts = []

        for rule in self.alert_rules:
            if not rule.enabled:
                continue

            # Check cooldown
            if self._is_in_cooldown(rule.name):
                continue

            # Evaluate rule condition
            if self._evaluate_rule_condition(rule, data):
                alert = self._create_alert_from_rule(rule, data)
                if alert:
                    alerts.append(alert)
                    self._update_cooldown(rule.name)

        # Sort alerts by severity and confidence
        alerts.sort(key=lambda a: (a.severity.value, -a.confidence_score))

        return alerts

    def get_stakeholder_alerts(
        self, stakeholder_type: StakeholderType, data: Dict[str, Any]
    ) -> List[Alert]:
        """Get alerts filtered for specific stakeholder type."""
        all_alerts = self.generate_alerts(data)
        return [alert for alert in all_alerts if stakeholder_type in alert.stakeholders]

    def format_alerts_for_cli(self, alerts: List[Alert]) -> str:
        """Format alerts for CLI display with rich formatting."""
        if not alerts:
            return "✅ No active alerts - all systems operating normally"

        lines = []
        lines.append("🚨 ACTIVE ALERTS")
        lines.append("=" * 50)

        # Group by severity
        critical_alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]
        high_alerts = [a for a in alerts if a.severity == AlertSeverity.HIGH]
        medium_alerts = [a for a in alerts if a.severity == AlertSeverity.MEDIUM]

        # Critical alerts first
        if critical_alerts:
            lines.append("\n🔴 CRITICAL ALERTS")
            lines.append("-" * 30)
            for alert in critical_alerts:
                lines.append(self._format_alert_for_cli(alert))

        # High priority alerts
        if high_alerts:
            lines.append("\n🟡 HIGH PRIORITY ALERTS")
            lines.append("-" * 30)
            for alert in high_alerts:
                lines.append(self._format_alert_for_cli(alert))

        # Medium priority alerts (limit to 3 for CLI brevity)
        if medium_alerts:
            lines.append("\n🟠 MEDIUM PRIORITY ALERTS")
            lines.append("-" * 30)
            for alert in medium_alerts[:3]:
                lines.append(self._format_alert_for_cli(alert))

            if len(medium_alerts) > 3:
                lines.append(
                    f"   ... and {len(medium_alerts) - 3} more medium priority alerts"
                )

        # Summary and next actions
        lines.append(f"\n📊 SUMMARY")
        lines.append(f"   Total alerts: {len(alerts)}")
        lines.append(f"   Highest priority: {alerts[0].severity.value.upper()}")
        lines.append(
            f"   Requires immediate attention: {len(critical_alerts) + len(high_alerts)}"
        )

        lines.append(f"\n💡 NEXT ACTIONS")
        lines.append(
            f"   ./claudedirector reports executive    # Generate detailed report"
        )
        lines.append(f"   ./claudedirector dashboard --refresh  # Update all data")

        return "\n".join(lines)

    def _initialize_alert_rules(self) -> List[AlertRule]:
        """Initialize default alert rules for executive scenarios."""
        return [
            # Critical delivery risks
            AlertRule(
                name="critical_blocked_issues",
                category=AlertCategory.DELIVERY_RISK,
                severity=AlertSeverity.CRITICAL,
                stakeholders=[StakeholderType.VP_ENGINEERING, StakeholderType.CEO],
                condition_func="check_critical_blocked_issues",
                cooldown_hours=4,
            ),
            AlertRule(
                name="velocity_crash",
                category=AlertCategory.DELIVERY_RISK,
                severity=AlertSeverity.HIGH,
                stakeholders=[
                    StakeholderType.VP_ENGINEERING,
                    StakeholderType.PRODUCT_TEAM,
                ],
                condition_func="check_velocity_crash",
                cooldown_hours=12,
            ),
            AlertRule(
                name="initiative_at_risk",
                category=AlertCategory.STRATEGIC,
                severity=AlertSeverity.HIGH,
                stakeholders=[StakeholderType.CEO, StakeholderType.VP_ENGINEERING],
                condition_func="check_strategic_initiatives_at_risk",
                cooldown_hours=24,
            ),
            # Team health alerts
            AlertRule(
                name="team_health_degrading",
                category=AlertCategory.TEAM_HEALTH,
                severity=AlertSeverity.MEDIUM,
                stakeholders=[
                    StakeholderType.VP_ENGINEERING,
                    StakeholderType.ENGINEERING_MANAGER,
                ],
                condition_func="check_team_health_degrading",
                cooldown_hours=48,
            ),
            # Technical debt alerts
            AlertRule(
                name="technical_debt_spike",
                category=AlertCategory.TECHNICAL_DEBT,
                severity=AlertSeverity.MEDIUM,
                stakeholders=[StakeholderType.VP_ENGINEERING],
                condition_func="check_technical_debt_spike",
                cooldown_hours=72,
            ),
            # Security alerts
            AlertRule(
                name="security_vulnerabilities",
                category=AlertCategory.SECURITY,
                severity=AlertSeverity.CRITICAL,
                stakeholders=[StakeholderType.CEO, StakeholderType.VP_ENGINEERING],
                condition_func="check_security_vulnerabilities",
                cooldown_hours=1,
            ),
            # Performance alerts
            AlertRule(
                name="delivery_predictability_drop",
                category=AlertCategory.PERFORMANCE,
                severity=AlertSeverity.MEDIUM,
                stakeholders=[
                    StakeholderType.VP_ENGINEERING,
                    StakeholderType.PRODUCT_TEAM,
                ],
                condition_func="check_delivery_predictability_drop",
                cooldown_hours=24,
            ),
        ]

    def _is_in_cooldown(self, rule_name: str) -> bool:
        """Check if alert rule is in cooldown period."""
        last_triggered = self.cooldown_tracker.get(rule_name)
        if not last_triggered:
            return False

        rule = next((r for r in self.alert_rules if r.name == rule_name), None)
        if not rule:
            return False

        cooldown_period = timedelta(hours=rule.cooldown_hours)
        return datetime.now() - last_triggered < cooldown_period

    def _update_cooldown(self, rule_name: str):
        """Update cooldown tracker for alert rule."""
        self.cooldown_tracker[rule_name] = datetime.now()

    def _evaluate_rule_condition(self, rule: AlertRule, data: Dict[str, Any]) -> bool:
        """Evaluate if alert rule condition is met."""
        # Map condition functions to actual implementations
        condition_map = {
            "check_critical_blocked_issues": self._check_critical_blocked_issues,
            "check_velocity_crash": self._check_velocity_crash,
            "check_strategic_initiatives_at_risk": self._check_strategic_initiatives_at_risk,
            "check_team_health_degrading": self._check_team_health_degrading,
            "check_technical_debt_spike": self._check_technical_debt_spike,
            "check_security_vulnerabilities": self._check_security_vulnerabilities,
            "check_delivery_predictability_drop": self._check_delivery_predictability_drop,
        }

        condition_func = condition_map.get(rule.condition_func)
        if not condition_func:
            return False

        return condition_func(data)

    def _create_alert_from_rule(
        self, rule: AlertRule, data: Dict[str, Any]
    ) -> Optional[Alert]:
        """Create alert instance from triggered rule."""
        # Generate alert content based on rule type
        alert_generators = {
            "check_critical_blocked_issues": self._generate_blocked_issues_alert,
            "check_velocity_crash": self._generate_velocity_crash_alert,
            "check_strategic_initiatives_at_risk": self._generate_initiatives_alert,
            "check_team_health_degrading": self._generate_team_health_alert,
            "check_technical_debt_spike": self._generate_technical_debt_alert,
            "check_security_vulnerabilities": self._generate_security_alert,
            "check_delivery_predictability_drop": self._generate_predictability_alert,
        }

        generator = alert_generators.get(rule.condition_func)
        if not generator:
            return None

        return generator(rule, data)

    def _format_alert_for_cli(self, alert: Alert) -> str:
        """Format individual alert for CLI display."""
        lines = []

        # Alert header with severity indicator
        severity_icons = {
            AlertSeverity.CRITICAL: "🔴",
            AlertSeverity.HIGH: "🟡",
            AlertSeverity.MEDIUM: "🟠",
            AlertSeverity.LOW: "🟢",
            AlertSeverity.INFO: "ℹ️",
        }

        icon = severity_icons.get(alert.severity, "•")
        lines.append(f"{icon} {alert.title}")
        lines.append(f"   {alert.message}")

        # Add actionable items if available
        if alert.actionable_items:
            lines.append("   Actions:")
            for action in alert.actionable_items[:2]:  # Limit for CLI brevity
                lines.append(f"   • {action}")

        lines.append(
            f"   Confidence: {alert.confidence_score:.0%} | {alert.created_at.strftime('%H:%M')}"
        )
        lines.append("")

        return "\n".join(lines)

    # Condition checking methods
    def _check_critical_blocked_issues(self, data: Dict[str, Any]) -> bool:
        """Check for critical blocked issues."""
        risk_data = data.get("risk_indicators", {})
        blocked_issues = risk_data.get("blocked_issues", 0)
        critical_bugs = risk_data.get("critical_bugs", 0)

        return blocked_issues >= 3 or critical_bugs >= 2

    def _check_velocity_crash(self, data: Dict[str, Any]) -> bool:
        """Check for significant velocity drop."""
        velocity_data = data.get("team_velocity", {})
        current = velocity_data.get("current_sprint", 0)
        average = velocity_data.get("average_last_5", 0)

        if average == 0:
            return False

        # Alert if velocity dropped by more than 30%
        drop_percentage = (average - current) / average
        return drop_percentage > 0.3

    def _check_strategic_initiatives_at_risk(self, data: Dict[str, Any]) -> bool:
        """Check for strategic initiatives at risk."""
        initiative_data = data.get("initiative_health", {})
        at_risk = initiative_data.get("at_risk", 0)
        critical = initiative_data.get("critical", 0)

        return critical >= 2 or at_risk >= 4

    def _check_team_health_degrading(self, data: Dict[str, Any]) -> bool:
        """Check for degrading team health metrics."""
        health_data = data.get("team_health", {})
        overall_score = health_data.get("overall_score", 100)

        return overall_score < 70

    def _check_technical_debt_spike(self, data: Dict[str, Any]) -> bool:
        """Check for technical debt spike."""
        health_data = data.get("team_health", {})
        debt_ratio = health_data.get("technical_debt_ratio", 0)

        return debt_ratio > 0.25  # Alert if technical debt > 25%

    def _check_security_vulnerabilities(self, data: Dict[str, Any]) -> bool:
        """Check for security vulnerabilities."""
        risk_data = data.get("risk_indicators", {})
        security_vulns = risk_data.get("security_vulnerabilities", 0)

        return security_vulns > 0

    def _check_delivery_predictability_drop(self, data: Dict[str, Any]) -> bool:
        """Check for delivery predictability drop."""
        velocity_data = data.get("team_velocity", {})
        accuracy = velocity_data.get("sprint_commitment_accuracy", 1.0)

        return accuracy < 0.70  # Alert if accuracy drops below 70%

    # Alert generation methods
    def _generate_blocked_issues_alert(
        self, rule: AlertRule, data: Dict[str, Any]
    ) -> Alert:
        """Generate alert for blocked issues."""
        risk_data = data.get("risk_indicators", {})
        blocked_issues = risk_data.get("blocked_issues", 0)
        critical_bugs = risk_data.get("critical_bugs", 0)

        return Alert(
            id=f"blocked_issues_{datetime.now().strftime('%Y%m%d_%H%M')}",
            title="Critical Delivery Blockers Detected",
            message=f"{blocked_issues} blocked issues and {critical_bugs} critical bugs require immediate attention to prevent delivery delays.",
            severity=rule.severity,
            category=rule.category,
            stakeholders=rule.stakeholders,
            data_source="jira",
            created_at=datetime.now(),
            context={"blocked_issues": blocked_issues, "critical_bugs": critical_bugs},
            actionable_items=[
                "Review blocked issues in daily standup",
                "Escalate critical bugs to senior engineers",
                "Consider scope reduction if timeline at risk",
            ],
            confidence_score=0.95,
        )

    def _generate_velocity_crash_alert(
        self, rule: AlertRule, data: Dict[str, Any]
    ) -> Alert:
        """Generate alert for velocity crash."""
        velocity_data = data.get("team_velocity", {})
        current = velocity_data.get("current_sprint", 0)
        average = velocity_data.get("average_last_5", 0)

        drop_percentage = ((average - current) / average) * 100 if average > 0 else 0

        return Alert(
            id=f"velocity_crash_{datetime.now().strftime('%Y%m%d_%H%M')}",
            title="Team Velocity Significant Drop",
            message=f"Sprint velocity dropped {drop_percentage:.0f}% below recent average ({current} vs {average} points).",
            severity=rule.severity,
            category=rule.category,
            stakeholders=rule.stakeholders,
            data_source="jira",
            created_at=datetime.now(),
            context={
                "current_velocity": current,
                "average_velocity": average,
                "drop_percentage": drop_percentage,
            },
            actionable_items=[
                "Investigate team capacity and blockers",
                "Review sprint commitment accuracy",
                "Consider team support and process improvements",
            ],
            confidence_score=0.90,
        )

    def _generate_initiatives_alert(
        self, rule: AlertRule, data: Dict[str, Any]
    ) -> Alert:
        """Generate alert for strategic initiatives at risk."""
        initiative_data = data.get("initiative_health", {})
        at_risk = initiative_data.get("at_risk", 0)
        critical = initiative_data.get("critical", 0)

        return Alert(
            id=f"initiatives_risk_{datetime.now().strftime('%Y%m%d_%H%M')}",
            title="Strategic Initiatives Risk Alert",
            message=f"{critical} initiatives in critical state, {at_risk} at risk. Strategic goals may be impacted.",
            severity=rule.severity,
            category=rule.category,
            stakeholders=rule.stakeholders,
            data_source="jira",
            created_at=datetime.now(),
            context={"critical_initiatives": critical, "at_risk_initiatives": at_risk},
            actionable_items=[
                "Review initiative roadmaps and dependencies",
                "Reallocate resources to critical initiatives",
                "Consider scope adjustments or timeline extensions",
            ],
            confidence_score=0.85,
        )

    def _generate_team_health_alert(
        self, rule: AlertRule, data: Dict[str, Any]
    ) -> Alert:
        """Generate alert for team health degradation."""
        health_data = data.get("team_health", {})
        overall_score = health_data.get("overall_score", 100)

        return Alert(
            id=f"team_health_{datetime.now().strftime('%Y%m%d_%H%M')}",
            title="Team Health Degradation",
            message=f"Team health score dropped to {overall_score}%. Team sustainability and productivity may be at risk.",
            severity=rule.severity,
            category=rule.category,
            stakeholders=rule.stakeholders,
            data_source="claudedirector",
            created_at=datetime.now(),
            context={"health_score": overall_score},
            actionable_items=[
                "Schedule team retrospective and feedback sessions",
                "Review workload distribution and burnout indicators",
                "Consider team building and process improvements",
            ],
            confidence_score=0.80,
        )

    def _generate_technical_debt_alert(
        self, rule: AlertRule, data: Dict[str, Any]
    ) -> Alert:
        """Generate alert for technical debt spike."""
        health_data = data.get("team_health", {})
        debt_ratio = health_data.get("technical_debt_ratio", 0)

        return Alert(
            id=f"tech_debt_{datetime.now().strftime('%Y%m%d_%H%M')}",
            title="Technical Debt Accumulation",
            message=f"Technical debt ratio reached {debt_ratio:.1%}. Code quality and development velocity may be impacted.",
            severity=rule.severity,
            category=rule.category,
            stakeholders=rule.stakeholders,
            data_source="claudedirector",
            created_at=datetime.now(),
            context={"debt_ratio": debt_ratio},
            actionable_items=[
                "Schedule technical debt reduction sprint",
                "Review code quality standards and practices",
                "Allocate time for refactoring in upcoming sprints",
            ],
            confidence_score=0.75,
        )

    def _generate_security_alert(self, rule: AlertRule, data: Dict[str, Any]) -> Alert:
        """Generate alert for security vulnerabilities."""
        risk_data = data.get("risk_indicators", {})
        security_vulns = risk_data.get("security_vulnerabilities", 0)

        return Alert(
            id=f"security_{datetime.now().strftime('%Y%m%d_%H%M')}",
            title="Security Vulnerabilities Detected",
            message=f"{security_vulns} security vulnerabilities require immediate remediation.",
            severity=rule.severity,
            category=rule.category,
            stakeholders=rule.stakeholders,
            data_source="security_scan",
            created_at=datetime.now(),
            context={"vulnerability_count": security_vulns},
            actionable_items=[
                "Prioritize security patches in current sprint",
                "Review security scanning and monitoring processes",
                "Escalate to security team for immediate assessment",
            ],
            confidence_score=0.98,
        )

    def _generate_predictability_alert(
        self, rule: AlertRule, data: Dict[str, Any]
    ) -> Alert:
        """Generate alert for delivery predictability drop."""
        velocity_data = data.get("team_velocity", {})
        accuracy = velocity_data.get("sprint_commitment_accuracy", 1.0)

        return Alert(
            id=f"predictability_{datetime.now().strftime('%Y%m%d_%H%M')}",
            title="Delivery Predictability Decline",
            message=f"Sprint commitment accuracy dropped to {accuracy:.0%}. Planning and estimation may need adjustment.",
            severity=rule.severity,
            category=rule.category,
            stakeholders=rule.stakeholders,
            data_source="jira",
            created_at=datetime.now(),
            context={"commitment_accuracy": accuracy},
            actionable_items=[
                "Review estimation and planning processes",
                "Analyze sprint commitment vs delivery patterns",
                "Consider team capacity and external dependency factors",
            ],
            confidence_score=0.85,
        )
