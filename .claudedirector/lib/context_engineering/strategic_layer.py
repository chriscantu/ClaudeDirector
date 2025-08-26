"""
Strategic Layer Memory

Initiative tracking, goal progression, and strategic decision outcomes.
Provides strategic continuity and initiative health intelligence.
"""

from typing import Dict, List, Any, Optional
import time
import logging
from dataclasses import dataclass, asdict
from enum import Enum


class InitiativeStatus(Enum):
    """Strategic initiative status tracking"""

    PLANNED = "planned"
    ACTIVE = "active"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class StrategicInitiative:
    """Strategic initiative data structure"""

    initiative_id: str
    name: str
    description: str
    status: InitiativeStatus
    start_date: float
    target_completion_date: Optional[float]
    actual_completion_date: Optional[float]
    priority: str  # high, medium, low
    stakeholders: List[str]
    dependencies: List[str]
    frameworks_applied: List[str]
    progress_percentage: float
    health_score: float
    last_updated: float
    outcomes: List[Dict[str, Any]]


class StrategicLayerMemory:
    """
    Strategic initiative tracking and decision outcome analysis

    Features:
    - Initiative lifecycle management with health scoring
    - Strategic decision pattern recognition
    - Cross-initiative dependency tracking
    - Framework effectiveness measurement
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize strategic layer with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Storage configuration
        self.max_initiatives = self.config.get("max_initiatives", 100)
        self.health_score_threshold = self.config.get("health_threshold", 0.7)

        # In-memory storage for Phase 1
        # Phase 2 will add SQLite persistent storage with health analytics
        self.initiatives: Dict[str, StrategicInitiative] = {}
        self.decision_patterns: List[Dict[str, Any]] = []

        self.logger.info("StrategicLayerMemory initialized with initiative tracking")

    def track_initiative(self, initiative_data: Dict[str, Any]) -> bool:
        """
        Track or update a strategic initiative

        Args:
            initiative_data: Initiative information dict

        Returns:
            True if tracking successful, False otherwise
        """
        try:
            initiative_id = (
                initiative_data.get("initiative_id") or f"init_{int(time.time())}"
            )

            # Create or update initiative
            if initiative_id in self.initiatives:
                # Update existing initiative
                initiative = self.initiatives[initiative_id]
                for key, value in initiative_data.items():
                    if hasattr(initiative, key) and value is not None:
                        setattr(initiative, key, value)
                initiative.last_updated = time.time()
            else:
                # Create new initiative
                initiative = StrategicInitiative(
                    initiative_id=initiative_id,
                    name=initiative_data.get("name", ""),
                    description=initiative_data.get("description", ""),
                    status=InitiativeStatus(initiative_data.get("status", "planned")),
                    start_date=initiative_data.get("start_date", time.time()),
                    target_completion_date=initiative_data.get(
                        "target_completion_date"
                    ),
                    actual_completion_date=initiative_data.get(
                        "actual_completion_date"
                    ),
                    priority=initiative_data.get("priority", "medium"),
                    stakeholders=initiative_data.get("stakeholders", []),
                    dependencies=initiative_data.get("dependencies", []),
                    frameworks_applied=initiative_data.get("frameworks_applied", []),
                    progress_percentage=initiative_data.get("progress_percentage", 0.0),
                    health_score=initiative_data.get("health_score", 0.8),
                    last_updated=time.time(),
                    outcomes=initiative_data.get("outcomes", []),
                )
                self.initiatives[initiative_id] = initiative

            # Update health score based on progress and timeline
            self._update_initiative_health(initiative_id)

            self.logger.debug(f"Tracked initiative: {initiative_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to track initiative: {e}")
            return False

    def get_initiative_context(self, session_id: str = "default") -> Dict[str, Any]:
        """
        Get relevant strategic initiative context

        Args:
            session_id: Session identifier for context

        Returns:
            Strategic context with active initiatives and patterns
        """
        try:
            # Get active initiatives
            active_initiatives = [
                asdict(init)
                for init in self.initiatives.values()
                if init.status
                in [
                    InitiativeStatus.ACTIVE,
                    InitiativeStatus.ON_TRACK,
                    InitiativeStatus.AT_RISK,
                ]
            ]

            # Get at-risk initiatives
            at_risk_initiatives = [
                asdict(init)
                for init in self.initiatives.values()
                if init.status == InitiativeStatus.AT_RISK
                or init.health_score < self.health_score_threshold
            ]

            # Get recent completions
            recent_completions = [
                asdict(init)
                for init in self.initiatives.values()
                if init.status == InitiativeStatus.COMPLETED
                and (time.time() - init.actual_completion_date)
                < (30 * 24 * 3600)  # Last 30 days
            ]

            # Calculate strategic health metrics
            total_initiatives = len(self.initiatives)
            active_count = len(active_initiatives)
            at_risk_count = len(at_risk_initiatives)
            completed_count = len(
                [
                    i
                    for i in self.initiatives.values()
                    if i.status == InitiativeStatus.COMPLETED
                ]
            )

            health_metrics = {
                "total_initiatives": total_initiatives,
                "active_initiatives": active_count,
                "at_risk_initiatives": at_risk_count,
                "completed_initiatives": completed_count,
                "average_health_score": sum(
                    i.health_score for i in self.initiatives.values()
                )
                / max(total_initiatives, 1),
                "success_rate": (
                    completed_count / max(total_initiatives, 1)
                    if total_initiatives > 0
                    else 0.0
                ),
            }

            return {
                "active_initiatives": active_initiatives[:5],  # Top 5 most relevant
                "at_risk_initiatives": at_risk_initiatives,
                "recent_completions": recent_completions,
                "health_metrics": health_metrics,
                "strategic_patterns": self._get_strategic_patterns(),
                "recommendations": self._generate_strategic_recommendations(),
            }

        except Exception as e:
            self.logger.error(f"Failed to get initiative context: {e}")
            return {"active_initiatives": [], "error": str(e)}

    def record_strategic_decision(self, decision_data: Dict[str, Any]) -> bool:
        """Record a strategic decision for pattern analysis"""
        try:
            decision_record = {
                "decision_id": f"decision_{int(time.time())}",
                "decision_type": decision_data.get("type", "unknown"),
                "context": decision_data.get("context", ""),
                "frameworks_used": decision_data.get("frameworks_used", []),
                "stakeholders_involved": decision_data.get("stakeholders", []),
                "outcome": decision_data.get("outcome", "pending"),
                "effectiveness_score": decision_data.get("effectiveness", 0.0),
                "timestamp": time.time(),
                "session_id": decision_data.get("session_id", "default"),
            }

            self.decision_patterns.append(decision_record)

            # Limit stored patterns
            if len(self.decision_patterns) > 1000:
                self.decision_patterns = self.decision_patterns[-1000:]

            return True

        except Exception as e:
            self.logger.error(f"Failed to record strategic decision: {e}")
            return False

    def _update_initiative_health(self, initiative_id: str) -> None:
        """Update initiative health score based on progress and timeline"""
        if initiative_id not in self.initiatives:
            return

        initiative = self.initiatives[initiative_id]

        # Calculate health based on multiple factors
        progress_health = initiative.progress_percentage / 100.0

        # Timeline health (on track vs behind schedule)
        timeline_health = 1.0
        if initiative.target_completion_date:
            time_elapsed = time.time() - initiative.start_date
            total_time = initiative.target_completion_date - initiative.start_date
            expected_progress = time_elapsed / total_time if total_time > 0 else 0

            if expected_progress > 0:
                timeline_health = min(
                    1.0, initiative.progress_percentage / (expected_progress * 100)
                )

        # Status health
        status_health_map = {
            InitiativeStatus.PLANNED: 0.8,
            InitiativeStatus.ACTIVE: 0.9,
            InitiativeStatus.ON_TRACK: 1.0,
            InitiativeStatus.AT_RISK: 0.5,
            InitiativeStatus.BLOCKED: 0.2,
            InitiativeStatus.COMPLETED: 1.0,
            InitiativeStatus.CANCELLED: 0.0,
        }
        status_health = status_health_map.get(initiative.status, 0.5)

        # Combined health score
        initiative.health_score = (
            progress_health * 0.4 + timeline_health * 0.4 + status_health * 0.2
        )

        # Update status based on health
        if initiative.health_score < 0.3 and initiative.status not in [
            InitiativeStatus.COMPLETED,
            InitiativeStatus.CANCELLED,
        ]:
            initiative.status = InitiativeStatus.AT_RISK
        elif (
            initiative.health_score > 0.8
            and initiative.status == InitiativeStatus.AT_RISK
        ):
            initiative.status = InitiativeStatus.ON_TRACK

    def _get_strategic_patterns(self) -> List[Dict[str, Any]]:
        """Analyze strategic decision patterns"""
        if not self.decision_patterns:
            return []

        # Analyze framework effectiveness
        framework_effectiveness = {}
        for decision in self.decision_patterns:
            for framework in decision.get("frameworks_used", []):
                if framework not in framework_effectiveness:
                    framework_effectiveness[framework] = {
                        "uses": 0,
                        "total_effectiveness": 0.0,
                    }
                framework_effectiveness[framework]["uses"] += 1
                framework_effectiveness[framework][
                    "total_effectiveness"
                ] += decision.get("effectiveness_score", 0.0)

        # Calculate average effectiveness
        for framework, data in framework_effectiveness.items():
            data["average_effectiveness"] = data["total_effectiveness"] / data["uses"]

        # Top performing frameworks
        top_frameworks = sorted(
            framework_effectiveness.items(),
            key=lambda x: x[1]["average_effectiveness"],
            reverse=True,
        )[:5]

        return [
            {
                "pattern_type": "framework_effectiveness",
                "top_frameworks": [
                    {
                        "framework": f,
                        "effectiveness": d["average_effectiveness"],
                        "usage_count": d["uses"],
                    }
                    for f, d in top_frameworks
                ],
            }
        ]

    def _generate_strategic_recommendations(self) -> List[Dict[str, Any]]:
        """Generate strategic recommendations based on patterns"""
        recommendations = []

        # At-risk initiative recommendations
        at_risk_count = len(
            [
                i
                for i in self.initiatives.values()
                if i.health_score < self.health_score_threshold
            ]
        )
        if at_risk_count > 0:
            recommendations.append(
                {
                    "type": "initiative_health",
                    "priority": "high",
                    "message": f"{at_risk_count} initiatives below health threshold ({self.health_score_threshold})",
                    "action": "Review initiative scope, resources, or timeline",
                }
            )

        # Framework usage recommendations
        if self.decision_patterns:
            recent_decisions = [
                d
                for d in self.decision_patterns
                if (time.time() - d["timestamp"]) < (7 * 24 * 3600)
            ]
            if len(recent_decisions) > 3:
                avg_effectiveness = sum(
                    d.get("effectiveness_score", 0) for d in recent_decisions
                ) / len(recent_decisions)
                if avg_effectiveness < 0.6:
                    recommendations.append(
                        {
                            "type": "decision_effectiveness",
                            "priority": "medium",
                            "message": f"Recent decision effectiveness below target ({avg_effectiveness:.2f})",
                            "action": "Consider different frameworks or additional stakeholder input",
                        }
                    )

        return recommendations

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        import json

        initiatives_size = sum(
            len(json.dumps(asdict(init), default=str).encode("utf-8"))
            for init in self.initiatives.values()
        )
        decisions_size = sum(
            len(json.dumps(decision).encode("utf-8"))
            for decision in self.decision_patterns
        )

        return {
            "total_initiatives": len(self.initiatives),
            "total_decisions": len(self.decision_patterns),
            "initiatives_memory_bytes": initiatives_size,
            "decisions_memory_bytes": decisions_size,
            "total_memory_bytes": initiatives_size + decisions_size,
            "total_memory_mb": (initiatives_size + decisions_size) / (1024 * 1024),
        }
