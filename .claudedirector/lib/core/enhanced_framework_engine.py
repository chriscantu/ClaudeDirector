"""
Phase 4.1: Enhanced Strategic Framework Engine
Multi-framework integration with context awareness and conversation memory.

Backwards Compatible Enhancement of existing embedded_framework_engine.py
Zero-setup, chat-only, conversation-native intelligence.

Author: Martin (Phase 4 Implementation)
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from collections import defaultdict, Counter
import structlog

# Import existing framework engine for backwards compatibility
from .embedded_framework_engine import (
    EmbeddedFrameworkEngine,
    FrameworkAnalysis,
    SystematicResponse,
)

# Configure logging
logger = structlog.get_logger(__name__)


@dataclass
class ConversationContext:
    """Represents conversation context for enhanced framework selection"""

    session_id: str
    previous_topics: List[str] = field(default_factory=list)
    strategic_themes: Set[str] = field(default_factory=set)
    stakeholder_mentions: Set[str] = field(default_factory=set)
    domain_focus: Optional[str] = None
    complexity_level: str = "medium"  # low, medium, high
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    framework_usage_history: List[str] = field(default_factory=list)


@dataclass
class MultiFrameworkAnalysis:
    """Result of enhanced multi-framework analysis"""

    primary_framework: FrameworkAnalysis
    supporting_frameworks: List[FrameworkAnalysis]
    integrated_insights: Dict[str, Any]
    cross_framework_patterns: List[str]
    comprehensive_recommendations: List[str]
    implementation_roadmap: Dict[str, List[str]]
    stakeholder_considerations: Dict[str, List[str]]
    confidence_score: float
    context_relevance: float


@dataclass
class EnhancedSystematicResponse:
    """Complete enhanced systematic analysis response with context awareness"""

    multi_framework_analysis: MultiFrameworkAnalysis
    persona_integrated_response: str
    context_aware_recommendations: List[str]
    conversation_continuity_notes: List[str]
    processing_time_ms: int
    frameworks_applied: List[str]
    learning_insights: Dict[str, Any]


class ConversationMemoryEngine:
    """Manages conversation context and learning across sessions"""

    def __init__(self):
        self.session_contexts: Dict[str, ConversationContext] = {}
        self.global_patterns: Dict[str, int] = defaultdict(int)
        self.framework_effectiveness: Dict[str, List[float]] = defaultdict(list)
        self.topic_framework_mapping: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )

    def get_or_create_context(self, session_id: str) -> ConversationContext:
        """Get existing or create new conversation context"""
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = ConversationContext(
                session_id=session_id
            )
        return self.session_contexts[session_id]

    def update_context(
        self,
        session_id: str,
        user_input: str,
        topics: List[str],
        frameworks_used: List[str],
    ) -> ConversationContext:
        """Update conversation context with new information"""
        context = self.get_or_create_context(session_id)

        # Update conversation history
        context.conversation_history.append(
            {
                "input": user_input,
                "timestamp": time.time(),
                "topics": topics,
                "frameworks": frameworks_used,
            }
        )

        # Update topics and themes
        context.previous_topics.extend(topics)
        context.strategic_themes.update(topics)
        context.framework_usage_history.extend(frameworks_used)

        # Learn patterns for future recommendations
        for topic in topics:
            for framework in frameworks_used:
                self.topic_framework_mapping[topic][framework] += 1

        return context

    def get_context_insights(self, session_id: str) -> Dict[str, Any]:
        """Generate insights from conversation context"""
        context = self.get_or_create_context(session_id)

        # Analyze conversation patterns
        topic_frequency = Counter(context.previous_topics)
        framework_frequency = Counter(context.framework_usage_history)

        return {
            "recurring_themes": list(topic_frequency.most_common(3)),
            "preferred_frameworks": list(framework_frequency.most_common(3)),
            "conversation_depth": len(context.conversation_history),
            "domain_focus": context.domain_focus,
            "complexity_progression": self._analyze_complexity_progression(context),
        }

    def _analyze_complexity_progression(
        self, context: ConversationContext
    ) -> Dict[str, Any]:
        """Analyze how conversation complexity has evolved"""
        if len(context.conversation_history) < 2:
            return {"trend": "insufficient_data", "complexity": "medium"}

        # Simple complexity heuristic based on input length and framework usage
        recent_complexity = []
        for entry in context.conversation_history[-3:]:
            complexity_score = (
                len(entry["input"]) / 100 + len(entry["frameworks"]) * 0.5
            )
            recent_complexity.append(complexity_score)

        if len(recent_complexity) > 1:
            trend = (
                "increasing"
                if recent_complexity[-1] > recent_complexity[0]
                else "stable"
            )
        else:
            trend = "stable"

        return {
            "trend": trend,
            "current_complexity": (
                "high"
                if recent_complexity[-1] > 2
                else "medium" if recent_complexity[-1] > 1 else "low"
            ),
            "progression": recent_complexity,
        }


class MultiFrameworkIntegrationEngine:
    """Handles intelligent combination of multiple strategic frameworks"""

    def __init__(self, base_engine: EmbeddedFrameworkEngine):
        self.base_engine = base_engine
        self.framework_synergies = self._initialize_framework_synergies()
        self.integration_patterns = self._initialize_integration_patterns()

    def _initialize_framework_synergies(self) -> Dict[str, List[str]]:
        """Define which frameworks work well together"""
        return {
            "rumelt_strategy_kernel": [
                "decisive_wrap_framework",
                "strategic_platform_assessment",
                "organizational_transformation",
            ],
            "decisive_wrap_framework": [
                "rumelt_strategy_kernel",
                "technical_strategy_framework",
            ],
            "strategic_platform_assessment": [
                "rumelt_strategy_kernel",
                "organizational_transformation",
                "technical_strategy_framework",
            ],
            "team_topologies": [
                "organizational_transformation",
                "accelerate_team_performance",
                "scaling_up_excellence",
            ],
            "accelerate_team_performance": ["team_topologies", "scaling_up_excellence"],
            "crucial_conversations": [
                "organizational_transformation",
                "scaling_up_excellence",
            ],
        }

    def _initialize_integration_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Define patterns for integrating specific framework combinations"""
        return {
            "strategic_analysis": {
                "frameworks": [
                    "rumelt_strategy_kernel",
                    "strategic_platform_assessment",
                ],
                "integration_focus": "comprehensive_strategic_planning",
                "output_structure": [
                    "diagnosis",
                    "policy",
                    "actions",
                    "platform_considerations",
                ],
            },
            "organizational_design": {
                "frameworks": [
                    "team_topologies",
                    "accelerate_team_performance",
                    "organizational_transformation",
                ],
                "integration_focus": "team_structure_optimization",
                "output_structure": [
                    "current_state",
                    "team_patterns",
                    "performance_metrics",
                    "transformation_plan",
                ],
            },
            "decision_making": {
                "frameworks": ["decisive_wrap_framework", "rumelt_strategy_kernel"],
                "integration_focus": "systematic_decision_process",
                "output_structure": [
                    "options",
                    "evidence",
                    "distance",
                    "preparation",
                    "strategic_alignment",
                ],
            },
            "scaling_leadership": {
                "frameworks": [
                    "scaling_up_excellence",
                    "crucial_conversations",
                    "organizational_transformation",
                ],
                "integration_focus": "leadership_scaling_strategy",
                "output_structure": [
                    "excellence_spread",
                    "communication_strategy",
                    "change_management",
                ],
            },
        }

    def identify_optimal_frameworks(
        self, user_input: str, context: ConversationContext
    ) -> List[str]:
        """Intelligently select multiple frameworks based on input and context"""
        # Get base framework recommendation
        primary_framework = self._select_primary_framework(user_input, context)

        # Find synergistic frameworks
        supporting_frameworks = self._find_supporting_frameworks(
            primary_framework, user_input, context
        )

        # Limit to 3 frameworks maximum for manageable complexity
        all_frameworks = [primary_framework] + supporting_frameworks[:2]

        logger.info(
            "Multi-framework selection",
            primary=primary_framework,
            supporting=supporting_frameworks,
            final_selection=all_frameworks,
        )

        return all_frameworks

    def _select_primary_framework(
        self, user_input: str, context: ConversationContext
    ) -> str:
        """Select the primary framework using enhanced context awareness"""
        # Use existing framework selection logic but enhance with context
        base_selection = self._get_base_framework_recommendation(user_input)

        # Enhance selection based on conversation history
        if context.framework_usage_history:
            recent_frameworks = context.framework_usage_history[-3:]
            framework_frequency = Counter(recent_frameworks)

            # If user frequently uses certain frameworks, consider related ones
            for framework, count in framework_frequency.most_common(2):
                synergistic = self.framework_synergies.get(framework, [])
                if base_selection in synergistic:
                    logger.info(
                        "Framework selection enhanced by usage history",
                        base=base_selection,
                        historic_pattern=framework,
                    )
                    break

        return base_selection

    def _get_base_framework_recommendation(self, user_input: str) -> str:
        """Get base framework recommendation using existing logic"""
        # Simple keyword-based selection for now - this can be enhanced
        input_lower = user_input.lower()

        if any(
            word in input_lower
            for word in ["strategy", "strategic", "direction", "vision"]
        ):
            return "rumelt_strategy_kernel"
        elif any(
            word in input_lower for word in ["decision", "choose", "options", "decide"]
        ):
            return "decisive_wrap_framework"
        elif any(
            word in input_lower for word in ["platform", "architecture", "technical"]
        ):
            return "strategic_platform_assessment"
        elif any(word in input_lower for word in ["team", "organization", "structure"]):
            return "team_topologies"
        elif any(
            word in input_lower for word in ["performance", "metrics", "velocity"]
        ):
            return "accelerate_team_performance"
        elif any(word in input_lower for word in ["scaling", "growth", "expansion"]):
            return "scaling_up_excellence"
        elif any(
            word in input_lower
            for word in ["communication", "conversation", "conflict"]
        ):
            return "crucial_conversations"
        else:
            return "rumelt_strategy_kernel"  # Default to strategy kernel

    def _find_supporting_frameworks(
        self, primary_framework: str, user_input: str, context: ConversationContext
    ) -> List[str]:
        """Find frameworks that complement the primary framework"""
        synergistic = self.framework_synergies.get(primary_framework, [])

        # Score supporting frameworks based on input relevance and context
        framework_scores = {}

        for framework in synergistic:
            score = self._calculate_framework_relevance(framework, user_input, context)
            framework_scores[framework] = score

        # Return top scoring frameworks
        sorted_frameworks = sorted(
            framework_scores.items(), key=lambda x: x[1], reverse=True
        )
        return [framework for framework, score in sorted_frameworks if score > 0.3]

    def _calculate_framework_relevance(
        self, framework: str, user_input: str, context: ConversationContext
    ) -> float:
        """Calculate how relevant a framework is to current input and context"""
        score = 0.0
        input_lower = user_input.lower()

        # Framework-specific keyword relevance
        framework_keywords = {
            "decisive_wrap_framework": ["decision", "options", "evidence", "choose"],
            "strategic_platform_assessment": [
                "platform",
                "technical",
                "architecture",
                "infrastructure",
            ],
            "organizational_transformation": [
                "change",
                "transform",
                "culture",
                "organization",
            ],
            "team_topologies": ["team", "structure", "topology", "boundary"],
            "accelerate_team_performance": [
                "performance",
                "velocity",
                "metrics",
                "throughput",
            ],
            "scaling_up_excellence": ["scaling", "growth", "excellence", "spread"],
            "crucial_conversations": [
                "communication",
                "conversation",
                "dialogue",
                "conflict",
            ],
        }

        keywords = framework_keywords.get(framework, [])
        keyword_matches = sum(1 for keyword in keywords if keyword in input_lower)
        score += keyword_matches * 0.3

        # Context relevance based on conversation history
        if framework in context.framework_usage_history:
            usage_frequency = context.framework_usage_history.count(framework)
            score += min(usage_frequency * 0.1, 0.4)  # Cap at 0.4

        # Strategic theme alignment
        theme_alignment = self._check_theme_alignment(
            framework, context.strategic_themes
        )
        score += theme_alignment * 0.3

        return min(score, 1.0)  # Cap at 1.0

    def _check_theme_alignment(self, framework: str, themes: Set[str]) -> float:
        """Check how well framework aligns with conversation themes"""
        framework_themes = {
            "rumelt_strategy_kernel": {"strategy", "planning", "direction", "goals"},
            "decisive_wrap_framework": {"decisions", "choices", "options", "analysis"},
            "strategic_platform_assessment": {
                "platform",
                "technology",
                "architecture",
                "technical",
            },
            "team_topologies": {"teams", "structure", "organization", "boundaries"},
            "accelerate_team_performance": {
                "performance",
                "metrics",
                "velocity",
                "delivery",
            },
            "scaling_up_excellence": {"scaling", "growth", "excellence", "standards"},
            "crucial_conversations": {
                "communication",
                "relationships",
                "conflict",
                "dialogue",
            },
        }

        framework_theme_set = framework_themes.get(framework, set())
        overlap = len(themes.intersection(framework_theme_set))

        return min(overlap / max(len(framework_theme_set), 1), 1.0)

    def integrate_framework_analyses(
        self,
        analyses: List[FrameworkAnalysis],
        user_input: str,
        context: ConversationContext,
    ) -> MultiFrameworkAnalysis:
        """Integrate multiple framework analyses into comprehensive insights"""
        if not analyses:
            raise ValueError("At least one framework analysis required")

        primary_analysis = analyses[0]
        supporting_analyses = analyses[1:] if len(analyses) > 1 else []

        # Combine insights from all frameworks
        integrated_insights = self._combine_insights(analyses)

        # Identify cross-framework patterns
        cross_patterns = self._identify_cross_patterns(analyses)

        # Generate comprehensive recommendations
        comprehensive_recommendations = self._generate_comprehensive_recommendations(
            analyses, context
        )

        # Create implementation roadmap
        implementation_roadmap = self._create_implementation_roadmap(analyses, context)

        # Analyze stakeholder considerations
        stakeholder_considerations = self._analyze_stakeholder_considerations(
            analyses, context
        )

        # Calculate confidence and relevance scores
        confidence_score = self._calculate_confidence_score(analyses, user_input)
        context_relevance = self._calculate_context_relevance(analyses, context)

        return MultiFrameworkAnalysis(
            primary_framework=primary_analysis,
            supporting_frameworks=supporting_analyses,
            integrated_insights=integrated_insights,
            cross_framework_patterns=cross_patterns,
            comprehensive_recommendations=comprehensive_recommendations,
            implementation_roadmap=implementation_roadmap,
            stakeholder_considerations=stakeholder_considerations,
            confidence_score=confidence_score,
            context_relevance=context_relevance,
        )

    def _combine_insights(self, analyses: List[FrameworkAnalysis]) -> Dict[str, Any]:
        """Combine insights from multiple framework analyses"""
        combined = {
            "strategic_themes": [],
            "common_patterns": [],
            "complementary_perspectives": {},
            "unified_diagnosis": "",
            "integrated_approach": [],
        }

        # Extract strategic themes from all analyses
        for analysis in analyses:
            if "strategic_themes" in analysis.structured_insights:
                combined["strategic_themes"].extend(
                    analysis.structured_insights["strategic_themes"]
                )

        # Find common patterns across frameworks
        all_patterns = []
        for analysis in analyses:
            if "patterns" in analysis.structured_insights:
                all_patterns.extend(analysis.structured_insights.get("patterns", []))

        pattern_frequency = Counter(all_patterns)
        combined["common_patterns"] = [
            pattern for pattern, count in pattern_frequency.most_common(5) if count > 1
        ]

        # Organize complementary perspectives
        for analysis in analyses:
            combined["complementary_perspectives"][analysis.framework_name] = {
                "unique_insights": analysis.structured_insights.get(
                    "unique_insights", []
                ),
                "framework_focus": analysis.structured_insights.get("focus_area", ""),
                "key_recommendations": analysis.recommendations[:3],
            }

        return combined

    def _identify_cross_patterns(self, analyses: List[FrameworkAnalysis]) -> List[str]:
        """Identify patterns that emerge across multiple frameworks"""
        patterns = []

        # Look for common themes in recommendations
        all_recommendations = []
        for analysis in analyses:
            all_recommendations.extend(analysis.recommendations)

        # Simple pattern detection based on keyword frequency
        recommendation_text = " ".join(all_recommendations).lower()

        # Key pattern indicators
        pattern_indicators = {
            "communication_focus": [
                "communication",
                "stakeholder",
                "alignment",
                "clarity",
            ],
            "incremental_approach": [
                "phase",
                "gradual",
                "step",
                "incremental",
                "iterative",
            ],
            "measurement_emphasis": [
                "metrics",
                "measure",
                "track",
                "monitor",
                "assess",
            ],
            "risk_mitigation": [
                "risk",
                "mitigation",
                "contingency",
                "backup",
                "fallback",
            ],
            "stakeholder_engagement": [
                "stakeholder",
                "engagement",
                "buy-in",
                "support",
                "involvement",
            ],
        }

        for pattern_name, keywords in pattern_indicators.items():
            keyword_count = sum(
                1 for keyword in keywords if keyword in recommendation_text
            )
            if keyword_count >= 2:  # At least 2 keywords present
                patterns.append(
                    f"Cross-framework emphasis on {pattern_name.replace('_', ' ')}"
                )

        return patterns

    def _generate_comprehensive_recommendations(
        self, analyses: List[FrameworkAnalysis], context: ConversationContext
    ) -> List[str]:
        """Generate recommendations that synthesize insights from all frameworks"""
        recommendations = []

        # Prioritize recommendations based on framework consensus
        all_recommendations = []
        for analysis in analyses:
            all_recommendations.extend(analysis.recommendations)

        # Group similar recommendations
        recommendation_themes = self._group_recommendation_themes(all_recommendations)

        # Generate synthesized recommendations
        for theme, theme_recommendations in recommendation_themes.items():
            if len(theme_recommendations) > 1:  # Multiple frameworks agree
                synthesized = f"Multiple frameworks converge on {theme}: {theme_recommendations[0]}"
                recommendations.append(synthesized)

        # Add context-specific recommendations
        context_recommendations = self._generate_context_specific_recommendations(
            analyses, context
        )
        recommendations.extend(context_recommendations)

        return recommendations[:8]  # Limit to top 8 recommendations

    def _group_recommendation_themes(
        self, recommendations: List[str]
    ) -> Dict[str, List[str]]:
        """Group recommendations by similar themes"""
        themes = defaultdict(list)

        # Simple theme detection based on keywords
        theme_keywords = {
            "communication": [
                "communication",
                "stakeholder",
                "alignment",
                "clarity",
                "transparency",
            ],
            "planning": ["plan", "strategy", "roadmap", "timeline", "milestone"],
            "measurement": ["metrics", "measure", "track", "monitor", "kpi"],
            "risk_management": ["risk", "mitigation", "contingency", "backup"],
            "team_development": [
                "team",
                "skill",
                "capability",
                "training",
                "development",
            ],
            "process_improvement": [
                "process",
                "workflow",
                "efficiency",
                "optimization",
            ],
        }

        for recommendation in recommendations:
            rec_lower = recommendation.lower()
            best_theme = "general"
            max_matches = 0

            for theme, keywords in theme_keywords.items():
                matches = sum(1 for keyword in keywords if keyword in rec_lower)
                if matches > max_matches:
                    max_matches = matches
                    best_theme = theme

            themes[best_theme].append(recommendation)

        return dict(themes)

    def _generate_context_specific_recommendations(
        self, analyses: List[FrameworkAnalysis], context: ConversationContext
    ) -> List[str]:
        """Generate recommendations specific to conversation context"""
        recommendations = []

        # Based on conversation history patterns
        if len(context.conversation_history) > 3:
            recommendations.append(
                "Build on previous discussions to maintain strategic continuity"
            )

        # Based on recurring themes
        if len(context.strategic_themes) > 2:
            theme_list = ", ".join(list(context.strategic_themes)[:3])
            recommendations.append(
                f"Consider integrated approach addressing recurring themes: {theme_list}"
            )

        # Based on complexity progression
        insights = (
            context.conversation_history[-1] if context.conversation_history else {}
        )
        if insights and len(insights.get("frameworks", [])) > 1:
            recommendations.append(
                "Leverage multi-framework insights for comprehensive strategic planning"
            )

        return recommendations

    def _create_implementation_roadmap(
        self, analyses: List[FrameworkAnalysis], context: ConversationContext
    ) -> Dict[str, List[str]]:
        """Create implementation roadmap from integrated analysis"""
        roadmap = {
            "immediate_actions": [],
            "short_term_initiatives": [],
            "long_term_strategic_goals": [],
            "ongoing_practices": [],
        }

        # Extract implementation steps from all analyses
        all_steps = []
        for analysis in analyses:
            all_steps.extend(analysis.implementation_steps)

        # Categorize steps by timeline (simple heuristic)
        for step in all_steps:
            step_lower = step.lower()

            if any(
                word in step_lower
                for word in ["immediate", "today", "now", "asap", "urgent"]
            ):
                roadmap["immediate_actions"].append(step)
            elif any(
                word in step_lower
                for word in ["month", "quarter", "short", "soon", "next"]
            ):
                roadmap["short_term_initiatives"].append(step)
            elif any(
                word in step_lower
                for word in ["year", "long", "strategic", "future", "vision"]
            ):
                roadmap["long_term_strategic_goals"].append(step)
            else:
                roadmap["ongoing_practices"].append(step)

        # Limit each category to avoid overwhelming output
        for category in roadmap:
            roadmap[category] = roadmap[category][:4]

        return roadmap

    def _analyze_stakeholder_considerations(
        self, analyses: List[FrameworkAnalysis], context: ConversationContext
    ) -> Dict[str, List[str]]:
        """Analyze stakeholder considerations from integrated perspective"""
        stakeholder_analysis = {
            "executive_leadership": [],
            "engineering_teams": [],
            "product_organization": [],
            "external_stakeholders": [],
        }

        # Extract stakeholder mentions from analyses
        for analysis in analyses:
            considerations = analysis.key_considerations

            for consideration in considerations:
                consideration_lower = consideration.lower()

                if any(
                    word in consideration_lower
                    for word in ["executive", "leadership", "ceo", "cto", "vp"]
                ):
                    stakeholder_analysis["executive_leadership"].append(consideration)
                elif any(
                    word in consideration_lower
                    for word in ["engineering", "developer", "team", "technical"]
                ):
                    stakeholder_analysis["engineering_teams"].append(consideration)
                elif any(
                    word in consideration_lower
                    for word in ["product", "pm", "user", "customer"]
                ):
                    stakeholder_analysis["product_organization"].append(consideration)
                elif any(
                    word in consideration_lower
                    for word in ["external", "vendor", "partner", "client"]
                ):
                    stakeholder_analysis["external_stakeholders"].append(consideration)

        # Add context-based stakeholder considerations
        if context.stakeholder_mentions:
            for stakeholder in context.stakeholder_mentions:
                stakeholder_analysis["executive_leadership"].append(
                    f"Consider {stakeholder}'s perspective and requirements"
                )

        return stakeholder_analysis

    def _calculate_confidence_score(
        self, analyses: List[FrameworkAnalysis], user_input: str
    ) -> float:
        """Calculate overall confidence in the multi-framework analysis"""
        if not analyses:
            return 0.0

        # Base confidence on individual analysis confidence scores
        individual_confidences = [analysis.analysis_confidence for analysis in analyses]
        avg_confidence = sum(individual_confidences) / len(individual_confidences)

        # Boost confidence for multiple aligned frameworks
        if len(analyses) > 1:
            alignment_bonus = min(0.2, 0.1 * (len(analyses) - 1))
            avg_confidence += alignment_bonus

        # Adjust based on input clarity (simple heuristic)
        input_clarity = min(
            len(user_input.split()) / 20, 1.0
        )  # Longer inputs often clearer
        clarity_adjustment = input_clarity * 0.1

        final_confidence = min(avg_confidence + clarity_adjustment, 1.0)

        return final_confidence

    def _calculate_context_relevance(
        self, analyses: List[FrameworkAnalysis], context: ConversationContext
    ) -> float:
        """Calculate how relevant the analysis is to conversation context"""
        if not context.conversation_history:
            return 0.5  # Neutral relevance for new conversations

        relevance = 0.0

        # Historical framework alignment
        used_frameworks = [analysis.framework_name for analysis in analyses]
        historical_frameworks = set(context.framework_usage_history)

        alignment_score = len(
            set(used_frameworks).intersection(historical_frameworks)
        ) / max(len(used_frameworks), 1)
        relevance += alignment_score * 0.4

        # Theme consistency
        current_themes = set()
        for analysis in analyses:
            if "strategic_themes" in analysis.structured_insights:
                current_themes.update(analysis.structured_insights["strategic_themes"])

        theme_overlap = len(
            current_themes.intersection(context.strategic_themes)
        ) / max(len(current_themes), 1)
        relevance += theme_overlap * 0.4

        # Conversation progression appropriateness
        if context.conversation_history:
            recent_complexity = len(
                context.conversation_history[-1].get("frameworks", [])
            )
            current_complexity = len(analyses)

            if (
                abs(current_complexity - recent_complexity) <= 1
            ):  # Appropriate complexity progression
                relevance += 0.2

        return min(relevance, 1.0)


