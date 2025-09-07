"""
Context Engineering Phase 2.1: Workspace Integration (TS-4 Enhanced)

This module provides intelligent workspace monitoring and strategic document
integration for ClaudeDirector's Context Engineering system.

Capabilities:
- File system monitoring for strategic documents
- Automatic context extraction from workspace files
- Cross-session context persistence
- Strategic initiative detection from documents
- TS-4: Enhanced strategic context analysis and code-strategic mapping
- TS-4: Workflow optimization suggestions and efficiency tracking
- TS-4: Advanced document analysis with framework recommendations
"""

import os
import json
import sqlite3
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict

# TS-4: Import strategic analysis capabilities
try:
    from ..integration.code_strategic_mapper import (
        CodeStrategicMapper,
        StrategicRecommendation,
    )

    TS4_STRATEGIC_ANALYSIS_AVAILABLE = True
except ImportError:
    TS4_STRATEGIC_ANALYSIS_AVAILABLE = False

    # Lightweight fallback for graceful degradation
    class StrategicRecommendation:
        def __init__(self, **kwargs):
            pass


try:
    from watchdog.observers import Observer
    from watchdog.events import (
        FileSystemEventHandler,
        FileModifiedEvent,
        FileCreatedEvent,
    )

    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

    # Fallback minimal implementations
    class FileSystemEventHandler:
        def on_modified(self, event):
            pass

        def on_created(self, event):
            pass

        def on_deleted(self, event):
            pass

    class Observer:
        def schedule(self, handler, path, recursive=False):
            pass

        def start(self):
            pass

        def stop(self):
            pass

        def join(self):
            pass

    class FileModifiedEvent:
        def __init__(self, src_path):
            self.src_path = src_path

    class FileCreatedEvent:
        def __init__(self, src_path):
            self.src_path = src_path


logger = logging.getLogger(__name__)


# Configuration constants (SOLID: DRY principle)
PRIORITY_LEVELS = {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}

FILE_TYPES = {
    "INITIATIVE": "initiative",
    "MEETING_PREP": "meeting_prep",
    "STRATEGY": "strategy",
    "ANALYSIS": "analysis",
    "BUDGET": "budget",
    "REPORT": "report",
    "GENERAL": "general",
}


# TS-4: Enhanced Strategic Analysis Data Models
@dataclass
class TS4StrategicInsight:
    """TS-4: Enhanced strategic insight from workspace analysis"""

    file_path: str
    insight_type: (
        str  # 'framework_recommendation', 'workflow_optimization', 'strategic_pattern'
    )
    confidence_score: float
    recommendation: str
    strategic_frameworks: List[str]
    efficiency_opportunities: List[str]
    stakeholder_impact: str
    priority_level: str  # 'high', 'medium', 'low'
    timestamp: datetime


@dataclass
class TS4WorkflowMetrics:
    """TS-4: Workflow efficiency metrics and optimization suggestions"""

    document_velocity: float  # docs/hour
    strategic_alignment_score: float  # 0-1
    framework_utilization_rate: float  # 0-1
    efficiency_opportunities: List[str]
    bottleneck_indicators: List[str]
    optimization_suggestions: List[str]
    last_calculated: datetime


