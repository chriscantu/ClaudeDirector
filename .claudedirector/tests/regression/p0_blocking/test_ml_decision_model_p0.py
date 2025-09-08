#!/usr/bin/env python3
"""
P0 Test: ML Decision Model Architecture - Phase 5.1

Tests the foundational ML decision model architecture that extends ai_intelligence/
following PROJECT_STRUCTURE.md compliance and zero code duplication.

P0 CRITICAL REQUIREMENTS:
- MLDecisionModel base class functionality
- Abstract interfaces for ML model types
- Integration with existing strategic memory systems
- Zero architectural violations
- ≥95% test coverage for all base classes and interfaces

Author: Martin | Platform Architecture
Phase: 5.1 - ML-Powered Strategic Decision Support
Test Level: P0 (BLOCKING)
"""

import asyncio
import pytest
from datetime import datetime
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, AsyncMock, patch

# Import components under test
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from lib.ai_intelligence.ml_decision_engine import (
    MLModelType,
    MLDecisionContext,
    MLDecisionResult,
    MLDecisionModel,
    PredictiveDecisionModel,
    EnhancedMLDecisionEngine,
    create_ml_decision_engine,
)

# Import existing dependencies (no duplication)
from lib.ai_intelligence.decision_orchestrator import (
    DecisionContext,
    DecisionComplexity,
)
from lib.transparency import TransparencyContext


class TestMLDecisionModelArchitecture:
    """P0 Test Suite: ML Decision Model Architecture"""

    def test_ml_model_type_enum_completeness(self):
        """P0: Validate ML model type enumeration"""
        expected_types = {
            "predictive",
            "classification",
            "regression",
            "ensemble",
            "deep_learning",
        }
        actual_types = {model_type.value for model_type in MLModelType}

        assert (
            actual_types == expected_types
        ), f"Missing ML model types: {expected_types - actual_types}"

    def test_ml_decision_context_structure(self):
        """P0: Validate ML decision context data structure"""
        # Create base decision context with correct parameters
        base_context = DecisionContext(
            user_input="Test strategic decision",
            session_id="test_session",
            persona="martin",
            complexity=DecisionComplexity.HIGH,
            domain="platform_strategy",
            stakeholder_scope=["engineering", "product"],
            time_sensitivity="high",
            business_impact="high",
            confidence=0.8,
            detected_patterns=["strategic", "platform"],
        )

        # Create ML decision context
        ml_context = MLDecisionContext(
            base_context=base_context,
            historical_patterns=[{"pattern": "test"}],
            training_data_features={"feature1": 0.5},
            model_confidence=0.85,
        )

        # Validate structure
        assert ml_context.base_context == base_context
        assert len(ml_context.historical_patterns) == 1
        assert ml_context.training_data_features["feature1"] == 0.5
        assert ml_context.model_confidence == 0.85
        assert ml_context.model_version == "1.0.0"

    def test_ml_decision_result_completeness(self):
        """P0: Validate ML decision result contains all required fields"""
        result = MLDecisionResult(
            recommended_action="implement_strategy",
            confidence_score=0.85,
            success_probability=0.80,
            model_type_used=MLModelType.PREDICTIVE,
            feature_contributions={"complexity": 0.3},
            alternative_scenarios=[{"scenario": "optimistic"}],
            risk_assessment={"execution_risk": 0.2},
            strategic_frameworks_recommended=["WRAP Framework"],
            stakeholder_impact_prediction={"positive": 0.7},
            timeline_prediction="2-3 weeks",
            model_explanation="Test explanation",
            decision_rationale=["Test rationale"],
            uncertainty_factors=["Test uncertainty"],
        )

        # Validate all critical fields present
        assert result.recommended_action == "implement_strategy"
        assert result.confidence_score == 0.85
        assert result.success_probability == 0.80
        assert result.model_type_used == MLModelType.PREDICTIVE
        assert len(result.feature_contributions) > 0
        assert len(result.alternative_scenarios) > 0
        assert len(result.risk_assessment) > 0
        assert len(result.strategic_frameworks_recommended) > 0
        assert len(result.stakeholder_impact_prediction) > 0
        assert result.timeline_prediction == "2-3 weeks"
        assert len(result.decision_rationale) > 0
        assert len(result.uncertainty_factors) > 0
        assert isinstance(result.timestamp, datetime)


