"""
Enhanced Predictive Engine - Phase 11 Advanced AI Intelligence

Martin | Platform Architecture with MCP Sequential enhancement
Building on Phase 10 foundation (16 directories, 32/32 P0 tests, enterprise architecture)

This module extends the DecisionIntelligenceOrchestrator with predictive capabilities:
- Strategic decision outcome prediction (85%+ accuracy target)
- Team collaboration forecasting (2-week advance warnings)
- Initiative health prediction (80%+ outcome accuracy)
- Context-aware recommendation engine (90%+ relevance)
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import structlog
import json
import statistics

# Import existing Phase 10 foundation
try:
    from .decision_orchestrator import (
        DecisionIntelligenceOrchestrator,
        DecisionContext,
        DecisionIntelligenceResult,
        DecisionComplexity,
    )
    from ..transparency.integrated_transparency import TransparencyContext
except ImportError:
    # Graceful fallback for testing environments
    class DecisionIntelligenceOrchestrator:
        def __init__(self, *args, **kwargs):
            self.is_available = False

    class DecisionContext:
        def __init__(self, *args, **kwargs):
            self.complexity = "medium"
            self.persona = "diego"

    class DecisionIntelligenceResult:
        def __init__(self, *args, **kwargs):
            self.success = True

    class DecisionComplexity(Enum):
        SIMPLE = "simple"
        MEDIUM = "medium"
        COMPLEX = "complex"

    class TransparencyContext:
        def __init__(self, *args, **kwargs):
            self.persona = "diego"


logger = structlog.get_logger(__name__)


class PredictionType(Enum):
    """Types of predictions supported by the engine"""

    DECISION_OUTCOME = "decision_outcome"
    TEAM_COLLABORATION = "team_collaboration"
    INITIATIVE_HEALTH = "initiative_health"
    STRATEGIC_CHALLENGE = "strategic_challenge"
    FRAMEWORK_EFFECTIVENESS = "framework_effectiveness"


class PredictionConfidence(Enum):
    """Confidence levels for predictions"""

    HIGH = "high"  # 85%+ accuracy
    MEDIUM = "medium"  # 70-85% accuracy
    LOW = "low"  # 50-70% accuracy
    UNCERTAIN = "uncertain"  # <50% accuracy


@dataclass
class PredictionFeatures:
    """Feature set for predictive modeling"""

    # Historical data features
    historical_patterns: Dict[str, Any] = field(default_factory=dict)
    decision_context: Dict[str, Any] = field(default_factory=dict)
    team_dynamics: Dict[str, Any] = field(default_factory=dict)
    organizational_state: Dict[str, Any] = field(default_factory=dict)

    # Time-based features
    timeline_pressure: float = 0.0
    resource_availability: float = 1.0
    stakeholder_engagement: float = 0.5

    # Strategic context features
    strategic_alignment: float = 0.5
    complexity_score: float = 0.5
    precedent_similarity: float = 0.0


@dataclass
class PredictionResult:
    """Result of a predictive analysis"""

    prediction_type: PredictionType
    predicted_outcome: str
    confidence: PredictionConfidence
    confidence_score: float  # 0.0-1.0
    reasoning: List[str]
    contributing_factors: Dict[str, float]
    risk_factors: List[str]
    mitigation_suggestions: List[str]
    timeline_estimate: Optional[str] = None
    probability_distribution: Dict[str, float] = field(default_factory=dict)

    # Metadata
    prediction_timestamp: datetime = field(default_factory=datetime.now)
    model_version: str = "1.0.0"
    transparency_trail: List[str] = field(default_factory=list)


@dataclass
class StrategicChallengePrediction:
    """Prediction for upcoming strategic challenges"""

    challenge_type: str
    probability: float
    expected_timeline: str
    impact_severity: str
    affected_areas: List[str]
    early_warning_indicators: List[str]
    recommended_preparation: List[str]


class EnhancedPredictiveEngine:
    """
    🧠 PHASE 11: Enhanced Predictive Engine

    Extends DecisionIntelligenceOrchestrator with predictive capabilities:
    - Strategic decision outcome prediction (85%+ accuracy target)
    - Team collaboration forecasting with 2-week advance warnings
    - Initiative health prediction with 80%+ outcome accuracy
    - Context-aware recommendations with 90%+ relevance rate

    Built on Phase 10 enterprise foundation with MCP Sequential enhancement.
    """

    def __init__(
        self,
        decision_orchestrator: Optional[DecisionIntelligenceOrchestrator] = None,
        enable_ml_models: bool = True,
    ):
        """
        Initialize Enhanced Predictive Engine

        Args:
            decision_orchestrator: Existing decision intelligence foundation
            enable_ml_models: Enable machine learning models (requires dependencies)
        """
        # Foundation from Phase 10
        self.decision_orchestrator = (
            decision_orchestrator or DecisionIntelligenceOrchestrator()
        )
        self.enable_ml_models = enable_ml_models

        # Predictive capabilities
        self.prediction_models = self._initialize_prediction_models()
        self.feature_extractors = self._initialize_feature_extractors()
        self.historical_data = self._initialize_historical_data()

        # Performance tracking
        self.prediction_metrics = {
            "predictions_made": 0,
            "accuracy_score": 0.0,
            "avg_confidence": 0.0,
            "avg_processing_time_ms": 0,
        }

        logger.info(
            "enhanced_predictive_engine_initialized",
            ml_models_enabled=enable_ml_models,
            prediction_types=len(PredictionType),
            foundation_orchestrator=bool(decision_orchestrator),
        )

    def _initialize_prediction_models(self) -> Dict[PredictionType, Any]:
        """Initialize prediction models for each prediction type"""
        models = {}

        for prediction_type in PredictionType:
            # Start with rule-based models, upgrade to ML later
            models[prediction_type] = {
                "type": "rule_based",
                "accuracy": 0.75,  # Conservative baseline
                "rules": self._get_rules_for_prediction_type(prediction_type),
            }

        return models

    def _initialize_feature_extractors(self) -> Dict[str, Any]:
        """Initialize feature extraction functions"""
        return {
            "historical": self._extract_historical_features,
            "contextual": self._extract_contextual_features,
            "organizational": self._extract_organizational_features,
            "temporal": self._extract_temporal_features,
        }

    def _initialize_historical_data(self) -> Dict[str, List[Any]]:
        """Initialize historical data storage for pattern learning"""
        return {
            "decisions": [],
            "outcomes": [],
            "team_interactions": [],
            "initiative_results": [],
            "framework_effectiveness": [],
        }

    def _get_rules_for_prediction_type(
        self, prediction_type: PredictionType
    ) -> List[str]:
        """Get rule-based logic for each prediction type"""
        rules = {
            PredictionType.DECISION_OUTCOME: [
                "High stakeholder engagement + clear framework → success_likely",
                "Low stakeholder engagement + complex timeline → risk_high",
                "Strong historical precedent + aligned resources → confidence_high",
            ],
            PredictionType.TEAM_COLLABORATION: [
                "Communication frequency drop + deadline pressure → coordination_risk",
                "Cross-team dependencies + unclear ownership → conflict_likely",
                "Strong leadership presence + clear processes → success_likely",
            ],
            PredictionType.INITIATIVE_HEALTH: [
                "Budget variance >20% + timeline slip → health_declining",
                "Stakeholder disengagement + resource constraints → failure_risk",
                "Consistent progress + stakeholder satisfaction → success_track",
            ],
            PredictionType.STRATEGIC_CHALLENGE: [
                "Market changes + internal resistance → adaptation_challenge",
                "Resource constraints + growth pressure → scaling_challenge",
                "Technology debt + feature velocity → technical_challenge",
            ],
            PredictionType.FRAMEWORK_EFFECTIVENESS: [
                "Framework complexity + team experience → adoption_prediction",
                "Historical success rate + current context → effectiveness_score",
                "Stakeholder buy-in + clear benefits → implementation_success",
            ],
        }
        return rules.get(prediction_type, [])

    async def predict_decision_outcome(
        self, decision_context: DecisionContext, user_input: str
    ) -> PredictionResult:
        """
        Predict the outcome of a strategic decision

        Args:
            decision_context: Context from decision orchestrator
            user_input: Original user query

        Returns:
            PredictionResult with outcome prediction and confidence
        """
        start_time = time.time()

        try:
            # Extract features for prediction
            features = await self._extract_prediction_features(
                decision_context, user_input, PredictionType.DECISION_OUTCOME
            )

            # Apply prediction model
            prediction_result = await self._apply_prediction_model(
                PredictionType.DECISION_OUTCOME, features
            )

            # Enhance with MCP Sequential analysis for complex decisions
            if decision_context.complexity == DecisionComplexity.COMPLEX:
                prediction_result = await self._enhance_with_mcp_analysis(
                    prediction_result, decision_context
                )

            # Update metrics
            processing_time = int((time.time() - start_time) * 1000)
            self._update_prediction_metrics(
                processing_time, prediction_result.confidence_score
            )

            logger.info(
                "decision_outcome_predicted",
                prediction_type="decision_outcome",
                confidence=prediction_result.confidence.value,
                processing_time_ms=processing_time,
            )

            return prediction_result

        except Exception as e:
            logger.error("decision_outcome_prediction_failed", error=str(e))
            return self._create_fallback_prediction(
                PredictionType.DECISION_OUTCOME, f"Prediction failed: {e}"
            )

    async def predict_team_collaboration_challenges(
        self, team_context: Dict[str, Any], timeline_weeks: int = 2
    ) -> List[StrategicChallengePrediction]:
        """
        Predict potential team collaboration challenges

        Args:
            team_context: Current team state and dynamics
            timeline_weeks: Prediction timeline (default 2 weeks)

        Returns:
            List of predicted challenges with advance warning
        """
        try:
            # Extract collaboration features
            features = self._extract_collaboration_features(team_context)

            # Apply collaboration prediction model
            challenges = await self._predict_collaboration_patterns(
                features, timeline_weeks
            )

            # Filter for high-confidence predictions
            significant_challenges = [
                challenge
                for challenge in challenges
                if challenge.probability > 0.7  # High confidence threshold
            ]

            logger.info(
                "collaboration_challenges_predicted",
                challenges_count=len(significant_challenges),
                timeline_weeks=timeline_weeks,
                high_risk_count=len(
                    [c for c in significant_challenges if c.impact_severity == "high"]
                ),
            )

            return significant_challenges

        except Exception as e:
            logger.error("collaboration_prediction_failed", error=str(e))
            return []

    async def predict_initiative_health(
        self, initiative_data: Dict[str, Any]
    ) -> PredictionResult:
        """
        Predict initiative health and success probability

        Args:
            initiative_data: Current initiative state and metrics

        Returns:
            PredictionResult with health prediction and risk factors
        """
        try:
            # Extract initiative features
            features = self._extract_initiative_features(initiative_data)

            # Apply health prediction model
            prediction_result = await self._apply_prediction_model(
                PredictionType.INITIATIVE_HEALTH, features
            )

            # Add specific health indicators
            health_score = self._calculate_health_score(features)
            prediction_result.contributing_factors["health_score"] = health_score

            # Risk factor analysis
            risk_factors = self._analyze_risk_factors(features)
            prediction_result.risk_factors.extend(risk_factors)

            logger.info(
                "initiative_health_predicted",
                health_score=health_score,
                confidence=prediction_result.confidence.value,
                risk_factors_count=len(risk_factors),
            )

            return prediction_result

        except Exception as e:
            logger.error("initiative_health_prediction_failed", error=str(e))
            return self._create_fallback_prediction(
                PredictionType.INITIATIVE_HEALTH, f"Health prediction failed: {e}"
            )

    async def generate_context_aware_recommendations(
        self, context: Dict[str, Any], prediction_results: List[PredictionResult]
    ) -> List[str]:
        """
        Generate context-aware recommendations based on predictions

        Args:
            context: Current organizational and situational context
            prediction_results: Results from various predictions

        Returns:
            List of actionable recommendations
        """
        recommendations = []

        try:
            # Analyze prediction patterns
            high_risk_predictions = [
                pred for pred in prediction_results if pred.confidence_score > 0.8
            ]

            # Generate contextual recommendations
            for prediction in high_risk_predictions:
                contextual_recs = self._generate_contextual_recommendations(
                    prediction, context
                )
                recommendations.extend(contextual_recs)

            # Add proactive recommendations
            proactive_recs = self._generate_proactive_recommendations(context)
            recommendations.extend(proactive_recs)

            # Deduplicate and prioritize
            recommendations = list(set(recommendations))
            recommendations = self._prioritize_recommendations(recommendations, context)

            logger.info(
                "context_aware_recommendations_generated",
                recommendations_count=len(recommendations),
                high_risk_predictions=len(high_risk_predictions),
            )

            return recommendations[:10]  # Return top 10 recommendations

        except Exception as e:
            logger.error("recommendation_generation_failed", error=str(e))
            return ["Unable to generate recommendations due to system error"]

    # === FEATURE EXTRACTION METHODS ===

    async def _extract_prediction_features(
        self,
        decision_context: DecisionContext,
        user_input: str,
        prediction_type: PredictionType,
    ) -> PredictionFeatures:
        """Extract features for prediction modeling"""
        features = PredictionFeatures()

        # Extract historical patterns
        features.historical_patterns = self._extract_historical_features(
            decision_context, prediction_type
        )

        # Extract decision context features
        features.decision_context = {
            "complexity": decision_context.complexity.value,
            "persona": decision_context.persona,
            "user_input_length": len(user_input),
            "urgency_indicators": self._detect_urgency_indicators(user_input),
        }

        # Extract organizational features
        features.organizational_state = self._extract_organizational_features(
            decision_context
        )

        # Calculate derived features
        features.complexity_score = self._calculate_complexity_score(decision_context)
        features.strategic_alignment = self._calculate_strategic_alignment(
            decision_context
        )

        return features

    def _extract_historical_features(
        self, context: Any, prediction_type: PredictionType
    ) -> Dict[str, Any]:
        """Extract historical pattern features"""
        return {
            "similar_decisions_count": len(self.historical_data.get("decisions", [])),
            "success_rate": 0.75,  # Placeholder - would come from actual historical data
            "pattern_confidence": 0.8,
        }

    def _extract_contextual_features(self, context: Any) -> Dict[str, Any]:
        """Extract contextual features"""
        return {
            "stakeholder_count": getattr(context, "stakeholder_count", 3),
            "timeline_pressure": 0.5,  # Normalized timeline pressure
            "resource_availability": 0.8,  # Resource availability score
        }

    def _extract_organizational_features(self, context: Any) -> Dict[str, Any]:
        """Extract organizational state features"""
        return {
            "team_size": 5,  # Default team size
            "organizational_health": 0.8,
            "change_velocity": 0.6,
            "communication_effectiveness": 0.7,
        }

    def _extract_temporal_features(self, context: Any) -> Dict[str, Any]:
        """Extract time-based features"""
        now = datetime.now()
        return {
            "time_of_day": now.hour,
            "day_of_week": now.weekday(),
            "quarter_progress": (now.month - 1) // 3,
        }

    def _extract_collaboration_features(
        self, team_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract team collaboration features"""
        return {
            "communication_frequency": team_context.get("communication_frequency", 0.5),
            "cross_team_dependencies": team_context.get("dependencies", []),
            "leadership_visibility": team_context.get("leadership_visibility", 0.7),
            "process_clarity": team_context.get("process_clarity", 0.6),
        }

    def _extract_initiative_features(
        self, initiative_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract initiative health features"""
        return {
            "budget_variance": initiative_data.get("budget_variance", 0.0),
            "timeline_variance": initiative_data.get("timeline_variance", 0.0),
            "stakeholder_satisfaction": initiative_data.get(
                "stakeholder_satisfaction", 0.7
            ),
            "progress_velocity": initiative_data.get("progress_velocity", 0.6),
            "risk_indicators": initiative_data.get("risk_indicators", []),
        }

    # === PREDICTION MODEL APPLICATION ===

    async def _apply_prediction_model(
        self, prediction_type: PredictionType, features: PredictionFeatures
    ) -> PredictionResult:
        """Apply prediction model to features"""
        model = self.prediction_models[prediction_type]

        if model["type"] == "rule_based":
            return await self._apply_rule_based_model(prediction_type, features, model)
        elif model["type"] == "ml_model" and self.enable_ml_models:
            return await self._apply_ml_model(prediction_type, features, model)
        else:
            # Fallback to rule-based
            return await self._apply_rule_based_model(prediction_type, features, model)

    async def _apply_rule_based_model(
        self,
        prediction_type: PredictionType,
        features: PredictionFeatures,
        model: Dict[str, Any],
    ) -> PredictionResult:
        """Apply rule-based prediction model"""
        # Simulate rule-based logic
        confidence_score = 0.75  # Base confidence for rule-based models

        # Adjust confidence based on features
        if features.strategic_alignment > 0.8:
            confidence_score += 0.1
        if features.complexity_score < 0.3:
            confidence_score += 0.05

        confidence_score = min(confidence_score, 0.95)  # Cap at 95%

        # Determine confidence level
        if confidence_score >= 0.85:
            confidence = PredictionConfidence.HIGH
        elif confidence_score >= 0.70:
            confidence = PredictionConfidence.MEDIUM
        else:
            confidence = PredictionConfidence.LOW

        # Generate prediction outcome
        outcome = self._generate_outcome_for_type(prediction_type, features)

        return PredictionResult(
            prediction_type=prediction_type,
            predicted_outcome=outcome,
            confidence=confidence,
            confidence_score=confidence_score,
            reasoning=self._generate_reasoning(prediction_type, features),
            contributing_factors=self._extract_contributing_factors(features),
            risk_factors=self._identify_risk_factors(features),
            mitigation_suggestions=self._generate_mitigation_suggestions(
                prediction_type, features
            ),
            transparency_trail=[
                f"Rule-based model applied for {prediction_type.value}"
            ],
        )

    def _generate_outcome_for_type(
        self, prediction_type: PredictionType, features: PredictionFeatures
    ) -> str:
        """Generate predicted outcome based on prediction type"""
        outcomes = {
            PredictionType.DECISION_OUTCOME: [
                "Success likely",
                "Success uncertain",
                "Risk high",
            ],
            PredictionType.TEAM_COLLABORATION: [
                "Smooth collaboration",
                "Minor friction expected",
                "Coordination challenges likely",
            ],
            PredictionType.INITIATIVE_HEALTH: [
                "Healthy progress",
                "Monitor closely",
                "Intervention needed",
            ],
            PredictionType.STRATEGIC_CHALLENGE: [
                "No challenges expected",
                "Minor challenges possible",
                "Significant challenges likely",
            ],
            PredictionType.FRAMEWORK_EFFECTIVENESS: [
                "High effectiveness",
                "Moderate effectiveness",
                "Low effectiveness",
            ],
        }

        # Simple logic based on complexity score
        outcome_list = outcomes.get(prediction_type, ["Outcome uncertain"])
        if features.complexity_score < 0.3:
            return outcome_list[0]  # Best outcome
        elif features.complexity_score < 0.7:
            return outcome_list[1] if len(outcome_list) > 1 else outcome_list[0]
        else:
            return outcome_list[-1]  # Worst outcome

    async def _enhance_with_mcp_analysis(
        self, prediction_result: PredictionResult, decision_context: DecisionContext
    ) -> PredictionResult:
        """Enhance prediction with MCP Sequential analysis"""
        try:
            # Use existing decision orchestrator for MCP enhancement
            enhanced_analysis = (
                await self.decision_orchestrator.analyze_decision_intelligence(
                    f"Analyze prediction: {prediction_result.predicted_outcome}",
                    "prediction_enhancement",
                    decision_context.persona,
                )
            )

            # Integrate MCP insights
            if enhanced_analysis.success:
                prediction_result.reasoning.append(
                    "Enhanced with MCP Sequential analysis"
                )
                prediction_result.confidence_score = min(
                    prediction_result.confidence_score + 0.05, 0.95
                )
                prediction_result.transparency_trail.append(
                    f"MCP Sequential enhancement applied via {len(enhanced_analysis.mcp_servers_used)} servers"
                )

            return prediction_result

        except Exception as e:
            logger.warning("mcp_enhancement_failed", error=str(e))
            return prediction_result

    # === UTILITY METHODS ===

    def _calculate_complexity_score(self, decision_context: DecisionContext) -> float:
        """Calculate complexity score from decision context"""
        complexity_map = {
            DecisionComplexity.SIMPLE: 0.2,
            DecisionComplexity.MEDIUM: 0.5,
            DecisionComplexity.COMPLEX: 0.8,
        }
        return complexity_map.get(decision_context.complexity, 0.5)

    def _calculate_strategic_alignment(
        self, decision_context: DecisionContext
    ) -> float:
        """Calculate strategic alignment score"""
        # Placeholder - would integrate with actual strategic context
        return 0.7

    def _calculate_health_score(self, features: Dict[str, Any]) -> float:
        """Calculate overall health score"""
        scores = []
        if "budget_variance" in features:
            scores.append(max(0, 1.0 - abs(features["budget_variance"])))
        if "stakeholder_satisfaction" in features:
            scores.append(features["stakeholder_satisfaction"])
        if "progress_velocity" in features:
            scores.append(features["progress_velocity"])

        return statistics.mean(scores) if scores else 0.5

    def _detect_urgency_indicators(self, user_input: str) -> List[str]:
        """Detect urgency indicators in user input"""
        urgency_keywords = [
            "urgent",
            "asap",
            "immediately",
            "crisis",
            "emergency",
            "deadline",
        ]
        return [
            keyword
            for keyword in urgency_keywords
            if keyword.lower() in user_input.lower()
        ]

    def _generate_reasoning(
        self, prediction_type: PredictionType, features: PredictionFeatures
    ) -> List[str]:
        """Generate reasoning for the prediction"""
        return [
            f"Based on {prediction_type.value} analysis",
            f"Complexity score: {features.complexity_score:.2f}",
            f"Strategic alignment: {features.strategic_alignment:.2f}",
            "Applied rule-based prediction model",
        ]

    def _extract_contributing_factors(
        self, features: PredictionFeatures
    ) -> Dict[str, float]:
        """Extract contributing factors with weights"""
        return {
            "complexity": features.complexity_score,
            "strategic_alignment": features.strategic_alignment,
            "resource_availability": features.resource_availability,
            "timeline_pressure": features.timeline_pressure,
        }

    def _identify_risk_factors(self, features: PredictionFeatures) -> List[str]:
        """Identify risk factors from features"""
        risks = []
        if features.complexity_score > 0.7:
            risks.append("High complexity may impact execution")
        if features.timeline_pressure > 0.8:
            risks.append("Timeline pressure may affect quality")
        if features.resource_availability < 0.5:
            risks.append("Limited resources may constrain options")
        return risks

    def _generate_mitigation_suggestions(
        self, prediction_type: PredictionType, features: PredictionFeatures
    ) -> List[str]:
        """Generate mitigation suggestions"""
        suggestions = []
        if features.complexity_score > 0.7:
            suggestions.append("Consider breaking down into smaller, manageable phases")
        if features.timeline_pressure > 0.8:
            suggestions.append("Review timeline expectations with stakeholders")
        if features.resource_availability < 0.5:
            suggestions.append("Identify additional resources or adjust scope")
        return suggestions

    async def _predict_collaboration_patterns(
        self, features: Dict[str, Any], timeline_weeks: int
    ) -> List[StrategicChallengePrediction]:
        """Predict collaboration patterns and challenges"""
        challenges = []

        # Communication frequency challenge
        if features.get("communication_frequency", 0.5) < 0.3:
            challenges.append(
                StrategicChallengePrediction(
                    challenge_type="Communication Breakdown",
                    probability=0.8,
                    expected_timeline=f"{timeline_weeks} weeks",
                    impact_severity="high",
                    affected_areas=["Team coordination", "Decision making"],
                    early_warning_indicators=[
                        "Decreased meeting frequency",
                        "Delayed responses",
                    ],
                    recommended_preparation=[
                        "Schedule regular check-ins",
                        "Clarify communication protocols",
                    ],
                )
            )

        # Cross-team dependency challenge
        if len(features.get("cross_team_dependencies", [])) > 3:
            challenges.append(
                StrategicChallengePrediction(
                    challenge_type="Dependency Coordination",
                    probability=0.7,
                    expected_timeline=f"{timeline_weeks-1} weeks",
                    impact_severity="medium",
                    affected_areas=["Timeline adherence", "Quality delivery"],
                    early_warning_indicators=[
                        "Dependency conflicts",
                        "Unclear ownership",
                    ],
                    recommended_preparation=[
                        "Map dependency chains",
                        "Establish clear owners",
                    ],
                )
            )

        return challenges

    def _generate_contextual_recommendations(
        self, prediction: PredictionResult, context: Dict[str, Any]
    ) -> List[str]:
        """Generate contextual recommendations based on prediction"""
        recommendations = []

        if prediction.confidence == PredictionConfidence.HIGH:
            if "risk" in prediction.predicted_outcome.lower():
                recommendations.append(
                    "Take immediate action to mitigate identified risks"
                )
            else:
                recommendations.append(
                    "Proceed with confidence but maintain monitoring"
                )

        # Add prediction-specific recommendations
        recommendations.extend(prediction.mitigation_suggestions)

        return recommendations

    def _generate_proactive_recommendations(self, context: Dict[str, Any]) -> List[str]:
        """Generate proactive recommendations based on context"""
        return [
            "Establish regular health check cadence",
            "Document decision rationale for future reference",
            "Plan stakeholder communication strategy",
        ]

    def _prioritize_recommendations(
        self, recommendations: List[str], context: Dict[str, Any]
    ) -> List[str]:
        """Prioritize recommendations based on context"""
        # Simple prioritization - would be more sophisticated in production
        priority_keywords = ["immediate", "urgent", "risk", "stakeholder"]
        prioritized = []
        standard = []

        for rec in recommendations:
            if any(keyword in rec.lower() for keyword in priority_keywords):
                prioritized.append(rec)
            else:
                standard.append(rec)

        return prioritized + standard

    def _analyze_risk_factors(self, features: Dict[str, Any]) -> List[str]:
        """Analyze risk factors from initiative features"""
        risks = []
        if features.get("budget_variance", 0) > 0.2:
            risks.append("Budget overrun risk")
        if features.get("timeline_variance", 0) > 0.15:
            risks.append("Timeline delay risk")
        if features.get("stakeholder_satisfaction", 1.0) < 0.6:
            risks.append("Stakeholder disengagement risk")
        return risks

    def _create_fallback_prediction(
        self, prediction_type: PredictionType, error_message: str
    ) -> PredictionResult:
        """Create fallback prediction when errors occur"""
        return PredictionResult(
            prediction_type=prediction_type,
            predicted_outcome="Unable to generate prediction",
            confidence=PredictionConfidence.UNCERTAIN,
            confidence_score=0.0,
            reasoning=[f"Prediction failed: {error_message}"],
            contributing_factors={},
            risk_factors=["Prediction system error"],
            mitigation_suggestions=["Manual analysis recommended"],
            transparency_trail=[f"Fallback prediction due to error: {error_message}"],
        )

    def _update_prediction_metrics(
        self, processing_time_ms: int, confidence_score: float
    ):
        """Update prediction performance metrics"""
        self.prediction_metrics["predictions_made"] += 1

        # Update average processing time
        prev_avg = self.prediction_metrics["avg_processing_time_ms"]
        count = self.prediction_metrics["predictions_made"]
        self.prediction_metrics["avg_processing_time_ms"] = (
            prev_avg * (count - 1) + processing_time_ms
        ) / count

        # Update average confidence
        prev_conf = self.prediction_metrics["avg_confidence"]
        self.prediction_metrics["avg_confidence"] = (
            prev_conf * (count - 1) + confidence_score
        ) / count

    def get_prediction_metrics(self) -> Dict[str, Any]:
        """Get current prediction performance metrics"""
        return self.prediction_metrics.copy()


# Factory function for easy integration
async def create_enhanced_predictive_engine(
    enable_ml_models: bool = True,
    decision_orchestrator: Optional[DecisionIntelligenceOrchestrator] = None,
) -> EnhancedPredictiveEngine:
    """
    🏗️ Factory for Enhanced Predictive Engine

    Creates predictive engine using existing Phase 10 foundation.

    Args:
        enable_ml_models: Enable machine learning models
        decision_orchestrator: Existing decision intelligence orchestrator

    Returns:
        EnhancedPredictiveEngine ready for predictive intelligence
    """
    if decision_orchestrator is None:
        from .decision_orchestrator import create_decision_intelligence_orchestrator

        decision_orchestrator = await create_decision_intelligence_orchestrator()

    engine = EnhancedPredictiveEngine(
        decision_orchestrator=decision_orchestrator, enable_ml_models=enable_ml_models
    )

    logger.info(
        "enhanced_predictive_engine_created",
        ml_models_enabled=enable_ml_models,
        foundation_ready=True,
    )

    return engine
