"""
Organizational Layer Memory

Cultural context, team dynamics, and institutional knowledge.
Provides organizational intelligence for strategic adaptation.
"""

from typing import Dict, List, Any, Optional
import time
import logging
from dataclasses import dataclass, asdict
from enum import Enum


class OrganizationSize(Enum):
    """Organization size classification"""

    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class CulturalDimension(Enum):
    """Cultural dimension classification"""

    HIERARCHICAL = "hierarchical"
    COLLABORATIVE = "collaborative"
    INNOVATIVE = "innovative"
    PROCESS_DRIVEN = "process_driven"
    RESULTS_ORIENTED = "results_oriented"
    CUSTOMER_FOCUSED = "customer_focused"


@dataclass
class TeamStructure:
    """Team structure information"""

    team_id: str
    team_name: str
    team_type: str  # engineering, product, design, etc.
    size: int
    reporting_structure: str
    collaboration_patterns: List[str]
    communication_frequency: str
    decision_making_style: str
    performance_metrics: Dict[str, float]
    last_updated: float


@dataclass
class OrganizationalChange:
    """Organizational change tracking"""

    change_id: str
    change_type: str  # restructure, process, technology, cultural
    description: str
    impact_areas: List[str]
    stakeholders_affected: List[str]
    success_metrics: Dict[str, float]
    resistance_factors: List[str]
    success_factors: List[str]
    start_date: float
    completion_date: Optional[float]
    effectiveness_score: float
    lessons_learned: List[str]


