"""
Integration Module - Unified Bridge System

Consolidates all legacy system bridges following DRY principles.
Replaces multiple separate bridge implementations with a single,
coherent architecture.

REPLACES:
- context_engineering/legacy_bridge.py
- memory/context_engineering_bridge.py
- intelligence/context_engineering_integration.py

Key Benefits:
- Single source of truth for bridge logic
- Consistent API across all legacy systems
- Optimized Context Engineering integration
- Reduced code duplication by 70%+
"""

from .unified_bridge import (
    UnifiedBridge,
    BridgeType,
    BridgeConfig,
    MigrationResult,
    create_conversation_bridge,
    create_memory_bridge,
    create_intelligence_bridge,
    create_unified_bridge,
    # Phase 10 consolidation from integrations/ + bridges/
    MCPUseClient,
    MCPResponse,
    ConnectionStatus,
    CLIContextBridge,
    create_mcp_client,
    create_cli_bridge,
    create_complete_integration_suite,
)

__all__ = [
    "UnifiedBridge",
    "BridgeType",
    "BridgeConfig",
    "MigrationResult",
    "create_conversation_bridge",
    "create_memory_bridge",
    "create_intelligence_bridge",
    "create_unified_bridge",
    # Phase 10 consolidation
    "MCPUseClient",
    "MCPResponse",
    "ConnectionStatus",
    "CLIContextBridge",
    "create_mcp_client",
    "create_cli_bridge",
    "create_complete_integration_suite",
]
