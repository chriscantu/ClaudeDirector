"""
Risk Assessment Engine - Single Responsibility Implementation

Advanced risk assessment with multi-factor analysis for collaboration success
prediction. Follows Single Responsibility Principle by focusing exclusively
on risk calculation, mitigation recommendations, and timeline prediction.

Phase: Phase 3A.1.4c - ML Models Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

import logging
from typing import Dict, List, Optional

# Import types from centralized types module
from ..ml_pattern_types import (
    CollaborationOutcome,
    FeatureVector,
    CollaborationPrediction,
    TeamCollaborationOutcome,
    EnsembleModelConfig,
    RiskAssessment,
)

# Configure logging
logger = logging.getLogger(__name__)


class RiskAssessmentEngine:
    """
    Advanced risk assessment with multi-factor analysis.

    Single Responsibility: Risk assessment and mitigation recommendations only.
    Focuses exclusively on analyzing collaboration risks and generating
    actionable mitigation strategies.
    """

    def __init__(self, config: Optional[EnsembleModelConfig] = None):
        """
        Initialize risk assessment engine with configuration.

        Args:
            config: Optional ensemble model configuration for risk weighting
        """
        self.config = config or EnsembleModelConfig()
        self.risk_factors = {
            "communication_risk": 0.25,
            "temporal_risk": 0.20,
            "network_risk": 0.20,
            "contextual_risk": 0.15,
            "historical_risk": 0.20,
        }

    def calculate_risk_assessment(
        self,
        prediction: CollaborationPrediction,
        features: FeatureVector,
        historical_data: Optional[List[TeamCollaborationOutcome]] = None,
    ) -> RiskAssessment:
        """
        Calculate comprehensive risk assessment with multi-factor analysis.

        Args:
            prediction: Base collaboration prediction
            features: Feature vector from team interactions
            historical_data: Optional historical collaboration outcomes

        Returns:
            RiskAssessment with overall risk score and mitigation recommendations
        """
        try:
            # Calculate individual risk factors
            risk_scores = {}

            # Communication risk - based on frequency and responsiveness
            comm_freq = features.communication_features.get(
                "communication_frequency", 0
            )
            risk_scores["communication_risk"] = max(0.0, 1.0 - comm_freq)

            # Temporal risk - based on timing patterns and consistency
            temporal_alignment = features.temporal_features.get("time_alignment", 0)
            risk_scores["temporal_risk"] = max(0.0, 1.0 - temporal_alignment)

            # Network risk - based on connectivity issues
            network_connectivity = features.network_features.get(
                "network_connectivity", 0
            )
            risk_scores["network_risk"] = max(0.0, 1.0 - network_connectivity)

            # Contextual risk - based on project complexity factors
            complexity_score = features.contextual_features.get(
                "project_complexity", 0.5
            )
            risk_scores["contextual_risk"] = min(1.0, complexity_score)

            # Historical risk - based on past outcomes
            if historical_data:
                failure_rate = self._calculate_historical_failure_rate(historical_data)
                risk_scores["historical_risk"] = failure_rate
            else:
                risk_scores["historical_risk"] = 0.5  # Default moderate risk

            # Calculate overall risk score (weighted average)
            overall_risk = sum(
                risk_scores[factor] * weight
                for factor, weight in self.risk_factors.items()
            )

            # Generate mitigation recommendations
            recommendations = self._generate_mitigation_recommendations(risk_scores)

            # Calculate confidence interval
            base_confidence = prediction.confidence_score
            confidence_interval = (
                max(0.0, base_confidence - 0.1),
                min(1.0, base_confidence + 0.1),
            )

            # Timeline prediction
            timeline = self._predict_timeline_risk(overall_risk, features)

            return RiskAssessment(
                overall_risk_score=overall_risk,
                risk_factors=risk_scores,
                mitigation_recommendations=recommendations,
                confidence_interval=confidence_interval,
                timeline_prediction=timeline,
            )

        except Exception as e:
            logger.error(f"Error in risk assessment calculation: {e}")
            # Return default moderate risk assessment
            return RiskAssessment(
                overall_risk_score=0.5,
                risk_factors={factor: 0.5 for factor in self.risk_factors.keys()},
                mitigation_recommendations=["Review team coordination patterns"],
                confidence_interval=(0.3, 0.7),
                timeline_prediction="2-3 weeks",
            )

    def _calculate_historical_failure_rate(
        self, historical_data: List[TeamCollaborationOutcome]
    ) -> float:
        """
        Calculate historical failure rate from past outcomes.

        Args:
            historical_data: List of historical collaboration outcomes

        Returns:
            Float representing failure rate (0.0 = no failures, 1.0 = all failures)
        """
        if not historical_data:
            return 0.5

        total_outcomes = len(historical_data)
        failed_outcomes = sum(
            1
            for outcome in historical_data
            if outcome.outcome == CollaborationOutcome.FAILURE
        )

        return failed_outcomes / total_outcomes if total_outcomes > 0 else 0.5

    def _generate_mitigation_recommendations(
        self, risk_scores: Dict[str, float]
    ) -> List[str]:
        """
        Generate actionable mitigation recommendations based on risk factors.

        Args:
            risk_scores: Dictionary of risk factor scores

        Returns:
            List of actionable mitigation strategies
        """
        recommendations = []

        # Communication risk mitigation
        if risk_scores.get("communication_risk", 0) > 0.6:
            recommendations.append(
                "Increase communication frequency with daily standups or check-ins"
            )
            recommendations.append(
                "Establish clear communication channels and response time expectations"
            )

        # Temporal risk mitigation
        if risk_scores.get("temporal_risk", 0) > 0.6:
            recommendations.append(
                "Align team schedules and establish core collaboration hours"
            )
            recommendations.append(
                "Implement asynchronous collaboration tools and processes"
            )

        # Network risk mitigation
        if risk_scores.get("network_risk", 0) > 0.6:
            recommendations.append(
                "Strengthen team connections through cross-functional pairing"
            )
            recommendations.append("Create shared spaces for informal team interaction")

        # Contextual risk mitigation
        if risk_scores.get("contextual_risk", 0) > 0.6:
            recommendations.append(
                "Break down complex deliverables into smaller, manageable tasks"
            )
            recommendations.append("Ensure adequate resources and expertise allocation")

        # Historical risk mitigation
        if risk_scores.get("historical_risk", 0) > 0.6:
            recommendations.append(
                "Apply lessons learned from previous similar collaborations"
            )
            recommendations.append(
                "Implement additional oversight and support structures"
            )

        return recommendations or ["Continue monitoring team collaboration patterns"]

    def _predict_timeline_risk(
        self, overall_risk: float, features: FeatureVector
    ) -> str:
        """
        Predict timeline impact based on risk assessment.

        Args:
            overall_risk: Overall calculated risk score
            features: Feature vector for additional timeline analysis

        Returns:
            String describing predicted timeline impact
        """
        if overall_risk < 0.3:
            return "1-2 weeks (low risk)"
        elif overall_risk < 0.6:
            return "2-3 weeks (moderate risk)"
        elif overall_risk < 0.8:
            return "3-4 weeks (high risk)"
        else:
            return "4+ weeks (critical risk)"
