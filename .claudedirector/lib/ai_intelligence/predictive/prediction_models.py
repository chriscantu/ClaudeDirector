"""
Prediction Models for Strategic Challenge Analysis

Lightweight ML models and rule-based indicators for Phase 7.1
"""

from typing import Dict, List, Any, Tuple
from enum import Enum
import logging


class ChallengeType(Enum):
    """Types of strategic challenges that can be predicted"""

    TEAM_BURNOUT = "team_burnout"
    STAKEHOLDER_CONFLICT = "stakeholder_conflict"
    DELIVERY_RISK = "delivery_risk"
    TECHNICAL_DEBT = "technical_debt"
    RESOURCE_SHORTAGE = "resource_shortage"
    COMMUNICATION_BREAKDOWN = "communication_breakdown"
    STRATEGIC_MISALIGNMENT = "strategic_misalignment"
    TALENT_RETENTION = "talent_retention"
    # Spec 002 FR2: Project Success Predictions (MCP Server Enhancement)
    PROJECT_SUCCESS = "project_success"


class PredictionModels:
    """
    Lightweight prediction models for strategic challenge detection

    Phase 7.1: Rule-based models with pattern recognition
    Phase 7.2+: Will integrate advanced ML models
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self._initialize_models()

    def _initialize_models(self):
        """Initialize rule-based prediction models"""
        self.challenge_indicators = {
            ChallengeType.TEAM_BURNOUT: {
                "velocity_decline_threshold": 0.15,
                "overtime_pattern_days": 14,
                "satisfaction_threshold": 0.6,
                "key_signals": [
                    "velocity_decline",
                    "overtime_pattern",
                    "satisfaction_drop",
                ],
            },
            ChallengeType.STAKEHOLDER_CONFLICT: {
                "communication_frequency_drop": 0.3,
                "sentiment_decline_threshold": 0.2,
                "decision_delay_days": 7,
                "key_signals": [
                    "communication_drop",
                    "sentiment_decline",
                    "decision_delays",
                ],
            },
            ChallengeType.DELIVERY_RISK: {
                "scope_creep_threshold": 0.2,
                "dependency_failure_rate": 0.15,
                "quality_decline_threshold": 0.25,
                "key_signals": ["scope_creep", "dependency_issues", "quality_decline"],
            },
            ChallengeType.TECHNICAL_DEBT: {
                "complexity_growth_rate": 0.1,
                "bug_fix_time_increase": 0.3,
                "new_feature_velocity_decline": 0.2,
                "key_signals": [
                    "complexity_growth",
                    "slower_bug_fixes",
                    "feature_velocity_decline",
                ],
            },
            # Spec 002 FR2: Project Success Prediction Indicators
            ChallengeType.PROJECT_SUCCESS: {
                "team_velocity_trend": 0.15,  # Positive trend required
                "stakeholder_satisfaction_min": 0.75,  # High satisfaction needed
                "scope_stability_threshold": 0.85,  # Minimal scope changes
                "quality_metrics_min": 0.80,  # Strong quality indicators
                "timeline_adherence_min": 0.90,  # On-track delivery
                "team_morale_min": 0.70,  # Healthy team dynamics
                "key_signals": [
                    "consistent_velocity",
                    "stakeholder_alignment",
                    "stable_scope",
                    "high_quality",
                    "on_schedule",
                    "team_health",
                ],
            },
        }

    def get_challenge_indicators(self, challenge_type: ChallengeType) -> Dict[str, Any]:
        """Get indicators configuration for specific challenge type"""
        return self.challenge_indicators.get(challenge_type, {})

    def calculate_base_probability(
        self, challenge_type: ChallengeType, context_data: Dict[str, Any]
    ) -> float:
        """Calculate base probability for challenge occurrence"""
        indicators = self.get_challenge_indicators(challenge_type)
        if not indicators:
            return 0.0

        # Default implementation returns moderate probability
        # Specific analyzers will provide detailed calculations
        return 0.4

    def get_prediction_confidence_threshold(self) -> float:
        """Get minimum confidence threshold for predictions"""
        return self.config.get("prediction_threshold", 0.7)

    def get_supported_challenge_types(self) -> List[ChallengeType]:
        """Get list of supported challenge types"""
        return list(self.challenge_indicators.keys())
