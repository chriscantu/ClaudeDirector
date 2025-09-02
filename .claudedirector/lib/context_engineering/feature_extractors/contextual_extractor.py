"""
Contextual Feature Extractor - Single Responsibility Implementation

Extracts contextual features from project and organizational context following
Single Responsibility Principle. Focuses exclusively on project complexity,
team experience, organizational support, and external factors.

Phase: Phase 3A.1.3 - Feature Extractors Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

from typing import Dict, List, Any

# Import from Real-Time Intelligence foundation
try:
    from ..realtime_monitor import TeamEvent
    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False

# Import types from centralized types module
from ..ml_pattern_types import FeatureExtractor


class ContextualFeatureExtractor(FeatureExtractor):
    """
    Extracts contextual features from project and organizational context.

    Single Responsibility: Contextual environment analysis only.
    Focuses on project complexity, team capabilities, organizational factors,
    and external dependencies that influence collaboration success.
    """

    def extract_features(
        self, interactions: List[TeamEvent], context: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Extract contextual features from project and organizational environment.

        Args:
            interactions: List of team interaction events (used for context analysis)
            context: Additional context information containing organizational data

        Returns:
            Dictionary of contextual feature values
        """
        features = {}

        # Project complexity - based on complexity indicators
        complexity_indicators = context.get("complexity_indicators", {})
        features["project_complexity"] = min(
            1.0, len(complexity_indicators) / 10.0
        )  # Normalize to 0-1 scale

        # Team experience - normalized team experience in months
        team_experience = context.get("team_experience_months", 12)
        features["team_experience_score"] = min(1.0, team_experience / 36.0)  # 3 years max

        # Organizational support - direct score from context
        support_score = context.get("organizational_support_score", 0.5)
        features["organizational_support"] = float(support_score)

        # Resource availability - direct score from context
        resource_score = context.get("resource_availability_score", 0.5)
        features["resource_availability"] = float(resource_score)

        # Change pressure - based on recent organizational changes
        change_frequency = context.get("recent_changes_count", 0)
        features["change_pressure"] = min(1.0, change_frequency / 5.0)

        # External dependencies - normalized dependency count
        external_deps = context.get("external_dependencies", [])
        features["external_dependency_ratio"] = min(1.0, len(external_deps) / 5.0)

        return features