class OrganizationalLayerMemory:
    """
    Organizational context and institutional knowledge management

    Features:
    - Cultural context adaptation and learning
    - Team dynamics tracking and optimization
    - Organizational change pattern recognition
    - Institutional knowledge preservation and application
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize organizational layer with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.max_team_history = self.config.get("max_team_history", 50)
        self.change_retention_days = self.config.get("change_retention", 730)  # 2 years

        # In-memory storage for Phase 1
        # Phase 2 will add SQLite persistent storage with cultural analytics
        self.organizational_profile: Dict[str, Any] = self._initialize_org_profile()
        self.team_structures: Dict[str, TeamStructure] = {}
        self.organizational_changes: Dict[str, OrganizationalChange] = {}
        self.cultural_observations: List[Dict[str, Any]] = []
        self.knowledge_artifacts: List[Dict[str, Any]] = []

        self.logger.info(
            "OrganizationalLayerMemory initialized with cultural intelligence"
        )

    def update_organizational_profile(self, profile_data: Dict[str, Any]) -> bool:
        """
        Update organizational profile information

        Args:
            profile_data: Organization profile updates

        Returns:
            True if update successful, False otherwise
        """
        try:
            # Update organizational profile
            for key, value in profile_data.items():
                if key in self.organizational_profile and value is not None:
                    self.organizational_profile[key] = value

            # Update timestamp
            self.organizational_profile["last_updated"] = time.time()

            # Record cultural observation
            self._record_cultural_observation(
                {
                    "type": "profile_update",
                    "updates": profile_data,
                    "timestamp": time.time(),
                }
            )

            self.logger.debug("Updated organizational profile")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update organizational profile: {e}")
            return False

    def track_team_structure(self, team_data: Dict[str, Any]) -> bool:
        """
        Track or update team structure information

        Args:
            team_data: Team structure information

        Returns:
            True if tracking successful, False otherwise
        """
        try:
            team_id = team_data.get("team_id") or team_data.get(
                "team_name", ""
            ).lower().replace(" ", "_")

            if not team_id:
                self.logger.warning("Cannot track team without ID or name")
                return False

            # Create or update team structure
            if team_id in self.team_structures:
                # Update existing team
                team = self.team_structures[team_id]
                for key, value in team_data.items():
                    if hasattr(team, key) and value is not None:
                        setattr(team, key, value)
                team.last_updated = time.time()
            else:
                # Create new team structure
                team = TeamStructure(
                    team_id=team_id,
                    team_name=team_data.get("team_name", ""),
                    team_type=team_data.get("team_type", "unknown"),
                    size=team_data.get("size", 0),
                    reporting_structure=team_data.get("reporting_structure", ""),
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
                self.team_structures[team_id] = team

            self.logger.debug(f"Tracked team structure: {team_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to track team structure: {e}")
            return False

    def record_organizational_change(self, change_data: Dict[str, Any]) -> bool:
        """
        Record organizational change for pattern learning

        Args:
            change_data: Organizational change information

        Returns:
            True if recording successful, False otherwise
        """
        try:
            change_id = change_data.get("change_id") or f"change_{int(time.time())}"

            change = OrganizationalChange(
                change_id=change_id,
                change_type=change_data.get("change_type", "unknown"),
                description=change_data.get("description", ""),
                impact_areas=change_data.get("impact_areas", []),
                stakeholders_affected=change_data.get("stakeholders_affected", []),
                success_metrics=change_data.get("success_metrics", {}),
                resistance_factors=change_data.get("resistance_factors", []),
                success_factors=change_data.get("success_factors", []),
                start_date=change_data.get("start_date", time.time()),
                completion_date=change_data.get("completion_date"),
                effectiveness_score=change_data.get("effectiveness_score", 0.0),
                lessons_learned=change_data.get("lessons_learned", []),
            )

            self.organizational_changes[change_id] = change

            # Record cultural observation
            self._record_cultural_observation(
                {
                    "type": "organizational_change",
                    "change_type": change.change_type,
                    "impact_areas": change.impact_areas,
                    "timestamp": time.time(),
                }
            )

            # Cleanup old changes
            self._cleanup_old_changes()

            return True

        except Exception as e:
            self.logger.error(f"Failed to record organizational change: {e}")
            return False

    def add_knowledge_artifact(self, artifact_data: Dict[str, Any]) -> bool:
        """
        Add institutional knowledge artifact

        Args:
            artifact_data: Knowledge artifact information

        Returns:
            True if addition successful, False otherwise
        """
        try:
            artifact = {
                "artifact_id": f"knowledge_{int(time.time())}",
                "title": artifact_data.get("title", ""),
                "content": artifact_data.get("content", ""),
                "artifact_type": artifact_data.get(
                    "type", "general"
                ),  # decision, process, lesson, guideline
                "tags": artifact_data.get("tags", []),
                "stakeholders": artifact_data.get("stakeholders", []),
                "related_initiatives": artifact_data.get("related_initiatives", []),
                "importance_level": artifact_data.get("importance", "medium"),
                "created_date": time.time(),
                "last_accessed": time.time(),
                "access_count": 0,
            }

            self.knowledge_artifacts.append(artifact)

            # Limit artifacts
            if len(self.knowledge_artifacts) > 1000:
                # Keep most important and recently accessed
                self.knowledge_artifacts.sort(
                    key=lambda x: (x["importance_level"] == "high", x["last_accessed"]),
                    reverse=True,
                )
                self.knowledge_artifacts = self.knowledge_artifacts[:1000]

            return True

        except Exception as e:
            self.logger.error(f"Failed to add knowledge artifact: {e}")
            return False

    def get_structure_context(self) -> Dict[str, Any]:
        """
        Get organizational structure and cultural context

        Returns:
            Organizational context with cultural intelligence
        """
        try:
            # Get cultural insights
            cultural_insights = self._analyze_cultural_patterns()

            # Get team dynamics
            team_dynamics = self._analyze_team_dynamics()

            # Get change patterns
            change_patterns = self._analyze_change_patterns()

            # Get knowledge insights
            knowledge_insights = self._get_relevant_knowledge()

            # Generate organizational recommendations
            org_recommendations = self._generate_organizational_recommendations()

            return {
                "organizational_profile": self.organizational_profile,
                "cultural_insights": cultural_insights,
                "team_dynamics": team_dynamics,
                "change_patterns": change_patterns,
                "institutional_knowledge": knowledge_insights,
                "organizational_recommendations": org_recommendations,
                "organizational_health": self._calculate_organizational_health(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get structure context: {e}")
            return {
                "organizational_profile": self.organizational_profile,
                "error": str(e),
            }

    def _initialize_org_profile(self) -> Dict[str, Any]:
        """Initialize organizational profile with defaults"""
        return {
            "organization_name": "",
            "organization_size": OrganizationSize.MEDIUM.value,
            "industry": "",
            "cultural_dimensions": [CulturalDimension.COLLABORATIVE.value],
            "primary_values": [],
            "communication_style": "balanced",
            "decision_making_approach": "consensus",
            "change_tolerance": "medium",
            "innovation_focus": "medium",
            "risk_tolerance": "medium",
            "hierarchy_level": "medium",
            "geographic_distribution": "single_location",
            "remote_work_adoption": "hybrid",
            "technology_maturity": "medium",
            "learning_orientation": "medium",
            "performance_focus": "balanced",
            "last_updated": time.time(),
        }

    def _record_cultural_observation(self, observation: Dict[str, Any]) -> None:
        """Record cultural observation for pattern analysis"""
        self.cultural_observations.append(observation)

        # Limit observations
        if len(self.cultural_observations) > 1000:
            self.cultural_observations = self.cultural_observations[-1000:]

    def _cleanup_old_changes(self) -> None:
        """Remove organizational changes older than retention period"""
        cutoff_time = time.time() - (self.change_retention_days * 24 * 3600)

        # Keep changes within retention period
        self.organizational_changes = {
            change_id: change
            for change_id, change in self.organizational_changes.items()
            if change.start_date > cutoff_time
        }

    def _analyze_cultural_patterns(self) -> List[Dict[str, Any]]:
        """Analyze cultural patterns from observations"""
        patterns = []

        # Communication pattern analysis
        comm_observations = [
            obs
            for obs in self.cultural_observations
            if "communication" in obs.get("type", "")
        ]
        if len(comm_observations) > 3:
            patterns.append(
                {
                    "pattern_type": "communication",
                    "observation": f"Organization shows {self.organizational_profile['communication_style']} communication patterns",
                    "evidence_count": len(comm_observations),
                    "confidence": min(1.0, len(comm_observations) / 10.0),
                }
            )

        # Change tolerance analysis
        change_observations = [
            obs
            for obs in self.cultural_observations
            if obs.get("type") == "organizational_change"
        ]
        if change_observations:
            avg_resistance = sum(
                len(change.resistance_factors)
                for change in self.organizational_changes.values()
            ) / max(len(self.organizational_changes), 1)
            if avg_resistance > 3:
                patterns.append(
                    {
                        "pattern_type": "change_resistance",
                        "observation": "Organization shows higher resistance to change",
                        "resistance_level": avg_resistance,
                        "recommendation": "Consider gradual change implementation and strong communication",
                    }
                )

        # Decision making pattern
        if self.team_structures:
            decision_styles = [
                team.decision_making_style for team in self.team_structures.values()
            ]
            most_common_style = (
                max(set(decision_styles), key=decision_styles.count)
                if decision_styles
                else "collaborative"
            )
            patterns.append(
                {
                    "pattern_type": "decision_making",
                    "observation": f"Predominant decision-making style: {most_common_style}",
                    "confidence": decision_styles.count(most_common_style)
                    / len(decision_styles),
                }
            )

        return patterns

    def _analyze_team_dynamics(self) -> Dict[str, Any]:
        """Analyze team dynamics and collaboration patterns"""
        if not self.team_structures:
            return {"status": "no_team_data"}

        total_teams = len(self.team_structures)
        avg_team_size = (
            sum(team.size for team in self.team_structures.values()) / total_teams
        )

        # Collaboration pattern analysis
        collaboration_patterns = []
        for team in self.team_structures.values():
            collaboration_patterns.extend(team.collaboration_patterns)

        pattern_frequency = {}
        for pattern in collaboration_patterns:
            pattern_frequency[pattern] = pattern_frequency.get(pattern, 0) + 1

        top_patterns = sorted(
            pattern_frequency.items(), key=lambda x: x[1], reverse=True
        )[:5]

        # Communication frequency analysis
        comm_frequencies = [
            team.communication_frequency for team in self.team_structures.values()
        ]
        most_common_freq = (
            max(set(comm_frequencies), key=comm_frequencies.count)
            if comm_frequencies
            else "weekly"
        )

        return {
            "total_teams": total_teams,
            "average_team_size": avg_team_size,
            "top_collaboration_patterns": top_patterns,
            "most_common_communication_frequency": most_common_freq,
            "team_distribution": self._get_team_distribution(),
            "performance_metrics": self._aggregate_team_performance(),
        }

    def _analyze_change_patterns(self) -> Dict[str, Any]:
        """Analyze organizational change patterns and effectiveness"""
        if not self.organizational_changes:
            return {"status": "no_change_data"}

        changes = list(self.organizational_changes.values())

        # Change type distribution
        change_types = {}
        for change in changes:
            change_types[change.change_type] = (
                change_types.get(change.change_type, 0) + 1
            )

        # Average effectiveness by type
        type_effectiveness = {}
        for change_type in change_types:
            type_changes = [c for c in changes if c.change_type == change_type]
            avg_effectiveness = sum(c.effectiveness_score for c in type_changes) / len(
                type_changes
            )
            type_effectiveness[change_type] = avg_effectiveness

        # Common resistance factors
        all_resistance = []
        for change in changes:
            all_resistance.extend(change.resistance_factors)

        resistance_frequency = {}
        for factor in all_resistance:
            resistance_frequency[factor] = resistance_frequency.get(factor, 0) + 1

        top_resistance = sorted(
            resistance_frequency.items(), key=lambda x: x[1], reverse=True
        )[:5]

        # Success patterns
        successful_changes = [c for c in changes if c.effectiveness_score > 0.7]
        common_success_factors = []
        for change in successful_changes:
            common_success_factors.extend(change.success_factors)

        success_frequency = {}
        for factor in common_success_factors:
            success_frequency[factor] = success_frequency.get(factor, 0) + 1

        top_success = sorted(
            success_frequency.items(), key=lambda x: x[1], reverse=True
        )[:5]

        return {
            "total_changes": len(changes),
            "change_type_distribution": change_types,
            "effectiveness_by_type": type_effectiveness,
            "average_effectiveness": sum(c.effectiveness_score for c in changes)
            / len(changes),
            "top_resistance_factors": top_resistance,
            "top_success_factors": top_success,
            "successful_changes_count": len(successful_changes),
        }

    def _get_relevant_knowledge(self) -> List[Dict[str, Any]]:
        """Get relevant institutional knowledge artifacts"""
        # Sort by importance and recent access
        sorted_artifacts = sorted(
            self.knowledge_artifacts,
            key=lambda x: (x["importance_level"] == "high", x["last_accessed"]),
            reverse=True,
        )

        # Return top 10 most relevant
        return sorted_artifacts[:10]

    def _generate_organizational_recommendations(self) -> List[Dict[str, Any]]:
        """Generate organizational improvement recommendations"""
        recommendations = []

        # Team size recommendations
        if self.team_structures:
            avg_size = sum(team.size for team in self.team_structures.values()) / len(
                self.team_structures
            )
            if avg_size > 10:
                recommendations.append(
                    {
                        "type": "team_size",
                        "priority": "medium",
                        "message": f"Average team size ({avg_size:.1f}) may be too large for optimal collaboration",
                        "action": "Consider splitting larger teams or improving coordination mechanisms",
                    }
                )

        # Change effectiveness recommendations
        if self.organizational_changes:
            avg_effectiveness = sum(
                c.effectiveness_score for c in self.organizational_changes.values()
            ) / len(self.organizational_changes)
            if avg_effectiveness < 0.6:
                recommendations.append(
                    {
                        "type": "change_effectiveness",
                        "priority": "high",
                        "message": f"Organizational change effectiveness below target ({avg_effectiveness:.2f})",
                        "action": "Review change management processes and stakeholder engagement",
                    }
                )

        # Cultural alignment recommendations
        if (
            self.organizational_profile["change_tolerance"] == "low"
            and len(self.organizational_changes) > 3
        ):
            recommendations.append(
                {
                    "type": "cultural_alignment",
                    "priority": "high",
                    "message": "High change frequency with low change tolerance may create resistance",
                    "action": "Focus on change communication and gradual implementation",
                }
            )

        return recommendations

    def _get_team_distribution(self) -> Dict[str, int]:
        """Get team distribution by type"""
        distribution = {}
        for team in self.team_structures.values():
            team_type = team.team_type
            distribution[team_type] = distribution.get(team_type, 0) + 1
        return distribution

    def _aggregate_team_performance(self) -> Dict[str, float]:
        """Aggregate team performance metrics"""
        all_metrics = {}
        metric_counts = {}

        for team in self.team_structures.values():
            for metric, value in team.performance_metrics.items():
                if metric not in all_metrics:
                    all_metrics[metric] = 0
                    metric_counts[metric] = 0
                all_metrics[metric] += value
                metric_counts[metric] += 1

        # Calculate averages
        avg_metrics = {}
        for metric, total in all_metrics.items():
            avg_metrics[metric] = total / metric_counts[metric]

        return avg_metrics

    def _calculate_organizational_health(self) -> Dict[str, Any]:
        """Calculate overall organizational health metrics"""
        health_score = 0.5  # Base score

        # Team health contribution
        if self.team_structures:
            avg_team_performance = sum(
                sum(team.performance_metrics.values())
                / max(len(team.performance_metrics), 1)
                for team in self.team_structures.values()
            ) / len(self.team_structures)
            health_score += avg_team_performance * 0.3

        # Change effectiveness contribution
        if self.organizational_changes:
            avg_change_effectiveness = sum(
                c.effectiveness_score for c in self.organizational_changes.values()
            ) / len(self.organizational_changes)
            health_score += avg_change_effectiveness * 0.3

        # Cultural alignment contribution (simplified)
        cultural_alignment = (
            0.7  # Placeholder - would be calculated from cultural observations
        )
        health_score += cultural_alignment * 0.2

        health_score = min(1.0, health_score)

        return {
            "overall_health_score": health_score,
            "team_health_contribution": (
                avg_team_performance if self.team_structures else 0.0
            ),
            "change_effectiveness_contribution": (
                avg_change_effectiveness if self.organizational_changes else 0.0
            ),
            "cultural_alignment_score": cultural_alignment,
            "health_status": (
                "healthy"
                if health_score > 0.7
                else "needs_attention" if health_score > 0.5 else "at_risk"
            ),
        }

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        import json

        profile_size = len(json.dumps(self.organizational_profile).encode("utf-8"))
        teams_size = sum(
            len(json.dumps(asdict(team), default=str).encode("utf-8"))
            for team in self.team_structures.values()
        )
        changes_size = sum(
            len(json.dumps(asdict(change), default=str).encode("utf-8"))
            for change in self.organizational_changes.values()
        )
        observations_size = sum(
            len(json.dumps(obs).encode("utf-8")) for obs in self.cultural_observations
        )
        knowledge_size = sum(
            len(json.dumps(artifact).encode("utf-8"))
            for artifact in self.knowledge_artifacts
        )

        return {
            "organizational_profile_bytes": profile_size,
            "team_structures_count": len(self.team_structures),
            "organizational_changes_count": len(self.organizational_changes),
            "cultural_observations_count": len(self.cultural_observations),
            "knowledge_artifacts_count": len(self.knowledge_artifacts),
            "teams_memory_bytes": teams_size,
            "changes_memory_bytes": changes_size,
            "observations_memory_bytes": observations_size,
            "knowledge_memory_bytes": knowledge_size,
            "total_memory_bytes": profile_size
            + teams_size
            + changes_size
            + observations_size
            + knowledge_size,
            "total_memory_mb": (
                profile_size
                + teams_size
                + changes_size
                + observations_size
                + knowledge_size
            )
            / (1024 * 1024),
        }
