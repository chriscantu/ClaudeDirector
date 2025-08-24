"""
Core ClaudeDirector functionality
Database management, configuration, and shared utilities
"""

from .config import ClaudeDirectorConfig
from .database import DatabaseManager
from .exceptions import (
    AIDetectionError,
    ClaudeDirectorError,
    ConfigurationError,
    DatabaseError,
)
from .hybrid_installation_manager import (
    HybridInstallationManager,
    InstallationResult,
    InstallationCommand,
    UsageStats,
    get_hybrid_manager,
    install_mcp_package,
)
from .enhanced_persona_manager import (
    EnhancedPersonaManager,
    EnhancedResponse,
    TransparencyManager,
    EnhancementStatus,
)
from .complexity_analyzer import (
    AnalysisComplexityDetector,
    ComplexityAnalysis,
    AnalysisComplexity,
    EnhancementStrategy,
)

__all__ = [
    "ClaudeDirectorConfig",
    "DatabaseManager",
    "ClaudeDirectorError",
    "DatabaseError",
    "AIDetectionError",
    "ConfigurationError",
    "HybridInstallationManager",
    "InstallationResult",
    "InstallationCommand",
    "UsageStats",
    "get_hybrid_manager",
    "install_mcp_package",
    "EnhancedPersonaManager",
    "EnhancedResponse",
    "TransparencyManager",
    "EnhancementStatus",
    "AnalysisComplexityDetector",
    "ComplexityAnalysis",
    "AnalysisComplexity",
    "EnhancementStrategy",
]
