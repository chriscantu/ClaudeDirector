"""
Learning Layer Memory

Pattern recognition, framework effectiveness, and adaptive optimization.
Provides learning intelligence for strategic decision improvement.
"""

from typing import Dict, List, Any, Optional, Tuple
import time
import logging
from dataclasses import dataclass, asdict
from collections import defaultdict
import statistics


@dataclass
class FrameworkUsage:
    """Framework usage tracking with effectiveness measurement"""

    framework_name: str
    usage_count: int
    total_effectiveness: float
    average_effectiveness: float
    contexts_used: List[str]
    success_rate: float
    last_used: float
    improvement_trend: float  # positive = improving, negative = declining


@dataclass
class DecisionPattern:
    """Strategic decision pattern with outcome tracking"""

    pattern_id: str
    decision_type: str
    context_keywords: List[str]
    frameworks_combination: List[str]
    stakeholders_involved: List[str]
    success_rate: float
    average_outcome_score: float
    usage_frequency: int
    pattern_confidence: float
    last_applied: float


class LearningLayerMemory:
    """
    Strategic learning and pattern recognition for adaptive intelligence

    Features:
    - Framework effectiveness tracking and optimization
    - Decision pattern recognition and recommendation
    - Personal strategic style learning and adaptation
    - Outcome-based learning and improvement suggestions
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize learning layer with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Learning configuration
        self.min_usage_for_pattern = self.config.get("min_usage_for_pattern", 3)
        self.effectiveness_threshold = self.config.get("effectiveness_threshold", 0.7)
        self.pattern_confidence_threshold = self.config.get("pattern_confidence", 0.6)

        # In-memory storage for Phase 1
        # Phase 2 will add SQLite persistent storage with pattern analytics
        self.framework_usage: Dict[str, FrameworkUsage] = {}
        self.decision_patterns: Dict[str, DecisionPattern] = {}
        self.learning_history: List[Dict[str, Any]] = []
        self.personal_style_profile: Dict[str, Any] = self._initialize_style_profile()

        self.logger.info("LearningLayerMemory initialized with pattern recognition")

    def update_framework_usage(
        self,
        framework_name: str,
        session_id: str,
        effectiveness_score: float = None,
        context: str = "",
    ) -> bool:
        """
        Update framework usage tracking with effectiveness measurement

        Args:
            framework_name: Name of the strategic framework used
            session_id: Session identifier
            effectiveness_score: Optional effectiveness rating (0.0-1.0)
            context: Context where framework was applied

        Returns:
            True if update successful, False otherwise
        """
        try:
            if framework_name not in self.framework_usage:
                # Initialize new framework tracking
                self.framework_usage[framework_name] = FrameworkUsage(
                    framework_name=framework_name,
                    usage_count=0,
                    total_effectiveness=0.0,
                    average_effectiveness=0.0,
                    contexts_used=[],
                    success_rate=0.0,
                    last_used=time.time(),
                    improvement_trend=0.0,
                )

            usage = self.framework_usage[framework_name]
            usage.usage_count += 1
            usage.last_used = time.time()

            # Add context if provided
            if context and context not in usage.contexts_used:
                usage.contexts_used.append(context)

            # Update effectiveness if provided
            if effectiveness_score is not None:
                usage.total_effectiveness += effectiveness_score
                usage.average_effectiveness = (
                    usage.total_effectiveness / usage.usage_count
                )

                # Update success rate (effectiveness > threshold)
                successful_uses = sum(
                    1
                    for score in self._get_framework_scores(framework_name)
                    if score > self.effectiveness_threshold
                )
                usage.success_rate = successful_uses / usage.usage_count

                # Calculate improvement trend
                usage.improvement_trend = self._calculate_improvement_trend(
                    framework_name
                )

            # Record learning event
            self._record_learning_event(
                {
                    "type": "framework_usage",
                    "framework": framework_name,
                    "session_id": session_id,
                    "effectiveness": effectiveness_score,
                    "context": context,
                    "timestamp": time.time(),
                }
            )

            self.logger.debug(f"Updated framework usage: {framework_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update framework usage: {e}")
            return False

    def record_decision_outcome(self, decision_data: Dict[str, Any]) -> bool:
        """
        Record strategic decision outcome for pattern learning

        Args:
            decision_data: Decision details with outcome information

        Returns:
            True if recording successful, False otherwise
        """
        try:
            # Extract pattern key from decision context
            pattern_key = self._generate_pattern_key(decision_data)

            if pattern_key not in self.decision_patterns:
                # Create new decision pattern
                self.decision_patterns[pattern_key] = DecisionPattern(
                    pattern_id=pattern_key,
                    decision_type=decision_data.get("type", "unknown"),
                    context_keywords=decision_data.get("context_keywords", []),
                    frameworks_combination=decision_data.get("frameworks", []),
                    stakeholders_involved=decision_data.get("stakeholders", []),
                    success_rate=0.0,
                    average_outcome_score=0.0,
                    usage_frequency=0,
                    pattern_confidence=0.0,
                    last_applied=time.time(),
                )

            pattern = self.decision_patterns[pattern_key]
            pattern.usage_frequency += 1
            pattern.last_applied = time.time()

            # Update outcome metrics
            outcome_score = decision_data.get("outcome_score", 0.5)
            total_outcomes = (
                pattern.average_outcome_score * (pattern.usage_frequency - 1)
                + outcome_score
            )
            pattern.average_outcome_score = total_outcomes / pattern.usage_frequency

            # Update success rate
            success_count = sum(
                1
                for event in self.learning_history
                if event.get("pattern_key") == pattern_key
                and event.get("outcome_score", 0) > self.effectiveness_threshold
            )
            pattern.success_rate = success_count / pattern.usage_frequency

            # Update pattern confidence based on usage frequency and consistency
            pattern.pattern_confidence = (
                min(1.0, pattern.usage_frequency / self.min_usage_for_pattern)
                * pattern.success_rate
            )

            # Record learning event
            self._record_learning_event(
                {
                    "type": "decision_outcome",
                    "pattern_key": pattern_key,
                    "outcome_score": outcome_score,
                    "decision_data": decision_data,
                    "timestamp": time.time(),
                }
            )

            # Update personal style profile
            self._update_personal_style(decision_data)

            return True

        except Exception as e:
            self.logger.error(f"Failed to record decision outcome: {e}")
            return False

    def get_skill_context(self, session_id: str = "default") -> Dict[str, Any]:
        """
        Get learning-based strategic skill context

        Args:
            session_id: Session identifier

        Returns:
            Learning context with framework recommendations and patterns
        """
        try:
            # Get top performing frameworks
            top_frameworks = self._get_top_performing_frameworks(5)

            # Get emerging patterns
            emerging_patterns = self._get_emerging_patterns()

            # Get improvement opportunities
            improvement_opportunities = self._get_improvement_opportunities()

            # Get personal style insights
            style_insights = self._get_style_insights()

            # Generate learning recommendations
            learning_recommendations = self._generate_learning_recommendations()

            return {
                "top_performing_frameworks": top_frameworks,
                "emerging_decision_patterns": emerging_patterns,
                "improvement_opportunities": improvement_opportunities,
                "personal_style_insights": style_insights,
                "learning_recommendations": learning_recommendations,
                "learning_metrics": self._calculate_learning_metrics(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get skill context: {e}")
            return {"top_performing_frameworks": [], "error": str(e)}

    def _initialize_style_profile(self) -> Dict[str, Any]:
        """Initialize personal strategic style profile"""
        return {
            "preferred_frameworks": [],
            "decision_speed": "medium",  # fast, medium, slow
            "collaboration_preference": "medium",  # high, medium, low
            "risk_tolerance": "medium",  # high, medium, low
            "analytical_depth": "medium",  # high, medium, low
            "stakeholder_focus": "balanced",  # high, medium, low
            "framework_diversity": 0.0,  # 0.0 to 1.0
            "adaptation_rate": 0.0,  # 0.0 to 1.0
            "consistency_score": 0.0,  # 0.0 to 1.0
        }

    def _generate_pattern_key(self, decision_data: Dict[str, Any]) -> str:
        """Generate unique pattern key from decision context"""
        decision_type = decision_data.get("type", "unknown")
        context_hash = hash(tuple(sorted(decision_data.get("context_keywords", []))))
        frameworks_hash = hash(tuple(sorted(decision_data.get("frameworks", []))))
        return f"{decision_type}_{abs(context_hash)}_{abs(frameworks_hash)}"

    def _get_framework_scores(self, framework_name: str) -> List[float]:
        """Get all effectiveness scores for a framework"""
        scores = []
        for event in self.learning_history:
            if (
                event.get("type") == "framework_usage"
                and event.get("framework") == framework_name
                and event.get("effectiveness") is not None
            ):
                scores.append(event["effectiveness"])
        return scores

    def _calculate_improvement_trend(self, framework_name: str) -> float:
        """Calculate improvement trend for framework usage"""
        scores = self._get_framework_scores(framework_name)
        if len(scores) < 3:
            return 0.0

        # Simple linear trend calculation
        recent_scores = scores[-5:]  # Last 5 uses
        early_scores = scores[:5] if len(scores) > 5 else scores[: len(scores) // 2]

        if not early_scores or not recent_scores:
            return 0.0

        recent_avg = statistics.mean(recent_scores)
        early_avg = statistics.mean(early_scores)

        return recent_avg - early_avg

    def _record_learning_event(self, event_data: Dict[str, Any]) -> None:
        """Record learning event for pattern analysis"""
        self.learning_history.append(event_data)

        # Limit history size
        if len(self.learning_history) > 10000:
            self.learning_history = self.learning_history[-10000:]

    def _update_personal_style(self, decision_data: Dict[str, Any]) -> None:
        """Update personal strategic style based on decision patterns"""
        style = self.personal_style_profile

        # Update preferred frameworks
        frameworks = decision_data.get("frameworks", [])
        for framework in frameworks:
            if framework not in style["preferred_frameworks"]:
                style["preferred_frameworks"].append(framework)

        # Update framework diversity
        unique_frameworks = len(set(f for f in style["preferred_frameworks"]))
        total_usage = sum(usage.usage_count for usage in self.framework_usage.values())
        style["framework_diversity"] = unique_frameworks / max(total_usage, 1)

        # Update collaboration preference based on stakeholder involvement
        stakeholder_count = len(decision_data.get("stakeholders", []))
        if stakeholder_count > 3:
            style["collaboration_preference"] = "high"
        elif stakeholder_count > 1:
            style["collaboration_preference"] = "medium"
        else:
            style["collaboration_preference"] = "low"

        # Update consistency score based on pattern usage
        pattern_usage_variance = (
            statistics.variance(
                [p.usage_frequency for p in self.decision_patterns.values()]
            )
            if len(self.decision_patterns) > 1
            else 0
        )
        style["consistency_score"] = max(0.0, 1.0 - (pattern_usage_variance / 10.0))

    def _get_top_performing_frameworks(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing frameworks by effectiveness"""
        frameworks = []
        for usage in self.framework_usage.values():
            if usage.usage_count >= self.min_usage_for_pattern:
                frameworks.append(
                    {
                        "framework": usage.framework_name,
                        "effectiveness": usage.average_effectiveness,
                        "success_rate": usage.success_rate,
                        "usage_count": usage.usage_count,
                        "improvement_trend": usage.improvement_trend,
                        "contexts": usage.contexts_used,
                    }
                )

        # Sort by effectiveness and return top performers
        frameworks.sort(key=lambda x: x["effectiveness"], reverse=True)
        return frameworks[:limit]

    def _get_emerging_patterns(self) -> List[Dict[str, Any]]:
        """Get emerging decision patterns with high confidence"""
        patterns = []
        for pattern in self.decision_patterns.values():
            if (
                pattern.pattern_confidence > self.pattern_confidence_threshold
                and pattern.usage_frequency >= self.min_usage_for_pattern
            ):
                patterns.append(
                    {
                        "pattern_type": pattern.decision_type,
                        "frameworks_combination": pattern.frameworks_combination,
                        "success_rate": pattern.success_rate,
                        "confidence": pattern.pattern_confidence,
                        "usage_frequency": pattern.usage_frequency,
                        "context_keywords": pattern.context_keywords,
                    }
                )

        # Sort by confidence and success rate
        patterns.sort(key=lambda x: (x["confidence"], x["success_rate"]), reverse=True)
        return patterns[:5]

    def _get_improvement_opportunities(self) -> List[Dict[str, Any]]:
        """Identify areas for strategic improvement"""
        opportunities = []

        # Frameworks with declining trends
        for usage in self.framework_usage.values():
            if usage.improvement_trend < -0.1 and usage.usage_count > 3:
                opportunities.append(
                    {
                        "type": "framework_decline",
                        "framework": usage.framework_name,
                        "issue": f"Effectiveness declining (trend: {usage.improvement_trend:.2f})",
                        "recommendation": "Consider alternative frameworks or additional training",
                    }
                )

        # Low-performing patterns
        for pattern in self.decision_patterns.values():
            if pattern.success_rate < 0.5 and pattern.usage_frequency > 2:
                opportunities.append(
                    {
                        "type": "pattern_improvement",
                        "pattern": pattern.decision_type,
                        "issue": f"Low success rate ({pattern.success_rate:.2f})",
                        "recommendation": "Analyze context factors and consider different approach",
                    }
                )

        # Framework diversity
        if self.personal_style_profile["framework_diversity"] < 0.3:
            opportunities.append(
                {
                    "type": "framework_diversity",
                    "issue": "Limited framework variety in use",
                    "recommendation": "Explore additional strategic frameworks for different contexts",
                }
            )

        return opportunities

    def _get_style_insights(self) -> List[Dict[str, Any]]:
        """Generate insights about personal strategic style"""
        style = self.personal_style_profile
        insights = []

        # Framework preference insight
        if len(style["preferred_frameworks"]) > 0:
            top_framework = (
                max(self.framework_usage.items(), key=lambda x: x[1].usage_count)[0]
                if self.framework_usage
                else None
            )
            if top_framework:
                insights.append(
                    {
                        "type": "framework_preference",
                        "insight": f"Strong preference for {top_framework}",
                        "usage_count": self.framework_usage[top_framework].usage_count,
                    }
                )

        # Collaboration style insight
        insights.append(
            {
                "type": "collaboration_style",
                "insight": f"Collaboration preference: {style['collaboration_preference']}",
                "recommendation": self._get_collaboration_recommendation(
                    style["collaboration_preference"]
                ),
            }
        )

        # Consistency insight
        if style["consistency_score"] > 0.8:
            insights.append(
                {
                    "type": "consistency",
                    "insight": "High consistency in strategic approach",
                    "recommendation": "Consider occasional experimentation with new frameworks",
                }
            )
        elif style["consistency_score"] < 0.4:
            insights.append(
                {
                    "type": "consistency",
                    "insight": "Variable strategic approach",
                    "recommendation": "Consider developing more consistent patterns for similar contexts",
                }
            )

        return insights

    def _get_collaboration_recommendation(self, preference: str) -> str:
        """Get recommendation based on collaboration preference"""
        recommendations = {
            "high": "Leverage your collaborative approach for complex multi-stakeholder decisions",
            "medium": "Balance collaborative input with decisive leadership",
            "low": "Consider increasing stakeholder engagement for better buy-in",
        }
        return recommendations.get(
            preference, "Adapt collaboration style to decision context"
        )

    def _generate_learning_recommendations(self) -> List[Dict[str, Any]]:
        """Generate specific learning recommendations"""
        recommendations = []

        # Framework mastery recommendations
        underused_frameworks = [
            usage
            for usage in self.framework_usage.values()
            if usage.usage_count < 3 and usage.average_effectiveness > 0.7
        ]

        if underused_frameworks:
            recommendations.append(
                {
                    "type": "framework_mastery",
                    "priority": "medium",
                    "message": f"{len(underused_frameworks)} high-potential frameworks underutilized",
                    "action": "Increase usage of effective but underused frameworks",
                }
            )

        # Pattern optimization recommendations
        low_confidence_patterns = [
            pattern
            for pattern in self.decision_patterns.values()
            if pattern.pattern_confidence < 0.5 and pattern.usage_frequency > 2
        ]

        if low_confidence_patterns:
            recommendations.append(
                {
                    "type": "pattern_optimization",
                    "priority": "high",
                    "message": f"{len(low_confidence_patterns)} decision patterns need optimization",
                    "action": "Analyze and refine low-confidence decision patterns",
                }
            )

        return recommendations

    def _calculate_learning_metrics(self) -> Dict[str, Any]:
        """Calculate overall learning progress metrics"""
        if not self.framework_usage:
            return {"status": "no_data"}

        total_frameworks = len(self.framework_usage)
        effective_frameworks = len(
            [
                u
                for u in self.framework_usage.values()
                if u.average_effectiveness > self.effectiveness_threshold
            ]
        )

        avg_effectiveness = (
            sum(u.average_effectiveness for u in self.framework_usage.values())
            / total_frameworks
        )
        avg_success_rate = (
            sum(u.success_rate for u in self.framework_usage.values())
            / total_frameworks
        )

        total_patterns = len(self.decision_patterns)
        confident_patterns = len(
            [
                p
                for p in self.decision_patterns.values()
                if p.pattern_confidence > self.pattern_confidence_threshold
            ]
        )

        return {
            "total_frameworks_used": total_frameworks,
            "effective_frameworks_count": effective_frameworks,
            "framework_effectiveness_rate": effective_frameworks / total_frameworks,
            "average_framework_effectiveness": avg_effectiveness,
            "average_success_rate": avg_success_rate,
            "total_decision_patterns": total_patterns,
            "confident_patterns_count": confident_patterns,
            "pattern_confidence_rate": confident_patterns / max(total_patterns, 1),
            "learning_events_count": len(self.learning_history),
            "overall_learning_score": (
                avg_effectiveness
                + avg_success_rate
                + (confident_patterns / max(total_patterns, 1))
            )
            / 3,
        }

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        import json

        framework_size = sum(
            len(json.dumps(asdict(usage), default=str).encode("utf-8"))
            for usage in self.framework_usage.values()
        )
        pattern_size = sum(
            len(json.dumps(asdict(pattern), default=str).encode("utf-8"))
            for pattern in self.decision_patterns.values()
        )
        history_size = sum(
            len(json.dumps(event).encode("utf-8")) for event in self.learning_history
        )
        style_size = len(json.dumps(self.personal_style_profile).encode("utf-8"))

        return {
            "framework_usage_count": len(self.framework_usage),
            "decision_patterns_count": len(self.decision_patterns),
            "learning_events_count": len(self.learning_history),
            "framework_memory_bytes": framework_size,
            "pattern_memory_bytes": pattern_size,
            "history_memory_bytes": history_size,
            "style_memory_bytes": style_size,
            "total_memory_bytes": framework_size
            + pattern_size
            + history_size
            + style_size,
            "total_memory_mb": (
                framework_size + pattern_size + history_size + style_size
            )
            / (1024 * 1024),
        }
