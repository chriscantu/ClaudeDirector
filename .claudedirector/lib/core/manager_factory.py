"""
Manager Factory System

Consolidated factory and registry system for all manager types.
Eliminates duplicate factory functions and instantiation patterns across 32+ managers.

Author: Martin | Platform Architecture
Phase: 8.1 - Manager Pattern Consolidation
Compliance: PROJECT_STRUCTURE.md + BLOAT_PREVENTION_SYSTEM.md
"""

import logging
import sys
from typing import Dict, Any, Optional, Type, Union, List
from pathlib import Path
from threading import Lock
from datetime import datetime

# Import manager types and base classes
try:
    from .base_manager import BaseManager, BaseManagerConfig, ManagerType
    from .manager_types import (
        ManagerRegistration,
        ManagerPriority,
        ManagerState,
        ManagerFactory as ManagerFactoryProtocol,
        MANAGER_PRIORITY_MAP,
        get_manager_priority,
        validate_manager_config,
    )
    from .models import ValidationError
except ImportError:
    # Fallback for test environments
    sys.path.insert(0, str(Path(__file__).parent.parent))
    try:
        from base_manager import BaseManager, BaseManagerConfig, ManagerType
        from manager_types import (
            ManagerRegistration,
            ManagerPriority,
            ManagerState,
            ManagerFactoryProtocol,
            MANAGER_PRIORITY_MAP,
            get_manager_priority,
            validate_manager_config,
        )
        from models import ValidationError
    except ImportError:
        # Mock for isolated testing
        class ValidationError(Exception):
            pass

        class ManagerRegistration:
            pass

        class ManagerPriority:
            CRITICAL = 1
            HIGH = 2
            MEDIUM = 3
            LOW = 4


class ManagerRegistry:
    """
    Thread-safe registry for manager types and instances

    Consolidates manager registration patterns and provides
    centralized manager lifecycle management.
    """

    def __init__(self):
        self._registrations: Dict[ManagerType, ManagerRegistration] = {}
        self._instances: Dict[str, BaseManager] = {}  # manager_name -> instance
        self._lock = Lock()
        self._initialized = False

    def register(self, registration: ManagerRegistration) -> bool:
        """
        Register a manager type

        Args:
            registration: Manager registration information

        Returns:
            bool: True if registered successfully
        """
        with self._lock:
            if registration.manager_type in self._registrations:
                existing = self._registrations[registration.manager_type]
                if existing.manager_class != registration.manager_class:
                    raise ValueError(
                        f"Manager type {registration.manager_type} already registered "
                        f"with different class: {existing.manager_class}"
                    )
                return False  # Already registered

            # Validate registration
            if not issubclass(registration.manager_class, BaseManager):
                raise ValueError(
                    f"Manager class {registration.manager_class} must inherit from BaseManager"
                )

            self._registrations[registration.manager_type] = registration
            return True

    def unregister(self, manager_type: ManagerType) -> bool:
        """Unregister a manager type"""
        with self._lock:
            if manager_type in self._registrations:
                del self._registrations[manager_type]
                return True
            return False

    def get_registration(
        self, manager_type: ManagerType
    ) -> Optional[ManagerRegistration]:
        """Get registration for manager type"""
        with self._lock:
            return self._registrations.get(manager_type)

    def get_all_registrations(self) -> Dict[ManagerType, ManagerRegistration]:
        """Get all registered manager types"""
        with self._lock:
            return self._registrations.copy()

    def is_registered(self, manager_type: ManagerType) -> bool:
        """Check if manager type is registered"""
        with self._lock:
            return manager_type in self._registrations

    def register_instance(self, manager_name: str, instance: BaseManager):
        """Register manager instance"""
        with self._lock:
            self._instances[manager_name] = instance

    def unregister_instance(self, manager_name: str) -> bool:
        """Unregister manager instance"""
        with self._lock:
            if manager_name in self._instances:
                del self._instances[manager_name]
                return True
            return False

    def get_instance(self, manager_name: str) -> Optional[BaseManager]:
        """Get registered manager instance"""
        with self._lock:
            return self._instances.get(manager_name)

    def get_all_instances(self) -> Dict[str, BaseManager]:
        """Get all registered instances"""
        with self._lock:
            return self._instances.copy()

    def get_instances_by_type(self, manager_type: ManagerType) -> List[BaseManager]:
        """Get all instances of specific manager type"""
        with self._lock:
            instances = []
            for instance in self._instances.values():
                if instance.config.manager_type == manager_type:
                    instances.append(instance)
            return instances

    def clear(self):
        """Clear all registrations and instances"""
        with self._lock:
            self._registrations.clear()
            self._instances.clear()


