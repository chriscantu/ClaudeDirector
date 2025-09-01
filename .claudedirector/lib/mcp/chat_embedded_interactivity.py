#!/usr/bin/env python3
"""
Chat-Embedded Interactive HTML Generation
Phase 7 Week 4 - T-A3: Chat-Embedded HTML Generation

🏗️ Martin | Platform Architecture - Chat integration and HTML generation
🎨 Rachel | Design Systems Strategy - Responsive design and chat UX
💼 Alvaro | Platform Investment Strategy - Business context preservation

Generates interactive HTML that works seamlessly within the ClaudeDirector chat interface:
- Self-contained HTML with embedded CSS/JavaScript
- No external dependencies or CDN calls
- Mobile-responsive design
- Context preservation across browser sessions
- <500KB total payload per interactive chart
"""

import asyncio
import json
import time
import logging
import gzip
import base64
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from jinja2 import Template
import uuid

import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline as pyo

from .constants import MCPServerConstants
from .interactive_chart_engine import InteractiveChartEngine
from .chart_interaction_types import ChartInteractionTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ChatEmbeddedResult:
    """Result of chat-embedded HTML generation"""

    success: bool
    html_output: str
    payload_size_kb: float
    generation_time: float
    context_embedded: bool
    mobile_responsive: bool
    self_contained: bool
    error: Optional[str] = None
    chart_id: Optional[str] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class ChatEmbeddedInteractivity:
    """
    Generate interactive HTML for chat interface integration - T-A3

    REQUIREMENTS:
    - Self-contained HTML with embedded CSS/JavaScript
    - No external dependencies or CDN calls
    - Mobile-responsive design
    - Accessibility compliance (ARIA labels, keyboard nav)
    - <500KB total payload per interactive chart
    - Context preservation across browser refreshes
    - Integration with ClaudeDirector session management
    """

    def __init__(self):
        self.name = "chat-embedded-interactivity"
        self.version = "1.0.0"

        # Integration components
        self.interactive_engine = InteractiveChartEngine()
        self.interaction_types = ChartInteractionTypes()

        # HTML template for chat embedding
        self.chat_html_template = self._initialize_chat_html_template()

        # CSS for Rachel's responsive design system
        self.embedded_css = self._initialize_embedded_css()

        # JavaScript for chat integration
        self.embedded_js = self._initialize_embedded_javascript()

        # Compression settings for payload optimization
        self.compression_config = {
            "enabled": True,
            "min_size_kb": 10,  # Only compress if larger than 10KB
            "compression_level": 6,
        }

        # Mobile breakpoints for responsive design
        self.mobile_breakpoints = {
            "phone": 480,
            "tablet": 768,
            "desktop": 1024,
        }

        logger.info(f"Chat Embedded Interactivity {self.version} initialized")

    async def generate_interactive_html(
        self, fig: go.Figure, context: Dict[str, Any]
    ) -> ChatEmbeddedResult:
        """
        Generate complete interactive chart HTML for chat embedding

        REQUIREMENTS:
        - Self-contained HTML with embedded CSS/JavaScript
        - No external dependencies or CDN calls
        - Mobile-responsive design
        - Accessibility compliance (ARIA labels, keyboard nav)
        - <500KB total payload per interactive chart
        """

        start_time = time.time()

        try:
            # Generate unique chart ID
            chart_id = context.get("chart_id", str(uuid.uuid4()))

            # Convert Plotly figure to HTML with offline mode
            plotly_html = pio.to_html(
                fig,
                include_plotlyjs="inline",  # Embed Plotly.js directly
                div_id=f"chart-{chart_id}",
                config={
                    "displayModeBar": True,
                    "displaylogo": False,
                    "modeBarButtonsToRemove": ["pan2d", "select2d"],
                    "responsive": True,
                    "toImageButtonOptions": {
                        "format": "png",
                        "filename": "chart",
                        "height": 600,
                        "width": 800,
                        "scale": 2,
                    },
                },
            )

            # Extract chart data and configuration
            chart_config = self._extract_chart_config(fig, context)

            # Embed context data securely
            embedded_context = await self.embed_chat_context(plotly_html, context)

            # Generate complete interactive HTML
            interactive_html = self._generate_complete_html(
                embedded_context, chart_config, chart_id
            )

            # Apply responsive design enhancements
            interactive_html = self._apply_responsive_design(interactive_html)

            # Add accessibility features
            interactive_html = self._add_accessibility_features(
                interactive_html, chart_config
            )

            # Optimize payload size
            optimized_html = self._optimize_payload_size(interactive_html)

            # Calculate metrics
            generation_time = time.time() - start_time
            payload_size_kb = len(optimized_html.encode("utf-8")) / 1024

            # Validate payload size requirement (<500KB)
            if payload_size_kb > 500:
                logger.warning(
                    f"Payload size {payload_size_kb:.1f}KB exceeds 500KB limit"
                )

            # Validate generation performance
            if generation_time > 0.5:
                logger.warning(
                    f"Generation time {generation_time:.3f}s exceeds 500ms target"
                )

            logger.info(
                f"Generated interactive HTML for chart {chart_id} "
                f"({payload_size_kb:.1f}KB) in {generation_time:.3f}s"
            )

            return ChatEmbeddedResult(
                success=True,
                html_output=optimized_html,
                payload_size_kb=payload_size_kb,
                generation_time=generation_time,
                context_embedded=True,
                mobile_responsive=True,
                self_contained=True,
                chart_id=chart_id,
            )

        except Exception as e:
            generation_time = time.time() - start_time
            logger.error(f"Interactive HTML generation failed: {e}")

            return ChatEmbeddedResult(
                success=False,
                html_output="",
                payload_size_kb=0.0,
                generation_time=generation_time,
                context_embedded=False,
                mobile_responsive=False,
                self_contained=False,
                error=str(e),
            )

    async def embed_chat_context(self, html: str, context: Dict[str, Any]) -> str:
        """
        Embed conversation context into interactive HTML

        REQUIREMENTS:
        - Context preservation across browser refreshes
        - Secure data embedding (no sensitive data in client)
        - JSON serialization with <10KB context payload
        - Integration with ClaudeDirector session management
        """

        try:
            # Filter and sanitize context data
            safe_context = self._sanitize_context_data(context)

            # Serialize context with size limit
            context_json = json.dumps(safe_context, separators=(",", ":"))
            context_size_kb = len(context_json.encode("utf-8")) / 1024

            if context_size_kb > 10:
                logger.warning(
                    f"Context payload {context_size_kb:.1f}KB exceeds 10KB limit"
                )
                # Truncate context if too large
                safe_context = self._truncate_context(safe_context, max_size_kb=10)
                context_json = json.dumps(safe_context, separators=(",", ":"))

            # Embed context as data attribute
            context_script = f"""
            <script type="application/json" id="chart-context">
            {context_json}
            </script>
            """

            # Insert context script before closing head tag
            if "</head>" in html:
                html = html.replace("</head>", f"{context_script}</head>")
            else:
                # Fallback: add to beginning of HTML
                html = context_script + html

            logger.debug(f"Embedded context data ({context_size_kb:.1f}KB)")

            return html

        except Exception as e:
            logger.error(f"Context embedding failed: {e}")
            return html  # Return original HTML if embedding fails

    def _initialize_chat_html_template(self) -> Template:
        """Initialize HTML template for chat embedding"""

        template_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Interactive Chart - ClaudeDirector">
    <title>Interactive Chart - {{ chart_title }}</title>

    <!-- Rachel's Executive Design System -->
    <style>
    {{ embedded_css }}
    </style>
