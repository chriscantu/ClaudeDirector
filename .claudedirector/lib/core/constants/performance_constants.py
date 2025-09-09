"""
Performance Constants for ClaudeDirector

Centralizes all performance-related constants to eliminate DRY violations
and provide single source of truth for performance thresholds.

Author: Martin | Platform Architecture
Phase: 9.2 - DRY Compliance Refactoring
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class UnifiedQueryType(Enum):
    """Unified query types across all performance managers"""
    EXECUTIVE_CRITICAL = "executive_critical"  # <100ms target
    STRATEGIC_STANDARD = "strategic_standard"  # <200ms target  
    ANALYSIS_COMPLEX = "analysis_complex"     # <500ms target
    BACKGROUND_TASK = "background_task"       # <2s target
    
    # Legacy compatibility
    ULTRA_FAST = "executive_critical"
    FAST = "strategic_standard"
    NORMAL = "analysis_complex"
    SLOW = "background_task"


@dataclass
class PerformanceConstants:
    """Centralized performance constants eliminating hard-coded values"""
    
    # Response Time Targets (milliseconds)
    EXECUTIVE_TARGET_MS: int = 100
    STRATEGIC_TARGET_MS: int = 200
    ANALYSIS_TARGET_MS: int = 500
    BACKGROUND_TARGET_MS: int = 2000
    
    # Warning Thresholds (80% of target)
    EXECUTIVE_WARNING_MS: int = 80
    STRATEGIC_WARNING_MS: int = 160
    ANALYSIS_WARNING_MS: int = 400
    BACKGROUND_WARNING_MS: int = 1500
    
    # SLA Targets (percentages)
    EXECUTIVE_SLA_PERCENTAGE: float = 95.0
    STRATEGIC_SLA_PERCENTAGE: float = 95.0
    ANALYSIS_SLA_PERCENTAGE: float = 90.0
    BACKGROUND_SLA_PERCENTAGE: float = 85.0
    
    # Memory Thresholds (MB)
    MEMORY_BASELINE_MB: int = 100
    MEMORY_WARNING_THRESHOLD: float = 1.2  # 20% over baseline
    MEMORY_PRESSURE_THRESHOLD: float = 1.3  # 30% over baseline
    MEMORY_EFFICIENCY_THRESHOLD: float = 80.0  # Minimum efficiency percentage
    
    # Cache Configuration
    DEFAULT_CACHE_MEMORY_MB: int = 20
    DEFAULT_RETENTION_HOURS: int = 24
    
    # Monitoring Configuration  
    DEFAULT_MONITORING_INTERVAL_SECONDS: int = 30
    PERFORMANCE_HISTORY_HOURS: int = 1  # 3600 seconds
    BASELINE_TEST_ITERATIONS: int = 10
    BASELINE_TEST_SLEEP_MS: float = 0.01
    
    # Conversion Constants
    MS_TO_SECONDS: float = 1000.0
    BYTES_TO_MB: int = 1024 * 1024


@dataclass 
class PerformanceThresholds:
    """Performance monitoring thresholds for alerting"""
    
    # Response time thresholds
    RESPONSE_TIME_WARNING_MS: int = 400
    RESPONSE_TIME_CRITICAL_MS: int = 800
    
    # Memory thresholds  
    MEMORY_WARNING_MB: int = 45
    MEMORY_CRITICAL_MB: int = 50
    
    # Cache performance thresholds
    CACHE_HIT_RATE_WARNING: float = 0.7
    CACHE_HIT_RATE_CRITICAL: float = 0.5
    
    # Error rate thresholds
    ERROR_RATE_WARNING: float = 0.01
    ERROR_RATE_CRITICAL: float = 0.05
    
    # Queue depth thresholds
    QUEUE_DEPTH_WARNING: int = 100
    QUEUE_DEPTH_CRITICAL: int = 500
    
    # Garbage collection thresholds
    GC_TIME_WARNING_MS: int = 100
    GC_TIME_CRITICAL_MS: int = 500


# Global instances for easy access
PERFORMANCE_CONSTANTS = PerformanceConstants()
PERFORMANCE_THRESHOLDS = PerformanceThresholds()


def get_performance_target(query_type: UnifiedQueryType) -> Dict[str, Any]:
    """Get performance target configuration for query type"""
    targets = {
        UnifiedQueryType.EXECUTIVE_CRITICAL: {
            "target_ms": PERFORMANCE_CONSTANTS.EXECUTIVE_TARGET_MS,
            "warning_ms": PERFORMANCE_CONSTANTS.EXECUTIVE_WARNING_MS,
            "sla_percentage": PERFORMANCE_CONSTANTS.EXECUTIVE_SLA_PERCENTAGE,
        },
        UnifiedQueryType.STRATEGIC_STANDARD: {
            "target_ms": PERFORMANCE_CONSTANTS.STRATEGIC_TARGET_MS,
            "warning_ms": PERFORMANCE_CONSTANTS.STRATEGIC_WARNING_MS,
            "sla_percentage": PERFORMANCE_CONSTANTS.STRATEGIC_SLA_PERCENTAGE,
        },
        UnifiedQueryType.ANALYSIS_COMPLEX: {
            "target_ms": PERFORMANCE_CONSTANTS.ANALYSIS_TARGET_MS,
            "warning_ms": PERFORMANCE_CONSTANTS.ANALYSIS_WARNING_MS,
            "sla_percentage": PERFORMANCE_CONSTANTS.ANALYSIS_SLA_PERCENTAGE,
        },
        UnifiedQueryType.BACKGROUND_TASK: {
            "target_ms": PERFORMANCE_CONSTANTS.BACKGROUND_TARGET_MS,
            "warning_ms": PERFORMANCE_CONSTANTS.BACKGROUND_WARNING_MS,
            "sla_percentage": PERFORMANCE_CONSTANTS.BACKGROUND_SLA_PERCENTAGE,
        },
    }
    return targets.get(query_type, targets[UnifiedQueryType.STRATEGIC_STANDARD])


def get_memory_thresholds() -> Dict[str, float]:
    """Get memory threshold configuration"""
    return {
        "baseline_mb": PERFORMANCE_CONSTANTS.MEMORY_BASELINE_MB,
        "warning_multiplier": PERFORMANCE_CONSTANTS.MEMORY_WARNING_THRESHOLD,
        "pressure_multiplier": PERFORMANCE_CONSTANTS.MEMORY_PRESSURE_THRESHOLD,
        "efficiency_threshold": PERFORMANCE_CONSTANTS.MEMORY_EFFICIENCY_THRESHOLD,
    }
