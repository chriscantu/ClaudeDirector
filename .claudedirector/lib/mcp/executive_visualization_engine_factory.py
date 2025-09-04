#!/usr/bin/env python3
"""
🎯 STORY 2.2.3: EXECUTIVE VISUALIZATION ENGINE FACTORY ELIMINATION

REPLACED: ExecutiveVisualizationEngineFactory (161 lines) → UnifiedFactory delegation
ELIMINATES: Duplicate factory registry, engine creation, configuration mapping

All executive visualization engine creation now delegated to UnifiedFactory for DRY compliance.
Maintains 100% API compatibility while eliminating factory duplication.
"""

import logging
from typing import Dict, Any

# Import UnifiedFactory for elimination-first consolidation
from ..core.unified_factory import UnifiedFactory, ComponentType, get_unified_factory

logger = logging.getLogger(__name__)


class ExecutiveVisualizationEngineFactory:
    """
    🎯 STORY 2.2.3: EXECUTIVE VISUALIZATION ENGINE FACTORY ELIMINATION

    ULTRA-LIGHTWEIGHT FACADE - All logic delegated to UnifiedFactory
    ELIMINATES: 161+ lines of duplicate factory logic
    MAINTAINS: 100% API compatibility for backward compatibility
    """

    def __init__(self):
        """
        🎯 STORY 2.2.3: ELIMINATION-FIRST INITIALIZATION
        All complex factory logic delegated to UnifiedFactory
        """
        self.logger = logger

        # Get unified factory instance for delegation
        self.unified_factory = get_unified_factory()

        self.logger.info(
            "executive_visualization_engine_factory_facade_initialized",
            pattern="ultra_lightweight_facade",
            delegation_target="UnifiedFactory",
            eliminated_lines="161+",
            api_compatibility="100%",
        )

    @staticmethod
    def create_engine_components() -> Dict[str, Any]:
        """Create and configure all engine components and dependencies"""
        # Delegate to UnifiedFactory - ELIMINATES duplicate logic
        unified_factory = get_unified_factory()
        return unified_factory.create_component(
            ComponentType.EXECUTIVE_VISUALIZATION_ENGINE,
            {"component_type": "engine_components"},
        )

    @staticmethod
    def create_processors(components: Dict[str, Any]) -> Dict[str, Any]:
        """Create and configure all processors based on engine components"""
        # Delegate to UnifiedFactory - ELIMINATES duplicate logic
        unified_factory = get_unified_factory()
        return unified_factory.create_component(
            ComponentType.EXECUTIVE_VISUALIZATION_ENGINE,
            {"component_type": "processors", "components": components},
        )

    @staticmethod
    def create_orchestration_processor(
        processors: Dict[str, Any], components: Dict[str, Any]
    ) -> Any:
        """Create the main orchestration processor with all dependencies"""
        # Delegate to UnifiedFactory - ELIMINATES duplicate logic
        unified_factory = get_unified_factory()
        return unified_factory.create_component(
            ComponentType.EXECUTIVE_VISUALIZATION_ENGINE,
            {
                "component_type": "orchestration_processor",
                "processors": processors,
                "components": components,
            },
        )

    @classmethod
    def initialize_engine(cls, engine_instance):
        """🏗️ Complete engine initialization using factory pattern"""
        # Delegate to UnifiedFactory - ELIMINATES duplicate logic
        unified_factory = get_unified_factory()
        return unified_factory.create_component(
            ComponentType.EXECUTIVE_VISUALIZATION_ENGINE,
            {"component_type": "initialize_engine", "engine_instance": engine_instance},
        )
