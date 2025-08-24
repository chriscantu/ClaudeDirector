"""
ROI Investment Tracker Interface

Defines the contract for ROI investment tracking services.
Enables Dependency Inversion Principle for SOLID architecture.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from decimal import Decimal
from datetime import datetime

from ..models.roi_models import (
    InvestmentProposal,
    ROITracking,
    InvestmentPortfolioSummary,
    InvestmentCategory,
)


class InvestmentTrackerInterface(ABC):
    """Interface for ROI Investment Tracker functionality"""

    @abstractmethod
    def create_investment_proposal(
        self,
        title: str,
        description: str,
        category: InvestmentCategory,
        total_investment: Decimal,
        implementation_cost: Decimal,
        ongoing_annual_cost: Decimal,
        proposed_start_date: datetime,
        estimated_duration_months: int,
        year_1_benefits: Decimal,
        year_2_benefits: Decimal,
        year_3_benefits: Decimal,
        business_problem: str,
        proposed_solution: str,
        success_metrics: List[str],
        risk_factors: List[str],
        alternatives_considered: List[str],
        business_sponsor: str,
        technical_lead: str,
        affected_stakeholders: List[str],
    ) -> InvestmentProposal:
        """Create a new investment proposal"""

    @abstractmethod
    def evaluate_investment_proposal(self, proposal_id: str) -> Dict[str, Any]:
        """Evaluate an investment proposal for approval"""

    @abstractmethod
    def track_investment_performance(
        self, investment_id: str, period: str
    ) -> ROITracking:
        """Track actual ROI performance of approved investments"""

    @abstractmethod
    def generate_portfolio_summary(
        self, reporting_period: str
    ) -> InvestmentPortfolioSummary:
        """Generate comprehensive portfolio performance summary"""

    @abstractmethod
    def generate_investment_justification_report(
        self, proposal_id: str
    ) -> Dict[str, Any]:
        """Generate detailed investment justification report"""
