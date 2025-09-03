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
        """
        Update organizational profile information
        Phase 3B.1.2: Delegate to consolidated processor

        Args:
            profile_data: Organization profile updates

        Returns:
            True if update successful, False otherwise
        """
        try:
            # Update organizational profile directly (maintains compatibility)
            for key, value in profile_data.items():
                if key in self.processor.organizational_profile and value is not None:
                    self.processor.organizational_profile[key] = value

            # Update timestamp
            self.processor.organizational_profile["last_updated"] = time.time()

            # Record cultural observation through processor
            self.processor._record_cultural_observation(
                {
                    "type": "profile_update",
                    "updates": profile_data,
                    "timestamp": time.time(),
                }
            )

            self.logger.debug(
                "Updated organizational profile via consolidated processor"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to update organizational profile: {e}")
            return False

    def track_team_structure(self, team_data: Dict[str, Any]) -> bool:
        """
        Track team structure information
        Phase 3B.1.2: Delegate to consolidated processor

        Args:
            team_data: Team structure information

        Returns:
            True if tracking successful, False otherwise
        """
        try:
            team_id = team_data.get("team_id") or f"team_{int(time.time())}"

            # Create TeamStructure using consolidated types
            team_structure = TeamStructure(
                team_id=team_id,
                team_name=team_data.get("team_name", f"Team {team_id}"),
                team_type=team_data.get("team_type", "unknown"),
                size=team_data.get("size", 1),
                reporting_structure=team_data.get("reporting_structure", "unknown"),
                collaboration_patterns=team_data.get("collaboration_patterns", []),
                communication_frequency=team_data.get(
                    "communication_frequency", "weekly"
                ),
                decision_making_style=team_data.get(
                    "decision_making_style", "collaborative"
                ),
                performance_metrics=team_data.get("performance_metrics", {}),
                last_updated=time.time(),
            )

            # Store in processor's team structures
            self.processor.team_structures[team_id] = team_structure

            # Analyze team dynamics using consolidated processor
            dynamics_analysis = self.processor.analyze_team_dynamics(team_structure)

            self.logger.debug(
                f"Tracked team structure {team_id} with dynamics score: {dynamics_analysis.get('overall_dynamics_score', 0.0)}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to track team structure: {e}")
            return False

    def record_organizational_change(self, change_data: Dict[str, Any]) -> bool:
        """
        Record organizational change for pattern learning
        Phase 3B.1.2: Delegate to consolidated processor

        Args:
            change_data: Organizational change information

        Returns:
            True if recording successful, False otherwise
        """
        try:
            # Phase 3B.1.2: Delegate to consolidated processor
            result = self.processor.track_organizational_change(change_data)
            return "error" not in result

        except Exception as e:
            self.logger.error(f"Failed to record organizational change: {e}")
            return False

    def add_knowledge_artifact(self, artifact_data: Dict[str, Any]) -> bool:
        """
        Add institutional knowledge artifact
        Phase 3B.1.2: Simplified delegation to processor

        Args:
            artifact_data: Knowledge artifact information

        Returns:
            True if addition successful, False otherwise
        """
        try:
            artifact_id = (
                artifact_data.get("artifact_id") or f"artifact_{int(time.time())}"
            )

            # Create KnowledgeArtifact using consolidated types
            artifact = {
                "artifact_id": artifact_id,
                "artifact_type": artifact_data.get("artifact_type", "document"),
                "title": artifact_data.get("title", "Untitled"),
                "content": artifact_data.get("content", ""),
                "tags": artifact_data.get("tags", []),
                "author": artifact_data.get("author", "unknown"),
                "relevance_score": artifact_data.get("relevance_score", 0.5),
                "access_frequency": artifact_data.get("access_frequency", 0),
                "last_accessed": artifact_data.get("last_accessed"),
                "creation_date": time.time(),
                "metadata": artifact_data.get("metadata", {}),
            }

            # Store in processor's knowledge artifacts
            self.processor.knowledge_artifacts.append(artifact)

            # Limit artifacts using processor configuration
            max_artifacts = self.processor.max_knowledge_artifacts
            if len(self.processor.knowledge_artifacts) > max_artifacts:
                # Keep most recent artifacts
                self.processor.knowledge_artifacts = self.processor.knowledge_artifacts[
                    -max_artifacts:
                ]

            self.logger.debug(f"Added knowledge artifact {artifact_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add knowledge artifact: {e}")
            return False

    def get_structure_context(self) -> Dict[str, Any]:
        """
        Get organizational structure and cultural context
        Phase 3B.1.2: Delegate to consolidated processor comprehensive analysis

        Returns:
            Organizational context with cultural intelligence
        """
        try:
            # Phase 3B.1.2: Delegate to consolidated processor for comprehensive analysis
            return self.processor.get_comprehensive_analysis()

        except Exception as e:
            self.logger.error(f"Failed to get structure context: {e}")
            return {
                "organizational_profile": self.organizational_profile,
                "error": str(e),
            }

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
