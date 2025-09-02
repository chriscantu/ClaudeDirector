#!/usr/bin/env python3
"""
Visualization Template Router
Phase 3B.2.1: Consolidated template routing for executive visualization server

🏗️ Martin | Platform Architecture - DRY principle consolidation
🎨 Rachel | Design Systems Strategy - Persona template optimization
💼 Alvaro | Business Strategy - Template routing efficiency
🤖 Berny | AI/ML Engineering - Performance optimization through consolidation

Replaces 5 persona template methods with single consolidated router.
NET REDUCTION TARGET: -70 lines from template consolidation.
"""

from typing import Dict, Any, Callable
import plotly.graph_objects as go


class VisualizationTemplateRouter:
    """
    Consolidated template router replacing 5 duplicate persona template methods
    Implements DRY principle for template method patterns
    """

    def __init__(self, visualization_engine):
        """Initialize router with reference to visualization engine"""
        self.engine = visualization_engine

        # Persona template mappings (Phase 3B.2.1 - DRY consolidation)
        self.persona_mappings = {
            'diego': {
                'leadership_dashboard': self.engine._create_leadership_dashboard,
                'team_metrics': self.engine._create_team_metrics_chart,
                'strategic_trends': self.engine._create_strategic_trends_chart,
                'support_analysis': self.engine._create_support_analysis_chart,
            },
            'alvaro': {
                'roi_analysis': self.engine._create_roi_dashboard,
                'investment_tracking': self.engine._create_investment_chart,
                'business_metrics': self.engine._create_business_metrics_chart,
                'cost_analysis': self.engine._create_cost_analysis_chart,
            },
            'martin': {
                'architecture_health': self.engine._create_architecture_health_dashboard,
                'service_performance': self.engine._create_service_performance_chart,
                'system_dependency_map': self.engine._create_system_dependency_map,
                'technical_debt_trends': self.engine._create_technical_debt_trends,
                'performance_metrics': self.engine._create_performance_chart,
                'system_dependencies': self.engine._create_dependency_chart,
            },
            'camille': {
                'technology_roadmap': self.engine._create_technology_roadmap,
                'innovation_metrics': self.engine._create_innovation_chart,
            },
            'rachel': {
                'component_adoption': self.engine._create_component_adoption_chart,
                'design_system_maturity': self.engine._create_design_system_maturity,
                'usage_trend_analysis': self.engine._create_usage_trend_analysis,
                'team_comparison': self.engine._create_team_comparison_dashboard,
                'design_debt_visualization': self.engine._create_design_debt_visualization,
                'design_system_health': self.engine._create_design_system_dashboard,
                'adoption_metrics': self.engine._create_adoption_chart,
            },
        }

    def get_template_for_persona(self, persona: str) -> Callable:
        """
        Consolidated template router - replaces 5 duplicate template methods
        Returns unified template function for any persona

        Args:
            persona: Persona identifier (diego, alvaro, martin, camille, rachel)

        Returns:
            Template function for the specified persona
        """
        return lambda data, chart_type, title, context: self._route_template(
            persona, data, chart_type, title, context
        )

    def _route_template(
        self,
        persona: str,
        data: Dict[str, Any],
        chart_type: str,
        title: str,
        context: Dict[str, Any]
    ) -> go.Figure:
        """
        Unified template routing logic - replaces all duplicate if/elif chains

        Args:
            persona: Persona identifier
            data: Visualization data
            chart_type: Type of chart to create
            title: Chart title
            context: Additional context

        Returns:
            Plotly figure based on persona and chart type
        """
        persona_lower = persona.lower()

        # Get persona-specific mappings
        mappings = self.persona_mappings.get(persona_lower, {})

        # Route to specific chart creation method
        chart_method = mappings.get(chart_type)

        if chart_method:
            return chart_method(data, title)
        else:
            # Fallback to default chart
            return self.engine._create_default_chart(data, chart_type, title)
