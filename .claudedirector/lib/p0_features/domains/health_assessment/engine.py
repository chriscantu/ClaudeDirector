"""
Health Assessment Engine - SOLID Refactored

Martin's SOLID-compliant refactoring of Berny's health prediction.
Configuration-driven, follows SRP, enables dependency injection.
"""

import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import structlog

from ...shared.ai_core.interfaces import (
    IHealthPredictionEngine,
    HealthPredictionResult,
    ModelNotLoadedError,
    ValidationResult,
    PerformanceMetric,
)
from ...shared.infrastructure.config import (
    get_config,
    HealthStatus,
    RiskLevel,
    PriorityLevel,
    HealthPredictionConfig,
    PerformanceThresholds,
    RecommendationConfig,
)

logger = structlog.get_logger(__name__)


class HealthAssessmentEngine(IHealthPredictionEngine):
    """
    SOLID-compliant health assessment engine

    Single Responsibility: Focuses only on health prediction and risk assessment
    Open/Closed: Extensible via configuration without code modification
    Liskov Substitution: Consistent interface with other AI engines
    Interface Segregation: Implements only required interfaces
    Dependency Inversion: Depends on configuration abstraction
    """

    def __init__(
        self,
        config: Optional[HealthPredictionConfig] = None,
        recommendation_config: Optional[RecommendationConfig] = None,
    ):
        """
        Initialize with dependency injection (Dependency Inversion Principle)
        """
        self.config = config or get_config().health_prediction
        self.recommendation_config = (
            recommendation_config or get_config().recommendations
        )
        self.logger = logger.bind(component="health_assessment")

        self._model_loaded = False
        self._accuracy_history: List[float] = []
        self._performance_metrics: List[Dict[str, Any]] = []

        # Configuration-driven behavior (no hard-coded values)
        self._scoring_weights = self.config.scoring_weights
        self._status_thresholds = self.config.status_thresholds
        self._risk_weights = self.config.risk_weights
        self._recommendation_templates = self.recommendation_config.templates

    def predict(self, initiative_data: Dict[str, Any]) -> HealthPredictionResult:
        """
        Perform health prediction with SOLID principles

        Single Responsibility: Only handles inference, delegates other concerns
        """
        if not self.is_model_loaded():
            raise ModelNotLoadedError("Health assessment model not loaded")

        start_time = time.time()

        try:
            # Input validation and normalization
            normalized_data = self._validate_and_normalize_input(initiative_data)
            if not normalized_data:
                return self._create_error_result("Invalid input data format")

            # Core health assessment pipeline
            health_components = self._calculate_health_components(normalized_data)
            overall_health_score = self._calculate_overall_health_score(
                health_components
            )
            risk_assessment = self._assess_risks(normalized_data)
            trend_analysis = self._analyze_trends(normalized_data)
            recommendations = self._generate_recommendations(
                health_components, risk_assessment, normalized_data
            )

            # Classify results using configuration thresholds
            health_status = self._determine_health_status(overall_health_score)
            risk_level = self._determine_risk_level(risk_assessment, trend_analysis)

            # Calculate prediction confidence
            prediction_confidence = self._calculate_prediction_confidence(
                health_components, risk_assessment, normalized_data
            )

            processing_time_ms = int((time.time() - start_time) * 1000)

            # Record performance metrics (delegation to monitoring interface)
            self.record_query_performance(
                str(normalized_data.get("id", "unknown")),
                processing_time_ms,
                1,
                prediction_confidence,
            )

            return HealthPredictionResult(
                success=True,
                health_score=round(overall_health_score, 3),
                health_status=health_status,
                risk_level=risk_level,
                confidence=round(prediction_confidence, 3),
                processing_time_ms=processing_time_ms,
                health_components=health_components,
                risk_assessment=risk_assessment,
                trend_analysis=trend_analysis,
                recommendations=recommendations,
            )

        except Exception as e:
            self.logger.error("Health prediction failed", error=str(e))
            return self._create_error_result(f"Prediction failed: {str(e)}")

    def load_model(self) -> bool:
        """Load health prediction model with configuration-driven behavior"""
        try:
            start_time = time.time()

            self.logger.info(
                "Loading health assessment model",
                model_name=self.config.model_name,
                accuracy_threshold=self.config.accuracy_threshold,
            )

            # Configuration-driven model loading
            test_mode = getattr(self.config, "test_mode", False)
            if not test_mode:
                time.sleep(0.1)  # Simulate realistic loading

            # Validate configuration
            if self.config.accuracy_threshold < 0.80:
                self.logger.warning(
                    "Health prediction accuracy threshold below recommended 80%",
                    threshold=self.config.accuracy_threshold,
                )

            self._model_loaded = True
            load_time = (time.time() - start_time) * 1000

            self.logger.info(
                "Health assessment model loaded successfully", load_time_ms=load_time
            )

            return True

        except Exception as e:
            self.logger.error("Failed to load health assessment model", error=str(e))
            return False

    def is_model_loaded(self) -> bool:
        """Check if model is ready for inference"""
        return self._model_loaded

    def validate_accuracy(
        self, test_data: List[Tuple[Dict[str, Any], Dict[str, Any]]]
    ) -> ValidationResult:
        """
        Validate model accuracy (Interface Segregation - separate concern)
        """
        if not test_data:
            return ValidationResult(
                accuracy=0.0, test_cases=0, passed=False, details={}
            )

        correct_predictions = 0
        accuracy_scores = []

        for initiative_data, expected_outcome in test_data:
            try:
                result = self.predict(initiative_data)

                if result.success:
                    predicted_status = result.health_status
                    expected_status = expected_outcome.get("expected_health_status")

                    # Exact match scoring
                    if predicted_status == expected_status:
                        correct_predictions += 1
                        accuracy_scores.append(1.0)
                    else:
                        # Partial scoring for adjacent categories
                        partial_score = self._calculate_partial_accuracy(
                            predicted_status, expected_status
                        )
                        accuracy_scores.append(partial_score)
                        if partial_score > 0.7:  # Consider "close enough" as correct
                            correct_predictions += 1

            except Exception as e:
                self.logger.error("Validation error", error=str(e))
                accuracy_scores.append(0.0)

        accuracy = (
            sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0.0
        )
        self._accuracy_history.append(accuracy)

        passed = accuracy >= self.config.accuracy_threshold

        details = {
            "correct_predictions": correct_predictions,
            "total_predictions": len(test_data),
            "accuracy_scores": accuracy_scores[:5],  # Sample for debugging
            "threshold": self.config.accuracy_threshold,
        }

        self.logger.info(
            "Health assessment accuracy validation completed",
            accuracy=accuracy,
            passed=passed,
            test_cases=len(test_data),
        )

        return ValidationResult(
            accuracy=accuracy, test_cases=len(test_data), passed=passed, details=details
        )

    def get_accuracy_history(self) -> List[float]:
        """Get historical accuracy measurements"""
        return self._accuracy_history.copy()

    def record_query_performance(
        self, query: str, execution_time_ms: int, result_count: int, confidence: float
    ) -> None:
        """Record performance metrics (Interface Segregation - separate concern)"""
        metric = {
            "timestamp": datetime.now().isoformat(),
            "query_hash": hash(query) % 10000,
            "execution_time_ms": execution_time_ms,
            "result_count": result_count,
            "confidence": confidence,
            "meets_time_sla": execution_time_ms < self.config.max_inference_time_ms,
            "meets_accuracy_sla": confidence >= self.config.accuracy_threshold,
        }

        self._performance_metrics.append(metric)

        # Alert on SLA violations
        if (
            execution_time_ms > self.config.max_inference_time_ms
            or confidence < self.config.accuracy_threshold
        ):
            self.logger.warning(
                "Health assessment SLA violation",
                execution_time_ms=execution_time_ms,
                confidence=confidence,
                time_threshold=self.config.max_inference_time_ms,
                accuracy_threshold=self.config.accuracy_threshold,
            )

    def get_performance_metrics(self) -> List[PerformanceMetric]:
        """Get collected performance metrics"""
        return self._performance_metrics.copy()

    def check_sla_compliance(self, thresholds: PerformanceThresholds) -> bool:
        """Check if recent performance meets SLA thresholds"""
        if not self._performance_metrics:
            return True

        recent_metrics = self._performance_metrics[-10:]  # Last 10 queries
        violations = sum(
            1
            for m in recent_metrics
            if not m["meets_time_sla"] or not m["meets_accuracy_sla"]
        )

        violation_rate = violations / len(recent_metrics)
        return violation_rate <= thresholds.max_error_rate

    def configure(self, config: Dict[str, Any]) -> None:
        """Apply configuration updates (Dependency Inversion Principle)"""
        for key, value in config.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        # Refresh configuration-driven components
        self._scoring_weights = self.config.scoring_weights
        self._status_thresholds = self.config.status_thresholds
        self._risk_weights = self.config.risk_weights

        self.logger.info(
            "Health assessment configuration updated", updates=list(config.keys())
        )

    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.dict()

    # Private methods implementing core business logic

    def _validate_and_normalize_input(
        self, input_data: Any
    ) -> Optional[Dict[str, Any]]:
        """Validate and normalize input data format"""
        if not isinstance(input_data, dict):
            return None

        # Configuration-driven field defaults
        default_values = {
            "id": "unknown",
            "current_progress": 0.0,
            "stakeholder_engagement_score": 0.5,
            "milestone_completion_rate": 0.0,
            "budget_utilization": 0.0,
            "risk_indicators": [],
        }

        normalized_data = {}

        # Normalize required fields
        for field, default_value in default_values.items():
            value = input_data.get(field, default_value)

            # Normalize numeric values to 0-1 range
            if field in [
                "current_progress",
                "stakeholder_engagement_score",
                "milestone_completion_rate",
                "budget_utilization",
            ]:
                normalized_data[field] = max(0.0, min(1.0, float(value or 0)))
            else:
                normalized_data[field] = value

        # Preserve optional fields
        optional_fields = [
            "start_date",
            "target_end_date",
            "team_satisfaction",
            "quality_metrics",
            "external_dependencies",
        ]

        for field in optional_fields:
            if field in input_data:
                normalized_data[field] = input_data[field]

        return normalized_data

    def _calculate_health_components(
        self, initiative_data: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate individual health component scores using configuration weights"""
        components = {}

        # Progress completion score
        components["progress_score"] = initiative_data.get("current_progress", 0)

        # Stakeholder engagement score
        components["stakeholder_score"] = initiative_data.get(
            "stakeholder_engagement_score", 0.5
        )

        # Milestone completion score
        components["milestone_score"] = initiative_data.get(
            "milestone_completion_rate", 0
        )

        # Budget health score (configuration-driven optimal range)
        budget_util = initiative_data.get("budget_utilization", 0)
        optimal_min, optimal_max = self.config.optimal_budget_range

        if budget_util <= optimal_max:
            budget_score = budget_util / optimal_max  # Linear up to optimal max
        else:
            # Penalty after optimal range
            budget_score = max(0, 1.0 - (budget_util - optimal_max) * 2)
        components["budget_score"] = budget_score

        # Timeline adherence
        components["timeline_score"] = self._calculate_timeline_score(initiative_data)

        # Risk indicator score (inverted)
        risk_score = self._calculate_risk_score(initiative_data)
        components["risk_score"] = 1.0 - risk_score

        return components

    def _calculate_overall_health_score(self, components: Dict[str, float]) -> float:
        """Calculate weighted overall health score using configuration"""
        total_score = 0.0

        # Use configuration weights for scoring
        weight_mapping = {
            "progress_completion": "progress_score",
            "stakeholder_engagement": "stakeholder_score",
            "milestone_completion": "milestone_score",
            "budget_health": "budget_score",
            "timeline_adherence": "timeline_score",
            "risk_indicators": "risk_score",
        }

        for weight_key, score_key in weight_mapping.items():
            weight = getattr(self._scoring_weights, weight_key)
            component_score = components.get(score_key, 0.5)
            total_score += component_score * weight

        return max(0.0, min(1.0, total_score))

    def _assess_risks(self, initiative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform risk assessment using configuration-driven weights"""
        risk_indicators = initiative_data.get("risk_indicators", [])
        overall_risk_score = self._calculate_risk_score(initiative_data)

        # Categorize risks using configuration weights
        categorized_risks = {"high_impact": [], "medium_impact": [], "low_impact": []}

        for risk in risk_indicators:
            category = self._risk_weights.get_risk_category(risk)
            categorized_risks[category].append(risk)

        # Risk trend analysis (simplified)
        risk_trend = "increasing" if len(risk_indicators) >= 4 else "stable"

        return {
            "overall_risk_score": overall_risk_score,
            "risk_indicators": risk_indicators,
            "categorized_risks": categorized_risks,
            "risk_trend": risk_trend,
            "critical_risks": categorized_risks["high_impact"],
        }

    def _calculate_risk_score(self, initiative_data: Dict[str, Any]) -> float:
        """Calculate risk score using configuration-driven weights"""
        risk_indicators = initiative_data.get("risk_indicators", [])

        if not risk_indicators:
            return 0.1  # Minimal risk when no indicators

        total_risk = 0.0
        for risk in risk_indicators:
            weight = self._risk_weights.get_weight(risk)
            total_risk += weight

        return min(1.0, total_risk)

    def _analyze_trends(self, initiative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends and momentum indicators"""
        progress = initiative_data.get("current_progress", 0)
        engagement = initiative_data.get("stakeholder_engagement_score", 0.5)
        milestone_rate = initiative_data.get("milestone_completion_rate", 0)

        # Momentum calculation
        momentum_score = (progress + engagement + milestone_rate) / 3

        # Configuration-driven momentum classification
        if momentum_score >= 0.8:
            momentum = "accelerating"
        elif momentum_score >= 0.6:
            momentum = "steady"
        elif momentum_score >= 0.4:
            momentum = "slowing"
        else:
            momentum = "stalled"

        return {
            "momentum": momentum,
            "momentum_score": momentum_score,
            "trend_indicators": {
                "progress_trend": "stable",
                "engagement_trend": "stable",
                "risk_trend": "stable",
            },
        }

    def _generate_recommendations(
        self,
        health_components: Dict[str, float],
        risk_assessment: Dict[str, Any],
        initiative_data: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Generate recommendations using configuration templates"""
        recommendations = []

        # Identify weak health components
        weak_components = [
            (component, score)
            for component, score in health_components.items()
            if score < 0.6
        ]

        # Sort by severity
        weak_components.sort(key=lambda x: x[1])

        # Generate recommendations for weak areas using configuration templates
        component_template_mapping = {
            "stakeholder_score": "stakeholder_engagement",
            "timeline_score": "timeline_management",
            "budget_score": "budget_management",
            "risk_score": "risk_mitigation",
        }

        for component, score in weak_components[:3]:  # Top 3 issues
            template_key = component_template_mapping.get(component)
            if template_key and template_key in self._recommendation_templates:
                priority = (
                    PriorityLevel.HIGH.value
                    if score < 0.4
                    else PriorityLevel.MEDIUM.value
                )
                recommendations.extend(
                    self._create_recommendations(template_key, priority, score)
                )

        # Add critical risk recommendations
        critical_risks = risk_assessment.get("critical_risks", [])
        for risk in critical_risks:
            recommendations.append(
                {
                    "type": "risk_mitigation",
                    "priority": PriorityLevel.URGENT.value,
                    "description": f"Address critical risk: {risk.replace('_', ' ').title()}",
                    "action_items": [
                        f"Develop mitigation plan for {risk}",
                        f"Monitor {risk} indicators daily",
                        f"Establish contingency for {risk}",
                    ],
                }
            )

        # Limit to configuration maximum
        return recommendations[: self.recommendation_config.max_recommendations]

    def _create_recommendations(
        self, category: str, priority: str, score: float
    ) -> List[Dict[str, Any]]:
        """Create recommendations using configuration templates"""
        template = self._recommendation_templates.get(category, {})
        descriptions = template.get("descriptions", [])
        action_items = template.get("action_items", [])

        if not descriptions:
            return []

        # Select template based on severity
        template_index = min(
            len(descriptions) - 1, int((1 - score) * len(descriptions))
        )
        description = descriptions[template_index]

        return [
            {
                "type": category,
                "priority": priority,
                "description": description,
                "score_impact": score,
                "action_items": action_items[:3],  # Limit action items
            }
        ]

    def _determine_health_status(self, health_score: float) -> str:
        """Determine health status using configuration thresholds"""
        thresholds = [
            (self._status_thresholds.excellent, HealthStatus.EXCELLENT.value),
            (self._status_thresholds.healthy, HealthStatus.HEALTHY.value),
            (self._status_thresholds.at_risk, HealthStatus.AT_RISK.value),
            (self._status_thresholds.failing, HealthStatus.FAILING.value),
        ]

        for threshold, status in thresholds:
            if health_score >= threshold:
                return status

        return HealthStatus.FAILING.value

    def _determine_risk_level(
        self, risk_assessment: Dict[str, Any], trend_analysis: Dict[str, Any]
    ) -> str:
        """Determine overall risk level"""
        risk_score = risk_assessment.get("overall_risk_score", 0)
        momentum = trend_analysis.get("momentum", "steady")

        # Adjust risk based on momentum
        if momentum == "stalled":
            risk_score += 0.2
        elif momentum == "accelerating":
            risk_score -= 0.1

        # Configuration-driven risk level thresholds
        if risk_score >= 0.7:
            return RiskLevel.HIGH.value
        elif risk_score >= 0.4:
            return RiskLevel.MEDIUM.value
        else:
            return RiskLevel.LOW.value

    def _calculate_prediction_confidence(
        self,
        health_components: Dict[str, float],
        risk_assessment: Dict[str, Any],
        initiative_data: Dict[str, Any],
    ) -> float:
        """Calculate confidence using configuration parameters"""
        base_confidence = self.config.base_confidence

        # Configuration-driven confidence calculation
        required_fields = [
            "current_progress",
            "stakeholder_engagement_score",
            "milestone_completion_rate",
            "budget_utilization",
        ]

        missing_fields = sum(
            1 for field in required_fields if initiative_data.get(field) is None
        )

        confidence_penalty = missing_fields * self.config.missing_field_penalty

        # Extreme value penalty
        extreme_penalty = 0
        for component, score in health_components.items():
            if score == 0.0 or score == 1.0:
                extreme_penalty += self.config.extreme_value_penalty

        final_confidence = max(
            0.5, base_confidence - confidence_penalty - extreme_penalty
        )
        return final_confidence

    def _calculate_timeline_score(self, initiative_data: Dict[str, Any]) -> float:
        """Calculate timeline adherence score"""
        try:
            start_date = initiative_data.get("start_date")
            target_end_date = initiative_data.get("target_end_date")
            current_progress = initiative_data.get("current_progress", 0)

            if not start_date or not target_end_date:
                return 0.7  # Default score when timeline data unavailable

            # Simple date parsing
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            if isinstance(target_end_date, str):
                target_end_date = datetime.fromisoformat(
                    target_end_date.replace("Z", "+00:00")
                )

            now = datetime.now()
            total_duration = (target_end_date - start_date).days
            elapsed_duration = (now - start_date).days

            if total_duration <= 0:
                return 0.7

            expected_progress = elapsed_duration / total_duration
            progress_variance = current_progress - expected_progress

            # Score based on timeline adherence
            if progress_variance >= 0:
                return min(1.0, 0.8 + progress_variance * 0.5)
            else:
                return max(0.0, 0.8 + progress_variance)

        except Exception:
            return 0.7  # Default score on error

    def _calculate_partial_accuracy(self, predicted: str, expected: str) -> float:
        """Calculate partial accuracy for adjacent health status categories"""
        status_order = [
            HealthStatus.FAILING.value,
            HealthStatus.AT_RISK.value,
            HealthStatus.HEALTHY.value,
            HealthStatus.EXCELLENT.value,
        ]

        try:
            pred_idx = status_order.index(predicted)
            exp_idx = status_order.index(expected)

            distance = abs(pred_idx - exp_idx)

            if distance == 0:
                return 1.0
            elif distance == 1:
                return 0.7  # Adjacent categories
            elif distance == 2:
                return 0.3  # Two categories away
            else:
                return 0.0  # Completely wrong

        except ValueError:
            return 0.0

    def _create_error_result(self, error_message: str) -> HealthPredictionResult:
        """Create standardized error result"""
        return HealthPredictionResult(
            success=False,
            health_score=0.0,
            health_status=HealthStatus.UNKNOWN.value,
            risk_level=RiskLevel.HIGH.value,
            confidence=0.0,
            processing_time_ms=0,
            health_components={},
            risk_assessment={},
            trend_analysis={},
            recommendations=[],
            error=error_message,
        )
