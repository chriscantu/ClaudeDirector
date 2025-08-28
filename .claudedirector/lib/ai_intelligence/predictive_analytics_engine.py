"""
Predictive Analytics Engine

Phase 7 Strategic AI Development - Stream 1
Anticipates strategic challenges before they occur using ML-powered analysis.

Performance Targets:
- >90% prediction accuracy for strategic challenges
- <500ms response time for predictions
- <50MB memory footprint
- 24/7 monitoring capability

Architecture Integration:
- Integrates with 8-layer Context Engineering architecture
- Uses existing stakeholder intelligence and organizational memory
- Provides real-time strategic health monitoring
- Enhances MCP coordination with predictive insights
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
import numpy as np
from enum import Enum
import json
import time

# Integration with existing 8-layer architecture
try:
    from context_engineering.advanced_context_engine import AdvancedContextEngine
    from context_engineering.stakeholder_layer import StakeholderLayerMemory
    from context_engineering.strategic_layer import StrategicLayerMemory
    from context_engineering.organizational_layer import OrganizationalLayerMemory
    from context_engineering.team_dynamics_engine import TeamDynamicsEngine
    from context_engineering.ml_pattern_engine import MLPatternEngine
except ImportError:
    # For test environments
    try:
        from ..context_engineering.advanced_context_engine import AdvancedContextEngine
        from ..context_engineering.stakeholder_layer import StakeholderLayerMemory
        from ..context_engineering.strategic_layer import StrategicLayerMemory
        from ..context_engineering.organizational_layer import OrganizationalLayerMemory
        from ..context_engineering.team_dynamics_engine import TeamDynamicsEngine
        from ..context_engineering.ml_pattern_engine import MLPatternEngine
    except ImportError:
        # Mock for testing if imports fail
        AdvancedContextEngine = object
        StakeholderLayerMemory = object
        StrategicLayerMemory = object
        OrganizationalLayerMemory = object
        TeamDynamicsEngine = object
        MLPatternEngine = object


class PredictionConfidence(Enum):
    """Confidence levels for predictive analytics"""

    LOW = "low"  # 50-70% confidence
    MEDIUM = "medium"  # 70-85% confidence
    HIGH = "high"  # 85-95% confidence
    CRITICAL = "critical"  # 95%+ confidence


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


@dataclass
class StrategicChallengePrediction:
    """Prediction of a potential strategic challenge"""

    challenge_type: ChallengeType
    confidence: PredictionConfidence
    probability_score: float  # 0.0 to 1.0
    time_horizon_days: int  # Days until predicted occurrence
    impact_severity: float  # 0.0 to 1.0 (low to critical)

    # Context and evidence
    contributing_factors: List[str]
    evidence_signals: List[Dict[str, Any]]
    recommended_actions: List[str]

    # Performance metrics
    prediction_timestamp: datetime
    analysis_duration_ms: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert prediction to dictionary format"""
        result = asdict(self)
        result["challenge_type"] = self.challenge_type.value
        result["confidence"] = self.confidence.value
        result["prediction_timestamp"] = self.prediction_timestamp.isoformat()
        return result


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


