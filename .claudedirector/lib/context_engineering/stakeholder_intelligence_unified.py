"""
Stakeholder Intelligence Unified Module - Phase 9 Consolidation

This module consolidates all stakeholder intelligence functionality from:
- context_engineering/stakeholder_layer.py
- intelligence/stakeholder.py
- memory/intelligent_stakeholder_detector.py
- memory/stakeholder_engagement_engine.py
- p2_communication/stakeholder_targeting/

Status: Phase 9 Architecture Cleanup - Single Source of Truth Implementation
Author: Martin | Platform Architecture with MCP Sequential enhancement
"""

import sys
import time
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# Phase 3A.3.1: Extract type definitions for SOLID compliance
from .stakeholder_intelligence_types import (
    StakeholderRole,
    CommunicationStyle,
    InfluenceLevel,
    StakeholderProfile,
)

# Add project root to path for legacy imports during transition
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

# Enhanced imports for Phase 9 integration + Phase 2 Migration
try:
    from ..core.config import get_config

    # Phase 2 Migration: Prefer UnifiedDatabaseCoordinator
    try:
        from ..core.unified_database import (
            get_unified_database_coordinator as get_database_manager,
        )

        print(
            "📊 Phase 2: Using UnifiedDatabaseCoordinator for stakeholder intelligence"
        )
    except ImportError:
        from ..core.database import get_database_manager

        print(
            "📊 Phase 2: Fallback to legacy DatabaseManager for stakeholder intelligence"
        )

    from ..core.exceptions import AIDetectionError, DatabaseError
    from ..performance.cache_manager import get_cache_manager
    from ..performance.memory_optimizer import get_memory_optimizer
    from ..performance.response_optimizer import get_response_optimizer
except ImportError:
    # Graceful fallback for migration period
    logging.warning(
        "Phase 9 migration: Using legacy imports for stakeholder intelligence"
    )

    class MinimalConfig:
        def __init__(self):
            self.database_path = str(PROJECT_ROOT / "data" / "strategic_memory.db")
            self.workspace_dir = str(PROJECT_ROOT / "leadership-workspace")

        @property
        def workspace_path_obj(self):
            return Path(self.workspace_dir)

    def get_config():
        return MinimalConfig()

    class AIDetectionError(Exception):
        def __init__(self, message, detection_type=None):
            super().__init__(message)
            self.detection_type = detection_type

    class DatabaseError(Exception):
        pass


