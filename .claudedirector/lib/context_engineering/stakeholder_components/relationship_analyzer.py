"""
Relationship Analyzer - Phase 3A.3.4 SOLID Extraction
Single Responsibility: Stakeholder relationship intelligence and interaction analysis

Extracted from StakeholderIntelligenceUnified for SOLID compliance
Author: Martin | Platform Architecture with Sequential7 methodology
"""

import re
import time
import logging
from typing import Dict, List, Any, Optional

# Import types
from ..stakeholder_intelligence_types import StakeholderProfile


class RelationshipAnalyzer:
    """
    Stakeholder relationship intelligence and interaction analysis
    
    Single Responsibility: Analyze stakeholder relationships, record interactions,
    generate insights, and calculate relationship health metrics.
    """

    def __init__(
        self, 
        repository=None,
        cache_manager=None,
        enable_performance: bool = True,
        interaction_retention_days: int = 365,
    ):
        """Initialize relationship analyzer"""
        self.logger = logging.getLogger(__name__)
        self.repository = repository
        self.cache_manager = cache_manager
        self.enable_performance = enable_performance and cache_manager is not None
        self.interaction_retention_days = interaction_retention_days
        
        # In-memory storage for interactions
        self.interactions: List[Dict[str, Any]] = []

    def record_interaction(
        self,
        stakeholder_id: str,
        interaction_type: str,
        context: Dict[str, Any],
        outcome: Optional[str] = None,
    ) -> bool:
        """
        Record stakeholder interaction with outcome tracking
        
        Args:
            stakeholder_id: ID of stakeholder involved
            interaction_type: Type of interaction (meeting, email, review, etc.)
            context: Context information about the interaction
            outcome: Outcome assessment (positive, negative, neutral)
            
        Returns:
            True if recorded successfully, False otherwise
        """
        try:
            if not self.repository:
                self.logger.error("Repository required for interaction recording")
                return False
                
            # Verify stakeholder exists
            stakeholder = self.repository.get_stakeholder(stakeholder_id)
            if not stakeholder:
                self.logger.warning(f"Cannot record interaction for unknown stakeholder: {stakeholder_id}")
                return False

            interaction = {
                "stakeholder_id": stakeholder_id,
                "type": interaction_type,
                "timestamp": time.time(),
                "context": context,
                "outcome": outcome,
                "interaction_id": f"{stakeholder_id}_{int(time.time())}_{len(self.interactions)}",
            }

            self.interactions.append(interaction)

            # Update stakeholder profile based on interaction
            self._update_stakeholder_from_interaction(stakeholder, interaction)

            # Clean up old interactions periodically
            if len(self.interactions) % 50 == 0:  # Every 50 interactions
                self._cleanup_old_interactions()

            # Cache invalidation
            if self.enable_performance:
                self.cache_manager.delete_pattern(f"relationship_*")
                self.cache_manager.delete_pattern(f"interaction_*")

            self.logger.debug(f"Recorded interaction for {stakeholder_id}: {interaction_type}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to record interaction: {e}")
            return False

    def get_relationship_context(
        self, query: str, limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get relationship context for strategic queries
        
        Args:
            query: Query text to analyze for stakeholder context
            limit: Maximum number of stakeholders to return
            
        Returns:
            Relationship context with stakeholders and insights
        """
        try:
            if not self.repository:
                return {"error": "Repository not available"}
                
            # Use caching for performance
            if self.enable_performance:
                cache_key = f"relationship_context:{hash(query)}:{limit}"
                cached_result = self.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result

            query_lower = query.lower()
            mentioned_stakeholder_ids = self._extract_stakeholder_mentions(query)

            # Get stakeholder profiles
            relevant_stakeholders = []
            for stakeholder_id in mentioned_stakeholder_ids[:limit]:
                stakeholder = self.repository.get_stakeholder(stakeholder_id)
                if stakeholder:
                    relevant_stakeholders.append(stakeholder.to_dict())

            # Generate relationship insights
            insights = self._generate_relationship_insights(query, relevant_stakeholders)

            # Get recent interactions
            recent_interactions = self._get_recent_interactions(mentioned_stakeholder_ids)

            # Generate strategic recommendations
            recommendations = self._generate_strategic_recommendations(query_lower, relevant_stakeholders)

            result = {
                "query": query,
                "stakeholders": relevant_stakeholders,
                "insights": insights,
                "recent_interactions": recent_interactions,
                "recommendations": recommendations,
                "relationship_health": self._calculate_relationship_health(),
                "timestamp": time.time(),
            }

            # Cache result
            if self.enable_performance:
                self.cache_manager.set(cache_key, result, ttl=1800)  # 30 minute cache

            return result

        except Exception as e:
            self.logger.error(f"Failed to get relationship context: {e}")
            return {"error": str(e), "stakeholders": [], "insights": []}

    def _extract_stakeholder_mentions(self, text: str) -> List[str]:
        """Extract stakeholder mentions from text"""
        if not self.repository:
            return []
            
        mentioned = []
        text_lower = text.lower()

        # Direct name mentions
        for stakeholder_id, profile in self.repository.stakeholders.items():
            name_lower = profile.name.lower()
            if name_lower in text_lower:
                mentioned.append(stakeholder_id)

        # Role-based mentions
        role_keywords = {
            "executive": ["exec", "leadership", "c-level", "director", "vp"],
            "engineering_manager": ["eng manager", "engineering lead", "team lead"],
            "product_manager": ["pm", "product", "product owner"],
            "designer": ["design", "ux", "ui"],
        }

        for role, keywords in role_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                # Find stakeholders with this role
                role_matches = [
                    stakeholder_id
                    for stakeholder_id, profile in self.repository.stakeholders.items()
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
            insights.append({
                "type": "communication_style",
                "stakeholder": stakeholder_name,
                "insight": f"Prefers {style} communication approach",
                "recommendation": self._get_style_recommendation(style),
                "priority": "medium",
            })

            # Influence level insight
            influence = profile.get("influence_level", "medium")
            if influence in ["critical", "high"]:
                insights.append({
                    "type": "influence",
                    "stakeholder": stakeholder_name,
                    "insight": f"{influence.title()} influence stakeholder - key decision maker",
                    "recommendation": "Ensure alignment and clear communication of strategic value",
                    "priority": "high",
                })

            # Platform position insight
            position = profile.get("platform_position", "unknown")
            if position == "opponent":
                insights.append({
                    "type": "platform_risk",
                    "stakeholder": stakeholder_name,
                    "insight": "Platform opponent - requires careful engagement",
                    "recommendation": "Focus on business value and address concerns directly",
                    "priority": "high",
                })
            elif position == "supporter":
                insights.append({
                    "type": "platform_opportunity",
                    "stakeholder": stakeholder_name,
                    "insight": "Platform supporter - leverage for advocacy",
                    "recommendation": "Engage for testimonials and support in decisions",
                    "priority": "medium",
                })

            # Relationship quality insight
            quality = profile.get("relationship_quality", 0.7)
            if quality < 0.5:
                insights.append({
                    "type": "relationship_risk",
                    "stakeholder": stakeholder_name,
                    "insight": f"Low relationship quality ({quality:.2f})",
                    "recommendation": "Consider relationship building activities or conflict resolution",
                    "priority": "high",
                })
            elif quality > 0.9:
                insights.append({
                    "type": "relationship_strength",
                    "stakeholder": stakeholder_name,
                    "insight": f"Strong relationship ({quality:.2f})",
                    "recommendation": "Leverage strong relationship for strategic initiatives",
                    "priority": "low",
                })

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
        if not self.repository or not self.repository.stakeholders:
            return {"status": "no_data"}

        stakeholder_list = list(self.repository.stakeholders.values())
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
            position = profile.platform_position
            platform_distribution[position] = platform_distribution.get(position, 0) + 1

        return {
            "status": "healthy" if avg_relationship_quality > 0.7 else "needs_attention",
            "total_stakeholders": total_stakeholders,
            "average_relationship_quality": avg_relationship_quality,
            "average_trust_level": avg_trust_level,
            "influence_distribution": influence_distribution,
            "platform_distribution": platform_distribution,
            "recent_interactions": len(self.interactions),
            "relationship_risks": sum(1 for s in stakeholder_list if s.relationship_quality < 0.5),
        }

    def _generate_strategic_recommendations(
        self, query_lower: str, profiles: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate strategic communication recommendations"""
        recommendations = []

        # Platform-related queries
        if any(word in query_lower for word in ["platform", "architecture", "technical"]):
            opponents = [p for p in profiles if p.get("platform_position") == "opponent"]
            if opponents:
                recommendations.append({
                    "type": "platform_opposition",
                    "priority": "high",
                    "message": f"{len(opponents)} platform opponents in stakeholder set",
                    "action": "Focus on business value, ROI, and address specific concerns with data",
                })

        # Financial decision context
        if any(word in query_lower for word in ["budget", "cost", "investment", "resource"]):
            recommendations.append({
                "type": "financial_communication",
                "priority": "medium",
                "message": "Financial decision context detected",
                "action": "Prepare ROI analysis, cost-benefit breakdown, and competitive comparisons",
            })

        return recommendations

    def _update_stakeholder_from_interaction(
        self, stakeholder: StakeholderProfile, interaction: Dict[str, Any]
    ) -> None:
        """Update stakeholder profile based on recorded interaction"""
        # Update interaction frequency
        stakeholder.interaction_frequency += 0.1
        stakeholder.last_interaction = interaction["timestamp"]

        # Adjust relationship metrics based on outcome
        outcome = interaction.get("outcome", "neutral")
        if outcome == "positive":
            stakeholder.relationship_quality = min(1.0, stakeholder.relationship_quality + 0.05)
            stakeholder.trust_level = min(1.0, stakeholder.trust_level + 0.03)
        elif outcome == "negative":
            stakeholder.relationship_quality = max(0.0, stakeholder.relationship_quality - 0.1)
            stakeholder.trust_level = max(0.0, stakeholder.trust_level - 0.05)

    def _cleanup_old_interactions(self) -> None:
        """Remove interactions older than retention period"""
        cutoff_time = time.time() - (self.interaction_retention_days * 24 * 3600)
        
        original_count = len(self.interactions)
        self.interactions = [
            interaction for interaction in self.interactions
            if interaction.get("timestamp", 0) > cutoff_time
        ]
        
        cleaned_count = original_count - len(self.interactions)
        if cleaned_count > 0:
            self.logger.debug(f"Cleaned up {cleaned_count} old interactions")

    def get_interaction_stats(self) -> Dict[str, Any]:
        """Get interaction statistics"""
        if not self.interactions:
            return {"total_interactions": 0, "status": "no_interactions"}

        # Interaction type distribution
        type_distribution = {}
        outcome_distribution = {"positive": 0, "negative": 0, "neutral": 0}
        
        for interaction in self.interactions:
            interaction_type = interaction.get("type", "unknown")
            type_distribution[interaction_type] = type_distribution.get(interaction_type, 0) + 1
            
            outcome = interaction.get("outcome", "neutral")
            if outcome in outcome_distribution:
                outcome_distribution[outcome] += 1

        # Recent activity (last 30 days)
        recent_cutoff = time.time() - (30 * 24 * 3600)
        recent_interactions = sum(
            1 for interaction in self.interactions
            if interaction.get("timestamp", 0) > recent_cutoff
        )

        return {
            "total_interactions": len(self.interactions),
            "type_distribution": type_distribution,
            "outcome_distribution": outcome_distribution,
            "recent_interactions_30d": recent_interactions,
            "retention_days": self.interaction_retention_days,
        }
