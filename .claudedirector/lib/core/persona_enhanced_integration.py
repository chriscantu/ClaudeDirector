"""
Phase 4.1: Enhanced Persona Integration with Multi-Framework Engine
Seamlessly integrates enhanced framework capabilities with existing persona system.

Maintains backwards compatibility while adding conversation intelligence.

Author: Martin & Rachel (Phase 4 Collaboration)
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import structlog

# Import enhanced framework engine
from .enhanced_framework_engine import (
    EnhancedFrameworkEngine,
    EnhancedSystematicResponse
)

# Import existing persona system for integration
try:
    from .persona_activation_engine import PersonaManager, PersonaResponse
except ImportError:
    # Fallback for development/testing
    PersonaManager = None
    PersonaResponse = None

logger = structlog.get_logger(__name__)


@dataclass
class EnhancedPersonaResponse:
    """Enhanced persona response with multi-framework intelligence"""
    persona_name: str
    base_response: str
    enhanced_insights: Dict[str, Any]
    framework_integration: Dict[str, Any]
    conversation_continuity: List[str]
    collaborative_suggestions: List[str]
    confidence_score: float
    processing_time_ms: int


class PersonaFrameworkOrchestrator:
    """
    Orchestrates collaboration between personas and enhanced framework engine.

    Enables intelligent persona activation and framework selection based on
    conversation context and strategic needs.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.enhanced_engine = EnhancedFrameworkEngine(config)

        # Initialize persona manager if available
        self.persona_manager = self._initialize_persona_manager()

        # Persona-framework affinity mapping
        self.persona_framework_affinity = self._initialize_persona_affinities()

        # Enhanced activation thresholds
        self.activation_thresholds = {
            "single_persona": 0.7,
            "collaborative_personas": 0.8,
            "framework_enhancement": 0.6
        }

        logger.info("Persona Framework Orchestrator initialized",
                   persona_manager_available=self.persona_manager is not None,
                   enhanced_mode=self.enhanced_engine.enhanced_mode)

    def _initialize_persona_manager(self):
        """Initialize persona manager if available"""
        if PersonaManager is None:
            logger.warning("PersonaManager not available, using enhanced framework only")
            return None

        try:
            return PersonaManager(self.config)
        except Exception as e:
            logger.warning("Failed to initialize PersonaManager", error=str(e))
            return None

    def _initialize_persona_affinities(self) -> Dict[str, List[str]]:
        """Define which frameworks each persona prefers"""
        return {
            "alvaro": [
                "rumelt_strategy_kernel",
                "strategic_platform_assessment",
                "capital_allocation_framework",
                "decisive_wrap_framework"
            ],
            "rachel": [
                "team_topologies",
                "crucial_conversations",
                "organizational_transformation",
                "scaling_up_excellence"
            ],
            "martin": [
                "strategic_platform_assessment",
                "technical_strategy_framework",
                "rumelt_strategy_kernel",
                "accelerate_team_performance"
            ],
            "diego": [
                "organizational_transformation",
                "team_topologies",
                "accelerate_team_performance",
                "scaling_up_excellence"
            ],
            "camille": [
                "rumelt_strategy_kernel",
                "decisive_wrap_framework",
                "organizational_transformation",
                "integrated_strategic_decision"
            ],
            "marcus": [
                "scaling_up_excellence",
                "crucial_conversations",
                "organizational_transformation",
                "accelerate_team_performance"
            ],
            "david": [
                "capital_allocation_framework",
                "rumelt_strategy_kernel",
                "decisive_wrap_framework",
                "strategic_platform_assessment"
            ]
        }

    def analyze_with_enhanced_personas(self, user_input: str, session_id: str = "default",
                                     requested_persona: Optional[str] = None) -> EnhancedPersonaResponse:
        """
        Perform enhanced analysis with intelligent persona and framework integration.

        This is the main entry point for Phase 4.1 conversation intelligence.
        """
        start_time = time.time()

        # Step 1: Enhanced framework analysis
        enhanced_response = self.enhanced_engine.analyze_systematically(user_input, session_id)

        # Step 2: Determine optimal persona(s)
        optimal_personas = self._determine_optimal_personas(
            user_input, enhanced_response, requested_persona
        )

        # Step 3: Generate persona-specific response
        primary_persona = optimal_personas[0] if optimal_personas else "camille"

        if self.persona_manager:
            persona_response = self._generate_persona_response(
                primary_persona, enhanced_response, user_input
            )
        else:
            # Fallback to enhanced framework response
            persona_response = self._generate_fallback_response(
                primary_persona, enhanced_response
            )

        # Step 4: Generate collaborative suggestions
        collaborative_suggestions = self._generate_collaborative_suggestions(
            optimal_personas, enhanced_response, user_input
        )

        # Step 5: Extract framework integration insights
        framework_integration = self._extract_framework_integration(enhanced_response)

        processing_time = int((time.time() - start_time) * 1000)

        return EnhancedPersonaResponse(
            persona_name=primary_persona,
            base_response=persona_response,
            enhanced_insights=enhanced_response.learning_insights,
            framework_integration=framework_integration,
            conversation_continuity=enhanced_response.conversation_continuity_notes,
            collaborative_suggestions=collaborative_suggestions,
            confidence_score=enhanced_response.multi_framework_analysis.confidence_score,
            processing_time_ms=processing_time
        )

    def _determine_optimal_personas(self, user_input: str, enhanced_response: EnhancedSystematicResponse,
                                  requested_persona: Optional[str]) -> List[str]:
        """Determine which persona(s) are optimal for this conversation"""
        if requested_persona:
            return [requested_persona]

        # Analyze input and framework usage to determine best personas
        frameworks_applied = enhanced_response.frameworks_applied
        input_lower = user_input.lower()

        persona_scores = {}

        # Score personas based on framework affinity
        for persona, preferred_frameworks in self.persona_framework_affinity.items():
            framework_overlap = set(frameworks_applied).intersection(set(preferred_frameworks))
            framework_score = len(framework_overlap) / max(len(preferred_frameworks), 1)
            persona_scores[persona] = framework_score

        # Enhance scoring based on input content
        content_scoring = {
            "alvaro": ["business", "roi", "investment", "capital", "strategy", "executive"],
            "rachel": ["team", "people", "culture", "communication", "user", "experience"],
            "martin": ["platform", "architecture", "technical", "system", "engineering"],
            "diego": ["leadership", "organization", "management", "coordination"],
            "camille": ["strategic", "vision", "transformation", "executive", "decision"],
            "marcus": ["adoption", "change", "internal", "scaling", "excellence"],
            "david": ["cost", "budget", "financial", "allocation", "planning"]
        }

        for persona, keywords in content_scoring.items():
            keyword_matches = sum(1 for keyword in keywords if keyword in input_lower)
            content_score = keyword_matches / len(keywords)
            persona_scores[persona] = persona_scores.get(persona, 0) + content_score * 0.5

        # Return top scoring personas
        sorted_personas = sorted(persona_scores.items(), key=lambda x: x[1], reverse=True)

        # Filter by minimum threshold
        qualified_personas = [
            persona for persona, score in sorted_personas
            if score >= self.activation_thresholds["single_persona"]
        ]

        if not qualified_personas:
            # Fallback to default strategic personas
            return ["camille", "alvaro"]

        # Return top 2 personas for potential collaboration
        return qualified_personas[:2]

    def _generate_persona_response(self, persona_name: str, enhanced_response: EnhancedSystematicResponse,
                                 user_input: str) -> str:
        """Generate persona-specific response using enhanced framework insights"""
        if not self.persona_manager:
            return self._generate_fallback_response(persona_name, enhanced_response)

        try:
            # Extract key insights for persona context
            persona_context = {
                "frameworks_applied": enhanced_response.frameworks_applied,
                "confidence_score": enhanced_response.multi_framework_analysis.confidence_score,
                "strategic_themes": enhanced_response.multi_framework_analysis.integrated_insights.get("strategic_themes", []),
                "recommendations": enhanced_response.context_aware_recommendations[:3],
                "implementation_focus": enhanced_response.multi_framework_analysis.implementation_roadmap.get("immediate_actions", [])
            }

            # Generate persona response with enhanced context
            persona_response = self.persona_manager.generate_response(
                persona_name, user_input, context=persona_context
            )

            return persona_response.response if hasattr(persona_response, 'response') else str(persona_response)

        except Exception as e:
            logger.warning("Persona response generation failed", persona=persona_name, error=str(e))
            return self._generate_fallback_response(persona_name, enhanced_response)

    def _generate_fallback_response(self, persona_name: str, enhanced_response: EnhancedSystematicResponse) -> str:
        """Generate fallback response when persona manager is not available"""
        base_response = enhanced_response.persona_integrated_response

        # Add persona-specific framing
        persona_styles = {
            "alvaro": f"From a business strategy perspective: {base_response}",
            "rachel": f"Considering the people and design aspects: {base_response}",
            "martin": f"From a platform architecture standpoint: {base_response}",
            "diego": f"From an engineering leadership view: {base_response}",
            "camille": f"Strategic assessment: {base_response}",
            "marcus": f"For internal adoption and scaling: {base_response}",
            "david": f"From a financial planning perspective: {base_response}"
        }

        return persona_styles.get(persona_name, base_response)

    def _generate_collaborative_suggestions(self, personas: List[str],
                                          enhanced_response: EnhancedSystematicResponse,
                                          user_input: str) -> List[str]:
        """Generate suggestions for persona collaboration"""
        suggestions = []

        if len(personas) > 1:
            primary, secondary = personas[0], personas[1]

            collaboration_patterns = {
                ("alvaro", "rachel"): "Consider how business strategy aligns with team dynamics and user experience",
                ("alvaro", "martin"): "Evaluate the technical platform investment from a business ROI perspective",
                ("rachel", "martin"): "Balance technical architecture decisions with team structure and user needs",
                ("diego", "alvaro"): "Align engineering leadership initiatives with business strategic priorities",
                ("camille", "martin"): "Integrate executive strategic vision with platform technical roadmap",
                ("marcus", "rachel"): "Design change management approach that considers team culture and adoption patterns"
            }

            pattern_key = (primary, secondary)
            reverse_key = (secondary, primary)

            if pattern_key in collaboration_patterns:
                suggestions.append(collaboration_patterns[pattern_key])
            elif reverse_key in collaboration_patterns:
                suggestions.append(collaboration_patterns[reverse_key])

        # Add framework-based collaborative suggestions
        frameworks = enhanced_response.frameworks_applied
        if len(frameworks) > 1:
            suggestions.append(f"The {frameworks[0]} and {frameworks[1]} frameworks provide complementary perspectives on this challenge")

        # Add context-based suggestions
        if enhanced_response.conversation_continuity_notes:
            suggestions.append("Build on insights from our previous discussions to maintain strategic momentum")

        return suggestions

    def _extract_framework_integration(self, enhanced_response: EnhancedSystematicResponse) -> Dict[str, Any]:
        """Extract framework integration insights for enhanced response"""
        multi_analysis = enhanced_response.multi_framework_analysis

        integration_insights = {
            "primary_framework": {
                "name": multi_analysis.primary_framework.framework_name,
                "confidence": multi_analysis.primary_framework.analysis_confidence,
                "key_insights": multi_analysis.primary_framework.structured_insights
            },
            "supporting_frameworks": [
                {
                    "name": framework.framework_name,
                    "confidence": framework.analysis_confidence,
                    "unique_contribution": framework.structured_insights.get("unique_insights", [])
                }
                for framework in multi_analysis.supporting_frameworks
            ],
            "cross_framework_patterns": multi_analysis.cross_framework_patterns,
            "implementation_roadmap": multi_analysis.implementation_roadmap,
            "stakeholder_analysis": multi_analysis.stakeholder_considerations,
            "overall_confidence": multi_analysis.confidence_score,
            "context_relevance": multi_analysis.context_relevance
        }

        return integration_insights

    # Backwards compatibility methods
    def simple_persona_analysis(self, user_input: str, persona_name: str = "camille") -> str:
        """Simple persona analysis for backwards compatibility"""
        enhanced_response = self.analyze_with_enhanced_personas(user_input, requested_persona=persona_name)
        return enhanced_response.base_response

    def get_available_personas(self) -> List[str]:
        """Get list of available personas"""
        return list(self.persona_framework_affinity.keys())

    def get_persona_frameworks(self, persona_name: str) -> List[str]:
        """Get preferred frameworks for a persona"""
        return self.persona_framework_affinity.get(persona_name, [])


