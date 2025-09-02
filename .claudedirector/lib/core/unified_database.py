"""
Unified Database Interface - Phase 1 Implementation

Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
Story: 1.1 Database Architecture Unification
Priority: P0 - BLOCKING

This module provides the unified database interface that consolidates:
- core/database.py (DatabaseManager)
- p0_features/shared/database_manager/* (Hybrid engines)
- 293 scattered SQLite operations across 21 files

Key Features:
- Strategy pattern for SQLite/DuckDB/Faiss routing
- Thread-safe connection pooling
- Dependency injection support
- Performance monitoring and SLA enforcement
- Data preservation guarantee

CRITICAL: All existing database functionality must be preserved
"""

import sqlite3
import threading
import time
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Union

try:
    import structlog

    logger = structlog.get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

# Import existing types and configs for compatibility
try:
    from .database_types import (
        QueryType,
        WorkloadPattern,
        DatabaseConfig,
        QueryContext,
        DatabaseResult,
        DatabaseEngineBase,
    )
except ImportError:
    # Fallback definitions if P0 features not available
    from enum import Enum
    from dataclasses import dataclass
    from typing import Optional, Any, List

    class QueryType(Enum):
        TRANSACTIONAL = "transactional"
        ANALYTICAL = "analytical"
        SEMANTIC = "semantic"
        MIXED = "mixed"

    class WorkloadPattern(Enum):
        OLTP = "oltp"
        OLAP = "olap"
        VECTOR_SEARCH = "vector_search"
        HYBRID = "hybrid"

    @dataclass
    class DatabaseConfig:
        engine_type: str
        database_path: Path
        max_query_time_ms: int = 200
        cache_size_mb: int = 100
        connection_pool_size: int = 10
        sqlite_config: Optional[Dict[str, Any]] = None
        duckdb_config: Optional[Dict[str, Any]] = None
        faiss_config: Optional[Dict[str, Any]] = None

    @dataclass
    class QueryContext:
        query_type: QueryType
        workload_pattern: WorkloadPattern
        expected_result_size: int = 0
        priority: str = "normal"
        cache_enabled: bool = True
        preferred_engine: Optional[str] = None

    @dataclass
    class DatabaseResult:
        success: bool
        data: Any = None
        columns: List[str] = None
        execution_time_ms: float = 0.0
        error: Optional[str] = None
        engine: str = "unknown"
        strategy_used: Optional[str] = None
        query_type: Optional[str] = None


try:
    from core.config import get_config
except ImportError:
    from .config import get_config

try:
    from core.exceptions import DatabaseError
except ImportError:
    try:
        from .exceptions import DatabaseError
    except ImportError:

        class DatabaseError(Exception):
            def __init__(self, message: str, db_path: str = ""):
                super().__init__(message)
                self.db_path = db_path


