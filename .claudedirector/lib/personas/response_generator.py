#!/usr/bin/env python3
"""
🎯 RESPONSE GENERATOR - SOLID Compliance Decomposition

Single Responsibility: Response generation and enhancement only.
Part of unified_persona_engine.py decomposition (1,514 → ~400 lines each).

Author: Martin | Platform Architecture
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

try:
    from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
except ImportError:
    from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType

# Import the decomposed components
from .persona_manager import PersonaType, PersonaBehavior
from .challenge_framework import ChallengeFramework


class StrategicThinkingDepth(Enum):
    """Strategic thinking depth levels"""

    SURFACE = "surface"
    ANALYTICAL = "analytical"
    STRATEGIC = "strategic"
    SYSTEMATIC = "systematic"


@dataclass
class EnhancedResponseResult:
    """Enhanced response result structure"""

    original_response: str
    enhanced_response: str
    persona_applied: PersonaType
    challenge_applied: Optional[str]
    frameworks_used: List[str]
    thinking_depth: StrategicThinkingDepth
    transparency_info: Dict[str, Any]
    processing_time: float


class ResponseGenerator(BaseManager):
    """
    🎯 SINGLE RESPONSIBILITY: Response generation and enhancement only

    Generates and enhances responses using persona behaviors and challenges.
    No longer handles persona management or challenge patterns directly.
    """

    def __init__(self, config: Optional[BaseManagerConfig] = None):
        """Initialize response generator with focused responsibility"""
        if config is None:
            config = BaseManagerConfig(
                manager_name="response_generator",
                manager_type=ManagerType.PERSONA,  # Use existing type
                enable_caching=True,
                enable_metrics=True,
            )

        super().__init__(config)
        self.challenge_framework = ChallengeFramework()
        self.response_cache = {}

        self.logger.info("ResponseGenerator initialized - focused responsibility")

    def manage(self) -> Dict[str, Any]:
        """Required BaseManager abstract method implementation"""
        return {
            "status": "active",
            "cache_size": len(self.response_cache),
            "challenge_framework_available": self.challenge_framework is not None,
            "responsibility": "response_generation_only",
        }

    def generate_enhanced_response(
        self,
        original_response: str,
        persona_behavior: PersonaBehavior,
        context: Dict[str, Any] = None,
    ) -> EnhancedResponseResult:
        """Generate enhanced response using persona behavior"""
        start_time = time.time()

        try:
            context = context or {}

            # Generate strategic challenge if needed
            challenge = None
            if persona_behavior.challenge_intensity > 0.5:
                challenge = self.challenge_framework.generate_challenge(
                    context, persona_behavior.challenge_intensity
                )

            # Enhance response based on persona
            enhanced_response = self._enhance_with_persona(
                original_response, persona_behavior, challenge, context
            )

            # Determine thinking depth
            thinking_depth = self._determine_thinking_depth(context, persona_behavior)

            # Create transparency info
            transparency_info = self._create_transparency_info(
                persona_behavior, challenge, context
            )

            processing_time = time.time() - start_time

            result = EnhancedResponseResult(
                original_response=original_response,
                enhanced_response=enhanced_response,
                persona_applied=persona_behavior.persona_type,
                challenge_applied=challenge,
                frameworks_used=persona_behavior.framework_focus or [],
                thinking_depth=thinking_depth,
                transparency_info=transparency_info,
                processing_time=processing_time,
            )

            self.logger.info(f"Enhanced response generated in {processing_time:.3f}s")
            return result

        except Exception as e:
            self.logger.error(f"Response enhancement failed: {e}")
            return self._get_fallback_response(original_response, persona_behavior)

    def _enhance_with_persona(
        self,
        response: str,
        behavior: PersonaBehavior,
        challenge: Optional[str],
        context: Dict[str, Any],
    ) -> str:
        """Enhance response with persona-specific behavior"""

        # Add persona header
        persona_header = f"**{behavior.persona_type.value.title()} | {self._get_persona_title(behavior.persona_type)}**"

        # Add challenge if present
        challenge_section = ""
        if challenge and behavior.challenge_intensity > 0.6:
            challenge_section = f"\n\n**🎯 Strategic Challenge Applied**: {challenge}\n"

        # Add framework attribution if specified
        framework_section = ""
        if behavior.framework_focus:
            frameworks = ", ".join(behavior.framework_focus)
            framework_section = f"\n\n📚 **Strategic Framework**: {frameworks} detected"

        # Combine enhanced response
        enhanced = (
            f"{persona_header}{challenge_section}\n\n{response}{framework_section}"
        )

        return enhanced

    def _get_persona_title(self, persona_type: PersonaType) -> str:
        """Get persona title for display"""
        titles = {
            PersonaType.DIEGO: "Engineering Leadership",
            PersonaType.CAMILLE: "Strategic Technology",
            PersonaType.RACHEL: "Design Systems Strategy",
            PersonaType.ALVARO: "Platform Investment Strategy",
            PersonaType.MARTIN: "Platform Architecture",
            PersonaType.MARCUS: "Platform Adoption",
            PersonaType.DAVID: "Financial Planning",
            PersonaType.SOFIA: "Vendor Strategy",
            PersonaType.ELENA: "Compliance Strategy",
        }
        return titles.get(persona_type, "Strategic Leadership")

    def _determine_thinking_depth(
        self, context: Dict[str, Any], behavior: PersonaBehavior
    ) -> StrategicThinkingDepth:
        """Determine appropriate thinking depth"""
        complexity_indicators = context.get("complexity_indicators", [])

        if len(complexity_indicators) > 3 or behavior.challenge_intensity > 0.8:
            return StrategicThinkingDepth.SYSTEMATIC
        elif len(complexity_indicators) > 1 or behavior.challenge_intensity > 0.6:
            return StrategicThinkingDepth.STRATEGIC
        elif behavior.challenge_intensity > 0.4:
            return StrategicThinkingDepth.ANALYTICAL
        else:
            return StrategicThinkingDepth.SURFACE

    def _create_transparency_info(
        self,
        behavior: PersonaBehavior,
        challenge: Optional[str],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create transparency information"""
        return {
            "persona_type": behavior.persona_type.value,
            "challenge_intensity": behavior.challenge_intensity,
            "challenge_applied": challenge is not None,
            "framework_focus": behavior.framework_focus or [],
            "response_style": behavior.response_style,
            "transparency_level": behavior.transparency_level,
            "context_complexity": len(context.get("complexity_indicators", [])),
        }

    def _get_fallback_response(
        self, original_response: str, behavior: PersonaBehavior
    ) -> EnhancedResponseResult:
        """Provide fallback response for error cases"""
        import time

        return EnhancedResponseResult(
            original_response=original_response,
            enhanced_response=f"**Strategic Leadership** - {original_response}",
            persona_applied=behavior.persona_type,
            challenge_applied=None,
            frameworks_used=[],
            thinking_depth=StrategicThinkingDepth.SURFACE,
            transparency_info={"fallback": True},
            processing_time=0.001,
        )

    def get_response_metrics(self) -> Dict[str, Any]:
        """Get response generation metrics"""
        return {
            "cache_size": len(self.response_cache),
            "challenge_framework_available": self.challenge_framework is not None,
            "thinking_depths": len(list(StrategicThinkingDepth)),
        }


# Import time at module level
import time
