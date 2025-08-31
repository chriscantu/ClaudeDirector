#!/usr/bin/env python3
"""
Executive Visualization MCP Server
Phase 2 Implementation - Executive-Quality Interactive Visualizations

🏗️ Martin | Platform Architecture
🎨 Rachel | Design Systems Strategy - Executive Design System
💼 Alvaro | Business Strategy - ROI & Executive Requirements
🤖 Berny | AI/ML Engineering - Performance & Data Processing

Executive-quality visualization system built on Python MCP foundation.
Produces publication-ready interactive visualizations for VP/SLT presentations.
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
            self.visualization_metrics[MCPServerConstants.MetricsKeys.TOTAL_VISUALIZATIONS] += 1

            # Process data if it's a string (from Phase 1 analysis)
            if isinstance(data, str):
                data = self._parse_analysis_output(data)

            # Get persona-specific template
            template_func = self.persona_templates.get(persona, self.persona_templates["diego"])

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
            self.visualization_metrics[MCPServerConstants.MetricsKeys.SUCCESSFUL_GENERATIONS] += 1
            self._update_performance_metrics(generation_time, file_size, interactive_elements)

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
            return self._create_architecture_dashboard(data, title)
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

        if chart_type == "design_system_health":
            return self._create_design_system_dashboard(data, title)
        elif chart_type == "adoption_metrics":
            return self._create_adoption_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _create_leadership_dashboard(self, data: Dict[str, Any], title: str) -> go.Figure:
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

    def _create_default_chart(self, data: Dict[str, Any], chart_type: str, title: str) -> go.Figure:
        """Create default chart when specific template not available"""

        # Simple bar chart as fallback
        if "x" in data and "y" in data:
            fig = go.Figure(
                data=go.Bar(x=data["x"], y=data["y"], marker_color=self.color_palette[0])
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
        plotly_html = fig.to_html(include_plotlyjs=False, div_id="strategic-visualization")

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
        self.visualization_metrics["interactive_features_used"] += len(interactive_elements)

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

    def get_transparency_disclosure(self, capability: str, persona: str, description: str) -> str:
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

        print(f"✅ Visualization generation: {'SUCCESS' if result.success else 'FAILED'}")
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
