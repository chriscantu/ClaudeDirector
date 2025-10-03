"""
Performance Component-Specific Test Fixtures

🏗️ Martin | Platform Architecture - Performance Test Support

Fixtures specific to performance components (caching, optimization,
monitoring).

EXTENDS: .claudedirector/tests/unit/conftest.py (root fixtures)
SCOPE: Performance component testing
"""

import pytest
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any


# ============================================================================
# CACHE FIXTURES
# ============================================================================


@pytest.fixture
def sample_cache_config():
    """
    Sample cache configuration for testing.
    """
    return {
        "max_memory_mb": 100,
        "max_entries": 1000,
        "default_ttl_seconds": 3600,
        "performance_threshold_ms": 100,
        "cleanup_interval_seconds": 300,
        "enable_metrics": True,
    }


@pytest.fixture
def mock_prompt_cache_optimizer():
    """
    Mock SDK-inspired prompt cache optimizer.
    """
    mock = Mock()

    # Cache operations
    mock.get_cached_segment = Mock(return_value=None)
    mock.cache_segment = Mock()
    mock.invalidate_segment = Mock()

    # Performance tracking
    mock.get_cache_stats = Mock(
        return_value={
            "hits": 150,
            "misses": 30,
            "hit_rate": 0.833,
            "total_latency_saved_ms": 4500.0,
            "memory_usage_mb": 25.3,
        }
    )

    # Optimization
    mock.optimize_prompt = Mock(
        return_value={
            "original_tokens": 1500,
            "cached_tokens": 1200,
            "cache_efficiency": 0.80,
            "estimated_cost_savings": 0.30,
        }
    )

    return mock


# ============================================================================
# PERFORMANCE MONITORING FIXTURES
# ============================================================================


@pytest.fixture
def mock_performance_monitor():
    """
    Mock performance monitor for real-time tracking.
    """
    mock = Mock()

    # Metrics recording
    mock.record_latency = Mock()
    mock.record_throughput = Mock()
    mock.record_error = Mock()

    # Metrics retrieval
    mock.get_metrics = Mock(
        return_value={
            "avg_latency_ms": 125.5,
            "p95_latency_ms": 250.0,
            "p99_latency_ms": 450.0,
            "throughput_rps": 45.2,
            "error_rate": 0.005,
        }
    )

    # Alerting
    mock.check_thresholds = Mock(
        return_value={
            "violations": [],
            "status": "healthy",
        }
    )

    return mock


# ============================================================================
# RESPONSE OPTIMIZATION FIXTURES
# ============================================================================


@pytest.fixture
def mock_response_optimizer():
    """
    Mock response optimizer for priority-based optimization.
    """
    mock = Mock()

    # Response optimization
    mock.optimize_response = AsyncMock(
        return_value={
            "original_size": 5000,
            "optimized_size": 3500,
            "compression_ratio": 0.70,
            "optimization_time_ms": 15.0,
        }
    )

    # Priority queue
    mock.prioritize_request = Mock(
        return_value={
            "priority": "HIGH",
            "queue_position": 2,
            "estimated_wait_ms": 50.0,
        }
    )

    return mock


# ============================================================================
# SAMPLE PERFORMANCE DATA
# ============================================================================


@pytest.fixture
def sample_performance_metrics():
    """
    Sample performance metrics for testing.
    """
    return {
        "timestamp": "2025-10-03T00:00:00Z",
        "component": "decision_orchestrator",
        "metrics": {
            "latency_ms": {
                "min": 50.0,
                "max": 450.0,
                "avg": 125.5,
                "p50": 100.0,
                "p95": 250.0,
                "p99": 450.0,
            },
            "throughput": {
                "requests_per_second": 45.2,
                "successful_requests": 4500,
                "failed_requests": 23,
            },
            "resources": {
                "cpu_percent": 35.2,
                "memory_mb": 256.8,
                "cache_hit_rate": 0.833,
            },
        },
    }
