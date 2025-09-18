"""
Agents Module - Autonomous strategic platform operations

This module provides autonomous agents for strategic platform tasks including:
- Weekly report generation
- Strategic analysis automation
- Cross-functional coordination

All agents follow ClaudeDirector BaseManager patterns for consistency.
"""

from .weekly_report_agent import WeeklyReportAgent, WeeklyReportConfig

__all__ = ["WeeklyReportAgent", "WeeklyReportConfig"]
