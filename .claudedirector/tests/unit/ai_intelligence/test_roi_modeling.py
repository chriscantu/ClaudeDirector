"""
Unit Tests for ROI Modeling Engine - Spec 002 FR2

🏗️ Martin | Platform Architecture - Spec 002 FR2 Test Coverage

Tests the ROI prediction engine for platform investments and strategic initiatives.

TESTING STANDARD: unittest.TestCase (per TESTING_ARCHITECTURE.md)
COVERAGE TARGET: >90% for roi_modeling.py
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path
from datetime import datetime

# Add lib directory to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from ai_intelligence.predictive.roi_modeling import (
    ROIModelingEngine,
    InvestmentType,
    InvestmentContext,
    ROIPrediction,
    ROITimeframe,
)


class TestROIModelingEngine(unittest.TestCase):
    """Test suite for ROIModelingEngine"""

    def setUp(self):
        """Set up test environment"""
        self.config = {
            "confidence_threshold": 0.8,
            "min_roi_threshold": 10.0,
        }
        self.engine = ROIModelingEngine(self.config)

    def test_initialization(self):
        """Test ROIModelingEngine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertEqual(self.engine.config, self.config)
        self.assertIsNotNone(self.engine.baseline_roi_by_type)
        self.assertIsNotNone(self.engine.benefit_multipliers)
        self.assertIsNotNone(self.engine.risk_factors)

    def test_baseline_roi_for_all_investment_types(self):
        """Test baseline ROI exists for all InvestmentType values"""
        for investment_type in InvestmentType:
            self.assertIn(investment_type, self.engine.baseline_roi_by_type)
            baseline = self.engine.baseline_roi_by_type[investment_type]
            self.assertIn("baseline_roi", baseline)
            self.assertIn("confidence", baseline)
            self.assertIn("typical_payback_months", baseline)

    def test_predict_roi_platform_infrastructure(self):
        """Test ROI prediction for platform infrastructure investment"""
        context = InvestmentContext(
            investment_type=InvestmentType.PLATFORM_INFRASTRUCTURE,
            estimated_cost=100000.0,
            team_size=15,
            current_velocity=0.75,
            technical_debt_level=0.3,
            stakeholder_priority=0.8,
            timeframe=ROITimeframe.MEDIUM_TERM,
        )

        prediction = self.engine.predict_roi(context)

        # Verify prediction structure
        self.assertIsInstance(prediction, ROIPrediction)
        self.assertEqual(
            prediction.investment_type, InvestmentType.PLATFORM_INFRASTRUCTURE
        )
        self.assertGreaterEqual(prediction.confidence_score, 0.0)
        self.assertLessEqual(prediction.confidence_score, 1.0)
        self.assertGreater(prediction.payback_period_months, 0)
        self.assertIsNotNone(prediction.recommendations)
        self.assertIsNotNone(prediction.risk_factors)

    def test_predict_roi_automation_investment(self):
        """Test ROI prediction for automation investment"""
        context = InvestmentContext(
            investment_type=InvestmentType.AUTOMATION,
            estimated_cost=50000.0,
            team_size=10,
            current_velocity=0.8,
            technical_debt_level=0.2,
            stakeholder_priority=0.9,
            timeframe=ROITimeframe.SHORT_TERM,
        )

        prediction = self.engine.predict_roi(context)

        self.assertIsInstance(prediction, ROIPrediction)
        # Automation typically has high ROI
        self.assertGreater(prediction.expected_roi, 0)

    def test_predict_roi_with_historical_data(self):
        """Test ROI prediction with historical similar investments"""
        historical_data = [
            {"roi": 150.0, "payback_months": 8, "success": True},
            {"roi": 120.0, "payback_months": 10, "success": True},
        ]

        context = InvestmentContext(
            investment_type=InvestmentType.DEVELOPER_TOOLING,
            estimated_cost=75000.0,
            team_size=12,
            current_velocity=0.7,
            technical_debt_level=0.4,
            stakeholder_priority=0.7,
            timeframe=ROITimeframe.MEDIUM_TERM,
            historical_similar_investments=historical_data,
        )

        prediction = self.engine.predict_roi(context)

        # With historical success data, confidence should be reasonable
        self.assertGreater(prediction.confidence_score, 0.0)

    def test_calculate_team_size_multiplier(self):
        """Test team size multiplier calculation"""
        # Small team
        multiplier_small = self.engine._calculate_team_size_multiplier(5)
        # Medium team
        multiplier_medium = self.engine._calculate_team_size_multiplier(15)
        # Large team
        multiplier_large = self.engine._calculate_team_size_multiplier(30)

        # Larger teams should have higher multipliers
        self.assertGreater(multiplier_large, multiplier_small)
        # All multipliers should be positive
        self.assertGreater(multiplier_small, 0)
        self.assertGreater(multiplier_medium, 0)
        self.assertGreater(multiplier_large, 0)

    def test_calculate_technical_debt_multiplier(self):
        """Test technical debt impact multiplier"""
        # Low debt (< 0.3)
        multiplier_low = self.engine._calculate_technical_debt_multiplier(0.2)
        # Medium debt (0.3-0.6)
        multiplier_medium = self.engine._calculate_technical_debt_multiplier(0.5)
        # High debt (> 0.6)
        multiplier_high = self.engine._calculate_technical_debt_multiplier(0.8)

        # Lower debt should have better multiplier than high debt
        self.assertGreater(multiplier_low, multiplier_high)
        # All multipliers should be positive
        self.assertGreater(multiplier_low, 0)
        self.assertGreater(multiplier_medium, 0)
        self.assertGreater(multiplier_high, 0)

    def test_calculate_stakeholder_multiplier(self):
        """Test stakeholder priority multiplier"""
        # High priority
        multiplier_high = self.engine._calculate_stakeholder_multiplier(0.9)
        # Low priority
        multiplier_low = self.engine._calculate_stakeholder_multiplier(0.3)

        # Higher priority should have better multiplier
        self.assertGreater(multiplier_high, multiplier_low)
        self.assertGreater(multiplier_low, 0)  # Should be positive
        self.assertGreater(multiplier_high, 0)  # Should be positive

    def test_calculate_confidence_with_historical_data(self):
        """Test confidence calculation with historical data"""
        context_with_history = InvestmentContext(
            investment_type=InvestmentType.PLATFORM_INFRASTRUCTURE,
            estimated_cost=100000.0,
            team_size=15,
            current_velocity=0.8,
            technical_debt_level=0.3,
            stakeholder_priority=0.8,
            timeframe=ROITimeframe.MEDIUM_TERM,
            historical_similar_investments=[
                {"roi": 150.0, "success": True},
                {"roi": 130.0, "success": True},
            ],
        )

        context_without_history = InvestmentContext(
            investment_type=InvestmentType.PLATFORM_INFRASTRUCTURE,
            estimated_cost=100000.0,
            team_size=15,
            current_velocity=0.8,
            technical_debt_level=0.3,
            stakeholder_priority=0.8,
            timeframe=ROITimeframe.MEDIUM_TERM,
        )

        # Method signature: _calculate_confidence(base_confidence: float, context: InvestmentContext)
        base_confidence = 0.85
        confidence_with = self.engine._calculate_confidence(
            base_confidence, context_with_history
        )
        confidence_without = self.engine._calculate_confidence(
            base_confidence, context_without_history
        )

        # Historical data should increase confidence
        self.assertGreater(confidence_with, confidence_without)

    def test_identify_risk_factors(self):
        """Test risk factor identification"""
        high_risk_context = InvestmentContext(
            investment_type=InvestmentType.TECHNICAL_DEBT_REDUCTION,
            estimated_cost=200000.0,  # High cost
            team_size=5,  # Small team
            current_velocity=0.4,  # Low velocity
            technical_debt_level=0.9,  # Very high debt
            stakeholder_priority=0.3,  # Low priority
            timeframe=ROITimeframe.SHORT_TERM,
        )

        risk_factors = self.engine._identify_risk_factors(high_risk_context)

        # Should identify risk factors
        self.assertIsInstance(risk_factors, list)
        # Type-specific risks should be included
        self.assertGreater(len(risk_factors), 0)

    def test_generate_recommendations(self):
        """Test recommendation generation"""
        context = InvestmentContext(
            investment_type=InvestmentType.AUTOMATION,
            estimated_cost=50000.0,
            team_size=10,
            current_velocity=0.7,
            technical_debt_level=0.3,
            stakeholder_priority=0.8,
            timeframe=ROITimeframe.MEDIUM_TERM,
        )

        # Method signature: _generate_recommendations(context, predicted_roi, confidence)
        predicted_roi = 3.5
        confidence = 0.85
        recommendations = self.engine._generate_recommendations(
            context, predicted_roi, confidence
        )

        # Should generate actionable recommendations
        self.assertGreater(len(recommendations), 0)
        self.assertIsInstance(recommendations, list)

    def test_calculate_estimated_benefits(self):
        """Test benefit calculation"""
        context = InvestmentContext(
            investment_type=InvestmentType.DEVELOPER_TOOLING,
            estimated_cost=75000.0,
            team_size=15,
            current_velocity=0.75,
            technical_debt_level=0.3,
            stakeholder_priority=0.8,
            timeframe=ROITimeframe.MEDIUM_TERM,
        )

        predicted_roi = 2.5
        benefits = self.engine._calculate_estimated_benefits(context, predicted_roi)

        # Should calculate multiple benefit categories
        self.assertIsInstance(benefits, dict)
        self.assertGreater(len(benefits), 0)

    def test_analyze_investment_portfolio(self):
        """Test portfolio analysis for multiple investments"""
        investments = [
            InvestmentContext(
                investment_type=InvestmentType.AUTOMATION,
                estimated_cost=50000.0,
                team_size=10,
                current_velocity=0.8,
                technical_debt_level=0.2,
                stakeholder_priority=0.9,
                timeframe=ROITimeframe.SHORT_TERM,
            ),
            InvestmentContext(
                investment_type=InvestmentType.PLATFORM_INFRASTRUCTURE,
                estimated_cost=100000.0,
                team_size=15,
                current_velocity=0.7,
                technical_debt_level=0.4,
                stakeholder_priority=0.7,
                timeframe=ROITimeframe.MEDIUM_TERM,
            ),
        ]

        # Returns Dict[str, Any]
        result = self.engine.analyze_investment_portfolio(investments)

        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertIn("total_investments", result)
        self.assertIn("predictions", result)
        self.assertIn("recommended_sequence", result)
        self.assertIn("portfolio_expected_roi", result)

        # Verify counts
        self.assertEqual(result["total_investments"], 2)
        self.assertEqual(len(result["predictions"]), 2)

        # Predictions should be sorted by priority score
        predictions = result["predictions"]
        if len(predictions) > 1:
            self.assertGreaterEqual(
                predictions[0]["priority_score"],
                predictions[1]["priority_score"],
            )

    def test_fallback_prediction(self):
        """Test fallback prediction when data is insufficient"""
        minimal_context = InvestmentContext(
            investment_type=InvestmentType.PROCESS_IMPROVEMENT,
            estimated_cost=10000.0,
            team_size=5,
            current_velocity=0.0,  # No velocity data
            technical_debt_level=0.0,  # No debt data
            stakeholder_priority=0.5,
            timeframe=ROITimeframe.SHORT_TERM,
        )

        prediction = self.engine._create_fallback_prediction(minimal_context)

        # Should create valid fallback prediction
        self.assertIsInstance(prediction, ROIPrediction)
        self.assertEqual(prediction.investment_type, InvestmentType.PROCESS_IMPROVEMENT)
        self.assertGreater(len(prediction.recommendations), 0)


