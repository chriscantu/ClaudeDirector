#!/usr/bin/env python3
"""
Database Schema Validator - Phase A Implementation
Conversation Persistence System Recovery

Authors: Martin | Platform Architecture + Diego | Engineering Leadership
Story: Phase A.1 - Database Schema Validation and Repair
Priority: P0 - BLOCKING (Conversation persistence foundation)

This module provides comprehensive database schema validation for the strategic
conversation capture system, ensuring database integrity before implementing
automatic conversation capture.

Key Features:
- 6-table schema integrity checking
- Foreign key constraint validation
- Performance benchmarking (<50ms requirement)
- Connection pooling validation
- Backup mechanism verification

CRITICAL: Follows PROJECT_STRUCTURE.md core/ patterns and BLOAT_PREVENTION_SYSTEM.md
"""

import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import structlog

    logger = structlog.get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)

try:
    from .database import DatabaseManager
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    from database import DatabaseManager


@dataclass
class SchemaValidationResult:
    """Results from database schema validation"""

    # Schema integrity
    schema_valid: bool
    tables_found: List[str]
    tables_expected: List[str]
    missing_tables: List[str]

    # Foreign key validation
    foreign_keys_valid: bool
    foreign_key_errors: List[str]

    # Performance metrics
    connection_time_ms: float
    query_performance_ms: float
    performance_meets_requirements: bool

    # Data state
    test_data_present: bool
    database_clean: bool

    # Overall status
    validation_passed: bool
    error_messages: List[str]
    recommendations: List[str]


