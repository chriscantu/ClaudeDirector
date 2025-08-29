"""
Indicator Analyzers for Strategic Challenge Prediction

Specialized analyzers for different types of strategic challenges
"""

from typing import Dict, List, Any, Tuple
import logging
from .prediction_models import ChallengeType


class IndicatorAnalyzers:
    """Collection of specialized analyzers for different challenge types"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def analyze_burnout_indicators(
        self, context_data: Dict[str, Any], indicators: Dict[str, Any]
    ) -> Tuple[float, List[Dict], List[str]]:
        """Analyze team burnout indicators"""
        probability = 0.0
        evidence = []
        factors = []

        # Check velocity decline
        strategic_data = context_data.get("strategic", {})
        if (
            "velocity_trend" in strategic_data
            and strategic_data["velocity_trend"]
            < -indicators["velocity_decline_threshold"]
        ):
            probability += 0.3
            evidence.append(
                {
                    "signal": "velocity_decline",
                    "value": strategic_data["velocity_trend"],
                }
            )
            factors.append("declining_team_velocity")

        # Check team dynamics
        team_data = context_data.get("team_dynamics", {})
        if "stress_indicators" in team_data and team_data["stress_indicators"] > 0.7:
            probability += 0.4
            evidence.append(
                {"signal": "stress_indicators", "value": team_data["stress_indicators"]}
            )
            factors.append("high_stress_levels")

        # Check organizational signals
        org_data = context_data.get("organizational", {})
        if "workload_increase" in org_data and org_data["workload_increase"] > 0.2:
            probability += 0.3
            evidence.append(
                {"signal": "workload_increase", "value": org_data["workload_increase"]}
            )
            factors.append("increased_workload")

        return min(probability, 1.0), evidence, factors

    def analyze_conflict_indicators(
        self, context_data: Dict[str, Any], indicators: Dict[str, Any]
    ) -> Tuple[float, List[Dict], List[str]]:
        """Analyze stakeholder conflict indicators"""
        probability = 0.0
        evidence = []
        factors = []

        stakeholder_data = context_data.get("stakeholder", {})

        # Check communication patterns
        if "communication_frequency" in stakeholder_data:
            freq_change = stakeholder_data.get("communication_frequency_change", 0)
            if freq_change < -indicators["communication_frequency_drop"]:
                probability += 0.4
                evidence.append(
                    {"signal": "communication_decline", "value": freq_change}
                )
                factors.append("reduced_stakeholder_communication")

        # Check sentiment indicators
        if (
            "sentiment_score" in stakeholder_data
            and stakeholder_data["sentiment_score"] < 0.4
        ):
            probability += 0.3
            evidence.append(
                {
                    "signal": "negative_sentiment",
                    "value": stakeholder_data["sentiment_score"],
                }
            )
            factors.append("stakeholder_dissatisfaction")

        # Check decision delays
        strategic_data = context_data.get("strategic", {})
        if "average_decision_time" in strategic_data:
            if (
                strategic_data["average_decision_time"]
                > indicators["decision_delay_days"]
            ):
                probability += 0.3
                evidence.append(
                    {
                        "signal": "decision_delays",
                        "value": strategic_data["average_decision_time"],
                    }
                )
                factors.append("delayed_strategic_decisions")

        return min(probability, 1.0), evidence, factors

    def analyze_delivery_indicators(
        self, context_data: Dict[str, Any], indicators: Dict[str, Any]
    ) -> Tuple[float, List[Dict], List[str]]:
        """Analyze delivery risk indicators"""
        probability = 0.0
        evidence = []
        factors = []

        strategic_data = context_data.get("strategic", {})

        # Check scope management
        if "scope_creep_rate" in strategic_data:
            if strategic_data["scope_creep_rate"] > indicators["scope_creep_threshold"]:
                probability += 0.4
                evidence.append(
                    {
                        "signal": "scope_creep",
                        "value": strategic_data["scope_creep_rate"],
                    }
                )
                factors.append("uncontrolled_scope_expansion")

        # Check dependency health
        if "dependency_failure_rate" in strategic_data:
            if (
                strategic_data["dependency_failure_rate"]
                > indicators["dependency_failure_rate"]
            ):
                probability += 0.3
                evidence.append(
                    {
                        "signal": "dependency_failures",
                        "value": strategic_data["dependency_failure_rate"],
                    }
                )
                factors.append("external_dependency_issues")

        # Check quality trends
        if "quality_score_trend" in strategic_data:
            if (
                strategic_data["quality_score_trend"]
                < -indicators["quality_decline_threshold"]
            ):
                probability += 0.3
                evidence.append(
                    {
                        "signal": "quality_decline",
                        "value": strategic_data["quality_score_trend"],
                    }
                )
                factors.append("declining_delivery_quality")

        return min(probability, 1.0), evidence, factors

    def analyze_debt_indicators(
        self, context_data: Dict[str, Any], indicators: Dict[str, Any]
    ) -> Tuple[float, List[Dict], List[str]]:
        """Analyze technical debt indicators"""
        probability = 0.0
        evidence = []
        factors = []

        strategic_data = context_data.get("strategic", {})

        # Check complexity growth
        if "code_complexity_trend" in strategic_data:
            if (
                strategic_data["code_complexity_trend"]
                > indicators["complexity_growth_rate"]
            ):
                probability += 0.3
                evidence.append(
                    {
                        "signal": "complexity_growth",
                        "value": strategic_data["code_complexity_trend"],
                    }
                )
                factors.append("increasing_system_complexity")

        # Check bug fix efficiency
        if "bug_fix_time_trend" in strategic_data:
            if (
                strategic_data["bug_fix_time_trend"]
                > indicators["bug_fix_time_increase"]
            ):
                probability += 0.4
                evidence.append(
                    {
                        "signal": "slower_bug_fixes",
                        "value": strategic_data["bug_fix_time_trend"],
                    }
                )
                factors.append("decreasing_maintenance_efficiency")

        # Check feature velocity
        if "feature_velocity_trend" in strategic_data:
            if (
                strategic_data["feature_velocity_trend"]
                < -indicators["new_feature_velocity_decline"]
            ):
                probability += 0.3
                evidence.append(
                    {
                        "signal": "feature_velocity_decline",
                        "value": strategic_data["feature_velocity_trend"],
                    }
                )
                factors.append("reduced_development_velocity")

        return min(probability, 1.0), evidence, factors

    def analyze_general_indicators(
        self, context_data: Dict[str, Any], indicators: Dict[str, Any]
    ) -> Tuple[float, List[Dict], List[str]]:
        """Default analysis for other challenge types"""
        return 0.3, [], ["general_risk_indicators"]

    def get_analyzer_for_challenge(self, challenge_type: ChallengeType):
        """Get appropriate analyzer function for challenge type"""
        analyzer_map = {
            ChallengeType.TEAM_BURNOUT: self.analyze_burnout_indicators,
            ChallengeType.STAKEHOLDER_CONFLICT: self.analyze_conflict_indicators,
            ChallengeType.DELIVERY_RISK: self.analyze_delivery_indicators,
            ChallengeType.TECHNICAL_DEBT: self.analyze_debt_indicators,
        }
        return analyzer_map.get(challenge_type, self.analyze_general_indicators)
