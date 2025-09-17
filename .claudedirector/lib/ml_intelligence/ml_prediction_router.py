"""
Phase 13: ML Prediction Router - TECHNICAL STORY TS-13.1.1

Routes strategic queries to appropriate ML prediction models while maintaining
seamless integration with existing MCP architecture and transparency standards.

Author: Martin | Platform Architecture + Berny | AI/ML Engineering
Integration: Decision Orchestrator, MCP Coordinator, Transparency Engine
Foundation: Leverages Phase 12 always-on MCP enhancement patterns
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import structlog

# TS-4: Import unified response handler (eliminates duplicate MLPredictionResponse pattern)
from ..performance import (
    create_ml_response,
    UnifiedResponse,
    ResponseStatus,
)

# Graceful imports for ML dependencies
try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

    # Mock numpy for basic operations
    class MockNumpy:
        @staticmethod
        def random():
            import random

            return random.random()

        @staticmethod
        def array(data):
            return data

    np = MockNumpy()

logger = structlog.get_logger(__name__)


class MLModelType(Enum):
    """Types of ML models available for prediction"""

    COLLABORATION_SUCCESS = "collaboration_success"
    TIMELINE_FORECASTING = "timeline_forecasting"
    RISK_ASSESSMENT = "risk_assessment"
    SUCCESS_FACTORS = "success_factors"


@dataclass
class MLPredictionRequest:
    """Request for ML prediction"""

    model_type: MLModelType
    features: Dict[str, Any]
    context: str
    persona: str
    timeout_ms: int = 5000  # 5 second timeout per TS-13.1.1


# TS-4: MLPredictionResponse class ELIMINATED - replaced with UnifiedResponse
# This eliminates 25+ lines of duplicate response handling logic
# All MLPredictionResponse functionality now handled by create_ml_response() from unified_response_handler


class MLPredictionRouter:
    """
    🤖 PHASE 13: ML Prediction Router

    Routes strategic queries to appropriate ML models for predictive intelligence.
    Integrates with existing Decision Orchestrator while maintaining <5s latency.

    TECHNICAL STORY: TS-13.1.1 - ML Pipeline Integration with Decision Orchestrator

    Key Requirements:
    - <5s ML prediction latency for complex queries
    - <50ms transparency overhead (Phase 12 standard maintained)
    - Graceful fallback to Phase 12 when ML unavailable
    - Complete transparency disclosure for audit compliance
    """

    def __init__(self, enable_numpy: bool = True):
        """
        Initialize ML Prediction Router

        Args:
            enable_numpy: Use numpy for ML operations (graceful fallback if unavailable)
        """
        self.models_loaded = False
        self.model_cache = {}
        self.performance_metrics = {
            "predictions_served": 0,
            "avg_latency_ms": 0,
            "cache_hit_rate": 0.0,
            "fallback_rate": 0.0,
        }

        # Check ML dependencies
        self.ml_available = HAS_NUMPY and enable_numpy
        if not self.ml_available:
            logger.warning(
                "ml_dependencies_unavailable", fallback="lightweight_prediction_stubs"
            )

        # Initialize prediction models (lightweight stubs for Phase 13.1)
        self._initialize_prediction_models()

        logger.info(
            "ml_prediction_router_initialized",
            ml_available=self.ml_available,
            models_loaded=self.models_loaded,
        )

    def _initialize_prediction_models(self):
        """Initialize ML prediction models (Phase 13.1: Lightweight stubs)"""
        try:
            # Phase 13.1: Initialize with lightweight prediction stubs
            # These will be replaced with actual trained models in Phase 13.2
            self.model_cache = {
                MLModelType.COLLABORATION_SUCCESS: self._create_collaboration_stub(),
                MLModelType.TIMELINE_FORECASTING: self._create_timeline_stub(),
                MLModelType.RISK_ASSESSMENT: self._create_risk_stub(),
                MLModelType.SUCCESS_FACTORS: self._create_success_factors_stub(),
            }
            self.models_loaded = True
            logger.info(
                "ml_prediction_models_initialized",
                model_count=len(self.model_cache),
                type="lightweight_stubs",
            )
        except Exception as e:
            logger.error("ml_model_initialization_failed", error=str(e))
            self.models_loaded = False

    async def predict_collaboration_success(
        self, features: Dict[str, Any], context: str, persona: str
    ) -> Dict[str, Any]:
        """
        Predict collaboration success probability for strategic initiatives

        Returns: {
            "success_probability": float,  # 0.0 to 1.0
            "risk_factors": List[str],
            "success_factors": List[str],
            "confidence": float
        }
        """
        start_time = time.time()

        try:
            request = MLPredictionRequest(
                model_type=MLModelType.COLLABORATION_SUCCESS,
                features=features,
                context=context,
                persona=persona,
            )

            response = await self._route_prediction(request)

            if response.success:
                return response.prediction
            else:
                # Fallback to heuristic-based prediction
                return self._fallback_collaboration_prediction(features, context)

        except Exception as e:
            logger.warning(
                "collaboration_prediction_failed",
                error=str(e),
                fallback="heuristic_prediction",
            )
            return self._fallback_collaboration_prediction(features, context)
        finally:
            latency_ms = int((time.time() - start_time) * 1000)
            self._update_metrics(latency_ms, MLModelType.COLLABORATION_SUCCESS)

    async def predict_timeline_forecast(
        self, features: Dict[str, Any], context: str, horizon_weeks: int = 4
    ) -> Dict[str, Any]:
        """
        Predict timeline forecast for multi-week planning

        Returns: {
            "weekly_probabilities": Dict[str, float],  # {"week_1": 0.95, "week_2": 0.87, ...}
            "risk_weeks": List[str],
            "confidence": float
        }
        """
        start_time = time.time()

        try:
            request = MLPredictionRequest(
                model_type=MLModelType.TIMELINE_FORECASTING,
                features={**features, "horizon_weeks": horizon_weeks},
                context=context,
                persona=features.get("persona", "diego"),
            )

            response = await self._route_prediction(request)

            if response.success:
                return response.prediction
            else:
                return self._fallback_timeline_prediction(features, horizon_weeks)

        except Exception as e:
            logger.warning(
                "timeline_prediction_failed",
                error=str(e),
                fallback="heuristic_forecast",
            )
            return self._fallback_timeline_prediction(features, horizon_weeks)
        finally:
            latency_ms = int((time.time() - start_time) * 1000)
            self._update_metrics(latency_ms, MLModelType.TIMELINE_FORECASTING)

    async def _route_prediction(self, request: MLPredictionRequest) -> UnifiedResponse:
        """Route prediction request to appropriate model"""
        start_time = time.time()

        if not self.models_loaded:
            return await create_ml_response(
                content="ML models not loaded",
                status=ResponseStatus.ERROR,
                success=False,
                error="ML models not loaded",
                metadata={"fallback_used": True},
            )

        model = self.model_cache.get(request.model_type)
        if not model:
            return await create_ml_response(
                content=f"Model {request.model_type.value} not available",
                status=ResponseStatus.ERROR,
                success=False,
                error=f"Model {request.model_type.value} not available",
                metadata={"fallback_used": True},
            )

        try:
            # Phase 13.1: Use lightweight prediction stubs
            prediction = await model(request.features, request.context)

            processing_time_ms = int((time.time() - start_time) * 1000)

            return await create_ml_response(
                content=str(prediction),
                status=ResponseStatus.SUCCESS,
                success=True,
                confidence=0.85,  # Phase 13.1: Fixed confidence for stubs
                metadata={
                    "prediction": prediction,
                    "processing_time_ms": processing_time_ms,
                },
            )

        except Exception as e:
            processing_time_ms = int((time.time() - start_time) * 1000)
            return await create_ml_response(
                content=str(e),
                status=ResponseStatus.ERROR,
                success=False,
                error=str(e),
                metadata={
                    "processing_time_ms": processing_time_ms,
                    "fallback_used": True,
                },
            )

    def _create_collaboration_stub(self):
        """Create collaboration success prediction stub for Phase 13.1"""

        async def predict(features: Dict[str, Any], context: str) -> Dict[str, Any]:
            # Phase 13.1: Heuristic-based prediction using feature analysis
            base_probability = 0.75

            # Adjust based on features
            if features.get("stakeholder_count", 0) > 3:
                base_probability -= 0.1  # More stakeholders = higher complexity

            if features.get("time_sensitivity") == "immediate":
                base_probability -= 0.15  # Urgency reduces success probability
            elif features.get("time_sensitivity") == "long_term":
                base_probability += 0.1  # Long-term planning improves success

            if features.get("business_impact") == "critical":
                base_probability += 0.05  # High stakes improve focus

            # Add some realistic variance
            variance = (np.random() - 0.5) * 0.2  # ±10% variance
            final_probability = max(0.1, min(0.95, base_probability + variance))

            # Generate risk and success factors based on features
            risk_factors = []
            success_factors = []

            if features.get("stakeholder_count", 0) > 3:
                risk_factors.append("High stakeholder count may complicate alignment")
            if features.get("time_sensitivity") == "immediate":
                risk_factors.append(
                    "Immediate timeline pressure may reduce planning quality"
                )

            if features.get("has_technical_terms"):
                success_factors.append(
                    "Technical expertise available for implementation"
                )
            if features.get("persona") in ["diego", "martin"]:
                success_factors.append(
                    "Engineering leadership expertise aligns with initiative"
                )

            return {
                "success_probability": final_probability,
                "risk_factors": risk_factors,
                "success_factors": success_factors,
                "confidence": 0.85,
            }

        return predict

    def _create_timeline_stub(self):
        """Create timeline forecasting stub for Phase 13.1"""

        async def predict(features: Dict[str, Any], context: str) -> Dict[str, Any]:
            horizon_weeks = features.get("horizon_weeks", 4)
            base_probability = 0.9

            # Model degradation over time with complexity factors
            complexity_factor = (
                0.05 if features.get("complexity") == "strategic" else 0.03
            )

            weekly_probabilities = {}
            risk_weeks = []

            for week in range(1, horizon_weeks + 1):
                # Exponential decay with complexity
                week_probability = base_probability * (
                    0.95 ** ((week - 1) * (1 + complexity_factor))
                )

                # Add variance
                variance = (np.random() - 0.5) * 0.1
                week_probability = max(0.3, min(0.98, week_probability + variance))

                weekly_probabilities[f"week_{week}"] = week_probability

                if week_probability < 0.8:
                    risk_weeks.append(f"week_{week}")

            return {
                "weekly_probabilities": weekly_probabilities,
                "risk_weeks": risk_weeks,
                "confidence": 0.80,
            }

        return predict

    def _create_risk_stub(self):
        """Create risk assessment stub for Phase 13.1"""

        async def predict(features: Dict[str, Any], context: str) -> Dict[str, Any]:
            # Simple risk scoring based on features
            risk_score = 0.3  # Base risk

            if features.get("stakeholder_count", 0) > 3:
                risk_score += 0.2
            if features.get("complexity") == "strategic":
                risk_score += 0.15
            if features.get("time_sensitivity") == "immediate":
                risk_score += 0.25

            risk_score = min(0.9, risk_score)

            return {
                "risk_score": risk_score,
                "risk_level": (
                    "high"
                    if risk_score > 0.7
                    else "medium" if risk_score > 0.4 else "low"
                ),
                "confidence": 0.75,
            }

        return predict

    def _create_success_factors_stub(self):
        """Create success factors identification stub for Phase 13.1"""

        async def predict(features: Dict[str, Any], context: str) -> Dict[str, Any]:
            success_factors = []

            if features.get("has_technical_terms"):
                success_factors.append("Technical implementation capability")
            if features.get("business_impact") in ["high", "critical"]:
                success_factors.append(
                    "High business priority ensures resource allocation"
                )
            if features.get("persona") in ["diego", "camille"]:
                success_factors.append("Senior leadership involvement")

            return {
                "success_factors": success_factors,
                "factor_count": len(success_factors),
                "confidence": 0.80,
            }

        return predict

    def _fallback_collaboration_prediction(
        self, features: Dict[str, Any], context: str
    ) -> Dict[str, Any]:
        """Fallback heuristic collaboration prediction when ML unavailable"""
        # Simple heuristic based on common patterns
        base_probability = 0.7

        if "collaboration" in context.lower():
            base_probability += 0.1
        if "team" in context.lower():
            base_probability += 0.05

        return {
            "success_probability": base_probability,
            "risk_factors": ["ML prediction unavailable - using heuristic fallback"],
            "success_factors": ["Historical collaboration patterns applied"],
            "confidence": 0.6,  # Lower confidence for fallback
            "fallback_mode": True,
        }

    def _fallback_timeline_prediction(
        self, features: Dict[str, Any], horizon_weeks: int
    ) -> Dict[str, Any]:
        """Fallback heuristic timeline prediction when ML unavailable"""
        # Conservative linear degradation
        weekly_probabilities = {}
        for week in range(1, horizon_weeks + 1):
            probability = max(0.5, 0.95 - (week - 1) * 0.1)
            weekly_probabilities[f"week_{week}"] = probability

        return {
            "weekly_probabilities": weekly_probabilities,
            "risk_weeks": [f"week_{week}" for week in range(3, horizon_weeks + 1)],
            "confidence": 0.5,  # Lower confidence for fallback
            "fallback_mode": True,
        }

    def _update_metrics(self, latency_ms: int, model_type: MLModelType):
        """Update performance metrics for monitoring"""
        self.performance_metrics["predictions_served"] += 1

        # Update average latency
        current_avg = self.performance_metrics["avg_latency_ms"]
        count = self.performance_metrics["predictions_served"]
        new_avg = ((current_avg * (count - 1)) + latency_ms) / count
        self.performance_metrics["avg_latency_ms"] = new_avg

        # Track if this was a fallback
        if not self.ml_available:
            fallback_count = self.performance_metrics.get("fallback_count", 0) + 1
            self.performance_metrics["fallback_count"] = fallback_count
            self.performance_metrics["fallback_rate"] = fallback_count / count

    def get_health_status(self) -> Dict[str, Any]:
        """Get ML prediction router health status"""
        return {
            "status": "healthy" if self.models_loaded else "degraded",
            "ml_available": self.ml_available,
            "models_loaded": self.models_loaded,
            "performance_metrics": self.performance_metrics,
            "supported_models": [model.value for model in MLModelType],
        }

    async def health_check(self) -> bool:
        """Perform health check for circuit breaker pattern"""
        try:
            # Quick health check with minimal features
            test_features = {"test": True}
            result = await self.predict_collaboration_success(
                features=test_features, context="health check", persona="diego"
            )
            return result is not None
        except Exception as e:
            logger.warning("ml_health_check_failed", error=str(e))
            return False


# Factory function for integration with Decision Orchestrator
def create_ml_prediction_router(enable_ml: bool = True) -> Optional[MLPredictionRouter]:
    """
    Create ML Prediction Router with graceful fallback

    Args:
        enable_ml: Enable ML predictions (graceful fallback if disabled)

    Returns:
        MLPredictionRouter instance or None if completely unavailable
    """
    try:
        router = MLPredictionRouter(enable_numpy=enable_ml)
        logger.info(
            "ml_prediction_router_created",
            ml_available=router.ml_available,
            models_loaded=router.models_loaded,
        )
        return router
    except Exception as e:
        logger.error("ml_prediction_router_creation_failed", error=str(e))
        return None
