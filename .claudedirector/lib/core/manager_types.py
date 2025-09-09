"""
Manager Types and Utilities

Provides type definitions, utilities, and helper functions for the BaseManager system.
Eliminates duplicate type definitions across manager implementations.

Author: Martin | Platform Architecture
Phase: 8.1 - Manager Pattern Consolidation
"""

from typing import Dict, Any, Optional, Type, Union, Protocol, runtime_checkable
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Re-export core types for convenience
from .base_manager import ManagerType, BaseManagerConfig, BaseManager, ManagerProtocol


class ManagerPriority(Enum):
    """Manager priority levels for initialization and shutdown ordering"""

    CRITICAL = 1  # Core infrastructure (database, config, logging)
    HIGH = 2  # Performance and security managers
    MEDIUM = 3  # Application layer managers
    LOW = 4  # Specialized and optional managers


class ManagerState(Enum):
    """Manager lifecycle states"""

    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    STARTING = "starting"
    ACTIVE = "active"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    MAINTENANCE = "maintenance"


@dataclass
class ManagerRegistration:
    """Manager registration information for factory system"""

    manager_type: ManagerType
    manager_class: Type[BaseManager]
    priority: ManagerPriority
    dependencies: Optional[list] = None
    config_schema: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

    def __post_init__(self):
        """Validate registration data"""
        if self.dependencies is None:
            self.dependencies = []

        # Validate manager class
        if not issubclass(self.manager_class, BaseManager):
            raise ValueError(
                f"Manager class {self.manager_class} must inherit from BaseManager"
            )


@runtime_checkable
class ManagerFactory(Protocol):
    """Protocol for manager factory implementations"""

    def create_manager(
        self, manager_type: Union[str, ManagerType], config: BaseManagerConfig, **kwargs
    ) -> BaseManager:
        """Create manager instance"""
        ...

    def register_manager(self, registration: ManagerRegistration) -> bool:
        """Register manager type"""
        ...

    def get_registered_types(self) -> Dict[ManagerType, ManagerRegistration]:
        """Get all registered manager types"""
        ...


