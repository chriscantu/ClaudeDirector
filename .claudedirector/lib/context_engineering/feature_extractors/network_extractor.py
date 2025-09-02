"""
Network Feature Extractor - Single Responsibility Implementation

Extracts network and team connectivity features following Single Responsibility
Principle. Focuses exclusively on network topology, participation balance,
team size factors, and cross-functional collaboration metrics.

Phase: Phase 3A.1.3 - Feature Extractors Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

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


class NetworkFeatureExtractor(FeatureExtractor):
    """
    Extracts network and team connectivity features.

    Single Responsibility: Network topology and connectivity analysis only.
    Focuses on interaction networks, participation patterns, and collaboration structure.
    """

    def extract_features(
        self, interactions: List[TeamEvent], context: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Extract network and connectivity features from team interactions.

        Args:
            interactions: List of team interaction events
            context: Additional context information

        Returns:
            Dictionary of network-related feature values
        """
        if not interactions:
            return self._get_default_features()

        features = {}

        # Build interaction network
        interaction_pairs = set()
        participant_counts = {}

        for interaction in interactions:
            participants = interaction.participants
            for participant in participants:
                participant_counts[participant] = (
                    participant_counts.get(participant, 0) + 1
                )

            # Add all pairs - complete graph within each interaction
            for i in range(len(participants)):
                for j in range(i + 1, len(participants)):
                    pair = tuple(sorted([participants[i], participants[j]]))
                    interaction_pairs.add(pair)

        # Network connectivity - how well connected is the team
        total_participants = len(participant_counts)
        max_possible_pairs = total_participants * (total_participants - 1) / 2
        features["network_connectivity"] = len(interaction_pairs) / max(
            max_possible_pairs, 1
        )

        # Participation balance - how evenly distributed is participation
        if participant_counts:
            participation_values = list(participant_counts.values())
            features["participation_balance"] = 1.0 - (
                np.std(participation_values) / np.mean(participation_values)
            )
        else:
            features["participation_balance"] = 0.0

        # Team size factors - actual vs expected team size
        expected_team_size = context.get("expected_team_size", total_participants)
        features["team_size_ratio"] = total_participants / max(expected_team_size, 1)

        # Cross-functional collaboration - role diversity
        participant_roles = context.get("participant_roles", {})
        unique_roles = set(participant_roles.values())
        features["cross_functional_ratio"] = len(unique_roles) / max(
            total_participants, 1
        )

        return features

    def _get_default_features(self) -> Dict[str, float]:
        """
        Return default feature values when no interactions available.

        Returns:
            Dictionary with default network feature values
        """
        return {
            "network_connectivity": 0.1,
            "participation_balance": 0.3,
            "team_size_ratio": 0.5,
            "cross_functional_ratio": 0.3,
        }
