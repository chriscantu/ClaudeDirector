#!/usr/bin/env python3
"""
Initialize strategic memory database for CI environment
Ensures the database exists with proper schema for P0 conversation tracking tests
"""

import sqlite3
import sys
from pathlib import Path


def create_strategic_database(db_path: str):
    """Create strategic memory database with required schema"""

    # Ensure directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        # Create session context tables (matching actual schema)
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS session_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                session_type TEXT NOT NULL,

                -- Context preservation data
                active_personas TEXT,
                stakeholder_context TEXT,
                strategic_initiatives_context TEXT,
                executive_context TEXT,
                roi_discussions_context TEXT,
                coalition_mapping_context TEXT,

                -- Conversation state
                conversation_thread TEXT,
                decision_context TEXT,
                action_items_context TEXT,

                -- Session metadata
                last_backup_timestamp TIMESTAMP NOT NULL,
                session_start_timestamp TIMESTAMP NOT NULL,
                session_end_timestamp TIMESTAMP,
                context_quality_score REAL,

                -- Recovery metadata
                recovery_priority TEXT DEFAULT 'medium',
                context_validation_status TEXT DEFAULT 'pending',
                manual_recovery_required BOOLEAN DEFAULT FALSE,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS context_gaps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                gap_type TEXT NOT NULL,
                gap_description TEXT NOT NULL,
                severity TEXT NOT NULL,
                gap_details TEXT,
                suggested_action TEXT,
                priority_level INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                resolution_notes TEXT,
                FOREIGN KEY (session_id) REFERENCES session_context(session_id)
            );

            -- Create indexes for performance
            CREATE INDEX IF NOT EXISTS idx_session_context_session_id ON session_context(session_id);
            CREATE INDEX IF NOT EXISTS idx_session_context_type ON session_context(session_type);
            CREATE INDEX IF NOT EXISTS idx_session_context_backup_timestamp ON session_context(last_backup_timestamp);
        """
        )

        # Create test data for P0 tests
        conn.execute(
            """
            INSERT OR IGNORE INTO session_context
            (session_id, session_type, active_personas, conversation_thread,
             last_backup_timestamp, session_start_timestamp, context_quality_score)
            VALUES
            ('test-session-001', 'strategic', '["diego", "rachel"]',
             '{"summary": "Test strategic conversation"}',
             datetime('now'), datetime('now'), 0.85)
        """
        )

        conn.commit()

    print(f"✅ Strategic memory database initialized at {db_path}")
    return True


def main():
    """Initialize database for CI environment"""

    # Default path that tests expect
    db_path = "data/strategic_memory.db"

    if len(sys.argv) > 1:
        db_path = sys.argv[1]

    try:
        create_strategic_database(db_path)
        print("✅ Database initialization successful")
        return 0
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
