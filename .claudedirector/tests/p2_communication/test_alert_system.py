"""
Test Intelligent Alert System

Comprehensive tests for P2.1 Intelligent Alert System.
Tests alert generation, stakeholder filtering, and CLI formatting.
"""

import unittest
from datetime import datetime
from typing import Dict, Any

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from lib.claudedirector.p2_communication.integrations.alert_system import (
    IntelligentAlertSystem,
    AlertSeverity,
    AlertCategory,
)
from lib.claudedirector.p2_communication.interfaces.report_interface import (
    StakeholderType,
    IDataSource,
)


class MockDataSource(IDataSource):
    """Mock data source for testing."""

    def __init__(self, mock_data: Dict[str, Any]):
        self.mock_data = mock_data

    def get_data(self, time_period: str, metrics: list) -> Dict[str, Any]:
        return self.mock_data

    def get_data_freshness(self) -> str:
        return "2025-08-10 09:00:00"

    def is_available(self) -> bool:
        return True


class TestIntelligentAlertSystem(unittest.TestCase):
    """Test cases for Intelligent Alert System."""

    def setUp(self):
        """Set up test fixtures."""
        self.normal_data = {
            "team_velocity": {
                "current_sprint": 42,
                "average_last_5": 40,
                "trend": "stable",
                "sprint_commitment_accuracy": 0.85,
            },
            "risk_indicators": {
                "blocked_issues": 1,
                "overdue_issues": 2,
                "critical_bugs": 0,
                "security_vulnerabilities": 0,
            },
            "initiative_health": {"on_track": 8, "at_risk": 1, "critical": 0},
            "team_health": {"overall_score": 82, "technical_debt_ratio": 0.15},
        }

        self.data_source = MockDataSource(self.normal_data)
        self.alert_system = IntelligentAlertSystem(self.data_source)

    def test_alert_system_initialization(self):
        """Test that alert system initializes correctly."""
        self.assertIsNotNone(self.alert_system)
        self.assertEqual(self.alert_system.data_source, self.data_source)
        self.assertIsInstance(self.alert_system.alert_rules, list)
        self.assertGreater(len(self.alert_system.alert_rules), 0)
        self.assertEqual(len(self.alert_system.alert_history), 0)
        self.assertEqual(len(self.alert_system.cooldown_tracker), 0)

    def test_no_alerts_normal_conditions(self):
        """Test that no alerts are generated under normal conditions."""
        alerts = self.alert_system.generate_alerts(self.normal_data)
        self.assertEqual(len(alerts), 0)

        should_alert = self.alert_system.should_alert(self.normal_data)
        self.assertFalse(should_alert)

        alert_message = self.alert_system.generate_alert(self.normal_data)
        self.assertEqual(alert_message, "No alerts at this time.")

    def test_critical_blocked_issues_alert(self):
        """Test alert generation for critical blocked issues."""
        problem_data = self.normal_data.copy()
        problem_data["risk_indicators"] = {
            "blocked_issues": 4,  # Triggers alert (>= 3)
            "overdue_issues": 2,
            "critical_bugs": 0,
            "security_vulnerabilities": 0,
        }

        alerts = self.alert_system.generate_alerts(problem_data)

        # Should generate blocked issues alert
        blocked_alerts = [
            a
            for a in alerts
            if "blocker" in a.title.lower() or "delivery" in a.title.lower()
        ]
        self.assertGreater(len(blocked_alerts), 0)

        blocked_alert = blocked_alerts[0]
        self.assertEqual(blocked_alert.severity, AlertSeverity.CRITICAL)
        self.assertEqual(blocked_alert.category, AlertCategory.DELIVERY_RISK)
        self.assertIn(StakeholderType.VP_ENGINEERING, blocked_alert.stakeholders)
        self.assertGreater(len(blocked_alert.actionable_items), 0)

    def test_security_vulnerability_alert(self):
        """Test alert generation for security vulnerabilities."""
        problem_data = self.normal_data.copy()
        problem_data["risk_indicators"] = {
            "blocked_issues": 1,
            "overdue_issues": 2,
            "critical_bugs": 0,
            "security_vulnerabilities": 2,  # Triggers alert (> 0)
        }

        alerts = self.alert_system.generate_alerts(problem_data)

        # Should generate security alert
        security_alerts = [a for a in alerts if "security" in a.title.lower()]
        self.assertGreater(len(security_alerts), 0)

        security_alert = security_alerts[0]
        self.assertEqual(security_alert.severity, AlertSeverity.CRITICAL)
        self.assertEqual(security_alert.category, AlertCategory.SECURITY)
        self.assertIn(StakeholderType.CEO, security_alert.stakeholders)
        self.assertGreater(
            security_alert.confidence_score, 0.9
        )  # High confidence for security

    def test_velocity_crash_alert(self):
        """Test alert generation for velocity crash."""
        problem_data = self.normal_data.copy()
        problem_data["team_velocity"] = {
            "current_sprint": 25,  # 37.5% drop from average of 40
            "average_last_5": 40,
            "trend": "decreasing",
            "sprint_commitment_accuracy": 0.85,
        }

        alerts = self.alert_system.generate_alerts(problem_data)

        # Should generate velocity crash alert
        velocity_alerts = [a for a in alerts if "velocity" in a.title.lower()]
        self.assertGreater(len(velocity_alerts), 0)

        velocity_alert = velocity_alerts[0]
        self.assertEqual(velocity_alert.severity, AlertSeverity.HIGH)
        self.assertEqual(velocity_alert.category, AlertCategory.DELIVERY_RISK)
        self.assertIn(StakeholderType.VP_ENGINEERING, velocity_alert.stakeholders)

    def test_team_health_degrading_alert(self):
        """Test alert generation for degrading team health."""
        problem_data = self.normal_data.copy()
        problem_data["team_health"] = {
            "overall_score": 65,  # Triggers alert (< 70)
            "technical_debt_ratio": 0.15,
        }

        alerts = self.alert_system.generate_alerts(problem_data)

        # Should generate team health alert
        health_alerts = [a for a in alerts if "health" in a.title.lower()]
        self.assertGreater(len(health_alerts), 0)

        health_alert = health_alerts[0]
        self.assertEqual(health_alert.severity, AlertSeverity.MEDIUM)
        self.assertEqual(health_alert.category, AlertCategory.TEAM_HEALTH)
        self.assertIn(StakeholderType.VP_ENGINEERING, health_alert.stakeholders)

    def test_technical_debt_spike_alert(self):
        """Test alert generation for technical debt spike."""
        problem_data = self.normal_data.copy()
        problem_data["team_health"] = {
            "overall_score": 82,
            "technical_debt_ratio": 0.30,  # Triggers alert (> 0.25)
        }

        alerts = self.alert_system.generate_alerts(problem_data)

        # Should generate technical debt alert
        debt_alerts = [a for a in alerts if "debt" in a.title.lower()]
        self.assertGreater(len(debt_alerts), 0)

        debt_alert = debt_alerts[0]
        self.assertEqual(debt_alert.severity, AlertSeverity.MEDIUM)
        self.assertEqual(debt_alert.category, AlertCategory.TECHNICAL_DEBT)
        self.assertIn(StakeholderType.VP_ENGINEERING, debt_alert.stakeholders)

    def test_strategic_initiatives_at_risk_alert(self):
        """Test alert generation for strategic initiatives at risk."""
        problem_data = self.normal_data.copy()
        problem_data["initiative_health"] = {
            "on_track": 5,
            "at_risk": 3,
            "critical": 2,  # Triggers alert (>= 2 critical)
        }

        alerts = self.alert_system.generate_alerts(problem_data)

        # Should generate initiatives alert
        initiative_alerts = [a for a in alerts if "initiative" in a.title.lower()]
        self.assertGreater(len(initiative_alerts), 0)

        initiative_alert = initiative_alerts[0]
        self.assertEqual(initiative_alert.severity, AlertSeverity.HIGH)
        self.assertEqual(initiative_alert.category, AlertCategory.STRATEGIC)
        self.assertIn(StakeholderType.CEO, initiative_alert.stakeholders)

    def test_delivery_predictability_drop_alert(self):
        """Test alert generation for delivery predictability drop."""
        problem_data = self.normal_data.copy()
        problem_data["team_velocity"] = {
            "current_sprint": 42,
            "average_last_5": 40,
            "trend": "stable",
            "sprint_commitment_accuracy": 0.65,  # Triggers alert (< 0.70)
        }

        alerts = self.alert_system.generate_alerts(problem_data)

        # Should generate predictability alert
        predictability_alerts = [
            a for a in alerts if "predictability" in a.title.lower()
        ]
        self.assertGreater(len(predictability_alerts), 0)

        predictability_alert = predictability_alerts[0]
        self.assertEqual(predictability_alert.severity, AlertSeverity.MEDIUM)
        self.assertEqual(predictability_alert.category, AlertCategory.PERFORMANCE)
        self.assertIn(StakeholderType.VP_ENGINEERING, predictability_alert.stakeholders)

    def test_multiple_alerts_sorting(self):
        """Test that multiple alerts are sorted by severity and confidence."""
        problem_data = self.normal_data.copy()
        problem_data.update(
            {
                "risk_indicators": {
                    "blocked_issues": 4,  # Critical alert
                    "security_vulnerabilities": 1,  # Critical alert
                    "overdue_issues": 2,
                    "critical_bugs": 0,
                },
                "team_health": {
                    "overall_score": 65,  # Medium alert
                    "technical_debt_ratio": 0.30,  # Medium alert
                },
            }
        )

        alerts = self.alert_system.generate_alerts(problem_data)

        # Should have multiple alerts
        self.assertGreater(len(alerts), 1)

        # Critical alerts should come first
        critical_alerts = [a for a in alerts if a.severity == AlertSeverity.CRITICAL]
        medium_alerts = [a for a in alerts if a.severity == AlertSeverity.MEDIUM]

        self.assertGreater(len(critical_alerts), 0)
        self.assertGreater(len(medium_alerts), 0)

        # First alerts should be critical
        for i in range(len(critical_alerts)):
            self.assertEqual(alerts[i].severity, AlertSeverity.CRITICAL)

    def test_stakeholder_specific_filtering(self):
        """Test filtering alerts for specific stakeholders."""
        problem_data = self.normal_data.copy()
        problem_data.update(
            {
                "risk_indicators": {
                    "blocked_issues": 4,  # VP Engineering + CEO
                    "security_vulnerabilities": 1,  # CEO + VP Engineering
                    "overdue_issues": 2,
                    "critical_bugs": 0,
                },
                "team_health": {
                    "overall_score": 65,  # VP Engineering only
                    "technical_debt_ratio": 0.15,
                },
            }
        )

        all_alerts = self.alert_system.generate_alerts(problem_data)

        # Test CEO filtering
        ceo_alerts = self.alert_system.get_stakeholder_alerts(
            StakeholderType.CEO, problem_data
        )
        for alert in ceo_alerts:
            self.assertIn(StakeholderType.CEO, alert.stakeholders)

        # Test VP Engineering filtering
        vp_alerts = self.alert_system.get_stakeholder_alerts(
            StakeholderType.VP_ENGINEERING, problem_data
        )
        for alert in vp_alerts:
            self.assertIn(StakeholderType.VP_ENGINEERING, alert.stakeholders)

        # VP Engineering should have more alerts (including team health)
        self.assertGreaterEqual(len(vp_alerts), len(ceo_alerts))

    def test_alert_cooldown_mechanism(self):
        """Test that alert cooldown prevents spam."""
        problem_data = self.normal_data.copy()
        problem_data["risk_indicators"] = {
            "blocked_issues": 4,  # Triggers alert
            "overdue_issues": 2,
            "critical_bugs": 0,
            "security_vulnerabilities": 0,
        }

        # First alert generation should work
        alerts1 = self.alert_system.generate_alerts(problem_data)
        blocked_alerts1 = [
            a
            for a in alerts1
            if "blocker" in a.title.lower() or "delivery" in a.title.lower()
        ]
        self.assertGreater(len(blocked_alerts1), 0)

        # Second alert generation should be blocked by cooldown
        alerts2 = self.alert_system.generate_alerts(problem_data)
        blocked_alerts2 = [
            a
            for a in alerts2
            if "blocker" in a.title.lower() or "delivery" in a.title.lower()
        ]
        self.assertEqual(len(blocked_alerts2), 0)  # Should be in cooldown

        # Verify cooldown tracking
        self.assertIn("critical_blocked_issues", self.alert_system.cooldown_tracker)

    def test_cli_formatting_no_alerts(self):
        """Test CLI formatting when no alerts are active."""
        formatted = self.alert_system.format_alerts_for_cli([])
        self.assertIn("No active alerts", formatted)
        self.assertIn("all systems operating normally", formatted)

    def test_cli_formatting_with_alerts(self):
        """Test CLI formatting with active alerts."""
        problem_data = self.normal_data.copy()
        problem_data.update(
            {
                "risk_indicators": {
                    "blocked_issues": 4,  # Critical
                    "security_vulnerabilities": 1,  # Critical
                    "overdue_issues": 2,
                    "critical_bugs": 0,
                },
                "team_health": {
                    "overall_score": 65,  # Medium
                    "technical_debt_ratio": 0.30,  # Medium
                },
            }
        )

        alerts = self.alert_system.generate_alerts(problem_data)
        formatted = self.alert_system.format_alerts_for_cli(alerts)

        # Should contain proper sections
        self.assertIn("ACTIVE ALERTS", formatted)
        self.assertIn("CRITICAL ALERTS", formatted)
        self.assertIn("MEDIUM PRIORITY ALERTS", formatted)
        self.assertIn("SUMMARY", formatted)
        self.assertIn("NEXT ACTIONS", formatted)

        # Should contain alert content
        self.assertIn("blocked issues", formatted)
        self.assertIn("security vulnerabilities", formatted)

        # Should contain actionable items
        self.assertIn("Actions:", formatted)

        # Should contain CLI command suggestions
        self.assertIn("./claudedirector", formatted)

    def test_alert_channels(self):
        """Test available alert channels."""
        channels = self.alert_system.get_alert_channels()

        expected_channels = ["cli", "email", "slack", "dashboard"]
        for channel in expected_channels:
            self.assertIn(channel, channels)

    def test_alert_rule_initialization(self):
        """Test that alert rules are properly initialized."""
        rules = self.alert_system.alert_rules

        # Should have multiple rules
        self.assertGreater(len(rules), 5)

        # Check specific rules exist
        rule_names = [rule.name for rule in rules]
        expected_rules = [
            "critical_blocked_issues",
            "velocity_crash",
            "initiative_at_risk",
            "team_health_degrading",
            "technical_debt_spike",
            "security_vulnerabilities",
            "delivery_predictability_drop",
        ]

        for expected_rule in expected_rules:
            self.assertIn(expected_rule, rule_names)

        # Verify rule properties
        for rule in rules:
            self.assertIsInstance(rule.name, str)
            self.assertIsInstance(rule.category, AlertCategory)
            self.assertIsInstance(rule.severity, AlertSeverity)
            self.assertIsInstance(rule.stakeholders, list)
            self.assertGreater(len(rule.stakeholders), 0)
            self.assertIsInstance(rule.condition_func, str)
            self.assertGreater(rule.cooldown_hours, 0)
            self.assertIsInstance(rule.enabled, bool)

    def test_alert_context_and_metadata(self):
        """Test that alerts contain proper context and metadata."""
        problem_data = self.normal_data.copy()
        problem_data["risk_indicators"] = {
            "blocked_issues": 4,
            "critical_bugs": 2,
            "overdue_issues": 2,
            "security_vulnerabilities": 0,
        }

        alerts = self.alert_system.generate_alerts(problem_data)
        blocked_alert = next(
            a
            for a in alerts
            if "blocker" in a.title.lower() or "delivery" in a.title.lower()
        )

        # Verify alert structure
        self.assertIsNotNone(blocked_alert.id)
        self.assertIsNotNone(blocked_alert.title)
        self.assertIsNotNone(blocked_alert.message)
        self.assertIsInstance(blocked_alert.created_at, datetime)
        self.assertIsInstance(blocked_alert.context, dict)
        self.assertIsInstance(blocked_alert.actionable_items, list)
        self.assertIsInstance(blocked_alert.confidence_score, float)

        # Verify context contains relevant data
        self.assertIn("blocked_issues", blocked_alert.context)
        self.assertIn("critical_bugs", blocked_alert.context)

        # Verify actionable items are provided
        self.assertGreater(len(blocked_alert.actionable_items), 0)
        for item in blocked_alert.actionable_items:
            self.assertIsInstance(item, str)
            self.assertGreater(len(item), 10)  # Should be meaningful text


if __name__ == "__main__":
    unittest.main()
