#!/usr/bin/env python3
"""
Stakeholder Intelligence Components
Phase 3A.3.5: Aggressive Code Reduction

🏗️ Martin | Platform Architecture - DRY over SOLID ceremony
🤝 Diego | Engineering Leadership - Stakeholder relationship intelligence
🤖 Berny | AI/ML Engineering - Code bloat elimination

Consolidated stakeholder intelligence components for aggressive code reduction.
Phase 3A.3.5 eliminates over-engineering by merging related functionality.
"""

# Phase 3A.3.5: Consolidated components (aggressive code reduction)
from .stakeholder_repository import StakeholderRepository
from .stakeholder_processor import (
    StakeholderProcessor,
)  # Consolidates detection + content + relationships

# Phase 3A.3.3: Legacy compatibility wrappers for extracted components
from .stakeholder_layer_memory import StakeholderLayerMemory
from .stakeholder_intelligence import StakeholderIntelligence

__all__ = [
    # Consolidated components (Phase 3A.3.5)
    "StakeholderRepository",
    "StakeholderProcessor",
    # Legacy compatibility wrappers (Phase 3A.3.3)
    "StakeholderLayerMemory",
    "StakeholderIntelligence",
]