class ConversationIntelligenceEngine:
    """
    Phase 4.1: Complete Conversation Intelligence Engine

    Main entry point for enhanced conversation intelligence that combines
    multi-framework analysis, persona intelligence, and context awareness.

    Zero-setup, chat-only, backwards compatible.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.orchestrator = PersonaFrameworkOrchestrator(config)

        # Conversation intelligence settings
        self.intelligence_mode = self.config.get("intelligence_mode", "enhanced")  # enhanced, standard, auto
        self.context_retention = self.config.get("context_retention", True)
        self.collaborative_mode = self.config.get("collaborative_mode", True)

        logger.info("Conversation Intelligence Engine initialized",
                   intelligence_mode=self.intelligence_mode,
                   context_retention=self.context_retention,
                   collaborative_mode=self.collaborative_mode)

    def process_conversation(self, user_input: str, session_id: str = "default",
                           persona_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Main conversation processing method for Phase 4.1

        Returns comprehensive response with enhanced intelligence while maintaining
        backwards compatibility.
        """
        start_time = time.time()

        # Process with enhanced persona orchestration
        enhanced_response = self.orchestrator.analyze_with_enhanced_personas(
            user_input, session_id, persona_hint
        )

        # Format response for chat interface
        chat_response = self._format_for_chat_interface(enhanced_response, user_input)

        # Add processing metadata
        processing_time = int((time.time() - start_time) * 1000)

        response_package = {
            "response": chat_response["main_response"],
            "persona": enhanced_response.persona_name,
            "frameworks_used": enhanced_response.framework_integration["primary_framework"]["name"],
            "confidence": enhanced_response.confidence_score,
            "conversation_insights": chat_response["conversation_insights"],
            "collaborative_suggestions": enhanced_response.collaborative_suggestions,
            "processing_time_ms": processing_time,
            "session_id": session_id,
            "intelligence_mode": self.intelligence_mode
        }

        # Add optional enhancements if enabled
        if self.collaborative_mode and enhanced_response.collaborative_suggestions:
            response_package["collaboration_opportunities"] = enhanced_response.collaborative_suggestions

        if self.context_retention and enhanced_response.conversation_continuity:
            response_package["context_continuity"] = enhanced_response.conversation_continuity

        return response_package

    def _format_for_chat_interface(self, enhanced_response: EnhancedPersonaResponse,
                                 user_input: str) -> Dict[str, Any]:
        """Format enhanced response for natural chat interface"""

        # Main response combines persona response with key insights
        main_response = enhanced_response.base_response

        # Add framework insights if multiple frameworks were used
        supporting_frameworks = enhanced_response.framework_integration.get("supporting_frameworks", [])
        if supporting_frameworks:
            framework_names = [f["name"] for f in supporting_frameworks]
            main_response += f"\n\n*Drawing additional insights from {', '.join(framework_names[:2])} for comprehensive analysis.*"

        # Add conversation continuity notes naturally
        if enhanced_response.conversation_continuity:
            continuity_note = enhanced_response.conversation_continuity[0]
            main_response += f"\n\n*{continuity_note}*"

        # Conversation insights for optional display
        insights = {
            "confidence_level": "high" if enhanced_response.confidence_score > 0.8 else "medium" if enhanced_response.confidence_score > 0.6 else "moderate",
            "frameworks_applied": len(enhanced_response.framework_integration.get("supporting_frameworks", [])) + 1,
            "strategic_depth": "comprehensive" if len(enhanced_response.framework_integration.get("cross_framework_patterns", [])) > 2 else "focused"
        }

        return {
            "main_response": main_response,
            "conversation_insights": insights
        }

    # Backwards compatibility methods
    def simple_response(self, user_input: str, persona: str = "camille") -> str:
        """Simple response method for backwards compatibility"""
        result = self.process_conversation(user_input, persona_hint=persona)
        return result["response"]

    def get_conversation_stats(self, session_id: str) -> Dict[str, Any]:
        """Get conversation statistics for a session"""
        context = self.orchestrator.enhanced_engine.memory_engine.get_or_create_context(session_id)
        insights = self.orchestrator.enhanced_engine.memory_engine.get_context_insights(session_id)

        return {
            "conversation_length": len(context.conversation_history),
            "strategic_themes": list(context.strategic_themes),
            "frameworks_used": list(set(context.framework_usage_history)),
            "complexity_trend": insights["complexity_progression"]["trend"],
            "recurring_themes": insights["recurring_themes"][:3]
        }


# Export main intelligence engine for Phase 4 usage
__all__ = [
    "ConversationIntelligenceEngine",
    "PersonaFrameworkOrchestrator",
    "EnhancedPersonaResponse"
]
