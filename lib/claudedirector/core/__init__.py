"""
ClaudeDirector Core Module

Core functionality for strategic leadership AI system including:
- First-run wizard for role-based customization
- Cursor IDE integration
- Persona enhancement engine
- Transparency engine integration
- Framework detection
"""

from .first_run_wizard import (
    FirstRunWizard,
    UserRole,
    OrganizationType,
    ChallengeFocus,
    UserConfiguration,
    RolePersonaMapper,
)

from .cursor_wizard_integration import (
    CursorWizardIntegration,
    initialize_cursor_integration,
    process_cursor_input,
)

__all__ = [
    "FirstRunWizard",
    "CursorWizardIntegration",
    "UserRole",
    "OrganizationType",
    "ChallengeFocus",
    "UserConfiguration",
    "RolePersonaMapper",
    "initialize_cursor_integration",
    "process_cursor_input",
]
