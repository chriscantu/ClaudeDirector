#!/usr/bin/env python3
"""
Analytics Processor - Sequential Thinking Phase 4.1.2

Consolidated analytics processing engine extracting logic from:
- FrameworkPatternAnalyzer (511 lines)
- InitiativeHealthScorer (372 lines)
- StakeholderEngagementAnalyzer (101 lines)

Total consolidation: ~984 lines of complex analytics logic
Target: Unified processor following Story 4.2 proven methodology
"""

import logging
import time
import re
import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import math

from .analytics_config import (
    PRIORITY_LEVELS,
    CONFIDENCE_THRESHOLDS,
    SCORE_THRESHOLDS,
    FRAMEWORK_KEYWORDS,
    FRAMEWORK_CONTEXT_PATTERNS,
    FRAMEWORK_SUCCESS_CONTEXTS,
    FRAMEWORK_SUCCESS_RATES,
    FRAMEWORK_BASE_PROBABILITIES,
    FRAMEWORK_DESCRIPTIONS,
    SENTIMENT_SCORES,
    INFLUENCE_WEIGHTS,
    STATUS_SCORES,
    RESOURCE_STATUS_SCORES,
    HIGH_IMPACT_KEYWORDS,
    MEDIUM_IMPACT_KEYWORDS,
    COMPLEXITY_INDICATORS,
    URGENCY_INDICATORS,
    SCORING_WEIGHTS,
    PERFORMANCE_TARGETS,
    WARNING_LEVEL_THRESHOLDS,
    LIMITS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES,
    DESCRIPTION_TEMPLATES,
    get_framework_config,
    get_scoring_config,
    get_performance_config,
)

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


