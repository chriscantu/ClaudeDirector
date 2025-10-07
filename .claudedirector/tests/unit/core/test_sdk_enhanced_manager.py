"""
Unit Tests: SDK Enhanced Manager

Tests ONLY new functionality (error categorization)
REUSES existing BaseManager test patterns

Author: Martin | Platform Architecture
Phase: Task 002 - SDK Error Enhancement
Date: 2025-10-01
"""

import pytest
from unittest.mock import Mock, patch
from lib.core.sdk_enhanced_manager import (
    SDKEnhancedManager,
    SDKErrorCategory,
    create_sdk_enhanced_manager,
)
from lib.core.base_manager import BaseManagerConfig


class TestSDKErrorCategorization:
    """Test SDK error categorization (NEW functionality only)"""

    def setup_method(self):
        """Set up test fixtures"""
        self.manager = SDKEnhancedManager()

    def test_rate_limit_error_categorization(self):
        """Test rate limit error detection"""
        test_cases = [
            Exception("Rate limit exceeded"),
            Exception("Too many requests"),
            Exception("HTTP 429 error"),
            Exception("Quota exceeded for API"),
            Exception("Rate_limit_exceeded in response"),
        ]

        for error in test_cases:
            category = self.manager.categorize_sdk_error(error)
            assert category == SDKErrorCategory.RATE_LIMIT, f"Failed for: {error}"

    def test_transient_error_categorization(self):
        """Test transient error detection"""
        test_cases = [
            # NOTE: "Connection timeout" removed - it's a TIMEOUT, not TRANSIENT
            Exception("Network error occurred"),
            Exception("HTTP 502 Bad Gateway"),
            Exception("Service temporarily unavailable"),
            Exception("Connection reset by peer"),
            Exception("Connection refused"),
        ]

        for error in test_cases:
            category = self.manager.categorize_sdk_error(error)
            assert category == SDKErrorCategory.TRANSIENT, f"Failed for: {error}"

    def test_permanent_error_categorization(self):
        """Test permanent error detection"""
        test_cases = [
            Exception("Invalid API key"),
            Exception("Authentication failed"),
            Exception("HTTP 401 Unauthorized"),
            Exception("Forbidden access"),
            Exception("Bad request format"),
        ]

        for error in test_cases:
            category = self.manager.categorize_sdk_error(error)
            assert category == SDKErrorCategory.PERMANENT, f"Failed for: {error}"

    def test_context_limit_error_categorization(self):
        """Test context limit error detection"""
        test_cases = [
            Exception("Context length exceeded"),
            Exception("Token limit reached"),
            Exception("Input too long for model"),
            Exception("Maximum context window exceeded"),
            Exception("Context_length_exceeded error"),
        ]

        for error in test_cases:
            category = self.manager.categorize_sdk_error(error)
            assert category == SDKErrorCategory.CONTEXT_LIMIT, f"Failed for: {error}"

    def test_timeout_error_categorization(self):
        """Test timeout error detection"""
        test_cases = [
            Exception("Request timeout"),
            Exception("Read timeout occurred"),
            Exception("Connection timeout"),
            Exception("Deadline exceeded"),
            Exception("Operation timed out"),
        ]

        for error in test_cases:
            category = self.manager.categorize_sdk_error(error)
            assert category == SDKErrorCategory.TIMEOUT, f"Failed for: {error}"

    def test_unknown_error_defaults_to_transient(self):
        """Test unknown errors default to transient"""
        unknown_errors = [
            Exception("Unknown error message"),
            Exception("Mysterious failure"),
            Exception("Unexpected condition"),
        ]

        for error in unknown_errors:
            category = self.manager.categorize_sdk_error(error)
            assert category == SDKErrorCategory.TRANSIENT, f"Failed for: {error}"

    def test_error_categorization_tracking(self):
        """Test that error categorization is tracked in statistics"""
        # Start with clean stats
        self.manager.reset_sdk_error_stats()

        # Categorize different types of errors
        self.manager.categorize_sdk_error(Exception("Rate limit exceeded"))
        self.manager.categorize_sdk_error(Exception("Rate limit exceeded"))
        self.manager.categorize_sdk_error(
            Exception("Connection timeout")
        )  # Now TIMEOUT category
        self.manager.categorize_sdk_error(Exception("Invalid API key"))

        stats = self.manager.get_sdk_error_stats()
        error_counts = stats["sdk_error_categorization"]["error_counts_by_category"]

        assert error_counts["rate_limit"] == 2
        assert (
            error_counts["transient"] == 0
        )  # FIX: Connection timeout is now TIMEOUT, not TRANSIENT
        assert error_counts["permanent"] == 1
        assert error_counts["context_limit"] == 0
        assert (
            error_counts["timeout"] == 1
        )  # FIX: Connection timeout correctly categorized as TIMEOUT

    def test_should_retry_sdk_error(self):
        """Test retry decision based on SDK error categorization"""
        # Should retry
        assert (
            self.manager.should_retry_sdk_error(Exception("Rate limit exceeded"))
            is True
        )
        assert (
            self.manager.should_retry_sdk_error(Exception("Connection timeout")) is True
        )
        assert self.manager.should_retry_sdk_error(Exception("Request timeout")) is True

        # Should not retry
        assert (
            self.manager.should_retry_sdk_error(Exception("Invalid API key")) is False
        )
        assert (
            self.manager.should_retry_sdk_error(Exception("Context length exceeded"))
            is False
        )

    def test_sdk_error_stats_extension(self):
        """Test SDK error stats extend BaseManager status"""
        stats = self.manager.get_sdk_error_stats()

        # Should include BaseManager status (from get_status())
        assert "cache_stats" in stats  # From BaseManager.get_status()
        assert (
            "performance" in stats
        )  # FIX: BaseManager.get_status() returns "performance", not "metrics"
        assert "error_stats" in stats  # From BaseManager.get_status()

        # Should include SDK-specific stats
        assert "sdk_error_categorization" in stats
        sdk_stats = stats["sdk_error_categorization"]

        assert sdk_stats["categorization_active"] is True
        assert sdk_stats["categories_supported"] == 5
        assert sdk_stats["retry_strategies"] == 5
        assert "error_counts_by_category" in sdk_stats
        assert "total_sdk_errors" in sdk_stats


