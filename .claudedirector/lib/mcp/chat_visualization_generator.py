#!/usr/bin/env python3
"""
Chat Visualization Generator
Phase 3B.2.2: Consolidated chat chart generation for executive visualization server

🏗️ Martin | Platform Architecture - DRY principle for chat visualizations
🎨 Rachel | Design Systems Strategy - Consistent chat UX patterns
💼 Alvaro | Business Strategy - Streamlined chat visualization efficiency
🤖 Berny | AI/ML Engineering - Performance optimization through consolidation

Replaces 7 chat visualization methods with single consolidated generator.
NET REDUCTION TARGET: -150 lines from chat method consolidation.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Union


class ChatVisualizationGenerator:
    """
    Consolidated chat chart generator replacing 7 duplicate chat methods
    Implements DRY principle for chat visualization patterns
    """

    def __init__(self, color_palette: List[str], layout_template: Dict[str, Any]):
        """
        Initialize chat generator with styling configuration

        Args:
            color_palette: Executive color palette
            layout_template: Executive layout template
        """
        self.color_palette = color_palette
        self.layout_template = layout_template

        # Chat configuration constants
        self.CHAT_HEIGHT = 250
        self.MAX_CATEGORIES = 6  # Optimal for chat display

        # Chart type mappings (Phase 3B.2.2 - DRY consolidation)
        self.chart_generators = {
            "sprint_dashboard": self._generate_sprint_dashboard,
            "team_performance": self._generate_team_performance,
            "roi_dashboard": self._generate_roi_dashboard,
            "design_system": self._generate_design_system,
            "github_activity": self._generate_github_activity,
            "simple_metrics": self._generate_simple_metrics,
            "default": self._generate_default_bar_chart,
        }

    def create_chat_visualization(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """
        Unified chat visualization generator - replaces 7 duplicate chat methods

        Args:
            data: Chart data
            chart_type: Type of chart to create
            title: Chart title

        Returns:
            Plotly figure optimized for chat display
        """
        # Get appropriate generator function
        generator = self.chart_generators.get(
            chart_type, self.chart_generators["default"]
        )

        # Generate chart
        fig = generator(data, title)

        # Apply consistent chat styling
        self._apply_chat_styling(fig, title)

        return fig

    def _generate_sprint_dashboard(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Generate sprint dashboard for chat"""
        progress = data.get("progress", {})
        metrics = data.get("metrics", {})

        # Single row layout for chat compactness
        fig = make_subplots(
            rows=1,
            cols=3,
            subplot_titles=("Progress", "Velocity", "Completion"),
            specs=[[{"type": "pie"}, {"type": "bar"}, {"type": "indicator"}]],
        )

        # Progress pie chart
        fig.add_trace(
            go.Pie(
                labels=list(progress.keys()),
                values=list(progress.values()),
                marker_colors=self.color_palette[: len(progress)],
            ),
            row=1,
            col=1,
        )

        # Velocity bar chart
        velocity_data = metrics.get("velocity", {})
        fig.add_trace(
            go.Bar(
                x=list(velocity_data.keys()),
                y=list(velocity_data.values()),
                marker_color=self.color_palette[0],
            ),
            row=1,
            col=2,
        )

        # Completion indicator
        fig.add_trace(
            go.Indicator(
                mode="number+gauge",
                value=metrics.get("completion_rate", 0) * 100,
                number={"suffix": "%"},
                title={"text": "Completion"},
                gauge={"threshold": {"value": 80}},
            ),
            row=1,
            col=3,
        )

        return fig

    def _generate_team_performance(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Generate team performance chart for chat"""
        metrics = data.get("metrics", {})

        categories = ["Completion", "Quality", "Speed"]
        values = [
            metrics.get("story_completion_rate", 0) * 100,
            (1 - metrics.get("defect_rate", 0.03)) * 100,
            max(0, (10 - metrics.get("average_cycle_time", 5)) * 10),
        ]

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=categories,
                y=values,
                marker_color=self.color_palette[:3],
                text=[f"{v:.1f}%" for v in values],
                textposition="auto",
            )
        )

        fig.update_yaxis(title="Score %")
        return fig

    def _generate_roi_dashboard(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Generate ROI dashboard for chat"""
        investment = data.get("investment", {})
        returns = data.get("returns", {})
        roi_metrics = data.get("roi_metrics", {})

        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=("Investment vs Returns", "ROI"),
            specs=[[{"type": "bar"}, {"type": "indicator"}]],
        )

        # Investment vs Returns
        fig.add_trace(
            go.Bar(
                x=["Investment", "Returns"],
                y=[investment.get("total_cost", 0), sum(returns.values())],
                marker_color=[self.color_palette[2], self.color_palette[0]],
            ),
            row=1,
            col=1,
        )

        # ROI Indicator
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=roi_metrics.get("roi_percentage", 0),
                number={"suffix": "x"},
                title={"text": "ROI Multiple"},
                delta={"reference": 1.0},
            ),
            row=1,
            col=2,
        )

        return fig

    def _generate_design_system(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Generate design system chart for chat"""
        adoption = data.get("adoption", {})
        usage = data.get("usage", {})

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=["Components", "Teams", "Implementations"],
                y=[
                    adoption.get("adoption_rate", 0) * 100,
                    (usage.get("active_teams", 0) / usage.get("total_teams", 1)) * 100,
                    min(100, usage.get("implementations", 0) / 2),  # Scale for display
                ],
                marker_color=self.color_palette[:3],
            )
        )

        fig.update_yaxis(title="Adoption %")
        return fig

    def _generate_github_activity(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Generate GitHub activity chart for chat"""
        activity = data.get("activity", {})

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=["Commits", "PRs", "Issues Closed"],
                y=[
                    activity.get("commits", 0),
                    activity.get("pull_requests", 0),
                    activity.get("issues_closed", 0),
                ],
                marker_color=self.color_palette[:3],
            )
        )

        fig.update_yaxis(title="Count")
        return fig

    def _generate_simple_metrics(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Generate simple metrics chart for chat"""
        # Extract numeric values
        metrics = {}
        for key, value in data.items():
            if isinstance(value, (int, float)):
                metrics[key] = value
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, (int, float)):
                        metrics[f"{key}_{subkey}"] = subvalue

        if metrics:
            # Limit categories for chat display
            items = list(metrics.items())[: self.MAX_CATEGORIES]
            categories, values = zip(*items) if items else ([], [])

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=list(categories),
                    y=list(values),
                    marker_color=self.color_palette[: len(categories)],
                )
            )
        else:
            fig = self._generate_default_bar_chart({}, title)

        return fig

    def _generate_default_bar_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Generate default bar chart for unknown types"""
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for visualization",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font_size=14,
        )
        return fig

    def _apply_chat_styling(self, fig: go.Figure, title: str) -> None:
        """Apply consistent chat-optimized styling"""
        fig.update_layout(
            title=title,
            height=self.CHAT_HEIGHT,
            showlegend=False,  # Save space in chat
            margin={"l": 40, "r": 40, "t": 50, "b": 40},  # Compact margins
            **self.layout_template,
        )
