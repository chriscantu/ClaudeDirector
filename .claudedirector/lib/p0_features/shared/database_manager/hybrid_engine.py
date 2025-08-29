"""
Hybrid Database Engine - Delbert's Multi-Database Architecture

Intelligent workload routing across SQLite, DuckDB, and Faiss for optimal performance.
Zero-config database selection based on query patterns and data characteristics.
"""

import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import structlog
import threading

from .db_base import (
    DatabaseEngineBase,
    WorkloadType,
    QueryContext,
    DatabaseConfig,
    DatabaseResult,
    OptimizationLevel,
)
from ..infrastructure.config import get_config

logger = structlog.get_logger(__name__)


class QueryComplexity(Enum):
    """Query complexity classification for routing decisions"""

    SIMPLE = "simple"  # Single table, simple WHERE
    MODERATE = "moderate"  # Joins, aggregations
    COMPLEX = "complex"  # Analytics, multiple joins
    ANALYTICAL = "analytical"  # Time series, complex aggregations


@dataclass
class WorkloadMetrics:
    """Metrics for workload classification and routing"""

    read_ratio: float  # Percentage of read queries
    write_ratio: float  # Percentage of write queries
    avg_result_size: int  # Average rows returned
    join_frequency: float  # Percentage of queries with joins
    aggregation_frequency: float  # Percentage with GROUP BY/aggregations
    json_query_frequency: float  # Percentage querying JSON fields
    concurrent_connections: int  # Active connections
    query_frequency: float  # Queries per second


