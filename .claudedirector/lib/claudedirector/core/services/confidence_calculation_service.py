"""
Confidence Calculation Service - SOLID Refactoring Phase 1

Implements confidence calculation logic with Single Responsibility Principle (SRP).
This service is focused solely on calculating confidence scores for analysis results,
extracted from the monolithic EmbeddedFrameworkEngine.

Author: Martin (SOLID Refactoring Implementation)
"""

from typing import Dict, List, Optional, Any
import structlog
from dataclasses import dataclass
import math

from ..interfaces.framework_provider_interface import (
    IConfidenceCalculator,
    AnalysisInsight,
    FrameworkContext,
    FrameworkRecommendation,
    AnalysisComplexity,
)

logger = structlog.get_logger(__name__)


@dataclass
class ConfidenceFactors:
    """Factors that contribute to confidence calculation"""

    evidence_strength: float
    pattern_matches: float
    context_relevance: float
    framework_alignment: float
    consistency_score: float
    completeness_score: float


class ConfidenceCalculationService:
    """
    Service responsible for calculating confidence scores for analysis results.

    Implements Single Responsibility Principle (SRP) by focusing only on confidence
    calculation logic. Provides sophisticated scoring algorithms that consider
    multiple factors for accurate confidence assessment.
    """

    def __init__(self):
        # Confidence calculation weights
        self.evidence_weight = 0.25
        self.pattern_weight = 0.20
        self.context_weight = 0.20
        self.framework_weight = 0.15
        self.consistency_weight = 0.10
        self.completeness_weight = 0.10

        # Confidence thresholds
        self.min_confidence = 0.1
        self.max_confidence = 1.0
        self.high_confidence_threshold = 0.8
        self.medium_confidence_threshold = 0.6

        # Evidence quality factors
        self.evidence_quality_factors = {
            "specific_examples": 1.0,
            "quantitative_data": 0.9,
            "stakeholder_mentions": 0.8,
            "pattern_matches": 0.7,
            "contextual_references": 0.6,
            "general_statements": 0.4,
        }

    def calculate_insight_confidence(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> float:
        """
        Calculate confidence score for an individual insight.

        Args:
            insight: Analysis insight to score
            context: Analysis context for additional scoring factors

        Returns:
            Confidence score between 0.0 and 1.0
        """
        try:
            # Calculate individual confidence factors
            factors = self._calculate_confidence_factors(insight, context)

            # Weighted combination of factors
            confidence = (
                factors.evidence_strength * self.evidence_weight
                + factors.pattern_matches * self.pattern_weight
                + factors.context_relevance * self.context_weight
                + factors.framework_alignment * self.framework_weight
                + factors.consistency_score * self.consistency_weight
                + factors.completeness_score * self.completeness_weight
            )

            # Apply bounds and adjustments
            confidence = self._apply_confidence_adjustments(
                confidence, insight, context
            )

            # Ensure within valid range
            confidence = max(self.min_confidence, min(confidence, self.max_confidence))

            logger.debug(
                "Insight confidence calculated",
                insight_category=insight.category,
                confidence=confidence,
                factors=factors,
            )

            return confidence

        except Exception as e:
            logger.error(
                "Insight confidence calculation failed",
                insight_category=insight.category,
                error=str(e),
            )
            return 0.5  # Default medium confidence on error

    def calculate_overall_confidence(
        self, insights: List[AnalysisInsight], framework_relevance: float
    ) -> float:
        """
        Calculate overall confidence for the complete analysis.

        Args:
            insights: List of analysis insights
            framework_relevance: Relevance score of selected framework

        Returns:
            Overall confidence score between 0.0 and 1.0
        """
        try:
            if not insights:
                return 0.0

            # Calculate individual insight confidences
            insight_confidences = [insight.confidence for insight in insights]

            # Calculate base confidence metrics
            avg_confidence = sum(insight_confidences) / len(insight_confidences)
            min_confidence = min(insight_confidences)
            max_confidence = max(insight_confidences)
            confidence_variance = self._calculate_variance(insight_confidences)

            # Calculate consistency bonus/penalty
            consistency_factor = self._calculate_consistency_factor(insight_confidences)

            # Calculate completeness factor
            completeness_factor = self._calculate_completeness_factor(insights)

            # Calculate framework alignment factor
            framework_factor = min(
                framework_relevance * 1.2, 1.0
            )  # Slight boost for good framework match

            # Weighted combination
            overall_confidence = (
                avg_confidence * 0.4  # Base average
                + min_confidence * 0.2  # Weakest link consideration
                + consistency_factor * 0.2  # Consistency across insights
                + completeness_factor * 0.1  # Completeness of analysis
                + framework_factor * 0.1  # Framework appropriateness
            )

            # Apply final adjustments
            overall_confidence = self._apply_overall_adjustments(
                overall_confidence, insights, framework_relevance
            )

            # Ensure within valid range
            overall_confidence = max(
                self.min_confidence, min(overall_confidence, self.max_confidence)
            )

            logger.info(
                "Overall confidence calculated",
                insights_count=len(insights),
                avg_individual_confidence=avg_confidence,
                overall_confidence=overall_confidence,
                framework_relevance=framework_relevance,
            )

            return overall_confidence

        except Exception as e:
            logger.error(
                "Overall confidence calculation failed",
                insights_count=len(insights) if insights else 0,
                error=str(e),
            )
            return 0.5  # Default medium confidence on error

    def get_confidence_explanation(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> Dict[str, Any]:
        """
        Get detailed explanation of confidence calculation for debugging/transparency.

        Args:
            insight: Analysis insight to explain
            context: Analysis context

        Returns:
            Dictionary with detailed confidence breakdown
        """
        try:
            factors = self._calculate_confidence_factors(insight, context)

            explanation = {
                "overall_confidence": insight.confidence,
                "confidence_level": self._get_confidence_level(insight.confidence),
                "factors": {
                    "evidence_strength": {
                        "score": factors.evidence_strength,
                        "weight": self.evidence_weight,
                        "contribution": factors.evidence_strength
                        * self.evidence_weight,
                        "description": "Quality and quantity of supporting evidence",
                    },
                    "pattern_matches": {
                        "score": factors.pattern_matches,
                        "weight": self.pattern_weight,
                        "contribution": factors.pattern_matches * self.pattern_weight,
                        "description": "Strength of pattern matches in user input",
                    },
                    "context_relevance": {
                        "score": factors.context_relevance,
                        "weight": self.context_weight,
                        "contribution": factors.context_relevance * self.context_weight,
                        "description": "Relevance to provided context and history",
                    },
                    "framework_alignment": {
                        "score": factors.framework_alignment,
                        "weight": self.framework_weight,
                        "contribution": factors.framework_alignment
                        * self.framework_weight,
                        "description": "Alignment with framework methodology",
                    },
                    "consistency_score": {
                        "score": factors.consistency_score,
                        "weight": self.consistency_weight,
                        "contribution": factors.consistency_score
                        * self.consistency_weight,
                        "description": "Consistency with other insights",
                    },
                    "completeness_score": {
                        "score": factors.completeness_score,
                        "weight": self.completeness_weight,
                        "contribution": factors.completeness_score
                        * self.completeness_weight,
                        "description": "Completeness of insight information",
                    },
                },
                "evidence_analysis": {
                    "evidence_count": len(insight.evidence),
                    "evidence_quality": self._assess_evidence_quality(insight.evidence),
                    "evidence_diversity": self._assess_evidence_diversity(
                        insight.evidence
                    ),
                },
            }

            return explanation

        except Exception as e:
            logger.error("Confidence explanation generation failed", error=str(e))
            return {"error": "Unable to generate confidence explanation"}

    # Private helper methods

    def _calculate_confidence_factors(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> ConfidenceFactors:
        """Calculate individual confidence factors"""

        # Evidence strength
        evidence_strength = self._calculate_evidence_strength(insight.evidence)

        # Pattern matches
        pattern_matches = self._calculate_pattern_match_strength(insight, context)

        # Context relevance
        context_relevance = self._calculate_context_relevance(insight, context)

        # Framework alignment
        framework_alignment = self._calculate_framework_alignment(insight, context)

        # Consistency score (placeholder - would need other insights for comparison)
        consistency_score = 0.7  # Default moderate consistency

        # Completeness score
        completeness_score = self._calculate_completeness_score(insight)

        return ConfidenceFactors(
            evidence_strength=evidence_strength,
            pattern_matches=pattern_matches,
            context_relevance=context_relevance,
            framework_alignment=framework_alignment,
            consistency_score=consistency_score,
            completeness_score=completeness_score,
        )

    def _calculate_evidence_strength(self, evidence: List[str]) -> float:
        """Calculate strength of supporting evidence"""
        if not evidence:
            return 0.0

        # Base score from evidence count
        count_score = min(
            len(evidence) / 5.0, 1.0
        )  # Normalize to max 5 pieces of evidence

        # Quality score from evidence content
        quality_scores = []
        for evidence_item in evidence:
            quality_score = self._assess_single_evidence_quality(evidence_item)
            quality_scores.append(quality_score)

        avg_quality = (
            sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        )

        # Combine count and quality
        return (count_score * 0.4) + (avg_quality * 0.6)

    def _assess_single_evidence_quality(self, evidence_item: str) -> float:
        """Assess quality of a single piece of evidence"""
        evidence_lower = evidence_item.lower()

        # Check for quality indicators
        quality_score = 0.5  # Base score

        # Specific examples or data
        if any(
            indicator in evidence_lower
            for indicator in ["example", "data", "metric", "number"]
        ):
            quality_score += 0.3

        # Stakeholder mentions
        if any(
            indicator in evidence_lower
            for indicator in ["team", "stakeholder", "user", "customer"]
        ):
            quality_score += 0.2

        # Process or system references
        if any(
            indicator in evidence_lower
            for indicator in ["process", "system", "workflow", "method"]
        ):
            quality_score += 0.2

        # Outcome or impact references
        if any(
            indicator in evidence_lower
            for indicator in ["impact", "result", "outcome", "benefit"]
        ):
            quality_score += 0.2

        return min(quality_score, 1.0)

    def _calculate_pattern_match_strength(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> float:
        """Calculate strength of pattern matches"""
        user_input_lower = context.user_input.lower()

        # Count evidence items that appear in user input
        matching_evidence = sum(
            1 for evidence in insight.evidence if evidence.lower() in user_input_lower
        )

        if not insight.evidence:
            return 0.0

        # Calculate match ratio
        match_ratio = matching_evidence / len(insight.evidence)

        # Boost for direct matches
        return min(match_ratio * 1.2, 1.0)

    def _calculate_context_relevance(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> float:
        """Calculate relevance to provided context"""
        relevance_score = 0.5  # Base score

        # Stakeholder context relevance
        if context.stakeholder_context:
            stakeholder_keywords = str(context.stakeholder_context).lower()
            if any(
                evidence.lower() in stakeholder_keywords
                for evidence in insight.evidence
            ):
                relevance_score += 0.2

        # Organizational context relevance
        if context.organizational_context:
            org_keywords = str(context.organizational_context).lower()
            if any(evidence.lower() in org_keywords for evidence in insight.evidence):
                relevance_score += 0.2

        # Session history relevance
        if context.session_history:
            history_text = " ".join(context.session_history).lower()
            if any(evidence.lower() in history_text for evidence in insight.evidence):
                relevance_score += 0.3

        return min(relevance_score, 1.0)

    def _calculate_framework_alignment(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> float:
        """Calculate alignment with framework methodology"""
        # This would ideally check against framework-specific criteria
        # For now, use category-based heuristics

        category_alignment_scores = {
            "current_state": 0.8,
            "stakeholder_mapping": 0.9,
            "success_metrics": 0.7,
            "implementation_roadmap": 0.8,
            "risk_mitigation": 0.7,
        }

        return category_alignment_scores.get(insight.category, 0.6)

    def _calculate_completeness_score(self, insight: AnalysisInsight) -> float:
        """Calculate completeness of insight information"""
        completeness_factors = []

        # Has meaningful insight text
        if len(insight.insight.strip()) > 20:
            completeness_factors.append(1.0)
        else:
            completeness_factors.append(0.3)

        # Has evidence
        if insight.evidence and len(insight.evidence) > 0:
            completeness_factors.append(1.0)
        else:
            completeness_factors.append(0.0)

        # Has category
        if insight.category and insight.category.strip():
            completeness_factors.append(1.0)
        else:
            completeness_factors.append(0.0)

        # Is marked as actionable
        if insight.actionable:
            completeness_factors.append(1.0)
        else:
            completeness_factors.append(0.7)

        return sum(completeness_factors) / len(completeness_factors)

    def _apply_confidence_adjustments(
        self,
        base_confidence: float,
        insight: AnalysisInsight,
        context: FrameworkContext,
    ) -> float:
        """Apply final adjustments to confidence score"""
        adjusted_confidence = base_confidence

        # Complexity adjustment
        if context.complexity_level == AnalysisComplexity.HIGH:
            adjusted_confidence *= 0.9  # Slight reduction for high complexity
        elif context.complexity_level == AnalysisComplexity.LOW:
            adjusted_confidence *= 1.1  # Slight boost for low complexity

        # Length adjustment (very short or very long insights are less reliable)
        insight_length = len(insight.insight.strip())
        if insight_length < 10:
            adjusted_confidence *= 0.5
        elif insight_length > 500:
            adjusted_confidence *= 0.8

        return adjusted_confidence

    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of confidence values"""
        if len(values) < 2:
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance

    def _calculate_consistency_factor(self, confidences: List[float]) -> float:
        """Calculate consistency factor from confidence variance"""
        if len(confidences) < 2:
            return 1.0

        variance = self._calculate_variance(confidences)
        # Lower variance = higher consistency
        consistency = max(0.0, 1.0 - (variance * 2))  # Scale variance to consistency
        return consistency

    def _calculate_completeness_factor(self, insights: List[AnalysisInsight]) -> float:
        """Calculate completeness factor from insights coverage"""
        if not insights:
            return 0.0

        # Check category coverage
        categories = set(insight.category for insight in insights)
        expected_categories = {
            "current_state",
            "stakeholder_mapping",
            "success_metrics",
            "implementation_roadmap",
            "risk_mitigation",
        }

        category_coverage = len(categories & expected_categories) / len(
            expected_categories
        )

        # Check evidence coverage
        total_evidence = sum(len(insight.evidence) for insight in insights)
        evidence_completeness = min(
            total_evidence / (len(insights) * 3), 1.0
        )  # Expect ~3 evidence per insight

        return (category_coverage * 0.6) + (evidence_completeness * 0.4)

    def _apply_overall_adjustments(
        self,
        base_confidence: float,
        insights: List[AnalysisInsight],
        framework_relevance: float,
    ) -> float:
        """Apply final adjustments to overall confidence"""
        adjusted_confidence = base_confidence

        # Framework relevance adjustment
        if framework_relevance < 0.5:
            adjusted_confidence *= 0.8  # Reduce confidence for poor framework match
        elif framework_relevance > 0.8:
            adjusted_confidence *= 1.1  # Boost confidence for excellent framework match

        # Insights count adjustment
        insights_count = len(insights)
        if insights_count < 3:
            adjusted_confidence *= 0.9  # Reduce for insufficient insights
        elif insights_count > 8:
            adjusted_confidence *= (
                0.95  # Slight reduction for too many insights (potential noise)
            )

        return adjusted_confidence

    def _get_confidence_level(self, confidence: float) -> str:
        """Get human-readable confidence level"""
        if confidence >= self.high_confidence_threshold:
            return "high"
        elif confidence >= self.medium_confidence_threshold:
            return "medium"
        else:
            return "low"

    def _assess_evidence_quality(self, evidence: List[str]) -> str:
        """Assess overall quality of evidence list"""
        if not evidence:
            return "none"

        quality_scores = [
            self._assess_single_evidence_quality(item) for item in evidence
        ]
        avg_quality = sum(quality_scores) / len(quality_scores)

        if avg_quality >= 0.8:
            return "high"
        elif avg_quality >= 0.6:
            return "medium"
        else:
            return "low"

    def _assess_evidence_diversity(self, evidence: List[str]) -> str:
        """Assess diversity of evidence types"""
        if not evidence:
            return "none"

        # Simple diversity check based on unique words
        all_words = set()
        for item in evidence:
            words = item.lower().split()
            all_words.update(words)

        diversity_ratio = len(all_words) / len(evidence) if evidence else 0

        if diversity_ratio >= 3:
            return "high"
        elif diversity_ratio >= 2:
            return "medium"
        else:
            return "low"
