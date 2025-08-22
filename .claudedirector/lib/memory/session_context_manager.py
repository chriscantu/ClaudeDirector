#!/usr/bin/env python3
"""
ClaudeDirector Session Context Manager
Critical framework enhancement for session continuity across restarts
"""

import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List

from .memory_manager import StrategicMemoryManager


class SessionContextManager(StrategicMemoryManager):
    """
    Enhanced strategic memory manager with session context preservation
    Ensures critical context survives session restarts and system interruptions
    """

    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to ClaudeDirector data directory
            from pathlib import Path

            base_path = Path(__file__).parent.parent.parent.parent.parent
            db_path = str(base_path / "data" / "strategic_memory.db")
        super().__init__(db_path)
        self.current_session_id = None
        self.context_backup_interval = 300  # 5 minutes
        self.critical_context_patterns = [
            "stakeholder_profiles",
            "executive_sessions",
            "strategic_initiatives",
            "roi_discussions",
            "coalition_mapping",
            "platform_investment_context",
        ]
        self._ensure_session_schema()

    def _ensure_session_schema(self):
        """Ensure session context tables exist"""
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "config",
            "schemas",
            "session_context_schema.sql",
        )

        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                schema_sql = f.read()

            with self.get_connection() as conn:
                conn.executescript(schema_sql)
        else:
            # Fallback: create essential tables inline
            self._create_essential_session_tables()

    def _create_essential_session_tables(self):
        """Create essential session context tables if schema file unavailable"""
        with self.get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS session_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    session_type TEXT NOT NULL,
                    active_personas TEXT,
                    stakeholder_context TEXT,
                    strategic_initiatives_context TEXT,
                    executive_context TEXT,
                    roi_discussions_context TEXT,
                    coalition_mapping_context TEXT,
                    conversation_thread TEXT,
                    last_backup_timestamp TIMESTAMP NOT NULL,
                    session_start_timestamp TIMESTAMP NOT NULL,
                    context_quality_score REAL DEFAULT 0.5,
                    recovery_priority TEXT DEFAULT 'medium',
                    context_validation_status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS context_gaps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    gap_type TEXT NOT NULL,
                    gap_description TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    recovery_strategy TEXT,
                    recovery_status TEXT DEFAULT 'identified',
                    detected_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

    def get_recent_sessions(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent sessions within specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT session_id, session_type, session_start_timestamp,
                       last_backup_timestamp, context_quality_score
                FROM session_context
                WHERE session_start_timestamp > ?
                ORDER BY session_start_timestamp DESC
            """,
                (cutoff_time.isoformat(),),
            )

            sessions = []
            for row in cursor.fetchall():
                sessions.append(
                    {
                        "session_id": row[0],
                        "session_type": row[1],
                        "session_start_timestamp": row[2],
                        "last_backup_timestamp": row[3],
                        "context_quality_score": row[4],
                    }
                )

            return sessions

    def update_session_context(
        self, session_id: str, context_data: Dict[str, Any]
    ) -> bool:
        """Update session context with new data"""
        try:
            with self.get_connection() as conn:
                # Prepare context data as JSON strings
                active_personas = json.dumps(context_data.get("active_personas", []))
                stakeholder_context = json.dumps(
                    context_data.get("stakeholder_mentions", [])
                )
                strategic_initiatives = json.dumps(
                    context_data.get("strategic_topics", [])
                )
                conversation_thread = json.dumps(
                    context_data.get("conversation_thread", [])
                )

                # Calculate quality score based on content
                quality_score = self._calculate_context_quality(context_data)

                conn.execute(
                    """
                    UPDATE session_context
                    SET active_personas = ?, stakeholder_context = ?,
                        strategic_initiatives_context = ?, conversation_thread = ?,
                        context_quality_score = ?, last_backup_timestamp = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                """,
                    (
                        active_personas,
                        stakeholder_context,
                        strategic_initiatives,
                        conversation_thread,
                        quality_score,
                        datetime.now().isoformat(),
                        session_id,
                    ),
                )

                return conn.total_changes > 0

        except Exception as e:
            print(f"❌ Session context update failed: {e}")
            return False

    def _calculate_context_quality(self, context_data: Dict[str, Any]) -> float:
        """Calculate context quality score based on available data"""
        quality_factors = {
            "conversation_turns": min(
                len(context_data.get("conversation_thread", [])) / 10, 1.0
            ),
            "personas_active": min(
                len(context_data.get("active_personas", [])) / 3, 1.0
            ),
            "stakeholder_mentions": min(
                len(context_data.get("stakeholder_mentions", [])) / 5, 1.0
            ),
            "strategic_topics": min(
                len(context_data.get("strategic_topics", [])) / 5, 1.0
            ),
            "decisions_made": min(len(context_data.get("decisions_made", [])) / 3, 1.0),
        }

        return sum(quality_factors.values()) / len(quality_factors)

    def start_session(self, session_type: str = "strategic") -> str:
        """
        Start new session with context tracking
        Returns session_id for reference
        """
        session_id = str(uuid.uuid4())
        self.current_session_id = session_id

        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO session_context
                (session_id, session_type, session_start_timestamp, last_backup_timestamp)
                VALUES (?, ?, ?, ?)
            """,
                (
                    session_id,
                    session_type,
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                ),
            )

        return session_id

    def backup_session_context(self, session_id: str = None) -> bool:
        """
        Backup current session context for recovery
        """
        if not session_id:
            session_id = self.current_session_id

        if not session_id:
            return False

        try:
            # Gather current context
            context = {
                "active_personas": self._get_active_personas(),
                "stakeholder_context": self._get_stakeholder_intelligence(),
                "strategic_initiatives": self._get_active_initiatives(),
                "executive_context": self._get_executive_session_state(),
                "roi_discussions": self._get_roi_discussion_context(),
                "coalition_mapping": self._get_coalition_mapping_context(),
            }

            # Calculate context quality score
            quality_score = self._calculate_context_quality(context)

            # Update session context
            with self.get_connection() as conn:
                conn.execute(
                    """
                    UPDATE session_context
                    SET active_personas = ?, stakeholder_context = ?,
                        strategic_initiatives_context = ?, executive_context = ?,
                        roi_discussions_context = ?, coalition_mapping_context = ?,
                        last_backup_timestamp = ?, context_quality_score = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                """,
                    (
                        json.dumps(context["active_personas"]),
                        json.dumps(context["stakeholder_context"]),
                        json.dumps(context["strategic_initiatives"]),
                        json.dumps(context["executive_context"]),
                        json.dumps(context["roi_discussions"]),
                        json.dumps(context["coalition_mapping"]),
                        datetime.now().isoformat(),
                        quality_score,
                        session_id,
                    ),
                )

            return True

        except Exception as e:
            print(f"Context backup failed: {e}")
            return False

    def detect_session_restart(self) -> bool:
        """
        Detect if this is a session restart requiring context recovery
        """
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT session_id, last_backup_timestamp, context_quality_score
                FROM session_context
                WHERE session_end_timestamp IS NULL
                ORDER BY last_backup_timestamp DESC
                LIMIT 1
            """
            )

            recent_session = cursor.fetchone()

            if recent_session:
                session_id, last_backup, quality_score = recent_session
                last_backup_time = datetime.fromisoformat(last_backup)

                # If last backup was recent and had good quality, likely a restart
                time_since_backup = datetime.now() - last_backup_time
                if time_since_backup < timedelta(hours=2) and quality_score > 0.6:
                    self.current_session_id = session_id
                    return True

            return False

    def restore_session_context(self, session_id: str = None) -> Dict[str, Any]:
        """
        Restore session context from last backup
        """
        if not session_id:
            session_id = self.current_session_id

        if not session_id:
            return {}

        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT active_personas, stakeholder_context, strategic_initiatives_context,
                       executive_context, roi_discussions_context, coalition_mapping_context,
                       context_quality_score
                FROM session_context
                WHERE session_id = ?
            """,
                (session_id,),
            )

            row = cursor.fetchone()
            if not row:
                return {}

            # Parse JSON context data
            context = {}
            fields = [
                "active_personas",
                "stakeholder_context",
                "strategic_initiatives_context",
                "executive_context",
                "roi_discussions_context",
                "coalition_mapping_context",
            ]

            for i, field in enumerate(fields):
                try:
                    context[field] = json.loads(row[i]) if row[i] else {}
                except (json.JSONDecodeError, TypeError):
                    context[field] = {}

            context["quality_score"] = row[6] if row[6] else 0.0

            return context

    def validate_context_completeness(
        self, session_id: str = None
    ) -> List[Dict[str, Any]]:
        """
        Validate current context and identify gaps
        Returns list of context gaps that need resolution
        """
        if not session_id:
            session_id = self.current_session_id

        gaps = []
        context = self.restore_session_context(session_id)

        # Check for critical context gaps
        required_contexts = [
            ("stakeholder_context", "Stakeholder relationship mapping missing"),
            ("strategic_initiatives_context", "Active strategic initiatives unclear"),
            ("executive_context", "Executive session preparation incomplete"),
            ("roi_discussions_context", "ROI strategy conversations missing"),
        ]

        for context_key, description in required_contexts:
            if not context.get(context_key) or not context[context_key]:
                gap = {
                    "type": f"{context_key}_missing",
                    "description": description,
                    "severity": (
                        "high"
                        if "executive" in context_key or "stakeholder" in context_key
                        else "medium"
                    ),
                    "recovery_strategy": self._get_recovery_strategy(context_key),
                }
                gaps.append(gap)

                # Store gap in database
                self._store_context_gap(session_id, gap)

        return gaps

    def get_context_recovery_prompt(self, session_id: str = None) -> str:
        """
        Generate context recovery prompt for user
        """
        gaps = self.validate_context_completeness(session_id)

        if not gaps:
            return "✅ Complete context preserved - ready to continue strategic work."

        prompt = "🔄 **Context Recovery Required**\n\n"
        prompt += "Before continuing strategic work, please refresh the following context:\n\n"

        for i, gap in enumerate(gaps, 1):
            prompt += f"{i}. **{gap['description']}**\n"
            if gap.get("recovery_strategy"):
                prompt += f"   - {gap['recovery_strategy']}\n"
            prompt += "\n"

        prompt += "Please provide the missing context so we can continue effectively."

        return prompt

    def _get_active_personas(self) -> List[str]:
        """Get currently active personas from recent conversations"""
        personas = []

        # Check recent session contexts for persona mentions
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT conversation_thread
                FROM session_context
                WHERE conversation_thread IS NOT NULL
                AND last_backup_timestamp >= datetime('now', '-24 hours')
                ORDER BY last_backup_timestamp DESC
                LIMIT 5
            """
            )

            for row in cursor.fetchall():
                try:
                    if row[0]:
                        conversation_data = json.loads(row[0])
                        if isinstance(conversation_data, list):
                            for turn in conversation_data:
                                if isinstance(turn, dict) and turn.get(
                                    "personas_activated"
                                ):
                                    personas.extend(turn["personas_activated"])
                except (json.JSONDecodeError, TypeError):
                    continue

        # Also detect personas from recent conversation content
        persona_patterns = {
            "diego": ["engineering leadership", "stress-test", "platform strategy"],
            "camille": ["strategic technology", "business alignment", "executive"],
            "rachel": ["design systems", "ux leadership", "user experience"],
            "alvaro": ["platform investment", "roi analysis", "business value"],
            "martin": [
                "platform architecture",
                "technical architecture",
                "evolutionary",
            ],
        }

        # Scan recent conversations for persona indicators
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT conversation_thread
                FROM session_context
                WHERE conversation_thread IS NOT NULL
                AND last_backup_timestamp >= datetime('now', '-7 days')
                ORDER BY last_backup_timestamp DESC
                LIMIT 10
            """
            )

            for row in cursor.fetchall():
                try:
                    if row[0]:
                        conversation_data = json.loads(row[0])
                        if isinstance(conversation_data, list):
                            for turn in conversation_data:
                                if isinstance(turn, dict):
                                    text = f"{turn.get('user_input', '')} {turn.get('assistant_response', '')}".lower()
                                    for persona, keywords in persona_patterns.items():
                                        if any(keyword in text for keyword in keywords):
                                            personas.append(persona)
                except (json.JSONDecodeError, TypeError):
                    continue

        return list(set(personas))  # Remove duplicates

    def _get_stakeholder_intelligence(self) -> Dict[str, Any]:
        """Get current stakeholder relationship context"""
        stakeholders = {}

        # Get recent stakeholder profiles
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT stakeholder_key, display_name, role_title, communication_style
                FROM stakeholder_profiles
                WHERE updated_at >= date('now', '-30 days')
            """
            )

            for row in cursor.fetchall():
                stakeholders[row[0]] = {"name": row[1], "role": row[2], "style": row[3]}

        return stakeholders

    def _get_active_initiatives(self) -> Dict[str, Any]:
        """Get active strategic initiatives context"""
        initiatives = self.recall_strategic_initiatives(status="in_progress")
        initiatives.extend(self.recall_strategic_initiatives(status="at_risk"))

        return {init["initiative_key"]: init for init in initiatives}

    def _get_executive_session_state(self) -> Dict[str, Any]:
        """Get recent executive session context"""
        sessions = self.recall_executive_sessions(days=14)
        return {"recent_sessions": sessions}

    def _get_roi_discussion_context(self) -> Dict[str, Any]:
        """Get ROI discussion context from recent conversations"""
        roi_context = {
            "recent_discussions": [],
            "key_metrics": [],
            "investment_decisions": [],
            "budget_topics": [],
        }

        # ROI-related keywords to detect
        roi_keywords = [
            "roi",
            "return on investment",
            "cost",
            "budget",
            "investment",
            "value",
            "savings",
        ]
        platform_investment_keywords = [
            "platform investment",
            "infrastructure cost",
            "developer productivity",
        ]

        # Scan recent conversations for ROI discussions
        with self.get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT conversation_thread, last_backup_timestamp
                FROM session_context
                WHERE conversation_thread IS NOT NULL
                AND last_backup_timestamp >= datetime('now', '-30 days')
                ORDER BY last_backup_timestamp DESC
                LIMIT 15
            """
            )

            for row in cursor.fetchall():
                try:
                    if row[0]:
                        conversation_data = json.loads(row[0])
                        if isinstance(conversation_data, list):
                            for turn in conversation_data:
                                if isinstance(turn, dict):
                                    text = f"{turn.get('user_input', '')} {turn.get('assistant_response', '')}".lower()

                                    # Check for ROI discussions
                                    if any(keyword in text for keyword in roi_keywords):
                                        roi_context["recent_discussions"].append(
                                            {
                                                "timestamp": row[1],
                                                "summary": (
                                                    text[:200] + "..."
                                                    if len(text) > 200
                                                    else text
                                                ),
                                                "context_type": "roi_discussion",
                                            }
                                        )

                                    # Check for platform investment topics
                                    if any(
                                        keyword in text
                                        for keyword in platform_investment_keywords
                                    ):
                                        roi_context["investment_decisions"].append(
                                            {
                                                "timestamp": row[1],
                                                "topic": "platform_investment",
                                                "discussion_snippet": (
                                                    text[:150] + "..."
                                                    if len(text) > 150
                                                    else text
                                                ),
                                            }
                                        )

                                    # Extract specific metrics mentioned
                                    if (
                                        "efficiency" in text
                                        or "productivity" in text
                                        or "cost savings" in text
                                    ):
                                        roi_context["key_metrics"].append(
                                            {
                                                "timestamp": row[1],
                                                "metric_type": "efficiency_productivity",
                                                "mention": (
                                                    text[:100] + "..."
                                                    if len(text) > 100
                                                    else text
                                                ),
                                            }
                                        )

                except (json.JSONDecodeError, TypeError):
                    continue

        # Also check strategic initiatives for ROI context
        try:
            initiatives = self.recall_strategic_initiatives(status="in_progress")
            for initiative in initiatives:
                if any(
                    keyword in initiative.get("description", "").lower()
                    for keyword in ["roi", "cost", "investment", "budget"]
                ):
                    roi_context["budget_topics"].append(
                        {
                            "initiative": initiative.get("initiative_key"),
                            "roi_context": initiative.get("description", "")[:200],
                        }
                    )
        except Exception:
            pass  # Gracefully handle if initiatives system not available

        return roi_context

    def _get_coalition_mapping_context(self) -> Dict[str, Any]:
        """Get stakeholder coalition mapping context from relationships and interactions"""
        coalition_context = {
            "platform_advocates": [],
            "platform_opponents": [],
            "neutral_stakeholders": [],
            "key_relationships": [],
            "influence_patterns": [],
        }

        # Get stakeholder profiles and analyze relationships
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """
                    SELECT stakeholder_key, display_name, role_title, communication_style,
                           strategic_context, last_interaction_summary
                    FROM stakeholder_profiles
                    WHERE updated_at >= date('now', '-60 days')
                    ORDER BY last_updated DESC
                """
                )

                stakeholders = cursor.fetchall()

                # Analyze each stakeholder for coalition patterns
                for stakeholder in stakeholders:
                    stakeholder_key, name, role, style, context, last_interaction = (
                        stakeholder
                    )

                    # Analyze strategic context and interactions for coalition indicators
                    full_context = f"{context or ''} {last_interaction or ''}".lower()

                    # Platform advocacy indicators
                    platform_positive = any(
                        phrase in full_context
                        for phrase in [
                            "platform investment",
                            "platform advocate",
                            "supports platform",
                            "infrastructure benefits",
                            "technical excellence",
                            "developer productivity",
                        ]
                    )

                    # Platform opposition indicators
                    platform_negative = any(
                        phrase in full_context
                        for phrase in [
                            "product delivery focus",
                            "opposes platform",
                            "product-first",
                            "platform skeptical",
                            "delivery over platform",
                            "anti-platform",
                        ]
                    )

                    # Executive/influence indicators
                    high_influence = (
                        any(
                            phrase in role.lower()
                            for phrase in [
                                "vp",
                                "director",
                                "executive",
                                "chief",
                                "head of",
                            ]
                        )
                        if role
                        else False
                    )

                    stakeholder_data = {
                        "key": stakeholder_key,
                        "name": name,
                        "role": role,
                        "influence_level": "high" if high_influence else "medium",
                        "context_snippet": (
                            full_context[:150] + "..."
                            if len(full_context) > 150
                            else full_context
                        ),
                    }

                    # Categorize into coalitions
                    if platform_positive:
                        coalition_context["platform_advocates"].append(stakeholder_data)
                    elif platform_negative:
                        coalition_context["platform_opponents"].append(stakeholder_data)
                    else:
                        coalition_context["neutral_stakeholders"].append(
                            stakeholder_data
                        )

                # Analyze relationship patterns from conversation history
                cursor = conn.execute(
                    """
                    SELECT conversation_thread, last_backup_timestamp
                    FROM session_context
                    WHERE conversation_thread IS NOT NULL
                    AND last_backup_timestamp >= datetime('now', '-45 days')
                    ORDER BY last_backup_timestamp DESC
                    LIMIT 10
                """
                )

                for row in cursor.fetchall():
                    try:
                        if row[0]:
                            conversation_data = json.loads(row[0])
                            if isinstance(conversation_data, list):
                                for turn in conversation_data:
                                    if isinstance(turn, dict):
                                        text = f"{turn.get('user_input', '')} {turn.get('assistant_response', '')}".lower()

                                        # Look for relationship mentions
                                        if any(
                                            phrase in text
                                            for phrase in [
                                                "stakeholder relationship",
                                                "coalition",
                                                "alliance",
                                                "opposition",
                                                "support",
                                                "resistance",
                                            ]
                                        ):
                                            coalition_context[
                                                "key_relationships"
                                            ].append(
                                                {
                                                    "timestamp": row[1],
                                                    "relationship_context": (
                                                        text[:200] + "..."
                                                        if len(text) > 200
                                                        else text
                                                    ),
                                                }
                                            )

                                        # Detect influence patterns
                                        if any(
                                            phrase in text
                                            for phrase in [
                                                "executive influence",
                                                "decision maker",
                                                "key stakeholder",
                                                "leadership team",
                                                "senior level",
                                            ]
                                        ):
                                            coalition_context[
                                                "influence_patterns"
                                            ].append(
                                                {
                                                    "timestamp": row[1],
                                                    "pattern": (
                                                        text[:150] + "..."
                                                        if len(text) > 150
                                                        else text
                                                    ),
                                                }
                                            )

                    except (json.JSONDecodeError, TypeError):
                        continue

        except Exception:
            # Gracefully handle database issues
            pass

        return coalition_context

    def _calculate_context_quality(self, context: Dict[str, Any]) -> float:
        """Calculate context completeness quality score (0.0-1.0)"""
        total_weight = 0
        weighted_score = 0

        context_weights = {
            "stakeholder_context": 0.25,
            "strategic_initiatives": 0.20,
            "executive_context": 0.20,
            "roi_discussions": 0.15,
            "coalition_mapping": 0.10,
            "active_personas": 0.10,
        }

        for key, weight in context_weights.items():
            total_weight += weight
            if context.get(key) and context[key]:
                weighted_score += weight

        return weighted_score / total_weight if total_weight > 0 else 0.0

    def _get_recovery_strategy(self, context_key: str) -> str:
        """Get recovery strategy for specific context gap"""
        strategies = {
            "stakeholder_context": "Please refresh stakeholder positions and relationship dynamics",
            "strategic_initiatives_context": "Please update status of current strategic initiatives",
            "executive_context": "Please provide recent executive session context and preparations",
            "roi_discussions_context": "Please refresh ROI strategy discussions and current positioning",
        }
        return strategies.get(context_key, "Please provide missing context information")

    def _store_context_gap(self, session_id: str, gap: Dict[str, Any]):
        """Store identified context gap in database"""
        try:
            with self.get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO context_gaps
                    (session_id, gap_type, gap_description, severity, recovery_strategy, detected_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        session_id,
                        gap["type"],
                        gap["description"],
                        gap["severity"],
                        gap.get("recovery_strategy", ""),
                        datetime.now().isoformat(),
                    ),
                )
        except Exception as e:
            print(f"Failed to store context gap: {e}")

    def end_session(self, session_id: str = None):
        """Mark session as ended"""
        if not session_id:
            session_id = self.current_session_id

        if session_id:
            with self.get_connection() as conn:
                conn.execute(
                    """
                    UPDATE session_context
                    SET session_end_timestamp = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                """,
                    (datetime.now().isoformat(), session_id),
                )
