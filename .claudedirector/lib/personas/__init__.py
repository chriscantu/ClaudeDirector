"""
Advanced Persona Intelligence Module - Phase 14 Track 3

🎨 Rachel | Design Systems Strategy

Enterprise-grade persona intelligence with advanced strategic thinking depth,
context-aware behavior adaptation, and multi-persona coordination.

Architecture Integration:
- Extends existing persona management with advanced personality modeling
- Integrates with context_engineering for persona-specific memory
- Builds on MCP enhancement for persona-specific strategic intelligence
- Maintains existing transparency and framework attribution systems
"""

from .advanced_personality_engine import (
    AdvancedPersonalityEngine,
    PersonaBehavior,
    PersonaConsistencyMetrics,
    StrategicThinkingDepth,
    create_advanced_personality_engine,
)

# Multi-persona coordination (optional - may not be implemented yet)
try:
    from .multi_persona_coordinator import (
        MultiPersonaCoordinator,
        PersonaCoordination,
        CoordinationStrategy,
        ConflictResolution,
    )

    _multi_persona_available = True
except ImportError:
    # Graceful fallback if multi-persona coordinator not implemented
    MultiPersonaCoordinator = None
    PersonaCoordination = None
    CoordinationStrategy = None
    ConflictResolution = None
    _multi_persona_available = False

# Strategic Challenge Framework
from .strategic_challenge_framework import (
    StrategicChallengeFramework,
    ChallengeType,
    strategic_challenge_framework,
)

__all__ = [
    "AdvancedPersonalityEngine",
    "PersonaBehavior",
    "PersonaConsistencyMetrics",
    "StrategicThinkingDepth",
    "create_advanced_personality_engine",
    "StrategicChallengeFramework",
    "ChallengeType",
    "strategic_challenge_framework",
]

# Add multi-persona exports if available
if _multi_persona_available:
    __all__.extend(
        [
            "MultiPersonaCoordinator",
            "PersonaCoordination",
            "CoordinationStrategy",
            "ConflictResolution",
        ]
    )
