"""
Stakeholder Layer Memory

Relationship mapping, communication preferences, and interaction patterns.
Provides stakeholder intelligence for strategic recommendations.
"""

from typing import Dict, List, Any, Optional
import time
import logging
from dataclasses import dataclass, asdict
from enum import Enum


class StakeholderRole(Enum):
    """Stakeholder role classification"""

    EXECUTIVE = "executive"
    ENGINEERING_MANAGER = "engineering_manager"
    PRODUCT_MANAGER = "product_manager"
    DESIGNER = "designer"
    ENGINEER = "engineer"
    VENDOR = "vendor"
    CUSTOMER = "customer"
    OTHER = "other"


class CommunicationStyle(Enum):
    """Communication style preferences"""

    DIRECT = "direct"
    COLLABORATIVE = "collaborative"
    ANALYTICAL = "analytical"
    DIPLOMATIC = "diplomatic"
    RESULTS_FOCUSED = "results_focused"


@dataclass
class StakeholderProfile:
    """Stakeholder profile with interaction intelligence"""

    stakeholder_id: str
    name: str
    role: StakeholderRole
    organization: str
    communication_style: CommunicationStyle
    influence_level: str  # high, medium, low
    collaboration_patterns: List[str]
    preferred_frameworks: List[str]
    conflict_triggers: List[str]
    success_patterns: List[str]
    interaction_frequency: float  # interactions per week
    last_interaction: float
    relationship_quality: float  # 0.0 to 1.0
    trust_level: float  # 0.0 to 1.0
    decision_making_style: str
    key_interests: List[str]


