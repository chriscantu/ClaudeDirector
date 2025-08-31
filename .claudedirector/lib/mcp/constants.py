#!/usr/bin/env python3
"""
MCP Server Constants
Centralized constants for Strategic Python MCP and Executive Visualization systems

🏗️ Martin | Platform Architecture - Constants refactoring for maintainability
🎯 Phase 2 Enhancement - Eliminates hard-coded strings across MCP infrastructure

This module provides a single source of truth for all MCP server configuration,
capabilities, personas, and system messages to improve maintainability and consistency.
"""

from typing import List, Dict, Any


class MCPServerConstants:
    """Core MCP server constants and configuration"""

    # Server Identity
    STRATEGIC_PYTHON_SERVER_NAME = "strategic-python"
    STRATEGIC_PYTHON_SERVER_VERSION = "1.0.0"

    EXECUTIVE_VISUALIZATION_SERVER_NAME = "executive-visualization"
    EXECUTIVE_VISUALIZATION_SERVER_VERSION = "1.0.0"

    INTEGRATED_WORKFLOW_NAME = "integrated-visualization-workflow"
    INTEGRATED_WORKFLOW_VERSION = "1.0.0"

    class Capabilities:
        """MCP server capabilities constants"""

        # Strategic Python MCP Capabilities
        STRATEGIC_DATA_ANALYSIS = "strategic_data_analysis"
        ROI_CALCULATIONS = "roi_calculations"
        STAKEHOLDER_ANALYTICS = "stakeholder_analytics"
        PERFORMANCE_METRICS = "performance_metrics"
        EXECUTIVE_REPORTING = "executive_reporting"

        # Executive Visualization Capabilities
        EXECUTIVE_DASHBOARDS = "executive_dashboards"
        INTERACTIVE_CHARTS = "interactive_charts"
        STRATEGIC_PRESENTATIONS = "strategic_presentations"
        PUBLICATION_QUALITY_VISUALS = "publication_quality_visuals"

        # Integrated Workflow Capabilities
        INTEGRATED_STRATEGIC_ANALYSIS = "integrated_strategic_analysis"
        DATA_DRIVEN_VISUALIZATIONS = "data_driven_visualizations"
        EXECUTIVE_READY_PRESENTATIONS = "executive_ready_presentations"
        END_TO_END_INTELLIGENCE = "end_to_end_intelligence"

    class Personas:
        """Strategic persona constants"""

        DIEGO = "diego"
        ALVARO = "alvaro"
        MARTIN = "martin"
        CAMILLE = "camille"
        RACHEL = "rachel"

        # Persona display names
        PERSONA_TITLES = {
            DIEGO: "Engineering Leadership",
            ALVARO: "Business Strategy",
            MARTIN: "Platform Architecture",
            CAMILLE: "Strategic Technology",
            RACHEL: "Design Systems Strategy",
        }

        # Persona focus areas
        PERSONA_FOCUS = {
            DIEGO: "leadership_metrics",
            ALVARO: "business_intelligence",
            MARTIN: "architecture_analysis",
            CAMILLE: "strategic_technology",
            RACHEL: "design_analytics",
        }

    class Security:
        """Security configuration constants"""

        # Configuration keys
        MAX_EXECUTION_TIME_KEY = "max_execution_time"
        MAX_MEMORY_MB_KEY = "max_memory_mb"
        ALLOWED_IMPORTS_KEY = "allowed_imports"
        BLOCKED_IMPORTS_KEY = "blocked_imports"
        BLOCKED_OPERATIONS_KEY = "blocked_operations"

        # Default values
        DEFAULT_MAX_EXECUTION_TIME = 30  # seconds
        DEFAULT_MAX_MEMORY_MB = 512  # MB

        # Allowed imports for strategic analysis
        ALLOWED_IMPORTS = [
            "pandas",
            "numpy",
            "json",
            "datetime",
            "time",
            "math",
            "statistics",
            "collections",
            "itertools",
            "functools",
            "operator",
            "decimal",
            "fractions",
        ]

        # Blocked imports for security
        BLOCKED_IMPORTS = [
            "os",
            "sys",
            "subprocess",
            "socket",
            "urllib",
            "requests",
            "shutil",
            "glob",
            "pickle",
            "marshal",
            "importlib",
            "exec",
            "eval",
            "__import__",
        ]

        # Blocked operations for security
        BLOCKED_OPERATIONS = [
            "open(",
            "file(",
            "exec(",
            "eval(",
            "compile(",
            "subprocess",
            "__import__",
            "globals(",
            "locals(",
            "vars(",
            "dir(",
            "getattr(",
            "setattr(",
            "delattr(",
        ]

        # Dangerous patterns
        DANGEROUS_PATTERNS = [
            "__",
            "exec",
            "eval",
            "compile",
            "globals",
            "locals",
            "getattr",
            "setattr",
            "delattr",
            "hasattr",
        ]

    class ErrorMessages:
        """Standardized error messages"""

        # Strategic scope violations
        SCOPE_VIOLATION = "Code outside strategic scope. Only strategic analysis allowed."
        EXECUTION_TIMEOUT = "Execution timeout exceeded ({timeout}s)"
        INVALID_REQUEST = "Invalid MCP request: capability or persona not supported"

        # Execution errors
        EXECUTION_ERROR = "Execution error: {error}"
        STRATEGIC_PYTHON_EXECUTION_ERROR = "Strategic Python execution error: {error}"
        VISUALIZATION_GENERATION_ERROR = "Visualization generation error: {error}"
        INTEGRATED_WORKFLOW_ERROR = "Integrated workflow error: {error}"

        # MCP integration errors
        MCP_INTEGRATION_ERROR = "MCP integration error: {error}"
        MCP_REQUEST_PROCESSING_ERROR = "MCP request processing error: {error}"

        # Security warnings
        BLOCKED_IMPORT_WARNING = "Blocked import detected: {import_name}"
        BLOCKED_OPERATION_WARNING = "Blocked operation detected: {operation}"
        DANGEROUS_PATTERN_WARNING = "Potentially dangerous pattern detected: {pattern}"

        # Health check errors
        HEALTH_CHECK_FAILED = "Health check failed: {error}"
        INTEGRATED_WORKFLOW_HEALTH_CHECK_FAILED = "Integrated workflow health check failed: {error}"

    class ChartTypes:
        """Visualization chart type constants"""

        # Diego's leadership charts
        LEADERSHIP_DASHBOARD = "leadership_dashboard"
        TEAM_METRICS = "team_metrics"
        STRATEGIC_TRENDS = "strategic_trends"
        SUPPORT_ANALYSIS = "support_analysis"

        # Alvaro's business charts
        ROI_ANALYSIS = "roi_analysis"
        INVESTMENT_TRACKING = "investment_tracking"
        BUSINESS_METRICS = "business_metrics"
        COST_ANALYSIS = "cost_analysis"

        # Martin's architecture charts
        ARCHITECTURE_HEALTH = "architecture_health"
        PERFORMANCE_METRICS_CHART = "performance_metrics"
        SYSTEM_DEPENDENCIES = "system_dependencies"

        # Camille's technology charts
        TECHNOLOGY_ROADMAP = "technology_roadmap"
        INNOVATION_METRICS = "innovation_metrics"

        # Rachel's design charts
        DESIGN_SYSTEM_HEALTH = "design_system_health"
        ADOPTION_METRICS = "adoption_metrics"

        # Default/fallback
        DEFAULT = "default"

    class Colors:
        """Rachel's executive color palette constants"""

        PRIMARY_BLUE = "#4dabf7"
        SUCCESS_GREEN = "#51cf66"
        ALERT_RED = "#ff6b6b"
        WARNING_YELLOW = "#ffd43b"
        PURPLE_ACCENT = "#9775fa"
        TEAL_ACCENT = "#20c997"

        # Executive color palette as list
        EXECUTIVE_PALETTE = [
            PRIMARY_BLUE,
            SUCCESS_GREEN,
            ALERT_RED,
            WARNING_YELLOW,
            PURPLE_ACCENT,
            TEAL_ACCENT,
        ]

        # Persona-specific title colors
        PERSONA_COLORS = {
            "diego": "#2c3e50",
            "alvaro": "#27ae60",
            "martin": "#8e44ad",
            "camille": "#e74c3c",
            "rachel": "#f39c12",
        }

    class Typography:
        """Typography and styling constants"""

        EXECUTIVE_FONT_FAMILY = "Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
        DEFAULT_FONT_SIZE = 12
        TITLE_FONT_SIZE = 24
        DEFAULT_FONT_COLOR = "#333"

    class Layout:
        """Layout and spacing constants"""

        # Plotly layout defaults
        PAPER_BGCOLOR = "rgba(0,0,0,0)"
        PLOT_BGCOLOR = "rgba(0,0,0,0)"

        # Margins
        DEFAULT_MARGIN_LEFT = 60
        DEFAULT_MARGIN_RIGHT = 60
        DEFAULT_MARGIN_TOP = 80
        DEFAULT_MARGIN_BOTTOM = 60

        # Chart dimensions
        DEFAULT_CHART_HEIGHT = 800
        DEFAULT_CHART_WIDTH = 1200

    class MetricsKeys:
        """Metrics tracking keys"""

        # Strategic Python metrics
        TOTAL_EXECUTIONS = "total_executions"
        SUCCESSFUL_EXECUTIONS = "successful_executions"
        AVG_EXECUTION_TIME = "avg_execution_time"
        SECURITY_VIOLATIONS = "security_violations"

        # Visualization metrics
        TOTAL_VISUALIZATIONS = "total_visualizations"
        SUCCESSFUL_GENERATIONS = "successful_generations"
        AVG_GENERATION_TIME = "avg_generation_time"
        AVG_FILE_SIZE = "avg_file_size"
        INTERACTIVE_FEATURES_USED = "interactive_features_used"

        # Integration metrics
        REQUESTS_PROCESSED = "requests_processed"
        SUCCESSFUL_REQUESTS = "successful_requests"
        AVG_RESPONSE_TIME = "avg_response_time"
        TRANSPARENCY_DISCLOSURES = "transparency_disclosures"

        # Workflow metrics
        TOTAL_WORKFLOWS = "total_workflows"
        SUCCESSFUL_WORKFLOWS = "successful_workflows"
        AVG_WORKFLOW_TIME = "avg_workflow_time"
        ANALYSIS_SUCCESS_RATE = "analysis_success_rate"
        VISUALIZATION_SUCCESS_RATE = "visualization_success_rate"

    class TransparencyMessages:
        """Transparency disclosure templates"""

        STRATEGIC_PYTHON_DISCLOSURE = """
🔧 Accessing MCP Server: strategic-python (Strategic Python MCP Server)
*Executing strategic analysis using {persona} persona...*

**Strategic Python Enhancement**:
- **Capability**: {capability}
- **Persona**: {persona} (Strategic Analysis)
- **Process**: {description}
- **Security**: Sandboxed execution with resource limits
- **Scope**: Strategic analysis only (no system operations)

**Execution Environment**: Secure Python sandbox with import restrictions
**Performance**: <30s execution time, 512MB memory limit
**Audit Trail**: Complete execution logging and transparency
"""

        EXECUTIVE_VISUALIZATION_DISCLOSURE = """
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

        INTEGRATED_WORKFLOW_DISCLOSURE = """
