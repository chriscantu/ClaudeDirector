"""
🎯 STORY 9.5.4: FILE LIFECYCLE MANAGER - PHASE 3 DECOMPOSITION

SOLID COMPLIANCE ACHIEVED:
- Single Responsibility: File lifecycle operations only (create, archive, retain, cleanup)
- Open/Closed: Extensible through BaseManager inheritance
- Liskov Substitution: Proper BaseManager implementation
- Interface Segregation: Focused lifecycle interface
- Dependency Inversion: Depends on BaseManager abstraction

EXTRACTED FROM: UnifiedFileManager (867 lines) → Specialized Manager (~200 lines)
ELIMINATES: SRP violations by focusing solely on file lifecycle operations

Sequential Thinking Phase 9.5.4 - Manager decomposition for SOLID compliance.
Author: Martin | Platform Architecture
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# STORY 9.5.4: BaseManager inheritance for SOLID compliance
from .base_manager import BaseManager, BaseManagerConfig, ManagerType


class FileRetentionStatus(Enum):
    """File retention status for lifecycle management"""

    ACTIVE = "active"
    ARCHIVED = "archived"
    RETAINED = "retained"
    SCHEDULED_DELETION = "scheduled_deletion"


@dataclass
class FileMetadata:
    """File metadata for lifecycle tracking"""

    created_at: datetime
    retention_status: FileRetentionStatus = FileRetentionStatus.ACTIVE
    tags: List[str] = None
    business_context: Optional[str] = None
    strategic_value: float = 0.0
    retention_reason: Optional[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class FileLifecycleManager(BaseManager):
    """
    🎯 STORY 9.5.4: FILE LIFECYCLE MANAGER - SOLID Compliant

    SINGLE RESPONSIBILITY: File lifecycle operations only
    - File creation with metadata tracking
    - Archive management based on age/criteria
    - Retention marking and management
    - Workspace cleanup operations

    ELIMINATES SRP VIOLATIONS from UnifiedFileManager mega-class.
    Focused interface for lifecycle operations only.
    """

    def __init__(self, workspace_path: str, metadata_manager=None) -> None:
        """
        🎯 STORY 9.5.4: SOLID compliant initialization
        """
        # BaseManager initialization for infrastructure
        config = BaseManagerConfig(
            manager_name="file_lifecycle_manager",
            manager_type=ManagerType.WORKSPACE,
            enable_metrics=True,
            enable_caching=True,
            enable_logging=True,
            custom_config={"workspace_path": workspace_path},
        )
        super().__init__(config)

        self.workspace_path = Path(workspace_path)
        self.metadata_manager = (
            metadata_manager  # Dependency injection for metadata ops
        )

        self.logger.info(
            f"FileLifecycleManager initialized for workspace: {workspace_path}"
        )

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Focused lifecycle operation delegation
        """
        if operation == "create_file":
            return self.create_file(*args, **kwargs)
        elif operation == "archive_files":
            return self.archive_old_files(*args, **kwargs)
        elif operation == "retain_file":
            return self.mark_for_retention(*args, **kwargs)
        elif operation == "cleanup_workspace":
            return self.cleanup_workspace(*args, **kwargs)
        elif operation == "get_workspace_stats":
            return self.get_workspace_statistics()
        else:
            self.logger.warning(f"Unknown lifecycle operation: {operation}")
            return None

    def create_file(
        self, filename: str, content: str = "", metadata: Optional[Dict] = None
    ) -> Path:
        """Create file with lifecycle tracking"""
        file_path = self.workspace_path / filename

        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        file_path.write_text(content)

        # Create lifecycle metadata
        file_metadata = FileMetadata(
            created_at=datetime.now(),
            retention_status=FileRetentionStatus.ACTIVE,
            tags=metadata.get("tags", []) if metadata else [],
            business_context=metadata.get("business_context") if metadata else None,
            strategic_value=metadata.get("strategic_value", 0.0) if metadata else 0.0,
        )

        # Store metadata via metadata manager (dependency injection)
        if self.metadata_manager:
            self.metadata_manager.update_file_metadata(
                file_path, file_metadata.__dict__
            )

        self.logger.info(f"Created file with lifecycle tracking: {file_path}")
        return file_path

    def archive_old_files(self, days_threshold: int = 30) -> List[Path]:
        """Archive files based on age criteria"""
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        archived_files = []

        if not self.metadata_manager:
            self.logger.warning("No metadata manager available for archival")
            return archived_files

        metadata_store = self.metadata_manager.get_all_metadata()

        for file_path_str, metadata_dict in metadata_store.items():
            file_path = Path(file_path_str)
            if not self._validate_file_exists(file_path):
                continue

            created_at = datetime.fromisoformat(metadata_dict["created_at"])
            if (
                created_at < cutoff_date
                and metadata_dict["retention_status"]
                == FileRetentionStatus.ACTIVE.value
            ):
                # Move to archive
                archive_path = self._move_to_archive(file_path)
                if archive_path:
                    # Update metadata via metadata manager
                    self.metadata_manager.update_file_metadata(
                        file_path,
                        {"retention_status": FileRetentionStatus.ARCHIVED.value},
                    )
                    archived_files.append(archive_path)

        self.logger.info(f"Archived {len(archived_files)} files")
        return archived_files

    def mark_for_retention(self, file_path: Path, reason: str = "") -> bool:
        """Mark file for retention with lifecycle tracking"""
        if not self.metadata_manager:
            self.logger.warning("No metadata manager available for retention")
            return False

        # Update metadata via metadata manager
        updates = {
            "retention_status": FileRetentionStatus.RETAINED.value,
            "retention_reason": reason,
        }
        success = self.metadata_manager.update_file_metadata(file_path, updates)

        if success:
            self.logger.info(f"Marked for retention: {file_path}")
        return success

    def cleanup_workspace(self, dry_run: bool = False) -> Dict[str, int]:
        """Lifecycle-focused workspace cleanup"""
        stats = {
            "files_analyzed": 0,
            "files_archived": 0,
            "space_saved_mb": 0,
        }

        # Analyze all workspace files for lifecycle operations
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                stats["files_analyzed"] += 1

                # Check for archival candidates
                if self._should_archive(file_path):
                    if not dry_run:
                        archive_path = self._move_to_archive(file_path)
                        if archive_path:
                            stats["files_archived"] += 1
                            # Estimate space saved (simplified)
                            try:
                                stats["space_saved_mb"] += file_path.stat().st_size / (
                                    1024 * 1024
                                )
                            except OSError:
                                pass

        self.logger.info(f"Workspace cleanup completed: {stats}")
        return stats

    def get_workspace_statistics(self) -> Dict[str, Any]:
        """Get lifecycle-focused workspace statistics"""
        stats = {
            "total_files": 0,
            "active_files": 0,
            "archived_files": 0,
            "retained_files": 0,
            "total_size_mb": 0,
        }

        # Count files by lifecycle status
        if self.metadata_manager:
            metadata_store = self.metadata_manager.get_all_metadata()
            for file_path_str, metadata_dict in metadata_store.items():
                file_path = Path(file_path_str)
                if self._validate_file_exists(file_path):
                    stats["total_files"] += 1

                    # Categorize by retention status
                    status = metadata_dict.get(
                        "retention_status", FileRetentionStatus.ACTIVE.value
                    )
                    if status == FileRetentionStatus.ACTIVE.value:
                        stats["active_files"] += 1
                    elif status == FileRetentionStatus.ARCHIVED.value:
                        stats["archived_files"] += 1
                    elif status == FileRetentionStatus.RETAINED.value:
                        stats["retained_files"] += 1

                    # Calculate size
                    try:
                        stats["total_size_mb"] += file_path.stat().st_size / (
                            1024 * 1024
                        )
                    except OSError:
                        pass

        return stats

    # ===== PRIVATE HELPER METHODS =====

    def _validate_file_exists(self, file_path: Path) -> bool:
        """Validate file existence for lifecycle operations"""
        return file_path.exists() and file_path.is_file()

    def _should_archive(self, file_path: Path) -> bool:
        """Determine if file should be archived based on lifecycle criteria"""
        # Simple heuristic - files older than 90 days and not accessed recently
        try:
            stat = file_path.stat()
            age_days = (datetime.now().timestamp() - stat.st_mtime) / (24 * 3600)
            return age_days > 90
        except OSError:
            return False

    def _move_to_archive(self, file_path: Path) -> Optional[Path]:
        """Move file to archive location"""
        try:
            # Create archive directory structure
            archive_dir = (
                self.workspace_path / "archived" / datetime.now().strftime("%Y/%m")
            )
            archive_dir.mkdir(parents=True, exist_ok=True)

            # Move file to archive
            archive_path = archive_dir / file_path.name
            file_path.rename(archive_path)

            self.logger.info(f"Moved to archive: {file_path} → {archive_path}")
            return archive_path
        except Exception as e:
            self.logger.error(f"Failed to archive {file_path}: {e}")
            return None
