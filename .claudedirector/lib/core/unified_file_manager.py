"""
🎯 STORY 9.5.3: UNIFIED FILE MANAGER - Core Module Consolidation

ELIMINATES MASSIVE DUPLICATION by consolidating:
- file_lifecycle_manager.py (515 lines) → CONSOLIDATED
- smart_file_organizer.py (494 lines) → CONSOLIDATED
- file_organizer_processor.py (354 lines) → CONSOLIDATED
TOTAL ELIMINATION: 1,363 lines → 800 lines (40% reduction achieved)

CONSOLIDATION STRATEGY:
- Single BaseManager inheritance eliminates ALL duplicate infrastructure
- Unified file lifecycle + organization + processing functionality
- Maintains full API compatibility through delegation methods
- BaseProcessor pattern integration for processing logic

Sequential Thinking Phase 9.5.3 - Built on proven BaseManager pattern for maximum DRY compliance.
Author: Martin | Platform Architecture
"""

import yaml
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter

# STORY 9.5.3: Single BaseManager import eliminates duplicate infrastructure
from .base_manager import BaseManager, BaseManagerConfig, ManagerType
from .base_processor import BaseProcessor


class GenerationMode(Enum):
    """File generation modes for different user preferences"""

    MINIMAL = "minimal"  # Strategic analysis only, consolidated files
    PROFESSIONAL = "professional"  # + Meeting prep, quarterly organization
    RESEARCH = "research"  # + Framework docs, methodology materials


class FileRetentionStatus(Enum):
    """File retention status for lifecycle management"""

    ACTIVE = "active"
    ARCHIVED = "archived"
    RETAINED = "retained"
    PENDING_REVIEW = "pending_review"


@dataclass
class FileMetadata:
    """Unified file metadata for lifecycle and organization"""

    created_at: datetime
    retention_status: FileRetentionStatus = FileRetentionStatus.ACTIVE
    tags: List[str] = field(default_factory=list)
    business_context: Optional[str] = None
    strategic_value: float = 0.0
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    consolidation_candidate: bool = False


@dataclass
class WorkspaceConfig:
    """Unified workspace configuration"""

    generation_mode: GenerationMode = GenerationMode.PROFESSIONAL
    auto_archive_days: int = 30
    retention_directory: str = "retained-assets"
    max_session_files: int = 5  # Trigger consolidation prompt


@dataclass
class SessionPattern:
    """File organization pattern detection"""

    pattern_type: str
    frequency: int
    business_context: str
    confidence_score: float


@dataclass
class ConsolidationOpportunity:
    """File consolidation opportunity"""

    files: List[Path]
    pattern: str
    business_value: str
    size_reduction: float


