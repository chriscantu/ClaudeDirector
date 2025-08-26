#!/usr/bin/env python3
"""
Context Engineering Analytics Engine

Advanced analytics and predictive intelligence for strategic decisions.
Provides framework recommendations, initiative health scoring, and
organizational learning acceleration.

Phase 2.2 Implementation - Advanced Analytics Engine
"""

import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta

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


class FrameworkPatternAnalyzer:
    """Analyzes framework usage patterns and predicts optimal applications"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__ + ".FrameworkAnalyzer")

        # Framework effectiveness database (will be populated from historical data)
        self.framework_patterns = {}
        self.success_metrics = {}

        self.logger.info("FrameworkPatternAnalyzer initialized")

    def predict_optimal_framework(
        self,
        context: str,
        stakeholders: List[str] = None,
        current_initiatives: List[str] = None,
    ) -> FrameworkRecommendation:
        """
        Predict best framework for given strategic context

        Args:
            context: Strategic context description
            stakeholders: Involved stakeholders
            current_initiatives: Related initiatives

        Returns:
            FrameworkRecommendation with confidence and reasoning
        """
        try:
            start_time = time.time()

            # Analyze context for framework indicators
            context_indicators = self._extract_context_indicators(context)

            # Score frameworks based on context match
            framework_scores = self._score_frameworks(
                context_indicators, stakeholders, current_initiatives
            )

            # Select best framework
            best_framework, confidence = self._select_best_framework(framework_scores)

            # Generate reasoning
            reasoning = self._generate_reasoning(best_framework, context_indicators)

            # Calculate success probability
            success_prob = self._calculate_success_probability(
                best_framework, context_indicators
            )

            # Estimate impact
            impact = self._estimate_impact(best_framework, context)

            processing_time = time.time() - start_time
            self.logger.info(
                f"Framework prediction completed in {processing_time:.3f}s"
            )

            return FrameworkRecommendation(
                framework_name=best_framework,
                confidence_score=confidence,
                reasoning=reasoning,
                context_indicators=context_indicators,
                success_probability=success_prob,
                estimated_impact=impact,
            )

        except Exception as e:
            self.logger.error(f"Error predicting framework: {e}")
            return self._get_fallback_recommendation()

    def _extract_context_indicators(self, context: str) -> List[str]:
        """Extract strategic indicators from context"""
        indicators = []
        context_lower = context.lower()

        # Framework trigger patterns
        framework_patterns = {
            "team_topologies": ["team", "cognitive load", "organization", "structure"],
            "wrap_framework": ["decision", "options", "choice", "analysis"],
            "good_strategy": ["strategy", "competitive", "advantage", "positioning"],
            "crucial_conversations": [
                "stakeholder",
                "conflict",
                "alignment",
                "communication",
            ],
            "capital_allocation": ["budget", "investment", "resource", "roi"],
            "accelerate": ["performance", "devops", "delivery", "metrics"],
            "platform_strategy": ["platform", "ecosystem", "scalability", "reuse"],
        }

        for pattern, keywords in framework_patterns.items():
            if any(keyword in context_lower for keyword in keywords):
                indicators.append(pattern)

        return indicators

    def _score_frameworks(
        self,
        indicators: List[str],
        stakeholders: List[str] = None,
        initiatives: List[str] = None,
    ) -> Dict[str, float]:
        """Score frameworks based on context indicators"""
        scores = {}

        # Base scoring from indicators
        for indicator in indicators:
            if indicator not in scores:
                scores[indicator] = 0.0
            scores[indicator] += 0.3  # Base score for context match

        # Stakeholder complexity bonus
        if stakeholders and len(stakeholders) > 3:
            scores["crucial_conversations"] = (
                scores.get("crucial_conversations", 0.0) + 0.2
            )
            scores["team_topologies"] = scores.get("team_topologies", 0.0) + 0.2

        # Initiative complexity bonus
        if initiatives and len(initiatives) > 2:
            scores["capital_allocation"] = scores.get("capital_allocation", 0.0) + 0.2
            scores["good_strategy"] = scores.get("good_strategy", 0.0) + 0.2

        return scores

    def _select_best_framework(self, scores: Dict[str, float]) -> Tuple[str, float]:
        """Select best framework with confidence score"""
        if not scores:
            return "wrap_framework", 0.5  # Default framework

        best_framework = max(scores.keys(), key=lambda k: scores[k])
        max_score = scores[best_framework]

        # Normalize confidence (max possible score is ~0.7)
        confidence = min(max_score / 0.7, 1.0)

        return best_framework, confidence

    def _generate_reasoning(self, framework: str, indicators: List[str]) -> List[str]:
        """Generate human-readable reasoning for framework selection"""
        reasoning = []

        framework_descriptions = {
            "team_topologies": "Optimal for organizational design and team structure decisions",
            "wrap_framework": "Best for structured decision-making with multiple options",
            "good_strategy": "Ideal for competitive positioning and strategic planning",
            "crucial_conversations": "Perfect for stakeholder alignment and difficult discussions",
            "capital_allocation": "Optimal for resource investment and budget decisions",
            "accelerate": "Best for engineering performance and delivery optimization",
            "platform_strategy": "Ideal for platform design and ecosystem decisions",
        }

        if framework in framework_descriptions:
            reasoning.append(framework_descriptions[framework])

        if indicators:
            reasoning.append(f"Context indicators: {', '.join(indicators)}")

        return reasoning

    def _calculate_success_probability(
        self, framework: str, indicators: List[str]
    ) -> float:
        """Calculate probability of successful framework application"""
        # Base success probability for each framework
        base_probabilities = {
            "team_topologies": 0.85,
            "wrap_framework": 0.90,
            "good_strategy": 0.80,
            "crucial_conversations": 0.75,
            "capital_allocation": 0.85,
            "accelerate": 0.80,
            "platform_strategy": 0.85,
        }

        base_prob = base_probabilities.get(framework, 0.70)

        # Boost probability based on strong context indicators
        if len(indicators) >= 2:
            base_prob = min(base_prob + 0.1, 0.95)

        return base_prob

    def _estimate_impact(self, framework: str, context: str) -> str:
        """Estimate potential impact of framework application"""
        context_lower = context.lower()

        # High impact indicators
        high_impact_keywords = [
            "strategic",
            "organizational",
            "transformation",
            "critical",
        ]

        # Medium impact indicators
        medium_impact_keywords = [
            "improvement",
            "optimization",
            "enhancement",
            "planning",
        ]

        if any(keyword in context_lower for keyword in high_impact_keywords):
            return "high"
        elif any(keyword in context_lower for keyword in medium_impact_keywords):
            return "medium"
        else:
            return "low"

    def _get_fallback_recommendation(self) -> FrameworkRecommendation:
        """Provide fallback recommendation when analysis fails"""
        return FrameworkRecommendation(
            framework_name="wrap_framework",
            confidence_score=0.5,
            reasoning=["Default recommendation due to analysis error"],
            context_indicators=[],
            success_probability=0.7,
            estimated_impact="medium",
        )


class InitiativeHealthScorer:
    """Scores initiative health and predicts risks"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__ + ".InitiativeScorer")

        self.logger.info("InitiativeHealthScorer initialized")

    def calculate_health_score(
        self, initiative_data: Dict[str, Any]
    ) -> InitiativeHealthScore:
        """
        Calculate multi-factor health score for strategic initiative

        Args:
            initiative_data: Initiative information including progress, stakeholders, etc.

        Returns:
            InitiativeHealthScore with risk assessment
        """
        try:
            initiative_id = initiative_data.get("id", "unknown")

            # Calculate component scores
            progress_score = self._calculate_progress_score(initiative_data)
            stakeholder_score = self._calculate_stakeholder_score(initiative_data)
            timeline_score = self._calculate_timeline_score(initiative_data)
            resource_score = self._calculate_resource_score(initiative_data)

            # Weighted overall score
            overall_score = (
                progress_score * 0.3
                + stakeholder_score * 0.25
                + timeline_score * 0.25
                + resource_score * 0.2
            )

            # Identify risk factors and success indicators
            risk_factors = self._identify_risk_factors(
                initiative_data,
                {
                    "progress": progress_score,
                    "stakeholder": stakeholder_score,
                    "timeline": timeline_score,
                    "resource": resource_score,
                },
            )

            success_indicators = self._identify_success_indicators(initiative_data)

            # Determine trend and warning level
            trend = self._determine_trend(initiative_data)
            warning_level = self._determine_warning_level(overall_score, risk_factors)
            predicted_outcome = self._predict_outcome(overall_score, trend)

            return InitiativeHealthScore(
                initiative_id=initiative_id,
                overall_score=overall_score,
                risk_factors=risk_factors,
                success_indicators=success_indicators,
                trend=trend,
                predicted_outcome=predicted_outcome,
                warning_level=warning_level,
            )

        except Exception as e:
            self.logger.error(f"Error calculating health score: {e}")
            return self._get_fallback_health_score(initiative_data.get("id", "unknown"))

    def _calculate_progress_score(self, data: Dict[str, Any]) -> float:
        """Calculate progress-based score"""
        # Placeholder implementation - would analyze actual progress metrics
        return 0.75  # Default moderate progress

    def _calculate_stakeholder_score(self, data: Dict[str, Any]) -> float:
        """Calculate stakeholder engagement score"""
        # Placeholder implementation - would analyze stakeholder data
        return 0.80  # Default good stakeholder engagement

    def _calculate_timeline_score(self, data: Dict[str, Any]) -> float:
        """Calculate timeline adherence score"""
        # Placeholder implementation - would analyze timeline data
        return 0.70  # Default slight timeline concern

    def _calculate_resource_score(self, data: Dict[str, Any]) -> float:
        """Calculate resource availability score"""
        # Placeholder implementation - would analyze resource data
        return 0.85  # Default good resource availability

    def _identify_risk_factors(
        self, data: Dict[str, Any], scores: Dict[str, float]
    ) -> List[str]:
        """Identify potential risk factors"""
        risks = []

        if scores["progress"] < 0.6:
            risks.append("Progress behind schedule")
        if scores["stakeholder"] < 0.7:
            risks.append("Stakeholder engagement issues")
        if scores["timeline"] < 0.6:
            risks.append("Timeline pressure")
        if scores["resource"] < 0.7:
            risks.append("Resource constraints")

        return risks

    def _identify_success_indicators(self, data: Dict[str, Any]) -> List[str]:
        """Identify positive success indicators"""
        # Placeholder implementation
        return ["Strong team engagement", "Clear deliverables defined"]

    def _determine_trend(self, data: Dict[str, Any]) -> str:
        """Determine initiative trend"""
        # Placeholder implementation - would analyze historical data
        return "stable"

    def _determine_warning_level(self, score: float, risks: List[str]) -> str:
        """Determine warning level based on score and risks"""
        if score < 0.5 or len(risks) >= 3:
            return "critical"
        elif score < 0.7 or len(risks) >= 2:
            return "concern"
        elif score < 0.8 or len(risks) >= 1:
            return "watch"
        else:
            return "none"

    def _predict_outcome(self, score: float, trend: str) -> str:
        """Predict likely initiative outcome"""
        if score >= 0.8 and trend in ["improving", "stable"]:
            return "success_likely"
        elif score >= 0.6:
            return "success_possible"
        else:
            return "risk_high"

    def _get_fallback_health_score(self, initiative_id: str) -> InitiativeHealthScore:
        """Provide fallback health score when analysis fails"""
        return InitiativeHealthScore(
            initiative_id=initiative_id,
            overall_score=0.5,
            risk_factors=["Analysis unavailable"],
            success_indicators=[],
            trend="unknown",
            predicted_outcome="uncertain",
            warning_level="watch",
        )


