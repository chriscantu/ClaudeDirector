"""
ClaudeDirector - Your AI Strategic Leadership Team

The first completely transparent AI strategic leadership system for engineering leaders.
Automatically customizes to your specific role and challenges.
"""

__version__ = "1.2.1"
__author__ = "ClaudeDirector Development Team"
__email__ = "support@claudedirector.ai"

# Core imports for easy access
from .core.first_run_wizard import (
    FirstRunWizard,
    UserRole,
    OrganizationType,
    ChallengeFocus,
)
from .core.cursor_wizard_integration import CursorWizardIntegration

# Version info
VERSION_INFO = {
    "version": __version__,
    "features": [
        "Role-based customization (6 supported roles)",
        "Automatic persona activation",
        "Strategic framework detection (25+ frameworks)",
        "Complete AI transparency",
        "Cursor IDE integration",
        "Persistent configuration",
    ],
    "supported_roles": [
        "VP/SVP Engineering",
        "CTO",
        "Engineering Director",
        "Engineering Manager",
        "Staff/Principal Engineer",
        "Product Engineering Lead",
    ],
}


def get_version():
    """Get ClaudeDirector version information"""
    return VERSION_INFO


# Make key classes available at package level
__all__ = [
    "FirstRunWizard",
    "CursorWizardIntegration",
    "UserRole",
    "OrganizationType",
    "ChallengeFocus",
    "get_version",
    "VERSION_INFO",
]
