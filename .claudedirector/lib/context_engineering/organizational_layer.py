"""
Organizational Layer Memory
Phase 3B.1.2: Consolidated facade using OrganizationalProcessor

Cultural context, team dynamics, and institutional knowledge.
Provides organizational intelligence for strategic adaptation.

🏗️ Martin | Platform Architecture - Facade pattern for API compatibility
🤖 Berny | AI/ML Engineering - Consolidated backend processing
🎯 Diego | Engineering Leadership - Zero-breaking-change consolidation
"""

from typing import Dict, List, Any, Optional
import time
import logging
from dataclasses import asdict

# Phase 3B.1.2: Use consolidated processor for backend functionality
from .organizational_processor import OrganizationalProcessor

# Import types from extracted module (Phase 3B.1.1 - Code Reduction)
from .organizational_types import (
    OrganizationSize,
    CulturalDimension,
    TeamStructure,
    OrganizationalChange,
    OrganizationalProfile,
    CulturalObservation,
    KnowledgeArtifact,
    OrganizationalRecommendation,
    OrganizationalHealthMetrics,
)


class OrganizationalLayerMemory:
    """
    Organizational context and institutional knowledge management
    Phase 3B.1.2: Facade pattern delegating to consolidated OrganizationalProcessor

    Features:
    - Cultural context adaptation and learning
    - Team dynamics tracking and optimization
    - Organizational change pattern recognition
    - Institutional knowledge preservation and application

    All core functionality consolidated in OrganizationalProcessor for DRY compliance.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize organizational layer with consolidated processor backend
        Phase 3B.1.2: Facade pattern delegates to OrganizationalProcessor
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Phase 3B.1.2: Initialize consolidated processor backend
        self.processor = OrganizationalProcessor(config)

        # Maintain API compatibility by exposing processor attributes
        self.organizational_profile = self.processor.organizational_profile
        self.team_structures = self.processor.team_structures
        self.organizational_changes = self.processor.organizational_changes
        self.cultural_observations = self.processor.cultural_observations
        self.knowledge_artifacts = self.processor.knowledge_artifacts

        # Legacy configuration access for backward compatibility
        self.max_team_history = self.processor.max_team_history
        self.change_retention_days = self.processor.change_retention_days

        self.logger.info(
            "OrganizationalLayerMemory initialized with consolidated processor backend"
        )

    def update_organizational_profile(self, profile_data: Dict[str, Any]) -> bool:
        """🏗️ Sequential Thinking: Simplified profile update delegation"""
        return self.processor.update_organizational_profile(profile_data)

    def track_team_structure(self, team_data: Dict[str, Any]) -> bool:
        """🏗️ Sequential Thinking: Simplified team tracking delegation"""
        return self.processor.track_team_structure(team_data)

    def record_organizational_change(self, change_data: Dict[str, Any]) -> bool:
        """🏗️ Sequential Thinking: Simplified change recording delegation"""
        return "error" not in self.processor.track_organizational_change(change_data)

    def add_knowledge_artifact(self, artifact_data: Dict[str, Any]) -> bool:
        """🏗️ Sequential Thinking: Simplified artifact addition delegation"""
        return self.processor.add_knowledge_artifact(artifact_data)

    def get_structure_context(self) -> Dict[str, Any]:
        """🏗️ Sequential Thinking: Simplified context retrieval delegation"""
        return self.processor.get_comprehensive_analysis()

    def get_memory_usage(self) -> Dict[str, Any]:
        """
        Get memory usage statistics
        Phase 3B.1.2: Simplified implementation using consolidated processor
        """
        try:
            # Get basic statistics from consolidated processor
            return {
                "organizational_profile_size": len(
                    str(self.processor.organizational_profile)
                ),
                "team_structures_count": len(self.processor.team_structures),
                "organizational_changes_count": len(
                    self.processor.organizational_changes
                ),
                "cultural_observations_count": len(
                    self.processor.cultural_observations
                ),
                "knowledge_artifacts_count": len(self.processor.knowledge_artifacts),
                "learning_patterns_count": len(self.processor.learning_patterns),
                "cache_entries": len(self.processor._analysis_cache),
                "total_estimated_kb": self._estimate_total_memory_kb(),
            }
        except Exception as e:
            self.logger.error(f"Failed to get memory usage: {e}")
            return {"error": str(e)}

    def _estimate_total_memory_kb(self) -> float:
        """Estimate total memory usage in KB"""
        try:
            # Simple estimation based on string representation lengths
            profile_size = len(str(self.processor.organizational_profile))
            structures_size = sum(
                len(str(s)) for s in self.processor.team_structures.values()
            )
            changes_size = sum(
                len(str(c)) for c in self.processor.organizational_changes.values()
            )
            observations_size = sum(
                len(str(o)) for o in self.processor.cultural_observations
            )
            artifacts_size = sum(
                len(str(a)) for a in self.processor.knowledge_artifacts
            )
            patterns_size = sum(len(str(p)) for p in self.processor.learning_patterns)

            total_chars = (
                profile_size
                + structures_size
                + changes_size
                + observations_size
                + artifacts_size
                + patterns_size
            )
            return total_chars / 1024.0  # Rough estimate: 1 char ≈ 1 byte
        except Exception:
            return 0.0
