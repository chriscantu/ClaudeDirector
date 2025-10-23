"""
Team Allocation Data Models

BLOAT_PREVENTION: Single source of truth for allocation data structures
Used by AllocationCalculator and AllocationReportGenerator

Data Models:
- TeamAllocation: Type-safe allocation data with validation
- AllocationSummary: Cross-team aggregation (Phase 2)

Validation Rules:
- Allocation percentages must sum to 100% (±0.1% tolerance)
- No negative percentages allowed
- Date range validation (start < end)
- Type hints for all fields
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Tuple, Dict, Any


@dataclass
class TeamAllocation:
    """
    Type-safe team allocation data with automatic validation

    Allocation Categories:
    - L0: Keep-the-lights-on work (interrupts, operational, compliance)
    - L1: Work enabling L2 initiatives (prerequisites, dependencies)
    - L2: Strategic initiatives (platform capabilities, major features)
    - Other: Unclassified work (meetings, admin, etc.)

    Validation:
    - Percentages must sum to 100% (±0.1% tolerance)
    - No negative percentages
    - Valid date range (start_date < end_date)

    Usage:
    ```python
    allocation = TeamAllocation(
        team_name="Web Platform",
        date_range=(start_date, end_date),
        l0_pct=30.0, l1_pct=20.0, l2_pct=40.0, other_pct=10.0,
        total_issues=100,
        l2_velocity_actual=4.0,
        l2_velocity_projected=10.0
    )

    # Check if support burden is impacting velocity
    if allocation.velocity_impact < -50:
        print(f"⚠️ {allocation.team_name} L2 velocity down {abs(allocation.velocity_impact):.1f}%")
    ```
    """

    # Team identification
    team_name: str
    date_range: Tuple[datetime, datetime]

    # Allocation percentages (must sum to 100%)
    l0_pct: float  # Keep-the-lights-on work
    l1_pct: float  # L2 enabling work
    l2_pct: float  # Strategic initiatives
    other_pct: float  # Unclassified work

    # Volume metrics
    total_issues: int  # Total completed issues in period

    # Velocity metrics (L2 focus)
    l2_velocity_actual: float  # Actual L2 issues completed per week
    l2_velocity_projected: float  # Expected L2 velocity without support burden

    def __post_init__(self):
        """
        Validation: Enforce business rules on initialization

        Raises:
            ValueError: If percentages don't sum to 100%, are negative, or date range invalid
        """
        # Validate percentages sum to 100% (±0.1% tolerance)
        total = self.l0_pct + self.l1_pct + self.l2_pct + self.other_pct
        if not (99.9 <= total <= 100.1):
            raise ValueError(
                f"Allocation percentages must sum to 100% (±0.1%), got {total:.2f}%"
            )

        # Validate no negative percentages
        if any(
            pct < 0 for pct in [self.l0_pct, self.l1_pct, self.l2_pct, self.other_pct]
        ):
            raise ValueError(
                f"Allocation percentages cannot be negative: "
                f"L0={self.l0_pct}, L1={self.l1_pct}, L2={self.l2_pct}, Other={self.other_pct}"
            )

        # Validate date range
        start_date, end_date = self.date_range
        if start_date >= end_date:
            raise ValueError(
                f"Invalid date range: start_date ({start_date}) must be before end_date ({end_date})"
            )

    @property
    def total_percentage(self) -> float:
        """
        Calculate total allocation percentage (should always be ~100%)

        Returns:
            Sum of L0 + L1 + L2 + Other percentages
        """
        return self.l0_pct + self.l1_pct + self.l2_pct + self.other_pct

    @property
    def velocity_impact(self) -> float:
        """
        Calculate L2 velocity impact as percentage change

        Negative value = support burden impacting L2 velocity
        Positive value = exceeding projected velocity

        Formula: ((actual - projected) / projected) * 100

        Returns:
            Velocity impact percentage (-100 to +∞)

        Example:
            actual=2, projected=8 → -75% (L2 velocity down 75%)
            actual=10, projected=8 → +25% (L2 velocity up 25%)
        """
        if self.l2_velocity_projected == 0:
            return 0.0

        return (
            (self.l2_velocity_actual - self.l2_velocity_projected)
            / self.l2_velocity_projected
        ) * 100

    @property
    def start_date(self) -> datetime:
        """Extract start date from date_range tuple"""
        return self.date_range[0]

    @property
    def end_date(self) -> datetime:
        """Extract end date from date_range tuple"""
        return self.date_range[1]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert allocation to dictionary for JSON serialization

        Returns:
            Dictionary with all fields + computed properties
        """
        result = {
            "team_name": self.team_name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "l0_pct": self.l0_pct,
            "l1_pct": self.l1_pct,
            "l2_pct": self.l2_pct,
            "other_pct": self.other_pct,
            "total_percentage": self.total_percentage,
            "total_issues": self.total_issues,
            "l2_velocity_actual": self.l2_velocity_actual,
            "l2_velocity_projected": self.l2_velocity_projected,
            "velocity_impact": self.velocity_impact,
        }
        return result

    def __repr__(self) -> str:
        """Executive-friendly representation"""
        return (
            f"TeamAllocation(team='{self.team_name}', "
            f"L0={self.l0_pct:.1f}%, L1={self.l1_pct:.1f}%, L2={self.l2_pct:.1f}%, Other={self.other_pct:.1f}%, "
            f"velocity_impact={self.velocity_impact:+.1f}%)"
        )
