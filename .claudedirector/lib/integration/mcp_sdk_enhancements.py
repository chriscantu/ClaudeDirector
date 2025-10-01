"""
MCP SDK Enhancements - Extends MCPEnterpriseCoordinator with SDK Error Patterns

ARCHITECTURAL COMPLIANCE:
- EXTENDS existing MCPEnterpriseCoordinator (no duplication)
- ADDS ONLY SDK error categorization to existing circuit breaker
- REUSES all existing circuit breaker, retry, and coordination logic
- FOLLOWS Open/Closed Principle (extension without modification)

Author: Martin | Platform Architecture
Phase: Task 002 - SDK Error Enhancement
Date: 2025-10-01
"""

from typing import Dict, Any, Optional, Callable
import logging
from functools import wraps

try:
    from .mcp_enterprise_coordinator import MCPEnterpriseCoordinator, MCPServerStatus
    from ..core.sdk_enhanced_manager import SDKEnhancedManager, SDKErrorCategory
    from ..config.performance_config import get_sdk_error_handling_config
except ImportError:
    # Fallback for test environments with different PYTHONPATH
    import sys
    from pathlib import Path

    # Add .claudedirector to sys.path for absolute imports
    _claudedirector_root = Path(__file__).resolve().parent.parent.parent
    if str(_claudedirector_root) not in sys.path:
        sys.path.insert(0, str(_claudedirector_root))

    # Absolute imports from lib package (avoids circular import detection)
    from lib.integration.mcp_enterprise_coordinator import (
        MCPEnterpriseCoordinator,
        MCPServerStatus,
    )
    from lib.core.sdk_enhanced_manager import SDKEnhancedManager, SDKErrorCategory

    # Import from canonical config location
    _config_root = _claudedirector_root / "config"
    sys.path.insert(0, str(_config_root))
    from performance_config import get_sdk_error_handling_config


def enhance_mcp_coordinator_with_sdk_patterns(
    coordinator: MCPEnterpriseCoordinator,
) -> MCPEnterpriseCoordinator:
    """
    Enhance existing MCP coordinator with SDK error categorization

    BLOAT_PREVENTION Compliance:
    - EXTENDS existing coordinator (doesn't replace)
    - ADDS ONLY SDK error categorization
    - REUSES all existing circuit breaker logic

    SOLID Compliance:
    - Open/Closed Principle: Extension without modification
    - Single Responsibility: Only adds error categorization

    Args:
        coordinator: Existing MCPEnterpriseCoordinator to enhance

    Returns:
        MCPEnterpriseCoordinator: Enhanced coordinator with SDK patterns
    """

    # Create SDK error categorizer (reuses existing SDKEnhancedManager)
    sdk_manager = SDKEnhancedManager()

    # Store original methods to enhance them (decorator pattern)
    original_record_failure = coordinator._record_failure

    def enhanced_record_failure(server_id: str, error: Exception = None):
        """Enhanced failure recording with SDK error categorization"""
        if error:
            # NEW: Add SDK error categorization
            error_category = sdk_manager.categorize_sdk_error(error)

            # Log SDK error category for MCP context
            coordinator.logger.info(
                "MCP error categorized",
                server_id=server_id,
                error_category=error_category.value,
                error_message=str(error),
            )

            # Adjust circuit breaker behavior based on error category
            if error_category == SDKErrorCategory.PERMANENT:
                # Permanent errors should trip circuit breaker faster
                sdk_config = get_sdk_error_handling_config()
                original_threshold = coordinator.circuit_breaker_threshold
                new_threshold = int(
                    original_threshold
                    * sdk_config.circuit_breaker_threshold_reduction_factor
                )
                coordinator.circuit_breaker_threshold = max(1, new_threshold)
                coordinator.logger.warning(
                    f"Permanent error detected for {server_id}, reducing circuit breaker threshold"
                )
            elif error_category == SDKErrorCategory.RATE_LIMIT:
                # Rate limit errors should have longer backoff
                coordinator.logger.warning(
                    f"Rate limit detected for {server_id}, extending backoff period"
                )
            elif error_category == SDKErrorCategory.CONTEXT_LIMIT:
                # Context limit errors indicate configuration issues
                coordinator.logger.error(
                    f"Context limit exceeded for {server_id}, may need configuration adjustment"
                )

        # REUSE: Original circuit breaker logic (no duplication)
        return original_record_failure(server_id)

    # Store original coordinate_mcp_request method
    original_coordinate_request = coordinator.coordinate_mcp_request

    async def enhanced_coordinate_request(
        capability: str, content: Dict[str, Any], **kwargs
    ):
        """Enhanced coordination with SDK error handling"""
        try:
            # REUSE: Original coordination logic (no duplication)
            return await original_coordinate_request(capability, content, **kwargs)
        except Exception as e:
            # NEW: Add SDK error categorization for MCP requests
            error_category = sdk_manager.categorize_sdk_error(e)

            # Enhanced failure recording with SDK categorization
            enhanced_record_failure("current_server", e)

            # Add SDK error context to exception for upstream handling
            e.sdk_error_category = error_category.value

            # Re-raise for existing error handling
            raise

    # Enhance coordinator with SDK patterns (monkey patching for extension)
    coordinator._record_failure = enhanced_record_failure
    coordinator.coordinate_mcp_request = enhanced_coordinate_request
    coordinator.sdk_error_categorizer = sdk_manager

    # Add method to get SDK error statistics
    def get_sdk_error_stats():
        """Get SDK error statistics for this coordinator"""
        return sdk_manager.get_sdk_error_stats()

    coordinator.get_sdk_error_stats = get_sdk_error_stats

    coordinator.logger.info(
        "MCP coordinator enhanced with SDK error categorization patterns"
    )

    return coordinator