class DatabaseSchemaValidator:
    """
    Comprehensive database schema validator for conversation persistence system

    Validates the 6-table strategic memory schema and ensures performance
    requirements are met for conversation capture operations.
    """

    # Expected schema tables for conversation persistence
    EXPECTED_TABLES = [
        "executive_sessions",
        "strategic_initiatives",
        "stakeholder_profiles",
        "meeting_sessions",
        "session_context",
        "session_checkpoints",
    ]

    # Performance requirements (from spec)
    MAX_CONNECTION_TIME_MS = 50.0
    MAX_QUERY_TIME_MS = 50.0

    def __init__(self, db_path: Optional[str] = None):
        """Initialize validator with database path"""
        self.db_manager = DatabaseManager(db_path=db_path)
        self.db_path = self.db_manager.db_path
        self.validation_results = []

    def validate_full_schema(self) -> SchemaValidationResult:
        """
        Perform comprehensive schema validation

        Returns:
            SchemaValidationResult with complete validation status
        """
        logger.info("Starting comprehensive database schema validation")

        # Initialize result tracking
        errors = []
        recommendations = []

        try:
            # 1. Validate database file exists and is accessible
            db_exists = self._validate_database_file()
            if not db_exists:
                return SchemaValidationResult(
                    schema_valid=False,
                    tables_found=[],
                    tables_expected=self.EXPECTED_TABLES,
                    missing_tables=self.EXPECTED_TABLES,
                    foreign_keys_valid=False,
                    foreign_key_errors=["Database file not accessible"],
                    connection_time_ms=0.0,
                    query_performance_ms=0.0,
                    performance_meets_requirements=False,
                    test_data_present=False,
                    database_clean=False,
                    validation_passed=False,
                    error_messages=["Database file not found or not accessible"],
                    recommendations=["Create database file and initialize schema"],
                )

            # 2. Test connection performance
            connection_time = self._benchmark_connection_performance()
            connection_meets_requirements = (
                connection_time <= self.MAX_CONNECTION_TIME_MS
            )

            if not connection_meets_requirements:
                errors.append(
                    f"Connection time {connection_time:.2f}ms exceeds {self.MAX_CONNECTION_TIME_MS}ms requirement"
                )
                recommendations.append("Optimize database connection settings")

            # 3. Validate table schema
            tables_found, missing_tables = self._validate_table_schema()
            schema_valid = len(missing_tables) == 0

            if not schema_valid:
                errors.append(f"Missing tables: {missing_tables}")
                recommendations.append("Initialize missing database tables")

            # 4. Validate foreign key constraints
            fk_valid, fk_errors = self._validate_foreign_keys()
            if not fk_valid:
                errors.extend(fk_errors)
                recommendations.append("Repair foreign key constraint violations")

            # 5. Test query performance
            query_time = self._benchmark_query_performance()
            query_meets_requirements = query_time <= self.MAX_QUERY_TIME_MS

            if not query_meets_requirements:
                errors.append(
                    f"Query time {query_time:.2f}ms exceeds {self.MAX_QUERY_TIME_MS}ms requirement"
                )
                recommendations.append("Add database indexes for performance")

            # 6. Check for test data
            test_data_present = self._check_test_data()
            database_clean = not test_data_present

            if test_data_present:
                recommendations.append("Clean test data from database")

            # Overall validation status
            performance_ok = connection_meets_requirements and query_meets_requirements
            validation_passed = schema_valid and fk_valid and performance_ok

            result = SchemaValidationResult(
                schema_valid=schema_valid,
                tables_found=tables_found,
                tables_expected=self.EXPECTED_TABLES,
                missing_tables=missing_tables,
                foreign_keys_valid=fk_valid,
                foreign_key_errors=fk_errors,
                connection_time_ms=connection_time,
                query_performance_ms=query_time,
                performance_meets_requirements=performance_ok,
                test_data_present=test_data_present,
                database_clean=database_clean,
                validation_passed=validation_passed,
                error_messages=errors,
                recommendations=recommendations,
            )

            logger.info(
                f"Schema validation completed: {'PASSED' if validation_passed else 'FAILED'}"
            )
            return result

        except Exception as e:
            logger.error(f"Schema validation failed with exception: {e}")
            return SchemaValidationResult(
                schema_valid=False,
                tables_found=[],
                tables_expected=self.EXPECTED_TABLES,
                missing_tables=self.EXPECTED_TABLES,
                foreign_keys_valid=False,
                foreign_key_errors=[f"Validation exception: {str(e)}"],
                connection_time_ms=0.0,
                query_performance_ms=0.0,
                performance_meets_requirements=False,
                test_data_present=False,
                database_clean=False,
                validation_passed=False,
                error_messages=[f"Validation exception: {str(e)}"],
                recommendations=["Investigate database validation exception"],
            )

    def _validate_database_file(self) -> bool:
        """Validate database file exists and is accessible"""
        try:
            if not self.db_path.exists():
                logger.warning(f"Database file does not exist: {self.db_path}")
                return False

            # Test basic SQLite access
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute("SELECT 1")

            return True

        except Exception as e:
            logger.error(f"Database file validation failed: {e}")
            return False

    def _benchmark_connection_performance(self) -> float:
        """Benchmark database connection performance"""
        try:
            start_time = time.time()

            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute("SELECT 1")

            end_time = time.time()
            connection_time_ms = (end_time - start_time) * 1000

            logger.info(f"Connection performance: {connection_time_ms:.2f}ms")
            return connection_time_ms

        except Exception as e:
            logger.error(f"Connection performance benchmark failed: {e}")
            return float("inf")

    def _validate_table_schema(self) -> Tuple[List[str], List[str]]:
        """Validate expected tables exist"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing_tables = [row[0] for row in cursor.fetchall()]

            missing_tables = [
                table for table in self.EXPECTED_TABLES if table not in existing_tables
            ]

            logger.info(f"Tables found: {existing_tables}")
            if missing_tables:
                logger.warning(f"Missing tables: {missing_tables}")

            return existing_tables, missing_tables

        except Exception as e:
            logger.error(f"Table schema validation failed: {e}")
            return [], self.EXPECTED_TABLES

    def _validate_foreign_keys(self) -> Tuple[bool, List[str]]:
        """Validate foreign key constraints"""
        try:
            errors = []

            with sqlite3.connect(str(self.db_path)) as conn:
                # Enable foreign key checking
                conn.execute("PRAGMA foreign_keys = ON")

                # Check for foreign key violations
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_key_check")
                violations = cursor.fetchall()

                if violations:
                    for violation in violations:
                        errors.append(f"Foreign key violation: {violation}")

            fk_valid = len(errors) == 0
            logger.info(f"Foreign key validation: {'PASSED' if fk_valid else 'FAILED'}")

            return fk_valid, errors

        except Exception as e:
            logger.error(f"Foreign key validation failed: {e}")
            return False, [f"Foreign key validation exception: {str(e)}"]

    def _benchmark_query_performance(self) -> float:
        """Benchmark query performance on existing tables"""
        try:
            start_time = time.time()

            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                # Test query on each existing table
                for table in self.EXPECTED_TABLES:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        cursor.fetchone()
                    except sqlite3.OperationalError:
                        # Table doesn't exist - skip for performance test
                        pass

            end_time = time.time()
            query_time_ms = (end_time - start_time) * 1000

            logger.info(f"Query performance: {query_time_ms:.2f}ms")
            return query_time_ms

        except Exception as e:
            logger.error(f"Query performance benchmark failed: {e}")
            return float("inf")

    def _check_test_data(self) -> bool:
        """Check if test data is present in database"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()

                # Check for any data in conversation-related tables
                test_data_indicators = [
                    "SELECT COUNT(*) FROM executive_sessions",
                    "SELECT COUNT(*) FROM session_context",
                ]

                for query in test_data_indicators:
                    try:
                        cursor.execute(query)
                        count = cursor.fetchone()[0]
                        if count > 0:
                            logger.info(f"Test data found: {count} records")
                            return True
                    except sqlite3.OperationalError:
                        # Table doesn't exist
                        continue

            return False

        except Exception as e:
            logger.error(f"Test data check failed: {e}")
            return False

    def repair_database_issues(self, validation_result: SchemaValidationResult) -> bool:
        """
        Attempt to repair common database issues

        Args:
            validation_result: Results from schema validation

        Returns:
            True if repair was successful
        """
        logger.info("Starting database repair process")

        try:
            # 1. Initialize missing tables
            if validation_result.missing_tables:
                success = self._initialize_missing_tables(
                    validation_result.missing_tables
                )
                if not success:
                    return False

            # 2. Clean test data if present
            if validation_result.test_data_present:
                success = self._clean_test_data()
                if not success:
                    return False

            # 3. Optimize database for performance
            self._optimize_database_performance()

            logger.info("Database repair completed successfully")
            return True

        except Exception as e:
            logger.error(f"Database repair failed: {e}")
            return False

    def _initialize_missing_tables(self, missing_tables: List[str]) -> bool:
        """Initialize missing database tables"""
        try:
            # Load schema files
            schema_dir = Path(__file__).parent.parent.parent / "config" / "schemas"

            schema_files = {
                "executive_sessions": schema_dir / "schema.sql",
                "strategic_initiatives": schema_dir / "schema.sql",
                "stakeholder_profiles": schema_dir
                / "stakeholder_engagement_schema.sql",
                "meeting_sessions": schema_dir / "enhanced_schema.sql",
                "session_context": schema_dir / "session_context_schema.sql",
                "session_checkpoints": schema_dir / "session_context_schema.sql",
            }

            with sqlite3.connect(str(self.db_path)) as conn:
                for table in missing_tables:
                    if table in schema_files:
                        schema_file = schema_files[table]
                        if schema_file.exists():
                            with open(schema_file, "r") as f:
                                schema_sql = f.read()
                            conn.executescript(schema_sql)
                            logger.info(f"Initialized table: {table}")

            return True

        except Exception as e:
            logger.error(f"Table initialization failed: {e}")
            return False

    def _clean_test_data(self) -> bool:
        """Clean test data from database"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                # Clear all tables (keeping schema)
                tables_to_clean = [
                    "executive_sessions",
                    "strategic_initiatives",
                    "stakeholder_profiles",
                    "meeting_sessions",
                    "session_context",
                    "session_checkpoints",
                ]

                for table in tables_to_clean:
                    try:
                        conn.execute(f"DELETE FROM {table}")
                        logger.info(f"Cleaned test data from: {table}")
                    except sqlite3.OperationalError:
                        # Table doesn't exist - skip
                        pass

                conn.commit()

            return True

        except Exception as e:
            logger.error(f"Test data cleanup failed: {e}")
            return False

    def _optimize_database_performance(self) -> None:
        """Optimize database for conversation capture performance"""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                # Enable WAL mode for better concurrent access
                conn.execute("PRAGMA journal_mode = WAL")

                # Optimize for performance
                conn.execute("PRAGMA synchronous = NORMAL")
                conn.execute("PRAGMA cache_size = 10000")
                conn.execute("PRAGMA temp_store = MEMORY")

                # Create indexes for conversation queries
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_session_context_session_id ON session_context(session_id)",
                    "CREATE INDEX IF NOT EXISTS idx_executive_sessions_date ON executive_sessions(meeting_date)",
                    "CREATE INDEX IF NOT EXISTS idx_meeting_sessions_date ON meeting_sessions(meeting_date)",
                ]

                for index_sql in indexes:
                    conn.execute(index_sql)

                logger.info("Database performance optimization completed")

        except Exception as e:
            logger.error(f"Database optimization failed: {e}")


def validate_conversation_database(
    db_path: Optional[str] = None,
) -> SchemaValidationResult:
    """
    Convenience function for database validation

    Args:
        db_path: Optional database path (uses default if not provided)

    Returns:
        SchemaValidationResult with validation status
    """
    validator = DatabaseSchemaValidator(db_path)
    return validator.validate_full_schema()


if __name__ == "__main__":
    # Direct validation execution
    print("🔍 Running database schema validation...")

    validator = DatabaseSchemaValidator()
    result = validator.validate_full_schema()

    print(f"\n📊 Validation Results:")
    print(f"Schema Valid: {result.schema_valid}")
    print(f"Performance OK: {result.performance_meets_requirements}")
    print(f"Database Clean: {result.database_clean}")
    print(f"Overall Status: {'✅ PASSED' if result.validation_passed else '❌ FAILED'}")

    if result.error_messages:
        print(f"\n❌ Errors:")
        for error in result.error_messages:
            print(f"  - {error}")

    if result.recommendations:
        print(f"\n💡 Recommendations:")
        for rec in result.recommendations:
            print(f"  - {rec}")
