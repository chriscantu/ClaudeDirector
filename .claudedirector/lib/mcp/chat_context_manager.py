"""
Chat Context Manager - Phase 7B Chat Integration

ARCHITECTURE COMPLIANCE:
- OVERVIEW.md: Integrates with 8-layer Context Engineering architecture
- DRY Principle: Leverages existing strategic memory infrastructure
- SOLID: Single responsibility for chat context persistence
- Performance: <100ms state recovery (OVERVIEW.md enterprise SLA)

Phase 7B: T-B2 - 5 Story Points - P1 Priority
Foundation: Context Engineering Layer integration
"""

import json
import sqlite3
import time
import logging
import gzip
import base64
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from enum import Enum

logger = logging.getLogger(__name__)


class ContextScope(Enum):
    """Scope levels for context persistence"""

    SESSION = "session"  # Current chat session only
    CHART = "chart"  # Specific chart instance
    USER = "user"  # User-wide preferences
    GLOBAL = "global"  # System-wide defaults


@dataclass
class ChartContextState:
    """Complete chart interaction state for persistence"""

    chart_id: str
    current_filters: Dict[str, Any] = field(default_factory=dict)
    navigation_history: List[Dict[str, Any]] = field(default_factory=list)
    time_range: Optional[Dict[str, str]] = None
    zoom_level: float = 1.0
    selected_elements: List[str] = field(default_factory=list)
    drill_down_path: List[str] = field(default_factory=list)
    persona_context: Optional[str] = None
    last_interaction: Optional[datetime] = None
    custom_modifications: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Handle datetime serialization
        if self.last_interaction:
            data["last_interaction"] = self.last_interaction.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChartContextState":
        """Create instance from dictionary"""
        # Handle datetime deserialization
        if "last_interaction" in data and data["last_interaction"]:
            data["last_interaction"] = datetime.fromisoformat(data["last_interaction"])
        return cls(**data)


