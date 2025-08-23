"""
P0 Features Configuration Management

Martin's SOLID-compliant configuration system eliminating hard-coded strings.
Centralized, type-safe, environment-aware configuration for all P0 components.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import os
import yaml
from pydantic import BaseModel, validator, Field


class EnvironmentType(str, Enum):
    """Deployment environment types"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class AIModelType(str, Enum):
    """Supported AI model types"""

    DECISION_INTELLIGENCE = "decision_intelligence"
    HEALTH_PREDICTION = "health_prediction"
    PATTERN_RECOGNITION = "pattern_recognition"


class HealthStatus(str, Enum):
    """Standard health status levels"""

    EXCELLENT = "excellent"
    HEALTHY = "healthy"
    AT_RISK = "at_risk"
    FAILING = "failing"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    """Standard risk levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PriorityLevel(str, Enum):
    """Priority levels for recommendations"""

    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DecisionLifecycle(str, Enum):
    """Decision lifecycle stages"""

    IDENTIFIED = "identified"
    ANALYZED = "analyzed"
    DECIDED = "decided"
    IMPLEMENTED = "implemented"


class DecisionType(str, Enum):
    """Decision classification types"""

    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    TECHNICAL = "technical"
    ORGANIZATIONAL = "organizational"
    FINANCIAL = "financial"
    GENERAL = "general"


@dataclass(frozen=True)
class PerformanceThresholds:
    """Performance SLA thresholds"""

    max_inference_time_ms: int = 200
    min_accuracy: float = 0.85
    max_memory_usage_mb: int = 150
    max_error_rate: float = 0.05


@dataclass(frozen=True)
class HealthScoringWeights:
    """Health scoring component weights (must sum to 1.0)"""

    progress_completion: float = 0.25
    stakeholder_engagement: float = 0.20
    milestone_completion: float = 0.20
    budget_health: float = 0.15
    timeline_adherence: float = 0.10
    risk_indicators: float = 0.10

    def __post_init__(self):
        """Validate weights sum to 1.0"""
        total = (
            self.progress_completion
            + self.stakeholder_engagement
            + self.milestone_completion
            + self.budget_health
            + self.timeline_adherence
            + self.risk_indicators
        )
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Health scoring weights must sum to 1.0, got {total}")


@dataclass(frozen=True)
class HealthStatusThresholds:
    """Health status classification thresholds"""

    excellent: float = 0.85
    healthy: float = 0.70
    at_risk: float = 0.50
    failing: float = 0.30


@dataclass(frozen=True)
class RiskIndicatorWeights:
    """Risk indicator impact weights"""

    # High impact risks
    budget_overrun: float = 0.20
    stakeholder_disengagement: float = 0.18
    scope_creep: float = 0.15
    resource_constraints: float = 0.12

    # Medium impact risks
    technical_blockers: float = 0.10
    timeline_delays: float = 0.08
    quality_issues: float = 0.07

    # Low impact risks
    external_dependencies: float = 0.05
    team_turnover: float = 0.05

    def get_weight(self, risk_indicator: str) -> float:
        """Get weight for a risk indicator"""
        return getattr(self, risk_indicator, 0.05)  # Default weight

    def get_risk_category(self, risk_indicator: str) -> str:
        """Categorize risk by impact level"""
        weight = self.get_weight(risk_indicator)
        if weight >= 0.15:
            return "high_impact"
        elif weight >= 0.08:
            return "medium_impact"
        else:
            return "low_impact"


class DecisionDetectionConfig(BaseModel):
    """Configuration for decision detection AI"""

    model_name: str = "decision_intelligence_v1"
    accuracy_threshold: float = Field(0.85, ge=0.0, le=1.0)
    confidence_threshold: float = Field(0.60, ge=0.0, le=1.0)
    max_inference_time_ms: int = Field(200, gt=0)

    # Decision type classification keywords
    classification_keywords: Dict[DecisionType, List[str]] = Field(
        default_factory=lambda: {
            DecisionType.STRATEGIC: [
                "vision",
                "strategy",
                "roadmap",
                "architecture",
                "investment",
            ],
            DecisionType.OPERATIONAL: ["process", "workflow", "procedure", "policy"],
            DecisionType.TECHNICAL: [
                "technology",
                "platform",
                "system",
                "infrastructure",
            ],
            DecisionType.ORGANIZATIONAL: ["team", "hiring", "structure", "role"],
            DecisionType.FINANCIAL: ["budget", "cost", "investment", "funding"],
        }
    )

    # Lifecycle detection patterns
    lifecycle_patterns: Dict[DecisionLifecycle, List[str]] = Field(
        default_factory=lambda: {
            DecisionLifecycle.IDENTIFIED: ["proposed", "considering", "evaluating"],
            DecisionLifecycle.ANALYZED: ["analyzing", "reviewing", "discussing"],
            DecisionLifecycle.DECIDED: ["decided", "approved", "chosen", "selected"],
            DecisionLifecycle.IMPLEMENTED: ["implementing", "executing", "started"],
        }
    )

    # Urgency classification
    urgency_keywords: Dict[PriorityLevel, List[str]] = Field(
        default_factory=lambda: {
            PriorityLevel.URGENT: ["urgent", "critical", "immediate", "asap"],
            PriorityLevel.HIGH: [
                "critical",
                "major",
                "significant",
                "strategic",
                "enterprise",
            ],
            PriorityLevel.MEDIUM: ["important", "moderate", "substantial"],
            PriorityLevel.LOW: ["minor", "small", "limited"],
        }
    )


class HealthPredictionConfig(BaseModel):
    """Configuration for health prediction AI"""

    model_name: str = "health_prediction_v1"
    accuracy_threshold: float = Field(0.80, ge=0.0, le=1.0)
    max_inference_time_ms: int = Field(200, gt=0)

    # Component scoring weights
    scoring_weights: HealthScoringWeights = Field(default_factory=HealthScoringWeights)

    # Status thresholds
    status_thresholds: HealthStatusThresholds = Field(
        default_factory=HealthStatusThresholds
    )

    # Risk indicator weights
    risk_weights: RiskIndicatorWeights = Field(default_factory=RiskIndicatorWeights)

    # Optimal budget utilization range
    optimal_budget_range: tuple[float, float] = Field((0.70, 0.80))

    # Confidence calculation parameters
    base_confidence: float = Field(0.85, ge=0.0, le=1.0)
    missing_field_penalty: float = Field(0.05, ge=0.0, le=1.0)
    extreme_value_penalty: float = Field(0.02, ge=0.0, le=1.0)


class RecommendationConfig(BaseModel):
    """Configuration for recommendation generation"""

    max_recommendations: int = Field(5, gt=0)

    # Recommendation templates by category
    templates: Dict[str, Dict[str, List[str]]] = Field(
        default_factory=lambda: {
            "stakeholder_engagement": {
                "descriptions": [
                    "Schedule stakeholder alignment sessions",
                    "Improve communication frequency with key stakeholders",
                    "Address stakeholder concerns proactively",
                ],
                "action_items": [
                    "Review current stakeholder engagement metrics",
                    "Develop improvement plan for stakeholder engagement",
                    "Monitor stakeholder engagement progress weekly",
                ],
            },
            "timeline_management": {
                "descriptions": [
                    "Review and adjust project timeline",
                    "Identify critical path dependencies",
                    "Consider scope reduction to meet deadlines",
                ],
                "action_items": [
                    "Review current timeline management metrics",
                    "Develop improvement plan for timeline management",
                    "Monitor timeline management progress weekly",
                ],
            },
            "budget_management": {
                "descriptions": [
                    "Conduct budget review and reforecasting",
                    "Identify cost optimization opportunities",
                    "Escalate budget variance to leadership",
                ],
                "action_items": [
                    "Review current budget management metrics",
                    "Develop improvement plan for budget management",
                    "Monitor budget management progress weekly",
                ],
            },
            "risk_mitigation": {
                "descriptions": [
                    "Develop comprehensive risk mitigation plan",
                    "Increase monitoring frequency for high-risk areas",
                    "Establish contingency plans for critical risks",
                ],
                "action_items": [
                    "Review current risk mitigation metrics",
                    "Develop improvement plan for risk mitigation",
                    "Monitor risk mitigation progress weekly",
                ],
            },
            "resource_optimization": {
                "descriptions": [
                    "Assess resource allocation and utilization",
                    "Consider additional resource allocation",
                    "Optimize team structure and responsibilities",
                ],
                "action_items": [
                    "Review current resource optimization metrics",
                    "Develop improvement plan for resource optimization",
                    "Monitor resource optimization progress weekly",
                ],
            },
        }
    )


class DatabaseConfig(BaseModel):
    """Database configuration"""

    connection_timeout: int = Field(30, gt=0)
    query_timeout: int = Field(10, gt=0)
    max_connections: int = Field(10, gt=0)

    # SQLite optimization settings
    sqlite_config: Dict[str, Any] = Field(
        default_factory=lambda: {
            "journal_mode": "WAL",
            "synchronous": "NORMAL",
            "cache_size": 10000,  # 10MB cache
            "mmap_size": 268435456,  # 256MB mmap
            "temp_store": "MEMORY",
        }
    )


class MonitoringConfig(BaseModel):
    """Performance monitoring configuration"""

    enable_performance_tracking: bool = True
    enable_accuracy_tracking: bool = True
    metrics_retention_days: int = Field(30, gt=0)
    alert_on_sla_violation: bool = True
    performance_sample_rate: float = Field(1.0, ge=0.0, le=1.0)


class P0FeatureConfig(BaseModel):
    """Master configuration for all P0 features"""

    # Environment settings
    environment: EnvironmentType = EnvironmentType.DEVELOPMENT
    debug_mode: bool = True

    # Feature flags
    enable_decision_intelligence: bool = True
    enable_health_prediction: bool = True
    enable_pattern_recognition: bool = False  # P1 feature

    # Component configurations
    decision_detection: DecisionDetectionConfig = Field(
        default_factory=DecisionDetectionConfig
    )
    health_prediction: HealthPredictionConfig = Field(
        default_factory=HealthPredictionConfig
    )
    recommendations: RecommendationConfig = Field(default_factory=RecommendationConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)

    # Global performance thresholds
    performance: PerformanceThresholds = Field(default_factory=PerformanceThresholds)

    @validator("environment")
    def validate_environment(cls, v):
        """Validate environment-specific settings"""
        if v == EnvironmentType.PRODUCTION:
            # Production should have stricter settings
            pass
        return v

    @classmethod
    def load_from_file(cls, config_path: Path) -> "P0FeatureConfig":
        """Load configuration from YAML file"""
        if not config_path.exists():
            return cls()  # Return defaults

        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)

        return cls(**config_data)

    @classmethod
    def load_from_environment(cls) -> "P0FeatureConfig":
        """Load configuration with environment overrides"""
        env = os.getenv("CLAUDE_DIRECTOR_ENV", "development")
        config_dir = Path(__file__).parent.parent.parent.parent.parent / "config"

        # Load base config
        base_config_path = config_dir / "p0_features.yaml"
        config = cls.load_from_file(base_config_path)

        # Load environment-specific overrides
        env_config_path = config_dir / f"p0_features_{env}.yaml"
        if env_config_path.exists():
            with open(env_config_path, "r") as f:
                env_overrides = yaml.safe_load(f)

            # Apply overrides (simple merge for now)
            for key, value in env_overrides.items():
                if hasattr(config, key):
                    setattr(config, key, value)

        # Environment variable overrides
        if os.getenv("P0_DEBUG_MODE"):
            config.debug_mode = os.getenv("P0_DEBUG_MODE").lower() == "true"

        return config

    def save_to_file(self, config_path: Path):
        """Save configuration to YAML file"""
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            yaml.dump(self.dict(), f, default_flow_style=False)


# Global configuration instance
_config: Optional[P0FeatureConfig] = None


def get_config() -> P0FeatureConfig:
    """Get global configuration instance (singleton pattern)"""
    global _config
    if _config is None:
        _config = P0FeatureConfig.load_from_environment()
    return _config


def reset_config():
    """Reset global configuration (for testing)"""
    global _config
    _config = None


def set_config(config: P0FeatureConfig):
    """Set global configuration instance (for testing)"""
    global _config
    _config = config
