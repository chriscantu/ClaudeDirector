"""
Embedded Strategic Framework Engine - SOLID Refactored
Provides systematic analysis capabilities without external dependencies.

REFACTORED: This file now uses SOLID-compliant service architecture instead of
monolithic implementation. The original 2,338-line class has been replaced with
service orchestration following all SOLID principles.

Author: Martin (Principal Platform Architect) - SOLID Refactoring
"""

from typing import Dict, List, Optional, Any
import structlog

# Import shared types to avoid circular imports
from .framework_types import FrameworkAnalysis, SystematicResponse

# Configure logging
logger = structlog.get_logger(__name__)


class EmbeddedFrameworkEngine:
    """
    SOLID-Refactored Strategic Framework Engine

    This class now serves as a facade over the new SOLID-compliant service architecture.
    The original 2,338-line monolithic implementation has been replaced with service
    orchestration following all SOLID principles:

    - Single Responsibility: Each service has one focused purpose
    - Open/Closed: New frameworks via service injection
    - Liskov Substitution: All services are substitutable
    - Interface Segregation: Focused service interfaces
    - Dependency Inversion: Depends on abstractions

    BACKWARD COMPATIBILITY: Maintains the same public API as the original implementation.
    """

    def __init__(self, config: Optional[Dict] = None):
        """Initialize with SOLID-compliant service architecture"""
        self.config = config or {}

        # Lazy initialization to avoid circular imports
        self._refactored_engine = None

        # Extract framework definitions for backward compatibility
        self.strategic_frameworks = self._extract_framework_definitions()

        logger.info(
            "EmbeddedFrameworkEngine initialized with SOLID architecture",
            config_provided=config is not None,
            frameworks_available=len(self.strategic_frameworks),
        )

    def _get_refactored_engine(self):
        """Get the refactored engine, initializing if needed"""
        if self._refactored_engine is None:
            # Import here to avoid circular imports
            from .refactored_framework_engine import RefactoredFrameworkEngine

            self._refactored_engine = RefactoredFrameworkEngine(config=self.config)
        return self._refactored_engine

    def analyze_systematically(
        self,
        user_input: str,
        persona_context: Optional[Dict] = None,
        session_id: str = "default",
        domain_focus: Optional[List[str]] = None,
        **kwargs,
    ) -> SystematicResponse:
        """
        Perform systematic analysis using SOLID-compliant service architecture.

        REFACTORED: This method now orchestrates specialized services instead of
        implementing all logic in a monolithic class.
        """
        try:
            # Normalize persona_context for backward compatibility
            if isinstance(persona_context, str):
                persona_context = {"persona_name": persona_context}
            elif persona_context is None:
                persona_context = {}

            # Use the new SOLID-compliant engine
            result = self._get_refactored_engine().analyze_systematically(
                user_input=user_input,
                persona_context=persona_context,
                session_id=session_id,
                domain_focus=domain_focus,
                **kwargs,
            )

            # Convert to backward-compatible format
            return self._convert_to_legacy_format(result)

        except Exception as e:
            logger.error("Systematic analysis failed", error=str(e))
            return self._create_error_response(user_input, str(e))

    # Backward compatibility methods - now delegating to SOLID services

    def _select_framework(
        self, user_input: str, persona_context: Optional[Dict] = None
    ) -> Optional[str]:
        """Select framework using SOLID framework selection service"""
        return self._get_refactored_engine()._select_framework(
            user_input, persona_context
        )

    def _apply_framework(
        self, framework_name: str, user_input: str
    ) -> FrameworkAnalysis:
        """Apply framework using SOLID framework analysis service"""
        return self._get_refactored_engine()._apply_framework(
            framework_name, user_input
        )

    def _extract_framework_definitions(self) -> Dict[str, Any]:
        """Extract framework definitions for backward compatibility"""
        # Use static framework definitions to avoid circular dependency
        from .framework_definitions import get_strategic_frameworks

        return get_strategic_frameworks()

    def _convert_to_legacy_format(self, result) -> SystematicResponse:
        """Convert new SOLID result format to legacy SystematicResponse format"""
        analysis_result = result.analysis_result

        legacy_analysis = FrameworkAnalysis(
            framework_name=analysis_result.framework_name,
            structured_insights={
                "insights": [
                    {
                        "category": insight.category,
                        "insight": insight.insight,
                        "evidence": insight.evidence,
                        "confidence": insight.confidence,
                    }
                    for insight in analysis_result.insights
                ],
                "recommendations": [
                    {
                        "title": rec.title,
                        "description": rec.description,
                        "priority": rec.priority,
                    }
                    for rec in analysis_result.recommendations
                ],
            },
            recommendations=[
                rec.description for rec in analysis_result.recommendations
            ],
            implementation_steps=[
                step.description for step in analysis_result.implementation_steps
            ],
            key_considerations=[
                insight.insight
                for insight in analysis_result.insights
                if insight.category == "risk_mitigation"
            ],
            analysis_confidence=analysis_result.overall_confidence,
        )

        return SystematicResponse(
            analysis=legacy_analysis,
            persona_integrated_response=result.persona_integrated_response,
            processing_time_ms=result.processing_time_ms,
            framework_applied=result.framework_applied,
        )

    def _create_error_response(
        self, user_input: str, error_message: str
    ) -> SystematicResponse:
        """Create error response in legacy format"""
        error_analysis = FrameworkAnalysis(
            framework_name="error_fallback",
            structured_insights={"error": error_message},
            recommendations=["Review input and try again"],
            implementation_steps=["Address the error condition"],
            key_considerations=["System encountered an error during analysis"],
            analysis_confidence=0.1,
        )

        return SystematicResponse(
            analysis=error_analysis,
            persona_integrated_response="I encountered an issue during analysis. Please try again.",
            processing_time_ms=0,
            framework_applied="error_fallback",
        )


# Legacy class for backward compatibility
class EmbeddedPersonaIntegrator:
    """
    DEPRECATED: Legacy persona integrator for backward compatibility.

    This functionality is now handled by the SOLID-compliant PersonaIntegrator
    service in the new architecture.
    """

    def __init__(self, framework_engine: EmbeddedFrameworkEngine):
        """Initialize with framework engine reference"""
        self.framework_engine = framework_engine
        logger.warning(
            "EmbeddedPersonaIntegrator is deprecated. "
            "Use the new SOLID-compliant PersonaIntegrator service instead."
        )

    def create_systematic_response(
        self, user_input: str, persona_name: str = "diego", session_id: str = "default"
    ) -> SystematicResponse:
        """Create systematic response using the refactored engine"""
        persona_context = {"persona_name": persona_name}

        return self._get_refactored_engine().analyze_systematically(
            user_input=user_input,
            persona_context=persona_context,
            session_id=session_id,
        )
