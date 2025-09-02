"""
ML Models - SOLID Compliance Module for ML Pattern Detection

Extracted from ml_pattern_engine.py for Single Responsibility Principle compliance.
Each ML model class has a focused, cohesive responsibility for specific aspects
of machine learning prediction and analysis.

Phase: Phase 3A.1.4 - ML Models Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

# Import individual ML model classes
from .collaboration_classifier import CollaborationClassifier
from .ml_pattern_engine import MLPatternEngine
from .risk_assessment_engine import RiskAssessmentEngine
from .collaboration_scorer import CollaborationScorer

# Phase 3A.1.4 COMPLETE - All ML classes extracted!
# All major ML classes now follow Single Responsibility Principle

# Define public API for the ml_models module
__all__ = [
    "CollaborationClassifier",
    "MLPatternEngine",
    "RiskAssessmentEngine",
    "CollaborationScorer",
]
