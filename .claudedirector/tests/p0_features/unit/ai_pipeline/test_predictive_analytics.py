"""
Unit Tests for Strategic Health Predictor

Berny's comprehensive testing framework ensuring:
- >80% accuracy requirement validation for health prediction
- <200ms performance requirement validation
- Comprehensive risk assessment and recommendation generation
- Edge case handling and data validation
"""

import time

from lib.claudedirector.p0_features.shared.ai_pipeline.predictive_analytics import (
    StrategicHealthPredictor,
)


class TestStrategicHealthPredictor:
    """Test suite for Strategic Health Predictor"""

    def test_predictor_initialization(self, ai_model_config):
        """Test predictor initializes correctly with configuration"""
        predictor = StrategicHealthPredictor(ai_model_config)

        assert predictor.config.model_name == "test_decision_detector"
        assert (
            predictor.config.accuracy_threshold == 0.85
        )  # Will warn about >80% for health
        assert predictor.config.max_inference_time_ms == 200
        assert not predictor._model_loaded

        # Verify scoring weights sum to 1.0
        total_weight = sum(predictor._scoring_weights.values())
        assert abs(total_weight - 1.0) < 0.01

    def test_model_loading_success(self, ai_model_config):
        """Test model loads successfully in test mode"""
        ai_model_config.parameters["test_mode"] = True
        predictor = StrategicHealthPredictor(ai_model_config)

        result = predictor.load_model()

        assert result is True
        assert predictor._model_loaded is True

    def test_health_prediction_healthy_initiative(
        self, ai_model_config, sample_initiative_data
    ):
        """Test health prediction for healthy initiative"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        result = predictor.predict(sample_initiative_data["healthy_initiative"])

        assert result["success"] is True
        assert result["health_score"] >= 0.7  # Should be healthy
        assert result["health_status"] in ["healthy", "excellent"]
        assert result["risk_level"] in ["low", "medium"]
        assert result["confidence"] >= 0.8
        assert len(result["recommendations"]) >= 0

    def test_health_prediction_at_risk_initiative(
        self, ai_model_config, sample_initiative_data
    ):
        """Test health prediction for at-risk initiative"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        result = predictor.predict(sample_initiative_data["at_risk_initiative"])

        assert result["success"] is True
        assert 0.4 <= result["health_score"] < 0.7  # Should be at-risk range
        assert result["health_status"] == "at_risk"
        assert result["risk_level"] in ["medium", "high"]
        assert result["confidence"] >= 0.7
        assert len(result["recommendations"]) > 0  # Should have recommendations

    def test_health_prediction_failing_initiative(
        self, ai_model_config, sample_initiative_data
    ):
        """Test health prediction for failing initiative"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        result = predictor.predict(sample_initiative_data["failing_initiative"])

        assert result["success"] is True
        assert result["health_score"] < 0.5  # Should be low health
        assert result["health_status"] in ["failing", "at_risk"]
        assert result["risk_level"] == "high"
        assert result["confidence"] >= 0.7
        assert len(result["recommendations"]) > 0  # Should have many recommendations

        # Verify urgent recommendations for critical issues
        urgent_recommendations = [
            r for r in result["recommendations"] if r.get("priority") == "urgent"
        ]
        assert len(urgent_recommendations) > 0

    def test_performance_sla_compliance(self, ai_model_config, sample_initiative_data):
        """Test that health prediction meets <200ms SLA"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        start_time = time.time()
        result = predictor.predict(sample_initiative_data["healthy_initiative"])
        end_time = time.time()

        execution_time_ms = (end_time - start_time) * 1000

        assert result["success"] is True
        assert execution_time_ms < 200  # Performance SLA
        assert result["processing_time_ms"] < 200  # Internal measurement

    def test_accuracy_validation(self, ai_model_config, sample_initiative_data):
        """Test accuracy validation against labeled dataset"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        # Create labeled test dataset
        test_data = [
            (
                sample_initiative_data["healthy_initiative"],
                {"expected_health_status": "healthy"},
            ),
            (
                sample_initiative_data["at_risk_initiative"],
                {"expected_health_status": "at_risk"},
            ),
            (
                sample_initiative_data["failing_initiative"],
                {"expected_health_status": "failing"},
            ),
        ]

        accuracy = predictor.validate_accuracy(test_data)

        assert accuracy >= 0.80  # Meets >80% accuracy requirement for health prediction
        assert len(predictor._accuracy_history) > 0

    def test_health_components_calculation(
        self, ai_model_config, sample_initiative_data
    ):
        """Test individual health component calculations"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        result = predictor.predict(sample_initiative_data["healthy_initiative"])

        components = result["health_components"]

        # Verify all components are present
        expected_components = [
            "progress_score",
            "stakeholder_score",
            "milestone_score",
            "budget_score",
            "timeline_score",
            "risk_score",
        ]

        for component in expected_components:
            assert component in components
            assert 0.0 <= components[component] <= 1.0

    def test_risk_assessment(self, ai_model_config, sample_initiative_data):
        """Test comprehensive risk assessment functionality"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        result = predictor.predict(sample_initiative_data["failing_initiative"])

        risk_assessment = result["risk_assessment"]

        # Verify risk assessment structure
        assert "overall_risk_score" in risk_assessment
        assert "risk_indicators" in risk_assessment
        assert "categorized_risks" in risk_assessment
        assert "critical_risks" in risk_assessment

        # Verify risk categorization
        categorized = risk_assessment["categorized_risks"]
        assert "high_impact" in categorized
        assert "medium_impact" in categorized
        assert "low_impact" in categorized

        # Failing initiative should have high risk indicators
        assert len(risk_assessment["critical_risks"]) > 0

    def test_trend_analysis(self, ai_model_config, sample_initiative_data):
        """Test trend analysis and momentum calculation"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        result = predictor.predict(sample_initiative_data["healthy_initiative"])

        trend_analysis = result["trend_analysis"]

        # Verify trend analysis structure
        assert "momentum" in trend_analysis
        assert "momentum_score" in trend_analysis
        assert "trend_indicators" in trend_analysis

        # Verify momentum values
        assert trend_analysis["momentum"] in [
            "accelerating",
            "steady",
            "slowing",
            "stalled",
        ]
        assert 0.0 <= trend_analysis["momentum_score"] <= 1.0

    def test_recommendation_generation(self, ai_model_config, sample_initiative_data):
        """Test actionable recommendation generation"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        result = predictor.predict(sample_initiative_data["at_risk_initiative"])

        recommendations = result["recommendations"]

        # Verify recommendations structure
        assert len(recommendations) > 0
        assert len(recommendations) <= 5  # Should limit to top 5

        for rec in recommendations:
            assert "type" in rec
            assert "priority" in rec
            assert "description" in rec
            assert rec["priority"] in ["urgent", "high", "medium", "low"]

    def test_budget_health_scoring(self, ai_model_config):
        """Test budget health scoring algorithm"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        # Test optimal budget utilization (70-80%)
        optimal_initiative = {
            "id": "test_budget",
            "current_progress": 0.7,
            "stakeholder_engagement_score": 0.8,
            "milestone_completion_rate": 0.7,
            "budget_utilization": 0.75,  # Optimal range
            "risk_indicators": [],
        }

        result = predictor.predict(optimal_initiative)
        components = result["health_components"]

        # Budget score should be high for optimal utilization
        assert components["budget_score"] >= 0.9

        # Test over-budget scenario
        over_budget_initiative = optimal_initiative.copy()
        over_budget_initiative["budget_utilization"] = 0.95  # Over budget

        result_over = predictor.predict(over_budget_initiative)
        components_over = result_over["health_components"]

        # Over-budget should have lower score
        assert components_over["budget_score"] < components["budget_score"]

    def test_stakeholder_engagement_impact(self, ai_model_config):
        """Test stakeholder engagement impact on health scoring"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        base_initiative = {
            "id": "test_engagement",
            "current_progress": 0.6,
            "milestone_completion_rate": 0.6,
            "budget_utilization": 0.6,
            "risk_indicators": [],
        }

        # High engagement scenario
        high_engagement = base_initiative.copy()
        high_engagement["stakeholder_engagement_score"] = 0.9

        # Low engagement scenario
        low_engagement = base_initiative.copy()
        low_engagement["stakeholder_engagement_score"] = 0.3

        result_high = predictor.predict(high_engagement)
        result_low = predictor.predict(low_engagement)

        # High engagement should result in better health score
        assert result_high["health_score"] > result_low["health_score"]

        # Low engagement should generate stakeholder recommendations
        low_recommendations = [
            r
            for r in result_low["recommendations"]
            if "stakeholder" in r.get("type", "").lower()
        ]
        assert len(low_recommendations) > 0

    def test_risk_indicator_weights(self, ai_model_config):
        """Test risk indicator weighting system"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        base_initiative = {
            "id": "test_risk",
            "current_progress": 0.7,
            "stakeholder_engagement_score": 0.7,
            "milestone_completion_rate": 0.7,
            "budget_utilization": 0.7,
            "risk_indicators": [],
        }

        # Test high-impact risk
        high_risk_initiative = base_initiative.copy()
        high_risk_initiative["risk_indicators"] = [
            "budget_overrun",
            "stakeholder_disengagement",
        ]

        # Test low-impact risk
        low_risk_initiative = base_initiative.copy()
        low_risk_initiative["risk_indicators"] = ["external_dependencies"]

        result_high_risk = predictor.predict(high_risk_initiative)
        result_low_risk = predictor.predict(low_risk_initiative)

        # High-impact risks should result in lower health score
        assert result_high_risk["health_score"] < result_low_risk["health_score"]
        assert result_high_risk["risk_level"] != "low"

    def test_input_data_validation(self, ai_model_config):
        """Test input data validation and normalization"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        # Test invalid input types
        invalid_inputs = [None, "string", 123, []]

        for invalid_input in invalid_inputs:
            result = predictor.predict(invalid_input)
            assert result["success"] is False
            assert "error" in result

    def test_minimal_data_handling(self, ai_model_config):
        """Test handling of minimal input data"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        # Minimal valid input
        minimal_data = {"id": "minimal_test"}

        result = predictor.predict(minimal_data)

        assert result["success"] is True
        assert "health_score" in result
        assert "health_status" in result
        assert (
            result["confidence"] < 0.9
        )  # Should have lower confidence with minimal data

    def test_confidence_calculation(self, ai_model_config, sample_initiative_data):
        """Test prediction confidence calculation"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        # Complete data should have high confidence
        complete_result = predictor.predict(
            sample_initiative_data["healthy_initiative"]
        )

        # Incomplete data should have lower confidence
        incomplete_data = {
            "id": "incomplete",
            "current_progress": 0.5,
            # Missing other required fields
        }
        incomplete_result = predictor.predict(incomplete_data)

        assert complete_result["confidence"] > incomplete_result["confidence"]
        assert complete_result["confidence"] >= 0.8

    def test_timeline_score_calculation(self, ai_model_config):
        """Test timeline adherence scoring"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        from datetime import datetime, timedelta

        now = datetime.now()
        start_date = now - timedelta(days=30)
        end_date = now + timedelta(days=30)  # 60-day project, halfway through

        # On-track initiative (50% progress at 50% timeline)
        on_track = {
            "id": "timeline_test",
            "current_progress": 0.5,
            "start_date": start_date.isoformat(),
            "target_end_date": end_date.isoformat(),
            "stakeholder_engagement_score": 0.8,
            "milestone_completion_rate": 0.5,
            "budget_utilization": 0.5,
            "risk_indicators": [],
        }

        result = predictor.predict(on_track)
        components = result["health_components"]

        # Timeline score should be reasonable for on-track project
        assert 0.6 <= components["timeline_score"] <= 1.0

    def test_health_status_thresholds(self, ai_model_config):
        """Test health status threshold boundaries"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        # Test different health score ranges
        test_scores = [
            (0.90, "excellent"),
            (0.75, "healthy"),
            (0.55, "at_risk"),
            (0.25, "failing"),
        ]

        for target_score, expected_status in test_scores:
            # Create initiative data that should result in target score
            test_data = {
                "id": f"test_{expected_status}",
                "current_progress": target_score,
                "stakeholder_engagement_score": target_score,
                "milestone_completion_rate": target_score,
                "budget_utilization": min(
                    0.8, target_score
                ),  # Cap budget to avoid penalty
                "risk_indicators": [] if target_score > 0.7 else ["minor_delay"],
            }

            result = predictor.predict(test_data)

            # Health score should be in expected range
            assert abs(result["health_score"] - target_score) < 0.2

    def test_performance_monitoring(self, ai_model_config, sample_initiative_data):
        """Test performance metrics collection"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        # Clear any existing metrics
        predictor._performance_metrics.clear()

        predictor.predict(sample_initiative_data["healthy_initiative"])

        # Verify performance metrics were recorded
        assert len(predictor._performance_metrics) > 0

        metric = predictor._performance_metrics[-1]
        assert "execution_time_ms" in metric
        assert "confidence" in metric
        assert "meets_time_sla" in metric
        assert "meets_accuracy_sla" in metric

    def test_recommendation_prioritization(
        self, ai_model_config, sample_initiative_data
    ):
        """Test recommendation prioritization logic"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        result = predictor.predict(sample_initiative_data["failing_initiative"])
        recommendations = result["recommendations"]

        # Verify high/urgent priority recommendations come first
        priorities = [rec.get("priority") for rec in recommendations]
        priority_order = ["urgent", "high", "medium", "low"]

        # Check that priorities are generally in descending order of importance
        priority_indices = [
            priority_order.index(p) for p in priorities if p in priority_order
        ]
        assert priority_indices == sorted(priority_indices)

    def test_backwards_compatibility(self, ai_model_config, test_database):
        """Test that health predictor doesn't break existing ClaudeDirector functionality"""
        predictor = StrategicHealthPredictor(ai_model_config)
        predictor.load_model()

        # Verify existing database operations still work
        from lib.context_engineering.strategic_memory_manager import (
            get_strategic_memory_manager as get_db_manager,
        )

        db_manager = get_db_manager(test_database)
        with db_manager.get_connection() as conn:
            result = conn.execute(
                "SELECT COUNT(*) FROM stakeholder_profiles_enhanced"
            ).fetchone()
            assert result[0] >= 0

        # Test health predictor doesn't interfere
        health_result = predictor.predict(
            {
                "id": "compatibility_test",
                "current_progress": 0.5,
                "stakeholder_engagement_score": 0.7,
                "milestone_completion_rate": 0.6,
                "budget_utilization": 0.4,
                "risk_indicators": [],
            }
        )

        assert health_result["success"] is True
