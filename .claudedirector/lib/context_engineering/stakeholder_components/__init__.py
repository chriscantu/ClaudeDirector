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

from .stakeholder_layer_memory import StakeholderLayerMemory
from .stakeholder_intelligence import StakeholderIntelligence

__all__ = [
    "StakeholderLayerMemory",
    "StakeholderIntelligence",
]
