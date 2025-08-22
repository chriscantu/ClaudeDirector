"""
P0 AI Model Factory - SOLID Implementation

Martin's factory pattern implementation following Open/Closed Principle.
Enables extension with new AI models without modifying existing code.
"""

from typing import Dict, Any, Optional, Type, Union, List
import structlog

from ..shared.ai_core.interfaces import (
    ModelFactory,
    IDecisionIntelligenceEngine,
    IHealthPredictionEngine,
    AIModelType,
)
from ..shared.infrastructure.config import (
    get_config,
    P0FeatureConfig,
    DecisionDetectionConfig,
    HealthPredictionConfig,
)
from ..domains.decision_intelligence.engine import DecisionIntelligenceEngine
from ..domains.health_assessment.engine import HealthAssessmentEngine

logger = structlog.get_logger(__name__)


class P0ModelFactory(ModelFactory):
    """
    Concrete factory for P0 AI models

    Open/Closed Principle: Can be extended with new models without modification
    Single Responsibility: Focuses only on model creation and configuration
    """

    def __init__(self, config: Optional[P0FeatureConfig] = None):
        """
        Initialize factory with configuration dependency injection
        """
        self.config = config or get_config()
        self.logger = logger.bind(component="model_factory")

        # Registry of supported models (Open/Closed - extensible)
        self._model_registry: Dict[AIModelType, Type] = {
            AIModelType.DECISION_INTELLIGENCE: DecisionIntelligenceEngine,
            AIModelType.HEALTH_PREDICTION: HealthAssessmentEngine,
        }

        # Configuration mapping
        self._config_mapping = {
            AIModelType.DECISION_INTELLIGENCE: self.config.decision_detection,
            AIModelType.HEALTH_PREDICTION: self.config.health_prediction,
        }

    def create_decision_engine(
        self, config: Optional[Dict[str, Any]] = None
    ) -> IDecisionIntelligenceEngine:
        """
        Create decision intelligence engine with configuration injection

        Args:
            config: Optional configuration overrides

        Returns:
            IDecisionIntelligenceEngine: Configured decision engine

        Raises:
            ValueError: If decision intelligence is disabled or unsupported
        """
        if not self.config.enable_decision_intelligence:
            raise ValueError("Decision intelligence is disabled in configuration")

        try:
            # Get base configuration
            base_config = self._config_mapping[AIModelType.DECISION_INTELLIGENCE]

            # Apply configuration overrides if provided
            if config:
                # Create a copy to avoid mutating the base config
                engine_config = DecisionDetectionConfig(
                    **{**base_config.dict(), **config}
                )
            else:
                engine_config = base_config

            # Create engine with dependency injection
            engine = DecisionIntelligenceEngine(config=engine_config)

            self.logger.info(
                "Decision intelligence engine created",
                model_name=engine_config.model_name,
                accuracy_threshold=engine_config.accuracy_threshold,
            )

            return engine

        except Exception as e:
            self.logger.error(
                "Failed to create decision intelligence engine", error=str(e)
            )
            raise ValueError(f"Failed to create decision engine: {str(e)}")

    def create_health_engine(
        self, config: Optional[Dict[str, Any]] = None
    ) -> IHealthPredictionEngine:
        """
        Create health prediction engine with configuration injection

        Args:
            config: Optional configuration overrides

        Returns:
            IHealthPredictionEngine: Configured health engine

        Raises:
            ValueError: If health prediction is disabled or unsupported
        """
        if not self.config.enable_health_prediction:
            raise ValueError("Health prediction is disabled in configuration")

        try:
            # Get base configuration
            base_config = self._config_mapping[AIModelType.HEALTH_PREDICTION]

            # Apply configuration overrides if provided
            if config:
                # Create a copy to avoid mutating the base config
                engine_config = HealthPredictionConfig(
                    **{**base_config.dict(), **config}
                )
            else:
                engine_config = base_config

            # Create engine with dependency injection
            engine = HealthAssessmentEngine(
                config=engine_config, recommendation_config=self.config.recommendations
            )

            self.logger.info(
                "Health assessment engine created",
                model_name=engine_config.model_name,
                accuracy_threshold=engine_config.accuracy_threshold,
            )

            return engine

        except Exception as e:
            self.logger.error("Failed to create health assessment engine", error=str(e))
            raise ValueError(f"Failed to create health engine: {str(e)}")

    def supports_model_type(self, model_type: AIModelType) -> bool:
        """
        Check if factory supports the specified model type

        Args:
            model_type: AI model type to check

        Returns:
            bool: True if model type is supported
        """
        return model_type in self._model_registry

    def get_supported_models(self) -> List[AIModelType]:
        """Get list of supported model types"""
        return list(self._model_registry.keys())

    def register_model(self, model_type: AIModelType, model_class: Type) -> None:
        """
        Register a new model type (Open/Closed Principle extension point)

        Args:
            model_type: AI model type identifier
            model_class: Model implementation class
        """
        self._model_registry[model_type] = model_class
        self.logger.info(
            "New model type registered",
            model_type=model_type.value,
            model_class=model_class.__name__,
        )

    def create_model(
        self, model_type: AIModelType, config: Optional[Dict[str, Any]] = None
    ) -> Union[IDecisionIntelligenceEngine, IHealthPredictionEngine]:
        """
        Generic model creation method

        Args:
            model_type: Type of model to create
            config: Optional configuration overrides

        Returns:
            AI engine instance

        Raises:
            ValueError: If model type is not supported
        """
        if model_type == AIModelType.DECISION_INTELLIGENCE:
            return self.create_decision_engine(config)
        elif model_type == AIModelType.HEALTH_PREDICTION:
            return self.create_health_engine(config)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


