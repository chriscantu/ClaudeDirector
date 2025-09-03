#!/usr/bin/env python3
"""
Executive Visualization Engine Factory - Sequential Thinking Phase 4.4.2
🏗️ Martin | Platform Architecture - Ultra-aggressive facade transformation

Consolidates all engine initialization complexity for maximum facade simplification.
This factory handles all processor instantiation and configuration setup.
"""

import logging
from typing import Dict, Any

from .visualization_template_router import VisualizationTemplateRouter
from .chat_visualization_generator import ChatVisualizationGenerator
from .visualization_dashboard_factory import VisualizationDashboardFactory
from .html_template_processor import HTMLTemplateProcessor
from .visualization_utility_processor import VisualizationUtilityProcessor
from .visualization_orchestration_processor import VisualizationOrchestrationProcessor
from .constants import MCPServerConstants

logger = logging.getLogger(__name__)


class ExecutiveVisualizationEngineFactory:
    """
    🏗️ Sequential Thinking Phase 4.4.2: Complete initialization consolidation

    Consolidates all engine initialization complexity:
    - Processor instantiation and configuration
    - Dependencies setup and wiring
    - Performance metrics initialization
    - Capabilities and configuration setup
    """

    @staticmethod
    def create_engine_components() -> Dict[str, Any]:
        """Create and configure all engine components and dependencies"""

        # Basic configuration
        name = MCPServerConstants.EXECUTIVE_VISUALIZATION_SERVER_NAME
        version = MCPServerConstants.EXECUTIVE_VISUALIZATION_SERVER_VERSION
        color_palette = MCPServerConstants.Colors.EXECUTIVE_PALETTE
        layout_template = MCPServerConstants.get_executive_layout_template()

        # Capabilities configuration
        capabilities = [
            MCPServerConstants.Capabilities.EXECUTIVE_DASHBOARDS,
            MCPServerConstants.Capabilities.INTERACTIVE_CHARTS,
            MCPServerConstants.Capabilities.STRATEGIC_PRESENTATIONS,
            MCPServerConstants.Capabilities.PUBLICATION_QUALITY_VISUALS,
        ]

        # Performance metrics initialization
        visualization_metrics = {
            MCPServerConstants.MetricsKeys.TOTAL_VISUALIZATIONS: 0,
            MCPServerConstants.MetricsKeys.SUCCESSFUL_GENERATIONS: 0,
            MCPServerConstants.MetricsKeys.AVG_GENERATION_TIME: 0.0,
            MCPServerConstants.MetricsKeys.AVG_FILE_SIZE: 0,
            MCPServerConstants.MetricsKeys.INTERACTIVE_FEATURES_USED: 0,
        }

        return {
            "name": name,
            "version": version,
            "color_palette": color_palette,
            "layout_template": layout_template,
            "capabilities": capabilities,
            "visualization_metrics": visualization_metrics,
        }

    @staticmethod
    def create_processors(components: Dict[str, Any]) -> Dict[str, Any]:
        """Create and wire all visualization processors"""

        # Extract components
        color_palette = components["color_palette"]
        layout_template = components["layout_template"]
        visualization_metrics = components["visualization_metrics"]
        version = components["version"]

        # Create template router (requires engine reference - will be set later)
        template_router = None  # Placeholder

        # Create chat visualization generator
        chat_generator = ChatVisualizationGenerator(color_palette, layout_template)

        # Create dashboard factory
        dashboard_factory = VisualizationDashboardFactory(color_palette)

        # Create HTML template processor
        html_processor = HTMLTemplateProcessor()

        # Create utility processor
        utility_processor = VisualizationUtilityProcessor(
            color_palette, layout_template, visualization_metrics
        )

        return {
            "template_router": template_router,
            "chat_generator": chat_generator,
            "dashboard_factory": dashboard_factory,
            "html_processor": html_processor,
            "utility_processor": utility_processor,
        }

    @staticmethod
    def create_orchestration_processor(
        processors: Dict[str, Any], components: Dict[str, Any]
    ) -> VisualizationOrchestrationProcessor:
        """Create the main orchestration processor with all dependencies"""

        return VisualizationOrchestrationProcessor(
            processors["template_router"],
            processors["dashboard_factory"],
            processors["html_processor"],
            processors["utility_processor"],
            processors["chat_generator"],
            components["visualization_metrics"],
            components["version"],
        )

    @classmethod
    def initialize_engine(cls, engine_instance):
        """🏗️ Complete engine initialization using factory pattern"""

        # Create all components
        components = cls.create_engine_components()

        # Set basic properties
        engine_instance.name = components["name"]
        engine_instance.version = components["version"]
        engine_instance.color_palette = components["color_palette"]
        engine_instance.layout_template = components["layout_template"]
        engine_instance.capabilities = components["capabilities"]
        engine_instance.visualization_metrics = components["visualization_metrics"]

        # Create processors
        processors = cls.create_processors(components)

        # Set template router with engine reference
        processors["template_router"] = VisualizationTemplateRouter(engine_instance)

        # Set individual processors
        engine_instance.template_router = processors["template_router"]
        engine_instance.chat_generator = processors["chat_generator"]
        engine_instance.dashboard_factory = processors["dashboard_factory"]
        engine_instance.html_processor = processors["html_processor"]
        engine_instance.utility_processor = processors["utility_processor"]

        # Create orchestration processor with all dependencies
        engine_instance.orchestration_processor = cls.create_orchestration_processor(
            processors, components
        )

        # Legacy integration placeholder
        engine_instance.strategic_python_server = None

        logger.info(
            f"Executive Visualization Engine {components['version']} initialized via factory"
        )