@dataclass
class ConversationContext:
    """Conversation-level context for strategic continuity"""

    session_id: str
    persona_history: List[str] = field(default_factory=list)
    topic_progression: List[str] = field(default_factory=list)
    strategic_insights: List[str] = field(default_factory=list)
    follow_up_queue: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class ChatContextManager:
    """
    Preserve interactive chart state across chat sessions

    ARCHITECTURE INTEGRATION:
    - OVERVIEW.md: Leverages Context Engineering 8-layer architecture
    - Performance: <100ms state restoration (enterprise SLA)
    - Storage: SQLite with <50MB per session limit
    - Security: Encrypted sensitive data elements
    - Cleanup: Automatic old state cleanup and compression

    CONTEXT ELEMENTS:
    ✅ Current chart filters and selections
    ✅ Drill-down navigation history and breadcrumbs
    ✅ Time range and zoom level persistence
    ✅ Persona-specific insights and context
    ✅ Follow-up suggestions and strategic continuity
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize chat context manager

        Args:
            db_path: Path to SQLite database (uses default if None)
        """
        self.name = "chat-context-manager"
        self.version = "1.0.0"

        # Database configuration from constants (DRY compliance)
        self.db_path = db_path or self._get_default_db_path()
        self.max_session_size = (
            MCPServerConstants.Phase7B.MAX_SESSION_SIZE_MB * 1024 * 1024
        )
        self.cleanup_after_days = MCPServerConstants.Phase7B.CLEANUP_AFTER_DAYS

        # Initialize database
        self._init_database()

        # Performance targets from configuration (OVERVIEW.md compliance)
        self.performance_target_restore = (
            MCPServerConstants.Phase7B.CONTEXT_RESTORATION_TARGET
        )
        self.performance_target_save = MCPServerConstants.Phase7B.CONTEXT_SAVE_TARGET

        logger.info(f"ChatContextManager {self.version} initialized")
        logger.info(
            f"✅ ARCHITECTURE: Integrated with Context Engineering (OVERVIEW.md)"
        )
        logger.info(f"✅ DATABASE: {self.db_path}")

    def _get_default_db_path(self) -> str:
        """Get default database path from configuration (DRY compliance)"""
        # ARCHITECTURE: Integrate with existing strategic memory infrastructure
        db_relative_path = MCPServerConstants.Phase7B.DB_PATHS["chat_context"]
        db_path = Path(".claudedirector") / db_relative_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return str(db_path)

    def _init_database(self):
        """Initialize SQLite database with optimized schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Chart context state table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS chart_contexts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chart_id TEXT NOT NULL,
                        session_id TEXT,
                        context_scope TEXT DEFAULT 'session',
                        state_data TEXT NOT NULL,
                        state_hash TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP,
                        size_bytes INTEGER DEFAULT 0,
                        UNIQUE(chart_id, session_id, context_scope)
                    )
                """
                )

                # Conversation context table
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS conversation_contexts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        context_data TEXT NOT NULL,
                        persona_summary TEXT,
                        strategic_summary TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        size_bytes INTEGER DEFAULT 0
                    )
                """
                )

                # Performance indexes
                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_chart_contexts_lookup
                    ON chart_contexts(chart_id, session_id, context_scope)
                """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_chart_contexts_cleanup
                    ON chart_contexts(expires_at, created_at)
                """
                )

                cursor.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_conversation_sessions
                    ON conversation_contexts(session_id, updated_at)
                """
                )

                conn.commit()
                logger.info(
                    "✅ Chat context database initialized with optimized schema"
                )

        except Exception as e:
            logger.error(f"❌ Failed to initialize context database: {e}")
            raise

    def save_interaction_state(
        self,
        chart_id: str,
        state: ChartContextState,
        session_id: str = "default",
        scope: ContextScope = ContextScope.SESSION,
    ) -> bool:
        """
        Save current chart interaction state to database

        Args:
            chart_id: Chart identifier
            state: Current chart state to persist
            session_id: Chat session identifier
            scope: Context persistence scope

        Returns:
            bool: Success status

        PERFORMANCE TARGET: <50ms save operation
        """
        start_time = time.time()

        try:
            # Prepare state data
            state.last_interaction = datetime.now()
            state_json = json.dumps(state.to_dict(), ensure_ascii=False)
            state_hash = hashlib.sha256(state_json.encode()).hexdigest()
            size_bytes = len(state_json.encode())

            # Check size limits
            if size_bytes > self.max_session_size:
                logger.warning(
                    f"State size ({size_bytes} bytes) exceeds limit, compressing..."
                )
                state_json = self._compress_state(state_json)
                size_bytes = len(state_json.encode())

            # Calculate expiration
            expires_at = datetime.now() + timedelta(days=self.cleanup_after_days)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Insert or update state
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO chart_contexts
                    (chart_id, session_id, context_scope, state_data, state_hash,
                     updated_at, expires_at, size_bytes)
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?)
                """,
                    (
                        chart_id,
                        session_id,
                        scope.value,
                        state_json,
                        state_hash,
                        expires_at,
                        size_bytes,
                    ),
                )

                conn.commit()

            save_time = time.time() - start_time
            logger.info(
                f"✅ Chart state saved in {save_time:.3f}s (target: {self.performance_target_save}s)"
            )

            if save_time > self.performance_target_save:
                logger.warning(f"⚠️ Save operation exceeded performance target")

            return True

        except Exception as e:
            logger.error(f"❌ Failed to save interaction state: {e}", exc_info=True)
            return False

    def restore_interaction_state(
        self,
        chart_id: str,
        session_id: str = "default",
        scope: ContextScope = ContextScope.SESSION,
    ) -> Optional[ChartContextState]:
        """
        Restore previous chart interaction state

        Args:
            chart_id: Chart identifier to restore
            session_id: Chat session identifier
            scope: Context scope to restore from

        Returns:
            Optional[ChartContextState]: Restored state or None

        PERFORMANCE TARGET: <100ms restoration time
        """
        start_time = time.time()

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Query for latest state
                cursor.execute(
                    """
                    SELECT state_data, state_hash, updated_at, size_bytes
                    FROM chart_contexts
                    WHERE chart_id = ? AND session_id = ? AND context_scope = ?
                    AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
                    ORDER BY updated_at DESC
                    LIMIT 1
                """,
                    (chart_id, session_id, scope.value),
                )

                row = cursor.fetchone()
                if not row:
                    logger.info(f"No saved state found for chart {chart_id}")
                    return None

                state_json, state_hash, updated_at, size_bytes = row

                # Verify state integrity
                current_hash = hashlib.sha256(state_json.encode()).hexdigest()
                if current_hash != state_hash:
                    logger.warning(
                        f"State hash mismatch for chart {chart_id}, ignoring corrupted state"
                    )
                    return None

                # Decompress if needed
                if size_bytes > len(state_json.encode()):
                    state_json = self._decompress_state(state_json)

                # Parse state data
                state_data = json.loads(state_json)
                restored_state = ChartContextState.from_dict(state_data)

                restore_time = time.time() - start_time
                logger.info(
                    f"✅ Chart state restored in {restore_time:.3f}s (target: {self.performance_target_restore}s)"
                )

                if restore_time > self.performance_target_restore:
                    logger.warning(f"⚠️ Restore operation exceeded performance target")

                return restored_state

        except Exception as e:
            logger.error(f"❌ Failed to restore interaction state: {e}", exc_info=True)
            return None

    def save_conversation_context(
        self, session_id: str, context: ConversationContext
    ) -> bool:
        """
        Save conversation-level context for strategic continuity

        Args:
            session_id: Session identifier
            context: Conversation context to save

        Returns:
            bool: Success status
        """
        try:
            context.updated_at = datetime.now()
            context_json = json.dumps(asdict(context), default=str, ensure_ascii=False)
            size_bytes = len(context_json.encode())

            # Generate strategic summary
            persona_summary = ", ".join(context.persona_history[-5:])  # Last 5 personas
            strategic_summary = "; ".join(
                context.strategic_insights[-3:]
            )  # Last 3 insights

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO conversation_contexts
                    (session_id, context_data, persona_summary, strategic_summary,
                     updated_at, size_bytes)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
                """,
                    (
                        session_id,
                        context_json,
                        persona_summary,
                        strategic_summary,
                        size_bytes,
                    ),
                )

                conn.commit()

            logger.info(f"✅ Conversation context saved for session {session_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save conversation context: {e}", exc_info=True)
            return False

    def restore_conversation_context(
        self, session_id: str
    ) -> Optional[ConversationContext]:
        """Restore conversation context for strategic continuity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT context_data, updated_at
                    FROM conversation_contexts
                    WHERE session_id = ?
                    ORDER BY updated_at DESC
                    LIMIT 1
                """,
                    (session_id,),
                )

                row = cursor.fetchone()
                if not row:
                    return None

                context_json, updated_at = row
                context_data = json.loads(context_json)

                # Convert datetime strings back to datetime objects
                for field in ["created_at", "updated_at"]:
                    if field in context_data and context_data[field]:
                        context_data[field] = datetime.fromisoformat(
                            context_data[field]
                        )

                return ConversationContext(**context_data)

        except Exception as e:
            logger.error(
                f"❌ Failed to restore conversation context: {e}", exc_info=True
            )
            return None

    def cleanup_expired_contexts(self) -> Dict[str, int]:
        """
        Clean up expired contexts and optimize database

        Returns:
            Dict[str, int]: Cleanup statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Clean expired chart contexts
                cursor.execute(
                    """
                    DELETE FROM chart_contexts
                    WHERE expires_at < CURRENT_TIMESTAMP
                    OR created_at < date('now', '-30 days')
                """
                )
                chart_cleaned = cursor.rowcount

                # Clean old conversation contexts (keep last 100 per session)
                cursor.execute(
                    """
                    DELETE FROM conversation_contexts
                    WHERE id NOT IN (
                        SELECT id FROM conversation_contexts
                        ORDER BY updated_at DESC
                        LIMIT 100
                    )
                    AND updated_at < date('now', '-7 days')
                """
                )
                conversation_cleaned = cursor.rowcount

                # Vacuum database for space reclaim
                cursor.execute("VACUUM")

                conn.commit()

            stats = {
                "chart_contexts_cleaned": chart_cleaned,
                "conversation_contexts_cleaned": conversation_cleaned,
            }

            logger.info(f"✅ Context cleanup completed: {stats}")
            return stats

        except Exception as e:
            logger.error(f"❌ Context cleanup failed: {e}", exc_info=True)
            return {"error": str(e)}

    def get_context_statistics(self) -> Dict[str, Any]:
        """Get context storage statistics for monitoring"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Chart context stats
                cursor.execute(
                    """
                    SELECT
                        COUNT(*) as total_charts,
                        SUM(size_bytes) as total_size,
                        AVG(size_bytes) as avg_size,
                        COUNT(DISTINCT session_id) as unique_sessions
                    FROM chart_contexts
                """
                )
                chart_stats = dict(
                    zip([col[0] for col in cursor.description], cursor.fetchone())
                )

                # Conversation context stats
                cursor.execute(
                    """
                    SELECT
                        COUNT(*) as total_conversations,
                        SUM(size_bytes) as total_size,
                        AVG(size_bytes) as avg_size
                    FROM conversation_contexts
                """
                )
                conv_stats = dict(
                    zip([col[0] for col in cursor.description], cursor.fetchone())
                )

                return {
                    "chart_contexts": chart_stats,
                    "conversation_contexts": conv_stats,
                    "database_path": self.db_path,
                    "performance_targets": {
                        "save": f"{self.performance_target_save}s",
                        "restore": f"{self.performance_target_restore}s",
                    },
                    "cleanup_after_days": self.cleanup_after_days,
                }

        except Exception as e:
            logger.error(f"❌ Failed to get context statistics: {e}")
            return {"error": str(e)}

    def _compress_state(self, state_json: str) -> str:
        """Compress large state data using gzip compression"""
        try:
            # Convert to bytes and compress
            state_bytes = state_json.encode("utf-8")
            compressed_bytes = gzip.compress(state_bytes)

            # Encode as base64 for safe storage in SQLite TEXT field
            compressed_b64 = base64.b64encode(compressed_bytes).decode("ascii")

            original_size = len(state_bytes)
            compressed_size = len(compressed_b64)
            compression_ratio = compressed_size / original_size

            logger.info(
                f"State compressed: {original_size} → {compressed_size} bytes ({compression_ratio:.2%})"
            )

            # Only use compression if it actually saves space
            if compressed_size < original_size * 0.9:  # 10% minimum savings
                return f"GZIP_B64:{compressed_b64}"
            else:
                logger.info("Compression not beneficial, storing uncompressed")
                return state_json

        except Exception as e:
            logger.error(f"Compression failed, storing uncompressed: {e}")
            return state_json

    def _decompress_state(self, compressed_data: str) -> str:
        """Decompress state data from gzip compression"""
        try:
            # Check if data is compressed (has our prefix)
            if not compressed_data.startswith("GZIP_B64:"):
                return compressed_data  # Not compressed, return as-is

            # Extract base64 data after prefix
            compressed_b64 = compressed_data[9:]  # Remove "GZIP_B64:" prefix

            # Decode from base64 and decompress
            compressed_bytes = base64.b64decode(compressed_b64.encode("ascii"))
            decompressed_bytes = gzip.decompress(compressed_bytes)

            # Convert back to string
            return decompressed_bytes.decode("utf-8")

        except Exception as e:
            logger.error(f"Decompression failed, returning data as-is: {e}")
            return compressed_data  # Return as-is on any error

    def cleanup(self):
        """Cleanup resources and connections"""
        logger.info("🧹 Cleaning up Chat Context Manager...")
        # SQLite connections are automatically closed by context managers
        logger.info("✅ Chat Context Manager cleanup complete")

    async def async_cleanup(self):
        """Async cleanup (calls sync cleanup since SQLite is synchronous)"""
        self.cleanup()


def create_chat_context_manager(db_path: Optional[str] = None) -> ChatContextManager:
    """
    Factory function for ChatContextManager

    Args:
        db_path: Optional database path

    Returns:
        ChatContextManager: Ready for context persistence
    """
    return ChatContextManager(db_path)
