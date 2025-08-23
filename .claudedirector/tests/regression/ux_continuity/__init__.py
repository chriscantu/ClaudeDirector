"""
UX Continuity Regression Tests

Rachel's comprehensive test suite for user experience continuity
that ensures consistent, reliable, and trustworthy interactions
across all strategic intelligence workflows.

Test Categories:
- Persona Consistency: Behavior and communication style consistency
- Context Switching: Smooth transitions between topics and personas
- Error Recovery: Graceful error handling and user trust preservation
- Cross-Environment: Consistent experience across platforms

UX IMPACT: Failures in these areas lead to:
- User confusion and reduced trust
- Fragmented strategic intelligence experience
- Increased learning curve and reduced adoption
- Poor error experiences that destroy confidence
"""

from .test_persona_consistency import TestPersonaConsistency
from .test_context_switching import TestContextSwitching
from .test_error_recovery import TestErrorRecovery
from .test_cross_environment import TestCrossEnvironmentConsistency

__all__ = [
    "TestPersonaConsistency",
    "TestContextSwitching",
    "TestErrorRecovery",
    "TestCrossEnvironmentConsistency",
]
