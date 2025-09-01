#!/usr/bin/env python3
"""
Interactive Chart Engine
Phase 7 Week 4 - Core Interactive Engine Implementation

🏗️ Martin | Platform Architecture - Interactive chart capabilities
🎨 Rachel | Design Systems Strategy - Executive interactive design
💼 Alvaro | Platform Investment Strategy - ROI-driven interactivity

Adds interactive capabilities to existing Plotly charts with chat integration.
Built on Phase 2 Executive Visualization System foundation.
"""

import asyncio
import json
import time
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from jinja2 import Template

from .constants import MCPServerConstants
from .executive_visualization_server import (
    VisualizationResult,
    ExecutiveVisualizationEngine,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InteractionType(Enum):
    """Types of chart interactions supported"""

    CLICK_TO_DRILL_DOWN = "drill_down"
    MULTI_SELECT_FILTER = "filter"
    ZOOM_AND_PAN = "navigation"
    HOVER_DETAILS = "details"
    TIME_SERIES_BRUSH = "time_brush"


@dataclass
class InteractionResult:
    """Result of chart interaction processing"""

    success: bool
    updated_chart: Optional[go.Figure]
    interaction_data: Dict[str, Any]
    processing_time: float
    context_preserved: bool
    error: Optional[str] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class InteractionEvent:
    """Chart interaction event data"""

    event_type: str
    chart_id: str
    element_id: str
    data_point: Dict[str, Any]
    coordinates: Dict[str, float]
    timestamp: float

    def __post_init__(self):
        if not hasattr(self, "timestamp"):
            self.timestamp = time.time()


class InteractiveChartEngine:
    """
    Interactive Chart Engine - T-A1 Implementation

    Adds interactive capabilities to existing Plotly charts:
    - <200ms processing time for interaction addition
    - Local JavaScript generation (no external CDNs)
    - Progressive enhancement support
    - Graceful degradation to static charts
    """

    def __init__(self):
        self.name = "interactive-chart-engine"
        self.version = "1.0.0"

        # Integration with existing visualization engine
        self.visualization_engine = ExecutiveVisualizationEngine()

        # Interactive session management
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.interaction_history: Dict[str, List[InteractionEvent]] = {}

        # Performance metrics
        self.interaction_metrics = {
            "total_interactions": 0,
            "successful_interactions": 0,
            "avg_processing_time": 0.0,
            "active_sessions": 0,
            "memory_usage_mb": 0.0,
        }

        # Rachel's interactive design system
        self.interactive_theme = {
            "hover_color": "#4dabf7",
            "selection_color": "#51cf66",
            "transition_duration": 300,
            "animation_easing": "cubic-bezier(0.25, 0.1, 0.25, 1)",
        }

        logger.info(f"Interactive Chart Engine {self.version} initialized")

    async def add_interactivity(
        self, fig: go.Figure, interaction_type: str, context: Dict[str, Any] = None
    ) -> go.Figure:
        """
        Add interactive capabilities to existing Plotly charts

        REQUIREMENTS:
        - <200ms processing time for interaction addition
        - Local JavaScript generation (no external CDNs)
        - Progressive enhancement support
        - Graceful degradation to static charts
        """

        start_time = time.time()
        context = context or {}

        try:
            # Create unique chart session
            chart_id = str(uuid.uuid4())
            session_data = {
                "chart_id": chart_id,
                "interaction_type": interaction_type,
                "context": context,
                "created_at": time.time(),
                "interactions": [],
            }

            # Add interaction capabilities based on type
            if interaction_type == InteractionType.CLICK_TO_DRILL_DOWN.value:
                fig = self._add_drill_down_capability(fig, chart_id, context)
            elif interaction_type == InteractionType.MULTI_SELECT_FILTER.value:
                fig = self._add_filtering_capability(fig, chart_id, context)
            elif interaction_type == InteractionType.ZOOM_AND_PAN.value:
                fig = self._add_navigation_capability(fig, chart_id, context)
            elif interaction_type == InteractionType.HOVER_DETAILS.value:
                fig = self._add_hover_details(fig, chart_id, context)
            elif interaction_type == InteractionType.TIME_SERIES_BRUSH.value:
                fig = self._add_time_brush_capability(fig, chart_id, context)

            # Apply Rachel's interactive styling
            fig = self._apply_interactive_styling(fig)

            # Store session
            self.active_sessions[chart_id] = session_data

            # Update metrics
            processing_time = time.time() - start_time
            self._update_interaction_metrics(processing_time, success=True)

            # Ensure performance requirement (<200ms)
            if processing_time > 0.2:
                logger.warning(
                    f"Interaction addition took {processing_time:.3f}s (>200ms limit)"
                )

            logger.info(
                f"Added {interaction_type} interactivity to chart {chart_id} in {processing_time:.3f}s"
            )

            return fig

        except Exception as e:
            processing_time = time.time() - start_time
            self._update_interaction_metrics(processing_time, success=False)
            logger.error(f"Failed to add interactivity: {e}")

            # Graceful degradation - return original chart
            return fig

    async def handle_chart_interaction(
        self, event: Dict[str, Any]
    ) -> InteractionResult:
        """
        Process user interactions with charts

        REQUIREMENTS:
        - <200ms response time for all interaction events
        - Local data processing only (no external APIs)
        - Context preservation across interactions
        - Error handling with graceful fallbacks
        """

        start_time = time.time()

        try:
            # Parse interaction event
            chart_id = event.get("chart_id")
            event_type = event.get("event_type")
            element_data = event.get("element_data", {})

            if not chart_id or chart_id not in self.active_sessions:
                raise ValueError(f"Invalid or expired chart session: {chart_id}")

            session = self.active_sessions[chart_id]

            # Create interaction event record
            interaction_event = InteractionEvent(
                event_type=event_type,
                chart_id=chart_id,
                element_id=element_data.get("id", ""),
                data_point=element_data.get("data", {}),
                coordinates=element_data.get("coordinates", {}),
                timestamp=time.time(),
            )

            # Process interaction based on type
            updated_chart = None
            if event_type == "drill_down":
                updated_chart = await self._process_drill_down(
                    session, interaction_event
                )
            elif event_type == "filter":
                updated_chart = await self._process_filter(session, interaction_event)
            elif event_type == "navigation":
                updated_chart = await self._process_navigation(
                    session, interaction_event
                )

            # Store interaction history
            if chart_id not in self.interaction_history:
                self.interaction_history[chart_id] = []
            self.interaction_history[chart_id].append(interaction_event)

            # Update session
            session["interactions"].append(
                {
                    "event_type": event_type,
                    "timestamp": interaction_event.timestamp,
                    "data": element_data,
                }
            )

            processing_time = time.time() - start_time

            # Ensure performance requirement (<200ms)
            if processing_time > 0.2:
                logger.warning(
                    f"Interaction handling took {processing_time:.3f}s (>200ms limit)"
                )

            return InteractionResult(
                success=True,
                updated_chart=updated_chart,
                interaction_data=element_data,
                processing_time=processing_time,
                context_preserved=True,
            )

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Failed to handle chart interaction: {e}")

            return InteractionResult(
                success=False,
                updated_chart=None,
                interaction_data={},
                processing_time=processing_time,
                context_preserved=False,
                error=str(e),
            )

    def generate_interaction_handlers(self, chart_type: str) -> Dict[str, str]:
        """
        Generate JavaScript handlers for chart interactions

        REQUIREMENTS:
        - Vanilla JavaScript only (no external dependencies)
        - <50KB total JavaScript payload per chart
        - Mobile-touch support for tablet presentations
        - Accessibility compliance (keyboard navigation)
        """

        # Base interaction handlers (vanilla JavaScript)
        base_handlers = {
            "click_handler": """
                function handleChartClick(eventData) {
                    const chartId = eventData.target.closest('.chart-container').id;
                    const elementData = {
                        id: eventData.points[0].pointIndex,
                        data: eventData.points[0],
                        coordinates: { x: eventData.event.clientX, y: eventData.event.clientY }
                    };

                    // Send interaction to chart engine
                    sendInteraction('click', chartId, elementData);

                    // Visual feedback
                    highlightSelection(eventData.target);
                }
            """,
            "hover_handler": """
                function handleChartHover(eventData) {
                    const tooltip = document.createElement('div');
                    tooltip.className = 'chart-tooltip';
                    tooltip.innerHTML = formatTooltipContent(eventData.points[0]);
                    tooltip.style.cssText = `
                        position: absolute;
                        left: ${eventData.event.clientX + 10}px;
                        top: ${eventData.event.clientY - 30}px;
                        background: rgba(0,0,0,0.8);
                        color: white;
                        padding: 8px;
                        border-radius: 4px;
                        font-size: 12px;
                        pointer-events: none;
                        z-index: 1000;
                    `;
                    document.body.appendChild(tooltip);

                    setTimeout(() => tooltip.remove(), 3000);
                }
            """,
            "touch_handler": """
                function handleTouchInteraction(eventData) {
                    // Mobile-touch support for tablet presentations
                    if (eventData.touches && eventData.touches.length === 1) {
                        // Single touch - treat as click
                        handleChartClick(eventData);
                    } else if (eventData.touches && eventData.touches.length === 2) {
                        // Two finger gesture - zoom/pan
                        handleZoomPan(eventData);
                    }
                }
            """,
            "keyboard_handler": """
                function handleKeyboardNavigation(eventData) {
                    // Accessibility compliance (keyboard navigation)
                    const key = eventData.key;
                    const chartContainer = eventData.target.closest('.chart-container');

                    if (key === 'Enter' || key === ' ') {
                        // Activate current selection
                        const activeElement = chartContainer.querySelector('.active-element');
                        if (activeElement) {
                            activeElement.click();
                        }
                    } else if (key === 'ArrowUp' || key === 'ArrowDown' ||
                               key === 'ArrowLeft' || key === 'ArrowRight') {
                        // Navigate between chart elements
                        navigateChartElements(chartContainer, key);
                    }
                }
            """,
            "utility_functions": """
                function sendInteraction(eventType, chartId, elementData) {
                    // Send to ClaudeDirector's chat interface
                    const interactionData = {
                        event_type: eventType,
                        chart_id: chartId,
                        element_data: elementData,
                        timestamp: Date.now()
                    };

                    // Integration with chat interface
                    if (window.claudeDirectorChat) {
                        window.claudeDirectorChat.handleChartInteraction(interactionData);
                    }
                }

                function highlightSelection(element) {
                    // Visual feedback with Rachel's design system
                    element.style.filter = 'brightness(1.2)';
                    element.style.transition = 'filter 0.3s ease';

                    setTimeout(() => {
                        element.style.filter = 'none';
                    }, 1000);
                }

                function formatTooltipContent(dataPoint) {
                    return `
                        <strong>${dataPoint.data.name || 'Data Point'}</strong><br>
                        Value: ${dataPoint.y}<br>
                        Category: ${dataPoint.x}
                    `;
                }
            """,
        }

        # Chart-type specific enhancements
        if chart_type in ["roi_analysis", "investment_tracking"]:
            # Alvaro's business chart enhancements
            base_handlers[
                "business_specific"
            ] = """
                function formatBusinessTooltip(dataPoint) {
                    return `
                        <strong>${dataPoint.data.investment_name}</strong><br>
                        ROI: ${dataPoint.y}%<br>
                        Investment: $${dataPoint.data.amount.toLocaleString()}<br>
                        Status: ${dataPoint.data.status}
                    `;
                }
            """

        elif chart_type in ["architecture_health", "system_dependencies"]:
            # Martin's architecture chart enhancements
            base_handlers[
                "architecture_specific"
            ] = """
                function formatArchitectureTooltip(dataPoint) {
                    return `
                        <strong>${dataPoint.data.service_name}</strong><br>
                        Health: ${dataPoint.y}%<br>
                        Response Time: ${dataPoint.data.response_time}ms<br>
                        Dependencies: ${dataPoint.data.dependency_count}
                    `;
                }
            """

        # Combine all handlers and compress for <50KB limit
        combined_js = "\n".join(base_handlers.values())

        # Verify size constraint
        js_size_kb = len(combined_js.encode("utf-8")) / 1024
        if js_size_kb > 50:
            logger.warning(f"JavaScript payload {js_size_kb:.1f}KB exceeds 50KB limit")

        return {
            "combined_handlers": combined_js,
            "size_kb": js_size_kb,
            "chart_type": chart_type,
        }

    def _add_drill_down_capability(
        self, fig: go.Figure, chart_id: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Add click-to-drill-down functionality"""

        # Enable clickmode for drill-down
        fig.update_layout(clickmode="event+select", hovermode="closest")

        # Add drill-down metadata to traces
        for trace in fig.data:
            if hasattr(trace, "customdata"):
                # Add drill-down context to existing customdata
                if trace.customdata is None:
                    trace.customdata = []

                # Ensure each point has drill-down info
                for i, _ in enumerate(
                    trace.x if hasattr(trace, "x") else range(len(trace.values))
                ):
                    drill_context = {
                        "chart_id": chart_id,
                        "can_drill_down": True,
                        "drill_level": context.get("current_level", 0),
                        "next_level_data": context.get("drill_data", {}),
                    }

                    if len(trace.customdata) <= i:
                        trace.customdata.append(drill_context)
                    else:
                        trace.customdata[i].update(drill_context)

        return fig

    def _add_filtering_capability(
        self, fig: go.Figure, chart_id: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Add multi-select filtering capability"""

        fig.update_layout(selectmode="points+box", dragmode="select")

        # Add filter metadata
        for trace in fig.data:
            trace.selected = dict(marker=dict(color="#51cf66", size=8))
            trace.unselected = dict(marker=dict(color="rgba(0,0,0,0.3)", size=6))

        return fig

    def _add_navigation_capability(
        self, fig: go.Figure, chart_id: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Add zoom and pan controls"""

        fig.update_layout(
            dragmode="zoom",
            showlegend=True,
            xaxis=dict(
                fixedrange=False,
                rangeslider=dict(visible=False),  # Controlled zoom instead
            ),
            yaxis=dict(fixedrange=False),
        )

        return fig

    def _add_hover_details(
        self, fig: go.Figure, chart_id: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Add rich hover details"""

        fig.update_layout(
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)",
                bordercolor="#4dabf7",
                font_size=12,
                font_family="Segoe UI, sans-serif",
            ),
        )

        # Enhanced hover templates
        for trace in fig.data:
            if hasattr(trace, "hovertemplate"):
                trace.hovertemplate = (
                    "<b>%{fullData.name}</b><br>"
                    "Value: %{y}<br>"
                    "Category: %{x}<br>"
                    "<extra></extra>"
                )

        return fig

    def _add_time_brush_capability(
        self, fig: go.Figure, chart_id: str, context: Dict[str, Any]
    ) -> go.Figure:
        """Add time series brushing capability"""

        fig.update_layout(
            xaxis=dict(rangeslider=dict(visible=True, thickness=0.1), type="date"),
            selectmode="box",
        )

        return fig

    def _apply_interactive_styling(self, fig: go.Figure) -> go.Figure:
        """Apply Rachel's interactive design system"""

        fig.update_layout(
            transition_duration=self.interactive_theme["transition_duration"],
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
                size=12,
                color="#333",
            ),
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)",
                bordercolor=self.interactive_theme["hover_color"],
                font_color="white",
            ),
        )

        return fig

    async def _process_drill_down(
        self, session: Dict[str, Any], event: InteractionEvent
    ) -> Optional[go.Figure]:
        """Process drill-down interaction"""

        # Implementation would create new chart with drilled-down data
        # For now, return None to indicate no chart update
        logger.info(f"Processing drill-down for chart {event.chart_id}")
        return None

    async def _process_filter(
        self, session: Dict[str, Any], event: InteractionEvent
    ) -> Optional[go.Figure]:
        """Process filtering interaction"""

        logger.info(f"Processing filter for chart {event.chart_id}")
        return None

    async def _process_navigation(
        self, session: Dict[str, Any], event: InteractionEvent
    ) -> Optional[go.Figure]:
        """Process navigation interaction"""

        logger.info(f"Processing navigation for chart {event.chart_id}")
        return None

    def _update_interaction_metrics(self, processing_time: float, success: bool):
        """Update performance metrics"""

        self.interaction_metrics["total_interactions"] += 1
        if success:
            self.interaction_metrics["successful_interactions"] += 1

        # Update rolling average
        current_avg = self.interaction_metrics["avg_processing_time"]
        total = self.interaction_metrics["total_interactions"]
        self.interaction_metrics["avg_processing_time"] = (
            current_avg * (total - 1) + processing_time
        ) / total

        self.interaction_metrics["active_sessions"] = len(self.active_sessions)

    def get_metrics(self) -> Dict[str, Any]:
        """Get current interaction metrics"""
        return self.interaction_metrics.copy()

    def cleanup_expired_sessions(self, max_age_hours: int = 24):
        """Clean up expired interactive sessions"""

        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)

        expired_sessions = [
            session_id
            for session_id, session in self.active_sessions.items()
            if session.get("created_at", 0) < cutoff_time
        ]

        for session_id in expired_sessions:
            del self.active_sessions[session_id]
            if session_id in self.interaction_history:
                del self.interaction_history[session_id]

        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")


# Factory function for integration
def create_interactive_chart_engine() -> InteractiveChartEngine:
    """Create Interactive Chart Engine instance"""
    return InteractiveChartEngine()
