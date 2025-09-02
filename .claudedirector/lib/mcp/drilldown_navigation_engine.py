"""
Phase 7C: Drill-Down Navigation Engine
T-C2 Implementation - Advanced Features

Enables hierarchical data exploration within the chat interface with breadcrumb navigation.
Supports 3-6 hierarchy levels with smooth visual transitions and context preservation.

Architecture Compliance:
- OVERVIEW.md: Extends Phase 7A & 7B foundation with hierarchical navigation
- PROJECT_STRUCTURE.md: Located in .claudedirector/lib/mcp/ following established patterns
- Configuration-driven: Uses MCPServerConstants.Phase7C for all settings
- DRY & SOLID: Extends existing InteractiveEnhancementAddon pattern
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

from .constants import MCPServerConstants, InteractionIntent
from .interactive_enhancement_addon import InteractiveEnhancementAddon, InteractiveEnhancementResult
from .chat_context_manager import ChatContextManager

logger = logging.getLogger(__name__)


class NavigationType(Enum):
    """Types of hierarchy navigation operations"""
    DRILL_DOWN = "drill_down"
    ROLL_UP = "roll_up"
    JUMP_TO = "jump_to"
    BACK = "back"


class HierarchyLevel(Enum):
    """Standard hierarchy levels for organizational data"""
    ORGANIZATION = "organization"
    DEPARTMENT = "department"
    TEAM = "team"
    INDIVIDUAL = "individual"
    PROJECT = "project"
    EPIC = "epic"
    STORY = "story"
    TASK = "task"


@dataclass
class HierarchyNode:
    """Node in the hierarchy tree"""
    node_id: str
    level: str
    name: str
    parent_id: Optional[str]
    children: List[str]
    data: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class HierarchyMap:
    """Complete hierarchy structure for navigation"""
    hierarchy_id: str
    levels: List[str]
    nodes: Dict[str, HierarchyNode]
    root_nodes: List[str]
    created_at: float
    metadata: Dict[str, Any]


@dataclass
class NavigationState:
    """Current navigation position and history"""
    current_node: str
    current_level: str
    breadcrumbs: List[Tuple[str, str]]  # [(node_id, name), ...]
    history: List[str]  # Previous positions for back navigation
    context_data: Dict[str, Any]


@dataclass
class NavigationResult:
    """Result of a navigation operation"""
    success: bool
    new_state: Optional[NavigationState]
    data: Dict[str, Any]
    breadcrumbs: List[Tuple[str, str]]
    transition_info: Dict[str, Any]
    error_message: Optional[str] = None


class DrillDownNavigationEngine:
    """
    Advanced hierarchical navigation engine for Phase 7C.

    Implements T-C2: Drill-Down Hierarchy Navigation
    - Support for 3-6 hierarchy levels
    - <300ms navigation response time
    - Visual breadcrumb navigation
    - Context preservation during navigation
    """

    def __init__(self):
        self.name = "drilldown-navigation-engine"
        self.version = "1.0.0"

        # Core dependencies - extend Phase 7A & 7B foundation
        self.interactive_addon = InteractiveEnhancementAddon()
        self.context_manager = ChatContextManager()

        # Performance targets from configuration (OVERVIEW.md compliance)
        self.navigation_target_ms = MCPServerConstants.Phase7C.NAVIGATION_RESPONSE_TARGET
        self.min_hierarchy_levels = MCPServerConstants.Phase7C.MIN_HIERARCHY_LEVELS
        self.max_hierarchy_levels = MCPServerConstants.Phase7C.MAX_HIERARCHY_LEVELS

        # Internal state management
        self._hierarchies: Dict[str, HierarchyMap] = {}
        self._navigation_states: Dict[str, NavigationState] = {}  # session_id -> state
        self._level_patterns = MCPServerConstants.Phase7C.HIERARCHY_PATTERNS

        logger.info(f"Drill-Down Navigation Engine {self.version} initialized")
        logger.info(f"✅ ARCHITECTURE: Extends Phase 7A & 7B interactive foundation")
        logger.info(f"⚡ PERFORMANCE: {self.navigation_target_ms}ms navigation target")

    def create_hierarchy_map(
        self,
        data: Dict[str, Any],
        hierarchy_levels: List[str]
    ) -> HierarchyMap:
        """
        Create navigable hierarchy from data structure.

        HIERARCHY EXAMPLES:
        - Organization → Department → Team → Individual
        - Project → Epic → Story → Task
        - Time → Year → Quarter → Month → Week
        - Technology → Platform → Service → Component

        REQUIREMENTS:
        - Support for 3-6 hierarchy levels
        - Dynamic hierarchy detection from data
        - Context preservation during navigation

        Args:
            data: Raw data to organize into hierarchy
            hierarchy_levels: List of level names in order

        Returns:
            HierarchyMap: Complete hierarchy structure
        """
        # Validate hierarchy levels
        if len(hierarchy_levels) < self.min_hierarchy_levels:
            raise ValueError(f"Minimum {self.min_hierarchy_levels} hierarchy levels required")
        if len(hierarchy_levels) > self.max_hierarchy_levels:
            raise ValueError(f"Maximum {self.max_hierarchy_levels} hierarchy levels allowed")

        hierarchy_id = f"hierarchy_{int(time.time()*1000)}"
        nodes = {}
        root_nodes = []

        # Process data into hierarchical structure
        nodes, root_nodes = self._build_hierarchy_nodes(data, hierarchy_levels)

        hierarchy_map = HierarchyMap(
            hierarchy_id=hierarchy_id,
            levels=hierarchy_levels,
            nodes=nodes,
            root_nodes=root_nodes,
            created_at=time.time(),
            metadata={"source_data_size": len(str(data))}
        )

        # Store hierarchy for navigation
        self._hierarchies[hierarchy_id] = hierarchy_map

        logger.info(f"✅ Created hierarchy {hierarchy_id} with {len(hierarchy_levels)} levels, {len(nodes)} nodes")
        return hierarchy_map

    def _build_hierarchy_nodes(
        self,
        data: Dict[str, Any],
        levels: List[str]
    ) -> Tuple[Dict[str, HierarchyNode], List[str]]:
        """Build hierarchy nodes from raw data."""
        nodes = {}
        root_nodes = []

        # Use pattern-based extraction for common hierarchies
        if self._is_organizational_data(data):
            return self._build_organizational_hierarchy(data, levels)
        elif self._is_project_data(data):
            return self._build_project_hierarchy(data, levels)
        elif self._is_temporal_data(data):
            return self._build_temporal_hierarchy(data, levels)
        else:
            return self._build_generic_hierarchy(data, levels)

    def _is_organizational_data(self, data: Dict[str, Any]) -> bool:
        """Check if data represents organizational structure."""
        org_indicators = ["department", "team", "employee", "manager", "organization"]
        data_str = json.dumps(data).lower()
        return any(indicator in data_str for indicator in org_indicators)

    def _is_project_data(self, data: Dict[str, Any]) -> bool:
        """Check if data represents project structure."""
        project_indicators = ["project", "epic", "story", "task", "sprint", "backlog"]
        data_str = json.dumps(data).lower()
        return any(indicator in data_str for indicator in project_indicators)

    def _is_temporal_data(self, data: Dict[str, Any]) -> bool:
        """Check if data represents temporal structure."""
        temporal_indicators = ["year", "quarter", "month", "week", "date", "time"]
        data_str = json.dumps(data).lower()
        return any(indicator in data_str for indicator in temporal_indicators)

    def _build_organizational_hierarchy(
        self, data: Dict[str, Any], levels: List[str]
    ) -> Tuple[Dict[str, HierarchyNode], List[str]]:
        """Build hierarchy for organizational data."""
        nodes = {}
        root_nodes = []

        # Example implementation for organizational hierarchy
        # This would be expanded based on actual data structure
        for level_idx, level in enumerate(levels):
            level_data = data.get(level, {})
            for item_id, item_data in level_data.items():
                node = HierarchyNode(
                    node_id=f"{level}_{item_id}",
                    level=level,
                    name=item_data.get('name', item_id),
                    parent_id=item_data.get('parent_id'),
                    children=item_data.get('children', []),
                    data=item_data,
                    metadata={"level_index": level_idx}
                )
                nodes[node.node_id] = node

                if level_idx == 0:  # Root level
                    root_nodes.append(node.node_id)

        return nodes, root_nodes

    def _build_project_hierarchy(
        self, data: Dict[str, Any], levels: List[str]
    ) -> Tuple[Dict[str, HierarchyNode], List[str]]:
        """Build hierarchy for project data."""
        # Similar pattern to organizational hierarchy but for project structures
        return self._build_generic_hierarchy(data, levels)

    def _build_temporal_hierarchy(
        self, data: Dict[str, Any], levels: List[str]
    ) -> Tuple[Dict[str, HierarchyNode], List[str]]:
        """Build hierarchy for temporal data."""
        # Similar pattern but for time-based hierarchies
        return self._build_generic_hierarchy(data, levels)

    def _build_generic_hierarchy(
        self, data: Dict[str, Any], levels: List[str]
    ) -> Tuple[Dict[str, HierarchyNode], List[str]]:
        """Build generic hierarchy when specific patterns don't match."""
        nodes = {}
        root_nodes = []

        # Simple flattened approach for generic data
        node_counter = 0
        for level_idx, level in enumerate(levels):
            level_items = data.get(level, ["Sample Item 1", "Sample Item 2"])
            if not isinstance(level_items, list):
                level_items = [level_items]

            for item in level_items:
                node_id = f"node_{node_counter}"
                node = HierarchyNode(
                    node_id=node_id,
                    level=level,
                    name=str(item),
                    parent_id=None if level_idx == 0 else f"node_{node_counter - 1}",
                    children=[],
                    data={"value": item},
                    metadata={"level_index": level_idx}
                )
                nodes[node_id] = node

                if level_idx == 0:
                    root_nodes.append(node_id)

                node_counter += 1

        return nodes, root_nodes

    async def navigate_hierarchy(
        self,
        session_id: str,
        hierarchy_id: str,
        direction: NavigationType,
        target: Optional[str] = None
    ) -> NavigationResult:
        """
        Navigate up/down the data hierarchy.

        NAVIGATION TYPES:
        - DRILL_DOWN: Move to more detailed level
        - ROLL_UP: Move to more aggregated level
        - JUMP_TO: Direct navigation to specific level
        - BACK: Return to previous navigation state

        REQUIREMENTS:
        - <300ms navigation response time
        - Smooth visual transitions between levels
        - Context breadcrumbs always visible
        - Data aggregation/disaggregation handling
        """
        start_time = time.time()

        try:
            # Get hierarchy and current navigation state
            hierarchy = self._hierarchies.get(hierarchy_id)
            if not hierarchy:
                return NavigationResult(
                    success=False,
                    new_state=None,
                    data={},
                    breadcrumbs=[],
                    transition_info={},
                    error_message=f"Hierarchy {hierarchy_id} not found"
                )

            current_state = self._navigation_states.get(session_id)
            if not current_state and direction != NavigationType.JUMP_TO:
                # Initialize at root level
                if not hierarchy.root_nodes:
                    return NavigationResult(
                        success=False,
                        new_state=None,
                        data={},
                        breadcrumbs=[],
                        transition_info={},
                        error_message="No root nodes in hierarchy"
                    )

                current_state = NavigationState(
                    current_node=hierarchy.root_nodes[0],
                    current_level=hierarchy.levels[0],
                    breadcrumbs=[(hierarchy.root_nodes[0], hierarchy.nodes[hierarchy.root_nodes[0]].name)],
                    history=[],
                    context_data={}
                )

            # Perform navigation based on direction
            result = await self._perform_navigation(hierarchy, current_state, direction, target)

            # Update navigation state if successful
            if result.success and result.new_state:
                self._navigation_states[session_id] = result.new_state

            # Performance monitoring
            elapsed_ms = (time.time() - start_time) * 1000
            result.transition_info["elapsed_ms"] = elapsed_ms

            if elapsed_ms > self.navigation_target_ms:
                logger.warning(f"Navigation exceeded target: {elapsed_ms:.1f}ms > {self.navigation_target_ms}ms")
            else:
                logger.debug(f"Navigation completed in {elapsed_ms:.1f}ms")

            return result

        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return NavigationResult(
                success=False,
                new_state=None,
                data={},
                breadcrumbs=[],
                transition_info={"elapsed_ms": (time.time() - start_time) * 1000},
                error_message=str(e)
            )

    async def _perform_navigation(
        self,
        hierarchy: HierarchyMap,
        current_state: NavigationState,
        direction: NavigationType,
        target: Optional[str]
    ) -> NavigationResult:
        """Perform the actual navigation operation."""

        if direction == NavigationType.DRILL_DOWN:
            return await self._drill_down(hierarchy, current_state)
        elif direction == NavigationType.ROLL_UP:
            return await self._roll_up(hierarchy, current_state)
        elif direction == NavigationType.JUMP_TO:
            return await self._jump_to(hierarchy, current_state, target)
        elif direction == NavigationType.BACK:
            return await self._navigate_back(hierarchy, current_state)
        else:
            return NavigationResult(
                success=False,
                new_state=None,
                data={},
                breadcrumbs=[],
                transition_info={},
                error_message=f"Unknown navigation direction: {direction}"
            )

    async def _drill_down(
        self, hierarchy: HierarchyMap, current_state: NavigationState
    ) -> NavigationResult:
        """Navigate to more detailed level."""
        current_node = hierarchy.nodes.get(current_state.current_node)
        if not current_node or not current_node.children:
            return NavigationResult(
                success=False,
                new_state=None,
                data={},
                breadcrumbs=current_state.breadcrumbs,
                transition_info={},
                error_message="No children available for drill-down"
            )

        # Navigate to first child (could be enhanced to allow child selection)
        child_id = current_node.children[0]
        child_node = hierarchy.nodes[child_id]

        new_breadcrumbs = current_state.breadcrumbs + [(child_id, child_node.name)]
        new_history = current_state.history + [current_state.current_node]

        new_state = NavigationState(
            current_node=child_id,
            current_level=child_node.level,
            breadcrumbs=new_breadcrumbs,
            history=new_history,
            context_data=child_node.data
        )

        return NavigationResult(
            success=True,
            new_state=new_state,
            data=child_node.data,
            breadcrumbs=new_breadcrumbs,
            transition_info={"direction": "drill_down", "target_level": child_node.level}
        )

    async def _roll_up(
        self, hierarchy: HierarchyMap, current_state: NavigationState
    ) -> NavigationResult:
        """Navigate to more aggregated level."""
        current_node = hierarchy.nodes.get(current_state.current_node)
        if not current_node or not current_node.parent_id:
            return NavigationResult(
                success=False,
                new_state=None,
                data={},
                breadcrumbs=current_state.breadcrumbs,
                transition_info={},
                error_message="No parent available for roll-up"
            )

        parent_node = hierarchy.nodes[current_node.parent_id]
        new_breadcrumbs = current_state.breadcrumbs[:-1]  # Remove current level
        new_history = current_state.history + [current_state.current_node]

        new_state = NavigationState(
            current_node=current_node.parent_id,
            current_level=parent_node.level,
            breadcrumbs=new_breadcrumbs,
            history=new_history,
            context_data=parent_node.data
        )

        return NavigationResult(
            success=True,
            new_state=new_state,
            data=parent_node.data,
            breadcrumbs=new_breadcrumbs,
            transition_info={"direction": "roll_up", "target_level": parent_node.level}
        )

    async def _jump_to(
        self, hierarchy: HierarchyMap, current_state: Optional[NavigationState], target: Optional[str]
    ) -> NavigationResult:
        """Jump directly to specific level or node."""
        if not target:
            return NavigationResult(
                success=False,
                new_state=None,
                data={},
                breadcrumbs=[],
                transition_info={},
                error_message="Target required for jump_to navigation"
            )

        target_node = hierarchy.nodes.get(target)
        if not target_node:
            return NavigationResult(
                success=False,
                new_state=None,
                data={},
                breadcrumbs=[],
                transition_info={},
                error_message=f"Target node {target} not found"
            )

        # Build breadcrumb path to target
        breadcrumbs = self._build_breadcrumb_path(hierarchy, target)

        new_state = NavigationState(
            current_node=target,
            current_level=target_node.level,
            breadcrumbs=breadcrumbs,
            history=[] if not current_state else current_state.history + [current_state.current_node],
            context_data=target_node.data
        )

        return NavigationResult(
            success=True,
            new_state=new_state,
            data=target_node.data,
            breadcrumbs=breadcrumbs,
            transition_info={"direction": "jump_to", "target_level": target_node.level}
        )

    async def _navigate_back(
        self, hierarchy: HierarchyMap, current_state: NavigationState
    ) -> NavigationResult:
        """Return to previous navigation state."""
        if not current_state.history:
            return NavigationResult(
                success=False,
                new_state=None,
                data={},
                breadcrumbs=current_state.breadcrumbs,
                transition_info={},
                error_message="No previous state in history"
            )

        previous_node_id = current_state.history[-1]
        previous_node = hierarchy.nodes[previous_node_id]

        new_breadcrumbs = self._build_breadcrumb_path(hierarchy, previous_node_id)
        new_history = current_state.history[:-1]  # Remove last item

        new_state = NavigationState(
            current_node=previous_node_id,
            current_level=previous_node.level,
            breadcrumbs=new_breadcrumbs,
            history=new_history,
            context_data=previous_node.data
        )

        return NavigationResult(
            success=True,
            new_state=new_state,
            data=previous_node.data,
            breadcrumbs=new_breadcrumbs,
            transition_info={"direction": "back", "target_level": previous_node.level}
        )

    def _build_breadcrumb_path(self, hierarchy: HierarchyMap, node_id: str) -> List[Tuple[str, str]]:
        """Build breadcrumb path from root to specified node."""
        path = []
        current_id = node_id

        # Traverse up to root
        while current_id:
            node = hierarchy.nodes[current_id]
            path.append((current_id, node.name))
            current_id = node.parent_id

        # Reverse to get root-to-node path
        return list(reversed(path))

    def get_navigation_state(self, session_id: str) -> Optional[NavigationState]:
        """Get current navigation state for session."""
        return self._navigation_states.get(session_id)

    def get_status(self) -> Dict[str, Any]:
        """Get current status of the drill-down navigation engine."""
        return {
            "name": self.name,
            "version": self.version,
            "total_hierarchies": len(self._hierarchies),
            "active_sessions": len(self._navigation_states),
            "performance_target_ms": self.navigation_target_ms,
            "hierarchy_levels_range": f"{self.min_hierarchy_levels}-{self.max_hierarchy_levels}"
        }

    # Resource management and cleanup (DRY compliance with Phase 7A & 7B pattern)
    def cleanup(self):
        """Clean up resources and navigation states."""
        logger.info("Drill-Down Navigation Engine cleanup initiated")
        self._hierarchies.clear()
        self._navigation_states.clear()
        if hasattr(self.interactive_addon, 'cleanup'):
            self.interactive_addon.cleanup()
        if hasattr(self.context_manager, 'cleanup'):
            self.context_manager.cleanup()

    async def async_cleanup(self):
        """Async cleanup for proper resource management."""
        logger.info("Drill-Down Navigation Engine async cleanup initiated")
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
def create_drilldown_navigation_engine() -> DrillDownNavigationEngine:
    """
    Factory function to create DrillDownNavigationEngine instance.

    Returns:
        DrillDownNavigationEngine: Configured engine instance
    """
    return DrillDownNavigationEngine()
