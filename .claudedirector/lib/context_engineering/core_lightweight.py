"""
Lightweight Core Context Engineering - Phase 9 P0 Compatibility

This module provides essential context engineering functionality without
heavyweight dependencies (numpy, sklearn, watchdog) for P0 test compatibility.

Status: Phase 9 Architecture Cleanup - Lightweight Core
Author: Martin | Platform Architecture with MCP Sequential enhancement
"""

import json
import logging
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# Core imports only - no heavyweight dependencies
try:
    from ..core.config import get_config
    from ..core.exceptions import DatabaseError
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

    # Fallback minimal config
    class MinimalConfig:
        def __init__(self):
            self.database_path = "data/strategic_memory.db"

    def get_config():
        return MinimalConfig()

logger = logging.getLogger(__name__)


@dataclass
class LightweightMemorySession:
    """Lightweight session for P0 test compatibility"""
    session_id: str
    session_type: str
    created_timestamp: float
    updated_timestamp: float
    status: str = "active"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "session_type": self.session_type,
            "created_timestamp": self.created_timestamp,
            "updated_timestamp": self.updated_timestamp,
            "status": self.status
        }


class LightweightMemoryManager:
    """
    Lightweight Memory Manager - Essential functionality only

    Provides core memory management without heavyweight dependencies
    for P0 test compatibility during Phase 9 architecture cleanup.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize lightweight memory manager"""
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)

        # Initialize database path
        if hasattr(self.config, 'database_path'):
            self.db_path = self.config.database_path
        else:
            self.db_path = "data/strategic_memory.db"

        # Ensure directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

        self.logger.info("LightweightMemoryManager initialized for P0 compatibility")

    def _init_database(self) -> None:
        """Initialize SQLite database with essential tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Essential session table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        session_type TEXT NOT NULL,
                        created_timestamp REAL NOT NULL,
                        updated_timestamp REAL NOT NULL,
                        status TEXT DEFAULT 'active',
                        metadata TEXT
                    )
                """)

                # Essential context table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS session_context (
                        context_id TEXT PRIMARY KEY,
                        session_id TEXT NOT NULL,
                        context_type TEXT NOT NULL,
                        context_data TEXT NOT NULL,
                        created_timestamp REAL NOT NULL,
                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                    )
                """)

                conn.commit()
                self.logger.debug("Lightweight database schema initialized")

        except Exception as e:
            raise DatabaseError(f"Failed to initialize lightweight database: {e}")

    def start_session(self, session_type: str = "strategic") -> str:
        """Start new session with lightweight tracking"""
        session_id = f"session_{int(time.time() * 1000)}"
        current_time = time.time()

        session = LightweightMemorySession(
            session_id=session_id,
            session_type=session_type,
            created_timestamp=current_time,
            updated_timestamp=current_time
        )

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO sessions
                    (session_id, session_type, created_timestamp, updated_timestamp, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    session.session_id,
                    session.session_type,
                    session.created_timestamp,
                    session.updated_timestamp,
                    session.status
                ))
                conn.commit()

            self.logger.info(f"Started lightweight session: {session_id}")
            return session_id

        except Exception as e:
            raise DatabaseError(f"Failed to start session: {e}")

    def store_context(
        self,
        session_id: str,
        context_type: str,
        context_data: Dict[str, Any]
    ) -> bool:
        """Store context data for session"""
        context_id = f"ctx_{int(time.time() * 1000000)}"

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO session_context
                    (context_id, session_id, context_type, context_data, created_timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    context_id,
                    session_id,
                    context_type,
                    json.dumps(context_data),
                    time.time()
                ))
                conn.commit()

            self.logger.debug(f"Stored context: {context_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to store context: {e}")
            return False

    def get_session(self, session_id: str) -> Optional[LightweightMemorySession]:
        """Get session by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT session_id, session_type, created_timestamp,
                           updated_timestamp, status
                    FROM sessions WHERE session_id = ?
                """, (session_id,))

                row = cursor.fetchone()
                if row:
                    return LightweightMemorySession(
                        session_id=row[0],
                        session_type=row[1],
                        created_timestamp=row[2],
                        updated_timestamp=row[3],
                        status=row[4]
                    )
                return None

        except Exception as e:
            self.logger.error(f"Failed to get session: {e}")
            return None

    def list_sessions(self, limit: int = 50) -> List[LightweightMemorySession]:
        """List recent sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT session_id, session_type, created_timestamp,
                           updated_timestamp, status
                    FROM sessions
                    ORDER BY created_timestamp DESC
                    LIMIT ?
                """, (limit,))

                sessions = []
                for row in cursor.fetchall():
                    sessions.append({
                        "session_id": row[0],
                        "session_type": row[1],
                        "created_timestamp": row[2],
                        "updated_timestamp": row[3],
                        "status": row[4],
                        "session_start_timestamp": datetime.fromtimestamp(row[2]).isoformat(),
                        "last_activity": row[3]
                    })

                return sessions

        except Exception as e:
            self.logger.error(f"Failed to list sessions: {e}")
            return []

    def get_session_context(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all context for a session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT context_type, context_data, created_timestamp
                    FROM session_context
                    WHERE session_id = ?
                    ORDER BY created_timestamp ASC
                """, (session_id,))

                contexts = []
                for row in cursor.fetchall():
                    contexts.append({
                        "context_type": row[0],
                        "context_data": json.loads(row[1]),
                        "created_timestamp": row[2]
                    })

                return contexts

        except Exception as e:
            self.logger.error(f"Failed to get session context: {e}")
            return []

    def end_session(self, session_id: str) -> bool:
        """End session (alias for close_session)"""
        return self.close_session(session_id)

    def close_session(self, session_id: str) -> bool:
        """Close session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE sessions
                    SET status = 'closed', updated_timestamp = ?
                    WHERE session_id = ?
                """, (time.time(), session_id))
                conn.commit()

            self.logger.info(f"Closed session: {session_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to close session: {e}")
            return False

    def get_recent_sessions(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent sessions within specified hours"""
        cutoff_time = time.time() - (hours * 3600)  # Convert hours to seconds

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT session_id, session_type, created_timestamp,
                           updated_timestamp, status
                    FROM sessions
                    WHERE created_timestamp > ?
                    ORDER BY created_timestamp DESC
                """, (cutoff_time,))

                sessions = []
                for row in cursor.fetchall():
                    sessions.append({
                        "session_id": row[0],
                        "session_type": row[1],
                        "created_timestamp": row[2],
                        "updated_timestamp": row[3],
                        "status": row[4],
                        "session_start_timestamp": datetime.fromtimestamp(row[2]).isoformat(),
                        "last_activity": row[3]
                    })

                return sessions

        except Exception as e:
            self.logger.error(f"Failed to get recent sessions: {e}")
            return []

    def update_session_context(
        self,
        session_id: str,
        context_updates: Dict[str, Any]
    ) -> bool:
        """Update session context with new data"""
        return self.store_context(session_id, "context_update", context_updates)

    def restore_session_context(self, session_id: str) -> Dict[str, Any]:
        """Restore session context"""
        contexts = self.get_session_context(session_id)
        return {
            "contexts": contexts,
            "restored": len(contexts) > 0,
            "session_id": session_id,
            "context_data": contexts
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get lightweight memory manager statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Count sessions
                cursor.execute("SELECT COUNT(*) FROM sessions")
                total_sessions = cursor.fetchone()[0]

                # Count active sessions
                cursor.execute("SELECT COUNT(*) FROM sessions WHERE status = 'active'")
                active_sessions = cursor.fetchone()[0]

                # Count context entries
                cursor.execute("SELECT COUNT(*) FROM session_context")
                total_contexts = cursor.fetchone()[0]

                return {
                    "total_sessions": total_sessions,
                    "active_sessions": active_sessions,
                    "total_contexts": total_contexts,
                    "lightweight_mode": True,
                    "last_updated": time.time()
                }

        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {"error": str(e), "lightweight_mode": True}


# Global lightweight instance
_lightweight_manager = None

def get_lightweight_memory_manager() -> LightweightMemoryManager:
    """Get lightweight memory manager instance"""
    global _lightweight_manager
    if _lightweight_manager is None:
        _lightweight_manager = LightweightMemoryManager()
    return _lightweight_manager


# Compatibility aliases for P0 tests
def get_strategic_memory_manager():
    """Compatibility alias for strategic memory manager"""
    return get_lightweight_memory_manager()


class SessionContextManager:
    """Compatibility wrapper for legacy SessionContextManager"""

    def __init__(self, db_path: str = None):
        self.memory_manager = get_lightweight_memory_manager()

    def start_session(self, session_type: str = "strategic") -> str:
        return self.memory_manager.start_session(session_type)

    def store_stakeholder_profile(self, stakeholder_key: str, profile_data: Dict[str, Any]) -> bool:
        # Find or create a session for this operation
        sessions = self.memory_manager.list_sessions(limit=1)
        if sessions:
            session_id = sessions[0].session_id
        else:
            session_id = self.memory_manager.start_session("stakeholder_management")

        return self.memory_manager.store_context(
            session_id,
            "stakeholder_profile",
            {"stakeholder_key": stakeholder_key, "profile_data": profile_data}
        )

    def detect_session_restart(self) -> bool:
        """Simple restart detection"""
        sessions = self.memory_manager.list_sessions(limit=10)
        return len(sessions) > 0

    def restore_session_context(self, session_id: str) -> Dict[str, Any]:
        """Restore session context"""
        contexts = self.memory_manager.get_session_context(session_id)
        return {"contexts": contexts, "restored": len(contexts) > 0}
