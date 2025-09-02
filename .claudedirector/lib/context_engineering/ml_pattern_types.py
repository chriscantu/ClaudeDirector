"""
ML Pattern Detection - Core Type Definitions

Extracted from ml_pattern_engine.py for SOLID compliance (Phase 3A.1.1)
This module contains core type definitions, enums, and data classes used
throughout the ML Pattern Detection system.

Single Responsibility: Type definitions and interfaces only
Open/Closed: Abstract interfaces enable extension
Interface Segregation: Small, focused type definitions
Dependency Inversion: Abstract base classes for extensibility

Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
Phase: Phase 3A.1.1 - Type Extraction for SOLID Compliance
"""

import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple, Union
from abc import ABC, abstractmethod

# ML Dependencies - graceful degradation if not available
try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

    # Minimal numpy fallback for compatibility
    class MockNumpy:
        ndarray = list  # Mock ndarray as list type

        @staticmethod
        def array(data):
            return data

        @staticmethod
        def mean(data):
            return sum(data) / len(data) if data else 0

        @staticmethod
        def std(data):
            return 0.1  # Fallback

        @staticmethod
        def random():
            class Random:
                @staticmethod
                def rand():
                    return 0.5

            return Random()

        @staticmethod
        def zeros(shape):
            return [0] * (shape if isinstance(shape, int) else shape[0])

    np = MockNumpy()

# Import from Real-Time Intelligence foundation
try:
    from .realtime_monitor import TeamEvent, EventType, Alert, AlertSeverity

    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False

    # Fallback stubs if realtime_monitor unavailable
    class TeamEvent:
        pass

    class EventType:
        pass

    class Alert:
        pass

    class AlertSeverity:
        pass


# Configure logging
logger = logging.getLogger(__name__)


# =============================================================================
# CORE ENUMERATIONS
# =============================================================================


class FeatureType(Enum):
    """Types of features extracted from team interaction data."""

    COMMUNICATION = "communication"
    TEMPORAL = "temporal"
    NETWORK = "network"
    CONTEXTUAL = "contextual"


class CollaborationOutcome(Enum):
    """Possible outcomes for team collaboration."""

    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    UNKNOWN = "unknown"


# =============================================================================
# ABSTRACT INTERFACES - DEPENDENCY INVERSION PRINCIPLE
# =============================================================================


