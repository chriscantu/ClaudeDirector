"""
P1.1 Visual Dashboard Framework
Rachel's design-system approach to organizational intelligence visualization
"""

from .dashboard_engine import DashboardEngine
from .visual_components import (
    ImpactScoreIndicator,
    DomainPerformanceChart,
    TrendSparkline,
    ExecutiveSummaryWidget,
    ROIVisualization,
)
from .design_system import VisualizationDesignSystem

__all__ = [
    "DashboardEngine",
    "ImpactScoreIndicator",
    "DomainPerformanceChart",
    "TrendSparkline",
    "ExecutiveSummaryWidget",
    "ROIVisualization",
    "VisualizationDesignSystem",
]

# Version and feature info
__version__ = "1.1.0"
__description__ = (
    "Rachel-approved visual intelligence dashboard for engineering directors"
)
