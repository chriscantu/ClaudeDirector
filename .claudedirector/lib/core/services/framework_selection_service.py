"""
Framework Selection Service - SOLID Refactoring Phase 1

Implements framework selection logic with Single Responsibility Principle (SRP).
This service is focused solely on selecting the most appropriate framework
for a given context, extracted from the monolithic EmbeddedFrameworkEngine.

Author: Martin (SOLID Refactoring Implementation)
"""

from typing import List, Optional
import structlog
from dataclasses import dataclass

from ..interfaces.framework_provider_interface import (
    IFrameworkProvider,
    FrameworkContext,
    FrameworkDomain,
    AnalysisComplexity,
    FrameworkDefinition,
)

logger = structlog.get_logger(__name__)


@dataclass
class FrameworkMatch:
    """Represents a framework match with scoring details"""

    framework_name: str
    relevance_score: float
    keyword_matches: List[str]
    domain_matches: List[FrameworkDomain]
    complexity_match: bool
    confidence_threshold_met: bool


class FrameworkSelectionService:
    """
    Service responsible for selecting the most appropriate framework for analysis.

    Implements Single Responsibility Principle (SRP) by focusing only on framework
    selection logic. Depends on abstractions (IFrameworkProvider) following
    Dependency Inversion Principle (DIP).
    """

    def __init__(self, framework_provider: IFrameworkProvider):
        self.framework_provider = framework_provider

        # Selection configuration
        self.min_relevance_threshold = 0.3
        self.keyword_weight = 0.4
        self.domain_weight = 0.3
        self.complexity_weight = 0.2
        self.context_weight = 0.1

        # Strategic keywords for enhanced matching
        self.strategic_keywords = {
            "organizational": [
                "team",
                "organization",
                "structure",
                "people",
                "culture",
                "leadership",
                "management",
                "coordination",
                "collaboration",
                "stakeholder",
                "communication",
                "alignment",
                "governance",
            ],
            "technical": [
                "architecture",
                "system",
                "platform",
                "technology",
                "technical",
                "infrastructure",
                "design",
                "implementation",
                "development",
                "engineering",
                "code",
                "software",
                "api",
                "service",
            ],
            "strategic": [
                "strategy",
                "strategic",
                "planning",
                "roadmap",
                "vision",
                "goals",
                "objectives",
                "priorities",
                "investment",
                "decision",
                "business",
                "market",
                "competitive",
                "growth",
                "scaling",
            ],
            "financial": [
                "budget",
                "cost",
                "investment",
                "roi",
                "financial",
                "funding",
                "resource",
                "allocation",
                "efficiency",
                "optimization",
                "value",
            ],
            "design": [
                "design",
                "user",
                "experience",
                "interface",
                "usability",
                "accessibility",
                "visual",
                "component",
                "system",
                "pattern",
            ],
        }

    def select_framework(
        self,
        context: FrameworkContext,
        available_frameworks: Optional[List[str]] = None,
    ) -> Optional[str]:
        """
        Select the most appropriate framework for the given context.

        Args:
            context: Analysis context with user input and metadata
            available_frameworks: Optional list to limit selection from

        Returns:
            Name of selected framework or None if no suitable match
        """
        try:
            # Get available frameworks
            if available_frameworks is None:
                available_frameworks = (
                    self.framework_provider.get_available_frameworks()
                )

            if not available_frameworks:
                logger.warning("No frameworks available for selection")
                return None

            # Score all frameworks
            framework_matches = []
            for framework_name in available_frameworks:
                relevance_score = self.calculate_framework_relevance(
                    framework_name, context
                )

                if relevance_score >= self.min_relevance_threshold:
                    framework_def = self.framework_provider.get_framework_definition(
                        framework_name
                    )
                    if framework_def:
                        match = self._create_framework_match(
                            framework_name, framework_def, context, relevance_score
                        )
                        framework_matches.append(match)

            if not framework_matches:
                logger.info(
                    "No frameworks met relevance threshold",
                    threshold=self.min_relevance_threshold,
                    context_input=context.user_input[:100],
                )
                return None

            # Sort by relevance score and select best match
            framework_matches.sort(key=lambda x: x.relevance_score, reverse=True)
            best_match = framework_matches[0]

            logger.info(
                "Framework selected",
                framework=best_match.framework_name,
                relevance_score=best_match.relevance_score,
                keyword_matches=best_match.keyword_matches,
                domain_matches=[
                    d.value if hasattr(d, "value") else str(d)
                    for d in best_match.domain_matches
                ],
            )

            return best_match.framework_name

        except Exception as e:
            logger.error("Framework selection failed", error=str(e))
            return None

    def calculate_framework_relevance(
        self, framework_name: str, context: FrameworkContext
    ) -> float:
        """
        Calculate relevance score (0.0-1.0) for a framework given context.

        Args:
            framework_name: Name of framework to score
            context: Analysis context

        Returns:
            Relevance score between 0.0 and 1.0
        """
        try:
            framework_def = self.framework_provider.get_framework_definition(
                framework_name
            )
            if not framework_def:
                return 0.0

            # Calculate component scores
            keyword_score = self._calculate_keyword_score(framework_def, context)
            domain_score = self._calculate_domain_score(framework_def, context)
            complexity_score = self._calculate_complexity_score(framework_def, context)
            context_score = self._calculate_context_score(framework_def, context)

            # Weighted combination
            relevance_score = (
                keyword_score * self.keyword_weight
                + domain_score * self.domain_weight
                + complexity_score * self.complexity_weight
                + context_score * self.context_weight
            )

            return min(relevance_score, 1.0)

        except Exception as e:
            logger.error(
                "Relevance calculation failed", framework=framework_name, error=str(e)
            )
            return 0.0

    def get_framework_matches_with_scores(
        self,
        context: FrameworkContext,
        available_frameworks: Optional[List[str]] = None,
    ) -> List[FrameworkMatch]:
        """
        Get all framework matches with detailed scoring information.

        Useful for debugging and understanding selection decisions.
        """
        if available_frameworks is None:
            available_frameworks = self.framework_provider.get_available_frameworks()

        matches = []
        for framework_name in available_frameworks:
            relevance_score = self.calculate_framework_relevance(
                framework_name, context
            )
            framework_def = self.framework_provider.get_framework_definition(
                framework_name
            )

            if framework_def and relevance_score > 0:
                match = self._create_framework_match(
                    framework_name, framework_def, context, relevance_score
                )
                matches.append(match)

        return sorted(matches, key=lambda x: x.relevance_score, reverse=True)

    # Private helper methods

    def _create_framework_match(
        self,
        framework_name: str,
        framework_def: FrameworkDefinition,
        context: FrameworkContext,
        relevance_score: float,
    ) -> FrameworkMatch:
        """Create a FrameworkMatch with detailed scoring information"""
        keyword_matches = self._find_keyword_matches(framework_def, context)
        domain_matches = self._find_domain_matches(framework_def, context)
        complexity_match = self._check_complexity_match(framework_def, context)
        confidence_threshold_met = relevance_score >= framework_def.confidence_threshold

        return FrameworkMatch(
            framework_name=framework_name,
            relevance_score=relevance_score,
            keyword_matches=keyword_matches,
            domain_matches=domain_matches,
            complexity_match=complexity_match,
            confidence_threshold_met=confidence_threshold_met,
        )

    def _calculate_keyword_score(
        self, framework_def: FrameworkDefinition, context: FrameworkContext
    ) -> float:
        """Calculate keyword matching score"""
        user_input_lower = context.user_input.lower()

        # Direct keyword matches
        direct_matches = sum(
            1
            for keyword in framework_def.keywords
            if keyword.lower() in user_input_lower
        )

        # Strategic keyword matches
        strategic_matches = 0
        for domain, keywords in self.strategic_keywords.items():
            domain_matches = sum(
                1 for keyword in keywords if keyword.lower() in user_input_lower
            )
            if domain_matches > 0 and FrameworkDomain(domain) in framework_def.domains:
                strategic_matches += domain_matches

        # Normalize scores
        max_direct = len(framework_def.keywords)
        max_strategic = sum(
            len(keywords)
            for domain, keywords in self.strategic_keywords.items()
            if FrameworkDomain(domain) in framework_def.domains
        )

        direct_score = direct_matches / max_direct if max_direct > 0 else 0
        strategic_score = strategic_matches / max_strategic if max_strategic > 0 else 0

        # Combine with weights
        return (direct_score * 0.7) + (strategic_score * 0.3)

    def _calculate_domain_score(
        self, framework_def: FrameworkDefinition, context: FrameworkContext
    ) -> float:
        """Calculate domain matching score"""
        if not context.domain_hints:
            return 0.5  # Neutral score if no domain hints

        matching_domains = set(framework_def.domains) & set(context.domain_hints)
        return len(matching_domains) / len(context.domain_hints)

    def _calculate_complexity_score(
        self, framework_def: FrameworkDefinition, context: FrameworkContext
    ) -> float:
        """Calculate complexity matching score"""
        # Simple heuristic: frameworks with more components are more complex
        framework_complexity = len(framework_def.analysis_components)

        complexity_mapping = {
            AnalysisComplexity.LOW: (1, 3),
            AnalysisComplexity.MEDIUM: (3, 6),
            AnalysisComplexity.HIGH: (6, 15),
        }

        min_components, max_components = complexity_mapping.get(
            context.complexity_level, (1, 15)
        )

        if min_components <= framework_complexity <= max_components:
            return 1.0
        elif framework_complexity < min_components:
            return 0.7  # Framework might be too simple
        else:
            return 0.5  # Framework might be too complex

    def _calculate_context_score(
        self, framework_def: FrameworkDefinition, context: FrameworkContext
    ) -> float:
        """Calculate contextual matching score"""
        score = 0.0

        # Stakeholder context matching
        if context.stakeholder_context and "stakeholder" in framework_def.keywords:
            score += 0.3

        # Organizational context matching
        if (
            context.organizational_context
            and FrameworkDomain.ORGANIZATIONAL in framework_def.domains
        ):
            score += 0.3

        # Session history relevance
        if context.session_history:
            history_text = " ".join(context.session_history).lower()
            keyword_matches = sum(
                1
                for keyword in framework_def.keywords
                if keyword.lower() in history_text
            )
            if keyword_matches > 0:
                score += 0.4

        return min(score, 1.0)

    def _find_keyword_matches(
        self, framework_def: FrameworkDefinition, context: FrameworkContext
    ) -> List[str]:
        """Find specific keyword matches for debugging"""
        user_input_lower = context.user_input.lower()
        return [
            keyword
            for keyword in framework_def.keywords
            if keyword.lower() in user_input_lower
        ]

    def _find_domain_matches(
        self, framework_def: FrameworkDefinition, context: FrameworkContext
    ) -> List[FrameworkDomain]:
        """Find domain matches for debugging"""
        if not context.domain_hints:
            return []
        return list(set(framework_def.domains) & set(context.domain_hints))

    def _check_complexity_match(
        self, framework_def: FrameworkDefinition, context: FrameworkContext
    ) -> bool:
        """Check if framework complexity matches context complexity"""
        framework_complexity = len(framework_def.analysis_components)

        complexity_ranges = {
            AnalysisComplexity.LOW: (1, 3),
            AnalysisComplexity.MEDIUM: (3, 6),
            AnalysisComplexity.HIGH: (6, 15),
        }

        min_components, max_components = complexity_ranges.get(
            context.complexity_level, (1, 15)
        )

        return min_components <= framework_complexity <= max_components