class DatabaseStrategy(ABC):
    """
    Abstract base class for database strategies following Open/Closed Principle.
    Each strategy handles a specific database engine (SQLite, DuckDB, Faiss).
    """

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.logger = structlog.get_logger(f"{self.__class__.__name__}")
        self._connection_pool = {}
        self._pool_lock = threading.Lock()

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the database engine"""
        pass

    @abstractmethod
    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        context: Optional[QueryContext] = None,
    ) -> DatabaseResult:
        """Execute query with performance monitoring"""
        pass

    @abstractmethod
    def execute_transaction(self, operations: List[Dict[str, Any]]) -> DatabaseResult:
        """Execute multiple operations in a transaction"""
        pass

    @abstractmethod
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for monitoring"""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the database strategy is healthy"""
        pass

    def close_connections(self):
        """Close all connections in the pool"""
        with self._pool_lock:
            for conn in self._connection_pool.values():
                try:
                    conn.close()
                except Exception as e:
                    self.logger.warning(f"Error closing connection: {e}")
            self._connection_pool.clear()


class SQLiteStrategy(DatabaseStrategy):
    """
    SQLite strategy for transactional workloads (OLTP).
    Preserves all existing DatabaseManager functionality.
    """

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self._local = threading.local()
        self._initialized = False

    def connect(self) -> bool:
        """Connect to SQLite database with existing optimizations"""
        try:
            # Ensure database directory exists (preserve existing behavior)
            self.config.database_path.parent.mkdir(parents=True, exist_ok=True)

            # Test connection
            conn = sqlite3.connect(
                str(self.config.database_path), check_same_thread=False, timeout=30.0
            )

            # Apply existing optimizations from DatabaseManager
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")

            # Apply config-specific optimizations
            if self.config.sqlite_config:
                for pragma, value in self.config.sqlite_config.items():
                    if pragma != "journal_mode":  # Already set
                        conn.execute(f"PRAGMA {pragma} = {value}")

            conn.close()
            self._initialized = True
            self.logger.info(
                "SQLite strategy initialized", db_path=str(self.config.database_path)
            )
            return True

        except Exception as e:
            self.logger.error(f"SQLite connection failed: {e}")
            return False

    def get_connection(self) -> sqlite3.Connection:
        """
        Get thread-local SQLite connection (preserves DatabaseManager pattern).
        Each thread gets its own connection for thread safety.
        """
        if not hasattr(self._local, "connection") or self._local.connection is None:
            try:
                self._local.connection = sqlite3.connect(
                    str(self.config.database_path),
                    check_same_thread=False,
                    timeout=30.0,
                )

                # Apply all existing optimizations
                self._local.connection.execute("PRAGMA foreign_keys = ON")
                self._local.connection.execute("PRAGMA journal_mode = WAL")
                self._local.connection.execute("PRAGMA synchronous = NORMAL")

                # Apply additional config optimizations
                if self.config.sqlite_config:
                    for pragma, value in self.config.sqlite_config.items():
                        if pragma not in [
                            "journal_mode",
                            "synchronous",
                            "foreign_keys",
                        ]:
                            self._local.connection.execute(f"PRAGMA {pragma} = {value}")

            except Exception as e:
                raise DatabaseError(
                    f"Failed to connect to SQLite database: {e}",
                    db_path=str(self.config.database_path),
                )

        return self._local.connection

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor (preserves DatabaseManager pattern)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(
                f"SQLite operation failed: {e}", db_path=str(self.config.database_path)
            )
        finally:
            cursor.close()

    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        context: Optional[QueryContext] = None,
    ) -> DatabaseResult:
        """Execute SQLite query with performance monitoring"""
        start_time = time.time()

        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                # Handle different query types
                if query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                else:
                    results = cursor.rowcount
                    columns = []

                execution_time = (time.time() - start_time) * 1000  # ms

                # Performance SLA check
                if execution_time > self.config.max_query_time_ms:
                    self.logger.warning(
                        f"Query exceeded SLA: {execution_time:.2f}ms > {self.config.max_query_time_ms}ms"
                    )

                return DatabaseResult(
                    success=True,
                    data=results,
                    columns=columns,
                    execution_time_ms=execution_time,
                    engine="sqlite",
                )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"SQLite query failed: {e}", query=query[:100])

            return DatabaseResult(
                success=False,
                data=None,
                columns=[],
                execution_time_ms=execution_time,
                error=str(e),
                engine="sqlite",
            )

    def execute_transaction(self, operations: List[Dict[str, Any]]) -> DatabaseResult:
        """Execute multiple SQLite operations in a transaction"""
        start_time = time.time()

        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Begin explicit transaction
            cursor.execute("BEGIN")

            results = []
            for op in operations:
                query = op.get("query", "")
                params = op.get("params", {})

                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if query.strip().upper().startswith("SELECT"):
                    results.append(cursor.fetchall())
                else:
                    results.append(cursor.rowcount)

            conn.commit()
            execution_time = (time.time() - start_time) * 1000

            return DatabaseResult(
                success=True,
                data=results,
                columns=[],
                execution_time_ms=execution_time,
                engine="sqlite",
            )

        except Exception as e:
            conn.rollback()
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"SQLite transaction failed: {e}")

            return DatabaseResult(
                success=False,
                data=None,
                columns=[],
                execution_time_ms=execution_time,
                error=str(e),
                engine="sqlite",
            )
        finally:
            cursor.close()

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get SQLite performance metrics"""
        try:
            with self.get_cursor() as cursor:
                # Get basic database stats
                cursor.execute("PRAGMA page_count")
                page_count = cursor.fetchone()[0]

                cursor.execute("PRAGMA page_size")
                page_size = cursor.fetchone()[0]

                cursor.execute("PRAGMA cache_size")
                cache_size = cursor.fetchone()[0]

                return {
                    "engine": "sqlite",
                    "database_size_mb": (page_count * page_size) / (1024 * 1024),
                    "page_count": page_count,
                    "page_size": page_size,
                    "cache_size": cache_size,
                    "connection_count": len(self._connection_pool),
                    "health": "healthy",
                }

        except Exception as e:
            self.logger.error(f"Failed to get SQLite metrics: {e}")
            return {"engine": "sqlite", "health": "error", "error": str(e)}

    def health_check(self) -> bool:
        """Check SQLite database health"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception:
            return False


class UnifiedDatabaseCoordinator:
    """
    Unified database coordinator that routes queries to appropriate strategies.

    This class consolidates:
    - DatabaseManager singleton pattern and functionality
    - Hybrid database routing from p0_features/shared/database_manager/
    - Strategy selection based on workload patterns
    - Performance monitoring and SLA enforcement

    Key principles:
    - Single Responsibility: Database coordination and routing
    - Open/Closed: Extensible via strategy pattern
    - Dependency Inversion: Depends on DatabaseStrategy abstractions
    """

    def __init__(self, dependency_container=None):
        self.logger = structlog.get_logger("UnifiedDatabaseCoordinator")
        self.strategies: Dict[str, DatabaseStrategy] = {}
        self._default_strategy = "sqlite"
        self._routing_rules = self._setup_routing_rules()

        # Initialize with default SQLite strategy (preserve existing behavior)
        self._initialize_default_strategies()

        self.logger.info(
            "UnifiedDatabaseCoordinator initialized with data preservation"
        )

    def _setup_routing_rules(self) -> Dict[QueryType, str]:
        """Setup intelligent query routing rules"""
        return {
            QueryType.TRANSACTIONAL: "sqlite",
            QueryType.ANALYTICAL: "duckdb",  # Future implementation
            QueryType.SEMANTIC: "faiss",  # Future implementation
            QueryType.MIXED: "sqlite",  # Default to SQLite for mixed
        }

    def _initialize_default_strategies(self):
        """Initialize default SQLite strategy to preserve existing functionality"""
        try:
            config = get_config()

            # Create SQLite config preserving existing DatabaseManager behavior
            # Use the strategic_memory_db path from config
            db_path = Path(config.paths.strategic_memory_db)
            if not db_path.is_absolute():
                db_path = Path.cwd() / db_path

            sqlite_config = DatabaseConfig(
                engine_type="sqlite",
                database_path=db_path,
                max_query_time_ms=200,
                cache_size_mb=100,
                connection_pool_size=10,
            )

            # Initialize SQLite strategy
            sqlite_strategy = SQLiteStrategy(sqlite_config)
            if sqlite_strategy.connect():
                self.strategies["sqlite"] = sqlite_strategy
                self.logger.info("Default SQLite strategy initialized")
            else:
                raise DatabaseError("Failed to initialize default SQLite strategy")

        except Exception as e:
            self.logger.error(f"Failed to initialize default strategies: {e}")
            raise

    def register_strategy(self, name: str, strategy: DatabaseStrategy):
        """Register a new database strategy"""
        self.strategies[name] = strategy
        self.logger.info(f"Registered database strategy: {name}")

    def _analyze_query(
        self, query: str, context: Optional[QueryContext] = None
    ) -> QueryType:
        """
        Analyze query to determine optimal routing strategy.
        Simple heuristic-based analysis for Phase 1.
        """
        if context and context.query_type:
            return context.query_type

        query_upper = query.strip().upper()

        # Transactional patterns (SQLite)
        if any(
            pattern in query_upper
            for pattern in ["INSERT", "UPDATE", "DELETE", "BEGIN", "COMMIT", "ROLLBACK"]
        ):
            return QueryType.TRANSACTIONAL

        # Simple SELECT queries (SQLite)
        if query_upper.startswith("SELECT") and len(query) < 500:
            return QueryType.TRANSACTIONAL

        # Complex analytical queries (future: DuckDB)
        if any(
            pattern in query_upper
            for pattern in ["GROUP BY", "HAVING", "WINDOW", "OVER", "PARTITION"]
        ):
            return QueryType.ANALYTICAL

        # Semantic/vector queries (future: Faiss)
        if any(
            pattern in query_upper for pattern in ["SIMILARITY", "VECTOR", "EMBEDDING"]
        ):
            return QueryType.SEMANTIC

        # Default to transactional
        return QueryType.TRANSACTIONAL

    def _select_strategy(
        self, query_type: QueryType, context: Optional[QueryContext] = None
    ) -> str:
        """Select appropriate strategy based on query type and context"""

        # Check for preferred engine in context
        if (
            context
            and context.preferred_engine
            and context.preferred_engine in self.strategies
        ):
            return context.preferred_engine

        # Use routing rules
        strategy_name = self._routing_rules.get(query_type, self._default_strategy)

        # Fallback to available strategies
        if strategy_name not in self.strategies:
            # For Phase 1, fallback to SQLite (always available)
            strategy_name = self._default_strategy

        return strategy_name

    def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        context: Optional[QueryContext] = None,
    ) -> DatabaseResult:
        """
        Execute query through appropriate strategy with intelligent routing.
        This method preserves all existing DatabaseManager functionality.
        """
        start_time = time.time()

        try:
            # Analyze query to determine routing
            query_type = self._analyze_query(query, context)
            strategy_name = self._select_strategy(query_type, context)

            # Get strategy
            strategy = self.strategies.get(strategy_name)
            if not strategy:
                raise DatabaseError(
                    f"Database strategy '{strategy_name}' not available"
                )

            # Execute query
            result = strategy.execute_query(query, params, context)

            # Add routing metadata
            result.strategy_used = strategy_name
            result.query_type = query_type.value

            routing_time = (time.time() - start_time) * 1000
            self.logger.debug(
                f"Query routed to {strategy_name}",
                query_type=query_type.value,
                routing_time_ms=routing_time,
                execution_time_ms=result.execution_time_ms,
            )

            return result

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"Query execution failed: {e}", query=query[:100])

            return DatabaseResult(
                success=False,
                data=None,
                columns=[],
                execution_time_ms=execution_time,
                error=str(e),
                engine="coordinator",
            )

    def execute_transaction(
        self, operations: List[Dict[str, Any]], strategy_name: Optional[str] = None
    ) -> DatabaseResult:
        """Execute transaction through specified or default strategy"""

        if not strategy_name:
            strategy_name = self._default_strategy

        strategy = self.strategies.get(strategy_name)
        if not strategy:
            raise DatabaseError(f"Database strategy '{strategy_name}' not available")

        return strategy.execute_transaction(operations)

    # Preserve existing DatabaseManager interface for backward compatibility
    def get_connection(self) -> sqlite3.Connection:
        """Get SQLite connection (preserves existing DatabaseManager interface)"""
        sqlite_strategy = self.strategies.get("sqlite")
        if not sqlite_strategy or not isinstance(sqlite_strategy, SQLiteStrategy):
            raise DatabaseError("SQLite strategy not available")

        return sqlite_strategy.get_connection()

    @contextmanager
    def get_cursor(self):
        """Get SQLite cursor (preserves existing DatabaseManager interface)"""
        sqlite_strategy = self.strategies.get("sqlite")
        if not sqlite_strategy or not isinstance(sqlite_strategy, SQLiteStrategy):
            raise DatabaseError("SQLite strategy not available")

        with sqlite_strategy.get_cursor() as cursor:
            yield cursor

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics from all strategies"""
        metrics = {
            "coordinator": {
                "strategies_available": list(self.strategies.keys()),
                "default_strategy": self._default_strategy,
                "routing_rules": {k.value: v for k, v in self._routing_rules.items()},
            }
        }

        for name, strategy in self.strategies.items():
            metrics[name] = strategy.get_performance_metrics()

        return metrics

    def health_check(self) -> Dict[str, bool]:
        """Check health of all strategies"""
        health = {}
        for name, strategy in self.strategies.items():
            health[name] = strategy.health_check()
        return health

    def close_all_connections(self):
        """Close all connections across all strategies"""
        for strategy in self.strategies.values():
            strategy.close_connections()


