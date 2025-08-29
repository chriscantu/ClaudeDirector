"""
Health Metrics Calculator for Organizational Intelligence

Calculates comprehensive organizational health metrics and indicators
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import logging


@dataclass
class OrganizationalHealthMetrics:
    """Real-time organizational health indicators"""

    overall_health_score: float  # 0.0 to 1.0
    team_velocity_trend: float  # -1.0 to 1.0 (declining to improving)
    stakeholder_satisfaction: float  # 0.0 to 1.0
    technical_debt_ratio: float  # 0.0 to 1.0
    communication_effectiveness: float  # 0.0 to 1.0

    # Detailed metrics
    burnout_risk_indicators: List[str]
    conflict_probability: float
    delivery_confidence: float
    talent_retention_risk: float

    # Performance tracking
    calculated_timestamp: datetime
    data_freshness_hours: float


class HealthMetricsCalculator:
    """Calculates organizational health metrics from context data"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def calculate_health_metrics(
        self,
        stakeholder_data: Dict[str, Any],
        strategic_data: Dict[str, Any],
        organizational_data: Dict[str, Any],
        team_dynamics_data: Dict[str, Any],
        calculation_start_time: float,
    ) -> OrganizationalHealthMetrics:
        """Calculate comprehensive health metrics"""

        return OrganizationalHealthMetrics(
            overall_health_score=self._calculate_overall_health_score(
                stakeholder_data,
                strategic_data,
                organizational_data,
                team_dynamics_data,
            ),
            team_velocity_trend=self._calculate_velocity_trend(strategic_data),
            stakeholder_satisfaction=self._calculate_stakeholder_satisfaction(
                stakeholder_data
            ),
            technical_debt_ratio=self._calculate_technical_debt_ratio(strategic_data),
            communication_effectiveness=self._calculate_communication_effectiveness(
                stakeholder_data, team_dynamics_data
            ),
            burnout_risk_indicators=self._identify_burnout_indicators(
                strategic_data, team_dynamics_data
            ),
            conflict_probability=self._calculate_conflict_probability(stakeholder_data),
            delivery_confidence=self._calculate_delivery_confidence(strategic_data),
            talent_retention_risk=self._calculate_retention_risk(
                organizational_data, team_dynamics_data
            ),
            calculated_timestamp=datetime.now(),
            data_freshness_hours=(calculation_start_time) / 3600,
        )

    def _calculate_overall_health_score(self, *health_data) -> float:
        """Calculate composite organizational health score"""
        scores = []

        for data in health_data:
            if data:
                # Extract key health indicators and normalize
                data_scores = [
                    v
                    for v in data.values()
                    if isinstance(v, (int, float)) and 0 <= v <= 1
                ]
                if data_scores:
                    scores.extend(data_scores)

        return sum(scores) / len(scores) if scores else 0.5

    def _calculate_velocity_trend(self, strategic_data: Dict[str, Any]) -> float:
        """Calculate team velocity trend"""
        return strategic_data.get("velocity_trend", 0.0)

    def _calculate_stakeholder_satisfaction(
        self, stakeholder_data: Dict[str, Any]
    ) -> float:
        """Calculate stakeholder satisfaction score"""
        satisfaction_scores = stakeholder_data.get("satisfaction_scores", [0.5])
        return sum(satisfaction_scores) / len(satisfaction_scores)

    def _calculate_technical_debt_ratio(self, strategic_data: Dict[str, Any]) -> float:
        """Calculate technical debt ratio"""
        # Inverse of quality trend (higher quality = lower debt)
        quality_trend = strategic_data.get("quality_score_trend", 0.0)
        base_debt = 0.3  # Baseline debt ratio
        return max(0.0, min(1.0, base_debt - quality_trend))

    def _calculate_communication_effectiveness(
        self, stakeholder_data: Dict[str, Any], team_data: Dict[str, Any]
    ) -> float:
        """Calculate communication effectiveness score"""
        stakeholder_comm = stakeholder_data.get("communication_frequency", 0.5)
        team_comm = team_data.get("communication_effectiveness", 0.5)
        return (stakeholder_comm + team_comm) / 2

    def _identify_burnout_indicators(
        self, strategic_data: Dict[str, Any], team_data: Dict[str, Any]
    ) -> List[str]:
        """Identify burnout risk indicators"""
        indicators = []

        if strategic_data.get("velocity_trend", 0) < -0.1:
            indicators.append("declining_velocity")
        if team_data.get("stress_indicators", 0) > 0.7:
            indicators.append("high_stress_levels")
        if strategic_data.get("quality_score_trend", 0) < -0.15:
            indicators.append("quality_decline")

        return indicators or ["normal_operations"]

    def _calculate_conflict_probability(
        self, stakeholder_data: Dict[str, Any]
    ) -> float:
        """Calculate probability of stakeholder conflicts"""
        sentiment = stakeholder_data.get("sentiment_score", 0.5)
        engagement = stakeholder_data.get("engagement_level", 0.5)

        # Lower sentiment and engagement increase conflict probability
        return 1.0 - ((sentiment + engagement) / 2)

    def _calculate_delivery_confidence(self, strategic_data: Dict[str, Any]) -> float:
        """Calculate delivery confidence score"""
        return strategic_data.get("delivery_confidence", 0.5)

    def _calculate_retention_risk(
        self, org_data: Dict[str, Any], team_data: Dict[str, Any]
    ) -> float:
        """Calculate talent retention risk"""
        retention_indicators = org_data.get("retention_indicators", 0.5)
        stress_level = team_data.get("stress_indicators", 0.5)

        # Higher stress increases retention risk
        return 1.0 - ((retention_indicators + (1.0 - stress_level)) / 2)
