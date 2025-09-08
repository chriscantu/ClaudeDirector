"""
Strategic Analysis Module - Phase 5

External spec-kit integration with analytical enhancement layer.
Follows PROJECT_STRUCTURE.md architectural requirements.

Phase 5 Implementation - Q1 2025
Investment: $1.0M for 4.9x ROI
"""

# Core Strategic Analysis Components (Phase 5.0)
from .spec_kit_integrator import SpecKitIntegrator
from .strategic_spec_enhancer import StrategicSpecEnhancer
from .context_intelligence_bridge import ContextIntelligenceBridge
from .external_tool_coordinator import ExternalToolCoordinator
from .sequential_spec_workflow import SequentialSpecCreator, SequentialSpecWorkflow

# Phase 5.1 ML-Powered Decision Support Components
from .ml_sequential_workflow import (
    MLSequentialThinkingWorkflow,
    MLSequentialWorkflow,
    SequentialMLAnalysisStep,
    create_ml_sequential_workflow,
)

# Future Phase 5.2+ Components (not yet implemented)
# from .predictive_analytics_engine import PredictiveAnalyticsEngine
# from .strategic_framework_synthesizer import StrategicFrameworkSynthesizer

__all__ = [
    "SpecKitIntegrator",
    "StrategicSpecEnhancer",
    "ContextIntelligenceBridge",
    "ExternalToolCoordinator",
    "SequentialSpecCreator",
    "SequentialSpecWorkflow",
    # Phase 5.1 ML-Powered Decision Support
    "MLSequentialThinkingWorkflow",
    "MLSequentialWorkflow",
    "SequentialMLAnalysisStep",
    "create_ml_sequential_workflow",
    # Future components will be added in Phase 5.2+
    # "PredictiveAnalyticsEngine",
    # "StrategicFrameworkSynthesizer",
]

# Version and metadata
__version__ = "5.0.0"
__phase__ = "Phase 5: Strategic AI Analysis Platform"
__architecture_compliance__ = "PROJECT_STRUCTURE.md v2.12.0+"
