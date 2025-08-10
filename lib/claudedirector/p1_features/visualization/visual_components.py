#!/usr/bin/env python3
"""
Visual Components for P1.1 Dashboard
Rachel-approved visualization components following design system principles
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import math
from .design_system import design_system, ColorScale, ComponentSize


@dataclass
class VisualizationData:
    """Base data structure for all visualizations"""

    title: str
    value: float
    target: Optional[float] = None
    trend_data: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None


class ImpactScoreIndicator:
    """
    Circular progress indicator for organizational impact scores
    Rachel's design: Clear, accessible, executive-friendly
    """

    def __init__(self, size: ComponentSize = ComponentSize.LG):
        self.size = size
        self.design_system = design_system

    def render_ascii(self, score: float, title: str = "Impact Score") -> str:
        """
        ASCII representation for terminal display
        Rachel approved: Clear visual hierarchy and status indication
        """
        # Get status indicator
        status = self.design_system.get_status_indicator(score, 1.0)

        # Create circular progress visualization
        progress_chars = self._create_progress_circle(score)
        percentage = score * 100

        # Format with design system typography hierarchy
        return f"""
╭─────────────────────────╮
│ {title:^23} │
│                         │
│    {progress_chars[0]}   {progress_chars[1]}   {progress_chars[2]}     │
│  {progress_chars[7]}     {percentage:5.1f}%     {progress_chars[3]}   │
│    {progress_chars[6]}   {progress_chars[5]}   {progress_chars[4]}     │
│                         │
│ {status['icon']} {status['label']:^19} │
╰─────────────────────────╯"""

    def _create_progress_circle(self, score: float) -> List[str]:
        """Create 8-point circular progress indicator"""
        filled_segments = int(score * 8)
        segments = ["○"] * 8  # Empty circles

        # Fill segments based on score
        for i in range(filled_segments):
            segments[i] = "●"  # Filled circles

        return segments

    def get_svg_data(self, score: float, title: str = "Impact Score") -> Dict[str, Any]:
        """
        SVG data for web dashboard
        Rachel approved: Accessible, responsive, brand-consistent
        """
        status = self.design_system.get_status_indicator(score, 1.0)
        color = status["color"]

        return {
            "type": "circular_progress",
            "data": {
                "score": score,
                "percentage": score * 100,
                "title": title,
                "color": color,
                "status": status["status"],
                "label": status["label"],
            },
            "config": {
                "size": 120 if self.size == ComponentSize.LG else 80,
                "stroke_width": 8,
                "background_color": design_system.tokens.colors["neutral"]["100"],
                "text_color": design_system.tokens.colors["neutral"]["900"],
            },
        }


class DomainPerformanceChart:
    """
    Horizontal bar chart with target lines for domain performance
    Rachel's design: Clear comparison, accessible colors, executive insights
    """

    def __init__(self, width: int = 60):
        self.width = width
        self.design_system = design_system

    def render_ascii(self, domains: List[Dict[str, Any]]) -> str:
        """
        ASCII horizontal bar chart
        Rachel approved: Clear performance comparison at a glance
        """
        output = ["📊 Domain Performance Analysis"]
        output.append("=" * (self.width + 20))

        for domain in domains:
            name = domain["name"]
            current = domain["current"]
            target = domain.get("target", 1.0)
            weight = domain.get("weight", 0.0)

            # Get status and formatting
            status = self.design_system.get_status_indicator(current, target)

            # Create bar visualization
            bar = self._create_horizontal_bar(current, target)

            # Format domain line
            name_display = name.replace("_", " ").title()[:20]
            current_pct = current * 100
            target_pct = target * 100 if target > 0 else 0

            output.append(f"{name_display:<20} {status['icon']} {bar}")
            output.append(
                f"{'':20} Current: {current_pct:5.1f}% │ Target: {target_pct:5.1f}% │ Weight: {weight:.2f}"
            )
            output.append("")

        return "\n".join(output)

    def _create_horizontal_bar(self, current: float, target: float) -> str:
        """Create horizontal bar with target line"""
        bar_width = 30

        # Calculate filled portion
        if target > 0:
            fill_ratio = min(current / target, 1.0)
        else:
            fill_ratio = current

        filled_chars = int(fill_ratio * bar_width)

        # Create bar
        bar = "█" * filled_chars + "░" * (bar_width - filled_chars)

        # Add target line if different from 100%
        if target > 0 and target != 1.0:
            target_pos = min(int(1.0 * bar_width), bar_width - 1)
            bar = bar[:target_pos] + "│" + bar[target_pos + 1 :]

        return f"[{bar}] {current * 100:5.1f}%"

    def get_chart_data(self, domains: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Chart data for web dashboard
        Rachel approved: Accessible, responsive, clear hierarchy
        """
        chart_data = []

        for domain in domains:
            status = self.design_system.get_status_indicator(
                domain["current"], domain.get("target", 1.0)
            )

            chart_data.append(
                {
                    "name": domain["name"].replace("_", " ").title(),
                    "current": domain["current"],
                    "target": domain.get("target", 1.0),
                    "weight": domain.get("weight", 0.0),
                    "color": status["color"],
                    "status": status["status"],
                }
            )

        return {
            "type": "horizontal_bar",
            "data": chart_data,
            "config": {
                "width": 800,
                "height": len(domains) * 60 + 100,
                "margin": {"top": 20, "right": 40, "bottom": 40, "left": 200},
                "colors": self.design_system.get_color_palette(len(domains)),
            },
        }


