#!/usr/bin/env python3
"""
Analytics Engine Configuration Constants

Centralized configuration to follow DRY principles and SOLID architecture.
All hardcoded strings and magic numbers moved here for maintainability.
"""

from typing import Dict, List, Any

# Priority Levels
PRIORITY_LEVELS = {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}

# Confidence Thresholds
CONFIDENCE_THRESHOLDS = {"DEFAULT": 0.7, "HIGH": 0.8, "MINIMUM": 0.5}

# Score Thresholds
SCORE_THRESHOLDS = {
    "EXCELLENT": 0.9,
    "GOOD": 0.8,
    "AVERAGE": 0.7,
    "POOR": 0.5,
    "CRITICAL": 0.2,
    "MINIMUM": 0.0,
    "MAXIMUM": 1.0,
}

# Framework Success Rates (Historical Data)
FRAMEWORK_SUCCESS_RATES = {
    "team_topologies": 0.87,
    "wrap_framework": 0.92,
    "good_strategy": 0.84,
    "crucial_conversations": 0.79,
    "capital_allocation": 0.88,
    "accelerate": 0.85,
    "platform_strategy": 0.86,
}

# Framework Keywords
FRAMEWORK_KEYWORDS = {
    "team_topologies": [
        "team",
        "cognitive load",
        "organization",
        "structure",
        "topology",
        "conway",
    ],
    "wrap_framework": [
        "decision",
        "options",
        "choice",
        "analysis",
        "alternatives",
        "criteria",
    ],
    "good_strategy": [
        "strategy",
        "competitive",
        "advantage",
        "positioning",
        "market",
        "vision",
    ],
    "crucial_conversations": [
        "stakeholder",
        "conflict",
        "alignment",
        "communication",
        "difficult",
        "conversation",
    ],
    "capital_allocation": [
        "budget",
        "investment",
        "resource",
        "roi",
        "allocation",
        "priority",
    ],
    "accelerate": [
        "performance",
        "devops",
        "delivery",
        "metrics",
        "flow",
        "deployment",
    ],
    "platform_strategy": [
        "platform",
        "ecosystem",
        "scalability",
        "reuse",
        "api",
        "infrastructure",
    ],
}

# Framework Context Patterns
FRAMEWORK_CONTEXT_PATTERNS = {
    "team_topologies": ["organizational", "scaling", "team design", "communication"],
    "wrap_framework": ["strategic decision", "multiple options", "evaluation"],
    "good_strategy": ["strategic planning", "competitive analysis", "market position"],
    "crucial_conversations": [
        "stakeholder management",
        "conflict resolution",
        "alignment",
    ],
    "capital_allocation": [
        "resource planning",
        "investment decision",
        "budget allocation",
    ],
    "accelerate": ["engineering performance", "delivery optimization", "metrics"],
    "platform_strategy": ["platform design", "ecosystem building", "scalability"],
}

# Framework Success Contexts
FRAMEWORK_SUCCESS_CONTEXTS = {
    "team_topologies": ["growing team", "microservices", "platform team"],
    "wrap_framework": ["complex decision", "stakeholder alignment", "option analysis"],
    "good_strategy": ["strategy development", "competitive response", "vision setting"],
    "crucial_conversations": [
        "stakeholder conflict",
        "alignment issues",
        "difficult discussions",
    ],
    "capital_allocation": [
        "resource constraints",
        "investment decision",
        "priority setting",
    ],
    "accelerate": ["performance improvement", "delivery speed", "engineering metrics"],
    "platform_strategy": [
        "platform development",
        "ecosystem strategy",
        "scalability planning",
    ],
}

# Framework Base Probabilities
FRAMEWORK_BASE_PROBABILITIES = {
    "team_topologies": 0.90,
    "wrap_framework": 0.80,
    "good_strategy": 0.95,
    "crucial_conversations": 0.75,
    "capital_allocation": 0.85,
    "accelerate": 0.80,
    "platform_strategy": 0.85,
}

# Framework Descriptions
FRAMEWORK_DESCRIPTIONS = {
    "team_topologies": "Optimal for organizational design and team structure decisions",
    "wrap_framework": "Best for structured decision-making with multiple options",
    "good_strategy": "Ideal for defining clear strategic direction and competitive advantage",
    "crucial_conversations": "Perfect for stakeholder alignment and difficult discussions",
    "capital_allocation": "Optimal for resource investment and budget decisions",
    "accelerate": "Best for engineering performance and delivery optimization",
    "platform_strategy": "Ideal for platform design and ecosystem decisions",
}

# Sentiment Scores
SENTIMENT_SCORES = {"positive": 1.0, "neutral": 0.6, "negative": 0.2}

# Influence Weights
INFLUENCE_WEIGHTS = {"high": 1.2, "medium": 1.0, "low": 0.8}

