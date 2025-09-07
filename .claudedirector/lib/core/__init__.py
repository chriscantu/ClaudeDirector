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

# TS-4: Temporarily disable enhanced_persona_manager import to fix P0 test failures
# from .enhanced_persona_manager import (
#     EnhancedPersonaManager,
#     EnhancedResponse,
#     TransparencyManager,
#     EnhancementStatus,
# )
# TS-4: Temporarily disable persona_chat_integration import to fix P0 test failures
# This breaks circular dependency: persona_chat_integration -> unified_response_handler -> performance
# from .persona_chat_integration import (
#     UnifiedPersonaChatIntegration,
#     PersonaChatInterface,
#     PersonaP2Bridge,
#     ConversationFormatter,
#     P2ChatAdapter,
#     PersonaType,
#     ChatRequest,
#     ChatResponse,
#     PersonaResponse,
#     ConversationStyle,
#     RequestType,
#     get_persona_chat_integration,
# )
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
    "UnifiedPersonaChatIntegration",
    "PersonaChatInterface",
    "PersonaP2Bridge",
    "ConversationFormatter",
    "P2ChatAdapter",
    "PersonaType",
    "ChatRequest",
    "ChatResponse",
    "PersonaResponse",
    "ConversationStyle",
    "RequestType",
    "get_persona_chat_integration",
    "AnalysisComplexityDetector",
    "ComplexityAnalysis",
    "AnalysisComplexity",
    "EnhancementStrategy",
]
