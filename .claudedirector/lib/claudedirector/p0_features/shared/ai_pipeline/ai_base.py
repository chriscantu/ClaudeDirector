"""
AI Pipeline Base Classes - Architecture Foundation

Designed by Martin, implemented by Berny.
Provides base interfaces and configuration for all AI components.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from pathlib import Path
import structlog

logger = structlog.get_logger(__name__)


@dataclass
class AIModelConfig:
    """Configuration for AI models with performance requirements"""

    model_name: str
    accuracy_threshold: float = 0.85  # Berny's requirement: >85% accuracy
    max_inference_time_ms: int = 200  # Performance requirement
    model_path: Optional[Path] = None
    cache_size: int = 1000
    retrain_interval_days: int = 30
    validation_split: float = 0.2

    # Model-specific parameters
    parameters: Dict[str, Any] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


class AIEngineBase(ABC):
    """
    Base class for all AI engines in P0 features.

    Design Philosophy:
    - Zero-config for end users (models auto-download and configure)
    - Performance-first (sub-200ms inference time)
    - Accuracy-driven (>85% threshold for production use)
    - Evolutionary (models improve through usage)
    """

    def __init__(self, config: AIModelConfig):
        self.config = config
        self.logger = logger.bind(ai_engine=self.__class__.__name__)
        self._model = None
        self._accuracy_history: List[float] = []

    @abstractmethod
    def load_model(self) -> bool:
        """
        Load or initialize the AI model.

        Returns:
            bool: True if model loaded successfully

        Implementation by Berny:
        - Auto-download pre-trained models if not available
        - Fallback to rule-based implementation if model fails
        - Performance validation during load
        """

    @abstractmethod
    def predict(self, input_data: Any) -> Dict[str, Any]:
        """
        Make prediction with performance and accuracy guarantees.

        Args:
            input_data: Model-specific input format

        Returns:
            Dict with prediction results including confidence scores

        Performance Requirements:
        - <200ms inference time
        - >85% accuracy on validation set
        - Graceful degradation if performance drops
        """

    @abstractmethod
    def validate_accuracy(self, test_data: List[Any]) -> float:
        """
        Validate model accuracy against test dataset.

        Args:
            test_data: Validation dataset

        Returns:
            float: Accuracy score (0.0-1.0)

        Berny Implementation Notes:
        - Use stratified sampling for balanced validation
        - Track accuracy trends over time
        - Trigger retraining if accuracy drops below threshold
        """

    def get_model_health(self) -> Dict[str, Any]:
        """Get comprehensive model health metrics"""
        return {
            "accuracy_current": (
                self._accuracy_history[-1] if self._accuracy_history else 0.0
            ),
            "accuracy_trend": self._calculate_accuracy_trend(),
            "performance_status": self._check_performance_status(),
            "model_age_days": self._get_model_age_days(),
            "needs_retraining": self._needs_retraining(),
        }

    def _calculate_accuracy_trend(self) -> str:
        """Calculate accuracy trend over recent predictions"""
        if len(self._accuracy_history) < 5:
            return "insufficient_data"

        recent = self._accuracy_history[-5:]
        trend = (recent[-1] - recent[0]) / len(recent)

        if trend > 0.02:
            return "improving"
        elif trend < -0.02:
            return "declining"
        else:
            return "stable"

    def _check_performance_status(self) -> str:
        """Check if model meets performance requirements"""
        if not self._accuracy_history:
            return "not_evaluated"

        current_accuracy = self._accuracy_history[-1]

        if current_accuracy >= self.config.accuracy_threshold:
            return "excellent"
        elif current_accuracy >= self.config.accuracy_threshold - 0.05:
            return "acceptable"
        else:
            return "needs_improvement"

    def _get_model_age_days(self) -> int:
        """Get model age in days (implementation specific)"""
        # Override in specific implementations
        return 0

    def _needs_retraining(self) -> bool:
        """Determine if model needs retraining"""
        if not self._accuracy_history:
            return False

        # Retrain if accuracy below threshold or declining trend
        current_accuracy = self._accuracy_history[-1]
        trend = self._calculate_accuracy_trend()

        return current_accuracy < self.config.accuracy_threshold or trend == "declining"


class StrategicIntelligenceResult:
    """Standard result format for all strategic intelligence operations"""

    def __init__(
        self,
        success: bool,
        confidence: float,
        result_data: Dict[str, Any],
        processing_time_ms: int,
        model_version: str = "unknown",
    ):
        self.success = success
        self.confidence = confidence
        self.result_data = result_data
        self.processing_time_ms = processing_time_ms
        self.model_version = model_version
        self.meets_performance_sla = processing_time_ms < 200
        self.meets_confidence_threshold = confidence >= 0.85

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for API responses"""
        return {
            "success": self.success,
            "confidence": self.confidence,
            "result_data": self.result_data,
            "processing_time_ms": self.processing_time_ms,
            "model_version": self.model_version,
            "performance_sla_met": self.meets_performance_sla,
            "confidence_threshold_met": self.meets_confidence_threshold,
        }