🔧 Accessing MCP Servers: strategic-python + executive-visualization (Integrated Workflow)
*Executing end-to-end strategic intelligence: data analysis → executive visualization...*

**Integrated Strategic Intelligence Workflow**:
- **Phase 1**: Strategic Python MCP Server (Data Analysis)
  - Persona: {persona} (Strategic Analysis)
  - Execution: {analysis_time:.2f}s
  - Status: {analysis_status}
  
- **Phase 2**: Executive Visualization System (Publication-Quality Charts)
  - Chart Type: {chart_type}
  - Generation: {viz_time:.2f}s
  - File Size: {file_size:,} bytes
  - Interactive Elements: {interactive_count}
  - Status: {viz_status}

**Workflow Steps**: {workflow_steps}
**Total Processing**: {total_time:.2f}s
**Security**: Sandboxed Python execution + Safe HTML generation
**Quality**: Executive-grade interactive visualizations with Rachel's design system
"""

    @classmethod
    def get_default_persona_config(cls, persona: str) -> Dict[str, Any]:
        """Get default configuration for a persona"""
        return {
            "focus": cls.Personas.PERSONA_FOCUS.get(persona, "strategic_analysis"),
            "default_imports": ["pandas", "numpy"],
            "template_vars": {
                "role": cls.Personas.PERSONA_TITLES.get(persona, "Strategic Analysis")
            },
        }

    @classmethod
    def get_executive_layout_template(cls) -> Dict[str, Any]:
        """Get executive layout template for Plotly charts"""
        return {
            "paper_bgcolor": cls.Layout.PAPER_BGCOLOR,
            "plot_bgcolor": cls.Layout.PLOT_BGCOLOR,
            "font": {
                "family": cls.Typography.EXECUTIVE_FONT_FAMILY,
                "size": cls.Typography.DEFAULT_FONT_SIZE,
                "color": cls.Typography.DEFAULT_FONT_COLOR,
            },
            "colorway": cls.Colors.EXECUTIVE_PALETTE,
            "margin": {
                "l": cls.Layout.DEFAULT_MARGIN_LEFT,
                "r": cls.Layout.DEFAULT_MARGIN_RIGHT,
                "t": cls.Layout.DEFAULT_MARGIN_TOP,
                "b": cls.Layout.DEFAULT_MARGIN_BOTTOM,
            },
        }

    @classmethod
    def get_security_config(cls) -> Dict[str, Any]:
        """Get complete security configuration"""
        return {
            cls.Security.MAX_EXECUTION_TIME_KEY: cls.Security.DEFAULT_MAX_EXECUTION_TIME,
            cls.Security.MAX_MEMORY_MB_KEY: cls.Security.DEFAULT_MAX_MEMORY_MB,
            cls.Security.ALLOWED_IMPORTS_KEY: cls.Security.ALLOWED_IMPORTS.copy(),
            cls.Security.BLOCKED_IMPORTS_KEY: cls.Security.BLOCKED_IMPORTS.copy(),
            cls.Security.BLOCKED_OPERATIONS_KEY: cls.Security.BLOCKED_OPERATIONS.copy(),
        }

    @classmethod
    def get_all_capabilities(cls) -> List[str]:
        """Get all MCP server capabilities"""
        return [
            # Strategic Python capabilities
            cls.Capabilities.STRATEGIC_DATA_ANALYSIS,
            cls.Capabilities.ROI_CALCULATIONS,
            cls.Capabilities.STAKEHOLDER_ANALYTICS,
            cls.Capabilities.PERFORMANCE_METRICS,
            cls.Capabilities.EXECUTIVE_REPORTING,
            # Executive Visualization capabilities
            cls.Capabilities.EXECUTIVE_DASHBOARDS,
            cls.Capabilities.INTERACTIVE_CHARTS,
            cls.Capabilities.STRATEGIC_PRESENTATIONS,
            cls.Capabilities.PUBLICATION_QUALITY_VISUALS,
            # Integrated Workflow capabilities
            cls.Capabilities.INTEGRATED_STRATEGIC_ANALYSIS,
            cls.Capabilities.DATA_DRIVEN_VISUALIZATIONS,
            cls.Capabilities.EXECUTIVE_READY_PRESENTATIONS,
            cls.Capabilities.END_TO_END_INTELLIGENCE,
        ]

    @classmethod
    def get_all_personas(cls) -> List[str]:
        """Get all supported personas"""
        return [
            cls.Personas.DIEGO,
            cls.Personas.ALVARO,
            cls.Personas.MARTIN,
            cls.Personas.CAMILLE,
            cls.Personas.RACHEL,
        ]

    @classmethod
    def get_all_chart_types(cls) -> List[str]:
        """Get all supported chart types"""
        return [
            cls.ChartTypes.LEADERSHIP_DASHBOARD,
            cls.ChartTypes.TEAM_METRICS,
            cls.ChartTypes.STRATEGIC_TRENDS,
            cls.ChartTypes.SUPPORT_ANALYSIS,
            cls.ChartTypes.ROI_ANALYSIS,
            cls.ChartTypes.INVESTMENT_TRACKING,
            cls.ChartTypes.BUSINESS_METRICS,
            cls.ChartTypes.COST_ANALYSIS,
            cls.ChartTypes.ARCHITECTURE_HEALTH,
            cls.ChartTypes.PERFORMANCE_METRICS_CHART,
            cls.ChartTypes.SYSTEM_DEPENDENCIES,
            cls.ChartTypes.TECHNOLOGY_ROADMAP,
            cls.ChartTypes.INNOVATION_METRICS,
            cls.ChartTypes.DESIGN_SYSTEM_HEALTH,
            cls.ChartTypes.ADOPTION_METRICS,
            cls.ChartTypes.DEFAULT,
        ]


# Convenience aliases for backward compatibility during refactoring
STRATEGIC_PYTHON_SERVER_NAME = MCPServerConstants.STRATEGIC_PYTHON_SERVER_NAME
EXECUTIVE_VISUALIZATION_SERVER_NAME = MCPServerConstants.EXECUTIVE_VISUALIZATION_SERVER_NAME

# Export main constants class
__all__ = ["MCPServerConstants"]