class ConsolidatedManagerFactory:
    """
    Consolidated factory for all manager types

    Eliminates duplicate factory functions across the codebase by providing
    a single, unified factory with type registry and dependency resolution.

    Features:
    - Type registration and validation
    - Dependency resolution
    - Instance lifecycle management
    - Configuration validation
    - Error handling and recovery
    """

    def __init__(self, registry: Optional[ManagerRegistry] = None):
        self.registry = registry or ManagerRegistry()
        self._creation_lock = Lock()
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

        # Initialize with default manager registrations
        self._register_default_managers()

    def _register_default_managers(self):
        """Register default manager types that are always available"""
        # This will be populated as we refactor existing managers
        # For now, we define the structure without hard-coding classes
        pass

    def register_manager_type(
        self,
        manager_type: ManagerType,
        manager_class: Type[BaseManager],
        priority: Optional[ManagerPriority] = None,
        dependencies: Optional[List[ManagerType]] = None,
        config_schema: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
    ) -> bool:
        """
        Register a manager type with the factory

        Args:
            manager_type: Type of manager to register
            manager_class: Manager class (must inherit from BaseManager)
            priority: Manager priority for initialization ordering
            dependencies: List of manager types this manager depends on
            config_schema: Optional configuration schema for validation
            description: Human-readable description

        Returns:
            bool: True if registered successfully
        """
        if priority is None:
            priority = get_manager_priority(manager_type)

        registration = ManagerRegistration(
            manager_type=manager_type,
            manager_class=manager_class,
            priority=priority,
            dependencies=dependencies or [],
            config_schema=config_schema,
            description=description,
        )

        return self.registry.register(registration)

    def create_manager(
        self,
        manager_type: Union[str, ManagerType],
        config: BaseManagerConfig,
        register_instance: bool = True,
        **kwargs,
    ) -> BaseManager:
        """
        Create manager instance

        Args:
            manager_type: Type of manager to create (string or ManagerType)
            config: Manager configuration
            register_instance: Whether to register instance in registry
            **kwargs: Additional arguments for manager constructor

        Returns:
            BaseManager: Created manager instance

        Raises:
            ValueError: If manager type not registered or configuration invalid
            RuntimeError: If manager creation fails
        """
        with self._creation_lock:
            # Convert string to ManagerType if needed
            if isinstance(manager_type, str):
                try:
                    manager_type = ManagerType(manager_type.lower())
                except ValueError:
                    # Try to find by name
                    for mt in ManagerType:
                        if mt.name.lower() == manager_type.lower():
                            manager_type = mt
                            break
                    else:
                        raise ValueError(f"Unknown manager type: {manager_type}")

            # Get registration
            registration = self.registry.get_registration(manager_type)
            if not registration:
                raise ValueError(f"Manager type {manager_type} not registered")

            # Validate configuration
            validate_manager_config(config)

            # Set manager type in config if not already set
            if config.manager_type is None:
                config.manager_type = manager_type

            try:
                # Create manager instance
                self._logger.info(
                    f"Creating manager instance",
                    manager_type=manager_type.value,
                    manager_name=config.manager_name,
                    manager_class=registration.manager_class.__name__,
                )

                instance = registration.manager_class(config, **kwargs)

                # Register instance if requested
                if register_instance:
                    self.registry.register_instance(config.manager_name, instance)

                self._logger.info(
                    f"Manager instance created successfully",
                    manager_type=manager_type.value,
                    manager_name=config.manager_name,
                )

                return instance

            except Exception as e:
                self._logger.error(
                    f"Failed to create manager instance",
                    manager_type=manager_type.value,
                    manager_name=config.manager_name,
                    error=str(e),
                )
                raise RuntimeError(
                    f"Failed to create {manager_type.value} manager: {e}"
                ) from e

    def get_or_create_manager(
        self, manager_type: Union[str, ManagerType], config: BaseManagerConfig, **kwargs
    ) -> BaseManager:
        """
        Get existing manager instance or create new one

        Args:
            manager_type: Type of manager
            config: Manager configuration
            **kwargs: Additional arguments for manager constructor

        Returns:
            BaseManager: Existing or new manager instance
        """
        # Check if instance already exists
        existing = self.registry.get_instance(config.manager_name)
        if existing:
            return existing

        # Create new instance
        return self.create_manager(manager_type, config, **kwargs)

    def create_managers_by_priority(
        self, configs: List[BaseManagerConfig], **kwargs
    ) -> Dict[str, BaseManager]:
        """
        Create multiple managers in priority order

        Args:
            configs: List of manager configurations
            **kwargs: Additional arguments for manager constructors

        Returns:
            Dict[str, BaseManager]: Created managers by name
        """
        managers = {}

        # Group configs by priority
        priority_groups = {}
        for config in configs:
            if config.manager_type:
                priority = get_manager_priority(config.manager_type)
                if priority not in priority_groups:
                    priority_groups[priority] = []
                priority_groups[priority].append(config)

        # Create managers in priority order
        for priority in sorted(priority_groups.keys(), key=lambda p: p.value):
            for config in priority_groups[priority]:
                try:
                    manager = self.create_manager(config.manager_type, config, **kwargs)
                    managers[config.manager_name] = manager
                except Exception as e:
                    self._logger.error(
                        f"Failed to create manager in priority group",
                        manager_name=config.manager_name,
                        priority=priority.name,
                        error=str(e),
                    )
                    # Continue with other managers

        return managers

    def destroy_manager(self, manager_name: str) -> bool:
        """
        Destroy manager instance

        Args:
            manager_name: Name of manager to destroy

        Returns:
            bool: True if destroyed successfully
        """
        instance = self.registry.get_instance(manager_name)
        if not instance:
            return False

        try:
            # Perform cleanup if manager supports it
            if hasattr(instance, "cleanup"):
                instance.cleanup()

            # Unregister from registry
            self.registry.unregister_instance(manager_name)

            self._logger.info(f"Manager destroyed", manager_name=manager_name)
            return True

        except Exception as e:
            self._logger.error(
                f"Failed to destroy manager", manager_name=manager_name, error=str(e)
            )
            return False

    def get_registered_types(self) -> Dict[ManagerType, ManagerRegistration]:
        """Get all registered manager types"""
        return self.registry.get_all_registrations()

    def get_active_managers(self) -> Dict[str, BaseManager]:
        """Get all active manager instances"""
        return self.registry.get_all_instances()

    def get_manager_status(self, manager_name: str) -> Optional[Dict[str, Any]]:
        """Get status of specific manager"""
        instance = self.registry.get_instance(manager_name)
        if instance:
            return instance.get_status()
        return None

    def get_all_manager_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all active managers"""
        status = {}
        for name, instance in self.registry.get_all_instances().items():
            try:
                status[name] = instance.get_status()
            except Exception as e:
                status[name] = {"error": str(e), "healthy": False}
        return status

    def health_check_all(self) -> Dict[str, bool]:
        """Perform health check on all active managers"""
        health_status = {}
        for name, instance in self.registry.get_all_instances().items():
            try:
                health_status[name] = instance.health_check()
            except Exception:
                health_status[name] = False
        return health_status

    def reset_all_metrics(self):
        """Reset metrics for all active managers"""
        for instance in self.registry.get_all_instances().values():
            try:
                instance.reset_metrics()
            except Exception as e:
                self._logger.warning(
                    f"Failed to reset metrics for manager",
                    manager_name=instance.config.manager_name,
                    error=str(e),
                )

    def clear_all_caches(self):
        """Clear caches for all active managers"""
        for instance in self.registry.get_all_instances().values():
            try:
                instance.clear_cache()
            except Exception as e:
                self._logger.warning(
                    f"Failed to clear cache for manager",
                    manager_name=instance.config.manager_name,
                    error=str(e),
                )


# Global factory instance
_global_factory: Optional[ConsolidatedManagerFactory] = None
_factory_lock = Lock()


def get_manager_factory() -> ConsolidatedManagerFactory:
    """
    Get global manager factory instance (singleton pattern)

    Returns:
        ConsolidatedManagerFactory: Global factory instance
    """
    global _global_factory

    if _global_factory is None:
        with _factory_lock:
            if _global_factory is None:
                _global_factory = ConsolidatedManagerFactory()

    return _global_factory


def create_manager(
    manager_type: Union[str, ManagerType], manager_name: str, **config_kwargs
) -> BaseManager:
    """
    Convenience function to create manager with default factory

    Args:
        manager_type: Type of manager to create
        manager_name: Name for the manager instance
        **config_kwargs: Configuration options

    Returns:
        BaseManager: Created manager instance
    """
    # Create configuration
    config = BaseManagerConfig(
        manager_name=manager_name,
        manager_type=manager_type if isinstance(manager_type, ManagerType) else None,
        **config_kwargs,
    )

    # Use global factory
    factory = get_manager_factory()
    return factory.create_manager(manager_type, config)


def register_manager_type(
    manager_type: ManagerType, manager_class: Type[BaseManager], **kwargs
) -> bool:
    """
    Convenience function to register manager type with default factory

    Args:
        manager_type: Type of manager to register
        manager_class: Manager class
        **kwargs: Additional registration options

    Returns:
        bool: True if registered successfully
    """
    factory = get_manager_factory()
    return factory.register_manager_type(manager_type, manager_class, **kwargs)


def get_manager(manager_name: str) -> Optional[BaseManager]:
    """
    Convenience function to get manager instance by name

    Args:
        manager_name: Name of manager to retrieve

    Returns:
        BaseManager or None: Manager instance if found
    """
    factory = get_manager_factory()
    return factory.registry.get_instance(manager_name)


def destroy_manager(manager_name: str) -> bool:
    """
    Convenience function to destroy manager instance

    Args:
        manager_name: Name of manager to destroy

    Returns:
        bool: True if destroyed successfully
    """
    factory = get_manager_factory()
    return factory.destroy_manager(manager_name)
