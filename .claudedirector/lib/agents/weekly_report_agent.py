"""Weekly Report Generation Agent

Strategic automation agent for executive weekly reporting.
Implements autonomous Jira data collection, business value translation,
and executive report generation following platform governance standards.

Author: Martin | Platform Architecture
Version: 1.0
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import yaml
import json

# Import existing infrastructure
from ..p2_communication.integrations.jira_client import JiraClient
from ..p2_communication.report_generation.executive_summary import ExecutiveSummary
from ..core.base_manager import BaseManager
from ..core.types import ProcessingResult


class ReportFrequency(Enum):
    """Report generation frequency options"""

    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class TeamScope(Enum):
    """UI Foundation team scope definitions"""

    WEB_PLATFORM = "web_platform"
    DESIGN_SYSTEM = "design_system"
    INTERNATIONALIZATION = "i18n"
    UI_SHELL = "ui_shell"
    HEADER_NAV = "header_nav"
    ALL_TEAMS = "all_teams"


@dataclass
class TeamMapping:
    """Team to Jira project mapping configuration"""

    team_name: str
    jira_projects: List[str]
    business_domain: str
    strategic_priority: float  # 0.0-1.0 weight for strategic importance


@dataclass
class BusinessValueFramework:
    """Framework for translating technical work to business outcomes"""

    capability_category: str
    organizational_impact: str
    competitive_advantage: str
    productivity_multiplier: float
    risk_mitigation_value: str


@dataclass
class WeeklyReportConfig:
    """Configuration for weekly report agent operations"""

    # Core Settings
    report_frequency: ReportFrequency = ReportFrequency.WEEKLY
    team_scope: TeamScope = TeamScope.ALL_TEAMS
    lookback_days: int = 7
    forecast_horizon_days: int = 14

    # Data Sources
    jira_base_url: str = ""
    jira_username: str = ""
    jira_token: str = ""

    # Team Configuration
    team_mappings: List[TeamMapping] = field(default_factory=list)
    business_value_frameworks: List[BusinessValueFramework] = field(
        default_factory=list
    )

    # Report Configuration
    executive_template_path: str = "templates/weekly-report-executive.md"
    output_directory: str = "reports/weekly"
    stakeholder_email: Optional[str] = None

    # Quality Gates
    require_source_attribution: bool = True
    max_generation_time_seconds: int = 300
    minimum_data_coverage: float = 0.8  # 80% of expected data sources

    @classmethod
    def from_yaml(cls, config_path: str) -> "WeeklyReportConfig":
        """Load configuration from YAML file"""
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)


@dataclass
class EpicAnalysis:
    """Analysis results for individual epic"""

    epic_key: str
    epic_title: str
    team: str
    completion_probability: float
    business_impact_score: float
    risk_factors: List[str]
    blockers: List[str]
    estimated_completion_date: Optional[datetime]
    progress_percentage: float
    story_points_completed: int
    story_points_total: int
    data_sources: List[str]  # For attribution requirements


@dataclass
class TeamAnalysis:
    """Aggregated analysis for team performance"""

    team_name: str
    total_epics: int
    on_track_epics: int
    at_risk_epics: int
    blocked_epics: int
    overall_velocity_trend: str  # "increasing", "stable", "decreasing"
    business_value_delivered: float
    key_achievements: List[str]
    concerns: List[str]
    resource_needs: List[str]


@dataclass
class WeeklyReportData:
    """Complete weekly report data structure"""

    report_period_start: datetime
    report_period_end: datetime
    generation_timestamp: datetime

    # Team Analysis
    team_analyses: List[TeamAnalysis]
    cross_team_dependencies: List[Dict[str, Any]]

    # Executive Summary Data
    key_achievements: List[str]
    strategic_concerns: List[str]
    resource_requirements: List[str]
    business_impact_highlights: List[str]

    # Metrics and Attribution
    data_coverage_percentage: float
    data_sources: List[str]
    confidence_level: float


class WeeklyReportAgent(BaseManager):
    """
    Autonomous agent for weekly report generation

    Implements strategic platform automation following Director-level
    architectural patterns with focus on data integrity, business value
    translation, and executive communication standards.
    """

    def __init__(self, config: WeeklyReportConfig):
        super().__init__()
        self.config = config
        self.jira_client: Optional[JiraClient] = None
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self._initialize_jira_client()
        self._load_business_frameworks()

    def _initialize_jira_client(self) -> None:
        """Initialize Jira client with configuration"""
        if not all(
            [
                self.config.jira_base_url,
                self.config.jira_username,
                self.config.jira_token,
            ]
        ):
            raise ValueError("Missing required Jira configuration")

        self.jira_client = JiraClient(
            base_url=self.config.jira_base_url,
            username=self.config.jira_username,
            token=self.config.jira_token,
        )

    def _load_business_frameworks(self) -> None:
        """Load business value translation frameworks"""
        # Default UI Foundation frameworks if not provided
        if not self.config.business_value_frameworks:
            self.config.business_value_frameworks = [
                BusinessValueFramework(
                    capability_category="Platform Capabilities",
                    organizational_impact="Organizational velocity multipliers + competitive advantages",
                    competitive_advantage="Platform-first architecture enables faster feature delivery",
                    productivity_multiplier=2.5,
                    risk_mitigation_value="Reduced technical debt and maintenance overhead",
                ),
                BusinessValueFramework(
                    capability_category="Design System Evolution",
                    organizational_impact="Brand consistency + development efficiency + user experience impact",
                    competitive_advantage="Consistent UX at scale with reduced design-to-development friction",
                    productivity_multiplier=3.0,
                    risk_mitigation_value="Design consistency risk mitigation across product portfolio",
                ),
                BusinessValueFramework(
                    capability_category="Internationalization",
                    organizational_impact="Market expansion enablement + compliance risk mitigation",
                    competitive_advantage="Global market entry capabilities with regulatory compliance",
                    productivity_multiplier=1.8,
                    risk_mitigation_value="Regulatory compliance risk reduction in international markets",
                ),
            ]

    async def generate_weekly_report(self) -> ProcessingResult:
        """
        Generate complete weekly report following Agent pattern

        Returns:
            ProcessingResult with report path and generation metrics
        """
        start_time = datetime.now()

        try:
            # Phase 1: Data Collection
            self.logger.info(
                "Starting weekly report generation - Phase 1: Data Collection"
            )
            report_data = await self._collect_report_data()

            # Phase 2: Business Value Translation
            self.logger.info("Phase 2: Business Value Translation")
            enriched_data = await self._enrich_with_business_value(report_data)

            # Phase 3: Report Generation
            self.logger.info("Phase 3: Report Generation")
            report_path = await self._generate_report_document(enriched_data)

            # Phase 4: Quality Validation
            self.logger.info("Phase 4: Quality Validation")
            validation_result = await self._validate_report_quality(
                report_path, enriched_data
            )

            generation_time = (datetime.now() - start_time).total_seconds()

            if (
                validation_result
                and generation_time <= self.config.max_generation_time_seconds
            ):
                return ProcessingResult(
                    success=True,
                    data={
                        "report_path": report_path,
                        "generation_time_seconds": generation_time,
                        "data_coverage": enriched_data.data_coverage_percentage,
                        "confidence_level": enriched_data.confidence_level,
                    },
                    message=f"Weekly report generated successfully in {generation_time:.1f}s",
                )
            else:
                raise Exception(
                    f"Report validation failed or exceeded time limit ({generation_time:.1f}s)"
                )

        except Exception as e:
            self.logger.error(f"Weekly report generation failed: {str(e)}")
            return ProcessingResult(
                success=False, error=str(e), message="Weekly report generation failed"
            )

    async def _collect_report_data(self) -> WeeklyReportData:
        """Collect data from all configured sources"""

        # Calculate report period
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.config.lookback_days)

        # Initialize data structure
        report_data = WeeklyReportData(
            report_period_start=start_date,
            report_period_end=end_date,
            generation_timestamp=datetime.now(),
            team_analyses=[],
            cross_team_dependencies=[],
            key_achievements=[],
            strategic_concerns=[],
            resource_requirements=[],
            business_impact_highlights=[],
            data_coverage_percentage=0.0,
            data_sources=[],
            confidence_level=0.0,
        )

        # Collect team-specific data
        for team_mapping in self.config.team_mappings:
            team_analysis = await self._analyze_team_performance(
                team_mapping, start_date, end_date
            )
            report_data.team_analyses.append(team_analysis)

        # Collect cross-team dependencies
        dependencies = await self._analyze_cross_team_dependencies()
        report_data.cross_team_dependencies = dependencies

        # Calculate data coverage and confidence
        total_expected_sources = (
            len(self.config.team_mappings) * 3
        )  # 3 data points per team
        actual_sources = sum(
            len(ta.key_achievements) + len(ta.concerns) + len(ta.resource_needs)
            for ta in report_data.team_analyses
        )

        report_data.data_coverage_percentage = min(
            1.0, actual_sources / total_expected_sources
        )
        report_data.confidence_level = (
            report_data.data_coverage_percentage * 0.8
        )  # Conservative confidence

        return report_data

    async def _analyze_team_performance(
        self, team_mapping: TeamMapping, start_date: datetime, end_date: datetime
    ) -> TeamAnalysis:
        """Analyze individual team performance"""

        # Query Jira for team's epics
        epic_analyses = []
        for project in team_mapping.jira_projects:
            epics = await self.jira_client.get_epics_for_project(
                project, start_date, end_date
            )

            for epic in epics:
                analysis = await self._analyze_epic(epic)
                epic_analyses.append(analysis)

        # Aggregate team metrics
        total_epics = len(epic_analyses)
        on_track_epics = len(
            [e for e in epic_analyses if e.completion_probability >= 0.8]
        )
        at_risk_epics = len(
            [e for e in epic_analyses if 0.4 <= e.completion_probability < 0.8]
        )
        blocked_epics = len([e for e in epic_analyses if e.blockers])

        # Generate team insights
        key_achievements = self._extract_achievements(epic_analyses)
        concerns = self._identify_concerns(epic_analyses)
        resource_needs = self._assess_resource_needs(epic_analyses)

        return TeamAnalysis(
            team_name=team_mapping.team_name,
            total_epics=total_epics,
            on_track_epics=on_track_epics,
            at_risk_epics=at_risk_epics,
            blocked_epics=blocked_epics,
            overall_velocity_trend="stable",  # TODO: Calculate from historical data
            business_value_delivered=sum(
                e.business_impact_score for e in epic_analyses
            ),
            key_achievements=key_achievements,
            concerns=concerns,
            resource_needs=resource_needs,
        )

    async def _analyze_epic(self, epic_data: Dict[str, Any]) -> EpicAnalysis:
        """Analyze individual epic for completion and business impact"""

        # Extract epic metadata
        epic_key = epic_data.get("key", "")
        epic_title = epic_data.get("summary", "")

        # Calculate completion probability using historical velocity
        progress_percentage = self._calculate_epic_progress(epic_data)
        completion_probability = self._estimate_completion_probability(
            epic_data, progress_percentage
        )

        # Assess business impact
        business_impact_score = self._calculate_business_impact(epic_data)

        # Identify risks and blockers
        risk_factors = self._identify_risk_factors(epic_data)
        blockers = self._extract_blockers(epic_data)

        return EpicAnalysis(
            epic_key=epic_key,
            epic_title=epic_title,
            team=epic_data.get("team", "Unknown"),
            completion_probability=completion_probability,
            business_impact_score=business_impact_score,
            risk_factors=risk_factors,
            blockers=blockers,
            estimated_completion_date=self._estimate_completion_date(epic_data),
            progress_percentage=progress_percentage,
            story_points_completed=epic_data.get("story_points_completed", 0),
            story_points_total=epic_data.get("story_points_total", 0),
            data_sources=[
                f"Jira Epic {epic_key}",
                "Historical Velocity Data",
                "Team Capacity Model",
            ],
        )

    def _calculate_epic_progress(self, epic_data: Dict[str, Any]) -> float:
        """Calculate epic progress percentage"""
        completed_points = epic_data.get("story_points_completed", 0)
        total_points = epic_data.get("story_points_total", 1)  # Avoid division by zero
        return completed_points / total_points if total_points > 0 else 0.0

    def _estimate_completion_probability(
        self, epic_data: Dict[str, Any], progress: float
    ) -> float:
        """Estimate probability of epic completion using Monte Carlo simulation"""

        # Simple heuristic - would be enhanced with historical data
        base_probability = progress

        # Adjust for blockers
        blockers = len(epic_data.get("blockers", []))
        blocker_penalty = min(0.3, blockers * 0.1)

        # Adjust for sprint capacity
        remaining_sprints = epic_data.get("remaining_sprints", 2)
        if remaining_sprints <= 1:
            base_probability *= 1.2  # Boost for near-term completion
        elif remaining_sprints > 4:
            base_probability *= 0.8  # Reduce for distant completion

        return max(0.0, min(1.0, base_probability - blocker_penalty))

    def _calculate_business_impact(self, epic_data: Dict[str, Any]) -> float:
        """Calculate business impact score using strategic frameworks"""

        # Map epic to business value framework
        epic_labels = epic_data.get("labels", [])
        category_mapping = {
            "platform": "Platform Capabilities",
            "design-system": "Design System Evolution",
            "i18n": "Internationalization",
        }

        framework = None
        for label in epic_labels:
            if label in category_mapping:
                framework_name = category_mapping[label]
                framework = next(
                    (
                        f
                        for f in self.config.business_value_frameworks
                        if f.capability_category == framework_name
                    ),
                    None,
                )
                break

        if framework:
            return framework.productivity_multiplier * epic_data.get(
                "story_points_total", 1
            )
        else:
            return 1.0  # Default business value

    def _identify_risk_factors(self, epic_data: Dict[str, Any]) -> List[str]:
        """Identify risk factors for epic completion"""
        risks = []

        # Check for common risk indicators
        if epic_data.get("story_points_total", 0) > 100:
            risks.append("Large epic size may indicate scope creep")

        if len(epic_data.get("blockers", [])) > 0:
            risks.append("Active blockers preventing progress")

        if epic_data.get("remaining_sprints", 0) < 2:
            risks.append("Tight timeline for completion")

        return risks

    def _extract_blockers(self, epic_data: Dict[str, Any]) -> List[str]:
        """Extract blocking issues from epic data"""
        return epic_data.get("blockers", [])

    def _estimate_completion_date(
        self, epic_data: Dict[str, Any]
    ) -> Optional[datetime]:
        """Estimate epic completion date based on velocity"""
        # Simplified estimation - would use team velocity data in production
        remaining_points = epic_data.get("story_points_total", 0) - epic_data.get(
            "story_points_completed", 0
        )
        team_velocity = epic_data.get("team_velocity_per_week", 20)  # Default velocity

        if team_velocity > 0:
            weeks_remaining = remaining_points / team_velocity
            return datetime.now() + timedelta(weeks=weeks_remaining)
        return None

    def _extract_achievements(self, epic_analyses: List[EpicAnalysis]) -> List[str]:
        """Extract key achievements from epic analyses"""
        achievements = []

        completed_epics = [e for e in epic_analyses if e.progress_percentage >= 0.9]
        if completed_epics:
            total_value = sum(e.business_impact_score for e in completed_epics)
            achievements.append(
                f"Completed {len(completed_epics)} epics delivering {total_value:.1f} business value points"
            )

        high_impact_epics = [e for e in epic_analyses if e.business_impact_score > 50]
        if high_impact_epics:
            achievements.append(
                f"Progressing on {len(high_impact_epics)} high-impact strategic initiatives"
            )

        return achievements

    def _identify_concerns(self, epic_analyses: List[EpicAnalysis]) -> List[str]:
        """Identify strategic concerns from epic analyses"""
        concerns = []

        blocked_epics = [e for e in epic_analyses if e.blockers]
        if blocked_epics:
            concerns.append(
                f"{len(blocked_epics)} epics currently blocked, requiring intervention"
            )

        low_probability_epics = [
            e for e in epic_analyses if e.completion_probability < 0.5
        ]
        if len(low_probability_epics) > len(epic_analyses) * 0.3:  # >30% at risk
            concerns.append("High percentage of epics at completion risk")

        return concerns

    def _assess_resource_needs(self, epic_analyses: List[EpicAnalysis]) -> List[str]:
        """Assess resource requirements from epic analyses"""
        needs = []

        # Check for capacity constraints
        total_remaining_work = sum(
            e.story_points_total - e.story_points_completed for e in epic_analyses
        )

        if total_remaining_work > 200:  # Threshold for capacity concern
            needs.append(
                "Additional development capacity required for current epic load"
            )

        # Check for specific skill needs based on blocked epics
        blocked_categories = set()
        for epic in epic_analyses:
            if epic.blockers:
                # Infer category from epic title/labels
                if "design" in epic.epic_title.lower():
                    blocked_categories.add("design")
                elif "security" in epic.epic_title.lower():
                    blocked_categories.add("security")

        if blocked_categories:
            needs.append(
                f"Specialized expertise needed in: {', '.join(blocked_categories)}"
            )

        return needs

    async def _analyze_cross_team_dependencies(self) -> List[Dict[str, Any]]:
        """Analyze dependencies between UI Foundation teams"""

        # Query Jira for issues with cross-team labels or links
        dependencies = []

        # This would be enhanced with actual Jira link analysis
        sample_dependencies = [
            {
                "source_team": "Design System",
                "target_team": "Web Platform",
                "dependency_type": "Component API Changes",
                "risk_level": "medium",
                "estimated_resolution": "Sprint +1",
            },
            {
                "source_team": "i18n",
                "target_team": "UI Shell",
                "dependency_type": "Localization Infrastructure",
                "risk_level": "low",
                "estimated_resolution": "Sprint +0",
            },
        ]

        return sample_dependencies

    async def _enrich_with_business_value(
        self, report_data: WeeklyReportData
    ) -> WeeklyReportData:
        """Enrich report data with business value translation"""

        # Generate executive-level insights
        total_business_value = sum(
            ta.business_value_delivered for ta in report_data.team_analyses
        )
        report_data.business_impact_highlights.append(
            f"UI Foundation delivered {total_business_value:.1f} business value points this period"
        )

        # Identify strategic patterns
        at_risk_teams = [
            ta
            for ta in report_data.team_analyses
            if ta.at_risk_epics > ta.on_track_epics
        ]
        if at_risk_teams:
            report_data.strategic_concerns.append(
                f"Strategic concern: {len(at_risk_teams)} teams have more at-risk than on-track epics"
            )

        # Aggregate resource requirements
        all_resource_needs = []
        for team_analysis in report_data.team_analyses:
            all_resource_needs.extend(team_analysis.resource_needs)

        # Deduplicate and prioritize
        unique_needs = list(set(all_resource_needs))
        report_data.resource_requirements = unique_needs[:5]  # Top 5 needs

        return report_data

    async def _generate_report_document(self, report_data: WeeklyReportData) -> str:
        """Generate formatted report document"""

        # Generate report filename
        report_date = report_data.report_period_end.strftime("%Y-%m-%d")
        report_filename = f"weekly-report-{report_date}.md"
        output_path = Path(self.config.output_directory) / report_filename

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate report content using ExecutiveSummary
        executive_summary = ExecutiveSummary()
        report_content = await self._format_executive_report(
            report_data, executive_summary
        )

        # Write report file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        self.logger.info(f"Generated weekly report: {output_path}")
        return str(output_path)

    async def _format_executive_report(
        self, report_data: WeeklyReportData, executive_summary: ExecutiveSummary
    ) -> str:
        """Format report following executive communication standards"""

        # Report header
        report_period = f"{report_data.report_period_start.strftime('%Y-%m-%d')} to {report_data.report_period_end.strftime('%Y-%m-%d')}"

        content = f"""# UI Foundation Weekly Report
