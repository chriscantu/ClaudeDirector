#!/usr/bin/env python3
"""
Unit Tests for Duration-Agnostic Jira Reporter
Phase 0, Task 0.1.1: TDD RED Phase - Write Tests First

Tests the JiraReporter base class with duration parameterization.
Following BLOAT_PREVENTION principles: test duration-agnostic functionality.

Author: ClaudeDirector AI Framework (Martin)
Version: 1.0.0 (Phase 0)
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path


class TestJiraReporterDurationLabels:
    """Test duration label generation for different time periods"""

    def test_duration_label_weekly(self):
        """Weekly report (7 days) should return 'Weekly' label"""
        # Import will fail initially (RED phase)
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter
        
        # Test duration label generation
        label = JiraReporter._get_duration_label(7)
        assert label == "Weekly", "7 days should map to 'Weekly'"

    def test_duration_label_90day(self):
        """90-day report should return '90-Day' label"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter
        
        label = JiraReporter._get_duration_label(90)
        assert label == "90-Day", "90 days should map to '90-Day'"

    def test_duration_label_monthly(self):
        """30-day report should return 'Monthly' label"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter
        
        label = JiraReporter._get_duration_label(30)
        assert label == "Monthly", "30 days should map to 'Monthly'"

    def test_duration_label_multi_week(self):
        """14-day report should return '2-Week' label"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter
        
        label = JiraReporter._get_duration_label(14)
        assert label == "2-Week", "14 days should map to '2-Week'"

    def test_duration_label_custom_days(self):
        """45-day report should return '45-Day' label"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter
        
        label = JiraReporter._get_duration_label(45)
        assert label == "45-Day", "45 days should map to '45-Day'"

    def test_duration_label_quarterly(self):
        """Quarterly report (91 days) should return '91-Day' or 'Quarterly'"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter
        
        label = JiraReporter._get_duration_label(91)
        # Accept either format for quarterly
        assert label in ["91-Day", "Quarterly"], "91 days should map to quarterly format"