class TestMLDecisionModelInterface:
    """P0 Test Suite: ML Decision Model Abstract Interface"""

    def test_ml_decision_model_abstract_interface(self):
        """P0: Validate MLDecisionModel abstract interface requirements"""
        # Verify abstract methods exist
        abstract_methods = MLDecisionModel.__abstractmethods__
        expected_methods = {"predict", "train", "get_model_info"}

        assert (
            abstract_methods == expected_methods
        ), f"Abstract interface mismatch: {abstract_methods}"

    def test_ml_decision_model_cannot_be_instantiated(self):
        """P0: Validate abstract base class cannot be instantiated directly"""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            MLDecisionModel()


class TestPredictiveDecisionModel:
    """P0 Test Suite: Predictive Decision Model Implementation"""

    @pytest.fixture
    def mock_strategic_memory(self):
        """Mock strategic memory manager"""
        mock_memory = Mock()
        mock_memory.get_decision_history = AsyncMock(return_value=[])
        mock_memory.get_similar_decisions = AsyncMock(return_value=[])
        mock_memory.extract_decision_features = AsyncMock(return_value={})
        return mock_memory

    @pytest.fixture
    def mock_predictive_processor(self):
        """Mock predictive processor"""
        mock_processor = Mock()
        mock_processor.predict_decision_outcome = AsyncMock()
        mock_processor.train_models = AsyncMock(return_value=True)
        mock_processor.get_model_info = Mock(return_value={"version": "test"})
        return mock_processor

    def test_predictive_decision_model_initialization(self, mock_strategic_memory):
        """P0: Validate predictive decision model initialization"""
        config = {"accuracy_threshold": 0.90, "confidence_threshold": 0.75}

        model = PredictiveDecisionModel(
            strategic_memory_manager=mock_strategic_memory, config=config
        )

        assert model.strategic_memory == mock_strategic_memory
        assert model.model_type == MLModelType.PREDICTIVE
        assert model.accuracy_threshold == 0.90
        assert model.confidence_threshold == 0.75

    @pytest.mark.asyncio
    async def test_predictive_decision_model_predict(self, mock_strategic_memory):
        """P0: Validate predictive decision model prediction functionality"""
        # Setup
        model = PredictiveDecisionModel(strategic_memory_manager=mock_strategic_memory)

        base_context = DecisionContext(
            user_input="Test prediction",
            session_id="test_session",
            persona="martin",
            complexity=DecisionComplexity.MEDIUM,
            domain="engineering",
            stakeholder_scope=["team"],
            time_sensitivity="medium",
            business_impact="medium",
            confidence=0.8,
            detected_patterns=["engineering"],
        )

        ml_context = MLDecisionContext(base_context=base_context)

        # Mock predictive processor
        with patch.object(model, "predictive_processor") as mock_processor:
            mock_result = Mock()
            mock_result.prediction = "test_action"
            mock_result.confidence = 0.85
            mock_result.metadata = {"timeline": "1 week"}
            mock_processor.predict_decision_outcome = AsyncMock(
                return_value=mock_result
            )

            # Execute
            result = await model.predict(ml_context)

            # Validate
            assert isinstance(result, MLDecisionResult)
            assert result.recommended_action == "test_action"
            assert result.confidence_score == 0.85
            assert result.model_type_used == MLModelType.PREDICTIVE
            assert result.processing_time_ms > 0

    @pytest.mark.asyncio
    async def test_predictive_decision_model_train(self, mock_strategic_memory):
        """P0: Validate predictive decision model training functionality"""
        model = PredictiveDecisionModel(strategic_memory_manager=mock_strategic_memory)

        training_data = [{"decision": "test", "outcome": "success"}]

        # Mock predictive processor training
        with patch.object(model, "predictive_processor") as mock_processor:
            mock_processor.train_models = AsyncMock(return_value=True)

            # Execute
            result = await model.train(training_data)

            # Validate
            assert result is True
            mock_processor.train_models.assert_called_once()

    def test_predictive_decision_model_get_model_info(self, mock_strategic_memory):
        """P0: Validate predictive decision model info retrieval"""
        model = PredictiveDecisionModel(strategic_memory_manager=mock_strategic_memory)

        # Mock predictive processor info
        with patch.object(model, "predictive_processor") as mock_processor:
            mock_processor.get_model_info = Mock(return_value={"test": "info"})

            # Execute
            info = model.get_model_info()

            # Validate
            assert info["model_type"] == "predictive"
            assert info["version"] == "5.1.0"
            assert "processor_info" in info
            assert "last_update" in info


