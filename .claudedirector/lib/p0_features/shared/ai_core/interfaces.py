"""
SOLID-Compliant AI Interfaces

Martin's interface segregation implementation following SOLID principles.
Minimal, focused interfaces enabling testability and extensibility.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from ..infrastructure.config import AIModelType, PerformanceThresholds


class InferenceResult(Protocol):
    """Protocol for AI inference results"""
    success: bool
    confidence: float
    processing_time_ms: int
    error: Optional[str]


class ValidationResult(Protocol):
    """Protocol for validation results"""
    accuracy: float
    test_cases: int
    passed: bool
    details: Dict[str, Any]


class PerformanceMetric(Protocol):
    """Protocol for performance metrics"""
    timestamp: str
    execution_time_ms: int
    confidence: float
    meets_time_sla: bool
    meets_accuracy_sla: bool


@runtime_checkable
class IInferenceEngine(Protocol):
    """
    Core inference interface (Interface Segregation Principle)

    Focused solely on AI model inference without validation or monitoring concerns.
    """

    def predict(self, input_data: Any) -> InferenceResult:
        """
        Perform AI inference on input data

        Args:
            input_data: Model-specific input data

        Returns:
            InferenceResult with prediction and metadata
        """
        ...

    def load_model(self) -> bool:
        """
        Load AI model for inference

        Returns:
            bool: True if model loaded successfully
        """
        ...

    def is_model_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        ...


@runtime_checkable
class IModelValidator(Protocol):
    """
    Model validation interface (Interface Segregation Principle)

    Separated from inference to enable independent testing and validation.
    """

    def validate_accuracy(self, test_data: List[Any]) -> ValidationResult:
        """
        Validate model accuracy against labeled test dataset

        Args:
            test_data: List of (input, expected_output) tuples

        Returns:
            ValidationResult with accuracy metrics
        """
        ...

    def get_accuracy_history(self) -> List[float]:
        """Get historical accuracy measurements"""
        ...


@runtime_checkable
class IPerformanceMonitor(Protocol):
    """
    Performance monitoring interface (Interface Segregation Principle)

    Separated from inference to enable independent performance tracking.
    """

    def record_query_performance(self, query: str, execution_time_ms: int,
                                result_count: int, confidence: float) -> None:
        """Record performance metrics for a query"""
        ...

    def get_performance_metrics(self) -> List[PerformanceMetric]:
        """Get collected performance metrics"""
        ...

    def check_sla_compliance(self, thresholds: PerformanceThresholds) -> bool:
        """Check if recent performance meets SLA thresholds"""
        ...


@runtime_checkable
class IConfigurable(Protocol):
    """
    Configuration interface (Dependency Inversion Principle)

    Enables dependency injection of configuration without tight coupling.
    """

    def configure(self, config: Dict[str, Any]) -> None:
        """Apply configuration to component"""
        ...

    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration"""
        ...


class AIEngineBase(ABC):
    """
    Abstract base for AI engines implementing common patterns

    Follows Single Responsibility Principle - focuses only on common infrastructure.
    """

    def __init__(self, model_type: AIModelType):
        self.model_type = model_type
        self._model_loaded = False
        self._accuracy_history: List[float] = []
        self._performance_metrics: List[Dict[str, Any]] = []

    @abstractmethod
    def predict(self, input_data: Any) -> Dict[str, Any]:
        """Subclasses implement specific prediction logic"""

    @abstractmethod
    def load_model(self) -> bool:
        """Subclasses implement model loading"""

    def is_model_loaded(self) -> bool:
        """Check if model is ready for inference"""
        return self._model_loaded


class DecisionIntelligenceResult:
    """
    Strongly-typed result for decision intelligence

    Replaces generic dictionaries with type-safe data structures.
    """

    def __init__(self, success: bool, decisions: List[Dict[str, Any]],
                 overall_confidence: float, processing_time_ms: int,
                 error: Optional[str] = None):
        self.success = success
        self.decisions = decisions
        self.overall_confidence = overall_confidence
        self.processing_time_ms = processing_time_ms
        self.error = error
        self.decisions_detected = len(decisions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backwards compatibility"""
        result = {
            'success': self.success,
            'decisions_detected': self.decisions_detected,
            'decisions': self.decisions,
            'overall_confidence': self.overall_confidence,
            'processing_time_ms': self.processing_time_ms
        }
        if self.error:
            result['error'] = self.error
        return result


class HealthPredictionResult:
    """
    Strongly-typed result for health prediction

    Replaces generic dictionaries with type-safe data structures.
    """

    def __init__(self, success: bool, health_score: float, health_status: str,
                 risk_level: str, confidence: float, processing_time_ms: int,
                 health_components: Dict[str, float], risk_assessment: Dict[str, Any],
                 trend_analysis: Dict[str, Any], recommendations: List[Dict[str, Any]],
                 error: Optional[str] = None):
        self.success = success
        self.health_score = health_score
        self.health_status = health_status
        self.risk_level = risk_level
        self.confidence = confidence
        self.processing_time_ms = processing_time_ms
        self.health_components = health_components
        self.risk_assessment = risk_assessment
        self.trend_analysis = trend_analysis
        self.recommendations = recommendations
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for backwards compatibility"""
        result = {
            'success': self.success,
            'health_score': self.health_score,
            'health_status': self.health_status,
            'risk_level': self.risk_level,
            'confidence': self.confidence,
            'processing_time_ms': self.processing_time_ms,
            'health_components': self.health_components,
            'risk_assessment': self.risk_assessment,
            'trend_analysis': self.trend_analysis,
            'recommendations': self.recommendations
        }
        if self.error:
            result['error'] = self.error
        return result


@runtime_checkable
class IDecisionIntelligenceEngine(IInferenceEngine, IModelValidator, IPerformanceMonitor, IConfigurable, Protocol):
    """
    Composite interface for decision intelligence

    Combines focused interfaces without violating Interface Segregation.
    Clients can depend on only the interfaces they need.
    """

    def predict(self, text: str) -> DecisionIntelligenceResult:
        """Predict decisions from text content"""
        ...


@runtime_checkable
class IHealthPredictionEngine(IInferenceEngine, IModelValidator, IPerformanceMonitor, IConfigurable, Protocol):
    """
    Composite interface for health prediction

    Combines focused interfaces without violating Interface Segregation.
    Clients can depend on only the interfaces they need.
    """

    def predict(self, initiative_data: Dict[str, Any]) -> HealthPredictionResult:
        """Predict health status from initiative data"""
        ...


class ModelFactory(ABC):
    """
    Abstract factory for AI models (Open/Closed Principle)

    Enables extension with new models without modifying existing code.
    """

    @abstractmethod
    def create_decision_engine(self, config: Dict[str, Any]) -> IDecisionIntelligenceEngine:
        """Create decision intelligence engine"""

    @abstractmethod
    def create_health_engine(self, config: Dict[str, Any]) -> IHealthPredictionEngine:
        """Create health prediction engine"""

    @abstractmethod
    def supports_model_type(self, model_type: AIModelType) -> bool:
        """Check if factory supports model type"""


class InferenceError(Exception):
    """Base exception for inference errors"""


class ModelNotLoadedError(InferenceError):
    """Exception raised when model is not loaded"""


class ValidationError(InferenceError):
    """Exception raised during validation"""


class PerformanceError(InferenceError):
    """Exception raised for performance violations"""