class ModelFactoryRegistry:
    """
    Registry for model factories (Singleton pattern)

    Enables multiple factory implementations while maintaining global access
    """

    _instance: Optional["ModelFactoryRegistry"] = None
    _factories: Dict[str, ModelFactory] = {}

    def __new__(cls) -> "ModelFactoryRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_factory(cls, factory_name: str = "default") -> ModelFactory:
        """
        Get model factory by name

        Args:
            factory_name: Name of factory to retrieve

        Returns:
            ModelFactory: Factory instance
        """
        if factory_name not in cls._factories:
            if factory_name == "default":
                cls._factories[factory_name] = P0ModelFactory()
            else:
                raise ValueError(f"Unknown factory: {factory_name}")

        return cls._factories[factory_name]

    @classmethod
    def register_factory(cls, name: str, factory: ModelFactory) -> None:
        """
        Register a new factory implementation

        Args:
            name: Factory name
            factory: Factory implementation
        """
        cls._factories[name] = factory
        logger.info(
            "Model factory registered", name=name, factory_type=type(factory).__name__
        )

    @classmethod
    def list_factories(cls) -> List[str]:
        """Get list of registered factory names"""
        return list(cls._factories.keys())


# Convenience functions for easy access


def get_model_factory(factory_name: str = "default") -> ModelFactory:
    """
    Get model factory instance

    Args:
        factory_name: Name of factory to retrieve

    Returns:
        ModelFactory: Factory instance
    """
    return ModelFactoryRegistry.get_factory(factory_name)


def create_decision_engine(
    config: Optional[Dict[str, Any]] = None,
) -> IDecisionIntelligenceEngine:
    """
    Convenience function to create decision intelligence engine

    Args:
        config: Optional configuration overrides

    Returns:
        IDecisionIntelligenceEngine: Configured decision engine
    """
    factory = get_model_factory()
    return factory.create_decision_engine(config)


def create_health_engine(
    config: Optional[Dict[str, Any]] = None,
) -> IHealthPredictionEngine:
    """
    Convenience function to create health prediction engine

    Args:
        config: Optional configuration overrides

    Returns:
        IHealthPredictionEngine: Configured health engine
    """
    factory = get_model_factory()
    return factory.create_health_engine(config)


class MockModelFactory(ModelFactory):
    """
    Mock factory for testing (Test Double pattern)

    Enables testing without real AI models
    """

    def __init__(self):
        self.logger = logger.bind(component="mock_factory")

    def create_decision_engine(
        self, config: Optional[Dict[str, Any]] = None
    ) -> IDecisionIntelligenceEngine:
        """Create mock decision engine for testing"""
        from ..testing.mocks import MockDecisionEngine

        return MockDecisionEngine(config or {})

    def create_health_engine(
        self, config: Optional[Dict[str, Any]] = None
    ) -> IHealthPredictionEngine:
        """Create mock health engine for testing"""
        from ..testing.mocks import MockHealthEngine

        return MockHealthEngine(config or {})

    def supports_model_type(self, model_type: AIModelType) -> bool:
        """Mock factory supports all model types"""
        return True


# Initialize default factory
def initialize_factories():
    """Initialize default model factories"""
    registry = ModelFactoryRegistry()

    # Register default factory
    if "default" not in registry.list_factories():
        registry.register_factory("default", P0ModelFactory())

    # Register mock factory for testing
    if "mock" not in registry.list_factories():
        registry.register_factory("mock", MockModelFactory())


# Auto-initialize on module import
initialize_factories()
