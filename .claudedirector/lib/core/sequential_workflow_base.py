#!/usr/bin/env python3
"""
🧠 Base Sequential Thinking Workflow
Consolidated implementation eliminating duplication across phases

ELIMINATION ACHIEVED:
- Consolidated phase93_sequential_thinking_workflow.py (766 lines)
- Consolidated ml_sequential_workflow.py (741+ lines)
- Consolidated sequential_spec_workflow.py patterns
- Single source of truth for Sequential Thinking methodology

Author: Martin | Platform Architecture - DRY Consolidation
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Protocol
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

# Import existing infrastructure (leverage, don't duplicate)
try:
    from .base_processor import BaseProcessor, BaseProcessorConfig
    from .constants import ML_CONFIG, SYSTEM
except ImportError:
    # Graceful fallback for test environments
    BaseProcessor = None
    BaseProcessorConfig = None
    ML_CONFIG = None
    SYSTEM = None

logger = logging.getLogger(__name__)


class SequentialPhase(Enum):
    """Universal Sequential Thinking phases"""

    PROBLEM_ANALYSIS = "problem_analysis"
    SYSTEMATIC_APPROACH = "systematic_approach"
    IMPLEMENTATION_STRATEGY = "implementation_strategy"
    VALIDATION_PLAN = "validation_plan"
    STRATEGIC_ENHANCEMENT = "strategic_enhancement"
    SUCCESS_METRICS = "success_metrics"


@dataclass
class SequentialStep:
    """Universal Sequential Thinking step"""

    phase: SequentialPhase
    description: str
    started: bool = False
    completed: bool = False
    results: Optional[Dict[str, Any]] = None
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None


@dataclass
class SequentialWorkflow:
    """Universal Sequential Thinking workflow result"""

    phase_name: str
    user_stories: List[str] = field(default_factory=list)
    sequential_steps: List[SequentialStep] = field(default_factory=list)
    success: bool = False
    total_time: float = 0.0
    results: Dict[str, Any] = field(default_factory=dict)


class BaseSequentialWorkflow(ABC):
    """
    🧠 Base Sequential Thinking Workflow

    Eliminates duplication across all phase-specific sequential implementations.
    Provides common methodology while allowing phase-specific customization.
    """

    def __init__(self, phase_name: str, user_stories: List[str]):
        """Initialize base sequential workflow"""
        self.phase_name = phase_name
        self.user_stories = user_stories
        self.logger = logger

        # Common configuration
        self.workflow_config = {
            "phase": phase_name,
            "methodology": "Sequential Thinking",
            "architectural_compliance_required": True,
            "p0_test_protection": True,
        }

        self.logger.info(
            f"Sequential Thinking {phase_name} workflow initialized",
            user_stories=len(user_stories),
        )

    async def execute_workflow(
        self, context: Optional[Dict[str, Any]] = None
    ) -> SequentialWorkflow:
        """Execute complete Sequential Thinking workflow"""
        workflow_start_time = time.time()

        # Initialize workflow tracking
        sequential_steps = self._initialize_steps()
        workflow = SequentialWorkflow(
            phase_name=self.phase_name,
            user_stories=self.user_stories,
            sequential_steps=sequential_steps,
        )

        try:
            # Execute all 6 sequential steps
            for i, step in enumerate(sequential_steps):
                self.logger.info(
                    f"🧠 Sequential Thinking Step {i+1}: {step.description}"
                )
                step.started = True
                step.start_time = datetime.now()

                # Call phase-specific implementation
                step_result = await self._execute_step(
                    step.phase, context, workflow.results
                )

                step.completed = True
                step.results = step_result
                step.completion_time = datetime.now()

                # Update workflow results
                workflow.results[step.phase.value] = step_result

                self.logger.info(f"✅ Step {i+1} completed: {step.phase.value}")

            workflow.success = True
            workflow.total_time = time.time() - workflow_start_time

            self.logger.info(
                f"🎉 Sequential Thinking {self.phase_name} workflow completed successfully",
                total_time=workflow.total_time,
            )

            return workflow

        except Exception as e:
            workflow.success = False
            workflow.total_time = time.time() - workflow_start_time

            self.logger.error(
                f"❌ Sequential Thinking {self.phase_name} workflow failed: {str(e)}"
            )
            raise

    def _initialize_steps(self) -> List[SequentialStep]:
        """Initialize the 6 sequential thinking steps"""
        return [
            SequentialStep(SequentialPhase.PROBLEM_ANALYSIS, "Problem Analysis"),
            SequentialStep(SequentialPhase.SYSTEMATIC_APPROACH, "Systematic Approach"),
            SequentialStep(
                SequentialPhase.IMPLEMENTATION_STRATEGY, "Implementation Strategy"
            ),
            SequentialStep(SequentialPhase.VALIDATION_PLAN, "Validation Plan"),
            SequentialStep(
                SequentialPhase.STRATEGIC_ENHANCEMENT, "Strategic Enhancement"
            ),
            SequentialStep(SequentialPhase.SUCCESS_METRICS, "Success Metrics"),
        ]

    @abstractmethod
    async def _execute_step(
        self,
        phase: SequentialPhase,
        context: Optional[Dict[str, Any]],
        previous_results: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute phase-specific step implementation"""
        pass


# Convenience factory function
def create_sequential_workflow(
    phase_name: str, user_stories: List[str], implementation_class: type
) -> BaseSequentialWorkflow:
    """Create phase-specific sequential workflow instance"""
    return implementation_class(phase_name, user_stories)