class TestInvestmentTypeEnum(unittest.TestCase):
    """Test suite for InvestmentType enum"""

    def test_all_investment_types_exist(self):
        """Test all expected investment types are present"""
        expected_types = [
            "PLATFORM_INFRASTRUCTURE",
            "DEVELOPER_TOOLING",
            "AUTOMATION",
            "TECHNICAL_DEBT_REDUCTION",
            "TEAM_EXPANSION",
            "TRAINING_DEVELOPMENT",
            "PROCESS_IMPROVEMENT",
        ]

        for expected_type in expected_types:
            self.assertTrue(
                hasattr(InvestmentType, expected_type),
                f"InvestmentType missing: {expected_type}",
            )

    def test_investment_type_values_are_lowercase_snake_case(self):
        """Test InvestmentType enum values follow naming convention"""
        for investment_type in InvestmentType:
            value = investment_type.value
            # Should be lowercase with underscores
            self.assertEqual(value, value.lower())
            self.assertNotIn(" ", value)
            self.assertNotIn("-", value)


class TestROITimeframeEnum(unittest.TestCase):
    """Test suite for ROITimeframe enum"""

    def test_all_timeframes_exist(self):
        """Test all expected timeframes are present"""
        expected_timeframes = ["SHORT_TERM", "MEDIUM_TERM", "LONG_TERM"]

        for expected_timeframe in expected_timeframes:
            self.assertTrue(
                hasattr(ROITimeframe, expected_timeframe),
                f"ROITimeframe missing: {expected_timeframe}",
            )