# Factory function for creating unified database coordinator
def create_unified_database_coordinator(
    dependency_container=None,
) -> UnifiedDatabaseCoordinator:
    """
    Factory function to create UnifiedDatabaseCoordinator with proper initialization.
    Supports dependency injection pattern for testing and future enhancements.
    """
    return UnifiedDatabaseCoordinator(dependency_container)


# Singleton instance for backward compatibility (preserves existing usage patterns)
_coordinator_instance: Optional[UnifiedDatabaseCoordinator] = None
_coordinator_lock = threading.Lock()


def get_unified_database_coordinator() -> UnifiedDatabaseCoordinator:
    """
    Get singleton instance of UnifiedDatabaseCoordinator.
    Preserves existing singleton pattern from DatabaseManager.
    """
    global _coordinator_instance

    if _coordinator_instance is None:
        with _coordinator_lock:
            if _coordinator_instance is None:
                _coordinator_instance = create_unified_database_coordinator()

    return _coordinator_instance


# Backward compatibility aliases (preserves existing imports)
DatabaseManager = UnifiedDatabaseCoordinator
get_database_manager = get_unified_database_coordinator
get_connection = (
    lambda db_path=None: get_unified_database_coordinator().get_connection()
)


# Additional compatibility functions for predictive analytics and other components
def get_legacy_database_manager():
    """
    Provide legacy database manager interface for systems that need it.
    Specifically ensures predictive analytics and context engines continue working.
    """
    return get_unified_database_coordinator()


def ensure_database_compatibility():
    """
    Ensure database compatibility for all legacy components.
    Called during system initialization to prevent runtime errors.
    """
    try:
        coordinator = get_unified_database_coordinator()
        # Verify basic functionality
        coordinator.health_check()
        return True
    except Exception as e:
        logger.error(f"Database compatibility check failed: {e}")
        return False
