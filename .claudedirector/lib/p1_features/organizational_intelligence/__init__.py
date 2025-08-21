"""
P1 Organizational Leverage Intelligence
Configuration-driven system for directors to optimize organizational impact
"""

from .director_profile_manager import (
    DirectorProfileManager,
    DirectorProfile,
    MetricDefinition,
    InvestmentCategory,
)
from .cli_customization import org_intelligence

__all__ = [
    "DirectorProfileManager",
    "DirectorProfile",
    "MetricDefinition",
    "InvestmentCategory",
    "org_intelligence",
]

# Version and feature info
__version__ = "1.0.0"
__description__ = (
    "Flexible organizational leverage intelligence for engineering directors"
)
