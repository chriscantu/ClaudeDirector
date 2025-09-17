"""
MCP Missing Modules Detection Engine - Task 001 Implementation

Team: Martin (Platform Architecture) + Sequential MCP + Context7 MCP
GitHub Issue: https://github.com/chriscantu/ClaudeDirector/pull/146

Intelligent detection of missing modules with MCP-enhanced analysis, integrated
with existing ClaudeDirector MCP infrastructure and framework detection patterns.

BUILDS ON EXISTING:
- MCPEnhancedDecisionPipeline: MCP server coordination patterns
- RealMCPIntegrationHelper: Production MCP server integration
- FrameworkDetector: Framework detection infrastructure
- PROJECT_STRUCTURE.md: Architectural compliance
- BLOAT_PREVENTION_SYSTEM.md: DRY principle enforcement

INTEGRATES WITH:
- ai_intelligence/mcp_decision_pipeline.py: MCP coordination
- transparency/real_mcp_integration.py: MCP server calls
- ai_intelligence/framework_detector.py: Framework import analysis
"""

import ast
import sys
import importlib.util
import time
from typing import Dict, Any, List, Optional, Set, Tuple, Union
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import structlog

# Core dependencies - follow existing patterns
from .decision_orchestrator import DecisionContext, DecisionComplexity
from .mcp_decision_pipeline import MCPEnhancedDecisionPipeline, PipelineExecutionResult

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

# Optional framework detection - follow existing patterns
try:
    from .framework_detector import FrameworkDetector

    FRAMEWORK_DETECTOR_AVAILABLE = True
except ImportError:
    # Graceful fallback - framework detection not available
    FrameworkDetector = None
    FRAMEWORK_DETECTOR_AVAILABLE = False

logger = structlog.get_logger(__name__)


class MissingModuleCategory(Enum):
    """Classification of missing module types"""

    CORE_FRAMEWORK = "core_framework"  # React, Vue, Angular, etc.
    MCP_SERVER = "mcp_server"  # Context7, Sequential, Magic
    PYTHON_PACKAGE = "python_package"  # External Python dependencies
    INTERNAL_MODULE = "internal_module"  # ClaudeDirector internal modules
    OPTIONAL_FEATURE = "optional_feature"  # Optional functionality


class MissingModuleSeverity(Enum):
    """Severity levels for missing modules"""

    CRITICAL = "critical"  # Blocks core functionality
    HIGH = "high"  # Significantly impacts features
    MODERATE = "moderate"  # Some features unavailable
    LOW = "low"  # Optional enhancements only


@dataclass
class MissingModuleInfo:
    """Information about a missing module"""

    module_name: str
    import_statement: str
    category: MissingModuleCategory
    severity: MissingModuleSeverity
    file_path: str
    line_number: int
    suggested_resolution: str
    fallback_available: bool
    framework_context: Optional[str] = None
    mcp_server_context: Optional[str] = None


@dataclass
class ModuleAvailabilityResult:
    """Result of module availability analysis"""

    modules_checked: int
    missing_modules: List[MissingModuleInfo]
    available_modules: List[str]
    mcp_servers_available: Dict[str, bool]
    framework_dependencies: Dict[str, List[str]]
    analysis_confidence: float
    processing_time_ms: int
    mcp_enhanced: bool = False