# Status Score Mappings
STATUS_SCORES = {
    "completed": 1.0,
    "on_track": 0.8,
    "at_risk": 0.5,
    "blocked": 0.2,
    "cancelled": 0.0,
}

# Resource Status Scores
RESOURCE_STATUS_SCORES = {
    "abundant": 0.9,
    "adequate": 0.8,
    "constrained": 0.5,
    "critical": 0.2,
}

# Impact Keywords
HIGH_IMPACT_KEYWORDS = ["strategic", "organizational", "transformation", "critical"]
MEDIUM_IMPACT_KEYWORDS = ["improvement", "optimization", "enhancement", "planning"]

# Complexity Indicators
COMPLEXITY_INDICATORS = [r"\b(complex|difficult|challenging|strategic)\b"]
URGENCY_INDICATORS = [r"\b(urgent|critical|immediate|asap)\b"]

# Weight Configurations
SCORING_WEIGHTS = {
    "progress": {
        "milestone_progress": 0.5,
        "velocity_score": 0.3,
        "timeline_bonus": 0.2,
    },
    "stakeholder": {"sentiment": 0.4, "interaction": 0.3, "response": 0.3},
    "resource": {"budget": 0.3, "capacity": 0.4, "skills": 0.2, "dependency": 0.1},
    "overall": {
        "progress": 0.3,
        "stakeholder": 0.25,
        "timeline": 0.25,
        "resource": 0.2,
    },
}

# Performance Targets
PERFORMANCE_TARGETS = {
    "retrieval_time": 3.0,
    "relevance_score": 0.9,
    "memory_footprint": 1024 * 1024 * 1024,  # 1GB
    "analytics_response_time": 2.0,
    "framework_accuracy": 0.85,
}

# Warning Level Thresholds
WARNING_LEVEL_THRESHOLDS = {"critical": 0.5, "alert": 0.7, "watch": 0.8, "none": 1.0}

# Timeout and Limits
LIMITS = {
    "max_indicators": 5,
    "max_dependency_penalty": 0.5,
    "min_sample_confidence": 50.0,
    "optimal_capacity_min": 0.8,
    "optimal_capacity_max": 0.95,
    "optimal_budget_min": 0.7,
    "optimal_budget_max": 0.9,
}

# Error Messages
ERROR_MESSAGES = {
    "analysis_failed": "Analysis failed, providing general recommendation",
    "calculation_error": "Error calculating health score",
    "engagement_error": "Error analyzing stakeholder engagement",
    "fallback_reason": "Analysis unavailable",
    "insufficient_data": "Insufficient data for analysis",
}

# Success Messages
SUCCESS_MESSAGES = {
    "analyzer_initialized": "FrameworkPatternAnalyzer initialized with ML capabilities",
    "scorer_initialized": "InitiativeHealthScorer initialized",
    "stakeholder_analyzer_initialized": "StakeholderEngagementAnalyzer initialized",
    "analytics_engine_initialized": "AnalyticsEngine initialized with predictive intelligence capabilities",
}

# Description Templates
DESCRIPTION_TEMPLATES = {
    "health_assessment": "Health assessment for strategic initiatives",
    "stakeholder_analytics": "Stakeholder interaction and engagement analytics",
    "pattern_analyzer": "Analyzes framework usage patterns and predicts optimal applications using ML",
    "health_scorer": "Scores initiative health and predicts risks",
    "engagement_analyzer": "Analyzes stakeholder interaction patterns and engagement",
}


def get_framework_config() -> Dict[str, Any]:
    """Get complete framework configuration"""
    return {
        "keywords": FRAMEWORK_KEYWORDS,
        "context_patterns": FRAMEWORK_CONTEXT_PATTERNS,
        "success_contexts": FRAMEWORK_SUCCESS_CONTEXTS,
        "success_rates": FRAMEWORK_SUCCESS_RATES,
        "base_probabilities": FRAMEWORK_BASE_PROBABILITIES,
        "descriptions": FRAMEWORK_DESCRIPTIONS,
    }


def get_scoring_config() -> Dict[str, Any]:
    """Get complete scoring configuration"""
    return {
        "thresholds": SCORE_THRESHOLDS,
        "weights": SCORING_WEIGHTS,
        "sentiment_scores": SENTIMENT_SCORES,
        "influence_weights": INFLUENCE_WEIGHTS,
        "status_scores": STATUS_SCORES,
        "resource_status_scores": RESOURCE_STATUS_SCORES,
    }


def get_performance_config() -> Dict[str, Any]:
    """Get performance targets and limits"""
    return {
        "targets": PERFORMANCE_TARGETS,
        "limits": LIMITS,
        "warning_levels": WARNING_LEVEL_THRESHOLDS,
    }
