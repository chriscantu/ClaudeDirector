"""
🎯 STORY 9.5.4: FILE METADATA MANAGER - PHASE 3 DECOMPOSITION

SOLID COMPLIANCE ACHIEVED:
- Single Responsibility: File metadata operations only (load, save, update, query)
- Open/Closed: Extensible through BaseManager inheritance
- Liskov Substitution: Proper BaseManager implementation
- Interface Segregation: Focused metadata interface
- Dependency Inversion: Depends on BaseManager abstraction

EXTRACTED FROM: UnifiedFileManager (867 lines) → Specialized Manager (~150 lines)
ELIMINATES: SRP violations by focusing solely on metadata operations

Sequential Thinking Phase 9.5.4 - Manager decomposition for SOLID compliance.
Author: Martin | Platform Architecture
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# STORY 9.5.4: BaseManager inheritance for SOLID compliance
from .base_manager import BaseManager, BaseManagerConfig, ManagerType
from .file_lifecycle_manager import FileMetadata


class FileMetadataManager(BaseManager):
    """
    🎯 STORY 9.5.4: FILE METADATA MANAGER - SOLID Compliant

    SINGLE RESPONSIBILITY: File metadata operations only
    - Load and save metadata store
    - Update file metadata with batch operations
    - Query metadata by various criteria
    - Ensure metadata consistency and validation

    ELIMINATES SRP VIOLATIONS from UnifiedFileManager mega-class.
    Focused interface for metadata operations only.
    """

    def __init__(self, workspace_path: str) -> None:
        """
        🎯 STORY 9.5.4: SOLID compliant initialization
        """
        # BaseManager initialization for infrastructure
        config = BaseManagerConfig(
            manager_name="file_metadata_manager",
            manager_type=ManagerType.WORKSPACE,
            enable_metrics=True,
            enable_caching=True,
            enable_logging=True,
            custom_config={"workspace_path": workspace_path},
        )
        super().__init__(config)

        self.workspace_path = Path(workspace_path)
        self.metadata_file = (
            self.workspace_path / ".claudedirector" / "file_metadata.json"
        )

        # Load metadata store
        self.metadata_store = self._load_metadata()

        self.logger.info(
            f"FileMetadataManager initialized for workspace: {workspace_path}"
        )

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Focused metadata operation delegation
        """
        if operation == "update_metadata":
            return self.update_file_metadata(*args, **kwargs)
        elif operation == "get_metadata":
            return self.get_file_metadata(*args, **kwargs)
        elif operation == "get_all_metadata":
            return self.get_all_metadata()
        elif operation == "save_metadata":
            return self.save_metadata()
        elif operation == "query_metadata":
            return self.query_metadata(*args, **kwargs)
        elif operation == "ensure_metadata":
            return self.ensure_metadata_exists(*args, **kwargs)
        else:
            self.logger.warning(f"Unknown metadata operation: {operation}")
            return None

    def update_file_metadata(self, file_path: Path, updates: Dict[str, Any]) -> bool:
        """
        🎯 STORY 9.5.4: DRY Pattern Applied - Centralized metadata updates

        Update file metadata with validation and consistency checks.
        Replaces duplicate patterns from original UnifiedFileManager.
        """
        try:
            file_path_str = str(file_path)

            # Ensure metadata exists
            if file_path_str not in self.metadata_store:
                self._ensure_metadata_exists(file_path)

            # Apply updates with validation
            for key, value in updates.items():
                if self._validate_metadata_field(key, value):
                    self.metadata_store[file_path_str][key] = value
                else:
                    self.logger.warning(
                        f"Invalid metadata field {key}={value} for {file_path}"
                    )

            # Save changes
            self.save_metadata()
            self.logger.debug(f"Updated metadata for {file_path}: {updates}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating metadata for {file_path}: {e}")
            return False

    def get_file_metadata(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific file"""
        file_path_str = str(file_path)
        if file_path_str in self.metadata_store:
            return self.metadata_store[file_path_str].copy()
        return None

    def get_all_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Get all metadata store (copy for safety)"""
        return self.metadata_store.copy()

    def query_metadata(self, **criteria) -> List[Dict[str, Any]]:
        """Query metadata by criteria"""
        results = []

        for file_path_str, metadata in self.metadata_store.items():
            match = True
            for key, value in criteria.items():
                if key not in metadata or metadata[key] != value:
                    match = False
                    break

            if match:
                result = metadata.copy()
                result["file_path"] = file_path_str
                results.append(result)

        return results

    def ensure_metadata_exists(self, file_path: Path) -> bool:
        """Ensure metadata exists for a file"""
        return self._ensure_metadata_exists(file_path)

    def save_metadata(self) -> bool:
        """Save metadata store to disk"""
        try:
            self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.metadata_file, "w") as f:
                json.dump(self.metadata_store, f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Error saving metadata: {e}")
            return False

    def get_metadata_statistics(self) -> Dict[str, Any]:
        """Get metadata store statistics"""
        stats = {
            "total_files": len(self.metadata_store),
            "metadata_file_size_kb": 0,
            "retention_status_counts": {},
            "business_context_counts": {},
        }

        # Calculate metadata file size
        try:
            if self.metadata_file.exists():
                stats["metadata_file_size_kb"] = (
                    self.metadata_file.stat().st_size / 1024
                )
        except OSError:
            pass

        # Analyze metadata content
        for metadata in self.metadata_store.values():
            # Count retention statuses
            status = metadata.get("retention_status", "unknown")
            stats["retention_status_counts"][status] = (
                stats["retention_status_counts"].get(status, 0) + 1
            )

            # Count business contexts
            context = metadata.get("business_context", "none")
            stats["business_context_counts"][context] = (
                stats["business_context_counts"].get(context, 0) + 1
            )

        return stats

    # ===== PRIVATE HELPER METHODS =====

    def _load_metadata(self) -> Dict[str, Dict]:
        """Load metadata store from disk"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    metadata = json.load(f)
                self.logger.info(f"Loaded metadata for {len(metadata)} files")
                return metadata
            except Exception as e:
                self.logger.warning(f"Could not load metadata: {e}")

        return {}

    def _ensure_metadata_exists(self, file_path: Path) -> bool:
        """Ensure metadata exists for a file with defaults"""
        file_path_str = str(file_path)

        if file_path_str not in self.metadata_store:
            try:
                # Create default metadata
                self.metadata_store[file_path_str] = FileMetadata(
                    created_at=datetime.fromtimestamp(file_path.stat().st_mtime)
                ).__dict__
                return True
            except OSError:
                # File doesn't exist, use current time
                self.metadata_store[file_path_str] = FileMetadata(
                    created_at=datetime.now()
                ).__dict__
                return True

        return True

    def _validate_metadata_field(self, key: str, value: Any) -> bool:
        """Validate metadata field values"""
        # Basic validation - can be extended
        if key == "strategic_value":
            return isinstance(value, (int, float)) and 0 <= value <= 10
        elif key == "tags":
            return isinstance(value, list) and all(
                isinstance(tag, str) for tag in value
            )
        elif key == "retention_status":
            valid_statuses = ["active", "archived", "retained", "scheduled_deletion"]
            return value in valid_statuses
        elif key == "business_context":
            return value is None or isinstance(value, str)
        elif key == "retention_reason":
            return value is None or isinstance(value, str)

        return True  # Allow other fields by default
