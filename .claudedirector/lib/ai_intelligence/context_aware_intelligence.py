"""
Context-Aware Intelligence System

Phase 7 Strategic AI Development - Stream 1.2
Provides situational awareness and optimal framework selection based on context analysis.

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

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import logging
import time
import json

# Integration with existing ClaudeDirector architecture
try:
    from context_engineering.advanced_context_engine import AdvancedContextEngine
    from ai_intelligence.framework_detector import FrameworkDetector
    from ai_intelligence.mcp_decision_pipeline import MCPEnhancedDecisionPipeline
    from transparency.mcp_transparency_engine import MCPTransparencyEngine
    from ai_intelligence.predictive_analytics_engine import PredictiveAnalyticsEngine
except ImportError:
    # For test environments
    try:
        from ..context_engineering.advanced_context_engine import AdvancedContextEngine
        from ..ai_intelligence.framework_detector import FrameworkDetector
        from ..ai_intelligence.mcp_decision_pipeline import MCPEnhancedDecisionPipeline
        from ..transparency.mcp_transparency_engine import MCPTransparencyEngine
        from .predictive_analytics_engine import PredictiveAnalyticsEngine
    except ImportError:
        # Mock for testing if imports fail
        AdvancedContextEngine = object
        FrameworkDetector = object
        MCPEnhancedDecisionPipeline = object
        MCPTransparencyEngine = object
        PredictiveAnalyticsEngine = object


class ContextComplexity(Enum):
    """Strategic context complexity levels"""

    SIMPLE = "simple"  # Single domain, clear objectives
    MODERATE = "moderate"  # Multiple domains, some ambiguity
    COMPLEX = "complex"  # Cross-functional, high ambiguity
    ENTERPRISE = "enterprise"  # Multi-stakeholder, high stakes


class SituationalContext(Enum):
    """Types of strategic situations requiring different approaches"""

    CRISIS_RESPONSE = "crisis_response"
    STRATEGIC_PLANNING = "strategic_planning"
    TEAM_COORDINATION = "team_coordination"
    STAKEHOLDER_ALIGNMENT = "stakeholder_alignment"
    TECHNICAL_DECISION = "technical_decision"
    EXECUTIVE_COMMUNICATION = "executive_communication"
    PROCESS_OPTIMIZATION = "process_optimization"
    ORGANIZATIONAL_CHANGE = "organizational_change"


@dataclass
class ContextualFrameworkRecommendation:
    """Contextually optimized framework recommendation"""

    framework_name: str
    confidence_score: float  # 0.0 to 1.0
    relevance_score: float  # 0.0 to 1.0
    situational_fit: float  # 0.0 to 1.0

    # Context analysis
    context_complexity: ContextComplexity
    situational_context: SituationalContext
    stakeholder_involvement: List[str]
    time_sensitivity: str  # immediate, short_term, long_term

    # Application guidance
    key_focus_areas: List[str]
    adaptation_suggestions: List[str]
    success_metrics: List[str]

    # Performance metadata
    selection_timestamp: datetime
    analysis_duration_ms: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        result = asdict(self)
        result["context_complexity"] = self.context_complexity.value
        result["situational_context"] = self.situational_context.value
        result["selection_timestamp"] = self.selection_timestamp.isoformat()
        return result


@dataclass
class PersonaActivationRecommendation:
    """Optimal persona selection based on context"""

    recommended_persona: str
    activation_confidence: float  # 0.0 to 1.0
    context_alignment: float  # 0.0 to 1.0

    # Context factors
    domain_expertise_match: float
    stakeholder_preference_match: float
    communication_style_match: float

    # Coordination guidance
    supporting_personas: List[str]
    collaboration_strategy: str
    escalation_path: Optional[str]

    # Performance tracking
    selection_reasoning: List[str]
    alternative_personas: List[Dict[str, float]]


class ContextAwareIntelligence:
    """
    Situational awareness and optimal framework/persona selection system

    Provides dynamic adaptation based on strategic context analysis using
    ClaudeDirector's 8-layer Context Engineering architecture.

    Key Capabilities:
    - Situational context detection and classification
    - Optimal framework selection for specific contexts
    - Dynamic persona activation based on situation
    - Real-time adaptation to changing contexts
    - Integration with predictive analytics for proactive recommendations
    """

    def __init__(
        self,
        context_engine: AdvancedContextEngine,
        framework_detector: FrameworkDetector,
        mcp_pipeline: Optional[MCPEnhancedDecisionPipeline] = None,
        predictive_engine: Optional[PredictiveAnalyticsEngine] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize context-aware intelligence system"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Core dependencies
        self.context_engine = context_engine
        self.framework_detector = framework_detector
        self.mcp_pipeline = mcp_pipeline
        self.predictive_engine = predictive_engine

        # Configuration
        self.response_time_target_ms = self.config.get("response_time_target_ms", 200)
        self.relevance_threshold = self.config.get("relevance_threshold", 0.8)
        self.context_cache_duration_minutes = self.config.get("cache_duration", 15)

        # Persona expertise mapping
        self.persona_expertise = {
            "diego": {
                "domains": [
                    "engineering_leadership",
                    "platform_strategy",
                    "team_coordination",
                ],
                "situations": [
                    SituationalContext.TEAM_COORDINATION,
                    SituationalContext.STRATEGIC_PLANNING,
                ],
                "complexity_preference": [
                    ContextComplexity.COMPLEX,
                    ContextComplexity.ENTERPRISE,
                ],
                "communication_style": "direct_strategic",
            },
            "camille": {
                "domains": [
                    "strategic_technology",
                    "organizational_scaling",
                    "executive_advisory",
                ],
                "situations": [
                    SituationalContext.EXECUTIVE_COMMUNICATION,
                    SituationalContext.STRATEGIC_PLANNING,
                ],
                "complexity_preference": [
                    ContextComplexity.ENTERPRISE,
                    ContextComplexity.COMPLEX,
                ],
                "communication_style": "executive_strategic",
            },
            "rachel": {
                "domains": [
                    "design_systems",
                    "ux_leadership",
                    "cross_functional_alignment",
                ],
                "situations": [
                    SituationalContext.STAKEHOLDER_ALIGNMENT,
                    SituationalContext.PROCESS_OPTIMIZATION,
                ],
                "complexity_preference": [
                    ContextComplexity.MODERATE,
                    ContextComplexity.COMPLEX,
                ],
                "communication_style": "collaborative_design",
            },
            "alvaro": {
                "domains": [
                    "platform_investment",
                    "business_value",
                    "stakeholder_communication",
                ],
                "situations": [
                    SituationalContext.EXECUTIVE_COMMUNICATION,
                    SituationalContext.STRATEGIC_PLANNING,
                ],
                "complexity_preference": [
                    ContextComplexity.ENTERPRISE,
                    ContextComplexity.COMPLEX,
                ],
                "communication_style": "business_strategic",
            },
            "martin": {
                "domains": [
                    "platform_architecture",
                    "technical_strategy",
                    "evolutionary_design",
                ],
                "situations": [
                    SituationalContext.TECHNICAL_DECISION,
                    SituationalContext.ORGANIZATIONAL_CHANGE,
                ],
                "complexity_preference": [
                    ContextComplexity.COMPLEX,
                    ContextComplexity.MODERATE,
                ],
                "communication_style": "technical_strategic",
            },
        }

        # Framework situational mapping
        self.framework_situation_map = {
            SituationalContext.CRISIS_RESPONSE: [
                "Crucial Conversations",
                "WRAP Framework",
                "Team Topologies",
            ],
            SituationalContext.STRATEGIC_PLANNING: [
                "Good Strategy Bad Strategy",
                "Strategic Analysis Framework",
                "Capital Allocation Framework",
            ],
            SituationalContext.TEAM_COORDINATION: [
                "Team Topologies",
                "Scaling Up Excellence",
                "Organizational Design",
            ],
            SituationalContext.STAKEHOLDER_ALIGNMENT: [
                "Crucial Conversations",
                "Stakeholder Analysis",
                "Communication Strategy",
            ],
            SituationalContext.TECHNICAL_DECISION: [
                "Technical Strategy Framework",
                "ADR Patterns",
                "Evolutionary Architecture",
            ],
            SituationalContext.EXECUTIVE_COMMUNICATION: [
                "Strategic Analysis Framework",
                "Business Model Canvas",
                "Executive Communication",
            ],
        }

        # Context analysis cache
        self.context_cache: Dict[str, Dict[str, Any]] = {}
        self.last_cache_cleanup = datetime.now()

        self.logger.info(
            "ContextAwareIntelligence initialized with situational analysis capabilities"
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

            # Analyze query characteristics
            query_analysis = self._analyze_query_characteristics(query)

            # Determine situational context
            situational_context = self._classify_situational_context(
                query, query_analysis, layer_context
            )

            # Assess complexity level
            complexity_level = self._assess_context_complexity(
                query_analysis, layer_context, additional_context
            )

            # Identify stakeholders involved
            stakeholder_analysis = self._identify_involved_stakeholders(
                layer_context, query_analysis
            )

            # Determine time sensitivity
            time_sensitivity = self._assess_time_sensitivity(
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
                "layer_context_summary": self._summarize_layer_context(layer_context),
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
            return {
                "query": query,
                "situational_context": SituationalContext.STRATEGIC_PLANNING,
                "complexity_level": ContextComplexity.MODERATE,
                "stakeholder_analysis": {"primary": ["team_lead"], "secondary": []},
                "time_sensitivity": "short_term",
                "error": str(e),
                "analysis_timestamp": datetime.now(),
                "analysis_duration_ms": (time.time() - start_time) * 1000,
            }

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
            situational_context = context_analysis["situational_context"]
            complexity_level = context_analysis["complexity_level"]
            stakeholder_analysis = context_analysis["stakeholder_analysis"]

            # Get situational framework candidates
            framework_candidates = self.framework_situation_map.get(
                situational_context, ["Strategic Analysis Framework"]
            )

            # Use existing framework detector with context enhancement
            if self.framework_detector:
                detected_frameworks = await self._safe_async_call(
                    self.framework_detector.detect_frameworks, context_analysis["query"]
                )
            else:
                detected_frameworks = []

            # Score frameworks based on context fit
            framework_scores = {}
            for framework in framework_candidates:
                score = self._calculate_framework_context_fit(
                    framework,
                    situational_context,
                    complexity_level,
                    stakeholder_analysis,
                )
                framework_scores[framework] = score

            # Include detected frameworks with context scoring
            for detection in detected_frameworks:
                framework_name = detection.get("framework_name", "")
                if framework_name and framework_name not in framework_scores:
                    base_score = detection.get("confidence", 0.5)
                    context_score = self._calculate_framework_context_fit(
                        framework_name,
                        situational_context,
                        complexity_level,
                        stakeholder_analysis,
                    )
                    framework_scores[framework_name] = (base_score + context_score) / 2

            # Select best framework
            if framework_scores:
                best_framework = max(framework_scores.items(), key=lambda x: x[1])
                framework_name, confidence_score = best_framework
            else:
                framework_name = "Strategic Analysis Framework"
                confidence_score = 0.7

            # Generate contextual recommendation
            recommendation = ContextualFrameworkRecommendation(
                framework_name=framework_name,
                confidence_score=confidence_score,
                relevance_score=self._calculate_relevance_score(
                    framework_name, context_analysis
                ),
                situational_fit=self._calculate_situational_fit(
                    framework_name, situational_context
                ),
                context_complexity=complexity_level,
                situational_context=situational_context,
                stakeholder_involvement=stakeholder_analysis.get("primary", []),
                time_sensitivity=context_analysis["time_sensitivity"],
                key_focus_areas=self._identify_framework_focus_areas(
                    framework_name, context_analysis
                ),
                adaptation_suggestions=self._generate_framework_adaptations(
                    framework_name, context_analysis
                ),
                success_metrics=self._define_framework_success_metrics(
                    framework_name, situational_context
                ),
                selection_timestamp=datetime.now(),
                analysis_duration_ms=(time.time() - start_time) * 1000,
            )

            self.logger.info(
                f"Framework recommendation: {framework_name} "
                f"(confidence: {confidence_score:.2f}, "
                f"duration: {recommendation.analysis_duration_ms:.1f}ms)"
            )

            return recommendation

        except Exception as e:
            self.logger.error(f"Framework recommendation failed: {e}")
            # Return safe default recommendation
            return ContextualFrameworkRecommendation(
                framework_name="Strategic Analysis Framework",
                confidence_score=0.5,
                relevance_score=0.5,
                situational_fit=0.5,
                context_complexity=ContextComplexity.MODERATE,
                situational_context=SituationalContext.STRATEGIC_PLANNING,
                stakeholder_involvement=["team_lead"],
                time_sensitivity="short_term",
                key_focus_areas=["strategic_analysis"],
                adaptation_suggestions=["standard_application"],
                success_metrics=["framework_application_success"],
                selection_timestamp=datetime.now(),
                analysis_duration_ms=(time.time() - start_time) * 1000,
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
            situational_context = context_analysis["situational_context"]
            complexity_level = context_analysis["complexity_level"]
            stakeholder_analysis = context_analysis["stakeholder_analysis"]

            # Score personas based on context fit
            persona_scores = {}
            persona_details = {}

            for persona_name, persona_config in self.persona_expertise.items():
                # Calculate domain expertise match
                domain_match = self._calculate_domain_expertise_match(
                    persona_config, context_analysis
                )

                # Calculate situational context match
                situation_match = self._calculate_situational_match(
                    persona_config, situational_context
                )

                # Calculate complexity preference match
                complexity_match = self._calculate_complexity_match(
                    persona_config, complexity_level
                )

                # Calculate stakeholder preference match
                stakeholder_match = self._calculate_stakeholder_match(
                    persona_config, stakeholder_analysis
                )

                # Calculate composite score
                composite_score = (
                    domain_match * 0.3
                    + situation_match * 0.3
                    + complexity_match * 0.2
                    + stakeholder_match * 0.2
                )

                persona_scores[persona_name] = composite_score
                persona_details[persona_name] = {
                    "domain_match": domain_match,
                    "situation_match": situation_match,
                    "complexity_match": complexity_match,
                    "stakeholder_match": stakeholder_match,
                }

            # Select best persona
            if persona_scores:
                best_persona = max(persona_scores.items(), key=lambda x: x[1])
                recommended_persona, activation_confidence = best_persona
            else:
                recommended_persona = "diego"  # Default to diego
                activation_confidence = 0.5

            # Calculate context alignment
            persona_detail = persona_details.get(recommended_persona, {})
            context_alignment = (
                persona_detail.get("domain_match", 0.5)
                + persona_detail.get("situation_match", 0.5)
            ) / 2

            # Identify supporting personas
            supporting_personas = [
                persona
                for persona, score in persona_scores.items()
                if persona != recommended_persona and score > 0.6
            ]

            # Generate collaboration strategy
            collaboration_strategy = self._generate_collaboration_strategy(
                recommended_persona, supporting_personas, context_analysis
            )

            # Generate selection reasoning
            selection_reasoning = self._generate_persona_reasoning(
                recommended_persona, persona_detail, context_analysis
            )

            # Prepare alternative personas
            alternative_personas = [
                {"persona": persona, "score": score}
                for persona, score in sorted(
                    persona_scores.items(), key=lambda x: x[1], reverse=True
                )
                if persona != recommended_persona
            ][
                :3
            ]  # Top 3 alternatives

            recommendation = PersonaActivationRecommendation(
                recommended_persona=recommended_persona,
                activation_confidence=activation_confidence,
                context_alignment=context_alignment,
                domain_expertise_match=persona_detail.get("domain_match", 0.5),
                stakeholder_preference_match=persona_detail.get(
                    "stakeholder_match", 0.5
                ),
                communication_style_match=persona_detail.get("situation_match", 0.5),
                supporting_personas=supporting_personas,
                collaboration_strategy=collaboration_strategy,
                escalation_path=self._determine_escalation_path(
                    recommended_persona, complexity_level, stakeholder_analysis
                ),
                selection_reasoning=selection_reasoning,
                alternative_personas=alternative_personas,
            )

            analysis_duration = (time.time() - start_time) * 1000

            self.logger.info(
                f"Persona recommendation: {recommended_persona} "
                f"(confidence: {activation_confidence:.2f}, "
                f"duration: {analysis_duration:.1f}ms)"
            )

            return recommendation

        except Exception as e:
            self.logger.error(f"Persona recommendation failed: {e}")
            # Return safe default recommendation
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
            # Return minimal safe strategy
            return {
                "error": str(e),
                "fallback_strategy": {
                    "framework": "Strategic Analysis Framework",
                    "persona": "diego",
                    "approach": "standard_strategic_guidance",
                },
                "strategy_timestamp": datetime.now(),
            }

    # === PRIVATE HELPER METHODS ===

    async def _gather_layered_context(self, query: str) -> Dict[str, Any]:
        """Gather context from all 8 layers of Context Engineering"""
        layer_context = {}

        try:
            # Layer 1: Conversation Memory
            if hasattr(self.context_engine, "conversation_layer"):
                layer_context["conversation"] = await self._safe_async_call(
                    getattr(
                        self.context_engine.conversation_layer,
                        "get_conversation_context",
                        lambda x: {},
                    ),
                    query,
                )

            # Layer 2: Strategic Memory
            if hasattr(self.context_engine, "strategic_layer"):
                layer_context["strategic"] = await self._safe_async_call(
                    getattr(
                        self.context_engine.strategic_layer,
                        "get_strategic_context",
                        lambda x: {},
                    ),
                    query,
                )

            # Layer 3: Stakeholder Intelligence
            if hasattr(self.context_engine, "stakeholder_layer"):
                layer_context["stakeholder"] = await self._safe_async_call(
                    getattr(
                        self.context_engine.stakeholder_layer,
                        "get_stakeholder_context",
                        lambda x: {},
                    ),
                    query,
                )

            # Layer 4: Learning Patterns
            if hasattr(self.context_engine, "learning_layer"):
                layer_context["learning"] = await self._safe_async_call(
                    getattr(
                        self.context_engine.learning_layer,
                        "get_learning_context",
                        lambda x: {},
                    ),
                    query,
                )

            # Layer 5: Organizational Memory
            if hasattr(self.context_engine, "organizational_layer"):
                layer_context["organizational"] = await self._safe_async_call(
                    getattr(
                        self.context_engine.organizational_layer,
                        "get_organizational_context",
                        lambda x: {},
                    ),
                    query,
                )

            # Layers 6-8: Advanced engines if available
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

    def _analyze_query_characteristics(self, query: str) -> Dict[str, Any]:
        """Analyze query characteristics for context classification"""
        query_lower = query.lower()

        # Domain indicators
        domain_indicators = {
            "technical": ["architecture", "system", "code", "technical", "engineering"],
            "strategic": ["strategy", "planning", "roadmap", "vision", "goals"],
            "organizational": ["team", "people", "culture", "process", "organization"],
            "stakeholder": [
                "stakeholder",
                "communication",
                "alignment",
                "relationship",
            ],
            "executive": ["board", "vp", "executive", "leadership", "senior"],
        }

        domain_scores = {}
        for domain, indicators in domain_indicators.items():
            score = sum(1 for indicator in indicators if indicator in query_lower)
            domain_scores[domain] = score / len(indicators)

        # Complexity indicators
        complexity_indicators = {
            "multiple_teams": ["teams", "cross-functional", "multiple", "across"],
            "high_stakes": ["critical", "urgent", "important", "executive"],
            "ambiguity": ["unclear", "ambiguous", "complex", "challenging"],
            "scale": ["large", "enterprise", "organization-wide", "global"],
        }

        complexity_scores = {}
        for indicator_type, indicators in complexity_indicators.items():
            score = sum(1 for indicator in indicators if indicator in query_lower)
            complexity_scores[indicator_type] = score > 0

        # Urgency indicators
        urgency_indicators = ["urgent", "immediate", "asap", "quickly", "soon"]
        urgency_score = sum(
            1 for indicator in urgency_indicators if indicator in query_lower
        )

        return {
            "query_length": len(query.split()),
            "domain_scores": domain_scores,
            "complexity_indicators": complexity_scores,
            "urgency_score": urgency_score,
            "primary_domain": (
                max(domain_scores.items(), key=lambda x: x[1])[0]
                if domain_scores
                else "strategic"
            ),
            "estimated_complexity": sum(complexity_scores.values())
            / len(complexity_scores),
        }

    def _classify_situational_context(
        self, query: str, query_analysis: Dict[str, Any], layer_context: Dict[str, Any]
    ) -> SituationalContext:
        """Classify the situational context based on analysis"""

        query_lower = query.lower()
        primary_domain = query_analysis["primary_domain"]

        # Crisis indicators
        crisis_keywords = [
            "crisis",
            "urgent",
            "emergency",
            "critical",
            "failure",
            "down",
            "broken",
        ]
        if any(keyword in query_lower for keyword in crisis_keywords):
            return SituationalContext.CRISIS_RESPONSE

        # Executive communication indicators
        exec_keywords = ["present", "board", "vp", "executive", "leadership", "senior"]
        if any(keyword in query_lower for keyword in exec_keywords):
            return SituationalContext.EXECUTIVE_COMMUNICATION

        # Technical decision indicators
        tech_keywords = ["architecture", "technical", "code", "system", "engineering"]
        if primary_domain == "technical" or any(
            keyword in query_lower for keyword in tech_keywords
        ):
            return SituationalContext.TECHNICAL_DECISION

        # Team coordination indicators
        team_keywords = ["team", "coordination", "collaboration", "work together"]
        if any(keyword in query_lower for keyword in team_keywords):
            return SituationalContext.TEAM_COORDINATION

        # Stakeholder alignment indicators
        stakeholder_keywords = [
            "stakeholder",
            "alignment",
            "communication",
            "agreement",
        ]
        if any(keyword in query_lower for keyword in stakeholder_keywords):
            return SituationalContext.STAKEHOLDER_ALIGNMENT

        # Process optimization indicators
        process_keywords = ["process", "optimize", "improve", "efficiency", "workflow"]
        if any(keyword in query_lower for keyword in process_keywords):
            return SituationalContext.PROCESS_OPTIMIZATION

        # Organizational change indicators
        change_keywords = ["change", "transform", "restructure", "reorganize", "scale"]
        if any(keyword in query_lower for keyword in change_keywords):
            return SituationalContext.ORGANIZATIONAL_CHANGE

        # Default to strategic planning
        return SituationalContext.STRATEGIC_PLANNING

    def _assess_context_complexity(
        self,
        query_analysis: Dict[str, Any],
        layer_context: Dict[str, Any],
        additional_context: Optional[Dict[str, Any]],
    ) -> ContextComplexity:
        """Assess the complexity level of the strategic context"""

        complexity_score = 0

        # Query complexity
        if query_analysis["query_length"] > 20:
            complexity_score += 1

        # Multiple domain involvement
        domain_count = sum(
            1 for score in query_analysis["domain_scores"].values() if score > 0.3
        )
        if domain_count > 2:
            complexity_score += 1

        # Complexity indicators from query analysis
        complexity_indicators = query_analysis.get("complexity_indicators", {})
        complexity_score += sum(complexity_indicators.values())

        # Stakeholder complexity
        stakeholder_context = layer_context.get("stakeholder", {})
        if stakeholder_context.get("stakeholder_count", 0) > 3:
            complexity_score += 1

        # Strategic context complexity
        strategic_context = layer_context.get("strategic", {})
        if strategic_context.get("active_initiatives", 0) > 2:
            complexity_score += 1

        # Map score to complexity level
        if complexity_score >= 4:
            return ContextComplexity.ENTERPRISE
        elif complexity_score >= 3:
            return ContextComplexity.COMPLEX
        elif complexity_score >= 2:
            return ContextComplexity.MODERATE
        else:
            return ContextComplexity.SIMPLE

    def _identify_involved_stakeholders(
        self, layer_context: Dict[str, Any], query_analysis: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Identify stakeholders involved in the strategic context"""

        stakeholder_context = layer_context.get("stakeholder", {})
        primary_domain = query_analysis["primary_domain"]

        # Default stakeholder mapping based on domain
        domain_stakeholders = {
            "technical": ["tech_lead", "senior_engineers", "engineering_manager"],
            "strategic": ["engineering_director", "product_manager", "executive_team"],
            "organizational": ["engineering_manager", "hr_partner", "team_leads"],
            "stakeholder": ["product_manager", "design_lead", "business_stakeholders"],
            "executive": ["vp_engineering", "cto", "executive_team"],
        }

        primary_stakeholders = domain_stakeholders.get(
            primary_domain, ["engineering_manager"]
        )

        # Add stakeholders from context
        context_stakeholders = stakeholder_context.get("active_stakeholders", [])
        primary_stakeholders.extend(context_stakeholders)

        # Remove duplicates and organize
        primary_stakeholders = list(set(primary_stakeholders))

        return {
            "primary": primary_stakeholders[:3],  # Top 3 primary
            "secondary": primary_stakeholders[3:],  # Rest as secondary
            "total_count": len(primary_stakeholders),
        }

    def _assess_time_sensitivity(
        self,
        query: str,
        layer_context: Dict[str, Any],
        situational_context: SituationalContext,
    ) -> str:
        """Assess time sensitivity of the strategic context"""

        query_lower = query.lower()

        # Immediate indicators
        immediate_keywords = ["urgent", "asap", "immediately", "emergency", "critical"]
        if any(keyword in query_lower for keyword in immediate_keywords):
            return "immediate"

        # Short-term indicators
        short_term_keywords = [
            "soon",
            "quickly",
            "next week",
            "this sprint",
            "short term",
        ]
        if any(keyword in query_lower for keyword in short_term_keywords):
            return "short_term"

        # Long-term indicators
        long_term_keywords = [
            "roadmap",
            "vision",
            "long term",
            "next year",
            "strategic",
        ]
        if any(keyword in query_lower for keyword in long_term_keywords):
            return "long_term"

        # Situational defaults
        if situational_context == SituationalContext.CRISIS_RESPONSE:
            return "immediate"
        elif situational_context in [
            SituationalContext.TEAM_COORDINATION,
            SituationalContext.STAKEHOLDER_ALIGNMENT,
        ]:
            return "short_term"
        elif situational_context in [
            SituationalContext.STRATEGIC_PLANNING,
            SituationalContext.ORGANIZATIONAL_CHANGE,
        ]:
            return "long_term"

        return "short_term"  # Default

    def _summarize_layer_context(self, layer_context: Dict[str, Any]) -> Dict[str, str]:
        """Summarize layer context for strategic analysis"""
        summary = {}

        for layer_name, layer_data in layer_context.items():
            if layer_data:
                # Extract key insights from each layer
                if layer_name == "strategic":
                    summary[layer_name] = (
                        f"Active initiatives: {layer_data.get('active_initiatives', 0)}"
                    )
                elif layer_name == "stakeholder":
                    summary[layer_name] = (
                        f"Stakeholders: {layer_data.get('stakeholder_count', 0)}"
                    )
                elif layer_name == "organizational":
                    summary[layer_name] = (
                        f"Structure: {layer_data.get('structure_type', 'unknown')}"
                    )
                else:
                    summary[layer_name] = f"Data available: {len(layer_data)} fields"
            else:
                summary[layer_name] = "No data available"

        return summary

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

    # === FRAMEWORK RECOMMENDATION HELPERS ===

    def _calculate_framework_context_fit(
        self,
        framework_name: str,
        situational_context: SituationalContext,
        complexity_level: ContextComplexity,
        stakeholder_analysis: Dict[str, Any],
    ) -> float:
        """Calculate how well a framework fits the context"""

        # Base score from situational mapping
        situational_frameworks = self.framework_situation_map.get(
            situational_context, []
        )
        if framework_name in situational_frameworks:
            base_score = 0.8
        else:
            base_score = 0.4

        # Complexity adjustment
        complexity_bonus = {
            ContextComplexity.SIMPLE: 0.0,
            ContextComplexity.MODERATE: 0.1,
            ContextComplexity.COMPLEX: 0.15,
            ContextComplexity.ENTERPRISE: 0.2,
        }.get(complexity_level, 0.0)

        # Stakeholder count adjustment
        stakeholder_count = stakeholder_analysis.get("total_count", 1)
        if stakeholder_count > 3:
            stakeholder_bonus = 0.1
        else:
            stakeholder_bonus = 0.0

        return min(1.0, base_score + complexity_bonus + stakeholder_bonus)

    def _calculate_relevance_score(
        self, framework_name: str, context_analysis: Dict[str, Any]
    ) -> float:
        """Calculate framework relevance to specific context"""

        # Framework relevance mapping (simplified for Phase 7.1)
        framework_relevance = {
            "Team Topologies": {
                "domains": ["organizational", "technical"],
                "situations": [
                    SituationalContext.TEAM_COORDINATION,
                    SituationalContext.ORGANIZATIONAL_CHANGE,
                ],
            },
            "Good Strategy Bad Strategy": {
                "domains": ["strategic", "executive"],
                "situations": [
                    SituationalContext.STRATEGIC_PLANNING,
                    SituationalContext.EXECUTIVE_COMMUNICATION,
                ],
            },
            "Crucial Conversations": {
                "domains": ["stakeholder", "organizational"],
                "situations": [
                    SituationalContext.STAKEHOLDER_ALIGNMENT,
                    SituationalContext.CRISIS_RESPONSE,
                ],
            },
            "Strategic Analysis Framework": {
                "domains": ["strategic", "executive"],
                "situations": [
                    SituationalContext.STRATEGIC_PLANNING,
                    SituationalContext.EXECUTIVE_COMMUNICATION,
                ],
            },
        }

        framework_config = framework_relevance.get(framework_name, {})
        if not framework_config:
            return 0.5  # Default relevance

        # Domain match
        primary_domain = context_analysis.get("query_characteristics", {}).get(
            "primary_domain", "strategic"
        )
        relevant_domains = framework_config.get("domains", [])
        domain_match = 1.0 if primary_domain in relevant_domains else 0.3

        # Situation match
        situational_context = context_analysis.get("situational_context")
        relevant_situations = framework_config.get("situations", [])
        situation_match = 1.0 if situational_context in relevant_situations else 0.3

        return (domain_match + situation_match) / 2

    def _calculate_situational_fit(
        self, framework_name: str, situational_context: SituationalContext
    ) -> float:
        """Calculate how well framework fits the specific situation"""

        situational_frameworks = self.framework_situation_map.get(
            situational_context, []
        )
        if framework_name in situational_frameworks:
            # Get position in list (earlier = better fit)
            position = situational_frameworks.index(framework_name)
            return 1.0 - (position * 0.1)  # Decrease by 0.1 for each position

        return 0.5  # Default fit

    def _identify_framework_focus_areas(
        self, framework_name: str, context_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify key focus areas for framework application"""

        # Framework focus mapping
        framework_focus = {
            "Team Topologies": [
                "team_structure",
                "cognitive_load",
                "communication_patterns",
            ],
            "Good Strategy Bad Strategy": [
                "strategy_kernel",
                "strategic_objectives",
                "competitive_advantage",
            ],
            "Crucial Conversations": [
                "difficult_conversations",
                "stakeholder_alignment",
                "conflict_resolution",
            ],
            "Strategic Analysis Framework": [
                "situation_analysis",
                "strategic_options",
                "decision_criteria",
            ],
            "Capital Allocation Framework": [
                "resource_allocation",
                "investment_priorities",
                "roi_analysis",
            ],
        }

        default_focus = ["strategic_analysis", "framework_application"]
        return framework_focus.get(framework_name, default_focus)

    def _generate_framework_adaptations(
        self, framework_name: str, context_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate framework adaptation suggestions"""

        complexity_level = context_analysis.get(
            "complexity_level", ContextComplexity.MODERATE
        )
        time_sensitivity = context_analysis.get("time_sensitivity", "short_term")

        adaptations = []

        # Complexity-based adaptations
        if complexity_level == ContextComplexity.ENTERPRISE:
            adaptations.append(
                "Scale framework application across multiple stakeholder groups"
            )
            adaptations.append(
                "Include executive communication and change management elements"
            )
        elif complexity_level == ContextComplexity.SIMPLE:
            adaptations.append(
                "Simplify framework application for focused team context"
            )

        # Time-sensitive adaptations
        if time_sensitivity == "immediate":
            adaptations.append("Focus on immediate actionable elements of framework")
            adaptations.append("Defer comprehensive analysis for rapid decision making")
        elif time_sensitivity == "long_term":
            adaptations.append(
                "Include comprehensive strategic analysis and planning phases"
            )

        # Framework-specific adaptations
        if framework_name == "Team Topologies":
            adaptations.append(
                "Assess current team cognitive load and communication patterns"
            )
        elif framework_name == "Good Strategy Bad Strategy":
            adaptations.append("Develop clear strategy kernel with specific objectives")

        return adaptations or ["Apply framework systematically with context awareness"]

    def _define_framework_success_metrics(
        self, framework_name: str, situational_context: SituationalContext
    ) -> List[str]:
        """Define success metrics for framework application"""

        # Framework-specific metrics
        framework_metrics = {
            "Team Topologies": [
                "Reduced cross-team dependencies",
                "Improved team autonomy scores",
                "Decreased cognitive load indicators",
            ],
            "Good Strategy Bad Strategy": [
                "Clear strategic objectives defined",
                "Stakeholder alignment on strategy",
                "Measurable strategic progress",
            ],
            "Crucial Conversations": [
                "Successful difficult conversation outcomes",
                "Improved stakeholder relationships",
                "Reduced conflict incidents",
            ],
            "Strategic Analysis Framework": [
                "Comprehensive situation analysis completed",
                "Strategic options identified and evaluated",
                "Clear decision criteria established",
            ],
        }

        # Situational metrics
        situational_metrics = {
            SituationalContext.CRISIS_RESPONSE: [
                "Crisis resolution time",
                "Stakeholder confidence restoration",
            ],
            SituationalContext.TEAM_COORDINATION: [
                "Team collaboration effectiveness",
                "Communication frequency",
            ],
            SituationalContext.EXECUTIVE_COMMUNICATION: [
                "Executive understanding",
                "Decision clarity",
            ],
        }

        metrics = framework_metrics.get(
            framework_name, ["Framework application success"]
        )
        metrics.extend(situational_metrics.get(situational_context, []))

        return list(set(metrics))  # Remove duplicates

    # === PERSONA RECOMMENDATION HELPERS ===

    def _calculate_domain_expertise_match(
        self, persona_config: Dict[str, Any], context_analysis: Dict[str, Any]
    ) -> float:
        """Calculate domain expertise match for persona"""

        primary_domain = context_analysis.get("query_characteristics", {}).get(
            "primary_domain", "strategic"
        )
        persona_domains = persona_config.get("domains", [])

        # Direct domain match
        if any(domain in primary_domain for domain in persona_domains):
            return 1.0

        # Partial domain match
        domain_keywords = {
            "engineering_leadership": ["technical", "organizational"],
            "strategic_technology": ["strategic", "technical"],
            "design_systems": ["technical", "stakeholder"],
            "platform_investment": ["strategic", "executive"],
            "platform_architecture": ["technical"],
        }

        for persona_domain in persona_domains:
            keywords = domain_keywords.get(persona_domain, [])
            if primary_domain in keywords:
                return 0.7

        return 0.3  # Default low match

    def _calculate_situational_match(
        self, persona_config: Dict[str, Any], situational_context: SituationalContext
    ) -> float:
        """Calculate situational context match for persona"""

        persona_situations = persona_config.get("situations", [])

        if situational_context in persona_situations:
            return 1.0

        # Related situation matching
        situation_groups = {
            "strategic": [
                SituationalContext.STRATEGIC_PLANNING,
                SituationalContext.EXECUTIVE_COMMUNICATION,
            ],
            "operational": [
                SituationalContext.TEAM_COORDINATION,
                SituationalContext.PROCESS_OPTIMIZATION,
            ],
            "interpersonal": [
                SituationalContext.STAKEHOLDER_ALIGNMENT,
                SituationalContext.CRISIS_RESPONSE,
            ],
        }

        for group_name, situations in situation_groups.items():
            if situational_context in situations:
                # Check if persona has any situations in this group
                if any(sit in persona_situations for sit in situations):
                    return 0.7

        return 0.3  # Default low match

    def _calculate_complexity_match(
        self, persona_config: Dict[str, Any], complexity_level: ContextComplexity
    ) -> float:
        """Calculate complexity preference match for persona"""

        persona_complexity_prefs = persona_config.get("complexity_preference", [])

        if complexity_level in persona_complexity_prefs:
            return 1.0

        # Adjacent complexity matching
        complexity_order = [
            ContextComplexity.SIMPLE,
            ContextComplexity.MODERATE,
            ContextComplexity.COMPLEX,
            ContextComplexity.ENTERPRISE,
        ]
        current_index = complexity_order.index(complexity_level)

        for pref in persona_complexity_prefs:
            pref_index = complexity_order.index(pref)
            if abs(current_index - pref_index) == 1:
                return 0.7

        return 0.5  # Default neutral match

    def _calculate_stakeholder_match(
        self, persona_config: Dict[str, Any], stakeholder_analysis: Dict[str, Any]
    ) -> float:
        """Calculate stakeholder preference match for persona"""

        stakeholder_count = stakeholder_analysis.get("total_count", 1)
        primary_stakeholders = stakeholder_analysis.get("primary", [])

        # High-level stakeholder indicators
        executive_stakeholders = ["vp_engineering", "cto", "executive_team"]
        has_executives = any(
            stakeholder in executive_stakeholders
            for stakeholder in primary_stakeholders
        )

        # Persona preferences for stakeholder types
        if (
            persona_config.get("communication_style") == "executive_strategic"
            and has_executives
        ):
            return 1.0
        elif (
            persona_config.get("communication_style") == "technical_strategic"
            and stakeholder_count <= 3
        ):
            return 0.9
        elif (
            persona_config.get("communication_style") == "collaborative_design"
            and stakeholder_count > 2
        ):
            return 0.8

        return 0.6  # Default reasonable match

    def _generate_collaboration_strategy(
        self,
        primary_persona: str,
        supporting_personas: List[str],
        context_analysis: Dict[str, Any],
    ) -> str:
        """Generate collaboration strategy for multiple personas"""

        if not supporting_personas:
            return f"Single persona approach with {primary_persona} leading strategic guidance"

        complexity_level = context_analysis.get(
            "complexity_level", ContextComplexity.MODERATE
        )

        if complexity_level == ContextComplexity.ENTERPRISE:
            return f"{primary_persona} leads with coordinated input from {', '.join(supporting_personas)} for comprehensive multi-domain analysis"
        elif len(supporting_personas) == 1:
            return f"{primary_persona} leads with {supporting_personas[0]} providing specialized domain expertise"
        else:
            return f"{primary_persona} coordinates strategic approach with {', '.join(supporting_personas[:2])} providing complementary perspectives"

    def _generate_persona_reasoning(
        self,
        persona_name: str,
        persona_detail: Dict[str, Any],
        context_analysis: Dict[str, Any],
    ) -> List[str]:
        """Generate reasoning for persona selection"""

        reasoning = []

        # Domain expertise reasoning
        domain_match = persona_detail.get("domain_match", 0)
        if domain_match > 0.8:
            reasoning.append(
                f"Strong domain expertise match ({domain_match:.1f}) for strategic context"
            )

        # Situational reasoning
        situation_match = persona_detail.get("situation_match", 0)
        if situation_match > 0.8:
            reasoning.append(
                f"Optimal situational context fit ({situation_match:.1f}) for current scenario"
            )

        # Complexity reasoning
        complexity_match = persona_detail.get("complexity_match", 0)
        if complexity_match > 0.8:
            reasoning.append(
                f"Appropriate complexity handling capability ({complexity_match:.1f})"
            )

        # Context-specific reasoning
        situational_context = context_analysis.get("situational_context")
        if situational_context == SituationalContext.EXECUTIVE_COMMUNICATION:
            reasoning.append(
                "Executive communication expertise required for stakeholder context"
            )
        elif situational_context == SituationalContext.TEAM_COORDINATION:
            reasoning.append(
                "Team coordination and organizational design expertise needed"
            )

        return reasoning or [f"Selected {persona_name} as default strategic persona"]

    def _determine_escalation_path(
        self,
        primary_persona: str,
        complexity_level: ContextComplexity,
        stakeholder_analysis: Dict[str, Any],
    ) -> Optional[str]:
        """Determine escalation path if needed"""

        # Executive escalation for high complexity or executive stakeholders
        executive_stakeholders = ["vp_engineering", "cto", "executive_team"]
        primary_stakeholders = stakeholder_analysis.get("primary", [])
        has_executives = any(
            stakeholder in executive_stakeholders
            for stakeholder in primary_stakeholders
        )

        if complexity_level == ContextComplexity.ENTERPRISE or has_executives:
            if primary_persona not in ["camille", "alvaro"]:
                return "Escalate to Camille or Alvaro for executive-level strategic guidance"

        # Cross-functional escalation for complex coordination
        if (
            complexity_level == ContextComplexity.COMPLEX
            and primary_persona == "martin"
        ):
            return "Consider Diego for organizational coordination if technical solution requires team changes"

        return None

    # === MCP AND PREDICTIVE INTEGRATION HELPERS ===

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

        return {
            "communication_style": self.persona_expertise.get(
                persona_recommendation.recommended_persona, {}
            ).get("communication_style", "strategic"),
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
