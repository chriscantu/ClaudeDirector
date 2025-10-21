"""
ROI Modeling Engine - Spec 002 FR2 MCP Server Enhancement

Provides platform investment and strategic initiative ROI predictions.

BLOAT_PREVENTION Compliance:
- Uses shared InvestmentType enum (eliminates duplication with roi_investment_tracker)
- Integrates with existing prediction_models.py patterns
- Follows PROJECT_STRUCTURE.md (lib/ai_intelligence/predictive/)
- Extends existing predictive capabilities without duplication

Author: Martin | Platform Architecture
Spec: 002-mcp-server-enhancement FR2
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging

# Import shared InvestmentType to eliminate duplication
# Path: lib/ai_intelligence/predictive/ -> lib/p0_features/shared/models/
from p0_features.shared.models.investment_types import InvestmentType


class ROITimeframe(Enum):
    """ROI calculation timeframes"""

    SHORT_TERM = "short_term"  # 3-6 months
    MEDIUM_TERM = "medium_term"  # 6-12 months
    LONG_TERM = "long_term"  # 12-24 months


@dataclass
class InvestmentContext:
    """Context for ROI prediction"""

    investment_type: InvestmentType
    estimated_cost: float
    team_size: int
    current_velocity: float
    technical_debt_level: float
    stakeholder_priority: float  # 0.0-1.0
    timeframe: ROITimeframe
    historical_similar_investments: List[Dict[str, Any]] = None


@dataclass
class ROIPrediction:
    """ROI prediction result"""

    investment_type: InvestmentType
    predicted_roi_percent: float
    confidence_score: float  # 0.0-1.0
    payback_period_months: float
    estimated_benefits: Dict[str, float]  # Quantified benefits
    risk_factors: List[str]
    recommendations: List[str]
    best_case_roi: float
    worst_case_roi: float
    expected_roi: float
    prediction_timestamp: datetime


class ROIModelingEngine:
    """
    ROI Modeling Engine for platform investments and strategic initiatives

    Provides data-driven ROI predictions with confidence intervals to support
    strategic investment decisions and platform planning.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize ROI modeling engine"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # ROI model parameters
        self.baseline_roi_by_type = self._initialize_baseline_roi()
        self.benefit_multipliers = self._initialize_benefit_multipliers()
        self.risk_factors = self._initialize_risk_factors()

        self.logger.info("ROI Modeling Engine initialized")

    def _initialize_baseline_roi(self) -> Dict[InvestmentType, Dict[str, float]]:
        """Initialize baseline ROI expectations by investment type"""
        return {
            InvestmentType.PLATFORM_INFRASTRUCTURE: {
                "baseline_roi": 2.5,  # 250% ROI
                "confidence": 0.85,
                "typical_payback_months": 12,
            },
            InvestmentType.DEVELOPER_TOOLING: {
                "baseline_roi": 3.0,  # 300% ROI
                "confidence": 0.90,
                "typical_payback_months": 6,
            },
            InvestmentType.DEVELOPER_TOOLS: {  # Tracker system alias
                "baseline_roi": 3.0,  # 300% ROI (same as DEVELOPER_TOOLING)
                "confidence": 0.90,
                "typical_payback_months": 6,
            },
            InvestmentType.AUTOMATION: {
                "baseline_roi": 4.0,  # 400% ROI
                "confidence": 0.88,
                "typical_payback_months": 9,
            },
            InvestmentType.AUTOMATION_SYSTEMS: {  # Tracker system alias
                "baseline_roi": 4.0,  # 400% ROI (same as AUTOMATION)
                "confidence": 0.88,
                "typical_payback_months": 9,
            },
            InvestmentType.TECHNICAL_DEBT_REDUCTION: {
                "baseline_roi": 2.2,  # 220% ROI
                "confidence": 0.75,
                "typical_payback_months": 15,
            },
            InvestmentType.TEAM_EXPANSION: {
                "baseline_roi": 1.8,  # 180% ROI
                "confidence": 0.70,
                "typical_payback_months": 18,
            },
            InvestmentType.TRAINING_DEVELOPMENT: {
                "baseline_roi": 2.8,  # 280% ROI
                "confidence": 0.80,
                "typical_payback_months": 8,
            },
            InvestmentType.PROCESS_IMPROVEMENT: {
                "baseline_roi": 3.5,  # 350% ROI
                "confidence": 0.92,
                "typical_payback_months": 4,
            },
            # Additional investment types from unified enum (with reasonable defaults)
            InvestmentType.ANALYTICS_CAPABILITIES: {
                "baseline_roi": 2.7,  # 270% ROI
                "confidence": 0.82,
                "typical_payback_months": 10,
            },
            InvestmentType.SECURITY_IMPROVEMENTS: {
                "baseline_roi": 2.0,  # 200% ROI (risk mitigation)
                "confidence": 0.78,
                "typical_payback_months": 16,
            },
            InvestmentType.COLLABORATION_TOOLS: {
                "baseline_roi": 2.4,  # 240% ROI
                "confidence": 0.85,
                "typical_payback_months": 7,
            },
            InvestmentType.MONITORING_OBSERVABILITY: {
                "baseline_roi": 3.2,  # 320% ROI
                "confidence": 0.87,
                "typical_payback_months": 8,
            },
        }

    def _initialize_benefit_multipliers(self) -> Dict[str, Dict[str, float]]:
        """Initialize benefit multipliers based on context factors"""
        return {
            "team_size": {
                "small": 1.0,  # <10 people
                "medium": 1.3,  # 10-50 people
                "large": 1.6,  # >50 people
            },
            "technical_debt": {
                "low": 1.2,  # More capacity for value delivery
                "medium": 1.0,  # Baseline
                "high": 0.7,  # Drag on productivity
            },
            "velocity_trend": {
                "declining": 0.8,
                "stable": 1.0,
                "improving": 1.2,
            },
            "stakeholder_alignment": {
                "low": 0.7,  # <0.5 priority
                "medium": 1.0,  # 0.5-0.75
                "high": 1.3,  # >0.75
            },
        }

    def _initialize_risk_factors(self) -> Dict[str, List[str]]:
        """Initialize risk factors by investment type"""
        return {
            InvestmentType.PLATFORM_INFRASTRUCTURE.value: [
                "Long implementation timeline",
                "Complex integration requirements",
                "Organizational resistance to change",
            ],
            InvestmentType.AUTOMATION.value: [
                "Process variability",
                "Maintenance overhead",
                "Initial productivity dip",
            ],
            InvestmentType.TECHNICAL_DEBT_REDUCTION.value: [
                "Opportunity cost of feature development",
                "Risk of regression",
                "Difficulty quantifying benefits",
            ],
        }

    def predict_roi(self, investment_context: InvestmentContext) -> ROIPrediction:
        """
        Predict ROI for a platform investment or strategic initiative

        Args:
            investment_context: Context for the investment

        Returns:
            ROIPrediction with expected ROI, confidence, and risk factors
        """
        start_time = datetime.now()

        try:
            # Get baseline ROI for investment type
            baseline = self.baseline_roi_by_type.get(
                investment_context.investment_type, {}
            )
            base_roi = baseline.get("baseline_roi", 2.0)
            base_confidence = baseline.get("confidence", 0.75)
            base_payback = baseline.get("typical_payback_months", 12)

            # Apply context multipliers
            team_multiplier = self._calculate_team_size_multiplier(
                investment_context.team_size
            )
            debt_multiplier = self._calculate_technical_debt_multiplier(
                investment_context.technical_debt_level
            )
            stakeholder_multiplier = self._calculate_stakeholder_multiplier(
                investment_context.stakeholder_priority
            )

            # Calculate adjusted ROI
            adjusted_roi = (
                base_roi * team_multiplier * debt_multiplier * stakeholder_multiplier
            )

            # Calculate confidence based on context
            confidence = self._calculate_confidence(base_confidence, investment_context)

            # Calculate payback period
            payback_months = base_payback / (adjusted_roi / base_roi)

            # Calculate benefit scenarios
            best_case = adjusted_roi * 1.3  # 30% upside
            worst_case = adjusted_roi * 0.6  # 40% downside
            expected = adjusted_roi

            # Identify risk factors
            risks = self._identify_risk_factors(investment_context)

            # Generate recommendations
            recommendations = self._generate_recommendations(
                investment_context, adjusted_roi, confidence
            )

            # Calculate estimated benefits
            benefits = self._calculate_estimated_benefits(
                investment_context, adjusted_roi
            )

            prediction = ROIPrediction(
                investment_type=investment_context.investment_type,
                predicted_roi_percent=adjusted_roi * 100,  # Convert to percentage
                confidence_score=confidence,
                payback_period_months=payback_months,
                estimated_benefits=benefits,
                risk_factors=risks,
                recommendations=recommendations,
                best_case_roi=best_case * 100,
                worst_case_roi=worst_case * 100,
                expected_roi=expected * 100,
                prediction_timestamp=datetime.now(),
            )

            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            self.logger.info(
                f"ROI prediction completed in {processing_time:.2f}ms",
                extra={
                    "investment_type": investment_context.investment_type.value,
                    "predicted_roi": adjusted_roi,
                    "confidence": confidence,
                },
            )

            return prediction

        except Exception as e:
            self.logger.error(f"ROI prediction failed: {e}")
            # Return conservative fallback prediction
            return self._create_fallback_prediction(investment_context)

    def _calculate_team_size_multiplier(self, team_size: int) -> float:
        """Calculate team size benefit multiplier"""
        multipliers = self.benefit_multipliers["team_size"]
        if team_size < 10:
            return multipliers["small"]
        elif team_size < 50:
            return multipliers["medium"]
        else:
            return multipliers["large"]

    def _calculate_technical_debt_multiplier(
        self, technical_debt_level: float
    ) -> float:
        """Calculate technical debt drag multiplier"""
        multipliers = self.benefit_multipliers["technical_debt"]
        if technical_debt_level < 0.3:
            return multipliers["low"]
        elif technical_debt_level < 0.6:
            return multipliers["medium"]
        else:
            return multipliers["high"]

    def _calculate_stakeholder_multiplier(self, stakeholder_priority: float) -> float:
        """Calculate stakeholder alignment multiplier"""
        multipliers = self.benefit_multipliers["stakeholder_alignment"]
        if stakeholder_priority < 0.5:
            return multipliers["low"]
        elif stakeholder_priority < 0.75:
            return multipliers["medium"]
        else:
            return multipliers["high"]

    def _calculate_confidence(
        self, base_confidence: float, context: InvestmentContext
    ) -> float:
        """Calculate prediction confidence based on context quality"""
        # Adjust confidence based on data availability
        confidence = base_confidence

        # Reduce confidence if no historical data
        if not context.historical_similar_investments:
            confidence *= 0.9

        # Reduce confidence for high technical debt
        if context.technical_debt_level > 0.7:
            confidence *= 0.85

        # Increase confidence for high stakeholder alignment
        if context.stakeholder_priority > 0.8:
            confidence *= 1.05

        return min(confidence, 0.95)  # Cap at 95%

    def _identify_risk_factors(self, context: InvestmentContext) -> List[str]:
        """Identify risk factors for the investment"""
        risks = []

        # Get type-specific risks
        type_risks = self.risk_factors.get(context.investment_type.value, [])
        risks.extend(type_risks)

        # Add context-specific risks
        if context.technical_debt_level > 0.7:
            risks.append("High technical debt may slow implementation")

        if context.stakeholder_priority < 0.5:
            risks.append("Low stakeholder priority may limit support")

        if context.team_size < 5:
            risks.append("Small team size limits parallel execution")

        return risks

    def _generate_recommendations(
        self, context: InvestmentContext, predicted_roi: float, confidence: float
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if predicted_roi > 3.0:
            recommendations.append(
                f"Strong ROI ({predicted_roi:.1f}x) - Consider prioritizing this investment"
            )
        elif predicted_roi > 2.0:
            recommendations.append(
                f"Good ROI ({predicted_roi:.1f}x) - Viable strategic investment"
            )
        else:
            recommendations.append(
                f"Moderate ROI ({predicted_roi:.1f}x) - Evaluate alternatives"
            )

        if confidence < 0.7:
            recommendations.append(
                "Low confidence - Gather more data before committing"
            )

        if context.technical_debt_level > 0.7:
            recommendations.append("Consider technical debt reduction as prerequisite")

        if context.stakeholder_priority > 0.8:
            recommendations.append(
                "High stakeholder support - Favorable execution environment"
            )

        return recommendations

    def _calculate_estimated_benefits(
        self, context: InvestmentContext, predicted_roi: float
    ) -> Dict[str, float]:
        """Calculate quantified benefits"""
        total_value = context.estimated_cost * predicted_roi

        # Distribute benefits across categories
        benefits = {
            "productivity_gain": total_value * 0.4,
            "cost_reduction": total_value * 0.3,
            "quality_improvement": total_value * 0.2,
            "team_satisfaction": total_value * 0.1,
        }

        return benefits

    def _create_fallback_prediction(self, context: InvestmentContext) -> ROIPrediction:
        """Create conservative fallback prediction on error"""
        return ROIPrediction(
            investment_type=context.investment_type,
            predicted_roi_percent=150.0,  # Conservative 150% ROI
            confidence_score=0.50,  # Low confidence
            payback_period_months=18.0,
            estimated_benefits={
                "productivity_gain": context.estimated_cost * 0.6,
                "cost_reduction": context.estimated_cost * 0.4,
                "quality_improvement": context.estimated_cost * 0.3,
                "team_satisfaction": context.estimated_cost * 0.15,
            },
            risk_factors=["Insufficient data for accurate prediction"],
            recommendations=["Gather more data before proceeding"],
            best_case_roi=200.0,
            worst_case_roi=100.0,
            expected_roi=150.0,
            prediction_timestamp=datetime.now(),
        )

    def analyze_investment_portfolio(
        self, investments: List[InvestmentContext]
    ) -> Dict[str, Any]:
        """
        Analyze a portfolio of potential investments

        Args:
            investments: List of investment contexts

        Returns:
            Portfolio analysis with prioritization recommendations
        """
        predictions = []

        for investment in investments:
            prediction = self.predict_roi(investment)
            predictions.append(
                {
                    "context": investment,
                    "prediction": prediction,
                    "priority_score": self._calculate_priority_score(prediction),
                }
            )

        # Sort by priority score
        predictions.sort(key=lambda x: x["priority_score"], reverse=True)

        return {
            "total_investments": len(investments),
            "predictions": predictions,
            "recommended_sequence": [
                p["context"].investment_type.value for p in predictions
            ],
            "portfolio_expected_roi": (
                sum(p["prediction"].expected_roi for p in predictions)
                / len(predictions)
                if predictions
                else 0
            ),
            "analysis_timestamp": datetime.now(),
        }

    def _calculate_priority_score(self, prediction: ROIPrediction) -> float:
        """Calculate priority score for investment"""
        # Weight ROI and confidence
        roi_score = prediction.expected_roi / 100  # Normalize
        confidence_weight = prediction.confidence_score

        # Priority = ROI * confidence / payback_period
        priority = (roi_score * confidence_weight) / max(
            prediction.payback_period_months, 1
        )

        return priority
