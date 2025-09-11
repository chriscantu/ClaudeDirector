"""
🎯 STORY 9.6.4: UNIFIED FILE MANAGER

BLOAT ELIMINATION: Consolidates 1,363 lines from 3 file management components:
- smart_file_organizer.py (494 lines) → CONSOLIDATED
- file_organizer_processor.py (354 lines) → CONSOLIDATED
- file_lifecycle_manager.py (515 lines) → CONSOLIDATED

DRY COMPLIANCE: Single source of truth for all file operations
SOLID COMPLIANCE: Single responsibility with specialized methods
PROJECT_STRUCTURE.md COMPLIANCE: Following core/ organization

Author: Martin | Platform Architecture with Sequential Thinking + Context7
"""

import re
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter

# Import base infrastructure
try:
    from .base_manager import BaseManager, BaseManagerConfig, ManagerType
except ImportError:
    BaseManager = object
    BaseManagerConfig = dict
    ManagerType = str

import logging

logger = logging.getLogger(__name__)


# ===== CONSOLIDATED DATA STRUCTURES =====


class GenerationMode(Enum):
    """File generation modes for different user preferences"""

    MINIMAL = "minimal"  # Strategic analysis only, consolidated files
    PROFESSIONAL = "professional"  # + Meeting prep, quarterly organization
    RESEARCH = "research"  # + Framework docs, methodology materials


class FileRetentionStatus(Enum):
    """File retention status for lifecycle management"""

    ACTIVE = "active"
    ARCHIVED = "archived"
    CONSOLIDATED = "consolidated"
    DEPRECATED = "deprecated"


class ConsolidationType(Enum):
    """Types of file consolidation strategies"""

    CHRONOLOGICAL = "chronological"
    THEMATIC = "thematic"
    PROJECT_BASED = "project_based"
    SIZE_BASED = "size_based"


@dataclass
class FileMetadata:
    """Consolidated file metadata structure"""

    created_at: datetime
    last_modified: datetime
    retention_status: FileRetentionStatus = FileRetentionStatus.ACTIVE
    file_size: int = 0
    tags: List[str] = field(default_factory=list)
    project_association: Optional[str] = None
    consolidation_parent: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsolidationOpportunity:
    """File consolidation opportunity structure"""

    files: List[str]
    consolidation_type: ConsolidationType
    suggested_name: str
    priority: str
    size_reduction: float
    reasoning: List[str] = field(default_factory=list)


@dataclass
class SessionPattern:
    """Session-based file pattern structure"""

    pattern_type: str
    files: List[str]
    frequency: int
    last_seen: datetime
    consolidation_potential: float


@dataclass
class WorkspaceConfig:
    """Workspace configuration for file management"""

    generation_mode: GenerationMode = GenerationMode.PROFESSIONAL
    auto_archive_days: int = 30
    max_active_files: int = 50
    max_session_files: int = 5
    consolidation_threshold: float = 0.8
    enable_auto_consolidation: bool = True