class TestJiraReporterInitialization:
    """Test JiraReporter initialization with duration parameter"""

    def test_duration_parameter_defaults_to_7(self):
        """JiraReporter should default to 7 days (weekly) if not specified"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter, ConfigManager
        
        # Mock config
        mock_config = ConfigManager.__new__(ConfigManager)
        mock_config.config = {
            "jira": {"base_url": "https://test.atlassian.net", "auth": {"email": "test@test.com", "api_token": "test"}},
            "jql_queries": {}
        }
        
        reporter = JiraReporter(mock_config)
        assert reporter.duration_days == 7, "Default duration should be 7 days"
        assert reporter.duration_label == "Weekly", "Default label should be 'Weekly'"

    def test_duration_parameter_accepts_custom_value(self):
        """JiraReporter should accept custom duration_days parameter"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter, ConfigManager
        
        mock_config = ConfigManager.__new__(ConfigManager)
        mock_config.config = {
            "jira": {"base_url": "https://test.atlassian.net", "auth": {"email": "test@test.com", "api_token": "test"}},
            "jql_queries": {}
        }
        
        reporter = JiraReporter(mock_config, duration_days=90)
        assert reporter.duration_days == 90, "Duration should be set to 90 days"
        assert reporter.duration_label == "90-Day", "Label should be '90-Day'"

    def test_duration_label_set_on_init(self):
        """Duration label should be automatically set during initialization"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter, ConfigManager
        
        mock_config = ConfigManager.__new__(ConfigManager)
        mock_config.config = {
            "jira": {"base_url": "https://test.atlassian.net", "auth": {"email": "test@test.com", "api_token": "test"}},
            "jql_queries": {}
        }
        
        reporter = JiraReporter(mock_config, duration_days=30)
        assert hasattr(reporter, 'duration_label'), "Reporter should have duration_label attribute"
        assert reporter.duration_label == "Monthly", "30-day label should be 'Monthly'"


class TestJiraReporterDateRangeCalculation:
    """Test date range calculation for different durations"""

    def test_calculate_date_range_weekly(self):
        """Weekly report should calculate 7-day range"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter, ConfigManager
        
        mock_config = ConfigManager.__new__(ConfigManager)
        mock_config.config = {
            "jira": {"base_url": "https://test.atlassian.net", "auth": {"email": "test@test.com", "api_token": "test"}},
            "jql_queries": {}
        }
        
        reporter = JiraReporter(mock_config, duration_days=7)
        end_date = datetime.now()
        start_date = reporter._calculate_start_date(end_date)
        
        expected_start = end_date - timedelta(days=7)
        assert abs((start_date - expected_start).total_seconds()) < 1, "Start date should be 7 days before end date"

    def test_calculate_date_range_90day(self):
        """90-day report should calculate 90-day range"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter, ConfigManager
        
        mock_config = ConfigManager.__new__(ConfigManager)
        mock_config.config = {
            "jira": {"base_url": "https://test.atlassian.net", "auth": {"email": "test@test.com", "api_token": "test"}},
            "jql_queries": {}
        }
        
        reporter = JiraReporter(mock_config, duration_days=90)
        end_date = datetime.now()
        start_date = reporter._calculate_start_date(end_date)
        
        expected_start = end_date - timedelta(days=90)
        assert abs((start_date - expected_start).total_seconds()) < 1, "Start date should be 90 days before end date"


class TestBLOATPrevention:
    """Test BLOAT_PREVENTION compliance - ensure no duplication"""

    def test_jira_reporter_module_exists(self):
        """jira_reporter.py module should exist"""
        # Tests are in: .claudedirector/tests/unit/reporting/test_jira_reporter.py
        # Module is in: .claudedirector/lib/reporting/jira_reporter.py
        # __file__.parent = reporting, parent.parent = unit, parent.parent.parent = tests, parent^4 = .claudedirector
        # Simplest: use absolute path from project root
        project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        jira_reporter_path = project_root / ".claudedirector" / "lib" / "reporting" / "jira_reporter.py"
        assert jira_reporter_path.exists(), f"jira_reporter.py should exist at {jira_reporter_path}"

    def test_no_duplicate_duration_logic_in_weekly_reporter(self):
        """weekly_reporter.py should NOT duplicate duration logic"""
        weekly_reporter_path = Path(__file__).parent.parent.parent / "lib" / "reporting" / "weekly_reporter.py"
        
        if weekly_reporter_path.exists():
            content = weekly_reporter_path.read_text()
            
            # After refactoring, weekly_reporter should import JiraReporter
            assert "from .jira_reporter import" in content or "from reporting.jira_reporter import" in content, \
                "weekly_reporter.py should import from jira_reporter (DRY compliance)"

    def test_single_source_of_truth_for_duration(self):
        """Verify single source of truth: jira_reporter owns duration logic"""
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from lib.reporting.jira_reporter import JiraReporter
        
        # JiraReporter should have _get_duration_label as class/static method
        assert hasattr(JiraReporter, '_get_duration_label'), \
            "JiraReporter should own _get_duration_label method (single source of truth)"


class TestBackwardCompatibility:
    """Test backward compatibility after refactoring"""

    def test_weekly_reporter_still_importable(self):
        """weekly_reporter.py module should still be importable"""
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from lib.reporting import weekly_reporter
            assert weekly_reporter is not None, "weekly_reporter module should still exist"
        except ImportError as e:
            pytest.fail(f"weekly_reporter should remain importable for backward compatibility: {e}")

    def test_weekly_reporter_classes_available(self):
        """Core classes should still be available from weekly_reporter (via imports)"""
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from lib.reporting.weekly_reporter import JiraClient, StrategicAnalyzer, ConfigManager
            
            assert JiraClient is not None, "JiraClient should be available"
            assert StrategicAnalyzer is not None, "StrategicAnalyzer should be available"
            assert ConfigManager is not None, "ConfigManager should be available"
        except ImportError as e:
            pytest.fail(f"Core classes should remain importable from weekly_reporter: {e}")


# TDD RED Phase: These tests will FAIL initially
# Expected failures:
# - ModuleNotFoundError: No module named '.claudedirector.lib.reporting.jira_reporter'
# - AttributeError: JiraReporter has no attribute '_get_duration_label'
# - AttributeError: JiraReporter has no attribute 'duration_days'
# 
# GREEN Phase (next): Implement jira_reporter.py to make these tests pass
# REFACTOR Phase (final): Clean up, add docstrings, optimize