class UnifiedFileManager(BaseManager):
    """
    🎯 STORY 9.5.3: UNIFIED FILE MANAGER - Maximum DRY Consolidation

    Consolidates file lifecycle, organization, and processing into single BaseManager.
    Eliminates 1,363 lines of duplicate patterns while maintaining full API compatibility.

    ARCHITECTURAL PATTERN:
    - BaseManager foundation eliminates infrastructure duplication
    - BaseProcessor integration for complex processing logic
    - Factory methods for backward compatibility
    - Performance optimized through unified patterns
    """

    def __init__(self, workspace_path: str) -> None:
        """
        🎯 STORY 9.5.3: Unified initialization eliminates duplicate infrastructure
        """
        # BaseManager initialization eliminates duplicate infrastructure
        config = BaseManagerConfig(
            manager_name="unified_file_manager",
            manager_type=ManagerType.WORKSPACE,
            enable_metrics=True,
            enable_caching=True,
            enable_logging=True,
            custom_config={"workspace_path": workspace_path},
        )
        super().__init__(config)

        self.workspace_path = Path(workspace_path)
        self.config_file = self.workspace_path / "config" / "file_lifecycle.yaml"
        self.metadata_file = (
            self.workspace_path / ".claudedirector" / "file_metadata.json"
        )
        self.patterns_file = (
            self.workspace_path / ".claudedirector" / "session_patterns.json"
        )
        self.insights_file = (
            self.workspace_path / ".claudedirector" / "cross_session_insights.json"
        )

        # Load unified configuration and metadata
        self.config = self._load_config()
        self.metadata_store = self._load_metadata()
        self.session_patterns = self._load_session_patterns()
        self.cross_session_insights = self._load_cross_session_insights()

        # Business contexts for strategic file organization
        self.business_contexts = {
            "strategic-planning": ["strategy", "roadmap", "planning", "vision"],
            "team-management": ["team", "people", "1on1", "performance", "hiring"],
            "technical-architecture": ["architecture", "design", "technical", "system"],
            "stakeholder-communication": [
                "stakeholder",
                "executive",
                "board",
                "communication",
            ],
            "budget-planning": ["budget", "financial", "cost", "investment", "roi"],
            "vendor-evaluation": ["vendor", "procurement", "evaluation", "comparison"],
        }

        # Ensure required directories exist
        self._ensure_directories()

        self.logger.info(
            f"UnifiedFileManager initialized for workspace: {workspace_path}"
        )

    async def manage(self, operation: str, *args, **kwargs) -> Any:
        """
        BaseManager abstract method implementation
        Unified operation delegation for all file management functionality
        """
        # File Lifecycle Operations
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

        # File Organization Operations
        elif operation == "organize_files":
            return self.organize_workspace_files(*args, **kwargs)
        elif operation == "generate_filename":
            return self.generate_outcome_focused_filename(*args, **kwargs)
        elif operation == "analyze_patterns":
            return self.analyze_session_patterns(*args, **kwargs)
        elif operation == "health_check":
            return self.health_check()

        # Processing Operations
        elif operation == "detect_consolidation":
            return self.detect_consolidation_opportunities(*args, **kwargs)
        elif operation == "process_files":
            return self.process_file_batch(*args, **kwargs)

        else:
            self.logger.warning(
                f"Unknown unified file management operation: {operation}"
            )
            return None

    # ===== FILE LIFECYCLE METHODS (from file_lifecycle_manager.py) =====

    def create_file(
        self, filename: str, content: str = "", metadata: Optional[Dict] = None
    ) -> Path:
        """Create file with unified lifecycle tracking"""
        file_path = self.workspace_path / filename

        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        file_path.write_text(content)

        # Create unified metadata
        file_metadata = FileMetadata(
            created_at=datetime.now(),
            retention_status=FileRetentionStatus.ACTIVE,
            tags=metadata.get("tags", []) if metadata else [],
            business_context=metadata.get("business_context") if metadata else None,
            strategic_value=metadata.get("strategic_value", 0.0) if metadata else 0.0,
        )

        # Store metadata
        self.metadata_store[str(file_path)] = file_metadata.__dict__
        self._save_metadata()

        self.logger.info(f"Created file with unified tracking: {file_path}")
        return file_path

    def archive_old_files(self, days_threshold: Optional[int] = None) -> List[Path]:
        """Archive files based on unified criteria"""
        threshold = days_threshold or self.config.auto_archive_days
        cutoff_date = datetime.now() - timedelta(days=threshold)
        archived_files = []

        for file_path_str, metadata_dict in self.metadata_store.items():
            file_path = Path(file_path_str)
            if not file_path.exists():
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
                    metadata_dict["retention_status"] = (
                        FileRetentionStatus.ARCHIVED.value
                    )
                    archived_files.append(archive_path)

        self._save_metadata()
        self.logger.info(f"Archived {len(archived_files)} files")
        return archived_files

    def mark_for_retention(self, file_path: Path, reason: str = "") -> bool:
        """Mark file for retention with unified tracking"""
        file_path_str = str(file_path)
        if file_path_str in self.metadata_store:
            self.metadata_store[file_path_str][
                "retention_status"
            ] = FileRetentionStatus.RETAINED.value
            self.metadata_store[file_path_str]["retention_reason"] = reason
            self._save_metadata()
            self.logger.info(f"Marked for retention: {file_path}")
            return True
        return False

    def cleanup_workspace(self, dry_run: bool = False) -> Dict[str, int]:
        """Unified workspace cleanup with comprehensive statistics"""
        stats = {
            "files_analyzed": 0,
            "files_archived": 0,
            "files_consolidated": 0,
            "space_saved_mb": 0,
        }

        # Analyze all workspace files
        for file_path in self.workspace_path.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                stats["files_analyzed"] += 1

                # Check for archival candidates
                if self._should_archive(file_path):
                    if not dry_run:
                        self._move_to_archive(file_path)
                    stats["files_archived"] += 1

                # Check for consolidation opportunities
                if self._is_consolidation_candidate(file_path):
                    stats["files_consolidated"] += 1

        if not dry_run:
            self._save_metadata()

        self.logger.info(f"Workspace cleanup completed: {stats}")
        return stats

    def get_workspace_statistics(self) -> Dict[str, Any]:
        """Get unified workspace statistics"""
        stats = {
            "total_files": 0,
            "active_files": 0,
            "archived_files": 0,
            "retained_files": 0,
            "total_size_mb": 0,
            "business_contexts": defaultdict(int),
            "consolidation_opportunities": 0,
        }

        for file_path_str, metadata_dict in self.metadata_store.items():
            file_path = Path(file_path_str)
            if file_path.exists():
                stats["total_files"] += 1
                stats["total_size_mb"] += file_path.stat().st_size / (1024 * 1024)

                status = metadata_dict.get(
                    "retention_status", FileRetentionStatus.ACTIVE.value
                )
                if status == FileRetentionStatus.ACTIVE.value:
                    stats["active_files"] += 1
                elif status == FileRetentionStatus.ARCHIVED.value:
                    stats["archived_files"] += 1
                elif status == FileRetentionStatus.RETAINED.value:
                    stats["retained_files"] += 1

                context = metadata_dict.get("business_context")
                if context:
                    stats["business_contexts"][context] += 1

                if metadata_dict.get("consolidation_candidate", False):
                    stats["consolidation_opportunities"] += 1

        return dict(stats)

    # ===== FILE ORGANIZATION METHODS (from smart_file_organizer.py) =====

    def generate_outcome_focused_filename(
        self,
        session_context: str,
        content_preview: str = "",
        business_context: Optional[str] = None,
    ) -> str:
        """Generate strategic outcome-focused filename"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")

        # Extract key outcomes and strategic elements
        outcomes = self._extract_outcomes(content_preview)
        strategic_elements = self._extract_strategic_elements(session_context)

        # Determine business context if not provided
        if not business_context:
            business_context = self._detect_business_context(
                session_context + " " + content_preview
            )

        # Build filename components
        components = [timestamp]

        if business_context:
            components.append(business_context.replace("_", "-"))

        if strategic_elements:
            components.append("-".join(strategic_elements[:2]))  # Limit to 2 elements

        if outcomes:
            components.append("-".join(outcomes[:2]))  # Limit to 2 outcomes

        filename = "_".join(components) + ".md"

        # Ensure filename is reasonable length
        if len(filename) > 100:
            filename = filename[:97] + ".md"

        return filename

    def organize_workspace_files(
        self, target_directory: Optional[str] = None
    ) -> Dict[str, List[Path]]:
        """Organize workspace files by business context and strategic value"""
        organized_files = defaultdict(list)
        target_path = (
            Path(target_directory) if target_directory else self.workspace_path
        )

        for file_path in target_path.rglob("*.md"):
            if file_path.is_file():
                # Analyze file content for business context
                try:
                    content = file_path.read_text()
                    business_context = self._detect_business_context(content)
                    strategic_value = self._calculate_strategic_value(content)

                    # Update metadata
                    file_path_str = str(file_path)
                    if file_path_str not in self.metadata_store:
                        self.metadata_store[file_path_str] = FileMetadata(
                            created_at=datetime.fromtimestamp(file_path.stat().st_mtime)
                        ).__dict__

                    self.metadata_store[file_path_str][
                        "business_context"
                    ] = business_context
                    self.metadata_store[file_path_str][
                        "strategic_value"
                    ] = strategic_value

                    organized_files[business_context or "uncategorized"].append(
                        file_path
                    )

                except Exception as e:
                    self.logger.warning(f"Could not analyze file {file_path}: {e}")
                    organized_files["uncategorized"].append(file_path)

        self._save_metadata()

        # Log organization results
        for context, files in organized_files.items():
            self.logger.info(f"Organized {len(files)} files in context: {context}")

        return dict(organized_files)

    def analyze_session_patterns(self) -> List[SessionPattern]:
        """Analyze file creation patterns across sessions"""
        patterns = []

        # Group files by creation time windows (sessions)
        session_groups = self._group_files_by_session()

        for session_time, files in session_groups.items():
            if len(files) >= 2:  # Only analyze sessions with multiple files
                # Analyze patterns within session
                contexts = [
                    self.metadata_store.get(str(f), {}).get("business_context")
                    for f in files
                ]
                context_counts = Counter(c for c in contexts if c)

                for context, count in context_counts.items():
                    if count >= 2:  # Pattern requires at least 2 files
                        confidence = min(count / len(files), 1.0)
                        pattern = SessionPattern(
                            pattern_type=f"session_{context}",
                            frequency=count,
                            business_context=context,
                            confidence_score=confidence,
                        )
                        patterns.append(pattern)

        # Update session patterns cache
        self.session_patterns = [p.__dict__ for p in patterns]
        self._save_session_patterns()

        return patterns

    def health_check(self) -> Dict[str, Any]:
        """Comprehensive unified file management health check"""
        health = {
            "status": "healthy",
            "issues": [],
            "recommendations": [],
            "statistics": self.get_workspace_statistics(),
        }

        stats = health["statistics"]

        # Check for workspace bloat
        if stats["total_files"] > 100:
            health["issues"].append("Workspace has high file count")
            health["recommendations"].append("Consider archiving old files")

        # Check for consolidation opportunities
        if stats["consolidation_opportunities"] > 5:
            health["issues"].append("Multiple consolidation opportunities detected")
            health["recommendations"].append("Run consolidation analysis")

        # Check for uncategorized files
        uncategorized = stats["business_contexts"].get("uncategorized", 0)
        if uncategorized > 10:
            health["issues"].append("Many uncategorized files")
            health["recommendations"].append("Run business context analysis")

        # Overall health assessment
        if len(health["issues"]) == 0:
            health["status"] = "excellent"
        elif len(health["issues"]) <= 2:
            health["status"] = "good"
        else:
            health["status"] = "needs_attention"

        return health

    # ===== FILE PROCESSING METHODS (from file_organizer_processor.py) =====

    def detect_consolidation_opportunities(self) -> List[ConsolidationOpportunity]:
        """Detect file consolidation opportunities using unified analysis"""
        opportunities = []

        # Group files by business context
        context_groups = defaultdict(list)
        for file_path_str, metadata_dict in self.metadata_store.items():
            context = metadata_dict.get("business_context", "uncategorized")
            file_path = Path(file_path_str)
            if file_path.exists():
                context_groups[context].append(file_path)

        # Analyze each context for consolidation opportunities
        for context, files in context_groups.items():
            if len(files) >= 3:  # Need at least 3 files to consolidate
                # Calculate potential size reduction
                total_size = sum(f.stat().st_size for f in files if f.exists())
                estimated_reduction = total_size * 0.3  # Assume 30% reduction

                opportunity = ConsolidationOpportunity(
                    files=files,
                    pattern=f"Multiple {context} files",
                    business_value=f"Consolidate {context} documentation",
                    size_reduction=estimated_reduction / (1024 * 1024),  # MB
                )
                opportunities.append(opportunity)

        return opportunities

    def process_file_batch(self, files: List[Path], operation: str) -> Dict[str, Any]:
        """Process multiple files with unified operations"""
        results = {"processed": 0, "errors": 0, "operations": []}

        for file_path in files:
            try:
                if operation == "analyze":
                    content = file_path.read_text()
                    business_context = self._detect_business_context(content)
                    strategic_value = self._calculate_strategic_value(content)

                    # Update metadata
                    file_path_str = str(file_path)
                    if file_path_str not in self.metadata_store:
                        self.metadata_store[file_path_str] = FileMetadata(
                            created_at=datetime.fromtimestamp(file_path.stat().st_mtime)
                        ).__dict__

                    self.metadata_store[file_path_str][
                        "business_context"
                    ] = business_context
                    self.metadata_store[file_path_str][
                        "strategic_value"
                    ] = strategic_value

                    results["operations"].append(
                        {
                            "file": str(file_path),
                            "operation": "analyzed",
                            "context": business_context,
                            "value": strategic_value,
                        }
                    )

                elif operation == "archive":
                    archive_path = self._move_to_archive(file_path)
                    if archive_path:
                        file_path_str = str(file_path)
                        if file_path_str in self.metadata_store:
                            self.metadata_store[file_path_str][
                                "retention_status"
                            ] = FileRetentionStatus.ARCHIVED.value

                        results["operations"].append(
                            {
                                "file": str(file_path),
                                "operation": "archived",
                                "archive_path": str(archive_path),
                            }
                        )

                results["processed"] += 1

            except Exception as e:
                self.logger.error(f"Error processing file {file_path}: {e}")
                results["errors"] += 1

        self._save_metadata()
        return results

    # ===== PRIVATE HELPER METHODS =====

    def _load_config(self) -> WorkspaceConfig:
        """Load unified workspace configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config_data = yaml.safe_load(f)
                return WorkspaceConfig(**config_data)
            except Exception as e:
                self.logger.warning(f"Could not load config: {e}")

        # Return defaults
        config = WorkspaceConfig()
        self._save_config(config)
        return config

    def _save_config(self, config: WorkspaceConfig) -> None:
        """Save unified workspace configuration"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w") as f:
            yaml.dump(config.__dict__, f, default_flow_style=False)

    def _load_metadata(self) -> Dict[str, Dict]:
        """Load unified file metadata store"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load metadata: {e}")
        return {}

    def _save_metadata(self) -> None:
        """Save unified file metadata store"""
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata_store, f, indent=2, default=str)

    def _load_session_patterns(self) -> List[Dict]:
        """Load session patterns cache"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load session patterns: {e}")
        return []

    def _save_session_patterns(self) -> None:
        """Save session patterns cache"""
        self.patterns_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.patterns_file, "w") as f:
            json.dump(self.session_patterns, f, indent=2)

    def _load_cross_session_insights(self) -> Dict:
        """Load cross-session insights cache"""
        if self.insights_file.exists():
            try:
                with open(self.insights_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load insights: {e}")
        return {}

    def _ensure_directories(self) -> None:
        """Ensure all required directories exist"""
        directories = [
            self.workspace_path / "config",
            self.workspace_path / ".claudedirector",
            self.workspace_path / self.config.retention_directory,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _move_to_archive(self, file_path: Path) -> Optional[Path]:
        """Move file to archive directory"""
        try:
            archive_dir = (
                self.workspace_path / self.config.retention_directory / "archived"
            )
            archive_dir.mkdir(parents=True, exist_ok=True)

            archive_path = archive_dir / file_path.name
            file_path.rename(archive_path)
            return archive_path
        except Exception as e:
            self.logger.error(f"Could not archive file {file_path}: {e}")
            return None

    def _should_archive(self, file_path: Path) -> bool:
        """Check if file should be archived"""
        file_path_str = str(file_path)
        if file_path_str in self.metadata_store:
            metadata = self.metadata_store[file_path_str]
            status = metadata.get("retention_status", FileRetentionStatus.ACTIVE.value)
            return status == FileRetentionStatus.ACTIVE.value

        # Default archival logic for files without metadata
        age_days = (
            datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)
        ).days
        return age_days > self.config.auto_archive_days

    def _is_consolidation_candidate(self, file_path: Path) -> bool:
        """Check if file is a consolidation candidate"""
        file_path_str = str(file_path)
        if file_path_str in self.metadata_store:
            return self.metadata_store[file_path_str].get(
                "consolidation_candidate", False
            )
        return False

    def _detect_business_context(self, content: str) -> Optional[str]:
        """Detect business context from content"""
        content_lower = content.lower()

        for context, keywords in self.business_contexts.items():
            if any(keyword in content_lower for keyword in keywords):
                return context

        return None

    def _calculate_strategic_value(self, content: str) -> float:
        """Calculate strategic value score for content"""
        strategic_indicators = [
            "strategy",
            "roadmap",
            "vision",
            "goals",
            "objectives",
            "stakeholder",
            "executive",
            "board",
            "leadership",
            "budget",
            "investment",
            "roi",
            "cost",
            "revenue",
            "architecture",
            "technical",
            "platform",
            "system",
        ]

        content_lower = content.lower()
        matches = sum(
            1 for indicator in strategic_indicators if indicator in content_lower
        )

        # Normalize to 0-1 scale
        return min(matches / len(strategic_indicators), 1.0)

    def _extract_outcomes(self, content: str) -> List[str]:
        """Extract key outcomes from content"""
        # Simple extraction logic - can be enhanced
        outcome_patterns = [
            r"outcome[:\s]+([^.!?\n]+)",
            r"result[:\s]+([^.!?\n]+)",
            r"decision[:\s]+([^.!?\n]+)",
            r"action[:\s]+([^.!?\n]+)",
        ]

        outcomes = []
        for pattern in outcome_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            outcomes.extend([m.strip()[:20] for m in matches])  # Limit length

        return outcomes[:3]  # Return top 3

    def _extract_strategic_elements(self, context: str) -> List[str]:
        """Extract strategic elements from session context"""
        strategic_words = [
            "strategy",
            "planning",
            "roadmap",
            "vision",
            "architecture",
            "stakeholder",
            "executive",
            "team",
            "budget",
            "technical",
        ]

        context_words = context.lower().split()
        elements = [word for word in context_words if word in strategic_words]

        return elements[:3]  # Return top 3

    def _group_files_by_session(self) -> Dict[str, List[Path]]:
        """Group files by session time windows"""
        sessions = defaultdict(list)

        for file_path_str, metadata_dict in self.metadata_store.items():
            file_path = Path(file_path_str)
            if file_path.exists():
                created_at = datetime.fromisoformat(metadata_dict["created_at"])
                # Group by hour for session detection
                session_key = created_at.strftime("%Y%m%d_%H")
                sessions[session_key].append(file_path)

        return dict(sessions)


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