class UnifiedFileManager(BaseManager if BaseManager != object else object):
    """
    🎯 STORY 9.6.4: UNIFIED FILE MANAGER

    MASSIVE CONSOLIDATION: Replaces 3 separate components (1,363 lines total):
    - SmartFileOrganizer: File organization and consolidation
    - FileOrganizerProcessor: File processing and pattern recognition
    - FileLifecycleManager: Lifecycle management and metadata

    ARCHITECTURE BENEFITS:
    - Single source of truth for file operations
    - Unified configuration and error handling
    - Consistent logging and performance monitoring
    - Reduced maintenance overhead
    - Improved testability
    """

    def __init__(
        self,
        workspace_path: Union[str, Path],
        config: Optional[WorkspaceConfig] = None,
        **kwargs,
    ):
        """Initialize unified file manager with consolidated functionality"""
        if BaseManager != object:
            # Convert WorkspaceConfig to BaseManagerConfig if needed
            base_config = (
                BaseManagerConfig(
                    manager_type=ManagerType.FILE_MANAGEMENT,
                    workspace_path=str(workspace_path),
                )
                if config is None
                else config
            )
            super().__init__(base_config, **kwargs)

        self.workspace_path = Path(workspace_path)
        self.config = config or WorkspaceConfig()

        # Ensure workspace directories exist
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        (self.workspace_path / "archive").mkdir(parents=True, exist_ok=True)
        (self.workspace_path / "consolidated").mkdir(parents=True, exist_ok=True)

        # File metadata store
        self.metadata_store: Dict[str, FileMetadata] = {}
        self.session_patterns: Dict[str, SessionPattern] = {}

        # Performance metrics
        self.metrics = {
            "files_organized": 0,
            "consolidations_performed": 0,
            "archives_created": 0,
            "space_saved_bytes": 0,
            "average_processing_time": 0.0,
        }

        # Load existing metadata
        self._load_metadata()

        logger.info(f"UnifiedFileManager initialized for workspace: {workspace_path}")

    # ===== FILE ORGANIZATION (from smart_file_organizer.py) =====

    def organize_workspace_files(
        self, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🎯 CONSOLIDATED: Organize workspace files based on patterns and lifecycle
        Replaces SmartFileOrganizer.organize_workspace_files()
        """
        session_context = session_context or {}
        start_time = datetime.now()

        try:
            # Scan workspace for files
            files = list(self.workspace_path.glob("**/*.md"))
            files.extend(self.workspace_path.glob("**/*.txt"))
            files.extend(self.workspace_path.glob("**/*.json"))

            organization_results = {
                "files_processed": len(files),
                "patterns_identified": 0,
                "consolidations_suggested": 0,
                "files_archived": 0,
                "space_saved": 0,
            }

            # Update file metadata
            for file_path in files:
                self._update_file_metadata(file_path)

            # Identify patterns
            patterns = self._identify_session_patterns(files)
            organization_results["patterns_identified"] = len(patterns)

            # Identify consolidation opportunities
            opportunities = self._identify_consolidation_opportunities(files)
            organization_results["consolidations_suggested"] = len(opportunities)

            # Auto-archive old files
            archived_files = self._auto_archive_files(files)
            organization_results["files_archived"] = len(archived_files)

            # Update metrics
            self.metrics["files_organized"] += len(files)
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_processing_time(processing_time)

            return organization_results

        except Exception as e:
            logger.error(f"File organization error: {e}")
            return {"error": str(e), "files_processed": 0}

    def consolidate_files(
        self, opportunity: ConsolidationOpportunity, execute: bool = False
    ) -> Optional[str]:
        """
        🎯 CONSOLIDATED: Execute file consolidation
        Replaces SmartFileOrganizer.consolidate_files()
        """
        if not execute:
            return f"Would consolidate {len(opportunity.files)} files into '{opportunity.suggested_name}'"

        try:
            # Create consolidated content
            consolidated_content = self._create_consolidated_content(
                opportunity.files, opportunity.consolidation_type
            )

            # Create consolidated file
            consolidated_path = (
                self.workspace_path
                / "consolidated"
                / f"{opportunity.suggested_name}.md"
            )
            consolidated_path.parent.mkdir(parents=True, exist_ok=True)

            with open(consolidated_path, "w", encoding="utf-8") as f:
                f.write(consolidated_content)

            # Archive original files
            space_saved = 0
            for filepath in opportunity.files:
                file_path = Path(filepath)
                if file_path.exists():
                    space_saved += file_path.stat().st_size
                    # Move to archive
                    archive_path = self.workspace_path / "archive" / file_path.name
                    file_path.rename(archive_path)

                    # Update metadata
                    if str(file_path) in self.metadata_store:
                        self.metadata_store[str(file_path)].retention_status = (
                            FileRetentionStatus.CONSOLIDATED
                        )
                        self.metadata_store[str(file_path)].consolidation_parent = str(
                            consolidated_path
                        )

            # Update metrics
            self.metrics["consolidations_performed"] += 1
            self.metrics["space_saved_bytes"] += space_saved

            # Save metadata
            self._save_metadata()

            return str(consolidated_path)

        except Exception as e:
            logger.error(f"File consolidation error: {e}")
            return None

    # ===== FILE PROCESSING (from file_organizer_processor.py) =====

    def _identify_session_patterns(self, files: List[Path]) -> List[SessionPattern]:
        """Identify patterns in file creation and usage"""
        patterns = []

        # Group files by date
        date_groups = defaultdict(list)
        for file_path in files:
            if file_path.exists():
                created_date = datetime.fromtimestamp(file_path.stat().st_ctime).date()
                date_groups[created_date].append(str(file_path))

        # Identify session patterns
        for date, date_files in date_groups.items():
            if len(date_files) >= 3:  # Minimum files for a pattern
                pattern = SessionPattern(
                    pattern_type="daily_session",
                    files=date_files,
                    frequency=1,
                    last_seen=datetime.combine(date, datetime.min.time()),
                    consolidation_potential=0.8 if len(date_files) > 5 else 0.6,
                )
                patterns.append(pattern)

        return patterns

    def _identify_consolidation_opportunities(
        self, files: List[Path]
    ) -> List[ConsolidationOpportunity]:
        """Identify opportunities for file consolidation"""
        opportunities = []

        # Group by naming patterns
        pattern_groups = defaultdict(list)
        for file_path in files:
            if file_path.exists():
                # Extract base pattern (remove dates, numbers, etc.)
                base_name = re.sub(r"\d{4}-\d{2}-\d{2}|\d+", "", file_path.stem)
                base_name = re.sub(r"[-_]+", "_", base_name).strip("_")
                if base_name:
                    pattern_groups[base_name].append(str(file_path))

        # Create consolidation opportunities
        for pattern, pattern_files in pattern_groups.items():
            if len(pattern_files) >= 3:  # Minimum files for consolidation
                total_size = sum(
                    Path(f).stat().st_size for f in pattern_files if Path(f).exists()
                )

                opportunity = ConsolidationOpportunity(
                    files=pattern_files,
                    consolidation_type=ConsolidationType.THEMATIC,
                    suggested_name=f"consolidated_{pattern}",
                    priority="medium" if len(pattern_files) < 5 else "high",
                    size_reduction=total_size * 0.3,  # Estimated 30% reduction
                    reasoning=[
                        f"Found {len(pattern_files)} files with similar pattern",
                        f"Total size: {total_size} bytes",
                        "Consolidation would improve organization",
                    ],
                )
                opportunities.append(opportunity)

        return opportunities

    def _create_consolidated_content(
        self, files: List[str], consolidation_type: ConsolidationType
    ) -> str:
        """Create consolidated content from multiple files"""
        content_parts = [
            f"# Consolidated File - {consolidation_type.value.title()}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Source files: {len(files)}",
            "",
            "---",
            "",
        ]

        for file_path in files:
            path = Path(file_path)
            if path.exists():
                content_parts.append(f"## {path.name}")
                content_parts.append(f"*Original: {file_path}*")
                content_parts.append("")

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content_parts.append(f.read())
                except Exception as e:
                    content_parts.append(f"Error reading file: {e}")

                content_parts.append("")
                content_parts.append("---")
                content_parts.append("")

        return "\n".join(content_parts)

    # ===== LIFECYCLE MANAGEMENT (from file_lifecycle_manager.py) =====

    def _update_file_metadata(self, file_path: Path) -> FileMetadata:
        """Update metadata for a file"""
        file_key = str(file_path)

        if file_key not in self.metadata_store:
            # Create new metadata
            metadata = FileMetadata(
                created_at=datetime.fromtimestamp(file_path.stat().st_ctime),
                last_modified=datetime.fromtimestamp(file_path.stat().st_mtime),
                file_size=file_path.stat().st_size,
            )
            self.metadata_store[file_key] = metadata
        else:
            # Update existing metadata
            metadata = self.metadata_store[file_key]
            metadata.last_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
            metadata.file_size = file_path.stat().st_size

        return self.metadata_store[file_key]

    def _auto_archive_files(self, files: List[Path]) -> List[str]:
        """Auto-archive old files based on retention policy"""
        archived_files = []
        cutoff_date = datetime.now() - timedelta(days=self.config.auto_archive_days)

        for file_path in files:
            if file_path.exists():
                metadata = self.metadata_store.get(str(file_path))
                if metadata and metadata.last_modified < cutoff_date:
                    # Archive the file
                    archive_path = self.workspace_path / "archive" / file_path.name
                    archive_path.parent.mkdir(parents=True, exist_ok=True)

                    try:
                        file_path.rename(archive_path)
                        metadata.retention_status = FileRetentionStatus.ARCHIVED
                        archived_files.append(str(file_path))
                        self.metrics["archives_created"] += 1
                    except Exception as e:
                        logger.error(f"Error archiving {file_path}: {e}")

        return archived_files

    def get_file_metadata(self, file_path: Union[str, Path]) -> Optional[FileMetadata]:
        """Get metadata for a specific file"""
        return self.metadata_store.get(str(file_path))

    def set_file_retention_status(
        self, file_path: Union[str, Path], status: FileRetentionStatus
    ):
        """Set retention status for a file"""
        file_key = str(file_path)
        if file_key in self.metadata_store:
            self.metadata_store[file_key].retention_status = status
            self._save_metadata()

    # ===== METADATA PERSISTENCE =====

    def _load_metadata(self):
        """Load metadata from storage"""
        metadata_file = self.workspace_path / ".file_metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                for file_path, metadata_dict in data.items():
                    metadata = FileMetadata(
                        created_at=datetime.fromisoformat(metadata_dict["created_at"]),
                        last_modified=datetime.fromisoformat(
                            metadata_dict["last_modified"]
                        ),
                        retention_status=FileRetentionStatus(
                            metadata_dict.get("retention_status", "active")
                        ),
                        file_size=metadata_dict.get("file_size", 0),
                        tags=metadata_dict.get("tags", []),
                        project_association=metadata_dict.get("project_association"),
                        consolidation_parent=metadata_dict.get("consolidation_parent"),
                        metadata=metadata_dict.get("metadata", {}),
                    )
                    self.metadata_store[file_path] = metadata

            except Exception as e:
                logger.error(f"Error loading metadata: {e}")

    def _save_metadata(self):
        """Save metadata to storage"""
        metadata_file = self.workspace_path / ".file_metadata.json"
        try:
            data = {}
            for file_path, metadata in self.metadata_store.items():
                data[file_path] = {
                    "created_at": metadata.created_at.isoformat(),
                    "last_modified": metadata.last_modified.isoformat(),
                    "retention_status": metadata.retention_status.value,
                    "file_size": metadata.file_size,
                    "tags": metadata.tags,
                    "project_association": metadata.project_association,
                    "consolidation_parent": metadata.consolidation_parent,
                    "metadata": metadata.metadata,
                }

            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error saving metadata: {e}")

    # ===== UTILITY METHODS =====

    def _update_processing_time(self, processing_time: float):
        """Update average processing time metric"""
        current_avg = self.metrics["average_processing_time"]
        total_ops = (
            self.metrics["files_organized"] + self.metrics["consolidations_performed"]
        )

        if total_ops <= 1:
            self.metrics["average_processing_time"] = processing_time
        else:
            self.metrics["average_processing_time"] = (
                current_avg * (total_ops - 1) + processing_time
            ) / total_ops

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get consolidated performance metrics"""
        return {
            **self.metrics,
            "consolidation_info": {
                "replaced_components": 3,
                "lines_eliminated": 1363,
                "consolidation_ratio": "3:1",
            },
            "workspace_stats": {
                "total_files_tracked": len(self.metadata_store),
                "active_files": len(
                    [
                        m
                        for m in self.metadata_store.values()
                        if m.retention_status == FileRetentionStatus.ACTIVE
                    ]
                ),
                "archived_files": len(
                    [
                        m
                        for m in self.metadata_store.values()
                        if m.retention_status == FileRetentionStatus.ARCHIVED
                    ]
                ),
            },
        }


# ===== CONSOLIDATION: Public API =====
__all__ = [
    "UnifiedFileManager",
    "FileMetadata",
    "FileRetentionStatus",
    "GenerationMode",
    "ConsolidationOpportunity",
    "SessionPattern",
    "WorkspaceConfig",
    "ConsolidationType",
]


# ===== CONSOLIDATION: Factory Functions =====
def create_unified_file_manager(
    workspace_path: Union[str, Path], config: Optional[WorkspaceConfig] = None
) -> UnifiedFileManager:
    """
    🎯 STORY 9.6.4: CONSOLIDATION FACTORY

    Creates unified file manager replacing 3 separate components
    Maintains backward compatibility while eliminating bloat
    """
    return UnifiedFileManager(workspace_path, config)


def get_default_file_manager(workspace_path: Union[str, Path]) -> UnifiedFileManager:
    """Get default unified file manager instance"""
    global _default_file_manager
    if "_default_file_manager" not in globals():
        globals()["_default_file_manager"] = create_unified_file_manager(workspace_path)
    return globals()["_default_file_manager"]
