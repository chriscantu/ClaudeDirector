# MCP Server Infrastructure
# Strategic Python MCP Server and Executive Visualization System

from .constants import MCPServerConstants
from .strategic_python_server import StrategicPythonMCPServer, ExecutionResult
from .mcp_integration import (
    StrategicPythonMCPIntegration,
    MCPRequest,
    MCPResponse,
    create_strategic_python_integration,
    StrategicPythonMCPContext,
)
from .executive_visualization_server import (
    ExecutiveVisualizationEngine,
    ExecutiveVisualizationMCPServer,
    VisualizationResult,
    create_executive_visualization_server,
)
from .integrated_visualization_workflow import (
    IntegratedVisualizationWorkflow,
    IntegratedWorkflowResult,
    create_integrated_visualization_workflow,
)

# Phase 7 Week 2: Conversational Analytics
from .conversational_data_manager import (
    ConversationalDataManager,
    ConversationalQuery,
    DataResponse,
    QueryType,
    create_conversational_data_manager,
)
from .conversational_analytics_workflow import (
    ConversationalAnalyticsWorkflow,
    ConversationalAnalyticsResult,
    create_conversational_analytics_workflow,
)

# Phase 7 Week 3: MCP Integration
from .mcp_integration_manager import (
    MCPIntegrationManager,
    MCPServerType,
    MCPServerStatus,
    MCPIntegrationResult,
    create_mcp_integration_manager,
)

# Phase 7 Week 4: Interactive Enhancement System (DRY Compliant)
from .interactive_enhancement_addon import (
    InteractiveEnhancementAddon,
    InteractiveEnhancementResult,
    create_interactive_enhancement_addon,
)

# DEPRECATED: Phase 7 Week 4 Components (DRY Violations - Remove Next Session)
# These components duplicate existing ExecutiveVisualizationEngine functionality
# and violate DRY principles. Use InteractiveEnhancementAddon instead.
try:
    from .interactive_chart_engine import (
        InteractiveChartEngine,
        InteractionType,
        InteractionEvent,
        InteractionResult,
        create_interactive_chart_engine,
    )
    from .chart_interaction_types import (
        ChartInteractionTypes,
        DrillDownLevel,
        FilterState,
        create_chart_interaction_types,
    )
    from .chat_embedded_interactivity import (
        ChatEmbeddedInteractivity,
        ChatEmbeddedResult,
        create_chat_embedded_interactivity,
    )
    from .integrated_interactive_visualization import (
        IntegratedInteractiveVisualization,
        IntegratedInteractiveResult,
        create_integrated_interactive_visualization,
    )

    # Issue deprecation warning
    import warnings

    warnings.warn(
        "Interactive Chart Engine components are DEPRECATED due to DRY violations. "
        "Use InteractiveEnhancementAddon which extends existing systems without duplication.",
        DeprecationWarning,
        stacklevel=2,
    )
except ImportError:
    # Components will be removed in next session
    pass

__all__ = [
    "MCPServerConstants",
    "StrategicPythonMCPServer",
    "ExecutionResult",
    "StrategicPythonMCPIntegration",
    "MCPRequest",
    "MCPResponse",
    "create_strategic_python_integration",
    "StrategicPythonMCPContext",
    "ExecutiveVisualizationEngine",
    "ExecutiveVisualizationMCPServer",
    "VisualizationResult",
    "create_executive_visualization_server",
    "IntegratedVisualizationWorkflow",
    "IntegratedWorkflowResult",
    "create_integrated_visualization_workflow",
    # Phase 7 Week 2: Conversational Analytics
    "ConversationalDataManager",
    "ConversationalQuery",
    "DataResponse",
    "QueryType",
    "create_conversational_data_manager",
    "ConversationalAnalyticsWorkflow",
    "ConversationalAnalyticsResult",
    "create_conversational_analytics_workflow",
    # Phase 7 Week 3: MCP Integration
    "MCPIntegrationManager",
    "MCPServerType",
    "MCPServerStatus",
    "MCPIntegrationResult",
    "create_mcp_integration_manager",
    # Phase 7 Week 4: Interactive Enhancement System (DRY Compliant)
    "InteractiveEnhancementAddon",
    "InteractiveEnhancementResult",
    "create_interactive_enhancement_addon",
    # DEPRECATED: Phase 7 Week 4 Original Components (DRY Violations)
    "InteractiveChartEngine",  # DEPRECATED - Use InteractiveEnhancementAddon
    "InteractionType",  # DEPRECATED
    "InteractionEvent",  # DEPRECATED
    "InteractionResult",  # DEPRECATED
    "create_interactive_chart_engine",  # DEPRECATED
    "ChartInteractionTypes",  # DEPRECATED
    "DrillDownLevel",  # DEPRECATED
    "FilterState",  # DEPRECATED
    "create_chart_interaction_types",  # DEPRECATED
    "ChatEmbeddedInteractivity",  # DEPRECATED
    "ChatEmbeddedResult",  # DEPRECATED
    "create_chat_embedded_interactivity",  # DEPRECATED
    "IntegratedInteractiveVisualization",  # DEPRECATED
    "IntegratedInteractiveResult",  # DEPRECATED
    "create_integrated_interactive_visualization",  # DEPRECATED
]
