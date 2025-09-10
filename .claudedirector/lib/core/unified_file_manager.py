"""
🎯 STORY 9.5.4: UNIFIED FILE MANAGER - SOLID Compliant Orchestration Proxy

PHASE 3 DECOMPOSITION COMPLETE:
- Original 867-line mega-class → 5 SOLID-compliant specialized managers
- FileLifecycleManager: File lifecycle operations (~200 lines)
- FileMetadataManager: Metadata operations (~150 lines)
- FileOrganizationManager: Organization operations (~200 lines)
- FileProcessingManager: Processing operations (~200 lines)
- FileManagerOrchestrator: Coordination layer (~150 lines)

SOLID COMPLIANCE ACHIEVED:
- Single Responsibility: Each manager has one focused responsibility
- Open/Closed: Extensible through BaseManager inheritance
- Liskov Substitution: Proper BaseManager implementations
- Interface Segregation: Focused interfaces per responsibility
- Dependency Inversion: All depend on BaseManager abstraction

BACKWARD COMPATIBILITY: 100% API compatibility maintained through orchestration.
Sequential Thinking Phase 9.5.4 - SOLID compliance through systematic decomposition.
Author: Martin | Platform Architecture
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# STORY 9.5.4: BaseManager inheritance for SOLID compliance
from .base_manager import BaseManager, BaseManagerConfig, ManagerType
from .file_manager_orchestrator import FileManagerOrchestrator


class UnifiedFileManager(BaseManager):
    """
    🎯 STORY 9.5.4: UNIFIED FILE MANAGER - SOLID Compliant Orchestration Proxy

    BACKWARD COMPATIBILITY LAYER:
    Maintains 100% API compatibility with original UnifiedFileManager while delegating
    to SOLID-compliant specialized managers through FileManagerOrchestrator.

    ARCHITECTURAL PATTERN:
    - Delegates all operations to FileManagerOrchestrator
    - Maintains original method signatures for backward compatibility
    - Provides seamless transition from monolithic to SOLID architecture
    - Zero breaking changes for existing code

    SOLID COMPLIANCE: Achieved through delegation to specialized managers.
    """

    def __init__(self, workspace_path: str) -> None:
        """
        🎯 STORY 9.5.4: SOLID compliant initialization via orchestration
        """
        # BaseManager initialization for compatibility
        config = BaseManagerConfig(
            manager_name="unified_file_manager_proxy",
            manager_type=ManagerType.WORKSPACE,
            enable_metrics=True,
            enable_caching=True,
            enable_logging=True,
            custom_config={"workspace_path": workspace_path},
        )
        super().__init__(config)

        # Delegate to SOLID-compliant orchestrator
        self.orchestrator = FileManagerOrchestrator(workspace_path)

        # Maintain backward compatibility properties
        self.workspace_path = Path(workspace_path)
        self.config_file = self.workspace_path / "config" / "file_lifecycle.yaml"
        self.metadata_file = (
            self.workspace_path / ".claudedirector" / "file_metadata.json"
        )

        self.logger.info(
            f"UnifiedFileManager (SOLID Proxy) initialized for workspace: {workspace_path}"
        )

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        🎯 STORY 9.5.4: Delegates to SOLID-compliant orchestrator
        """
        return await self.orchestrator.manage(operation, *args, **kwargs)

    # ===== BACKWARD COMPATIBILITY DELEGATION METHODS =====
    # 🎯 STORY 9.5.4: All methods delegate to SOLID-compliant orchestrator

    def create_file(
        self, filename: str, content: str = "", metadata: Optional[Dict] = None
    ) -> Path:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.create_file(filename, content, metadata)

    def archive_old_files(self, days_threshold: Optional[int] = None) -> List[Path]:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.archive_old_files(days_threshold)

    def mark_for_retention(self, file_path: Path, reason: str = "") -> bool:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.mark_for_retention(file_path, reason)

    def cleanup_workspace(self, dry_run: bool = False) -> Dict[str, int]:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.cleanup_workspace(dry_run)

    def organize_workspace_files(self, mode: Optional[str] = None) -> Dict[str, Any]:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.organize_workspace_files(mode)

    def generate_outcome_focused_filename(
        self, content_summary: str, context: str = "", strategic_value: float = 0.0
    ) -> str:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.generate_outcome_focused_filename(
            content_summary, context, strategic_value
        )

    def analyze_session_patterns(self) -> Dict[str, Any]:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.analyze_session_patterns()

    def detect_consolidation_opportunities(
        self, min_similarity: float = 0.7
    ) -> List[Any]:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.detect_consolidation_opportunities(min_similarity)

    def process_file_batch(
        self, file_paths: List[Path], operation: str, mode: str = "batch", **kwargs
    ) -> Dict[str, Any]:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.process_file_batch(
            file_paths, operation, mode, **kwargs
        )

    def get_workspace_statistics(self) -> Dict[str, Any]:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.get_workspace_statistics()

    def health_check(self) -> Dict[str, Any]:
        """🎯 STORY 9.5.4: Delegate to SOLID-compliant orchestrator"""
        return self.orchestrator.health_check()

    # ===== STORY 9.5.4: DRY PATTERN EXTRACTION - PHASE 2 HELPERS =====
    # Maintained for backward compatibility, but delegate to orchestrator

    def _update_file_metadata_batch(
        self, file_path: Path, updates: Dict[str, Any]
    ) -> None:
        """🎯 STORY 9.5.4: Delegate to orchestrator metadata manager"""
        self.orchestrator._update_file_metadata_batch(file_path, updates)

    def _handle_file_operation_error(
        self, file_path: Path, operation: str, error: Exception
    ) -> None:
        """🎯 STORY 9.5.4: Delegate to orchestrator error handling"""
        self.orchestrator._handle_file_operation_error(file_path, operation, error)

    def _validate_file_exists(self, file_path: Path) -> bool:
        """🎯 STORY 9.5.4: Delegate to orchestrator validation"""
        return self.orchestrator._validate_file_exists(file_path)


# ===== FACTORY FUNCTIONS FOR BACKWARD COMPATIBILITY =====


def create_unified_file_manager(workspace_path: str) -> UnifiedFileManager:
    """Factory function for creating unified file manager"""
    return UnifiedFileManager(workspace_path)


def create_file_lifecycle_manager(workspace_path: str) -> UnifiedFileManager:
    """Backward compatibility factory for FileLifecycleManager"""
    return UnifiedFileManager(workspace_path)


def create_smart_file_organizer(workspace_path: str) -> UnifiedFileManager:
    """Backward compatibility factory for SmartFileOrganizer"""
    return UnifiedFileManager(workspace_path)


def create_file_organizer_processor(workspace_path: str) -> UnifiedFileManager:
    """Backward compatibility factory for FileOrganizerProcessor"""
    return UnifiedFileManager(workspace_path)
