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
    from ..config.performance_config import get_cache_manager_config
except ImportError:
    # Fallback for test environments
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    from base_manager import BaseManager, BaseManagerConfig
    from config.performance_config import get_cache_manager_config


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
        super().__init__(config or BaseManagerConfig())

        # SDK-specific error categorization rules (NEW functionality)
        self.sdk_error_patterns = {
            SDKErrorCategory.RATE_LIMIT: [
                "rate limit",
                "too many requests",
                "quota exceeded",
                "429",
                "rate_limit_exceeded",
                "throttled",
                "rate limiting",
            ],
            SDKErrorCategory.TRANSIENT: [
                "timeout",
                "connection",
                "network",
                "502",
                "503",
                "504",
                "temporary failure",
                "service unavailable",
                "connection reset",
            ],
            SDKErrorCategory.PERMANENT: [
                "authentication",
                "unauthorized",
                "invalid api key",
                "401",
                "403",
                "forbidden",
                "invalid_request",
                "bad_request",
                "400",
            ],
            SDKErrorCategory.CONTEXT_LIMIT: [
                "context length",
                "token limit",
                "input too long",
                "context_length_exceeded",
                "maximum context",
                "context window",
                "tokens exceeded",
            ],
            SDKErrorCategory.TIMEOUT: [
                "request timeout",
                "read timeout",
                "connection timeout",
                "deadline exceeded",
                "timed out",
                "timeout error",
            ],
        }

        # SDK-specific retry strategies (maps to existing BaseManager config)
        self.sdk_retry_strategies = {
            SDKErrorCategory.RATE_LIMIT: {
                "backoff_multiplier": 2.0,
                "max_retries": 5,
                "should_retry": True,
            },
            SDKErrorCategory.TRANSIENT: {
                "backoff_multiplier": 1.5,
                "max_retries": 3,
                "should_retry": True,
            },
            SDKErrorCategory.PERMANENT: {
                "backoff_multiplier": 0,
                "max_retries": 0,
                "should_retry": False,
            },
            SDKErrorCategory.CONTEXT_LIMIT: {
                "backoff_multiplier": 0,
                "max_retries": 0,
                "should_retry": False,
            },
            SDKErrorCategory.TIMEOUT: {
                "backoff_multiplier": 1.2,
                "max_retries": 2,
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

        def sdk_enhanced_operation():
            """Wrapper that adds SDK error categorization"""
            try:
                # Execute the actual operation (delegated to subclass)
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
                    raise

                # Re-raise for BaseManager retry logic to handle
                raise

        # REUSE: BaseManager._execute_with_retry (no duplication)
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
            enable_logging=config.get("enable_logging", True),
            enable_caching=config.get("enable_caching", True),
            enable_metrics=config.get("enable_metrics", True),
            max_retries=config.get("max_retries", 3),
            error_recovery=config.get("error_recovery", True),
            custom_config=config.get("custom_config", {}),
        )
    else:
        manager_config = BaseManagerConfig()

    return SDKEnhancedManager(manager_config)


# Export public interface
__all__ = ["SDKErrorCategory", "SDKEnhancedManager", "create_sdk_enhanced_manager"]
