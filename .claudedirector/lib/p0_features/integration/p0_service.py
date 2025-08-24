"""
P0 Strategic Intelligence Service

Martin's unified service orchestrating all P0 domains.
Provides high-level API while maintaining SOLID principles and domain separation.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import structlog

from ..shared.ai_core.interfaces import (
    IDecisionIntelligenceEngine,
    IHealthPredictionEngine,
)
from ..shared.infrastructure.config import get_config, P0FeatureConfig
from .model_factory import get_model_factory, ModelFactory

logger = structlog.get_logger(__name__)


@dataclass
class StrategicIntelligenceRequest:
    """Request for strategic intelligence analysis"""

    content: str
    content_type: str  # 'meeting_notes', 'document', 'report'
    context: Optional[Dict[str, Any]] = None
    request_id: Optional[str] = None


@dataclass
class InitiativeHealthRequest:
    """Request for initiative health assessment"""

    initiative_data: Dict[str, Any]
    request_id: Optional[str] = None


@dataclass
class P0AnalysisResult:
    """Unified result from P0 analysis"""

    request_id: str
    timestamp: str
    success: bool

    # Decision intelligence results
    decisions_detected: int
    decisions: List[Dict[str, Any]]
    decision_confidence: float

    # Health assessment results (if applicable)
    health_score: Optional[float]
    health_status: Optional[str]
    risk_level: Optional[str]
    health_confidence: Optional[float]
    health_components: Optional[Dict[str, Any]]
    risk_assessment: Optional[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]

    # Processing metadata
    processing_time_ms: int
    model_versions: Dict[str, str]
    error: Optional[str] = None


class P0StrategicIntelligenceService:
    """
    Unified service for P0 strategic intelligence

    Single Responsibility: Orchestrates P0 domains without implementing AI logic
    Open/Closed: Extensible with new domains via factory pattern
    Liskov Substitution: Consistent service interface regardless of implementation
    Interface Segregation: Clients use only needed service methods
    Dependency Inversion: Depends on abstractions, not concrete implementations
    """

    def __init__(
        self,
        config: Optional[P0FeatureConfig] = None,
        model_factory: Optional[ModelFactory] = None,
    ):
        """
        Initialize service with dependency injection
        """
        self.config = config or get_config()
        self.model_factory = model_factory or get_model_factory()
        self.logger = logger.bind(component="p0_service")

        # Lazy-loaded AI engines (performance optimization)
        self._decision_engine: Optional[IDecisionIntelligenceEngine] = None
        self._health_engine: Optional[IHealthPredictionEngine] = None

        self.logger.info(
            "P0 Strategic Intelligence Service initialized",
            decision_enabled=self.config.enable_decision_intelligence,
            health_enabled=self.config.enable_health_prediction,
        )

    async def analyze_strategic_content(
        self, request: StrategicIntelligenceRequest
    ) -> P0AnalysisResult:
        """
        Analyze strategic content for decision intelligence

        Args:
            request: Strategic intelligence analysis request

        Returns:
            P0AnalysisResult: Unified analysis results
        """
        start_time = datetime.now()
        request_id = request.request_id or f"req_{int(start_time.timestamp() * 1000)}"

        try:
            self.logger.info(
                "Starting strategic content analysis",
                request_id=request_id,
                content_type=request.content_type,
                content_length=len(request.content),
            )

            # Get decision intelligence engine
            decision_engine = await self._get_decision_engine()

            # Perform decision analysis
            decision_result = decision_engine.predict(request.content)

            # Calculate processing time
            processing_time_ms = int(
                (datetime.now() - start_time).total_seconds() * 1000
            )

            # Create unified result
            result = P0AnalysisResult(
                request_id=request_id,
                timestamp=start_time.isoformat(),
                success=decision_result.success,
                decisions_detected=decision_result.decisions_detected,
                decisions=decision_result.decisions,
                decision_confidence=decision_result.overall_confidence,
                health_score=None,
                health_status=None,
                risk_level=None,
                health_confidence=None,
                health_components=None,
                risk_assessment=None,
                recommendations=[],
                processing_time_ms=processing_time_ms,
                model_versions={
                    "decision_intelligence": decision_engine.get_configuration().get(
                        "model_name", "unknown"
                    )
                },
                error=decision_result.error,
            )

            self.logger.info(
                "Strategic content analysis completed",
                request_id=request_id,
                decisions_detected=result.decisions_detected,
                confidence=result.decision_confidence,
                processing_time_ms=processing_time_ms,
            )

            return result

        except Exception as e:
            processing_time_ms = int(
                (datetime.now() - start_time).total_seconds() * 1000
            )
            self.logger.error(
                "Strategic content analysis failed", request_id=request_id, error=str(e)
            )

            return P0AnalysisResult(
                request_id=request_id,
                timestamp=start_time.isoformat(),
                success=False,
                decisions_detected=0,
                decisions=[],
                decision_confidence=0.0,
                health_score=None,
                health_status=None,
                risk_level=None,
                health_confidence=None,
                health_components=None,
                risk_assessment=None,
                recommendations=[],
                processing_time_ms=processing_time_ms,
                model_versions={},
                error=str(e),
            )

    async def assess_initiative_health(
        self, request: InitiativeHealthRequest
    ) -> P0AnalysisResult:
        """
        Assess initiative health and generate recommendations

        Args:
            request: Initiative health assessment request

        Returns:
            P0AnalysisResult: Unified analysis results
        """
        start_time = datetime.now()
        request_id = request.request_id or f"req_{int(start_time.timestamp() * 1000)}"

        try:
            self.logger.info(
                "Starting initiative health assessment",
                request_id=request_id,
                initiative_id=request.initiative_data.get("id", "unknown"),
            )

            # Get health assessment engine
            health_engine = await self._get_health_engine()

            # Perform health analysis
            health_result = health_engine.predict(request.initiative_data)

            # Calculate processing time
            processing_time_ms = int(
                (datetime.now() - start_time).total_seconds() * 1000
            )

            # Create unified result
            result = P0AnalysisResult(
                request_id=request_id,
                timestamp=start_time.isoformat(),
                success=health_result.success,
                decisions_detected=0,
                decisions=[],
                decision_confidence=0.0,
                health_score=health_result.health_score,
                health_status=health_result.health_status,
                risk_level=health_result.risk_level,
                health_confidence=health_result.confidence,
                health_components=health_result.health_components,
                risk_assessment=health_result.risk_assessment,
                recommendations=health_result.recommendations,
                processing_time_ms=processing_time_ms,
                model_versions={
                    "health_prediction": health_engine.get_configuration().get(
                        "model_name", "unknown"
                    )
                },
                error=health_result.error,
            )

            self.logger.info(
                "Initiative health assessment completed",
                request_id=request_id,
                health_score=result.health_score,
                health_status=result.health_status,
                risk_level=result.risk_level,
                recommendations_count=len(result.recommendations),
                processing_time_ms=processing_time_ms,
            )

            return result

        except Exception as e:
            processing_time_ms = int(
                (datetime.now() - start_time).total_seconds() * 1000
            )
            self.logger.error(
                "Initiative health assessment failed",
                request_id=request_id,
                error=str(e),
            )

            return P0AnalysisResult(
                request_id=request_id,
                timestamp=start_time.isoformat(),
                success=False,
                decisions_detected=0,
                decisions=[],
                decision_confidence=0.0,
                health_score=None,
                health_status=None,
                risk_level=None,
                health_confidence=None,
                health_components=None,
                risk_assessment=None,
                recommendations=[],
                processing_time_ms=processing_time_ms,
                model_versions={},
                error=str(e),
            )

    async def comprehensive_analysis(
        self, content: str, initiative_data: Optional[Dict[str, Any]] = None
    ) -> P0AnalysisResult:
        """
        Perform comprehensive analysis combining decision intelligence and health assessment

        Args:
            content: Strategic content to analyze
            initiative_data: Optional initiative data for health assessment

        Returns:
            P0AnalysisResult: Combined analysis results
        """
        start_time = datetime.now()
        request_id = f"comprehensive_{int(start_time.timestamp() * 1000)}"

        try:
            self.logger.info(
                "Starting comprehensive strategic analysis",
                request_id=request_id,
                has_initiative_data=initiative_data is not None,
            )

            # Parallel execution of both analyses

            # Decision intelligence analysis
            decision_request = StrategicIntelligenceRequest(
                content=content,
                content_type="comprehensive",
                request_id=f"{request_id}_decision",
            )
            decision_task = self.analyze_strategic_content(decision_request)

            # Health assessment (if data provided)
            health_task = None
            if initiative_data:
                health_request = InitiativeHealthRequest(
                    initiative_data=initiative_data, request_id=f"{request_id}_health"
                )
                health_task = self.assess_initiative_health(health_request)

            # Execute analyses
            decision_result = await decision_task
            health_result = await health_task if health_task else None

            # Calculate total processing time
            processing_time_ms = int(
                (datetime.now() - start_time).total_seconds() * 1000
            )

            # Combine results
            model_versions = decision_result.model_versions.copy()
            if health_result:
                model_versions.update(health_result.model_versions)

            combined_result = P0AnalysisResult(
                request_id=request_id,
                timestamp=start_time.isoformat(),
                success=decision_result.success
                and (health_result.success if health_result else True),
                decisions_detected=decision_result.decisions_detected,
                decisions=decision_result.decisions,
                decision_confidence=decision_result.decision_confidence,
                health_score=health_result.health_score if health_result else None,
                health_status=health_result.health_status if health_result else None,
                risk_level=health_result.risk_level if health_result else None,
                health_confidence=(
                    health_result.health_confidence if health_result else None
                ),
                health_components=(
                    health_result.health_components if health_result else None
                ),
                risk_assessment=(
                    health_result.risk_assessment if health_result else None
                ),
                recommendations=health_result.recommendations if health_result else [],
                processing_time_ms=processing_time_ms,
                model_versions=model_versions,
                error=decision_result.error
                or (health_result.error if health_result else None),
            )

            self.logger.info(
                "Comprehensive strategic analysis completed",
                request_id=request_id,
                decisions_detected=combined_result.decisions_detected,
                health_score=combined_result.health_score,
                recommendations_count=len(combined_result.recommendations),
                processing_time_ms=processing_time_ms,
            )

            return combined_result

        except Exception as e:
            processing_time_ms = int(
                (datetime.now() - start_time).total_seconds() * 1000
            )
            self.logger.error(
                "Comprehensive strategic analysis failed",
                request_id=request_id,
                error=str(e),
            )

            return P0AnalysisResult(
                request_id=request_id,
                timestamp=start_time.isoformat(),
                success=False,
                decisions_detected=0,
                decisions=[],
                decision_confidence=0.0,
                health_score=None,
                health_status=None,
                risk_level=None,
                health_confidence=None,
                health_components=None,
                risk_assessment=None,
                recommendations=[],
                processing_time_ms=processing_time_ms,
                model_versions={},
                error=str(e),
            )

    async def get_service_health(self) -> Dict[str, Any]:
        """
        Get P0 service health status

        Returns:
            Dict containing service health information
        """
        try:
            service_health = {
                "timestamp": datetime.now().isoformat(),
                "service_status": "healthy",
                "features": {
                    "decision_intelligence": {
                        "enabled": self.config.enable_decision_intelligence,
                        "status": "unknown",
                    },
                    "health_prediction": {
                        "enabled": self.config.enable_health_prediction,
                        "status": "unknown",
                    },
                },
                "performance": {
                    "decision_engine_loaded": self._decision_engine is not None,
                    "health_engine_loaded": self._health_engine is not None,
                },
            }

            # Check decision engine health
            if self.config.enable_decision_intelligence:
                try:
                    decision_engine = await self._get_decision_engine()
                    if decision_engine.is_model_loaded():
                        service_health["features"]["decision_intelligence"][
                            "status"
                        ] = "healthy"

                        # Check SLA compliance
                        from ..shared.infrastructure.config import PerformanceThresholds

                        thresholds = PerformanceThresholds()
                        sla_compliance = decision_engine.check_sla_compliance(
                            thresholds
                        )
                        service_health["features"]["decision_intelligence"][
                            "sla_compliance"
                        ] = sla_compliance
                    else:
                        service_health["features"]["decision_intelligence"][
                            "status"
                        ] = "model_not_loaded"
                except Exception as e:
                    service_health["features"]["decision_intelligence"][
                        "status"
                    ] = f"error: {str(e)}"

            # Check health engine health
            if self.config.enable_health_prediction:
                try:
                    health_engine = await self._get_health_engine()
                    if health_engine.is_model_loaded():
                        service_health["features"]["health_prediction"][
                            "status"
                        ] = "healthy"

                        # Check SLA compliance
                        from ..shared.infrastructure.config import PerformanceThresholds

                        thresholds = PerformanceThresholds()
                        sla_compliance = health_engine.check_sla_compliance(thresholds)
                        service_health["features"]["health_prediction"][
                            "sla_compliance"
                        ] = sla_compliance
                    else:
                        service_health["features"]["health_prediction"][
                            "status"
                        ] = "model_not_loaded"
                except Exception as e:
                    service_health["features"]["health_prediction"][
                        "status"
                    ] = f"error: {str(e)}"

            # Determine overall service status
            feature_statuses = [
                f["status"] for f in service_health["features"].values() if f["enabled"]
            ]
            if all(status == "healthy" for status in feature_statuses):
                service_health["service_status"] = "healthy"
            elif any("error" in status for status in feature_statuses):
                service_health["service_status"] = "degraded"
            else:
                service_health["service_status"] = "starting"

            return service_health

        except Exception as e:
            self.logger.error("Failed to get service health", error=str(e))
            return {
                "timestamp": datetime.now().isoformat(),
                "service_status": "error",
                "error": str(e),
            }

    # Private methods for lazy loading and dependency management

    async def _get_decision_engine(self) -> IDecisionIntelligenceEngine:
        """Get or create decision intelligence engine (lazy loading)"""
        if self._decision_engine is None:
            self._decision_engine = self.model_factory.create_decision_engine()

            # Ensure model is loaded
            if not self._decision_engine.is_model_loaded():
                success = self._decision_engine.load_model()
                if not success:
                    raise RuntimeError("Failed to load decision intelligence model")

        return self._decision_engine

    async def _get_health_engine(self) -> IHealthPredictionEngine:
        """Get or create health assessment engine (lazy loading)"""
        if self._health_engine is None:
            self._health_engine = self.model_factory.create_health_engine()

            # Ensure model is loaded
            if not self._health_engine.is_model_loaded():
                success = self._health_engine.load_model()
                if not success:
                    raise RuntimeError("Failed to load health assessment model")

        return self._health_engine


# Convenience functions for service access

_service_instance: Optional[P0StrategicIntelligenceService] = None


def get_p0_service(
    config: Optional[P0FeatureConfig] = None,
) -> P0StrategicIntelligenceService:
    """
    Get global P0 service instance (singleton pattern)

    Args:
        config: Optional configuration override

    Returns:
        P0StrategicIntelligenceService: Service instance
    """
    global _service_instance
    if _service_instance is None or config is not None:
        _service_instance = P0StrategicIntelligenceService(config=config)
    return _service_instance


def reset_p0_service():
    """Reset global service instance (for testing)"""
    global _service_instance
    _service_instance = None
