"""
P2.1 Interfaces Module

Abstract interfaces for P2.1 Executive Communication components.
Follows SOLID principles with dependency inversion.
"""

from .report_interface import (
    IReportGenerator,
    IReportFormatter,
    IDataSource,
    IAlertSystem,
    ReportContext,
    ReportSection,
    GeneratedReport,
    StakeholderType,
    ReportFormat,
)

__all__ = [
    "IReportGenerator",
    "IReportFormatter",
    "IDataSource",
    "IAlertSystem",
    "ReportContext",
    "ReportSection",
    "GeneratedReport",
    "StakeholderType",
    "ReportFormat",
]
