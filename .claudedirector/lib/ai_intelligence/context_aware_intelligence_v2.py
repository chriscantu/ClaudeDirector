"""
Context-Aware Intelligence System - Refactored Modular Version

Phase 7 Strategic AI Development - Stream 1.2
Lightweight orchestration of specialized context analysis components.

Performance Targets:
- <200ms framework selection response time
- >95% context relevance accuracy
- Dynamic persona activation based on situation
- Seamless integration with existing MCP coordination

Architecture Integration:
- Integrates with existing Framework Detection system
- Enhances MCP Decision Pipeline with context awareness
- Uses 8-layer Context Engineering for situational analysis
- Provides real-time adaptation to changing strategic contexts
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import time

# Integration with existing ClaudeDirector architecture
try:
    from context_engineering.advanced_context_engine import AdvancedContextEngine
    from ai_intelligence.framework_detector import FrameworkDetector
    from ai_intelligence.mcp_decision_pipeline import MCPEnhancedDecisionPipeline
    from ai_intelligence.predictive_analytics_engine_v2 import PredictiveAnalyticsEngine
except ImportError:
    try:
        from ..context_engineering.advanced_context_engine import AdvancedContextEngine
        from ..ai_intelligence.framework_detector import FrameworkDetector
        from ..ai_intelligence.mcp_decision_pipeline import MCPEnhancedDecisionPipeline
        from .predictive_analytics_engine_v2 import PredictiveAnalyticsEngine
    except ImportError:
        # Mock for testing if imports fail
        AdvancedContextEngine = object
        FrameworkDetector = object
        MCPEnhancedDecisionPipeline = object
        PredictiveAnalyticsEngine = object

# Import specialized components
from .context.context_analyzer import (
    ContextAnalyzer,
    ContextComplexity,
    SituationalContext,
)
from .context.framework_selector import (
    FrameworkSelector,
    ContextualFrameworkRecommendation,
)
from .context.persona_selector import PersonaSelector, PersonaActivationRecommendation


class ContextAwareIntelligence:
    """
    Lightweight orchestration engine for context-aware intelligence

    Coordinates specialized components for context analysis, framework
    selection, and persona recommendation.
    """

    def __init__(
        self,
        context_engine: AdvancedContextEngine,
        framework_detector: FrameworkDetector,
        mcp_pipeline: Optional[MCPEnhancedDecisionPipeline] = None,
        predictive_engine: Optional[PredictiveAnalyticsEngine] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize context-aware intelligence system with modular components"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Core dependencies
        self.context_engine = context_engine
        self.framework_detector = framework_detector
        self.mcp_pipeline = mcp_pipeline
        self.predictive_engine = predictive_engine

        # Initialize specialized components
        self.context_analyzer = ContextAnalyzer(self.config)
        self.framework_selector = FrameworkSelector(self.config)
        self.persona_selector = PersonaSelector(self.config)

        # Configuration
        self.response_time_target_ms = self.config.get("response_time_target_ms", 200)
        self.relevance_threshold = self.config.get("relevance_threshold", 0.8)
        self.context_cache_duration_minutes = self.config.get("cache_duration", 15)

        # Context analysis cache
        self.context_cache: Dict[str, Dict[str, Any]] = {}
        self.last_cache_cleanup = datetime.now()

        self.logger.info(
            "ContextAwareIntelligence initialized with modular architecture"
        )

    async def analyze_strategic_context(
        self, query: str, additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze strategic context to determine situation and complexity

        Args:
            query: Strategic question or request
            additional_context: Optional additional context information

        Returns:
            Comprehensive context analysis including complexity and situation
        """
        start_time = time.time()

        try:
            # Check cache first
            cache_key = f"context_{hash(query)}"
            if cache_key in self.context_cache:
                cached_result = self.context_cache[cache_key]
                if (
                    datetime.now() - cached_result["timestamp"]
                ).total_seconds() < 900:  # 15 minutes
                    return cached_result["analysis"]

            # Gather comprehensive context from 8-layer architecture
            layer_context = await self._gather_layered_context(query)

            # Analyze query characteristics using specialized analyzer
            query_analysis = self.context_analyzer.analyze_query_characteristics(query)

            # Determine situational context
            situational_context = self.context_analyzer.classify_situational_context(
                query, query_analysis, layer_context
            )

            # Assess complexity level
            complexity_level = self.context_analyzer.assess_context_complexity(
                query_analysis, layer_context, additional_context
            )

            # Identify stakeholders involved
            stakeholder_analysis = self.context_analyzer.identify_involved_stakeholders(
                layer_context, query_analysis
            )

            # Determine time sensitivity
            time_sensitivity = self.context_analyzer.assess_time_sensitivity(
                query, layer_context, situational_context
            )

            # Compile strategic context analysis
            context_analysis = {
                "query": query,
                "situational_context": situational_context,
                "complexity_level": complexity_level,
                "stakeholder_analysis": stakeholder_analysis,
                "time_sensitivity": time_sensitivity,
                "query_characteristics": query_analysis,
                "layer_context_summary": self.context_analyzer.summarize_layer_context(
                    layer_context
                ),
                "analysis_timestamp": datetime.now(),
                "analysis_duration_ms": (time.time() - start_time) * 1000,
            }

            # Cache the analysis
            self.context_cache[cache_key] = {
                "analysis": context_analysis,
                "timestamp": datetime.now(),
            }

            # Cleanup old cache entries periodically
            await self._cleanup_context_cache()

            self.logger.info(
                f"Strategic context analyzed: {situational_context.value}, "
                f"complexity: {complexity_level.value}, "
                f"duration: {context_analysis['analysis_duration_ms']:.1f}ms"
            )

            return context_analysis

        except Exception as e:
            self.logger.error(f"Context analysis failed: {e}")
            # Return safe default analysis
            return self._get_default_context_analysis(query, start_time)

    async def recommend_optimal_framework(
        self, context_analysis: Dict[str, Any]
    ) -> ContextualFrameworkRecommendation:
        """
        Recommend optimal framework based on strategic context analysis

        Args:
            context_analysis: Result from analyze_strategic_context

        Returns:
            Contextually optimized framework recommendation
        """
        start_time = time.time()

        try:
            # Use existing framework detector with context enhancement
            framework_detector_results = []
            if self.framework_detector:
                detected_frameworks = await self._safe_async_call(
                    self.framework_detector.detect_frameworks, context_analysis["query"]
                )
                framework_detector_results = detected_frameworks or []

            # Get framework recommendation from specialized selector
            recommendation = self.framework_selector.recommend_optimal_framework(
                context_analysis, framework_detector_results
            )

            # Update timing
            recommendation.analysis_duration_ms = (time.time() - start_time) * 1000

            self.logger.info(
                f"Framework recommendation: {recommendation.framework_name} "
                f"(confidence: {recommendation.confidence_score:.2f}, "
                f"duration: {recommendation.analysis_duration_ms:.1f}ms)"
            )

            return recommendation

        except Exception as e:
            self.logger.error(f"Framework recommendation failed: {e}")
            return self._get_default_framework_recommendation(
                context_analysis, start_time
            )

    async def recommend_optimal_persona(
        self, context_analysis: Dict[str, Any]
    ) -> PersonaActivationRecommendation:
        """
        Recommend optimal persona activation based on context analysis

        Args:
            context_analysis: Result from analyze_strategic_context

        Returns:
            Optimal persona activation recommendation
        """
        start_time = time.time()

        try:
            # Get persona recommendation from specialized selector
            recommendation = self.persona_selector.recommend_optimal_persona(
                context_analysis
            )

            analysis_duration = (time.time() - start_time) * 1000

            self.logger.info(
                f"Persona recommendation: {recommendation.recommended_persona} "
                f"(confidence: {recommendation.activation_confidence:.2f}, "
                f"duration: {analysis_duration:.1f}ms)"
            )

            return recommendation

        except Exception as e:
            self.logger.error(f"Persona recommendation failed: {e}")
            return self._get_default_persona_recommendation()

    async def generate_adaptive_response_strategy(
        self,
        context_analysis: Dict[str, Any],
        framework_recommendation: ContextualFrameworkRecommendation,
        persona_recommendation: PersonaActivationRecommendation,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive adaptive response strategy

        Args:
            context_analysis: Strategic context analysis
            framework_recommendation: Optimal framework recommendation
            persona_recommendation: Optimal persona recommendation

        Returns:
            Comprehensive response strategy with all adaptive elements
        """
        start_time = time.time()

        try:
            # Generate MCP enhancement strategy if available
            mcp_strategy = None
            if self.mcp_pipeline:
                mcp_strategy = await self._generate_mcp_enhancement_strategy(
                    context_analysis, framework_recommendation
                )

            # Generate predictive insights if available
            predictive_insights = None
            if self.predictive_engine:
                predictive_insights = await self._generate_predictive_insights(
                    context_analysis
                )

            # Compile comprehensive strategy
            response_strategy = {
                "context_analysis": context_analysis,
                "framework_strategy": {
                    "primary_framework": framework_recommendation.framework_name,
                    "confidence": framework_recommendation.confidence_score,
                    "focus_areas": framework_recommendation.key_focus_areas,
                    "adaptations": framework_recommendation.adaptation_suggestions,
                    "success_metrics": framework_recommendation.success_metrics,
                },
                "persona_strategy": {
                    "primary_persona": persona_recommendation.recommended_persona,
                    "confidence": persona_recommendation.activation_confidence,
                    "supporting_personas": persona_recommendation.supporting_personas,
                    "collaboration_strategy": persona_recommendation.collaboration_strategy,
                    "escalation_path": persona_recommendation.escalation_path,
                },
                "mcp_enhancement": mcp_strategy,
                "predictive_insights": predictive_insights,
                "response_guidance": self._generate_response_guidance(
                    context_analysis, framework_recommendation, persona_recommendation
                ),
                "adaptation_triggers": self._identify_adaptation_triggers(
                    context_analysis
                ),
                "performance_metrics": {
                    "total_analysis_time_ms": (time.time() - start_time) * 1000,
                    "context_analysis_time_ms": context_analysis.get(
                        "analysis_duration_ms", 0
                    ),
                    "framework_selection_time_ms": framework_recommendation.analysis_duration_ms,
                    "persona_selection_time_ms": 0,  # PersonaActivationRecommendation doesn't have duration
                },
                "strategy_timestamp": datetime.now(),
            }

            self.logger.info(
                f"Adaptive response strategy generated: "
                f"framework={framework_recommendation.framework_name}, "
                f"persona={persona_recommendation.recommended_persona}, "
                f"duration={response_strategy['performance_metrics']['total_analysis_time_ms']:.1f}ms"
            )

            return response_strategy

        except Exception as e:
            self.logger.error(f"Response strategy generation failed: {e}")
            return self._get_default_response_strategy(e)

    # === PRIVATE HELPER METHODS ===

    async def _gather_layered_context(self, query: str) -> Dict[str, Any]:
        """Gather context from all 8 layers of Context Engineering"""
        layer_context = {}

        try:
            # Simplified layer context gathering
            for layer_name in [
                "conversation",
                "strategic",
                "stakeholder",
                "learning",
                "organizational",
            ]:
                if hasattr(self.context_engine, f"{layer_name}_layer"):
                    layer = getattr(self.context_engine, f"{layer_name}_layer")
                    context_method = getattr(
                        layer, f"get_{layer_name}_context", lambda x: {}
                    )
                    layer_context[layer_name] = await self._safe_async_call(
                        context_method, query
                    )

            # Advanced engines if available
            if hasattr(self.context_engine, "team_dynamics_engine"):
                layer_context["team_dynamics"] = await self._safe_async_call(
                    getattr(
                        self.context_engine.team_dynamics_engine,
                        "get_current_dynamics",
                        lambda: {},
                    )
                )

        except Exception as e:
            self.logger.warning(f"Layer context gathering partial failure: {e}")

        return layer_context

    async def _safe_async_call(self, func, *args, **kwargs):
        """Safely call async or sync function"""
        try:
            if hasattr(func, "__call__"):
                result = func(*args, **kwargs)
                # If it's a coroutine, await it
                if hasattr(result, "__await__"):
                    return await result
                return result
            return {}
        except Exception as e:
            self.logger.warning(f"Safe async call failed: {e}")
            return {}

    async def _cleanup_context_cache(self):
        """Clean up old cache entries"""
        now = datetime.now()
        if (now - self.last_cache_cleanup).total_seconds() > 3600:  # Cleanup every hour
            expired_keys = [
                key
                for key, value in self.context_cache.items()
                if (now - value["timestamp"]).total_seconds() > 3600  # 1 hour expiry
            ]

            for key in expired_keys:
                del self.context_cache[key]

            self.last_cache_cleanup = now

            if expired_keys:
                self.logger.info(
                    f"Cleaned up {len(expired_keys)} expired cache entries"
                )

    async def _generate_mcp_enhancement_strategy(
        self,
        context_analysis: Dict[str, Any],
        framework_recommendation: ContextualFrameworkRecommendation,
    ) -> Optional[Dict[str, Any]]:
        """Generate MCP enhancement strategy if applicable"""

        if not self.mcp_pipeline:
            return None

        complexity_level = context_analysis.get(
            "complexity_level", ContextComplexity.MODERATE
        )

        # Determine if MCP enhancement is beneficial
        if complexity_level in [
            ContextComplexity.COMPLEX,
            ContextComplexity.ENTERPRISE,
        ]:
            return {
                "recommend_enhancement": True,
                "suggested_servers": ["sequential", "context7"],
                "enhancement_rationale": "Complex strategic context benefits from systematic analysis and pattern access",
                "transparency_disclosure": "MCP enhancement will be disclosed for systematic strategic analysis",
            }

        return {
            "recommend_enhancement": False,
            "rationale": "Standard persona response sufficient for current complexity level",
        }

    async def _generate_predictive_insights(
        self, context_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Generate predictive insights if predictive engine available"""

        if not self.predictive_engine:
            return None

        try:
            # Get quick health assessment
            health_metrics = (
                await self.predictive_engine.get_organizational_health_metrics()
            )

            return {
                "health_score": health_metrics.overall_health_score,
                "key_risks": health_metrics.burnout_risk_indicators[:3],
                "recommendation": "Include predictive health context in strategic guidance",
            }
        except Exception as e:
            self.logger.warning(f"Predictive insights generation failed: {e}")
            return None

    def _generate_response_guidance(
        self,
        context_analysis: Dict[str, Any],
        framework_recommendation: ContextualFrameworkRecommendation,
        persona_recommendation: PersonaActivationRecommendation,
    ) -> Dict[str, Any]:
        """Generate comprehensive response guidance"""

        persona_config = self.persona_selector.persona_expertise.get(
            persona_recommendation.recommended_persona, {}
        )

        return {
            "communication_style": persona_config.get(
                "communication_style", "strategic"
            ),
            "key_message_priorities": [
                f"Apply {framework_recommendation.framework_name} methodology",
                f"Address {context_analysis['situational_context'].value.replace('_', ' ')} context",
                "Provide actionable strategic guidance",
            ],
            "stakeholder_considerations": context_analysis.get(
                "stakeholder_analysis", {}
            ).get("primary", []),
            "time_sensitivity_note": f"Time sensitivity: {context_analysis.get('time_sensitivity', 'moderate')}",
            "complexity_adaptations": framework_recommendation.adaptation_suggestions,
        }

    def _identify_adaptation_triggers(
        self, context_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify triggers that would require strategy adaptation"""

        triggers = []

        complexity_level = context_analysis.get("complexity_level")
        if complexity_level == ContextComplexity.ENTERPRISE:
            triggers.append("Executive stakeholder involvement changes")
            triggers.append("Multi-team coordination requirements")

        situational_context = context_analysis.get("situational_context")
        if situational_context == SituationalContext.CRISIS_RESPONSE:
            triggers.append("Crisis escalation or resolution")
            triggers.append("Emergency stakeholder communication needs")

        time_sensitivity = context_analysis.get("time_sensitivity")
        if time_sensitivity == "immediate":
            triggers.append("Urgent timeline changes")
            triggers.append("Immediate decision requirements")

        return triggers or [
            "Significant context changes",
            "Stakeholder feedback",
            "Timeline modifications",
        ]

    def _get_default_context_analysis(
        self, query: str, start_time: float
    ) -> Dict[str, Any]:
        """Return safe default context analysis on error"""
        return {
            "query": query,
            "situational_context": SituationalContext.STRATEGIC_PLANNING,
            "complexity_level": ContextComplexity.MODERATE,
            "stakeholder_analysis": {"primary": ["team_lead"], "secondary": []},
            "time_sensitivity": "short_term",
            "error": "Context analysis failed - using defaults",
            "analysis_timestamp": datetime.now(),
            "analysis_duration_ms": (time.time() - start_time) * 1000,
        }

    def _get_default_framework_recommendation(
        self, context_analysis: Dict[str, Any], start_time: float
    ) -> ContextualFrameworkRecommendation:
        """Return safe default framework recommendation on error"""
        return ContextualFrameworkRecommendation(
            framework_name="Strategic Analysis Framework",
            confidence_score=0.5,
            relevance_score=0.5,
            situational_fit=0.5,
            context_complexity=context_analysis.get(
                "complexity_level", ContextComplexity.MODERATE
            ),
            situational_context=context_analysis.get(
                "situational_context", SituationalContext.STRATEGIC_PLANNING
            ),
            stakeholder_involvement=["team_lead"],
            time_sensitivity="short_term",
            key_focus_areas=["strategic_analysis"],
            adaptation_suggestions=["standard_application"],
            success_metrics=["framework_application_success"],
            selection_timestamp=datetime.now(),
            analysis_duration_ms=(time.time() - start_time) * 1000,
        )

    def _get_default_persona_recommendation(self) -> PersonaActivationRecommendation:
        """Return safe default persona recommendation on error"""
        return PersonaActivationRecommendation(
            recommended_persona="diego",
            activation_confidence=0.5,
            context_alignment=0.5,
            domain_expertise_match=0.5,
            stakeholder_preference_match=0.5,
            communication_style_match=0.5,
            supporting_personas=[],
            collaboration_strategy="standard_strategic_guidance",
            escalation_path=None,
            selection_reasoning=["default_engineering_leadership_persona"],
            alternative_personas=[],
        )

    def _get_default_response_strategy(self, error: Exception) -> Dict[str, Any]:
        """Return minimal safe strategy on error"""
        return {
            "error": str(error),
            "fallback_strategy": {
                "framework": "Strategic Analysis Framework",
                "persona": "diego",
                "approach": "standard_strategic_guidance",
            },
            "strategy_timestamp": datetime.now(),
        }
