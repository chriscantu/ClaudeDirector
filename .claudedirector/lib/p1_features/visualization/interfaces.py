#!/usr/bin/env python3
"""
Interfaces for P1.1 Visualization System
Addresses SOLID principles - Interface Segregation and Dependency Inversion
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class OrganizationalData:
    """Data structure for organizational metrics"""

    impact_score: float
    domains: List[Dict[str, Any]]
    trends: Dict[str, List[float]]
    investments: List[Dict[str, Any]]
    sample_metrics: Dict[str, float]


class ProfileManagerInterface(ABC):
    """Interface for director profile management"""

    @abstractmethod
    def get_current_profile(self) -> Any:
        """Get the current director profile"""

    @abstractmethod
    def calculate_organizational_impact_score(self, metrics: Dict[str, float]) -> float:
        """Calculate organizational impact score from metrics"""


class ConfigManagerInterface(ABC):
    """Interface for configuration management"""

    @abstractmethod
    def get_sample_metric(self, metric_name: str) -> float:
        """Get sample metric value"""

    @abstractmethod
    def get_domain_performance(self, domain_type: str) -> Dict[str, float]:
        """Get domain performance configuration"""

    @abstractmethod
    def get_trend_data(self, trend_name: str) -> List[float]:
        """Get trend data"""

    @abstractmethod
    def get_investment_multiplier(self, investment_name: str) -> float:
        """Get investment multiplier"""


class DataGeneratorInterface(ABC):
    """Interface for data generation"""

    @abstractmethod
    def generate_sample_data(self, profile: Any) -> OrganizationalData:
        """Generate sample organizational data"""

    @abstractmethod
    def collect_real_data(self, profile: Any) -> OrganizationalData:
        """Collect real organizational data"""


class VisualizationComponentInterface(ABC):
    """Interface for visualization components"""

    @abstractmethod
    def render_ascii(self, *args, **kwargs) -> str:
        """Render ASCII visualization"""


class DashboardEngineInterface(ABC):
    """Interface for dashboard engine"""

    @abstractmethod
    def render_executive_dashboard(self, sample_data: bool = False) -> str:
        """Render executive dashboard"""

    @abstractmethod
    def get_quick_status(self) -> str:
        """Get quick status overview"""

    @abstractmethod
    def export_dashboard_data(self, format: str = "json") -> Dict[str, Any]:
        """Export dashboard data"""


class DesignSystemInterface(ABC):
    """Interface for design system operations"""

    @abstractmethod
    def get_status_indicator(self, value: float, target: float) -> Dict[str, str]:
        """Get status indicator for value vs target"""

    @abstractmethod
    def get_color_for_score(self, score: float, context: str = "performance") -> str:
        """Get color for score based on context"""

    @abstractmethod
    def format_metric_value(self, value: float, metric_type: str) -> str:
        """Format metric value for display"""
