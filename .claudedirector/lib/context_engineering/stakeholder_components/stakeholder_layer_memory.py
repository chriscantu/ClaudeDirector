#!/usr/bin/env python3
"""
Stakeholder Layer Memory Compatibility
Phase 3A.3.3: Legacy Compatibility Extraction for SOLID Compliance

🏗️ Martin | Platform Architecture - SOLID Single Responsibility Principle
🤝 Diego | Engineering Leadership - Stakeholder memory management
🤖 Berny | AI/ML Engineering - Legacy system compatibility

Extracted from stakeholder_intelligence_unified.py to provide clean separation
of legacy compatibility concerns from core intelligence functionality.
"""

from typing import Dict, Any


class StakeholderLayerMemory:
    """Legacy compatibility wrapper for StakeholderLayerMemory

    Single Responsibility: Provide backward compatibility for legacy
    stakeholder layer memory interfaces while delegating to the unified system.

    This class maintains API compatibility for existing code that expects
    the legacy StakeholderLayerMemory interface, ensuring zero-disruption
    migration to the unified stakeholder intelligence system.

    Note: Implementation will be injected to avoid circular dependencies.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize with legacy configuration compatibility"""
        # Import here to avoid circular dependency
        from ..stakeholder_intelligence_unified import StakeholderIntelligenceUnified

        self._unified = StakeholderIntelligenceUnified(config)

    def update_stakeholder_profile(self, stakeholder_data: Dict[str, Any]) -> bool:
        """Update stakeholder profile via unified system"""
        return self._unified.add_stakeholder(stakeholder_data)

    def record_interaction(self, interaction_data: Dict[str, Any]) -> bool:
        """Record stakeholder interaction via unified system"""
        stakeholder_id = interaction_data.get("stakeholder_id", "")
        return self._unified.record_interaction(stakeholder_id, interaction_data)

    def get_relationship_context(self, query: str) -> Dict[str, Any]:
        """Get relationship context via unified system"""
        return self._unified.get_relationship_context(query)

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics via unified system"""
        return self._unified.get_memory_usage()
