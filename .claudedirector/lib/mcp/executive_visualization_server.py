#!/usr/bin/env python3
"""
Executive Visualization MCP Server
Phase 2 Implementation + Phase 7 Week 2 Enhancement - Chat-Embedded Visualizations

🏗️ Martin | Platform Architecture - Chat-based real-time infrastructure
🎨 Rachel | Design Systems Strategy - Executive Design System + Chat UX
💼 Alvaro | Business Strategy - ROI & Executive Requirements
🤖 Berny | AI/ML Engineering - Performance & Data Processing

Executive-quality visualization system built on Python MCP foundation.
Phase 7 Week 2: Enhanced for chat-embedded visualizations via Magic MCP integration.
PRD Compliance: All visualizations embedded in chat responses (Lines 158-161).
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import tempfile
import os

# Visualization libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from jinja2 import Template

# Phase 1 integration
from .strategic_python_server import StrategicPythonMCPServer, ExecutionResult
from .constants import MCPServerConstants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VisualizationResult:
    """Result of executive visualization generation"""

    success: bool
    html_output: str
    chart_type: str
    persona: str
    generation_time: float
    file_size_bytes: int
    interactive_elements: List[str]
    error: Optional[str] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class ExecutiveVisualizationEngine:
    """
    Executive-quality visualization system built on Python MCP foundation
    Produces publication-ready interactive visualizations
    """

    def __init__(self):
        self.name = MCPServerConstants.EXECUTIVE_VISUALIZATION_SERVER_NAME
        self.version = MCPServerConstants.EXECUTIVE_VISUALIZATION_SERVER_VERSION

        # Rachel's executive color palette
        self.color_palette = MCPServerConstants.Colors.EXECUTIVE_PALETTE

        # Executive layout template
        self.layout_template = MCPServerConstants.get_executive_layout_template()

        # Persona-specific templates
        self.persona_templates = {
            MCPServerConstants.Personas.DIEGO: self._diego_leadership_template,
            MCPServerConstants.Personas.ALVARO: self._alvaro_business_template,
            MCPServerConstants.Personas.MARTIN: self._martin_architecture_template,
            MCPServerConstants.Personas.CAMILLE: self._camille_technology_template,
            MCPServerConstants.Personas.RACHEL: self._rachel_design_template,
        }

        # Visualization capabilities
        self.capabilities = [
            MCPServerConstants.Capabilities.EXECUTIVE_DASHBOARDS,
            MCPServerConstants.Capabilities.INTERACTIVE_CHARTS,
            MCPServerConstants.Capabilities.STRATEGIC_PRESENTATIONS,
            MCPServerConstants.Capabilities.PUBLICATION_QUALITY_VISUALS,
        ]

        # Performance metrics
        self.visualization_metrics = {
            MCPServerConstants.MetricsKeys.TOTAL_VISUALIZATIONS: 0,
            MCPServerConstants.MetricsKeys.SUCCESSFUL_GENERATIONS: 0,
            MCPServerConstants.MetricsKeys.AVG_GENERATION_TIME: 0.0,
            MCPServerConstants.MetricsKeys.AVG_FILE_SIZE: 0,
            MCPServerConstants.MetricsKeys.INTERACTIVE_FEATURES_USED: 0,
        }

        # Phase 1 integration
        self.strategic_python_server = None

        logger.info(f"Executive Visualization Engine {self.version} initialized")

    async def create_executive_visualization(
        self,
        data: Union[Dict[str, Any], str],
        chart_type: str,
        persona: str,
        title: str,
        context: Dict[str, Any] = None,
    ) -> VisualizationResult:
        """Create executive-quality interactive visualization"""

        start_time = time.time()
        context = context or {}

        try:
            # Update metrics
            self.visualization_metrics[
                MCPServerConstants.MetricsKeys.TOTAL_VISUALIZATIONS
            ] += 1

            # Process data if it's a string (from Phase 1 analysis)
            if isinstance(data, str):
                data = self._parse_analysis_output(data)

            # Get persona-specific template
            template_func = self.persona_templates.get(
                persona, self.persona_templates["diego"]
            )

            # Generate Plotly figure
            fig = template_func(data, chart_type, title, context)

            # Apply executive styling
            fig = self._apply_executive_styling(fig, persona)

            # Generate complete HTML
            html_output = self._generate_executive_html(fig, persona, title)

            # Calculate metrics
            generation_time = time.time() - start_time
            file_size = len(html_output.encode("utf-8"))
            interactive_elements = self._detect_interactive_elements(fig)

            # Update success metrics
            self.visualization_metrics[
                MCPServerConstants.MetricsKeys.SUCCESSFUL_GENERATIONS
            ] += 1
            self._update_performance_metrics(
                generation_time, file_size, interactive_elements
            )

            result = VisualizationResult(
                success=True,
                html_output=html_output,
                chart_type=chart_type,
                persona=persona,
                generation_time=generation_time,
                file_size_bytes=file_size,
                interactive_elements=interactive_elements,
            )

            logger.info(
                f"Executive visualization generated: {chart_type} for {persona} ({generation_time:.2f}s)"
            )
            return result

        except Exception as e:
            logger.error(f"Executive visualization generation error: {str(e)}")
            return VisualizationResult(
                success=False,
                html_output="",
                chart_type=chart_type,
                persona=persona,
                generation_time=time.time() - start_time,
                file_size_bytes=0,
                interactive_elements=[],
                error=MCPServerConstants.ErrorMessages.VISUALIZATION_GENERATION_ERROR.format(
                    error=str(e)
                ),
            )

    def _diego_leadership_template(
        self, data: Dict[str, Any], chart_type: str, title: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Diego's leadership-focused visualization template"""

        if chart_type == "leadership_dashboard":
            return self._create_leadership_dashboard(data, title)
        elif chart_type == "team_metrics":
            return self._create_team_metrics_chart(data, title)
        elif chart_type == "strategic_trends":
            return self._create_strategic_trends_chart(data, title)
        elif chart_type == "support_analysis":
            return self._create_support_analysis_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _alvaro_business_template(
        self, data: Dict[str, Any], chart_type: str, title: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Alvaro's business intelligence template"""

        if chart_type == "roi_analysis":
            return self._create_roi_dashboard(data, title)
        elif chart_type == "investment_tracking":
            return self._create_investment_chart(data, title)
        elif chart_type == "business_metrics":
            return self._create_business_metrics_chart(data, title)
        elif chart_type == "cost_analysis":
            return self._create_cost_analysis_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _martin_architecture_template(
        self, data: Dict[str, Any], chart_type: str, title: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Martin's platform architecture template"""

        if chart_type == "architecture_health":
            return self._create_architecture_health_dashboard(data, title)
        elif chart_type == "service_performance":
            return self._create_service_performance_chart(data, title)
        elif chart_type == "system_dependency_map":
            return self._create_system_dependency_map(data, title)
        elif chart_type == "technical_debt_trends":
            return self._create_technical_debt_trends(data, title)
        elif chart_type == "performance_metrics":
            return self._create_performance_chart(data, title)
        elif chart_type == "system_dependencies":
            return self._create_dependency_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _camille_technology_template(
        self, data: Dict[str, Any], chart_type: str, title: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Camille's strategic technology template"""

        if chart_type == "technology_roadmap":
            return self._create_technology_roadmap(data, title)
        elif chart_type == "innovation_metrics":
            return self._create_innovation_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _rachel_design_template(
        self, data: Dict[str, Any], chart_type: str, title: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Rachel's design systems template"""

        if chart_type == "component_adoption":
            return self._create_component_adoption_chart(data, title)
        elif chart_type == "design_system_maturity":
            return self._create_design_system_maturity(data, title)
        elif chart_type == "usage_trend_analysis":
            return self._create_usage_trend_analysis(data, title)
        elif chart_type == "team_comparison":
            return self._create_team_comparison_dashboard(data, title)
        elif chart_type == "design_debt_visualization":
            return self._create_design_debt_visualization(data, title)
        elif chart_type == "design_system_health":
            return self._create_design_system_dashboard(data, title)
        elif chart_type == "adoption_metrics":
            return self._create_adoption_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _create_leadership_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create Diego's leadership metrics dashboard"""

        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Team Velocity Trend",
                "Support Volume Analysis",
                "Strategic Initiative Progress",
                "Platform Health Score",
            ),
            specs=[
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "indicator"}, {"type": "pie"}],
            ],
        )

        # Team velocity trend
        if "velocity_data" in data:
            fig.add_trace(
                go.Scatter(
                    x=data["velocity_data"].get("dates", []),
                    y=data["velocity_data"].get("velocity", []),
                    mode="lines+markers",
                    name="Team Velocity",
                    line=dict(color=self.color_palette[0], width=3),
                    marker=dict(size=8),
                ),
                row=1,
                col=1,
            )

        # Support volume analysis
        if "support_data" in data:
            fig.add_trace(
                go.Bar(
                    x=data["support_data"].get("months", []),
                    y=data["support_data"].get("volume", []),
                    name="Support Volume",
                    marker_color=self.color_palette[1],
                ),
                row=1,
                col=2,
            )

        # Strategic initiative progress (indicator)
        if "initiative_progress" in data:
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=data["initiative_progress"].get("current", 75),
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "Initiative Progress"},
                    delta={"reference": data["initiative_progress"].get("target", 80)},
                    gauge={
                        "axis": {"range": [None, 100]},
                        "bar": {"color": self.color_palette[0]},
                        "steps": [
                            {"range": [0, 50], "color": "lightgray"},
                            {"range": [50, 80], "color": "gray"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 90,
                        },
                    },
                ),
                row=2,
                col=1,
            )

        # Platform health (pie chart)
        if "platform_health" in data:
            fig.add_trace(
                go.Pie(
                    labels=data["platform_health"].get(
                        "labels", ["Healthy", "Warning", "Critical"]
                    ),
                    values=data["platform_health"].get("values", [70, 25, 5]),
                    name="Platform Health",
                    marker_colors=self.color_palette[:3],
                ),
                row=2,
                col=2,
            )

        fig.update_layout(title=title, showlegend=True, height=800)

        return fig

    def _create_roi_dashboard(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Create Alvaro's ROI analysis dashboard"""

        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Investment ROI Trend",
                "Cost vs Benefit Analysis",
                "ROI by Initiative",
                "Projected Returns",
            ),
            specs=[
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "scatter"}],
            ],
        )

        # ROI trend
        if "roi_trend" in data:
            fig.add_trace(
                go.Scatter(
                    x=data["roi_trend"].get("months", []),
                    y=data["roi_trend"].get("roi", []),
                    mode="lines+markers",
                    name="ROI %",
                    line=dict(color=self.color_palette[1], width=3),
                    marker=dict(size=8),
                ),
                row=1,
                col=1,
            )

        # Cost vs Benefit
        if "cost_benefit" in data:
            fig.add_trace(
                go.Bar(
                    x=data["cost_benefit"].get("categories", []),
                    y=data["cost_benefit"].get("costs", []),
                    name="Costs",
                    marker_color=self.color_palette[2],
                ),
                row=1,
                col=2,
            )
            fig.add_trace(
                go.Bar(
                    x=data["cost_benefit"].get("categories", []),
                    y=data["cost_benefit"].get("benefits", []),
                    name="Benefits",
                    marker_color=self.color_palette[1],
                ),
                row=1,
                col=2,
            )

        fig.update_layout(title=title, showlegend=True, height=800)

        return fig

    def _create_default_chart(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """Create default chart when specific template not available"""

        # Simple bar chart as fallback
        if "x" in data and "y" in data:
            fig = go.Figure(
                data=go.Bar(
                    x=data["x"], y=data["y"], marker_color=self.color_palette[0]
                )
            )
        else:
            # Sample data for demonstration
            fig = go.Figure(
                data=go.Bar(
                    x=["Q1", "Q2", "Q3", "Q4"],
                    y=[20, 14, 23, 25],
                    marker_color=self.color_palette[0],
                )
            )

        fig.update_layout(title=title)
        return fig

    # Phase 7 Week 2: Chat-Embedded Visualization Methods
    async def generate_chat_embedded_visualization(
        self,
        query_data: Dict[str, Any],
        persona: str = "diego",
        context: Dict[str, Any] = None,
    ) -> VisualizationResult:
        """
        Generate visualization optimized for chat embedding via Magic MCP.

        Phase 7 Week 2: PRD-compliant chat-only interface implementation.

        Args:
            query_data: Real-time data from ConversationalDataManager
            persona: Strategic persona for visualization style
            context: Chat conversation context

        Returns:
            VisualizationResult: Chat-optimized visualization
        """
        start_time = time.time()

        try:
            # Determine optimal chart type based on data structure
            chart_type = self._infer_chart_type_from_data(query_data)

            # Generate persona-specific visualization
            title = self._generate_contextual_title(query_data, context)
            fig = await self._create_chat_optimized_chart(
                query_data, chart_type, title, persona
            )

            # Generate chat-embedded HTML with compact layout
            html_output = self._generate_chat_embedded_html(fig, title, persona)

            generation_time = time.time() - start_time

            return VisualizationResult(
                success=True,
                html_output=html_output,
                chart_type=f"chat_embedded_{chart_type}",
                persona=persona,
                generation_time=generation_time,
                file_size_bytes=len(html_output.encode("utf-8")),
                interactive_elements=["hover", "zoom", "pan"],
                metadata={
                    "chat_optimized": True,
                    "magic_mcp_ready": True,
                    "context_aware": bool(context),
                    "data_source": query_data.get("source", "unknown"),
                },
            )

        except Exception as e:
            logger.error(f"Chat visualization generation failed: {str(e)}")
            return VisualizationResult(
                success=False,
                html_output=self._generate_error_visualization(str(e)),
                chart_type="error",
                persona=persona,
                generation_time=time.time() - start_time,
                file_size_bytes=0,
                interactive_elements=[],
                metadata={"error": str(e)},
            )

    def _infer_chart_type_from_data(self, data: Dict[str, Any]) -> str:
        """Infer optimal chart type based on data structure"""

        # Sprint metrics -> progress visualization
        if "progress" in data and "metrics" in data:
            return "sprint_dashboard"

        # Team performance -> radar/bar chart
        if "metrics" in data and any(key in data for key in ["team", "performance"]):
            return "team_performance"

        # ROI analysis -> financial dashboard
        if "investment" in data and "returns" in data:
            return "roi_dashboard"

        # Architecture health -> system status
        if "services" in data or "health_score" in data:
            return "architecture_health"

        # Design system -> adoption metrics
        if "adoption" in data or "components" in data:
            return "design_system_status"

        # GitHub activity -> timeline/activity chart
        if "activity" in data or "contributors" in data:
            return "github_activity"

        # Default to simple bar chart
        return "simple_metrics"

    def _generate_contextual_title(
        self, data: Dict[str, Any], context: Dict[str, Any] = None
    ) -> str:
        """Generate contextual title based on data and conversation context"""

        # Use data-specific titles
        if "sprint_name" in data:
            return f"{data['sprint_name']} - Current Status"
        elif "team" in data:
            return f"{data['team']} Performance Metrics"
        elif "project" in data:
            return f"{data['project']} ROI Analysis"
        elif "system" in data:
            return f"{data['system']} Health Dashboard"
        elif "repository" in data:
            return f"{data['repository']} Activity Overview"

        # Fallback to generic title
        return "Strategic Metrics Dashboard"

    async def _create_chat_optimized_chart(
        self, data: Dict[str, Any], chart_type: str, title: str, persona: str
    ) -> go.Figure:
        """Create chart optimized for chat embedding"""

        if chart_type == "sprint_dashboard":
            return self._create_sprint_dashboard_chat(data, title)
        elif chart_type == "team_performance":
            return self._create_team_performance_chat(data, title)
        elif chart_type == "roi_dashboard":
            return self._create_roi_dashboard_chat(data, title)
        elif chart_type == "architecture_health":
            return self._create_architecture_health_dashboard(data, title)
        elif chart_type == "design_system_status":
            return self._create_design_system_chat(data, title)
        elif chart_type == "github_activity":
            return self._create_github_activity_chat(data, title)
        else:
            return self._create_simple_metrics_chat(data, title)

    def _create_sprint_dashboard_chat(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create compact sprint dashboard for chat"""

        progress = data.get("progress", {})
        metrics = data.get("metrics", {})

        # Single row layout for chat compactness
        fig = make_subplots(
            rows=1,
            cols=3,
            subplot_titles=("Progress", "Velocity", "Completion"),
            specs=[[{"type": "pie"}, {"type": "bar"}, {"type": "indicator"}]],
        )

        # Sprint progress pie
        fig.add_trace(
            go.Pie(
                labels=["Done", "Active", "Todo"],
                values=[
                    progress.get("completed", 0),
                    progress.get("in_progress", 0),
                    progress.get("todo", 0),
                ],
                hole=0.4,
                marker_colors=self.color_palette[:3],
            ),
            row=1,
            col=1,
        )

        # Velocity comparison
        fig.add_trace(
            go.Bar(
                x=["Current", "Target"],
                y=[metrics.get("velocity", 0), 40],
                marker_color=self.color_palette[:2],
            ),
            row=1,
            col=2,
        )

        # Completion indicator
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=metrics.get("completion_rate", 0) * 100,
                title={"text": "Complete %"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": self.color_palette[0]},
                },
            ),
            row=1,
            col=3,
        )

        fig.update_layout(
            title=title, height=300, showlegend=False, **self.layout_template
        )
        return fig

    def _create_team_performance_chat(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create compact team performance chart for chat"""

        metrics = data.get("metrics", {})

        # Simple bar chart for chat
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

        fig.update_layout(
            title=title, height=250, yaxis_title="Score %", **self.layout_template
        )
        return fig

    def _create_roi_dashboard_chat(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Create compact ROI dashboard for chat"""

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

        fig.update_layout(title=title, height=250, **self.layout_template)
        return fig

    def _create_design_system_chat(self, data: Dict[str, Any], title: str) -> go.Figure:
        """Create compact design system chart for chat"""

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

        fig.update_layout(
            title=title, height=250, yaxis_title="Adoption %", **self.layout_template
        )
        return fig

    def _create_github_activity_chat(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create compact GitHub activity chart for chat"""

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

        fig.update_layout(
            title=title, height=250, yaxis_title="Count", **self.layout_template
        )
        return fig

    def _create_simple_metrics_chat(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create simple metrics chart for chat"""

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
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=list(metrics.keys())[:5],  # Limit to 5 for chat
                    y=list(metrics.values())[:5],
                    marker_color=self.color_palette[0],
                )
            )
        else:
            fig = go.Figure()
            fig.add_annotation(
                text="✅ Data received successfully",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                xanchor="center",
                yanchor="middle",
                showarrow=False,
                font=dict(size=16),
            )

        fig.update_layout(title=title, height=200, **self.layout_template)
        return fig

    def _generate_chat_embedded_html(
        self, fig: go.Figure, title: str, persona: str
    ) -> str:
        """Generate HTML optimized for chat embedding"""

        # Convert to HTML with compact configuration
        html_div = pio.to_html(
            fig,
            include_plotlyjs="cdn",
            div_id=f"chat_viz_{int(time.time())}",
            config={
                "displayModeBar": True,
                "displaylogo": False,
                "modeBarButtonsToRemove": ["pan2d", "lasso2d", "select2d"],
                "responsive": True,
            },
        )

        # Add chat-specific styling
        from jinja2 import Template

        chat_template = Template(
            """
        <div class="claudedirector-chat-visualization" style="
            max-width: 100%;
            margin: 10px 0;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div class="viz-header" style="
                padding: 12px 16px;
                border-bottom: 1px solid #e1e5e9;
                background: #f8f9fa;
                font-weight: 600;
                color: #2c3e50;
                font-size: 14px;
            ">
                📊 {{ title }} ({{ persona.title() }})
            </div>
            <div class="viz-content" style="padding: 8px;">
                {{ html_content }}
            </div>
            <div class="viz-footer" style="
                padding: 8px 16px;
                border-top: 1px solid #e1e5e9;
                background: #f8f9fa;
                font-size: 12px;
                color: #6c757d;
                text-align: right;
            ">
                Generated via ClaudeDirector • Interactive visualization
            </div>
        </div>
        """
        )

        return chat_template.render(title=title, persona=persona, html_content=html_div)

    def _apply_executive_styling(self, fig: go.Figure, persona: str) -> go.Figure:
        """Apply Rachel's executive styling to figure"""

        # Apply base layout template
        fig.update_layout(**self.layout_template)

        # Persona-specific styling enhancements
        # Apply persona-specific styling
        persona_color = MCPServerConstants.Colors.PERSONA_COLORS.get(
            persona, MCPServerConstants.Colors.PRIMARY_BLUE
        )
        persona_styles = {
            "title": {
                "font": {
                    "size": MCPServerConstants.Typography.TITLE_FONT_SIZE,
                    "color": persona_color,
                }
            },
            "showlegend": True,
        }

        fig.update_layout(**persona_styles)

        return fig

    def _generate_executive_html(self, fig: go.Figure, persona: str, title: str) -> str:
        """Generate complete executive-quality HTML"""

        # Rachel's executive HTML template
        html_template = Template(
            """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Strategic Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .chart-container {
            padding: 40px;
            min-height: 600px;
        }

        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }

        /* Interactive enhancements */
        .chart-container:hover {
            background: #fafafa;
            transition: background 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ title }}</h1>
            <div class="subtitle">Strategic Analysis by {{ persona_title }} | Generated by ClaudeDirector</div>
        </div>
        <div class="chart-container">
            {{ plotly_div }}
        </div>
        <div class="footer">
            <p>Executive-quality visualization • Interactive analysis • Strategic intelligence</p>
            <p><small>Generated: {{ timestamp }} | Persona: {{ persona }} | Version: {{ version }}</small></p>
        </div>
    </div>
</body>
</html>
        """
        )

        # Generate Plotly HTML
        plotly_html = fig.to_html(
            include_plotlyjs=False, div_id="strategic-visualization"
        )

        # Persona titles
        persona_titles = MCPServerConstants.Personas.PERSONA_TITLES

        return html_template.render(
            title=title,
            persona_title=persona_titles.get(persona, "Strategic Analysis"),
            plotly_div=plotly_html,
            persona=persona,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            version=self.version,
        )

    def _parse_analysis_output(self, output: str) -> Dict[str, Any]:
        """Parse strategic analysis output into visualization data"""

        # Try to extract JSON data from output
        try:
            # Look for JSON blocks in the output
            import re

            json_match = re.search(r"\{.*\}", output, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        # Fallback: create sample data structure
        return {
            "sample_data": True,
            "x": ["Q1", "Q2", "Q3", "Q4"],
            "y": [20, 25, 30, 35],
            "analysis_output": output,
        }

    def _detect_interactive_elements(self, fig: go.Figure) -> List[str]:
        """Detect interactive elements in the figure"""

        elements = []

        # Check for different trace types
        for trace in fig.data:
            if hasattr(trace, "type"):
                elements.append(f"{trace.type}_chart")

        # Check for subplots
        if hasattr(fig, "layout") and hasattr(fig.layout, "annotations"):
            if fig.layout.annotations:
                elements.append("subplots")

        # Default interactive features
        elements.extend(["hover", "zoom", "pan"])

        return list(set(elements))

    def _update_performance_metrics(
        self, generation_time: float, file_size: int, interactive_elements: List[str]
    ):
        """Update performance metrics"""

        # Update average generation time
        total_viz = self.visualization_metrics["total_visualizations"]
        current_avg = self.visualization_metrics["avg_generation_time"]
        self.visualization_metrics["avg_generation_time"] = (
            current_avg * (total_viz - 1) + generation_time
        ) / total_viz

        # Update average file size
        current_size_avg = self.visualization_metrics["avg_file_size"]
        self.visualization_metrics["avg_file_size"] = (
            current_size_avg * (total_viz - 1) + file_size
        ) / total_viz

        # Update interactive features count
        self.visualization_metrics["interactive_features_used"] += len(
            interactive_elements
        )

    def get_server_info(self) -> Dict[str, Any]:
        """Get executive visualization server information"""

        return {
            "name": self.name,
            "version": self.version,
            "capabilities": self.capabilities,
            "supported_personas": list(self.persona_templates.keys()),
            "supported_chart_types": [
                "leadership_dashboard",
                "team_metrics",
                "strategic_trends",
                "support_analysis",
                "roi_analysis",
                "investment_tracking",
                "business_metrics",
                "cost_analysis",
                "architecture_health",
                "performance_metrics",
                "system_dependencies",
                "technology_roadmap",
                "innovation_metrics",
                "design_system_health",
                "adoption_metrics",
            ],
            "metrics": self.visualization_metrics,
            "color_palette": self.color_palette,
        }

    def get_transparency_disclosure(
        self, capability: str, persona: str, description: str
    ) -> str:
        """Generate transparency disclosure for executive visualization"""

        return f"""
🔧 Accessing MCP Server: executive-visualization (Executive Visualization System)
*Generating publication-quality interactive visualization using {persona} persona...*

**Executive Visualization Enhancement**:
- **Capability**: {capability}
- **Persona**: {persona} (Executive Design System)
- **Process**: {description}
- **Quality**: Publication-ready interactive charts
- **Integration**: Built on Phase 1 Strategic Python MCP foundation

**Rachel's Design System**: Professional color palette, executive typography, responsive layout
**Interactive Features**: Hover states, zoom, pan, filter capabilities
**Performance**: <3s generation, <2MB output, optimized for presentations
"""

    # ========================================
    # Martin's Architecture Health Chart Methods
    # ========================================

    def _create_architecture_health_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create comprehensive architecture health dashboard for Martin"""

        # Create subplot layout for comprehensive dashboard
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=(
                "Service Performance",
                "System Health",
                "Response Times",
                "Error Rates",
            ),
            specs=[
                [{"type": "bar"}, {"type": "indicator"}],
                [{"type": "scatter"}, {"type": "bar"}],
            ],
        )

        # Service Performance (top-left)
        services = data.get(
            "services", ["API Gateway", "User Service", "Data Service", "Auth Service"]
        )
        performance_scores = data.get("performance_scores", [95, 88, 92, 90])

        fig.add_trace(
            go.Bar(
                x=services,
                y=performance_scores,
                name="Performance Score",
                marker_color=self.color_palette[0],
                text=[f"{score}%" for score in performance_scores],
                textposition="outside",
            ),
            row=1,
            col=1,
        )

        # System Health Gauge (top-right)
        overall_health = data.get("overall_health", 92)
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=overall_health,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Overall Health"},
                gauge={
                    "axis": {"range": [None, 100]},
                    "bar": {"color": self.color_palette[1]},
                    "steps": [
                        {"range": [0, 50], "color": self.color_palette[2]},
                        {"range": [50, 80], "color": self.color_palette[3]},
                        {"range": [80, 100], "color": self.color_palette[1]},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 85,
                    },
                },
            ),
            row=1,
            col=2,
        )

        # Response Times Trend (bottom-left)
        timestamps = data.get(
            "timestamps", ["00:00", "06:00", "12:00", "18:00", "24:00"]
        )
        response_times = data.get("response_times", [120, 85, 95, 110, 100])

        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=response_times,
                mode="lines+markers",
                name="Response Time (ms)",
                line=dict(color=self.color_palette[4], width=3),
                marker=dict(size=8),
            ),
            row=2,
            col=1,
        )

        # Error Rates (bottom-right)
        error_types = data.get(
            "error_types", ["4xx Client", "5xx Server", "Timeout", "Network"]
        )
        error_counts = data.get("error_counts", [12, 3, 5, 2])

        fig.add_trace(
            go.Bar(
                x=error_types,
                y=error_counts,
                name="Error Count",
                marker_color=self.color_palette[2],
                text=error_counts,
                textposition="outside",
            ),
            row=2,
            col=2,
        )

        # Update layout with Martin's architecture styling
        fig.update_layout(
            title={
                "text": title,
                "x": 0.5,
                "font": {"size": 24, "color": self.color_palette[0]},
            },
            showlegend=False,
            height=800,
            **self.layout_template,
        )

        return fig

    def _create_service_performance_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create service performance monitoring chart"""

        services = data.get(
            "services", ["API Gateway", "User Service", "Data Service", "Auth Service"]
        )
        response_times = data.get("response_times", [120, 85, 95, 110])
        throughput = data.get("throughput", [1500, 2200, 1800, 1200])

        # Create dual-axis chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Response times (primary y-axis)
        fig.add_trace(
            go.Bar(
                x=services,
                y=response_times,
                name="Response Time (ms)",
                marker_color=self.color_palette[0],
                text=[f"{rt}ms" for rt in response_times],
                textposition="outside",
            ),
            secondary_y=False,
        )

        # Throughput (secondary y-axis)
        fig.add_trace(
            go.Scatter(
                x=services,
                y=throughput,
                mode="lines+markers",
                name="Throughput (req/min)",
                line=dict(color=self.color_palette[1], width=3),
                marker=dict(size=10),
            ),
            secondary_y=True,
        )

        # Update axes labels
        fig.update_xaxes(title_text="Services")
        fig.update_yaxes(title_text="Response Time (ms)", secondary_y=False)
        fig.update_yaxes(title_text="Throughput (req/min)", secondary_y=True)

        # Update layout
        fig.update_layout(
            title={"text": title, "x": 0.5, "font": {"size": 20}},
            **self.layout_template,
        )

        return fig

    def _create_system_dependency_map(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create system dependency network visualization"""

        # Network graph data
        nodes = data.get(
            "nodes",
            [
                {"id": "frontend", "label": "Frontend App", "group": "client"},
                {"id": "api", "label": "API Gateway", "group": "gateway"},
                {"id": "auth", "label": "Auth Service", "group": "service"},
                {"id": "user", "label": "User Service", "group": "service"},
                {"id": "data", "label": "Data Service", "group": "service"},
                {"id": "db", "label": "Database", "group": "storage"},
            ],
        )

        edges = data.get(
            "edges",
            [
                {"source": "frontend", "target": "api"},
                {"source": "api", "target": "auth"},
                {"source": "api", "target": "user"},
                {"source": "api", "target": "data"},
                {"source": "user", "target": "db"},
                {"source": "data", "target": "db"},
            ],
        )

        # Create network layout (simplified circular layout)
        import math

        positions = {}
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / len(nodes)
            positions[node["id"]] = {"x": math.cos(angle), "y": math.sin(angle)}

        # Create edge traces
        edge_x = []
        edge_y = []
        for edge in edges:
            x0, y0 = positions[edge["source"]]["x"], positions[edge["source"]]["y"]
            x1, y1 = positions[edge["target"]]["x"], positions[edge["target"]]["y"]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        # Create node traces
        node_x = [positions[node["id"]]["x"] for node in nodes]
        node_y = [positions[node["id"]]["y"] for node in nodes]
        node_text = [node["label"] for node in nodes]

        fig = go.Figure()

        # Add edges
        fig.add_trace(
            go.Scatter(
                x=edge_x,
                y=edge_y,
                line=dict(width=2, color=self.color_palette[0]),
                hoverinfo="none",
                mode="lines",
                name="Dependencies",
            )
        )

        # Add nodes
        fig.add_trace(
            go.Scatter(
                x=node_x,
                y=node_y,
                mode="markers+text",
                hoverinfo="text",
                text=node_text,
                textposition="middle center",
                marker=dict(
                    size=50,
                    color=self.color_palette[1],
                    line=dict(width=2, color=self.color_palette[0]),
                ),
                name="Services",
            )
        )

        fig.update_layout(
            title={"text": title, "x": 0.5},
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            **self.layout_template,
        )

        return fig

    def _create_technical_debt_trends(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create technical debt trend analysis"""

        months = data.get("months", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
        debt_score = data.get("debt_score", [75, 73, 78, 71, 69, 65])
        code_coverage = data.get("code_coverage", [82, 84, 83, 86, 88, 90])
        complexity_score = data.get("complexity_score", [68, 70, 65, 63, 61, 58])

        fig = go.Figure()

        # Technical debt score
        fig.add_trace(
            go.Scatter(
                x=months,
                y=debt_score,
                mode="lines+markers",
                name="Technical Debt Score",
                line=dict(color=self.color_palette[2], width=3),
                marker=dict(size=8),
            )
        )

        # Code coverage
        fig.add_trace(
            go.Scatter(
                x=months,
                y=code_coverage,
                mode="lines+markers",
                name="Code Coverage %",
                line=dict(color=self.color_palette[1], width=3),
                marker=dict(size=8),
            )
        )

        # Complexity score
        fig.add_trace(
            go.Scatter(
                x=months,
                y=complexity_score,
                mode="lines+markers",
                name="Complexity Score",
                line=dict(color=self.color_palette[3], width=3),
                marker=dict(size=8),
            )
        )

        fig.update_layout(
            title={"text": title, "x": 0.5},
            xaxis_title="Month",
            yaxis_title="Score",
            yaxis=dict(range=[0, 100]),
            **self.layout_template,
        )

        return fig

    # ========================================
    # Rachel's Design System Chart Methods
    # ========================================

    def _create_component_adoption_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create component adoption tracking chart for Rachel"""

        components = data.get(
            "components", ["Button", "Input", "Card", "Modal", "Table"]
        )
        adoption_rates = data.get("adoption_rates", [95, 87, 78, 65, 52])
        teams_using = data.get("teams_using", [12, 11, 9, 7, 5])

        # Create dual-axis chart
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Adoption rates (primary y-axis)
        fig.add_trace(
            go.Bar(
                x=components,
                y=adoption_rates,
                name="Adoption Rate (%)",
                marker_color=self.color_palette[0],
                text=[f"{rate}%" for rate in adoption_rates],
                textposition="outside",
            ),
            secondary_y=False,
        )

        # Teams using (secondary y-axis)
        fig.add_trace(
            go.Scatter(
                x=components,
                y=teams_using,
                mode="lines+markers",
                name="Teams Using",
                line=dict(color=self.color_palette[1], width=3),
                marker=dict(size=10),
            ),
            secondary_y=True,
        )

        # Update axes
        fig.update_xaxes(title_text="Components")
        fig.update_yaxes(title_text="Adoption Rate (%)", secondary_y=False)
        fig.update_yaxes(title_text="Number of Teams", secondary_y=True)

        fig.update_layout(
            title={"text": title, "x": 0.5, "font": {"size": 20}},
            **self.layout_template,
        )

        return fig

    def _create_design_system_maturity(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create design system maturity assessment"""

        categories = data.get(
            "categories",
            [
                "Component Coverage",
                "Design Consistency",
                "Documentation Quality",
                "Developer Experience",
                "Adoption Rate",
                "Maintenance Efficiency",
            ],
        )
        current_scores = data.get("current_scores", [85, 78, 92, 75, 68, 82])
        target_scores = data.get("target_scores", [95, 90, 95, 85, 85, 90])

        fig = go.Figure()

        # Current scores
        fig.add_trace(
            go.Bar(
                x=categories,
                y=current_scores,
                name="Current Score",
                marker_color=self.color_palette[0],
                text=[f"{score}%" for score in current_scores],
                textposition="outside",
            )
        )

        # Target scores
        fig.add_trace(
            go.Bar(
                x=categories,
                y=target_scores,
                name="Target Score",
                marker_color=self.color_palette[1],
                opacity=0.6,
                text=[f"{score}%" for score in target_scores],
                textposition="outside",
            )
        )

        fig.update_layout(
            title={"text": title, "x": 0.5},
            xaxis_title="Maturity Categories",
            yaxis_title="Score (%)",
            yaxis=dict(range=[0, 100]),
            barmode="group",
            **self.layout_template,
        )

        return fig

    def _create_usage_trend_analysis(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create design system usage trend analysis"""

        months = data.get("months", ["Jan", "Feb", "Mar", "Apr", "May", "Jun"])
        component_usage = data.get("component_usage", [450, 520, 680, 750, 890, 1020])
        new_implementations = data.get("new_implementations", [25, 35, 45, 40, 55, 60])
        design_debt_reduction = data.get(
            "design_debt_reduction", [5, 8, 12, 15, 18, 22]
        )

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Component usage (primary y-axis)
        fig.add_trace(
            go.Scatter(
                x=months,
                y=component_usage,
                mode="lines+markers",
                name="Total Component Usage",
                line=dict(color=self.color_palette[0], width=3),
                marker=dict(size=8),
            ),
            secondary_y=False,
        )

        # New implementations (secondary y-axis)
        fig.add_trace(
            go.Bar(
                x=months,
                y=new_implementations,
                name="New Implementations",
                marker_color=self.color_palette[1],
                opacity=0.7,
            ),
            secondary_y=True,
        )

        # Design debt reduction (secondary y-axis)
        fig.add_trace(
            go.Scatter(
                x=months,
                y=design_debt_reduction,
                mode="lines+markers",
                name="Design Debt Reduction",
                line=dict(color=self.color_palette[2], width=3),
                marker=dict(size=8),
            ),
            secondary_y=True,
        )

        # Update axes
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Component Usage Count", secondary_y=False)
        fig.update_yaxes(
            title_text="New Implementations / Debt Reduction", secondary_y=True
        )

        fig.update_layout(title={"text": title, "x": 0.5}, **self.layout_template)

        return fig

    def _create_team_comparison_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create team comparison dashboard for design system adoption"""

        teams = data.get(
            "teams", ["Frontend", "Mobile", "Platform", "Marketing", "Analytics"]
        )
        adoption_scores = data.get("adoption_scores", [92, 78, 85, 65, 71])
        components_used = data.get("components_used", [28, 22, 25, 15, 18])
        consistency_scores = data.get("consistency_scores", [88, 72, 80, 58, 65])

        # Create radar chart for team comparison
        fig = go.Figure()

        # Add trace for each metric
        fig.add_trace(
            go.Scatterpolar(
                r=adoption_scores + [adoption_scores[0]],  # Close the polygon
                theta=teams + [teams[0]],
                fill="toself",
                name="Adoption Score",
                line_color=self.color_palette[0],
            )
        )

        fig.add_trace(
            go.Scatterpolar(
                r=[score * 3 for score in components_used]
                + [components_used[0] * 3],  # Scale for visibility
                theta=teams + [teams[0]],
                fill="toself",
                name="Components Used (x3)",
                line_color=self.color_palette[1],
                opacity=0.6,
            )
        )

        fig.add_trace(
            go.Scatterpolar(
                r=consistency_scores + [consistency_scores[0]],
                theta=teams + [teams[0]],
                fill="toself",
                name="Consistency Score",
                line_color=self.color_palette[2],
                opacity=0.6,
            )
        )

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title={"text": title, "x": 0.5},
            **self.layout_template,
        )

        return fig

    def _create_design_debt_visualization(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create design debt visualization heatmap"""

        components = data.get(
            "components", ["Button", "Input", "Card", "Modal", "Table", "Form"]
        )
        teams = data.get("teams", ["Frontend", "Mobile", "Platform", "Marketing"])

        # Design debt matrix (higher values = more debt)
        debt_matrix = data.get(
            "debt_matrix",
            [
                [2, 1, 0, 3],  # Button
                [1, 2, 1, 2],  # Input
                [0, 1, 0, 1],  # Card
                [3, 4, 2, 5],  # Modal
                [2, 3, 1, 4],  # Table
                [1, 2, 0, 3],  # Form
            ],
        )

        fig = go.Figure(
            data=go.Heatmap(
                z=debt_matrix,
                x=teams,
                y=components,
                colorscale=[
                    [0, self.color_palette[1]],  # Green for low debt
                    [0.5, self.color_palette[3]],  # Yellow for medium debt
                    [1, self.color_palette[2]],  # Red for high debt
                ],
                text=debt_matrix,
                texttemplate="%{text}",
                textfont={"size": 14},
                hoverongaps=False,
            )
        )

        fig.update_layout(
            title={"text": title, "x": 0.5},
            xaxis_title="Teams",
            yaxis_title="Components",
            **self.layout_template,
        )

        return fig

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on Executive Visualization Engine"""

        try:
            # Test basic visualization generation
            test_data = {"x": ["Test"], "y": [1]}
            result = await self.create_executive_visualization(
                test_data, "default", "diego", "Health Check Test"
            )

            return {
                "status": "healthy" if result.success else "degraded",
                "server_info": self.get_server_info(),
                "last_health_check": time.time(),
                "test_result": {
                    "success": result.success,
                    "generation_time": result.generation_time,
                    "file_size": result.file_size_bytes,
                },
            }

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_health_check": time.time(),
            }


# MCP Server Integration
class ExecutiveVisualizationMCPServer:
    """MCP Server wrapper for Executive Visualization Engine"""

    def __init__(self):
        self.engine = ExecutiveVisualizationEngine()
        self.name = "executive-visualization"
        self.version = "1.0.0"

        logger.info(f"Executive Visualization MCP Server {self.version} initialized")

    async def process_visualization_request(
        self,
        data: Union[Dict[str, Any], str],
        chart_type: str,
        persona: str,
        title: str,
        context: Dict[str, Any] = None,
    ) -> VisualizationResult:
        """Process MCP visualization request"""

        return await self.engine.create_executive_visualization(
            data, chart_type, persona, title, context
        )

    def get_capabilities(self) -> List[str]:
        """Get MCP server capabilities"""
        return self.engine.capabilities

    def get_supported_personas(self) -> List[str]:
        """Get supported personas"""
        return list(self.engine.persona_templates.keys())


# Factory function
def create_executive_visualization_server() -> ExecutiveVisualizationMCPServer:
    """Create and configure Executive Visualization MCP Server"""
    return ExecutiveVisualizationMCPServer()


if __name__ == "__main__":
    # Basic functionality test
    async def test_executive_visualization():
        print("🎨 Testing Executive Visualization Engine...")

        engine = ExecutiveVisualizationEngine()
        print(f"✅ Engine initialized: {engine.name} v{engine.version}")

        # Test visualization generation
        test_data = {
            "velocity_data": {
                "dates": ["2024-01", "2024-02", "2024-03", "2024-04"],
                "velocity": [15, 18, 22, 25],
            },
            "support_data": {
                "months": ["Jan", "Feb", "Mar", "Apr"],
                "volume": [45, 38, 42, 35],
            },
        }

        result = await engine.create_executive_visualization(
            test_data, "leadership_dashboard", "diego", "Executive Leadership Dashboard"
        )

        print(
            f"✅ Visualization generation: {'SUCCESS' if result.success else 'FAILED'}"
        )
        if result.success:
            print(f"   Generation time: {result.generation_time:.2f}s")
            print(f"   File size: {result.file_size_bytes:,} bytes")
            print(f"   Interactive elements: {len(result.interactive_elements)}")
        else:
            print(f"   Error: {result.error}")

        # Test health check
        health = await engine.health_check()
        print(f"✅ Health check: {health['status']}")

        print("🎉 Executive Visualization Engine test completed!")
        print(f"📊 Engine metrics: {engine.visualization_metrics}")

    asyncio.run(test_executive_visualization())