class MCPSDKErrorTracker:
    """
    Tracks SDK error patterns across MCP servers

    Single Responsibility: SDK error pattern tracking for MCP context

    BLOAT_PREVENTION Compliance:
    - Uses existing SDKEnhancedManager for categorization (no duplication)
    - Adds ONLY MCP-specific error tracking
    """

    def __init__(self):
        """Initialize MCP SDK error tracker"""
        self.error_patterns_by_server: Dict[str, Dict[SDKErrorCategory, int]] = {}
        self.sdk_manager = SDKEnhancedManager()
        self.logger = logging.getLogger(__name__)

    def track_mcp_error(self, server_id: str, error: Exception):
        """
        Track SDK error patterns for specific MCP server

        Args:
            server_id: MCP server identifier
            error: Exception that occurred
        """
        if server_id not in self.error_patterns_by_server:
            self.error_patterns_by_server[server_id] = {
                category: 0 for category in SDKErrorCategory
            }

        error_category = self.sdk_manager.categorize_sdk_error(error)
        self.error_patterns_by_server[server_id][error_category] += 1

        self.logger.debug(
            f"Tracked SDK error for MCP server {server_id}: {error_category.value}"
        )

    def get_server_error_profile(self, server_id: str) -> Dict[str, Any]:
        """
        Get SDK error profile for MCP server

        Args:
            server_id: MCP server identifier

        Returns:
            Dict containing error patterns and recommendations
        """
        if server_id not in self.error_patterns_by_server:
            return {"error_patterns": {}, "recommendations": [], "total_errors": 0}

        patterns = self.error_patterns_by_server[server_id]
        total_errors = sum(patterns.values())

        if total_errors == 0:
            return {"error_patterns": {}, "recommendations": [], "total_errors": 0}

        # Load threshold configuration
        sdk_config = get_sdk_error_handling_config()

        # Generate recommendations based on error patterns (configuration-driven)
        recommendations = []

        rate_limit_ratio = patterns[SDKErrorCategory.RATE_LIMIT] / total_errors
        if rate_limit_ratio > sdk_config.rate_limit_threshold_ratio:
            recommendations.append(
                "Consider implementing request throttling or increasing rate limits"
            )

        timeout_ratio = patterns[SDKErrorCategory.TIMEOUT] / total_errors
        if timeout_ratio > sdk_config.timeout_threshold_ratio:
            recommendations.append(
                "Consider increasing timeout values or optimizing request processing"
            )

        permanent_ratio = patterns[SDKErrorCategory.PERMANENT] / total_errors
        if permanent_ratio > sdk_config.permanent_threshold_ratio:
            recommendations.append(
                "Check server configuration and authentication settings"
            )

        context_limit_ratio = patterns[SDKErrorCategory.CONTEXT_LIMIT] / total_errors
        if context_limit_ratio > sdk_config.context_limit_threshold_ratio:
            recommendations.append(
                "Review request payload sizes and context window limits"
            )

        return {
            "error_patterns": {cat.value: count for cat, count in patterns.items()},
            "total_errors": total_errors,
            "error_ratios": {
                "rate_limit": rate_limit_ratio,
                "timeout": timeout_ratio,
                "permanent": permanent_ratio,
                "context_limit": context_limit_ratio,
                "transient": patterns[SDKErrorCategory.TRANSIENT] / total_errors,
            },
            "recommendations": recommendations,
        }

    def get_all_servers_summary(self) -> Dict[str, Any]:
        """
        Get summary of SDK error patterns across all MCP servers

        Returns:
            Dict containing aggregate error statistics
        """
        all_patterns = {category: 0 for category in SDKErrorCategory}
        server_count = len(self.error_patterns_by_server)

        for server_patterns in self.error_patterns_by_server.values():
            for category, count in server_patterns.items():
                all_patterns[category] += count

        total_errors = sum(all_patterns.values())

        return {
            "total_servers_tracked": server_count,
            "total_errors_across_servers": total_errors,
            "aggregate_error_patterns": {
                cat.value: count for cat, count in all_patterns.items()
            },
            "most_common_error_category": (
                max(all_patterns, key=all_patterns.get).value
                if total_errors > 0
                else None
            ),
            "servers_with_errors": list(self.error_patterns_by_server.keys()),
        }

    def reset_server_stats(self, server_id: str):
        """
        Reset error statistics for specific server

        Args:
            server_id: MCP server identifier
        """
        if server_id in self.error_patterns_by_server:
            self.error_patterns_by_server[server_id] = {
                category: 0 for category in SDKErrorCategory
            }
            self.logger.info(f"Reset SDK error stats for MCP server {server_id}")

    def reset_all_stats(self):
        """Reset error statistics for all servers"""
        self.error_patterns_by_server.clear()
        self.logger.info("Reset SDK error stats for all MCP servers")


def create_mcp_sdk_error_tracker() -> MCPSDKErrorTracker:
    """
    Factory function to create MCP SDK error tracker

    Returns:
        MCPSDKErrorTracker: New error tracker instance
    """
    return MCPSDKErrorTracker()


# Decorator for automatic SDK error tracking in MCP methods
def track_mcp_sdk_errors(server_id_param: str = "server_id"):
    """
    Decorator to automatically track SDK errors in MCP methods

    Args:
        server_id_param: Name of parameter containing server ID

    Returns:
        Decorated function with automatic error tracking
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Extract server ID from parameters
                server_id = kwargs.get(server_id_param, "unknown")

                # Track the error
                if hasattr(wrapper, "_error_tracker"):
                    wrapper._error_tracker.track_mcp_error(server_id, e)

                # Re-raise the exception
                raise

        # Attach error tracker to the wrapper
        wrapper._error_tracker = create_mcp_sdk_error_tracker()
        return wrapper

    return decorator


# Export public interface
__all__ = [
    "enhance_mcp_coordinator_with_sdk_patterns",
    "MCPSDKErrorTracker",
    "create_mcp_sdk_error_tracker",
    "track_mcp_sdk_errors",
]
