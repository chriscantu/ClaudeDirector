"""
Investment Proposal Service

Single Responsibility: Investment proposal creation and evaluation.
Extracted from monolithic ROI tracker for SOLID compliance.
"""

from typing import Dict, List, Optional, Any
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import structlog
import uuid

from ..models.roi_models import (
    InvestmentProposal,
    InvestmentCategory,
    InvestmentStatus,
    ROICalculationMethod,
)


class InvestmentProposalService:
    """Service for managing investment proposals"""

    def __init__(self, business_calculator):
        self.business_calculator = business_calculator
        self.logger = structlog.get_logger(__name__)

        # ROI calculation parameters
        self._roi_parameters = {
            "discount_rate": Decimal("0.08"),  # 8% discount rate for NPV
            "minimum_acceptable_roi": Decimal("1.15"),  # 15% minimum ROI
            "risk_adjustment_factors": {
                InvestmentCategory.PLATFORM_INFRASTRUCTURE: Decimal("1.1"),
                InvestmentCategory.DEVELOPER_TOOLS: Decimal("1.0"),
                InvestmentCategory.ANALYTICS_CAPABILITIES: Decimal("1.2"),
                InvestmentCategory.AUTOMATION_SYSTEMS: Decimal("0.9"),
                InvestmentCategory.SECURITY_IMPROVEMENTS: Decimal("1.3"),
                InvestmentCategory.COLLABORATION_TOOLS: Decimal("0.95"),
                InvestmentCategory.MONITORING_OBSERVABILITY: Decimal("1.05"),
            },
            "strategic_value_multipliers": {
                "competitive_advantage": Decimal("1.5"),
                "market_expansion": Decimal("2.0"),
                "regulatory_compliance": Decimal("1.2"),
                "technical_debt_reduction": Decimal("1.3"),
            },
        }

    def create_investment_proposal(
        self, proposal_data: Dict[str, Any]
    ) -> InvestmentProposal:
        """Create new investment proposal with business justification"""
        try:
            proposal_id = str(uuid.uuid4())

            # Calculate ROI projections
            roi_projections = self._calculate_roi_projections(proposal_data)

            # Create proposal
            proposal = InvestmentProposal(
                proposal_id=proposal_id,
                title=proposal_data["title"],
                description=proposal_data["description"],
                category=InvestmentCategory(proposal_data["category"]),
                total_investment=Decimal(str(proposal_data["total_investment"])),
                implementation_cost=Decimal(str(proposal_data["implementation_cost"])),
                ongoing_annual_cost=Decimal(
                    str(proposal_data.get("ongoing_annual_cost", 0))
                ),
                proposed_start_date=proposal_data["proposed_start_date"],
                estimated_duration_months=proposal_data["estimated_duration_months"],
                year_1_benefits=roi_projections["year_1"],
                year_2_benefits=roi_projections["year_2"],
                year_3_benefits=roi_projections["year_3"],
                roi_calculation_method=ROICalculationMethod(
                    proposal_data["roi_method"]
                ),
                business_problem=proposal_data["business_problem"],
                proposed_solution=proposal_data["proposed_solution"],
                success_metrics=proposal_data["success_metrics"],
                risk_factors=proposal_data["risk_factors"],
                alternatives_considered=proposal_data.get(
                    "alternatives_considered", []
                ),
                business_sponsor=proposal_data["business_sponsor"],
                technical_lead=proposal_data["technical_lead"],
                affected_stakeholders=proposal_data["affected_stakeholders"],
                status=InvestmentStatus.PROPOSED,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            self.logger.info(
                "Investment proposal created",
                proposal_id=proposal_id,
                title=proposal.title,
                total_investment=str(proposal.total_investment),
                projected_3yr_roi=str(roi_projections["total_roi"]),
            )

            return proposal

        except Exception as e:
            self.logger.error("Investment proposal creation failed", error=str(e))
            raise

    def evaluate_investment_proposal(
        self, proposal: InvestmentProposal
    ) -> Dict[str, Any]:
        """Evaluate investment proposal for approval decision"""
        try:
            # Calculate financial metrics
            financial_analysis = self._analyze_financial_metrics(proposal)

            # Assess risks
            risk_assessment = self._assess_proposal_risks(proposal)

            # Calculate strategic alignment
            strategic_score = self._calculate_strategic_alignment_score(proposal)

            # Generate recommendation
            recommendation = self._generate_investment_recommendation(
                proposal, financial_analysis, risk_assessment, strategic_score
            )

            return {
                "proposal_id": proposal.proposal_id,
                "financial_analysis": financial_analysis,
                "risk_assessment": risk_assessment,
                "strategic_alignment_score": strategic_score,
                "recommendation": recommendation,
                "evaluated_at": datetime.now(),
            }

        except Exception as e:
            self.logger.error(
                "Investment proposal evaluation failed",
                proposal_id=proposal.proposal_id,
                error=str(e),
            )
            return {"error": str(e)}

    def _calculate_roi_projections(
        self, proposal_data: Dict[str, Any]
    ) -> Dict[str, Decimal]:
        """Calculate ROI projections for investment proposal"""
        try:
            total_investment = Decimal(str(proposal_data["total_investment"]))
            roi_method = ROICalculationMethod(proposal_data["roi_method"])
            category = InvestmentCategory(proposal_data["category"])

            # Base benefit calculations
            base_annual_benefit = total_investment * Decimal("0.25")  # 25% base return

            # Apply risk adjustment
            risk_factor = self._roi_parameters["risk_adjustment_factors"][category]
            adjusted_benefit = base_annual_benefit * risk_factor

            # Calculate 3-year projection with growth
            year_1 = adjusted_benefit
            year_2 = adjusted_benefit * Decimal("1.1")  # 10% growth
            year_3 = adjusted_benefit * Decimal("1.2")  # 20% growth

            total_roi = (year_1 + year_2 + year_3) / total_investment

            return {
                "year_1": year_1,
                "year_2": year_2,
                "year_3": year_3,
                "total_roi": total_roi,
            }

        except Exception as e:
            self.logger.error("ROI projection calculation failed", error=str(e))
            raise

    def _analyze_financial_metrics(
        self, proposal: InvestmentProposal
    ) -> Dict[str, Any]:
        """Analyze financial metrics for proposal"""
        total_benefits = (
            proposal.year_1_benefits
            + proposal.year_2_benefits
            + proposal.year_3_benefits
        )
        roi_ratio = total_benefits / proposal.total_investment
        payback_period = proposal.total_investment / proposal.year_1_benefits

        return {
            "total_3yr_benefits": total_benefits,
            "roi_ratio": roi_ratio,
            "payback_period_years": payback_period,
            "meets_minimum_roi": roi_ratio
            >= self._roi_parameters["minimum_acceptable_roi"],
        }

    def _assess_proposal_risks(self, proposal: InvestmentProposal) -> Dict[str, Any]:
        """Assess risks for investment proposal"""
        risk_score = len(proposal.risk_factors) * 0.1  # Simple risk scoring
        risk_level = (
            "LOW" if risk_score < 0.3 else "MEDIUM" if risk_score < 0.6 else "HIGH"
        )

        return {
            "risk_factors_count": len(proposal.risk_factors),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "mitigation_required": risk_level == "HIGH",
        }

    def _calculate_strategic_alignment_score(
        self, proposal: InvestmentProposal
    ) -> Decimal:
        """Calculate strategic alignment score"""
        # Simple scoring based on category strategic value
        category_scores = {
            InvestmentCategory.PLATFORM_INFRASTRUCTURE: Decimal("0.9"),
            InvestmentCategory.DEVELOPER_TOOLS: Decimal("0.8"),
            InvestmentCategory.ANALYTICS_CAPABILITIES: Decimal("0.85"),
            InvestmentCategory.AUTOMATION_SYSTEMS: Decimal("0.75"),
            InvestmentCategory.SECURITY_IMPROVEMENTS: Decimal("0.95"),
            InvestmentCategory.COLLABORATION_TOOLS: Decimal("0.7"),
            InvestmentCategory.MONITORING_OBSERVABILITY: Decimal("0.8"),
        }
        return category_scores.get(proposal.category, Decimal("0.5"))

    def _generate_investment_recommendation(
        self,
        proposal: InvestmentProposal,
        financial: Dict,
        risk: Dict,
        strategic: Decimal,
    ) -> Dict[str, Any]:
        """Generate investment recommendation"""
        # Simple decision logic
        if (
            financial["meets_minimum_roi"]
            and risk["risk_level"] != "HIGH"
            and strategic >= Decimal("0.7")
        ):
            decision = "APPROVE"
        elif financial["meets_minimum_roi"] and strategic >= Decimal("0.8"):
            decision = "APPROVE_WITH_CONDITIONS"
        else:
            decision = "REJECT"

        return {
            "decision": decision,
            "confidence": "HIGH" if decision == "APPROVE" else "MEDIUM",
            "key_factors": [
                f"ROI: {financial['roi_ratio']:.2f}",
                f"Risk: {risk['risk_level']}",
                f"Strategic: {strategic:.2f}",
            ],
        }
