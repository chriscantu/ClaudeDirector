"""
Integration tests for Smart File Organizer Phase 2
Tests session consolidation, outcome naming, and pattern recognition
"""

import pytest
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from lib.core.file_lifecycle_manager import (
    FileLifecycleManager,
    FileMetadata,
    FileRetentionStatus,
    GenerationMode,
)
from lib.core.smart_file_organizer import (
    SmartFileOrganizer,
    ConsolidationOpportunity,
)
from lib.core.advanced_archiving import AdvancedArchivingSystem
from lib.core.pattern_recognition import PatternRecognitionEngine


class TestSmartFileOrganizer:
    """Test Smart File Organizer Phase 2 functionality"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def lifecycle_manager(self, temp_workspace):
        """Create lifecycle manager for testing"""
        return FileLifecycleManager(temp_workspace)

    @pytest.fixture
    def smart_organizer(self, lifecycle_manager):
        """Create smart organizer for testing"""
        return SmartFileOrganizer(lifecycle_manager)

    def test_outcome_focused_filename_generation(self, smart_organizer):
        """Test outcome-focused filename generation"""

        # Test platform context
        filename = smart_organizer.generate_outcome_focused_filename(
            content_preview="Platform migration strategy for Q3 scaling initiative",
            content_type="strategic_analysis",
            business_context="Platform architecture roadmap discussion",
            persona="diego",
        )

        assert "platform" in filename.lower()
        assert "migration" in filename.lower() or "scaling" in filename.lower()
        assert filename.endswith(".md")

        # Test quarterly planning context
        filename = smart_organizer.generate_outcome_focused_filename(
            content_preview="Q4 objectives and key results planning",
            content_type="quarterly_planning",
            business_context="Strategic planning session",
            persona="alvaro",
        )

        assert "q4" in filename.lower() or "quarterly" in filename.lower()
        assert filename.endswith(".md")

    def test_business_context_detection(self, smart_organizer):
        """Test business context detection from content"""

        # Test platform context
        contexts = smart_organizer._detect_business_contexts(
            "Platform migration and infrastructure scaling for engineering teams"
        )
        assert "platform" in contexts
        assert "team" in contexts

        # Test strategy context
        contexts = smart_organizer._detect_business_contexts(
            "Strategic roadmap planning for quarterly objectives"
        )
        assert "strategy" in contexts
        assert "quarterly" in contexts

        # Test stakeholder context
        contexts = smart_organizer._detect_business_contexts(
            "Executive stakeholder communication and board presentation"
        )
        assert "stakeholder" in contexts

    def test_consolidation_opportunity_identification(
        self, smart_organizer, temp_workspace
    ):
        """Test identification of consolidation opportunities"""

        # Create test files with metadata
        workspace_path = Path(temp_workspace)
        test_files = [
            ("platform-analysis-1.md", "strategic_analysis"),
            ("platform-analysis-2.md", "strategic_analysis"),
            ("team-structure.md", "strategic_analysis"),
            ("meeting-prep.md", "meeting_prep"),
        ]

        session_id = "test_session_123"

        # Create files and metadata
        for filename, content_type in test_files:
            file_path = workspace_path / "analysis-results" / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(f"Test content for {filename}")

            # Register with lifecycle manager
            metadata = FileMetadata(
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                retention_status=FileRetentionStatus.STANDARD,
                generation_mode=GenerationMode.PROFESSIONAL,
                content_type=content_type,
                session_id=session_id,
            )
            smart_organizer.lifecycle_manager.metadata_store[str(file_path)] = metadata

        # Test consolidation opportunity detection
        opportunities = smart_organizer.identify_consolidation_opportunities()

        assert len(opportunities) > 0

        # Check for session-based opportunity
        session_opportunity = next(
            (
                opp
                for opp in opportunities
                if opp.consolidation_type == "session_summary"
            ),
            None,
        )
        assert session_opportunity is not None
        assert (
            len(session_opportunity.files) >= 3
        )  # Should find multiple files from same session

    def test_smart_consolidation_execution(self, smart_organizer, temp_workspace):
        """Test smart consolidation execution"""

        workspace_path = Path(temp_workspace)

        # Create test files
        test_files = [
            "strategic-analysis-1.md",
            "strategic-analysis-2.md",
            "meeting-prep.md",
        ]

        file_paths = []
        for filename in test_files:
            file_path = workspace_path / "analysis-results" / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(
                f"# {filename}\n\nTest strategic content for {filename}"
            )
            file_paths.append(str(file_path))

        # Create consolidation opportunity
        opportunity = ConsolidationOpportunity(
            files=file_paths,
            suggested_name="consolidated-strategic-analysis.md",
            business_value="Test strategic analysis consolidation",
            consolidation_type="session_summary",
            priority="high",
            size_reduction=2.5,
        )

        # Execute consolidation
        result = smart_organizer.consolidate_files(opportunity, user_approved=True)

        assert result is not None
        consolidated_path = Path(result)
        assert consolidated_path.exists()

        # Check consolidated content
        content = consolidated_path.read_text()
        assert "Test strategic analysis consolidation" in content
        assert "strategic-analysis-1.md" in content
        assert "strategic-analysis-2.md" in content

    def test_pattern_recognition_integration(self, smart_organizer):
        """Test pattern recognition engine integration"""

        # Test pattern engine exists
        assert smart_organizer.pattern_engine is not None
        assert isinstance(smart_organizer.pattern_engine, PatternRecognitionEngine)

        # Test pattern insights generation
        insights = smart_organizer.get_pattern_insights()
        assert isinstance(insights, dict)
        assert "total_patterns" in insights
        assert "template_recommendations" in insights

    def test_advanced_archiving_integration(self, smart_organizer):
        """Test advanced archiving system integration"""

        # Test archiving system exists
        assert smart_organizer.advanced_archiving is not None
        assert isinstance(smart_organizer.advanced_archiving, AdvancedArchivingSystem)

        # Test archive statistics
        stats = smart_organizer.get_archive_statistics()
        assert isinstance(stats, dict)
        assert "total_files" in stats

    def test_cross_session_insights_generation(self, smart_organizer, temp_workspace):
        """Test cross-session insights generation"""

        workspace_path = Path(temp_workspace)

        # Create test files from different time periods
        base_time = datetime.now()
        test_files = [
            ("week1-analysis.md", base_time - timedelta(days=7), "strategic_analysis"),
            ("week2-analysis.md", base_time - timedelta(days=3), "strategic_analysis"),
            ("current-analysis.md", base_time, "meeting_prep"),
        ]

        for filename, created_time, content_type in test_files:
            file_path = workspace_path / "analysis-results" / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(f"Test content for {filename}")

            metadata = FileMetadata(
                created_at=created_time,
                last_accessed=created_time,
                retention_status=FileRetentionStatus.STANDARD,
                generation_mode=GenerationMode.PROFESSIONAL,
                content_type=content_type,
            )
            smart_organizer.lifecycle_manager.metadata_store[str(file_path)] = metadata

        # Generate cross-session insights
        insights = smart_organizer.generate_cross_session_insights()

        assert isinstance(insights, dict)
        assert "productivity_trends" in insights
        assert "content_type_evolution" in insights
        assert "business_context_focus" in insights
        assert "workflow_efficiency" in insights
        assert "pattern_recommendations" in insights

        # Check productivity trends
        productivity = insights["productivity_trends"]
        assert "weekly_file_counts" in productivity
        assert "trend" in productivity
        assert "total_files_30_days" in productivity

    def test_workflow_optimization_suggestions(self, smart_organizer):
        """Test workflow optimization suggestions"""

        suggestions = smart_organizer.suggest_workflow_optimizations()
        assert isinstance(suggestions, list)

        # Should return suggestions even with empty patterns
        # (may be empty list, but should not error)

    def test_archive_search_functionality(self, smart_organizer, temp_workspace):
        """Test archive search functionality"""

        # Test search interface exists
        results = smart_organizer.search_archived_files("test query", limit=5)
        assert isinstance(results, list)

        # Should return empty list for new workspace, but not error

    def test_business_context_extraction_accuracy(self, smart_organizer):
        """Test accuracy of business context extraction"""

        test_cases = [
            ("Platform migration strategy", ["platform"]),
            ("Team hiring and organizational structure", ["team"]),
            ("Strategic roadmap planning", ["strategy"]),
            ("Executive stakeholder communication", ["stakeholder"]),
            ("Budget planning and ROI analysis", ["budget"]),
            ("Quarterly objectives and key results", ["quarterly", "strategy"]),
        ]

        for content, expected_contexts in test_cases:
            detected = smart_organizer._detect_business_contexts(content)

            # Should detect at least one expected context
            assert any(
                context in detected for context in expected_contexts
            ), f"Failed to detect {expected_contexts} in '{content}', got {detected}"

    def test_session_pattern_detection(self, smart_organizer, temp_workspace):
        """Test session pattern detection"""

        workspace_path = Path(temp_workspace)

        # Create files that simulate a pattern
        session_files = [
            ("monday-planning.md", "meeting_prep"),
            ("monday-analysis.md", "strategic_analysis"),
            ("monday-summary.md", "session_summary"),
        ]

        session_id = "monday_pattern_session"

        for filename, content_type in session_files:
            file_path = workspace_path / "analysis-results" / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(f"Test content for {filename}")

            metadata = FileMetadata(
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                retention_status=FileRetentionStatus.STANDARD,
                generation_mode=GenerationMode.PROFESSIONAL,
                content_type=content_type,
                session_id=session_id,
            )
            smart_organizer.lifecycle_manager.metadata_store[str(file_path)] = metadata

        # Detect patterns
        smart_organizer.detect_session_patterns()

        # Should not error and should update patterns
        assert smart_organizer.session_patterns is not None


class TestAdvancedArchivingSystem:
    """Test Advanced Archiving System functionality"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def archiving_system(self, temp_workspace):
        """Create archiving system for testing"""
        return AdvancedArchivingSystem(temp_workspace)

    def test_business_context_extraction(self, archiving_system):
        """Test business context extraction from content"""

        # Test platform context extraction
        content = "Platform migration strategy for scaling infrastructure across engineering teams"
        context = archiving_system._extract_business_context(content)

        assert "platform-migration" in context or "platform-scaling" in context
        assert "team" in context.lower() or "infrastructure" in context

        # Test stakeholder context extraction
        content = "Executive stakeholder communication for board presentation"
        context = archiving_system._extract_business_context(content)

        assert "executive" in context.lower() or "stakeholder" in context.lower()

    def test_keyword_extraction(self, archiving_system):
        """Test keyword extraction for search indexing"""

        content = """
        # Platform Migration Strategy

        This document outlines the strategic approach for platform migration,
        focusing on infrastructure scaling and team coordination.

        ## Key Objectives
        - Migrate legacy systems
        - Scale infrastructure
        - Coordinate engineering teams
        """

        keywords = archiving_system._extract_keywords(content)

        assert "platform" in keywords
        assert "migration" in keywords
        assert "infrastructure" in keywords
        assert "team" in keywords or "teams" in keywords

    def test_retention_score_calculation(self, archiving_system):
        """Test retention score calculation"""

        # Test high-value content
        high_value_content = (
            "Executive board presentation ROI analysis quarterly strategic planning"
        )
        score = archiving_system._calculate_retention_score(
            high_value_content, "executive_presentation"
        )

        assert score >= 8.0  # Should be high value

        # Test lower-value content
        low_value_content = "Basic meeting notes"
        score = archiving_system._calculate_retention_score(
            low_value_content, "session_summary"
        )

        assert score < 8.0  # Should be lower value

    def test_database_initialization(self, archiving_system):
        """Test SQLite database initialization"""

        # Database should be initialized
        assert archiving_system.index_db_path.exists()

        # Should be able to query (even if empty)
        import sqlite3

        with sqlite3.connect(str(archiving_system.index_db_path)) as conn:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            assert "archived_files" in tables
            assert "archived_files_fts" in tables


