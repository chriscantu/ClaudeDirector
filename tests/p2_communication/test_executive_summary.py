"""
Test Executive Summary Generation

Comprehensive tests for P2.1 Executive Summary Generator.
Tests stakeholder-specific content, data handling, and output formatting.
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from typing import Dict, Any

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lib.claudedirector.p2_communication.report_generation.executive_summary import (
    ExecutiveSummaryGenerator, SummaryTemplate
)
from lib.claudedirector.p2_communication.interfaces.report_interface import (
    ReportContext, StakeholderType, ReportFormat, IDataSource
)


class MockDataSource(IDataSource):
    """Mock data source for testing."""

    def __init__(self, mock_data: Dict[str, Any]):
        self.mock_data = mock_data

    def get_data(self, time_period: str, metrics: list) -> Dict[str, Any]:
        return self.mock_data

    def get_data_freshness(self) -> str:
        return "2025-08-10 09:00:00"

    def is_available(self) -> bool:
        return True


class TestExecutiveSummaryGenerator(unittest.TestCase):
    """Test cases for Executive Summary Generator."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_data = {
            "team_velocity": {
                "current_sprint": 42,
                "last_sprint": 38,
                "trend": "increasing"
            },
            "risk_indicators": {
                "blocked_issues": 2,
                "overdue_issues": 3,
                "critical_bugs": 1
            },
            "initiative_health": {
                "on_track": 8,
                "at_risk": 2,
                "critical": 1
            },
            "cross_team_dependencies": {
                "total_dependencies": 12,
                "blocked_dependencies": 2
            },
            "data_freshness": "2025-08-10 09:00:00"
        }

        self.data_source = MockDataSource(self.mock_data)
        self.generator = ExecutiveSummaryGenerator(self.data_source)

    def test_generator_initialization(self):
        """Test that generator initializes correctly."""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.data_source, self.data_source)
        self.assertIsNone(self.generator.ai_client)
        self.assertIsInstance(self.generator.templates, dict)

    def test_supported_stakeholders(self):
        """Test that all expected stakeholder types are supported."""
        supported = self.generator.get_supported_stakeholders()

        expected_stakeholders = [
            StakeholderType.CEO,
            StakeholderType.VP_ENGINEERING,
            StakeholderType.BOARD,
            StakeholderType.PRODUCT_TEAM,
            StakeholderType.ENGINEERING_MANAGER
        ]

        for stakeholder in expected_stakeholders:
            self.assertIn(stakeholder, supported)

    def test_context_validation_valid(self):
        """Test context validation with valid context."""
        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        self.assertTrue(self.generator.validate_context(context))

    def test_context_validation_invalid_stakeholder(self):
        """Test context validation with invalid stakeholder."""
        # Create a mock stakeholder type that doesn't exist in templates
        # We'll patch the get_supported_stakeholders method to simulate this
        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        # Mock get_supported_stakeholders to return empty list
        with patch.object(self.generator, 'get_supported_stakeholders', return_value=[]):
            self.assertFalse(self.generator.validate_context(context))

    def test_context_validation_invalid_format(self):
        """Test context validation with invalid format."""
        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.JSON  # Not supported
        )

        self.assertFalse(self.generator.validate_context(context))

    def test_generate_report_ceo(self):
        """Test report generation for CEO stakeholder."""
        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        report = self.generator.generate_report(context)

        # Verify report structure
        self.assertIsNotNone(report)
        self.assertEqual(report.context.stakeholder_type, StakeholderType.CEO)
        self.assertGreater(len(report.sections), 0)
        self.assertIsNotNone(report.confidence_score)
        self.assertIn("jira", report.data_sources)

        # Verify CEO-specific content
        section_titles = [section.title for section in report.sections]
        self.assertIn("Executive Summary", section_titles)
        self.assertIn("Key Metrics", section_titles)

    def test_generate_report_vp_engineering(self):
        """Test report generation for VP Engineering stakeholder."""
        context = ReportContext(
            stakeholder_type=StakeholderType.VP_ENGINEERING,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        report = self.generator.generate_report(context)

        # Verify VP Engineering specific content
        section_titles = [section.title for section in report.sections]
        self.assertIn("Team Performance", section_titles)

        # Check for engineering-specific messaging
        summary_section = next(s for s in report.sections if s.title == "Executive Summary")
        self.assertIn("Team performance remains strong", summary_section.content)

    def test_generate_report_board(self):
        """Test report generation for Board stakeholder."""
        context = ReportContext(
            stakeholder_type=StakeholderType.BOARD,
            time_period="current_quarter",
            format=ReportFormat.CLI_RICH
        )

        report = self.generator.generate_report(context)

        # Verify Board-specific content exists (strategic initiatives section is generated when board stakeholder)
        # The board section is created in _generate_stakeholder_specific_sections
        section_titles = [section.title for section in report.sections]

        # Check that report was generated for board
        self.assertEqual(report.context.stakeholder_type, StakeholderType.BOARD)

        # Board reports should have fewer sections (max 3)
        self.assertLessEqual(len(report.sections), 3)

        # Should have executive summary and key metrics at minimum
        self.assertIn("Executive Summary", section_titles)
        self.assertIn("Key Metrics", section_titles)

    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        report = self.generator.generate_report(context)

        # With complete mock data, confidence should be high
        self.assertGreaterEqual(report.confidence_score, 0.8)
        self.assertLessEqual(report.confidence_score, 1.0)

    def test_confidence_calculation_missing_data(self):
        """Test confidence calculation with missing data."""
        # Create data source with incomplete data
        incomplete_data = {
            "team_velocity": {"current_sprint": 42},
            "data_freshness": "2025-08-10 09:00:00"
        }

        incomplete_source = MockDataSource(incomplete_data)
        generator = ExecutiveSummaryGenerator(incomplete_source)

        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        report = generator.generate_report(context)

        # With incomplete data, confidence should be lower
        self.assertLess(report.confidence_score, 0.8)

    def test_section_priority_ordering(self):
        """Test that sections are ordered by priority."""
        context = ReportContext(
            stakeholder_type=StakeholderType.VP_ENGINEERING,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        report = self.generator.generate_report(context)

        # Verify sections are in priority order (lower number = higher priority)
        priorities = [section.priority for section in report.sections]
        self.assertEqual(priorities, sorted(priorities))

    def test_stakeholder_relevant_filtering(self):
        """Test that sections are marked with relevant stakeholders."""
        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        report = self.generator.generate_report(context)

        # All sections should be relevant to CEO
        for section in report.sections:
            self.assertIn(StakeholderType.CEO, section.stakeholder_relevant)

    def test_risk_section_inclusion(self):
        """Test risk section inclusion based on context."""
        # Test with risks enabled
        context_with_risks = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH,
            include_risks=True
        )

        report_with_risks = self.generator.generate_report(context_with_risks)
        section_titles = [section.title for section in report_with_risks.sections]
        self.assertIn("Risks & Opportunities", section_titles)

        # Test with risks disabled
        context_without_risks = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH,
            include_risks=False
        )

        report_without_risks = self.generator.generate_report(context_without_risks)
        section_titles = [section.title for section in report_without_risks.sections]
        self.assertNotIn("Risks & Opportunities", section_titles)

    def test_custom_metrics(self):
        """Test report generation with custom metrics."""
        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH,
            custom_metrics=["team_velocity", "custom_metric"]
        )

        # Mock data source should be called with custom metrics
        with patch.object(self.data_source, 'get_data') as mock_get_data:
            mock_get_data.return_value = self.mock_data

            report = self.generator.generate_report(context)

            # Verify custom metrics were requested
            mock_get_data.assert_called_once_with(
                "current_week",
                ["team_velocity", "custom_metric"]
            )

    def test_title_generation(self):
        """Test report title generation."""
        context = ReportContext(
            stakeholder_type=StakeholderType.VP_ENGINEERING,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        report = self.generator.generate_report(context)

        expected_title = "Executive Summary - Vp Engineering (current_week)"
        self.assertEqual(report.title, expected_title)

    def test_data_freshness_propagation(self):
        """Test that data freshness is propagated to sections."""
        context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH
        )

        report = self.generator.generate_report(context)

        # Most sections should have data freshness information
        sections_with_freshness = [s for s in report.sections if s.data_freshness]
        self.assertGreater(len(sections_with_freshness), 0)

    def test_metric_formatting(self):
        """Test metric formatting for different data types."""
        generator = self.generator

        # Test dict formatting with velocity data
        velocity_metric = generator._format_metric("team_velocity", {
            "current_sprint": 42,
            "trend": "increasing"
        })
        self.assertIn("42", velocity_metric)
        self.assertIn("increasing", velocity_metric)

        # Test dict formatting with dependency data
        dep_metric = generator._format_metric("cross_team_dependencies", {
            "total_dependencies": 12,
            "blocked_dependencies": 2
        })
        self.assertIn("12", dep_metric)
        self.assertIn("2", dep_metric)

        # Test simple value formatting
        simple_metric = generator._format_metric("simple_metric", "test_value")
        self.assertIn("Simple Metric", simple_metric)
        self.assertIn("test_value", simple_metric)

    def test_template_initialization(self):
        """Test that templates are properly initialized."""
        templates = self.generator.templates

        # Verify all stakeholder types have templates
        expected_stakeholders = [
            StakeholderType.CEO,
            StakeholderType.VP_ENGINEERING,
            StakeholderType.BOARD,
            StakeholderType.PRODUCT_TEAM,
            StakeholderType.ENGINEERING_MANAGER
        ]

        for stakeholder in expected_stakeholders:
            self.assertIn(stakeholder, templates)

            template = templates[stakeholder]
            self.assertIsInstance(template, SummaryTemplate)
            self.assertEqual(template.stakeholder_type, stakeholder)
            self.assertGreater(template.max_sections, 0)
            self.assertGreater(len(template.key_metrics), 0)
            self.assertGreater(len(template.focus_areas), 0)


if __name__ == '__main__':
    unittest.main()
