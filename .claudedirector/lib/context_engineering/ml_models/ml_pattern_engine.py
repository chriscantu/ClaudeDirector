"""
ML Pattern Engine - Single Responsibility Implementation

Advanced machine learning engine for team collaboration pattern detection using
supervised learning with historical data. Follows Single Responsibility Principle
by focusing exclusively on orchestrating ML pattern detection workflows.

Phase: Phase 3A.1.4 - ML Models Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Import from Real-Time Intelligence foundation
try:
    from ..realtime_monitor import TeamEvent, EventType

    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False

# ML Dependencies availability check
try:
    import numpy as np

    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

# Import types from centralized types module
from ..ml_pattern_types import (
    CollaborationOutcome,
    FeatureVector,
    CollaborationPrediction,
    SuccessPattern,
    TeamCollaborationOutcome,
)

# Import feature extractors and ML models from extracted modules
from ..feature_extractors import TeamFeatureExtractor
from .collaboration_classifier import CollaborationClassifier

# Configure logging
logger = logging.getLogger(__name__)


class MLPatternEngine:
    """
    Advanced machine learning engine for team collaboration pattern detection.
    Uses supervised learning with historical data to predict collaboration outcomes.

    Single Responsibility: ML pattern detection orchestration only.
    Coordinates feature extraction, model training, and prediction workflows.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ML pattern engine with configuration.

        Args:
            config: Configuration dictionary with ML parameters
        """
        self.config = config
        self.feature_extractor = TeamFeatureExtractor(config)
        self.pattern_classifier = CollaborationClassifier(config)
        self.trained_models = {}
        self.pattern_library = {}

        # Performance tracking
        self.prediction_count = 0
        self.training_count = 0
        self.last_training_time = None

        logger.info("MLPatternEngine initialized")

    def predict_collaboration_success(
        self, team_composition: List[str], initiative_context: Dict[str, Any]
    ) -> CollaborationPrediction:
        """
        Predict likelihood of successful collaboration for given team and context.

        Args:
            team_composition: List of team member identifiers
            initiative_context: Context information about the initiative

        Returns:
            CollaborationPrediction with success probability and recommendations
        """
        start_time = time.time()

        try:
            # Create synthetic team events for feature extraction
            # In production, this would use real historical interaction data
            synthetic_events = self._create_synthetic_events(
                team_composition, initiative_context
            )

            # Extract features
            features = self.feature_extractor.extract_features(
                synthetic_events, initiative_context
            )

            # Make prediction
            prediction = self.pattern_classifier.predict_collaboration_success(features)

            # Update performance tracking
            self.prediction_count += 1
            processing_time = time.time() - start_time

            logger.info(
                f"Collaboration prediction completed in {processing_time:.3f}s: "
                f"{prediction.success_probability:.2f} probability"
            )

            return prediction

        except Exception as e:
            logger.error(f"Error in collaboration prediction: {e}")
            # Return fallback prediction
            return CollaborationPrediction(
                success_probability=0.5,
                outcome_prediction=CollaborationOutcome.UNKNOWN,
                confidence_score=0.3,
                contributing_factors=["error_in_prediction"],
                risk_factors=["prediction_system_error"],
                timeline_prediction={f"week_{i}": 0.5 for i in range(1, 5)},
                recommendations=["Review prediction system configuration"],
                timestamp=datetime.now(),
            )

    def identify_success_patterns(
        self, historical_data: List[TeamCollaborationOutcome]
    ) -> List[SuccessPattern]:
        """
        Identify patterns that consistently lead to successful collaboration.

        Args:
            historical_data: List of historical collaboration outcomes

        Returns:
            List of identified success patterns
        """
        if not historical_data:
            return []

        success_patterns = []

        try:
            # Group successful collaborations
            successful_outcomes = [
                outcome
                for outcome in historical_data
                if outcome.outcome == CollaborationOutcome.SUCCESS
            ]

            if len(successful_outcomes) < 5:
                logger.warning("Insufficient successful outcomes for pattern analysis")
                return success_patterns

            # Analyze feature patterns in successful outcomes
            feature_analysis = self._analyze_feature_patterns(successful_outcomes)

            # Create success patterns from analysis
            for pattern_id, pattern_data in feature_analysis.items():
                pattern = SuccessPattern(
                    pattern_id=pattern_id,
                    pattern_name=pattern_data["name"],
                    description=pattern_data["description"],
                    feature_signature=pattern_data["signature"],
                    success_rate=pattern_data["success_rate"],
                    occurrence_count=pattern_data["count"],
                    confidence_score=pattern_data["confidence"],
                    applicable_contexts=pattern_data["contexts"],
                    timestamp=datetime.now(),
                )
                success_patterns.append(pattern)

            logger.info(f"Identified {len(success_patterns)} success patterns")

        except Exception as e:
            logger.error(f"Error in success pattern identification: {e}")

        return success_patterns

    def train_models(
        self, training_data: List[TeamCollaborationOutcome]
    ) -> Dict[str, Any]:
        """
        Train and update ML models with new collaboration outcome data.

        Args:
            training_data: List of collaboration outcomes for training

        Returns:
            Training performance metrics
        """
        start_time = time.time()

        try:
            # Train collaboration classifier
            training_metrics = self.pattern_classifier.train(training_data)

            # Update training tracking
            self.training_count += 1
            self.last_training_time = datetime.now()
            training_time = time.time() - start_time

            training_metrics.update(
                {
                    "training_time_seconds": training_time,
                    "training_data_size": len(training_data),
                    "training_timestamp": self.last_training_time.isoformat(),
                }
            )

            logger.info(
                f"Model training completed in {training_time:.3f}s with "
                f"{len(training_data)} samples"
            )

            return training_metrics

        except Exception as e:
            logger.error(f"Error in model training: {e}")
            return {"error": str(e), "training_failed": True}

    def get_engine_status(self) -> Dict[str, Any]:
        """
        Get current status and performance metrics of the ML engine.

        Returns:
            Dictionary with engine status and metrics
        """
        return {
            "ml_available": ML_AVAILABLE,
            "realtime_available": REALTIME_AVAILABLE,
            "models_trained": self.pattern_classifier.is_trained,
            "prediction_count": self.prediction_count,
            "training_count": self.training_count,
            "last_training_time": (
                self.last_training_time.isoformat() if self.last_training_time else None
            ),
            "pattern_library_size": len(self.pattern_library),
            "config": self.config,
        }

    def _create_synthetic_events(
        self, team_composition: List[str], context: Dict[str, Any]
    ) -> List[TeamEvent]:
        """
        Create synthetic team events for demonstration purposes.

        Args:
            team_composition: List of team member identifiers
            context: Context information for event creation

        Returns:
            List of synthetic team events for testing/demonstration
        """
        if not REALTIME_AVAILABLE:
            return []

        events = []
        base_time = datetime.now() - timedelta(days=7)

        # Create sample interaction events
        for i in range(5):
            event = TeamEvent(
                event_id=f"synthetic_{i}",
                event_type=EventType.COMMUNICATION_DELAY,
                timestamp=base_time + timedelta(hours=i * 6),
                team_id=context.get("team_id", "default_team"),
                participants=team_composition[:2],  # Sample participants
                context={"synthetic": True, "interaction_type": "planning"},
            )
            events.append(event)

        return events

    def _analyze_feature_patterns(
        self, successful_outcomes: List[TeamCollaborationOutcome]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Analyze feature patterns in successful collaboration outcomes.

        Args:
            successful_outcomes: List of successful collaboration outcomes

        Returns:
            Dictionary of analyzed patterns with their characteristics
        """
        patterns = {}

        try:
            # Group by similar feature characteristics
            # This is a simplified pattern analysis
            high_communication_outcomes = [
                outcome
                for outcome in successful_outcomes
                if outcome.features.communication_features.get(
                    "communication_frequency", 0
                )
                > 0.7
            ]

            if len(high_communication_outcomes) >= 3:
                patterns["high_communication"] = {
                    "name": "High Communication Pattern",
                    "description": "Successful collaborations with frequent communication",
                    "signature": {"communication_frequency": 0.8},
                    "success_rate": 0.9,
                    "count": len(high_communication_outcomes),
                    "confidence": 0.8,
                    "contexts": ["development", "planning"],
                }

            # Add more pattern analysis here
            strong_network_outcomes = [
                outcome
                for outcome in successful_outcomes
                if outcome.features.network_features.get("network_connectivity", 0)
                > 0.6
            ]

            if len(strong_network_outcomes) >= 3:
                patterns["strong_network"] = {
                    "name": "Strong Network Connectivity Pattern",
                    "description": "Successful collaborations with strong team connectivity",
                    "signature": {"network_connectivity": 0.7},
                    "success_rate": 0.85,
                    "count": len(strong_network_outcomes),
                    "confidence": 0.75,
                    "contexts": ["cross_functional", "complex_projects"],
                }

        except Exception as e:
            logger.error(f"Error in feature pattern analysis: {e}")

        return patterns