class TrendSparkline:
    """
    Sparkline showing week-over-week progress trends
    Rachel's design: Minimal, informative, pattern recognition
    """

    def __init__(self, width: int = 20):
        self.width = width
        self.design_system = design_system

    def render_ascii(self, trend_data: List[float], title: str = "Trend") -> str:
        """
        ASCII sparkline visualization
        Rachel approved: Quick trend identification
        """
        if not trend_data or len(trend_data) < 2:
            return f"{title}: No trend data available"

        # Create sparkline
        sparkline = self._create_sparkline(trend_data)

        # Calculate trend direction
        trend_direction = self._calculate_trend_direction(trend_data)

        # Format output
        latest_value = trend_data[-1]
        change = (
            ((trend_data[-1] / trend_data[0]) - 1) * 100 if trend_data[0] != 0 else 0
        )

        return f"{title:<20} {sparkline} {latest_value:.3f} ({trend_direction['icon']}{change:+.1f}%)"

    def _create_sparkline(self, data: List[float]) -> str:
        """Create ASCII sparkline from data points"""
        if not data:
            return "─" * self.width

        # Normalize data to 0-7 range for unicode block characters
        min_val = min(data)
        max_val = max(data)

        if min_val == max_val:
            return "─" * min(len(data), self.width)

        # Map to block characters
        blocks = "▁▂▃▄▅▆▇█"
        sparkline = ""

        step = len(data) / self.width if len(data) > self.width else 1

        for i in range(min(self.width, len(data))):
            if step == 1:
                value = data[i]
            else:
                # Average values for compressed display
                start_idx = int(i * step)
                end_idx = min(int((i + 1) * step), len(data))
                value = sum(data[start_idx:end_idx]) / (end_idx - start_idx)

            # Normalize to 0-7 range
            normalized = (value - min_val) / (max_val - min_val)
            block_idx = min(int(normalized * 7), 7)
            sparkline += blocks[block_idx]

        return sparkline

    def _calculate_trend_direction(self, data: List[float]) -> Dict[str, str]:
        """Calculate overall trend direction"""
        if len(data) < 2:
            return {"icon": "─", "direction": "stable"}

        # Simple linear trend calculation
        start_avg = sum(data[: len(data) // 3]) / (len(data) // 3)
        end_avg = sum(data[-len(data) // 3 :]) / (len(data) // 3)

        if end_avg > start_avg * 1.05:
            return {"icon": "↗", "direction": "increasing"}
        elif end_avg < start_avg * 0.95:
            return {"icon": "↘", "direction": "decreasing"}
        else:
            return {"icon": "→", "direction": "stable"}


class ExecutiveSummaryWidget:
    """
    Executive summary widget with key insights
    Rachel's design: Scannable, action-oriented, business-focused
    """

    def __init__(self):
        self.design_system = design_system

    def render_ascii(self, summary_data: Dict[str, Any]) -> str:
        """
        Executive summary for terminal
        Rachel approved: Clear hierarchy, actionable insights
        """
        role = summary_data.get("role", "Director")
        impact_score = summary_data.get("impact_score", 0.0)
        top_domain = summary_data.get("top_performing_domain", "N/A")
        attention_domain = summary_data.get("needs_attention_domain", "N/A")

        status = self.design_system.get_status_indicator(impact_score, 1.0)

        output = f"""
╭─────────────────────────────────────────────────────────────╮
│                    EXECUTIVE SUMMARY                        │
│                                                             │
│ {role:<59} │
│                                                             │
│ 📊 Overall Impact Score: {impact_score:.3f} {status['icon']} {status['label']:<25} │
│                                                             │
│ 🎯 Top Performing Area:                                     │
│    ✅ {top_domain.replace('_', ' ').title():<51} │
│                                                             │
│ ⚠️  Needs Strategic Attention:                              │
│    🔍 {attention_domain.replace('_', ' ').title():<51} │
│                                                             │
│ 💡 Recommended Actions:                                     │
│    • Review underperforming domain targets                 │
│    • Leverage success patterns from top domain             │
│    • Schedule strategic review for attention areas         │
│                                                             │
╰─────────────────────────────────────────────────────────────╯"""

        return output


class ROIVisualization:
    """
    Investment ROI visualization
    Rachel's design: Financial clarity, investment insights
    """

    def render_ascii(self, investments: List[Dict[str, Any]]) -> str:
        """
        ROI visualization for terminal
        Rachel approved: Clear financial impact communication
        """
        output = ["💰 Investment ROI Analysis"]
        output.append("=" * 50)

        total_invested = sum(inv.get("invested", 0) for inv in investments)
        total_return = sum(inv.get("projected_return", 0) for inv in investments)
        overall_roi = (
            ((total_return - total_invested) / total_invested * 100)
            if total_invested > 0
            else 0
        )

        output.append(f"📊 Portfolio Overview:")
        output.append(f"   Total Invested: ${total_invested:,.0f}")
        output.append(f"   Projected Return: ${total_return:,.0f}")
        output.append(f"   Overall ROI: {overall_roi:+.1f}%")
        output.append("")

        for inv in investments:
            name = inv["name"].replace("_", " ").title()
            invested = inv.get("invested", 0)
            projected = inv.get("projected_return", 0)
            roi = ((projected - invested) / invested * 100) if invested > 0 else 0

            # ROI status indicator
            if roi > 20:
                status_icon = "🎉"
                status = "Excellent"
            elif roi > 10:
                status_icon = "✅"
                status = "Good"
            elif roi > 0:
                status_icon = "⚠️"
                status = "Moderate"
            else:
                status_icon = "🚨"
                status = "Poor"

            output.append(f"{status_icon} {name:<25}")
            output.append(
                f"   Invested: ${invested:>8,.0f} │ Return: ${projected:>8,.0f} │ ROI: {roi:+6.1f}% ({status})"
            )
            output.append("")

        return "\n".join(output)


# Component factory for easy instantiation
class VisualizationFactory:
    """
    Factory for creating Rachel-approved visualization components
    """

    @staticmethod
    def create_impact_score(
        size: ComponentSize = ComponentSize.LG,
    ) -> ImpactScoreIndicator:
        return ImpactScoreIndicator(size)

    @staticmethod
    def create_domain_chart(width: int = 60) -> DomainPerformanceChart:
        return DomainPerformanceChart(width)

    @staticmethod
    def create_trend_sparkline(width: int = 20) -> TrendSparkline:
        return TrendSparkline(width)

    @staticmethod
    def create_executive_summary() -> ExecutiveSummaryWidget:
        return ExecutiveSummaryWidget()

    @staticmethod
    def create_roi_visualization() -> ROIVisualization:
        return ROIVisualization()


# Export factory instance
visualization_factory = VisualizationFactory()
