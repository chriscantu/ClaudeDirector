"""
Performance Optimization Module

Phase 8 enterprise-grade performance optimizations for ClaudeDirector.
Implements <500ms response times with <50MB memory usage.
"""

from .cache_manager import CacheManager
from .memory_optimizer import MemoryOptimizer
from .performance_monitor import PerformanceMonitor

# PHASE 8.4: Import unified response functionality from consolidated manager
from ..core.unified_data_performance_manager import (
    UnifiedResponse,
    ResponseStatus,
    ResponseType,
    get_unified_manager,
    create_mcp_response,
    create_persona_response,
    create_fallback_response,
    create_conversational_response,
)

# Legacy compatibility aliases
UnifiedResponseHandler = get_unified_manager
get_unified_response_handler = get_unified_manager


# Additional response creation functions for backward compatibility
async def create_ml_response(
    content: str, confidence: float = 0.0, **kwargs
) -> UnifiedResponse:
    """Create ML prediction response (legacy compatibility)"""
    manager = get_unified_manager()
    return await manager.create_response(
        content=content,
        response_type=ResponseType.ML_PREDICTION,
        confidence=confidence,
        **kwargs,
    )


async def create_data_response(content: str, **kwargs) -> UnifiedResponse:
    """Create data query response (legacy compatibility)"""
    manager = get_unified_manager()
    return await manager.create_response(
        content=content, response_type=ResponseType.DATA_QUERY, **kwargs
    )


async def create_systematic_response(
    content: str, frameworks: list = None, **kwargs
) -> UnifiedResponse:
    """Create systematic analysis response (legacy compatibility)"""
    manager = get_unified_manager()
    return await manager.create_response(
        content=content,
        response_type=ResponseType.SYSTEMATIC_ANALYSIS,
        frameworks_detected=frameworks or [],
        **kwargs,
    )


# Import unified performance manager for legacy compatibility
try:
    from ..core.unified_data_performance_manager import create_response_optimizer

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
    # PHASE 8.4: Unified Response functionality (consolidated from unified_response_handler.py)
    "UnifiedResponseHandler",
    "UnifiedResponse",
    "ResponseStatus",
    "ResponseType",
    "get_unified_response_handler",
    "get_unified_manager",
    "create_mcp_response",
    "create_persona_response",
    "create_fallback_response",
    "create_conversational_response",
    "create_ml_response",
    "create_data_response",
    "create_systematic_response",
]
