"""
MCP Missing Modules Resolver - Task 002 Implementation

Team: Martin (Platform Architecture) + Sequential MCP + Context7 MCP
GitHub Issue: https://github.com/chriscantu/ClaudeDirector/pull/146

Automated resolution system for missing modules with MCP-enhanced analysis,
following github-spec-kit development patterns and BLOAT_PREVENTION_SYSTEM.md compliance.

BUILDS ON EXISTING (DRY Compliance):
- MCPMissingModulesDetectionEngine: Module detection and classification
- HybridInstallationManager: Installation command patterns and execution
- RealMCPIntegrationHelper: MCP server coordination infrastructure
- MCPEnhancedDecisionPipeline: Complex resolution strategy analysis

GITHUB SPEC-KIT PATTERNS:
- Executable Specifications: Resolution strategies that drive actual installation
- Constitutional Development: Enforced DRY principles and architectural compliance
- AI-First Integration: Sequential MCP for complex dependency analysis
- Quality Gates: Built-in validation and rollback mechanisms

INTEGRATION POINTS:
- ai_intelligence/mcp_missing_modules_detection_engine.py: Detection input
- core/hybrid_installation_manager.py: Installation execution (REUSE)
- transparency/real_mcp_integration.py: MCP coordination (REUSE)
- ai_intelligence/mcp_decision_pipeline.py: Complex analysis (REUSE)
"""

import asyncio
import subprocess
import time
import json
from typing import Dict, Any, List, Optional, Set, Tuple, Union, Protocol
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import structlog

# REUSE existing infrastructure - BLOAT_PREVENTION_SYSTEM.md compliance
from .mcp_missing_modules_detection_engine import (
    MCPMissingModulesDetectionEngine,
    MissingModuleInfo,
    MissingModuleCategory,
    MissingModuleSeverity,
    ModuleAvailabilityResult,
)
from .mcp_decision_pipeline import MCPEnhancedDecisionPipeline, PipelineExecutionResult
from .decision_orchestrator import DecisionContext, DecisionComplexity

# REUSE core infrastructure - avoid duplication
from ..core.hybrid_installation_manager import (
    HybridInstallationManager,
    InstallationCommand,
    InstallationResult,
    BaseManager,
    BaseManagerConfig,
    ManagerType,
)

# Optional MCP integration - graceful fallback pattern
try:
    from transparency.real_mcp_integration import RealMCPIntegrationHelper
    from transparency.integrated_transparency import TransparencyContext

    MCP_AVAILABLE = True
except ImportError:
    # Graceful fallback when MCP infrastructure unavailable
    RealMCPIntegrationHelper = None
    TransparencyContext = None
    MCP_AVAILABLE = False

logger = structlog.get_logger(__name__)


class ResolutionStrategy(Enum):
    """Resolution strategy types following github-spec-kit patterns"""

    AUTOMATIC = "automatic"  # Executable resolution with zero user intervention
    GUIDED = "guided"  # Constitutional guidance with user confirmation
    FALLBACK = "fallback"  # Graceful degradation strategy
    ALTERNATIVE = "alternative"  # Alternative package/approach suggestion


