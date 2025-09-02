"""
Communication Feature Extractor - Single Responsibility Implementation

Extracts communication-related features from team interactions following
Single Responsibility Principle. Focuses exclusively on communication patterns,
response times, clarity metrics, and participant engagement analysis.

Phase: Phase 3A.1.3 - Feature Extractors Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

from datetime import datetime
from typing import Dict, List, Any

# ML Dependencies - graceful degradation if not available
try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

    # Minimal numpy fallback for compatibility
    class MockNumpy:
        @staticmethod
        def mean(data):
            return sum(data) / len(data) if data else 0

        @staticmethod
        def std(data):
            return 0.1  # Fallback

    np = MockNumpy()

# Import from Real-Time Intelligence foundation
try:
    from ..realtime_monitor import TeamEvent

    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False

# Import types from centralized types module
from ..ml_pattern_types import FeatureExtractor


class CommunicationFeatureExtractor(FeatureExtractor):
    """
    Extracts communication-related features from team interactions.

    Single Responsibility: Communication pattern analysis only.
    Focuses on frequency, response times, clarity, and engagement metrics.
    """

    def extract_features(
        self, interactions: List[TeamEvent], context: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Extract communication pattern features from team interactions.

        Args:
            interactions: List of team interaction events
            context: Additional context information

        Returns:
            Dictionary of communication-related feature values
        """
        if not interactions:
            return self._get_default_features()

        features = {}

        # Communication frequency - interactions per day
        features["communication_frequency"] = len(interactions) / max(
            (datetime.now() - interactions[0].timestamp).days, 1
        )

        # Response time analysis
        response_times = []
        for i in range(1, len(interactions)):
            time_diff = (
                interactions[i].timestamp - interactions[i - 1].timestamp
            ).total_seconds() / 3600  # hours
            response_times.append(time_diff)

        if response_times:
            features["avg_response_time_hours"] = np.mean(response_times)
            features["response_time_consistency"] = 1.0 / (1.0 + np.std(response_times))
        else:
            features["avg_response_time_hours"] = 24.0  # Default high value
            features["response_time_consistency"] = 0.5

        # Communication clarity (based on context richness)
        clarity_scores = []
        for interaction in interactions:
            context_richness = len(interaction.context) / 10.0  # Normalize
            clarity_scores.append(min(1.0, context_richness))

        features["avg_clarity_score"] = (
            np.mean(clarity_scores) if clarity_scores else 0.5
        )

        # Participant engagement
        unique_participants = set()
        for interaction in interactions:
            unique_participants.update(interaction.participants)
        features["participant_engagement_ratio"] = len(unique_participants) / max(
            len(context.get("team_size", [1])), 1
        )

        return features

    def _get_default_features(self) -> Dict[str, float]:
        """
        Return default feature values when no interactions available.

        Returns:
            Dictionary with default communication feature values
        """
        return {
            "communication_frequency": 0.0,
            "avg_response_time_hours": 48.0,
            "response_time_consistency": 0.1,
            "avg_clarity_score": 0.3,
            "participant_engagement_ratio": 0.1,
        }
