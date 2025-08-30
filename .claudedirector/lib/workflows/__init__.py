"""
Strategic Workflow Management Module - Phase 14 Track 3

🎯 Diego | Engineering Leadership

Enterprise-grade strategic workflow automation with progress tracking,
template-driven processes, and cross-team coordination capabilities.

Architecture Integration:
- Extends existing context_engineering for workflow state persistence
- Integrates with advanced_personality_engine for persona-specific workflows
- Builds on performance optimization for <50ms workflow operations
- Maintains existing transparency and audit trail systems
"""

from .strategic_workflow_engine import (
    StrategicWorkflowEngine,
    WorkflowTemplate,
    WorkflowExecution,
    WorkflowStep,
    WorkflowStatus,
    ProgressMetrics,
    create_strategic_workflow_engine,
)

from .workflow_coordinator import (
    WorkflowCoordinator,
    CrossTeamWorkflow,
    CollaborationPattern,
    StakeholderAlignment,
)

__all__ = [
    "StrategicWorkflowEngine",
    "WorkflowTemplate",
    "WorkflowExecution",
    "WorkflowStep",
    "WorkflowStatus",
    "ProgressMetrics",
    "create_strategic_workflow_engine",
    "WorkflowCoordinator",
    "CrossTeamWorkflow",
    "CollaborationPattern",
    "StakeholderAlignment",
]
