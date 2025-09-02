#!/usr/bin/env python3
"""
Persona Template Manager
Phase 3A.2.2: Persona Template Extraction for SOLID Compliance

🏗️ Martin | Platform Architecture - Single Responsibility Principle
🎨 Rachel | Design Systems Strategy - Persona-specific visualization templates
💼 Alvaro | Business Strategy - Executive visualization requirements

Extracted from ExecutiveVisualizationEngine to manage persona-specific
visualization templates with clean separation of concerns.
"""

import plotly.graph_objects as go
from typing import Dict, Any, Callable
from ..constants import MCPServerConstants


class PersonaTemplateManager:
    """
    Manages persona-specific visualization templates and styling.

    Single Responsibility: Persona template management and selection.
    Provides specialized visualization templates for different strategic personas.
    """

    def __init__(self):
        """Initialize persona template management"""
        # Persona-specific template mapping
        self.persona_templates: Dict[str, Callable] = {
            MCPServerConstants.Personas.DIEGO: self._diego_leadership_template,
            MCPServerConstants.Personas.ALVARO: self._alvaro_business_template,
            MCPServerConstants.Personas.MARTIN: self._martin_architecture_template,
            MCPServerConstants.Personas.CAMILLE: self._camille_technology_template,
            MCPServerConstants.Personas.RACHEL: self._rachel_design_template,
        }

        # Executive layout template
        self.layout_template = MCPServerConstants.get_executive_layout_template()

    def get_template_for_persona(self, persona: str) -> Callable:
        """Get the appropriate template function for a persona"""
        return self.persona_templates.get(
            persona, self._diego_leadership_template  # Default fallback
        )

    def get_supported_personas(self) -> list:
        """Get list of supported personas"""
        return list(self.persona_templates.keys())

    def _diego_leadership_template(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """Diego's leadership-focused visualization template"""
        if chart_type == "leadership_dashboard":
            return self._create_leadership_dashboard(data, title)
        elif chart_type == "team_metrics":
            return self._create_team_metrics_chart(data, title)
        elif chart_type == "strategic_trends":
            return self._create_strategic_trends_chart(data, title)
        elif chart_type == "support_analysis":
            return self._create_support_analysis_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _alvaro_business_template(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """Alvaro's business strategy visualization template"""
        if chart_type == "roi_dashboard":
            return self._create_roi_dashboard(data, title)
        elif chart_type == "investment_analysis":
            return self._create_investment_chart(data, title)
        elif chart_type == "business_metrics":
            return self._create_business_metrics_chart(data, title)
        elif chart_type == "cost_analysis":
            return self._create_cost_analysis_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _martin_architecture_template(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """Martin's platform architecture visualization template"""
        if chart_type == "architecture_health":
            return self._create_architecture_health_dashboard(data, title)
        elif chart_type == "service_performance":
            return self._create_service_performance_chart(data, title)
        elif chart_type == "system_metrics":
            return self._create_system_metrics_chart(data, title)
        elif chart_type == "performance_trends":
            return self._create_performance_chart(data, title)
        elif chart_type == "dependency_analysis":
            return self._create_dependency_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _camille_technology_template(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """Camille's technology strategy visualization template"""
        if chart_type == "technology_trends":
            return self._create_technology_trends_chart(data, title)
        elif chart_type == "innovation_metrics":
            return self._create_innovation_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    def _rachel_design_template(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """Rachel's design systems visualization template"""
        if chart_type == "design_system_health":
            return self._create_design_system_dashboard(data, title)
        elif chart_type == "team_comparison":
            return self._create_team_comparison_dashboard(data, title)
        elif chart_type == "component_adoption":
            return self._create_component_adoption_chart(data, title)
        elif chart_type == "adoption_metrics":
            return self._create_adoption_chart(data, title)
        else:
            return self._create_default_chart(data, chart_type, title)

    # Note: Actual chart creation methods would be injected via dependency injection
    # or delegated to specialized chart factories. This maintains clean separation
    # of concerns while preserving template functionality.

    def _create_default_chart(
        self, data: Dict[str, Any], chart_type: str, title: str
    ) -> go.Figure:
        """Default fallback chart creation - delegates to chart factory"""
        # This would delegate to a ChartFactory in the full implementation
        # For now, maintaining minimal structure for extraction
        fig = go.Figure()
        fig.update_layout(title=title, **self.layout_template)
        return fig
