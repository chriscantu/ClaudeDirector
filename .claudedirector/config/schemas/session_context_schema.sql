-- Session Context Preservation Schema Extension
-- Critical enhancement for ClaudeDirector framework context continuity

-- Session context tracking for restart recovery
CREATE TABLE IF NOT EXISTS session_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,  -- UUID for session identification
    session_type TEXT NOT NULL,  -- 'strategic', 'executive', 'planning', 'technical'

    -- Context preservation data
    active_personas TEXT,  -- JSON array of currently activated personas
    stakeholder_context TEXT,  -- JSON with current stakeholder relationship state
    strategic_initiatives_context TEXT,  -- JSON with active initiatives and status
    executive_context TEXT,  -- JSON with ongoing executive discussions/preparations
    roi_discussions_context TEXT,  -- JSON with ROI strategy conversations
    coalition_mapping_context TEXT,  -- JSON with current stakeholder coalition state

    -- Conversation state
    conversation_thread TEXT,  -- JSON with key conversation context points
    decision_context TEXT,  -- JSON with pending/recent strategic decisions
    action_items_context TEXT,  -- JSON with active action items and owners

    -- Session metadata
    last_backup_timestamp TIMESTAMP NOT NULL,
    session_start_timestamp TIMESTAMP NOT NULL,
    session_end_timestamp TIMESTAMP,
    context_quality_score REAL,  -- 0.0-1.0 score of context completeness

    -- Recovery metadata
    recovery_priority TEXT DEFAULT 'medium',  -- 'critical', 'high', 'medium', 'low'
    context_validation_status TEXT DEFAULT 'pending',  -- 'validated', 'pending', 'incomplete'
    manual_recovery_required BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session backup checkpoints for granular recovery
CREATE TABLE IF NOT EXISTS session_checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    checkpoint_type TEXT NOT NULL,  -- 'auto', 'manual', 'critical_event'

    -- Checkpoint data
    context_snapshot TEXT NOT NULL,  -- JSON snapshot of complete context
    trigger_event TEXT,  -- What triggered this checkpoint

    -- Metadata
    checkpoint_timestamp TIMESTAMP NOT NULL,
    context_delta TEXT,  -- JSON with changes since last checkpoint

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id) REFERENCES session_context(session_id)
);

-- Context gap tracking for recovery management
CREATE TABLE IF NOT EXISTS context_gaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    gap_type TEXT NOT NULL,  -- 'stakeholder_missing', 'initiative_incomplete', 'roi_context_lost'

    -- Gap details
    gap_description TEXT NOT NULL,
    severity TEXT NOT NULL,  -- 'critical', 'high', 'medium', 'low'
    required_for_continuity BOOLEAN DEFAULT TRUE,

    -- Recovery information
    recovery_strategy TEXT,  -- JSON with suggested recovery actions
    recovery_status TEXT DEFAULT 'identified',  -- 'identified', 'in_progress', 'resolved', 'accepted'
    manual_input_required BOOLEAN DEFAULT FALSE,

    -- Context
    detected_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id) REFERENCES session_context(session_id)
);

-- Recovery protocol tracking
CREATE TABLE IF NOT EXISTS session_recovery_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    recovery_event_type TEXT NOT NULL,  -- 'session_restore', 'context_validation', 'gap_resolution'

    -- Recovery details
    recovery_action TEXT NOT NULL,
    success_status BOOLEAN NOT NULL,
    context_before TEXT,  -- JSON snapshot before recovery
    context_after TEXT,   -- JSON snapshot after recovery

    -- Performance metrics
    recovery_duration_ms INTEGER,
    user_intervention_required BOOLEAN DEFAULT FALSE,

    -- Context
    performed_at TIMESTAMP NOT NULL,
    performed_by TEXT DEFAULT 'system',  -- 'system', 'user', 'manual'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id) REFERENCES session_context(session_id)
);

-- Indexes for optimal performance
CREATE INDEX IF NOT EXISTS idx_session_context_session_id ON session_context(session_id);
CREATE INDEX IF NOT EXISTS idx_session_context_type ON session_context(session_type);
CREATE INDEX IF NOT EXISTS idx_session_context_backup_timestamp ON session_context(last_backup_timestamp);
CREATE INDEX IF NOT EXISTS idx_session_checkpoints_session_id ON session_checkpoints(session_id);
CREATE INDEX IF NOT EXISTS idx_session_checkpoints_timestamp ON session_checkpoints(checkpoint_timestamp);
CREATE INDEX IF NOT EXISTS idx_context_gaps_session_id ON context_gaps(session_id);
CREATE INDEX IF NOT EXISTS idx_context_gaps_severity ON context_gaps(severity);
CREATE INDEX IF NOT EXISTS idx_recovery_log_session_id ON session_recovery_log(session_id);
CREATE INDEX IF NOT EXISTS idx_recovery_log_timestamp ON session_recovery_log(performed_at);
