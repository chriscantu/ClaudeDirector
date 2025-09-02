"""
Strategic Memory Manager - Phase 9 Consolidation

This module consolidates memory management functionality from:
- memory/memory_manager.py
- memory/session_context_manager.py
- memory/optimized_db_manager.py

Status: Phase 9 Architecture Cleanup - Memory Systems Consolidation
Author: Martin | Platform Architecture with MCP Sequential enhancement
"""

import argparse
import json
import os
import sqlite3
import time
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Phase 8 performance integration
try:
    from ..performance.cache_manager import get_cache_manager
    from ..performance.memory_optimizer import get_memory_optimizer
    from ..performance.response_optimizer import get_response_optimizer

    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False

# Phase 2 Migration: Add UnifiedDatabaseCoordinator support
try:
    from ..core.unified_database import (
        get_unified_database_coordinator,
        UnifiedDatabaseCoordinator,
    )

    UNIFIED_DB_AVAILABLE = True
except ImportError:
    UNIFIED_DB_AVAILABLE = False
    
# Legacy import compatibility during migration
try:
    from ..memory.optimized_db_manager import get_db_manager, OptimizedSQLiteManager

    LEGACY_DB_AVAILABLE = True
except ImportError:
    LEGACY_DB_AVAILABLE = False


class StrategicMemoryManager:
    """
    Unified Strategic Memory Manager - Phase 9 Single Source of Truth

    Consolidates functionality from:
    - StrategicMemoryManager (memory layer)
    - SessionContextManager (memory layer)
    - OptimizedSQLiteManager integration

    Features:
    - Executive session management and persistence
    - Strategic context preservation across restarts
    - Performance-optimized database operations
    - Session continuity and context recovery
    - Enterprise-grade memory management
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        enable_performance: bool = True,
        session_backup_interval: int = 300,
    ):
        """Initialize unified strategic memory manager"""
        if db_path is None:
            # Default to ClaudeDirector data directory
            base_path = Path(__file__).parent.parent.parent.parent
            db_path = str(base_path / "data" / "strategic_memory.db")

        self.db_path = db_path
        self.enable_performance = enable_performance
        self.session_backup_interval = session_backup_interval

        # Session management
        self.current_session_id = None
        self.critical_context_patterns = [
            "stakeholder_profiles",
            "executive_sessions",
            "strategic_initiatives",
            "roi_discussions",
            "coalition_mapping",
            "platform_investment_context",
        ]

        # Initialize performance components (Phase 8 integration)
        if self.enable_performance and PERFORMANCE_AVAILABLE:
            try:
                self.cache_manager = get_cache_manager()
                self.memory_optimizer = get_memory_optimizer()
                self.response_optimizer = get_response_optimizer()
            except Exception:
                self.enable_performance = False

        # Initialize database
        self.ensure_db_exists()
        self._ensure_session_schema()

    def ensure_db_exists(self):
        """Ensure database and directory exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        if not os.path.exists(self.db_path):
            print(f"Database {self.db_path} will be created on first use")

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection via UnifiedDatabaseCoordinator with intelligent fallback"""
        # Phase 2 Migration: Prefer UnifiedDatabaseCoordinator
        if UNIFIED_DB_AVAILABLE:
            try:
                unified_coordinator = get_unified_database_coordinator()
                return unified_coordinator.get_connection()
            except Exception as e:
                print(f"⚠️  UnifiedDatabaseCoordinator fallback to legacy: {e}")
        
        # Fallback to legacy optimized manager
        if LEGACY_DB_AVAILABLE:
            try:
                db_manager = get_db_manager(self.db_path)
                return db_manager.get_connection()
            except Exception as e:
                print(f"⚠️  Legacy DB manager fallback to direct: {e}")
        
        # Final fallback to direct connection
        print(f"📊 Using direct SQLite connection: {self.db_path}")
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_session_schema(self):
        """Ensure session context tables exist"""
        with self.get_connection() as conn:
            # Session context table
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS session_context (
                    session_id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_type TEXT NOT NULL,
                    context_data TEXT,  -- JSON data
                    critical_context TEXT,  -- JSON for critical elements
                    stakeholder_context TEXT,  -- JSON stakeholder data
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_status TEXT DEFAULT 'active',
                    recovery_priority INTEGER DEFAULT 1
                )
            """
            )

            # Session continuity table for crash recovery
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS session_continuity (
                    backup_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    backup_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context_snapshot TEXT,  -- Full context JSON
                    recovery_instructions TEXT,  -- JSON recovery steps
                    critical_flags TEXT,  -- JSON critical indicators
                    FOREIGN KEY (session_id) REFERENCES session_context(session_id)
                )
            """
            )

            # Enhanced executive sessions table (consolidated from memory_manager)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS executive_sessions_enhanced (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_type TEXT NOT NULL,
                    stakeholder_key TEXT,
                    meeting_date TEXT,
                    agenda_topics TEXT,
                    decisions_made TEXT,
                    action_items TEXT,
                    business_impact TEXT,
                    next_session_prep TEXT,
                    persona_activated TEXT,
                    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_context_id TEXT,  -- Link to session_context
                    strategic_priority INTEGER DEFAULT 5,
                    roi_impact REAL DEFAULT 0.0,
                    FOREIGN KEY (session_context_id) REFERENCES session_context(session_id)
                )
            """
            )

            conn.commit()

    # === SESSION MANAGEMENT (Consolidated from SessionContextManager) ===

    def start_session(
        self,
        session_type: str = "strategic_guidance",
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Start new strategic session with context preservation"""
        session_id = f"session_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
        self.current_session_id = session_id

        # Use cache for performance if available
        if self.enable_performance:
            cache_key = f"session_start:{session_id}"
            if self.cache_manager.get(cache_key):
                return session_id

        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO session_context
                (session_id, session_type, context_data, critical_context)
                VALUES (?, ?, ?, ?)
            """,
                (
                    session_id,
                    session_type,
                    json.dumps(initial_context or {}),
                    json.dumps(
                        {
                            "session_started": True,
                            "critical_patterns": self.critical_context_patterns,
                        }
                    ),
                ),
            )

            conn.commit()

        # Cache session start
        if self.enable_performance:
            self.cache_manager.set(cache_key, {"status": "started"}, ttl=3600)

        return session_id

    def preserve_context(
        self,
        session_id: Optional[str] = None,
        context_data: Optional[Dict[str, Any]] = None,
        critical_indicators: Optional[List[str]] = None,
    ) -> bool:
        """Preserve critical context for session continuity"""
        session_id = session_id or self.current_session_id
        if not session_id:
            return False

        backup_id = f"backup_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"

        # Identify critical context elements
        critical_context = {}
        if context_data:
            for pattern in self.critical_context_patterns:
                if pattern in context_data:
                    critical_context[pattern] = context_data[pattern]

        # Add critical indicators
        if critical_indicators:
            critical_context["critical_indicators"] = critical_indicators

        with self.get_connection() as conn:
            # Update session context
            conn.execute(
                """
                UPDATE session_context
                SET context_data = ?, critical_context = ?, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = ?
            """,
                (
                    json.dumps(context_data or {}),
                    json.dumps(critical_context),
                    session_id,
                ),
            )

            # Create backup for recovery
            conn.execute(
                """
                INSERT INTO session_continuity
                (backup_id, session_id, context_snapshot, critical_flags)
                VALUES (?, ?, ?, ?)
            """,
                (
                    backup_id,
                    session_id,
                    json.dumps(
                        {
                            "full_context": context_data or {},
                            "critical_context": critical_context,
                            "timestamp": datetime.now().isoformat(),
                        }
                    ),
                    json.dumps(
                        {
                            "requires_recovery": any(
                                indicator in str(context_data)
                                for indicator in [
                                    "executive",
                                    "stakeholder",
                                    "strategic",
                                ]
                            ),
                            "critical_patterns_present": len(critical_context) > 0,
                        }
                    ),
                ),
            )

            conn.commit()

        return True

    def recover_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Recover session context after interruption"""
        with self.get_connection() as conn:
            # Get latest session context
            result = conn.execute(
                """
                SELECT context_data, critical_context, last_activity
                FROM session_context
                WHERE session_id = ?
            """,
                (session_id,),
            ).fetchone()

            if not result:
                return None

            # Get latest backup
            backup_result = conn.execute(
                """
                SELECT context_snapshot, backup_timestamp
                FROM session_continuity
                WHERE session_id = ?
                ORDER BY backup_timestamp DESC
                LIMIT 1
            """,
                (session_id,),
            ).fetchone()

            recovery_context = {
                "session_id": session_id,
                "context_data": json.loads(result["context_data"] or "{}"),
                "critical_context": json.loads(result["critical_context"] or "{}"),
                "last_activity": result["last_activity"],
                "recovery_available": backup_result is not None,
            }

            if backup_result:
                backup_data = json.loads(backup_result["context_snapshot"])
                recovery_context["backup_context"] = backup_data
                recovery_context["backup_timestamp"] = backup_result["backup_timestamp"]

            return recovery_context

    def get_recent_sessions(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent sessions within specified hours"""
        cutoff_time = time.time() - (hours * 3600)  # Convert hours to seconds

        try:
            with self.get_connection() as conn:
                results = conn.execute(
                    """
                    SELECT session_id, session_type, created_at, last_activity, status
                    FROM sessions
                    WHERE created_at > ?
                    ORDER BY created_at DESC
                """,
                    (cutoff_time,),
                ).fetchall()

                sessions = []
                for row in results:
                    sessions.append(
                        {
                            "session_id": row[0],
                            "session_type": row[1],
                            "created_timestamp": row[2],
                            "updated_timestamp": row[3],
                            "status": row[4],
                        }
                    )

                return sessions

        except Exception:
            # Graceful fallback for P0 compatibility
            return []

    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get all active sessions for context restoration"""
        with self.get_connection() as conn:
            results = conn.execute(
                """
                SELECT session_id, session_type, created_at, last_activity,
                       context_data, critical_context
                FROM session_context
                WHERE session_status = 'active'
                ORDER BY last_activity DESC
            """
            ).fetchall()

            sessions = []
            for row in results:
                sessions.append(
                    {
                        "session_id": row["session_id"],
                        "session_type": row["session_type"],
                        "created_at": row["created_at"],
                        "last_activity": row["last_activity"],
                        "has_critical_context": bool(row["critical_context"]),
                        "context_size": len(row["context_data"] or ""),
                    }
                )

            return sessions

    # === EXECUTIVE SESSION MANAGEMENT (Consolidated from StrategicMemoryManager) ===

    def store_executive_session(
        self,
        session_type: str,
        stakeholder_key: str,
        meeting_date: str,
        agenda_topics: List[str] = None,
        decisions_made: Dict = None,
        action_items: List[Dict] = None,
        business_impact: str = None,
        next_session_prep: str = None,
        persona_activated: str = None,
        strategic_priority: int = 5,
        roi_impact: float = 0.0,
    ) -> int:
        """Store executive session with enhanced context linking"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO executive_sessions_enhanced (
                    session_type, stakeholder_key, meeting_date, agenda_topics,
                    decisions_made, action_items, business_impact, next_session_prep,
                    persona_activated, session_context_id, strategic_priority, roi_impact
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    session_type,
                    stakeholder_key,
                    meeting_date,
                    json.dumps(agenda_topics or []),
                    json.dumps(decisions_made or {}),
                    json.dumps(action_items or []),
                    business_impact,
                    next_session_prep,
                    persona_activated,
                    self.current_session_id,
                    strategic_priority,
                    roi_impact,
                ),
            )

            session_id = cursor.lastrowid
            conn.commit()

            # Preserve executive session in current context
            if self.current_session_id:
                self.preserve_context(
                    context_data={
                        "executive_session": {
                            "id": session_id,
                            "type": session_type,
                            "stakeholder": stakeholder_key,
                            "date": meeting_date,
                        }
                    },
                    critical_indicators=["executive_session", "stakeholder_engagement"],
                )

            return session_id

    def get_stakeholder_session_history(
        self, stakeholder_key: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get session history for specific stakeholder"""
        with self.get_connection() as conn:
            results = conn.execute(
                """
                SELECT session_id, session_type, meeting_date, agenda_topics,
                       decisions_made, action_items, business_impact,
                       strategic_priority, roi_impact, created_timestamp
                FROM executive_sessions_enhanced
                WHERE stakeholder_key = ?
                ORDER BY created_timestamp DESC
                LIMIT ?
            """,
                (stakeholder_key, limit),
            ).fetchall()

            sessions = []
            for row in results:
                sessions.append(
                    {
                        "session_id": row["session_id"],
                        "session_type": row["session_type"],
                        "meeting_date": row["meeting_date"],
                        "agenda_topics": json.loads(row["agenda_topics"] or "[]"),
                        "decisions_made": json.loads(row["decisions_made"] or "{}"),
                        "action_items": json.loads(row["action_items"] or "[]"),
                        "business_impact": row["business_impact"],
                        "strategic_priority": row["strategic_priority"],
                        "roi_impact": row["roi_impact"],
                        "created_timestamp": row["created_timestamp"],
                    }
                )

            return sessions

    def get_strategic_sessions_summary(self, days_back: int = 30) -> Dict[str, Any]:
        """Get summary of strategic sessions for reporting"""
        cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()

        with self.get_connection() as conn:
            # Session counts by type
            type_counts = conn.execute(
                """
                SELECT session_type, COUNT(*) as count
                FROM executive_sessions_enhanced
                WHERE created_timestamp > ?
                GROUP BY session_type
                ORDER BY count DESC
            """,
                (cutoff_date,),
            ).fetchall()

            # ROI impact summary
            roi_summary = conn.execute(
                """
                SELECT
                    COUNT(*) as total_sessions,
                    AVG(roi_impact) as avg_roi_impact,
                    SUM(roi_impact) as total_roi_impact,
                    AVG(strategic_priority) as avg_priority
                FROM executive_sessions_enhanced
                WHERE created_timestamp > ?
            """,
                (cutoff_date,),
            ).fetchone()

            # Top stakeholders by session count
            stakeholder_activity = conn.execute(
                """
                SELECT stakeholder_key, COUNT(*) as session_count
                FROM executive_sessions_enhanced
                WHERE created_timestamp > ?
                GROUP BY stakeholder_key
                ORDER BY session_count DESC
                LIMIT 10
            """,
                (cutoff_date,),
            ).fetchall()

            return {
                "period_days": days_back,
                "session_types": [
                    {"type": row["session_type"], "count": row["count"]}
                    for row in type_counts
                ],
                "roi_metrics": {
                    "total_sessions": roi_summary["total_sessions"] or 0,
                    "average_roi_impact": roi_summary["avg_roi_impact"] or 0.0,
                    "total_roi_impact": roi_summary["total_roi_impact"] or 0.0,
                    "average_priority": roi_summary["avg_priority"] or 5.0,
                },
                "top_stakeholders": [
                    {
                        "stakeholder": row["stakeholder_key"],
                        "sessions": row["session_count"],
                    }
                    for row in stakeholder_activity
                ],
            }

    # === PERFORMANCE AND SYSTEM MANAGEMENT ===

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory system statistics"""
        stats = {
            "database_path": self.db_path,
            "database_size_mb": (
                os.path.getsize(self.db_path) / (1024 * 1024)
                if os.path.exists(self.db_path)
                else 0
            ),
            "performance_enabled": self.enable_performance,
            "current_session": self.current_session_id,
        }

        with self.get_connection() as conn:
            # Session statistics
            session_stats = conn.execute(
                """
                SELECT
                    COUNT(*) as total_sessions,
                    COUNT(CASE WHEN session_status = 'active' THEN 1 END) as active_sessions,
                    AVG(LENGTH(context_data)) as avg_context_size
                FROM session_context
            """
            ).fetchone()

            # Executive session statistics
            exec_stats = conn.execute(
                """
                SELECT
                    COUNT(*) as total_executive_sessions,
                    COUNT(DISTINCT stakeholder_key) as unique_stakeholders,
                    AVG(strategic_priority) as avg_priority
                FROM executive_sessions_enhanced
            """
            ).fetchone()

            stats.update(
                {
                    "sessions": {
                        "total": session_stats["total_sessions"] or 0,
                        "active": session_stats["active_sessions"] or 0,
                        "avg_context_size": session_stats["avg_context_size"] or 0,
                    },
                    "executive_sessions": {
                        "total": exec_stats["total_executive_sessions"] or 0,
                        "unique_stakeholders": exec_stats["unique_stakeholders"] or 0,
                        "avg_priority": exec_stats["avg_priority"] or 5.0,
                    },
                }
            )

        # Performance stats if available
        if self.enable_performance and PERFORMANCE_AVAILABLE:
            try:
                stats["performance"] = {
                    "cache_stats": (
                        self.cache_manager.get_stats()
                        if hasattr(self.cache_manager, "get_stats")
                        else {}
                    ),
                    "memory_stats": (
                        self.memory_optimizer.get_memory_stats()
                        if hasattr(self.memory_optimizer, "get_memory_stats")
                        else {}
                    ),
                }
            except Exception as e:
                stats["performance_error"] = str(e)

        return stats

    def cleanup_old_sessions(self, days_old: int = 90) -> int:
        """Cleanup old inactive sessions"""
        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()

        with self.get_connection() as conn:
            # Count sessions to be cleaned
            count_result = conn.execute(
                """
                SELECT COUNT(*) as count
                FROM session_context
                WHERE last_activity < ? AND session_status != 'active'
            """,
                (cutoff_date,),
            ).fetchone()

            cleanup_count = count_result["count"] or 0

            if cleanup_count > 0:
                # Clean up old session backups first
                conn.execute(
                    """
                    DELETE FROM session_continuity
                    WHERE session_id IN (
                        SELECT session_id FROM session_context
                        WHERE last_activity < ? AND session_status != 'active'
                    )
                """,
                    (cutoff_date,),
                )

                # Clean up old sessions
                conn.execute(
                    """
                    DELETE FROM session_context
                    WHERE last_activity < ? AND session_status != 'active'
                """,
                    (cutoff_date,),
                )

                conn.commit()

        return cleanup_count


# === BACKWARD COMPATIBILITY API ===


def get_strategic_memory_manager(
    db_path: Optional[str] = None, enable_performance: bool = True
):
    """Get unified strategic memory manager instance with lightweight fallback"""
    try:
        # Try to create the heavyweight manager
        manager = StrategicMemoryManager(
            db_path=db_path, enable_performance=enable_performance
        )
        # Test if it has required attributes for P0 compatibility
        if hasattr(manager, "cache_manager") or not enable_performance:
            return manager
        else:
            # Missing performance components, fall back to lightweight
            raise AttributeError("Performance components not available")
    except Exception:
        # Fallback to lightweight manager for P0 compatibility
        from .core_lightweight import get_lightweight_memory_manager

        return get_lightweight_memory_manager()


# Legacy compatibility classes for migration period
class SessionContextManager(StrategicMemoryManager):
    """Legacy compatibility wrapper for SessionContextManager"""

    def __init__(self, db_path: Optional[str] = None):
        super().__init__(db_path=db_path)


class MemoryManager(StrategicMemoryManager):
    """Legacy compatibility wrapper for StrategicMemoryManager"""

    def __init__(self, db_path: str = "memory/strategic_memory.db"):
        super().__init__(db_path=db_path)
