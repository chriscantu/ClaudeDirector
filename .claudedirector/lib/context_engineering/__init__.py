"""
Context Engineering Module

Multi-layered strategic memory architecture for ClaudeDirector.
Provides persistent strategic intelligence across sessions.

Priority 1 Implementation - Q1 2025
Investment: $380K for 3.2x ROI
"""

from .advanced_context_engine import AdvancedContextEngine
from .conversation_layer import ConversationLayerMemory
from .strategic_layer import StrategicLayerMemory
from .stakeholder_layer import StakeholderLayerMemory
from .learning_layer import LearningLayerMemory
from .organizational_layer import OrganizationalLayerMemory
from .context_orchestrator import ContextOrchestrator
from .clarity_analyzer import (
    ClarityAnalyzer,
    ActionDetectionEngine,
    ClarityMetricsEngine,
    ConversationAnalyzer,
    ActionItem,
    ActionType,
    ClarityMetrics,
    ClarityIndicator,
    ConversationAnalysis,
    get_clarity_analyzer,
)
from .realtime_monitor import (
    RealTimeMonitor,
    EventProcessor,
    AlertEngine,
    TeamDataCollector,
    RealTimeBottleneckDetector,
    TeamEvent,
    Alert,
    EventType,
    AlertSeverity,
)

# Optional ML Pattern Engine import for P0 compatibility
try:
    # Import types first (Phase 3A.1.2 - SOLID compliance)
    from .ml_pattern_types import (
        FeatureVector,
        CollaborationPrediction,
        SuccessPattern,
        TeamCollaborationOutcome,
        CollaborationOutcome,
        FeatureType,
        EnsembleModelConfig,
        RiskAssessment,
        AdvancedCollaborationPrediction,
    )

    # Import implementation classes
    from .ml_pattern_engine import (
        MLPatternEngine,
        TeamFeatureExtractor,
        CollaborationClassifier,
        CollaborationScorer,
        RiskAssessmentEngine,
    )

    ML_PATTERN_ENGINE_AVAILABLE = True
except (ImportError, TypeError, AttributeError) as e:
    # Fallback for P0 compatibility when heavyweight dependencies unavailable
    ML_PATTERN_ENGINE_AVAILABLE = False

    # Minimal stubs for compatibility
    class MLPatternEngine:
        def __init__(self, *args, **kwargs):
            pass

    class TeamFeatureExtractor:
        def __init__(self, *args, **kwargs):
            pass

    class CollaborationClassifier:
        def __init__(self, *args, **kwargs):
            pass

    FeatureVector = dict
    CollaborationPrediction = dict
    SuccessPattern = dict
    TeamCollaborationOutcome = dict
    CollaborationOutcome = dict
    FeatureType = str

    class CollaborationScorer:
        def __init__(self, *args, **kwargs):
            pass

    EnsembleModelConfig = dict
    RiskAssessment = dict

    class RiskAssessmentEngine:
        def __init__(self, *args, **kwargs):
            pass

    AdvancedCollaborationPrediction = dict

from .strategic_layer import InitiativeStatus
from .stakeholder_layer import StakeholderRole, CommunicationStyle
from .learning_layer import FrameworkUsage, DecisionPattern
from .organizational_layer import (
    TeamStructure,
    OrganizationalChange,
    OrganizationSize,
    CulturalDimension,
)
from .context_orchestrator import ContextPriority

__all__ = [
    "AdvancedContextEngine",
    "ConversationLayerMemory",
    "StrategicLayerMemory",
    "StakeholderLayerMemory",
    "LearningLayerMemory",
    "OrganizationalLayerMemory",
    "ContextOrchestrator",
    "ClarityAnalyzer",
    "ActionDetectionEngine",
    "ClarityMetricsEngine",
    "ConversationAnalyzer",
    "ActionItem",
    "ActionType",
    "ClarityMetrics",
    "ClarityIndicator",
    "ConversationAnalysis",
    "get_clarity_analyzer",
    "RealTimeMonitor",
    "EventProcessor",
    "AlertEngine",
    "TeamDataCollector",
    "RealTimeBottleneckDetector",
    "TeamEvent",
    "Alert",
    "EventType",
    "AlertSeverity",
    "MLPatternEngine",
    "TeamFeatureExtractor",
    "CollaborationClassifier",
    "FeatureVector",
    "CollaborationPrediction",
    "SuccessPattern",
    "TeamCollaborationOutcome",
    "CollaborationOutcome",
    "FeatureType",
    # CollaborationScorer - Epic 2 Completion Components
    "CollaborationScorer",
    "EnsembleModelConfig",
    "RiskAssessment",
    "RiskAssessmentEngine",
    "AdvancedCollaborationPrediction",
    "InitiativeStatus",
    "StakeholderRole",
    "CommunicationStyle",
    "FrameworkUsage",
    "DecisionPattern",
    "TeamStructure",
    "OrganizationalChange",
    "OrganizationSize",
    "CulturalDimension",
    "ContextPriority",
]

__version__ = "1.0.0"
__priority__ = "P1-BLOCKING"
