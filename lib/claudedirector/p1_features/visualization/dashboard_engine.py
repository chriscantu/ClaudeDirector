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


class DashboardEngine:
    """
    Main dashboard engine coordinating all visual components
    Rachel's design: Consistent, accessible, executive-focused
    """

    def __init__(self, config_path: Optional[str] = None):
        self.profile_manager = DirectorProfileManager(
            config_path or "config/p1_organizational_intelligence.yaml"
        )
        self.design_system = design_system
        self.layout = DashboardLayout()

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
            return self._generate_sample_data()
        else:
            return self._collect_real_data()

    def _generate_sample_data(self) -> Dict[str, Any]:
        """
        Generate realistic sample data for demonstration
        Rachel approved: Realistic scenarios for accurate visualization testing
        """
        profile = self.profile_manager.current_profile

        # Sample current metrics
        sample_metrics = {
            "component_usage_consistency": 0.78,
            "design_debt_reduction": 0.12,
            "cross_team_design_velocity": 0.22,
            "adoption_rate_percentage": 0.75,
            "developer_satisfaction_score": 4.3,
            "time_to_onboard_new_teams": 2.8,
            "api_response_times": 180,
            "service_dependency_health": 0.95,
        }

        # Calculate impact score
        impact_score = self.profile_manager.calculate_organizational_impact_score(
            sample_metrics
        )

        # Domain performance data
        domain_data = []
        for domain_name, metrics in profile.enabled_domains.items():
            if metrics:
                weight = metrics[0].weight
                target = metrics[0].target_value if metrics[0].target_value > 0 else 0.8

                # Simulate current performance
                if "design" in domain_name:
                    current = 0.78
                elif "platform" in domain_name:
                    current = 0.75
                elif "api" in domain_name:
                    current = 0.85
                else:
                    current = 0.70

                domain_data.append(
                    {
                        "name": domain_name,
                        "current": current,
                        "target": target,
                        "weight": weight,
                    }
                )

        # Trend data (last 8 weeks)
        trend_data = {
            "design_system_leverage": [0.65, 0.68, 0.71, 0.73, 0.75, 0.77, 0.78, 0.78],
            "platform_adoption": [0.68, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.75],
            "api_service_efficiency": [0.80, 0.82, 0.83, 0.84, 0.85, 0.85, 0.85, 0.85],
        }

        # Investment ROI data
        investment_data = []
        for name, investment in profile.investment_categories.items():
            roi_multiplier = {
                "design_system_enhancement": 1.25,
                "platform_infrastructure": 1.18,
                "developer_experience": 1.30,
                "cross_team_tooling": 1.15,
            }.get(name, 1.20)

            invested = 50000 * investment.priority_weight
            projected_return = invested * roi_multiplier

            investment_data.append(
                {
                    "name": name,
                    "invested": invested,
                    "projected_return": projected_return,
                    "measurement_period": investment.measurement_period_months,
                }
            )

        return {
            "impact_score": max(impact_score, 0.65),  # Ensure realistic demo score
            "domains": domain_data,
            "trends": trend_data,
            "investments": investment_data,
            "sample_metrics": sample_metrics,
        }

    def _collect_real_data(self) -> Dict[str, Any]:
        """Collect real organizational data (placeholder for future integration)"""
        # For now, return sample data
        # In production, this would integrate with actual data sources
        return self._generate_sample_data()

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
                "status": design_system.get_status_indicator(
                    org_data["impact_score"], 1.0
                ),
            },
            "domains": [
                {
                    **domain,
                    "status": design_system.get_status_indicator(
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
                "colors": design_system.tokens.colors,
                "typography": design_system.tokens.typography,
                "spacing": design_system.tokens.spacing,
            },
        }

        return dashboard_export

    def get_quick_status(self) -> str:
        """
        Quick status view for daily use
        Rachel approved: Minimal, scannable, actionable
        """
        org_data = self._generate_sample_data()
        score = org_data["impact_score"]
        status = design_system.get_status_indicator(score, 1.0)

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
