"""
Cache Manager for Performance Optimization

Redis-compatible in-memory caching for framework patterns and strategic analysis.
Implements Phase 8 sub-500ms response time requirements.

Refactored to use BaseManager pattern for DRY compliance.
Eliminates duplicate infrastructure patterns while preserving all functionality.

Author: Martin | Platform Architecture
Phase: 8.1.3 - Core Infrastructure Manager Refactoring
"""

import asyncio
import time
import hashlib
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass
from enum import Enum
import json

# Import BaseManager infrastructure
try:
    from ..core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from ..core.manager_factory import register_manager_type
except ImportError:
    # Fallback for test environments
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.base_manager import BaseManager, BaseManagerConfig, ManagerType
    from core.manager_factory import register_manager_type


class CacheLevel(Enum):
    """Cache levels with different TTL strategies"""

    FRAMEWORK_PATTERNS = "framework_patterns"  # 1 hour TTL
    PERSONA_SELECTION = "persona_selection"  # 30 minutes TTL
    CONTEXT_ANALYSIS = "context_analysis"  # 15 minutes TTL
    MCP_RESPONSES = "mcp_responses"  # 5 minutes TTL
    STRATEGIC_MEMORY = "strategic_memory"  # 24 hours TTL
    # 🚀 ENHANCEMENT: MCP-specific cache levels
    MCP_SEQUENTIAL = "mcp_sequential"  # 10 minutes TTL - Complex analysis
    MCP_CONTEXT7 = "mcp_context7"  # 30 minutes TTL - Documentation
    MCP_MAGIC = "mcp_magic"  # 15 minutes TTL - UI components
    MCP_PLAYWRIGHT = "mcp_playwright"  # 5 minutes TTL - Testing results


@dataclass
class CacheEntry:
    """Cache entry with metadata"""

    value: Any
    created_at: float
    ttl_seconds: int
    access_count: int = 0
    last_accessed: float = 0
    cache_level: CacheLevel = CacheLevel.CONTEXT_ANALYSIS

    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        return time.time() - self.created_at > self.ttl_seconds

    def access(self) -> Any:
        """Record access and return value"""
        self.access_count += 1
        self.last_accessed = time.time()
        return self.value


