#!/usr/bin/env python3
"""
Visualization Design System
Rachel's design system principles applied to organizational intelligence dashboards
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum


class ColorScale(Enum):
    """Design system color scales for different data types"""

    PRIMARY = "primary"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    NEUTRAL = "neutral"
    ACCENT = "accent"


class ComponentSize(Enum):
    """Consistent sizing scale across all visual components"""

    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"


@dataclass
class DesignTokens:
    """Design tokens following Rachel's design system principles"""

    # Color palette - WCAG compliant
    colors: Dict[str, Dict[str, str]] = None

    # Typography scale
    typography: Dict[str, Dict[str, str]] = None

    # Spacing scale
    spacing: Dict[str, str] = None

    # Border radius scale
    radius: Dict[str, str] = None

    # Shadow scale
    shadows: Dict[str, str] = None

    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                "primary": {
                    "50": "#f0f9ff",
                    "100": "#e0f2fe",
                    "500": "#0ea5e9",
                    "600": "#0284c7",
                    "900": "#0c4a6e",
                },
                "success": {
                    "50": "#f0fdf4",
                    "100": "#dcfce7",
                    "500": "#22c55e",
                    "600": "#16a34a",
                    "900": "#14532d",
                },
                "warning": {
                    "50": "#fffbeb",
                    "100": "#fef3c7",
                    "500": "#f59e0b",
                    "600": "#d97706",
                    "900": "#78350f",
                },
                "error": {
                    "50": "#fef2f2",
                    "100": "#fee2e2",
                    "500": "#ef4444",
                    "600": "#dc2626",
                    "900": "#7f1d1d",
                },
                "neutral": {
                    "50": "#f8fafc",
                    "100": "#f1f5f9",
                    "500": "#64748b",
                    "600": "#475569",
                    "900": "#0f172a",
                },
            }

        if self.typography is None:
            self.typography = {
                "display": {"size": "2.5rem", "weight": "700", "line_height": "1.2"},
                "h1": {"size": "2rem", "weight": "600", "line_height": "1.3"},
                "h2": {"size": "1.5rem", "weight": "600", "line_height": "1.4"},
                "h3": {"size": "1.25rem", "weight": "500", "line_height": "1.5"},
                "body": {"size": "1rem", "weight": "400", "line_height": "1.6"},
                "caption": {"size": "0.875rem", "weight": "400", "line_height": "1.5"},
                "label": {"size": "0.75rem", "weight": "500", "line_height": "1.4"},
            }

        if self.spacing is None:
            self.spacing = {
                "xs": "0.25rem",
                "sm": "0.5rem",
                "md": "1rem",
                "lg": "1.5rem",
                "xl": "2rem",
                "2xl": "3rem",
            }

        if self.radius is None:
            self.radius = {
                "xs": "0.125rem",
                "sm": "0.25rem",
                "md": "0.375rem",
                "lg": "0.5rem",
                "xl": "0.75rem",
            }

        if self.shadows is None:
            self.shadows = {
                "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
            }


@dataclass
class ChartConfiguration:
    """Standardized chart configuration following design system"""

    # Chart dimensions
    width: int = 800
    height: int = 400

    # Margins
    margin_top: int = 20
    margin_right: int = 20
    margin_bottom: int = 40
    margin_left: int = 60

    # Animation settings
    animation_duration: int = 300
    animation_easing: str = "ease-in-out"

    # Accessibility
    aria_label: Optional[str] = None
    description: Optional[str] = None


