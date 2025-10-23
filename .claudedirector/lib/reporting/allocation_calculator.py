"""
Allocation Calculator - Team L0/L1/L2 Work Distribution

BLOAT_PREVENTION: Reuses existing JiraClient and TeamAllocation
Phase: TDD GREEN (full implementation)

This module calculates team allocation percentages across:
- L0: Keep-the-lights-on work (support, operational, compliance)
- L1: Work enabling L2 initiatives
- L2: Strategic initiatives
- Other: Unclassified work

Cross-Project Hierarchy:
Story → Team Epic → Strategic Initiative (L0/L1/L2)

Context7 Patterns Applied:
- Google SRE "Toil Tracking": Measure operational overhead
- Spotify "Innovation Time": Quantify strategic vs. maintenance split
- Industry Standard: 60-70% strategic, 30-40% operational target
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from lib.reporting.jira_reporter import JiraClient, JiraIssue
from lib.reporting.allocation_models import TeamAllocation
import logging

logger = logging.getLogger(__name__)


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
        self._cached_issues: Optional[List[Dict]] = None  # Cache for test lookups

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
        # Fetch completed work items for the team in the date range
        days_back = (self.end_date - self.start_date).days
        jql = f'project = "{jira_project}" AND type != Epic AND status = Done AND status CHANGED TO Done AFTER -{days_back}d'

        try:
            raw_issues = self.jira_client.fetch_issues(jql, max_results=1000)
            self._cached_issues = raw_issues  # Cache for classify_story lookups
        except Exception as e:
            logger.warning(f"Failed to fetch issues for {jira_project}: {e}")
            raw_issues = []
            self._cached_issues = []

        # Classify each story
        l0_count = 0
        l1_count = 0
        l2_count = 0
        other_count = 0
        l2_stories = []

        for raw_issue in raw_issues:
            issue_key = raw_issue.get("key", "")
            classification = self.classify_story(issue_key, raw_issue)

            if classification == "L0":
                l0_count += 1
            elif classification == "L1":
                l1_count += 1
            elif classification == "L2":
                l2_count += 1
                l2_stories.append(raw_issue)
            else:
                other_count += 1

        total_issues = len(raw_issues)

        # Calculate percentages
        if total_issues > 0:
            l0_pct = (l0_count / total_issues) * 100
            l1_pct = (l1_count / total_issues) * 100
            l2_pct = (l2_count / total_issues) * 100
            other_pct = (other_count / total_issues) * 100
        else:
            # Edge case: no stories - set Other to 100%
            l0_pct = 0.0
            l1_pct = 0.0
            l2_pct = 0.0
            other_pct = 100.0

        # Round percentages to 1 decimal place
        l0_pct = round(l0_pct, 1)
        l1_pct = round(l1_pct, 1)
        l2_pct = round(l2_pct, 1)
        other_pct = round(other_pct, 1)

        # Normalize to ensure exactly 100% (handle rounding errors)
        total_pct = l0_pct + l1_pct + l2_pct + other_pct
        if abs(total_pct - 100.0) > 0.01 and total_issues > 0:
            # Adjust the largest percentage to make total exactly 100%
            diff = 100.0 - total_pct
            if other_pct >= max(l0_pct, l1_pct, l2_pct):
                other_pct = round(other_pct + diff, 1)
            elif l2_pct >= max(l0_pct, l1_pct, other_pct):
                l2_pct = round(l2_pct + diff, 1)
            elif l1_pct >= max(l0_pct, l2_pct, other_pct):
                l1_pct = round(l1_pct + diff, 1)
            else:
                l0_pct = round(l0_pct + diff, 1)

        # Calculate L2 velocity (stories per week)
        weeks = days_back / 7.0
        l2_velocity_actual = len(l2_stories) / weeks if weeks > 0 else 0.0

        # Projected L2 velocity (baseline expectation based on industry standards)
        # Context7 Pattern: Google SRE targets <50% toil, Spotify 70-80% innovation time
        # Baseline assumption: 30% L0 is "normal", actual is compared to this baseline
        l2_velocity_projected = l2_velocity_actual

        if l2_velocity_actual > 0:
            # Calculate what velocity WOULD be at 30% L0 (industry baseline)
            # If L0 < 30%: team is operating above baseline → projected < actual
            # If L0 > 30%: team is burdened → projected > actual
            baseline_l0 = 30.0
            l0_delta = l0_pct - baseline_l0

            if (
                abs(l0_delta) > 1.0
            ):  # Only adjust if significantly different from baseline
                # For every 10% deviation from baseline L0, assume 20% velocity impact
                # Context7: High L0 burden (60%+) can reduce strategic velocity by 60-70%
                velocity_adjustment = (l0_delta / 10.0) * 0.20
                l2_velocity_projected = l2_velocity_actual / (1.0 - velocity_adjustment)

        return TeamAllocation(
            team_name=team_name,
            date_range=(self.start_date, self.end_date),
            l0_pct=l0_pct,  # Already rounded above
            l1_pct=l1_pct,  # Already rounded above
            l2_pct=l2_pct,  # Already rounded above
            other_pct=other_pct,  # Already rounded above
            total_issues=total_issues,
            l2_velocity_actual=round(l2_velocity_actual, 2),
            l2_velocity_projected=round(l2_velocity_projected, 2),
        )

    def classify_story(self, story_key: str, raw_issue: Optional[Dict] = None) -> str:
        """
        Classify a story as L0/L1/L2/Other based on parent hierarchy

        Cross-Project Hierarchy Traversal:
        1. Story → parent field → Epic key
        2. Epic → parent field → Initiative key (in "Procore Initiatives" project)
        3. Initiative summary → "L0:", "L1:", "L2:" prefix detection

        Context7 Pattern: Multi-level parent traversal for strategic classification

        Args:
            story_key: Jira story key (e.g., "WEB-1234")
            raw_issue: Optional raw Jira issue data (for efficiency)

        Returns:
            Classification: "L0", "L1", "L2", or "Other"
        """
        # If no raw_issue provided, look up from cache
        if not raw_issue and self._cached_issues:
            for issue in self._cached_issues:
                if issue.get("key") == story_key:
                    raw_issue = issue
                    break

        if not raw_issue:
            return "Other"

        fields = raw_issue.get("fields", {})
        parent = fields.get("parent", {})

        if not parent:
            # No parent epic - classified as "Other"
            return "Other"

        parent_key = parent.get("key", "")
        parent_fields = parent.get("fields", {})
        parent_summary = parent_fields.get("summary", "")

        # Check if parent epic itself has L0/L1/L2 markers
        epic_level = self.detect_initiative_level_from_summary(parent_summary)
        if epic_level in ["L0", "L1", "L2"]:
            return epic_level

        # Check epic's parent (strategic initiative in cross-project)
        epic_parent = parent_fields.get("parent", {})
        if epic_parent:
            initiative_key = epic_parent.get("key", "")
            initiative_fields = epic_parent.get("fields", {})
            initiative_summary = initiative_fields.get("summary", "")

            # Detect initiative level from summary or labels
            initiative_level = self.detect_initiative_level_from_summary(
                initiative_summary
            )
            if initiative_level in ["L0", "L1", "L2"]:
                return initiative_level

            # Check labels as fallback
            initiative_labels = initiative_fields.get("labels", [])
            for label in initiative_labels:
                if label.upper() in ["L0", "L1", "L2"]:
                    return label.upper()

        # No strategic classification found
        return "Other"

    def detect_initiative_level(self, initiative_key: str) -> str:
        """
        Detect L0/L1/L2 level from initiative by looking up in cached issues

        This method looks up the initiative in the cached issues and detects
        its level from the summary or labels.

        Args:
            initiative_key: Initiative key (e.g., "PI-14632")

        Returns:
            Level: "L0", "L1", "L2", or "Strategic"
        """
        if not self._cached_issues:
            return "Strategic"

        # Look for the initiative in cached issues
        # It might be a parent of a parent (nested hierarchy)
        for issue in self._cached_issues:
            fields = issue.get("fields", {})
            parent = fields.get("parent", {})

            if parent.get("key") == initiative_key:
                # Found as direct parent
                parent_fields = parent.get("fields", {})
                summary = parent_fields.get("summary", "")
                labels = parent_fields.get("labels", [])

                level = self.detect_initiative_level_from_summary(summary)
                if level in ["L0", "L1", "L2"]:
                    return level

                # Check labels
                for label in labels:
                    if label.upper() in ["L0", "L1", "L2"]:
                        return label.upper()

            # Check if it's a parent's parent (epic's parent = initiative)
            if parent:
                parent_fields = parent.get("fields", {})
                epic_parent = parent_fields.get("parent", {})

                if epic_parent.get("key") == initiative_key:
                    initiative_fields = epic_parent.get("fields", {})
                    summary = initiative_fields.get("summary", "")
                    labels = initiative_fields.get("labels", [])

                    level = self.detect_initiative_level_from_summary(summary)
                    if level in ["L0", "L1", "L2"]:
                        return level

                    # Check labels
                    for label in labels:
                        if label.upper() in ["L0", "L1", "L2"]:
                            return label.upper()

        return "Strategic"

    def detect_initiative_level_from_summary(self, summary: str) -> str:
        """
        Detect L0/L1/L2 level from initiative summary

        BLOAT_PREVENTION: Reuses detection logic from StrategicAnalyzer pattern

        Detection methods:
        1. Explicit prefix: "L0:", "L1:", "L2:"
        2. Layer notation: "Layer 0", "Layer 1", "Layer 2"
        3. Keyword inference: compliance keywords → L0, platform keywords → L2

        Context7 Pattern: Industry-standard initiative classification

        Args:
            summary: Initiative or epic summary text

        Returns:
            Level: "L0", "L1", "L2", or "Strategic"
        """
        if not summary:
            return "Strategic"

        # Explicit prefix detection
        if "L0:" in summary or "Layer 0" in summary:
            return "L0"
        elif "L2:" in summary or "Layer 2" in summary:
            return "L2"
        elif "L1:" in summary or "Layer 1" in summary:
            return "L1"

        # Keyword-based inference (Context7 pattern)
        compliance_keywords = [
            "compliance",
            "security",
            "audit",
            "risk",
            "regulatory",
            "certification",
            "fedramp",
            "soc2",
        ]
        platform_keywords = [
            "platform",
            "v1",
            "v2",
            "developer",
            "build",
            "tool",
            "capability",
            "strategic",
        ]

        summary_lower = summary.lower()

        if any(keyword in summary_lower for keyword in compliance_keywords):
            return "L0"
        elif any(keyword in summary_lower for keyword in platform_keywords):
            return "L2"

        return "Strategic"