class TS4StrategicAnalyzer:
    """
    TS-4: Enhanced strategic analysis for workspace integration

    Follows SOLID principles:
    - Single Responsibility: Strategic analysis only
    - Open/Closed: Extensible through composition
    - Liskov Substitution: Implements consistent interface
    - Interface Segregation: Focused strategic analysis interface
    - Dependency Inversion: Depends on abstractions (CodeStrategicMapper)
    """

    def __init__(self):
        self.strategic_mapper = (
            CodeStrategicMapper() if TS4_STRATEGIC_ANALYSIS_AVAILABLE else None
        )
        self.insights_cache: Dict[str, TS4StrategicInsight] = {}
        self.workflow_metrics: Optional[TS4WorkflowMetrics] = None

    def analyze_strategic_document(
        self, file_path: str, content: str
    ) -> Optional[TS4StrategicInsight]:
        """Analyze document for strategic insights using TS-4 capabilities"""
        if not self.strategic_mapper:
            return None

        try:
            # Use code-strategic mapper for document analysis
            strategic_context = self.strategic_mapper.analyze_strategic_context(
                content, {"file_path": file_path, "content_type": "document"}
            )

            if not strategic_context:
                return None

            insight = TS4StrategicInsight(
                file_path=file_path,
                insight_type=self._determine_insight_type(content),
                confidence_score=strategic_context.confidence_score,
                recommendation=self._generate_document_recommendation(
                    strategic_context
                ),
                strategic_frameworks=strategic_context.recommended_frameworks,
                efficiency_opportunities=strategic_context.efficiency_opportunities,
                stakeholder_impact=self._assess_stakeholder_impact(strategic_context),
                priority_level=self._determine_priority_level(strategic_context),
                timestamp=datetime.now(),
            )

            # Cache for performance (DRY: reuse cached results)
            self.insights_cache[file_path] = insight
            return insight

        except Exception as e:
            logger.warning(f"TS-4 strategic analysis failed for {file_path}: {e}")
            return None

    def calculate_workflow_metrics(
        self, strategic_files: Dict[str, Any]
    ) -> TS4WorkflowMetrics:
        """Calculate workflow efficiency metrics"""
        if not strategic_files:
            return self._create_empty_metrics()

        # Calculate document velocity (simplified)
        recent_files = self._get_recent_files(strategic_files)
        document_velocity = len(recent_files) / 24.0  # docs per hour

        # Calculate strategic alignment score
        alignment_score = self._calculate_alignment_score(strategic_files)

        # Framework utilization rate
        utilization_rate = self._calculate_utilization_rate()

        return TS4WorkflowMetrics(
            document_velocity=document_velocity,
            strategic_alignment_score=alignment_score,
            framework_utilization_rate=utilization_rate,
            efficiency_opportunities=self._identify_efficiency_opportunities(
                strategic_files
            ),
            bottleneck_indicators=self._identify_bottlenecks(strategic_files),
            optimization_suggestions=self._generate_optimization_suggestions(
                strategic_files
            ),
            last_calculated=datetime.now(),
        )

    def _create_empty_metrics(self) -> TS4WorkflowMetrics:
        """Create empty metrics for graceful handling"""
        return TS4WorkflowMetrics(
            document_velocity=0.0,
            strategic_alignment_score=0.0,
            framework_utilization_rate=0.0,
            efficiency_opportunities=[],
            bottleneck_indicators=[],
            optimization_suggestions=[],
            last_calculated=datetime.now(),
        )

    def _get_recent_files(self, strategic_files: Dict[str, Any]) -> List[Any]:
        """Get files modified in last 24 hours"""
        return [
            f
            for f in strategic_files.values()
            if hasattr(f, "last_modified")
            and f.last_modified > datetime.now() - timedelta(hours=24)
        ]

    def _calculate_alignment_score(self, strategic_files: Dict[str, Any]) -> float:
        """Calculate strategic alignment score"""
        framework_mentions = sum(
            1
            for f in strategic_files.values()
            if hasattr(f, "strategic_topics") and f.strategic_topics
        )
        return min(framework_mentions / max(len(strategic_files), 1), 1.0)

    def _calculate_utilization_rate(self) -> float:
        """Calculate framework utilization rate"""
        if not self.insights_cache:
            return 0.0
        files_with_frameworks = sum(
            1
            for insight in self.insights_cache.values()
            if insight.strategic_frameworks
        )
        return files_with_frameworks / len(self.insights_cache)

    def _determine_insight_type(self, content: str) -> str:
        """Determine the type of strategic insight from content"""
        content_lower = content.lower()
        if any(fw in content_lower for fw in ["framework", "methodology", "approach"]):
            return "framework_recommendation"
        elif any(opt in content_lower for opt in ["optimize", "improve", "efficiency"]):
            return "workflow_optimization"
        else:
            return "strategic_pattern"

    def _generate_document_recommendation(self, strategic_context) -> str:
        """Generate actionable recommendation from strategic context"""
        if (
            hasattr(strategic_context, "priority_actions")
            and strategic_context.priority_actions
        ):
            return f"Priority action: {strategic_context.priority_actions[0]}"
        elif (
            hasattr(strategic_context, "recommended_frameworks")
            and strategic_context.recommended_frameworks
        ):
            return f"Consider applying {strategic_context.recommended_frameworks[0]} framework"
        else:
            return "Review for strategic alignment opportunities"

    def _assess_stakeholder_impact(self, strategic_context) -> str:
        """Assess stakeholder impact level"""
        if hasattr(strategic_context, "stakeholder_impact"):
            impact_score = strategic_context.stakeholder_impact
            if impact_score > 0.8:
                return "high"
            elif impact_score > 0.5:
                return "medium"
            else:
                return "low"
        return "medium"  # default

    def _determine_priority_level(self, strategic_context) -> str:
        """Determine priority level based on strategic context"""
        if hasattr(strategic_context, "decision_complexity"):
            complexity = strategic_context.decision_complexity
            if complexity > 0.7:
                return "high"
            elif complexity > 0.4:
                return "medium"
            else:
                return "low"
        return "medium"  # default

    def _identify_efficiency_opportunities(
        self, strategic_files: Dict[str, Any]
    ) -> List[str]:
        """Identify workflow efficiency opportunities"""
        opportunities = []

        # Check for duplicate strategic themes (DRY principle)
        duplicates = self._find_duplicate_themes(strategic_files)
        if duplicates:
            opportunities.append(
                f"Consolidate duplicate strategic themes: {', '.join(duplicates[:3])}"
            )

        # Check for missing framework applications
        if self._has_missing_frameworks(strategic_files):
            opportunities.append(
                "Apply strategic frameworks to increase decision quality"
            )

        return opportunities

    def _find_duplicate_themes(self, strategic_files: Dict[str, Any]) -> List[str]:
        """Find duplicate strategic themes across files"""
        all_topics = []
        for file_data in strategic_files.values():
            if hasattr(file_data, "strategic_topics"):
                all_topics.extend(file_data.strategic_topics)

        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        return [topic for topic, count in topic_counts.items() if count > 3]

    def _has_missing_frameworks(self, strategic_files: Dict[str, Any]) -> bool:
        """Check if many files lack framework applications"""
        files_without_frameworks = sum(
            1
            for f in strategic_files.values()
            if hasattr(f, "strategic_topics")
            and not any("framework" in topic.lower() for topic in f.strategic_topics)
        )
        return files_without_frameworks > len(strategic_files) * 0.5

    def _identify_bottlenecks(self, strategic_files: Dict[str, Any]) -> List[str]:
        """Identify workflow bottlenecks"""
        bottlenecks = []

        # Check for stale documents
        stale_threshold = datetime.now() - timedelta(days=7)
        stale_files = [
            f
            for f in strategic_files.values()
            if hasattr(f, "last_modified") and f.last_modified < stale_threshold
        ]

        if len(stale_files) > len(strategic_files) * 0.3:
            bottlenecks.append("High number of stale strategic documents")

        return bottlenecks

    def _generate_optimization_suggestions(
        self, strategic_files: Dict[str, Any]
    ) -> List[str]:
        """Generate workflow optimization suggestions"""
        suggestions = []

        # Suggest framework standardization
        if len(strategic_files) > 5:
            suggestions.append(
                "Standardize strategic framework application across documents"
            )

        # Suggest automation opportunities
        suggestions.append("Consider automated strategic theme extraction")

        return suggestions


