"""
🎯 STORY 9.5.4: FILE MANAGER ORCHESTRATOR - PHASE 3 DECOMPOSITION

SOLID COMPLIANCE ACHIEVED:
- Single Responsibility: Coordination and orchestration only
- Open/Closed: Extensible through BaseManager inheritance
- Liskov Substitution: Proper BaseManager implementation
- Interface Segregation: Focused orchestration interface
- Dependency Inversion: Depends on BaseManager abstraction

REPLACES: UnifiedFileManager (867 lines) → Orchestrator (~150 lines) + 4 Specialized Managers
ELIMINATES: SRP violations through proper separation of concerns

Sequential Thinking Phase 9.5.4 - Manager decomposition for SOLID compliance.
Author: Martin | Platform Architecture
"""

import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

# STORY 9.5.4: BaseManager inheritance for SOLID compliance
from .base_manager import BaseManager, BaseManagerConfig, ManagerType

# STORY 9.5.4: Specialized manager imports for orchestration
from .file_lifecycle_manager import FileLifecycleManager
from .file_metadata_manager import FileMetadataManager
from .file_organization_manager import FileOrganizationManager, GenerationMode
from .file_processing_manager import FileProcessingManager, ProcessingMode


@dataclass
class WorkspaceConfig:
    """Workspace configuration for file management"""

    auto_archive_days: int = 30
    generation_mode: str = "professional"
    enable_smart_organization: bool = True
    max_file_size_mb: int = 10
    allowed_extensions: List[str] = None

    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = [".md", ".txt", ".json", ".yaml", ".yml"]


