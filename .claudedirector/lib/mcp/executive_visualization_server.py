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

# Phase 4.2.1: HTML template processor consolidation for DRY compliance (Sequential Thinking)
from .html_template_processor import HTMLTemplateProcessor

# Phase 4.3.1: Visualization utility processor consolidation for DRY compliance (Sequential Thinking)
from .visualization_utility_processor import VisualizationUtilityProcessor

# Phase 4.3.2: Ultimate orchestration processor consolidation for DRY compliance (Sequential Thinking)
from .visualization_orchestration_processor import VisualizationOrchestrationProcessor

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

        # Phase 4.2.1: HTML template processor consolidation (Sequential Thinking DRY consolidation)
        self.html_processor = HTMLTemplateProcessor()

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

        # Phase 4.3.1: Visualization utility processor consolidation (Sequential Thinking DRY consolidation)
        self.utility_processor = VisualizationUtilityProcessor(
            self.color_palette, self.layout_template, self.visualization_metrics
        )

        # Phase 4.3.2: Ultimate orchestration processor consolidation (Sequential Thinking DRY consolidation)
        self.orchestration_processor = VisualizationOrchestrationProcessor(
            self.template_router,
            self.dashboard_factory,
            self.html_processor,
            self.utility_processor,
            self.chat_generator,
            self.visualization_metrics,
            self.version,
        )

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
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return await self.orchestration_processor.create_executive_visualization(
            data, chart_type, persona, title, context, MCPServerConstants
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
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return await self.orchestration_processor.generate_chat_embedded_visualization(
            query_data, persona, context
        )

    def _infer_chart_type_from_data(self, data: Dict[str, Any]) -> str:
        """🏗️ Sequential Thinking Phase 4.3.1: Delegate to utility processor"""
        return self.utility_processor.infer_chart_type_from_data(data)

    def _generate_contextual_title(
        self, data: Dict[str, Any], context: Dict[str, Any] = None
    ) -> str:
        """🏗️ Sequential Thinking Phase 4.3.1: Delegate to utility processor"""
        return self.utility_processor.generate_contextual_title(data, context)

    async def _create_chat_optimized_chart(
        self, data: Dict[str, Any], chart_type: str, title: str, persona: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return await self.orchestration_processor.create_chat_optimized_chart(
            data, chart_type, title, persona
        )

    # Chat methods consolidated in Phase 3B.2.2 (ChatVisualizationGenerator)

    def _generate_chat_embedded_html(
        self, fig: go.Figure, title: str, persona: str, context: Dict[str, Any] = None
    ) -> str:
        """🏗️ Sequential Thinking Phase 4.2.1: Delegate to HTML template processor"""
        return self.html_processor.generate_chat_embedded_html(
            fig, title, persona, context
        )

    def _apply_executive_styling(self, fig: go.Figure, persona: str) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4.3.1: Delegate to utility processor"""
        return self.utility_processor.apply_executive_styling(
            fig,
            persona,
            MCPServerConstants.Colors.PERSONA_COLORS,
            MCPServerConstants.Colors.PRIMARY_BLUE,
            MCPServerConstants.Typography.TITLE_FONT_SIZE,
        )

    def _generate_executive_html(self, fig: go.Figure, persona: str, title: str) -> str:
        """🏗️ Sequential Thinking Phase 4.2.1: Delegate to HTML template processor"""
        return self.html_processor.generate_executive_html(
            fig,
            persona,
            title,
            MCPServerConstants.Personas.PERSONA_TITLES,
            self.version,
        )

    def _parse_analysis_output(self, output: str) -> Dict[str, Any]:
        """🏗️ Sequential Thinking Phase 4.3.1: Delegate to utility processor"""
        return self.utility_processor.parse_analysis_output(output)

    def _detect_interactive_elements(self, fig: go.Figure) -> List[str]:
        """🏗️ Sequential Thinking Phase 4.3.1: Delegate to utility processor"""
        return self.utility_processor.detect_interactive_elements(fig)

    def _update_performance_metrics(
        self, generation_time: float, file_size: int, interactive_elements: List[str]
    ):
        """🏗️ Sequential Thinking Phase 4.3.1: Delegate to utility processor"""
        self.utility_processor.update_performance_metrics(
            generation_time, file_size, interactive_elements
        )

    def get_server_info(self) -> Dict[str, Any]:
        """🏗️ Sequential Thinking Phase 4.3.1: Delegate to utility processor"""
        # Get supported personas from constants
        supported_personas = list(MCPServerConstants.Personas.PERSONA_TITLES.keys())
        return self.utility_processor.get_server_info(
            self.name,
            self.version,
            self.capabilities,
            supported_personas,
            self.color_palette,
        )

    def get_transparency_disclosure(
        self, capability: str, persona: str, description: str
    ) -> str:
        """🏗️ Sequential Thinking Phase 4.3.1: Delegate to utility processor"""
        return self.utility_processor.get_transparency_disclosure(
            capability, persona, description
        )

    # ========================================
    # Martin's Architecture Health Chart Methods
    # ========================================

    def _create_architecture_health_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return self.orchestration_processor.create_architecture_health_dashboard(
            data, title
        )

    def _create_service_performance_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return self.orchestration_processor.create_service_performance_chart(
            data, title
        )

    def _create_system_dependency_map(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return self.orchestration_processor.create_system_dependency_map(data, title)

    def _create_technical_debt_trends(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return self.orchestration_processor.create_technical_debt_trends(data, title)

    # ========================================
    # Rachel's Design System Chart Methods
    # ========================================

    def _create_component_adoption_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return self.orchestration_processor.create_component_adoption_chart(data, title)

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
        """🏗️ Sequential Thinking Phase 4.3.2: Delegate to orchestration processor"""
        return self.orchestration_processor.create_design_debt_visualization(
            data, title
        )

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
