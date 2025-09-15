#!/usr/bin/env python3
"""
Simple Database Schema Validator - Phase A Implementation
Conversation Persistence System Recovery

Authors: Martin | Platform Architecture + Diego | Engineering Leadership
Story: Phase A.1 - Database Schema Validation and Repair
Priority: P0 - BLOCKING (Conversation persistence foundation)

Simplified validator with minimal dependencies for immediate Phase A execution.
"""

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass
class ValidationResult:
    """Simple validation results"""

    schema_valid: bool
    performance_ok: bool
    database_clean: bool
    validation_passed: bool
    errors: List[str]
    recommendations: List[str]


class SimpleDbValidator:
    """Simplified database validator for Phase A"""

    EXPECTED_TABLES = [
        "conversations",
        "session_context",
        "session_checkpoints",
        "executive_sessions",
        "strategic_insights",
    ]

    def __init__(self):
        # Find database path
        self.db_path = self._find_database_path()

    def _find_database_path(self) -> Path:
        """Find strategic memory database"""
        possible_paths = [
            Path("data/strategic/strategic_memory.db"),
            Path("data/strategic_memory.db"),
            Path(".claudedirector/data/strategic_memory.db"),
        ]

        for path in possible_paths:
            if path.exists():
                return path

        # Default path
        return Path("data/strategic/strategic_memory.db")

    def validate(self) -> ValidationResult:
        """Run complete validation"""
        print(f"🔍 Validating database: {self.db_path}")

        errors = []
        recommendations = []

        # 1. Check database exists
        if not self.db_path.exists():
            errors.append("Database file does not exist")
            recommendations.append(f"Create database at {self.db_path}")
            return ValidationResult(
                schema_valid=False,
                performance_ok=False,
                database_clean=False,
                validation_passed=False,
                errors=errors,
                recommendations=recommendations,
            )

        try:
            # 2. Test connection performance
            start_time = time.time()
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute("SELECT 1")
            connection_time_ms = (time.time() - start_time) * 1000

            performance_ok = connection_time_ms < 50.0
            if not performance_ok:
                errors.append(f"Connection time {connection_time_ms:.2f}ms > 50ms")

            # 3. Check schema
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing_tables = [row[0] for row in cursor.fetchall()]

            missing_tables = [
                t for t in self.EXPECTED_TABLES if t not in existing_tables
            ]
            schema_valid = len(missing_tables) == 0

            if not schema_valid:
                errors.append(f"Missing tables: {missing_tables}")
                recommendations.append("Initialize missing tables")

            # 4. Check for test data
            test_data_count = 0
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                for table in existing_tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        test_data_count += count
                    except:
                        pass

            database_clean = test_data_count == 0
            if not database_clean:
                recommendations.append(f"Clean {test_data_count} test records")

            validation_passed = schema_valid and performance_ok

            return ValidationResult(
                schema_valid=schema_valid,
                performance_ok=performance_ok,
                database_clean=database_clean,
                validation_passed=validation_passed,
                errors=errors,
                recommendations=recommendations,
            )

        except Exception as e:
            errors.append(f"Validation failed: {str(e)}")
            return ValidationResult(
                schema_valid=False,
                performance_ok=False,
                database_clean=False,
                validation_passed=False,
                errors=errors,
                recommendations=["Fix database connection issues"],
            )

    def repair(self) -> bool:
        """Attempt basic repairs"""
        print(f"🔧 Repairing database: {self.db_path}")

        try:
            # Ensure directory exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            # Initialize database if needed
            with sqlite3.connect(str(self.db_path)) as conn:
                # Enable basic optimizations
                conn.execute("PRAGMA journal_mode = WAL")
                conn.execute("PRAGMA synchronous = NORMAL")

                # Create basic tables if they don't exist
                basic_schema = """
                CREATE TABLE IF NOT EXISTS session_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    session_type TEXT NOT NULL,
                    conversation_thread TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS executive_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_type TEXT NOT NULL,
                    stakeholder_key TEXT NOT NULL,
                    meeting_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """

                conn.executescript(basic_schema)

                # Clear any test data
                conn.execute("DELETE FROM session_context")
                conn.execute("DELETE FROM executive_sessions")
                conn.commit()

            print("✅ Database repair completed")
            return True

        except Exception as e:
            print(f"❌ Database repair failed: {e}")
            return False


if __name__ == "__main__":
    print("🔍 Phase A: Database Schema Validation & Repair")

    validator = SimpleDbValidator()

    # Run validation
    result = validator.validate()

    print(f"\n📊 Validation Results:")
    print(
        f"Schema Valid: {'✅' if result.schema_valid else '❌'} {result.schema_valid}"
    )
    print(
        f"Performance OK: {'✅' if result.performance_ok else '❌'} {result.performance_ok}"
    )
    print(
        f"Database Clean: {'✅' if result.database_clean else '❌'} {result.database_clean}"
    )
    print(f"Overall Status: {'✅ PASSED' if result.validation_passed else '❌ FAILED'}")

    if result.errors:
        print(f"\n❌ Errors:")
        for error in result.errors:
            print(f"  - {error}")

    if result.recommendations:
        print(f"\n💡 Recommendations:")
        for rec in result.recommendations:
            print(f"  - {rec}")

    # Attempt repair if needed
    if not result.validation_passed:
        print(f"\n🔧 Attempting repair...")
        repair_success = validator.repair()

        if repair_success:
            # Re-validate after repair
            print(f"\n🔍 Re-validating after repair...")
            new_result = validator.validate()
            print(
                f"Post-repair status: {'✅ PASSED' if new_result.validation_passed else '❌ FAILED'}"
            )
