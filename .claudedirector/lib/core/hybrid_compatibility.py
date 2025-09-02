"""
Hybrid Database Compatibility Bridge - Phase 2A Implementation

Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
Enhanced by: MCP Sequential7 systematic migration approach
Status: Phase 2 Engine Consolidation - Hybrid Database Migration
Priority: P0 - BLOCKING (P0 feature dependencies)

This module provides a compatibility bridge that maps hybrid database manager
concepts to UnifiedDatabaseCoordinator, enabling zero-downtime P0 feature migration.

Key Features:
- Maps QueryType, WorkloadPattern, and DatabaseConfig from hybrid → unified
- Preserves existing API contracts for P0 features
- Provides performance monitoring and routing compatibility
- Enables gradual migration with fallback capability
- Zero functional regressions during transition

CRITICAL: All P0 features must continue working during migration
"""

from typing import Dict, List, Any, Optional
import time
from dataclasses import dataclass

try:
    import structlog

    logger = structlog.get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

# Import unified database system
try:
    from .unified_database import (
        get_unified_database_coordinator,
        UnifiedDatabaseCoordinator,
        QueryType as UnifiedQueryType,
        DatabaseConfig as UnifiedDatabaseConfig,
        DatabaseResult,
        QueryContext as UnifiedQueryContext,
    )

    UNIFIED_DB_AVAILABLE = True
except ImportError:
    UNIFIED_DB_AVAILABLE = False
    logger.warning("UnifiedDatabaseCoordinator not available, hybrid bridge disabled")

# Import hybrid database types for compatibility
try:
    from .database_types import (
        QueryType,
        WorkloadPattern,
        DatabaseConfig,
        QueryContext,
        DatabaseEngineBase,
    )

    HYBRID_TYPES_AVAILABLE = True
except ImportError:
    HYBRID_TYPES_AVAILABLE = False
    logger.warning(
        "Hybrid database types not available, bridge may have limited compatibility"
    )


@dataclass
class BridgePerformanceMetrics:
    """Performance metrics for bridge operations"""

    query_count: int = 0
    total_execution_time_ms: float = 0.0
    average_execution_time_ms: float = 0.0
    successful_queries: int = 0
    failed_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0


