"""
Persona Enhancement Engine with Embedded Frameworks
Coordinates embedded strategic frameworks with persona personalities to provide enhanced capabilities
while preserving authentic persona characteristics.

Author: Martin (Principal Platform Architect)
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
import structlog

from .embedded_framework_engine import (
    EmbeddedFrameworkEngine,
    EmbeddedPersonaIntegrator,
)
from .complexity_analyzer import (
    AnalysisComplexityDetector,
    ComplexityAnalysis,
    EnhancementStrategy,
)

# Configure logging
logger = structlog.get_logger(__name__)


@dataclass
class EnhancementContext:
    """Context for persona enhancement"""

    persona_name: str
    user_input: str
    base_response: str
    complexity_analysis: ComplexityAnalysis
    enhancement_type: Optional[str]
    conversation_context: Optional[Dict[str, Any]] = None


@dataclass
class EnhancementResult:
    """Result of persona enhancement"""

    enhanced_response: str
    enhancement_applied: bool
    framework_used: Optional[str]
    analysis_data: Optional[Dict[str, Any]]
    processing_time_ms: int
    fallback_reason: Optional[str] = None


class PersonaEnhancementEngine:
    """
    Coordinates embedded strategic frameworks with persona personalities.

    Provides systematic analysis while preserving persona authenticity.
    Handles framework selection, response integration, and graceful degradation.
    """

    def __init__(
        self,
        complexity_detector: AnalysisComplexityDetector,
        config: Optional[Dict] = None,
    ):
        self.complexity_detector = complexity_detector
        self.config = config or {}

        # Initialize embedded framework engine
        self.framework_engine = EmbeddedFrameworkEngine(config)
        self.persona_integrator = EmbeddedPersonaIntegrator(self.framework_engine)

        # Persona personality filters - preserve authentic voice
        self.persona_filters = {
            "diego": {
                "voice_characteristics": [
                    "warm and engaging",
                    "collaborative",
                    "multinational perspective",
                    "emotionally intelligent",
                    "pragmatic",
                    "solution-focused",
                ],
                "communication_patterns": {
                    "opening_style": [
                        "Great to connect!",
                        "I'm excited about this challenge",
                        "Let's dive into this",
                    ],
                    "transition_phrases": [
                        "Here's what I'm thinking",
                        "From my experience",
                        "Let me share what's worked",
                    ],
                    "analytical_markers": [
                        "Looking at this systematically",
                        "Breaking this down",
                        "Here's the framework I'd use",
                    ],
                    "personal_touches": [
                        "😊",
                        "What's your gut feeling?",
                        "Let's get real about this",
                    ],
                    "closure_style": [
                        "What resonates most?",
                        "How does this land?",
                        "Let's build on this together",
                    ],
                },
                "systematic_integration": {
                    "prefix_patterns": [
                        "Let me work through this systematically...",
                        "I've been thinking about frameworks for this...",
                        "Here's how I'd approach this step-by-step...",
                    ],
                    "framework_intro": [
                        "Using proven strategic planning approaches...",
                        "Drawing from organizational analysis frameworks...",
                        "Following systematic methodology...",
                    ],
                    "analysis_wrapping": [
                        "What this analysis tells us is...",
                        "The systematic approach suggests...",
                        "Based on this framework...",
                    ],
                },
            },
            "martin": {
                "voice_characteristics": [
                    "thoughtful",
                    "measured",
                    "precise",
                    "pattern-focused",
                    "evolutionary thinking",
                    "principled",
                ],
                "communication_patterns": {
                    "opening_style": [
                        "Let me think about this",
                        "There's an interesting pattern here",
                        "This reminds me of",
                    ],
                    "analytical_markers": [
                        "The trade-offs are",
                        "Evolutionarily",
                        "From an architectural perspective",
                    ],
                    "framework_integration": [
                        "This follows the pattern of",
                        "Using established principles",
                        "The framework suggests",
                    ],
                },
            },
            "rachel": {
                "voice_characteristics": [
                    "collaborative",
                    "user-centered",
                    "systems thinking",
                    "inclusive",
                    "practical",
                    "empathetic",
                ],
                "communication_patterns": {
                    "opening_style": [
                        "Let's think about the user experience",
                        "I love where this is going",
                        "How does this feel for teams?",
                    ],
                    "framework_integration": [
                        "Design systems research shows",
                        "User-centered frameworks suggest",
                        "Cross-team patterns indicate",
                    ],
                },
            },
        }

        # Enhancement quality thresholds
        self.quality_thresholds = {
            "minimum_enhancement_value": 0.3,  # Don't enhance unless adding significant value
            "personality_preservation": 0.8,  # Must maintain persona authenticity
            "response_coherence": 0.7,  # Enhanced response must be coherent
            "processing_timeout": 10.0,  # Maximum time for enhancement (seconds)
        }

    def enhance_response(
        self,
        persona_name: str,
        user_input: str,
        base_response: str,
        conversation_context: Optional[Dict[str, Any]] = None,
    ) -> EnhancementResult:
        """
        Enhance persona response with embedded framework capabilities.

        Args:
            persona_name: Name of the persona providing response
            user_input: Original user input/question
            base_response: Standard persona response
            conversation_context: Optional conversation history and context

        Returns:
            EnhancementResult with enhanced response or fallback reasoning
        """
        start_time = time.time()

        try:
            # Analyze input complexity
            context_dict = {"current_persona": persona_name}
            if conversation_context:
                context_dict.update(conversation_context)

            complexity_analysis = self.complexity_detector.analyze_input_complexity(
                user_input, context=context_dict
            )

            # Determine if enhancement should be applied
            should_enhance, enhancement_type = (
                self._should_enhance_with_embedded_framework(
                    complexity_analysis,
                    persona_name,
                    self.config.get("enhancement_thresholds"),
                )
            )

            if not should_enhance:
                processing_time = int((time.time() - start_time) * 1000)
                return EnhancementResult(
                    enhanced_response=base_response,
                    enhancement_applied=False,
                    framework_used=None,
                    analysis_data=None,
                    processing_time_ms=processing_time,
                    fallback_reason="Below enhancement threshold or persona not suitable",
                )

            # Create enhancement context
            context = EnhancementContext(
                persona_name=persona_name,
                user_input=user_input,
                base_response=base_response,
                complexity_analysis=complexity_analysis,
                enhancement_type=enhancement_type,
                conversation_context=conversation_context,
            )

            # Apply embedded framework enhancement
            enhanced_response = self._apply_embedded_enhancement(context)

            if enhanced_response:
                processing_time = int((time.time() - start_time) * 1000)

                logger.info(
                    "persona_enhancement_success",
                    persona=persona_name,
                    framework_type=enhancement_type,
                    complexity=complexity_analysis.complexity.value,
                    strategy=complexity_analysis.enhancement_strategy.value,
                    processing_time_ms=processing_time,
                )

                return EnhancementResult(
                    enhanced_response=enhanced_response,
                    enhancement_applied=True,
                    framework_used=enhancement_type,
                    analysis_data=self._extract_analysis_metadata(complexity_analysis),
                    processing_time_ms=processing_time,
                )
            else:
                # Fallback to base response
                processing_time = int((time.time() - start_time) * 1000)
                return EnhancementResult(
                    enhanced_response=base_response,
                    enhancement_applied=False,
                    framework_used=None,
                    analysis_data=None,
                    processing_time_ms=processing_time,
                    fallback_reason="Embedded framework enhancement failed",
                )

        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            logger.error(
                "persona_enhancement_error",
                persona=persona_name,
                error=str(e),
                processing_time_ms=processing_time,
            )

            return EnhancementResult(
                enhanced_response=base_response,
                enhancement_applied=False,
                framework_used=None,
                analysis_data=None,
                processing_time_ms=processing_time,
                fallback_reason=f"Enhancement error: {str(e)}",
            )

    def _should_enhance_with_embedded_framework(
        self,
        analysis: ComplexityAnalysis,
        persona: str,
        thresholds: Optional[Dict[str, float]] = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        Determine if embedded framework enhancement should be used for this persona.

        Args:
            analysis: The complexity analysis result
            persona: The target persona name
            thresholds: Override thresholds from config

        Returns:
            Tuple of (should_enhance, enhancement_type)
        """
        if not thresholds:
            thresholds = self.config.get(
                "enhancement_thresholds",
                {
                    "systematic_analysis": 0.7,
                    "framework_lookup": 0.6,
                    "visual_generation": 0.8,
                    "minimum_complexity": 0.5,
                },
            )

        # Check minimum complexity threshold
        if analysis.confidence < thresholds.get("minimum_complexity", 0.5):
            return False, None

        # Check persona suitability
        persona_score = analysis.persona_suitability.get(persona, 0.0)
        if persona_score < 0.3:  # Minimum persona suitability
            return False, None

        # Determine enhancement type based on strategy
        strategy_mapping = {
            EnhancementStrategy.SYSTEMATIC_ANALYSIS: "systematic_analysis",
            EnhancementStrategy.LIGHT_FRAMEWORK: "framework_lookup",
            EnhancementStrategy.VISUAL_ENHANCEMENT: "visual_generation",
        }

        enhancement_type = strategy_mapping.get(analysis.enhancement_strategy)
        if not enhancement_type:
            return False, None

        # Check strategy-specific thresholds
        required_threshold = thresholds.get(enhancement_type, 0.7)

        if analysis.confidence >= required_threshold:
            return True, enhancement_type

        return False, None

    def _apply_embedded_enhancement(self, context: EnhancementContext) -> Optional[str]:
        """Apply embedded framework enhancement to persona response"""

        try:
            # Determine domain focus based on complexity analysis
            domain_focus = self._determine_domain_focus(context.complexity_analysis)

            # Create systematic response using embedded framework
            systematic_response = self.persona_integrator.create_systematic_response(
                persona_name=context.persona_name,
                user_input=context.user_input,
                base_response=context.base_response,
                domain_focus=domain_focus,
                complexity_level=context.complexity_analysis.complexity.value,
            )

            if systematic_response and systematic_response.persona_integrated_response:
                logger.info(
                    "embedded_framework_enhancement_success",
                    persona=context.persona_name,
                    framework=systematic_response.framework_applied,
                    processing_time_ms=systematic_response.processing_time_ms,
                )
                return systematic_response.persona_integrated_response
            else:
                logger.warning(
                    "embedded_framework_enhancement_failed",
                    persona=context.persona_name,
                    enhancement_type=context.enhancement_type,
                )
                return None

        except Exception as e:
            logger.error(
                "embedded_framework_enhancement_error",
                persona=context.persona_name,
                error=str(e),
            )
            return None

    def _determine_domain_focus(self, analysis: ComplexityAnalysis) -> List[str]:
        """Determine domain focus from complexity analysis"""

        # Map capabilities to domains
        capability_domain_map = {
            "systematic_analysis": "strategic",
            "strategic_planning": "strategic",
            "leadership_frameworks": "organizational",
            "organizational_analysis": "organizational",
            "pattern_access": "technical",
            "architectural_patterns": "technical",
            "methodology_lookup": "process",
            "best_practices": "process",
        }

        # Extract domains from recommended capabilities
        domains = []
        for capability in analysis.recommended_capabilities:
            domain = capability_domain_map.get(capability)
            if domain and domain not in domains:
                domains.append(domain)

        # Default to strategic if no specific domains identified
        if not domains:
            domains = ["strategic"]

        return domains

    def _extract_analysis_metadata(
        self, analysis: ComplexityAnalysis
    ) -> Dict[str, Any]:
        """Extract metadata from complexity analysis for tracking"""
        return {
            "complexity": analysis.complexity.value,
            "confidence": analysis.confidence,
            "strategy": analysis.enhancement_strategy.value,
            "capabilities": analysis.recommended_capabilities,
            "trigger_keywords": analysis.trigger_keywords,
            "reasoning": analysis.reasoning,
        }
