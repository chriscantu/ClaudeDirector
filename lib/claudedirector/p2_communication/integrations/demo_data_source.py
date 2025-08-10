"""
Demo Data Source

Provides sample data for testing P2.1 features when JIRA is unavailable.
Simulates realistic JIRA data patterns for development and demonstration.
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

from ..interfaces.report_interface import IDataSource


class DemoDataSource(IDataSource):
    """
    Demo data source for P2.1 testing and development.

    Provides realistic sample data when JIRA integration is unavailable.
    Useful for development, testing, and demonstrations.
    """

    def __init__(self):
        self.last_update = datetime.now()
        self._demo_data = self._generate_demo_data()

    def get_data(self, time_period: str, metrics: List[str]) -> Dict[str, Any]:
        """Get demo data for specified time period and metrics."""
        # Simulate slight data variation
        self._update_demo_data()

        # Filter data based on requested metrics
        filtered_data = {}
        for metric in metrics:
            if metric in self._demo_data:
                filtered_data[metric] = self._demo_data[metric]

        # Always include core demo data
        for key in [
            "team_velocity",
            "risk_indicators",
            "initiative_health",
            "cross_team_dependencies",
        ]:
            if key not in filtered_data:
                filtered_data[key] = self._demo_data[key]

        # Add metadata
        filtered_data["data_freshness"] = self.last_update.strftime("%Y-%m-%d %H:%M:%S")
        filtered_data["time_period"] = time_period
        filtered_data["metrics_requested"] = metrics
        filtered_data["data_source"] = "demo"

        return filtered_data

    def get_data_freshness(self) -> str:
        """Return timestamp of when data was last updated."""
        return self.last_update.strftime("%Y-%m-%d %H:%M:%S")

    def is_available(self) -> bool:
        """Demo data source is always available."""
        return True

    def _generate_demo_data(self) -> Dict[str, Any]:
        """Generate realistic demo data."""
        return {
            "team_velocity": {
                "current_sprint": 42,
                "last_sprint": 38,
                "average_last_5": 40,
                "trend": "increasing",
                "velocity_variance": 0.15,
                "sprint_commitment_accuracy": 0.85,
            },
            "risk_indicators": {
                "blocked_issues": 4,  # Trigger critical alert (>= 3)
                "overdue_issues": 6,
                "critical_bugs": 2,  # Trigger critical alert (>= 2)
                "security_vulnerabilities": 1,  # Trigger security alert (> 0)
                "technical_debt_items": 12,
                "dependency_risks": 2,
            },
            "initiative_health": {
                "on_track": 8,
                "at_risk": 2,
                "critical": 1,
                "completed_this_quarter": 5,
                "total_initiatives": 11,
            },
            "cross_team_dependencies": {
                "total_dependencies": 12,
                "blocked_dependencies": 2,
                "at_risk_dependencies": 3,
                "resolved_this_week": 4,
                "dependency_resolution_time_avg": "3.2 days",
            },
            "team_health": {
                "overall_score": 65,  # Trigger team health alert (< 70)
                "velocity_consistency": 75,
                "quality_metrics": 68,
                "collaboration_score": 78,
                "technical_debt_ratio": 0.28,  # Trigger tech debt alert (> 0.25)
            },
            "delivery_metrics": {
                "stories_completed": 15,
                "defect_rate": 0.08,
                "cycle_time_avg": "4.2 days",
                "lead_time_avg": "8.1 days",
                "deployment_frequency": "2.3 per week",
            },
            "quality_indicators": {
                "code_coverage": 0.86,
                "automated_test_success_rate": 0.94,
                "production_incidents": 1,
                "customer_reported_bugs": 2,
                "security_scan_score": 0.96,
            },
            "business_impact": {
                "feature_adoption_rate": 0.73,
                "user_satisfaction_score": 4.2,
                "platform_performance_score": 0.91,
                "cost_per_feature": "$12,400",
                "roi_estimate": "280%",
            },
            "strategic_alignment": {
                "okr_completion_rate": 0.67,
                "strategic_initiative_progress": 0.74,
                "innovation_pipeline_health": 0.82,
                "competitive_advantage_score": 0.88,
            },
        }

    def _update_demo_data(self):
        """Simulate slight variations in demo data to make it feel live."""
        # Update timestamp
        self.last_update = datetime.now()

        # Add small random variations to make data feel dynamic
        velocity_change = random.randint(-2, 3)
        self._demo_data["team_velocity"]["current_sprint"] = max(
            35, self._demo_data["team_velocity"]["current_sprint"] + velocity_change
        )

        # Occasionally change trend
        if random.random() < 0.1:  # 10% chance
            trends = ["increasing", "stable", "decreasing"]
            self._demo_data["team_velocity"]["trend"] = random.choice(trends)

        # Simulate risk changes
        if random.random() < 0.2:  # 20% chance
            self._demo_data["risk_indicators"]["blocked_issues"] = random.randint(0, 4)
            self._demo_data["risk_indicators"]["overdue_issues"] = random.randint(0, 5)

        # Update health scores slightly
        health_change = random.randint(-2, 2)
        current_health = self._demo_data["team_health"]["overall_score"]
        self._demo_data["team_health"]["overall_score"] = max(
            70, min(95, current_health + health_change)
        )

    def get_velocity_data(self, team_id: str, sprints: int = 5) -> Dict[str, Any]:
        """Get velocity data for demo team."""
        base_data = self.get_data("velocity_demo", ["team_velocity"])

        # Add team-specific demo data
        base_data["team_id"] = team_id
        base_data["sprint_history"] = [
            {"sprint": f"Sprint {i}", "velocity": 35 + random.randint(-5, 10)}
            for i in range(sprints)
        ]

        return base_data

    def get_risk_indicators(self, project_keys: List[str]) -> Dict[str, Any]:
        """Get risk indicators for demo projects."""
        base_data = self.get_data("risk_demo", ["risk_indicators"])
        base_data["project_keys"] = project_keys

        return base_data

    def get_initiative_status(
        self, time_period: str = "current_quarter"
    ) -> Dict[str, Any]:
        """Get initiative status for demo."""
        base_data = self.get_data(
            time_period, ["initiative_health", "strategic_alignment"]
        )

        # Add detailed initiative demo data
        base_data["initiative_details"] = [
            {
                "name": "Design System V3",
                "status": "on_track",
                "progress": 0.78,
                "risk_level": "low",
                "team": "UI Foundation",
            },
            {
                "name": "Cross-Platform Authentication",
                "status": "at_risk",
                "progress": 0.45,
                "risk_level": "medium",
                "team": "Platform Security",
            },
            {
                "name": "Performance Optimization",
                "status": "on_track",
                "progress": 0.62,
                "risk_level": "low",
                "team": "Backend Services",
            },
        ]

        return base_data

    def get_demo_insights(self) -> List[str]:
        """Get demo insights for testing AI summary generation."""
        return [
            "Team velocity has increased 12% over the last 3 sprints",
            "Cross-team dependencies are resolving 15% faster than last quarter",
            "Technical debt ratio remains stable at healthy 12% of total codebase",
            "Design system adoption reached 85% across all product teams",
            "Security scan scores consistently above 95% for 8 consecutive weeks",
            "Feature delivery predictability improved to 85% commitment accuracy",
        ]
