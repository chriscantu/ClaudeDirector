"""
Stakeholder Repository - Phase 3A.3.4 SOLID Extraction
Single Responsibility: Stakeholder data persistence and CRUD operations

Extracted from StakeholderIntelligenceUnified for SOLID compliance
Author: Martin | Platform Architecture with Sequential7 methodology
"""

import time
import logging
from typing import Dict, List, Any, Optional

# Import types
from ..stakeholder_intelligence_types import (
    StakeholderRole,
    CommunicationStyle,
    InfluenceLevel,
    StakeholderProfile,
)


class StakeholderRepository:
    """
    Stakeholder data repository with CRUD operations

    Single Responsibility: Manage stakeholder data persistence, caching,
    and filtering operations with performance optimization.
    """

    def __init__(
        self,
        cache_manager=None,
        enable_performance: bool = True,
        max_stakeholders: int = 500,
    ):
        """Initialize repository"""
        self.logger = logging.getLogger(__name__)
        self.cache_manager = cache_manager
        self.enable_performance = enable_performance and cache_manager is not None
        self.max_stakeholders = max_stakeholders

        # In-memory storage
        self.stakeholders: Dict[str, StakeholderProfile] = {}

    def add_stakeholder(
        self,
        stakeholder_data: Dict[str, Any],
        source: str = "manual",
        confidence: float = 1.0,
    ) -> bool:
        """
        Add or update stakeholder profile

        Args:
            stakeholder_data: Comprehensive stakeholder information
            source: Source of the data (manual, ai_detection, file_analysis)
            confidence: Confidence level for AI-detected stakeholders

        Returns:
            True if successful, False otherwise
        """
        try:
            stakeholder_id = stakeholder_data.get(
                "stakeholder_id"
            ) or stakeholder_data.get("name", "").lower().replace(" ", "_")

            if not stakeholder_id:
                self.logger.warning("Cannot add stakeholder without ID or name")
                return False

            current_time = time.time()

            if stakeholder_id in self.stakeholders:
                # Update existing profile
                profile = self.stakeholders[stakeholder_id]
                self._update_existing_profile(profile, stakeholder_data, current_time)
            else:
                # Check max stakeholders limit
                if len(self.stakeholders) >= self.max_stakeholders:
                    self.logger.warning(
                        f"Maximum stakeholders limit reached: {self.max_stakeholders}"
                    )
                    return False

                # Create new profile
                profile = self._create_new_profile(
                    stakeholder_data, stakeholder_id, current_time, source, confidence
                )
                self.stakeholders[stakeholder_id] = profile

            # Cache invalidation for performance
            if self.enable_performance:
                self.cache_manager.delete_pattern(f"stakeholder_*")

            self.logger.debug(f"Added/updated stakeholder: {stakeholder_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add stakeholder: {e}")
            return False

    def get_stakeholder(self, stakeholder_id: str) -> Optional[StakeholderProfile]:
        """Get stakeholder profile by ID"""
        return self.stakeholders.get(stakeholder_id)

    def list_stakeholders(
        self, filter_by: Optional[Dict[str, Any]] = None, include_metadata: bool = False
    ) -> List[Dict[str, Any]]:
        """
        List stakeholders with optional filtering

        Args:
            filter_by: Optional filters (role, influence_level, platform_position, etc.)
            include_metadata: Include detection and timing metadata

        Returns:
            List of stakeholder profiles as dictionaries
        """
        try:
            # Use cached result if available
            if self.enable_performance:
                cache_key = (
                    f"stakeholder_list:{hash(str(sorted((filter_by or {}).items())))}"
                )
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            stakeholders = list(self.stakeholders.values())

            # Apply filters
            if filter_by:
                stakeholders = self._apply_stakeholder_filters(stakeholders, filter_by)

            # Convert to dictionaries
            result = []
            for stakeholder in stakeholders:
                data = stakeholder.to_dict()
                if not include_metadata:
                    # Remove metadata for cleaner API
                    metadata_keys = [
                        "detection_confidence",
                        "auto_created",
                        "created_timestamp",
                        "updated_timestamp",
                        "source_files",
                    ]
                    for key in metadata_keys:
                        data.pop(key, None)
                result.append(data)

            # Cache result
            if self.enable_performance:
                self.cache_manager.set(cache_key, result, ttl=3600)  # 1 hour cache

            return result

        except Exception as e:
            self.logger.error(f"Failed to list stakeholders: {e}")
            return []

    def remove_stakeholder(self, stakeholder_id: str) -> bool:
        """Remove stakeholder from repository"""
        try:
            if stakeholder_id in self.stakeholders:
                del self.stakeholders[stakeholder_id]

                # Cache invalidation
                if self.enable_performance:
                    self.cache_manager.delete_pattern(f"stakeholder_*")

                self.logger.debug(f"Removed stakeholder: {stakeholder_id}")
                return True
            else:
                self.logger.warning(
                    f"Stakeholder not found for removal: {stakeholder_id}"
                )
                return False

        except Exception as e:
            self.logger.error(f"Failed to remove stakeholder: {e}")
            return False

    def get_stakeholder_count(self) -> int:
        """Get total number of stakeholders"""
        return len(self.stakeholders)

    def get_stakeholder_ids(self) -> List[str]:
        """Get all stakeholder IDs"""
        return list(self.stakeholders.keys())

    def _create_new_profile(
        self,
        stakeholder_data: Dict[str, Any],
        stakeholder_id: str,
        current_time: float,
        source: str,
        confidence: float,
    ) -> StakeholderProfile:
        """Create new stakeholder profile with defaults"""
        return StakeholderProfile(
            stakeholder_id=stakeholder_id,
            name=stakeholder_data.get("name", ""),
            role=StakeholderRole(stakeholder_data.get("role", "other")),
            organization=stakeholder_data.get("organization", ""),
            communication_style=CommunicationStyle(
                stakeholder_data.get("communication_style", "collaborative")
            ),
            influence_level=InfluenceLevel(
                stakeholder_data.get("influence_level", "medium")
            ),
            # Enhanced fields
            collaboration_patterns=stakeholder_data.get("collaboration_patterns", []),
            preferred_frameworks=stakeholder_data.get("preferred_frameworks", []),
            conflict_triggers=stakeholder_data.get("conflict_triggers", []),
            success_patterns=stakeholder_data.get("success_patterns", []),
            decision_making_style=stakeholder_data.get(
                "decision_making_style", "collaborative"
            ),
            key_interests=stakeholder_data.get("key_interests", []),
            platform_position=stakeholder_data.get("platform_position", "unknown"),
            # Metrics
            interaction_frequency=stakeholder_data.get("interaction_frequency", 1.0),
            last_interaction=current_time,
            relationship_quality=stakeholder_data.get("relationship_quality", 0.7),
            trust_level=stakeholder_data.get("trust_level", 0.7),
            # Detection metadata
            detection_confidence=confidence,
            validated=source == "manual",
            auto_created=source != "manual",
            # Timestamps
            created_timestamp=current_time,
            updated_timestamp=current_time,
            source_files=stakeholder_data.get("source_files", []),
        )

    def _update_existing_profile(
        self,
        profile: StakeholderProfile,
        stakeholder_data: Dict[str, Any],
        current_time: float,
    ) -> None:
        """Update existing stakeholder profile with new data"""
        for key, value in stakeholder_data.items():
            if hasattr(profile, key) and value is not None:
                # Handle enum fields
                if key == "role" and isinstance(value, str):
                    profile.role = StakeholderRole(value)
                elif key == "communication_style" and isinstance(value, str):
                    profile.communication_style = CommunicationStyle(value)
                elif key == "influence_level" and isinstance(value, str):
                    profile.influence_level = InfluenceLevel(value)
                else:
                    setattr(profile, key, value)

        profile.updated_timestamp = current_time
        profile.last_interaction = current_time

    def _apply_stakeholder_filters(
        self, stakeholders: List[StakeholderProfile], filters: Dict[str, Any]
    ) -> List[StakeholderProfile]:
        """Apply filters to stakeholder list"""
        filtered = stakeholders

        if "role" in filters:
            role_filter = filters["role"]
            if isinstance(role_filter, str):
                filtered = [s for s in filtered if s.role.value == role_filter]
            elif isinstance(role_filter, list):
                filtered = [s for s in filtered if s.role.value in role_filter]

        if "influence_level" in filters:
            influence_filter = filters["influence_level"]
            if isinstance(influence_filter, str):
                filtered = [
                    s for s in filtered if s.influence_level.value == influence_filter
                ]
            elif isinstance(influence_filter, list):
                filtered = [
                    s for s in filtered if s.influence_level.value in influence_filter
                ]

        if "platform_position" in filters:
            position_filter = filters["platform_position"]
            if isinstance(position_filter, str):
                filtered = [
                    s for s in filtered if s.platform_position == position_filter
                ]
            elif isinstance(position_filter, list):
                filtered = [
                    s for s in filtered if s.platform_position in position_filter
                ]

        if "organization" in filters:
            org_filter = filters["organization"]
            if isinstance(org_filter, str):
                filtered = [s for s in filtered if s.organization == org_filter]
            elif isinstance(org_filter, list):
                filtered = [s for s in filtered if s.organization in org_filter]

        if "validated" in filters:
            validated_filter = filters["validated"]
            filtered = [s for s in filtered if s.validated == validated_filter]

        if "auto_created" in filters:
            auto_filter = filters["auto_created"]
            filtered = [s for s in filtered if s.auto_created == auto_filter]

        if "min_trust_level" in filters:
            min_trust = float(filters["min_trust_level"])
            filtered = [s for s in filtered if s.trust_level >= min_trust]

        if "min_relationship_quality" in filters:
            min_quality = float(filters["min_relationship_quality"])
            filtered = [s for s in filtered if s.relationship_quality >= min_quality]

        return filtered

    def get_repository_stats(self) -> Dict[str, Any]:
        """Get repository statistics"""
        if not self.stakeholders:
            return {"total_stakeholders": 0, "status": "empty"}

        stakeholder_list = list(self.stakeholders.values())

        # Role distribution
        role_distribution = {}
        for profile in stakeholder_list:
            role = profile.role.value
            role_distribution[role] = role_distribution.get(role, 0) + 1

        # Influence distribution
        influence_distribution = {}
        for profile in stakeholder_list:
            influence = profile.influence_level.value
            influence_distribution[influence] = (
                influence_distribution.get(influence, 0) + 1
            )

        return {
            "total_stakeholders": len(stakeholder_list),
            "role_distribution": role_distribution,
            "influence_distribution": influence_distribution,
            "auto_created_count": sum(1 for s in stakeholder_list if s.auto_created),
            "validated_count": sum(1 for s in stakeholder_list if s.validated),
            "average_trust_level": sum(s.trust_level for s in stakeholder_list)
            / len(stakeholder_list),
            "average_relationship_quality": sum(
                s.relationship_quality for s in stakeholder_list
            )
            / len(stakeholder_list),
        }