class HybridToUnifiedBridge:
    """
    Compatibility bridge that maps hybrid database calls to UnifiedDatabaseCoordinator.

    This class provides a migration path for P0 features that currently use
    HybridDatabaseEngine to gradually migrate to UnifiedDatabaseCoordinator
    while maintaining API compatibility and zero functional regressions.

    Design Principles:
    - Preserve all existing API contracts
    - Map similar concepts between hybrid and unified systems
    - Provide performance monitoring for migration validation
    - Enable gradual migration with comprehensive fallback
    """

    def __init__(self):
        """Initialize hybrid to unified bridge with performance monitoring"""
        self.logger = logger.bind(component="HybridToUnifiedBridge")
        self._metrics = BridgePerformanceMetrics()

        if UNIFIED_DB_AVAILABLE:
            try:
                self.unified_coordinator = get_unified_database_coordinator()
                self.logger.info(
                    "✅ HybridToUnifiedBridge initialized with UnifiedDatabaseCoordinator"
                )
            except Exception as e:
                self.unified_coordinator = None
                self.logger.error(
                    f"Failed to initialize UnifiedDatabaseCoordinator: {e}"
                )
        else:
            self.unified_coordinator = None
            self.logger.warning("UnifiedDatabaseCoordinator not available")

    def is_available(self) -> bool:
        """Check if the bridge is functional"""
        return UNIFIED_DB_AVAILABLE and self.unified_coordinator is not None

    def connect(self) -> bool:
        """
        Connect to unified database system (compatibility method).
        Maps to UnifiedDatabaseCoordinator initialization.
        """
        if not self.is_available():
            self.logger.warning("HybridToUnifiedBridge not available for connection")
            return False

        try:
            # Test connection through unified coordinator
            conn = self.unified_coordinator.get_connection()
            if conn:
                self.logger.info(
                    "✅ HybridToUnifiedBridge connected via UnifiedDatabaseCoordinator"
                )
                return True
        except Exception as e:
            self.logger.error(f"Bridge connection failed: {e}")
            return False

        return False

    def execute_query(
        self, query: str, context: Optional["QueryContext"] = None
    ) -> Dict[str, Any]:
        """
        Execute query via UnifiedDatabaseCoordinator with hybrid API compatibility.

        Args:
            query: SQL query or search request
            context: Hybrid QueryContext (will be mapped to unified format)

        Returns:
            Dict with results and performance metrics (hybrid API format)
        """
        start_time = time.time()

        try:
            if not self.is_available():
                raise Exception("HybridToUnifiedBridge not available")

            # Map hybrid context to unified context if provided
            unified_context = None
            if context and HYBRID_TYPES_AVAILABLE:
                unified_context = self._map_query_context(context)

            # Execute via unified coordinator
            result = self.unified_coordinator.execute_query(query, unified_context)

            # Map result to hybrid format
            execution_time_ms = (time.time() - start_time) * 1000
            hybrid_result = self._map_result_to_hybrid_format(result, execution_time_ms)

            # Update metrics
            self._update_metrics(execution_time_ms, success=True)

            self.logger.debug(
                f"Bridge query executed successfully in {execution_time_ms:.2f}ms"
            )
            return hybrid_result

        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            self._update_metrics(execution_time_ms, success=False)
            self.logger.error(
                f"Bridge query failed after {execution_time_ms:.2f}ms: {e}"
            )

            # Return hybrid-compatible error response
            return {
                "success": False,
                "error": str(e),
                "execution_time_ms": execution_time_ms,
                "results": [],
                "row_count": 0,
                "performance_metrics": {
                    "query_time": execution_time_ms,
                    "cache_hit": False,
                },
            }

    def _map_query_context(self, hybrid_context: "QueryContext") -> Dict[str, Any]:
        """Map hybrid QueryContext to unified format"""
        if not hybrid_context:
            return {}

        try:
            unified_context = {
                "query_type": (
                    hybrid_context.query_type.value
                    if hasattr(hybrid_context.query_type, "value")
                    else str(hybrid_context.query_type)
                ),
                "workload_pattern": (
                    hybrid_context.workload_pattern.value
                    if hasattr(hybrid_context.workload_pattern, "value")
                    else str(hybrid_context.workload_pattern)
                ),
                "priority": getattr(hybrid_context, "priority", "normal"),
                "cache_enabled": getattr(hybrid_context, "cache_enabled", True),
                "expected_result_size": getattr(
                    hybrid_context, "expected_result_size", 0
                ),
                "estimated_execution_time_ms": getattr(
                    hybrid_context, "estimated_execution_time_ms", 0
                ),
            }

            # Map additional context if available
            if hasattr(hybrid_context, "preferred_engine"):
                unified_context["preferred_strategy"] = hybrid_context.preferred_engine

            if hasattr(hybrid_context, "fallback_engines"):
                unified_context["fallback_strategies"] = hybrid_context.fallback_engines

            return unified_context

        except Exception as e:
            self.logger.warning(f"Failed to map hybrid context, using defaults: {e}")
            return {"query_type": "transactional", "priority": "normal"}

    def _map_result_to_hybrid_format(
        self, unified_result: Any, execution_time_ms: float
    ) -> Dict[str, Any]:
        """Map UnifiedDatabaseCoordinator result to hybrid API format"""
        try:
            # Handle DatabaseResult object
            if hasattr(unified_result, "success"):
                return {
                    "success": unified_result.success,
                    "results": getattr(unified_result, "data", []),
                    "row_count": getattr(unified_result, "row_count", 0),
                    "execution_time_ms": execution_time_ms,
                    "performance_metrics": {
                        "query_time": execution_time_ms,
                        "cache_hit": getattr(unified_result, "cache_hit", False),
                        "strategy_used": getattr(
                            unified_result, "strategy_used", "sqlite"
                        ),
                    },
                    "error": (
                        getattr(unified_result, "error_message", None)
                        if not unified_result.success
                        else None
                    ),
                }

            # Handle direct query results (list/dict)
            elif isinstance(unified_result, (list, dict)):
                results = (
                    unified_result
                    if isinstance(unified_result, list)
                    else [unified_result]
                )
                return {
                    "success": True,
                    "results": results,
                    "row_count": len(results),
                    "execution_time_ms": execution_time_ms,
                    "performance_metrics": {
                        "query_time": execution_time_ms,
                        "cache_hit": False,
                        "strategy_used": "sqlite",
                    },
                }

            # Fallback for unknown result types
            else:
                return {
                    "success": True,
                    "results": [unified_result] if unified_result is not None else [],
                    "row_count": 1 if unified_result is not None else 0,
                    "execution_time_ms": execution_time_ms,
                    "performance_metrics": {
                        "query_time": execution_time_ms,
                        "cache_hit": False,
                        "strategy_used": "sqlite",
                    },
                }

        except Exception as e:
            self.logger.error(f"Failed to map unified result to hybrid format: {e}")
            return {
                "success": False,
                "error": f"Result mapping error: {e}",
                "execution_time_ms": execution_time_ms,
                "results": [],
                "row_count": 0,
            }

    def _update_metrics(self, execution_time_ms: float, success: bool = True):
        """Update bridge performance metrics"""
        self._metrics.query_count += 1
        self._metrics.total_execution_time_ms += execution_time_ms

        if success:
            self._metrics.successful_queries += 1
        else:
            self._metrics.failed_queries += 1

        # Update average
        if self._metrics.query_count > 0:
            self._metrics.average_execution_time_ms = (
                self._metrics.total_execution_time_ms / self._metrics.query_count
            )

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get bridge performance metrics (hybrid API compatibility)"""
        return {
            "total_queries": self._metrics.query_count,
            "successful_queries": self._metrics.successful_queries,
            "failed_queries": self._metrics.failed_queries,
            "average_execution_time_ms": self._metrics.average_execution_time_ms,
            "total_execution_time_ms": self._metrics.total_execution_time_ms,
            "success_rate": (
                self._metrics.successful_queries / self._metrics.query_count
                if self._metrics.query_count > 0
                else 0.0
            ),
            "cache_hit_rate": (
                self._metrics.cache_hits / self._metrics.query_count
                if self._metrics.query_count > 0
                else 0.0
            ),
            "bridge_status": "active" if self.is_available() else "unavailable",
        }

    def health_check(self) -> bool:
        """Perform health check (hybrid API compatibility)"""
        try:
            if not self.is_available():
                return False

            # Test basic connectivity
            conn = self.unified_coordinator.get_connection()
            if not conn:
                return False

            # Test basic query execution
            test_result = self.execute_query("SELECT 1 as test_value")
            return test_result.get("success", False)

        except Exception as e:
            self.logger.error(f"Bridge health check failed: {e}")
            return False


# Convenience function for P0 features
def get_hybrid_bridge() -> HybridToUnifiedBridge:
    """Get the hybrid to unified database bridge instance"""
    return HybridToUnifiedBridge()


# Backward compatibility aliases for easier migration
HybridDatabaseEngine = HybridToUnifiedBridge  # Allows drop-in replacement


def create_hybrid_engine_replacement(
    config: Optional["DatabaseConfig"] = None,
) -> HybridToUnifiedBridge:
    """
    Create a replacement for HybridDatabaseEngine using the bridge.
    Provides API compatibility for P0 features during migration.
    """
    bridge = HybridToUnifiedBridge()

    if config:
        logger.info(
            f"Bridge initialized with config for engine type: {getattr(config, 'engine_type', 'unknown')}"
        )

    return bridge
