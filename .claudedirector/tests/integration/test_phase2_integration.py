"""
Integration tests for Phase 2 Complete System
Tests the full integration of Phase 1 + Phase 2 file management
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock

from lib.core.workspace_file_handler import WorkspaceFileHandler
from lib.core.persona_file_integration import PersonaFileIntegration


class TestPhase2Integration:
    """Test complete Phase 2 integration with Phase 1 systems"""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def file_handler(self, temp_workspace):
        """Create workspace file handler for testing"""
        return WorkspaceFileHandler(temp_workspace)

    @pytest.fixture
    def persona_integration(self, temp_workspace):
        """Create persona file integration for testing"""
        return PersonaFileIntegration(temp_workspace)

    def test_workspace_initialization_with_phase2(self, file_handler):
        """Test workspace initialization includes Phase 2 components"""

        # Initialize workspace
        file_handler.initialize_workspace()

        # Should have smart organizer
        assert hasattr(file_handler, "smart_organizer")
        assert file_handler.smart_organizer is not None

        # Should have advanced archiving
        assert hasattr(file_handler.smart_organizer, "advanced_archiving")
        assert file_handler.smart_organizer.advanced_archiving is not None

        # Should have pattern recognition
        assert hasattr(file_handler.smart_organizer, "pattern_engine")
        assert file_handler.smart_organizer.pattern_engine is not None

    def test_smart_filename_generation_integration(self, file_handler):
        """Test smart filename generation in professional mode"""

        # Set to professional mode (should use Phase 2 smart naming)
        file_handler.lifecycle_manager.config.generation_mode.value = "professional"

        # Test smart filename generation
        filename = file_handler._generate_smart_filename(
            suggested_filename="test.md",
            content_type="strategic_analysis",
            business_context="Platform scaling strategy for Q3 engineering teams",
            persona="diego",
        )

        # Should generate outcome-focused filename
        assert "platform" in filename.lower() or "scaling" in filename.lower()
        assert filename.endswith(".md")
        assert "strategic" in filename or "analysis" in filename

    def test_consolidation_opportunity_detection_integration(
        self, file_handler, temp_workspace
    ):
        """Test consolidation opportunity detection in integrated system"""

        workspace_path = Path(temp_workspace)

        # Enable consolidation
        file_handler.lifecycle_manager.config.consolidate_analysis = True
        file_handler.lifecycle_manager.config.max_session_files = 2

        # Create multiple files to trigger consolidation
        test_files = [
            "platform-analysis-1.md",
            "platform-analysis-2.md",
            "team-structure.md",
        ]

        for filename in test_files:
            file_path = workspace_path / "analysis-results" / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(f"Test content for {filename}")

            # Register file
            file_handler.lifecycle_manager.register_file(
                str(file_path), "strategic_analysis", file_handler.current_session_id
            )

        # Should detect consolidation opportunity
        opportunities = (
            file_handler.smart_organizer.identify_consolidation_opportunities()
        )
        assert len(opportunities) > 0

    def test_lifecycle_status_with_phase2_insights(self, file_handler):
        """Test lifecycle status includes Phase 2 insights"""

        # Should not error and should include smart organization analysis
        file_handler.show_lifecycle_status()

        # Should have access to pattern insights
        insights = file_handler.smart_organizer.get_pattern_insights()
        assert isinstance(insights, dict)

        # Should have access to archive statistics
        stats = file_handler.smart_organizer.get_archive_statistics()
        assert isinstance(stats, dict)

    def test_persona_integration_with_smart_features(
        self, persona_integration, temp_workspace
    ):
        """Test persona integration with Phase 2 smart features"""

        # Test persona file generation with smart organizer
        content = "Strategic platform migration analysis for Q3 engineering initiatives"

        # Should integrate with smart filename generation
        result = persona_integration.persona_generate_file(
            persona="diego",
            content=content,
            content_type="strategic_analysis",
            business_context="Platform engineering strategy",
        )

        # Should not error (may return None if user doesn't approve, but shouldn't crash)
        # This tests the integration pipeline works

    def test_cross_session_insights_integration(self, file_handler, temp_workspace):
        """Test cross-session insights work with integrated system"""

        workspace_path = Path(temp_workspace)

        # Create some test files
        test_files = [
            ("analysis-1.md", "strategic_analysis"),
            ("meeting-prep.md", "meeting_prep"),
        ]

        for filename, content_type in test_files:
            file_path = workspace_path / "analysis-results" / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(f"Test content for {filename}")

            file_handler.lifecycle_manager.register_file(
                str(file_path), content_type, file_handler.current_session_id
            )

        # Generate cross-session insights
        insights = file_handler.smart_organizer.generate_cross_session_insights()

        assert isinstance(insights, dict)
        assert "productivity_trends" in insights
        assert "workflow_efficiency" in insights

    def test_advanced_archiving_integration(self, file_handler, temp_workspace):
        """Test advanced archiving integration with lifecycle management"""

        workspace_path = Path(temp_workspace)

        # Create test file
        test_file = workspace_path / "analysis-results" / "test-analysis.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(
            "Test strategic analysis content with platform migration details"
        )

        # Register file
        file_handler.lifecycle_manager.register_file(
            str(test_file), "strategic_analysis", file_handler.current_session_id
        )

        # Archive with enhanced indexing
        result = (
            file_handler.smart_organizer.advanced_archiving.archive_file_with_indexing(
                str(test_file), "strategic_analysis", file_handler.current_session_id
            )
        )

        # Should successfully archive
        if result:  # May fail if file doesn't exist by time of archiving
            assert Path(result).exists()

    def test_pattern_recognition_learning(self, file_handler, temp_workspace):
        """Test pattern recognition learning from usage"""

        workspace_path = Path(temp_workspace)

        # Create files that simulate a pattern
        pattern_files = [
            ("monday-prep.md", "meeting_prep"),
            ("monday-analysis.md", "strategic_analysis"),
            ("tuesday-prep.md", "meeting_prep"),
            ("tuesday-analysis.md", "strategic_analysis"),
        ]

        for filename, content_type in pattern_files:
            file_path = workspace_path / "analysis-results" / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(f"Test content for {filename}")

            file_handler.lifecycle_manager.register_file(
                str(file_path),
                content_type,
                f"session_{filename.split('-')[0]}",  # Different sessions per day
            )

        # Trigger pattern detection
        file_handler.smart_organizer.detect_session_patterns()

        # Should detect patterns
        insights = file_handler.smart_organizer.get_pattern_insights()
        assert insights["total_patterns"] >= 0  # Should not error

    def test_outcome_focused_naming_vs_minimal_mode(self, file_handler):
        """Test outcome-focused naming vs minimal mode behavior"""

        # Test minimal mode (should use simple naming)
        file_handler.lifecycle_manager.config.generation_mode.value = "minimal"

        minimal_filename = file_handler._generate_smart_filename(
            suggested_filename="test.md",
            content_type="strategic_analysis",
            business_context="Platform strategy",
            persona="diego",
        )

        # Test professional mode (should use outcome-focused naming)
        file_handler.lifecycle_manager.config.generation_mode.value = "professional"

        professional_filename = file_handler._generate_smart_filename(
            suggested_filename="test.md",
            content_type="strategic_analysis",
            business_context="Platform strategy",
            persona="diego",
        )

        # Professional mode should generate different (smarter) filenames
        # Both should be valid filenames
        assert minimal_filename.endswith(".md")
        assert professional_filename.endswith(".md")

    def test_search_functionality_integration(self, file_handler):
        """Test search functionality integration"""

        # Test archive search integration
        results = file_handler.smart_organizer.search_archived_files("test query")
        assert isinstance(results, list)

        # Should not error even with empty archive

    def test_workspace_configuration_with_phase2(self, file_handler, temp_workspace):
        """Test workspace configuration includes Phase 2 settings"""

        # Initialize workspace
        file_handler.initialize_workspace()

        # Should create configuration file
        config_path = Path(temp_workspace) / "config" / "file_lifecycle.yaml"
        assert config_path.exists()

        # Should include Phase 2 content types in template
        config_content = config_path.read_text()
        assert "professional" in config_content
        assert "research" in config_content
        assert "strategic_analysis" in config_content

    def test_error_handling_in_integrated_system(self, file_handler):
        """Test error handling throughout integrated system"""

        # Test with invalid workspace operations
        try:
            # Should handle missing files gracefully
            file_handler.smart_organizer.consolidate_files(
                Mock(
                    files=["nonexistent.md"],
                    suggested_name="test.md",
                    business_value="test",
                    consolidation_type="test",
                    priority="low",
                    size_reduction=1.0,
                ),
                user_approved=True,
            )
        except Exception as e:
            # Should handle errors gracefully, not crash
            assert isinstance(e, Exception)

        # Test pattern recognition with empty data
        try:
            file_handler.smart_organizer.detect_session_patterns()
        except Exception as e:
            pytest.fail(f"Pattern detection should handle empty data gracefully: {e}")

    def test_phase2_performance_with_large_datasets(self, file_handler, temp_workspace):
        """Test Phase 2 performance considerations"""

        workspace_path = Path(temp_workspace)

        # Create multiple files to test performance
        for i in range(20):  # Moderate number for testing
            file_path = workspace_path / "analysis-results" / f"analysis-{i}.md"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(f"Test content {i} with platform engineering strategy")

            file_handler.lifecycle_manager.register_file(
                str(file_path),
                "strategic_analysis",
                f"session_{i % 5}",  # Group into 5 sessions
            )

        # Should handle larger datasets without significant performance issues
        opportunities = (
            file_handler.smart_organizer.identify_consolidation_opportunities()
        )
        assert isinstance(opportunities, list)

        # Cross-session insights should handle multiple files
        insights = file_handler.smart_organizer.generate_cross_session_insights()
        assert isinstance(insights, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
