"""
Centralized Constants for ClaudeDirector
SOLID Compliance: Eliminates hard-coded strings throughout the system
"""

from .constants import (
    FrameworkConstants,
    PersonaConstants,
    SystemConstants,
    MLConstants,
    TransparencyConstants,
    ConfigurationManager,
    CONFIG,
    FRAMEWORKS,
    PERSONAS,
    SYSTEM,
    ML_CONFIG,
    TRANSPARENCY,
)

from .framework_definitions import (
    FrameworkDefinition,
    FrameworkPatternRegistry,
    FRAMEWORK_REGISTRY,
)

__all__ = [
    "FrameworkConstants",
    "PersonaConstants",
    "SystemConstants",
    "MLConstants",
    "TransparencyConstants",
    "ConfigurationManager",
    "CONFIG",
    "FRAMEWORKS",
    "PERSONAS",
    "SYSTEM",
    "ML_CONFIG",
    "TRANSPARENCY",
    "FrameworkDefinition",
    "FrameworkPatternRegistry",
    "FRAMEWORK_REGISTRY",
]
