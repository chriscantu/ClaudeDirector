"""
Framework Analysis Service - SOLID Refactoring Phase 1

Implements framework analysis logic with Single Responsibility Principle (SRP).
This service is focused solely on executing framework analysis and generating
insights, extracted from the monolithic EmbeddedFrameworkEngine.

Author: Martin (SOLID Refactoring Implementation)
"""

import re
from typing import Dict, List, Optional, Any, Set
import structlog
from dataclasses import dataclass

from ..interfaces.framework_provider_interface import (
    IFrameworkProvider,
    IFrameworkAnalyzer,
    IInsightGenerator,
    FrameworkContext,
    FrameworkDefinition,
    AnalysisInsight,
    FrameworkRecommendation,
    ImplementationStep,
    AnalysisComplexity,
)
from ..config import ClaudeDirectorConfig, get_config

logger = structlog.get_logger(__name__)


@dataclass
class AnalysisComponent:
    """Represents a component of framework analysis"""

    name: str
    questions: List[str]
    deliverables: List[str]
    insights_generated: List[AnalysisInsight]
    confidence: float


class FrameworkAnalysisService:
    """
    Service responsible for executing framework analysis and generating insights.

    Implements Single Responsibility Principle (SRP) by focusing only on analysis
    execution. Depends on abstractions following Dependency Inversion Principle (DIP).
    """

    def __init__(
        self,
        framework_provider: IFrameworkProvider,
        insight_generator: IInsightGenerator,
        config: Optional[ClaudeDirectorConfig] = None,
    ):
        self.framework_provider = framework_provider
        self.config = config or get_config()
        self.insight_generator = insight_generator

        # Analysis configuration
        self.min_insight_confidence = 0.4
        self.max_insights_per_component = 5
        self.recommendation_priority_threshold = 0.6

        # Pattern matching for enhanced analysis
        self.analysis_patterns = {
            "problem_indicators": [
                r"problem",
                r"issue",
                r"challenge",
                r"difficulty",
                r"struggle",
                r"bottleneck",
                r"blocker",
                r"obstacle",
                r"concern",
                r"risk",
            ],
            "solution_indicators": [
                r"solution",
                r"approach",
                r"strategy",
                r"method",
                r"way",
                r"implement",
                r"execute",
                r"achieve",
                r"accomplish",
                r"resolve",
            ],
            "stakeholder_indicators": [
                r"team",
                r"people",
                r"stakeholder",
                r"user",
                r"customer",
                r"executive",
                r"leadership",
                r"management",
                r"developer",
            ],
            "outcome_indicators": [
                r"result",
                r"outcome",
                r"impact",
                r"benefit",
                r"value",
                r"improvement",
                r"success",
                r"goal",
                r"objective",
                r"target",
            ],
        }

    def analyze_with_framework(
        self, framework_name: str, context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """
        Analyze context using the specified framework.

        Args:
            framework_name: Name of framework to use for analysis
            context: Analysis context with user input and metadata

        Returns:
            List of analysis insights generated from framework application
        """
        try:
            framework_def = self.framework_provider.get_framework_definition(framework_name)
            if not framework_def:
                logger.error("Framework definition not found", framework=framework_name)
                return []

            logger.info(
                "Starting framework analysis",
                framework=framework_name,
                input_length=len(context.user_input),
                complexity=context.complexity_level.value,
            )

            # Generate base insights using framework components
            base_insights = self.insight_generator.generate_insights(framework_def, context)

            # Enrich insights with pattern matching and context
            enriched_insights = self.insight_generator.enrich_insights_with_patterns(
                base_insights, context
            )

            # Filter and validate insights
            validated_insights = self._validate_and_filter_insights(enriched_insights, context)

            logger.info(
                "Framework analysis completed",
                framework=framework_name,
                insights_generated=len(validated_insights),
                avg_confidence=(
                    sum(i.confidence for i in validated_insights) / len(validated_insights)
                    if validated_insights
                    else 0
                ),
            )

            return validated_insights

        except Exception as e:
            logger.error("Framework analysis failed", framework=framework_name, error=str(e))
            return []

    def generate_recommendations(
        self, insights: List[AnalysisInsight], context: FrameworkContext
    ) -> List[FrameworkRecommendation]:
        """
        Generate strategic recommendations from analysis insights.

        Args:
            insights: List of analysis insights
            context: Analysis context

        Returns:
            List of strategic recommendations
        """
        try:
            if not insights:
                return []

            # Group insights by category for recommendation generation
            insights_by_category = self._group_insights_by_category(insights)

            recommendations = []
            for category, category_insights in insights_by_category.items():
                category_recommendations = self._generate_category_recommendations(
                    category, category_insights, context
                )
                recommendations.extend(category_recommendations)

            # Prioritize and filter recommendations
            prioritized_recommendations = self._prioritize_recommendations(recommendations, context)

            logger.info(
                "Recommendations generated",
                total_recommendations=len(prioritized_recommendations),
                high_priority=len(
                    [
                        r
                        for r in prioritized_recommendations
                        if r.priority == self.config.get_enum_values("priority_levels")[1]
                    ]
                ),
            )

            return prioritized_recommendations

        except Exception as e:
            logger.error("Recommendation generation failed", error=str(e))
            return []

    def create_implementation_plan(
        self, recommendations: List[FrameworkRecommendation], context: FrameworkContext
    ) -> List[ImplementationStep]:
        """
        Create concrete implementation steps from recommendations.

        Args:
            recommendations: List of strategic recommendations
            context: Analysis context

        Returns:
            List of implementation steps
        """
        try:
            if not recommendations:
                return []

            # Sort recommendations by priority and impact
            sorted_recommendations = self._sort_recommendations_for_implementation(recommendations)

            implementation_steps = []
            step_number = 1

            for recommendation in sorted_recommendations:
                steps = self._create_steps_for_recommendation(recommendation, step_number, context)
                implementation_steps.extend(steps)
                step_number += len(steps)

            # Add dependencies between steps
            implementation_steps = self._add_step_dependencies(implementation_steps)

            logger.info(
                "Implementation plan created",
                total_steps=len(implementation_steps),
                recommendations_covered=len(sorted_recommendations),
            )

            return implementation_steps

        except Exception as e:
            logger.error("Implementation plan creation failed", error=str(e))
            return []

    # Private helper methods

    def _validate_and_filter_insights(
        self, insights: List[AnalysisInsight], context: FrameworkContext
    ) -> List[AnalysisInsight]:
        """Validate and filter insights based on quality criteria"""
        validated_insights = []

        for insight in insights:
            # Check minimum confidence threshold
            if insight.confidence < self.min_insight_confidence:
                continue

            # Check for meaningful content
            if len(insight.insight.strip()) < 10:
                continue

            # Check for evidence support
            if not insight.evidence or len(insight.evidence) == 0:
                continue

            validated_insights.append(insight)

        # Limit insights per category to prevent overwhelming output
        category_counts = {}
        filtered_insights = []

        for insight in validated_insights:
            category = insight.category
            if category_counts.get(category, 0) < self.max_insights_per_component:
                filtered_insights.append(insight)
                category_counts[category] = category_counts.get(category, 0) + 1

        return filtered_insights

    def _group_insights_by_category(
        self, insights: List[AnalysisInsight]
    ) -> Dict[str, List[AnalysisInsight]]:
        """Group insights by category for recommendation generation"""
        grouped = {}
        for insight in insights:
            category = insight.category
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(insight)
        return grouped

    def _generate_category_recommendations(
        self, category: str, insights: List[AnalysisInsight], context: FrameworkContext
    ) -> List[FrameworkRecommendation]:
        """Generate recommendations for a specific category of insights"""
        if not insights:
            return []

        # Calculate category confidence
        avg_confidence = sum(i.confidence for i in insights) / len(insights)

        # Generate recommendation based on category and insights
        recommendation_templates = {
            "current_state": {
                "title": "Current State Assessment",
                "description_template": "Based on analysis of {category}, we recommend conducting a comprehensive assessment of {focus_areas}.",
                "priority": (
                    self.config.get_enum_values("priority_levels")[1]
                    if avg_confidence > 0.7
                    else self.config.get_enum_values("priority_levels")[2]
                ),
                "implementation_effort": self.config.get_enum_values("priority_levels")[2],
                "expected_impact": (
                    self.config.get_enum_values("priority_levels")[1]
                    if avg_confidence > 0.7
                    else self.config.get_enum_values("priority_levels")[2]
                ),
            },
            "stakeholder_mapping": {
                "title": "Stakeholder Alignment Strategy",
                "description_template": "Implement stakeholder alignment initiatives focusing on {focus_areas} to address identified concerns.",
                "priority": self.config.get_enum_values("priority_levels")[1],
                "implementation_effort": self.config.get_enum_values("priority_levels")[1],
                "expected_impact": self.config.get_enum_values("priority_levels")[1],
            },
            "success_metrics": {
                "title": "Success Metrics Framework",
                "description_template": "Establish comprehensive metrics framework for {focus_areas} with clear measurement criteria.",
                "priority": self.config.get_enum_values("priority_levels")[2],
                "implementation_effort": self.config.get_enum_values("priority_levels")[2],
                "expected_impact": self.config.get_enum_values("priority_levels")[2],
            },
            "implementation_roadmap": {
                "title": "Implementation Roadmap",
                "description_template": "Develop detailed implementation roadmap for {focus_areas} with clear milestones and dependencies.",
                "priority": "high",
                "implementation_effort": "high",
                "expected_impact": "high",
            },
            "risk_mitigation": {
                "title": "Risk Mitigation Strategy",
                "description_template": "Implement risk mitigation strategies for {focus_areas} to ensure successful outcomes.",
                "priority": "medium",
                "implementation_effort": "medium",
                "expected_impact": "medium",
            },
        }

        template = recommendation_templates.get(
            category,
            {
                "title": f"{category.replace('_', ' ').title()} Strategy",
                "description_template": "Address {category} considerations through systematic approach to {focus_areas}.",
                "priority": "medium",
                "implementation_effort": "medium",
                "expected_impact": "medium",
            },
        )

        # Extract focus areas from insights
        focus_areas = list(
            set(
                evidence_item
                for insight in insights
                for evidence_item in insight.evidence[:2]  # Limit to top 2 evidence items
            )
        )[
            :3
        ]  # Limit to 3 focus areas

        focus_areas_text = ", ".join(focus_areas) if focus_areas else "identified areas"

        recommendation = FrameworkRecommendation(
            title=template["title"],
            description=template["description_template"].format(
                category=category.replace("_", " "), focus_areas=focus_areas_text
            ),
            priority=template["priority"],
            implementation_effort=template["implementation_effort"],
            expected_impact=template["expected_impact"],
            dependencies=[],
            timeline=self._estimate_timeline(template["implementation_effort"]),
        )

        return [recommendation]

    def _prioritize_recommendations(
        self, recommendations: List[FrameworkRecommendation], context: FrameworkContext
    ) -> List[FrameworkRecommendation]:
        """Prioritize recommendations based on impact and effort"""
        # Priority scoring
        priority_scores = {"high": 3, "medium": 2, "low": 1}
        impact_scores = {"high": 3, "medium": 2, "low": 1}
        effort_scores = {
            "low": 3,
            "medium": 2,
            "high": 1,
        }  # Lower effort = higher score

        def calculate_priority_score(rec: FrameworkRecommendation) -> float:
            priority_score = priority_scores.get(rec.priority, 2)
            impact_score = impact_scores.get(rec.expected_impact, 2)
            effort_score = effort_scores.get(rec.implementation_effort, 2)

            # Weighted combination: impact and priority matter more than effort
            return (priority_score * 0.4) + (impact_score * 0.4) + (effort_score * 0.2)

        # Sort by priority score
        prioritized = sorted(recommendations, key=calculate_priority_score, reverse=True)

        # Limit to reasonable number of recommendations
        max_recommendations = 8
        return prioritized[:max_recommendations]

    def _sort_recommendations_for_implementation(
        self, recommendations: List[FrameworkRecommendation]
    ) -> List[FrameworkRecommendation]:
        """Sort recommendations for optimal implementation order"""

        # Implementation order: high priority first, then by effort (easier first)
        def implementation_sort_key(rec: FrameworkRecommendation) -> tuple:
            priority_order = {"high": 0, "medium": 1, "low": 2}
            effort_order = {"low": 0, "medium": 1, "high": 2}

            return (
                priority_order.get(rec.priority, 1),
                effort_order.get(rec.implementation_effort, 1),
            )

        return sorted(recommendations, key=implementation_sort_key)

    def _create_steps_for_recommendation(
        self,
        recommendation: FrameworkRecommendation,
        starting_step_number: int,
        context: FrameworkContext,
    ) -> List[ImplementationStep]:
        """Create implementation steps for a specific recommendation"""
        steps = []

        # Generate steps based on recommendation type and effort
        if recommendation.implementation_effort == "low":
            num_steps = 2
        elif recommendation.implementation_effort == "medium":
            num_steps = 3
        else:  # high
            num_steps = 4

        step_templates = [
            "Plan and prepare for {title}",
            "Execute initial phase of {title}",
            "Monitor and adjust {title} implementation",
            "Complete and validate {title} outcomes",
        ]

        for i in range(num_steps):
            step = ImplementationStep(
                step_number=starting_step_number + i,
                title=step_templates[i].format(title=recommendation.title),
                description=f"Detailed implementation of {recommendation.description}",
                timeline=self._estimate_step_timeline(
                    recommendation.implementation_effort, i, num_steps
                ),
                dependencies=[],
                success_criteria=[
                    f"Completion criteria for step {i+1} of {recommendation.title}",
                    f"Quality validation for {recommendation.title} phase {i+1}",
                ],
            )
            steps.append(step)

        return steps

    def _add_step_dependencies(self, steps: List[ImplementationStep]) -> List[ImplementationStep]:
        """Add logical dependencies between implementation steps"""
        # Simple dependency logic: each step depends on the previous step
        for i, step in enumerate(steps):
            if i > 0:
                step.dependencies = [steps[i - 1].step_number]

        return steps

    def _estimate_timeline(self, effort: str) -> str:
        """Estimate timeline based on implementation effort"""
        timeline_mapping = {
            "low": "1-2 weeks",
            "medium": "3-6 weeks",
            "high": "2-3 months",
        }
        return timeline_mapping.get(effort, "4-8 weeks")

    def _estimate_step_timeline(self, effort: str, step_index: int, total_steps: int) -> str:
        """Estimate timeline for individual implementation step"""
        base_timelines = {
            "low": ["3-5 days", "5-7 days"],
            "medium": ["1 week", "2 weeks", "1 week"],
            "high": ["2 weeks", "3-4 weeks", "2-3 weeks", "1-2 weeks"],
        }

        timelines = base_timelines.get(effort, ["1 week"] * total_steps)
        return timelines[min(step_index, len(timelines) - 1)]
