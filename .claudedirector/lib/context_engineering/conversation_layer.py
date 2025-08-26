"""
Conversation Layer Memory

Semantic conversation indexing and retrieval with 90-day retention.
Provides conversation continuity across sessions.
"""

from typing import Dict, List, Any, Optional
import time
import json
import logging
from pathlib import Path


class ConversationLayerMemory:
    """
    Conversation context storage and retrieval with semantic indexing

    Features:
    - Semantic conversation clustering by topic and strategic domain
    - 90-day conversation retention with automatic cleanup
    - Relevance scoring for intelligent context assembly
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize conversation layer with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Storage configuration
        self.retention_days = self.config.get("retention_days", 90)
        self.max_conversations_per_session = self.config.get("max_conversations", 1000)

        # In-memory storage for Phase 1 implementation
        # Phase 2 will add SQLite/DuckDB persistent storage
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}

        self.logger.info(
            f"ConversationLayerMemory initialized with {self.retention_days} day retention"
        )

    def store_conversation_context(self, session_data: Dict[str, Any]) -> bool:
        """
        Store conversation context with semantic indexing

        Args:
            session_data: Contains session_id, query, response, timestamp

        Returns:
            True if storage successful, False otherwise
        """
        try:
            session_id = session_data.get("session_id", "default")

            # Initialize session if not exists
            if session_id not in self.conversations:
                self.conversations[session_id] = []

            # Add conversation with metadata
            conversation_record = {
                "query": session_data.get("query", ""),
                "response": session_data.get("response", ""),
                "timestamp": session_data.get("timestamp", time.time()),
                "topics": self._extract_topics(session_data.get("query", "")),
                "strategic_domains": self._identify_strategic_domains(
                    session_data.get("query", "")
                ),
                "conversation_id": f"{session_id}_{int(time.time())}",
            }

            self.conversations[session_id].append(conversation_record)

            # Cleanup old conversations
            self._cleanup_old_conversations(session_id)

            # Limit conversations per session
            if len(self.conversations[session_id]) > self.max_conversations_per_session:
                self.conversations[session_id] = self.conversations[session_id][
                    -self.max_conversations_per_session :
                ]

            self.logger.debug(f"Stored conversation for session {session_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to store conversation context: {e}")
            return False

    def retrieve_relevant_context(
        self, current_query: str, session_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Retrieve relevant conversation context with semantic similarity

        Args:
            current_query: Current user query for context matching
            session_id: Session identifier

        Returns:
            Relevant conversation context with relevance scores
        """
        try:
            if session_id not in self.conversations:
                return {"conversations": [], "relevance_score": 0.0}

            conversations = self.conversations[session_id]

            # Extract topics from current query
            current_topics = self._extract_topics(current_query)
            current_domains = self._identify_strategic_domains(current_query)

            # Score conversations by relevance
            scored_conversations = []
            for conv in conversations:
                relevance_score = self._calculate_conversation_relevance(
                    current_topics, current_domains, conv
                )
                if relevance_score > 0.3:  # Relevance threshold
                    scored_conversations.append(
                        {"conversation": conv, "relevance_score": relevance_score}
                    )

            # Sort by relevance and limit results
            scored_conversations.sort(key=lambda x: x["relevance_score"], reverse=True)
            top_conversations = scored_conversations[:5]  # Top 5 most relevant

            # Calculate overall relevance
            overall_relevance = sum(
                sc["relevance_score"] for sc in top_conversations
            ) / max(len(top_conversations), 1)

            return {
                "conversations": [sc["conversation"] for sc in top_conversations],
                "relevance_scores": [sc["relevance_score"] for sc in top_conversations],
                "overall_relevance": overall_relevance,
                "total_conversations": len(conversations),
                "relevant_conversations": len(top_conversations),
            }

        except Exception as e:
            self.logger.error(f"Failed to retrieve conversation context: {e}")
            return {"conversations": [], "relevance_score": 0.0, "error": str(e)}

    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text (simplified implementation)"""
        # Phase 2: Enhance with NLP-based topic extraction
        strategic_keywords = [
            "strategy",
            "team",
            "platform",
            "architecture",
            "stakeholder",
            "framework",
            "decision",
            "initiative",
            "planning",
            "scaling",
            "organization",
            "leadership",
            "alignment",
            "design",
            "system",
        ]

        text_lower = text.lower()
        topics = [keyword for keyword in strategic_keywords if keyword in text_lower]
        return topics

    def _identify_strategic_domains(self, text: str) -> List[str]:
        """Identify strategic domains in text"""
        domain_patterns = {
            "engineering_leadership": [
                "team",
                "leadership",
                "management",
                "coordination",
            ],
            "platform_strategy": ["platform", "architecture", "technical", "system"],
            "design_systems": ["design", "ui", "ux", "component", "interface"],
            "business_strategy": ["business", "roi", "investment", "value", "market"],
            "organizational": ["organization", "structure", "culture", "process"],
        }

        text_lower = text.lower()
        domains = []

        for domain, keywords in domain_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                domains.append(domain)

        return domains

    def _calculate_conversation_relevance(
        self,
        current_topics: List[str],
        current_domains: List[str],
        conversation: Dict[str, Any],
    ) -> float:
        """Calculate relevance score between current query and stored conversation"""
        conv_topics = conversation.get("topics", [])
        conv_domains = conversation.get("strategic_domains", [])

        # Topic overlap score
        topic_overlap = len(set(current_topics) & set(conv_topics)) / max(
            len(current_topics), 1
        )

        # Domain overlap score
        domain_overlap = len(set(current_domains) & set(conv_domains)) / max(
            len(current_domains), 1
        )

        # Time decay factor (more recent conversations more relevant)
        time_diff = time.time() - conversation.get("timestamp", time.time())
        time_decay = max(0.1, 1.0 - (time_diff / (7 * 24 * 3600)))  # Decay over 7 days

        # Combined relevance score
        relevance = topic_overlap * 0.4 + domain_overlap * 0.4 + time_decay * 0.2

        return min(relevance, 1.0)

    def _cleanup_old_conversations(self, session_id: str) -> None:
        """Remove conversations older than retention period"""
        if session_id not in self.conversations:
            return

        cutoff_time = time.time() - (self.retention_days * 24 * 3600)

        self.conversations[session_id] = [
            conv
            for conv in self.conversations[session_id]
            if conv.get("timestamp", time.time()) > cutoff_time
        ]

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        total_conversations = sum(len(convs) for convs in self.conversations.values())
        total_sessions = len(self.conversations)

        # Estimate memory usage
        estimated_bytes = 0
        for session_convs in self.conversations.values():
            for conv in session_convs:
                estimated_bytes += len(json.dumps(conv).encode("utf-8"))

        return {
            "total_conversations": total_conversations,
            "total_sessions": total_sessions,
            "estimated_memory_bytes": estimated_bytes,
            "estimated_memory_mb": estimated_bytes / (1024 * 1024),
            "retention_days": self.retention_days,
            "total_memory_bytes": estimated_bytes,
            "total_memory_mb": estimated_bytes / (1024 * 1024),
        }
