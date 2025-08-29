"""
Workspace Monitor Unified - Phase 9 Consolidation

This module consolidates workspace monitoring functionality from:
- memory/workspace_monitor.py
- context_engineering/workspace_integration.py (partial)

Status: Phase 9 Architecture Cleanup - Memory Systems Consolidation
Author: Martin | Platform Architecture with MCP Sequential enhancement
"""

import json
import sqlite3
import time
import logging
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, asdict

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

    # Fallback minimal implementations
    class FileSystemEventHandler:
        def on_modified(self, event): pass
        def on_created(self, event): pass
        def on_deleted(self, event): pass

    class Observer:
        def schedule(self, handler, path, recursive=False): pass
        def start(self): pass
        def stop(self): pass
        def join(self): pass

# Import strategic memory manager
try:
    from .strategic_memory_manager import get_strategic_memory_manager

    STRATEGIC_MEMORY_AVAILABLE = True
except ImportError:
    STRATEGIC_MEMORY_AVAILABLE = False

# Import stakeholder intelligence
try:
    from .stakeholder_intelligence_unified import get_stakeholder_intelligence

    STAKEHOLDER_INTELLIGENCE_AVAILABLE = True
except ImportError:
    STAKEHOLDER_INTELLIGENCE_AVAILABLE = False

# Import meeting intelligence (legacy compatibility)
try:
    from ..memory.meeting_intelligence import MeetingIntelligenceManager

    MEETING_INTELLIGENCE_AVAILABLE = True
except ImportError:
    MEETING_INTELLIGENCE_AVAILABLE = False

# Phase 8 performance integration
try:
    from ..performance.cache_manager import get_cache_manager
    from ..performance.memory_optimizer import get_memory_optimizer

    PERFORMANCE_AVAILABLE = True
except ImportError:
    PERFORMANCE_AVAILABLE = False


@dataclass
class StrategyFile:
    """Represents a strategic document in the workspace"""

    path: str
    file_type: str  # 'initiative', 'meeting_prep', 'strategy', 'analysis', 'budget'
    last_modified: datetime
    content_hash: str
    priority: str  # 'high', 'medium', 'low'
    stakeholders: List[str]
    extracted_context: Dict[str, Any]
    processing_status: str  # 'pending', 'processed', 'error'
    strategic_value: float  # 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data["last_modified"] = self.last_modified.isoformat()
        return data


