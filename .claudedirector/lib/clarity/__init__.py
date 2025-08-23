"""
Next Action Clarity Framework

Core module for tracking and measuring strategic conversation effectiveness.
Implements the Next Action Clarity Rate metric as defined in PRD.
"""

from .conversation_analyzer import ConversationFlowAnalyzer
from .action_detector import ActionDetectionEngine
from .clarity_metrics import ClarityMeasurementSystem
from .models import (
    ClarityMetrics,
    ActionItem,
    ActionType,
    ClarityReport,
    Conversation,
    ConversationMessage,
    ClarityIndicator,
    StuckPattern,
)

__version__ = "1.0.0"
__all__ = [
    "ConversationFlowAnalyzer",
    "ActionDetectionEngine",
    "ClarityMeasurementSystem",
    "ClarityMetrics",
    "ActionItem",
    "ActionType",
    "ClarityReport",
    "Conversation",
    "ConversationMessage",
    "ClarityIndicator",
    "StuckPattern",
]