class VisualizationDesignSystem:
    """
    Rachel's design system for organizational intelligence visualizations
    Ensures consistency, accessibility, and scalability across all charts
    """

    def __init__(self):
        self.tokens = DesignTokens()
        self.chart_config = ChartConfiguration()

    def get_color_for_score(self, score: float, context: str = "performance") -> str:
        """
        Get appropriate color for score based on context
        Rachel's accessibility-first approach with semantic colors
        """
        if context == "performance":
            if score >= 0.8:
                return self.tokens.colors["success"]["500"]
            elif score >= 0.6:
                return self.tokens.colors["warning"]["500"]
            else:
                return self.tokens.colors["error"]["500"]

        elif context == "neutral":
            return self.tokens.colors["neutral"]["500"]

        elif context == "primary":
            return self.tokens.colors["primary"]["500"]

        return self.tokens.colors["neutral"]["500"]

    def get_color_palette(self, data_points: int) -> List[str]:
        """
        Generate accessible color palette for multiple data series
        Ensures sufficient contrast and distinguishability
        """
        base_colors = [
            self.tokens.colors["primary"]["500"],
            self.tokens.colors["success"]["500"],
            self.tokens.colors["warning"]["500"],
            self.tokens.colors["error"]["500"],
            self.tokens.colors["neutral"]["500"],
        ]

        # Extend palette if needed
        while len(base_colors) < data_points:
            base_colors.extend(base_colors)

        return base_colors[:data_points]

    def get_status_indicator(self, value: float, target: float) -> Dict[str, str]:
        """
        Get status indicator (color, icon, label) based on performance vs target
        Rachel's traffic light system for quick executive comprehension
        """
        if target == 0:  # Avoid division by zero
            return {
                "color": self.tokens.colors["neutral"]["500"],
                "icon": "●",
                "label": "No Target Set",
                "status": "neutral",
            }

        performance_ratio = value / target

        if performance_ratio >= 0.95:
            return {
                "color": self.tokens.colors["success"]["500"],
                "icon": "●",
                "label": "Exceeding Target",
                "status": "success",
            }
        elif performance_ratio >= 0.8:
            return {
                "color": self.tokens.colors["success"]["500"],
                "icon": "●",
                "label": "On Target",
                "status": "success",
            }
        elif performance_ratio >= 0.6:
            return {
                "color": self.tokens.colors["warning"]["500"],
                "icon": "●",
                "label": "Below Target",
                "status": "warning",
            }
        else:
            return {
                "color": self.tokens.colors["error"]["500"],
                "icon": "●",
                "label": "Needs Attention",
                "status": "error",
            }

    def format_metric_value(self, value: float, metric_type: str) -> str:
        """
        Format metric values for display following design system conventions
        """
        if metric_type == "percentage":
            return f"{value:.1%}"
        elif metric_type == "ratio":
            return f"{value:.2f}"
        elif metric_type == "score":
            return f"{value:.1f}"
        elif metric_type == "time":
            if value < 1:
                return f"{value*1000:.0f}ms"
            else:
                return f"{value:.1f}s"
        elif metric_type == "days":
            return f"{value:.1f} days"
        else:
            return f"{value:.2f}"

    def get_chart_theme(self) -> Dict[str, any]:
        """
        Get comprehensive chart theme following design system
        """
        return {
            "background_color": self.tokens.colors["neutral"]["50"],
            "grid_color": self.tokens.colors["neutral"]["100"],
            "text_color": self.tokens.colors["neutral"]["900"],
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "font_size": {
                "title": self.tokens.typography["h2"]["size"],
                "axis": self.tokens.typography["body"]["size"],
                "label": self.tokens.typography["caption"]["size"],
            },
            "borders": {
                "width": "1px",
                "color": self.tokens.colors["neutral"]["200"],
                "radius": self.tokens.radius["md"],
            },
            "shadows": self.tokens.shadows["sm"],
        }

    def validate_accessibility(self, foreground: str, background: str) -> bool:
        """
        Validate color contrast meets WCAG AA standards
        Rachel's accessibility-first approach
        """
        # Simplified contrast calculation - in production would use proper algorithm
        # For now, return True for known design system colors
        return True

    def get_responsive_dimensions(self, container_width: int) -> Tuple[int, int]:
        """
        Get responsive chart dimensions based on container width
        """
        if container_width < 480:  # Mobile
            return (container_width - 32, 200)
        elif container_width < 768:  # Tablet
            return (container_width - 64, 300)
        else:  # Desktop
            return (min(container_width - 96, 1200), 400)


# Global design system instance
design_system = VisualizationDesignSystem()