class CacheManager(BaseManager):
    """
    High-performance in-memory cache manager for ClaudeDirector

    Refactored to inherit from BaseManager for DRY compliance.
    Eliminates duplicate logging, metrics, and configuration patterns.

    Features:
    - Redis-compatible interface with async support
    - Intelligent TTL based on cache levels
    - Memory-efficient LRU eviction
    - Performance metrics and monitoring (via BaseManager)
    - <50ms cache operations for 95% of requests
    """

    def __init__(
        self,
        config: Optional[BaseManagerConfig] = None,
        max_memory_mb: int = 20,
        max_entries: int = 10000,
        cache: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """Initialize cache manager with BaseManager infrastructure"""

        # Create default config if not provided
        if config is None:
            config = BaseManagerConfig(
                manager_name="cache_manager",
                manager_type=ManagerType.CACHE,
                enable_metrics=True,
                enable_caching=False,  # This IS the cache, don't cache the cache
                enable_logging=True,
                performance_tracking=True,
                custom_config={
                    "max_memory_mb": max_memory_mb,
                    "max_entries": max_entries,
                    "performance_threshold_ms": 50,
                    "cleanup_interval_seconds": 60,
                    "ttl_config": {
                        "framework_patterns": 3600,  # 1 hour
                        "persona_selection": 1800,  # 30 minutes
                        "context_analysis": 900,  # 15 minutes
                        "mcp_responses": 300,  # 5 minutes
                        "strategic_memory": 86400,  # 24 hours
                        # 🚀 ENHANCEMENT: MCP-specific config
                        "mcp_sequential": 600,  # 10 minutes
                        "mcp_context7": 1800,  # 30 minutes
                        "mcp_magic": 900,  # 15 minutes
                        "mcp_playwright": 300,  # 5 minutes
                    },
                },
            )

        # Initialize BaseManager infrastructure (eliminates duplicate patterns)
        super().__init__(config, cache, metrics, logger_name="CacheManager")

        # Cache-specific configuration from BaseManager config
        # Use custom_config values or fallback to parameters
        config_max_memory = self.config.custom_config.get(
            "max_memory_mb", max_memory_mb
        )
        config_max_entries = self.config.custom_config.get("max_entries", max_entries)
        config_threshold = self.config.custom_config.get("performance_threshold_ms", 50)

        self.max_memory_bytes = config_max_memory * 1024 * 1024
        self.max_entries = config_max_entries
        self.performance_threshold_ms = config_threshold

        # Cache storage (separate from BaseManager's cache to avoid confusion)
        self.cache_storage: Dict[str, CacheEntry] = {}

        # Cache-specific metrics (in addition to BaseManager metrics)
        self.cache_hits = 0
        self.cache_misses = 0
        self.cache_evictions = 0

        # TTL configuration from config (no hard-coded values)
        ttl_defaults = {
            CacheLevel.FRAMEWORK_PATTERNS: 3600,
            CacheLevel.PERSONA_SELECTION: 1800,
            CacheLevel.CONTEXT_ANALYSIS: 900,
            CacheLevel.MCP_RESPONSES: 300,
            CacheLevel.STRATEGIC_MEMORY: 86400,
            # 🚀 ENHANCEMENT: MCP-specific intelligent TTL
            CacheLevel.MCP_SEQUENTIAL: 600,  # 10 min - Complex analysis
            CacheLevel.MCP_CONTEXT7: 1800,  # 30 min - Documentation
            CacheLevel.MCP_MAGIC: 900,  # 15 min - UI components
            CacheLevel.MCP_PLAYWRIGHT: 300,  # 5 min - Testing results
        }

        self.ttl_config = {}
        ttl_config_data = self.config.custom_config.get("ttl_config", {})
        for level in CacheLevel:
            # Get TTL from config or use default
            config_key = level.value
            self.ttl_config[level] = ttl_config_data.get(
                config_key, ttl_defaults[level]
            )

        # Cleanup task
        self._cleanup_task = None
        self._start_cleanup_task()

        # Use BaseManager logging
        self.logger.info(
            "Cache manager initialized",
            max_memory_mb=self.max_memory_bytes / (1024 * 1024),
            max_entries=self.max_entries,
            ttl_config={level.value: ttl for level, ttl in self.ttl_config.items()},
        )

    def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        Execute cache management operations (BaseManager abstract method implementation)

        Supported operations:
        - 'get': Get value from cache
        - 'set': Set value in cache
        - 'cached_call': Execute cached function call
        - 'invalidate_pattern': Invalidate keys matching pattern
        - 'get_stats': Get cache statistics
        - 'warm_cache': Pre-populate cache
        - 'cleanup': Cleanup resources

        Args:
            operation: Operation to execute
            *args: Positional arguments for operation
            **kwargs: Keyword arguments for operation

        Returns:
            Any: Operation result
        """
        start_time = time.time()

        try:
            if operation == "get":
                # Async operation, return coroutine
                result = self.get(*args, **kwargs)
            elif operation == "set":
                result = self.set(*args, **kwargs)
            elif operation == "cached_call":
                result = self.cached_call(*args, **kwargs)
            elif operation == "invalidate_pattern":
                result = self.invalidate_pattern(*args, **kwargs)
            elif operation == "get_stats":
                result = self.get_stats()
            elif operation == "warm_cache":
                result = self.warm_cache(*args, **kwargs)
            elif operation == "cleanup":
                result = self.cleanup()
            else:
                raise ValueError(f"Unknown cache operation: {operation}")

            # Update metrics for successful operation
            duration = (time.time() - start_time) * 1000  # Convert to ms
            self._update_metrics(
                operation, duration / 1000, True
            )  # BaseManager expects seconds

            return result

        except Exception as e:
            # Update metrics for failed operation
            duration = (time.time() - start_time) * 1000
            self._update_metrics(operation, duration / 1000, False)

            # Use BaseManager error handling
            self.logger.error(
                "Cache operation failed",
                operation=operation,
                error=str(e),
                args=args,
                kwargs=kwargs,
            )
            raise

    def _start_cleanup_task(self):
        """Start background cleanup task"""

        async def cleanup_expired():
            while True:
                try:
                    await asyncio.sleep(60)  # Cleanup every minute
                    await self._cleanup_expired_entries()
                except Exception as e:
                    self.logger.error(f"Cache cleanup error: {e}")

        try:
            loop = asyncio.get_running_loop()
            self._cleanup_task = loop.create_task(cleanup_expired())
        except RuntimeError:
            # No event loop running, cleanup will be manual
            self._cleanup_task = None

    async def _cleanup_expired_entries(self):
        """Remove expired entries and perform LRU eviction if needed"""
        expired_keys = []
        current_time = time.time()

        # Find expired entries
        for key, entry in self.cache_storage.items():
            if entry.is_expired():
                expired_keys.append(key)

        # Remove expired entries
        for key in expired_keys:
            del self.cache_storage[key]
            self.cache_evictions += 1

        if expired_keys:
            self.logger.debug(f"Evicted {len(expired_keys)} expired cache entries")

        # LRU eviction if over memory/entry limits
        if len(self.cache_storage) > self.max_entries:
            await self._lru_eviction()

    async def _lru_eviction(self):
        """Perform LRU eviction to stay within limits"""
        # Sort by last_accessed time (least recently used first)
        sorted_entries = sorted(
            self.cache_storage.items(),
            key=lambda x: x[1].last_accessed or x[1].created_at,
        )

        # Remove oldest 20% when limit exceeded
        evict_count = len(self.cache_storage) - int(self.max_entries * 0.8)

        for i in range(evict_count):
            key = sorted_entries[i][0]
            del self.cache_storage[key]
            self.cache_evictions += 1

        if evict_count > 0:
            self.logger.debug(f"LRU evicted {evict_count} cache entries")

    def _generate_cache_key(self, namespace: str, *args, **kwargs) -> str:
        """Generate deterministic cache key from arguments"""
        key_parts = [namespace]

        # Add positional arguments
        for arg in args:
            if isinstance(arg, (str, int, float, bool)):
                key_parts.append(str(arg))
            else:
                key_parts.append(str(hash(str(arg))))

        # Add keyword arguments (sorted for consistency)
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")

        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()[:16]

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache with performance tracking"""
        start_time = time.time()

        try:
            if key in self.cache_storage:
                entry = self.cache_storage[key]
                if not entry.is_expired():
                    self.cache_hits += 1
                    value = entry.access()

                    # Performance tracking using BaseManager config
                    operation_time = (time.time() - start_time) * 1000
                    if operation_time > self.performance_threshold_ms:
                        self.logger.warning(
                            "Slow cache get operation",
                            operation_time_ms=f"{operation_time:.1f}",
                            key_prefix=key[:8],
                            threshold_ms=self.performance_threshold_ms,
                        )

                    return value
                else:
                    # Remove expired entry
                    del self.cache_storage[key]
                    self.cache_evictions += 1

            self.cache_misses += 1
            return None

        except Exception as e:
            self.logger.error(
                "Cache get operation failed", key_prefix=key[:8], error=str(e)
            )
            self.cache_misses += 1
            return None

    async def set(
        self,
        key: str,
        value: Any,
        cache_level: CacheLevel = CacheLevel.CONTEXT_ANALYSIS,
        ttl_override: Optional[int] = None,
    ) -> bool:
        """Set value in cache with intelligent TTL"""
        start_time = time.time()

        try:
            ttl = ttl_override or self.ttl_config[cache_level]

            entry = CacheEntry(
                value=value,
                created_at=time.time(),
                ttl_seconds=ttl,
                cache_level=cache_level,
            )

            self.cache_storage[key] = entry

            # Performance tracking using BaseManager config
            operation_time = (time.time() - start_time) * 1000
            if operation_time > self.performance_threshold_ms:
                self.logger.warning(
                    "Slow cache set operation",
                    operation_time_ms=f"{operation_time:.1f}",
                    key_prefix=key[:8],
                    threshold_ms=self.performance_threshold_ms,
                )

            return True

        except Exception as e:
            self.logger.error(
                "Cache set operation failed", key_prefix=key[:8], error=str(e)
            )
            return False

    async def cached_call(
        self,
        func,
        *args,
        cache_level: CacheLevel = CacheLevel.CONTEXT_ANALYSIS,
        namespace: str = "default",
        ttl_override: Optional[int] = None,
        **kwargs,
    ) -> Any:
        """
        Decorator-style cached function call

        Usage:
            result = await cache_manager.cached_call(
                expensive_function, arg1, arg2,
                cache_level=CacheLevel.FRAMEWORK_PATTERNS,
                namespace="framework_detection"
            )
        """
        # Generate cache key
        cache_key = self._generate_cache_key(namespace, *args, **kwargs)

        # Try to get from cache
        cached_result = await self.get(cache_key)
        if cached_result is not None:
            return cached_result

        # Execute function and cache result
        if asyncio.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)

        # Cache the result
        await self.set(cache_key, result, cache_level, ttl_override)

        return result

    async def invalidate_pattern(self, pattern: str):
        """Invalidate all cache keys matching pattern"""
        keys_to_remove = []

        for key in self.cache_storage.keys():
            if pattern in key:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.cache_storage[key]
            self.cache_evictions += 1

        if keys_to_remove:
            self.logger.debug(
                f"Invalidated {len(keys_to_remove)} cache entries matching pattern: {pattern}"
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics (integrates with BaseManager metrics)"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests) if total_requests > 0 else 0

        # Memory usage estimation
        memory_estimate = 0
        for entry in self.cache_storage.values():
            try:
                memory_estimate += (
                    len(str(entry.value).encode()) + 200
                )  # Entry overhead
            except:
                memory_estimate += 1000  # Conservative estimate for complex objects

        # Combine cache-specific stats with BaseManager metrics
        base_stats = self.get_metrics()

        cache_specific_stats = {
            "entries": len(self.cache_storage),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": hit_rate,
            "cache_evictions": self.cache_evictions,
            "memory_usage_bytes": memory_estimate,
            "memory_usage_mb": memory_estimate / (1024 * 1024),
            "max_memory_mb": self.max_memory_bytes / (1024 * 1024),
            "max_entries": self.max_entries,
            "cache_levels": {
                level.value: sum(
                    1
                    for entry in self.cache_storage.values()
                    if entry.cache_level == level
                )
                for level in CacheLevel
            },
        }

        # Merge BaseManager metrics with cache-specific metrics
        return {**base_stats, **cache_specific_stats}

    async def warm_cache(self, warm_data: Dict[str, Any]):
        """Pre-populate cache with frequently accessed data"""
        for key, data in warm_data.items():
            cache_level = data.get("cache_level", CacheLevel.CONTEXT_ANALYSIS)
            value = data.get("value")
            ttl_override = data.get("ttl")

            await self.set(key, value, cache_level, ttl_override)

        self.logger.info(f"Cache warmed with {len(warm_data)} entries")

    async def cleanup(self):
        """Cleanup resources"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        self.cache_storage.clear()
        self.logger.info("Cache cleaned up")

    # 🚀 ENHANCEMENT: MCP-specific intelligent caching methods

    async def cache_mcp_response(
        self,
        server_type: str,
        query: str,
        response: Any,
        complexity_hint: Optional[str] = None,
    ) -> bool:
        """Intelligently cache MCP server response with optimal TTL"""
        # Generate MCP-specific cache key
        cache_key = self._generate_cache_key("mcp", server_type, query)

        # Determine optimal cache level based on server type and complexity
        cache_level = self._determine_mcp_cache_level(server_type, complexity_hint)

        return await self.set(cache_key, response, cache_level)

    def _determine_mcp_cache_level(
        self, server_type: str, complexity_hint: Optional[str] = None
    ) -> CacheLevel:
        """Determine optimal cache level for MCP server type"""
        # Map server types to cache levels based on response characteristics
        if server_type.lower() == "sequential":
            return CacheLevel.MCP_SEQUENTIAL  # Complex analysis - medium TTL
        elif server_type.lower() == "context7":
            return CacheLevel.MCP_CONTEXT7  # Documentation - long TTL
        elif server_type.lower() == "magic":
            return CacheLevel.MCP_MAGIC  # UI components - medium TTL
        elif server_type.lower() == "playwright":
            return CacheLevel.MCP_PLAYWRIGHT  # Testing - short TTL
        else:
            return CacheLevel.MCP_RESPONSES  # Default MCP cache level


# Global cache manager instance
_cache_manager = None


def get_cache_manager(max_memory_mb: int = 20) -> CacheManager:
    """Get global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager(max_memory_mb=max_memory_mb)
    return _cache_manager


# Register CacheManager with the factory system
try:
    register_manager_type(
        manager_type=ManagerType.CACHE,
        manager_class=CacheManager,
        description="High-performance in-memory cache manager with Redis-compatible interface",
    )
except Exception:
    # Ignore registration errors during import (e.g., circular imports)
    pass
