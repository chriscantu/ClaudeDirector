"""
Framework Engine Types - Shared Data Classes
============================================

Shared data classes for framework analysis to avoid circular imports.
These classes are used by both the legacy and refactored framework engines.

Author: Martin | Platform Architecture
Purpose: Eliminate circular import issues in framework engine
"""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class FrameworkAnalysis:
    """Result of embedded framework analysis - BACKWARD COMPATIBILITY"""

    framework_name: str
    structured_insights: Dict[str, Any]
    recommendations: List[str]
    implementation_steps: List[str]
    key_considerations: List[str]
    analysis_confidence: float


@dataclass
class SystematicResponse:
    """Complete systematic analysis response - BACKWARD COMPATIBILITY"""

    analysis: FrameworkAnalysis
    persona_integrated_response: str
    processing_time_ms: int
    framework_applied: str
