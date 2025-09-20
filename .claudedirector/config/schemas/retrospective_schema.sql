-- Weekly Retrospective System Schema Extension
-- Phase 1 Database Integration - EXTENDS existing database infrastructure
--
-- BLOAT_PREVENTION: REUSES existing patterns (timestamps, constraints, indexes, triggers)
-- ARCHITECTURE: Follows existing schema.sql conventions and data structures
-- DRY COMPLIANCE: NO duplication of database management patterns

-- REUSE existing timestamp, constraint, and indexing patterns from schema.sql
CREATE TABLE weekly_retrospectives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_ending DATE NOT NULL,
    progress_response TEXT NOT NULL,
    improvement_response TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 10),
    rating_explanation TEXT NOT NULL,
    themes_extracted TEXT, -- JSON array (follows existing JSON patterns)
    sentiment_scores TEXT, -- JSON object (follows existing JSON patterns)
    session_metadata TEXT, -- JSON object (follows existing metadata patterns)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- REUSE existing timestamp pattern
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- REUSE existing timestamp pattern
);

-- REUSE existing indexing patterns from schema.sql
CREATE INDEX idx_retrospectives_week_ending ON weekly_retrospectives(week_ending);
CREATE INDEX idx_retrospectives_rating ON weekly_retrospectives(rating);
CREATE INDEX idx_retrospectives_created ON weekly_retrospectives(created_at);

-- REUSE existing view patterns for trend analysis (follows platform_metrics_trending pattern)
CREATE VIEW retrospective_trends AS
SELECT
    week_ending,
    rating,
    themes_extracted,
    sentiment_scores,
    created_at
FROM weekly_retrospectives
ORDER BY week_ending DESC;

-- REUSE existing trigger patterns for timestamp updates (follows existing trigger structure)
CREATE TRIGGER update_retrospectives_timestamp
    AFTER UPDATE ON weekly_retrospectives
BEGIN
    UPDATE weekly_retrospectives SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Update schema metadata table to track retrospective extension
INSERT INTO schema_metadata (version, description) VALUES
('3.0.0', 'Weekly Retrospective System Phase 1 - Database schema extension following DRY principles');
