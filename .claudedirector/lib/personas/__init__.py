"""
🎯 STORY 9.6.1: UNIFIED PERSONA INTELLIGENCE MODULE

CONSOLIDATION ACHIEVEMENT:
- Replaced multiple persona files with single unified_persona_engine.py
- Eliminated duplicate functionality and imports
- Reduced complexity while maintaining all features

BLOAT ELIMINATION:
- Single source of truth for persona functionality
- DRY-compliant implementation
- Backward compatibility maintained
- PROJECT_STRUCTURE.md compliant organization

Author: Martin | Platform Architecture
Sequential Thinking Phase 9.6.1 - Persona system consolidation
"""

# CONSOLIDATION: Import from unified persona engine
from .unified_persona_engine import (
    UnifiedPersonaEngine,
    PersonaType,
    ChallengeType,
    StrategicThinkingDepth,
    PersonaBehavior,
    ChallengePattern,
    PersonaConsistencyMetrics,
    create_unified_persona_engine,
    get_default_persona_engine,
    get_persona_engine,
)

# CONSOLIDATION: Backward compatibility aliases
AdvancedPersonalityEngine = UnifiedPersonaEngine
create_advanced_personality_engine = create_unified_persona_engine
StrategicChallengeFramework = UnifiedPersonaEngine
strategic_challenge_framework = get_persona_engine

# CONSOLIDATION: Simplified exports - single source of truth
__all__ = [
    "UnifiedPersonaEngine",
    "PersonaType",
    "ChallengeType",
    "StrategicThinkingDepth",
    "PersonaBehavior",
    "ChallengePattern",
    "PersonaConsistencyMetrics",
    "create_unified_persona_engine",
    "get_default_persona_engine",
    "get_persona_engine",
    # Backward compatibility
    "AdvancedPersonalityEngine",
    "create_advanced_personality_engine",
    "StrategicChallengeFramework",
    "strategic_challenge_framework",
]