class StrategicWorkspaceHandler(FileSystemEventHandler):
    """
    Unified workspace event handler for strategic intelligence capture

    Consolidates functionality from:
    - StrategicWorkspaceHandler (memory layer)
    - WorkspaceIntegration monitoring features
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        workspace_root: Optional[Path] = None,
        enable_performance: bool = True,
    ):
        self.db_path = db_path
        self.workspace_root = workspace_root or Path("leadership-workspace")
        self.enable_performance = enable_performance

        # Initialize strategic memory manager
        if STRATEGIC_MEMORY_AVAILABLE:
            self.memory_manager = get_strategic_memory_manager(db_path)
        else:
            self.memory_manager = None

        # Initialize stakeholder intelligence
        if STAKEHOLDER_INTELLIGENCE_AVAILABLE:
            self.stakeholder_intelligence = get_stakeholder_intelligence()
        else:
            self.stakeholder_intelligence = None

        # Initialize meeting intelligence (legacy compatibility)
        if MEETING_INTELLIGENCE_AVAILABLE and db_path:
            self.meeting_manager = MeetingIntelligenceManager(db_path)
        else:
            self.meeting_manager = None

        # Initialize performance components
        if self.enable_performance and PERFORMANCE_AVAILABLE:
            try:
                self.cache_manager = get_cache_manager()
                self.memory_optimizer = get_memory_optimizer()
            except Exception:
                self.enable_performance = False

        # File processing configuration
        self.supported_extensions = {".md", ".txt", ".json"}
        self.ignore_patterns = {
            "__pycache__",
            ".git",
            ".vscode",
            "node_modules",
            ".env",
            "venv",
            ".pytest_cache",
        }

        # Strategic file type classification
        self.file_type_patterns = {
            "initiative": ["initiative", "project", "epic"],
            "meeting_prep": ["meeting-prep", "agenda", "prep"],
            "strategy": ["strategy", "strategic", "roadmap"],
            "analysis": ["analysis", "research", "study"],
            "budget": ["budget", "cost", "roi", "financial"],
            "stakeholder": ["stakeholder", "relationship", "coalition"],
        }

        self.logger = logging.getLogger(__name__)

    def on_created(self, event):
        """Handle file/directory creation events"""
        if event.is_directory:
            self._handle_directory_created(event.src_path)
        else:
            self._handle_file_created(event.src_path)

    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory:
            self._handle_file_modified(event.src_path)

    def _handle_file_created(self, file_path: str):
        """Process newly created files for strategic intelligence"""
        path = Path(file_path)

        if not self._should_process_file(path):
            return

        try:
            # Classify file type
            file_type = self._classify_file_type(path)

            # Extract content
            content = self._read_file_content(path)
            if not content:
                return

            # Create strategy file record
            strategy_file = self._create_strategy_file(path, file_type, content)

            # Process for strategic intelligence
            self._process_strategic_content(strategy_file, content)

            self.logger.info(
                f"Processed new strategic file: {path} (type: {file_type})"
            )

        except Exception as e:
            self.logger.error(f"Error processing created file {file_path}: {e}")

    def _handle_file_modified(self, file_path: str):
        """Process modified files for updated intelligence"""
        path = Path(file_path)

        if not self._should_process_file(path):
            return

        try:
            # Check if content actually changed
            current_hash = self._calculate_file_hash(path)

            # Use cache to check if we've already processed this version
            if self.enable_performance:
                cache_key = f"file_hash:{path}"
                cached_hash = self.cache_manager.get(cache_key)
                if cached_hash == current_hash:
                    return  # No actual change
                self.cache_manager.set(cache_key, current_hash, ttl=3600)

            # Process as updated file
            content = self._read_file_content(path)
            if content:
                file_type = self._classify_file_type(path)
                strategy_file = self._create_strategy_file(path, file_type, content)
                self._process_strategic_content(strategy_file, content, is_update=True)

                self.logger.info(f"Processed modified strategic file: {path}")

        except Exception as e:
            self.logger.error(f"Error processing modified file {file_path}: {e}")

    def _handle_directory_created(self, dir_path: str):
        """Handle directory creation for strategic initiative tracking"""
        path = Path(dir_path)

        # Check if this looks like a strategic initiative directory
        strategic_indicators = ["initiative", "project", "strategic", "epic"]

        if any(indicator in path.name.lower() for indicator in strategic_indicators):
            try:
                # Create initiative tracking record
                initiative_data = {
                    "directory_path": str(path),
                    "initiative_name": path.name,
                    "created_timestamp": datetime.now().isoformat(),
                    "status": "discovered",
                    "type": "directory_initiative",
                }

                # Store in strategic memory if available
                if self.memory_manager:
                    self.memory_manager.preserve_context(
                        context_data={"new_initiative": initiative_data},
                        critical_indicators=["initiative_tracking"],
                    )

                self.logger.info(
                    f"Discovered new strategic initiative directory: {path}"
                )

            except Exception as e:
                self.logger.error(
                    f"Error processing initiative directory {dir_path}: {e}"
                )

    def _should_process_file(self, path: Path) -> bool:
        """Determine if file should be processed for strategic intelligence"""
        # Check extension
        if path.suffix.lower() not in self.supported_extensions:
            return False

        # Check ignore patterns
        if any(pattern in str(path) for pattern in self.ignore_patterns):
            return False

        # Check minimum file size (avoid empty files)
        try:
            if path.stat().st_size < 10:
                return False
        except (OSError, FileNotFoundError):
            return False

        # Check if within workspace
        try:
            path.relative_to(self.workspace_root)
        except ValueError:
            return False  # Outside workspace

        return True

    def _classify_file_type(self, path: Path) -> str:
        """Classify file type based on path and content patterns"""
        path_str = str(path).lower()

        # Check path patterns
        for file_type, patterns in self.file_type_patterns.items():
            if any(pattern in path_str for pattern in patterns):
                return file_type

        # Check parent directory patterns
        parent_parts = [part.lower() for part in path.parent.parts]
        for file_type, patterns in self.file_type_patterns.items():
            if any(pattern in " ".join(parent_parts) for pattern in patterns):
                return file_type

        return "general"

    def _read_file_content(self, path: Path) -> Optional[str]:
        """Safely read file content"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except (UnicodeDecodeError, OSError, FileNotFoundError):
            try:
                # Try with different encoding
                with open(path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception:
                return None

    def _calculate_file_hash(self, path: Path) -> str:
        """Calculate file content hash for change detection"""
        try:
            content = self._read_file_content(path)
            if content:
                return hashlib.md5(content.encode("utf-8")).hexdigest()
        except Exception:
            pass
        return ""

    def _create_strategy_file(
        self, path: Path, file_type: str, content: str
    ) -> StrategyFile:
        """Create StrategyFile record from path and content"""
        return StrategyFile(
            path=str(path),
            file_type=file_type,
            last_modified=datetime.fromtimestamp(path.stat().st_mtime),
            content_hash=self._calculate_file_hash(path),
            priority=self._determine_priority(path, content),
            stakeholders=self._extract_stakeholders(content),
            extracted_context=self._extract_strategic_context(content, file_type),
            processing_status="processed",
            strategic_value=self._calculate_strategic_value(content, file_type),
        )

    def _determine_priority(self, path: Path, content: str) -> str:
        """Determine strategic priority of document"""
        priority_indicators = {
            "high": [
                "urgent",
                "critical",
                "executive",
                "board",
                "ceo",
                "vp",
                "director",
            ],
            "medium": ["important", "strategic", "priority", "milestone"],
            "low": ["general", "note", "draft", "idea"],
        }

        content_lower = content.lower()
        path_lower = str(path).lower()

        for priority, indicators in priority_indicators.items():
            if any(
                indicator in content_lower or indicator in path_lower
                for indicator in indicators
            ):
                return priority

        return "medium"  # Default

    def _extract_stakeholders(self, content: str) -> List[str]:
        """Extract stakeholder mentions from content"""
        if not self.stakeholder_intelligence:
            return []

        try:
            # Use stakeholder intelligence for detection
            context = {"category": "workspace_monitoring", "auto_detection": True}
            candidates = self.stakeholder_intelligence.detect_stakeholders_in_content(
                content, context
            )

            return [
                candidate["name"]
                for candidate in candidates
                if candidate.get("confidence", 0) > 0.6
            ]
        except Exception as e:
            self.logger.warning(f"Stakeholder extraction failed: {e}")
            return []

    def _extract_strategic_context(
        self, content: str, file_type: str
    ) -> Dict[str, Any]:
        """Extract strategic context based on file type"""
        context = {
            "file_type": file_type,
            "content_length": len(content),
            "extracted_at": datetime.now().isoformat(),
        }

        # Extract key phrases based on file type
        if file_type == "meeting_prep":
            context.update(self._extract_meeting_context(content))
        elif file_type == "initiative":
            context.update(self._extract_initiative_context(content))
        elif file_type == "strategy":
            context.update(self._extract_strategy_context(content))
        elif file_type == "budget":
            context.update(self._extract_budget_context(content))

        return context

    def _extract_meeting_context(self, content: str) -> Dict[str, Any]:
        """Extract meeting-specific context"""
        context = {}

        # Look for agenda items
        agenda_indicators = ["agenda", "topics", "discussion points"]
        for indicator in agenda_indicators:
            if indicator in content.lower():
                context["has_agenda"] = True
                break

        # Look for action items
        action_indicators = ["action item", "next steps", "follow up", "todo"]
        for indicator in action_indicators:
            if indicator in content.lower():
                context["has_action_items"] = True
                break

        return context

    def _extract_initiative_context(self, content: str) -> Dict[str, Any]:
        """Extract initiative-specific context"""
        context = {}

        # Look for objectives
        if any(
            term in content.lower()
            for term in ["objective", "goal", "target", "outcome"]
        ):
            context["has_objectives"] = True

        # Look for timeline
        if any(
            term in content.lower()
            for term in ["timeline", "schedule", "deadline", "milestone"]
        ):
            context["has_timeline"] = True

        # Look for resources
        if any(
            term in content.lower()
            for term in ["resource", "budget", "team", "allocation"]
        ):
            context["has_resources"] = True

        return context

    def _extract_strategy_context(self, content: str) -> Dict[str, Any]:
        """Extract strategy-specific context"""
        context = {}

        # Look for strategic elements
        strategy_indicators = {
            "vision": ["vision", "direction", "future state"],
            "analysis": ["swot", "analysis", "competitive", "market"],
            "objectives": ["objective", "goal", "target", "kpi"],
            "tactics": ["tactic", "approach", "method", "strategy"],
        }

        for element, indicators in strategy_indicators.items():
            if any(indicator in content.lower() for indicator in indicators):
                context[f"has_{element}"] = True

        return context

    def _extract_budget_context(self, content: str) -> Dict[str, Any]:
        """Extract budget-specific context"""
        context = {}

        # Look for financial elements
        if any(
            term in content.lower()
            for term in ["$", "cost", "budget", "expense", "revenue"]
        ):
            context["has_financial_data"] = True

        # Look for ROI analysis
        if any(
            term in content.lower()
            for term in ["roi", "return on investment", "payback", "benefit"]
        ):
            context["has_roi_analysis"] = True

        return context

    def _calculate_strategic_value(self, content: str, file_type: str) -> float:
        """Calculate strategic value score (0.0 to 1.0)"""
        base_scores = {
            "strategy": 0.8,
            "initiative": 0.7,
            "meeting_prep": 0.6,
            "budget": 0.7,
            "analysis": 0.6,
            "stakeholder": 0.6,
            "general": 0.3,
        }

        score = base_scores.get(file_type, 0.3)

        # Boost score based on content indicators
        high_value_terms = [
            "executive",
            "strategic",
            "critical",
            "urgent",
            "board",
            "vision",
            "objectives",
            "roi",
            "competitive advantage",
            "transformation",
        ]

        content_lower = content.lower()
        term_count = sum(1 for term in high_value_terms if term in content_lower)

        # Boost score based on term density
        boost = min(0.2, term_count * 0.05)

        return min(1.0, score + boost)

    def _process_strategic_content(
        self, strategy_file: StrategyFile, content: str, is_update: bool = False
    ):
        """Process strategic content with all intelligence systems"""
        try:
            # Store in strategic memory
            if self.memory_manager:
                context_data = {
                    "workspace_file": strategy_file.to_dict(),
                    "processing_type": "update" if is_update else "new",
                    "stakeholders_detected": strategy_file.stakeholders,
                    "strategic_value": strategy_file.strategic_value,
                }

                critical_indicators = ["workspace_intelligence"]
                if strategy_file.strategic_value > 0.7:
                    critical_indicators.append("high_value_content")
                if strategy_file.stakeholders:
                    critical_indicators.append("stakeholder_content")

                self.memory_manager.preserve_context(
                    context_data=context_data, critical_indicators=critical_indicators
                )

            # Process with stakeholder intelligence
            if self.stakeholder_intelligence and strategy_file.stakeholders:
                context = {
                    "file_path": strategy_file.path,
                    "file_type": strategy_file.file_type,
                    "category": "workspace_monitoring",
                }

                self.stakeholder_intelligence.process_content_for_stakeholders(
                    content,
                    context,
                    auto_create=False,  # Don't auto-create from workspace monitoring
                )

            # Process with meeting intelligence (legacy compatibility)
            if self.meeting_manager and strategy_file.file_type == "meeting_prep":
                self.meeting_manager.process_meeting_document(
                    strategy_file.path, content
                )

        except Exception as e:
            self.logger.error(f"Error processing strategic content: {e}")


class WorkspaceMonitorUnified:
    """
    Unified Workspace Monitor - Phase 9 Single Source of Truth

    Consolidates functionality from:
    - StrategicWorkspaceMonitor (memory layer)
    - WorkspaceIntegration monitoring features
    - File system watching capabilities
    """

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        db_path: Optional[str] = None,
        enable_performance: bool = True,
        auto_start: bool = False,
    ):
        self.workspace_root = workspace_root or Path("leadership-workspace")
        self.db_path = db_path
        self.enable_performance = enable_performance

        # Initialize handler
        self.handler = StrategicWorkspaceHandler(
            db_path=db_path,
            workspace_root=self.workspace_root,
            enable_performance=enable_performance,
        )

        # Initialize observer
        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.workspace_root), recursive=True)

        self.is_monitoring = False
        self.logger = logging.getLogger(__name__)

        if auto_start:
            self.start_monitoring()

    def start_monitoring(self) -> bool:
        """Start workspace monitoring"""
        try:
            if not self.workspace_root.exists():
                self.workspace_root.mkdir(parents=True, exist_ok=True)

            if not self.is_monitoring:
                self.observer.start()
                self.is_monitoring = True
                self.logger.info(f"Started monitoring workspace: {self.workspace_root}")

            return True
        except Exception as e:
            self.logger.error(f"Failed to start workspace monitoring: {e}")
            return False

    def stop_monitoring(self) -> bool:
        """Stop workspace monitoring"""
        try:
            if self.is_monitoring:
                self.observer.stop()
                self.observer.join()
                self.is_monitoring = False
                self.logger.info("Stopped workspace monitoring")

            return True
        except Exception as e:
            self.logger.error(f"Failed to stop workspace monitoring: {e}")
            return False

    def scan_existing_files(self) -> Dict[str, Any]:
        """Scan existing files in workspace for strategic intelligence"""
        results = {
            "files_processed": 0,
            "strategic_files_found": 0,
            "stakeholders_detected": 0,
            "high_value_files": 0,
            "processing_errors": 0,
        }

        try:
            for file_path in self.workspace_root.rglob("*"):
                if file_path.is_file():
                    try:
                        if self.handler._should_process_file(file_path):
                            # Process existing file
                            content = self.handler._read_file_content(file_path)
                            if content:
                                file_type = self.handler._classify_file_type(file_path)
                                strategy_file = self.handler._create_strategy_file(
                                    file_path, file_type, content
                                )

                                results["files_processed"] += 1
                                results["strategic_files_found"] += 1

                                if strategy_file.stakeholders:
                                    results["stakeholders_detected"] += len(
                                        strategy_file.stakeholders
                                    )

                                if strategy_file.strategic_value > 0.7:
                                    results["high_value_files"] += 1

                                # Process strategic content
                                self.handler._process_strategic_content(
                                    strategy_file, content
                                )

                    except Exception as e:
                        results["processing_errors"] += 1
                        self.logger.warning(f"Error processing {file_path}: {e}")

        except Exception as e:
            self.logger.error(f"Error during workspace scan: {e}")

        return results

    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get workspace monitoring statistics"""
        return {
            "workspace_root": str(self.workspace_root),
            "is_monitoring": self.is_monitoring,
            "performance_enabled": self.enable_performance,
            "workspace_exists": self.workspace_root.exists(),
            "total_files": (
                len(list(self.workspace_root.rglob("*")))
                if self.workspace_root.exists()
                else 0
            ),
        }


# === FACTORY FUNCTIONS ===


def get_workspace_monitor(
    workspace_root: Optional[Path] = None,
    db_path: Optional[str] = None,
    enable_performance: bool = True,
    auto_start: bool = False,
) -> WorkspaceMonitorUnified:
    """Get unified workspace monitor instance"""
    return WorkspaceMonitorUnified(
        workspace_root=workspace_root,
        db_path=db_path,
        enable_performance=enable_performance,
        auto_start=auto_start,
    )


def create_workspace_handler(
    db_path: Optional[str] = None,
    workspace_root: Optional[Path] = None,
    enable_performance: bool = True,
) -> StrategicWorkspaceHandler:
    """Create strategic workspace handler instance"""
    return StrategicWorkspaceHandler(
        db_path=db_path,
        workspace_root=workspace_root,
        enable_performance=enable_performance,
    )


# Legacy compatibility for migration period
class StrategicWorkspaceMonitor(WorkspaceMonitorUnified):
    """Legacy compatibility wrapper"""

    pass
