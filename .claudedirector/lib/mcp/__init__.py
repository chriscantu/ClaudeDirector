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
]