class StakeholderEngagementAnalyzer:
    """Analyzes stakeholder interaction patterns and engagement"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__ + ".StakeholderAnalyzer")

        self.logger.info("StakeholderEngagementAnalyzer initialized")

    def analyze_stakeholder_engagement(
        self, stakeholder_id: str, interaction_history: List[Dict[str, Any]]
    ) -> StakeholderEngagementMetrics:
        """
        Analyze stakeholder engagement patterns

        Args:
            stakeholder_id: Unique stakeholder identifier
            interaction_history: Historical interaction data

        Returns:
            StakeholderEngagementMetrics with analysis results
        """
        try:
            # Calculate engagement metrics
            engagement_score = self._calculate_engagement_score(interaction_history)
            communication_freq = self._calculate_communication_frequency(
                interaction_history
            )
            sentiment_trend = self._analyze_sentiment_trend(interaction_history)
            influence_level = self._assess_influence_level(
                stakeholder_id, interaction_history
            )
            collaboration_effectiveness = self._assess_collaboration_effectiveness(
                interaction_history
            )
            risk_indicators = self._identify_engagement_risks(interaction_history)

            return StakeholderEngagementMetrics(
                stakeholder_id=stakeholder_id,
                engagement_score=engagement_score,
                communication_frequency=communication_freq,
                sentiment_trend=sentiment_trend,
                influence_level=influence_level,
                collaboration_effectiveness=collaboration_effectiveness,
                risk_indicators=risk_indicators,
            )

        except Exception as e:
            self.logger.error(f"Error analyzing stakeholder engagement: {e}")
            return self._get_fallback_engagement_metrics(stakeholder_id)

    def _calculate_engagement_score(self, history: List[Dict[str, Any]]) -> float:
        """Calculate overall engagement score"""
        # Placeholder implementation
        return 0.75

    def _calculate_communication_frequency(
        self, history: List[Dict[str, Any]]
    ) -> float:
        """Calculate communication frequency metric"""
        # Placeholder implementation
        return 0.8

    def _analyze_sentiment_trend(self, history: List[Dict[str, Any]]) -> str:
        """Analyze sentiment trend over time"""
        # Placeholder implementation
        return "positive"

    def _assess_influence_level(
        self, stakeholder_id: str, history: List[Dict[str, Any]]
    ) -> str:
        """Assess stakeholder influence level"""
        # Placeholder implementation
        return "high"

    def _assess_collaboration_effectiveness(
        self, history: List[Dict[str, Any]]
    ) -> float:
        """Assess collaboration effectiveness"""
        # Placeholder implementation
        return 0.85

    def _identify_engagement_risks(self, history: List[Dict[str, Any]]) -> List[str]:
        """Identify engagement risk indicators"""
        # Placeholder implementation
        return []

    def _get_fallback_engagement_metrics(
        self, stakeholder_id: str
    ) -> StakeholderEngagementMetrics:
        """Provide fallback metrics when analysis fails"""
        return StakeholderEngagementMetrics(
            stakeholder_id=stakeholder_id,
            engagement_score=0.5,
            communication_frequency=0.5,
            sentiment_trend="neutral",
            influence_level="medium",
            collaboration_effectiveness=0.5,
            risk_indicators=["Analysis unavailable"],
        )


class AnalyticsEngine:
    """
    Advanced analytics and predictive intelligence for strategic decisions

    Coordinates framework pattern analysis, initiative health scoring,
    and stakeholder engagement analytics to provide comprehensive
    strategic intelligence.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Initialize component analyzers
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

        self.logger.info(
            "AnalyticsEngine initialized with predictive intelligence capabilities"
        )

    def get_strategic_recommendations(
        self,
        context: str,
        stakeholders: List[str] = None,
        initiatives: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get comprehensive strategic recommendations based on context analysis

        Args:
            context: Strategic context description
            stakeholders: Involved stakeholders
            initiatives: Current initiative data

        Returns:
            Comprehensive recommendations including frameworks, risks, and actions
        """
        start_time = time.time()

        try:
            recommendations = {}

            # Framework recommendations
            framework_rec = self.framework_analyzer.predict_optimal_framework(
                context, stakeholders, [i.get("id", "") for i in (initiatives or [])]
            )
            recommendations["framework"] = framework_rec

            # Initiative health analysis
            if initiatives:
                initiative_health = []
                for initiative in initiatives:
                    health_score = self.initiative_scorer.calculate_health_score(
                        initiative
                    )
                    initiative_health.append(health_score)
                recommendations["initiative_health"] = initiative_health

            # Stakeholder engagement analysis
            if stakeholders:
                stakeholder_analysis = []
                for stakeholder in stakeholders[:5]:  # Limit to top 5 for performance
                    # Mock interaction history - would come from real data
                    interaction_history = []
                    engagement_metrics = (
                        self.stakeholder_analyzer.analyze_stakeholder_engagement(
                            stakeholder, interaction_history
                        )
                    )
                    stakeholder_analysis.append(engagement_metrics)
                recommendations["stakeholder_engagement"] = stakeholder_analysis

            # Generate strategic insights
            insights = self._generate_strategic_insights(recommendations)
            recommendations["strategic_insights"] = insights

            # Track performance
            processing_time = time.time() - start_time
            self.analytics_metrics.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "processing_time": processing_time,
                    "components_used": list(recommendations.keys()),
                }
            )

            if processing_time > 2.0:
                self.logger.warning(
                    f"Analytics processing exceeded 2s target: {processing_time:.2f}s"
                )

            recommendations["analytics_metadata"] = {
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat(),
                "confidence_level": self._calculate_overall_confidence(recommendations),
            }

            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating strategic recommendations: {e}")
            return self._get_fallback_recommendations()

    def _generate_strategic_insights(
        self, recommendations: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable strategic insights from analysis results"""
        insights = []

        # Framework insights
        if "framework" in recommendations:
            framework_rec = recommendations["framework"]
            if framework_rec.confidence_score > 0.8:
                insights.append(
                    f"High confidence recommendation: Apply {framework_rec.framework_name} "
                    f"framework (confidence: {framework_rec.confidence_score:.1%})"
                )
            elif framework_rec.confidence_score < 0.6:
                insights.append(
                    "Consider multiple framework approaches due to moderate confidence in recommendation"
                )

        # Initiative health insights
        if "initiative_health" in recommendations:
            health_scores = recommendations["initiative_health"]
            critical_initiatives = [
                h for h in health_scores if h.warning_level == "critical"
            ]
            if critical_initiatives:
                insights.append(
                    f"URGENT: {len(critical_initiatives)} initiative(s) require immediate attention"
                )

            declining_initiatives = [h for h in health_scores if h.trend == "declining"]
            if declining_initiatives:
                insights.append(
                    f"Monitor {len(declining_initiatives)} initiative(s) showing declining trends"
                )

        # Stakeholder engagement insights
        if "stakeholder_engagement" in recommendations:
            engagement_metrics = recommendations["stakeholder_engagement"]
            low_engagement = [s for s in engagement_metrics if s.engagement_score < 0.6]
            if low_engagement:
                insights.append(
                    f"Stakeholder engagement concern: {len(low_engagement)} stakeholder(s) "
                    "require increased attention"
                )

        return insights

    def _calculate_overall_confidence(self, recommendations: Dict[str, Any]) -> float:
        """Calculate overall confidence in recommendations"""
        confidences = []

        if "framework" in recommendations:
            confidences.append(recommendations["framework"].confidence_score)

        if "initiative_health" in recommendations:
            health_scores = recommendations["initiative_health"]
            avg_health = sum(h.overall_score for h in health_scores) / len(
                health_scores
            )
            confidences.append(avg_health)

        if "stakeholder_engagement" in recommendations:
            engagement_scores = recommendations["stakeholder_engagement"]
            avg_engagement = sum(s.engagement_score for s in engagement_scores) / len(
                engagement_scores
            )
            confidences.append(avg_engagement)

        return sum(confidences) / len(confidences) if confidences else 0.5

    def _get_fallback_recommendations(self) -> Dict[str, Any]:
        """Provide fallback recommendations when analysis fails"""
        return {
            "framework": FrameworkRecommendation(
                framework_name="wrap_framework",
                confidence_score=0.5,
                reasoning=["Fallback recommendation due to analysis error"],
                context_indicators=[],
                success_probability=0.7,
                estimated_impact="medium",
            ),
            "strategic_insights": [
                "Analytics temporarily unavailable - using default strategic guidance"
            ],
            "analytics_metadata": {
                "processing_time": 0.1,
                "timestamp": datetime.now().isoformat(),
                "confidence_level": 0.5,
                "status": "fallback",
            },
        }

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get analytics engine performance summary"""
        if not self.analytics_metrics:
            return {"status": "no_analytics_performed"}

        avg_processing_time = sum(
            m["processing_time"] for m in self.analytics_metrics
        ) / len(self.analytics_metrics)
        total_operations = len(self.analytics_metrics)

        return {
            "total_operations": total_operations,
            "average_processing_time": avg_processing_time,
            "target_compliance": avg_processing_time < 2.0,
            "last_operation": self.analytics_metrics[-1]["timestamp"],
            "components_usage": {
                "framework_analysis": sum(
                    1
                    for m in self.analytics_metrics
                    if "framework" in m["components_used"]
                ),
                "initiative_scoring": sum(
                    1
                    for m in self.analytics_metrics
                    if "initiative_health" in m["components_used"]
                ),
                "stakeholder_analysis": sum(
                    1
                    for m in self.analytics_metrics
                    if "stakeholder_engagement" in m["components_used"]
                ),
            },
        }
