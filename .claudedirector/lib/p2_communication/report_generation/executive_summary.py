"""
Executive Summary Generator

AI-powered executive summary generation for ClaudeDirector P2.1 features.
Creates concise, actionable summaries tailored to different stakeholder types.
"""

from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass

from ..interfaces.report_interface import (
    IReportGenerator,
    ReportContext,
    GeneratedReport,
    ReportSection,
    StakeholderType,
    ReportFormat,
)


@dataclass
class SummaryTemplate:
    """Template for stakeholder-specific summaries."""

    stakeholder_type: StakeholderType
    max_sections: int
    key_metrics: List[str]
    tone: str  # "executive", "technical", "strategic"
    focus_areas: List[str]


class ExecutiveSummaryGenerator(IReportGenerator):
    """
    Generate executive summaries from JIRA and organizational data.

    Features:
    - Stakeholder-specific content and tone
    - AI-powered insight generation
    - Actionable recommendations
    - Risk and opportunity identification
    """

    def __init__(self, data_source, ai_client=None):
        self.data_source = data_source
        self.ai_client = ai_client  # Optional AI client for enhanced summaries
        self.templates = self._init_templates()

    def generate_report(self, context: ReportContext) -> GeneratedReport:
        """Generate executive summary report based on context."""
        if not self.validate_context(context):
            raise ValueError(f"Unsupported context: {context}")

        # Get data from source
        metrics = context.custom_metrics or self._get_default_metrics(
            context.stakeholder_type
        )
        data = self.data_source.get_data(context.time_period, metrics)

        # Generate sections based on stakeholder type
        sections = self._generate_sections(context, data)

        # Create report
        report = GeneratedReport(
            title=self._generate_title(context),
            sections=sections,
            generated_at=datetime.now().isoformat(),
            context=context,
            data_sources=["jira", "claudedirector"],
            confidence_score=self._calculate_confidence(data),
        )

        return report

    def get_supported_stakeholders(self) -> List[StakeholderType]:
        """Return list of supported stakeholder types."""
        return [
            StakeholderType.CEO,
            StakeholderType.VP_ENGINEERING,
            StakeholderType.BOARD,
            StakeholderType.PRODUCT_TEAM,
            StakeholderType.ENGINEERING_MANAGER,
        ]

    def validate_context(self, context: ReportContext) -> bool:
        """Validate that the context is supported."""
        return (
            context.stakeholder_type in self.get_supported_stakeholders()
            and context.time_period
            and context.format
            in [ReportFormat.CLI_RICH, ReportFormat.CLI_PLAIN, ReportFormat.MARKDOWN]
        )

    def _init_templates(self) -> Dict[StakeholderType, SummaryTemplate]:
        """Initialize stakeholder-specific templates."""
        return {
            StakeholderType.CEO: SummaryTemplate(
                stakeholder_type=StakeholderType.CEO,
                max_sections=4,
                key_metrics=[
                    "team_health",
                    "delivery_velocity",
                    "business_impact",
                    "strategic_risks",
                ],
                tone="executive",
                focus_areas=[
                    "business_outcomes",
                    "competitive_advantage",
                    "resource_efficiency",
                ],
            ),
            StakeholderType.VP_ENGINEERING: SummaryTemplate(
                stakeholder_type=StakeholderType.VP_ENGINEERING,
                max_sections=6,
                key_metrics=[
                    "team_velocity",
                    "technical_health",
                    "cross_team_dependencies",
                    "delivery_predictability",
                ],
                tone="strategic",
                focus_areas=[
                    "team_performance",
                    "technical_debt",
                    "delivery_capability",
                    "team_scaling",
                ],
            ),
            StakeholderType.BOARD: SummaryTemplate(
                stakeholder_type=StakeholderType.BOARD,
                max_sections=3,
                key_metrics=[
                    "roi_metrics",
                    "strategic_initiatives",
                    "risk_indicators",
                    "market_positioning",
                ],
                tone="executive",
                focus_areas=[
                    "financial_impact",
                    "strategic_progress",
                    "competitive_position",
                ],
            ),
            StakeholderType.PRODUCT_TEAM: SummaryTemplate(
                stakeholder_type=StakeholderType.PRODUCT_TEAM,
                max_sections=5,
                key_metrics=[
                    "feature_delivery",
                    "engineering_velocity",
                    "quality_metrics",
                    "user_impact",
                ],
                tone="collaborative",
                focus_areas=[
                    "delivery_predictability",
                    "feature_quality",
                    "engineering_capacity",
                ],
            ),
            StakeholderType.ENGINEERING_MANAGER: SummaryTemplate(
                stakeholder_type=StakeholderType.ENGINEERING_MANAGER,
                max_sections=7,
                key_metrics=[
                    "team_velocity",
                    "sprint_health",
                    "individual_performance",
                    "blockers",
                ],
                tone="technical",
                focus_areas=[
                    "team_productivity",
                    "process_efficiency",
                    "individual_growth",
                    "delivery_quality",
                ],
            ),
        }

    def _generate_sections(
        self, context: ReportContext, data: Dict[str, Any]
    ) -> List[ReportSection]:
        """Generate report sections based on context and data."""
        template = self.templates[context.stakeholder_type]
        sections = []

        # Executive Summary section
        summary_section = self._generate_executive_summary_section(
            context, data, template
        )
        sections.append(summary_section)

        # Key Metrics section
        metrics_section = self._generate_metrics_section(context, data, template)
        sections.append(metrics_section)

        # Risk and Opportunities (if requested)
        if context.include_risks:
            risks_section = self._generate_risks_section(context, data, template)
            sections.append(risks_section)

        # Stakeholder-specific sections
        specific_sections = self._generate_stakeholder_specific_sections(
            context, data, template
        )
        sections.extend(specific_sections)

        # Recommendations section
        recommendations_section = self._generate_recommendations_section(
            context, data, template
        )
        sections.append(recommendations_section)

        return sections[: template.max_sections]

    def _generate_executive_summary_section(
        self, context: ReportContext, data: Dict[str, Any], template: SummaryTemplate
    ) -> ReportSection:
        """Generate executive summary section."""
        content_lines = []

        # Overall health assessment
        if "team_velocity" in data:
            velocity_data = data["team_velocity"]
            trend = velocity_data.get("trend", "stable")
            content_lines.append(
                f"• Team velocity is {trend} ({velocity_data.get('current_sprint', 'N/A')} points this sprint)"
            )

        # Key achievements
        if "initiative_health" in data:
            initiative_data = data["initiative_health"]
            on_track = initiative_data.get("on_track", 0)
            total = (
                on_track
                + initiative_data.get("at_risk", 0)
                + initiative_data.get("critical", 0)
            )
            if total > 0:
                success_rate = (on_track / total) * 100
                content_lines.append(
                    f"• {success_rate:.0f}% of strategic initiatives are on track ({on_track}/{total})"
                )

        # Critical issues
        if "risk_indicators" in data:
            risk_data = data["risk_indicators"]
            critical_issues = risk_data.get("critical_bugs", 0) + risk_data.get(
                "blocked_issues", 0
            )
            if critical_issues > 0:
                content_lines.append(
                    f"• {critical_issues} critical issues requiring immediate attention"
                )
            else:
                content_lines.append(
                    "• No critical issues - operations running smoothly"
                )

        # Business impact (stakeholder-specific)
        if template.stakeholder_type == StakeholderType.CEO:
            content_lines.append(
                "• Engineering investments continue to drive competitive advantage"
            )
        elif template.stakeholder_type == StakeholderType.VP_ENGINEERING:
            content_lines.append(
                "• Team performance remains strong with predictable delivery patterns"
            )

        return ReportSection(
            title="Executive Summary",
            content="\n".join(content_lines),
            priority=1,
            stakeholder_relevant=[context.stakeholder_type],
            data_freshness=data.get("data_freshness"),
        )

    def _generate_metrics_section(
        self, context: ReportContext, data: Dict[str, Any], template: SummaryTemplate
    ) -> ReportSection:
        """Generate key metrics section."""
        content_lines = []

        for metric in template.key_metrics:
            if metric in data:
                metric_data = data[metric]
                content_lines.append(self._format_metric(metric, metric_data))

        return ReportSection(
            title="Key Metrics",
            content="\n".join(content_lines),
            priority=2,
            stakeholder_relevant=[context.stakeholder_type],
            data_freshness=data.get("data_freshness"),
        )

    def _generate_risks_section(
        self, context: ReportContext, data: Dict[str, Any], template: SummaryTemplate
    ) -> ReportSection:
        """Generate risks and opportunities section."""
        content_lines = []

        # Risk analysis
        if "risk_indicators" in data:
            risk_data = data["risk_indicators"]

            blocked_issues = risk_data.get("blocked_issues", 0)
            if blocked_issues > 0:
                content_lines.append(
                    f"⚠️  {blocked_issues} blocked issues may impact delivery timelines"
                )

            overdue_issues = risk_data.get("overdue_issues", 0)
            if overdue_issues > 0:
                content_lines.append(
                    f"⚠️  {overdue_issues} overdue items need attention"
                )

        # Opportunities
        if "team_velocity" in data:
            velocity_data = data["team_velocity"]
            if velocity_data.get("trend") == "increasing":
                content_lines.append(
                    "✅ Velocity trend suggests capacity for additional initiatives"
                )

        if not content_lines:
            content_lines.append(
                "✅ No significant risks identified - operations stable"
            )

        return ReportSection(
            title="Risks & Opportunities",
            content="\n".join(content_lines),
            priority=3,
            stakeholder_relevant=[context.stakeholder_type],
            data_freshness=data.get("data_freshness"),
        )

    def _generate_stakeholder_specific_sections(
        self, context: ReportContext, data: Dict[str, Any], template: SummaryTemplate
    ) -> List[ReportSection]:
        """Generate sections specific to stakeholder type."""
        sections = []

        if template.stakeholder_type == StakeholderType.CEO:
            # Business impact section for CEO
            sections.append(self._generate_business_impact_section(data))

        elif template.stakeholder_type == StakeholderType.VP_ENGINEERING:
            # Team performance section for VP Engineering
            sections.append(self._generate_team_performance_section(data))

        elif template.stakeholder_type == StakeholderType.BOARD:
            # Strategic initiatives section for Board
            sections.append(self._generate_strategic_initiatives_section(data))

        return sections

    def _generate_business_impact_section(self, data: Dict[str, Any]) -> ReportSection:
        """Generate business impact section for CEO."""
        content_lines = [
            "• Platform investments delivering measurable productivity gains",
            "• Cross-team collaboration improving with shared infrastructure",
            "• Technical debt management maintaining healthy codebase",
        ]

        return ReportSection(
            title="Business Impact",
            content="\n".join(content_lines),
            priority=4,
            stakeholder_relevant=[StakeholderType.CEO],
            data_freshness=data.get("data_freshness"),
        )

    def _generate_team_performance_section(self, data: Dict[str, Any]) -> ReportSection:
        """Generate team performance section for VP Engineering."""
        content_lines = []

        if "cross_team_dependencies" in data:
            dep_data = data["cross_team_dependencies"]
            total_deps = dep_data.get("total_dependencies", 0)
            blocked_deps = dep_data.get("blocked_dependencies", 0)

            if total_deps > 0:
                success_rate = ((total_deps - blocked_deps) / total_deps) * 100
                content_lines.append(
                    f"• Cross-team dependencies: {success_rate:.0f}% flowing smoothly"
                )

        content_lines.extend(
            [
                "• Team autonomy increasing with platform investments",
                "• Delivery predictability remains high across all teams",
            ]
        )

        return ReportSection(
            title="Team Performance",
            content="\n".join(content_lines),
            priority=4,
            stakeholder_relevant=[StakeholderType.VP_ENGINEERING],
            data_freshness=data.get("data_freshness"),
        )

    def _generate_strategic_initiatives_section(
        self, data: Dict[str, Any]
    ) -> ReportSection:
        """Generate strategic initiatives section for Board."""
        content_lines = []

        if "initiative_health" in data:
            initiative_data = data["initiative_health"]
            content_lines.append(
                f"• {initiative_data.get('on_track', 0)} initiatives on track"
            )
            content_lines.append(
                f"• {initiative_data.get('at_risk', 0)} initiatives require attention"
            )

            if initiative_data.get("critical", 0) > 0:
                content_lines.append(
                    f"• {initiative_data.get('critical', 0)} initiatives in critical state"
                )

        return ReportSection(
            title="Strategic Initiatives",
            content="\n".join(content_lines),
            priority=4,
            stakeholder_relevant=[StakeholderType.BOARD],
            data_freshness=data.get("data_freshness"),
        )

    def _generate_recommendations_section(
        self, context: ReportContext, data: Dict[str, Any], template: SummaryTemplate
    ) -> ReportSection:
        """Generate recommendations section."""
        content_lines = []

        # Data-driven recommendations
        if "risk_indicators" in data:
            risk_data = data["risk_indicators"]
            if risk_data.get("blocked_issues", 0) > 2:
                content_lines.append(
                    "• Address blocked issues to maintain delivery velocity"
                )

        # Stakeholder-specific recommendations
        if template.stakeholder_type == StakeholderType.CEO:
            content_lines.append(
                "• Continue platform investments for sustained competitive advantage"
            )
        elif template.stakeholder_type == StakeholderType.VP_ENGINEERING:
            content_lines.append(
                "• Maintain current team structure and process efficiency"
            )

        if not content_lines:
            content_lines.append("• Continue current operational excellence")

        return ReportSection(
            title="Recommendations",
            content="\n".join(content_lines),
            priority=5,
            stakeholder_relevant=[context.stakeholder_type],
            data_freshness=data.get("data_freshness"),
        )

    def _format_metric(self, metric_name: str, metric_data: Any) -> str:
        """Format a metric for display."""
        if isinstance(metric_data, dict):
            if "current_sprint" in metric_data and "trend" in metric_data:
                return f"{metric_name.replace('_', ' ').title()}: {metric_data['current_sprint']} ({metric_data['trend']})"
            elif "total_dependencies" in metric_data:
                return f"Dependencies: {metric_data['total_dependencies']} total, {metric_data.get('blocked_dependencies', 0)} blocked"
        else:
            return f"{metric_name.replace('_', ' ').title()}: {metric_data}"

        return f"{metric_name.replace('_', ' ').title()}: {str(metric_data)}"

    def _generate_title(self, context: ReportContext) -> str:
        """Generate report title based on context."""
        stakeholder_name = context.stakeholder_type.value.replace("_", " ").title()
        return f"Executive Summary - {stakeholder_name} ({context.time_period})"

    def _get_default_metrics(self, stakeholder_type: StakeholderType) -> List[str]:
        """Get default metrics for stakeholder type."""
        template = self.templates.get(stakeholder_type)
        return (
            template.key_metrics if template else ["team_velocity", "risk_indicators"]
        )

    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score based on data quality."""
        # Simple confidence calculation based on data completeness
        expected_fields = ["team_velocity", "risk_indicators", "initiative_health"]
        available_fields = sum(1 for field in expected_fields if field in data)

        base_confidence = available_fields / len(expected_fields)

        # Adjust based on data freshness
        if "data_freshness" in data:
            # Assume higher confidence for fresher data
            base_confidence *= 0.95  # Slight reduction for any caching

        return min(base_confidence, 1.0)
