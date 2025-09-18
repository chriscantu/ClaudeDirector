"""
Agents Module - Autonomous strategic platform operations

This module provides autonomous agents for strategic platform tasks including:
- Weekly report generation leveraging existing weekly_reporter.py infrastructure
- Strategic analysis automation
- Cross-functional coordination

All agents follow ClaudeDirector BaseManager patterns for consistency and
leverage existing proven business logic for reliability.
"""

from .weekly_report_agent import (
    WeeklyReportAgent,
    WeeklyReportConfig,
    create_weekly_report_agent,
)

__all__ = ["WeeklyReportAgent", "WeeklyReportConfig", "create_weekly_report_agent"]
