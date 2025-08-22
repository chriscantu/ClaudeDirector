#!/usr/bin/env python3
"""
Optimized SQLite Database Manager for ClaudeDirector
High-performance SQLite configuration with zero-setup complexity
"""

import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
import structlog

logger = structlog.get_logger(__name__)


class OptimizedSQLiteManager:
    """
    High-performance SQLite manager with strategic optimizations
    Maintains plug-and-play simplicity while maximizing SQLite capabilities
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_path: Optional[str] = None):
        """Singleton pattern for connection management"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_path: Optional[str] = None):
        if hasattr(self, "initialized"):
            return

        self.db_path = db_path or "memory/strategic_memory.db"
        self.logger = logger.bind(component="optimized_sqlite")

        # Thread-local storage for connections
        self._local = threading.local()

        # Performance monitoring
        self._query_stats = {
            "total_queries": 0,
            "slow_queries": 0,
            "cache_hits": 0,
            "connection_reuses": 0,
        }

        # Ensure database directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # Initialize with optimal settings
        self._initialize_database()
        self.initialized = True

    def _initialize_database(self):
        """Initialize database with performance optimizations"""
        try:
            with self._get_optimized_connection() as conn:
                # Apply strategic performance optimizations
                self._apply_performance_settings(conn)
                self._create_strategic_indexes(conn)

            self.logger.info("Database initialized with performance optimizations")

        except Exception as e:
            self.logger.error("Failed to initialize optimized database", error=str(e))
            raise

    def _apply_performance_settings(self, conn: sqlite3.Connection):
        """Apply SQLite performance optimizations"""

        # WAL mode for better concurrency (readers don't block writers)
        conn.execute("PRAGMA journal_mode=WAL")

        # Reduce fsync calls for better write performance
        conn.execute("PRAGMA synchronous=NORMAL")

        # Larger cache size (10MB) for better read performance
        conn.execute("PRAGMA cache_size=10000")

        # Faster temporary storage
        conn.execute("PRAGMA temp_store=MEMORY")

        # Optimize page size for modern systems
        conn.execute("PRAGMA page_size=4096")

        # Enable memory-mapped I/O for large databases
        conn.execute("PRAGMA mmap_size=268435456")  # 256MB

        # Optimize for mixed read/write workload
        conn.execute("PRAGMA optimize")

        # Enable foreign key constraints for data integrity
        conn.execute("PRAGMA foreign_keys=ON")

        # Set busy timeout for concurrent access
        conn.execute("PRAGMA busy_timeout=30000")  # 30 seconds

        self.logger.info("Applied SQLite performance optimizations")

    def _create_strategic_indexes(self, conn: sqlite3.Connection):
        """Create strategic indexes for ClaudeDirector intelligence workloads"""

        strategic_indexes = [
            # Stakeholder engagement patterns
            """CREATE INDEX IF NOT EXISTS idx_stakeholder_engagement_temporal
               ON stakeholder_engagements(stakeholder_profile_id, last_activity_at DESC)""",
            """CREATE INDEX IF NOT EXISTS idx_stakeholder_relationship_health
               ON relationship_health_metrics(stakeholder_profile_id, measurement_date DESC)""",
            # Meeting intelligence optimization
            """CREATE INDEX IF NOT EXISTS idx_meeting_sessions_temporal
               ON meeting_sessions(session_date DESC, meeting_type, stakeholder_count)""",
            """CREATE INDEX IF NOT EXISTS idx_meeting_participants_lookup
               ON meeting_participants(meeting_session_id, participant_role)""",
            # Document intelligence patterns
            """CREATE INDEX IF NOT EXISTS idx_google_docs_intelligence_composite
               ON google_docs_intelligence(drive_file_id, intelligence_type, processed_into_system)""",
            """CREATE INDEX IF NOT EXISTS idx_google_docs_validation
               ON google_docs_intelligence(validation_status, extracted_at DESC)""",
            # Cross-system intelligence queries
            """CREATE INDEX IF NOT EXISTS idx_strategic_tasks_stakeholder
               ON strategic_tasks(responsible_stakeholder_id, due_date, priority_level)""",
            """CREATE INDEX IF NOT EXISTS idx_task_activity_temporal
               ON task_activity_log(task_id, activity_timestamp DESC)""",
            # Executive session optimization
            """CREATE INDEX IF NOT EXISTS idx_executive_sessions_stakeholder
               ON executive_sessions(stakeholder_key, session_date DESC)""",
            # Workspace monitoring
            """CREATE INDEX IF NOT EXISTS idx_workspace_changes_temporal
               ON workspace_changes(event_timestamp DESC, change_type)""",
            # Google Drive sync performance
            """CREATE INDEX IF NOT EXISTS idx_google_drive_sync_status
               ON google_drive_documents(sync_status, last_synced_at DESC)""",
            """CREATE INDEX IF NOT EXISTS idx_google_drive_sync_metrics_temporal
               ON google_drive_sync_metrics(started_at DESC, sync_type)""",
        ]

        for index_sql in strategic_indexes:
            try:
                conn.execute(index_sql)
            except sqlite3.OperationalError as e:
                if "already exists" not in str(e).lower():
                    self.logger.warning(
                        "Index creation warning", sql=index_sql, error=str(e)
                    )

        conn.commit()
        self.logger.info(f"Created {len(strategic_indexes)} strategic indexes")

    @contextmanager
    def _get_optimized_connection(self):
        """Get thread-local optimized connection"""
        if not hasattr(self._local, "connection"):
            self._local.connection = sqlite3.connect(
                self.db_path, timeout=30.0, check_same_thread=False
            )
            self._local.connection.row_factory = sqlite3.Row

            # Apply performance settings to new connections
            if hasattr(self, "initialized"):
                self._apply_performance_settings(self._local.connection)

            self._query_stats["connection_reuses"] += 1

        try:
            yield self._local.connection
        finally:
            # Keep connection open for reuse
            pass

    def get_connection(self) -> sqlite3.Connection:
        """Public interface for getting database connection"""
        # For backward compatibility with existing code
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row

        # Apply optimizations
        self._apply_performance_settings(conn)

        return conn

    @contextmanager
    def get_optimized_connection(self):
        """Get optimized connection with automatic management"""
        with self._get_optimized_connection() as conn:
            yield conn

    def execute_with_timing(self, sql: str, params=None, fetch_all=False):
        """Execute query with performance monitoring"""
        start_time = time.time()

        with self.get_optimized_connection() as conn:
            cursor = conn.cursor()

            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            if fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()

            conn.commit()

        execution_time = time.time() - start_time
        self._query_stats["total_queries"] += 1

        if execution_time > 0.5:  # Log slow queries
            self._query_stats["slow_queries"] += 1
            self.logger.warning(
                "Slow query detected", sql=sql[:100], execution_time=execution_time
            )

        return result

    def bulk_insert(self, table: str, columns: list, data: list):
        """Optimized bulk insert for intelligence data"""
        if not data:
            return

        placeholders = ",".join(["?" for _ in columns])
        sql = f"INSERT OR REPLACE INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

        with self.get_optimized_connection() as conn:
            # Use transaction for bulk operations
            conn.execute("BEGIN TRANSACTION")
            try:
                conn.executemany(sql, data)
                conn.commit()
                self.logger.info(f"Bulk inserted {len(data)} records into {table}")
            except Exception as e:
                conn.rollback()
                self.logger.error(f"Bulk insert failed for {table}", error=str(e))
                raise

    def vacuum_and_analyze(self):
        """Maintenance operations for optimal performance"""
        try:
            with self.get_optimized_connection() as conn:
                # Update query planner statistics
                conn.execute("ANALYZE")

                # Check if VACUUM is needed (if database is >10% fragmented)
                result = conn.execute("PRAGMA page_count").fetchone()
                freelist_result = conn.execute("PRAGMA freelist_count").fetchone()

                if result and freelist_result:
                    total_pages = result[0]
                    free_pages = freelist_result[0]

                    if total_pages > 0 and (free_pages / total_pages) > 0.1:
                        self.logger.info(
                            "Database fragmentation detected, running VACUUM"
                        )
                        conn.execute("VACUUM")

            self.logger.info("Database maintenance completed")

        except Exception as e:
            self.logger.error("Database maintenance failed", error=str(e))

    def get_performance_stats(self) -> dict:
        """Get performance statistics for monitoring"""
        with self.get_optimized_connection() as conn:
            # Database size information
            size_result = conn.execute("PRAGMA page_count").fetchone()
            page_size_result = conn.execute("PRAGMA page_size").fetchone()

            db_size_mb = 0
            if size_result and page_size_result:
                db_size_mb = (size_result[0] * page_size_result[0]) / (1024 * 1024)

            # Cache hit ratio
            cache_stats = conn.execute("PRAGMA cache_size").fetchone()

        return {
            "database_size_mb": round(db_size_mb, 2),
            "total_queries": self._query_stats["total_queries"],
            "slow_queries": self._query_stats["slow_queries"],
            "slow_query_percentage": (
                self._query_stats["slow_queries"]
                / max(self._query_stats["total_queries"], 1)
                * 100
            ),
            "connection_reuses": self._query_stats["connection_reuses"],
            "cache_size": cache_stats[0] if cache_stats else 0,
        }

    def close_connections(self):
        """Clean up connections (for shutdown)"""
        if hasattr(self._local, "connection"):
            self._local.connection.close()
            delattr(self._local, "connection")


# Singleton instance for global use
_db_manager = None


def get_db_manager(db_path: Optional[str] = None) -> OptimizedSQLiteManager:
    """Get global database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = OptimizedSQLiteManager(db_path)
    return _db_manager


if __name__ == "__main__":
    """CLI for database optimization and monitoring"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="ClaudeDirector Database Optimization")
    parser.add_argument(
        "--stats", action="store_true", help="Show performance statistics"
    )
    parser.add_argument(
        "--maintenance", action="store_true", help="Run database maintenance"
    )
    parser.add_argument(
        "--optimize", action="store_true", help="Apply performance optimizations"
    )
    parser.add_argument("--db-path", help="Database path")

    args = parser.parse_args()

    db_manager = get_db_manager(args.db_path)

    if args.stats:
        stats = db_manager.get_performance_stats()
        print("Database Performance Statistics:")
        print(json.dumps(stats, indent=2))

    elif args.maintenance:
        print("Running database maintenance...")
        db_manager.vacuum_and_analyze()
        print("Maintenance completed.")

    elif args.optimize:
        print("Applying database optimizations...")
        db_manager._initialize_database()
        print("Optimizations applied.")

    else:
        parser.print_help()
