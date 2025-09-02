"""
Team Feature Extractor - Composition Pattern Implementation

Main orchestrator for comprehensive team feature extraction using composition.
Coordinates specialized feature extractors following Dependency Inversion Principle
and Single Responsibility Principle.

Phase: Phase 3A.1.3 - Feature Extractors Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any

# Import from Real-Time Intelligence foundation
try:
    from ..realtime_monitor import TeamEvent
    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False

# Import types from centralized types module
from ..ml_pattern_types import FeatureVector

# Import specialized feature extractors using Dependency Inversion
from .communication_extractor import CommunicationFeatureExtractor
from .temporal_extractor import TemporalFeatureExtractor
from .network_extractor import NetworkFeatureExtractor
from .contextual_extractor import ContextualFeatureExtractor


class TeamFeatureExtractor:
    """
    Advanced feature extraction from team interaction data for ML model training.
    Transforms raw team events into comprehensive ML-ready feature vectors.

    Architecture: Uses composition pattern with specialized extractors.
    SOLID Compliance: Follows Dependency Inversion and Single Responsibility.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize feature extractor with configuration.

        Uses Dependency Inversion Principle - depends on abstractions (FeatureExtractor)
        not concretions, enabling flexible composition and testing.

        Args:
            config: Configuration dictionary with extraction parameters
        """
        self.config = config

        # Composition: Inject specialized feature extractors
        # This follows Dependency Inversion Principle
        self.communication_extractor = CommunicationFeatureExtractor()
        self.temporal_extractor = TemporalFeatureExtractor()
        self.network_extractor = NetworkFeatureExtractor()
        self.contextual_extractor = ContextualFeatureExtractor()

        # Feature extraction configuration
        self.feature_window_days = config.get("feature_window_days", 30)
        self.min_interactions_threshold = config.get("min_interactions_threshold", 3)

    def extract_features(
        self, team_interactions: List[TeamEvent], context: Dict[str, Any]
    ) -> FeatureVector:
        """
        Extract comprehensive feature set from team interaction data.

        Single Responsibility: Orchestrates feature extraction process only.
        Delegates actual feature extraction to specialized classes.

        Args:
            team_interactions: List of team interaction events
            context: Additional context information

        Returns:
            FeatureVector with all extracted features organized by category
        """
        # Filter recent interactions within feature window
        cutoff_date = datetime.now() - timedelta(days=self.feature_window_days)
        recent_interactions = [
            interaction
            for interaction in team_interactions
            if interaction.timestamp > cutoff_date
        ]

        # Extract features from each specialized category
        # Each extractor follows Single Responsibility Principle
        communication_features = self.communication_extractor.extract_features(
            recent_interactions, context
        )
        temporal_features = self.temporal_extractor.extract_features(
            recent_interactions, context
        )
        network_features = self.network_extractor.extract_features(
            recent_interactions, context
        )
        contextual_features = self.contextual_extractor.extract_features(
            recent_interactions, context
        )

        # Compose final feature vector
        return FeatureVector(
            communication_features=communication_features,
            temporal_features=temporal_features,
            network_features=network_features,
            contextual_features=contextual_features,
            timestamp=datetime.now(),
        )

    def get_feature_names(self) -> List[str]:
        """
        Get ordered list of all feature names for consistent ML model input.

        Returns:
            Complete list of feature names in canonical order
        """
        # Communication features (from CommunicationFeatureExtractor)
        comm_features = [
            "communication_frequency",
            "avg_response_time_hours",
            "response_time_consistency",
            "avg_clarity_score",
            "participant_engagement_ratio",
        ]

        # Temporal features (from TemporalFeatureExtractor)
        temporal_features = [
            "collaboration_duration_days",
            "timing_consistency",
            "avg_interaction_interval_hours",
            "business_hours_ratio",
            "deadline_pressure",
        ]

        # Network features (from NetworkFeatureExtractor)
        network_features = [
            "network_connectivity",
            "participation_balance",
            "team_size_ratio",
            "cross_functional_ratio",
        ]

        # Contextual features (from ContextualFeatureExtractor)
        contextual_features = [
            "project_complexity",
            "team_experience_score",
            "organizational_support",
            "resource_availability",
            "change_pressure",
            "external_dependency_ratio",
        ]

        # Return complete ordered feature list for ML model consistency
        return (
            comm_features + temporal_features + network_features + contextual_features
        )