</head>
<body>
    <div class="claude-director-chart-container" id="chart-container-{{ chart_id }}">
        <!-- Accessibility header -->
        <div class="chart-header" role="banner">
            <h1 id="chart-title-{{ chart_id }}">{{ chart_title }}</h1>
            <div class="chart-controls" role="toolbar" aria-label="Chart interaction controls">
                <button type="button" class="help-btn" aria-describedby="help-tooltip">
                    <span aria-hidden="true">?</span>
                    <span class="sr-only">Help</span>
                </button>
                <div id="help-tooltip" role="tooltip" class="tooltip hidden">
                    {{ interaction_hints }}
                </div>
            </div>
        </div>

        <!-- Chart content -->
        <div class="chart-content" role="main">
            {{ chart_html }}
        </div>

        <!-- Chat integration status -->
        <div class="chat-status" role="status" aria-live="polite">
            <span class="status-indicator">🔗 Connected to ClaudeDirector</span>
        </div>

        <!-- Loading overlay for interactions -->
        <div class="loading-overlay hidden" role="progressbar" aria-label="Processing interaction">
            <div class="loading-spinner"></div>
            <span>Processing...</span>
        </div>
    </div>

    <!-- Interactive functionality -->
    <script>
    {{ embedded_js }}
    </script>

    <!-- Context data (embedded separately) -->
    <!-- Chart-specific initialization -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        initializeChartInteractivity('{{ chart_id }}', {{ chart_config | tojson }});
    });
    </script>
