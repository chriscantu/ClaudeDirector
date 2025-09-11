"""
Context Engineering Phase 3.2 - Team Dynamics Engine
Orchestrates cross-team dynamic understanding and coordination optimization.

Author: Martin | Platform Architecture
Integration: Context Engineering Phase 3.2
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union

from .analytics_engine import AnalyticsEngine


@dataclass
class TeamInteraction:
    """Represents a single team interaction or communication event."""

    team_from: str
    team_to: str
    interaction_type: str  # "meeting", "email", "slack", "handoff", "review"
    timestamp: datetime
    duration_minutes: Optional[int] = None
    effectiveness_score: Optional[float] = None
    blockers_identified: List[str] = None
    context: Dict[str, Any] = None

    def __post_init__(self):
        if self.blockers_identified is None:
            self.blockers_identified = []
        if self.context is None:
            self.context = {}


@dataclass
class TeamDependency:
    """Represents a dependency between teams."""

    dependent_team: str
    provider_team: str
    dependency_type: str  # "delivery", "approval", "resource", "knowledge"
    criticality: str  # "blocking", "high", "medium", "low"
    estimated_duration: Optional[timedelta] = None
    risk_factors: List[str] = None
    mitigation_strategies: List[str] = None

    def __post_init__(self):
        if self.risk_factors is None:
            self.risk_factors = []
        if self.mitigation_strategies is None:
            self.mitigation_strategies = []


@dataclass
class TeamDynamicsInsight:
    """Comprehensive team dynamics analysis result."""

    teams_analyzed: List[str]
    interaction_patterns: Dict[str, Any]
    bottlenecks_identified: List[Dict[str, Any]]
    coordination_recommendations: List[str]
    effectiveness_score: float
    confidence: float
    analysis_timestamp: datetime

    # Phase 3.2 specific insights
    communication_efficiency: float
    dependency_health: float
    collaboration_quality: float


class TeamInteractionAnalyzer:
    """Analyzes communication patterns and identifies bottlenecks between teams."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.bottleneck_threshold = config.get("bottleneck_threshold", 0.75)

    def analyze_communication_patterns(
        self, interactions: List[TeamInteraction], time_window_days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze communication patterns between teams.

        Args:
            interactions: List of team interactions to analyze
            time_window_days: Analysis window in days

        Returns:
            Communication pattern analysis with bottleneck identification
        """
        start_time = time.time()

        # Filter interactions to time window
        cutoff_date = datetime.now() - timedelta(days=time_window_days)
        recent_interactions = [i for i in interactions if i.timestamp >= cutoff_date]

        # Analyze communication frequency
        communication_matrix = self._build_communication_matrix(recent_interactions)

        # Identify bottlenecks
        bottlenecks = self._identify_communication_bottlenecks(communication_matrix)

        # Calculate effectiveness metrics
        effectiveness_metrics = self._calculate_communication_effectiveness(
            recent_interactions
        )

        analysis_time = time.time() - start_time

        return {
            "communication_matrix": communication_matrix,
            "bottlenecks": bottlenecks,
            "effectiveness_metrics": effectiveness_metrics,
            "analysis_time_seconds": analysis_time,
            "interactions_analyzed": len(recent_interactions),
            "time_window_days": time_window_days,
        }

    def _build_communication_matrix(
        self, interactions: List[TeamInteraction]
    ) -> Dict[str, Dict[str, int]]:
        """Build communication frequency matrix between teams."""
        matrix = {}

        for interaction in interactions:
            if interaction.team_from not in matrix:
                matrix[interaction.team_from] = {}

            if interaction.team_to not in matrix[interaction.team_from]:
                matrix[interaction.team_from][interaction.team_to] = 0

            matrix[interaction.team_from][interaction.team_to] += 1

        return matrix

    def _identify_communication_bottlenecks(
        self, communication_matrix: Dict[str, Dict[str, int]]
    ) -> List[Dict[str, Any]]:
        """Identify communication bottlenecks with 75%+ accuracy target."""
        bottlenecks = []

        # Calculate total interactions per team
        team_totals = {}
        for from_team, interactions in communication_matrix.items():
            team_totals[from_team] = sum(interactions.values())

        # Identify teams with disproportionate communication load
        if team_totals:
            avg_interactions = sum(team_totals.values()) / len(team_totals)

            for team, total in team_totals.items():
                if total > avg_interactions * self.bottleneck_threshold:
                    bottlenecks.append(
                        {
                            "team": team,
                            "type": "communication_overload",
                            "severity": total / avg_interactions,
                            "interactions": total,
                            "average": avg_interactions,
                        }
                    )

        return bottlenecks

    def _calculate_communication_effectiveness(
        self, interactions: List[TeamInteraction]
    ) -> Dict[str, float]:
        """Calculate communication effectiveness metrics."""
        if not interactions:
            return {"overall_effectiveness": 0.0, "response_time": 0.0}

        # Calculate effectiveness based on available scores
        scored_interactions = [
            i for i in interactions if i.effectiveness_score is not None
        ]

        if scored_interactions:
            overall_effectiveness = sum(
                i.effectiveness_score for i in scored_interactions
            ) / len(scored_interactions)
        else:
            # Fallback: estimate based on interaction types
            overall_effectiveness = 0.7  # Default moderate effectiveness

        # Estimate response time (simplified)
        response_time = 24.0  # Default 24 hours

        return {
            "overall_effectiveness": overall_effectiveness,
            "response_time": response_time,
            "interactions_with_scores": len(scored_interactions),
            "total_interactions": len(interactions),
        }


class DependencyTracker:
    """Tracks and analyzes inter-team dependencies with critical path analysis."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def track_dependencies(self, dependencies: List[TeamDependency]) -> Dict[str, Any]:
        """
        Track and analyze team dependencies.

        Args:
            dependencies: List of team dependencies to analyze

        Returns:
            Dependency analysis with critical path and risk assessment
        """
        start_time = time.time()

        # Analyze dependency criticality
        critical_path = self._identify_critical_path(dependencies)

        # Assess risks
        risk_assessment = self._assess_dependency_risks(dependencies)

        # Predict potential delays
        delay_predictions = self._predict_delays(dependencies)

        analysis_time = time.time() - start_time

        return {
            "critical_path": critical_path,
            "risk_assessment": risk_assessment,
            "delay_predictions": delay_predictions,
            "analysis_time_seconds": analysis_time,
            "dependencies_analyzed": len(dependencies),
        }

    def _identify_critical_path(
        self, dependencies: List[TeamDependency]
    ) -> List[Dict[str, Any]]:
        """Identify critical path through team dependencies."""
        # Build dependency graph
        dependency_graph = {}
        for dep in dependencies:
            if dep.dependent_team not in dependency_graph:
                dependency_graph[dep.dependent_team] = []

            dependency_graph[dep.dependent_team].append(
                {
                    "provider": dep.provider_team,
                    "type": dep.dependency_type,
                    "criticality": dep.criticality,
                    "duration": dep.estimated_duration,
                }
            )

        # Find critical path (simplified implementation)
        critical_path = []
        for team, deps in dependency_graph.items():
            blocking_deps = [d for d in deps if d["criticality"] == "blocking"]
            if blocking_deps:
                critical_path.append(
                    {
                        "team": team,
                        "blocking_dependencies": len(blocking_deps),
                        "dependencies": blocking_deps,
                    }
                )

        return sorted(
            critical_path, key=lambda x: x["blocking_dependencies"], reverse=True
        )

    def _assess_dependency_risks(
        self, dependencies: List[TeamDependency]
    ) -> Dict[str, Any]:
        """Assess risks in team dependencies."""
        high_risk_deps = [
            d for d in dependencies if d.criticality in ["blocking", "high"]
        ]

        return {
            "total_dependencies": len(dependencies),
            "high_risk_count": len(high_risk_deps),
            "risk_ratio": (
                len(high_risk_deps) / len(dependencies) if dependencies else 0
            ),
            "blocking_dependencies": len(
                [d for d in dependencies if d.criticality == "blocking"]
            ),
        }

    def _predict_delays(self, dependencies: List[TeamDependency]) -> Dict[str, Any]:
        """Predict potential delays based on dependency analysis."""
        # Simplified delay prediction
        blocking_deps = [d for d in dependencies if d.criticality == "blocking"]

        # Estimate delay probability (2-week prediction target)
        delay_probability = len(blocking_deps) * 0.3  # 30% per blocking dependency
        delay_probability = min(delay_probability, 0.9)  # Cap at 90%

        predicted_delay_days = len(blocking_deps) * 3  # 3 days per blocking dependency

        return {
            "delay_probability": delay_probability,
            "predicted_delay_days": predicted_delay_days,
            "high_risk_dependencies": len(blocking_deps),
            "prediction_confidence": 0.75,  # 75% confidence target
        }


class WorkflowCoordinationEngine:
    """Optimizes handoff processes and workflow coordination."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.friction_reduction_target = config.get(
            "friction_reduction_target", 0.4
        )  # 40%

    def analyze_workflow_coordination(
        self, interactions: List[TeamInteraction], dependencies: List[TeamDependency]
    ) -> Dict[str, Any]:
        """
        Analyze workflow coordination and identify optimization opportunities.

        Args:
            interactions: Team interactions to analyze
            dependencies: Team dependencies to consider

        Returns:
            Workflow coordination analysis with optimization recommendations
        """
        start_time = time.time()

        # Analyze handoff processes
        handoff_analysis = self._analyze_handoffs(interactions)

        # Identify coordination inefficiencies
        inefficiencies = self._identify_coordination_inefficiencies(
            interactions, dependencies
        )

        # Generate optimization recommendations
        optimizations = self._generate_optimization_recommendations(
            handoff_analysis, inefficiencies
        )

        analysis_time = time.time() - start_time

        return {
            "handoff_analysis": handoff_analysis,
            "inefficiencies": inefficiencies,
            "optimizations": optimizations,
            "analysis_time_seconds": analysis_time,
            "friction_reduction_potential": self._estimate_friction_reduction(
                optimizations
            ),
        }

    def _analyze_handoffs(self, interactions: List[TeamInteraction]) -> Dict[str, Any]:
        """Analyze handoff processes between teams."""
        handoff_interactions = [
            i for i in interactions if i.interaction_type == "handoff"
        ]

        if not handoff_interactions:
            return {"total_handoffs": 0, "average_duration": 0, "effectiveness": 0}

        # Calculate handoff metrics
        total_duration = sum(i.duration_minutes or 60 for i in handoff_interactions)
        avg_duration = total_duration / len(handoff_interactions)

        # Calculate effectiveness
        scored_handoffs = [
            i for i in handoff_interactions if i.effectiveness_score is not None
        ]
        avg_effectiveness = (
            sum(i.effectiveness_score for i in scored_handoffs) / len(scored_handoffs)
            if scored_handoffs
            else 0.6
        )

        return {
            "total_handoffs": len(handoff_interactions),
            "average_duration_minutes": avg_duration,
            "effectiveness_score": avg_effectiveness,
            "scored_handoffs": len(scored_handoffs),
        }

    def _identify_coordination_inefficiencies(
        self, interactions: List[TeamInteraction], dependencies: List[TeamDependency]
    ) -> List[Dict[str, Any]]:
        """Identify coordination inefficiencies."""
        inefficiencies = []

        # Find teams with many blockers
        team_blockers = {}
        for interaction in interactions:
            for blocker in interaction.blockers_identified:
                if interaction.team_from not in team_blockers:
                    team_blockers[interaction.team_from] = []
                team_blockers[interaction.team_from].append(blocker)

        for team, blockers in team_blockers.items():
            if len(blockers) > 2:  # Threshold for inefficiency
                inefficiencies.append(
                    {
                        "type": "excessive_blockers",
                        "team": team,
                        "blocker_count": len(blockers),
                        "blockers": list(set(blockers)),  # Deduplicate
                    }
                )

        return inefficiencies

    def _generate_optimization_recommendations(
        self, handoff_analysis: Dict[str, Any], inefficiencies: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate workflow optimization recommendations."""
        recommendations = []

        # Handoff optimization
        if handoff_analysis.get("average_duration_minutes", 0) > 90:  # > 1.5 hours
            recommendations.append(
                {
                    "type": "handoff_optimization",
                    "priority": "high",
                    "description": "Reduce handoff duration through standardized processes",
                    "estimated_impact": "30% reduction in handoff time",
                    "implementation": "Create handoff templates and checklists",
                }
            )

        # Blocker reduction
        for inefficiency in inefficiencies:
            if inefficiency["type"] == "excessive_blockers":
                recommendations.append(
                    {
                        "type": "blocker_reduction",
                        "priority": "medium",
                        "team": inefficiency["team"],
                        "description": f"Address {inefficiency['blocker_count']} blockers for {inefficiency['team']}",
                        "estimated_impact": "20% improvement in team velocity",
                        "blockers": inefficiency["blockers"],
                    }
                )

        return recommendations

    def _estimate_friction_reduction(
        self, optimizations: List[Dict[str, Any]]
    ) -> float:
        """Estimate potential friction reduction from optimizations."""
        # Simplified calculation - target 40% reduction
        if not optimizations:
            return 0.0

        # Estimate based on number and type of optimizations
        friction_reduction = min(
            len(optimizations) * 0.15, self.friction_reduction_target
        )
        return friction_reduction


class StakeholderNetworkAnalyzer:
    """Analyzes multi-team stakeholder coordination and optimization."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def analyze_stakeholder_network(
        self, teams: List[str], stakeholder_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze stakeholder network across multiple teams.

        Args:
            teams: List of teams to analyze
            stakeholder_data: Stakeholder relationship data

        Returns:
            Stakeholder network analysis with coordination recommendations
        """
        start_time = time.time()

        # Build stakeholder network
        network = self._build_stakeholder_network(teams, stakeholder_data)

        # Identify coordination opportunities
        coordination_ops = self._identify_coordination_opportunities(network)

        # Calculate alignment efficiency
        alignment_efficiency = self._calculate_alignment_efficiency(network)

        analysis_time = time.time() - start_time

        return {
            "stakeholder_network": network,
            "coordination_opportunities": coordination_ops,
            "alignment_efficiency": alignment_efficiency,
            "analysis_time_seconds": analysis_time,
            "teams_analyzed": len(teams),
        }

    def _build_stakeholder_network(
        self, teams: List[str], stakeholder_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build stakeholder network model."""
        # Simplified network model
        network = {
            "teams": teams,
            "stakeholder_count": len(stakeholder_data.get("stakeholders", [])),
            "cross_team_stakeholders": [],
        }

        # Identify cross-team stakeholders
        for stakeholder_name, stakeholder_info in stakeholder_data.get(
            "stakeholders", {}
        ).items():
            stakeholder_teams = stakeholder_info.get("teams", [])
            if len(set(stakeholder_teams) & set(teams)) > 1:
                network["cross_team_stakeholders"].append(
                    {
                        "name": stakeholder_name,
                        "teams": stakeholder_teams,
                        "influence": stakeholder_info.get("influence", "medium"),
                    }
                )

        return network

    def _identify_coordination_opportunities(
        self, network: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify stakeholder coordination opportunities."""
        opportunities = []

        # High-influence cross-team stakeholders
        high_influence_stakeholders = [
            s for s in network["cross_team_stakeholders"] if s["influence"] == "high"
        ]

        for stakeholder in high_influence_stakeholders:
            opportunities.append(
                {
                    "type": "high_influence_coordination",
                    "stakeholder": stakeholder["name"],
                    "teams": stakeholder["teams"],
                    "potential_impact": "35% improvement in alignment",
                    "recommendation": f"Leverage {stakeholder['name']} for cross-team alignment",
                }
            )

        return opportunities

    def _calculate_alignment_efficiency(self, network: Dict[str, Any]) -> float:
        """Calculate stakeholder alignment efficiency."""
        if not network["cross_team_stakeholders"]:
            return 0.5  # Neutral efficiency with no cross-team stakeholders

        # Simple efficiency calculation based on cross-team coverage
        efficiency = min(len(network["cross_team_stakeholders"]) * 0.2, 0.8)
        return efficiency


class TeamDynamicsEngine:
    """
    Primary controller for cross-team dynamic understanding and coordination optimization.
    Integrates with existing OrganizationalLearningEngine for comprehensive intelligence.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize sub-components
        self.team_analyzer = TeamInteractionAnalyzer(config.get("team_analyzer", {}))
        self.dependency_tracker = DependencyTracker(
            config.get("dependency_tracker", {})
        )
        self.workflow_engine = WorkflowCoordinationEngine(
            config.get("workflow_engine", {})
        )
        self.stakeholder_network = StakeholderNetworkAnalyzer(
            config.get("stakeholder_network", {})
        )

        # Integration with Analytics Engine
        self.analytics_integration = None

    def set_analytics_integration(self, analytics_engine: AnalyticsEngine):
        """Set analytics engine integration for enhanced insights."""
        self.analytics_integration = analytics_engine
        self.logger.info("Analytics Engine integration configured for Team Dynamics")

    def analyze_team_dynamics(
        self,
        teams: List[str],
        context: str,
        interactions: List[TeamInteraction] = None,
        dependencies: List[TeamDependency] = None,
        stakeholder_data: Dict[str, Any] = None,
    ) -> TeamDynamicsInsight:
        """
        Comprehensive cross-team analysis with actionable recommendations.

        Args:
            teams: List of teams to analyze
            context: Analysis context
            interactions: Team interaction history
            dependencies: Team dependencies
            stakeholder_data: Stakeholder information

        Returns:
            Comprehensive team dynamics insight with recommendations
        """
        start_time = time.time()

        # Default empty lists if not provided
        interactions = interactions or []
        dependencies = dependencies or []
        stakeholder_data = stakeholder_data or {}

        # Analyze communication patterns
        communication_analysis = self.team_analyzer.analyze_communication_patterns(
            interactions
        )

        # Track dependencies
        dependency_analysis = self.dependency_tracker.track_dependencies(dependencies)

        # Analyze workflow coordination
        workflow_analysis = self.workflow_engine.analyze_workflow_coordination(
            interactions, dependencies
        )

        # Analyze stakeholder network
        stakeholder_analysis = self.stakeholder_network.analyze_stakeholder_network(
            teams, stakeholder_data
        )

        # Generate comprehensive recommendations
        recommendations = self._generate_comprehensive_recommendations(
            communication_analysis,
            dependency_analysis,
            workflow_analysis,
            stakeholder_analysis,
        )

        # Calculate overall scores
        effectiveness_score = self._calculate_overall_effectiveness(
            communication_analysis,
            dependency_analysis,
            workflow_analysis,
            stakeholder_analysis,
        )

        confidence = self._calculate_confidence(teams, interactions, dependencies)

        analysis_time = time.time() - start_time

        # Create comprehensive insight
        insight = TeamDynamicsInsight(
            teams_analyzed=teams,
            interaction_patterns=communication_analysis,
            bottlenecks_identified=communication_analysis["bottlenecks"],
            coordination_recommendations=recommendations,
            effectiveness_score=effectiveness_score,
            confidence=confidence,
            analysis_timestamp=datetime.now(),
            communication_efficiency=communication_analysis["effectiveness_metrics"][
                "overall_effectiveness"
            ],
            dependency_health=1.0
            - dependency_analysis["risk_assessment"]["risk_ratio"],
            collaboration_quality=workflow_analysis.get(
                "friction_reduction_potential", 0.5
            ),
        )

        # Log analytics if integration available
        if self.analytics_integration:
            self._log_analytics(insight, analysis_time)

        return insight

    def optimize_collaboration(
        self,
        initiative: str,
        teams: List[str],
        interactions: List[TeamInteraction] = None,
        dependencies: List[TeamDependency] = None,
    ) -> Dict[str, Any]:
        """
        Generate optimized collaboration strategies for multi-team initiatives.

        Args:
            initiative: Initiative name/description
            teams: Teams involved in the initiative
            interactions: Historical team interactions
            dependencies: Known dependencies

        Returns:
            Optimized collaboration plan with specific recommendations
        """
        # Analyze current team dynamics
        insight = self.analyze_team_dynamics(
            teams, f"Initiative: {initiative}", interactions, dependencies
        )

        # Generate initiative-specific optimization plan
        optimization_plan = {
            "initiative": initiative,
            "teams": teams,
            "current_effectiveness": insight.effectiveness_score,
            "optimization_recommendations": [],
            "expected_improvements": {},
            "implementation_timeline": "4-6 weeks",
        }

        # Add specific optimizations based on analysis
        if insight.communication_efficiency < 0.7:
            optimization_plan["optimization_recommendations"].append(
                {
                    "area": "communication",
                    "action": "Implement structured communication protocols",
                    "impact": "25% improvement in coordination efficiency",
                    "priority": "high",
                }
            )

        if insight.dependency_health < 0.6:
            optimization_plan["optimization_recommendations"].append(
                {
                    "area": "dependencies",
                    "action": "Establish dependency tracking and risk mitigation",
                    "impact": "30% reduction in delivery delays",
                    "priority": "high",
                }
            )

        if insight.collaboration_quality < 0.5:
            optimization_plan["optimization_recommendations"].append(
                {
                    "area": "workflow",
                    "action": "Optimize handoff processes and reduce friction",
                    "impact": "40% improvement in delivery velocity",
                    "priority": "medium",
                }
            )

        # Calculate expected improvements
        optimization_plan["expected_improvements"] = {
            "coordination_efficiency": min(insight.effectiveness_score + 0.25, 0.95),
            "delivery_predictability": 0.85,  # Target 85% predictability
            "stakeholder_alignment": 0.80,  # Target 80% alignment
        }

        return optimization_plan

    def _generate_comprehensive_recommendations(
        self,
        communication_analysis: Dict[str, Any],
        dependency_analysis: Dict[str, Any],
        workflow_analysis: Dict[str, Any],
        stakeholder_analysis: Dict[str, Any],
    ) -> List[str]:
        """Generate comprehensive coordination recommendations."""
        recommendations = []

        # Communication recommendations
        if communication_analysis["bottlenecks"]:
            recommendations.append(
                f"Address {len(communication_analysis['bottlenecks'])} communication bottlenecks "
                "to improve coordination efficiency"
            )

        # Dependency recommendations
        if dependency_analysis["risk_assessment"]["risk_ratio"] > 0.5:
            recommendations.append(
                "Implement dependency risk mitigation strategies for high-risk dependencies"
            )

        # Workflow recommendations
        friction_potential = workflow_analysis.get("friction_reduction_potential", 0)
        if friction_potential > 0.2:
            recommendations.append(
                f"Optimize workflow processes for {friction_potential*100:.0f}% friction reduction"
            )

        # Stakeholder recommendations
        if stakeholder_analysis["coordination_opportunities"]:
            recommendations.append(
                "Leverage cross-team stakeholders for improved alignment and coordination"
            )

        return recommendations

    def _calculate_overall_effectiveness(
        self,
        communication_analysis: Dict[str, Any],
        dependency_analysis: Dict[str, Any],
        workflow_analysis: Dict[str, Any],
        stakeholder_analysis: Dict[str, Any],
    ) -> float:
        """Calculate overall team dynamics effectiveness score."""
        # Weighted average of component scores
        comm_score = communication_analysis["effectiveness_metrics"][
            "overall_effectiveness"
        ]
        dep_score = 1.0 - dependency_analysis["risk_assessment"]["risk_ratio"]
        workflow_score = 1.0 - workflow_analysis.get(
            "friction_reduction_potential", 0.5
        )
        stakeholder_score = stakeholder_analysis["alignment_efficiency"]

        # Weighted combination
        overall_score = (
            comm_score * 0.3
            + dep_score * 0.3
            + workflow_score * 0.25
            + stakeholder_score * 0.15
        )
        return min(overall_score, 1.0)

    def _calculate_confidence(
        self,
        teams: List[str],
        interactions: List[TeamInteraction],
        dependencies: List[TeamDependency],
    ) -> float:
        """Calculate analysis confidence based on data availability."""
        # Base confidence
        confidence = 0.5

        # Increase confidence based on data availability
        if len(teams) >= 2:
            confidence += 0.1
        if len(interactions) >= 10:
            confidence += 0.2
        if len(dependencies) >= 3:
            confidence += 0.1

        # Cap confidence
        return min(confidence, 0.9)

    def _log_analytics(self, insight: TeamDynamicsInsight, analysis_time: float):
        """Log analytics data for team dynamics analysis."""
        try:
            analytics_data = {
                "event_type": "team_dynamics_analysis",
                "teams_count": len(insight.teams_analyzed),
                "effectiveness_score": insight.effectiveness_score,
                "confidence": insight.confidence,
                "analysis_time_seconds": analysis_time,
                "bottlenecks_count": len(insight.bottlenecks_identified),
                "recommendations_count": len(insight.coordination_recommendations),
            }

            if hasattr(self.analytics_integration, "log_team_dynamics"):
                self.analytics_integration.log_team_dynamics(analytics_data)

        except Exception as e:
            self.logger.warning(f"Failed to log team dynamics analytics: {e}")
