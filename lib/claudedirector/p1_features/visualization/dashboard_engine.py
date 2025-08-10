#!/usr/bin/env python3
"""
P1.1 Dashboard Engine
Rachel-approved visual dashboard orchestration with design system consistency
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from lib.claudedirector.p1_features.organizational_intelligence import (
    DirectorProfileManager,
)
from .visual_components import (
    ImpactScoreIndicator,
    DomainPerformanceChart,
    TrendSparkline,
    ExecutiveSummaryWidget,
    ROIVisualization,
    visualization_factory,
)
from .design_system import design_system, ComponentSize
from .interfaces import (
    DashboardEngineInterface,
    ProfileManagerInterface,
    DataGeneratorInterface,
    DesignSystemInterface,
)
from .data_generator import SampleDataGenerator
from .config_manager import visualization_config


@dataclass
class DashboardLayout:
    """Dashboard layout configuration following Rachel's design system"""

    # Layout type
    layout_type: str = "executive"  # executive, technical, comparative

    # Component sizes
    impact_score_size: ComponentSize = ComponentSize.LG
    chart_width: int = 60
    sparkline_width: int = 20

    # Display preferences
    show_trends: bool = True
    show_roi: bool = True
    show_executive_summary: bool = True
    compact_mode: bool = False


class DashboardEngine(DashboardEngineInterface):
    """
    Main dashboard engine coordinating all visual components
    Rachel's design: Consistent, accessible, executive-focused
    Implements dependency injection (Dependency Inversion Principle)
    """

    def __init__(
        self,
        profile_manager: Optional[ProfileManagerInterface] = None,
        data_generator: Optional[DataGeneratorInterface] = None,
        design_system_impl: Optional[DesignSystemInterface] = None,
        config_path: Optional[str] = None,
    ):
        # Dependency injection - follows Dependency Inversion Principle
        self.profile_manager = profile_manager or DirectorProfileManager(
            config_path or "config/p1_organizational_intelligence.yaml"
        )
        self.data_generator = data_generator or SampleDataGenerator()
        self.design_system = design_system_impl or design_system
        self.layout = DashboardLayout()
        self.config = visualization_config

    def render_executive_dashboard(self, sample_data: bool = False) -> str:
        """
        Render complete executive dashboard
        Rachel approved: Clear visual hierarchy, scannable layout
        """
        output = []

        # Dashboard header
        output.append(self._render_dashboard_header())
        output.append("")

        # Get organizational data
        org_data = self._get_organizational_data(sample_data)

        # 1. Impact Score (Primary KPI)
        output.append(self._render_impact_score_section(org_data))
        output.append("")

        # 2. Domain Performance (Secondary KPIs)
        output.append(self._render_domain_performance_section(org_data))
        output.append("")

        # 3. Trend Analysis (if enabled)
        if self.layout.show_trends:
            output.append(self._render_trend_analysis_section(org_data))
            output.append("")

        # 4. Investment ROI (if enabled)
        if self.layout.show_roi:
            output.append(self._render_roi_section(org_data))
            output.append("")

        # 5. Executive Summary (if enabled)
        if self.layout.show_executive_summary:
            output.append(self._render_executive_summary_section(org_data))

        return "\n".join(output)

    def _render_dashboard_header(self) -> str:
        """Render dashboard header with director profile info"""
        profile = self.profile_manager.current_profile

        return f"""
╭─────────────────────────────────────────────────────────────────────────────╮
│                        ORGANIZATIONAL INTELLIGENCE DASHBOARD                 │
│                                                                             │
│ 👤 {profile.role_title:<67} │
│ 🔍 {profile.primary_focus:<67} │
│ 📊 Dashboard Type: Executive Summary                                        │
╰─────────────────────────────────────────────────────────────────────────────╯"""

    def _get_organizational_data(self, sample_data: bool = False) -> Dict[str, Any]:
        """Get or generate organizational data for visualization"""
        if sample_data:
            # Use the data generator (follows Single Responsibility Principle)
            org_data = self.data_generator.generate_sample_data(self.profile_manager)
            return self._convert_to_dict(org_data)
        else:
            # Use the data generator for real data collection
            org_data = self.data_generator.collect_real_data(self.profile_manager)
            return self._convert_to_dict(org_data)

    def _convert_to_dict(self, org_data) -> Dict[str, Any]:
        """Convert OrganizationalData to dictionary format"""
        return {
            "impact_score": org_data.impact_score,
            "domains": org_data.domains,
            "trends": org_data.trends,
            "investments": org_data.investments,
            "sample_metrics": org_data.sample_metrics,
        }

    # NOTE: Sample data generation moved to SampleDataGenerator class (SRP)

    def _render_impact_score_section(self, org_data: Dict[str, Any]) -> str:
        """Render the impact score visualization"""
        impact_indicator = visualization_factory.create_impact_score(
            self.layout.impact_score_size
        )

        score = org_data["impact_score"]

        return impact_indicator.render_ascii(score, "Organizational Impact")

    def _render_domain_performance_section(self, org_data: Dict[str, Any]) -> str:
        """Render domain performance chart"""
        domain_chart = visualization_factory.create_domain_chart(
            self.layout.chart_width
        )

        return domain_chart.render_ascii(org_data["domains"])

    def _render_trend_analysis_section(self, org_data: Dict[str, Any]) -> str:
        """Render trend analysis with sparklines"""
        output = ["📈 Trend Analysis (8-week view)"]
        output.append("=" * 60)

        trend_sparkline = visualization_factory.create_trend_sparkline(
            self.layout.sparkline_width
        )

        for domain_name, trend_data in org_data["trends"].items():
            trend_line = trend_sparkline.render_ascii(
                trend_data, domain_name.replace("_", " ").title()
            )
            output.append(trend_line)

        return "\n".join(output)

    def _render_roi_section(self, org_data: Dict[str, Any]) -> str:
        """Render ROI visualization"""
        roi_viz = visualization_factory.create_roi_visualization()

        return roi_viz.render_ascii(org_data["investments"])

    def _render_executive_summary_section(self, org_data: Dict[str, Any]) -> str:
        """Render executive summary widget"""
        executive_widget = visualization_factory.create_executive_summary()

        # Prepare summary data
        domains = org_data["domains"]
        top_domain = max(
            domains,
            key=lambda d: (
                d["current"] / d["target"] if d["target"] > 0 else d["current"]
            ),
        )
        attention_domain = min(
            domains,
            key=lambda d: (
                d["current"] / d["target"] if d["target"] > 0 else d["current"]
            ),
        )

        summary_data = {
            "role": self.profile_manager.current_profile.role_title,
            "impact_score": org_data["impact_score"],
            "top_performing_domain": top_domain["name"],
            "needs_attention_domain": attention_domain["name"],
        }

        return executive_widget.render_ascii(summary_data)

    def customize_layout(self, **kwargs) -> None:
        """
        Customize dashboard layout
        Rachel approved: Flexible configuration while maintaining design consistency
        """
        for key, value in kwargs.items():
            if hasattr(self.layout, key):
                setattr(self.layout, key, value)

    def export_dashboard_data(self, format: str = "json") -> Dict[str, Any]:
        """
        Export dashboard data for web visualization
        Rachel approved: Consistent data structure for cross-platform rendering
        """
        org_data = self._get_organizational_data(sample_data=True)

        dashboard_export = {
            "profile": {
                "role": self.profile_manager.current_profile.role_title,
                "focus": self.profile_manager.current_profile.primary_focus,
                "strategic_priorities": self.profile_manager.current_profile.strategic_priorities,
            },
            "impact_score": {
                "value": org_data["impact_score"],
                "status": self.design_system.get_status_indicator(
                    org_data["impact_score"], 1.0
                ),
            },
            "domains": [
                {
                    **domain,
                    "status": self.design_system.get_status_indicator(
                        domain["current"], domain["target"]
                    ),
                }
                for domain in org_data["domains"]
            ],
            "trends": org_data["trends"],
            "investments": org_data["investments"],
            "layout": {
                "type": self.layout.layout_type,
                "components": {
                    "impact_score": True,
                    "domain_performance": True,
                    "trends": self.layout.show_trends,
                    "roi": self.layout.show_roi,
                    "executive_summary": self.layout.show_executive_summary,
                },
            },
            "design_system": {
                "colors": self.design_system.tokens.colors,
                "typography": self.design_system.tokens.typography,
                "spacing": self.design_system.tokens.spacing,
            },
        }

        return dashboard_export

    def get_quick_status(self) -> str:
        """
        Quick status view for daily use
        Rachel approved: Minimal, scannable, actionable
        """
        org_data = self._get_organizational_data(sample_data=True)
        score = org_data["impact_score"]
        status = self.design_system.get_status_indicator(score, 1.0)

        # Find top and bottom performing domains
        domains = org_data["domains"]
        top = max(domains, key=lambda d: d["current"])
        attention = min(domains, key=lambda d: d["current"])

        return f"""
🎯 Quick Status | {self.profile_manager.current_profile.role_title}
─────────────────────────────────────────────────────────────
📊 Impact Score: {score:.3f} {status['icon']} {status['label']}
✅ Top Performer: {top['name'].replace('_', ' ').title()} ({top['current']:.1%})
⚠️  Needs Focus: {attention['name'].replace('_', ' ').title()} ({attention['current']:.1%})
"""
