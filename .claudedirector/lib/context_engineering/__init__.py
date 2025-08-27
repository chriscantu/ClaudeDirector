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
from .ml_pattern_engine import (
    MLPatternEngine,
    TeamFeatureExtractor,
    CollaborationClassifier,
    FeatureVector,
    CollaborationPrediction,
    SuccessPattern,
    TeamCollaborationOutcome,
    CollaborationOutcome,
    FeatureType,
    # CollaborationScorer - Epic 2 Completion Components
    CollaborationScorer,
    EnsembleModelConfig,
    RiskAssessment,
    RiskAssessmentEngine,
    AdvancedCollaborationPrediction,
)

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