class StakeholderLayerMemory:
    """
    Stakeholder relationship intelligence and communication optimization

    Features:
    - Stakeholder profiling with communication preferences
    - Interaction pattern analysis and optimization
    - Conflict detection and resolution strategies
    - Influence mapping and collaboration optimization
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize stakeholder layer with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Storage configuration
        self.max_stakeholders = self.config.get("max_stakeholders", 200)
        self.interaction_retention_days = self.config.get("interaction_retention", 365)

        # In-memory storage for Phase 1
        # Phase 2 will add SQLite persistent storage with relationship analytics
        self.stakeholders: Dict[str, StakeholderProfile] = {}
        self.interactions: List[Dict[str, Any]] = []

        self.logger.info(
            "StakeholderLayerMemory initialized with relationship tracking"
        )

    def update_stakeholder_profile(self, stakeholder_data: Dict[str, Any]) -> bool:
        """
        Update or create stakeholder profile

        Args:
            stakeholder_data: Stakeholder information dict

        Returns:
            True if update successful, False otherwise
        """
        try:
            stakeholder_id = stakeholder_data.get(
                "stakeholder_id"
            ) or stakeholder_data.get("name", "").lower().replace(" ", "_")

            if not stakeholder_id:
                self.logger.warning("Cannot update stakeholder without ID or name")
                return False

            # Create or update stakeholder profile
            if stakeholder_id in self.stakeholders:
                # Update existing profile
                profile = self.stakeholders[stakeholder_id]
                for key, value in stakeholder_data.items():
                    if hasattr(profile, key) and value is not None:
                        setattr(profile, key, value)
                profile.last_interaction = time.time()
            else:
                # Create new profile
                profile = StakeholderProfile(
                    stakeholder_id=stakeholder_id,
                    name=stakeholder_data.get("name", ""),
                    role=StakeholderRole(stakeholder_data.get("role", "other")),
                    organization=stakeholder_data.get("organization", ""),
                    communication_style=CommunicationStyle(
                        stakeholder_data.get("communication_style", "collaborative")
                    ),
                    influence_level=stakeholder_data.get("influence_level", "medium"),
                    collaboration_patterns=stakeholder_data.get(
                        "collaboration_patterns", []
                    ),
                    preferred_frameworks=stakeholder_data.get(
                        "preferred_frameworks", []
                    ),
                    conflict_triggers=stakeholder_data.get("conflict_triggers", []),
                    success_patterns=stakeholder_data.get("success_patterns", []),
                    interaction_frequency=stakeholder_data.get(
                        "interaction_frequency", 1.0
                    ),
                    last_interaction=time.time(),
                    relationship_quality=stakeholder_data.get(
                        "relationship_quality", 0.7
                    ),
                    trust_level=stakeholder_data.get("trust_level", 0.7),
                    decision_making_style=stakeholder_data.get(
                        "decision_making_style", "collaborative"
                    ),
                    key_interests=stakeholder_data.get("key_interests", []),
                )
                self.stakeholders[stakeholder_id] = profile

            self.logger.debug(f"Updated stakeholder profile: {stakeholder_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update stakeholder profile: {e}")
            return False

    def record_interaction(self, interaction_data: Dict[str, Any]) -> bool:
        """
        Record stakeholder interaction for pattern analysis

        Args:
            interaction_data: Interaction details dict

        Returns:
            True if recording successful, False otherwise
        """
        try:
            interaction_record = {
                "interaction_id": f"int_{int(time.time())}",
                "stakeholder_id": interaction_data.get("stakeholder_id", ""),
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
            stakeholder_id = interaction_record["stakeholder_id"]
            if stakeholder_id in self.stakeholders:
                self._update_stakeholder_from_interaction(
                    stakeholder_id, interaction_record
                )

            # Cleanup old interactions
            self._cleanup_old_interactions()

            return True

        except Exception as e:
            self.logger.error(f"Failed to record interaction: {e}")
            return False

    def get_relationship_context(self, query: str) -> Dict[str, Any]:
        """
        Get relevant stakeholder relationship context

        Args:
            query: Current query to find relevant stakeholder context

        Returns:
            Stakeholder context with relationship intelligence
        """
        try:
            # Extract potential stakeholder mentions from query
            mentioned_stakeholders = self._extract_stakeholder_mentions(query)

            # Get relevant stakeholder profiles
            relevant_profiles = []
            for stakeholder_id in mentioned_stakeholders:
                if stakeholder_id in self.stakeholders:
                    relevant_profiles.append(asdict(self.stakeholders[stakeholder_id]))

            # Add high-influence stakeholders if none mentioned
            if not relevant_profiles:
                high_influence = [
                    asdict(profile)
                    for profile in self.stakeholders.values()
                    if profile.influence_level == "high"
                ][
                    :3
                ]  # Top 3 high-influence stakeholders
                relevant_profiles.extend(high_influence)

            # Get recent interactions
            recent_interactions = [
                interaction
                for interaction in self.interactions
                if (time.time() - interaction["timestamp"])
                < (30 * 24 * 3600)  # Last 30 days
            ][
                -10:
            ]  # Last 10 interactions

            # Generate relationship insights
            insights = self._generate_relationship_insights(query, relevant_profiles)

            # Calculate relationship health metrics
            health_metrics = self._calculate_relationship_health()

            return {
                "relevant_stakeholders": relevant_profiles,
                "recent_interactions": recent_interactions,
                "relationship_insights": insights,
                "health_metrics": health_metrics,
                "communication_recommendations": self._generate_communication_recommendations(
                    query, relevant_profiles
                ),
            }

        except Exception as e:
            self.logger.error(f"Failed to get relationship context: {e}")
            return {"relevant_stakeholders": [], "error": str(e)}

    def _extract_stakeholder_mentions(self, text: str) -> List[str]:
        """Extract potential stakeholder mentions from text"""
        text_lower = text.lower()
        mentioned = []

        # Check for explicit stakeholder names
        for stakeholder_id, profile in self.stakeholders.items():
            if profile.name.lower() in text_lower or stakeholder_id in text_lower:
                mentioned.append(stakeholder_id)

        # Check for role-based mentions
        role_keywords = {
            "executive": ["cto", "vp", "director", "executive", "leadership"],
            "product": ["product", "pm", "product manager"],
            "design": ["design", "designer", "ux", "ui"],
            "engineering": ["engineer", "developer", "tech lead"],
        }

        for role, keywords in role_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                # Find stakeholders with matching roles
                role_matches = [
                    stakeholder_id
                    for stakeholder_id, profile in self.stakeholders.items()
                    if role in profile.role.value
                ]
                mentioned.extend(role_matches[:2])  # Limit to 2 per role

        return list(set(mentioned))  # Remove duplicates

    def _update_stakeholder_from_interaction(
        self, stakeholder_id: str, interaction: Dict[str, Any]
    ) -> None:
        """Update stakeholder profile based on interaction data"""
        if stakeholder_id not in self.stakeholders:
            return

        profile = self.stakeholders[stakeholder_id]

        # Update interaction frequency (simple moving average)
        profile.interaction_frequency = (profile.interaction_frequency * 0.8) + (
            1.0 * 0.2
        )

        # Update relationship quality based on satisfaction
        satisfaction = interaction.get("satisfaction_level", 0.7)
        profile.relationship_quality = (profile.relationship_quality * 0.9) + (
            satisfaction * 0.1
        )

        # Update collaboration quality
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

        # Update last interaction time
        profile.last_interaction = time.time()

    def _generate_relationship_insights(
        self, query: str, profiles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate insights about stakeholder relationships"""
        insights = []

        for profile in profiles:
            # Communication style insight
            style = profile.get("communication_style", "collaborative")
            insights.append(
                {
                    "type": "communication_style",
                    "stakeholder": profile.get("name", ""),
                    "insight": f"Prefers {style} communication approach",
                    "recommendation": self._get_style_recommendation(style),
                }
            )

            # Influence level insight
            influence = profile.get("influence_level", "medium")
            if influence == "high":
                insights.append(
                    {
                        "type": "influence",
                        "stakeholder": profile.get("name", ""),
                        "insight": "High influence stakeholder - key decision maker",
                        "recommendation": "Ensure alignment and clear communication of strategic value",
                    }
                )

            # Relationship quality insight
            quality = profile.get("relationship_quality", 0.7)
            if quality < 0.5:
                insights.append(
                    {
                        "type": "relationship_risk",
                        "stakeholder": profile.get("name", ""),
                        "insight": f"Low relationship quality ({quality:.2f})",
                        "recommendation": "Consider relationship building activities or conflict resolution",
                    }
                )

        return insights

    def _get_style_recommendation(self, style: str) -> str:
        """Get communication recommendation based on style"""
        recommendations = {
            "direct": "Use clear, concise communication with specific action items",
            "collaborative": "Encourage input and build consensus through discussion",
            "analytical": "Provide data, metrics, and logical reasoning",
            "diplomatic": "Use careful language and consider multiple perspectives",
            "results_focused": "Emphasize outcomes, benefits, and measurable impact",
        }
        return recommendations.get(
            style, "Adapt communication to stakeholder preferences"
        )

    def _calculate_relationship_health(self) -> Dict[str, Any]:
        """Calculate overall relationship health metrics"""
        if not self.stakeholders:
            return {"status": "no_data"}

        total_stakeholders = len(self.stakeholders)
        avg_relationship_quality = (
            sum(p.relationship_quality for p in self.stakeholders.values())
            / total_stakeholders
        )
        avg_trust_level = (
            sum(p.trust_level for p in self.stakeholders.values()) / total_stakeholders
        )

        # Count stakeholders by influence level
        influence_distribution = {"high": 0, "medium": 0, "low": 0}
        for profile in self.stakeholders.values():
            influence_distribution[profile.influence_level] += 1

        # Recent interaction analysis
        recent_interactions = [
            i
            for i in self.interactions
            if (time.time() - i["timestamp"]) < (30 * 24 * 3600)
        ]

        return {
            "total_stakeholders": total_stakeholders,
            "average_relationship_quality": avg_relationship_quality,
            "average_trust_level": avg_trust_level,
            "influence_distribution": influence_distribution,
            "recent_interactions_count": len(recent_interactions),
            "relationship_health_score": (avg_relationship_quality + avg_trust_level)
            / 2,
        }

    def _generate_communication_recommendations(
        self, query: str, profiles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate specific communication recommendations"""
        recommendations = []

        # Analyze communication needs based on query and stakeholder profiles
        if "decision" in query.lower() and profiles:
            high_influence = [p for p in profiles if p.get("influence_level") == "high"]
            if high_influence:
                recommendations.append(
                    {
                        "type": "decision_communication",
                        "priority": "high",
                        "message": "Decision involves high-influence stakeholders",
                        "action": "Ensure early engagement and clear rationale communication",
                    }
                )

        if "conflict" in query.lower() or "problem" in query.lower():
            recommendations.append(
                {
                    "type": "conflict_management",
                    "priority": "medium",
                    "message": "Potential conflict situation detected",
                    "action": "Consider diplomatic communication approach and mediation strategies",
                }
            )

        return recommendations

    def _cleanup_old_interactions(self) -> None:
        """Remove interactions older than retention period"""
        cutoff_time = time.time() - (self.interaction_retention_days * 24 * 3600)
        self.interactions = [
            interaction
            for interaction in self.interactions
            if interaction.get("timestamp", time.time()) > cutoff_time
        ]

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        import json

        stakeholders_size = sum(
            len(json.dumps(asdict(profile), default=str).encode("utf-8"))
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
