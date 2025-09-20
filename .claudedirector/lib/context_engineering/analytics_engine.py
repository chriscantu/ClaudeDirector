#!/usr/bin/env python3
"""
Context Engineering Analytics Engine

🏗️ Sequential Thinking Phase 4.1.3 - Lightweight Facade Implementation
Advanced analytics and predictive intelligence for strategic decisions.
All complex logic consolidated into AnalyticsProcessor for maximum efficiency.

Phase 2.2 Implementation - Advanced Analytics Engine
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FrameworkRecommendation:
    """Recommended framework with confidence and reasoning"""

    framework_name: str
    confidence_score: float  # 0.0 to 1.0
    reasoning: List[str]
    context_indicators: List[str]
    success_probability: float
    estimated_impact: str  # 'high', 'medium', 'low'


@dataclass
class InitiativeHealthScore:
    """Health assessment for strategic initiatives"""

    initiative_id: str
    overall_score: float  # 0.0 to 1.0
    risk_factors: List[str]
    success_indicators: List[str]
    trend: str  # 'improving', 'stable', 'declining'
    predicted_outcome: str
    warning_level: str  # 'none', 'watch', 'concern', 'critical'


@dataclass
class StakeholderEngagementMetrics:
    """Stakeholder interaction and engagement analytics"""

    stakeholder_id: str
    engagement_score: float  # 0.0 to 1.0
    communication_frequency: float
    sentiment_trend: str
    influence_level: str
    collaboration_effectiveness: float
    risk_indicators: List[str]


@dataclass
class SessionInsights:
    """🚀 ENHANCEMENT: Session pattern analysis insights for MCP enhancement"""

    patterns: Dict[str, float]  # Detected patterns with confidence scores
    trends: Dict[str, str]  # Trend analysis results
    recommendations: List[str]  # Actionable recommendations
    confidence: float  # Overall confidence in analysis


class FrameworkPatternAnalyzer:
    """🏗️ Sequential Thinking Phase 4.1.3: Lightweight facade for backward compatibility"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # Import AnalyticsProcessor for delegation
        from .analytics_processor import AnalyticsProcessor

        self.processor = AnalyticsProcessor(config)

    def predict_optimal_framework(
        self,
        context: str,
        stakeholders: List[str] = None,
        current_initiatives: List[str] = None,
    ) -> FrameworkRecommendation:
        """🏗️ Sequential Thinking Phase 4.1.3: Delegate to AnalyticsProcessor"""
        return self.processor.predict_optimal_framework(
            context, stakeholders, current_initiatives
        )


class InitiativeHealthScorer:
    """🏗️ Sequential Thinking Phase 4.1.3: Lightweight facade for backward compatibility"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # Import AnalyticsProcessor for delegation
        from .analytics_processor import AnalyticsProcessor

        self.processor = AnalyticsProcessor(config)

    def calculate_health_score(
        self, initiative_data: Dict[str, Any]
    ) -> InitiativeHealthScore:
        """🏗️ Sequential Thinking Phase 4.1.3: Delegate to AnalyticsProcessor"""
        return self.processor.calculate_health_score(initiative_data)


class StakeholderEngagementAnalyzer:
    """🏗️ Sequential Thinking Phase 4.1.3: Lightweight facade for backward compatibility"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        # Import AnalyticsProcessor for delegation
        from .analytics_processor import AnalyticsProcessor

        self.processor = AnalyticsProcessor(config)

    def analyze_stakeholder_engagement(
        self, stakeholder_id: str, interaction_history: List[Dict[str, Any]]
    ) -> StakeholderEngagementMetrics:
        """🏗️ Sequential Thinking Phase 4.1.3: Delegate to AnalyticsProcessor"""
        return self.processor.analyze_stakeholder_engagement(
            stakeholder_id, interaction_history
        )


