"""
Collaboration Classifier - Single Responsibility ML Implementation

Machine learning classifier for team collaboration outcome prediction using
ensemble methods. Follows Single Responsibility Principle by focusing exclusively
on ML classification tasks for collaboration success prediction.

Phase: Phase 3A.1.4 - ML Models Directory Structure
Authors: Martin | Platform Architecture, Berny | AI/ML Engineering
"""

import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple

# ML Dependencies - graceful degradation if not available
try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import StandardScaler

    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

    # Minimal numpy fallback for compatibility
    class MockNumpy:
        @staticmethod
        def array(data):
            return data

        @staticmethod
        def mean(data):
            return sum(data) / len(data) if data else 0

        @staticmethod
        def var(data):
            return 0.1  # Fallback variance

    np = MockNumpy()

# Import types from centralized types module
from ..ml_pattern_types import (
    CollaborationOutcome,
    FeatureVector,
    CollaborationPrediction,
    TeamCollaborationOutcome,
)

# Configure logging
logger = logging.getLogger(__name__)


class CollaborationClassifier:
    """
    Machine learning classifier for team collaboration outcome prediction.
    Uses ensemble methods for robust classification performance.

    Single Responsibility: ML classification for collaboration success only.
    Focuses exclusively on training models and predicting outcomes.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize collaboration classifier with ML model configuration.

        Args:
            config: Configuration dictionary with ML parameters
        """
        self.config = config
        self.models = {}
        self.is_trained = False
        self.feature_scaler = StandardScaler() if ML_AVAILABLE else None
        self.feature_names = []

        if ML_AVAILABLE:
            # Initialize ensemble models
            self.models = {
                "random_forest": RandomForestClassifier(
                    n_estimators=config.get("rf_n_estimators", 100),
                    max_depth=config.get("rf_max_depth", 10),
                    random_state=42,
                ),
                "gradient_boosting": GradientBoostingClassifier(
                    n_estimators=config.get("gb_n_estimators", 100),
                    max_depth=config.get("gb_max_depth", 6),
                    random_state=42,
                ),
            }

    def train(self, training_data: List[TeamCollaborationOutcome]) -> Dict[str, float]:
        """
        Train the collaboration classifier with historical outcome data.

        Args:
            training_data: List of historical collaboration outcomes

        Returns:
            Training performance metrics dictionary
        """
        start_time = time.time()

        if not ML_AVAILABLE:
            logger.warning("ML libraries not available, using fallback prediction")
            return {
                "overall_accuracy": 0.7,
                "accuracy": 0.7,  # Keep for backward compatibility
                "model": "fallback",
                "training_time_seconds": time.time() - start_time,
                "training_data_size": len(training_data),
                "training_timestamp": datetime.now().isoformat(),
            }

        if len(training_data) < 10:
            logger.warning(f"Insufficient training data: {len(training_data)} samples")
            return {
                "overall_accuracy": 0.0,
                "accuracy": 0.0,
                "error": "insufficient_data",
                "training_time_seconds": time.time() - start_time,
                "training_data_size": len(training_data),
                "training_timestamp": datetime.now().isoformat(),
            }

        # Prepare training data
        feature_vectors = []
        labels = []

        for outcome in training_data:
            feature_vector = outcome.features.to_array()
            if len(feature_vector) > 0:
                feature_vectors.append(feature_vector)
                # Convert outcome to numeric label
                label_mapping = {
                    CollaborationOutcome.SUCCESS: 1,
                    CollaborationOutcome.PARTIAL_SUCCESS: 0.5,
                    CollaborationOutcome.FAILURE: 0,
                    CollaborationOutcome.UNKNOWN: 0.3,
                }
                labels.append(label_mapping[outcome.outcome])

        if len(feature_vectors) == 0:
            return {
                "overall_accuracy": 0.0,
                "accuracy": 0.0,
                "error": "no_valid_features",
                "training_time_seconds": time.time() - start_time,
                "training_data_size": len(training_data),
                "training_timestamp": datetime.now().isoformat(),
            }

        X = np.array(feature_vectors)
        y = np.array(labels)

        # Scale features
        X_scaled = self.feature_scaler.fit_transform(X)

        # Train ensemble models
        performance_metrics = {}
        for model_name, model in self.models.items():
            try:
                # Cross-validation for performance estimation
                cv_scores = cross_val_score(model, X_scaled, y, cv=min(5, len(y)))
                performance_metrics[f"{model_name}_cv_accuracy"] = np.mean(cv_scores)

                # Train on full dataset
                model.fit(X_scaled, y)

            except Exception as e:
                logger.error(f"Error training {model_name}: {e}")
                performance_metrics[f"{model_name}_error"] = str(e)

        self.is_trained = True
        performance_metrics["overall_accuracy"] = np.mean(
            [
                score
                for key, score in performance_metrics.items()
                if "cv_accuracy" in key
            ]
        )

        return performance_metrics

    def predict_collaboration_success(
        self, features: FeatureVector
    ) -> CollaborationPrediction:
        """
        Predict collaboration success probability for given features.

        Args:
            features: Feature vector from team interactions

        Returns:
            Collaboration prediction with success probability and recommendations
        """
        if not ML_AVAILABLE or not self.is_trained:
            return self._fallback_prediction(features)

        try:
            # Prepare feature array
            feature_array = features.to_array().reshape(1, -1)
            if len(feature_array[0]) == 0:
                return self._fallback_prediction(features)

            # Scale features
            feature_array_scaled = self.feature_scaler.transform(feature_array)

            # Get predictions from ensemble models
            predictions = {}
            for model_name, model in self.models.items():
                try:
                    # Get probability predictions
                    proba = model.predict_proba(feature_array_scaled)[0]
                    # Assuming binary classification (0: failure, 1: success)
                    success_prob = proba[1] if len(proba) > 1 else proba[0]
                    predictions[model_name] = success_prob
                except Exception as e:
                    logger.error(f"Error with {model_name} prediction: {e}")

            if not predictions:
                return self._fallback_prediction(features)

            # Ensemble prediction (average)
            success_probability = np.mean(list(predictions.values()))

            # Determine outcome prediction
            if success_probability >= 0.75:
                outcome = CollaborationOutcome.SUCCESS
            elif success_probability >= 0.5:
                outcome = CollaborationOutcome.PARTIAL_SUCCESS
            else:
                outcome = CollaborationOutcome.FAILURE

            # Calculate confidence score
            prediction_variance = np.var(list(predictions.values()))
            confidence_score = max(0.1, 1.0 - prediction_variance)

            # Generate recommendations and risk factors
            recommendations, risk_factors = self._generate_recommendations(features)
            contributing_factors = self._identify_contributing_factors(features)

            # Generate timeline prediction
            timeline_prediction = self._generate_timeline_prediction(
                success_probability, features
            )

            return CollaborationPrediction(
                success_probability=success_probability,
                outcome_prediction=outcome,
                confidence_score=confidence_score,
                contributing_factors=contributing_factors,
                risk_factors=risk_factors,
                timeline_prediction=timeline_prediction,
                recommendations=recommendations,
                timestamp=datetime.now(),
            )

        except Exception as e:
            logger.error(f"Error in collaboration prediction: {e}")
            return self._fallback_prediction(features)

    def _fallback_prediction(self, features: FeatureVector) -> CollaborationPrediction:
        """
        Provide fallback prediction when ML models are unavailable.

        Args:
            features: Feature vector for heuristic-based prediction

        Returns:
            CollaborationPrediction using simple heuristics
        """
        # Simple heuristic-based prediction with proper capping (Phase 3A P0 fix)
        comm_score = min(
            1.0, np.mean(list(features.communication_features.values()) or [0.5])
        )
        temporal_score = min(
            1.0, np.mean(list(features.temporal_features.values()) or [0.5])
        )
        network_score = min(
            1.0, np.mean(list(features.network_features.values()) or [0.5])
        )
        context_score = min(
            1.0, np.mean(list(features.contextual_features.values()) or [0.5])
        )

        # Weighted average to ensure overall_score <= 1.0
        overall_score = min(
            1.0,
            (
                comm_score * 0.3
                + temporal_score * 0.25
                + network_score * 0.25
                + context_score * 0.2
            ),
        )

        outcome = (
            CollaborationOutcome.SUCCESS
            if overall_score >= 0.7
            else (
                CollaborationOutcome.PARTIAL_SUCCESS
                if overall_score >= 0.4
                else CollaborationOutcome.FAILURE
            )
        )

        return CollaborationPrediction(
            success_probability=overall_score,
            outcome_prediction=outcome,
            confidence_score=0.6,  # Lower confidence for fallback
            contributing_factors=["heuristic_analysis"],
            risk_factors=["limited_ml_analysis"],
            timeline_prediction={f"week_{i}": overall_score for i in range(1, 5)},
            recommendations=["Enable ML libraries for enhanced predictions"],
            timestamp=datetime.now(),
        )

    def _generate_recommendations(
        self, features: FeatureVector
    ) -> Tuple[List[str], List[str]]:
        """
        Generate recommendations and risk factors based on features.

        Args:
            features: Feature vector for analysis

        Returns:
            Tuple of (recommendations list, risk factors list)
        """
        recommendations = []
        risk_factors = []

        # Communication analysis
        comm_freq = features.communication_features.get("communication_frequency", 0)
        if comm_freq < 0.5:
            recommendations.append("Increase communication frequency")
            risk_factors.append("Low communication frequency")

        response_time = features.communication_features.get(
            "avg_response_time_hours", 24
        )
        if response_time > 12:
            recommendations.append("Improve response times")
            risk_factors.append("Slow response times")

        # Network analysis
        connectivity = features.network_features.get("network_connectivity", 0)
        if connectivity < 0.5:
            recommendations.append("Improve team connectivity")
            risk_factors.append("Poor network connectivity")

        # Contextual analysis
        org_support = features.contextual_features.get("organizational_support", 0.5)
        if org_support < 0.6:
            recommendations.append("Seek additional organizational support")
            risk_factors.append("Limited organizational support")

        return recommendations, risk_factors

    def _identify_contributing_factors(self, features: FeatureVector) -> List[str]:
        """
        Identify factors contributing to collaboration success.

        Args:
            features: Feature vector for analysis

        Returns:
            List of positive contributing factors
        """
        factors = []

        # Identify positive factors
        engagement = features.communication_features.get(
            "participant_engagement_ratio", 0
        )
        if engagement > 0.7:
            factors.append("High participant engagement")

        consistency = features.temporal_features.get("timing_consistency", 0)
        if consistency > 0.7:
            factors.append("Consistent collaboration timing")

        connectivity = features.network_features.get("network_connectivity", 0)
        if connectivity > 0.7:
            factors.append("Strong team connectivity")

        return factors

    def _generate_timeline_prediction(
        self, base_probability: float, features: FeatureVector
    ) -> Dict[str, float]:
        """
        Generate timeline-based success probability predictions.

        Args:
            base_probability: Base success probability
            features: Feature vector for timeline analysis

        Returns:
            Dictionary mapping weeks to predicted success probabilities
        """
        timeline = {}

        # Simple decay model for timeline prediction
        for week in range(1, 5):
            # Probability may decay over time without intervention
            time_factor = 0.95**week  # Slight decay
            prob = base_probability * time_factor
            timeline[f"week_{week}"] = max(0.1, min(1.0, prob))

        return timeline
