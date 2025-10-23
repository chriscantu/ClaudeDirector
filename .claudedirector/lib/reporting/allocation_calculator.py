"""
Allocation Calculator - Team L0/L1/L2 Work Distribution

BLOAT_PREVENTION: Reuses existing JiraClient and TeamAllocation
Phase: TDD GREEN (stub implementation - tests still failing)

This module calculates team allocation percentages across:
- L0: Keep-the-lights-on work (support, operational, compliance)
- L1: Work enabling L2 initiatives
- L2: Strategic initiatives
- Other: Unclassified work

Cross-Project Hierarchy:
Story → Team Epic → Strategic Initiative (L0/L1/L2)
"""

from datetime import datetime
from typing import Dict, List, Optional
from lib.reporting.jira_reporter import JiraClient
from lib.reporting.allocation_models import TeamAllocation


class AllocationCalculator:
    """
    Calculate team allocation percentages across L0/L1/L2 work

    TDD Status: STUB - Tests written, implementation in progress

    Usage:
    ```python
    calculator = AllocationCalculator(
        jira_client=jira_client,
        start_date=datetime(2025, 1, 1),
        end_date=datetime(2025, 3, 31)
    )

    allocation = calculator.calculate_team_allocation(
        team_name="Platform Team",
        jira_project="WEB"
    )
    ```
    """

    def __init__(
        self, jira_client: JiraClient, start_date: datetime, end_date: datetime
    ):
        """
        Initialize allocation calculator

        Args:
            jira_client: JiraClient instance for API access
            start_date: Start of allocation period
            end_date: End of allocation period
        """
        self.jira_client = jira_client
        self.start_date = start_date
        self.end_date = end_date

    def calculate_team_allocation(
        self, team_name: str, jira_project: str
    ) -> TeamAllocation:
        """
        Calculate team allocation for the period

        Args:
            team_name: Name of the team
            jira_project: Jira project key (e.g., "WEB")

        Returns:
            TeamAllocation with L0/L1/L2/Other percentages
        """
        # TODO: Implement actual calculation
        # For now, return a stub to allow test collection
        return TeamAllocation(
            team_name=team_name,
            date_range=(self.start_date, self.end_date),
            l0_pct=0.0,
            l1_pct=0.0,
            l2_pct=0.0,
            other_pct=100.0,
            total_issues=0,
            l2_velocity_actual=0.0,
            l2_velocity_projected=0.0,
        )

    def classify_story(self, story_key: str) -> str:
        """
        Classify a story as L0/L1/L2/Other based on parent hierarchy

        Args:
            story_key: Jira story key (e.g., "WEB-1234")

        Returns:
            Classification: "L0", "L1", "L2", or "Other"
        """
        # TODO: Implement cross-project hierarchy traversal
        return "Other"

    def detect_initiative_level(self, initiative_key: str) -> str:
        """
        Detect L0/L1/L2 level from initiative

        Detection methods:
        1. Summary prefix: "L0:", "L1:", "L2:"
        2. Labels: ["L0"], ["L1"], ["L2"]

        Args:
            initiative_key: Initiative key (e.g., "PI-14632")

        Returns:
            Level: "L0", "L1", "L2", or "Strategic"
        """
        # TODO: Implement initiative level detection
        return "Strategic"
