"""
Test CLI Formatter

Comprehensive tests for P2.1 CLI Report Formatter.
Tests rich terminal output, color formatting, and layout rendering.
"""

import unittest
from unittest.mock import patch

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from lib.claudedirector.p2_communication.report_generation.cli_formatter import (
    CLIReportFormatter,
    CLIColors,
)
from lib.claudedirector.p2_communication.interfaces.report_interface import (
    GeneratedReport,
    ReportSection,
    ReportContext,
    StakeholderType,
    ReportFormat,
)


class TestCLIColors(unittest.TestCase):
    """Test cases for CLI Colors utility."""

    def test_color_constants(self):
        """Test that color constants are properly defined."""
        # Basic colors
        self.assertIsInstance(CLIColors.RED, str)
        self.assertIsInstance(CLIColors.GREEN, str)
        self.assertIsInstance(CLIColors.YELLOW, str)
        self.assertIsInstance(CLIColors.BLUE, str)

        # Styles
        self.assertIsInstance(CLIColors.BOLD, str)
        self.assertIsInstance(CLIColors.DIM, str)
        self.assertIsInstance(CLIColors.UNDERLINE, str)
        self.assertIsInstance(CLIColors.RESET, str)

        # Colors should contain ANSI escape codes
        self.assertTrue(CLIColors.RED.startswith("\033["))
        self.assertTrue(CLIColors.RESET.startswith("\033["))

    @patch("os.getenv")
    @patch("os.sys.stderr.isatty")
    def test_color_support_detection(self, mock_isatty, mock_getenv):
        """Test color support detection."""
        # Test with color support
        mock_getenv.return_value = "xterm-256color"
        mock_isatty.return_value = True
        self.assertTrue(CLIColors.is_supported())

        # Test without color support (dumb terminal)
        mock_getenv.return_value = "dumb"
        self.assertFalse(CLIColors.is_supported())

        # Test without TTY
        mock_getenv.return_value = "xterm-256color"
        mock_isatty.return_value = False
        self.assertFalse(CLIColors.is_supported())