class TestInvestmentContext(unittest.TestCase):
    """Test suite for InvestmentContext dataclass"""

    def test_investment_context_creation(self):
        """Test InvestmentContext can be created with required fields"""
        context = InvestmentContext(
            investment_type=InvestmentType.AUTOMATION,
            estimated_cost=50000.0,
            team_size=10,
            current_velocity=0.8,
            technical_debt_level=0.2,
            stakeholder_priority=0.9,
            timeframe=ROITimeframe.SHORT_TERM,
        )

        self.assertEqual(context.investment_type, InvestmentType.AUTOMATION)
        self.assertEqual(context.estimated_cost, 50000.0)
        self.assertEqual(context.team_size, 10)

    def test_investment_context_with_historical_data(self):
        """Test InvestmentContext with optional historical data"""
        historical_data = [{"roi": 120.0, "success": True}]

        context = InvestmentContext(
            investment_type=InvestmentType.AUTOMATION,
            estimated_cost=50000.0,
            team_size=10,
            current_velocity=0.8,
            technical_debt_level=0.2,
            stakeholder_priority=0.9,
            timeframe=ROITimeframe.SHORT_TERM,
            historical_similar_investments=historical_data,
        )

        self.assertEqual(context.historical_similar_investments, historical_data)


if __name__ == "__main__":
    unittest.main()