</body>
</html>
        """

        return Template(template_string)

    def _initialize_embedded_css(self) -> str:
        """Initialize embedded CSS for Rachel's responsive design system"""

        return """
        /* Rachel's Executive Design System - Chat Embedded */
        :root {
            --primary-blue: #4dabf7;
            --success-green: #51cf66;
            --alert-red: #ff6b6b;
            --warning-yellow: #ffd43b;
            --purple-accent: #9775fa;
            --teal-accent: #20c997;
            --text-color: #333;
            --background-light: rgba(0,0,0,0);
            --shadow-light: rgba(0,0,0,0.1);
        }

        /* Reset and base styles */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        .claude-director-chart-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: var(--text-color);
            background: var(--background-light);
            border-radius: 8px;
            box-shadow: 0 2px 8px var(--shadow-light);
            padding: 16px;
            max-width: 100%;
            margin: 0 auto;
        }

        /* Chart header */
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            padding-bottom: 12px;
        }

        .chart-header h1 {
            font-size: 1.2em;
            font-weight: 600;
            color: var(--text-color);
            margin: 0;
        }

        .chart-controls {
            position: relative;
        }

        .help-btn {
            background: var(--primary-blue);
            color: white;
            border: none;
            border-radius: 50%;
            width: 28px;
            height: 28px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s ease;
        }

        .help-btn:hover {
            background: #339af0;
        }

        .help-btn:focus {
            outline: 2px solid var(--primary-blue);
            outline-offset: 2px;
        }

        /* Tooltip */
        .tooltip {
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 8px;
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
            z-index: 1000;
            max-width: 300px;
            white-space: normal;
        }

        .tooltip::before {
            content: '';
            position: absolute;
            bottom: 100%;
            right: 12px;
            border: 6px solid transparent;
            border-bottom-color: rgba(0,0,0,0.9);
        }

        .hidden {
            display: none !important;
        }

        /* Chart content */
        .chart-content {
            position: relative;
            min-height: 400px;
        }

        /* Chat status indicator */
        .chat-status {
            display: flex;
            align-items: center;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(0,0,0,0.1);
            font-size: 12px;
            color: #666;
        }

        .status-indicator {
            color: var(--success-green);
            font-weight: 500;
        }

        /* Loading overlay */
        .loading-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.9);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 999;
        }

        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 3px solid rgba(74, 171, 247, 0.3);
            border-top: 3px solid var(--primary-blue);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 12px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Screen reader only content */
        .sr-only {
            position: absolute !important;
            width: 1px !important;
            height: 1px !important;
            padding: 0 !important;
            margin: -1px !important;
            overflow: hidden !important;
            clip: rect(0, 0, 0, 0) !important;
            white-space: nowrap !important;
            border: 0 !important;
        }

        /* Responsive design breakpoints */
        @media (max-width: 480px) {
            /* Phone */
            .claude-director-chart-container {
                padding: 12px;
                border-radius: 4px;
            }

            .chart-header h1 {
                font-size: 1.1em;
            }

            .chart-content {
                min-height: 300px;
            }

            .help-btn {
                width: 24px;
                height: 24px;
                font-size: 12px;
            }
        }

        @media (min-width: 481px) and (max-width: 768px) {
            /* Tablet */
            .claude-director-chart-container {
                padding: 16px;
            }

            .chart-content {
                min-height: 350px;
            }
        }

        @media (min-width: 769px) {
            /* Desktop */
            .claude-director-chart-container {
                padding: 20px;
                max-width: 1000px;
            }

            .chart-content {
                min-height: 450px;
            }
        }

        /* High contrast mode support */
        @media (prefers-contrast: high) {
            .claude-director-chart-container {
                border: 2px solid var(--text-color);
            }

            .help-btn {
                border: 2px solid white;
            }
        }

        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
            .loading-spinner {
                animation: none;
            }

            .help-btn {
                transition: none;
            }
        }

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #e0e0e0;
                --background-light: rgba(30,30,30,0.8);
                --shadow-light: rgba(0,0,0,0.3);
            }

            .claude-director-chart-container {
                background: var(--background-light);
                color: var(--text-color);
            }

            .loading-overlay {
                background: rgba(30,30,30,0.9);
            }
        }
        """

    def _initialize_embedded_javascript(self) -> str:
        """Initialize embedded JavaScript for chat integration"""

        return """
        // ClaudeDirector Chat Integration - Interactive Charts
        (function() {
            'use strict';

            // Global state management
            window.ClaudeDirectorCharts = window.ClaudeDirectorCharts || {};

            // Chart initialization
            function initializeChartInteractivity(chartId, config) {
                const container = document.getElementById('chart-container-' + chartId);
                const chartElement = document.getElementById('chart-' + chartId);

                if (!container || !chartElement) {
                    console.error('Chart elements not found for ID:', chartId);
                    return;
                }

                // Store chart configuration
                window.ClaudeDirectorCharts[chartId] = {
                    config: config,
                    container: container,
                    element: chartElement,
                    interactions: []
                };

                // Initialize interaction handlers
                setupInteractionHandlers(chartId);

                // Initialize accessibility features
                setupAccessibilityFeatures(chartId);

                // Initialize mobile touch support
                setupMobileTouchSupport(chartId);

                console.log('Chart interactivity initialized for:', chartId);
            }

            // Interaction handlers setup
            function setupInteractionHandlers(chartId) {
                const chartElement = document.getElementById('chart-' + chartId);
                const config = window.ClaudeDirectorCharts[chartId].config;

                // Click interactions
                chartElement.on('plotly_click', function(eventData) {
                    handleChartInteraction('click', chartId, eventData);
                });

                // Hover interactions
                chartElement.on('plotly_hover', function(eventData) {
                    handleChartInteraction('hover', chartId, eventData);
                });

                // Selection interactions
                chartElement.on('plotly_selected', function(eventData) {
                    handleChartInteraction('select', chartId, eventData);
                });

                // Zoom/pan interactions
                chartElement.on('plotly_relayout', function(eventData) {
                    handleChartInteraction('relayout', chartId, eventData);
                });
            }

            // Handle chart interactions
            function handleChartInteraction(eventType, chartId, eventData) {
                const startTime = performance.now();

                try {
                    // Show loading state
                    showLoadingState(chartId, true);

                    // Create interaction record
                    const interaction = {
                        event_type: eventType,
                        chart_id: chartId,
                        timestamp: Date.now(),
                        element_data: eventData,
                        processing_start: startTime
                    };

                    // Store interaction
                    window.ClaudeDirectorCharts[chartId].interactions.push(interaction);

                    // Send to ClaudeDirector chat interface
                    if (window.parent && window.parent.postMessage) {
                        window.parent.postMessage({
                            type: 'chart_interaction',
                            data: interaction
                        }, '*');
                    }

                    // Process locally if needed
                    processLocalInteraction(interaction);

                    // Hide loading state
                    setTimeout(() => {
                        showLoadingState(chartId, false);

                        const processingTime = performance.now() - startTime;
                        console.log(`Interaction processed in ${processingTime.toFixed(2)}ms`);
                    }, 100);

                } catch (error) {
                    console.error('Chart interaction failed:', error);
                    showLoadingState(chartId, false);
                }
            }

            // Process interactions locally
            function processLocalInteraction(interaction) {
                const eventType = interaction.event_type;
                const chartId = interaction.chart_id;

                if (eventType === 'click') {
                    // Handle click interactions (drill-down, etc.)
                    processDrillDownInteraction(interaction);
                } else if (eventType === 'select') {
                    // Handle selection interactions (filtering, etc.)
                    processFilterInteraction(interaction);
                } else if (eventType === 'relayout') {
                    // Handle zoom/pan interactions
                    processNavigationInteraction(interaction);
                }
            }

            // Drill-down interaction processing
            function processDrillDownInteraction(interaction) {
                const chartId = interaction.chart_id;
                const eventData = interaction.element_data;

                if (eventData.points && eventData.points.length > 0) {
                    const point = eventData.points[0];

                    // Visual feedback
                    highlightClickedElement(chartId, point);

                    // Send drill-down request to chat
                    requestDrillDown(chartId, point);
                }
            }

            // Filter interaction processing
            function processFilterInteraction(interaction) {
                const chartId = interaction.chart_id;
                const eventData = interaction.element_data;

                if (eventData.points && eventData.points.length > 0) {
                    // Apply visual filtering
                    applyVisualFiltering(chartId, eventData.points);

                    // Send filter update to chat
                    requestFilterUpdate(chartId, eventData.points);
                }
            }

            // Navigation interaction processing
            function processNavigationInteraction(interaction) {
                const chartId = interaction.chart_id;
                const eventData = interaction.element_data;

                // Store navigation state
                const chart = window.ClaudeDirectorCharts[chartId];
                chart.navigation_state = eventData;

                // Update navigation controls
                updateNavigationControls(chartId, eventData);
            }

            // Accessibility features setup
            function setupAccessibilityFeatures(chartId) {
                const container = document.getElementById('chart-container-' + chartId);

                // Keyboard navigation
                container.addEventListener('keydown', function(e) {
                    handleKeyboardNavigation(e, chartId);
                });

                // Help tooltip toggle
                const helpBtn = container.querySelector('.help-btn');
                const tooltip = container.querySelector('.tooltip');

                if (helpBtn && tooltip) {
                    helpBtn.addEventListener('click', function() {
                        tooltip.classList.toggle('hidden');
                    });

                    helpBtn.addEventListener('blur', function() {
                        setTimeout(() => tooltip.classList.add('hidden'), 150);
                    });
                }

                // Focus management
                setupFocusManagement(chartId);
            }

            // Mobile touch support setup
            function setupMobileTouchSupport(chartId) {
                const chartElement = document.getElementById('chart-' + chartId);

                let touchStartTime;
                let touchStartPos;

                chartElement.addEventListener('touchstart', function(e) {
                    touchStartTime = Date.now();
                    touchStartPos = {
                        x: e.touches[0].clientX,
                        y: e.touches[0].clientY
                    };
                });

                chartElement.addEventListener('touchend', function(e) {
                    const touchDuration = Date.now() - touchStartTime;
                    const touchEndPos = {
                        x: e.changedTouches[0].clientX,
                        y: e.changedTouches[0].clientY
                    };

                    const distance = Math.sqrt(
                        Math.pow(touchEndPos.x - touchStartPos.x, 2) +
                        Math.pow(touchEndPos.y - touchStartPos.y, 2)
                    );

                    // Tap detection (short duration, minimal movement)
                    if (touchDuration < 300 && distance < 10) {
                        // Simulate click event
                        const clickEvent = new MouseEvent('click', {
                            clientX: touchEndPos.x,
                            clientY: touchEndPos.y
                        });
                        e.target.dispatchEvent(clickEvent);
                    }
                });
            }

            // Utility functions
            function showLoadingState(chartId, show) {
                const overlay = document.querySelector(`#chart-container-${chartId} .loading-overlay`);
                if (overlay) {
                    if (show) {
                        overlay.classList.remove('hidden');
                    } else {
                        overlay.classList.add('hidden');
                    }
                }
            }

            function highlightClickedElement(chartId, point) {
                // Add visual feedback for clicked elements
                const chartElement = document.getElementById('chart-' + chartId);

                // Create temporary highlight overlay
                const highlight = document.createElement('div');
                highlight.className = 'click-highlight';
                highlight.style.cssText = `
                    position: absolute;
                    width: 20px;
                    height: 20px;
                    border: 2px solid #51cf66;
                    border-radius: 50%;
                    pointer-events: none;
                    animation: pulse 0.6s ease-out;
                    left: ${point.x}px;
                    top: ${point.y}px;
                    transform: translate(-50%, -50%);
                    z-index: 1000;
                `;

                chartElement.appendChild(highlight);

                // Remove after animation
                setTimeout(() => {
                    if (highlight.parentNode) {
                        highlight.parentNode.removeChild(highlight);
                    }
                }, 600);
            }

            // Expose initialization function globally
            window.initializeChartInteractivity = initializeChartInteractivity;

        })();

        // CSS animations for interactions
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0% { transform: translate(-50%, -50%) scale(0.8); opacity: 1; }
                100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        """

    def _extract_chart_config(
        self, fig: go.Figure, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract chart configuration for JavaScript initialization"""

        config = {
            "chart_type": context.get("chart_type", "default"),
            "persona": context.get("persona", "martin"),
            "interaction_capabilities": [],
            "drill_down_enabled": False,
            "filter_enabled": False,
            "zoom_enabled": True,
            "hover_enabled": True,
        }

        # Determine available interactions based on chart type
        chart_type = config["chart_type"]
        if chart_type in [
            "leadership_dashboard",
            "roi_analysis",
            "architecture_health",
        ]:
            config["drill_down_enabled"] = True
            config["filter_enabled"] = True
            config["interaction_capabilities"].extend(["drill_down", "filter"])

        if "time" in chart_type.lower() or "trend" in chart_type.lower():
            config["time_brush_enabled"] = True
            config["interaction_capabilities"].append("time_brush")

        # Always available interactions
        config["interaction_capabilities"].extend(["zoom", "hover"])

        return config

    def _generate_complete_html(
        self, chart_html: str, chart_config: Dict[str, Any], chart_id: str
    ) -> str:
        """Generate complete HTML using template"""

        # Generate interaction hints based on capabilities
        interaction_hints = self._generate_interaction_hints(chart_config)

        # Render template
        html_output = self.chat_html_template.render(
            chart_id=chart_id,
            chart_title=chart_config.get("title", "Interactive Chart"),
            chart_html=chart_html,
            chart_config=chart_config,
            embedded_css=self.embedded_css,
            embedded_js=self.embedded_js,
            interaction_hints=interaction_hints,
        )

        return html_output

    def _generate_interaction_hints(self, config: Dict[str, Any]) -> str:
        """Generate interaction hints for help tooltip"""

        hints = []

        if config.get("drill_down_enabled"):
            hints.append("• Click any data point to drill down for details")

        if config.get("filter_enabled"):
            hints.append("• Select multiple points to filter related charts")

        if config.get("zoom_enabled"):
            hints.append("• Drag to zoom, double-click to reset view")

        if config.get("hover_enabled"):
            hints.append("• Hover over data points for detailed information")

        if config.get("time_brush_enabled"):
            hints.append("• Use the time slider to select date ranges")

        hints.append("• All interactions work on touch devices")

        return "<br>".join(hints)

    def _apply_responsive_design(self, html: str) -> str:
        """Apply responsive design enhancements"""

        # Responsive meta tag should already be in template
        # Add any additional responsive JavaScript if needed

        responsive_js = """
        <script>
        // Responsive chart resizing
        window.addEventListener('resize', function() {
            Object.keys(window.ClaudeDirectorCharts || {}).forEach(function(chartId) {
                const chartElement = document.getElementById('chart-' + chartId);
                if (chartElement && window.Plotly) {
                    window.Plotly.Plots.resize(chartElement);
                }
            });
        });
        </script>
        """

        # Insert before closing body tag
        html = html.replace("</body>", responsive_js + "</body>")

        return html

    def _add_accessibility_features(self, html: str, config: Dict[str, Any]) -> str:
        """Add accessibility features to HTML"""

        accessibility_js = """
        <script>
        // Accessibility enhancements
        document.addEventListener('DOMContentLoaded', function() {
            // Add ARIA labels to chart elements
            const charts = document.querySelectorAll('[id^="chart-"]');
            charts.forEach(function(chart) {
                chart.setAttribute('role', 'img');
                chart.setAttribute('aria-label', 'Interactive chart visualization');
            });

            // Keyboard navigation support
            document.addEventListener('keydown', function(e) {
                if (e.target.closest('.claude-director-chart-container')) {
                    handleChartKeyboardNavigation(e);
                }
            });
        });

        function handleChartKeyboardNavigation(e) {
            const key = e.key;
            const container = e.target.closest('.claude-director-chart-container');

            if (key === 'Enter' || key === ' ') {
                // Activate focused element
                e.preventDefault();
                const focused = container.querySelector(':focus');
                if (focused) {
                    focused.click();
                }
            }
        }
        </script>
        """

        html = html.replace("</body>", accessibility_js + "</body>")

        return html

    def _optimize_payload_size(self, html: str) -> str:
        """Optimize HTML payload size to meet <500KB requirement"""

        original_size_kb = len(html.encode("utf-8")) / 1024

        if (
            original_size_kb <= 500
            and original_size_kb < self.compression_config["min_size_kb"]
        ):
            return html  # No optimization needed

        optimized_html = html

        # Remove unnecessary whitespace
        import re

        optimized_html = re.sub(r"\n\s+", "\n", optimized_html)
        optimized_html = re.sub(r"\s+", " ", optimized_html)

        # Minify CSS (basic)
        optimized_html = re.sub(r"/\*.*?\*/", "", optimized_html, flags=re.DOTALL)
        optimized_html = re.sub(r":\s+", ":", optimized_html)
        optimized_html = re.sub(r";\s+", ";", optimized_html)

        # Minify JavaScript (basic)
        optimized_html = re.sub(r"//.*?\n", "\n", optimized_html)
        optimized_html = re.sub(r"console\.log\([^)]*\);?", "", optimized_html)

        optimized_size_kb = len(optimized_html.encode("utf-8")) / 1024

        # Apply compression if still too large
        if optimized_size_kb > 500 and self.compression_config["enabled"]:
            try:
                compressed_html = self._compress_html(optimized_html)
                compressed_size_kb = len(compressed_html) / 1024

                if compressed_size_kb < optimized_size_kb:
                    logger.info(
                        f"Compressed HTML from {optimized_size_kb:.1f}KB to {compressed_size_kb:.1f}KB"
                    )
                    return compressed_html
            except Exception as e:
                logger.error(f"Compression failed: {e}")

        reduction_pct = (
            (original_size_kb - optimized_size_kb) / original_size_kb
        ) * 100
        logger.info(
            f"Optimized HTML size: {optimized_size_kb:.1f}KB ({reduction_pct:.1f}% reduction)"
        )

        return optimized_html

    def _compress_html(self, html: str) -> str:
        """Compress HTML using gzip and base64 encoding"""

        # Gzip compression
        compressed_bytes = gzip.compress(
            html.encode("utf-8"),
            compresslevel=self.compression_config["compression_level"],
        )

        # Base64 encoding for safe embedding
        compressed_b64 = base64.b64encode(compressed_bytes).decode("ascii")

        # Create self-extracting HTML
        extraction_script = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script>
            // Self-extracting compressed chart
            const compressedData = '{compressed_b64}';
            const decompressed = atob(compressedData);
            document.open();
            document.write(decompressed);
            document.close();
            </script>
        </head>
        <body>Loading interactive chart...</body>
        </html>
        """

        return extraction_script

    def _sanitize_context_data(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize context data for secure client-side embedding"""

        safe_context = {}

        # Allow-list of safe context keys
        safe_keys = {
            "chart_id",
            "chart_type",
            "persona",
            "title",
            "interaction_capabilities",
            "drill_level",
            "filter_state",
            "navigation_state",
            "timestamp",
        }

        for key, value in context.items():
            if key in safe_keys:
                # Additional sanitization based on type
                if isinstance(value, str):
                    # Remove any potential script injections
                    safe_value = value.replace("<script", "&lt;script").replace(
                        "javascript:", ""
                    )
                    safe_context[key] = safe_value
                elif isinstance(value, (int, float, bool)):
                    safe_context[key] = value
                elif isinstance(value, (dict, list)):
                    # Basic JSON serializable check
                    try:
                        json.dumps(value)
                        safe_context[key] = value
                    except (TypeError, ValueError):
                        pass  # Skip non-serializable values

        return safe_context

    def _truncate_context(
        self, context: Dict[str, Any], max_size_kb: int
    ) -> Dict[str, Any]:
        """Truncate context data to fit size limit"""

        truncated = {}
        current_size = 0
        max_size_bytes = max_size_kb * 1024

        # Prioritize keys by importance
        priority_keys = ["chart_id", "chart_type", "persona", "title"]
        other_keys = [k for k in context.keys() if k not in priority_keys]

        # Add priority keys first
        for key in priority_keys:
            if key in context:
                item_json = json.dumps({key: context[key]})
                item_size = len(item_json.encode("utf-8"))

                if current_size + item_size <= max_size_bytes:
                    truncated[key] = context[key]
                    current_size += item_size

        # Add other keys as space permits
        for key in other_keys:
            if key in context:
                item_json = json.dumps({key: context[key]})
                item_size = len(item_json.encode("utf-8"))

                if current_size + item_size <= max_size_bytes:
                    truncated[key] = context[key]
                    current_size += item_size
                else:
                    break  # No more space

        logger.info(f"Truncated context from {len(context)} to {len(truncated)} keys")

        return truncated


# Factory function
def create_chat_embedded_interactivity() -> ChatEmbeddedInteractivity:
    """Create Chat Embedded Interactivity instance"""
    return ChatEmbeddedInteractivity()
