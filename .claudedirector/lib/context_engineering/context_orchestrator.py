"""
Context Orchestrator

Intelligent assembly and coordination of multi-layered strategic context.
Provides optimized context selection and relevance ranking.
"""

from typing import Dict, List, Any, Optional, Tuple
import time
import logging
import json
from dataclasses import dataclass


@dataclass
class ContextPriority:
    """Context priority scoring for intelligent assembly"""

    layer_name: str
    relevance_score: float
    importance_weight: float
    size_bytes: int
    retrieval_cost: float


class ContextOrchestrator:
    """
    Multi-layered context orchestration with intelligent assembly

    Features:
    - Context relevance scoring and prioritization
    - Intelligent context size management
    - Performance-optimized context assembly
    - Cross-layer coherence validation
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize context orchestrator with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.max_context_size = self.config.get(
            "max_context_size", 1024 * 1024
        )  # 1MB default
        self.relevance_threshold = self.config.get("relevance_threshold", 0.3)
        self.performance_target_ms = self.config.get("performance_target_ms", 200)

        # Layer importance weights
        self.layer_weights = self.config.get(
            "layer_weights",
            {
                "conversation": 0.20,
                "strategic": 0.25,
                "stakeholder": 0.15,
                "learning": 0.15,
                "organizational": 0.15,
                "workspace": 0.10,  # Phase 2.1: Workspace context weight
            },
        )

        # Performance tracking
        self.assembly_metrics: List[Dict[str, Any]] = []

        self.logger.info("ContextOrchestrator initialized with intelligent assembly")

    def assemble_strategic_context(
        self,
        query: str,
        conversation_context: Dict[str, Any],
        strategic_context: Dict[str, Any],
        stakeholder_context: Dict[str, Any],
        learning_context: Dict[str, Any],
        organizational_context: Dict[str, Any],
        workspace_context: Optional[Dict[str, Any]] = None,
        analytics_insights: Optional[Dict[str, Any]] = None,  # Phase 2.2 parameter
        org_learning_insights: Optional[Dict[str, Any]] = None,  # Phase 3.1 parameter
        team_dynamics_insights: Optional[Dict[str, Any]] = None,  # Phase 3.2 parameter
        max_size_bytes: int = None,
    ) -> Dict[str, Any]:
        """
        Intelligently assemble strategic context from all layers

        Args:
            query: Current user query
            conversation_context: Context from conversation layer
            strategic_context: Context from strategic layer
            stakeholder_context: Context from stakeholder layer
            learning_context: Context from learning layer
            organizational_context: Context from organizational layer
            workspace_context: Context from workspace files (Phase 2.1)
            max_size_bytes: Maximum context size limit

        Returns:
            Assembled strategic context optimized for relevance and performance
        """
        start_time = time.time()
        max_size = max_size_bytes or self.max_context_size

        try:
            # Calculate context priorities
            context_layers = {
                "conversation": conversation_context,
                "strategic": strategic_context,
                "stakeholder": stakeholder_context,
                "learning": learning_context,
                "organizational": organizational_context,
            }

            # Phase 2.1: Add workspace context if available
            if workspace_context:
                context_layers["workspace"] = workspace_context

            # Phase 2.2: Add analytics insights if available
            if analytics_insights:
                context_layers["analytics"] = analytics_insights

            # Phase 3.1: Add organizational learning insights if available
            if org_learning_insights:
                context_layers["organizational_learning"] = org_learning_insights

            # Phase 3.2: Add team dynamics insights if available
            if team_dynamics_insights:
                context_layers["team_dynamics"] = team_dynamics_insights

            priorities = self._calculate_context_priorities(query, context_layers)

            # Assemble context with size constraints
            assembled_context = self._assemble_with_constraints(
                priorities, max_size, query
            )

            # Validate cross-layer coherence
            coherence_score = self._validate_coherence(assembled_context)

            # Calculate assembly metrics
            assembly_time = time.time() - start_time
            context_size = self._calculate_context_size(assembled_context)

            # Track performance
            metrics = {
                "assembly_time_ms": assembly_time * 1000,
                "context_size_bytes": context_size,
                "layers_included": list(assembled_context.keys()),
                "coherence_score": coherence_score,
                "relevance_scores": {
                    p.layer_name: p.relevance_score for p in priorities
                },
                "query_length": len(query),
                "timestamp": time.time(),
            }
            self.assembly_metrics.append(metrics)

            # Performance warnings
            if assembly_time * 1000 > self.performance_target_ms:
                self.logger.warning(
                    f"Context assembly exceeded target ({assembly_time * 1000:.1f}ms)"
                )

            if coherence_score < 0.7:
                self.logger.warning(
                    f"Context coherence below threshold ({coherence_score:.2f})"
                )

            return {
                "strategic_context": assembled_context,
                "assembly_metrics": metrics,
                "context_quality": {
                    "coherence_score": coherence_score,
                    "relevance_distribution": {
                        p.layer_name: p.relevance_score for p in priorities
                    },
                    "size_efficiency": context_size / max_size,
                    "layer_coverage": len(assembled_context) / 5.0,  # 5 total layers
                },
                "performance_status": (
                    "optimal"
                    if assembly_time * 1000 < self.performance_target_ms
                    else "degraded"
                ),
            }

        except Exception as e:
            self.logger.error(f"Context assembly failed: {e}")
            return self._get_fallback_assembly(query)

    def _calculate_context_priorities(
        self, query: str, layer_contexts: Dict[str, Dict[str, Any]]
    ) -> List[ContextPriority]:
        """Calculate priority scores for each context layer"""
        priorities = []

        for layer_name, context in layer_contexts.items():
            # Calculate relevance score
            relevance_score = self._calculate_layer_relevance(
                query, layer_name, context
            )

            # Get layer importance weight
            importance_weight = self.layer_weights.get(layer_name, 0.1)

            # Calculate context size
            size_bytes = self._calculate_context_size(context)

            # Calculate retrieval cost (based on size and complexity)
            retrieval_cost = self._calculate_retrieval_cost(context)

            priority = ContextPriority(
                layer_name=layer_name,
                relevance_score=relevance_score,
                importance_weight=importance_weight,
                size_bytes=size_bytes,
                retrieval_cost=retrieval_cost,
            )

            priorities.append(priority)

        # Sort by combined priority score
        priorities.sort(
            key=lambda p: p.relevance_score * p.importance_weight, reverse=True
        )

        return priorities

    def _calculate_layer_relevance(
        self, query: str, layer_name: str, context: Dict[str, Any]
    ) -> float:
        """Calculate relevance score for a specific layer"""
        query_lower = query.lower()

        # Layer-specific relevance calculation
        if layer_name == "conversation":
            return self._calculate_conversation_relevance(query_lower, context)
        elif layer_name == "strategic":
            return self._calculate_strategic_relevance(query_lower, context)
        elif layer_name == "stakeholder":
            return self._calculate_stakeholder_relevance(query_lower, context)
        elif layer_name == "learning":
            return self._calculate_learning_relevance(query_lower, context)
        elif layer_name == "organizational":
            return self._calculate_organizational_relevance(query_lower, context)
        else:
            return 0.5  # Default relevance

    def _calculate_conversation_relevance(
        self, query: str, context: Dict[str, Any]
    ) -> float:
        """Calculate conversation layer relevance"""
        conversations = context.get("conversations", [])
        if not conversations:
            return 0.1

        # Check for topic overlap and recent interactions
        relevance_scores = context.get("relevance_scores", [])
        overall_relevance = context.get("overall_relevance", 0.0)

        # Boost relevance if we have strong topic matches
        if relevance_scores and max(relevance_scores) > 0.7:
            return min(1.0, overall_relevance + 0.2)

        return overall_relevance

    def _calculate_strategic_relevance(
        self, query: str, context: Dict[str, Any]
    ) -> float:
        """Calculate strategic layer relevance"""
        # Keywords that indicate strategic context
        strategic_keywords = [
            "initiative",
            "project",
            "goal",
            "strategy",
            "planning",
            "roadmap",
            "vision",
            "mission",
            "objective",
            "milestone",
        ]

        keyword_matches = sum(1 for keyword in strategic_keywords if keyword in query)
        base_relevance = min(1.0, keyword_matches / 3.0)

        # Boost if we have active initiatives
        active_initiatives = context.get("active_initiatives", [])
        if active_initiatives:
            base_relevance += 0.2

        # Boost if we have at-risk initiatives (high importance)
        at_risk_initiatives = context.get("at_risk_initiatives", [])
        if at_risk_initiatives:
            base_relevance += 0.3

        return min(1.0, base_relevance)

    def _calculate_stakeholder_relevance(
        self, query: str, context: Dict[str, Any]
    ) -> float:
        """Calculate stakeholder layer relevance"""
        # Keywords that indicate stakeholder context
        stakeholder_keywords = [
            "team",
            "stakeholder",
            "communication",
            "collaboration",
            "relationship",
            "meeting",
            "discussion",
            "alignment",
        ]

        keyword_matches = sum(1 for keyword in stakeholder_keywords if keyword in query)
        base_relevance = min(1.0, keyword_matches / 3.0)

        # Boost if we have relevant stakeholder profiles
        relevant_stakeholders = context.get("relevant_stakeholders", [])
        if relevant_stakeholders:
            base_relevance += 0.3

        # Boost if we have relationship insights
        relationship_insights = context.get("relationship_insights", [])
        if relationship_insights:
            base_relevance += 0.2

        return min(1.0, base_relevance)

    def _calculate_learning_relevance(
        self, query: str, context: Dict[str, Any]
    ) -> float:
        """Calculate learning layer relevance"""
        # Keywords that indicate learning context
        learning_keywords = [
            "framework",
            "approach",
            "method",
            "pattern",
            "learning",
            "improvement",
            "optimization",
            "best practice",
            "lesson",
        ]

        keyword_matches = sum(1 for keyword in learning_keywords if keyword in query)
        base_relevance = min(1.0, keyword_matches / 3.0)

        # Boost if we have framework recommendations
        top_frameworks = context.get("top_performing_frameworks", [])
        if top_frameworks:
            base_relevance += 0.2

        # Boost if we have improvement opportunities
        improvements = context.get("improvement_opportunities", [])
        if improvements:
            base_relevance += 0.3

        return min(1.0, base_relevance)

    def _calculate_organizational_relevance(
        self, query: str, context: Dict[str, Any]
    ) -> float:
        """Calculate organizational layer relevance"""
        # Keywords that indicate organizational context
        org_keywords = [
            "organization",
            "culture",
            "process",
            "structure",
            "change",
            "transformation",
            "team",
            "company",
            "organizational",
        ]

        keyword_matches = sum(1 for keyword in org_keywords if keyword in query)
        base_relevance = min(1.0, keyword_matches / 3.0)

        # Boost if we have cultural insights
        cultural_insights = context.get("cultural_insights", [])
        if cultural_insights:
            base_relevance += 0.2

        # Boost if we have organizational recommendations
        org_recommendations = context.get("organizational_recommendations", [])
        if org_recommendations:
            base_relevance += 0.3

        return min(1.0, base_relevance)

    def _calculate_retrieval_cost(self, context: Dict[str, Any]) -> float:
        """Calculate retrieval cost based on context complexity"""
        size = self._calculate_context_size(context)

        # Cost factors: size, nesting depth, array lengths
        base_cost = size / 1024  # Cost per KB

        # Add complexity cost
        complexity_cost = self._calculate_complexity_cost(context)

        return base_cost + complexity_cost

    def _calculate_complexity_cost(self, context: Dict[str, Any]) -> float:
        """Calculate complexity cost based on context structure"""
        complexity = 0.0

        def count_complexity(obj, depth=0):
            nonlocal complexity
            if depth > 10:  # Prevent infinite recursion
                return

            if isinstance(obj, dict):
                complexity += len(obj) * 0.1
                for value in obj.values():
                    count_complexity(value, depth + 1)
            elif isinstance(obj, list):
                complexity += len(obj) * 0.05
                for item in obj:
                    count_complexity(item, depth + 1)

        count_complexity(context)
        return min(complexity, 10.0)  # Cap complexity cost

    def _assemble_with_constraints(
        self, priorities: List[ContextPriority], max_size: int, query: str
    ) -> Dict[str, Any]:
        """Assemble context with size and relevance constraints"""
        assembled = {}
        current_size = 0

        # Add layers in priority order while respecting size constraints
        for priority in priorities:
            # Skip if relevance is too low
            if priority.relevance_score < self.relevance_threshold:
                continue

            # Check if adding this layer would exceed size limit
            if current_size + priority.size_bytes > max_size:
                # Try to include a summary or subset
                layer_context = self._get_layer_summary(
                    priority.layer_name, priority, max_size - current_size
                )
                if layer_context:
                    assembled[priority.layer_name] = layer_context
                    current_size += self._calculate_context_size(layer_context)
                break
            else:
                # Include full layer context
                # Note: We need to get the actual context data here
                # For now, we'll include a placeholder
                assembled[priority.layer_name] = {
                    "relevance_score": priority.relevance_score,
                    "importance_weight": priority.importance_weight,
                    "included": "full_context",
                }
                current_size += priority.size_bytes

        return assembled

    def _get_layer_summary(
        self, layer_name: str, priority: ContextPriority, available_bytes: int
    ) -> Optional[Dict[str, Any]]:
        """Get summarized version of layer context that fits in available space"""
        if available_bytes < 100:  # Minimum viable context
            return None

        # Create a summary that fits in available space
        summary = {
            "layer": layer_name,
            "relevance_score": priority.relevance_score,
            "summary": f"Summarized {layer_name} context (space constrained)",
            "size_constraint": available_bytes,
        }

        return summary

    def _validate_coherence(self, assembled_context: Dict[str, Any]) -> float:
        """Validate cross-layer coherence of assembled context"""
        if len(assembled_context) < 2:
            return 1.0  # Single layer is always coherent

        # Simple coherence calculation based on layer compatibility
        coherence_score = 1.0

        # Check for contradictory information (simplified)
        layers = list(assembled_context.keys())

        # Penalize if we have stakeholder context but no strategic context
        if "stakeholder" in layers and "strategic" not in layers:
            coherence_score -= 0.1

        # Penalize if we have learning context but no conversation context
        if "learning" in layers and "conversation" not in layers:
            coherence_score -= 0.1

        # Reward balanced layer representation
        layer_balance = len(layers) / 5.0  # 5 total layers
        coherence_score += layer_balance * 0.2

        return max(0.0, min(1.0, coherence_score))

    def _calculate_context_size(self, context: Dict[str, Any]) -> int:
        """Calculate context size in bytes"""
        try:
            return len(json.dumps(context, default=str).encode("utf-8"))
        except Exception:
            return 1024  # Default estimate

    def _get_fallback_assembly(self, query: str) -> Dict[str, Any]:
        """Provide fallback context assembly in case of errors"""
        return {
            "strategic_context": {
                "status": "fallback",
                "query": query,
                "message": "Using fallback context due to assembly error",
            },
            "assembly_metrics": {
                "assembly_time_ms": 1.0,
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
        }

    def get_orchestration_metrics(self) -> Dict[str, Any]:
        """Get orchestration performance metrics"""
        if not self.assembly_metrics:
            return {"status": "no_metrics"}

        recent_metrics = self.assembly_metrics[-100:]  # Last 100 assemblies

        avg_assembly_time = sum(m["assembly_time_ms"] for m in recent_metrics) / len(
            recent_metrics
        )
        avg_context_size = sum(m["context_size_bytes"] for m in recent_metrics) / len(
            recent_metrics
        )
        avg_coherence = sum(m["coherence_score"] for m in recent_metrics) / len(
            recent_metrics
        )

        # Layer inclusion frequency
        layer_frequency = {}
        for metrics in recent_metrics:
            for layer in metrics["layers_included"]:
                layer_frequency[layer] = layer_frequency.get(layer, 0) + 1

        return {
            "performance_summary": {
                "average_assembly_time_ms": avg_assembly_time,
                "average_context_size_bytes": avg_context_size,
                "average_coherence_score": avg_coherence,
                "total_assemblies": len(self.assembly_metrics),
                "recent_assemblies_analyzed": len(recent_metrics),
            },
            "targets": {
                "assembly_time_target_ms": self.performance_target_ms,
                "max_context_size_bytes": self.max_context_size,
                "coherence_target": 0.7,
                "relevance_threshold": self.relevance_threshold,
            },
            "compliance": {
                "assembly_time_compliant": avg_assembly_time
                < self.performance_target_ms,
                "context_size_compliant": avg_context_size < self.max_context_size,
                "coherence_compliant": avg_coherence > 0.7,
            },
            "layer_usage_frequency": layer_frequency,
            "optimization_suggestions": self._generate_optimization_suggestions(
                recent_metrics
            ),
        }

    def _generate_optimization_suggestions(
        self, metrics: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate optimization suggestions based on performance metrics"""
        suggestions = []

        avg_assembly_time = sum(m["assembly_time_ms"] for m in metrics) / len(metrics)

        if avg_assembly_time > self.performance_target_ms:
            suggestions.append(
                {
                    "type": "performance",
                    "issue": f"Assembly time ({avg_assembly_time:.1f}ms) exceeds target ({self.performance_target_ms}ms)",
                    "suggestion": "Consider increasing relevance threshold or reducing layer weights",
                }
            )

        # Check layer balance
        layer_counts = {}
        for m in metrics:
            for layer in m["layers_included"]:
                layer_counts[layer] = layer_counts.get(layer, 0) + 1

        total_assemblies = len(metrics)
        underused_layers = [
            layer
            for layer, count in layer_counts.items()
            if count / total_assemblies < 0.3
        ]

        if underused_layers:
            suggestions.append(
                {
                    "type": "layer_balance",
                    "issue": f"Layers {underused_layers} are underutilized",
                    "suggestion": "Review layer weights or relevance calculation for underused layers",
                }
            )

        return suggestions

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        metrics_size = sum(
            len(json.dumps(metric).encode("utf-8")) for metric in self.assembly_metrics
        )
        config_size = len(json.dumps(self.config).encode("utf-8"))

        return {
            "assembly_metrics_count": len(self.assembly_metrics),
            "metrics_memory_bytes": metrics_size,
            "config_memory_bytes": config_size,
            "total_memory_bytes": metrics_size + config_size,
            "total_memory_mb": (metrics_size + config_size) / (1024 * 1024),
        }