class AnalyticsEngine:
    """
    🏗️ Sequential Thinking Phase 4.1.3: Lightweight orchestration facade

    Advanced analytics and predictive intelligence for strategic decisions
    Coordinates framework pattern analysis, initiative health scoring,
    and stakeholder engagement analytics to provide comprehensive
    strategic intelligence.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Import AnalyticsProcessor for consolidated logic
        from .analytics_processor import AnalyticsProcessor

        self.processor = AnalyticsProcessor(config)

        # Initialize lightweight component facades for backward compatibility
        self.framework_analyzer = FrameworkPatternAnalyzer(
            self.config.get("framework_analyzer", {})
        )
        self.initiative_scorer = InitiativeHealthScorer(
            self.config.get("initiative_scorer", {})
        )
        self.stakeholder_analyzer = StakeholderEngagementAnalyzer(
            self.config.get("stakeholder_analyzer", {})
        )

        # Performance tracking
        self.analytics_metrics = []

        self.logger.info("AnalyticsEngine initialized with lightweight facade pattern")

    def get_strategic_recommendations(
        self,
        context: str,
        stakeholders: List[str] = None,
        initiatives: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """🏗️ Sequential Thinking Phase 4.1.3: Delegate to AnalyticsProcessor"""
        return self.processor.get_strategic_recommendations(
            context, stakeholders, initiatives
        )

    def get_performance_summary(self) -> Dict[str, Any]:
        """🏗️ Sequential Thinking Phase 4.1.3: Delegate to AnalyticsProcessor"""
        return self.processor.get_performance_summary()

    # 🚀 ENHANCEMENT: MCP Session Pattern Analysis (Task 002)
    async def analyze_mcp_session_patterns(
        self, session_data: List[Dict]
    ) -> "SessionInsights":
        """
        🚀 ENHANCEMENT: Add MCP session pattern analysis to existing analytics

        Leverages existing analytics infrastructure while adding:
        - Session conversation pattern analysis
        - Query type trend detection within session
        - Simple rule-based recommendations
        - Integration with existing persona system for context-aware insights
        """
        patterns = self._detect_session_patterns(session_data)
        trends = self._analyze_session_trends(session_data)
        recommendations = self._generate_session_recommendations(patterns, trends)

        # 🚀 PHASE 1 EXTENSION: Add retrospective-specific analysis using existing patterns
        insights = SessionInsights(
            patterns=patterns,
            trends=trends,
            recommendations=recommendations,
            confidence=self._calculate_confidence(session_data),
        )

        # EXTEND with retrospective analysis if retrospective session detected
        if self._is_retrospective_session(session_data):
            insights = await self._enhance_with_retrospective_analysis(
                insights, session_data
            )

        return insights

    def _detect_session_patterns(self, session_data: List[Dict]) -> Dict[str, float]:
        """Detect patterns using existing ML pattern engine."""
        # Use existing ml_pattern_engine for session-scoped analysis
        from .ml_pattern_engine import CollaborationScorer

        try:
            if not session_data:
                return {"no_data": 1.0}

            # Analyze query patterns within session
            query_types = {}
            for entry in session_data:
                query_type = self._classify_query_type(entry.get("query", ""))
                query_types[query_type] = query_types.get(query_type, 0) + 1

            total_queries = len(session_data)
            patterns = {}

            # Calculate pattern percentages
            for query_type, count in query_types.items():
                patterns[query_type] = count / total_queries

            # Detect conversation flow patterns
            patterns.update(self._detect_conversation_flow(session_data))

            return patterns

        except Exception as e:
            self.logger.warning(f"Pattern detection error: {e}")
            return {"fallback_pattern": 0.7}

    def _analyze_session_trends(self, session_data: List[Dict]) -> Dict[str, str]:
        """Analyze trends within session using existing analytics infrastructure."""
        # Trend analysis within session boundaries
        if not session_data or len(session_data) < 2:
            return {"trend": "insufficient_data"}

        try:
            # Analyze complexity progression
            complexity_scores = []
            for entry in session_data:
                complexity = self._assess_query_complexity(entry.get("query", ""))
                complexity_scores.append(complexity)

            # Calculate trend direction
            if len(complexity_scores) >= 3:
                early_avg = sum(complexity_scores[: len(complexity_scores) // 2]) / (
                    len(complexity_scores) // 2
                )
                late_avg = sum(complexity_scores[len(complexity_scores) // 2 :]) / (
                    len(complexity_scores) - len(complexity_scores) // 2
                )

                if late_avg > early_avg + 0.1:
                    complexity_trend = "increasing"
                elif early_avg > late_avg + 0.1:
                    complexity_trend = "decreasing"
                else:
                    complexity_trend = "stable"
            else:
                complexity_trend = "stable"

            return {
                "complexity_trend": complexity_trend,
                "session_focus": self._determine_session_focus(session_data),
                "engagement_level": self._assess_engagement_level(session_data),
            }

        except Exception as e:
            self.logger.warning(f"Trend analysis error: {e}")
            return {"trend": "analysis_error"}

    def _generate_session_recommendations(
        self, patterns: Dict, trends: Dict
    ) -> List[str]:
        """Generate actionable recommendations based on session analysis."""
        # Rule-based recommendations using existing patterns
        recommendations = []

        try:
            # Pattern-based recommendations
            if patterns.get("strategic_analysis", 0) > 0.5:
                recommendations.append(
                    "Consider using Sequential MCP server for deeper strategic analysis"
                )

            if patterns.get("technical_documentation", 0) > 0.4:
                recommendations.append(
                    "Leverage Context7 MCP server for comprehensive documentation lookup"
                )

            if patterns.get("ui_design", 0) > 0.3:
                recommendations.append(
                    "Utilize Magic MCP server for UI component generation and design"
                )

            # Trend-based recommendations
            complexity_trend = trends.get("complexity_trend", "stable")
            if complexity_trend == "increasing":
                recommendations.append(
                    "Break down complex queries into smaller, focused questions"
                )
            elif complexity_trend == "decreasing":
                recommendations.append(
                    "Consider exploring more advanced strategic frameworks"
                )

            engagement_level = trends.get("engagement_level", "medium")
            if engagement_level == "low":
                recommendations.append(
                    "Try more specific, actionable questions to improve session value"
                )
            elif engagement_level == "high":
                recommendations.append(
                    "Maintain current interaction patterns for optimal results"
                )

            return recommendations[:5]  # Limit for readability

        except Exception as e:
            self.logger.warning(f"Recommendation generation error: {e}")
            return ["Continue current session patterns and monitor for improvements"]

    def _classify_query_type(self, query: str) -> str:
        """Classify query type for pattern analysis."""
        query_lower = query.lower()

        # Strategic analysis patterns
        strategic_keywords = [
            "strategy",
            "roadmap",
            "planning",
            "decision",
            "business",
            "roi",
        ]
        if any(keyword in query_lower for keyword in strategic_keywords):
            return "strategic_analysis"

        # Technical documentation patterns
        tech_keywords = [
            "documentation",
            "docs",
            "api",
            "library",
            "framework",
            "guide",
        ]
        if any(keyword in query_lower for keyword in tech_keywords):
            return "technical_documentation"

        # UI/Design patterns
        ui_keywords = [
            "component",
            "design",
            "ui",
            "interface",
            "button",
            "form",
            "layout",
        ]
        if any(keyword in query_lower for keyword in ui_keywords):
            return "ui_design"

        # Testing patterns
        test_keywords = ["test", "testing", "automation", "e2e", "playwright"]
        if any(keyword in query_lower for keyword in test_keywords):
            return "testing_automation"

        return "general_query"

    def _detect_conversation_flow(self, session_data: List[Dict]) -> Dict[str, float]:
        """Detect conversation flow patterns within session."""
        if len(session_data) < 2:
            return {"flow_pattern": 0.5}

        # Analyze query transitions
        transitions = []
        for i in range(len(session_data) - 1):
            current_type = self._classify_query_type(session_data[i].get("query", ""))
            next_type = self._classify_query_type(session_data[i + 1].get("query", ""))
            transitions.append((current_type, next_type))

        # Calculate flow coherence
        same_topic_transitions = sum(
            1 for curr, next_t in transitions if curr == next_t
        )
        flow_coherence = (
            same_topic_transitions / len(transitions) if transitions else 0.5
        )

        return {
            "flow_coherence": flow_coherence,
            "topic_diversity": len(
                set(
                    self._classify_query_type(entry.get("query", ""))
                    for entry in session_data
                )
            )
            / max(len(session_data), 1),
        }

    def _assess_query_complexity(self, query: str) -> float:
        """Assess complexity of individual query."""
        if not query:
            return 0.1

        # Simple complexity heuristics
        complexity_indicators = [
            "analyze",
            "compare",
            "implement",
            "optimize",
            "integrate",
            "strategic",
        ]
        complexity_score = sum(
            1 for indicator in complexity_indicators if indicator in query.lower()
        )

        # Length-based complexity
        length_score = min(len(query.split()) / 20, 1.0)  # Normalize to 0-1

        return (complexity_score * 0.3 + length_score * 0.7) / 2

    def _determine_session_focus(self, session_data: List[Dict]) -> str:
        """Determine primary focus of session."""
        if not session_data:
            return "unknown"

        query_types = [
            self._classify_query_type(entry.get("query", "")) for entry in session_data
        ]
        from collections import Counter

        type_counts = Counter(query_types)

        if type_counts:
            most_common = type_counts.most_common(1)[0]
            if most_common[1] > len(session_data) * 0.4:  # >40% of queries
                return most_common[0]

        return "mixed_focus"

    def _assess_engagement_level(self, session_data: List[Dict]) -> str:
        """Assess user engagement level in session."""
        if not session_data:
            return "low"

        # Simple engagement heuristics
        avg_query_length = sum(
            len(entry.get("query", "").split()) for entry in session_data
        ) / len(session_data)
        session_length = len(session_data)

        if avg_query_length > 10 and session_length > 5:
            return "high"
        elif avg_query_length > 5 or session_length > 3:
            return "medium"
        else:
            return "low"

    def _calculate_confidence(self, session_data: List[Dict]) -> float:
        """Calculate confidence in session analysis."""
        if not session_data:
            return 0.1

        # Confidence based on data quality and quantity
        data_quality = len(session_data) / 10  # More data = higher confidence
        query_quality = sum(
            1 for entry in session_data if len(entry.get("query", "")) > 10
        ) / len(session_data)

        return min((data_quality + query_quality) / 2, 0.95)

    # 🚀 PHASE 1 EXTENSION: Retrospective-specific analysis methods (REUSE existing patterns)
    def _is_retrospective_session(self, session_data: List[Dict]) -> bool:
        """
        Detect if session contains retrospective patterns - EXTENDS existing detection logic

        BLOAT_PREVENTION: REUSES existing pattern detection approach
        """
        if not session_data:
            return False

        # Check for retrospective keywords in session queries (REUSE existing classification logic)
        retrospective_indicators = [
            "retrospective",
            "reflection",
            "weekly review",
            "progress",
            "improvement",
            "rating",
            "what did i",
            "how could i",
            "scale of 1",
        ]

        retrospective_count = 0
        for entry in session_data:
            query = entry.get("query", "").lower()
            if any(indicator in query for indicator in retrospective_indicators):
                retrospective_count += 1

        # Consider it a retrospective session if >30% of queries contain retrospective patterns
        return retrospective_count / len(session_data) > 0.3

    async def _enhance_with_retrospective_analysis(
        self, insights: SessionInsights, session_data: List[Dict]
    ) -> SessionInsights:
        """
        EXTEND: Add retrospective-specific insights using existing analytics framework

        BLOAT_PREVENTION: REUSES existing SessionInsights structure, trend analysis, recommendation generation
        ARCHITECTURE: Integrates with existing analytics patterns
        """
        try:
            # REUSE existing patterns structure and ADD retrospective-specific patterns
            enhanced_patterns = insights.patterns.copy()
            enhanced_patterns.update(
                {
                    "retrospective_focus": self._calculate_retrospective_focus(
                        session_data
                    ),
                    "progress_assessment": self._analyze_progress_patterns(
                        session_data
                    ),
                    "improvement_identification": self._analyze_improvement_patterns(
                        session_data
                    ),
                }
            )

            # REUSE existing trends structure and ADD retrospective-specific trends
            enhanced_trends = insights.trends.copy()
            enhanced_trends.update(
                {
                    "retrospective_depth": self._assess_retrospective_depth(
                        session_data
                    ),
                    "reflection_quality": self._assess_reflection_quality(session_data),
                }
            )

            # REUSE existing recommendation generation and ADD retrospective-specific recommendations
            enhanced_recommendations = insights.recommendations.copy()
            retrospective_recommendations = (
                self._generate_retrospective_recommendations(
                    enhanced_patterns, enhanced_trends
                )
            )
            enhanced_recommendations.extend(retrospective_recommendations)

            # Return enhanced insights using existing SessionInsights structure
            return SessionInsights(
                patterns=enhanced_patterns,
                trends=enhanced_trends,
                recommendations=enhanced_recommendations[:8],  # Limit for readability
                confidence=insights.confidence,
            )

        except Exception as e:
            self.logger.warning(f"Retrospective analysis enhancement error: {e}")
            # Return original insights if enhancement fails (graceful degradation)
            return insights

    def _calculate_retrospective_focus(self, session_data: List[Dict]) -> float:
        """Calculate how focused the session is on retrospective themes."""
        if not session_data:
            return 0.0

        retrospective_terms = [
            "progress",
            "achievement",
            "improvement",
            "challenge",
            "learning",
        ]
        focus_score = 0.0

        for entry in session_data:
            query = entry.get("query", "").lower()
            term_count = sum(1 for term in retrospective_terms if term in query)
            focus_score += min(term_count / len(retrospective_terms), 1.0)

        return focus_score / len(session_data)

    def _analyze_progress_patterns(self, session_data: List[Dict]) -> float:
        """Analyze patterns related to progress assessment."""
        progress_indicators = [
            "accomplished",
            "completed",
            "achieved",
            "finished",
            "delivered",
        ]

        progress_mentions = 0
        for entry in session_data:
            query = entry.get("query", "").lower()
            progress_mentions += sum(
                1 for indicator in progress_indicators if indicator in query
            )

        return min(progress_mentions / max(len(session_data), 1), 1.0)

    def _analyze_improvement_patterns(self, session_data: List[Dict]) -> float:
        """Analyze patterns related to improvement identification."""
        improvement_indicators = [
            "better",
            "improve",
            "enhance",
            "optimize",
            "should have",
            "could have",
        ]

        improvement_mentions = 0
        for entry in session_data:
            query = entry.get("query", "").lower()
            improvement_mentions += sum(
                1 for indicator in improvement_indicators if indicator in query
            )

        return min(improvement_mentions / max(len(session_data), 1), 1.0)

    def _assess_retrospective_depth(self, session_data: List[Dict]) -> str:
        """Assess the depth of retrospective analysis."""
        if not session_data:
            return "shallow"

        depth_indicators = [
            "why",
            "because",
            "impact",
            "result",
            "consequence",
            "root cause",
        ]
        depth_score = 0

        for entry in session_data:
            query = entry.get("query", "").lower()
            depth_score += sum(
                1 for indicator in depth_indicators if indicator in query
            )

        avg_depth = depth_score / len(session_data)

        if avg_depth > 1.5:
            return "deep"
        elif avg_depth > 0.5:
            return "moderate"
        else:
            return "shallow"

    def _assess_reflection_quality(self, session_data: List[Dict]) -> str:
        """Assess quality of reflection based on session patterns."""
        if not session_data:
            return "low"

        quality_indicators = [
            "learned",
            "insight",
            "pattern",
            "trend",
            "hypothesis",
            "evidence",
        ]
        quality_score = 0

        for entry in session_data:
            query = entry.get("query", "").lower()
            quality_score += sum(
                1 for indicator in quality_indicators if indicator in query
            )

        avg_quality = quality_score / len(session_data)

        if avg_quality > 1.0:
            return "high"
        elif avg_quality > 0.3:
            return "medium"
        else:
            return "low"

    def _generate_retrospective_recommendations(
        self, patterns: Dict, trends: Dict
    ) -> List[str]:
        """Generate retrospective-specific recommendations using existing recommendation patterns."""
        recommendations = []

        # Progress-focused recommendations
        if patterns.get("progress_assessment", 0) < 0.3:
            recommendations.append(
                "Focus more on specific accomplishments and measurable progress indicators"
            )

        # Improvement-focused recommendations
        if patterns.get("improvement_identification", 0) < 0.3:
            recommendations.append(
                "Spend more time identifying specific areas for improvement and actionable next steps"
            )

        # Depth-focused recommendations
        if trends.get("retrospective_depth") == "shallow":
            recommendations.append(
                "Consider asking 'why' more often to deepen retrospective analysis"
            )
        elif trends.get("retrospective_depth") == "deep":
            recommendations.append(
                "Excellent depth of analysis - continue this reflective approach"
            )

        # Quality-focused recommendations
        if trends.get("reflection_quality") == "low":
            recommendations.append(
                "Try to identify patterns and insights from your experiences"
            )
        elif trends.get("reflection_quality") == "high":
            recommendations.append(
                "Strong reflective quality - consider documenting key insights for future reference"
            )

        # Focus-focused recommendations
        if patterns.get("retrospective_focus", 0) > 0.8:
            recommendations.append(
                "Well-focused retrospective session with clear themes"
            )
        elif patterns.get("retrospective_focus", 0) < 0.4:
            recommendations.append(
                "Consider structuring retrospective around specific themes (progress, challenges, learnings)"
            )

        return recommendations[:3]  # Return top 3 recommendations

    # 🏗️ All complex logic consolidated into AnalyticsProcessor
    # This lightweight facade maintains API compatibility while leveraging consolidated implementation
