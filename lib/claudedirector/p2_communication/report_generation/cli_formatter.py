"""
CLI Report Formatter

Rich terminal output formatting for ClaudeDirector executive reports.
Provides executive-friendly, scannable CLI output with colors and formatting.
"""

import os
from typing import Dict, List, Optional
from datetime import datetime

from ..interfaces.report_interface import (
    IReportFormatter,
    ReportFormat,
    GeneratedReport,
    ReportSection,
)


class CLIColors:
    """ANSI color codes for terminal output."""

    # Basic colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Reset
    RESET = "\033[0m"

    @classmethod
    def is_supported(cls) -> bool:
        """Check if terminal supports colors."""
        return (
            os.getenv("TERM") != "dumb"
            and hasattr(os.sys.stderr, "isatty")
            and os.sys.stderr.isatty()
        )


class CLIReportFormatter(IReportFormatter):
    """
    CLI report formatter for executive-friendly terminal output.

    Features:
    - Rich text output with colors and formatting
    - Executive-friendly scannable layouts
    - ASCII charts and progress indicators
    - Clear section hierarchy and prioritization
    """

    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors and CLIColors.is_supported()
        self.width = self._get_terminal_width()

    def format_report(self, report: GeneratedReport) -> str:
        """Format a generated report for CLI output."""
        output = []

        # Header
        output.append(self._format_header(report))
        output.append("")

        # Executive Summary (if available)
        summary_sections = [s for s in report.sections if "summary" in s.title.lower()]
        if summary_sections:
            output.append(self._format_executive_summary(summary_sections[0]))
            output.append("")

        # Key Metrics
        metrics_sections = [s for s in report.sections if "metric" in s.title.lower()]
        if metrics_sections:
            output.append(self._format_key_metrics(metrics_sections))
            output.append("")

        # Detailed Sections (sorted by priority)
        detailed_sections = [
            s
            for s in report.sections
            if "summary" not in s.title.lower() and "metric" not in s.title.lower()
        ]
        detailed_sections.sort(key=lambda x: x.priority)

        for section in detailed_sections:
            output.append(self._format_section(section))
            output.append("")

        # Footer
        output.append(self._format_footer(report))

        return "\n".join(output)

    def get_supported_formats(self) -> List[ReportFormat]:
        """Return list of supported output formats."""
        return [ReportFormat.CLI_RICH, ReportFormat.CLI_PLAIN]

    def _get_terminal_width(self) -> int:
        """Get terminal width, default to 80 if unavailable."""
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80

    def _format_header(self, report: GeneratedReport) -> str:
        """Format report header with title and metadata."""
        lines = []

        # Title with border
        title_line = f" {report.title} "
        border_char = "═"
        border_length = min(len(title_line) + 4, self.width)

        lines.append(
            self._colorize(border_char * border_length, CLIColors.BLUE + CLIColors.BOLD)
        )
        lines.append(
            self._colorize(
                f"║{title_line.center(border_length-2)}║",
                CLIColors.BLUE + CLIColors.BOLD,
            )
        )
        lines.append(
            self._colorize(border_char * border_length, CLIColors.BLUE + CLIColors.BOLD)
        )

        # Metadata
        generated_time = datetime.fromisoformat(
            report.generated_at.replace("Z", "+00:00")
        )
        metadata = (
            f"Generated: {generated_time.strftime('%Y-%m-%d %H:%M')} | "
            f"Stakeholder: {report.context.stakeholder_type.value} | "
            f"Period: {report.context.time_period}"
        )

        if report.confidence_score:
            metadata += f" | Confidence: {report.confidence_score:.1%}"

        lines.append(self._colorize(metadata, CLIColors.DIM))

        return "\n".join(lines)

    def _format_executive_summary(self, section: ReportSection) -> str:
        """Format executive summary with emphasis."""
        lines = []

        # Section title
        lines.append(
            self._colorize("📋 EXECUTIVE SUMMARY", CLIColors.BOLD + CLIColors.CYAN)
        )
        lines.append(self._colorize("─" * 50, CLIColors.CYAN))

        # Content with proper formatting
        content_lines = section.content.split("\n")
        for line in content_lines:
            if line.strip():
                if line.startswith("•") or line.startswith("-"):
                    lines.append(
                        f"  {self._colorize('▶', CLIColors.GREEN)} {line[1:].strip()}"
                    )
                else:
                    lines.append(f"  {line}")
            else:
                lines.append("")

        return "\n".join(lines)

    def _format_key_metrics(self, metrics_sections: List[ReportSection]) -> str:
        """Format key metrics in a dashboard-style layout."""
        lines = []

        lines.append(
            self._colorize("📊 KEY METRICS", CLIColors.BOLD + CLIColors.YELLOW)
        )
        lines.append(self._colorize("─" * 50, CLIColors.YELLOW))

        # Simple metrics layout
        for section in metrics_sections:
            lines.append(f"  {self._colorize('●', CLIColors.GREEN)} {section.title}")

            # Extract key-value pairs from content
            content_lines = section.content.split("\n")
            for line in content_lines:
                if ":" in line and line.strip():
                    key, value = line.split(":", 1)
                    formatted_line = (
                        f"    {key.strip()}: {self._format_metric_value(value.strip())}"
                    )
                    lines.append(formatted_line)

        return "\n".join(lines)

    def _format_section(self, section: ReportSection) -> str:
        """Format a detailed report section."""
        lines = []

        # Section title with priority indicator
        priority_indicator = (
            "🔴" if section.priority <= 2 else "🟡" if section.priority <= 4 else "🟢"
        )
        title = f"{priority_indicator} {section.title.upper()}"
        lines.append(self._colorize(title, CLIColors.BOLD))
        lines.append(
            self._colorize("─" * min(len(title) - 2, 50), CLIColors.DIM)
        )  # -2 for emoji

        # Content formatting
        content_lines = section.content.split("\n")
        for line in content_lines:
            if line.strip():
                if line.startswith("•") or line.startswith("-"):
                    lines.append(
                        f"  {self._colorize('▶', CLIColors.BLUE)} {line[1:].strip()}"
                    )
                elif ":" in line:
                    key, value = line.split(":", 1)
                    lines.append(
                        f"  {key.strip()}: {self._format_metric_value(value.strip())}"
                    )
                else:
                    lines.append(f"  {line}")
            else:
                lines.append("")

        # Data freshness if available
        if section.data_freshness:
            freshness_line = f"  {self._colorize('ℹ', CLIColors.DIM)} Data as of: {section.data_freshness}"
            lines.append(freshness_line)

        return "\n".join(lines)

    def _format_footer(self, report: GeneratedReport) -> str:
        """Format report footer with data sources and next actions."""
        lines = []

        # Data sources
        if report.data_sources:
            lines.append(self._colorize("📍 DATA SOURCES", CLIColors.DIM))
            sources_text = " • ".join(report.data_sources)
            lines.append(self._colorize(f"  {sources_text}", CLIColors.DIM))

        # CLI command hints
        lines.append("")
        lines.append(self._colorize("💡 NEXT ACTIONS", CLIColors.DIM))
        lines.append(
            self._colorize(
                "  ./claudedirector dashboard --refresh    # Update data", CLIColors.DIM
            )
        )
        lines.append(
            self._colorize(
                "  ./claudedirector alerts                 # Check critical issues",
                CLIColors.DIM,
            )
        )
        lines.append(
            self._colorize(
                "  ./claudedirector reports board          # Generate board report",
                CLIColors.DIM,
            )
        )

        return "\n".join(lines)

    def _format_metric_value(self, value: str) -> str:
        """Format metric values with appropriate colors."""
        value = value.strip()

        # Handle percentages
        if "%" in value:
            try:
                num = float(value.replace("%", ""))
                if num >= 80:
                    return self._colorize(value, CLIColors.GREEN)
                elif num >= 60:
                    return self._colorize(value, CLIColors.YELLOW)
                else:
                    return self._colorize(value, CLIColors.RED)
            except ValueError:
                pass

        # Handle trend indicators
        if any(
            word in value.lower() for word in ["increasing", "improving", "up", "good"]
        ):
            return self._colorize(value, CLIColors.GREEN)
        elif any(
            word in value.lower()
            for word in ["decreasing", "declining", "down", "poor"]
        ):
            return self._colorize(value, CLIColors.RED)
        elif any(word in value.lower() for word in ["stable", "steady", "normal"]):
            return self._colorize(value, CLIColors.YELLOW)

        # Default formatting
        return value

    def _colorize(self, text: str, color_code: str) -> str:
        """Apply color to text if colors are enabled."""
        if self.use_colors:
            return f"{color_code}{text}{CLIColors.RESET}"
        else:
            return text

    def format_quick_status(self, data: Dict[str, any]) -> str:
        """Format quick status output for ./claudedirector status command."""
        lines = []

        # Quick header
        lines.append(self._colorize("⚡ QUICK STATUS", CLIColors.BOLD + CLIColors.CYAN))
        lines.append(self._colorize("─" * 30, CLIColors.CYAN))

        # Health indicators
        if "team_health" in data:
            health = data["team_health"]
            health_color = (
                CLIColors.GREEN
                if health >= 80
                else CLIColors.YELLOW if health >= 60 else CLIColors.RED
            )
            lines.append(f"  Team Health: {self._colorize(f'{health}%', health_color)}")

        if "velocity_trend" in data:
            trend = data["velocity_trend"]
            lines.append(f"  Velocity: {self._format_metric_value(trend)}")

        if "critical_issues" in data:
            issues = data["critical_issues"]
            issue_color = CLIColors.RED if issues > 0 else CLIColors.GREEN
            lines.append(
                f"  Critical Issues: {self._colorize(str(issues), issue_color)}"
            )

        # Data freshness
        if "last_updated" in data:
            lines.append(
                f"  {self._colorize('Last Updated:', CLIColors.DIM)} {data['last_updated']}"
            )

        return "\n".join(lines)
