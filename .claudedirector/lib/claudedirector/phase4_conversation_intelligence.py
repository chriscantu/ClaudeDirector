"""
Phase 4.1: Conversation Intelligence - Main Entry Point
Complete integration of enhanced framework engine, persona orchestration, and conversation memory.

This is the primary interface for Phase 4.1 conversation intelligence capabilities
while maintaining full backwards compatibility.

Zero-setup, chat-only, conversation-native intelligence.

Author: Martin (Phase 4 Lead), Rachel (UX Integration), Camille (Strategic Architecture)
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import structlog

# Import Phase 4.1 core components
from .core.persona_enhanced_integration import ConversationIntelligenceEngine
from .core.enhanced_framework_engine import EnhancedFrameworkEngine
from .core.embedded_framework_engine import (
    EmbeddedFrameworkEngine,
)  # Backwards compatibility

# Configure logging
logger = structlog.get_logger(__name__)


@dataclass
class ConversationIntelligenceResponse:
    """Complete conversation intelligence response for Phase 4.1"""

    # Main response (chat-ready)
    response: str
    persona: str
    confidence: float

    # Enhanced intelligence features
    frameworks_used: List[str]
    conversation_insights: Dict[str, Any]
    context_continuity: List[str]
    collaborative_suggestions: List[str]

    # Processing metadata
    processing_time_ms: int
    session_id: str
    intelligence_level: str

    # Backwards compatibility
    systematic_response: Optional[Dict[str, Any]] = None


class ClaudeDirectorPhase4:
    """
    Phase 4.1: Complete Conversation Intelligence System

    Main entry point that provides:
    - Multi-framework strategic analysis
    - Context-aware persona activation
    - Conversation memory and learning
    - Collaborative persona suggestions
    - Chat-native interface

    Maintains full backwards compatibility with existing ClaudeDirector interface.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

        # Initialize conversation intelligence engine
        self.intelligence_engine = ConversationIntelligenceEngine(self.config)

        # Backwards compatibility engines
        self.enhanced_engine = EnhancedFrameworkEngine(self.config)
        self.base_engine = EmbeddedFrameworkEngine(self.config)

        # Conversation intelligence settings
        self.intelligence_mode = self.config.get(
            "intelligence_mode", "enhanced"
        )  # enhanced, standard, auto
        self.enable_context_memory = self.config.get("enable_context_memory", True)
        self.enable_persona_collaboration = self.config.get(
            "enable_persona_collaboration", True
        )
        self.enable_framework_blending = self.config.get(
            "enable_framework_blending", True
        )

        # Performance settings
        self.max_response_time_ms = self.config.get("max_response_time_ms", 5000)
        self.fallback_on_timeout = self.config.get("fallback_on_timeout", True)

        logger.info(
            "ClaudeDirector Phase 4.1 initialized",
            intelligence_mode=self.intelligence_mode,
            context_memory=self.enable_context_memory,
            persona_collaboration=self.enable_persona_collaboration,
            framework_blending=self.enable_framework_blending,
        )

    def respond(
        self,
        user_input: str,
        session_id: str = "default",
        persona_hint: Optional[str] = None,
        **kwargs,
    ) -> ConversationIntelligenceResponse:
        """
        Main conversation response method for Phase 4.1

        Provides enhanced conversation intelligence while maintaining backwards compatibility.

        Args:
            user_input: User's message or question
            session_id: Session identifier for context retention
            persona_hint: Optional persona preference
            **kwargs: Additional parameters for backwards compatibility

        Returns:
            ConversationIntelligenceResponse with enhanced intelligence features
        """
        start_time = time.time()

        try:
            # Process with enhanced conversation intelligence
            if self.intelligence_mode == "enhanced":
                result = self._process_enhanced_conversation(
                    user_input, session_id, persona_hint
                )
            elif self.intelligence_mode == "standard":
                result = self._process_standard_conversation(
                    user_input, session_id, persona_hint
                )
            else:  # auto mode
                result = self._process_auto_conversation(
                    user_input, session_id, persona_hint
                )

            # Add processing time
            processing_time = int((time.time() - start_time) * 1000)
            result["processing_time_ms"] = processing_time

            # Check performance and fallback if needed
            if processing_time > self.max_response_time_ms and self.fallback_on_timeout:
                logger.warning(
                    "Response time exceeded threshold, considering fallback",
                    processing_time=processing_time,
                    threshold=self.max_response_time_ms,
                )

            return ConversationIntelligenceResponse(
                response=result["response"],
                persona=result["persona"],
                confidence=result["confidence"],
                frameworks_used=result.get("frameworks_used", []),
                conversation_insights=result.get("conversation_insights", {}),
                context_continuity=result.get("context_continuity", []),
                collaborative_suggestions=result.get("collaborative_suggestions", []),
                processing_time_ms=processing_time,
                session_id=session_id,
                intelligence_level=self.intelligence_mode,
                systematic_response=result.get("systematic_response"),
            )

        except Exception as e:
            logger.error("Enhanced conversation processing failed", error=str(e))

            # Fallback to base engine for reliability
            fallback_result = self._fallback_response(
                user_input, persona_hint or "camille"
            )
            processing_time = int((time.time() - start_time) * 1000)

            return ConversationIntelligenceResponse(
                response=fallback_result,
                persona=persona_hint or "camille",
                confidence=0.7,  # Moderate confidence for fallback
                frameworks_used=["rumelt_strategy_kernel"],  # Default framework
                conversation_insights={"mode": "fallback"},
                context_continuity=[],
                collaborative_suggestions=[],
                processing_time_ms=processing_time,
                session_id=session_id,
                intelligence_level="fallback",
            )

    def _process_enhanced_conversation(
        self, user_input: str, session_id: str, persona_hint: Optional[str]
    ) -> Dict[str, Any]:
        """Process conversation with full enhanced intelligence"""
        return self.intelligence_engine.process_conversation(
            user_input, session_id, persona_hint
        )

    def _process_standard_conversation(
        self, user_input: str, session_id: str, persona_hint: Optional[str]
    ) -> Dict[str, Any]:
        """Process conversation with standard framework engine (backwards compatible)"""
        # Use enhanced engine but in single-framework mode
        enhanced_response = self.enhanced_engine.analyze_systematically(
            user_input, session_id
        )

        return {
            "response": enhanced_response.persona_integrated_response,
            "persona": persona_hint or "camille",
            "confidence": enhanced_response.multi_framework_analysis.confidence_score,
            "frameworks_used": enhanced_response.frameworks_applied,
            "conversation_insights": {
                "mode": "standard",
                "frameworks_applied": len(enhanced_response.frameworks_applied),
            },
            "systematic_response": {
                "analysis": asdict(
                    enhanced_response.multi_framework_analysis.primary_framework
                ),
                "processing_time_ms": enhanced_response.processing_time_ms,
            },
        }

    def _process_auto_conversation(
        self, user_input: str, session_id: str, persona_hint: Optional[str]
    ) -> Dict[str, Any]:
        """Automatically choose between enhanced and standard based on input complexity"""
        # Simple heuristic for complexity
        input_complexity = self._assess_input_complexity(user_input)

        if input_complexity > 0.6:  # High complexity - use enhanced
            return self._process_enhanced_conversation(
                user_input, session_id, persona_hint
            )
        else:  # Low complexity - use standard
            return self._process_standard_conversation(
                user_input, session_id, persona_hint
            )

    def _assess_input_complexity(self, user_input: str) -> float:
        """Assess input complexity to determine processing mode"""
        complexity_score = 0.0

        # Length factor
        complexity_score += min(len(user_input) / 200, 0.3)

        # Multiple question indicators
        question_count = user_input.count("?")
        complexity_score += min(question_count * 0.1, 0.2)

        # Strategic complexity keywords
        complex_keywords = [
            "strategy",
            "organization",
            "decision",
            "platform",
            "architecture",
            "stakeholder",
            "transformation",
            "scaling",
            "comprehensive",
            "integration",
        ]

        keyword_matches = sum(
            1 for keyword in complex_keywords if keyword.lower() in user_input.lower()
        )
        complexity_score += min(keyword_matches * 0.1, 0.4)

        # Multi-domain indicators
        domains = ["business", "technical", "people", "process", "financial"]
        domain_matches = sum(1 for domain in domains if domain in user_input.lower())
        if domain_matches > 1:
            complexity_score += 0.2

        return min(complexity_score, 1.0)

    def _fallback_response(self, user_input: str, persona: str) -> str:
        """Generate fallback response using base engine"""
        try:
            base_response = self.base_engine.analyze_systematically(user_input)
            return f"[{persona.title()}] {base_response.persona_integrated_response}"
        except Exception:
            return f"[{persona.title()}] I'm here to help with your strategic challenges. Could you provide more specific details about what you'd like to explore?"

    # Backwards compatibility methods
    def analyze_systematically(
        self,
        user_input: str,
        framework_name: Optional[str] = None,
        session_id: str = "default",
    ) -> Dict[str, Any]:
        """Backwards compatible systematic analysis method"""
        if framework_name:
            # Direct framework request - use base engine
            base_response = self.base_engine.analyze_systematically(
                user_input, framework_name
            )
            return {
                "analysis": asdict(base_response.analysis),
                "response": base_response.persona_integrated_response,
                "framework_applied": base_response.framework_applied,
                "processing_time_ms": base_response.processing_time_ms,
            }
        else:
            # Enhanced analysis
            enhanced_response = self.enhanced_engine.analyze_systematically(
                user_input, session_id
            )
            return {
                "analysis": asdict(
                    enhanced_response.multi_framework_analysis.primary_framework
                ),
                "response": enhanced_response.persona_integrated_response,
                "framework_applied": (
                    enhanced_response.frameworks_applied[0]
                    if enhanced_response.frameworks_applied
                    else "rumelt_strategy_kernel"
                ),
                "processing_time_ms": enhanced_response.processing_time_ms,
                "enhanced_features": {
                    "frameworks_used": enhanced_response.frameworks_applied,
                    "confidence_score": enhanced_response.multi_framework_analysis.confidence_score,
                    "context_relevance": enhanced_response.multi_framework_analysis.context_relevance,
                },
            }

    def simple_response(self, user_input: str, persona: str = "camille") -> str:
        """Simple response method for backwards compatibility"""
        result = self.respond(user_input, persona_hint=persona)
        return result.response

    def get_available_frameworks(self) -> List[str]:
        """Get available frameworks (backwards compatible)"""
        return self.base_engine.get_available_frameworks()

    def get_framework_info(self, framework_name: str) -> Dict[str, Any]:
        """Get framework information (backwards compatible)"""
        return self.base_engine.get_framework_info(framework_name)

    # Phase 4.1 specific methods
    def get_conversation_stats(self, session_id: str) -> Dict[str, Any]:
        """Get conversation statistics for a session"""
        return self.intelligence_engine.get_conversation_stats(session_id)

    def get_persona_recommendations(self, user_input: str) -> List[Dict[str, Any]]:
        """Get persona recommendations for user input"""
        # Use orchestrator to determine optimal personas
        orchestrator = self.intelligence_engine.orchestrator

        try:
            # Create mock enhanced response for persona determination
            from unittest.mock import Mock

            mock_response = Mock()
            mock_response.frameworks_applied = ["rumelt_strategy_kernel"]  # Default

            # Get conversation context
            context = orchestrator.enhanced_engine.memory_engine.get_or_create_context(
                "temp_session"
            )

            optimal_personas = orchestrator._determine_optimal_personas(
                user_input, mock_response, None
            )

            # Get framework affinities for each persona
            recommendations = []
            for persona in optimal_personas[:3]:  # Top 3 personas
                persona_frameworks = orchestrator.get_persona_frameworks(persona)
                recommendations.append(
                    {
                        "persona": persona,
                        "relevance_score": 0.8,  # Placeholder
                        "preferred_frameworks": persona_frameworks[:3],
                        "specialization": self._get_persona_specialization(persona),
                    }
                )

            return recommendations

        except Exception as e:
            logger.warning("Persona recommendations failed", error=str(e))
            return [
                {
                    "persona": "camille",
                    "relevance_score": 0.7,
                    "preferred_frameworks": ["rumelt_strategy_kernel"],
                    "specialization": "Strategic Leadership",
                }
            ]

    def _get_persona_specialization(self, persona: str) -> str:
        """Get persona specialization description"""
        specializations = {
            "alvaro": "Business Strategy & ROI Analysis",
            "rachel": "Team Dynamics & User Experience",
            "martin": "Platform Architecture & Technical Strategy",
            "diego": "Engineering Leadership & Organization",
            "camille": "Executive Strategy & Transformation",
            "marcus": "Internal Adoption & Change Management",
            "david": "Financial Planning & Resource Allocation",
        }
        return specializations.get(persona, "Strategic Advisory")

    def set_intelligence_mode(self, mode: str) -> None:
        """Set conversation intelligence mode"""
        valid_modes = ["enhanced", "standard", "auto"]
        if mode in valid_modes:
            self.intelligence_mode = mode
            logger.info("Intelligence mode updated", mode=mode)
        else:
            raise ValueError(f"Invalid mode. Must be one of: {valid_modes}")

    def get_system_status(self) -> Dict[str, Any]:
        """Get Phase 4.1 system status"""
        return {
            "phase": "4.1",
            "version": "conversation_intelligence",
            "intelligence_mode": self.intelligence_mode,
            "features": {
                "context_memory": self.enable_context_memory,
                "persona_collaboration": self.enable_persona_collaboration,
                "framework_blending": self.enable_framework_blending,
            },
            "engines": {
                "conversation_intelligence": self.intelligence_engine is not None,
                "enhanced_framework": self.enhanced_engine is not None,
                "base_framework": self.base_engine is not None,
            },
            "performance": {
                "max_response_time_ms": self.max_response_time_ms,
                "fallback_enabled": self.fallback_on_timeout,
            },
            "backwards_compatibility": True,
        }


