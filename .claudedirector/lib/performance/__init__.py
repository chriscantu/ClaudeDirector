"""
Performance Optimization Module

Phase 8 enterprise-grade performance optimizations for ClaudeDirector.
Implements <500ms response times with <50MB memory usage.
"""

from .cache_manager import CacheManager
from .memory_optimizer import MemoryOptimizer
from .performance_monitor import PerformanceMonitor

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
]
