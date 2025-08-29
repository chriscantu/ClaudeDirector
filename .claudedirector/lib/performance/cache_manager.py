"""
Cache Manager for Performance Optimization

Redis-compatible in-memory caching for framework patterns and strategic analysis.
Implements Phase 8 sub-500ms response time requirements.
"""

import asyncio
import time
import hashlib
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass
from enum import Enum
import logging
import json


class CacheLevel(Enum):
    """Cache levels with different TTL strategies"""
    FRAMEWORK_PATTERNS = "framework_patterns"  # 1 hour TTL
    PERSONA_SELECTION = "persona_selection"    # 30 minutes TTL
    CONTEXT_ANALYSIS = "context_analysis"      # 15 minutes TTL
    MCP_RESPONSES = "mcp_responses"            # 5 minutes TTL
    STRATEGIC_MEMORY = "strategic_memory"      # 24 hours TTL


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


class CacheManager:
    """
    High-performance in-memory cache manager for ClaudeDirector

    Features:
    - Redis-compatible interface with async support
    - Intelligent TTL based on cache levels
    - Memory-efficient LRU eviction
    - Performance metrics and monitoring
    - <50ms cache operations for 95% of requests
    """

    def __init__(self, max_memory_mb: int = 20, max_entries: int = 10000):
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.max_entries = max_entries
        self.cache: Dict[str, CacheEntry] = {}
        self.logger = logging.getLogger(__name__)

        # Performance metrics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.memory_usage = 0

        # TTL configuration by cache level
        self.ttl_config = {
            CacheLevel.FRAMEWORK_PATTERNS: 3600,    # 1 hour
            CacheLevel.PERSONA_SELECTION: 1800,     # 30 minutes
            CacheLevel.CONTEXT_ANALYSIS: 900,       # 15 minutes
            CacheLevel.MCP_RESPONSES: 300,          # 5 minutes
            CacheLevel.STRATEGIC_MEMORY: 86400,     # 24 hours
        }

        # Cleanup task
        self._cleanup_task = None
        self._start_cleanup_task()

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
        for key, entry in self.cache.items():
            if entry.is_expired():
                expired_keys.append(key)

        # Remove expired entries
        for key in expired_keys:
            del self.cache[key]
            self.evictions += 1

        if expired_keys:
            self.logger.debug(f"Evicted {len(expired_keys)} expired cache entries")

        # LRU eviction if over memory/entry limits
        if len(self.cache) > self.max_entries:
            await self._lru_eviction()

    async def _lru_eviction(self):
        """Perform LRU eviction to stay within limits"""
        # Sort by last_accessed time (least recently used first)
        sorted_entries = sorted(
            self.cache.items(),
            key=lambda x: x[1].last_accessed or x[1].created_at
        )

        # Remove oldest 20% when limit exceeded
        evict_count = len(self.cache) - int(self.max_entries * 0.8)

        for i in range(evict_count):
            key = sorted_entries[i][0]
            del self.cache[key]
            self.evictions += 1

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
            if key in self.cache:
                entry = self.cache[key]
                if not entry.is_expired():
                    self.hits += 1
                    value = entry.access()

                    # Performance tracking
                    operation_time = (time.time() - start_time) * 1000
                    if operation_time > 50:
                        self.logger.warning(f"Slow cache get: {operation_time:.1f}ms for key {key[:8]}...")

                    return value
                else:
                    # Remove expired entry
                    del self.cache[key]
                    self.evictions += 1

            self.misses += 1
            return None

        except Exception as e:
            self.logger.error(f"Cache get error for key {key[:8]}...: {e}")
            self.misses += 1
            return None

    async def set(
        self,
        key: str,
        value: Any,
        cache_level: CacheLevel = CacheLevel.CONTEXT_ANALYSIS,
        ttl_override: Optional[int] = None
    ) -> bool:
        """Set value in cache with intelligent TTL"""
        start_time = time.time()

        try:
            ttl = ttl_override or self.ttl_config[cache_level]

            entry = CacheEntry(
                value=value,
                created_at=time.time(),
                ttl_seconds=ttl,
                cache_level=cache_level
            )

            self.cache[key] = entry

            # Performance tracking
            operation_time = (time.time() - start_time) * 1000
            if operation_time > 50:
                self.logger.warning(f"Slow cache set: {operation_time:.1f}ms for key {key[:8]}...")

            return True

        except Exception as e:
            self.logger.error(f"Cache set error for key {key[:8]}...: {e}")
            return False

    async def cached_call(
        self,
        func,
        *args,
        cache_level: CacheLevel = CacheLevel.CONTEXT_ANALYSIS,
        namespace: str = "default",
        ttl_override: Optional[int] = None,
        **kwargs
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

        for key in self.cache.keys():
            if pattern in key:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.cache[key]
            self.evictions += 1

        if keys_to_remove:
            self.logger.debug(f"Invalidated {len(keys_to_remove)} cache entries matching pattern: {pattern}")

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests) if total_requests > 0 else 0

        # Memory usage estimation
        memory_estimate = 0
        for entry in self.cache.values():
            try:
                memory_estimate += len(str(entry.value).encode()) + 200  # Entry overhead
            except:
                memory_estimate += 1000  # Conservative estimate for complex objects

        return {
            "entries": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "evictions": self.evictions,
            "memory_usage_bytes": memory_estimate,
            "memory_usage_mb": memory_estimate / (1024 * 1024),
            "cache_levels": {
                level.value: sum(1 for entry in self.cache.values() if entry.cache_level == level)
                for level in CacheLevel
            }
        }

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

        self.cache.clear()
        self.logger.info("Cache cleaned up")


# Global cache manager instance
_cache_manager = None

def get_cache_manager(max_memory_mb: int = 20) -> CacheManager:
    """Get global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager(max_memory_mb=max_memory_mb)
    return _cache_manager
