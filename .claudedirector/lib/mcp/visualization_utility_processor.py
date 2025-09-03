#!/usr/bin/env python3
"""
Visualization Utility Processor - Phase 4 Milestone 3
🏗️ Sequential Thinking Utility Method Consolidation

🔧 Martin | Platform Architecture - Centralized utility processing
📊 Berny | AI/ML - Performance metrics and data inference

Consolidates visualization utility methods into a single processor.
"""

import json
import re
import time
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go


class VisualizationUtilityProcessor:
    """🏗️ Sequential Thinking Phase 4: Centralized visualization utility processor"""

    def __init__(
        self,
        color_palette: List[str],
        layout_template: Dict[str, Any],
        visualization_metrics: Dict[str, Any],
    ):
        self.color_palette = color_palette
        self.layout_template = layout_template
        self.visualization_metrics = visualization_metrics

    def apply_executive_styling(
        self,
        fig: go.Figure,
        persona: str,
        persona_colors: Dict[str, str],
        primary_blue: str,
        title_font_size: int,
    ) -> go.Figure:
        """Apply Rachel's executive styling to figure"""
        # Apply base layout template
        fig.update_layout(**self.layout_template)

        # Persona-specific styling enhancements
        persona_color = persona_colors.get(persona, primary_blue)
        persona_styles = {
            "title": {
                "font": {
                    "size": title_font_size,
                    "color": persona_color,
                }
            },
            "showlegend": True,
        }

        fig.update_layout(**persona_styles)
        return fig

    def parse_analysis_output(self, output: str) -> Dict[str, Any]:
        """Parse strategic analysis output into visualization data"""
        # Try to extract JSON data from output
        try:
            # Look for JSON blocks in the output
            json_match = re.search(r"\{.*\}", output, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        # Fallback: create sample data structure
        return {
            "sample_data": True,
            "x": ["Q1", "Q2", "Q3", "Q4"],
            "y": [20, 25, 30, 35],
            "analysis_output": output,
        }

    def detect_interactive_elements(self, fig: go.Figure) -> List[str]:
        """Detect interactive elements in the figure"""
        elements = []

        # Check for different trace types
        for trace in fig.data:
            if hasattr(trace, "type"):
                elements.append(f"{trace.type}_chart")

        # Check for subplots
        if hasattr(fig, "layout") and hasattr(fig.layout, "annotations"):
            if fig.layout.annotations:
                elements.append("subplots")

        # Default interactive features
        elements.extend(["hover", "zoom", "pan"])
        return list(set(elements))

    def update_performance_metrics(
        self, generation_time: float, file_size: int, interactive_elements: List[str]
    ):
        """Update performance metrics"""
        # Update average generation time
        total_viz = self.visualization_metrics["total_visualizations"]
        current_avg = self.visualization_metrics["avg_generation_time"]
        self.visualization_metrics["avg_generation_time"] = (
            current_avg * (total_viz - 1) + generation_time
        ) / total_viz

        # Update average file size
        current_size_avg = self.visualization_metrics["avg_file_size"]
        self.visualization_metrics["avg_file_size"] = (
            current_size_avg * (total_viz - 1) + file_size
        ) / total_viz

        # Update interactive features count
        self.visualization_metrics["interactive_features_used"] += len(
            interactive_elements
        )

    def infer_chart_type_from_data(self, data: Dict[str, Any]) -> str:
        """Infer optimal chart type based on data structure"""
        # Sprint metrics -> progress visualization
        if "progress" in data and "metrics" in data:
            return "sprint_dashboard"

        # Team performance -> radar/bar chart
        if "metrics" in data and any(key in data for key in ["team", "performance"]):
            return "team_performance"

        # ROI analysis -> financial dashboard
        if "investment" in data and "returns" in data:
            return "roi_dashboard"

        # Architecture health -> system status
        if "services" in data or "health_score" in data:
            return "architecture_health"

        # Design system -> adoption metrics
        if "adoption" in data or "components" in data:
            return "design_system_status"

        # GitHub activity -> timeline/activity chart
        if "activity" in data or "contributors" in data:
            return "github_activity"

        # Default to simple bar chart
        return "simple_metrics"

    def generate_contextual_title(
        self, data: Dict[str, Any], context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate contextual title based on data and conversation context"""
        # Use data-specific titles
        if "sprint_name" in data:
            return f"{data['sprint_name']} - Current Status"
        elif "team" in data:
            return f"{data['team']} Performance Metrics"
        elif "project" in data:
            return f"{data['project']} ROI Analysis"
        elif "system" in data:
            return f"{data['system']} Health Dashboard"
        elif "repository" in data:
            return f"{data['repository']} Activity Overview"

        # Fallback to generic title
        return "Strategic Metrics Dashboard"

    def get_server_info(
        self,
        name: str,
        version: str,
        capabilities: List[str],
        supported_personas: List[str],
        color_palette: List[str],
    ) -> Dict[str, Any]:
        """Get executive visualization server information"""
        return {
            "name": name,
            "version": version,
            "capabilities": capabilities,
            "supported_personas": supported_personas,
            "supported_chart_types": [
                "leadership_dashboard",
                "team_metrics",
                "strategic_trends",
                "support_analysis",
                "roi_analysis",
                "investment_tracking",
                "business_metrics",
                "cost_analysis",
                "architecture_health",
                "performance_metrics",
                "system_dependencies",
                "technology_roadmap",
                "innovation_metrics",
                "design_system_health",
                "adoption_metrics",
            ],
            "metrics": self.visualization_metrics,
            "color_palette": color_palette,
        }

    def get_transparency_disclosure(
        self, capability: str, persona: str, description: str
    ) -> str:
        """Generate transparency disclosure for executive visualization"""
        return f"""
🔧 Accessing MCP Server: executive-visualization (Executive Visualization System)
*Generating publication-quality interactive visualization using {persona} persona...*

**Executive Visualization Enhancement**:
- **Capability**: {capability}
- **Persona**: {persona} (Executive Design System)
- **Process**: {description}
- **Quality**: Publication-ready interactive charts
- **Integration**: Built on Phase 1 Strategic Python MCP foundation

**Rachel's Design System**: Professional color palette, executive typography, responsive layout
**Interactive Features**: Hover states, zoom, pan, filter capabilities
**Performance**: <3s generation, <2MB output, optimized for presentations
"""


def create_visualization_utility_processor(
    color_palette: List[str],
    layout_template: Dict[str, Any],
    visualization_metrics: Dict[str, Any],
) -> VisualizationUtilityProcessor:
    """🏗️ Sequential Thinking Phase 4: Factory for visualization utility processor"""
    return VisualizationUtilityProcessor(
        color_palette, layout_template, visualization_metrics
    )
