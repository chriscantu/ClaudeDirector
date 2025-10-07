"""
SDK Enhanced Manager - Extends BaseManager with Agent SDK Error Categorization

ARCHITECTURAL COMPLIANCE:
- EXTENDS existing BaseManager (no duplication)
- ADDS ONLY SDK-specific error categorization
- REUSES all existing retry, error handling, and metrics infrastructure
- FOLLOWS Single Responsibility Principle (only error categorization)

Author: Martin | Platform Architecture
Phase: Task 002 - SDK Error Enhancement
Date: 2025-10-01
"""

from typing import Dict, Any, Optional
from enum import Enum
from abc import ABC

try:
    from .base_manager import BaseManager, BaseManagerConfig
    from ..config.performance_config import (
        get_cache_manager_config,
        get_sdk_error_handling_config,
    )
except ImportError:
    # Fallback for test environments with different PYTHONPATH
    import sys
    from pathlib import Path

    # Add .claudedirector to sys.path for absolute imports
    _claudedirector_root = Path(__file__).resolve().parent.parent.parent
    if str(_claudedirector_root) not in sys.path:
        sys.path.insert(0, str(_claudedirector_root))

    # Absolute imports from lib package (avoids circular import detection)
    from lib.core.base_manager import BaseManager, BaseManagerConfig

    # Import from canonical config location
    _config_root = _claudedirector_root / "config"
    sys.path.insert(0, str(_config_root))
    from performance_config import (
        get_cache_manager_config,
        get_sdk_error_handling_config,
    )


class SDKErrorCategory(Enum):
    """Agent SDK-inspired error categorization"""

    RATE_LIMIT = "rate_limit"  # API rate limiting errors
    TRANSIENT = "transient"  # Temporary network/service issues
    PERMANENT = "permanent"  # Configuration or authentication errors
    CONTEXT_LIMIT = "context_limit"  # Context window exceeded
    TIMEOUT = "timeout"  # Request timeout errors


