"""
Memory Optimizer for Phase 8 Performance

Implements <50MB memory usage with object pooling and efficient resource management.
Refactored to inherit from BaseManager for DRY compliance.
"""

import gc
import time
import weakref
from typing import Dict, Any, Optional, List, Type, TypeVar, Generic
from dataclasses import dataclass
from collections import defaultdict
import logging
import threading
from pathlib import Path
import sys

# Import BaseManager infrastructure
try:
    from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from ..core.manager_factory import register_manager_type
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from core.manager_factory import register_manager_type


T = TypeVar("T")


@dataclass
class MemoryStats:
    """Memory usage statistics"""

    current_usage_mb: float
    peak_usage_mb: float
    object_pool_size: int
    cache_memory_mb: float
    garbage_collections: int
    last_gc_time: float
    memory_efficiency: float  # Objects reused / total objects created


class ObjectPool(Generic[T]):
    """
    High-performance object pool for expensive-to-create objects

    Reduces memory allocation overhead and garbage collection pressure
    """

    def __init__(self, factory_func, max_size: int = 100):
        self.factory_func = factory_func
        self.max_size = max_size
        self.pool: List[T] = []
        self.created_count = 0
        self.reused_count = 0
        self._lock = threading.Lock()

    def acquire(self) -> T:
        """Get object from pool or create new one"""
        with self._lock:
            if self.pool:
                obj = self.pool.pop()
                self.reused_count += 1
                return obj
            else:
                obj = self.factory_func()
                self.created_count += 1
                return obj

    def release(self, obj: T):
        """Return object to pool for reuse"""
        with self._lock:
            if len(self.pool) < self.max_size:
                # Reset object state if it has a reset method
                if hasattr(obj, "reset"):
                    obj.reset()
                self.pool.append(obj)

    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics"""
        total_requests = self.created_count + self.reused_count
        reuse_rate = (self.reused_count / total_requests) if total_requests > 0 else 0

        return {
            "pool_size": len(self.pool),
            "created_count": self.created_count,
            "reused_count": self.reused_count,
            "reuse_rate": reuse_rate,
            "max_size": self.max_size,
        }


class MemoryOptimizer(BaseManager):
    """
    Enterprise-grade memory optimization for ClaudeDirector

    Features:
    - Object pooling for expensive objects
    - Intelligent garbage collection scheduling
    - Memory usage monitoring and alerting
    - Automatic memory pressure relief
    - <50MB target memory usage

    Refactored to inherit from BaseManager for DRY compliance.
    Eliminates duplicate logging, metrics, and configuration patterns.
    """

    def __init__(
        self,
        config: Optional[BaseManagerConfig] = None,
        target_memory_mb: int = 40,
        alert_threshold_mb: int = 45,
        cache: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        if config is None:
            config = BaseManagerConfig(
                manager_name="memory_optimizer",
                manager_type=ManagerType.MEMORY,
                enable_metrics=True,
                enable_caching=True,
                enable_logging=True,
                performance_tracking=True,
                custom_config={
                    "target_memory_mb": target_memory_mb,
                    "alert_threshold_mb": alert_threshold_mb,
                },
            )

        super().__init__(config, cache, metrics, logger_name="MemoryOptimizer")

        # Get configuration values from BaseManager config
        self.target_memory_mb = self.config.custom_config.get(
            "target_memory_mb", target_memory_mb
        )
        self.alert_threshold_mb = self.config.custom_config.get(
            "alert_threshold_mb", alert_threshold_mb
        )

        # Object pools for common expensive objects
        self.pools: Dict[str, ObjectPool] = {}

        # Memory tracking
        self.peak_memory_mb = 0
        self.gc_count = 0
        self.last_gc_time = 0
        self.memory_alerts = 0

        # Weak references to track object lifecycle
        self.tracked_objects = weakref.WeakSet()

        # Performance counters
        self.objects_pooled = 0
        self.objects_reused = 0

        # Initialize garbage collection optimization
        self._optimize_gc_settings()

    def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        Implement BaseManager abstract method for memory optimization operations
        """
        start_time = time.time()

        try:
            if operation == "create_pool":
                result = self.create_object_pool(*args, **kwargs)
            elif operation == "get_pool":
                result = self.get_pool(*args, **kwargs)
            elif operation == "force_gc":
                result = self.force_gc(*args, **kwargs)
            elif operation == "get_memory_usage":
                result = self.get_memory_usage()
            elif operation == "get_stats":
                result = self.get_stats()
            elif operation == "cleanup_memory":
                result = self.cleanup_memory()
            elif operation == "optimize_memory":
                result = self.optimize_memory()
            else:
                raise ValueError(f"Unknown memory optimizer operation: {operation}")

            duration = time.time() - start_time
            self._update_metrics(operation, duration, True)

            return result

        except Exception as e:
            duration = time.time() - start_time
            self._update_metrics(operation, duration, False)

            self.logger.error(
                "Memory optimizer operation failed",
                operation=operation,
                error=str(e),
                args=args,
                kwargs=kwargs,
            )
            raise

    def _optimize_gc_settings(self):
        """Optimize garbage collection for performance"""
        # Adjust GC thresholds for better performance
        # More objects before gen0 collection, fewer for gen1/gen2
        gc.set_threshold(1000, 15, 15)

        # Enable automatic garbage collection
        gc.enable()

        self.logger.info("Garbage collection optimized for performance")

    def create_object_pool(
        self, pool_name: str, factory_func, max_size: int = 100
    ) -> ObjectPool:
        """Create a new object pool"""
        pool = ObjectPool(factory_func, max_size)
        self.pools[pool_name] = pool
        self.logger.debug(f"Created object pool '{pool_name}' with max_size={max_size}")
        return pool

    def get_pool(self, pool_name: str) -> Optional[ObjectPool]:
        """Get existing object pool"""
        return self.pools.get(pool_name)

    def track_object(self, obj: Any, category: str = "general"):
        """Track object for memory monitoring"""
        self.tracked_objects.add(obj)
        # Could add category-specific tracking here if needed

    def force_gc(self, generation: Optional[int] = None) -> int:
        """Force garbage collection and return collected objects count"""
        start_time = time.time()

        if generation is not None:
            collected = gc.collect(generation)
        else:
            collected = gc.collect()

        gc_time = (time.time() - start_time) * 1000
        self.gc_count += 1
        self.last_gc_time = time.time()

        if gc_time > 100:  # Log slow GC
            self.logger.warning(
                f"Slow garbage collection: {gc_time:.1f}ms, collected {collected} objects"
            )
        else:
            self.logger.debug(
                f"Garbage collection: {gc_time:.1f}ms, collected {collected} objects"
            )

        return collected

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB (requires psutil for accurate measurement)"""
        try:
            import psutil
            import os

            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024

            # Update peak memory tracking
            if memory_mb > self.peak_memory_mb:
                self.peak_memory_mb = memory_mb

            return memory_mb
        except ImportError:
            # Fallback estimation without psutil
            return self._estimate_memory_usage()

    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage without psutil"""
        # Simple estimation based on tracked objects and GC stats
        base_usage = 20  # Base Python interpreter usage

        # Estimate from object pools
        pool_usage = sum(
            len(pool.pool) * 0.1 for pool in self.pools.values()
        )  # 0.1MB per pooled object estimate

        # Estimate from tracked objects
        tracked_usage = (
            len(self.tracked_objects) * 0.01
        )  # 10KB per tracked object estimate

        return base_usage + pool_usage + tracked_usage

    def check_memory_pressure(self) -> bool:
        """Check if memory usage is above threshold"""
        current_usage = self.get_memory_usage()

        if current_usage > self.alert_threshold_mb:
            self.memory_alerts += 1
            self.logger.warning(
                f"Memory usage alert: {current_usage:.1f}MB (threshold: {self.alert_threshold_mb}MB)"
            )
            return True

        return False

    def memory_pressure_relief(self):
        """Perform memory pressure relief operations"""
        self.logger.info("Performing memory pressure relief...")

        # Clear object pools (keep some capacity)
        for pool_name, pool in self.pools.items():
            if len(pool.pool) > 10:
                # Clear 70% of pooled objects
                clear_count = int(len(pool.pool) * 0.7)
                for _ in range(clear_count):
                    pool.pool.pop()
                self.logger.debug(
                    f"Cleared {clear_count} objects from pool '{pool_name}'"
                )

        # Force garbage collection
        collected = self.force_gc()

        # Log results
        current_usage = self.get_memory_usage()
        self.logger.info(
            f"Memory pressure relief complete: {current_usage:.1f}MB, collected {collected} objects"
        )

    def optimize_for_performance(self):
        """Perform performance-focused memory optimizations"""
        # Aggressive garbage collection of generation 0 and 1
        gc.collect(0)
        gc.collect(1)

        # Check if we need more aggressive cleanup
        if self.check_memory_pressure():
            self.memory_pressure_relief()

    def get_memory_stats(self) -> MemoryStats:
        """Get comprehensive memory statistics"""
        current_usage = self.get_memory_usage()

        # Calculate object pool stats
        total_pool_size = sum(len(pool.pool) for pool in self.pools.values())

        # Calculate efficiency metrics
        total_objects_created = sum(pool.created_count for pool in self.pools.values())
        total_objects_reused = sum(pool.reused_count for pool in self.pools.values())
        total_requests = total_objects_created + total_objects_reused
        efficiency = (
            (total_objects_reused / total_requests) if total_requests > 0 else 0
        )

        # Estimate cache memory (would need integration with cache manager)
        cache_memory = 0  # Placeholder for cache memory calculation

        return MemoryStats(
            current_usage_mb=current_usage,
            peak_usage_mb=self.peak_memory_mb,
            object_pool_size=total_pool_size,
            cache_memory_mb=cache_memory,
            garbage_collections=self.gc_count,
            last_gc_time=self.last_gc_time,
            memory_efficiency=efficiency,
        )

    def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed memory and pool statistics"""
        memory_stats = self.get_memory_stats()

        pool_stats = {}
        for pool_name, pool in self.pools.items():
            pool_stats[pool_name] = pool.get_stats()

        return {
            "memory": {
                "current_mb": memory_stats.current_usage_mb,
                "peak_mb": memory_stats.peak_usage_mb,
                "target_mb": self.target_memory_mb,
                "alert_threshold_mb": self.alert_threshold_mb,
                "efficiency": memory_stats.memory_efficiency,
                "alerts_count": self.memory_alerts,
            },
            "garbage_collection": {
                "count": memory_stats.garbage_collections,
                "last_gc_time": memory_stats.last_gc_time,
                "thresholds": gc.get_threshold(),
            },
            "object_pools": pool_stats,
            "tracked_objects": len(self.tracked_objects),
        }

    def cleanup(self):
        """Cleanup memory optimizer resources"""
        # Clear all object pools
        for pool in self.pools.values():
            pool.pool.clear()

        # Force final garbage collection
        self.force_gc()

        self.logger.info("Memory optimizer cleaned up")


# Global memory optimizer instance
_memory_optimizer = None


def get_memory_optimizer(target_memory_mb: int = 40) -> MemoryOptimizer:
    """Get global memory optimizer instance"""
    global _memory_optimizer
    if _memory_optimizer is None:
        _memory_optimizer = MemoryOptimizer(target_memory_mb=target_memory_mb)
    return _memory_optimizer


# Common object pool factories
def create_dict_pool(pool_name: str = "dict_pool", max_size: int = 50) -> ObjectPool:
    """Create a pool for dictionary objects"""

    def dict_factory():
        return {}

    optimizer = get_memory_optimizer()
    return optimizer.create_object_pool(pool_name, dict_factory, max_size)


def create_list_pool(pool_name: str = "list_pool", max_size: int = 50) -> ObjectPool:
    """Create a pool for list objects"""

    def list_factory():
        return []

    optimizer = get_memory_optimizer()
    return optimizer.create_object_pool(pool_name, list_factory, max_size)


# Register MemoryOptimizer with the factory system
try:
    register_manager_type(
        manager_type=ManagerType.MEMORY,
        manager_class=MemoryOptimizer,
        description="Enterprise-grade memory optimization with object pooling and GC management",
    )
except Exception:
    pass
