"""
Semantic Search Engine for Decision Intelligence

Delbert's semantic search infrastructure for ClaudeDirector.
Enables natural language queries across strategic documents and decision history.
"""

import time
import json
import sqlite3
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import structlog
import threading
import math

from .db_base import DatabaseEngineBase
from ....core.config import ClaudeDirectorConfig, get_config

logger = structlog.get_logger(__name__)


class SearchType(Enum):
    """Types of semantic search queries"""

    DECISION_CONTEXT = "decision_context"  # Find decisions similar to current context
    STAKEHOLDER_INTELLIGENCE = "stakeholder"  # Search stakeholder interaction patterns
    INITIATIVE_SIMILARITY = "initiative"  # Find similar initiatives and outcomes
    STRATEGIC_THEMES = "strategic"  # Identify strategic patterns and themes
    MEETING_INTELLIGENCE = "meeting"  # Search meeting outcomes and context


@dataclass
class SemanticResult:
    """Semantic search result with relevance scoring"""

    content: str
    source_table: str
    source_id: str
    relevance_score: float
    context_type: SearchType
    metadata: Dict[str, Any]
    highlighted_snippets: List[str]


@dataclass
class SearchQuery:
    """Semantic search query specification"""

    query_text: str
    search_type: SearchType
    max_results: int = 10
    min_relevance: float = 0.3
    context_filters: Optional[Dict[str, Any]] = None
    include_metadata: bool = True