class TestPatternRecognitionEngine:
    """Test Pattern Recognition Engine functionality"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def pattern_engine(self, temp_workspace):
        """Create pattern recognition engine for testing"""
        return PatternRecognitionEngine(temp_workspace)

    def test_workflow_pattern_analysis(self, pattern_engine):
        """Test workflow pattern analysis"""

        # Create test session data
        session_data = [
            {
                "session_id": "weekly_session_1",
                "content_type": "meeting_prep",
                "created_at": "2024-08-05T09:00:00",
                "business_context": "weekly planning",
            },
            {
                "session_id": "weekly_session_1",
                "content_type": "strategic_analysis",
                "created_at": "2024-08-05T10:00:00",
                "business_context": "team structure",
            },
            {
                "session_id": "weekly_session_2",
                "content_type": "meeting_prep",
                "created_at": "2024-08-12T09:00:00",
                "business_context": "weekly planning",
            },
            {
                "session_id": "weekly_session_2",
                "content_type": "strategic_analysis",
                "created_at": "2024-08-12T10:00:00",
                "business_context": "platform strategy",
            },
        ]

        patterns = pattern_engine.analyze_user_patterns(session_data)

        assert isinstance(patterns, list)
        # Should detect some pattern from the data

    def test_template_recommendation_generation(self, pattern_engine):
        """Test template recommendation generation"""

        from lib.core.pattern_recognition import WorkflowPattern

        # Create test pattern
        test_pattern = WorkflowPattern(
            pattern_id="weekly_planning_sequence",
            pattern_name="Weekly Strategic Planning",
            trigger_contexts=["weekly", "planning"],
            typical_sequence=["meeting_prep", "strategic_analysis", "session_summary"],
            frequency="weekly",
            confidence=0.85,
            business_value="Consistent weekly strategic planning workflow",
            template_suggestion="weekly_planning_template",
        )

        recommendations = pattern_engine.generate_template_recommendations(
            [test_pattern]
        )

        assert isinstance(recommendations, list)
        if recommendations:  # May be empty for unknown patterns
            rec = recommendations[0]
            assert hasattr(rec, "template_name")
            assert hasattr(rec, "confidence")

    def test_workflow_optimization_suggestions(self, pattern_engine):
        """Test workflow optimization suggestions"""

        from lib.core.pattern_recognition import WorkflowPattern

        # Create high-confidence pattern
        high_confidence_pattern = WorkflowPattern(
            pattern_id="daily_standup_sequence",
            pattern_name="Daily Team Standup",
            trigger_contexts=["daily", "standup"],
            typical_sequence=["meeting_prep"],
            frequency="daily",
            confidence=0.9,
            business_value="Daily team coordination",
            template_suggestion="daily_standup_template",
        )

        suggestions = pattern_engine.suggest_workflow_optimizations(
            [high_confidence_pattern]
        )

        assert isinstance(suggestions, list)
        # Should provide suggestions for high-confidence patterns

    def test_pattern_insights_generation(self, pattern_engine):
        """Test pattern insights generation"""

        insights = pattern_engine.get_pattern_insights()

        assert isinstance(insights, dict)
        assert "total_patterns" in insights
        assert "high_confidence_patterns" in insights
        assert "pattern_frequency_distribution" in insights
        assert "top_patterns" in insights
        assert "template_recommendations" in insights

        # Should not error even with no patterns
        assert insights["total_patterns"] >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
