"""
Legacy Compatibility Bridge

Provides backward compatibility for existing ConversationMemoryEngine usage
while migrating to the new Context Engineering architecture.

This bridge allows existing code to continue working during the transition period.
"""

from typing import Dict, List, Any, Optional
import time
import logging
from dataclasses import dataclass

from .advanced_context_engine import AdvancedContextEngine
from ..core.enhanced_framework_engine import ConversationContext


@dataclass
class LegacyConversationContext:
    """Legacy-compatible conversation context"""

    session_id: str
    previous_topics: List[str]
    strategic_themes: set
    framework_usage_history: List[str]
    conversation_history: List[Dict[str, Any]]

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.previous_topics = []
        self.strategic_themes = set()
        self.framework_usage_history = []
        self.conversation_history = []


class LegacyConversationMemoryBridge:
    """
    Bridge between old ConversationMemoryEngine interface and new Context Engineering

    Provides complete API compatibility while using Context Engineering backend.
    This allows existing code to work without changes during migration.
    """

    def __init__(self, context_engine: Optional[AdvancedContextEngine] = None):
        """Initialize bridge with optional existing context engine"""
        self.logger = logging.getLogger(__name__)

        # Use provided context engine or create new one
        if context_engine:
            self.context_engine = context_engine
        else:
            # Default configuration for legacy compatibility
            legacy_config = {
                "conversation": {"retention_days": 90, "max_conversations": 1000},
                "strategic": {"max_initiatives": 100, "health_threshold": 0.7},
                "stakeholder": {"max_stakeholders": 200, "interaction_retention": 365},
                "learning": {
                    "min_usage_for_pattern": 3,
                    "effectiveness_threshold": 0.7,
                },
                "organizational": {"max_team_history": 50, "change_retention": 730},
                "orchestrator": {
                    "max_context_size": 1024 * 1024,
                    "performance_target_ms": 200,
                },
            }
            self.context_engine = AdvancedContextEngine(legacy_config)

        # Legacy compatibility storage
        self.session_contexts: Dict[str, LegacyConversationContext] = {}
        self.global_patterns: Dict[str, int] = {}
        self.framework_effectiveness: Dict[str, List[float]] = {}
        self.topic_framework_mapping: Dict[str, Dict[str, int]] = {}

        self.logger.info(
            "LegacyConversationMemoryBridge initialized with Context Engineering backend"
        )

    def get_or_create_context(self, session_id: str) -> LegacyConversationContext:
        """Get existing or create new conversation context (legacy compatible)"""
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = LegacyConversationContext(session_id)

        return self.session_contexts[session_id]

    def update_context(
        self,
        session_id: str,
        user_input: str,
        topics: List[str],
        frameworks_used: List[str],
    ) -> LegacyConversationContext:
        """Update conversation context with new information (legacy compatible)"""
        # Update legacy context for immediate compatibility
        context = self.get_or_create_context(session_id)

        # Store in legacy format
        interaction = {
            "input": user_input,
            "timestamp": time.time(),
            "topics": topics,
            "frameworks": frameworks_used,
        }
        context.conversation_history.append(interaction)
        context.previous_topics.extend(topics)
        context.strategic_themes.update(topics)
        context.framework_usage_history.extend(frameworks_used)

        # ALSO store in new Context Engineering system
        try:
            # Store conversation in Context Engineering
            conversation_stored = (
                self.context_engine.conversation_layer.store_conversation_context(
                    {
                        "session_id": session_id,
                        "query": user_input,
                        "response": "",  # Response will be added later if available
                        "timestamp": time.time(),
                    }
                )
            )

            # Store learning patterns
            for framework in frameworks_used:
                self.context_engine.learning_layer.update_framework_usage(
                    framework, session_id, effectiveness_score=0.8, context=user_input
                )

            # Store decision patterns if this looks like a strategic decision
            if any(
                keyword in user_input.lower()
                for keyword in ["decide", "choose", "recommend", "strategy"]
            ):
                decision_data = {
                    "type": "strategic_conversation",
                    "context_keywords": topics,
                    "frameworks": frameworks_used,
                    "stakeholders": [],  # Could be extracted from user_input
                    "outcome_score": 0.7,  # Default for conversation context
                    "session_id": session_id,
                }
                self.context_engine.learning_layer.record_decision_outcome(
                    decision_data
                )

            if conversation_stored:
                self.logger.debug(
                    f"Successfully stored conversation in Context Engineering: {session_id}"
                )
            else:
                self.logger.warning(
                    f"Failed to store conversation in Context Engineering: {session_id}"
                )

        except Exception as e:
            self.logger.error(f"Error storing in Context Engineering: {e}")
            # Continue with legacy behavior if Context Engineering fails

        # Learn patterns for future recommendations (legacy behavior)
        for topic in topics:
            for framework in frameworks_used:
                if topic not in self.topic_framework_mapping:
                    self.topic_framework_mapping[topic] = {}
                if framework not in self.topic_framework_mapping[topic]:
                    self.topic_framework_mapping[topic][framework] = 0
                self.topic_framework_mapping[topic][framework] += 1

        return context

    def get_recent_interactions(
        self, session_id: str = "default", limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get recent conversation interactions for context analysis (legacy compatible)"""
        try:
            # Try to get from Context Engineering first (enhanced capabilities)
            context_result = (
                self.context_engine.conversation_layer.retrieve_relevant_context(
                    current_query="", session_id=session_id
                )
            )

            if (
                context_result
                and "conversations" in context_result
                and context_result["conversations"]
            ):
                # Convert Context Engineering format to legacy format
                conversations = context_result["conversations"][-limit:]  # Most recent

                return [
                    {
                        "content": conv.get("query", ""),
                        "timestamp": conv.get("timestamp", 0),
                        "topics": conv.get("topics", []),
                        "frameworks": conv.get(
                            "strategic_domains", []
                        ),  # Map strategic_domains to frameworks
                    }
                    for conv in conversations
                ]

        except Exception as e:
            self.logger.warning(
                f"Error retrieving from Context Engineering, falling back to legacy: {e}"
            )

        # Fallback to legacy storage
        if session_id not in self.session_contexts:
            return []

        context = self.session_contexts[session_id]
        recent_history = (
            context.conversation_history[-limit:]
            if context.conversation_history
            else []
        )

        return [
            {
                "content": interaction.get("input", ""),
                "timestamp": interaction.get("timestamp", 0),
                "topics": interaction.get("topics", []),
                "frameworks": interaction.get("frameworks", []),
            }
            for interaction in recent_history
        ]

    def get_context_insights(self, session_id: str) -> Dict[str, Any]:
        """Generate insights from conversation context (enhanced with Context Engineering)"""
        try:
            # Get enhanced insights from Context Engineering
            context_intelligence = self.context_engine.get_contextual_intelligence(
                query="context insights",
                session_id=session_id,
                max_context_size=256 * 1024,
            )

            if context_intelligence and "context" in context_intelligence:
                context_data = context_intelligence["context"]

                # Extract meaningful insights
                insights = {
                    "session_summary": f"Enhanced context available with {len(context_data.get('layers_included', []))} active layers",
                    "context_quality": context_data.get("context_quality", {}),
                    "strategic_themes": [],
                    "framework_recommendations": [],
                    "conversation_patterns": {},
                    "enhanced_available": True,
                }

                # Add strategic context if available
                strategic_context = context_data.get("strategic_context", {})
                if "active_initiatives" in strategic_context:
                    insights["active_initiatives_count"] = len(
                        strategic_context["active_initiatives"]
                    )

                return insights

        except Exception as e:
            self.logger.warning(
                f"Error getting Context Engineering insights, using legacy: {e}"
            )

        # Fallback to legacy insights
        if session_id not in self.session_contexts:
            return {
                "session_summary": "No conversation context available",
                "strategic_themes": [],
                "framework_recommendations": [],
                "conversation_patterns": {},
                "enhanced_available": False,
            }

        context = self.session_contexts[session_id]

        return {
            "session_summary": f"Legacy context: {len(context.conversation_history)} interactions",
            "strategic_themes": list(context.strategic_themes),
            "framework_recommendations": list(set(context.framework_usage_history)),
            "conversation_patterns": self.topic_framework_mapping,
            "enhanced_available": False,
        }

    def get_context_engine(self) -> AdvancedContextEngine:
        """Get access to the underlying Context Engineering system"""
        return self.context_engine

    def migrate_legacy_data(self, old_memory_engine) -> Dict[str, Any]:
        """Migrate data from old ConversationMemoryEngine to Context Engineering"""
        migration_stats = {
            "sessions_migrated": 0,
            "conversations_migrated": 0,
            "patterns_migrated": 0,
            "errors": [],
        }

        try:
            # Migrate session contexts
            if hasattr(old_memory_engine, "session_contexts"):
                for (
                    session_id,
                    old_context,
                ) in old_memory_engine.session_contexts.items():
                    try:
                        # Create new legacy context
                        new_context = self.get_or_create_context(session_id)

                        # Migrate conversation history
                        if hasattr(old_context, "conversation_history"):
                            for interaction in old_context.conversation_history:
                                self.update_context(
                                    session_id=session_id,
                                    user_input=interaction.get("input", ""),
                                    topics=interaction.get("topics", []),
                                    frameworks_used=interaction.get("frameworks", []),
                                )
                                migration_stats["conversations_migrated"] += 1

                        migration_stats["sessions_migrated"] += 1

                    except Exception as e:
                        error_msg = f"Error migrating session {session_id}: {e}"
                        migration_stats["errors"].append(error_msg)
                        self.logger.error(error_msg)

            # Migrate topic-framework patterns
            if hasattr(old_memory_engine, "topic_framework_mapping"):
                self.topic_framework_mapping = (
                    old_memory_engine.topic_framework_mapping.copy()
                )
                migration_stats["patterns_migrated"] = len(self.topic_framework_mapping)

            self.logger.info(f"Migration completed: {migration_stats}")
            return migration_stats

        except Exception as e:
            error_msg = f"Migration failed: {e}"
            migration_stats["errors"].append(error_msg)
            self.logger.error(error_msg)
            return migration_stats


def create_legacy_bridge(
    context_engine: Optional[AdvancedContextEngine] = None,
) -> LegacyConversationMemoryBridge:
    """Factory function to create legacy compatibility bridge"""
    return LegacyConversationMemoryBridge(context_engine)
