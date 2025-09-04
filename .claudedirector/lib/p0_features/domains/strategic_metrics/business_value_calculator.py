"""
Strategic Business Value Calculator

🏗️ Sequential Thinking Phase 5.1.3: Lightweight Facade Implementation
All complex business calculation logic delegated to BusinessIntelligenceProcessor.

Alvaro's framework for translating technical platform metrics into business outcomes.
Designed for executive reporting and investment justification.
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import structlog
from decimal import Decimal, ROUND_HALF_UP

from ...shared.infrastructure.config import get_config

# Phase 2D: Use HybridToUnifiedBridge for database access (no legacy fallback)
from ....core.hybrid_compatibility import HybridToUnifiedBridge

print("📊 Phase 2D: Using HybridToUnifiedBridge for BusinessValueCalculator")

logger = structlog.get_logger(__name__)


class BusinessMetricType(Enum):
    """Categories of business metrics for executive reporting"""

    LEADERSHIP_VELOCITY = "leadership_velocity"  # Speed of strategic decisions
    PLATFORM_ROI = "platform_roi"  # Return on platform investment
    RISK_MITIGATION = "risk_mitigation"  # Risk reduction value
    EFFICIENCY_GAINS = "efficiency_gains"  # Operational efficiency improvements
    STAKEHOLDER_SATISFACTION = (
        "stakeholder_satisfaction"  # Stakeholder engagement quality
    )
    STRATEGIC_ALIGNMENT = (
        "strategic_alignment"  # Initiative alignment with business goals
    )
    COMPETITIVE_ADVANTAGE = "competitive_advantage"  # Market positioning improvements


class MetricTrend(Enum):
    """Trend directions for business metrics"""

    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    VOLATILE = "volatile"


@dataclass
class BusinessMetric:
    """Individual business metric for value calculation"""

    metric_type: BusinessMetricType
    name: str
    current_value: Decimal
    previous_value: Optional[Decimal]
    trend: MetricTrend
    business_impact_dollars: Decimal
    confidence_score: float  # 0.0 to 1.0
    methodology: str
    last_updated: datetime


@dataclass
class BusinessImpactReport:
    """
    🏗️ Sequential Thinking Phase 5.1.3: Business impact calculation report
    Comprehensive business impact assessment for executive decision-making
    """

    # Core business value metrics
    total_business_value: Decimal
    roi_percentage: Decimal
    efficiency_gains: Decimal
    risk_mitigation_value: Decimal

    # Strategic alignment metrics
    strategic_alignment_score: float
    competitive_advantage_score: float

    # Individual metrics breakdown
    business_metrics: List[BusinessMetric]

    # Calculation metadata
    calculation_period_days: int
    data_quality_score: float
    generated_at: datetime
    methodology_notes: List[str]


class BusinessValueCalculator:
    """
    🏗️ Sequential Thinking Phase 5.1.3: Lightweight business value calculation facade

    Strategic business value calculator for translating technical metrics into business outcomes.
    All complex calculation logic delegated to BusinessIntelligenceProcessor for maximum
    efficiency while maintaining 100% API compatibility.

    Alvaro's framework for:
    - ROI calculation and investment justification
    - Executive dashboard metrics and business impact measurement
    - Strategic alignment scoring and competitive analysis
    """

    def __init__(self):
        """🏗️ Sequential Thinking Phase 5.1.3: Lightweight facade initialization"""
        # Import BusinessIntelligenceProcessor for delegation
        from .business_intelligence_processor import BusinessIntelligenceProcessor

        self.processor = BusinessIntelligenceProcessor()

        # Preserve original interface dependencies for backward compatibility
        self.database_bridge = HybridToUnifiedBridge()
        self.analytics_pipeline = None  # Unified bridge handles all analytics
        self.config = get_config()
        self.logger = logger.bind(component="business_value_calculator")

        self.logger.info("BusinessValueCalculator initialized as lightweight facade")

    def calculate_comprehensive_business_impact(
        self, analysis_period_days: int = 90
    ) -> BusinessImpactReport:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Calculate comprehensive business impact using processor
        """
        return self.processor.calculate_comprehensive_business_impact(
            analysis_period_days
        )

    def calculate_roi_justification(
        self,
        investment_amount: Decimal,
        time_horizon_months: int = 12,
        risk_factor: float = 0.1,
    ) -> Dict[str, Any]:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Calculate ROI justification using processor
        """
        return self.processor.calculate_roi_justification(
            investment_amount, time_horizon_months, risk_factor
        )

    def generate_executive_dashboard_metrics(self) -> Dict[str, Any]:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Generate executive dashboard metrics using processor
        """
        return self.processor.generate_executive_dashboard_metrics()

    def calculate_leadership_velocity_value(
        self, current_cycle_days: float, target_cycle_days: float = 7.0
    ) -> Decimal:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Calculate leadership velocity business value using processor
        """
        return self.processor.calculate_leadership_velocity_value(
            current_cycle_days, target_cycle_days
        )

    def calculate_platform_roi_value(
        self, efficiency_improvements: List[Dict[str, Any]]
    ) -> Decimal:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Calculate platform ROI value using processor
        """
        return self.processor.calculate_platform_roi_value(efficiency_improvements)

    def calculate_risk_mitigation_value(
        self, risks_mitigated: List[Dict[str, Any]]
    ) -> Decimal:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Calculate risk mitigation value using processor
        """
        return self.processor.calculate_risk_mitigation_value(risks_mitigated)

    def calculate_stakeholder_satisfaction_value(
        self, satisfaction_improvements: Dict[str, float]
    ) -> Decimal:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Calculate stakeholder satisfaction business value using processor
        """
        return self.processor.calculate_stakeholder_satisfaction_value(
            satisfaction_improvements
        )

    def calculate_competitive_advantage_score(
        self, performance_metrics: Dict[str, Any]
    ) -> float:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Calculate competitive advantage score using processor
        """
        return self.processor.calculate_competitive_advantage_score(performance_metrics)

    def validate_calculation_accuracy(
        self, report: BusinessImpactReport
    ) -> Dict[str, float]:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Validate calculation accuracy using processor
        """
        return self.processor.validate_calculation_accuracy(report)

    def generate_trend_analysis(
        self, metrics: List[str], time_period: str
    ) -> Dict[str, Any]:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        Generate trend analysis using processor
        """
        return self.processor.generate_trend_analysis(metrics, time_period)

    def health_check(self) -> Dict[str, Any]:
        """
        🏗️ Sequential Thinking Phase 5.1.3: Delegate to BusinessIntelligenceProcessor
        System health check using processor
        """
        return self.processor.health_check()


# Factory function for backward compatibility
def create_business_value_calculator() -> BusinessValueCalculator:
    """
    🏗️ Sequential Thinking Phase 5.1.3: Factory function preserved for compatibility
    Create BusinessValueCalculator instance
    """
    return BusinessValueCalculator()
