"""
Data models for Next Action Clarity Framework
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ActionType(Enum):
    """Types of actions that can be identified in strategic conversations"""

    DECISION = "decision"
    TASK_ASSIGNMENT = "task_assignment"
    MEETING_SCHEDULING = "meeting_scheduling"
    RESOURCE_ALLOCATION = "resource_allocation"
    STAKEHOLDER_ENGAGEMENT = "stakeholder_engagement"
    ANALYSIS_REQUEST = "analysis_request"
    PROCESS_CHANGE = "process_change"
    INVESTMENT_DECISION = "investment_decision"
    COMMUNICATION = "communication"
    TIMELINE_COMMITMENT = "timeline_commitment"


@dataclass
class ActionItem:
    """Represents a specific actionable item identified in conversation"""

    text: str
    action_type: ActionType
    specificity_score: float  # 0.0 to 1.0, higher = more specific
    timeline: Optional[str] = None
    responsible_party: Optional[str] = None
    dependencies: List[str] = None
    confidence: float = 0.0  # AI confidence in action detection

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class ClarityIndicator:
    """Indicators that suggest conversation clarity or lack thereof"""

    type: str  # "positive", "negative", "neutral"
    text: str
    confidence: float
    pattern: str  # The pattern that matched this indicator


@dataclass
class StuckPattern:
    """Patterns that indicate user is stuck in analysis without action"""

    pattern_type: str
    description: str
    severity: float  # 0.0 to 1.0, higher = more concerning
    intervention_suggestion: str


@dataclass
class ClarityMetrics:
    """Comprehensive clarity metrics for a conversation"""

    conversation_id: str
    clarity_score: float  # 0.0 to 1.0, higher = clearer next actions
    action_items: List[ActionItem]
    clarity_indicators: List[ClarityIndicator]
    stuck_patterns: List[StuckPattern]
    time_to_clarity: Optional[int] = None  # seconds
    decision_frameworks_used: List[str] = None
    persona_effectiveness: Dict[str, float] = None

    def __post_init__(self):
        if self.decision_frameworks_used is None:
            self.decision_frameworks_used = []
        if self.persona_effectiveness is None:
            self.persona_effectiveness = {}

    @property
    def has_clear_actions(self) -> bool:
        """Returns True if conversation has clear, actionable next steps"""
        return (
            self.clarity_score >= 0.85
            and len(self.action_items) > 0
            and any(action.specificity_score >= 0.7 for action in self.action_items)
        )

    @property
    def action_count(self) -> int:
        """Number of actionable items identified"""
        return len(self.action_items)

    @property
    def high_confidence_actions(self) -> List[ActionItem]:
        """Actions with high confidence scores (>0.8)"""
        return [action for action in self.action_items if action.confidence >= 0.8]


@dataclass
class ConversationMessage:
    """Represents a single message in a conversation"""

    content: str
    timestamp: datetime
    speaker: str  # "user" or persona name
    message_type: str = "text"  # "text", "system", "framework_application"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Conversation:
    """Represents a complete strategic conversation"""

    id: str
    messages: List[ConversationMessage]
    start_time: datetime
    end_time: Optional[datetime] = None
    user_id: str = "default"
    topic: Optional[str] = None
    strategic_context: Dict[str, Any] = None

    def __post_init__(self):
        if self.strategic_context is None:
            self.strategic_context = {}

    @property
    def duration_seconds(self) -> Optional[int]:
        """Duration of conversation in seconds"""
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds())
        return None

    @property
    def message_count(self) -> int:
        """Total number of messages in conversation"""
        return len(self.messages)

    @property
    def user_messages(self) -> List[ConversationMessage]:
        """Only user messages (not persona responses)"""
        return [msg for msg in self.messages if msg.speaker == "user"]


@dataclass
class ClarityTrend:
    """Represents clarity trends over time"""

    period: str  # "daily", "weekly", "monthly"
    start_date: datetime
    end_date: datetime
    average_clarity_score: float
    total_conversations: int
    conversations_with_clear_actions: int
    clarity_rate: float
    improvement_from_previous: Optional[float] = None


@dataclass
class ClarityReport:
    """Comprehensive clarity analytics report"""

    report_id: str
    generated_at: datetime
    time_period: str

    # Overall metrics
    total_conversations: int
    average_clarity_score: float
    clarity_rate: float  # % of conversations achieving clear actions

    # Detailed breakdowns
    clarity_by_persona: Dict[str, float]
    clarity_by_framework: Dict[str, float]
    action_type_distribution: Dict[ActionType, int]

    # Trends and patterns
    trends: List[ClarityTrend]
    top_stuck_patterns: List[StuckPattern]
    improvement_recommendations: List[str]

    # Performance metrics
    average_time_to_clarity: Optional[float] = None
    conversations_requiring_intervention: int = 0

    def __post_init__(self):
        # Calculate clarity rate if not provided
        if self.total_conversations > 0:
            self.clarity_rate = (
                sum(
                    1
                    for trend in self.trends
                    if trend.conversations_with_clear_actions > 0
                )
                / len(self.trends)
                if self.trends
                else 0.0
            )


# Database schema constants
CLARITY_METRICS_SCHEMA = """
CREATE TABLE IF NOT EXISTS clarity_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    clarity_score REAL NOT NULL,
    action_items_json TEXT,  -- JSON serialized ActionItem list
    clarity_indicators_json TEXT,  -- JSON serialized ClarityIndicator list
    stuck_patterns_json TEXT,  -- JSON serialized StuckPattern list
    time_to_clarity INTEGER,
    decision_frameworks_used TEXT,  -- JSON array
    persona_effectiveness_json TEXT,  -- JSON dict
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_clarity_conversation_id ON clarity_metrics(conversation_id);
CREATE INDEX IF NOT EXISTS idx_clarity_score ON clarity_metrics(clarity_score);
CREATE INDEX IF NOT EXISTS idx_clarity_created_at ON clarity_metrics(created_at);
"""
