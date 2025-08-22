"""
Framework Analysis Data Models
Core data structures for embedded framework engine.

Author: Martin (Principal Platform Architect)
Refactored from: embedded_framework_engine.py for better testability
"""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class FrameworkAnalysis:
    """Result of embedded framework analysis"""

    framework_name: str
    structured_insights: Dict[str, Any]
    recommendations: List[str]
    implementation_steps: List[str]
    key_considerations: List[str]
    analysis_confidence: float


@dataclass
class SystematicResponse:
    """Complete systematic analysis response"""

    analysis: FrameworkAnalysis
    persona_integrated_response: str
    processing_time_ms: int
    framework_applied: str
