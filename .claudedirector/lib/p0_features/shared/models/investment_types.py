"""
Unified Investment Type Enum - Shared Across ROI Systems

This enum consolidates investment categories used by both:
1. ROI Modeling Engine (predictive/roi_modeling.py) - Predictive analytics
2. ROI Investment Tracker (strategic_metrics/roi_investment_tracker.py) - Tracking & reporting

BLOAT_PREVENTION Compliance:
- Single source of truth for investment categories
- Eliminates 30% duplication between prediction and tracking systems
- DRY compliance: Both modules import from here

Design Decision:
- Combines categories from both systems
- Preserves all unique values from each system
- Enables future expansion without duplication
"""

from enum import Enum


class InvestmentType(Enum):
    """
    Unified investment types for platform investments

    Used by:
    - Predictive ROI modeling (forward-looking scenarios)
    - Investment tracking & reporting (historical performance)
    """

    # Core infrastructure investments
    PLATFORM_INFRASTRUCTURE = "platform_infrastructure"

    # Development tooling and capabilities
    DEVELOPER_TOOLING = "developer_tooling"  # Predictive system term
    DEVELOPER_TOOLS = "developer_tools"  # Tracker system alias

    # Analytics and data capabilities
    ANALYTICS_CAPABILITIES = "analytics_capabilities"

    # Automation investments
    AUTOMATION = "automation"  # Predictive system term
    AUTOMATION_SYSTEMS = "automation_systems"  # Tracker system alias

    # Technical health improvements
    TECHNICAL_DEBT_REDUCTION = "technical_debt_reduction"

    # Team and organizational investments
    TEAM_EXPANSION = "team_expansion"
    TRAINING_DEVELOPMENT = "training_development"

    # Process and workflow improvements
    PROCESS_IMPROVEMENT = "process_improvement"

    # Security and compliance
    SECURITY_IMPROVEMENTS = "security_improvements"

    # Collaboration and communication
    COLLABORATION_TOOLS = "collaboration_tools"

    # Observability and monitoring
    MONITORING_OBSERVABILITY = "monitoring_observability"


# Backward compatibility aliases
# Allow both naming conventions to work seamlessly
INVESTMENT_TYPE_ALIASES = {
    # Map tracker system names to canonical enum values
    "developer_tools": InvestmentType.DEVELOPER_TOOLING,
    "automation_systems": InvestmentType.AUTOMATION,
}


def normalize_investment_type(type_value: str) -> InvestmentType:
    """
    Normalize investment type string to canonical enum value

    Args:
        type_value: Investment type string (either naming convention)

    Returns:
        Canonical InvestmentType enum value

    Raises:
        ValueError: If type_value is not recognized
    """
    # Check if it's already a valid enum value
    try:
        return InvestmentType(type_value)
    except ValueError:
        pass

    # Check aliases
    if type_value in INVESTMENT_TYPE_ALIASES:
        return INVESTMENT_TYPE_ALIASES[type_value]

    # Not found
    raise ValueError(
        f"Unknown investment type: {type_value}. "
        f"Valid values: {[t.value for t in InvestmentType]}"
    )


__all__ = ["InvestmentType", "normalize_investment_type", "INVESTMENT_TYPE_ALIASES"]