class ManagerOperationResult:
    """Result wrapper for manager operations"""

    def __init__(
        self,
        success: bool,
        result: Any = None,
        error: Optional[Exception] = None,
        operation: Optional[str] = None,
        duration: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.success = success
        self.result = result
        self.error = error
        self.operation = operation
        self.duration = duration
        self.metadata = metadata or {}

    def __bool__(self) -> bool:
        """Boolean evaluation based on success"""
        return self.success

    def __repr__(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        return f"ManagerOperationResult({status}, operation='{self.operation}')"


class ManagerConfigBuilder:
    """Builder pattern for BaseManagerConfig creation"""

    def __init__(self, manager_name: str, manager_type: Optional[ManagerType] = None):
        self._config_data = {"manager_name": manager_name, "manager_type": manager_type}

    def with_metrics(self, enabled: bool = True) -> "ManagerConfigBuilder":
        """Configure metrics tracking"""
        self._config_data["enable_metrics"] = enabled
        return self

    def with_caching(
        self, enabled: bool = True, ttl_seconds: int = 3600
    ) -> "ManagerConfigBuilder":
        """Configure caching"""
        self._config_data["enable_caching"] = enabled
        self._config_data["cache_ttl_seconds"] = ttl_seconds
        return self

    def with_logging(
        self, enabled: bool = True, level: str = "INFO"
    ) -> "ManagerConfigBuilder":
        """Configure logging"""
        self._config_data["enable_logging"] = enabled
        self._config_data["log_level"] = level
        return self

    def with_performance_tracking(self, enabled: bool = True) -> "ManagerConfigBuilder":
        """Configure performance tracking"""
        self._config_data["performance_tracking"] = enabled
        return self

    def with_error_recovery(
        self, enabled: bool = True, max_retries: int = 3
    ) -> "ManagerConfigBuilder":
        """Configure error recovery"""
        self._config_data["error_recovery"] = enabled
        self._config_data["max_retries"] = max_retries
        return self

    def with_timeout(self, seconds: int) -> "ManagerConfigBuilder":
        """Configure operation timeout"""
        self._config_data["timeout_seconds"] = seconds
        return self

    def with_custom_config(self, **kwargs) -> "ManagerConfigBuilder":
        """Add custom configuration values"""
        if "custom_config" not in self._config_data:
            self._config_data["custom_config"] = {}
        self._config_data["custom_config"].update(kwargs)
        return self

    def build(self) -> BaseManagerConfig:
        """Build the configuration"""
        return BaseManagerConfig(**self._config_data)


def create_manager_config(
    manager_name: str, manager_type: Optional[ManagerType] = None, **kwargs
) -> BaseManagerConfig:
    """
    Convenience function to create manager configuration

    Args:
        manager_name: Name of the manager instance
        manager_type: Type of manager (optional)
        **kwargs: Additional configuration options

    Returns:
        BaseManagerConfig: Configured manager config
    """
    config_data = {"manager_name": manager_name, "manager_type": manager_type, **kwargs}

    return BaseManagerConfig(**config_data)


def get_manager_type_from_string(type_str: str) -> Optional[ManagerType]:
    """
    Get ManagerType enum from string

    Args:
        type_str: String representation of manager type

    Returns:
        ManagerType or None if not found
    """
    try:
        return ManagerType(type_str.lower())
    except ValueError:
        # Try to find by name
        for manager_type in ManagerType:
            if manager_type.name.lower() == type_str.lower():
                return manager_type
        return None


def validate_manager_config(config: BaseManagerConfig) -> bool:
    """
    Validate manager configuration

    Args:
        config: Configuration to validate

    Returns:
        bool: True if valid

    Raises:
        ValueError: If configuration is invalid
    """
    if not config.manager_name:
        raise ValueError("Manager name is required")

    if not isinstance(config.manager_name, str):
        raise ValueError("Manager name must be a string")

    if config.timeout_seconds <= 0:
        raise ValueError("Timeout must be positive")

    if config.max_retries < 0:
        raise ValueError("Max retries cannot be negative")

    if config.cache_ttl_seconds < 0:
        raise ValueError("Cache TTL cannot be negative")

    return True


class ManagerMetrics:
    """Utility class for manager metrics operations"""

    @staticmethod
    def calculate_success_rate(success_count: int, total_count: int) -> float:
        """Calculate success rate percentage"""
        if total_count == 0:
            return 0.0
        return (success_count / total_count) * 100.0

    @staticmethod
    def calculate_average_duration(
        total_duration: float, operation_count: int
    ) -> float:
        """Calculate average operation duration"""
        if operation_count == 0:
            return 0.0
        return total_duration / operation_count

    @staticmethod
    def calculate_cache_hit_rate(hits: int, total_requests: int) -> float:
        """Calculate cache hit rate percentage"""
        if total_requests == 0:
            return 0.0
        return (hits / total_requests) * 100.0

    @staticmethod
    def format_metrics_summary(metrics: Dict[str, Any]) -> str:
        """Format metrics for human-readable display"""
        lines = []

        if "operations_count" in metrics:
            lines.append(f"Operations: {metrics['operations_count']}")

        if "success_rate" in metrics:
            lines.append(f"Success Rate: {metrics['success_rate']:.1f}%")

        if "average_processing_time" in metrics:
            lines.append(f"Avg Duration: {metrics['average_processing_time']:.3f}s")

        if "cache_hit_rate" in metrics:
            lines.append(f"Cache Hit Rate: {metrics['cache_hit_rate']:.1f}%")

        return " | ".join(lines)


# Manager type to priority mapping for initialization ordering
MANAGER_PRIORITY_MAP = {
    ManagerType.DATABASE: ManagerPriority.CRITICAL,
    ManagerType.CONFIGURATION: ManagerPriority.CRITICAL,
    ManagerType.LOGGING: ManagerPriority.CRITICAL,
    ManagerType.SECURITY: ManagerPriority.HIGH,
    ManagerType.PERFORMANCE: ManagerPriority.HIGH,
    ManagerType.CACHE: ManagerPriority.HIGH,
    ManagerType.MEMORY: ManagerPriority.HIGH,
    ManagerType.METRICS: ManagerPriority.HIGH,
    ManagerType.WORKSPACE: ManagerPriority.MEDIUM,
    ManagerType.FILE: ManagerPriority.MEDIUM,
    ManagerType.SESSION: ManagerPriority.MEDIUM,
    ManagerType.VALIDATION: ManagerPriority.MEDIUM,
    ManagerType.RESPONSE: ManagerPriority.MEDIUM,
    ManagerType.BACKUP: ManagerPriority.MEDIUM,
    ManagerType.MIGRATION: ManagerPriority.MEDIUM,
    ManagerType.THRESHOLD: ManagerPriority.MEDIUM,
    ManagerType.TRANSPARENCY: ManagerPriority.LOW,
    ManagerType.PERSONA: ManagerPriority.LOW,
    ManagerType.FRAMEWORK: ManagerPriority.LOW,
    ManagerType.MCP: ManagerPriority.LOW,
    ManagerType.ANALYTICS: ManagerPriority.LOW,
    ManagerType.CONTEXT: ManagerPriority.LOW,
    ManagerType.TEMPLATE: ManagerPriority.LOW,
    ManagerType.VISUALIZATION: ManagerPriority.LOW,
    ManagerType.INTEGRATION: ManagerPriority.LOW,
    ManagerType.WORKFLOW: ManagerPriority.LOW,
    ManagerType.NOTIFICATION: ManagerPriority.LOW,
    ManagerType.COMPLIANCE: ManagerPriority.LOW,
    ManagerType.ARCHIVE: ManagerPriority.LOW,
    ManagerType.SYNC: ManagerPriority.LOW,
    ManagerType.QUEUE: ManagerPriority.LOW,
    ManagerType.HEALTH: ManagerPriority.LOW,
}


def get_manager_priority(manager_type: ManagerType) -> ManagerPriority:
    """Get priority for manager type"""
    return MANAGER_PRIORITY_MAP.get(manager_type, ManagerPriority.LOW)
