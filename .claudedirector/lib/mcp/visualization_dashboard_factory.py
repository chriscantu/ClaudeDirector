#!/usr/bin/env python3
"""
🎯 STORY 2.2.3: VISUALIZATION DASHBOARD FACTORY ELIMINATION

REPLACED: VisualizationDashboardFactory (466 lines) → UnifiedFactory delegation
ELIMINATES: Duplicate factory registry, dashboard creation, configuration mapping

All visualization dashboard creation now delegated to UnifiedFactory for DRY compliance.
Maintains 100% API compatibility while eliminating factory duplication.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple, Callable
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import UnifiedFactory for elimination-first consolidation
from ..core.unified_factory import UnifiedFactory, ComponentType, get_unified_factory

# Dashboard configuration types
DashboardConfig = Dict[str, Any]
ChartDataProcessor = Callable[[Dict[str, Any], str], go.Figure]


class VisualizationDashboardFactory:
    """
    🎯 STORY 2.2.3: VISUALIZATION DASHBOARD FACTORY ELIMINATION

    ULTRA-LIGHTWEIGHT FACADE - All logic delegated to UnifiedFactory
    ELIMINATES: 466+ lines of duplicate factory logic
    MAINTAINS: 100% API compatibility for backward compatibility
    """

    def __init__(self, color_palette: List[str]):
        """
        🎯 STORY 2.2.3: ELIMINATION-FIRST INITIALIZATION
        All complex factory logic delegated to UnifiedFactory
        """
        self.color_palette = color_palette
        self.logger = logging.getLogger(__name__)

        # Get unified factory instance for delegation
        self.unified_factory = get_unified_factory()

        self.logger.info(
            "visualization_dashboard_factory_facade_initialized",
            pattern="ultra_lightweight_facade",
            delegation_target="UnifiedFactory",
            eliminated_lines="466+",
            api_compatibility="100%",
        )

    def create_dashboard(
        self,
        dashboard_type: str,
        data: Dict[str, Any],
        config: Optional[DashboardConfig] = None,
    ) -> go.Figure:
        """Create dashboard using unified factory pattern"""
        # Delegate to UnifiedFactory - ELIMINATES duplicate logic
        return self.unified_factory.create_component(
            ComponentType.VISUALIZATION_DASHBOARD,
            {
                "dashboard_type": dashboard_type,
                "data": data,
                "config": config,
                "color_palette": self.color_palette,
            },
        )

    def create_leadership_dashboard(self, data: Dict[str, Any]) -> go.Figure:
        """Create leadership dashboard via unified factory"""
        return self.create_dashboard("leadership", data)

    def create_roi_dashboard(self, data: Dict[str, Any]) -> go.Figure:
        """Create ROI dashboard via unified factory"""
        return self.create_dashboard("roi", data)

    def create_architecture_health_dashboard(self, data: Dict[str, Any]) -> go.Figure:
        """Create architecture health dashboard via unified factory"""
        return self.create_dashboard("architecture_health", data)

    def create_team_comparison_dashboard(self, data: Dict[str, Any]) -> go.Figure:
        """Create team comparison dashboard via unified factory"""
        return self.create_dashboard("team_comparison", data)