@dataclass
class StrategyFile:
    """Represents a strategic document in the workspace"""

    path: str
    file_type: str  # 'initiative', 'meeting_prep', 'strategy', 'analysis', 'budget'
    last_modified: datetime
    content_hash: str
    strategic_topics: List[str]
    stakeholders_mentioned: List[str]
    initiatives_referenced: List[str]
    priority_level: str  # 'high', 'medium', 'low'


@dataclass
class WorkspaceContext:
    """Strategic context extracted from workspace files"""

    active_initiatives: List[str]
    recent_meetings: List[str]
    stakeholder_activity: Dict[str, List[str]]
    strategic_themes: List[str]
    priority_files: List[str]
    last_updated: datetime


class StrategicFileHandler(FileSystemEventHandler):
    """Handles file system events for strategic documents"""

    def __init__(self, workspace_monitor: "WorkspaceMonitor"):
        self.workspace_monitor = workspace_monitor
        self.strategic_extensions = {".md", ".yaml", ".txt", ".json"}
        self.strategic_directories = {
            "current-initiatives",
            "meeting-prep",
            "strategy",
            "analysis",
            "budget-planning",
            "reports",
        }

    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory and self._is_strategic_file(event.src_path):
            logger.info(f"Strategic file modified: {event.src_path}")
            self.workspace_monitor.process_file_change(event.src_path, "modified")

    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory and self._is_strategic_file(event.src_path):
            logger.info(f"Strategic file created: {event.src_path}")
            self.workspace_monitor.process_file_change(event.src_path, "created")

    def _is_strategic_file(self, file_path: str) -> bool:
        """Determine if a file is strategically relevant"""
        path = Path(file_path)

        # Check extension
        if path.suffix.lower() not in self.strategic_extensions:
            return False

        # Check if in strategic directory
        path_parts = path.parts
        for part in path_parts:
            if part in self.strategic_directories:
                return True

        # Check for strategic keywords in filename
        strategic_keywords = {
            "strategy",
            "initiative",
            "meeting",
            "stakeholder",
            "analysis",
            "budget",
            "planning",
            "roadmap",
        }
        filename_lower = path.name.lower()
        return any(keyword in filename_lower for keyword in strategic_keywords)


