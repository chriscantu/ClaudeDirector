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

# TS-4: Import unified response handler (eliminates duplicate SystematicResponse pattern)
from ..performance import (
    create_systematic_response,
    UnifiedResponse,
    ResponseStatus,
)


@dataclass
class FrameworkAnalysis:
    """Result of embedded framework analysis - BACKWARD COMPATIBILITY"""

    framework_name: str
    structured_insights: Dict[str, Any]
    recommendations: List[str]
    implementation_steps: List[str]
    key_considerations: List[str]
    analysis_confidence: float


# TS-4: SystematicResponse class ELIMINATED - replaced with UnifiedResponse
# This eliminates 25+ lines of duplicate response handling logic
# All SystematicResponse functionality now handled by create_systematic_response() from unified_response_handler
