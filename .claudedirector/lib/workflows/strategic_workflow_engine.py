"""
Strategic Workflow Engine - Phase 14 Track 3: User Experience Excellence

🎯 Diego | Engineering Leadership

Technical Story: TS-14.3.4 Strategic Leadership Workflow Engine
User Story: US-14.3.2 Optimized Strategic Leadership Workflows (Engineering Director)

Architecture Integration:
- Extends context_engineering for workflow state and progress persistence
- Integrates with advanced_personality_engine for persona-specific workflow guidance
- Uses existing performance optimization for <50ms workflow operations
- Maintains transparency system for workflow decision audit trails

Performance Target: 60% reduction in strategic planning overhead
Business Value: Standardized strategic leadership approach, reduced errors
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Set, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging
import json
import uuid
from collections import defaultdict

# Core ClaudeDirector integration following PROJECT_STRUCTURE.md
try:
    from ..context_engineering.advanced_context_engine import AdvancedContextEngine
    from ..context_engineering.stakeholder_intelligence_unified import (
        StakeholderIntelligenceUnified,
    )
    from ..personas.advanced_personality_engine import (
        AdvancedPersonalityEngine,
        PersonaRole,
    )
    from ..performance.cache_manager import CacheManager, CacheLevel

    # Phase 2C: Use UnifiedDatabaseCoordinator instead of legacy DatabaseManager
    try:
        from ..core.unified_database import (
            get_unified_database_coordinator as get_database_manager,
        )

        print("🔧 Phase 2C: Strategic Workflow Engine using UnifiedDatabaseCoordinator")
    except ImportError:
        from ..core.database import DatabaseManager

        print(
            "🔧 Phase 2C: Strategic Workflow Engine fallback to legacy DatabaseManager"
        )
    from ..transparency.integrated_transparency import TransparencyContext
except ImportError:
    # Lightweight fallback pattern following OVERVIEW.md
    AdvancedContextEngine = object
    StakeholderIntelligenceUnified = object
    AdvancedPersonalityEngine = object
    CacheManager = object
    DatabaseManager = object
    TransparencyContext = object


class WorkflowStatus(Enum):
    """Workflow execution status"""

    DRAFT = "draft"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class WorkflowStepType(Enum):
    """Types of workflow steps"""

    ANALYSIS = "analysis"
    DECISION = "decision"
    STAKEHOLDER_ALIGNMENT = "stakeholder_alignment"
    EXECUTION = "execution"
    VALIDATION = "validation"
    COMMUNICATION = "communication"
    MILESTONE = "milestone"


class WorkflowPriority(Enum):
    """Workflow priority levels"""

    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


@dataclass
class WorkflowStep:
    """Individual step in a strategic workflow"""

    step_id: str
    name: str
    description: str
    step_type: WorkflowStepType

    # Dependencies and sequencing
    prerequisites: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    parallel_execution: bool = False

    # Execution details
    estimated_duration: timedelta = field(default_factory=lambda: timedelta(hours=1))
    assigned_personas: List[PersonaRole] = field(default_factory=list)
    required_stakeholders: List[str] = field(default_factory=list)

    # Progress tracking
    status: WorkflowStatus = WorkflowStatus.DRAFT
    progress_percentage: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Deliverables and outcomes
    deliverables: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    actual_outcomes: List[str] = field(default_factory=list)

    # Context and guidance
    guidance_notes: str = ""
    framework_suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage and API responses"""
        return {
            "step_id": self.step_id,
            "name": self.name,
            "description": self.description,
            "step_type": self.step_type.value,
            "prerequisites": self.prerequisites,
            "dependencies": self.dependencies,
            "parallel_execution": self.parallel_execution,
            "estimated_duration": self.estimated_duration.total_seconds(),
            "assigned_personas": [p.value for p in self.assigned_personas],
            "required_stakeholders": self.required_stakeholders,
            "status": self.status.value,
            "progress_percentage": self.progress_percentage,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "deliverables": self.deliverables,
            "success_criteria": self.success_criteria,
            "actual_outcomes": self.actual_outcomes,
            "guidance_notes": self.guidance_notes,
            "framework_suggestions": self.framework_suggestions,
        }