class WorkspaceMonitor:
    """Monitors workspace for strategic document changes and extracts context"""

    def __init__(self, workspace_path: str, context_cache_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path)
        self.context_cache_path = context_cache_path or str(
            self.workspace_path / ".context-cache"
        )
        self.cache_db_path = Path(self.context_cache_path) / "workspace-context.db"

        # Ensure cache directory exists
        Path(self.context_cache_path).mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

        # File system monitoring
        self.observer = Observer()
        self.file_handler = StrategicFileHandler(self)

        # Context state
        self.current_context: Optional[WorkspaceContext] = None
        self.strategic_files: Dict[str, StrategyFile] = {}

        # TS-4: Enhanced strategic analysis capabilities
        self.ts4_analyzer = TS4StrategicAnalyzer()
        self.ts4_insights: Dict[str, TS4StrategicInsight] = {}
        self.ts4_metrics: Optional[TS4WorkflowMetrics] = None

        logger.info(
            f"WorkspaceMonitor initialized for {workspace_path} with TS-4 enhancements"
        )

    def _init_database(self):
        """Initialize SQLite database for context cache"""
        with sqlite3.connect(self.cache_db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS strategic_files (
                    path TEXT PRIMARY KEY,
                    file_type TEXT NOT NULL,
                    last_modified TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    strategic_topics TEXT,  -- JSON array
                    stakeholders_mentioned TEXT,  -- JSON array
                    initiatives_referenced TEXT,  -- JSON array
                    priority_level TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS workspace_context (
                    id INTEGER PRIMARY KEY,
                    active_initiatives TEXT,  -- JSON array
                    recent_meetings TEXT,  -- JSON array
                    stakeholder_activity TEXT,  -- JSON object
                    strategic_themes TEXT,  -- JSON array
                    priority_files TEXT,  -- JSON array
                    last_updated TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS context_sessions (
                    session_id TEXT PRIMARY KEY,
                    workspace_context_snapshot TEXT,  -- JSON
                    active_files TEXT,  -- JSON array
                    session_start TEXT NOT NULL,
                    session_end TEXT,
                    context_quality_score REAL
                )
            """
            )

            conn.commit()

    def start_monitoring(self):
        """Start file system monitoring"""
        try:
            self.observer.schedule(
                self.file_handler, str(self.workspace_path), recursive=True
            )
            self.observer.start()
            logger.info("Workspace monitoring started")

            # Perform initial scan
            self._initial_workspace_scan()

        except Exception as e:
            logger.error(f"Failed to start workspace monitoring: {e}")
            raise

    def stop_monitoring(self):
        """Stop file system monitoring"""
        if self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            logger.info("Workspace monitoring stopped")

    def _initial_workspace_scan(self):
        """Perform initial scan of workspace for strategic files"""
        logger.info("Performing initial workspace scan...")

        strategic_paths = [
            self.workspace_path / "current-initiatives",
            self.workspace_path / "meeting-prep",
            self.workspace_path / "strategy",
            self.workspace_path / "analysis",
            self.workspace_path / "budget-planning",
            self.workspace_path / "reports",
        ]

        for strategic_dir in strategic_paths:
            if strategic_dir.exists():
                for file_path in strategic_dir.rglob("*"):
                    if file_path.is_file() and self.file_handler._is_strategic_file(
                        str(file_path)
                    ):
                        self.process_file_change(str(file_path), "discovered")

        # Update workspace context after initial scan
        self._update_workspace_context()
        logger.info(
            f"Initial scan complete. Found {len(self.strategic_files)} strategic files"
        )

    def process_file_change(self, file_path: str, change_type: str):
        """Process a strategic file change"""
        try:
            path = Path(file_path)
            if not path.exists():
                # File deleted
                self._remove_strategic_file(file_path)
                return

            # Analyze file content
            strategy_file = self._analyze_strategic_file(file_path)
            if strategy_file:
                self.strategic_files[file_path] = strategy_file
                self._save_strategic_file(strategy_file)

                # TS-4: Enhanced strategic analysis
                self._perform_ts4_analysis(file_path, strategy_file)

                # Update workspace context
                self._update_workspace_context()

                logger.info(f"Processed strategic file: {file_path} ({change_type})")

        except Exception as e:
            logger.error(f"Error processing file change {file_path}: {e}")

    def _analyze_strategic_file(self, file_path: str) -> Optional[StrategyFile]:
        """Analyze a file for strategic content"""
        try:
            path = Path(file_path)

            # Read file content
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # Calculate content hash
            content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()

            # Determine file type based on path
            file_type = self._classify_file_type(file_path)

            # Extract strategic information
            strategic_topics = self._extract_strategic_topics(content)
            stakeholders = self._extract_stakeholders(content)
            initiatives = self._extract_initiatives(content)
            priority = self._assess_priority(content, file_type)

            return StrategyFile(
                path=file_path,
                file_type=file_type,
                last_modified=datetime.fromtimestamp(path.stat().st_mtime),
                content_hash=content_hash,
                strategic_topics=strategic_topics,
                stakeholders_mentioned=stakeholders,
                initiatives_referenced=initiatives,
                priority_level=priority,
            )

        except Exception as e:
            logger.error(f"Error analyzing strategic file {file_path}: {e}")
            return None

    def _classify_file_type(self, file_path: str) -> str:
        """Classify the type of strategic file"""
        path_lower = file_path.lower()

        if "current-initiatives" in path_lower or "initiative" in path_lower:
            return FILE_TYPES["INITIATIVE"]
        elif "meeting-prep" in path_lower or "meeting" in path_lower:
            return FILE_TYPES["MEETING_PREP"]
        elif "strategy" in path_lower:
            return FILE_TYPES["STRATEGY"]
        elif "analysis" in path_lower:
            return FILE_TYPES["ANALYSIS"]
        elif "budget" in path_lower:
            return FILE_TYPES["BUDGET"]
        elif "report" in path_lower:
            return FILE_TYPES["REPORT"]
        else:
            return FILE_TYPES["GENERAL"]

    def _extract_strategic_topics(self, content: str) -> List[str]:
        """Extract strategic topics from content"""
        strategic_keywords = {
            "platform strategy",
            "organizational design",
            "team topology",
            "stakeholder management",
            "resource allocation",
            "technical debt",
            "architecture decision",
            "engineering efficiency",
            "cross-team coordination",
            "strategic initiative",
            "roadmap planning",
            "capacity planning",
            "vendor evaluation",
            "technology assessment",
            "roi analysis",
        }

        content_lower = content.lower()
        found_topics = []

        for topic in strategic_keywords:
            if topic in content_lower:
                found_topics.append(topic)

        return found_topics

    def _extract_stakeholders(self, content: str) -> List[str]:
        """Extract mentioned stakeholders from content"""
        # Common stakeholder patterns
        stakeholder_patterns = [
            r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",  # Name patterns
            r"\b(VP|CTO|Director|Manager|Principal|Staff) [A-Z][a-z]+\b",  # Title patterns
        ]

        import re

        stakeholders = set()

        for pattern in stakeholder_patterns:
            matches = re.findall(pattern, content)
            stakeholders.update(matches)

        # Filter out common false positives
        false_positives = {
            "Code Review",
            "Pull Request",
            "Design System",
            "User Interface",
        }
        stakeholders = {s for s in stakeholders if s not in false_positives}

        return list(stakeholders)[:10]  # Limit to top 10

    def _extract_initiatives(self, content: str) -> List[str]:
        """Extract initiative references from content"""
        import re

        # Look for initiative patterns
        initiative_patterns = [
            r"Initiative[:\s]+([A-Z][^.\n]*)",
            r"Project[:\s]+([A-Z][^.\n]*)",
            r"Epic[:\s]+([A-Z][^.\n]*)",
            r"PI[-\s]?\d+[:\s]+([A-Z][^.\n]*)",
        ]

        initiatives = set()
        for pattern in initiative_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            initiatives.update(
                match.strip() for match in matches if len(match.strip()) > 5
            )

        return list(initiatives)[:5]  # Limit to top 5

    def _assess_priority(self, content: str, file_type: str) -> str:
        """Assess the priority level of the strategic file"""
        content_lower = content.lower()

        # High priority indicators
        high_priority_indicators = {
            "critical",
            "urgent",
            "p0",
            "blocking",
            "executive",
            "board",
            "deadline",
            "milestone",
            "risk",
            "escalation",
        }

        # Medium priority indicators
        medium_priority_indicators = {
            "important",
            "significant",
            "strategic",
            "planning",
            "roadmap",
        }

        # Count indicators
        high_count = sum(
            1 for indicator in high_priority_indicators if indicator in content_lower
        )
        medium_count = sum(
            1 for indicator in medium_priority_indicators if indicator in content_lower
        )

        # File type priority boost
        if file_type in ["meeting_prep", "initiative"]:
            high_count += 1
        elif file_type in ["strategy", "analysis"]:
            medium_count += 1

        if high_count >= 2:
            return PRIORITY_LEVELS["HIGH"]
        elif medium_count >= 2 or high_count >= 1:
            return PRIORITY_LEVELS["MEDIUM"]
        else:
            return PRIORITY_LEVELS["LOW"]

    def _save_strategic_file(self, strategy_file: StrategyFile):
        """Save strategic file to database"""
        now = datetime.now().isoformat()

        with sqlite3.connect(self.cache_db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO strategic_files (
                    path, file_type, last_modified, content_hash,
                    strategic_topics, stakeholders_mentioned, initiatives_referenced,
                    priority_level, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    strategy_file.path,
                    strategy_file.file_type,
                    strategy_file.last_modified.isoformat(),
                    strategy_file.content_hash,
                    json.dumps(strategy_file.strategic_topics),
                    json.dumps(strategy_file.stakeholders_mentioned),
                    json.dumps(strategy_file.initiatives_referenced),
                    strategy_file.priority_level,
                    now,
                    now,
                ),
            )
            conn.commit()

    def _remove_strategic_file(self, file_path: str):
        """Remove strategic file from tracking"""
        if file_path in self.strategic_files:
            del self.strategic_files[file_path]

        with sqlite3.connect(self.cache_db_path) as conn:
            conn.execute("DELETE FROM strategic_files WHERE path = ?", (file_path,))
            conn.commit()

    def _update_workspace_context(self):
        """Update overall workspace context based on current files"""
        try:
            # Aggregate information from all strategic files
            active_initiatives = []
            recent_meetings = []
            stakeholder_activity = {}
            strategic_themes = []
            priority_files = []

            for file_path, strategy_file in self.strategic_files.items():
                # Collect initiatives
                active_initiatives.extend(strategy_file.initiatives_referenced)

                # Collect recent meetings (within last 30 days)
                if (
                    strategy_file.file_type == "meeting_prep"
                    and strategy_file.last_modified
                    > datetime.now() - timedelta(days=30)
                ):
                    recent_meetings.append(file_path)

                # Collect stakeholder activity
                for stakeholder in strategy_file.stakeholders_mentioned:
                    if stakeholder not in stakeholder_activity:
                        stakeholder_activity[stakeholder] = []
                    stakeholder_activity[stakeholder].append(file_path)

                # Collect strategic themes
                strategic_themes.extend(strategy_file.strategic_topics)

                # Collect priority files
                if strategy_file.priority_level == PRIORITY_LEVELS["HIGH"]:
                    priority_files.append(file_path)

            # Deduplicate and limit
            active_initiatives = list(set(active_initiatives))[:10]
            strategic_themes = list(set(strategic_themes))[:15]
            priority_files = priority_files[:10]

            # Create workspace context
            self.current_context = WorkspaceContext(
                active_initiatives=active_initiatives,
                recent_meetings=recent_meetings,
                stakeholder_activity=stakeholder_activity,
                strategic_themes=strategic_themes,
                priority_files=priority_files,
                last_updated=datetime.now(),
            )

            # Save to database
            self._save_workspace_context()

        except Exception as e:
            logger.error(f"Error updating workspace context: {e}")

    def _save_workspace_context(self):
        """Save workspace context to database"""
        if not self.current_context:
            return

        now = datetime.now().isoformat()

        with sqlite3.connect(self.cache_db_path) as conn:
            # Remove old context entries (keep only latest)
            conn.execute("DELETE FROM workspace_context")

            # Insert new context
            conn.execute(
                """
                INSERT INTO workspace_context (
                    active_initiatives, recent_meetings, stakeholder_activity,
                    strategic_themes, priority_files, last_updated, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    json.dumps(self.current_context.active_initiatives),
                    json.dumps(self.current_context.recent_meetings),
                    json.dumps(self.current_context.stakeholder_activity),
                    json.dumps(self.current_context.strategic_themes),
                    json.dumps(self.current_context.priority_files),
                    self.current_context.last_updated.isoformat(),
                    now,
                ),
            )
            conn.commit()

    def get_workspace_context(self) -> Optional[WorkspaceContext]:
        """Get current workspace context"""
        return self.current_context

    def get_strategic_files_by_type(self, file_type: str) -> List[StrategyFile]:
        """Get strategic files of a specific type"""
        return [sf for sf in self.strategic_files.values() if sf.file_type == file_type]

    def get_priority_files(self, priority: str = None) -> List[StrategyFile]:
        """Get files by priority level"""
        if priority is None:
            priority = PRIORITY_LEVELS["HIGH"]
        return [
            sf for sf in self.strategic_files.values() if sf.priority_level == priority
        ]

    def save_session_context(self, session_id: str, context_quality_score: float = 0.0):
        """Save current context as a session snapshot"""
        if not self.current_context:
            return

        now = datetime.now().isoformat()

        with sqlite3.connect(self.cache_db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO context_sessions (
                    session_id, workspace_context_snapshot, active_files,
                    session_start, context_quality_score
                ) VALUES (?, ?, ?, ?, ?)
            """,
                (
                    session_id,
                    json.dumps(asdict(self.current_context), default=str),
                    json.dumps(list(self.strategic_files.keys())),
                    now,
                    context_quality_score,
                ),
            )
            conn.commit()

    def load_session_context(self, session_id: str) -> Optional[WorkspaceContext]:
        """Load context from a previous session"""
        with sqlite3.connect(self.cache_db_path) as conn:
            cursor = conn.execute(
                """
                SELECT workspace_context_snapshot FROM context_sessions
                WHERE session_id = ?
            """,
                (session_id,),
            )

            row = cursor.fetchone()
            if row:
                context_data = json.loads(row[0])
                # Convert datetime strings back to datetime objects
                context_data["last_updated"] = datetime.fromisoformat(
                    context_data["last_updated"]
                )
                return WorkspaceContext(**context_data)

        return None

    # TS-4: Enhanced Strategic Analysis Methods
    def _perform_ts4_analysis(self, file_path: str, strategy_file: StrategyFile):
        """Perform TS-4 enhanced strategic analysis on a file"""
        try:
            # Read file content for analysis
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Generate strategic insights
            insight = self.ts4_analyzer.analyze_strategic_document(file_path, content)
            if insight:
                self.ts4_insights[file_path] = insight
                logger.info(
                    f"TS-4 strategic insight generated for {file_path}: {insight.insight_type}"
                )

            # Update workflow metrics
            self.ts4_metrics = self.ts4_analyzer.calculate_workflow_metrics(
                self.strategic_files
            )

        except Exception as e:
            logger.warning(f"TS-4 analysis failed for {file_path}: {e}")

    def get_ts4_strategic_insights(
        self, file_type: str = None
    ) -> List[TS4StrategicInsight]:
        """Get TS-4 strategic insights, optionally filtered by file type"""
        insights = list(self.ts4_insights.values())

        if file_type:
            # Filter by file type if specified
            filtered_insights = []
            for insight in insights:
                if file_path := insight.file_path:
                    if strategy_file := self.strategic_files.get(file_path):
                        if strategy_file.file_type == file_type:
                            filtered_insights.append(insight)
            return filtered_insights

        return insights

    def get_ts4_workflow_metrics(self) -> Optional[TS4WorkflowMetrics]:
        """Get current TS-4 workflow metrics"""
        return self.ts4_metrics

    def get_ts4_efficiency_recommendations(self) -> List[str]:
        """Get TS-4 efficiency recommendations"""
        if not self.ts4_metrics:
            return []

        recommendations = []
        recommendations.extend(self.ts4_metrics.efficiency_opportunities)
        recommendations.extend(self.ts4_metrics.optimization_suggestions)

        # Add insight-based recommendations
        high_priority_insights = [
            insight
            for insight in self.ts4_insights.values()
            if insight.priority_level == "high"
        ]

        for insight in high_priority_insights[:3]:  # Top 3 high-priority insights
            recommendations.append(f"High priority: {insight.recommendation}")

        return recommendations

    def get_ts4_strategic_summary(self) -> Dict[str, Any]:
        """Get comprehensive TS-4 strategic summary"""
        return {
            "total_insights": len(self.ts4_insights),
            "insights_by_type": self._group_insights_by_type(),
            "workflow_metrics": asdict(self.ts4_metrics) if self.ts4_metrics else None,
            "efficiency_recommendations": self.get_ts4_efficiency_recommendations(),
            "high_priority_files": self._get_high_priority_files(),
            "framework_utilization": self._calculate_framework_utilization(),
            "last_updated": datetime.now().isoformat(),
        }

    def _group_insights_by_type(self) -> Dict[str, int]:
        """Group insights by type for summary"""
        type_counts = {}
        for insight in self.ts4_insights.values():
            type_counts[insight.insight_type] = (
                type_counts.get(insight.insight_type, 0) + 1
            )
        return type_counts

    def _get_high_priority_files(self) -> List[str]:
        """Get list of high-priority files based on TS-4 analysis"""
        return [
            insight.file_path
            for insight in self.ts4_insights.values()
            if insight.priority_level == "high"
        ]

    def _calculate_framework_utilization(self) -> float:
        """Calculate framework utilization rate"""
        if not self.ts4_insights:
            return 0.0

        files_with_frameworks = sum(
            1 for insight in self.ts4_insights.values() if insight.strategic_frameworks
        )

        return files_with_frameworks / len(self.ts4_insights)

    def __enter__(self):
        """Context manager entry"""
        self.start_monitoring()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_monitoring()
