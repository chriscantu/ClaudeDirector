"""
Report Generation Interface

Abstract interface for all report generation components following
SOLID principles and dependency inversion.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class StakeholderType(Enum):
    """Stakeholder types for targeted reporting."""

    CEO = "ceo"
    VP_ENGINEERING = "vp_engineering"
    BOARD = "board"
    PRODUCT_TEAM = "product_team"
    ENGINEERING_MANAGER = "engineering_manager"


class ReportFormat(Enum):
    """Output format options for reports."""

    CLI_RICH = "cli_rich"
    CLI_PLAIN = "cli_plain"
    MARKDOWN = "markdown"
    JSON = "json"


@dataclass
class ReportContext:
    """Context information for report generation."""

    stakeholder_type: StakeholderType
    time_period: str
    include_predictions: bool = True
    include_risks: bool = True
    format: ReportFormat = ReportFormat.CLI_RICH
    custom_metrics: Optional[List[str]] = None


@dataclass
class ReportSection:
    """Individual section of a report."""

    title: str
    content: str
    priority: int
    stakeholder_relevant: List[StakeholderType]
    data_freshness: Optional[str] = None


@dataclass
class GeneratedReport:
    """Complete generated report with metadata."""

    title: str
    sections: List[ReportSection]
    generated_at: str
    context: ReportContext
    data_sources: List[str]
    confidence_score: Optional[float] = None


class IReportGenerator(ABC):
    """Abstract interface for report generation components."""

    @abstractmethod
    def generate_report(self, context: ReportContext) -> GeneratedReport:
        """Generate a report based on the provided context."""

    @abstractmethod
    def get_supported_stakeholders(self) -> List[StakeholderType]:
        """Return list of supported stakeholder types."""

    @abstractmethod
    def validate_context(self, context: ReportContext) -> bool:
        """Validate that the context is supported by this generator."""


class IReportFormatter(ABC):
    """Abstract interface for report formatting components."""

    @abstractmethod
    def format_report(self, report: GeneratedReport) -> str:
        """Format a generated report for output."""

    @abstractmethod
    def get_supported_formats(self) -> List[ReportFormat]:
        """Return list of supported output formats."""


class IDataSource(ABC):
    """Abstract interface for data source components."""

    @abstractmethod
    def get_data(self, time_period: str, metrics: List[str]) -> Dict[str, Any]:
        """Retrieve data for the specified time period and metrics."""

    @abstractmethod
    def get_data_freshness(self) -> str:
        """Return timestamp of when data was last updated."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the data source is currently available."""


class IAlertSystem(ABC):
    """Abstract interface for alert system components."""

    @abstractmethod
    def should_alert(self, data: Dict[str, Any]) -> bool:
        """Determine if an alert should be triggered based on data."""

    @abstractmethod
    def generate_alert(self, data: Dict[str, Any]) -> str:
        """Generate alert message based on data."""

    @abstractmethod
    def get_alert_channels(self) -> List[str]:
        """Return list of available alert channels."""