class SDKEnhancedManager(BaseManager):
    """
    Extends BaseManager with Agent SDK error categorization patterns.

    BLOAT_PREVENTION Compliance:
    - EXTENDS BaseManager (doesn't replace)
    - REUSES existing _execute_with_retry logic
    - ADDS ONLY new SDK error categorization
    - Single responsibility: SDK error pattern recognition

    SOLID Compliance:
    - Single Responsibility: SDK error categorization only
    - Open/Closed: Extends BaseManager without modification
    - Liskov Substitution: Can replace BaseManager in all contexts
    - Interface Segregation: Focused SDK error interface
    - Dependency Inversion: Depends on BaseManager abstraction
    """

    def __init__(self, config: Optional[BaseManagerConfig] = None):
        """Initialize with existing BaseManager infrastructure"""
        # Default config if not provided (with required manager_name)
        if config is None:
            config = BaseManagerConfig(
                manager_name="sdk_enhanced_manager",
                manager_type=None,  # Can be specified by subclasses
            )

        super().__init__(config)

        # Load SDK error configuration from centralized config
        sdk_config = get_sdk_error_handling_config()

        # SDK-specific error categorization rules (from configuration)
        self.sdk_error_patterns = {
            SDKErrorCategory.RATE_LIMIT: sdk_config.rate_limit_patterns,
            SDKErrorCategory.TRANSIENT: sdk_config.transient_patterns,
            SDKErrorCategory.PERMANENT: sdk_config.permanent_patterns,
            SDKErrorCategory.CONTEXT_LIMIT: sdk_config.context_limit_patterns,
            SDKErrorCategory.TIMEOUT: sdk_config.timeout_patterns,
        }

        # SDK-specific retry strategies (from configuration)
        self.sdk_retry_strategies = {
            SDKErrorCategory.RATE_LIMIT: {
                "backoff_multiplier": sdk_config.rate_limit_backoff_multiplier,
                "max_retries": sdk_config.rate_limit_max_retries,
                "should_retry": True,
            },
            SDKErrorCategory.TRANSIENT: {
                "backoff_multiplier": sdk_config.transient_backoff_multiplier,
                "max_retries": sdk_config.transient_max_retries,
                "should_retry": True,
            },
            SDKErrorCategory.PERMANENT: {
                "backoff_multiplier": sdk_config.permanent_backoff_multiplier,
                "max_retries": sdk_config.permanent_max_retries,
                "should_retry": False,
            },
            SDKErrorCategory.CONTEXT_LIMIT: {
                "backoff_multiplier": sdk_config.context_limit_backoff_multiplier,
                "max_retries": sdk_config.context_limit_max_retries,
                "should_retry": False,
            },
            SDKErrorCategory.TIMEOUT: {
                "backoff_multiplier": sdk_config.timeout_backoff_multiplier,
                "max_retries": sdk_config.timeout_max_retries,
                "should_retry": True,
            },
        }

        # SDK error tracking metrics
        self.sdk_error_stats = {category.value: 0 for category in SDKErrorCategory}

    def categorize_sdk_error(self, error: Exception) -> SDKErrorCategory:
        """
        NEW: Categorize error using Agent SDK patterns

        This is the ONLY new functionality - everything else reuses BaseManager

        Args:
            error: Exception to categorize

        Returns:
            SDKErrorCategory: Categorized error type
        """
        error_message = str(error).lower()

        for category, patterns in self.sdk_error_patterns.items():
            if any(pattern in error_message for pattern in patterns):
                # Track categorization for metrics
                self.sdk_error_stats[category.value] += 1
                return category

        # Default to transient for unknown errors
        self.sdk_error_stats[SDKErrorCategory.TRANSIENT.value] += 1
        return SDKErrorCategory.TRANSIENT

    def should_retry_sdk_error(self, error: Exception) -> bool:
        """
        NEW: Determine if error should be retried based on SDK categorization

        Args:
            error: Exception to evaluate

        Returns:
            bool: Whether error should be retried
        """
        error_category = self.categorize_sdk_error(error)
        strategy = self.sdk_retry_strategies.get(error_category, {})
        return strategy.get("should_retry", True)

    def manage_with_sdk_categorization(self, operation: str, *args, **kwargs) -> Any:
        """
        Enhanced management with SDK error categorization

        REUSES: BaseManager._execute_with_retry (no duplication)
        ADDS: SDK error categorization and logging

        Args:
            operation: Operation to execute
            *args: Operation arguments
            **kwargs: Operation keyword arguments

        Returns:
            Any: Operation result
        """
        # First attempt - check if error is retryable
        try:
            return self._execute_operation(operation, *args, **kwargs)
        except Exception as e:
            # NEW: Add SDK error categorization
            error_category = self.categorize_sdk_error(e)

            # Log SDK error category for transparency
            self.logger.info(
                "SDK error categorized",
                error_category=error_category.value,
                error_message=str(e),
                operation=operation,
            )

            # Check if we should retry based on SDK category
            if not self.should_retry_sdk_error(e):
                self.logger.warning(
                    f"Non-retryable error detected ({error_category.value}), not retrying: {e}"
                )
                # Re-raise immediately without retry for non-retryable errors
                raise

            # For retryable errors, use BaseManager retry logic
            def sdk_enhanced_operation():
                """Wrapper for retryable operations"""
                try:
                    return self._execute_operation(operation, *args, **kwargs)
                except Exception as retry_error:
                    # Re-categorize on each retry for stats
                    self.categorize_sdk_error(retry_error)
                    raise

            # REUSE: BaseManager._execute_with_retry for retryable errors only
            return self._execute_with_retry(sdk_enhanced_operation)

    def get_sdk_error_stats(self) -> Dict[str, Any]:
        """NEW: Get SDK-specific error statistics"""
        # This extends BaseManager.get_status() with SDK-specific metrics
        base_status = self.get_status()

        # Add SDK error categorization stats
        base_status["sdk_error_categorization"] = {
            "categories_supported": len(self.sdk_error_patterns),
            "retry_strategies": len(self.sdk_retry_strategies),
            "categorization_active": True,
            "error_counts_by_category": self.sdk_error_stats.copy(),
            "total_sdk_errors": sum(self.sdk_error_stats.values()),
        }

        return base_status

    def reset_sdk_error_stats(self):
        """NEW: Reset SDK error statistics"""
        self.sdk_error_stats = {category.value: 0 for category in SDKErrorCategory}

    def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        Abstract method implementation with SDK enhancement

        This is the BaseManager abstract method implementation
        that adds SDK error categorization to all operations
        """
        return self.manage_with_sdk_categorization(operation, *args, **kwargs)

    def _execute_operation(self, operation: str, *args, **kwargs) -> Any:
        """
        Template method for subclasses to implement specific operations

        This should be overridden by concrete implementations.
        Default implementation logs the operation and returns None.
        """
        self.logger.warning(
            f"No specific implementation for operation: {operation}. "
            f"Subclass should override _execute_operation for custom behavior."
        )
        return None


def create_sdk_enhanced_manager(
    config: Optional[Dict[str, Any]] = None,
) -> SDKEnhancedManager:
    """
    Factory function to create SDK enhanced manager

    Args:
        config: Optional configuration dictionary

    Returns:
        SDKEnhancedManager: Configured SDK enhanced manager
    """
    if config:
        manager_config = BaseManagerConfig(
            manager_name=config.get("manager_name", "sdk_enhanced_manager"),
            manager_type=config.get("manager_type", None),
            enable_logging=config.get("enable_logging", True),
            enable_caching=config.get("enable_caching", True),
            enable_metrics=config.get("enable_metrics", True),
            max_retries=config.get("max_retries", 3),
            error_recovery=config.get("error_recovery", True),
            custom_config=config.get("custom_config", {}),
        )
    else:
        manager_config = None  # Will use default in __init__

    return SDKEnhancedManager(manager_config)


# Export public interface
__all__ = ["SDKErrorCategory", "SDKEnhancedManager", "create_sdk_enhanced_manager"]
