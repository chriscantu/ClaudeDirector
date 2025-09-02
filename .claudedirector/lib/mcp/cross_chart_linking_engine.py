"""
Phase 7C: Cross-Chart Linking Engine
T-C1 Implementation - Advanced Features

Enables synchronized interactions across multiple interactive charts within the chat interface.
Supports filter sync, zoom sync, time sync, and highlight sync across 2-5 linked charts.

Architecture Compliance:
- OVERVIEW.md: Extends Phase 7A & 7B foundation with advanced interactive features
- PROJECT_STRUCTURE.md: Located in .claudedirector/lib/mcp/ following established patterns
- Configuration-driven: Uses MCPServerConstants.Phase7C for all settings
- DRY & SOLID: Extends existing InteractiveEnhancementAddon pattern
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional, Set, Tuple
from enum import Enum
from dataclasses import dataclass

from .constants import MCPServerConstants, InteractionIntent, QueryIntent
from .interactive_enhancement_addon import InteractiveEnhancementAddon, InteractiveEnhancementResult
from .chat_context_manager import ChatContextManager

logger = logging.getLogger(__name__)


class LinkType(Enum):
    """Types of cross-chart linking synchronization"""
    FILTER_SYNC = "filter_sync"
    ZOOM_SYNC = "zoom_sync"
    TIME_SYNC = "time_sync"
    HIGHLIGHT_SYNC = "highlight_sync"


class LinkageStatus(Enum):
    """Status of chart linkage"""
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    REMOVED = "removed"


@dataclass
class LinkageConfig:
    """Configuration for cross-chart linkage"""
    linkage_id: str
    charts: List[str]
    link_type: LinkType
    status: LinkageStatus
    created_at: float
    updated_at: float
    metadata: Dict[str, Any]


@dataclass
class ChartUpdate:
    """Update to be applied to a linked chart"""
    chart_id: str
    update_type: str
    update_data: Dict[str, Any]
    source_chart: str
    timestamp: float


class CrossChartLinkingEngine:
    """
    Advanced cross-chart linking engine for Phase 7C.

    Implements T-C1: Cross-Chart Linking Implementation
    - Synchronized interactions across multiple charts
    - Support for filter, zoom, time, and highlight synchronization
    - <200ms cross-chart update performance target
    - Error isolation prevents cascade failures
    """

    def __init__(self):
        self.name = "cross-chart-linking-engine"
        self.version = "1.0.0"

        # Core dependencies - extend Phase 7A & 7B foundation
        self.interactive_addon = InteractiveEnhancementAddon()
        self.context_manager = ChatContextManager()

        # Performance targets from configuration (OVERVIEW.md compliance)
        self.update_target_ms = MCPServerConstants.Phase7C.CROSS_CHART_UPDATE_TARGET
        self.max_linked_charts = MCPServerConstants.Phase7C.MAX_LINKED_CHARTS

        # Internal state management
        self._linkages: Dict[str, LinkageConfig] = {}
        self._chart_linkage_map: Dict[str, Set[str]] = {}  # chart_id -> set of linkage_ids
        self._active_updates: Dict[str, float] = {}  # prevent update loops

        logger.info(f"Cross-Chart Linking Engine {self.version} initialized")
        logger.info(f"✅ ARCHITECTURE: Extends Phase 7A & 7B interactive foundation")
        logger.info(f"⚡ PERFORMANCE: {self.update_target_ms}ms cross-chart update target")

    def create_chart_linkage(
        self,
        charts: List[str],
        link_type: LinkType,
        metadata: Optional[Dict[str, Any]] = None
    ) -> LinkageConfig:
        """
        Create linkage between multiple charts.

        REQUIREMENTS:
        - Support for 2-5 linked charts simultaneously
        - Memory efficient linkage tracking
        - Graceful handling of chart type mismatches

        Args:
            charts: List of chart IDs to link (2-5 charts)
            link_type: Type of synchronization (filter, zoom, time, highlight)
            metadata: Optional metadata for the linkage

        Returns:
            LinkageConfig: Configuration object for the created linkage
        """
        # Validate input parameters
        if len(charts) < 2:
            raise ValueError("Minimum 2 charts required for linking")
        if len(charts) > self.max_linked_charts:
            raise ValueError(f"Maximum {self.max_linked_charts} charts allowed per linkage")

        # Generate unique linkage ID
        linkage_id = f"linkage_{link_type.value}_{int(time.time()*1000)}"
        current_time = time.time()

        # Create linkage configuration
        linkage_config = LinkageConfig(
            linkage_id=linkage_id,
            charts=list(charts),
            link_type=link_type,
            status=LinkageStatus.ACTIVE,
            created_at=current_time,
            updated_at=current_time,
            metadata=metadata or {}
        )

        # Store linkage and update chart mapping
        self._linkages[linkage_id] = linkage_config
        for chart_id in charts:
            if chart_id not in self._chart_linkage_map:
                self._chart_linkage_map[chart_id] = set()
            self._chart_linkage_map[chart_id].add(linkage_id)

        logger.info(f"✅ Created {link_type.value} linkage: {linkage_id} for {len(charts)} charts")
        return linkage_config

    async def propagate_interaction(
        self,
        source_chart: str,
        event: Dict[str, Any]
    ) -> List[ChartUpdate]:
        """
        Propagate interaction from source chart to linked charts.

        REQUIREMENTS:
        - <200ms cross-chart update time
        - Asynchronous updates to prevent UI blocking
        - Intelligent event filtering to prevent update loops
        - Error isolation (failure in one chart doesn't break others)

        Args:
            source_chart: ID of the chart that triggered the event
            event: Event data with interaction details

        Returns:
            List[ChartUpdate]: Updates to apply to linked charts
        """
        start_time = time.time()
        updates = []

        # Check if source chart has any linkages
        if source_chart not in self._chart_linkage_map:
            logger.debug(f"No linkages found for chart: {source_chart}")
            return updates

        # Prevent update loops - check if this update is already in progress
        update_key = f"{source_chart}_{event.get('type', 'unknown')}_{event.get('timestamp', time.time())}"
        if update_key in self._active_updates:
            current_time = time.time()
            if current_time - self._active_updates[update_key] < 1.0:  # 1 second debounce
                logger.debug(f"Skipping duplicate update: {update_key}")
                return updates

        self._active_updates[update_key] = time.time()

        try:
            # Get all linkages for this chart
            linkage_ids = self._chart_linkage_map[source_chart].copy()

            for linkage_id in linkage_ids:
                linkage = self._linkages.get(linkage_id)
                if not linkage or linkage.status != LinkageStatus.ACTIVE:
                    continue

                # Process linkage based on type and event
                try:
                    linkage_updates = await self._process_linkage_event(
                        linkage, source_chart, event
                    )
                    updates.extend(linkage_updates)
                except Exception as e:
                    logger.error(f"Error processing linkage {linkage_id}: {e}")
                    # Error isolation - continue processing other linkages
                    continue

            # Performance monitoring
            elapsed_ms = (time.time() - start_time) * 1000
            if elapsed_ms > self.update_target_ms:
                logger.warning(f"Cross-chart update exceeded target: {elapsed_ms:.1f}ms > {self.update_target_ms}ms")
            else:
                logger.debug(f"Cross-chart update completed in {elapsed_ms:.1f}ms")

            return updates

        finally:
            # Cleanup update tracking after processing
            if update_key in self._active_updates:
                del self._active_updates[update_key]

    async def _process_linkage_event(
        self,
        linkage: LinkageConfig,
        source_chart: str,
        event: Dict[str, Any]
    ) -> List[ChartUpdate]:
        """Process a specific linkage event and generate updates for target charts."""
        updates = []
        target_charts = [chart for chart in linkage.charts if chart != source_chart]

        if not target_charts:
            return updates

        # Generate updates based on link type and event
        if linkage.link_type == LinkType.FILTER_SYNC:
            updates = await self._generate_filter_sync_updates(target_charts, source_chart, event)
        elif linkage.link_type == LinkType.ZOOM_SYNC:
            updates = await self._generate_zoom_sync_updates(target_charts, source_chart, event)
        elif linkage.link_type == LinkType.TIME_SYNC:
            updates = await self._generate_time_sync_updates(target_charts, source_chart, event)
        elif linkage.link_type == LinkType.HIGHLIGHT_SYNC:
            updates = await self._generate_highlight_sync_updates(target_charts, source_chart, event)

        return updates

    async def _generate_filter_sync_updates(
        self, target_charts: List[str], source_chart: str, event: Dict[str, Any]
    ) -> List[ChartUpdate]:
        """Generate filter synchronization updates."""
        updates = []
        filter_data = event.get('filter_data', {})

        for chart_id in target_charts:
            update = ChartUpdate(
                chart_id=chart_id,
                update_type="apply_filter",
                update_data=filter_data,
                source_chart=source_chart,
                timestamp=time.time()
            )
            updates.append(update)

        return updates

    async def _generate_zoom_sync_updates(
        self, target_charts: List[str], source_chart: str, event: Dict[str, Any]
    ) -> List[ChartUpdate]:
        """Generate zoom synchronization updates."""
        updates = []
        zoom_data = event.get('zoom_data', {})

        for chart_id in target_charts:
            update = ChartUpdate(
                chart_id=chart_id,
                update_type="apply_zoom",
                update_data=zoom_data,
                source_chart=source_chart,
                timestamp=time.time()
            )
            updates.append(update)

        return updates

    async def _generate_time_sync_updates(
        self, target_charts: List[str], source_chart: str, event: Dict[str, Any]
    ) -> List[ChartUpdate]:
        """Generate time range synchronization updates."""
        updates = []
        time_data = event.get('time_data', {})

        for chart_id in target_charts:
            update = ChartUpdate(
                chart_id=chart_id,
                update_type="apply_time_range",
                update_data=time_data,
                source_chart=source_chart,
                timestamp=time.time()
            )
            updates.append(update)

        return updates

    async def _generate_highlight_sync_updates(
        self, target_charts: List[str], source_chart: str, event: Dict[str, Any]
    ) -> List[ChartUpdate]:
        """Generate highlight synchronization updates."""
        updates = []
        highlight_data = event.get('highlight_data', {})

        for chart_id in target_charts:
            update = ChartUpdate(
                chart_id=chart_id,
                update_type="apply_highlight",
                update_data=highlight_data,
                source_chart=source_chart,
                timestamp=time.time()
            )
            updates.append(update)

        return updates

    def remove_chart_linkage(self, linkage_id: str) -> bool:
        """Remove a chart linkage by ID."""
        if linkage_id not in self._linkages:
            return False

        linkage = self._linkages[linkage_id]

        # Remove from chart mapping
        for chart_id in linkage.charts:
            if chart_id in self._chart_linkage_map:
                self._chart_linkage_map[chart_id].discard(linkage_id)
                if not self._chart_linkage_map[chart_id]:
                    del self._chart_linkage_map[chart_id]

        # Remove linkage
        del self._linkages[linkage_id]

        logger.info(f"✅ Removed linkage: {linkage_id}")
        return True

    def get_chart_linkages(self, chart_id: str) -> List[LinkageConfig]:
        """Get all linkages for a specific chart."""
        if chart_id not in self._chart_linkage_map:
            return []

        linkages = []
        for linkage_id in self._chart_linkage_map[chart_id]:
            if linkage_id in self._linkages:
                linkages.append(self._linkages[linkage_id])

        return linkages

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the cross-chart linking engine."""
        return {
            "name": self.name,
            "version": self.version,
            "total_linkages": len(self._linkages),
            "active_linkages": len([l for l in self._linkages.values() if l.status == LinkageStatus.ACTIVE]),
            "linked_charts": len(self._chart_linkage_map),
            "performance_target_ms": self.update_target_ms,
            "max_linked_charts": self.max_linked_charts
        }

    # Resource management and cleanup (DRY compliance with Phase 7A & 7B pattern)
    def cleanup(self):
        """Clean up resources and active linkages."""
        logger.info("Cross-Chart Linking Engine cleanup initiated")
        self._linkages.clear()
        self._chart_linkage_map.clear()
        self._active_updates.clear()
        if hasattr(self.interactive_addon, 'cleanup'):
            self.interactive_addon.cleanup()
        if hasattr(self.context_manager, 'cleanup'):
            self.context_manager.cleanup()

    async def async_cleanup(self):
        """Async cleanup for proper resource management."""
        logger.info("Cross-Chart Linking Engine async cleanup initiated")
        if hasattr(self.interactive_addon, 'async_cleanup'):
            await self.interactive_addon.async_cleanup()
        if hasattr(self.context_manager, 'async_cleanup'):
            await self.context_manager.async_cleanup()
        self.cleanup()

    # Context manager support (DRY compliance)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.async_cleanup()


# Factory function for consistent instantiation pattern (DRY compliance)
def create_cross_chart_linking_engine() -> CrossChartLinkingEngine:
    """
    Factory function to create CrossChartLinkingEngine instance.

    Returns:
        CrossChartLinkingEngine: Configured engine instance
    """
    return CrossChartLinkingEngine()