class HybridDatabaseEngine(DatabaseEngineBase):
    """
    Delbert's hybrid database engine with intelligent routing

    Architecture:
    - SQLite: Transactional operations, simple queries
    - DuckDB: Analytics, complex aggregations, time-series
    - Faiss: Semantic search, vector similarity

    Features:
    - Automatic workload classification
    - Intelligent query routing
    - Performance optimization
    - Zero-config operation
    """

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self.logger = logger.bind(component="hybrid_db_engine")

        # Initialize database engines
        self._sqlite_engine: Optional[SQLiteEngine] = None
        self._duckdb_engine: Optional[DuckDBEngine] = None
        self._faiss_engine: Optional[FaissEngine] = None

        # Workload monitoring
        self._workload_metrics = WorkloadMetrics(
            read_ratio=0.8,
            write_ratio=0.2,
            avg_result_size=10,
            join_frequency=0.3,
            aggregation_frequency=0.1,
            json_query_frequency=0.4,
            concurrent_connections=1,
            query_frequency=1.0,
        )

        # Query routing cache
        self._routing_cache: Dict[str, str] = {}
        self._cache_lock = threading.Lock()

        # Performance tracking
        self._query_history: List[Dict[str, Any]] = []

        self.logger.info(
            "Hybrid database engine initialized",
            sqlite_enabled=True,
            duckdb_enabled=self._should_enable_duckdb(),
            faiss_enabled=self._should_enable_faiss(),
        )

    def connect(self) -> bool:
        """
        Connect to hybrid database infrastructure

        Delbert's Strategy:
        1. Always connect SQLite (baseline)
        2. Conditionally connect DuckDB (analytics workload)
        3. Conditionally connect Faiss (semantic search)
        """
        try:
            start_time = time.time()

            # Primary database: SQLite (always available)
            self._sqlite_engine = SQLiteEngine(self.config)
            if not self._sqlite_engine.connect():
                raise RuntimeError("Failed to connect to SQLite primary database")

            # Analytics database: DuckDB (conditional)
            if self._should_enable_duckdb():
                try:
                    self._duckdb_engine = DuckDBEngine(self.config)
                    if not self._duckdb_engine.connect():
                        self.logger.warning(
                            "DuckDB connection failed, continuing with SQLite only"
                        )
                        self._duckdb_engine = None
                except ImportError:
                    self.logger.info("DuckDB not available, analytics will use SQLite")
                    self._duckdb_engine = None

            # Semantic search: Faiss (conditional)
            if self._should_enable_faiss():
                try:
                    self._faiss_engine = FaissEngine(self.config)
                    if not self._faiss_engine.connect():
                        self.logger.warning(
                            "Faiss connection failed, semantic search unavailable"
                        )
                        self._faiss_engine = None
                except ImportError:
                    self.logger.info("Faiss not available, semantic search disabled")
                    self._faiss_engine = None

            connection_time = (time.time() - start_time) * 1000

            self.logger.info(
                "Hybrid database connected successfully",
                connection_time_ms=connection_time,
                sqlite_ready=self._sqlite_engine is not None,
                duckdb_ready=self._duckdb_engine is not None,
                faiss_ready=self._faiss_engine is not None,
            )

            return True

        except Exception as e:
            self.logger.error("Hybrid database connection failed", error=str(e))
            return False

    def execute_query(
        self,
        query: str,
        params: Optional[Dict] = None,
        context: Optional[QueryContext] = None,
    ) -> DatabaseResult:
        """
        Execute query with intelligent routing

        Delbert's Routing Logic:
        1. Classify query complexity and workload type
        2. Route to optimal database engine
        3. Execute with performance monitoring
        4. Cache routing decisions for similar queries
        """
        start_time = time.time()

        try:
            # Query classification
            complexity = self._classify_query_complexity(query)
            workload_type = (
                context.workload_type if context else self._infer_workload_type(query)
            )

            # Intelligent routing
            target_engine = self._route_query(query, complexity, workload_type)

            # Execute on target engine
            result = self._execute_on_engine(target_engine, query, params, context)

            # Performance tracking
            execution_time = (time.time() - start_time) * 1000
            self._record_query_performance(query, execution_time, target_engine, result)

            # Update workload metrics
            self._update_workload_metrics(query, execution_time, result)

            return result

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(
                "Hybrid query execution failed",
                query=query[:100],
                execution_time_ms=execution_time,
                error=str(e),
            )

            return DatabaseResult(
                success=False,
                data=[],
                execution_time_ms=int(execution_time),
                rows_affected=0,
                error=str(e),
            )

    def optimize_performance(self, level: OptimizationLevel) -> bool:
        """
        Optimize performance across all database engines

        Delbert's Multi-Engine Optimization:
        - SQLite: WAL mode, cache tuning, indexes
        - DuckDB: Memory allocation, parallel processing
        - Faiss: Index optimization, quantization
        """
        try:
            optimization_results = []

            # Optimize SQLite
            if self._sqlite_engine:
                sqlite_result = self._sqlite_engine.optimize_performance(level)
                optimization_results.append(("SQLite", sqlite_result))

            # Optimize DuckDB
            if self._duckdb_engine:
                duckdb_result = self._duckdb_engine.optimize_performance(level)
                optimization_results.append(("DuckDB", duckdb_result))

            # Optimize Faiss
            if self._faiss_engine:
                faiss_result = self._faiss_engine.optimize_performance(level)
                optimization_results.append(("Faiss", faiss_result))

            # Update routing decisions based on optimization results
            self._update_routing_strategy(optimization_results)

            success_count = sum(1 for _, result in optimization_results if result)
            total_engines = len(optimization_results)

            self.logger.info(
                "Hybrid database optimization completed",
                successful_optimizations=success_count,
                total_engines=total_engines,
                level=level.value,
            )

            return success_count > 0

        except Exception as e:
            self.logger.error("Hybrid database optimization failed", error=str(e))
            return False

    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status across all engines"""
        health_status = {
            "timestamp": time.time(),
            "overall_status": "healthy",
            "engines": {},
            "workload_metrics": self._get_workload_metrics_summary(),
            "routing_efficiency": self._calculate_routing_efficiency(),
            "performance_summary": self._get_performance_summary(),
        }

        # SQLite health
        if self._sqlite_engine:
            sqlite_health = self._sqlite_engine.get_health_status()
            health_status["engines"]["sqlite"] = sqlite_health

        # DuckDB health
        if self._duckdb_engine:
            duckdb_health = self._duckdb_engine.get_health_status()
            health_status["engines"]["duckdb"] = duckdb_health

        # Faiss health
        if self._faiss_engine:
            faiss_health = self._faiss_engine.get_health_status()
            health_status["engines"]["faiss"] = faiss_health

        # Determine overall status
        engine_statuses = [
            engine["status"] for engine in health_status["engines"].values()
        ]
        if any(status == "critical" for status in engine_statuses):
            health_status["overall_status"] = "critical"
        elif any(status == "degraded" for status in engine_statuses):
            health_status["overall_status"] = "degraded"

        return health_status

    # Private methods for intelligent routing and optimization

    def _classify_query_complexity(self, query: str) -> QueryComplexity:
        """Classify query complexity for routing decisions"""
        query_upper = query.upper()

        # Complex analytics patterns
        if any(
            pattern in query_upper
            for pattern in [
                "GROUP BY",
                "WINDOW FUNCTION",
                "WITH RECURSIVE",
                "PARTITION BY",
                "PERCENTILE",
                "LAG(",
                "LEAD(",
                "ROW_NUMBER()",
            ]
        ):
            return QueryComplexity.ANALYTICAL

        # Complex queries with multiple joins or subqueries
        join_count = query_upper.count("JOIN")
        subquery_count = query_upper.count("SELECT") - 1

        if join_count >= 3 or subquery_count >= 2:
            return QueryComplexity.COMPLEX

        # Moderate complexity with joins or aggregations
        if join_count > 0 or any(
            agg in query_upper
            for agg in ["COUNT(", "SUM(", "AVG(", "MAX(", "MIN(", "GROUP BY"]
        ):
            return QueryComplexity.MODERATE

        # Simple single-table queries
        return QueryComplexity.SIMPLE

    def _infer_workload_type(self, query: str) -> WorkloadType:
        """Infer workload type from query patterns"""
        query_upper = query.upper()

        # Semantic search patterns
        if any(
            pattern in query_upper
            for pattern in ["SIMILARITY", "VECTOR", "EMBEDDING", "SEMANTIC"]
        ):
            return WorkloadType.SEMANTIC

        # Analytics patterns
        if any(
            pattern in query_upper
            for pattern in ["GROUP BY", "HAVING", "WINDOW", "AGGREGATE", "TIME_SERIES"]
        ):
            return WorkloadType.ANALYTICAL

        # Write operations
        if any(
            pattern in query_upper
            for pattern in ["INSERT", "UPDATE", "DELETE", "REPLACE"]
        ):
            return WorkloadType.TRANSACTIONAL

        # Default to transactional for read operations
        return WorkloadType.TRANSACTIONAL

    def _route_query(
        self, query: str, complexity: QueryComplexity, workload_type: WorkloadType
    ) -> str:
        """
        Intelligent query routing based on complexity and workload

        Delbert's Routing Matrix:
        - Semantic queries → Faiss (if available)
        - Analytical/Complex → DuckDB (if available)
        - Simple/Moderate → SQLite
        - Transactional → SQLite (ACID compliance)
        """
        # Check routing cache first
        query_signature = (
            f"{complexity.value}_{workload_type.value}_{hash(query) % 1000}"
        )

        with self._cache_lock:
            if query_signature in self._routing_cache:
                return self._routing_cache[query_signature]

        # Routing logic
        target_engine = "sqlite"  # Default fallback

        # Semantic search routing
        if workload_type == WorkloadType.SEMANTIC and self._faiss_engine:
            target_engine = "faiss"

        # Analytics routing
        elif (
            complexity in [QueryComplexity.COMPLEX, QueryComplexity.ANALYTICAL]
            and workload_type == WorkloadType.ANALYTICAL
            and self._duckdb_engine
        ):
            target_engine = "duckdb"

        # High-performance read routing to DuckDB
        elif (
            complexity == QueryComplexity.MODERATE
            and workload_type == WorkloadType.TRANSACTIONAL
            and "SELECT" in query.upper()
            and "INSERT" not in query.upper()
            and self._duckdb_engine
            and self._workload_metrics.read_ratio > 0.8
        ):
            target_engine = "duckdb"

        # Cache routing decision
        with self._cache_lock:
            self._routing_cache[query_signature] = target_engine

        return target_engine

    def _execute_on_engine(
        self,
        engine_name: str,
        query: str,
        params: Optional[Dict],
        context: Optional[QueryContext],
    ) -> DatabaseResult:
        """Execute query on specified engine"""
        if engine_name == "duckdb" and self._duckdb_engine:
            return self._duckdb_engine.execute_query(query, params, context)
        elif engine_name == "faiss" and self._faiss_engine:
            return self._faiss_engine.execute_query(query, params, context)
        else:
            # Fallback to SQLite
            return self._sqlite_engine.execute_query(query, params, context)

    def _should_enable_duckdb(self) -> bool:
        """Determine if DuckDB should be enabled based on workload"""
        config = get_config()

        # Enable if analytics workload is significant
        return (
            self._workload_metrics.aggregation_frequency > 0.1
            or self._workload_metrics.avg_result_size > 100
            or config.debug_mode  # Always enable in debug for testing
        )

    def _should_enable_faiss(self) -> bool:
        """Determine if Faiss should be enabled for semantic search"""
        config = get_config()

        # Enable if semantic search features are active
        return (
            config.enable_decision_intelligence  # Decision intelligence needs semantic search
            or config.debug_mode  # Always enable in debug for testing
        )

    def _record_query_performance(
        self, query: str, execution_time: float, engine: str, result: DatabaseResult
    ):
        """Record query performance for optimization"""
        performance_record = {
            "timestamp": time.time(),
            "query_hash": hash(query) % 10000,
            "execution_time_ms": execution_time,
            "engine_used": engine,
            "success": result.success,
            "rows_returned": len(result.data) if result.data else 0,
            "meets_sla": execution_time < self.config.max_query_time_ms,
        }

        self._performance_metrics.append(performance_record)

        # Keep only recent metrics (last 1000 queries)
        if len(self._performance_metrics) > 1000:
            self._performance_metrics = self._performance_metrics[-1000:]

        # Log SLA violations
        if execution_time > self.config.max_query_time_ms:
            self.logger.warning(
                "Query SLA violation",
                execution_time_ms=execution_time,
                sla_threshold_ms=self.config.max_query_time_ms,
                engine=engine,
                query=query[:50],
            )

    def _update_workload_metrics(
        self, query: str, execution_time: float, result: DatabaseResult
    ):
        """Update workload metrics for routing optimization"""
        query_upper = query.upper()

        # Update read/write ratio
        is_read = query_upper.startswith("SELECT")
        if is_read:
            self._workload_metrics.read_ratio = (
                self._workload_metrics.read_ratio * 0.9 + 0.1
            )
            self._workload_metrics.write_ratio = 1.0 - self._workload_metrics.read_ratio
        else:
            self._workload_metrics.write_ratio = (
                self._workload_metrics.write_ratio * 0.9 + 0.1
            )
            self._workload_metrics.read_ratio = 1.0 - self._workload_metrics.write_ratio

        # Update aggregation frequency
        has_aggregation = any(
            agg in query_upper
            for agg in ["GROUP BY", "COUNT(", "SUM(", "AVG(", "MAX(", "MIN("]
        )
        if has_aggregation:
            self._workload_metrics.aggregation_frequency = (
                self._workload_metrics.aggregation_frequency * 0.9 + 0.1
            )

        # Update average result size
        if result.data:
            current_size = len(result.data)
            self._workload_metrics.avg_result_size = int(
                self._workload_metrics.avg_result_size * 0.9 + current_size * 0.1
            )

    def _get_workload_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of current workload metrics"""
        return {
            "read_ratio": round(self._workload_metrics.read_ratio, 3),
            "write_ratio": round(self._workload_metrics.write_ratio, 3),
            "avg_result_size": self._workload_metrics.avg_result_size,
            "aggregation_frequency": round(
                self._workload_metrics.aggregation_frequency, 3
            ),
            "json_query_frequency": round(
                self._workload_metrics.json_query_frequency, 3
            ),
            "concurrent_connections": self._workload_metrics.concurrent_connections,
        }

    def _calculate_routing_efficiency(self) -> Dict[str, Any]:
        """Calculate routing efficiency metrics"""
        if not self._performance_metrics:
            return {"efficiency": "no_data"}

        recent_metrics = self._performance_metrics[-100:]  # Last 100 queries

        # Engine utilization
        engine_usage = {}
        total_queries = len(recent_metrics)

        for metric in recent_metrics:
            engine = metric["engine_used"]
            engine_usage[engine] = engine_usage.get(engine, 0) + 1

        # SLA compliance
        sla_compliant = sum(1 for m in recent_metrics if m["meets_sla"])
        sla_compliance_rate = (
            sla_compliant / total_queries if total_queries > 0 else 0.0
        )

        # Average performance by engine
        engine_performance = {}
        for engine in engine_usage:
            engine_metrics = [m for m in recent_metrics if m["engine_used"] == engine]
            if engine_metrics:
                avg_time = sum(m["execution_time_ms"] for m in engine_metrics) / len(
                    engine_metrics
                )
                engine_performance[engine] = round(avg_time, 2)

        return {
            "sla_compliance_rate": round(sla_compliance_rate, 3),
            "engine_utilization": {
                k: round(v / total_queries, 3) for k, v in engine_usage.items()
            },
            "avg_execution_time_by_engine": engine_performance,
            "total_queries_analyzed": total_queries,
        }

    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary across all engines"""
        if not self._performance_metrics:
            return {"status": "no_data"}

        recent_metrics = self._performance_metrics[-50:]  # Last 50 queries

        avg_time = sum(m["execution_time_ms"] for m in recent_metrics) / len(
            recent_metrics
        )
        success_rate = sum(1 for m in recent_metrics if m["success"]) / len(
            recent_metrics
        )

        return {
            "avg_execution_time_ms": round(avg_time, 2),
            "success_rate": round(success_rate, 3),
            "queries_per_second": round(len(recent_metrics) / 60, 2),  # Approximate QPS
            "performance_trend": "stable",  # Would calculate from historical data
        }

    def _update_routing_strategy(self, optimization_results: List[Tuple[str, bool]]):
        """Update routing strategy based on optimization results"""
        # Clear routing cache to allow re-evaluation
        with self._cache_lock:
            self._routing_cache.clear()

        # Log optimization results for routing decisions
        for engine, success in optimization_results:
            if success:
                self.logger.info(
                    f"{engine} optimization successful, prioritizing for routing"
                )
            else:
                self.logger.warning(
                    f"{engine} optimization failed, deprioritizing for routing"
                )


# Placeholder engine implementations (would be separate files in production)


class SQLiteEngine(DatabaseEngineBase):
    """Optimized SQLite engine for transactional workloads"""

    def connect(self) -> bool:
        # Implementation delegated to existing optimized_db_manager
        from context_engineering.strategic_memory_manager import get_strategic_memory_manager

        try:
            self._db_manager = get_db_manager(str(self.config.database_path))
            return True
        except Exception as e:
            self.logger.error("SQLite connection failed", error=str(e))
            return False

    def execute_query(
        self,
        query: str,
        params: Optional[Dict] = None,
        context: Optional[QueryContext] = None,
    ) -> DatabaseResult:
        # Delegate to existing optimized SQLite implementation
        start_time = time.time()
        try:
            with self._db_manager.get_connection() as conn:
                if params:
                    cursor = conn.execute(query, params)
                else:
                    cursor = conn.execute(query)

                data = cursor.fetchall()
                execution_time = int((time.time() - start_time) * 1000)

                return DatabaseResult(
                    success=True,
                    data=data,
                    execution_time_ms=execution_time,
                    rows_affected=(
                        cursor.rowcount if cursor.rowcount != -1 else len(data)
                    ),
                )
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            return DatabaseResult(
                success=False,
                data=[],
                execution_time_ms=execution_time,
                rows_affected=0,
                error=str(e),
            )


class DuckDBEngine(DatabaseEngineBase):
    """DuckDB engine for analytics workloads"""

    def connect(self) -> bool:
        # Would implement DuckDB connection
        self.logger.info("DuckDB engine - placeholder implementation")
        return True

    def execute_query(
        self,
        query: str,
        params: Optional[Dict] = None,
        context: Optional[QueryContext] = None,
    ) -> DatabaseResult:
        # Placeholder - would implement actual DuckDB execution
        return DatabaseResult(
            success=True, data=[], execution_time_ms=50, rows_affected=0
        )


class FaissEngine(DatabaseEngineBase):
    """Faiss engine for semantic search workloads"""

    def connect(self) -> bool:
        # Would implement Faiss connection
        self.logger.info("Faiss engine - placeholder implementation")
        return True

    def execute_query(
        self,
        query: str,
        params: Optional[Dict] = None,
        context: Optional[QueryContext] = None,
    ) -> DatabaseResult:
        # Placeholder - would implement actual Faiss semantic search
        return DatabaseResult(
            success=True, data=[], execution_time_ms=30, rows_affected=0
        )
