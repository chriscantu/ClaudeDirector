"""
P2.1 Executive Communication Module

Enhanced CLI reporting and communication features for ClaudeDirector.
Provides AI-powered executive summaries, stakeholder-specific reports,
and intelligent alert systems.
"""

from .report_generation.executive_summary import ExecutiveSummaryGenerator
from .report_generation.cli_formatter import CLIReportFormatter
from .integrations.jira_client import JIRAIntegrationClient

__version__ = "2.1.0"
__author__ = "ClaudeDirector Team"

__all__ = ["ExecutiveSummaryGenerator", "CLIReportFormatter", "JIRAIntegrationClient"]
