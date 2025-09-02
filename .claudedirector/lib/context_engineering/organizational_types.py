#!/usr/bin/env python3
"""
Organizational Intelligence Type Definitions
Phase 3B.1.1: Extracted from organizational_layer.py for code reduction

🏗️ Martin | Platform Architecture - Type safety and code organization
🤖 Berny | AI/ML Engineering - Systematic type extraction
🎯 Diego | Engineering Leadership - Organizational intelligence types
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
import time


class OrganizationSize(Enum):
    """Organization size classification"""

    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class CulturalDimension(Enum):
    """Cultural dimension classification"""

    HIERARCHICAL = "hierarchical"
    COLLABORATIVE = "collaborative"
    INNOVATIVE = "innovative"
    PROCESS_DRIVEN = "process_driven"
    RESULTS_ORIENTED = "results_oriented"
    CUSTOMER_FOCUSED = "customer_focused"


class ChangeToleranceLevel(Enum):
    """Change tolerance level classification"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CommunicationStyle(Enum):
    """Communication style classification"""

    FORMAL = "formal"
    INFORMAL = "informal"
    BALANCED = "balanced"
    DIRECT = "direct"
    DIPLOMATIC = "diplomatic"


class DecisionMakingStyle(Enum):
    """Decision making style classification"""

    HIERARCHICAL = "hierarchical"
    COLLABORATIVE = "collaborative"
    CONSENSUS = "consensus"
    DELEGATED = "delegated"
    AUTOCRATIC = "autocratic"


class TeamType(Enum):
    """Team type classification"""

    ENGINEERING = "engineering"
    PRODUCT = "product"
    DESIGN = "design"
    MARKETING = "marketing"
    SALES = "sales"
    OPERATIONS = "operations"
    SUPPORT = "support"
    UNKNOWN = "unknown"


@dataclass
class TeamStructure:
    """Team structure information"""

    team_id: str
    team_name: str
    team_type: str  # engineering, product, design, etc.
    size: int
    reporting_structure: str
    collaboration_patterns: List[str]
    communication_frequency: str
    decision_making_style: str
    performance_metrics: Dict[str, float]
    last_updated: float


@dataclass
class OrganizationalChange:
    """Organizational change tracking"""

    change_id: str
    change_type: str  # restructure, process, technology, cultural
    description: str
    impact_areas: List[str]
    stakeholders_affected: List[str]
    success_metrics: Dict[str, float]
    resistance_factors: List[str]
    success_factors: List[str]
    start_date: float
    completion_date: Optional[float]
    effectiveness_score: float
    lessons_learned: List[str]


@dataclass
class OrganizationalProfile:
    """Organizational profile data structure"""

    organization_name: str
    organization_size: str
    industry: str
    cultural_dimensions: List[str]
    primary_values: List[str]
    communication_style: str
    decision_making_approach: str
    change_tolerance: str
    innovation_focus: str
    risk_tolerance: str
    hierarchy_level: str
    geographic_distribution: str
    remote_work_adoption: str
    technology_maturity: str
    learning_orientation: str
    performance_focus: str
    last_updated: float


@dataclass
class CulturalObservation:
    """Cultural observation data structure"""

    observation_id: str
    observation_type: str
    description: str
    evidence: List[str]
    confidence_level: float
    timestamp: float
    impact_assessment: str


@dataclass
class KnowledgeArtifact:
    """Knowledge artifact data structure"""

    artifact_id: str
    title: str
    content: str
    artifact_type: str  # decision, process, lesson, guideline
    tags: List[str]
    stakeholders: List[str]
    related_initiatives: List[str]
    importance_level: str
    created_date: float
    last_accessed: float
    access_count: int


@dataclass
class OrganizationalRecommendation:
    """Organizational improvement recommendation"""

    recommendation_id: str
    recommendation_type: str
    priority: str  # high, medium, low
    title: str
    description: str
    action_items: List[str]
    expected_impact: str
    implementation_effort: str
    success_metrics: List[str]
    created_date: float


@dataclass
class OrganizationalHealthMetrics:
    """Organizational health assessment metrics"""

    overall_health_score: float
    team_health_contribution: float
    change_effectiveness_contribution: float
    cultural_alignment_score: float
    health_status: str  # healthy, needs_attention, at_risk
    assessment_date: float
    improvement_areas: List[str]
    strengths: List[str]


# Type aliases for improved code readability
OrganizationalContext = Dict[str, Any]
TeamMetrics = Dict[str, float]
ChangeMetrics = Dict[str, Any]
CulturalPatterns = List[Dict[str, Any]]

# Constants for organizational intelligence
DEFAULT_TEAM_SIZE_THRESHOLD = 10
DEFAULT_CHANGE_RETENTION_DAYS = 730  # 2 years
DEFAULT_MAX_TEAM_HISTORY = 50
DEFAULT_MAX_CULTURAL_OBSERVATIONS = 1000
DEFAULT_MAX_KNOWLEDGE_ARTIFACTS = 1000

# Performance and quality thresholds
HIGH_PERFORMANCE_THRESHOLD = 0.8
MEDIUM_PERFORMANCE_THRESHOLD = 0.6
HIGH_EFFECTIVENESS_THRESHOLD = 0.7
MEDIUM_EFFECTIVENESS_THRESHOLD = 0.5
