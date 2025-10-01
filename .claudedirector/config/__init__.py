"""
ClaudeDirector Configuration Module

Canonical location for all performance and system configuration.
"""

from .performance_config import (
    PromptCachingConfig,
    CacheManagerConfig,
    ContextEngineConfig,
    SDKErrorHandlingConfig,
    get_prompt_caching_config,
    get_cache_manager_config,
    get_context_engine_config,
    get_sdk_error_handling_config,
    validate_performance_config,
    PROMPT_CACHING_CONFIG,
    CACHE_MANAGER_CONFIG,
    CONTEXT_ENGINE_CONFIG,
    SDK_ERROR_HANDLING_CONFIG,
)

__all__ = [
    "PromptCachingConfig",
    "CacheManagerConfig",
    "ContextEngineConfig",
    "SDKErrorHandlingConfig",
    "get_prompt_caching_config",
    "get_cache_manager_config",
    "get_context_engine_config",
    "get_sdk_error_handling_config",
    "validate_performance_config",
    "PROMPT_CACHING_CONFIG",
    "CACHE_MANAGER_CONFIG",
    "CONTEXT_ENGINE_CONFIG",
    "SDK_ERROR_HANDLING_CONFIG",
]
