"""
Advanced Context Engine

Five-layer strategic context with intelligent orchestration.
Core implementation for Context Engineering Priority 1.

Performance Targets:
- <3s context retrieval time
- >95% context retention across sessions
- >90% relevance accuracy
- <1GB memory footprint
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time
import logging

from .conversation_layer import ConversationLayerMemory
from .strategic_layer import StrategicLayerMemory
from .stakeholder_layer import StakeholderLayerMemory
from .learning_layer import LearningLayerMemory
from .organizational_layer import OrganizationalLayerMemory
from .context_orchestrator import ContextOrchestrator
from .workspace_integration import WorkspaceMonitor, WorkspaceContext
from .analytics_engine import AnalyticsEngine  # Phase 2.2 Analytics Integration
from .organizational_processor import (
    OrganizationalProcessor,
)  # Phase 3B Sequential Thinking: Consolidated organizational intelligence
from .team_dynamics_engine import (
    TeamDynamicsEngine,
)  # Phase 3.2 Team Dynamics


@dataclass
class ContextRetrievalMetrics:
    """Performance metrics for context retrieval operations"""

    retrieval_time_seconds: float
    context_layers_accessed: List[str]
    relevance_score: float
    total_context_size_bytes: int


class AdvancedContextEngine:
    """
    Multi-layered strategic context with intelligent assembly

    Architecture:
    - Conversation Layer: Semantic chat history with 90-day retention
    - Strategic Layer: Initiative tracking and decision outcomes
    - Stakeholder Layer: Relationship dynamics and communication preferences
    - Learning Layer: Framework mastery and skill progression
    - Organizational Layer: Structure evolution and cultural context
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Advanced Context Engine with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Initialize context layers
        self.conversation_layer = ConversationLayerMemory(
            self.config.get("conversation", {})
        )
        self.strategic_layer = StrategicLayerMemory(self.config.get("strategic", {}))
        self.stakeholder_layer = StakeholderLayerMemory(
            self.config.get("stakeholder", {})
        )
        self.learning_layer = LearningLayerMemory(self.config.get("learning", {}))
        self.organizational_layer = OrganizationalLayerMemory(
            self.config.get("organizational", {})
        )

        # Context orchestration
        self.context_orchestrator = ContextOrchestrator(
            self.config.get("orchestrator", {})
        )

        # Phase 2.2: Advanced Analytics Engine integration
        analytics_config = self.config.get("analytics", {})
        self.analytics_enabled = analytics_config.get("enabled", True)
        self.analytics_engine = None

        if self.analytics_enabled:
            try:
                self.analytics_engine = AnalyticsEngine(analytics_config)
                self.logger.info("Advanced Analytics Engine integrated successfully")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Analytics Engine: {e}")
                self.analytics_enabled = False

        # Workspace integration (Phase 2.1)
        workspace_config = self.config.get("workspace", {})
        self.workspace_monitor: Optional[WorkspaceMonitor] = None
        self.workspace_enabled = workspace_config.get("enabled", True)

        if self.workspace_enabled:
            workspace_path = workspace_config.get("path", "leadership-workspace")
            try:
                self.workspace_monitor = WorkspaceMonitor(workspace_path)
                self.workspace_monitor.start_monitoring()
                self.logger.info(f"Workspace monitoring enabled for {workspace_path}")
            except Exception as e:
                self.logger.warning(f"Failed to start workspace monitoring: {e}")
                self.workspace_enabled = False

        # Phase 3.1: Organizational Learning Engine integration
        org_learning_config = self.config.get("organizational_learning", {})
        self.org_learning_enabled = org_learning_config.get("enabled", True)
        self.org_learning_engine = None

        if self.org_learning_enabled:
            try:
                self.org_learning_engine = OrganizationalProcessor(org_learning_config)

                # TODO: Analytics integration - add to OrganizationalProcessor in future iteration
                # Skipping analytics integration for now during Sequential Thinking consolidation

                self.logger.info(
                    "Organizational Processor (Sequential Thinking) integrated successfully"
                )
            except Exception as e:
                self.logger.warning(
                    f"Failed to initialize Organizational Processor: {e}"
                )
                self.org_learning_enabled = False

        # Phase 3.2: Team Dynamics Engine integration
        team_dynamics_config = self.config.get("team_dynamics", {})
        self.team_dynamics_enabled = team_dynamics_config.get("enabled", True)
        self.team_dynamics_engine = None

        if self.team_dynamics_enabled:
            try:
                self.team_dynamics_engine = TeamDynamicsEngine(team_dynamics_config)

                # Integrate with Analytics Engine if available
                if self.analytics_enabled and self.analytics_engine:
                    self.team_dynamics_engine.set_analytics_integration(
                        self.analytics_engine
                    )

                self.logger.info("Team Dynamics Engine integrated successfully")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Team Dynamics Engine: {e}")
                self.team_dynamics_enabled = False

        # Performance tracking
        self.performance_metrics: List[ContextRetrievalMetrics] = []

        self.logger.info(
            "AdvancedContextEngine initialized with 5-layer architecture + workspace integration"
        )

    def get_contextual_intelligence(
        self,
        query: str,
        session_id: str = "default",
        max_context_size: int = 1024 * 1024,
    ) -> Dict[str, Any]:
        """
        Intelligent context assembly for strategic responses

        Args:
            query: Current user query
            session_id: Session identifier for context tracking
            max_context_size: Maximum context size in bytes

        Returns:
            Assembled strategic context with performance metrics
        """
        start_time = time.time()
        layers_accessed = []

        try:
            # Gather context from each layer
            conversation_context = self._get_conversation_context(query, session_id)
            layers_accessed.append("conversation")

            strategic_context = self._get_strategic_context(query, session_id)
            layers_accessed.append("strategic")

            stakeholder_context = self._get_stakeholder_context(query, session_id)
            layers_accessed.append("stakeholder")

            learning_context = self._get_learning_context(query, session_id)
            layers_accessed.append("learning")

            organizational_context = self._get_organizational_context(query, session_id)
            layers_accessed.append("organizational")

            # Phase 2.1: Gather workspace context
            workspace_context = self._get_workspace_context(query, session_id)
            if workspace_context:
                layers_accessed.append("workspace")

            # Phase 2.2: Generate analytics insights if enabled
            analytics_insights = None
            if self.analytics_enabled and self.analytics_engine:
                try:
                    # Extract stakeholder and initiative data for analytics
                    stakeholder_list = self._extract_stakeholders_from_context(
                        stakeholder_context, workspace_context
                    )
                    initiative_list = self._extract_initiatives_from_context(
                        strategic_context, workspace_context
                    )

                    analytics_insights = (
                        self.analytics_engine.get_strategic_recommendations(
                            context=query,
                            stakeholders=stakeholder_list,
                            initiatives=initiative_list,
                        )
                    )
                    layers_accessed.append("analytics")
                except Exception as e:
                    self.logger.warning(f"Analytics insights generation failed: {e}")

            # Phase 3.1: Generate organizational learning insights if enabled
            org_learning_insights = None
            if self.org_learning_enabled and self.org_learning_engine:
                try:
                    # Prepare stakeholder data for organizational analysis
                    stakeholder_data = {
                        "stakeholders": self._extract_stakeholders_from_context(
                            stakeholder_context, workspace_context
                        ),
                        "communication_patterns": stakeholder_context.get(
                            "communication_patterns", {}
                        ),
                        "decision_style": stakeholder_context.get(
                            "decision_style", "unknown"
                        ),
                    }

                    org_learning_insights = (
                        self.org_learning_engine.analyze_organizational_context(
                            context=query,
                            stakeholder_data=stakeholder_data,
                            strategic_context=strategic_context,
                        )
                    )
                    layers_accessed.append("organizational_learning")
                except Exception as e:
                    self.logger.warning(
                        f"Organizational learning insights generation failed: {e}"
                    )

            # Phase 3.2: Generate team dynamics insights if enabled
            team_dynamics_insights = None
            if self.team_dynamics_enabled and self.team_dynamics_engine:
                try:
                    # Extract team information from context
                    teams = self._extract_teams_from_context(
                        stakeholder_context, workspace_context, query
                    )

                    if teams and len(teams) > 1:  # Multi-team scenario
                        team_dynamics_insights = self.team_dynamics_engine.analyze_team_dynamics(
                            teams=teams,
                            context=query,
                            stakeholder_data={
                                "stakeholders": self._extract_stakeholders_from_context(
                                    stakeholder_context, workspace_context
                                )
                            },
                        )
                        layers_accessed.append("team_dynamics")
                except Exception as e:
                    self.logger.warning(
                        f"Team dynamics insights generation failed: {e}"
                    )

            # Orchestrate intelligent context assembly
            assembled_context = self.context_orchestrator.assemble_strategic_context(
                query=query,
                conversation_context=conversation_context,
                strategic_context=strategic_context,
                stakeholder_context=stakeholder_context,
                learning_context=learning_context,
                organizational_context=organizational_context,
                workspace_context=workspace_context,
                analytics_insights=analytics_insights,  # Phase 2.2 parameter
                org_learning_insights=org_learning_insights,  # Phase 3.1 parameter
                team_dynamics_insights=team_dynamics_insights,  # Phase 3.2 parameter
                max_size_bytes=max_context_size,
            )

            # Calculate performance metrics
            retrieval_time = time.time() - start_time
            context_size = self._calculate_context_size(assembled_context)
            relevance_score = self._calculate_relevance_score(query, assembled_context)

            # Track performance
            metrics = ContextRetrievalMetrics(
                retrieval_time_seconds=retrieval_time,
                context_layers_accessed=layers_accessed,
                relevance_score=relevance_score,
                total_context_size_bytes=context_size,
            )
            self.performance_metrics.append(metrics)

            # Validate performance targets
            if retrieval_time > 3.0:
                self.logger.warning(
                    f"Context retrieval exceeded 3s target: {retrieval_time:.2f}s"
                )

            if relevance_score < 0.9:
                self.logger.warning(
                    f"Context relevance below 90% target: {relevance_score:.2f}"
                )

            return {
                "context": assembled_context,
                "metrics": {
                    "retrieval_time_seconds": retrieval_time,
                    "layers_accessed": layers_accessed,
                    "relevance_score": relevance_score,
                    "context_size_bytes": context_size,
                },
                "session_id": session_id,
                "timestamp": time.time(),
            }

        except Exception as e:
            self.logger.error(f"Context retrieval failed: {e}")
            # Graceful degradation - return basic context
            return self._get_fallback_context(query, session_id)

    def store_conversation_outcome(
        self,
        session_id: str,
        query: str,
        response: str,
        frameworks_used: List[str] = None,
        strategic_decisions: List[Dict[str, Any]] = None,
    ) -> bool:
        """Store conversation outcome across relevant context layers"""
        try:
            # Store in conversation layer
            self.conversation_layer.store_conversation_context(
                {
                    "session_id": session_id,
                    "query": query,
                    "response": response,
                    "timestamp": time.time(),
                }
            )

            # Update strategic context if strategic decisions were made
            if strategic_decisions:
                for decision in strategic_decisions:
                    self.strategic_layer.track_initiative(decision)

            # Update learning context based on frameworks used
            if frameworks_used:
                for framework in frameworks_used:
                    self.learning_layer.update_framework_usage(framework, session_id)

            return True

        except Exception as e:
            self.logger.error(f"Failed to store conversation outcome: {e}")
            return False

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for monitoring and optimization"""
        if not self.performance_metrics:
            return {"status": "no_metrics", "message": "No performance data available"}

        recent_metrics = self.performance_metrics[-100:]  # Last 100 retrievals

        avg_retrieval_time = sum(
            m.retrieval_time_seconds for m in recent_metrics
        ) / len(recent_metrics)
        avg_relevance_score = sum(m.relevance_score for m in recent_metrics) / len(
            recent_metrics
        )
        avg_context_size = sum(
            m.total_context_size_bytes for m in recent_metrics
        ) / len(recent_metrics)

        return {
            "performance_summary": {
                "average_retrieval_time_seconds": avg_retrieval_time,
                "average_relevance_score": avg_relevance_score,
                "average_context_size_bytes": avg_context_size,
                "total_retrievals": len(self.performance_metrics),
                "recent_retrievals_analyzed": len(recent_metrics),
            },
            "targets": {
                "retrieval_time_target": 3.0,
                "relevance_score_target": 0.9,
                "memory_footprint_target": 1024 * 1024 * 1024,  # 1GB
            },
            "compliance": {
                "retrieval_time_compliant": avg_retrieval_time < 3.0,
                "relevance_score_compliant": avg_relevance_score > 0.9,
                "memory_footprint_compliant": avg_context_size < 1024 * 1024 * 1024,
            },
        }

    def _get_conversation_context(self, query: str, session_id: str) -> Dict[str, Any]:
        """Get relevant conversation context"""
        return self.conversation_layer.retrieve_relevant_context(query, session_id)

    def _get_strategic_context(self, query: str, session_id: str) -> Dict[str, Any]:
        """Get relevant strategic context"""
        return self.strategic_layer.get_initiative_context(session_id)

    def _get_stakeholder_context(self, query: str, session_id: str) -> Dict[str, Any]:
        """Get relevant stakeholder context"""
        return self.stakeholder_layer.get_relationship_context(query)

    def _get_learning_context(self, query: str, session_id: str) -> Dict[str, Any]:
        """Get relevant learning context"""
        return self.learning_layer.get_skill_context(session_id)

    def _get_organizational_context(
        self, query: str, session_id: str
    ) -> Dict[str, Any]:
        """Get relevant organizational context"""
        return self.organizational_layer.get_structure_context()

    def _get_workspace_context(
        self, query: str, session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get relevant workspace context from strategic documents"""
        if not self.workspace_enabled or not self.workspace_monitor:
            return None

        try:
            workspace_context = self.workspace_monitor.get_workspace_context()
            if not workspace_context:
                return None

            # Convert workspace context to strategic context format
            return {
                "active_initiatives": workspace_context.active_initiatives,
                "priority_files": workspace_context.priority_files,
                "recent_meetings": workspace_context.recent_meetings,
                "strategic_themes": workspace_context.strategic_themes,
                "stakeholder_activity": workspace_context.stakeholder_activity,
                "last_updated": workspace_context.last_updated.isoformat(),
                "context_type": "workspace",
                "relevance_indicators": self._calculate_workspace_relevance(
                    query, workspace_context
                ),
            }
        except Exception as e:
            self.logger.error(f"Error retrieving workspace context: {e}")
            return None

    def _calculate_workspace_relevance(
        self, query: str, workspace_context: WorkspaceContext
    ) -> List[str]:
        """Calculate relevance indicators for workspace context"""
        indicators = []
        query_lower = query.lower()

        # Check for initiative mentions
        for initiative in workspace_context.active_initiatives:
            if any(word in query_lower for word in initiative.lower().split()):
                indicators.append(f"initiative:{initiative}")

        # Check for strategic theme alignment
        for theme in workspace_context.strategic_themes:
            if any(word in query_lower for word in theme.lower().split()):
                indicators.append(f"theme:{theme}")

        # Check for stakeholder mentions
        for stakeholder in workspace_context.stakeholder_activity.keys():
            if stakeholder.lower() in query_lower:
                indicators.append(f"stakeholder:{stakeholder}")

        return indicators[:5]  # Limit to top 5 indicators

    def _extract_stakeholders_from_context(
        self,
        stakeholder_context: Dict[str, Any],
        workspace_context: Optional[Dict[str, Any]],
    ) -> List[str]:
        """Extract stakeholder list for analytics from context data"""
        stakeholders = []

        # Extract from stakeholder context
        if stakeholder_context and "relationships" in stakeholder_context:
            stakeholders.extend(stakeholder_context["relationships"].keys())

        # Extract from workspace context
        if workspace_context and "stakeholder_activity" in workspace_context:
            stakeholders.extend(workspace_context["stakeholder_activity"].keys())

        # Remove duplicates and return
        return list(set(stakeholders))

    def _extract_teams_from_context(
        self,
        stakeholder_context: Dict[str, Any],
        workspace_context: Optional[Dict[str, Any]],
        query: str,
    ) -> List[str]:
        """Extract team information from context and query for team dynamics analysis."""
        teams = set()

        # Common team keywords
        team_keywords = [
            "frontend",
            "backend",
            "platform",
            "design",
            "qa",
            "devops",
            "security",
            "mobile",
            "data",
            "analytics",
            "infrastructure",
            "product",
            "engineering",
            "ui",
            "ux",
            "api",
            "database",
            "testing",
            "operations",
        ]

        # Extract from query
        query_lower = query.lower()
        for keyword in team_keywords:
            if keyword in query_lower:
                teams.add(keyword.title())

        # Extract from stakeholder context
        if stakeholder_context and "teams" in stakeholder_context:
            if isinstance(stakeholder_context["teams"], list):
                teams.update(stakeholder_context["teams"])

        # Extract from workspace context
        if workspace_context and "teams" in workspace_context:
            if isinstance(workspace_context["teams"], list):
                teams.update(workspace_context["teams"])

        # Look for team mentions in stakeholder data
        if stakeholder_context and "relationships" in stakeholder_context:
            for stakeholder_info in stakeholder_context["relationships"].values():
                if isinstance(stakeholder_info, dict) and "teams" in stakeholder_info:
                    if isinstance(stakeholder_info["teams"], list):
                        teams.update(stakeholder_info["teams"])

        return list(teams)

    def _extract_initiatives_from_context(
        self,
        strategic_context: Dict[str, Any],
        workspace_context: Optional[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Extract initiative list for analytics from context data"""
        initiatives = []

        # Extract from strategic context
        if strategic_context and "initiatives" in strategic_context:
            for initiative_id, initiative_data in strategic_context[
                "initiatives"
            ].items():
                initiatives.append({"id": initiative_id, **initiative_data})

        # Extract from workspace context
        if workspace_context and "active_initiatives" in workspace_context:
            for initiative_name in workspace_context["active_initiatives"]:
                # Create basic initiative data structure
                initiatives.append(
                    {
                        "id": initiative_name,
                        "name": initiative_name,
                        "source": "workspace",
                    }
                )

        return initiatives

    def _calculate_context_size(self, context: Dict[str, Any]) -> int:
        """Calculate approximate context size in bytes"""
        import json

        return len(json.dumps(context, default=str).encode("utf-8"))

    def _calculate_relevance_score(self, query: str, context: Dict[str, Any]) -> float:
        """Calculate context relevance score (placeholder implementation)"""
        # Semantic relevance scoring implementation
        # Phase 1: Return high baseline score, Phase 2 will add ML-based scoring
        return 0.95

    def _get_fallback_context(self, query: str, session_id: str) -> Dict[str, Any]:
        """Provide fallback context in case of errors"""
        return {
            "context": {
                "strategic_context": {
                    "status": "fallback",
                    "query": query,
                    "session_id": session_id,
                    "message": "Using fallback context due to retrieval error",
                },
                "assembly_metrics": {
                    "assembly_time_ms": 0.1,
                    "context_size_bytes": 256,
                    "layers_included": ["fallback"],
                    "coherence_score": 0.5,
                    "timestamp": time.time(),
                },
                "context_quality": {
                    "coherence_score": 0.5,
                    "relevance_distribution": {"fallback": 0.5},
                    "size_efficiency": 0.0,
                    "layer_coverage": 0.2,
                },
                "performance_status": "fallback",
            },
            "metrics": {
                "retrieval_time_seconds": 0.1,
                "layers_accessed": ["fallback"],
                "relevance_score": 0.5,
                "context_size_bytes": 256,
            },
            "session_id": session_id,
            "timestamp": time.time(),
        }

    def save_session_context(self, session_id: str, context_quality_score: float = 0.0):
        """Save current context as a session snapshot for cross-session persistence"""
        try:
            if self.workspace_enabled and self.workspace_monitor:
                self.workspace_monitor.save_session_context(
                    session_id, context_quality_score
                )

            # Also save to other layers for comprehensive persistence
            self.conversation_layer.save_session_context(session_id)
            self.strategic_layer.save_session_context(session_id)

            self.logger.info(f"Session context saved for {session_id}")
        except Exception as e:
            self.logger.error(f"Error saving session context: {e}")

    def restore_session_context(self, session_id: str) -> bool:
        """Restore context from a previous session"""
        try:
            success = False

            # Restore workspace context
            if self.workspace_enabled and self.workspace_monitor:
                workspace_context = self.workspace_monitor.load_session_context(
                    session_id
                )
                if workspace_context:
                    success = True

            # Restore other layer contexts
            if hasattr(self.conversation_layer, "restore_session_context"):
                success |= self.conversation_layer.restore_session_context(session_id)

            if hasattr(self.strategic_layer, "restore_session_context"):
                success |= self.strategic_layer.restore_session_context(session_id)

            if success:
                self.logger.info(f"Session context restored for {session_id}")

            return success
        except Exception as e:
            self.logger.error(f"Error restoring session context: {e}")
            return False

    def get_workspace_status(self) -> Dict[str, Any]:
        """Get current workspace integration status"""
        if not self.workspace_enabled or not self.workspace_monitor:
            return {
                "enabled": False,
                "status": "disabled",
                "reason": "workspace monitoring not enabled",
            }

        try:
            workspace_context = self.workspace_monitor.get_workspace_context()
            strategic_files = len(self.workspace_monitor.strategic_files)

            return {
                "enabled": True,
                "status": "active",
                "workspace_path": str(self.workspace_monitor.workspace_path),
                "strategic_files_count": strategic_files,
                "active_initiatives": (
                    len(workspace_context.active_initiatives)
                    if workspace_context
                    else 0
                ),
                "last_updated": (
                    workspace_context.last_updated.isoformat()
                    if workspace_context
                    else None
                ),
                "monitoring": self.workspace_monitor.observer.is_alive(),
            }
        except Exception as e:
            return {"enabled": True, "status": "error", "error": str(e)}

    def cleanup(self):
        """Cleanup resources and stop monitoring"""
        if self.workspace_monitor:
            try:
                self.workspace_monitor.stop_monitoring()
                self.logger.info("Workspace monitoring stopped")
            except Exception as e:
                self.logger.error(f"Error stopping workspace monitoring: {e}")

        # Clear performance metrics to free memory
        self.performance_metrics.clear()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
