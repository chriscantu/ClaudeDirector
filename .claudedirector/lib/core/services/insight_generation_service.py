"""
Insight Generation Service - SOLID Refactoring Phase 1

Implements insight generation logic with Single Responsibility Principle (SRP).
This service is focused solely on generating insights from framework analysis,
extracted from the monolithic EmbeddedFrameworkEngine.

Author: Martin (SOLID Refactoring Implementation)
"""

import re
from typing import Dict, List, Optional, Any, Set, Tuple
import structlog
from dataclasses import dataclass

from ..interfaces.framework_provider_interface import (
    IInsightGenerator,
    FrameworkDefinition,
    FrameworkContext,
    AnalysisInsight,
    AnalysisComplexity,
)

logger = structlog.get_logger(__name__)


@dataclass
class PatternMatch:
    """Represents a pattern match in user input"""

    pattern_type: str
    matched_text: str
    confidence: float
    context_words: List[str]


class InsightGenerationService:
    """
    Service responsible for generating insights from framework analysis.

    Implements Single Responsibility Principle (SRP) by focusing only on insight
    generation. Uses pattern matching and framework components to create
    meaningful strategic insights.
    """

    def __init__(self):
        # Pattern matching configurations
        self.insight_patterns = {
            "problem_identification": {
                "patterns": [
                    r"(?i)\b(problem|issue|challenge|difficulty|struggle|bottleneck|blocker|obstacle|concern|risk)\b",
                    r"(?i)\b(not working|failing|broken|inefficient|slow|delayed|stuck)\b",
                    r"(?i)\b(can't|cannot|unable|difficult to|hard to|impossible)\b",
                ],
                "confidence_base": 0.8,
                "category": "current_state",
            },
            "solution_seeking": {
                "patterns": [
                    r"(?i)\b(solution|approach|strategy|method|way|how to|need to|want to)\b",
                    r"(?i)\b(implement|execute|achieve|accomplish|resolve|fix|improve)\b",
                    r"(?i)\b(should we|could we|would it|what if|how about)\b",
                ],
                "confidence_base": 0.7,
                "category": "implementation_roadmap",
            },
            "stakeholder_mentions": {
                "patterns": [
                    r"(?i)\b(team|people|stakeholder|user|customer|client|executive|leadership|management|developer|engineer)\b",
                    r"(?i)\b(organization|company|department|group|committee|board)\b",
                    r"(?i)\b(communication|collaboration|coordination|alignment|buy-in)\b",
                ],
                "confidence_base": 0.6,
                "category": "stakeholder_mapping",
            },
            "outcome_focus": {
                "patterns": [
                    r"(?i)\b(result|outcome|impact|benefit|value|improvement|success|goal|objective|target)\b",
                    r"(?i)\b(measure|metric|kpi|indicator|benchmark|performance)\b",
                    r"(?i)\b(roi|return|efficiency|productivity|quality|satisfaction)\b",
                ],
                "confidence_base": 0.7,
                "category": "success_metrics",
            },
            "risk_awareness": {
                "patterns": [
                    r"(?i)\b(risk|threat|danger|concern|worry|fear|uncertainty|unknown)\b",
                    r"(?i)\b(might fail|could go wrong|what if|contingency|backup|fallback)\b",
                    r"(?i)\b(compliance|regulation|audit|security|privacy|legal)\b",
                ],
                "confidence_base": 0.6,
                "category": "risk_mitigation",
            },
        }

        # Strategic insight templates
        self.insight_templates = {
            "current_state": [
                "Current situation analysis reveals {insight_focus} requiring strategic attention",
                "Assessment indicates {insight_focus} as a key factor in current state",
                "Analysis shows {insight_focus} significantly impacts current operations",
            ],
            "stakeholder_mapping": [
                "Stakeholder analysis identifies {insight_focus} as critical for alignment",
                "Key stakeholder considerations include {insight_focus} for successful outcomes",
                "Stakeholder engagement strategy should address {insight_focus}",
            ],
            "success_metrics": [
                "Success measurement framework should incorporate {insight_focus}",
                "Key performance indicators should track {insight_focus} for strategic visibility",
                "Metrics strategy must include {insight_focus} to ensure accountability",
            ],
            "implementation_roadmap": [
                "Implementation approach should prioritize {insight_focus} for maximum impact",
                "Roadmap development must consider {insight_focus} as a critical path element",
                "Strategic execution requires careful attention to {insight_focus}",
            ],
            "risk_mitigation": [
                "Risk management strategy should address {insight_focus} proactively",
                "Mitigation planning must account for {insight_focus} as a potential concern",
                "Risk assessment indicates {insight_focus} requires specific attention",
            ],
        }

    def generate_insights(
        self, framework_definition: FrameworkDefinition, context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """
        Generate insights using framework components.

        Args:
            framework_definition: Framework to use for insight generation
            context: Analysis context with user input and metadata

        Returns:
            List of analysis insights generated from framework components
        """
        try:
            insights = []

            # Generate insights from each framework component
            for (
                component_name,
                component_data,
            ) in framework_definition.analysis_components.items():
                component_insights = self._generate_component_insights(
                    component_name, component_data, context
                )
                insights.extend(component_insights)

            # Generate pattern-based insights
            pattern_insights = self._generate_pattern_based_insights(context)
            insights.extend(pattern_insights)

            logger.info(
                "Insights generated",
                framework=framework_definition.name,
                total_insights=len(insights),
                component_insights=len(insights) - len(pattern_insights),
                pattern_insights=len(pattern_insights),
            )

            return insights

        except Exception as e:
            logger.error(
                "Insight generation failed",
                framework=framework_definition.name,
                error=str(e),
            )
            return []

    def enrich_insights_with_patterns(
        self, insights: List[AnalysisInsight], context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """
        Enrich insights with pattern matching and additional context.

        Args:
            insights: Base insights to enrich
            context: Analysis context

        Returns:
            Enriched insights with additional pattern-based information
        """
        try:
            enriched_insights = []

            for insight in insights:
                # Enhance insight with pattern matches
                enhanced_insight = self._enhance_insight_with_patterns(insight, context)

                # Add contextual evidence
                enhanced_insight = self._add_contextual_evidence(
                    enhanced_insight, context
                )

                # Adjust confidence based on pattern strength
                enhanced_insight = self._adjust_confidence_with_patterns(
                    enhanced_insight, context
                )

                enriched_insights.append(enhanced_insight)

            # Add cross-insight connections
            connected_insights = self._add_insight_connections(
                enriched_insights, context
            )

            logger.info(
                "Insights enriched",
                original_count=len(insights),
                enriched_count=len(connected_insights),
            )

            return connected_insights

        except Exception as e:
            logger.error("Insight enrichment failed", error=str(e))
            return insights  # Return original insights if enrichment fails

    # Private helper methods

    def _generate_component_insights(
        self,
        component_name: str,
        component_data: Dict[str, Any],
        context: FrameworkContext,
    ) -> List[AnalysisInsight]:
        """Generate insights for a specific framework component"""
        insights = []

        # Extract component information
        questions = component_data.get("questions", [])
        deliverables = component_data.get("deliverables", [])

        # Generate insights based on component questions and user input
        for question in questions:
            insight = self._generate_question_based_insight(
                component_name, question, context
            )
            if insight:
                insights.append(insight)

        # Generate insights based on deliverables
        for deliverable in deliverables:
            insight = self._generate_deliverable_based_insight(
                component_name, deliverable, context
            )
            if insight:
                insights.append(insight)

        return insights

    def _generate_question_based_insight(
        self, component_name: str, question: str, context: FrameworkContext
    ) -> Optional[AnalysisInsight]:
        """Generate insight based on framework component question"""
        # Extract key concepts from question
        question_concepts = self._extract_concepts_from_text(question)

        # Find relevant concepts in user input
        input_concepts = self._extract_concepts_from_text(context.user_input)

        # Find overlap between question and input concepts
        relevant_concepts = set(question_concepts) & set(input_concepts)

        if not relevant_concepts:
            return None

        # Generate insight based on relevant concepts
        insight_focus = ", ".join(list(relevant_concepts)[:3])  # Limit to top 3

        # Select appropriate template
        templates = self.insight_templates.get(
            component_name,
            [
                "Analysis of {insight_focus} provides strategic insights for consideration"
            ],
        )

        insight_text = templates[0].format(insight_focus=insight_focus)

        # Calculate confidence based on concept overlap
        confidence = min(len(relevant_concepts) / len(question_concepts), 1.0) * 0.8

        return AnalysisInsight(
            category=component_name,
            insight=insight_text,
            evidence=list(relevant_concepts),
            confidence=confidence,
            actionable=True,
        )

    def _generate_deliverable_based_insight(
        self, component_name: str, deliverable: str, context: FrameworkContext
    ) -> Optional[AnalysisInsight]:
        """Generate insight based on framework component deliverable"""
        # Check if user input relates to this deliverable
        deliverable_keywords = self._extract_keywords_from_text(deliverable)
        input_text_lower = context.user_input.lower()

        matching_keywords = [
            keyword
            for keyword in deliverable_keywords
            if keyword.lower() in input_text_lower
        ]

        if not matching_keywords:
            return None

        # Generate insight about the deliverable
        insight_text = f"Strategic deliverable '{deliverable}' should address identified {', '.join(matching_keywords)}"

        confidence = min(len(matching_keywords) / len(deliverable_keywords), 1.0) * 0.6

        return AnalysisInsight(
            category=component_name,
            insight=insight_text,
            evidence=matching_keywords,
            confidence=confidence,
            actionable=True,
        )

    def _generate_pattern_based_insights(
        self, context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """Generate insights based on pattern matching in user input"""
        insights = []

        for pattern_type, pattern_config in self.insight_patterns.items():
            matches = self._find_pattern_matches(
                context.user_input, pattern_config["patterns"]
            )

            if matches:
                insight = self._create_pattern_insight(
                    pattern_type, pattern_config, matches, context
                )
                if insight:
                    insights.append(insight)

        return insights

    def _find_pattern_matches(
        self, text: str, patterns: List[str]
    ) -> List[PatternMatch]:
        """Find pattern matches in text"""
        matches = []

        for pattern in patterns:
            regex_matches = re.finditer(pattern, text)
            for match in regex_matches:
                # Extract context around the match
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context_text = text[start:end]
                context_words = context_text.split()

                pattern_match = PatternMatch(
                    pattern_type=pattern,
                    matched_text=match.group(),
                    confidence=0.8,  # Base confidence for pattern matches
                    context_words=context_words,
                )
                matches.append(pattern_match)

        return matches

    def _create_pattern_insight(
        self,
        pattern_type: str,
        pattern_config: Dict[str, Any],
        matches: List[PatternMatch],
        context: FrameworkContext,
    ) -> Optional[AnalysisInsight]:
        """Create insight from pattern matches"""
        if not matches:
            return None

        category = pattern_config["category"]
        confidence_base = pattern_config["confidence_base"]

        # Extract evidence from matches
        evidence = list(set(match.matched_text for match in matches))

        # Generate insight text
        templates = self.insight_templates.get(
            category, ["Pattern analysis indicates {insight_focus} requires attention"]
        )

        insight_focus = ", ".join(evidence[:3])  # Limit to top 3 pieces of evidence
        insight_text = templates[0].format(insight_focus=insight_focus)

        # Calculate confidence based on number and strength of matches
        match_strength = len(matches) / 10.0  # Normalize by expected max matches
        confidence = min(confidence_base + match_strength, 1.0)

        return AnalysisInsight(
            category=category,
            insight=insight_text,
            evidence=evidence,
            confidence=confidence,
            actionable=True,
        )

    def _enhance_insight_with_patterns(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> AnalysisInsight:
        """Enhance existing insight with additional pattern information"""
        # Find additional patterns related to the insight category
        category_patterns = {
            config["category"]: patterns
            for patterns, config in self.insight_patterns.items()
            if config["category"] == insight.category
        }

        if insight.category in category_patterns:
            # Look for additional evidence in user input
            additional_evidence = []
            for pattern_type, pattern_config in self.insight_patterns.items():
                if pattern_config["category"] == insight.category:
                    matches = self._find_pattern_matches(
                        context.user_input, pattern_config["patterns"]
                    )
                    additional_evidence.extend([m.matched_text for m in matches])

            # Add unique additional evidence
            existing_evidence = set(insight.evidence)
            new_evidence = [
                e for e in additional_evidence if e not in existing_evidence
            ]

            if new_evidence:
                insight.evidence.extend(new_evidence[:3])  # Limit additional evidence

        return insight

    def _add_contextual_evidence(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> AnalysisInsight:
        """Add contextual evidence from stakeholder and organizational context"""
        additional_evidence = []

        # Add stakeholder context evidence
        if context.stakeholder_context:
            stakeholder_info = str(context.stakeholder_context)
            if any(
                evidence.lower() in stakeholder_info.lower()
                for evidence in insight.evidence
            ):
                additional_evidence.append("stakeholder context alignment")

        # Add organizational context evidence
        if context.organizational_context:
            org_info = str(context.organizational_context)
            if any(
                evidence.lower() in org_info.lower() for evidence in insight.evidence
            ):
                additional_evidence.append("organizational context relevance")

        # Add session history evidence
        if context.session_history:
            history_text = " ".join(context.session_history).lower()
            if any(evidence.lower() in history_text for evidence in insight.evidence):
                additional_evidence.append("session history consistency")

        if additional_evidence:
            insight.evidence.extend(additional_evidence)

        return insight

    def _adjust_confidence_with_patterns(
        self, insight: AnalysisInsight, context: FrameworkContext
    ) -> AnalysisInsight:
        """Adjust insight confidence based on pattern strength"""
        # Count supporting patterns in user input
        supporting_patterns = 0

        for evidence in insight.evidence:
            if evidence.lower() in context.user_input.lower():
                supporting_patterns += 1

        # Adjust confidence based on pattern support
        pattern_boost = min(supporting_patterns * 0.1, 0.3)  # Max 0.3 boost
        insight.confidence = min(insight.confidence + pattern_boost, 1.0)

        return insight

    def _add_insight_connections(
        self, insights: List[AnalysisInsight], context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """Add connections between related insights"""
        # Group insights by category
        category_groups = {}
        for insight in insights:
            category = insight.category
            if category not in category_groups:
                category_groups[category] = []
            category_groups[category].append(insight)

        # Add cross-category evidence for related insights
        for category, category_insights in category_groups.items():
            for insight in category_insights:
                # Look for evidence from other categories
                for other_category, other_insights in category_groups.items():
                    if other_category != category:
                        shared_evidence = []
                        for other_insight in other_insights:
                            shared = set(insight.evidence) & set(other_insight.evidence)
                            shared_evidence.extend(list(shared))

                        if shared_evidence:
                            insight.evidence.extend(
                                [
                                    f"cross-category connection: {evidence}"
                                    for evidence in shared_evidence[:2]
                                ]
                            )

        return insights

    # Utility methods

    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Simple concept extraction - could be enhanced with NLP
        words = re.findall(r"\b\w+\b", text.lower())

        # Filter out common words
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
        }

        concepts = [word for word in words if word not in stop_words and len(word) > 3]

        # Return unique concepts
        return list(set(concepts))

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract keywords from text (simpler than concepts)"""
        words = re.findall(r"\b\w+\b", text.lower())
        return [word for word in words if len(word) > 2]
