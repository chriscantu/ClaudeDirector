"""
Configuration Management Module

Centralized configuration for ClaudeDirector system components.
Provides single source of truth for all configuration constants.

Author: Martin | Platform Architecture
Phase: Task 001 - Configuration Consolidation
Date: 2025-10-01
"""

from .user_config import *

# Import from canonical location: .claudedirector/config/performance_config.py
# This avoids duplication and follows PROJECT_STRUCTURE.md
import sys
from pathlib import Path

# Get absolute path to .claudedirector directory
# __file__ is .claudedirector/lib/config/__init__.py
# parent is .claudedirector/lib/config/
# parent.parent is .claudedirector/lib/
# parent.parent.parent is .claudedirector/
_claudedirector_root = Path(__file__).resolve().parent.parent.parent
_repo_root = _claudedirector_root.parent

# Add repo root to sys.path if not already present
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

# Now import from .claudedirector.config (absolute import)
try:
    from claudedirector.config import (
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
except ModuleNotFoundError:
    # Fallback: Direct file import if package import fails
    # Performance config is in .claudedirector/config/ (canonical location)
    import importlib.util

    _config_path = _claudedirector_root / "config" / "performance_config.py"
    spec = importlib.util.spec_from_file_location("performance_config", _config_path)
    performance_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(performance_config)

    # Re-export all from the loaded module
    PromptCachingConfig = performance_config.PromptCachingConfig
    CacheManagerConfig = performance_config.CacheManagerConfig
    ContextEngineConfig = performance_config.ContextEngineConfig
    SDKErrorHandlingConfig = performance_config.SDKErrorHandlingConfig
    get_prompt_caching_config = performance_config.get_prompt_caching_config
    get_cache_manager_config = performance_config.get_cache_manager_config
    get_context_engine_config = performance_config.get_context_engine_config
    get_sdk_error_handling_config = performance_config.get_sdk_error_handling_config
    validate_performance_config = performance_config.validate_performance_config
    PROMPT_CACHING_CONFIG = performance_config.PROMPT_CACHING_CONFIG
    CACHE_MANAGER_CONFIG = performance_config.CACHE_MANAGER_CONFIG
    CONTEXT_ENGINE_CONFIG = performance_config.CONTEXT_ENGINE_CONFIG
    SDK_ERROR_HANDLING_CONFIG = performance_config.SDK_ERROR_HANDLING_CONFIG

__all__ = [
    # Performance configuration
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