class MCPMissingModulesDetectionEngine:
    """
    🚀 MCP Missing Modules Detection Engine

    Team Lead: Martin | MCP Integration: Sequential + Context7

    Intelligent detection and analysis of missing modules with MCP-enhanced
    insights and automatic resolution suggestions.

    ARCHITECTURE COMPLIANCE:
    - PROJECT_STRUCTURE.md: Placed in ai_intelligence/ (AI enhancement domain)
    - BLOAT_PREVENTION_SYSTEM.md: Single source of truth for missing module detection
    - Existing patterns: Follows graceful import fallback patterns

    MCP INTEGRATION:
    - Sequential MCP: Systematic dependency analysis
    - Context7 MCP: Framework-specific import pattern recognition
    - Real MCP Helper: Production server coordination

    FEATURES:
    - AST-based import analysis
    - Framework-aware dependency checking
    - MCP server availability validation
    - Intelligent resolution suggestions
    - Graceful fallback strategies
    """

    def __init__(
        self,
        mcp_helper: Optional[RealMCPIntegrationHelper] = None,
        framework_detector: Optional[FrameworkDetector] = None,
        decision_pipeline: Optional[MCPEnhancedDecisionPipeline] = None,
    ):
        """
        Initialize MCP Missing Modules Detection Engine

        Args:
            mcp_helper: MCP server integration (optional)
            framework_detector: Framework detection engine (optional)
            decision_pipeline: MCP enhanced decision pipeline (optional)
        """
        self.mcp_helper = mcp_helper
        self.framework_detector = framework_detector
        self.decision_pipeline = decision_pipeline

        # Core detection patterns
        self.framework_import_patterns = self._initialize_framework_patterns()
        self.mcp_server_patterns = self._initialize_mcp_patterns()
        self.internal_module_patterns = self._initialize_internal_patterns()

        # Performance metrics
        self.detection_metrics = {
            "analyses_performed": 0,
            "modules_detected": 0,
            "mcp_enhancements_applied": 0,
            "avg_processing_time_ms": 0,
        }

        logger.info(
            "mcp_missing_modules_detection_engine_initialized",
            mcp_available=MCP_AVAILABLE,
            framework_detector_available=FRAMEWORK_DETECTOR_AVAILABLE,
            patterns_loaded=len(self.framework_import_patterns)
            + len(self.mcp_server_patterns),
        )

    def _initialize_framework_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        🏗️ Martin's Architecture: Initialize framework import patterns

        Maps framework-specific imports to resolution strategies.
        """
        return {
            "react": {
                "patterns": ["react", "react-dom", "@types/react"],
                "category": MissingModuleCategory.CORE_FRAMEWORK,
                "severity": MissingModuleSeverity.HIGH,
                "resolution": "npm install react react-dom @types/react",
                "fallback": "Use vanilla JavaScript or alternative framework",
            },
            "vue": {
                "patterns": ["vue", "@vue/", "vue-router", "vuex"],
                "category": MissingModuleCategory.CORE_FRAMEWORK,
                "severity": MissingModuleSeverity.HIGH,
                "resolution": "npm install vue @vue/cli vue-router",
                "fallback": "Use vanilla JavaScript or alternative framework",
            },
            "angular": {
                "patterns": ["@angular/", "angular"],
                "category": MissingModuleCategory.CORE_FRAMEWORK,
                "severity": MissingModuleSeverity.HIGH,
                "resolution": "npm install @angular/core @angular/cli",
                "fallback": "Use vanilla JavaScript or alternative framework",
            },
            "fastapi": {
                "patterns": ["fastapi", "uvicorn", "pydantic"],
                "category": MissingModuleCategory.CORE_FRAMEWORK,
                "severity": MissingModuleSeverity.HIGH,
                "resolution": "pip install fastapi uvicorn pydantic",
                "fallback": "Use Flask or Django as alternative web framework",
            },
            "django": {
                "patterns": ["django", "rest_framework"],
                "category": MissingModuleCategory.CORE_FRAMEWORK,
                "severity": MissingModuleSeverity.HIGH,
                "resolution": "pip install django djangorestframework",
                "fallback": "Use Flask or FastAPI as alternative web framework",
            },
        }

    def _initialize_mcp_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        🏗️ Martin's Architecture: Initialize MCP server patterns

        Maps MCP server dependencies to availability checking strategies.
        """
        return {
            "context7": {
                "server_name": "context7",
                "category": MissingModuleCategory.MCP_SERVER,
                "severity": MissingModuleSeverity.MODERATE,
                "capabilities": ["pattern_recognition", "documentation_access"],
                "resolution": "Ensure Context7 MCP server is running and configured",
                "fallback": "Use local pattern matching and documentation lookup",
            },
            "sequential": {
                "server_name": "sequential",
                "category": MissingModuleCategory.MCP_SERVER,
                "severity": MissingModuleSeverity.MODERATE,
                "capabilities": ["systematic_analysis", "framework_application"],
                "resolution": "Ensure Sequential MCP server is running and configured",
                "fallback": "Use local systematic analysis frameworks",
            },
            "magic": {
                "server_name": "magic",
                "category": MissingModuleCategory.MCP_SERVER,
                "severity": MissingModuleSeverity.LOW,
                "capabilities": ["diagram_generation", "visual_enhancement"],
                "resolution": "Ensure Magic MCP server is running and configured",
                "fallback": "Skip visual enhancements or use alternative tools",
            },
        }

    def _initialize_internal_patterns(self) -> Dict[str, Dict[str, Any]]:
        """
        🏗️ Martin's Architecture: Initialize internal module patterns

        Maps ClaudeDirector internal modules to resolution strategies.
        """
        return {
            "context_engineering": {
                "patterns": ["context_engineering", "advanced_context_engine"],
                "category": MissingModuleCategory.INTERNAL_MODULE,
                "severity": MissingModuleSeverity.CRITICAL,
                "resolution": "Ensure context_engineering module is properly installed",
                "fallback": "Use basic context management",
            },
            "transparency": {
                "patterns": ["transparency", "real_mcp_integration"],
                "category": MissingModuleCategory.INTERNAL_MODULE,
                "severity": MissingModuleSeverity.HIGH,
                "resolution": "Ensure transparency system is properly configured",
                "fallback": "Use basic logging and tracking",
            },
            "ai_intelligence": {
                "patterns": ["ai_intelligence", "decision_orchestrator"],
                "category": MissingModuleCategory.INTERNAL_MODULE,
                "severity": MissingModuleSeverity.HIGH,
                "resolution": "Ensure AI intelligence modules are available",
                "fallback": "Use basic decision processing",
            },
        }

    async def analyze_module_availability(
        self,
        file_path: str,
        transparency_context: Optional[TransparencyContext] = None,
        use_mcp_enhancement: bool = True,
    ) -> ModuleAvailabilityResult:
        """
        🎯 CORE METHOD: Analyze module availability for a Python file

        Performs AST-based import analysis with optional MCP enhancement
        for intelligent dependency resolution.

        Args:
            file_path: Path to Python file to analyze
            transparency_context: Transparency tracking context
            use_mcp_enhancement: Whether to use MCP servers for enhanced analysis

        Returns:
            ModuleAvailabilityResult with comprehensive analysis
        """
        start_time = time.time()
        missing_modules = []
        available_modules = []

        try:
            # Parse Python file using AST
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            tree = ast.parse(source_code, filename=file_path)

            # Extract import statements
            import_statements = self._extract_import_statements(tree)

            # Analyze each import
            for import_info in import_statements:
                module_name = import_info["module"]
                line_number = import_info["line_number"]
                import_statement = import_info["statement"]

                # Check module availability
                is_available = self._check_module_availability(module_name)

                if is_available:
                    available_modules.append(module_name)
                else:
                    # Classify missing module
                    missing_module = self._classify_missing_module(
                        module_name, import_statement, file_path, line_number
                    )
                    missing_modules.append(missing_module)

            # Check MCP server availability
            mcp_servers_available = await self._check_mcp_server_availability()

            # Analyze framework dependencies
            framework_dependencies = self._analyze_framework_dependencies(
                import_statements, file_path
            )

            # MCP Enhancement - if available and requested
            mcp_enhanced = False
            analysis_confidence = 0.85  # Base confidence

            if use_mcp_enhancement and self.mcp_helper and missing_modules:
                try:
                    enhanced_analysis = await self._perform_mcp_enhanced_analysis(
                        missing_modules, framework_dependencies, transparency_context
                    )

                    if enhanced_analysis:
                        # Update missing modules with MCP insights
                        missing_modules = enhanced_analysis.get(
                            "enhanced_modules", missing_modules
                        )
                        analysis_confidence = enhanced_analysis.get("confidence", 0.85)
                        mcp_enhanced = True

                        self.detection_metrics["mcp_enhancements_applied"] += 1

                except Exception as e:
                    logger.warning(
                        "mcp_enhancement_failed_using_fallback",
                        error=str(e),
                        file_path=file_path,
                    )

            processing_time_ms = int((time.time() - start_time) * 1000)

            # Update metrics
            self._update_detection_metrics(
                len(import_statements), len(missing_modules), processing_time_ms
            )

            result = ModuleAvailabilityResult(
                modules_checked=len(import_statements),
                missing_modules=missing_modules,
                available_modules=available_modules,
                mcp_servers_available=mcp_servers_available,
                framework_dependencies=framework_dependencies,
                analysis_confidence=analysis_confidence,
                processing_time_ms=processing_time_ms,
                mcp_enhanced=mcp_enhanced,
            )

            logger.info(
                "module_availability_analysis_completed",
                file_path=file_path,
                modules_checked=len(import_statements),
                missing_modules=len(missing_modules),
                mcp_enhanced=mcp_enhanced,
                processing_time_ms=processing_time_ms,
            )

            return result

        except Exception as e:
            processing_time_ms = int((time.time() - start_time) * 1000)

            logger.error(
                "module_availability_analysis_failed",
                file_path=file_path,
                error=str(e),
                processing_time_ms=processing_time_ms,
            )

            # Return error result
            return ModuleAvailabilityResult(
                modules_checked=0,
                missing_modules=[],
                available_modules=[],
                mcp_servers_available={},
                framework_dependencies={},
                analysis_confidence=0.0,
                processing_time_ms=processing_time_ms,
            )

    def _extract_import_statements(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        🏗️ Martin's Architecture: Extract import statements using AST

        Analyzes Python AST to identify all import statements and their context.
        """
        import_statements = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    import_statements.append(
                        {
                            "module": alias.name,
                            "alias": alias.asname,
                            "statement": f"import {alias.name}",
                            "line_number": node.lineno,
                            "type": "import",
                        }
                    )

            elif isinstance(node, ast.ImportFrom):
                module_name = node.module or ""
                for alias in node.names:
                    full_module = (
                        f"{module_name}.{alias.name}" if module_name else alias.name
                    )
                    import_statements.append(
                        {
                            "module": module_name,
                            "imported_name": alias.name,
                            "alias": alias.asname,
                            "statement": f"from {module_name} import {alias.name}",
                            "line_number": node.lineno,
                            "type": "from_import",
                            "full_module": full_module,
                        }
                    )

        return import_statements

    def _check_module_availability(self, module_name: str) -> bool:
        """
        🏗️ Martin's Architecture: Check if a module is available for import

        Uses importlib to safely check module availability without importing.
        """
        if not module_name:
            return True

        try:
            # Handle relative imports
            if module_name.startswith("."):
                return True  # Assume relative imports are valid

            # Check if module spec exists
            spec = importlib.util.find_spec(module_name)
            return spec is not None

        except (ImportError, ValueError, AttributeError):
            return False

    def _classify_missing_module(
        self, module_name: str, import_statement: str, file_path: str, line_number: int
    ) -> MissingModuleInfo:
        """
        🏗️ Martin's Architecture: Classify missing module and suggest resolution

        Analyzes missing module context to provide intelligent classification
        and resolution suggestions.
        """
        # Check framework patterns
        for framework, info in self.framework_import_patterns.items():
            if any(pattern in module_name for pattern in info["patterns"]):
                return MissingModuleInfo(
                    module_name=module_name,
                    import_statement=import_statement,
                    category=info["category"],
                    severity=info["severity"],
                    file_path=file_path,
                    line_number=line_number,
                    suggested_resolution=info["resolution"],
                    fallback_available=True,
                    framework_context=framework,
                )

        # Check internal module patterns
        for internal, info in self.internal_module_patterns.items():
            if any(pattern in module_name for pattern in info["patterns"]):
                return MissingModuleInfo(
                    module_name=module_name,
                    import_statement=import_statement,
                    category=info["category"],
                    severity=info["severity"],
                    file_path=file_path,
                    line_number=line_number,
                    suggested_resolution=info["resolution"],
                    fallback_available=True,
                )

        # Default classification for unknown modules
        return MissingModuleInfo(
            module_name=module_name,
            import_statement=import_statement,
            category=MissingModuleCategory.PYTHON_PACKAGE,
            severity=MissingModuleSeverity.MODERATE,
            file_path=file_path,
            line_number=line_number,
            suggested_resolution=f"pip install {module_name}",
            fallback_available=False,
        )

    async def _check_mcp_server_availability(self) -> Dict[str, bool]:
        """
        🏗️ Martin's Architecture: Check MCP server availability

        Tests availability of Context7, Sequential, and Magic MCP servers.
        """
        mcp_servers = {}

        if not self.mcp_helper:
            # No MCP helper available
            for server_name in self.mcp_server_patterns.keys():
                mcp_servers[server_name] = False
            return mcp_servers

        # Check each MCP server
        for server_name, info in self.mcp_server_patterns.items():
            try:
                # Use a lightweight capability check
                result = await self.mcp_helper.call_mcp_server(
                    server_name, "status_check", query="availability test", timeout=2
                )
                mcp_servers[server_name] = result is not None

            except Exception as e:
                logger.debug(
                    "mcp_server_availability_check_failed",
                    server=server_name,
                    error=str(e),
                )
                mcp_servers[server_name] = False

        return mcp_servers

    def _analyze_framework_dependencies(
        self, import_statements: List[Dict[str, Any]], file_path: str
    ) -> Dict[str, List[str]]:
        """
        🏗️ Martin's Architecture: Analyze framework-specific dependencies

        Groups imports by detected frameworks for dependency analysis.
        """
        framework_deps = {}

        # Use framework detector if available
        if FRAMEWORK_DETECTOR_AVAILABLE and self.framework_detector:
            try:
                # Analyze file content for framework patterns
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Get framework detection results
                detected_frameworks = self.framework_detector.detect_frameworks(content)

                for framework in detected_frameworks:
                    framework_deps[framework] = []

                    # Map imports to frameworks
                    for import_info in import_statements:
                        module_name = import_info["module"]

                        # Check if import belongs to this framework
                        if framework in self.framework_import_patterns:
                            patterns = self.framework_import_patterns[framework][
                                "patterns"
                            ]
                            if any(pattern in module_name for pattern in patterns):
                                framework_deps[framework].append(module_name)

            except Exception as e:
                logger.warning(
                    "framework_dependency_analysis_failed",
                    file_path=file_path,
                    error=str(e),
                )

        return framework_deps

    async def _perform_mcp_enhanced_analysis(
        self,
        missing_modules: List[MissingModuleInfo],
        framework_dependencies: Dict[str, List[str]],
        transparency_context: Optional[TransparencyContext],
    ) -> Optional[Dict[str, Any]]:
        """
        🚀 MCP Enhancement: Perform enhanced analysis using MCP servers

        Uses Sequential and Context7 MCP servers for intelligent dependency analysis.
        """
        if not self.decision_pipeline or not transparency_context:
            return None

        try:
            # Create decision context for MCP analysis
            decision_context = DecisionContext(
                message=f"Analyze missing modules: {[m.module_name for m in missing_modules]}",
                stakeholder_scope="development_team",
                persona="martin",  # Technical architecture persona
                complexity=DecisionComplexity.MODERATE,
                detected_frameworks=list(framework_dependencies.keys()),
                metadata={
                    "analysis_type": "missing_modules",
                    "module_count": len(missing_modules),
                    "frameworks": framework_dependencies,
                },
            )

            # Execute MCP enhanced analysis
            pipeline_result = await self.decision_pipeline.execute_pipeline(
                decision_context, transparency_context
            )

            if pipeline_result.success:
                # Extract enhanced insights
                enhanced_modules = self._process_mcp_insights(
                    missing_modules, pipeline_result
                )

                return {
                    "enhanced_modules": enhanced_modules,
                    "confidence": pipeline_result.confidence_score,
                    "mcp_insights": pipeline_result.framework_insights,
                    "recommendations": pipeline_result.final_recommendations,
                }

        except Exception as e:
            logger.warning(
                "mcp_enhanced_analysis_failed",
                error=str(e),
                module_count=len(missing_modules),
            )

        return None

    def _process_mcp_insights(
        self,
        missing_modules: List[MissingModuleInfo],
        pipeline_result: PipelineExecutionResult,
    ) -> List[MissingModuleInfo]:
        """
        🚀 MCP Enhancement: Process MCP insights to enhance missing module info

        Enriches missing module information with MCP-generated insights.
        """
        enhanced_modules = []

        for module in missing_modules:
            enhanced_module = module

            # Extract relevant insights from MCP pipeline
            if pipeline_result.framework_insights:
                # Check for framework-specific recommendations
                for stage_name, insights in pipeline_result.framework_insights.items():
                    if isinstance(insights, list):
                        for insight in insights:
                            if module.module_name in str(insight):
                                # Enhance resolution suggestion with MCP insight
                                enhanced_module.suggested_resolution += (
                                    f" | MCP Insight: {insight}"
                                )

            # Check final recommendations
            for recommendation in pipeline_result.final_recommendations:
                if module.module_name in recommendation:
                    enhanced_module.suggested_resolution += (
                        f" | Recommended: {recommendation}"
                    )

            enhanced_modules.append(enhanced_module)

        return enhanced_modules

    def _update_detection_metrics(
        self, modules_checked: int, missing_count: int, processing_time_ms: int
    ):
        """🏗️ Martin: Update detection performance metrics"""
        self.detection_metrics["analyses_performed"] += 1
        self.detection_metrics["modules_detected"] += modules_checked

        # Update average processing time
        current_avg = self.detection_metrics["avg_processing_time_ms"]
        count = self.detection_metrics["analyses_performed"]
        new_avg = ((current_avg * (count - 1)) + processing_time_ms) / count
        self.detection_metrics["avg_processing_time_ms"] = new_avg

    def get_detection_metrics(self) -> Dict[str, Any]:
        """Get current detection performance metrics"""
        return self.detection_metrics.copy()

    async def analyze_directory_modules(
        self,
        directory_path: str,
        recursive: bool = True,
        transparency_context: Optional[TransparencyContext] = None,
    ) -> Dict[str, ModuleAvailabilityResult]:
        """
        🎯 BULK ANALYSIS: Analyze module availability for all Python files in directory

        Performs batch analysis with intelligent resource management.
        """
        results = {}
        directory = Path(directory_path)

        # Find all Python files
        if recursive:
            python_files = list(directory.rglob("*.py"))
        else:
            python_files = list(directory.glob("*.py"))

        logger.info(
            "directory_module_analysis_started",
            directory=directory_path,
            file_count=len(python_files),
            recursive=recursive,
        )

        # Analyze each file
        for py_file in python_files:
            try:
                result = await self.analyze_module_availability(
                    str(py_file), transparency_context, use_mcp_enhancement=True
                )
                results[str(py_file)] = result

            except Exception as e:
                logger.error(
                    "file_analysis_failed", file_path=str(py_file), error=str(e)
                )

        logger.info(
            "directory_module_analysis_completed",
            directory=directory_path,
            files_analyzed=len(results),
            total_files=len(python_files),
        )

        return results


# Factory function for easy integration
def create_mcp_missing_modules_detection_engine(
    mcp_helper: Optional[RealMCPIntegrationHelper] = None,
    framework_detector: Optional[FrameworkDetector] = None,
    decision_pipeline: Optional[MCPEnhancedDecisionPipeline] = None,
) -> MCPMissingModulesDetectionEngine:
    """
    🏗️ Martin's Architecture: Factory for MCP Missing Modules Detection Engine

    Creates detection engine with optional MCP enhancement capabilities.
    """
    engine = MCPMissingModulesDetectionEngine(
        mcp_helper=mcp_helper,
        framework_detector=framework_detector,
        decision_pipeline=decision_pipeline,
    )

    logger.info(
        "mcp_missing_modules_detection_engine_created",
        mcp_available=MCP_AVAILABLE,
        framework_detector_available=FRAMEWORK_DETECTOR_AVAILABLE,
    )

    return engine
