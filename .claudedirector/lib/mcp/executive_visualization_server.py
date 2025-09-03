#!/usr/bin/env python3
"""Executive Visualization MCP Server - Sequential Thinking Phase 4.4+ Ultra-Facade"""

import logging
from typing import Dict, Any, List, Optional, Union
import plotly.graph_objects as go

from .visualization_types import VisualizationResult
from .visualization_template_router import VisualizationTemplateRouter
from .chat_visualization_generator import ChatVisualizationGenerator
from .visualization_dashboard_factory import VisualizationDashboardFactory
from .html_template_processor import HTMLTemplateProcessor
from .visualization_utility_processor import VisualizationUtilityProcessor
from .visualization_orchestration_processor import VisualizationOrchestrationProcessor
from .executive_visualization_engine_factory import ExecutiveVisualizationEngineFactory
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
        """🏗️ Sequential Thinking Phase 4.4.2: Ultra-aggressive facade using initialization factory"""
        ExecutiveVisualizationEngineFactory.initialize_engine(self)

    async def create_executive_visualization(
        self,
        data: Union[Dict[str, Any], str],
        chart_type: str,
        persona: str,
        title: str,
        context: Dict[str, Any] = None,
    ) -> VisualizationResult:
        """🏗️ Delegate to orchestration processor"""
        return await self.orchestration_processor.create_executive_visualization(
            data, chart_type, persona, title, context, MCPServerConstants
        )

    def _create_leadership_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to dashboard factory"""
        return self.dashboard_factory.create_dashboard("leadership", data, title)

    def _create_roi_dashboard(self, data: Dict[str, Any], title: str) -> go.Figure:
        """🏗️ Delegate to dashboard factory"""
        return self.dashboard_factory.create_dashboard("roi", data, title)

    def _create_default_chart(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """🏗️ Delegate to orchestration processor"""
        return self.orchestration_processor.create_default_chart(
            data, chart_type, title
        )

    async def generate_chat_embedded_visualization(
        self,
        query_data: Dict[str, Any],
        persona: str = "diego",
        context: Dict[str, Any] = None,
    ) -> VisualizationResult:
        """🏗️ Delegate to orchestration processor"""
        return await self.orchestration_processor.generate_chat_embedded_visualization(
            query_data, persona, context
        )

    def _infer_chart_type_from_data(self, data: Dict[str, Any]) -> str:
        """🏗️ Delegate to utility processor"""
        return self.utility_processor.infer_chart_type_from_data(data)

    def _generate_contextual_title(
        self, data: Dict[str, Any], context: Dict[str, Any] = None
    ) -> str:
        """🏗️ Delegate to utility processor"""
        return self.utility_processor.generate_contextual_title(data, context)

    async def _create_chat_optimized_chart(
        self, data: Dict[str, Any], chart_type: str, title: str, persona: str
    ) -> go.Figure:
        """🏗️ Delegate to orchestration processor"""
        return await self.orchestration_processor.create_chat_optimized_chart(
            data, chart_type, title, persona
        )

    def _generate_chat_embedded_html(
        self, fig: go.Figure, title: str, persona: str, context: Dict[str, Any] = None
    ) -> str:
        """🏗️ Delegate to HTML template processor"""
        return self.html_processor.generate_chat_embedded_html(
            fig, title, persona, context
        )

    def _apply_executive_styling(self, fig: go.Figure, persona: str) -> go.Figure:
        """🏗️ Delegate to utility processor"""
        return self.utility_processor.apply_executive_styling(
            fig,
            persona,
            MCPServerConstants.Colors.PERSONA_COLORS,
            MCPServerConstants.Colors.PRIMARY_BLUE,
            MCPServerConstants.Typography.TITLE_FONT_SIZE,
        )

    def _generate_executive_html(self, fig: go.Figure, persona: str, title: str) -> str:
        """🏗️ Delegate to HTML template processor"""
        return self.html_processor.generate_executive_html(
            fig,
            persona,
            title,
            MCPServerConstants.Personas.PERSONA_TITLES,
            self.version,
        )

    def _parse_analysis_output(self, output: str) -> Dict[str, Any]:
        """🏗️ Delegate to utility processor"""
        return self.utility_processor.parse_analysis_output(output)

    def _detect_interactive_elements(self, fig: go.Figure) -> List[str]:
        """🏗️ Delegate to utility processor"""
        return self.utility_processor.detect_interactive_elements(fig)

    def _update_performance_metrics(
        self, generation_time: float, file_size: int, interactive_elements: List[str]
    ):
        """🏗️ Delegate to utility processor"""
        self.utility_processor.update_performance_metrics(
            generation_time, file_size, interactive_elements
        )

    def get_server_info(self) -> Dict[str, Any]:
        """🏗️ Delegate to utility processor"""
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
        """🏗️ Delegate to utility processor"""
        return self.utility_processor.get_transparency_disclosure(
            capability, persona, description
        )

    # Martin's Architecture Health Methods

    def _create_architecture_health_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to orchestration processor"""
        return self.orchestration_processor.create_architecture_health_dashboard(
            data, title
        )

    def _create_service_performance_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to orchestration processor"""
        return self.orchestration_processor.create_service_performance_chart(
            data, title
        )

    def _create_system_dependency_map(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to orchestration processor"""
        return self.orchestration_processor.create_system_dependency_map(data, title)

    def _create_technical_debt_trends(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to orchestration processor"""
        return self.orchestration_processor.create_technical_debt_trends(data, title)

    # Rachel's Design System Methods

    def _create_component_adoption_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to orchestration processor"""
        return self.orchestration_processor.create_component_adoption_chart(data, title)

    def _create_design_system_maturity(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to dashboard factory"""
        return self.dashboard_factory.create_dashboard(
            "design_system_maturity", data, title
        )

    def _create_usage_trend_analysis(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to dashboard factory"""
        return self.dashboard_factory.create_dashboard(
            "usage_trend_analysis", data, title
        )

    def _create_team_comparison_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to dashboard factory"""
        return self.dashboard_factory.create_dashboard("team_comparison", data, title)

    def _create_design_debt_visualization(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Delegate to orchestration processor"""
        return self.orchestration_processor.create_design_debt_visualization(
            data, title
        )

    async def health_check(self) -> Dict[str, Any]:
        """🏗️ Sequential Thinking Phase 4.4.1: Delegate to orchestration processor"""
        return await self.orchestration_processor.health_check(
            self.create_executive_visualization, self.get_server_info()
        )

    def _generate_error_visualization(self, error_message: str) -> str:
        """🏗️ Sequential Thinking Phase 4.4.1: Delegate to orchestration processor"""
        return self.orchestration_processor.generate_error_visualization(error_message)


class ExecutiveVisualizationMCPServer:
    """MCP Server wrapper for Executive Visualization Engine"""

    def __init__(self):
        self.engine = ExecutiveVisualizationEngine()
        self.name, self.version = "executive-visualization", "1.0.0"
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
        return [
            "diego",
            "camille",
            "rachel",
            "alvaro",
            "martin",
        ]  # Fixed: hardcoded list


def create_executive_visualization_server() -> ExecutiveVisualizationMCPServer:
    """Create and configure Executive Visualization MCP Server"""
    return ExecutiveVisualizationMCPServer()


# 🏗️ Sequential Thinking Phase 4.4.1: Test code moved to separate test module for clean production code
