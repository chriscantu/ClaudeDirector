"""
Feature Extractors - SOLID Compliance Module for ML Pattern Detection

Extracted from ml_pattern_engine.py for Single Responsibility Principle compliance.
Each feature extractor class has a focused, cohesive responsibility for extracting
specific types of features from team interaction data.

Phase: Phase 3A.1.3 - Feature Extractors Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

# Import individual feature extractors
from .communication_extractor import CommunicationFeatureExtractor
from .temporal_extractor import TemporalFeatureExtractor
from .network_extractor import NetworkFeatureExtractor
from .contextual_extractor import ContextualFeatureExtractor
from .team_feature_extractor import TeamFeatureExtractor

# Define public API for the feature_extractors module
__all__ = [
    "CommunicationFeatureExtractor",
    "TemporalFeatureExtractor",
    "NetworkFeatureExtractor",
    "ContextualFeatureExtractor",
    "TeamFeatureExtractor",
]
