"""
Core Data Models for ClaudeDirector

Provides base data models and exceptions used across the system.
Follows SOLID principles with clear separation of concerns.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class ValidationError(Exception):
    """Validation error for input validation"""

    pass


@dataclass
class StrategicContext:
    """Strategic context for decision making and analysis"""

    stakeholders: List[str] = None
    frameworks: List[str] = None
    constraints: List[str] = None
    objectives: List[str] = None
    timeline: Optional[str] = None
    budget: Optional[float] = None
    risk_tolerance: str = "medium"
    success_metrics: List[str] = None

    # PHASE 8.4: P0 compatibility fields for test interface
    organizational_context: Optional[str] = None
    strategic_objectives: List[str] = None
    stakeholder_priorities: Dict[str, str] = None

    def __post_init__(self):
        # Initialize default empty lists
        if self.stakeholders is None:
            self.stakeholders = []
        if self.frameworks is None:
            self.frameworks = []
        if self.constraints is None:
            self.constraints = []
        if self.objectives is None:
            self.objectives = []
        if self.success_metrics is None:
            self.success_metrics = []
        if self.strategic_objectives is None:
            self.strategic_objectives = []
        if self.stakeholder_priorities is None:
            self.stakeholder_priorities = {}


# BLOAT_PREVENTION: Centralized Jira data models (extracted from weekly_reporter.py)
@dataclass
class JiraIssue:
    """Data class for Jira issue representation"""

    key: str
    summary: str
    status: str
    priority: str
    project: str
    assignee: str
    parent_key: Optional[str] = None
    watchers: int = 0
    links: int = 0
    business_value: str = ""
    # Phase 2 Enhancement: Cycle time fields for Monte Carlo forecasting
    cycle_time_days: Optional[float] = None
    created_date: Optional[str] = None
    resolved_date: Optional[str] = None
    in_progress_date: Optional[str] = None


@dataclass
class StrategicScore:
    """Data class for strategic impact scoring"""

    score: int = 0
    indicators: List[str] = field(default_factory=list)

    def add_score(self, points: int, indicator: str):
        self.score += points
        self.indicators.append(indicator)


@dataclass
class Initiative:
    """Data class for L0/L2 strategic initiatives"""

    key: str
    title: str
    level: str  # L0, L1, L2
    progress_pct: int = 0
    status_desc: str = ""  # "releasing this week", "60% complete"
    business_context: str = ""
    team_impact: str = ""  # "minimal impact to teams"
    decision: Optional[str] = None
    project: str = ""
    status: str = ""
    child_stories: List["JiraIssue"] = field(default_factory=list)


@dataclass
class DecisionContext:
    """Context for strategic decision making"""

    decision_type: str
    urgency: str
    impact_scope: str
    stakeholders_affected: List[str]
    resources_required: Dict[str, Any]
    constraints: Dict[str, Any]
    alternatives: List[str]


@dataclass
class FrameworkApplication:
    """Framework application result"""

    framework_name: str
    confidence: float
    applicability: str
    recommendations: List[str]
    evidence: List[str]


@dataclass
class AnalysisResult:
    """Generic analysis result"""

    success: bool
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    errors: List[str]
    warnings: List[str]


class Priority(Enum):
    """Priority levels for tasks and decisions"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(Enum):
    """Status values for processes and tasks"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
