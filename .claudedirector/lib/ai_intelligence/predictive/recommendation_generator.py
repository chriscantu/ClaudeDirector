"""
Recommendation Generator for Strategic Challenge Predictions

Generates actionable recommendations based on challenge predictions
"""

from typing import Dict, List, Any
from enum import Enum
import logging
from .prediction_models import ChallengeType


class PredictionConfidence(Enum):
    """Confidence levels for predictive analytics"""

    LOW = "low"  # 50-70% confidence
    MEDIUM = "medium"  # 70-85% confidence
    HIGH = "high"  # 85-95% confidence
    CRITICAL = "critical"  # 95%+ confidence


class RecommendationGenerator:
    """Generates strategic recommendations based on predictions"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self._initialize_recommendation_templates()

    def _initialize_recommendation_templates(self):
        """Initialize recommendation templates for different challenge types"""
        self.action_templates = {
            ChallengeType.TEAM_BURNOUT: [
                "Implement immediate workload redistribution",
                "Schedule team retrospective to identify stressors",
                "Consider temporary resource augmentation",
                "Review and adjust sprint planning capacity",
            ],
            ChallengeType.STAKEHOLDER_CONFLICT: [
                "Schedule immediate stakeholder alignment meeting",
                "Clarify roles and decision-making authority",
                "Implement structured communication protocols",
                "Consider bringing in neutral facilitator",
            ],
            ChallengeType.DELIVERY_RISK: [
                "Conduct immediate scope review and prioritization",
                "Implement stricter change control processes",
                "Increase delivery checkpoint frequency",
                "Assess and mitigate critical dependencies",
            ],
            ChallengeType.TECHNICAL_DEBT: [
                "Allocate dedicated refactoring capacity",
                "Implement code quality gates and reviews",
                "Create technical debt tracking and prioritization",
                "Schedule architecture review sessions",
            ],
        }

        self.success_metrics_templates = {
            ChallengeType.TEAM_BURNOUT: [
                "Team satisfaction score improvement",
                "Velocity stabilization within 2 sprints",
                "Overtime reduction to <10% team capacity",
            ],
            ChallengeType.STAKEHOLDER_CONFLICT: [
                "Stakeholder alignment score >0.8",
                "Decision time reduction to <3 days",
                "Communication frequency restoration",
            ],
            ChallengeType.DELIVERY_RISK: [
                "Scope adherence >90%",
                "Dependency success rate >95%",
                "Quality metrics maintained",
            ],
        }

        self.stakeholder_templates = {
            ChallengeType.TEAM_BURNOUT: [
                "Team Lead",
                "Engineering Manager",
                "HR Partner",
            ],
            ChallengeType.STAKEHOLDER_CONFLICT: [
                "Product Manager",
                "Engineering Director",
                "Project Stakeholders",
            ],
            ChallengeType.DELIVERY_RISK: [
                "Project Manager",
                "Tech Lead",
                "Product Owner",
            ],
            ChallengeType.TECHNICAL_DEBT: [
                "Tech Lead",
                "Senior Engineers",
                "Architecture Team",
            ],
        }

    def generate_challenge_actions(
        self, challenge_type: ChallengeType, context_data: Dict[str, Any]
    ) -> List[str]:
        """Generate recommended actions for challenge type"""
        return self.action_templates.get(
            challenge_type, ["Monitor situation closely", "Gather additional data"]
        )

    def calculate_prediction_confidence(
        self, probability: float, evidence: List[Dict]
    ) -> PredictionConfidence:
        """Calculate prediction confidence based on probability and evidence quality"""
        evidence_quality = len(evidence) / 5.0  # Normalize evidence count
        confidence_score = (probability + evidence_quality) / 2

        if confidence_score >= 0.95:
            return PredictionConfidence.CRITICAL
        elif confidence_score >= 0.85:
            return PredictionConfidence.HIGH
        elif confidence_score >= 0.70:
            return PredictionConfidence.MEDIUM
        else:
            return PredictionConfidence.LOW

    def calculate_impact_severity(
        self, challenge_type: ChallengeType, context_data: Dict[str, Any]
    ) -> float:
        """Calculate impact severity for challenge type"""
        severity_map = {
            ChallengeType.TEAM_BURNOUT: 0.9,
            ChallengeType.STAKEHOLDER_CONFLICT: 0.8,
            ChallengeType.DELIVERY_RISK: 0.85,
            ChallengeType.TECHNICAL_DEBT: 0.7,
            ChallengeType.RESOURCE_SHORTAGE: 0.75,
            ChallengeType.COMMUNICATION_BREAKDOWN: 0.8,
            ChallengeType.STRATEGIC_MISALIGNMENT: 0.9,
            ChallengeType.TALENT_RETENTION: 0.85,
        }
        return severity_map.get(challenge_type, 0.5)

    def generate_comprehensive_recommendation(
        self,
        challenge_type: ChallengeType,
        probability_score: float,
        impact_severity: float,
    ) -> Dict[str, Any]:
        """Generate comprehensive recommendation for a challenge prediction"""
        return {
            "challenge_type": challenge_type.value,
            "urgency_score": probability_score * impact_severity,
            "impact_score": impact_severity,
            "recommended_actions": self.action_templates.get(
                challenge_type, ["Monitor situation closely"]
            ),
            "success_metrics": self.get_success_metrics_for_challenge(challenge_type),
            "resource_requirements": self.estimate_resource_requirements(
                challenge_type
            ),
            "stakeholder_involvement": self.identify_key_stakeholders(challenge_type),
        }

    def get_success_metrics_for_challenge(
        self, challenge_type: ChallengeType
    ) -> List[str]:
        """Get success metrics for addressing specific challenge"""
        return self.success_metrics_templates.get(
            challenge_type, ["Situation monitoring", "Regular assessment"]
        )

    def estimate_resource_requirements(
        self, challenge_type: ChallengeType
    ) -> Dict[str, str]:
        """Estimate resource requirements for addressing challenge"""
        return {
            "time_investment": "1-2 weeks focused effort",
            "people_involved": "2-5 team members",
            "external_support": "May require management escalation",
            "budget_impact": "Minimal additional cost",
        }

    def identify_key_stakeholders(self, challenge_type: ChallengeType) -> List[str]:
        """Identify key stakeholders for addressing challenge"""
        return self.stakeholder_templates.get(
            challenge_type, ["Engineering Manager", "Team Lead"]
        )
