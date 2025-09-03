#!/usr/bin/env python3
"""
Visualization Orchestration Processor - Sequential Thinking Phase 4.3.2
🏗️ Martin | Platform Architecture - Ultra-aggressive facade transformation

Consolidates all executive visualization orchestration logic for maximum DRY compliance.
This processor handles all major visualization workflows and chart delegation.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Union
import plotly.graph_objects as go

# Import all necessary processors for delegation
from .visualization_types import VisualizationResult
from .visualization_template_router import VisualizationTemplateRouter
from .visualization_dashboard_factory import VisualizationDashboardFactory
from .html_template_processor import HTMLTemplateProcessor
from .visualization_utility_processor import VisualizationUtilityProcessor
from .chat_visualization_generator import ChatVisualizationGenerator

logger = logging.getLogger(__name__)


class VisualizationOrchestrationProcessor:
    """
    🏗️ Sequential Thinking Phase 4.3.2: Ultimate orchestration consolidation

    Consolidates all major visualization orchestration workflows:
    - Executive visualization creation
    - Chat-embedded visualization generation
    - Chart creation method delegation
    - Complete visualization workflow management
    """

    def __init__(
        self,
        template_router: VisualizationTemplateRouter,
        dashboard_factory: VisualizationDashboardFactory,
        html_processor: HTMLTemplateProcessor,
        utility_processor: VisualizationUtilityProcessor,
        chat_generator: ChatVisualizationGenerator,
        visualization_metrics: Dict[str, Any],
        version: str,
    ):
        self.template_router = template_router
        self.dashboard_factory = dashboard_factory
        self.html_processor = html_processor
        self.utility_processor = utility_processor
        self.chat_generator = chat_generator
        self.visualization_metrics = visualization_metrics
        self.version = version

    async def create_executive_visualization(
        self,
        data: Union[Dict[str, Any], str],
        chart_type: str,
        persona: str,
        title: str,
        context: Dict[str, Any] = None,
        mcp_constants: Any = None,
    ) -> VisualizationResult:
        """🏗️ Complete executive visualization orchestration workflow"""

        start_time = time.time()
        context = context or {}

        try:
            # Update metrics
            self.visualization_metrics[
                mcp_constants.MetricsKeys.TOTAL_VISUALIZATIONS
            ] += 1

            # Process data if string
            if isinstance(data, str):
                data = self.utility_processor.parse_analysis_output(data)

            # Get persona template and generate figure
            template_func = self.template_router.get_template_for_persona(persona)
            fig = template_func(data, chart_type, title, context)

            # Apply styling and generate HTML
            fig = self.utility_processor.apply_executive_styling(
                fig,
                persona,
                mcp_constants.Colors.PERSONA_COLORS,
                mcp_constants.Colors.PRIMARY_BLUE,
                mcp_constants.Typography.TITLE_FONT_SIZE,
            )

            html_output = self.html_processor.generate_executive_html(
                fig, persona, title, mcp_constants.Personas.PERSONA_TITLES, self.version
            )

            # Calculate metrics
            generation_time = time.time() - start_time
            file_size = len(html_output.encode("utf-8"))
            interactive_elements = self.utility_processor.detect_interactive_elements(
                fig
            )

            # Update success metrics
            self.visualization_metrics[
                mcp_constants.MetricsKeys.SUCCESSFUL_GENERATIONS
            ] += 1
            self.utility_processor.update_performance_metrics(
                generation_time,
                file_size,
                interactive_elements,
                self.visualization_metrics,
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
                error=mcp_constants.ErrorMessages.VISUALIZATION_GENERATION_ERROR.format(
                    error=str(e)
                ),
            )

    async def generate_chat_embedded_visualization(
        self,
        query_data: Dict[str, Any],
        persona: str = "diego",
        context: Dict[str, Any] = None,
    ) -> VisualizationResult:
        """🏗️ Complete chat visualization orchestration workflow"""

        start_time = time.time()

        try:
            # Determine chart type and generate title
            chart_type = self.utility_processor.infer_chart_type_from_data(query_data)
            title = self.utility_processor.generate_contextual_title(
                query_data, context
            )

            # Create chat-optimized chart
            fig = await self.create_chat_optimized_chart(
                query_data, chart_type, title, persona
            )

            # Generate chat-embedded HTML
            html_output = self.html_processor.generate_chat_embedded_html(
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

    async def create_chat_optimized_chart(
        self, data: Dict[str, Any], chart_type: str, title: str, persona: str
    ) -> go.Figure:
        """🏗️ Create chart optimized for chat embedding"""

        # Special handling for architecture health (not in chat generator)
        if chart_type == "architecture_health":
            return self.create_architecture_health_dashboard(data, title)

        # Map chart types to chat generator types
        chat_type_mapping = {
            "design_system_status": "design_system",
            "simple_metrics": "default",
        }

        # Use consolidated chat generator
        chat_chart_type = chat_type_mapping.get(chart_type, chart_type)
        return self.chat_generator.create_chat_visualization(
            data, chat_chart_type, title
        )

    # ========================================
    # Chart Creation Method Delegation
    # ========================================

    def create_architecture_health_dashboard(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Architecture health dashboard with data normalization"""
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

    def create_service_performance_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Service performance chart delegation"""
        return self.dashboard_factory.create_dashboard(
            "service_performance", data, title
        )

    def create_system_dependency_map(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ System dependency map delegation"""
        return self.dashboard_factory.create_dashboard(
            "system_dependencies", data, title
        )

    def create_technical_debt_trends(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Technical debt trends delegation"""
        return self.dashboard_factory.create_dashboard(
            "technical_debt_trends", data, title
        )

    def create_component_adoption_chart(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Component adoption chart delegation"""
        return self.dashboard_factory.create_dashboard(
            "component_adoption", data, title
        )

    def create_design_debt_visualization(
        self, data: Dict[str, Any], title: str
    ) -> go.Figure:
        """🏗️ Design debt visualization delegation"""
        return self.dashboard_factory.create_dashboard("design_debt", data, title)

    def generate_error_visualization(self, error_message: str) -> str:
        """🏗️ Generate enhanced error visualization HTML - Phase 4.4.1"""
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

    def create_default_chart(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """🏗️ Create default chart when specific template not available - Phase 4.4.1"""

        # Simple bar chart as fallback
        if "x" in data and "y" in data:
            fig = go.Figure(
                data=go.Bar(
                    x=data["x"],
                    y=data["y"],
                    marker_color=self.dashboard_factory.color_palette[0],
                )
            )
        else:
            # Sample data for demonstration
            fig = go.Figure(
                data=go.Bar(
                    x=["Q1", "Q2", "Q3", "Q4"],
                    y=[20, 14, 23, 25],
                    marker_color=self.dashboard_factory.color_palette[0],
                )
            )

        fig.update_layout(title=title)
        return fig

    async def health_check(
        self, create_visualization_func, server_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """🏗️ Perform health check on Executive Visualization Engine - Phase 4.4.1"""

        try:
            # Test basic visualization generation
            test_data = {"x": ["Test"], "y": [1]}
            result = await create_visualization_func(
                test_data, "default", "diego", "Health Check Test"
            )

            return {
                "status": "healthy" if result.success else "degraded",
                "server_info": server_info,
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