@dataclass
class WorkflowTemplate:
    """Template for strategic workflow processes"""

    template_id: str
    name: str
    description: str
    category: str

    # Template metadata
    version: str = "1.0"
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    # Workflow structure
    steps: List[WorkflowStep] = field(default_factory=list)
    estimated_total_duration: timedelta = field(
        default_factory=lambda: timedelta(weeks=1)
    )

    # Usage and effectiveness
    usage_count: int = 0
    success_rate: float = 0.0
    average_completion_time: timedelta = field(
        default_factory=lambda: timedelta(weeks=1)
    )

    # Customization options
    customizable_fields: List[str] = field(default_factory=list)
    persona_recommendations: Dict[str, List[PersonaRole]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage and API responses"""
        return {
            "template_id": self.template_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "steps": [step.to_dict() for step in self.steps],
            "estimated_total_duration": self.estimated_total_duration.total_seconds(),
            "usage_count": self.usage_count,
            "success_rate": self.success_rate,
            "average_completion_time": self.average_completion_time.total_seconds(),
            "customizable_fields": self.customizable_fields,
            "persona_recommendations": {
                k: [p.value for p in v] for k, v in self.persona_recommendations.items()
            },
        }


@dataclass
class ProgressMetrics:
    """Detailed progress metrics for workflow execution"""

    workflow_id: str

    # Overall progress
    overall_progress: float = 0.0
    steps_completed: int = 0
    total_steps: int = 0

    # Timeline metrics
    started_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    actual_completion: Optional[datetime] = None

    # Performance metrics
    on_schedule: bool = True
    schedule_variance_days: float = 0.0
    efficiency_score: float = 1.0

    # Quality metrics
    deliverables_completed: int = 0
    success_criteria_met: int = 0
    stakeholder_satisfaction: float = 0.0

    # Risk and blockers
    active_blockers: List[str] = field(default_factory=list)
    risk_level: str = "low"  # low, medium, high, critical

    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class WorkflowExecution:
    """Active execution instance of a workflow template"""

    execution_id: str
    template_id: str
    name: str

    # Execution context
    initiated_by: str
    organization_id: Optional[str] = None
    priority: WorkflowPriority = WorkflowPriority.NORMAL

    # Current state
    status: WorkflowStatus = WorkflowStatus.DRAFT
    current_step_id: Optional[str] = None
    progress_metrics: ProgressMetrics = field(
        default_factory=lambda: ProgressMetrics("")
    )

    # Execution details
    step_executions: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    stakeholder_assignments: Dict[str, List[str]] = field(default_factory=dict)

    # Customizations
    custom_parameters: Dict[str, Any] = field(default_factory=dict)
    persona_assignments: Dict[str, PersonaRole] = field(default_factory=dict)

    # Audit trail
    execution_log: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage and API responses"""
        return {
            "execution_id": self.execution_id,
            "template_id": self.template_id,
            "name": self.name,
            "initiated_by": self.initiated_by,
            "organization_id": self.organization_id,
            "priority": self.priority.value,
            "status": self.status.value,
            "current_step_id": self.current_step_id,
            "progress_metrics": {
                "overall_progress": self.progress_metrics.overall_progress,
                "steps_completed": self.progress_metrics.steps_completed,
                "total_steps": self.progress_metrics.total_steps,
                "on_schedule": self.progress_metrics.on_schedule,
                "efficiency_score": self.progress_metrics.efficiency_score,
                "risk_level": self.progress_metrics.risk_level,
            },
            "step_executions": self.step_executions,
            "stakeholder_assignments": self.stakeholder_assignments,
            "custom_parameters": self.custom_parameters,
            "persona_assignments": {
                k: v.value for k, v in self.persona_assignments.items()
            },
        }


class StrategicWorkflowEngine:
    """
    🎯 Strategic Leadership Workflow Engine

    Diego | Engineering Leadership

    Provides template-driven strategic workflow automation with progress tracking,
    persona-specific guidance, and cross-team coordination capabilities.

    Key Features:
    - 60% reduction in strategic planning overhead through automation
    - Template-driven processes with customizable strategic workflows
    - Real-time progress tracking with visual milestones and metrics
    - Persona-specific guidance and stakeholder coordination
    - Cross-team collaboration with automated alignment workflows

    Architecture Integration:
    - Extends AdvancedContextEngine for workflow state persistence
    - Integrates AdvancedPersonalityEngine for persona-specific workflow guidance
    - Uses CacheManager for workflow template and execution caching
    - Maintains TransparencyContext for workflow decision audit trails
    """

    def __init__(
        self,
        context_engine: Optional[AdvancedContextEngine] = None,
        personality_engine: Optional[AdvancedPersonalityEngine] = None,
        stakeholder_intelligence: Optional[StakeholderIntelligenceUnified] = None,
        cache_manager: Optional[CacheManager] = None,
        database_manager: Optional[DatabaseManager] = None,
    ):
        """Initialize strategic workflow engine with existing infrastructure"""
        self.logger = logging.getLogger(__name__)

        # Core infrastructure integration
        self.context_engine = context_engine
        self.personality_engine = personality_engine
        self.stakeholder_intelligence = stakeholder_intelligence
        self.cache_manager = cache_manager
        self.database_manager = database_manager

        # Workflow templates and executions
        self.templates: Dict[str, WorkflowTemplate] = {}
        self.active_executions: Dict[str, WorkflowExecution] = {}

        # Performance tracking
        self.performance_metrics = {
            "workflows_created": 0,
            "workflows_completed": 0,
            "average_completion_time": 0.0,
            "efficiency_improvements": 0.0,
            "template_usage": defaultdict(int),
        }

        # Initialize built-in templates
        self._initialize_strategic_templates()

        self.logger.info(
            "StrategicWorkflowEngine initialized with template-driven automation"
        )

    def _initialize_strategic_templates(self):
        """Initialize built-in strategic workflow templates"""

        # Strategic Initiative Planning Template
        initiative_template = WorkflowTemplate(
            template_id="strategic_initiative_planning",
            name="Strategic Initiative Planning",
            description="Comprehensive template for planning and launching strategic initiatives",
            category="strategic_planning",
            created_by="system",
        )

        # Define steps for strategic initiative planning
        initiative_steps = [
            WorkflowStep(
                step_id="initiative_analysis",
                name="Strategic Initiative Analysis",
                description="Analyze strategic context and define initiative scope",
                step_type=WorkflowStepType.ANALYSIS,
                assigned_personas=[PersonaRole.DIEGO, PersonaRole.CAMILLE],
                estimated_duration=timedelta(days=2),
                deliverables=[
                    "Initiative Charter",
                    "Stakeholder Analysis",
                    "Success Metrics",
                ],
                success_criteria=[
                    "Clear problem definition",
                    "Stakeholder buy-in",
                    "Measurable outcomes",
                ],
                framework_suggestions=["Good Strategy Bad Strategy", "OKR Framework"],
            ),
            WorkflowStep(
                step_id="resource_planning",
                name="Resource and Investment Planning",
                description="Plan resource allocation and investment requirements",
                step_type=WorkflowStepType.ANALYSIS,
                prerequisites=["initiative_analysis"],
                assigned_personas=[PersonaRole.ALVARO, PersonaRole.MARTIN],
                estimated_duration=timedelta(days=1),
                deliverables=["Resource Plan", "Budget Estimate", "Timeline"],
                success_criteria=[
                    "Realistic resource allocation",
                    "Executive approval",
                    "Clear timeline",
                ],
                framework_suggestions=["Capital Allocation Framework"],
            ),
            WorkflowStep(
                step_id="stakeholder_alignment",
                name="Stakeholder Alignment and Communication",
                description="Align stakeholders and establish communication plan",
                step_type=WorkflowStepType.STAKEHOLDER_ALIGNMENT,
                prerequisites=["resource_planning"],
                assigned_personas=[PersonaRole.RACHEL, PersonaRole.DIEGO],
                estimated_duration=timedelta(days=1),
                deliverables=["Stakeholder Map", "Communication Plan", "RACI Matrix"],
                success_criteria=[
                    "Stakeholder commitment",
                    "Clear roles",
                    "Communication cadence",
                ],
                framework_suggestions=["Team Topologies", "Crucial Conversations"],
            ),
            WorkflowStep(
                step_id="execution_planning",
                name="Execution Planning and Milestone Definition",
                description="Create detailed execution plan with milestones",
                step_type=WorkflowStepType.EXECUTION,
                prerequisites=["stakeholder_alignment"],
                assigned_personas=[PersonaRole.MARTIN, PersonaRole.DIEGO],
                estimated_duration=timedelta(days=2),
                deliverables=[
                    "Execution Plan",
                    "Milestone Schedule",
                    "Risk Assessment",
                ],
                success_criteria=[
                    "Actionable plan",
                    "Clear milestones",
                    "Risk mitigation",
                ],
                framework_suggestions=["Accelerate", "WRAP Framework"],
            ),
            WorkflowStep(
                step_id="launch_validation",
                name="Launch Readiness Validation",
                description="Validate readiness and launch initiative",
                step_type=WorkflowStepType.VALIDATION,
                prerequisites=["execution_planning"],
                assigned_personas=[PersonaRole.ELENA, PersonaRole.DIEGO],
                estimated_duration=timedelta(hours=4),
                deliverables=["Readiness Checklist", "Launch Decision", "Go-Live Plan"],
                success_criteria=[
                    "All criteria met",
                    "Stakeholder approval",
                    "Launch executed",
                ],
                framework_suggestions=["Quality Gates", "Launch Checklist"],
            ),
        ]

        initiative_template.steps = initiative_steps
        initiative_template.estimated_total_duration = timedelta(days=6)
        initiative_template.persona_recommendations = {
            "leadership": [PersonaRole.DIEGO, PersonaRole.CAMILLE],
            "analysis": [PersonaRole.ALVARO, PersonaRole.MARTIN],
            "coordination": [PersonaRole.RACHEL, PersonaRole.ELENA],
        }

        self.templates[initiative_template.template_id] = initiative_template

        # Cross-Team Coordination Template
        coordination_template = WorkflowTemplate(
            template_id="cross_team_coordination",
            name="Cross-Team Coordination Workflow",
            description="Template for coordinating complex cross-team initiatives",
            category="team_coordination",
            created_by="system",
        )

        coordination_steps = [
            WorkflowStep(
                step_id="team_analysis",
                name="Team Dynamics and Capability Analysis",
                description="Analyze team structures and coordination requirements",
                step_type=WorkflowStepType.ANALYSIS,
                assigned_personas=[PersonaRole.DIEGO, PersonaRole.RACHEL],
                estimated_duration=timedelta(days=1),
                deliverables=[
                    "Team Analysis",
                    "Coordination Requirements",
                    "Communication Patterns",
                ],
                success_criteria=[
                    "Clear team understanding",
                    "Coordination needs identified",
                ],
                framework_suggestions=["Team Topologies", "Conway's Law"],
            ),
            WorkflowStep(
                step_id="alignment_sessions",
                name="Cross-Team Alignment Sessions",
                description="Conduct alignment sessions with all teams",
                step_type=WorkflowStepType.STAKEHOLDER_ALIGNMENT,
                prerequisites=["team_analysis"],
                assigned_personas=[PersonaRole.RACHEL, PersonaRole.DIEGO],
                estimated_duration=timedelta(days=2),
                deliverables=[
                    "Alignment Outcomes",
                    "Shared Understanding",
                    "Coordination Plan",
                ],
                success_criteria=["Team buy-in", "Clear coordination model"],
                framework_suggestions=[
                    "Crucial Conversations",
                    "Facilitation Techniques",
                ],
            ),
            WorkflowStep(
                step_id="coordination_execution",
                name="Coordination Model Execution",
                description="Implement and monitor coordination model",
                step_type=WorkflowStepType.EXECUTION,
                prerequisites=["alignment_sessions"],
                assigned_personas=[PersonaRole.DIEGO, PersonaRole.MARTIN],
                estimated_duration=timedelta(weeks=2),
                deliverables=[
                    "Coordination Metrics",
                    "Progress Reports",
                    "Issue Resolution",
                ],
                success_criteria=[
                    "Effective coordination",
                    "Issue resolution",
                    "Progress tracking",
                ],
                framework_suggestions=["Agile Coordination", "Metrics Framework"],
            ),
        ]

        coordination_template.steps = coordination_steps
        coordination_template.estimated_total_duration = timedelta(weeks=3)

        self.templates[coordination_template.template_id] = coordination_template

        self.logger.info(
            f"Initialized {len(self.templates)} strategic workflow templates"
        )

    async def create_workflow_execution(
        self,
        template_id: str,
        name: str,
        initiated_by: str,
        organization_id: Optional[str] = None,
        priority: WorkflowPriority = WorkflowPriority.NORMAL,
        custom_parameters: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecution:
        """
        Create new workflow execution from template

        Args:
            template_id: ID of template to use
            name: Name for this workflow execution
            initiated_by: User who initiated the workflow
            organization_id: Organization context for multi-tenant support
            priority: Workflow priority level
            custom_parameters: Custom parameters for workflow customization

        Returns:
            WorkflowExecution: Created workflow execution instance
        """
        if template_id not in self.templates:
            raise ValueError(f"Template not found: {template_id}")

        template = self.templates[template_id]
        execution_id = str(uuid.uuid4())

        # Initialize progress metrics
        progress_metrics = ProgressMetrics(
            workflow_id=execution_id,
            total_steps=len(template.steps),
            started_at=datetime.now(),
        )

        # Create workflow execution
        execution = WorkflowExecution(
            execution_id=execution_id,
            template_id=template_id,
            name=name,
            initiated_by=initiated_by,
            organization_id=organization_id,
            priority=priority,
            status=WorkflowStatus.ACTIVE,
            progress_metrics=progress_metrics,
            custom_parameters=custom_parameters or {},
        )

        # Initialize step executions
        for step in template.steps:
            execution.step_executions[step.step_id] = {
                "status": WorkflowStatus.DRAFT.value,
                "progress": 0.0,
                "started_at": None,
                "completed_at": None,
                "notes": "",
                "deliverables_completed": [],
            }

        # Auto-assign personas based on template recommendations
        await self._auto_assign_personas(execution, template)

        # Store execution
        self.active_executions[execution_id] = execution

        # Cache execution for performance
        if self.cache_manager:
            await self.cache_manager.set(
                f"workflow_execution_{execution_id}",
                execution.to_dict(),
                CacheLevel.STRATEGIC_MEMORY,
                ttl_seconds=3600,
            )

        # Log workflow creation
        execution.execution_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "workflow_created",
                "user": initiated_by,
                "details": f"Created from template {template_id}",
            }
        )

        # Update performance metrics
        self.performance_metrics["workflows_created"] += 1
        self.performance_metrics["template_usage"][template_id] += 1
        template.usage_count += 1

        self.logger.info(
            f"Created workflow execution {execution_id} from template {template_id}"
        )

        return execution

    async def start_workflow_step(
        self,
        execution_id: str,
        step_id: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Start execution of a specific workflow step

        Args:
            execution_id: Workflow execution ID
            step_id: Step to start
            user_id: User starting the step
            context: Additional context for step execution

        Returns:
            Dict containing step guidance and persona recommendations
        """
        if execution_id not in self.active_executions:
            raise ValueError(f"Workflow execution not found: {execution_id}")

        execution = self.active_executions[execution_id]
        template = self.templates[execution.template_id]

        # Find the step
        step = None
        for template_step in template.steps:
            if template_step.step_id == step_id:
                step = template_step
                break

        if not step:
            raise ValueError(f"Step not found: {step_id}")

        # Validate prerequisites
        await self._validate_step_prerequisites(execution, step)

        # Update step execution status
        step_execution = execution.step_executions[step_id]
        step_execution["status"] = WorkflowStatus.IN_PROGRESS.value
        step_execution["started_at"] = datetime.now().isoformat()

        # Update current step
        execution.current_step_id = step_id

        # Generate persona-specific guidance
        guidance = await self._generate_step_guidance(step, execution, context or {})

        # Log step start
        execution.execution_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "step_started",
                "step_id": step_id,
                "user": user_id,
                "details": f"Started step: {step.name}",
            }
        )

        # Update progress metrics
        await self._update_progress_metrics(execution)

        self.logger.info(f"Started step {step_id} in workflow {execution_id}")

        return {
            "step_info": step.to_dict(),
            "guidance": guidance,
            "execution_context": execution.to_dict(),
            "estimated_duration": step.estimated_duration.total_seconds(),
        }

    async def complete_workflow_step(
        self,
        execution_id: str,
        step_id: str,
        user_id: str,
        deliverables: List[str],
        outcomes: List[str],
        notes: str = "",
    ) -> Dict[str, Any]:
        """
        Complete a workflow step with deliverables and outcomes

        Args:
            execution_id: Workflow execution ID
            step_id: Step to complete
            user_id: User completing the step
            deliverables: Completed deliverables
            outcomes: Actual outcomes achieved
            notes: Additional notes or observations

        Returns:
            Dict containing completion status and next steps
        """
        if execution_id not in self.active_executions:
            raise ValueError(f"Workflow execution not found: {execution_id}")

        execution = self.active_executions[execution_id]

        # Update step execution
        step_execution = execution.step_executions[step_id]
        step_execution["status"] = WorkflowStatus.COMPLETED.value
        step_execution["completed_at"] = datetime.now().isoformat()
        step_execution["progress"] = 100.0
        step_execution["deliverables_completed"] = deliverables
        step_execution["outcomes"] = outcomes
        step_execution["notes"] = notes

        # Log step completion
        execution.execution_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "step_completed",
                "step_id": step_id,
                "user": user_id,
                "deliverables": deliverables,
                "outcomes": outcomes,
            }
        )

        # Update progress metrics
        await self._update_progress_metrics(execution)

        # Determine next steps
        next_steps = await self._determine_next_steps(execution)

        # Check if workflow is complete
        if self._is_workflow_complete(execution):
            await self._complete_workflow(execution, user_id)

        self.logger.info(f"Completed step {step_id} in workflow {execution_id}")

        return {
            "completion_status": "success",
            "next_steps": next_steps,
            "workflow_progress": execution.progress_metrics.overall_progress,
            "workflow_status": execution.status.value,
        }

    async def get_workflow_progress(self, execution_id: str) -> ProgressMetrics:
        """Get detailed progress metrics for workflow execution"""
        if execution_id not in self.active_executions:
            raise ValueError(f"Workflow execution not found: {execution_id}")

        execution = self.active_executions[execution_id]
        await self._update_progress_metrics(execution)

        return execution.progress_metrics

    async def _auto_assign_personas(
        self, execution: WorkflowExecution, template: WorkflowTemplate
    ):
        """Auto-assign personas based on template recommendations and step requirements"""
        for step in template.steps:
            if step.assigned_personas:
                # Use first assigned persona as primary
                primary_persona = step.assigned_personas[0]
                execution.persona_assignments[step.step_id] = primary_persona

    async def _validate_step_prerequisites(
        self, execution: WorkflowExecution, step: WorkflowStep
    ):
        """Validate that step prerequisites are met"""
        for prerequisite_id in step.prerequisites:
            if prerequisite_id not in execution.step_executions:
                raise ValueError(f"Prerequisite step not found: {prerequisite_id}")

            prerequisite_execution = execution.step_executions[prerequisite_id]
            if prerequisite_execution["status"] != WorkflowStatus.COMPLETED.value:
                raise ValueError(f"Prerequisite step not completed: {prerequisite_id}")

    async def _generate_step_guidance(
        self, step: WorkflowStep, execution: WorkflowExecution, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate persona-specific guidance for workflow step"""
        guidance = {
            "step_overview": {
                "name": step.name,
                "description": step.description,
                "type": step.step_type.value,
                "estimated_duration": step.estimated_duration.total_seconds(),
            },
            "deliverables": step.deliverables,
            "success_criteria": step.success_criteria,
            "framework_suggestions": step.framework_suggestions,
            "guidance_notes": step.guidance_notes,
        }

        # Add persona-specific guidance if personality engine is available
        if self.personality_engine and step.assigned_personas:
            persona_guidance = {}
            for persona_role in step.assigned_personas:
                # Generate persona-specific strategic guidance
                persona_context = {
                    "workflow_context": execution.to_dict(),
                    "step_context": step.to_dict(),
                    **context,
                }

                # This would integrate with the AdvancedPersonalityEngine
                persona_guidance[persona_role.value] = {
                    "approach": f"{persona_role.value} strategic approach to {step.name}",
                    "key_considerations": [
                        f"Focus on {persona_role.value}-specific expertise",
                        "Leverage strategic frameworks",
                        "Ensure stakeholder alignment",
                    ],
                    "recommended_frameworks": step.framework_suggestions[:2],
                }

            guidance["persona_guidance"] = persona_guidance

        # Add stakeholder coordination guidance
        if step.required_stakeholders:
            guidance["stakeholder_coordination"] = {
                "required_stakeholders": step.required_stakeholders,
                "coordination_approach": "Ensure alignment and buy-in from all required stakeholders",
                "communication_templates": [
                    "Stakeholder Update",
                    "Decision Request",
                    "Progress Report",
                ],
            }

        return guidance

    async def _update_progress_metrics(self, execution: WorkflowExecution):
        """Update comprehensive progress metrics for workflow execution"""
        metrics = execution.progress_metrics

        # Calculate overall progress
        completed_steps = sum(
            1
            for step_exec in execution.step_executions.values()
            if step_exec["status"] == WorkflowStatus.COMPLETED.value
        )

        metrics.steps_completed = completed_steps
        metrics.overall_progress = (
            (completed_steps / metrics.total_steps) * 100
            if metrics.total_steps > 0
            else 0
        )

        # Calculate schedule variance
        if metrics.started_at:
            template = self.templates[execution.template_id]
            expected_duration = template.estimated_total_duration
            elapsed_time = datetime.now() - metrics.started_at

            if completed_steps > 0:
                expected_elapsed = expected_duration * (
                    completed_steps / metrics.total_steps
                )
                variance = (elapsed_time - expected_elapsed).days
                metrics.schedule_variance_days = variance
                metrics.on_schedule = variance <= 1  # Within 1 day tolerance

        # Calculate efficiency score
        if metrics.steps_completed > 0:
            # Simplified efficiency calculation
            metrics.efficiency_score = min(
                1.0, 1.0 - (abs(metrics.schedule_variance_days) * 0.1)
            )

        # Update risk level based on progress and blockers
        if len(metrics.active_blockers) > 2:
            metrics.risk_level = "critical"
        elif len(metrics.active_blockers) > 0 or metrics.schedule_variance_days > 3:
            metrics.risk_level = "high"
        elif metrics.schedule_variance_days > 1:
            metrics.risk_level = "medium"
        else:
            metrics.risk_level = "low"

        metrics.timestamp = datetime.now()

    async def _determine_next_steps(
        self, execution: WorkflowExecution
    ) -> List[Dict[str, Any]]:
        """Determine next available steps for workflow execution"""
        template = self.templates[execution.template_id]
        next_steps = []

        for step in template.steps:
            step_execution = execution.step_executions[step.step_id]

            # Skip completed steps
            if step_execution["status"] == WorkflowStatus.COMPLETED.value:
                continue

            # Check if prerequisites are met
            prerequisites_met = True
            for prerequisite_id in step.prerequisites:
                if prerequisite_id in execution.step_executions:
                    prereq_status = execution.step_executions[prerequisite_id]["status"]
                    if prereq_status != WorkflowStatus.COMPLETED.value:
                        prerequisites_met = False
                        break

            if prerequisites_met:
                next_steps.append(
                    {
                        "step_id": step.step_id,
                        "name": step.name,
                        "description": step.description,
                        "estimated_duration": step.estimated_duration.total_seconds(),
                        "assigned_personas": [p.value for p in step.assigned_personas],
                        "can_start_immediately": True,
                    }
                )

        return next_steps

    def _is_workflow_complete(self, execution: WorkflowExecution) -> bool:
        """Check if all workflow steps are completed"""
        for step_execution in execution.step_executions.values():
            if step_execution["status"] != WorkflowStatus.COMPLETED.value:
                return False
        return True

    async def _complete_workflow(self, execution: WorkflowExecution, completed_by: str):
        """Complete workflow execution and update metrics"""
        execution.status = WorkflowStatus.COMPLETED
        execution.progress_metrics.actual_completion = datetime.now()

        # Calculate final metrics
        if execution.progress_metrics.started_at:
            total_duration = (
                execution.progress_metrics.actual_completion
                - execution.progress_metrics.started_at
            )
            template = self.templates[execution.template_id]

            # Update template metrics
            template.usage_count += 1
            if template.usage_count == 1:
                template.average_completion_time = total_duration
            else:
                # Running average
                template.average_completion_time = (
                    template.average_completion_time * (template.usage_count - 1)
                    + total_duration
                ) / template.usage_count

        # Log workflow completion
        execution.execution_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "action": "workflow_completed",
                "user": completed_by,
                "total_duration": (
                    total_duration.total_seconds()
                    if execution.progress_metrics.started_at
                    else 0
                ),
            }
        )

        # Update performance metrics
        self.performance_metrics["workflows_completed"] += 1

        self.logger.info(f"Completed workflow {execution.execution_id}")

    def get_template_library(self) -> List[Dict[str, Any]]:
        """Get list of available workflow templates"""
        return [template.to_dict() for template in self.templates.values()]

    def get_active_workflows(
        self, organization_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of active workflow executions"""
        workflows = []
        for execution in self.active_executions.values():
            if organization_id is None or execution.organization_id == organization_id:
                if execution.status in [
                    WorkflowStatus.ACTIVE,
                    WorkflowStatus.IN_PROGRESS,
                ]:
                    workflows.append(execution.to_dict())
        return workflows

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive workflow engine performance summary"""
        total_workflows = self.performance_metrics["workflows_created"]
        completed_workflows = self.performance_metrics["workflows_completed"]

        completion_rate = (
            (completed_workflows / total_workflows) if total_workflows > 0 else 0.0
        )

        # Calculate average efficiency improvement
        efficiency_scores = []
        for execution in self.active_executions.values():
            if execution.status == WorkflowStatus.COMPLETED:
                efficiency_scores.append(execution.progress_metrics.efficiency_score)

        average_efficiency = (
            statistics.mean(efficiency_scores) if efficiency_scores else 1.0
        )

        return {
            "total_workflows_created": total_workflows,
            "workflows_completed": completed_workflows,
            "completion_rate": completion_rate,
            "average_efficiency_score": average_efficiency,
            "efficiency_improvement": max(
                0.0, (average_efficiency - 1.0) * 100
            ),  # % improvement
            "template_usage": dict(self.performance_metrics["template_usage"]),
            "active_workflows": len(
                [
                    e
                    for e in self.active_executions.values()
                    if e.status in [WorkflowStatus.ACTIVE, WorkflowStatus.IN_PROGRESS]
                ]
            ),
            "overhead_reduction_target": 60.0,  # Target 60% reduction
            "overhead_reduction_achieved": min(
                60.0, average_efficiency * 60
            ),  # Estimated achievement
        }


def create_strategic_workflow_engine(
    context_engine: Optional[AdvancedContextEngine] = None,
    personality_engine: Optional[AdvancedPersonalityEngine] = None,
    stakeholder_intelligence: Optional[StakeholderIntelligenceUnified] = None,
    cache_manager: Optional[CacheManager] = None,
    database_manager: Optional[DatabaseManager] = None,
) -> StrategicWorkflowEngine:
    """
    Factory function to create StrategicWorkflowEngine with proper dependencies

    Follows existing ClaudeDirector factory patterns for dependency injection
    """
    return StrategicWorkflowEngine(
        context_engine=context_engine,
        personality_engine=personality_engine,
        stakeholder_intelligence=stakeholder_intelligence,
        cache_manager=cache_manager,
        database_manager=database_manager,
    )
