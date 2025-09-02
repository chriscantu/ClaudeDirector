#!/usr/bin/env python3
"""
Stakeholder Intelligence Components
Phase 3A.3: SOLID Compliance Decomposition

🏗️ Martin | Platform Architecture - Component architecture design
🤝 Diego | Engineering Leadership - Stakeholder relationship intelligence
🤖 Berny | AI/ML Engineering - Modular design principles

Decomposed stakeholder intelligence components from stakeholder_intelligence_unified.py
following Single Responsibility Principle and clean architecture patterns.
"""

# Phase 3A.3.4: Core SOLID-compliant components
from .stakeholder_detection_engine import StakeholderDetectionEngine
from .stakeholder_repository import StakeholderRepository
from .content_processor import ContentProcessor
from .relationship_analyzer import RelationshipAnalyzer

# Phase 3A.3.3: Legacy compatibility wrappers for extracted components
from .stakeholder_layer_memory import StakeholderLayerMemory
from .stakeholder_intelligence import StakeholderIntelligence

__all__ = [
    # Core SOLID components (Phase 3A.3.4)
    "StakeholderDetectionEngine",
    "StakeholderRepository",
    "ContentProcessor",
    "RelationshipAnalyzer",
    # Legacy compatibility wrappers (Phase 3A.3.3)
    "StakeholderLayerMemory",
    "StakeholderIntelligence",
]