class TestCLIReportFormatter(unittest.TestCase):
    """Test cases for CLI Report Formatter."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = CLIReportFormatter(
            use_colors=False
        )  # Disable colors for testing

        # Create sample report sections
        self.executive_summary = ReportSection(
            title="Executive Summary",
            content="• Team velocity is increasing (42 points this sprint)\n• 85% of strategic initiatives are on track (8/10)\n• No critical issues - operations running smoothly",
            priority=1,
            stakeholder_relevant=[StakeholderType.CEO],
            data_freshness="2025-08-10 09:00:00",
        )

        self.key_metrics = ReportSection(
            title="Key Metrics",
            content="Team Velocity: 42 (increasing)\nTeam Health: 85%\nDelivery Predictability: 90%",
            priority=2,
            stakeholder_relevant=[StakeholderType.VP_ENGINEERING],
            data_freshness="2025-08-10 09:00:00",
        )

        self.risks_section = ReportSection(
            title="Risks & Opportunities",
            content="✅ No significant risks identified - operations stable\n✅ Velocity trend suggests capacity for additional initiatives",
            priority=3,
            stakeholder_relevant=[StakeholderType.CEO, StakeholderType.VP_ENGINEERING],
            data_freshness="2025-08-10 09:00:00",
        )

        # Create sample report context
        self.context = ReportContext(
            stakeholder_type=StakeholderType.CEO,
            time_period="current_week",
            format=ReportFormat.CLI_RICH,
            include_predictions=True,
            include_risks=True,
        )

        # Create sample report
        self.sample_report = GeneratedReport(
            title="Executive Summary - CEO (current_week)",
            sections=[self.executive_summary, self.key_metrics, self.risks_section],
            generated_at="2025-08-10T09:00:00",
            context=self.context,
            data_sources=["jira", "claudedirector"],
            confidence_score=0.95,
        )

    def test_formatter_initialization(self):
        """Test formatter initialization."""
        # Test with colors enabled
        formatter_with_colors = CLIReportFormatter(use_colors=True)
        self.assertIsInstance(formatter_with_colors.use_colors, bool)
        self.assertIsInstance(formatter_with_colors.width, int)
        self.assertGreater(formatter_with_colors.width, 0)

        # Test with colors disabled
        formatter_no_colors = CLIReportFormatter(use_colors=False)
        self.assertFalse(formatter_no_colors.use_colors)

    def test_supported_formats(self):
        """Test supported output formats."""
        supported = self.formatter.get_supported_formats()

        self.assertIn(ReportFormat.CLI_RICH, supported)
        self.assertIn(ReportFormat.CLI_PLAIN, supported)
        self.assertIsInstance(supported, list)

    def test_terminal_width_detection(self):
        """Test terminal width detection."""
        width = self.formatter._get_terminal_width()
        self.assertIsInstance(width, int)
        self.assertGreaterEqual(width, 80)  # Should default to at least 80

    def test_format_report_structure(self):
        """Test basic report formatting structure."""
        formatted = self.formatter.format_report(self.sample_report)

        # Should contain main sections
        self.assertIn("Executive Summary - CEO", formatted)
        self.assertIn("EXECUTIVE SUMMARY", formatted)
        self.assertIn("KEY METRICS", formatted)
        self.assertIn("RISKS & OPPORTUNITIES", formatted)
        self.assertIn("DATA SOURCES", formatted)
        self.assertIn("NEXT ACTIONS", formatted)

        # Should contain metadata
        self.assertIn("Generated:", formatted)
        self.assertIn("Stakeholder: ceo", formatted)
        self.assertIn("Period: current_week", formatted)
        self.assertIn("Confidence: 95.0%", formatted)

    def test_format_header(self):
        """Test report header formatting."""
        header = self.formatter._format_header(self.sample_report)

        # Should contain title
        self.assertIn("Executive Summary - CEO", header)

        # Should contain metadata
        self.assertIn("Generated:", header)
        self.assertIn("Stakeholder:", header)
        self.assertIn("Period:", header)
        self.assertIn("Confidence:", header)

        # Should contain border characters
        self.assertIn("═", header)
        self.assertIn("║", header)

    def test_format_executive_summary(self):
        """Test executive summary formatting."""
        formatted = self.formatter._format_executive_summary(self.executive_summary)

        # Should contain section title
        self.assertIn("EXECUTIVE SUMMARY", formatted)

        # Should format bullet points with arrows
        self.assertIn("▶", formatted)

        # Should contain content
        self.assertIn("Team velocity is increasing", formatted)
        self.assertIn("strategic initiatives", formatted)

    def test_format_key_metrics(self):
        """Test key metrics formatting."""
        formatted = self.formatter._format_key_metrics([self.key_metrics])

        # Should contain section title
        self.assertIn("KEY METRICS", formatted)

        # Should format metrics with bullets
        self.assertIn("●", formatted)

        # Should contain metric content
        self.assertIn("Team Velocity", formatted)
        self.assertIn("Team Health", formatted)

    def test_format_section_with_priority(self):
        """Test section formatting with priority indicators."""
        # Test high priority section
        high_priority_section = ReportSection(
            title="Critical Issues",
            content="• Security vulnerability detected\n• Immediate action required",
            priority=1,  # High priority
            stakeholder_relevant=[StakeholderType.CEO],
        )

        formatted = self.formatter._format_section(high_priority_section)
        self.assertIn("🔴", formatted)  # Should have red indicator
        self.assertIn("CRITICAL ISSUES", formatted)

        # Test medium priority section
        medium_priority_section = ReportSection(
            title="Process Improvements",
            content="• Review current workflows\n• Consider automation opportunities",
            priority=3,  # Medium priority
            stakeholder_relevant=[StakeholderType.VP_ENGINEERING],
        )

        formatted = self.formatter._format_section(medium_priority_section)
        self.assertIn("🟡", formatted)  # Should have yellow indicator

        # Test low priority section
        low_priority_section = ReportSection(
            title="Future Planning",
            content="• Strategic roadmap review\n• Long-term capacity planning",
            priority=6,  # Low priority
            stakeholder_relevant=[StakeholderType.CEO],
        )

        formatted = self.formatter._format_section(low_priority_section)
        self.assertIn("🟢", formatted)  # Should have green indicator

    def test_format_footer(self):
        """Test footer formatting."""
        footer = self.formatter._format_footer(self.sample_report)

        # Should contain data sources
        self.assertIn("DATA SOURCES", footer)
        self.assertIn("jira", footer)
        self.assertIn("claudedirector", footer)

        # Should contain next actions
        self.assertIn("NEXT ACTIONS", footer)
        self.assertIn("./claudedirector", footer)

        # Should contain specific commands
        self.assertIn("dashboard --refresh", footer)
        self.assertIn("alerts", footer)
        self.assertIn("reports board", footer)

    def test_metric_value_formatting(self):
        """Test metric value formatting with colors."""
        formatter_with_colors = CLIReportFormatter(use_colors=True)

        # Test percentage formatting
        high_percentage = formatter_with_colors._format_metric_value("85%")
        good_percentage = formatter_with_colors._format_metric_value("75%")
        low_percentage = formatter_with_colors._format_metric_value("55%")

        # Colors are applied conditionally based on value ranges
        self.assertIsInstance(high_percentage, str)
        self.assertIsInstance(good_percentage, str)
        self.assertIsInstance(low_percentage, str)

        # Test trend formatting
        increasing_trend = formatter_with_colors._format_metric_value("increasing")
        decreasing_trend = formatter_with_colors._format_metric_value("decreasing")
        stable_trend = formatter_with_colors._format_metric_value("stable")

        self.assertIsInstance(increasing_trend, str)
        self.assertIsInstance(decreasing_trend, str)
        self.assertIsInstance(stable_trend, str)

    def test_colorize_functionality(self):
        """Test color application functionality."""
        # Test with colors enabled
        formatter_with_colors = CLIReportFormatter(use_colors=True)

        if CLIColors.is_supported():
            colored_text = formatter_with_colors._colorize("Test", CLIColors.RED)
            self.assertIn(CLIColors.RED, colored_text)
            self.assertIn(CLIColors.RESET, colored_text)
            self.assertIn("Test", colored_text)

        # Test with colors disabled
        uncolored_text = self.formatter._colorize("Test", CLIColors.RED)
        self.assertEqual(uncolored_text, "Test")

    def test_format_quick_status(self):
        """Test quick status formatting."""
        status_data = {
            "team_health": 85,
            "velocity_trend": "increasing",
            "critical_issues": 2,
            "last_updated": "2025-08-10 09:00:00",
        }

        formatted = self.formatter.format_quick_status(status_data)

        # Should contain quick status header
        self.assertIn("QUICK STATUS", formatted)

        # Should contain health indicators
        self.assertIn("Team Health: 85%", formatted)
        self.assertIn("Velocity: increasing", formatted)
        self.assertIn("Critical Issues: 2", formatted)
        self.assertIn("Last Updated:", formatted)

    def test_content_line_processing(self):
        """Test content line processing for different formats."""
        # Test bullet point processing
        content_with_bullets = "• First item\n• Second item\n- Third item"
        section = ReportSection(
            title="Test Section",
            content=content_with_bullets,
            priority=2,
            stakeholder_relevant=[StakeholderType.CEO],
        )

        formatted = self.formatter._format_section(section)

        # Should convert bullets to arrows
        self.assertIn("▶ First item", formatted)
        self.assertIn("▶ Second item", formatted)
        self.assertIn("▶ Third item", formatted)

        # Test key-value pair processing
        content_with_kvp = "Velocity: 42 points\nHealth Score: 85%\nTrend: increasing"
        section_kvp = ReportSection(
            title="Metrics",
            content=content_with_kvp,
            priority=2,
            stakeholder_relevant=[StakeholderType.CEO],
        )

        formatted_kvp = self.formatter._format_section(section_kvp)
        self.assertIn("Velocity:", formatted_kvp)
        self.assertIn("Health Score:", formatted_kvp)
        self.assertIn("Trend:", formatted_kvp)

    def test_data_freshness_display(self):
        """Test data freshness information display."""
        section_with_freshness = ReportSection(
            title="Test Section",
            content="Test content",
            priority=2,
            stakeholder_relevant=[StakeholderType.CEO],
            data_freshness="2025-08-10 09:00:00",
        )

        formatted = self.formatter._format_section(section_with_freshness)

        # Should include data freshness information
        self.assertIn("Data as of:", formatted)
        self.assertIn("2025-08-10 09:00:00", formatted)
        self.assertIn("ℹ", formatted)  # Info icon

        # Test section without freshness
        section_no_freshness = ReportSection(
            title="Test Section",
            content="Test content",
            priority=2,
            stakeholder_relevant=[StakeholderType.CEO],
        )

        formatted_no_freshness = self.formatter._format_section(section_no_freshness)
        self.assertNotIn("Data as of:", formatted_no_freshness)

    def test_long_content_handling(self):
        """Test handling of long content that might exceed terminal width."""
        long_content = "This is a very long line of content that might exceed the typical terminal width and should be handled gracefully by the formatter without breaking the layout or causing display issues."

        long_section = ReportSection(
            title="Long Content Test",
            content=long_content,
            priority=2,
            stakeholder_relevant=[StakeholderType.CEO],
        )

        formatted = self.formatter._format_section(long_section)

        # Should handle long content gracefully
        self.assertIn(long_content, formatted)
        self.assertIn("LONG CONTENT TEST", formatted)

    def test_empty_sections_handling(self):
        """Test handling of empty or minimal sections."""
        empty_section = ReportSection(
            title="Empty Section",
            content="",
            priority=2,
            stakeholder_relevant=[StakeholderType.CEO],
        )

        formatted = self.formatter._format_section(empty_section)

        # Should handle empty content gracefully
        self.assertIn("EMPTY SECTION", formatted)
        # Should not crash or produce malformed output
        self.assertIsInstance(formatted, str)

    def test_special_characters_handling(self):
        """Test handling of special characters and Unicode."""
        special_content = (
            "• Unicode bullets ✅ ⚠️ 🔴\n• Arrows → ← ↑ ↓\n• Progress: 85% ±2%"
        )

        special_section = ReportSection(
            title="Special Characters",
            content=special_content,
            priority=2,
            stakeholder_relevant=[StakeholderType.CEO],
        )

        formatted = self.formatter._format_section(special_section)

        # Should preserve special characters
        self.assertIn("✅", formatted)
        self.assertIn("⚠️", formatted)
        self.assertIn("🔴", formatted)
        self.assertIn("85%", formatted)


if __name__ == "__main__":
    unittest.main()
