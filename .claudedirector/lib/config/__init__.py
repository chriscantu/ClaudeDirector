"""
Configuration Management Module

Centralized configuration for ClaudeDirector system components.
Provides single source of truth for all configuration constants.

Author: Martin | Platform Architecture
Phase: Task 001 - Configuration Consolidation
Date: 2025-10-01
"""

from .user_config import *
from .performance_config import (
    PromptCachingConfig,
    CacheManagerConfig,
    ContextEngineConfig,
    get_prompt_caching_config,
    get_cache_manager_config,
    get_context_engine_config,
    validate_performance_config,
    PROMPT_CACHING_CONFIG,
    CACHE_MANAGER_CONFIG,
    CONTEXT_ENGINE_CONFIG,
)

__all__ = [
    # Performance configuration
    "PromptCachingConfig",
    "CacheManagerConfig",
    "ContextEngineConfig",
    "get_prompt_caching_config",
    "get_cache_manager_config",
    "get_context_engine_config",
    "validate_performance_config",
    "PROMPT_CACHING_CONFIG",
    "CACHE_MANAGER_CONFIG",
    "CONTEXT_ENGINE_CONFIG",
]
