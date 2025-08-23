"""
ROI Investment Tracker Data Models

Alvaro's comprehensive investment tracking data structures.
Extracted from monolithic tracker for SOLID compliance.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from decimal import Decimal


class InvestmentCategory(Enum):
    """Categories of platform investments"""

    PLATFORM_INFRASTRUCTURE = "platform_infrastructure"
    DEVELOPER_TOOLS = "developer_tools"
    ANALYTICS_CAPABILITIES = "analytics_capabilities"
    AUTOMATION_SYSTEMS = "automation_systems"
    SECURITY_IMPROVEMENTS = "security_improvements"
    COLLABORATION_TOOLS = "collaboration_tools"
    MONITORING_OBSERVABILITY = "monitoring_observability"


class InvestmentStatus(Enum):
    """Investment tracking status"""

    PROPOSED = "proposed"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class ROICalculationMethod(Enum):
    """Methods for calculating ROI"""

    DIRECT_SAVINGS = "direct_savings"  # Direct cost savings
    PRODUCTIVITY_GAINS = "productivity_gains"  # Efficiency improvements
    RISK_MITIGATION = "risk_mitigation"  # Risk reduction value
    REVENUE_ENABLEMENT = "revenue_enablement"  # Revenue opportunities
    STRATEGIC_VALUE = "strategic_value"  # Long-term strategic benefits


@dataclass
class InvestmentProposal:
    """Investment proposal with business justification"""

    proposal_id: str
    title: str
    description: str
    category: InvestmentCategory

    # Financial details
    total_investment: Decimal
    implementation_cost: Decimal
    ongoing_annual_cost: Decimal

    # Timeline
    proposed_start_date: datetime
    estimated_duration_months: int

    # ROI projections
    year_1_benefits: Decimal
    year_2_benefits: Decimal
    year_3_benefits: Decimal
    roi_calculation_method: ROICalculationMethod

    # Business justification
    business_problem: str
    proposed_solution: str
    success_metrics: List[str]
    risk_factors: List[str]
    alternatives_considered: List[str]

    # Stakeholder information
    business_sponsor: str
    technical_lead: str
    affected_stakeholders: List[str]

    # Status and tracking
    status: InvestmentStatus
    approval_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None

    # Actual performance (filled during implementation)
    actual_investment: Optional[Decimal] = None
    actual_benefits_ytd: Optional[Decimal] = None

    created_at: datetime = None
    updated_at: datetime = None


@dataclass
class ROITracking:
    """ROI tracking data for approved investments"""

    investment_id: str
    measurement_period: str

    # Financial tracking
    planned_benefits: Decimal
    actual_benefits: Decimal
    variance_amount: Decimal
    variance_percentage: Decimal

    # Benefit breakdown
    direct_savings: Decimal
    productivity_gains: Decimal
    risk_mitigation_value: Decimal
    strategic_value: Decimal

    # Performance indicators
    success_metrics_achieved: int
    total_success_metrics: int
    stakeholder_satisfaction: Decimal  # 0-10 scale

    # Implementation metrics
    timeline_adherence: Decimal  # Percentage on-time
    budget_adherence: Decimal  # Percentage on-budget

    # Lessons learned
    key_successes: List[str]
    challenges_faced: List[str]
    recommendations: List[str]

    measured_at: datetime
    measured_by: str


@dataclass
class InvestmentPortfolioSummary:
    """Summary of investment portfolio performance"""

    reporting_period: str

    # Portfolio overview
    total_active_investments: int
    total_portfolio_value: Decimal
    total_expected_annual_roi: Decimal

    # Performance summary
    investments_exceeding_roi: int
    investments_meeting_timeline: int
    investments_on_budget: int

    # Financial summary
    total_benefits_realized: Decimal
    total_investment_spent: Decimal
    portfolio_roi_actual: Decimal
    portfolio_roi_projected: Decimal

    # Category breakdown
    investment_by_category: Dict[str, Decimal]
    roi_by_category: Dict[str, Decimal]

    # Risk analysis
    high_risk_investments: int
    investments_requiring_attention: List[str]

    # Strategic insights
    top_performing_investments: List[str]
    recommended_future_investments: List[str]

    generated_at: datetime