# Default instance for easy import and usage
default_director = ClaudeDirectorPhase4()


# Convenience functions for easy integration
def respond_intelligently(
    user_input: str,
    session_id: str = "default",
    persona: Optional[str] = None,
    **kwargs,
) -> ConversationIntelligenceResponse:
    """
    Main conversation intelligence function for Phase 4.1

    Zero-setup conversation intelligence with enhanced strategic analysis.
    """
    return default_director.respond(user_input, session_id, persona, **kwargs)


def simple_strategic_response(user_input: str, persona: str = "camille") -> str:
    """Simple strategic response for backwards compatibility"""
    return default_director.simple_response(user_input, persona)


def analyze_with_framework(user_input: str, framework_name: str) -> Dict[str, Any]:
    """Analyze input with specific framework (backwards compatible)"""
    return default_director.analyze_systematically(user_input, framework_name)


def get_conversation_insights(session_id: str) -> Dict[str, Any]:
    """Get conversation insights for session"""
    return default_director.get_conversation_stats(session_id)


# Export main interface
__all__ = [
    "ClaudeDirectorPhase4",
    "ConversationIntelligenceResponse",
    "respond_intelligently",
    "simple_strategic_response",
    "analyze_with_framework",
    "get_conversation_insights",
    "default_director",
]