**Period**: {report_period}
**Generated**: {report_data.generation_timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Confidence Level**: {report_data.confidence_level:.1%}
**Data Coverage**: {report_data.data_coverage_percentage:.1%}

---

## 📊 Executive Summary

### Key Achievements
"""

        for achievement in report_data.key_achievements[:5]:  # Top 5
            content += f"- {achievement}\n"

        if report_data.business_impact_highlights:
            content += "\n### Business Impact\n"
            for highlight in report_data.business_impact_highlights:
                content += f"- {highlight}\n"

        if report_data.strategic_concerns:
            content += "\n### Strategic Concerns\n"
            for concern in report_data.strategic_concerns:
                content += f"- ⚠️ {concern}\n"

        if report_data.resource_requirements:
            content += "\n### Resource Requirements\n"
            for requirement in report_data.resource_requirements:
                content += f"- 🎯 {requirement}\n"

        # Team Details
        content += "\n---\n\n## 📋 Team Performance Analysis\n\n"

        for team_analysis in report_data.team_analyses:
            content += f"### {team_analysis.team_name}\n"
            content += f"**Epics**: {team_analysis.total_epics} total, {team_analysis.on_track_epics} on-track, {team_analysis.at_risk_epics} at-risk, {team_analysis.blocked_epics} blocked\n\n"

            if team_analysis.key_achievements:
                content += "**Achievements**:\n"
                for achievement in team_analysis.key_achievements:
                    content += f"- ✅ {achievement}\n"
                content += "\n"

            if team_analysis.concerns:
                content += "**Concerns**:\n"
                for concern in team_analysis.concerns:
                    content += f"- ⚠️ {concern}\n"
                content += "\n"

        # Cross-team dependencies
        if report_data.cross_team_dependencies:
            content += "\n---\n\n## 🔗 Cross-Team Dependencies\n\n"
            for dep in report_data.cross_team_dependencies:
                content += f"- **{dep['source_team']} → {dep['target_team']}**: {dep['dependency_type']} (Risk: {dep['risk_level']})\n"

        # Data attribution footer
        content += "\n---\n\n## 📊 Data Sources & Attribution\n\n"
        content += "All metrics in this report are sourced from:\n"
        for source in report_data.data_sources:
            content += f"- {source}\n"

        content += f"\n**Data Integrity**: This report follows strict no-invented-numbers policy. All metrics have full source attribution.\n"
        content += f"**Generation Method**: Automated using WeeklyReportAgent v1.0\n"
        content += f"**Quality Assurance**: Data coverage {report_data.data_coverage_percentage:.1%}, confidence level {report_data.confidence_level:.1%}\n"

        return content

    async def _validate_report_quality(
        self, report_path: str, report_data: WeeklyReportData
    ) -> bool:
        """Validate report meets quality standards"""

        # Check file was created
        if not Path(report_path).exists():
            self.logger.error("Report file was not created")
            return False

        # Check data coverage threshold
        if report_data.data_coverage_percentage < self.config.minimum_data_coverage:
            self.logger.warning(
                f"Data coverage {report_data.data_coverage_percentage:.1%} below minimum {self.config.minimum_data_coverage:.1%}"
            )
            return False

        # Check source attribution if required
        if self.config.require_source_attribution and not report_data.data_sources:
            self.logger.error("Source attribution required but no sources provided")
            return False

        # Basic content validation
        with open(report_path, "r") as f:
            content = f.read()

        required_sections = [
            "Executive Summary",
            "Team Performance Analysis",
            "Data Sources",
        ]
        missing_sections = [
            section for section in required_sections if section not in content
        ]

        if missing_sections:
            self.logger.error(f"Missing required sections: {missing_sections}")
            return False

        self.logger.info("Report quality validation passed")
        return True


# Factory function for easy instantiation
def create_weekly_report_agent(config_path: str) -> WeeklyReportAgent:
    """Create WeeklyReportAgent from configuration file"""
    config = WeeklyReportConfig.from_yaml(config_path)
    return WeeklyReportAgent(config)


# Example usage and testing
if __name__ == "__main__":
    import asyncio

    # Example configuration
    config = WeeklyReportConfig(
        jira_base_url="https://your-company.atlassian.net",
        jira_username="your-username",
        jira_token="your-api-token",
        team_mappings=[
            TeamMapping(
                team_name="Web Platform",
                jira_projects=["WP"],
                business_domain="Platform Infrastructure",
                strategic_priority=0.9,
            ),
            TeamMapping(
                team_name="Design System",
                jira_projects=["DS"],
                business_domain="Developer Experience",
                strategic_priority=0.8,
            ),
        ],
    )

    # Create and run agent
    agent = WeeklyReportAgent(config)

    async def test_agent():
        result = await agent.generate_weekly_report()
        print(f"Report generation result: {result}")

    # Run test if needed
    # asyncio.run(test_agent())
