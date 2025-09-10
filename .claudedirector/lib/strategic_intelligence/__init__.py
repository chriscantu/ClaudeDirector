"""
Strategic Analysis Module - Phase 5

External spec-kit integration with analytical enhancement layer.
Follows PROJECT_STRUCTURE.md architectural requirements.

Phase 5 Implementation - Q1 2025
Investment: $1.0M for 4.9x ROI
"""

# Core Strategic Analysis Components (Phase 5.0)
from .spec_kit_integrator import SpecKitIntegrator

# Strategic enhancement now provided by ai_intelligence.framework_processor

# Context intelligence now provided by context_engineering module
from .external_tool_coordinator import ExternalToolCoordinator
from .sequential_spec_workflow import SequentialSpecCreator, SequentialSpecWorkflow

# ML-Powered Decision Support Components temporarily disabled for P0 compatibility

__all__ = [
    "SpecKitIntegrator",
    "ExternalToolCoordinator",
    "SequentialSpecCreator",
    "SequentialSpecWorkflow",
]

# Version and metadata
__version__ = "5.0.0"
__phase__ = "Phase 5: Strategic AI Analysis Platform"
__architecture_compliance__ = "PROJECT_STRUCTURE.md v2.12.0+"