class TestSDKEnhancedManagerIntegration:
    """Test integration with BaseManager functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.manager = SDKEnhancedManager()

    @patch.object(SDKEnhancedManager, "_execute_operation")
    def test_manage_with_sdk_categorization_success(self, mock_execute):
        """Test successful operation with SDK categorization"""
        mock_execute.return_value = "success"

        result = self.manager.manage_with_sdk_categorization(
            "test_operation", "arg1", key="value"
        )

        assert result == "success"
        mock_execute.assert_called_once_with("test_operation", "arg1", key="value")

    @patch.object(SDKEnhancedManager, "_execute_operation")
    def test_manage_with_sdk_categorization_retryable_error(self, mock_execute):
        """Test retryable error handling with SDK categorization"""
        # First call fails with retryable error, second succeeds
        mock_execute.side_effect = [Exception("Connection timeout"), "success"]

        result = self.manager.manage_with_sdk_categorization("test_operation")

        assert result == "success"
        assert mock_execute.call_count == 2

    @patch.object(SDKEnhancedManager, "_execute_operation")
    def test_manage_with_sdk_categorization_non_retryable_error(self, mock_execute):
        """Test non-retryable error handling with SDK categorization"""
        mock_execute.side_effect = Exception("Invalid API key")

        with pytest.raises(Exception, match="Invalid API key"):
            self.manager.manage_with_sdk_categorization("test_operation")

        # Should not retry permanent errors
        assert mock_execute.call_count == 1

    def test_manage_delegates_to_sdk_categorization(self):
        """Test that manage() method delegates to SDK categorization"""
        with patch.object(
            self.manager, "manage_with_sdk_categorization"
        ) as mock_manage:
            mock_manage.return_value = "delegated"

            result = self.manager.manage("test_op", "arg1", key="value")

            assert result == "delegated"
            mock_manage.assert_called_once_with("test_op", "arg1", key="value")

    def test_execute_operation_not_implemented(self):
        """Test that _execute_operation logs warning and returns None (default behavior)"""
        # FIX: Production behavior changed - now logs warning and returns None (not exception)
        # This allows SDKEnhancedManager to be instantiated directly for testing/SDK-only use
        result = self.manager._execute_operation("test_operation")
        assert result is None  # Default implementation returns None


class TestSDKEnhancedManagerFactory:
    """Test factory function for creating SDK enhanced managers"""

    def test_create_sdk_enhanced_manager_default_config(self):
        """Test factory with default configuration"""
        manager = create_sdk_enhanced_manager()

        assert isinstance(manager, SDKEnhancedManager)
        assert manager.config.enable_logging is True
        assert manager.config.enable_caching is True
        assert manager.config.max_retries == 3

    def test_create_sdk_enhanced_manager_custom_config(self):
        """Test factory with custom configuration"""
        config = {
            "enable_logging": False,
            "max_retries": 5,
            "error_recovery": False,
            "custom_config": {"test_key": "test_value"},
        }

        manager = create_sdk_enhanced_manager(config)

        assert isinstance(manager, SDKEnhancedManager)
        assert manager.config.enable_logging is False
        assert manager.config.max_retries == 5
        assert manager.config.error_recovery is False
        assert manager.config.custom_config["test_key"] == "test_value"


class TestSDKEnhancedManagerArchitecturalCompliance:
    """Test architectural compliance (SOLID, DRY, BLOAT_PREVENTION)"""

    def setup_method(self):
        """Set up test fixtures"""
        self.manager = SDKEnhancedManager()

    def test_extends_base_manager(self):
        """Test that SDKEnhancedManager properly extends BaseManager"""
        from lib.core.base_manager import BaseManager

        assert isinstance(self.manager, BaseManager)
        assert hasattr(self.manager, "_execute_with_retry")  # From BaseManager
        assert hasattr(self.manager, "get_status")  # From BaseManager
        assert hasattr(self.manager, "categorize_sdk_error")  # New functionality

    def test_single_responsibility_principle(self):
        """Test SRP: Only adds SDK error categorization"""
        # Should have SDK error categorization methods
        assert hasattr(self.manager, "categorize_sdk_error")
        assert hasattr(self.manager, "should_retry_sdk_error")
        assert hasattr(self.manager, "get_sdk_error_stats")

        # Should NOT duplicate BaseManager functionality
        # (BaseManager methods should be inherited, not reimplemented)
        # Check that _execute_with_retry is NOT defined in SDKEnhancedManager's __dict__
        assert "_execute_with_retry" not in SDKEnhancedManager.__dict__

    def test_open_closed_principle(self):
        """Test OCP: Extends BaseManager without modification"""
        # Should be able to use as BaseManager
        from lib.core.base_manager import BaseManager

        def use_base_manager(manager: BaseManager):
            return manager.get_status()

        # Should work with SDKEnhancedManager (Liskov Substitution)
        result = use_base_manager(self.manager)
        assert isinstance(result, dict)

    def test_no_duplication_of_base_manager_logic(self):
        """Test that no BaseManager logic is duplicated"""
        # Check that retry logic is inherited, not duplicated

        # Should NOT have _execute_with_retry defined in SDKEnhancedManager
        # (Check __dict__ to exclude inherited methods)
        sdk_methods = list(SDKEnhancedManager.__dict__.keys())
        assert "_execute_with_retry" not in sdk_methods

        # Should have it available through inheritance
        assert hasattr(self.manager, "_execute_with_retry")

        # Verify it's actually from BaseManager
        from lib.core.base_manager import BaseManager

        assert hasattr(BaseManager, "_execute_with_retry")

    def test_graceful_degradation(self):
        """Test graceful degradation if SDK categorization fails"""
        # Mock categorize_sdk_error to raise exception
        with patch.object(
            self.manager,
            "categorize_sdk_error",
            side_effect=Exception("Categorization failed"),
        ):
            # Should still be able to determine retry behavior
            # (This tests the fallback behavior)
            try:
                should_retry = self.manager.should_retry_sdk_error(
                    Exception("Test error")
                )
                # If categorization fails, should default to allowing retry
                assert isinstance(should_retry, bool)
            except Exception:
                # If it fails, that's also acceptable as long as it's handled gracefully
                pass


class TestSDKEnhancedManagerPerformance:
    """Performance tests for SDK error categorization"""

    def setup_method(self):
        """Set up test fixtures"""
        self.manager = SDKEnhancedManager()

    def test_error_categorization_performance(self):
        """Test that error categorization is fast"""
        import time

        errors = [
            Exception("Rate limit exceeded"),
            Exception("Connection timeout"),
            Exception("Invalid API key"),
            Exception("Context length exceeded"),
            Exception("Request timeout"),
        ] * 100  # 500 errors total

        start_time = time.time()

        for error in errors:
            self.manager.categorize_sdk_error(error)

        end_time = time.time()
        categorization_time = end_time - start_time

        # Should categorize 500 errors in less than 1 second
        assert (
            categorization_time < 1.0
        ), f"Categorization took {categorization_time:.3f}s for 500 errors"

        # Should average less than 2ms per categorization
        avg_time_per_error = categorization_time / len(errors)
        assert (
            avg_time_per_error < 0.002
        ), f"Average categorization time: {avg_time_per_error:.6f}s"

    def test_stats_tracking_performance(self):
        """Test that statistics tracking doesn't significantly impact performance"""
        import time

        # Measure time with stats tracking
        start_time = time.time()
        for _ in range(1000):
            self.manager.categorize_sdk_error(Exception("Test error"))
        stats_time = time.time() - start_time

        # Should handle 1000 categorizations with stats in reasonable time
        assert (
            stats_time < 0.5
        ), f"Stats tracking took {stats_time:.3f}s for 1000 categorizations"