class SemanticSearchEngine(DatabaseEngineBase):
    """
    Semantic search engine for strategic intelligence

    Delbert's Semantic Search Features:
    1. Natural language querying across all strategic data
    2. Context-aware relevance scoring
    3. Strategic pattern recognition
    4. Cross-table semantic correlation
    5. Real-time embedding generation and caching
    """

    def __init__(self, config, director_config: Optional[ClaudeDirectorConfig] = None):
        super().__init__(config)
        self.director_config = director_config or get_config()
        self.logger = logger.bind(component="semantic_search_engine")

        # Search engine configuration
        self._embedding_cache: Dict[str, List[float]] = {}
        self._cache_lock = threading.Lock()
        self._max_cache_size = 10000

        # Semantic indexing for strategic content
        self._strategic_content_index = {
            "executive_sessions": [
                "agenda_topics",
                "decisions_made",
                "action_items",
                "business_impact",
                "next_session_prep",
            ],
            "strategic_initiatives": [
                "initiative_name",
                "business_value",
                "milestone_history",
                "roi_tracking",
                "stakeholder_impact",
            ],
            "stakeholder_profiles": [
                "communication_style",
                "decision_criteria",
                "interaction_history",
                "preferred_personas",
                "success_metrics",
            ],
            "platform_intelligence": [
                "metric_name",
                "business_impact",
                "action_required",
            ],
            "meeting_sessions": [
                "agenda_items",
                "meeting_outcomes",
                "strategic_themes",
                "preparation_notes",
                "next_meeting_prep",
            ],
        }

        # Relevance scoring weights
        self._relevance_weights = {
            "text_similarity": 0.4,
            "context_relevance": 0.3,
            "recency_factor": 0.2,
            "strategic_importance": 0.1,
        }

        # Performance metrics
        self._search_metrics = {
            "total_searches": 0,
            "avg_response_time_ms": 0,
            "cache_hit_ratio": 0,
            "relevance_scores": [],
        }

    def connect(self) -> bool:
        """Connect semantic search engine with indexing preparation"""
        try:
            start_time = time.time()

            # Connect to primary database
            self._connection = sqlite3.connect(
                str(self.config.database_path), timeout=30, check_same_thread=False
            )
            self._connection.row_factory = sqlite3.Row

            # Initialize semantic search schema
            self._initialize_semantic_schema()

            # Build semantic indexes if needed
            self._build_semantic_indexes()

            # Validate search performance
            self._validate_search_performance()

            connection_time = (time.time() - start_time) * 1000

            self.logger.info(
                "Semantic search engine connected",
                connection_time_ms=connection_time,
                indexed_tables=len(self._strategic_content_index),
                cache_enabled=True,
            )

            return True

        except Exception as e:
            self.logger.error("Semantic search engine connection failed", error=str(e))
            return False

    def search(self, query: SearchQuery) -> List[SemanticResult]:
        """
        Execute semantic search across strategic content

        Delbert's Search Algorithm:
        1. Parse query and extract semantic features
        2. Generate search embeddings
        3. Calculate relevance scores across content
        4. Apply context filters and ranking
        5. Return ranked results with metadata
        """
        start_time = time.time()

        try:
            self._search_metrics["total_searches"] += 1

            # Generate query embedding
            query_embedding = self._generate_query_embedding(query.query_text)

            # Search across relevant tables
            raw_results = self._search_content_tables(query, query_embedding)

            # Calculate relevance scores
            scored_results = self._calculate_relevance_scores(
                raw_results, query, query_embedding
            )

            # Apply filters and ranking
            filtered_results = self._apply_filters_and_ranking(scored_results, query)

            # Generate highlighted snippets
            final_results = self._generate_highlighted_results(filtered_results, query)

            execution_time = (time.time() - start_time) * 1000

            # Update performance metrics
            self._update_search_metrics(execution_time, final_results)

            self.logger.info(
                "Semantic search completed",
                query_text=query.query_text[:50],
                search_type=query.search_type.value,
                results_found=len(final_results),
                execution_time_ms=execution_time,
            )

            return final_results

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(
                "Semantic search failed",
                query_text=query.query_text[:50],
                execution_time_ms=execution_time,
                error=str(e),
            )
            return []

    def find_similar_decisions(
        self, context: Dict[str, Any], max_results: int = 5
    ) -> List[SemanticResult]:
        """Find decisions similar to current context"""
        context_text = self._extract_context_text(context)

        query = SearchQuery(
            query_text=context_text,
            search_type=SearchType.DECISION_CONTEXT,
            max_results=max_results,
            min_relevance=0.4,
            context_filters={"has_decisions": True},
        )

        return self.search(query)

    def search_stakeholder_patterns(
        self, stakeholder_key: str, pattern_query: str
    ) -> List[SemanticResult]:
        """Search for specific patterns in stakeholder interactions"""
        query = SearchQuery(
            query_text=pattern_query,
            search_type=SearchType.STAKEHOLDER_INTELLIGENCE,
            max_results=8,
            min_relevance=0.3,
            context_filters={"stakeholder_key": stakeholder_key},
        )

        return self.search(query)

    def find_strategic_themes(
        self, theme_query: str, time_range_days: int = 90
    ) -> List[SemanticResult]:
        """Find strategic themes and patterns across time"""
        query = SearchQuery(
            query_text=theme_query,
            search_type=SearchType.STRATEGIC_THEMES,
            max_results=15,
            min_relevance=0.25,
            context_filters={"time_range_days": time_range_days},
        )

        return self.search(query)

    def get_search_performance_metrics(self) -> Dict[str, Any]:
        """Get semantic search performance metrics"""
        return {
            "total_searches": self._search_metrics["total_searches"],
            "avg_response_time_ms": self._search_metrics["avg_response_time_ms"],
            "cache_hit_ratio": self._search_metrics["cache_hit_ratio"],
            "cache_size": len(self._embedding_cache),
            "avg_relevance_score": (
                sum(self._search_metrics["relevance_scores"])
                / len(self._search_metrics["relevance_scores"])
                if self._search_metrics["relevance_scores"]
                else 0
            ),
            "indexed_content_types": len(self._strategic_content_index),
        }

    # Private methods for semantic search implementation

    def _initialize_semantic_schema(self):
        """Initialize semantic search schema and indexes"""
        try:
            # Create semantic search cache table
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS semantic_search_cache (
                    content_hash TEXT PRIMARY KEY,
                    embedding_vector TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create semantic search index
            self._connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_semantic_cache_type
                ON semantic_search_cache(content_type)
            """
            )

            # Create search performance tracking
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS search_performance_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_text TEXT NOT NULL,
                    search_type TEXT NOT NULL,
                    execution_time_ms INTEGER NOT NULL,
                    results_count INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            self._connection.commit()

        except Exception as e:
            self.logger.warning("Semantic schema initialization failed", error=str(e))

    def _build_semantic_indexes(self):
        """Build semantic indexes for strategic content"""
        try:
            # Check if indexes need to be built/updated
            cursor = self._connection.execute(
                """
                SELECT COUNT(*) as count FROM semantic_search_cache
            """
            )
            cached_count = cursor.fetchone()["count"]

            if cached_count < 10:  # Rebuild if cache is sparse
                self.logger.info("Building semantic indexes for strategic content")
                self._rebuild_semantic_cache()

        except Exception as e:
            self.logger.warning("Semantic index building failed", error=str(e))

    def _validate_search_performance(self):
        """Validate semantic search performance"""
        test_queries = [
            SearchQuery("platform adoption metrics", SearchType.STRATEGIC_THEMES),
            SearchQuery(
                "stakeholder engagement patterns", SearchType.STAKEHOLDER_INTELLIGENCE
            ),
            SearchQuery("initiative risk factors", SearchType.DECISION_CONTEXT),
        ]

        performance_results = []

        for query in test_queries:
            start_time = time.time()
            results = self.search(query)
            execution_time = (time.time() - start_time) * 1000

            performance_results.append(
                {
                    "query_type": query.search_type.value,
                    "execution_time_ms": execution_time,
                    "results_count": len(results),
                    "meets_sla": execution_time < self.config.max_query_time_ms,
                }
            )

        sla_compliant = sum(1 for r in performance_results if r["meets_sla"])
        avg_time = sum(r["execution_time_ms"] for r in performance_results) / len(
            performance_results
        )

        self.logger.info(
            "Semantic search performance validation",
            sla_compliant_queries=sla_compliant,
            total_test_queries=len(performance_results),
            avg_execution_time_ms=round(avg_time, 2),
        )

    def _generate_query_embedding(self, query_text: str) -> List[float]:
        """Generate embedding for search query (simplified implementation)"""
        # Check cache first
        query_hash = hashlib.md5(query_text.encode()).hexdigest()

        with self._cache_lock:
            if query_hash in self._embedding_cache:
                return self._embedding_cache[query_hash]

        # Simplified embedding generation (would use actual embedding model)
        # For now, use simple text feature extraction
        embedding = self._extract_text_features(query_text)

        # Cache the embedding
        with self._cache_lock:
            if len(self._embedding_cache) >= self._max_cache_size:
                # Remove oldest entry
                oldest_key = next(iter(self._embedding_cache))
                del self._embedding_cache[oldest_key]

            self._embedding_cache[query_hash] = embedding

        return embedding

    def _extract_text_features(self, text: str) -> List[float]:
        """Extract simplified text features for semantic comparison"""
        # Simplified feature extraction (would use proper embeddings in production)
        text_lower = text.lower()

        # Strategic keyword features
        strategic_keywords = {
            "decision": ["decision", "decide", "choice", "select"],
            "risk": ["risk", "danger", "threat", "concern"],
            "progress": ["progress", "advance", "forward", "improve"],
            "stakeholder": ["stakeholder", "team", "people", "user"],
            "initiative": ["initiative", "project", "effort", "program"],
            "platform": ["platform", "system", "infrastructure", "framework"],
            "health": ["health", "status", "condition", "state"],
            "trend": ["trend", "pattern", "direction", "movement"],
        }

        features = []

        # Keyword presence features
        for category, keywords in strategic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            features.append(score / len(keywords))  # Normalize

        # Text length feature
        features.append(min(1.0, len(text) / 500))  # Normalize to 500 chars

        # Question vs statement feature
        features.append(1.0 if "?" in text else 0.0)

        # Urgency indicators
        urgency_words = ["urgent", "critical", "immediate", "asap", "priority"]
        urgency_score = sum(1 for word in urgency_words if word in text_lower)
        features.append(min(1.0, urgency_score / 3))

        # Temporal indicators
        temporal_words = ["now", "today", "tomorrow", "next", "soon", "later"]
        temporal_score = sum(1 for word in temporal_words if word in text_lower)
        features.append(min(1.0, temporal_score / 3))

        # Pad to fixed size (16 features)
        while len(features) < 16:
            features.append(0.0)

        return features[:16]  # Ensure exactly 16 features

    def _search_content_tables(
        self, query: SearchQuery, query_embedding: List[float]
    ) -> List[Dict[str, Any]]:
        """Search across strategic content tables"""
        raw_results = []

        # Search based on query type
        if query.search_type == SearchType.DECISION_CONTEXT:
            raw_results.extend(self._search_executive_sessions(query))
            raw_results.extend(self._search_meeting_sessions(query))

        elif query.search_type == SearchType.STAKEHOLDER_INTELLIGENCE:
            raw_results.extend(self._search_stakeholder_profiles(query))
            raw_results.extend(self._search_executive_sessions(query))

        elif query.search_type == SearchType.INITIATIVE_SIMILARITY:
            raw_results.extend(self._search_strategic_initiatives(query))

        elif query.search_type == SearchType.STRATEGIC_THEMES:
            # Search across all tables for strategic themes
            raw_results.extend(self._search_executive_sessions(query))
            raw_results.extend(self._search_strategic_initiatives(query))
            raw_results.extend(self._search_platform_intelligence(query))

        elif query.search_type == SearchType.MEETING_INTELLIGENCE:
            raw_results.extend(self._search_meeting_sessions(query))
            raw_results.extend(self._search_executive_sessions(query))

        return raw_results

    def _search_executive_sessions(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """Search executive sessions table"""
        sql = """
            SELECT id, session_type, stakeholder_key, meeting_date,
                   agenda_topics, decisions_made, action_items, business_impact,
                   next_session_prep, persona_activated
            FROM executive_sessions
            WHERE 1=1
        """

        params = []

        # Apply context filters
        if query.context_filters:
            if "stakeholder_key" in query.context_filters:
                sql += " AND stakeholder_key = ?"
                params.append(query.context_filters["stakeholder_key"])

            if "time_range_days" in query.context_filters:
                sql += " AND meeting_date >= date('now', '-' || ? || ' days')"
                params.append(query.context_filters["time_range_days"])

            if "has_decisions" in query.context_filters:
                sql += " AND decisions_made IS NOT NULL AND decisions_made != ''"

        sql += " ORDER BY meeting_date DESC LIMIT 50"

        cursor = self._connection.execute(sql, params)
        results = []

        for row in cursor.fetchall():
            # Combine searchable content
            content_parts = []
            for field in [
                "agenda_topics",
                "decisions_made",
                "action_items",
                "business_impact",
            ]:
                if row[field]:
                    content_parts.append(str(row[field]))

            content = " ".join(content_parts)

            results.append(
                {
                    "source_table": "executive_sessions",
                    "source_id": str(row["id"]),
                    "content": content,
                    "metadata": {
                        "session_type": row["session_type"],
                        "stakeholder_key": row["stakeholder_key"],
                        "meeting_date": row["meeting_date"],
                        "persona_activated": row["persona_activated"],
                    },
                }
            )

        return results

    def _search_strategic_initiatives(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """Search strategic initiatives table"""
        sql = """
            SELECT id, initiative_key, initiative_name, status, priority,
                   business_value, risk_level, milestone_history, roi_tracking,
                   stakeholder_impact, created_at, updated_at
            FROM strategic_initiatives
            WHERE 1=1
        """

        params = []

        if query.context_filters and "time_range_days" in query.context_filters:
            sql += " AND updated_at >= date('now', '-' || ? || ' days')"
            params.append(query.context_filters["time_range_days"])

        sql += " ORDER BY updated_at DESC LIMIT 50"

        cursor = self._connection.execute(sql, params)
        results = []

        for row in cursor.fetchall():
            content_parts = [
                row["initiative_name"] or "",
                row["business_value"] or "",
                row["milestone_history"] or "",
                row["stakeholder_impact"] or "",
            ]

            content = " ".join(filter(None, content_parts))

            results.append(
                {
                    "source_table": "strategic_initiatives",
                    "source_id": str(row["id"]),
                    "content": content,
                    "metadata": {
                        "initiative_key": row["initiative_key"],
                        "status": row["status"],
                        "priority": row["priority"],
                        "risk_level": row["risk_level"],
                        "updated_at": row["updated_at"],
                    },
                }
            )

        return results

    def _search_stakeholder_profiles(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """Search stakeholder profiles table"""
        sql = """
            SELECT id, stakeholder_key, display_name, role_title,
                   communication_style, decision_criteria, interaction_history,
                   preferred_personas, success_metrics
            FROM stakeholder_profiles
            WHERE 1=1
        """

        params = []

        if query.context_filters and "stakeholder_key" in query.context_filters:
            sql += " AND stakeholder_key = ?"
            params.append(query.context_filters["stakeholder_key"])

        sql += " LIMIT 20"

        cursor = self._connection.execute(sql, params)
        results = []

        for row in cursor.fetchall():
            content_parts = [
                row["communication_style"] or "",
                row["decision_criteria"] or "",
                row["interaction_history"] or "",
                row["success_metrics"] or "",
            ]

            content = " ".join(filter(None, content_parts))

            results.append(
                {
                    "source_table": "stakeholder_profiles",
                    "source_id": str(row["id"]),
                    "content": content,
                    "metadata": {
                        "stakeholder_key": row["stakeholder_key"],
                        "display_name": row["display_name"],
                        "role_title": row["role_title"],
                        "communication_style": row["communication_style"],
                    },
                }
            )

        return results

    def _search_platform_intelligence(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """Search platform intelligence table"""
        sql = """
            SELECT id, intelligence_type, category, metric_name, value_numeric,
                   value_text, business_impact, action_required, measurement_date
            FROM platform_intelligence
            WHERE 1=1
        """

        params = []

        if query.context_filters and "time_range_days" in query.context_filters:
            sql += " AND measurement_date >= date('now', '-' || ? || ' days')"
            params.append(query.context_filters["time_range_days"])

        sql += " ORDER BY measurement_date DESC LIMIT 30"

        cursor = self._connection.execute(sql, params)
        results = []

        for row in cursor.fetchall():
            content_parts = [
                row["metric_name"] or "",
                row["business_impact"] or "",
                row["action_required"] or "",
            ]

            content = " ".join(filter(None, content_parts))

            results.append(
                {
                    "source_table": "platform_intelligence",
                    "source_id": str(row["id"]),
                    "content": content,
                    "metadata": {
                        "category": row["category"],
                        "metric_name": row["metric_name"],
                        "value_numeric": row["value_numeric"],
                        "trend_direction": row.get("trend_direction"),
                        "measurement_date": row["measurement_date"],
                    },
                }
            )

        return results

    def _search_meeting_sessions(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """Search meeting sessions table (if exists)"""
        # Check if meeting_sessions table exists
        try:
            cursor = self._connection.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='meeting_sessions'
            """
            )
            if not cursor.fetchone():
                return []
        except:
            return []

        sql = """
            SELECT id, meeting_key, meeting_type, stakeholder_primary,
                   agenda_items, meeting_outcomes, strategic_themes,
                   preparation_notes, meeting_date
            FROM meeting_sessions
            WHERE meeting_status = 'completed'
        """

        params = []

        if query.context_filters:
            if "stakeholder_key" in query.context_filters:
                sql += " AND stakeholder_primary = ?"
                params.append(query.context_filters["stakeholder_key"])

            if "time_range_days" in query.context_filters:
                sql += " AND meeting_date >= date('now', '-' || ? || ' days')"
                params.append(query.context_filters["time_range_days"])

        sql += " ORDER BY meeting_date DESC LIMIT 30"

        try:
            cursor = self._connection.execute(sql, params)
            results = []

            for row in cursor.fetchall():
                content_parts = [
                    row["agenda_items"] or "",
                    row["meeting_outcomes"] or "",
                    row["strategic_themes"] or "",
                    row["preparation_notes"] or "",
                ]

                content = " ".join(filter(None, content_parts))

                results.append(
                    {
                        "source_table": "meeting_sessions",
                        "source_id": str(row["id"]),
                        "content": content,
                        "metadata": {
                            "meeting_key": row["meeting_key"],
                            "meeting_type": row["meeting_type"],
                            "stakeholder_primary": row["stakeholder_primary"],
                            "meeting_date": row["meeting_date"],
                        },
                    }
                )

            return results

        except Exception as e:
            self.logger.warning("Meeting sessions search failed", error=str(e))
            return []

    def _calculate_relevance_scores(
        self,
        raw_results: List[Dict[str, Any]],
        query: SearchQuery,
        query_embedding: List[float],
    ) -> List[Dict[str, Any]]:
        """Calculate relevance scores for search results"""
        scored_results = []

        for result in raw_results:
            # Generate content embedding
            content_embedding = self._extract_text_features(result["content"])

            # Calculate similarity score
            similarity_score = self._cosine_similarity(
                query_embedding, content_embedding
            )

            # Calculate context relevance
            context_score = self._calculate_context_relevance(result, query)

            # Calculate recency factor
            recency_score = self._calculate_recency_factor(result)

            # Calculate strategic importance
            importance_score = self._calculate_strategic_importance(result)

            # Weighted final score
            final_score = (
                similarity_score * self._relevance_weights["text_similarity"]
                + context_score * self._relevance_weights["context_relevance"]
                + recency_score * self._relevance_weights["recency_factor"]
                + importance_score * self._relevance_weights["strategic_importance"]
            )

            result["relevance_score"] = final_score
            result["similarity_score"] = similarity_score
            result["context_score"] = context_score

            scored_results.append(result)

        return scored_results

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(a * a for a in vec2))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def _calculate_context_relevance(
        self, result: Dict[str, Any], query: SearchQuery
    ) -> float:
        """Calculate context-specific relevance score"""
        score = 0.5  # Base score

        metadata = result.get("metadata", {})

        # Table-specific relevance
        if query.search_type == SearchType.DECISION_CONTEXT:
            if result["source_table"] == "executive_sessions":
                score += 0.3
            if "decisions_made" in result["content"].lower():
                score += 0.2

        elif query.search_type == SearchType.STAKEHOLDER_INTELLIGENCE:
            if result["source_table"] == "stakeholder_profiles":
                score += 0.3
            if query.context_filters and "stakeholder_key" in query.context_filters:
                if (
                    metadata.get("stakeholder_key")
                    == query.context_filters["stakeholder_key"]
                ):
                    score += 0.4

        elif query.search_type == SearchType.STRATEGIC_THEMES:
            if "strategic" in result["content"].lower():
                score += 0.2
            if metadata.get("session_type") == "strategic_planning":
                score += 0.3

        return min(1.0, score)

    def _calculate_recency_factor(self, result: Dict[str, Any]) -> float:
        """Calculate recency factor for result relevance"""
        metadata = result.get("metadata", {})

        # Extract date from metadata
        date_field = None
        for field in ["meeting_date", "updated_at", "measurement_date"]:
            if field in metadata and metadata[field]:
                date_field = metadata[field]
                break

        if not date_field:
            return 0.5  # Default for no date

        try:
            # Simplified recency calculation (would use proper date parsing)
            # Assume recent items get higher scores
            if "date(" in str(date_field) or "2025-" in str(date_field):
                return 0.9  # Recent
            elif "2024-" in str(date_field):
                return 0.7  # Somewhat recent
            else:
                return 0.3  # Older
        except:
            return 0.5

    def _calculate_strategic_importance(self, result: Dict[str, Any]) -> float:
        """Calculate strategic importance score"""
        importance = 0.5  # Base importance

        content_lower = result["content"].lower()
        metadata = result.get("metadata", {})

        # High importance indicators
        if any(
            word in content_lower
            for word in ["critical", "urgent", "strategic", "priority"]
        ):
            importance += 0.3

        # Table-specific importance
        if result["source_table"] == "executive_sessions":
            if metadata.get("session_type") == "strategic_planning":
                importance += 0.2

        elif result["source_table"] == "strategic_initiatives":
            if metadata.get("priority") in [
                self.director_config.get_enum_values("priority_levels")[0],
                self.director_config.get_enum_values("priority_levels")[1],
            ]:
                importance += 0.3
            if metadata.get("risk_level") == "red":
                importance += 0.2

        return min(1.0, importance)

    def _apply_filters_and_ranking(
        self, scored_results: List[Dict[str, Any]], query: SearchQuery
    ) -> List[Dict[str, Any]]:
        """Apply filters and rank results"""
        # Filter by minimum relevance
        filtered_results = [
            r for r in scored_results if r["relevance_score"] >= query.min_relevance
        ]

        # Sort by relevance score
        ranked_results = sorted(
            filtered_results, key=lambda x: x["relevance_score"], reverse=True
        )

        # Limit results
        return ranked_results[: query.max_results]

    def _generate_highlighted_results(
        self, ranked_results: List[Dict[str, Any]], query: SearchQuery
    ) -> List[SemanticResult]:
        """Generate final semantic results with highlighting"""
        final_results = []

        for result in ranked_results:
            # Generate highlighted snippets (simplified)
            snippets = self._generate_snippets(result["content"], query.query_text)

            semantic_result = SemanticResult(
                content=result["content"],
                source_table=result["source_table"],
                source_id=result["source_id"],
                relevance_score=result["relevance_score"],
                context_type=query.search_type,
                metadata=result.get("metadata", {}),
                highlighted_snippets=snippets,
            )

            final_results.append(semantic_result)

        return final_results

    def _generate_snippets(self, content: str, query_text: str) -> List[str]:
        """Generate highlighted snippets from content"""
        # Simplified snippet generation
        words = content.split()
        query_words = [w.lower() for w in query_text.split()]

        snippets = []
        snippet_length = 50  # words

        # Find passages containing query words
        for i in range(0, len(words), snippet_length // 2):
            snippet_words = words[i : i + snippet_length]
            snippet_text = " ".join(snippet_words).lower()

            # Check if snippet contains query words
            if any(qword in snippet_text for qword in query_words):
                snippet = " ".join(snippet_words)
                if len(snippet) > 20:  # Minimum snippet length
                    snippets.append(snippet)

                if len(snippets) >= 3:  # Max 3 snippets
                    break

        return snippets

    def _extract_context_text(self, context: Dict[str, Any]) -> str:
        """Extract searchable text from context"""
        text_parts = []

        for key, value in context.items():
            if isinstance(value, str) and len(value) > 5:
                text_parts.append(value)
            elif isinstance(value, dict):
                text_parts.append(json.dumps(value))

        return " ".join(text_parts)

    def _rebuild_semantic_cache(self):
        """Rebuild semantic search cache (placeholder)"""
        # Would implement cache rebuilding logic
        self.logger.info("Semantic cache rebuild - placeholder implementation")

    def _update_search_metrics(
        self, execution_time: float, results: List[SemanticResult]
    ):
        """Update search performance metrics"""
        self._search_metrics["avg_response_time_ms"] = (
            self._search_metrics["avg_response_time_ms"]
            * (self._search_metrics["total_searches"] - 1)
            + execution_time
        ) / self._search_metrics["total_searches"]

        if results:
            avg_relevance = sum(r.relevance_score for r in results) / len(results)
            self._search_metrics["relevance_scores"].append(avg_relevance)

            # Keep only recent relevance scores
            if len(self._search_metrics["relevance_scores"]) > 100:
                self._search_metrics["relevance_scores"] = self._search_metrics[
                    "relevance_scores"
                ][-100:]