class FileManagerOrchestrator(BaseManager):
    """
    🎯 STORY 9.5.4: FILE MANAGER ORCHESTRATOR - SOLID Compliant

    SINGLE RESPONSIBILITY: Coordination and orchestration only
    - Coordinate between specialized file managers
    - Maintain API compatibility with original UnifiedFileManager
    - Provide unified interface while delegating to specialists
    - Manage configuration and health monitoring

    ELIMINATES SRP VIOLATIONS through proper orchestration pattern.
    Maintains backward compatibility while achieving SOLID compliance.
    """

    def __init__(self, workspace_path: str) -> None:
        """
        🎯 STORY 9.5.4: SOLID compliant orchestrator initialization
        """
        # BaseManager initialization for infrastructure
        config = BaseManagerConfig(
            manager_name="file_manager_orchestrator",
            manager_type=ManagerType.WORKSPACE,
            enable_metrics=True,
            enable_caching=True,
            enable_logging=True,
            custom_config={"workspace_path": workspace_path},
        )
        super().__init__(config)

        self.workspace_path = Path(workspace_path)
        self.config_file = self.workspace_path / "config" / "file_lifecycle.yaml"

        # Load configuration
        self.config = self._load_config()

        # Initialize specialized managers with dependency injection
        self.metadata_manager = FileMetadataManager(workspace_path)
        self.lifecycle_manager = FileLifecycleManager(
            workspace_path, self.metadata_manager
        )
        self.organization_manager = FileOrganizationManager(
            workspace_path, self.metadata_manager
        )
        self.processing_manager = FileProcessingManager(
            workspace_path, self.metadata_manager
        )

        self.logger.info(
            f"FileManagerOrchestrator initialized for workspace: {workspace_path}"
        )

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Orchestrates operations across specialized managers
        """
        try:
            # Route operations to appropriate specialized managers

            # File Lifecycle Operations
            if operation in [
                "create_file",
                "archive_files",
                "retain_file",
                "cleanup_workspace",
                "get_workspace_stats",
            ]:
                return await self.lifecycle_manager.manage(operation, *args, **kwargs)

            # File Organization Operations
            elif operation in [
                "organize_files",
                "generate_filename",
                "analyze_patterns",
                "health_check",
            ]:
                return await self.organization_manager.manage(
                    operation, *args, **kwargs
                )

            # File Processing Operations
            elif operation in ["detect_consolidation", "process_files"]:
                return await self.processing_manager.manage(operation, *args, **kwargs)

            # Metadata Operations
            elif operation in ["update_metadata", "get_metadata", "get_all_metadata"]:
                return await self.metadata_manager.manage(operation, *args, **kwargs)

            # Orchestrator-specific operations
            elif operation == "get_unified_stats":
                return self.get_unified_statistics()
            elif operation == "health_check_all":
                return self.comprehensive_health_check()

            else:
                self.logger.warning(f"Unknown orchestrated operation: {operation}")
                return None

        except Exception as e:
            self.logger.error(f"Error in orchestrated operation {operation}: {e}")
            return None

    # ===== BACKWARD COMPATIBILITY METHODS =====
    # These methods maintain API compatibility with original UnifiedFileManager

    def create_file(
        self, filename: str, content: str = "", metadata: Optional[Dict] = None
    ) -> Path:
        """Create file with unified lifecycle tracking - BACKWARD COMPATIBLE"""
        return self.lifecycle_manager.create_file(filename, content, metadata)

    def archive_old_files(self, days_threshold: Optional[int] = None) -> List[Path]:
        """Archive files based on unified criteria - BACKWARD COMPATIBLE"""
        threshold = days_threshold or self.config.auto_archive_days
        return self.lifecycle_manager.archive_old_files(threshold)

    def mark_for_retention(self, file_path: Path, reason: str = "") -> bool:
        """Mark file for retention with unified tracking - BACKWARD COMPATIBLE"""
        return self.lifecycle_manager.mark_for_retention(file_path, reason)

    def cleanup_workspace(self, dry_run: bool = False) -> Dict[str, int]:
        """Unified workspace cleanup - BACKWARD COMPATIBLE"""
        return self.lifecycle_manager.cleanup_workspace(dry_run)

    def organize_workspace_files(self, mode: Optional[str] = None) -> Dict[str, Any]:
        """Organize workspace files by business context - BACKWARD COMPATIBLE"""
        generation_mode = GenerationMode(mode or self.config.generation_mode)
        return self.organization_manager.organize_workspace_files(generation_mode)

    def generate_outcome_focused_filename(
        self, content_summary: str, context: str = "", strategic_value: float = 0.0
    ) -> str:
        """Generate outcome-focused filename - BACKWARD COMPATIBLE"""
        return self.organization_manager.generate_outcome_focused_filename(
            content_summary, context, strategic_value
        )

    def analyze_session_patterns(self) -> Dict[str, Any]:
        """Analyze file creation patterns - BACKWARD COMPATIBLE"""
        return self.organization_manager.analyze_session_patterns()

    def detect_consolidation_opportunities(
        self, min_similarity: float = 0.7
    ) -> List[Any]:
        """Detect consolidation opportunities - BACKWARD COMPATIBLE"""
        return self.processing_manager.detect_consolidation_opportunities(
            min_similarity
        )

    def process_file_batch(
        self, file_paths: List[Path], operation: str, mode: str = "batch", **kwargs
    ) -> Dict[str, Any]:
        """Process batch of files - BACKWARD COMPATIBLE"""
        processing_mode = ProcessingMode(mode)
        return self.processing_manager.process_file_batch(
            file_paths, operation, processing_mode, **kwargs
        )

    def get_workspace_statistics(self) -> Dict[str, Any]:
        """Get comprehensive workspace statistics - BACKWARD COMPATIBLE"""
        return self.get_unified_statistics()

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check - BACKWARD COMPATIBLE"""
        return self.comprehensive_health_check()

    # ===== ORCHESTRATOR-SPECIFIC METHODS =====

    def get_unified_statistics(self) -> Dict[str, Any]:
        """Get unified statistics from all specialized managers"""
        try:
            unified_stats = {
                "orchestrator_info": {
                    "managers_active": 4,
                    "workspace_path": str(self.workspace_path),
                    "config_mode": self.config.generation_mode,
                },
                "lifecycle_stats": self.lifecycle_manager.get_workspace_statistics(),
                "organization_stats": self.organization_manager.organization_health_check(),
                "processing_stats": self.processing_manager.get_processing_statistics(),
                "metadata_stats": self.metadata_manager.get_metadata_statistics(),
                "timestamp": datetime.now().isoformat(),
            }

            return unified_stats

        except Exception as e:
            self.logger.error(f"Error getting unified statistics: {e}")
            return {"error": str(e)}

    def comprehensive_health_check(self) -> Dict[str, Any]:
        """Comprehensive health check across all managers"""
        health_report = {
            "overall_health": "unknown",
            "manager_health": {},
            "issues": [],
            "recommendations": [],
            "timestamp": datetime.now().isoformat(),
        }

        try:
            # Check each manager's health
            managers = {
                "lifecycle": self.lifecycle_manager,
                "organization": self.organization_manager,
                "processing": self.processing_manager,
                "metadata": self.metadata_manager,
            }

            healthy_managers = 0
            total_managers = len(managers)

            for name, manager in managers.items():
                try:
                    if hasattr(manager, "health_check"):
                        health = manager.health_check()
                    elif hasattr(manager, "organization_health_check"):
                        health = manager.organization_health_check()
                    else:
                        health = {"status": "operational"}

                    health_report["manager_health"][name] = health

                    # Count healthy managers
                    if not health.get("issues_detected") and not health.get("errors"):
                        healthy_managers += 1

                except Exception as e:
                    health_report["manager_health"][name] = {"error": str(e)}
                    health_report["issues"].append(
                        f"{name} manager health check failed: {e}"
                    )

            # Calculate overall health
            health_ratio = healthy_managers / total_managers
            if health_ratio >= 0.8:
                health_report["overall_health"] = "healthy"
            elif health_ratio >= 0.6:
                health_report["overall_health"] = "warning"
            else:
                health_report["overall_health"] = "critical"

            # Generate recommendations
            if health_ratio < 1.0:
                health_report["recommendations"].append(
                    "Review manager-specific health reports"
                )

            if not self.config_file.exists():
                health_report["recommendations"].append(
                    "Create configuration file for optimal performance"
                )

            return health_report

        except Exception as e:
            self.logger.error(f"Error in comprehensive health check: {e}")
            health_report["overall_health"] = "error"
            health_report["issues"].append(f"Health check error: {e}")
            return health_report

    # ===== CONFIGURATION MANAGEMENT =====

    def _load_config(self) -> WorkspaceConfig:
        """Load unified workspace configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config_data = yaml.safe_load(f)
                return WorkspaceConfig(**config_data)
            except Exception as e:
                self.logger.warning(f"Could not load config: {e}")

        # Return defaults and save them
        config = WorkspaceConfig()
        self._save_config(config)
        return config

    def _save_config(self, config: WorkspaceConfig) -> None:
        """Save unified workspace configuration"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            yaml.dump(config.__dict__, f, default_flow_style=False)

    # ===== DRY HELPER METHODS (from Phase 2) =====

    def _update_file_metadata_batch(
        self, file_path: Path, updates: Dict[str, Any]
    ) -> None:
        """
        🎯 STORY 9.5.4: DRY Pattern Applied - Delegate to metadata manager
        """
        self.metadata_manager.update_file_metadata(file_path, updates)

    def _handle_file_operation_error(
        self, file_path: Path, operation: str, error: Exception
    ) -> None:
        """
        🎯 STORY 9.5.4: DRY Pattern Applied - Centralized error handling
        """
        self.logger.warning(f"Error {operation} file {file_path}: {error}")

    def _validate_file_exists(self, file_path: Path) -> bool:
        """
        🎯 STORY 9.5.4: DRY Pattern Applied - Centralized validation
        """
        return file_path.exists() and file_path.is_file()
