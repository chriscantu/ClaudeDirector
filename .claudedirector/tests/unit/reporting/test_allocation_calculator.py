"""
Unit Tests: Allocation Calculator

TDD Phase: RED (write tests first, then implement calculator)

Test Coverage:
- Cross-project hierarchy traversal (Story → Epic → L0/L1/L2 Initiative)
- L0/L1/L2 classification based on parent epic labels
- Percentage calculation (must sum to 100%)
- Edge cases: empty data, all L0, orphaned stories
- Velocity impact calculation
"""

import pytest
from datetime import datetime, timedelta
from typing import List, Dict


class TestAllocationCalculatorBasics:
    """
    TDD RED: Test AllocationCalculator before implementation

    Requirements from Context7:
    - Cross-project parent-child traversal
    - Percentage normalization (sum to 100%)
    - L0/L1/L2 detection through parent epic links
    - Handle edge cases gracefully
    """

    def test_calculator_creation_with_jira_client(self):
        """AllocationCalculator should accept JiraClient and date range"""
        from lib.reporting.allocation_calculator import AllocationCalculator
        from lib.reporting.jira_reporter import JiraClient
        from unittest.mock import MagicMock

        # Mock JiraClient (don't need real config in tests)
        jira_client = MagicMock(spec=JiraClient)

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        calculator = AllocationCalculator(
            jira_client=jira_client, start_date=start_date, end_date=end_date
        )

        assert calculator.start_date == start_date
        assert calculator.end_date == end_date
        assert calculator.jira_client is not None

    def test_calculate_team_allocation_returns_team_allocation_object(self):
        """Calculator should return TeamAllocation with percentages summing to 100%"""
        from lib.reporting.allocation_calculator import AllocationCalculator
        from lib.reporting.allocation_models import TeamAllocation

        # Mock calculator with test data
        calculator = self._create_mock_calculator()

        allocation = calculator.calculate_team_allocation(
            team_name="Platform Team", jira_project="WEB"
        )

        assert isinstance(allocation, TeamAllocation)
        assert allocation.team_name == "Platform Team"
        assert 99.9 <= allocation.total_percentage <= 100.1  # Sum to 100%

    def test_allocation_with_known_distribution(self):
        """
        Test allocation calculation with known L0/L1/L2 distribution

        Scenario: 10 stories completed
        - 3 stories linked to L0 epic (30%)
        - 2 stories linked to L1 epic (20%)
        - 4 stories linked to L2 epic (40%)
        - 1 story with no parent (10% - Other)

        Expected: L0=30%, L1=20%, L2=40%, Other=10%
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_test_data(
            l0_stories=3, l1_stories=2, l2_stories=4, other_stories=1
        )

        allocation = calculator.calculate_team_allocation(
            team_name="Platform Team", jira_project="WEB"
        )

        assert allocation.l0_pct == pytest.approx(30.0, abs=0.1)
        assert allocation.l1_pct == pytest.approx(20.0, abs=0.1)
        assert allocation.l2_pct == pytest.approx(40.0, abs=0.1)
        assert allocation.other_pct == pytest.approx(10.0, abs=0.1)
        assert allocation.total_issues == 10

    def test_allocation_all_l0_work(self):
        """
        Edge case: All stories are L0 (support/operational work)

        Expected: L0=100%, L1=0%, L2=0%, Other=0%
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_test_data(
            l0_stories=10, l1_stories=0, l2_stories=0, other_stories=0
        )

        allocation = calculator.calculate_team_allocation(
            team_name="Support Team", jira_project="WEB"
        )

        assert allocation.l0_pct == 100.0
        assert allocation.l1_pct == 0.0
        assert allocation.l2_pct == 0.0
        assert allocation.other_pct == 0.0

    def test_allocation_with_no_completed_stories(self):
        """
        Edge case: No completed stories in the period

        Expected: All percentages 0%, but still valid TeamAllocation
        Should set Other=100% to ensure sum is 100%
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_test_data(
            l0_stories=0, l1_stories=0, l2_stories=0, other_stories=0
        )

        allocation = calculator.calculate_team_allocation(
            team_name="Idle Team", jira_project="WEB"
        )

        assert allocation.total_issues == 0
        assert allocation.total_percentage == 100.0  # Must still sum to 100%
        # When no data, Other should be 100% (or all zeros with special handling)

    def test_percentage_normalization_ensures_100_percent(self):
        """
        Percentages must always sum to exactly 100%

        Test with floating point edge case: 3 stories should be 33.33%, 33.33%, 33.34%
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_test_data(
            l0_stories=1, l1_stories=1, l2_stories=1, other_stories=0
        )

        allocation = calculator.calculate_team_allocation(
            team_name="Platform Team", jira_project="WEB"
        )

        # Regardless of rounding, total must be 100%
        assert allocation.total_percentage == pytest.approx(100.0, abs=0.01)

    # Helper methods for creating test data
    def _create_mock_calculator(self):
        """Create a mock calculator for basic testing"""
        from lib.reporting.allocation_calculator import AllocationCalculator
        from lib.reporting.jira_reporter import JiraClient
        from unittest.mock import MagicMock

        jira_client = MagicMock(spec=JiraClient)
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        return AllocationCalculator(
            jira_client=jira_client, start_date=start_date, end_date=end_date
        )

    def _create_calculator_with_test_data(
        self, l0_stories: int, l1_stories: int, l2_stories: int, other_stories: int
    ):
        """Create calculator pre-populated with test data"""
        # For TDD RED phase, just return a mock calculator
        # GREEN phase will implement actual test data population
        return self._create_mock_calculator()


