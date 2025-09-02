"""
Temporal Feature Extractor - Single Responsibility Implementation

Extracts temporal collaboration pattern features following Single Responsibility
Principle. Focuses exclusively on timing patterns, work schedules, deadline pressure,
and temporal consistency metrics.

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


class TemporalFeatureExtractor(FeatureExtractor):
    """
    Extracts temporal collaboration pattern features.

    Single Responsibility: Temporal pattern analysis only.
    Focuses on duration, timing consistency, work patterns, and deadlines.
    """

    def extract_features(
        self, interactions: List[TeamEvent], context: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Extract temporal pattern features from team interactions.

        Args:
            interactions: List of team interaction events
            context: Additional context information

        Returns:
            Dictionary of temporal-related feature values
        """
        if not interactions:
            return self._get_default_features()

        features = {}

        # Time span analysis - total collaboration duration
        if len(interactions) > 1:
            time_span = (
                interactions[-1].timestamp - interactions[0].timestamp
            ).total_seconds() / 86400  # days
            features["collaboration_duration_days"] = time_span
        else:
            features["collaboration_duration_days"] = 0.0

        # Timing consistency - how regular are the interactions
        time_intervals = []
        for i in range(1, len(interactions)):
            interval = (
                interactions[i].timestamp - interactions[i - 1].timestamp
            ).total_seconds() / 3600  # hours
            time_intervals.append(interval)

        if time_intervals:
            features["timing_consistency"] = 1.0 / (1.0 + np.std(time_intervals))
            features["avg_interaction_interval_hours"] = np.mean(time_intervals)
        else:
            features["timing_consistency"] = 0.5
            features["avg_interaction_interval_hours"] = 24.0

        # Work pattern analysis (business hours vs off-hours)
        business_hours_count = 0
        for interaction in interactions:
            hour = interaction.timestamp.hour
            if 9 <= hour <= 17:  # Business hours
                business_hours_count += 1

        features["business_hours_ratio"] = business_hours_count / len(interactions)

        # Deadline adherence (if available in context)
        deadline = context.get("deadline")
        if deadline and isinstance(deadline, datetime):
            days_to_deadline = (deadline - datetime.now()).days
            features["deadline_pressure"] = max(0.0, 1.0 - (days_to_deadline / 30.0))
        else:
            features["deadline_pressure"] = 0.5

        return features

    def _get_default_features(self) -> Dict[str, float]:
        """
        Return default feature values when no interactions available.

        Returns:
            Dictionary with default temporal feature values
        """
        return {
            "collaboration_duration_days": 0.0,
            "timing_consistency": 0.3,
            "avg_interaction_interval_hours": 48.0,
            "business_hours_ratio": 0.5,
            "deadline_pressure": 0.5,
        }
