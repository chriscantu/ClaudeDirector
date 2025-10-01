"""
Performance Configuration Constants

Centralized configuration for all performance-related hard-coded values.
Eliminates BLOAT_PREVENTION_SYSTEM.md violations by providing single source of truth.

Author: Martin | Platform Architecture
Phase: Task 001 - Configuration Consolidation
Date: 2025-10-01
"""

from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


@dataclass
class PromptCachingConfig:
    """SDK-inspired prompt caching configuration"""

    # Cache TTL settings
    default_cache_ttl_seconds: int = 3600  # 1 hour

    # Token estimation defaults
    persona_template_tokens: int = 2000
    framework_context_tokens: int = 300
    system_instructions_tokens: int = 1500

    # Performance baselines
    baseline_assembly_time_ms: float = 150.0
    target_assembly_time_ms: float = 100.0
    latency_saved_per_cache_hit_ms: float = 15.0

    # Cache hit rate expectations
    persona_template_hit_rate: float = 0.95  # 95%
    framework_context_hit_rate: float = 0.60  # 60%
    system_instructions_hit_rate: float = 0.99  # 99%


@dataclass
class CacheManagerConfig:
    """Cache manager configuration constants"""

    # Memory limits
    default_max_memory_mb: int = 20
    default_max_entries: int = 10000

    # Performance thresholds
    performance_threshold_ms: int = 50
    cleanup_interval_seconds: int = 60

    # Cache eviction settings
    eviction_threshold_ratio: float = 0.8  # Remove oldest 20% when limit exceeded

    # TTL defaults (centralized)
    ttl_defaults: Dict[str, int] = None

    def __post_init__(self):
        if self.ttl_defaults is None:
            self.ttl_defaults = {
                "framework_patterns": 3600,  # 1 hour
                "persona_selection": 1800,  # 30 minutes
                "context_analysis": 900,  # 15 minutes
                "mcp_responses": 300,  # 5 minutes
                "strategic_memory": 86400,  # 24 hours
                "mcp_sequential": 600,  # 10 minutes
                "mcp_context7": 1800,  # 30 minutes
                "mcp_magic": 900,  # 15 minutes
                "mcp_playwright": 300,  # 5 minutes
            }


@dataclass
class ContextEngineConfig:
    """Advanced context engine configuration constants"""

    # Size limits
    default_max_context_size_bytes: int = 1024 * 1024  # 1MB

    # Performance targets
    retrieval_time_target_seconds: float = 3.0
    relevance_score_target: float = 0.9
    memory_footprint_target_bytes: int = 1024 * 1024 * 1024  # 1GB

    # Metrics tracking
    recent_metrics_limit: int = 100  # Last 100 retrievals

    # Fallback values
    fallback_assembly_time_ms: float = 0.1
    fallback_context_size_bytes: int = 256
    fallback_coherence_score: float = 0.5
    fallback_relevance_score: float = 0.5
    fallback_layer_coverage: float = 0.2


# Global configuration instances
PROMPT_CACHING_CONFIG = PromptCachingConfig()
CACHE_MANAGER_CONFIG = CacheManagerConfig()
CONTEXT_ENGINE_CONFIG = ContextEngineConfig()


def get_prompt_caching_config() -> PromptCachingConfig:
    """Get prompt caching configuration"""
    return PROMPT_CACHING_CONFIG


def get_cache_manager_config() -> CacheManagerConfig:
    """Get cache manager configuration"""
    return CACHE_MANAGER_CONFIG


def get_context_engine_config() -> ContextEngineConfig:
    """Get context engine configuration"""
    return CONTEXT_ENGINE_CONFIG


# Configuration validation
def validate_performance_config() -> bool:
    """Validate all performance configuration values"""
    try:
        # Validate prompt caching config
        assert PROMPT_CACHING_CONFIG.default_cache_ttl_seconds > 0
        assert PROMPT_CACHING_CONFIG.persona_template_tokens > 0
        assert PROMPT_CACHING_CONFIG.baseline_assembly_time_ms > 0
        assert 0.0 <= PROMPT_CACHING_CONFIG.persona_template_hit_rate <= 1.0

        # Validate cache manager config
        assert CACHE_MANAGER_CONFIG.default_max_memory_mb > 0
        assert CACHE_MANAGER_CONFIG.performance_threshold_ms > 0
        assert 0.0 < CACHE_MANAGER_CONFIG.eviction_threshold_ratio < 1.0

        # Validate context engine config
        assert CONTEXT_ENGINE_CONFIG.default_max_context_size_bytes > 0
        assert CONTEXT_ENGINE_CONFIG.retrieval_time_target_seconds > 0
        assert 0.0 <= CONTEXT_ENGINE_CONFIG.relevance_score_target <= 1.0

        return True
    except AssertionError:
        return False