class StakeholderIntelligenceUnified:
    """
    Unified Stakeholder Intelligence System - Phase 9 Single Source of Truth

    Consolidates functionality from:
    - StakeholderLayerMemory (context_engineering)
    - StakeholderIntelligence (intelligence layer)
    - IntelligentStakeholderDetector (memory layer)
    - StakeholderEngagementEngine (memory layer)

    Features:
    - AI-powered stakeholder detection and profiling
    - Relationship intelligence and pattern analysis
    - Communication optimization and conflict resolution
    - Enterprise-grade performance with caching and optimization
    - Complete backward compatibility during migration
    """

    def __init__(
        self, config: Optional[Dict[str, Any]] = None, enable_performance: bool = True
    ):
        """Initialize unified stakeholder intelligence system"""
        self.config = config or get_config()
        self.logger = logging.getLogger(__name__)
        self.enable_performance = enable_performance

        # Storage configuration
        self.max_stakeholders = getattr(self.config, "max_stakeholders", 500)
        self.interaction_retention_days = getattr(
            self.config, "interaction_retention", 365
        )

        # Initialize performance components (Phase 8 integration)
        if self.enable_performance:
            try:
                self.cache_manager = get_cache_manager()
                self.memory_optimizer = get_memory_optimizer()
                self.response_optimizer = get_response_optimizer()
                self.logger.info(
                    "Phase 8 performance optimization enabled for stakeholder intelligence"
                )
            except Exception as e:
                self.logger.warning(f"Performance optimization unavailable: {e}")
                self.enable_performance = False

        # In-memory storage (Phase 9.1)
        # Phase 9.2 will add SQLite persistent storage with relationship analytics
        self.stakeholders: Dict[str, StakeholderProfile] = {}
        self.interactions: List[Dict[str, Any]] = []

        # Legacy compatibility layer for migration period
        self._init_legacy_compatibility()

        self.logger.info(
            "StakeholderIntelligenceUnified initialized - Phase 9 consolidation active"
        )

    def _init_legacy_compatibility(self) -> None:
        """Initialize legacy compatibility during migration"""
        try:
            # Try to import legacy stakeholder data
            self._migrate_legacy_stakeholder_data()
        except Exception as e:
            self.logger.warning(f"Legacy migration skipped: {e}")

    def _migrate_legacy_stakeholder_data(self) -> None:
        """Migrate stakeholder data from legacy systems during Phase 9"""
        # This will be implemented to preserve existing stakeholder intelligence
        # during the migration process
        pass

    # === CORE STAKEHOLDER MANAGEMENT ===

    def add_stakeholder(
        self,
        stakeholder_data: Dict[str, Any],
        source: str = "manual",
        confidence: float = 1.0,
    ) -> bool:
        """
        Add or update stakeholder profile with enhanced intelligence

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
            filtered = [s for s in filtered if s.platform_position == position_filter]

        if "validated" in filters:
            validated_filter = filters["validated"]
            filtered = [s for s in filtered if s.validated == validated_filter]

        return filtered

    # === INTERACTION TRACKING ===

    def record_interaction(
        self, stakeholder_id: str, interaction_data: Dict[str, Any]
    ) -> bool:
        """
        Record stakeholder interaction for pattern analysis

        Args:
            stakeholder_id: ID of the stakeholder
            interaction_data: Detailed interaction information

        Returns:
            True if successful, False otherwise
        """
        try:
            interaction_record = {
                "interaction_id": f"int_{int(time.time())}_{stakeholder_id}",
                "stakeholder_id": stakeholder_id,
                "context": interaction_data.get("context", ""),
                "communication_method": interaction_data.get("method", "conversation"),
                "topics_discussed": interaction_data.get("topics", []),
                "frameworks_used": interaction_data.get("frameworks", []),
                "outcome": interaction_data.get("outcome", ""),
                "satisfaction_level": interaction_data.get("satisfaction", 0.7),
                "conflicts_observed": interaction_data.get("conflicts", []),
                "collaboration_quality": interaction_data.get(
                    "collaboration_quality", 0.7
                ),
                "timestamp": time.time(),
                "session_id": interaction_data.get("session_id", "default"),
            }

            self.interactions.append(interaction_record)

            # Update stakeholder profile based on interaction
            if stakeholder_id in self.stakeholders:
                self._update_stakeholder_from_interaction(
                    stakeholder_id, interaction_record
                )

            # Cleanup old interactions
            self._cleanup_old_interactions()

            # Cache invalidation
            if self.enable_performance:
                self.cache_manager.delete_pattern(f"stakeholder_context_*")
                self.cache_manager.delete_pattern(f"relationship_health_*")

            return True

        except Exception as e:
            self.logger.error(f"Failed to record interaction: {e}")
            return False

    def _update_stakeholder_from_interaction(
        self, stakeholder_id: str, interaction: Dict[str, Any]
    ) -> None:
        """Update stakeholder profile based on interaction data"""
        if stakeholder_id not in self.stakeholders:
            return

        profile = self.stakeholders[stakeholder_id]

        # Update interaction frequency (exponential moving average)
        profile.interaction_frequency = (profile.interaction_frequency * 0.8) + (
            1.0 * 0.2
        )

        # Update relationship quality based on satisfaction
        satisfaction = interaction.get("satisfaction_level", 0.7)
        profile.relationship_quality = (profile.relationship_quality * 0.9) + (
            satisfaction * 0.1
        )

        # Update trust level based on collaboration quality
        collaboration = interaction.get("collaboration_quality", 0.7)
        if collaboration > 0.8:
            profile.trust_level = min(1.0, profile.trust_level + 0.05)
        elif collaboration < 0.5:
            profile.trust_level = max(0.0, profile.trust_level - 0.05)

        # Learn from frameworks used
        frameworks = interaction.get("frameworks_used", [])
        for framework in frameworks:
            if framework not in profile.preferred_frameworks:
                profile.preferred_frameworks.append(framework)

        # Update timestamp
        profile.last_interaction = time.time()
        profile.updated_timestamp = time.time()

    def _cleanup_old_interactions(self) -> None:
        """Remove interactions older than retention period"""
        cutoff_time = time.time() - (self.interaction_retention_days * 24 * 3600)
        self.interactions = [
            interaction
            for interaction in self.interactions
            if interaction.get("timestamp", time.time()) > cutoff_time
        ]

    # === RELATIONSHIP INTELLIGENCE ===

    def get_relationship_context(
        self, query: str, stakeholder_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive relationship context for strategic guidance

        Args:
            query: Current query to find relevant stakeholder context
            stakeholder_ids: Optional specific stakeholder IDs to include

        Returns:
            Comprehensive stakeholder context with relationship intelligence
        """
        try:
            # Use cached result if available
            if self.enable_performance:
                cache_key = f"stakeholder_context:{hash(query)}:{hash(str(sorted(stakeholder_ids or [])))}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            # Extract stakeholder mentions from query
            mentioned_stakeholders = self._extract_stakeholder_mentions(query)

            # Combine with explicitly requested stakeholders
            if stakeholder_ids:
                mentioned_stakeholders.extend(stakeholder_ids)
            mentioned_stakeholders = list(
                set(mentioned_stakeholders)
            )  # Remove duplicates

            # Get relevant stakeholder profiles
            relevant_profiles = []
            for stakeholder_id in mentioned_stakeholders:
                if stakeholder_id in self.stakeholders:
                    relevant_profiles.append(
                        self.stakeholders[stakeholder_id].to_dict()
                    )

            # Add high-influence stakeholders if none mentioned
            if not relevant_profiles:
                high_influence = [
                    profile.to_dict()
                    for profile in self.stakeholders.values()
                    if profile.influence_level
                    in [InfluenceLevel.CRITICAL, InfluenceLevel.HIGH]
                ][
                    :3
                ]  # Top 3 high-influence stakeholders
                relevant_profiles.extend(high_influence)

            # Get recent interactions
            recent_interactions = self._get_recent_interactions(mentioned_stakeholders)

            # Generate relationship insights
            insights = self._generate_relationship_insights(query, relevant_profiles)

            # Calculate relationship health metrics
            health_metrics = self._calculate_relationship_health()

            # Generate communication recommendations
            comm_recommendations = self._generate_communication_recommendations(
                query, relevant_profiles
            )

            result = {
                "relevant_stakeholders": relevant_profiles,
                "recent_interactions": recent_interactions,
                "relationship_insights": insights,
                "health_metrics": health_metrics,
                "communication_recommendations": comm_recommendations,
                "context_generated_at": time.time(),
            }

            # Cache result
            if self.enable_performance:
                self.cache_manager.set(cache_key, result, ttl=1800)  # 30 minute cache

            return result

        except Exception as e:
            self.logger.error(f"Failed to get relationship context: {e}")
            return {"relevant_stakeholders": [], "error": str(e)}

    def _extract_stakeholder_mentions(self, text: str) -> List[str]:
        """Extract potential stakeholder mentions from text using enhanced NLP"""
        text_lower = text.lower()
        mentioned = []

        # Check for explicit stakeholder names
        for stakeholder_id, profile in self.stakeholders.items():
            if profile.name.lower() in text_lower or stakeholder_id in text_lower:
                mentioned.append(stakeholder_id)

        # Enhanced role-based mentions for enterprise contexts
        role_keywords = {
            "executive": [
                "cto",
                "vp",
                "director",
                "executive",
                "leadership",
                "c-level",
                "svp",
            ],
            "engineering_manager": [
                "engineering manager",
                "eng manager",
                "team lead",
                "manager",
            ],
            "product": ["product", "pm", "product manager", "product owner"],
            "design": ["design", "designer", "ux", "ui", "user experience"],
            "engineer": [
                "engineer",
                "developer",
                "tech lead",
                "software engineer",
                "staff engineer",
            ],
            "board": ["board", "board member", "investor", "stakeholder"],
        }

        for role, keywords in role_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                # Find stakeholders with matching roles
                role_matches = [
                    stakeholder_id
                    for stakeholder_id, profile in self.stakeholders.items()
                    if role in profile.role.value
                    or any(keyword in profile.role.value for keyword in keywords)
                ]
                mentioned.extend(role_matches[:2])  # Limit to 2 per role

        return list(set(mentioned))  # Remove duplicates

    def _get_recent_interactions(
        self, stakeholder_ids: List[str], days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get recent interactions for specific stakeholders"""
        cutoff_time = time.time() - (days * 24 * 3600)

        recent = []
        for interaction in self.interactions:
            if (
                interaction.get("timestamp", 0) > cutoff_time
                and interaction.get("stakeholder_id") in stakeholder_ids
            ):
                recent.append(interaction)

        # Sort by timestamp (most recent first)
        recent.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return recent[:10]  # Return last 10 interactions

    def _generate_relationship_insights(
        self, query: str, profiles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate enhanced relationship insights for enterprise contexts"""
        insights = []

        for profile in profiles:
            stakeholder_name = profile.get("name", "")

            # Communication style insight
            style = profile.get("communication_style", "collaborative")
            insights.append(
                {
                    "type": "communication_style",
                    "stakeholder": stakeholder_name,
                    "insight": f"Prefers {style} communication approach",
                    "recommendation": self._get_style_recommendation(style),
                    "priority": "medium",
                }
            )

            # Influence level insight
            influence = profile.get("influence_level", "medium")
            if influence in ["critical", "high"]:
                insights.append(
                    {
                        "type": "influence",
                        "stakeholder": stakeholder_name,
                        "insight": f"{influence.title()} influence stakeholder - key decision maker",
                        "recommendation": "Ensure alignment and clear communication of strategic value",
                        "priority": "high",
                    }
                )

            # Platform position insight
            position = profile.get("platform_position", "unknown")
            if position == "opponent":
                insights.append(
                    {
                        "type": "platform_risk",
                        "stakeholder": stakeholder_name,
                        "insight": "Platform opponent - requires careful engagement",
                        "recommendation": "Focus on business value and address concerns directly",
                        "priority": "high",
                    }
                )
            elif position == "supporter":
                insights.append(
                    {
                        "type": "platform_opportunity",
                        "stakeholder": stakeholder_name,
                        "insight": "Platform supporter - leverage for advocacy",
                        "recommendation": "Engage for testimonials and support in decisions",
                        "priority": "medium",
                    }
                )

            # Relationship quality insight
            quality = profile.get("relationship_quality", 0.7)
            if quality < 0.5:
                insights.append(
                    {
                        "type": "relationship_risk",
                        "stakeholder": stakeholder_name,
                        "insight": f"Low relationship quality ({quality:.2f})",
                        "recommendation": "Consider relationship building activities or conflict resolution",
                        "priority": "high",
                    }
                )
            elif quality > 0.9:
                insights.append(
                    {
                        "type": "relationship_strength",
                        "stakeholder": stakeholder_name,
                        "insight": f"Strong relationship ({quality:.2f})",
                        "recommendation": "Leverage strong relationship for strategic initiatives",
                        "priority": "low",
                    }
                )

        return insights

    def _get_style_recommendation(self, style: str) -> str:
        """Get enhanced communication recommendation based on style"""
        recommendations = {
            "direct": "Use clear, concise communication with specific action items and deadlines",
            "collaborative": "Encourage input and build consensus through discussion and workshops",
            "analytical": "Provide data, metrics, ROI analysis and logical reasoning with evidence",
            "diplomatic": "Use careful language, consider multiple perspectives, and build bridges",
            "results_focused": "Emphasize outcomes, business benefits, and measurable impact",
            "executive_brief": "Provide high-level summary with key decisions and business impact",
            "technical_detail": "Include technical specifications, architecture details, and implementation plans",
        }
        return recommendations.get(
            style, "Adapt communication to stakeholder preferences"
        )

    def _calculate_relationship_health(self) -> Dict[str, Any]:
        """Calculate comprehensive relationship health metrics"""
        if not self.stakeholders:
            return {"status": "no_data"}

        stakeholder_list = list(self.stakeholders.values())
        total_stakeholders = len(stakeholder_list)

        # Basic metrics
        avg_relationship_quality = (
            sum(s.relationship_quality for s in stakeholder_list) / total_stakeholders
        )
        avg_trust_level = (
            sum(s.trust_level for s in stakeholder_list) / total_stakeholders
        )

        # Influence distribution
        influence_distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for profile in stakeholder_list:
            influence_distribution[profile.influence_level.value] += 1

        # Platform position analysis
        platform_distribution = {
            "supporter": 0,
            "neutral": 0,
            "opponent": 0,
            "unknown": 0,
        }
        for profile in stakeholder_list:
            platform_distribution[profile.platform_position] += 1

        # Recent interaction analysis
        recent_interactions = [
            i
            for i in self.interactions
            if (time.time() - i["timestamp"]) < (30 * 24 * 3600)
        ]

        # Risk indicators
        risk_indicators = []
        if platform_distribution["opponent"] > 0:
            risk_indicators.append(
                f"{platform_distribution['opponent']} platform opponents identified"
            )
        if avg_relationship_quality < 0.6:
            risk_indicators.append("Below-average relationship quality detected")
        if (
            influence_distribution["critical"] + influence_distribution["high"]
            > total_stakeholders * 0.3
        ):
            risk_indicators.append("High concentration of high-influence stakeholders")

        return {
            "total_stakeholders": total_stakeholders,
            "average_relationship_quality": avg_relationship_quality,
            "average_trust_level": avg_trust_level,
            "influence_distribution": influence_distribution,
            "platform_distribution": platform_distribution,
            "recent_interactions_count": len(recent_interactions),
            "relationship_health_score": (avg_relationship_quality + avg_trust_level)
            / 2,
            "risk_indicators": risk_indicators,
            "health_status": self._determine_health_status(
                avg_relationship_quality, avg_trust_level, risk_indicators
            ),
        }

    def _determine_health_status(
        self, avg_quality: float, avg_trust: float, risk_indicators: List[str]
    ) -> str:
        """Determine overall relationship health status"""
        combined_score = (avg_quality + avg_trust) / 2

        if len(risk_indicators) > 2:
            return "critical"
        elif combined_score < 0.5:
            return "poor"
        elif combined_score < 0.7:
            return "fair"
        elif combined_score < 0.8:
            return "good"
        else:
            return "excellent"

    def _generate_communication_recommendations(
        self, query: str, profiles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate specific communication recommendations based on context"""
        recommendations = []

        # Analyze communication needs based on query content
        query_lower = query.lower()

        if any(
            word in query_lower for word in ["decision", "decide", "choose", "select"]
        ):
            high_influence = [
                p for p in profiles if p.get("influence_level") in ["critical", "high"]
            ]
            if high_influence:
                recommendations.append(
                    {
                        "type": "decision_communication",
                        "priority": "high",
                        "message": f"Decision involves {len(high_influence)} high-influence stakeholders",
                        "action": "Ensure early engagement and clear rationale communication before announcement",
                    }
                )

        if any(
            word in query_lower
            for word in ["conflict", "problem", "issue", "disagreement"]
        ):
            recommendations.append(
                {
                    "type": "conflict_management",
                    "priority": "high",
                    "message": "Potential conflict situation detected",
                    "action": "Consider diplomatic communication approach and structured mediation",
                }
            )

        if any(
            word in query_lower for word in ["platform", "architecture", "technical"]
        ):
            opponents = [
                p for p in profiles if p.get("platform_position") == "opponent"
            ]
            if opponents:
                recommendations.append(
                    {
                        "type": "platform_opposition",
                        "priority": "high",
                        "message": f"{len(opponents)} platform opponents in stakeholder set",
                        "action": "Focus on business value, ROI, and address specific concerns with data",
                    }
                )

        if any(
            word in query_lower for word in ["budget", "cost", "investment", "resource"]
        ):
            recommendations.append(
                {
                    "type": "financial_communication",
                    "priority": "medium",
                    "message": "Financial decision context detected",
                    "action": "Prepare ROI analysis, cost-benefit breakdown, and competitive comparisons",
                }
            )

        return recommendations

    # === AI DETECTION CAPABILITIES (LEGACY CONSOLIDATION) ===

    def detect_stakeholders_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        AI-powered stakeholder detection in content
        Consolidates functionality from IntelligentStakeholderDetector

        Args:
            content: Text content to analyze
            context: Context information (file_path, category, etc.)

        Returns:
            List of detected stakeholder candidates with confidence scores
        """
        try:
            # Use performance optimization if available
            if self.enable_performance:
                cache_key = f"stakeholder_detection:{hash(content)}:{hash(str(sorted(context.items())))}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            # Enhanced AI detection logic
            candidates = self._analyze_content_for_stakeholders(content, context)

            # Cache results
            if self.enable_performance and candidates:
                self.cache_manager.set(cache_key, candidates, ttl=7200)  # 2 hour cache

            return candidates

        except Exception as e:
            raise AIDetectionError(
                f"Stakeholder detection failed: {e}", detection_type="stakeholder"
            )

    def _analyze_content_for_stakeholders(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze content for stakeholder mentions and patterns"""
        candidates = []
        content_lower = content.lower()

        # Name pattern detection (simplified for Phase 9)
        import re

        # Executive patterns
        executive_patterns = [
            r"\b([A-Z][a-z]+ [A-Z][a-z]+)\s*(?:VP|CTO|Director|SVP|Chief)",
            r"\b(?:VP|CTO|Director|SVP|Chief)\s*([A-Z][a-z]+ [A-Z][a-z]+)",
            r"\b([A-Z][a-z]+ [A-Z][a-z]+)\s*leads?\s*(?:engineering|product|design)",
        ]

        for pattern in executive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    name = " ".join(match)
                else:
                    name = match

                if len(name.strip()) > 3:  # Basic validation
                    candidates.append(
                        {
                            "name": name.strip(),
                            "role": "executive",
                            "confidence": 0.8,
                            "detection_method": "pattern_match",
                            "context": context.get("category", "general"),
                            "source_file": context.get("file_path", ""),
                            "influence_level": "high",
                        }
                    )

        # Role-based detection
        role_indicators = {
            "engineering_manager": ["engineering manager", "eng manager", "team lead"],
            "product_manager": ["product manager", "pm", "product owner"],
            "designer": ["design lead", "ux lead", "ui designer"],
            "engineer": ["software engineer", "developer", "programmer"],
        }

        for role, indicators in role_indicators.items():
            for indicator in indicators:
                if indicator in content_lower:
                    # Try to extract name near the role mention
                    role_pattern = rf"\b([A-Z][a-z]+ [A-Z][a-z]+)\s*(?:is|as|our|the)?\s*{re.escape(indicator)}"
                    matches = re.findall(role_pattern, content, re.IGNORECASE)

                    for name in matches:
                        if len(name.strip()) > 3:
                            candidates.append(
                                {
                                    "name": name.strip(),
                                    "role": role,
                                    "confidence": 0.6,
                                    "detection_method": "role_indicator",
                                    "context": context.get("category", "general"),
                                    "source_file": context.get("file_path", ""),
                                    "influence_level": "medium",
                                }
                            )

        # Remove duplicates and validate
        unique_candidates = []
        seen_names = set()

        for candidate in candidates:
            name_key = candidate["name"].lower().strip()
            if name_key not in seen_names and len(name_key) > 3:
                seen_names.add(name_key)
                unique_candidates.append(candidate)

        return unique_candidates[:10]  # Limit to top 10 candidates

    def process_content_for_stakeholders(
        self, content: str, context: Dict[str, Any], auto_create: bool = True
    ) -> Dict[str, Any]:
        """
        Process content and automatically handle stakeholder detection and creation
        Consolidates functionality from multiple legacy modules

        Args:
            content: Text content to analyze
            context: Context information
            auto_create: Whether to automatically create stakeholder profiles

        Returns:
            Processing results with counts and actions taken
        """
        try:
            # Detect stakeholder candidates
            candidates = self.detect_stakeholders_in_content(content, context)

            candidates_detected = len(candidates)
            auto_created = 0
            profiling_needed = 0

            if auto_create:
                for candidate in candidates:
                    # Check if stakeholder already exists
                    stakeholder_id = candidate["name"].lower().replace(" ", "_")

                    if stakeholder_id not in self.stakeholders:
                        # Create new stakeholder profile
                        stakeholder_data = {
                            "name": candidate["name"],
                            "role": candidate["role"],
                            "influence_level": candidate.get(
                                "influence_level", "medium"
                            ),
                            "detection_confidence": candidate["confidence"],
                            "source_files": [context.get("file_path", "")],
                        }

                        if self.add_stakeholder(
                            stakeholder_data,
                            source="ai_detection",
                            confidence=candidate["confidence"],
                        ):
                            auto_created += 1

                            # High-confidence detections need profiling
                            if candidate["confidence"] > 0.7:
                                profiling_needed += 1

            return {
                "candidates_detected": candidates_detected,
                "auto_created": auto_created,
                "profiling_needed": profiling_needed,
                "candidates": candidates,
                "processing_timestamp": time.time(),
            }

        except Exception as e:
            raise AIDetectionError(
                f"Content processing failed: {e}", detection_type="stakeholder"
            )

    # === WORKSPACE PROCESSING ===

    def process_workspace_for_stakeholders(
        self, workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process entire workspace for stakeholder detection with performance optimization
        Consolidates functionality from intelligence layer

        Args:
            workspace_path: Optional workspace path override

        Returns:
            Processing results with performance metrics
        """
        try:
            workspace_dir = (
                Path(workspace_path)
                if workspace_path
                else self.config.workspace_path_obj
            )

            # Find relevant files
            file_patterns = ["*.md", "*.txt"]
            all_files = []

            for pattern in file_patterns:
                all_files.extend(workspace_dir.rglob(pattern))

            # Filter files by size and relevance
            relevant_files = [
                f
                for f in all_files
                if 10 < f.stat().st_size < 50 * 1024 * 1024  # 10 bytes to 50MB
            ]

            if not relevant_files:
                return {
                    "files_processed": 0,
                    "stakeholders_detected": 0,
                    "auto_created": 0,
                    "needs_profiling": 0,
                    "processing_time": 0.0,
                }

            # Use performance optimization for large file sets
            if self.enable_performance and len(relevant_files) > 5:
                return self._process_files_with_optimization(
                    relevant_files, workspace_dir
                )
            else:
                return self._process_files_sequential(relevant_files, workspace_dir)

        except Exception as e:
            raise AIDetectionError(
                f"Workspace processing failed: {e}", detection_type="stakeholder"
            )

    def _process_files_with_optimization(
        self, files: List[Path], workspace_dir: Path
    ) -> Dict[str, Any]:
        """Process files using Phase 8 performance optimization"""
        start_time = time.time()

        def process_single_file(file_path: Path) -> Optional[Dict[str, Any]]:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if len(content.strip()) < 20:
                    return None

                context = self._build_file_context(file_path, workspace_dir)
                result = self.process_content_for_stakeholders(content, context)
                return {"file_path": str(file_path), "result": result}

            except Exception as e:
                self.logger.warning(f"File processing error: {file_path} - {e}")
                return None

        # Use memory optimizer for chunked processing
        total_stakeholders = 0
        total_auto_created = 0
        total_needs_profiling = 0
        files_processed = 0

        chunk_processor = lambda file_path: process_single_file(file_path)

        for chunk_result in self.memory_optimizer.process_items_in_chunks(
            files, chunk_processor, chunk_size=10
        ):
            for result in chunk_result["results"]:
                if result and "result" in result:
                    file_result = result["result"]
                    total_stakeholders += file_result.get("candidates_detected", 0)
                    total_auto_created += file_result.get("auto_created", 0)
                    total_needs_profiling += file_result.get("profiling_needed", 0)
                    files_processed += 1

        processing_time = time.time() - start_time

        return {
            "files_processed": files_processed,
            "stakeholders_detected": total_stakeholders,
            "auto_created": total_auto_created,
            "needs_profiling": total_needs_profiling,
            "processing_time": processing_time,
            "optimization_used": True,
        }

    def _process_files_sequential(
        self, files: List[Path], workspace_dir: Path
    ) -> Dict[str, Any]:
        """Process files sequentially for smaller datasets"""
        start_time = time.time()

        total_stakeholders = 0
        total_auto_created = 0
        total_needs_profiling = 0
        files_processed = 0

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if len(content.strip()) < 20:
                    continue

                context = self._build_file_context(file_path, workspace_dir)
                result = self.process_content_for_stakeholders(content, context)

                total_stakeholders += result.get("candidates_detected", 0)
                total_auto_created += result.get("auto_created", 0)
                total_needs_profiling += result.get("profiling_needed", 0)
                files_processed += 1

            except Exception as e:
                self.logger.warning(f"File processing error: {file_path} - {e}")

        processing_time = time.time() - start_time

        return {
            "files_processed": files_processed,
            "stakeholders_detected": total_stakeholders,
            "auto_created": total_auto_created,
            "needs_profiling": total_needs_profiling,
            "processing_time": processing_time,
            "optimization_used": False,
        }

    def _build_file_context(
        self, file_path: Path, workspace_dir: Path
    ) -> Dict[str, Any]:
        """Build context for file analysis"""
        relative_path = file_path.relative_to(workspace_dir)

        context = {
            "file_path": str(file_path),
            "relative_path": str(relative_path),
            "category": "general",
        }

        # Enhanced category detection
        path_parts = relative_path.parts

        if any(part in ["meeting-prep", "meetings"] for part in path_parts):
            context["category"] = "meeting_prep"
        elif any(
            part in ["initiatives", "projects", "current-initiatives"]
            for part in path_parts
        ):
            context["category"] = "current_initiatives"
        elif any(part in ["strategic", "strategy"] for part in path_parts):
            context["category"] = "strategic_docs"
        elif any(part in ["stakeholder", "relationships"] for part in path_parts):
            context["category"] = "stakeholder_management"

        return context

    # === SYSTEM MANAGEMENT ===

    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        stats = {
            "total_stakeholders": len(self.stakeholders),
            "total_interactions": len(self.interactions),
            "system_health": self._calculate_relationship_health(),
            "performance_enabled": self.enable_performance,
            "last_updated": time.time(),
        }

        if self.enable_performance:
            try:
                stats["performance_stats"] = {
                    "cache_stats": (
                        self.cache_manager.get_stats()
                        if hasattr(self.cache_manager, "get_stats")
                        else {}
                    ),
                    "memory_stats": (
                        self.memory_optimizer.get_memory_stats()
                        if hasattr(self.memory_optimizer, "get_memory_stats")
                        else {}
                    ),
                }
            except Exception as e:
                stats["performance_error"] = str(e)

        return stats

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        stakeholders_size = sum(
            len(json.dumps(profile.to_dict(), default=str).encode("utf-8"))
            for profile in self.stakeholders.values()
        )

        interactions_size = sum(
            len(json.dumps(interaction).encode("utf-8"))
            for interaction in self.interactions
        )

        return {
            "total_stakeholders": len(self.stakeholders),
            "total_interactions": len(self.interactions),
            "stakeholders_memory_bytes": stakeholders_size,
            "interactions_memory_bytes": interactions_size,
            "total_memory_bytes": stakeholders_size + interactions_size,
            "total_memory_mb": (stakeholders_size + interactions_size) / (1024 * 1024),
        }


# === BACKWARD COMPATIBILITY API ===


def get_stakeholder_intelligence(
    config: Optional[Dict[str, Any]] = None, enable_performance: bool = True
) -> StakeholderIntelligenceUnified:
    """Get unified stakeholder intelligence instance"""
    return StakeholderIntelligenceUnified(
        config=config, enable_performance=enable_performance
    )


def detect_stakeholders(content: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convenience function for stakeholder detection"""
    intelligence = get_stakeholder_intelligence()
    return intelligence.detect_stakeholders_in_content(content, context)


# Legacy compatibility for migration period
class StakeholderLayerMemory:
    """Legacy compatibility wrapper for StakeholderLayerMemory"""

    def __init__(self, config: Dict[str, Any] = None):
        self._unified = StakeholderIntelligenceUnified(config)

    def update_stakeholder_profile(self, stakeholder_data: Dict[str, Any]) -> bool:
        return self._unified.add_stakeholder(stakeholder_data)

    def record_interaction(self, interaction_data: Dict[str, Any]) -> bool:
        stakeholder_id = interaction_data.get("stakeholder_id", "")
        return self._unified.record_interaction(stakeholder_id, interaction_data)

    def get_relationship_context(self, query: str) -> Dict[str, Any]:
        return self._unified.get_relationship_context(query)

    def get_memory_usage(self) -> Dict[str, Any]:
        return self._unified.get_memory_usage()


class StakeholderIntelligence:
    """Legacy compatibility wrapper for intelligence/stakeholder.py"""

    def __init__(
        self,
        config=None,
        db_path: Optional[str] = None,
        enable_performance: bool = True,
    ):
        self._unified = StakeholderIntelligenceUnified(config, enable_performance)

    def detect_stakeholders_in_content(
        self, content: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        return self._unified.detect_stakeholders_in_content(content, context)

    def process_content_for_stakeholders(
        self, content: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self._unified.process_content_for_stakeholders(content, context)

    def list_stakeholders(
        self, filter_by: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return self._unified.list_stakeholders(filter_by)

    def add_stakeholder(
        self, stakeholder_key: str, display_name: str, **kwargs
    ) -> bool:
        stakeholder_data = {"name": display_name, **kwargs}
        return self._unified.add_stakeholder(stakeholder_data)

    def get_stakeholder(self, stakeholder_key: str) -> Optional[Dict[str, Any]]:
        profile = self._unified.get_stakeholder(stakeholder_key)
        return profile.to_dict() if profile else None

    def process_workspace_for_stakeholders(
        self, workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        return self._unified.process_workspace_for_stakeholders(workspace_path)

    def get_system_stats(self) -> Dict[str, Any]:
        return self._unified.get_system_stats()