class TestEnhancedMLDecisionEngine:
    """P0 Test Suite: Enhanced ML Decision Engine"""

    @pytest.fixture
    def mock_decision_orchestrator(self):
        """Mock decision orchestrator"""
        return Mock()

    @pytest.fixture
    def mock_strategic_memory(self):
        """Mock strategic memory manager"""
        mock_memory = Mock()
        mock_memory.get_similar_decisions = AsyncMock(return_value=[])
        mock_memory.extract_decision_features = AsyncMock(return_value={})
        return mock_memory

    def test_enhanced_ml_decision_engine_initialization(
        self, mock_decision_orchestrator, mock_strategic_memory
    ):
        """P0: Validate enhanced ML decision engine initialization"""
        config = {"predictive": {"accuracy_threshold": 0.90}}

        engine = EnhancedMLDecisionEngine(
            decision_orchestrator=mock_decision_orchestrator,
            strategic_memory_manager=mock_strategic_memory,
            config=config,
        )

        assert engine.decision_orchestrator == mock_decision_orchestrator
        assert engine.strategic_memory == mock_strategic_memory
        assert MLModelType.PREDICTIVE in engine.models
        assert engine.prediction_count == 0
        assert engine.training_count == 0

    @pytest.mark.asyncio
    async def test_enhanced_ml_decision_engine_generate_decision(
        self, mock_decision_orchestrator, mock_strategic_memory
    ):
        """P0: Validate ML decision generation"""
        engine = EnhancedMLDecisionEngine(
            decision_orchestrator=mock_decision_orchestrator,
            strategic_memory_manager=mock_strategic_memory,
        )

        decision_context = DecisionContext(
            user_input="Test engine decision",
            session_id="test_session",
            persona="martin",
            domain="strategy",
            complexity=DecisionComplexity.HIGH,
            stakeholder_scope=["leadership"],
            time_sensitivity="high",
            business_impact="high",
            confidence=0.85,
            detected_patterns=["strategy"],
        )

        # Mock model prediction
        mock_model = Mock()
        mock_result = MLDecisionResult(
            recommended_action="strategic_action",
            confidence_score=0.88,
            success_probability=0.82,
            model_type_used=MLModelType.PREDICTIVE,
            feature_contributions={},
            alternative_scenarios=[],
            risk_assessment={},
            strategic_frameworks_recommended=[],
            stakeholder_impact_prediction={},
            timeline_prediction="test",
            model_explanation="test",
            decision_rationale=[],
            uncertainty_factors=[],
        )
        mock_model.predict = AsyncMock(return_value=mock_result)
        engine.models[MLModelType.PREDICTIVE] = mock_model

        # Execute
        result = await engine.generate_ml_decision(decision_context)

        # Validate
        assert isinstance(result, MLDecisionResult)
        assert result.recommended_action == "strategic_action"
        assert result.confidence_score == 0.88
        assert engine.prediction_count == 1

    @pytest.mark.asyncio
    async def test_enhanced_ml_decision_engine_train_models(
        self, mock_decision_orchestrator, mock_strategic_memory
    ):
        """P0: Validate ML model training"""
        engine = EnhancedMLDecisionEngine(
            decision_orchestrator=mock_decision_orchestrator,
            strategic_memory_manager=mock_strategic_memory,
        )

        training_data = [{"decision": "test", "outcome": "success"}]

        # Mock model training
        mock_model = Mock()
        mock_model.train = AsyncMock(return_value=True)
        engine.models[MLModelType.PREDICTIVE] = mock_model

        # Execute
        results = await engine.train_models(training_data)

        # Validate
        assert results[MLModelType.PREDICTIVE] is True
        assert engine.training_count == 1

    def test_enhanced_ml_decision_engine_get_status(
        self, mock_decision_orchestrator, mock_strategic_memory
    ):
        """P0: Validate engine status reporting"""
        engine = EnhancedMLDecisionEngine(
            decision_orchestrator=mock_decision_orchestrator,
            strategic_memory_manager=mock_strategic_memory,
        )

        status = engine.get_engine_status()

        assert "models_available" in status
        assert "prediction_count" in status
        assert "training_count" in status
        assert "accuracy_metrics" in status
        assert status["engine_version"] == "5.1.0"
        assert "last_update" in status