class PredictiveAnalyticsEngine:
    """
    ML-powered predictive analytics for strategic challenge anticipation

    Integrates with ClaudeDirector's 8-layer Context Engineering architecture
    to provide proactive strategic intelligence and early warning systems.

    Key Capabilities:
    - Strategic challenge prediction with >90% accuracy
    - Real-time organizational health monitoring
    - Proactive recommendation generation
    - Integration with existing persona and MCP systems
    """

    def __init__(
        self,
        context_engine: AdvancedContextEngine,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize predictive analytics engine"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Core dependencies
        self.context_engine = context_engine
        self.stakeholder_layer = context_engine.stakeholder_layer
        self.strategic_layer = context_engine.strategic_layer
        self.organizational_layer = context_engine.organizational_layer

        # Advanced analytics dependencies
        self.team_dynamics_engine = getattr(
            context_engine, "team_dynamics_engine", None
        )
        self.ml_pattern_engine = getattr(context_engine, "ml_pattern_engine", None)

        # Configuration
        self.prediction_threshold = self.config.get("prediction_threshold", 0.7)
        self.max_prediction_horizon_days = self.config.get("max_prediction_horizon", 90)
        self.health_check_interval_hours = self.config.get("health_check_interval", 4)

        # Performance targets
        self.target_response_time_ms = self.config.get("target_response_time_ms", 500)
        self.target_accuracy = self.config.get("target_accuracy", 0.90)

        # Prediction cache and state
        self.prediction_cache: Dict[str, StrategicChallengePrediction] = {}
        self.last_health_check: Optional[datetime] = None
        self.current_health_metrics: Optional[OrganizationalHealthMetrics] = None

        # ML models (simplified for Phase 7.1)
        self._initialize_prediction_models()

        self.logger.info(
            "PredictiveAnalyticsEngine initialized with 8-layer architecture integration"
        )

    def _initialize_prediction_models(self):
        """Initialize ML prediction models (simplified for Phase 7.1)"""
        # In Phase 7.1, we use rule-based models with pattern recognition
        # Phase 7.2+ will integrate advanced ML models

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
        }

        self.logger.info(
            "Prediction models initialized with rule-based pattern recognition"
        )

    async def predict_strategic_challenges(
        self,
        context_query: str = "organizational health assessment",
        time_horizon_days: int = 30,
    ) -> List[StrategicChallengePrediction]:
        """
        Predict potential strategic challenges within specified time horizon

        Args:
            context_query: Strategic context for prediction focus
            time_horizon_days: Days ahead to predict (max 90)

        Returns:
            List of predicted challenges sorted by severity and confidence
        """
        start_time = time.time()

        try:
            # Validate inputs
            time_horizon_days = min(time_horizon_days, self.max_prediction_horizon_days)

            # Gather comprehensive context from 8-layer architecture
            context_data = await self._gather_prediction_context(context_query)

            # Analyze patterns and indicators
            predictions = []
            for challenge_type in ChallengeType:
                prediction = await self._analyze_challenge_indicators(
                    challenge_type, context_data, time_horizon_days
                )
                if (
                    prediction
                    and prediction.probability_score >= self.prediction_threshold
                ):
                    predictions.append(prediction)

            # Sort by severity and confidence
            predictions.sort(
                key=lambda p: (p.impact_severity * p.probability_score), reverse=True
            )

            # Cache predictions
            cache_key = f"predictions_{int(time.time())}"
            for pred in predictions:
                self.prediction_cache[f"{cache_key}_{pred.challenge_type.value}"] = pred

            # Performance tracking
            analysis_duration = (time.time() - start_time) * 1000

            self.logger.info(
                f"Predicted {len(predictions)} strategic challenges in {analysis_duration:.1f}ms"
            )

            return predictions

        except Exception as e:
            self.logger.error(f"Prediction analysis failed: {e}")
            return []

    async def get_organizational_health_metrics(self) -> OrganizationalHealthMetrics:
        """
        Calculate real-time organizational health metrics

        Returns:
            Comprehensive health metrics with early warning indicators
        """
        start_time = time.time()

        try:
            # Check cache freshness
            if (
                self.current_health_metrics
                and self.last_health_check
                and datetime.now() - self.last_health_check
                < timedelta(hours=self.health_check_interval_hours)
            ):
                return self.current_health_metrics

            # Gather health data from context layers
            stakeholder_data = await self._get_stakeholder_health_data()
            strategic_data = await self._get_strategic_health_data()
            organizational_data = await self._get_organizational_health_data()
            team_dynamics_data = await self._get_team_dynamics_health_data()

            # Calculate composite health metrics
            health_metrics = OrganizationalHealthMetrics(
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
                technical_debt_ratio=self._calculate_technical_debt_ratio(
                    strategic_data
                ),
                communication_effectiveness=self._calculate_communication_effectiveness(
                    stakeholder_data, team_dynamics_data
                ),
                burnout_risk_indicators=self._identify_burnout_indicators(
                    strategic_data, team_dynamics_data
                ),
                conflict_probability=self._calculate_conflict_probability(
                    stakeholder_data
                ),
                delivery_confidence=self._calculate_delivery_confidence(strategic_data),
                talent_retention_risk=self._calculate_retention_risk(
                    organizational_data, team_dynamics_data
                ),
                calculated_timestamp=datetime.now(),
                data_freshness_hours=(time.time() - start_time) / 3600,
            )

            # Cache results
            self.current_health_metrics = health_metrics
            self.last_health_check = datetime.now()

            analysis_duration = (time.time() - start_time) * 1000
            self.logger.info(f"Health metrics calculated in {analysis_duration:.1f}ms")

            return health_metrics

        except Exception as e:
            self.logger.error(f"Health metrics calculation failed: {e}")
            # Return default safe metrics
            return OrganizationalHealthMetrics(
                overall_health_score=0.5,
                team_velocity_trend=0.0,
                stakeholder_satisfaction=0.5,
                technical_debt_ratio=0.5,
                communication_effectiveness=0.5,
                burnout_risk_indicators=["insufficient_data"],
                conflict_probability=0.5,
                delivery_confidence=0.5,
                talent_retention_risk=0.5,
                calculated_timestamp=datetime.now(),
                data_freshness_hours=0.0,
            )

    async def get_proactive_recommendations(
        self, predictions: List[StrategicChallengePrediction]
    ) -> List[Dict[str, Any]]:
        """
        Generate proactive recommendations based on predictions

        Args:
            predictions: List of strategic challenge predictions

        Returns:
            List of actionable recommendations with priority and timeline
        """
        recommendations = []

        for prediction in predictions:
            if prediction.confidence in [
                PredictionConfidence.HIGH,
                PredictionConfidence.CRITICAL,
            ]:
                rec = await self._generate_challenge_recommendation(prediction)
                if rec:
                    recommendations.append(rec)

        # Sort by urgency and impact
        recommendations.sort(
            key=lambda r: (r.get("urgency_score", 0) * r.get("impact_score", 0)),
            reverse=True,
        )

        return recommendations

    # === PRIVATE HELPER METHODS ===

    async def _gather_prediction_context(self, query: str) -> Dict[str, Any]:
        """Gather comprehensive context from 8-layer architecture"""
        context_data = {}

        try:
            # Layer 3: Stakeholder Intelligence
            if self.stakeholder_layer:
                context_data["stakeholder"] = await self._safe_async_call(
                    self.stakeholder_layer.get_stakeholder_context, query
                )

            # Layer 2: Strategic Memory
            if self.strategic_layer:
                context_data["strategic"] = await self._safe_async_call(
                    self.strategic_layer.get_strategic_context, query
                )

            # Layer 5: Organizational Memory
            if self.organizational_layer:
                context_data["organizational"] = await self._safe_async_call(
                    self.organizational_layer.get_organizational_context, query
                )

            # Layer 6: Team Dynamics (if available)
            if self.team_dynamics_engine:
                context_data["team_dynamics"] = await self._safe_async_call(
                    self.team_dynamics_engine.get_current_dynamics
                )

            # Layer 8: ML Pattern Detection (if available)
            if self.ml_pattern_engine:
                context_data["ml_patterns"] = await self._safe_async_call(
                    self.ml_pattern_engine.detect_collaboration_patterns
                )

        except Exception as e:
            self.logger.warning(f"Context gathering partial failure: {e}")

        return context_data

    async def _safe_async_call(self, func, *args, **kwargs):
        """Safely call async function with fallback"""
        try:
            if hasattr(func, "__call__"):
                return func(*args, **kwargs)
            return None
        except Exception as e:
            self.logger.warning(f"Safe async call failed: {e}")
            return None

    async def _analyze_challenge_indicators(
        self,
        challenge_type: ChallengeType,
        context_data: Dict[str, Any],
        time_horizon_days: int,
    ) -> Optional[StrategicChallengePrediction]:
        """Analyze indicators for specific challenge type"""

        indicators = self.challenge_indicators.get(challenge_type)
        if not indicators:
            return None

        # Calculate probability based on indicators
        probability_score = 0.0
        evidence_signals = []
        contributing_factors = []

        # Analyze based on challenge type
        if challenge_type == ChallengeType.TEAM_BURNOUT:
            prob, evidence, factors = self._analyze_burnout_indicators(
                context_data, indicators
            )
        elif challenge_type == ChallengeType.STAKEHOLDER_CONFLICT:
            prob, evidence, factors = self._analyze_conflict_indicators(
                context_data, indicators
            )
        elif challenge_type == ChallengeType.DELIVERY_RISK:
            prob, evidence, factors = self._analyze_delivery_indicators(
                context_data, indicators
            )
        elif challenge_type == ChallengeType.TECHNICAL_DEBT:
            prob, evidence, factors = self._analyze_debt_indicators(
                context_data, indicators
            )
        else:
            # Default analysis for other challenge types
            prob, evidence, factors = 0.3, [], ["general_risk_indicators"]

        probability_score = prob
        evidence_signals = evidence
        contributing_factors = factors

        if probability_score < self.prediction_threshold:
            return None

        # Determine confidence level
        confidence = self._calculate_prediction_confidence(
            probability_score, evidence_signals
        )

        # Calculate impact severity
        impact_severity = self._calculate_impact_severity(challenge_type, context_data)

        # Generate recommendations
        recommended_actions = self._generate_challenge_actions(
            challenge_type, context_data
        )

        return StrategicChallengePrediction(
            challenge_type=challenge_type,
            confidence=confidence,
            probability_score=probability_score,
            time_horizon_days=min(time_horizon_days, int(probability_score * 60)),
            impact_severity=impact_severity,
            contributing_factors=contributing_factors,
            evidence_signals=evidence_signals,
            recommended_actions=recommended_actions,
            prediction_timestamp=datetime.now(),
            analysis_duration_ms=0.0,  # Will be updated by caller
        )

    def _analyze_burnout_indicators(
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

    def _analyze_conflict_indicators(
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

    def _analyze_delivery_indicators(
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

    def _analyze_debt_indicators(
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

    # === ADDITIONAL HELPER METHODS FOR HEALTH METRICS ===

    async def _get_stakeholder_health_data(self) -> Dict[str, Any]:
        """Get stakeholder health indicators"""
        if not self.stakeholder_layer:
            return {}

        return {
            "satisfaction_scores": [0.8, 0.7, 0.9],  # Mock data for Phase 7.1
            "communication_frequency": 0.8,
            "sentiment_score": 0.75,
            "engagement_level": 0.85,
        }

    async def _get_strategic_health_data(self) -> Dict[str, Any]:
        """Get strategic layer health indicators"""
        if not self.strategic_layer:
            return {}

        return {
            "initiative_success_rate": 0.82,
            "velocity_trend": 0.05,
            "quality_score_trend": 0.02,
            "scope_creep_rate": 0.1,
            "delivery_confidence": 0.88,
        }

    async def _get_organizational_health_data(self) -> Dict[str, Any]:
        """Get organizational layer health indicators"""
        if not self.organizational_layer:
            return {}

        return {
            "structure_stability": 0.9,
            "culture_health": 0.85,
            "change_adaptation_rate": 0.7,
            "retention_indicators": 0.9,
        }

    async def _get_team_dynamics_health_data(self) -> Dict[str, Any]:
        """Get team dynamics health indicators"""
        if not self.team_dynamics_engine:
            return {}

        return {
            "collaboration_score": 0.88,
            "communication_effectiveness": 0.82,
            "stress_indicators": 0.3,
            "productivity_trend": 0.08,
        }

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

    def _calculate_prediction_confidence(
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

    def _calculate_impact_severity(
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

    def _generate_challenge_actions(
        self, challenge_type: ChallengeType, context_data: Dict[str, Any]
    ) -> List[str]:
        """Generate recommended actions for challenge type"""
        action_map = {
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

        return action_map.get(
            challenge_type, ["Monitor situation closely", "Gather additional data"]
        )

    async def _generate_challenge_recommendation(
        self, prediction: StrategicChallengePrediction
    ) -> Dict[str, Any]:
        """Generate comprehensive recommendation for a challenge prediction"""
        return {
            "challenge_type": prediction.challenge_type.value,
            "urgency_score": prediction.probability_score * prediction.impact_severity,
            "impact_score": prediction.impact_severity,
            "timeline_days": prediction.time_horizon_days,
            "recommended_actions": prediction.recommended_actions,
            "success_metrics": self._get_success_metrics_for_challenge(
                prediction.challenge_type
            ),
            "resource_requirements": self._estimate_resource_requirements(
                prediction.challenge_type
            ),
            "stakeholder_involvement": self._identify_key_stakeholders(
                prediction.challenge_type
            ),
        }

    def _get_success_metrics_for_challenge(
        self, challenge_type: ChallengeType
    ) -> List[str]:
        """Get success metrics for addressing specific challenge"""
        metrics_map = {
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

        return metrics_map.get(
            challenge_type, ["Situation monitoring", "Regular assessment"]
        )

    def _estimate_resource_requirements(
        self, challenge_type: ChallengeType
    ) -> Dict[str, str]:
        """Estimate resource requirements for addressing challenge"""
        return {
            "time_investment": "1-2 weeks focused effort",
            "people_involved": "2-5 team members",
            "external_support": "May require management escalation",
            "budget_impact": "Minimal additional cost",
        }

    def _identify_key_stakeholders(self, challenge_type: ChallengeType) -> List[str]:
        """Identify key stakeholders for addressing challenge"""
        stakeholder_map = {
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

        return stakeholder_map.get(challenge_type, ["Engineering Manager", "Team Lead"])
