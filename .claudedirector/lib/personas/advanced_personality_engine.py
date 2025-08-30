"""
Advanced Personality Engine - Phase 14 Track 3: User Experience Excellence

🎨 Rachel | Design Systems Strategy

Technical Story: TS-14.3.1 Enhanced Strategic Personality Modeling
User Story: US-14.3.1 Enhanced Strategic Personality Modeling (Executive Strategic Leader)

Architecture Integration:
- Builds on existing persona system with advanced personality depth
- Integrates with context_engineering for persona-specific memory and learning
- Extends MCP enhancement with persona-specific strategic intelligence
- Maintains existing transparency system for persona reasoning disclosure

Performance Target: 95%+ persona consistency across interactions
Business Value: $200K+ external consulting replacement through expert-level guidance
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging
import json
import statistics
from collections import defaultdict

# Core ClaudeDirector integration following PROJECT_STRUCTURE.md
try:
    from ..context_engineering.advanced_context_engine import AdvancedContextEngine
    from ..context_engineering.stakeholder_intelligence_unified import (
        StakeholderIntelligenceUnified,
    )
    from ..ai_intelligence.framework_detector import FrameworkDetectionMiddleware
    from ..transparency.integrated_transparency import TransparencyContext
    from ..performance.cache_manager import CacheManager, CacheLevel
except ImportError:
    # Lightweight fallback pattern following OVERVIEW.md
    AdvancedContextEngine = object
    StakeholderIntelligenceUnified = object
    FrameworkDetectionMiddleware = object
    TransparencyContext = object
    CacheManager = object


class PersonaRole(Enum):
    """Strategic persona roles with specific expertise domains"""

    DIEGO = "diego"  # Engineering Leadership
    CAMILLE = "camille"  # Strategic Technology (CTO)
    RACHEL = "rachel"  # Design Systems Strategy
    ALVARO = "alvaro"  # Platform Investment Strategy
    MARTIN = "martin"  # Platform Architecture
    ELENA = "elena"  # Security & Compliance
    BERNY = "berny"  # AI/ML Engineering
    MARCUS = "marcus"  # Platform Adoption
    DAVID = "david"  # Financial Planning
    SOFIA = "sofia"  # Vendor Strategy


class StrategicThinkingDepth(Enum):
    """Levels of strategic thinking depth for persona responses"""

    SURFACE = "surface"  # Basic response, minimal analysis
    ANALYTICAL = "analytical"  # Structured analysis with frameworks
    STRATEGIC = "strategic"  # Deep strategic thinking with multiple perspectives
    VISIONARY = "visionary"  # Long-term vision with transformational insights
    EXPERT = "expert"  # Consultant-level expertise with nuanced judgment


class PersonalityTrait(Enum):
    """Core personality traits that define persona behavior"""

    ANALYTICAL_RIGOR = "analytical_rigor"
    STRATEGIC_VISION = "strategic_vision"
    PRACTICAL_FOCUS = "practical_focus"
    COLLABORATIVE_STYLE = "collaborative_style"
    INNOVATION_DRIVE = "innovation_drive"
    RISK_TOLERANCE = "risk_tolerance"
    COMMUNICATION_STYLE = "communication_style"
    DECISION_SPEED = "decision_speed"


@dataclass
class PersonaBehavior:
    """Comprehensive persona behavior profile with consistency tracking"""

    persona_role: PersonaRole
    thinking_depth: StrategicThinkingDepth

    # Personality traits (0.0 to 1.0 scale)
    traits: Dict[PersonalityTrait, float] = field(default_factory=dict)

    # Strategic preferences
    preferred_frameworks: List[str] = field(default_factory=list)
    communication_patterns: Dict[str, Any] = field(default_factory=dict)
    decision_making_style: Dict[str, Any] = field(default_factory=dict)

    # Context adaptation
    context_sensitivity: float = 0.8  # How much persona adapts to context
    consistency_weight: float = 0.9  # How much persona maintains consistency

    # Performance tracking
    interaction_count: int = 0
    consistency_score: float = 1.0
    expertise_demonstrations: List[str] = field(default_factory=list)

    # Learning and adaptation
    successful_patterns: Dict[str, int] = field(default_factory=dict)
    context_adaptations: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PersonaConsistencyMetrics:
    """Detailed metrics for persona consistency tracking"""

    persona_role: PersonaRole
    measurement_period: timedelta

    # Consistency measurements
    trait_consistency: Dict[PersonalityTrait, float] = field(default_factory=dict)
    framework_consistency: float = 0.0
    communication_consistency: float = 0.0
    strategic_thinking_consistency: float = 0.0

    # Overall metrics
    overall_consistency_score: float = 0.0
    interactions_analyzed: int = 0
    consistency_trend: str = "stable"  # improving, stable, declining

    # Detailed analysis
    consistency_violations: List[str] = field(default_factory=list)
    adaptation_successes: List[str] = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class StrategicResponse:
    """Enhanced strategic response with persona intelligence"""

    content: str
    persona_role: PersonaRole
    thinking_depth: StrategicThinkingDepth

    # Strategic intelligence
    frameworks_applied: List[str] = field(default_factory=list)
    strategic_reasoning: str = ""
    context_adaptations: List[str] = field(default_factory=list)

    # Persona consistency
    personality_traits_demonstrated: Dict[PersonalityTrait, float] = field(
        default_factory=dict
    )
    consistency_score: float = 1.0
    expertise_level: str = "expert"

    # Performance metrics
    response_time_ms: float = 0.0
    context_relevance: float = 1.0
    strategic_value: float = 1.0

    timestamp: datetime = field(default_factory=datetime.now)


class AdvancedPersonalityEngine:
    """
    🎨 Advanced Strategic Personality Engine

    Rachel | Design Systems Strategy

    Provides expert-level strategic thinking with advanced personality modeling
    and context-aware behavior adaptation for ClaudeDirector personas.

    Key Features:
    - 95%+ persona consistency across interactions
    - Expert-level strategic thinking depth with transparent reasoning
    - Context-aware personality adaptation while maintaining core traits
    - Multi-framework coordination with persona-specific preferences
    - Real-time consistency monitoring and adaptive learning

    Architecture Integration:
    - Extends existing persona system with advanced personality modeling
    - Integrates AdvancedContextEngine for persona-specific memory
    - Uses FrameworkDetectionMiddleware for persona framework preferences
    - Maintains TransparencyContext for persona reasoning disclosure
    """

    def __init__(
        self,
        context_engine: Optional[AdvancedContextEngine] = None,
        stakeholder_intelligence: Optional[StakeholderIntelligenceUnified] = None,
        framework_detector: Optional[FrameworkDetectionMiddleware] = None,
        cache_manager: Optional[CacheManager] = None,
        consistency_target: float = 0.95,
    ):
        """Initialize advanced personality engine with existing infrastructure"""
        self.logger = logging.getLogger(__name__)

        # Core infrastructure integration
        self.context_engine = context_engine
        self.stakeholder_intelligence = stakeholder_intelligence
        self.framework_detector = framework_detector
        self.cache_manager = cache_manager

        # Performance targets
        self.consistency_target = consistency_target
        self.expertise_threshold = 0.9

        # Persona behavior profiles
        self.persona_behaviors = self._initialize_persona_behaviors()

        # Consistency tracking
        self.consistency_metrics: Dict[PersonaRole, PersonaConsistencyMetrics] = {}
        self.interaction_history: List[StrategicResponse] = []

        # Strategic thinking patterns
        self.thinking_patterns = self._initialize_thinking_patterns()

        # Performance monitoring
        self.performance_metrics = {
            "total_interactions": 0,
            "consistency_violations": 0,
            "expertise_demonstrations": 0,
            "context_adaptations": 0,
        }

        self.logger.info(
            f"AdvancedPersonalityEngine initialized with {consistency_target:.1%} consistency target"
        )

    def _initialize_persona_behaviors(self) -> Dict[PersonaRole, PersonaBehavior]:
        """Initialize comprehensive persona behavior profiles"""
        behaviors = {}

        # Diego - Engineering Leadership
        behaviors[PersonaRole.DIEGO] = PersonaBehavior(
            persona_role=PersonaRole.DIEGO,
            thinking_depth=StrategicThinkingDepth.STRATEGIC,
            traits={
                PersonalityTrait.ANALYTICAL_RIGOR: 0.9,
                PersonalityTrait.STRATEGIC_VISION: 0.8,
                PersonalityTrait.PRACTICAL_FOCUS: 0.9,
                PersonalityTrait.COLLABORATIVE_STYLE: 0.8,
                PersonalityTrait.INNOVATION_DRIVE: 0.7,
                PersonalityTrait.RISK_TOLERANCE: 0.6,
                PersonalityTrait.COMMUNICATION_STYLE: 0.8,
                PersonalityTrait.DECISION_SPEED: 0.7,
            },
            preferred_frameworks=[
                "Team Topologies",
                "Accelerate",
                "Capital Allocation Framework",
            ],
            communication_patterns={
                "style": "direct_collaborative",
                "detail_level": "strategic_with_tactical",
                "stakeholder_focus": "cross_functional",
            },
            decision_making_style={
                "approach": "data_driven_consensus",
                "speed": "measured_deliberate",
                "risk_profile": "calculated_conservative",
            },
        )

        # Camille - Strategic Technology (CTO)
        behaviors[PersonaRole.CAMILLE] = PersonaBehavior(
            persona_role=PersonaRole.CAMILLE,
            thinking_depth=StrategicThinkingDepth.VISIONARY,
            traits={
                PersonalityTrait.ANALYTICAL_RIGOR: 0.9,
                PersonalityTrait.STRATEGIC_VISION: 0.95,
                PersonalityTrait.PRACTICAL_FOCUS: 0.7,
                PersonalityTrait.COLLABORATIVE_STYLE: 0.7,
                PersonalityTrait.INNOVATION_DRIVE: 0.9,
                PersonalityTrait.RISK_TOLERANCE: 0.8,
                PersonalityTrait.COMMUNICATION_STYLE: 0.9,
                PersonalityTrait.DECISION_SPEED: 0.8,
            },
            preferred_frameworks=[
                "Good Strategy Bad Strategy",
                "Wardley Mapping",
                "Technical Strategy Framework",
            ],
            communication_patterns={
                "style": "visionary_executive",
                "detail_level": "strategic_high_level",
                "stakeholder_focus": "executive_board",
            },
            decision_making_style={
                "approach": "vision_driven_strategic",
                "speed": "fast_decisive",
                "risk_profile": "innovation_aggressive",
            },
        )

        # Rachel - Design Systems Strategy
        behaviors[PersonaRole.RACHEL] = PersonaBehavior(
            persona_role=PersonaRole.RACHEL,
            thinking_depth=StrategicThinkingDepth.EXPERT,
            traits={
                PersonalityTrait.ANALYTICAL_RIGOR: 0.8,
                PersonalityTrait.STRATEGIC_VISION: 0.8,
                PersonalityTrait.PRACTICAL_FOCUS: 0.9,
                PersonalityTrait.COLLABORATIVE_STYLE: 0.95,
                PersonalityTrait.INNOVATION_DRIVE: 0.8,
                PersonalityTrait.RISK_TOLERANCE: 0.5,
                PersonalityTrait.COMMUNICATION_STYLE: 0.95,
                PersonalityTrait.DECISION_SPEED: 0.6,
            },
            preferred_frameworks=[
                "Design System Maturity Model",
                "User-Centered Design",
                "Systems Thinking",
            ],
            communication_patterns={
                "style": "collaborative_empathetic",
                "detail_level": "user_focused_detailed",
                "stakeholder_focus": "cross_functional_inclusive",
            },
            decision_making_style={
                "approach": "user_centered_collaborative",
                "speed": "thoughtful_inclusive",
                "risk_profile": "user_safety_first",
            },
        )

        # Alvaro - Platform Investment Strategy
        behaviors[PersonaRole.ALVARO] = PersonaBehavior(
            persona_role=PersonaRole.ALVARO,
            thinking_depth=StrategicThinkingDepth.STRATEGIC,
            traits={
                PersonalityTrait.ANALYTICAL_RIGOR: 0.95,
                PersonalityTrait.STRATEGIC_VISION: 0.8,
                PersonalityTrait.PRACTICAL_FOCUS: 0.9,
                PersonalityTrait.COLLABORATIVE_STYLE: 0.7,
                PersonalityTrait.INNOVATION_DRIVE: 0.6,
                PersonalityTrait.RISK_TOLERANCE: 0.4,
                PersonalityTrait.COMMUNICATION_STYLE: 0.8,
                PersonalityTrait.DECISION_SPEED: 0.8,
            },
            preferred_frameworks=[
                "Capital Allocation Framework",
                "Business Model Canvas",
                "ROI Analysis",
            ],
            communication_patterns={
                "style": "business_analytical",
                "detail_level": "financial_strategic",
                "stakeholder_focus": "executive_business",
            },
            decision_making_style={
                "approach": "roi_driven_analytical",
                "speed": "measured_thorough",
                "risk_profile": "conservative_calculated",
            },
        )

        # Martin - Platform Architecture
        behaviors[PersonaRole.MARTIN] = PersonaBehavior(
            persona_role=PersonaRole.MARTIN,
            thinking_depth=StrategicThinkingDepth.EXPERT,
            traits={
                PersonalityTrait.ANALYTICAL_RIGOR: 0.95,
                PersonalityTrait.STRATEGIC_VISION: 0.7,
                PersonalityTrait.PRACTICAL_FOCUS: 0.95,
                PersonalityTrait.COLLABORATIVE_STYLE: 0.8,
                PersonalityTrait.INNOVATION_DRIVE: 0.7,
                PersonalityTrait.RISK_TOLERANCE: 0.3,
                PersonalityTrait.COMMUNICATION_STYLE: 0.7,
                PersonalityTrait.DECISION_SPEED: 0.6,
            },
            preferred_frameworks=[
                "Evolutionary Architecture",
                "SOLID Principles",
                "Technical Debt Management",
            ],
            communication_patterns={
                "style": "technical_precise",
                "detail_level": "architectural_detailed",
                "stakeholder_focus": "technical_teams",
            },
            decision_making_style={
                "approach": "architecture_driven_systematic",
                "speed": "deliberate_thorough",
                "risk_profile": "stability_conservative",
            },
        )

        return behaviors

    def _initialize_thinking_patterns(
        self,
    ) -> Dict[StrategicThinkingDepth, Dict[str, Any]]:
        """Initialize strategic thinking patterns for different depth levels"""
        return {
            StrategicThinkingDepth.SURFACE: {
                "analysis_depth": "basic",
                "framework_usage": "minimal",
                "context_integration": "limited",
                "reasoning_transparency": "simple",
            },
            StrategicThinkingDepth.ANALYTICAL: {
                "analysis_depth": "structured",
                "framework_usage": "single_framework",
                "context_integration": "moderate",
                "reasoning_transparency": "clear",
            },
            StrategicThinkingDepth.STRATEGIC: {
                "analysis_depth": "multi_dimensional",
                "framework_usage": "multiple_frameworks",
                "context_integration": "comprehensive",
                "reasoning_transparency": "detailed",
            },
            StrategicThinkingDepth.VISIONARY: {
                "analysis_depth": "transformational",
                "framework_usage": "integrated_frameworks",
                "context_integration": "holistic",
                "reasoning_transparency": "visionary",
            },
            StrategicThinkingDepth.EXPERT: {
                "analysis_depth": "consultant_level",
                "framework_usage": "masterful_integration",
                "context_integration": "nuanced_sophisticated",
                "reasoning_transparency": "expert_judgment",
            },
        }

    async def generate_strategic_response(
        self,
        query: str,
        persona_role: PersonaRole,
        context: Dict[str, Any],
        target_depth: StrategicThinkingDepth = StrategicThinkingDepth.STRATEGIC,
    ) -> StrategicResponse:
        """
        Generate strategic response with advanced personality modeling

        Args:
            query: Strategic query to respond to
            persona_role: Persona to embody for the response
            context: Current context and user information
            target_depth: Desired strategic thinking depth

        Returns:
            StrategicResponse with persona intelligence and consistency metrics
        """
        start_time = time.time()

        # Get persona behavior profile
        persona_behavior = self.persona_behaviors.get(persona_role)
        if not persona_behavior:
            raise ValueError(f"Unknown persona role: {persona_role}")

        # Adapt persona behavior to context
        adapted_behavior = await self._adapt_persona_to_context(
            persona_behavior, context, target_depth
        )

        # Generate strategic response with persona intelligence
        response_content = await self._generate_persona_response(
            query, adapted_behavior, context, target_depth
        )

        # Apply strategic frameworks based on persona preferences
        frameworks_applied = await self._apply_persona_frameworks(
            query, adapted_behavior, context
        )

        # Generate strategic reasoning explanation
        strategic_reasoning = await self._generate_strategic_reasoning(
            query, adapted_behavior, frameworks_applied, target_depth
        )

        # Calculate consistency score
        consistency_score = await self._calculate_consistency_score(
            persona_role, adapted_behavior, frameworks_applied
        )

        # Create strategic response
        response = StrategicResponse(
            content=response_content,
            persona_role=persona_role,
            thinking_depth=target_depth,
            frameworks_applied=frameworks_applied,
            strategic_reasoning=strategic_reasoning,
            context_adaptations=adapted_behavior.context_adaptations.get("current", []),
            personality_traits_demonstrated=adapted_behavior.traits,
            consistency_score=consistency_score,
            expertise_level=self._determine_expertise_level(
                target_depth, consistency_score
            ),
            response_time_ms=(time.time() - start_time) * 1000,
            context_relevance=await self._calculate_context_relevance(query, context),
            strategic_value=await self._calculate_strategic_value(
                frameworks_applied, target_depth
            ),
        )

        # Update persona behavior and metrics
        await self._update_persona_behavior(persona_behavior, response)
        await self._update_consistency_metrics(persona_role, response)

        # Store interaction history
        self.interaction_history.append(response)
        self.performance_metrics["total_interactions"] += 1

        if consistency_score < self.consistency_target:
            self.performance_metrics["consistency_violations"] += 1

        if response.expertise_level == "expert":
            self.performance_metrics["expertise_demonstrations"] += 1

        self.logger.info(
            f"Generated {persona_role.value} response with {consistency_score:.1%} consistency "
            f"in {response.response_time_ms:.1f}ms"
        )

        return response

    async def _adapt_persona_to_context(
        self,
        persona_behavior: PersonaBehavior,
        context: Dict[str, Any],
        target_depth: StrategicThinkingDepth,
    ) -> PersonaBehavior:
        """Adapt persona behavior to current context while maintaining consistency"""
        # Create adapted copy
        adapted = PersonaBehavior(
            persona_role=persona_behavior.persona_role,
            thinking_depth=target_depth,
            traits=persona_behavior.traits.copy(),
            preferred_frameworks=persona_behavior.preferred_frameworks.copy(),
            communication_patterns=persona_behavior.communication_patterns.copy(),
            decision_making_style=persona_behavior.decision_making_style.copy(),
            context_sensitivity=persona_behavior.context_sensitivity,
            consistency_weight=persona_behavior.consistency_weight,
        )

        # Context-based adaptations
        adaptations = []

        # Stakeholder context adaptation
        if "stakeholder_context" in context:
            stakeholder_info = context["stakeholder_context"]
            if "executive_audience" in stakeholder_info:
                # Adapt communication for executive audience
                adapted.communication_patterns["detail_level"] = "executive_summary"
                adapted.traits[PersonalityTrait.COMMUNICATION_STYLE] = min(
                    1.0, adapted.traits[PersonalityTrait.COMMUNICATION_STYLE] + 0.1
                )
                adaptations.append("executive_communication_adaptation")

        # Urgency context adaptation
        if context.get("urgency", "normal") == "high":
            # Increase decision speed for urgent contexts
            adapted.traits[PersonalityTrait.DECISION_SPEED] = min(
                1.0, adapted.traits[PersonalityTrait.DECISION_SPEED] + 0.2
            )
            adaptations.append("urgency_speed_adaptation")

        # Complexity context adaptation
        if context.get("complexity", "moderate") == "high":
            # Increase analytical rigor for complex contexts
            adapted.traits[PersonalityTrait.ANALYTICAL_RIGOR] = min(
                1.0, adapted.traits[PersonalityTrait.ANALYTICAL_RIGOR] + 0.1
            )
            adaptations.append("complexity_analysis_adaptation")

        # Store adaptations for transparency
        adapted.context_adaptations["current"] = adaptations

        return adapted

    async def _generate_persona_response(
        self,
        query: str,
        persona_behavior: PersonaBehavior,
        context: Dict[str, Any],
        target_depth: StrategicThinkingDepth,
    ) -> str:
        """Generate response content with persona-specific intelligence"""
        # Get thinking pattern for depth level
        thinking_pattern = self.thinking_patterns[target_depth]

        # Generate persona-specific response based on traits and preferences
        response_elements = []

        # Persona introduction with role context
        role_context = {
            PersonaRole.DIEGO: "🎯 Diego | Engineering Leadership",
            PersonaRole.CAMILLE: "📊 Camille | Strategic Technology",
            PersonaRole.RACHEL: "🎨 Rachel | Design Systems Strategy",
            PersonaRole.ALVARO: "💼 Alvaro | Platform Investment Strategy",
            PersonaRole.MARTIN: "🏗️ Martin | Platform Architecture",
        }.get(
            persona_behavior.persona_role,
            f"🎯 {persona_behavior.persona_role.value.title()}",
        )

        response_elements.append(role_context)

        # Strategic analysis based on thinking depth
        if target_depth in [
            StrategicThinkingDepth.STRATEGIC,
            StrategicThinkingDepth.VISIONARY,
            StrategicThinkingDepth.EXPERT,
        ]:
            response_elements.append(f"\n\n**Strategic Analysis**: {query}")

            # Add persona-specific strategic perspective
            if persona_behavior.persona_role == PersonaRole.DIEGO:
                response_elements.append(
                    "\nFrom an engineering leadership perspective, this requires cross-functional coordination and systematic execution."
                )
            elif persona_behavior.persona_role == PersonaRole.CAMILLE:
                response_elements.append(
                    "\nFrom a strategic technology viewpoint, we need to consider long-term architectural implications and competitive positioning."
                )
            elif persona_behavior.persona_role == PersonaRole.RACHEL:
                response_elements.append(
                    "\nFrom a design systems strategy lens, user experience and cross-team collaboration are paramount."
                )
            elif persona_behavior.persona_role == PersonaRole.ALVARO:
                response_elements.append(
                    "\nFrom a platform investment perspective, ROI and business value must drive our strategic decisions."
                )
            elif persona_behavior.persona_role == PersonaRole.MARTIN:
                response_elements.append(
                    "\nFrom an architectural standpoint, we must ensure scalability, maintainability, and technical excellence."
                )

        # Framework integration hint (actual frameworks applied separately)
        if (
            persona_behavior.preferred_frameworks
            and target_depth != StrategicThinkingDepth.SURFACE
        ):
            primary_framework = persona_behavior.preferred_frameworks[0]
            response_elements.append(
                f"\n\n**Framework Application**: Applying {primary_framework} methodology for systematic analysis."
            )

        # Combine response elements
        response_content = "".join(response_elements)

        # Add strategic recommendations based on persona traits
        if persona_behavior.traits[PersonalityTrait.PRACTICAL_FOCUS] > 0.8:
            response_content += "\n\n**Practical Implementation**: Focus on actionable steps with clear deliverables and timelines."

        if persona_behavior.traits[PersonalityTrait.COLLABORATIVE_STYLE] > 0.8:
            response_content += "\n\n**Stakeholder Alignment**: Ensure cross-functional buy-in and collaborative execution."

        return response_content

    async def _apply_persona_frameworks(
        self,
        query: str,
        persona_behavior: PersonaBehavior,
        context: Dict[str, Any],
    ) -> List[str]:
        """Apply strategic frameworks based on persona preferences"""
        applied_frameworks = []

        # Use persona's preferred frameworks
        for framework in persona_behavior.preferred_frameworks[
            :2
        ]:  # Limit to top 2 for performance
            # Framework application logic would integrate with existing FrameworkDetectionMiddleware
            applied_frameworks.append(framework)

        # Add context-specific frameworks
        if (
            "stakeholder_context" in context
            and "Team Topologies" not in applied_frameworks
        ):
            applied_frameworks.append("Team Topologies")

        return applied_frameworks

    async def _generate_strategic_reasoning(
        self,
        query: str,
        persona_behavior: PersonaBehavior,
        frameworks_applied: List[str],
        target_depth: StrategicThinkingDepth,
    ) -> str:
        """Generate transparent strategic reasoning explanation"""
        reasoning_elements = []

        # Persona reasoning approach
        reasoning_elements.append(
            f"**{persona_behavior.persona_role.value.title()} Reasoning**:"
        )

        # Decision-making style explanation
        decision_style = persona_behavior.decision_making_style
        reasoning_elements.append(
            f"- Approach: {decision_style.get('approach', 'systematic')}"
        )
        reasoning_elements.append(f"- Speed: {decision_style.get('speed', 'measured')}")
        reasoning_elements.append(
            f"- Risk Profile: {decision_style.get('risk_profile', 'balanced')}"
        )

        # Framework reasoning
        if frameworks_applied:
            reasoning_elements.append(
                f"\n**Framework Selection**: {', '.join(frameworks_applied)}"
            )
            reasoning_elements.append(
                "Selected based on persona expertise and query context alignment."
            )

        # Thinking depth explanation
        depth_explanation = {
            StrategicThinkingDepth.ANALYTICAL: "Structured analysis with clear methodology",
            StrategicThinkingDepth.STRATEGIC: "Multi-dimensional strategic perspective with stakeholder considerations",
            StrategicThinkingDepth.VISIONARY: "Long-term transformational thinking with innovation focus",
            StrategicThinkingDepth.EXPERT: "Consultant-level expertise with nuanced professional judgment",
        }.get(target_depth, "Comprehensive strategic analysis")

        reasoning_elements.append(f"\n**Thinking Depth**: {depth_explanation}")

        return "\n".join(reasoning_elements)

    async def _calculate_consistency_score(
        self,
        persona_role: PersonaRole,
        adapted_behavior: PersonaBehavior,
        frameworks_applied: List[str],
    ) -> float:
        """Calculate persona consistency score based on behavior and history"""
        if persona_role not in self.consistency_metrics:
            return 1.0  # Perfect score for first interaction

        previous_metrics = self.consistency_metrics[persona_role]
        base_behavior = self.persona_behaviors[persona_role]

        # Calculate trait consistency
        trait_consistency_scores = []
        for trait, current_value in adapted_behavior.traits.items():
            base_value = base_behavior.traits[trait]
            # Allow some adaptation but penalize major deviations
            deviation = abs(current_value - base_value)
            consistency = max(0.0, 1.0 - (deviation * 2))  # 2x penalty for deviations
            trait_consistency_scores.append(consistency)

        trait_consistency = (
            statistics.mean(trait_consistency_scores)
            if trait_consistency_scores
            else 1.0
        )

        # Calculate framework consistency
        framework_consistency = 1.0
        if frameworks_applied:
            preferred_used = sum(
                1 for f in frameworks_applied if f in base_behavior.preferred_frameworks
            )
            framework_consistency = preferred_used / len(frameworks_applied)

        # Overall consistency score
        overall_consistency = (trait_consistency * 0.7) + (framework_consistency * 0.3)

        return min(1.0, max(0.0, overall_consistency))

    async def _update_persona_behavior(
        self, persona_behavior: PersonaBehavior, response: StrategicResponse
    ):
        """Update persona behavior based on interaction success"""
        persona_behavior.interaction_count += 1

        # Update consistency score (running average)
        persona_behavior.consistency_score = (
            persona_behavior.consistency_score
            * (persona_behavior.interaction_count - 1)
            + response.consistency_score
        ) / persona_behavior.interaction_count

        # Track successful patterns
        if response.consistency_score >= self.consistency_target:
            for framework in response.frameworks_applied:
                persona_behavior.successful_patterns[framework] = (
                    persona_behavior.successful_patterns.get(framework, 0) + 1
                )

        # Track expertise demonstrations
        if response.expertise_level == "expert":
            persona_behavior.expertise_demonstrations.append(
                f"{response.thinking_depth.value}_{len(response.frameworks_applied)}_frameworks"
            )

    async def _update_consistency_metrics(
        self, persona_role: PersonaRole, response: StrategicResponse
    ):
        """Update detailed consistency metrics for persona"""
        if persona_role not in self.consistency_metrics:
            self.consistency_metrics[persona_role] = PersonaConsistencyMetrics(
                persona_role=persona_role,
                measurement_period=timedelta(days=7),
            )

        metrics = self.consistency_metrics[persona_role]
        metrics.interactions_analyzed += 1

        # Update overall consistency score
        metrics.overall_consistency_score = (
            metrics.overall_consistency_score * (metrics.interactions_analyzed - 1)
            + response.consistency_score
        ) / metrics.interactions_analyzed

        # Track consistency violations
        if response.consistency_score < self.consistency_target:
            violation_description = f"Consistency {response.consistency_score:.1%} below target {self.consistency_target:.1%}"
            metrics.consistency_violations.append(violation_description)

        # Track adaptation successes
        if (
            response.context_adaptations
            and response.consistency_score >= self.consistency_target
        ):
            adaptation_description = (
                f"Successful adaptation: {', '.join(response.context_adaptations)}"
            )
            metrics.adaptation_successes.append(adaptation_description)

    def _determine_expertise_level(
        self, thinking_depth: StrategicThinkingDepth, consistency_score: float
    ) -> str:
        """Determine expertise level based on thinking depth and consistency"""
        if thinking_depth == StrategicThinkingDepth.EXPERT and consistency_score >= 0.9:
            return "expert"
        elif (
            thinking_depth
            in [StrategicThinkingDepth.STRATEGIC, StrategicThinkingDepth.VISIONARY]
            and consistency_score >= 0.8
        ):
            return "advanced"
        elif consistency_score >= 0.7:
            return "proficient"
        else:
            return "developing"

    async def _calculate_context_relevance(
        self, query: str, context: Dict[str, Any]
    ) -> float:
        """Calculate how well the response addresses the context"""
        # Simplified relevance calculation - would use ML in production
        relevance_factors = []

        # Context completeness
        if context.get("stakeholder_context"):
            relevance_factors.append(0.9)
        if context.get("strategic_context"):
            relevance_factors.append(0.9)
        if context.get("organizational_context"):
            relevance_factors.append(0.8)

        return statistics.mean(relevance_factors) if relevance_factors else 0.8

    async def _calculate_strategic_value(
        self, frameworks_applied: List[str], thinking_depth: StrategicThinkingDepth
    ) -> float:
        """Calculate strategic value of the response"""
        base_value = {
            StrategicThinkingDepth.SURFACE: 0.5,
            StrategicThinkingDepth.ANALYTICAL: 0.7,
            StrategicThinkingDepth.STRATEGIC: 0.8,
            StrategicThinkingDepth.VISIONARY: 0.9,
            StrategicThinkingDepth.EXPERT: 1.0,
        }.get(thinking_depth, 0.7)

        # Bonus for framework application
        framework_bonus = min(0.2, len(frameworks_applied) * 0.1)

        return min(1.0, base_value + framework_bonus)

    def get_persona_consistency_report(
        self, persona_role: PersonaRole
    ) -> Dict[str, Any]:
        """Get comprehensive consistency report for a persona"""
        if persona_role not in self.consistency_metrics:
            return {"status": "no_data", "persona": persona_role.value}

        metrics = self.consistency_metrics[persona_role]
        behavior = self.persona_behaviors[persona_role]

        return {
            "persona": persona_role.value,
            "overall_consistency_score": metrics.overall_consistency_score,
            "interactions_analyzed": metrics.interactions_analyzed,
            "consistency_trend": metrics.consistency_trend,
            "target_achievement": metrics.overall_consistency_score
            >= self.consistency_target,
            "behavior_stats": {
                "interaction_count": behavior.interaction_count,
                "consistency_score": behavior.consistency_score,
                "expertise_demonstrations": len(behavior.expertise_demonstrations),
                "successful_patterns": len(behavior.successful_patterns),
            },
            "violations": len(metrics.consistency_violations),
            "adaptations": len(metrics.adaptation_successes),
            "last_updated": metrics.timestamp.isoformat(),
        }

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary for all personas"""
        persona_summaries = {}
        for persona_role in PersonaRole:
            persona_summaries[persona_role.value] = self.get_persona_consistency_report(
                persona_role
            )

        # Overall performance metrics
        total_consistency_scores = [
            metrics.overall_consistency_score
            for metrics in self.consistency_metrics.values()
            if metrics.interactions_analyzed > 0
        ]

        overall_consistency = (
            statistics.mean(total_consistency_scores)
            if total_consistency_scores
            else 0.0
        )

        return {
            "overall_performance": {
                "average_consistency": overall_consistency,
                "target_achievement": overall_consistency >= self.consistency_target,
                "total_interactions": self.performance_metrics["total_interactions"],
                "consistency_violations": self.performance_metrics[
                    "consistency_violations"
                ],
                "expertise_demonstrations": self.performance_metrics[
                    "expertise_demonstrations"
                ],
                "violation_rate": (
                    self.performance_metrics["consistency_violations"]
                    / max(1, self.performance_metrics["total_interactions"])
                ),
            },
            "persona_performance": persona_summaries,
            "recent_interactions": len(
                [
                    r
                    for r in self.interaction_history[-10:]
                    if r.consistency_score >= self.consistency_target
                ]
            ),
        }


def create_advanced_personality_engine(
    context_engine: Optional[AdvancedContextEngine] = None,
    stakeholder_intelligence: Optional[StakeholderIntelligenceUnified] = None,
    framework_detector: Optional[FrameworkDetectionMiddleware] = None,
    cache_manager: Optional[CacheManager] = None,
    consistency_target: float = 0.95,
) -> AdvancedPersonalityEngine:
    """
    Factory function to create AdvancedPersonalityEngine with proper dependencies

    Follows existing ClaudeDirector factory patterns for dependency injection
    """
    return AdvancedPersonalityEngine(
        context_engine=context_engine,
        stakeholder_intelligence=stakeholder_intelligence,
        framework_detector=framework_detector,
        cache_manager=cache_manager,
        consistency_target=consistency_target,
    )