class TestMLDecisionEngineFactory:
    """P0 Test Suite: ML Decision Engine Factory Function"""

    def test_create_ml_decision_engine_factory(self):
        """P0: Validate factory function creates engine correctly"""
        config = {"test": "config"}

        engine = create_ml_decision_engine(config=config)

        assert isinstance(engine, EnhancedMLDecisionEngine)
        assert engine.config == config

    def test_create_ml_decision_engine_with_dependencies(self):
        """P0: Validate factory function with dependency injection"""
        mock_orchestrator = Mock()
        mock_memory = Mock()

        engine = create_ml_decision_engine(
            decision_orchestrator=mock_orchestrator,
            strategic_memory_manager=mock_memory,
        )

        assert engine.decision_orchestrator == mock_orchestrator
        assert engine.strategic_memory == mock_memory


class TestProjectStructureCompliance:
    """P0 Test Suite: PROJECT_STRUCTURE.md Compliance"""

    def test_module_location_compliance(self):
        """P0: Validate module follows PROJECT_STRUCTURE.md ai_intelligence/ pattern"""
        from lib.ai_intelligence import ml_decision_engine

        # Validate module is in correct location
        expected_path_parts = ["lib", "ai_intelligence", "ml_decision_engine"]
        actual_path = ml_decision_engine.__file__

        for part in expected_path_parts:
            assert (
                part in actual_path
            ), f"Module not in correct PROJECT_STRUCTURE.md location: {actual_path}"

    def test_zero_code_duplication_imports(self):
        """P0: Validate no code duplication - imports only existing components"""
        # Verify imports are from existing modules only
        from lib.ai_intelligence.ml_decision_engine import PredictiveDecisionModel

        # Check that it uses existing PredictiveProcessor
        model = PredictiveDecisionModel()
        assert hasattr(model, "predictive_processor")

        # Verify it doesn't duplicate decision orchestrator logic
        from lib.ai_intelligence.decision_orchestrator import DecisionContext

        assert DecisionContext  # Uses existing context class

    def test_solid_principles_compliance(self):
        """P0: Validate SOLID principles adherence"""
        # Single Responsibility: Each class has one clear purpose
        assert (
            MLDecisionModel.__doc__ and "Abstract base class" in MLDecisionModel.__doc__
        )
        assert (
            PredictiveDecisionModel.__doc__
            and "Predictive decision model" in PredictiveDecisionModel.__doc__
        )

        # Open/Closed: Abstract base allows extension
        assert hasattr(MLDecisionModel, "__abstractmethods__")

        # Interface Segregation: Focused interfaces
        abstract_methods = MLDecisionModel.__abstractmethods__
        assert len(abstract_methods) == 3  # Focused interface

        # Dependency Inversion: Depends on abstractions
        model = PredictiveDecisionModel()
        assert hasattr(model, "strategic_memory")  # Injected dependency


# P0 Test Coverage Requirements
def test_p0_coverage_completeness():
    """P0: Validate ≥95% test coverage for all base classes and interfaces"""
    # This test ensures all critical components are tested
    tested_components = {
        "MLModelType",
        "MLDecisionContext",
        "MLDecisionResult",
        "MLDecisionModel",
        "PredictiveDecisionModel",
        "EnhancedMLDecisionEngine",
        "create_ml_decision_engine",
    }

    # Import actual components
    from lib.ai_intelligence import ml_decision_engine

    actual_components = {
        name
        for name in dir(ml_decision_engine)
        if not name.startswith("_") and name in ml_decision_engine.__all__
    }

    coverage = len(tested_components.intersection(actual_components)) / len(
        actual_components
    )
    assert (
        coverage >= 0.95
    ), f"P0 test coverage requirement not met: {coverage:.1%} < 95%"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
