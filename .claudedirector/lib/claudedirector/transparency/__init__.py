"""
ClaudeDirector Transparency System
Advanced transparency and attribution system for persona responses with MCP integration
"""

from .integrated_transparency import (
    IntegratedTransparencySystem,
    TransparencyContext,
    TransparencyConfig,
    create_transparency_system,
    PersonaTransparencyDecorator,
    transparent_persona_response,
)

from .persona_integration import (
    TransparentPersonaManager,
    PersonaIntegrationFactory,
    MCPIntegrationHelper,
    PersonaResponse,
)

from .mcp_transparency import MCPTransparencyMiddleware, MCPContext, MCPCall

from .framework_detection import (
    FrameworkDetectionMiddleware,
    FrameworkUsage,
    FrameworkPatterns,
)

# Version information
__version__ = "1.0.0"
__author__ = "ClaudeDirector Team"
__description__ = "Transparency system for ClaudeDirector persona responses"

# Main exports for easy importing
__all__ = [
    # Core transparency system
    "IntegratedTransparencySystem",
    "TransparencyContext",
    "TransparencyConfig",
    "create_transparency_system",
    # Persona integration
    "TransparentPersonaManager",
    "PersonaIntegrationFactory",
    "MCPIntegrationHelper",
    "PersonaResponse",
    # MCP transparency components
    "MCPTransparencyMiddleware",
    "MCPContext",
    "MCPCall",
    # Framework detection
    "FrameworkDetectionMiddleware",
    "FrameworkUsage",
    "FrameworkPatterns",
    # Decorators and utilities
    "PersonaTransparencyDecorator",
    "transparent_persona_response",
]

# Configuration defaults
DEFAULT_TRANSPARENCY_CONFIG = TransparencyConfig.create_default()
MINIMAL_TRANSPARENCY_CONFIG = TransparencyConfig.create_minimal()
DEBUG_TRANSPARENCY_CONFIG = TransparencyConfig.create_debug()


# Quick setup functions
def quick_setup_default():
    """Quick setup with default configuration"""
    return PersonaIntegrationFactory.create_transparent_manager("default")


def quick_setup_minimal():
    """Quick setup with minimal configuration"""
    return PersonaIntegrationFactory.create_transparent_manager("minimal")


def quick_setup_debug():
    """Quick setup with debug configuration"""
    return PersonaIntegrationFactory.create_transparent_manager("debug")


def wrap_existing_persona_manager(existing_manager, config="default"):
    """Convenience function to wrap existing persona manager"""
    return PersonaIntegrationFactory.wrap_existing_manager(existing_manager, config)


# Module metadata
def get_version_info():
    """Get detailed version information"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "components": {
            "integrated_transparency": "Core transparency orchestration",
            "persona_integration": "Persona manager integration layer",
            "mcp_transparency": "MCP server call transparency",
            "framework_detection": "Strategic framework attribution",
        },
        "features": [
            "MCP server call transparency",
            "Strategic framework attribution",
            "Performance monitoring",
            "Persona-specific communication patterns",
            "Configurable transparency levels",
            "Comprehensive testing suite",
        ],
    }


def print_version_info():
    """Print version information"""
    info = get_version_info()
    print(f"ClaudeDirector Transparency System v{info['version']}")
    print(f"Author: {info['author']}")
    print(f"Description: {info['description']}")
    print("\nComponents:")
    for component, description in info["components"].items():
        print(f"  - {component}: {description}")
    print("\nFeatures:")
    for feature in info["features"]:
        print(f"  - {feature}")
