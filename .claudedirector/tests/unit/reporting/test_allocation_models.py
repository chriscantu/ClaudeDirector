"""
Unit Tests: Team Allocation Data Models

TDD Phase: RED (write tests first, then implement models)

Test Coverage:
- TeamAllocation dataclass with percentage validation
- Allocation percentages must sum to 100% (±0.1% tolerance)
- Type hints for all fields
- ValueError raised for invalid percentages
- Helper properties and methods
"""

import pytest
from datetime import datetime
from dataclasses import fields


class TestTeamAllocationDataclass:
    """
    TDD RED: Test TeamAllocation dataclass before implementation

    Requirements:
    - Allocation percentages must sum to 100% (±0.1% tolerance)
    - Type hints for all fields
    - Validation in __post_init__
    - Helper properties for total_percentage, velocity_impact
    """

    def test_allocation_creation_with_valid_percentages(self):
        """Valid allocation should create successfully"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        allocation = TeamAllocation(
            team_name="Platform Team",
            date_range=(start_date, end_date),
            l0_pct=30.0,
            l1_pct=20.0,
            l2_pct=40.0,
            other_pct=10.0,
            total_issues=100,
            l2_velocity_actual=4.0,
            l2_velocity_projected=10.0,
        )

        assert allocation.team_name == "Platform Team"
        assert allocation.l0_pct == 30.0
        assert allocation.l1_pct == 20.0
        assert allocation.l2_pct == 40.0
        assert allocation.other_pct == 10.0
        assert allocation.total_issues == 100

    def test_allocation_percentages_sum_to_100(self):
        """Allocation percentages must sum to 100%"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        allocation = TeamAllocation(
            team_name="Platform Team",
            date_range=(start_date, end_date),
            l0_pct=30.0,
            l1_pct=20.0,
            l2_pct=40.0,
            other_pct=10.0,
            total_issues=100,
            l2_velocity_actual=4.0,
            l2_velocity_projected=10.0,
        )

        # Test total_percentage property
        total = allocation.total_percentage
        assert 99.9 <= total <= 100.1, f"Expected ~100%, got {total}%"

    def test_allocation_rejects_percentages_not_summing_to_100(self):
        """Should raise ValueError if percentages don't sum to 100%"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        # Test: percentages sum to 150% (invalid)
        with pytest.raises(ValueError, match="must sum to 100%"):
            TeamAllocation(
                team_name="Platform Team",
                date_range=(start_date, end_date),
                l0_pct=50.0,
                l1_pct=50.0,
                l2_pct=50.0,
                other_pct=0.0,
                total_issues=100,
                l2_velocity_actual=4.0,
                l2_velocity_projected=10.0,
            )

    def test_allocation_accepts_percentages_within_tolerance(self):
        """Should accept percentages that sum to 100% ±0.1%"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        # 99.95% should be accepted (within ±0.1% tolerance)
        allocation = TeamAllocation(
            team_name="Platform Team",
            date_range=(start_date, end_date),
            l0_pct=29.95,
            l1_pct=20.0,
            l2_pct=40.0,
            other_pct=10.0,
            total_issues=100,
            l2_velocity_actual=4.0,
            l2_velocity_projected=10.0,
        )

        assert 99.9 <= allocation.total_percentage <= 100.1

    def test_allocation_has_correct_type_hints(self):
        """Validate type hints are defined correctly"""
        from lib.reporting.allocation_models import TeamAllocation

        annotations = TeamAllocation.__annotations__

        assert annotations["team_name"] == str
        assert annotations["l0_pct"] == float
        assert annotations["l1_pct"] == float
        assert annotations["l2_pct"] == float
        assert annotations["other_pct"] == float
        assert annotations["total_issues"] == int
        assert annotations["l2_velocity_actual"] == float
        assert annotations["l2_velocity_projected"] == float

    def test_allocation_total_percentage_property(self):
        """Test total_percentage property calculation"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        allocation = TeamAllocation(
            team_name="Platform Team",
            date_range=(start_date, end_date),
            l0_pct=25.0,
            l1_pct=15.0,
            l2_pct=50.0,
            other_pct=10.0,
            total_issues=80,
            l2_velocity_actual=5.0,
            l2_velocity_projected=8.0,
        )

        assert allocation.total_percentage == 100.0

    def test_allocation_velocity_impact_property(self):
        """Test velocity_impact property calculation"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        allocation = TeamAllocation(
            team_name="Platform Team",
            date_range=(start_date, end_date),
            l0_pct=60.0,  # High L0 (support burden)
            l1_pct=15.0,
            l2_pct=20.0,  # Low L2
            other_pct=5.0,
            total_issues=100,
            l2_velocity_actual=2.0,  # Low actual velocity
            l2_velocity_projected=8.0,  # Expected high velocity
        )

        # velocity_impact should show negative impact (actual < projected)
        velocity_impact = allocation.velocity_impact
        assert velocity_impact < 0, "Expected negative velocity impact due to L0 burden"
        assert velocity_impact == pytest.approx(-75.0, abs=0.1)  # (2-8)/8 * 100

    def test_allocation_with_zero_issues(self):
        """Test allocation with zero total issues"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        allocation = TeamAllocation(
            team_name="Platform Team",
            date_range=(start_date, end_date),
            l0_pct=0.0,
            l1_pct=0.0,
            l2_pct=0.0,
            other_pct=100.0,  # All "other" work
            total_issues=0,
            l2_velocity_actual=0.0,
            l2_velocity_projected=0.0,
        )

        assert allocation.total_issues == 0
        assert allocation.total_percentage == 100.0

    def test_allocation_date_range_validation(self):
        """Test date range is validated"""
        from lib.reporting.allocation_models import TeamAllocation

        # Invalid: end date before start date
        start_date = datetime(2025, 3, 31)
        end_date = datetime(2025, 1, 1)

        with pytest.raises(ValueError, match="date range"):
            TeamAllocation(
                team_name="Platform Team",
                date_range=(start_date, end_date),
                l0_pct=25.0,
                l1_pct=25.0,
                l2_pct=25.0,
                other_pct=25.0,
                total_issues=100,
                l2_velocity_actual=5.0,
                l2_velocity_projected=8.0,
            )

    def test_allocation_negative_percentages_rejected(self):
        """Negative percentages should be rejected"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        with pytest.raises(ValueError, match="negative"):
            TeamAllocation(
                team_name="Platform Team",
                date_range=(start_date, end_date),
                l0_pct=-10.0,  # Invalid
                l1_pct=30.0,
                l2_pct=50.0,
                other_pct=30.0,
                total_issues=100,
                l2_velocity_actual=5.0,
                l2_velocity_projected=8.0,
            )

    def test_allocation_to_dict_method(self):
        """Test to_dict() method for JSON serialization"""
        from lib.reporting.allocation_models import TeamAllocation

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 3, 31)

        allocation = TeamAllocation(
            team_name="Platform Team",
            date_range=(start_date, end_date),
            l0_pct=30.0,
            l1_pct=20.0,
            l2_pct=40.0,
            other_pct=10.0,
            total_issues=100,
            l2_velocity_actual=4.0,
            l2_velocity_projected=10.0,
        )

        result = allocation.to_dict()

        assert result["team_name"] == "Platform Team"
        assert result["l0_pct"] == 30.0
        assert result["l1_pct"] == 20.0
        assert result["l2_pct"] == 40.0
        assert result["other_pct"] == 10.0
        assert result["total_issues"] == 100
        assert result["total_percentage"] == 100.0
        assert "start_date" in result
        assert "end_date" in result
