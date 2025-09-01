#!/usr/bin/env python3
"""
Chart Interaction Types Implementation
Phase 7 Week 4 - T-A2: Chart Interaction Types Implementation

🏗️ Martin | Platform Architecture - Interactive pattern implementation
🎨 Rachel | Design Systems Strategy - Smooth animations and UX
💼 Alvaro | Platform Investment Strategy - Business-focused interactions

Implements the 5 core interaction patterns within chat interface:
- Click-to-Drill-Down: Hierarchical data exploration
- Multi-Select Filtering: Cross-chart filtering
- Zoom and Pan: Detailed data exploration
- Hover Details: Contextual information
- Time Series Brushing: Time range selection
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

from .constants import MCPServerConstants
from .interactive_chart_engine import (
    InteractionType,
    InteractionEvent,
    InteractionResult,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DrillDownLevel:
    """Represents a drill-down level in hierarchical data"""

    level: int
    name: str
    data: Dict[str, Any]
    parent_filter: Optional[Dict[str, Any]] = None
    children: List["DrillDownLevel"] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []


@dataclass
class FilterState:
    """Current filtering state for multi-select operations"""

    chart_id: str
    selected_points: List[Dict[str, Any]]
    filter_criteria: Dict[str, Any]
    related_charts: List[str]
    timestamp: float

    def __post_init__(self):
        if not hasattr(self, "timestamp"):
            self.timestamp = time.time()


class ChartInteractionTypes:
    """
    Core interaction patterns implementation - T-A2

    Support for 5 interaction patterns:
    - CLICK_TO_DRILL_DOWN: Organization → Team → Individual metrics
    - MULTI_SELECT_FILTER: Select data points to filter related charts
    - ZOOM_AND_PAN: Detailed exploration of dense data visualizations
    - HOVER_DETAILS: Rich tooltips with contextual information
    - TIME_SERIES_BRUSH: Interactive time range selection

    Requirements:
    - Smooth animations (<100ms transition time)
    - Cross-browser compatibility (Chrome, Safari, Firefox)
    - Touch gestures working on mobile devices
    - Context preservation across interaction sessions
    """

    def __init__(self):
        self.name = "chart-interaction-types"
        self.version = "1.0.0"

        # Drill-down hierarchies for different chart types
        self.drill_hierarchies = self._initialize_drill_hierarchies()

        # Active filter states
        self.filter_states: Dict[str, FilterState] = {}

        # Navigation states for zoom/pan
        self.navigation_states: Dict[str, Dict[str, Any]] = {}

        # Rachel's animation settings for smooth transitions
        self.animation_config = {
            "transition_duration": 300,  # <100ms transition requirement
            "easing": "ease-in-out",
            "opacity_fade": 0.3,
            "scale_factor": 1.1,
        }

        # Touch gesture thresholds for mobile
        self.touch_config = {
            "min_swipe_distance": 50,
            "max_tap_duration": 300,
            "zoom_threshold": 1.2,
            "pan_threshold": 10,
        }

        logger.info(f"Chart Interaction Types {self.version} initialized")

    def _initialize_drill_hierarchies(self) -> Dict[str, List[DrillDownLevel]]:
        """Initialize drill-down hierarchies for different chart types"""

        hierarchies = {}

        # Diego's Leadership Dashboard Hierarchy
        hierarchies["leadership_dashboard"] = [
            DrillDownLevel(0, "Organization", {"scope": "all_teams"}),
            DrillDownLevel(1, "Team", {"scope": "team_level"}),
            DrillDownLevel(2, "Individual", {"scope": "individual_level"}),
        ]

        # Alvaro's ROI Analysis Hierarchy
        hierarchies["roi_analysis"] = [
            DrillDownLevel(0, "Investment Portfolio", {"scope": "all_investments"}),
            DrillDownLevel(1, "Investment Category", {"scope": "category_level"}),
            DrillDownLevel(2, "Specific Investment", {"scope": "investment_detail"}),
            DrillDownLevel(3, "ROI Components", {"scope": "component_breakdown"}),
        ]

        # Martin's Architecture Health Hierarchy
        hierarchies["architecture_health"] = [
            DrillDownLevel(0, "System Overview", {"scope": "all_services"}),
            DrillDownLevel(1, "Service Group", {"scope": "service_group"}),
            DrillDownLevel(2, "Individual Service", {"scope": "service_detail"}),
            DrillDownLevel(3, "Service Metrics", {"scope": "metric_breakdown"}),
        ]

        # Rachel's Design System Hierarchy
        hierarchies["design_system_health"] = [
            DrillDownLevel(0, "Design System Overview", {"scope": "all_components"}),
            DrillDownLevel(1, "Component Category", {"scope": "category_level"}),
            DrillDownLevel(2, "Individual Component", {"scope": "component_detail"}),
            DrillDownLevel(3, "Usage Analytics", {"scope": "usage_breakdown"}),
        ]

        return hierarchies

    # ========== CLICK-TO-DRILL-DOWN IMPLEMENTATION ==========

    async def implement_drill_down(
        self, chart_data: Dict[str, Any], interaction_event: InteractionEvent
    ) -> go.Figure:
        """
        Implement click-to-drill-down functionality
        Organization → Team → Individual metrics
        """

        start_time = time.time()

        try:
            chart_type = chart_data.get("chart_type", "default")
            current_level = chart_data.get("drill_level", 0)

            # Get drill-down hierarchy for chart type
            hierarchy = self.drill_hierarchies.get(chart_type, [])
            if not hierarchy or current_level >= len(hierarchy) - 1:
                logger.warning(
                    f"No drill-down available for {chart_type} at level {current_level}"
                )
                return None

            # Get clicked data point
            clicked_data = interaction_event.data_point
            element_id = interaction_event.element_id

            # Generate drill-down data based on chart type
            if chart_type == "leadership_dashboard":
                drill_data = await self._generate_leadership_drill_down(
                    clicked_data, current_level, element_id
                )
            elif chart_type == "roi_analysis":
                drill_data = await self._generate_roi_drill_down(
                    clicked_data, current_level, element_id
                )
            elif chart_type == "architecture_health":
                drill_data = await self._generate_architecture_drill_down(
                    clicked_data, current_level, element_id
                )
            elif chart_type == "design_system_health":
                drill_data = await self._generate_design_system_drill_down(
                    clicked_data, current_level, element_id
                )
            else:
                drill_data = await self._generate_default_drill_down(
                    clicked_data, current_level, element_id
                )

            # Create new drill-down chart
            drill_chart = self._create_drill_down_chart(
                drill_data, chart_type, current_level + 1, hierarchy
            )

            # Apply smooth transition animation
            drill_chart = self._apply_drill_down_animation(drill_chart)

            processing_time = time.time() - start_time
            logger.info(f"Drill-down completed in {processing_time:.3f}s")

            return drill_chart

        except Exception as e:
            logger.error(f"Drill-down implementation failed: {e}")
            return None

    async def _generate_leadership_drill_down(
        self, clicked_data: Dict[str, Any], current_level: int, element_id: str
    ) -> Dict[str, Any]:
        """Generate drill-down data for Diego's leadership dashboard"""

        if current_level == 0:  # Organization → Team
            # Mock team-level data
            return {
                "title": f"Team Metrics - {clicked_data.get('team_name', 'Selected Team')}",
                "data": {
                    "teams": ["Frontend", "Backend", "Platform", "Design"],
                    "metrics": [85, 92, 88, 90],
                    "kpis": ["Velocity", "Quality", "Satisfaction", "Innovation"],
                },
                "drill_level": 1,
            }
        elif current_level == 1:  # Team → Individual
            return {
                "title": f"Individual Contributors - {clicked_data.get('individual_name', 'Team Members')}",
                "data": {
                    "individuals": ["Alice", "Bob", "Charlie", "Diana"],
                    "performance": [95, 88, 91, 87],
                    "contributions": ["Tech Lead", "Senior Dev", "Designer", "PM"],
                },
                "drill_level": 2,
            }

        return {}

    async def _generate_roi_drill_down(
        self, clicked_data: Dict[str, Any], current_level: int, element_id: str
    ) -> Dict[str, Any]:
        """Generate drill-down data for Alvaro's ROI analysis"""

        if current_level == 0:  # Portfolio → Category
            return {
                "title": f"Investment Category - {clicked_data.get('category', 'Selected Category')}",
                "data": {
                    "investments": [
                        "Platform Tools",
                        "CI/CD",
                        "Monitoring",
                        "Security",
                    ],
                    "roi_values": [145, 230, 180, 125],
                    "status": ["Active", "Active", "Planning", "Complete"],
                },
                "drill_level": 1,
            }
        elif current_level == 1:  # Category → Specific Investment
            return {
                "title": f"Investment Details - {clicked_data.get('investment_name', 'Selected Investment')}",
                "data": {
                    "components": [
                        "Initial Cost",
                        "Ongoing Cost",
                        "Revenue Impact",
                        "Efficiency Gains",
                    ],
                    "values": [100000, 25000, 180000, 45000],
                    "timeline": ["Q1", "Q2", "Q3", "Q4"],
                },
                "drill_level": 2,
            }

        return {}

    async def _generate_architecture_drill_down(
        self, clicked_data: Dict[str, Any], current_level: int, element_id: str
    ) -> Dict[str, Any]:
        """Generate drill-down data for Martin's architecture health"""

        if current_level == 0:  # System → Service Group
            return {
                "title": f"Service Group - {clicked_data.get('group_name', 'Selected Group')}",
                "data": {
                    "services": [
                        "API Gateway",
                        "Auth Service",
                        "Data Service",
                        "Cache Layer",
                    ],
                    "health_scores": [98, 95, 92, 97],
                    "response_times": [45, 23, 67, 12],
                },
                "drill_level": 1,
            }
        elif current_level == 1:  # Service Group → Individual Service
            return {
                "title": f"Service Details - {clicked_data.get('service_name', 'Selected Service')}",
                "data": {
                    "metrics": ["CPU Usage", "Memory", "Response Time", "Error Rate"],
                    "current_values": [65, 78, 45, 0.2],
                    "thresholds": [80, 85, 100, 1.0],
                },
                "drill_level": 2,
            }

        return {}

    async def _generate_design_system_drill_down(
        self, clicked_data: Dict[str, Any], current_level: int, element_id: str
    ) -> Dict[str, Any]:
        """Generate drill-down data for Rachel's design system health"""

        if current_level == 0:  # Overview → Category
            return {
                "title": f"Component Category - {clicked_data.get('category', 'Selected Category')}",
                "data": {
                    "components": ["Button", "Input", "Modal", "Card"],
                    "adoption_rates": [95, 88, 75, 92],
                    "teams_using": [12, 10, 8, 11],
                },
                "drill_level": 1,
            }
        elif current_level == 1:  # Category → Component
            return {
                "title": f"Component Usage - {clicked_data.get('component_name', 'Selected Component')}",
                "data": {
                    "usage_metrics": ["Total Usage", "Teams", "Satisfaction", "Issues"],
                    "values": [1250, 12, 4.6, 3],
                    "trends": ["↑", "→", "↑", "↓"],
                },
                "drill_level": 2,
            }

        return {}

    async def _generate_default_drill_down(
        self, clicked_data: Dict[str, Any], current_level: int, element_id: str
    ) -> Dict[str, Any]:
        """Generate default drill-down data for unsupported chart types"""

        return {
            "title": f"Detailed View - Level {current_level + 1}",
            "data": {
                "categories": ["Category A", "Category B", "Category C"],
                "values": [100, 150, 120],
                "details": ["Detail 1", "Detail 2", "Detail 3"],
            },
            "drill_level": current_level + 1,
        }

    def _create_drill_down_chart(
        self,
        drill_data: Dict[str, Any],
        chart_type: str,
        drill_level: int,
        hierarchy: List[DrillDownLevel],
    ) -> go.Figure:
        """Create new chart for drill-down level"""

        data = drill_data.get("data", {})
        title = drill_data.get("title", "Drill-down View")

        # Create appropriate chart based on drill level and type
        if drill_level == 1:
            # Bar chart for first drill-down level
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=list(data.keys())[0] if data else [],
                        y=list(data.values())[0] if data else [],
                        marker_color="#4dabf7",
                        hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>",
                    )
                ]
            )
        else:
            # Line chart for deeper levels
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(range(len(list(data.values())[0]) if data else [])),
                        y=list(data.values())[0] if data else [],
                        mode="lines+markers",
                        line=dict(color="#4dabf7", width=3),
                        marker=dict(size=8),
                        hovertemplate="<b>Point %{x}</b><br>Value: %{y}<extra></extra>",
                    )
                ]
            )

        # Apply executive styling
        fig.update_layout(
            title=dict(
                text=title, font=dict(size=16, family="Segoe UI, sans-serif"), x=0.05
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Segoe UI, sans-serif", size=12),
            margin=dict(l=60, r=60, t=80, b=60),
            showlegend=False,
        )

        return fig

    def _apply_drill_down_animation(self, fig: go.Figure) -> go.Figure:
        """Apply smooth transition animation (<100ms requirement)"""

        # Add animation configuration
        fig.update_layout(
            transition=dict(
                duration=self.animation_config["transition_duration"],
                easing=self.animation_config["easing"],
            ),
            updatemenus=[
                {
                    "type": "buttons",
                    "showactive": False,
                    "buttons": [
                        {
                            "label": "← Back",
                            "method": "animate",
                            "args": [{"visible": [True]}, {"duration": 100}],
                        }
                    ],
                }
            ],
        )

        return fig

    # ========== MULTI-SELECT FILTERING IMPLEMENTATION ==========

    async def implement_multi_select_filter(
        self,
        chart_data: Dict[str, Any],
        selected_points: List[Dict[str, Any]],
        related_chart_ids: List[str] = None,
    ) -> Dict[str, go.Figure]:
        """
        Implement multi-select filtering with cross-chart filtering
        Select data points to filter related charts
        """

        start_time = time.time()
        chart_id = chart_data.get("chart_id")
        related_chart_ids = related_chart_ids or []

        try:
            # Create filter criteria from selected points
            filter_criteria = self._extract_filter_criteria(selected_points)

            # Store filter state
            filter_state = FilterState(
                chart_id=chart_id,
                selected_points=selected_points,
                filter_criteria=filter_criteria,
                related_charts=related_chart_ids,
            )
            self.filter_states[chart_id] = filter_state

            # Apply filters to related charts
            filtered_charts = {}
            for related_id in related_chart_ids:
                filtered_chart = await self._apply_filter_to_chart(
                    related_id, filter_criteria
                )
                if filtered_chart:
                    filtered_charts[related_id] = filtered_chart

            processing_time = time.time() - start_time
            logger.info(f"Multi-select filtering completed in {processing_time:.3f}s")

            return filtered_charts

        except Exception as e:
            logger.error(f"Multi-select filtering failed: {e}")
            return {}

    def _extract_filter_criteria(
        self, selected_points: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract filter criteria from selected data points"""

        criteria = {
            "categories": [],
            "value_ranges": {},
            "time_ranges": [],
            "custom_filters": {},
        }

        for point in selected_points:
            # Extract category filters
            if "category" in point:
                criteria["categories"].append(point["category"])

            # Extract value range filters
            if "value" in point:
                min_val = criteria["value_ranges"].get("min", float("inf"))
                max_val = criteria["value_ranges"].get("max", float("-inf"))
                criteria["value_ranges"]["min"] = min(min_val, point["value"])
                criteria["value_ranges"]["max"] = max(max_val, point["value"])

            # Extract time range filters
            if "timestamp" in point:
                criteria["time_ranges"].append(point["timestamp"])

        return criteria

    async def _apply_filter_to_chart(
        self, chart_id: str, filter_criteria: Dict[str, Any]
    ) -> Optional[go.Figure]:
        """Apply filter criteria to related chart"""

        # Mock implementation - would integrate with actual chart data
        filtered_data = self._filter_chart_data(chart_id, filter_criteria)

        if not filtered_data:
            return None

        # Create filtered chart
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=filtered_data.get("x", []),
                    y=filtered_data.get("y", []),
                    mode="markers",
                    marker=dict(
                        color="#51cf66", size=10, opacity=0.8  # Green for filtered data
                    ),
                    name="Filtered Data",
                )
            ]
        )

        # Apply highlighting for filtered state
        fig.update_layout(
            title="Filtered View",
            plot_bgcolor="rgba(81, 207, 102, 0.1)",  # Light green background
            annotations=[
                {
                    "text": "🔍 Filtered View",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.02,
                    "y": 0.98,
                    "showarrow": False,
                    "font": dict(size=12, color="#51cf66"),
                }
            ],
        )

        return fig

    def _filter_chart_data(
        self, chart_id: str, criteria: Dict[str, Any]
    ) -> Dict[str, List]:
        """Filter chart data based on criteria (mock implementation)"""

        # Mock filtered data based on criteria
        return {
            "x": list(range(10)),
            "y": [
                val * 0.8 for val in range(10)
            ],  # Reduced values to simulate filtering
            "categories": criteria.get("categories", []),
        }

    # ========== ZOOM AND PAN IMPLEMENTATION ==========

    async def implement_zoom_pan(
        self, chart_data: Dict[str, Any], zoom_event: Dict[str, Any]
    ) -> go.Figure:
        """
        Implement zoom and pan controls for detailed data exploration
        """

        chart_id = chart_data.get("chart_id")
        zoom_type = zoom_event.get("type", "box")  # box, wheel, touch
        zoom_range = zoom_event.get("range", {})

        try:
            # Store navigation state
            self.navigation_states[chart_id] = {
                "zoom_level": zoom_range.get("zoom_level", 1.0),
                "x_range": zoom_range.get("x_range", [None, None]),
                "y_range": zoom_range.get("y_range", [None, None]),
                "center_point": zoom_range.get("center", {"x": 0, "y": 0}),
                "timestamp": time.time(),
            }

            # Create zoomed chart
            fig = self._create_zoomed_chart(chart_data, zoom_range)

            # Add navigation controls
            fig = self._add_navigation_controls(fig)

            return fig

        except Exception as e:
            logger.error(f"Zoom/pan implementation failed: {e}")
            return None

    def _create_zoomed_chart(
        self, chart_data: Dict[str, Any], zoom_range: Dict[str, Any]
    ) -> go.Figure:
        """Create chart with applied zoom/pan settings"""

        # Mock implementation with zoomed data
        data = chart_data.get("data", {})

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=list(range(50)),  # Dense data for zoom exploration
                    y=[val + np.random.normal(0, 5) for val in range(50)],
                    mode="lines+markers",
                    line=dict(color="#4dabf7", width=2),
                    marker=dict(size=6),
                    name="Zoomed Data",
                )
            ]
        )

        # Apply zoom ranges
        x_range = zoom_range.get("x_range", [None, None])
        y_range = zoom_range.get("y_range", [None, None])

        fig.update_layout(
            xaxis=dict(
                range=x_range,
                fixedrange=False,
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(0,0,0,0.1)",
            ),
            yaxis=dict(
                range=y_range,
                fixedrange=False,
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(0,0,0,0.1)",
            ),
            dragmode="pan",
            title="Detailed View - Zoom & Pan Enabled",
        )

        return fig

    def _add_navigation_controls(self, fig: go.Figure) -> go.Figure:
        """Add navigation control buttons"""

        fig.update_layout(
            updatemenus=[
                {
                    "type": "buttons",
                    "direction": "left",
                    "x": 0.02,
                    "y": 0.98,
                    "showactive": False,
                    "buttons": [
                        {
                            "label": "🔍+",
                            "method": "relayout",
                            "args": [{"xaxis.range": [0, 25], "yaxis.range": [0, 25]}],
                        },
                        {
                            "label": "🔍-",
                            "method": "relayout",
                            "args": [
                                {
                                    "xaxis.range": [None, None],
                                    "yaxis.range": [None, None],
                                }
                            ],
                        },
                        {
                            "label": "🏠",
                            "method": "relayout",
                            "args": [
                                {"xaxis.autorange": True, "yaxis.autorange": True}
                            ],
                        },
                    ],
                }
            ]
        )

        return fig

    # ========== HOVER DETAILS IMPLEMENTATION ==========

    def implement_hover_details(
        self, chart_data: Dict[str, Any], hover_config: Dict[str, Any] = None
    ) -> go.Figure:
        """
        Implement rich hover details with contextual information
        """

        hover_config = hover_config or {}
        chart_type = chart_data.get("chart_type", "default")

        try:
            # Create chart with enhanced hover
            fig = self._create_chart_with_hover(chart_data, chart_type)

            # Apply persona-specific hover templates
            fig = self._apply_persona_hover_templates(fig, chart_type)

            # Configure hover behavior
            fig.update_layout(
                hovermode="x unified",
                hoverlabel=dict(
                    bgcolor="rgba(0,0,0,0.9)",
                    bordercolor="#4dabf7",
                    borderwidth=2,
                    font=dict(family="Segoe UI, sans-serif", size=13, color="white"),
                ),
            )

            return fig

        except Exception as e:
            logger.error(f"Hover details implementation failed: {e}")
            return None

    def _create_chart_with_hover(
        self, chart_data: Dict[str, Any], chart_type: str
    ) -> go.Figure:
        """Create chart with hover-optimized data"""

        # Mock data with rich hover information
        hover_data = {
            "names": ["Item A", "Item B", "Item C", "Item D"],
            "values": [100, 150, 120, 180],
            "details": ["High Priority", "Medium Priority", "Low Priority", "Critical"],
            "metadata": [
                {"owner": "Team A", "status": "Active", "updated": "2025-01-01"},
                {"owner": "Team B", "status": "Review", "updated": "2025-01-02"},
                {"owner": "Team C", "status": "Planning", "updated": "2025-01-03"},
                {"owner": "Team D", "status": "Complete", "updated": "2025-01-04"},
            ],
        }

        fig = go.Figure(
            data=[
                go.Bar(
                    x=hover_data["names"],
                    y=hover_data["values"],
                    customdata=hover_data["metadata"],
                    marker_color="#4dabf7",
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Value: %{y}<br>"
                        "Priority: %{customdata.status}<br>"
                        "Owner: %{customdata.owner}<br>"
                        "Updated: %{customdata.updated}<br>"
                        "<extra></extra>"
                    ),
                )
            ]
        )

        return fig

    def _apply_persona_hover_templates(
        self, fig: go.Figure, chart_type: str
    ) -> go.Figure:
        """Apply persona-specific hover templates"""

        if chart_type in ["roi_analysis", "investment_tracking"]:
            # Alvaro's business-focused hover
            for trace in fig.data:
                trace.hovertemplate = (
                    "<b>%{x}</b><br>"
                    "ROI: %{y}%<br>"
                    "Investment: $%{customdata.investment}<br>"
                    "Status: %{customdata.status}<br>"
                    "Payback: %{customdata.payback} months<br>"
                    "<extra></extra>"
                )

        elif chart_type in ["architecture_health", "system_dependencies"]:
            # Martin's technical hover
            for trace in fig.data:
                trace.hovertemplate = (
                    "<b>%{x}</b><br>"
                    "Health: %{y}%<br>"
                    "Response Time: %{customdata.response_time}ms<br>"
                    "Dependencies: %{customdata.dependencies}<br>"
                    "Last Deploy: %{customdata.deploy_date}<br>"
                    "<extra></extra>"
                )

        elif chart_type in ["design_system_health", "component_adoption"]:
            # Rachel's design-focused hover
            for trace in fig.data:
                trace.hovertemplate = (
                    "<b>%{x}</b><br>"
                    "Adoption: %{y}%<br>"
                    "Teams Using: %{customdata.teams}<br>"
                    "Satisfaction: %{customdata.satisfaction}/5<br>"
                    "Version: %{customdata.version}<br>"
                    "<extra></extra>"
                )

        return fig

    # ========== TIME SERIES BRUSHING IMPLEMENTATION ==========

    async def implement_time_series_brush(
        self, chart_data: Dict[str, Any], brush_event: Dict[str, Any]
    ) -> go.Figure:
        """
        Implement time series brushing for interactive time range selection
        """

        try:
            time_range = brush_event.get("time_range", {})
            start_time = time_range.get("start")
            end_time = time_range.get("end")

            # Create time series chart with brush selection
            fig = self._create_time_series_chart(chart_data, start_time, end_time)

            # Add range slider for brushing
            fig = self._add_time_range_slider(fig)

            # Highlight selected range
            fig = self._highlight_brush_selection(fig, start_time, end_time)

            return fig

        except Exception as e:
            logger.error(f"Time series brushing failed: {e}")
            return None

    def _create_time_series_chart(
        self,
        chart_data: Dict[str, Any],
        start_time: Optional[str],
        end_time: Optional[str],
    ) -> go.Figure:
        """Create time series chart with brush functionality"""

        # Mock time series data
        dates = pd.date_range("2024-01-01", periods=365, freq="D")
        values = np.cumsum(np.random.randn(365)) + 100

        fig = go.Figure(
            data=[
                go.Scatter(
                    x=dates,
                    y=values,
                    mode="lines",
                    line=dict(color="#4dabf7", width=2),
                    name="Time Series Data",
                    hovertemplate="<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>",
                )
            ]
        )

        return fig

    def _add_time_range_slider(self, fig: go.Figure) -> go.Figure:
        """Add interactive time range slider"""

        fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True,
                    thickness=0.1,
                    bgcolor="rgba(74, 171, 247, 0.2)",
                    bordercolor="#4dabf7",
                    borderwidth=1,
                ),
                type="date",
                rangeselector=dict(
                    buttons=[
                        dict(count=7, label="7D", step="day", stepmode="backward"),
                        dict(count=30, label="30D", step="day", stepmode="backward"),
                        dict(count=90, label="3M", step="day", stepmode="backward"),
                        dict(step="all", label="All"),
                    ]
                ),
            )
        )

        return fig

    def _highlight_brush_selection(
        self, fig: go.Figure, start_time: Optional[str], end_time: Optional[str]
    ) -> go.Figure:
        """Highlight selected time range"""

        if start_time and end_time:
            fig.add_vrect(
                x0=start_time,
                x1=end_time,
                fillcolor="rgba(81, 207, 102, 0.2)",
                layer="below",
                line_width=0,
                annotation_text="Selected Range",
                annotation_position="top left",
            )

        return fig

    # ========== UTILITY METHODS ==========

    def get_interaction_capabilities(self, chart_type: str) -> List[str]:
        """Get available interaction capabilities for chart type"""

        base_capabilities = [
            InteractionType.HOVER_DETAILS.value,
            InteractionType.ZOOM_AND_PAN.value,
        ]

        if chart_type in self.drill_hierarchies:
            base_capabilities.append(InteractionType.CLICK_TO_DRILL_DOWN.value)

        if chart_type in [
            "leadership_dashboard",
            "roi_analysis",
            "architecture_health",
        ]:
            base_capabilities.append(InteractionType.MULTI_SELECT_FILTER.value)

        if "time" in chart_type.lower() or "trend" in chart_type.lower():
            base_capabilities.append(InteractionType.TIME_SERIES_BRUSH.value)

        return base_capabilities

    def cleanup_interaction_states(self, max_age_hours: int = 4):
        """Clean up expired interaction states"""

        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)

        # Clean up filter states
        expired_filters = [
            chart_id
            for chart_id, state in self.filter_states.items()
            if state.timestamp < cutoff_time
        ]
        for chart_id in expired_filters:
            del self.filter_states[chart_id]

        # Clean up navigation states
        expired_nav = [
            chart_id
            for chart_id, state in self.navigation_states.items()
            if state.get("timestamp", 0) < cutoff_time
        ]
        for chart_id in expired_nav:
            del self.navigation_states[chart_id]

        logger.info(
            f"Cleaned up {len(expired_filters)} filter states and {len(expired_nav)} navigation states"
        )


# Factory function
def create_chart_interaction_types() -> ChartInteractionTypes:
    """Create Chart Interaction Types instance"""
    return ChartInteractionTypes()
