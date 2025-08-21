"""
P2.1 Report Generation Module

Core report generation and formatting components for P2.1 Executive Communication.
"""

from .executive_summary import ExecutiveSummaryGenerator
from .cli_formatter import CLIReportFormatter, CLIColors

__all__ = ["ExecutiveSummaryGenerator", "CLIReportFormatter", "CLIColors"]
