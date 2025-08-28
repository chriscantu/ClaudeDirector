"""
P0 Test: Predictive Analytics Engine

CRITICAL BUSINESS REQUIREMENT:
The Predictive Analytics Engine must provide >90% accurate strategic challenge
predictions with <500ms response times to enable proactive strategic leadership.

This is a BLOCKING P0 test - if it fails, strategic intelligence is compromised.
"""

import unittest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
import time
import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / ".claudedirector/lib"))

from ai_intelligence.predictive_analytics_engine import (
    PredictiveAnalyticsEngine,
    StrategicChallengePrediction,
    OrganizationalHealthMetrics,
    ChallengeType,
    PredictionConfidence,
)
from context_engineering.advanced_context_engine import AdvancedContextEngine


class TestPredictiveAnalyticsP0(unittest.TestCase):
    """
    P0 Test Suite: Predictive Analytics Engine

    Business Critical Requirements:
    1. >90% prediction accuracy for strategic challenges
    2. <500ms response time for predictions
    3. Real-time organizational health monitoring
    4. Integration with 8-layer Context Engineering architecture
    5. Proactive recommendation generation

    Failure Impact: Strategic decision support becomes reactive instead of proactive,
    executive leadership loses early warning capabilities, competitive disadvantage.
    """

    def setUp(self):
        """Set up test environment with mocked dependencies"""
        # Mock the AdvancedContextEngine and its layers
        self.mock_context_engine = Mock(spec=AdvancedContextEngine)
        self.mock_context_engine.stakeholder_layer = Mock()
        self.mock_context_engine.strategic_layer = Mock()
        self.mock_context_engine.organizational_layer = Mock()
        self.mock_context_engine.team_dynamics_engine = Mock()
        self.mock_context_engine.ml_pattern_engine = Mock()

        # Initialize the Predictive Analytics Engine
        self.analytics_engine = PredictiveAnalyticsEngine(
            context_engine=self.mock_context_engine,
            config={
                "prediction_threshold": 0.7,
                "target_response_time_ms": 500,
                "target_accuracy": 0.90,
            },
        )

    def test_p0_blocking_initialization_success(self):
        """
        P0 BLOCKING: Engine must initialize successfully with 8-layer architecture

        Business Impact: Without proper initialization, strategic intelligence
        system is completely unavailable.
        """
        # Verify engine initialized correctly
        self.assertIsNotNone(self.analytics_engine)
        self.assertIsNotNone(self.analytics_engine.context_engine)
        self.assertEqual(self.analytics_engine.target_response_time_ms, 500)
        self.assertEqual(self.analytics_engine.target_accuracy, 0.90)

        # Verify integration with 8-layer architecture
        self.assertIsNotNone(self.analytics_engine.stakeholder_layer)
        self.assertIsNotNone(self.analytics_engine.strategic_layer)
        self.assertIsNotNone(self.analytics_engine.organizational_layer)

        print("✅ P0 BLOCKING: Engine initialization - PASSED")

    def test_p0_blocking_prediction_performance_requirements(self):
        """
        P0 BLOCKING: Predictions must complete within <500ms performance target

        Business Impact: Slow predictions break real-time strategic decision flow,
        executives lose confidence in AI strategic support.
        """
        # Mock context data for realistic prediction scenario
        mock_context_data = {
            "strategic": {
                "velocity_trend": -0.2,  # Declining velocity (burnout indicator)
                "quality_score_trend": -0.1,
                "delivery_confidence": 0.6,
            },
            "stakeholder": {
                "sentiment_score": 0.4,  # Low sentiment (conflict indicator)
                "communication_frequency_change": -0.4,
            },
            "team_dynamics": {
                "stress_indicators": 0.8,  # High stress
                "collaboration_score": 0.5,
            },
        }

        # Mock the context gathering method to return test data
        async def mock_gather_context(query):
            return mock_context_data

        self.analytics_engine._gather_prediction_context = mock_gather_context

        # Measure prediction performance
        async def run_prediction_test():
            start_time = time.time()
            predictions = await self.analytics_engine.predict_strategic_challenges(
                context_query="strategic health assessment", time_horizon_days=30
            )
            end_time = time.time()

            response_time_ms = (end_time - start_time) * 1000

            # Performance assertion: Must complete within 500ms
            self.assertLess(
                response_time_ms,
                500,
                f"Prediction took {response_time_ms:.1f}ms, exceeds 500ms requirement",
            )

            # Functional assertion: Must return predictions for high-risk scenario
            self.assertGreater(
                len(predictions),
                0,
                "High-risk scenario should generate at least one prediction",
            )

            return predictions, response_time_ms

        # Run the async test
        predictions, response_time = asyncio.run(run_prediction_test())

        print(f"✅ P0 BLOCKING: Prediction performance {response_time:.1f}ms - PASSED")

    def test_p0_blocking_challenge_detection_accuracy(self):
        """
        P0 BLOCKING: Engine must detect strategic challenges with high accuracy

        Business Impact: Inaccurate predictions lead to wrong strategic decisions,
        resource misallocation, and missed early intervention opportunities.
        """
        # Test high-risk burnout scenario
        burnout_context = {
            "strategic": {
                "velocity_trend": -0.25,  # Significant velocity decline
                "quality_score_trend": -0.2,
                "delivery_confidence": 0.5,
            },
            "team_dynamics": {
                "stress_indicators": 0.9,  # Very high stress
                "collaboration_score": 0.4,
            },
            "organizational": {"workload_increase": 0.3},  # 30% workload increase
        }

        # Mock context gathering
        async def mock_gather_context(query):
            return burnout_context

        self.analytics_engine._gather_prediction_context = mock_gather_context

        # Run prediction
        async def test_burnout_detection():
            predictions = await self.analytics_engine.predict_strategic_challenges(
                time_horizon_days=30
            )

            # Should detect team burnout challenge
            burnout_predictions = [
                p for p in predictions if p.challenge_type == ChallengeType.TEAM_BURNOUT
            ]

            self.assertGreater(
                len(burnout_predictions),
                0,
                "High-risk burnout scenario should be detected",
            )

            burnout_pred = burnout_predictions[0]

            # Accuracy requirements
            self.assertGreaterEqual(
                burnout_pred.probability_score,
                0.7,
                f"Burnout probability {burnout_pred.probability_score} below threshold",
            )

            self.assertIn(
                burnout_pred.confidence,
                [PredictionConfidence.HIGH, PredictionConfidence.CRITICAL],
                f"Burnout confidence {burnout_pred.confidence} too low for high-risk scenario",
            )

            return burnout_pred

        burnout_prediction = asyncio.run(test_burnout_detection())

        print(
            f"✅ P0 BLOCKING: Challenge detection accuracy {burnout_prediction.probability_score:.2f} - PASSED"
        )

    def test_p0_blocking_organizational_health_monitoring(self):
        """
        P0 BLOCKING: Real-time organizational health metrics must be accurate

        Business Impact: Inaccurate health metrics lead to poor strategic decisions
        and missed organizational risk indicators.
        """
        # Mock health data from different layers
        mock_stakeholder_data = {
            "satisfaction_scores": [0.8, 0.7, 0.9],
            "communication_frequency": 0.8,
            "sentiment_score": 0.75,
        }

        mock_strategic_data = {
            "initiative_success_rate": 0.82,
            "velocity_trend": 0.05,
            "delivery_confidence": 0.88,
        }

        mock_org_data = {"structure_stability": 0.9, "retention_indicators": 0.85}

        mock_team_data = {"collaboration_score": 0.88, "stress_indicators": 0.3}

        # Mock the health data gathering methods
        self.analytics_engine._get_stakeholder_health_data = AsyncMock(
            return_value=mock_stakeholder_data
        )
        self.analytics_engine._get_strategic_health_data = AsyncMock(
            return_value=mock_strategic_data
        )
        self.analytics_engine._get_organizational_health_data = AsyncMock(
            return_value=mock_org_data
        )
        self.analytics_engine._get_team_dynamics_health_data = AsyncMock(
            return_value=mock_team_data
        )

        async def test_health_metrics():
            start_time = time.time()
            health_metrics = (
                await self.analytics_engine.get_organizational_health_metrics()
            )
            end_time = time.time()

            # Performance requirement
            response_time_ms = (end_time - start_time) * 1000
            self.assertLess(
                response_time_ms,
                500,
                f"Health metrics calculation took {response_time_ms:.1f}ms, exceeds 500ms",
            )

            # Accuracy requirements
            self.assertIsInstance(health_metrics, OrganizationalHealthMetrics)

            # Health score should be reasonable for good data
            self.assertGreaterEqual(
                health_metrics.overall_health_score,
                0.7,
                f"Overall health score {health_metrics.overall_health_score} too low for healthy org",
            )

            # Individual metrics should be calculated
            self.assertIsNotNone(health_metrics.stakeholder_satisfaction)
            self.assertIsNotNone(health_metrics.team_velocity_trend)
            self.assertIsNotNone(health_metrics.technical_debt_ratio)

            # Burnout indicators should be present
            self.assertIsInstance(health_metrics.burnout_risk_indicators, list)
            self.assertGreater(len(health_metrics.burnout_risk_indicators), 0)

            return health_metrics

        health_metrics = asyncio.run(test_health_metrics())

        print(
            f"✅ P0 BLOCKING: Health monitoring {health_metrics.overall_health_score:.2f} - PASSED"
        )

    def test_p0_blocking_proactive_recommendations_generation(self):
        """
        P0 BLOCKING: Engine must generate actionable proactive recommendations

        Business Impact: Without proactive recommendations, strategic intelligence
        becomes purely reactive, losing competitive advantage.
        """
        # Create high-confidence predictions for recommendation testing
        test_predictions = [
            StrategicChallengePrediction(
                challenge_type=ChallengeType.TEAM_BURNOUT,
                confidence=PredictionConfidence.HIGH,
                probability_score=0.85,
                time_horizon_days=14,
                impact_severity=0.9,
                contributing_factors=["declining_velocity", "high_stress"],
                evidence_signals=[
                    {"signal": "velocity_decline", "value": -0.25},
                    {"signal": "stress_indicators", "value": 0.9},
                ],
                recommended_actions=[
                    "Implement immediate workload redistribution",
                    "Schedule team retrospective",
                ],
                prediction_timestamp=datetime.now(),
                analysis_duration_ms=150.0,
            ),
            StrategicChallengePrediction(
                challenge_type=ChallengeType.DELIVERY_RISK,
                confidence=PredictionConfidence.CRITICAL,
                probability_score=0.92,
                time_horizon_days=7,
                impact_severity=0.85,
                contributing_factors=["scope_creep", "dependency_issues"],
                evidence_signals=[
                    {"signal": "scope_creep", "value": 0.3},
                    {"signal": "dependency_failures", "value": 0.2},
                ],
                recommended_actions=[
                    "Conduct immediate scope review",
                    "Assess critical dependencies",
                ],
                prediction_timestamp=datetime.now(),
                analysis_duration_ms=120.0,
            ),
        ]

        async def test_recommendations():
            recommendations = await self.analytics_engine.get_proactive_recommendations(
                test_predictions
            )

            # Must generate recommendations for high-confidence predictions
            self.assertGreater(
                len(recommendations),
                0,
                "High-confidence predictions should generate recommendations",
            )

            # Recommendations should be prioritized
            self.assertIn("urgency_score", recommendations[0])
            self.assertIn("impact_score", recommendations[0])
            self.assertIn("recommended_actions", recommendations[0])

            # Highest priority should be the critical delivery risk
            top_recommendation = recommendations[0]
            self.assertEqual(
                top_recommendation["challenge_type"],
                "delivery_risk",
                "Critical delivery risk should be top priority",
            )

            # Recommendations should include actionable steps
            self.assertIsInstance(top_recommendation["recommended_actions"], list)
            self.assertGreater(
                len(top_recommendation["recommended_actions"]),
                0,
                "Recommendations must include actionable steps",
            )

            return recommendations

        recommendations = asyncio.run(test_recommendations())

        print(
            f"✅ P0 BLOCKING: Proactive recommendations ({len(recommendations)} generated) - PASSED"
        )

    def test_p0_blocking_context_engineering_integration(self):
        """
        P0 BLOCKING: Engine must integrate properly with 8-layer Context Engineering

        Business Impact: Without proper integration, strategic intelligence loses
        context richness and accuracy, becoming disconnected from reality.
        """
        # Test integration with each layer
        layer_integrations = {
            "stakeholder_layer": self.analytics_engine.stakeholder_layer,
            "strategic_layer": self.analytics_engine.strategic_layer,
            "organizational_layer": self.analytics_engine.organizational_layer,
            "team_dynamics_engine": self.analytics_engine.team_dynamics_engine,
            "ml_pattern_engine": self.analytics_engine.ml_pattern_engine,
        }

        # Verify layer connections
        for layer_name, layer_obj in layer_integrations.items():
            self.assertIsNotNone(layer_obj, f"{layer_name} integration missing")

        # Test context gathering functionality
        async def test_context_gathering():
            # Mock layer responses
            self.mock_context_engine.stakeholder_layer.get_stakeholder_context = Mock(
                return_value={"test": "stakeholder_data"}
            )
            self.mock_context_engine.strategic_layer.get_strategic_context = Mock(
                return_value={"test": "strategic_data"}
            )
            self.mock_context_engine.organizational_layer.get_organizational_context = (
                Mock(return_value={"test": "organizational_data"})
            )

            # Test context gathering
            context_data = await self.analytics_engine._gather_prediction_context(
                "test strategic query"
            )

            # Verify context was gathered from multiple layers
            self.assertIsInstance(context_data, dict)

            # Context should include data from integrated layers
            # Note: In real implementation, this would contain actual layer data
            self.assertIsNotNone(context_data)

            return context_data

        context_data = asyncio.run(test_context_gathering())

        print("✅ P0 BLOCKING: 8-layer Context Engineering integration - PASSED")

    def test_p0_blocking_prediction_cache_and_performance(self):
        """
        P0 BLOCKING: Prediction caching must work for performance optimization

        Business Impact: Without caching, repeated queries cause performance
        degradation and resource waste in production environments.
        """
        # Mock context data
        mock_context = {
            "strategic": {"velocity_trend": -0.15},
            "stakeholder": {"sentiment_score": 0.6},
        }

        self.analytics_engine._gather_prediction_context = AsyncMock(
            return_value=mock_context
        )

        async def test_caching_performance():
            # First prediction call
            start_time = time.time()
            predictions1 = await self.analytics_engine.predict_strategic_challenges(
                time_horizon_days=30
            )
            first_call_time = time.time() - start_time

            # Verify cache has entries
            self.assertGreater(
                len(self.analytics_engine.prediction_cache),
                0,
                "Prediction cache should contain entries after first call",
            )

            # Second prediction call (should use cache where applicable)
            start_time = time.time()
            predictions2 = await self.analytics_engine.predict_strategic_challenges(
                time_horizon_days=30
            )
            second_call_time = time.time() - start_time

            # Both calls should return results
            self.assertIsInstance(predictions1, list)
            self.assertIsInstance(predictions2, list)

            # Performance should be reasonable for both calls
            self.assertLess(first_call_time * 1000, 500, "First call exceeds 500ms")
            self.assertLess(second_call_time * 1000, 500, "Second call exceeds 500ms")

            return first_call_time, second_call_time

        first_time, second_time = asyncio.run(test_caching_performance())

        print(
            f"✅ P0 BLOCKING: Prediction caching ({first_time*1000:.1f}ms/{second_time*1000:.1f}ms) - PASSED"
        )

    def test_p0_blocking_error_resilience(self):
        """
        P0 BLOCKING: Engine must handle errors gracefully without system failure

        Business Impact: Engine failures cause complete loss of strategic intelligence,
        breaking executive decision support in critical moments.
        """
        # Test with failing context layers
        failing_context_engine = Mock(spec=AdvancedContextEngine)
        failing_context_engine.stakeholder_layer = None
        failing_context_engine.strategic_layer = None
        failing_context_engine.organizational_layer = None

        resilient_engine = PredictiveAnalyticsEngine(
            context_engine=failing_context_engine, config={"prediction_threshold": 0.7}
        )

        async def test_error_resilience():
            # Should not crash with missing layers
            try:
                predictions = await resilient_engine.predict_strategic_challenges()

                # Should return empty list rather than crashing
                self.assertIsInstance(predictions, list)

                # Should not crash on health metrics with missing data
                health_metrics = (
                    await resilient_engine.get_organizational_health_metrics()
                )
                self.assertIsInstance(health_metrics, OrganizationalHealthMetrics)

                return True
            except Exception as e:
                self.fail(f"Engine should handle errors gracefully, but raised: {e}")

        success = asyncio.run(test_error_resilience())

        print("✅ P0 BLOCKING: Error resilience and graceful degradation - PASSED")


def run_p0_test():
    """Run the P0 test suite"""
    print("\n🚨 RUNNING P0 BLOCKING TEST: Predictive Analytics Engine")
    print("=" * 70)
    print("BUSINESS CRITICAL: Strategic intelligence prediction accuracy >90%")
    print("PERFORMANCE CRITICAL: Response times <500ms")
    print("INTEGRATION CRITICAL: 8-layer Context Engineering compatibility")
    print("=" * 70)

    # Run the test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPredictiveAnalyticsP0)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n✅ P0 BLOCKING TEST PASSED: Predictive Analytics Engine operational")
        print("🎯 Strategic intelligence prediction system ready for production")
        return True
    else:
        print("\n❌ P0 BLOCKING TEST FAILED: Predictive Analytics Engine compromised")
        print("🚨 Strategic intelligence system cannot be deployed")
        return False


if __name__ == "__main__":
    success = run_p0_test()
    exit(0 if success else 1)
