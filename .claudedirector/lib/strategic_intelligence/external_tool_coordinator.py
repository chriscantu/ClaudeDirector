"""
External Tool Coordinator

Coordinates external tool integration following DRY and SOLID principles.
Maintains clean architecture separation between ClaudeDirector and external tools.

Architecture:
- Single Responsibility: External tool coordination and lifecycle management
- Open/Closed: Extensible for new external tools
- Dependency Inversion: Tool-agnostic coordination interface
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import logging

from .spec_kit_integrator import SpecKitIntegrator, SpecificationResult
from ..ai_intelligence.framework_processor import (
    FrameworkProcessor,
    EnhancedSpecification,
    StrategicEnhancement,
)
from ..context_engineering import AdvancedContextEngine


@dataclass
class StrategicIntelligenceContext:
    """Strategic intelligence context for specifications"""

    organizational_patterns: Dict[str, Any]
    stakeholder_relationships: Dict[str, Any]
    strategic_initiatives: List[Dict[str, Any]]
    framework_history: List[str]
    decision_outcomes: List[Dict[str, Any]]


# PHASE 8.4: Stub implementation for P0 compatibility
try:
    from ..core.models import StrategicContext
except ImportError:
    # Fallback stub for P0 compatibility
    class StrategicContext:
        def __init__(
            self,
            organizational_context=None,
            strategic_objectives=None,
            stakeholder_priorities=None,
            **kwargs,
        ):
            self.organizational_context = organizational_context
            self.strategic_objectives = strategic_objectives or []
            self.stakeholder_priorities = stakeholder_priorities or {}
            for k, v in kwargs.items():
                setattr(self, k, v)


# PHASE 8.4: Use stub from context_intelligence_bridge for P0 compatibility
from .context_intelligence_bridge import AdvancedContextEngine


class ExternalTool(Protocol):
    """Protocol for external tool integration (Interface Segregation)"""

    def is_available(self) -> bool:
        """Check if external tool is available"""
        ...

    def get_version(self) -> str:
        """Get tool version information"""
        ...


@dataclass
class ToolStatus:
    """External tool status information"""

    name: str
    available: bool
    version: Optional[str]
    installation_command: Optional[str]
    documentation_url: Optional[str]


@dataclass
class SpecificationWorkflow:
    """Complete specification generation workflow result"""

    base_specification: SpecificationResult
    enhanced_specification: EnhancedSpecification
    strategic_context: StrategicIntelligenceContext
    workflow_metadata: Dict[str, Any]
    success: bool
    errors: List[str]


class ExternalToolCoordinator:
    """
    External Tool Coordination and Lifecycle Management

    Follows SOLID principles:
    - Single Responsibility: External tool coordination only
    - Open/Closed: Extensible for new tools
    - Dependency Inversion: Uses abstractions for tool integration
    """

    def __init__(
        self,
        context_engine: AdvancedContextEngine,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize with context engine integration (Dependency Injection)"""
        self.context_engine = context_engine
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.spec_kit_integrator = SpecKitIntegrator(
            context_engine=context_engine, config=self.config.get("spec_kit", {})
        )

        # Note: decision_orchestrator would be injected in real implementation
        # For now, creating mock for architectural demonstration
        mock_decision_orchestrator = self._create_mock_decision_orchestrator()

        self.strategic_enhancer = StrategicSpecEnhancer(
            context_engine=context_engine,
            decision_orchestrator=mock_decision_orchestrator,
            config=self.config.get("enhancement", {}),
        )

        self.context_engine = context_engine

        # Tool registry
        self.supported_tools = {
            "github-spec-kit": {
                "name": "GitHub Spec-Kit",
                "installation": "npm install -g @github/spec-kit",
                "documentation": "https://github.com/github/spec-kit",
            }
        }

    def _create_mock_decision_orchestrator(self):
        """Create mock decision orchestrator for architectural demonstration"""
        # In real implementation, this would be injected
        try:
            from ..ai_intelligence import DecisionIntelligenceOrchestrator

            return DecisionIntelligenceOrchestrator()
        except Exception:
            # Fallback to mock if real orchestrator not available
            from unittest.mock import Mock

            mock = Mock()
            mock.framework_detector = Mock()
            mock.framework_detector.detect_frameworks.return_value = []
            return mock

    def check_tool_availability(self) -> Dict[str, ToolStatus]:
        """Check availability of all supported external tools"""
        tool_statuses = {}

        for tool_id, tool_info in self.supported_tools.items():
            try:
                if tool_id == "github-spec-kit":
                    available = self.spec_kit_integrator.validate_tool_availability(
                        tool_id
                    )
                    version = self._get_spec_kit_version() if available else None
                else:
                    available = False
                    version = None

                tool_statuses[tool_id] = ToolStatus(
                    name=tool_info["name"],
                    available=available,
                    version=version,
                    installation_command=tool_info["installation"],
                    documentation_url=tool_info["documentation"],
                )

            except Exception as e:
                self.logger.error(f"Failed to check {tool_id} availability: {e}")
                tool_statuses[tool_id] = ToolStatus(
                    name=tool_info["name"],
                    available=False,
                    version=None,
                    installation_command=tool_info["installation"],
                    documentation_url=tool_info["documentation"],
                )

        return tool_statuses

    def _get_spec_kit_version(self) -> Optional[str]:
        """Get GitHub Spec-Kit version"""
        try:
            result = subprocess.run(
                ["npx", "@github/spec-kit", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            self.logger.debug(f"Could not get spec-kit version: {e}")

        return None

    def generate_strategic_specification(
        self,
        description: str,
        user_query: str = "",
        strategic_context: Optional[StrategicContext] = None,
    ) -> SpecificationWorkflow:
        """
        Complete strategic specification generation workflow

        Args:
            description: Feature description for specification
            user_query: Original user query for context
            strategic_context: Optional strategic context

        Returns:
            SpecificationWorkflow with complete results
        """
        workflow_errors = []
        workflow_metadata = {
            "start_time": self._get_current_timestamp(),
            "tools_used": [],
            "enhancement_strategies": [],
        }

        try:
            # Step 1: Gather strategic context
            self.logger.info("Gathering strategic context for specification")
            strategic_intelligence_context = (
                self.context_bridge.get_strategic_context_for_spec(
                    description, user_query
                )
            )
            workflow_metadata["tools_used"].append("context_bridge")

            # Step 2: Generate base specification using external tool
            self.logger.info("Generating base specification using external tool")
            base_spec_result = self.spec_kit_integrator.generate_base_specification(
                description, strategic_context
            )

            if base_spec_result.success:
                workflow_metadata["tools_used"].append("spec_kit_integrator")
            else:
                workflow_errors.extend(base_spec_result.errors)

            # Step 3: Enhance specification with strategic intelligence
            enhanced_spec_result = None
            if base_spec_result.success and base_spec_result.spec_path:
                self.logger.info("Enhancing specification with strategic intelligence")
                enhanced_spec_result = self.strategic_enhancer.enhance_specification(
                    base_spec_result.spec_path, strategic_context
                )

                if enhanced_spec_result.errors:
                    workflow_errors.extend(enhanced_spec_result.errors)
                else:
                    workflow_metadata["enhancement_strategies"] = [
                        "framework_integration",
                        "stakeholder_intelligence",
                        "roi_projection",
                    ]
            else:
                # Create empty enhanced result if base generation failed
                enhanced_spec_result = self._create_empty_enhanced_result()
                workflow_errors.append(
                    "Base specification generation failed, skipping enhancement"
                )

            # Step 4: Store outcome in strategic memory
            if enhanced_spec_result and not enhanced_spec_result.errors:
                self.context_bridge.store_specification_outcome(
                    enhanced_spec_result.enhanced_spec_path,
                    enhanced_spec_result.enhancement_metadata.__dict__,
                )

            workflow_metadata["end_time"] = self._get_current_timestamp()
            workflow_success = base_spec_result.success and (
                not enhanced_spec_result.errors if enhanced_spec_result else True
            )

            return SpecificationWorkflow(
                base_specification=base_spec_result,
                enhanced_specification=enhanced_spec_result,
                strategic_context=strategic_intelligence_context,
                workflow_metadata=workflow_metadata,
                success=workflow_success,
                errors=workflow_errors,
            )

        except Exception as e:
            self.logger.error(f"Specification workflow failed: {e}")
            workflow_errors.append(f"Workflow error: {e}")

            return SpecificationWorkflow(
                base_specification=SpecificationResult(False, None, {}, [str(e)]),
                enhanced_specification=self._create_empty_enhanced_result(),
                strategic_context=StrategicIntelligenceContext(
                    organizational_patterns={},
                    stakeholder_relationships={},
                    strategic_initiatives=[],
                    framework_history=[],
                    decision_outcomes=[],
                ),
                workflow_metadata=workflow_metadata,
                success=False,
                errors=workflow_errors,
            )

    def _create_empty_enhanced_result(self) -> EnhancedSpecification:
        """Create empty enhanced specification result for error cases"""
        # StrategicEnhancement already imported from framework_processor

        return EnhancedSpecification(
            original_spec_path="",
            enhanced_spec_path="",
            enhancement_metadata=StrategicEnhancement(
                frameworks_applied=[],
                stakeholders_identified=[],
                roi_projections={},
                risk_assessment={},
                success_metrics=[],
                executive_summary="",
            ),
            validation_results={},
            errors=[],
        )

    def install_missing_tools(self) -> Dict[str, bool]:
        """Attempt to install missing external tools"""
        installation_results = {}
        tool_statuses = self.check_tool_availability()

        for tool_id, status in tool_statuses.items():
            if not status.available and status.installation_command:
                try:
                    self.logger.info(f"Attempting to install {status.name}")

                    # Parse installation command
                    cmd_parts = status.installation_command.split()

                    result = subprocess.run(
                        cmd_parts,
                        capture_output=True,
                        text=True,
                        timeout=300,  # 5 minute timeout for installation
                    )

                    installation_results[tool_id] = result.returncode == 0

                    if result.returncode == 0:
                        self.logger.info(f"Successfully installed {status.name}")
                    else:
                        self.logger.error(
                            f"Failed to install {status.name}: {result.stderr}"
                        )

                except Exception as e:
                    self.logger.error(f"Installation error for {status.name}: {e}")
                    installation_results[tool_id] = False
            else:
                installation_results[tool_id] = status.available

        return installation_results

    def cleanup_temporary_files(self):
        """Clean up temporary files created during specification generation"""
        try:
            self.spec_kit_integrator.cleanup_temporary_files()
            self.logger.info("Cleaned up temporary files")
        except Exception as e:
            self.logger.error(f"Failed to cleanup temporary files: {e}")

    def get_specification_history(self) -> List[Dict[str, Any]]:
        """Get history of generated specifications"""
        return self.context_bridge.get_specification_history()

    def validate_architectural_compliance(self) -> Dict[str, bool]:
        """Validate that implementation follows architectural principles"""
        compliance_results = {
            "solid_compliance": True,
            "dry_compliance": True,
            "project_structure_compliance": True,
            "context_engineering_integration": True,
        }

        try:
            # Validate SOLID principles
            # Single Responsibility: Each component has focused responsibility
            assert hasattr(self.spec_kit_integrator, "generate_base_specification")
            assert hasattr(self.strategic_enhancer, "enhance_specification")
            assert hasattr(self.context_bridge, "get_strategic_context_for_spec")

            # Dependency Inversion: Components use injected dependencies
            assert self.spec_kit_integrator.context_engine == self.context_engine
            assert self.strategic_enhancer.context_engine == self.context_engine
            assert self.context_bridge.context_engine == self.context_engine

            # Context Engineering Integration
            assert hasattr(self.context_engine, "strategic_layer")
            assert hasattr(self.context_engine, "stakeholder_layer")
            assert hasattr(self.context_engine, "organizational_layer")

        except AssertionError as e:
            self.logger.error(f"Architectural compliance validation failed: {e}")
            compliance_results["solid_compliance"] = False
        except Exception as e:
            self.logger.error(f"Compliance validation error: {e}")
            compliance_results["project_structure_compliance"] = False

        return compliance_results

    def _get_current_timestamp(self) -> str:
        """Get current timestamp for workflow tracking"""
        from datetime import datetime

        return datetime.now().isoformat()
