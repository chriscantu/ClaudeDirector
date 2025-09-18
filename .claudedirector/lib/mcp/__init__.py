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

# 🚀 ENHANCEMENT FIX: Make executive visualization optional due to plotly dependency
try:
    from .executive_visualization_server import (
        ExecutiveVisualizationEngine,
        ExecutiveVisualizationMCPServer,
        VisualizationResult,
        create_executive_visualization_server,
    )

    EXECUTIVE_VISUALIZATION_AVAILABLE = True
except ImportError:
    # Create fallback classes if plotly not available
    class ExecutiveVisualizationEngine:
        def __init__(self):
            pass

    class ExecutiveVisualizationMCPServer:
        def __init__(self):
            pass

    class VisualizationResult:
        def __init__(self):
            pass

    def create_executive_visualization_server():
        return ExecutiveVisualizationMCPServer()

    EXECUTIVE_VISUALIZATION_AVAILABLE = False
# 🚀 ENHANCEMENT FIX: Make integrated visualization optional due to dependency chain
try:
    from .integrated_visualization_workflow import (
        IntegratedVisualizationWorkflow,
        IntegratedWorkflowResult,
        create_integrated_visualization_workflow,
    )

    INTEGRATED_VISUALIZATION_AVAILABLE = True
except ImportError:
    # Create fallback classes if dependencies not available
    class IntegratedVisualizationWorkflow:
        def __init__(self):
            pass

    class IntegratedWorkflowResult:
        def __init__(self):
            pass

    def create_integrated_visualization_workflow():
        return IntegratedVisualizationWorkflow()

    INTEGRATED_VISUALIZATION_AVAILABLE = False

# Phase 7 Week 2: Conversational Analytics - Make optional
try:
    from .conversational_data_manager import (
        ConversationalDataManager,
        ConversationalQuery,
        DataResponse,
        QueryType,
        create_conversational_data_manager,
    )

    CONVERSATIONAL_DATA_AVAILABLE = True
except ImportError:
    # Create fallback classes
    class ConversationalDataManager:
        pass

    class ConversationalQuery:
        pass

    class DataResponse:
        pass

    class QueryType:
        pass

    def create_conversational_data_manager():
        return ConversationalDataManager()

    CONVERSATIONAL_DATA_AVAILABLE = False

try:
    from .conversational_analytics_workflow import (
        ConversationalAnalyticsWorkflow,
        ConversationalAnalyticsResult,
        create_conversational_analytics_workflow,
    )

    CONVERSATIONAL_ANALYTICS_AVAILABLE = True
except ImportError:
    # Create fallback classes
    class ConversationalAnalyticsWorkflow:
        pass

    class ConversationalAnalyticsResult:
        pass

    def create_conversational_analytics_workflow():
        return ConversationalAnalyticsWorkflow()

    CONVERSATIONAL_ANALYTICS_AVAILABLE = False

# Phase 7 Week 3: MCP Integration
from .mcp_integration_manager import (
    MCPIntegrationManager,
    MCPServerType,
    MCPServerStatus,
    MCPIntegrationResult,
    create_mcp_integration_manager,
)

# Phase 7 Week 4: Interactive Enhancement System (DRY Compliant) - Make optional
try:
    from .interactive_enhancement_addon import (
        InteractiveEnhancementAddon,
        InteractiveEnhancementResult,
        create_interactive_enhancement_addon,
    )

    INTERACTIVE_ENHANCEMENT_AVAILABLE = True
except ImportError:
    # Create fallback classes
    class InteractiveEnhancementAddon:
        pass

    class InteractiveEnhancementResult:
        pass

    def create_interactive_enhancement_addon():
        return InteractiveEnhancementAddon()

    INTERACTIVE_ENHANCEMENT_AVAILABLE = False

# Phase 7B: Chat Integration (Configuration-Driven, DRY Compliant) - Make optional
try:
    from .conversational_interaction_manager import (
        ConversationalInteractionManager,
        create_conversational_interaction_manager,
        InteractionIntent,
        QueryIntent,
        InteractionResponse,
    )

    CONVERSATIONAL_INTERACTION_AVAILABLE = True
except ImportError:
    # Create fallback classes
    class ConversationalInteractionManager:
        pass

    class InteractionIntent:
        pass

    class QueryIntent:
        pass

    class InteractionResponse:
        pass

    def create_conversational_interaction_manager():
        return ConversationalInteractionManager()

    CONVERSATIONAL_INTERACTION_AVAILABLE = False

try:
    from .chat_context_manager import (
        ChatContextManager,
        create_chat_context_manager,
        ChartContextState,
        ConversationContext,
        ContextScope,
    )

    CHAT_CONTEXT_AVAILABLE = True
except ImportError:
    # Create fallback classes
    class ChatContextManager:
        pass

    class ChartContextState:
        pass

    class ConversationContext:
        pass

    class ContextScope:
        pass

    def create_chat_context_manager():
        return ChatContextManager()

    CHAT_CONTEXT_AVAILABLE = False

# Phase 7C: Advanced Features (Configuration-Driven, DRY & SOLID Compliant) - Make optional
try:
    from .cross_chart_linking_engine import (
        CrossChartLinkingEngine,
        create_cross_chart_linking_engine,
        LinkType,
        LinkageConfig,
        ChartUpdate,
    )

    CROSS_CHART_LINKING_AVAILABLE = True
except ImportError:
    # Create fallback classes
    class CrossChartLinkingEngine:
        pass

    class LinkType:
        pass

    class LinkageConfig:
        pass

    class ChartUpdate:
        pass

    def create_cross_chart_linking_engine():
        return CrossChartLinkingEngine()

    CROSS_CHART_LINKING_AVAILABLE = False

try:
    from .drilldown_navigation_engine import (
        DrillDownNavigationEngine,
        create_drilldown_navigation_engine,
        NavigationType,
        HierarchyMap,
        NavigationResult,
    )

    DRILLDOWN_NAVIGATION_AVAILABLE = True
except ImportError:
    # Create fallback classes
    class DrillDownNavigationEngine:
        pass

    class NavigationType:
        pass

    class HierarchyMap:
        pass

    class NavigationResult:
        pass

    def create_drilldown_navigation_engine():
        return DrillDownNavigationEngine()

    DRILLDOWN_NAVIGATION_AVAILABLE = False

# Phase 7 Week 4: Deprecated components removed due to DRY violations
# Use InteractiveEnhancementAddon which extends existing systems without duplication

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
    # Phase 7B: Chat Integration (Configuration-Driven, DRY Compliant)
    "ConversationalInteractionManager",
    "create_conversational_interaction_manager",
    "InteractionIntent",
    "QueryIntent",
    "InteractionResponse",
    "ChatContextManager",
    "create_chat_context_manager",
    "ChartContextState",
    "ConversationContext",
    "ContextScope",
    # Phase 7C: Advanced Features (Configuration-Driven, DRY & SOLID Compliant)
    "CrossChartLinkingEngine",
    "create_cross_chart_linking_engine",
    "LinkType",
    "LinkageConfig",
    "ChartUpdate",
    "DrillDownNavigationEngine",
    "create_drilldown_navigation_engine",
    "NavigationType",
    "HierarchyMap",
    "NavigationResult",
]