class TestCrossProjectHierarchyTraversal:
    """
    Test cross-project parent-child relationship traversal

    Critical Discovery from Spec:
    - L0/L1/L2 initiatives live in "Procore Initiatives" project
    - Team epics live in team projects (e.g., "Web Platform")
    - Stories link to team epics, team epics link to strategic initiatives

    Traversal pattern:
    Story (WEB-1234) → Epic (WEB-1000) → Initiative (PI-14632 in "Procore Initiatives")
    """

    def test_detect_l0_from_cross_project_parent(self):
        """
        Story → Team Epic → L0 Initiative (cross-project)

        Example:
        WEB-1234 (Story) → parent: WEB-1000 (Epic) → parent: PI-14632 (L0: FedRAMP)

        Expected: Story classified as L0
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_cross_project_data()

        # Mock story with cross-project L0 parent
        story_key = "WEB-1234"
        classification = calculator.classify_story(story_key)

        assert classification == "L0"

    def test_detect_l2_from_cross_project_parent(self):
        """
        Story → Team Epic → L2 Initiative (cross-project)

        Example:
        WEB-5678 (Story) → parent: WEB-2000 (Epic) → parent: PI-20000 (L2: Platform v2)

        Expected: Story classified as L2
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_cross_project_data()

        story_key = "WEB-5678"
        classification = calculator.classify_story(story_key)

        assert classification == "L2"

    def test_detect_l1_enabling_work(self):
        """
        L1 work enables L2 initiatives

        Example:
        WEB-3000 (Story) → parent: WEB-1500 (Epic) → parent: PI-15000 (L1: Enabling Platform v2)

        Expected: Story classified as L1
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_cross_project_data()

        story_key = "WEB-3000"
        classification = calculator.classify_story(story_key)

        assert classification == "L1"

    def test_orphaned_story_without_parent_epic(self):
        """
        Story with no parent epic → classified as "Other"

        Example:
        WEB-9999 (Story) → parent: None

        Expected: Story classified as Other
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_cross_project_data()

        story_key = "WEB-9999"  # Orphaned story
        classification = calculator.classify_story(story_key)

        assert classification == "Other"

    def test_epic_without_strategic_parent_defaults_to_other(self):
        """
        Story → Team Epic (no L0/L1/L2 parent) → classified as "Other"

        Example:
        WEB-4000 (Story) → parent: WEB-3000 (Epic with no strategic parent)

        Expected: Story classified as Other
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_cross_project_data()

        story_key = "WEB-4000"
        classification = calculator.classify_story(story_key)

        assert classification == "Other"

    def test_classification_uses_initiative_summary_l0_prefix(self):
        """
        L0/L1/L2 detection using "L0:", "L1:", "L2:" prefix in initiative summary

        Example:
        Initiative PI-14632 summary: "L0: FedRAMP Compliance Follow-up"

        Expected: Detected as L0
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_cross_project_data()

        initiative_key = "PI-14632"
        level = calculator.detect_initiative_level(initiative_key)

        assert level == "L0"

    def test_classification_uses_initiative_labels(self):
        """
        Fallback: L0/L1/L2 detection using labels if no prefix in summary

        Example:
        Initiative PI-20000 labels: ["L2", "platform", "strategic"]

        Expected: Detected as L2
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_cross_project_data()

        initiative_key = "PI-20000"
        level = calculator.detect_initiative_level(initiative_key)

        assert level == "L2"

    # Helper methods
    def _create_calculator_with_cross_project_data(self):
        """Create calculator with mock cross-project hierarchy"""
        from lib.reporting.allocation_calculator import AllocationCalculator
        from lib.reporting.jira_reporter import JiraClient
        from unittest.mock import MagicMock

        jira_client = MagicMock(spec=JiraClient)
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        return AllocationCalculator(
            jira_client=jira_client, start_date=start_date, end_date=end_date
        )


class TestVelocityImpactCalculation:
    """
    Test velocity impact calculation

    Formula: ((actual_l2_velocity - projected_l2_velocity) / projected_l2_velocity) * 100

    Context7 Pattern: Support burden (high L0%) typically correlates with low L2 velocity
    """

    def test_velocity_impact_with_high_l0_burden(self):
        """
        High L0 work (60%) should show negative velocity impact

        Scenario:
        - L0: 60% (high support burden)
        - L2: 20% (low strategic work)
        - Projected L2 velocity: 10 stories/week
        - Actual L2 velocity: 3 stories/week

        Expected: velocity_impact ≈ -70% (significant degradation)
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_velocity_data(
            l0_pct=60.0, l2_pct=20.0, projected_velocity=10.0, actual_velocity=3.0
        )

        allocation = calculator.calculate_team_allocation(
            team_name="Burdened Team", jira_project="WEB"
        )

        assert allocation.velocity_impact < -60.0  # Significant negative impact
        assert allocation.l0_pct == 60.0

    def test_velocity_impact_with_healthy_l2_allocation(self):
        """
        Healthy L2 allocation (50%) should show positive or neutral velocity

        Scenario:
        - L0: 20% (manageable support)
        - L2: 50% (healthy strategic work)
        - Projected L2 velocity: 8 stories/week
        - Actual L2 velocity: 9 stories/week

        Expected: velocity_impact ≈ +12.5% (exceeding projections)
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_velocity_data(
            l0_pct=20.0, l2_pct=50.0, projected_velocity=8.0, actual_velocity=9.0
        )

        allocation = calculator.calculate_team_allocation(
            team_name="Healthy Team", jira_project="WEB"
        )

        assert allocation.velocity_impact > 0  # Positive impact
        assert allocation.l2_pct == 50.0

    def test_velocity_calculation_from_completed_l2_stories(self):
        """
        Actual L2 velocity calculated from completed L2 stories in period

        Scenario: 90-day period (13 weeks), 26 L2 stories completed

        Expected: actual_l2_velocity = 26 / 13 = 2.0 stories/week
        """
        from lib.reporting.allocation_calculator import AllocationCalculator

        calculator = self._create_calculator_with_l2_stories(
            l2_story_count=26, period_days=90
        )

        allocation = calculator.calculate_team_allocation(
            team_name="Platform Team", jira_project="WEB"
        )

        # 90 days ≈ 13 weeks, 26 stories / 13 weeks ≈ 2.0 stories/week
        assert allocation.l2_velocity_actual == pytest.approx(2.0, abs=0.1)

    # Helper methods
    def _create_calculator_with_velocity_data(
        self,
        l0_pct: float,
        l2_pct: float,
        projected_velocity: float,
        actual_velocity: float,
    ):
        """Create calculator with mock velocity data"""
        from lib.reporting.allocation_calculator import AllocationCalculator
        from lib.reporting.jira_reporter import JiraClient
        from unittest.mock import MagicMock

        jira_client = MagicMock(spec=JiraClient)
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        return AllocationCalculator(
            jira_client=jira_client, start_date=start_date, end_date=end_date
        )

    def _create_calculator_with_l2_stories(self, l2_story_count: int, period_days: int):
        """Create calculator with mock L2 stories for velocity calculation"""
        from lib.reporting.allocation_calculator import AllocationCalculator
        from lib.reporting.jira_reporter import JiraClient
        from unittest.mock import MagicMock

        jira_client = MagicMock(spec=JiraClient)
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 1) + timedelta(days=period_days)

        return AllocationCalculator(
            jira_client=jira_client, start_date=start_date, end_date=end_date
        )


class TestBLOATPrevention:
    """
    Ensure AllocationCalculator doesn't duplicate existing logic
    """

    def test_allocation_calculator_reuses_jira_client(self):
        """AllocationCalculator should reuse JiraClient, not duplicate API logic"""
        from lib.reporting.allocation_calculator import AllocationCalculator
        from lib.reporting.jira_reporter import JiraClient

        # Verify AllocationCalculator accepts JiraClient instance
        # This ensures we're not duplicating Jira API logic
        import inspect

        init_signature = inspect.signature(AllocationCalculator.__init__)
        params = list(init_signature.parameters.keys())

        assert "jira_client" in params, "AllocationCalculator should accept JiraClient"

    def test_allocation_calculator_returns_team_allocation_dataclass(self):
        """AllocationCalculator should return existing TeamAllocation, not new class"""
        from lib.reporting.allocation_calculator import AllocationCalculator
        from lib.reporting.allocation_models import TeamAllocation

        # Verify return type uses existing TeamAllocation dataclass
        # This ensures we're not creating duplicate data models
        import inspect

        calc_method = AllocationCalculator.calculate_team_allocation
        return_annotation = inspect.signature(calc_method).return_annotation

        # Should return TeamAllocation (might be string annotation)
        assert "TeamAllocation" in str(return_annotation)
