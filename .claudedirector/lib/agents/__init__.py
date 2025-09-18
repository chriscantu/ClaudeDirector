"""Agent Framework Module

Agent-based automation system for strategic platform operations.
Implements autonomous agents following Director-level architectural patterns.
"""

from .weekly_report_agent import WeeklyReportAgent, WeeklyReportConfig

__all__ = [
    "WeeklyReportAgent",
    "WeeklyReportConfig",
]
