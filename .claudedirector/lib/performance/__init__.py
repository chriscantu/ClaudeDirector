"""
Performance Optimization Module

Phase 8 enterprise-grade performance optimizations for ClaudeDirector.
Implements <500ms response times with <50MB memory usage.
"""

from .cache_manager import CacheManager
from .memory_optimizer import MemoryOptimizer
from .performance_monitor import PerformanceMonitor

# TS-4: Import unified response handler (eliminates 298+ lines of duplicate response patterns)
from .unified_response_handler import (
    UnifiedResponseHandler,
    UnifiedResponse,
    ResponseStatus,
    ResponseType,
    get_unified_response_handler,
    create_mcp_response,
    create_persona_response,
    create_fallback_response,
    create_conversational_response,
    create_ml_response,
    create_data_response,
    create_systematic_response,
)

# Import unified performance manager for legacy compatibility
try:
    from ..core.unified_performance_manager import create_response_optimizer

    ResponseOptimizer = create_response_optimizer
except ImportError:
    # Fallback if unified performance manager not available
    class ResponseOptimizer:
        def __init__(self, *args, **kwargs):
            pass


__all__ = [
    "CacheManager",
    "MemoryOptimizer",
    "ResponseOptimizer",
    "PerformanceMonitor",
    # TS-4: Unified Response Handler exports
    "UnifiedResponseHandler",
    "UnifiedResponse",
    "ResponseStatus",
    "ResponseType",
    "get_unified_response_handler",
    "create_mcp_response",
    "create_persona_response",
    "create_fallback_response",
    "create_conversational_response",
    "create_ml_response",
    "create_data_response",
    "create_systematic_response",
]
