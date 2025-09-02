#!/usr/bin/env python3
"""
Stakeholder Intelligence Compatibility
Phase 3A.3.3: Legacy Intelligence Interface Extraction for SOLID Compliance

🏗️ Martin | Platform Architecture - SOLID Single Responsibility Principle
🤝 Diego | Engineering Leadership - Stakeholder intelligence management
🤖 Berny | AI/ML Engineering - Legacy system compatibility

Extracted from stakeholder_intelligence_unified.py to provide clean separation
of legacy intelligence interface concerns from core unified functionality.
"""

from typing import Dict, Any, List, Optional


class StakeholderIntelligence:
    """Legacy compatibility wrapper for intelligence/stakeholder.py

    Single Responsibility: Provide backward compatibility for legacy
    stakeholder intelligence interfaces while delegating to the unified system.

    This class maintains API compatibility for existing code that expects
    the legacy StakeholderIntelligence interface, ensuring zero-disruption
    migration to the unified stakeholder intelligence system.

    Note: Implementation will be injected to avoid circular dependencies.
    """

    def __init__(
        self,
        config=None,
        db_path: Optional[str] = None,
        enable_performance: bool = True,
    ):
        """Initialize with legacy configuration compatibility"""
        # Import here to avoid circular dependency
        from ..stakeholder_intelligence_unified import StakeholderIntelligenceUnified

        self._unified = StakeholderIntelligenceUnified(config, enable_performance)

    def detect_stakeholders_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Detect stakeholders in content via unified system"""
        return self._unified.detect_stakeholders_in_content(content, context)

    def process_content_for_stakeholders(
        self, content: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process content for stakeholders via unified system"""
        return self._unified.process_content_for_stakeholders(content, context)

    def list_stakeholders(
        self, filter_by: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """List stakeholders via unified system"""
        return self._unified.list_stakeholders(filter_by)

    def add_stakeholder(
        self, stakeholder_key: str, display_name: str, **kwargs
    ) -> bool:
        """Add stakeholder via unified system"""
        stakeholder_data = {"name": display_name, **kwargs}
        return self._unified.add_stakeholder(stakeholder_data)

    def get_stakeholder(self, stakeholder_key: str) -> Optional[Dict[str, Any]]:
        """Get stakeholder via unified system"""
        profile = self._unified.get_stakeholder(stakeholder_key)
        return profile.to_dict() if profile else None

    def process_workspace_for_stakeholders(
        self, workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process workspace for stakeholders via unified system"""
        return self._unified.process_workspace_for_stakeholders(workspace_path)

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics via unified system"""
        return self._unified.get_system_stats()
