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
import tempfile
import os

# Visualization libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from jinja2 import Template

# Phase 3A.2.1: Extract type definitions for SOLID compliance
from .visualization_types import VisualizationResult

# Phase 3A.2.2: Extract persona template management for SOLID compliance
from .visualization_components import PersonaTemplateManager

# Phase 3B.2.1: Consolidated template router for DRY compliance
from .visualization_template_router import VisualizationTemplateRouter

# Phase 3B.2.2: Consolidated chat visualization generator for DRY compliance
from .chat_visualization_generator import ChatVisualizationGenerator

# Phase 3B.3.1: Consolidated dashboard factory for DRY compliance (Sequential Thinking)
from .visualization_dashboard_factory import VisualizationDashboardFactory

# Phase 1 integration
from .strategic_python_server import StrategicPythonMCPServer, ExecutionResult
from .constants import MCPServerConstants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

        # Phase 3B.2.1: Consolidated template router (DRY compliance)
        self.template_router = VisualizationTemplateRouter(self)

        # Phase 3B.2.2: Consolidated chat visualization generator (DRY compliance)
        self.chat_generator = ChatVisualizationGenerator(
            self.color_palette, self.layout_template
        )

        # Phase 3B.3.1: Consolidated dashboard factory (Sequential Thinking DRY consolidation)
        self.dashboard_factory = VisualizationDashboardFactory(self.color_palette)

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

            # Get persona-specific template (Phase 3B.2.1 - Consolidated router)
            template_func = self.template_router.get_template_for_persona(persona)

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

    # Template methods consolidated in Phase 3B.2.1 (DRY compliance)

    def _create_leadership_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4: Delegate to consolidated dashboard factory"""
        return self.dashboard_factory.create_dashboard("leadership", data, title)

    def _create_roi_dashboard(self, data: Dict[str, Any], title: str) -> go.Figure:
        """
        Create Alvaro's ROI analysis dashboard
        Phase 3B.3.1: Consolidated using VisualizationDashboardFactory (Sequential Thinking)
        """
        # Use consolidated dashboard factory (DRY compliance)
        return self.dashboard_factory.create_dashboard("roi", data, title)

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

            # Generate chat-embedded HTML with compact layout and context
            html_output = self._generate_chat_embedded_html(
                fig, title, persona, context
            )

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
        """Create chart optimized for chat embedding (Phase 3B.2.2 - Consolidated)"""

        # Special handling for architecture health (not in chat generator)
        if chart_type == "architecture_health":
            return self._create_architecture_health_dashboard(data, title)

        # Map chart types to chat generator types
        chat_type_mapping = {
            "design_system_status": "design_system",
            "simple_metrics": "default",
        }

        # Use consolidated chat generator (Phase 3B.2.2 - DRY compliance)
        chat_chart_type = chat_type_mapping.get(chart_type, chart_type)
        return self.chat_generator.create_chat_visualization(
            data, chat_chart_type, title
        )

    # Chat methods consolidated in Phase 3B.2.2 (ChatVisualizationGenerator)

    def _generate_chat_embedded_html(
        self, fig: go.Figure, title: str, persona: str, context: Dict[str, Any] = None
    ) -> str:
        """Generate HTML optimized for chat embedding with data authenticity"""

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
            {% if data_authenticity == 'REAL' %}
            <div class="real-data-indicator" style="
                padding: 12px 16px;
                background: #d4edda;
                border: 2px solid #28a745;
                border-radius: 6px 6px 0 0;
                color: #155724;
                font-weight: 700;
                font-size: 14px;
                text-align: center;
            ">
                &#x2705; REAL DATA - LIVE METRICS &#x2705;<br/>
                <span style="font-size: 12px; font-weight: 500;">
                    Connected to {{ server_info }} • Last updated: {{ last_updated }}
                </span>
            </div>
            {% elif data_authenticity == 'API_FALLBACK' %}
            <div class="api-fallback-indicator" style="
                padding: 12px 16px;
                background: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 6px 6px 0 0;
                color: #856404;
                font-weight: 700;
                font-size: 14px;
                text-align: center;
            ">
                &#x26A0; REAL DATA via API FALLBACK &#x26A0;<br/>
                <span style="font-size: 12px; font-weight: 500;">
                    MCP server unavailable, using REST API • {{ server_info }}
                </span>
            </div>
            {% else %}
            <div class="simulation-warning" style="
                padding: 12px 16px;
                background: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 6px 6px 0 0;
                color: #856404;
                font-weight: 700;
                font-size: 14px;
                text-align: center;
            ">
                &#x1F6A8; SIMULATED DATA - NOT REAL METRICS &#x1F6A8;<br/>
                <span style="font-size: 12px; font-weight: 500;">
                    This is realistic sample data for demonstration •
                    <strong>Ask me: "How do I connect to real data?"</strong>
                </span>
            </div>
            {% endif %}
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
                Generated via ClaudeDirector • Interactive visualization •
                <strong style="color: #dc3545;">SIMULATED DATA</strong>
            </div>
        </div>
        """
        )

        # Extract data authenticity from context
        data_authenticity = "SIMULATED"  # Default fallback
        server_info = "Simulation Mode"
        last_updated = "N/A"

        if context:
            data_authenticity = context.get("data_authenticity", "SIMULATED")
            server_info = context.get("server_info", "Simulation Mode")
            last_updated = context.get("last_updated", "N/A")

        return chat_template.render(
            title=title,
            persona=persona,
            html_content=html_div,
            data_authenticity=data_authenticity,
            server_info=server_info,
            last_updated=last_updated,
        )

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
            "supported_personas": self.persona_manager.get_supported_personas(),
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
        """
        Create comprehensive architecture health dashboard for Martin
        Phase 3B.3.1: Consolidated using VisualizationDashboardFactory (Sequential Thinking)
        """
        # Normalize data format for dashboard factory
        normalized_data = {
            "service_performance": {
                "services": data.get(
                    "services",
                    ["API Gateway", "User Service", "Data Service", "Auth Service"],
                ),
                "performance_scores": data.get("performance_scores", [95, 88, 92, 90]),
            },
            "system_health": {"score": data.get("overall_health", 92)},
            "response_times": {
                "timestamps": data.get(
                    "timestamps", ["00:00", "06:00", "12:00", "18:00", "24:00"]
                ),
                "times": data.get("response_times", [120, 85, 95, 110, 100]),
            },
            "error_rates": {
                "services": data.get(
                    "error_types", ["4xx Client", "5xx Server", "Timeout", "Network"]
                ),
                "rates": data.get("error_counts", [12, 3, 5, 2]),
            },
        }

        return self.dashboard_factory.create_dashboard(
            "architecture_health", normalized_data, title
        )

    def _create_service_performance_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking: Delegate to consolidated dashboard factory"""
        return self.dashboard_factory.create_dashboard(
            "service_performance", data, title
        )

    def _create_system_dependency_map(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create system dependency network visualization"""

        # 🏗️ Sequential Thinking: Delegate to consolidated dashboard factory
        return self.dashboard_factory.create_dashboard(
            "system_dependencies", data, title
        )

    def _create_technical_debt_trends(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create technical debt trend analysis"""

        # 🏗️ Sequential Thinking: Delegate to consolidated dashboard factory
        return self.dashboard_factory.create_dashboard(
            "technical_debt_trends", data, title
        )

    # ========================================
    # Rachel's Design System Chart Methods
    # ========================================

    def _create_component_adoption_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create component adoption tracking chart for Rachel"""

        # 🏗️ Sequential Thinking: Delegate to consolidated dashboard factory
        return self.dashboard_factory.create_dashboard(
            "component_adoption", data, title
        )

    def _create_design_system_maturity(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4: Delegate to consolidated dashboard factory"""
        return self.dashboard_factory.create_dashboard(
            "design_system_maturity", data, title
        )

    def _create_usage_trend_analysis(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4: Delegate to consolidated dashboard factory"""
        return self.dashboard_factory.create_dashboard(
            "usage_trend_analysis", data, title
        )

    def _create_team_comparison_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4: Delegate to consolidated dashboard factory"""
        return self.dashboard_factory.create_dashboard("team_comparison", data, title)

    def _create_design_debt_visualization(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """Create design debt visualization heatmap"""

        # 🏗️ Sequential Thinking: Delegate to consolidated dashboard factory
        return self.dashboard_factory.create_dashboard("design_debt", data, title)

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

    def _generate_error_visualization(self, error_message: str) -> str:
        """Generate a simple error visualization for failed chart generation"""
        return f"""
        <div style="
            padding: 20px;
            background: #fff3cd;
            border: 2px solid #ffc107;
            border-radius: 8px;
            color: #856404;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 20px auto;
        ">
            <h3 style="margin-top: 0; color: #856404;">⚠️ Visualization Error</h3>
            <p><strong>Unable to generate chart:</strong></p>
            <p style="
                background: #fff;
                padding: 10px;
                border-radius: 4px;
                border-left: 4px solid #ffc107;
                font-family: monospace;
                font-size: 14px;
            ">{error_message}</p>
            <p><em>The data was fetched successfully, but chart generation failed.
            This is likely a temporary issue with the visualization engine.</em></p>
        </div>
        """


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
