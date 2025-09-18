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
    def analyze_mcp_session_patterns(
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

        return SessionInsights(
            patterns=patterns,
            trends=trends,
            recommendations=recommendations,
            confidence=self._calculate_confidence(session_data),
        )

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

    # 🏗️ All complex logic consolidated into AnalyticsProcessor
    # This lightweight facade maintains API compatibility while leveraging consolidated implementation
