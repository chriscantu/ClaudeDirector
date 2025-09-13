"""
🎯 Phase 2: Proactive Code Generation Compliance System - Generation Module

🏗️ Martin | Platform Architecture with Sequential Thinking + Context7 MCP Integration

ARCHITECTURAL COMPLIANCE:
✅ PROJECT_STRUCTURE.md: Placed in .claudedirector/lib/core/generation/ (line 71-75)
✅ DRY: Extends existing BasicSOLIDTemplateEngine (no duplication)
✅ SOLID: Single responsibility modules for generation and placement
✅ BLOAT_PREVENTION_SYSTEM.md: Reuses existing UnifiedFactory patterns

PHASE 2 COMPONENTS:
- SOLIDTemplateEngine: Principle-enforced code generation templates
- StructureAwarePlacementEngine: Automatic PROJECT_STRUCTURE.md compliance

Author: Strategic Team (Diego, Martin, Camille) with Sequential Thinking methodology
"""

from .basic_solid_template_engine import BasicSOLIDTemplateEngine
from .solid_template_engine import (
    SOLIDTemplateEngine,
    SOLIDPrinciple,
    TemplateContext,
    GenerationResult,
)
from .structure_aware_placement_engine import (
    StructureAwarePlacementEngine,
    PlacementResult,
)
from .placement_config_loader import (
    PlacementConfigLoader,
    ComponentCategory,
    PlacementRule,
    create_placement_config_loader,
)

__all__ = [
    "BasicSOLIDTemplateEngine",
    "SOLIDTemplateEngine",
    "SOLIDPrinciple",
    "TemplateContext",
    "GenerationResult",
    "StructureAwarePlacementEngine",
    "PlacementResult",
    "PlacementConfigLoader",
    "ComponentCategory",
    "PlacementRule",
    "create_placement_config_loader",
]
