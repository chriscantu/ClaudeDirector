#!/usr/bin/env python3
"""
🏗️ Sequential Thinking Step 5: DRY/SOLID Compliance - Framework Detection Constants

Centralized framework detection patterns to eliminate DRY violations in Enhanced Framework Engine.
Follows @BLOAT_PREVENTION_SYSTEM.md principles by consolidating duplicate pattern definitions.

🎯 DRY PRINCIPLE ENFORCEMENT:
- Single source of truth for all framework patterns
- Eliminates duplicate pattern definitions across 3+ methods
- Centralizes framework configuration and weights

🎯 SOLID PRINCIPLE COMPLIANCE:
- Single Responsibility: Only pattern definitions
- Open/Closed: Extensible pattern system
- Dependency Inversion: Abstract pattern interface

Author: Martin | Platform Architecture + Sequential Thinking Step 5
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class FrameworkCategory(Enum):
    """Framework categorization for enhanced detection"""

    ORGANIZATIONAL = "organizational"
    STRATEGIC = "strategic"
    DECISION_MAKING = "decision_making"
    COMMUNICATION = "communication"
    TECHNICAL = "technical"


@dataclass
class FrameworkPatternConfig:
    """Centralized framework pattern configuration"""

    patterns: List[str]
    weight: float
    context_boost_terms: List[str]
    category: FrameworkCategory
    semantic_concepts: List[str]
    min_pattern_matches: int = 1
    min_semantic_matches: int = 2


class FrameworkDetectionConstants:
    """
    🏗️ DRY PRINCIPLE: Single Source of Truth for Framework Detection

    Eliminates duplicate pattern definitions across:
    - _pattern_based_detection()
    - _semantic_detection()
    - _extract_strategic_elements()
    """

    # === CENTRALIZED FRAMEWORK PATTERNS ===

    FRAMEWORK_PATTERNS: Dict[str, FrameworkPatternConfig] = {
        "Team Topologies": FrameworkPatternConfig(
            patterns=[
                "team topology",
                "cognitive load",
                "stream-aligned",
                "platform team",
                "enabling team",
            ],
            weight=0.9,
            context_boost_terms=["organizational", "teams", "structure"],
            category=FrameworkCategory.ORGANIZATIONAL,
            semantic_concepts=[
                "team",
                "organization",
                "structure",
                "responsibility",
                "boundary",
            ],
        ),
        "Good Strategy Bad Strategy": FrameworkPatternConfig(
            patterns=[
                "strategy kernel",
                "coherent action",
                "strategic",
                "competitive advantage",
            ],
            weight=0.85,
            context_boost_terms=["strategy", "planning", "business"],
            category=FrameworkCategory.STRATEGIC,
            semantic_concepts=[
                "strategy",
                "goal",
                "objective",
                "competitive",
                "advantage",
                "position",
            ],
        ),
        "Capital Allocation Framework": FrameworkPatternConfig(
            patterns=[
                "capital allocation",
                "investment",
                "roi",
                "resource allocation",
                "budget",
            ],
            weight=0.8,
            context_boost_terms=["financial", "investment", "resource"],
            category=FrameworkCategory.STRATEGIC,
            semantic_concepts=[
                "resource",
                "investment",
                "allocation",
                "priority",
                "budget",
                "return",
            ],
        ),
        "WRAP Framework": FrameworkPatternConfig(
            patterns=[
                "wrap framework",
                "decision making",
                "widen options",
                "reality test",
            ],
            weight=0.85,
            context_boost_terms=["decision", "choice", "options"],
            category=FrameworkCategory.DECISION_MAKING,
            semantic_concepts=[
                "decision",
                "option",
                "alternative",
                "choice",
                "evaluate",
                "test",
            ],
        ),
        "Crucial Conversations": FrameworkPatternConfig(
            patterns=[
                "crucial conversation",
                "difficult conversation",
                "dialogue",
                "mutual respect",
            ],
            weight=0.8,
            context_boost_terms=["communication", "conflict", "stakeholder"],
            category=FrameworkCategory.COMMUNICATION,
            semantic_concepts=[
                "communication",
                "dialogue",
                "conversation",
                "conflict",
                "stakeholder",
                "agreement",
            ],
        ),
    }

    # === STRATEGIC CONTEXT INDICATORS ===

    STRATEGIC_CONTEXT_INDICATORS: Dict[str, List[str]] = {
        "organizational": ["team", "organization", "structure", "people"],
        "financial": ["budget", "cost", "investment", "roi", "revenue"],
        "operational": ["process", "efficiency", "performance", "quality"],
        "strategic": ["strategy", "vision", "goal", "objective", "competitive"],
        "technical": ["technology", "platform", "architecture", "system"],
    }

    # === DETECTION CONFIGURATION ===

    # 🧠 Sequential Thinking Step 3: Replace hard-coded values with centralized constants
    @classmethod
    def get_detection_config(cls) -> Dict[str, Any]:
        """Get detection configuration using centralized Phase 9.3 constants"""
        try:
            from ..core.constants.phase93_constants import Phase93ConfigurationManager

            config_manager = Phase93ConfigurationManager()
            confidence_weights = config_manager.get_confidence_weights()

            return {
                "confidence_weights": confidence_weights,
                "bonus_thresholds": {
                    "method_diversity_max": 0.15,  # TODO: Move to Phase93Constants
                    "evidence_accumulation_max": 0.10,  # TODO: Move to Phase93Constants
                    "complexity_bonus_max": 0.10,  # TODO: Move to Phase93Constants
                },
                "quality_scoring": {
                    "comprehensiveness": 0.25,  # TODO: Move to Phase93Constants
                    "strategic_depth": 0.25,  # TODO: Move to Phase93Constants
                    "actionability": 0.2,  # TODO: Move to Phase93Constants
                    "evidence_quality": 0.15,  # TODO: Move to Phase93Constants
                    "executive_readiness": 0.15,  # TODO: Move to Phase93Constants
                },
            }
        except ImportError:
            # Fallback for environments without Phase93Constants
            return cls._get_fallback_detection_config()

    @classmethod
    def _get_fallback_detection_config(cls) -> Dict[str, Any]:
        """Fallback detection config when Phase93Constants unavailable"""
        return {
            "confidence_weights": {
                "pattern_match": 0.4,
                "semantic_match": 0.25,
                "context_relevance": 0.2,
                "historical_accuracy": 0.1,
                "complexity_bonus": 0.05,
            },
            "bonus_thresholds": {
                "method_diversity_max": 0.15,
                "evidence_accumulation_max": 0.10,
                "complexity_bonus_max": 0.10,
            },
            "quality_scoring": {
                "comprehensiveness": 0.25,
                "strategic_depth": 0.25,
                "actionability": 0.2,
                "evidence_quality": 0.15,
                "executive_readiness": 0.15,
            },
        }

    # Backward compatibility - use get_detection_config() instead
    DETECTION_CONFIG = {}

    # === UTILITY METHODS ===

    @classmethod
    def get_framework_by_category(
        cls, category: FrameworkCategory
    ) -> Dict[str, FrameworkPatternConfig]:
        """Get frameworks filtered by category"""
        return {
            name: config
            for name, config in cls.FRAMEWORK_PATTERNS.items()
            if config.category == category
        }

    @classmethod
    def get_all_patterns(cls) -> List[str]:
        """Get all framework patterns for validation"""
        all_patterns = []
        for config in cls.FRAMEWORK_PATTERNS.values():
            all_patterns.extend(config.patterns)
        return all_patterns

    @classmethod
    def get_all_semantic_concepts(cls) -> List[str]:
        """Get all semantic concepts for validation"""
        all_concepts = []
        for config in cls.FRAMEWORK_PATTERNS.values():
            all_concepts.extend(config.semantic_concepts)
        return list(set(all_concepts))  # Remove duplicates

    @classmethod
    def validate_framework_coverage(cls, content: str) -> Dict[str, Any]:
        """Validate framework pattern coverage for testing"""
        content_lower = content.lower()

        coverage_stats = {
            "total_frameworks": len(cls.FRAMEWORK_PATTERNS),
            "patterns_found": 0,
            "concepts_found": 0,
            "context_indicators_found": 0,
            "coverage_percentage": 0.0,
        }

        # Count pattern matches
        for pattern in cls.get_all_patterns():
            if pattern in content_lower:
                coverage_stats["patterns_found"] += 1

        # Count concept matches
        for concept in cls.get_all_semantic_concepts():
            if concept in content_lower:
                coverage_stats["concepts_found"] += 1

        # Count context indicators
        for indicators in cls.STRATEGIC_CONTEXT_INDICATORS.values():
            for indicator in indicators:
                if indicator in content_lower:
                    coverage_stats["context_indicators_found"] += 1
                    break  # Only count once per category

        # Calculate coverage percentage
        total_possible = len(cls.get_all_patterns()) + len(
            cls.get_all_semantic_concepts()
        )
        total_found = (
            coverage_stats["patterns_found"] + coverage_stats["concepts_found"]
        )
        coverage_stats["coverage_percentage"] = (
            (total_found / total_possible) * 100 if total_possible > 0 else 0
        )

        return coverage_stats


# === FACTORY FUNCTIONS ===


def get_framework_patterns() -> Dict[str, FrameworkPatternConfig]:
    """Factory function to get framework patterns"""
    return FrameworkDetectionConstants.FRAMEWORK_PATTERNS.copy()


def get_strategic_context_indicators() -> Dict[str, List[str]]:
    """Factory function to get strategic context indicators"""
    return FrameworkDetectionConstants.STRATEGIC_CONTEXT_INDICATORS.copy()


def get_detection_config() -> Dict[str, Any]:
    """Factory function to get detection configuration"""
    return FrameworkDetectionConstants.DETECTION_CONFIG.copy()