class EnhancedFrameworkEngine:
    """
    Phase 4.1: Enhanced Strategic Framework Engine

    Provides multi-framework integration, context awareness, and conversation memory
    while maintaining backwards compatibility with existing framework engine.

    Zero-setup, chat-only, conversation-native intelligence enhancement.
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

        # Initialize base components
        self.base_engine = EmbeddedFrameworkEngine(config)
        self.memory_engine = ConversationMemoryEngine()
        self.integration_engine = MultiFrameworkIntegrationEngine(self.base_engine)

        # Enhanced capabilities
        self.enhanced_mode = self.config.get("enhanced_mode", True)
        self.max_frameworks = self.config.get("max_frameworks", 3)
        self.context_window = self.config.get(
            "context_window", 5
        )  # Number of previous interactions to consider

        logger.info(
            "Enhanced Framework Engine initialized",
            enhanced_mode=self.enhanced_mode,
            max_frameworks=self.max_frameworks,
        )

    def analyze_systematically(
        self,
        user_input: str,
        session_id: str = "default",
        persona_context: Optional[Dict] = None,
    ) -> EnhancedSystematicResponse:
        """
        Enhanced systematic analysis with multi-framework integration and context awareness.

        Backwards compatible with existing analyze_systematically method.
        """
        start_time = time.time()

        # Get or create conversation context
        context = self.memory_engine.get_or_create_context(session_id)

        # Extract topics and themes from user input
        topics = self._extract_topics(user_input)

        # Determine optimal frameworks based on input and context
        if self.enhanced_mode:
            selected_frameworks = self.integration_engine.identify_optimal_frameworks(
                user_input, context
            )
        else:
            # Fallback to single framework for backwards compatibility
            primary_framework = self.integration_engine._select_primary_framework(
                user_input, context
            )
            selected_frameworks = [primary_framework]

        logger.info(
            "Framework selection completed",
            frameworks=selected_frameworks,
            enhanced_mode=self.enhanced_mode,
        )

        # Perform analysis with selected frameworks
        framework_analyses = []
        for framework_name in selected_frameworks:
            try:
                # Use base engine for individual framework analysis
                single_analysis = self.base_engine.analyze_systematically(
                    user_input, framework_name
                )
                framework_analyses.append(single_analysis.analysis)
            except Exception as e:
                logger.warning(
                    "Framework analysis failed", framework=framework_name, error=str(e)
                )
                continue

        if not framework_analyses:
            # Fallback to default framework if all fail
            fallback_analysis = self.base_engine.analyze_systematically(user_input)
            framework_analyses = [fallback_analysis.analysis]
            selected_frameworks = [fallback_analysis.framework_applied]

        # Integrate multiple framework analyses
        if len(framework_analyses) > 1 and self.enhanced_mode:
            multi_analysis = self.integration_engine.integrate_framework_analyses(
                framework_analyses, user_input, context
            )
        else:
            # Single framework analysis (backwards compatible)
            multi_analysis = MultiFrameworkAnalysis(
                primary_framework=framework_analyses[0],
                supporting_frameworks=[],
                integrated_insights={},
                cross_framework_patterns=[],
                comprehensive_recommendations=framework_analyses[0].recommendations,
                implementation_roadmap={
                    "immediate_actions": framework_analyses[0].implementation_steps
                },
                stakeholder_considerations={},
                confidence_score=framework_analyses[0].analysis_confidence,
                context_relevance=0.8,
            )

        # Generate persona-integrated response
        persona_response = self._generate_persona_integrated_response(
            multi_analysis, selected_frameworks, persona_context
        )

        # Generate context-aware recommendations
        context_recommendations = self._generate_context_aware_recommendations(
            multi_analysis, context, user_input
        )

        # Generate conversation continuity notes
        continuity_notes = self._generate_continuity_notes(context, multi_analysis)

        # Extract learning insights
        learning_insights = self._extract_learning_insights(
            user_input, multi_analysis, context, selected_frameworks
        )

        # Update conversation context
        self.memory_engine.update_context(
            session_id, user_input, topics, selected_frameworks
        )

        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)

        return EnhancedSystematicResponse(
            multi_framework_analysis=multi_analysis,
            persona_integrated_response=persona_response,
            context_aware_recommendations=context_recommendations,
            conversation_continuity_notes=continuity_notes,
            processing_time_ms=processing_time,
            frameworks_applied=selected_frameworks,
            learning_insights=learning_insights,
        )

    def _extract_topics(self, user_input: str) -> List[str]:
        """Extract strategic topics from user input"""
        topics = []
        input_lower = user_input.lower()

        # Strategic topic indicators
        topic_patterns = {
            "platform_strategy": ["platform", "architecture", "technical strategy"],
            "organizational_design": ["organization", "team structure", "reporting"],
            "decision_making": ["decision", "choice", "option", "evaluate"],
            "performance_optimization": [
                "performance",
                "efficiency",
                "optimization",
                "velocity",
            ],
            "stakeholder_management": ["stakeholder", "communication", "alignment"],
            "strategic_planning": ["strategy", "planning", "roadmap", "vision"],
            "risk_management": ["risk", "mitigation", "uncertainty", "contingency"],
            "team_development": ["team", "capability", "skill", "development"],
            "process_improvement": ["process", "workflow", "methodology", "practice"],
            "change_management": ["change", "transformation", "transition", "adoption"],
        }

        for topic, keywords in topic_patterns.items():
            if any(keyword in input_lower for keyword in keywords):
                topics.append(topic)

        return topics if topics else ["general_strategy"]

    def _generate_persona_integrated_response(
        self,
        multi_analysis: MultiFrameworkAnalysis,
        frameworks: List[str],
        persona_context: Optional[Dict],
    ) -> str:
        """Generate response that integrates analysis with persona characteristics"""
        # Base response on primary framework analysis
        base_response = multi_analysis.primary_framework.structured_insights.get(
            "summary", ""
        )

        # Enhance with multi-framework insights if available
        if multi_analysis.supporting_frameworks:
            framework_names = [
                f.framework_name for f in multi_analysis.supporting_frameworks
            ]
            enhancement = f"\n\nI'm also drawing insights from {', '.join(framework_names)} to provide you with a comprehensive perspective."
            base_response += enhancement

        # Add cross-framework patterns if identified
        if multi_analysis.cross_framework_patterns:
            patterns_text = (
                "\n\nInteresting patterns emerge across frameworks:\n"
                + "\n".join(
                    f"• {pattern}"
                    for pattern in multi_analysis.cross_framework_patterns[:3]
                )
            )
            base_response += patterns_text

        # Integrate persona characteristics if provided
        if persona_context:
            persona_name = persona_context.get("name", "Strategic Advisor")
            persona_style = persona_context.get("communication_style", "professional")

            if persona_style == "collaborative":
                base_response = f"Let's work through this together. {base_response}"
            elif persona_style == "directive":
                base_response = f"Here's my strategic assessment: {base_response}"
            elif persona_style == "consultative":
                base_response = f"Based on my analysis, I recommend: {base_response}"

        return base_response

    def _generate_context_aware_recommendations(
        self,
        multi_analysis: MultiFrameworkAnalysis,
        context: ConversationContext,
        user_input: str,
    ) -> List[str]:
        """Generate recommendations that consider conversation context"""
        recommendations = multi_analysis.comprehensive_recommendations.copy()

        # Add context-specific recommendations
        context_insights = self.memory_engine.get_context_insights(context.session_id)

        # Based on recurring themes
        if context_insights["recurring_themes"]:
            theme_name = context_insights["recurring_themes"][0][0]
            recommendations.append(
                f"Continue building on the recurring theme of {theme_name} from our discussions"
            )

        # Based on conversation depth
        if context_insights["conversation_depth"] > 3:
            recommendations.append(
                "Leverage insights from our ongoing strategic discussions for implementation"
            )

        # Based on complexity progression
        complexity_info = context_insights["complexity_progression"]
        if complexity_info["trend"] == "increasing":
            recommendations.append(
                "Consider breaking down complex initiatives into manageable phases"
            )

        return recommendations

    def _generate_continuity_notes(
        self, context: ConversationContext, multi_analysis: MultiFrameworkAnalysis
    ) -> List[str]:
        """Generate notes that maintain conversation continuity"""
        notes = []

        # Reference previous discussions
        if len(context.conversation_history) > 1:
            notes.append("This builds on our previous strategic discussions")

        # Reference framework consistency
        if context.framework_usage_history:
            consistent_frameworks = set(multi_analysis.frameworks_applied).intersection(
                set(context.framework_usage_history)
            )
            if consistent_frameworks:
                framework_names = ", ".join(consistent_frameworks)
                notes.append(
                    f"Maintaining consistency with {framework_names} approach from earlier conversations"
                )

        # Reference strategic themes
        if len(context.strategic_themes) > 2:
            notes.append(
                "Aligning with established strategic themes from our ongoing dialogue"
            )

        return notes

    def _extract_learning_insights(
        self,
        user_input: str,
        multi_analysis: MultiFrameworkAnalysis,
        context: ConversationContext,
        frameworks: List[str],
    ) -> Dict[str, Any]:
        """Extract insights for continuous learning and improvement"""
        insights = {
            "framework_effectiveness": {},
            "topic_patterns": {},
            "user_preferences": {},
            "conversation_patterns": {},
        }

        # Framework effectiveness based on confidence scores
        for framework in frameworks:
            effectiveness_score = (
                multi_analysis.confidence_score * multi_analysis.context_relevance
            )
            insights["framework_effectiveness"][framework] = effectiveness_score

        # Topic analysis patterns
        topics = self._extract_topics(user_input)
        insights["topic_patterns"] = {
            "current_topics": topics,
            "topic_complexity": len(topics),
            "frameworks_used": frameworks,
        }

        # User preference indicators
        input_characteristics = {
            "length": len(user_input),
            "complexity_indicators": len(
                [word for word in user_input.split() if len(word) > 8]
            ),
            "question_type": "detailed" if len(user_input) > 100 else "concise",
        }
        insights["user_preferences"] = input_characteristics

        # Conversation patterns
        insights["conversation_patterns"] = {
            "session_length": len(context.conversation_history),
            "framework_evolution": (
                context.framework_usage_history[-3:]
                if context.framework_usage_history
                else []
            ),
            "theme_consistency": len(context.strategic_themes),
        }

        return insights

    # Backwards compatibility methods
    def get_available_frameworks(self) -> List[str]:
        """Get list of available frameworks (backwards compatible)"""
        return self.base_engine.get_available_frameworks()

    def get_framework_info(self, framework_name: str) -> Dict[str, Any]:
        """Get framework information (backwards compatible)"""
        return self.base_engine.get_framework_info(framework_name)

    def simple_analyze(
        self, user_input: str, framework_name: Optional[str] = None
    ) -> SystematicResponse:
        """Simple analysis using single framework (backwards compatible)"""
        return self.base_engine.analyze_systematically(user_input, framework_name)


# Export enhanced engine for Phase 4 usage
__all__ = [
    "EnhancedFrameworkEngine",
    "EnhancedSystematicResponse",
    "MultiFrameworkAnalysis",
    "ConversationContext",
]
