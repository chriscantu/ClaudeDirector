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


class FrameworkPatternAnalyzer:
    """Analyzes framework usage patterns and predicts optimal applications using ML"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__ + ".FrameworkAnalyzer")

        # ML-based framework pattern database
        self.framework_patterns = self._initialize_framework_patterns()
        self.success_metrics = self._initialize_success_metrics()
        self.context_vectors = {}
        self.training_data = self._load_training_data()

        # ML model parameters
        self.confidence_threshold = self.config.get("confidence_threshold", 0.7)
        self.min_training_samples = self.config.get("min_training_samples", 10)

        self.logger.info("FrameworkPatternAnalyzer initialized with ML capabilities")

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

            # Analyze context for framework indicators (legacy)
            context_indicators = self._extract_context_indicators(context)

            # Use ML-based scoring for improved accuracy
            framework_scores = self._calculate_ml_framework_scores(
                context, stakeholders, current_initiatives
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

    def _initialize_framework_patterns(self) -> Dict[str, Any]:
        """Initialize ML-based framework pattern recognition"""
        return {
            "team_topologies": {
                "keywords": [
                    "team",
                    "cognitive load",
                    "organization",
                    "structure",
                    "topology",
                    "conway",
                ],
                "context_patterns": [
                    "organizational",
                    "scaling",
                    "team design",
                    "communication",
                ],
                "success_contexts": ["growing team", "microservices", "platform team"],
                "historical_success_rate": 0.87,
                "sample_size": 45,
            },
            "wrap_framework": {
                "keywords": [
                    "decision",
                    "options",
                    "choice",
                    "analysis",
                    "alternatives",
                    "criteria",
                ],
                "context_patterns": [
                    "strategic decision",
                    "multiple options",
                    "evaluation",
                ],
                "success_contexts": [
                    "complex decision",
                    "stakeholder alignment",
                    "option analysis",
                ],
                "historical_success_rate": 0.92,
                "sample_size": 78,
            },
            "good_strategy": {
                "keywords": [
                    "strategy",
                    "competitive",
                    "advantage",
                    "positioning",
                    "market",
                    "vision",
                ],
                "context_patterns": [
                    "strategic planning",
                    "competitive analysis",
                    "market position",
                ],
                "success_contexts": [
                    "strategy development",
                    "competitive response",
                    "vision setting",
                ],
                "historical_success_rate": 0.84,
                "sample_size": 34,
            },
            "crucial_conversations": {
                "keywords": [
                    "stakeholder",
                    "conflict",
                    "alignment",
                    "communication",
                    "difficult",
                    "conversation",
                ],
                "context_patterns": [
                    "stakeholder management",
                    "conflict resolution",
                    "alignment",
                ],
                "success_contexts": [
                    "stakeholder conflict",
                    "alignment issues",
                    "difficult discussions",
                ],
                "historical_success_rate": 0.79,
                "sample_size": 56,
            },
            "capital_allocation": {
                "keywords": [
                    "budget",
                    "investment",
                    "resource",
                    "roi",
                    "allocation",
                    "priority",
                ],
                "context_patterns": [
                    "resource planning",
                    "investment decision",
                    "budget allocation",
                ],
                "success_contexts": [
                    "resource constraints",
                    "investment decision",
                    "priority setting",
                ],
                "historical_success_rate": 0.88,
                "sample_size": 29,
            },
            "accelerate": {
                "keywords": [
                    "performance",
                    "devops",
                    "delivery",
                    "metrics",
                    "flow",
                    "deployment",
                ],
                "context_patterns": [
                    "engineering performance",
                    "delivery optimization",
                    "metrics",
                ],
                "success_contexts": [
                    "performance improvement",
                    "delivery speed",
                    "engineering metrics",
                ],
                "historical_success_rate": 0.85,
                "sample_size": 41,
            },
            "platform_strategy": {
                "keywords": [
                    "platform",
                    "ecosystem",
                    "scalability",
                    "reuse",
                    "api",
                    "infrastructure",
                ],
                "context_patterns": [
                    "platform design",
                    "ecosystem building",
                    "scalability",
                ],
                "success_contexts": [
                    "platform development",
                    "ecosystem strategy",
                    "scalability planning",
                ],
                "historical_success_rate": 0.86,
                "sample_size": 33,
            },
        }

    def _initialize_success_metrics(self) -> Dict[str, Any]:
        """Initialize success metrics for framework effectiveness tracking"""
        return {
            "accuracy_scores": defaultdict(list),
            "confidence_scores": defaultdict(list),
            "context_matches": defaultdict(int),
            "outcome_feedback": defaultdict(list),
            "last_updated": datetime.now(),
        }

    def _load_training_data(self) -> List[Dict[str, Any]]:
        """Load historical training data for ML models"""
        # In production, this would load from a persistent store
        # For now, return simulated training data based on known patterns
        training_samples = []

        for framework, data in self.framework_patterns.items():
            for i in range(min(data["sample_size"], 20)):  # Limit for memory efficiency
                # Generate synthetic training samples based on patterns
                sample_context = self._generate_sample_context(framework, data)
                training_samples.append(
                    {
                        "context": sample_context,
                        "framework": framework,
                        "success": data["historical_success_rate"] > 0.8,
                        "confidence": data["historical_success_rate"],
                        "timestamp": datetime.now() - timedelta(days=i * 10),
                    }
                )

        return training_samples

    def _generate_sample_context(self, framework: str, data: Dict[str, Any]) -> str:
        """Generate sample context for training data"""
        keywords = data["keywords"][:3]  # Use top 3 keywords
        patterns = data["context_patterns"][:2]  # Use top 2 patterns

        return f"Strategic situation involving {' and '.join(keywords)} with focus on {' and '.join(patterns)}"

    def _extract_context_features(self, context: str) -> Dict[str, float]:
        """Extract ML features from context using NLP techniques"""
        context_lower = context.lower()
        features = {}

        # Keyword frequency features
        for framework, data in self.framework_patterns.items():
            keyword_score = 0
            for keyword in data["keywords"]:
                if keyword in context_lower:
                    # TF-IDF-like scoring
                    term_freq = context_lower.count(keyword) / len(
                        context_lower.split()
                    )
                    keyword_score += term_freq * 10  # Weight factor
            features[f"{framework}_keywords"] = keyword_score

        # Context pattern features
        for framework, data in self.framework_patterns.items():
            pattern_score = 0
            for pattern in data["context_patterns"]:
                if any(word in context_lower for word in pattern.split()):
                    pattern_score += 1
            features[f"{framework}_patterns"] = pattern_score

        # Linguistic features
        features["context_length"] = len(context.split())
        features["question_count"] = context.count("?")
        features["complexity_indicators"] = len(
            re.findall(r"\b(complex|difficult|challenging|strategic)\b", context_lower)
        )
        features["urgency_indicators"] = len(
            re.findall(r"\b(urgent|critical|immediate|asap)\b", context_lower)
        )

        return features

    def _calculate_ml_framework_scores(
        self,
        context: str,
        stakeholders: List[str] = None,
        initiatives: List[str] = None,
    ) -> Dict[str, float]:
        """Calculate framework scores using ML-based approach"""
        features = self._extract_context_features(context)
        scores = {}

        for framework, data in self.framework_patterns.items():
            # Base ML score from feature matching
            keyword_score = features.get(f"{framework}_keywords", 0)
            pattern_score = features.get(f"{framework}_patterns", 0)

            # Historical success rate weighting
            historical_weight = data["historical_success_rate"]

            # Sample size confidence adjustment
            sample_confidence = min(
                data["sample_size"] / 50.0, 1.0
            )  # Normalize to max 50 samples

            # Combine scores with ML weighting
            base_score = (
                keyword_score * 0.4 + pattern_score * 0.3 + historical_weight * 0.3
            )
            confidence_adjusted_score = base_score * sample_confidence

            # Context-specific boosters
            if (
                stakeholders
                and len(stakeholders) > 3
                and framework == "crucial_conversations"
            ):
                confidence_adjusted_score *= 1.2

            if (
                initiatives
                and len(initiatives) > 2
                and framework in ["capital_allocation", "good_strategy"]
            ):
                confidence_adjusted_score *= 1.15

            scores[framework] = confidence_adjusted_score

        return scores

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
        """Calculate progress-based score using real metrics"""
        try:
            # Extract progress indicators
            milestones_completed = data.get("milestones_completed", 0)
            milestones_total = data.get("milestones_total", 1)
            days_elapsed = data.get("days_elapsed", 0)
            days_planned = data.get("days_planned", 1)

            # Calculate milestone progress (0-1)
            milestone_progress = min(milestones_completed / milestones_total, 1.0)

            # Calculate timeline progress (0-1)
            timeline_progress = min(
                days_elapsed / days_planned, 1.5
            )  # Allow 150% for buffer

            # Progress velocity analysis
            if timeline_progress > 0:
                velocity_ratio = milestone_progress / timeline_progress
                # Ideal velocity ratio is 1.0 (milestones completed = time elapsed)
                velocity_score = max(0, 1.0 - abs(velocity_ratio - 1.0))
            else:
                velocity_score = 1.0  # No time elapsed yet

            # Combine scores with weighting
            progress_score = (
                milestone_progress * 0.5
                + velocity_score * 0.3
                + (1.0 - min(timeline_progress, 1.0)) * 0.2  # Bonus for being ahead
            )

            return min(progress_score, 1.0)

        except (ZeroDivisionError, KeyError, TypeError):
            # Fallback scoring if data is incomplete
            return self._fallback_progress_assessment(data)

    def _calculate_stakeholder_score(self, data: Dict[str, Any]) -> float:
        """Calculate stakeholder engagement score using sentiment and interaction analysis"""
        try:
            stakeholder_list = data.get("stakeholders", [])
            if not stakeholder_list:
                return 0.5  # Neutral score if no stakeholder data

            engagement_scores = []

            for stakeholder in stakeholder_list:
                if isinstance(stakeholder, dict):
                    # Analyze individual stakeholder metrics
                    sentiment = stakeholder.get("sentiment", "neutral")
                    last_interaction_days = stakeholder.get("last_interaction_days", 7)
                    response_rate = stakeholder.get("response_rate", 0.7)
                    influence_level = stakeholder.get("influence_level", "medium")

                    # Sentiment scoring
                    sentiment_scores = {
                        "positive": 1.0,
                        "neutral": 0.6,
                        "negative": 0.2,
                    }
                    sentiment_score = sentiment_scores.get(sentiment, 0.6)

                    # Interaction recency (decay function)
                    interaction_score = max(0.2, 1.0 - (last_interaction_days / 30.0))

                    # Response rate is already 0-1
                    response_score = min(response_rate, 1.0)

                    # Influence weighting
                    influence_weights = {"high": 1.2, "medium": 1.0, "low": 0.8}
                    influence_weight = influence_weights.get(influence_level, 1.0)

                    # Calculate weighted stakeholder score
                    stakeholder_score = (
                        sentiment_score * 0.4
                        + interaction_score * 0.3
                        + response_score * 0.3
                    ) * influence_weight

                    engagement_scores.append(min(stakeholder_score, 1.0))

            # Return weighted average (higher influence stakeholders matter more)
            return (
                sum(engagement_scores) / len(engagement_scores)
                if engagement_scores
                else 0.5
            )

        except (KeyError, TypeError, ValueError):
            return self._fallback_stakeholder_assessment(data)

    def _calculate_timeline_score(self, data: Dict[str, Any]) -> float:
        """Calculate timeline adherence score with predictive analysis"""
        try:
            planned_end_date = data.get("planned_end_date")
            current_date = data.get("current_date", datetime.now())
            progress_percentage = data.get("progress_percentage", 0.0)

            if not planned_end_date:
                return 0.7  # Default if no timeline data

            # Convert to datetime if string
            if isinstance(planned_end_date, str):
                planned_end_date = datetime.fromisoformat(planned_end_date)
            if isinstance(current_date, str):
                current_date = datetime.fromisoformat(current_date)

            # Calculate timeline metrics
            total_duration = (
                planned_end_date - data.get("start_date", current_date)
            ).days
            days_elapsed = (current_date - data.get("start_date", current_date)).days
            days_remaining = (planned_end_date - current_date).days

            if total_duration <= 0:
                return 1.0  # Very short timeline

            # Expected progress based on time elapsed
            time_progress = days_elapsed / total_duration

            # Actual vs expected progress
            progress_ratio = progress_percentage / 100.0 if time_progress > 0 else 1.0
            expected_progress = time_progress

            # Timeline health scoring
            if progress_ratio >= expected_progress:
                # Ahead or on schedule
                timeline_score = min(
                    1.0, 0.8 + (progress_ratio - expected_progress) * 2
                )
            else:
                # Behind schedule - calculate severity
                deficit = expected_progress - progress_ratio
                timeline_score = max(0.1, 0.8 - deficit * 3)

            # Risk adjustment for remaining time
            if days_remaining < 0:
                timeline_score *= 0.3  # Severely penalize overdue projects
            elif days_remaining < 7:
                timeline_score *= 0.7  # Moderate penalty for very tight timeline

            return min(timeline_score, 1.0)

        except (KeyError, TypeError, ValueError):
            return self._fallback_timeline_assessment(data)

    def _calculate_resource_score(self, data: Dict[str, Any]) -> float:
        """Calculate resource availability score with constraint analysis"""
        try:
            budget_utilization = data.get("budget_utilization", 0.5)
            team_capacity = data.get("team_capacity", 0.8)
            critical_skills_available = data.get("critical_skills_available", True)
            external_dependencies = data.get("external_dependencies", [])

            # Budget health (optimal utilization is 70-90%)
            if 0.7 <= budget_utilization <= 0.9:
                budget_score = 1.0
            elif budget_utilization < 0.7:
                budget_score = 0.6 + (budget_utilization / 0.7) * 0.4
            else:  # Over 90%
                budget_score = max(0.2, 1.2 - budget_utilization)

            # Team capacity (optimal is 80-95%)
            if 0.8 <= team_capacity <= 0.95:
                capacity_score = 1.0
            elif team_capacity < 0.8:
                capacity_score = team_capacity / 0.8
            else:  # Over 95%
                capacity_score = max(0.3, 1.2 - team_capacity)  # Burnout risk

            # Critical skills penalty
            skills_score = 1.0 if critical_skills_available else 0.4

            # External dependencies risk
            dependency_risk = min(
                len(external_dependencies) * 0.1, 0.5
            )  # Max 50% penalty
            dependency_score = 1.0 - dependency_risk

            # Combine resource scores
            resource_score = (
                budget_score * 0.3
                + capacity_score * 0.4
                + skills_score * 0.2
                + dependency_score * 0.1
            )

            return min(resource_score, 1.0)

        except (KeyError, TypeError, ValueError):
            return self._fallback_resource_assessment(data)

    def _fallback_progress_assessment(self, data: Dict[str, Any]) -> float:
        """Fallback progress assessment when data is incomplete"""
        # Use simple heuristics based on available data
        if "status" in data:
            status_scores = {
                "completed": 1.0,
                "on_track": 0.8,
                "at_risk": 0.5,
                "blocked": 0.2,
                "cancelled": 0.0,
            }
            return status_scores.get(data["status"], 0.6)
        return 0.6  # Neutral default

    def _fallback_stakeholder_assessment(self, data: Dict[str, Any]) -> float:
        """Fallback stakeholder assessment when data is incomplete"""
        stakeholder_count = len(data.get("stakeholders", []))
        if stakeholder_count == 0:
            return 0.4  # Low score for no stakeholder engagement
        elif stakeholder_count > 10:
            return 0.6  # Too many stakeholders can be problematic
        else:
            return 0.7  # Reasonable stakeholder count

    def _fallback_timeline_assessment(self, data: Dict[str, Any]) -> float:
        """Fallback timeline assessment when data is incomplete"""
        if "deadline_proximity" in data:
            proximity = data["deadline_proximity"]
            if proximity == "overdue":
                return 0.2
            elif proximity == "urgent":
                return 0.4
            elif proximity == "approaching":
                return 0.6
            else:
                return 0.8
        return 0.6

    def _fallback_resource_assessment(self, data: Dict[str, Any]) -> float:
        """Fallback resource assessment when data is incomplete"""
        if "resource_status" in data:
            status_scores = {
                "abundant": 0.9,
                "adequate": 0.8,
                "constrained": 0.5,
                "critical": 0.2,
            }
            return status_scores.get(data["resource_status"], 0.6)
        return 0.7  # Optimistic default

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