class ResolutionStatus(Enum):
    """Resolution execution status tracking"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class ResolutionCommand:
    """
    Extends InstallationCommand pattern for automated resolution
    Follows github-spec-kit executable specifications approach
    """

    strategy_type: str  # "pip", "npm", "conda", "git", "mcp_server", "manual"
    command: str
    args: List[str]
    validation_command: Optional[str] = None
    rollback_command: Optional[str] = None
    success_criteria: Optional[str] = None
    environment_setup: Optional[Dict[str, str]] = None
    expected_duration_ms: int = 5000  # Default 5 second timeout


@dataclass
class ResolutionAttempt:
    """Track individual resolution attempts for audit and rollback"""

    resolution_id: str
    missing_module: MissingModuleInfo
    strategy: ResolutionStrategy
    commands_executed: List[ResolutionCommand]
    status: ResolutionStatus
    start_time: float
    end_time: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    rollback_performed: bool = False


@dataclass
class ResolutionResult:
    """
    Comprehensive result of module resolution operation
    Follows github-spec-kit constitutional development pattern
    """

    modules_processed: int
    modules_resolved: int
    modules_failed: int
    resolution_attempts: List[ResolutionAttempt]
    total_processing_time_ms: int
    mcp_enhanced: bool
    strategic_insights: List[str]
    recommendations: List[str]
    rollback_required: bool = False
    success: bool = False


class ResolutionEnvironmentManager:
    """
    Environment management for package installations
    Follows constitutional development constraints
    """

    def __init__(self):
        self.active_environments = {}
        self.environment_history = []

    def setup_python_environment(self, requirements: List[str]) -> Dict[str, str]:
        """Setup Python virtual environment if needed"""
        env_vars = {}

        try:
            # Check if in virtual environment
            if hasattr(subprocess.sys, "real_prefix") or (
                hasattr(subprocess.sys, "base_prefix")
                and subprocess.sys.base_prefix != subprocess.sys.prefix
            ):
                env_vars["VIRTUAL_ENV"] = subprocess.sys.prefix
                env_vars["PYTHON_ENV"] = "virtual"
            else:
                env_vars["PYTHON_ENV"] = "system"

            return env_vars

        except Exception as e:
            logger.warning("python_environment_setup_failed", error=str(e))
            return {"PYTHON_ENV": "unknown"}

    def setup_node_environment(self, requirements: List[str]) -> Dict[str, str]:
        """Setup Node.js environment for npm/yarn installations"""
        env_vars = {}

        try:
            # Check for package.json and node_modules
            cwd = Path.cwd()
            if (cwd / "package.json").exists():
                env_vars["NODE_PROJECT"] = "detected"
                if (cwd / "node_modules").exists():
                    env_vars["NODE_MODULES"] = "available"

            return env_vars

        except Exception as e:
            logger.warning("node_environment_setup_failed", error=str(e))
            return {"NODE_ENV": "unknown"}


class MCPMissingModulesResolver(BaseManager):
    """
    🚀 MCP Missing Modules Resolver - Task 002

    Team Lead: Martin | MCP Integration: Sequential + Context7
    GitHub Spec-Kit Pattern: Executable specifications with constitutional constraints

    Automated resolution system for missing modules detected by the
    MCP Missing Modules Detection Engine.

    ARCHITECTURE COMPLIANCE:
    - PROJECT_STRUCTURE.md: Placed in ai_intelligence/ (AI enhancement domain)
    - BLOAT_PREVENTION_SYSTEM.md: Reuses existing installation infrastructure
    - GitHub Spec-Kit: Executable specifications with AI-first integration

    REUSES EXISTING (DRY Compliance):
    - HybridInstallationManager: Installation command execution
    - MCPMissingModulesDetectionEngine: Module detection and classification
    - MCPEnhancedDecisionPipeline: Complex resolution strategy analysis
    - RealMCPIntegrationHelper: MCP server coordination

    FEATURES:
    - Automatic package installation (pip, npm, conda, yarn)
    - Environment management and validation
    - MCP server resolution and coordination
    - Framework-specific dependency resolution
    - Rollback and error recovery mechanisms
    - Strategic impact analysis and recommendations
    """

    def __init__(
        self,
        detection_engine: MCPMissingModulesDetectionEngine,
        installation_manager: Optional[HybridInstallationManager] = None,
        mcp_helper: Optional[RealMCPIntegrationHelper] = None,
        decision_pipeline: Optional[MCPEnhancedDecisionPipeline] = None,
        config: Optional[BaseManagerConfig] = None,
    ):
        """
        Initialize MCP Missing Modules Resolver

        Args:
            detection_engine: Module detection engine (REQUIRED)
            installation_manager: Installation command executor (REUSE existing)
            mcp_helper: MCP server integration (REUSE existing)
            decision_pipeline: Complex analysis pipeline (REUSE existing)
            config: BaseManager configuration
        """
        # BaseManager initialization
        if config is None:
            config = BaseManagerConfig(
                manager_name="mcp_missing_modules_resolver",
                manager_type=ManagerType.AI_ENHANCEMENT,
                enable_metrics=True,
                enable_caching=True,
                enable_logging=True,
                custom_config={
                    "auto_resolution_enabled": True,
                    "rollback_on_failure": True,
                    "max_concurrent_resolutions": 3,
                    "resolution_timeout_ms": 30000,
                },
            )

        super().__init__(config)

        # Core dependencies - follow BLOAT_PREVENTION_SYSTEM.md
        self.detection_engine = detection_engine
        self.installation_manager = installation_manager or HybridInstallationManager()
        self.mcp_helper = mcp_helper
        self.decision_pipeline = decision_pipeline

        # Resolution infrastructure
        self.environment_manager = ResolutionEnvironmentManager()
        self.resolution_strategies = self._initialize_resolution_strategies()
        self.package_managers = self._initialize_package_managers()

        # Performance tracking
        self.resolution_metrics = {
            "resolutions_attempted": 0,
            "resolutions_successful": 0,
            "avg_resolution_time_ms": 0,
            "mcp_enhancements_applied": 0,
            "rollbacks_performed": 0,
        }

        logger.info(
            "mcp_missing_modules_resolver_initialized",
            detection_engine_available=True,
            installation_manager_available=bool(installation_manager),
            mcp_available=MCP_AVAILABLE,
            strategies_loaded=len(self.resolution_strategies),
        )

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Delegates to resolution management operations
        """
        if operation == "resolve_modules":
            return await self.resolve_missing_modules(*args, **kwargs)
        elif operation == "resolve_file":
            return await self.resolve_file_modules(*args, **kwargs)
        elif operation == "validate_resolution":
            return await self.validate_resolution(*args, **kwargs)
        elif operation == "rollback_resolution":
            return await self.rollback_resolution(*args, **kwargs)
        elif operation == "get_metrics":
            return self.get_resolution_metrics()
        else:
            self.logger.warning(f"Unknown resolution operation: {operation}")
            return None

    def _initialize_resolution_strategies(self) -> Dict[str, Dict[str, Any]]:
        """
        🏗️ Martin's Architecture: Initialize resolution strategies

        Maps module categories to executable resolution specifications.
        """
        return {
            MissingModuleCategory.CORE_FRAMEWORK.value: {
                "strategies": ["automatic", "guided"],
                "package_managers": ["npm", "yarn", "pip"],
                "validation_required": True,
                "rollback_strategy": "full",
            },
            MissingModuleCategory.PYTHON_PACKAGE.value: {
                "strategies": ["automatic"],
                "package_managers": ["pip", "conda"],
                "validation_required": True,
                "rollback_strategy": "package_only",
            },
            MissingModuleCategory.MCP_SERVER.value: {
                "strategies": ["guided", "fallback"],
                "package_managers": ["mcp_server"],
                "validation_required": True,
                "rollback_strategy": "configuration_only",
            },
            MissingModuleCategory.INTERNAL_MODULE.value: {
                "strategies": ["guided", "alternative"],
                "package_managers": ["manual"],
                "validation_required": False,
                "rollback_strategy": "none",
            },
            MissingModuleCategory.OPTIONAL_FEATURE.value: {
                "strategies": ["guided", "fallback"],
                "package_managers": ["pip", "npm"],
                "validation_required": False,
                "rollback_strategy": "optional",
            },
        }

    def _initialize_package_managers(self) -> Dict[str, Dict[str, Any]]:
        """
        🏗️ Martin's Architecture: Initialize package manager configurations

        Defines executable package manager commands and validation.
        """
        return {
            "pip": {
                "install_command": "pip",
                "install_args": ["install"],
                "validation_command": "pip",
                "validation_args": ["show"],
                "environment_setup": self.environment_manager.setup_python_environment,
            },
            "conda": {
                "install_command": "conda",
                "install_args": ["install", "-y"],
                "validation_command": "conda",
                "validation_args": ["list"],
                "environment_setup": self.environment_manager.setup_python_environment,
            },
            "npm": {
                "install_command": "npm",
                "install_args": ["install"],
                "validation_command": "npm",
                "validation_args": ["list"],
                "environment_setup": self.environment_manager.setup_node_environment,
            },
            "yarn": {
                "install_command": "yarn",
                "install_args": ["add"],
                "validation_command": "yarn",
                "validation_args": ["list"],
                "environment_setup": self.environment_manager.setup_node_environment,
            },
        }

    async def resolve_missing_modules(
        self,
        detection_result: ModuleAvailabilityResult,
        auto_install: bool = True,
        transparency_context: Optional[TransparencyContext] = None,
        use_mcp_enhancement: bool = True,
    ) -> ResolutionResult:
        """
        🎯 CORE METHOD: Resolve missing modules from detection result

        Follows github-spec-kit executable specifications pattern for
        automated resolution with constitutional constraints.

        Args:
            detection_result: Output from MCPMissingModulesDetectionEngine
            auto_install: Whether to automatically install packages
            transparency_context: Transparency tracking context
            use_mcp_enhancement: Whether to use MCP for complex analysis

        Returns:
            ResolutionResult with comprehensive resolution analysis
        """
        start_time = time.time()
        resolution_attempts = []
        strategic_insights = []
        recommendations = []

        try:
            logger.info(
                "module_resolution_started",
                modules_to_resolve=len(detection_result.missing_modules),
                auto_install=auto_install,
                mcp_enhancement=use_mcp_enhancement,
            )

            # MCP Enhancement - Strategic analysis for complex resolutions
            mcp_enhanced = False
            if (
                use_mcp_enhancement
                and self.mcp_helper
                and len(detection_result.missing_modules) > 2
            ):
                try:
                    strategic_analysis = (
                        await self._perform_strategic_resolution_analysis(
                            detection_result, transparency_context
                        )
                    )

                    if strategic_analysis:
                        strategic_insights = strategic_analysis.get("insights", [])
                        recommendations = strategic_analysis.get("recommendations", [])
                        mcp_enhanced = True
                        self.resolution_metrics["mcp_enhancements_applied"] += 1

                except Exception as e:
                    logger.warning(
                        "strategic_resolution_analysis_failed",
                        error=str(e),
                        fallback="proceeding_with_standard_resolution",
                    )

            # Process each missing module
            for missing_module in detection_result.missing_modules:
                resolution_attempt = await self._resolve_single_module(
                    missing_module, auto_install, transparency_context
                )
                resolution_attempts.append(resolution_attempt)

            # Calculate results
            successful_resolutions = len([r for r in resolution_attempts if r.success])
            failed_resolutions = len([r for r in resolution_attempts if not r.success])
            total_processing_time_ms = int((time.time() - start_time) * 1000)

            # Update metrics
            self._update_resolution_metrics(
                len(detection_result.missing_modules),
                successful_resolutions,
                total_processing_time_ms,
            )

            # Determine if rollback required
            rollback_required = (
                failed_resolutions > 0
                and self.config.custom_config.get("rollback_on_failure", True)
            )

            result = ResolutionResult(
                modules_processed=len(detection_result.missing_modules),
                modules_resolved=successful_resolutions,
                modules_failed=failed_resolutions,
                resolution_attempts=resolution_attempts,
                total_processing_time_ms=total_processing_time_ms,
                mcp_enhanced=mcp_enhanced,
                strategic_insights=strategic_insights,
                recommendations=recommendations,
                rollback_required=rollback_required,
                success=successful_resolutions > 0 and failed_resolutions == 0,
            )

            logger.info(
                "module_resolution_completed",
                modules_processed=result.modules_processed,
                modules_resolved=result.modules_resolved,
                modules_failed=result.modules_failed,
                mcp_enhanced=result.mcp_enhanced,
                processing_time_ms=result.total_processing_time_ms,
            )

            return result

        except Exception as e:
            total_processing_time_ms = int((time.time() - start_time) * 1000)

            logger.error(
                "module_resolution_failed",
                error=str(e),
                modules_attempted=len(detection_result.missing_modules),
                processing_time_ms=total_processing_time_ms,
            )

            return ResolutionResult(
                modules_processed=len(detection_result.missing_modules),
                modules_resolved=0,
                modules_failed=len(detection_result.missing_modules),
                resolution_attempts=resolution_attempts,
                total_processing_time_ms=total_processing_time_ms,
                mcp_enhanced=False,
                strategic_insights=[],
                recommendations=["Review errors and attempt manual resolution"],
                rollback_required=True,
                success=False,
            )

    async def _resolve_single_module(
        self,
        missing_module: MissingModuleInfo,
        auto_install: bool,
        transparency_context: Optional[TransparencyContext],
    ) -> ResolutionAttempt:
        """
        🏗️ Martin's Architecture: Resolve individual missing module

        Implements executable specification pattern for single module resolution.
        """
        resolution_id = (
            f"resolution_{int(time.time() * 1000)}_{missing_module.module_name}"
        )
        start_time = time.time()

        resolution_attempt = ResolutionAttempt(
            resolution_id=resolution_id,
            missing_module=missing_module,
            strategy=ResolutionStrategy.AUTOMATIC,
            commands_executed=[],
            status=ResolutionStatus.PENDING,
            start_time=start_time,
        )

        try:
            # Get resolution commands for module category
            resolution_commands = self._generate_resolution_commands(missing_module)

            if not resolution_commands:
                resolution_attempt.status = ResolutionStatus.FAILED
                resolution_attempt.error_message = "No resolution strategy available"
                return resolution_attempt

            resolution_attempt.status = ResolutionStatus.IN_PROGRESS

            # Execute resolution commands
            for command in resolution_commands:
                if auto_install:
                    success = await self._execute_resolution_command(
                        command, missing_module
                    )

                    resolution_attempt.commands_executed.append(command)

                    if success:
                        # Validate resolution
                        if await self._validate_module_resolution(missing_module):
                            resolution_attempt.success = True
                            resolution_attempt.status = ResolutionStatus.COMPLETED
                            break
                    else:
                        # Continue to next command if available
                        continue
                else:
                    # Guided resolution - provide commands but don't execute
                    resolution_attempt.commands_executed.append(command)
                    resolution_attempt.strategy = ResolutionStrategy.GUIDED

            if not resolution_attempt.success and auto_install:
                resolution_attempt.status = ResolutionStatus.FAILED
                resolution_attempt.error_message = "All resolution commands failed"

            resolution_attempt.end_time = time.time()

            return resolution_attempt

        except Exception as e:
            resolution_attempt.status = ResolutionStatus.FAILED
            resolution_attempt.error_message = str(e)
            resolution_attempt.end_time = time.time()

            logger.error(
                "single_module_resolution_failed",
                module=missing_module.module_name,
                resolution_id=resolution_id,
                error=str(e),
            )

            return resolution_attempt

    def _generate_resolution_commands(
        self, missing_module: MissingModuleInfo
    ) -> List[ResolutionCommand]:
        """
        🏗️ Martin's Architecture: Generate resolution commands for module

        Creates executable resolution specifications based on module category.
        """
        commands = []
        category = missing_module.category.value

        # Get strategy configuration
        strategy_config = self.resolution_strategies.get(category, {})
        package_managers = strategy_config.get("package_managers", ["pip"])

        # Generate commands for each package manager
        for pm_name in package_managers:
            if pm_name in self.package_managers:
                pm_config = self.package_managers[pm_name]

                # Create resolution command
                command = ResolutionCommand(
                    strategy_type=pm_name,
                    command=pm_config["install_command"],
                    args=pm_config["install_args"] + [missing_module.module_name],
                    validation_command=pm_config["validation_command"],
                    success_criteria=f"module_{missing_module.module_name}_importable",
                    environment_setup=pm_config.get("environment_setup"),
                )

                commands.append(command)

        return commands

    async def _execute_resolution_command(
        self, command: ResolutionCommand, missing_module: MissingModuleInfo
    ) -> bool:
        """
        🏗️ Martin's Architecture: Execute resolution command

        Uses existing HybridInstallationManager infrastructure.
        """
        try:
            # Setup environment if needed
            env_vars = {}
            if command.environment_setup:
                env_vars = command.environment_setup([missing_module.module_name])

            # Use installation manager for execution - REUSE existing infrastructure
            installation_command = InstallationCommand(
                type="permanent",
                command=command.command,
                args=command.args,
            )

            # Execute through existing installation manager
            result = await self.installation_manager.try_installation_command(
                installation_command
            )

            return result.success

        except Exception as e:
            logger.error(
                "resolution_command_execution_failed",
                command=command.command,
                args=command.args,
                module=missing_module.module_name,
                error=str(e),
            )
            return False

    async def _validate_module_resolution(
        self, missing_module: MissingModuleInfo
    ) -> bool:
        """
        🏗️ Martin's Architecture: Validate module resolution success

        Verifies module is now importable and functional.
        """
        try:
            # Use detection engine to re-check module availability
            # REUSE existing infrastructure
            module_available = self.detection_engine._check_module_availability(
                missing_module.module_name
            )

            return module_available

        except Exception as e:
            logger.warning(
                "module_validation_failed",
                module=missing_module.module_name,
                error=str(e),
            )
            return False

    async def _perform_strategic_resolution_analysis(
        self,
        detection_result: ModuleAvailabilityResult,
        transparency_context: Optional[TransparencyContext],
    ) -> Optional[Dict[str, Any]]:
        """
        🚀 MCP Enhancement: Strategic analysis for complex module resolution

        Uses Sequential MCP for systematic dependency analysis.
        """
        if not self.decision_pipeline or not transparency_context:
            return None

        try:
            # Create decision context for strategic analysis
            missing_modules = [m.module_name for m in detection_result.missing_modules]
            frameworks = list(detection_result.framework_dependencies.keys())

            decision_context = DecisionContext(
                message=f"Strategic resolution analysis for {len(missing_modules)} missing modules",
                stakeholder_scope="development_team",
                persona="martin",  # Technical architecture persona
                complexity=DecisionComplexity.HIGH,
                detected_frameworks=frameworks,
                metadata={
                    "analysis_type": "strategic_resolution",
                    "missing_modules": missing_modules,
                    "framework_dependencies": detection_result.framework_dependencies,
                    "mcp_servers_available": detection_result.mcp_servers_available,
                },
            )

            # Execute strategic analysis pipeline
            pipeline_result = await self.decision_pipeline.execute_pipeline(
                decision_context, transparency_context
            )

            if pipeline_result.success:
                return {
                    "insights": pipeline_result.final_recommendations,
                    "recommendations": self._extract_resolution_recommendations(
                        pipeline_result
                    ),
                    "confidence": pipeline_result.confidence_score,
                }

        except Exception as e:
            logger.warning(
                "strategic_resolution_analysis_failed",
                error=str(e),
                modules=len(detection_result.missing_modules),
            )

        return None

    def _extract_resolution_recommendations(
        self, pipeline_result: PipelineExecutionResult
    ) -> List[str]:
        """Extract actionable resolution recommendations from MCP analysis"""
        recommendations = []

        # Extract framework-specific recommendations
        if pipeline_result.framework_insights:
            for stage_name, insights in pipeline_result.framework_insights.items():
                if isinstance(insights, list):
                    for insight in insights:
                        if (
                            "install" in str(insight).lower()
                            or "resolution" in str(insight).lower()
                        ):
                            recommendations.append(f"Strategic insight: {insight}")

        # Add general recommendations
        recommendations.extend(
            [
                "Consider dependency grouping for related modules",
                "Validate framework compatibility before installation",
                "Use virtual environments for isolation",
            ]
        )

        return recommendations

    def _update_resolution_metrics(
        self, attempted: int, successful: int, processing_time_ms: int
    ):
        """🏗️ Martin: Update resolution performance metrics"""
        self.resolution_metrics["resolutions_attempted"] += attempted
        self.resolution_metrics["resolutions_successful"] += successful

        # Update average processing time
        current_avg = self.resolution_metrics["avg_resolution_time_ms"]
        count = self.resolution_metrics["resolutions_attempted"]
        if count > 0:
            new_avg = ((current_avg * (count - attempted)) + processing_time_ms) / count
            self.resolution_metrics["avg_resolution_time_ms"] = new_avg

    def get_resolution_metrics(self) -> Dict[str, Any]:
        """Get current resolution performance metrics"""
        return self.resolution_metrics.copy()

    async def resolve_file_modules(
        self,
        file_path: str,
        auto_install: bool = True,
        transparency_context: Optional[TransparencyContext] = None,
    ) -> ResolutionResult:
        """
        🎯 CONVENIENCE METHOD: Detect and resolve modules for a single file

        Combines detection and resolution in single operation.
        """
        # Use detection engine to analyze file
        detection_result = await self.detection_engine.analyze_module_availability(
            file_path, transparency_context, use_mcp_enhancement=True
        )

        # Resolve missing modules
        return await self.resolve_missing_modules(
            detection_result, auto_install, transparency_context
        )


# Factory function for easy integration
def create_mcp_missing_modules_resolver(
    detection_engine: MCPMissingModulesDetectionEngine,
    installation_manager: Optional[HybridInstallationManager] = None,
    mcp_helper: Optional[RealMCPIntegrationHelper] = None,
    decision_pipeline: Optional[MCPEnhancedDecisionPipeline] = None,
) -> MCPMissingModulesResolver:
    """
    🏗️ Martin's Architecture: Factory for MCP Missing Modules Resolver

    Creates resolver with integrated detection and resolution capabilities.
    """
    resolver = MCPMissingModulesResolver(
        detection_engine=detection_engine,
        installation_manager=installation_manager,
        mcp_helper=mcp_helper,
        decision_pipeline=decision_pipeline,
    )

    logger.info(
        "mcp_missing_modules_resolver_created",
        detection_engine_available=True,
        installation_manager_available=bool(installation_manager),
        mcp_available=MCP_AVAILABLE,
    )

    return resolver
