"""
Clarity Measurement System for Next Action Clarity Framework

Tracks and reports Next Action Clarity Rate metrics.
"""

import json
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path
from .models import (
    ClarityMetrics,
    ClarityReport,
    ClarityTrend,
    ActionType,
    StuckPattern,
    CLARITY_METRICS_SCHEMA,
)


class ClarityMeasurementSystem:
    """Tracks and reports Next Action Clarity Rate metrics"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # Default to data directory
            data_dir = Path(__file__).parent.parent.parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "strategic_memory.db")

        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database with clarity metrics schema"""
        conn = sqlite3.connect(self.db_path)
        try:
            # First create conversations table if it doesn't exist
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

            # Execute clarity metrics schema
            conn.executescript(CLARITY_METRICS_SCHEMA)
            conn.commit()
        finally:
            conn.close()

    def record_conversation_outcome(
        self, conversation_id: str, clarity_metrics: ClarityMetrics
    ):
        """Record clarity metrics for a conversation"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO clarity_metrics (
                    conversation_id, clarity_score, action_items_json,
                    clarity_indicators_json, stuck_patterns_json,
                    time_to_clarity, decision_frameworks_used,
                    persona_effectiveness_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    conversation_id,
                    clarity_metrics.clarity_score,
                    json.dumps(
                        [
                            {
                                "text": action.text,
                                "action_type": action.action_type.value,
                                "specificity_score": action.specificity_score,
                                "timeline": action.timeline,
                                "responsible_party": action.responsible_party,
                                "confidence": action.confidence,
                            }
                            for action in clarity_metrics.action_items
                        ]
                    ),
                    json.dumps(
                        [
                            {
                                "type": indicator.type,
                                "text": indicator.text,
                                "confidence": indicator.confidence,
                                "pattern": indicator.pattern,
                            }
                            for indicator in clarity_metrics.clarity_indicators
                        ]
                    ),
                    json.dumps(
                        [
                            {
                                "pattern_type": pattern.pattern_type,
                                "description": pattern.description,
                                "severity": pattern.severity,
                                "intervention_suggestion": pattern.intervention_suggestion,
                            }
                            for pattern in clarity_metrics.stuck_patterns
                        ]
                    ),
                    clarity_metrics.time_to_clarity,
                    json.dumps(clarity_metrics.decision_frameworks_used),
                    json.dumps(clarity_metrics.persona_effectiveness),
                ),
            )
            conn.commit()

    def calculate_clarity_rate(self, time_period: str = "30d") -> float:
        """Calculate Next Action Clarity Rate for a time period"""
        start_date = self._parse_time_period(time_period)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT
                    COUNT(*) as total_conversations,
                    SUM(CASE WHEN clarity_score >= 0.85 THEN 1 ELSE 0 END) as clear_conversations
                FROM clarity_metrics
                WHERE created_at >= ?
            """,
                (start_date,),
            )

            result = cursor.fetchone()
            total, clear = result[0], result[1]

            if total == 0:
                return 0.0

            return round(clear / total, 3)

    def generate_clarity_report(
        self, time_period: str = "30d", include_trends: bool = True
    ) -> ClarityReport:
        """Generate comprehensive clarity analytics report"""
        start_date = self._parse_time_period(time_period)

        with sqlite3.connect(self.db_path) as conn:
            # Overall metrics
            cursor = conn.execute(
                """
                SELECT
                    COUNT(*) as total_conversations,
                    AVG(clarity_score) as avg_clarity_score,
                    SUM(CASE WHEN clarity_score >= 0.85 THEN 1 ELSE 0 END) as clear_conversations,
                    AVG(time_to_clarity) as avg_time_to_clarity,
                    SUM(CASE WHEN stuck_patterns_json != '[]' THEN 1 ELSE 0 END) as conversations_with_stuck_patterns
                FROM clarity_metrics
                WHERE created_at >= ?
            """,
                (start_date,),
            )

            overall_result = cursor.fetchone()
            total_conversations = overall_result[0]
            avg_clarity_score = round(overall_result[1] or 0.0, 3)
            clear_conversations = overall_result[2]
            avg_time_to_clarity = overall_result[3]
            conversations_requiring_intervention = overall_result[4]

            clarity_rate = (
                (clear_conversations / total_conversations)
                if total_conversations > 0
                else 0.0
            )

            # Persona effectiveness
            clarity_by_persona = self._calculate_persona_effectiveness(conn, start_date)

            # Framework effectiveness
            clarity_by_framework = self._calculate_framework_effectiveness(
                conn, start_date
            )

            # Action type distribution
            action_type_distribution = self._calculate_action_type_distribution(
                conn, start_date
            )

            # Trends
            trends = []
            if include_trends:
                trends = self._calculate_clarity_trends(conn, start_date)

            # Top stuck patterns
            top_stuck_patterns = self._get_top_stuck_patterns(conn, start_date)

            # Improvement recommendations
            improvement_recommendations = self._generate_improvement_recommendations(
                clarity_rate, avg_clarity_score, top_stuck_patterns
            )

            return ClarityReport(
                report_id=f"clarity_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                generated_at=datetime.now(),
                time_period=time_period,
                total_conversations=total_conversations,
                average_clarity_score=avg_clarity_score,
                clarity_rate=clarity_rate,
                clarity_by_persona=clarity_by_persona,
                clarity_by_framework=clarity_by_framework,
                action_type_distribution=action_type_distribution,
                trends=trends,
                top_stuck_patterns=top_stuck_patterns,
                improvement_recommendations=improvement_recommendations,
                average_time_to_clarity=avg_time_to_clarity,
                conversations_requiring_intervention=conversations_requiring_intervention,
            )

    def track_clarity_trends(self, days: int = 30) -> List[ClarityTrend]:
        """Track clarity trends over time"""
        with sqlite3.connect(self.db_path) as conn:
            return self._calculate_clarity_trends(
                conn, datetime.now() - timedelta(days=days)
            )

    def get_conversation_clarity(
        self, conversation_id: str
    ) -> Optional[ClarityMetrics]:
        """Get clarity metrics for a specific conversation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT * FROM clarity_metrics WHERE conversation_id = ?
            """,
                (conversation_id,),
            )

            result = cursor.fetchone()
            if not result:
                return None

            # Reconstruct ClarityMetrics from database row
            # This is a simplified version - in production, you'd want proper deserialization
            return ClarityMetrics(
                conversation_id=result[1],
                clarity_score=result[2],
                action_items=[],  # Would deserialize from JSON
                clarity_indicators=[],  # Would deserialize from JSON
                stuck_patterns=[],  # Would deserialize from JSON
                time_to_clarity=result[5],
                decision_frameworks_used=json.loads(result[6] or "[]"),
                persona_effectiveness=json.loads(result[7] or "{}"),
            )

    def _parse_time_period(self, time_period: str) -> datetime:
        """Parse time period string to datetime"""
        if time_period.endswith("d"):
            days = int(time_period[:-1])
            return datetime.now() - timedelta(days=days)
        elif time_period.endswith("w"):
            weeks = int(time_period[:-1])
            return datetime.now() - timedelta(weeks=weeks)
        elif time_period.endswith("m"):
            months = int(time_period[:-1])
            return datetime.now() - timedelta(days=months * 30)
        else:
            raise ValueError(f"Invalid time period format: {time_period}")

    def _calculate_persona_effectiveness(
        self, conn: sqlite3.Connection, start_date: datetime
    ) -> Dict[str, float]:
        """Calculate clarity effectiveness by persona"""
        cursor = conn.execute(
            """
            SELECT persona_effectiveness_json, clarity_score
            FROM clarity_metrics
            WHERE created_at >= ? AND persona_effectiveness_json IS NOT NULL
        """,
            (start_date,),
        )

        persona_scores = {}
        persona_counts = {}

        for row in cursor.fetchall():
            try:
                persona_data = json.loads(row[0])
                clarity_score = row[1]

                for persona, effectiveness in persona_data.items():
                    if persona not in persona_scores:
                        persona_scores[persona] = 0.0
                        persona_counts[persona] = 0

                    # Weight persona effectiveness by conversation clarity
                    persona_scores[persona] += effectiveness * clarity_score
                    persona_counts[persona] += 1
            except (json.JSONDecodeError, TypeError):
                continue

        # Calculate averages
        return {
            persona: round(persona_scores[persona] / persona_counts[persona], 3)
            for persona in persona_scores
            if persona_counts[persona] > 0
        }

    def _calculate_framework_effectiveness(
        self, conn: sqlite3.Connection, start_date: datetime
    ) -> Dict[str, float]:
        """Calculate clarity effectiveness by framework"""
        cursor = conn.execute(
            """
            SELECT decision_frameworks_used, clarity_score
            FROM clarity_metrics
            WHERE created_at >= ? AND decision_frameworks_used IS NOT NULL
        """,
            (start_date,),
        )

        framework_scores = {}
        framework_counts = {}

        for row in cursor.fetchall():
            try:
                frameworks = json.loads(row[0])
                clarity_score = row[1]

                for framework in frameworks:
                    if framework not in framework_scores:
                        framework_scores[framework] = 0.0
                        framework_counts[framework] = 0

                    framework_scores[framework] += clarity_score
                    framework_counts[framework] += 1
            except (json.JSONDecodeError, TypeError):
                continue

        return {
            framework: round(
                framework_scores[framework] / framework_counts[framework], 3
            )
            for framework in framework_scores
            if framework_counts[framework] > 0
        }

    def _calculate_action_type_distribution(
        self, conn: sqlite3.Connection, start_date: datetime
    ) -> Dict[ActionType, int]:
        """Calculate distribution of action types"""
        cursor = conn.execute(
            """
            SELECT action_items_json
            FROM clarity_metrics
            WHERE created_at >= ? AND action_items_json IS NOT NULL
        """,
            (start_date,),
        )

        action_counts = {action_type: 0 for action_type in ActionType}

        for row in cursor.fetchall():
            try:
                actions = json.loads(row[0])
                for action in actions:
                    action_type = ActionType(
                        action.get("action_type", "task_assignment")
                    )
                    action_counts[action_type] += 1
            except (json.JSONDecodeError, TypeError, ValueError):
                continue

        return action_counts

    def _calculate_clarity_trends(
        self, conn: sqlite3.Connection, start_date: datetime
    ) -> List[ClarityTrend]:
        """Calculate clarity trends over time"""
        cursor = conn.execute(
            """
            SELECT
                DATE(created_at) as date,
                COUNT(*) as total_conversations,
                AVG(clarity_score) as avg_clarity_score,
                SUM(CASE WHEN clarity_score >= 0.85 THEN 1 ELSE 0 END) as clear_conversations
            FROM clarity_metrics
            WHERE created_at >= ?
            GROUP BY DATE(created_at)
            ORDER BY date
        """,
            (start_date,),
        )

        trends = []
        for row in cursor.fetchall():
            date_str = row[0]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            total = row[1]
            avg_score = row[2]
            clear_convs = row[3]
            clarity_rate = clear_convs / total if total > 0 else 0.0

            trends.append(
                ClarityTrend(
                    period="daily",
                    start_date=date_obj,
                    end_date=date_obj + timedelta(days=1),
                    average_clarity_score=round(avg_score, 3),
                    total_conversations=total,
                    conversations_with_clear_actions=clear_convs,
                    clarity_rate=round(clarity_rate, 3),
                )
            )

        return trends

    def _get_top_stuck_patterns(
        self, conn: sqlite3.Connection, start_date: datetime, limit: int = 5
    ) -> List[StuckPattern]:
        """Get most common stuck patterns"""
        cursor = conn.execute(
            """
            SELECT stuck_patterns_json
            FROM clarity_metrics
            WHERE created_at >= ? AND stuck_patterns_json IS NOT NULL AND stuck_patterns_json != '[]'
        """,
            (start_date,),
        )

        pattern_counts = {}

        for row in cursor.fetchall():
            try:
                patterns = json.loads(row[0])
                for pattern_data in patterns:
                    pattern_type = pattern_data.get("pattern_type")
                    if pattern_type:
                        if pattern_type not in pattern_counts:
                            pattern_counts[pattern_type] = {
                                "count": 0,
                                "total_severity": 0.0,
                                "description": pattern_data.get("description", ""),
                                "intervention": pattern_data.get(
                                    "intervention_suggestion", ""
                                ),
                            }
                        pattern_counts[pattern_type]["count"] += 1
                        pattern_counts[pattern_type][
                            "total_severity"
                        ] += pattern_data.get("severity", 0.0)
            except (json.JSONDecodeError, TypeError):
                continue

        # Sort by frequency and create StuckPattern objects
        top_patterns = []
        for pattern_type, data in sorted(
            pattern_counts.items(), key=lambda x: x[1]["count"], reverse=True
        )[:limit]:
            avg_severity = (
                data["total_severity"] / data["count"] if data["count"] > 0 else 0.0
            )
            top_patterns.append(
                StuckPattern(
                    pattern_type=pattern_type,
                    description=f"{data['description']} (occurred {data['count']} times)",
                    severity=round(avg_severity, 2),
                    intervention_suggestion=data["intervention"],
                )
            )

        return top_patterns

    def _generate_improvement_recommendations(
        self,
        clarity_rate: float,
        avg_clarity_score: float,
        stuck_patterns: List[StuckPattern],
    ) -> List[str]:
        """Generate recommendations for improving clarity"""
        recommendations = []

        # Clarity rate recommendations
        if clarity_rate < 0.85:
            recommendations.append(
                f"Current clarity rate ({clarity_rate:.1%}) is below target (85%). "
                "Focus on action-oriented responses and decision frameworks."
            )

        # Average clarity score recommendations
        if avg_clarity_score < 0.7:
            recommendations.append(
                f"Average clarity score ({avg_clarity_score:.2f}) indicates conversations "
                "need more specific, actionable outcomes."
            )

        # Stuck pattern recommendations
        if stuck_patterns:
            top_pattern = stuck_patterns[0]
            recommendations.append(
                f"Most common stuck pattern: {top_pattern.pattern_type}. "
                f"Recommendation: {top_pattern.intervention_suggestion}"
            )

        # General recommendations
        if not recommendations:
            recommendations.append(
                "Clarity metrics are performing well. Continue focusing on "
                "specific, actionable outcomes in strategic conversations."
            )

        return recommendations