class FeatureExtractor(ABC):
    """Abstract base class for feature extractors.

    Implements Dependency Inversion Principle - high-level modules depend on
    abstractions, not concretions. Enables extensibility through composition.
    """

    @abstractmethod
    def extract_features(
        self, interactions: List[TeamEvent], context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Extract features from team interactions."""
        pass


# =============================================================================
# CORE DATA CLASSES - SINGLE RESPONSIBILITY PRINCIPLE
# =============================================================================


@dataclass
class FeatureVector:
    """Feature vector extracted from team interaction data.

    Single Responsibility: Encapsulates feature data with conversion methods.
    Interface Segregation: Focused on feature representation only.
    """

    communication_features: Dict[str, float] = field(default_factory=dict)
    temporal_features: Dict[str, float] = field(default_factory=dict)
    network_features: Dict[str, float] = field(default_factory=dict)
    contextual_features: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_array(self) -> np.ndarray:
        """Convert feature vector to numpy array for ML model input."""
        if not NUMPY_AVAILABLE:
            return np.array([])

        features = []
        features.extend(self.communication_features.values())
        features.extend(self.temporal_features.values())
        features.extend(self.network_features.values())
        features.extend(self.contextual_features.values())
        return np.array(features)

    def to_dict(self) -> Dict[str, Any]:
        """Convert feature vector to dictionary representation."""
        return {
            "communication_features": self.communication_features,
            "temporal_features": self.temporal_features,
            "network_features": self.network_features,
            "contextual_features": self.contextual_features,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class CollaborationPrediction:
    """Prediction result for team collaboration success.

    Single Responsibility: Encapsulates prediction results and metadata.
    """

    success_probability: float
    outcome_prediction: CollaborationOutcome
    confidence_score: float
    contributing_factors: List[str]
    risk_factors: List[str]
    timeline_prediction: Dict[str, float]  # week -> success probability
    recommendations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert prediction to dictionary representation."""
        return {
            "success_probability": self.success_probability,
            "outcome_prediction": self.outcome_prediction.value,
            "confidence_score": self.confidence_score,
            "contributing_factors": self.contributing_factors,
            "risk_factors": self.risk_factors,
            "timeline_prediction": self.timeline_prediction,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class SuccessPattern:
    """Identified pattern that leads to successful collaboration.

    Single Responsibility: Encapsulates success pattern data and metadata.
    """

    pattern_id: str
    pattern_name: str
    description: str
    feature_signature: Dict[str, float]
    success_rate: float
    occurrence_count: int
    confidence_score: float
    applicable_contexts: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert success pattern to dictionary representation."""
        return {
            "pattern_id": self.pattern_id,
            "pattern_name": self.pattern_name,
            "description": self.description,
            "feature_signature": self.feature_signature,
            "success_rate": self.success_rate,
            "occurrence_count": self.occurrence_count,
            "confidence_score": self.confidence_score,
            "applicable_contexts": self.applicable_contexts,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class TeamCollaborationOutcome:
    """Historical team collaboration outcome for model training.

    Single Responsibility: Encapsulates training data for ML models.
    """

    team_id: str
    participants: List[str]
    outcome: CollaborationOutcome
    success_score: float  # 0.0-1.0
    duration_days: int
    context: Dict[str, Any]
    features: FeatureVector
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        """Convert collaboration outcome to dictionary representation."""
        return {
            "team_id": self.team_id,
            "participants": self.participants,
            "outcome": self.outcome.value,
            "success_score": self.success_score,
            "duration_days": self.duration_days,
            "context": self.context,
            "features": self.features.to_dict(),
            "timestamp": self.timestamp.isoformat(),
        }


# =============================================================================
# CONFIGURATION CLASSES - SINGLE RESPONSIBILITY PRINCIPLE
# =============================================================================


@dataclass
class EnsembleModelConfig:
    """Configuration for ensemble ML models in CollaborationScorer.

    Single Responsibility: ML model configuration parameters only.
    Open/Closed: Can be extended with new parameters without modification.
    """

    # Model weights for ensemble voting
    decision_tree_weight: float = 0.2
    random_forest_weight: float = 0.3
    gradient_boosting_weight: float = 0.3
    neural_network_weight: float = 0.2

    # Training parameters
    n_estimators: int = 100
    max_depth: int = 10
    test_size: float = 0.2
    random_state: int = 42

    # Performance thresholds
    min_accuracy_threshold: float = 0.85
    confidence_threshold: float = 0.7
    min_training_samples: int = 10


# =============================================================================
# ADVANCED PREDICTION TYPES - LISKOV SUBSTITUTION PRINCIPLE
# =============================================================================


@dataclass
class RiskAssessment:
    """Risk assessment result from CollaborationScorer.

    Single Responsibility: Risk assessment data and metadata.
    """

    overall_risk_score: float  # 0.0 (low risk) to 1.0 (high risk)
    risk_factors: Dict[str, float]  # Individual risk factor scores
    mitigation_recommendations: List[str]
    confidence_interval: Tuple[float, float]  # (lower_bound, upper_bound)
    timeline_prediction: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AdvancedCollaborationPrediction(CollaborationPrediction):
    """Enhanced collaboration prediction with ensemble model results.

    Liskov Substitution Principle: Can be used anywhere CollaborationPrediction
    is expected, with additional ensemble-specific functionality.
    """

    ensemble_predictions: Dict[str, float] = field(
        default_factory=dict
    )  # Individual model predictions
    risk_assessment: Optional[RiskAssessment] = None
    feature_importance: Dict[str, float] = field(default_factory=dict)
    model_confidence: Dict[str, float] = field(default_factory=dict)


# =============================================================================
# TYPE ALIASES AND COMPATIBILITY
# =============================================================================

# Type aliases for improved readability and future flexibility
FeatureDict = Dict[str, float]
PredictionDict = Dict[str, Any]
PatternDict = Dict[str, Any]
OutcomeDict = Dict[str, Any]

# Version information for API compatibility
__version__ = "3.0.0"  # Phase 3A.1.1 - Type Extraction
__api_version__ = "1.0"
__last_updated__ = "2025-02-09"

# Export all public types for easy importing
__all__ = [
    # Enums
    "FeatureType",
    "CollaborationOutcome",
    # Abstract interfaces
    "FeatureExtractor",
    # Core data classes
    "FeatureVector",
    "CollaborationPrediction",
    "SuccessPattern",
    "TeamCollaborationOutcome",
    # Configuration
    "EnsembleModelConfig",
    # Advanced types
    "RiskAssessment",
    "AdvancedCollaborationPrediction",
    # Type aliases
    "FeatureDict",
    "PredictionDict",
    "PatternDict",
    "OutcomeDict",
    # Dependencies
    "TeamEvent",
    "EventType",
    "Alert",
    "AlertSeverity",
    "NUMPY_AVAILABLE",
    "REALTIME_AVAILABLE",
    # Version info
    "__version__",
    "__api_version__",
]
