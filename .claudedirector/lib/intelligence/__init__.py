"""
Intelligence modules for ClaudeDirector
AI-powered stakeholder detection, task extraction, and meeting intelligence

INTEGRATION NOTICE: Intelligence modules now integrate with Context Engineering
for enhanced capabilities. See context_engineering_integration.py for details.
"""

from .meeting import MeetingIntelligence
from .stakeholder import StakeholderIntelligence
from .task import TaskIntelligence

# Import unified bridge system (replaces context_engineering_integration)
try:
    from ..integration.unified_bridge import create_intelligence_bridge

    UNIFIED_BRIDGE_AVAILABLE = True
except ImportError:
    UNIFIED_BRIDGE_AVAILABLE = False

    def create_intelligence_bridge(*args, **kwargs):
        raise ImportError("Unified bridge system not available")


__all__ = [
    "StakeholderIntelligence",
    "TaskIntelligence",
    "MeetingIntelligence",
    "create_intelligence_bridge",  # Now from unified bridge
]
