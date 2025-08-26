"""
ClaudeDirector Memory Management Module

This module provides strategic memory and data persistence capabilities
for the ClaudeDirector AI framework.

Components:
- Memory Manager: Core memory operations and persistence
- Stakeholder Intelligence: AI-powered stakeholder detection and engagement
- Meeting Intelligence: Meeting analysis and strategic insights
- Architecture Health Monitor: Platform architecture monitoring
- Workspace Monitor: Development environment monitoring
"""

from .memory_manager import StrategicMemoryManager
from .optimized_db_manager import OptimizedSQLiteManager

# Import unified bridge system (replaces context_engineering_bridge)
try:
    from ..integration.unified_bridge import create_memory_bridge

    UNIFIED_BRIDGE_AVAILABLE = True
except ImportError:
    UNIFIED_BRIDGE_AVAILABLE = False

    def create_memory_bridge(*args, **kwargs):
        raise ImportError("Unified bridge system not available")


# MIGRATION NOTICE: memory/ modules are being migrated to Context Engineering
# Bridge functionality now provided by integration.unified_bridge
# See MIGRATION_NOTICE.md for details and migration path

__all__ = [
    "StrategicMemoryManager",
    "OptimizedSQLiteManager",
    "create_memory_bridge",  # Now from unified bridge
]
