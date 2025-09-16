"""
Centralized database management with connection pooling and schema management

Refactored to use BaseManager pattern for DRY compliance.
Eliminates duplicate infrastructure patterns while preserving all functionality.

Author: Martin | Platform Architecture
Phase: 8.1.3 - Core Infrastructure Manager Refactoring
"""

import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Optional

# Import BaseManager infrastructure
try:
    from .base_manager import BaseManager, BaseManagerConfig, ManagerType
    from .manager_factory import register_manager_type
    from .config import get_config
    from .exceptions import DatabaseError
except ImportError:
    # Fallback for test environments
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from base_manager import BaseManager, BaseManagerConfig, ManagerType
    from manager_factory import register_manager_type
    from config import get_config
    from exceptions import DatabaseError


class DatabaseManager(BaseManager):
    """
    Centralized database management with connection pooling and schema management

    Refactored to inherit from BaseManager for DRY compliance.
    Eliminates duplicate logging, configuration, and initialization patterns.
    """

    # Class-level singleton pattern (preserved for backward compatibility)
    _instance = None
    _lock = threading.Lock()

    def __new__(
        cls,
        config: Optional[BaseManagerConfig] = None,
        db_path: Optional[str] = None,
        **kwargs,
    ):
        """Thread-safe singleton initialization with BaseManager integration"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._manager_initialized = False
        return cls._instance

    def __init__(
        self,
        config: Optional[BaseManagerConfig] = None,
        db_path: Optional[str] = None,
        cache: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """Initialize database manager with BaseManager infrastructure"""
        if getattr(self, "_manager_initialized", False):
            return

        # Create default config if not provided
        if config is None:
            config = BaseManagerConfig(
                manager_name="database_manager",
                manager_type=ManagerType.DATABASE,
                enable_metrics=True,
                enable_caching=True,
                enable_logging=True,
                performance_tracking=True,
                custom_config={
                    "db_path": db_path,
                    "connection_timeout": 30.0,
                    "enable_wal": True,
                    "enable_foreign_keys": True,
                },
            )

        # Initialize BaseManager infrastructure
        super().__init__(config, cache, metrics, logger_name="DatabaseManager")

        # Database-specific initialization
        system_config = get_config()

        # Determine database path from config or parameter
        if db_path:
            self.db_path = Path(db_path)
        elif config.get_nested("db_path"):
            self.db_path = Path(config.get_nested("db_path"))
        else:
            # Use the strategic_memory_db path from system config
            db_path_from_config = Path(system_config.paths.strategic_memory_db)
            if not db_path_from_config.is_absolute():
                self.db_path = Path.cwd() / db_path_from_config
            else:
                self.db_path = db_path_from_config

        # Store system config reference
        self.system_config = system_config

        # Database-specific attributes
        self._local = threading.local()
        self._schema_versions = {}
        self._manager_initialized = True

        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database with basic structure
        self._initialize_database()

        # Use BaseManager's structured logging
        self.logger.info(
            "Database manager initialized",
            db_path=str(self.db_path),
            config_source="parameter" if db_path else "system_config",
        )

    def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        Execute database management operations (BaseManager abstract method implementation)

        Supported operations:
        - 'get_connection': Get database connection
        - 'ensure_schema': Ensure schema is applied
        - 'get_table_info': Get table information
        - 'get_stats': Get database statistics
        - 'close': Close connections

        Args:
            operation: Operation to execute
            *args: Positional arguments for operation
            **kwargs: Keyword arguments for operation

        Returns:
            Any: Operation result
        """
        start_time = self.performance_stats.get("operations_count", 0)
        operation_start = self.performance_stats.get("total_processing_time", 0.0)

        try:
            if operation == "get_connection":
                result = self.get_connection()
            elif operation == "ensure_schema":
                result = self.ensure_schema(*args, **kwargs)
            elif operation == "get_table_info":
                result = self.get_table_info(*args, **kwargs)
            elif operation == "get_stats":
                result = self.get_database_stats()
            elif operation == "close":
                result = self.close()
            elif operation == "health_check":
                result = self.health_check()
            else:
                raise ValueError(f"Unknown database operation: {operation}")

            # Update metrics for successful operation
            duration = 0.001  # Minimal duration for immediate operations
            self._update_metrics(operation, duration, True)

            return result

        except Exception as e:
            # Update metrics for failed operation
            duration = 0.001
            self._update_metrics(operation, duration, False)

            # Use BaseManager error handling
            self.logger.error(
                "Database operation failed",
                operation=operation,
                error=str(e),
                args=args,
                kwargs=kwargs,
            )
            raise

    def get_connection(self) -> sqlite3.Connection:
        """
        Get thread-local database connection
        Each thread gets its own connection for thread safety
        """
        if not hasattr(self._local, "connection") or self._local.connection is None:
            try:
                # Get timeout from config with fallback
                timeout = self.config.get_nested("connection_timeout", 30.0)
                if timeout is None:
                    timeout = 30.0

                self._local.connection = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False,
                    timeout=timeout,
                )

                # Configure database based on config settings
                if self.config.get_nested("enable_foreign_keys", True):
                    self._local.connection.execute("PRAGMA foreign_keys = ON")

                if self.config.get_nested("enable_wal", True):
                    self._local.connection.execute("PRAGMA journal_mode = WAL")
                    self._local.connection.execute("PRAGMA synchronous = NORMAL")

                # Use BaseManager logging
                self.logger.debug(
                    "Database connection established",
                    db_path=str(self.db_path),
                    timeout=timeout,
                )

            except Exception as e:
                # Use BaseManager error handling
                self.logger.error(
                    "Failed to connect to database",
                    db_path=str(self.db_path),
                    error=str(e),
                )
                raise DatabaseError(
                    f"Failed to connect to database: {e}", db_path=str(self.db_path)
                )

        return self._local.connection

    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor with automatic commit/rollback"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(
                f"Database operation failed: {e}", db_path=str(self.db_path)
            )
        finally:
            cursor.close()

    def _initialize_database(self):
        """Initialize database with basic structure"""
        try:
            with self.get_cursor() as cursor:
                # Create basic metadata table for schema versioning
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS claudedirector_metadata (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )

                # Record database initialization
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO claudedirector_metadata (key, value)
                    VALUES ('database_version', '1.0.0')
                """
                )

        except Exception as e:
            raise DatabaseError(
                f"Failed to initialize database: {e}", db_path=str(self.db_path)
            )

    def ensure_schema(
        self, schema_name: str, schema_path: Optional[Path] = None
    ) -> bool:
        """
        Ensure specific schema is applied to database
        Returns True if schema was applied, False if already current
        """
        if schema_path is None:
            # Auto-detect schema path based on name
            schema_mapping = {
                "meeting": self.config.meeting_schema_path,
                "stakeholder": self.config.stakeholder_schema_path,
                "task": self.config.task_schema_path,
            }
            schema_path = schema_mapping.get(schema_name)

        if not schema_path or not schema_path.exists():
            self.logger.warning(
                "Schema file not found",
                schema_name=schema_name,
                schema_path=str(schema_path),
            )
            return False

        # Check if schema is already applied
        schema_version_key = f"schema_{schema_name}_version"

        try:
            with self.get_cursor() as cursor:
                cursor.execute(
                    "SELECT value FROM claudedirector_metadata WHERE key = ?",
                    (schema_version_key,),
                )
                result = cursor.fetchone()

                # Get file modification time as version
                current_version = str(schema_path.stat().st_mtime)

                if result and result[0] == current_version:
                    self.logger.debug("Schema already current", schema_name=schema_name)
                    return False

                # Apply schema
                with open(schema_path, "r") as f:
                    schema_sql = f.read()

                # Execute schema (may contain multiple statements)
                cursor.executescript(schema_sql)

                # Update schema version
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO claudedirector_metadata (key, value)
                    VALUES (?, ?)
                """,
                    (schema_version_key, current_version),
                )

                self.logger.info("Schema applied successfully", schema_name=schema_name)
                return True

        except Exception as e:
            raise DatabaseError(
                f"Failed to apply schema '{schema_name}': {e}",
                db_path=str(self.db_path),
            )

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get information about a specific table"""
        try:
            with self.get_cursor() as cursor:
                # Check if table exists
                cursor.execute(
                    """
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name=?
                """,
                    (table_name,),
                )

                if not cursor.fetchone():
                    return {"exists": False}

                # Get table schema
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()

                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]

                return {
                    "exists": True,
                    "columns": [
                        {
                            "name": col[1],
                            "type": col[2],
                            "not_null": bool(col[3]),
                            "default": col[4],
                            "primary_key": bool(col[5]),
                        }
                        for col in columns
                    ],
                    "row_count": row_count,
                }

        except Exception as e:
            raise DatabaseError(f"Failed to get table info for '{table_name}': {e}")

    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            with self.get_cursor() as cursor:
                # Get all tables
                cursor.execute(
                    """
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    ORDER BY name
                """
                )
                tables = [row[0] for row in cursor.fetchall()]

                # Get stats for each table
                table_stats = {}
                total_rows = 0

                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    table_stats[table] = count
                    total_rows += count

                # Get database size
                db_size = self.db_path.stat().st_size if self.db_path.exists() else 0

                return {
                    "database_path": str(self.db_path),
                    "database_size_bytes": db_size,
                    "database_size_mb": round(db_size / (1024 * 1024), 2),
                    "total_tables": len(tables),
                    "total_rows": total_rows,
                    "tables": table_stats,
                }

        except Exception as e:
            raise DatabaseError(f"Failed to get database stats: {e}")

    def close(self):
        """Close database connections"""
        try:
            if hasattr(self._local, "connection") and self._local.connection:
                self._local.connection.close()
                self._local.connection = None
            self.logger.info("Database connections closed")
        except Exception as e:
            self.logger.error("Error closing database connections", error=str(e))

    def __del__(self):
        """Cleanup on deletion"""
        try:
            self.close()
        except:
            pass


# Convenience functions for backward compatibility
def get_database_manager(db_path: Optional[str] = None) -> DatabaseManager:
    """Get the database manager instance"""
    return DatabaseManager(db_path)


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Get database connection (backward compatibility)"""
    return get_database_manager(db_path).get_connection()


# Register DatabaseManager with the factory system
try:
    register_manager_type(
        manager_type=ManagerType.DATABASE,
        manager_class=DatabaseManager,
        description="Centralized database management with connection pooling and schema management",
    )
except Exception:
    # Ignore registration errors during import (e.g., circular imports)
    pass