class AnalyticsProcessor:
    """
    🏗️ Sequential Thinking Phase 4.1.2: Unified Analytics Processor

    Consolidates all complex analytics logic from multiple analyzer classes:
    - Framework pattern analysis and ML-like predictions
    - Initiative health scoring with multi-dimensional assessment
    - Stakeholder engagement analysis and trend detection

    Follows proven Story 4.2 methodology for aggressive consolidation
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """🏗️ Initialize unified analytics processor with consolidated configuration"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__ + ".AnalyticsProcessor")

        # Framework analysis configuration
        self.framework_config = self.config.get("framework_analyzer", {})
        self.framework_patterns = self._initialize_framework_patterns()
        self.success_metrics = self._initialize_success_metrics()
        self.training_data = self._load_training_data()

        # Initiative scoring configuration
        self.scoring_config = self.config.get("initiative_scorer", {})

        # Stakeholder analysis configuration
        self.stakeholder_config = self.config.get("stakeholder_analyzer", {})

        self.logger.info(
            "🏗️ AnalyticsProcessor initialized with unified analytics capabilities"
        )

    # ========================================================================
    # FRAMEWORK PATTERN ANALYSIS (Consolidated from FrameworkPatternAnalyzer)
    # ========================================================================

    def predict_optimal_framework(
        self,
        context: str,
        stakeholders: List[str] = None,
        initiatives: List[str] = None,
    ) -> FrameworkRecommendation:
        """🏗️ Predict optimal framework using consolidated ML-like analysis"""
        start_time = time.time()

        try:
            # Extract context indicators
            indicators = self._extract_context_indicators(context)

            # Calculate framework scores using consolidated ML approach
            scores = self._calculate_ml_framework_scores(
                context, stakeholders or [], initiatives or []
            )

            # Select best framework
            framework_name, confidence = self._select_best_framework(scores)

            # Generate comprehensive reasoning
            reasoning = self._generate_reasoning(framework_name, indicators)

            # Calculate success probability
            success_prob = self._calculate_success_probability(
                framework_name, context, stakeholders or []
            )

            # Estimate impact
            impact = self._estimate_impact(framework_name, context)

            processing_time = time.time() - start_time
            if processing_time > 1.0:
                self.logger.warning(
                    f"Framework prediction exceeded 1s: {processing_time:.2f}s"
                )

            return FrameworkRecommendation(
                framework_name=framework_name,
                confidence_score=confidence,
                reasoning=reasoning,
                context_indicators=indicators,
                success_probability=success_prob,
                estimated_impact=impact,
            )

        except Exception as e:
            self.logger.error(f"Framework prediction error: {e}")
            return self._get_fallback_framework_recommendation()

    def _extract_context_indicators(self, context: str) -> List[str]:
        """🏗️ Extract framework context indicators from text"""
        indicators = []
        context_lower = context.lower()

        # Check for framework-specific keywords
        for framework, keywords in FRAMEWORK_KEYWORDS.items():
            keyword_matches = sum(1 for keyword in keywords if keyword in context_lower)
            if keyword_matches >= 2:
                indicators.append(f"{framework}_keywords_{keyword_matches}")

        # Check for context patterns
        for pattern_name, pattern_regex in FRAMEWORK_CONTEXT_PATTERNS.items():
            if re.search(pattern_regex, context, re.IGNORECASE):
                indicators.append(f"pattern_{pattern_name}")

        # Analyze complexity and urgency
        complexity_score = sum(
            1 for indicator in COMPLEXITY_INDICATORS if indicator in context_lower
        )
        urgency_score = sum(
            1 for indicator in URGENCY_INDICATORS if indicator in context_lower
        )

        if complexity_score > 2:
            indicators.append("high_complexity")
        if urgency_score > 1:
            indicators.append("urgent_timeline")

        return indicators[:10]  # Limit for performance

    def _initialize_framework_patterns(self) -> Dict[str, Any]:
        """🏗️ Initialize framework patterns for analysis"""
        return {
            "team_topologies": {
                "keywords": [
                    "team",
                    "cognitive load",
                    "conway's law",
                    "stream",
                    "platform",
                ],
                "context_patterns": [
                    "team.*structure",
                    "organizational.*design",
                    "platform.*team",
                ],
                "success_indicators": [
                    "reduced handoffs",
                    "faster delivery",
                    "clear ownership",
                ],
            },
            "good_strategy_bad_strategy": {
                "keywords": ["strategy", "kernel", "coherent", "advantage", "focus"],
                "context_patterns": ["strategic.*planning", "competitive.*advantage"],
                "success_indicators": [
                    "clear direction",
                    "resource focus",
                    "competitive edge",
                ],
            },
            "crucial_conversations": {
                "keywords": [
                    "difficult",
                    "conversation",
                    "stakeholder",
                    "alignment",
                    "conflict",
                ],
                "context_patterns": ["stakeholder.*alignment", "difficult.*discussion"],
                "success_indicators": [
                    "improved communication",
                    "stakeholder buy-in",
                    "conflict resolution",
                ],
            },
            "capital_allocation": {
                "keywords": ["budget", "investment", "roi", "resource", "allocation"],
                "context_patterns": ["resource.*allocation", "investment.*decision"],
                "success_indicators": [
                    "optimized spending",
                    "clear roi",
                    "strategic alignment",
                ],
            },
        }

    def _initialize_success_metrics(self) -> Dict[str, Any]:
        """🏗️ Initialize success metrics for framework analysis"""
        return {
            "accuracy_target": 0.85,
            "confidence_threshold": 0.6,
            "processing_time_target": 1.0,
            "min_indicators": 2,
        }

    def _load_training_data(self) -> List[Dict[str, Any]]:
        """🏗️ Load consolidated training data for framework analysis"""
        # Simplified training data - would be loaded from real data in production
        return [
            {
                "context": "team structure optimization",
                "framework": "team_topologies",
                "success": True,
            },
            {
                "context": "strategic planning initiative",
                "framework": "good_strategy_bad_strategy",
                "success": True,
            },
            {
                "context": "stakeholder alignment challenge",
                "framework": "crucial_conversations",
                "success": True,
            },
            {
                "context": "budget optimization project",
                "framework": "capital_allocation",
                "success": True,
            },
        ]

    def _calculate_ml_framework_scores(
        self, context: str, stakeholders: List[str], initiatives: List[str]
    ) -> Dict[str, float]:
        """🏗️ Calculate framework scores using consolidated ML approach"""
        scores = {}

        # Extract features from context
        features = self._extract_context_features(context)

        # Score each framework
        for framework in FRAMEWORK_BASE_PROBABILITIES.keys():
            # Base probability
            base_score = FRAMEWORK_BASE_PROBABILITIES.get(framework, 0.1)

            # Context feature matching
            feature_score = self._score_framework_features(framework, features)

            # Stakeholder and initiative context
            context_score = self._score_framework_context(
                framework, stakeholders, initiatives
            )

            # Combine scores with weights
            final_score = base_score * 0.3 + feature_score * 0.5 + context_score * 0.2

            scores[framework] = min(final_score, 1.0)

        return scores

    def _extract_context_features(self, context: str) -> Dict[str, float]:
        """🏗️ Extract quantitative features from context"""
        features = {}
        context_lower = context.lower()

        # Keyword density features
        for framework, keywords in FRAMEWORK_KEYWORDS.items():
            keyword_count = sum(1 for keyword in keywords if keyword in context_lower)
            features[f"{framework}_density"] = keyword_count / max(len(keywords), 1)

        # Text complexity features
        features["complexity"] = len(
            [w for w in COMPLEXITY_INDICATORS if w in context_lower]
        ) / len(COMPLEXITY_INDICATORS)
        features["urgency"] = len(
            [w for w in URGENCY_INDICATORS if w in context_lower]
        ) / len(URGENCY_INDICATORS)

        # Length and structure features
        features["text_length"] = min(len(context) / 1000, 1.0)  # Normalized
        features["sentence_count"] = min(len(context.split(".")), 20) / 20  # Normalized

        return features

    def _score_framework_features(
        self, framework: str, features: Dict[str, float]
    ) -> float:
        """🏗️ Score framework match based on extracted features"""
        framework_key = f"{framework}_density"
        if framework_key in features:
            return features[framework_key]
        return 0.1  # Low baseline score

    def _score_framework_context(
        self, framework: str, stakeholders: List[str], initiatives: List[str]
    ) -> float:
        """🏗️ Score framework based on stakeholder and initiative context"""
        score = 0.5  # Baseline

        # Stakeholder context scoring
        if stakeholders:
            stakeholder_context = " ".join(stakeholders).lower()
            if "executive" in stakeholder_context and framework in [
                "good_strategy_bad_strategy",
                "capital_allocation",
            ]:
                score += 0.2
            if "team" in stakeholder_context and framework == "team_topologies":
                score += 0.2

        # Initiative context scoring
        if initiatives:
            initiative_context = " ".join(initiatives).lower()
            if (
                "strategic" in initiative_context
                and framework == "good_strategy_bad_strategy"
            ):
                score += 0.1
            if "team" in initiative_context and framework == "team_topologies":
                score += 0.1

        return min(score, 1.0)

    def _select_best_framework(self, scores: Dict[str, float]) -> Tuple[str, float]:
        """🏗️ Select best framework from consolidated scores"""
        if not scores:
            return "good_strategy_bad_strategy", 0.5  # Fallback

        best_framework = max(scores.items(), key=lambda x: x[1])
        return best_framework[0], best_framework[1]

    def _generate_reasoning(self, framework: str, indicators: List[str]) -> List[str]:
        """🏗️ Generate reasoning for framework recommendation"""
        reasoning = []

        # Framework-specific reasoning
        framework_desc = FRAMEWORK_DESCRIPTIONS.get(framework, "Strategic framework")
        reasoning.append(f"Selected {framework_desc} based on context analysis")

        # Indicator-based reasoning
        if indicators:
            reasoning.append(f"Key indicators detected: {', '.join(indicators[:3])}")

        # Pattern-based reasoning
        if any("pattern_" in ind for ind in indicators):
            reasoning.append("Context patterns suggest structured approach needed")

        if any("complexity" in ind for ind in indicators):
            reasoning.append(
                "High complexity detected - framework guidance recommended"
            )

        return reasoning[:5]  # Limit for readability

    def _calculate_success_probability(
        self, framework: str, context: str, stakeholders: List[str]
    ) -> float:
        """🏗️ Calculate success probability for framework application"""
        base_prob = FRAMEWORK_SUCCESS_RATES.get(framework, 0.7)

        # Adjust based on context complexity
        context_lower = context.lower()
        complexity_adjustment = 0

        if any(indicator in context_lower for indicator in COMPLEXITY_INDICATORS):
            complexity_adjustment -= 0.1  # More complex = slightly lower success rate

        if any(indicator in context_lower for indicator in URGENCY_INDICATORS):
            complexity_adjustment -= 0.05  # Urgent = slightly lower success rate

        # Stakeholder adjustment
        stakeholder_adjustment = 0
        if len(stakeholders) > 5:
            stakeholder_adjustment -= (
                0.05  # Many stakeholders = coordination complexity
            )
        elif len(stakeholders) < 2:
            stakeholder_adjustment += 0.05  # Few stakeholders = easier alignment

        final_prob = base_prob + complexity_adjustment + stakeholder_adjustment
        return max(0.1, min(final_prob, 0.95))  # Bound between 10% and 95%

    def _estimate_impact(self, framework: str, context: str) -> str:
        """🏗️ Estimate impact level for framework application"""
        context_lower = context.lower()

        # High impact indicators
        high_impact_count = sum(
            1 for keyword in HIGH_IMPACT_KEYWORDS if keyword in context_lower
        )
        medium_impact_count = sum(
            1 for keyword in MEDIUM_IMPACT_KEYWORDS if keyword in context_lower
        )

        if high_impact_count >= 2 or "strategic" in context_lower:
            return "high"
        elif medium_impact_count >= 2 or "team" in context_lower:
            return "medium"
        else:
            return "low"

    def _get_fallback_framework_recommendation(self) -> FrameworkRecommendation:
        """🏗️ Get fallback framework recommendation for error cases"""
        return FrameworkRecommendation(
            framework_name="good_strategy_bad_strategy",
            confidence_score=0.5,
            reasoning=["Fallback recommendation due to analysis error"],
            context_indicators=["fallback_mode"],
            success_probability=0.6,
            estimated_impact="medium",
        )

    # ========================================================================
    # INITIATIVE HEALTH SCORING (Consolidated from InitiativeHealthScorer)
    # ========================================================================

    def calculate_initiative_health_score(
        self, initiative_data: Dict[str, Any]
    ) -> InitiativeHealthScore:
        """🏗️ Calculate comprehensive initiative health score"""
        try:
            initiative_id = initiative_data.get("id", "unknown")

            # Multi-dimensional scoring
            progress_score = self._calculate_progress_score(initiative_data)
            stakeholder_score = self._calculate_stakeholder_score(initiative_data)
            timeline_score = self._calculate_timeline_score(initiative_data)
            resource_score = self._calculate_resource_score(initiative_data)

            # Weighted overall score
            weights = SCORING_WEIGHTS
            overall_score = (
                progress_score * weights["progress"]
                + stakeholder_score * weights["stakeholder"]
                + timeline_score * weights["timeline"]
                + resource_score * weights["resource"]
            )

            # Risk and success factor analysis
            risk_factors = self._identify_risk_factors(initiative_data, overall_score)
            success_indicators = self._identify_success_indicators(initiative_data)

            # Trend analysis
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
            self.logger.error(f"Initiative health scoring error: {e}")
            return self._get_fallback_health_score(initiative_data.get("id", "unknown"))

    def _calculate_progress_score(self, data: Dict[str, Any]) -> float:
        """🏗️ Calculate progress dimension score"""
        try:
            # Progress indicators
            completed_milestones = data.get("completed_milestones", 0)
            total_milestones = data.get("total_milestones", 1)
            progress_percentage = data.get("progress_percentage", 0)

            # Calculate milestone completion rate
            milestone_completion = completed_milestones / max(total_milestones, 1)

            # Combine progress indicators
            progress_score = (
                milestone_completion * 0.6 + (progress_percentage / 100) * 0.4
            )

            # Apply performance adjustments
            if data.get("ahead_of_schedule", False):
                progress_score *= 1.2
            elif data.get("behind_schedule", False):
                progress_score *= 0.8

            return min(progress_score, 1.0)

        except Exception:
            return self._fallback_progress_assessment(data)

    def _calculate_stakeholder_score(self, data: Dict[str, Any]) -> float:
        """🏗️ Calculate stakeholder dimension score"""
        try:
            # Stakeholder engagement metrics
            stakeholder_satisfaction = data.get("stakeholder_satisfaction", 0.5)
            communication_frequency = data.get("communication_frequency", "medium")
            conflict_resolution = data.get("conflicts_resolved", 0)
            total_conflicts = data.get("total_conflicts", 0)

            # Convert communication frequency to score
            comm_scores = {"low": 0.3, "medium": 0.6, "high": 0.9}
            comm_score = comm_scores.get(communication_frequency, 0.6)

            # Conflict resolution rate
            if total_conflicts > 0:
                conflict_score = conflict_resolution / total_conflicts
            else:
                conflict_score = 1.0  # No conflicts is good

            # Combine stakeholder metrics
            stakeholder_score = (
                stakeholder_satisfaction * 0.5 + comm_score * 0.3 + conflict_score * 0.2
            )

            return min(stakeholder_score, 1.0)

        except Exception:
            return self._fallback_stakeholder_assessment(data)

    def _calculate_timeline_score(self, data: Dict[str, Any]) -> float:
        """🏗️ Calculate timeline dimension score"""
        try:
            # Timeline metrics
            original_deadline = data.get("original_deadline")
            current_deadline = data.get("current_deadline")
            completion_date = data.get("estimated_completion")

            if not all([original_deadline, current_deadline, completion_date]):
                return self._fallback_timeline_assessment(data)

            # Parse dates (simplified - would use proper date parsing in production)
            deadline_changes = data.get("deadline_changes", 0)
            schedule_variance = data.get("schedule_variance_days", 0)

            # Calculate timeline stability
            stability_score = max(0, 1.0 - (deadline_changes * 0.1))

            # Calculate schedule performance
            if schedule_variance <= 0:  # On time or ahead
                schedule_score = 1.0
            elif schedule_variance <= 7:  # Within a week
                schedule_score = 0.8
            elif schedule_variance <= 30:  # Within a month
                schedule_score = 0.6
            else:  # Significantly delayed
                schedule_score = 0.3

            # Combine timeline metrics
            timeline_score = stability_score * 0.4 + schedule_score * 0.6

            return min(timeline_score, 1.0)

        except Exception:
            return self._fallback_timeline_assessment(data)

    def _calculate_resource_score(self, data: Dict[str, Any]) -> float:
        """🏗️ Calculate resource dimension score"""
        try:
            # Resource metrics
            budget_utilization = data.get("budget_utilization", 0.5)
            team_capacity = data.get("team_capacity_utilization", 0.8)
            resource_conflicts = data.get("resource_conflicts", 0)
            budget_variance = data.get("budget_variance_percent", 0)

            # Budget performance
            if abs(budget_variance) <= 5:  # Within 5%
                budget_score = 1.0
            elif abs(budget_variance) <= 15:  # Within 15%
                budget_score = 0.8
            else:  # Significant variance
                budget_score = 0.5

            # Team capacity score
            if 0.7 <= team_capacity <= 0.9:  # Optimal range
                capacity_score = 1.0
            elif team_capacity < 0.7:  # Underutilized
                capacity_score = 0.7
            else:  # Overutilized
                capacity_score = 0.6

            # Resource conflict penalty
            conflict_penalty = min(resource_conflicts * 0.1, 0.3)

            # Combine resource metrics
            resource_score = (
                budget_score * 0.4
                + capacity_score * 0.4
                + (1.0 - conflict_penalty) * 0.2
            )

            return min(resource_score, 1.0)

        except Exception:
            return self._fallback_resource_assessment(data)

    def _fallback_progress_assessment(self, data: Dict[str, Any]) -> float:
        """🏗️ Fallback progress assessment when data is incomplete"""
        # Simple heuristic based on available data
        if data.get("status") == "completed":
            return 1.0
        elif data.get("status") == "in_progress":
            return 0.6
        elif data.get("status") == "not_started":
            return 0.1
        return 0.5

    def _fallback_stakeholder_assessment(self, data: Dict[str, Any]) -> float:
        """🏗️ Fallback stakeholder assessment when data is incomplete"""
        # Simple heuristic
        if data.get("stakeholder_issues", []):
            return 0.4
        return 0.6

    def _fallback_timeline_assessment(self, data: Dict[str, Any]) -> float:
        """🏗️ Fallback timeline assessment when data is incomplete"""
        # Simple heuristic
        if data.get("behind_schedule", False):
            return 0.4
        elif data.get("ahead_of_schedule", False):
            return 0.9
        return 0.6

    def _fallback_resource_assessment(self, data: Dict[str, Any]) -> float:
        """🏗️ Fallback resource assessment when data is incomplete"""
        # Simple heuristic
        if data.get("over_budget", False):
            return 0.4
        elif data.get("under_budget", False):
            return 0.8
        return 0.6

    def _identify_risk_factors(
        self, data: Dict[str, Any], overall_score: float
    ) -> List[str]:
        """🏗️ Identify risk factors for initiative"""
        risks = []

        if overall_score < 0.4:
            risks.append("Low overall health score")

        if data.get("behind_schedule", False):
            risks.append("Behind schedule")

        if data.get("over_budget", False):
            risks.append("Budget overrun")

        if data.get("stakeholder_issues", []):
            risks.append("Stakeholder alignment issues")

        if data.get("resource_conflicts", 0) > 2:
            risks.append("Resource contention")

        if data.get("deadline_changes", 0) > 3:
            risks.append("Timeline instability")

        return risks[:5]  # Limit for readability

    def _identify_success_indicators(self, data: Dict[str, Any]) -> List[str]:
        """🏗️ Identify success indicators for initiative"""
        successes = []

        if data.get("ahead_of_schedule", False):
            successes.append("Ahead of schedule")

        if data.get("under_budget", False):
            successes.append("Under budget")

        if data.get("stakeholder_satisfaction", 0) > 0.8:
            successes.append("High stakeholder satisfaction")

        if data.get("team_morale", 0) > 0.8:
            successes.append("High team morale")

        if data.get("quality_metrics", 0) > 0.8:
            successes.append("High quality delivery")

        return successes[:5]  # Limit for readability

    def _determine_trend(self, data: Dict[str, Any]) -> str:
        """🏗️ Determine initiative trend"""
        # Simple trend analysis based on recent data
        recent_scores = data.get("recent_health_scores", [])

        if len(recent_scores) >= 2:
            if recent_scores[-1] > recent_scores[-2]:
                return "improving"
            elif recent_scores[-1] < recent_scores[-2]:
                return "declining"

        return "stable"

    def _determine_warning_level(self, score: float, risks: List[str]) -> str:
        """🏗️ Determine warning level based on score and risks"""
        if score < 0.3 or len(risks) >= 4:
            return "critical"
        elif score < 0.5 or len(risks) >= 2:
            return "concern"
        elif score < 0.7 or len(risks) >= 1:
            return "watch"
        else:
            return "none"

    def _predict_outcome(self, score: float, trend: str) -> str:
        """🏗️ Predict initiative outcome"""
        if trend == "improving" and score > 0.6:
            return "likely_success"
        elif trend == "declining" or score < 0.4:
            return "at_risk"
        elif score > 0.7:
            return "on_track"
        else:
            return "uncertain"

    def _get_fallback_health_score(self, initiative_id: str) -> InitiativeHealthScore:
        """🏗️ Get fallback health score for error cases"""
        return InitiativeHealthScore(
            initiative_id=initiative_id,
            overall_score=0.5,
            risk_factors=["Data unavailable"],
            success_indicators=["Analysis fallback"],
            trend="stable",
            predicted_outcome="uncertain",
            warning_level="watch",
        )

    # ========================================================================
    # STAKEHOLDER ENGAGEMENT ANALYSIS (Consolidated from StakeholderEngagementAnalyzer)
    # ========================================================================

    def analyze_stakeholder_engagement(
        self, stakeholder_id: str, interaction_history: List[Dict[str, Any]]
    ) -> StakeholderEngagementMetrics:
        """🏗️ Analyze stakeholder engagement with consolidated metrics"""
        try:
            # Calculate engagement dimensions
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
            self.logger.error(f"Stakeholder engagement analysis error: {e}")
            return self._get_fallback_engagement_metrics(stakeholder_id)

    def _calculate_engagement_score(self, history: List[Dict[str, Any]]) -> float:
        """🏗️ Calculate overall engagement score"""
        if not history:
            return 0.3  # Low baseline for no history

        # Engagement metrics
        total_interactions = len(history)
        recent_interactions = len(
            [h for h in history[-30:] if h]
        )  # Last 30 interactions
        response_rate = sum(1 for h in history if h.get("responded", False)) / max(
            total_interactions, 1
        )

        # Engagement score calculation
        activity_score = min(recent_interactions / 10, 1.0)  # Normalize to 0-1
        response_score = response_rate
        consistency_score = min(total_interactions / 50, 1.0)  # Long-term engagement

        engagement_score = (
            activity_score * 0.4 + response_score * 0.4 + consistency_score * 0.2
        )
        return min(engagement_score, 1.0)

    def _calculate_communication_frequency(
        self, history: List[Dict[str, Any]]
    ) -> float:
        """🏗️ Calculate communication frequency score"""
        if not history:
            return 0.1

        # Calculate interactions per time period
        recent_history = history[
            -30:
        ]  # Last 30 interactions as proxy for recent period
        frequency = len(recent_history) / max(30, 1)  # Interactions per period

        return min(frequency, 1.0)

    def _analyze_sentiment_trend(self, history: List[Dict[str, Any]]) -> str:
        """🏗️ Analyze sentiment trend over time"""
        if not history:
            return "neutral"

        # Simple sentiment analysis based on available sentiment scores
        recent_sentiments = [h.get("sentiment_score", 0.5) for h in history[-10:]]

        if len(recent_sentiments) >= 2:
            avg_recent = sum(recent_sentiments) / len(recent_sentiments)
            if avg_recent > 0.6:
                return "positive"
            elif avg_recent < 0.4:
                return "negative"

        return "neutral"

    def _assess_influence_level(
        self, stakeholder_id: str, history: List[Dict[str, Any]]
    ) -> str:
        """🏗️ Assess stakeholder influence level"""
        # Simple heuristic based on stakeholder ID and interaction patterns
        stakeholder_lower = stakeholder_id.lower()

        if any(
            title in stakeholder_lower for title in ["ceo", "vp", "svp", "director"]
        ):
            return "high"
        elif any(title in stakeholder_lower for title in ["manager", "lead", "senior"]):
            return "medium"
        else:
            return "low"

    def _assess_collaboration_effectiveness(
        self, history: List[Dict[str, Any]]
    ) -> float:
        """🏗️ Assess collaboration effectiveness"""
        if not history:
            return 0.5  # Neutral baseline

        # Collaboration indicators
        positive_interactions = sum(
            1 for h in history if h.get("sentiment_score", 0.5) > 0.6
        )
        total_interactions = len(history)
        collaborative_actions = sum(
            1 for h in history if h.get("collaborative_action", False)
        )

        # Effectiveness score
        sentiment_effectiveness = positive_interactions / max(total_interactions, 1)
        action_effectiveness = collaborative_actions / max(total_interactions, 1)

        effectiveness = sentiment_effectiveness * 0.6 + action_effectiveness * 0.4
        return min(effectiveness, 1.0)

    def _identify_engagement_risks(self, history: List[Dict[str, Any]]) -> List[str]:
        """🏗️ Identify engagement risk indicators"""
        risks = []

        if not history:
            risks.append("No interaction history")
            return risks

        # Recent interaction analysis
        recent_history = history[-10:]

        # Low response rate
        response_rate = sum(
            1 for h in recent_history if h.get("responded", False)
        ) / max(len(recent_history), 1)
        if response_rate < 0.3:
            risks.append("Low response rate")

        # Negative sentiment trend
        negative_sentiments = sum(
            1 for h in recent_history if h.get("sentiment_score", 0.5) < 0.4
        )
        if negative_sentiments > len(recent_history) * 0.5:
            risks.append("Negative sentiment trend")

        # Long gaps in communication
        if len(recent_history) < 3:
            risks.append("Infrequent communication")

        return risks[:3]  # Limit for readability

    def _get_fallback_engagement_metrics(
        self, stakeholder_id: str
    ) -> StakeholderEngagementMetrics:
        """🏗️ Get fallback engagement metrics for error cases"""
        return StakeholderEngagementMetrics(
            stakeholder_id=stakeholder_id,
            engagement_score=0.5,
            communication_frequency=0.5,
            sentiment_trend="neutral",
            influence_level="medium",
            collaboration_effectiveness=0.5,
            risk_indicators=["Analysis unavailable"],
        )
